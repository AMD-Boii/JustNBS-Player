# Released under the MIT License. See LICENSE for details.
#
"""PyWebIO app."""

from __future__ import annotations
from typing import Any, Optional, Union

from pywebio import start_server, config
from pywebio.input import *
from pywebio.output import *
from pywebio.pin import *
from pywebio.session import set_env, info as session_info, run_js

from os import environ, path
from requests import get as get_req, post as post_req, patch as patch_req
from re import fullmatch, sub

from io import BytesIO

import json

from nbs_parser import (
    TEMPO, get_metadata, parse, sepparate_data, Header
)


try:
    JUSTNBS_GIST_ID = environ['JUSTNBS_GIST_ID']
    try:
        ACTUAL_PLAYLIST_RAW = environ['ACTUAL_PLAYLIST_RAW']
        try:
            LATEST_TRACKS_RAW = environ['LATEST_TRACKS_RAW']
            try:
                GISTS_ACCESS_TOKEN = environ['GISTS_ACCESS_TOKEN']
                API_URL = 'https://api.github.com/gists/'
                REQ_HEADERS = {
                    'Accept': 'application/vnd.github+json',
                    'Authorization': f'Bearer {GISTS_ACCESS_TOKEN}',
                    'X-GitHub-Api-Version': '2022-11-28',
                }
            except:
                GISTS_ACCESS_TOKEN = None
        except:
            LATEST_TRACKS_RAW = None
    except:
        ACTUAL_PLAYLIST_RAW = None
except:
    JUSTNBS_GIST_ID = None

STYLE_MARGIN_TOP = r'margin-top:20px;'


@config(theme='dark')
def main():
    global translate

    if session_info.user_language == 'ru':
        import translation.ru as translate
    else:
        import translation.en as translate

    # ЗАГЛУШКА ДЛЯ РАЗРАБОТКИ
    import translation.ru as translate

    lang = translate.Main

    set_env(title=lang.TAB_TITLE)
    
    put_scope('image', position=0,)
    put_scope('title', position=1,)
    put_scope('content', position=2,)
    put_scope('inputs', position=3,)
    put_scope('latest_tracks', position=4,)

    if JUSTNBS_GIST_ID is None:
        put_markdown(lang.NO_JUSTNBS_GIST_ID)
    elif not bool(fullmatch(r'[0-9a-f]{32}', JUSTNBS_GIST_ID),):
        put_markdown(lang.WRONG_JUSTNBS_GIST_ID_FORMAT)

    elif ACTUAL_PLAYLIST_RAW is None:
        put_markdown(lang.NO_ACTUAL_PLAYLIST_RAW)
    elif not ACTUAL_PLAYLIST_RAW.startswith(r'https://gist.github.com/'):
        put_markdown(lang.WRONG_ACTUAL_PLAYLIST_RAW_FORMAT)
    elif not JUSTNBS_GIST_ID in ACTUAL_PLAYLIST_RAW:
        put_markdown(lang.WRONG_ACTUAL_PLAYLIST_RAW_FORMAT)

    elif LATEST_TRACKS_RAW is None:
        put_markdown(lang.NO_LATEST_TRACKS_RAW)
    elif not LATEST_TRACKS_RAW.startswith(r'https://gist.github.com/'):
        put_markdown(lang.WRONG_LATEST_TRACKS_RAW_FORMAT)
    elif not JUSTNBS_GIST_ID in LATEST_TRACKS_RAW:
        put_markdown(lang.WRONG_LATEST_TRACKS_RAW_FORMAT)

    elif GISTS_ACCESS_TOKEN is None:
        put_markdown(lang.NO_GISTS_ACCESS_TOKEN)
    elif not GISTS_ACCESS_TOKEN.startswith(r'ghp_'):
        put_markdown(lang.WRONG_GISTS_ACCESS_TOKEN_FORMAT)
    elif not bool(fullmatch(r'[0-9a-zA-Z]{36}', GISTS_ACCESS_TOKEN[4:]),):
        put_markdown(lang.WRONG_GISTS_ACCESS_TOKEN_FORMAT)
    else:
        try:
            with use_scope('image', clear=True,):
                put_image(
                    open(path.join('resources', lang.LOGO,), 'rb').read(),)
        except:
            with use_scope('image', clear=True,):
                put_markdown('# NO_IMAGE')
        index_page()
        check_token()

