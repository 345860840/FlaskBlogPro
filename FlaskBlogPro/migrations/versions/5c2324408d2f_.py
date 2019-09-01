"""empty message

Revision ID: 5c2324408d2f
Revises: ce6479f7532d
Create Date: 2019-08-31 19:17:54.642401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c2324408d2f'
down_revision = 'ce6479f7532d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('alabel_ibfk_1', 'alabel', type_='foreignkey')
    # op.create_foreign_key(None, 'alabel', 'article', ['articleid'], ['id'], ondelete='CASCADE')
    op.drop_constraint('comment_ibfk_1', 'comment', type_='foreignkey')
    # op.create_foreign_key(None, 'comment', 'article', ['articleid'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_constraint(None, 'comment', type_='foreignkey')
    op.create_foreign_key('comment_ibfk_1', 'comment', 'article', ['articleid'], ['id'])
    # op.drop_constraint(None, 'alabel', type_='foreignkey')
    op.create_foreign_key('alabel_ibfk_1', 'alabel', 'article', ['articleid'], ['id'])
    # ### end Alembic commands ###