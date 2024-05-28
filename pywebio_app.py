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
from sys import getsizeof

from io import BytesIO

import json

from nbs_parser import (
    TEMPO, Header, get_nbs_data, parse_nbs, get_duration_string,)


try:
    JUSTNBS_GIST_ID = environ['JUSTNBS_GIST_ID']
    try:
        REQ_HEADERS = {
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {environ['GIST_ACCESS_TOKEN']}',
            'X-GitHub-Api-Version': '2022-11-28',}
        API_URL = 'https://api.github.com/gists'
        RAW_URL = 'https://gist.githubusercontent.com'
    except:
        REQ_HEADERS = None
except:
    JUSTNBS_GIST_ID = None

GITHUB_USER: str

STYLE_MARGIN_TOP = r'margin-top:20px;'


total_uploaded: int = 0


def get_noun_form(number: int, forms: Optional[tuple[str, str, str]] = None) -> str:
    if forms is None:
        forms = ('символ', 'символа', 'символов')
    if number == 1:
        return f'{number} {forms[0]}'
    elif 11 <= number % 100 <= 19:
        return f'{number} {forms[2]}'
    elif number % 10 == 1:
        return f'{number} {forms[0]}'
    elif 2 <= number % 10 <= 4:
        return f'{number} {forms[1]}'
    else:
        return f'{number} {forms[2]}'

@config(theme='dark')
def main():
    global translate

    if session_info.user_language == 'ru':
        import translation.ru as translate
    else:
        import translation.en as translate

    # ЗАГЛУШКА ДЛЯ РАЗРАБОТКИ
    import translation.ru as translate

    LANG = translate.Main

    def check_token():
        global GITHUB_USER
        LANG = translate.Main

        test_token = get_req(url=f'{API_URL[:-5]}user', headers=REQ_HEADERS)

        if test_token.status_code == 403:
            remove('title')
            remove('content')
            remove('inputs')
            put_markdown(LANG.REACHED_API_LIMIT)
        elif test_token.status_code != 200:
            remove('title')
            remove('content')
            remove('inputs')
            put_markdown(LANG.INVALID_GIST_ACCESS_TOKEN)
        else:
            GITHUB_USER = test_token.json()['login']
    
    set_env(title=LANG.TAB_TITLE)
    # run_js("$('head link[rel=icon]').attr('href', image_url)", 
    #        image_url="https://www.python.org/static/favicon.ico")
    
    put_scope('image', position=0,)
    put_scope('title', position=1,)
    put_scope('content', position=2,)
    put_scope('inputs', position=3,)
    put_scope('latest_tracks', position=4,)

    if JUSTNBS_GIST_ID is None:
        put_markdown(LANG.NO_JUSTNBS_GIST_ID)
    elif not bool(fullmatch(r'[0-9a-f]{32}', JUSTNBS_GIST_ID),):
        put_markdown(LANG.WRONG_JUSTNBS_GIST_ID_FORMAT)

    elif REQ_HEADERS is None:
        put_markdown(LANG.NO_GIST_ACCESS_TOKEN)
    elif not bool(
            fullmatch(r'[0-9a-zA-Z]{36}', REQ_HEADERS['Authorization'][-36:]),
        ) and not (
            REQ_HEADERS['Authorization'][-40:][:4] == 'ghp_'
        ):
        put_markdown(LANG.WRONG_GIST_ACCESS_TOKEN_FORMAT)
    else:
        try:
            with use_scope('image', clear=True,):
                put_image(
                    open(path.join('resources', None,), 'rb').read(),)
                # put_image(
                #     open(path.join('resources', LANG.LOGO,), 'rb').read(),)
        except:
            with use_scope('image', clear=True,):
                put_markdown('# NO_IMAGE')
        index_page()
        check_token()
    
