from django.db import models

class BusinessCallingData(models.Model):
    Userid = models.IntegerField(null=False)
    DisbursementID = models.IntegerField(null=False)
    AllocatedDate = models.DateTimeField(null=True)
    Type = models.CharField(max_length=100, default='')
    CallingStatus = models.CharField(max_length=100, default='')
    calling_status = models.CharField(max_length=100, default='')
    call_date_time = models.DateTimeField(blank=True, null=True)
    reschedule_date_time = models.DateTimeField(blank=True, null=True)
    customer_feedback = models.CharField(max_length=500, default='')
    sequence_number = models.CharField(max_length=100, default='')
    collection_classfication = models.CharField(max_length=100, default='')
    collection_history_band = models.CharField(max_length=100, default='')
    is_delegated = models.BooleanField(default=True)
    is_reallocated = models.BooleanField(default=True)
    repeat_call = models.BooleanField(default=True)
    task_id = models.CharField(max_length=100, default='')
    task_assigned_to = models.IntegerField(null=True)
    task_status = models.CharField(max_length=100, default='')
    task_completion_date = models.DateField(auto_now_add=True, null=True)
    feedback_response = models.CharField(max_length=100, default='')
    feedback_code = models.BooleanField(default=True)
    calling_attempt = models.IntegerField(null=True)
    IS_active = models.BooleanField(null=True)
    call_primary_id = models.IntegerField(null=True)
    call_initiated_id = models.IntegerField(null=True)
    
    
    class Meta:
        managed = False
        db_table = 'BusinessCallingData'



class PendingPromiseData(models.Model):
    Userid = models.IntegerField(null=False)
    DisbursementID = models.IntegerField(null=False)
    AllocatedDate = models.DateField(auto_now_add=True,null=True)
    Type = models.CharField(max_length=100,default='')
    calling_attempt = models.IntegerField(null=True)
    CallingStatus = models.CharField(max_length=100,default='')
    calling_status = models.CharField(max_length=100,default='')
    call_date_time = models.DateTimeField(blank=True, null=True)
    reschedule_date_time = models.DateTimeField(blank=True, null=True)
    customer_feedback = models.CharField(max_length=500,default='')
    sequence_number = models.CharField(max_length=100,default='')
    collection_classfication = models.CharField(max_length=100,default='')
    collection_history_band = models.CharField(max_length=100,default='')
    is_delegated = models.BooleanField(default=True)
    is_reallocated = models.BooleanField(default=True)
    repeat_call = models.BooleanField(default=True)
    task_id = models.CharField(max_length=100,default='')
    task_assigned_to = models.IntegerField(null=False)
    task_status = models.CharField(max_length=100,default='')
    task_completion_date = models.DateField(auto_now_add=True,null=True)
    feedback_response = models.CharField(max_length=100,default='')
    feedback_code = models.BooleanField(null=True)
    promise_date = models.DateField(null=True)
    promise_type = models.CharField(max_length=100,default='')
    class Meta:
        managed = False
        db_table = 'PendingPromiseData'
        

class NpaCollectionExpressLoanRepository(models.Model):
    DisbursementID = models.CharField(primary_key=True, max_length=255)
    filter1 = models.CharField(max_length=255)
    active_loans = models.IntegerField()
    As_On_Date = models.DateField()
    BranchID = models.CharField(max_length=50)
    CustomerInfoID = models.CharField(max_length=50)
    LoanType = models.IntegerField()
    DisbursementDate = models.DateField()
    DisbursedAmt = models.DecimalField(max_digits=18, decimal_places=2)
    CenterID = models.IntegerField()
    Centercode = models.CharField(max_length=20)
    CustomerCode = models.CharField(max_length=20)
    CenterName = models.CharField(max_length=100)
    ApplicantName = models.CharField(max_length=100)
    mobile_no = models.IntegerField()
    ProductName = models.CharField(max_length=100)
    UserID = models.IntegerField()
    latest_collected_date = models.DateField()
    loan_classification = models.CharField(max_length=50)
    Loan_Closing_Date = models.DateField()
    ret_status = models.IntegerField()
    channel = models.CharField(max_length=50)
    wh_status = models.IntegerField()
    wh_date = models.DateField()
    blaster_status = models.IntegerField()
    blaster_date = models.DateField()
    vb_status = models.IntegerField()
    vd_date = models.DateField()
    cc_status = models.IntegerField()
    cc_date = models.DateField()
    is_retained = models.BooleanField()
    pending_amount = models.IntegerField()
    pending_installments = models.IntegerField()
    feedback_response = models.CharField(max_length=100,default='')
    feedback_code = models.BooleanField(null=True)
    IS_active = models.BooleanField(null=True)
    calling_attempt = models.IntegerField(null=True)
    feedback_user_id = models.IntegerField(null=True)
    UploadedDate = models.DateField()
    feedback_response = models.CharField(max_length=100,default='')
    feedback_code = models.BooleanField(null=True)
    IS_active = models.BooleanField(null=True)
    calling_attempt = models.IntegerField(null=True)
    bm_call = models.BooleanField(null=True)

    class Meta:
        managed = False
        db_table = 'npa_collection_repository'


