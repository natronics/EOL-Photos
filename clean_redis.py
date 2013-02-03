import redis
import os

REDIS_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
r = redis.StrictRedis.from_url(REDIS_URL)

data = r.smembers('eol-image-sets')
for d in data:
    r.delete('eol-'+d)

r.delete('eol-image-sets')
