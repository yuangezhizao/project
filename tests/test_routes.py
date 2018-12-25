import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from main import app


class TestClass(object):
    def setup_class(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def teardown_class(self):
        pass

    def test_hello_world(self):
        response = self.app.get('/')
        assert b'Hello World!' == response.data
