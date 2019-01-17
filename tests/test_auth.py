from flask import url_for

from tests.base import BaseTestCase


class AuthTestCase(BaseTestCase):

    def test_login_user(self):
        response = self.login()
        data = response.get_data(as_text=True)
        self.assertIn('用户信息', data)

    def test_fail_login_wrong_username(self):
        response = self.login(username='wrong-username', password='admin')
        data = response.get_data(as_text=True)
        self.assertIn('不存在的用户名！', data)

    def test_fail_login_wrong_password(self):
        response = self.login(username='admin', password='wrong-password')
        data = response.get_data(as_text=True)
        self.assertIn('不正确的密码！', data)

    def test_logout_user(self):
        self.login()
        response = self.logout()
        data = response.get_data(as_text=True)
        self.assertIn('注销成功！', data)

    def test_login_protect(self):
        response = self.client.get(url_for('user.index', id=0), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('未授权用户，请先登录！', data)
