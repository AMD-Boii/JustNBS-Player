from __future__ import annotations
from typing import Any, Optional, Union

from flask import Flask, request, render_template_string

from pywebio.platform.flask import webio_view
from pywebio.input import input, FLOAT
from pywebio.output import put_text

#from nbs_parser import get_metadata, parse, separate_data

try:
    import github_token
    TOKEN = github_token.get()
except:
    TOKEN = None

app = Flask(__name__)

@app.route('/')
def upload_form():
    return render_template_string('''
    <!doctype html>
    <title>Upload File</title>
    <h1>Upload a binary file</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    ''')

@app.route('/', methods=['POST'])
def upload_file():
    # Проверяем, что в запросе есть файл
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    
    # Проверяем, что файл выбран
    if file.filename == '':
        return 'No selected file', 400

    # Читаем файл в бинарную переменную
    file_content = file.read()

    # Для примера выводим размер файла в байтах
    file_size = len(file_content)
    return f'File uploaded successfully! File size: {file_size} bytes'

if __name__ == "__main__":
    app.run(debug=True)