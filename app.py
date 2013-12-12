import os
from flask import Flask, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)

app.debug = True

from models import *


@app.route("/")
def index():
    resp =  "db: " + os.getenv('DATABASE_URL')
    for s in PhotoSet.query.all():
        resp += "\n" + s.id + '|' +  s.date.isoformat()

    return resp


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    app.debug = True
    app.run()
