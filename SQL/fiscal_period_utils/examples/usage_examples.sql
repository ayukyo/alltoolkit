-- ============================================================================
-- SQL Fiscal Period Utilities - Usage Examples
-- ============================================================================
-- Practical examples demonstrating how to use fiscal_period_utils
-- Compatible with MySQL, PostgreSQL, SQL Server, and SQLite
--
-- Author: AllToolkit
-- License: MIT
-- ============================================================================

-- ============================================================================
-- EXAMPLE 1: BASIC FISCAL YEAR CALCULATION
-- ============================================================================

-- Scenario: Your company uses April as fiscal year start (UK/India/Japan style)
-- You need to convert calendar dates to fiscal years

-- MySQL Example:
/*
-- Create sample orders table
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    order_date DATE,
    customer_name VARCHAR(100),
    amount DECIMAL(10,2)
);

INSERT INTO orders VALUES
(1, '2024-03-31', 'Customer A', 500.00),  -- FY2023 Q4
(2, '2024-04-01', 'Customer B', 600.00),  -- FY2024 Q1
(3, '2024-05-15', 'Customer C', 700.00),  -- FY2024 Q1
(4, '2024-07-01', 'Customer D', 800.00),  -- FY2024 Q2
(5, '2024-12-31', 'Customer E', 900.00),  -- FY2024 Q3
(6, '2025-01-15', 'Customer F', 1000.00); -- FY2024 Q4

-- Calculate fiscal year and quarter for each order
SELECT 
    order_id,
    order_date,
    amount,
    -- Fiscal Year (April start)
    CASE 
        WHEN MONTH(order_date) >= 4 THEN YEAR(order_date)
        ELSE YEAR(order_date) - 1
    END AS fiscal_year,
    -- Fiscal Quarter (April start)
    CASE 
        WHEN MONTH(order_date) BETWEEN 4 AND 6 THEN 1
        WHEN MONTH(order_date) BETWEEN 7 AND 9 THEN 2
        WHEN MONTH(order_date) BETWEEN 10 AND 12 THEN 3
        ELSE 4
    END AS fiscal_quarter,
    -- Fiscal Period Label
    CONCAT('FY', RIGHT(CAST(
        CASE WHEN MONTH(order_date) >= 4 THEN YEAR(order_date) ELSE YEAR(order_date) - 1 END
    AS CHAR), 2), '-Q', CASE 
        WHEN MONTH(order_date) BETWEEN 4 AND 6 THEN 1
        WHEN MONTH(order_date) BETWEEN 7 AND 9 THEN 2
        WHEN MONTH(order_date) BETWEEN 10 AND 12 THEN 3
        ELSE 4
    END) AS fiscal_period
FROM orders;
*/

-- ============================================================================
-- EXAMPLE 2: SALES REPORT BY FISCAL PERIOD
-- ============================================================================

-- Scenario: Generate a quarterly sales report aligned to fiscal year

-- PostgreSQL Example:
/*
WITH fiscal_orders AS (
    SELECT 
        order_id,
        order_date,
        amount,
        -- Calculate fiscal year (April start)
        CASE 
            WHEN EXTRACT(MONTH FROM order_date) >= 4 THEN EXTRACT(YEAR FROM order_date)
            ELSE EXTRACT(YEAR FROM order_date) - 1
        END AS fiscal_year,
        -- Calculate fiscal quarter
        CASE 
            WHEN EXTRACT(MONTH FROM order_date) BETWEEN 4 AND 6 THEN 1
            WHEN EXTRACT(MONTH FROM order_date) BETWEEN 7 AND 9 THEN 2
            WHEN EXTRACT(MONTH FROM order_date) BETWEEN 10 AND 12 THEN 3
            ELSE 4
        END AS fiscal_quarter
    FROM orders
)
SELECT 
    fiscal_year,
    fiscal_quarter,
    'FY' || fiscal_year::text || '-Q' || fiscal_quarter::text AS period,
    COUNT(*) AS order_count,
    SUM(amount) AS total_sales,
    ROUND(AVG(amount)::numeric, 2) AS avg_order_value,
    MIN(amount) AS min_order,
    MAX(amount) AS max_order
FROM fiscal_orders
GROUP BY fiscal_year, fiscal_quarter
ORDER BY fiscal_year, fiscal_quarter;
*/

