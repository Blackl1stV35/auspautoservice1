"""
Data Store v2: CSV-based CRUD with automatic Git commits.
Windows-compatible. Enhanced with:
  - UUID-based transaction IDs
  - Duplicate issuance prevention (time-window check)
  - Monthly accumulation helpers (VBA "N+" style)
  - Heatmap data builder
  - Per-material anomaly detection
"""
import pandas as pd
import numpy as np
import os
import subprocess
import uuid
from datetime import datetime, timedelta
import logging
import threading

logger = logging.getLogger(__name__)
DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
)

# Cross-platform thread lock (replaces Unix-only fcntl)
_file_lock = threading.Lock()

# Duplicate-prevention window in seconds
DUPLICATE_WINDOW_SECS = 120


# ═══════════════════════════════════════════════════════════════════
# Core I/O
# ═══════════════════════════════════════════════════════════════════

def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def _csv_path(name: str) -> str:
    return os.path.join(DATA_DIR, f"{name}.csv")


def load(name: str) -> pd.DataFrame:
    """Load a CSV by table name. Returns empty DataFrame if missing."""
    p = _csv_path(name)
    if os.path.exists(p):
        try:
            return pd.read_csv(p)
        except Exception as e:
            logger.warning(f"Failed to read {p}: {e}")
    return pd.DataFrame()


def save(name: str, df: pd.DataFrame):
    """Thread-safe write of DataFrame → CSV."""
    _ensure_data_dir()
    with _file_lock:
        df.to_csv(_csv_path(name), index=False)


def append_row(name: str, row: dict) -> pd.DataFrame:
    """Append a single dict-row to a CSV and return updated DataFrame."""
    with _file_lock:
        df = load(name)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        _ensure_data_dir()
        df.to_csv(_csv_path(name), index=False)
    return df


# ═══════════════════════════════════════════════════════════════════
# Convenience loaders (public API used by app.py)
# ═══════════════════════════════════════════════════════════════════

def get_requisitions() -> pd.DataFrame:
    """Requisitions with quantity guaranteed numeric."""
    df = load("requisitions")
    if not df.empty and "quantity" in df.columns:
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)
    return df


def get_employees() -> pd.DataFrame:
    return load("employees")


def get_materials() -> pd.DataFrame:
    return load("materials")


def get_stock() -> pd.DataFrame:
    """Stock with current_qty guaranteed numeric."""
    df = load("stock")
    if not df.empty and "current_qty" in df.columns:
        df["current_qty"] = pd.to_numeric(df["current_qty"], errors="coerce").fillna(0).astype(int)
    return df


def get_purchases() -> pd.DataFrame:
    return load("purchases")


def get_audit_log() -> pd.DataFrame:
    return load("audit_log")


# ═══════════════════════════════════════════════════════════════════
# Audit & Git
# ═══════════════════════════════════════════════════════════════════

def log_audit(user: str, action: str, detail: str, commit: bool = False):
    """
    Append one row to audit_log.csv.
    Args:
        commit: If True, also git-commit immediately after writing.
                Default False because callers like issue_material() /
                add_stock() commit at the end of their own transaction.
                Set True when log_audit is the *only* mutation in a flow
                (e.g. standalone admin notes).
    """
    append_row("audit_log", {
        "timestamp": datetime.now().isoformat(),
        "user": user,
        "action": action,
        "detail": detail,
    })
    if commit:
        git_commit(f"audit: {action} — {detail[:60]}")


def _run_git(args: list[str], root: str) -> subprocess.CompletedProcess:
    """Run a git command and return the CompletedProcess. Logs debug info."""
    cmd = ["git"] + args
    logger.debug(f"Git command: {' '.join(cmd)}  cwd={root}")
    result = subprocess.run(
        cmd, cwd=root, capture_output=True, text=True, timeout=15,
    )
    if result.returncode != 0:
        logger.debug(f"  rc={result.returncode}  "
                     f"stdout={result.stdout.strip()!r}  "
                     f"stderr={result.stderr.strip()!r}")
    return result


