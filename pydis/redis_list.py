from . import RedisObject

class RedisList(RedisObject):
    def __init__(self, id=None, item_type=str, items=None):
        super(RedisList, self).__init__(id)
        self.item_type = item_type

        if items:
            for item in items:
                self.append(item)

    @classmethod
    def as_child(cls, parent, tag, item_type):
        def helper(_ = None):
            return cls(parent.id + ':' + tag, item_type)

        return helper

    def __getitem__(self, index):
        if isinstance(index, slice):
            if index.step is not None and index.step != 1:
                raise NotImplementedError('Cannot specify a step to a RedisObject slice')
            return [
                self.decode_value(self.item_type, el)
                for el in self.redis.lrange(self.id, index.start, index.stop)
            ]
        else:
            return self.decode_value(self.item_type, self.redis.lindex(self.id, index))

    def __setitem__(self, index, val):
        self.redis.lset(self.id, index, self.encode_value(val))

    def __len__(self):
        return self.redis.llen(self.id)

    def __delitem__(self, index):
        self.redis.lset(self.id, index, '__DELETED__')
        self.redis.lrem(self.id, 1, '__DELETED__')

    def __iter__(self):
        for el in self.redis.lrange(self.id, 0, -1):
            yield self.decode_value(self.item_type, el)

    def lpop(self):
        return self.decode_value(self.item_type, self.redis.lpop(self.id))

    def rpop(self):
        return self.decode_value(self.item_type, self.redis.rpop(self.id))

    def lpush(self, val):
        self.redis.lpush(self.id, self.encode_value(val))

    def rpush(self, val):
        self.redis.rpush(self.id, self.encode_value(val))

    def append(self, val):
        self.rpush(val)

    def insert_before(self, ref, val):
        return self.redis.linsert(self.id, 'BEFORE', ref, val)

    def insert_after(self, ref, val):
        return self.redis.linsert(self.id, 'AFTER', ref, val)

    def trim(self, start, stop):
        return self.redis.ltrim(self.id, start, stop)
