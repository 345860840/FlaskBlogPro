"""empty message

Revision ID: 2afd67efabca
Revises: e5deeeab230c
Create Date: 2019-08-31 11:13:32.890058

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2afd67efabca'
down_revision = 'e5deeeab230c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('articletype', sa.Column('keywd', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('articletype', 'keywd')
    # ### end Alembic commands ###
