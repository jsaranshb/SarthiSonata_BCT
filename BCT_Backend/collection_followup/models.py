from django.db import models
from django.utils import timezone
from datetime import date, datetime

# Create your models here.
class CallingIssues(models.Model):
    category = models.CharField(max_length=255, default='')
    disbursement_id = models.IntegerField(null=True)
    customer_info_id = models.IntegerField(null=True)
    customer_name = models.CharField(max_length=255, default='')
    customer_number = models.IntegerField(null=True)
    promise_date = models.DateField()
    promise_time = models.CharField(max_length=255, default='')
    promise_amount = models.IntegerField(null=True)
    payment_method = models.CharField(max_length=255, default='')
   
    payment_collection_location = models.CharField(max_length=255, default='')
    bro_taskid = models.IntegerField(null=True)
    task_id_ref1 = models.IntegerField(null=True)
    task_id_ref2 = models.IntegerField(null=True)

    class Meta:
        managed = False
        db_table = "CallingIssues"

class WhatsAppQueue(models.Model):
    # id = models.IntegerField(null=False)
    user_id = models.IntegerField(null=False)
    task_id = models.IntegerField(null=False)
    flow_name = models.CharField(max_length=100)
    update_time = models.DateTimeField(blank=True, default=datetime.now())
    contact_number = models.IntegerField(null=False)
    status = models.IntegerField(null=False, default=0)
    stage = models.CharField(max_length=50)
    response = models.CharField(max_length=1000)
    counter = models.IntegerField(null=False, default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    bc_id = models.IntegerField(null=False)
    # string fields for message
    field_1 = models.CharField(max_length=50)
    field_2 = models.CharField(max_length=50)
    field_3 = models.CharField(max_length=50)
    field_4 = models.CharField(max_length=50)
    field_5 = models.CharField(max_length=50)
    field_6 = models.CharField(max_length=50)
    field_7 = models.CharField(max_length=50)
    field_8 = models.CharField(max_length=50)
    field_9 = models.CharField(max_length=50)
    field_10 = models.CharField(max_length=50)
    field_11 = models.CharField(max_length=50)
    field_12 = models.CharField(max_length=50)
    field_13 = models.CharField(max_length=50)
    field_14 = models.CharField(max_length=50)
    field_15 = models.CharField(max_length=50)
    field_16 = models.CharField(max_length=50)
    field_17 = models.CharField(max_length=50)
    field_18 = models.CharField(max_length=50)
    field_19 = models.CharField(max_length=50)
    field_20 = models.CharField(max_length=50)
    issue_id = models.IntegerField(null=True)
    exceptions_occured = models.CharField(max_length=500)
    conversations = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'WhatsAppQueue'

class Retention_Rejected_Clients(models.Model):
    Userid = models.IntegerField(null=False)
    DisbursementID = models.IntegerField(null=False)
    AllocatedDate = models.DateField(auto_now_add=True, null=True)

    class Meta:
        managed = False
        db_table = "retention_rejected_clients"

class demographic(models.Model):
    CustomerInfoId = models.BigIntegerField(primary_key=True, unique=True)
    Zone = models.CharField(max_length=9, blank=True, null=True, default="")
    DivID = models.IntegerField(blank=True, null=True)
    DivName = models.CharField(max_length=100, blank=True, null=True, default="")
    RgnID = models.IntegerField(blank=True, null=True)
    RgnName = models.CharField(max_length=100, blank=True, null=True, default="")
    HubID = models.IntegerField(blank=True, null=True)
    HubName = models.CharField(max_length=100, blank=True, null=True, default="")
    BranchId = models.IntegerField(blank=True, null=True)
    BranchName = models.CharField(max_length=100, blank=True, null=True, default="")
    CustomerCode = models.CharField(max_length=50, blank=True, null=True, default="")
    ApplicantName = models.CharField(max_length=100, default="")
    FirstName = models.CharField(max_length=100, blank=True, null=True, default="")
    MiddleName = models.CharField(max_length=100, blank=True, null=True, default="")
    LastName = models.CharField(max_length=50, blank=True, null=True, default="")
    Gender = models.CharField(max_length=2, blank=True, null=True, default="")
    mobile_no = models.CharField(max_length=50, blank=True, null=True, default="")
    LoanIterationNo = models.IntegerField(blank=True, null=True)
    DropOutStatus = models.CharField(max_length=1, blank=True, null=True, default="")
    EmailID = models.CharField(max_length=50, blank=True, null=True, default="")
    LoanTypeID = models.CharField(max_length=10, blank=True, null=True, default="")
    LoanType = models.CharField(max_length=3, default="")
    StaffId = models.IntegerField(blank=True, null=True)
    Staff = models.CharField(max_length=100, blank=True, null=True, default="")
    CustomerOnboardDt = models.DateTimeField()
    CenterId = models.IntegerField(blank=True, null=True)
    Centercode = models.CharField(max_length=30, blank=True, null=True, default="")
    CenterName = models.CharField(max_length=100, blank=True, null=True, default="")
    CenterStaff = models.IntegerField(blank=True, null=True)
    CenterStaffName = models.CharField(
        max_length=100, blank=True, null=True, default=""
    )
    Age = models.IntegerField(blank=True, null=True)
    DOB = models.DateTimeField(blank=True, null=True)
    BirthPlace = models.CharField(max_length=100, blank=True, null=True, default="")
    HusbandName = models.CharField(max_length=100, blank=True, null=True, default="")
    FatherName = models.CharField(max_length=100, blank=True, null=True, default="")
    MotherName = models.CharField(max_length=100, blank=True, null=True, default="")
    MaritalStatus = models.CharField(max_length=2, blank=True, null=True, default="")
    IsHandicaped = models.BooleanField(blank=True, null=True)
    MemberLiteracy = models.BooleanField(blank=True, null=True)
    Religion = models.IntegerField(blank=True, null=True)
    AgricultureIncome = models.DecimalField(
        max_digits=19, decimal_places=4, blank=True, null=True
    )
    AnimalValue = models.CharField(max_length=30, blank=True, null=True, default="")
    AnnualIncome = models.DecimalField(
        max_digits=19, decimal_places=4, blank=True, null=True, default=""
    )
    AssetValue = models.CharField(max_length=20, blank=True, null=True, default="")
    StateID = models.IntegerField(blank=True, null=True)
    LocationID = models.IntegerField(blank=True, null=True)
    Location = models.TextField(blank=True, null=True, default="")
    StateName = models.CharField(max_length=200, blank=True, null=True, default="")
    StateCode = models.CharField(max_length=5, blank=True, null=True, default="")
    DistrictID = models.IntegerField(blank=True, null=True)
    DistrictName = models.CharField(max_length=100, blank=True, null=True, default="")
    Address1 = models.CharField(max_length=1000, blank=True, null=True, default="")

    VillageName = models.CharField(max_length=100, blank=True, null=True, default="")
    ZipCode1 = models.CharField(max_length=50, blank=True, null=True)
    NatureOfBusiness = models.CharField(
        max_length=100, blank=True, null=True, default=""
    )

    occupation = models.CharField(max_length=150, null=True, blank=True)

    VillageName = models.CharField(max_length=100, null=True, blank=True)

    income_category = models.CharField(max_length=80, null=True, blank=True)
    age_category = models.CharField(max_length=80, null=True, blank=True)
    can_contact = models.BooleanField(default=False, null=True)
    can_call = models.BooleanField(default=False, null=True)

    assigned_to_ai = models.BooleanField(blank=True, null=True, default=False)

    legal_case_filed = models.CharField(max_length=10, blank=True, null=True)
    legal_case_number = models.CharField(max_length=200, blank=True, null=True)

    feedback = models.CharField(null=True, max_length=100, default="Not Available ")
    detailed_feedback = models.CharField(max_length=700, null=True, blank=True)
    # Need to disscuss

    contact_status = models.CharField(
        null=True, max_length=200, default="NON CONTACTABLE"
    )
    recommendation = models.CharField(null=True, max_length=100, default="")
    field_agent_id = models.CharField(null=True, max_length=100, default="")

    residential_status = models.CharField(null=True, max_length=150, default="")

    last_modified_date = models.DateTimeField(default=timezone.now, null=True)

    class Meta:
        unique_together = [["CustomerInfoId"]]

class CustomerLevelSummarised(models.Model):
    CustomerInfoID = models.ForeignKey(
        demographic, on_delete=models.CASCADE, db_column="CustomerInfoID", primary_key=True
    )
    # cid = models.BigIntegerField()
    ApplicantName = models.CharField(max_length=100, default="")
    No_Of_Loans = models.IntegerField()
    Pending_Installments = models.IntegerField()
    total_outstanding = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    total_pos = models.DecimalField(max_digits=19,decimal_places=4, blank=True, null=True)
    # loan_count_from_ammort = models.IntegerField()
    DisbursementID = models.IntegerField()
    DisbursementDate = models.DateTimeField(blank=True, null=True)
    Max_User_DPD = models.IntegerField()
    mobile_no = models.CharField(max_length=50, blank=True, null=True, default="")
    CustomerCode = models.CharField(max_length=50, blank=True, null=True, default="")
    CenterID = models.BigIntegerField()
    UserID = models.BigIntegerField()
    # f1 = models.IntegerField()
    # f2 = models.IntegerField()
    # f3 = models.IntegerField()
    
    NON_ACTIVE_NON_WOFF=models.IntegerField()
    Dropout_Inactive=models.IntegerField()
    class Meta:
        managed = False
        db_table = "Customer_level_summarised_final"

class Retention_Response(models.Model):
    Userid = models.IntegerField(null=False)
    DisbursementID = models.IntegerField(null=False)
    allocated_date = models.DateTimeField(null=True)
    send_date = models.DateField(null=True)
    amount = models.IntegerField(null=True)
    purpose = models.CharField(max_length=200)
    bank_account_details = models.CharField(max_length=200)
    coapp_info = models.CharField(max_length=500)
    new_address = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'Retention_Response'

class BusinessCallingFeedbackDataPoints(models.Model):
    id = models.AutoField(primary_key=True)
    Submission_Date = models.DateField(auto_now_add=True,null=True)
    UserID = models.IntegerField(null=False)
    UserName = models.CharField(max_length=100,default='')
    # RoleName = models.CharField(max_length=100,default='')
    # Section = models.CharField(max_length=200,default='')
    DisbursementID = models.IntegerField(null=False)
    CustomerInfoID = models.IntegerField(null=False)
    # ApplicantName = models.CharField(max_length=100,default='')
    Mobile_No = models.CharField(max_length=100,default='')
    Feedback_Status = models.CharField(max_length=100,default='')
    Alternate_No = models.CharField(max_length=100,default='')
    P2P_date = models.DateField(null=True)
    P2P_Amount = models.IntegerField(null=True)
    Expected_Loan_Amount = models.IntegerField(null=True)
    Loan_Purpose = models.CharField(max_length=2000,default='')
    Task_ID = models.IntegerField(null=True)
    # Path = models.CharField(max_length=1000,default='')
    class Meta:
        managed = False
        db_table = "Business_calling_Feedback_DataPoints"

class Retention_Calling_History(models.Model):
    Srno = models.AutoField(primary_key=True)
    DisbursementID = models.IntegerField(null=False)
    LastDialledDate = models.DateField(auto_now_add=True,null=True)
    task_id = models.CharField(max_length=100,default='')
    task_assigned_to = models.IntegerField(null=False)
    task_status = models.CharField(max_length=100,default='')
    task_completion_date = models.DateField(auto_now_add=True,null=True)
    feedback_response = models.CharField(max_length=100,default='')
    feedback_code = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = "Retention_Calling_History"

class FeedbackObservations(models.Model):
    reason = models.CharField(max_length=1000, default='')

    class Meta:
        managed = False
        db_table = "FeedbackObservations"

class BusinessCallingDataHistory(models.Model):
    Srno = models.AutoField(primary_key=True)
    DisbursementID = models.IntegerField(null=False)
    LastDialledDate = models.DateField(auto_now_add=True,null=True)
    task_id = models.CharField(max_length=100,default='')
    task_assigned_to = models.IntegerField(null=False)
    task_status = models.CharField(max_length=100,default='')
    task_completion_date = models.DateField(auto_now_add=True,null=True)
    feedback_response = models.CharField(max_length=100,default='')
    feedback_code = models.BooleanField(default=True)
    call_primary_id = models.IntegerField(null=True)
    call_initiated_id = models.IntegerField(null=True)

    class Meta:
        managed = False
        db_table = "businesscallingdatahistory"

class PendingPromiseDataHistory(models.Model):
    Srno = models.AutoField(primary_key=True)
    DisbursementID = models.IntegerField(null=False)
    LastDialledDate = models.DateField(auto_now_add=True,null=True)
    task_id = models.CharField(max_length=100,default='')
    task_assigned_to = models.IntegerField(null=False)
    task_status = models.CharField(max_length=100,default='')
    task_completion_date = models.DateField(auto_now_add=True,null=True)
    feedback_response = models.CharField(max_length=100,default='')
    feedback_code = models.BooleanField(default=True)
    promise_date = models.DateField(null=True)
    class Meta:
        managed = False
        db_table = "PendingPromiseData_History"