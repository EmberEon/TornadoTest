from enum import Enum, unique, IntEnum
from types import DynamicClassAttribute


class BaseEnum(Enum):
    """继承自该类的枚举设置的模型必须为： name = (value/值, desc/描述或说明) 否则报错"""

    @DynamicClassAttribute
    def val(self):
        """值"""
        return self.value[0]

    @DynamicClassAttribute
    def desc(self):
        """描述"""
        return self.value[1]

    @DynamicClassAttribute
    def data(self):
        """数据(第三项 可选)"""
        if len(self.value) > 3:
            return self.value[2]
        return None

    @classmethod
    def query_name(cls, name):
        return name in cls._member_names_

    @classmethod
    def query_value(cls, value):
        for v in cls._value2member_map_.values():
            if v.val == value:
                return True
        return False

    @classmethod
    def get_desc(cls, value):
        for v in cls._value2member_map_.values():
            if v.val == value:
                return v.desc
        return ""

    @classmethod
    def all_type(cls):
        all_list = []
        for v in cls._value2member_map_.values():
            all_list.append({'value': v.val, "label": v.desc})
        return all_list


class WSChannel:
    """Websocket -- Redis 信道定义"""
    SYSTEM_COMMON = "SYSTEM_COMMON"
    '''全局系统消息'''
    GATEWAY_HALL = "GATEWAY_HALL"
    '''大厅网关'''
    GATEWAY_CHILD = "GATEWAY_CHILD"
    '''子游戏网关'''
    ROOM_HALL = "ROOM_HALL"
    '''大厅房间'''
    ROOM_CHILD = "ROOM_CHILD"
    '''子游戏房间'''

    MSG_TO_USER = "MSG_TO_USER"
    '''通知玩家 直接下发到网关'''
    MSG_TO_CHILD_GAME = "MSG_TO_CHILD_GAME"
    '''通知子游戏'''
    MSG_TO_CLUB = "MSG_TO_CLUB"
    '''通知酒馆'''
    MSG_TO_CBS_MATCH = "MSG_TO_CBS_MATCH"
    '''通知冲榜赛'''
    RED_DOT_DDZ = "RED_DOT_MSG_DDZ"
    '''斗地主红点消息服务'''
    XXC_COMPUTER = "COMPUTER_XXC"


class GoodsItem:
    DIAMOND = 2001
    '''钻石'''
    GOLD = 2002
    '''金币'''
    COUPON = 2003
    '''点券'''
    EXP_POINT = 2004
    '''经验值'''
    VIP_EXP_POINT = 2005
    '''VIP经验值'''
    CHIPS_ROLE = 2006
    '''角色碎片'''
    CHIPS_SKIN = 2007
    '''皮肤碎片'''
    FRIEND_LETTER = 2010
    '''好友书信'''
    RAINING = 2008
    '''雨滴'''
    SUNSHINE = 2009
    '''阳光'''
    NAME_CARD = 2011
    '''改名卡'''
    Double_GOlD_CARD = 2012
    '''双倍金币卡'''
    RANK_PROJECT_CARD = 2013
    '''排位保护卡'''
    INFINITE_ENJOY = 2084
    '''无限畅玩卡'''
    ZHAN_LING_EXP = 2092
    '''战令经验'''
    PU_TONG_ZHAN_LING_TICKET = 2117
    '''普通战令'''


class RpsCode(BaseEnum):
    OK = 1, "请求成功"
    RQ_FAIL = -1, "请求失败"
    SIGN_FAIL = -2, "签名错误"
    DATA_BROKEN = -3, "参数错误"
    SYSTEM_ERR = -4, "系统错误"
    ASSET_FAIL = -5, "资产不足"
    UID_ERROR = -6, "用户不存在"


