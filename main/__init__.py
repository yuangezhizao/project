from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFError
from flask_login import current_user
from flask_migrate import Migrate
import os
import click
import datetime

from main.settings import config
from main.blueprints.main import main_bp
from main.blueprints.auth import auth_bp
from main.blueprints.user import user_bp
from main.plugins.extensions import db, login_manager, whooshee, csrf, moment
from main.models.user import User, Role


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'default')

    app = Flask(__name__, static_folder='static')

    app.config.from_object(config[config_name])

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    # app.jinja_env.auto_reload = True

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_commands(app)
    register_template_context(app)

    return app


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    whooshee.init_app(app)
    register_shell_context(app)
    csrf.init_app(app)
    moment.init_app(app)
    migrate = Migrate(app, db)


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')


def register_errorhandlers(app):
    @app.errorhandler(400)
    def bad_request(reason):
        if reason is not None:
            return render_template('errors/400.html', reason=reason), 400
        return render_template('errors/400.html'), 400

    @app.errorhandler(CSRFError)
    def csrf_error(reason):
        if reason is not None:
            return render_template('errors/csrf_error.html', reason=reason), 400
        return render_template('errors/csrf_error.html'), 400

    @app.errorhandler(403)
    def forbidden(reason):
        if reason is not None:
            return render_template('errors/403.html', reason=reason), 403
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(reason):
        if reason is not None:
            return render_template('errors/404.html', reason=reason), 404
        return render_template('errors/404.html'), 404

    @app.errorhandler(413)
    def request_entity_too_large(reason):
        if reason is not None:
            return render_template('errors/413.html', reason=reason), 413
        return render_template('errors/413.html'), 413

    @app.errorhandler(500)
    def internal_server_error(reason):
        if reason is not None:
            return render_template('errors/500.html', reason=reason), 500
        return render_template('errors/500.html'), 500


def register_commands(app):
    @app.cli.command()
    def init():
        click.echo('初始化数据库……')
        db.create_all()

        click.echo('初始化角色和权限……')
        Role.init_role()

        click.echo('初始化完成！')

    @app.cli.command()
    def drop():
        if drop:
            click.confirm('执行本操作之后会清空数据库表且无法恢复，请确认！', abort=True)
            db.drop_all()
            click.echo('已清空数据库表！')

    @app.cli.command()
    def set():
        click.echo('设定管理员……')
        admin_user = User(email='admin@yuangezhizao.cn', name='管理员', username='admin')
        admin_user.set_password('admin')

        click.echo('设定用户……')
        normal_user = User(email='user@yuangezhizao.cn', name='用户', username='user')
        normal_user.set_password('user')

        click.echo('设定审核者一……')
        ins_user = User(email='ins@yuangezhizao.cn', name='审核者一', username='ins')
        ins_user.set_password('ins')

        click.echo('设定审核者二……')
        mod_user = User(email='mod@yuangezhizao.cn', name='审核者二', username='mod')
        mod_user.set_password('mod')

        db.session.add_all([admin_user, normal_user, ins_user, mod_user])
        db.session.commit()

        click.echo('设定完成！')


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User)


def register_template_context(app):
    @app.context_processor
    def my_context_processor():
        template_variables = {
            'user': current_user,
            'ip': request.remote_addr,
            'url': request.url,
            'timestamp': datetime.datetime.utcnow()
        }
        return template_variables

    @app.before_request
    def before_request():
        if current_user.is_authenticated:
            current_user.last_seen = datetime.datetime.utcnow()
            db.session.commit()
