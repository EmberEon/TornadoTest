import logging
import traceback

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.FileItem import FileItem
from alipay.aop.api.domain.AlipayTradeAppPayModel import AlipayTradeAppPayModel
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.domain.AlipayTradePayModel import AlipayTradePayModel
from alipay.aop.api.domain.GoodsDetail import GoodsDetail
from alipay.aop.api.domain.SettleDetailInfo import SettleDetailInfo
from alipay.aop.api.domain.SettleInfo import SettleInfo
from alipay.aop.api.domain.SubMerchant import SubMerchant
from alipay.aop.api.request.AlipayOfflineMaterialImageUploadRequest import AlipayOfflineMaterialImageUploadRequest
from alipay.aop.api.request.AlipayTradeAppPayRequest import AlipayTradeAppPayRequest
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.request.AlipayTradePayRequest import AlipayTradePayRequest
from alipay.aop.api.response.AlipayOfflineMaterialImageUploadResponse import AlipayOfflineMaterialImageUploadResponse
from alipay.aop.api.response.AlipayTradePayResponse import AlipayTradePayResponse
from alipay.aop.api.request.AlipayTradeQueryRequest import AlipayTradeQueryRequest, AlipayTradeQueryModel
from alipay.aop.api.response.AlipayTradeQueryResponse import AlipayTradeQueryResponse

import os
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a',)
logger = logging.getLogger('')


def make_zhi_fu_bao_url(seller_id="seller_id", body="body", subject="subject", total_amount=0, timeout_express="90m", out_trade_no="201800000001201"):
    """
    设置配置，包括支付宝网关地址、app_id、应用私钥、支付宝公钥等，其他配置值可以查看AlipayClientConfig的定义。
    """
    alipay_client_config = AlipayClientConfig()
    alipay_client_config.server_url = 'https://openapi-sandbox.dl.alipaydev.com/gateway.do'
    alipay_client_config.app_id = '9021000128661576'
    alipay_client_config.app_private_key = 'MIIEogIBAAKCAQEAhn+LHXvviQVs99n6vYET0oz927RbDXOkxC10QYQS4jccG7U/DDwOM7bNhYkaXb7KHDoCViQV5RYX5hDzLmhO8CiW7elrNSJIdeewJAZcqeLmVZa4G69IMxoDNWwF0VzUB8VdkmcZKNGt08ejdGP9bHXQkS8WV0TU+QUclgnT2yoF38mYjB4IiNh8kbHcvmkdNVYbCZUcxf3F29tUfWB94pnxvCrD/rPVdpKARj4/ItmT4stCDQLtAYJmHCNAhrViNQKXnvBcqKheWwd43g90laD3u2yrOg3nBT2DhOKwJhZ65zmyHN1XkN/W7p9L+jsX5lqSNw45nF4V+PQJjMmsUQIDAQABAoIBABnGMVOaH4IjjwlENX/BT5omuLM0sco3IhkSGNhBRhkhtHo+1nEyxQn1+xae+nWCjVqxZyc4zRVUkYneL6vyA0aUkK/Q7mGFS1uE5cVRjspjl/5I3sk3Yt+gGYNQSyEe5+cBVHgs165x2BzgghtY2gTB4xEfc+mPYDzEVQEPqxCxiihKvLOUNDqu/YoDtWidejV5FyFc8hXEYfmdw59yYFFbLMtbHZyP+k0TDliLWtnNP9x7aRFw8VxvRCrIIcJWvw9fVJSNb9ZOJI63eDv8vRQOrKfkk7270MMZn85Ck4pOUG4Pr79TFgxFryFXVLqvQhuIMc/eiK440HhlBs4eSZ0CgYEA06o16lTu4Lwxly1yPeFzH5qcNKcUS1R0i7Jxrw/VRR8WQH+Bl3QJ015HlSgjc8UgX50hgTUtPlF6YqQD22OtsLHKxXWvXj5Zg2dP0i9fjJ6ds0Bmzrt1BratJ1FFNNNzXRYRrWWN8YkcNQW5GUZmTGwK8tdDhU0tqRfgEHg21L8CgYEAoquKPjNAhr/YsGn938ydjIlaY7xfr3L+gBk7t3aYIST1ktBC/Z/uyS6qsXr6s8dkFp6Cr84m9OG21UIZeQWV5ykIPwNRvciVXZg2ySmU4Dkkj2Ehd+ohdTZR2FIkbS3JR8Ja9h78SUgpe2d+V1opx3IxLrto7ra/xTfh6AQkcu8CgYBhYPKTD2YjAJH0ElV3wKwdQx1QX/nHOmCwEHWa67bbqRSssbymOB15H+vg5GmDDpL5Sioq7pMVE5kxnnGj0nULUJCQTbdTrW2zNamUcnUMFcFJwXxK6hVJ9GsvJoWnawytK8UQOCOYltLiVfK1fRz9Vcuns3996WbzX2eXTCc1swKBgDwD084c9JqCXzy+7hZKlHnMFxgi4J6Ha5PxO1H1pCzeSOfwhDa0cdGxsPIn8CSx1KBvvMGF6mOAfwbxCxrWT7boMY2l+NtvDIRqaxQOjkmna3CmokVukQeAkfOgYqYRNWiPMSYKyoNy5zMLPNaXgkB+Rdz68bzYman2cxc5qATrAoGAFZWLhRl6vp/PM2jwsVRH9hhyeFH0dhJS0rDh6lj7ryFWrzY16colRJcPDxXq4cY5mskSij5EXLsm6kYeQTfouHyMt6UDJ1zXAQPm3a9if/ROpNpPeAfwkfol1H1iDD99r/RqVZhleYuJxf2VV9hgSPZC5KXaTvlbrRilzDNlbr0='
    alipay_client_config.alipay_public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAh1+YtCLltReM7c7ZviFdk9xjbfC4OITQUNQH5p7GTJkbl8CbUyuB8/8wYKum0WJUJbU6BhJWxKWWsC1JQCe8hZWUKmZB6MC/pJwuBzc8EBqavQXOQchKrNhowtVMa3/sVK6Sq8niC63befn0mn2Zu5bwuDTBVp68q12SP/048Rx43q7qfOIVTNZRr0R5AvgfOQi4oXAlTEsmNwYfjgTlHeZtS3kcs+M6S+ZIUeMqRIlt+E/kDuTTLP+sw2CuyylBznzilppZ1HIwNZJcKy9sGzis/7GMdt74op4Sw1A9Jrm9xGrSzzgoUEWiXis1tJ1VeLDSgUzoiegxAtDUJeVOswIDAQAB'

    """
    得到客户端对象。
    注意，一个alipay_client_config对象对应一个DefaultAlipayClient，定义DefaultAlipayClient对象后，alipay_client_config不得修改，如果想使用不同的配置，请定义不同的DefaultAlipayClient。
    logger参数用于打印日志，不传则不打印，建议传递。
    """
    client = DefaultAlipayClient(alipay_client_config=alipay_client_config, logger=logger)

    """
    构造唤起支付宝客户端支付时传递的请求串示例：alipay.trade.app.pay
    """
    model = AlipayTradeAppPayModel()
    model.timeout_express = timeout_express
    model.total_amount = total_amount #total_amount
    model.seller_id = "2088721019379584"  #跟项目走
    model.product_code = "QUICK_MSECURITY_PAY"
    model.body = body
    model.subject = subject
    model.out_trade_no = out_trade_no
    request = AlipayTradeAppPayRequest(biz_model=model)
    request.notify_url = "https://mjweb.0858sy.com/aliPayNotify"
    response = client.sdk_execute(request)
    print("alipay.trade.app.pay response:" + response)
    return response


