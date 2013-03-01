import feedparser
import redis
import os
import json
import eol

REDIS_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
r = redis.StrictRedis.from_url(REDIS_URL)

print "Checking EOL for updates"

url = "http://eol.jsc.nasa.gov/sseop/NewPhotos.xml"
d = feedparser.parse(url)

# Find the new image RSS entry in the list
for entry in d.entries:
    if '-Images' in entry.guid:
        guid = int(entry.guid[-15:-7])

        # check to see if set is new
        if not r.sismember('eol-image-sets', guid):

            print "Found new photos"

            # get photo ids
            link = eol.SETURL_BASE.format(guid=guid)
            photos = eol.scrape_photos(link)

            # push into redis
            for photo in photos:
                r.lpush('eol-'+str(guid), json.dumps(photo))

            r.lpush('eol-image-set-list', guid)
        r.sadd('eol-image-sets', guid)

print "Finished"