def index_page(nickname: str = ''):
    LANG = translate.IndexPage

    global total_uploaded
    total_uploaded = 0

    run_js(r"window.onbeforeunload = null")
    close_popup()

    def show_latests(): # TODO
        pass

    def button_actions(action: str):
        nonlocal nickname
        match action:
            case 'btn_go_inp_nick':
                input_nickname_page(nickname)
            case 'btn_res_pack':
                run_js(r"""
                navigator.clipboard.writeText(
                "https://gitlab.com/-/snippets/3710689/raw/main/EXTENDED_1.13.zip"
                ).then(function() {}, function(err) {
                    console.error('Could not copy text: ', err);
                });
                """)
                popup(LANG.LINK_COPIED, [
                    put_markdown(LANG.HOW_TO_USE_LINK),
                    put_buttons(
                        [
                            dict(label=i[0], value=i[1], color=i[2])  
                            for i in [
                                [LANG.B_GOTCHA, 'btn_gotcha', 'primary'],]
                        ], 
                        onclick=lambda _: close_popup(),)
                ])
            case 'btn_onbs_dwnld':
                run_js(r"""
                window.open(
                "https://github.com/OpenNBS/OpenNoteBlockStudio/releases/latest")
                """)
            case 'btn_github_repo':
                run_js(r"""
                window.open("https://github.com/AMD-Boii/JustNBS-Player")
                """)
            case 'btn_go_search':
                index_page()
    
    with use_scope('title', clear=True):
        put_markdown(LANG.WELCOME)
    
    with use_scope('content', clear=True):
        put_tabs(
            tabs=[
            {
                'title': LANG.ABOUT,
                'content': [
                    put_markdown(LANG.ABOUT_CONTENT),
                    put_buttons(
                        [  
                            dict(label=i[0], value=i[1], color=i[2])  
                            for i in [
                                [LANG.B_GHUB_REPO, 'btn_github_repo', 'info'],]  
                        ],
                        onclick=lambda action: button_actions(action),),
                ],
            },
            {
                'title': LANG.INSTALLING,
                'content': [
                    put_markdown(LANG.INSTALLING_CONTENT),
                    put_buttons(
                        [  
                            dict(label=i[0], value=i[1], color=i[2])  
                            for i in [
                                [LANG.B_RES_LINK, 'btn_res_pack', 'info'],]  
                        ],
                        onclick=lambda action: button_actions(action),),
                ],
            },
            {
                'title': LANG.REQS,
                'content': [
                    put_markdown(LANG.REQS_CONTENT),],
            },
            {
                'title': LANG.RECENT_TRACKS,
                'content': [
                    put_markdown('# TODO вывод последних'), #TODO
                    put_buttons(
                        [  
                            dict(label=i[0], value=i[1], color=i[2])  
                            for i in [
                                [LANG.B_REFRESH, 'btn_refresh_recent', 'info'],]  
                        ],
                        onclick=lambda action: button_actions(action),),
                ],
            },
            {
                'title': LANG.HELP,
                'content': [
                    put_markdown(LANG.HELP_CONTENT),
                    put_buttons(
                        [  
                            dict(label=i[0], value=i[1], color=i[2])  
                            for i in [
                                [LANG.B_DOWN_ONBS, 'btn_onbs_dwnld', 'danger'],]  
                        ],
                        onclick=lambda action: button_actions(action),),
                ],
            },],
        )
    
    with use_scope('inputs', clear=True,):
        put_buttons(
            [  
                dict(label=i[0], value=i[1], color=i[2])  
                for i in [
                    [LANG.B_UPLOAD, 'btn_go_inp_nick', 'primary'],
                    [LANG.B_SEARCH, 'btn_go_search', 'primary'],]  
            ],
            onclick=lambda action: button_actions(action),)

