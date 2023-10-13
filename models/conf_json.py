from models.base_orm import BaseORM, BaseRedis
from forum.utils import utils


class JsonConfig(BaseORM, BaseRedis):
    base_conf_db = "json_config"

    def __init__(self):
        BaseORM.__init__(self)
        BaseRedis.__init__(self)

    def get_config(self, conf_id: str, db_force=False):
        if db_force:
            return self.__from_db(conf_id)
        conf = self.get_hash_kv(self.base_conf_db, conf_id)
        return utils.to_dict(conf) if conf else self.__from_db(conf_id)

    def __from_db(self, conf_id: str):
        sql = "SELECT conf_data FROM {} WHERE conf_id='{}' LIMIT 1".format(self.base_conf_db, conf_id)
        cfg_row = self.query_one(sql)
        if cfg_row:
            conf = utils.to_dict(cfg_row.get('conf_data'))
            conf and self.save_hash_kv(self.base_conf_db, conf_id, conf)
            return conf
        return {}

    def update_conf(self, conf_id: str, conf: dict, is_sql=False):
        sql = "INSERT INTO {}(conf_id,conf_data,update_time) VALUES('{}','{}',{}) ON DUPLICATE KEY UPDATE " \
              "conf_data=VALUES(conf_data),update_time=VALUES(update_time)".format(
                self.base_conf_db, conf_id, utils.json_encode(conf, True), utils.timestamp())
        if is_sql:
            return sql
        return self.row_count_ex(sql)

    def update_reddot(self, uid: int, update_name: str, is_dec=False, count=1):
        home_reddot = self.get_hash_kv("home_reddot", uid)
        if home_reddot:
            home_reddot = utils.to_dict(home_reddot)
            update_data = home_reddot.get(update_name)
            if is_dec:
                update_data -= count
                home_reddot[update_name] = update_data
                return self.save_hash_kv("home_reddot", uid, home_reddot)
            update_data += count
            home_reddot[update_name] = update_data
            return self.save_hash_kv("home_reddot", uid, home_reddot)
        return 0
