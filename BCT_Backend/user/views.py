# Django Imports
from django.core.cache import cache
from django.http import JsonResponse
from django.contrib.auth import login, authenticate

# Django Rest Framework (DRF) Imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.tokens import RefreshToken

# Third-Party Library Imports
from sqlalchemy import create_engine
import pandas as pd
import base64
import json
import os

# Project-Specific Imports
from .models import *

# Define a global function for creating the database engine
def get_db_engine():
    user = os.getenv('DATABASE_USER')
    password = os.getenv('DATABASE_PASSWORD')
    db = os.getenv('DATABASE_NAME')
    server = os.getenv('DATABASE_HOST')
    engine = create_engine(f"mssql+pyodbc://{user}:{password}@{server}/{db}?driver=ODBC+Driver+17+for+SQL+Server")
    return engine

# Define global role IDs that are allowed
ROLE_IDS = [65, 63, 34, 35, 36, 13, 42, 43, 44, 33, 51, 56, 67, 41]

class DictToObject:
    def __init__(self, data):
        self.__dict__.update(data)

class Login(APIView):

    def get(self, request):
        UID = request.GET.get('UID')
        TID = request.GET.get('TID')

        if UID and UID[:3] == 'UC_':
            user = Mst_UserTbl.objects.filter(UserCode=UID).first()
            if user:
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)

                # SQL Logic for role handling
                engine = get_db_engine()
                sql_query = f"SET NOCOUNT ON;EXEC [Sonata_Connect].[dbo].[UserDetails_New] @userid = {user.UserID};SET NOCOUNT OFF"
                df = pd.read_sql_query(sql_query, engine)

                if len(df) > 1:
                    df = df[df['RoleId'].isin(ROLE_IDS)]
                    df = df.reset_index(drop=True).sort_values(by=['RoleId'], ascending=True)

                    # Check role and redirect accordingly
                    if df['RoleName'][0] == 'BRO':
                        request.session['calling_number_registerd'] = is_calling_number_registered(request)
                        if not request.session['calling_number_registerd']:
                            return Response({'message': 'Redirect to register calling number'}, status=status.HTTP_302_FOUND)
                        return Response({'access_token': str(refresh.access_token), 'role': 'BRO', 'message': 'Redirect to BRO page'}, status=status.HTTP_200_OK)
                    else:
                        request.session['RoleName'] = df['RoleName'][0]
                        return Response({'access_token': str(refresh.access_token), 'role': df['RoleName'][0], 'message': 'Login successful'}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid User'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):

        # Get the request body
        data = json.loads(request.body)

        userid = data['username']
        # Decode the base64 encoded password
        password = decode_obfuscated_data(data['password'])

        # Handle UC_ users differently
        if userid and userid[:3] == 'UC_':
            user_sp_data = login_sp_data(request, userid, password)
    
            if user_sp_data not in [-1, 0, -2]:

                # Convert numpy.int64 to regular Python int
                user_sp_data = int(user_sp_data)
                try:
                    engine = get_db_engine()
                    query = f"select * from accounts_Mst_UserTbl where UserID={user_sp_data} and is_active=1 and IsDropout=0"
                    df = pd.read_sql_query(query, engine)
                    user_dict = df.to_dict(orient='records')[0]
                    user = DictToObject(user_dict)
                    
                    if user:
                        
                        # storing values in cache
                        user_data = DictToObject({'UserID':user_dict['UserID'], 'UserName':user_dict['UserName']})
                        cache.set('user', user_data)
                        calling_number = is_calling_number_registered(request, user.UserID)
                        cache.set('calling_number_registerd', calling_number)
                        
                        # Generate JWT tokens for the user
                        refresh = RefreshToken.for_user(user)
                        return JsonResponse({
                            'access_token': str(refresh.access_token),
                            'refresh_token': str(refresh),
                            'message': 'Login successful'
                        }, status=200)
                    else:
                        print("User not found")  # Debugging
                        return JsonResponse({'error': 'User not found'}, status=400)

                except Exception as e:
                    print(f"Error fetching user: {e}")
                    return JsonResponse({'error': 'Error fetching user data'}, status=500)
    
        return JsonResponse({'error': 'Invalid credentials'}, status=400)

class Logout(APIView):
    def post(self, request):
        
        cache.clear()

        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


# Decode function for password obfuscation
def decode_obfuscated_data(obfuscated_data):
    try:

        # Add padding if necessary
        missing_padding = len(obfuscated_data) % 4
        if missing_padding:
            obfuscated_data += '=' * (4 - missing_padding)

        decoded_data = base64.b64decode(obfuscated_data).decode('utf-8')
        return decoded_data
    except Exception as e:
        # Handle decoding errors
        print(f"Error decoding data: {e}")
        return None


# Function to authorize the user
def login_sp_data(request, userid, upassword):
    engine = get_db_engine()  # Use the global engine function
    sql_query = f"SET NOCOUNT ON;EXEC [Sonata_Connect].[dbo].[SP_Authorise_HRMSUser] '{userid}','{upassword}';SET NOCOUNT OFF"
    df = pd.read_sql_query(sql_query, engine)
    return df['USERID'].values[0] if len(df) > 0 else None

def is_calling_number_registered(request, userid):
    calling_obj = calling_number_list.objects.filter(UserID = userid).first()
    print(calling_obj)
    if calling_obj:
        return True
    else:
        return False