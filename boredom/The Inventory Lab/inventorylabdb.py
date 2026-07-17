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


def addstuff(item, price, quantity):
    global connection

    try:
        query = f"INSERT INTO public.\"The_Inventory_Lab\"(item, price, quantity) VALUES ('{item}',{price},{quantity});"
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

def getstuff():
    global connection

    try:
        query = f"SELECT id, item, price, quantity FROM public.\"The_Inventory_Lab\" ORDER BY id ASC "
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

def updating(id, newquantity):
    global connection

    try:
        query = f"UPDATE public.\"The_Inventory_Lab\" SET quantity={newquantity} WHERE id={id};"
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
        query = f"DELETE FROM public.\"The_Inventory_Lab\" WHERE id={id};"
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
