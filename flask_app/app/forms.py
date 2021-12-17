from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateField, SelectField, \
    IntegerField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User, Interview, Grade, Question
from app import db
from datetime import datetime


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    # name = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    # name = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


# class CreateNewUsersForm(FlaskForm):
#     username = StringField('Username', validators=DataRequired())
#     email = StringField('Email')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    # name = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class AddQuestionForm(FlaskForm):
    essence = StringField('Question', validators=[DataRequired()])
    supposed_answer = StringField('Answer', validators=[DataRequired()])
    max_grade = IntegerField('Max grade')
    submit = SubmitField('Add')

    def validate_essence(self, essence):
        question = Question.query.filter_by(essence=essence.data).first()
        if question is not None:
            raise ValidationError('Please use a different essence.')


class EditQuestionForm(FlaskForm):
    essence = StringField('Question', validators=[DataRequired()])
    supposed_answer = StringField('Answer', validators=[DataRequired()])
    max_grade = IntegerField('Max Grade')
    submit = SubmitField('Submit')

    def __init__(self, grade, *args, **kwargs):
        super(EditQuestionForm, self).__init__(*args, **kwargs)
        self.grades = grade

    def validate_username(self, essence):
        if essence.data != self.essence:
            question = Question.query.filter_by(essence=self.essence.data).first()
            if question is not None:
                raise ValidationError('Please use a different essence.')


class AddInterviewForm(FlaskForm):
    candidate = StringField('Candidate full name', validators=[DataRequired()])
    questions = SelectMultipleField('Select question', coerce=str, choices=[question for question in Question.query.order_by(Question.essence).all()],
                                   validators=[DataRequired()])
    date = DateField('Choose date', format="%m/%d/%Y", validators=[DataRequired()])
    start_time = SelectField('Choose starting time(in 24hr expression)', coerce=int,
                             choices=[(i, i) for i in range(9, 18)], validators=[DataRequired()])
    end_time = SelectField('Choose starting time(in 24hr expression)', coerce=int,
                           choices=[(i, i) for i in range(9, 18)], validators=[DataRequired()])
    # users = SelectMultipleField('Select interviewers', coerce=str, validators=[DataRequired()],
    #                             choices=[(user.id, user.username) for user in User.query.order_by('username').all()])
    users = SelectMultipleField('Select interviewers:', coerce=str, validators=[DataRequired()],
                                choices=[(user.id, user.username) for user in Interview.query.filter(Interview.users).all()])
    grade = IntegerField(Grade.query.order_by(Grade.interview_id).all())
    # final_grade = Grade.query.order_by(Grade.interview_id).all()
    submit = SubmitField('Add')

    # def __init__(self, questions, users, grade, *args, **kwargs):
    #     super(AddInterviewForm, self).__init__(questions, users,grade)
    #     self.questions = questions
    #     self.users = users
    #     self.grade = grade

    def validate_candidate(self, candidate):
        candidate = Interview.query.filter_by(candidate=candidate.data).first()
        if candidate is not None:
            raise ValidationError('Please use a different candidate.')


class BookinterviewForm(FlaskForm):
    candidate = StringField('Candidate name', validators=[DataRequired()])
    interviewer = StringField('Interviewers Email', validators=[DataRequired()])
    question = StringField('Question Essence', validators=[DataRequired()])
    supposed_answer = StringField('Supposed Answer', validators=[DataRequired()])
    date = DateField('Choose date', format="%m/%d/%Y", validators=[DataRequired()])
    start_time = SelectField('Choose starting time(in 24hr expression)', coerce=int,
                             choices=[(i, i) for i in range(9, 18)])
    end_time = SelectField('Choose starting time(in 24hr expression)', coerce=int,
                           choices=[(i, i) for i in range(9, 18)])
    submit = SubmitField('Book Interview')

    def validate_interviewer(self, interviewer):
        s = Interviewer.query.filter_by(email=self.interviewer.data).first()
        if s is None:
            raise ValidationError("Email id is not present in the database")

    def validate_candidate(self, candidate):
        i = Interview.query.filter_by(candidate=self.candidate.data).first()
        if i is None:
            raise ValidationError("Email id is not present in the database")

    def validate_date(self, date):
        if self.date.data < datetime.datetime.now().date():
            raise ValidationError('You can only book for day after today.')


class GradeForm(FlaskForm):
    grade = SelectField('Grade', coerce=int, choices=[i for i in range(0, 11)], validators=[DataRequired()])
    question_id = SelectField('Question', coerce=int, choices=[(q.id, q.essence) for q in Question.query.order_by('essence')])
    rater_id = SelectField('Interviewer', coerce=str, choices=[(u.id, u.username) for u in User.query.order_by('username')])
    interview_id = SelectField('Interview', coerce=int, choices=[(i.id, i.candidate) for i in Interview.query.order_by('candidate')])
    submit = SubmitField('Add')


class EditGradeForm(FlaskForm):
    grade = IntegerField('Grade', validators=[DataRequired()])
    question_id = SelectField('Question', coerce=int,
                              choices=[(q.id, q.essence) for q in Question.query.order_by('essence')])
    rater_id = SelectField('Interviewer', coerce=str,
                           choices=[(u.id, u.username) for u in User.query.order_by('username')])
    interview_id = SelectField('Interview', coerce=int,
                               choices=[(i.id, i.candidate) for i in Interview.query.order_by('candidate')])
    submit = SubmitField('Add')
