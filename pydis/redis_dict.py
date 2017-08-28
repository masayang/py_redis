from . import RedisObject

class RedisDict(RedisObject):
    '''An equivalent to dict where all keys/values are stored in Redis.'''

    def __init__(self, id=None, fields={}, defaults=None, *args, **kwargs):
        '''
        Create a new RedisObject
        id: If specified, use this as the redis ID, otherwise generate a random ID.
        fields: A map of field name to construtor used to read values from redis.
            Objects will be written with json.dumps with default = str, so override __str__ for custom objects.
            This should generally be set by the subobject's constructor.
        defaults: A map of field name to values to store when constructing the object.
        '''

        super(RedisDict, self).__init__(id, *args, **kwargs)
        self.fields = fields
        if defaults:
            for key, val in defaults.items():
                self[key] = val

    def __getitem__(self, key):
        '''
        Load a field from this redis object.
        Keys that were not specified in self.fields will raise an exception.
        Keys that have not been set (either in defaults or __setitem__) will return the default for their type (if set)
        '''

        if key == 'id':
            return self.id.rsplit(':', 1)[-1]

        if not key in self.fields:
            raise KeyError('{} not found in {}'.format(key, self))

        return RedisObject.decode_value(self.fields[key], self.redis.hget(self.id, key))

    def __setitem__(self, key, val):
        '''
        Store a value in this redis object.
        Keys that were not specified in self.fields will raise an exception.
        Keys will be stored with json.dumps with a default of str, so override __str__ for custom objects.
        '''

        if not key in self.fields:
            raise KeyError('{} not found in {}'.format(key, self))

        self.redis.hset(self.id, key, RedisObject.encode_value(val))

    def __iter__(self):
        '''Return (key, val) pairs for all values stored in this RedisDict.'''

        yield ('id', self.id.rsplit(':', 1)[-1])

        for key in self.fields:
            yield (key, self[key])

    def __len__(self):
        return self.redis.hlen(self.id)

    def __delitem__(self, key):
        self.redis.hdel(self.id, key)

    def incrby(self, key, amount=1):
        self.redis.hincrby(self.id, key, amount)

    def incrbyfloat(self, key, amount=1.0):
        self.redis.hincrbyfloat(self.id, key, amount)

    def keys(self):
        return self.redis.hkeys(self.id)

    def values(self):
        return self.redis.hvals(self.id)

'''
HKEYS
HSCAN
HSTRLEN
HVALS
'''