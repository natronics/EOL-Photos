import os
from flask import Flask, jsonify, render_template, send_from_directory
app = Flask(__name__)

GLOBALS = {"sitename": "EOL Browser"}

@app.route("/")
def index():
    return render_template('index.html', sitename=GLOBALS["sitename"], title="Most Resent Images")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.debug = True
    app.run()
