from app import app, db
from app.models import User, Post, Interview, Question, Grade


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Interview': Interview, 'Question': Question, 'Grade': Grade}

if __name__ == "__main__":
    app.run("0.0.0.0", 5000)