def check_token():
    lang = translate.Main

    test_token = get_req(url=API_URL[:-6]+'user', headers=REQ_HEADERS)

    if test_token.status_code == 403:
        remove('title')
        remove('content')
        remove('inputs')
        put_markdown(lang.REACHED_API_LIMIT)
    elif test_token.status_code != 200:
        remove('title')
        remove('content')
        remove('inputs')
        put_markdown(lang.INVALID_GISTS_ACCESS_TOKEN)
    
def index_page():
    lang = translate.IndexPage

    run_js(r"window.onbeforeunload = null")

    def button_actions(value):
        match value:
            case 'btn_go_upload':
                upload_page()
            case 'btn_res_pack':
                run_js(r"""
                navigator.clipboard.writeText(
                "https://gitlab.com/-/snippets/3710689/raw/main/EXTENDED_1.13.zip"
                ).then(function() {}, function(err) {
                    console.error('Could not copy text: ', err);
                });
                """)
                toast(
                    content=lang.LINK_COPIED,
                    duration=3, color='info',)
            case 'btn_onbs_dwnld':
                run_js(r"""
                window.open(
                "https://github.com/OpenNBS/OpenNoteBlockStudio/releases")
                """)
            case 'btn_github_repo':
                run_js(r"""
                window.open("https://github.com/AMD-Boii/JustNBS-Player")
                """)
            case 'btn_go_search':
                index_page()
    
    with use_scope('title', clear=True):
        put_markdown(lang.WELCOME)
    
    with use_scope('content', clear=True):
        put_tabs(
            tabs=[
            {
                'title': lang.ABOUT,
                'content': [
                    put_markdown(lang.ABOUT_CONTENT),
                    put_buttons(
                        [  
                            dict(label=i[0], value=i[1], color=i[2])  
                            for i in [
                                [lang.B_GHUB_REPO, 'btn_github_repo', 'info'],]  
                        ],
                        onclick=lambda value: button_actions(value),),
                ],
            },
            {
                'title': lang.INSTALLING,
                'content': [
                    put_markdown(lang.INSTALLING_CONTENT),
                    put_buttons(
                        [  
                            dict(label=i[0], value=i[1], color=i[2])  
                            for i in [
                                [lang.B_RES_LINK, 'btn_res_pack', 'info'],]  
                        ],
                        onclick=lambda value: button_actions(value),),
                ],
            },
            {
                'title': lang.REQS,
                'content': [
                    put_markdown(lang.REQS_CONTENT),],
            },
            {
                'title': lang.RECENT_TRACKS,
                'content': [
                    put_markdown('# TODO вывод последних'), #TODO
                    put_buttons(
                        [  
                            dict(label=i[0], value=i[1], color=i[2])  
                            for i in [
                                [lang.B_REFRESH, 'btn_refresh_recent', 'info'],]  
                        ],
                        onclick=lambda value: button_actions(value),),
                ],
            },
            {
                'title': lang.HELP,
                'content': [
                    put_markdown(lang.HELP_CONTENT),
                    put_buttons(
                        [  
                            dict(label=i[0], value=i[1], color=i[2])  
                            for i in [
                                [lang.B_DOWN_ONBS, 'btn_onbs_dwnld', 'danger'],]  
                        ],
                        onclick=lambda value: button_actions(value),),
                ],
            },],
        )
    
    with use_scope('inputs', clear=True,):
        put_buttons(
            [  
                dict(label=i[0], value=i[1], color=i[2])  
                for i in [
                    [lang.B_UPLOAD, 'btn_go_upload', 'primary'],
                    [lang.B_SEARCH, 'btn_go_search', 'primary'],]  
            ],
            onclick=lambda value: button_actions(value),)

def show_latests(): # TODO
    pass

