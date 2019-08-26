# 模型

from .exts import db


class User(db.Model):
    # 表名
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True)
    age = db.Column(db.Integer, default=1)


