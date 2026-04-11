"""
ETL Pipeline สำหรับ SP Auto Service
- อ่าน Excel ที่ยุ่งเหยิง → ตาราง CSV ที่สะอาด
- จัดการ notation "5+", "5+5+", วันที่ไทย, กริดกว้าง
"""
import pandas as pd
import re
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

# ---------------------------------------------------------------------------
# Utility functions (adapted from auspautoservice1/src/workers/etl.py)
# ---------------------------------------------------------------------------

def clean_quantity(val) -> int:
    """Parse '5+', '5+5+5+', numbers, etc. into total integer quantity."""
    if pd.isna(val) or val == "" or val is None:
        return 0
    s = str(val).strip()
    numbers = re.findall(r"\d+", s)
    if not numbers:
        return 0
    return sum(int(n) for n in numbers)


def fix_thai_date(dt):
    """Fix Excel dates that appear in the 1960s (Buddhist Era offset of +543)."""
    if pd.isnull(dt):
        return None
    if isinstance(dt, str):
        try:
            dt = pd.to_datetime(dt, dayfirst=True)
        except Exception:
            return None
    if hasattr(dt, "year") and dt.year < 2100:
        if dt.year < 2000:
            try:
                return dt.replace(year=dt.year + 543 + 57)  # 1963 → 2563
            except Exception:
                return dt
    return dt


def _is_month_header(val) -> bool:
    """Check if a cell value is a month header like 'เดือน1/2569'."""
    if val is None:
        return False
    return bool(re.match(r"เดือน\d+/\d+", str(val).strip()))


def _extract_month_year(val: str):
    """Extract (month, year) from 'เดือน2/2569' → (2, 2569)."""
    m = re.match(r"เดือน(\d+)/(\d+)", str(val).strip())
    if m:
        return int(m.group(1)), int(m.group(2))
    return None, None


# ---------------------------------------------------------------------------
# REQUISITIONS ETL (File 1: สถิติเบิกวัสดุสิ้นเปลือง)
# ---------------------------------------------------------------------------

