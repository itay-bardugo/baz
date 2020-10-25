from unittest import TestCase
from redis import Redis


class TestRedis(TestCase):
    def test_it_connects(self):
        try:
            Redis(host="baz-redis")
        except Exception:
            self.fail()

    def test_it_writes(self):
        r = Redis(host="baz-redis")
        self.assertTrue(r.mset({"test": '1'}))

    def test_it_reads(self):
        r = Redis(host="baz-redis")
        self.assertEquals(r.mget("test")[0].decode("utf-8"), '1')

    def test_it_removes(self):
        r = Redis(host="baz-redis")
        self.assertTrue(r.delete("test"))
