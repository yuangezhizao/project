from datetime import datetime

from main.plugins.extensions import db, whooshee
from main.models.task_dict import task_dict


@whooshee.register_model('name_third')
class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name_first = db.Column(db.String(30))
    name_second = db.Column(db.String(30))
    name_third = db.Column(db.String(512), unique=True, index=True)
    kind = db.Column(db.String(30))

    photos = db.relationship('Photo', back_populates='task')

    @staticmethod
    def init_tasks():
        count = 1
        for task_name_first in task_dict.keys():
            for task_name_second in task_dict[task_name_first]:
                for task_name_third in task_dict[task_name_first][task_name_second]:
                    task = Task(id=count, name_first=task_name_first, name_second=task_name_second,
                                name_third=task_name_third['details'], kind=task_name_third['kind'])
                    count += 1
                    db.session.add(task)
        db.session.commit()

    def __repr__(self):
        return f'<Task {self.id}>'


@whooshee.register_model('description')
class Photo(db.Model):
    __tablename__ = 'photos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text())
    filename = db.Column(db.String(64))
    filename_m = db.Column(db.String(64))
    filename_s = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    public_status = db.Column(db.Integer, default=0)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User', back_populates='photos')

    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    task = db.relationship('Task', back_populates='photos')

    def __repr__(self):
        return f'<Photo {self.id}>'

    def set_task_by_id(self, task_id=1):
        self.task = Task.query.filter_by(id=task_id).first()
        db.session.commit()

    def set_task_by_name_third(self, name_third):
        self.task = Task.query.filter_by(name_third=name_third).first()
        db.session.commit()
