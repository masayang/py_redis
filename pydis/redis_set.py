from . import RedisObject

class RedisSet(RedisObject):
    '''
    An equivalent to set where all items are stored in Redis.
    '''
    def __init__(self, id=None, item_type=str, items=None):
        '''
        Create a new RedisSet
        :param id: If specified, use this as the redis ID, otherwise generate a random ID.
        :param item_type: The constructor to use when reading items from redis.
        :param items: Default values to store during construction.
        '''
        super(RedisSet, self).__init__(id)
        self.item_type = item_type

        if items:
            for item in items:
                self.add(item)

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

    def __len__(self):
        '''
        :return: length of the set
        '''
        return self.redis.scard(self.id)

    def __iter__(self):
        '''
        Iterate over all items in this set.
        '''
        for item in self.redis.smembers(self.id):
            yield self.decode_value(type(item), item)

    def add(self, item):
        '''
        Add an item to the set
        :param item:
        :return: None
        '''
        self.redis.sadd(self.id, self.encode_value(item))

    def remove(self, item):
        '''
        Remove an item from the set.
        :param item:
        :return: None
        '''
        self.redis.srem(self.id, item)

    def ismember(self, item):
        '''
        Return a boolean indicating if item is a member of set
        '''
        return self.redis.sismember(self.id, self.encode_value(item))

    def randmember(self, number=1):
        '''
        returns a list of number random memebers of set.
        '''
        return self.redis.srandmember(self.id, number)

    def pop(self, number=1):
        '''
        Remove and return a random member of set
        '''
        return self.redis.spop(self.id, number)

    def members(self):
        '''
        Return all members of the set
        '''
        return self.redis.smembers(self.id)

