import base64
import redis
import os

class RedisObject(object):
    '''
    A base object backed by redis.
    Genrally, use RedisDict or RedisList rather than this directly.
    '''

    def __init__(self, id=None, host='localhost', port=6379, db=0, password=None):
        '''Create or load a RedisObject.'''
        self.redis = redis.StrictRedis(
            host=host,
            port=port,
            db=db,
            password=password,
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
        return self.id == other.id

    def __str__(self):
        '''Return this object as a string for testing purposes.'''
        return self.id

    def delete(self):
        '''Delete this object from redis'''
        self.redis.delete(self.id)

    @staticmethod
    def decode_value(type, value):
        if value is None:
            return None
        else:
            return type(value)

    @staticmethod
    def encode_value(value):
        if value is None:
            return str()
        else:
            return str(value)
