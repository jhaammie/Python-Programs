from flask import Flask, request
from flask_cors import CORS
import os
import psycopg2
# Defining app
app = Flask(__name__)  # Creates an instance of app
CORS(app)

def __GetdbConn():
    connection = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        host=os.getenv("HOST")
    )
    return connection

# Defining the path and method
@app.route('/GetSchoolNames', methods=["GET"])
# Defining the function 'GetSchoolNames'
def GetSchoolNames():

    # Creating an argument called name
    name = request.args.get('search_query')

    # If there is no name then I'm throwing an error
    if name is None:
        return "Please enter a valid argument"

    # Otherwise I'm returning the following statement
    return {"name":matchinggg(name)}

def matchinggg(name):
    data = []
    try:
        query = f"select distinct \"Skola\" from \"2018\" where \"Skola\" ilike '%{name}%'"
        connection = __GetdbConn()
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
        # print('Database connection closed.')
    return data


# http://127.0.0.1:5006/GetSchoolNames?search_query=anna
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5006)
