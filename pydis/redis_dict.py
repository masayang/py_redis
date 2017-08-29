from . import RedisObject

class RedisDict(RedisObject):
    def __init__(self, id=None, fields={}, defaults=None):
        super(RedisDict, self).__init__(id)
        self.fields = fields
        if defaults:
            for key, val in defaults.items():
                self[key] = val

    def __getitem__(self, key):
        if key == 'id':
            return self.id.rsplit(':', 1)[-1]

        if not key in self.fields:
            raise KeyError('{} not found in {}'.format(key, self))

        return RedisObject.decode_value(self.fields[key], self.redis.hget(self.id, key))

    def __setitem__(self, key, val):
        if not key in self.fields:
            raise KeyError('{} not found in {}'.format(key, self))

        self.redis.hset(self.id, key, RedisObject.encode_value(val))

    def __iter__(self):
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
