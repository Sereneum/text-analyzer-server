from pdf_converter import convert_pdf_to_excel, multi_converter, convert_pdf_to_excel_with_path_props
import os
from error_parser import error_parser
# used .py files: main, pdf_converter, error_parser, functions

file_paths = [
    'pdfs/ФМУ-76_ 67_05.06.2023(39).pdf',
    'pdfs/ФМУ-76  №592 от 30.03.2023.pdf',
    'pdfs/ФМУ-76 №32947 от 22.08.2023 к ФМУ-73 №7 от 07.08.2023.pdf',
    'pdfs/ФМУ-76 №31434 от 31.07.2023.pdf'
]


def middleware(error_parser_response):
    return error_parser_response
    # if len(errors):
    #     return {
    #         'description': 'Файл содержит ошибки.',
    #         'errors': errors
    #     }
    # else:
    #     return {
    #         'description': 'Файл не содержит ошибки.',
    #         'errors': []
    #     }


def server_file_processing(filepath):
    excel_path = convert_pdf_to_excel_with_path_props(filepath)
    response = error_parser(excel_path)
    return middleware(response)
    # return [{"filepath": filepath, "errors": errors}]


# curr_path = 'outputs/output2.xlsx'
# errors = error_parser(curr_path)
# print('errors:', errors)

