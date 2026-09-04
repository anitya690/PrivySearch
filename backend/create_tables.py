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