-- ============================================================================
-- EXAMPLE 3: US FEDERAL GOVERNMENT FISCAL YEAR (October Start)
-- ============================================================================

-- Scenario: Work with US Federal Government fiscal periods
-- US Federal FY2024 = Oct 1, 2023 to Sep 30, 2024

-- SQL Server Example:
/*
-- Sample transactions
DECLARE @transactions TABLE (
    trans_id INT,
    trans_date DATE,
    department VARCHAR(50),
    expenditure DECIMAL(10,2)
);

INSERT INTO @transactions VALUES
(1, '2023-10-01', 'Defense', 100000),
(2, '2023-11-15', 'Education', 50000),
(3, '2024-01-01', 'Health', 75000),
(4, '2024-03-31', 'Transport', 60000),
(5, '2024-06-15', 'Interior', 45000),
(6, '2024-09-30', 'Labor', 80000);

-- Calculate US Federal fiscal periods
SELECT 
    trans_id,
    trans_date,
    department,
    expenditure,
    -- US Federal Fiscal Year (October start)
    CASE 
        WHEN MONTH(trans_date) >= 10 THEN YEAR(trans_date) + 1
        ELSE YEAR(trans_date)
    END AS federal_fy,
    -- US Federal Fiscal Quarter
    CASE 
        WHEN MONTH(trans_date) BETWEEN 10 AND 12 THEN 1  -- Oct-Dec
        WHEN MONTH(trans_date) BETWEEN 1 AND 3 THEN 2    -- Jan-Mar
        WHEN MONTH(trans_date) BETWEEN 4 AND 6 THEN 3    -- Apr-Jun
        ELSE 4                                           -- Jul-Sep
    END AS federal_quarter,
    -- Period label
    'FY' + CAST(CASE 
        WHEN MONTH(trans_date) >= 10 THEN YEAR(trans_date) + 1 ELSE YEAR(trans_date)
    END AS VARCHAR) + '-Q' + CAST(CASE 
        WHEN MONTH(trans_date) BETWEEN 10 AND 12 THEN 1
        WHEN MONTH(trans_date) BETWEEN 1 AND 3 THEN 2
        WHEN MONTH(trans_date) BETWEEN 4 AND 6 THEN 3
        ELSE 4
    END AS VARCHAR) AS federal_period
FROM @transactions
ORDER BY trans_date;
*/

-- ============================================================================
-- EXAMPLE 4: YEAR-OVER-YEAR COMPARISON BY FISCAL QUARTER
-- ============================================================================

-- Scenario: Compare Q1 FY2024 sales with Q1 FY2023

-- MySQL Example:
/*
-- Sample sales data spanning multiple fiscal years
CREATE TABLE quarterly_sales (
    sale_date DATE,
    product VARCHAR(50),
    revenue DECIMAL(10,2)
);

INSERT INTO quarterly_sales VALUES
-- FY2023 Q1 (Apr-Jun 2023)
('2023-04-15', 'Product A', 10000),
('2023-05-15', 'Product A', 12000),
('2023-06-15', 'Product A', 15000),
-- FY2023 Q2 (Jul-Sep 2023)
('2023-07-15', 'Product A', 13000),
('2023-08-15', 'Product A', 14000),
('2023-09-15', 'Product A', 16000),
-- FY2024 Q1 (Apr-Jun 2024)
('2024-04-15', 'Product A', 11500),  -- 15% growth
('2024-05-15', 'Product A', 13800),  -- 15% growth
('2024-06-15', 'Product A', 17250);  -- 15% growth

-- Year-over-Year analysis
WITH fy_sales AS (
    SELECT 
        CASE 
            WHEN MONTH(sale_date) >= 4 THEN YEAR(sale_date)
            ELSE YEAR(sale_date) - 1
        END AS fiscal_year,
        CASE 
            WHEN MONTH(sale_date) BETWEEN 4 AND 6 THEN 1
            WHEN MONTH(sale_date) BETWEEN 7 AND 9 THEN 2
            WHEN MONTH(sale_date) BETWEEN 10 AND 12 THEN 3
            ELSE 4
        END AS fiscal_quarter,
        SUM(revenue) AS total_revenue
    FROM quarterly_sales
    GROUP BY 
        CASE WHEN MONTH(sale_date) >= 4 THEN YEAR(sale_date) ELSE YEAR(sale_date) - 1 END,
        CASE WHEN MONTH(sale_date) BETWEEN 4 AND 6 THEN 1 WHEN MONTH(sale_date) BETWEEN 7 AND 9 THEN 2 WHEN MONTH(sale_date) BETWEEN 10 AND 12 THEN 3 ELSE 4 END
)
SELECT 
    fy1.fiscal_year,
    fy1.fiscal_quarter,
    fy1.total_revenue AS current_revenue,
    fy2.total_revenue AS previous_revenue,
    fy1.total_revenue - fy2.total_revenue AS revenue_change,
    ROUND((fy1.total_revenue - fy2.total_revenue) / fy2.total_revenue * 100, 2) AS yoy_growth_pct
FROM fy_sales fy1
LEFT JOIN fy_sales fy2 ON 
    fy1.fiscal_quarter = fy2.fiscal_quarter 
    AND fy1.fiscal_year = fy2.fiscal_year + 1
WHERE fy1.fiscal_year = 2024
ORDER BY fy1.fiscal_quarter;
*/

