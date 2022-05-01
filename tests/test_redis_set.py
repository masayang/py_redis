from pydis.redis_set import RedisSet
import pytest


class TestRedisSet:
    def test_constructor_without_items(self, resource):
        s = RedisSet('test_set')
        assert s.id == 'RedisSet:test_set'

    def test_constructor_with_items(self, resource):
        s = RedisSet('test_set', items=set(['a', 'b', 'c']))
        assert s.ismember('a')
        assert s.ismember('b')
        assert s.ismember('c')
        assert not s.ismember(1)

    def test_len(self, resource):
        s = RedisSet('test_set', items=set(['a', 'b', 'c']))
        assert len(s) == 3

    def test_iter(self, resource):
        s = RedisSet('test_set', items=set(['a', 'b', 'c']))
        result = set([])
        for x in s:
            result.add(x)
        assert result == set(['a', 'b', 'c'])

    def test_remove(self, resource):
        s = RedisSet('test_set', items=set(['a', 'b', 'c']))
        s.remove('b')
        assert s.members() == set(['a', 'c'])

    def test_randmember(self, resource):
        s = RedisSet('test_set', items=set(['a', 'b', 'c']))
        r = s.randmember(2)
        assert r.__class__ == [].__class__
        assert len(r) == 2
        assert (
            (r == ['a', 'b']) or 
            (r == ['a', 'c']) or
            (r == ['b', 'a']) or
            (r == ['b', 'c']) or
            (r == ['c', 'a']) or
            (r == ['c', 'b']) 
        )

    def test_pop(self, resource):
        s = RedisSet('test_set', items=set(['a', 'b', 'c']))
        r = s.pop(2)
        assert r.__class__ == [].__class__
        assert len(s) == 1
        assert (
            (r == ['a', 'b']) or 
            (r == ['a', 'c']) or
            (r == ['b', 'a']) or
            (r == ['b', 'c']) or
            (r == ['c', 'a']) or
            (r == ['c', 'b']) 
        )