import peewee_async
from tornado import ioloop
from forum import create_app, obj
from forum.models import *
from uuid import uuid4
import asyncio

def start_app():
    app = create_app()
    ioloop.IOLoop.current().start()


def create_table():
    UserModel.create_table(True)


async def create_data():
    await obj.create(UserModel, id=uuid4(), email='1419273079@qq.com', password='123456', nick_name='吕布')



if __name__ == '__main__':
    start_app()
    # create_table()
    # result = ioloop.IOLoop.current().run_sync(create_data)
    # loop = asyncio.get_event_loop()
    # result = loop.run_until_complete(create_data())
