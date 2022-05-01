from pydis.redis_sortedset import RedisSortedSet
import pytest
import base64

def os_urandom_mock(hoge):
    return b"This is a random string"


@pytest.fixture
def ss():
    return RedisSortedSet('hogehoge', init_items=[
            {'2017-01': 10},
            {'2017-02': 20},
            {'2017-03': 30}
        ])


class TestRedisSortedSet:
    def test_constructor_empty(self, resource, mocker):
        mocker.patch('os.urandom', side_effect=os_urandom_mock)
        ss = RedisSortedSet()
        assert ss is not None
        assert ss.id == "RedisSortedSet:" + base64.urlsafe_b64encode(b"This is a random string").decode('utf-8')
        assert len(ss) == 0

    def test_constructor_with_items(self, resource, ss):
        assert ss.score('2017-01') == 10.0
        assert ss.score('2017-02') == 20.0
        assert ss.score('2017-03') == 30.0

    def test_count(self, resource, ss):
        assert ss.count(0, 99999) == 3
        assert ss.count(15, 99999) == 2
        assert ss.count(25, 99999) == 1
        assert ss.count(35, 99999) == 0
        
    def test_incrby(self, resource, ss):
        assert ss.incrby('2017-01', 100.0) == 110.0

    def test_range(self, resource, ss):
        assert ss.range(0, -1) == [('2017-01', 10.0), ('2017-02', 20.0), ('2017-03', 30.0)]
        assert ss.range(0, 1) == [('2017-01', 10.0), ('2017-02', 20.0)]
        assert ss.range(0, 0) == [('2017-01', 10.0)]

    def test_revrange(self, resource, ss):
        assert ss.revrange(0, -1) == [('2017-03', 30.0), ('2017-02', 20.0), ('2017-01', 10.0)]
        assert ss.revrange(0, 1) == [('2017-03', 30.0), ('2017-02', 20.0)]
        assert ss.revrange(0, 0) == [('2017-03', 30.0)]

    def test_rangebyscore(self, resource, ss):
        assert ss.rangebyscore(0, 99999) == [('2017-01', 10.0), ('2017-02', 20.0), ('2017-03', 30.0)]
        assert ss.rangebyscore(0, 25) == [('2017-01', 10.0), ('2017-02', 20.0)]
        assert ss.rangebyscore(15, 25) == [('2017-02', 20.0)]
        assert ss.rangebyscore(150, 250) == []

    def test_rem(self, resource, ss):
        assert ss.rem('2017-01', '2017-02') == 2
        assert ss.rangebyscore(0, 99999) == [('2017-03', 30.0)]
        
    def test_remrangebyrank(self, resource, ss):
        assert ss.remrangebyrank(0, 1) == 2
        assert ss.rangebyscore(0, 99999) == [('2017-03', 30.0)]

    def test_remrangebyscore(self, resource, ss):
        assert ss.remrangebyscore(10, 20) == 2
        assert ss.rangebyscore(0, 99999) == [('2017-03', 30.0)]

    def test_revrangebyscore(self, resource, ss):
        assert ss.revrangebyscore(35, 15) == [('2017-03', 30.0), ('2017-02', 20.0)]

    def test_rank(self, resource, ss):
        assert ss.rank('2017-01') == 0
        assert ss.rank('2017-02') == 1
        assert ss.rank('2017-03') == 2
        assert ss.rank('2017-04') is None

    def test_revrank(self, resource, ss):
        assert ss.revrank('2017-03') == 0
        assert ss.revrank('2017-02') == 1
        assert ss.revrank('2017-01') == 2
        assert ss.rank('2017-04') is None

    def test_score(self, resource, ss):
        assert ss.score('2017-01') == 10.0
        assert ss.score('2017-02') == 20.0
        assert ss.score('2017-03') == 30.0
        assert ss.score('2017-04') is None