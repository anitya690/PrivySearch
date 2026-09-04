import os
import psycopg2


try:
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "127.0.0.1"),
        port=int(os.getenv("POSTGRES_PORT", "5433")),
        database=os.getenv("POSTGRES_DB", "privysearch"),
        user=os.getenv("POSTGRES_USER", "privysearch"),
       password=os.environ["POSTGRES_PASSWORD"]
    )

    print("SUCCESS: PostgreSQL connected!")

    conn.close()

except Exception as e:
    print("FAILED:")
    print(repr(e))