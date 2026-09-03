import json
import meilisearch


client = meilisearch.Client("http://127.0.0.1:7700")

index = client.index("documents")


# Load all documents
with open("crawler/all_documents.json", "r", encoding="utf-8") as file:
    documents = json.load(file)


# Clear existing documents
index.delete_all_documents()


# Add fresh documents
task = index.add_documents(documents)


print(f"{len(documents)} documents added successfully!")
print(task)