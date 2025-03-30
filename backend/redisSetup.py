import redis
def redisSetup():
    r  = redis.Redis(host='localhost', port=6379, db=0)
    return r