def process_requisitions(file_path: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Process the consumable requisition Excel file.
    Returns (requisitions_df, employees_df, materials_df).
    
    The sheet structure repeats blocks of employees per "page" within each sheet.
    Row 0 = material headers, Row 1 = month header + column numbers, 
    then employee rows until next month header.
    """
    xls = pd.ExcelFile(file_path)
    all_records = []
    all_employees = set()
    all_materials = set()

    for sheet_name in xls.sheet_names:
        if "ฟอร์มเปล่า" in sheet_name:
            continue

        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
        if df.empty or len(df.columns) < 2:
            continue

        # Row 0 has material names in columns 1+
        material_names = []
        for col_idx in range(1, len(df.columns)):
            mat = df.iloc[0, col_idx]
            if pd.notna(mat) and str(mat).strip():
                material_names.append(str(mat).strip())
            else:
                material_names.append(f"col_{col_idx}")
        all_materials.update(m for m in material_names if not m.startswith("col_"))

        # Extract month/year from sheet name
        sn_match = re.search(r"(\d+)-(\d+)", sheet_name)
        sheet_month = int(sn_match.group(1)) if sn_match else None
        sheet_year_short = int(sn_match.group(2)) if sn_match else None
        sheet_year = (2500 + sheet_year_short) if sheet_year_short and sheet_year_short < 100 else sheet_year_short

        current_month = sheet_month
        current_year = sheet_year

        # Iterate rows starting from row 1
        for row_idx in range(1, len(df)):
            first_cell = df.iloc[row_idx, 0]
            if pd.isna(first_cell) or str(first_cell).strip() == "":
                continue

            first_str = str(first_cell).strip()

            # Check if this is a month header row
            if _is_month_header(first_str):
                m, y = _extract_month_year(first_str)
                if m:
                    current_month = m
                if y:
                    current_year = y
                continue

            # Skip numeric-only rows (column index rows)
            try:
                float(first_str)
                continue
            except ValueError:
                pass

            # Skip summary/total rows
            if any(kw in first_str for kw in ["รวม", "ยอด", "หมายเหตุ", "total"]):
                continue

            # This is an employee row
            employee_name = first_str
            all_employees.add(employee_name)

            for col_idx in range(1, min(len(material_names) + 1, len(df.columns))):
                cell_val = df.iloc[row_idx, col_idx]
                qty = clean_quantity(cell_val)
                if qty > 0:
                    mat_name = material_names[col_idx - 1]
                    if mat_name.startswith("col_"):
                        continue
                    all_records.append({
                        "employee_name": employee_name,
                        "material_name": mat_name,
                        "quantity": qty,
                        "month": current_month,
                        "year": current_year,
                        "sheet": sheet_name,
                    })

    # Build DataFrames
    req_df = pd.DataFrame(all_records)
    if not req_df.empty:
        req_df["req_id"] = range(1, len(req_df) + 1)
        req_df["date"] = req_df.apply(
            lambda r: f"{r['year']}-{r['month']:02d}-01" if r["year"] and r["month"] else None, axis=1
        )

    emp_df = pd.DataFrame(sorted(all_employees), columns=["name"])
    emp_df["emp_id"] = range(1, len(emp_df) + 1)

    mat_list = sorted(m for m in all_materials if m)
    mat_df = pd.DataFrame(mat_list, columns=["item_name"])
    mat_df["mat_id"] = range(1, len(mat_df) + 1)
    mat_df["category"] = mat_df["item_name"].apply(_guess_category)
    mat_df["unit"] = "ชิ้น"
    mat_df["reorder_level"] = 10

    logger.info(f"Requisitions ETL: {len(req_df)} records, {len(emp_df)} employees, {len(mat_df)} materials")
    return req_df, emp_df, mat_df


def _guess_category(name: str) -> str:
    """Guess material category from its Thai name."""
    n = name.lower()
    if any(k in n for k in ["กดท", "กระดาษทราย"]):
        return "กระดาษทราย"
    if "สเปย์" in n or "spray" in n:
        return "สเปรย์"
    if "ถุงมือ" in n:
        return "ถุงมือ"
    if "แปรง" in n or "ขนแกะ" in n:
        return "แปรง/ขนแกะ"
    if "แผ่น" in n:
        return "แผ่นขัด"
    return "อื่นๆ"


# ---------------------------------------------------------------------------
# PURCHASES ETL (File 2: ต้นทุนแผนกสี)
# ---------------------------------------------------------------------------

def process_purchases(file_path: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Process the purchase/cost Excel file.
    Returns (purchases_df, summary_df).
    """
    xls = pd.ExcelFile(file_path)
    all_purchases = []

    for sheet_name in xls.sheet_names:
        if "สรุปยอด" in sheet_name:
            continue  # handle summary separately

        df = pd.read_excel(file_path, sheet_name=sheet_name, header=0)
        if df.empty:
            continue

        # Map Thai column names
        col_map = {
            "รายการ": "item_name",
            "ชื่อร้าน": "supplier_name",
            "ชื่อร้านค้า": "supplier_name",
            "จำนวน": "quantity_raw",
            "จำนวน/ตัว": "quantity_raw",
            "ราคา/ชิ้น": "price_per_unit",
            "รวมจำนวนเงิน": "total_amount",
            "รวมก่อนVAT": "amount_before_vat",
            "ว/ด/ป": "purchase_date",
            "บิลเลขที่": "invoice_no",
            "หมายเหตุ": "notes",
            "ประเภท": "category",
            "ส่วนลด%": "discount_pct",
        }
        df.rename(columns={k: v for k, v in col_map.items() if k in df.columns}, inplace=True)

        # Keep only rows with item_name and some amount
        if "item_name" not in df.columns:
            continue
        amount_col = "total_amount" if "total_amount" in df.columns else "amount_before_vat"
        if amount_col not in df.columns:
            continue
        df = df.dropna(subset=["item_name"])
        df = df[df[amount_col].notna() & (df[amount_col] != 0)]

        if "quantity_raw" in df.columns:
            df["quantity"] = df["quantity_raw"].apply(clean_quantity)
        else:
            df["quantity"] = 1

        if "purchase_date" in df.columns:
            df["purchase_date"] = df["purchase_date"].apply(fix_thai_date)

        # Forward-fill category
        if "category" in df.columns:
            df["category"] = df["category"].ffill()
        else:
            df["category"] = sheet_name

        df["sheet_category"] = sheet_name

        # Forward-fill supplier
        if "supplier_name" in df.columns:
            df["supplier_name"] = df["supplier_name"].ffill()

        cols_to_keep = [c for c in [
            "item_name", "supplier_name", "quantity", "price_per_unit",
            "total_amount", "amount_before_vat", "purchase_date",
            "invoice_no", "notes", "category", "sheet_category", "discount_pct"
        ] if c in df.columns]

        all_purchases.append(df[cols_to_keep])

    purchases_df = pd.concat(all_purchases, ignore_index=True) if all_purchases else pd.DataFrame()
    if not purchases_df.empty:
        purchases_df["pur_id"] = range(1, len(purchases_df) + 1)
        if "purchase_date" in purchases_df.columns:
            purchases_df["purchase_date"] = pd.to_datetime(purchases_df["purchase_date"], errors="coerce")

    # Process summary sheet
    summary_df = pd.DataFrame()
    if "สรุปยอดประจำเดือน" in xls.sheet_names:
        sdf = pd.read_excel(file_path, sheet_name="สรุปยอดประจำเดือน", header=1)
        col_map_s = {
            "ว/ด/ป": "date",
            "ชื่อร้านค้า": "supplier",
            "ยอดรวม": "total",
            "เลขที่บิล": "invoice",
            "หมายเหตุ": "notes",
        }
        sdf.rename(columns={k: v for k, v in col_map_s.items() if k in sdf.columns}, inplace=True)
        if "total" in sdf.columns:
            sdf = sdf.dropna(subset=["total"])
            if "date" in sdf.columns:
                sdf["date"] = sdf["date"].apply(fix_thai_date)
            summary_df = sdf

    logger.info(f"Purchases ETL: {len(purchases_df)} purchase records")
    return purchases_df, summary_df


# ---------------------------------------------------------------------------
# Full pipeline: run both + save CSVs
# ---------------------------------------------------------------------------

def run_full_etl(req_file: str = None, pur_file: str = None) -> dict:
    """Run full ETL and save to data/ directory. Returns dict of DataFrames."""
    os.makedirs(DATA_DIR, exist_ok=True)
    result = {}

    if req_file and os.path.exists(req_file):
        req_df, emp_df, mat_df = process_requisitions(req_file)
        req_df.to_csv(os.path.join(DATA_DIR, "requisitions.csv"), index=False)
        emp_df.to_csv(os.path.join(DATA_DIR, "employees.csv"), index=False)
        mat_df.to_csv(os.path.join(DATA_DIR, "materials.csv"), index=False)
        result["requisitions"] = req_df
        result["employees"] = emp_df
        result["materials"] = mat_df
        logger.info("Saved requisitions, employees, materials CSVs")

    if pur_file and os.path.exists(pur_file):
        pur_df, sum_df = process_purchases(pur_file)
        pur_df.to_csv(os.path.join(DATA_DIR, "purchases.csv"), index=False)
        if not sum_df.empty:
            sum_df.to_csv(os.path.join(DATA_DIR, "purchase_summary.csv"), index=False)
        result["purchases"] = pur_df
        result["purchase_summary"] = sum_df
        logger.info("Saved purchases CSV")

    # Initialize stock & audit log if they don't exist
    stock_path = os.path.join(DATA_DIR, "stock.csv")
    if not os.path.exists(stock_path):
        if "materials" in result and not result["materials"].empty:
            stock = result["materials"][["mat_id", "item_name"]].copy()
            stock["current_qty"] = 0
            stock["last_updated"] = datetime.now().isoformat()
            stock.to_csv(stock_path, index=False)

    audit_path = os.path.join(DATA_DIR, "audit_log.csv")
    if not os.path.exists(audit_path):
        pd.DataFrame(columns=["timestamp", "user", "action", "detail"]).to_csv(audit_path, index=False)

    # Auto-commit all ETL output to Git (reuses the robust git_commit
    # from data_store which handles init, user config, -A flag, etc.)
    _etl_git_commit(result)

    return result


def _etl_git_commit(result: dict):
    """Commit ETL output via data_store.git_commit for consistency."""
    try:
        from src.data_store import git_commit
        counts = ", ".join(f"{k}={len(v)}" for k, v in result.items()
                           if hasattr(v, "__len__"))
        ok = git_commit(f"ETL: {counts}")
        if ok:
            logger.info("ETL git commit OK")
        else:
            logger.warning("ETL git commit returned False")
    except ImportError:
        # Fallback if data_store can't be imported (standalone ETL run)
        import subprocess
        try:
            root = os.path.dirname(DATA_DIR)
            subprocess.run(["git", "add", "-A", "data/"], cwd=root,
                           capture_output=True, timeout=15)
            counts = ", ".join(f"{k}={len(v)}" for k, v in result.items()
                               if hasattr(v, "__len__"))
            subprocess.run(["git", "commit", "-m", f"ETL: {counts}"],
                           cwd=root, capture_output=True, timeout=15)
        except Exception as e:
            logger.warning(f"ETL git commit fallback failed: {e}")
        logger.info("ETL git commit OK")
    except Exception as e:
        logger.warning(f"ETL git commit skipped: {e}")