-- ============================================================================
-- EXAMPLE 5: FISCAL YEAR-TO-DATE CALCULATIONS
-- ============================================================================

-- Scenario: Calculate year-to-date metrics for current fiscal year

-- SQLite Example:
/*
-- Sample expense transactions
CREATE TABLE expenses (
    expense_date DATE,
    category VARCHAR(50),
    amount DECIMAL(10,2)
);

INSERT INTO expenses VALUES
('2024-04-01', 'Marketing', 5000),
('2024-05-01', 'Marketing', 6000),
('2024-06-01', 'Marketing', 7000),
('2024-07-01', 'Operations', 3000),
('2024-08-01', 'Operations', 4000),
('2024-09-01', 'Operations', 5000),
('2024-10-01', 'R&D', 8000),
('2024-11-01', 'R&D', 9000);

-- Calculate fiscal YTD (April start, as of November 2024)
SELECT 
    category,
    SUM(amount) AS ytd_expenses,
    COUNT(*) AS expense_count,
    ROUND(AVG(amount), 2) AS avg_expense
FROM expenses
WHERE 
    -- Fiscal year starts in April, we're in FY2024
    expense_date >= '2024-04-01'
    AND expense_date <= '2024-11-30'
GROUP BY category
ORDER BY ytd_expenses DESC;
*/

-- ============================================================================
-- EXAMPLE 6: FISCAL PERIOD BUDGET ALLOCATION
-- ============================================================================

-- Scenario: Allocate annual budget across fiscal quarters

-- PostgreSQL Example:
/*
-- Annual budget table
CREATE TABLE annual_budgets (
    fiscal_year INT,
    department VARCHAR(50),
    annual_budget DECIMAL(12,2)
);

INSERT INTO annual_budgets VALUES
(2024, 'Sales', 1000000),
(2024, 'Marketing', 500000),
(2024, 'Operations', 750000),
(2024, 'R&D', 1200000);

-- Generate quarterly budget breakdown (Q1=25%, Q2=30%, Q3=25%, Q4=20%)
SELECT 
    fiscal_year,
    department,
    annual_budget,
    ROUND(annual_budget * 0.25, 2) AS q1_budget,
    ROUND(annual_budget * 0.30, 2) AS q2_budget,
    ROUND(annual_budget * 0.25, 2) AS q3_budget,
    ROUND(annual_budget * 0.20, 2) AS q4_budget,
    'FY' || fiscal_year || '-Q1' AS q1_period,
    'FY' || fiscal_year || '-Q2' AS q2_period,
    'FY' || fiscal_year || '-Q3' AS q3_period,
    'FY' || fiscal_year || '-Q4' AS q4_period
FROM annual_budgets
ORDER BY department;
*/

-- ============================================================================
-- EXAMPLE 7: FINDING RECORDS IN A SPECIFIC FISCAL PERIOD
-- ============================================================================

-- Scenario: Get all transactions for FY2024 Q2 (Jul-Sep)

