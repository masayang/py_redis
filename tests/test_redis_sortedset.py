import unittest
from ..pydis import RedisSortedSet
from redis import StrictRedis
from mock import patch

class TestRedisSortedSet(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('redis.StrictRedis')
    def test_constructor_empty(self, StrictRedis):
        pass
