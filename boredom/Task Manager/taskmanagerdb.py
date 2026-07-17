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


def addingtask(task):
    global connection

    try:
        query = f"INSERT INTO public.\"TaskManager\"(title) VALUES ('{task}');"
        connection = __GetdbConn()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        id = cursor.fetchone()
        print(f"Successfully inserted {id} row(s).")

        cursor.close()
        connection.close()
        return id
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        connection.close()
        return -1

def gettasks():
    global connection

    try:
        query = f"SELECT id, title, is_completed FROM public.\"TaskManager\" ORDER BY id "
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

def updating(id, check):
    global connection

    try:
        query = f"UPDATE public.\"TaskManager\" SET is_completed={check} WHERE id={id};"
        connection = __GetdbConn()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        id = cursor.fetchone()
        print(f"Successfully inserted {id} row(s).")

        cursor.close()
        connection.close()
        return id
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        connection.close()
        return -1

def delete(id):
    global connection

    try:
        query = f"DELETE FROM public.\"TaskManager\" WHERE id={id};"
        connection = __GetdbConn()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        print(f"Successfully deleted {id} row(s).")

        cursor.close()
        connection.close()
        return id
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        connection.close()
        return -1
