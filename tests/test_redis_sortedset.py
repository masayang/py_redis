import unittest
from ..pydis import RedisSortedSet
from redis import StrictRedis
from mock import patch, call

class TestRedisSortedSet(unittest.TestCase):
    @patch('os.urandom')
    @patch('redis.StrictRedis')
    def setUp(self, StrictRedis, urandom):
        pass

    def tearDown(self):
        pass

    @patch('os.urandom')
    @patch('redis.StrictRedis')
    def test_constructor_empty(self, StrictRedis, urandom):
        urandom.return_value = '\xd8X\xfa@\x97\x90\x00dr'
        ss = RedisSortedSet()
        self.assertIsNotNone(ss)
        self.assertEqual(ss.id, u'RedisSortedSet:2Fj6QJeQAGRy')

    @patch('os.urandom')
    @patch('redis.StrictRedis')
    def test_constructor_with_items(self, StrictRedis, urandom):
        urandom.return_value = '\xd8X\xfa@\x97\x90\x00dr'
        ss = RedisSortedSet(init_items=[
            {'2017-01': 10},
            {'2017-02': 20},
            {'2017-03': 30}
        ])
        ss.redis.zadd.assert_has_calls([
            call(u'RedisSortedSet:2Fj6QJeQAGRy', 10, '2017-01'),
            call(u'RedisSortedSet:2Fj6QJeQAGRy', 20, '2017-02'),
            call(u'RedisSortedSet:2Fj6QJeQAGRy', 30, '2017-03')])

    @patch('redis.StrictRedis')
    def test_count(self, StrictRedis):
        StrictRedis().zcount.return_value = 1111
        ss = RedisSortedSet(id="test_ss")
        self.assertEquals(ss.count(10, 10000), 1111)
        ss.redis.zcount.assert_called_with('RedisSortedSet:test_ss', 10, 10000)

    @patch('redis.StrictRedis')
    def test_incrby(self, StrictRedis):
        StrictRedis().zincrby.return_value = 11
        ss = RedisSortedSet(id="test_ss", init_items=[{'key': 10}])
        self.assertEquals(ss.incrby('key', 1), 11)
        ss.redis.zincrby.assert_called_with('RedisSortedSet:test_ss', 'key', 1)

    @patch('redis.StrictRedis')
    def test_range(self, StrictRedis):
        StrictRedis().zrange.return_value = "some return value"
        ss = RedisSortedSet(id="test_ss", init_items=[{'key': 10}, {'another': 20}])
        self.assertEquals(ss.range(0, -1), "some return value")
        ss.redis.zrange.assert_called_with('RedisSortedSet:test_ss', 0, -1, False, withscores=True)

        self.assertEquals(ss.range(0, -1, desc=True), "some return value")
        ss.redis.zrange.assert_called_with('RedisSortedSet:test_ss', 0, -1, True, withscores=True)

    @patch('redis.StrictRedis')
    def test_revrange(self, StrictRedis):
        StrictRedis().zrevrange.return_value = "some return value"
        ss = RedisSortedSet(id="test_ss", init_items=[{'key': 10}, {'another': 20}])
        self.assertEquals(ss.revrange(0, -1), "some return value")
        ss.redis.zrevrange.assert_called_with('RedisSortedSet:test_ss', 0, -1, withscores=True)

    @patch('redis.StrictRedis')
    def test_rangebyscore(self, StrictRedis):
        StrictRedis().zrangebyscore.return_value = "some return value"
        ss = RedisSortedSet(id="test_ss", init_items=[{'key': 10}, {'another': 20}])
        self.assertEquals(ss.rangebyscore(0, -1), "some return value")
        ss.redis.zrangebyscore.assert_called_with('RedisSortedSet:test_ss', 0, -1, None, None, withscores=True)

    @patch('redis.StrictRedis')
    def test_rem(self, StrictRedis):
        StrictRedis().zrem.return_value = 2
        ss = RedisSortedSet(id="test_ss", init_items=[{'key': 10}, {'another': 20}])
        self.assertEquals(ss.rem('key', 'another'), 2)
        ss.redis.zrem.assert_called_with('RedisSortedSet:test_ss', 'key', 'another')

    @patch('redis.StrictRedis')
    def test_remrangebyrank(self, StrictRedis):
        StrictRedis().zremrangebyrank.return_value = 2
        ss = RedisSortedSet(id="test_ss", init_items=[{'key': 10}, {'another': 20}])
        self.assertEquals(ss.remrangebyrank(0, 1), 2)
        ss.redis.zremrangebyrank.assert_called_with('RedisSortedSet:test_ss', 0, 1)

    @patch('redis.StrictRedis')
    def test_remrangebyscore(self, StrictRedis):
        StrictRedis().zremrangebyscore.return_value = 2
        ss = RedisSortedSet(id="test_ss", init_items=[{'key': 10}, {'another': 20}])
        self.assertEquals(ss.remrangebyscore(10, 20), 2)
        ss.redis.zremrangebyscore.assert_called_with('RedisSortedSet:test_ss', 10, 20)

    @patch('redis.StrictRedis')
    def test_revrangebyscore(self, StrictRedis):
        StrictRedis().zrevrangebyscore.return_value = "some return value"
        ss = RedisSortedSet(id="test_ss", init_items=[{'key': 10}, {'another': 20}])
        self.assertEquals(ss.revrangebyscore(0, 1000), "some return value")
        ss.redis.zrevrangebyscore.assert_called_with('RedisSortedSet:test_ss', 0, 1000, withscores=True)

    @patch('redis.StrictRedis')
    def test_rank(self, StrictRedis):
        StrictRedis().zrank.return_value = 1
        ss = RedisSortedSet(id="test_ss", init_items=[{'key': 10}, {'another': 20}])
        self.assertEquals(ss.rank('another'), 1)
        ss.redis.zrank.assert_called_with('RedisSortedSet:test_ss', 'another')

    @patch('redis.StrictRedis')
    def test_revrank(self, StrictRedis):
        StrictRedis().zrevrank.return_value = 1
        ss = RedisSortedSet(id="test_ss", init_items=[{'key': 10}, {'another': 20}])
        self.assertEquals(ss.revrank('another'), 1)
        ss.redis.zrevrank.assert_called_with('RedisSortedSet:test_ss', 'another')

    @patch('redis.StrictRedis')
    def test_score(self, StrictRedis):
        StrictRedis().zscore.return_value = 10
        ss = RedisSortedSet(id="test_ss", init_items=[{'key': 10}, {'another': 20}])
        self.assertEquals(ss.score('key'), 10)
        ss.redis.zscore.assert_called_with('RedisSortedSet:test_ss', 'key')

