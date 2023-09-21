import json

import redis

from configs import config
from models import task_model, server_model
# from models import server_model
from models.player_friendship import friend_model
from utils import utils

_seconds = 120  # 语音超时的秒数
_connect = None  # 共享的redis连接对象


def connect(redis_name='redis_base'):
    try:
        redis_info = config.get_by_key(redis_name)  # redis的数据
        return redis.StrictRedis(**redis_info)
    except Exception as data:
        print("Please set configs of ", redis_name, data)


def share_connect() -> redis.StrictRedis:
    global _connect
    if not _connect:
        _connect = connect("redis_base")
    return _connect


def save(key, value):
    share_connect().set(key, value, ex=_seconds)


def save_with_time(key, value, time=3600):
    share_connect().set(key, value, ex=time)


def fetch(key):
    return share_connect().get(key)


def add_to_set(key, values):
    return share_connect().sadd(key, values)


def pop_from_set(key):
    return share_connect().spop(key)


def _hash_to_dict(data):
    result = dict()
    if not data:
        return result
    for k, v in list(data.items()):
        result[utils.bytes_to_str(k)] = utils.check_int(utils.bytes_to_str(v))
    return result


def get_table_info(room_id):
    if not share_connect():
        return ""
    key = "table_info"
    data = utils.json_decode((share_connect().hget(key, room_id) or b"").decode("utf-8"))
    return data


def get_all_configs():
    name = "all_system_configs"
    data = share_connect().hgetall(name)
    if not data:
        return dict()
    return _hash_to_dict(data)


def update_club_redis(club_id, rooms):
    name = 'club' + str(club_id)
    return share_connect().sadd(name, rooms)


def get_bytes_access_token():
    name = "bytes_access_token"
    data = share_connect().get(name)
    if data:
        return bytes.decode(data)
    return ""


def set_bytes_access_token(value):
    name = "bytes_access_token"
    return share_connect().set(name, value, ex=3600)


def get_club_rooms(club_id):
    key = "club" + str(club_id)
    return share_connect().smembers(key)


def set_configs_multi(configs):
    name = "all_system_configs"
    return share_connect().hmset(name, configs)
    # return share_connect().hset(name, 1, 2)


def set_lottery_configs(configs):
    name = "lottery_configs"
    return save_with_time(name, json.dumps(configs), 7200)


def get_lottery_configs():
    name = "lottery_configs"
    return fetch(name)


def save_sign(sign, expired=1800):
    name = "sign:" + sign
    return share_connect().setex(name, expired, 1)


def set_phone_code(phone, code):
    name = "code_" + str(phone)
    return save_with_time(name, code, 7200)


def get_phone_code(phone):
    name = "code_" + str(phone)
    return utils.bytes_to_str(fetch(name))


def get_sign_exist(sign):
    name = "sign:" + sign
    result = share_connect().get(name)
    return utils.str_to_int(utils.bytes_to_str(result)) > 0


def save_code_sign(sign, expired=1800):
    name = "codesign:" + sign
    return share_connect().setex(name, expired, 1)


# def save_child_game_command(command):
#     name = "command"
#     return share_connect().sadd(name, command)

# def get_xxc_info():
#     name = "hall_xxc_info"
#     data = share_connect().get(name)
#     if data:
#         return eval(data)
#     return []
#
#
# def save_xxc_info(xxc_info):
#     name = "hall_xxc_info"
#     return share_connect().set(name, xxc_info)
#
#
# def get_gz_xxc_info():
#     name = "hall_gz_xxc_info"
#     data = utils.to_dict(share_connect().get(name))
#     if data:
#         return data
#     return []
#
#
# def save_gz_xxc_info(xxc_info):
#     name = "hall_gz_xxc_info"
#     return share_connect().set(name, xxc_info)


def get_face_config():
    name = "face_config"
    data = share_connect().get(name)
    if data:
        return eval(data)
    return []


def get_player_xxc_last_lose_count(uid):
    name = "xxc_last_lose_count" + utils.today_str()
    data = share_connect().hget(name, uid)
    return eval(data) if data else 0


def get_player_gz_xxc_last_lose_count(uid):
    name = "gz_xxc_last_lose_count" + utils.today_str()
    data = share_connect().hget(name, uid)
    return eval(data) if data else 0


