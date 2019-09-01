from flask import Flask
from .views import blog, admin
from .exts import init_exts, RegexConverter


def create_app():
    app = Flask(__name__)

    # 配置数据库
    db_uri = 'mysql+pymysql://root:1234@localhost:3306/blogdb'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.url_map.converters['re'] = RegexConverter
    app.register_blueprint(blueprint=blog)  # 注册蓝图
    app.register_blueprint(blueprint=admin)  # 注册蓝图

    init_exts(app)  # 初始化插件

    return app

