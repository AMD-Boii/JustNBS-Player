from __future__ import annotations
from typing import Any, Optional, Union

from pywebio import start_server, config
from pywebio.input import *
from pywebio.output import *
from pywebio.pin import *
from pywebio.session import set_env, info as session_info, run_js

from threading import Thread
from os import environ, path
from io import BytesIO
from requests import get as req_get, post as req_post

import requests
import json
import asyncio

from nbs_parser import TEMPO, get_metadata, parse, separate_data


try:
    PLAYLIST_GIST = environ['PLAYLIST_GIST']
    try:
        GITHUB_TOKEN = environ['GITHUB_TOKEN']
        URL = f'https://api.github.com/gists/{PLAYLIST_GIST}'
    except:
        GITHUB_TOKEN = None
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

    if PLAYLIST_GIST is None:
        put_markdown('# ОТСУТСТВУЕТ PLAYLIST_GIST В ПЕРЕМЕННЫХ СРЕДЫ')
    else:
        if GITHUB_TOKEN is None:
            put_markdown('# ОТСУТСТВУЕТ GITHUB_TOKEN В ПЕРЕМЕННЫХ СРЕДЫ')
        elif not GITHUB_TOKEN.startswith('ghp_'):
            put_markdown('# НЕВЕРНЫЙ ФОРМАТ GITHUB_TOKEN')
        else:
            try:
                with use_scope('image', clear=True):
                    put_image(
                        open(path.join('resources', 'logo.png'), 'rb').read()
                    )
            except:
                with use_scope('image', clear=True):
                    put_markdown('# NO_IMAGE')
            index_page()

def index_page():
    def buttons_action(value):
        match value:
            case 'upload_page':
                upload_page()
            case 'module_page':
                run_js(
                    """
                    navigator.clipboard.writeText("Hello, World!").then(function() {
                    }, function(err) {
                        console.error('Could not copy text: ', err);
                    });
                    """
                )
                toast(
                    content='Ссылка скопирована в буфер обмена!',
                    duration=3, color='info',
                )
            case 'onbs_download':
                run_js(
                    """
                    window.open(
                        "https://github.com/OpenNBS/OpenNoteBlockStudio/releases"
                    )
                    """
                )
            case 'github_repo':
                run_js(
                    """
                    window.open("https://github.com/AMD-Boii/JustNBS-Player")
                    """
                )
            case 'advice_page':
                advice_page()
            case _:
                toast(
                    content='ОШИБКА ОБРАБОТЧИКА НАЖАТИЙ INDEX_PAGE',
                    duration=3, color='red',
                )
                index_page()
    
    with use_scope('title', clear=True):
        put_markdown('# Добро пожаловать')
    
    with use_scope('description', clear=True):
        put_markdown(
            '''
            Ссылка на ресурс пак с расширением октав
            Требования к .nbs файлу:
            • версия OpenNBS -- 3.10.0
            • использовать только стандартные звуки
            Короткий гайд по созданию мелодии:
            • скачайте и установите Open Note Block Studio 3.10.0
            '''
        )
    
    with use_scope('inputs', clear=True):
        put_buttons(
            [  
                dict(label=i[0], value=i[1], color=i[2])  
                for i in [
                    ['Опубликовать NBS трек', 'upload_page', 'primary'],
                    ['Ссылка на модуль', 'module_page', 'info'],
                    ['Скачать OpenNBS', 'onbs_download', 'danger'],
                    ['GitHub репозиторий', 'github_repo', 'info'],
                    ['Советы по OpenNBS', 'advice_page', 'info'],
                ]  
            ],
            onclick=lambda value: buttons_action(value)
        )

def advice_page():
    def buttons_action(value):
        match value:
            case 'index_page':
                index_page() 

    with use_scope('title', clear=True):
        put_markdown('# Советы по работе с OpenNBS')
    
    with use_scope('description', clear=True):
        put_markdown(
            '''
            Короткий гайд по созданию мелодии:
            • скачайте и установите Open Note Block Studio 3.10.0
            '''
        )
    
    with use_scope('inputs', clear=True):
        put_buttons(
            [  
                dict(label=i[0], value=i[1], color=i[2])  
                for i in [
                    ['На главную', 'index_page', 'primary'],
                ]  
            ],
            onclick=lambda value: buttons_action(value)
        )
    
def upload_page():
    def buttons_action(value):
        match value:
            case 'upload_nbs':
                if pin.uploaded_nbs is None:
                    toast(
                        content='Для начала, выберите файл',
                        duration=3, color='info',
                    )
                else:
                    nbs_data = get_metadata(BytesIO(pin.uploaded_nbs['content']))
                    if isinstance(nbs_data, str):
                        toast(
                            content=str(nbs_data),
                            duration=3, color='red',
                        )
                    elif not nbs_data[0].tempo in TEMPO:
                        edit_tempo_page(nbs_data)
                    else:
                        edit_meta_page(nbs_data)

            case 'index_page':
                index_page()

    with use_scope('title', clear=True):
        put_markdown('# Выберите файл для загрузки')
    
    with use_scope('description', clear=True):
        put_markdown('правила загрузки')
    
    with use_scope('inputs', clear=True):
        put_file_upload(
            name='uploaded_nbs', accept=".nbs",
            max_size='250K', placeholder='Выбери NBS файл для загрузки',
            help_text='hello'
        )
        put_buttons(
            [  
                dict(label=i[0], value=i[1], color=i[2])  
                for i in [
                    ['Загрузить', 'upload_nbs', 'primary'],
                    ['Отмена', 'index_page', 'danger']
                ]  
            ],
            onclick=lambda value: buttons_action(value)
        )

