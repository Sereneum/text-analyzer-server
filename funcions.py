from api import ask_question
# находит индекс первого куска данных таблицы
def find_table_begin_position(sheet):
    try:
        def is_row_begin(r):
            if not str(r[0].value) == '1':
                return False
            row10 = list([r[i].value for i in range(10)])
            test10 = list([i for i in range(1, 11)])
            return row10 == test10

        flag_row_begin = False
        row_begin_position = -1

        for row_idx, row in enumerate(sheet.iter_rows(), start=1):
            if not flag_row_begin:
                flag_row_begin = is_row_begin(row)
                if not flag_row_begin:
                    continue
            if not row[0].value == '':
                row_begin_position = row_idx
                break
        return row_begin_position
    except Exception as e:
        print('[ERROR]', e)
        return -1


def create_table_buffer_m11(sheet, table_begin_position):
    try:
        buffer_size = min(16, sheet.max_column)
        buffer = list([[] for i in range(0, buffer_size)])
        row_max = sheet.max_row

        for row_pos in range(table_begin_position, row_max):
            for i in range(buffer_size):
                col = i + 1
                cell = sheet.cell(row_pos, col).value
                if col == 2 or cell is None:
                    continue
                buffer[i].append(cell)

        return buffer
    except Exception as e:
        print('[ERROR]', e)
        return []


def operations_m11(buffer):
    try:
        errors = []
        # print(min_buf_size(buffer))
        print(buffer)
        for buffer_index in range(len(buffer[0])):
            try:
                buf_3 = str(buffer[3][buffer_index])
                buf_8 = str(buffer[8][buffer_index])
                buf_9 = str(buffer[9][buffer_index])
                buf_10 = str(buffer[10][buffer_index])
                buf_11 = str(buffer[11][buffer_index])
                buf_12 = str(buffer[12][buffer_index])
                buf_13 = str(buffer[13][buffer_index])
            except:
                continue

            if not len(str(buf_3)) == 10 and not buf_3 == '-':
                e = f'Ошибке в длине номенклатурного номера: {buf_3}'
                errors.append(e)
            if not str(buf_3).isdigit() and not buf_3 == '-':
                e = f'Ошибке в формате номенклатурного номера: {buf_3}'
                errors.append(e)
            if str(buf_8).isdigit() and len(buf_8) and not buf_8 == '-':
                e = f'Ошибке в коде единицы измерения материальных ценностей: {buf_8}'
                errors.append(e)
            if not str(buf_9).isdigit() and len(buf_9) and not buf_9 == '-':
                e = f'Ошибке в наименовании единицы измерения материальных ценностей: {buf_9}'
                errors.append(e)
            if not is_float(buf_10) and len(buf_10) and not buf_10 == '-':
                e = f'Ошибке в формате количества товарно-материальных ценностей: {buf_10}'
                errors.append(e)
            if not is_float(buf_11) and len(buf_11) and not buf_11 == '-':
                e = f'Ошибке в формате фактическом количестве отпущенных материальных ценностей: {buf_11}'
                errors.append(e)
            if not is_float(buf_12) and len(buf_12) and not buf_12 == '-':
                e = f'Ошибке в формате цены за единицу отпускаемых товарно-материальных ценностей (без учета НДС): {buf_12}'
                errors.append(e)
            if not is_float(buf_13) and len(buf_13) and not buf_13 == '-':
                e = f'Ошибке в формате стоимости (без учета НДС) ценностей : {buf_13}'
                errors.append(e)
        return errors
    except Exception as e:
        print('[ERROR]', e)
        return [f'Ошибка в обработки таблицы для поиска ошибки. возможна ошибка в заполнении таблицы.']


def fill_data_table_m11(sheet):
    table_begin_position = find_table_begin_position(sheet)
    if table_begin_position == -1:
        e = 'ОШИБКА ИНДЕКСАЦИИ ТАБЛИЦЫ'
        return [], [e]
    table_begin_position += 1
    buffer = create_table_buffer_m11(sheet, table_begin_position)
    if not len(buffer):
        e = 'ошибка заполнения буфера данными из таблицы'
        return [], [e]
    errors = operations_m11(buffer)

    return [], [errors]


def define_doc_type(sheet):
    try:
        for row in range(sheet.max_row):
            for col in range(sheet.max_column):
                cell = str(sheet.cell(row + 1, col + 1).value)
                if cell is None:
                    continue
                if not cell.find("ФМУ-76") == -1:
                    return "ФМУ-76"
                if not cell.find("М-11") == -1:
                    return "М-11"
        return ""
    except Exception as e:
        print('[ERROR]', e)
        return "error"


def create_table_buffer(sheet, table_begin_position):
    try:
        buffer_size = min(18, sheet.max_column)
        buffer = list([[] for i in range(0, buffer_size)])
        row_max = sheet.max_row

        # for row_pos in sheet.iter_rows()
        for row_pos in range(table_begin_position, row_max):
            for i in range(buffer_size):
                col = i + 1
                cell = sheet.cell(row_pos, col).value
                if col == 5 or col == 7 or cell == '' or cell is None:
                    continue
                # print({
                #     'row': row_pos,
                #     'col': col,
                #     'val': cell
                # })
                buffer[i].append(cell)

        return buffer
    except Exception as e:
        print('[ERROR]', e)
        return []


