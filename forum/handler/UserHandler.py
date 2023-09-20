import urllib

from forum.handler.BaseHandler import BaseHandler
from forum.utils.zhi_fu_bao_utils import make_zhi_fu_bao_url, queryalipay
from forum.wtforms import UserForm
from forum.models import UserModel
from uuid import uuid4
from forum.utils.email_util import send_mail
from config import email
from random import choice
from forum.utils import utils


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
