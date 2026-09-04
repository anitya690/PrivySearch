import os
import psycopg2


connection = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST", "127.0.0.1"),
    port=int(os.getenv("POSTGRES_PORT", "5433")),
    database=os.getenv("POSTGRES_DB", "privysearch"),
    user=os.getenv("POSTGRES_USER", "privysearch"),
    password=os.environ["POSTGRES_PASSWORD"]
)

cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM documents;")
count = cursor.fetchone()[0]

print("Total documents in PostgreSQL:", count)

cursor.execute("""
    SELECT source, COUNT(*)
    FROM documents
    GROUP BY source
    ORDER BY source;
""")

print("\nDocuments by source:")

for source, total in cursor.fetchall():
    print(f"{source}: {total}")

cursor.close()
connection.close()