from pydis.redis_object import redis_config
from sample import Tweet, TwitterUser, ScoreBoard
import base64
import pytest


def os_urandom_mock(hoge):
    return b"This is a random string"


class TestSample:
    def test_user_creation(self, resource):
        masayang = TwitterUser(
            twitter='@masayang'
        )
        guest = TwitterUser(
            twitter='@guest'
        )
        another_guest = TwitterUser(
            twitter='@another_guest'
        )

        masayang['friends'].add(guest)
        assert masayang.id == 'TwitterUser:@masayang'
        assert masayang['friends'].members() == {'TwitterUser:@guest'}

        masayang['friends'].add(guest)
        assert masayang['friends'].members() == {'TwitterUser:@guest'}

        masayang['friends'].add(another_guest)
        assert masayang['friends'].members(
        ) == {'TwitterUser:@another_guest', 'TwitterUser:@guest'}

        raw_masayang = masayang.redis.hgetall("TwitterUser:@masayang")
        assert raw_masayang == {'twitter': '@masayang'}

        raw_masayang_friends = masayang.redis.smembers(
            "TwitterUser:@masayang:friends")
        assert raw_masayang_friends == {
            'TwitterUser:@another_guest', 'TwitterUser:@guest'}

        masayang['score_board'].add('2017-01', 100)
        masayang['score_board'].add('2017-02', 200)
        masayang['score_board'].add('2017-03', 300)

        assert len(masayang['score_board']) == 3
        assert masayang['score_board'].rank('2017-01') == 0
        assert masayang['score_board'].rank('2017-02') == 1
        assert masayang['score_board'].rank('2017-03') == 2

        assert masayang['score_board'].revrank('2017-01') == 2
        assert masayang['score_board'].revrank('2017-02') == 1
        assert masayang['score_board'].revrank('2017-03') == 0

    def test_user_and_tweet_creation(self, mocker):
        mocker.patch('os.urandom', side_effect=os_urandom_mock)

        masayang = TwitterUser(
            twitter='@masayang'
        )
        tweet = Tweet(
            tweet='test message'
        )
        masayang['tweets'].append(tweet)
        assert masayang.id == 'TwitterUser:@masayang'
        assert len(masayang['tweets']) == 1

        result = []
        for t in masayang['tweets']:
            result.append(t.id)
        assert result == [
            "Tweet:" + base64.urlsafe_b64encode(b"This is a random string").decode('utf-8')]


@pytest.fixture
def board():
    return [
        {'2017-01': 100},
        {'2017-02': 200},
        {'2017-03': 300}
    ]


class TestScoreBoard:
    def test_len(self, resource, board):
        b = ScoreBoard(id="test_board", init_items=[*board])
        assert len(b) == 3

    def test_count(self, resource, board):
        b = ScoreBoard(id="test_board", init_items=[*board])

        assert b.count(0, 1000) == 3
        assert b.count(150, 1000) == 2
        assert b.count(250, 1000) == 1
        assert b.count(350, 1000) == 0

    def test_rank(self, resource, board):
        b = ScoreBoard(id="test_board", init_items=[*board])

        assert b.rank("2017-01") == 0
        assert b.rank("2017-02") == 1
        assert b.rank("2017-03") == 2

    def test_revrank(self, resource, board):
        b = ScoreBoard(id="test_board", init_items=[*board])

        assert b.revrank("2017-01") == 2
        assert b.revrank("2017-02") == 1
        assert b.revrank("2017-03") == 0

    def test_score(self, resource, board):
        b = ScoreBoard(id="test_board", init_items=[*board])

        assert b.score('2017-01') == 100.0
        assert b.score('2017-02') == 200.0
        assert b.score('2017-03') == 300.0

    def test_rem(self, resource, board):
        b = ScoreBoard(id="test_board", init_items=[*board])

        b.rem('2017-01')
        assert len(b) == 2
        assert b.rank('2017-01') is None


    def test_remrangebyrank(self, resource, board):
        b = ScoreBoard(id="test_board", init_items=[*board])

        b.remrangebyrank(0, 1)
        assert len(b) == 1
        assert b.score('2017-01') is None
        assert b.score('2017-02') is None
        assert b.score('2017-03') ==  300.0

    def test_remrangebyscore(self, resource, board):
        b = ScoreBoard(id="test_board", init_items=[*board])

        b.remrangebyscore(0, 150)
        assert len(b) == 2
        assert b.score('2017-01') is None
        assert b.score('2017-02') == 200.0
        assert b.score('2017-03') == 300.0

    def test_range(self, resource, board):
        b = ScoreBoard(id="test_board", init_items=[*board])

        r = b.range(0, 1)
        assert r == [('2017-01', 100.0), ('2017-02', 200.0)]

        r = b.range(0, 1, desc=True)
        assert r == [('2017-03', 300.0), ('2017-02', 200.0)]

    def test_revrange(self, resource, board):
        b = ScoreBoard(id="test_board", init_items=[*board])

        r = b.revrange(0, 1)
        assert r == [('2017-03', 300.0), ('2017-02', 200.0)]

        assert b.revrange(0, 1) == b.range(0, 1, desc=True)

    def test_rangebyscore(self, resource, board):
        b = ScoreBoard(id="test_board", init_items=[*board])

        r = b.rangebyscore(150, 250)
        assert r == [('2017-02', 200.0)]

        r = b.rangebyscore(150, 350)
        assert r == [('2017-02', 200.0), ('2017-03', 300.0)]

    def test_revrangebyscore(self, resource, board):
        b = ScoreBoard(id="test_board", init_items=[*board])

        r = b.revrangebyscore(250, 150)
        assert r == [('2017-02', 200.0)]

        r = b.revrangebyscore(350, 150)
        assert r == [('2017-03', 300), ('2017-02', 200)]

    def test_incrby(self, resource, board):
        b = ScoreBoard(id="test_board", init_items=[*board])

        b.incrby('2017-01', 1000)
        assert b.score('2017-01') == 1100
