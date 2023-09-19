import datetime
import random
import string


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
