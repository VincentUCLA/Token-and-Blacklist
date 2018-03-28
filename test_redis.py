from src.RedisTimer import RedisTimer
import unittest
import redis
import time

TOKEN_DB = redis.StrictRedis(host='localhost', port=6379, db=0)


class TestRedisTimer(unittest.TestCase):
    @staticmethod
    def get_time_diff(RT):
        return RT.dict_get("test_key")["absolute_limit"]\
               - RT.dict_get("test_key")["time_limit"]

    def test_generate_token(self):
        RT = RedisTimer(TOKEN_DB, "TestDB", 1, 5)
        RT.dict_generate("test_key", {})
        time_diff = self.get_time_diff(RT)
        self.assertEqual(time_diff, 4, "Token successfully generated with precise time limit!")
        time.sleep(1.5)
        self.assertEqual(RT.dict_get("test_key"), False, "Token properly expired!")
        return

    def test_extend_token(self):
        RT = RedisTimer(TOKEN_DB, "TestDB", 1, 5)
        RT.dict_generate("test_key", {})
        time_diff = self.get_time_diff(RT)
        self.assertEqual(time_diff, 4, "Token successfully generated with precise time limit!")
        time.sleep(0.5)
        RT.dict_extend("test_key")
        time.sleep(0.75)
        time_diff = self.get_time_diff(RT)
        self.assertTrue(time_diff < 3.5, "Token successfully extended!")
        time.sleep(0.75)
        self.assertEqual(RT.dict_get("test_key"), False, "Token properly expired!")
        return

    def test_absolute_limit(self):
        RT = RedisTimer(TOKEN_DB, "TestDB", 1, 5)
        RT.dict_generate("test_key", {})
        time_diff = self.get_time_diff(RT)
        self.assertEqual(time_diff, 4, "Token successfully generated with precise time limit!")
        time.sleep(0.9)
        RT.dict_extend("test_key")
        time_diff = self.get_time_diff(RT)
        self.assertTrue(time_diff < 3.1, "Token successfully extended!")
        time.sleep(0.9)
        RT.dict_extend("test_key")
        time_diff = self.get_time_diff(RT)
        self.assertTrue(time_diff < 2.2, "Token successfully extended!")
        time.sleep(0.9)
        RT.dict_extend("test_key")
        time_diff = self.get_time_diff(RT)
        self.assertTrue(time_diff < 1.3, "Token successfully extended!")
        time.sleep(0.9)
        RT.dict_extend("test_key")
        time_diff = self.get_time_diff(RT)
        self.assertTrue(time_diff < 0.4, "Token successfully extended!")
        time.sleep(0.9)
        RT.dict_extend("test_key")
        time_diff = self.get_time_diff(RT)
        self.assertEqual(time_diff, 0, "Token successfully extended!")
        time.sleep(0.25)
        time_diff = self.get_time_diff(RT)
        self.assertEqual(time_diff, 0, "Token successfully extended!")
        time.sleep(0.75)
        self.assertEqual(RT.dict_get("test_key"), False, "Token properly expired!")
        return


if __name__ == '__main__':
    unittest.main()
