import git
from flask import Blueprint, render_template, current_app

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    notice = ''
    return render_template('main/index.html', notice=notice)


@main_bp.route('/hello_world')
def hello_world():
    return 'Hello World!'


@main_bp.route('/commits')
def commits():
    commits = git.Repo(current_app.config['GIT_PATH']).iter_commits()
    return render_template('main/commits.html', commits=commits)