def get_player_xxc_hui_fu_count(uid):
    name = "xxc_hui_fu_count" + utils.today_str()
    data = share_connect().hget(name, uid)
    return eval(data) if data else 0


def set_player_xxc_hui_fu_count(uid, count):
    name = "xxc_hui_fu_count" + utils.today_str()
    share_connect().hset(name, uid, count)


def set_player_xxc_last_lose_count(uid, count):
    name = "xxc_last_lose_count" + utils.today_str()
    share_connect().hset(name, uid, count)


def get_xxc_player_jiu_ji_count(uid):
    name = "xxc_jiu_ji_count" + utils.today_str()
    data = share_connect().hget(name, uid)
    if data:
        return eval(data)
    return 0


def get_player_xxc_bu_zhu_count(uid):
    name = "xxc_bu_zhu_count" + utils.today_str()
    data = share_connect().hget(name, uid)
    return eval(data) if data else 0


def set_player_xxc_jiu_ji_count(uid, count):
    name = "xxc_jiu_ji_count" + utils.today_str()
    share_connect().hset(name, uid, count)


def set_player_xxc_bu_zhu_count(uid, count):
    name = "xxc_bu_zhu_count" + utils.today_str()
    share_connect().hset(name, uid, count)


def save_face_config(xxc_info):
    name = "face_config"
    return share_connect().set(name, xxc_info)


def get_hall_match_info():
    name = "hall_match_info"
    data = share_connect().get(name)
    if data:
        return eval(data)
    return []


def get_xxc_server_info():
    name = "hall_xxcserver_info"
    data = share_connect().get(name)
    if data:
        return eval(data)
    return []


def get_gz_xxc_server_info():
    name = "hall_gzxxcserver_info"
    data = share_connect().get(name)
    if data:
        return eval(data)
    return []


def get_xxc_server_info_new(prefix):
    if not prefix:
        return []
    name = "hall_{}xxc_server_info".format(prefix)
    data = share_connect().get(name)
    if data:
        return eval(data)
    return []


def get_xxc_real_count():
    name = "MXXC_REAL_TIME_COUNT"
    data = share_connect().hgetall(name)
    if data:
        return data
    return []


def save_xxc_server_info(xxc_info):
    name = "hall_xxcserver_info"
    return share_connect().set(name, xxc_info)


def save_gzxxc_server_info(xxc_info):
    name = "hall_gzxxcserver_info"
    return share_connect().set(name, xxc_info)


def save_xxc_server_info_new(xxc_info, prefix):
    name = "hall_{}xxc_server_info".format(prefix)
    return share_connect().set(name, xxc_info)


def save_hall_match_info(xxc_info):
    name = "hall_match_info"
    return share_connect().set(name, xxc_info)


def get_code_sign_exist(sign):
    name = "codesign:" + sign
    result = share_connect().get(name)
    return utils.str_to_int(utils.bytes_to_str(result)) > 0


def save_code_uid(sign, uid, expired=1800):
    name = "codeuid:" + sign
    return share_connect().setex(name, expired, uid)


def get_code_uid_exist(sign):
    name = "codeuid:" + str(sign)
    result = share_connect().get(name)
    return result


def check_code_used(code):
    name = "check_code"
    return share_connect().sismember(name, code)


def add_used_code(code):
    name = "check_code"
    return share_connect().sadd(name, code)


def save_exception(data, max_nums=1000):
    key = "client_exceptions"
    share_connect().lpush(key, data)
    share_connect().ltrim(key, 0, max_nums)


def get_all_exception(max_nums=1000):
    key = "client_exceptions"
    return share_connect().lrange(key, 0, max_nums)


def remove_all_exception():
    key = "client_exceptions"
    return share_connect().ltrim(key, 0, 0)


def get_all_play_details():
    key = "round_review_logs"
    return share_connect().lrange(key, 0, -1)


def get_all_club_rooms():
    key = "club_rooms"
    return share_connect().lrange(key, 0, -1)


def get_all_club_room_details():
    key = "club_room_details"
    return share_connect().lrange(key, 0, -1)


def get_club_room_details(club_room):
    key = club_room
    return share_connect().lrange(key, 0, -1)


def get_100_play_details():
    key = "round_review_logs"
    return share_connect().lrange(key, -100, -1)


def delete_play_detail(value):
    key = "round_review_logs"
    return share_connect().lrem(key, 1, value)


