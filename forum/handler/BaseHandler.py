from tornado import web


class BaseHandler(web.RequestHandler):
    def initialize(self):
        self.obj = self.application.obj
        self.redis = self.application.redis

    def set_default_headers(self):
        self.set_header('Access-Control-allow-Origin', '*')


class IndexHandler(web.RequestHandler):
    async def get(self):
        return self.finish({'msg': 'success', 'code': 200})
