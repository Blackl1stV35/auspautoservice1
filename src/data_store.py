"""
Data Store: CSV-based CRUD with automatic Git commits (Windows Compatible)
"""

import pandas as pd
import os
import subprocess
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def _csv_path(name: str) -> str:
    return os.path.join(DATA_DIR, f"{name}.csv")

def load(name: str) -> pd.DataFrame:
    """Load CSV or return empty DataFrame"""
    p = _csv_path(name)
    if os.path.exists(p):
        try:
            return pd.read_csv(p)
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()

def save(name: str, df: pd.DataFrame):
    """Save DataFrame to CSV"""
    _ensure_data_dir()
    df.to_csv(_csv_path(name), index=False)

def append_row(name: str, row: dict):
    """Append a single row to CSV"""
    df = load(name)
    new_row = pd.DataFrame([row])
    df = pd.concat([df, new_row], ignore_index=True)
    save(name, df)
    return df

def log_audit(user: str, action: str, detail: str):
    """Log audit entry"""
    append_row("audit_log", {
        "timestamp": datetime.now().isoformat(),
        "user": user,
        "action": action,
        "detail": detail,
    })

def git_commit(message: str = "Auto commit"):
    """Commit changes to git (non-critical)"""
    try:
        project_root = os.path.dirname(DATA_DIR)
        subprocess.run(["git", "add", "data/"], cwd=project_root, capture_output=True, timeout=10)
        subprocess.run(["git", "commit", "-m", message], cwd=project_root, capture_output=True, timeout=10)
    except Exception:
        pass  # Git commit is optional on Windows

# ===================================================================
# Domain-specific operations
# ===================================================================

def issue_material(employee_name: str, material_name: str, quantity: float, issued_by: str = "system"):
    """Record material issuance and update stock"""
    now = datetime.now()
    row = {
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "employee_name": employee_name,
        "material_name": material_name,
        "quantity": quantity,
        "issued_by": issued_by,
    }
    append_row("requisitions", row)

    # Update stock
    stock = load("stock")
    if not stock.empty:
        qty_col = "current_qty" if "current_qty" in stock.columns else "quantity"
        if "item_name" in stock.columns or "material_name" in stock.columns:
            name_col = "item_name" if "item_name" in stock.columns else "material_name"
            mask = stock[name_col] == material_name
            if mask.any():
                stock.loc[mask, qty_col] = stock.loc[mask, qty_col].astype(float) - quantity
                stock.loc[mask, "last_updated"] = now.isoformat()
                save("stock", stock)

    log_audit(issued_by, "เบิกวัสดุ", f"{employee_name} เบิก {material_name} x{quantity}")
    git_commit(f"เบิก: {employee_name} - {material_name} x{quantity}")
    return True


def add_stock(material_name: str, quantity: float, user: str = "system"):
    """Add stock from purchase or receiving"""
    stock = load("stock")
    now = datetime.now()
    qty_col = "current_qty" if "current_qty" in stock.columns else "quantity"
    name_col = "item_name" if "item_name" in stock.columns else "material_name"

    if stock.empty:
        stock = pd.DataFrame([{
            "item_name": material_name,
            qty_col: quantity,
            "last_updated": now.isoformat()
        }])
    else:
        mask = stock[name_col] == material_name
        if mask.any():
            stock.loc[mask, qty_col] = stock.loc[mask, qty_col].astype(float) + quantity
            stock.loc[mask, "last_updated"] = now.isoformat()
        else:
            new_row = pd.DataFrame([{
                "item_name": material_name,
                qty_col: quantity,
                "last_updated": now.isoformat()
            }])
            stock = pd.concat([stock, new_row], ignore_index=True)

    save("stock", stock)
    log_audit(user, "รับวัสดุเข้า", f"{material_name} +{quantity}")
    git_commit(f"รับเข้า: {material_name} +{quantity}")


def get_low_stock(threshold: int = 5) -> pd.DataFrame:
    """Return low stock items"""
    stock = load("stock")
    if stock.empty:
        return pd.DataFrame()
    qty_col = "current_qty" if "current_qty" in stock.columns else "quantity"
    stock[qty_col] = pd.to_numeric(stock[qty_col], errors="coerce").fillna(0)
    return stock[stock[qty_col] <= threshold].sort_values(qty_col)


def get_anomalies(z_threshold: float = 2.0) -> pd.DataFrame:
    """Detect employees with unusually high usage"""
    req = load("requisitions")
    if req.empty or "employee_name" not in req.columns:
        return pd.DataFrame()
    req["quantity"] = pd.to_numeric(req["quantity"], errors="coerce").fillna(0)
    usage = req.groupby("employee_name")["quantity"].sum().reset_index()
    if len(usage) < 2:
        return pd.DataFrame()
    mean_q = usage["quantity"].mean()
    std_q = usage["quantity"].std()
    if std_q == 0:
        return pd.DataFrame()
    usage["z_score"] = (usage["quantity"] - mean_q) / std_q
    return usage[usage["z_score"] > z_threshold].sort_values("z_score", ascending=False)