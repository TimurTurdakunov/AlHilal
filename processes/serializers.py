from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from processes.models import *
from processes.celery_app import send_request_ps_service_check


class DocumentIdentityDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentIdentityData
        fields = ['client_type', 'iin', 'full_name', 'dob', 'document_identity_id', 'country_residence']

    def create(self, validated_data):
        # validated_data['processes_clientform'] = self.context.get('ClientForm')
        data = DocumentIdentityData.objects.create(client_type=validated_data.get('client_type'),
                                                   iin=validated_data.get('iin'),
                                                   full_name=validated_data.get('full_name'),
                                                   dob=validated_data.get('dob'),
                                                   document_identity_id=validated_data.get('document_identity_id'),
                                                   country_residence=validated_data.get('country_residence'))
        return data

    def update(self, instance, validated_data):
        instance.client_type = validated_data.get('client_type')
        instance.iin = validated_data.get('iin')
        instance.full_name = validated_data.get('full_name')
        instance.dob = validated_data.get('dob')
        instance.document_identity_id = validated_data.get('document_identity_id')
        instance.country_residence = Country.objects.get(pk=validated_data.get('country_residence'))
        instance.expiry_date = validated_data.get('expiry_date')
        instance.issue_date = validated_data.get('issue_date')
        instance.issued_by = validated_data.get('issued_by')
        instance.save()
        return instance


class VisaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisaData
        fields = '__all__'

    def create(self, validated_data):
        data = VisaData.objects.create(border_crossing_type=validated_data.get('border_crossing_type'),
                                       visa_number=validated_data.get('visa_number'),
                                       visa_issue_date=validated_data.get('visa_issue_date'),
                                       visa_expiry_date=validated_data.get('visa_expiry_date'),
                                       migration_card_number=validated_data.get('migration_card_number'),
                                       migration_card_issue_date=validated_data.get('migration_card_issue_date'),
                                       migration_card_expiry_date=validated_data.get('migration_card_expiry_date'))
        return data

    def update(self, instance, validated_data):
        instance.border_crossing_type = validated_data.get('border_crossing_type')
        instance.visa_number = validated_data.get('visa_number')
        instance.visa_issue_date = validated_data.get('visa_issue_date')
        instance.visa_expiry_date = validated_data.get('visa_expiry_date')
        instance.migration_card_number = validated_data.get('migration_card_number')
        instance.migration_card_issue_date = validated_data.get('migration_card_issue_date')
        instance.migration_card_expiry_date = validated_data.get('migration_card_expiry_date')
        instance.save()
        return instance


class FatcaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FatcaData
        fields = '__all__'

    def create(self, validated_data):
        data = FatcaData.objects.create(**validated_data)
        return data

    def update(self, instance, validated_data):
        instance.born_in_usa = validated_data.get('born_in_usa')
        instance.born_in_us_com = validated_data.get('born_in_us_com')
        instance.us_passport = validated_data.get('us_passport')
        instance.us_passport_com = validated_data.get('us_passport_com')
        instance.greencard = validated_data.get('greencard')
        instance.green_card_com = validated_data.get('green_card_com')
        instance.us_address = validated_data.get('us_address')
        instance.us_address_com = validated_data.get('us_address_com')
        instance.care_of = validated_data.get('care_of')
        instance.care_of_com = validated_data.get('care_of_com')
        instance.hold_mail = validated_data.get('hold_mail')
        instance.hold_mail_com = validated_data.get('hold_mail_com')
        instance.us_phone = validated_data.get('us_phone')
        instance.us_phone_com = validated_data.get('us_phone_com')
        instance.pay_instruct = validated_data.get('pay_instruct')
        instance.pay_instruct_com = validated_data.get('pay_instruct_com')
        instance.attorney = validated_data.get('attorney')
        instance.attorney_com = validated_data.get('attorney_com')
        instance.residence_permit = validated_data.get('residence_permit')
        instance.us_id_type = validated_data.get('us_id_type')
        instance.us_id_number = validated_data.get('us_id_number')
        instance.save()
        return instance


class KatoClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = KatoClient
        fields = '__all__'

    def create(self, validated_data):
        data = KatoClient.objects.create(region_current=validated_data.get('region_current'),
                                         district_current=validated_data.get('district_current'),
                                         community_current=validated_data.get('community_current'),
                                         region_registration=validated_data.get('region_registration'),
                                         community_registration=validated_data.get('community_registration'),
                                         region_work=validated_data.get('region_work'),
                                         district_work=validated_data.get('district_work'),
                                         community_work=validated_data.get('community_work'))
        return data

    def update(self, instance, validated_data):
        if validated_data.get('region_current'):
            instance.region_current = KatoRegion.objects.get(pk=validated_data.get('region_current'))
        if validated_data.get('district_current'):
            instance.district_current = KatoDistrict.objects.get(pk=validated_data.get('district_current'))
        if validated_data.get('community_current'):
            instance.community_current = KatoCommunity.objects.get(pk=validated_data.get('community_current'))
        if validated_data.get('region_registration'):
            instance.region_registration = KatoRegion.objects.get(pk=validated_data.get('region_registration'))
        if validated_data.get('district_registration'):
            instance.district_registration = KatoDistrict.objects.get(pk=validated_data.get('district_registration'))
        if validated_data.get('community_registration'):
            instance.community_registration = KatoCommunity.objects.get(pk=validated_data.get('community_registration'))
        if validated_data.get('region_work'):
            instance.region_work = KatoRegion.objects.get(pk=validated_data.get('region_work'))
        if validated_data.get('district_work'):
            instance.district_work = KatoDistrict.objects.get(pk=validated_data.get('district_work'))
        if validated_data.get('community_work'):
            instance.community_work = KatoCommunity.objects.get(pk=validated_data.get('community_work'))
        instance.save()
        return instance


class WorkInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkInfo
        fields = '__all__'

    def create(self, validated_data):
        data = WorkInfo.objects.create(employer_name=validated_data.get('employer_name'),
                                       job_type=validated_data.get('job_type'),
                                       length_of_employment=validated_data.get('length_of_employment'),
                                       salary_min=validated_data.get('salary_min'),
                                       salary_max=validated_data.get('salary_max'),
                                       department=validated_data.get('department'),
                                       job_title=validated_data.get('job_title'),
                                       is_employee=validated_data.get('is_employee'),
                                       salary_currency=validated_data.get('salary_currency'))
        return data

    def update(self, instance, validated_data):
        instance.employer_name = validated_data.get('employer_name')
        instance.job_type = validated_data.get('job_type')
        instance.length_of_employment = validated_data.get('length_of_employment')
        instance.salary_min = validated_data.get('salary_min')
        instance.salary_max = validated_data.get('salary_max')
        instance.department = validated_data.get('department')
        instance.job_title = validated_data.get('job_title')
        instance.is_employee = validated_data.get('is_employee')
        instance.salary_currency = validated_data.get('salary_currency')
        instance.save()
        return instance


class ContactDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactData
        fields = '__all__'

    def create(self, validated_data):
        data = ContactData.objects.create(work_phone=validated_data.get('work_phone'),
                                          additional_phone=validated_data.get('additional_phone'),
                                          phone_number=validated_data.get('phone_number'),
                                          land_phone_number=validated_data.get('land_phone_number'),
                                          email=validated_data.get('email'),
                                          code_word=validated_data.get('code_word'))
        return data

    def update(self, instance, validated_data):
        instance.work_phone = validated_data.get('work_phone')
        instance.additional_phone = validated_data.get('additional_phone')
        instance.phone_number = validated_data.get('phone_number')
        instance.land_phone_number = validated_data.get('land_phone_number')
        instance.email = validated_data.get('email')
        instance.code_word = validated_data.get('code_word')
        instance.save()
        return instance


class ClientCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientCard
        fields = '__all__'

    def create(self, validated_data):
        data = ClientCard.objects.create(client=validated_data.get('client'),
                                         currency=validated_data.get('currency'),
                                         type=validated_data.get('type'),
                                         tariff_plan=validated_data.get('tariff_plan'))
        return data

    def update(self, instance, validated_data):
        instance.client = validated_data.get('client')
        instance.currency = validated_data.get('currency')
        instance.type = validated_data.get('type')
        instance.tariff_plan = validated_data.get('tariff_plan')
        instance.save()
        return instance


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    branch = BranchSerializer()

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'surname', 'middle_name', 'date_of_birth', 'is_active', 'date_joined',
                  'job_title', 'phone_number', 'iin', 'last_active_at', 'last_login', 'is_blocked', 'branch',
                  'user_permissions']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email')
        instance.date_of_birth = validated_data.get('date_of_birth')
        instance.username = validated_data.get('username')
        instance.first_name = validated_data.get('first_name')
        instance.surname = validated_data.get('surname')
        instance.middle_name = validated_data.get('middle_name')
        instance.job_title = validated_data.get('job_title')
        instance.branch = validated_data.get('branch')
        instance.phone_number = validated_data.get('phone_number')
        instance.save()
        return instance


class ClientFormSerializer(serializers.ModelSerializer):
    document_identity_data = DocumentIdentityDataSerializer()

    class Meta:
        model = ClientForm
        read_only_fields = ['maker', 'branch']
        fields = ['document_identity_data', 'id']

    def create(self, validated_data):
        maker = CustomUser.objects.get(pk=self.context.get('user_id'))
        client = ClientForm(maker=maker, branch=maker.branch)
        document_identity_data_serializer = DocumentIdentityDataSerializer(
            data=self.initial_data.get('document_identity_data'))

        if document_identity_data_serializer.is_valid():
            document_identity = document_identity_data_serializer.save()
            visa_data = VisaData.objects.create()
            kato_data = KatoClient.objects.create()
            fatca_data = FatcaData.objects.create()
            work_data = WorkInfo.objects.create()
            contact_data = ContactData.objects.create()
            client.visa = visa_data
            client.kato = kato_data
            client.document_identity_data = document_identity
            client.fatca = fatca_data
            client.work_info = work_data
            client.contact_data = contact_data
            client.save()
            ps_service_data = {'dob': document_identity.dob, 'iin': document_identity.iin,
                               'full_name': document_identity.full_name,
                               'document_identity_id': document_identity.document_identity_id,
                               'id': client.id, 'country_alpha2': document_identity.country_residence.alpha2
                               }
            send_request_ps_service_check.delay(**ps_service_data)
            return client
        else:
            return document_identity_data_serializer.errors

    def update(self, instance, validated_data):
        pass


class ClientFormDetailSerializer(serializers.ModelSerializer):
    document_identity_data = DocumentIdentityDataSerializer()
    #client_card = ClientCardSerializer()
    contact_data = ContactDataSerializer()
    work_info = WorkInfoSerializer()
    kato = KatoClientSerializer()
    fatca = FatcaDataSerializer()
    visa = VisaDataSerializer()

    class Meta:
        model = ClientForm
        fields = ['document_identity_data', 'contact_data', 'work_info', 'kato', 'fatca', 'visa']



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        # data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        user = CustomUserSerializer(self.user)
        data['user'] = user.data
        return data

    def get_token(self, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        return token
