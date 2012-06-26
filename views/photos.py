import web
import db.sqlite as db

render = web.template.render('templates/', cache=False, globals={})
render._keywords['globals']['render'] = render

def gallery(galid):
  urls    = []
  images  = db.get_images(galid)
  
  for image in images[0:100]:
    baseurl = "http://eol.jsc.nasa.gov/sseop/images/thumb/%s/%s-%s-%d.jpg"
    url     = baseurl % (image['mission'], image['mission'], image['roll'], image['frame'])
    urls.append(url)
    
  return render.gallery(urls)
