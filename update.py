import feedparser
import datetime
from app import db
from models import *



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
        r.lpush('eol-image-set-list', guid)
    r.sadd('eol-image-sets', guid)

def check_rss():
    print "Checking EOL for updates"

    url = "http://eol.jsc.nasa.gov/sseop/NewPhotos.xml"
    d = feedparser.parse(url)

    # Find the new image RSS entry in the list
    for entry in d.entries:
        if '-Images' in entry.guid:
            guid = entry.guid[-15:-7]
            photoset = PhotoSet(id=guid, date=datetime.datetime.now())
            db.session.add(photoset)
            db.session.commit()
            print guid
            #update_guid(guid)


if __name__ == '__main__':
    check_rss()
