import unittest
from ..pydis import RedisObject
from mock import patch
from redis import StrictRedis

class TestRedisObject(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('os.urandom')
    @patch('redis.StrictRedis')
    def test_constructor_without_id(self, StrictRedis, urandom):
        urandom.return_value = '\xd8X\xfa@\x97\x90\x00dr'
        r = RedisObject(db=1, host='some.host', password='secret', port=11111)
        StrictRedis.assert_called_with(db=1, decode_responses=True, host='some.host', password='secret', port=11111)
        self.assertEqual(r.id, u'RedisObject:2Fj6QJeQAGRy')

    @patch('redis.StrictRedis')
    def test_constructor_with_id(self, StrictRedis):
        r = RedisObject(id='i_have_an_id')
        StrictRedis.assert_called_with(db=0, decode_responses=True, host='localhost', password=None, port=6379)
        self.assertEqual(r.id, 'RedisObject:i_have_an_id')

    def test_bool(self):
        with patch.object(StrictRedis, 'exists') as new_exists:
            r = RedisObject()
            new_exists.return_value = False
            self.assertFalse(r.__bool__())

        with patch.object(StrictRedis, 'exists') as new_exists:
            r = RedisObject()
            new_exists.return_value = True
            self.assertTrue(r.__bool__())

    @patch('redis.StrictRedis')
    def test_equals(self, StrictRedis):
        r0 = RedisObject('some_key')
        r1 = RedisObject('some_key')
        self.assertEqual(r0, r1)

    @patch('redis.StrictRedis')
    def test_not_equals(self, StrictRedis):
        r0 = RedisObject('some_key')
        r1 = RedisObject('another_key')
        self.assertNotEqual(r0, r1)

    @patch('redis.StrictRedis')
    def test_constructor_without_id(self, StrictRedis):
        r = RedisObject('this is a key')
        self.assertEqual(r.__str__(), 'RedisObject:this is a key')

    def test_delete(self):
        with patch.object(StrictRedis, 'delete') as new_exists:
            r = RedisObject('this is a key')
            r.delete()
            r.redis.delete.assert_called_with('RedisObject:this is a key')

    def test_encode_decode(self):
        encoded = RedisObject.encode_value('string')
        self.assertEqual('string', RedisObject.decode_value(str, encoded))

        encoded = RedisObject.encode_value(12345)
        self.assertEqual(12345, RedisObject.decode_value(int, encoded))

