from __future__ import annotations
from typing import Any, Optional, Union

from pywebio import start_server, config
from pywebio.input import *
from pywebio.output import *
from pywebio.session import set_env, info as session_info

from threading import Thread

import requests
import json

#from nbs_parser import get_metadata, parse, separate_data

import github_token
TOKEN = github_token.get()

PLAYLIST_GIST = 'f8c7e17f23454fbf34c7ca0be7fe6d27'
URL = f'https://api.github.com/gists/{PLAYLIST_GIST}'

response: Optional[requests.Request] = None


def request():
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {TOKEN}',
        'X-GitHub-Api-Version': '2022-11-28'
    }

    content = json.dumps(
        {
            "C418": {
                "Sweeden":{
                    "duration": 4643,
                    "id": 'rsd34tt4t8hrvu',
                    "file_amount": 2
                }
            }
        }, 
    )

    new_content = {
        "files": {
            "playlist.json": {
                "content": content,
            }
        }
    }
    
    global response
    response = requests.patch(
        url=URL, headers=headers, data=json.dumps(new_content)
    )
    print(URL, headers, new_content)
    

@config(theme='dark')
def main():
    put_text(TOKEN)
    put_text('hello')

    put_buttons(
        ['Обновить Gist'], 
        onclick=lambda _: Thread(target=request).start()
    )

    global response
    
    while True:
        if response is not None:
            if response.status_code == 200:
                response = None
                popup('Обновление плейлиста успешно!', [
                    put_buttons(['OK'], onclick=lambda _: close_popup())
                ])
            else:
                response = None
                popup('Ошибка обновления', [
                    put_buttons(['Не OK :с'], onclick=lambda _: close_popup())
                ])


if __name__ == "__main__":
    start_server(main, debug=True, port=8000)