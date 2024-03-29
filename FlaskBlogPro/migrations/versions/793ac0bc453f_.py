"""empty message

Revision ID: 793ac0bc453f
Revises: 
Create Date: 2019-08-27 19:31:12.659073

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '793ac0bc453f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('articlelabel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('labelname', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('articletype',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=True),
    sa.Column('othertitle', sa.String(length=50), nullable=True),
    sa.Column('father', sa.Integer(), nullable=True),
    sa.Column('info', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('gonggao',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=True),
    sa.Column('msg', sa.String(length=5000), nullable=True),
    sa.Column('info', sa.String(length=255), nullable=True),
    sa.Column('isshadow', sa.Boolean(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lmessage',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('msg', sa.String(length=1500), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=50), nullable=True),
    sa.Column('QRcode', sa.String(length=200), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('icon', sa.String(length=255), nullable=True),
    sa.Column('sign', sa.String(length=255), nullable=True),
    sa.Column('registerdate', sa.DateTime(), nullable=True),
    sa.Column('tel', sa.String(length=11), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('youqinglianjie',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('webpath', sa.String(length=255), nullable=True),
    sa.Column('imgpath', sa.String(length=255), nullable=True),
    sa.Column('info', sa.String(length=255), nullable=True),
    sa.Column('target', sa.String(length=50), nullable=True),
    sa.Column('rel', sa.String(length=255), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('aboutme',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userid', sa.Integer(), nullable=False),
    sa.Column('imgpath', sa.String(length=255), nullable=True),
    sa.Column('msg', sa.String(length=5000), nullable=True),
    sa.Column('info', sa.String(length=255), nullable=True),
    sa.Column('title', sa.String(length=50), nullable=True),
    sa.Column('yuming', sa.String(length=50), nullable=True),
    sa.Column('beianhao', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['userid'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id', 'userid')
    )
    op.create_index(op.f('ix_aboutme_userid'), 'aboutme', ['userid'], unique=False)
    op.create_table('adminlog',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('adminid', sa.Integer(), nullable=True),
    sa.Column('ip', sa.String(length=50), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['adminid'], ['admin.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_adminlog_adminid'), 'adminlog', ['adminid'], unique=False)
    op.create_table('article',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userid', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('msg', sa.String(length=5000), nullable=True),
    sa.Column('imgpath', sa.String(length=255), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('isshadow', sa.Boolean(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('readnum', sa.Integer(), nullable=True),
    sa.Column('zan', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['type'], ['articletype.id'], ),
    sa.ForeignKeyConstraint(['userid'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_article_type'), 'article', ['type'], unique=False)
    op.create_index(op.f('ix_article_userid'), 'article', ['userid'], unique=False)
    op.create_table('image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('userid', sa.Integer(), nullable=True),
    sa.Column('path', sa.String(length=255), nullable=True),
    sa.Column('detail', sa.String(length=255), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['userid'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_image_userid'), 'image', ['userid'], unique=False)
    op.create_table('userlog',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userid', sa.Integer(), nullable=True),
    sa.Column('ip', sa.String(length=20), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['userid'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_userlog_userid'), 'userlog', ['userid'], unique=False)
    op.create_table('alabel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('articleid', sa.Integer(), nullable=True),
    sa.Column('labelid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['articleid'], ['article.id'], ),
    sa.ForeignKeyConstraint(['labelid'], ['articlelabel.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_alabel_articleid'), 'alabel', ['articleid'], unique=False)
    op.create_index(op.f('ix_alabel_labelid'), 'alabel', ['labelid'], unique=False)
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('articleid', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('msg', sa.String(length=500), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['articleid'], ['article.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comment_articleid'), 'comment', ['articleid'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_comment_articleid'), table_name='comment')
    op.drop_table('comment')
    op.drop_index(op.f('ix_alabel_labelid'), table_name='alabel')
    op.drop_index(op.f('ix_alabel_articleid'), table_name='alabel')
    op.drop_table('alabel')
    op.drop_index(op.f('ix_userlog_userid'), table_name='userlog')
    op.drop_table('userlog')
    op.drop_index(op.f('ix_image_userid'), table_name='image')
    op.drop_table('image')
    op.drop_index(op.f('ix_article_userid'), table_name='article')
    op.drop_index(op.f('ix_article_type'), table_name='article')
    op.drop_table('article')
    op.drop_index(op.f('ix_adminlog_adminid'), table_name='adminlog')
    op.drop_table('adminlog')
    op.drop_index(op.f('ix_aboutme_userid'), table_name='aboutme')
    op.drop_table('aboutme')
    op.drop_table('youqinglianjie')
    op.drop_table('user')
    op.drop_table('lmessage')
    op.drop_table('gonggao')
    op.drop_table('articletype')
    op.drop_table('articlelabel')
    op.drop_table('admin')
    # ### end Alembic commands ###
