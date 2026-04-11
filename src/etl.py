"""
ETL Pipeline v4 สำหรับ SP Auto Service
- อ่าน Excel ที่ยุ่งเหยิง → Supabase PostgreSQL
- ไม่บันทึก CSV อัตโนมัติ (ใช้ปุ่ม Backup Clean Excel แทน)
- จัดการ notation "5+", "5+5+", วันที่ไทย, กริดกว้าง
"""
import pandas as pd
import re
import os
import uuid
import logging
from datetime import datetime
from io import BytesIO

logger = logging.getLogger(__name__)
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


# ═══════════════════════════════════════════════════════════════════
# Utility functions
# ═══════════════════════════════════════════════════════════════════

def clean_quantity(val) -> int:
    if pd.isna(val) or val == "" or val is None:
        return 0
    numbers = re.findall(r"\d+", str(val).strip())
    return sum(int(n) for n in numbers) if numbers else 0


def fix_thai_date(dt):
    if pd.isnull(dt):
        return None
    if isinstance(dt, str):
        try:
            dt = pd.to_datetime(dt, dayfirst=True)
        except Exception:
            return None
    if hasattr(dt, "year") and dt.year < 2000:
        try:
            return dt.replace(year=dt.year + 543 + 57)
        except Exception:
            return dt
    return dt


def _is_month_header(val) -> bool:
    if val is None:
        return False
    return bool(re.match(r"เดือน\d+/\d+", str(val).strip()))


def _extract_month_year(val: str):
    m = re.match(r"เดือน(\d+)/(\d+)", str(val).strip())
    return (int(m.group(1)), int(m.group(2))) if m else (None, None)


def _guess_category(name: str) -> str:
    n = name.lower()
    if any(k in n for k in ["กดท", "กระดาษทราย"]): return "กระดาษทราย"
    if "สเปย์" in n or "spray" in n: return "สเปรย์"
    if "ถุงมือ" in n: return "ถุงมือ"
    if "แปรง" in n or "ขนแกะ" in n: return "แปรง/ขนแกะ"
    if "แผ่น" in n: return "แผ่นขัด"
    if "ทินเนอร์" in n: return "ทินเนอร์"
    if "สี" in n or "พ่น" in n: return "สี"
    if "น้ำมัน" in n: return "น้ำมัน"
    if "กิ๊บ" in n or "น๊อต" in n or "สกรู" in n: return "กิ๊บน๊อต"
    if "หลอดไฟ" in n: return "หลอดไฟ"
    return "อื่นๆ"


# ═══════════════════════════════════════════════════════════════════
# REQUISITIONS ETL
# ═══════════════════════════════════════════════════════════════════

