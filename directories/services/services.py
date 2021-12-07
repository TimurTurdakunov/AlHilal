import xlrd
from directories.models import KatoRegion, KatoDistrict, KatoCommunity

path = "C:\\Users\\Timur\\Desktop\\21_12_2020\\katonew1.xls"
path_2 = "C:\\Users\\Timur\\Desktop\\21_12_2020\\katonew2.xls"


def counter(path):
    excel_workbook = xlrd.open_workbook_xls(path)
    excel_worksheet = excel_workbook.sheet_by_index(0)

    for y in range(1, excel_worksheet.nrows):
        if excel_worksheet.cell_value(y, 2) == '00':
            reg_name = excel_worksheet.cell_value(y, 7)
            reg_code = excel_worksheet.cell_value(y, 1)
            KatoRegion.objects.create(name=reg_name, code=reg_code)
        if excel_worksheet.cell_value(y, 4) == '000' and excel_worksheet.cell_value(y, 2) != '00':
            dis_name = excel_worksheet.cell_value(y, 7)
            dis_code = excel_worksheet.cell_value(y, 2)
            dis_obj = KatoDistrict.objects.create(name=dis_name, code=dis_code, region=KatoRegion.objects.get(code=reg_code, name=reg_name))
            print(excel_worksheet.cell_value(y, 7), dis_obj.id)
        if excel_worksheet.cell_value(y, 4) != '000':
            com_name = excel_worksheet.cell_value(y, 7)
            com_code = excel_worksheet.cell_value(y, 3)
            print(y, 'com_name', com_name, type(excel_worksheet.cell_value(y, 4)), type(dis_code), type(dis_name))
            KatoCommunity.objects.create(name=com_name, code=com_code, district=KatoDistrict.objects.get(id=dis_obj.id))



# counter(path)
# counter(path_2)