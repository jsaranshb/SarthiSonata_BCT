# Django Imports
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.db.models import Q

# Django Rest Framework (DRF) Imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

# Third-Party Library Imports
import pandas as pd

# Standard Library Imports
from datetime import date, datetime, timedelta
import os

# Project-Specific Imports
from user.views import get_db_engine
from .models import *

class BusinessCallingAPI(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    
    def get(self, request):
        context = {}
        user = cache.get('user')
        user_id = user.UserID

        # Calling calling team dashboard counts SP
        sql_query = f"""SET NOCOUNT ON;EXEC [SP_BCT_Dashboard_Counts] @bcd_Userid = {user_id};SET NOCOUNT OFF"""
        BCD_Dashboard_Count_df = pd.read_sql_query(sql_query,get_db_engine)

        # Today's Promise Counts
        todays_prmoise_total_count = BCD_Dashboard_Count_df['promise_count'][0]
        todays_promise_attempted_card_count = BCD_Dashboard_Count_df['att_promise_count'][0]
        tppcount = todays_prmoise_total_count - todays_promise_attempted_card_count

        # Collection Followup COunts
        collection_followup_total_count = BCD_Dashboard_Count_df['total_cfu_Count'][0]
        collection_followup_attempted_card_count = BCD_Dashboard_Count_df['att_cfu_Counts'][0]
        cfucount = collection_followup_total_count - collection_followup_attempted_card_count
        
        # Insert data into context dictionary
        context['tptcount'] = todays_prmoise_total_count
        context['tpacount'] = todays_promise_attempted_card_count
        context['tppcount'] = tppcount
        context['cfutcount'] = collection_followup_total_count
        context['cfuacount'] = collection_followup_attempted_card_count
        context['cfu_count_at'] = cfucount
        
        return Response(context)