import psycopg2


def db_cursor():
    conn = psycopg2.connect('host=127.0.0.1 port=5432 user=postgres password=123 dbname=p-bank')
    conn.autocommit = True
    cursor = conn.cursor()

    return cursor
