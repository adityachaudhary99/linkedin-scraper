import redis
import json

class QueueHandler:
    def __init__(self):
        self.redis_conn = redis.Redis(host="localhost", port=6379, db=0)

    def add_to_queue(self, url):
        self.redis_conn.rpush("profile_urls", url)

    def get_from_queue(self):
        return self.redis_conn.lpop("profile_urls").decode('utf-8')

    def is_queue_empty(self):
        return self.redis_conn.llen("profile_urls") == 0
