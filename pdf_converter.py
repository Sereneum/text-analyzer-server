import pdftables_api
import hashlib
import os
import random
c = pdftables_api.Client('92tnoxxx3riq')
t_file_name = 'ФМУ76_1_21.08.2023.pdf'

outputs = 'outputs/'


def get_hash(f_name):
    def create_hash(s):
        hash_object = hashlib.sha256()
        hash_object.update(s.encode('utf-8'))
        return hash_object.hexdigest()

    name = f_name
    size = 10
    while True:
        h = create_hash(name)
        if len(h) < size:
            name += str(random.randint(0, 10000))
            continue
        if os.path.exists(os.path.join(outputs, h[:size] + '.xlsx')):
            name += str(random.randint(0, 10000))
            continue
        else:
            return h[:size]


def fast_get_hash(f_name):
    name = f_name
    size = 12
    while len(name) < 12:
        name += str(random.randint(0, 100))
    hash_object = hashlib.sha256()
    hash_object.update(name.encode('utf-8'))
    h = hash_object.hexdigest()[:12]
    return h + '.xlsx'


# принимает путь до файла и создает excel в outputs/
def convert_pdf_to_excel(file_name):
    h = get_hash(file_name) + '.xlsx'
    h_path = outputs + h
    c.xlsx(file_name, h_path)
    return h_path


# принимает путь до файла и создает excel в outputs/
def convert_pdf_to_excel_with_path_props(filepath):
    filename = os.path.basename(filepath)
    h = fast_get_hash(filename)
    h_path = outputs + h
    c.xlsx(filepath, h_path)
    return h_path


def multi_converter(file_paths):
    print('началось преобразование файлов в excel.')
    for file_path_index in range(len(file_paths)):
        convert_pdf_to_excel(file_paths[file_path_index])
        print(f'прогресс {int((file_path_index + 1) / len(file_paths)) * 100}%...')
    print('преобразование закончилось.')

