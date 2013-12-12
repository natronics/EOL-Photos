import os
from flask import Flask, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)

app.debug = True


class PhotoSet(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    date = db.Column(db.Date)

    def __repr__(self):
        return '<set %r>' % self.id

@app.route("/")
def index():
    resp =  "db: " + os.getenv('DATABASE_URL')
    for s in PhotoSet.query.all():
        resp += "\n" + s

    return resp


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    app.debug = True
    app.run()
