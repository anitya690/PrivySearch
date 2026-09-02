import meilisearch

client = meilisearch.Client("http://127.0.0.1:7700")

documents = [
    {
        "id": 1,
        "title": "Python Documentation",
        "url": "https://docs.python.org/3/",
        "description": "Official documentation and resources for Python programming."
    },
    {
        "id": 2,
        "title": "FastAPI Documentation",
        "url": "https://fastapi.tiangolo.com/",
        "description": "Modern and fast web framework for building APIs with Python."
    },
    {
        "id": 3,
        "title": "Machine Learning Basics",
        "url": "https://scikit-learn.org/",
        "description": "Introduction to machine learning algorithms and data analysis."
    },
    {
        "id": 4,
        "title": "Data Analytics Guide",
        "url": "https://pandas.pydata.org/",
        "description": "Learn data analysis and manipulation using Python and pandas."
    },
    {
        "id": 5,
        "title": "Privacy Preserving Machine Learning",
        "url": "https://en.wikipedia.org/wiki/Privacy-preserving_machine_learning",
        "description": "Techniques for applying machine learning while protecting sensitive information."
    }
]

index = client.index("documents")

task = index.add_documents(documents)

print("Documents added successfully!")
print(task)
