from __future__ import absolute_import
import os
import requests
import datetime
from celery import Celery
from smtplib import SMTP, SMTPException, SMTP_SSL
from email.message import EmailMessage
from lxml import etree
from urllib3.exceptions import NewConnectionError
from processes.servisses.services import parse_ps_response
from processes.servisses.other_functions import request_body_ps_service
from django.conf import settings
from celery import shared_task



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BPM.settings')
app = Celery('mainCelery')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@shared_task
def send_mail(title, text, email, multiple=False):
    try:
        if settings.IS_ENV_PROD:
            bpm_email = 'RPARobot@ALHILALBANK.KZ'
            bpm_email_password = 'IamRobot'
            smtp_server = 'ala-server05.alhilalbank.ae'
            smtp_port = 25
        else:
            bpm_email = 'boris.ignatov.99@gmail.com'
            bpm_email_password = 'Aa33351115Bia'
            smtp_server = 'smtp.gmail.com'
            smtp_port = 465
        msg = EmailMessage()
        msg['Subject'] = title
        msg['From'] = bpm_email
        if multiple:
            msg['To'] = ", ".join(email)
        else:
            msg['To'] = email
        msg.set_content(text)
        smtpObj = SMTP(smtp_server)
        if not settings.IS_ENV_PROD:
            smtpObj = SMTP_SSL(smtp_server, smtp_port)
            smtpObj.login(bpm_email, bpm_email_password)
        smtpObj.send_message(msg)
        smtpObj.quit()
        return True
    except SMTPException as e:
        print(e)


@shared_task
def send_request_ps_service_check(**kwargs):
    from processes.models import ClientChecks, ClientForm
    data = request_body_ps_service.format(id=kwargs['id'], full_name=kwargs['full_name'],
                                          dob=datetime.datetime.strptime(kwargs['dob'].split('T')[0], '%Y-%m-%d'),
                                          iin=kwargs['iin'], country_alpha2=kwargs['country_alpha2'],
                                          document_identity_id=kwargs['document_identity_id'])
    try:
        if settings.IS_ENV_PROD:
            response = requests.post(settings.PS_SERVICE_URL,
                                     data=data.encode('utf-8'),
                                     headers={'content-type': 'application/soap+xml; charset=utf-8'},
                                     verify=False)
        else:
            response = requests.post(settings.PS_SERVICE_URL,
                                     data=data.encode('utf-8'),
                                     headers={'content-type': 'application/soap+xml; charset=utf-8'})

        parsed_data = parse_ps_response(response, kwargs['iin'])
        if parsed_data:
            client = ClientForm.objects.get(pk=kwargs['id'])
            client_checks = ClientChecks.objects.create(**parsed_data)
            client.client_checks = client_checks
            client.save()
            return True

        else:
            return 'Parsing error'

    except ConnectionError as e:
        print(e)
        #create_notification
        return f'ConnectionError - {str(e)}'

    except NewConnectionError as e:
        print('New')
        #create_notification
        return f'Exception - {str(e)}'

    except requests.exceptions.ConnectionError as e:
        print(e)
        return f'Ошибка - Ошибка подключения'
