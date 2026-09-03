import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Load documents
with open("crawler/scraped_data.json", "r", encoding="utf-8") as file:
    documents = json.load(file)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Prepare text
texts = [
    f"{doc['title']}. {doc['description']}"
    for doc in documents
]

# Generate embeddings
embeddings = model.encode(
    texts,
    show_progress_bar=True
)

# Convert to float32 for FAISS
embeddings = np.array(embeddings).astype("float32")

# Create FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])

# Add embeddings
index.add(embeddings)

# Save index
faiss.write_index(index, "documents.index")

print("FAISS index created successfully!")
print("Documents:", len(documents))
print("Vectors:", index.ntotal)
print("Dimensions:", embeddings.shape[1])