from flask import Blueprint, flash, redirect, url_for, render_template, request, current_app, abort
from flask_login import login_required, current_user

from main.models.photo import Photo, Task, Comment, Advice
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
    if not public_status:
        return abort(400)
    photo.public_status = public_status
    flash(f'状态码已设置为：{public_status}', 'info')
    db.session.commit()
    return redirect(request.referrer)


@ins_bp.route('/photos_list_set_public', methods=['GET', 'POST'])
@login_required
@permission_required('SET_PUBLIC')
def photos_list_set_public():
    task_name_first = request.args.get('task_name_first', '0')
    task_name_second = request.args.get('task_name_second', '0')
    task_name_third = request.args.get('task_name_third', '0')
    show_set = request.args.get('show_set', '1')
    depart_id = current_user.depart_id
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PHOTO_PER_PAGE']
    filters = [User.depart_id == depart_id, ]
    if task_name_first != '0':
        filters.append(Task.name_first == task_name_first)
    if task_name_second != '0':
        filters.append(Task.name_second == task_name_second)
    if task_name_third != '0':
        filters.append(Task.name_third == task_name_third)
    if show_set:
        filters.append(Photo.public_status == 0)
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
    return render_template('ins/photos_list/set_public.html', all_count=all_count, wait_count=wait_count,
                           passed_count=passed_count, not_passed_count=not_passed_count,
                           task_name_first=task_name_first, task_name_second=task_name_second,
                           task_name_third=task_name_third, depart_id=depart_id, pagination=pagination, photos=photos)


@ins_bp.route('/photos_list_advice', methods=['GET', 'POST'])
@login_required
@permission_required('COMMENT')
def photos_list_advice():
    task_name_first = request.args.get('task_name_first', '0')
    task_name_second = request.args.get('task_name_second', '0')
    task_name_third = request.args.get('task_name_third', '0')
    depart_id = request.args.get('depart_id', 0, type=int)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PHOTO_PER_PAGE']
    filters = [Photo.public_status == 1, ]
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
        passed_count = Photo.query.join(Task).join(User).filter(*filters).filter(Photo.public_status == 1).count()
    else:
        pagination = Photo.query.order_by(Photo.timestamp.desc()).paginate(page, per_page)
        passed_count = Photo.query.filter_by(public_status=1).count()
    photos = pagination.items
    return render_template('ins/photos_list/advice.html', passed_count=passed_count,
                           task_name_first=task_name_first, task_name_second=task_name_second,
                           task_name_third=task_name_third, depart_id=depart_id, pagination=pagination, photos=photos)


@ins_bp.route('/set-advice/<int:advice_id>', methods=['POST'])
@login_required
@permission_required('ADVICE')
def set_advice(advice_id):
    advice = Advice.query.get_or_404(advice_id)
    status = request.form.get('status')
    if not status:
        return abort(400)
    advice.status = status
    flash(f'状态码已设置为：{status}', 'info')
    db.session.commit()
    return redirect(request.referrer)


@ins_bp.route('/advice', methods=['POST'])
@login_required
@permission_required('ADVICE')
def advice():
    body = request.form.get('body')
    depart_id = request.form.get('depart_id')
    passed_count = request.form.get('passed_count')
    url = request.form.get('url')
    filter = request.form.get('filter')
    advice = Advice(depart_id=depart_id,
                    passed_count=passed_count,
                    url=url,
                    filter=filter,
                    author=current_user._get_current_object())
    comment = Comment(body=body,
                      advice=advice,
                      author=current_user._get_current_object())
    db.session.add(advice, comment)
    db.session.commit()
    flash('评论成功！', 'success')
    return redirect(url_for('ins.photos_list_advice'))


@ins_bp.route('/advice_list', methods=['GET', 'POST'])
@login_required
@permission_required('COMMENT')
def advice_list():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ADVICE_LIST_PER_PAGE']
    if not current_user.can('ADVICE'):
        depart_id = current_user.depart_id
        pagination = Advice.query.filter(Advice.depart_id == depart_id).order_by(Advice.timestamp.desc()).paginate(page,
                                                                                                                   per_page)
    else:
        pagination = Advice.query.order_by(Advice.timestamp.desc()).paginate(page, per_page)
    advice_list = pagination.items
    return render_template('ins/advice_list.html', pagination=pagination, advice_list=advice_list)


@ins_bp.route('/advice/<int:advice_id>')
@login_required
@permission_required('COMMENT')
def show_advice(advice_id):
    advice = Advice.query.get_or_404(advice_id)
    comments = Comment.query.filter_by(advice_id=advice_id)
    return render_template('ins/advice.html', advice=advice, comments=comments)


@ins_bp.route('/comment', methods=['POST'])
@login_required
@permission_required('COMMENT')
def comment():
    body = request.form.get('body')
    advice_id = request.form.get('advice_id')
    advice = Advice.query.get_or_404(advice_id)
    if not current_user.can('ADVICE') and advice.comments[-1].author == current_user:
        flash('您已经回复，请等待新回复！', 'negative')
    else:
        if current_user.can('ADVICE'):
            advice.status = 2
        else:
            advice.status = 1
        comment = Comment(body=body,
                          advice=advice,
                          author=current_user)
        db.session.add(advice, comment)
        db.session.commit()
    flash('回复成功！', 'success')
    return redirect(url_for('ins.show_advice', advice_id=advice_id))
