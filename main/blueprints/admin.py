from flask import render_template, flash, redirect, Blueprint, request, current_app
from flask_login import login_required, current_user

admin_bp = Blueprint('admin', __name__)

from main.models.user import User, Depart
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
    departs_list = Depart.query.all()
    # TODO：这咋分页？
    return render_template('admin/register.html', departs_list=departs_list)


@admin_bp.route('/users_list')
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
    departs_list = Depart.query.all()
    # TODO：这咋分页？
    return render_template('admin/users_list.html', pagination=pagination, users_list=users_list,
                           departs_list=departs_list)


@admin_bp.route('/departs_list')
@login_required
@permission_required('ADMINISTER')
def departs_list():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['DEPARTS_LIST_PER_PAGE']
    pagination = Depart.query.paginate(page, per_page)
    departs_list = pagination.items
    return render_template('admin/departs_list.html', pagination=pagination, departs_list=departs_list)


@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@permission_required('RIGISTER')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user == current_user:
        flash(f'不能删除自己', 'negative')
        return redirect(request.referrer)
    if user.can('ADMINISTER'):
        flash(f'不能删除超级管理员', 'negative')
        return redirect(request.referrer)
    if user.can('ADVICE'):
        flash(f'不能删除全局评论者', 'negative')
        return redirect(request.referrer)
    if (not current_user.can('ADMINISTER')) and current_user.depart_id != user.depart_id:
        flash(f'不能删除非本部门用户', 'negative')
        return redirect(request.referrer)
    db.session.delete(user)
    db.session.commit()
    flash(f'已删除 ID 为 {user_id} 的用户', 'info')
    return redirect(request.referrer)


@admin_bp.route('/delete_depart/<int:depart_id>', methods=['POST'])
@login_required
@permission_required('ADMINISTER')
def delete_depart(depart_id):
    depart = Depart.query.get_or_404(depart_id)
    db.session.delete(depart)
    db.session.commit()
    flash(f'已删除 ID 为 {depart_id} 的部门', 'info')
    return redirect(request.referrer)


@admin_bp.route('/add_depart', methods=['POST'])
@login_required
@permission_required('ADMINISTER')
def add_depart():
    depart_name = request.form.get('depart_name')
    depart = Depart(name=depart_name)
    db.session.add(depart)
    db.session.commit()
    flash(f'新部门注册成功，名称：{depart}', 'info')
    return redirect(request.referrer)


@admin_bp.route('/edit_depart', methods=['POST'])
@login_required
@permission_required('ADMINISTER')
def edit_depart():
    depart_id = request.form.get('depart_id')
    depart_name = request.form.get('depart_name')
    depart = Depart.query.get_or_404(depart_id)
    depart.name = depart_name
    db.session.add(depart)
    db.session.commit()
    flash(f'修改成功，新部门名称：{depart}', 'info')
    return redirect(request.referrer)
