from ..pydis import RedisDict, RedisSet, RedisList
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
                'tweets': RedisList.as_child(self, 'tweets', Tweet)
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