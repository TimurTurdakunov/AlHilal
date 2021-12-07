import datetime
import random
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from directories.models import *
from processes.servisses.mails import send_activate_account, send_change_password


class CustomUserManager(BaseUserManager):
    """
    custom user model
    """

    def create_user(self, username, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        possible_characters = "abcdefghijklmnopqrstuvwxyz1234567890"
        user = self.model(
            username=username,
            **extra_fields
        )
        #corporate email check
        user.set_password(None)
        user.save(using=self._db)
        user.set_registration_otp()
        send_activate_account(user.id, user.email, user.username, user.registration_otp)

        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.model(username=username, first_name='admin', surname='admin',
                          middle_name='admin', is_superuser=True, email='boris.ignatov.99@gmail.com',
                          is_active=True, is_staff=True)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    password_created_at = models.DateTimeField(auto_now_add=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    branch = models.ForeignKey('Branch', models.CASCADE, null=True)
    iin = models.CharField(max_length=12, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    last_active_at = models.DateTimeField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    last_login_ip = models.CharField(max_length=30, null=True, blank=True)
    is_blocked = models.BooleanField(default=False)
    old_passwords = models.OneToOneField('UsersOldPasswords', models.DO_NOTHING, null=True, blank=True)
    registration_otp = models.CharField(max_length=4, null=True, blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return '{0} {1} {2}'.format(self.first_name, self.surname, self.middle_name)

    def set_registration_otp(self):
        otp = ''
        for i in range(4):
            otp += str(int(random.randint(0, 9)))
        self.registration_otp = otp
        self.save()


#нужно хранить 7 паролей
class UsersOldPasswords(models.Model):

    password1 = models.CharField(max_length=255, null=True)
    password2 = models.CharField(max_length=255, null=True)
    password3 = models.CharField(max_length=255, null=True)
    password4 = models.CharField(max_length=255, null=True)
    password5 = models.CharField(max_length=255, null=True)
    password6 = models.CharField(max_length=255, null=True)


class Branch(models.Model):

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    #director = models.ForeignKey('CustomUser', models.CASCADE)
    director = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Process(models.Model):

    name = models.CharField(max_length=255)


#данные для заведения нового клиента
class ClientForm(models.Model):

    cif = models.CharField(max_length=7, null=True)
    maker = models.ForeignKey('CustomUser', models.DO_NOTHING, related_name='maker')
    branch = models.ForeignKey('Branch', models.DO_NOTHING)
    authorizer = models.ForeignKey('CustomUser', models.DO_NOTHING, related_name='authorizer', null=True)
    operationist = models.ForeignKey('CustomUser', models.DO_NOTHING, related_name='operationist', null=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField(auto_now_add=True)
    document_identity_data = models.OneToOneField('DocumentIdentityData', models.CASCADE)
    client_checks = models.OneToOneField('ClientChecks', models.CASCADE, null=True)
    first_name_english = models.CharField(max_length=10, null=True)
    surname_english = models.CharField(max_length=15, null=True)
    sex = models.CharField(max_length=30, null=True)
    citizenship = models.ForeignKey('directories.Country', models.DO_NOTHING, null=True)
    tax_registr_id = models.CharField(max_length=50, null=True)
    task_status = models.IntegerField(default=0)
    visa = models.OneToOneField('VisaData', models.CASCADE, null=True)
    kato = models.OneToOneField('KatoClient', models.CASCADE, null=True)
    fatca = models.OneToOneField('FatcaData', models.CASCADE, null=True)
    work_info = models.OneToOneField('WorkInfo', models.CASCADE, null=True)
    contact_data = models.OneToOneField('ContactData', models.CASCADE, null=True)


#первоначальные данные клиента
class DocumentIdentityData(models.Model):

    client_type = models.CharField(max_length=50)
    iin = models.CharField(max_length=12)
    full_name = models.CharField(max_length=100)
    dob = models.DateField()
    document_identity_id = models.CharField(max_length=50)
    country_residence = models.ForeignKey('directories.Country', on_delete=models.DO_NOTHING)
    issue_date = models.CharField(max_length=50, null=True, blank=True)
    expiry_date = models.CharField(max_length=50, null=True, blank=True)
    issued_by = models.CharField(max_length=50, null=True, blank=True)


#провери по спискам, наличию в т24 и пс
class ClientChecks(models.Model):

    is_ps_answered = models.BooleanField(default=False)#ответил ли комплаенс в пс по worldCheck
    is_on_complience_ps = models.BooleanField(null=True)#клеиент ушел на проверку в комплаенс
    ps_complience_answer = models.BooleanField(null=True)#True если у клиента настоящее совпадение
    ps_complience_answer_comment = models.TextField(null=True)#Комментарий комплаенс(не прилетает)
    in_list_IP = models.BooleanField(null=True)#в списке ип
    IP_comment = models.TextField(null=True)  #
    in_list_bezd = models.BooleanField(null=True)#в списке бездействующих ип
    bezd_comment = models.TextField(null=True)  #
    in_list_banks = models.BooleanField(null=True)#сотрудник банка
    banks_comment = models.TextField(null=True)  #
    in_list_PEP = models.BooleanField(null=True)#является ипдл(PEP)
    PEP_comment = models.TextField(null=True) #
    in_list_WorldCheck = models.BooleanField(null=True)#террорист
    worldcheck_comment = models.TextField(null=True)#текст проверки по спискам террористов
    tax_debt = models.BooleanField(null=True)#есть задолжность
    tax_debt_comment = models.TextField(null=True)# текст задолжности
    t24_checked = models.BooleanField(null=True)# True если клиент уже создан в т24
    ps_checked = models.BooleanField(null=True)#True если клиент уже создан в ПС
    ps_response_status = models.IntegerField(null=True)#статус по проверке по спискам пс, 1 - отпарвлен на проверку в комплаенс, 2 - запрет создания


class VisaData(models.Model):

    border_crossing_type = models.BooleanField(null=True)
    visa_number = models.CharField(max_length=255, null=True)
    visa_issue_date = models.DateField(null=True)
    visa_expiry_date = models.DateField(null=True)
    migration_card_number = models.CharField(max_length=255, null=True)
    migration_card_issue_date = models.DateField(null=True)
    migration_card_expiry_date = models.DateField(null=True)


class FatcaData(models.Model):

    born_in_usa = models.BooleanField(null=True)
    born_in_us_com = models.CharField(max_length=255, null=True)
    us_passport = models.BooleanField(null=True)
    us_passport_com = models.CharField(max_length=255, null=True)
    greencard = models.BooleanField(null=True)
    green_card_com = models.CharField(max_length=255, null=True)
    us_address = models.BooleanField(null=True)
    us_address_com = models.CharField(max_length=255, null=True)
    care_of = models.BooleanField(null=True)
    care_of_com = models.CharField(max_length=255, null=True)
    hold_mail = models.BooleanField(null=True)
    hold_mail_com = models.CharField(max_length=255, null=True)
    us_phone = models.BooleanField(null=True)
    us_phone_com = models.CharField(max_length=255, null=True)
    pay_instruct = models.BooleanField(null=True)
    pay_instruct_com = models.CharField(max_length=255, null=True)
    attorney = models.BooleanField(null=True)
    attorney_com = models.CharField(max_length=255, null=True)
    residence_permit = models.BooleanField(null=True)
    us_id_type = models.CharField(max_length=255, null=True)
    us_id_number = models.CharField(max_length=255, null=True)


class KatoClient(models.Model):

    region_current = models.ForeignKey('directories.KatoRegion', models.DO_NOTHING, null=True, related_name='region_current')
    district_current = models.ForeignKey('directories.KatoDistrict', models.DO_NOTHING, null=True,related_name='district_current')
    community_current = models.ForeignKey('directories.KatoCommunity', models.DO_NOTHING, null=True, related_name='community_current')
    region_registration = models.ForeignKey('directories.KatoRegion', models.DO_NOTHING, null=True, related_name='region_registration')
    district_registration = models.ForeignKey('directories.KatoDistrict', models.DO_NOTHING, null=True, related_name='district_registration')
    community_registration = models.ForeignKey('directories.KatoCommunity', models.DO_NOTHING, null=True, related_name='community_registration')
    region_work = models.ForeignKey('directories.KatoRegion', models.DO_NOTHING, null=True, related_name='region_work')
    district_work = models.ForeignKey('directories.KatoDistrict', models.DO_NOTHING, null=True, related_name='district_work')
    community_work = models.ForeignKey('directories.KatoCommunity', models.DO_NOTHING, null=True, related_name='community_work')


class WorkInfo(models.Model):

    employer_name = models.CharField(max_length=255, null=True, blank=True)
    job_type = models.CharField(max_length=255,null=True, blank=True)
    length_of_employment = models.CharField(max_length=255, null=True, blank=True)
    salary_min = models.CharField(max_length=255, null=True, blank=True)
    salary_max = models.CharField(max_length=255, null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)
    job_title = models.CharField(max_length=255, null=True, blank=True)
    is_employee = models.BooleanField(default=False, null=True, blank=True)
    salary_currency = models.CharField(max_length=255, null=True, blank=True)


class ContactData(models.Model):

    work_phone = models.CharField(max_length=255, null=True)
    additional_phone = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    land_phone_number = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    code_word = models.CharField(max_length=255, null=True, blank=True)


class ClientCard(models.Model):

    client = models.ForeignKey('ClientForm', models.CASCADE)
    currency = models.CharField(max_length=255)
    type = models.ForeignKey('directories.CardType', models.DO_NOTHING)
    tariff_plan = models.ForeignKey('directories.TariffPlan', models.DO_NOTHING)


class OTP(models.Model):

    client = models.OneToOneField('ClientForm', models.CASCADE)
    code = models.CharField(max_length=10)
    count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(datetime.datetime.now() + datetime.timedelta(minutes=5))


class AuthorizerComment(models.Model):

    client = models.ForeignKey('ClientForm', models.CASCADE)
    text = models.TextField(blank=True)
    employee = models.ForeignKey('CustomUser', models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):

    title = models.CharField(max_length=255)
    body = models.TextField()
