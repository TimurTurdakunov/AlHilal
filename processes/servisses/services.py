import pyodbc as pyodbc
from lxml import etree
from django.conf import settings


def check_is_client_ip(iin):

    try:
        drivers = [item for item in pyodbc.drivers()]
        driver = drivers[-1]
        ip_conn = pyodbc.connect(f'DRIVER={{{driver}}};SERVER={settings.IP_DATABASE_IP};PORT=1433;DATABASE=\
                                 {settings.IP_DATABASE_NAME};UID={settings.IP_DATABASE_USERNAME};PWD={settings.IP_DATABASE_PASSWORD}')

        cursor = ip_conn.cursor()
        cursor.execute(f'SELECT CorporateName, Inactive FROM IDN WHERE EntrepreneurTypeFK = 32 AND BIN = {iin};')
        try:
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(row)
                    if not rows[0][0]:
                        ip_conn.close()
                        return ['есть в списке ИП', rows[0][1]]
                    ip_conn.close()
                    return [rows[0][0], rows[0][1]]
            else:
                ip_conn.close()
                return False
        except TypeError as e:
            print(e)
            ip_conn.close()
            return False
    except Exception as e:
        print(e)
        return False
        #log error


def parse_ps_response(response, iin):
    try:
        tree = etree.fromstring(response.content)
    except Exception as e:
        print(e)
        return False
    in_list_WorldCheck = False
    in_list_PEP = False
    in_list_banks = False
    in_list_bezd = False
    in_list_IP = False
    tax_debt = False
    worldcheck_comment = ''
    PEP_comment = None
    banks_comment = None
    bezd_comment = None
    tax_debt_comment = None
    IP_comment = None

    ps_response_status = 0
    '''ip_resp = check_is_client_ip(iin)
    if ip_resp:
        in_list_IP = True
        IP_comment = ip_resp[0]
        if ip_resp[1]:
            in_list_bezd = True
            bezd_comment = 'В списке бездействующих ип'''

    for i in tree.iter():
        if i.tag.split('}')[-1] == 'STATUS':
            ps_response_status = int(i.text)

        if i.tag.split('}')[-1] == 'COMMENT':
            try:
                if float(i.text.split(':')[1].split()[0]) != 0 and float(i.text.split(':')[2].split()[0]) != 0:
                    print(i)
                    tax_debt = True
            except ValueError as e:
                print(e)
                print(i)
                tax_debt = False
            tax_debt_comment = i.text

        if i.tag.split('}')[-1] == 'RESULT':

            source = ''
            status = 0
            info = ''

            for j in i:
                if j.tag.split('}')[-1] == 'STATUS':
                    try:
                        status = int(j.text)
                    except Exception as e:
                        print(e)
                        pass
                if j.tag.split('}')[-1] == 'ADDINFO':
                    info = j.text
                if j.tag.split('}')[-1] == 'SOURCE':
                    source_description = j.text
                    print(source_description, ' --- source description')

            if status == 1:
                try:
                    source = info.split('Справочник - ')[1].split()[0]
                    print(source, '--- source')

                except Exception as e:
                    print(e, '----source exception')

                print(status, '--- status')
                print(info, '--- info')
                print(tax_debt_comment, '--- tax_debt_comment')

                if source == 'DICT_WORLD_CHECK' or source.split('_')[0] == 'TERRORISTS':
                    in_list_WorldCheck = True
                    worldcheck_comment += info.split('\n')[2] + '\n' + info.split('\n')[4] + '\n'
                elif source == 'EXTERNAL_BANK_BLACK_LIST' or source == 'BANK_BLACK_LIST':
                    if source_description == 'Черный список банка':
                        in_list_WorldCheck = True
                        worldcheck_comment += info.split('\n')[2] + '\n' + info.split('\n')[4] + '\n'
                    elif source_description == 'Список связанных лиц банка':
                        in_list_banks = True
                        banks_comment = info
                elif source_description == 'Список ИПДЛ':
                    in_list_PEP = True
                    PEP_comment = info
                elif source_description == 'Черный список банка':
                    if info.split('\n')[0].split()[-1] == 'ИИН/БИН.':
                        in_list_WorldCheck = True
                        worldcheck_comment += info.split('\n')[1] + '\n'

    return {'in_list_WorldCheck': in_list_WorldCheck, 'worldcheck_comment': worldcheck_comment,
            'PEP_comment': PEP_comment, 'in_list_PEP': in_list_PEP,
            'banks_comment': banks_comment, 'in_list_banks': in_list_banks,
            'in_list_bezd': in_list_bezd, 'bezd_comment': bezd_comment,
            'ps_response_status': ps_response_status, 'tax_debt': tax_debt,
            'tax_debt_comment': tax_debt_comment, 'in_list_IP': in_list_IP, 'IP_comment': IP_comment}