def set_login_try_count(ip, count):
    if not ip:
        return
    name = "al:{0}".format(ip)
    share_connect().hmset(name, {"count": count, "time": utils.timestamp()})
    return share_connect().expire(name, 2 * 60 * 60)


def get_friend_info(conn, uid, update=False):
    # name = "friend_list"+str(uid)
    # if not update:
    #     friend_info = share_connect().get(name)
    #     if friend_info:
    #         return eval(friend_info)
    friend_info = friend_model.get_by_uid(conn, uid)
    # share_connect().set(name, friend_info)
    return friend_info


def get_apply_list_by_uid(conn, uid):
    name = "apply_list" + str(uid)
    apply_list = share_connect().get(name)
    if apply_list:
        return eval(apply_list)
    apply_list = friend_model.get_apply_list_by_uid(conn, uid)
    share_connect().set(name, apply_list)
    return apply_list


# def get_server_info(conn, game_type):
#     game_type = str(game_type)
#     name = "room_link"
#     servers = share_connect().hget(name, game_type)
#     if servers:
#         return utils.to_dict(servers)
#     servers = server_model.get_all_room_by_game_type(conn, game_type)
#     info = {}
#     if servers:
#         for server in servers:
#             info[server.get('sid')] = server
#         share_connect().hset(name, game_type, str(info))
#     return info
#
#
# def get_all_game_type(conn):
#     name = "GAME_TYPE_ALL"
#     all_type = utils.to_dict(share_connect().get(name)) or {}
#     if all_type:
#         return all_type
#     type_list = server_model.get_all_room(conn) or []
#     for item in type_list:
#         all_type[item.get('game_type')] = item.get('memo')
#     all_type and share_connect().set(name, all_type)
#     return all_type


def get_guan_jie_sta(self, uid):
    name = "guan_jie_sta"
    data = share_connect().hget(name, uid)
    if data:
        return data.decode("utf8")
    info = self.player_model.get_guan_jie_record(uid)
    data = info.get("guan_jie_sta")
    return data


def get_sai_ji_tan_chuang_sta(self, uid):
    cur_time = utils.timestamp()
    cur_week = int(utils.fmt_timestamp(cur_time, fmt='%Y%W'))
    name = "sai_ji_tan_chuang_sta" + str(cur_week)
    data = share_connect().hget(name, uid)
    if data:
        return eval(data)
    info = self.player_model.get_sai_ji_gx_record(uid)
    data = info.get("sai_ji_tan_chuang_sta")
    return data


def remove_server_info(game_type: int):
    share_connect().hdel('room_link', game_type)
    share_connect().delete('GAME_TYPE_ALL')


def get_min_p_count_server(game_type: int, sid_list: list):
    name = "SERVER_PLAYER_COUNT_{0}".format(game_type)
    s_info = share_connect().hgetall(name) or {}
    if not s_info or len(sid_list) == 1:
        return sid_list[0]
    len_s_info = len(s_info)
    if len_s_info < len(sid_list):
        return sid_list[len_s_info]
    min_sid, min_count = 0, 0
    for sid, count in s_info.items():
        sid, count = int(sid), int(count)
        if not min_sid:
            min_sid, min_count = sid, count
        if count <= min_count:
            min_sid, min_count = sid, count
    return min_sid


def publish_msg_to_server(channel, message):
    share_connect().publish(channel, utils.json_encode(message, is_cut=True))


def get_club_members_info(club_id):
    name = "club_members_info"
    return share_connect().hget(name, str(club_id))


def save_club_info(club_id, club_info):
    name = "club_info"
    share_connect().hset(name, club_id, club_info)


def save_club_members_info(club_id, members_info):
    name = "club_members_info"
    share_connect().hset(name, club_id, members_info)


def get_club_info(club_id):
    name = "club_info"
    share_connect().hget(name, str(club_id))


# def get_create_room_link_url(conn, game_type):
#     name = "room_link"
#     url = share_connect().hget(name, game_type)
#     if not url:
#         all_server_rooms = server_model.get_all_room(conn)
#         for room in all_server_rooms:
#             share_connect().hset(name, room.get('game_type'), room)
#     data = share_connect().hget(name, game_type)
#     return data


# def get_room_link_by_server_id(conn, server_id):
#     name = "room_link_"
#     if not share_connect().hexists(name, server_id):
#         server_room = server_model.get_room_link_server_id(conn, server_id)
#         share_connect().hset(name, server_id, str(server_room))
#     data = share_connect().hget(name, server_id)
#     return utils.to_dict(data)


