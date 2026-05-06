-- ============================================================================
-- SQL Aggregation Utilities Module - Test Suite
-- ============================================================================
-- Comprehensive test suite for aggregation utility functions
-- Tests are designed to work across MySQL 8.0+, PostgreSQL, SQL Server, 
-- and SQLite 3.25+
--
-- Author: AllToolkit
-- Version: 1.0.0
-- Date: 2026-05-07
-- ============================================================================

-- ============================================================================
-- TEST SETUP - Create sample tables and data
-- ============================================================================

-- Create test tables (adjust syntax for your database)
-- MySQL / PostgreSQL / SQLite:
CREATE TABLE IF NOT EXISTS test_employees (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(50),
    salary DECIMAL(10, 2),
    hire_date DATE,
    status VARCHAR(20),
    bonus DECIMAL(10, 2)
);

CREATE TABLE IF NOT EXISTS test_sales (
    id INTEGER PRIMARY KEY,
    product VARCHAR(50),
    region VARCHAR(50),
    country VARCHAR(50),
    sale_date DATE,
    amount DECIMAL(10, 2),
    quantity INTEGER
);

CREATE TABLE IF NOT EXISTS test_daily_sales (
    sale_date DATE PRIMARY KEY,
    amount DECIMAL(10, 2)
);