def _ensure_git_repo(root: str) -> bool:
    """
    Make sure `root` is a git repository with user identity configured.
    Auto-initialises and configures if missing — the user should never
    have to touch the terminal for git to work.
    """
    git_dir = os.path.join(root, ".git")
    if not os.path.isdir(git_dir):
        logger.info("No .git found — initialising repository automatically")
        r = _run_git(["init"], root)
        if r.returncode != 0:
            logger.warning(f"git init failed: {r.stderr.strip()}")
            return False

    # Ensure user identity (git commit refuses without it)
    for key, default in [("user.email", "sp-auto@local"),
                         ("user.name",  "SP Auto Service")]:
        check = _run_git(["config", key], root)
        if check.returncode != 0 or not check.stdout.strip():
            _run_git(["config", key, default], root)
            logger.info(f"Auto-configured git {key} = {default}")

    return True


def git_commit(message: str) -> bool:
    """
    Stage everything under data/ and commit.

    Handles automatically:
      • No .git yet → runs git init
      • No user.email/name → auto-configures
      • Untracked files → uses 'git add -A data/'
      • Nothing to commit → returns True (not an error)

    Returns True on success, False on genuine failure.
    Never crashes the app.
    """
    try:
        root = os.path.dirname(DATA_DIR)

        # 1. Ensure repo + identity exist
        if not _ensure_git_repo(root):
            return False

        # 2. Stage — use -A to catch new, modified, AND deleted files
        add_result = _run_git(["add", "-A", "data/"], root)
        if add_result.returncode != 0:
            logger.warning(f"git add failed: {add_result.stderr.strip()}")
            return False

        # 3. Check if there is anything staged (avoids a misleading
        #    "nothing to commit" failure on returncode 1)
        status = _run_git(["status", "--porcelain", "data/"], root)
        if status.returncode == 0 and not status.stdout.strip():
            logger.info("Git: nothing to commit (data/ unchanged)")
            return True  # no changes is still success

        # 4. Commit
        commit_result = _run_git(["commit", "-m", message], root)
        if commit_result.returncode == 0:
            logger.info(f"Git commit OK: {message}")
            return True

        # "nothing to commit" can also appear here on some git versions
        combined = commit_result.stdout + commit_result.stderr
        if "nothing to commit" in combined:
            logger.info("Git: nothing to commit (confirmed)")
            return True

        # Genuine failure — log full output for debugging
        logger.warning(
            f"git commit FAILED (rc={commit_result.returncode})\n"
            f"  stdout: {commit_result.stdout.strip()}\n"
            f"  stderr: {commit_result.stderr.strip()}"
        )
        return False

    except FileNotFoundError:
        logger.warning(
            "Git executable not found on PATH. "
            "Install Git from https://git-scm.com and restart the app."
        )
        return False
    except subprocess.TimeoutExpired:
        logger.warning("Git commit timed out (>15s)")
        return False
    except Exception as e:
        logger.warning(f"Git commit unexpected error: {e}", exc_info=True)
        return False


# ═══════════════════════════════════════════════════════════════════
# Transaction ID
# ═══════════════════════════════════════════════════════════════════

def generate_tx_id() -> str:
    """Unique transaction ID: SP-YYYYMMDD-HHMMSS-<short uuid>."""
    now = datetime.now()
    short = uuid.uuid4().hex[:6].upper()
    return f"SP-{now:%Y%m%d}-{now:%H%M%S}-{short}"


# ═══════════════════════════════════════════════════════════════════
# Duplicate detection
# ═══════════════════════════════════════════════════════════════════

def check_duplicate(employee_name: str, material_name: str,
                    quantity: int, window_secs: int = DUPLICATE_WINDOW_SECS) -> bool:
    """
    Return True if an identical (employee, material, quantity) row
    already exists within the last `window_secs` seconds.
    """
    req = load("requisitions")
    if req.empty or "date" not in req.columns or "time" not in req.columns:
        return False

    # Build timestamp from date+time columns
    try:
        req["_ts"] = pd.to_datetime(
            req["date"].astype(str) + " " + req["time"].astype(str),
            errors="coerce",
        )
    except Exception:
        return False

    cutoff = datetime.now() - timedelta(seconds=window_secs)
    recent = req[
        (req["employee_name"] == employee_name)
        & (req["material_name"] == material_name)
        & (req["quantity"].astype(int) == quantity)
        & (req["_ts"] >= cutoff)
    ]
    return len(recent) > 0


# ═══════════════════════════════════════════════════════════════════
# Domain operations
# ═══════════════════════════════════════════════════════════════════

