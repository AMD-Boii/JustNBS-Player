# Released under the MIT License. See LICENSE for details.
#
"""English locatization."""

class Main:
    LOGO = r'logo_en.jpg'

    NO_JUSTNBS_GIST_ID = r'# MISSING JUSTNBS_GIST_ID IN ENVIRONMENT VARIABLES'

    NO_PLAYLIST_RAW = r'# MISSING PLAYLIST_RAW IN ENVIRONMENT VARIABLES'

    NO_LATESTS_RAW = r'# MISSING LATESTS_RAW IN ENVIRONMENT VARIABLES'

    NO_GITHUB_TOKEN = r'# MISSING GITHUB_TOKEN IN ENVIRONMENT VARIABLES'

    WRONG_GITHUB_TOKEN_FORMAT = r'# INVALID OR CORRUPT GITHUB_TOKEN FORMAT'


class IndexPage:
    LINK_COPIED = r'Link copied to clipboard!'

    WELCOME = r'# Welcome'

    ABOUT = r'About the project'
    ABOUT_CONTENT = r"""
        Link to the resource pack with octave extension
    """

    INSTALLING = r'Installation'
    INSTALLING_CONTENT = r"""
        Requirements for the .nbs file:
        • OpenNBS version -- 3.10.0
        • Use only standard sounds
    """

    REQS = r'Requirements'
    REQS_CONTENT = r"""
        Requirements for the .nbs file:
        • OpenNBS version -- 3.10.0
        • Use only standard sounds
    """

    RECENT_TRACKS = r'Recent tracks'

    HELP = r'Help'
    HELP_CONTENT = r"""
        A short guide to creating a melody:
        • Download and install Open Note Block Studio 3.10.0
    """

    # Buttons
    B_GHUB_REPO = r'GitHub repository'
    B_RES_LINK = r'Resource pack'
    B_REFRESH = r'Refresh'
    B_DOWN_ONBS = r'Download OpenNBS'
    B_UPLOAD = r'Upload track'
    B_SEARCH = r'Search tracks'


class UploadPage:
    REFRESH_WARNING = r'Are you sure you want to leave this page?'
    
    CHOOSE_FILE = r'# Choose a file to upload'

    UPLOAD_RULES = r'upload rules'

    # Upload
    PLACEHOLDER = r'Choose an NBS file to upload'
    HELP_TEXT = r'hello'

    # Buttons
    UPLOAD = r'Upload'
    CANCEL = r'Cancel'

class EditTempoPage:
    UNSUPPORTED_TEMPO = r'# NBS has an unsupported tempo!'

    ITS_OK = r"""
        No worries! You can change the tempo right here!
        But it’s better to go back to OpenNBS and edit it carefully...
        Choose the tempo closest to the original.
    """

    # Select
    PICK_TEMPO = r'Choose a supported tempo (original tempo TEMPO t/s)'

    # Buttons
    ACCEPT = r'Confirm'
    CANCEL = r'Cancel'