class Retention_Calling_Data(models.Model):
    Userid = models.IntegerField(null=False)
    DisbursementID = models.IntegerField(null=False)
    AllocatedDate = models.DateField(auto_now_add=True, null=True)
    Type = models.CharField(max_length=100, default='')
    CallingStatus = models.CharField(max_length=100, default='')
    calling_status = models.CharField(max_length=100, default='')
    call_date_time = models.DateTimeField(blank=True, null=True)
    reschedule_date_time = models.DateTimeField(blank=True, null=True)
    customer_feedback = models.CharField(max_length=500, default='')
    sequence_number = models.CharField(max_length=100, default='')
    collection_classfication = models.CharField(max_length=100, default='')
    collection_history_band = models.CharField(max_length=100, default='')
    is_delegated = models.BooleanField(default=True)
    is_reallocated = models.BooleanField(default=True)
    repeat_call = models.BooleanField(default=True)
    task_id = models.CharField(max_length=100, default='')
    task_assigned_to = models.IntegerField(null=False)
    task_status = models.CharField(max_length=100, default='')
    task_completion_date = models.DateField(auto_now_add=True, null=True)
    feedback_response = models.CharField(max_length=100, default='')
    feedback_code = models.BooleanField(default=True)
    calling_attempt = models.IntegerField(null=True)
    IS_active = models.BooleanField(null=True)

    class Meta:
        managed = False
        db_table = 'accounts_Retention_Calling_Data'