def issue_material(employee_name: str, material_name: str, quantity: int,
                   issued_by: str = "system",
                   skip_dup_check: bool = False) -> dict:
    """
    Record a material issuance. Returns a result dict:
        {"ok": True/False, "tx_id": "...", "msg": "..."}
    """
    # Validation
    if quantity <= 0:
        return {"ok": False, "tx_id": None,
                "msg": "จำนวนต้องมากกว่า 0"}
    if not employee_name or not material_name:
        return {"ok": False, "tx_id": None,
                "msg": "กรุณาเลือกชื่อช่างและวัสดุ"}

    # Duplicate check
    if not skip_dup_check and check_duplicate(employee_name, material_name, quantity):
        return {"ok": False, "tx_id": None,
                "msg": (f"⚠️ พบรายการซ้ำ: {employee_name} เบิก {material_name} "
                        f"x{quantity} ภายใน {DUPLICATE_WINDOW_SECS} วินาทีที่ผ่านมา")}

    now = datetime.now()
    tx_id = generate_tx_id()

    # 1. Append requisition
    row = {
        "tx_id": tx_id,
        "req_id": tx_id,  # keep backward compat
        "employee_name": employee_name,
        "material_name": material_name,
        "quantity": quantity,
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "issued_by": issued_by,
        "month": now.month,
        "year": now.year + 543,
        "sheet": "app_entry",
    }
    append_row("requisitions", row)

    # 2. Decrement stock
    stock = load("stock")
    if not stock.empty and "item_name" in stock.columns:
        mask = stock["item_name"] == material_name
        if mask.any():
            stock["current_qty"] = pd.to_numeric(
                stock["current_qty"], errors="coerce"
            ).fillna(0)
            stock.loc[mask, "current_qty"] -= quantity
            stock.loc[mask, "last_updated"] = now.isoformat()
            save("stock", stock)

    # 3. Audit + Git
    detail = f"{employee_name} เบิก {material_name} x{quantity} [{tx_id}]"
    log_audit(issued_by, "เบิกวัสดุ", detail)
    committed = git_commit(f"เบิก: {detail}")

    return {"ok": True, "tx_id": tx_id, "committed": committed,
            "msg": f"✅ สำเร็จ! {employee_name} เบิก {material_name} x{quantity}"}


def add_stock(material_name: str, quantity: int, user: str = "system") -> dict:
    """Add stock from purchase/receiving. Returns result dict."""
    if quantity <= 0:
        return {"ok": False, "committed": False, "msg": "จำนวนต้องมากกว่า 0"}
    stock = load("stock")
    now = datetime.now()

    if stock.empty or "item_name" not in stock.columns:
        stock = pd.DataFrame([{
            "mat_id": 1, "item_name": material_name,
            "current_qty": quantity, "last_updated": now.isoformat(),
        }])
    else:
        mask = stock["item_name"] == material_name
        if mask.any():
            stock["current_qty"] = pd.to_numeric(
                stock["current_qty"], errors="coerce"
            ).fillna(0)
            stock.loc[mask, "current_qty"] += quantity
            stock.loc[mask, "last_updated"] = now.isoformat()
        else:
            new_id = (int(stock["mat_id"].max()) + 1
                      if "mat_id" in stock.columns else 1)
            stock = pd.concat([stock, pd.DataFrame([{
                "mat_id": new_id, "item_name": material_name,
                "current_qty": quantity, "last_updated": now.isoformat(),
            }])], ignore_index=True)

    save("stock", stock)
    log_audit(user, "รับวัสดุเข้า", f"{material_name} +{quantity}")
    committed = git_commit(f"รับเข้า: {material_name} +{quantity}")
    return {"ok": True, "committed": committed,
            "msg": f"✅ รับเข้า {material_name} +{quantity}"}


# ═══════════════════════════════════════════════════════════════════
# Stock alerts
# ═══════════════════════════════════════════════════════════════════

def get_low_stock(threshold: int = 10) -> pd.DataFrame:
    stock = get_stock()
    if stock.empty or "current_qty" not in stock.columns:
        return pd.DataFrame()
    return stock[stock["current_qty"] <= threshold].sort_values("current_qty")


def get_stock_status(row_qty: int) -> str:
    """Return a Thai status label for a stock quantity."""
    if row_qty <= 0:
        return "🔴 หมด"
    if row_qty <= 5:
        return "🟠 วิกฤต"
    if row_qty <= 10:
        return "🟡 ต่ำ"
    return "🟢 ปกติ"


