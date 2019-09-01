# 模型

from .exts import db


class AdminToken(db.Model):
    __tablename__ = "admintoken"
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255))
    admin = db.Column(db.Integer, db.ForeignKey('admin.id'))
    outtime = db.Column(db.DateTime)

#
class Admin(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    token = db.relationship(AdminToken, backref='adminn', uselist=False)


# 管理登录日志
class Adminlog(db.Model):
    __tablename__ = 'adminlog'

    id = db.Column(db.Integer, primary_key=True)
    adminid = db.Column(db.ForeignKey('admin.id'), index=True)
    ip = db.Column(db.String(50))
    time = db.Column(db.DateTime)
    status = db.Column(db.Integer)

    admin = db.relationship('Admin', primaryjoin='Adminlog.adminid == Admin.id', backref='adminlogs')

# 标签和文章的中间表   只能这样建了不然为会报错啊~
class Alabel(db.Model):
    __tablename__ = 'alabel'

    id = db.Column(db.Integer, primary_key=True)
    articleid = db.Column(db.ForeignKey('article.id'), index=True)  # 文章id
    labelid = db.Column(db.ForeignKey('articlelabel.id'), index=True)  # 标签id

    article = db.relationship('Article', primaryjoin='Alabel.articleid == Article.id', backref='alabels')
    articlelabel = db.relationship('Articlelabel', primaryjoin='Alabel.labelid == Articlelabel.id', backref='alabels')

# 文章表
class Article(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.ForeignKey('user.id'), index=True)
    title = db.Column(db.String(255))
    msg = db.Column(db.String(15000))
    imgpath = db.Column(db.String(255))
    time = db.Column(db.DateTime)
    type = db.Column(db.ForeignKey('articletype.id'), index=True)  # 文章类型
    isshadow = db.Column(db.Boolean,default=False)
    status = db.Column(db.Boolean,default=False)
    readnum = db.Column(db.Integer,default=0)
    zan = db.Column(db.Integer,default=0)
    descri = db.Column(db.String(255))
    keywd = db.Column(db.String(255))

    articletype = db.relationship('Articletype', primaryjoin='Article.type == Articletype.id', backref='articles')
    user = db.relationship('User', primaryjoin='Article.userid == User.id', backref='articles')



# 文章标签  一个文章多个标签1:N
class Articlelabel(db.Model):
    __tablename__ = 'articlelabel'

    id = db.Column(db.Integer, primary_key=True)
    labelname = db.Column(db.String(50))

# 文章类型
class Articletype(db.Model):
    __tablename__ = 'articletype'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    othertitle = db.Column(db.String(50))
    # father = db.Column(db.Integer)
    info = db.Column(db.String(255))
    level = db.Column(db.Integer)   # 当前类型等级
    keywd = db.Column(db.String(255))
    father = db.Column(db.ForeignKey('articletype.id'), index=True)  # 选择父类型的id


# 文章评论
class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    articleid = db.Column(db.ForeignKey('article.id'), index=True)
    name = db.Column(db.String(50))
    msg = db.Column(db.String(500))
    time = db.Column(db.DateTime)

    article = db.relationship('Article', primaryjoin='Comment.articleid == Article.id', backref='comments')

#
class Gonggao(db.Model):
    __tablename__ = 'gonggao'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    msg = db.Column(db.String(5000))
    info = db.Column(db.String(255))
    isshadow = db.Column(db.Boolean)
    status = db.Column(db.Boolean)
    time = db.Column(db.DateTime)

# 图片相册
class Image(db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    userid = db.Column(db.ForeignKey('user.id'), index=True)
    path = db.Column(db.String(255))
    detail = db.Column(db.String(255))
    time = db.Column(db.DateTime)

    user = db.relationship('User', primaryjoin='Image.userid == User.id', backref='images')

# 留言
class Lmessage(db.Model):
    __tablename__ = 'lmessage'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    msg = db.Column(db.String(1500))
    msgback = db.Column(db.String(1500))
    time = db.Column(db.DateTime)

# 用户
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    QRcode = db.Column(db.String(200))
    msg = db.Column(db.String(5000))
    name = db.Column(db.String(50))
    birthday = db.Column(db.Date)
    icon = db.Column(db.String(255))
    sign = db.Column(db.String(255))
    registerdate = db.Column(db.DateTime)
    tel = db.Column(db.String(11))

# 用户登录日志
class Userlog(db.Model):
    __tablename__ = 'userlog'

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.ForeignKey('user.id'), index=True)
    ip = db.Column(db.String(20))
    time = db.Column(db.DateTime)
    status = db.Column(db.Boolean)

    user = db.relationship('User', primaryjoin='Userlog.userid == User.id', backref='userlogs')


class Youqinglianjie(db.Model):
    __tablename__ = 'youqinglianjie'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    webpath = db.Column(db.String(255))
    imgpath = db.Column(db.String(255))
    info = db.Column(db.String(255))
    target = db.Column(db.String(50))
    rel = db.Column(db.String(255))
    time = db.Column(db.DateTime)

