import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask
from config import Config
from flask_restful import Api
from flask_admin import Admin
from flask_admin.contrib import sqla
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
# login.login_view = 'login'
login.init_app(app)
ma = Marshmallow(app)
api = Api()
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='interview', template_mode='bootstrap3')

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

from app import routes, models, errors, forms, schema, api_routes

if not models.User.query.filter_by(is_admin=True).all():
    user = models.User(username="admin", is_admin=True)
    user.set_password("admin")
    db.session.add(user)
    db.session.commit()


class AdminModelView(sqla.ModelView):
    page_size = 50

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin
        return current_user.is_authenticated


class UserModelView(AdminModelView):

    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(AdminModelView(models.User, db.session))
admin.add_view(UserModelView(models.Grade, db.session))
admin.add_view(UserModelView(models.Interview, db.session))
admin.add_view(UserModelView(models.Question, db.session))

api.add_resource(api_routes.UserApi, '/api/user')
api.add_resource(api_routes.GradesApi, '/api/grade')
api.add_resource(api_routes.QuestionApi, '/api/question')
api.add_resource(api_routes.InterviewApi, '/api/interview')
api.add_resource(api_routes.LoginApi, '/api/login')
api.add_resource(api_routes.LogoutApi, '/api/logout')