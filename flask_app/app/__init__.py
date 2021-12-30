import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, redirect
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
admin = Admin(app, name='Interview Platform', template_mode='bootstrap3')

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


@login.unauthorized_handler
def unauthorized_callback():
    # return {"error": "you need to login first"}
    return redirect('/login')


from app import routes, models, errors, forms, schema, api_routes
from app import admin_panel

if not models.User.query.filter_by(is_admin=True).all():
    user = models.User(username="admin", is_admin=True)
    user.set_password("admin")
    db.session.add(user)
    db.session.commit()
