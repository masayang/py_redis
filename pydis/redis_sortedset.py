from . import RedisObject

class RedisSortedSet(RedisObject):
    '''
    A wrapper class for Redis's sorted set.
    '''
    def __init__(self, id=None, init_items=None):
        '''
        Create a new RedisSortedSet
        :param id: If specified, use this as the redis ID, otherwise generate a random ID.
        :param init_items: Default value/score sets to store during construnction.
        '''
        super(RedisSortedSet, self).__init__(id)

        if init_items:
            for item in init_items:
                key = list(item.keys())[0]
                self.add(key, item[key])

    @classmethod
    def as_child(cls, parent, tag):
        '''
        Alternative callable constructor that instead defines this as a child object
        :param parent: Parent instance.
        :param tag: Tag of the child object
        '''
        def helper(_ = None):
            return cls(parent.id + ':' + tag)
        return helper

    def __len__(self):
        '''
        :return: length of the set
        '''
        return self.redis.zcard(self.id)

    def add(self, key, score):
        '''
        Set key/score pair to the sorted set
        :param key:
        :param score:
        :return:
        '''
        self.redis.zadd(self.id, score, key)

    def count(self, min, max):
        '''
        Returns the number of elements in the sorted set with a score between
        min and max.
        '''
        return self.redis.zcount(self.id, min, max)

    def incrby(self, value, amount=1):
        '''
        Increment the score of value in sortedset by amount
        '''
        return self.redis.zincrby(self.id, value, amount)

    def range(self, start, end, desc=False):
        '''
        Return a range of values from sorted set between start and end.
        :param desc: If true, returned values is sored in descending order.
        '''
        return self.redis.zrange(self.id, start, end, desc, withscores=True)

    def revrange(self, start, end):
        '''
        Return a range of values from sorted set between start and end sorted
        in descending order.
        '''
        return self.redis.zrevrange(self.id, start, end, withscores=True)

    def rangebyscore(self, min, max, start=None, num=None):
        '''
        Return a range of values from the sorted set with scores between min and
        max. If start and num are specified, then return a slice of the range.
        '''
        return self.redis.zrangebyscore(self.id, min, max, start, num, withscores=True)

    def rank(self, value):
        '''
        Returns a 0-based value indicating the rank of value in sorted set
        '''
        return self.redis.zrank(self.id, value)

    def rem(self, *values):
        '''
        Remove member values from sorted set
        '''
        return self.redis.zrem(self.id, *values)

    def remrangebyrank(self, min, max):
        '''
        Remove all elements in the sorted set with ranks between min and max.
        Values are 0-based, ordered from smallest score to largest.
        Values can be negative indicating the highest scores.
        Returns the number of elements removed
        '''
        return self.redis.zremrangebyrank(self.id, min, max)

    def remrangebyscore(self, min, max):
        '''
        Remove all elements in the sorted set with scores between min and max.
        Returns the number of elements removed.
        '''
        return self.redis.zremrangebyscore(self.id, min, max)

    def revrangebyscore(self, start, end):
        '''
        Return a range of values from the sorted set with scores between
        min and max in descending order.
        If start and num are specified, then return a slice of the range.
        '''
        return self.redis.zrevrangebyscore(self.id, start, end, withscores=True)

    def revrank(self, value):
        '''
        Returns a 0-based value indicating the descending rank of value in sorted set
        '''
        return self.redis.zrevrank(self.id, value)

    def score(self, value):
        '''
        Return the score of element value in sorted set
        '''
        return self.redis.zscore(self.id, value)
