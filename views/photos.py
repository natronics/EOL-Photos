import web

render = web.template.render('templates/', cache=False, globals={})
render._keywords['globals']['render'] = render

def gallery(**k):
  images = range(100)
  return render.gallery(images)