# ═══════════════════════════════════════════════════════════════════
# Anomaly detection (enhanced: overall + per-material)
# ═══════════════════════════════════════════════════════════════════

def get_anomalies(z_threshold: float = 2.0) -> pd.DataFrame:
    """Flag employees whose TOTAL usage is outlier."""
    req = get_requisitions()
    if req.empty or "employee_name" not in req.columns:
        return pd.DataFrame()
    usage = req.groupby("employee_name")["quantity"].sum().reset_index()
    mean_q, std_q = usage["quantity"].mean(), usage["quantity"].std()
    if std_q == 0 or pd.isna(std_q):
        return pd.DataFrame()
    usage["z_score"] = (usage["quantity"] - mean_q) / std_q
    return (usage[usage["z_score"] > z_threshold]
            .sort_values("z_score", ascending=False))


def get_anomalies_per_material(z_threshold: float = 2.0) -> pd.DataFrame:
    """Flag employee×material pairs that are outliers within each material."""
    req = get_requisitions()
    if req.empty:
        return pd.DataFrame()
    pivot = req.groupby(["employee_name", "material_name"])["quantity"].sum().reset_index()
    # Z-score within each material
    stats = pivot.groupby("material_name")["quantity"].agg(["mean", "std"]).reset_index()
    stats.columns = ["material_name", "mat_mean", "mat_std"]
    merged = pivot.merge(stats, on="material_name")
    merged["z_score"] = np.where(
        merged["mat_std"] > 0,
        (merged["quantity"] - merged["mat_mean"]) / merged["mat_std"],
        0,
    )
    flagged = merged[merged["z_score"] > z_threshold].sort_values("z_score", ascending=False)
    return flagged[["employee_name", "material_name", "quantity", "z_score"]]


# ═══════════════════════════════════════════════════════════════════
# Monthly accumulation (VBA "N+" style)
# ═══════════════════════════════════════════════════════════════════

def get_monthly_summary() -> pd.DataFrame:
    """
    Pivot: rows = employee, columns = month-year, values = total qty.
    Mimics the VBA monthly sheet accumulation.
    """
    req = get_requisitions()
    if req.empty:
        return pd.DataFrame()
    req["period"] = req.apply(
        lambda r: f"{int(r['month']):02d}/{int(r['year'])}"
        if pd.notna(r.get("month")) and pd.notna(r.get("year")) else "ไม่ระบุ",
        axis=1,
    )
    pivot = req.pivot_table(
        index="employee_name", columns="period",
        values="quantity", aggfunc="sum", fill_value=0,
    )
    pivot["รวมทั้งหมด"] = pivot.sum(axis=1)
    return pivot.sort_values("รวมทั้งหมด", ascending=False)


def get_monthly_by_material() -> pd.DataFrame:
    """Pivot: rows = material, columns = month-year, values = total qty."""
    req = get_requisitions()
    if req.empty:
        return pd.DataFrame()
    req["period"] = req.apply(
        lambda r: f"{int(r['month']):02d}/{int(r['year'])}"
        if pd.notna(r.get("month")) and pd.notna(r.get("year")) else "ไม่ระบุ",
        axis=1,
    )
    pivot = req.pivot_table(
        index="material_name", columns="period",
        values="quantity", aggfunc="sum", fill_value=0,
    )
    pivot["รวมทั้งหมด"] = pivot.sum(axis=1)
    return pivot.sort_values("รวมทั้งหมด", ascending=False)


# ═══════════════════════════════════════════════════════════════════
# Heatmap data
# ═══════════════════════════════════════════════════════════════════

def get_usage_heatmap() -> pd.DataFrame:
    """
    Pivot table: rows = employee, columns = material, values = total qty.
    Used by Plotly imshow() for the usage-intensity heatmap.
    """
    req = get_requisitions()
    if req.empty:
        return pd.DataFrame()
    pivot = req.pivot_table(
        index="employee_name", columns="material_name",
        values="quantity", aggfunc="sum", fill_value=0,
    )
    return pivot


def get_available_periods() -> list[str]:
    """Return sorted list of month/year periods present in requisitions."""
    req = get_requisitions()
    if req.empty:
        return []
    req["period"] = req.apply(
        lambda r: f"{int(r['month']):02d}/{int(r['year'])}"
        if pd.notna(r.get("month")) and pd.notna(r.get("year")) else None,
        axis=1,
    )
    periods = sorted(req["period"].dropna().unique().tolist())
    return periods