import web
import db.sqlite as db

render = web.template.render('templates/', cache=False, globals={})
render._keywords['globals']['render'] = render

def pack_homepage():
  dates     = db.get_dates()
  galleries = render.photo_date_list(dates)
  
  return galleries