# def set_create_room_link_url(conn, game_type, setting, sid=1):
#     name = "room_link"
#     server_model.set_create_room_link_url(conn, game_type, setting, sid)
#     share_connect().hset(name, game_type, setting)


def get_player_table_server(uid):
    name = "p_t_s"
    data = share_connect().hget(name, uid)
    if data:
        return eval(data)
    return


# def get_player_room_info(uid):
#     name = "p_in_r"
#     # data = share_connect().hget(name, uid)
#     # if data:
#     #     return eval(data)
#     return {}
#
#
# def save_player_room_info(uid, data):
#     name = "p_in_r"
#     if uid > 10000:
#         return share_connect().hset(name, uid, data)


def get_enter_room_count():
    return share_connect().hlen('p_in_r') or 0


def get_enter_match_count():
    return share_connect().hlen('p_in_m') or 0


def save_player_match_info(uid, qi_ci):
    name = "p_in_m"
    return share_connect().hset(name, uid, qi_ci)


def remove_player_match_info(uid):
    name = "p_in_m"
    return share_connect().hdel(name, uid)


def get_player_match_info(uid: int):
    return utils.to_dict(share_connect().hget('p_in_m', uid)) or None


def get_all_p_in_m_uid():
    p_in_m = share_connect().hkeys('p_in_m') or []
    p_in_dss = share_connect().hkeys('p_in_dss_bm') or []
    return p_in_m + p_in_dss


def get_server_info(conn, game_type):
    game_type = str(game_type)
    name = "room_link"
    servers = share_connect().hget(name, game_type)
    if servers:
        return utils.to_dict(servers)
    servers = server_model.get_all_room_by_game_type(conn, game_type)
    info = {}
    if servers:
        for server in servers:
            info[server.get('sid')] = server
        share_connect().hset(name, game_type, str(info))
    return info


def get_player_dss_bm_info(uid):
    return utils.to_dict(share_connect().hget('p_in_dss_bm', uid)) or None


def get_friends_by_uid(conn, uid, update=True):
    name = "friend_list"

    if not update:
        friend_lists = share_connect().hget(name, str(uid))
        if not friend_lists:
            friend_lists = friend_model.get_friends_by_uid(conn, uid)
            share_connect().hset(name, str(uid), friend_lists)
        else:
            friend_lists = eval(friend_lists)
        return friend_lists
    else:
        friend_lists = friend_model.get_friends_by_uid(conn, uid)
        share_connect().hset(name, uid, friend_lists)
        return friend_lists


# def get_game_room_link(conn, game_type, update=False):
#     name = "room_link"
#     data = share_connect().hget(name, game_type)
#     if not data or update:
#         settings = server_model.get_all_room(conn)
#         for setting in settings:
#             game_type1 = setting.get('game_type')
#             share_connect().hset(name, game_type1, setting)
#
#         data = share_connect().hget(name, game_type)
#         if data:
#             return eval(data)
#         return None
#     else:
#         return eval(data)


# def query_cbs_ranking(query_date: int, bd_type=1):
#     if bd_type == 1:
#         name = "cbs_phb_rb_" + utils.fmt_timestamp(query_date, fmt='%Y-%m-%d')
#     elif bd_type == 2:
#         name = "cbs_phb_zb_" + utils.fmt_timestamp(query_date, fmt='%Y_%W')
#     else:
#         name = "cbs_phb_yb_" + utils.fmt_timestamp(query_date, fmt='%Y-%m')
#     return share_connect().exists(name)


def cbs_get_rank_list(rank_id: str, start, end, bd=1):
    if bd == 1:
        name = "cbs_phb_rb_" + rank_id
    elif bd == 2:
        name = "cbs_phb_zb_" + rank_id
    else:
        name = "cbs_phb_yb_" + rank_id
    return share_connect().zrange(name, start, end, desc=True, withscores=True) or [], share_connect().zcard(name)


def cbs_get_uid_ranking(rank_id: str, uid, bd=1):
    if bd == 1:
        name = "cbs_phb_rb_" + rank_id
    elif bd == 2:
        name = "cbs_phb_zb_" + rank_id
    else:
        name = "cbs_phb_yb_" + rank_id
    ranking = share_connect().zrevrank(name, uid)
    score = share_connect().zscore(name, uid)
    return 0 if ranking is None else ranking + 1, score or 0