def input_nickname_page(nickname: str, upload: Optional[dict] = None,
                        nbs_data: Optional[tuple[Header, list, list,],] = None):
    LANG = translate.InputNicknamePage

    NICKNAME_MIN = 3
    NICKNAME_MAX = 16

    run_js(r"""
    window.onbeforeunload = function() {
        return "WARNING";
    }
    """.replace('WARNING', LANG.REFRESH_WARNING),)

    def check_nickname():
        nonlocal nickname
        if not pin.inp_nickname is None:
            pin.inp_nickname = sub(r'[^0-9a-zA-Z_]', '', pin.inp_nickname)
            if len(pin.inp_nickname) > NICKNAME_MAX:
                pin.inp_nickname = pin.inp_nickname[:NICKNAME_MAX]
            nickname = pin.inp_nickname

    def button_actions(action: str):
        nonlocal upload
        nonlocal nickname
        nonlocal nbs_data
        match action:
            case 'btn_continue':
                if len(nickname) < NICKNAME_MIN:
                    toast(
                        content=LANG.NICK_IS_SHORT,
                        duration=3, color='red',)
                else:
                    upload_page(nbs_data, nickname, upload)
            case 'btn_cancel':
                if not upload is None:
                    popup(LANG.ARE_YOU_SURE, [
                        put_markdown(LANG.WILL_LOSE_EVERYTHING),
                        put_buttons(
                            [
                                dict(label=i[0], value=i[1], color=i[2])  
                                for i in [
                                    [LANG.B_IM_SURE, 'btn_sure', 'danger'],
                                    [LANG.B_RETURN, 'btn_return', 'primary'],]
                            ], 
                            onclick=lambda value: button_actions(value),)
                    ])
                else:
                    index_page(nickname)
            case 'btn_sure':
                index_page(nickname)
            case 'btn_return':
                close_popup()
    
    with use_scope('title', clear=True):
        put_markdown(LANG.LETS_BEGIN)
    
    with use_scope('content', clear=True):
        put_markdown(LANG.NICKS_REQIRED_BECAUSE)
    
    with use_scope('inputs', clear=True,):
        put_input(
            'inp_nickname', label=LANG.ENTER_YOUR_NAME,
            value=nickname, type=TEXT,
            help_text=str(
                LANG.NICK_INPUT_REQS.replace(
                    'MIN', get_noun_form(NICKNAME_MIN),),).replace(
                        'MAX', get_noun_form(NICKNAME_MAX),)
        ).style(STYLE_MARGIN_TOP)
        pin_on_change(
            'inp_nickname', onchange=lambda _: check_nickname(),
            clear=True, init_run=True,)
        
        put_buttons(
            [  
                dict(label=i[0], value=i[1], color=i[2])  
                for i in [
                    [LANG.B_CONTINUE, 'btn_continue', 'primary'],
                    [LANG.B_CANCEL, 'btn_cancel', 'danger'],]  
            ],
            onclick=lambda value: button_actions(value),).style(STYLE_MARGIN_TOP)

def upload_page(nbs_data: Optional[tuple[Header, list, list,],],
                nickname: str, upload: Optional[dict],):
    LANG = translate.UploadPage

    MAX_SIZE = 256 # KB
    MAX_SUMMARY = 1048576 # 1 MB

    def go_further():
        nonlocal upload
        nonlocal nbs_data
        if nbs_data is None:
            nbs_data = get_nbs_data(BytesIO(upload['content']),)
        if isinstance(nbs_data, str):
            toast(
                content=LANG.WRONG_FILE,
                duration=3, color='red',)
        elif not nbs_data[0].old_tempo in TEMPO:
            fix_tempo_page(nbs_data, nickname, upload)
        else:
            edit_header_page(nbs_data, nickname, upload)

    def button_actions(value):
        global total_uploaded
        nonlocal upload
        nonlocal nbs_data
        match value:
            case 'btn_continue':
                if total_uploaded > MAX_SUMMARY:
                    popup(LANG.REACHED_LIMIT, [
                        put_markdown(LANG.DONT_WASTE_TRAFFIC),
                        put_buttons(
                            [
                                dict(label=i[0], value=i[1], color=i[2])  
                                for i in [
                                    [LANG.B_GOTCHA, 'btn_gotcha', 'primary'],]
                            ], 
                            onclick=lambda _: index_page(nickname),),])
                else:
                    if upload is None:
                        upload = pin.uploaded_file
                        if upload is None:
                            toast(
                                content=LANG.PICK_A_FILE_FIRST,
                                duration=3, color='info',)
                        else:
                            nbs_data = get_nbs_data(BytesIO(upload['content']),)
                            total_uploaded += getsizeof(upload['content'])
                            go_further()
                    else:
                        new_upload = pin.uploaded_file
                        if not new_upload is None:
                            nbs_data = get_nbs_data(BytesIO(upload['content']),)
                            total_uploaded += getsizeof(upload['content'])
                            upload = new_upload
                        go_further()
            case 'btn_back':
                input_nickname_page(nickname, upload, nbs_data)
            case 'btn_cancel':
                if not upload is None:
                    popup(LANG.ARE_YOU_SURE, [
                        put_markdown(LANG.WILL_LOSE_EVERYTHING),
                        put_buttons(
                            [
                                dict(label=i[0], value=i[1], color=i[2])  
                                for i in [
                                    [LANG.B_IM_SURE, 'btn_sure', 'danger'],
                                    [LANG.B_RETURN, 'btn_return', 'primary'],]
                            ], 
                            onclick=lambda value: button_actions(value),),])
                else:
                    index_page(nickname)
            case 'btn_sure':
                index_page(nickname)
            case 'btn_return':
                close_popup()

    with use_scope('title', clear=True,):
        put_markdown(LANG.CHOOSE_FILE)
    
    with use_scope('content', clear=True,):
        put_markdown(LANG.UPLOAD_RULES)
    
    with use_scope('inputs', clear=True,):
        put_file_upload(
            name='uploaded_file',
            label='Загрузите',
            accept='.nbs',
            max_size=f'{MAX_SIZE}K',
            placeholder=f'{LANG.ALREADY_UPLOADED} {upload['filename']}' if (
                not upload is None) else LANG.NOT_UPLOADED,
            help_text=LANG.MAX_SIZE.replace('MAX', str(MAX_SIZE)),
        ).style(STYLE_MARGIN_TOP)
        put_buttons(
            [  
                dict(label=i[0], value=i[1], color=i[2])  
                for i in [
                    [LANG.B_CONTINUE, 'btn_continue', 'primary'],
                    [LANG.B_BACK, 'btn_back', 'warning'],
                    [LANG.B_CANCEL, 'btn_cancel', 'danger'],]  
            ],
            onclick=lambda value: button_actions(value),).style(STYLE_MARGIN_TOP)
        # pin_wait_change('uploaded_file')

