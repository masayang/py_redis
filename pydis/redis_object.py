import base64
import redis
import os
from .redis_settings import redis_config


class RedisObject(object):
    def __init__(self, id=None):
        self.redis = redis.StrictRedis(
            host=redis_config['host'],
            port=redis_config['port'],
            db=redis_config['db'],
            password=redis_config['password'],
            decode_responses=True)

        if id:
            self.id = id
        else:
            self.id = base64.urlsafe_b64encode(os.urandom(9)).decode('utf-8')

        if ':' not in self.id:
            self.id = self.__class__.__name__ + ':' + self.id

    def __bool__(self):
        return self.redis.exists(self.id)

    def __eq__(self, other):
        try:
            return self.id == other.id
        except AttributeError as e:
            return False

    def __str__(self):
        return self.id

    def delete(self):
        self.redis.delete(self.id)

    @staticmethod
    def decode_value(type, value):
        if value == None:
            return type()
        else:
            return type(value)

    @staticmethod
    def encode_value(value):
        return str(value)