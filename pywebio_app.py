from __future__ import annotations
from typing import Any, Optional, Union

from pywebio import start_server, config
from pywebio.session import set_env, info as session_info
from pywebio.output import (
    put_scope, use_scope, put_image, put_markdown, put_table
)

from threading import Thread
from os import environ, path

import requests
import json
import asyncio
import pathlib

from pages import *


try:
    PLAYLIST_GIST = environ['PLAYLIST_GIST']
    try:
        GITHUB_TOKEN = environ['GITHUB_TOKEN']
        URL = f'https://api.github.com/gists/{PLAYLIST_GIST}'
    except:
        GITHUB_TOKEN = None
        URL = None
except:
    PLAYLIST_GIST = None


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
    set_env(title='JustNBS Player DB')
    
    put_scope('image', position=0)
    put_scope('title', position=1)
    put_scope('description', position=2)
    put_scope('inputs', position=3)
    put_scope('latest_tracks', position=4)

    with use_scope('image', clear=True):
        try:
            put_image(open(path.join('resources', 'logo.png'), 'rb').read())
        except:
            pass

    if PLAYLIST_GIST is None:
        put_markdown('# ОТСУТСТВУЕТ PLAYLIST_GIST В ПЕРЕМЕННЫХ СРЕДЫ')
    else:
        if GITHUB_TOKEN is None:
            put_markdown('# ОТСУТСТВУЕТ GITHUB_TOKEN В ПЕРЕМЕННЫХ СРЕДЫ')
        else:
            index_page()

def file_info_page():
    with use_scope('title', clear=True):
        put_markdown('# Подготовка к публикации')
    
    with use_scope('description', clear=True):
        put_markdown('правила загрузки')

    with use_scope('inputs', clear=True):
        pass


# # TODO: на потом
# def show_lyrics_input():
#     with use_scope('inputs', clear=True):
#         put_file_upload(
#             name='uploaded_txt', accept=".txt",
#             max_size='50K', placeholder='Загрузите текст песни',
#         )
#         put_buttons(['Загрузить'], lambda _: upload_data(pin.uploaded_txt))

# def show_latests_table():
#     with use_scope('latest_tracks', clear=True):
#         data = get_latest_tracks()
#         table_data = []
#         for author in data:
#             for track in data[author]:
#                 meta = data[author][track]
#                 table_data.append([author, meta['duration'], meta['file_amount'],],)
        
#         put_table(table_data)

# def get_latest_tracks():
#     response = requests.get(url='https://gist.github.com/AMD-Boii/f8c7e17f23454fbf34c7ca0be7fe6d27/raw/ce4675c5463ced399e779790f51b5bda5169ecff/latest_tracks.json')
#     return response.json()

# def backup_latest_tracks():
#     pass

# def get_full_playlist():
#     pass

# def backup_full_playlist():
#     pass

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