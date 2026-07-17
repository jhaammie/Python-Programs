from flask import Flask, request
from flask_cors import CORS
from taskmanagerdb import addingtask, gettasks, updating, delete

app = Flask(__name__)  # Creates an instance of app
CORS(app, origins=[
    "http://localhost:63342"

])

@app.route('/addtask', methods=['POST'])
def addtask():
    data = request.get_json()

    task = data.get('title')

    if task == '' or task.isspace() == True:
        return 0
    id = addingtask(task)
    return str(id)

@app.route('/fetchingtasks', methods=['GET'])
def reusable():
    lst = []
    aaa = gettasks()
    print(aaa)
    print(aaa[0])
    print(aaa[0][1])
    for i in range (len(aaa)):
        dict = {
            "id":aaa[i][0],
            "Task":aaa[i][1],
            "Is_Completed":aaa[i][2]
        }
        lst.append(dict)
    print(lst)
    return lst

@app.route('/tasks/<int:id>', methods=['PUT'])
def check(id):
    data = request.get_json()

    checked = data.get('checked')

    id = updating(id, checked)

    return str(id)

@app.route('/tasks/<int:id>', methods=['DELETE'])
def deleting(id):
    id = delete(id)

    return str(id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5006)

