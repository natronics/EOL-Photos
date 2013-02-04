import feedparser
import redis
import os
import sys
import json
import eol

REDIS_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
r = redis.StrictRedis.from_url(REDIS_URL)

def update_guid(guid):
    # check to see if set is new
    if not r.sismember('eol-image-sets', guid):

        print "Found new photos"

        # get photo ids
        link = eol.SETURL_BASE.format(guid=guid)
        photos = eol.scrape_photos(link)

        # push into redis
        for photo in photos:
            r.lpush('eol-'+str(guid), json.dumps(photo))

    r.sadd('eol-image-sets', guid)

def check_rss():
    print "Checking EOL for updates"

    url = "http://eol.jsc.nasa.gov/sseop/NewPhotos.xml"
    d = feedparser.parse(url)

    # Find the new image RSS entry in the list
    for entry in d.entries:
        if '-Images' in entry.guid:
            guid = int(entry.guid[-15:-7])
            update_guid(guid)


if len(sys.argv) == 2:
    url = sys.argv[1]
    guid = url[-15:-7]
    update_guid(guid)
else:
    check_rss()

print "Finished"
