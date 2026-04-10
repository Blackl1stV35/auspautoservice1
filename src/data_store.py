"""
Data Store: CSV-based CRUD with automatic Git commits.
"""
import pandas as pd
import os
import subprocess
from datetime import datetime
import logging
import fcntl

logger = logging.getLogger(__name__)
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def _csv_path(name: str) -> str:
    return os.path.join(DATA_DIR, f"{name}.csv")


def load(name: str) -> pd.DataFrame:
    p = _csv_path(name)
    if os.path.exists(p):
        return pd.read_csv(p)
    return pd.DataFrame()


def save(name: str, df: pd.DataFrame):
    _ensure_data_dir()
    df.to_csv(_csv_path(name), index=False)


def append_row(name: str, row: dict):
    df = load(name)
    new_row = pd.DataFrame([row])
    df = pd.concat([df, new_row], ignore_index=True)
    save(name, df)
    return df


def log_audit(user: str, action: str, detail: str):
    append_row("audit_log", {
        "timestamp": datetime.now().isoformat(),
        "user": user,
        "action": action,
        "detail": detail,
    })


def git_commit(message: str):
    """Commit all changes in data/ to git."""
    try:
        project_root = os.path.dirname(DATA_DIR)
        subprocess.run(["git", "add", "data/"], cwd=project_root,
                        capture_output=True, timeout=10)
        subprocess.run(["git", "commit", "-m", message], cwd=project_root,
                        capture_output=True, timeout=10)
        logger.info(f"Git commit: {message}")
    except Exception as e:
        logger.warning(f"Git commit failed (non-critical): {e}")


# ---------------------------------------------------------------------------
# Domain operations
# ---------------------------------------------------------------------------

def issue_material(employee_name: str, material_name: str, quantity: int, issued_by: str = "system"):
    """Record a material issuance and update stock."""
    now = datetime.now()
    row = {
        "req_id": int(now.timestamp() * 1000),
        "employee_name": employee_name,
        "material_name": material_name,
        "quantity": quantity,
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "issued_by": issued_by,
        "month": now.month,
        "year": now.year + 543,  # Thai year
        "sheet": "app_entry",
    }
    append_row("requisitions", row)

    # Update stock
    stock = load("stock")
    if not stock.empty and "item_name" in stock.columns:
        mask = stock["item_name"] == material_name
        if mask.any():
            stock.loc[mask, "current_qty"] = stock.loc[mask, "current_qty"].astype(int) - quantity
            stock.loc[mask, "last_updated"] = now.isoformat()
            save("stock", stock)

    log_audit(issued_by, "เบิกวัสดุ", f"{employee_name} เบิก {material_name} x{quantity}")
    git_commit(f"เบิก: {employee_name} - {material_name} x{quantity}")
    return True


def add_stock(material_name: str, quantity: int, user: str = "system"):
    """Add stock from purchase/receiving."""
    stock = load("stock")
    now = datetime.now()
    if stock.empty or "item_name" not in stock.columns:
        stock = pd.DataFrame([{
            "mat_id": 1, "item_name": material_name,
            "current_qty": quantity, "last_updated": now.isoformat()
        }])
    else:
        mask = stock["item_name"] == material_name
        if mask.any():
            stock.loc[mask, "current_qty"] = stock.loc[mask, "current_qty"].astype(int) + quantity
            stock.loc[mask, "last_updated"] = now.isoformat()
        else:
            new_id = stock["mat_id"].max() + 1 if "mat_id" in stock.columns else 1
            new_row = pd.DataFrame([{
                "mat_id": int(new_id), "item_name": material_name,
                "current_qty": quantity, "last_updated": now.isoformat()
            }])
            stock = pd.concat([stock, new_row], ignore_index=True)
    save("stock", stock)
    log_audit(user, "รับวัสดุเข้า", f"{material_name} +{quantity}")
    git_commit(f"รับเข้า: {material_name} +{quantity}")


def get_low_stock(threshold: int = 10) -> pd.DataFrame:
    stock = load("stock")
    if stock.empty:
        return pd.DataFrame()
    stock["current_qty"] = pd.to_numeric(stock["current_qty"], errors="coerce").fillna(0).astype(int)
    return stock[stock["current_qty"] <= threshold].sort_values("current_qty")


def get_anomalies(z_threshold: float = 2.0) -> pd.DataFrame:
    """Flag employees whose total usage is > z_threshold standard deviations above mean."""
    req = load("requisitions")
    if req.empty or "employee_name" not in req.columns:
        return pd.DataFrame()
    req["quantity"] = pd.to_numeric(req["quantity"], errors="coerce").fillna(0)
    usage = req.groupby("employee_name")["quantity"].sum().reset_index()
    mean_q = usage["quantity"].mean()
    std_q = usage["quantity"].std()
    if std_q == 0:
        return pd.DataFrame()
    usage["z_score"] = (usage["quantity"] - mean_q) / std_q
    return usage[usage["z_score"] > z_threshold].sort_values("z_score", ascending=False)
