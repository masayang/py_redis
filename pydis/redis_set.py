from . import RedisObject

class RedisSet(RedisObject):
    def __init__(self, id=None, item_type=str, items=None):
        super(RedisSet, self).__init__(id)
        self.item_type = item_type

        if items:
            for item in items:
                self.add(item)

    @classmethod
    def as_child(cls, parent, tag, item_type):
        def helper(_ = None):
            return cls(parent.id + ':' + tag, item_type)
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

    def members(self):
        return self.redis.smembers(self.id)

