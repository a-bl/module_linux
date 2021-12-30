from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Interview, Question, Grade
from app.forms import EditProfileForm, AddQuestionForm, EditQuestionForm, GradeForm, EditGradeForm, \
    AddInterviewForm, UserFrom


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@login_required
def admin_page():
    return redirect('/admin')


@app.route('/index')
@login_required
def index():
    users = User.query.all()
    return render_template('index.html', title='Home', users=users)


@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login_route'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout_route():
    logout_user()
    return redirect(url_for('login_route'))


# @login.unauthorized_handler
# def unauthorized_callback():
#     return redirect(url_for('login_route'))


@app.route('/register', methods=['GET', 'POST'])
def register_route():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, first_name=form.first_name.data,
                    last_name=form.last_name.data, email=form.email.data, is_admin=form.is_admin.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login_route'))
    return render_template('register.html', title='Register', form=form)


@app.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    form = UserFrom()
    if form.validate_on_submit():
        user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulation, you have just add a new user!')
        return redirect(url_for('users'))
    return render_template('add_user.html', form=form)


@app.route('/users')
@login_required
def users():
    users = User.query.all()
    return render_template('index.html', title='Users', users=users)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    questions = Question.query.all()
    grs = Grade.query.filter_by(interviewer_id=user.id).all()

    for interview in user.interviews:
        grades = Grade.query.filter_by(interview_id=interview.id).all()
        gs = []
        for grade in grades:
            gs.append(grade.grade)
        if len(gs) != 0:
            final_grade = sum(gs) / len(interview.interviewers) / (len(gs)/2 * 10)
            interview.final_grade = final_grade
            db.session.commit()
        # else:
        #     for question in interview.questions:
        #         return redirect(url_for('add_grade', username=user.username, question_id=question.id, interview_id=interview.id))

    for q in questions:
        grades = Grade.query.filter_by(question_id=q.id).all()
        if len(grades) != 0:
            max_grade = max([grade.grade for grade in grades])
            q.max_grade = max_grade
            db.session.commit()

    # interview = Interview.query.first()
    # interview.final_grade = final_grade
    # print(interview, interview.final_grade)
    # db.session.commit()
    # print(interview.final_grade)
    return render_template('user.html', title='Profile', user=user, grades=grs, questions=questions)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username, current_user.first_name, current_user.last_name)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('users'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.route('/add_question', methods=['GET', 'POST'])
@login_required
def add_question():
    form = AddQuestionForm()
    if form.validate_on_submit():
        _question = Question(essence=form.essence.data, supposed_answer=form.supposed_answer.data,
                             max_grade=0, short_description=form.short_description.data)
        db.session.add(_question)
        db.session.commit()
        flash('Congratulations, you have just created a new question!')
        return redirect(url_for('questions'))
    return render_template('add_question.html', title='Question', form=form)


@app.route('/questions')
@login_required
def questions():
    qs = db.session.query(Question).all()
    for q in qs:
        grades = Grade.query.filter_by(question_id=q.id).all()
        if len(grades) != 0:
            max_grade = max([grade.grade for grade in grades])
            q.max_grade = max_grade
            db.session.commit()
    return render_template('questions.html', title='Questions', qs=qs)


@app.route('/question/<id>')
@login_required
def question(id):
    q = Question.query.filter_by(id=id).first_or_404()
    grades = Grade.query.filter_by(question_id=q.id).all()
    if len(grades) != 0:
        max_grade = max([grade.grade for grade in grades])
        q.max_grade = max_grade
        db.session.commit()
    return render_template('question.html', question=q)


@app.route('/edit_question/<id>', methods=['GET', 'POST'])
@login_required
def edit_question(id):
    q = Question.query.get_or_404(id)
    form = EditQuestionForm()
    if form.validate_on_submit():
        q.essence = form.essence.data
        q.supposed_answer = form.supposed_answer.data
        q.short_description = form.short_description.data
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
    form = GradeForm.new()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.interviewers.data).first()
        question = Question.query.filter_by(id=form.questions.data).first()
        interview = Interview.query.filter_by(id=form.interviews.data).first()
        g = Grade(interviewer=user, question=question, interview=interview, grade=form.grade.data)
        db.session.add(g)
        db.session.commit()
        flash('Congratulations, you have just created a new grade!')
        return redirect(url_for('grades'))
    return render_template('add_grade.html', title='Grade', form=form)


@app.route('/add_grade/<username>/<question_id>/<interview_id>', methods=['GET', 'POST'])
@login_required
def add_user_grade(username, question_id, interview_id):
    form = GradeForm.new()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        question = Question.query.filter_by(id=question_id).first()
        interview = Interview.query.filter_by(id=interview_id).first()
        g = Grade(interviewer=user, question=question, interview=interview, grade=form.grade.data)
        db.session.add(g)
        db.session.commit()
        flash('Congratulations, you have just created a new grade!')
        return redirect(url_for('user', username=user.username))
    elif request.method == 'GET':
        form.interviewers.data = request.args.get('interviewer', '')
        form.interviews.data = request.args.get('interview', '')
        form.questions.data = request.args.get('question', '')
        form.grade.data = request.args.get('grade', '')
    # g = Grade(grade=grade, interviews=interviews, interviewers=interviewers, questions=questions)
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


@app.route('/edit_grade/<id>', methods=['GET', 'POST'])
@login_required
def edit_grade(id):
    g = db.session.query(Grade).get(id)
    # g = Grade.query.filter_by(id=id).first_or_404()
    form = EditGradeForm.new()
    if form.validate_on_submit():
        # g.grade = form.grade.data
        g.grade = request.form['grade']
        # g.interviewer = form.interviewers.data
        g.interviewer = request.form['interviewers']
        # g.interview = form.interviews.data
        g.interview = request.form['interviews']
        # g.question = form.questions.data
        g.question = request.form['questions']
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('grades'))
    elif request.method == 'GET':
        form.interviewers.data = User.query.filter_by(id=g.interviewer_id).all()[0]
        # form.interviewers.default = g.interviewer

        form.interviews.data = Interview.query.filter_by(id=g.interview_id).all()[0]
        # form.interviews.default = g.interview

        form.questions.data = Question.query.filter_by(id=g.question_id).all()[0]
        # form.questions.default = g.question

        form.grade.data = g.grade
        # form.interviewers.data = g.interview
        # form.interviews.data = g.interview
        # form.questions.data = g.question
    return render_template('edit_grade.html', title='Edit Grade', form=form)


@app.route('/add_interview', methods=['GET', 'POST'])
@login_required
def add_interview():
    form = AddInterviewForm().new()
    if form.validate_on_submit():
        questions = []
        interviewers = []
        max_grades = []
        for question_id in form.questions.data:
            question = Question.query.filter_by(id=question_id).first()
            max_grade = question.max_grade
            questions.append(question)
            max_grades.append(max_grade)
        for interviewer_id in form.interviewers.data:
            user = User.query.filter_by(id=interviewer_id).first()
            interviewers.append(user)
        # final_grade = sum(list(map(int, form.questions.data))) / len(form.interviewers.data) / (len(form.questions.data) * max(max_grades))
        interview = Interview(candidate=form.candidate.data, questions=questions, interviewers=interviewers, final_grade=0)
                              # date=form.date.data, start_time=form.start_time.data, end_time=form.end_time.data)
        all = [interview]
        # for user in interviewers:
        #     for question in questions:
        #         grade = Grade(question=question, interviewer=user, interview=interview)
        #         all.append(grade)
        db.session.add_all(all)
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