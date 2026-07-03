from flask import Flask, request
from flask_cors import CORS
from dbhw import getgreeting


app = Flask(__name__)  # Creates an instance of app
CORS(app, origins=[
    "http://localhost:63342"

])



@app.route('/GetGreeting', methods=["GET"])
def GetGreeting():
    greeting = getgreeting()
    a = greeting[0]
    b = a[0]
    print(b)
    greetingdictionaries = {
        "greeting": b
    }
    return greetingdictionaries
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5006)

