from flask import Flask, request
from flask_cors import CORS
from Feedbackdb import feedback as fb


app = Flask(__name__)  # Creates an instance of app
CORS(app, origins=[
    "http://localhost:63342"

])

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.get_json()

    comments = data.get('feedback')

    if comments == '' or comments.isspace() == True:
        return 0


    a = fb(comments)
    return str(a)
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5006)