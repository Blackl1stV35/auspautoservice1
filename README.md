# 🚗 SP Auto Service Management System

**Modernizing SP Auto Service Co., Ltd.** --- an independent auto repair
and body/paint garage in Chachoengsao, Thailand.

This repository documents the full evolution of the garage's internal
operations system:

- **v2.0.0-streamlit-phase1** (Current Recommended) — Modern Streamlit web app with clean ETL, stock tracking, mechanic audit trail, and Git versioning.
- **v1.5.0-vba** — Original working Excel + VBA macros (daily production use).
- **v1.0.0-original** — Early AI + LINE bot + Supabase pipeline (reference only).

------------------------------------------------------------------------

# 📋 Project Overview

SP Auto Service processes **100+ vehicles per day** with a workforce of
**40--60 technicians and staff**.\
The previous manual Excel workflow for **consumables issuance and
purchase/cost tracking** was slow, difficult to audit, and vulnerable to
waste or misuse.

This repository introduces a structured modernization path.

### What this repository provides

**Phase 1 -- Active System** - Clean **Streamlit web application** -
Automated **ETL pipeline** for the original Excel data sources - Digital
**consumable issuance system** - **Stock management** dashboard -
**Per-mechanic usage tracking** - Basic **anomaly detection for unusual
consumption**

**Original Pipeline (Legacy but included)**

The original architecture is still included for reference and
experimentation:

-   AI consumption analysis
-   LINE Bot interface
-   Supabase database integration

------------------------------------------------------------------------

# 🚀 Quick Start (Recommended -- Streamlit Phase 1)

Clone and run the modern web interface locally.

``` bash
# 1. Clone the repository
git clone https://github.com/Blackl1stV35/auspautoservice1.git
cd auspautoservice1

# 2. Create a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the Streamlit app
streamlit run app.py
```

Then open your browser:

    http://localhost:8501

------------------------------------------------------------------------

# 📁 Project Structure

    auspautoservice1/
    │
    ├── app.py                    # Main Streamlit application (Phase 1)
    ├── .streamlit/               # Streamlit configuration
    ├── data/                     # CSV/Parquet datasets (auto-managed)
    ├── src/                      # ETL pipeline and utility modules
    ├── v1-vba/                   # Original Excel + VBA system (planned archive)
    │
    ├── run_etl.py                # Legacy ETL pipeline
    ├── run_api.py                # Legacy API service
    │
    ├── requirements.txt
    ├── README.md
    └── .gitignore

------------------------------------------------------------------------

# 🔄 How the System Works (Streamlit Phase 1)

### 1️⃣ Upload Excel Data

Upload the original operational spreadsheets:

-   **สถิติเบิกวัสดุ** (Consumables issuance statistics)
-   **ต้นทุนแผนกสี** (Paint department cost tracking)

The system automatically cleans and converts them into structured
datasets.

------------------------------------------------------------------------

### 2️⃣ Issue Consumables

Mechanics can digitally request materials:

1.  Select **mechanic**
2.  Select **material**
3.  Enter **quantity**
4.  Submit request

Each transaction is logged with a **complete audit trail**.

------------------------------------------------------------------------

### 3️⃣ Stock Management

The system tracks:

-   Current inventory levels
-   Low-stock alerts
-   New purchase entries
-   Historical usage patterns

------------------------------------------------------------------------

### 4️⃣ Reports & Monitoring

Managers can view:

-   Per-mechanic material consumption
-   Top-used consumables
-   Early anomaly detection for unusual usage

------------------------------------------------------------------------

### 5️⃣ Automatic Git Versioning

Every change to the data layer is automatically tracked via **Git**,
enabling:

-   Full audit history
-   Data recovery
-   Operational transparency

------------------------------------------------------------------------

# 🗺️ Development Roadmap

### Phase 1 -- Current

-   Streamlit MVP
-   ETL pipeline for Excel files
-   Git-based version tracking

### Phase 2 -- Operations Enhancement

-   Barcode scanner support
-   Improved anomaly detection
-   Faster data ingestion

### Phase 3 -- Communication Layer

-   LINE Bot integration
-   Voice and text material requests
-   Supabase cloud database

### Phase 4 -- Intelligence Layer

-   AI forecasting for material demand
-   Automated procurement suggestions
-   Metabase operational dashboards

------------------------------------------------------------------------

# 📝 Design Principles

The system is designed with the real garage environment in mind:

-   **Mobile-friendly UI** for mechanics and supervisors
-   **Minimal training required**
-   **Full audit trail for accountability**
-   **Automatic Git backups** for operational safety

Legacy scripts remain available for teams experimenting with the full AI
pipeline.

------------------------------------------------------------------------

# 🏢 Organization

**SP Auto Service Co., Ltd.**\
Chachoengsao, Thailand

*Last Updated: April 2026*
