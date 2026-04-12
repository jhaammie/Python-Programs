from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:63344"

])


@app.route('/api/hello')
def hello_world():
    return 'Hello, World from Python Backend!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)