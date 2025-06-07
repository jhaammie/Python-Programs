import os
import yaml
from datetime import datetime
from typing import Optional, Tuple, List, Any

import psycopg2

# ============= Database Configuration =============
with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)
    db_config = config.get('database', {})

DB_USER = db_config.get('DB_USER', 'postgres')
DB_PASSWORD = db_config.get('DB_PASSWORD', '')
DB_NAME = db_config.get('DB_NAME', 'gymnasium')
DB_HOST = db_config.get('DB_HOST', 'localhost')
DB_PORT = db_config.get('DB_PORT', '5432')

# ============= Database Connection =============
def get_db_connection():
    """Create and return a new database connection."""
    return psycopg2.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME
    )

def __GetdbConn():
    """Legacy connection function - use get_db_connection() instead."""
    return get_db_connection()

# ============= User Management =============
def CreateUser(user_id: str, email: str, password: str, first_name: str, last_name: str, created_at: datetime) -> str:
    """Create a new user in the database."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (id, email, password, first_name, last_name, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (user_id, email, password, first_name, last_name, created_at, created_at))
            user_id = cur.fetchone()[0]
            conn.commit()
            return user_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def GetUserByEmail(email: str) -> Optional[Tuple[Any, ...]]:
    """Get user by email address."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, email, password, first_name, last_name, created_at, updated_at
                FROM users
                WHERE email = %s
            """, (email,))
            return cur.fetchone()
    finally:
        conn.close()

def GetUserById(user_id: str) -> Optional[Tuple[Any, ...]]:
    """Get user by ID."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, email, password, first_name, last_name, created_at, updated_at
                FROM users
                WHERE id = %s
            """, (user_id,))
            return cur.fetchone()
    finally:
        conn.close()

def UpdateUser(user_id: str, email: str, password: Optional[str], first_name: str, last_name: str, updated_at: datetime) -> bool:
    """Update user information."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            if password:
                cur.execute("""
                    UPDATE users
                    SET email = %s, password = %s, first_name = %s, last_name = %s, updated_at = %s
                    WHERE id = %s
                """, (email, password, first_name, last_name, updated_at, user_id))
            else:
                cur.execute("""
                    UPDATE users
                    SET email = %s, first_name = %s, last_name = %s, updated_at = %s
                    WHERE id = %s
                """, (email, first_name, last_name, updated_at, user_id))
            conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def SaveUserData(user_id, prelim_score, favorite_schools):
    """Save user's prelim score and favorite schools."""
    try:
        connection = __GetdbConn()
        cursor = connection.cursor()
        
        query = """
            INSERT INTO user_data (user_id, prelim_score, favorite_schools)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id) 
            DO UPDATE SET 
                prelim_score = EXCLUDED.prelim_score,
                favorite_schools = EXCLUDED.favorite_schools;
        """
        cursor.execute(query, (user_id, prelim_score, favorite_schools))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False

def GetUserData(user_id):
    """Get user's prelim score and favorite schools."""
    try:
        connection = __GetdbConn()
        cursor = connection.cursor()
        query = "SELECT prelim_score, favorite_schools FROM user_data WHERE user_id = %s;"
        cursor.execute(query, (user_id,))
        data = cursor.fetchone()
        cursor.close()
        connection.close()
        return data
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None

# ============= School Management =============
def GetListOfSchoolNames(pagenumber, pagesize):
    """Get paginated list of school names."""
    data = []
    offset = pagenumber*pagesize
    try:
        query = f"select distinct skola from gymnasium where skola not in (select distinct name from school) order by skola limit {pagesize} offset {offset}"
        connection = __GetdbConn()
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        connection.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return data

