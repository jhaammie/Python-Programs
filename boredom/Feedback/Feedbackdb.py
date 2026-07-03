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


def feedback(feedback):
    global connection

    try:
        query = f"INSERT INTO public.feedback(comments) VALUES ('{feedback}');"
        connection = __GetdbConn()
        cursor = connection.cursor()
        cursor.execute(query)
        rows_inserted = cursor.rowcount
        print(f"Successfully inserted {rows_inserted} row(s).")
        connection.commit()
        cursor.close()
        connection.close()
        return rows_inserted
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        connection.close()
        return -1
