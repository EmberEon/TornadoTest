import tornado.ioloop
import tornado.web
import traceback
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.request.AlipayTradeAppPayRequest import AlipayTradeAppPayRequest

# 替换为您的支付宝应用配置信息
APP_ID = '9021000128661576'
APP_PRIVATE_KEY = 'MIIEogIBAAKCAQEAhn+LHXvviQVs99n6vYET0oz927RbDXOkxC10QYQS4jccG7U/DDwOM7bNhYkaXb7KHDoCViQV5RYX5hDzLmhO8CiW7elrNSJIdeewJAZcqeLmVZa4G69IMxoDNWwF0VzUB8VdkmcZKNGt08ejdGP9bHXQkS8WV0TU+QUclgnT2yoF38mYjB4IiNh8kbHcvmkdNVYbCZUcxf3F29tUfWB94pnxvCrD/rPVdpKARj4/ItmT4stCDQLtAYJmHCNAhrViNQKXnvBcqKheWwd43g90laD3u2yrOg3nBT2DhOKwJhZ65zmyHN1XkN/W7p9L+jsX5lqSNw45nF4V+PQJjMmsUQIDAQABAoIBABnGMVOaH4IjjwlENX/BT5omuLM0sco3IhkSGNhBRhkhtHo+1nEyxQn1+xae+nWCjVqxZyc4zRVUkYneL6vyA0aUkK/Q7mGFS1uE5cVRjspjl/5I3sk3Yt+gGYNQSyEe5+cBVHgs165x2BzgghtY2gTB4xEfc+mPYDzEVQEPqxCxiihKvLOUNDqu/YoDtWidejV5FyFc8hXEYfmdw59yYFFbLMtbHZyP+k0TDliLWtnNP9x7aRFw8VxvRCrIIcJWvw9fVJSNb9ZOJI63eDv8vRQOrKfkk7270MMZn85Ck4pOUG4Pr79TFgxFryFXVLqvQhuIMc/eiK440HhlBs4eSZ0CgYEA06o16lTu4Lwxly1yPeFzH5qcNKcUS1R0i7Jxrw/VRR8WQH+Bl3QJ015HlSgjc8UgX50hgTUtPlF6YqQD22OtsLHKxXWvXj5Zg2dP0i9fjJ6ds0Bmzrt1BratJ1FFNNNzXRYRrWWN8YkcNQW5GUZmTGwK8tdDhU0tqRfgEHg21L8CgYEAoquKPjNAhr/YsGn938ydjIlaY7xfr3L+gBk7t3aYIST1ktBC/Z/uyS6qsXr6s8dkFp6Cr84m9OG21UIZeQWV5ykIPwNRvciVXZg2ySmU4Dkkj2Ehd+ohdTZR2FIkbS3JR8Ja9h78SUgpe2d+V1opx3IxLrto7ra/xTfh6AQkcu8CgYBhYPKTD2YjAJH0ElV3wKwdQx1QX/nHOmCwEHWa67bbqRSssbymOB15H+vg5GmDDpL5Sioq7pMVE5kxnnGj0nULUJCQTbdTrW2zNamUcnUMFcFJwXxK6hVJ9GsvJoWnawytK8UQOCOYltLiVfK1fRz9Vcuns3996WbzX2eXTCc1swKBgDwD084c9JqCXzy+7hZKlHnMFxgi4J6Ha5PxO1H1pCzeSOfwhDa0cdGxsPIn8CSx1KBvvMGF6mOAfwbxCxrWT7boMY2l+NtvDIRqaxQOjkmna3CmokVukQeAkfOgYqYRNWiPMSYKyoNy5zMLPNaXgkB+Rdz68bzYman2cxc5qATrAoGAFZWLhRl6vp/PM2jwsVRH9hhyeFH0dhJS0rDh6lj7ryFWrzY16colRJcPDxXq4cY5mskSij5EXLsm6kYeQTfouHyMt6UDJ1zXAQPm3a9if/ROpNpPeAfwkfol1H1iDD99r/RqVZhleYuJxf2VV9hgSPZC5KXaTvlbrRilzDNlbr0='
ALIPAY_PUBLIC_KEY = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAh1+YtCLltReM7c7ZviFdk9xjbfC4OITQUNQH5p7GTJkbl8CbUyuB8/8wYKum0WJUJbU6BhJWxKWWsC1JQCe8hZWUKmZB6MC/pJwuBzc8EBqavQXOQchKrNhowtVMa3/sVK6Sq8niC63befn0mn2Zu5bwuDTBVp68q12SP/048Rx43q7qfOIVTNZRr0R5AvgfOQi4oXAlTEsmNwYfjgTlHeZtS3kcs+M6S+ZIUeMqRIlt+E/kDuTTLP+sw2CuyylBznzilppZ1HIwNZJcKy9sGzis/7GMdt74op4Sw1A9Jrm9xGrSzzgoUEWiXis1tJ1VeLDSgUzoiegxAtDUJeVOswIDAQAB'

# 创建AlipayClient配置
alipay_client_config = AlipayClientConfig()
alipay_client_config.server_url = 'https://openapi-sandbox.dl.alipaydev.com/gateway.do'
alipay_client_config.app_id = APP_ID
alipay_client_config.app_private_key = APP_PRIVATE_KEY
alipay_client_config.alipay_public_key = ALIPAY_PUBLIC_KEY

# 创建AlipayClient实例
alipay_client = DefaultAlipayClient(alipay_client_config=alipay_client_config)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # 构造支付参数
        model = AlipayTradeAppPayRequest()
        model.total_amount = 1  # 订单总金额
        model.timeout_express = "90m"  # 订单超时时间
        model.subject = "查尔斯顿"  # 订单标题
        model.body = "测试"  # 订单描述
        model.out_trade_no = "12346546513220"  # 商户订单号

        # 调用支付宝接口生成支付链接
        try:
            response = alipay_client.page_execute(model, http_method="GET")
            # self.write(response)
            self.redirect(response)
        except Exception as e:
            traceback.print_exc()
            self.write("Failed to create Alipay payment link")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8002)
    tornado.ioloop.IOLoop.current().start()
