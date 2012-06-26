#!/usr/bin/env python
import eol
import sys
import db.sqlite as db
import datetime
import time

url         = "http://eol.jsc.nasa.gov/scripts/sseop/PhotoIdSets/PhotoIdSets.pl?set=DailyUpdates%2F20120620-Images"
#now         = datetime.datetime.now()
date        = url[84:84+8]
year        = int(date[0:4])
month       = int(date[5:6])
day         = int(date[6:])
image_date  = datetime.datetime(year, month, day)
unixtime    = int(time.mktime(image_date.timetuple()))

# get first set of images
print "Getting page 1"
images, key = eol.get_first_page(url)

for page in range(2, key['pages']+1):
  print "Getting page %3d of %d ... ..." % (page, key['pages']),
  _images = eol.get_page(key, page)
  
  for image in _images:
    images.append(image)

image_table = db.Images()
image_table.begin_transaction()
for image in images:
  image_table.insert_image(unixtime, image)
image_table.commit_transaction()
