from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import meilisearch
import faiss
import json
from sentence_transformers import SentenceTransformer
from database import get_connection


app = FastAPI(
    title="PrivySearch API",
    description="Privacy-first search engine backend",
    version="1.0.0"
)


# -----------------------------
# CORS
# -----------------------------

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
# Documents + Semantic Search
# -----------------------------

with open(
    "crawler/all_documents.json",
    "r",
    encoding="utf-8"
) as file:
    documents = json.load(file)


model = SentenceTransformer("all-MiniLM-L6-v2")

vector_index = faiss.read_index("documents.index")


# -----------------------------
# Health Check
# -----------------------------

@app.get("/api/health")
def health_check():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM documents;")
    document_count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return {
        "status": "healthy",
        "service": "PrivySearch API",
        "meilisearch": "connected",
        "faiss": "connected",
        "postgresql": "connected",
        "documents_in_db": document_count
    }
@app.get("/api/privacy")
def privacy_info():
    return {
        "privacy_by_design": True,
        "search_history": {
            "stored": False,
            "description": "Search queries are not stored as permanent user history."
        },
        "user_profiling": {
            "enabled": False,
            "description": "No user profiles are created from search activity."
        },
        "tracking": {
            "third_party_trackers": False,
            "description": "No unnecessary third-party tracking technologies are used."
        },
        "data_collection": {
            "query_storage": False,
            "user_identification": False
        }
    }


# -----------------------------
# Evaluation Report
# -----------------------------

@app.get("/api/evaluation")
def evaluation_report():

    with open(
        "evaluation/evaluation_report.json",
        "r",
        encoding="utf-8"
    ) as file:
        report = json.load(file)

    return report
# -----------------------------
# Hybrid Search
# -----------------------------

@app.get("/api/search")
def search(query: str = Query(..., min_length=1)):

    # =============================
    # Keyword Search
    # =============================

    keyword_response = index.search(
        query,
        {"limit": 3}
    )

    keyword_results = keyword_response["hits"]

    keyword_scores = [1.0, 0.67, 0.33]

    combined = {}

    for rank, doc in enumerate(keyword_results):

        doc_id = doc["id"]

        combined[doc_id] = {
            "title": doc.get("title", ""),
            "url": doc.get("url", ""),
            "description": doc.get("description", ""),
            "keyword_score": keyword_scores[rank],
            "semantic_score": 0.0
        }


    # =============================
    # Semantic Search
    # =============================

    query_embedding = model.encode(
        [query]
    ).astype("float32")

    distances, indices = vector_index.search(
        query_embedding,
        3
    )

    semantic_scores = [1.0, 0.67, 0.33]

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
                "keyword_score": 0.0,
                "semantic_score": 0.0
            }

        combined[doc_id]["semantic_score"] = semantic_scores[rank]


    # =============================
    # Hybrid Score
    # =============================

    for doc in combined.values():

        doc["hybrid_score"] = round(
            0.2 * doc["keyword_score"]
            + 0.8 * doc["semantic_score"],
            2
        )


    # =============================
    # Final Ranking
    # =============================

    results = sorted(
        combined.values(),
        key=lambda x: x["hybrid_score"],
        reverse=True
    )


    return {
        "query": query,
        "results": results
    }