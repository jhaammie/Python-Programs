from flask import Flask, request
from flask_cors import CORS
from inventorylabdb import addstuff as pooff, getstuff, updating, delete

app = Flask(__name__)  # Creates an instance of app
CORS(app, origins=[
    "http://localhost:63342"

])

@app.route('/addstuff', methods=['POST'])
def addstuff():
    data = request.get_json()

    item = data.get('item')
    price = data.get('price')
    quantity = data.get('quantity')
    print(type(item), type(price), type(quantity))

    if item == '' or item.isspace() == True:
        return 0
    elif price == 0 or price.isspace() == True:
        return 0
    elif quantity == 0 or quantity.isspace() == True:
        return 0
    a = pooff(item, price, quantity)
    return str(a)

@app.route('/getstuff', methods=['GET'])
def readthetable():
    lst = []
    aaa = getstuff()
    print(aaa)
    print(aaa[0])
    print(aaa[0][1])
    for i in range (len(aaa)):
        dict = {
            "id":aaa[i][0],
            "item":aaa[i][1],
            "price":aaa[i][2],
            "quantity": aaa[i][3]
        }
        lst.append(dict)
    print(lst)
    return lst

@app.route('/stuff/<int:id>', methods=['PUT'])
def update(id):
    data = request.get_json()

    NewQuantity = data.get('NewQuantity')

    id = updating(id, NewQuantity)

    return str(id)

@app.route('/stuff/<int:id>', methods=['DELETE'])
def deleting(id):
    id = delete(id)

    return str(id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5006)

