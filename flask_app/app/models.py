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
                           db.Column('user_id', db.Integer, db.ForeignKey('user.id'),
                                     primary_key=True),
                           db.Column('interview_id', db.Integer, db.ForeignKey('interview.id'), primary_key=True)
                           )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')  # one to many
    grades = db.relationship('Grade', foreign_keys='Grade.rater_id', backref='rater', lazy='dynamic')  # one to many
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    # interviewers = db.relationship('Interviewer',
    #                                secondary=interviewers_user,
    #                                back_populates='users',
    #                                lazy='dynamic'
    #                                )
    # role = db.Column(db.String(20))
    # recruiter = db.relationship('User', backref='recruiter', uselist=False)
    # interviewer = db.relationship('User', backref='interviewer', uselist=False)
    # manager = db.relationship('User', backref='manager', uselist=False)
    interviews = db.relationship('Interview',
                                 secondary=users_interview,
                                 back_populates='users'
                                 )  # many to many relation with interview

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# class Interviewer(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     interviews = db.relationship('Interview',
#                                  secondary=interviewers_interview,
#                                  back_populates='interviewers',
#                                  lazy='dynamic'
#                                  )  # many to many relation with interview
#     users = db.relationship('User',
#                             secondary=interviewers_user,
#                             back_populates='interviewers',
#                             lazy='dynamic'
#                             )
#
#     def __repr__(self):
#         return f'id: {self.id}, user id: {self.user_id}'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # many to one

    def __repr__(self):
        return f'<Post {self.body}>'


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    essence = db.Column(db.String(140))
    supposed_answer = db.Column(db.String(250))
    max_grade = db.Column(db.Integer, default=10)
    grades = db.relationship('Grade', foreign_keys='Grade.question_id', backref='question', lazy='dynamic')  # one to many
    interview_id = db.Column(db.Integer, db.ForeignKey('interview.id'))  # many to one

    def __repr__(self):
        return f'Question: {self.essence}\nSupposed answer: {self.supposed_answer}'


class Interview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate = db.Column(db.String(120), index=True, unique=True)
    questions = db.relationship('Question', foreign_keys='Question.interview_id', backref='interview', lazy='dynamic')  # one to many
    final_grade = db.Column(db.Integer)
    date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    # interviewers = db.relationship('Interviewer',
    #                                secondary=interviewers_interview,
    #                                back_populates='interviews',
    #                                lazy='dynamic'
    #                                )
    users = db.relationship('User',
                            secondary=users_interview,
                            back_populates='interviews'
                            )
    grades = db.relationship('Grade', foreign_keys='Grade.interview_id', backref='interview', lazy='dynamic')  # one to many

    def __repr__(self):
        return f'Interview {self.id} for candidate {self.candidate}'


class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))  # many to one
    rater_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # many to one
    interview_id = db.Column(db.Integer, db.ForeignKey('interview.id'))  # many to one
    grade = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'{self.rater} gives {self.interview} {self.grade} for {self.question}'