def InsertSchool(schoolname, latitude, longitude):
    """Insert a new school into the database."""
    try:
        connection = __GetdbConn()
        cursor = connection.cursor()
        sql = "insert into public.school(name, latitude, longitude) values(%s, %s, %s)"
        val = (schoolname, latitude, longitude)
        cursor.execute(sql, val)
        connection.commit()
        connection.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def GetCountOfDistinctSchools():
    """Get count of distinct schools not yet in the school table."""
    data = 0
    try:
        query = "select count(distinct skola) from gymnasium where skola not in (select distinct name from school)"
        connection = __GetdbConn()
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        connection.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return data[0][0]

def GetNearestSchools(latitude, longitude, count):
    """Get nearest schools to given coordinates."""
    data = []
    try:
        query = f"select name, ST_DistanceSphere(ST_MakePoint({longitude}, {latitude}), ST_MakePoint(school2.longitude, school2.latitude)) / 1000 as distance_in_km from school as school2 order by distance_in_km asc limit {count}"
        connection = __GetdbConn()
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        connection.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return data

def GetSchoolLocation(school_name):
    """Get school location coordinates."""
    data = None
    try:
        query = """
            SELECT 
                latitude,
                longitude
            FROM school 
            WHERE name = %s;
        """
        connection = __GetdbConn()
        cursor = connection.cursor()
        cursor.execute(query, (school_name,))
        data = cursor.fetchone()
        cursor.close()
        connection.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return data

# ============= School Data and Predictions =============
def GetDataForSchools(lst, sortby, sortOrder, minpreMerit=0, minfinMerit=0, maxpreMerit=1000, maxfinMerit=1000,
                      programs=None, year=None):
    """Get detailed data for specified schools with filtering options."""
    if programs is None:
        programs = []
    placeholders = ",".join(f"'{name}'" for name in lst)
    data = []
    query = f"select * from prelim_final_gymnasium where skola in ({placeholders})"
    try:
        if programs is not None:
            joined_str = "|".join(programs)
            query = f"{query} and studieväg ~* '^({joined_str})' "

        if year is not None:
            query = f"{query} and år = {year}"
        query = f"{query} and antagningsgräns_prelim between {minpreMerit} and {maxpreMerit}"
        query = f"{query} and (antagningsgräns_final between {minfinMerit} and {maxfinMerit} or antagningsgräns_final is null)"
        if sortby is not None:
            query = f"{query} order by {sortby} {sortOrder}"
        
        connection = __GetdbConn()
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        connection.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return data

def GetGymnasiumWithinRadius(latitude, longitude, radius, page_number, page_size):
    """Get paginated list of schools within specified radius."""
    offset = page_number * page_size
    data = []
    total_count = 0
    try:
        count_query = f"""
            SELECT COUNT(*) 
            FROM school 
            WHERE ST_DistanceSphere(
                ST_MakePoint({longitude}, {latitude}),
                ST_MakePoint(school.longitude, school.latitude)
            ) / 1000 <= {radius};
        """
        
        data_query = f"""
            SELECT 
                name,
                ST_DistanceSphere(
                    ST_MakePoint({longitude}, {latitude}),
                    ST_MakePoint(school.longitude, school.latitude)
                ) / 1000 as distance_in_km 
            FROM school 
            WHERE ST_DistanceSphere(
                ST_MakePoint({longitude}, {latitude}),
                ST_MakePoint(school.longitude, school.latitude)
            ) / 1000 <= {radius} 
            ORDER BY distance_in_km ASC 
            LIMIT {page_size} 
            OFFSET {offset};
        """
        connection = __GetdbConn()
        cursor = connection.cursor()
        
        cursor.execute(count_query)
        total_count = cursor.fetchone()[0]
        
        cursor.execute(data_query)
        data = cursor.fetchall()
        cursor.close()
        connection.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return data, total_count

