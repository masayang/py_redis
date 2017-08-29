import unittest
from mock import patch
from redis import StrictRedis
from ..samples import Tweet, TwitterUser, ScoreBoard
from ..pydis.redis_settings import redis_config


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.sr = StrictRedis(
            host=redis_config['host'],
            port=redis_config['port'],
            db=redis_config['db'],
            password=redis_config['password']
        )

    def tearDown(self):
        self.cleanup('TwitterUser')
        self.cleanup('Tweet')
        self.cleanup('RedisDict')
        self.cleanup('RedisList')
        self.cleanup('@masayang')
        self.cleanup('test_board')


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

class TestScoreBoard(unittest.TestCase):
    def setUp(self):
        self.sr = StrictRedis(
            host=redis_config['host'],
            port=redis_config['port'],
            db=redis_config['db'],
            password=redis_config['password']
        )

        self.board = ScoreBoard(id="test_board", init_items=[
            {'2017-01': 100},
            {'2017-02': 12},
            {'2017-03': 222}
        ])

    def tearDown(self):
        self.cleanup('test_board')

    def cleanup(self, prefix):
        for key in self.sr.keys(prefix + '*'):
            self.sr.delete(key)

    def test_len(self):
        self.assertEquals(len(self.board), 3)

    def test_count(self):
        self.assertEquals(self.board.count(0, 1000), 3)
        self.assertEquals(self.board.count(100, 1000), 2)
        self.assertEquals(self.board.count(200, 1000), 1)

    def test_rank(self):
        self.assertEquals(self.board.rank('2017-01'), 1)
        self.assertEquals(self.board.rank('2017-02'), 0)
        self.assertEquals(self.board.rank('2017-03'), 2)

    def test_lexcount(self):
        self.assertEquals(self.board.lexcount('2', '3'), 0)