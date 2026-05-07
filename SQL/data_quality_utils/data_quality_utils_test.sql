-- ============================================================================
-- Data Quality Utilities Test Suite
-- ============================================================================
-- Tests for data quality utility functions across different SQL databases.
-- Run these tests to verify functionality.
--
-- Author: AllToolkit
-- Version: 1.0.0
-- ============================================================================

-- ============================================================================
-- TEST SETUP - Create Test Tables
-- ============================================================================

-- MySQL Setup
DROP TABLE IF EXISTS test_customers;
DROP TABLE IF EXISTS test_orders;
DROP TABLE IF EXISTS test_products;

CREATE TABLE test_customers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    age INT,
    salary DECIMAL(10,2),
    created_at DATE
);

CREATE TABLE test_orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    product_id INT,
    quantity INT,
    total_amount DECIMAL(10,2),
    order_date DATE
);

CREATE TABLE test_products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10,2),
    stock INT
);

-- Insert test data with various data quality issues
INSERT INTO test_customers (name, email, phone, age, salary, created_at) VALUES
('John Doe', 'john@email.com', '1234567890', 25, 50000.00, '2024-01-15'),
('Jane Smith', 'jane@email.com', '2345678901', 30, 65000.00, '2024-01-16'),
('Bob Johnson', NULL, '3456789012', NULL, 45000.00, '2024-01-17'),
('Alice Brown', 'alice@email.com', NULL, 28, 55000.00, '2024-01-18'),
('Charlie Wilson', 'charlie@email.com', '4567890123', 35, 70000.00, '2024-01-19'),
(NULL, 'unknown@email.com', '5678901234', 22, 40000.00, '2024-01-20'),
('Diana Miller', 'invalid-email', '6789012345', -5, 60000.00, '2024-01-21'),
('Eve Davis', 'eve@email.com', '7890123456', 200, 80000.00, '2024-01-22'),
('  John Doe  ', 'john@email.com', '1234567890', 25, 50000.00, '2024-01-23'),
('John Doe', 'john@email.com', '1234567890', 25, 50000.00, '2024-01-15');

INSERT INTO test_orders (customer_id, product_id, quantity, total_amount, order_date) VALUES
(1, 1, 2, 100.00, '2024-02-01'),
(1, 2, 1, 50.00, '2024-02-02'),
(2, 1, 3, 150.00, '2024-02-03'),
(NULL, 1, 1, 50.00, '2024-02-04'),
(3, NULL, 2, NULL, '2024-02-05'),
(1, 1, 2, 100.00, '2024-02-01');

INSERT INTO test_products (name, category, price, stock) VALUES
('Laptop', 'Electronics', 999.99, 50),
('Mouse', 'Electronics', 29.99, 200),
('Keyboard', 'Electronics', 79.99, 150),
('Monitor', 'Electronics', 299.99, 75),
('Laptop', 'Electronics', 999.99, 50);

-- ============================================================================
-- TEST 1: NULL VALUE ANALYSIS
-- ============================================================================

-- Test null_count
SELECT 'TEST 1.1: NULL Count' AS test_name;
SELECT 
    COUNT(*) - COUNT(email) AS email_null_count,
    COUNT(*) - COUNT(phone) AS phone_null_count,
    COUNT(*) - COUNT(age) AS age_null_count
FROM test_customers;

-- Expected: email_null_count = 1, phone_null_count = 1, age_null_count = 2

