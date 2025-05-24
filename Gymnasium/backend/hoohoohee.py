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

def GetListOfSchoolNames(pagenumber, pagesize):
    data = []
    offset = pagenumber*pagesize
    try:
        query = f"select distinct skola from gymnasium where skola not in (select distinct name from school) order by skola limit {pagesize} offset {offset}"
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
        sql = "insert into public.school(name, latitude, longitude) values(%s, %s, %s)"

        val = (schoolname, latitude, longitude)
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
        query = "select count(distinct skola) from gymnasium where skola not in (select distinct name from school)"
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

def GetNearestSchools(latitude, longitude,count):
    data = []
    try:
        query = f"select name, ST_DistanceSphere(ST_MakePoint({longitude}, {latitude}), ST_MakePoint(school2.longitude, school2.latitude)) / 1000 as distance_in_km from school as school2 order by distance_in_km asc limit {count}"
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


def GetDataForSchools(lst, sortby, sortOrder, minpreMerit=0, minfinMerit=0, maxpreMerit=1000, maxfinMerit=1000,
                      programs=None, year=None):

    if programs is None:
        programs = []
    placeholders = ",".join(f"'{name}'" for name in lst)
    data = []
    query = f"select * from prelim_final_gymnasium where skola in ({placeholders})"
    try:

        if programs is not None:
            joined_str = "|".join(programs)
            query = f"{query} and studieväg ~* '^({joined_str})' "

        # ASK NISHA HOW 'NONE' IS POSSIBLE
        # EXPLAnATION FOR PROGRAMs
        if year is not None:
            query = f"{query} and år = {year}"
        query = f"{query} and antagningsgräns_prelim between {minpreMerit} and {maxpreMerit}"
        query = f"{query} and (antagningsgräns_final between {minfinMerit} and {maxfinMerit} or antagningsgräns_final is null)"
        if sortby is not None:
            query = f"{query} order by {sortby} {sortOrder}"
        print(query)
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

def GetGymnasiumWithinRadius(latitude, longitude, radius):
    data = []
    try:
        query = f"select name, ST_DistanceSphere(ST_MakePoint({longitude}, {latitude}), ST_MakePoint(school.longitude, school.latitude)) / 1000 as distance_in_km from school where ST_DistanceSphere(ST_MakePoint({longitude}, {latitude}), ST_MakePoint(school.longitude, school.latitude)) / 1000 <= {radius} order by distance_in_km asc;"
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


"""print(GetListOfSchoolNames(0, 2))
print(InsertSchool("S:t Botvids Gymnasium", "33.8", "88.99"))
"""
