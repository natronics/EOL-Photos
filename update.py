import feedparser
import redis
import os
import json
import eol

REDIS_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
r = redis.StrictRedis.from_url(REDIS_URL)

def check_updates():
    """Hit the EOL new photos rss feed and add any new sets"""

    url = "http://eol.jsc.nasa.gov/sseop/NewPhotos.xml"
    d = feedparser.parse(url)

    # Find the new image RSS entry in the list
    for entry in d.entries:
        if '-Images' in entry.guid:
            guid = int(entry.guid[-15:-7])
            num  = int(entry.title.split("Images for ")[1].split(" New Photographs")[0])
            photoset = {
                         'link': entry.links[0].href,
                         'numphotos': num,
                         'scraped': False,
                       }
            # add to redis. The guid is the key, photoset is metadata
            r.zadd('eol-image-sets', guid, json.dumps(photoset))

def scrape_photosets():
    """Check for newly defined sets and scrape all photos from them"""

    # Get list of all sets
    image_sets = r.zrevrange('eol-image-sets', 0, 0, withscores=True)

    # Loop through sets
    for s in image_sets:
        s = json.loads(s[0])
        
        # Scrape new sets:
        if not s['scraped']:
            print "New photos found"

            # get photo ids
            photos = eol.scrape_photos(s['link'])
            # push into redis
            for photo in photos:
                r.lpush('eol-photos', json.dumps(photo))


###############################################################################
# Script Run
###############################################################################

print "Checking EOL for updates"

check_updates()
scrape_photosets()

print "Finished"