CREATE TABLE IF NOT EXISTS test_events (
    id INTEGER PRIMARY KEY,
    event_name VARCHAR(100),
    created_at TIMESTAMP,
    category VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS test_customers (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    age INTEGER,
    income DECIMAL(10, 2),
    spending DECIMAL(10, 2)
);

-- Insert test data
INSERT INTO test_employees (id, name, department, salary, hire_date, status, bonus) VALUES
(1, 'Alice', 'Engineering', 85000.00, '2020-01-15', 'active', 5000.00),
(2, 'Bob', 'Engineering', 95000.00, '2019-06-01', 'active', 7500.00),
(3, 'Charlie', 'Engineering', 75000.00, '2021-03-20', 'active', NULL),
(4, 'Diana', 'Sales', 65000.00, '2020-07-10', 'active', 3000.00),
(5, 'Eve', 'Sales', 70000.00, '2018-11-05', 'active', 4000.00),
(6, 'Frank', 'Sales', 60000.00, '2022-02-28', 'inactive', NULL),
(7, 'Grace', 'Marketing', 72000.00, '2021-05-15', 'active', 2500.00),
(8, 'Henry', 'Marketing', 68000.00, '2019-09-01', 'active', 2000.00),
(9, 'Ivy', 'Marketing', 80000.00, '2020-12-01', 'inactive', NULL),
(10, 'Jack', 'Engineering', 100000.00, '2017-04-01', 'active', 10000.00);

INSERT INTO test_sales (id, product, region, country, sale_date, amount, quantity) VALUES
(1, 'Laptop', 'North', 'USA', '2024-01-15', 1200.00, 5),
(2, 'Laptop', 'North', 'Canada', '2024-01-16', 1150.00, 3),
(3, 'Phone', 'South', 'Mexico', '2024-01-17', 800.00, 10),
(4, 'Phone', 'South', 'Brazil', '2024-01-18', 750.00, 8),
(5, 'Tablet', 'East', 'Japan', '2024-02-01', 500.00, 15),
(6, 'Tablet', 'East', 'China', '2024-02-02', 450.00, 20),
(7, 'Laptop', 'West', 'Germany', '2024-02-15', 1100.00, 4),
(8, 'Phone', 'West', 'France', '2024-02-16', 850.00, 6),
(9, 'Tablet', 'North', 'USA', '2024-03-01', 480.00, 12),
(10, 'Laptop', 'South', 'Mexico', '2024-03-15', 1250.00, 2);

INSERT INTO test_daily_sales (sale_date, amount) VALUES
('2024-01-01', 1000.00),
('2024-01-02', 1500.00),
('2024-01-03', 1200.00),
('2024-01-04', 1800.00),
('2024-01-05', 2000.00),
('2024-01-06', 1600.00),
('2024-01-07', 2200.00),
('2024-01-08', 1900.00),
('2024-01-09', 2100.00),
('2024-01-10', 2500.00);

INSERT INTO test_customers (id, name, age, income, spending) VALUES
(1, 'Customer A', 22, 35000.00, 2500.00),
(2, 'Customer B', 28, 45000.00, 3200.00),
(3, 'Customer C', 35, 65000.00, 4500.00),
(4, 'Customer D', 42, 85000.00, 6000.00),
(5, 'Customer E', 55, 120000.00, 8000.00),
(6, 'Customer F', 19, 28000.00, 1800.00),
(7, 'Customer G', 31, 55000.00, 4000.00),
(8, 'Customer H', 48, 95000.00, 7000.00);

-- ============================================================================
-- TEST 1: CONDITIONAL AGGREGATION
-- ============================================================================

-- Test 1.1: Conditional count
SELECT 'Test 1.1: Conditional Count' as test_name;
SELECT 
    department,
    COUNT(*) as total_employees,
    COUNT(CASE WHEN status = 'active' THEN 1 END) as active_count,
    COUNT(CASE WHEN status = 'inactive' THEN 1 END) as inactive_count,
    COUNT(CASE WHEN salary > 75000 THEN 1 END) as high_earners
FROM test_employees
GROUP BY department
ORDER BY department;

-- Expected: Each department shows correct counts for each category

-- Test 1.2: Conditional sum
SELECT 'Test 1.2: Conditional Sum' as test_name;
SELECT 
    region,
    SUM(amount) as total_sales,
    SUM(CASE WHEN product = 'Laptop' THEN amount ELSE 0 END) as laptop_sales,
    SUM(CASE WHEN product = 'Phone' THEN amount ELSE 0 END) as phone_sales,
    SUM(CASE WHEN product = 'Tablet' THEN amount ELSE 0 END) as tablet_sales
FROM test_sales
GROUP BY region
ORDER BY region;

-- Expected: Regional sales broken down by product type

-- Test 1.3: Percentage breakdown
SELECT 'Test 1.3: Percentage Breakdown' as test_name;
SELECT 
    department,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM test_employees
GROUP BY department
ORDER BY count DESC;

-- Expected: Departments with count and percentage of total

-- ============================================================================
-- TEST 2: STATISTICAL AGGREGATION
-- ============================================================================

-- Test 2.1: Variance and Standard Deviation (syntax varies by DB)
SELECT 'Test 2.1: Statistical Measures' as test_name;
-- MySQL 8.0+:
SELECT 
    department,
    ROUND(AVG(salary), 2) as avg_salary,
    ROUND(VARIANCE(salary), 2) as salary_variance,
    ROUND(STDDEV(salary), 2) as salary_stddev
FROM test_employees
GROUP BY department
HAVING COUNT(*) > 1
ORDER BY department;

-- PostgreSQL equivalent:
-- SELECT 
--     department,
--     ROUND(AVG(salary)::numeric, 2) as avg_salary,
--     ROUND(VAR_POP(salary)::numeric, 2) as salary_variance,
--     ROUND(STDDEV_POP(salary)::numeric, 2) as salary_stddev
-- FROM test_employees
-- GROUP BY department
-- HAVING COUNT(*) > 1
-- ORDER BY department;

-- SQLite equivalent:
-- SELECT 
--     department,
--     ROUND(AVG(salary), 2) as avg_salary,
--     ROUND(AVG(salary * salary) - AVG(salary) * AVG(salary), 2) as salary_variance,
--     ROUND(SQRT(AVG(salary * salary) - AVG(salary) * AVG(salary)), 2) as salary_stddev
-- FROM test_employees
-- GROUP BY department
-- HAVING COUNT(*) > 1
-- ORDER BY department;

-- Test 2.2: Median calculation (using window functions)
SELECT 'Test 2.2: Median Calculation' as test_name;
WITH ranked AS (
    SELECT 
        department,
        salary,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary) as rn,
        COUNT(*) OVER (PARTITION BY department) as cnt
    FROM test_employees
    WHERE status = 'active'
)
SELECT 
    department,
    ROUND(AVG(salary), 2) as median_salary
FROM ranked
WHERE rn IN ((cnt + 1) / 2, (cnt + 2) / 2)
GROUP BY department
ORDER BY department;

-- Expected: Median salary for each department

-- Test 2.3: Mode calculation
SELECT 'Test 2.3: Mode Calculation' as test_name;
WITH value_counts AS (
    SELECT 
        department,
        salary,
        COUNT(*) as frequency,
        RANK() OVER (PARTITION BY department ORDER BY COUNT(*) DESC) as rn
    FROM test_employees
    GROUP BY department, salary
)
SELECT 
    department,
    salary as mode_salary,
    frequency
FROM value_counts
WHERE rn = 1
ORDER BY department;

-- Expected: Most frequent salary in each department

