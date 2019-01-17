from flask_login import LoginManager, AnonymousUserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_whooshee import Whooshee
from flask_wtf import CSRFProtect
from flask_moment import Moment


login_manager = LoginManager()
db = SQLAlchemy()
whooshee = Whooshee()
csrf = CSRFProtect()
moment = Moment()


@login_manager.user_loader
def load_user(user_id):
    from main.models.user import User
    return User.query.get(int(user_id))


login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = '未授权用户，请先登录！'
login_manager.login_message_category = 'negative'


class Guest(AnonymousUserMixin):

    def can(self, permission_name):
        return False

    @property
    def is_admin(self):
        return False


login_manager.anonymous_user = Guest
