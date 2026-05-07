-- ============================================================================
-- Data Quality Utilities - Usage Examples
-- ============================================================================
-- Real-world examples for using data quality utilities in SQL.
-- Copy and adapt these queries for your own database.
--
-- Author: AllToolkit
-- Version: 1.0.0
-- ============================================================================

-- ============================================================================
-- EXAMPLE 1: Data Quality Dashboard
-- ============================================================================
-- Generate a comprehensive data quality report for a table

-- Example: Complete quality dashboard for a customers table
SELECT 
    'customers' AS table_name,
    (SELECT COUNT(*) FROM customers) AS total_rows,
    (SELECT COUNT(DISTINCT id) FROM customers) AS unique_ids,
    (SELECT ROUND(100.0 * COUNT(email) / NULLIF(COUNT(*), 0), 2) FROM customers) AS email_completeness,
    (SELECT ROUND(100.0 * COUNT(phone) / NULLIF(COUNT(*), 0), 2) FROM customers) AS phone_completeness,
    (SELECT COUNT(*) FROM customers WHERE email NOT REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$') AS invalid_emails,
    (SELECT COUNT(*) FROM customers WHERE phone NOT REGEXP '^[+]?[0-9]{10,15}$') AS invalid_phones;

-- ============================================================================
-- EXAMPLE 2: Find and Fix Common Data Issues
-- ============================================================================

-- Step 1: Find all duplicate emails
SELECT email, COUNT(*) AS duplicate_count
FROM customers
GROUP BY email
HAVING COUNT(*) > 1;

-- Step 2: Keep only the first occurrence (highest priority) of duplicates
-- MySQL approach
DELETE c1 FROM customers c1
INNER JOIN customers c2
WHERE c1.id > c2.id AND c1.email = c2.email;

-- Step 3: Trim whitespace from names
UPDATE customers 
SET name = TRIM(name)
WHERE name != TRIM(name);

-- Step 4: Standardize email case
UPDATE customers 
SET email = LOWER(email)
WHERE email != LOWER(email);

-- ============================================================================
-- EXAMPLE 3: Data Completeness Report by Column
-- ============================================================================

-- For PostgreSQL - dynamic column analysis
SELECT 
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'customers'
ORDER BY ordinal_position;

-- Detailed completeness per column
SELECT 
    'id' AS column_name,
    COUNT(*) AS total_rows,
    SUM(CASE WHEN id IS NULL THEN 1 ELSE 0 END) AS null_count,
    ROUND(100.0 * SUM(CASE WHEN id IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS null_pct
FROM customers
UNION ALL
SELECT 'name', COUNT(*), SUM(CASE WHEN name IS NULL THEN 1 ELSE 0 END), 
       ROUND(100.0 * SUM(CASE WHEN name IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2)
FROM customers
UNION ALL
SELECT 'email', COUNT(*), SUM(CASE WHEN email IS NULL THEN 1 ELSE 0 END),
       ROUND(100.0 * SUM(CASE WHEN email IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2)
FROM customers;

-- ============================================================================
-- EXAMPLE 4: Validate Data Against Business Rules
-- ============================================================================

-- Rule 1: Age must be between 18 and 120
SELECT id, name, age
FROM customers
WHERE age IS NOT NULL AND (age < 18 OR age > 120);

-- Rule 2: Email must be unique and valid
SELECT email, COUNT(*) AS occurrences
FROM customers
WHERE email IS NOT NULL
GROUP BY email
HAVING COUNT(*) > 1;

-- Rule 3: Total order amount must be positive
SELECT *
FROM orders
WHERE total_amount <= 0;

-- Rule 4: Order date cannot be in the future
SELECT *
FROM orders
WHERE order_date > CURRENT_DATE;

-- ============================================================================
-- EXAMPLE 5: Statistical Analysis for Anomaly Detection
-- ============================================================================

-- Find outliers using standard deviation (values > 3 std from mean)
WITH stats AS (
    SELECT 
        AVG(order_amount) AS mean_val,
        STDDEV(order_amount) AS std_val
    FROM orders
    WHERE order_amount IS NOT NULL
)
SELECT 
    o.*,
    ROUND((o.order_amount - s.mean_val) / NULLIF(s.std_val, 0), 2) AS z_score
FROM orders o, stats s
WHERE ABS(o.order_amount - s.mean_val) / NULLIF(s.std_val, 0) > 3;

-- Find outliers using IQR method
WITH quartiles AS (
    SELECT 
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY price) AS q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY price) AS q3
    FROM products
    WHERE price IS NOT NULL
)
SELECT p.*
FROM products p, quartiles q
WHERE p.price < q.q1 - 1.5 * (q.q3 - q.q1)
   OR p.price > q.q3 + 1.5 * (q.q3 - q.q1);

-- ============================================================================
-- EXAMPLE 6: Data Reconciliation Between Tables
-- ============================================================================

-- Find orphaned records (orders without customers)
SELECT o.id AS order_id, o.customer_id
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.id
WHERE c.id IS NULL;

-- Find mismatched totals (order total != sum of line items)
SELECT 
    o.id AS order_id,
    o.total_amount AS order_total,
    SUM(oi.quantity * oi.price) AS calculated_total,
    o.total_amount - SUM(oi.quantity * oi.price) AS difference
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
GROUP BY o.id, o.total_amount
HAVING ABS(o.total_amount - SUM(oi.quantity * oi.price)) > 0.01;

-- ============================================================================
-- EXAMPLE 7: Time-Based Quality Analysis
-- ============================================================================

-- Quality trends over time
SELECT 
    DATE(created_at) AS date,
    COUNT(*) AS new_records,
    SUM(CASE WHEN email IS NULL THEN 1 ELSE 0 END) AS null_emails,
    SUM(CASE WHEN phone IS NULL THEN 1 ELSE 0 END) AS null_phones,
    ROUND(100.0 * SUM(CASE WHEN email IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS email_null_rate
FROM customers
GROUP BY DATE(created_at)
ORDER BY date DESC;

-- Compare quality metrics month over month
SELECT 
    DATE_FORMAT(created_at, '%Y-%m') AS month,
    COUNT(*) AS total_records,
    COUNT(DISTINCT email) AS unique_emails,
    COUNT(email) * 100.0 / COUNT(*) AS email_fill_rate
FROM customers
GROUP BY DATE_FORMAT(created_at, '%Y-%m')
ORDER BY month DESC;

-- ============================================================================
-- EXAMPLE 8: Cleaning Pipeline
-- ============================================================================

-- Complete data cleaning workflow
-- Step 1: Create backup
CREATE TABLE customers_backup AS SELECT * FROM customers;

-- Step 2: Fix whitespace issues
UPDATE customers SET name = TRIM(name) WHERE name != TRIM(name);
UPDATE customers SET email = TRIM(email) WHERE email != TRIM(email);

-- Step 3: Standardize case
UPDATE customers SET email = LOWER(email);

-- Step 4: Handle NULL values
UPDATE customers SET phone = 'N/A' WHERE phone IS NULL;

-- Step 5: Remove exact duplicates (keep highest ID)
DELETE c1 FROM customers c1
INNER JOIN customers c2
WHERE c1.id < c2.id 
  AND c1.email = c2.email 
  AND c1.name <=> c2.name;

-- Step 6: Validate and flag invalid records
ALTER TABLE customers ADD COLUMN IF NOT EXISTS data_quality_flag VARCHAR(20);

UPDATE customers 
SET data_quality_flag = CASE
    WHEN email NOT REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$' THEN 'invalid_email'
    WHEN phone = 'N/A' THEN 'missing_phone'
    WHEN name IS NULL OR name = '' THEN 'missing_name'
    ELSE 'valid'
END;

-- ============================================================================
-- EXAMPLE 9: Quality Scoring
-- ============================================================================

-- Calculate quality score for each record
SELECT 
    id,
    name,
    email,
    phone,
    (
        (CASE WHEN name IS NOT NULL AND name != '' THEN 25 ELSE 0 END) +
        (CASE WHEN email IS NOT NULL AND email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$' THEN 25 ELSE 0 END) +
        (CASE WHEN phone IS NOT NULL AND phone REGEXP '^[+]?[0-9]{10,15}$' THEN 25 ELSE 0 END) +
        (CASE WHEN created_at IS NOT NULL THEN 25 ELSE 0 END)
    ) AS quality_score
FROM customers
ORDER BY quality_score DESC;

-- ============================================================================
-- EXAMPLE 10: Automated Quality Monitoring
-- ============================================================================

-- Create a view for ongoing quality monitoring
CREATE OR REPLACE VIEW v_data_quality_metrics AS
SELECT 
    'customers' AS table_name,
    CURRENT_DATE AS check_date,
    (SELECT COUNT(*) FROM customers) AS total_records,
    (SELECT COUNT(*) FROM customers WHERE email IS NULL) AS null_emails,
    (SELECT COUNT(*) FROM customers WHERE phone IS NULL) AS null_phones,
    (SELECT COUNT(*) FROM customers WHERE name IS NULL OR name = '') AS null_names,
    (SELECT COUNT(DISTINCT email) FROM customers WHERE email IS NOT NULL) AS unique_emails,
    (SELECT COUNT(*) FROM customers WHERE email NOT REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$') AS invalid_emails;

-- Log daily quality metrics
CREATE TABLE IF NOT EXISTS data_quality_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(100),
    metric_name VARCHAR(100),
    metric_value DECIMAL(10,2),
    check_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert daily metrics
INSERT INTO data_quality_log (table_name, metric_name, metric_value, check_date)
SELECT 
    'customers', 'total_records', COUNT(*), CURRENT_DATE
FROM customers
UNION ALL
SELECT 
    'customers', 'null_email_rate', 
    ROUND(100.0 * SUM(CASE WHEN email IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2), CURRENT_DATE
FROM customers;

-- ============================================================================
-- EXAMPLE 11: Cross-Database Quality Queries
-- ============================================================================

-- PostgreSQL version of quality report
/*
SELECT 
    table_name,
    column_name,
    null_frac * 100 AS null_percentage,
    n_distinct AS distinct_values_estimate
FROM pg_stats
WHERE schemaname = 'public'
ORDER BY table_name, null_frac DESC;
*/

-- SQL Server version of quality report
/*
SELECT 
    t.name AS table_name,
    c.name AS column_name,
    ty.name AS data_type
FROM sys.tables t
JOIN sys.columns c ON t.object_id = c.object_id
JOIN sys.types ty ON c.user_type_id = ty.user_type_id
ORDER BY t.name, c.column_id;
*/