def queryalipay(order_id):
    alipay_client_config = AlipayClientConfig()
    alipay_client_config.server_url = 'https://openapi-sandbox.dl.alipaydev.com/gateway.do'
    alipay_client_config.app_id = '9021000128661576'
    alipay_client_config.app_private_key = 'MIIEogIBAAKCAQEAhn+LHXvviQVs99n6vYET0oz927RbDXOkxC10QYQS4jccG7U/DDwOM7bNhYkaXb7KHDoCViQV5RYX5hDzLmhO8CiW7elrNSJIdeewJAZcqeLmVZa4G69IMxoDNWwF0VzUB8VdkmcZKNGt08ejdGP9bHXQkS8WV0TU+QUclgnT2yoF38mYjB4IiNh8kbHcvmkdNVYbCZUcxf3F29tUfWB94pnxvCrD/rPVdpKARj4/ItmT4stCDQLtAYJmHCNAhrViNQKXnvBcqKheWwd43g90laD3u2yrOg3nBT2DhOKwJhZ65zmyHN1XkN/W7p9L+jsX5lqSNw45nF4V+PQJjMmsUQIDAQABAoIBABnGMVOaH4IjjwlENX/BT5omuLM0sco3IhkSGNhBRhkhtHo+1nEyxQn1+xae+nWCjVqxZyc4zRVUkYneL6vyA0aUkK/Q7mGFS1uE5cVRjspjl/5I3sk3Yt+gGYNQSyEe5+cBVHgs165x2BzgghtY2gTB4xEfc+mPYDzEVQEPqxCxiihKvLOUNDqu/YoDtWidejV5FyFc8hXEYfmdw59yYFFbLMtbHZyP+k0TDliLWtnNP9x7aRFw8VxvRCrIIcJWvw9fVJSNb9ZOJI63eDv8vRQOrKfkk7270MMZn85Ck4pOUG4Pr79TFgxFryFXVLqvQhuIMc/eiK440HhlBs4eSZ0CgYEA06o16lTu4Lwxly1yPeFzH5qcNKcUS1R0i7Jxrw/VRR8WQH+Bl3QJ015HlSgjc8UgX50hgTUtPlF6YqQD22OtsLHKxXWvXj5Zg2dP0i9fjJ6ds0Bmzrt1BratJ1FFNNNzXRYRrWWN8YkcNQW5GUZmTGwK8tdDhU0tqRfgEHg21L8CgYEAoquKPjNAhr/YsGn938ydjIlaY7xfr3L+gBk7t3aYIST1ktBC/Z/uyS6qsXr6s8dkFp6Cr84m9OG21UIZeQWV5ykIPwNRvciVXZg2ySmU4Dkkj2Ehd+ohdTZR2FIkbS3JR8Ja9h78SUgpe2d+V1opx3IxLrto7ra/xTfh6AQkcu8CgYBhYPKTD2YjAJH0ElV3wKwdQx1QX/nHOmCwEHWa67bbqRSssbymOB15H+vg5GmDDpL5Sioq7pMVE5kxnnGj0nULUJCQTbdTrW2zNamUcnUMFcFJwXxK6hVJ9GsvJoWnawytK8UQOCOYltLiVfK1fRz9Vcuns3996WbzX2eXTCc1swKBgDwD084c9JqCXzy+7hZKlHnMFxgi4J6Ha5PxO1H1pCzeSOfwhDa0cdGxsPIn8CSx1KBvvMGF6mOAfwbxCxrWT7boMY2l+NtvDIRqaxQOjkmna3CmokVukQeAkfOgYqYRNWiPMSYKyoNy5zMLPNaXgkB+Rdz68bzYman2cxc5qATrAoGAFZWLhRl6vp/PM2jwsVRH9hhyeFH0dhJS0rDh6lj7ryFWrzY16colRJcPDxXq4cY5mskSij5EXLsm6kYeQTfouHyMt6UDJ1zXAQPm3a9if/ROpNpPeAfwkfol1H1iDD99r/RqVZhleYuJxf2VV9hgSPZC5KXaTvlbrRilzDNlbr0='
    alipay_client_config.alipay_public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAh1+YtCLltReM7c7ZviFdk9xjbfC4OITQUNQH5p7GTJkbl8CbUyuB8/8wYKum0WJUJbU6BhJWxKWWsC1JQCe8hZWUKmZB6MC/pJwuBzc8EBqavQXOQchKrNhowtVMa3/sVK6Sq8niC63befn0mn2Zu5bwuDTBVp68q12SP/048Rx43q7qfOIVTNZRr0R5AvgfOQi4oXAlTEsmNwYfjgTlHeZtS3kcs+M6S+ZIUeMqRIlt+E/kDuTTLP+sw2CuyylBznzilppZ1HIwNZJcKy9sGzis/7GMdt74op4Sw1A9Jrm9xGrSzzgoUEWiXis1tJ1VeLDSgUzoiegxAtDUJeVOswIDAQAB'

    """
    得到客户端对象。
    注意，一个alipay_client_config对象对应一个DefaultAlipayClient，定义DefaultAlipayClient对象后，alipay_client_config不得修改，如果想使用不同的配置，请定义不同的DefaultAlipayClient。
    logger参数用于打印日志，不传则不打印，建议传递。
    """
    client = DefaultAlipayClient(alipay_client_config=alipay_client_config, logger=logger)
    model = AlipayTradeQueryModel()
    # model.org_pid = "90m"
    model.out_trade_no = order_id
    request = AlipayTradeQueryRequest(biz_model=model)
    # 执行请求，执行过程中如果发生异常，会抛出，请打印异常栈
    response_content = None
    try:
        response_content = client.execute(request)
    except Exception as e:
        print(traceback.format_exc())
        return False, "失败"
    if not response_content:
        print("failed execute")
        return False, "失败"
    else:
        response = AlipayTradeQueryResponse()
        # 解析响应结果
        response.parse_response_content(response_content)
        print(response.body)
        if response.is_success():
            # 如果业务成功，则通过respnse属性获取需要的值
            print("get response trade_no:" + response.trade_no)
            if response.trade_status == "TRADE_SUCCESS":
                return True, response.body
            else:
                return False, response.trade_status
        else:
            # 如果业务失败，则从错误码中可以得知错误情况，具体错误码信息可以查看接口文档
            print(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)
            return False, response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg