# Released under the MIT License. See LICENSE for details.
#
"""Русская локализация."""

class Main:
    TAB_TITLE = r'JustNBS Плеер'
    LOGO = r'logo_ru.jpg'

    NO_JUSTNBS_GIST_ID = r'# ОТСУТСТВУЕТ JUSTNBS_GIST_ID В ПЕРЕМЕННЫХ СРЕДЫ'
    WRONG_JUSTNBS_GIST_ID_FORMAT = r'# НЕВЕРНЫЙ ФОРМАТ ИЛИ ПОВРЕЖДЕН JUSTNBS_GIST_ID'

    NO_ACTUAL_PLAYLIST_RAW = r'# ОТСУТСТВУЕТ ACTUAL_PLAYLIST_RAW В ПЕРЕМЕННЫХ СРЕДЫ'
    WRONG_ACTUAL_PLAYLIST_RAW_FORMAT = r'# НЕВЕРНЫЙ ФОРМАТ ИЛИ ПОВРЕЖДЕН ACTUAL_PLAYLIST_RAW'

    NO_LATEST_TRACKS_RAW = r'# ОТСУТСТВУЕТ LATESTS_RAW В ПЕРЕМЕННЫХ СРЕДЫ'
    WRONG_LATEST_TRACKS_RAW_FORMAT = r'# НЕВЕРНЫЙ ФОРМАТ ИЛИ ПОВРЕЖДЕН LATESTS_RAW'

    NO_GITHUB_TOKEN = r'# ОТСУТСТВУЕТ GITHUB_TOKEN В ПЕРЕМЕННЫХ СРЕДЫ'
    WRONG_GITHUB_TOKEN_FORMAT = r'# НЕВЕРНЫЙ ФОРМАТ ИЛИ ПОВРЕЖДЕН GITHUB_TOKEN'


class IndexPage:
    LINK_COPIED = r'Ссылка скопирована в буфер обмена!'

    WELCOME = r'# Добро пожаловать'

    ABOUT = r'О проекте'
    ABOUT_CONTENT = r"""
        Ссылка на ресурс пак с расширением октав
    """

    INSTALLING = r'Установка'
    INSTALLING_CONTENT = r"""
        Требования к .nbs файлу:
        • версия OpenNBS -- 3.10.0
        • использовать только стандартные звуки
    """

    REQS = r'Требования'
    REQS_CONTENT = r"""
        Требования к .nbs файлу:
        • версия OpenNBS -- 3.10.0
        • использовать только стандартные звуки
    """

    RECENT_TRACKS = r'Недавние треки'

    HELP = r'Помощь'
    HELP_CONTENT = r"""
        Короткий гайд по созданию мелодии:
        • скачайте и установите Open Note Block Studio 3.10.0
    """

    # Buttons
    B_GHUB_REPO = r'GitHub репозиторий'
    B_RES_LINK = r'Ресурспак'
    B_REFRESH = r'Обновить'
    B_DOWN_ONBS = r'Скачать OpenNBS'
    B_UPLOAD = r'Опубликовать трек'
    B_SEARCH = r'Поиск треков'


class UploadPage:
    REFRESH_WARNING = r'Вы уверены, что хотите покинуть эту страницу?'

    CHOOSE_FILE = r'# Выберите файл для загрузки'

    UPLOAD_RULES = r'правила загрузки'

    # Upload
    PLACEHOLDER = r'Выбери NBS файл для загрузки'
    HELP_TEXT = r'hello'

    # Buttons
    UPLOAD = r'Загрузить'
    CANCEL = r'Отмена'

class EditTempoPage:
    UNSUPPORTED_TEMPO = r'# NBS имеет неподдерживаемый темп!'

    ITS_OK = r"""
        Не беда! Вы можете изменить темп прямо здесь!
        Но лучше вернуться в OpenNBS и тщательно его отредактировать...
        Выберите максимально близкий к исходному темп.
    """

    # Select
    PICK_TEMPO = r'Выберите поддерживаемый темп (исходный темп TEMPO t/s)'

    # Buttons
    ACCEPT = r'Подтвердить'
    CANCEL = r'Отмена'