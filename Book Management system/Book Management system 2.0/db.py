import psycopg2


def __GetdbConn():
    connection = psycopg2.connect(
        dbname="bms",
        user="postgres",
        password="password",
        host="localhost"
    )
    return connection


def insertbook(NameOfBook, AuthorOfBook):

    try:
        connection = __GetdbConn()
        cursor = connection.cursor()
        sql = "insert into public.books(title, author) values(%s, %s)"

        val = (NameOfBook, AuthorOfBook)
        cursor.execute(sql, val)

        connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection closed.')


def SortBooks(by):
    data = []
    try:
        query = "select * from books"
        if by == "title":
            query = 'SELECT * from books order by "title"'
        elif by == "author":
            query = 'SELECT * from books order by "author"'
        connection = __GetdbConn()
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        print(data)

        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection closed.')
    return data


def exists(TitleOfBook, AuthorOfBook):
    data = True
    try:
        query = f"SELECT EXISTS(SELECT  * from books WHERE author = '{AuthorOfBook}' and title='{TitleOfBook}')"
        connection = __GetdbConn()
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        print(f"{query}: QUERY")

        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection closed.')
    return data[0]
