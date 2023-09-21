import datetime
import random
import string
import ast
import base64
import binascii
import datetime
import hashlib
import ipaddress
import json
import os
import random
import re
import time

from jsmin import jsmin
from tornado.httpclient import AsyncHTTPClient

from Crypto.Cipher import AES

from forum.utils import random_com, file_log


class ObjectDict(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            return None

    def __setattr__(self, name, value):
        self[name] = value


class DictObj(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


def dict_to_obj(dict_obj):
    if not isinstance(dict_obj, dict):
        return dict_obj
    inst = DictObj()
    for k, v in dict_obj.items():
        inst[k] = dict_to_obj(v)
    return inst


def get_random_num(length=5):  # 获得随机数字，并返回字符串
    min_num = 10 ** (length - 1)
    max_num = 10 ** length - 1
    return str(random.randint(min_num, max_num))


def get_random_int(min_num: int, max_num: int, ji_shu=0):
    if ji_shu:
        res = random.randint(min_num, max_num)
        return (res // ji_shu) * ji_shu
    return random.randint(min_num, max_num)


def get_list_random_item(item_list: list, rate_arr=None, base_ratio=10000):
    """
    按概率随机获取列表里的某项 采用分段步进取值方式

    :param item_list: 取值的列表
    :param rate_arr: 概率列表 不传默认等概率
    :param base_ratio: 概率的比例基数
    """
    if not item_list:
        return None, 0
    if not base_ratio:
        base_ratio = 10000
    len_item = len(item_list)
    if not rate_arr:
        rate_arr = [(base_ratio / len_item) for _ in range(0, len_item)]
    len_rate = len(rate_arr)
    if len_item != len_rate:
        extra_num = len_item - len_rate
        if extra_num > 0:
            tmp_arr = [0 for _ in range(extra_num)]
            rate_arr += tmp_arr
        else:
            rate_arr = rate_arr[0: len_item]
    lottery_num = random.randint(1, sum(rate_arr))
    item_num, total_num = 0, 0
    for num in rate_arr:
        total_num += num
        if lottery_num <= total_num:
            return item_list[item_num], item_num
        item_num += 1
    return item_list[-1], item_num


def http_get_with_header(url, headers, success_func, fail_func):
    # 注意要使用 tornado 启动APP后此函数才有效
    def handle_request(response):
        if response.body:
            success_func(response.body)
            return
        if response.error:
            fail_func()
        else:
            success_func(response.body)

    http_client = AsyncHTTPClient()
    params = {'method': 'GET', 'headers': headers}
    http_client.fetch(url, handle_request, **params)


def http_get(url, success_func, fail_func):
    # 注意要使用 tornado 启动APP后此函数才有效
    def handle_request(response):
        if response.body:
            success_func(response.body)
            return
        if response.error:
            fail_func()
        else:
            success_func(response.body)

    http_client = AsyncHTTPClient()
    params = {'method': 'GET'}
    http_client.fetch(url, handle_request, **params)


def http_post(url, post_params, success_func, fail_func, body=None, headers=None, cert=False):
    # 注意要使用 tornado 启动APP后此函数才有效
    def handle_request(response):
        if response.body:
            success_func(response.body)
            return

        if response.error:
            fail_func()
        else:
            success_func(response.body)

    http_client = AsyncHTTPClient()
    params = {'method': 'POST', 'body': '', 'validate_cert': cert, 'headers': headers}
    if post_params:
        params['body'] = json_encode(post_params)
    if body:
        params['body'] = body
    http_client.fetch(url, handle_request, **params)


def read_file(file_path: str):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_txt = file.read()
            return file_txt
    except Exception as err:
        file_log.failed("文件读取失败:", err, file_path)


def read_json_conf(key_name: str):
    # json_str = read_file('./configs/config.json')
    json_str = read_file('./config.py')
    if json_str:
        try:
            json_data = json.loads(json_str)
            return json_data.get(key_name)
        except Exception as err:
            file_log.failed("解析JSON配置出错:", err)
    else:
        file_log.failed("读取JSON配置出错:")


# 读json文件，并返回对应的对象，适用于小配置文件的读取(定时任务迁移)
def read_json_file(filename):
    try:
        with open(filename, encoding='UTF-8') as js_file:
            mini_con = jsmin(js_file.read())
            obj = json.loads(mini_con, strict=False)
            return obj
    except Exception as data:
        print("read json file fail:", filename, data)
    return {}


def read_json_conf_base(key_name:str):
    json_str = read_file(key_name)
    if json_str:
        try:
            json_data = json.loads(json_str)
            return json_data
        except Exception as err:
            file_log.failed("解析JSON配置出错:", err)


def timestamp(is_ms=False):  # 返回时间戳 is_ms是否毫秒级
    if not is_ms:
        return int(time.time())
    else:
        return time.time() * 1000


def sha1(data):
    return hashlib.sha1(data.encode(encoding='UTF-8')).hexdigest()


def md5(data):
    return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()


def sha256(data):
    return hashlib.sha256(data.encode(encoding='UTF-8')).hexdigest()


def sha512(data):
    return hashlib.sha512(data.encode(encoding='UTF-8')).hexdigest()


def get_sign_string_from_map(sign_data):
    keys = list(sign_data.keys())
    keys.sort()
    values = []

    for k in keys:
        if not sign_data[k]:
            continue
        value_str = sign_data[k]
        if isinstance(value_str, dict):
            value_str = str(value_str)
        if isinstance(value_str, int):
            value_str = str(value_str)
        values.append(k + '=' + value_str)
    sign_data = "&".join(values)
    return sign_data


def json_encode(data, is_cut=False):
    if is_cut:
        return json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return json.dumps(data, ensure_ascii=False)


def json_decode(data):
    if isinstance(data, bytes):
        data = data.decode('utf8')
    try:
        py_ret = json.loads(data)
        return py_ret
    except Exception as exp:
        file_log.failed("解析JSON出错:", exp, data)
        return {}


def format_time_by_time(t, f="%Y-%m-%d %H:%M:%S"):
    return time.strftime(f, time.localtime(t))


def bytes_to_str(data: bytes or str) -> str:
    if not data:
        return ""
    if isinstance(data, bytes):
        return data.decode('utf-8')
    return str(data)


def filter_emoji_2(des_str, replace_str='?'):
    """
    只过滤emoji表情
    :param des_str: 需要过滤的字符串
    :param replace_str: 需要替换的字符串
    """
    return des_str

    # co = re.compile(u'[\U00010000-\U0010ffff\\u2600-\\u27ff\\uD800-\\uDBFF\\uDC00-\\uDFFF]')
    # return co.sub(replace_str, str(des_str))


def ip_address_format(ip):
    """
    INT 型 IP 地址转换成 IPV4 字符串
    :param ip: 1912018224
    """
    return str(ipaddress.ip_address(ip))


def get_public_phone_number(phone: str):
    if not phone:
        return ''
    if len(phone) != 11:
        return phone
    return phone[0:3] + "****" + phone[7:]


def get_num_in_str(num_str: str):
    """
    获取字符串里的数字
    "2343dddwedff34" --> 234334
    """
    return re.sub('\\D', "", num_str)


def to_dict(data: bytes or str):
    if data:
        if isinstance(data, dict) or isinstance(data, list):
            return data
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        try:
            return ast.literal_eval(data)
        except (ValueError, SyntaxError):
            pass
        try:
            return json.loads(data)
        except (SyntaxError, ValueError):
            file_log.failed('解析字典或json字符串出错, 数据格式错误:', data)
    return {}


def fmt_timestamp(time_stamp: float or int, fmt='%Y-%m-%d %H:%M:%S'):
    info = datetime.datetime.fromtimestamp(time_stamp)
    return info.strftime(fmt)


def str_to_datetime(s: str, fmt='%Y-%m-%d %H:%M:%S'):
    try:
        return datetime.datetime.strptime(s, fmt)
    except ValueError:
        return None


def date_to_str(date=None, fmt='%Y%m%d%H%M%S'):
    if not date:
        date = datetime.datetime.now()
    return date.strftime(fmt)


def today_str():
    """当天"""
    return date_to_str(fmt='%Y-%m-%d')


def last_day_str():
    """昨天"""
    return date_to_str(datetime.datetime.now() - datetime.timedelta(days=1), fmt='%Y-%m-%d')


def cur_week_str():
    """当前周 下划线"""
    return date_to_str(datetime.datetime.now(), fmt='%Y_%W')


def last_week_str():
    """上周 下划线"""
    return date_to_str(datetime.datetime.now() - datetime.timedelta(weeks=1), fmt='%Y_%W')


def cur_month_str():
    """当前月 间隔线"""
    return date_to_str(datetime.datetime.now(), fmt='%Y-%m')


def last_month_str():
    """上月 间隔线"""
    cur_date = datetime.datetime.now()
    return date_to_str(datetime.date(cur_date.year, cur_date.month, 1) - datetime.timedelta(days=1), fmt='%Y-%m')


def get_start_end_time(time_stamp: int):
    """获取该天开始和结束的时间戳"""
    date = datetime.datetime.strptime(
        datetime.datetime.fromtimestamp(time_stamp).date().strftime('%Y%m%d%H%M%S'), '%Y%m%d%H%M%S')
    next_date = date + datetime.timedelta(days=1)
    return datetime.datetime.timestamp(date), datetime.datetime.timestamp(next_date)


def today_timestamp():
    return int(time.mktime(datetime.date.today().timetuple()))


def timestamp_today():  # 返回当天0时的时间戳int型
    any_day = datetime.date(2011, 11, 1)
    date_today = any_day.today()
    date_str = time.strptime(str(date_today), "%Y-%m-%d")
    return int(time.mktime(date_str))


def timestamp_yesterday():  # 返回昨天的0点的时间戳
    return timestamp_today() - 24 * 60 * 60


def timestamp_seven_day():  # 返七天前0点时间戳
    return timestamp_today() - 7 * (24 * 60 * 60)


def timestamp_thirty_day():  # 返三十天前0点时间戳
    return timestamp_today() - 30 * (24 * 60 * 60)


def create_random_num(num: int):
    """生成指定长度的随机数"""
    return random.randint(10 ** (num - 1), 10 ** num - 1)


def cur_min_timestamp():
    dt = datetime.datetime.now()
    new_time = dt.replace(second=0, microsecond=0)
    return int(time.mktime(new_time.timetuple()))


def is_same_day(time_stamp: float or int):
    date = datetime.datetime.fromtimestamp(time_stamp)
    cur_date = datetime.datetime.now()
    fmt = '%Y%m%d'
    return date.strftime(fmt) == cur_date.strftime(fmt)


def is_same_week(time_stamp: float or int):
    date = datetime.datetime.fromtimestamp(time_stamp)
    cur_date = datetime.datetime.now()
    fmt = '%Y_%U'
    print(cur_date.strftime(fmt))
    print(date.strftime(fmt))
    return date.strftime(fmt) == cur_date.strftime(fmt)


def is_same_week_new(time_stamp: float or int):
    # 以前的is_same_week 周日的话 date和cur_date会不是同一周，所以使用一周开始来判断
    cur_date = datetime.datetime.now()
    cur_date_begin = cur_date - datetime.timedelta(days=cur_date.weekday())
    cur_time_begin = cur_date_begin.replace(hour=0, minute=0, second=0, microsecond=0)
    cur_time_begin_stamp = int(time.mktime(cur_time_begin.timetuple()))
    date = datetime.datetime.fromtimestamp(time_stamp)
    new_date = date - datetime.timedelta(days=date.weekday())
    new_time = new_date.replace(hour=0, minute=0, second=0, microsecond=0)
    new_time_stamp = int(time.mktime(new_time.timetuple()))
    print(cur_time_begin_stamp)
    print(new_time_stamp)
    return cur_time_begin_stamp == new_time_stamp


def is_same_month(time_stamp: float or int):
    date = datetime.datetime.fromtimestamp(time_stamp)
    cur_date = datetime.datetime.now()
    fmt = '%Y-%m'
    return date.strftime(fmt) == cur_date.strftime(fmt)


def is_same_year(time_stamp: float or int):
    date = datetime.datetime.fromtimestamp(time_stamp)
    cur_date = datetime.datetime.now()
    fmt = '%Y'
    return date.strftime(fmt) == cur_date.strftime(fmt)


def in_timedelta(time_stamp: int or float, is_add=False, weeks=0, days=0, hours=0, minutes=0, seconds=0):
    """取距离指定时间前后具体时间段的时间戳"""
    date = datetime.datetime.fromtimestamp(time_stamp)
    t_date = datetime.timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds)
    new_date = date + t_date if is_add else date - t_date
    return int(time.mktime(new_date.timetuple()))


def dec_month_timedelta(time_stamp: int or float, months=0):
    date = datetime.datetime.fromtimestamp(time_stamp)
    if date.month > months:
        new_date = date.replace(month=date.month - months)
    else:
        year = months // 12
        new_month = months % 12
        if date.month <= new_month:
            new_month = 12 + date.month - new_month
            year = date.year - (year + 1)
        else:
            new_month = date.month - new_month
            year = date.year - year
        new_date = date.replace(year=year, month=new_month)
    return int(time.mktime(new_date.timetuple()))


def get_day_begin(time_stamp: int or float):
    """获取指定时间戳的零点"""
    date = datetime.datetime.fromtimestamp(time_stamp)
    new_time = date.replace(hour=0, minute=0, second=0, microsecond=0)
    return int(time.mktime(new_time.timetuple()))


def get_day_end(time_stamp: int or float):
    """获取指定时间戳的当天的最后一秒"""
    date = datetime.datetime.fromtimestamp(time_stamp)
    new_time = date.replace(hour=23, minute=59, second=59, microsecond=0)
    return int(time.mktime(new_time.timetuple()))


def get_week_begin(time_stamp: int or float):
    """获取指定时间戳的所在周的零点"""
    date = datetime.datetime.fromtimestamp(time_stamp)
    new_date = date - datetime.timedelta(days=date.weekday())
    new_time = new_date.replace(hour=0, minute=0, second=0, microsecond=0)
    return int(time.mktime(new_time.timetuple()))


def get_month_begin(time_stamp: int or float):
    """获取指定时间戳的所在月的零点"""
    date = datetime.datetime.fromtimestamp(time_stamp)
    new_time = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return int(time.mktime(new_time.timetuple()))


def get_next_month_begin(time_stamp: int or float):
    """获取指定时间戳的所在月的结束时间"""
    date = datetime.datetime.fromtimestamp(time_stamp)
    new_time = date.replace(month=date.month + 1, day=1, hour=0, minute=0, second=0, microsecond=0)
    return int(time.mktime(new_time.timetuple()))


def base_encrypt(code_str: str):
    """常规加密"""
    if not isinstance(code_str, str):
        code_str = str(code_str)
    new_str = base64.b64encode(bytes(code_str, 'utf-8')).decode('utf-8')
    return str(random_com.random_num(6)) + new_str[0: len(new_str) - 2]


def base_decrypt(code_str: str):
    """常规解密"""
    if not isinstance(code_str, str):
        code_str = str(code_str)
    code_str = code_str[6: len(code_str)] + "=="
    try:
        return base64.b64decode(code_str).decode('utf-8')
    except (UnicodeDecodeError, TypeError, binascii.Error):
        return ""


def aes_encrypt(secret_key: str, item_str: str, aes_mode=AES.MODE_GCM):
    """AES加密"""
    iv = os.urandom(12)
    aes = AES.new(binascii.unhexlify(secret_key), aes_mode, iv)
    params, tag = aes.encrypt_and_digest(item_str.encode("utf-8"))
    base64_data = iv + params + tag
    return str(base64.b64encode(base64_data), encoding='utf-8')


def aes_decrypt(secret_key: str, item_str: str, aes_mode=AES.MODE_GCM):
    """AES解密"""
    encrypted_text = base64.b64decode(item_str)
    cipher = AES.new(binascii.unhexlify(secret_key), aes_mode, encrypted_text[:12])
    return cipher.decrypt_and_verify(encrypted_text[12:-16], encrypted_text[-16:])


def check_password(pwd: str):
    pass_require = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                    'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                    '.', '-', '_', '+', '=', '@', '$', '!', ',', '*', '(', ')', ',', '?']
    for item in pwd:
        if item.upper() not in pass_require:
            return False, item
    return True, pwd


def random_list_item(item_list: list, rate_arr=None, base_ratio=10000):
    """
    按概率随机获取列表里的某项 采用分段步进取值方式

    :param item_list: 取值的列表
    :param rate_arr: 概率列表 不传默认等概率
    :param base_ratio: 概率的比例基数
    """
    if not item_list:
        return None, 0
    if not base_ratio:
        base_ratio = 10000
    len_item = len(item_list)
    if not rate_arr:
        rate_arr = [(base_ratio / len_item) for _ in range(0, len_item)]
    len_rate = len(rate_arr)
    if len_item != len_rate:
        extra_num = len_item - len_rate
        if extra_num > 0:
            tmp_arr = [0 for _ in range(extra_num)]
            rate_arr += tmp_arr
        else:
            rate_arr = rate_arr[0: len_item]
    lottery_num = random.randint(1, sum(rate_arr))
    item_num, total_num = 0, 0
    for num in rate_arr:
        total_num += num
        if lottery_num <= total_num:
            return item_list[item_num], item_num
        item_num += 1
    return item_list[-1], item_num


def escape_str(str_data: str, is_json_str=False):
    if is_json_str:
        return filter_emoji_2(str_data).replace("\\n", "\\\\n").replace("\\r", "\\\\r").replace("%", "%%") \
            .replace('\032', '\\Z').replace("'", "\\'")
    return filter_emoji_2(str_data).replace("\\n", "\\\\n").replace("\\r", "\\\\r").replace("%", "%%") \
        .replace('\032', '\\Z').replace("'", "\\'").replace('"', '\\"')


def second_to_str(second: int):
    if not second:
        return "(永久)"
    if second < 86400:
        return "({0}小时)".format(int(second / 3600))
    return "({0}天)".format(int(second / 86400))


def up_count_str(amount: int):
    if amount < 10000:
        return str(amount)
    if 100000000 > amount >= 10000:
        return "{0}万".format(str(round(amount / 10000, 4))[0:6])
    if 1000000000000 > amount >= 100000000:
        return "{0}亿".format(str(round(amount / 100000000, 4))[0:6])
    return "{0}万亿".format(str(round(amount / 1000000000000, 4))[0:6])


def extract_num(s: str):
    return re.sub('/D', '', (s or ''))


def is_mobile_num(mobile: str):
    return re.match(r'^1[3456789]\d{9}', mobile)


def is_id_card_num(ID_num: str):
    """二代身份证校验（不适用于一代）"""
    if re.match(r'^[1-8]{2}[1-9]{4}[0-2][0-9]{3}[0-1][0-9][0-3]\d{4}[\dXx]$', ID_num):
        # 权位因子
        weight_F = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        # 二代身份证尾数校验码
        check_code = ["1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"]
        sum_num, i = 0, 0
        while i < len(weight_F):
            sum_num += weight_F[i] * int(ID_num[i])
            i += 1
        return True if check_code[sum_num % 11] == ID_num[-1].upper() else False


def is_https_url_link(url_str: str):
    return re.match(r'^https?:/{2}\w.+$', url_str, re.IGNORECASE)


def is_http_url_link(url_str: str):
    return re.match(r'^http?:/{2}\w.+$', url_str, re.IGNORECASE)


def is_ws_link(url_str: str):
    return re.match(r'^wss?:/{2}\w.+$', url_str, re.IGNORECASE)


def is_decimal(num_str: str):
    return re.match(r'(\d)|(^\d\.\d$)', num_str)


def is_color_val(color: str):
    return re.match(r'^#[A-Fa-f0-9]{6}', color)


def random_choice_by_weight(req: list, weights: list):
    data = req  # 定义数据
    rand = random.random()  # 获取一个0到1之间的随机数
    if rand < weights[0]:
        result = data[0]
    else:
        result = data[1]
    return result


def random_name():
    count = random.randint(2, 4)
    first_name = '赵钱孙李周吴郑王戚谢邹喻顾孟平黄熊纪舒屈江童颜郭郁单杭洪裴陆荣翁姬申扶堵漆雕乐正汝鄢涂钦羊舌微生伍余元卜伟刚勇毅俊峰强军平保东' \
                 '文辉力明永健世广志义兴良海山仁波宁贵福生龙元全国胜学祥才发武新利清'
    second_name = '赵钱孙李周吴郑王戚谢邹喻顾孟平黄熊纪舒屈江童颜郭郁单杭洪裴陆荣翁姬申扶堵漆雕乐正汝鄢涂钦羊舌微生伍余元卜伟刚勇毅俊峰强军平保' \
                  '东文辉力明永健世广志义兴良海山仁波宁贵福生龙元全国胜学祥才发武新利清豪言玉意泽彦轩景正程诚宇澄安青泽轩旭恒思宇嘉宏皓成宇' \
                  '轩玮桦宇达韵磊泽博昌信彤逸柏新劲鸿文恩远翰圣哲家林景行律本乐康昊宇麦冬景武茂才军林茂飞昊明明天伦峰志辰亦'
    last_name = '佳彤自怡颖宸雅微羽馨思纾欣元凡晴玥宁佳蕾桑妍萱宛欣灵烟文柏艺以如雪璐言婷青安昕淑雅颖云艺忻梓江丽梦雪沁思羽羽雅访烟萱忆慧娅茹嘉' \
                '幻辰妍雨蕊欣芸亦海山仁波宁贵福生龙元全国胜学祥才发武新利清豪言玉意泽彦轩景正程诚宇澄安青泽轩旭恒思宇嘉宏皓成文恩远翰圣哲家林景' \
                '行律本乐康昊宇麦冬景武茂才军林茂飞昊明'
    first_name = random.choice(first_name)
    second_name = random.choice(second_name)
    third_name = random.choice(second_name)
    last_name = random.choice(last_name)
    name = "志义兴"
    if count == 2:
        name = first_name + second_name
    if count == 3:
        name = first_name + second_name + third_name
    if count == 4:
        name = first_name + second_name + third_name + last_name
    return name


def is_all_english(strs: str):
    import string
    for i in strs:
        if i not in string.ascii_lowercase + string.ascii_uppercase:
            return False
    return True


class DFAFilter(object):
    def __init__(self):
        self.keyword_chains = {}  # 关键词链表
        self.delimit = '\x00'  # 限定

    def add(self, keyword):
        keyword = keyword.lower()  # 关键词英文变为小写
        chars = keyword.strip()  # 关键字去除首尾空格和换行
        if not chars:  # 如果关键词为空直接返回
            return
        level = self.keyword_chains
        # 遍历关键字的每个字
        for i in range(len(chars)):
            # 如果这个字已经存在字符链的key中就进入其子字典
            if chars[i] in level:
                level = level[chars[i]]
            else:
                if not isinstance(level, dict):
                    break
                for j in range(i, len(chars)):
                    level[chars[j]] = {}
                    last_level, last_char = level, chars[j]
                    level = level[chars[j]]
                last_level[last_char] = {self.delimit: 0}
                break
        if i == len(chars) - 1:
            level[self.delimit] = 0

    def parse(self, path):
        with open(path, encoding='utf-8') as f:
            for keyword in f:
                self.add(str(keyword).strip())
        print(self.keyword_chains)

    def filter(self, message, repl="*"):
        message = message.lower()
        ret = []
        start = 0
        while start < len(message):
            level = self.keyword_chains
            step_ins = 0
            for char in message[start:]:
                if char in level:
                    step_ins += 1
                    if self.delimit not in level[char]:
                        level = level[char]
                    else:
                        ret.append(repl * step_ins)
                        start += step_ins - 1
                        break
                else:
                    ret.append(message[start])
                    break
            else:
                ret.append(message[start])
            start += 1

        return ''.join(ret)



def get_obtain_order_number():
    # 获取当前时间
    current_time = datetime.datetime.now()
    # 格式化时间为年月日时分秒的字符串
    time_str = current_time.strftime("%Y%m%d%H%M%S")
    # 生成一个随机的字符串作为订单号的一部分
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    # 组合时间和随机字符串生成订单号
    order_number = f"{time_str}{random_str}"
    print("生成的订单号:", order_number)
    return order_number
