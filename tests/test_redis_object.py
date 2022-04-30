from pydis.redis_object import RedisObject, redis_config
import redis
import pytest

# https://stackoverflow.com/questions/26405380/how-do-i-correctly-setup-and-teardown-for-my-pytest-class-with-tests
@pytest.fixture()
def resource():
    delete_all()
    yield "resource"
    delete_all()

def get_client():
    return redis.StrictRedis(host=redis_config['host'], port=redis_config['port'], db=redis_config['db'], password=redis_config['password'])

def delete_all():
    r = get_client()
    for key in r.scan_iter("*"):
        r.delete(key)

class TestRedisObject:
    def test_constructor_without_id(self, resource):
        r = RedisObject()
        assert r.id != ""

    def test_constructor_with_id(self, resource):
        r = RedisObject(id='i_have_an_id')
        assert r.id == 'RedisObject:i_have_an_id'

#    def test_bool(self, resource):
#        r = RedisObject(id='i_have_an_id')
#        assert bool(r)

    def test_equals(self, resource):
        r0 = RedisObject('some_key')
        r1 = RedisObject('some_key')
        assert r0 == r1

    def test_not_equals(self, resource):
        r0 = RedisObject('some_key')
        r1 = RedisObject('another_key')
        assert r0 != r1

    def test_not_equals_non_object(self, resource):
        r0 = RedisObject('and now for')
        r1 = {'something': 'completely different'}
        assert r0.__eq__(r1) == False

    def test_str(self, resource):
        r = RedisObject('this is a key')
        assert r.__str__() == 'RedisObject:this is a key'

#    def test_delete(self, resource):
#        r = RedisObject('this is a key')
#        r.delete()

    def test_encode_decode(self, resource):
        encoded = RedisObject.encode_value('string')
        assert 'string' == RedisObject.decode_value(str, encoded)

        encoded = RedisObject.encode_value(12345)
        assert 12345 == RedisObject.decode_value(int, encoded)

    def test_encode_decode_none(self):
        encoded = RedisObject.encode_value(None)
        assert RedisObject.decode_value(str, encoded) == 'None'