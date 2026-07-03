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


def updateemail(oldemail, newemail):
    global connection

    try:
        query = f"UPDATE public.ooof SET email='{newemail}' WHERE email='{oldemail}';"
        connection = __GetdbConn()
        cursor = connection.cursor()
        cursor.execute(query)
        rows_updated = cursor.rowcount
        print(f"Successfully updated {rows_updated} row(s).")
        connection.commit()
        cursor.close()
        connection.close()
        return rows_updated
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        connection.close()
        return -1

def getfirstemail():
    global connection
    data = []
    try:
        query = f"SELECT email FROM public.ooof where id = 1;"
        connection = __GetdbConn()
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        cursor.close()
        connection.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        connection.close()

    return data