from flask import render_template, Blueprint, abort, request, flash, redirect, current_app, send_from_directory, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

from main.models.user import User
from main.models.photo import Photo
from main.models.task_dict import task_dict
from main.plugins.decorators import permission_required
from main.plugins.extensions import db
from main.plugins.utils import allowed_file, rename_image, resize_image

user_bp = Blueprint('user', __name__)


@user_bp.route('/<id>')
@login_required
def index(id):
    user = User.query.filter_by(id=id).first_or_404()
    if (not current_user.can('WATCH_OTHERS')) & (current_user != user):
        abort(403, '你的权限不足，缺少“WATCH_OTHERS”权限')
    photos = Photo.query.with_parent(user).order_by(Photo.timestamp.desc()).all()
    return render_template('user/index.html', user=user, photos=photos)


@user_bp.route('/upload', methods=['GET', 'POST'])
@login_required
@permission_required('UPLOAD')
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('请先“选择文件”', 'negative')
            return redirect(request.url)
        f = request.files.get('file')
        if not request.form.get('description'):
            flash('请填写“描述”', 'negative')
            return redirect(request.url)
        description = request.form.get('description')
        if not request.form.get('task_name_third'):
            flash('请选择“任务”', 'negative')
            return redirect(request.url)
        task_name_third = request.form.get('task_name_third')
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            filename = rename_image(filename)
            f.save(os.path.join(current_app.config['UPLOAD_PATH'], filename))
            filename_s = resize_image(f, filename, current_app.config['PHOTO_SIZE']['small'])
            filename_m = resize_image(f, filename, current_app.config['PHOTO_SIZE']['medium'])
            photo = Photo(
                filename=filename,
                filename_s=filename_s,
                filename_m=filename_m,
                description=description,
                author=current_user._get_current_object()
            )
            photo.set_task_by_name_third(task_name_third)
            db.session.add(photo)
            db.session.commit()
            return redirect(url_for('user.index', id=current_user.id))
    return render_template('user/upload.html')


@user_bp.route('/uploads/<path:filename>')
@login_required
def get_image(filename):
    return send_from_directory(current_app.config['UPLOAD_PATH'], filename)


@user_bp.route('/photo/<int:photo_id>')
@login_required
def show_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    return render_template('user/photo.html', photo=photo)


@user_bp.route('/get_task_name_html', methods=['POST'])
@login_required
def get_task_name_html():
    if request.method == 'POST':
        action = request.form.get('action')
        task_name_html = '<option value="0">==请选择==</option>'
        if action == 'getseconds':
            task_name_first = request.form.get('task_name_first')
            for task_name_second in task_dict[task_name_first]:
                task_name_html += f'<option value="{task_name_second}">{task_name_second}</option>'
        elif action == 'getthirds':
            task_name_first = request.form.get('task_name_first')
            task_name_second = request.form.get('task_name_second')
            for task_name_third in task_dict[task_name_first][task_name_second]:
                task_name_html += '<option value="{0}">{1}</option>'.format(task_name_third['details'], task_name_third['details'])
        return task_name_html