def upload_page():
    lang = translate.UploadPage
    max_size = 250

    run_js(r"""
    window.onbeforeunload = function() {
        return "WARNING";
    }
    """.replace('WARNING', lang.REFRESH_WARNING),)

    def button_actions(value):
        match value:
            case 'btn_upload':
                if pin.uploaded_file is None:
                    toast(
                        content=lang.PICK_A_FILE_FIRST,
                        duration=3, color='info',)
                else:
                    nbs_data = get_metadata(BytesIO(pin.uploaded_file['content']),)
                    if isinstance(nbs_data, str):
                        toast(
                            content=nbs_data,
                            duration=3, color='red',)
                    elif not nbs_data[0].old_tempo in TEMPO:
                        fix_tempo_page(nbs_data)
                    else:
                        edit_header_page(nbs_data)
            case 'btn_cancel':
                index_page()

    with use_scope('title', clear=True,):
        put_markdown(lang.CHOOSE_FILE)
    
    with use_scope('content', clear=True,):
        put_markdown(lang.UPLOAD_RULES)
    
    with use_scope('inputs', clear=True,):
        put_file_upload(
            name='uploaded_file',
            label='Выберите файл для загрузки',
            accept='.nbs',
            max_size=f'{max_size}K', placeholder=lang.PLACEHOLDER,
            help_text=lang.MAX_SIZE.replace('MAX', str(max_size))).style(STYLE_MARGIN_TOP)
        put_buttons(
            [  
                dict(label=i[0], value=i[1], color=i[2])  
                for i in [
                    [lang.UPLOAD, 'btn_upload', 'primary'],
                    [lang.CANCEL, 'btn_cancel', 'danger'],]  
            ],
            onclick=lambda value: button_actions(value),).style(STYLE_MARGIN_TOP)

def overview_custom_page(nbs_data: tuple[Header, list, list,]): # TODO
    pass
    # def button_actions(value):
    #     match value:
    #         case 'btn_accept':
    #             if not nbs_data[0].old_tempo in TEMPO:
    #                 fix_tempo_page(nbs_data)
    #             else:
    #                 edit_header_page(nbs_data)
    #         case 'btn_go_back':
    #             upload_page()

    # with use_scope('title', clear=True):
    #     put_markdown('# custom')
    
    # with use_scope('content', clear=True):
    #     put_markdown('custom')
    
    # with use_scope('inputs', clear=True):
    #     put_buttons(
    #         [  
    #             dict(label=i[0], value=i[1], color=i[2])
    #             for i in [
    #                 ['lang.ACCEPT', 'btn_accept', 'primary'],
    #                 ['lang.GO_BACK', 'btn_go_back', 'danger'],]
    #         ],
    #         onclick=lambda value: button_actions(value),)

def fix_tempo_page(nbs_data: tuple[Header, list, list,]):
    lang = translate.FixTempoPage
    header = nbs_data[0]

    def button_actions(value):
        match value:
            case 'btn_accept':
                header.tick_delay = pin.new_tempo
                edit_header_page(nbs_data)
            case 'btn_go_back':
                upload_page()
    
    with use_scope('title', clear=True):
        put_markdown(lang.UNSUPPORTED_TEMPO)
    
    with use_scope('content', clear=True):
        put_markdown(lang.NO_WORRIES)
    
    with use_scope('inputs', clear=True):
        put_select(
            name='new_tempo',
            label=lang.PICK_TEMPO,
            help_text=f'Исходный темп {header.old_tempo} t/s',
            options=[  
                dict(label=str(tempo)+r' t/s', value=i+1,
                     selected=(i+1 == header.tick_delay or i == 0))
                    for i, tempo in enumerate(TEMPO)],).style(STYLE_MARGIN_TOP)
        put_buttons(
            [  
                dict(label=i[0], value=i[1], color=i[2])
                for i in [
                    [lang.ACCEPT, 'btn_accept', 'primary'],
                    [lang.GO_BACK, 'btn_go_back', 'danger'],]
            ],
            onclick=lambda value: button_actions(value),).style(STYLE_MARGIN_TOP)

