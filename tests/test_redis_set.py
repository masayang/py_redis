import unittest
from ..pydis import RedisSet
from mock import patch, call
from redis import StrictRedis

class TestRedisSet(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('redis.StrictRedis')
    def test_constructor_without_items(self, StrictRedis):
        s = RedisSet('test_set')
        self.assertEqual(s.id, 'RedisSet:test_set')

    @patch('redis.StrictRedis')
    def test_constructor_with_items(self, StrictRedis):
        s = RedisSet('test_set', ('a', 'b', 'c'))
        s.redis.sadd.assert_has_calls([
            call('RedisSet:test_set', 'a'),
            call('RedisSet:test_set', 'b'),
            call('RedisSet:test_set', 'c')
        ])

    @patch('redis.StrictRedis')
    def test_len(self, StrictRedis):
        StrictRedis().scard.return_value = 100
        s = RedisSet('test_set')
        self.assertEqual(len(s), 100)
        s.redis.scard.assert_called_with('RedisSet:test_set')

    @patch('redis.StrictRedis')
    def test_iter(self, StrictRedis):
        StrictRedis().smembers.return_value = set([1, 2, 3, 4])
        s = RedisSet('test_set')
        result = set([])
        for x in s:
            result.add(x)
        self.assertEqual(result, set([1, 2, 3, 4]))

    @patch('redis.StrictRedis')
    def test_remove(self, StrictRedis):
        s = RedisSet('test_set')
        s.remove(123)
        s.redis.srem.assert_called_with('RedisSet:test_set', 123)

    @patch('redis.StrictRedis')
    def test_ismember(self, StrictRedis):
        StrictRedis().sismember.return_value = True
        s = RedisSet('test_set')
        self.assertTrue(s.ismember(123))
        s.redis.sismember.assert_called_with('RedisSet:test_set', '123')

    @patch('redis.StrictRedis')
    def test_randmember(self, StrictRedis):
        StrictRedis().srandmember.return_value = set(['123', '456'])
        s = RedisSet('test_set')
        self.assertEquals(s.randmember(2), set(['123', '456']))
        s.redis.srandmember.assert_called_with('RedisSet:test_set', 2)

    @patch('redis.StrictRedis')
    def test_pop(self, StrictRedis):
        StrictRedis().spop.return_value = set(['123', '456'])
        s = RedisSet('test_set')
        self.assertEquals(s.pop(2), set(['123', '456']))
        s.redis.spop.assert_called_with('RedisSet:test_set', 2)

