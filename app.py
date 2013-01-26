import os
from flask import Flask, request, jsonify, render_template, send_from_directory
import time
app = Flask(__name__)

GLOBALS = {"sitename": "EOL Browser"}

@app.route("/")
def index():
    return render_template('index.html', sitename=GLOBALS["sitename"]
                                       , title="Database of ISS Photographs"
                                       , links=[{"title": "About", "url": "/about.html"}])

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/loader.html", methods=['POST'])
def loader():
    try:
        after = int(request.form["after"])
    except:
        after = 0

    print "after:", after

    images = []
    for image in xrange(6*10):
        url = "/static/img/ISS031-E-146394.jpg"
        iid = after + image
        images.append({"id": iid, "url": url})

    # Simulate netowork delay
    time.sleep(1.85)
    return render_template('loader.html', images=images)

@app.route("/about.html")
def about():
    return render_template('about.html', sitename=GLOBALS["sitename"]
                                       , title="About This Site"
                                       , links=[{"title": "Image Gallery", "url": "/"}])

if __name__ == "__main__":
    app.debug = True
    app.run()
