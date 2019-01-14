from flask import Blueprint, flash, redirect, url_for
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
    if photo.can_public:
        photo.can_public = False
        flash('已关闭公开权限', 'info')
    else:
        photo.can_public = True
        flash('已开启公开权限', 'info')
    db.session.commit()
    return redirect(url_for('user.show_photo', photo_id=photo_id))
