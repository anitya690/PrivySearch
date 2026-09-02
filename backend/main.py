from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import meilisearch

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

# Connect to local Meilisearch
client = meilisearch.Client("http://127.0.0.1:7700")

# Search index
index = client.index("documents")


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "PrivySearch API",
        "meilisearch": "connected"
    }


@app.get("/api/search")
def search(query: str = Query(..., min_length=1)):

    search_result = index.search(query)

    results = []

    for hit in search_result["hits"]:
        results.append({
            "title": hit.get("title", ""),
            "url": hit.get("url", ""),
            "description": hit.get("description", "")
        })

    return {
        "query": query,
        "results": results
    }