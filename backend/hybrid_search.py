import json
import faiss
import meilisearch
from sentence_transformers import SentenceTransformer


# Load documents
with open("crawler/scraped_data.json", "r", encoding="utf-8") as file:
    documents = json.load(file)


# Meilisearch
client = meilisearch.Client("http://127.0.0.1:7700")
index = client.index("documents")


# FAISS + embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")
vector_index = faiss.read_index("documents.index")


# User query
query = input("Enter your search query: ")


# -----------------------------
# Keyword Search
# -----------------------------

keyword_response = index.search(query, {"limit": 3})

keyword_results = keyword_response["hits"]


# -----------------------------
# Semantic Search
# -----------------------------

query_embedding = model.encode([query]).astype("float32")

distances, indices = vector_index.search(
    query_embedding,
    3
)


# -----------------------------
# Combine Results
# -----------------------------

combined = {}


# Add keyword results
for rank, doc in enumerate(keyword_results):

    doc_id = doc["id"]

    combined[doc_id] = {
        "title": doc.get("title", ""),
        "url": doc.get("url", ""),
        "description": doc.get("description", ""),
        "keyword_score": 3 - rank,
        "semantic_score": 0
    }


# Add semantic results
for rank, idx in enumerate(indices[0]):

    if idx == -1:
        continue

    doc = documents[idx]
    doc_id = doc["id"]

    if doc_id not in combined:
        combined[doc_id] = {
            "title": doc["title"],
            "url": doc["url"],
            "description": doc["description"],
            "keyword_score": 0,
            "semantic_score": 0
        }

    combined[doc_id]["semantic_score"] = 3 - rank


# -----------------------------
# Hybrid Score
# -----------------------------

for doc in combined.values():

    doc["hybrid_score"] = (
        0.5 * doc["keyword_score"]
        + 0.5 * doc["semantic_score"]
    )


# Sort by hybrid score
results = sorted(
    combined.values(),
    key=lambda x: x["hybrid_score"],
    reverse=True
)


# -----------------------------
# Display Results
# -----------------------------

print("\nHybrid Search Results:\n")

for rank, result in enumerate(results, start=1):

    print(f"{rank}. {result['title']}")
    print(f"URL: {result['url']}")
    print(f"Hybrid Score: {result['hybrid_score']:.2f}")
    print()
    