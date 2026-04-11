"""
Data Store v4: Supabase PostgreSQL — Performance-optimized.

Key changes from v3:
  • st.cache_data(ttl=60) on all read functions → sub-second page loads
  • SQL views for heavy aggregations → no client-side groupby
  • Lazy column selection → less data over the wire
  • Cost & supplier analysis functions (new)
  • sanitize_for_json for NaN-safe inserts (kept from v3)
"""
import streamlit as st
import pandas as pd
import numpy as np
import os
import uuid
import math
from datetime import datetime, timedelta
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)
DUPLICATE_WINDOW_SECS = 120
_CACHE_TTL = 60  # seconds — balance freshness vs speed


# ═══════════════════════════════════════════════════════════════════
# Supabase connection (singleton, cached per process)
# ═══════════════════════════════════════════════════════════════════

def _get_supabase():
    url = None
    key = None
    try:
        sb = st.secrets.get("supabase", {})
        url = sb.get("url")
        key = sb.get("key")
    except Exception:
        pass
    if not url:
        url = os.environ.get("SUPABASE_URL")
    if not key:
        key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        raise RuntimeError("Supabase credentials not found in secrets.toml or env vars.")
    url, key = str(url).strip(), str(key).strip()
    if url.startswith("postgresql://") or url.startswith("postgres://"):
        import re
        m = re.search(r"postgres(?:ql)?://postgres\.([a-z0-9]+)", url)
        if m:
            url = f"https://{m.group(1)}.supabase.co"
    if not url.startswith("https://"):
        raise RuntimeError(f"URL must start with https://, got: {url[:50]}")
    from supabase import create_client
    return create_client(url, key)


@lru_cache(maxsize=1)
def _sb():
    return _get_supabase()


def _q(table: str):
    return _sb().table(table)


def db_status_info() -> dict:
    try:
        client = _sb()
        raw_url = str(getattr(client, "supabase_url", ""))
        project = None
        if "supabase.co" in raw_url:
            try:
                project = raw_url.split("//")[1].split(".")[0]
            except Exception:
                project = raw_url[:40]
        _q("employees").select("emp_id", count="exact").limit(1).execute()
        return {"connected": True, "project": project, "tables_ok": True}
    except Exception as e:
        return {"connected": False, "project": None, "tables_ok": False,
                "error": str(e)[:150]}


# ═══════════════════════════════════════════════════════════════════
# Cached read functions — @st.cache_data with TTL
# ═══════════════════════════════════════════════════════════════════

