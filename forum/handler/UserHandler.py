import json
import urllib
from asyncio import sleep

import aioredis
import redis

from forum.handler.BaseHandler import BaseHandler
from forum.utils.zhi_fu_bao_utils import make_zhi_fu_bao_url, queryalipay
from forum.wtforms import UserForm
from forum.models import UserModel
from uuid import uuid4
from forum.utils.email_util import send_mail
from configs.config import email
from random import choice
from forum.utils import utils
import requests
from forum.utils import ali_yun
import tornado.web
import os
import hashlib


class AddUserHandler(BaseHandler):
    async def post(self):
        rs_data = {}
        form = UserForm(self.request.arguments)
        # tm_code = self.get_body_argument('code')
        tm_code = self.get_query_argument('code')
        if form.validate():
            email = form.email.data
            try:
                exist_user = await self.obj.get(UserModel, email=email)
                if exist_user:
                    rs_data['code'] = 500
                    rs_data['msg'] = '用户名已存在'
            except Exception as e:
                code = self.redis.get(email)
                if code and code.decode() == tm_code:
                    form.id.data = uuid4()
                    await self.obj.create(UserModel, **form.data)
                    rs_data['code'] = 200
                    rs_data['msg'] = '注册成功'
                else:
                    rs_data['code'] = 500
                    rs_data['msg'] = '验证码错误'
        else:
            rs_data['code'] = 500
            rs_data['msg'] = '注册失败'
            for field in form.errors:
                rs_data[field] = form[field][0]
        return self.finish(rs_data)


class SendEmail(BaseHandler):
    def generate_code(self):
        base = '0123456789'
        code = []
        for i in range(4):
            code.append(choice(base))
        return ''.join(code)

    async def post(self, *args, **kwargs):
        # 此方法获取的是正文的email
        # user_email = self.get_body_argument('email')
        # 此方法获取的是URL的email
        code = self.generate_code()
        user_email = self.get_query_argument('email')
        msg = f'您好，您正在使用{user_email}注册cmz的网站，您的验证码是：{code}.如果非本人操作请忽略！'
        send_mail(from_email=email.get('uname'), passwd=email.get('password'), to_email=user_email,
                  subject='用户注册验证码', txt=msg)
        self.redis.set(user_email, code)
        print(self.redis.get(user_email))


class ZhiFuBaoPayHandler(BaseHandler):
    def get(self):
        # 使用self.redirect()方法进行跳转
        self.render('index.html')
        # self.redirect('/')


class BuyHandler(BaseHandler):
    def get(self, product_id):
        data = {}
        seller_id = "seller_id"
        total_amount = 0.01
        out_trade_no = utils.get_obtain_order_number()
        timeout_express = "90m"
        result = make_zhi_fu_bao_url(total_amount=total_amount, out_trade_no=out_trade_no,
                                     timeout_express=timeout_express)
        print(result)
        self.redirect(result)


class AliPayNotify(BaseHandler):
    def prepare(self):
        pass

    def get(self):
        return self._request()

    def post(self):
        return self._request()

    def _request(self):
        order_id = self.get_string('out_trade_no')
        # 回调后直接调查询在查一次
        result, msg = queryalipay(order_id)
        if not result:
            print("失败！")

    def get_string(self, name):
        """获取查询字符串值"""
        if name == "params":
            urlenparams = self.get_argument(name, '')
            serialparams = urllib.parse.unquote(urlenparams, 'utf-8', 'ignore')
            return serialparams
        return self.get_argument(name, '')


class WeatherHandler(BaseHandler):
    API_KEY = '72667c6e9bf10d68f07d3fa2bfb7889b'  # 请到 OpenWeatherMap 注册并获取 API KEY
    API_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

    async def get(self):
        city = self.get_argument('city', 'Beijing')
        response = requests.get(self.API_URL.format(city, self.API_KEY))
        if response.status_code == 200:
            data = response.json()
            main = data.get('main')
            main['temp'] = str(round(main.get('temp') - 273.15, 1)) + '°C'
            main['temp_min'] = str(round(main.get('temp_min') - 273.15, 1)) + '°C'
            main['temp_max'] = str(round(main.get('temp_max') - 273.15, 1)) + '°C'
            self.write(data)
        else:
            self.set_status(response.status_code)
            self.write({"error": "Unable to fetch weather data"})


class CheckHandler(BaseHandler):
    async def get(self):
        a = await ali_yun.check_txt()
        return await self.write_json(a)
        print(a)


class IndexHandler(BaseHandler):
    async def get(self):
        self.redis.publish("RED_DOT_MSG_DDZ", "hello!cmz")
        return self.finish({'msg': 0, 'code': 200, })


class MessagesHandler(BaseHandler):
    async def get(self):
        redis = await aioredis.create_redis(address='redis://192.168.232.128:26379', password='Cmz@123456', db=0)
        try:
            channel_name = 'RED_DOT_MSG_DDZ'
            # 订阅频道
            channel, = await redis.subscribe(channel_name)
            message = await channel.get(encoding='utf-8')
            sleep(0.5)
            if message:
                print(f"Received: {message}")
                return await self.write_json(data={"message": message})
            else:
                print("没有消息")
                return await self.write_json(desc="没有消息")
        finally:
            redis.close()
            await redis.wait_closed()


class DownloadHandler(tornado.web.RequestHandler):
    def get(self):
        # 定义您的软件的路径
        software_path = './software.txt'
        # 为下载的文件设置一个名称
        download_name = os.path.basename(software_path)

        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', f'attachment; filename={download_name}')

        with open(software_path, 'rb') as file:
            self.write(file.read())
        self.finish()

class WeChatVerificationHandler(tornado.web.RequestHandler):
    def get(self):
        signature = self.get_argument('signature', '')
        timestamp = self.get_argument('timestamp', '')
        nonce = self.get_argument('nonce', '')
        echostr = self.get_argument('echostr', '')

        token = '123456'  # 将这里替换为你的Token

        # 将参数排序并拼接
        params = [token, timestamp, nonce]
        params.sort()
        params_str = ''.join(params)

        # 使用SHA1哈希计算签名
        sha1 = hashlib.sha1()
        sha1.update(params_str.encode())
        hashcode = sha1.hexdigest()

        if hashcode == signature:
            self.write(echostr)
        else:
            self.write("Verification failed.")

    def post(self):
        # 处理微信消息
        # 在这里处理接收到的微信消息，例如回复消息等
        self.write("Success")