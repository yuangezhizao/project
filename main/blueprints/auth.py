from flask import render_template, flash, redirect, url_for, Blueprint, request
from flask_login import login_user, logout_user, login_required, current_user

from main.models.user import User
from main.plugins.utils import redirect_back

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.index', id=current_user.id))
    if request.method == 'POST':
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if user is not None and user.validate_password(request.form['password']):
            if login_user(user):
                return redirect_back('user.index', id=user.id)
        flash('授权失败！', 'negative')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('注销成功！', 'info')
    return redirect(url_for('auth.login'))
