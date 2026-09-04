from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import faiss
import json
import os
import re
from pathlib import Path
from fastembed import TextEmbedding
from database import get_connection


# -----------------------------
# Base Directory
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent


# -----------------------------
# Environment Variables
# -----------------------------

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173"
)


# -----------------------------
# FastAPI
# -----------------------------

app = FastAPI(
    title="PrivySearch API",
    description="Privacy-first semantic search engine",
    version="1.0.0"
)


# -----------------------------
# CORS
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL,
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Load Documents
# -----------------------------

DOCUMENTS_FILE = (
    BASE_DIR
    / "crawler"
    / "all_documents.json"
)

FAISS_INDEX_FILE = (
    BASE_DIR
    / "documents.index"
)


with open(
    DOCUMENTS_FILE,
    "r",
    encoding="utf-8"
) as file:
    documents = json.load(file)


# -----------------------------
# FastEmbed
# -----------------------------

embedding_model = TextEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)


# -----------------------------
# FAISS
# -----------------------------

vector_index = faiss.read_index(
    str(FAISS_INDEX_FILE)
)


# -----------------------------
# Keyword Search
# -----------------------------

def keyword_search(query, limit=3):

    query_words = set(
        re.findall(
            r"\b\w+\b",
            query.lower()
        )
    )

    scored_documents = []

    for doc in documents:

        title = doc.get(
            "title",
            ""
        ).lower()

        description = doc.get(
            "description",
            ""
        ).lower()

        text = f"{title} {description}"

        score = 0

        for word in query_words:

            if word in title:
                score += 3

            if word in description:
                score += 1

        if score > 0:
            scored_documents.append(
                (score, doc)
            )

    scored_documents.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [
        doc
        for score, doc in scored_documents[:limit]
    ]


# -----------------------------
# Health Check
# -----------------------------

@app.get("/api/health")
def health_check():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM documents;"
    )

    document_count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return {
        "status": "healthy",
        "service": "PrivySearch API",
        "keyword_search": "connected",
        "faiss": "connected",
        "postgresql": "connected",
        "documents_in_db": document_count
    }


# -----------------------------
# Privacy
# -----------------------------

@app.get("/api/privacy")
def privacy_info():

    return {
        "privacy_by_design": True,

        "search_history": {
            "stored": False,
            "description": (
                "Search queries are not stored as permanent "
                "user history."
            )
        },

        "user_profiling": {
            "enabled": False,
            "description": (
                "No user profiles are created from "
                "search activity."
            )
        },

        "tracking": {
            "third_party_trackers": False,
            "description": (
                "No unnecessary third-party tracking "
                "technologies are used."
            )
        },

        "data_collection": {
            "query_storage": False,
            "user_identification": False
        }
    }


# -----------------------------
# Evaluation
# -----------------------------

@app.get("/api/evaluation")
def evaluation_report():

    evaluation_file = (
        BASE_DIR
        / "evaluation"
        / "evaluation_report.json"
    )

    with open(
        evaluation_file,
        "r",
        encoding="utf-8"
    ) as file:
        report = json.load(file)

    return report


# -----------------------------
# Hybrid Search
# -----------------------------

@app.get("/api/search")
def search(
    query: str = Query(..., min_length=1)
):

    # =============================
    # Keyword Search
    # =============================

    keyword_results = keyword_search(
        query,
        limit=3
    )

    keyword_scores = [
        1.0,
        0.67,
        0.33
    ]

    combined = {}

    for rank, doc in enumerate(
        keyword_results
    ):

        doc_id = doc["id"]

        combined[doc_id] = {
            "title": doc.get(
                "title",
                ""
            ),
            "url": doc.get(
                "url",
                ""
            ),
            "description": doc.get(
                "description",
                ""
            ),
            "keyword_score": keyword_scores[
                rank
            ],
            "semantic_score": 0.0
        }


    # =============================
    # Semantic Search
    # =============================

    query_embedding = list(
        embedding_model.embed(
            [query]
        )
    )[0]

    query_embedding = (
        query_embedding
        .astype("float32")
        .reshape(1, -1)
    )

    distances, indices = (
        vector_index.search(
            query_embedding,
            3
        )
    )

    semantic_scores = [
        1.0,
        0.67,
        0.33
    ]

    for rank, idx in enumerate(
        indices[0]
    ):

        if idx == -1:
            continue

        doc = documents[idx]

        doc_id = doc["id"]

        if doc_id not in combined:

            combined[doc_id] = {
                "title": doc.get(
                    "title",
                    ""
                ),
                "url": doc.get(
                    "url",
                    ""
                ),
                "description": doc.get(
                    "description",
                    ""
                ),
                "keyword_score": 0.0,
                "semantic_score": 0.0
            }

        combined[doc_id][
            "semantic_score"
        ] = semantic_scores[rank]


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
        key=lambda x: x[
            "hybrid_score"
        ],
        reverse=True
    )


    return {
        "query": query,
        "results": results
    }