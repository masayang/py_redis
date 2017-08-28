from . import RedisObject

class RedisList(RedisObject):
    '''An equivalent to list where all items are stored in Redis.'''

    def __init__(self, id=None, item_type=str, items=None, *args, **kwargs):
        '''
        Create a new RedisList
        id: If specified, use this as the redis ID, otherwise generate a random ID.
        item_type: The constructor to use when reading items from redis.
        values: Default values to store during construction.
        '''

        super(RedisList, self).__init__(id, *args, **kwargs)
        self.item_type = item_type

        if items:
            for item in items:
                self.append(item)

    @classmethod
    def as_child(cls, parent, tag, item_type):
        '''Alternative callable constructor that instead defines this as a child object'''

        def helper(_ = None):
            return cls(parent.id + ':' + tag, item_type)

        return helper

    def __getitem__(self, index):
        '''
        Load an item by index where index is either an int or a slice
        Warning: this is O(n))
        '''
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
        '''Update an item by index
        Warning: this is O(n)
        '''
        self.redis.lset(self.id, index, self.encode_value(val))

    def __len__(self):
        '''Return the size of the list.'''

        return self.redis.llen(self.id)

    def __delitem__(self, index):
        '''Delete an item from a RedisList by index. (warning: this is O(n))'''

        self.redis.lset(self.id, index, '__DELETED__')
        self.redis.lrem(self.id, 1, '__DELETED__')

    def __iter__(self):
        '''Iterate over all items in this list.'''

        for el in self.redis.lrange(self.id, 0, -1):
            yield self.decode_value(self.item_type, el)

    def lpop(self):
        '''Remove and return a value from the left (low) end of the list.'''

        return self.decode_value(self.item_type, self.redis.lpop(self.id))

    def rpop(self):
        '''Remove a value from the right (high) end of the list.'''

        return self.decode_value(self.item_type, self.redis.rpop(self.id))

    def lpush(self, val):
        '''Add an item to the left (low) end of the list.'''

        self.redis.lpush(self.id, self.encode_value(val))

    def rpush(self, val):
        '''Add an item to the right (high) end of the list.'''

        self.redis.rpush(self.id, self.encode_value(val))

    def append(self, val):
        self.rpush(val)

    def insert_before(self, ref, val):
        return self.redis.linsert(self.id, 'BEFORE', ref, val)

    def insert_after(self, ref, val):
        return self.redis.linsert(self.id, 'AFTER', ref, val)

    def trim(self, start, stop):
        return self.redis.ltrim(self.id, start, stop)