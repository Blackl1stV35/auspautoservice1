<<<<<<< HEAD
# 🔧 SP Auto Service — ระบบจัดการวัสดุสิ้นเปลือง

ระบบ Streamlit สำหรับ **อู่เอสพี ออโต้เซอร์วิส** จ.ฉะเชิงเทรา  
แทนที่การจัดการ Excel ด้วยมือ ด้วยระบบเบิก-จ่ายวัสดุแบบดิจิทัล

## ⚡ Quick Start

```bash
# 1. Clone & เข้าโฟลเดอร์
git clone <your-repo-url>
cd sp-autoservice

# 2. สร้าง virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. ติดตั้ง dependencies
pip install -r requirements.txt

# 4. รันแอป
streamlit run app.py
```

เปิดเบราว์เซอร์ไปที่ `http://localhost:8501`

## 📁 โครงสร้างโปรเจค

```
sp-autoservice/
├── app.py                  # Streamlit main app
├── src/
│   ├── etl.py              # ETL pipeline (Excel → CSV)
│   └── data_store.py       # CSV CRUD + Git commit
├── data/                   # CSV data (auto-generated, git-tracked)
├── .streamlit/config.toml  # Streamlit config
├── requirements.txt
└── README.md
```

## 🔄 วิธีใช้งาน

1. **อัปโหลด Excel** — ใช้เมนู "อัปโหลด Excel" นำไฟล์ Excel เดิม 2 ไฟล์เข้าระบบ
2. **เบิกวัสดุ** — เลือกชื่อช่าง → เลือกวัสดุ → ใส่จำนวน → ยืนยัน
3. **ดูสต็อก** — ตรวจสอบสต็อกปัจจุบัน รับวัสดุเข้าสต็อกได้
4. **รายงาน** — ดูสถิติการเบิกรายช่าง ตรวจจับความผิดปกติ

## 📝 หมายเหตุ

- ข้อมูลทั้งหมดเก็บเป็น CSV ใน `data/`
- ทุกการเปลี่ยนแปลงจะ commit อัตโนมัติไปยัง Git
- รองรับภาษาไทยทั้งระบบ
- ใช้ได้บนมือถือ/แท็บเล็ต

## 🗺️ Phase 2 (อนาคต)

- Barcode/QR Scanner
- LINE Bot แจ้งเตือน
- Supabase cloud database
=======
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

---

## ✨ Features

### 1. Automated ETL Pipeline (`src/workers/etl.py`)
- Ingests messy, historical Excel sheets using CPU Multi-Processing.
- Cleans Thai dates, extracts numerical quantities from strings, and normalizes tabular structures.
- Multithreaded chunking for rapid upload to Supabase PostgreSQL.

### 2. Real-Time LINE Bot Integration (`src/api/bot.py` & `src/nlp/nlp_engine.py`)
- Mechanics can request materials via text or **Voice Memos** directly on LINE.
- Uses **Groq (Whisper-large-v3)** for rapid Thai Speech-to-Text.
- Uses local **Ollama (Typhoon 3B)** to extract structured JSON (Employee, Material, Quantity) from natural language.

### 3. Machine Learning Engine (`src/workers/ai_engine.py`)
- **Anomaly Detection:** Scikit-Learn's *Isolation Forest* detects suspicious historical price gouging from suppliers.
- **Demand Forecasting:** *Linear Regression* predicts 7-day future material requirements based on historical burn rates.
- **Cost Optimization:** Automatically evaluates and tags the most cost-effective suppliers.

### 4. Metabase BI Dashboard
- Dockerized local Metabase instance connected to the Supabase cloud via Supavisor pooler.
- Visualizes live requisition feeds, purchase spend over time, and dedicated AI Insights.

---

## 🚀 Quick Start Guide

### 1. Environment Setup

Install the required dependencies (Python 3.12 compatible):

```bash
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Set up your `.env` file with your API keys:

```env
SUPABASE_URL="https://your-url.supabase.co"
SUPABASE_KEY="your-service-role-key"
LINE_CHANNEL_ACCESS_TOKEN="your-line-token"
LINE_CHANNEL_SECRET="your-line-secret"
GROQ_API_KEY="your-groq-key"
```

### 2. Database Preparation

To wipe the database and start fresh (if necessary):

```bash
python reset_db.py
```

### 3. Run the Architecture (Decoupled Services)

**A. Start Local AI (Ollama) in the background:**

```bash
ollama run scb10x/llama3.2-typhoon2-3b-instruct:latest
```

**B. Start the 24/7 API Server:**

```bash
python run_api.py
```

> Expose to LINE via Ngrok: `ngrok http 8000`

**C. Run the Heavy Data Workers (when needed):**

```bash
# Load Excel Data
python run_etl.py

# Run AI Analysis
python run_ai.py
```

### 4. Launch Metabase

Deploy the Metabase container using Docker:

```bash
docker-compose up -d
```

Access your dashboards at `http://localhost:3001`.
>>>>>>> 879dea7dcbb7a4bcd718cbfeb898016608afe155
