import redis
import os
import datetime
import json
import urllib
import httplib
from BeautifulSoup import BeautifulSoup
import re
import time

REDIS_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
r = redis.StrictRedis.from_url(REDIS_URL)

# EOL constants
SETURL_BASE = "http://eol.jsc.nasa.gov/scripts/sseop/PhotoIdSets/PhotoIdSets.pl?set=DailyUpdates%2F{guid}-Images"
THUMB_BASE = "http://eol.jsc.nasa.gov/sseop/images/thumb/{mission}/{mission}-{roll}-{frame}.jpg"

def get_photosets():
    all_sets = r.lrange('eol-image-set-list', 0, -1)
    sets = []
    for s in all_sets:
        upload_date = datetime.datetime.strptime(str(int(s)), "%Y%m%d")
        upload_date = upload_date.strftime("%Y&ndash;%m&ndash;%d")
        num = r.llen('eol-'+s)
        sets.append({'datestr': upload_date, 'num': num, 'id': s})
    return sets

def count_photos():
    data = r.smembers('eol-image-sets')
    num = 0
    for d in data:
        num += r.llen('eol-'+d)
    return num 

def show_photos(key, num, after):
    photos = r.lrange(key,after,after+num-1)
    data = []
    for p in photos:
        p = json.loads(p)
        data.append({
                      'thumb': THUMB_BASE.format(mission=p['mission'], roll=p['roll'], frame=p['frame']),
                      'm': p['mission'],
                      'r': p['roll'],
                      'f': p['frame'],
                    })
    return data

def get_most_recent():
    setid = r.lindex('eol-image-set-list', 0)
    return "eol-"+setid

def get_next_set(setid):
    all_sets = r.lrange('eol-image-set-list', 0, -1)
    for i, s in enumerate(all_sets):
        if ('eol-'+s) == setid:
            if i == len(all_sets)-1:
                return None
            return 'eol-'+all_sets[i+1]
    return None

def get_metadata(setid):
    upload_date = "No new photos"
    if len(setid) > 4:
        upload_date = datetime.datetime.strptime(setid[4:], "%Y%m%d")
        upload_date = upload_date.strftime("%B %d, %Y")
    return upload_date

#================================================================
# Scrapper Code:
#================================================================

def get_images(soup):
    images = []     
    results = soup('table')[3]

    for row in results.findAll('tr'):
        columns = row.findAll('td')
        if len(columns) >= 3 :
            mission   =       columns[1].string.strip()
            roll      =       columns[2].string.strip()
            frame     =       columns[3].a.string.strip()
            #nadir_lat = float(columns[4].string.strip())
            #nadir_lon = float(columns[5].string.strip())

            image = {"mission": mission, "roll": roll, "frame": frame}
            images.append(image)

    return images

def get_first_page(url):
    page = urllib.urlopen(url)
    soup = BeautifulSoup(page)

    # Number of pages
    elem = soup.find('center', text=re.compile('Page '))
    pages = int(elem.findNext('b').findNext('b').text)
      
    record_key = {"pages": pages}
    # Next Page
    if pages > 1:
        next_page = soup('form', {'name': 'NextPage'})[0]        
        html_footer = str(next_page.find('input', {'name': 'HTMLfooter'})['value'])
        infile      = str(next_page.find('input', {'name': 'infile'})['value'])
        records     = int(next_page.find('input', {'name': 'records'})['value'])
        record_key["htmlfooter"] = html_footer
        record_key["infile"] = infile
        record_key["records"] = records

    images      = get_images(soup)
    return images, record_key

def get_page(key, page):
    images = []

    # POST data
    params = urllib.urlencode({ 'HTMLfooter': key['htmlfooter']
                              , 'infile':     key['infile']
                              , 'page':       page
                              , 'pagesize':   50
                              , 'records':    key['records']
                              , 'thumbs':     'N'
                              , 'url':        '/sseop/'})

    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("eol.jsc.nasa.gov:80")
    conn.request("POST", "/scripts/sseop/changepage.pl", params, headers)
    response = conn.getresponse()

    print response.status, response.reason

    if response.status == 200:

        page = response.read()
        soup = BeautifulSoup(page)
        conn.close()

        images = get_images(soup)

    return images

def scrape_photos(url):
    print "getting first page..."
    images_1, record_key = get_first_page(url)

    images = []
    for im in images_1:
        images.append(im)
    for i in range(2, record_key['pages']+1):
        print "getting page", i, "of", record_key['pages']
        images_page = get_page(record_key, i)
        for im in images_page:
            images.append(im)
        time.sleep(10)

    return images
