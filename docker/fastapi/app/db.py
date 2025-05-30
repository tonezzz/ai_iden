import psycopg2

def test():
    return {"data": "test"}

def open():
    connection = psycopg2.connect(database="test", user="postgres", password="postgres", host="pg", port=5432)
    cursor = connection.cursor()
    #init_db(cursor)

    return cursor