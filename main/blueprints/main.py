import git
from flask import Blueprint, render_template, current_app, request

from main.models.photo import Photo, Task
from main.models.user import User, Depart

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def intro():
    task_name_first = request.args.get('task_name_first', '0')
    task_name_second = request.args.get('task_name_second', '0')
    task_name_third = request.args.get('task_name_third', '0')
    depart_id = request.args.get('depart_id', 0, type=int)
    time_range = request.args.get('time_range')
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
    if time_range and '至' in time_range:
        begin_time = time_range.split('至')[0][:-1]
        end_time = time_range.split('至')[1][1:]
        filters.append(Photo.timestamp.between(begin_time, end_time))
    if filters:
        pagination = Photo.query.join(Task).join(User).filter(*filters).order_by(Photo.timestamp.desc()).paginate(page,
                                                                                                                  per_page)
    else:
        pagination = Photo.query.order_by(Photo.timestamp.desc()).paginate(page, per_page)
    photos = pagination.items
    departs_list = Depart.query.all()
    # TODO：这咋分页？
    return render_template('main/intro.html', time_range=time_range, task_name_first=task_name_first,
                           task_name_second=task_name_second, task_name_third=task_name_third, depart_id=depart_id,
                           pagination=pagination, photos=photos, departs_list=departs_list)


@main_bp.route('/index')
def index():
    notice = '【190516】更新日志不定时更新'
    return render_template('main/index.html', notice=notice)


@main_bp.route('/hello_world')
def hello_world():
    return 'Hello World!'


@main_bp.route('/commits')
def commits():
    commits = git.Repo(current_app.config['GIT_PATH']).iter_commits()
    return render_template('main/commits.html', commits=commits)
