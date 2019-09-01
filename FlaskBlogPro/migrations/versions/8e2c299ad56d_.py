"""empty message

Revision ID: 8e2c299ad56d
Revises: 6e8e5c75c3ba
Create Date: 2019-08-30 19:55:35.608580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e2c299ad56d'
down_revision = '6e8e5c75c3ba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('descri', sa.String(length=255), nullable=True))
    op.add_column('article', sa.Column('keywd', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article', 'keywd')
    op.drop_column('article', 'descri')
    # ### end Alembic commands ###