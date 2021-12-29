"""empty message

Revision ID: b7f8ce299336
Revises: a08edb71b211
Create Date: 2021-12-28 09:49:29.448631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7f8ce299336'
down_revision = 'a08edb71b211'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('interview',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('candidate', sa.String(length=120), nullable=False),
    sa.Column('final_grade', sa.Float(precision=2), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('start_time', sa.Time(), nullable=True),
    sa.Column('end_time', sa.Time(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('essence', sa.String(length=64), nullable=True),
    sa.Column('supposed_answer', sa.Text(), nullable=True),
    sa.Column('max_grade', sa.Integer(), nullable=True),
    sa.Column('short_description', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('first_name', sa.String(length=64), nullable=True),
    sa.Column('last_name', sa.String(length=64), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('grade',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.Column('interviewer_id', sa.Integer(), nullable=True),
    sa.Column('interview_id', sa.Integer(), nullable=True),
    sa.Column('grade', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['interview_id'], ['interview.id'], ),
    sa.ForeignKeyConstraint(['interviewer_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('interviews_question',
    sa.Column('interview_id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['interview_id'], ['interview.id'], ),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.PrimaryKeyConstraint('interview_id', 'question_id')
    )
    op.create_table('users_interview',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('interview_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['interview_id'], ['interview.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'interview_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_interview')
    op.drop_table('interviews_question')
    op.drop_table('grade')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('question')
    op.drop_table('interview')
    # ### end Alembic commands ###