def GetSchoolHistoricalData(school_name):
    """Get historical data for a specific school."""
    data = []
    try:
        query = """
            SELECT 
                år,
                studieväg,
                antagningsgräns_prelim,
                antagningsgräns_final,
                median_prelim,
                median_final,
                antal_platser_prelim,
                antal_platser_final,
                antagna_prelim,
                antagna_final,
                reserver_prelim,
                reserver_final,
                lediga_platser_prelim,
                lediga_platser_final,
                organistionsform,
                kommun
            FROM prelim_final_gymnasium 
            WHERE skola = %s
            ORDER BY år DESC, studieväg;
        """
        connection = __GetdbConn()
        cursor = connection.cursor()
        cursor.execute(query, (school_name,))
        data = cursor.fetchall()
        cursor.close()
        connection.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return data

def PredictSchools(prelim_score, year=None):
    """Predict suitable schools based on prelim score."""
    data = []
    try:
        query = """
            WITH RankedSchools AS (
                SELECT 
                    skola,
                    studieväg,
                    antagningsgräns_prelim,
                    antagningsgräns_final,
                    median_prelim,
                    median_final,
                    antal_platser_prelim,
                    antal_platser_final,
                    antagna_prelim,
                    antagna_final,
                    reserver_prelim,
                    reserver_final,
                    lediga_platser_prelim,
                    lediga_platser_final,
                    organistionsform,
                    kommun,
                    ROW_NUMBER() OVER (
                        PARTITION BY skola, studieväg 
                        ORDER BY år DESC
                    ) as rn
                FROM prelim_final_gymnasium
                WHERE antagningsgräns_prelim <= %s
        """
        params = [prelim_score]
        
        if year:
            query += " AND år = %s"
            params.append(year)
            
        query += """
            )
            SELECT * FROM RankedSchools 
            WHERE rn = 1
            ORDER BY antagningsgräns_prelim DESC
            LIMIT 25;
        """
        
        connection = __GetdbConn()
        cursor = connection.cursor()
        cursor.execute(query, params)
        data = cursor.fetchall()
        cursor.close()
        connection.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return data

def PredictSchoolsWithinRadius(prelim_score, latitude, longitude, radius, year=None):
    """Predict suitable schools within radius based on prelim score."""
    data = []
    try:
        query = """
            WITH RankedSchools AS (
                SELECT 
                    p.skola,
                    p.studieväg,
                    p.antagningsgräns_prelim,
                    p.antagningsgräns_final,
                    p.median_prelim,
                    p.median_final,
                    p.antal_platser_prelim,
                    p.antal_platser_final,
                    p.antagna_prelim,
                    p.antagna_final,
                    p.reserver_prelim,
                    p.reserver_final,
                    p.lediga_platser_prelim,
                    p.lediga_platser_final,
                    p.organistionsform,
                    p.kommun,
                    s.latitude,
                    s.longitude,
                    ST_DistanceSphere(
                        ST_MakePoint(%s, %s),
                        ST_MakePoint(s.longitude, s.latitude)
                    ) / 1000 as distance_in_km,
                    ROW_NUMBER() OVER (
                        PARTITION BY p.skola, p.studieväg 
                        ORDER BY p.år DESC
                    ) as rn
                FROM prelim_final_gymnasium p
                JOIN school s ON p.skola = s.name
                WHERE p.antagningsgräns_prelim <= %s
                AND ST_DistanceSphere(
                    ST_MakePoint(%s, %s),
                    ST_MakePoint(s.longitude, s.latitude)
                ) / 1000 <= %s
        """
        params = [longitude, latitude, prelim_score, longitude, latitude, radius]
        
        if year:
            query += " AND p.år = %s"
            params.append(year)
            
        query += """
            )
            SELECT * FROM RankedSchools 
            WHERE rn = 1
            ORDER BY antagningsgräns_prelim DESC, distance_in_km ASC
            LIMIT 25;
        """
        
        connection = __GetdbConn()
        cursor = connection.cursor()
        cursor.execute(query, params)
        data = cursor.fetchall()
        cursor.close()
        connection.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return data

"""print(GetListOfSchoolNames(0, 2))
print(InsertSchool("S:t Botvids Gymnasium", "33.8", "88.99"))
"""