class DayWiseSummarised(models.Model):
    # id = models.IntegerField(db_column="DisbursementID", primary_key=True)dat
    CustomerInfoId = models.BigIntegerField()
    BranchID = models.IntegerField()
    As_On_Date = models.DateField()
    DisbursementID = models.IntegerField(primary_key=True)
    mobile_no = models.CharField(max_length=50, blank=True, null=True)
    LoanType = models.IntegerField(blank=True, null=True)
    DisbursementDate = models.DateTimeField(blank=True, null=True)
    DisbursedAmt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    CenterID = models.IntegerField(blank=True, null=True)
    ProductName = models.CharField(max_length=100)
    Centercode = models.CharField(max_length=30, blank=True, null=True)
    CustomerCode = models.CharField(max_length=50, blank=True, null=True)  #
    CenterName = models.CharField(max_length=100, blank=True, null=True)
    ApplicantName = models.CharField(max_length=100, blank=True, null=True)  #
    # StaffId_Recg = models.IntegerField(blank=True, null=True)
    CenterMeetingTime = models.DateTimeField(blank=True, null=True)
    CenterMeetingDay = models.IntegerField(blank=True, null=True)
    UserID = models.CharField(max_length=100, blank=True, null=True)
    user_dpd_max = models.IntegerField(blank=True, null=True)
    account_DPD = models.IntegerField(blank=True, null=True)
    user_arrear_max = models.IntegerField(blank=True, null=True)
    account_arrear = models.IntegerField(blank=True, null=True)
    Is_NPA_Before=models.IntegerField(blank=True, null=True)
    pending_amount = models.DecimalField(
        max_digits=38, decimal_places=4, blank=True, null=True
    )
    total_outstanding = models.DecimalField(
        max_digits=38, decimal_places=4, blank=True, null=True
    )
    User_Arrear = models.IntegerField(blank=True, null=True)
    loan_classification = models.CharField(max_length=12, blank=True)
    Other_Active_Accounts = models.IntegerField(blank=True, null=True)
    current_installment_Amount = models.IntegerField(blank=True, null=True)
    upcoming_installment_ID = models.IntegerField(blank=True, null=True)
    upcoming_installment_Amount = models.IntegerField(blank=True, null=True)
    current_installment_ID = models.BigIntegerField(blank=True)
    principle_outstanding = models.BigIntegerField(blank=True)
    principle_arrear = models.BigIntegerField(blank=True)
    moratorium = models.BigIntegerField(blank=True)
    longitude = models.DecimalField(
        max_digits=19, decimal_places=4, blank=True, null=True
    )
    latitude = models.DecimalField(
        max_digits=19, decimal_places=4, blank=True, null=True
    )
    RIC = models.BooleanField(default=True)
   
    # call_response =  models.CharField(max_length=1000, blank=True, null=True)
    present_status = models.BooleanField(default=True)
    visited_status = models.BooleanField(default=True)
    Loan_Recommendation  = models.BooleanField(default=True)
    latest_3_emi_npa_flag = models.BooleanField(default=True)
    # next_promise_date = models.DateTimeField(null=True)
    
    # payment_status = models.CharField(max_length=100, null=True)
    
    # amount_collected = models.DecimalField(max_digits=18, decimal_places=2, null=True)
    
    # not_paying_reson = models.CharField(max_length=100, null=True)
    Last_Month_User_DPD =  models.IntegerField(blank=True, null=True)
    Last_Month_User_Arrear = models.IntegerField(blank=True, null=True)
    # first_time_arrear_clients=models.BooleanField(default=True)
    Total_Arrear=models.IntegerField(blank=True, null=True)

    # CONSTITUTION=models.CharField(max_length=100)
    NEW_ACCTS_IN_LAST_SIX_MONTHS= models.BigIntegerField(blank=True, null=True)
    DELINQUENT_ACCTS_IN_LAST_SIX_MONTHS= models.BigIntegerField(blank=True)
    # MAX_WORST_DELEQUENCY= models.BigIntegerField(blank=True)
    # INQUIRIES_IN_LAST_SIX_MONTHS= models.BigIntegerField(blank=True)
    # PRI_ASSOCIATION_OWN= models.BigIntegerField(blank=True)
    # PRI_ASSOCIATION_OTH= models.BigIntegerField(blank=True)
    # PRI_ASSOCIATION_OTH_ACTIVE= models.BigIntegerField(blank=True)
    # PRI_ACCTS_TOTAL= models.BigIntegerField(blank=True)
    # PRI_ACTIVE_ACCTS_TOTAL= models.BigIntegerField(blank=True)
    # PRI_CLOSED_ACCTS_TOTAL= models.BigIntegerField(blank=True)
    # PRI_DEFAULT_ACCTS_TOTAL=models.CharField(max_length=100)
    # PRI_DISBURSED_AMT_OWN=models.CharField(max_length=100)
    # PRI_DISBURSED_AMT_OTH=models.BigIntegerField(blank=True)
    # PRI_INSTAL_AMT_OWN=models.BigIntegerField(blank=True)
    # PRI_INSTAL_AMT_OTH= models.BigIntegerField(blank=True)
    # PRI_CURR_BALANCE_OWN= models.BigIntegerField(blank=True)
    # PRI_CURR_BALANCE_OTH=models.BigIntegerField(blank=True)
    Remaning_Installments = models.IntegerField(blank=True)
    last_three_installment=models.IntegerField(blank=True)
    payment_gap=models.IntegerField(blank=True)
    Total_Grantor=models.IntegerField(blank=True, null=True)
    Last_Disb_Date=  models.DateTimeField(blank=True, null=True)
    Others_Last_Paid_Date= models.DateTimeField()
    Sonata_Last_Paid_Date= models.DateTimeField()
    DISBURSED_AMT=models.IntegerField(blank=True, null=True)
    CURRENT_BAL=models.IntegerField(blank=True, null=True)
    OVERDUE_AMT=models.IntegerField(blank=True, null=True)
    Last_Disb_Amt=models.IntegerField(blank=True, null=True)
    Last_CREDIT_GRANTOR=models.CharField(max_length=100)
    pending_emi_date=models.DateTimeField(blank=True, null=True)
    latest_collected_date=models.DateTimeField(blank=True, null=True)
    First_Time_Arrear_Clients = models.IntegerField(blank=True, null=True)
    CUSTOMER_ID = models.FloatField(blank=True, null=True)
    LOS_APP_ID = models.BigIntegerField(blank=True, null=True)
    PERFORM_CNS_SCORE = models.BigIntegerField(blank=True, null=True)
    PERFORM_CNS_SCORE_DESCRIPTION = models.CharField(max_length=4000, blank=True, null=True)
    NO_OF_INQUIRIES = models.BigIntegerField(blank=True, null=True)
    PRI_NO_OF_ACCTS = models.BigIntegerField(blank=True, null=True)
    SEC_NO_OF_ACCTS = models.BigIntegerField(blank=True, null=True)
    PRI_ACTIVE_ACCTS = models.BigIntegerField(blank=True, null=True)
    SEC_ACTIVE_ACCTS= models.BigIntegerField(blank=True, null=True)
    PRI_OVERDU_ACCTS = models.BigIntegerField(blank=True, null=True)
    SEC_OVERDUE_ACCTS = models.BigIntegerField(blank=True, null=True)
    PRI_CURRENT_BALANCE = models.BigIntegerField(blank=True, null=True)
    SEC_CURRENT_BALANCE = models.BigIntegerField(blank=True, null=True)
    PRI_SANCTIONED_AMOUNT = models.BigIntegerField(blank=True, null=True)
    SEC_SANCTIONED_AMOUNT = models.BigIntegerField(blank=True, null=True)
    PRI_DISBURSED_AMOUNT = models.BigIntegerField(blank=True, null=True)
    SEC_DISBURSED_AMOUNT = models.BigIntegerField(blank=True, null=True)
    PRIMARY_INSTAL_AMT = models.BigIntegerField(blank=True, null=True)
    SEC_INSTAL_AMT = models.BigIntegerField(blank=True, null=True)
    AVERAGE_ACCT_AGE = models.CharField(max_length=4000, blank=True, null=True)
    CREDIT_HISTORY_LENGTH = models.CharField(max_length=4000, blank=True, null=True)
    Loan_Closing_Date = models.DateTimeField(blank=True, null=True)
    Predicted = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'day_wise_summarised_final'
        # VW_day_wise_summarised


