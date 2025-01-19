
import psycopg2

try:
    # Connect to the movies database
    connection = psycopg2.connect(
        dbname="Movies",
        user="postgres",
        password="password",
        host="localhost"
    )

# Sort movies by name
    cursor = connection.cursor()
    cursor.execute('SELECT * from movies order by "Name"')
    data = cursor.fetchmany(8)
    print(data)

    sql = "insert into public.actors(name, movie_id) values(%s, %s)"

    val = ("Raj Kumar Rao", "3")
    cursor.execute(sql, val)

    connection.commit()

    # close the communication with the PostgreSQL
    cursor.close()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if connection is not None:
        connection.close()
        print('Database connection closed.')

