from flask import url_for
import unittest

from main import create_app
from main.plugins.extensions import db
from main.models.user import User, Role


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        app = create_app('testing')
        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()

        db.create_all()
        Role.init_role()

        admin_user = User(email='admin@yuangezhizao.cn', name='管理员', username='admin')
        admin_user.set_password('admin')

        normal_user = User(email='user@yuangezhizao.cn', name='用户', username='user')
        normal_user.set_password('user')

        ins_user = User(email='ins@yuangezhizao.cn', name='审核者一', username='ins')
        ins_user.set_password('ins')

        mod_user = User(email='mod@yuangezhizao.cn', name='审核者二', username='mod')
        mod_user.set_password('mod')

        db.session.add_all([admin_user, normal_user, ins_user, mod_user])
        db.session.commit()

    def tearDown(self):
        db.drop_all()
        self.context.pop()

    def login(self, username=None, password=None):
        if username is None and password is None:
            username = 'admin'
            password = 'admin'
        return self.client.post(url_for('auth.login'), data=dict(username=username, password=password),
                                follow_redirects=True)

    def logout(self):
        return self.client.get(url_for('auth.logout'), follow_redirects=True)