def custom_instuments_page(nbs_data: tuple[Header, list, list,], # TODO
                           nickname: str): 
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
    #                 ['LANG.ACCEPT', 'btn_accept', 'primary'],
    #                 ['LANG.GO_BACK', 'btn_go_back', 'danger'],]
    #         ],
    #         onclick=lambda value: button_actions(value),)

def fix_tempo_page(nbs_data: tuple[Header, list, list,],
                   nickname: str, upload: dict):
    LANG = translate.FixTempoPage

    header = nbs_data[0]

    def change_tempo(new_tempo: tuple[float, int]):
        header.tempo = new_tempo[0]
        header.tick_delay = new_tempo[1]
        header.duration = header.tick_delay*header.length//20
        header.duration_string = get_duration_string(header.duration)

    def button_actions(value):
        match value:
            case 'btn_continue':
                edit_header_page(nbs_data, nickname, upload)
            case 'btn_back':
                upload_page(nbs_data, nickname, upload)
            case 'btn_cancel':
                popup(LANG.ARE_YOU_SURE, [
                    put_markdown(LANG.WILL_LOSE_EVERYTHING),
                    put_buttons(
                        [
                            dict(label=i[0], value=i[1], color=i[2])  
                            for i in [
                                [LANG.B_IM_SURE, 'btn_sure', 'danger'],
                                [LANG.B_RETURN, 'btn_return', 'primary'],]
                        ], 
                        onclick=lambda value: button_actions(value),)
                ])
            case 'btn_sure':
                index_page(nickname)
            case 'btn_return':
                close_popup()
    
    with use_scope('title', clear=True):
        put_markdown(LANG.UNSUPPORTED_TEMPO)
    
    with use_scope('content', clear=True):
        put_markdown(LANG.NO_WORRIES)
    
    with use_scope('inputs', clear=True):
        put_select(
            name='sel_tempo',
            label=LANG.PICK_TEMPO,
            help_text='{} {:.2f} t/s'.format(LANG.DEFAULT_TEMPO_IS, 
                                             header.old_tempo),
            options=[  
                dict(label='{:.2f} t/s'.format(tempo), value=(tempo,i+1),
                     selected=(i+1 == header.tick_delay or i == 0))
                    for i, tempo in enumerate(TEMPO)],).style(STYLE_MARGIN_TOP)
        pin_on_change(
            'sel_tempo', onchange=lambda new_tempo: change_tempo(new_tempo),
            clear=True, init_run=True,)
        put_buttons(
            [  
                dict(label=i[0], value=i[1], color=i[2])
                for i in [
                    [LANG.B_CONTINUE, 'btn_continue', 'primary'],
                    [LANG.B_BACK, 'btn_back', 'warning'],
                    [LANG.B_CANCEL, 'btn_cancel', 'danger'],]
            ],
            onclick=lambda value: button_actions(value),).style(STYLE_MARGIN_TOP)

