# Django Imports
from django.template.response import TemplateResponse
from django.contrib import messages
from django.core.cache import cache
from django.db.models import Max, Q
from django.http import JsonResponse
from django.utils.dateparse import parse_date

# Django Project Specific Imports
from .models import *
from user.models import *
from dashboard.models import *
from user.views import get_db_engine

# DRF (Django Rest Framework) Imports
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Third-Party Library Imports
from dateutil.relativedelta import relativedelta
import requests
import pandas as pd
import numpy as np
import json
import os

# Standard Library Imports
from datetime import date, datetime, timedelta

# import gupshup userid and password from .env
gupshup_uid = os.getenv("GUPSHUP_WHATSAPP_USERID")
gupshup_pass = os.getenv("GUPSHUP_WHATSAPP_PASSWORD")

class CollectionFollowUp(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):

        context = {}
        user = cache.get('user')

        from_date = date.today().replace(day=1)
        to_date = date.today()
        max_allocated_date = BusinessCallingData.objects.filter(Userid=user.UserID, IS_active=1).aggregate(Max('AllocatedDate'))['AllocatedDate__max']
        if max_allocated_date:

            calling_data = pd.DataFrame(BusinessCallingData.objects.filter(Userid=user.UserID, IS_active=True, AllocatedDate=max_allocated_date).values('DisbursementID', 'id', 'feedback_code', 'IS_active'))

            calling_data['id'] = calling_data['id'].astype(int,errors='ignore')

            calling_day_wise = pd.DataFrame(DayWiseSummarised.objects.filter(DisbursementID__in = calling_data['DisbursementID'].unique().tolist()).values('DisbursementID','UserID')).drop_duplicates(['DisbursementID'])

            calling_data = pd.merge(calling_day_wise,calling_data,left_on='DisbursementID',right_on='DisbursementID',how='inner')

            # collection follow up filtering
            calling_data = calling_data

            # 01-30 filtering logic
            firstcount = len(calling_data[calling_data['id']==8])
            firstcount_att = len(calling_data[(calling_data['id'].isin([8]))&(calling_data['feedback_code']==1)])
            firstcount_at = firstcount - firstcount_att
            context['firstcount']= firstcount
            context['firstcount_att']= firstcount_att
            context['firstcount_at']= firstcount_at

            # 31-60 filtering logic
            secondcount = len(calling_data[calling_data['id']==9])
            secondcount_att = len(calling_data[(calling_data['id'].isin([9]))&(calling_data['feedback_code']==1)])
            secondcount_at = secondcount - secondcount_att
            context['secondcount']= secondcount
            context['secondcount_att']= secondcount_att
            context['secondcount_at']= secondcount_at

            # 61-90 filtering logic
            thirdcount = len(calling_data[calling_data['id']==10])
            thirdcount_att = len(calling_data[(calling_data['id'].isin([10]))&(calling_data['feedback_code']==1)])
            thirdcount_at = thirdcount - thirdcount_att
            context['thirdcount']= thirdcount
            context['thirdcount_att']= thirdcount_att
            context['thirdcount_at']= thirdcount_at

            # NPA filtering logic
            npacount = len(calling_data[calling_data['id']==11])
            npacount_att = len(calling_data[(calling_data['id'].isin([11]))&(calling_data['feedback_code']==1)])
            npacount_at = npacount - npacount_att
            context['npacount']= npacount
            context['npacount_att']= npacount_att
            context['npacount_at']= npacount_at

            # Atilambit filtering logic
            atilcount = len(calling_data[calling_data['id']==12])
            atilcount_att = len(calling_data[(calling_data['id'].isin([12]))&(calling_data['feedback_code']==1)])
            atilcount_at = atilcount - atilcount_att
            context['atilcount']= atilcount
            context['atilcount_att']= atilcount_att
            context['atilcount_at']= atilcount_at

            # First Time arrear filtering logic
            ftacount = len(calling_data[calling_data['id']==13])
            ftacount_att = len(calling_data[(calling_data['id'].isin([13]))&(calling_data['feedback_code']==1)])
            ftacount_at = ftacount - ftacount_att
            context['ftacount']= ftacount
            context['ftacount_att']= ftacount_att
            context['ftacount_at']= ftacount_at

            upcoming_prmoise_card_count, upcoming_promise_attempted_card_count, uppcount, failed_prmoise_card_count, failed_promise_attempted_card_count, fppcount, cppcount, todays_prmoise_card_count, todays_promise_attempted_card_count, tppcount = 0,0,0,0,0,0,0,0,0,0

            context['upcoming_prmoise_card_count'] = upcoming_prmoise_card_count
            context['upcoming_promise_attempted_card_count'] = upcoming_promise_attempted_card_count
            context['uppcount'] = uppcount
            context['failed_prmoise_card_count'] = failed_prmoise_card_count
            context['failed_promise_attempted_card_count'] = failed_promise_attempted_card_count
            context['fppcount'] = fppcount
            context['cppcount'] = cppcount
            context['todays_prmoise_card_count'] = todays_prmoise_card_count
            context['todays_promise_attempted_card_count'] = todays_promise_attempted_card_count
            context['tppcount'] = tppcount

            context['ppcount'] = context['uppcount'] + context['fppcount'] + context['cppcount'] + context['tppcount']

            context['prmoise_card_count'] = context['upcoming_prmoise_card_count'] + context['failed_prmoise_card_count'] + context['todays_prmoise_card_count'] + context['cppcount']
            context['promise_attempted_card_count'] = context['upcoming_promise_attempted_card_count'] + context['failed_promise_attempted_card_count'] + context['todays_promise_attempted_card_count']

            context['total_count'] = firstcount + secondcount + thirdcount + npacount + atilcount + ftacount + context['prmoise_card_count']
            context['total_count_att'] = firstcount_att + secondcount_att + thirdcount_att + npacount_att + atilcount_att + ftacount_att + context['promise_attempted_card_count']
            # context['cfu'] = 'cfu'
            context['from_date'] = from_date
            context['to_date'] = to_date
            context['today_date'] = str(date.today())
        else:
            context['firstcount']= 0
            context['firstcount_att']= 0
            context['firstcount_at']= 0
            context['secondcount']= 0
            context['secondcount_att']= 0
            context['secondcount_at']= 0
            context['thirdcount']= 0
            context['thirdcount_att']= 0
            context['thirdcount_at']= 0
            context['npacount']= 0
            context['npacount_att']= 0
            context['npacount_at']= 0
            context['atilcount']= 0
            context['atilcount_att']= 0
            context['atilcount_at']= 0
            context['ftacount']= 0
            context['ftacount_att']= 0
            context['ftacount_at']= 0
            context['ppcount'] = 0
            context['promise_attempted_card_count'] = 0
            messages.error(request, "No Data Available")

        # Return a rendered HTML page using TemplateResponse
        return TemplateResponse(request, 'collection_follow_up.html', context)


def day_dict_creator():
    day_names=[]
    today_date = date.today()
    today_day = today_date.weekday()
    if today_day == 0:
        day_names=['Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','Monday']
    elif today_day == 1:
        day_names=['Wednesday','Thursday','Friday','Saturday','Sunday','Monday','Tuesday']
    elif today_day == 2:
        day_names=['Thursday','Friday','Saturday','Sunday','Monday','Tuesday','Wednesday']
    elif today_day == 3:
        day_names=['Friday','Saturday','Sunday','Monday','Tuesday','Wednesday','Thursday']
    elif today_day == 4:
        day_names=['Saturday','Sunday','Monday','Tuesday','Wednesday','Thursday','Friday']
    elif today_day == 5:
        day_names=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    elif today_day == 6:
        day_names=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    else:
        pass


    dates = []
    for i in range(1,8):
        dates.append(today_date + relativedelta(days=i))
    day_dict = dict(zip(day_names,dates))
    print('uiuiuiuiuiuiuui',day_dict)
    print('uiuiuiuiuiuiuui',today_date)
    return day_dict

def business_calling_card_data(request,id):

    user = cache.get('user')
    user_id = user.UserID
    db = os.getenv('DATABASE_NAME')

    engine = get_db_engine()
    sql_query = f"""SET NOCOUNT ON;EXEC [{db}].[dbo].[S_SP_BusinessCallingCardData] @bcd_Userid = {user_id},@bcd_id = {id} ;SET NOCOUNT OFF"""
    df=pd.read_sql_query(sql_query,engine)
    # df = df[df['Region_BuName'] == 'Sagar']
    # df[(df['BRO_UserID'] == 31063) & (df['AllocatedDate'] == '2023-05-01')]

    return df