-- MySQL Example:
/*
SELECT 
    transaction_id,
    transaction_date,
    amount,
    description
FROM transactions
WHERE 
    -- FY2024 Q2 = Jul 1, 2024 to Sep 30, 2024 (April start)
    transaction_date >= '2024-07-01'
    AND transaction_date <= '2024-09-30'
ORDER BY transaction_date;
*/

-- Alternative: Use fiscal calculations dynamically
/*
SELECT 
    transaction_id,
    transaction_date,
    amount,
    description
FROM transactions
WHERE 
    CASE WHEN MONTH(transaction_date) >= 4 THEN YEAR(transaction_date) ELSE YEAR(transaction_date) - 1 END = 2024
    AND CASE 
        WHEN MONTH(transaction_date) BETWEEN 4 AND 6 THEN 1
        WHEN MONTH(transaction_date) BETWEEN 7 AND 9 THEN 2
        WHEN MONTH(transaction_date) BETWEEN 10 AND 12 THEN 3
        ELSE 4
    END = 2
ORDER BY transaction_date;
*/

-- ============================================================================
-- EXAMPLE 8: AUSTRALIA/NEW ZEALAND FISCAL YEAR (July Start)
-- ============================================================================

-- Scenario: Australian company with July fiscal year start
-- FY2024 = Jul 1, 2023 to Jun 30, 2024

-- MySQL Example:
/*
-- Australian sales data
CREATE TABLE au_sales (
    sale_date DATE,
    region VARCHAR(50),
    sales_amount DECIMAL(10,2)
);

INSERT INTO au_sales VALUES
('2023-07-01', 'Sydney', 25000),
('2023-08-01', 'Melbourne', 22000),
('2023-09-01', 'Brisbane', 18000),
('2023-10-01', 'Perth', 15000),
('2024-01-01', 'Sydney', 30000),
('2024-03-01', 'Melbourne', 28000),
('2024-06-30', 'Brisbane', 20000);

-- Calculate Australian fiscal periods
SELECT 
    sale_date,
    region,
    sales_amount,
    -- Australian Fiscal Year (July start)
    CASE 
        WHEN MONTH(sale_date) >= 7 THEN YEAR(sale_date)
        ELSE YEAR(sale_date) - 1
    END AS australian_fy,
    -- Australian Fiscal Quarter
    CASE 
        WHEN MONTH(sale_date) BETWEEN 7 AND 9 THEN 1   -- Jul-Sep
        WHEN MONTH(sale_date) BETWEEN 10 AND 12 THEN 2 -- Oct-Dec
        WHEN MONTH(sale_date) BETWEEN 1 AND 3 THEN 3   -- Jan-Mar
        ELSE 4                                         -- Apr-Jun
    END AS australian_quarter
FROM au_sales
ORDER BY sale_date;
*/

-- ============================================================================
-- EXAMPLE 9: RUNNING TOTALS BY FISCAL PERIOD
-- ============================================================================

-- Scenario: Calculate cumulative sales by fiscal quarter

-- SQL Server Example:
/*
WITH fiscal_periods AS (
    SELECT 
        order_date,
        amount,
        CASE 
            WHEN MONTH(order_date) >= 4 THEN YEAR(order_date)
            ELSE YEAR(order_date) - 1
        END AS fiscal_year,
        CASE 
            WHEN MONTH(order_date) BETWEEN 4 AND 6 THEN 1
            WHEN MONTH(order_date) BETWEEN 7 AND 9 THEN 2
            WHEN MONTH(order_date) BETWEEN 10 AND 12 THEN 3
            ELSE 4
        END AS fiscal_quarter
    FROM orders
),
quarterly_totals AS (
    SELECT 
        fiscal_year,
        fiscal_quarter,
        SUM(amount) AS quarter_sales
    FROM fiscal_periods
    GROUP BY fiscal_year, fiscal_quarter
)
SELECT 
    fiscal_year,
    fiscal_quarter,
    quarter_sales,
    -- Running total across all quarters
    SUM(quarter_sales) OVER (ORDER BY fiscal_year, fiscal_quarter) AS cumulative_sales,
    -- 4-quarter moving average
    AVG(quarter_sales) OVER (
        ORDER BY fiscal_year, fiscal_quarter 
        ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
    ) AS moving_avg_4q,
    -- Same quarter last year
    LAG(quarter_sales, 4) OVER (ORDER BY fiscal_year, fiscal_quarter) AS same_q_last_year
FROM quarterly_totals
ORDER BY fiscal_year, fiscal_quarter;
*/