def edit_header_page(nbs_data: tuple[Header, list, list,]):
    lang = translate.EditHeaderPage
    loop_max = 128
    author_max = 24
    name_max = 36
    header = nbs_data[0]
    author_last_pressed = header.author

    def help_form_by_number(number: int) -> str:
        forms = ['символ', 'символа', 'символов']
        
        if number == 1:
            return forms[0]
        elif 11 <= number % 100 <= 19:
            return forms[2]
        elif number % 10 == 1:
            return forms[0]
        elif 2 <= number % 10 <= 4:
            return forms[1]
        else:
            return forms[2]

    def change_author_buttons():
        nonlocal author_last_pressed

        if pin.inp_author == header.old_author:
            with use_scope('input_author_btns', clear=True):
                put_buttons(
                    [  
                        dict(label=i[0], value=i[1], color=i[2])  
                        for i in [
                            ['Song author', 'use_song_author', 'light'],
                            ['Original song author', 'use_origin_author', 'secondary'],
                        ]  
                    ],
                    onclick=lambda value: button_actions(value),)
        elif pin.inp_author == header.old_original:
            with use_scope('input_author_btns', clear=True):
                put_buttons(
                    [  
                        dict(label=i[0], value=i[1], color=i[2])  
                        for i in [
                            ['Song author', 'use_song_author', 'secondary'],
                            ['Original song author', 'use_origin_author', 'light'],
                        ]  
                    ],
                    onclick=lambda value: button_actions(value),)
        else:
            if not author_last_pressed is None:
                author_last_pressed = None
                with use_scope('input_author_btns', clear=True):
                    put_buttons(
                        [  
                            dict(label=i[0], value=i[1], color=i[2])  
                            for i in [
                                ['Song author', 'use_song_author', 'secondary'],
                                ['Original song author', 'use_origin_author', 'secondary'],
                            ]  
                        ],
                        onclick=lambda value: button_actions(value),)

    def check_author():
        if not pin.inp_author is None:
            if len(pin.inp_author) > author_max:
                pin.inp_author = pin.inp_author[:author_max]
            header.author = sub(r'\s+', ' ', pin.inp_author.strip(),)
        change_author_buttons()
    
    def check_name():
        if not pin.inp_name is None:
            if len(pin.inp_name) > name_max:
                pin.inp_name = pin.inp_name[:name_max]
            header.name = sub(r'\s+', ' ', pin.inp_name.strip(),)
    
    def check_loop_count():
        if not pin.inp_loop_count is None:
            if pin.inp_loop_count < 0:
                pin.inp_loop_count = 0
            if pin.inp_loop_count > loop_max:
                pin.inp_loop_count = loop_max
            header.loop_count = pin.inp_loop_count

    def check_loop_start():
        if not pin.inp_loop_start is None:
            if pin.inp_loop_start < 0:
                pin.inp_loop_start = 0
            if pin.inp_loop_start > header.length:
                pin.inp_loop_start = header.length
            header.loop_start = pin.inp_loop_start

    def toggle_loop():
        if pin.rad_looping:
            header.loop = True
            with use_scope('input_looping_rad', clear=True):
                put_input(
                    name='inp_loop_count', label='Количество повторов',
                    help_text=f'0 - бесконечно. Максимум {loop_max} (а зачем больше?)',
                    type=NUMBER, value=header.loop_count).style(STYLE_MARGIN_TOP)
                pin_on_change(
                    'inp_loop_count', onchange=lambda _: check_loop_count(),
                    clear=True, init_run=True,)
                put_buttons(
                    [  
                        dict(label=i[0], value=i[1], color=i[2])  
                        for i in [
                            ['-', 'btn_loop_count_minus', 'danger'],
                            ['+', 'btn_loop_count_plus', 'success'],
                            ['По умолчанию', 'btn_loop_count_def', 'warning'],]  
                    ],
                    onclick=lambda value: button_actions(value), outline=True,)
                
                put_input(
                    name='inp_loop_start', label='Тик начала повтора',
                    help_text=f'Максимум {header.length}',
                    type=NUMBER, value=header.loop_start).style(STYLE_MARGIN_TOP)
                pin_on_change(
                    'inp_loop_start', onchange=lambda _: check_loop_start(),
                    clear=True, init_run=True,)
                put_buttons(
                    [  
                        dict(label=i[0], value=i[1], color=i[2])  
                        for i in [
                            ['-', 'btn_loop_start_minus', 'danger'],
                            ['+', 'btn_loop_start_plus', 'success'],
                            ['По умолчанию', 'btn_loop_start_def', 'warning']]  
                    ],
                    onclick=lambda value: button_actions(value), outline=True,)
        else:
            header.loop = False
            clear('input_looping_rad')

    def button_actions(value):
        nonlocal author_last_pressed
        match value:
            case 'btn_loop_count_minus':
                pin.inp_loop_count -= 1
                check_loop_count()
            case 'btn_loop_count_plus':
                pin.inp_loop_count += 1
                check_loop_count()
            case 'btn_loop_count_def':
                pin.inp_loop_count = header.old_loop_count
                check_loop_count()

            case 'btn_loop_start_minus':
                pin.inp_loop_start -= 1
                check_loop_start()
            case 'btn_loop_start_plus':
                pin.inp_loop_start += 1
                check_loop_start()
            case 'btn_loop_start_def':
                pin.inp_loop_start = header.old_loop_start
                check_loop_count()

            case 'use_song_author':
                if author_last_pressed == header.old_original or author_last_pressed is None:
                    author_last_pressed = header.old_author
                    pin.inp_author = header.author = header.old_author
                    check_author()
            case 'use_origin_author':
                if author_last_pressed == header.old_author or author_last_pressed is None:
                    author_last_pressed = header.old_original
                    pin.inp_author = header.author = header.old_original
                    check_author()
            
            case 'btn_name_def':
                pin.inp_name = header.old_name
                check_name()
                    
            case 'btn_go_overview':
                overview_page(nbs_data)
            case 'btn_go_back':
                if header.old_tempo in TEMPO:
                    upload_page()
                else:
                    fix_tempo_page(nbs_data)

    with use_scope('title', clear=True):
        put_markdown('# Подготовка к публикации')
    
    with use_scope('content', clear=True):
        put_markdown('### Здесь вы можете изменить параметры заголовка трека')

    with use_scope('inputs', clear=True):
        put_input(
            'inp_author', label='Исполнитель / Группа', value=header.author, type=TEXT,
            help_text=f'Максимум {author_max} {help_form_by_number(author_max)}',).style(STYLE_MARGIN_TOP)
        put_markdown('Взять значение из:')
        put_scope('input_author_btns', scope='inputs')
        change_author_buttons()
        pin_on_change(
            'inp_author', onchange=lambda _: check_author(),
            clear=True, init_run=True,)
        
        
            
        put_input(
            'inp_name', label='Название трека', value=header.name, type=TEXT,
            help_text=f'Максимум {name_max} {help_form_by_number(name_max)}',).style(STYLE_MARGIN_TOP)
        pin_on_change(
            'inp_name', onchange=lambda _: check_name(),
            clear=True, init_run=True,)
        put_buttons(
            [  
                dict(label=i[0], value=i[1], color=i[2])  
                for i in [
                    ['По умолчанию', 'btn_name_def', 'warning']]  
            ],
            onclick=lambda value: button_actions(value), outline=True,)

        if header.old_loop:
            put_markdown("""
                #### Было обнаружено, что трек использует повторы (looping)
            """)
            put_radio(
                name='rad_looping',
                options=[
                    {
                        "label": 'Проигрывать один раз',
                        "value": False,
                        "selected": True,
                    },
                    {
                        "label": 'Повторять',
                        "value": True,
                    },
                ], 
                inline=True,)
            
            put_scope('input_looping_rad')
            
            pin_on_change(
                'rad_looping', onchange=lambda _: toggle_loop(),
                clear=True, init_run=True,)
            
        put_buttons(
            [  
                dict(label=i[0], value=i[1], color=i[2])  
                for i in [
                    ['Продолжить', 'btn_go_overview', 'primary'],
                    ['Назад', 'btn_go_back', 'danger'],
                ]  
            ],
            onclick=lambda value: button_actions(value),).style(STYLE_MARGIN_TOP)

