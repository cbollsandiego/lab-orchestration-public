"""empty message

Revision ID: b7f47f79ddee
Revises: 
Create Date: 2023-08-08 15:33:16.508649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7f47f79ddee'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('create_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('role', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('labs',
    sa.Column('lab_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('questions', sa.String(), nullable=False),
    sa.Column('num_questions', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('lab_id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('role', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('course',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('course_name', sa.String(length=100), nullable=False),
    sa.Column('semester', sa.String(), nullable=True),
    sa.Column('section_num', sa.Integer(), nullable=True),
    sa.Column('course_instructor', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_instructor'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('session',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('lab_id', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['lab_id'], ['labs.lab_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_course',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group_name', sa.String(length=100), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('session_id', sa.Integer(), nullable=True),
    sa.Column('hand_raised', sa.Boolean(), nullable=True),
    sa.Column('at_checkpoint', sa.Boolean(), nullable=True),
    sa.Column('progress', sa.Integer(), nullable=True),
    sa.Column('max_progress', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['session_id'], ['session.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('student_answers',
    sa.Column('answer_id', sa.Integer(), nullable=False),
    sa.Column('question_num', sa.Integer(), nullable=True),
    sa.Column('group_name', sa.String(), nullable=True),
    sa.Column('session_id', sa.Integer(), nullable=True),
    sa.Column('submit_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('saved_answer', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['session_id'], ['session.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('answer_id')
    )
    op.create_table('user_group',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_group')
    op.drop_table('student_answers')
    op.drop_table('group')
    op.drop_table('user_course')
    op.drop_table('session')
    op.drop_table('course')
    op.drop_table('user')
    op.drop_table('labs')
    op.drop_table('create_user')
    # ### end Alembic commands ###