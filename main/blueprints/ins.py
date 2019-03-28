from flask import Blueprint, flash, redirect, url_for, render_template, request, current_app
from flask_login import login_required, current_user

from main.models.photo import Photo, Task, Comment
from main.models.user import User
from main.plugins.decorators import permission_required
from main.plugins.extensions import db

ins_bp = Blueprint('ins', __name__)


@ins_bp.route('/set-public/<int:photo_id>', methods=['POST'])
@login_required
@permission_required('SET_PUBLIC')
def set_public(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    public_status = request.form.get('public_status')
    photo.public_status = public_status
    flash(f'状态码已设置为：{public_status}', 'info')
    db.session.commit()
    return redirect(request.referrer)


@ins_bp.route('/photos_list', methods=['GET', 'POST'])
@login_required
@permission_required('SET_PUBLIC')
def photos_list():
    task_name_first = request.args.get('task_name_first', '0')
    task_name_second = request.args.get('task_name_second', '0')
    task_name_third = request.args.get('task_name_third', '0')
    depart_id = request.args.get('depart_id', 0, type=int)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PHOTO_PER_PAGE']
    filters = []
    if task_name_first != '0':
        filters.append(Task.name_first == task_name_first)
    if task_name_second != '0':
        filters.append(Task.name_second == task_name_second)
    if task_name_third != '0':
        filters.append(Task.name_third == task_name_third)
    if depart_id:
        filters.append(User.depart_id == depart_id)
    if filters:
        pagination = Photo.query.join(Task).join(User).filter(*filters).order_by(Photo.timestamp.desc()).paginate(page,
                                                                                                                  per_page)
        all_count = Photo.query.join(Task).join(User).filter(*filters).count()
        wait_count = Photo.query.join(Task).join(User).filter(*filters).filter(Photo.public_status == 0).count()
        passed_count = Photo.query.join(Task).join(User).filter(*filters).filter(Photo.public_status == 1).count()
        not_passed_count = Photo.query.join(Task).join(User).filter(*filters).filter(Photo.public_status == -1).count()
    else:
        pagination = Photo.query.order_by(Photo.timestamp.desc()).paginate(page, per_page)
        all_count = Photo.query.count()
        wait_count = Photo.query.filter_by(public_status=0).count()
        passed_count = Photo.query.filter_by(public_status=1).count()
        not_passed_count = Photo.query.filter_by(public_status=-1).count()
    photos = pagination.items
    return render_template('ins/photos_list.html', all_count=all_count, wait_count=wait_count,
                           passed_count=passed_count, not_passed_count=not_passed_count,
                           task_name_first=task_name_first, task_name_second=task_name_second,
                           task_name_third=task_name_third, depart_id=depart_id, pagination=pagination, photos=photos)


@ins_bp.route('/comment', methods=['POST'])
@login_required
@permission_required('COMMENT')
def comment():
    body = request.form.get('body')
    depart_id = request.form.get('depart_id')
    passed_count = request.form.get('passed_count')
    url = request.form.get('url')
    filter = request.form.get('filter')
    comment = Comment(body=body,
                      depart_id=depart_id,
                      passed_count=passed_count,
                      url=url,
                      filter=filter,
                      author=current_user._get_current_object())
    db.session.add(comment)
    db.session.commit()
    flash('评论成功！', 'success')
    return redirect(url_for('ins.photos_list'))


@ins_bp.route('/comments_list', methods=['GET', 'POST'])
@login_required
@permission_required('COMMENT')
def comments_list():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PHOTO_PER_PAGE']
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(page, per_page)
    comments = pagination.items
    return render_template('ins/comments_list.html', pagination=pagination, comments=comments)
