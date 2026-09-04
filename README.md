🔐 PrivySearch

Privacy-First Semantic Search Engine

PrivySearch is a privacy-conscious search engine prototype that combines keyword retrieval, semantic search, and hybrid ranking over a curated collection of technical web documents.

Instead of building user profiles or permanently storing search history, PrivySearch focuses on finding relevant information while minimizing unnecessary user data collection.

🌐 Live Demo: https://privy-search.vercel.app
💻 GitHub: https://github.com/anitya690/PrivySearch
⚙️ Backend API: https://privysearch.onrender.com

✨ Features

🔎 Keyword Search — matches query terms against document titles and descriptions.

🧠 Semantic Search — uses embeddings to find results based on meaning rather than exact words.

⚡ Hybrid Ranking — combines keyword and semantic relevance scores.

🔐 Privacy by Design — no permanent search history or user profiling.

🛡️ Privacy Center — exposes the application's privacy-related behavior through the backend API.

📊 Evaluation Dashboard — displays search quality and latency benchmark metrics.

🗄️ PostgreSQL Metadata Store — stores document metadata separately from the FAISS vector index.

🕷️ Scrapy Crawler — collects and cleans documents from selected technical documentation sources.

🚀 Cloud Deployment — React frontend deployed on Vercel and FastAPI backend deployed on Render.

🏗️ Architecture

                    ┌──────────────────────┐
                    │   React + Vite UI    │
                    │       Vercel         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     FastAPI API      │
                    │       Render         │
                    └──────────┬───────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
        Keyword Retrieval   FAISS Search   PostgreSQL
        title/description  embeddings      metadata
                │              │
                └──────┬───────┘
                       ▼
                Hybrid Ranking
                       │
                       ▼
                    Results


Scrapy Crawler
      │
      ▼
Clean + Deduplicate
      │
      ▼
all_documents.json
      │
      ├──────────────► PostgreSQL
      │
      └──────────────► FastEmbed → FAISS Index

🧰 Tech Stack

Frontend

React

Vite

CSS

Backend

Python

FastAPI

Uvicorn

Search & NLP

FastEmbed

BAAI/bge-small-en-v1.5

FAISS

Custom keyword retrieval

Hybrid ranking

Data

Scrapy

JSON document corpus

PostgreSQL

Neon

Deployment

Vercel

Render

GitHub

📚 Current Dataset

PrivySearch currently uses a curated corpus of 82 documents:

Source

Documents

MDN JavaScript documentation

65

Python documentation

17

Total

82

The current version intentionally uses a focused corpus rather than attempting to crawl the entire public web.

This makes the project lightweight, reproducible, and suitable for a portfolio-scale semantic search system.

🧠 How Search Works

For every query, PrivySearch performs two retrieval paths:

1. Keyword Retrieval

The query is tokenized and matched against document titles and descriptions.

Title matches receive a higher score than description matches.

2. Semantic Retrieval

The query is converted into an embedding using:

BAAI/bge-small-en-v1.5

FAISS then retrieves the closest document vectors.

3. Hybrid Ranking

The two signals are combined:

Hybrid Score =
    0.2 × Keyword Score
  + 0.8 × Semantic Score

The final results are sorted using the hybrid score.

🔐 Privacy Design

PrivySearch is designed around data minimization.

The application currently provides:

❌ No permanent search-history profiles

❌ No user profiling from search activity

❌ No unnecessary third-party tracking

❌ No user identification required for searching

❌ No permanent storage of search queries

The Privacy Center in the UI retrieves privacy information from the backend rather than displaying only static claims.

Privacy-conscious does not mean anonymous infrastructure. Hosting providers and standard operational infrastructure may still generate their own platform-level logs outside the application's search-history design.

📊 Evaluation

PrivySearch includes an evaluation dashboard for measuring:

Top-1 Accuracy

Top-3 Accuracy

Average Search Latency

P50 Latency

P95 Latency

Benchmark Query Count

The dashboard is available directly from the live application through the Evaluation button.

Evaluation is performed against a curated benchmark rather than claiming general web-search quality.

🌐 API Endpoints

Endpoint

Purpose

GET /api/health

Service and PostgreSQL health information

GET /api/search?query=...

Hybrid search

GET /api/privacy

Privacy configuration/status

GET /api/evaluation

Evaluation benchmark report

Interactive API documentation is available through FastAPI at:

https://privysearch.onrender.com/docs

📁 Project Structure

PrivySearch/
│
├── backend/
│   ├── crawler/
│   │   └── crawler/
│   │       └── spiders/
│   │           ├── python_docs.py
│   │           └── mdn_docs.py
│   │
│   ├── evaluation/
│   │   └── evaluation_report.json
│   │
│   ├── all_documents.json
│   ├── documents.index
│   ├── faiss_index.py
│   ├── database.py
│   ├── create_tables.py
│   ├── insert_documents.py
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── App.css
│   ├── package.json
│   └── ...
│
└── README.md

🚀 Run Locally

1. Clone

git clone https://github.com/anitya690/PrivySearch.git
cd PrivySearch

2. Backend

cd backend
python -m venv venv

Activate the virtual environment:

Windows PowerShell

.\venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Configure PostgreSQL using DATABASE_URL, then initialize the database:

python create_tables.py
python insert_documents.py

Start the API:

uvicorn main:app --reload

Backend:

http://127.0.0.1:8000

3. Frontend

Open another terminal:

cd frontend
npm install
npm run dev

Frontend:

http://localhost:5173

🕷️ Crawling & Indexing

The crawler collects selected technical documentation and produces the combined document corpus.

The indexing pipeline is:

Web Documentation
       ↓
Scrapy
       ↓
Clean + Deduplicate
       ↓
all_documents.json
       ↓
FastEmbed
       ↓
FAISS Index

The current corpus is intentionally limited to selected documentation sources. Expanding the corpus is a future improvement.

🎯 Why This Project?

PrivySearch was built to explore the engineering trade-offs involved in modern search systems:

lexical vs. semantic retrieval

vector indexing with FAISS

embedding model selection

hybrid ranking

document crawling and cleaning

API design with FastAPI

database-backed metadata

privacy-aware application design

retrieval evaluation and latency measurement

lightweight cloud deployment

⚠️ Current Limitations

The search corpus is currently limited to 82 curated documents.

It is not intended to compete with Google, Bing, or other large-scale web search engines.

The crawler is focused on selected technical documentation.

FAISS is currently used as a local vector index rather than a distributed vector database.

Search quality depends on the coverage and quality of the curated corpus.

Free cloud infrastructure introduces resource and cold-start limitations.

🔮 Future Improvements

Expand the curated corpus to additional high-quality technical sources.

Add incremental crawling and automatic index updates.

Improve hybrid ranking with learned or calibrated relevance scores.

Add filtering by source/topic.

Add query/result caching where privacy requirements allow it.

Improve benchmark coverage and evaluation methodology.

Explore distributed/vector-database infrastructure for larger corpora.

📌 Project Status

Status: Live & Deployed 🚀

The current production version includes:

React frontend

FastAPI backend

FastEmbed embeddings

FAISS semantic search

Keyword retrieval

Hybrid ranking

PostgreSQL metadata

Privacy Center

Evaluation Dashboard

Vercel + Render deployment

👨‍💻 Author

Anitya

Built as a learning and portfolio project focused on search systems, information retrieval, NLP, backend engineering, and privacy-aware application design.

⭐ If you find the project interesting, feel free to explore the code and live demo.