import psycopg2

def db_test():
    return {"data": "test"}

def db_init():
    connection = psycopg2.connect(database="test", user="postgres", password="postgres", host="pg", port=5432)
    cursor = connection.cursor()
    init_db_table(connection, cursor)
    return cursor

def db_get_img(cursor,id,fields="*"):
    cursor.execute("SELECT " + fields + " FROM doc_uri WHERE id=" + id + " LIMIT 1;")
    record = cursor.fetchone()
    if record:
        return record
    else:
        return None 

def db_get_img_url(cursor,id):
    return db_get_img(cursor,id)[1]


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError
import io

def print_to_string(*args, **kwargs):
    output = io.StringIO()
    print(*args, file=output, **kwargs)
    contents = output.getvalue()
    output.close()
    return contents

# Initialize the database table if it doesn't exist
def init_db_table(connection,cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doc_uri (
            id SERIAL PRIMARY KEY,
            uri TEXT NOT NULL
        );
    """)
    connection.commit()
    # Insert a sample image URI if the table is empty
    cursor.execute("SELECT COUNT(*) FROM doc_uri;")
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute("INSERT INTO doc_uri (uri) VALUES ('https://ultralytics.com/images/bus.jpg');")
        connection.commit()
