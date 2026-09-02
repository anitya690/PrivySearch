from fastapi import FastAPI,Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="PrivySearch API",
    description="Privacy-first search engine backend",
    version="1.0.0"
)

# Allow requests from our React frontend
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


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "PrivySearch API"
    }




@app.get("/api/search")
def search(query: str = Query(..., min_length=1)):
    results = [
        {
            "title": "Python Documentation",
            "url": "https://docs.python.org/3/",
            "description": "Official documentation and resources for Python.",
        },
        {
            "title": "Python Programming Guide",
            "url": "https://www.python.org/",
            "description": "Learn about Python programming, tools, and resources.",
        },
        {
            "title": "Python Tutorial",
            "url": "https://docs.python.org/3/tutorial/",
            "description": "An introduction to Python programming for beginners.",
        },
    ]

    return {
        "query": query,
        "results": results
    }