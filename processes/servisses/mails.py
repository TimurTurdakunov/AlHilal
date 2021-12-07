from django.conf import settings
from processes.celery_app import send_mail
from rest_framework.response import Response


def send_activate_account(id, email, login, otp):
    text = f"Добро пожаловать на BPMS Al Hilal. "\
           f"Пожалуйста перейдите по ссылке, чтобы подтвердить email {settings.SERVER_IP}/activate_account/{id} " \
           f"ваш логин: {login}. Код для доступа - {otp}"
    send_mail.delay('Активация аккаунта в БПМ', text, email)
    return True


def send_change_password(id, email, login, otp):
    text = "Восстановление пароля на BPMS Al Hilal \n Пожалуйста перейдите по ссылке, чтобы изменить email " +\
    settings.SERVER_IP + '/change_password/' + str(id) + ' \n ваш логин: '+ login + ' Одноразовый пароль: ' + str(otp)
    send_mail.delay('Изменение Пароля в БПМ', text, email)
    return Response({'success': 'письмо отправлено'}, 200)

