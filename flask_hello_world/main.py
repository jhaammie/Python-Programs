from flask import Flask

app = Flask(__name__)

@app.route('/hello')
def hello_world():
    return 'Hello, World from Python Backend!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)