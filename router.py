
from forum.handler.BaseHandler import IndexHandler
from forum.handler.UserHandler import AddUserHandler, SendEmail, ZhiFuBaoPayHandler, BuyHandler, AliPayNotify

handlers = [
    ('/api/user/add', AddUserHandler),
    ('/', IndexHandler),
    ('/api/send_msg', SendEmail),
    ('/index', ZhiFuBaoPayHandler),
    ('/buy/(\d+)', BuyHandler),
    ('/aliPayNotify', AliPayNotify),
]
