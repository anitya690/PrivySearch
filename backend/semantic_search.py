import json
import faiss
from sentence_transformers import SentenceTransformer

# Load documents
with open("crawler/scraped_data.json", "r", encoding="utf-8") as file:
    documents = json.load(file)

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
index = faiss.read_index("documents.index")

# User query
query = input("Enter your search query: ")

# Convert query into embedding
query_embedding = model.encode([query]).astype("float32")

# Search top 3 similar documents
distances, indices = index.search(query_embedding, 3)

print("\nSemantic Search Results:\n")

for rank, idx in enumerate(indices[0], start=1):
    doc = documents[idx]

    print(f"{rank}. {doc['title']}")
    print(f"URL: {doc['url']}")
    print(f"Distance: {distances[0][rank - 1]:.4f}")
    print()