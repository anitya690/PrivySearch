import psycopg2


connection = psycopg2.connect(
    host="127.0.0.1",
    port=5433,
    database="privysearch",
    user="privysearch",
    password="privysearch123"
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