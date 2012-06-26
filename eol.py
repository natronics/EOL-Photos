import urllib
import httplib
from BeautifulSoup import BeautifulSoup
import re

def get_images(soup):
  images = []
  
  results = soup('table')[3]
  
  for row in results.findAll('tr'):
    columns = row.findAll('td')
    if len(columns) > 4:
      mission   =       columns[1].string.strip()
      roll      =       columns[2].string.strip()
      frame     =       columns[3].a.string.strip()
      nadir_lat = float(columns[4].string.strip())
      nadir_lon = float(columns[5].string.strip())
      
      image = {"mission": mission, "roll": roll, "frame": frame, "lat": nadir_lat, "lon": nadir_lon}
      images.append(image)

  return images

def get_first_page(url):
  page = urllib.urlopen(url)
  soup = BeautifulSoup(page)
  
  # Next Page
  next_page = soup('form', {'name': 'NextPage'})[0]
  html_footer = str(next_page.find('input', {'name': 'HTMLfooter'})['value'])
  infile      = str(next_page.find('input', {'name': 'infile'})['value'])
  records     = int(next_page.find('input', {'name': 'records'})['value'])
  
  # Number of pages
  elem = soup.find('center', text=re.compile('Page '))
  pages = int(elem.findNext('b').findNext('b').text)
  
  images      = get_images(soup)
  record_key  = {"pages": pages, "htmlfooter": html_footer, "infile": infile, "records": records}

  return images, record_key

def get_page(key, page):
  images = []
  
  # POST data
  params = urllib.urlencode({   'HTMLfooter': key['htmlfooter']
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

  page = response.read()
  soup = BeautifulSoup(page)
  conn.close()
  
  images = get_images(soup)
  
  return images
