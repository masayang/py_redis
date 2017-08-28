import unittest
from pydis import RedisDict, RedisList, RedisSet



class TwitterUser(RedisDict):
    def __init__(self, id=None, twitter=None, *args, **kwargs):
        if twitter:
            id = twitter,
            kwargs['twitter'] = twitter

        super(TwitterUser, self).__init__(
            id=twitter,
            fields={
                'twitter': str,
                'friends': RedisList.as_child(self, 'friends', TwitterUser)
            },
            defaults=kwargs
        )

if __name__ == '__main__':
    masayang = TwitterUser(twitter="@masayang")
    print(masayang['twitter'])
    print(masayang['friends'])
    user1 = TwitterUser(twitter="@user1")
    masayang['friends'].append(user1)