class MsgType(BaseEnum):
    """消息类型"""
    UP_LEVEL = 1, '等级提升奖励'
    ORDER_STATUS = 2, '订单状态更新'
    PUB_NOTICE = 3, '发布公告'
    NOTICE_OFFLINE = 4, '通知下线'
    FRIEND_SEND = 5, '好友消息发送'
    FRIEND_RECEIVE = 6, '好友消息接收'
    RED_DOT = 7, '红点消息'
    IN_MATCH = 8, '比赛场信息'
    IN_XXC = 9, '休闲场信息'
    USER_UPDATE = 10, '玩家资产 等级更新'
    PO_CHAN = 11, '破产通知'
    MAILS = 12, '邮件'
    FRIEND_MESSAGE = 13, '好友红点'
    FRIEND_SEND_MESSAGE = 14, '好友列表红点'
    RED_DOT_HOME = 15, '新红点消息（大厅）'
    IS_NEXT_NOTICE = 16, '定时任务跨天通知'


class DotType(BaseEnum):
    LOGIN = 1, "登录下发"
    MAILS = 2, "邮件"
    FRIEND_APPLY = 3, "好友申请"
    LOTTERY = 4, "抽奖"
    SIGN_INFO = 5, "签到"
    AVATAR_BOX = 6, "头像框装扮"
    BUB_BOX = 7, "聊天气泡装扮"
    CHENG_HAO = 8, "称号"
    YU_YIN = 9, "语音包"
    ACTIVITY = 10, "首充活动"
    FU_LI = 11, "福利活动"
    FRIEND_MSG = 12, "好友消息"
    AD_GOT_VIP = 13, "看广告获得VIP经验"
    RELOAD_RED_DOT = 14, "刷新红点"


class HomeDotType(BaseEnum):
    FRIEND = 1, "好友红点"
    MAIl = 2, "邮件红点"
    FIRST_CHARGE = 3, "首充"
    LOTTERY = 4, "盲盒"
    SIGN_IN = 5, "签到"
    DRESS_UP = 6, "装扮"
    FARM = 7, "农场"
    SHOP_FREE = 8, "商店"
    RENEW = 9, "续费"
    BLESS = 10, "免费祈福"


class GameClass(BaseEnum):
    """游戏大类型"""
    ALL = 0, "全部"
    SHUI_YU = 1, "水鱼"
    GONG_ZHU = 2, "拱猪"
    MAHJONG = 3, "麻将"
    DDZ = 4, "斗地主"


class SMSCodeType(BaseEnum):
    """验证码类型"""

    BIND_TEL = 0, '绑定手机号'
    ACCOUNT = 1, '账户、资金相关操作'
    Q_FEEDBACK = 2, '问题反馈'
    LOGIN = 3, '登录'
    CERTIFICATION = 4, '实名认证'
    UN_BIND_PHONE = 5, '解绑手机号'
    POST_CROP = 6, '邮寄登记'


class GoodsType(BaseEnum):
    """物品类型"""

    V_ASSET = 1, '虚拟资产'
    HUA_FEI = 2, '话费兑换券'
    # TX_VIP = 3, '腾讯视频vip券'
    SHI_WU = 4, '实物类'
    TICKET = 5, '门票类'
    FRAME = 6, '头像框'
    BUB = 7, '聊天气泡'
    YU_YIN = 8, "语音包类"
    PACKAGE = 9, '礼盒类'
    JPQ_SKIN = 10, '记牌器闹钟类类'
    PROP = 11, '道具类'
    SAFE_BOX = 12, '保险箱类'
    ROLE = 13, '角色(英雄)',
    ROLE_SKIN = 14, '角色(英雄)皮肤'
    LIMIT_ROLE = 15, '角色体验卡',
    MANOR_PROP = 16, '庄园道具'
    CROP = 17, '收成后的农产品'
    LIMIT_SKIN = 18, '皮肤体验卡',
    ACTIVITY = 19, '活动类'


