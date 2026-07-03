import os
import time
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

def InsertData(Skola, Studievag, AntagningspoangPrelim, MedelsvardePrelim, AntagningspoangSlut, MedelvardeSlut, Antagningspoangreservng, medelvardeReserv):
    try:
        connection = __GetdbConn()
        cursor = connection.cursor()
        sql = ('insert into public."2023"'
               '("Skola", "Studieväg", "AntagningspoängPrelim", "MedelsvärdePrelim", "AntagningspoängSlut", "MedelvärdeSlut", "Antagningspoängreservng", "medelvärdeReserv") '
               'values (%s, %s, %s, %s, %s, %s, %s, %s)')
        val = (Skola, Studievag, AntagningspoangPrelim, MedelsvardePrelim, AntagningspoangSlut, MedelvardeSlut, Antagningspoangreservng, medelvardeReserv)
        cursor.execute(sql, val)

        connection.commit()


    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            # print('Database connection closed.')


def GetCountOfDistinctSchools():
    data = 0
    try:
        query = "select count(distinct \"Skola\") from reygothenburggymnasium where \"Skola\" not in (select distinct skola from uniqueschools)"
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
    return data[0][0]

def GetListOfSchoolNames(pagenumber, pagesize):
    data = []
    offset = pagenumber*pagesize
    try:
        query = f"select distinct \"Skola\" from reygothenburggymnasium where \"Skola\" not in (select distinct skola from uniqueschools) order by \"Skola\" limit {pagesize} offset {offset}"
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

def InsertSchool(schoolname, latitude, longitude):
    try:
        connection = __GetdbConn()
        cursor = connection.cursor()
        sql = "insert into public.uniqueschools(skola, latitude, longitude) values(%s, %s, %s)"

        val = (schoolname, latitude, longitude)
        cursor.execute(sql, val)

        connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()

def getSchools(latitude, longitude, radius, pageno, pagesize, sortby, sortOrder, minfinMerit, maxfinMerit, programs, year):
    time.sleep(5)
    try:
        connection = __GetdbConn()
        cursor = connection.cursor()
        joined_str = "|".join(programs)
        sql = f"select \"Skola\", \"Studieväg\", \"AntagningspoängPrelim\", \"MedelsvärdePrelim\", \"AntagningspoängSlut\", \"MedelvärdeSlut\", \"Antagningspoängreservng\", \"medelvärdeReserv\", \"år\", ST_DistanceSphere(ST_MakePoint({longitude}, {latitude}), ST_MakePoint(longitude, latitude)) / 1000 as distance_in_km from uniqueschools inner join reygothenburggymnasium on uniqueschools.skola = reygothenburggymnasium.\"Skola\" where ST_DistanceSphere(ST_MakePoint({longitude}, {latitude}), ST_MakePoint(longitude, latitude)) / 1000 <= {radius} and \"AntagningspoängSlut\" > {minfinMerit} and \"AntagningspoängSlut\" < {maxfinMerit} and \"år\" in ({year}) and \"Studieväg\" ~* '^({joined_str})' order by {sortby} {sortOrder} limit {pagesize} offset {pagesize*pageno};"
        print(sql)
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        return data
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()


