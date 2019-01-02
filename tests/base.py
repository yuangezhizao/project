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

        admin_user = User(email='150402207@sut.edu.cn', name='管理员', username='admin')
        admin_user.set_password('150402207')
        normal_user = User(email='root@yuangezhizao.cn', name='远哥制造', username='yuangezhizao')
        normal_user.set_password('yuangezhizao')

        db.session.add_all([admin_user, normal_user])
        db.session.commit()

    def tearDown(self):
        db.drop_all()
        self.context.pop()

    def login(self, username=None, password=None):
        if username is None and password is None:
            username = 'admin'
            password = '150402207'
        return self.client.post(url_for('auth.login'), data=dict(username=username, password=password),
                                follow_redirects=True)

    def logout(self):
        return self.client.get(url_for('auth.logout'), follow_redirects=True)
