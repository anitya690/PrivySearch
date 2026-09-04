from database import get_connection


connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    SELECT id, title, source
    FROM documents
    LIMIT 5;
""")

rows = cursor.fetchall()

print("Documents from PostgreSQL:\n")

for row in rows:
    print(row)

cursor.close()
connection.close()