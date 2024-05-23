from __future__ import annotations
from typing import Any, Optional, Union

from pywebio.output import use_scope, put_buttons, put_markdown, toast
from pywebio.session import run_js

from .upload import upload_page
from .advice import advice_page


def buttons_action(value):
    match value:
        case 'upload_nbs':
            upload_page()
        case 'module':
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
        case 'onbs_advice':
            advice_page()
        case _:
            toast(
                content='ОШИБКА ОБРАБОТЧИКА НАЖАТИЙ INDEX_PAGE',
                duration=3, color='red',
            )
            index_page()

def index_page():
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
                    ['Опубликовать NBS трек', 'upload_nbs', 'primary'],
                    ['Ссылка на модуль', 'module', 'info'],
                    ['Скачать OpenNBS', 'onbs_download', 'danger'],
                    ['GitHub репозиторий', 'github_repo', 'info'],
                    ['Советы по OpenNBS', 'onbs_advice', 'info']
                ]  
            ],
            onclick=lambda value: buttons_action(value)
        )