from flask import render_template, flash, redirect, Blueprint, request
from flask_login import login_required

admin_bp = Blueprint('admin', __name__)

from main.models.user import User
from main.plugins.decorators import permission_required
from main.plugins.extensions import db


@admin_bp.route('/register', methods=['GET', 'POST'])
@login_required
@permission_required('RIGISTER')
def register():
    if request.method == 'POST':
        depart_name = request.form.get('depart_name')
        role_name = request.form.get('role_name')
        email = request.form.get('email')
        about_me = request.form.get('about_me')
        username = request.form.get('username')
        name = request.form.get('name')
        password = request.form.get('password')
        user = User(email=email, username=username, name=name, about_me=about_me)
        user.set_password(password)
        user.set_role_by_role_name(role_name)
        user.set_depart_by_depart_name(depart_name)
        db.session.add(user)
        db.session.commit()
        flash(f'新用户注册成功，邮箱：{email}，用户名：{username}，昵称：{name}', 'info')
        return redirect(request.url)
    return render_template('admin/register.html')
