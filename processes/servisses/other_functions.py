from rest_framework_simplejwt.backends import TokenBackend

request_body_ps_service = '<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:p="http://p-s.kz/">\
                            <soap:Header/>\
                            <soap:Body>\
                            <p:CheckClientCard>\
                                <!--Optional:-->\
                                <p:request>\
                                    <p:SYSTEMID>4</p:SYSTEMID>\
                                    <!--Optional:-->\
                                    <p:UID>{id}BPM</p:UID>\
                                    <!--Optional:-->\
                                    <p:USERNAME>ADMIN</p:USERNAME>\
                                    <!--Optional:-->\
                                    <p:PARTICIPANTS>\
                                        <!--Zero or more repetitions:-->\
                                        <p:Person>\
                                            <p:ORDERNUMBER>1</p:ORDERNUMBER>\
                                            <p:FULL_NAME>{full_name}</p:FULL_NAME>\
                                            <p:BIRTH_DATE>{dob} 00:00:00</p:BIRTH_DATE>\
                                            <p:SUB_COUNTRY>{country_alpha2}</p:SUB_COUNTRY>\
                                            <p:CLIENT_ID>{iin}</p:CLIENT_ID>\
                                            <p:DOC_NUMBER>{document_identity_id}</p:DOC_NUMBER>\
                                            <p:CLIENT_TYPE>2</p:CLIENT_TYPE>\
                                            <p:BANK_CLIENT>1</p:BANK_CLIENT>\
                                            <p:PERSON_ROLE>1</p:PERSON_ROLE>\
                                        </p:Person>\
                                    </p:PARTICIPANTS>\
                                </p:request>\
                            </p:CheckClientCard>\
                            </soap:Body>\
                            </soap:Envelope>'


def validate_password(password, password_confirmation):
    if password == password_confirmation:
        if len(password) >= 8:
            if any(x.isupper() for x in password):
                if any(x.islower() for x in password):
                    if any(x.isdigit() for x in password):
                        if len(password) <= 30:
                            return False
                        else:
                            return 'максимальная длина пароля - 30 символов'
                    else:
                        return 'пароль должен содержать минимум 1 цифровое значение'
                else:
                    return 'пароль должен содержать минимум 1 строчный символ'
            else:
                return 'пароль должен содержать минимум 1 заглавную букву'
        else:
            return 'пароль не может быть короче 8 символов'
    else:
        return 'Пароли не совпадают'


def get_user_id_from_token(request):
    token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
    valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
    user_id = valid_data['user_id']
    return user_id
