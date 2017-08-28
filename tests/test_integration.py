import unittest
from datetime import datetime
from redis import StrictRedis
from ..samples import Tweet, TwitterUser

'''
Those tests involve actual Redis server, so please set those parameters below accordingly.
'''

HOST = "127.0.0.1"
PORT = 16379
DB = 0
PASSWORD = "PASSWORD"


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

    def test_user_and_tweet_creation(self):
        masayang = TwitterUser(
            twitter='@masayang'
        )
        tweet = Tweet(
            tweet='test message'
        )
        masayang['tweets'].append(tweet)
        self.assertEquals(masayang.id, 'TwitterUser:@masayang')
        self.assertEquals(masayang['tweets'], None)