def is_exist_hash_kv(name: str, key):
    return share_connect().hexists(name, key)


def get_task_configs(conn, task_type=1):
    name = "task_configs_" + str(task_type)
    data = share_connect().get(name)
    if data:
        return utils.to_dict(data)
    else:
        data = task_model.get_task_by_type(conn, task_type) or []
        if data:
            share_connect().set(name, data)
        return data


def cbs_get_player_info():
    name = "cbs_player_info" + utils.today_str()
    return share_connect().hkeys(name) or []


def cbs_get_player_info_count():
    name = "cbs_player_info" + utils.today_str()
    return share_connect().hlen(name) or 0


def cbs_query_player_by_uid(uid: int):
    name = "cbs_player_info" + utils.today_str()
    return utils.to_dict(share_connect().hget(name, uid)) or {}


def cbs_query_pi_pei_player():
    name = "cbs_pi_pei" + utils.today_str()
    return share_connect().zrange(name, 0, -1) or []


def cbs_query_pi_pei_player_count():
    name = "cbs_pi_pei" + utils.today_str()
    return share_connect().zlexcount(name, '-', '+') or 0


def cbs_query_pi_pei_top_100():
    name = 'cbs_pi_pei_top_100' + utils.today_str()
    return share_connect().zrange(name, 0, -1) or []


def cbs_query_pi_pei_top_100_count():
    name = 'cbs_pi_pei_top_100' + utils.today_str()
    return share_connect().zlexcount(name, '-', '+') or 0


def cbs_query_in_pi_pei(uid: int):
    name = 'cbs_pi_pei' + utils.today_str()
    return share_connect().zrank(name, uid)


def cbs_query_in_pi_pei_top(uid: int):
    name = 'cbs_pi_pei_top_100' + utils.today_str()
    return share_connect().zrank(name, uid)


def cbs_query_playing_player():
    name = "cbs_playing_player" + utils.today_str()
    data = share_connect().smembers(name) or {}
    return [int(item) for item in data]


def cbs_query_playing_player_count():
    name = "cbs_playing_player" + utils.today_str()
    return share_connect().scard(name) or 0


def cbs_query_bao_ming_player():
    name = "cbs_bao_ming_player" + utils.today_str()
    data = share_connect().smembers(name) or {}
    return [int(item) for item in data]


def cbs_query_bao_ming_player_count():
    name = "cbs_bao_ming_player" + utils.today_str()
    return share_connect().scard(name) or 0


def get_cbs_judge_info(tid):
    name = "match_judge_info"
    data = share_connect().hget(name, tid)
    return utils.to_dict(data) if data else {}


def get_cbs_all_judge():
    name = "match_only_47"
    data = share_connect().hget(name, 47)
    return utils.to_dict(data) or {}


def cbs_manual_close_table(tid: int):
    share_connect().lpush('manual_close_judge', tid)


def get_check_update_info():
    return utils.to_dict(share_connect().get('CHECK_UPDATE_INFO'))


def add_version_info(info: dict):
    share_connect().set('CHECK_UPDATE_INFO', utils.json_encode(info, is_cut=True))


def del_version_info():
    share_connect().delete('CHECK_UPDATE_INFO')


def push_tui_song_mail(mail_data: dict):
    share_connect().rpush('MAIL_TUI_SONG_DATA', utils.json_encode(mail_data, is_cut=True))


def get_player_xxc_jiu_ji_count(uid):
    name = "xxc_jiu_ji_count" + utils.today_str()
    data = share_connect().hget(name, uid)
    if data:
        return eval(data)
    return 0


def get_player_xxc_bu_zhu_data(uid):
    name = "xxc_player_bu_zhu_count"
    data = share_connect().hget(name, uid)
    return eval(data) if data else 0


def get_player_lian_sheng(uid):
    name = "player_lian_sheng"
    data = share_connect().hget(name, uid)
    if data:
        return eval(data)
    return 0


def get_player_lian_sheng_gz(uid):
    name = "player_lian_sheng_gz"
    data = share_connect().hget(name, uid)
    return eval(data) if data else 0


def get_xxc_all_player_one(uid):
    name = "xxc_all_player"
    data = share_connect().hget(name, uid)
    if data:
        return eval(data)
    return {}


