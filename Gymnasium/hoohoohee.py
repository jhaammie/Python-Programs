import psycopg2

def __GetdbConn():
    connection = psycopg2.connect(
        dbname="gymnasium",
        user="postgres",
        password="password",
        host="localhost"
    )
    return connection

def GetListOfSchoolNames(pagenumber, pagesize):
    data = []
    offset = pagenumber*pagesize
    try:
        query = f"select distinct skola from gymnasium order by skola limit {pagesize} offset {offset}"
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
        query = "select count (distinct skola) from gymnasium"
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


def GetDataForSchools(lst):
    placeholders = ",".join(f"'{name}'" for name in lst)
    data = []
    try:
        query = f"select * from gymnasium where skola in ({placeholders})"
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
