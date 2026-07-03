import json
from flask import Flask, request
from flask_cors import CORS
from dbpffft import pffft


app = Flask(__name__)  # Creates an instance of app
CORS(app, origins=[
    "http://localhost:63342"

])

@app.route('/getfruit', methods=['GET'])
def log_activity():

    aaa = pffft()
    fruit = []
    for i in range(0, len(aaa)):
        a = aaa[i]
        b = a[1]
        fruit.append(b)
    jsonArray = json.dumps(fruit)
    return jsonArray

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5006)