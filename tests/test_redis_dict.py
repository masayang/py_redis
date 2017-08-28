import unittest
from ..pydis import RedisDict
from mock import patch

class TestRedisDict(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('redis.StrictRedis')
    def test_constructor_empty(self, StrictRedis):
        d = RedisDict(id='test_dict')
        self.assertEquals(d.id, 'RedisDict:test_dict')
        self.assertEquals(d.fields, {})

    @patch('redis.StrictRedis')
    def test_constructor_with_fields(self, StrictRedis):
        d = RedisDict(id='test_dict', fields={
            'int_val': int,
            'str_val': str
        })
        self.assertEquals(d.id, 'RedisDict:test_dict')
        self.assertEquals(d.fields, {
            'int_val': int,
            'str_val': str
        })

    @patch('redis.StrictRedis')
    def test_constructor_with_fields_and_defaults(self, StrictRedis):
        StrictRedis().hget.return_value = 'this is a value from mock'
        d = RedisDict(id='test_dict', fields={
            'str_val': str
        }, defaults={
            'str_val': 'string'
        })
        self.assertEquals(d.id, 'RedisDict:test_dict')
        self.assertEquals(d.fields, {
            'str_val': str
        })

        self.assertEqual(d['str_val'], 'this is a value from mock')
        d.redis.hset.assert_called_with('RedisDict:test_dict', 'str_val', 'string')
        d.redis.hget.assert_called_with('RedisDict:test_dict', 'str_val')

    @patch('redis.StrictRedis')
    def test_len(self, StrictRedis):
        StrictRedis().hlen.return_value = 3
        d = RedisDict(id='test_dict', fields={
            'int_val': int,
            'str_val': str,
            'another': str
        })
        self.assertEquals(len(d), 3)
        d.redis.hlen.assert_called_with('RedisDict:test_dict')

    @patch('redis.StrictRedis')
    def test_get_id(self, StrictRedis):
        d = RedisDict(id='test_dict')
        self.assertEqual(d['id'], 'test_dict')

    @patch('redis.StrictRedis')
    def test_get_invalid_key(self, StrictRedis):
        d = RedisDict(id='test_dict')
        with self.assertRaises(KeyError) as context:
            d['something']
            self.assertTrue( 'something not found in RedisDict:test_dict' in context.exception)

    @patch('redis.StrictRedis')
    def test_set_invalid_key(self, StrictRedis):
        d = RedisDict(id='test_dict')
        with self.assertRaises(KeyError) as context:
            d['something'] = 'hoge'
            self.assertTrue( 'something not found in RedisDict:test_dict' in context.exception)

    @patch('redis.StrictRedis')
    def test_iterator(self, StrictRedis):
        StrictRedis().hget.return_value = 'string'
        d = RedisDict(id='test_dict', fields={
            'key1': str,
            'key2': str
        })
        d['key1'] = 'string'
        d['key2'] = 'string'

        results = []
        for kv in d:
            results.append(kv)
        self.assertEquals(results, [
            ('id', 'test_dict'),
            ('key2', 'string'),
            ('key1', 'string')
        ])

    @patch('redis.StrictRedis')
    def test_delitem(self, StrictRedis):
        d = RedisDict(id='test_dict', fields={
            'key1': str,
            'key2': str
        })
        d['key1'] = 'string'
        d['key2'] = 'string'

        del d['key1']
        d.redis.hdel.assert_called_with('RedisDict:test_dict', 'key1')

    @patch('redis.StrictRedis')
    def test_incrby(self, StrictRedis):
        d = RedisDict(id='test_dict', fields={
            'key1': int
        })
        d['key1'] = 1
        d.incrby('key1', 2)
        d.redis.hincrby.assert_called_with('RedisDict:test_dict', 'key1', 2)

    @patch('redis.StrictRedis')
    def test_incrbyfloat(self, StrictRedis):
        d = RedisDict(id='test_dict', fields={
            'key1': float
        })
        d['key1'] = 1.0
        d.incrbyfloat('key1', 2.5)
        d.redis.hincrbyfloat.assert_called_with('RedisDict:test_dict', 'key1', 2.5)

    @patch('redis.StrictRedis')
    def test_keys(self, StrictRedis):
        StrictRedis().hkeys.return_value = ['some', 'keys']
        d = RedisDict(id='test_dict')
        self.assertEquals(d.keys(), ['some', 'keys'])
        d.redis.hkeys.assert_called_with('RedisDict:test_dict')

    @patch('redis.StrictRedis')
    def test_values(self, StrictRedis):
        StrictRedis().hvals.return_value = ['some', 'values']
        d = RedisDict(id='test_dict')
        self.assertEquals(d.values(), ['some', 'values'])
        d.redis.hvals.assert_called_with('RedisDict:test_dict')

