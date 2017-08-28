from . import RedisObject

class RedisSet(RedisObject):
    def __init__(self, id=None, items=None):
        super(RedisSet, self).__init__(id)

        if items:
            for item in items:
                self.add(item)

    @classmethod
    def as_child(cls, parent, tag):
        def helper(_ = None):
            return cls(parent.id + ':' + tag)
        return helper

    def __len__(self):
        return self.redis.scard(self.id)

    def __iter__(self):
        for item in self.redis.smembers(self.id):
            yield self.decode_value(type(item), item)

    def add(self, item):
        self.redis.sadd(self.id, self.encode_value(item))

    def remove(self, item):
        self.redis.srem(self.id, item)

    def ismember(self, item):
        return self.redis.sismember(self.id, self.encode_value(item))

    def randmember(self, number=1):
        return self.redis.srandmember(self.id, number)

    def pop(self, number=1):
        return self.redis.spop(self.id, number)

'''
SDIFF
SDIFFSTORE
SINTER
SINTERSTORE
SMOVE
SSCAN
SUNION
SUNIONSTORE
'''
