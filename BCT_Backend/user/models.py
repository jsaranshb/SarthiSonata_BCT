from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import date, datetime

# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email")
        if not username:
            raise ValueError("Users must have username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.deactivated = False
        user.save(using=self._db)
        return user


class Mst_UserTbl(AbstractBaseUser):
    UserID = models.IntegerField(primary_key=True)  # max length was 37
    EmpID = models.CharField(max_length=10)  # max length was 7
    DesignationID = (
        models.PositiveSmallIntegerField()
    )  # min: 0, max: 1104, mean: 50.837163814180926
    UserName = models.CharField(max_length=50)  # max length was 32
    UserCode = models.CharField(unique=True, max_length=20)  # max length was 9
    # Password = models.CharField(max_length=50)  # max length was 34
    ContactNo = models.CharField(
        max_length=20
    )  # max length was 14; (!) contains 192 Nones (2.35%)
    Email = models.EmailField(
        max_length=150, unique=True, null=True
    )  # max length was 40; (!) contains 382 Nones (4.67%)
    Hoid = (
        models.PositiveSmallIntegerField()
    )  # min: 0, max: 3, mean: 0.9971882640586797
    DivisionID = models.CharField(
        max_length=10
    )  # (!) contains 191 Nones (2.33%); min: 0.0, max: 2200.0, mean: 1172.6517711853799
    RegionID = models.CharField(
        max_length=10
    )  # max length was 4; (!) contains 201 Nones (2.46%)
    HubID = models.CharField(
        max_length=20
    )  # max length was 8; (!) contains 255 Nones (3.12%)
    BranchID = models.CharField(
        max_length=50
    )  # max length was 36; (!) contains 261 Nones (3.19%)
    BranchJoinDate = models.CharField(max_length=30)  # max length was 19
    BranchExitDate = models.CharField(
        max_length=30
    )  # max length was 19; (!) contains 7223 Nones (88.30%)
    Comment = models.CharField(
        max_length=60
    )  # max length was 45; (!) contains 7608 Nones (93.01%)
    IsActive = models.CharField(
        max_length=30
    )  # max length was 19; (!) contains 1 Nones (0.01%)
    CreatedBy = models.FloatField(
        null=True
    )  # (!) contains 1 Nones (0.01%); min: 1.0, max: 25265.0, mean: 6368.6169458368995
    CreatedDate = models.CharField(
        max_length=40
    )  # max length was 29; (!) contains 1 Nones (0.01%)
    UpdatedBy = models.CharField(
        max_length=10
    )  # max length was 5; (!) contains 1115 Nones (13.63%)
    UpdatedDate = models.CharField(
        max_length=40
    )  # max length was 29; (!) contains 157 Nones (1.92%)
    Locked = models.CharField(
        max_length=10
    )  # max length was 5; (!) contains 1 Nones (0.01%)
    LastPasswordDate = models.CharField(
        max_length=40
    )  # max length was 29; (!) contains 2 Nones (0.02%)
    BUType = models.FloatField(
        null=True
    )  # (!) contains 2 Nones (0.02%); min: 0.0, max: 5.0, mean: 3.9191733920273903
    Buid = models.FloatField(
        null=True
    )  # (!) contains 2 Nones (0.02%); min: 0.0, max: 2210.0, mean: 742.616776718024
    IsLoggedin = models.CharField(
        max_length=10
    )  # max length was 5; (!) contains 446 Nones (5.45%)
    DeviceNo = models.CharField(
        max_length=80
    )  # max length was 55; (!) contains 661 Nones (8.08%)
    Session_Token_Id = models.CharField(
        max_length=50
    )  # max length was 36; (!) contains 4401 Nones (53.80%)
    LoginDevice = models.CharField(
        max_length=50
    )  # max length was 3; (!) contains 4381 Nones (53.56%)
    New = models.FloatField(
        null=True
    )  # (!) contains 7875 Nones (96.27%); min: 1.0, max: 5.0, mean: 3.9901639344262296
    NewBranchId = models.FloatField(
        null=True
    )  # (!) contains 5547 Nones (67.81%); min: 2.0, max: 2210.0, mean: 558.7132548423851
    EmpDOB = models.CharField(
        max_length=30
    )  # max length was 19; (!) contains 1428 Nones (17.46%)
    GLAccountId = models.FloatField(
        null=True
    )  # (!) contains 5483 Nones (67.03%); min: 223.0, max: 233.0, mean: 232.9962921764924
    AccountId = models.FloatField(
        null=True
    )  # (!) contains 5483 Nones (67.03%); min: 969961.0, max: 972664.0, mean: 971309.9540229886
    IsDropout = models.CharField(
        max_length=10
    )  # max length was 5; (!) contains 2 Nones (0.02%)
    DropoutDate = models.CharField(
        max_length=40
    )  # max length was 29; (!) contains 4103 Nones (50.16%)
    IsHelpDeskStaff = models.CharField(
        max_length=10
    )  # max length was 5; (!) contains 2 Nones (0.02%)
    registration_authenticated = models.BooleanField(default=True)
    date_joined = models.DateTimeField(
        verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    deactivated = models.BooleanField(default=False)

    USERNAME_FIELD = "UserCode"
    REQUIRED_FIELDS = []

    objects = MyAccountManager()

    class Meta:
        db_table = 'accounts_Mst_UserTbl'
        managed = False  # Set this to False if you don’t want Django to manage migrations for this table

class calling_number_list(models.Model):
    UserID = models.OneToOneField(Mst_UserTbl, primary_key=True,
                                  on_delete=models.CASCADE, related_name='calling_obj', db_column="UserID")
    CallingNumber = models.CharField(max_length=20)
    Is_active = models.BooleanField(default=True)
    registered_on = models.DateTimeField(auto_now_add=True)
    agent_id = models.CharField(max_length=50)

    class Meta:
        db_table = 'accounts_calling_number_list'
        managed = False 

class task_details(models.Model):
    task_id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=100, blank=True, null=True)
    task_description = models.CharField(max_length=1000, blank=True, null=True)
    created_by = models.ForeignKey(
        Mst_UserTbl, on_delete=models.CASCADE, db_column="created_by", related_name="task_created_by")
    assigned_to = models.ForeignKey(
        Mst_UserTbl, on_delete=models.CASCADE, db_column="assigned_to", related_name="task_assigned_to")
    status = models.CharField(max_length=100, default='Pending')
    category = models.CharField(max_length=100)
    assigned_role = models.CharField(max_length=100)
    complete_status = models.BooleanField(default=False)
    created_on = models.DateField(auto_now_add=True)
    deadline_date = models.DateField(blank=True, null=True)
    completion_date = models.DateField(blank=True, null=True)
    review = models.CharField(max_length=1000, blank=True, null=True)
    feedback = models.CharField(max_length=1000, blank=True, null=True)
    priority = models.IntegerField(null=True, blank=True, default=1,
                                   choices=((1,  'Immediate'),
                                            (2, 'High'),
                                            (3, 'Medium'),
                                            (4, 'Low')
                                            ))
    deadline_track = models.JSONField()
    review_track = models.JSONField()
    feedback_track = models.JSONField()
    t_info = models.CharField(max_length=50, blank=True, null=True)
    T_Info_ID = models.IntegerField(blank=True, null=True)
    # task_source=models.CharField(max_length=255, blank=True, null=True)
    bulk_task_status = models.IntegerField(choices=((0,'REGULAR TASK'),
                                                    (1,'RELATIVE BULK TASK'),
                                                    (2,"NOT RELATIVE BULK TASK")), blank=True, null=True, default=0)
    bulk_task_whatsapp_queue = models.BooleanField(default=False)




    @property
    def deadline_days(self):
        today = date.today()
        result = self.deadline_date - today
        return int(result.days)
    
    class Meta:
        db_table = 'accounts_task_details'
        managed = False 

class calling_number_list(models.Model):
    UserID = models.OneToOneField(Mst_UserTbl, primary_key=True,
                                  on_delete=models.CASCADE, related_name='calling_obj', db_column="UserID")
    CallingNumber = models.CharField(max_length=20)
    Is_active = models.BooleanField(default=True)
    registered_on = models.DateTimeField(auto_now_add=True)
    agent_id = models.CharField(max_length=50)

    class Meta:
        db_table = 'accounts_calling_number_list'
        managed = False 