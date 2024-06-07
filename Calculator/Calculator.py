

# Simple flask application
# Importing what I need
from flask import Flask, request
from flask_cors import CORS
# Defining app
app = Flask(__name__)  # Creates an instance of app
CORS(app)


# Defining the path and method
@app.route('/', methods=["GET"])
# Defining a function 'options'
def options():
    # Returning a list of things you can do

    return ("<h1>You can take the following paths:</h1>"
            "<br/>"
            "/hello?(name=your name) "
            "<br/>"
            "/add?(n1=...&n2=...) "
            "<br/>"
            "/sub?(n1=...&n2=...) "
            "<br/>"
            "/mul?(n1=...&n2=...) "
            "<br/>"
            "/div?(n1=...&n2=...) ")

# Defining the path and the method


@app.route('/hello', methods=["GET"])
# Defining the function 'hello'
def hello():

    # Creating an argument called name
    name = request.args.get('name')

    # If there is no name then I'm throwing an error
    if name is None:
        return "Please enter a valid argument"

    # Otherwise I'm returning the following statement
    return f"Hello {name}"
 

# Defining the path and method
@app.route('/add', methods=["GET"])
# Defining the function 'add'
def add():

    # Defining the argument for the first integer
    n1 = request.args.get('n1', '')

    # Defining the argument for the second integer
    n2 = request.args.get('n2', '')

    # If n1 and n2 are digits
    if n1.isdigit() and n2.isdigit():

        # Adding the numbers and returning the sum
        SumOfIntegers = int(n1) + int(n2)
        return str(SumOfIntegers)

    # Otherwise returning an error
    else:
        return "Please enter an integer."


# Defining the path and method
@app.route('/sub', methods=["GET"])
# Defining a function called 'sub'
def sub():

    # Defining the argument for the first integer
    n1 = request.args.get('n1', '')

    # Defining the argument for the second integer
    n2 = request.args.get('n2', '')

    # If n1 and n2 are digits
    if n1.isdigit() and n2.isdigit():

        # Subtracting the numbers and returning the difference
        DifferenceBetweenIntegers = int(n1) - int(n2)
        return str(DifferenceBetweenIntegers)

    # Otherwise throwing an error
    else:
        return "Please enter an integer."


# Defining the path and method
@app.route('/mul', methods=["GET"])
def mul():

    # Defining the argument for the first integer
    n1 = request.args.get('n1', '')

    # Defining the argument for the second integer
    n2 = request.args.get('n2', '')

    # If n1 and n2 are digits
    if n1.isdigit() and n2.isdigit():

        # Multiplying the numbers and returning the product
        ProductOfIntegers = int(n1) * int(n2)
        return str(ProductOfIntegers)
    else:
        return "Please enter an integer."


# Defining the path and method
@app.route('/div', methods=["GET"])
def div():

    # Defining the argument for the first integer
    n1 = request.args.get('n1', '')

    # Defining the argument for the second integer
    n2 = request.args.get('n2', '')

    # If n1 and n2 are digits
    if n1.isdigit() and n2.isdigit():

        if int(n2) == 0:
            return "Undefined"

        # Diving the numbers and returning the quotient
        QuotientOfIntegers = int(n1) / int(n2)
        return str(QuotientOfIntegers)

    # Otherwise throwing an error
    else:
        return "Please enter an integer."


if __name__ == "__main__":

    # Defining the IP of the host and making debugging possible
    app.run(debug=True, host='0.0.0.0')
