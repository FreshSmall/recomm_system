import redis


class RedisDB(object):
    def __init__(self):
        self.redis_client = redis.Redis(
            host="127.0.0.1", port=6379, db=10, password="", decode_responses=True
        )
