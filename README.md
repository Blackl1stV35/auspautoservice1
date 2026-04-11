# 🔧 SP Auto Service — ระบบจัดการวัสดุสิ้นเปลือง

**อู่เอสพี ออโต้เซอร์วิส** จ.ฉะเชิงเทรา (Eastern Economic Corridor)  
Streamlit web application for consumable materials management — replacing manual Excel workflows with a digital issuance, tracking, and cost intelligence system.

## What Changed from v2.1.2

| Area | v2.1.2 (Phase 1) | v4.0 (Current) |
|---|---|---|
| **Backend** | CSV files + Git auto-commit/push | Supabase PostgreSQL (cloud) |
| **Performance** | Full CSV reload on every page | `@st.cache_data` + SQL views — pages load <3s |
| **Cost Analysis** | None | Full 5-tab cost & supplier intelligence page |
| **Forecasting** | None | 3-month moving average cost forecast with budget alerts |
| **Price Monitoring** | None | Automated price spike detection (SQL `LAG()` window) |
| **Backup** | Auto-saved messy CSVs | On-demand "Backup Clean Excel" button |
| **Git dependency** | Required Git installed + PAT token | Removed entirely — zero Git dependency |

---

## Features

### Core Operations
- **เบิกวัสดุ (Material Issuance)** — dropdown-based form for mechanics, with real-time stock display, duplicate prevention (120s window), and UUID transaction IDs
- **สต็อกวัสดุ (Stock Management)** — current levels with 4-tier color coding (🔴🟠🟡🟢), search, and receive-stock form
- **อัปโหลด Excel (ETL)** — ingests the original messy Thai Excel files, handles "5+5+" notation, Buddhist Era dates, wide grids, and multi-sheet layouts

### Dashboards & Reports
- **หน้าหลัก (Home)** — KPI cards, Top 10 materials and mechanics charts, low-stock alerts
- **รายงานช่าง (Mechanic Reports)** — cumulative view, monthly comparison (grouped bars), and per-person drilldown with pie chart
- **สรุปรายเดือน (Monthly Summary)** — VBA-style accumulation pivot tables (employee × month, material × month)
- **Heatmap** — employee × material usage intensity with period filter
- **ตรวจจับความผิดปกติ (Anomaly Detection)** — Z-score based flagging, both overall and per-material, with threshold slider

### 💰 Cost & Supplier Analysis (NEW in v4)
- **Monthly cost trend** — line chart with category-stacked breakdown
- **Category breakdown** — donut + bar charts for paint, oil, nuts/bolts, lights, etc.
- **Supplier ranking** — by total spend, volume, order count, and unique items
- **Price spike detection** — flags materials with >30% price increase between consecutive purchases
- **Cost vs Usage** — purchased vs issued quantities, overstock/understock alerts
- **Cost forecast** — 3-month moving average with budget overrun warnings
- **KPI cards** — total spend, this month, YTD, average daily cost, top 3 cost drivers

### Data Integrity
- UUID transaction IDs (`SP-YYYYMMDD-HHMMSS-XXXXXX`)
- Duplicate prevention (identical mechanic + material + quantity within 120 seconds)
- NaN-safe JSON serialization (`sanitize_for_json`) for all Supabase inserts
- Full audit log with timestamp, user, action, and detail

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit 1.30+ |
| Database | Supabase PostgreSQL |
| Charts | Plotly Express + Graph Objects |
| ETL | pandas + openpyxl |
| Caching | `@st.cache_data(ttl=60)` |
| Heavy queries | PostgreSQL views (`v_monthly_cost`, `v_supplier_rank`, `v_price_history`, `v_category_cost`, `v_cost_vs_usage`, `v_employee_usage`) |

---

## Project Structure

```
sp-autoservice/
├── app.py                      # Streamlit app (10 pages)
├── src/
│   ├── data_store.py           # Supabase CRUD + caching + cost analysis
│   ├── etl.py                  # Excel → Supabase ETL pipeline
│   ├── db_schema.sql           # Base table definitions (run once)
│   └── db_views.sql            # Performance views & indexes (run once)
├── .streamlit/
│   ├── config.toml             # Streamlit theme/server config
│   └── secrets.toml            # Supabase credentials (gitignored)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Setup

### 1. Supabase Database

Go to [Supabase Dashboard](https://supabase.com/dashboard) → your project → SQL Editor:

```
-- Run db_schema.sql first (creates tables + RLS policies)
-- Then run db_views.sql (creates performance views + indexes)
```

### 2. Secrets Configuration

**Local development** — create `.streamlit/secrets.toml`:

```toml
[supabase]
url = "https://<your-project-id>.supabase.co"
key = "<your-service-role-key>"
```

**Streamlit Cloud** — paste the same content into Settings → Secrets.

> Find these at: Supabase Dashboard → Settings → API  
> `url` = Project URL, `key` = service_role secret (not anon key)

### 3. Install & Run

```bash
# Clone
git clone https://github.com/Blackl1stV35/auspautoservice1.git
cd auspautoservice1

# Virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Dependencies
pip install -r requirements.txt

# Run
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

### 4. First Use

1. Go to **📤 อัปโหลด Excel**
2. Upload the two original Excel files
3. Click **🚀 ประมวลผล → Supabase**
4. All data is now in PostgreSQL — dashboards will populate immediately

---

## Version History

| Version | Tag | Description |
|---|---|---|
| v1.0 | — | Initial CSV + local Git, basic issuance form |
| v2.0 | — | Enhanced dashboards, heatmap, monthly views, duplicate prevention |
| v2.1.2 | `v2.1.2-streamlit-phase1-optimized` | GitHub PAT push, robust Git auto-commit, all VBA features ported |
| v4.0 | *current* | Supabase PostgreSQL backend, Cost & Supplier Analysis page, `@st.cache_data` optimization, clean Excel backup, Git removed |

---

## Roadmap (Phase 2)

- Barcode / QR scanner integration for material issuance
- LINE Bot notifications (low stock alerts, daily summary)
- Role-based access control (admin vs mechanic)
- Multi-branch support
- Mobile-native PWA wrapper

---

## License

Proprietary — SP Auto Service Co., Ltd.
