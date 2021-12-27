from datetime import datetime

from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5

# interviewers_interview = db.Table('interviewers_interview',
#                                   db.Column('interviewer_id', db.Integer, db.ForeignKey('interviewer.id'),
#                                             primary_key=True),
#                                   db.Column('interview_id', db.Integer, db.ForeignKey('interview.id'), primary_key=True)
#                                   )

# interviewers_user = db.Table('interviewers_user',
#                              db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#                              db.Column('interviewer_id', db.Integer, db.ForeignKey('interviewer.id'), primary_key=True)
#                              )

users_interview = db.Table('users_interview',
                           db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                           db.Column('interview_id', db.Integer, db.ForeignKey('interview.id'), primary_key=True)
                           )

interviews_question = db.Table('interviews_question',
                               db.Column('interview_id', db.Integer, db.ForeignKey('interview.id'), primary_key=True),
                               db.Column('question_id', db.Integer, db.ForeignKey('question.id'), primary_key=True)
                               )

# users_question = db.Table('users_question',
#                           db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#                           db.Column('question_id', db.Integer, db.ForeignKey('question.id'), primary_key=True)
#                           )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean(False))
    # questions = db.relationship('Question', secondary=users_question, lazy='subquery',
    #                             backref=db.backref('interviewers', lazy=True))

    def __repr__(self):
        return f'{self.first_name} {self.last_name}'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    @staticmethod
    def get_selection_list():
        result = []
        for i in User.query.all():
            result.append((f'{i.id}', f'{i.first_name} {i.last_name}'))
        return result


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    essence = db.Column(db.String(64))
    supposed_answer = db.Column(db.Text)
    max_grade = db.Column(db.Integer)
    short_description = db.Column(db.String(140))

    def __repr__(self):
        return f'{self.short_description}'

    @staticmethod
    def get_selection_list():
        result = []
        for i in Question.query.all():
            result.append((f'{i.id}', f'{i.short_description}'))
            # result.append(i.id)
        return result


class Interview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate = db.Column(db.String(120), nullable=False)
    questions = db.relationship('Question', secondary=interviews_question, lazy='subquery',
                                backref=db.backref('interviews', lazy=True))
    interviewers = db.relationship('User', secondary=users_interview, lazy='subquery',
                                   backref=db.backref('interviews', lazy=True))
    final_grade = db.Column(db.Float(precision=2))
    date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)

    def __repr__(self):
        return f'{self.candidate}'

    @staticmethod
    def get_selection_list():
        result = []
        for i in Interview.query.all():
            result.append((f'{i.id}', f'{i.candidate}'))
        return result


class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))  # many to one
    question = db.relationship("Question", backref="grades")
    interviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # many to one
    interviewer = db.relationship("User", backref="grades")
    interview_id = db.Column(db.Integer, db.ForeignKey('interview.id'))  # many to one
    interview = db.relationship("Interview", backref="grades")
    grade = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f'{self.interviewer} gives {self.interview} {self.grade} for {self.question}'
