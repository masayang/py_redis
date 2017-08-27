import unittest
from ..pydis import RedisList, RedisObject
from mock import patch, call
from redis import StrictRedis


class TestRedisList(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_constructor_without_items(self):
        with patch.object(RedisObject, '__init__') as init:
            l = RedisList(id="xxx")
            init.assert_called_with('xxx')
            self.assertEqual(l.item_type, str)

    def test_constructor_with_items(self):
        with patch.object(RedisObject, '__init__') as init:
            with patch.object(RedisList, 'append') as m_append:
                l = RedisList(id="xxx", items=[1, 2, 3])
                init.assert_called_with('xxx')
                self.assertEqual(l.item_type, str)
                m_append.assert_has_calls([call(1), call(2), call(3)])

    @patch('redis.StrictRedis')
    def test_getitem_no_slice(self, StrictRedis):
        StrictRedis().lindex.return_value = '1'
        with patch.object(RedisList, 'append') as m_append:
            l = RedisList(id="list", items=[1, 2, 3])
            self.assertEquals(l[0], '1')
            l.redis.lindex.assert_called_with('RedisList:list', 0)

    @patch('redis.StrictRedis')
    def test_getitem_with_slice_no_step(self, StrictRedis):
        StrictRedis().lrange.return_value = ['1', '2']
        with patch.object(RedisList, 'append') as m_append:
            l = RedisList(id="list", items=[1, 2, 3])
            self.assertEquals(l[0:1], ['1', '2'])
            l.redis.lrange.assert_called_with('RedisList:list', 0, 1)

    @patch('redis.StrictRedis')
    def test_getitem_with_slice_with_step_1(self, StrictRedis):
        StrictRedis().lrange.return_value = ['1', '2']
        with patch.object(RedisList, 'append') as m_append:
            l = RedisList(id="list", items=[1, 2, 3])
            self.assertEquals(l[0:1:1], ['1', '2'])
            l.redis.lrange.assert_called_with('RedisList:list', 0, 1)

    @patch('redis.StrictRedis')
    def test_getitem_with_slice_with_step_2(self, StrictRedis):
        StrictRedis().lrange.return_value = ['1', '2']
        with patch.object(RedisList, 'append') as m_append:
            l = RedisList(id="list", items=[1, 2, 3])
            with self.assertRaises(NotImplementedError) as context:
                l[0:1:2]
                self.assertTrue('Cannot specify a step to a RedisObject slice'  in context.exception)

    @patch('redis.StrictRedis')
    def test_setitem(self, StrictRedis):
        l = RedisList(id="list")
        l[0] = "hogehoge"
        l.redis.lset.assert_called_with('RedisList:list', 0, 'hogehoge')

    @patch('redis.StrictRedis')
    def test_len(self, StrictRedis):
        StrictRedis().llen.return_value = 100
        l = RedisList(id="list")
        self.assertEqual(100, len(l))
        l.redis.llen.assert_called_with('RedisList:list')

    @patch('redis.StrictRedis')
    def test_delitem(self, StrictRedis):
        l = RedisList('list')
        del l[2]
        l.redis.lset.assert_called_with('RedisList:list', 2, '__DELETED__')
        l.redis.lrem.assert_called_with('RedisList:list', 1, '__DELETED__')

    @patch('redis.StrictRedis')
    def test_lpop(self, StrictRedis):
        StrictRedis().lpop.return_value = '1'
        l = RedisList('list')
        self.assertEqual('1', l.lpop())
        l.redis.lpop.assert_called_with('RedisList:list')

    @patch('redis.StrictRedis')
    def test_rpop(self, StrictRedis):
        StrictRedis().rpop.return_value = '1'
        l = RedisList('list')
        self.assertEqual('1', l.rpop())
        l.redis.rpop.assert_called_with('RedisList:list')

    @patch('redis.StrictRedis')
    def test_rpush(self, StrictRedis):
        l = RedisList('list')
        l.rpush(1)
        l.redis.rpush.assert_called_with('RedisList:list', '1')

    @patch('redis.StrictRedis')
    def test_lpush(self, StrictRedis):
        l = RedisList('list')
        l.lpush(1)
        l.redis.lpush.assert_called_with('RedisList:list', '1')

    @patch('redis.StrictRedis')
    def test_append(self, StrictRedis):
        l = RedisList('list')
        l.append(1)
        l.redis.rpush.assert_called_with('RedisList:list', '1')

