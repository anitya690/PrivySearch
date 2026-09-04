import os
import psycopg2


def get_connection():
    database_url = os.environ["DATABASE_URL"]

    return psycopg2.connect(database_url)