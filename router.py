from forum.handler.UserHandler import AddUserHandler, SendEmail, ZhiFuBaoPayHandler, BuyHandler, AliPayNotify, \
    WeatherHandler, CheckHandler, IndexHandler, MessagesHandler, DownloadHandler, WeChatVerificationHandler

handlers = [
    ('/api/user/add', AddUserHandler),
    ('/', IndexHandler),
    ('/api/send_msg', SendEmail),
    ('/index', ZhiFuBaoPayHandler),
    ('/buy/(\d+)', BuyHandler),
    ('/aliPayNotify', AliPayNotify),
    ("/getWeather", WeatherHandler),
    ("/check", CheckHandler),
    ("/messages", MessagesHandler),
    ("/download", DownloadHandler),
    ("/wechat", WeChatVerificationHandler),
]