def edit_header_page(nbs_data: tuple[Header, list, list,], # TODO перевод FIXME оптимизировать
                     nickname: str, upload: dict): # размер кода вывода кнопок
    LANG = translate.EditHeaderPage

    LOOP_MAX = 10
    AUTHOR_MAX = 24
    NAME_MAX = 36

    header = nbs_data[0]
    author_last_pressed = header.author

    def change_author_buttons(): # FIXME
        nonlocal author_last_pressed
        if (header.old_author == header.old_original) or (
                header.old_author == '') or (
                    header.old_original == ''):
            remove('markdown')
            if not author_last_pressed is None:
                author_last_pressed = None
                with use_scope('input_author_btns', clear=True):
                    remove('markdown')
                    put_buttons(
                        [  
                            dict(label=i[0], value=i[1], color=i[2])  
                            for i in [
                                [LANG.B_DEFAULT, 'btn_author_def', 'warning'],]  
                        ],
                        onclick=lambda value: button_actions(value), outline=True,)
        else:
            if pin.inp_author == header.old_author:
                author_last_pressed = header.old_author
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
                author_last_pressed = header.old_original
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

    def check_author(): # FIXME обращение к pin каждый раз делает опросы
        if not pin.inp_author is None:
            if len(pin.inp_author) > AUTHOR_MAX:
                pin.inp_author = pin.inp_author[:AUTHOR_MAX]
            header.author = sub(r'\s+', ' ', pin.inp_author.strip(),)
        change_author_buttons()
    
    def check_name(): # FIXME обращение к pin каждый раз делает опросы
        if not pin.inp_name is None:
            if len(pin.inp_name) > NAME_MAX:
                pin.inp_name = pin.inp_name[:NAME_MAX]
            header.name = sub(r'\s+', ' ', pin.inp_name.strip(),)
    
    def check_loop_count(): # FIXME обращение к pin каждый раз делает опросы
        if not pin.inp_loop_count is None:
            if pin.inp_loop_count < 0:
                pin.inp_loop_count = 0
            if pin.inp_loop_count > LOOP_MAX:
                pin.inp_loop_count = LOOP_MAX
            header.loop_count = pin.inp_loop_count

    def check_loop_start(): # FIXME обращение к pin каждый раз делает опросы
        if not pin.inp_loop_start is None:
            if pin.inp_loop_start < 0:
                pin.inp_loop_start = 0
            if pin.inp_loop_start > header.length:
                pin.inp_loop_start = header.length
            header.loop_start = pin.inp_loop_start

    def toggle_loop(): # FIXME обращение к pin каждый раз делает опросы
        if pin.rad_looping:
            header.loop = True
            with use_scope('input_looping_rad', clear=True):
                put_input(
                    name='inp_loop_count', label=LANG.LOOP_COUNT,
                    help_text=f'{LANG.LOOP_COUNT_LIMITS} {LOOP_MAX}',
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
                            [LANG.B_DEFAULT, 'btn_loop_count_def', 'warning'],]  
                    ],
                    onclick=lambda value: button_actions(value), outline=True,)
                put_input(
                    name='inp_loop_start', label=LANG.LOOP_START,
                    help_text=f'{LANG.MAX} {header.length}',
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
                            [LANG.B_DEFAULT, 'btn_loop_start_def', 'warning']]  
                    ],
                    onclick=lambda value: button_actions(value), outline=True,)
        else:
            header.loop = False
            clear('input_looping_rad')

    def button_actions(value):
        nonlocal author_last_pressed
        nonlocal upload
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
                if (author_last_pressed == header.old_original) or (
                                                author_last_pressed is None):
                    pin.inp_author = header.author = header.old_author
                    check_author()
            case 'use_origin_author':
                if (author_last_pressed == header.old_author) or (
                                                author_last_pressed is None):
                    pin.inp_author = header.author = header.old_original
                    check_author()
            
            case 'btn_author_def':
                pin.inp_author = header.default_author
                check_author()
            case 'btn_name_def':
                pin.inp_name = header.old_name
                check_name()
                    
            case 'btn_continue':
                overview_page(nbs_data, nickname, upload)
            case 'btn_back':
                if header.old_tempo in TEMPO:
                    upload_page(nbs_data, nickname, upload)
                else:
                    fix_tempo_page(nbs_data, nickname, upload)
            case 'btn_cancel':
                popup(LANG.ARE_YOU_SURE, [
                    put_markdown(LANG.WILL_LOSE_EVERYTHING),
                    put_buttons(
                        [
                            dict(label=i[0], value=i[1], color=i[2])  
                            for i in [
                                [LANG.B_IM_SURE, 'btn_sure', 'danger'],
                                [LANG.B_RETURN, 'btn_return', 'primary'],]
                        ], 
                        onclick=lambda value: button_actions(value),)
                ])
            case 'btn_sure':
                index_page(nickname)
            case 'btn_return':
                close_popup()

    with use_scope('title', clear=True):
        put_markdown(LANG.PUBLISH_PREPARATION)
    
    with use_scope('content', clear=True):
        put_markdown(LANG.YOU_CAN_CHANGE_HEADER)

    with use_scope('inputs', clear=True):
        put_input(
            'inp_author', label=LANG.AUTHOR, value=header.author, type=TEXT,
            help_text=f'{LANG.MAX} {get_noun_form(AUTHOR_MAX)}',
        ).style(STYLE_MARGIN_TOP)

        put_scope('markdown')
        with use_scope('markdown', clear=True):
            put_markdown(LANG.TAKE_AUTHOR_VAL_FROM)
        
        put_scope('input_author_btns', scope='inputs')
        change_author_buttons()

        pin_on_change(
            'inp_author', onchange=lambda _: check_author(),
            clear=True, init_run=True,)   
         
        put_input(
            'inp_name', label=LANG.SONG_NAME, value=header.name, type=TEXT,
            help_text=f'{LANG.MAX} {get_noun_form(NAME_MAX)}',
        ).style(STYLE_MARGIN_TOP)
        pin_on_change(
            'inp_name', onchange=lambda _: check_name(),
            clear=True, init_run=True,)
        put_buttons(
            [  
                dict(label=i[0], value=i[1], color=i[2])  
                for i in [
                    [LANG.B_DEFAULT, 'btn_name_def', 'warning']]  
            ],
            onclick=lambda value: button_actions(value), outline=True,)

        if header.old_loop:
            put_markdown(LANG.LOOPING_DETECTED)
            put_radio(
                name='rad_looping',
                options=[
                    {
                        'label': LANG.NO_LOOPS,
                        'value': False,
                        'selected': not header.loop,
                    },
                    {
                        'label': LANG.USE_LOOPING,
                        'value': True,
                        'selected': header.loop,
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
                    [LANG.B_CONTINUE, 'btn_continue', 'primary'],
                    [LANG.B_BACK, 'btn_back', 'warning'],
                    [LANG.B_CANCEL, 'btn_cancel', 'danger'],
                ]  
            ],
            onclick=lambda value: button_actions(value),).style(STYLE_MARGIN_TOP)

