from flask import Flask, render_template
import os
import click

from main.settings import config
from main.blueprints.main import main_bp
from main.blueprints.auth import auth_bp
from main.blueprints.user import user_bp
from main.plugins.extensions import db, login_manager, whooshee
from main.models.user import User, Role


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'default')

    app = Flask(__name__, static_folder='static')

    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_commands(app)

    return app


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    whooshee.init_app(app)
    register_shell_context(app)


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')


def register_errorhandlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(413)
    def request_entity_too_large(e):
        return render_template('errors/413.html'), 413

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500


def register_commands(app):
    @app.cli.command()
    def init():
        click.echo('初始化数据库……')
        db.create_all()

        click.echo('初始化角色和权限……')
        Role.init_role()

        click.echo('初始化完成！')


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User)
