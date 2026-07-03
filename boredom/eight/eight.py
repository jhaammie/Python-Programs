from flask import Flask
from flask_cors import CORS
from eightdb import getlikes, addlikestodb


app = Flask(__name__)  # Creates an instance of app
CORS(app, origins=[
    "http://localhost:63342"

])

@app.route('/likes', methods=['GET'])
def gettingnumberoflikes():
    aaa = getlikes()
    a = aaa[0]
    b = a[0]
    print(b)
    return str(b)
# gettingnumberoflikes()

@app.route('/likes', methods=['POST'])
def addlikes():
    g = addlikestodb()
    return str(g)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5006)

