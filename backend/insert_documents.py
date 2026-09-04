import json
import os
import psycopg2


# Load combined documents
with open(
    "crawler/all_documents.json",
    "r",
    encoding="utf-8"
) as file:
    documents = json.load(file)


# PostgreSQL connection
connection = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST", "127.0.0.1"),
    port=int(os.getenv("POSTGRES_PORT", "5433")),
    database=os.getenv("POSTGRES_DB", "privysearch"),
    user=os.getenv("POSTGRES_USER", "privysearch"),
   password=os.environ["POSTGRES_PASSWORD"]
)

cursor = connection.cursor()


# Insert documents
for doc in documents:

    source = (
        "MDN"
        if "developer.mozilla.org" in doc["url"]
        else "Python Docs"
    )

    cursor.execute(
        """
        INSERT INTO documents
        (id, title, url, source, description)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id)
        DO UPDATE SET
            title = EXCLUDED.title,
            url = EXCLUDED.url,
            source = EXCLUDED.source,
            description = EXCLUDED.description;
        """,
        (
            doc["id"],
            doc["title"],
            doc["url"],
            source,
            doc["description"]
        )
    )


connection.commit()

print(
    f"{len(documents)} documents inserted successfully!"
)


cursor.close()
connection.close()