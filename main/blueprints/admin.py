from flask import render_template, flash, redirect, Blueprint, request, current_app
from flask_login import login_required, current_user

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


@admin_bp.route('/users_list', methods=['GET'])
@login_required
@permission_required('RIGISTER')
def users_list():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['USERS_LIST_PER_PAGE']
    if not current_user.can('ADMINISTER'):
        depart_id = current_user.depart_id
        pagination = User.query.filter(User.depart_id == depart_id).order_by(User.member_since.desc()).paginate(page,
                                                                                                                per_page)
    else:
        depart_id = request.args.get('depart_id', 1, type=int)
        filters = []
        if depart_id != 0:
            filters.append(User.depart_id == depart_id)
        pagination = User.query.filter(*filters).order_by(User.member_since.desc()).paginate(page,
                                                                                             per_page)
    users_list = pagination.items
    return render_template('admin/users_list.html', pagination=pagination, users_list=users_list)


@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@permission_required('RIGISTER')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user == current_user:
        flash(f'不能删除自己', 'info')
        return redirect(request.referrer)
    if (not current_user.can('ADMINISTER')) and current_user.depart_id != user.depart_id:
        flash(f'不能删除非本部门用户', 'info')
        return redirect(request.referrer)
    db.session.delete(user)
    db.session.commit()
    flash(f'已删除 ID 为 {user_id} 的用户', 'info')
    return redirect(request.referrer)
