-- ═══════════════════════════════════════════════════════════════
-- SP Auto Service — Supabase Schema
-- Run this ONCE in Supabase Dashboard → SQL Editor → New Query
-- ═══════════════════════════════════════════════════════════════

-- 1. Employees (ช่าง)
CREATE TABLE IF NOT EXISTS employees (
    emp_id    SERIAL PRIMARY KEY,
    name      TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 2. Materials (วัสดุ)
CREATE TABLE IF NOT EXISTS materials (
    mat_id        SERIAL PRIMARY KEY,
    item_name     TEXT NOT NULL UNIQUE,
    category      TEXT DEFAULT 'อื่นๆ',
    unit          TEXT DEFAULT 'ชิ้น',
    reorder_level INT DEFAULT 10,
    created_at    TIMESTAMPTZ DEFAULT now()
);

-- 3. Stock (สต็อก)
CREATE TABLE IF NOT EXISTS stock (
    stock_id     SERIAL PRIMARY KEY,
    item_name    TEXT NOT NULL UNIQUE REFERENCES materials(item_name),
    current_qty  INT NOT NULL DEFAULT 0,
    last_updated TIMESTAMPTZ DEFAULT now()
);

-- 4. Requisitions (รายการเบิก)
CREATE TABLE IF NOT EXISTS requisitions (
    tx_id          TEXT PRIMARY KEY,
    employee_name  TEXT NOT NULL,
    material_name  TEXT NOT NULL,
    quantity       INT NOT NULL CHECK (quantity > 0),
    date           DATE NOT NULL DEFAULT CURRENT_DATE,
    time           TIME NOT NULL DEFAULT CURRENT_TIME,
    issued_by      TEXT DEFAULT 'system',
    month          INT,
    year           INT,
    sheet          TEXT DEFAULT 'app_entry',
    created_at     TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_req_employee ON requisitions(employee_name);
CREATE INDEX IF NOT EXISTS idx_req_material ON requisitions(material_name);
CREATE INDEX IF NOT EXISTS idx_req_date     ON requisitions(date);

-- 5. Purchases (ประวัติการซื้อ)
CREATE TABLE IF NOT EXISTS purchases (
    pur_id         SERIAL PRIMARY KEY,
    item_name      TEXT,
    supplier_name  TEXT,
    quantity       INT DEFAULT 0,
    price_per_unit NUMERIC(12,2),
    total_amount   NUMERIC(12,2),
    amount_before_vat NUMERIC(12,2),
    purchase_date  DATE,
    invoice_no     TEXT,
    notes          TEXT,
    category       TEXT,
    sheet_category TEXT,
    discount_pct   NUMERIC(5,2),
    created_at     TIMESTAMPTZ DEFAULT now()
);

-- 6. Audit log (ประวัติการใช้งาน)
CREATE TABLE IF NOT EXISTS audit_log (
    log_id     SERIAL PRIMARY KEY,
    timestamp  TIMESTAMPTZ DEFAULT now(),
    "user"     TEXT NOT NULL,
    action     TEXT NOT NULL,
    detail     TEXT
);
CREATE INDEX IF NOT EXISTS idx_audit_ts ON audit_log(timestamp DESC);

-- ═══════════════════════════════════════════════════════════════
-- RLS: Disable for service_role usage (enable later for user auth)
-- ═══════════════════════════════════════════════════════════════
ALTER TABLE employees   ENABLE ROW LEVEL SECURITY;
ALTER TABLE materials   ENABLE ROW LEVEL SECURITY;
ALTER TABLE stock       ENABLE ROW LEVEL SECURITY;
ALTER TABLE requisitions ENABLE ROW LEVEL SECURITY;
ALTER TABLE purchases   ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_log   ENABLE ROW LEVEL SECURITY;

-- Allow service_role full access
CREATE POLICY "service_role_all" ON employees    FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON materials    FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON stock        FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON requisitions FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON purchases    FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON audit_log    FOR ALL USING (true) WITH CHECK (true);
