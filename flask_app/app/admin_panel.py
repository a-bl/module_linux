from flask_admin.contrib import sqla
from flask_login import current_user

from app import admin, db
from app.models import User, Question, Interview, Grade


class AdminModelView(sqla.ModelView):
    page_size = 50
    form_args = {
        'password_hash': {
            "label": "Password"
        }
    }

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin
        return current_user.is_authenticated


class UserModelView(AdminModelView):

    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(AdminModelView(User, db.session))
admin.add_view(UserModelView(Question, db.session))
admin.add_view(UserModelView(Grade, db.session))
admin.add_view(UserModelView(Interview, db.session))
