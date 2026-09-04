import os
import psycopg2


def get_connection():

    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return psycopg2.connect(database_url)

    return psycopg2.connect(
        host="127.0.0.1",
        port=5433,
        database="privysearch",
        user="privysearch",
        password="privysearch123"
    )