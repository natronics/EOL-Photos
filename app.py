import os
from flask import Flask, request, jsonify, render_template, send_from_directory
import eol
import time
app = Flask(__name__)

GLOBALS = {"sitename": "EOL Browser"}

@app.route("/")
def index():
    fset = eol.get_most_recent()
    return render_template('index.html', sitename=GLOBALS["sitename"]
                                       , title="Recent ISS Photographs"
                                       , links=[{"title": "About", "url": "/about.html"}]
                                       , firstset=fset)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/updates/<int:setid>')
def showset(setid):
    setid = 'eol-'+str(setid)
    header = eol.get_metadata(setid)
    return render_template('update.html', sitename=GLOBALS["sitename"]
                                       , title="Recent ISS Photographs"
                                       , links=[{"title": "All Images", "url": "/"}, {"title": "About", "url": "/about.html"}]
                                       , setname=header
                                       , setid=setid)

@app.route("/loader.html", methods=['POST'])
def loader():
    chunk = 120
    try:
        after = int(request.form["after"]) +1
    except:
        after = 0

    setid = request.form["set"]

    if after == 0:
        header = eol.get_metadata(setid)
    else:
        header = None

    data = eol.show_photos(setid, chunk, after)

    if len(data) == 0:
        if request.form["infinite"] == "true":
            setid = eol.get_next_set(setid)
            if not setid:
                return render_template('loader.html')
            data = eol.show_photos(setid, chunk, 0)
            after = 0
            header = eol.get_metadata(setid)
        else:
            return render_template('loader.html')

    # Debug
    # print setid, after, len(data)

    images = []

    for i, d in enumerate(data):
        url = d['thumb']
        iid = after + i
        images.append({"id": iid, "url": url, "m": d['m'], "r": d['r'], "f":d['f']})

    # Simulate netowork delay
    #time.sleep(0.85)
    return render_template('loader.html', header=header
                                        , setid=setid
                                        , images=images)

@app.route("/about.html")
def about():
    sets = eol.get_photosets()
    n = eol.count_photos()
    return render_template('about.html', sitename=GLOBALS["sitename"]
                                       , title="About This Site"
                                       , links=[{"title": "All Images", "url": "/"}]
                                       , photosets=sets
                                       , nphotos=n)

if __name__ == "__main__":
    app.run()
