import json


PYTHON_DATA = "crawler/scraped_data.json"
MDN_DATA = "crawler/mdn_data.json"
OUTPUT_DATA = "crawler/all_documents.json"


# Load Python documentation
with open(PYTHON_DATA, "r", encoding="utf-8") as file:
    python_docs = json.load(file)


# Load MDN documentation
with open(MDN_DATA, "r", encoding="utf-8") as file:
    mdn_docs = json.load(file)


# Merge both datasets
all_documents = python_docs + mdn_docs


# Remove duplicate IDs
unique_documents = {}

for document in all_documents:
    unique_documents[document["id"]] = document


all_documents = list(unique_documents.values())


# Save merged dataset
with open(OUTPUT_DATA, "w", encoding="utf-8") as file:
    json.dump(
        all_documents,
        file,
        ensure_ascii=False,
        indent=2
    )


print("Data merge completed!")
print(f"Python documents: {len(python_docs)}")
print(f"MDN documents: {len(mdn_docs)}")
print(f"Total unique documents: {len(all_documents)}")