-- ============================================================================
-- EXAMPLE 10: FISCAL PERIOD DATE RANGE GENERATION
-- ============================================================================

-- Scenario: Generate all fiscal quarter date ranges for FY2024

-- PostgreSQL Example:
/*
SELECT 
    2024 AS fiscal_year,
    quarter_num AS fiscal_quarter,
    CASE quarter_num
        WHEN 1 THEN MAKE_DATE(2024, 4, 1)   -- Apr-Jun
        WHEN 2 THEN MAKE_DATE(2024, 7, 1)   -- Jul-Sep
        WHEN 3 THEN MAKE_DATE(2024, 10, 1)  -- Oct-Dec
        WHEN 4 THEN MAKE_DATE(2025, 1, 1)   -- Jan-Mar
    END AS quarter_start,
    CASE quarter_num
        WHEN 1 THEN MAKE_DATE(2024, 6, 30)
        WHEN 2 THEN MAKE_DATE(2024, 9, 30)
        WHEN 3 THEN MAKE_DATE(2024, 12, 31)
        WHEN 4 THEN MAKE_DATE(2025, 3, 31)
    END AS quarter_end,
    'FY2024-Q' || quarter_num AS period_label
FROM generate_series(1, 4) AS quarter_num;
*/

-- ============================================================================
-- EXAMPLE 11: CUSTOM FISCAL YEAR START (Any Month)
-- ============================================================================

-- Scenario: Company with custom fiscal year starting in February

-- MySQL Example:
/*
SET @fiscal_start = 2;  -- February start

SELECT 
    date_col,
    CASE 
        WHEN MONTH(date_col) >= @fiscal_start THEN YEAR(date_col)
        ELSE YEAR(date_col) - 1
    END AS fiscal_year,
    -- Calculate fiscal quarter based on fiscal start month
    ((MONTH(date_col) - @fiscal_start + 12) % 12) / 3 + 1 AS fiscal_quarter,
    -- Calculate fiscal month (1-12 within fiscal year)
    CASE 
        WHEN MONTH(date_col) >= @fiscal_start THEN MONTH(date_col) - @fiscal_start + 1
        ELSE MONTH(date_col) + 12 - @fiscal_start + 1
    END AS fiscal_month
FROM your_table;
*/

-- ============================================================================
-- EXAMPLE 12: MULTI-COUNTRY FISCAL YEAR SUPPORT
-- ============================================================================

-- Scenario: Global company with different fiscal years per region

-- PostgreSQL Example:
/*
-- Regional sales data
CREATE TABLE global_sales (
    sale_date DATE,
    country VARCHAR(50),
    region VARCHAR(20),  -- 'US', 'UK', 'AU', 'JP'
    amount DECIMAL(10,2)
);

INSERT INTO global_sales VALUES
('2023-10-01', 'USA', 'US', 100000),
('2024-04-01', 'UK', 'UK', 80000),
('2023-07-01', 'Australia', 'AU', 50000),
('2024-04-01', 'Japan', 'JP', 70000);

-- Calculate fiscal periods based on region
SELECT 
    sale_date,
    country,
    region,
    amount,
    CASE region
        WHEN 'US' THEN CASE WHEN EXTRACT(MONTH FROM sale_date) >= 10 THEN EXTRACT(YEAR FROM sale_date) + 1 ELSE EXTRACT(YEAR FROM sale_date) END
        WHEN 'UK' THEN CASE WHEN EXTRACT(MONTH FROM sale_date) >= 4 THEN EXTRACT(YEAR FROM sale_date) ELSE EXTRACT(YEAR FROM sale_date) - 1 END
        WHEN 'AU' THEN CASE WHEN EXTRACT(MONTH FROM sale_date) >= 7 THEN EXTRACT(YEAR FROM sale_date) ELSE EXTRACT(YEAR FROM sale_date) - 1 END
        WHEN 'JP' THEN CASE WHEN EXTRACT(MONTH FROM sale_date) >= 4 THEN EXTRACT(YEAR FROM sale_date) ELSE EXTRACT(YEAR FROM sale_date) - 1 END
        ELSE EXTRACT(YEAR FROM sale_date)
    END AS fiscal_year,
    CASE region
        WHEN 'US' THEN
            CASE 
                WHEN EXTRACT(MONTH FROM sale_date) BETWEEN 10 AND 12 THEN 1
                WHEN EXTRACT(MONTH FROM sale_date) BETWEEN 1 AND 3 THEN 2
                WHEN EXTRACT(MONTH FROM sale_date) BETWEEN 4 AND 6 THEN 3
                ELSE 4
            END
        WHEN 'UK' THEN
            CASE 
                WHEN EXTRACT(MONTH FROM sale_date) BETWEEN 4 AND 6 THEN 1
                WHEN EXTRACT(MONTH FROM sale_date) BETWEEN 7 AND 9 THEN 2
                WHEN EXTRACT(MONTH FROM sale_date) BETWEEN 10 AND 12 THEN 3
                ELSE 4
            END
        WHEN 'AU' THEN
            CASE 
                WHEN EXTRACT(MONTH FROM sale_date) BETWEEN 7 AND 9 THEN 1
                WHEN EXTRACT(MONTH FROM sale_date) BETWEEN 10 AND 12 THEN 2
                WHEN EXTRACT(MONTH FROM sale_date) BETWEEN 1 AND 3 THEN 3
                ELSE 4
            END
        ELSE EXTRACT(QUARTER FROM sale_date)
    END AS fiscal_quarter
FROM global_sales
ORDER BY sale_date;
*/

