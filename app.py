import os
from flask import Flask, send_from_directory, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import eol

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)

app.debug = True

from models import *


@app.route("/")
def index():

    photos = []
    for s in PhotoSet.query.all():
        for p in s.photos:
            photos.append({'mrf': p.mission + "-" + p.roll + "-" + str(p.frame),
                'url': eol.THUMB_BASE.format(mission=p.mission, roll=p.roll, frame=p.frame)})

    return render_template('index.html', title="Recent Images From Space", photos=photos[0:100])


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    app.debug = True
    app.run()
