from datetime import datetime

from flask import Flask, request
from flask_cors import CORS
from dbuhh import gettimestamp


app = Flask(__name__)  # Creates an instance of app
CORS(app, origins=[
    "http://localhost:63342"

])


@app.route('/LogActivity', methods=["POST"])
def timestamp():
    current_timestamp = datetime.now()
    gettimestamp(current_timestamp)

    return ""

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5006)