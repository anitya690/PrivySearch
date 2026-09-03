from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import meilisearch
import faiss
import json
from sentence_transformers import SentenceTransformer


app = FastAPI(
    title="PrivySearch API",
    description="Privacy-first search engine backend",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Meilisearch
# -----------------------------

client = meilisearch.Client("http://127.0.0.1:7700")
index = client.index("documents")


# -----------------------------
# Semantic Search
# -----------------------------

with open("crawler/scraped_data.json", "r", encoding="utf-8") as file:
    documents = json.load(file)

model = SentenceTransformer("all-MiniLM-L6-v2")

vector_index = faiss.read_index("documents.index")


# -----------------------------
# Health Check
# -----------------------------

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "PrivySearch API",
        "meilisearch": "connected",
        "faiss": "connected"
    }


# -----------------------------
# Search
# -----------------------------

@app.get("/api/search")
def search(query: str = Query(..., min_length=1)):

    # Keyword search
    keyword_result = index.search(query)

    keyword_results = []

    for hit in keyword_result["hits"]:
        keyword_results.append({
            "title": hit.get("title", ""),
            "url": hit.get("url", ""),
            "description": hit.get("description", "")
        })


    # Semantic search
    query_embedding = model.encode([query]).astype("float32")

    distances, indices = vector_index.search(
        query_embedding,
        3
    )

    semantic_results = []

    for idx, distance in zip(indices[0], distances[0]):

        if idx == -1:
            continue

        doc = documents[idx]

        semantic_results.append({
            "title": doc["title"],
            "url": doc["url"],
            "description": doc["description"],
            "distance": float(distance)
        })


    return {
        "query": query,
        "keyword_results": keyword_results,
        "semantic_results": semantic_results
    }