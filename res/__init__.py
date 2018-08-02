""" Main module entrypoint """
from flask import Flask
from res.models import initialize_database
from res.routes import res_blueprint
from config import CURRENT_CONFIG


def create_app():
    """ Helper method to create the app """
    initialize_database()

    app = Flask(__name__)
    app.register_blueprint(res_blueprint)
    app.config.from_object(CURRENT_CONFIG)

    return app
