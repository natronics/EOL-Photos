import feedparser
import redis
import os
import json
import eol

REDIS_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
r = redis.StrictRedis.from_url(REDIS_URL)

def check_updates():
    url = "http://eol.jsc.nasa.gov/sseop/NewPhotos.xml"

    d = feedparser.parse('NewPhotos.xml')

    for entry in d.entries:
        if '-Images' in entry.guid:
            guid = int(entry.guid[0:-7])
            num  = int(entry.title.split("Images for ")[1].split(" New Photographs")[0])
            photoset = {
                        'link': entry.links[0].href,
                        'numphotos': num,
                        }
            r.zadd('eol-image-sets', guid, json.dumps(photoset))
            #print guid, photoset
image_sets = r.zrevrange('eol-image-sets', 0, 0, withscores=True)
for s in image_sets:
    s = json.loads(s[0])
    photos = eol.scrape_photos(s['link'])
    for photo in photos:
        r.lpush('eol-photos', json.dumps(photo))