def overview_page(nbs_data: tuple[Header, list, list,], 
                  nickname: str, upload: dict): # TODO
    LANG = translate.OverviewPage
    header = nbs_data[0]

    def button_actions(value):
        match value:
            # case 'btn_check_duplicates':
            #     check_duplicates_page(nbs_data, nickname)
            case 'btn_parse':
                parse_nbs_page(nbs_data, nickname)
            case 'btn_go_back':
                edit_header_page(nbs_data, nickname, upload)

    with use_scope('title', clear=True):
        put_markdown('# Предварительный просмотр')
    
    with use_scope('content', clear=True):
        put_markdown('### Убедитесь, что все параметры верны')
    
    with use_scope('inputs', clear=True):
        put_table([ 
            [put_markdown('### Исполнитель'), 
             put_markdown('### Название'), 
             put_markdown('### Длительность'), 
             put_markdown('### Темп'), 
             put_markdown('### Цикличность')],
            [header.author, 
             header.name, 
             header.duration_string, 
             '{:.2f} t/s'.format(header.tempo), 
             put_markdown('Повторы: {}\nСтарт: {}'.format(
                     '∞' if header.loop_count == 0 else header.loop_count, header.loop_start
                 ) if header.loop else '—')],
        ])

        overview_style = 'color:rgb(255,87,51); margin-top:0px; margin-bottom:0px;'

        put_html("""
            <style>
                @font-face {
                    font-family: 'Minecraftia';
                    src: url('/fonts/minecraftia_2.0.ttf') format('truetype');
                }
                .font {
                    font-family: 'Minecraftia', sans-serif;
                    font-size: 14px;
                    line-height: 1;
                }
                .italic {
                    font-style: italic;
                }
                .name-col {
                    color: #ff55ff;
                }
                .author-col {
                    color: #55ff55;
                }
                .duration-col {
                    color: #555555;
                }
                .looped-col {
                    color: #aaaaaa;
                }
                .publisher-col {
                    color: #555555;
                }
                .auto-size {
                    width: auto;
                    height: auto;
                    display: inline-block;
                }
                .outer-frame {
                    background-color: black;
                    padding: 5px;
                }
                .inner-frame {
                    border: 2px solid #00008B;
                    padding: 10px
                    
                }
            </style>
            <div class="outer-frame auto-size">
                <div class="inner-frame auto-size">
                    <p class="font name-col">Bohemian Rhapsody</p>
                    <p class="font author-col">Queen</p>
                    <p>
                        <span class="font duration-col">5:47 </span>
                        <span class="font looped-col">LOOPED </span>
                        <span class="font duration-col">at 2:36 10 times</span>
                    </p>
                    <p class="font"></p>
                    <p class="font italic duration-col">By AMD_Boii</p>
                </div>
            </div>
        """)
        put_markdown('### Пример вывода в плейлист:')
        put_markdown(f'**{header.author} — {header.name}**').style(overview_style)
        put_markdown(f'**{header.duration_string}**').style(overview_style)
        if header.loop:
            put_markdown(f'**Loops: {'INFINITE' if header.loop_count == 0 else header.loop_count}**').style(overview_style)
            put_markdown(f'**Loop starts at: {header.loop_start}**').style(overview_style)
        put_markdown(f'**By: NICK_NAME**').style(overview_style)

        put_buttons(
            [  
                dict(label=i[0], value=i[1], color=i[2])  
                for i in [
                    ['К парсингу', 'btn_parse', 'primary'],
                    ['Назад', 'btn_go_back', 'danger'],
                ]  
            ],
            onclick=lambda value: button_actions(value),).style(STYLE_MARGIN_TOP)

