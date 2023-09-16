from peewee import *
from datetime import datetime
from forum import db


class BaseModel(Model):
    create_time = DateTimeField(default=datetime.now(), verbose_name='创建时间')

    def to_json(self):
        r = {}
        for k in self.__data__.keys():
            if k == 'create_time':
                r[k] = str(getattr(self, k))
            else:
                r[k] = getattr(self, k)

    class Meta:
        database = db


class UserModel(BaseModel):
    id = CharField(primary_key=True)
    email = CharField(max_length=32, verbose_name='账号')
    nick_name = CharField(max_length=32, verbose_name='昵称', null=True)
    password = CharField(max_length=32, verbose_name='')
    gender = IntegerField(verbose_name='性别', null=True)
    signatrue = CharField(max_length=128, verbose_name='签名', null=True)
    pic = CharField(max_length=512, verbose_name='头像', null=True)
    status = IntegerField(verbose_name='账号状态', default=1)

    class Meta:
        table_name = 't_user'