-- Test 2.4: Percentile calculation using NTILE
SELECT 'Test 2.4: Percentile Buckets' as test_name;
SELECT 
    NTILE(4) OVER (ORDER BY salary) as quartile,
    name,
    salary,
    department
FROM test_employees
ORDER BY salary;

-- Expected: Employees divided into 4 salary quartiles

-- ============================================================================
-- TEST 3: STRING AGGREGATION
-- ============================================================================

-- Test 3.1: String concatenation (GROUP_CONCAT / STRING_AGG)
SELECT 'Test 3.1: String Concatenation' as test_name;
-- MySQL / SQLite:
SELECT 
    department,
    GROUP_CONCAT(name, ', ') as employee_list
FROM test_employees
GROUP BY department
ORDER BY department;

-- PostgreSQL equivalent:
-- SELECT 
--     department,
--     STRING_AGG(name, ', ' ORDER BY name) as employee_list
-- FROM test_employees
-- GROUP BY department
-- ORDER BY department;

-- SQL Server equivalent:
-- SELECT 
--     department,
--     STRING_AGG(name, ', ') WITHIN GROUP (ORDER BY name) as employee_list
-- FROM test_employees
-- GROUP BY department
-- ORDER BY department;

-- Expected: Comma-separated list of names per department

-- Test 3.2: Distinct string aggregation
SELECT 'Test 3.2: Distinct String Aggregation' as test_name;
-- MySQL:
SELECT 
    department,
    GROUP_CONCAT(DISTINCT status ORDER BY status SEPARATOR ', ') as unique_statuses
FROM test_employees
GROUP BY department
ORDER BY department;

-- PostgreSQL:
-- SELECT 
--     department,
--     STRING_AGG(DISTINCT status, ', ' ORDER BY status) as unique_statuses
-- FROM test_employees
-- GROUP BY department
-- ORDER BY department;

-- Test 3.3: Conditional string aggregation
SELECT 'Test 3.3: Conditional String Aggregation' as test_name;
SELECT 
    department,
    GROUP_CONCAT(CASE WHEN status = 'active' THEN name END, ', ') as active_employees,
    GROUP_CONCAT(CASE WHEN status = 'inactive' THEN name END, ', ') as inactive_employees
FROM test_employees
GROUP BY department
ORDER BY department;

-- Expected: Separate lists for active and inactive employees per department

-- ============================================================================
-- TEST 4: TIME-SERIES AGGREGATION
-- ============================================================================

-- Test 4.1: Period aggregation (daily)
SELECT 'Test 4.1: Daily Aggregation' as test_name;
SELECT 
    sale_date,
    SUM(amount) as total_sales,
    COUNT(*) as transaction_count,
    ROUND(AVG(amount), 2) as avg_transaction
FROM test_daily_sales
GROUP BY sale_date
ORDER BY sale_date;

-- Expected: Daily sales totals

