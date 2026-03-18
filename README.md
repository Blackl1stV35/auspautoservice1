<div align="center">

# 🚗 Auto Shop AI & Data Pipeline

**A production-ready Data Engineering and Machine Learning pipeline for automotive shop inventory and cost management.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?style=flat-square&logo=supabase&logoColor=white)](https://supabase.com/)
[![Metabase](https://img.shields.io/badge/Metabase-Analytics-509EE3?style=flat-square&logo=metabase&logoColor=white)](https://www.metabase.com/)

*Transitioning legacy Excel-based workflows into a scalable, cloud-hosted relational database with AI-driven insights.*

</div>

---

## 📖 Overview

This project modernizes an automotive shop's operational data management by replacing manual Excel workflows with a robust, automated pipeline. It features a real-time LINE Messaging Bot for floor mechanics, Automated AI Data Extraction, and advanced Machine Learning for demand forecasting and cost optimization.

## ✨ Features

1. **Automated ETL Pipeline (`etl_pipeline.py`)**
   - Ingests messy, historical Excel sheets.
   - Cleans Thai dates, extracts numerical quantities from strings, and normalizes tabular structures.
   - Multithreaded chunking for rapid upload to Supabase PostgreSQL.

2. **Real-Time LINE Bot Integration (`bot.py` & `nlp_engine.py`)**
   - Mechanics can request materials via text or **Voice Memos** directly on LINE.
   - Uses **Groq (Whisper-large-v3)** for rapid Thai Speech-to-Text.
   - Uses local **Ollama (Typhoon 3B)** to extract structured JSON (Employee, Material, Quantity) from natural language.

3. **Machine Learning Engine (`ai_engine.py`)**
   - **Anomaly Detection:** Scikit-Learn's *Isolation Forest* detects suspicious historical price gouging from suppliers.
   - **Demand Forecasting:** *Linear Regression* predicts 7-day future material requirements based on historical burn rates.
   - **Cost Optimization:** Automatically evaluates and tags the most cost-effective suppliers.

4. **Metabase BI Dashboard**
   - Dockerized local Metabase instance connected directly to the Supabase cloud.
   - Visualizes live requisition feeds, purchase spend over time, and dedicated AI Insights.

---

## 🚀 Quick Start Guide

### 1. Environment Setup
Install the required dependencies (Python 3.12 compatible):
```bash
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt