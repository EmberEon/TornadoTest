from tornado import web
from configs.config import settings, port, mysql
import peewee_async
import redis

db = peewee_async.MySQLDatabase(**mysql)
obj = peewee_async.Manager(db)
r = redis.Redis(host='192.168.232.92', port=26379, db=0, password='Cmz@123456')
from router import handlers


class Application(web.Application):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        self.db = db
        self.obj = obj
        self.redis = r


def create_app():
    app = Application(handlers, **settings)
    app.listen(port)
    return app