-- Test 4.2: Running total
SELECT 'Test 4.2: Running Total' as test_name;
SELECT 
    sale_date,
    amount as daily_amount,
    SUM(amount) OVER (ORDER BY sale_date) as running_total,
    ROUND(AVG(amount) OVER (
        ORDER BY sale_date
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) as moving_avg_3day
FROM test_daily_sales
ORDER BY sale_date;

-- Expected: Daily amounts with cumulative totals and 3-day moving average

-- Test 4.3: Month-over-month comparison
SELECT 'Test 4.3: Month-over-Month' as test_name;
WITH monthly AS (
    SELECT 
        strftime('%Y-%m', sale_date) as month,
        SUM(amount) as total_sales
    FROM test_sales
    GROUP BY strftime('%Y-%m', sale_date)
),
with_previous AS (
    SELECT 
        month,
        total_sales,
        LAG(total_sales) OVER (ORDER BY month) as prev_month
    FROM monthly
)
SELECT 
    month,
    total_sales,
    prev_month,
    ROUND((total_sales - prev_month) * 100.0 / NULLIF(prev_month, 0), 2) as pct_change
FROM with_previous
ORDER BY month;

-- Expected: Monthly sales with percentage change from previous month

-- Test 4.4: Year-to-date
SELECT 'Test 4.4: Year-to-Date' as test_name;
SELECT 
    sale_date,
    amount,
    SUM(amount) OVER (
        ORDER BY sale_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as ytd_total
FROM test_daily_sales
ORDER BY sale_date;

-- Expected: Cumulative year-to-date totals

-- ============================================================================
-- TEST 5: GROUPING ENHANCEMENTS (ROLLUP)
-- ============================================================================

-- Test 5.1: ROLLUP aggregation
SELECT 'Test 5.1: ROLLUP Aggregation' as test_name;
-- MySQL / PostgreSQL / SQL Server:
SELECT 
    COALESCE(region, 'ALL REGIONS') as region,
    COALESCE(product, 'ALL PRODUCTS') as product,
    SUM(amount) as total_sales,
    COUNT(*) as transaction_count,
    GROUPING(region) as is_region_total,
    GROUPING(product) as is_product_total
FROM test_sales
GROUP BY ROLLUP(region, product)
ORDER BY region, product;

-- SQLite (use UNION ALL for older versions):
-- SELECT region, product, SUM(amount) as total_sales, COUNT(*) as transaction_count
-- FROM test_sales GROUP BY region, product
-- UNION ALL
-- SELECT region, NULL, SUM(amount), COUNT(*)
-- FROM test_sales GROUP BY region
-- UNION ALL
-- SELECT NULL, NULL, SUM(amount), COUNT(*)
-- FROM test_sales;

-- Expected: Subtotals at each level plus grand total

-- ============================================================================
-- TEST 6: AGGREGATE FILTERING
-- ============================================================================

-- Test 6.1: FILTER clause (PostgreSQL) / CASE (others)
SELECT 'Test 6.1: Filtered Aggregation' as test_name;
-- PostgreSQL:
-- SELECT 
--     department,
--     COUNT(*) as total_count,
--     COUNT(*) FILTER (WHERE status = 'active') as active_count,
--     AVG(salary) FILTER (WHERE status = 'active') as avg_active_salary,
--     SUM(bonus) FILTER (WHERE bonus IS NOT NULL) as total_bonuses
-- FROM test_employees
-- GROUP BY department
-- ORDER BY department;

-- MySQL / SQLite:
SELECT 
    department,
    COUNT(*) as total_count,
    COUNT(CASE WHEN status = 'active' THEN 1 END) as active_count,
    ROUND(AVG(CASE WHEN status = 'active' THEN salary END), 2) as avg_active_salary,
    SUM(CASE WHEN bonus IS NOT NULL THEN bonus ELSE 0 END) as total_bonuses
FROM test_employees
GROUP BY department
ORDER BY department;

-- Expected: Counts and averages filtered by status

-- Test 6.2: HAVING with subquery
SELECT 'Test 6.2: HAVING with Subquery' as test_name;
SELECT 
    department,
    ROUND(AVG(salary), 2) as avg_salary
FROM test_employees
GROUP BY department
HAVING AVG(salary) > (SELECT AVG(salary) FROM test_employees)
ORDER BY avg_salary DESC;

-- Expected: Departments with above-average salaries

-- Test 6.3: Complex HAVING conditions
SELECT 'Test 6.3: Complex HAVING' as test_name;
SELECT 
    department,
    COUNT(*) as employee_count,
    ROUND(AVG(salary), 2) as avg_salary,
    SUM(salary) as total_salary
FROM test_employees
GROUP BY department
HAVING COUNT(*) >= 2 
  AND AVG(salary) > 70000
ORDER BY avg_salary DESC;

-- Expected: Departments with 2+ employees and avg salary > 70k

-- ============================================================================
-- TEST 7: CUMULATIVE AGGREGATIONS
-- ============================================================================

-- Test 7.1: Partitioned running total
SELECT 'Test 7.1: Partitioned Running Total' as test_name;
SELECT 
    department,
    name,
    salary,
    SUM(salary) OVER (
        PARTITION BY department 
        ORDER BY salary DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as dept_running_total
FROM test_employees
WHERE status = 'active'
ORDER BY department, salary DESC;

-- Expected: Running salary totals within each department

-- Test 7.2: Running count and average
SELECT 'Test 7.2: Running Count and Average' as test_name;
SELECT 
    sale_date,
    amount,
    COUNT(*) OVER (ORDER BY sale_date) as running_count,
    ROUND(AVG(amount) OVER (ORDER BY sale_date), 2) as running_avg
FROM test_daily_sales
ORDER BY sale_date;

-- Expected: Cumulative count and average

-- ============================================================================
-- TEST 8: ADVANCED GROUPING
-- ============================================================================

-- Test 8.1: Bucket aggregation
SELECT 'Test 8.1: Bucket Aggregation' as test_name;
SELECT 
    CASE 
        WHEN age < 25 THEN 'Under 25'
        WHEN age BETWEEN 25 AND 34 THEN '25-34'
        WHEN age BETWEEN 35 AND 44 THEN '35-44'
        WHEN age >= 45 THEN '45+'
    END as age_group,
    COUNT(*) as count,
    ROUND(AVG(income), 2) as avg_income,
    ROUND(AVG(spending), 2) as avg_spending
FROM test_customers
GROUP BY 
    CASE 
        WHEN age < 25 THEN 'Under 25'
        WHEN age BETWEEN 25 AND 34 THEN '25-34'
        WHEN age BETWEEN 35 AND 44 THEN '35-44'
        WHEN age >= 45 THEN '45+'
    END
ORDER BY MIN(age);

-- Expected: Age groups with income and spending statistics

-- Test 8.2: Top N per group
SELECT 'Test 8.2: Top N Per Group' as test_name;
WITH ranked AS (
    SELECT 
        department,
        name,
        salary,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rn
    FROM test_employees
)
SELECT department, name, salary, rn as rank
FROM ranked
WHERE rn <= 2
ORDER BY department, rn;

-- Expected: Top 2 highest-paid employees per department

-- Test 8.3: LAG and LEAD
SELECT 'Test 8.3: LAG and LEAD' as test_name;
SELECT 
    sale_date,
    amount,
    LAG(amount) OVER (ORDER BY sale_date) as prev_day,
    LEAD(amount) OVER (ORDER BY sale_date) as next_day,
    amount - LAG(amount) OVER (ORDER BY sale_date) as day_change
FROM test_daily_sales
ORDER BY sale_date;

-- Expected: Daily amounts with previous/next day comparisons

-- Test 8.4: First and Last values
SELECT 'Test 8.4: First and Last Values' as test_name;
SELECT DISTINCT
    department,
    FIRST_VALUE(name) OVER (
        PARTITION BY department 
        ORDER BY hire_date
    ) as first_hired,
    LAST_VALUE(name) OVER (
        PARTITION BY department 
        ORDER BY hire_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) as last_hired
FROM test_employees
ORDER BY department;

-- Expected: First and last hired employee per department

-- ============================================================================
-- TEST 9: UTILITY FUNCTIONS
-- ============================================================================

-- Test 9.1: Weighted average
SELECT 'Test 9.1: Weighted Average' as test_name;
SELECT 
    product,
    ROUND(SUM(amount * quantity) / SUM(quantity), 2) as weighted_avg_price,
    ROUND(AVG(amount), 2) as simple_avg_price
FROM test_sales
GROUP BY product
ORDER BY product;

-- Expected: Weighted vs simple average prices

-- Test 9.2: NULL handling
SELECT 'Test 9.2: NULL Handling' as test_name;
SELECT 
    COUNT(*) as total_rows,
    COUNT(bonus) as non_null_count,
    COUNT(*) - COUNT(bonus) as null_count,
    ROUND((COUNT(*) - COUNT(bonus)) * 100.0 / COUNT(*), 2) as null_percentage
FROM test_employees;

-- Expected: NULL statistics for bonus column

-- Test 9.3: Deduplicated count
SELECT 'Test 9.3: Deduplicated Count' as test_name;
SELECT 
    department,
    COUNT(DISTINCT salary) as unique_salaries,
    COUNT(DISTINCT CASE WHEN status = 'active' THEN salary END) as active_unique_salaries
FROM test_employees
GROUP BY department
ORDER BY department;

-- Expected: Count of unique salary values

-- ============================================================================
-- TEST 10: PERFORMANCE TESTS
-- ============================================================================

-- Test 10.1: Window function performance
SELECT 'Test 10.1: Window Function Performance' as test_name;
EXPLAIN QUERY PLAN
SELECT 
    sale_date,
    amount,
    SUM(amount) OVER (ORDER BY sale_date) as running_total,
    AVG(amount) OVER (ORDER BY sale_date) as running_avg
FROM test_daily_sales
ORDER BY sale_date;

-- Expected: Query plan showing window function usage

-- ============================================================================
-- CLEANUP - Remove test tables
-- ============================================================================

DROP TABLE IF EXISTS test_employees;
DROP TABLE IF EXISTS test_sales;
DROP TABLE IF EXISTS test_daily_sales;
DROP TABLE IF EXISTS test_events;
DROP TABLE IF EXISTS test_customers;

-- ============================================================================
-- END OF TEST SUITE
-- ============================================================================