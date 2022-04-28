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
    def test_object(self, resource):
        o = RedisObject(id="hogehoge")
        assert o.id == "RedisObject:hogehoge"
        
        o2 = o = RedisObject(id="hogehoge")

        assert o == o2

        assert o.__str__() == "RedisObject:hogehoge"
