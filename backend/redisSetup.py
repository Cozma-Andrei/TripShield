import redisSetup
import redis
def setup():
    r  = redis.Redis(host='localhost', port=6379, db=0)
    return r