import os
from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "hello"


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    app.debug = True
    app.run()
