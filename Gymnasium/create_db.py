import psycopg2
from Hahahaha import PopulateLocation
from data.DataInsertionScript import insert_data_from_excel
from dotenv import load_dotenv
import os

load_dotenv()

def create_gymnasium_table():
    try:
       
        # Connect to the gymnasium database
        connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST")
        )
        cursor = connection.cursor()

        # Create the gymnasium table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS public.gymnasium
        (
            id SERIAL PRIMARY KEY,
            "år" SMALLINT NOT NULL,
            "är_preliminär" BOOLEAN NOT NULL,
            kommun VARCHAR(50) NOT NULL,
            skola VARCHAR(50) NOT NULL,
            "studievägskod" VARCHAR(20) NOT NULL,
            "studieväg" VARCHAR(200) NOT NULL,
            "antagningsgräns" DOUBLE PRECISION NOT NULL,
            median DOUBLE PRECISION NOT NULL,
            antal_platser SMALLINT NOT NULL,
            antagna SMALLINT NOT NULL,
            reserver SMALLINT NOT NULL,
            lediga_platser SMALLINT NOT NULL,
            organistionsform VARCHAR,
            CONSTRAINT gymnasium_year_program UNIQUE ("år", "är_preliminär", skola, "studievägskod", "studieväg")
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Table 'gymnasium' created successfully.")

    except (Exception, psycopg2.Error) as error:
        print(f"Error while working with PostgreSQL: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed.")

# Create the school table
def create_school_table():
    try:
        # Connect to the gymnasium database
        connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST")
        )
        cursor = connection.cursor()

        # Create the school table
        create_school_table_query = """
        CREATE TABLE IF NOT EXISTS public.school
        (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            latitude DOUBLE PRECISION NOT NULL,
            longitude DOUBLE PRECISION NOT NULL,
            CONSTRAINT fk_school_name FOREIGN KEY (name) REFERENCES public.gymnasium(skola)
        )
        """
        cursor.execute(create_school_table_query)
        connection.commit()
        print("Table 'school' created successfully.")

    except (Exception, psycopg2.Error) as error:
        print(f"Error while working with PostgreSQL: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed.")

def add_postgis_extension():
    try:
        # Connect to the gymnasium database
        connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST")
        )
        cursor = connection.cursor()

        # Add the PostGIS extension
        add_extension_query = "CREATE EXTENSION IF NOT EXISTS postgis;"
        cursor.execute(add_extension_query)
        connection.commit()
        print("PostGIS extension added successfully.")

    except (Exception, psycopg2.Error) as error:
        print(f"Error while working with PostgreSQL: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed.")         

if __name__ == "__main__":
    create_gymnasium_table()
    create_school_table()
    add_postgis_extension()
    insert_data_from_excel()
    # PopulateLocation()
