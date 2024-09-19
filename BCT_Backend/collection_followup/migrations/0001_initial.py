# Generated by Django 5.0.9 on 2024-09-16 08:55

import datetime
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessCallingFeedbackDataPoints',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Submission_Date', models.DateField(auto_now_add=True, null=True)),
                ('UserID', models.IntegerField()),
                ('UserName', models.CharField(default='', max_length=100)),
                ('DisbursementID', models.IntegerField()),
                ('CustomerInfoID', models.IntegerField()),
                ('Mobile_No', models.CharField(default='', max_length=100)),
                ('Feedback_Status', models.CharField(default='', max_length=100)),
                ('Alternate_No', models.CharField(default='', max_length=100)),
                ('P2P_date', models.DateField(null=True)),
                ('P2P_Amount', models.IntegerField(null=True)),
                ('Expected_Loan_Amount', models.IntegerField(null=True)),
                ('Loan_Purpose', models.CharField(default='', max_length=2000)),
                ('Task_ID', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'Business_calling_Feedback_DataPoints',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CallingIssues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(default='', max_length=255)),
                ('disbursement_id', models.IntegerField(null=True)),
                ('customer_info_id', models.IntegerField(null=True)),
                ('customer_name', models.CharField(default='', max_length=255)),
                ('customer_number', models.IntegerField(null=True)),
                ('promise_date', models.DateField()),
                ('promise_time', models.CharField(default='', max_length=255)),
                ('promise_amount', models.IntegerField(null=True)),
                ('payment_method', models.CharField(default='', max_length=255)),
                ('payment_collection_location', models.CharField(default='', max_length=255)),
                ('bro_taskid', models.IntegerField(null=True)),
                ('task_id_ref1', models.IntegerField(null=True)),
                ('task_id_ref2', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'CallingIssues',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='demographic',
            fields=[
                ('CustomerInfoId', models.BigIntegerField(primary_key=True, serialize=False, unique=True)),
                ('Zone', models.CharField(blank=True, default='', max_length=9, null=True)),
                ('DivID', models.IntegerField(blank=True, null=True)),
                ('DivName', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('RgnID', models.IntegerField(blank=True, null=True)),
                ('RgnName', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('HubID', models.IntegerField(blank=True, null=True)),
                ('HubName', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('BranchId', models.IntegerField(blank=True, null=True)),
                ('BranchName', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('CustomerCode', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('ApplicantName', models.CharField(default='', max_length=100)),
                ('FirstName', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('MiddleName', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('LastName', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('Gender', models.CharField(blank=True, default='', max_length=2, null=True)),
                ('mobile_no', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('LoanIterationNo', models.IntegerField(blank=True, null=True)),
                ('DropOutStatus', models.CharField(blank=True, default='', max_length=1, null=True)),
                ('EmailID', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('LoanTypeID', models.CharField(blank=True, default='', max_length=10, null=True)),
                ('LoanType', models.CharField(default='', max_length=3)),
                ('StaffId', models.IntegerField(blank=True, null=True)),
                ('Staff', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('CustomerOnboardDt', models.DateTimeField()),
                ('CenterId', models.IntegerField(blank=True, null=True)),
                ('Centercode', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('CenterName', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('CenterStaff', models.IntegerField(blank=True, null=True)),
                ('CenterStaffName', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('Age', models.IntegerField(blank=True, null=True)),
                ('DOB', models.DateTimeField(blank=True, null=True)),
                ('BirthPlace', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('HusbandName', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('FatherName', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('MotherName', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('MaritalStatus', models.CharField(blank=True, default='', max_length=2, null=True)),
                ('IsHandicaped', models.BooleanField(blank=True, null=True)),
                ('MemberLiteracy', models.BooleanField(blank=True, null=True)),
                ('Religion', models.IntegerField(blank=True, null=True)),
                ('AgricultureIncome', models.DecimalField(blank=True, decimal_places=4, max_digits=19, null=True)),
                ('AnimalValue', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('AnnualIncome', models.DecimalField(blank=True, decimal_places=4, default='', max_digits=19, null=True)),
                ('AssetValue', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('StateID', models.IntegerField(blank=True, null=True)),
                ('LocationID', models.IntegerField(blank=True, null=True)),
                ('Location', models.TextField(blank=True, default='', null=True)),
                ('StateName', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('StateCode', models.CharField(blank=True, default='', max_length=5, null=True)),
                ('DistrictID', models.IntegerField(blank=True, null=True)),
                ('DistrictName', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('Address1', models.CharField(blank=True, default='', max_length=1000, null=True)),
                ('ZipCode1', models.CharField(blank=True, max_length=50, null=True)),
                ('NatureOfBusiness', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('occupation', models.CharField(blank=True, max_length=150, null=True)),
                ('VillageName', models.CharField(blank=True, max_length=100, null=True)),
                ('income_category', models.CharField(blank=True, max_length=80, null=True)),
                ('age_category', models.CharField(blank=True, max_length=80, null=True)),
                ('can_contact', models.BooleanField(default=False, null=True)),
                ('can_call', models.BooleanField(default=False, null=True)),
                ('assigned_to_ai', models.BooleanField(blank=True, default=False, null=True)),
                ('legal_case_filed', models.CharField(blank=True, max_length=10, null=True)),
                ('legal_case_number', models.CharField(blank=True, max_length=200, null=True)),
                ('feedback', models.CharField(default='Not Available ', max_length=100, null=True)),
                ('detailed_feedback', models.CharField(blank=True, max_length=700, null=True)),
                ('contact_status', models.CharField(default='NON CONTACTABLE', max_length=200, null=True)),
                ('recommendation', models.CharField(default='', max_length=100, null=True)),
                ('field_agent_id', models.CharField(default='', max_length=100, null=True)),
                ('residential_status', models.CharField(default='', max_length=150, null=True)),
                ('last_modified_date', models.DateTimeField(default=django.utils.timezone.now, null=True)),
            ],
            options={
                'unique_together': {('CustomerInfoId',)},
            },
        ),
        migrations.CreateModel(
            name='Retention_Rejected_Clients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Userid', models.IntegerField()),
                ('DisbursementID', models.IntegerField()),
                ('AllocatedDate', models.DateField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'retention_rejected_clients',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Retention_Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Userid', models.IntegerField()),
                ('DisbursementID', models.IntegerField()),
                ('allocated_date', models.DateTimeField(null=True)),
                ('send_date', models.DateField(null=True)),
                ('amount', models.IntegerField(null=True)),
                ('purpose', models.CharField(max_length=200)),
                ('bank_account_details', models.CharField(max_length=200)),
                ('coapp_info', models.CharField(max_length=500)),
                ('new_address', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'Retention_Response',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WhatsAppQueue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('task_id', models.IntegerField()),
                ('flow_name', models.CharField(max_length=100)),
                ('update_time', models.DateTimeField(blank=True, default=datetime.datetime(2024, 9, 16, 14, 25, 34, 745102))),
                ('contact_number', models.IntegerField()),
                ('status', models.IntegerField(default=0)),
                ('stage', models.CharField(max_length=50)),
                ('response', models.CharField(max_length=1000)),
                ('counter', models.IntegerField(default=0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('bc_id', models.IntegerField()),
                ('field_1', models.CharField(max_length=50)),
                ('field_2', models.CharField(max_length=50)),
                ('field_3', models.CharField(max_length=50)),
                ('field_4', models.CharField(max_length=50)),
                ('field_5', models.CharField(max_length=50)),
                ('field_6', models.CharField(max_length=50)),
                ('field_7', models.CharField(max_length=50)),
                ('field_8', models.CharField(max_length=50)),
                ('field_9', models.CharField(max_length=50)),
                ('field_10', models.CharField(max_length=50)),
                ('field_11', models.CharField(max_length=50)),
                ('field_12', models.CharField(max_length=50)),
                ('field_13', models.CharField(max_length=50)),
                ('field_14', models.CharField(max_length=50)),
                ('field_15', models.CharField(max_length=50)),
                ('field_16', models.CharField(max_length=50)),
                ('field_17', models.CharField(max_length=50)),
                ('field_18', models.CharField(max_length=50)),
                ('field_19', models.CharField(max_length=50)),
                ('field_20', models.CharField(max_length=50)),
                ('issue_id', models.IntegerField(null=True)),
                ('exceptions_occured', models.CharField(max_length=500)),
                ('conversations', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'WhatsAppQueue',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CustomerLevelSummarised',
            fields=[
                ('CustomerInfoID', models.ForeignKey(db_column='CustomerInfoID', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='collection_followup.demographic')),
                ('ApplicantName', models.CharField(default='', max_length=100)),
                ('No_Of_Loans', models.IntegerField()),
                ('Pending_Installments', models.IntegerField()),
                ('total_outstanding', models.DecimalField(blank=True, decimal_places=4, max_digits=19, null=True)),
                ('total_pos', models.DecimalField(blank=True, decimal_places=4, max_digits=19, null=True)),
                ('DisbursementID', models.IntegerField()),
                ('DisbursementDate', models.DateTimeField(blank=True, null=True)),
                ('Max_User_DPD', models.IntegerField()),
                ('mobile_no', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('CustomerCode', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('CenterID', models.BigIntegerField()),
                ('UserID', models.BigIntegerField()),
                ('NON_ACTIVE_NON_WOFF', models.IntegerField()),
                ('Dropout_Inactive', models.IntegerField()),
            ],
            options={
                'db_table': 'Customer_level_summarised_final',
                'managed': False,
            },
        ),
    ]
