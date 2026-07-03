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

def getlikes():
    global connection

    try:
        query = f"select count(Likes) from likes;"
        connection = __GetdbConn()
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        cursor.close()
        connection.close()
        return data

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        connection.close()



def addlikestodb():
    global connection

    try:
        query = "INSERT INTO public.likes(\"Likes\") VALUES ('True');"
        connection = __GetdbConn()
        cursor = connection.cursor()
        cursor.execute(query)
        print(cursor.rowcount)
        connection.commit()
        cursor.close()
        rows_updated = cursor.rowcount
        connection.close()
        return rows_updated
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        connection.close()
        return -1

