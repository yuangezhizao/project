from flask import render_template, flash, redirect, url_for, Blueprint, request
from flask_login import login_user, logout_user, login_required, current_user

from main.models.user import User
# from main.plugins.extensions import csrf
from main.plugins.decorators import permission_required
from main.plugins.extensions import db
from main.plugins.utils import redirect_back

auth_bp = Blueprint('auth', __name__)


# @csrf.exempt
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.index', user_id=current_user.id))
    if request.method == 'POST':
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('不存在的用户名！', 'negative')
        elif not user.validate_password(request.form['password']):
            flash('不正确的密码！', 'negative')
        else:
            remember = request.form.get('remember', False)
            login_user(user, remember)
            return redirect_back('user.index', user_id=user.id)
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('注销成功！', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
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
