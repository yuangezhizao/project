import unittest

from main import create_app


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        app = create_app('testing')
        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()

    def tearDown(self):
        self.context.pop()
