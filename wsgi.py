from pywebio.platform.flask import webio_view
from flask import Flask
from pywebio_app import main

app = Flask(__name__)

app.add_url_rule(
    '/', 'webio_view', webio_view(main),
    methods=['GET', 'POST', 'OPTIONS']
)

if __name__ == "__main__":
    app.run(port=8000)