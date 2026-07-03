import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
def __GetdbConn():
    connection = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        host=os.getenv("HOST")
    )
    return connection


def gettimestamp(current_timestamp):
    global connection

    try:
        query = f"INSERT INTO uhh(purple) VALUES ('{current_timestamp}');"
        connection = __GetdbConn()
        cursor = connection.cursor()
        cursor.execute(query)

        connection.commit()
        cursor.close()
        connection.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        connection.close()


