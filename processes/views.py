from django.http import Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from rest_framework import mixins
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.views import TokenObtainPairView
from processes.models import *
from processes.serializers import *
from processes.servisses.other_functions import validate_password, get_user_id_from_token
from django.contrib.auth.models import Permission
from processes.permissions import *
from rest_condition import And, Or, Not


class ClientFormView(APIView):

    permission_classes = [Or(And(IsActive, IsMaker, IsMethodPost), And(IsActive, IsOperationist), And(IsActive, IsAuthorizer))]

    def get(self, request, *args, **kwargs):
        permission_classes = [IsActive]
        user_id = get_user_id_from_token(request)
        queryset = ClientForm.objects.filter(maker=user_id)
        user = CustomUser.objects.get(pk=user_id)
        serializer = ClientFormSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        permission_classes = [IsActive, IsMaker]
        try:
            user_id = get_user_id_from_token(request)
            serializer = ClientFormSerializer(data=request.data, context={'user_id': user_id})

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        except ValidationError as v:
            print("validation error", v)


class ClientFormDetailView(APIView, mixins.RetrieveModelMixin):

    def get_object(self, pk):
        try:
            return ClientForm.objects.get(pk=pk)
        except ClientForm.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        client = self.get_object(pk)
        serializer = ClientFormDetailSerializer(client)
        return Response(serializer.data)

    def put(self, request, pk):
        client = self.get_object(pk)
        if self.request.data.get('document_identity_data'):
            document_identity_data_serializer = DocumentIdentityDataSerializer(
                data=self.request.data.get('document_identity_data'))
            if document_identity_data_serializer.is_valid(raise_exception=True):
                document_identity_data_serializer.update(instance=client.document_identity_data,
                                                         validated_data=self.request.data.get('document_identity_data'))
            else:
                return Response(document_identity_data_serializer.errors)
        if self.request.data.get('visa_data'):
            visa_data_serializer = VisaDataSerializer(
                data=self.request.data.get('visa_data'))
            if visa_data_serializer.is_valid(raise_exception=True):
                visa_data_serializer.update(instance=client.visa,
                                            validated_data=self.request.data.get('visa_data'))
            else:
                return Response(visa_data_serializer.errors)
        if self.request.data.get('fatca_data'):
            fatca_data_serializer = FatcaDataSerializer(
                data=self.request.data.get('fatca_data'))
            if fatca_data_serializer.is_valid(raise_exception=True):
                fatca_data_serializer.update(instance=client.fatca,
                                             validated_data=self.request.data.get('fatca_data'))
            else:
                return Response(fatca_data_serializer.errors)
        if self.request.data.get('kato_data'):
            kato_client_serializer = KatoClientSerializer(
                data=self.request.data.get('kato_data')
            )
            if kato_client_serializer.is_valid(raise_exception=True):
                kato_client_serializer.update(instance=client.kato,
                                              validated_data=self.request.data.get('kato_data'))
            else:
                return Response(kato_client_serializer.errors)
        if self.request.data.get('work_data'):
            work_info_serializer = WorkInfoSerializer(
                data=self.request.data.get('work_data')
            )
            if work_info_serializer.is_valid(raise_exception=True):
                work_info_serializer.update(instance=client.work_info,
                                            validated_data=self.request.data.get('work_data'))
            else:
                return Response(work_info_serializer.errors)
        if self.request.data.get('contact_data'):
            contact_data_serializer = ContactDataSerializer(
                data=self.request.data.get('contact_data')
            )
            if contact_data_serializer.is_valid(raise_exception=True):
                contact_data_serializer.update(instance=client.contact_data,
                                               validated_data=self.request.data.get('contact_data'))
            else:
                return Response(contact_data_serializer.errors)
        return Response({'success': 'данные обновленны'})


class CustomUserView(APIView):

    def get(self, request, *args, **kwargs):
        queryset = CustomUser.objects.all()
        serializer = CustomUserSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid()
        serializer.update(CustomUser.objects.get(pk=kwargs['pk']), request.data)
        return Response(serializer.data)


def activate_account_view(request, user_id):
    if request.method == 'GET':
        return render(request, 'activate_acc.html')

    elif request.method == 'POST':
        otp = request.POST.get('otp')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')
        validation_error = validate_password(password, password_confirmation)
        if not validation_error:
            user = CustomUser.objects.get(id=user_id)
            if user is None:
                return render(request, 'activate_acc.html', {'error': 'такого пользователя не существует,'
                                                                      ' проверьте ссылку на почте'})
            if user.registration_otp != otp:
                return render(request, 'activate_acc.html', {'error': 'проверочный код не совпадает'})
            user.is_active = True
            user.password_created_at = datetime.datetime.utcnow()
            user.registration_otp = None
            user.set_password(password)
            user.save()
            # create notification
            return render(request, 'activate_acc.html', {'error': 'аккаунт был активирован'})
        else:
            return render(request, 'activate_acc.html', {'error': validation_error})


def forgot_password(request, user_id):
    pass


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