-- Test null_percentage
SELECT 'TEST 1.2: NULL Percentage' AS test_name;
SELECT 
    COUNT(*) AS total_rows,
    SUM(CASE WHEN email IS NULL THEN 1 ELSE 0 END) AS email_nulls,
    ROUND(100.0 * SUM(CASE WHEN email IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS email_null_pct,
    SUM(CASE WHEN age IS NULL THEN 1 ELSE 0 END) AS age_nulls,
    ROUND(100.0 * SUM(CASE WHEN age IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS age_null_pct
FROM test_customers;

-- Expected: email_null_pct = 10.00, age_null_pct = 20.00

-- ============================================================================
-- TEST 2: DATA COMPLETENESS METRICS
-- ============================================================================

SELECT 'TEST 2.1: Completeness Score' AS test_name;
SELECT 
    COUNT(*) AS total_rows,
    COUNT(email) AS non_null_email,
    ROUND(100.0 * COUNT(email) / COUNT(*), 2) AS email_completeness_pct
FROM test_customers;

-- Expected: email_completeness_pct = 90.00

SELECT 'TEST 2.2: Multi-Column Completeness' AS test_name;
SELECT 
    COUNT(*) AS total_rows,
    SUM(CASE WHEN name IS NOT NULL AND email IS NOT NULL AND phone IS NOT NULL THEN 1 ELSE 0 END) AS complete_rows,
    ROUND(100.0 * SUM(CASE WHEN name IS NOT NULL AND email IS NOT NULL AND phone IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS complete_pct
FROM test_customers;

-- Expected: complete_rows = 7, complete_pct = 70.00

-- ============================================================================
-- TEST 3: DUPLICATION DETECTION
-- ============================================================================

SELECT 'TEST 3.1: Duplicate Values in name column' AS test_name;
SELECT name, COUNT(*) AS duplicate_count
FROM test_customers
GROUP BY name
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC;

-- Expected: 'John Doe' appears 4 times (including whitespace variant)

SELECT 'TEST 3.2: Uniqueness Ratio' AS test_name;
SELECT 
    COUNT(*) AS total_rows,
    COUNT(DISTINCT email) AS unique_emails,
    ROUND(100.0 * COUNT(DISTINCT email) / COUNT(*), 2) AS uniqueness_pct
FROM test_customers;

-- Expected: unique_emails = 8 (10 rows, duplicates exist)

SELECT 'TEST 3.3: Exact Duplicate Rows' AS test_name;
SELECT id, name, email, COUNT(*) AS occurrence_count
FROM test_customers
WHERE name IS NOT NULL AND email IS NOT NULL
GROUP BY id, name, email
HAVING COUNT(*) > 1;

-- ============================================================================
-- TEST 4: DATA TYPE VALIDATION
-- ============================================================================

SELECT 'TEST 4.1: Invalid Emails' AS test_name;
SELECT name, email
FROM test_customers
WHERE email IS NOT NULL
  AND email NOT REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$';

-- Expected: 'invalid-email' should be found

SELECT 'TEST 4.2: Invalid Phone Numbers' AS test_name;
SELECT name, phone
FROM test_customers
WHERE phone IS NOT NULL
  AND phone NOT REGEXP '^[+]?[0-9]{10,15}$';

-- Expected: All phones should be valid format (10 digits)

SELECT 'TEST 4.3: Age Range Validation' AS test_name;
SELECT name, age
FROM test_customers
WHERE age IS NOT NULL AND (age < 0 OR age > 120);

-- Expected: -5 and 200 should be found as invalid

-- ============================================================================
-- TEST 5: OUTLIER DETECTION
-- ============================================================================

SELECT 'TEST 5.1: Statistical Summary for salary' AS test_name;
SELECT 
    COUNT(*) AS row_count,
    COUNT(salary) AS non_null_count,
    MIN(salary) AS min_salary,
    MAX(salary) AS max_salary,
    ROUND(AVG(salary), 2) AS avg_salary,
    ROUND(STDDEV(salary), 2) AS std_dev
FROM test_customers;

-- Expected: avg around 57,500, std_dev around 12,500

SELECT 'TEST 5.2: Values Outside Expected Range (age 0-120)' AS test_name;
SELECT name, age
FROM test_customers
WHERE age IS NOT NULL AND (age < 0 OR age > 120);

-- Expected: -5 and 200

-- ============================================================================
-- TEST 6: STATISTICAL SUMMARIES
-- ============================================================================

SELECT 'TEST 6.1: Distribution Histogram (category)' AS test_name;
SELECT 
    category,
    COUNT(*) AS frequency,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM test_products), 2) AS percentage
FROM test_products
GROUP BY category
ORDER BY frequency DESC;

-- Expected: Electronics = 100%

SELECT 'TEST 6.2: Value Frequency (product name)' AS test_name;
SELECT 
    name,
    COUNT(*) AS frequency
FROM test_products
GROUP BY name
ORDER BY frequency DESC;

-- Expected: Laptop = 2, others = 1

-- ============================================================================
-- TEST 7: DATA PROFILING
-- ============================================================================

SELECT 'TEST 7.1: Table Profile - test_customers' AS test_name;
SELECT 
    'Total Rows' AS metric, COUNT(*) AS value FROM test_customers
UNION ALL
SELECT 'Distinct Names', COUNT(DISTINCT name) FROM test_customers
UNION ALL
SELECT 'NULL Names', SUM(CASE WHEN name IS NULL THEN 1 ELSE 0 END) FROM test_customers
UNION ALL
SELECT 'Empty String Names', SUM(CASE WHEN name = '' THEN 1 ELSE 0 END) FROM test_customers
UNION ALL
SELECT 'Whitespace Only', SUM(CASE WHEN TRIM(name) = '' AND name IS NOT NULL THEN 1 ELSE 0 END) FROM test_customers;

-- Expected: Total Rows = 10, Distinct Names = 8, NULL Names = 1

-- ============================================================================
-- TEST 8: DATA CLEANING OPERATIONS
-- ============================================================================

SELECT 'TEST 8.1: Before Trim - Names with Whitespace' AS test_name;
SELECT id, name, LENGTH(name) AS len, LENGTH(TRIM(name)) AS trimmed_len
FROM test_customers
WHERE name != TRIM(name);

-- Expected: 1 row with extra whitespace

-- Test trim operation (preview, not actual update)
SELECT 'TEST 8.2: Trim Preview' AS test_name;
SELECT id, name AS original, TRIM(name) AS trimmed
FROM test_customers
WHERE name != TRIM(name);

-- ============================================================================
-- TEST 9: COMPREHENSIVE DATA QUALITY SCORE
-- ============================================================================

SELECT 'TEST 9.1: Overall Quality Metrics' AS test_name;
SELECT 
    'name' AS column_name,
    SUM(CASE WHEN name IS NULL THEN 1 ELSE 0 END) AS null_count,
    ROUND(100.0 * SUM(CASE WHEN name IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS null_pct,
    COUNT(DISTINCT name) AS distinct_values,
    ROUND(100.0 * COUNT(DISTINCT name) / COUNT(*), 2) AS uniqueness_pct,
    SUM(CASE WHEN name != TRIM(name) THEN 1 ELSE 0 END) AS whitespace_issues
FROM test_customers
UNION ALL
SELECT 
    'email',
    SUM(CASE WHEN email IS NULL THEN 1 ELSE 0 END),
    ROUND(100.0 * SUM(CASE WHEN email IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2),
    COUNT(DISTINCT email),
    ROUND(100.0 * COUNT(DISTINCT email) / COUNT(*), 2),
    SUM(CASE WHEN email != TRIM(email) THEN 1 ELSE 0 END)
FROM test_customers
UNION ALL
SELECT 
    'age',
    SUM(CASE WHEN age IS NULL THEN 1 ELSE 0 END),
    ROUND(100.0 * SUM(CASE WHEN age IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2),
    COUNT(DISTINCT age),
    ROUND(100.0 * COUNT(DISTINCT age) / COUNT(*), 2),
    0
FROM test_customers;

-- ============================================================================
-- TEST 10: ADVANCED QUERIES
-- ============================================================================

-- Test: Find customers with multiple data quality issues
SELECT 'TEST 10.1: Customers with Multiple Issues' AS test_name;
SELECT 
    id,
    name,
    email,
    phone,
    age,
    (CASE WHEN name IS NULL OR name = '' THEN 1 ELSE 0 END) +
    (CASE WHEN email IS NULL OR email NOT REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$' THEN 1 ELSE 0 END) +
    (CASE WHEN phone IS NULL THEN 1 ELSE 0 END) +
    (CASE WHEN age IS NULL OR age < 0 OR age > 120 THEN 1 ELSE 0 END) AS issue_count
FROM test_customers
HAVING issue_count > 0
ORDER BY issue_count DESC;

-- Test: Cross-table integrity check
SELECT 'TEST 10.2: Orphaned Orders (no matching customer)' AS test_name;
SELECT o.*
FROM test_orders o
LEFT JOIN test_customers c ON o.customer_id = c.id
WHERE o.customer_id IS NOT NULL AND c.id IS NULL;

-- Expected: 0 results (no orphans in test data)

SELECT 'TEST 10.3: Orphaned Products in Orders' AS test_name;
SELECT o.*
FROM test_orders o
LEFT JOIN test_products p ON o.product_id = p.id
WHERE o.product_id IS NOT NULL AND p.id IS NULL;

-- Expected: 0 results

-- ============================================================================
-- CLEANUP
-- ============================================================================

-- Uncomment to clean up test tables
-- DROP TABLE IF EXISTS test_customers;
-- DROP TABLE IF EXISTS test_orders;
-- DROP TABLE IF EXISTS test_products;

-- ============================================================================
-- TEST RESULTS SUMMARY
-- ============================================================================
-- Expected Results:
-- TEST 1.1: email_null_count = 1, phone_null_count = 1, age_null_count = 2
-- TEST 1.2: email_null_pct = 10.00, age_null_pct = 20.00
-- TEST 2.1: email_completeness_pct = 90.00
-- TEST 2.2: complete_rows = 7, complete_pct = 70.00
-- TEST 3.1: 'John Doe' duplicates found
-- TEST 3.2: unique_emails = 8
-- TEST 4.1: 'invalid-email' found
-- TEST 4.3: age values -5 and 200 found
-- TEST 5.1: Statistical summary computed
-- TEST 8.1: 1 row with whitespace found
-- TEST 9.1: Quality metrics computed for all columns
-- ============================================================================