import redis

from libs.torndb import Connection
from utils import file_log, utils

RDS_CONN = None
BASE_DB = None
LOG_DB = None
FORCE_LIST = []
LOG_FORCE_LIST = []


class BaseORM:
    __base_key = 'db_game'
    __log_key = 'db_logs'

    def __init__(self):
        self.__db = BASE_DB
        self.__log_db = LOG_DB
        self.__db_conf = None
        self.__db_log_conf = None
        self.__db_conn(self.__base_key)
        self.__db_conn(self.__log_key)

    @property
    def db_name(self):
        if self.__db_conf:
            return self.__db_conf.get('database')
        self.__db_conf = utils.read_json_conf(self.__base_key)
        return self.__db_conf.get('database')

    @property
    def log_db_name(self):
        if self.__db_log_conf:
            return self.__db_log_conf.get('database')
        db_log_conf = utils.read_json_conf(self.__log_key)
        self.__db_log_conf = db_log_conf
        return db_log_conf.get('database')

    def __db_conn(self, db_name):
        db_conf = utils.read_json_conf(db_name)
        try:
            if not self.__db and db_name == self.__base_key:
                self.__db_conf = db_conf
                self.__db = Connection(**db_conf)
                global BASE_DB
                BASE_DB = self.__db
            if not self.__log_db and db_name == self.__log_key:
                self.__db_log_conf = db_conf
                self.__log_db = Connection(**db_conf)
                global LOG_DB
                LOG_DB = self.__log_db
        except Exception as err:
            file_log.sql_fail("数据库链接错误:", err, "配置", db_conf)

    def __reconnect(self, db_name):
        if db_name == self.__base_key:
            try:
                self.__db.get('SELECT 1')
            except Exception as err:
                file_log.sql_fail("数据库连接失败:{0}, 即将重连".format(err))
                self.__db.reconnect()
            if FORCE_LIST:
                for sql in FORCE_LIST[:]:
                    FORCE_LIST.remove(sql)
                    self.execute(sql)
        else:
            try:
                self.__log_db.get('SELECT 1')
            except Exception as err:
                file_log.sql_fail("日志数据库连接失败:{0}, 即将重连".format(err))
                self.__log_db.reconnect()
            if LOG_FORCE_LIST:
                for sql in LOG_FORCE_LIST[:]:
                    LOG_FORCE_LIST.remove(sql)
                    self.execute_log(sql)

    def query(self, sql: str):
        try:
            return self.__db.query(sql)
        except Exception as err:
            file_log.sql_fail(err, sql)
            self.__reconnect(self.__base_key)
            return False

    def query_one(self, sql: str):
        try:
            return self.__db.get(sql)
        except Exception as err:
            file_log.sql_fail(err, sql)
            self.__reconnect(self.__base_key)
            return False

    def execute(self, sql, force=False):
        try:
            return self.__db.execute(sql)
        except Exception as err:
            force and FORCE_LIST.append(sql)
            file_log.sql_fail(err, sql)
            self.__reconnect(self.__base_key)
            if force:
                return 1
            raise Exception(err)

    def ex_last_id(self, sql, force=False):
        try:
            return self.__db.execute_lastrowid(sql)
        except Exception as err:
            force and FORCE_LIST.append(sql)
            file_log.sql_fail(err, sql)
            self.__reconnect(self.__base_key)
            if force:
                return 1
            raise Exception(err)

    def row_count_ex(self, sql: str, force=False):
        try:
            return self.__db.execute_rowcount(sql)
        except Exception as err:
            force and FORCE_LIST.append(sql)
            file_log.sql_fail(err, sql)
            self.__reconnect(self.__base_key)
            if force:
                return 1

    def query_log(self, sql):
        try:
            return self.__log_db.query(sql)
        except Exception as err:
            file_log.sql_fail(err, sql)
            self.__reconnect(self.__base_key)
            return False

    def query_log_one(self, sql):
        try:
            return self.__log_db.get(sql)
        except Exception as err:
            file_log.sql_fail(err, sql)
            self.__reconnect(self.__base_key)
            return False

    def execute_log(self, sql, force=False):
        try:
            return self.__log_db.execute(sql)
        except Exception as err:
            force and LOG_FORCE_LIST.append(sql)
            file_log.sql_fail(err, sql)
            self.__reconnect(self.__log_key)
            if force:
                return True
            return False

    def log_ex_count_ex(self, sql: str, force=False):
        try:
            return self.__log_db.execute_rowcount(sql)
        except Exception as err:
            force and LOG_FORCE_LIST.append(sql)
            file_log.sql_fail(err, sql)
            self.__reconnect(self.__log_key)
            if force:
                return True
            return False

    def log_last_id(self, sql, force=False):
        try:
            return self.__log_db.execute_lastrowid(sql)
        except Exception as err:
            force and LOG_FORCE_LIST.append(sql)
            file_log.sql_fail(err, sql)
            self.__reconnect(self.__log_key)
            if force:
                return True
            return False

    @staticmethod
    def __check_val(val, need_encrypt=False):
        if isinstance(val, int) or isinstance(val, float):
            if not need_encrypt:
                return "{0}".format(val)
            return "PASSWORD('{0}')".format(utils.escape_str(str(val)))
        if isinstance(val, str):
            if need_encrypt:
                return "PASSWORD('{0}')".format(utils.escape_str(val))
            return "'{0}'".format(utils.escape_str(val))
        if isinstance(val, dict) or isinstance(val, list):
            return "'{0}'".format(utils.escape_str(utils.json_encode(val, is_cut=True), is_json_str=True))
        if isinstance(val, bytes):
            return "'{0}'".format(utils.escape_str(utils.bytes_to_str(val)))
        return None

    @staticmethod
    def __double_check(sql: str, update_fields: list, add_fields: list, form_arr: list):
        if update_fields or add_fields:
            sql += " ON DUPLICATE KEY UPDATE "
            update_str = ""
            for item in update_fields or []:
                if item not in form_arr:
                    raise Exception('Error: SQL INSERT OR UPDATE参数错误: 没有可更新的表单')
                update_str += "{0}=VALUES({0}),".format(item)
            sql += update_str if add_fields else update_str[0:-1]
            add_str = ""
            for item in add_fields or []:
                if item not in form_arr:
                    raise Exception('Error: SQL INSERT OR UPDATE参数错误: 没有可更新的表单')
                add_str += "{0}={0}+VALUES({0}),".format(item)
            sql += add_str[0:-1]
        return sql

    def creat_insert_one(self, form_name: str, params_dict: dict, db_name=None, update_fields=None, add_fields=None,
                         encrypt_fields=None):
        """
        从字典合成单条insert语句
        当前数据库不支持emoji和json 所以json会转换成json字符串,emoji会用?替换

        :param form_name: 表单名
        :param db_name: 数据库名称 不填指定为当前数据库的名称
        :param params_dict: 数据表字典映射
        :param update_fields: INSERT语句里需要执行更新的字段名列表,没有该项只插入
        :param add_fields: INSERT语句里需要执行加减的字段名列表,相应的值应为数字类型 没有该项只插入
        :param encrypt_fields: 需要加密的字段
        """
        form_arr, val_list = [], []
        if not encrypt_fields:
            encrypt_fields = []
        for k, v in params_dict.items():
            if v is None:
                raise Exception('Error: {0}项值为None'.format(k))
            form_arr.append(k)
            need_encrypt = True if k in encrypt_fields else False
            val_list.append(self.__check_val(v, need_encrypt=need_encrypt))
        sql = "INSERT INTO {3}.{0}({1}) VALUES({2})".format(form_name, ','.join(form_arr), ','.join(val_list), db_name)\
            if db_name else "INSERT INTO {0}({1}) VALUES({2})".format(form_name, ','.join(form_arr), ','.join(val_list))
        if val_list:
            return self.__double_check(sql, update_fields=update_fields, add_fields=add_fields, form_arr=form_arr)
        raise Exception('Error: SQL 表单参数值错误: 没有可更新的表单')

    def cgs_creat_insert_one(self, form_name: str, params_dict: dict, db_name=None, update_fields=None, add_fields=None,
                         encrypt_fields=None):
        """
        从字典合成单条insert语句
        当前数据库不支持emoji和json 所以json会转换成json字符串,emoji会用?替换

        :param form_name: 表单名
        :param db_name: 数据库名称 不填指定为当前数据库的名称
        :param params_dict: 数据表字典映射
        :param update_fields: INSERT语句里需要执行更新的字段名列表,没有该项只插入
        :param add_fields: INSERT语句里需要执行加减的字段名列表,相应的值应为数字类型 没有该项只插入
        :param encrypt_fields: 需要加密的字段
        """
        form_arr, val_list = [], []
        if not encrypt_fields:
            encrypt_fields = []
        for k, v in params_dict.items():
            if k == 'index':
                k = '`index`'
            if v is None:
                raise Exception('Error: {0}项值为None'.format(k))
            form_arr.append(k)
            need_encrypt = True if k in encrypt_fields else False
            val_list.append(self.__check_val(v, need_encrypt=need_encrypt))
        sql = "INSERT INTO {3}.{0}({1}) VALUES({2})".format(form_name, ','.join(form_arr), ','.join(val_list), db_name)\
            if db_name else "INSERT INTO {0}({1}) VALUES({2})".format(form_name, ','.join(form_arr), ','.join(val_list))
        if val_list:
            return self.__double_check(sql, update_fields=update_fields, add_fields=add_fields, form_arr=form_arr)
        raise Exception('Error: SQL 表单参数值错误: 没有可更新的表单')

    def creat_insert_many(self, form_name: str, params_list: list, db_name=None, update_fields=None, add_fields=None):
        """
        从字典合成单条insert语句
        当前数据库不支持emoji和json 所以json会转换成json字符串,emoji会用?替换

        :param form_name: 表单名
        :param db_name: 数据库名称 不填指定为当前数据库的名称
        :param params_list: 数据表字典映射列表[{},{}...]
        :param update_fields: INSERT语句里需要执行更新的字段名列表,没有该项只插入
        :param add_fields: INSERT语句里需要执行加减的字段名列表,相应的值应为数字类型 没有该项只插入
        """
        val_str, form_arr = "", []
        for params in params_list:
            cur_len, len_param = len(params), len(form_arr)
            if len_param and len_param != cur_len:
                raise Exception('Error: 表单参数数量不一致')
            val_list = []
            for k, v in sorted(params.items()):
                if v is None:
                    raise Exception('Error: {0}项值为None'.format(k))
                if k not in form_arr:
                    form_arr.append(k)
                val_list.append(self.__check_val(v))
            val_str += "({0}),".format(",".join(val_list))
        sql = "INSERT INTO {3}.{0}({1}) VALUES{2}".format(form_name, ','.join(form_arr), val_str[0:-1], db_name) if \
            db_name else "INSERT INTO {0}({1}) VALUES{2}".format(form_name, ','.join(form_arr), val_str[0:-1])
        if val_str:
            return self.__double_check(sql, update_fields=update_fields, add_fields=add_fields, form_arr=form_arr)
        raise Exception('Error: SQL 表单参数值错误: 没有可更新的表单')

    def insert_one(self, form_name: str, params_dict: dict, update_fields=None, add_fields=None, encrypt_fields=None,
                   force=False):
        """
        插入或更新单条数据, INSERT OR UPDATE

        :param form_name: 表单名
        :param params_dict: 数据表字典映射
        :param update_fields: INSERT语句里需要执行更新的字段名列表,没有该项只插入
        :param add_fields: INSERT语句里需要执行加减的字段名列表,相应的值应为数字类型 没有该项只插入
        :param encrypt_fields: 需要加密的字段
        :param force: 是否强制更新 为True时在数据库重连后会重新写入
        """
        sql = self.creat_insert_one(
            form_name, params_dict, update_fields=update_fields, add_fields=add_fields, encrypt_fields=encrypt_fields)
        try:
            return self.__db.execute_rowcount(sql)
        except Exception as err:
            force and FORCE_LIST.append(sql)
            file_log.sql_fail(err, sql)
            self.__reconnect(self.__base_key)

    def cgs_insert_one(self, form_name: str, params_dict: dict, update_fields=None, add_fields=None, encrypt_fields=None,
                   force=False):
        """
        插入或更新单条数据, INSERT OR UPDATE

        :param form_name: 表单名
        :param params_dict: 数据表字典映射
        :param update_fields: INSERT语句里需要执行更新的字段名列表,没有该项只插入
        :param add_fields: INSERT语句里需要执行加减的字段名列表,相应的值应为数字类型 没有该项只插入
        :param encrypt_fields: 需要加密的字段
        :param force: 是否强制更新 为True时在数据库重连后会重新写入
        """
        sql = self.cgs_creat_insert_one(
            form_name, params_dict, update_fields=update_fields, add_fields=add_fields, encrypt_fields=encrypt_fields)
        try:
            return self.__db.execute_rowcount(sql)
        except Exception as err:
            force and FORCE_LIST.append(sql)
            file_log.sql_fail(err, sql)
            self.__reconnect(self.__base_key)

    def insert_many(self, form_name: str, params_list: list, update_fields=None, add_fields=False, force=False):
        sql = self.creat_insert_many(form_name, params_list, update_fields=update_fields, add_fields=add_fields)
        try:
            return self.__db.execute_rowcount(sql)
        except Exception as err:
            force and FORCE_LIST.append(sql)
            file_log.sql_fail(err, sql)
            self.__reconnect(self.__base_key)

    def insert_log_many(self, form_name: str, params_list: list, update_fields=None, add_fields=False, force=False):
        sql = self.creat_insert_many(form_name, params_list, update_fields=update_fields, add_fields=add_fields)
        try:
            return self.__log_db.execute_rowcount(sql)
        except Exception as err:
            force and FORCE_LIST.append(sql)
            file_log.sql_fail(err, sql)
            self.__reconnect(self.__log_key)

    def insert_log_one(self, form_name: str, params_dict: dict, update_fields=None, add_fields=False, force=False):
        """
        :param form_name: 表单名
        :param params_dict: 数据表字典映射
        :param update_fields: INSERT语句里需要执行更新的字段 没有只插入
        :param add_fields: INSERT语句里需要执行加减的字段,相应的值应为数字类型
        :param force: 是否强制更新 为True时在数据库重连后会重新写入
        """
        sql = self.creat_insert_one(form_name, params_dict, update_fields=update_fields, add_fields=add_fields)
        try:
            return self.__log_db.execute_rowcount(sql)
        except Exception as err:
            force and FORCE_LIST.append(sql)
            file_log.sql_fail(err, sql)
            self.__reconnect(self.__log_key)

    def transaction(self, sql_list: list):
        """
        mysql原子事务

        :param sql_list: 需要放在一个事务里的的SQL语句列表 数据模型 [sql 1, sql 2, sql 3, ...] 建议一次不超过10条
        """
        try:
            return self.__db.transaction(sql_list)
        except Exception as err:
            file_log.sql_fail("当前数据库链接创建事务失败,即将重连", err)
            self.__reconnect(self.__base_key)
            return False


