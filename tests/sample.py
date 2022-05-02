from pydis.redis_dict import RedisDict
from pydis.redis_set import RedisSet
from pydis.redis_list import RedisList
from pydis.redis_sortedset import RedisSortedSet
from datetime import datetime

class TwitterUser(RedisDict):
    def __init__(self, id=None, twitter=None, *args, **kwargs):
        if twitter:
            id = twitter,
            kwargs['twitter'] = twitter

        super(TwitterUser, self).__init__(
            id=twitter,
            fields={
                'twitter': str,
                'friends': RedisSet.as_child(self, 'friends', TwitterUser),
                'tweets': RedisList.as_child(self, 'tweets', Tweet),
                'score_board': RedisSortedSet.as_child(self, 'score_board')
            },
            defaults=kwargs
        )

class Tweet(RedisDict):
    def __init__(self, tweet=None, *args, **kwargs):
        kwargs['tweet'] = tweet
        kwargs['timestamp'] = datetime.now().isoformat()
        super(Tweet, self).__init__(
            id=None,
            fields={
                'timestamp': str,
                "tweet": tweet
            },
            defaults=kwargs
        )

class ScoreBoard(RedisSortedSet):
    def __init__(self, id=None, init_items=None):
        super(ScoreBoard, self).__init__(id=id, init_items=init_items)

