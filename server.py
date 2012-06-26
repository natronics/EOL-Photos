#!/usr/bin/env python
import web
import views.photos
import views.home

urls = (
  '/', 'index',
  '/gallery/(.+)', 'gallery'
)

class index:
  def GET(self):
    return views.home.render.base(views.home.pack_homepage(), title="Browse EOL")
    #return views.photos.render.base(views.photos.gallery(), title="New ISS Images")

class gallery:
  def GET(self, gal):
    return views.home.render.base(views.photos.gallery(int(gal)), title="Gallery")
    

if __name__ == "__main__":
  app = web.application(urls, globals())
  app.internalerror = web.debugerror
  app.run()
