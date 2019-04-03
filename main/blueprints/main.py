import git
from flask import Blueprint, render_template, current_app

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('main/index.html')


@main_bp.route('/hello_world')
def hello_world():
    return 'Hello World!'


@main_bp.route('/commits')
def commits():
    version = git.Repo(current_app.config['GIT_PATH']).git.describe(always=True)
    commits = git.Repo(current_app.config['GIT_PATH']).iter_commits()
    return render_template('main/commits.html', version=version, commits=commits)
