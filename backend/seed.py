import json
import meilisearch

client = meilisearch.Client("http://127.0.0.1:7700")

index = client.index("documents")

# Load scraped data
with open("crawler/scraped_data.json", "r", encoding="utf-8") as file:
    documents = json.load(file)

# Clear existing documents
index.delete_all_documents()

# Add fresh crawler data
task = index.add_documents(documents)

print(f"{len(documents)} documents added successfully!")
print(task)