class Reason(BaseEnum):
    """资产或物品增减reason 必须与Websocket保持一致"""
    SIGN_IN = 1, "签到奖励"
    MAIL_AWARDS = 2, "统一邮件奖励"
    GOT_BY_SHOP = 3, "商城交易获得"
    GOT_BY_RECHARGE = 4, "充值获得"
    LOTTERY_GOT = 5, "抽奖获得"
    ACTIVATION_DAILY = 6, "日活跃度奖励"
    ACTIVATION_WEEK = 7, "周活跃度奖励"
    TASK_AWARD = 8, "任务奖励"
    VIP_LEVEL = 9, "VIP等级特权奖励"
    VIP_DAILY = 10, "VIP每日特权奖励"
    VIP_AWARDS = 11, "VIP特权奖励"
    SYSTEM_SEND = 12, "系统赠送"
    FRIEND_SEND = 13, "玩家赠送获得"
    FIRST_CHARGE = 14, "首充奖励"
    DDZ_XXC_WIN = 15, "斗地主休闲场获胜获得"
    GOT_PO_CHAN = 16, "领取破产奖励"
    CERTIFICATION = 17, "实名认证奖励"
    DAILY_ADS = 18, "每日免费看广告奖励"
    ONLINE_TINE = 19, "在线时长奖励"
    CANCEL_PLANT = 20, "农场取消预约种植"
    XU_FEI = 21, "续费奖励"
    CROP_EXCHANGE = 22, "农作物兑换获得"
    LIMIT_CARD_TURN = 23, "体验卡兑换"
    FARM_LEVEL_UP = 24, "农场升级奖励"
    PWS_LEVEL = 25, "排位赛赛季结算段位奖励"
    BIND_PHONE = 26, "绑定手机"
    EXCHANGE_BOX = 27, "宝箱抽奖"
    FINISH_FARM_TASK = 28, "完成农场订单任务"
    FREE_GIFT = 29, "免费礼包"
    SALE_EXPERIENCE_CARD = 30, "出售体验卡"
    MESH_FARM_CROPS = 31, "合并作物"
    BANKRUPT_TO_GAME = 32, "购买金币进入场次"
    GAME_RETURN_GOLD = 33, "购买输掉的金币"
    FARM_COIN_EXCHANGE = 34, "农场币兑换"
    # 与server冲突加30
    PIGGY_BANK_DRAW = 65, "存钱罐取钱"
    SALE_FARM_ROLE_CHIPS = 66, "出售农场角色皮肤碎片"
    INFINITE_ENJOY = 67, "无限畅玩"
    PRIVILEGES = 68, "特权卡一次领取"
    PRIVILEGES_DAY = 69, "特权卡每日领取"
    WAR_ORDER = 70, "战令奖励"
    LIVE_WELFARE_CODE = 71, "直播福利码奖励"
    TEA_AWARDS = 72, "茶叶活动奖励"

    EXPIRED_REMOVE = -1, "过期移除"
    BUY_YU_YIN = -2, "购买语音包"
    COST_IN_SHOP = -3, "商城购买消耗"
    SEND_LETTER = -4, "发送好友信件消耗"
    LOTTERY_COST = -5, "抽奖消耗"
    BY_ROLE_SKIN = -7, "商城购买角色或皮肤"
    FARM_BUY_SEED = -8, "农场购买种子消耗"
    FARM_SUNSHINE = -9, "农场光照消耗"
    MODIFY_NAME = -10, "修改昵称消耗"
    USE_LIMIT_CARD = -11, "使用体验卡"
    FARM_FREE_BACK = -12, "农场种植空闲土地回收"
    SEND_FRIEND = -13, "交易赠送给玩家的礼物"
    DDZ_XXC_BAO_MING = -14, "斗地主休闲场报名消耗"
    DDZ_XXC_LOSE = -15, "斗地主休闲场输消耗"
    DOUBLE_GOLD = -16, "使用双倍金币卡"
    RANK_PROJECT = -17, "使用排位保护卡"
    CHIPS_EXCHANGE = -18, "碎片兑换"
    EXCHANGE_BOX_COST = -19, "宝箱抽奖"
    BANKRUPT_BUY_TO_GAME = -20, "购买金币进入场次"
    GAME_BUY_RETURN_GOLD = -21, "购买输掉的金币"
    PIGGY_BANK_DEPOSIT = -22, "存钱罐存钱"
    START_PIGGY_BANK = -23, "开启存钱罐"
    BUY_BARRIER_TICKET = -24, "购买闯关赛门票"
    USE_PROP = -25,    "使用类消耗"

    MAKE_PLANT = -20, "农场预约种植扣除"


