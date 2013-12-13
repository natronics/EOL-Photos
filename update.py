import feedparser
import eol
import datetime
from app import db
from models import *


def update_guid(guid):

    link = eol.SETURL_BASE.format(guid=guid)
    print link
    photos = eol.scrape_photos(link)

    for p in photos:
        photo = Photo(mission=p['mission'], roll=p['roll'], frame=p['frame'], set_id=guid, nadir_lon=p['lon'], nadir_lat=p['lat'])
        db.session.add(photo)

def check_rss():
    print "Checking EOL for updates"

    url = "http://eol.jsc.nasa.gov/sseop/NewPhotos.xml"
    d = feedparser.parse(url)

    # Find the new image RSS entry in the list
    for entry in d.entries:
        if '-Images' in entry.guid:
            guid = entry.guid[-15:-7]
            print guid

            if db.session.query(PhotoSet.id).filter(PhotoSet.id == guid).count() == 0:
                print "Found new photos"
                photoset = PhotoSet(id=guid, date=datetime.datetime.now())
                db.session.add(photoset)
                update_guid(guid)
                db.session.commit()


if __name__ == '__main__':
    check_rss()
