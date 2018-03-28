from src.common import *


class RedisTimer:
    def __init__(self, redis_db, db_name, idle_time, life_time):
        """
        Generates the object by parameters.

        :param redis_db: The Redis DB
        :param db_name: The DB name in Redis
        :param idle_time: idle time permitted
        :param life_time: the absolute expiration time
        :return: Nothing
        """
        self.redis_db = redis_db
        self.db_name = db_name
        self.idle_time = idle_time
        self.life_time = life_time

    def dict_generate(self, key, value):
        """
        Save a certain key-value pair to a table of Redis DB

        :param key: key
        :param value: value
        :return: True unless Redis error
        """
        now = get_timestamp()
        value["time_limit"] = now + self.idle_time
        value["absolute_limit"] = now + self.life_time
        r = self.redis_db.hset(self.db_name, key, value)
        s = self.redis_db.save()
        return True

    def dict_extend(self, key, idle_time=None):
        """
        Extend a certain key's time period.

        :param key: key
        :param idle_time: idle_time
        :return: If the key is expired, return False, otherwise return the new value
        """
        temp_json = self.dict_get(key)
        if not temp_json:
            return False

        now = get_timestamp()
        if idle_time:
            new_time_limit = min(now + idle_time, temp_json["absolute_limit"])
        else:
            new_time_limit = min(now + self.idle_time, temp_json["absolute_limit"])
        temp_json["time_limit"] = new_time_limit
        self.redis_db.hset(self.db_name, key, temp_json)
        return temp_json

    def dict_remove(self, key):
        """
        Remove a key from table.

        :param key: key
        :return: A boolean, whether a token's time limited is extended.
        """
        self.redis_db.hdel(self.db_name, key)

    def dict_get(self, key):
        """
        Get a key from table.

        :param key: key
        :return: If the key is expired, return False, otherwise return the new value
        """
        current_token = self.redis_db.hget(self.db_name, key)
        if not current_token:
            return False
        
        # If it exceeds absolute_limit, remove the token from the DB
        now = get_timestamp()
        temp_json = byte2json(current_token)
        if now > temp_json["absolute_limit"] or now > temp_json["time_limit"]:
            self.dict_remove(key)
            return False
        return temp_json

    def dict_modify(self, key, value):
        """
        Save a certain key-value pair to a table of Redis DB

        :param key: key
        :param value: value
        :return: True unless Redis error
        """
        self.redis_db.hset(self.db_name, key, value)
        return True
