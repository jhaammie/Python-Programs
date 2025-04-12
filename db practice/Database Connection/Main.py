
"""

Making/getting the connection from python

"""

import psycopg2

try:
    # Connect to the movies database
    connection = psycopg2.connect(
        dbname="bms",
        user="postgres",
        password="password",
        host="localhost"
    )

# Sort movies by name
# Cursor = db. When you execute something it points to the temporary memory the result is stored in
    cursor = connection.cursor()
    cursor.execute('SELECT * from books order by "title"')
    data = cursor.fetchmany(1)
    print(data)

    sql = "insert into public.books(title, author) values(%s, %s)"

# Inserting into the table from python
    val = ("Harry potter", "JK rowling")
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

