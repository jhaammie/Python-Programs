from flask import Flask, request
from flask_cors import CORS
from gemini import askgemini

app = Flask(__name__)  # Creates an instance of app
CORS(app, origins=[
    "http://localhost:63342"

])

@app.route('/askai', methods=['POST'])
def feedback():
    data = request.get_json()
    print(data)
    interesting = data.get('askai')

    if interesting == '' or interesting.isspace() == True:
        return 0
    a = askgemini(interesting)
    return a
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5006)