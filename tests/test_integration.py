import unittest
from mock import patch
from redis import StrictRedis
from ..samples import Tweet, TwitterUser

'''
Those tests involve actual Redis server, so please set those parameters below accordingly.
'''

HOST = "127.0.0.1"
PORT = 6379
DB = 0
PASSWORD = None


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.sr = StrictRedis(
            host=HOST,
            port=PORT,
            db=DB,
            password=PASSWORD
        )

    def tearDown(self):
        self.cleanup('TwitterUser')
        self.cleanup('Tweet')
        self.cleanup('RedisDict')
        self.cleanup('RedisList')
        self.cleanup('@masayang')


    def cleanup(self, prefix):
        for key in self.sr.keys(prefix + '*'):
            self.sr.delete(key)

    def test_user_creation(self):
        masayang = TwitterUser(
            twitter='@masayang'
        )
        guest = TwitterUser(
            twitter='@guest'
        )
        masayang['friends'].add(guest)
        self.assertEquals(masayang.id, 'TwitterUser:@masayang')
        self.assertEquals(masayang['friends'].members(), set(['TwitterUser:@guest']))

        masayang['friends'].add(guest)
        self.assertEquals(masayang['friends'].members(), set(['TwitterUser:@guest']))

        raw_masayang = self.sr.hgetall("TwitterUser:@masayang")
        self.assertEquals(raw_masayang, {'twitter': '@masayang'})

        raw_masayang_friends = self.sr.smembers("TwitterUser:@masayang:friends")
        self.assertEquals(raw_masayang_friends, set(['TwitterUser:@guest']))

    @patch('os.urandom')
    def test_user_and_tweet_creation(self, urandom):
        urandom.return_value = '\xd8X\xfa@\x97\x90\x00dr'
        masayang = TwitterUser(
            twitter='@masayang'
        )
        tweet = Tweet(
            tweet='test message'
        )
        masayang['tweets'].append(tweet)
        self.assertEquals(masayang.id, 'TwitterUser:@masayang')
        result = []
        for t in masayang['tweets']:
            result.append(t.id)
        self.assertEqual(result, [u'Tweet:2Fj6QJeQAGRy'])