def get_xxc_player_one(xxc_id: int, uid: int):
    name = "xxc_all_player" + str(xxc_id)
    data = share_connect().hget(name, uid)
    return eval(data) if data else {}


def get_gz_xxc_player_one(xxc_id: int, uid: int):
    name = "gz_xxc_all_player" + str(xxc_id)
    data = share_connect().hget(name, uid)
    return eval(data) if data else {}


def get_xxc_all_player():
    name = "xxc_all_player"
    data = share_connect().hkeys(name)
    return data or []


def get_xxc_all_player_count():
    name = "xxc_all_player"
    data = share_connect().hlen(name)
    if data:
        return eval(data)
    return {}


def get_xxc_all_player_xxc_id(xxc_id):
    name = "xxc_all_player" + str(xxc_id)
    data = share_connect().hkeys(name)
    return data or []


def get_gz_xxc_all_player_xxc_id(xxc_id):
    name = "gz_xxc_all_player" + str(xxc_id)
    data = share_connect().hkeys(name)
    return data or []


def get_xxc_p_count_xxc_id(xxc_id, prefix=""):
    name = "sy_xxc_all_player" + str(xxc_id)
    if prefix:
        name = prefix + name
    data = share_connect().hlen(name)
    return data or 0


def get_gz_xxc_p_count_xxc_id(xxc_id):
    name = "gz_xxc_all_player" + str(xxc_id)
    data = share_connect().hlen(name)
    return data or 0


def get_xxc_all_table_one(xxc_id, tid):
    name = "xxc_all_table" + str(xxc_id)
    data = share_connect().hget(name, tid)
    if data:
        return eval(data)
    return {}


def get_gz_xxc_all_table_one(xxc_id, tid):
    name = "gz_xxc_all_table" + str(xxc_id)
    data = share_connect().hget(name, tid)
    if data:
        return eval(data)
    return {}


def get_xxc_all_table():
    name = "xxc_all_table"
    data = share_connect().hkeys(name)
    return data


def get_xxc_table_count_xxc_id(xxc_id):
    name = "xxc_all_table" + str(xxc_id)
    data = share_connect().hlen(name)
    return data or 0


def get_xxc_all_table_xxc_id(xxc_id):
    name = "xxc_all_table" + str(xxc_id)
    data = share_connect().hkeys(name)
    return data or []


def get_gz_xxc_all_table_xxc_id(xxc_id):
    name = "gz_xxc_all_table" + str(xxc_id)
    data = share_connect().hkeys(name)
    return data or []


def get_cur_run_jjs(match_id: int):
    return share_connect().hvals('jjs_{0}'.format(match_id)) or []


def get_cur_run_dss(match_id: int):
    return share_connect().hvals('dss_{0}'.format(match_id)) or []


def get_cur_run_jjs_qi_ci(match_id: int):
    return share_connect().hkeys('jjs_{0}'.format(match_id)) or []


def jjs_history_qi_ci(match_id: int, start: int, end: int):
    return share_connect().lrange('HISTORY_match_{0}'.format(match_id), start, end) or []


def jjs_total_history_qi_ci(match_id: int):
    return share_connect().llen('HISTORY_match_{0}'.format(match_id)) or 0


def jjs_playing_player(uid: int, qi_ci: str):
    return share_connect().sismember("jjs_playing_player{0}".format(qi_ci), uid) or {}


def dss_playing_player(uid: int, qi_ci: str):
    return share_connect().sismember("dss_playing_player{0}".format(qi_ci), uid) or {}


def jjs_pi_pei_player(uid: int, qi_ci: str):
    z_score = share_connect().zscore("jjs_pi_pei_player{0}".format(qi_ci), uid)
    return 0 if z_score is None else 1


def dss_pi_pei_player(uid: int, qi_ci: str):
    z_score = share_connect().zscore("dss_pi_pei_player{0}".format(qi_ci), uid)
    return 0 if z_score is None else 1


def jjs_pm_player(uid, qi_ci):
    return share_connect().zrank("jjs_pi_pei_player{0}".format(qi_ci), uid) or 0


def dss_pm_player(uid, qi_ci):
    return share_connect().zrank("dss_pi_pei_player{0}".format(qi_ci), uid) or 0


def jjs_bm_player(uid: int, qi_ci: str):
    return share_connect().sismember("jjs_bao_ming_player{0}".format(qi_ci), uid) or {}


