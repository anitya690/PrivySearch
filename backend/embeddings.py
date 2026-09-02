import json
from sentence_transformers import SentenceTransformer

# Load scraped documents
with open("crawler/scraped_data.json", "r", encoding="utf-8") as file:
    documents = json.load(file)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create text for embedding
texts = [
    f"{doc['title']}. {doc['description']}"
    for doc in documents
]

# Generate embeddings
embeddings = model.encode(
    texts,
    show_progress_bar=True
)

print("Documents:", len(documents))
print("Embedding shape:", embeddings.shape)