import requests
import json
import faiss
from sentence_transformers import SentenceTransformer
import meilisearch


API_URL = "http://127.0.0.1:8000/api/search"


# =============================
# Load Documents
# =============================

with open("crawler/scraped_data.json", "r", encoding="utf-8") as file:
    documents = json.load(file)


# =============================
# Meilisearch
# =============================

client = meilisearch.Client("http://127.0.0.1:7700")
index = client.index("documents")


# =============================
# FAISS
# =============================

model = SentenceTransformer("all-MiniLM-L6-v2")
vector_index = faiss.read_index("documents.index")


# =============================
# Test Cases
# =============================

test_cases = [
    {
        "query": "how to handle errors in Python",
        "expected": "8. Errors and Exceptions"
    },
    {
        "query": "how to create a Python class",
        "expected": "9. Classes"
    },
    {
        "query": "how to work with lists",
        "expected": "5. Data Structures"
    },
    {
        "query": "how to import modules",
        "expected": "6. Modules"
    },
    {
        "query": "how to read and write files",
        "expected": "7. Input and Output"
    },
    {
        "query": "how to use virtual environments",
        "expected": "12. Virtual Environments and Packages"
    },
    {
        "query": "how to use the Python interpreter",
        "expected": "2. Using the Python Interpreter"
    },
    {
        "query": "how to take input from a user",
        "expected": "7. Input and Output"
    },
    {
        "query": "what are exceptions in Python",
        "expected": "8. Errors and Exceptions"
    },
    {
        "query": "how to control program flow",
        "expected": "4. More Control Flow Tools"
    }
]


keyword_top1 = 0
keyword_top3 = 0

semantic_top1 = 0
semantic_top3 = 0

hybrid_top1 = 0
hybrid_top3 = 0


print("=" * 70)
print("PrivySearch Retrieval Comparison")
print("=" * 70)


for test in test_cases:

    query = test["query"]
    expected = test["expected"]

    # =============================
    # Keyword Search
    # =============================

    keyword_response = index.search(
        query,
        {"limit": 3}
    )

    keyword_titles = [
        doc["title"]
        for doc in keyword_response["hits"]
    ]


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

    semantic_titles = []

    for idx in indices[0]:

        if idx != -1:
            semantic_titles.append(
                documents[idx]["title"]
            )


    # =============================
    # Hybrid Search via API
    # =============================

    response = requests.get(
        API_URL,
        params={"query": query}
    )

    response.raise_for_status()

    hybrid_data = response.json()

    hybrid_titles = [
        result["title"]
        for result in hybrid_data.get("results", [])
    ]


    # =============================
    # Keyword Metrics
    # =============================

    if keyword_titles:

        if keyword_titles[0] == expected:
            keyword_top1 += 1

        if expected in keyword_titles[:3]:
            keyword_top3 += 1


    # =============================
    # Semantic Metrics
    # =============================

    if semantic_titles:

        if semantic_titles[0] == expected:
            semantic_top1 += 1

        if expected in semantic_titles[:3]:
            semantic_top3 += 1


    # =============================
    # Hybrid Metrics
    # =============================

    if hybrid_titles:

        if hybrid_titles[0] == expected:
            hybrid_top1 += 1

        if expected in hybrid_titles[:3]:
            hybrid_top3 += 1


    # =============================
    # Display Query
    # =============================

    print(f"\nQuery: {query}")
    print(f"Expected: {expected}")

    print(
        f"Keyword Top-1: "
        f"{keyword_titles[0] if keyword_titles else 'None'}"
    )

    print(
        f"Semantic Top-1: "
        f"{semantic_titles[0] if semantic_titles else 'None'}"
    )

    print(
        f"Hybrid Top-1: "
        f"{hybrid_titles[0] if hybrid_titles else 'None'}"
    )


# =============================
# Final Results
# =============================

total = len(test_cases)


keyword_top1_accuracy = (
    keyword_top1 / total
) * 100

keyword_top3_accuracy = (
    keyword_top3 / total
) * 100


semantic_top1_accuracy = (
    semantic_top1 / total
) * 100

semantic_top3_accuracy = (
    semantic_top3 / total
) * 100


hybrid_top1_accuracy = (
    hybrid_top1 / total
) * 100

hybrid_top3_accuracy = (
    hybrid_top3 / total
) * 100


print("\n")
print("=" * 70)
print("FINAL COMPARISON")
print("=" * 70)

print(
    f"\nKeyword Search"
    f"\nTop-1 Accuracy: {keyword_top1_accuracy:.2f}%"
    f"\nTop-3 Accuracy: {keyword_top3_accuracy:.2f}%"
)

print(
    f"\nSemantic Search"
    f"\nTop-1 Accuracy: {semantic_top1_accuracy:.2f}%"
    f"\nTop-3 Accuracy: {semantic_top3_accuracy:.2f}%"
)

print(
    f"\nHybrid Search"
    f"\nTop-1 Accuracy: {hybrid_top1_accuracy:.2f}%"
    f"\nTop-3 Accuracy: {hybrid_top3_accuracy:.2f}%"
)

print("\n" + "=" * 70)