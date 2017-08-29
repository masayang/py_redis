from . import RedisObject

class RedisSortedSet(RedisObject):
    def __init__(self, id=None, init_items=None):
        super(RedisSortedSet, self).__init__(id)

        if init_items:
            for key in init_items.keys():
                self.add(key, init_items[key])

    @classmethod
    def as_child(cls, parent, tag):
        def helper(_ = None):
            return cls(parent.id + ':' + tag)
        return helper

    def __len__(self):
        return self.redis.zcard(self.id)

    def add(self, key, score):
        self.redis.zadd(self.id, key, score)

    def count(self, min, max):
        return self.redis.zcount(self.id, min, max)

    def lexcount(self, min, max):
        return self.redis.zlexcount(self.id, min, max)

    def incrby(self, value, amount=1):
        self.redis.zincrby(self.id, value, amount)

    def range(self, start, end, desc=False):
        return self.redis.zrange(self.id, start, end, desc)

    def rangebylex(self, min, max, start=None, num=None):
        return self.redis.zrangebylex(self.id, min, max, start, num)

    def rangebyscore(self, min, max, start=None, num=None):
        return self.redis.zrangebyscore(self.id, min, max, start, num)

    def rank(self, value):
        return self.redis.zrank(self.id, value)

    def rem(self, *values):
        return self.redis.zrem(self.id, *values)

    def remrangebylex(self, min, max):
        self.redis.zremrangebylex(self.id, min, max)

    def remrangebyrank(self, min, max):
        self.redis.zremrangebyrank(self.id, min, max)

    def remrangebyscore(self, min, max):
        self.redis.zremrangebyscore(self.id, min, max)

    def revrange(self, start, end):
        return self.redis.zrevrange(self.id, start, end)

    def revrangebylex(self, start, end):
        return self.redis.zrevrangebylex(self.id, start, end)

    def revrangebyscore(self, start, end):
        return self.redis.zrevrangebyscore(self.id, start, end)

    def revrank(self, value):
        return self.redis.zrevrank(self.id, value)

    def score(self, value):
        return self.redis.zscore(self.id, value)


