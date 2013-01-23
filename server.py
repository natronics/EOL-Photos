#!/usr/bin/env python
import web
import views.photos

urls = (
    '/', 'index',
    '/favicon.ico', 'favicon'
)

class index:
    def GET(self):
        return views.photos.render.base(views.photos.gallery(), title="New ISS Images")

class favicon:
    def GET(self):
        # redirect to the static file ...
        raise web.seeother('/static/favicon.ico')
        
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.run()
