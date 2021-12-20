from app import app, db
from app.models import User, UserInfo


@app.route('/')
def main_page():
    u = UserInfo.query.all()
    user = User.query.all()
    return f"{user}, {u}"


@app.route('/a')
def a():
    u = UserInfo.query.first()
    u.admin = False
    db.session.commit()
    return "done"