def dss_bm_player(uid: int, qi_ci: str):
    return share_connect().sismember("dss_bao_ming_player{0}".format(qi_ci), uid) or {}


def jjs_out_player(uid: int, qi_ci: str):
    return utils.to_dict(share_connect().hget("jjs_out_player{0}".format(qi_ci), uid)) or {}


def dss_out_player(uid, qi_ci: str):
    return utils.to_dict(share_connect().hget("dss_out_player{0}".format(qi_ci), uid)) or {}


def jjs_playing_qi_ci():
    return share_connect().hvals("jjs_info_playing") or []


def jjs_playing_qi_ci_data(qi_ci: str):
    return utils.to_dict(share_connect().hget("jjs_info_playing", qi_ci)) or {}


def jjs_qi_ci_data(match_id: int):
    return share_connect().hvals('jjs_{0}'.format(match_id)) or []


def get_all_jjs_qi_ci(match_list: list):
    qc_list = []
    for match in match_list or []:
        match_id = match.get('id')
        bm_qcs = share_connect().hkeys('jjs_{0}'.format(match_id)) or []
        for b_bm_qc in bm_qcs:
            bm_qc = utils.bytes_to_str(b_bm_qc)
            if bm_qc not in qc_list:
                qc_list.append(bm_qc)
    run_qcs = share_connect().hkeys('jjs_info_playing') or []
    for b_run_qc in run_qcs:
        run_qc = utils.bytes_to_str(b_run_qc)
        if run_qc not in qc_list:
            qc_list.append(run_qc)
    return qc_list


def dss_qi_ci_data(match_id: int):
    return share_connect().hvals('dss_{0}{1}'.format(match_id, utils.today_str())) or []


def dss_playing_qi_ci():
    return share_connect().hvals("dss_info_playing") or []


def get_dss_playing_by_qi_ci(qi_ci: str):
    return utils.to_dict(share_connect().hget("dss_info_playing", qi_ci)) or {}


def get_all_dss_qi_ci(match_list: list):
    qc_list = []
    for match in match_list or []:
        match_id = match.get('id')
        bm_qcs = share_connect().hkeys('dss_{0}{1}'.format(match_id, utils.today_str())) or []
        for b_bm_qc in bm_qcs:
            bm_qc = utils.bytes_to_str(b_bm_qc)
            if bm_qc not in qc_list:
                qc_list.append(bm_qc)
    run_qcs = share_connect().hkeys('dss_info_playing') or []
    for b_run_qc in run_qcs:
        run_qc = utils.bytes_to_str(b_run_qc)
        if run_qc not in qc_list:
            qc_list.append(run_qc)
    return qc_list


def jjs_all_pi_pei(qc_list: list):
    p_uids = []
    for qc in qc_list:
        p_list = share_connect().zrange('jjs_pi_pei_player{0}'.format(qc), 0, -1) or []
        for uid in p_list:
            uid = int(uid)
            (uid not in p_uids) and p_uids.append(uid)
    return p_uids


def jjs_qi_ci_pi_pei(qi_ci: str):
    p_uids = []
    p_list = share_connect().zrange('jjs_pi_pei_player{0}'.format(qi_ci), 0, -1) or []
    for uid in p_list:
        uid = int(uid)
        uid > 20000 and (uid not in p_uids) and p_uids.append(uid)
    return p_uids


def dss_all_pi_pei(qc_list: list):
    p_uids = []
    for qc in qc_list:
        p_list = share_connect().zrange('dss_pi_pei_player{0}'.format(qc), 0, -1) or []
        for uid in p_list:
            uid = int(uid)
            (uid not in p_uids) and p_uids.append(uid)
    return p_uids


def dss_qi_ci_pi_pei(qi_ci: str):
    p_uids = []
    p_list = share_connect().zrange('dss_pi_pei_player{0}'.format(qi_ci), 0, -1) or []
    for uid in p_list:
        uid = int(uid)
        uid > 20000 and (uid not in p_uids) and p_uids.append(uid)
    return p_uids


def jjs_all_playing(qc_list: list):
    p_uids = []
    for qc in qc_list:
        p_list = share_connect().smembers('jjs_playing_player{0}'.format(qc)) or []
        for uid in p_list:
            uid = int(uid)
            (uid not in p_uids) and p_uids.append(uid)
    return p_uids


