import base64
import redis
import os
from .redis_settings import redis_config


class RedisObject(object):
    '''
    A base object backed by redis.
    Genrally, use RedisDict or RedisList rather than this directly.
    '''

    def __init__(self, id=None):
        '''Create or load a RedisObject.'''
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
        '''Test if an object currently exists'''
        return self.redis.exists(self.id)

    def __eq__(self, other):
        '''Tests if two redis objects are equal (they have the same key)'''
        try:
            return self.id == other.id
        except AttributeError as e:
            return False

    def __str__(self):
        '''Return this object as a string for testing purposes.'''
        return self.id

    def delete(self):
        '''Delete this object from redis'''
        self.redis.delete(self.id)

    @staticmethod
    def decode_value(type, value):
        '''Decode a value if it is non-None, otherwise, decode with no arguments.'''

        if value == None:
            return type()
        else:
            return type(value)

    @staticmethod
    def encode_value(value):
        '''Encode a value using json.dumps, with default = str'''

        return str(value)