import zmail


def send_mail(from_email, passwd, to_email, subject, txt):
    # Send mail
    maiil_server = zmail.server(from_email, passwd)
    maiil_server.send_mail(to_email, {'subject': subject, 'content_text': txt})
    # maiil_server.send_mail('2175738754@qq.com', {'subject': 'Hello!', 'content_text': 'By zmail.'})
    # maiil_server.send_mail('2175738754@qq.com', {'subject': '臭宝，我在测试刚学的邮件发送功能，可忽略 小伙子', 'content_text': '猛男岑大哥.'})
