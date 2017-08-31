from . import RedisObject

class RedisList(RedisObject):
    '''
    An equivalent to list where all items are stored in Redis.
    '''
    def __init__(self, id=None, item_type=str, items=None):
        '''
        Create a new RedisList
        :param id: If specified, use this as the redis ID, otherwise generate a random ID.
        :param item_type: The constructor to use when reading items from redis.
        :param items: Default values to store during construction.
        '''
        super(RedisList, self).__init__(id)
        self.item_type = item_type

        if items:
            for item in items:
                self.append(item)

    @classmethod
    def as_child(cls, parent, tag, item_type):
        '''
        Alternative callable constructor that instead defines this as a child object
        :param parent: Parent instance.
        :param tag: Tag of the child object
        :param item_type: Type of the object
        '''
        def helper(_ = None):
            return cls(parent.id + ':' + tag, item_type)
        return helper

    def __getitem__(self, index):
        '''
        Load an item by index where index is either an int or a slice
        No step greater than 1 is allowed for a slice.
        Warning: this is O(n))
        :param index: Number or a slice
        :return: The value if exists otherwise None
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
        '''
        Update an item by index
        Warning: this is O(n)
        :param index: Number
        :param val: New value
        :return: None
        '''
        self.redis.lset(self.id, index, self.encode_value(val))

    def __len__(self):
        '''
        :return: length of the list
        '''
        return self.redis.llen(self.id)

    def __delitem__(self, index):
        '''
        Delete an item from the list.
        (warning: this is O(n))
        :param index: Target
        :return: None
        '''
        self.redis.lset(self.id, index, '__DELETED__')
        self.redis.lrem(self.id, 1, '__DELETED__')

    def __iter__(self):
        '''
        Iterate over all items in this list.
        '''
        for el in self.redis.lrange(self.id, 0, -1):
            yield self.decode_value(self.item_type, el)

    def lpop(self):
        '''
        Remove and return the first item of the list
        '''
        return self.decode_value(self.item_type, self.redis.lpop(self.id))

    def rpop(self):
        '''
        Remove and return the last item of the list
        :return:
        '''
        return self.decode_value(self.item_type, self.redis.rpop(self.id))

    def lpush(self, val):
        '''
        Push val onto the head of the list
        :param val:
        :return: None
        '''
        self.redis.lpush(self.id, self.encode_value(val))

    def rpush(self, val):
        '''
        Push val onto the tail of the list
        :param val:
        :return: None
        '''
        self.redis.rpush(self.id, self.encode_value(val))

    def append(self, val):
        '''
        An alias to rpush
        :param val:
        :return:
        '''
        self.rpush(val)

    def insert_before(self, ref, val):
        '''
        Insert val in list name immediately before ref
        :param ref:
        :param val:
        :return: the new length of the list on success or -1 if ref is not in the list.
        '''
        return self.redis.linsert(self.id, 'BEFORE', ref, val)

    def insert_after(self, ref, val):
        '''
        Insert val in list name immediately after ref
        :param ref:
        :param val:
        :return: the new length of the list on success or -1 if ref is not in the list.
        '''
        return self.redis.linsert(self.id, 'AFTER', ref, val)

    def trim(self, start, stop):
        '''
        Trim the list by removing all values not within the slice between start and end
        start and end can be negative numbers just like Python slicing notation
        :param start:
        :param stop:
        :return: None
        '''
        self.redis.ltrim(self.id, start, stop)