class MailOpType(BaseEnum):
    """
    邮件操作类型
    """
    READ = 1, '标记已读'
    GOT = 2, '领取奖励'
    DEL = 3, '删除'
    AGREE = 4, '同意'
    REFUSE = 5, '拒绝'


class MailOpSta(BaseEnum):
    """邮件领奖状态"""
    NONE = 0, '无状态'
    NO_GOT = 1, '未领奖'
    GOT = 2, '已领奖'
    WAITING = 3, '等待操作'
    AGREE = 4, '同意'
    REFUSE = 5, '拒绝'


class MailSta(BaseEnum):
    """邮件状态"""
    DELETED = 0, '已删除'
    UNREAD = 1, '未读'
    READ = 2, '已读 邮件包含奖励时，已读状态标记为领奖或未领奖状态'


class LandStatus(BaseEnum):
    """合成农场土地状态"""
    LOCK = 0, '未解锁'
    NO_SEED = 1, '解锁未种植'
    SEED = 2, '种植中'


class MailType(BaseEnum):
    """邮件类型"""
    SYS = 1, '系统邮件'
    LETTER = 2, '好友书信邮件'
    GIFT_SEND = 3, '礼物赠送邮件'
    GIFT_ASK = 4, '礼物索取邮件'


class MatchType(BaseEnum):
    HFS = 1, "话费赛"
    SWS = 2, "实物赛"
    JBS = 3, "锦标赛"
    CBS = 4, "冲榜赛"
    TTS = 5, "淘汰赛"
    CGS = 6, "闯关赛"


class ChargeMode(BaseEnum):
    WX_JSAPI = 1, "微信网页支付"
    ZHI_FU_BAO = 2, "支付宝网页支付"
    IAP = 3, "苹果支付"
    ZHI_FU_BAO_APP = 4, "原生支付宝APP支付"
    SD_WX_API = 5, "微信APP支付杉德支付"
    HUI_FU_WX_API = 6, "微信APP支付汇付支付"
    VIVO = 7, "vivo支付"
    OPPO = 8, "oppo支付"
    HUA_WEI = 9, "华为支付"
    YYB = 10, "应用宝支付"
    BILIBILI = 11, "b站支付"
    KUAISHOU =12, "快手支付"


class ChargeType(BaseEnum):
    SHOP = 1, '商城充值'
    SEND_GIFT = 2, '赠送礼物充值'
    ASK_GIFT = 3, '同意索取礼物充值'
    RUSH_LIMIT = 4, '限量抢购充值'
    BANKRUPT = 5, "破产超值充值"
    DAILY_SHOP = 6, "每日特惠充值"
    INFINITE_ENJOY = 7, "无限畅玩"
    REVENGE = 8, "大圣归来复仇"
    PRIVILEGES = 9, "特权卡"
    WAR_ORDER = 10, "战令"


class PutArea(BaseEnum):
    ASSET = 0, '玩家资产'
    BAG_C = 1, '放入仓库背包区'
    BAG_T = 2, '放入仓库时效区'
    PERSONAL = 3, '个人中心面板'


class AddType(BaseEnum):
    COUNT = 0, '按数量累加'
    TIME_LIMIT = 1, '按时效累加'


class PiggyBankOpt(BaseEnum):
    """存钱罐操作"""
    DEPOSIT = 0, '存钱'
    DRAW = 1, '取钱'


class CZOrderSta(BaseEnum):
    """充值订单的状态"""
    PAID = 0, '已支付'
    WAIT_PAY = 1, '等待支付'
    CANCEL = 2, '取消'
    EX_TIME = 3, '已过期'


