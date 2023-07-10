"""empty message

Revision ID: 0dcc877584bc
Revises: 8900a3cf5ef1
Create Date: 2023-07-10 14:26:25.915893

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0dcc877584bc'
down_revision = '8900a3cf5ef1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('group', schema=None) as batch_op:
        batch_op.add_column(sa.Column('hand_raised', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('at_checkpoint', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('progress', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('max_progress', sa.Integer(), nullable=True))

    with op.batch_alter_table('labs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('num_questions', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('labs', schema=None) as batch_op:
        batch_op.drop_column('num_questions')

    with op.batch_alter_table('group', schema=None) as batch_op:
        batch_op.drop_column('max_progress')
        batch_op.drop_column('progress')
        batch_op.drop_column('at_checkpoint')
        batch_op.drop_column('hand_raised')

    # ### end Alembic commands ###