def overview_page(nbs_data: tuple[Header, list, list,]):
    lang = translate.OverviewPage

    def button_actions(value):
        match value:
            case 'btn_go_back':
                edit_header_page(nbs_data)

    with use_scope('title', clear=True):
        put_markdown('# OVERVIEW')
    
    with use_scope('content', clear=True):
        put_markdown('Пожалуйста, подождите')
    
    with use_scope('inputs', clear=True):
        put_buttons(
            [  
                dict(label=i[0], value=i[1], color=i[2])  
                for i in [
                    ['Назад', 'btn_go_back', 'danger'],
                ]  
            ],
            onclick=lambda value: button_actions(value),).style(STYLE_MARGIN_TOP)

def parse_nbs_page(nbs_data: tuple[Header, list, list,]):
    with use_scope('title', clear=True):
        put_markdown('# Отправка трек в GitHub')
    
    with use_scope('content', clear=True):
        put_markdown('Пожалуйста, подождите')
    
    with use_scope('inputs', clear=True):
        put_loading(shape='border', color='primary')
    
    header = nbs_data[0]
    notes = nbs_data[1]
    layers = nbs_data[2]

    note_seq = parse(
        header.song_length, TEMPO.index(header.tempo) + 1, layers, notes)

    sepparated = sepparate_data(note_seq)
    
    req_headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {GISTS_ACCESS_TOKEN}',
        'X-GitHub-Api-Version': '2022-11-28'
    }

    req_content = {
        'description': header.song_author + header.song_name,
        'public': True,
        'files': {
            'header.json': {
                'content': 'empty'
            }
        }
    }

    response = requests.post(
        url=URL, headers=req_headers, data=json.dumps(req_content)
    )

    print(response.status_code)
    
    if response.status_code == 201:
        gist_id = '/' + response.json()['id']
        gist_raw_url = response.json()['files']['header.json']['raw_url'][:-11]

        req_content = {
            'files': {},
        }

        for element in sepparated:
            content = json.dumps(element, separators=(',', ':'))
            
            req_content['files'].update(
                {
                    f'track_{sepparated.index(element)}.json': {
                        'content': content,
                    }
                }
            )
        
        response = requests.patch(
            url=URL + gist_id, headers=req_headers, data=json.dumps(req_content)
        )

        print(response.status_code)

        if response.status_code == 200:
            links = []
            for i in range(len(sepparated)):
                links.append(gist_raw_url + 'track_' + str(i) + '.json')

            track_header = [
                header.song_author,
                header.song_name,
                header.loop,
                header.max_loop_count,
                header.loop_start,
                links,
            ]

            req_content = {
                'files': {
                    'header.json': {
                        'content': json.dumps(track_header)
                    }
                },
            }

            response = requests.patch(
                url=URL + gist_id, headers=req_headers, 
                data=json.dumps(req_content)
            )

            print(response.status_code)

            if response.status_code == 200:
                with use_scope('inputs', clear=True):
                    popup(title='Трек добавлен!', content=[
                        put_buttons(['OK'], onclick=lambda _: close_popup()),
                        put_textarea(
                            name='text',
                            value=response.json()['files']['header.json']['raw_url'],),
                    ])

    
    # response = requests.post(
    #     url=URL, headers=headers, data=json.dumps(new_content)
    # )
    
    # with use_scope('inputs', clear=True):
    #     if response.status_code == 201:
    #         popup(title='Трек добавлен!', content=[
    #             put_buttons(['OK'], onclick=lambda _: close_popup()),
    #             put_textarea(
    #                 name='text',
    #                 value=response.json()['files']['header.json']['raw_url'],),
    #         ])
    #     else:
    #         popup('Ошибка!', [
    #             put_buttons(['Не OK :с'], onclick=lambda _: close_popup()),
    #             put_markdown(str(response.status_code))
    #         ])

def publish_page(SOME_PARSED_DATA): # FIXME
    pass

def show_published_track():
    pass

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

# def upload_data(uploaded_nbs):
#     # popup(title='Размер файла', content=str(len(fileobj['content']),),)
#     show_lyrics_input()
    

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
    