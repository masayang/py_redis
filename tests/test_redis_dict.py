from pydis.redis_dict import RedisDict
import pytest
from collections import Counter


class TestRedisDict:
    def test_constructor_empty(self, resource):
        d = RedisDict(id='test_dict')
        assert d.id == 'RedisDict:test_dict'
        assert d.fields == {}

    def test_constructor_with_fields(self, resource):
        d = RedisDict(id='test_dict', fields={
            'int_val': int,
            'str_val': str
        })
        assert d.id == 'RedisDict:test_dict'
        assert d.fields == {
            'int_val': int,
            'str_val': str
        }

    def test_constructor_with_fields_and_defaults(self, resource):
        d = RedisDict(id='test_dict', fields={
            'str_val': str
        }, defaults={
            'str_val': 'string'
        })
        assert d.id == 'RedisDict:test_dict'
        assert d.fields == {
            'str_val': str
        }
        assert d['str_val'] == "string"

    def test_len(self, resource):
        d = RedisDict(id='test_dict', fields={
            'int_val': int,
            'str_val': str,
            'another': str
        }, defaults={
            'int_val': 1,
            'str_val': "ABC",
            'another': "DEF"
        })
        assert len(d) == 3

    def test_get_id(self, resource):
        d = RedisDict(id='test_dict')
        assert d['id'] == "test_dict"

    def test_get_invalid_key(self, resource):
        d = RedisDict(id='test_dict')
        with pytest.raises(KeyError, match=r".*unknown key not found in RedisDict:test_dict.*"):
            d['unknown key']

    def test_set_invalid_key(self, resource):
        d = RedisDict(id='test_dict')
        with pytest.raises(KeyError, match=r".*something not found in RedisDict:test_dict.*"):
            d['something'] = 'hoge'

    def test_iterator(self, resource):
        d = RedisDict(id='test_dict', fields={
            'key1': str,
            'key2': str
        })
        d['key1'] = 'string'
        d['key2'] = 'string'

        results = []
        for kv in d:
            results.append(kv)
        assert Counter(results) == Counter([
            ('id', 'test_dict'),
            ('key2', 'string'),
            ('key1', 'string')
        ])

    def test_delitem(self, resource):
        d = RedisDict(id='test_dict', fields={
            'key1': str,
            'key2': str
        })
        d['key1'] = 'string'
        d['key2'] = 'string'

        del d['key1']
        assert d['key1'] == ''

    def test_incrby(self, resource):
        d = RedisDict(id='test_dict', fields={
            'key1': int
        })
        d['key1'] = 1
        d.incrby('key1', 2)
        assert d['key1'] == 3

    def test_incrbyfloat(self, resource):
        d = RedisDict(id='test_dict', fields={
            'key1': float
        })
        d['key1'] = 1.0
        d.incrbyfloat('key1', 2.5)
        assert d['key1'] == 3.5

    def test_keys(self, resource):
        d = RedisDict(id='test_dict', fields={
            'key1': str,
            'key2': str
        })
        d['key1'] = 'string'
        d['key2'] = 'string'

        assert d.keys() == ['key1', 'key2']

    def test_values(self, resource):
        d = RedisDict(id='test_dict', fields={
            'key1': str,
            'key2': str
        })
        d['key1'] = 'some'
        d['key2'] = 'values'
        assert d.values() == ['some', 'values']
