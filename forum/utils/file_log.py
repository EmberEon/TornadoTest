import logging
import os
from logging import handlers

LOG_OBJ_DATA = {}


class FileLog:

    @staticmethod
    def __create_log_obj(log_path="", log_name="run_data", log_fmt=None) -> logging:
        log_path = "./output/" + log_path if log_path else "./output"
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        if not log_fmt:
            log_fmt = "%(asctime)s - %(process)d:%(lineno)s:%(levelname)s - %(message)s"
        log_item = logging.getLogger("{0}_{1}".format(log_path, log_name))
        if log_item.handlers:
            return log_item
        formatter = logging.Formatter(fmt=log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        log_handler = handlers.RotatingFileHandler(
            filename=log_path + "/" + log_name + ".log", mode="a", maxBytes=52428800, backupCount=10, encoding='utf-8')
        log_item.setLevel(logging.DEBUG)
        log_handler.setFormatter(formatter)
        log_item.addHandler(log_handler)
        return log_item

    def __base_log_obj(self, file_name="run_info", folder="", log_fmt=""):
        """
        添加日志

        :param file_name: 日志文件名 默认为‘run_info’（多字段命名请用下划线连接 不能带空格）
        :param folder: 日志目录名 默认无目录 既是output目录下的子目录名 不建议使用更多级的目录
        :param log_fmt: 日志记录格式 默认为 ‘%(asctime)s - %(process)d:%(lineno)s:%(levelname)s - %(message)s’ 格式
        """
        global LOG_OBJ_DATA
        name = "{0}/{1}".format(folder, file_name) if folder else file_name
        obj = LOG_OBJ_DATA.get(name)
        if obj:
            return obj
        obj = self.__create_log_obj(log_path=folder, log_name=file_name, log_fmt=log_fmt)
        LOG_OBJ_DATA[name] = obj
        return obj

    def failed(self, *data):
        """代码或执行失败或报错的日志"""
        obj = self.__base_log_obj(file_name='failed', folder='fail_log', log_fmt="")
        obj.fatal("{0}".format(data))

    def sql(self, *data):
        """sql记录日志"""
        obj = self.__base_log_obj(file_name='sql_info', folder='sql_log', log_fmt="")
        obj.info("{0}".format(data))

    def sql_fail(self, *data):
        """sql记录日志"""
        obj = self.__base_log_obj(file_name='sql_info', folder='sql_log', log_fmt="")
        obj.fatal("{0}".format(data))

    def info(self, *data):
        """标记或打印类的日志"""
        obj = self.__base_log_obj(file_name='info', folder='info_log', log_fmt="")
        obj.info("{0}".format(data))

    def client_update_log(self, *data):
        """标记或打印类的日志"""
        print(data)
        obj = self.__base_log_obj(file_name='client_log', folder='client_log', log_fmt="")
        obj.info("{0}".format(data))
