from flask import render_template, Blueprint, abort, request, flash, redirect, current_app, send_from_directory, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

from main.models.user import User
from main.models.photo import Photo
from main.plugins.decorators import permission_required
from main.plugins.extensions import db
from main.plugins.utils import allowed_file, rename_image, resize_image

user_bp = Blueprint('user', __name__)


@user_bp.route('/<id>')
@login_required
def index(id):
    user = User.query.filter_by(id=id).first_or_404()
    if user != current_user:
        return abort(403)
    photos = Photo.query.with_parent(user).order_by(Photo.timestamp.desc())
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
            db.session.add(photo)
            db.session.commit()
            return redirect(url_for('user.index', id=current_user.id))
    return render_template('user/upload.html')


@user_bp.route('/uploads/<path:filename>')
def get_image(filename):
    return send_from_directory(current_app.config['UPLOAD_PATH'], filename)
