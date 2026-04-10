# SP Autoservice - Inventory Management System

A comprehensive inventory and material management system for mechanical spare parts operations, built with **Streamlit**, **Pandas**, and **Git-based versioning**.

![Status](https://img.shields.io/badge/Status-Active-brightgreen) ![Version](https://img.shields.io/badge/Version-2.0.0%20Streamlit-blue) ![License](https://img.shields.io/badge/License-MIT-green)

---

## 📋 Overview

AUS Auto Service is a web-based inventory management solution designed for spare parts workshops. It provides:

✅ **Real-time Stock Management** - Track inventory levels, low stock alerts  
✅ **Material Requisition** - Record material issuance to employees  
✅ **Purchase Tracking** - Log incoming purchases and supplier info  
✅ **Audit Logging** - Complete transaction history with Git versioning  
✅ **Data Analytics** - Anomaly detection, usage patterns, forecasting  
✅ **User-Friendly Interface** - Built with Streamlit for instant access  

---

## 🏗️ Repository Structure

### Active Branch: `main` (Streamlit Phase 2+)

```
auspautoservice1/
├── app.py                 # Streamlit main application
├── requirements.txt       # Python dependencies
├── LICENSE                # MIT License
├── README.md             # This file
├── .gitignore            # Git ignore patterns
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── src/
│   ├── __init__.py
│   ├── data_store.py     # CSV-based data layer with Git integration
│   └── etl.py            # ETL and data processing
├── data/                  # CSV data storage (auto-committed to Git)
│   ├── stock.csv
│   ├── requisitions.csv
│   ├── employees.csv
│   ├── materials.csv
│   ├── purchases.csv
│   ├── audit_log.csv
│   └── purchase_summary.csv
├── v1-vba/               # Original Excel + VBA system (archived)
│   ├── README.md
│   ├── *.xlsx / *.xlsm
│   └── VBA_*.bas
└── v1-original-python/   # Original AI/ML pipeline (archived)
    ├── README.md
    ├── run_*.py
    ├── docker-compose.yml
    └── src_old_*/
```

### Archive Folders

**`v1-vba/`** - Original Excel + VBA system  
Contains the first version built in Excel with VBA macros for automation.

**`v1-original-python/`** - Original AI/ML Pipeline  
Contains the first Python-based system with Supabase backend, LINE Bot integration, and ML forecasting. See [v1-original-python/README.md](v1-original-python/README.md) for details.

---

## 📦 Installation & Setup

### Prerequisites

- Python 3.9+
- Git
- pip or conda

### Getting Started

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Blackl1stV35/auspautoservice1.git
   cd auspautoservice1
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**

   ```bash
   streamlit run app.py
   ```

5. **Access the app:**

   Open your browser to `http://localhost:8501`

---

## 🔑 Key Features

### Data Management

- **CSV-Based Storage**: Lightweight, version-controllable data format
- **Automatic Git Commits**: Every transaction is recorded in Git history
- **Thread-Safe Operations**: Concurrent access support with file locking
- **No Database Required**: Self-contained with zero external dependencies

### Domain Operations

```python
from src.data_store import *

# Get current stock levels
stock = get_stock()

# Issue material to employee
issue_material(
    employee_name="John",
    material_name="Bearing",
    quantity=5,
    issued_by="Manager"
)

# Add purchases/receiving
add_stock("Bearing", quantity=20, user="Supplier")

# Low stock alerts
low_items = get_low_stock(threshold=10)

# Usage analytics & anomaly detection
anomalies = get_anomalies(z_threshold=2.0)

# Complete audit trail
audit_log = get_audit_log()
```

### Audit & Git Integration

- All transactions logged to `audit_log.csv`
- Changes automatically committed to Git with descriptive messages
- Complete transaction history available via Git history
- Enables rollback and historical analysis

---

## 📊 Data Schema

### stock.csv
| Column | Type | Description |
|--------|------|-------------|
| mat_id | int | Material ID |
| item_name | str | Material name |
| current_qty | int | Current quantity in stock |
| last_updated | datetime | Last update timestamp |

### requisitions.csv
| Column | Type | Description |
|--------|------|-------------|
| req_id | int | Requisition ID (timestamp-based) |
| employee_name | str | Employee receiving the material |
| material_name | str | Material being issued |
| quantity | int | Quantity issued |
| date | date | Date of issuance |
| time | time | Time of issuance |
| issued_by | str | Person authorizing the issuance |
| month | int | Month |
| year | int | Year (Buddhist calendar) |
| sheet | str | Source (e.g., "app_entry") |

### audit_log.csv
| Column | Type | Description |
|--------|------|-------------|
| timestamp | datetime | When the action occurred |
| user | str | User performing the action |
| action | str | Type of action (Thai) |
| detail | str | Details of the action |

### materials.csv
| Column | Type | Description |
|--------|------|-------------|
| material_id | int | Unique identifier |
| material_name | str | Name of the material |
| unit | str | Unit of measurement |
| category | str | Material category |
| supplier | str | Default supplier |

### employees.csv
| Column | Type | Description |
|--------|------|-------------|
| employee_id | int | Unique identifier |
| name | str | Employee name |
| department | str | Department |
| position | str | Job position |

---

## 🌳 Version History & Releases

### Phase 2: **Streamlit Implementation** (Active) - [Tag: v2.0.0-streamlit-phase1]

**Status:** ✅ Production Ready

Modern web interface with Streamlit, perfect for daily operations:

- Real-time stock tracking
- Material requisition forms
- Purchase logging
- Audit trail visualization
- Analytics & anomaly detection
- Thai language support
- CSV-based local storage
- Automatic Git versioning
- Cross-platform (Windows, Linux, macOS)

**Key Features:**
- Zero external database dependencies
- Self-contained data storage
- Instant startup and deployment
- Easy data export and analysis

---

### Phase 1: **Excel + VBA System** (Archived) - [Tag: v1.5.0-vba]

**Status:** 🔄 Historical Reference

Original spreadsheet-based system with VBA macros:

- Excel workbooks with automated workflows
- VBA macros for calculations and validations
- Manual data entry and reporting
- See `v1-vba/` folder for original files

---

### Phase 0: **Original AI Pipeline** (Historical) - [Tag: v1.0.0-original]

**Status:** 📦 Archive

First Python-based implementation:

- Supabase cloud database
- LINE Bot integration for notifications
- ML forecasting engine
- Docker containerized deployment
- Metabase analytics
- See `v1-original-python/` folder for details

---

## 🔄 Git Integration

This system uses Git as a version control and audit trail system:

```bash
# View all material transactions
git log --oneline data/requisitions.csv

# See all stock additions
git log --grep="รับเข้า" --oneline

# View specific employee operations
git log --grep="John" --oneline

# See transaction details
git show <commit>:data/requisitions.csv

# Revert a transaction (advanced)
git checkout <commit> -- data/
```

### Automatic Commits

Every material transaction automatically creates a Git commit:

- **Material Issuance**: `เบิก: [Employee] - [Material] x[Qty]`
- **Stock Receipt**: `รับเข้า: [Material] +[Qty]`
- **Manual Audit**: Descriptive commit messages for all operations

---

## 🚀 Future Development (Phase 2+)

Planned features for upcoming releases:

- [ ] Barcode/QR code scanning for material tracking
- [ ] Advanced analytics dashboard with charts
- [ ] Supplier management system
- [ ] Predictive inventory alerts
- [ ] Multi-location support
- [ ] User authentication & role-based access control
- [ ] Export reports (PDF, Excel)
- [ ] Mobile app companion

---

## 🛠️ Technology Stack

- **Frontend**: Streamlit 1.56.0
- **Data Processing**: Pandas 3.0.2
- **Storage**: CSV + Git
- **Language Support**: Python 3.9+
- **Version Control**: Git 2.0+
- **License**: MIT

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details

This means you are free to:
- Use in personal or commercial projects
- Modify and distribute
- Use privately

---

## 👤 Contributors

- **Blackl1st V35** - Lead Developer - [GitHub](https://github.com/Blackl1stV35)

---

## 📞 Support & Issues

For issues, questions, or feature requests:

1. **Check existing issues** - [GitHub Issues](https://github.com/Blackl1stV35/auspautoservice1/issues)
2. **Create a new issue** - Provide detailed description and steps to reproduce
3. **Contact maintainer** - Via GitHub or email

### Common Issues

**Issue:** Streamlit app won't start
- **Solution:** Ensure Python 3.9+ and run `pip install -r requirements.txt`

**Issue:** Permission denied on data files
- **Solution:** Check file permissions in `data/` folder

**Issue:** Git commits not working
- **Solution:** Ensure Git is installed and in system PATH

---

## 📚 Documentation

- **Main Application**: [app.py](app.py)
- **Data Layer API**: [src/data_store.py](src/data_store.py)
- **ETL Logic**: [src/etl.py](src/etl.py)
- **Original System**: [v1-original-python/README.md](v1-original-python/README.md)
- **VBA System**: [v1-vba/README.md](v1-vba/README.md)
- **Configuration**: [.streamlit/config.toml](.streamlit/config.toml)

---

## 🎯 Project Goals

✅ **Simplify Operations** - Eliminate manual spreadsheet management  
✅ **Improve Accuracy** - Automated tracking and calculations  
✅ **Enable Analytics** - Data-driven decision making  
✅ **Maintain History** - Complete audit trail with Git  
✅ **Easy Deployment** - Zero dependencies, instant setup  

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📅 Project Timeline

- **v1.0.0 (Phase 0)** - Jan 2026 - Original AI/ML pipeline with Supabase
- **v1.5.0** - Feb 2026 - Added Excel VBA system (v1-vba)
- **v2.0.0 (Phase 1)** - Mar-Apr 2026 - Streamlit implementation (current)
- **v2.1.0 (Phase 2)** - Q2 2026 - Barcode scanning & mobile app
- **v3.0.0 (Phase 3)** - Q3 2026 - Multi-location & advanced features

---

*Last Updated: 2026-04-10*  
*Version: 2.0.0-streamlit-phase1*  
*Repository: https://github.com/Blackl1stV35/auspautoservice1*

---

## Quick Reference

| Task | Command |
|------|---------|
| Start App | `streamlit run app.py` |
| View History | `git log --oneline` |
| Check Tags | `git tag -l` |
| Create Backup | `git bundle create backup.bundle --all` |
| Export Data | View CSV files in `data/` folder |
| Reset Data | `git checkout <commit> -- data/` |
