import psycopg2


def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="esercizio",
        user="postgres",
        password="root356595")
