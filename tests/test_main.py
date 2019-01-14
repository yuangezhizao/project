from flask import url_for

from tests.base import BaseTestCase


class MainTestCase(BaseTestCase):

    def test_index_page(self):
        response = self.client.get(url_for('main.index'))
        data = response.get_data(as_text=True)
        self.assertIn('登录', data)

        self.login()
        response = self.client.get(url_for('main.index'))
        data = response.get_data(as_text=True)
        self.assertNotIn('登录', data)
        self.assertIn('注销', data)

    def test_hello_world_page(self):
        response = self.client.get(url_for('main.hello_world'))
        data = response.get_data(as_text=True)
        self.assertIn('Hello World!', data)