class Pending_Proposal_Data(models.Model):
    Userid = models.IntegerField(null=False)
    DisbursementID = models.IntegerField(null=False)
    AllocatedDate = models.DateField(auto_now_add=True, null=True)
    Type = models.CharField(max_length=100, default='')
    CallingStatus = models.CharField(max_length=100, default='')
    calling_status = models.CharField(max_length=100, default='')
    call_date_time = models.DateTimeField(blank=True, null=True)
    reschedule_date_time = models.DateTimeField(blank=True, null=True)
    customer_feedback = models.CharField(max_length=500, default='')
    sequence_number = models.CharField(max_length=100, default='')
    collection_classfication = models.CharField(max_length=100, default='')
    collection_history_band = models.CharField(max_length=100, default='')
    is_delegated = models.BooleanField(default=True)
    is_reallocated = models.BooleanField(default=True)
    repeat_call = models.BooleanField(default=True)
    task_id = models.CharField(max_length=100, default='')
    task_assigned_to = models.IntegerField(null=False)
    task_status = models.CharField(max_length=100, default='')
    task_completion_date = models.DateField(auto_now_add=True, null=True)
    feedback_response = models.CharField(max_length=100, default='')
    feedback_code = models.BooleanField(default=True)
    calling_attempt = models.IntegerField(null=True)
    IS_active = models.BooleanField(null=True)

    class Meta:
        managed = False
        db_table = 'Pending_Proposal_Data'
 