-- ═══════════════════════════════════════════════════════════════
-- SP Auto Service — Performance Views & Indexes
-- Run AFTER the base schema (db_schema.sql) is already in place.
-- ═══════════════════════════════════════════════════════════════

-- Additional indexes for cost analysis
CREATE INDEX IF NOT EXISTS idx_pur_date     ON purchases(purchase_date);
CREATE INDEX IF NOT EXISTS idx_pur_supplier ON purchases(supplier_name);
CREATE INDEX IF NOT EXISTS idx_pur_category ON purchases(sheet_category);
CREATE INDEX IF NOT EXISTS idx_pur_item     ON purchases(item_name);

-- Monthly cost summary view (pushed to PostgreSQL)
CREATE OR REPLACE VIEW v_monthly_cost AS
SELECT
    to_char(purchase_date, 'YYYY-MM') AS period,
    sheet_category,
    supplier_name,
    COUNT(*)                          AS tx_count,
    SUM(COALESCE(total_amount, 0))    AS total_cost,
    SUM(COALESCE(quantity, 0))        AS total_qty,
    AVG(COALESCE(price_per_unit, 0))  AS avg_unit_price
FROM purchases
WHERE purchase_date IS NOT NULL
GROUP BY period, sheet_category, supplier_name
ORDER BY period DESC;

-- Supplier ranking view
CREATE OR REPLACE VIEW v_supplier_rank AS
SELECT
    supplier_name,
    COUNT(*)                          AS order_count,
    SUM(COALESCE(total_amount, 0))    AS total_spend,
    SUM(COALESCE(quantity, 0))        AS total_qty,
    COUNT(DISTINCT item_name)         AS unique_items,
    MIN(purchase_date)                AS first_order,
    MAX(purchase_date)                AS last_order
FROM purchases
WHERE supplier_name IS NOT NULL
GROUP BY supplier_name
ORDER BY total_spend DESC;

-- Price history per item+supplier (for volatility detection)
CREATE OR REPLACE VIEW v_price_history AS
SELECT
    item_name,
    supplier_name,
    purchase_date,
    price_per_unit,
    total_amount,
    quantity,
    LAG(price_per_unit) OVER (
        PARTITION BY item_name, supplier_name ORDER BY purchase_date
    ) AS prev_price,
    CASE WHEN LAG(price_per_unit) OVER (
        PARTITION BY item_name, supplier_name ORDER BY purchase_date
    ) > 0 THEN
        ROUND(((price_per_unit - LAG(price_per_unit) OVER (
            PARTITION BY item_name, supplier_name ORDER BY purchase_date
        )) / LAG(price_per_unit) OVER (
            PARTITION BY item_name, supplier_name ORDER BY purchase_date
        ) * 100)::numeric, 1)
    ELSE NULL END AS pct_change
FROM purchases
WHERE price_per_unit > 0 AND purchase_date IS NOT NULL
ORDER BY item_name, purchase_date;

-- Category cost breakdown view
CREATE OR REPLACE VIEW v_category_cost AS
SELECT
    sheet_category AS category,
    COUNT(*)                        AS item_count,
    SUM(COALESCE(total_amount, 0))  AS total_cost,
    AVG(COALESCE(total_amount, 0))  AS avg_cost
FROM purchases
WHERE sheet_category IS NOT NULL
GROUP BY sheet_category
ORDER BY total_cost DESC;

-- Cost vs Usage linkage: purchased qty vs issued qty per material
CREATE OR REPLACE VIEW v_cost_vs_usage AS
SELECT
    COALESCE(p.item_name, r.material_name) AS item_name,
    COALESCE(p.purchased_qty, 0)           AS purchased_qty,
    COALESCE(p.purchase_cost, 0)           AS purchase_cost,
    COALESCE(r.issued_qty, 0)              AS issued_qty,
    COALESCE(s.current_qty, 0)             AS current_stock,
    CASE
        WHEN COALESCE(r.issued_qty, 0) = 0 THEN 'ไม่มีการเบิก'
        WHEN COALESCE(p.purchased_qty, 0) > COALESCE(r.issued_qty, 0) * 2 THEN 'สต็อกเกิน'
        WHEN COALESCE(s.current_qty, 0) <= 5 THEN 'สต็อกต่ำ'
        ELSE 'ปกติ'
    END AS stock_status
FROM
    (SELECT item_name,
            SUM(COALESCE(quantity, 0)) AS purchased_qty,
            SUM(COALESCE(total_amount, 0)) AS purchase_cost
     FROM purchases GROUP BY item_name) p
FULL OUTER JOIN
    (SELECT material_name,
            SUM(quantity) AS issued_qty
     FROM requisitions GROUP BY material_name) r
    ON p.item_name = r.material_name
LEFT JOIN stock s ON s.item_name = COALESCE(p.item_name, r.material_name);

-- Requisition usage by employee aggregated (for fast mechanic reports)
CREATE OR REPLACE VIEW v_employee_usage AS
SELECT
    employee_name,
    material_name,
    month,
    year,
    SUM(quantity) AS total_qty,
    COUNT(*)      AS tx_count
FROM requisitions
GROUP BY employee_name, material_name, month, year;

-- Enable RLS policies on views (read-only)
-- Views inherit the base table policies automatically in Supabase.

-- Notify PostgREST to reload the schema cache
NOTIFY pgrst, 'reload schema';
