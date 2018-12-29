from flask_login import LoginManager, AnonymousUserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_whooshee import Whooshee

login_manager = LoginManager()
db = SQLAlchemy()
whooshee = Whooshee()


@login_manager.user_loader
def load_user(user_id):
    from main.models.user import User
    user = User.query.get(int(user_id))
    return user


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
