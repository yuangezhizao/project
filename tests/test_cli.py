from tests.base import BaseTestCase

from main.plugins.extensions import db
from main.models.user import Role


class CLITestCase(BaseTestCase):

    def setUp(self):
        super(CLITestCase, self).setUp()
        db.drop_all()

    def test_init_command(self):
        result = self.runner.invoke(args=['init'])
        self.assertIn('初始化数据库……', result.output)
        self.assertIn('初始化角色和权限……', result.output)
        self.assertIn('初始化完成！', result.output)
        self.assertEqual(Role.query.count(), 3)
