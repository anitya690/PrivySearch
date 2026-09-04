# 🔐 PrivySearch

> Privacy-first semantic search engine built with React, FastAPI, Meilisearch, FAISS, Sentence Transformers, PostgreSQL, and Scrapy.

PrivySearch is a privacy-conscious search engine designed to return relevant results without building permanent search-history profiles or requiring user identification.

The project combines **keyword retrieval**, **semantic search**, and **hybrid ranking** over a curated technical documentation corpus.

---

## 🚀 Features

- 🔎 Semantic search using Sentence Transformers
- ⚡ Keyword search using Meilisearch
- 🧠 Vector search using FAISS
- 🔀 Hybrid ranking combining keyword and semantic relevance
- 🗄️ PostgreSQL document metadata storage
- 🕷️ Scrapy-based documentation crawler
- 🔒 Privacy-by-design architecture
- 📊 Search evaluation and latency benchmarking
- 🎯 Top-1 and Top-3 relevance evaluation
- 📈 P50 and P95 latency measurements
- 💻 React + Tailwind-inspired dark UI
- 🐳 Docker-based infrastructure

---

## 🏗️ Architecture

```text
                    ┌──────────────────┐
                    │   React Frontend │
                    │  Search + UI     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   FastAPI API    │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
       ┌────────────┐ ┌────────────┐ ┌──────────────┐
       │ Meilisearch│ │    FAISS   │ │  PostgreSQL  │
       │  Keyword   │ │  Semantic  │ │  Metadata    │
       │   Search   │ │   Search   │ │   Storage    │
       └──────┬─────┘ └──────┬─────┘ └──────────────┘
              │              │
              └──────┬───────┘
                     ▼
              ┌──────────────┐
              │Hybrid Ranking│
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │ Search Results│
              └──────────────┘


Scrapy Crawler
      │
      ▼
Curated Documentation
      │
      ├──────────────► Meilisearch
      │
      ├──────────────► FAISS
      │
      └──────────────► PostgreSQL
      