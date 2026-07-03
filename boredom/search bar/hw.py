from flask import Flask, request
from flask_cors import CORS
from dbhw import searchbar as search


app = Flask(__name__)  # Creates an instance of app
CORS(app, origins=[
    "http://localhost:63342"

])



@app.route('/searchbar', methods=["GET"])
def searchbar():
    a = request.args.get('search_query')
    print(a)
    b = search(a)
    """[{name:bird},
    {name:tiger},
    {name:lion}]"""
    lst = []
    for i in b:
        dictionary = {
            "name":i[0]
        }
        lst.append(dictionary)
    return lst


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5006)

