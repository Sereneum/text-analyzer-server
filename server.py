from flask import Flask, request, render_template
import requests
from flask_cors import CORS
import os
from error_parser import error_parser
from main import server_file_processing

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'  # Папка, в которую будут сохраняться загруженные файлы
ALLOWED_EXTENSIONS = {'pdf'}  # Разрешенные расширения файлов
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# @app.after_request
# def add_cors_headers(response):
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
#     response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
#     return response


@app.route('/', methods=['GET'])
def default_handler():
    # url = 'http://localhost:5000/upload'
    # files = {'file': ('req.pdf', open('pdfs/М-11 1029 от 27.01.2023.pdf', 'rb'), 'application/pdf')}
    # response = requests.post(url, files=files)
    #
    # print(response.text)

    return 'server is working'


@app.route('/upload', methods=['POST'])
def upload_file():
    print('[POST]')
    if 'file' not in request.files:
        return 'Файл не найден', 400

    file = request.files['file']

    if file.filename == '':
        return 'Имя файла пустое', 400

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        print(f'Файл сохранен по пути {filepath}')
        # simular_path = 'outputs/output2.xlsx'
        # result_processing = error_parser(simular_path)
        result_processing = server_file_processing(filepath)

        print(result_processing)
        return result_processing, 200
    else:
        return 'Недопустимое расширение файла', 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


