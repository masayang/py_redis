from . import RedisObject

class RedisDict(RedisObject):
    '''
    An equivalent to dict where all keys/values are stored in Redis.
    '''
    def __init__(self, id=None, fields={}, defaults=None):
        '''
        Create a RedisDict.
        :param id: If specified, use this as the redis ID, otherwise generate a random ID.
        :param fields: A map of field name to construtor used to read values from redis.
            Objects will be written with json.dumps with default = str, so override __str__ for custom objects.
            This should generally be set by the subobject's constructor.
        :param defaults: Initial value for each field.
        '''
        super(RedisDict, self).__init__(id)
        self.fields = fields
        if defaults:
            for key, val in defaults.items():
                self[key] = val

    def __getitem__(self, key):
        '''
        Load a field from this redis object.
        :param key: The key of the field
        :return: The value of the field. If key doesn't exist, KeyError is raised.
        '''
        if key == 'id':
            return self.id.rsplit(':', 1)[-1]

        if not key in self.fields:
            raise KeyError('{} not found in {}'.format(key, self))

        return RedisObject.decode_value(self.fields[key], self.redis.hget(self.id, key))

    def __setitem__(self, key, val):
        '''
        Store a value in this redis object.
        :param key: The key of the field. If key doesn't exist, KeyError is raised.
        :param val: The value of the field.
        :return: 1 if new field is created, 0 otherwise.
        '''
        if not key in self.fields:
            raise KeyError('{} not found in {}'.format(key, self))
        self.redis.hset(self.id, key, RedisObject.encode_value(val))

    def __iter__(self):
        '''
        :return:  (key, val) pairs for all values stored in this RedisDict.
        '''
        yield ('id', self.id.rsplit(':', 1)[-1])
        for key in self.fields:
            yield (key, self[key])

    def __len__(self):
        '''
        :return: Number of fields of the object.
        '''
        return self.redis.hlen(self.id)

    def __delitem__(self, key):
        '''
        Delete the object.
        :param key: Key of the object.
        :return: None
        '''
        self.redis.hdel(self.id, key)

    def incrby(self, key, amount=1):
        '''
        Increment the field.
        :param key: Key of the field.
        :param amount: Incremental amount.
        :return: incremented value
        '''
        return self.redis.hincrby(self.id, key, amount)

    def incrbyfloat(self, key, amount=1.0):
        '''
        Increment the field.
        :param key: Key of the field.
        :param amount: Incremental amount.
        :return: incremented value
        '''
        return self.redis.hincrbyfloat(self.id, key, amount)

    def keys(self):
        '''
        Get keys of the object.
        :return: Keys of the object
        '''
        return self.redis.hkeys(self.id)

    def values(self):
        '''
        Get values of the object
        :return:  Values of the object
        '''
        return self.redis.hvals(self.id)