def edit_tempo_page(nbs_data):    
    def buttons_action(value):
        match value:
            case 'edit_meta_page':
                edit_meta_page(nbs_data)
            case 'upload_page':
                upload_page()
    
    with use_scope('title', clear=True):
        put_markdown('# NBS имеет неподдерживаемый темп!')
    
    with use_scope('description', clear=True):
        put_markdown('Не беда! Вы можете изменить темп прямо здесь!')
        put_markdown('Но лучше вернуться в OpenNBS и тщательно его отредактировать...')
        put_markdown('')
        put_markdown('Выберите максимально близкий к исходному темп.')
    
    with use_scope('inputs', clear=True):
        put_select(
            label=f'Выберите поддерживаемый темп (исходный темп {nbs_data[0].tempo} t/s)',
            name='new_tempo',
            options=[  
                dict(label=i[0], value=i[1], selected=i[2])  
                for i in [
                    ['20.0 t/s', 20.0, True],
                    ['10.0 t/s', 10.0, None],
                    ['6.67 t/s', 6.67, None],
                    ['5.0 t/s', 5.0, None],
                    ['4.0 t/s', 4.0, None],
                    ['3.33 t/s', 3.33, None],
                    ['2.86 t/s', 2.86, None],
                    ['2.5 t/s', 2.5, None],
                    ['2.22 t/s', 2.22, None],
                    ['10.0 t/s', 10.0, None],
                ]  
            ],
        )
        put_buttons(
            [  
                dict(label=i[0], value=i[1], color=i[2])  
                for i in [
                    ['Подтвердить', 'edit_meta_page', 'danger'],
                    ['Отмена', 'upload_page', 'danger'],
                ]  
            ],
            onclick=lambda value: buttons_action(value)
        )

def edit_meta_page(nbs_data):
    def buttons_action(value):
        match value:
            case 'use_song_author':
                pin.author = nbs_data[0].song_author
            case 'use_origin_author':
                pin.author = nbs_data[0].original_author
            case 'upload_page':
                upload_page()

    with use_scope('title', clear=True):
        put_markdown('# Подготовка к публикации')
    
    with use_scope('description', clear=True):
        put_markdown('Подтвердите или измените метаданные NBS файла')

    with use_scope('inputs', clear=True):
        
        put_input('author', label='Автор', value=nbs_data[0].original_author)
        put_markdown('Использовать имя автора из:')
        put_buttons(
            [  
                dict(label=i[0], value=i[1], color=i[2])  
                for i in [
                    ['Song author', 'use_song_author', 'danger'],
                    ['Original song author', 'use_origin_author', 'danger']
                ]  
            ],
            onclick=lambda value: buttons_action(value)
        )
        
        put_input('song_name', label='Название', value=nbs_data[0].song_name)
        
        put_buttons(
            [  
                dict(label=i[0], value=i[1], color=i[2])  
                for i in [
                    ['Отмена', 'upload_page', 'danger']
                ]  
            ],
            onclick=lambda value: buttons_action(value)
        )

# FIXME
def add_lyrics_page(nbs_data):
    def buttons_action(value):
        match value:
            case 'upload_nbs':
                if pin.uploaded_nbs is None:
                    toast(
                        content='Для начала, выберите файл',
                        duration=3, color='info',
                    )
                else:
                    nbs_data = get_metadata(BytesIO(pin.uploaded_nbs['content']))
                    if isinstance(nbs_data, str):
                        toast(
                            content=str(nbs_data),
                            duration=3, color='red',
                        )
                    elif not nbs_data[0].tempo in TEMPO:
                        edit_tempo_page(nbs_data)
                    else:
                        edit_meta_page(nbs_data)

            case 'index_page':
                index_page()

    with use_scope('title', clear=True):
        put_markdown('# Выберите файл для загрузки')
    
    with use_scope('description', clear=True):
        put_markdown('правила загрузки')
    
    with use_scope('inputs', clear=True):
        put_file_upload(
            name='uploaded_nbs', accept=".nbs",
            max_size='250K', placeholder='Выбери NBS файл для загрузки',
            help_text='hello'
        )
        put_buttons(
            [  
                dict(label=i[0], value=i[1], color=i[2])  
                for i in [
                    ['Загрузить', 'upload_nbs', 'primary'],
                    ['Отмена', 'index_page', 'danger']
                ]  
            ],
            onclick=lambda value: buttons_action(value)
        )
        

def show_latests_table():
    with use_scope('latest_tracks', clear=True):
        data = get_latest_tracks()
        table_data = []
        for author in data:
            for track in data[author]:
                meta = data[author][track]
                table_data.append([author, meta['duration'], meta['file_amount'],],)
        
        put_table(table_data)

def get_latest_tracks():
    response = requests.get(url='https://gist.github.com/AMD-Boii/f8c7e17f23454fbf34c7ca0be7fe6d27/raw/ce4675c5463ced399e779790f51b5bda5169ecff/latest_tracks.json')
    return response.json()

def backup_latest_tracks():
    pass

def get_full_playlist():
    pass

def backup_full_playlist():
    pass

def upload_data(uploaded_nbs):
    # popup(title='Размер файла', content=str(len(fileobj['content']),),)
    show_lyrics_input()
    

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