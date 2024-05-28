# Released under the MIT License. See LICENSE for details.
#
"""Flask WSGI."""

# import logging

from pywebio.platform.flask import webio_view, send_from_directory
from flask import Flask
from pywebio_app import main

app = Flask(__name__)

# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

@app.route('/fonts/<path:filename>')
def serve_fonts(filename):
    return send_from_directory('fonts', filename)

app.add_url_rule(
    '/', 'webio_view', webio_view(main),
    methods=['GET', 'POST', 'OPTIONS']
)

if __name__ == '__main__':
    app.run(port=8000, debug=False)