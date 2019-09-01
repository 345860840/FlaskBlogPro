# 扩展的第三方插件
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache
from werkzeug.routing import BaseConverter

db = SQLAlchemy()  # ORM
migrate = Migrate()  # 数据迁移
cache = Cache(config={
       'CACHE_TYPE': 'simple',
  })

# 初始化插件
def init_exts(app):
    db.init_app(app)
    migrate.init_app(app=app, db=db)
    cache.init_app(app=app)


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        # 将接受的第1个参数当作匹配规则进行保存
        self.regex = args[0]