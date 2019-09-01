"""empty message

Revision ID: e5deeeab230c
Revises: 7e5312453ba5
Create Date: 2019-08-31 10:20:36.226363

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5deeeab230c'
down_revision = '7e5312453ba5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('articletype', sa.Column('father', sa.Integer(), nullable=True))
    op.add_column('articletype', sa.Column('level', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_articletype_father'), 'articletype', ['father'], unique=False)
    op.create_foreign_key(None, 'articletype', 'articletype', ['father'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'articletype', type_='foreignkey')
    op.drop_index(op.f('ix_articletype_father'), table_name='articletype')
    op.drop_column('articletype', 'level')
    op.drop_column('articletype', 'father')
    # ### end Alembic commands ###
