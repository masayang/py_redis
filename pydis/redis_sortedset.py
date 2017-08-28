from . import RedisObject

class RedisSortedSet(RedisObject):
    def __init__(self, id=None, init_scores=None):
        super(RedisSortedSet, self).__init__(id)

        if init_scores:
            for key in init_scores.keys():
                self.add(key, init_scores[key])

    def __len__(self):
        return self.redis.zcard(self.id)

    def add(self, key, score):
        self.redis.zadd(self.id, key, score)



