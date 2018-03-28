import redis, unittest, time
from src.IP_blacklist import IP_blacklist
TOKEN_DB = redis.StrictRedis(host='localhost', port=6379, db=0)


class TestREST(unittest.TestCase):
    def test_IP(self):
        ip1 = "1.1.1.14"
        ip2 = "1.1.1.15"
        I = IP_blacklist(TOKEN_DB, 5, 4, 1)
        for i in range(0, 10):
            I.violate(ip1)
            time.sleep(1)
            self.assertTrue(I.check_ip_validity(ip1))
        for i in range(0, 20):
            I.violate(ip2)
            time.sleep(0.5)
            if i <= 3:
                self.assertTrue(I.check_ip_validity(ip2))
            elif i <= 11 and (i % 2 == 1):
                self.assertTrue(I.check_ip_validity(ip2))
            elif i > 11 and (i % 2 == 0):
                self.assertTrue(I.check_ip_validity(ip2))
            else:
                self.assertFalse(I.check_ip_validity(ip2))


if __name__ == '__main__':
    unittest.main()
