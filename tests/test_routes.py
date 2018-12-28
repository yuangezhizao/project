from flask import url_for
from os import path
import sys

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from main import app


class TestClass(object):
    def setup_class(self):
        app.config['TESTING'] = True
        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()

    def teardown_class(self):
        pass

    def test_main_hello_world(self):
        response = self.client.get(url_for('main.hello_world'))
        assert b'Hello World!' == response.data

    def test_main_index(self):
        response = self.client.get(url_for('main.index'))
        assert b'yuangezhizao' in response.data
