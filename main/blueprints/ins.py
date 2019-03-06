from flask import Blueprint, flash, redirect, url_for, render_template, request
from flask_login import login_required

from main.models.photo import Photo
from main.plugins.decorators import permission_required
from main.plugins.extensions import db

ins_bp = Blueprint('ins', __name__)


@ins_bp.route('/set-public/<int:photo_id>', methods=['POST'])
@login_required
@permission_required('SET_PUBLIC')
def set_public(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    status = request.form.get('status')
    photo.status = status
    flash(f'状态码已设置为：{status}', 'info')
    db.session.commit()
    return redirect(url_for('user.show_photo', photo_id=photo_id))


@ins_bp.route('/photos_list')
@login_required
@permission_required('SET_PUBLIC')
def photos_list():
    all_count = Photo.query.count()
    wait_count = Photo.query.filter_by(status=0).count()
    passed_count = Photo.query.filter_by(status=1).count()
    not_passed_count = Photo.query.filter_by(status=-1).count()
    photos = Photo.query.all()
    return render_template('ins/photos_list.html', wait_count=wait_count, all_count=all_count,
                           passed_count=passed_count, not_passed_count=not_passed_count, photos=photos)
