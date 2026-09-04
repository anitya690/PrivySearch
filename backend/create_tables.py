import psycopg2


connection = psycopg2.connect(
    host="127.0.0.1",
    port=5433,
    database="privysearch",
    user="privysearch",
    password="privysearch123"
)

cursor = connection.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS documents (
    id VARCHAR(100) PRIMARY KEY,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    source VARCHAR(50),
    description TEXT
);
""")


connection.commit()

print("Documents table created successfully!")


cursor.close()
connection.close()