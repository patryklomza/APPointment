"""empty message

Revision ID: 0ab073266b33
Revises: 36eee5f22dc3
Create Date: 2019-06-12 12:10:17.172666

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ab073266b33'
down_revision = '36eee5f22dc3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('visit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('visit_date', sa.Text(), nullable=True),
    sa.Column('visit_time', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_visit_visit_date'), 'visit', ['visit_date'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_visit_visit_date'), table_name='visit')
    op.drop_table('visit')
    # ### end Alembic commands ###