class CallingBucket(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    def get(self, request, id):
        
        user = cache.get('user')
        user_id = user.UserID
        today_date = datetime.today()

        today= (today_date).strftime('%Y-%m-%d')
        tomorrow = (today_date + timedelta(days = 1)).strftime('%Y-%m-%d')
        day_aft_tomorrow = (today_date + timedelta(days = 2)).strftime('%Y-%m-%d')
        alloc_date = str(date.today()) + ' 00:00:00.000'

        bccd_df = business_calling_card_data(request,id)
        
        if len(bccd_df)<1:
            context={}
            messages.error(request,'No Data Found')
            print('error: DataFrame is Empty')
            # Return a rendered HTML page using TemplateResponse
            return TemplateResponse(request, 'business_temp.html', context)


        dates = bccd_df['AllocatedDate'].unique()
        bccd_df = bccd_df[bccd_df['AllocatedDate']==max(dates)]
        bccd_df = bccd_df[bccd_df['IS_active']==True]
        
        bccd_df = bccd_df.dropna(subset=['UserID'])
        
        try:
            bcd_data = pd.DataFrame(BusinessCallingData.objects.filter(
            Q(feedback_response__icontains='{"331205":{"status":true},"33120501":{"date"')&
            Q(Userid = user_id)
            ).values('Userid','DisbursementID','feedback_response'))
            def find_date(x):
                y = json.loads(str(x))
                if len(y) == 1:
                    return y[0]["33120501"]["date"]
                else:
                    for i in y:
                        try:
                            return i["33120501"]["date"]
                        except:
                            pass

            bcd_data['promises_date'] = bcd_data["feedback_response"].apply(find_date)
            bcd_data = bcd_data.sort_values(by=["promises_date"] , ascending = False)
        except:
            bcd_data = pd.DataFrame()

        print(bccd_df)
        print(bccd_df.columns)

        context = {}
        context['date'] = str(date.today())
        print('----------------',context['date'])
        context['dateand15days'] = str(date.today() + relativedelta(days=15))
        print(context['dateand15days'])
        context['id'] = id
        context['day_dict'] = day_dict_creator()
        context['feedback_observations'] = (pd.DataFrame(FeedbackObservations.objects.all().values())).to_dict('r')
        print(context['feedback_observations'])

        total_card_count = len(bccd_df)
        bccd_df = bccd_df[bccd_df['feedback_code']!=1]
        attempted_card_count = len(bccd_df)
        alloted_card_count = total_card_count - attempted_card_count
        if not bcd_data.empty:
            bccd_df = pd.merge(bccd_df,bcd_data,on='DisbursementID',how='left').drop_duplicates(subset='DisbursementID')
            bccd_df['promises_date'] = bccd_df['promises_date'].fillna(value='N/A')
        
        calling_day_wise = bccd_df

        try:
            calling_day_wise['CenterMeetingWeekday'] = None
            calling_day_wise.loc[calling_day_wise['CenterMeetingDay'] == 55,'CenterMeetingWeekday'] = 'Monday'
            calling_day_wise.loc[calling_day_wise['CenterMeetingDay'] == 56,'CenterMeetingWeekday'] = 'Tuesday'
            calling_day_wise.loc[calling_day_wise['CenterMeetingDay'] == 57,'CenterMeetingWeekday'] = 'Wednesday'
            calling_day_wise.loc[calling_day_wise['CenterMeetingDay'] == 58,'CenterMeetingWeekday'] = 'Thursday'
            calling_day_wise.loc[calling_day_wise['CenterMeetingDay'] == 59,'CenterMeetingWeekday'] = 'Friday'
            calling_day_wise.loc[calling_day_wise['CenterMeetingDay'] == 60,'CenterMeetingWeekday'] = 'Saturday'
            calling_day_wise.loc[calling_day_wise['CenterMeetingDay'] == 61,'CenterMeetingWeekday'] = 'Sunday'

            calling_day_wise["CenterMeetingTime"]=pd.to_datetime(calling_day_wise["CenterMeetingTime"])
            calling_day_wise["CenterMeetingTime"] = calling_day_wise["CenterMeetingTime"].dt.time

            calling_day_wise['Centercode'] = calling_day_wise['Centercode'].fillna(value='Unavailable')
            calling_day_wise['CenterName'] = calling_day_wise['CenterName'].fillna(value='Unavailable')
            calling_day_wise['CenterMeetingWeekday'] = calling_day_wise['CenterMeetingWeekday'].fillna(value='Unavailable')
            calling_day_wise['CenterMeetingDay'] = calling_day_wise['CenterMeetingDay'].fillna(value='Schedule Unavailable')
            calling_day_wise['CenterMeetingTime'] = calling_day_wise['CenterMeetingTime'].fillna(value='Schedule Unavailable')

        except Exception as e:
            context['total_card_count'] = 0
            context['attempted_card_count'] = 0
            context['alloted_card_count'] = 0
            messages.error(request,'No Data Found')
            print('error: calling day wise is empty', e)
            # Return a rendered HTML page using TemplateResponse
            return TemplateResponse(request, 'business_temp.html', context)

        promise_From_bcd = pd.DataFrame(BusinessCallingData.objects.filter(
            Q(feedback_response__icontains='{"331205":{"status":true},"33120501":{"date"')&
            Q(DisbursementID__in = calling_day_wise['DisbursementID'].to_list())
        ).values('DisbursementID','feedback_response'))
        if not promise_From_bcd.empty:
            def find_p_date(x):
                y = json.loads(str(x))
                if len(y) == 1:
                    return y[0]["33120501"]["date"]
                else:
                    for i in y:
                        try:
                            return i["33120501"]["date"]
                        except:
                            pass
            promise_From_bcd['promises_date'] = promise_From_bcd["feedback_response"].apply(find_p_date)
            cllc_date_dws = pd.DataFrame(DayWiseSummarised.objects.filter(
                DisbursementID__in = calling_day_wise['DisbursementID'].to_list()
            ).values('DisbursementID','latest_collected_date')).fillna(0)
            new_df = pd.merge(promise_From_bcd,cllc_date_dws,on='DisbursementID',how='left')
            new_df['last_broken_p_date'] = np.where(new_df['promises_date'] != new_df['latest_collected_date'], new_df['promises_date'], None)
            new_df['promises_date'] =  pd.to_datetime(new_df['promises_date'], format='%Y-%m-%d', errors='coerce')
            new_df = new_df[new_df['promises_date'] <= (datetime.today() - timedelta(days = 1))]
            new_df = new_df.drop_duplicates(subset='DisbursementID',keep='last').fillna(0)
            new_df = new_df[['DisbursementID','last_broken_p_date']]
            calling_day_wise = pd.merge(calling_day_wise,new_df,on='DisbursementID',how='left').fillna('N/A')
        
        calling_day_wise['pending_amount'] = calling_day_wise['pending_amount'].astype(int,errors='ignore')
        calling_day_wise['DisbursedAmt'] = calling_day_wise['DisbursedAmt'].astype(int,errors='ignore')
        calling_day_wise['current_installment_Amount'] = calling_day_wise['current_installment_Amount'].astype(int,errors='ignore')
        calling_day_wise['Other_Active_Accounts'] = calling_day_wise['Other_Active_Accounts'].astype(int,errors='ignore')
        calling_day_wise.eval('current_due_Amount = current_installment_Amount + pending_amount', inplace=True)
        calling_day_wise[['DisbursementDate','latest_collected_date',]] = calling_day_wise[['DisbursementDate','latest_collected_date']].apply(pd.to_datetime, errors='coerce',format='%Y-%m-%d')
        calling_day_wise.fillna(0,inplace=True)
        calling_day_wise = calling_day_wise.astype(str)
        calling_day_wise.loc[:, calling_day_wise.columns != 'calling_attempt'].replace("0","NA",inplace=True)



        #sort by calling_attempt
        
        calling_day_wise = calling_day_wise.sort_values(by=["calling_attempt","DisbursementID"] , ascending = True)
        calling_day_wise_0 = calling_day_wise[calling_day_wise['calling_attempt'] == '0'].sort_values(by="CallPriority" , ascending = True)
        calling_day_wise_1 = calling_day_wise[calling_day_wise['calling_attempt'] == '1'].sort_values(by="CallPriority" , ascending = True)
        calling_day_wise_2 = calling_day_wise[calling_day_wise['calling_attempt'] == '2'].sort_values(by="CallPriority" , ascending = True)
        calling_day_wise_3 = calling_day_wise[calling_day_wise['calling_attempt'] == '3'].sort_values(by="CallPriority" , ascending = True)
        calling_day_wise = pd.concat([calling_day_wise_0,calling_day_wise_1,calling_day_wise_2,calling_day_wise_3], axis=0, ignore_index=True)
        calling_day_wise = calling_day_wise.head(15) 

        context['day_wise_data'] = calling_day_wise.to_dict(orient="records")
        context['busi_calling'] = 1
        context['today'] = today
        context['tomorrow'] = tomorrow
        context['day_aft_tomorrow'] = day_aft_tomorrow
        context['total_card_count'] = total_card_count
        context['attempted_card_count'] = attempted_card_count
        context['alloted_card_count'] = alloted_card_count

        # Return a rendered HTML page using TemplateResponse
        return TemplateResponse(request, 'business_temp.html', context)
    
    def post(self, request, id):

        """This function is called when the Business Calling Team makes Submissions"""
        # TEST_REGION_ID = 3557 #Lucknow
        # belongs_to_test_region = region_checker(request, TEST_REGION_ID, request.POST.get('user_id'))

        user = cache.get('user')
        user_id = user.UserID
        business_caller_id = user.UserID
        UserName = str(user.UserName)
        call_feedback_json = request.POST.get('feedback_json')
        disbursementid = request.POST.get('disburstmentid')
        loaded = json.loads(call_feedback_json)
        customercode = request.POST.get('customercode')
        customerid = int(float(request.POST.get('custid')))
        broname = request.POST.get('broname')
        customer_contact_no = str(request.POST.get('mobile'))
        print(loaded,"feedback jsonnnnnnnnnnnnnnnnn")
        call_status, p2p_date, p2p_amt, alt_no, loan_purpose, loan_amt, task_id = [None] * 7

        try:
            customerinfoid = customerid
        except Exception as e:
            print('ERROR : ', str(e))

        # spuserid = user.UserID
        engine = get_db_engine()
        sql_query = f"""SET NOCOUNT ON;EXEC [Sonata_Connect].[dbo].[SP_UserHierarchy_Dynamic_07Jan23] @userid = 9755;SET NOCOUNT OFF"""
        df=pd.read_sql_query(sql_query,engine)

        if request.POST.get('retention') == 'true':
            msgx = []
            if request.POST.get('task3') == 'true': ## wrong number
                task_name = 'Wrong Number Communicated'
                user_id = request.POST.get('user_id')
                usr_instance = Mst_UserTbl.objects.get(UserID = int(request.POST.get('user_id')))
                created_by = Mst_UserTbl.objects.get(UserID = int(user.UserID))
                deadline_date = datetime.now()
                priority = '1'
                category = '10'
                applicant_name = request.POST.get('appname')
                applicant_number = request.POST.get('bronumber')
                alternate_number = None
                user_number = applicant_number
                ## create a message
                msgx = []

                for item in loaded:
                    for key,value in item.items():
                        if key == '331203':
                            msg1 = 'Customer (Customer id: ' + str(customerid) + ') has communicated wrong number|'
                            msgx.append(msg1)
                        if key == '33120301':
                            if value['feedback_3'] != '':
                                feedback_recvd = value['feedback_3']
                                msg2 = 'Feedback recieved: ' + value['feedback_3'] + '|'
                                msgx.append(msg2)
                        if key == '33120302':
                            alternate_number = value['alternate_num']
                            msg3 = 'Alternate number recieved ' + value['alternate_num'] + '|'
                            msgx.append(msg3)
                if len(msgx)>2:
                    msgx = (msgx[0] + msgx[1] + msgx[2])
                elif len(msgx)>1:
                    msgx = (msgx[0] + msgx[1])
                else:
                    msgx = msgx[0]

                msgx += f'Customer name {applicant_name} contact number {applicant_number}|'

                deadline_dt = None
                ## create a task for wrong number

                wn_task_obj = task_details()
                wn_task_obj.task_name = task_name
                wn_task_obj.task_description = msgx
                wn_task_obj.created_by = created_by
                wn_task_obj.assigned_to = usr_instance
                wn_task_obj.priority = priority
                wn_task_obj.t_info = disbursementid
                wn_task_obj.category = category
                wn_task_obj.deadline_date = deadline_date
                try:
                    wn_task_obj.feedback = feedback_recvd
                except:
                    wn_task_obj.feedback = ''

                wn_task_obj.save()
                task_id = wn_task_obj.task_id

                try:
                    issues_inst = CallingIssues()
                    issues_inst.category = 'Wrong Number Communicated'
                    issues_inst.disbursement_id = int(disbursementid)
                    issues_inst.customer_info_id = int(customerinfoid)
                    issues_inst.customer_name = CustomerLevelSummarised.objects.get(CustomerInfoID = int(customerinfoid)).ApplicantName
                    issues_inst.customer_number = CustomerLevelSummarised.objects.get(CustomerInfoID = int(customerinfoid)).mobile_no
                    issues_inst.save()
                except Exception as e:
                    print("calling issues inst not able to create : ", e)
                # applicant_number = Uncomment and Enter your number for testing flow 
                # Creating a Queue for wrong number
                # whatsapp queue logic
                # user_number = 'Uncomment and Enter your number for testing flow '
                # if belongs_to_test_region: # regionchecker
                try:
                    # Started Queueing WhatsApp Bot Flow for Wrong Number Tasks
                    # The first two flows -> [WNV_alert, WNV_flow] will be created everytime a task for WN is submitted
                    try :
                        queue_instance = WhatsAppQueue()
                        queue_instance.user_id = user_id
                        queue_instance.flow_name = 'WNV_alert'
                        queue_instance.status = 3
                        queue_instance.update_time = datetime.now()
                        queue_instance.contact_number = str(user_number)
                        queue_instance.field_1 = broname
                        queue_instance.field_2 = CustomerLevelSummarised.objects.get(CustomerInfoID = int(customerinfoid)).ApplicantName
                        queue_instance.field_3 = customercode
                        queue_instance.field_4 = alternate_number
                        queue_instance.field_5 = wn_task_obj.deadline_date.date()
                        queue_instance.field_6 = wn_task_obj.deadline_date.strftime('%H:%M')
                        queue_instance.field_12 = None
                        queue_instance.issue_id = issues_inst.id
                        queue_instance.field_13 = customer_contact_no
                        queue_instance.field_14 = customerinfoid
                        queue_instance.bc_id = business_caller_id
                        queue_instance.task_id = task_id
                        queue_instance.save()

                        print('storing visit flow  id ......')
                        visit_alert_id = queue_instance.id
                    except Exception as e:
                        print("WNV_alert", e)

                    try :
                        queue_instance = WhatsAppQueue()
                        queue_instance.user_id = user_id
                        queue_instance.flow_name = 'WNV_flow'
                        queue_instance.status = 3
                        queue_instance.update_time = datetime.now()
                        queue_instance.contact_number = str(user_number)
                        queue_instance.field_1 = broname
                        queue_instance.field_2 = CustomerLevelSummarised.objects.get(CustomerInfoID = int(customerinfoid)).ApplicantName
                        queue_instance.field_3 = customercode
                        queue_instance.field_4 = alternate_number
                        queue_instance.field_5 = wn_task_obj.deadline_date.date()
                        queue_instance.field_11 = visit_alert_id
                        queue_instance.field_12 = None
                        queue_instance.field_6 = wn_task_obj.deadline_date.strftime('%H:%M')
                        queue_instance.issue_id = issues_inst.id
                        queue_instance.field_13 = customer_contact_no
                        queue_instance.field_14 = customerinfoid
                        queue_instance.bc_id = business_caller_id
                        queue_instance.task_id = task_id
                        queue_instance.save()

                        print('storing visit flow  id ......')
                        visit_flow_id = queue_instance.id
                    except Exception as e:
                        print("WNV_flow", e)

                    if not alternate_number :
                        # If the Customer does not already have an alternate number , one flow -> [WNANP_flow] will be added to Queue
                        try :
                            queue_instance = WhatsAppQueue()
                            queue_instance.user_id = user_id
                            queue_instance.flow_name = 'WNANP_flow'
                            queue_instance.update_time = datetime.now()
                            queue_instance.contact_number = str(user_number)
                            queue_instance.field_1 = broname
                            queue_instance.field_2 = CustomerLevelSummarised.objects.get(CustomerInfoID = int(customerinfoid)).ApplicantName
                            queue_instance.field_3 = customercode
                            queue_instance.field_4 = alternate_number
                            queue_instance.field_5 = wn_task_obj.deadline_date.date()
                            queue_instance.field_6 = wn_task_obj.deadline_date.strftime('%H:%M')
                            queue_instance.field_7 = visit_alert_id
                            queue_instance.field_8 = visit_flow_id
                            queue_instance.field_12 = None
                            queue_instance.issue_id = issues_inst.id
                            queue_instance.field_13 = customer_contact_no
                            queue_instance.field_14 = customerinfoid
                            queue_instance.bc_id = business_caller_id
                            queue_instance.task_id = task_id
                            queue_instance.save()

                        except Exception as e:
                            print('WNANP_flow', e)


                    else : ## ALternate Number Present
                        # If the Customer already has an alternate number , two flows -> [WNAP_alert, WNAP_flow] will be added to Queue
                        try :
                            queue_instance = WhatsAppQueue()
                            queue_instance.user_id = user_id
                            queue_instance.flow_name = 'WNAP_alert'
                            queue_instance.update_time = datetime.now()
                            queue_instance.contact_number = str(user_number)
                            queue_instance.field_1 = broname
                            queue_instance.field_2 = CustomerLevelSummarised.objects.get(CustomerInfoID = int(customerinfoid)).ApplicantName
                            queue_instance.field_3 = customercode
                            queue_instance.field_4 = alternate_number
                            queue_instance.field_12 = None
                            queue_instance.field_5 = wn_task_obj.deadline_date.date()
                            queue_instance.field_6 = wn_task_obj.deadline_date.strftime('%H:%M')
                            queue_instance.field_7 = visit_alert_id
                            queue_instance.field_8 = visit_flow_id
                            queue_instance.issue_id = issues_inst.id
                            queue_instance.field_13 = customer_contact_no
                            queue_instance.field_14 = customerinfoid
                            queue_instance.bc_id = business_caller_id
                            queue_instance.task_id = task_id
                            queue_instance.save() 
                        except Exception as e:
                            print("WNAP_alert", e)
                        try :
                            from datetime import timedelta as td
                            queue_instance = WhatsAppQueue()
                            queue_instance.user_id = user_id
                            queue_instance.flow_name = 'WNAP_flow'
                            queue_instance.update_time = datetime.now() + td(hours=1)
                            queue_instance.contact_number = str(user_number)
                            queue_instance.field_1 = broname
                            queue_instance.field_2 = CustomerLevelSummarised.objects.get(CustomerInfoID = int(customerinfoid)).ApplicantName
                            queue_instance.field_3 = customercode
                            queue_instance.field_4 = alternate_number
                            queue_instance.field_5 = wn_task_obj.deadline_date.date()
                            queue_instance.field_12 = None
                            queue_instance.field_6 = wn_task_obj.deadline_date.strftime('%H:%M')
                            queue_instance.field_7 = visit_alert_id
                            queue_instance.field_8 = visit_flow_id
                            queue_instance.issue_id = issues_inst.id
                            queue_instance.field_13 = customer_contact_no
                            queue_instance.field_14 = customerinfoid
                            queue_instance.bc_id = business_caller_id
                            queue_instance.task_id = task_id
                            queue_instance.save() 
                        except Exception as e:
                            print("WNAP_flow", e)





                except Exception as e:
                    print("Wrong Number Communicated : ", e)

            elif request.POST.get('deny_status') == 'true':
                retention_call_obj = Retention_Calling_Data.objects.filter(DisbursementID = disbursementid).first()
                rejected_clients_inst = Retention_Rejected_Clients()
                rejected_clients_inst.Userid = retention_call_obj.Userid
                rejected_clients_inst.AllocatedDate = retention_call_obj.AllocatedDate
                rejected_clients_inst.DisbursementID = disbursementid
                rejected_clients_inst.save()

                branch_name = request.POST.get('branch_name')
                hub_id = request.POST.get('hub_id')
                rgn_id = request.POST.get('rgn_id')


                hub_userid = df[(df['RoleId'] == 36) & (df['U_BUID'] == int(hub_id))]['UserID'].iloc[0]
                rgn_userid = df[(df['RoleId'] == 35) & (df['U_BUID'] == int(rgn_id))]['UserID'].iloc[0]

                print(hub_userid, rgn_userid)

                task_name = 'Loan Rejected by Branch'
                created_by = Mst_UserTbl.objects.get(UserID = int(user.UserID))
                deadline_date = datetime.now()
                priority = '1'
                category = '18'
                applicant_name = request.POST.get('appname')
                customer_name = CustomerLevelSummarised.objects.get(CustomerInfoID = int(customerinfoid)).ApplicantName
                customer_code = str(customercode)
                task_desc = f'loan application submitted by our customer {customer_name}({customer_code}) has not been approved by the branch of {branch_name}.Your prompt attention to this matter is requested, thank you.'

                for user_id in [hub_userid,rgn_userid]:
                    # try:
                    task_assign_obj = task_details()
                    task_assign_obj.task_name = task_name
                    task_assign_obj.task_description = task_desc
                    task_assign_obj.created_by = created_by
                    task_assign_obj.priority = priority
                    task_assign_obj.t_info = disbursementid
                    task_assign_obj.category = category
                    task_assign_obj.deadline_date = deadline_date
                    usr_instance = Mst_UserTbl.objects.get(UserID = int(user_id))
                    task_assign_obj.assigned_to = usr_instance
                    task_assign_obj.save()

                    user_df = pd.DataFrame(calling_number_list.objects.filter(UserID=user_id).values())
                    user_number = user_df['CallingNumber'][0]
                    task_id = task_assign_obj.task_id
                    creator_name = request.user.UserName
                    creator_role = request.session["RoleName"]
                    category = task_assign_obj.category

                    if priority == "1":
                        priority_str = 'Immediate'
                    elif priority == "2":
                        priority_str = 'High'
                    elif priority == "3":
                        priority_str = 'Medium'
                    else:
                        priority_str = 'Low'
                    task_deadline = task_assign_obj.deadline_date.date()
                    print('params: ')
                    print(customer_name)
                    print('params: ')
                    # user_number = '8335076174'

                    url = f"https://media.smsgupshup.com/GatewayAPI/rest?userid=2000209909&password=z24gzBUA&send_to={user_number}&v=1.1&format=json&msg_type=TEXT&method=SENDMESSAGE&msg=%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF+%E0%A4%86%E0%A4%88%E0%A4%A1%E0%A5%80%3A+{task_id}%0A%E0%A4%86%E0%A4%AA%E0%A4%95%E0%A5%8B+%E0%A4%B6%E0%A5%8D%E0%A4%B0%E0%A5%80%E0%A4%AE%E0%A4%BE%E0%A4%A8+{creator_name}%28{creator_role}%29+%E0%A4%B8%E0%A5%87+%E0%A4%8F%E0%A4%95+%E0%A4%A8%E0%A4%AF%E0%A4%BE+%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF+%E0%A4%B8%E0%A5%8C%E0%A4%82%E0%A4%AA%E0%A4%BE+%E0%A4%97%E0%A4%AF%E0%A4%BE+%E0%A4%B9%E0%A5%88%E0%A5%A4%0A%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF+%E0%A4%B6%E0%A5%8D%E0%A4%B0%E0%A5%87%E0%A4%A3%E0%A5%80+{category}+%E0%A4%B9%E0%A5%88%E0%A5%A4%0A%E0%A4%89%E0%A4%AA%E0%A4%AD%E0%A5%8B%E0%A4%95%E0%A5%8D%E0%A4%A4%E0%A4%BE+%E0%A4%B5%E0%A4%BF%E0%A4%B5%E0%A4%B0%E0%A4%A3%3A+{customer_name}%28{customer_code}%29%0A%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF+%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%BE%E0%A4%A5%E0%A4%AE%E0%A4%BF%E0%A4%95%E0%A4%A4%E0%A4%BE+{priority_str}+%E0%A4%B9%E0%A5%88%E0%A5%A4%0A%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF+%E0%A4%95%E0%A5%80+%E0%A4%B8%E0%A4%AE%E0%A4%AF+%E0%A4%B8%E0%A5%80%E0%A4%AE%E0%A4%BE+%E0%A4%B9%E0%A5%88+{task_deadline}.%0A%E0%A4%85%E0%A4%A7%E0%A4%BF%E0%A4%95+%E0%A4%9C%E0%A4%BE%E0%A4%A8%E0%A4%A8%E0%A5%87+%E0%A4%95%E0%A5%87+%E0%A4%B2%E0%A4%BF%E0%A4%8F+%E0%A4%A8%E0%A5%80%E0%A4%9A%E0%A5%87+%E0%A4%A6%E0%A4%BF%E0%A4%8F+%E0%A4%97%E0%A4%8F+%E0%A4%B2%E0%A4%BF%E0%A4%82%E0%A4%95+%E0%A4%95%E0%A4%BE+%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%AF%E0%A5%8B%E0%A4%97+%E0%A4%95%E0%A4%B0%E0%A5%87%E0%A4%82%E0%A5%A4&isTemplate=true&header=%E0%A4%86%E0%A4%AA%E0%A4%95%E0%A5%87+%E0%A4%AA%E0%A4%BE%E0%A4%B8+%E0%A4%8F%E0%A4%95+%E0%A4%A8%E0%A4%AF%E0%A4%BE+%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF+%E0%A4%B9%E0%A5%88&buttonUrlParam={task_id}"
                    # url = f"https://media.smsgupshup.com/GatewayAPI/rest?userid=2000209909&password=z24gzBUA&send_to=8335076174&v=1.1&format=json&msg_type=TEXT&method=SENDMESSAGE&msg=%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF+%E0%A4%86%E0%A4%88%E0%A4%A1%E0%A5%80%3A+{task_id}%0A%E0%A4%86%E0%A4%AA%E0%A4%95%E0%A5%8B+%E0%A4%B6%E0%A5%8D%E0%A4%B0%E0%A5%80%E0%A4%AE%E0%A4%BE%E0%A4%A8+{creator_name}%28{creator_role}%29+%E0%A4%B8%E0%A5%87+%E0%A4%8F%E0%A4%95+%E0%A4%A8%E0%A4%AF%E0%A4%BE+%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF+%E0%A4%B8%E0%A5%8C%E0%A4%82%E0%A4%AA%E0%A4%BE+%E0%A4%97%E0%A4%AF%E0%A4%BE+%E0%A4%B9%E0%A5%88%E0%A5%A4%0A%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF+%E0%A4%B6%E0%A5%8D%E0%A4%B0%E0%A5%87%E0%A4%A3%E0%A5%80+{category}+%E0%A4%B9%E0%A5%88%E0%A5%A4%0A%E0%A4%89%E0%A4%AA%E0%A4%AD%E0%A5%8B%E0%A4%95%E0%A5%8D%E0%A4%A4%E0%A4%BE+%E0%A4%B5%E0%A4%BF%E0%A4%B5%E0%A4%B0%E0%A4%A3%3A+{customer_name}%28customercode%29%0A%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF+%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%BE%E0%A4%A5%E0%A4%AE%E0%A4%BF%E0%A4%95%E0%A4%A4%E0%A4%BE+Immediate+%E0%A4%B9%E0%A5%88%E0%A5%A4%0A%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF+%E0%A4%95%E0%A5%80+%E0%A4%B8%E0%A4%AE%E0%A4%AF+%E0%A4%B8%E0%A5%80%E0%A4%AE%E0%A4%BE+%E0%A4%B9%E0%A5%88+25%2F12%2F2023.%0A%E0%A4%85%E0%A4%A7%E0%A4%BF%E0%A4%95+%E0%A4%9C%E0%A4%BE%E0%A4%A8%E0%A4%A8%E0%A5%87+%E0%A4%95%E0%A5%87+%E0%A4%B2%E0%A4%BF%E0%A4%8F+%E0%A4%A8%E0%A5%80%E0%A4%9A%E0%A5%87+%E0%A4%A6%E0%A4%BF%E0%A4%8F+%E0%A4%97%E0%A4%8F+%E0%A4%B2%E0%A4%BF%E0%A4%82%E0%A4%95+%E0%A4%95%E0%A4%BE+%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%AF%E0%A5%8B%E0%A4%97+%E0%A4%95%E0%A4%B0%E0%A5%87%E0%A4%82%E0%A5%A4&isTemplate=true&header=%E0%A4%86%E0%A4%AA%E0%A4%95%E0%A5%87+%E0%A4%AA%E0%A4%BE%E0%A4%B8+%E0%A4%8F%E0%A4%95+%E0%A4%A8%E0%A4%AF%E0%A4%BE+%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF+%E0%A4%B9%E0%A5%88&buttonUrlParam=1233"
                    payload = {}
                    headers = {}
                    response = requests.request("GET", url, headers=headers, data=payload)
                    print(url)
                    print(response.text)
                    # except Exception as e:
                    #     print('exc', e)o

            elif request.POST.get('task6') == 'true': ##retention submission
                print("NOOO")
                # subtasks variables (initially False)
                # doc_submitted = False # => Documents submitted
                # bank_change = False # => Change in Bank Account
                # coapp_change = False # => Change in Co-Applicant
                # address_change = False # => Change in address


                #message creation for task description
                for item in loaded:
                    for key,value in item.items():

                        if key == '331206':
                            msg1 = 'Customer (Customer id: ' + str(customerid) + ') is interested in a new loan.'
                            msgx.append(msg1)
                        if key == '33120601':
                            loan_purpose = value['loan_purpose']
                            loan_amount = value['loan_amount']
                            # print(value['coapp_change'], "/////coap change", type(value['coapp_change']))
                            doc_submitted = value['doc_submitted']
                            coapp_change = value['coapp_change']
                            bank_change = value['bank_change']
                            address_change = value['address_change']

                            if value['loan_amount'] != '':
                                msg2 = 'Loan Amount asked for is ' + value['loan_amount'] + '|'
                                msgx.append(msg2)
                            if value['loan_purpose'] != '':
                                msg3 = value['loan_purpose'] + ' is the loan purpose|'
                                msgx.append(msg3)
                            if value['doc_submitted'] == 'true':
                                msg4 = 'Loan Documents have been submitted|'
                            else:
                                msg4 = 'Loan Documents have not been submitted|'
                            msgx.append(msg4)
                            if value['coapp_change'] == 'true':
                                msg5 = 'There is change in Co-Applicant|'
                            else:
                                msg5 = 'There is no change in Co-Applicant|'
                            msgx.append(msg5)
                            if value['bank_change'] == 'true':
                                msg6 = 'There is change in Bank Account|'
                            else:
                                msg6 = 'There is no change in Bank Account|'
                            msgx.append(msg6)
                            if value['address_change'] == 'true':
                                msg7 = 'There is change in Address|'
                            else:
                                msg7 = 'There is no change in Address|'
                            msgx.append(msg7)
                if len(msgx)>6:
                    msgx = (msgx[0] + msgx[1] + msgx[2] + msgx[3] + msgx[4] + msgx[5] + msgx[6])
                elif len(msgx)>5:
                    msgx = (msgx[0] + msgx[1] + msgx[2] + msgx[3] + msgx[4] + msgx[5])
                elif len(msgx)>4:
                    msgx = (msgx[0] + msgx[1] + msgx[2] + msgx[3] + msgx[4])
                elif len(msgx)>3:
                    msgx = (msgx[0] + msgx[1] + msgx[2] + msgx[3])
                elif len(msgx)>2:
                    msgx = (msgx[0] + msgx[1] + msgx[2])
                elif len(msgx)>1:
                    msgx = (msgx[0] + msgx[1])
                else:
                    msgx = msgx[0]
                #fetch calling number
                user_id = request.POST.get('user_id')
                print('user_id before df ', user_id )
                # user_df = pd.DataFrame(calling_number_list.objects.filter(UserID=int(user_id)).values())
                user_df = pd.DataFrame(Mst_UserTbl.objects.filter(UserID=int(user_id)).values())
                # user_number = user_df['CallingNumber']
                user_number = user_df['ContactNo']
                # user_number = 'Uncomment and Enter your number for testing flow '
                #prepare task data and save task instance
                task_name = "New Loan From Retention Customer Task"
                task_description = msgx
                usr_instance = Mst_UserTbl.objects.get(UserID = int(user_id))
                created_by = Mst_UserTbl.objects.get(UserID = int(user.UserID))
                deadline_date = datetime.now()
                priority = "1"
                taskup_obj = task_details()
                taskup_obj.task_name = task_name
                taskup_obj.task_description = task_description
                taskup_obj.created_by = created_by
                taskup_obj.assigned_to = usr_instance
                taskup_obj.category = "7"
                taskup_obj.deadline_date = deadline_date
                taskup_obj.t_info = disbursementid
                taskup_obj.T_Info_ID = 2
                taskup_obj.priority = priority
                taskup_obj.save()
                task_id = taskup_obj.task_id
                task_assigned_to = taskup_obj.assigned_to.UserID


                retention_response = Retention_Response()
                retention_response.Userid = user.UserID
                retention_response.DisbursementID = disbursementid
                retention_response.save()

                # if customerinfoid == None:
                #     customer_name = 'Customer'
                # else:
                #     customer_name = CustomerLevelSummarised.objects.get(CustomerInfoID = int(customerinfoid)).ApplicantName
                customer_name = request.POST.get('appname')
                #queueing whatsapp flows

                from datetime import time

                # if belongs_to_test_region: # regionchecker
                try:
                    queue_instance = WhatsAppQueue()
                    # issues_inst = CallingIssues()
                    queue_instance.user_id = user_id
                    queue_instance.flow_name = 'Retention Reminder'
                    queue_instance.status = 3
                    # print("puru promise datetime", issues_inst.promise_date , issues_inst.promise_time)
                    # p_datetime = datetime.strptime(str(issues_inst.promise_date) + ' ' + str(issues_inst.promise_time) + ':00', "%Y-%m-%d %H:%M:%S") #.strftime("%Y-%m-%d %H:%M:%S")
                    queue_instance.update_time =  taskup_obj.deadline_date - timedelta(minutes=15) #'promise datetime - timedelta(mins=15)'
                    # queue_instance.contact_number = '8335076174'
                    queue_instance.contact_number = str(user_number.iloc[0])
                    queue_instance.field_1 = customer_name
                    queue_instance.field_2 = customercode
                    queue_instance.field_3 = str(loan_amount)
                    queue_instance.field_4 = str(loan_purpose)
                    queue_instance.field_5 = 'Yes' if (doc_submitted == True) else 'No'
                    queue_instance.field_6 = 'Yes' if (coapp_change == True) else 'No'
                    queue_instance.field_7 = 'Yes' if (bank_change == True) else 'No'
                    queue_instance.field_8 = 'Yes' if (address_change == True) else 'No'
                    queue_instance.field_12 = None
                    queue_instance.issue_id = retention_response.id
                    queue_instance.task_id = task_id
                    queue_instance.field_13 = customer_contact_no
                    queue_instance.field_14 = customerinfoid
                    queue_instance.bc_id = business_caller_id
                    queue_instance.save()


                    ret_reminder_id = queue_instance.id
                    # print("time dekh le" , queue_instance.update_time)
                except Exception as e:
                    print("Retention reminder ", e)
                try:
                    queue_instance = WhatsAppQueue()
                    # issues_inst = CallingIssues()
                    queue_instance.user_id = user_id
                    queue_instance.flow_name = 'Retention Confirmation'
                    queue_instance.status = 3
                    # q_instance.update_time =  datetime.strptime(str(issues_inst.promise_date) + ' ' + str(issues_inst.promise_time) + ':00', "%Y-%m-%d %H:%M:%S") + timedelta(minutes=5) #'promise datetime + timedelta(mins = 5)'
                    queue_instance.contact_number = str(user_number.iloc[0])
                    queue_instance.field_1 = customer_name
                    queue_instance.field_2 = customercode
                    queue_instance.field_3 = str(loan_amount)
                    queue_instance.field_4 = str(loan_purpose)
                    queue_instance.field_5 = 'Yes' if (doc_submitted == True) else 'No'
                    queue_instance.field_6 = 'Yes' if (coapp_change == True) else 'No'
                    queue_instance.field_7 = 'Yes' if (bank_change == True) else 'No'
                    queue_instance.field_8 = 'Yes' if (address_change == True) else 'No'
                    queue_instance.field_11 = str(ret_reminder_id)
                    queue_instance.field_12 = None
                    queue_instance.issue_id = retention_response.id
                    queue_instance.task_id = task_id
                    # print("Info : ", msgx)
                    queue_instance.field_13 = customer_contact_no
                    queue_instance.field_14 = customerinfoid
                    queue_instance.bc_id = business_caller_id
                    queue_instance.save()

                    ret_conf_id = queue_instance.id

                except Exception as e:
                    print('Retention Confirmation',str(e))

                try:
                    queue_instance = WhatsAppQueue()
                    queue_instance.user_id = user_id
                    queue_instance.flow_name = 'Retention FollowUp'
                    queue_instance.update_time = datetime.now()
                    queue_instance.contact_number = str(user_number.iloc[0])
                    queue_instance.field_1 = customer_name
                    queue_instance.field_2 = customercode
                    queue_instance.field_3 = str(loan_amount)
                    queue_instance.field_4 = str(loan_purpose)
                    queue_instance.field_5 = 'Yes' if (doc_submitted == True) else 'No'
                    queue_instance.field_6 = 'Yes' if (coapp_change == True) else 'No'
                    queue_instance.field_7 = 'Yes' if (bank_change == True) else 'No'
                    queue_instance.field_8 = 'Yes' if (address_change == True) else 'No'
                    queue_instance.field_11 = str(ret_reminder_id) + ',' + str(ret_conf_id)
                    queue_instance.field_12 = None
                    queue_instance.issue_id = retention_response.id
                    queue_instance.task_id = task_id
                    # print("Info : ", msgx)
                    queue_instance.field_13 = customer_contact_no
                    queue_instance.field_14 = customerinfoid
                    queue_instance.bc_id = business_caller_id
                    queue_instance.save()
                except Exception as e:
                    print("Retention Followup ", e)

                try:
                    # user_df = pd.DataFrame(calling_number_list.objects.filter(UserID=int(user_id)).values())
                    # user_number = user_df['CallingNumber']
                    user_df = pd.DataFrame(Mst_UserTbl.objects.filter(UserID=int(user_id)).values())
                    user_number = user_df['ContactNo']
                    task_id = taskup_obj.task_id
                    creator_name = request.user.UserName
                    creator_role = request.session["RoleName"]
                    category = taskup_obj.category
                    customer_name = CustomerLevelSummarised.objects.get(CustomerInfoID = int(customerinfoid)).ApplicantName
                    customer_code = str(customerid)
                    if priority == "1":
                        priority = 'Immediate'
                    elif priority == "2":
                        priority = 'High'
                    elif priority == "3":
                        priority = 'Medium'
                    else:
                        priority = 'Low'
                    task_deadline = taskup_obj.deadline_date

                    url = "https://media.smsgupshup.com/GatewayAPI/rest"
                    headers = {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                    payload =f'userid={gupshup_uid}&password={gupshup_pass}&method=SendMessage&auth_scheme=plain&v=1.1&send_to={user_number}&msg=%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%86%E0%A4%88%E0%A4%A1%E0%A5%80%3A%20{task_id}%0A%E0%A4%86%E0%A4%AA%E0%A4%95%E0%A5%8B%20%E0%A4%B6%E0%A5%8D%E0%A4%B0%E0%A5%80%E0%A4%AE%E0%A4%BE%E0%A4%A8%20{creator_name}({creator_role})%20%E0%A4%B8%E0%A5%87%20%E0%A4%8F%E0%A4%95%20%E0%A4%A8%E0%A4%AF%E0%A4%BE%20%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%B8%E0%A5%8C%E0%A4%82%E0%A4%AA%E0%A4%BE%20%E0%A4%97%E0%A4%AF%E0%A4%BE%20%E0%A4%B9%E0%A5%88%E0%A5%A4%0A%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%B6%E0%A5%8D%E0%A4%B0%E0%A5%87%E0%A4%A3%E0%A5%80%20{category}%20%E0%A4%B9%E0%A5%88%E0%A5%A4%0A%E0%A4%89%E0%A4%AA%E0%A4%AD%E0%A5%8B%E0%A4%95%E0%A5%8D%E0%A4%A4%E0%A4%BE%20%E0%A4%B5%E0%A4%BF%E0%A4%B5%E0%A4%B0%E0%A4%A3%3A%20{customer_name}({customer_code})%0A%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%BE%E0%A4%A5%E0%A4%AE%E0%A4%BF%E0%A4%95%E0%A4%A4%E0%A4%BE%20{priority}%20%E0%A4%B9%E0%A5%88%E0%A5%A4%0A%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%95%E0%A5%80%20%E0%A4%B8%E0%A4%AE%E0%A4%AF%20%E0%A4%B8%E0%A5%80%E0%A4%AE%E0%A4%BE%20%E0%A4%B9%E0%A5%88%20{task_deadline}.%0A%E0%A4%85%E0%A4%A7%E0%A4%BF%E0%A4%95%20%E0%A4%9C%E0%A4%BE%E0%A4%A8%E0%A4%A8%E0%A5%87%20%E0%A4%95%E0%A5%87%20%E0%A4%B2%E0%A4%BF%E0%A4%8F%20%E0%A4%A8%E0%A5%80%E0%A4%9A%E0%A5%87%20%E0%A4%A6%E0%A4%BF%E0%A4%8F%20%E0%A4%97%E0%A4%8F%20%E0%A4%B2%E0%A4%BF%E0%A4%82%E0%A4%95%20%E0%A4%95%E0%A4%BE%20%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%AF%E0%A5%8B%E0%A4%97%20%E0%A4%95%E0%A4%B0%E0%A5%87%E0%A4%82%E0%A5%A4&msg_type=hsm&isHSM=true&isTemplate=true&data_encoding=Text&format=json&header=%E0%A4%86%E0%A4%AA%E0%A4%95%E0%A5%87%20%E0%A4%AA%E0%A4%BE%E0%A4%B8%20%E0%A4%8F%E0%A4%95%20%E0%A4%A8%E0%A4%AF%E0%A4%BE%20%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%B9%E0%A5%88&buttonUrlParam={task_id}'
                    response = requests.request("POST", url, headers=headers, data=payload)
                    print(response.text)
                except Exception as e:
                    print('exc', e)

            # Extraction of feedback points
            for item in loaded:
                # print("inside for loaded")
                for key,value in item.items():
                    # print(key,value)
                    if key == '331201' and value['status'] == True:
                        call_status = 'not_connected'   
                    if key == '331202' and value['status'] == True:
                        call_status = 'not_connected'          
                    if key == '33120501':
                        call_status = 'collection'
                        p2p_date = value['date']
                        p2p_amt = int(value['amount'])
                    if key == '33120601':
                        call_status = 'retention'
                        loan_amt = int(value['loan_amount'])
                        loan_purpose = value['loan_purpose']
                    if key == '331203':
                        if value['status'] == True:
                            call_status = 'wrong_number' 
                    if key == '33120302':
                        call_status = 'wrong_number'
                        alt_no = str(value['alternate_num'])
            # Datapoints submission in table
            feed_datapoint_obj = BusinessCallingFeedbackDataPoints()
            feed_datapoint_obj.UserID = business_caller_id
            # feed_datapoint_obj.RoleName = rolename
            feed_datapoint_obj.UserName = UserName
            # feed_datapoint_obj.Section = section
            feed_datapoint_obj.DisbursementID = disbursementid
            feed_datapoint_obj.CustomerInfoID = customerid
            # feed_datapoint_obj.ApplicantName = str(applicant_name)
            feed_datapoint_obj.Mobile_No = str(customer_contact_no)
            feed_datapoint_obj.Feedback_Status = str(call_status)
            feed_datapoint_obj.Alternate_No = alt_no
            feed_datapoint_obj.P2P_date = p2p_date
            feed_datapoint_obj.P2P_Amount = p2p_amt
            feed_datapoint_obj.Loan_Purpose = loan_purpose
            feed_datapoint_obj.Expected_Loan_Amount = loan_amt
            feed_datapoint_obj.Task_ID = task_id
            feed_datapoint_obj.save()
            print("Data Points Saved")

            if ('331201' in loaded[0].keys()) or ('331202' in loaded[0].keys()):
                business_call_obj = Retention_Calling_Data.objects.filter(DisbursementID = disbursementid).first()
                if (business_call_obj.calling_attempt is None) or (business_call_obj.calling_attempt < 3):
                    calling_count = business_call_obj.calling_attempt
                    if calling_count is None:
                        calling_count = 0
                    Retention_Calling_Data.objects.filter(DisbursementID = disbursementid).update(calling_attempt=calling_count + 1,feedback_response=call_feedback_json)
                    business_history_obj = Retention_Calling_History()
                    business_history_obj.DisbursementID = disbursementid
                    business_history_obj.feedback_response = call_feedback_json
                    business_history_obj.feedback_code = 1
                    business_history_obj.save()

                    return JsonResponse({'status':'success','check':'true'})
                else:
                    Retention_Calling_Data.objects.filter(DisbursementID = disbursementid).update(feedback_code = 1)
            else:
                Retention_Calling_Data.objects.filter(DisbursementID = disbursementid).update(feedback_code = 1,calling_attempt=1)
                print('calling attempt increased for ', disbursementid)
            Retention_Calling_Data.objects.filter(DisbursementID = disbursementid).update(feedback_response = call_feedback_json,feedback_code = 1)
            print('dsdsdsdsdsdsdsds')
            return JsonResponse({'status':'success','check':'false'})
        else:

            engine = get_db_engine()
            sql_query = f"""SET NOCOUNT ON;EXEC [Sonata_Connect].[dbo].[SP_UserHierarchy_Dynamic_07Jan23] @userid = 15179;SET NOCOUNT OFF"""
            df=pd.read_sql_query(sql_query,engine)
            df.drop_duplicates(subset='UserID',keep='first',inplace=True)
            div_df = df[(df['RoleId']==34)&(df['RoleName']=='DIVISION HEAD')][['U_BUID','UserID','UserName','buname']]
            div_df.rename(columns={'U_BUID':'Div_BUID','buname':'DivName','UserID':'Div_UserID','UserName':'Div_UserName'}, inplace=True)
            reg_df = df[(df['RoleId']==35)&(df['RoleName']=='REGION HEAD')][['U_BUID','UserID','UserName','buname','ReportingBUId']]
            reg_df.rename(columns={'U_BUID':'Region_BUID','ReportingBUId':'Region_ReportingBUId','buname':'RegionName','UserID':'Region_UserID','UserName':'Region_UserName'}, inplace=True)
            hub_df = df[(df['RoleId']==36)&(df['RoleName']=='HUB HEAD')][['U_BUID','UserID','UserName','buname','ReportingBUId']]
            hub_df.rename(columns={'U_BUID':'Hub_BUID','ReportingBUId':'Hub_ReportingBUId','buname':'HubName','UserID':'Hub_UserID','UserName':'Hub_UserName'}, inplace=True)
            bm_df = df[(df['RoleId']==13)&(df['RoleName']=='Branch Manager')][['U_BUID','buname','UserID','UserName','ReportingBUId']]
            bm_df.rename(columns={'U_BUID':'BM_BUID','ReportingBUId':'BM_ReportingBUId','buname':'BranchName','UserID':'BM_UserID','UserName':'BM_UserName'}, inplace=True)
            bro_df = df[(df['RoleId']==55)&(df['RoleName']=='BRO')][['U_BUID','UserID','UserName']]
            bro_df.rename(columns={'U_BUID':'BRO_BUID','UserID':'BRO_UserID','UserName':'BRO_UserName'}, inplace=True)
            M1 = pd.merge(bro_df,bm_df,left_on='BRO_BUID',right_on='BM_BUID',how='left').drop_duplicates(subset='BRO_UserID')
            M2 = pd.merge(M1,hub_df,left_on='BM_ReportingBUId',right_on='Hub_BUID',how='left').drop_duplicates(subset='BRO_UserID')
            M3 = pd.merge(M2,reg_df,left_on='Hub_ReportingBUId',right_on='Region_BUID',how='left').drop_duplicates(subset='BRO_UserID')
            dF = pd.merge(M3,div_df,left_on='Region_ReportingBUId',right_on='Div_BUID',how='left').drop_duplicates(subset='BRO_UserID')
            dF.fillna(0,inplace=True)
            dF[["BRO_UserID","BM_UserID","Hub_UserID","Region_UserID","Div_UserID"]] = dF[["BRO_UserID","BM_UserID","Hub_UserID","Region_UserID","Div_UserID"]].astype(int)
            dF = dF[dF['BRO_UserID'] == int(user_id)]
            print(dF,"$$$$$$")
            if dF.empty:
                send_list = []
            else:
                send_list = list(dF["BM_UserID"]) + list(dF["Hub_UserID"])
                if (send_list[0] == 0) or (send_list[1] == 0):
                    send_list = [i for i in send_list if i != 0]
                    send_list = send_list + list(dF["Region_UserID"])
                    if (send_list[0] == 0) or (send_list[1] == 0):
                        send_list = [i for i in send_list if i != 0]
                        send_list = send_list + list(dF["Div_UserID"])

            try:
                issues_inst = CallingIssues()
                issues_inst.category = 'Wrong Number Communicated'
                issues_inst.disbursement_id = int(disbursementid)
                issues_inst.customer_info_id = customerid
                issues_inst.customer_name = CustomerLevelSummarised.objects.get(CustomerInfoID = customerid).ApplicantName
                issues_inst.customer_number = CustomerLevelSummarised.objects.get(CustomerInfoID = customerid).mobile_no
                issues_inst.save()



            except Exception as e:
                print("calling issues fetch nahi ho raha ", e)
            task_id = None
            task_assigned_to = None
            alloc_date = request.POST.get('allocateddate')
            alloc_date = alloc_date.split(' ')[0]
            alloc_date = datetime.strptime(alloc_date, '%Y-%m-%d').date()
            print(alloc_date)

            call_initiated_id = int(request.POST.get('call_initiated_id'))
            call_primary_id = int(request.POST.get('call_primary_id'))

            for item in loaded:
                for key,value in item.items():
                    if key == '33120502':
                        if value['observation']:
                            print("inside value ...")
                            reason_df = pd.DataFrame(FeedbackObservations.objects.all().values())
                            reason_dict = dict(zip(reason_df['id'],reason_df['reason']))
                            reason = reason_dict[int(value['observation'])]
                            try:
                                taskid_list = []
                                for i in send_list:
                                    print("inside for loop ...")
                                    task_name = "Customer refused to pay back."
                                    task_description = f"Customer refused to pay back. Reason: {reason}"
                                    # deadline_date = datetime.now()
                                    usr_instance = Mst_UserTbl.objects.get(UserID = i)
                                    created_by = Mst_UserTbl.objects.get(UserID = int(user.UserID))
                                    deadline_date = datetime.now()
                                    priority = 1
                                    taskup_obj = task_details()
                                    taskup_obj.task_name = task_name
                                    taskup_obj.task_description = task_description
                                    taskup_obj.created_by = created_by
                                    taskup_obj.assigned_to = usr_instance
                                    taskup_obj.category = "14"
                                    taskup_obj.deadline_date = deadline_date
                                    taskup_obj.t_info = disbursementid
                                    taskup_obj.T_Info_ID = 2
                                    taskup_obj.priority = priority
                                    taskup_obj.save()
                                    print("task_object:",taskup_obj)
                                    task_id = taskup_obj.task_id
                                    task_assigned_to = taskup_obj.assigned_to.UserID
                                    taskid_list.append(task_id)
                                    print("tasklist: ",taskid_list)

                                    try:
                                        user_df = pd.DataFrame(calling_number_list.objects.filter(UserID = i).values())
                                        user_number = user_df['CallingNumber']
                                        task_id = taskup_obj.task_id
                                        creator_name = request.user.UserName
                                        creator_role = request.session["RoleName"]
                                        category = taskup_obj.category
                                        customer_name = CustomerLevelSummarised.objects.get(CustomerInfoID = int(customerinfoid)).ApplicantName
                                        customer_code = str(customerid)
                                        if priority == "1":
                                            priority = 'Immediate'
                                        elif priority == "2":
                                            priority = 'High'
                                        elif priority == "3":
                                            priority = 'Medium'
                                        else:
                                            priority = 'Low'
                                        task_deadline = taskup_obj.deadline_date

                                        url = "https://media.smsgupshup.com/GatewayAPI/rest"
                                        headers = {
                                            'Content-Type': 'application/x-www-form-urlencoded'
                                        }
                                        payload =f'userid={gupshup_uid}&password={gupshup_pass}&method=SendMessage&auth_scheme=plain&v=1.1&send_to={user_number}&msg=%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%86%E0%A4%88%E0%A4%A1%E0%A5%80%3A%20{task_id}%0A%E0%A4%86%E0%A4%AA%E0%A4%95%E0%A5%8B%20%E0%A4%B6%E0%A5%8D%E0%A4%B0%E0%A5%80%E0%A4%AE%E0%A4%BE%E0%A4%A8%20{creator_name}({creator_role})%20%E0%A4%B8%E0%A5%87%20%E0%A4%8F%E0%A4%95%20%E0%A4%A8%E0%A4%AF%E0%A4%BE%20%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%B8%E0%A5%8C%E0%A4%82%E0%A4%AA%E0%A4%BE%20%E0%A4%97%E0%A4%AF%E0%A4%BE%20%E0%A4%B9%E0%A5%88%E0%A5%A4%0A%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%B6%E0%A5%8D%E0%A4%B0%E0%A5%87%E0%A4%A3%E0%A5%80%20{category}%20%E0%A4%B9%E0%A5%88%E0%A5%A4%0A%E0%A4%89%E0%A4%AA%E0%A4%AD%E0%A5%8B%E0%A4%95%E0%A5%8D%E0%A4%A4%E0%A4%BE%20%E0%A4%B5%E0%A4%BF%E0%A4%B5%E0%A4%B0%E0%A4%A3%3A%20{customer_name}({customer_code})%0A%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%BE%E0%A4%A5%E0%A4%AE%E0%A4%BF%E0%A4%95%E0%A4%A4%E0%A4%BE%20{priority}%20%E0%A4%B9%E0%A5%88%E0%A5%A4%0A%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%95%E0%A5%80%20%E0%A4%B8%E0%A4%AE%E0%A4%AF%20%E0%A4%B8%E0%A5%80%E0%A4%AE%E0%A4%BE%20%E0%A4%B9%E0%A5%88%20{task_deadline}.%0A%E0%A4%85%E0%A4%A7%E0%A4%BF%E0%A4%95%20%E0%A4%9C%E0%A4%BE%E0%A4%A8%E0%A4%A8%E0%A5%87%20%E0%A4%95%E0%A5%87%20%E0%A4%B2%E0%A4%BF%E0%A4%8F%20%E0%A4%A8%E0%A5%80%E0%A4%9A%E0%A5%87%20%E0%A4%A6%E0%A4%BF%E0%A4%8F%20%E0%A4%97%E0%A4%8F%20%E0%A4%B2%E0%A4%BF%E0%A4%82%E0%A4%95%20%E0%A4%95%E0%A4%BE%20%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%AF%E0%A5%8B%E0%A4%97%20%E0%A4%95%E0%A4%B0%E0%A5%87%E0%A4%82%E0%A5%A4&msg_type=hsm&isHSM=true&isTemplate=true&data_encoding=Text&format=json&header=%E0%A4%86%E0%A4%AA%E0%A4%95%E0%A5%87%20%E0%A4%AA%E0%A4%BE%E0%A4%B8%20%E0%A4%8F%E0%A4%95%20%E0%A4%A8%E0%A4%AF%E0%A4%BE%20%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%B9%E0%A5%88&buttonUrlParam={task_id}'
                                        response = requests.request("POST", url, headers=headers, data=payload)
                                        print(response.text)
                                    except Exception as e:
                                        print('excin', e)
                            except Exception as e:
                                print('exc', e)

                            try:
                                issue_category = FeedbackObservations.objects.get(id=int(value['observation'])).reason
                                issues_inst = CallingIssues()
                                issues_inst.category = issue_category
                                issues_inst.disbursement_id = int(disbursementid)
                                issues_inst.customer_info_id = int(customerinfoid)
                                issues_inst.customer_name = CustomerLevelSummarised.objects.get(CustomerInfoID = int(customerinfoid)).ApplicantName
                                issues_inst.customer_number = CustomerLevelSummarised.objects.get(CustomerInfoID = int(customerinfoid)).mobile_no
                                issues_inst.task_id_ref1 = int(taskid_list[0])
                                issues_inst.task_id_ref2 = int(taskid_list[1])
                                issues_inst.save()
                            except:
                                pass



            applicant_name = request.POST.get('appname')
            applicant_number = request.POST.get('mobile')

            if request.POST.get('task3') == 'true':
                task_name = 'Wrong Number Communicated'
                user_id = request.POST.get('user_id')
                usr_instance = Mst_UserTbl.objects.get(UserID = int(request.POST.get('user_id')))
                created_by = Mst_UserTbl.objects.get(UserID = int(user.UserID))
                deadline_date = datetime.now()
                priority = '1'
                category = '10'
                applicant_name = request.POST.get('appname')
                applicant_number = request.POST.get('mobile')
                alternate_number = None

                msgx = []

                for item in loaded:
                        for key,value in item.items():
                            if key == '331203':
                                msg1 = 'Customer (Customer id: ' + str(customerid) + ') has communicated wrong number|'
                                msgx.append(msg1)
                            if key == '33120301':
                                if value['feedback_3'] != '':
                                    msg2 = 'Feedback recieved: ' + value['feedback_3'] + '|'
                                    msgx.append(msg2)
                            if key == '33120302':
                                alternate_number = value['alternate_num']
                                msg3 = 'Alternate number recieved ' + value['alternate_num'] + '|'
                                msgx.append(msg3)
                if len(msgx)>2:
                    msgx = (msgx[0] + msgx[1] + msgx[2])
                elif len(msgx)>1:
                    msgx = (msgx[0] + msgx[1])
                else:
                    msgx = msgx[0]

                msgx += f'Customer name {applicant_name} contact number {applicant_number}' + '|'

                deadline_dt = None
                ## create a task for wrong number


                wn_task_obj = task_details()
                wn_task_obj.task_name = task_name
                wn_task_obj.task_description = msgx
                wn_task_obj.created_by = created_by
                wn_task_obj.assigned_to = usr_instance
                wn_task_obj.priority = priority
                wn_task_obj.t_info = disbursementid
                wn_task_obj.category = category  ## category?? check if correct
                wn_task_obj.deadline_date = deadline_date
                try:
                    wn_task_obj.feedback = feedback_recvd
                except:
                    wn_task_obj.feedback = ''

                wn_task_obj.save() #temporarily commented
                #task details for later usage
                task_id = wn_task_obj.task_id

                try:
                    issues_inst = CallingIssues()
                    issues_inst.category = 'Wrong Number Communicated'
                    issues_inst.disbursement_id = int(disbursementid)
                    issues_inst.customer_info_id = customerid
                    issues_inst.customer_name = CustomerLevelSummarised.objects.get(CustomerInfoID = customerid).ApplicantName
                    issues_inst.customer_number = CustomerLevelSummarised.objects.get(CustomerInfoID = customerid).mobile_no
                    issues_inst.save()
                except Exception as e:
                    print("calling issues inst not able to create : ", e)

                # Creating a Queue for wrong number 
                # whatsapp queue logic
                # user_number = 'Uncomment and Enter your number for testing flow '
                user_number = applicant_number
                # if belongs_to_test_region: # regionchecker
                try:

                    try :
                        queue_instance = WhatsAppQueue()
                        queue_instance.user_id = user_id
                        queue_instance.flow_name = 'WNV_alert'
                        queue_instance.status = 3
                        queue_instance.update_time = datetime.now()
                        queue_instance.contact_number = user_number #str(applicant_number)
                        queue_instance.field_1 = broname
                        queue_instance.field_2 = CustomerLevelSummarised.objects.get(CustomerInfoID = customerid).ApplicantName
                        queue_instance.field_3 = customercode
                        queue_instance.field_4 = alternate_number
                        queue_instance.field_5 = wn_task_obj.deadline_date.date()
                        queue_instance.field_6 = wn_task_obj.deadline_date.strftime('%H:%M')
                        queue_instance.issue_id = issues_inst.id
                        queue_instance.task_id = task_id
                        queue_instance.field_13 = customer_contact_no
                        queue_instance.field_14 = customerinfoid
                        queue_instance.bc_id = business_caller_id
                        queue_instance.save()

                        visit_alert_id = queue_instance.id
                    except Exception as e:
                        print("WNV_alert", e)

                    try :
                        queue_instance = WhatsAppQueue()
                        queue_instance.user_id = user_id
                        queue_instance.flow_name = 'WNV_flow'
                        queue_instance.status = 3
                        queue_instance.update_time = datetime.now()
                        queue_instance.contact_number = user_number #str(applicant_number)
                        queue_instance.field_1 = broname
                        queue_instance.field_2 = CustomerLevelSummarised.objects.get(CustomerInfoID = customerid).ApplicantName
                        queue_instance.field_3 = customercode
                        queue_instance.field_4 = alternate_number
                        queue_instance.field_5 = wn_task_obj.deadline_date.date()
                        queue_instance.field_6 = wn_task_obj.deadline_date.strftime('%H:%M')
                        queue_instance.field_11 = visit_alert_id
                        queue_instance.issue_id = issues_inst.id
                        queue_instance.task_id = task_id
                        queue_instance.field_13 = customer_contact_no
                        queue_instance.field_14 = customerinfoid
                        queue_instance.bc_id = business_caller_id
                        queue_instance.save()

                        visit_flow_id = queue_instance.id
                    except Exception as e:
                        print("WNV_flow", e)

                    if not alternate_number :
                        try :
                            queue_instance = WhatsAppQueue()
                            queue_instance.user_id = user_id
                            queue_instance.flow_name = 'WNANP_flow'
                            queue_instance.update_time = datetime.now()
                            queue_instance.contact_number = user_number #str(applicant_number)
                            queue_instance.field_1 = broname
                            queue_instance.field_2 = CustomerLevelSummarised.objects.get(CustomerInfoID = customerid).ApplicantName
                            queue_instance.field_3 = customercode
                            queue_instance.field_4 = alternate_number
                            queue_instance.field_5 = wn_task_obj.deadline_date.date()
                            queue_instance.field_6 = wn_task_obj.deadline_date.strftime('%H:%M')
                            queue_instance.field_7 = visit_alert_id
                            queue_instance.field_8 = visit_flow_id  
                            queue_instance.issue_id = issues_inst.id
                            queue_instance.task_id = task_id
                            queue_instance.field_13 = customer_contact_no
                            queue_instance.field_14 = customerinfoid
                            queue_instance.bc_id = business_caller_id
                            queue_instance.save()

                        except Exception as e:
                            print('WNANP_flow', e)




                    else : ## ALternate Number Present

                        try :
                            queue_instance = WhatsAppQueue()
                            queue_instance.user_id = user_id
                            queue_instance.flow_name = 'WNAP_alert'
                            queue_instance.update_time = datetime.now()
                            queue_instance.contact_number = user_number #str(applicant_number)
                            queue_instance.field_1 = broname
                            queue_instance.field_2 = CustomerLevelSummarised.objects.get(CustomerInfoID = customerid).ApplicantName
                            queue_instance.field_3 = customercode
                            queue_instance.field_4 = alternate_number
                            queue_instance.field_5 = wn_task_obj.deadline_date.date()
                            queue_instance.field_6 = wn_task_obj.deadline_date.strftime('%H:%M')
                            queue_instance.field_7 = visit_alert_id
                            queue_instance.field_8 = visit_flow_id
                            queue_instance.issue_id = issues_inst.id
                            queue_instance.task_id = task_id
                            queue_instance.field_13 = customer_contact_no
                            queue_instance.field_14 = customerinfoid
                            queue_instance.bc_id = business_caller_id
                            queue_instance.save()

                            visit_instance_alert = queue_instance.id
                        except Exception as e:
                            print("WNAP_alert", e)
                        try :
                            from datetime import timedelta as td
                            queue_instance = WhatsAppQueue()
                            queue_instance.user_id = user_id
                            queue_instance.flow_name = 'WNAP_flow'
                            queue_instance.update_time = datetime.now() + td(hours=1)
                            queue_instance.contact_number = user_number #str(applicant_number)
                            queue_instance.field_1 = broname
                            queue_instance.field_2 = CustomerLevelSummarised.objects.get(CustomerInfoID = customerid).ApplicantName
                            queue_instance.field_3 = customercode
                            queue_instance.field_4 = alternate_number
                            queue_instance.field_5 = wn_task_obj.deadline_date.date()
                            queue_instance.field_6 = wn_task_obj.deadline_date.strftime('%H:%M')
                            queue_instance.field_7 = visit_alert_id
                            queue_instance.field_8 = visit_flow_id
                            queue_instance.issue_id = issues_inst.id
                            queue_instance.task_id = task_id
                            queue_instance.field_13 = customer_contact_no
                            queue_instance.field_14 = customerinfoid
                            queue_instance.bc_id = business_caller_id
                            queue_instance.save() 
                        except Exception as e:
                            print("WNAP_flow", e)





                except Exception as e:
                    print("Wrong Number Communicated : ", e)


            if request.POST.get('task5') == 'true':
                # try:
                #     issues_inst = CallingIssues()
                #     issues_inst.category = 'Promise to Pay'
                #     issues_inst.disbursement_id = int(disbursementid)
                #     issues_inst.customer_info_id = int(customerinfoid)
                #     issues_inst.customer_name = CustomerLevelSummarised.objects.get(CustomerInfoID = int(customerinfoid)).ApplicantName
                #     issues_inst.customer_number = CustomerLevelSummarised.objects.get(CustomerInfoID = int(customerinfoid)).mobile_no
                #     issues_inst.save()
                # except:
                #     pass

                msg = []

                for item in loaded:
                    for key,value in item.items():
                        # print(';;;;;', key)
                        if key == '33120501':
                            # try:
                            #     issues_inst = CallingIssues()
                            #     issues_inst.category = 'Promise to Pay'
                            #     issues_inst.disbursement_id = int(disbursementid)
                            #     issues_inst.customer_info_id = int(customerinfoid)
                            #     issues_inst.customer_name = CustomerLevelSummarised.objects.get(CustomerInfoID = int(customerinfoid)).ApplicantName
                            #     issues_inst.customer_number = CustomerLevelSummarised.objects.get(CustomerInfoID = int(customerinfoid)).mobile_no
                            #     issues_inst.promise_date = datetime.strptime(value['date'], '%Y-%m-%d').date()
                            #     issues_inst.promise_time = value['time']
                            #     issues_inst.promise_amount = value['amount']
                            #     issues_inst.payment_method = value['mode_of_payment']
                            #     if key == '3312050102':
                            #         issues_inst.payment_collection_location = value['paying_place']
                            #     print('/////////////////////////////////////////////////////')
                            #     issues_inst.save()
                            # except Exception as e:
                            #     print('wow//////////////////////////////', e)
                            deadline_dt = value['date']
                            msg1 = 'Customer (Customer id: ' + str(customerid) + ') will pay an amount of ' +  value['amount'] + ' on ' +  value['date'] + ' ' + value['time'] + ' by ' + value['mode_of_payment'] + '|'
                            msg.append(msg1)
                        if key == '3312050102':
                            msg2 = '.' + value['paying_place'] +'|'
                            print(msg2)
                            msg.append(msg2)


                if len(msg)>1:
                    msg = (msg[0] + msg[1])
                else:
                    msg = msg[0]


                msg += f'Customer name {applicant_name} contact number {applicant_number}|'



            if request.POST.get('task12') == 'true':
                msgg = []

                for item in loaded:
                        for key,value in item.items():
                            if key == '33121201':
                                msg3 = 'Appointment date is ' + value['proposed_date'] +'|'
                                msgg.append(msg3)


                if len(msgg)>0:
                    msgg = f'Collect bank statement from customer, name: {applicant_name} contact number: {applicant_number}' + msgg[0] + '|'
                else:
                    msgg = ''

                print('.........................9999999999999999',msgg)


            for item in loaded:
                for key,value in item.items():
                    if key == '33120502':
                        if value['observation']:
                            print('llllllll',value['observation'], type(value['observation']))

            user_id = request.POST.get('user_id')
            print('user_id',user_id)

            task_id = None
            task_assigned_to = None

            if request.POST.get('task5') == 'true':
                #task creation
                task_name = "Payment Collection Task"
                task_description = msg
                usr_instance = Mst_UserTbl.objects.get(UserID = int(user_id))
                created_by = Mst_UserTbl.objects.get(UserID = int(user.UserID))
                try:
                    deadline_date = deadline_dt
                except Exception as e:
                    print(e)
                    deadline_date = datetime.now()
                priority = "1"
                taskup_obj = task_details()
                taskup_obj.task_name = task_name
                taskup_obj.task_description = task_description
                taskup_obj.created_by = created_by
                taskup_obj.assigned_to = usr_instance
                taskup_obj.category = "3"
                taskup_obj.deadline_date = deadline_date
                taskup_obj.t_info = disbursementid
                taskup_obj.T_Info_ID = 2
                taskup_obj.priority = priority
                taskup_obj.save()
                print('task created')

                #task details for later usage
                task_id = taskup_obj.task_id
                task_assigned_to = taskup_obj.assigned_to.UserID

                #json extraction, calling issues promise to pay entry
                issues_inst = CallingIssues()
                for item in loaded:
                    print('this is item', item)
                    issues_inst.category = 'Promise to Pay'
                    try:
                        issues_inst.disbursement_id = int(disbursementid)
                        issues_inst.customer_info_id = int(customerinfoid)
                        issues_inst.customer_name = CustomerLevelSummarised.objects.get(CustomerInfoID = int(customerinfoid)).ApplicantName
                        issues_inst.customer_number = CustomerLevelSummarised.objects.get(CustomerInfoID = int(customerinfoid)).mobile_no
                    except:
                        pass
                    issues_inst.bro_taskid = int(task_id)
                    for key,value in item.items():
                        if key == '33120501':
                            try:
                                issues_inst.promise_date = datetime.strptime(value['date'], '%Y-%m-%d').date()
                                issues_inst.promise_time = value['time']
                                issues_inst.promise_amount = value['amount']
                                issues_inst.payment_method = value['mode_of_payment']
                            except Exception as e:
                                print('wow//////////////////////////////', e)
                        if key == '3312050102':
                            try:
                                issues_inst.payment_collection_location = value['paying_place']
                            except Exception as e:
                                print('ooo////',e)
                issues_inst.save() 
                print('calling issues saved')
                print("puru promise datetime", issues_inst.promise_date , issues_inst.promise_time)
                # whatsapp queue logic 

                for item in loaded:
                        for key,value in item.items():
                            if key == '33120501':
                                try:
                                    promise_time = value['time']
                                    promise_amount = value['amount']
                                except Exception as e:
                                    print('api json 1', e)
                            if key == '3312050102':
                                try:
                                    payment_collection_location = value['paying_place']
                                except Exception as e:
                                    print('api json 2',e)
                try:
                    user_df = pd.DataFrame(calling_number_list.objects.filter(UserID=int(user_id)).values())
                    user_number = user_df['CallingNumber']
                except:
                    user_number = '8888888888'
                # user_number = 'Uncomment and Enter your number for testing flow '

                # if belongs_to_test_region: # regionchecker
                try:

                    queue_instance = WhatsAppQueue()
                    # issues_inst = CallingIssues()
                    queue_instance.user_id = user_id
                    queue_instance.flow_name = 'Collection Reminder'
                    queue_instance.status = 3
                    print("puru promise datetime", issues_inst.promise_date , issues_inst.promise_time)
                    p_datetime = datetime.strptime(str(issues_inst.promise_date) + ' ' + str(issues_inst.promise_time) + ':00', "%Y-%m-%d %H:%M:%S") #.strftime("%Y-%m-%d %H:%M:%S")
                    queue_instance.update_time =  p_datetime - timedelta(minutes=15) #'promise datetime - timedelta(mins=15)'
                    # queue_instance.contact_number = '8335076174'
                    queue_instance.contact_number = str(user_number.iloc[0])
                    queue_instance.field_1 = task_id
                    queue_instance.field_2 = request.user.UserName
                    queue_instance.field_3 = request.session["RoleName"]
                    queue_instance.field_4 = CustomerLevelSummarised.objects.filter(CustomerCode = customercode).first().ApplicantName
                    queue_instance.field_5 = customercode
                    queue_instance.field_6 = priority
                    queue_instance.field_7 = taskup_obj.deadline_date
                    queue_instance.field_8 = promise_time
                    queue_instance.field_12 = None
                    queue_instance.field_9 = promise_amount
                    queue_instance.field_10 = payment_collection_location
                    queue_instance.issue_id = issues_inst.id
                    queue_instance.task_id = task_id
                    queue_instance.field_13 = customer_contact_no
                    queue_instance.field_14 = customerinfoid
                    queue_instance.bc_id = business_caller_id
                    queue_instance.save()

                    collectn_reminder_id = queue_instance.id

                    print("Updated Time : " , queue_instance.update_time)
                except Exception as e:
                    print("Colection rEminder ", e)

                try:
                    q_instance = WhatsAppQueue()
                    # issues_inst = CallingIssues()
                    q_instance.user_id = user_id
                    q_instance.flow_name = 'Collection Confirmation'
                    q_instance.status = 3
                    q_instance.update_time =  datetime.strptime(str(issues_inst.promise_date) + ' ' + str(issues_inst.promise_time) + ':00', "%Y-%m-%d %H:%M:%S") + timedelta(minutes=5) #'promise datetime + timedelta(mins = 5)'
                    q_instance.contact_number = str(user_number.iloc[0])
                    q_instance.field_1 = task_id
                    q_instance.field_2 = request.user.UserName
                    q_instance.field_3 = request.session["RoleName"]
                    q_instance.field_4 = CustomerLevelSummarised.objects.filter(CustomerCode = customercode).first().ApplicantName
                    q_instance.field_5 = customercode
                    q_instance.field_6 = priority
                    q_instance.field_11 = str(collectn_reminder_id)
                    q_instance.field_12 = None
                    q_instance.field_7 = taskup_obj.deadline_date
                    q_instance.field_8 = promise_time
                    q_instance.field_9 = promise_amount
                    q_instance.field_10 = payment_collection_location
                    q_instance.issue_id = issues_inst.id
                    q_instance.task_id = task_id
                    q_instance.field_13 = customer_contact_no
                    q_instance.field_14 = customerinfoid
                    q_instance.bc_id = business_caller_id
                    q_instance.save()

                    collectn_conf_id = q_instance.id
                except Exception as e:
                    print('Collection Confirmation',str(e))

                try:
                    queue_instance = WhatsAppQueue()
                    # issues_inst = CallingIssues()
                    queue_instance.user_id = user_id
                    queue_instance.flow_name = 'Collection FollowUp'
                    queue_instance.update_time = datetime.now()
                    queue_instance.contact_number = str(user_number.iloc[0])
                    queue_instance.field_1 = task_id
                    queue_instance.field_2 = request.user.UserName
                    queue_instance.field_3 = request.session["RoleName"]
                    queue_instance.field_4 = CustomerLevelSummarised.objects.filter(CustomerCode = customercode).first().ApplicantName
                    queue_instance.field_5 = customercode
                    queue_instance.field_6 = priority
                    queue_instance.field_7 = taskup_obj.deadline_date
                    queue_instance.field_8 = promise_time
                    queue_instance.field_12 = None
                    queue_instance.field_9 = promise_amount
                    queue_instance.field_10 = payment_collection_location
                    queue_instance.field_11 = str(collectn_reminder_id) + ',' + str(collectn_conf_id)
                    queue_instance.issue_id = issues_inst.id
                    queue_instance.task_id = task_id
                    queue_instance.field_13 = customer_contact_no
                    queue_instance.field_14 = customerinfoid
                    queue_instance.bc_id = business_caller_id
                    queue_instance.save()
                except Exception as e:
                    print("Colection Followup ", e)

            else:
                print('no task to create for payment collection')


            if request.POST.get('task12') == 'true':
                # BRO
                task_name = "Bank Statement Collection Task"
                task_description = msgg
                deadline_date = datetime.now()
                usr_instance = Mst_UserTbl.objects.get(UserID = int(user_id))
                created_by = Mst_UserTbl.objects.get(UserID = int(user.UserID))
                deadline_date = datetime.now()
                priority = "1"
                taskup_obj = task_details()
                taskup_obj.task_name = task_name
                taskup_obj.task_description = task_description
                taskup_obj.created_by = created_by
                taskup_obj.assigned_to = usr_instance
                taskup_obj.category = "3"
                taskup_obj.deadline_date = deadline_date
                taskup_obj.priority = priority
                taskup_obj.save()

                user_df = pd.DataFrame(calling_number_list.objects.filter(UserID=int(user_id)).values())
                user_number = user_df['CallingNumber']
                task_id = taskup_obj.task_id
                creator_name = request.user.UserName
                creator_role = request.session["RoleName"]
                category = taskup_obj.category
                customer_name = CustomerLevelSummarised.objects.get(CustomerInfoID = int(customerid)).ApplicantName
                customer_code = str(customerid)
                if priority == "1":
                    priority = 'Immediate'
                elif priority == "2":
                    priority = 'High'
                elif priority == "3":
                    priority = 'Medium'
                else:
                    priority = 'Low'
                task_deadline = taskup_obj.deadline_date

                url = "https://media.smsgupshup.com/GatewayAPI/rest"
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                payload =f'userid={gupshup_uid}&password={gupshup_pass}&method=SendMessage&auth_scheme=plain&v=1.1&send_to={user_number}&msg=%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%86%E0%A4%88%E0%A4%A1%E0%A5%80%3A%20{task_id}%0A%E0%A4%86%E0%A4%AA%E0%A4%95%E0%A5%8B%20%E0%A4%B6%E0%A5%8D%E0%A4%B0%E0%A5%80%E0%A4%AE%E0%A4%BE%E0%A4%A8%20{creator_name}({creator_role})%20%E0%A4%B8%E0%A5%87%20%E0%A4%8F%E0%A4%95%20%E0%A4%A8%E0%A4%AF%E0%A4%BE%20%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%B8%E0%A5%8C%E0%A4%82%E0%A4%AA%E0%A4%BE%20%E0%A4%97%E0%A4%AF%E0%A4%BE%20%E0%A4%B9%E0%A5%88%E0%A5%A4%0A%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%B6%E0%A5%8D%E0%A4%B0%E0%A5%87%E0%A4%A3%E0%A5%80%20{category}%20%E0%A4%B9%E0%A5%88%E0%A5%A4%0A%E0%A4%89%E0%A4%AA%E0%A4%AD%E0%A5%8B%E0%A4%95%E0%A5%8D%E0%A4%A4%E0%A4%BE%20%E0%A4%B5%E0%A4%BF%E0%A4%B5%E0%A4%B0%E0%A4%A3%3A%20{customer_name}({customer_code})%0A%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%BE%E0%A4%A5%E0%A4%AE%E0%A4%BF%E0%A4%95%E0%A4%A4%E0%A4%BE%20{priority}%20%E0%A4%B9%E0%A5%88%E0%A5%A4%0A%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%95%E0%A5%80%20%E0%A4%B8%E0%A4%AE%E0%A4%AF%20%E0%A4%B8%E0%A5%80%E0%A4%AE%E0%A4%BE%20%E0%A4%B9%E0%A5%88%20{task_deadline}.%0A%E0%A4%85%E0%A4%A7%E0%A4%BF%E0%A4%95%20%E0%A4%9C%E0%A4%BE%E0%A4%A8%E0%A4%A8%E0%A5%87%20%E0%A4%95%E0%A5%87%20%E0%A4%B2%E0%A4%BF%E0%A4%8F%20%E0%A4%A8%E0%A5%80%E0%A4%9A%E0%A5%87%20%E0%A4%A6%E0%A4%BF%E0%A4%8F%20%E0%A4%97%E0%A4%8F%20%E0%A4%B2%E0%A4%BF%E0%A4%82%E0%A4%95%20%E0%A4%95%E0%A4%BE%20%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%AF%E0%A5%8B%E0%A4%97%20%E0%A4%95%E0%A4%B0%E0%A5%87%E0%A4%82%E0%A5%A4&msg_type=hsm&isHSM=true&isTemplate=true&data_encoding=Text&format=json&header=%E0%A4%86%E0%A4%AA%E0%A4%95%E0%A5%87%20%E0%A4%AA%E0%A4%BE%E0%A4%B8%20%E0%A4%8F%E0%A4%95%20%E0%A4%A8%E0%A4%AF%E0%A4%BE%20%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%B9%E0%A5%88&buttonUrlParam={task_id}'
                response = requests.request("POST", url, headers=headers, data=payload)
                print(response.text)

            else:
                print('no task to create for bank statement collection')


            if request.POST.get('task3') == 'true':
                # BRO
                task_name = "Wrong Number Communicated Task"
                task_description = msgx
                deadline_date = datetime.now()
                usr_instance = Mst_UserTbl.objects.get(UserID = int(user_id))
                created_by = Mst_UserTbl.objects.get(UserID = int(user.UserID))
                deadline_date = datetime.now()
                priority = "1"
                taskup_obj = task_details()
                taskup_obj.task_name = task_name
                taskup_obj.task_description = task_description
                taskup_obj.created_by = created_by
                taskup_obj.assigned_to = usr_instance
                taskup_obj.category = "10"
                taskup_obj.deadline_date = deadline_date
                taskup_obj.t_info = disbursementid
                # taskup_obj.T_Info_ID = 2
                taskup_obj.priority = priority
                taskup_obj.save()

                task_id = taskup_obj.task_id
                task_assigned_to=taskup_obj.assigned_to.UserID

                try:
                    # print(taskup_obj.task_id,"$$$$$$$")
                    issues_inst = CallingIssues()
                    issues_inst.category = 'Wrong Number Communicated'
                    issues_inst.disbursement_id = int(disbursementid)
                    issues_inst.customer_info_id = int(customerinfoid)
                    issues_inst.customer_name = CustomerLevelSummarised.objects.get(CustomerInfoID = int(customerinfoid)).ApplicantName
                    issues_inst.customer_number = CustomerLevelSummarised.objects.get(CustomerInfoID = int(customerinfoid)).mobile_no
                    issues_inst.bro_taskid = int(task_id)
                    issues_inst.save()
                except:
                    pass


                try:
                    user_df = pd.DataFrame(calling_number_list.objects.filter(UserID=int(user_id)).values())
                    user_number = user_df['CallingNumber']
                    task_id = taskup_obj.task_id
                    creator_name = request.user.UserName
                    creator_role = request.session["RoleName"]
                    category = taskup_obj.category
                    customer_name = CustomerLevelSummarised.objects.get(CustomerInfoID = int(customerinfoid)).ApplicantName
                    customer_code = str(customerid)
                    if priority == "1":
                        priority = 'Immediate'
                    elif priority == "2":
                        priority = 'High'
                    elif priority == "3":
                        priority = 'Medium'
                    else:
                        priority = 'Low'
                    task_deadline = taskup_obj.deadline_date

                    # url = "https://media.smsgupshup.com/GatewayAPI/rest"
                    # headers = {
                    #     'Content-Type': 'application/x-www-form-urlencoded'
                    # }
                    # payload =f'userid={gupshup_uid}&password={gupshup_pass}&method=SendMessage&auth_scheme=plain&v=1.1&send_to={user_number}&msg=%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%86%E0%A4%88%E0%A4%A1%E0%A5%80%3A%20{task_id}%0A%E0%A4%86%E0%A4%AA%E0%A4%95%E0%A5%8B%20%E0%A4%B6%E0%A5%8D%E0%A4%B0%E0%A5%80%E0%A4%AE%E0%A4%BE%E0%A4%A8%20{creator_name}({creator_role})%20%E0%A4%B8%E0%A5%87%20%E0%A4%8F%E0%A4%95%20%E0%A4%A8%E0%A4%AF%E0%A4%BE%20%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%B8%E0%A5%8C%E0%A4%82%E0%A4%AA%E0%A4%BE%20%E0%A4%97%E0%A4%AF%E0%A4%BE%20%E0%A4%B9%E0%A5%88%E0%A5%A4%0A%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%B6%E0%A5%8D%E0%A4%B0%E0%A5%87%E0%A4%A3%E0%A5%80%20{category}%20%E0%A4%B9%E0%A5%88%E0%A5%A4%0A%E0%A4%89%E0%A4%AA%E0%A4%AD%E0%A5%8B%E0%A4%95%E0%A5%8D%E0%A4%A4%E0%A4%BE%20%E0%A4%B5%E0%A4%BF%E0%A4%B5%E0%A4%B0%E0%A4%A3%3A%20{customer_name}({customer_code})%0A%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%BE%E0%A4%A5%E0%A4%AE%E0%A4%BF%E0%A4%95%E0%A4%A4%E0%A4%BE%20{priority}%20%E0%A4%B9%E0%A5%88%E0%A5%A4%0A%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%95%E0%A5%80%20%E0%A4%B8%E0%A4%AE%E0%A4%AF%20%E0%A4%B8%E0%A5%80%E0%A4%AE%E0%A4%BE%20%E0%A4%B9%E0%A5%88%20{task_deadline}.%0A%E0%A4%85%E0%A4%A7%E0%A4%BF%E0%A4%95%20%E0%A4%9C%E0%A4%BE%E0%A4%A8%E0%A4%A8%E0%A5%87%20%E0%A4%95%E0%A5%87%20%E0%A4%B2%E0%A4%BF%E0%A4%8F%20%E0%A4%A8%E0%A5%80%E0%A4%9A%E0%A5%87%20%E0%A4%A6%E0%A4%BF%E0%A4%8F%20%E0%A4%97%E0%A4%8F%20%E0%A4%B2%E0%A4%BF%E0%A4%82%E0%A4%95%20%E0%A4%95%E0%A4%BE%20%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%AF%E0%A5%8B%E0%A4%97%20%E0%A4%95%E0%A4%B0%E0%A5%87%E0%A4%82%E0%A5%A4&msg_type=hsm&isHSM=true&isTemplate=true&data_encoding=Text&format=json&header=%E0%A4%86%E0%A4%AA%E0%A4%95%E0%A5%87%20%E0%A4%AA%E0%A4%BE%E0%A4%B8%20%E0%A4%8F%E0%A4%95%20%E0%A4%A8%E0%A4%AF%E0%A4%BE%20%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%B9%E0%A5%88&buttonUrlParam={task_id}'
                    # response = requests.request("POST", url, headers=headers, data=payload)
                    # print(response.text)
                    if user.UserID == 29968:
                        for item in loaded:
                            for key,value in item.items():
                                if key == '33120501':
                                    url = f"https://media.smsgupshup.com/GatewayAPI/rest?userid={gupshup_uid}&password={gupshup_pass}&send_to={user_number}&v=1.1&format=json&msg_type=TEXT&method=SENDMESSAGE&msg=%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF+%E0%A4%86%E0%A4%88%E0%A4%A1%E0%A5%80%3A+{task_id}%0A%E0%A4%86%E0%A4%AA%E0%A4%95%E0%A5%8B+%E0%A4%B6%E0%A5%8D%E0%A4%B0%E0%A5%80%E0%A4%AE%E0%A4%BE%E0%A4%A8+{creator_name}%28{creator_role}%29+%E0%A4%B8%E0%A5%87+%E0%A4%8F%E0%A4%95+%E0%A4%A8%E0%A4%AF%E0%A4%BE+%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF+%E0%A4%B8%E0%A5%8C%E0%A4%82%E0%A4%AA%E0%A4%BE+%E0%A4%97%E0%A4%AF%E0%A4%BE+%E0%A4%B9%E0%A5%88%E0%A5%A4%0A%E0%A4%89%E0%A4%AA%E0%A4%AD%E0%A5%8B%E0%A4%95%E0%A5%8D%E0%A4%A4%E0%A4%BE+%E0%A4%B5%E0%A4%BF%E0%A4%B5%E0%A4%B0%E0%A4%A3%3A+{customer_name}%28{customer_code}%29%0A%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF+%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%BE%E0%A4%A5%E0%A4%AE%E0%A4%BF%E0%A4%95%E0%A4%A4%E0%A4%BE+{priority}+%E0%A4%B9%E0%A5%88%E0%A5%A4%0A%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF+%E0%A4%95%E0%A5%80+%E0%A4%B8%E0%A4%AE%E0%A4%AF+%E0%A4%B8%E0%A5%80%E0%A4%AE%E0%A4%BE+%E0%A4%B9%E0%A5%88+{deadline_date}%2C{value['time']}%0A%E0%A4%B0%E0%A4%BE%E0%A4%B6%E0%A4%BF+%E0%A4%8F%E0%A4%95%E0%A4%A4%E0%A5%8D%E0%A4%B0+%E0%A4%95%E0%A5%80+%E0%A4%9C%E0%A4%BE%E0%A4%A8%E0%A5%80+%E0%A4%B9%E0%A5%88+{value['amount']}%0A%E0%A4%B8%E0%A4%82%E0%A4%97%E0%A5%8D%E0%A4%B0%E0%A4%B9+%E0%A4%B8%E0%A5%8D%E0%A4%A5%E0%A4%BE%E0%A4%A8+branch%0A%E0%A4%95%E0%A5%8D%E0%A4%AF%E0%A4%BE+%E0%A4%86%E0%A4%AA+%E0%A4%87%E0%A4%B8+%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF+%E0%A4%95%E0%A5%8B+%E0%A4%AA%E0%A5%82%E0%A4%B0%E0%A4%BE+%E0%A4%95%E0%A4%B0+%E0%A4%AA%E0%A4%BE%E0%A4%8F%E0%A4%82%E0%A4%97%E0%A5%87%3F&isTemplate=true&header=%E0%A4%86%E0%A4%AA%E0%A4%95%E0%A5%87+%E0%A4%AA%E0%A4%BE%E0%A4%B8+%E0%A4%8F%E0%A4%95+%E0%A4%A8%E0%A4%AF%E0%A4%BE+%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF+%E0%A4%B9%E0%A5%88"
                                    payload={}
                                    headers = {}
                                    response = requests.request("GET", url, headers=headers, data=payload)
                    # url = "https://media.smsgupshup.com/GatewayAPI/rest"
                    # headers = {
                    #     'Content-Type': 'application/x-www-form-urlencoded'
                    # }
                    # payload =f'userid={gupshup_uid}&password={gupshup_pass}&method=SendMessage&auth_scheme=plain&v=1.1&send_to={user_number}&msg=%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%86%E0%A4%88%E0%A4%A1%E0%A5%80%3A%20{task_id}%0A%E0%A4%86%E0%A4%AA%E0%A4%95%E0%A5%8B%20%E0%A4%B6%E0%A5%8D%E0%A4%B0%E0%A5%80%E0%A4%AE%E0%A4%BE%E0%A4%A8%20{creator_name}({creator_role})%20%E0%A4%B8%E0%A5%87%20%E0%A4%8F%E0%A4%95%20%E0%A4%A8%E0%A4%AF%E0%A4%BE%20%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%B8%E0%A5%8C%E0%A4%82%E0%A4%AA%E0%A4%BE%20%E0%A4%97%E0%A4%AF%E0%A4%BE%20%E0%A4%B9%E0%A5%88%E0%A5%A4%0A%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%B6%E0%A5%8D%E0%A4%B0%E0%A5%87%E0%A4%A3%E0%A5%80%20{category}%20%E0%A4%B9%E0%A5%88%E0%A5%A4%0A%E0%A4%89%E0%A4%AA%E0%A4%AD%E0%A5%8B%E0%A4%95%E0%A5%8D%E0%A4%A4%E0%A4%BE%20%E0%A4%B5%E0%A4%BF%E0%A4%B5%E0%A4%B0%E0%A4%A3%3A%20{customer_name}({customer_code})%0A%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%BE%E0%A4%A5%E0%A4%AE%E0%A4%BF%E0%A4%95%E0%A4%A4%E0%A4%BE%20{priority}%20%E0%A4%B9%E0%A5%88%E0%A5%A4%0A%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%95%E0%A5%80%20%E0%A4%B8%E0%A4%AE%E0%A4%AF%20%E0%A4%B8%E0%A5%80%E0%A4%AE%E0%A4%BE%20%E0%A4%B9%E0%A5%88%20{task_deadline}.%0A%E0%A4%85%E0%A4%A7%E0%A4%BF%E0%A4%95%20%E0%A4%9C%E0%A4%BE%E0%A4%A8%E0%A4%A8%E0%A5%87%20%E0%A4%95%E0%A5%87%20%E0%A4%B2%E0%A4%BF%E0%A4%8F%20%E0%A4%A8%E0%A5%80%E0%A4%9A%E0%A5%87%20%E0%A4%A6%E0%A4%BF%E0%A4%8F%20%E0%A4%97%E0%A4%8F%20%E0%A4%B2%E0%A4%BF%E0%A4%82%E0%A4%95%20%E0%A4%95%E0%A4%BE%20%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%AF%E0%A5%8B%E0%A4%97%20%E0%A4%95%E0%A4%B0%E0%A5%87%E0%A4%82%E0%A5%A4&msg_type=hsm&isHSM=true&isTemplate=true&data_encoding=Text&format=json&header=%E0%A4%86%E0%A4%AA%E0%A4%95%E0%A5%87%20%E0%A4%AA%E0%A4%BE%E0%A4%B8%20%E0%A4%8F%E0%A4%95%20%E0%A4%A8%E0%A4%AF%E0%A4%BE%20%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%B9%E0%A5%88&buttonUrlParam={task_id}'
                    # response = requests.request("POST", url, headers=headers, data=payload)
                    # print(response.text)
                        num = '91' + str(user_number)

                        #num = 8335076174
                        engine = get_db_engine()
                        sql_query = f""" INSERT INTO Sonata_Connect.dbo.whatsapp_log (waNumber,mobile,type,text_response,state,issue_id)
                        values (919151015811,{num},'image',{response.text},'bcd_alert',{issues_inst.id}) """
                        try:
                            dg=pd.read_sql_query(sql_query,engine)
                        except:
                            pass
                except Exception as e:
                    print('exc', e)
            else:
                print('no task to create for wrong number')

            call_status, p2p_date, p2p_amt, alt_no, loan_purpose, loan_amt = [None] * 6
            # Extraction of feedback points
            for item in loaded:
                # print("inside for loaded")
                for key,value in item.items():
                    # print(key,value)
                    if key == '331201' and value['status'] == True:
                        call_status = 'not_connected'   
                    if key == '331202' and value['status'] == True:
                        call_status = 'not_connected'          
                    if key == '33120501':
                        call_status = 'collection'
                        p2p_date = value['date']
                        p2p_amt = int(value['amount'])
                    if key == '33120601':
                        call_status = 'retention'
                        if 'loan_amount' not in value:
                            loan_amt = 0
                        else:
                            loan_amt = int(value['loan_amount'])
                        loan_purpose = value['loan_purpose']
                    if key == '331203':
                        if value['status'] == True:
                            call_status = 'wrong_number' 
                    if key == '33120302':
                        call_status = 'wrong_number'
                        alt_no = str(value['alternate_num'])
            # Datapoints submission in table
            feed_datapoint_obj = BusinessCallingFeedbackDataPoints()
            feed_datapoint_obj.UserID = business_caller_id
            # feed_datapoint_obj.RoleName = rolename
            feed_datapoint_obj.UserName = UserName
            # feed_datapoint_obj.Section = section
            feed_datapoint_obj.DisbursementID = disbursementid
            feed_datapoint_obj.CustomerInfoID = customerid
            # feed_datapoint_obj.ApplicantName = str(applicant_name)
            feed_datapoint_obj.Mobile_No = str(customer_contact_no)
            feed_datapoint_obj.Feedback_Status = str(call_status)
            feed_datapoint_obj.Alternate_No = alt_no
            feed_datapoint_obj.P2P_date = p2p_date
            feed_datapoint_obj.P2P_Amount = p2p_amt
            feed_datapoint_obj.Loan_Purpose = loan_purpose
            feed_datapoint_obj.Expected_Loan_Amount = loan_amt 
            feed_datapoint_obj.Task_ID = task_id
            feed_datapoint_obj.save()
            print("Data Points Saved")

            if ('331201' in loaded[0].keys()) or ('331202' in loaded[0].keys()):
                business_call_obj = BusinessCallingData.objects.filter(DisbursementID = disbursementid).filter(AllocatedDate__date=alloc_date).first()
                if (business_call_obj.calling_attempt is None) or (business_call_obj.calling_attempt < 3):
                    calling_count = business_call_obj.calling_attempt
                    if calling_count is None:
                        calling_count = 0
                    BusinessCallingData.objects.filter(DisbursementID = disbursementid).filter(AllocatedDate__date=alloc_date).update(
                        calling_attempt=calling_count + 1,
                        feedback_response=call_feedback_json, 
                        task_id=task_id, 
                        task_assigned_to=task_assigned_to,
                        call_initiated_id = call_initiated_id,
                        call_primary_id = call_primary_id)

                    business_history_obj = BusinessCallingDataHistory()
                    business_history_obj.DisbursementID = disbursementid
                    business_history_obj.feedback_response = call_feedback_json
                    business_history_obj.feedback_code = 1
                    business_history_obj.task_assigned_to = task_assigned_to
                    business_history_obj.task_id = task_id
                    business_history_obj.call_initiated_id = call_initiated_id
                    business_history_obj.call_primary_id = call_primary_id
                    business_history_obj.save()

                    print('calling attempt increased for1 ', disbursementid)
                    return JsonResponse({'status':'success','check':'true'})
                else:
                    BusinessCallingData.objects.filter(DisbursementID = disbursementid).filter(AllocatedDate__date=alloc_date).update(feedback_code = 1, task_id=task_id, task_assigned_to=task_assigned_to)

            else:

                BusinessCallingData.objects.filter(DisbursementID = disbursementid).filter(AllocatedDate__date=alloc_date).update(feedback_code = 1,calling_attempt = 1, task_id=task_id, task_assigned_to=task_assigned_to)
                print('calling attempt increased for2 ', disbursementid)

            BusinessCallingData.objects.filter(DisbursementID = disbursementid).filter(AllocatedDate__date=alloc_date).update(
                feedback_response = call_feedback_json,
                feedback_code = 1, task_id=task_id, 
                task_assigned_to=task_assigned_to,
                call_initiated_id = call_initiated_id,
                call_primary_id = call_primary_id)
            print('calling attempt increased for 3', disbursementid)
            sdf = pd.DataFrame(BusinessCallingData.objects.filter(DisbursementID = disbursementid).filter(AllocatedDate__date=alloc_date).values())
            print(sdf.to_dict(orient='r'),'~~~~~~~```')
            return JsonResponse({'status':'success','check':'false'})
        
def pending_promise_data(request):

    user = cache.get('user')
    user_id = user.UserID
    
    db = os.getenv('DATABASE_NAME')
    
    engine = get_db_engine()
    sql_query = f"""SET NOCOUNT ON;EXEC [{db}].[dbo].[S_SP_PendingPromisesData] @bcd_Userid = {user_id};SET NOCOUNT OFF"""
    df=pd.read_sql_query(sql_query,engine)
    return df

class TodaysPromises(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):

        user = cache.get('user')
        user_id = user.UserID

        context = {}
        min_date = str(date.today())
        today_date = datetime.today().date()
        from_date = to_date = datetime.strptime(min_date, "%Y-%m-%d").date()

        # Fetch todays promise section data from stored procedure
        promise_df = pending_promise_data(request)

        # Filter data through date
        promise_df = promise_df[(promise_df['promises_date'] >= from_date) & (promise_df['promises_date'] <= to_date)]
        total_card_count = len(promise_df)
        # Attempted data counts
        alloted_count = pd.DataFrame(PendingPromiseData.objects.filter(Userid=user_id,promise_date=today_date, feedback_code=1, promise_type='Todays-Promise').values())
        attempted_card_count = len(alloted_count)

        try:
            Todays_Promise_data = promise_df[~promise_df['DisbursementID'].duplicated(keep='first')]
            Todays_Promise_data['CenterMeetingWeekday'] = None
            Todays_Promise_data.loc[Todays_Promise_data['CenterMeetingDay'] == 55,'CenterMeetingWeekday'] = 'Monday'
            Todays_Promise_data.loc[Todays_Promise_data['CenterMeetingDay'] == 56,'CenterMeetingWeekday'] = 'Tuesday'
            Todays_Promise_data.loc[Todays_Promise_data['CenterMeetingDay'] == 57,'CenterMeetingWeekday'] = 'Wednesday'
            Todays_Promise_data.loc[Todays_Promise_data['CenterMeetingDay'] == 58,'CenterMeetingWeekday'] = 'Thursday'
            Todays_Promise_data.loc[Todays_Promise_data['CenterMeetingDay'] == 59,'CenterMeetingWeekday'] = 'Friday'
            Todays_Promise_data.loc[Todays_Promise_data['CenterMeetingDay'] == 60,'CenterMeetingWeekday'] = 'Saturday'
            Todays_Promise_data.loc[Todays_Promise_data['CenterMeetingDay'] == 61,'CenterMeetingWeekday'] = 'Sunday'
            Todays_Promise_data["CenterMeetingTime"] = None
            Todays_Promise_data['Centercode'] = Todays_Promise_data['Centercode'].fillna(value='Unavailable')
            Todays_Promise_data['CenterName'] = Todays_Promise_data['CenterName'].fillna(value='Unavailable')
            Todays_Promise_data['CenterMeetingWeekday'] = Todays_Promise_data['CenterMeetingWeekday'].fillna(value='Unavailable')
            Todays_Promise_data['CenterMeetingDay'] = Todays_Promise_data['CenterMeetingDay'].fillna(value='Schedule Unavailable')
            Todays_Promise_data['CenterMeetingTime'] = Todays_Promise_data['CenterMeetingTime'].fillna(value='Schedule Unavailable')
            Todays_Promise_data.fillna(0,inplace=True)
            Todays_Promise_data.eval('current_due_Amount = current_installment_Amount + pending_amount', inplace=True)
            Todays_Promise_data = Todays_Promise_data.sort_values(by=["promises_date"] , ascending = True)
        except Exception as e:
            context['total_card_count'] = 0
            context['attempted_card_count'] = 0
            context['alloted_card_count'] = 0
            messages.error(request,'No Promises found')
            print('error: calling day wise is empty', e)
            return TemplateResponse(request, 'todays_promise.html',context=context)

        context['min_date'] = min_date
        context['to_date'] = str(to_date)
        context['from_date'] = str(from_date)
        context['total_card_count'] = total_card_count
        context['attempted_card_count'] = attempted_card_count
        context['Todays_Promise_data'] = Todays_Promise_data.to_dict(orient="records")
        return TemplateResponse(request, "todays_promise.html", context=context)
    
    def post(self, request):

        user = cache.get('user')
        user_id = user.UserID

        business_caller_id = user_id
        UserName = str(user.UserName)
        call_feedback_json = request.POST.get('feedback_json')
        disbursementid = request.POST.get('disburstmentid')
        customerinfo_id = request.POST.get('customerinfoid')
        call_status, p2p_date, p2p_amt, alt_no, loan_purpose, loan_amt, task_id = [None] * 7

        # Fetch customer code form customerinfoid
        engine = get_db_engine()
        sql_query = f"""SET NOCOUNT ON;select CustomerCode from Sonata_Dec..mst_CustomerInfo
                                       where CustomerInfoId = {customerinfo_id};SET NOCOUNT OFF"""
        df = pd.read_sql_query(sql_query,engine)
        customercode = df.iloc[0]['CustomerCode']

        # customercode = DayWiseSummarised.objects.get(CustomerInfoId=customerinfo_id).CustomerCode
        loaded = json.loads(call_feedback_json)
        user_id =0
        task_idd=0

        applicant_name = request.POST.get('appname')    
        applicant_number = request.POST.get('mobile')  

        if request.POST.get('task5') == 'true':
            msg = []

            for item in loaded:
                    for key,value in item.items():
                        if key == '33120501':
                            msg1 = 'Customer will pay an amount of ' +  value['amount'] + ' on ' +  value['date'] + ' ' + value['time'] + ' by ' + value['mode_of_payment']
                            msg.append(msg1)
                        if key == '3312050102':
                            msg2 = '.' + value['paying_place']
                            print(msg2)
                            msg.append(msg2)
            if len(msg)>1:
                msg = (msg[0] + msg[1])
            else:
                msg = msg[0]            
            msg += f'Customer name {applicant_name} contact number {applicant_number}'

        if request.POST.get('task12') == 'true':
            msgg = []

            for item in loaded:
                    for key,value in item.items():
                        if key == '33121201':
                            msg3 = 'Appointment date is ' + value['proposed_date']
                            msgg.append(msg3)


            if len(msgg)>0:
                msgg = f'Collect bank statement from customer, name: {applicant_name} contact number: {applicant_number}' + msgg[0]
            else:
                msgg = ''

            print('.........................9999999999999999',msgg)


        disb_id = request.POST.get('disburstmentid')
        print('disb_id',disb_id)

        if request.POST.get('task3') == 'true':

            print("Wrong Number Communicated")
            task_name = 'Wrong Number Communicated'
            user_id = request.POST.get('user_id')
            usr_instance = Mst_UserTbl.objects.get(UserID = int(request.POST.get('user_id')))
            created_by = Mst_UserTbl.objects.get(UserID = int(user_id))
            deadline_date = datetime.now()
            priority = '1'
            category = '10'
            applicant_name = request.POST.get('appname')
            applicant_number = request.POST.get('mobile')
            alternate_number = None

            msgx = []

            for item in loaded:
                for key,value in item.items():
                    if key == '331203':
                        msg1 = 'Customer (Customer id: ' + str(customerinfo_id) + ') has communicated wrong number|'
                        msgx.append(msg1)
                    if key == '33120301':
                        if value['feedback_3'] != '':
                            msg2 = 'Feedback recieved: ' + value['feedback_3'] + '|'
                            msgx.append(msg2)
                    if key == '33120302':
                        alternate_number = value['alternate_num']
                        msg3 = 'Alternate number recieved ' + value['alternate_num'] + '|'
                        msgx.append(msg3)
            if len(msgx)>2:
                msgx = (msgx[0] + msgx[1] + msgx[2])
            elif len(msgx)>1:
                msgx = (msgx[0] + msgx[1])
            else:
                msgx = msgx[0]

            msgx += f'Customer name {applicant_name} contact number {applicant_number}' + '|'

            deadline_dt = None
            ## create a task for wrong number


            wn_task_obj = task_details()
            wn_task_obj.task_name = task_name
            wn_task_obj.task_description = msgx
            wn_task_obj.created_by = created_by
            wn_task_obj.assigned_to = usr_instance
            wn_task_obj.priority = priority
            wn_task_obj.t_info = disbursementid
            wn_task_obj.category = category  ## category?? check if correct
            wn_task_obj.deadline_date = deadline_date
            wn_task_obj.save() #temporarily commented
            #task details for later usage
            task_idd = wn_task_obj.task_id

            try:
                issues_inst = CallingIssues()
                issues_inst.category = 'Wrong Number Communicated'
                issues_inst.disbursement_id = int(disbursementid)
                issues_inst.customer_info_id = customerinfo_id
                issues_inst.customer_name = CustomerLevelSummarised.objects.get(CustomerInfoID = customerinfo_id).ApplicantName
                issues_inst.customer_number = CustomerLevelSummarised.objects.get(CustomerInfoID = customerinfo_id).mobile_no
                issues_inst.save()
            except Exception as e:
                print("calling issues inst not able to create : ", e)

            # Creating a Queue for wrong number 
            # whatsapp queue logic
            # user_number = 'Uncomment and Enter your number for testing flow '
            user_number = applicant_number
            broname = usr_instance.UserName
            # if belongs_to_test_region: # regionchecker
            try:
                try :
                    queue_instance = WhatsAppQueue()
                    queue_instance.user_id = user_id
                    queue_instance.flow_name = 'WNV_alert'
                    queue_instance.status = 3
                    queue_instance.update_time = datetime.now()
                    queue_instance.contact_number = user_number #str(applicant_number)
                    queue_instance.field_1 = broname
                    queue_instance.field_2 = CustomerLevelSummarised.objects.get(CustomerInfoID = customerinfo_id).ApplicantName
                    queue_instance.field_3 = customercode
                    queue_instance.field_4 = alternate_number
                    queue_instance.field_5 = wn_task_obj.deadline_date.date()
                    queue_instance.field_6 = wn_task_obj.deadline_date.strftime('%H:%M')
                    queue_instance.issue_id = issues_inst.id
                    queue_instance.task_id = task_idd
                    queue_instance.field_13 = user_number
                    queue_instance.field_14 = customerinfo_id
                    queue_instance.bc_id = business_caller_id
                    queue_instance.save()
                    visit_alert_id = queue_instance.id
                except Exception as e:
                    print("WNV_alert", e)

                try :
                    queue_instance = WhatsAppQueue()
                    queue_instance.user_id = user_id
                    queue_instance.flow_name = 'WNV_flow'
                    queue_instance.status = 3
                    queue_instance.update_time = datetime.now()
                    queue_instance.contact_number = user_number #str(applicant_number)
                    queue_instance.field_1 = broname
                    queue_instance.field_2 = CustomerLevelSummarised.objects.get(CustomerInfoID = customerinfo_id).ApplicantName
                    queue_instance.field_3 = customercode
                    queue_instance.field_4 = alternate_number
                    queue_instance.field_5 = wn_task_obj.deadline_date.date()
                    queue_instance.field_6 = wn_task_obj.deadline_date.strftime('%H:%M')
                    queue_instance.field_11 = visit_alert_id
                    queue_instance.issue_id = issues_inst.id
                    queue_instance.task_id = task_idd
                    queue_instance.field_13 = user_number
                    queue_instance.field_14 = customerinfo_id
                    queue_instance.bc_id = business_caller_id
                    queue_instance.save() 
                    visit_flow_id = queue_instance.id
                except Exception as e:
                    print("WNV_flow", e)

                if not alternate_number :
                    try :
                        queue_instance = WhatsAppQueue()
                        queue_instance.user_id = user_id
                        queue_instance.flow_name = 'WNANP_flow'
                        queue_instance.update_time = datetime.now()
                        queue_instance.contact_number = user_number #str(applicant_number)
                        queue_instance.field_1 = broname
                        queue_instance.field_2 = CustomerLevelSummarised.objects.get(CustomerInfoID = customerinfo_id).ApplicantName
                        queue_instance.field_3 = customercode
                        queue_instance.field_4 = alternate_number
                        queue_instance.field_5 = wn_task_obj.deadline_date.date()
                        queue_instance.field_6 = wn_task_obj.deadline_date.strftime('%H:%M')
                        queue_instance.field_7 = visit_alert_id
                        queue_instance.field_8 = visit_flow_id  
                        queue_instance.issue_id = issues_inst.id
                        queue_instance.task_id = task_idd
                        queue_instance.field_13 = user_number
                        queue_instance.field_14 = customerinfo_id
                        queue_instance.bc_id = business_caller_id
                        queue_instance.save()

                    except Exception as e:
                        print('WNANP_flow', e)

                else : ## ALternate Number Present
                    try :
                        queue_instance = WhatsAppQueue()
                        queue_instance.user_id = user_id
                        queue_instance.flow_name = 'WNAP_alert'
                        queue_instance.update_time = datetime.now()
                        queue_instance.contact_number = user_number #str(applicant_number)
                        queue_instance.field_1 = broname
                        queue_instance.field_2 = CustomerLevelSummarised.objects.get(CustomerInfoID = customerinfo_id).ApplicantName
                        queue_instance.field_3 = customercode
                        queue_instance.field_4 = alternate_number
                        queue_instance.field_5 = wn_task_obj.deadline_date.date()
                        queue_instance.field_6 = wn_task_obj.deadline_date.strftime('%H:%M')
                        queue_instance.field_7 = visit_alert_id
                        queue_instance.field_8 = visit_flow_id
                        queue_instance.issue_id = issues_inst.id
                        queue_instance.task_id = task_idd
                        queue_instance.field_13 = user_number
                        queue_instance.field_14 = customerinfo_id
                        queue_instance.bc_id = business_caller_id
                        queue_instance.save()
                        visit_instance_alert = queue_instance.id
                    except Exception as e:
                        print("WNAP_alert", e)

                    try :
                        from datetime import timedelta as td
                        queue_instance = WhatsAppQueue()
                        queue_instance.user_id = user_id
                        queue_instance.flow_name = 'WNAP_flow'
                        queue_instance.update_time = datetime.now() + td(hours=1)
                        queue_instance.contact_number = user_number #str(applicant_number)
                        queue_instance.field_1 = broname
                        queue_instance.field_2 = CustomerLevelSummarised.objects.get(CustomerInfoID = customerinfo_id).ApplicantName
                        queue_instance.field_3 = customercode
                        queue_instance.field_4 = alternate_number
                        queue_instance.field_5 = wn_task_obj.deadline_date.date()
                        queue_instance.field_6 = wn_task_obj.deadline_date.strftime('%H:%M')
                        queue_instance.field_7 = visit_alert_id
                        queue_instance.field_8 = visit_flow_id
                        queue_instance.issue_id = issues_inst.id
                        queue_instance.task_id = task_idd
                        queue_instance.field_13 = user_number
                        queue_instance.field_14 = customerinfo_id
                        queue_instance.bc_id = business_caller_id
                        queue_instance.save() 
                    except Exception as e:
                        print("WNAP_flow", e)
            except Exception as e:
                print("Wrong Number Communicated : ", e)

        if request.POST.get('task5') == 'true':

            user_id = request.POST.get('user_id')
            task_name = "Payment Collection Task"
            task_description = msg
            deadline_date = datetime.now()
            priority = "1"
            usr_instance = Mst_UserTbl.objects.get(UserID = int(user_id))
            created_by = Mst_UserTbl.objects.get(UserID = int(user_id))
            deadline_date = datetime.now()
            taskup_obj = task_details()
            taskup_obj.task_name = task_name
            taskup_obj.task_description = task_description
            taskup_obj.t_info = disb_id
            taskup_obj.created_by = created_by
            taskup_obj.assigned_to = usr_instance
            taskup_obj.category = "3"
            taskup_obj.deadline_date = deadline_date
            taskup_obj.priority = priority
            taskup_obj.save()
            print("task created successfully")
            task_idd = taskup_obj.task_id
            task_id = task_idd

            try:
                user_df = pd.DataFrame(calling_number_list.objects.filter(UserID=int(user_id)).values())
                user_number = user_df['CallingNumber']
                task_id = taskup_obj.task_id
                creator_name = request.user.UserName
                creator_role = request.session["RoleName"]
                category = taskup_obj.category
                customer_name = CustomerLevelSummarised.objects.get(CustomerInfoID = int(customerinfo_id)).ApplicantName
                customer_code = str(customerinfo_id)
                if priority == "1":
                    priority = 'Immediate'
                elif priority == "2":
                    priority = 'High'
                elif priority == "3":
                    priority = 'Medium'
                else:
                    priority = 'Low'
                task_deadline = taskup_obj.deadline_date

                url = "https://media.smsgupshup.com/GatewayAPI/rest"
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                payload =f'userid=2000209909&password=z24gzBUA&method=SendMessage&auth_scheme=plain&v=1.1&send_to={user_number}&msg=%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%86%E0%A4%88%E0%A4%A1%E0%A5%80%3A%20{task_id}%0A%E0%A4%86%E0%A4%AA%E0%A4%95%E0%A5%8B%20%E0%A4%B6%E0%A5%8D%E0%A4%B0%E0%A5%80%E0%A4%AE%E0%A4%BE%E0%A4%A8%20{creator_name}({creator_role})%20%E0%A4%B8%E0%A5%87%20%E0%A4%8F%E0%A4%95%20%E0%A4%A8%E0%A4%AF%E0%A4%BE%20%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%B8%E0%A5%8C%E0%A4%82%E0%A4%AA%E0%A4%BE%20%E0%A4%97%E0%A4%AF%E0%A4%BE%20%E0%A4%B9%E0%A5%88%E0%A5%A4%0A%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%B6%E0%A5%8D%E0%A4%B0%E0%A5%87%E0%A4%A3%E0%A5%80%20{category}%20%E0%A4%B9%E0%A5%88%E0%A5%A4%0A%E0%A4%89%E0%A4%AA%E0%A4%AD%E0%A5%8B%E0%A4%95%E0%A5%8D%E0%A4%A4%E0%A4%BE%20%E0%A4%B5%E0%A4%BF%E0%A4%B5%E0%A4%B0%E0%A4%A3%3A%20{customer_name}({customer_code})%0A%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%BE%E0%A4%A5%E0%A4%AE%E0%A4%BF%E0%A4%95%E0%A4%A4%E0%A4%BE%20{priority}%20%E0%A4%B9%E0%A5%88%E0%A5%A4%0A%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%95%E0%A5%80%20%E0%A4%B8%E0%A4%AE%E0%A4%AF%20%E0%A4%B8%E0%A5%80%E0%A4%AE%E0%A4%BE%20%E0%A4%B9%E0%A5%88%20{task_deadline}.%0A%E0%A4%85%E0%A4%A7%E0%A4%BF%E0%A4%95%20%E0%A4%9C%E0%A4%BE%E0%A4%A8%E0%A4%A8%E0%A5%87%20%E0%A4%95%E0%A5%87%20%E0%A4%B2%E0%A4%BF%E0%A4%8F%20%E0%A4%A8%E0%A5%80%E0%A4%9A%E0%A5%87%20%E0%A4%A6%E0%A4%BF%E0%A4%8F%20%E0%A4%97%E0%A4%8F%20%E0%A4%B2%E0%A4%BF%E0%A4%82%E0%A4%95%20%E0%A4%95%E0%A4%BE%20%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%AF%E0%A5%8B%E0%A4%97%20%E0%A4%95%E0%A4%B0%E0%A5%87%E0%A4%82%E0%A5%A4&msg_type=hsm&isHSM=true&isTemplate=true&data_encoding=Text&format=json&header=%E0%A4%86%E0%A4%AA%E0%A4%95%E0%A5%87%20%E0%A4%AA%E0%A4%BE%E0%A4%B8%20%E0%A4%8F%E0%A4%95%20%E0%A4%A8%E0%A4%AF%E0%A4%BE%20%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%20%E0%A4%B9%E0%A5%88&buttonUrlParam={task_id}'
                response = requests.request("POST", url, headers=headers, data=payload)
                print(response.text)
            except Exception as e:
                print('exc', e)

        else:
            print('no task to create for payment collection')

        if request.POST.get('agreed_on_payment') == 'true':

            user_id = request.POST.get('user_id')
            amount = request.POST.get('amount_to_pay')

            try:
                user_df = pd.DataFrame(calling_number_list.objects.filter(UserID=int(user_id)).values())
                user_number = user_df['CallingNumber']
                # task_id = taskup_obj.task_id
                # user_number ='8624008351'
                customer_name = CustomerLevelSummarised.objects.get(CustomerInfoID = int(customerinfo_id)).ApplicantName
                customer_code = str(customerinfo_id)

                url = "https://media.smsgupshup.com/GatewayAPI/rest"
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                payload =f'userid=2000209909&password=z24gzBUA&send_to={user_number}&v=1.1&format=json&msg_type=TEXT&method=SENDMESSAGE&msg=%E0%A4%97%E0%A5%8D%E0%A4%B0%E0%A4%BE%E0%A4%B9%E0%A4%95+{customer_name}%28{customer_code}%29+%E0%A4%A8%E0%A5%87+%E0%A4%86%E0%A4%9C+%E0%A4%A4%E0%A4%95+%E0%A4%85%E0%A4%AA%E0%A4%A8%E0%A5%87+%E0%A4%AC%E0%A4%95%E0%A4%BE%E0%A4%AF%E0%A4%BE+%E0%A4%AD%E0%A5%81%E0%A4%97%E0%A4%A4%E0%A4%BE%E0%A4%A8+%E0%A4%95%E0%A4%B0%E0%A4%A8%E0%A5%87+%E0%A4%95%E0%A5%80+%E0%A4%AA%E0%A5%81%E0%A4%B7%E0%A5%8D%E0%A4%9F%E0%A4%BF+%E0%A4%95%E0%A5%80+%E0%A4%B9%E0%A5%88%E0%A5%A4+%E0%A4%9C%E0%A4%AE%E0%A4%BE+%E0%A4%95%E0%A4%B0%E0%A4%A8%E0%A5%87+%E0%A4%95%E0%A5%87+%E0%A4%B2%E0%A4%BF%E0%A4%8F+%E0%A4%B0%E0%A4%BE%E0%A4%B6%E0%A4%BF+{amount}+%E0%A4%B9%E0%A5%88%E0%A5%A4+%E0%A4%95%E0%A5%83%E0%A4%AA%E0%A4%AF%E0%A4%BE+%E0%A4%89%E0%A4%A8%E0%A4%B8%E0%A5%87+%E0%A4%B8%E0%A4%82%E0%A4%AA%E0%A4%B0%E0%A5%8D%E0%A4%95+%E0%A4%95%E0%A4%B0%E0%A5%87%E0%A4%82+%E0%A4%94%E0%A4%B0+%E0%A4%B5%E0%A4%B8%E0%A5%82%E0%A4%B2%E0%A5%80+%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%95%E0%A5%8D%E0%A4%B0%E0%A4%BF%E0%A4%AF%E0%A4%BE+%E0%A4%AA%E0%A5%82%E0%A4%B0%E0%A5%80+%E0%A4%95%E0%A4%B0%E0%A5%87%E0%A4%82%E0%A5%A4&isTemplate=true&header=%E0%A4%A7%E0%A5%8D%E0%A4%AF%E0%A4%BE%E0%A4%A8+%E0%A4%A6%E0%A5%87%E0%A4%82%21'
                response = requests.request("POST", url, headers=headers, data=payload)
                print(response.text)
            except Exception as e:
                print('exc', e)

        else:
            print('no task to create for payment collection')

        # Extraction of feedback points
        for item in loaded:
            # print("inside for loaded")
            for key,value in item.items():
                # print(key,value)
                if key == '331201' and value['status'] == True:
                    call_status = 'not_connected'   
                if key == '331202' and value['status'] == True:
                    call_status = 'not_connected'          
                if key == '33120501':
                    call_status = 'collection'
                    p2p_date = value['date']
                    p2p_amt = int(value['amount'])
                if key == '33120601':
                    call_status = 'retention'
                    if 'loan_amount' not in value:
                        loan_amt = 0
                    else:
                        loan_amt = int(value['loan_amount'])
                    loan_purpose = value['loan_purpose']
                if key == '331203':
                    if value['status'] == True:
                        call_status = 'wrong_number' 
                if key == '33120302':
                    call_status = 'wrong_number'
                    alt_no = str(value['alternate_num'])

        # Datapoints submission in table
        feed_datapoint_obj = BusinessCallingFeedbackDataPoints()
        feed_datapoint_obj.UserID = business_caller_id
        # feed_datapoint_obj.RoleName = rolename
        feed_datapoint_obj.UserName = UserName
        # feed_datapoint_obj.Section = section
        feed_datapoint_obj.DisbursementID = disbursementid
        feed_datapoint_obj.CustomerInfoID = None
        # feed_datapoint_obj.ApplicantName = str(applicant_name)
        feed_datapoint_obj.Mobile_No = None
        feed_datapoint_obj.Feedback_Status = str(call_status)
        feed_datapoint_obj.Alternate_No = alt_no
        feed_datapoint_obj.P2P_date = p2p_date
        feed_datapoint_obj.P2P_Amount = p2p_amt
        feed_datapoint_obj.Loan_Purpose = loan_purpose
        feed_datapoint_obj.Expected_Loan_Amount = loan_amt 
        feed_datapoint_obj.Task_ID = task_id
        feed_datapoint_obj.save()
        print("Data Points Saved")

        if ('331201' in loaded[0].keys()) or ('331202' in loaded[0].keys()):

            todays_call_obj = PendingPromiseData.objects.filter(DisbursementID = disbursementid, promise_date=datetime.strptime(request.POST.get('promise_date'),'%Y-%m-%d')).first()
            if todays_call_obj is None:
                todays_call_obj = PendingPromiseData()
            if (todays_call_obj.calling_attempt is None) or (todays_call_obj.calling_attempt < 3):
                calling_count = todays_call_obj.calling_attempt
                if calling_count is None:
                    calling_count = 0
                if PendingPromiseData.objects.filter(DisbursementID = disbursementid, promise_date=datetime.strptime(request.POST.get('promise_date'),'%Y-%m-%d')).exists():
                    PendingPromiseData.objects.filter(DisbursementID = disbursementid, promise_date=datetime.strptime(request.POST.get('promise_date'),'%Y-%m-%d')).update(Userid = user_id, DisbursementID = disbursementid,task_id=task_idd,task_assigned_to=user_id,calling_attempt=calling_count + 1,feedback_response=call_feedback_json,promise_date=request.POST.get('promise_date'), promise_type='Todays-Promise')
                else:
                    PendingPromiseData.objects.create(Userid = user_id, DisbursementID = disbursementid,task_id=task_idd,task_assigned_to=user_id,calling_attempt=calling_count + 1,feedback_response=call_feedback_json,promise_date=request.POST.get('promise_date'), promise_type='Todays-Promise')

                todays_call_obj = PendingPromiseDataHistory()
                todays_call_obj.DisbursementID = disbursementid
                todays_call_obj.feedback_response = call_feedback_json
                todays_call_obj.promise_date = request.POST.get('promise_date')
                todays_call_obj.feedback_code = 1
                todays_call_obj.save()

                return JsonResponse({'status':'success','check':'true'})
            else:
                PendingPromiseData.objects.filter(DisbursementID = disbursementid, promise_date=datetime.strptime(request.POST.get('promise_date'),'%Y-%m-%d')).update(Userid = user_id, DisbursementID = disbursementid, feedback_response = call_feedback_json,feedback_code = 1,promise_date=request.POST.get('promise_date'), promise_type='Todays-Promise')

        if PendingPromiseData.objects.filter(DisbursementID = disbursementid, promise_date=datetime.strptime(request.POST.get('promise_date'),'%Y-%m-%d')).exists():
            PendingPromiseData.objects.filter(DisbursementID = disbursementid, promise_date=datetime.strptime(request.POST.get('promise_date'),'%Y-%m-%d')).update(Userid = user_id, DisbursementID = disbursementid,task_id=task_idd,task_assigned_to=user_id,calling_attempt = 1, feedback_response = call_feedback_json,feedback_code = 1,promise_date=request.POST.get('promise_date'), promise_type='Todays-Promise', P2P_date=feed_datapoint_obj.P2P_date, P2P_Amount=feed_datapoint_obj.P2P_Amount)
        else:
            PendingPromiseData.objects.create(Userid = user_id, DisbursementID = disbursementid,task_id=task_idd,task_assigned_to=user_id,calling_attempt = 1, feedback_response = call_feedback_json,feedback_code = 1,promise_date=request.POST.get('promise_date'), promise_type='Todays-Promise', P2P_date=feed_datapoint_obj.P2P_date, P2P_Amount=feed_datapoint_obj.P2P_Amount)

        return JsonResponse({'status':'success','check':'false'})