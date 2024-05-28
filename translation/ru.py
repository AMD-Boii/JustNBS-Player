# Released under the MIT License. See LICENSE for details.
#
"""Русская локализация."""


class Global:
    ARE_YOU_SURE = r'Вы уверены?'
    WILL_LOSE_EVERYTHING = r'Все изменения будут потеряны'

    B_IM_SURE = r'Отменить изменения'
    B_RETURN = r'Вернуться'
    B_CONTINUE = r'Продолжить'
    B_BACK = r'Назад'
    B_CANCEL = r'Отмена'
    B_GOTCHA = r'Понятно'


class Main:
    TAB_TITLE = r'JustNBS Плеер'
    LOGO = r'logo_ru.jpg'

    CONTACT_WITH_ME = """
        ### Свяжитесь с @AMD Boii в [Discord](https://discord.justmc.ru/) либо на сервере JustMC.
    """

    NO_JUSTNBS_GIST_ID = r'# ОТСУТСТВУЕТ JUSTNBS_GIST_ID В ПЕРЕМЕННЫХ СРЕДЫ' + CONTACT_WITH_ME
    WRONG_JUSTNBS_GIST_ID_FORMAT = r'# НЕВЕРНЫЙ ФОРМАТ ИЛИ ПОВРЕЖДЕН JUSTNBS_GIST_ID' + CONTACT_WITH_ME

    NO_GIST_ACCESS_TOKEN = r'# ОТСУТСТВУЕТ GIST_ACCESS_TOKEN В ПЕРЕМЕННЫХ СРЕДЫ' + CONTACT_WITH_ME
    WRONG_GIST_ACCESS_TOKEN_FORMAT = r'# НЕВЕРНЫЙ ФОРМАТ ИЛИ ПОВРЕЖДЕН GIST_ACCESS_TOKEN' + CONTACT_WITH_ME

    INVALID_GIST_ACCESS_TOKEN = r'# НЕДЕЙСТВИТЕЛЬНЫЙ GIST_ACCESS_TOKEN' + CONTACT_WITH_ME

    REACHED_API_LIMIT = """
        # ДОСТИГНУТ ЛИМИТ ЗАПРОСОВ К GITHUB API
        ### Вероятно, какая-то бяка решила нам нагадить 🤬
        ### Попробуйте вернуться позднее, когда GitHub сбросит часовой лимит
        ### Иначе, свяжитесь с @AMD Boii в [Discord](https://discord.justmc.ru/) либо на сервере JustMC
    """


class IndexPage(Global):
    LINK_COPIED = r'Ссылка скопирована в буфер обмена!'

    HOW_TO_USE_LINK = """
        /plot resourcepack add < ссылка >
    """

    WELCOME = r'# Добро пожаловать'

    ABOUT = 'О проекте'
    ABOUT_CONTENT = r"""
        Ссылка на ресурс пак с расширением октав
    """

    INSTALLING = r'Установка'
    INSTALLING_CONTENT = """
        Требования к .nbs файлу:
        • версия OpenNBS -- 3.10.0
        • использовать только стандартные звуки
    """

    REQS = r'Требования'
    REQS_CONTENT = """
        Требования к .nbs файлу:
        • версия OpenNBS -- 3.10.0
        • использовать только стандартные звуки
    """

    RECENT_TRACKS = r'Недавние треки'

    HELP = r'Помощь'
    HELP_CONTENT = """
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


class InputNicknamePage(Global):
    REFRESH_WARNING = r'Вы уверены, что хотите покинуть эту страницу?'

    NICK_IS_SHORT = r'Слишком короткий никнейм'

    LETS_BEGIN = r'# Приступим'

    NICKS_REQIRED_BECAUSE = r'### Ваш никнейм требуется для помещения трека в актуальный плейлист после проверки'
    
    ENTER_YOUR_NAME = r'Введите Ваш Minecraft никнейм'
    
    NICK_INPUT_REQS = r'Минимум MIN / Максимум MAX / Символы 0-9 a-z A-Z _'


class UploadPage(Global):
    CHOOSE_FILE = r'# Выберите файл для загрузки'

    UPLOAD_RULES = r'правила загрузки'

    PICK_A_FILE_FIRST = r'Для начала, выберите файл'

    ALREADY_UPLOADED = r'Уже загружен:'

    NOT_UPLOADED = r'Файл ещё не загружен'
    
    MAX_SIZE = r'Максимальный размер файла - MAX КБ'

    REACHED_LIMIT = r'Превышен загрузочный лимит!'

    DONT_WASTE_TRAFFIC = r'Не надо тратить трафик впустую!'

    WRONG_FILE = r'Неверный или поврежденный файл'


class FixTempoPage(Global):
    UNSUPPORTED_TEMPO = r'# Трек имеет неподдерживаемый темп!'

    NO_WORRIES = """
        ### Не беда! Вы можете изменить темп прямо здесь!
        Но лучше вернуться в OpenNBS и тщательно всё отредактировать...
        А пока, выберите максимально близкий к исходному темп.
    """

    PICK_TEMPO = r'Выберите новый темп'

    DEFAULT_TEMPO_IS = r'Исходный темп'


class EditHeaderPage(Global):
    B_DEFAULT = r'По умолчанию'



    pass


class OverviewPage:
    pass


class CheckDuplicatesPage:
    pass


class ParseNbsPage:
    pass
