from __future__ import annotations
from typing import Any, Optional, Union

from pywebio import start_server, config
from pywebio.input import *
from pywebio.output import *
from pywebio.pin import *
from pywebio.session import set_env, info as session_info

from threading import Thread

from os import pardir, path, pathsep

import requests
import json
import asyncio

#from nbs_parser import get_metadata, parse, separate_data

import github_token
TOKEN = github_token.get()

PLAYLIST_GIST = 'f8c7e17f23454fbf34c7ca0be7fe6d27'
URL = f'https://api.github.com/gists/{PLAYLIST_GIST}'

response: Optional[requests.Request] = None


# def lang(en: str, ru: str) -> str:
#     return ru if 'ru' or 'ua' or 'be' in session_info.user_language else en

# def request():
#     headers = {
#         'Accept': 'application/vnd.github+json',
#         'Authorization': f'Bearer {TOKEN}',
#         'X-GitHub-Api-Version': '2022-11-28'
#     }

#     content = json.dumps(
#         {
#             "C418": {
#                 "Sweeden":{
#                     "duration": 4643,
#                     "id": 'rsd34tt4t8hrvu',
#                     "file_amount": 2
#                 }
#             }
#         }, 
#     )

#     new_content = {
#         "files": {
#             "playlist.json": {
#                 "content": content,
#             }
#         }
#     }
    
#     global response
#     response = requests.patch(
#         url=URL, headers=headers, data=json.dumps(new_content)
#     )
#     print(URL, headers, new_content) 

@config(theme='dark')
def main():
    set_env(title="JustNBS")
    
    put_scope('image', position=0)
    put_scope('title', position=1)
    put_scope('description', position=2)
    put_scope('inputs', position=3)
    put_scope('latest_tracks', position=4)

    render_title()
    render_file_input()
    render_latests_table()

def render_image():
    with use_scope('title', clear=True):
        put_image()

def render_title():
    with use_scope('title', clear=True):
        put_markdown(
            '''
            # Загрузка мелодий в JustNBS плеер
            Ссылка на ресурс пак с расширением октав
            Требования к .nbs файлу:
            • версия OpenNBS -- 3.10.0
            • использовать только стандартные звуки
            Короткий гайд по созданию мелодии:
            • скачайте и установите Open Note Block Studio 3.10.0
            '''
        )

def render_file_input():
    with use_scope('inputs', clear=True):
        put_file_upload(
            name='uploaded_nbs', accept=".nbs",
            max_size='250K', placeholder='Выбери NBS файл для загрузки',
        )
        put_buttons(['Загрузить'], lambda _: upload_data(pin.uploaded_nbs))

def render_lyrics_input():
    with use_scope('inputs', clear=True):
        put_file_upload(
            name='uploaded_txt', accept=".txt",
            max_size='50K', placeholder='Загрузите текст песни',
        )
        put_buttons(['Загрузить'], lambda _: upload_data(pin.uploaded_txt))

def render_latests_table():
    with use_scope('latest_tracks', clear=True):
        table_data = [
            ['Столбец 1', 'Столбец 2', 'Столбец 3', 'Столбец 4', 'Столбец 5'],  
            ['Данные 1', 'Данные 2', 'Данные 3', 'Данные 4', 'Данные 5'],
        ]
        put_table(table_data)

def upload_data(uploaded_nbs):
    # popup(title='Размер файла', content=str(len(fileobj['content']),),)
    render_lyrics_input()
    

    # put_buttons(
    #     ['Обновить Gist'], 
    #     onclick=lambda _: Thread(target=request).start()
    # )

    # global response
    
    # while True:
    #     if response is not None:
    #         if response.status_code == 200:
    #             response = None
    #             popup('Обновление плейлиста успешно!', [
    #                 put_buttons(['OK'], onclick=lambda _: close_popup())
    #             ])
    #         else:
    #             response = None
    #             popup('Ошибка обновления', [
    #                 put_buttons(['Не OK :с'], onclick=lambda _: close_popup())
    #             ])


if __name__ == '__main__':
    start_server(main, host='127.0.0.1', port=8000)