def parse_nbs_page(nbs_data: tuple[Header, list, list,], 
                   nickname: str, check=None): # FIXME
    LANG = translate.ParseNbsPage
    header = nbs_data[0]
    notes = nbs_data[1]
    layers = nbs_data[2]

    with use_scope('title', clear=True):
        put_markdown('# Парсим NBS файл')
    
    with use_scope('content', clear=True):
        put_markdown('### Пожалуйста, подождите') 
    
    with use_scope('inputs', clear=True):
        put_loading(shape='border', color='primary')

    parsing_result = parse_nbs(length=header.length,
                                tick_delay=header.tick_delay,
                                notes=notes,
                                layers=layers,
                                loop_start=header.loop_start,
                                loop=header.loop)
    
    with use_scope('inputs', clear=True):
        if isinstance(parsing_result, str):
            put_markdown(parsing_result)
        else:
            file_amount = len(parsing_result)
            put_markdown(f'Ваш трек состоит из {file_amount} файлов')
            #publish_page(header, parsing_result)
        
    
    

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

def publish_page(header: Header, track_files: list[str]): # FIXME
    def button_actions(value, response):
        match value:
            case 'btn_go_index':
                index_page()
            case 'btn_url':
                run_js(r"""
                navigator.clipboard.writeText(
                "URL"
                ).then(function() {}, function(err) {
                    console.error('Could not copy text: ', err);
                });
                """.replace('URL', response.json()['files']['header.json']['raw_url']),)
                toast(
                    content='Скопировано',
                    duration=3, color='info',)
    
    with use_scope('title', clear=True):
        put_markdown('# Публикуем трек в плейлист')
    
    with use_scope('content', clear=True):
        put_markdown('### Пожалуйста, подождите')
        put_loading(shape='border', color='primary')
    
    with use_scope('inputs', clear=True):
        put_processbar('loading_bar', 0.5).style(STYLE_MARGIN_TOP)

    # req_content = {
    #     'description': header.song_author + header.song_name,
    #     'public': True,
    #     'files': {
    #         'header.json': {
    #             'content': 'empty'
    #         }
    #     }
    # }

    req_content = {
        'description': f'{header.author} — {header.name}',
        'public': False,
        'files': {},}

    track_dict = req_content['files']
    for i, track in enumerate(track_files):
        track_dict[f'track_{i}.json'] = {'content': track,}

    #try:
    response = post_req(
        url=API_URL, headers=REQ_HEADERS, 
        data=json.dumps(req_content, separators=(',', ':'),),)
    if response.status_code == 201:
        put_markdown('### РАБОТАЕТ')
        gist_id = response.json()['id']
        
        raws = []
        for url in response.json()['files']:
            raws.append(response.json()['files'][url]['raw_url'])

        req_content = {
            'files': {'header.json': {
                'content':json.dumps(raws, separators=(',', ':'),)},},}
        response = patch_req(
            url=f'{API_URL}/{gist_id}', headers=REQ_HEADERS, 
            data=json.dumps(req_content, separators=(',', ':'),),)
        
        if response.status_code == 200:
            with use_scope('inputs', clear=True,):
                put_buttons(
                    [  
                        dict(label=i[0], value=i[1], color=i[2])  
                        for i in [
                            ['Ссылка', 'btn_url', 'primary'],
                            ['Индекс', 'btn_go_index', 'primary'],]  
                    ],
                    onclick=lambda value: button_actions(value, response),)
        else:
            put_markdown('### ПОЛНЫЙ ОТВАЛ')
            print(response.json())
    else:
        put_markdown('### ПОЛНЫЙ ОТВАЛ')

    

    

    

    
    # except Exception as ex:
    #     print(ex.__str__(),)

    #print(response.status_code)
    
    

    #     req_content = {
    #         'files': {},
    #     }

    #     for element in sepparated:
    #         content = json.dumps(element, separators=(',', ':'))
            
    #         req_content['files'].update(
    #             {
    #                 f'track_{sepparated.index(element)}.json': {
    #                     'content': content,
    #                 }
    #             }
    #         )
        
    #     response = requests.patch(
    #         url=URL + gist_id, headers=req_headers, data=json.dumps(req_content)
    #     )

    #     print(response.status_code)

    #     if response.status_code == 200:
    #         links = []
    #         for i in range(len(sepparated)):
    #             links.append(gist_raw_url + 'track_' + str(i) + '.json')

    #         track_header = [
    #             header.song_author,
    #             header.song_name,
    #             header.loop,
    #             header.max_loop_count,
    #             header.loop_start,
    #             links,
    #         ]

    #         req_content = {
    #             'files': {
    #                 'header.json': {
    #                     'content': json.dumps(track_header)
    #                 }
    #             },
    #         }

    #         response = requests.patch(
    #             url=URL + gist_id, headers=req_headers, 
    #             data=json.dumps(req_content)
    #         )

    #         print(response.status_code)

    #         if response.status_code == 200:
    #             with use_scope('inputs', clear=True):
    #                 popup(title='Трек добавлен!', content=[
    #                     put_buttons(['OK'], onclick=lambda _: close_popup()),
    #                     put_textarea(
    #                         name='text',
    #                         value=response.json()['files']['header.json']['raw_url'],),
    #                 ])

    
    # response = requests.post(
    #     url=URL, headers=headers, data=json.dumps(new_content)
    # )

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
    