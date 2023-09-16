from forum.handler.BaseHandler import IndexHandler
from forum.handler.UserHandler import AddUserHandler, SendEmail

handlers = [
    ('/api/user/add', AddUserHandler),
    ('/', IndexHandler),
    ('/api/send_msg', SendEmail),
]
