import json

from flask import Flask, request
from flask_cors import CORS
from updateemaildb import updateemail, getfirstemail


app = Flask(__name__)  # Creates an instance of app
CORS(app, origins=[
    "http://localhost:63342"

])

@app.route('/updateemail', methods=['PUT'])
def email():
    data = request.get_json()
    print(data)
    newemail = data.get('updateemail')
    oldemail = data.get('oldemail')

    if newemail == '' or newemail.isspace() == True:
        return 0
    elif oldemail == '' or oldemail.isspace() == True:
        return 0


    a = updateemail(oldemail, newemail)
    return str(a)

@app.route('/getemail', methods=['GET'])
def gettingoriginalemail():
    print("abc")
    aaa = getfirstemail()
    print(aaa)
    a = aaa[0]
    print(a)
    b = a[0]
    print(b)
    emaildictionary = {
        "email": b
    }
    return emaildictionary

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5006)

