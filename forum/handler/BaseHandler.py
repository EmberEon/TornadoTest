from tornado import web


class BaseHandler(web.RequestHandler):
    def initialize(self):
        self.obj = self.application.obj
        self.redis = self.application.redis

    def set_default_headers(self):
        self.set_header('Access-Control-allow-Origin', '*')

    async def write_json(self, status=1, data=None, desc="", ex_fun=None, param=None):
        """
        :param status: 相应状态 默认OK
        :param data: 相应数据 默认null
        :param desc: 相应描述 默认为响应状态的默认描述
        :param ex_fun: 响应后需要执行的方法 必须为async异步/协程方法
        :param param: ex_fun响应方法的参数
        :return:
        """
        self.write({'status': status, 'desc': desc or "-1", 'data': data or None})
        self.finish()
        callable(ex_fun) and await ex_fun(*param)
        raise web.Finish


class IndexHandler(web.RequestHandler):
    async def get(self):
        return self.finish({'msg': 'success', 'code': 200})
