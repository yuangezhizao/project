from flask import render_template, flash, redirect, url_for, Blueprint, request
from flask_login import login_user, logout_user, login_required, current_user

from main.models.user import User
from main.plugins.utils import redirect_back
# from main.plugins.extensions import csrf

auth_bp = Blueprint('auth', __name__)


# @csrf.exempt
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.index', id=current_user.id))
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
            return redirect_back('user.index', id=user.id)
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('注销成功！', 'info')
    return redirect(url_for('auth.login'))