class PayType(BaseEnum):
    """
    支付类型
    """
    RMB = 1, "充值"
    DIAMOND = 2, '钻石兑换'
    GOLD = 3, '金币兑换'
    COUPON = 4, '点券兑换'
    CHIPS_ROLE = 5, '角色碎片兑换'
    CHIPS_SKIN = 6, '皮肤碎片兑换'
    RANDOM_BOX_TICKET = 7, '宝箱券'


class BuyLimitType(BaseEnum):
    """
    限购类型
    """
    NONE = 1, "不限购"
    DAILY = 2, "每日限购"
    WEEKLY = 3, "每周限购"
    MONTH = 4, "每月限购"
    YEAR = 5, "每年限购"


class PowerType(BaseEnum):
    """
    图片查看权限
    """
    MINE = 1, "自己可见"
    FRIEND = 2, "好友可见"
    ALL = 3, "所有人可见"


class ImgStatus(BaseEnum):
    """图片状态"""
    FAILED = 0, "审核失败"
    CHECKING = 1, "审核中"
    PASS = 2, "审核通过"


class ManageType(BaseEnum):
    """
    图片管理类型
    """
    DELETE = 1, '删除'
    MODIFY = 2, "修改权限"


class MsgStatus(BaseEnum):
    """消息状态"""
    DELETED = 0, '已删除'
    UNREAD = 1, '未读'
    READ = 2, '已读'


class BadnessType(BaseEnum):
    """举报选项类型"""
    ZUO_BI = 1, "合伙作弊"
    SAO_RAO = 2, "骚然信息"
    PERSONAL = 3, "个人信息违规"
    XIAO_JI = 4, "消极对局"


class CheckSta(BaseEnum):
    """审核状态"""
    MANUAL = -1, "需要人工审核"
    BLOCK = 0, "审核不通过"
    WAITING = 1, "等待审核"
    PASS = 2, "审核通过"


class GiftSta(BaseEnum):
    """礼物状态"""
    DELETED = 0, '已删除'
    WAIT_RECEIVE = 1, '等待领取'
    RECEIVED = 2, '已领取'
    WAIT_SEND = 3, '等待赠送'
    SEND = 4, '已赠送'
    REFUSE = 5, '已拒绝'
    CANCEL = 6, '已取消'


class AdsMarkType(BaseEnum):
    """看广告订单类型"""
    BU_QIAN = 1, "看广告补签"
    GOT_LOTTERY = 2, "看广告获取免费抽奖次数"
    DAILY_AWARD = 3, "每日看广告获得奖励"
    DAILY_JIU_JI = 4, "每日救济"
    FARM_SEED = 5, "看广告领农场种子"
    FARM_COIN = 6, "看广告领农场币"


class GotWay(BaseEnum):
    CREATE = 0, '通过创建角色默认选取'
    BUY = 1, '通过购买获取'
    BUY_LIMIT = 2, '通过限量抢购活动获取'
    ACT_PWS = 3, '通过排位赛任务获取'
    ACT_OTHERS = 4, '通过其他奖励活动获取'
    SEVEN_DAY_GIFT = 5, '七天大礼包'
    FIRST_CHARGE = 6, '首充'
    FARM_EXCHANGE = 7, '农场兑换'


class CropGotWay(BaseEnum):
    """农产品获取方式"""
    EXCHANGE = 1, "兑换钻石"
    POST = 2, "邮寄"
    DONATE = 3, "捐献"


class PlatformValue(BaseEnum):
    """平台渠道"""
    IOS = 1, "苹果"
    ANDROID = 2, "安卓"
    VIVO = 3, "vivo"
    HUA_WEI = 4, "华为"
    OPPO = 5, "oppo"
    BILIBILI = 6, "b站"
    YYB = 7, "应用宝"


class ImgType:
    head_img = 1
    sign_in_img = 2
    goods_item = 3
    store_img = 4
    store_item = 5
    match_type_item = 6
    lottery_img = 7
    load_conf = 8
    crops_img = 9
    public_goods = 10


