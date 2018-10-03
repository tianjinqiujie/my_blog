from flask import Flask
from .views.index import ind
from .views.account import account


def create_app():
    app = Flask(__name__)
    app.config.from_object('settings.Config')

    app.register_blueprint(ind)
    app.register_blueprint(account)

    return app