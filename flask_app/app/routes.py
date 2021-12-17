from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Interview, Question, Grade
from app.forms import EditProfileForm, BookinterviewForm, AddQuestionForm, EditQuestionForm, GradeForm, EditGradeForm, \
    AddInterviewForm


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index')
@login_required
def index():
    users = User.query.all()
    for user in users:
        posts = [
            {'author': user, 'body': 'Test post #1'},
            {'author': user, 'body': 'Test post #2'}
        ]
    questions = Question.query.all()
    return render_template('index.html', title='Home', users=users, posts=posts, questions=questions)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)
# recruiter routes
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         if current_user.role == "Manager":
#             interviews = Interview.query.order_by(Interview.id)
#             grades = Grade.query.order_by(Grade.id)
#             return render_template('manager_candidates.html', interviews=interviews, grades=grades)
#         elif current_user.role == "Interviewer":
#             return render_template('interviewer_layout.html')
#         else:
#             candidates = Interview.query.order_by(Interview.candidate)
#             return render_template('all_candidates.html', candidates=candidates)
#
#     form = LoginForm()
#     if request.method == 'POST' and form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user and user.password == form.password.data:
#             login_user(user)
#             if current_user.role == "Manager":
#                 interviews = Interview.query.order_by(Interview.id)
#                 grades = Grade.query.order_by(Grade.id)
#                 return render_template('manager_candidates.html', interviews=interviews, grades=grades)
#             elif current_user.role == "Interviewer":
#                 return render_template('interviewer_layout.html')
#             else:
#                 candidates = Interview.query.order_by(Interview.candidate)
#                 return render_template('all_candidates.html', candidates=candidates)
#         else:
#             flash('Login Unsuccessful. Please check email and password', 'danger')
#
#     return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.route('/add_question/', methods=['GET', 'POST'])
@login_required
def add_question():
    form = AddQuestionForm()
    if form.validate_on_submit():
        q = Question(essence=form.essence.data, supposed_answer=form.supposed_answer.data,
                     max_grade=form.max_grade.data)
        db.session.add(q)
        db.session.commit()
        flash('Congratulations, you have just created a new question!')
        return redirect(url_for('questions'))
    return render_template('add_question.html', title='Question', form=form)


@app.route('/questions')
@login_required
def questions():
    qs = Question.query.all()
    return render_template('questions.html', title='Questions', qs=qs)


@app.route('/question/<id>')
@login_required
def question(id):
    q = Question.query.filter_by(id=id).first_or_404()
    return render_template('question.html', question=q)


@app.route('/edit_question/<id>', methods=['GET', 'POST'])
@login_required
def edit_question(id):
    q = Question.query.get_or_404(id)
    grade = Grade.query.filter_by(id=id).all()
    form = EditQuestionForm(grade)
    if form.validate_on_submit():
        q.essence = form.essence.data
        q.supposed_answer = form.supposed_answer.data
        q.max_grade = form.max_grade.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('questions'))
    elif request.method == 'GET':
        form.essence.data = q.essence
        form.supposed_answer.data = q.supposed_answer
        form.max_grade.data = q.max_grade
    return render_template('edit_question.html', title='Edit Question', form=form)


@app.route('/add_grade', methods=['GET', 'POST'])
@login_required
def add_grade():
    form = GradeForm()
    if form.validate_on_submit():
        g = Grade(grade=form.grade.data, rater_id=form.rater_id.data,
                  interview_id=form.interview_id.data, question_id=form.question_id.data)
        db.session.add(g)
        db.session.commit()
        flash('Congratulations, you have just created a new grade!')
        return redirect(url_for('grades'))
    return render_template('add_grade.html', title='Grade', form=form)


@app.route('/grades')
@login_required
def grades():
    gs = Grade.query.all()
    return render_template('grades.html', title='Grades', gs=gs)


@app.route('/grade/<id>')
@login_required
def grade(id):
    g = Grade.query.filter_by(id=id).first_or_404()
    return render_template('grade.html', grade=g)


@app.route('/edit_grade', methods=['GET', 'POST'])
@login_required
def edit_grade():
    form = EditGradeForm(request.form)
    if form.validate_on_submit():
        request.form.grade = form.grade.data
        request.form.rater_id = form.rater_id.data
        request.form.interview_id = form.interview_id.data
        request.form.question_id = form.question_id.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_grade'))
    elif request.method == 'GET':
        form.grade.data = request.form.grade
        form.rater_id.data = request.form.rater_id
        form.interview_id.data = request.form.interview_id
        form.question_id.data = request.form.question_id
    return render_template('edit_grade.html', title='Edit Grade', form=form)


@app.route('/add_interview', methods=['GET', 'POST'])
@login_required
def add_interview():
    form = AddInterviewForm()
    if form.validate_on_submit():
        inw = Interview(candidate=form.candidate.data, date=form.date.data, satrt_time=form.start_time.data,
                        end_time=form.end_time.data, questions=form.questions.data,
                        users=User.query.filter(User.id.in_(form.users.data)).all())
        db.session.add(inw)
        db.session.commit()
        flash('Congratulations, you have just created a new interview!')
        return redirect(url_for('interviews'))
    return render_template('add_interview.html', title='Add Interview', form=form)


@app.route('/interviews')
@login_required
def interviews():
    inws = Interview.query.all()
    return render_template('interviews.html', title='Interviews', inws=inws)


@app.route('/interview/<id>')
@login_required
def interview(id):
    inw = Interview.query.filter_by(id=id).first_or_404()
    return render_template('interview.html', interview=inw)


@app.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    form = BookinterviewForm()
    if form.validate_on_submit():

        # check time collision
        interviewcollisions = Interview.query.filter_by(
            date=datetime.combine(form.date.data, datetime.min.time())).filter_by(email=form.interviewers.data).all()
        print(len(interviewcollisions))
        for interviewcollision in interviewcollisions:
            # [a, b] overlaps with [x, y] iff b > x and a < y
            if (form.start_time.data < interviewcollision.end_time and (
                    form.end_time.data) > interviewcollision.start_time):
                flash(
                    f'The time from {interviewcollision.start_time} to {interviewcollision.end_time} is already booked by {Interviewer.query.filter_by(email=interviewcollision.email).first().email}.')
                return redirect(url_for('book'))

        interviewcollisions2 = Interview.query.filter_by(
            date=datetime.combine(form.date.data, datetime.min.time())).filter_by(
            bookerEmail=form.interviewers.data).all()
        print(len(interviewcollisions2))
        for interviewcollision in interviewcollisions2:
            # [a, b] overlaps with [x, y] iff b > x and a < y
            if (form.start_time.data < interviewcollision.end_time and (
                    form.end_time.data) > interviewcollision.start_time):
                flash(
                    f'The time from {interviewcollision.start_time} to {interviewcollision.end_time} is already booked by {Interviewer.query.filter_by(email=interviewcollision.bookerEmail).first().email}.')
                return redirect(url_for('book'))

        end_time = form.end_time.data

        interview = Interview(candidate=form.candidate.data, date=form.date.data, start_time=form.start_time.data,
                              end_time=form.end_time.data, email=form.interviewer.data)
        db.session.add(interview)

        db.session.commit()

        flash('Interview Scheduling success!')
        return redirect(url_for('index'))
    return render_template('book.html', title='Schedule Interviews', form=form)