class BaseRedis:
    def __init__(self, redis_key='redis_base'):
        self.__conf_name = redis_key
        self.__conn = RDS_CONN

    def __connect(self):
        redis_info = utils.read_json_conf(self.__conf_name)
        if not redis_info:
            raise Exception("读取Redis配置出错,配置不存在:{}".format(self.__conf_name))
        try:
            return redis.StrictRedis(**redis_info)
        except Exception as data:
            file_log.sql_fail("Redis连接出错，请检查redis的链接配置：", data)

    @property
    def __share(self):
        if not self.__conn:
            global RDS_CONN
            RDS_CONN = self.__connect()
            self.__conn = self.__connect()
        return self.__conn

    def save_hash(self, name, data: dict):
        """
        批量存储哈希：{"a": str(data), "b", str(data)}
        备注：在设置字典map前，需要将值手动转换成字符串或bytes类型
        """
        try:
            self.__share.hmset(name, data)
        except Exception as err:
            file_log.sql_fail(err)

    def get_all_keys(self):
        return self.__share.keys()

    def get_hash_kv(self, name, key):
        return self.__share.hget(name, key)

    def get_hash_kvs(self, name, *key):
        return self.__share.hmget(name, *key)

    def get_hash_value(self, name):
        return self.__share.hvals(name)

    def save_hash_kv(self, name, key, value):
        return self.__share.hset(name, key, str(value))

    def is_exist_hash_kv(self, name, key):
        return self.__share.hexists(name, key)

    def is_exist(self, name):
        return self.__share.exists(name)

    def get_hash(self, name):
        return self.__share.hgetall(name)

    def get_text(self, name):
        return self.__share.get(name)

    def get_hkeys(self, name):
        return self.__share.hkeys(name)

    def get_hlen(self, name: str):
        return self.__share.hlen(name) or 0

    def del_hash_kv(self, name, *key):
        return self.__share.hdel(name, *key)

    def rpop(self, name):
        return self.__share.rpop(name)

    def lpop(self, name):
        return self.__share.lpop(name)

    def rpush(self, name, values):
        return self.__share.rpush(name, values)

    def remove_key(self, *name):
        return self.__share.delete(*name)

    def save_order_list(self, name, *data):
        """data应是一个长度为2的倍数且奇数项为score，偶数项为key的list"""
        return self.__share.zadd(name, *data)

    def order_list_set(self, name, uid, score):
        return self.__share.zadd(name, score, uid)

    def order_list_add(self, name, key, amount=0):
        """
        有序列表累加
        """
        return self.__share.zincrby(name, key, amount)

    def order_list_remove(self, name, *values):
        return self.__share.zrem(name, *values)

    def get_order_list(self, name: str, start: int, end: int, desc=True):
        file_log.info("zrange", name, start, end)
        return self.__share.zrange(name, start, end, desc=True, withscores=True)

    def get_score(self, name, user):
        score = self.__share.zscore(name, user) or 0
        return score

    def get_order_score(self, name: str, key):
        return self.__share.zscore(name, key)

    def get_ranking(self, name, user):
        ranking = self.__share.zrevrank(name, user)
        return 0 if ranking is None else ranking + 1

    def save_str(self, name, value):
        return self.__share.set(name, str(value))

    def get_str(self, name):
        """redis取字符串"""
        return self.__share.get(name)

    def get_keys(self, key: str):
        name = key + "*"
        return self.__share.keys(name)

    def set_str_exp(self, name, value, exp_time=600):
        return self.__share.setex(name, exp_time, value)

    def publish_msg(self, channel: str, msg_type: int, msg=None, uid=0 or [], sid=0):
        """
        消息发布
        :param channel: 频道 字符串类型
        :param msg_type: 消息类型
        :param msg: 消息数据
        :param uid: 单个玩家uid为玩家uid 多个玩家为玩家uid的列表或元组 为0则通知全部在线玩家
        :param sid: 如果通知子游戏，该值为对应的server_id
        """
        message = {'channel': channel, 'msg_type': msg_type, 'uid': uid, 'sid': sid, 'data': msg or {}}
        return self.__share.publish(channel, utils.json_encode(message, is_cut=True))

    def set_s_list(self, name, values: list):
        values and self.__share.sadd(name, *values)

    def len_s_list(self, name):
        return self.__share.scard(name)

    def get_s_list(self, name):
        return self.__share.smembers(name)

    def in_s_list(self, name, val):
        return 1 if self.__share.sismember(name, val) else 0

    def del_from_s_list(self, name, val):
        self.__share.srem(name, val)

    def set_oppo_goods(self, order_id, total):
        name = "oppo_goods" + utils.today_str()
        self.__share.hset(name, order_id, total)

    def set_oppo_goods_status(self, order_id, goods_status):
        name = "oppo_goods_status" + utils.today_str()
        self.__share.hset(name, order_id, goods_status)

    def get_oppo_goods(self, order_id):
        name = "oppo_goods" + utils.today_str()
        data = self.__share.hget(name, order_id)
        return eval(data) if data else {}

    def get_oppo_goods_status(self, order_id):
        name = "oppo_goods_status" + utils.today_str()
        data = self.__share.hget(name, order_id)
        return eval(data) if data else {}

    def set_vivo_goods_status(self, order_id, goods_status):
        name = "vivo_goods_status" + utils.today_str()
        self.__share.hset(name, order_id, goods_status)

    def get_vivo_goods_status(self, order_id):
        name = "vivo_goods_status" + utils.today_str()
        data = self.__share.hget(name, order_id)
        return eval(data) if data else {}

    def update_oppo_goods_status(self, order_id, goods_status):
        name = "oppo_goods_status" + utils.today_str()
        self.__share.hset(name, order_id, goods_status)

    def update_vivo_goods_status(self, order_id, goods_status):
        name = "vivo_goods_status" + utils.today_str()
        self.__share.hset(name, order_id, goods_status)

    def set_yyb_goods_status(self, order_id, goods_status):
        name = "yyb_goods_status" + utils.today_str()
        self.__share.hset(name, order_id, goods_status)

    def get_yyb_goods_status(self, order_id):
        name = "yyb_goods_status" + utils.today_str()
        data = self.__share.hget(name, order_id)
        return eval(data) if data else {}

    def update_yyb_goods_status(self, order_id, goods_status):
        name = "yyb_goods_status" + utils.today_str()
        self.__share.hset(name, order_id, goods_status)

    def set_kuaishou_goods_status(self, order_id, goods_status):
        name = "kuaishou_goods_status" + utils.today_str()
        self.__share.hset(name, order_id, goods_status)

    def get_kuaishou_goods_status(self, order_id):
        name = "kuaishou_goods_status" + utils.today_str()
        data = self.__share.hget(name, order_id)
        return eval(data) if data else {}

    def update_kuaishou_goods_status(self, order_id, goods_status):
        name = "kuaishou_goods_status" + utils.today_str()
        self.__share.hset(name, order_id, goods_status)