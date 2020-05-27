import csv
import json
import xlrd
from xml.etree import ElementTree as ET

def csv_print(file_name):
    csvfile = open(file_name, 'r')
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)

def json_print(file_name):
    json_data = open(file_name).read()
    data = json.loads(json_data)
    for key, value in data.items():
        if isinstance(value, list):
            print(key + ': ')
            for key_l, value_l in value[0].items():
                print('\t{}: {}'.format(key_l, value_l))
        elif isinstance(value, dict):
            print(key + ': ')
            for key_t, value_t in value.items():
                print('\t{}: {}'.format(key_t, value_t))
        else:
            print('{}: {}'.format(key,value))

def xml_print(file_name):
    tree = ET.parse(file_name)
    root = tree.getroot()
    NvSource = root.find('NvSource')

    all_data = []
    for product_NvInfo in NvSource:
        lookup_key = product_NvInfo.attrib.keys()
        record = {}
        if list(lookup_key)[0]== 'MODEM_NUMBER':
            rec_value = product_NvInfo.attrib['MODEM_NUMBER']
            if rec_value == '1':
                for product in product_NvInfo:
                    lookup_key_pro = product.attrib.keys()
                    print(lookup_key_pro)
                    if list(lookup_key_pro)[0] == 'product_id':
                        id_value = product.attrib['product_id']
                        if id_value == '0':
                            for nv in product:
                                lookup_key_nv = nv.attrib.keys()
                                if list(lookup_key_nv)[0] == 'id':
                                    rec_key = nv.attrib['id']
                                    rec_value = nv.text
                                record[rec_key] = rec_value
                all_data.append(record)
    print(all_data)

def excel_print(file_name, sheet_name):
    book = xlrd.open_workbook(file_name)
    sheet = book.sheet_by_name(sheet_name)
    for i in range(sheet.nrows):
        print(sheet.row_values(i))

#json_print("C:\\Users\\zach.zhang\\Desktop\\statistics-config.json")
#csv_print("C:\\Users\\zach.zhang\\Desktop\\_cache.csv")
#xml_print("C:\\Users\\zach.zhang\\Desktop\\0518_NV_New.xml")
#excel_print("C:\\Users\\zach.zhang\\Desktop\\1234.xlsx","Sheet1")