class UploadCfg:
    folder = "folder"
    img_width = "img_width"
    img_height = "img_height"
    size = "size"


class FarmShopOptType(BaseEnum):
    """农场商店购买类型"""
    FREE = 1, "免费领取"
    GOLD = 2, "金币购买"
    DIAMOND = 3, "钻石购买"
    ADVERT = 4, "看广告领取"
    COUPON = 5, "点券购买"


UPLOAD_CONF = {
    ImgType.head_img: {
        'folder': "head_icon",
        'img_width': 200,
        'img_height': 200,
        'size': 500.0
    },
    ImgType.sign_in_img: {
        'folder': "sign_in",
        'img_width': 74,
        'img_height': 74,
        'size': 60.0
    },
    ImgType.goods_item: {
        'folder': "ddz_goods_item",
        'img_width': 120,
        'img_height': 120,
        'size': 200.0
    },
    ImgType.store_img: {
        'folder': "store_img",
        'img_width': 100,
        'img_height': 100,
        'size': 100.0
    },
    ImgType.store_item: {
        'folder': "store_item",
        'img_width': 74,
        'img_height': 74,
        'size': 60.0
    },
    ImgType.match_type_item: {
        'folder': "match_type_img",
        'img_width': 550,
        'img_height': 160,
        'size': 150
    },
    ImgType.lottery_img: {
        'folder': "lottery_img",
        'img_width': 120,
        'img_height': 120,
        'size': 80
    },
    ImgType.load_conf: {
        'folder': "launch_config",
        'img_width': 1980,
        'img_height': 1080,
        'size': 500
    },
    ImgType.crops_img: {
        'folder': "crops_img",
        'img_width': 120,
        'img_height': 120,
        'size': 200
    },
    ImgType.public_goods: {
        'folder': "ddz_public_goods_img",
        'img_width': 120,
        'img_height': 120,
        'size': 200
    }
}


@unique
class ActivityType(IntEnum):
    QUE_SHEN_ZHAN_LING = 1007  # 雀神战令
    PU_TONG_ZHAN_LING = 1006  # 普通战令


@unique
class TaskType(IntEnum):
    """ 任务类型(根据周期性) """
    DAILY_TASK = 1  # 每日任务
    FRESH_TASK = 6  # 新手任务
    ZHAN_LING_TASK = 7  # 普通战令任务
    ZHAN_LING_TZ_TASK = 8  # 战令挑战任务


@unique
class TaskChildType(IntEnum):
    """ 任务类型(根据游戏性质) """
    TASK_TYPE_WIN = 1  # 赢几局
    TASK_TYPE_JOIN = 2  # 加入游戏玩几局
    TASK_TYPE_WIN_GOLD = 3  # 赢金币
    TASK_TYPE_FAN_YING = 4  # 反赢
    TASK_TYPE_TONG_SHA = 5  # 通杀
    TASK_TYPE_SHUI_YU = 6  # 拿水鱼
    TASK_TYPE_FEN_XIANG = 7  # 分享APP
    TASK_TYPE_JOIN_MATCH = 8  # 加入比赛
    TASK_TYPE_LOGIN_PER_DAY = 9  # 每天登录
    TASK_TYPE_CHONG_ZHI_DIAN_QUAN = 10  # 充值点券
    TASK_TYPE_USE_DIAMOND = 11  # 使用钻石
    TASK_TYPE_USE_DIAN_QUAN = 12  # 使用点券
    TASK_TYPE_MJ_JIAN = 13  # 麻将捡
    TASK_TYPE_MJ_MI = 14  # 麻将密
    TASK_TYPE_MJ_HU_10_BEI = 15  # 麻将胡牌10倍以上
    TASK_TYPE_CONTINUOUS_SIGN = 16  # 连续签到
    TASK_TYPE_HU_KAI = 17  # 成功胡开
    TASK_TYPE_PING_HU = 18  # 达成平胡以外牌型
    TASK_TYPE_MEN_HU = 19  # 闷胡
    TASK_TYPE_JIAN_HU = 20  # 捡胡
