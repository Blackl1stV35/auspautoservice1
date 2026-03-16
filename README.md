<div align="center">

# 🚗 Auto Shop AI & Data Pipeline

**A production-ready Data Engineering and Machine Learning pipeline for automotive shop inventory and cost management.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?style=flat-square&logo=supabase&logoColor=white)](https://supabase.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-IsolationForest-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)

*Transitioning legacy Excel-based workflows into a scalable, cloud-hosted relational database with AI-driven insights.*

</div>

---

## 📖 Overview

This project modernizes an automotive shop's operational data management by replacing manual Excel workflows with a robust, automated pipeline. It ingests raw multi-sheet spreadsheets, loads them into a cloud PostgreSQL database, and applies machine learning models to surface actionable insights — all exposed through a high-performance REST API.

---

## ✨ Features

| Feature | Description |
|---|---|
| ⚡ **Multi-Threaded ETL** | Parses, cleans, and unpivots messy multi-sheet Excel files using `pandas` and `concurrent.futures` |
| 🗄️ **Optimized DB Operations** | ID caching and batch insertions minimize network latency and memory overhead against PostgreSQL |
| 🤖 **AI Anomaly Detection** | `IsolationForest` (Scikit-Learn) automatically flags unusual price spikes from suppliers |
| 📈 **AI Demand Forecasting** | Meta's `Prophet` analyzes time-series transaction data to predict future material consumption |
| 🌐 **FastAPI Backend** | RESTful endpoints to trigger pipelines manually; webhook-ready for LINE Bot integrations |

---

## 📂 Project Structure

```
auto-shop-ai-pipeline/
│
├── data/                       # Raw .xlsx input files (Git-ignored)
├── src/
│   ├── __init__.py
│   ├── config.py               # Environment variables & logger setup
│   ├── db_operations.py        # Supabase caching & batch insert logic
│   ├── etl_pipeline.py         # Multi-threaded Excel data extraction
│   ├── ai_engine.py            # Prophet & Isolation Forest ML models
│   └── bot.py                  # FastAPI application & route handlers
│
├── .env.example                # Environment variable template
├── .gitignore
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- Python **3.11+**
- A [Supabase](https://supabase.com/) account (PostgreSQL)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/auto-shop-ai-pipeline.git
cd auto-shop-ai-pipeline
```

### 2. Set Up a Virtual Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy the template and fill in your Supabase credentials.

> ⚠️ **Important:** Use the **Service Role Key** to bypass Row Level Security during ETL batch inserts.

```bash
cp .env.example .env
# Then edit .env with your credentials
```

### 4. Prepare Input Data

Place your raw Excel files inside the `data/` directory. The pipeline expects:

```
data/เอสพี--สถิติเบิกวัสดุสิ้นเปลือง(69).xlsx
data/3--เอสพี--ต้นทุนแผนกสี และน้ำมัน และกิ๊บน๊อต.xlsx
```

### 5. Start the Server

```bash
uvicorn src.bot:app --reload
```

The API will be available at **`http://127.0.0.1:8000`**

### 6. Trigger the ETL Pipeline

Send a `POST` request or navigate to the endpoint in your browser:

```
http://127.0.0.1:8000/trigger-etl
```

Monitor progress in your terminal or in `pipeline.log`.

---

## 🐳 Docker Deployment

Build and run the entire pipeline inside a Docker container:

```bash
docker build -t auto-shop-ai .
docker run -p 8000:8000 --env-file .env auto-shop-ai
```

---

## 🗺️ Roadmap

- [ ] Connect FastAPI webhook to **LINE Messaging API** for real-time employee material requisitions
- [ ] Integrate **Metabase / Looker Studio** dashboards directly connected to Supabase for management reporting
- [ ] Connect **Typhoon 3B LLM** via Ollama/Groq for Natural Language Processing of voice memos

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **ETL / Data** | Python, Pandas, concurrent.futures |
| **Machine Learning** | Scikit-Learn (IsolationForest), Meta Prophet |
| **Database** | Supabase (PostgreSQL) |
| **Backend** | FastAPI, Uvicorn |
| **Containerization** | Docker |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