-- ============================================================================
-- EXAMPLE 13: FISCAL PERIOD PERFORMANCE METRICS
-- ============================================================================

-- Scenario: Calculate performance metrics against fiscal targets

-- SQL Server Example:
/*
-- Targets table
DECLARE @fiscal_targets TABLE (
    fiscal_year INT,
    fiscal_quarter INT,
    target_revenue DECIMAL(10,2)
);

INSERT INTO @fiscal_targets VALUES
(2024, 1, 50000),
(2024, 2, 60000),
(2024, 3, 55000),
(2024, 4, 45000);

-- Actual sales
DECLARE @actual_sales TABLE (
    sale_date DATE,
    actual_revenue DECIMAL(10,2)
);

INSERT INTO @actual_sales VALUES
('2024-04-15', 52000),
('2024-07-15', 58000),
('2024-10-15', 50000);

-- Performance against targets
WITH fiscal_actuals AS (
    SELECT 
        CASE WHEN MONTH(sale_date) >= 4 THEN YEAR(sale_date) ELSE YEAR(sale_date) - 1 END AS fiscal_year,
        CASE 
            WHEN MONTH(sale_date) BETWEEN 4 AND 6 THEN 1
            WHEN MONTH(sale_date) BETWEEN 7 AND 9 THEN 2
            WHEN MONTH(sale_date) BETWEEN 10 AND 12 THEN 3
            ELSE 4
        END AS fiscal_quarter,
        SUM(actual_revenue) AS total_actual
    FROM @actual_sales
    GROUP BY 
        CASE WHEN MONTH(sale_date) >= 4 THEN YEAR(sale_date) ELSE YEAR(sale_date) - 1 END,
        CASE WHEN MONTH(sale_date) BETWEEN 4 AND 6 THEN 1 WHEN MONTH(sale_date) BETWEEN 7 AND 9 THEN 2 WHEN MONTH(sale_date) BETWEEN 10 AND 12 THEN 3 ELSE 4 END
)
SELECT 
    t.fiscal_year,
    t.fiscal_quarter,
    t.target_revenue,
    a.total_actual AS actual_revenue,
    a.total_actual - t.target_revenue AS variance,
    ROUND((a.total_actual - t.target_revenue) / t.target_revenue * 100, 2) AS achievement_pct,
    CASE 
        WHEN a.total_actual >= t.target_revenue THEN 'Target Met'
        ELSE 'Below Target'
    END AS status
FROM @fiscal_targets t
LEFT JOIN fiscal_actuals a ON 
    t.fiscal_year = a.fiscal_year 
    AND t.fiscal_quarter = a.fiscal_quarter
ORDER BY t.fiscal_year, t.fiscal_quarter;
*/

-- ============================================================================
-- END OF EXAMPLES
-- ============================================================================