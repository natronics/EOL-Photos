import os
from flask import Flask, request, jsonify, render_template, send_from_directory
app = Flask(__name__)

GLOBALS = {"sitename": "EOL Browser"}

@app.route("/")
def index():
    return render_template('index.html', sitename=GLOBALS["sitename"], title="Most Resent Images")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/loader.html", methods=['POST'])
def loader():
    print request.form["id"]

    images = range(6*10)
    return render_template('loader.html', images=images)

if __name__ == "__main__":
    app.debug = True
    app.run()
