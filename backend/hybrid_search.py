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


# ==========================================
# Keyword Search
# ==========================================

keyword_response = index.search(
    query,
    {"limit": 5}
)

keyword_results = keyword_response["hits"]


# ==========================================
# Semantic Search
# ==========================================

query_embedding = model.encode([query]).astype("float32")

distances, indices = vector_index.search(
    query_embedding,
    5
)


# ==========================================
# Reciprocal Rank Fusion (RRF)
# ==========================================

combined = {}

# RRF constant
k = 60


# -----------------------------
# Keyword Results
# -----------------------------

for rank, doc in enumerate(keyword_results, start=1):

    doc_id = doc["id"]

    if doc_id not in combined:
        combined[doc_id] = {
            "title": doc.get("title", ""),
            "url": doc.get("url", ""),
            "description": doc.get("description", ""),
            "keyword_score": 0.0,
            "semantic_score": 0.0,
            "rrf_score": 0.0
        }

    combined[doc_id]["keyword_score"] = 1 / (k + rank)


# -----------------------------
# Semantic Results
# -----------------------------

for rank, idx in enumerate(indices[0], start=1):

    if idx == -1:
        continue

    doc = documents[idx]
    doc_id = doc["id"]

    if doc_id not in combined:
        combined[doc_id] = {
            "title": doc["title"],
            "url": doc["url"],
            "description": doc["description"],
            "keyword_score": 0.0,
            "semantic_score": 0.0,
            "rrf_score": 0.0
        }

    combined[doc_id]["semantic_score"] = 1 / (k + rank)


# ==========================================
# Calculate Final RRF Score
# ==========================================

for doc in combined.values():

    doc["rrf_score"] = (
        doc["keyword_score"]
        + doc["semantic_score"]
    )


# ==========================================
# Final Ranking
# ==========================================

results = sorted(
    combined.values(),
    key=lambda x: x["rrf_score"],
    reverse=True
)


# ==========================================
# Display Results
# ==========================================

print("\nHybrid Search Results (RRF):\n")

for rank, result in enumerate(results, start=1):

    print(f"{rank}. {result['title']}")
    print(f"URL: {result['url']}")
    print(
        f"Keyword RRF Score: "
        f"{result['keyword_score']:.4f}"
    )
    print(
        f"Semantic RRF Score: "
        f"{result['semantic_score']:.4f}"
    )
    print(
        f"Final RRF Score: "
        f"{result['rrf_score']:.4f}"
    )
    print()