column_names = [
    '''счет 32 (затраты)''',
    '''производственный заказ''',
    '''корреспондирующий счет (счет_субсчет)''',
    '''корреспондирующий счет (код аналитического учета)''',
    '''материальные ценности (наим., сорт, размер, марка)''',
    '''материальные ценности (номенклатурный счет)''',
    '''заводской номер детали''',
    '''ед. измерения (код)''',
    '''ед. измерения (наименование)''',
    '''нормативное кол.во''',
    '''фактическое израсходовано (кол-во) ''',
    '''фактическое израсходовано (цена, руб. коп.) ''',
    '''фактическое израсходовано (сумма, руб. коп) ''',
    '''откл. факт. расхода от нормы (-экономия, +перерасход)''',
    '''вид работ или ремонта, содержание хоз. операций''',
    '''срок пол. исп., причина откл. в расходе и др.''',
    '''регистрационный номер партии товара под надзором'''
]


def get_column_names(index):
    return column_names[index]


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# def bad_validation(buf="", v_not_=False, v_len=False, v_fl=False, v_dg=False):
#     # v_not_ == not buf == '-' -> (not v_not_)
#     # if not buf.isdigit() and not buf == '-':
#     return (v_not_ and not buf == '-') and (v_dg and not buf.isdigit()) \
#            and (v_len and len(buf)) and (v_fl and not is_float(buf))
 # if bad_validation(buf=buf_11, v_len=True, v_not_=True, v_fl=True):
            #     print('bad_validation')
            #     errors.append(f'Ошибке в формате цены (руб): {buf_11}')
# def bad_validation(buf="", type_v=""):
#     if type_v == "format":


# def error_handler()


def custom_ask_question(value):
    q = f'может ли наименование единицы измерения быть: {value}?'
    try:
        response = ask_question(q)
        if value.lower() == 'штука':
            return True, None
        print(f'bot_res: {response}')
        if len(response) >= 3:
            if response[:3].lower() == 'нет':
                return False, response
    except:
        return True, None
    return True, None



def operations(buffer):
    try:
        errors = []
        # phase 1
        for buffer_index in range(len(buffer[0])):
            try:
                buf_0 = str(buffer[0][buffer_index])
                buf_1 = str(buffer[1][buffer_index])
                buf_7 = str(buffer[7][buffer_index])
                buf_7_neuro = str(buffer[8][buffer_index])
                buf_10 = str(buffer[10][buffer_index])
                buf_11 = str(buffer[11][buffer_index])
                buf_12 = str(buffer[12][buffer_index])
                buf_13 = str(buffer[13][buffer_index])
            except:
                continue
            # print(f'buf_7_neuro={buf_7_neuro}')

            bot_res, text_bot_res = custom_ask_question(buf_7_neuro.lower())
            if not bot_res:
                e = f'Ошибка в наименовании ед. из.: {text_bot_res}'
                print(e)
                errors.append(e)

            if not len(buf_0) == 10 and not buf_0 == '-':
                e = f'Ошибке в длине кода учета затрат на производство: {buf_0}'
                errors.append(e)
            if not str(buf_0).isdigit() and not buf_0 == '-':
                e = f'Ошибке в формате кода учета затрат на производство: {buf_0}'
                errors.append(e)
            if not len(buf_1) == 12 and not buf_1 == '-':
                e = f'Ошибке в длине кода производственного заказа: {buf_1}'
                errors.append(e)
            if not buf_7.isdigit() and len(buf_7) and not buf_7 == '-':
                e = f'Ошибке в формате кода: {buf_7}'
                errors.append(e)
            if not is_float(buf_10) and len(buf_10) and not buf_10 == '-':
                e = f'Ошибке в формате (нормативного) кол-ва: {buf_10}'
                errors.append(e)
            if not is_float(buf_11) and len(buf_11) and not buf_11 == '-':
                e = f'Ошибке в формате цены (руб): {buf_11}'
                errors.append(e)
            if not is_float(buf_12) and len(buf_12) and not buf_12 == '-':
                e = f'Ошибке в формате суммы (руб): {buf_10}'
                errors.append(e)
            if is_float(buf_10) and len(buf_10) and is_float(buf_11) and len(buf_11) and is_float(buf_12) and len(
                    buf_12) and not buf_12 == '-':
                if not int(float(buf_10) * float(buf_11)) == int(float(buf_12)):
                    e = f'Неправильно посчитана сумма (руб): {buf_12}'
                    errors.append(e)

            if len(buf_13) and not buf_13 == '-' and not buf_13 == '+' and not buf_13 == '0':
                e = f'Ошибке в формате (расхода или перерасхода): {buf_13}'
                errors.append(e)

        # if len(errors):
        #     print('[ERRORS]', errors)
        return errors
    except Exception as e:
        print('[ERROR]', e)
        return [f'Ошибка в обработки таблицы для поиска ошибки. возможна ошибка в заполнении таблицы.']


def fill_data_table(sheet):
    table_begin_position = find_table_begin_position(sheet)
    if table_begin_position == -1:
        e = 'ОШИБКА ИНДЕКСАЦИИ ТАБЛИЦЫ'
        return [], [e]
    table_begin_position += 1  # ?
    buffer = create_table_buffer(sheet, table_begin_position)
    if not len(buffer):
        e = 'ошибка заполнения буфера данными из таблицы'
        return [], [e]
    errors = operations(buffer)

    try:
        table = list({"name": get_column_names(i), "content": []} for i in range(len(buffer)))
        for i in range(len(buffer)):
            for buf in buffer[i]:
                table[i]["content"].append(buf)
    except Exception as e:
        print('[ERROR]', e)
        table = []

    return [table, errors]