@st.cache_data(ttl=_CACHE_TTL)
def get_requisitions() -> pd.DataFrame:
    try:
        r = _q("requisitions").select(
            "tx_id,employee_name,material_name,quantity,date,time,issued_by,month,year,sheet,created_at"
        ).order("created_at", desc=True).execute()
        df = pd.DataFrame(r.data) if r.data else pd.DataFrame()
        if not df.empty and "quantity" in df.columns:
            df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)
        return df
    except Exception as e:
        logger.warning(f"get_requisitions: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=_CACHE_TTL)
def get_employees() -> pd.DataFrame:
    try:
        r = _q("employees").select("emp_id,name").order("name").execute()
        return pd.DataFrame(r.data) if r.data else pd.DataFrame()
    except Exception as e:
        logger.warning(f"get_employees: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=_CACHE_TTL)
def get_materials() -> pd.DataFrame:
    try:
        r = _q("materials").select("mat_id,item_name,category,unit,reorder_level").order("item_name").execute()
        return pd.DataFrame(r.data) if r.data else pd.DataFrame()
    except Exception as e:
        logger.warning(f"get_materials: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=_CACHE_TTL)
def get_stock() -> pd.DataFrame:
    try:
        r = _q("stock").select("stock_id,item_name,current_qty,last_updated").order("item_name").execute()
        df = pd.DataFrame(r.data) if r.data else pd.DataFrame()
        if not df.empty and "current_qty" in df.columns:
            df["current_qty"] = pd.to_numeric(df["current_qty"], errors="coerce").fillna(0).astype(int)
        return df
    except Exception as e:
        logger.warning(f"get_stock: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=_CACHE_TTL)
def get_purchases() -> pd.DataFrame:
    try:
        r = _q("purchases").select("*").order("pur_id", desc=True).execute()
        df = pd.DataFrame(r.data) if r.data else pd.DataFrame()
        for c in ["total_amount", "price_per_unit", "quantity"]:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
        return df
    except Exception as e:
        logger.warning(f"get_purchases: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=_CACHE_TTL)
def get_audit_log() -> pd.DataFrame:
    try:
        r = _q("audit_log").select("*").order("timestamp", desc=True).limit(500).execute()
        return pd.DataFrame(r.data) if r.data else pd.DataFrame()
    except Exception as e:
        logger.warning(f"get_audit_log: {e}")
        return pd.DataFrame()


def _invalidate_caches():
    """Clear all st.cache_data caches after a write operation."""
    for fn in [get_requisitions, get_employees, get_materials,
               get_stock, get_purchases, get_audit_log,
               get_monthly_cost, get_supplier_ranking,
               get_price_history, get_category_cost,
               get_cost_vs_usage]:
        fn.clear()


# ═══════════════════════════════════════════════════════════════════
# Audit & Transaction ID
# ═══════════════════════════════════════════════════════════════════

def log_audit(user: str, action: str, detail: str, **_kw):
    try:
        _q("audit_log").insert({"user": user, "action": action, "detail": detail}).execute()
    except Exception as e:
        logger.warning(f"log_audit: {e}")


def generate_tx_id() -> str:
    now = datetime.now()
    return f"SP-{now:%Y%m%d}-{now:%H%M%S}-{uuid.uuid4().hex[:6].upper()}"


# ═══════════════════════════════════════════════════════════════════
# Duplicate detection
# ═══════════════════════════════════════════════════════════════════

def check_duplicate(emp: str, mat: str, qty: int, window: int = DUPLICATE_WINDOW_SECS) -> bool:
    try:
        cutoff = (datetime.utcnow() - timedelta(seconds=window)).isoformat()
        r = (_q("requisitions").select("tx_id")
             .eq("employee_name", emp).eq("material_name", mat)
             .eq("quantity", qty).gte("created_at", cutoff).limit(1).execute())
        return bool(r.data)
    except Exception:
        return False


# ═══════════════════════════════════════════════════════════════════
# Domain operations — write + invalidate
# ═══════════════════════════════════════════════════════════════════

def issue_material(employee_name: str, material_name: str, quantity: int,
                   issued_by: str = "system", skip_dup_check: bool = False) -> dict:
    if quantity <= 0:
        return {"ok": False, "tx_id": None, "committed": False, "msg": "จำนวนต้องมากกว่า 0"}
    if not employee_name or not material_name:
        return {"ok": False, "tx_id": None, "committed": False, "msg": "กรุณาเลือกชื่อช่างและวัสดุ"}
    if not skip_dup_check and check_duplicate(employee_name, material_name, quantity):
        return {"ok": False, "tx_id": None, "committed": False,
                "msg": f"⚠️ พบรายการซ้ำภายใน {DUPLICATE_WINDOW_SECS} วินาที"}
    now = datetime.now()
    tx_id = generate_tx_id()
    try:
        _q("requisitions").insert({
            "tx_id": tx_id, "employee_name": employee_name,
            "material_name": material_name, "quantity": quantity,
            "date": now.strftime("%Y-%m-%d"), "time": now.strftime("%H:%M:%S"),
            "issued_by": issued_by, "month": now.month, "year": now.year + 543,
            "sheet": "app_entry",
        }).execute()
        # Decrement stock
        sr = _q("stock").select("current_qty").eq("item_name", material_name).limit(1).execute()
        if sr.data:
            _q("stock").update({"current_qty": int(sr.data[0]["current_qty"]) - quantity,
                                "last_updated": now.isoformat()}).eq("item_name", material_name).execute()
        log_audit(issued_by, "เบิกวัสดุ", f"{employee_name} เบิก {material_name} x{quantity} [{tx_id}]")
        _invalidate_caches()
        return {"ok": True, "tx_id": tx_id, "committed": True,
                "msg": f"✅ สำเร็จ! {employee_name} เบิก {material_name} x{quantity}"}
    except Exception as e:
        logger.error(f"issue_material: {e}")
        return {"ok": False, "tx_id": tx_id, "committed": False, "msg": f"❌ {e}"}


def add_stock(material_name: str, quantity: int, user: str = "system") -> dict:
    if quantity <= 0:
        return {"ok": False, "committed": False, "msg": "จำนวนต้องมากกว่า 0"}
    try:
        now = datetime.now()
        sr = _q("stock").select("current_qty").eq("item_name", material_name).limit(1).execute()
        if sr.data:
            _q("stock").update({"current_qty": int(sr.data[0]["current_qty"]) + quantity,
                                "last_updated": now.isoformat()}).eq("item_name", material_name).execute()
        else:
            _q("stock").insert({"item_name": material_name, "current_qty": quantity,
                                "last_updated": now.isoformat()}).execute()
        log_audit(user, "รับวัสดุเข้า", f"{material_name} +{quantity}")
        _invalidate_caches()
        return {"ok": True, "committed": True, "msg": f"✅ รับเข้า {material_name} +{quantity}"}
    except Exception as e:
        return {"ok": False, "committed": False, "msg": f"❌ {e}"}


# ═══════════════════════════════════════════════════════════════════
# Stock helpers
# ═══════════════════════════════════════════════════════════════════

def get_low_stock(threshold: int = 10) -> pd.DataFrame:
    s = get_stock()
    if s.empty or "current_qty" not in s.columns:
        return pd.DataFrame()
    return s[s["current_qty"] <= threshold].sort_values("current_qty")


def get_stock_status(qty: int) -> str:
    if qty <= 0:  return "🔴 หมด"
    if qty <= 5:  return "🟠 วิกฤต"
    if qty <= 10: return "🟡 ต่ำ"
    return "🟢 ปกติ"


# ═══════════════════════════════════════════════════════════════════
# Anomaly detection
# ═══════════════════════════════════════════════════════════════════

def get_anomalies(z_threshold: float = 2.0) -> pd.DataFrame:
    req = get_requisitions()
    if req.empty or "employee_name" not in req.columns:
        return pd.DataFrame()
    usage = req.groupby("employee_name")["quantity"].sum().reset_index()
    m, s = usage["quantity"].mean(), usage["quantity"].std()
    if s == 0 or pd.isna(s):
        return pd.DataFrame()
    usage["z_score"] = (usage["quantity"] - m) / s
    return usage[usage["z_score"] > z_threshold].sort_values("z_score", ascending=False)


def get_anomalies_per_material(z_threshold: float = 2.0) -> pd.DataFrame:
    req = get_requisitions()
    if req.empty:
        return pd.DataFrame()
    pivot = req.groupby(["employee_name", "material_name"])["quantity"].sum().reset_index()
    stats = pivot.groupby("material_name")["quantity"].agg(["mean", "std"]).reset_index()
    stats.columns = ["material_name", "mat_mean", "mat_std"]
    merged = pivot.merge(stats, on="material_name")
    merged["z_score"] = np.where(merged["mat_std"] > 0,
                                  (merged["quantity"] - merged["mat_mean"]) / merged["mat_std"], 0)
    f = merged[merged["z_score"] > z_threshold].sort_values("z_score", ascending=False)
    return f[["employee_name", "material_name", "quantity", "z_score"]]


# ═══════════════════════════════════════════════════════════════════
# Monthly accumulation (VBA "N+" style)
# ═══════════════════════════════════════════════════════════════════

def _add_period(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    df = df.copy()
    df["period"] = df.apply(
        lambda r: f"{int(r['month']):02d}/{int(r['year'])}"
        if pd.notna(r.get("month")) and pd.notna(r.get("year")) else "ไม่ระบุ", axis=1)
    return df


def get_monthly_summary() -> pd.DataFrame:
    req = _add_period(get_requisitions())
    if req.empty:
        return pd.DataFrame()
    pv = req.pivot_table(index="employee_name", columns="period",
                          values="quantity", aggfunc="sum", fill_value=0)
    pv["รวมทั้งหมด"] = pv.sum(axis=1)
    return pv.sort_values("รวมทั้งหมด", ascending=False)


def get_monthly_by_material() -> pd.DataFrame:
    req = _add_period(get_requisitions())
    if req.empty:
        return pd.DataFrame()
    pv = req.pivot_table(index="material_name", columns="period",
                          values="quantity", aggfunc="sum", fill_value=0)
    pv["รวมทั้งหมด"] = pv.sum(axis=1)
    return pv.sort_values("รวมทั้งหมด", ascending=False)


def get_available_periods() -> list[str]:
    req = _add_period(get_requisitions())
    if req.empty:
        return []
    return sorted(req["period"].dropna().unique().tolist())


def get_usage_heatmap() -> pd.DataFrame:
    req = get_requisitions()
    if req.empty:
        return pd.DataFrame()
    return req.pivot_table(index="employee_name", columns="material_name",
                            values="quantity", aggfunc="sum", fill_value=0)


# ═══════════════════════════════════════════════════════════════════
# ★ NEW: Cost & Supplier Analysis (uses SQL views for speed)
# ═══════════════════════════════════════════════════════════════════

@st.cache_data(ttl=_CACHE_TTL)
def get_monthly_cost() -> pd.DataFrame:
    """Monthly cost summary from v_monthly_cost view."""
    try:
        r = _q("v_monthly_cost").select("*").execute()
        df = pd.DataFrame(r.data) if r.data else pd.DataFrame()
        for c in ["total_cost", "total_qty", "avg_unit_price"]:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
        return df
    except Exception as e:
        logger.warning(f"get_monthly_cost (view fallback): {e}")
        # Fallback: compute from purchases table
        pur = get_purchases()
        if pur.empty or "purchase_date" not in pur.columns:
            return pd.DataFrame()
        pur["period"] = pd.to_datetime(pur["purchase_date"], errors="coerce").dt.strftime("%Y-%m")
        return pur.groupby(["period", "sheet_category", "supplier_name"]).agg(
            tx_count=("pur_id", "count"),
            total_cost=("total_amount", "sum"),
            total_qty=("quantity", "sum"),
            avg_unit_price=("price_per_unit", "mean"),
        ).reset_index()


@st.cache_data(ttl=_CACHE_TTL)
def get_supplier_ranking() -> pd.DataFrame:
    """Supplier ranking from v_supplier_rank view."""
    try:
        r = _q("v_supplier_rank").select("*").execute()
        df = pd.DataFrame(r.data) if r.data else pd.DataFrame()
        for c in ["total_spend", "total_qty", "order_count"]:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
        return df
    except Exception as e:
        logger.warning(f"get_supplier_ranking (fallback): {e}")
        pur = get_purchases()
        if pur.empty:
            return pd.DataFrame()
        return pur.groupby("supplier_name").agg(
            order_count=("pur_id", "count"),
            total_spend=("total_amount", "sum"),
            total_qty=("quantity", "sum"),
            unique_items=("item_name", "nunique"),
        ).reset_index().sort_values("total_spend", ascending=False)


@st.cache_data(ttl=_CACHE_TTL)
def get_price_history() -> pd.DataFrame:
    """Price history with pct_change from v_price_history view."""
    try:
        r = _q("v_price_history").select("*").execute()
        df = pd.DataFrame(r.data) if r.data else pd.DataFrame()
        for c in ["price_per_unit", "prev_price", "pct_change"]:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce")
        return df
    except Exception as e:
        logger.warning(f"get_price_history (fallback): {e}")
        return pd.DataFrame()


@st.cache_data(ttl=_CACHE_TTL)
def get_category_cost() -> pd.DataFrame:
    """Cost breakdown by category from v_category_cost view."""
    try:
        r = _q("v_category_cost").select("*").execute()
        df = pd.DataFrame(r.data) if r.data else pd.DataFrame()
        for c in ["total_cost", "avg_cost", "item_count"]:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
        return df
    except Exception as e:
        logger.warning(f"get_category_cost (fallback): {e}")
        pur = get_purchases()
        if pur.empty:
            return pd.DataFrame()
        return pur.groupby("sheet_category").agg(
            item_count=("pur_id", "count"),
            total_cost=("total_amount", "sum"),
            avg_cost=("total_amount", "mean"),
        ).reset_index().sort_values("total_cost", ascending=False)


@st.cache_data(ttl=_CACHE_TTL)
def get_cost_vs_usage() -> pd.DataFrame:
    """Purchased vs issued comparison from v_cost_vs_usage view."""
    try:
        r = _q("v_cost_vs_usage").select("*").execute()
        df = pd.DataFrame(r.data) if r.data else pd.DataFrame()
        for c in ["purchased_qty", "purchase_cost", "issued_qty", "current_stock"]:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
        return df
    except Exception as e:
        logger.warning(f"get_cost_vs_usage: {e}")
        return pd.DataFrame()


def get_price_spikes(threshold_pct: float = 30.0) -> pd.DataFrame:
    """Items with price increase > threshold_pct from previous purchase."""
    ph = get_price_history()
    if ph.empty or "pct_change" not in ph.columns:
        return pd.DataFrame()
    spikes = ph[ph["pct_change"] > threshold_pct].sort_values("pct_change", ascending=False)
    return spikes[["item_name", "supplier_name", "purchase_date",
                    "prev_price", "price_per_unit", "pct_change"]].head(50)


def get_cost_kpis() -> dict:
    """Quick KPI dict for the cost page header cards."""
    pur = get_purchases()
    if pur.empty:
        return {"total_spend": 0, "ytd_spend": 0, "avg_daily": 0,
                "top_drivers": [], "this_month": 0}
    pur["total_amount"] = pd.to_numeric(pur["total_amount"], errors="coerce").fillna(0)
    total = pur["total_amount"].sum()

    # This month
    now = datetime.now()
    pur["purchase_date"] = pd.to_datetime(pur["purchase_date"], errors="coerce")
    this_month = pur[
        (pur["purchase_date"].dt.month == now.month) &
        (pur["purchase_date"].dt.year == now.year)
    ]["total_amount"].sum()

    # YTD
    ytd = pur[pur["purchase_date"].dt.year == now.year]["total_amount"].sum()

    # Avg daily
    date_range = (pur["purchase_date"].max() - pur["purchase_date"].min()).days
    avg_daily = total / max(date_range, 1)

    # Top 3 cost drivers
    top3 = (pur.groupby("sheet_category")["total_amount"].sum()
            .nlargest(3).reset_index().values.tolist())

    return {"total_spend": total, "ytd_spend": ytd, "avg_daily": avg_daily,
            "top_drivers": top3, "this_month": this_month}


def get_cost_forecast() -> pd.DataFrame:
    """Simple monthly cost forecast using 3-month moving average."""
    mc = get_monthly_cost()
    if mc.empty or "total_cost" not in mc.columns:
        return pd.DataFrame()
    monthly = mc.groupby("period")["total_cost"].sum().reset_index().sort_values("period")
    if len(monthly) < 3:
        return monthly
    monthly["forecast"] = monthly["total_cost"].rolling(3, min_periods=1).mean().shift(1)
    monthly["over_budget"] = monthly["total_cost"] > monthly["forecast"] * 1.2
    return monthly


# ═══════════════════════════════════════════════════════════════════
# NaN sanitization for Supabase JSON inserts
# ═══════════════════════════════════════════════════════════════════

_NAN_DEFAULTS = {
    "quantity": 0, "price_per_unit": 0, "total_amount": 0,
    "amount_before_vat": 0, "discount_pct": 0, "reorder_level": 10,
    "current_qty": 0, "month": 0, "year": 0,
    "item_name": None, "supplier_name": None, "invoice_no": None,
    "notes": None, "category": None, "sheet_category": None,
    "purchase_date": None, "date": None, "time": None,
}


def sanitize_for_json(records: list[dict]) -> list[dict]:
    fixed = 0
    clean = []
    for row in records:
        out = {}
        for k, v in row.items():
            bad = False
            if v is None:
                pass
            elif isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
                bad = True
            elif isinstance(v, str) and v.strip().lower() in ("nan", "nat", "none", ""):
                bad = True
            elif hasattr(v, "item"):
                try:
                    pv = v.item()
                    if isinstance(pv, float) and (math.isnan(pv) or math.isinf(pv)):
                        bad = True
                    else:
                        v = pv
                except Exception:
                    pass
            else:
                try:
                    if pd.isna(v):
                        bad = True
                except (TypeError, ValueError):
                    pass
            if bad:
                v = _NAN_DEFAULTS.get(k)
                fixed += 1
            if hasattr(v, "item"):
                v = v.item()
            out[k] = v
        clean.append(out)
    if fixed:
        logger.info(f"sanitize_for_json: fixed {fixed} NaN values in {len(records)} records")
    return clean


# ═══════════════════════════════════════════════════════════════════
# ETL bulk insert helpers
# ═══════════════════════════════════════════════════════════════════

def bulk_upsert_employees(names: list[str]):
    for name in names:
        if not name or (isinstance(name, float) and pd.isna(name)):
            continue
        try:
            _q("employees").upsert({"name": str(name).strip()}, on_conflict="name").execute()
        except Exception:
            pass


def bulk_upsert_materials(records: list[dict]):
    for rec in sanitize_for_json(records):
        if not rec.get("item_name"):
            continue
        try:
            _q("materials").upsert(rec, on_conflict="item_name").execute()
        except Exception:
            pass


def bulk_insert_requisitions(records: list[dict]):
    records = sanitize_for_json(records)
    for i in range(0, len(records), 200):
        try:
            _q("requisitions").upsert(records[i:i+200], on_conflict="tx_id").execute()
        except Exception as e:
            logger.warning(f"bulk_insert_requisitions batch {i}: {e}")


def bulk_insert_purchases(records: list[dict]):
    records = sanitize_for_json(records)
    for i in range(0, len(records), 200):
        try:
            _q("purchases").insert(records[i:i+200]).execute()
        except Exception as e:
            logger.warning(f"bulk_insert_purchases batch {i}: {e}")


def init_stock_from_materials():
    try:
        mats = _q("materials").select("item_name").execute()
        existing = {r["item_name"] for r in (_q("stock").select("item_name").execute().data or [])}
        for m in (mats.data or []):
            if m["item_name"] not in existing:
                _q("stock").insert({"item_name": m["item_name"], "current_qty": 0}).execute()
    except Exception as e:
        logger.warning(f"init_stock_from_materials: {e}")
