import openpyxl
from funcions import fill_data_table, define_doc_type, fill_data_table_m11


def print_table(table, flag=True):
    if not flag:
        return
    for i in table:
        print(i)


fmy76 = "ФМУ-76"
m11 = "М-11"


def neuro_module():
    pass


def m11_(sheet):
    try:
        table, errors = fill_data_table_m11(sheet=sheet)
        return errors
    except Exception as e:
        print('[ERROR]', e)
        e = 'ошибка обработки таблицы. аварийное завершение.'
        print(e)
        return [e]


def fmy76_(sheet):
    try:
        table, errors = fill_data_table(sheet=sheet)
        # print_table(table, True)
        return errors
    except Exception as e:
        print('[ERROR]', e)
        e = 'ошибка обработки таблицы. аварийное завершение.'
        print(e)
        return [e]


def error_parser(file_path):
    wb = openpyxl.load_workbook(file_path)
    sheet = wb['Page 1']
    doc_type = define_doc_type(sheet)
    if doc_type == "":
        e = 'Тип документа не определен'
        print(e)
        return {'file_detect': False, 'filetype': e, 'errors': [e]}

    if doc_type == "error":
        e = 'Ошибка определения типа документа'
        print(e)
        return {'file_detect': False, 'filetype': e, 'errors': [e]}

    if doc_type == fmy76:
        print(f'Тип документа: {fmy76}')
        response = fmy76_(sheet)
        return {'file_detect': True, 'filetype': fmy76, 'errors': response}

    if doc_type == m11:
        print(f'Тип документа: {m11}')
        response = m11_(sheet)
        return {'file_detect': True, 'filetype': m11, 'errors': response}



