from __future__ import annotations
from typing import Any, Optional, Union

from pywebio import start_server, config
from pywebio.input import *
from pywebio.output import *
from pywebio.session import set_env, info as session_info

from threading import Thread

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
async def main():
    # Устанавливаем заголовок вкладки
    set_env(title="Название вкладки")

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
    
    async def handle_file_upload(popup_id):
        uploaded_file = await file_upload(
            "Загрузите файл .nbs", accept=".nbs", popup=popup_id
        )
        if uploaded_file:
            file_size = len(uploaded_file['content'])
            put_text(f"Размер загруженного файла: {file_size} байт", popup=popup_id)
            await asyncio.sleep(1)  # Пауза для демонстрации результата
            popup('popup_id').close()  # Закрываем popup после загрузки файла

    # Функция для отображения popup с формой загрузки файла
    async def show_upload_popup():
        async with popup('popup_id', title="Загрузка файла") as p:
            await handle_file_upload(p.popup_id)

    # Создаем кнопку для открытия popup с формой загрузки файла
    put_buttons(['Загрузить файл'], [show_upload_popup])

    # Добавляем таблицу внизу страницы
    table_data = [
        ['Столбец 1', 'Столбец 2', 'Столбец 3', 'Столбец 4', 'Столбец 5'],
        ['Данные 1', 'Данные 2', 'Данные 3', 'Данные 4', 'Данные 5'],
        ['Данные 1', 'Данные 2', 'Данные 3', 'Данные 4', 'Данные 5'],
        ['Данные 1', 'Данные 2', 'Данные 3', 'Данные 4', 'Данные 5'],
        ['Данные 1', 'Данные 2', 'Данные 3', 'Данные 4', 'Данные 5'],
    ]
    put_table(table_data)

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
    start_server(main, port=8000)