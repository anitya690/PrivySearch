import json
import numpy as np
import faiss
from fastembed import TextEmbedding


# -----------------------------
# Load documents
# -----------------------------

with open(
    "crawler/all_documents.json",
    "r",
    encoding="utf-8"
) as file:
    documents = json.load(file)


# -----------------------------
# Load FastEmbed model
# -----------------------------

model = TextEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)


# -----------------------------
# Prepare text
# -----------------------------

texts = [
    f"{doc['title']}. {doc['description']}"
    for doc in documents
]


# -----------------------------
# Generate embeddings
# -----------------------------

embeddings = list(
    model.embed(texts)
)


# -----------------------------
# Convert to NumPy float32
# -----------------------------

embeddings = np.array(
    embeddings
).astype("float32")


# -----------------------------
# Create FAISS index
# -----------------------------

index = faiss.IndexFlatL2(
    embeddings.shape[1]
)


# -----------------------------
# Add embeddings
# -----------------------------

index.add(embeddings)


# -----------------------------
# Save index
# -----------------------------

faiss.write_index(
    index,
    "documents.index"
)


print("FAISS index created successfully!")
print("Documents:", len(documents))
print("Vectors:", index.ntotal)
print("Dimensions:", embeddings.shape[1])