def process_requisitions(file_path: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    xls = pd.ExcelFile(file_path)
    all_records, all_employees, all_materials = [], set(), set()

    for sheet_name in xls.sheet_names:
        if "ฟอร์มเปล่า" in sheet_name:
            continue
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
        if df.empty or len(df.columns) < 2:
            continue

        material_names = []
        for col_idx in range(1, len(df.columns)):
            mat = df.iloc[0, col_idx]
            material_names.append(str(mat).strip() if pd.notna(mat) and str(mat).strip() else f"col_{col_idx}")
        all_materials.update(m for m in material_names if not m.startswith("col_"))

        sn_match = re.search(r"(\d+)-(\d+)", sheet_name)
        sheet_month = int(sn_match.group(1)) if sn_match else None
        sheet_year_short = int(sn_match.group(2)) if sn_match else None
        sheet_year = (2500 + sheet_year_short) if sheet_year_short and sheet_year_short < 100 else sheet_year_short
        current_month, current_year = sheet_month, sheet_year

        for row_idx in range(1, len(df)):
            first_cell = df.iloc[row_idx, 0]
            if pd.isna(first_cell) or str(first_cell).strip() == "":
                continue
            first_str = str(first_cell).strip()
            if _is_month_header(first_str):
                m, y = _extract_month_year(first_str)
                if m: current_month = m
                if y: current_year = y
                continue
            try:
                float(first_str); continue
            except ValueError:
                pass
            if any(kw in first_str for kw in ["รวม", "ยอด", "หมายเหตุ", "total"]):
                continue

            employee_name = first_str
            all_employees.add(employee_name)
            for col_idx in range(1, min(len(material_names) + 1, len(df.columns))):
                qty = clean_quantity(df.iloc[row_idx, col_idx])
                if qty > 0:
                    mat_name = material_names[col_idx - 1]
                    if not mat_name.startswith("col_"):
                        all_records.append({
                            "employee_name": employee_name, "material_name": mat_name,
                            "quantity": qty, "month": current_month, "year": current_year,
                            "sheet": sheet_name,
                        })

    req_df = pd.DataFrame(all_records)
    if not req_df.empty:
        req_df["req_id"] = range(1, len(req_df) + 1)
        req_df["date"] = req_df.apply(
            lambda r: f"{r['year']}-{r['month']:02d}-01" if r["year"] and r["month"] else None, axis=1)

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


# ═══════════════════════════════════════════════════════════════════
# PURCHASES ETL
# ═══════════════════════════════════════════════════════════════════

def process_purchases(file_path: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    xls = pd.ExcelFile(file_path)
    all_purchases = []

    for sheet_name in xls.sheet_names:
        if "สรุปยอด" in sheet_name:
            continue
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=0)
        if df.empty:
            continue
        col_map = {
            "รายการ": "item_name", "ชื่อร้าน": "supplier_name",
            "ชื่อร้านค้า": "supplier_name", "จำนวน": "quantity_raw",
            "จำนวน/ตัว": "quantity_raw", "ราคา/ชิ้น": "price_per_unit",
            "รวมจำนวนเงิน": "total_amount", "รวมก่อนVAT": "amount_before_vat",
            "ว/ด/ป": "purchase_date", "บิลเลขที่": "invoice_no",
            "หมายเหตุ": "notes", "ประเภท": "category", "ส่วนลด%": "discount_pct",
        }
        df.rename(columns={k: v for k, v in col_map.items() if k in df.columns}, inplace=True)
        if "item_name" not in df.columns:
            continue
        amount_col = "total_amount" if "total_amount" in df.columns else "amount_before_vat"
        if amount_col not in df.columns:
            continue
        df = df.dropna(subset=["item_name"])
        df = df[df[amount_col].notna() & (df[amount_col] != 0)]
        df["quantity"] = df["quantity_raw"].apply(clean_quantity) if "quantity_raw" in df.columns else 1
        if "purchase_date" in df.columns:
            df["purchase_date"] = df["purchase_date"].apply(fix_thai_date)
        if "category" in df.columns:
            df["category"] = df["category"].ffill()
        else:
            df["category"] = sheet_name
        df["sheet_category"] = sheet_name
        if "supplier_name" in df.columns:
            df["supplier_name"] = df["supplier_name"].ffill()
        cols = [c for c in ["item_name", "supplier_name", "quantity", "price_per_unit",
                             "total_amount", "amount_before_vat", "purchase_date",
                             "invoice_no", "notes", "category", "sheet_category", "discount_pct"]
                if c in df.columns]
        all_purchases.append(df[cols])

    purchases_df = pd.concat(all_purchases, ignore_index=True) if all_purchases else pd.DataFrame()
    if not purchases_df.empty:
        purchases_df["pur_id"] = range(1, len(purchases_df) + 1)
        if "purchase_date" in purchases_df.columns:
            purchases_df["purchase_date"] = pd.to_datetime(purchases_df["purchase_date"], errors="coerce")

    summary_df = pd.DataFrame()
    if "สรุปยอดประจำเดือน" in xls.sheet_names:
        sdf = pd.read_excel(file_path, sheet_name="สรุปยอดประจำเดือน", header=1)
        sdf.rename(columns={"ว/ด/ป": "date", "ชื่อร้านค้า": "supplier",
                             "ยอดรวม": "total", "เลขที่บิล": "invoice",
                             "หมายเหตุ": "notes"}, inplace=True)
        if "total" in sdf.columns:
            sdf = sdf.dropna(subset=["total"])
            if "date" in sdf.columns:
                sdf["date"] = sdf["date"].apply(fix_thai_date)
            summary_df = sdf

    logger.info(f"Purchases ETL: {len(purchases_df)} records")
    return purchases_df, summary_df


# ═══════════════════════════════════════════════════════════════════
# Full pipeline → Supabase (NO auto CSV saves)
# ═══════════════════════════════════════════════════════════════════

def run_full_etl(req_file: str = None, pur_file: str = None) -> dict:
    from src import data_store as ds
    os.makedirs(DATA_DIR, exist_ok=True)
    result = {}

    if req_file and os.path.exists(req_file):
        req_df, emp_df, mat_df = process_requisitions(req_file)

        ds.bulk_upsert_employees(emp_df["name"].tolist())
        ds.bulk_upsert_materials(
            mat_df[["item_name", "category", "unit", "reorder_level"]].to_dict("records"))

        if "tx_id" not in req_df.columns or req_df["tx_id"].isna().all():
            req_df["tx_id"] = [f"ETL-{i:06d}-{uuid.uuid4().hex[:6].upper()}" for i in range(len(req_df))]
        rr = req_df[["tx_id", "employee_name", "material_name", "quantity",
                      "date", "month", "year", "sheet"]].copy()
        rr["issued_by"] = "etl"
        rr["time"] = "00:00:00"
        rr["date"] = rr["date"].apply(lambda x: str(x) if pd.notna(x) and str(x) != "None" else None)
        ds.bulk_insert_requisitions(rr.to_dict("records"))
        ds.init_stock_from_materials()

        result["requisitions"] = req_df
        result["employees"] = emp_df
        result["materials"] = mat_df
        logger.info(f"ETL req: {len(req_df)} rows, {len(emp_df)} emp, {len(mat_df)} mat")

    if pur_file and os.path.exists(pur_file):
        pur_df, sum_df = process_purchases(pur_file)
        pur_cols = ["item_name", "supplier_name", "quantity", "price_per_unit",
                    "total_amount", "amount_before_vat", "purchase_date",
                    "invoice_no", "notes", "category", "sheet_category", "discount_pct"]
        pr = pur_df[[c for c in pur_cols if c in pur_df.columns]].copy()
        if "purchase_date" in pr.columns:
            pr["purchase_date"] = pr["purchase_date"].apply(
                lambda x: x.strftime("%Y-%m-%d") if pd.notna(x) and hasattr(x, "strftime") else None)
        ds.bulk_insert_purchases(pr.to_dict("records"))
        result["purchases"] = pur_df
        result["purchase_summary"] = sum_df
        logger.info(f"ETL pur: {len(pur_df)} rows")

    counts = ", ".join(f"{k}={len(v)}" for k, v in result.items() if hasattr(v, "__len__"))
    ds.log_audit("admin", "ETL", f"อัปโหลด Excel: {counts}")
    ds._invalidate_caches()
    return result


# ═══════════════════════════════════════════════════════════════════
# Clean Excel backup (called from app.py button)
# ═══════════════════════════════════════════════════════════════════

def generate_clean_excel(req_file: str = None, pur_file: str = None) -> bytes:
    """
    Process the raw Excel files and return a clean, well-organized
    Excel workbook as bytes (for download via st.download_button).
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        if req_file and os.path.exists(req_file):
            req_df, emp_df, mat_df = process_requisitions(req_file)
            if not req_df.empty:
                req_df.to_excel(writer, sheet_name="รายการเบิก", index=False)
            if not emp_df.empty:
                emp_df.to_excel(writer, sheet_name="รายชื่อช่าง", index=False)
            if not mat_df.empty:
                mat_df.to_excel(writer, sheet_name="รายการวัสดุ", index=False)

        if pur_file and os.path.exists(pur_file):
            pur_df, sum_df = process_purchases(pur_file)
            if not pur_df.empty:
                # Clean up dates for Excel
                if "purchase_date" in pur_df.columns:
                    pur_df["purchase_date"] = pd.to_datetime(
                        pur_df["purchase_date"], errors="coerce")
                pur_df.to_excel(writer, sheet_name="ประวัติการซื้อ", index=False)
            if not sum_df.empty:
                sum_df.to_excel(writer, sheet_name="สรุปรายเดือน", index=False)

    return output.getvalue()
