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

        masayang['score_board'].add('2017-01', 100)
        self.assertEqual(len(masayang['score_board']), 1)
        self.assertEqual(masayang['score_board'].rank('2017-01'), 0)

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

    def test_revrank(self):
        self.assertEquals(self.board.revrank('2017-01'), 1)
        self.assertEquals(self.board.revrank('2017-02'), 2)
        self.assertEquals(self.board.revrank('2017-03'), 0)

    def test_score(self):
        self.assertEquals(self.board.score('2017-01'), 100)
        self.assertEquals(self.board.score('2017-02'), 12)
        self.assertEquals(self.board.score('2017-03'), 222)

    def test_rem(self):
        self.board.rem('2017-01')
        self.assertEquals(len(self.board), 2)
        self.assertIsNone(self.board.rank('2017-01'))

    def test_remrangebyrank(self):
        self.board.remrangebyrank(0, 1)
        self.assertEqual(len(self.board), 1)
        self.assertIsNone(self.board.score('2017-01'))
        self.assertIsNone(self.board.score('2017-02'))
        self.assertEquals(self.board.score('2017-03'), 222)

    def test_remrangebyscore(self):
        self.board.remrangebyscore(0, 99)
        self.assertEqual(len(self.board), 2)
        self.assertEqual(self.board.score('2017-01'), 100)
        self.assertIsNone(self.board.score('2017-02'))
        self.assertEquals(self.board.score('2017-03'), 222)

    def test_range(self):
        range = self.board.range(0, 1)
        self.assertEquals(range, [('2017-02', 12), ('2017-01', 100)])

        range = self.board.range(0, 1, desc=True)
        self.assertEquals(range, [('2017-03', 222), ('2017-01', 100)])

    def test_revrange(self):
        range = self.board.revrange(0, 1)
        self.assertEquals(range, [('2017-03', 222), ('2017-01', 100)])

    def test_rangebyscore(self):
        range = self.board.rangebyscore(0, 99)
        self.assertEquals(range, [('2017-02', 12)])

        range = self.board.rangebyscore(0, 100)
        self.assertEquals(range, [('2017-02', 12), ('2017-01', 100)])

    def test_revrangebyscore(self):
        range = self.board.revrangebyscore(99, 0)
        self.assertEquals(range, [('2017-02', 12)])

        range = self.board.revrangebyscore(100, 0)
        self.assertEquals(range, [('2017-01', 100), ('2017-02', 12)])

    def test_incrby(self):
        self.board.incrby('2017-01', 1000)
        self.assertEqual(self.board.score('2017-01'), 1100)