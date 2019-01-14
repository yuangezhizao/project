from tests.base import BaseTestCase

from main.plugins.extensions import db
from main.models.user import Role, Depart


class CLITestCase(BaseTestCase):

    def setUp(self):
        super(CLITestCase, self).setUp()
        db.drop_all()

    def test_drop_command(self):
        result = self.runner.invoke(args=['drop'], input='y')
        self.assertIn('执行本操作之后会清空数据库表且无法恢复，请确认！', result.output)
        self.assertIn('已清空数据库表！', result.output)

    def test_init_command(self):
        result = self.runner.invoke(args=['init'])
        self.assertIn('初始化数据库……', result.output)
        self.assertIn('初始化角色和权限……', result.output)
        self.assertIn('初始化部门……', result.output)
        self.assertIn('初始化完成！', result.output)
        self.assertEqual(Role.query.count(), 4)  # 角色表行数
        self.assertEqual(Depart.query.count(), 8)  # 部门表行数
