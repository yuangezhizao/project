import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from main.plugins.extensions import db, whooshee

# relationship table
roles_permissions = db.Table('roles_permissions',
                             db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
                             db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'))
                             )


class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    roles = db.relationship('Role', secondary=roles_permissions, back_populates='permissions')

    def __repr__(self):
        return f'<Permission {self.name}>'


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    users = db.relationship('User', back_populates='role')
    permissions = db.relationship('Permission', secondary=roles_permissions, back_populates='roles')

    @staticmethod
    def init_roles():
        roles_permissions_map = {
            'User': ['UPLOAD'],
            'Inspector': ['UPLOAD', 'RIGISTER', 'WATCH_OTHERS', 'SET_PUBLIC', 'COMMENT'],
            'Moderator': ['UPLOAD', 'RIGISTER', 'WATCH_OTHERS', 'COMMENT'],
            'Administrator': ['UPLOAD', 'RIGISTER', 'WATCH_OTHERS', 'SET_PUBLIC', 'COMMENT', 'ADMINISTER']
        }

        # 权限分配：
        # 用户：上传；
        # 审核者一：上传、注册、浏览他人、公开；
        # 审核者二：上传、注册、浏览他人、修改；
        # 管理员：全部。

        for role_name in roles_permissions_map:
            role = Role.query.filter_by(name=role_name).first()
            if role is None:
                role = Role(name=role_name)
                db.session.add(role)
            role.permissions = []
            for permission_name in roles_permissions_map[role_name]:
                permission = Permission.query.filter_by(name=permission_name).first()
                if permission is None:
                    permission = Permission(name=permission_name)
                    db.session.add(permission)
                role.permissions.append(permission)
        db.session.commit()

    def __repr__(self):
        return f'<Role {self.name}>'


class Depart(db.Model):
    __tablename__ = 'departs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    users = db.relationship('User', back_populates='depart')

    @staticmethod
    def init_departs():
        depart_list = ['本科生第一支部', '本科生第二支部', '研究生第一支部', '研究生第二支部', '研究生第三支部', '教工第一支部', '教工第二支部', '计算机系支部']
        # 八个部门列表硬编码于此处，初始化时自动写入数据库
        for depart in depart_list:
            depart = Depart(name=depart)
            db.session.add(depart)
        db.session.commit()

    def __repr__(self):
        return f'<Depart {self.name}>'


@whooshee.register_model('name', 'username')
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    email = db.Column(db.String(254), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(30))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.datetime.utcnow)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Role', back_populates='users')
    depart_id = db.Column(db.Integer, db.ForeignKey('departs.id'))
    depart = db.relationship('Depart', back_populates='users')

    photos = db.relationship('Photo', back_populates='author', cascade='all')
    comments = db.relationship('Comment', back_populates='author', cascade='all')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.set_role_by_role_name()
        self.set_depart_by_depart_name()

    def __repr__(self):
        return f'<User {self.username}>'

    # @property
    # def password(self):
    #     raise AttributeError('密码不具有可读属性')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def set_role_by_role_name(self, role_name='User'):
        self.role = Role.query.filter_by(name=role_name).first()
        db.session.commit()

    def set_depart_by_depart_name(self, depart_name='本科生第一支部'):
        self.depart = Depart.query.filter_by(name=depart_name).first()
        db.session.commit()

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role.name == 'Administrator'

    def can(self, permission_name):
        permission = Permission.query.filter_by(name=permission_name).first()
        return permission is not None and self.role is not None and permission in self.role.permissions

    def ping(self):
        self.last_seen = datetime.datetime.utcnow()
        db.session.commit()
