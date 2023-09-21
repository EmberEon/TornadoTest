import random
import string
import time
from datetime import datetime

STR_LIST = {}


class RandomCom:
    def __init__(self):
        self.__total_len = 30

    @staticmethod
    def __date_int(fmt='%Y%m%d%H%M%S%f'):
        return int(datetime.now().strftime(fmt))

    @staticmethod
    def __tamp_int():
        return int(time.time() * 1000)

    @staticmethod
    def __hex_num(num: int):
        """转16进制"""
        return hex(num)[2:]

    @staticmethod
    def __random_num(length: int):
        return str(random.randint(10 ** (length - 1), 10 ** length - 1))

    @staticmethod
    def __random_str(length: int):
        return ''.join(random.sample(string.ascii_lowercase + string.digits, length))

    def __order_hex(self, ran_len: int, is_stamp=True):
        return "{0}{1}".format(self.__hex_num(self.__tamp_int()), self.__random_str(ran_len)) if is_stamp else \
            "{0}{1}".format(self.__hex_num(self.__date_int()), self.__random_str(ran_len))

    def __ran_str_hex(self, ran_len, short_mode=True):
        return "{0}{1}".format(self.__hex_num(self.__tamp_int()), self.__random_str(ran_len)) if short_mode else \
            "{0}{1}".format(self.__hex_num(self.__date_int()), self.__random_str(ran_len))

    def __ran_num(self, ran_len: int, is_stamp=True):
        return "{0}{1}".format(self.__tamp_int(), self.__random_num(ran_len)) if is_stamp else \
            "{0}{1}".format(self.__date_int(), self.__random_num(ran_len))

    @staticmethod
    def __create(ran_len: int, create_random, is_stamp=True):
        while True:
            global STR_LIST
            if len(STR_LIST) > 50000:
                time.sleep(0.001)
                STR_LIST = {}
            order = create_random(ran_len, is_stamp)
            if order not in STR_LIST:
                STR_LIST[order] = ""
                return order

    def hex_order(self, str_len=30, is_stamp=False):
        """
        (不重复)按时间生成指定长度不重复的订单号，默认长度30，最短15,最长42 不在该的长度范围取默认值

        :param str_len: 生成字符串长度. 默认长度30，时间戳模式最短15,最长42 非时间戳模式最短21,最长42
        :param is_stamp: 是否使用时间戳模式
        """
        if str_len > 42 or str_len < 15:
            str_len = self.__total_len
            if (str_len < 21) and (not is_stamp):
                str_len = self.__total_len
        time_len = 11 if is_stamp else 17
        return self.__create(str_len - time_len, self.__order_hex, is_stamp)

    def hex_str(self, str_len=30, short_mode=True):
        """
        (不重复)按时间生成指定长度不重复的字符串，默认长度30，短模式最短15 非短模式最短21 最长47 不在该的长度范围取默认值

        :param str_len: 生成字符串长度. 默认长度30
        :param short_mode: 是否使用短模式 默认 是
        """
        if str_len < 15 or str_len > 47:
            str_len = self.__total_len
            if (str_len < 21) and (not short_mode):
                str_len = self.__total_len
        time_len = 11 if short_mode else 17
        return self.__create(str_len - time_len, self.__ran_str_hex, short_mode)

    def ran_num(self, str_len=30, is_stamp=True):
        """
        (不重复)按时间生成指定长度不重复的数字单号，默认长度30，时间戳模式最短20 非时间戳模式最短26 最长不限 不在该的长度范围取默认值

        :param str_len: 生成字符串长度. 默认长度30
        :param is_stamp: 是否使用时间戳模式 默认 是
        """
        if str_len > 42 or str_len < 20:
            str_len = self.__total_len
            if (str_len < 26) and (not is_stamp):
                str_len = self.__total_len
        time_len = 13 if is_stamp else 20
        return self.__create(str_len - time_len, self.__ran_num, is_stamp)

    @staticmethod
    def random_int(min_num: int, max_num: int, ji_shu=0):
        """
        (允许重复)按最大值最小值范围取随机数

        :param min_num: 最小值
        :param max_num: 最大值
        :param ji_shu: 取值基数 该参数不为0时 取到的值会对对该值取整再乘以该值
        """
        res = random.randint(min_num, max_num)
        if ji_shu:
            return (res // ji_shu) * ji_shu
        return res

    @staticmethod
    def random_num(length=5):
        """(允许重复)取指定数量级范围内的随机数"""
        return random.randint(10 ** (length - 1), 10 ** length - 1)

    @staticmethod
    def ran_list_one(item_list: list):
        if item_list and isinstance(item_list, list):
            return random.choice(item_list)
        return None