def jjs_qi_ci_playing(qi_ci: str):
    p_uids = []
    p_list = share_connect().smembers('jjs_playing_player{0}'.format(qi_ci)) or []
    for uid in p_list:
        uid = int(uid)
        uid > 20000 and (uid not in p_uids) and p_uids.append(uid)
    return p_uids


def dss_all_playing(qc_list: list):
    p_uids = []
    for qc in qc_list:
        p_list = share_connect().smembers('dss_playing_player{0}'.format(qc)) or []
        for uid in p_list:
            uid = int(uid)
            (uid not in p_uids) and p_uids.append(uid)
    return p_uids


def dss_qi_ci_playing(qi_ci: str):
    p_uids = []
    p_list = share_connect().smembers('dss_playing_player{0}'.format(qi_ci)) or []
    for uid in p_list:
        uid = int(uid)
        uid > 20000 and (uid not in p_uids) and p_uids.append(uid)
    return p_uids


def jjs_all_bao_ming(qc_list: list):
    p_uids = []
    for qc in qc_list:
        p_list = share_connect().smembers('jjs_bao_ming_player{0}'.format(qc)) or []
        for uid in p_list:
            uid = int(uid)
            (uid not in p_uids) and p_uids.append(uid)
    return p_uids


def jjs_qi_ci_bao_ming(qi_ci: str):
    p_uids = []
    p_list = share_connect().smembers('jjs_bao_ming_player{0}'.format(qi_ci)) or []
    for uid in p_list:
        uid = int(uid)
        uid > 20000 and (uid not in p_uids) and p_uids.append(uid)
    return p_uids


def dss_all_bao_ming(qc_list: list):
    p_uids = []
    for qc in qc_list:
        p_list = share_connect().smembers('dss_bao_ming_player{0}'.format(qc)) or []
        for uid in p_list:
            uid = int(uid)
            (uid not in p_uids) and p_uids.append(uid)
    return p_uids


def dss_qi_ci_bao_ming(qi_ci: str):
    p_uids = []
    p_list = share_connect().smembers('dss_bao_ming_player{0}'.format(qi_ci)) or []
    for uid in p_list:
        uid = int(uid)
        uid > 20000 and (uid not in p_uids) and p_uids.append(uid)
    return p_uids


def jjs_all_out(qc_list: list):
    p_uids = []
    for qc in qc_list:
        p_list = share_connect().hkeys('jjs_out_player{0}'.format(qc)) or []
        for uid in p_list:
            uid = int(uid)
            (uid not in p_uids) and p_uids.append(uid)
    return p_uids


def jjs_qi_ci_out(qi_ci: str):
    p_uids = []
    p_list = share_connect().hkeys('jjs_out_player{0}'.format(qi_ci)) or []
    for uid in p_list:
        uid = int(uid)
        uid > 20000 and (uid not in p_uids) and p_uids.append(uid)
    return p_uids


def dss_all_out(qc_list: list):
    p_uids = []
    for qc in qc_list:
        p_list = share_connect().hkeys('dss_out_player{0}'.format(qc)) or []
        for uid in p_list:
            uid = int(uid)
            (uid not in p_uids) and p_uids.append(uid)
    return p_uids


def dss_qi_ci_out(qi_ci: str):
    p_uids = []
    p_list = share_connect().hkeys('dss_out_player{0}'.format(qi_ci)) or []
    for uid in p_list:
        uid = int(uid)
        uid > 20000 and (uid not in p_uids) and p_uids.append(uid)
    return p_uids


def get_gz_yi_chang_tables(page: int, amount: int):
    d_list = share_connect().lrange('gz_xxc_yi_chang_judges', page, amount)
    count = share_connect().llen('gz_xxc_yi_chang_judges')
    return d_list or [], count or 0


def get_match_player_count(match_id: int, hfs_type=1):
    name = 'JJS_PLAYER_COUNT' if hfs_type else 'DSS_PLAYER_COUNT'
    name = '{}_{}'.format(name, match_id)
    return int(share_connect().get(name) or 0)


def get_test_player_count():
    name = 'PLAYER_COUNT_TEST'
    return utils.to_dict(share_connect().get(name)) or []


def get_test_djj_player_count():
    name = 'PLAYER_COUNT_DJJ_TEST'
    return utils.to_dict(share_connect().get(name)) or []
