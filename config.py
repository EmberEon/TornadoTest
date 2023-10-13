import os

# 获取当前项目的目录
base_url = os.path.dirname(__file__)
settings = {
    'static_path': os.path.join(base_url, 'static'),
    'static_url_prefix': '/static/',
    'debug': True
}
port = 8001

mysql = {
    'database': 'forum',
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '123456',
}

email = {
    'uname': '1419273079@qq.com',
    'password': 'yjfviaqbfooegdfe'
}

ali_yun_conf = {
    'ALIBABA_CLOUD_ACCESS_KEY_ID': 'LTAI5tBezMjB9aGR9r38q2w8',
    'ALIBABA_CLOUD_ACCESS_KEY_SECRET': 'CFxeA1oglkGBaR9F6t7gEToZDihJWK'
}
