from __future__ import annotations
from typing import Any, Optional, Union

from pywebio.output import use_scope, put_buttons, put_markdown, toast
from pywebio.pin import pin, put_file_upload

from nbs_parser import get_metadata

from .index import index_page


def buttons_action(value):
    match value:
        case 'upload_nbs':
            if pin.uploaded_nbs is None:
                toast(
                    content='Для начала, выберите файл',
                    duration=3, color='info',
                )
            else:
                meta = get_metadata(pin.uploaded_nbs)
        case 'index':
            index_page()
        case _:
            toast(
                content='ОШИБКА ОБРАБОТЧИКА НАЖАТИЙ UPLOAD_PAGE',
                duration=3, color='red',
            )
            index_page()

def upload_page():
    with use_scope('title', clear=True):
        put_markdown('# Выберите файл для загрузки')
    
    with use_scope('description', clear=True):
        put_markdown('правила загрузки')
    
    with use_scope('inputs', clear=True):
        put_file_upload(
            name='uploaded_nbs', accept=".nbs",
            max_size='250K', placeholder='Выбери NBS файл для загрузки',
        )
        put_buttons(
            [  
                dict(label=i[0], value=i[1], color=i[2])  
                for i in [
                    ['Загрузить', 'upload_nbs', 'primary'],
                    ['Отмена', 'index', 'danger']
                ]  
            ],
            onclick=lambda value: buttons_action(value)
        )