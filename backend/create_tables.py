import os
from database import get_connection
connection = get_connection()
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