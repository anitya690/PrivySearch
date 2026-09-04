import psycopg2

try:
    conn = psycopg2.connect(
        host="127.0.0.1",
        port=5433,
        database="privysearch",
        user="privysearch",
        password="privysearch123"
    )

    print("SUCCESS: PostgreSQL connected!")

    conn.close()

except Exception as e:
    print("FAILED:")
    print(repr(e))