"""empty message

Revision ID: ab50197dcd36
Revises: 5c2324408d2f
Create Date: 2019-08-31 19:43:18.193543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab50197dcd36'
down_revision = '5c2324408d2f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('alabel_ibfk_3', 'alabel', type_='foreignkey')
    op.create_foreign_key(None, 'alabel', 'article', ['articleid'], ['id'])
    op.drop_constraint('comment_ibfk_1', 'comment', type_='foreignkey')
    op.create_foreign_key(None, 'comment', 'article', ['articleid'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.create_foreign_key('comment_ibfk_1', 'comment', 'article', ['articleid'], ['id'], ondelete='CASCADE')
    op.drop_constraint(None, 'alabel', type_='foreignkey')
    op.create_foreign_key('alabel_ibfk_3', 'alabel', 'article', ['articleid'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###