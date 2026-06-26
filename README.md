# 🧪 Qdrant Vector DB – Mastery Experiments

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Qdrant](https://img.shields.io/badge/Qdrant-1.12%2B-brightgreen)](https://qdrant.tech/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

> **A structured, hands-on repository for mastering Qdrant—from basic CRUD to production-grade RAG and hybrid search.**

---

## 📖 Overview

This repository is your **complete learning companion** for [Qdrant](https://qdrant.tech/), the high-performance vector database.

Instead of scattered snippets, this repo provides a **progressive, phase-based curriculum**. Each script builds upon the last, taking you from a complete beginner to confidently building scalable, AI-powered retrieval systems.

**By the end of this journey, you will have executed 10 core experiments covering:**

- ✅ Basic CRUD & Payload Management
- ✅ Advanced Filtering (Geo, Range, Nested)
- ✅ Hybrid Search (Dense + Sparse BM42)
- ✅ Retrieval-Augmented Generation (RAG) Pipelines
- ✅ Performance Optimization (Quantization)
- ✅ Production Maintenance (Snapshots & Backup)

---

## 🏛️ System Architecture

The repository is designed to switch seamlessly between local development (Docker), in-memory testing, and Qdrant Cloud.

![System Architecture](architecture.png)

*Figure: High-level architecture showing how your experiments interact with Qdrant locally or in the cloud.*

### How an Experiment Executes

Every script follows this exact workflow to ensure reliability:

1. **Initialize** – The experiment script loads environment variables and connects to Qdrant via the client factory.
2. **Setup** – The script creates a collection (if it doesn't already exist) with the correct vector size and distance metric.
3. **Data Injection** – It generates synthetic data or loads real datasets, then upserts vectors and payloads in batches.
4. **Query** – The script embeds your search query (or uses raw vectors) and sends a search/recommendation request.
5. **Process** – Qdrant returns the top-K nearest neighbors with scores and metadata.
6. **Display** – Results are printed to the console and optionally logged for later analysis.

---

## 📂 Repository Structure

This modular structure ensures you can reuse the client, embedders, and synthetic data across all experiments.

```text
qdrant-experiments/
├── .env.example                 # Template for environment variables
├── .gitignore                   # Python, env, and data ignores
├── docker-compose.yml           # Spin up Qdrant instantly
├── pyproject.toml               # Modern Python dependency management
├── Makefile                     # Shortcuts (e.g., `make run-exp EX=05`)
├── README.md                    # This file!
│
├── config/                      # Global settings
│   └── settings.py              # Loads URLs, API keys, vector dimensions
│
├── src/                         # Reusable core library
│   ├── __init__.py
│   ├── client_factory.py        # Returns Qdrant client (local/cloud/memory)
│   ├── embedding_utils.py       # Wrappers for Sentence-Transformers
│   └── synthetic_data.py        # Generate dummy vectors & fake payloads
│
├── experiments/                 # 📌 THE MAIN LEARNING PATH
│   ├── 01_basic_crud.py
│   ├── 02_search_and_filter.py
│   ├── 03_batch_upsert_scroll.py
│   ├── 04_payload_indexing.py
│   ├── 05_geo_filtering.py
│   ├── 06_recommendation_api.py
│   ├── 07_hybrid_search_bm42.py
│   ├── 08_rag_text_embeddings.py
│   ├── 09_quantization_benchmark.py
│   └── 10_snapshots_backup.py
│
├── notebooks/
│   └── exploration.ipynb        # Visualize vectors & debugging
├── data/                        # Static datasets (e.g., Quora, Wiki snippets)
│   └── .gitkeep
├── tests/                       # Pytest suite to validate connections
│   ├── test_client.py
│   └── test_basic_flow.py
└── scripts/
    └── cleanup_collections.py   # Nuke all collections to start fresh

🚀 Quick Start (Get Running in 5 Minutes)
1. Prerequisites
Python 3.9+

Docker Desktop (for local Qdrant)

(Optional) uv for ultra-fast dependency management

2. Clone & Setup
bash
git clone https://github.com/your-username/qdrant-experiments.git
cd qdrant-experiments

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .          # or 'uv pip install -e .' if using uv
3. Environment Variables
Copy the environment template and configure your Qdrant Cloud credentials (optional).

bash
cp .env.example .env
.env.example:

ini
# Local default (Docker)
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_URL=http://localhost:6333

# For Qdrant Cloud (uncomment and fill in)
# QDRANT_URL=https://your-cluster.cloud.qdrant.io
# QDRANT_API_KEY=your-secret-api-key
4. Launch Qdrant (Docker)
bash
docker-compose up -d
This runs Qdrant on http://localhost:6333 with persistent storage in ./qdrant_storage.

5. Run Your First Experiment!
bash
python experiments/01_basic_crud.py
You should see output confirming collection creation, upsert, and search results.

🗺️ The Experiment Roadmap
Follow these scripts in order for maximum learning. Each experiment builds on concepts from the previous one.

Phase 1: Foundations (CRUD & Core Concepts)
#	Script	What You'll Learn
01	basic_crud.py	Creating collections, inserting points, fetching by ID, and deleting.
02	search_and_filter.py	Vector similarity search + basic must filters on payloads.
03	batch_upsert_scroll.py	Batch processing for 10k+ vectors and pagination using scroll().
Phase 2: Advanced Querying & Business Logic
#	Script	What You'll Learn
04	payload_indexing.py	Speeding up filtered queries using Qdrant's Payload Indexing.
05	geo_filtering.py	Geospatial queries: finding points within a radius or bounding box.
06	recommendation_api.py	Using positive/negative examples for "more like this, but less like that".
Phase 3: Modern AI Patterns (RAG & Hybrid)
#	Script	What You'll Learn
07	hybrid_search_bm42.py	Configuring Sparse Vectors and combining BM42 with dense semantic search.
08	rag_text_embeddings.py	Chunking text, generating embeddings with Sentence-Transformers, and building a mini RAG pipeline.
Phase 4: Production & Performance Tuning
#	Script	What You'll Learn
09	quantization_benchmark.py	Compressing vectors (Scalar/Binary) to save RAM and measuring recall loss.
10	snapshots_backup.py	Creating, deleting, and restoring collections from disaster-recovery snapshots.
🛠️ Advanced Usage & Automation
We provide a Makefile to save you keystrokes:

bash
# Run any experiment
make run-exp EX=08

# Run the full test suite
make test

# Destroy all collections and start fresh
make reset
Running in Qdrant Cloud
Switch from local to cloud by changing one line in your .env file. The src/client_factory.py will automatically handle the API key authentication.

Jupyter Notebooks
Use the notebooks/exploration.ipynb to visualize vector distributions using PCA/t-SNE and debug why certain searches return specific results.

🧪 Testing
Maintain code reliability with pytest:

bash
pytest tests/ -v
The tests check:

If the Qdrant client can connect.

If collection creation/drop works.

If a basic search returns the correct shape of results.

🤝 Contributing
Found a bug? Want to add an experiment (e.g., "Multitenancy with Partitioning")?

Fork the repository.

Create your feature branch (git checkout -b feature/amazing-feature).

Commit your changes (git commit -m 'Add some amazing feature').

Push to the branch (git push origin feature/amazing-feature).

Open a Pull Request.

📚 Further Reading
Official Qdrant Documentation

Qdrant Cloud Free Tier

Sentence-Transformers Docs
