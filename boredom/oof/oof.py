from flask import Flask, request
from flask_cors import CORS
from dboof import oof


app = Flask(__name__)  # Creates an instance of app
CORS(app, origins=[
    "http://localhost:63342"

])

@app.route('/LogActivity', methods=['POST'])
def log_activity():

    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    print(f"Received Login - Email: {email}, Password: {password}")
    oof(email, password)

    return email
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5006)