"""
Data Store: CSV-based CRUD with automatic Git commits.
Windows-compatible (no fcntl dependency).
"""
import pandas as pd
import os
import subprocess
from datetime import datetime
import logging
import threading

logger = logging.getLogger(__name__)
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

# Thread lock replaces fcntl for cross-platform file safety
_file_lock = threading.Lock()


def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def _csv_path(name: str) -> str:
    return os.path.join(DATA_DIR, f"{name}.csv")


# ---------------------------------------------------------------------------
# Core I/O
# ---------------------------------------------------------------------------

def load(name: str) -> pd.DataFrame:
    """Load a CSV from data/ by table name. Returns empty DataFrame if missing."""
    p = _csv_path(name)
    if os.path.exists(p):
        try:
            return pd.read_csv(p)
        except Exception as e:
            logger.warning(f"Failed to read {p}: {e}")
    return pd.DataFrame()


def save(name: str, df: pd.DataFrame):
    """Save a DataFrame to data/<name>.csv (thread-safe)."""
    _ensure_data_dir()
    with _file_lock:
        df.to_csv(_csv_path(name), index=False)


def append_row(name: str, row: dict) -> pd.DataFrame:
    """Append a single row dict to a CSV and return the updated DataFrame."""
    with _file_lock:
        df = load(name)
        new_row = pd.DataFrame([row])
        df = pd.concat([df, new_row], ignore_index=True)
        _ensure_data_dir()
        df.to_csv(_csv_path(name), index=False)
    return df


# ---------------------------------------------------------------------------
# Convenience loaders (called by app.py)
# ---------------------------------------------------------------------------

def get_requisitions() -> pd.DataFrame:
    """Return the requisitions table with quantity as numeric."""
    df = load("requisitions")
    if not df.empty and "quantity" in df.columns:
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)
    return df


def get_employees() -> pd.DataFrame:
    return load("employees")


def get_materials() -> pd.DataFrame:
    return load("materials")


def get_stock() -> pd.DataFrame:
    """Return stock table with current_qty guaranteed numeric."""
    df = load("stock")
    if not df.empty and "current_qty" in df.columns:
        df["current_qty"] = pd.to_numeric(df["current_qty"], errors="coerce").fillna(0).astype(int)
    return df


def get_purchases() -> pd.DataFrame:
    return load("purchases")


def get_audit_log() -> pd.DataFrame:
    return load("audit_log")


# ---------------------------------------------------------------------------
# Audit & Git
# ---------------------------------------------------------------------------

def log_audit(user: str, action: str, detail: str):
    """Append one row to audit_log.csv."""
    append_row("audit_log", {
        "timestamp": datetime.now().isoformat(),
        "user": user,
        "action": action,
        "detail": detail,
    })


def git_commit(message: str):
    """Commit all changes in data/ to git (best-effort, never crashes app)."""
    try:
        project_root = os.path.dirname(DATA_DIR)
        subprocess.run(["git", "add", "data/"], cwd=project_root,
                       capture_output=True, timeout=10)
        subprocess.run(["git", "commit", "-m", message], cwd=project_root,
                       capture_output=True, timeout=10)
        logger.info(f"Git commit: {message}")
    except FileNotFoundError:
        logger.warning("Git not found on PATH — skipping commit")
    except Exception as e:
        logger.warning(f"Git commit failed (non-critical): {e}")


# ---------------------------------------------------------------------------
# Domain operations
# ---------------------------------------------------------------------------

def issue_material(employee_name: str, material_name: str, quantity: int,
                   issued_by: str = "system") -> bool:
    """Record a material issuance and decrement stock. Returns True on success."""
    now = datetime.now()

    # 1. Append to requisitions
    row = {
        "req_id": int(now.timestamp() * 1000),
        "employee_name": employee_name,
        "material_name": material_name,
        "quantity": quantity,
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "issued_by": issued_by,
        "month": now.month,
        "year": now.year + 543,  # Buddhist Era
        "sheet": "app_entry",
    }
    append_row("requisitions", row)

    # 2. Decrement stock
    stock = load("stock")
    if not stock.empty and "item_name" in stock.columns:
        mask = stock["item_name"] == material_name
        if mask.any():
            stock["current_qty"] = pd.to_numeric(stock["current_qty"], errors="coerce").fillna(0)
            stock.loc[mask, "current_qty"] = stock.loc[mask, "current_qty"] - quantity
            stock.loc[mask, "last_updated"] = now.isoformat()
            save("stock", stock)

    # 3. Audit + Git
    log_audit(issued_by, "เบิกวัสดุ",
              f"{employee_name} เบิก {material_name} x{quantity}")
    git_commit(f"เบิก: {employee_name} - {material_name} x{quantity}")
    return True


def add_stock(material_name: str, quantity: int, user: str = "system"):
    """Add stock from purchase/receiving."""
    stock = load("stock")
    now = datetime.now()

    if stock.empty or "item_name" not in stock.columns:
        stock = pd.DataFrame([{
            "mat_id": 1,
            "item_name": material_name,
            "current_qty": quantity,
            "last_updated": now.isoformat(),
        }])
    else:
        mask = stock["item_name"] == material_name
        if mask.any():
            stock["current_qty"] = pd.to_numeric(stock["current_qty"], errors="coerce").fillna(0)
            stock.loc[mask, "current_qty"] = stock.loc[mask, "current_qty"] + quantity
            stock.loc[mask, "last_updated"] = now.isoformat()
        else:
            new_id = int(stock["mat_id"].max()) + 1 if "mat_id" in stock.columns else 1
            new_row = pd.DataFrame([{
                "mat_id": new_id,
                "item_name": material_name,
                "current_qty": quantity,
                "last_updated": now.isoformat(),
            }])
            stock = pd.concat([stock, new_row], ignore_index=True)

    save("stock", stock)
    log_audit(user, "รับวัสดุเข้า", f"{material_name} +{quantity}")
    git_commit(f"รับเข้า: {material_name} +{quantity}")


def get_low_stock(threshold: int = 10) -> pd.DataFrame:
    """Return stock items at or below the threshold."""
    stock = get_stock()
    if stock.empty or "current_qty" not in stock.columns:
        return pd.DataFrame()
    return stock[stock["current_qty"] <= threshold].sort_values("current_qty")


def get_anomalies(z_threshold: float = 2.0) -> pd.DataFrame:
    """Flag employees whose total usage is > z_threshold std-devs above mean."""
    req = get_requisitions()
    if req.empty or "employee_name" not in req.columns:
        return pd.DataFrame()

    usage = req.groupby("employee_name")["quantity"].sum().reset_index()
    mean_q = usage["quantity"].mean()
    std_q = usage["quantity"].std()
    if std_q == 0 or pd.isna(std_q):
        return pd.DataFrame()

    usage["z_score"] = (usage["quantity"] - mean_q) / std_q
    flagged = usage[usage["z_score"] > z_threshold].sort_values("z_score", ascending=False)
    return flagged
