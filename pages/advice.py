from __future__ import annotations
from typing import Any, Optional, Union

from pywebio.output import use_scope, put_buttons, put_markdown, toast

from .index import index_page


def buttons_action(value):
    match value:
        case 'index':
            index_page() 
        case _:
            toast(
                content='ОШИБКА ОБРАБОТЧИКА НАЖАТИЙ ADVICE_PAGE',
                duration=3, color='red',
            )
            index_page()

def advice_page():
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
                    ['На главную', 'index', 'primary'],
                    ['Опубликовать NBS трек', 'upload_nbs', 'primary'],
                    ['Скачать OpenNBS', 'onbs_download', 'danger'],
                    ['GitHub репозиторий', 'github_repo', 'info'],
                ]  
            ],
            onclick=lambda value: buttons_action(value)
        )