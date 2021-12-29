from marshmallow import fields, validate

from app import ma, db
from app.models import User, Question, Interview, Grade


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ['password_hash']

    id = ma.auto_field()
    username = fields.Str(validate=[validate.Length(64)], required=True)
    email = fields.Str(required=True)
    first_name = fields.Str(validate=[validate.Length(64)], required=True)
    last_name = fields.Str(validate=[validate.Length(64)], required=True)
    password_hash = fields.Str(validate=[validate.Length(255)], required=True)
    is_admin = fields.Boolean(default=False, required=True)


class GradeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Grade

    id = ma.auto_field()
    question_id = fields.Int(required=True)
    question = fields.Nested("QuestionSchema", default=[], required=True)
    interviewer_id = fields.Int(required=True)
    interviewer = fields.Nested("UserSchema", default=[], required=True)
    interview_id = fields.Int(required=True)
    interview = fields.Nested("InterviewSchema", default=[], required=True)
    grade = fields.Int(required=True)


class QuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Question

    id = ma.auto_field()
    essence = fields.Str(required=True)
    supposed_answer = fields.Str(required=True, validate=validate.Length(64))
    max_grade = fields.Int(required=True)
    short_description = fields.Str(required=True, validate=validate.Length(140))


class InterviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Interview
        sqla_session = db.session

    id = ma.auto_field()
    candidate = fields.Str(required=True, validate=[validate.Length(64)])
    questions = fields.Nested("QuestionSchema", default=[], many=True, required=True)
    interviewers = fields.Nested("UserSchema", default=[], many=True, required=True)
    final_grade = fields.Decimal(rounding="2", required=True)
    