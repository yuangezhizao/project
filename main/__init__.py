from flask import Flask

from main.blueprints.main import main_bp


def create_app():

    app = Flask(__name__)

    register_blueprints(app)

    return app


def register_blueprints(app):
    app.register_blueprint(main_bp)
