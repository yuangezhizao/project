from flask import render_template, Blueprint, abort
from flask_login import login_required, current_user

from main.models.user import User


user_bp = Blueprint('user', __name__)


@user_bp.route('/<id>')
@login_required
def index(id):
    user = User.query.filter_by(id=id).first_or_404()
    if user != current_user:
        return abort(403)
    return render_template('user/index.html', user=user)
