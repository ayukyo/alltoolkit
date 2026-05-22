-- ============================================================================
-- SQL Fiscal Period Utilities Module
-- ============================================================================
-- A comprehensive collection of fiscal period (fiscal year/quarter) utility functions.
-- Supports multiple fiscal year start configurations (January, April, July, October).
-- Compatible with MySQL, PostgreSQL, SQL Server, and SQLite.
--
-- Features:
--   - Fiscal year calculation from any date
--   - Fiscal quarter determination
--   - Fiscal month within fiscal year
--   - Fiscal period range (start/end dates)
--   - Year-over-year comparisons
--   - Custom fiscal year start month support
--
-- Common Fiscal Year Configurations:
--   - Calendar Year: Starts January 1 (default)
--   - US Federal: Starts October 1
--   - UK/India/Australia: Starts April 1
--   - Japan: Starts April 1
--   - New Zealand: Starts July 1
--
-- Usage:
--   Copy individual query patterns for your specific database.
--   Adjust @fiscal_year_start parameter as needed.
--
-- Author: AllToolkit
-- License: MIT
-- ============================================================================

-- ============================================================================
-- SECTION 1: FISCAL YEAR CALCULATION
-- ============================================================================

-- Calculate fiscal year from date (Fiscal Year starts in April)
-- If date is in Jan-Mar, it belongs to previous fiscal year
-- Example: 2024-02-15 is in Fiscal Year 2023 (Apr 2023 - Mar 2024)

-- MySQL: Fiscal Year starting April (FY starts Apr 1)
/*
SELECT 
    date_col,
    CASE 
        WHEN MONTH(date_col) >= 4 THEN YEAR(date_col)
        ELSE YEAR(date_col) - 1
    END AS fiscal_year,
    CONCAT('FY', CASE 
        WHEN MONTH(date_col) >= 4 THEN YEAR(date_col)
        ELSE YEAR(date_col) - 1
    END) AS fiscal_year_label
FROM your_table;
*/

-- PostgreSQL: Fiscal Year starting April
/*
SELECT 
    date_col,
    CASE 
        WHEN EXTRACT(MONTH FROM date_col) >= 4 THEN EXTRACT(YEAR FROM date_col)
        ELSE EXTRACT(YEAR FROM date_col) - 1
    END AS fiscal_year,
    'FY' || CASE 
        WHEN EXTRACT(MONTH FROM date_col) >= 4 THEN EXTRACT(YEAR FROM date_col)
        ELSE EXTRACT(YEAR FROM date_col) - 1
    END AS fiscal_year_label
FROM your_table;
*/

-- SQL Server: Fiscal Year starting April
/*
SELECT 
    date_col,
    CASE 
        WHEN MONTH(date_col) >= 4 THEN YEAR(date_col)
        ELSE YEAR(date_col) - 1
    END AS fiscal_year,
    'FY' + CAST(CASE 
        WHEN MONTH(date_col) >= 4 THEN YEAR(date_col)
        ELSE YEAR(date_col) - 1
    END AS VARCHAR) AS fiscal_year_label
FROM your_table;
*/

-- SQLite: Fiscal Year starting April
/*
SELECT 
    date_col,
    CASE 
        WHEN CAST(strftime('%m', date_col) AS INTEGER) >= 4 THEN CAST(strftime('%Y', date_col) AS INTEGER)
        ELSE CAST(strftime('%Y', date_col) AS INTEGER) - 1
    END AS fiscal_year,
    'FY' || CASE 
        WHEN CAST(strftime('%m', date_col) AS INTEGER) >= 4 THEN CAST(strftime('%Y', date_col) AS INTEGER)
        ELSE CAST(strftime('%Y', date_col) AS INTEGER) - 1
    END AS fiscal_year_label
FROM your_table;
*/

-- ============================================================================
-- SECTION 2: GENERIC FISCAL YEAR CALCULATION (Configurable Start Month)
-- ============================================================================

-- Generic fiscal year calculation with configurable start month
-- @fiscal_year_start: The month number when fiscal year begins (1-12)
--   1 = January (Calendar Year)
--   4 = April (UK, India, Japan)
--   7 = July (Australia, New Zealand)
--   10 = October (US Federal Government)

-- MySQL: Generic fiscal year with configurable start
/*
SET @fiscal_year_start = 10;  -- October for US Federal

SELECT 
    date_col,
    CASE 
        WHEN MONTH(date_col) >= @fiscal_year_start THEN YEAR(date_col) + 1
        ELSE YEAR(date_col)
    END AS fiscal_year,
    -- Alternative: Label as FY2024 (year it ends)
    CONCAT('FY', CASE 
        WHEN MONTH(date_col) >= @fiscal_year_start THEN YEAR(date_col) + 1
        ELSE YEAR(date_col)
    END) AS fiscal_year_label
FROM your_table;
*/

-- PostgreSQL: Generic fiscal year with configurable start
/*
-- US Federal Fiscal Year (starts October)
SELECT 
    date_col,
    CASE 
        WHEN EXTRACT(MONTH FROM date_col) >= 10 THEN EXTRACT(YEAR FROM date_col) + 1
        ELSE EXTRACT(YEAR FROM date_col)
    END AS fiscal_year,
    'FY' || CASE 
        WHEN EXTRACT(MONTH FROM date_col) >= 10 THEN EXTRACT(YEAR FROM date_col) + 1
        ELSE EXTRACT(YEAR FROM date_col)
    END AS fiscal_year_label
FROM your_table;
*/

-- SQL Server: Generic fiscal year with configurable start
/*
DECLARE @fiscal_year_start INT = 10;  -- October for US Federal

SELECT 
    date_col,
    CASE 
        WHEN MONTH(date_col) >= @fiscal_year_start THEN YEAR(date_col) + 1
        ELSE YEAR(date_col)
    END AS fiscal_year,
    'FY' + CAST(CASE 
        WHEN MONTH(date_col) >= @fiscal_year_start THEN YEAR(date_col) + 1
        ELSE YEAR(date_col)
    END AS VARCHAR) AS fiscal_year_label
FROM your_table;
*/

-- SQLite: Generic fiscal year with configurable start
/*
-- Fiscal year starting October (US Federal)
SELECT 
    date_col,
    CASE 
        WHEN CAST(strftime('%m', date_col) AS INTEGER) >= 10 THEN CAST(strftime('%Y', date_col) AS INTEGER) + 1
        ELSE CAST(strftime('%Y', date_col) AS INTEGER)
    END AS fiscal_year,
    'FY' || CASE 
        WHEN CAST(strftime('%m', date_col) AS INTEGER) >= 10 THEN CAST(strftime('%Y', date_col) AS INTEGER) + 1
        ELSE CAST(strftime('%Y', date_col) AS INTEGER)
    END AS fiscal_year_label
FROM your_table;
*/

-- ============================================================================
-- SECTION 3: FISCAL QUARTER CALCULATION
-- ============================================================================

-- Fiscal Quarter calculation with configurable fiscal year start
-- Quarters are numbered 1-4 within the fiscal year

-- MySQL: Fiscal Quarter (Fiscal Year starts April)
/*
SET @fiscal_year_start = 4;  -- April

SELECT 
    date_col,
    -- Fiscal year
    CASE 
        WHEN MONTH(date_col) >= @fiscal_year_start THEN YEAR(date_col)
        ELSE YEAR(date_col) - 1
    END AS fiscal_year,
    -- Fiscal quarter
    CASE 
        WHEN MONTH(date_col) BETWEEN 4 AND 6 THEN 1
        WHEN MONTH(date_col) BETWEEN 7 AND 9 THEN 2
        WHEN MONTH(date_col) BETWEEN 10 AND 12 THEN 3
        ELSE 4  -- Jan-Mar
    END AS fiscal_quarter,
    -- Fiscal quarter label
    CONCAT('Q', CASE 
        WHEN MONTH(date_col) BETWEEN 4 AND 6 THEN 1
        WHEN MONTH(date_col) BETWEEN 7 AND 9 THEN 2
        WHEN MONTH(date_col) BETWEEN 10 AND 12 THEN 3
        ELSE 4
    END, ' FY', CASE 
        WHEN MONTH(date_col) >= @fiscal_year_start THEN YEAR(date_col)
        ELSE YEAR(date_col) - 1
    END) AS fiscal_period
FROM your_table;
*/

-- PostgreSQL: Fiscal Quarter (Fiscal Year starts October - US Federal)
/*
SELECT 
    date_col,
    -- Fiscal year
    CASE 
        WHEN EXTRACT(MONTH FROM date_col) >= 10 THEN EXTRACT(YEAR FROM date_col) + 1
        ELSE EXTRACT(YEAR FROM date_col)
    END AS fiscal_year,
    -- Fiscal quarter (Oct-Dec=Q1, Jan-Mar=Q2, Apr-Jun=Q3, Jul-Sep=Q4)
    CASE 
        WHEN EXTRACT(MONTH FROM date_col) BETWEEN 10 AND 12 THEN 1
        WHEN EXTRACT(MONTH FROM date_col) BETWEEN 1 AND 3 THEN 2
        WHEN EXTRACT(MONTH FROM date_col) BETWEEN 4 AND 6 THEN 3
        ELSE 4
    END AS fiscal_quarter,
    -- Fiscal period label
    'Q' || CASE 
        WHEN EXTRACT(MONTH FROM date_col) BETWEEN 10 AND 12 THEN 1
        WHEN EXTRACT(MONTH FROM date_col) BETWEEN 1 AND 3 THEN 2
        WHEN EXTRACT(MONTH FROM date_col) BETWEEN 4 AND 6 THEN 3
        ELSE 4
    END || ' FY' || CASE 
        WHEN EXTRACT(MONTH FROM date_col) >= 10 THEN EXTRACT(YEAR FROM date_col) + 1
        ELSE EXTRACT(YEAR FROM date_col)
    END AS fiscal_period
FROM your_table;
*/

-- SQL Server: Fiscal Quarter with dynamic calculation
/*
DECLARE @fiscal_year_start INT = 4;  -- April start

SELECT 
    date_col,
    -- Calculate adjusted month (shifted for fiscal year)
    (MONTH(date_col) - @fiscal_year_start + 12) % 12 + 1 AS fiscal_month,
    -- Calculate fiscal quarter
    ((MONTH(date_col) - @fiscal_year_start + 12) % 12) / 3 + 1 AS fiscal_quarter,
    -- Calculate fiscal year
    CASE 
        WHEN MONTH(date_col) >= @fiscal_year_start THEN YEAR(date_col)
        ELSE YEAR(date_col) - 1
    END AS fiscal_year
FROM your_table;
*/

-- SQLite: Fiscal Quarter (Fiscal Year starts July)
/*
SELECT 
    date_col,
    -- Fiscal year (July start)
    CASE 
        WHEN CAST(strftime('%m', date_col) AS INTEGER) >= 7 THEN CAST(strftime('%Y', date_col) AS INTEGER)
        ELSE CAST(strftime('%Y', date_col) AS INTEGER) - 1
    END AS fiscal_year,
    -- Fiscal quarter (Jul-Sep=Q1, Oct-Dec=Q2, Jan-Mar=Q3, Apr-Jun=Q4)
    CASE 
        WHEN CAST(strftime('%m', date_col) AS INTEGER) BETWEEN 7 AND 9 THEN 1
        WHEN CAST(strftime('%m', date_col) AS INTEGER) BETWEEN 10 AND 12 THEN 2
        WHEN CAST(strftime('%m', date_col) AS INTEGER) BETWEEN 1 AND 3 THEN 3
        ELSE 4
    END AS fiscal_quarter
FROM your_table;
*/

-- ============================================================================
-- SECTION 4: FISCAL PERIOD RANGE (Start/End Dates)
-- ============================================================================

-- Get fiscal year start and end dates

-- MySQL: Fiscal Year date range (April start)
/*
SET @fiscal_year = 2024;
SET @fiscal_year_start_month = 4;

SELECT 
    @fiscal_year AS fiscal_year,
    DATE(CONCAT(@fiscal_year - 1, '-', @fiscal_year_start_month, '-01')) AS fiscal_year_start,
    DATE(DATE_ADD(DATE(CONCAT(@fiscal_year, '-', @fiscal_year_start_month, '-01')), INTERVAL -1 DAY)) AS fiscal_year_end,
    DATE_FORMAT(DATE(CONCAT(@fiscal_year - 1, '-', @fiscal_year_start_month, '-01')), '%Y-%m-%d') AS start_date,
    DATE_FORMAT(DATE(DATE_ADD(DATE(CONCAT(@fiscal_year, '-', @fiscal_year_start_month, '-01')), INTERVAL -1 DAY)), '%Y-%m-%d') AS end_date;
*/

-- PostgreSQL: Fiscal Year date range (October start - US Federal)
/*
SELECT 
    2024 AS fiscal_year,
    MAKE_DATE(2023, 10, 1) AS fiscal_year_start,
    MAKE_DATE(2024, 9, 30) AS fiscal_year_end,
    TO_CHAR(MAKE_DATE(2023, 10, 1), 'YYYY-MM-DD') AS start_date,
    TO_CHAR(MAKE_DATE(2024, 9, 30), 'YYYY-MM-DD') AS end_date;
*/

-- SQL Server: Fiscal Year date range
/*
DECLARE @fiscal_year INT = 2024;
DECLARE @fiscal_year_start_month INT = 10;  -- October

SELECT 
    @fiscal_year AS fiscal_year,
    DATEFROMPARTS(@fiscal_year - 1, @fiscal_year_start_month, 1) AS fiscal_year_start,
    DATEADD(DAY, -1, DATEFROMPARTS(@fiscal_year, @fiscal_year_start_month, 1)) AS fiscal_year_end;
*/

-- SQLite: Fiscal Year date range
/*
SELECT 
    '2024' AS fiscal_year,
    date('2023-10-01') AS fiscal_year_start,
    date('2024-09-30') AS fiscal_year_end;
*/

-- Fiscal Quarter date range

-- MySQL: Fiscal Quarter date range (April start)
/*
SET @fiscal_year = 2024;
SET @fiscal_quarter = 2;

SELECT 
    @fiscal_year AS fiscal_year,
    @fiscal_quarter AS fiscal_quarter,
    CASE @fiscal_quarter
        WHEN 1 THEN DATE(CONCAT(@fiscal_year - 1, '-04-01'))  -- Q1: Apr-Jun
        WHEN 2 THEN DATE(CONCAT(@fiscal_year - 1, '-07-01'))  -- Q2: Jul-Sep
        WHEN 3 THEN DATE(CONCAT(@fiscal_year - 1, '-10-01'))  -- Q3: Oct-Dec
        WHEN 4 THEN DATE(CONCAT(@fiscal_year, '-01-01'))      -- Q4: Jan-Mar
    END AS quarter_start,
    CASE @fiscal_quarter
        WHEN 1 THEN DATE(CONCAT(@fiscal_year - 1, '-06-30'))  -- Q1: Apr-Jun
        WHEN 2 THEN DATE(CONCAT(@fiscal_year - 1, '-09-30'))  -- Q2: Jul-Sep
        WHEN 3 THEN DATE(CONCAT(@fiscal_year - 1, '-12-31'))  -- Q3: Oct-Dec
        WHEN 4 THEN DATE(CONCAT(@fiscal_year, '-03-31'))      -- Q4: Jan-Mar
    END AS quarter_end;
*/

-- PostgreSQL: Fiscal Quarter date range (October start - US Federal)
/*
SELECT 
    2024 AS fiscal_year,
    2 AS fiscal_quarter,
    MAKE_DATE(2024, 1, 1) AS quarter_start,
    MAKE_DATE(2024, 3, 31) AS quarter_end;
-- Q1: Oct-Dec (previous calendar year Oct)
-- Q2: Jan-Mar
-- Q3: Apr-Jun
-- Q4: Jul-Sep
*/

-- SQLite: Fiscal Quarter date range
/*
SELECT 
    '2024' AS fiscal_year,
    '2' AS fiscal_quarter,
    date('2024-01-01') AS quarter_start,
    date('2024-03-31') AS quarter_end;
*/

-- ============================================================================
-- SECTION 5: FISCAL MONTH CALCULATION
-- ============================================================================

-- Fiscal Month is the month number within the fiscal year (1-12)

-- MySQL: Fiscal Month (April start)
/*
SET @fiscal_year_start = 4;  -- April

SELECT 
    date_col,
    MONTH(date_col) AS calendar_month,
    CASE 
        WHEN MONTH(date_col) >= @fiscal_year_start THEN MONTH(date_col) - @fiscal_year_start + 1
        ELSE MONTH(date_col) + (12 - @fiscal_year_start) + 1
    END AS fiscal_month,
    -- Fiscal month name
    CASE 
        WHEN MONTH(date_col) >= @fiscal_year_start THEN MONTH(date_col) - @fiscal_year_start + 1
        ELSE MONTH(date_col) + (12 - @fiscal_year_start) + 1
    END AS fiscal_month_number,
    ELT(
        CASE 
            WHEN MONTH(date_col) >= @fiscal_year_start THEN MONTH(date_col) - @fiscal_year_start + 1
            ELSE MONTH(date_col) + (12 - @fiscal_year_start) + 1
        END,
        'April', 'May', 'June', 'July', 'August', 'September',
        'October', 'November', 'December', 'January', 'February', 'March'
    ) AS fiscal_month_name
FROM your_table;
*/

-- PostgreSQL: Fiscal Month (October start - US Federal)
/*
SELECT 
    date_col,
    EXTRACT(MONTH FROM date_col) AS calendar_month,
    CASE 
        WHEN EXTRACT(MONTH FROM date_col) >= 10 THEN EXTRACT(MONTH FROM date_col) - 10 + 1
        ELSE EXTRACT(MONTH FROM date_col) + 3
    END AS fiscal_month,
    CASE 
        WHEN EXTRACT(MONTH FROM date_col) >= 10 THEN EXTRACT(MONTH FROM date_col) - 10 + 1
        ELSE EXTRACT(MONTH FROM date_col) + 3
    END AS fiscal_month_number
FROM your_table;
-- Fiscal months: Oct=1, Nov=2, Dec=3, Jan=4, Feb=5, Mar=6, Apr=7, May=8, Jun=9, Jul=10, Aug=11, Sep=12
*/

-- SQL Server: Fiscal Month
/*
DECLARE @fiscal_year_start INT = 4;  -- April

SELECT 
    date_col,
    MONTH(date_col) AS calendar_month,
    CASE 
        WHEN MONTH(date_col) >= @fiscal_year_start THEN MONTH(date_col) - @fiscal_year_start + 1
        ELSE MONTH(date_col) + 12 - @fiscal_year_start + 1
    END AS fiscal_month
FROM your_table;
*/

-- SQLite: Fiscal Month (July start)
/*
SELECT 
    date_col,
    CAST(strftime('%m', date_col) AS INTEGER) AS calendar_month,
    CASE 
        WHEN CAST(strftime('%m', date_col) AS INTEGER) >= 7 THEN CAST(strftime('%m', date_col) AS INTEGER) - 7 + 1
        ELSE CAST(strftime('%m', date_col) AS INTEGER) + 6
    END AS fiscal_month
FROM your_table;
-- Fiscal months: Jul=1, Aug=2, Sep=3, Oct=4, Nov=5, Dec=6, Jan=7, Feb=8, Mar=9, Apr=10, May=11, Jun=12
*/

-- ============================================================================
-- SECTION 6: YEAR-OVER-YEAR COMPARISONS
-- ============================================================================

-- Compare current period with same period in previous fiscal year

-- MySQL: Year-over-Year comparison
/*
SELECT 
    -- Current fiscal period
    CASE 
        WHEN MONTH(order_date) >= 4 THEN YEAR(order_date)
        ELSE YEAR(order_date) - 1
    END AS fiscal_year,
    CASE 
        WHEN MONTH(order_date) BETWEEN 4 AND 6 THEN 1
        WHEN MONTH(order_date) BETWEEN 7 AND 9 THEN 2
        WHEN MONTH(order_date) BETWEEN 10 AND 12 THEN 3
        ELSE 4
    END AS fiscal_quarter,
    -- Current period sales
    SUM(CASE 
        WHEN CASE WHEN MONTH(order_date) >= 4 THEN YEAR(order_date) ELSE YEAR(order_date) - 1 END = 2024
        THEN amount ELSE 0 END) AS current_fy_sales,
    -- Previous period sales
    SUM(CASE 
        WHEN CASE WHEN MONTH(order_date) >= 4 THEN YEAR(order_date) ELSE YEAR(order_date) - 1 END = 2023
        THEN amount ELSE 0 END) AS previous_fy_sales,
    -- YoY growth
    (SUM(CASE WHEN CASE WHEN MONTH(order_date) >= 4 THEN YEAR(order_date) ELSE YEAR(order_date) - 1 END = 2024 THEN amount ELSE 0 END) -
     SUM(CASE WHEN CASE WHEN MONTH(order_date) >= 4 THEN YEAR(order_date) ELSE YEAR(order_date) - 1 END = 2023 THEN amount ELSE 0 END)) /
    NULLIF(SUM(CASE WHEN CASE WHEN MONTH(order_date) >= 4 THEN YEAR(order_date) ELSE YEAR(order_date) - 1 END = 2023 THEN amount ELSE 0 END), 0) * 100 AS yoy_growth_pct
FROM orders
GROUP BY fiscal_year, fiscal_quarter
ORDER BY fiscal_year, fiscal_quarter;
*/

-- PostgreSQL: Year-over-Year comparison
/*
WITH fiscal_orders AS (
    SELECT 
        order_date,
        amount,
        CASE 
            WHEN EXTRACT(MONTH FROM order_date) >= 4 THEN EXTRACT(YEAR FROM order_date)
            ELSE EXTRACT(YEAR FROM order_date) - 1
        END AS fiscal_year,
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
    SUM(amount) AS total_sales,
    LAG(SUM(amount)) OVER (ORDER BY fiscal_year, fiscal_quarter) AS prev_period_sales,
    (SUM(amount) - LAG(SUM(amount)) OVER (ORDER BY fiscal_year, fiscal_quarter)) / 
    LAG(SUM(amount)) OVER (ORDER BY fiscal_year, fiscal_quarter) * 100 AS growth_pct
FROM fiscal_orders
GROUP BY fiscal_year, fiscal_quarter
ORDER BY fiscal_year, fiscal_quarter;
*/

-- SQL Server: Year-over-Year comparison
/*
WITH FiscalOrders AS (
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
)
SELECT 
    fiscal_year,
    fiscal_quarter,
    SUM(amount) AS total_sales,
    LAG(SUM(amount)) OVER (ORDER BY fiscal_year, fiscal_quarter) AS prev_period_sales,
    (SUM(amount) - LAG(SUM(amount)) OVER (ORDER BY fiscal_year, fiscal_quarter)) * 100.0 /
    NULLIF(LAG(SUM(amount)) OVER (ORDER BY fiscal_year, fiscal_quarter), 0) AS growth_pct
FROM FiscalOrders
GROUP BY fiscal_year, fiscal_quarter
ORDER BY fiscal_year, fiscal_quarter;
*/

-- SQLite: Year-over-Year comparison
/*
WITH fiscal_orders AS (
    SELECT 
        order_date,
        amount,
        CASE 
            WHEN CAST(strftime('%m', order_date) AS INTEGER) >= 4 THEN CAST(strftime('%Y', order_date) AS INTEGER)
            ELSE CAST(strftime('%Y', order_date) AS INTEGER) - 1
        END AS fiscal_year,
        CASE 
            WHEN CAST(strftime('%m', order_date) AS INTEGER) BETWEEN 4 AND 6 THEN 1
            WHEN CAST(strftime('%m', order_date) AS INTEGER) BETWEEN 7 AND 9 THEN 2
            WHEN CAST(strftime('%m', order_date) AS INTEGER) BETWEEN 10 AND 12 THEN 3
            ELSE 4
        END AS fiscal_quarter
    FROM orders
)
SELECT 
    fiscal_year,
    fiscal_quarter,
    SUM(amount) AS total_sales
FROM fiscal_orders
GROUP BY fiscal_year, fiscal_quarter
ORDER BY fiscal_year, fiscal_quarter;
*/

-- ============================================================================
-- SECTION 7: FISCAL PERIOD AGGREGATIONS
-- ============================================================================

-- Aggregate data by fiscal year/quarter

-- MySQL: Sales by Fiscal Quarter
/*
SELECT 
    CASE 
        WHEN MONTH(order_date) >= 4 THEN YEAR(order_date)
        ELSE YEAR(order_date) - 1
    END AS fiscal_year,
    CASE 
        WHEN MONTH(order_date) BETWEEN 4 AND 6 THEN 1
        WHEN MONTH(order_date) BETWEEN 7 AND 9 THEN 2
        WHEN MONTH(order_date) BETWEEN 10 AND 12 THEN 3
        ELSE 4
    END AS fiscal_quarter,
    CONCAT('FY', CASE WHEN MONTH(order_date) >= 4 THEN YEAR(order_date) ELSE YEAR(order_date) - 1 END,
           '-Q', CASE 
               WHEN MONTH(order_date) BETWEEN 4 AND 6 THEN 1
               WHEN MONTH(order_date) BETWEEN 7 AND 9 THEN 2
               WHEN MONTH(order_date) BETWEEN 10 AND 12 THEN 3
               ELSE 4
           END) AS fiscal_period,
    COUNT(*) AS order_count,
    SUM(amount) AS total_sales,
    AVG(amount) AS avg_order_value,
    MIN(amount) AS min_order,
    MAX(amount) AS max_order
FROM orders
GROUP BY fiscal_year, fiscal_quarter
ORDER BY fiscal_year, fiscal_quarter;
*/

-- PostgreSQL: Running total by fiscal period
/*
WITH fiscal_data AS (
    SELECT 
        order_date,
        amount,
        CASE 
            WHEN EXTRACT(MONTH FROM order_date) >= 4 THEN EXTRACT(YEAR FROM order_date)
            ELSE EXTRACT(YEAR FROM order_date) - 1
        END AS fiscal_year,
        CASE 
            WHEN EXTRACT(MONTH FROM order_date) BETWEEN 4 AND 6 THEN 1
            WHEN EXTRACT(MONTH FROM order_date) BETWEEN 7 AND 9 THEN 2
            WHEN EXTRACT(MONTH FROM order_date) BETWEEN 10 AND 12 THEN 3
            ELSE 4
        END AS fiscal_quarter
    FROM orders
),
period_totals AS (
    SELECT 
        fiscal_year,
        fiscal_quarter,
        SUM(amount) AS period_sales
    FROM fiscal_data
    GROUP BY fiscal_year, fiscal_quarter
)
SELECT 
    fiscal_year,
    fiscal_quarter,
    period_sales,
    SUM(period_sales) OVER (ORDER BY fiscal_year, fiscal_quarter) AS running_total,
    AVG(period_sales) OVER (
        ORDER BY fiscal_year, fiscal_quarter 
        ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
    ) AS moving_avg_4q
FROM period_totals
ORDER BY fiscal_year, fiscal_quarter;
*/

-- SQL Server: Month-to-date and Quarter-to-date within fiscal year
/*
DECLARE @report_date DATE = '2024-08-15';
DECLARE @fiscal_year_start INT = 4;  -- April

SELECT 
    -- Fiscal period info
    CASE 
        WHEN MONTH(@report_date) >= @fiscal_year_start THEN YEAR(@report_date)
        ELSE YEAR(@report_date) - 1
    END AS current_fiscal_year,
    CASE 
        WHEN MONTH(@report_date) BETWEEN 4 AND 6 THEN 1
        WHEN MONTH(@report_date) BETWEEN 7 AND 9 THEN 2
        WHEN MONTH(@report_date) BETWEEN 10 AND 12 THEN 3
        ELSE 4
    END AS current_fiscal_quarter,
    -- Month-to-date sales
    SUM(CASE 
        WHEN order_date >= DATEFROMPARTS(YEAR(@report_date), MONTH(@report_date), 1) 
         AND order_date <= @report_date 
        THEN amount ELSE 0 END) AS mtd_sales,
    -- Quarter-to-date sales
    SUM(CASE 
        WHEN order_date >= CASE 
            WHEN MONTH(@report_date) BETWEEN 4 AND 6 THEN DATEFROMPARTS(YEAR(@report_date), 4, 1)
            WHEN MONTH(@report_date) BETWEEN 7 AND 9 THEN DATEFROMPARTS(YEAR(@report_date), 7, 1)
            WHEN MONTH(@report_date) BETWEEN 10 AND 12 THEN DATEFROMPARTS(YEAR(@report_date), 10, 1)
            ELSE DATEFROMPARTS(YEAR(@report_date), 1, 1)
        END
         AND order_date <= @report_date 
        THEN amount ELSE 0 END) AS qtd_sales,
    -- Year-to-date sales (fiscal year)
    SUM(CASE 
        WHEN order_date >= CASE 
            WHEN MONTH(@report_date) >= @fiscal_year_start THEN DATEFROMPARTS(YEAR(@report_date), @fiscal_year_start, 1)
            ELSE DATEFROMPARTS(YEAR(@report_date) - 1, @fiscal_year_start, 1)
        END
         AND order_date <= @report_date 
        THEN amount ELSE 0 END) AS ytd_sales
FROM orders
WHERE order_date <= @report_date;
*/

-- ============================================================================
-- SECTION 8: FISCAL PERIOD LABELS AND FORMATTING
-- ============================================================================

-- Generate human-readable fiscal period labels

-- MySQL: Fiscal period labels
/*
SELECT 
    date_col,
    -- Short label: "FY24 Q2"
    CONCAT('FY', RIGHT(CAST(
        CASE WHEN MONTH(date_col) >= 4 THEN YEAR(date_col) ELSE YEAR(date_col) - 1 END
    AS CHAR), 2), 
    ' Q', CASE 
        WHEN MONTH(date_col) BETWEEN 4 AND 6 THEN 1
        WHEN MONTH(date_col) BETWEEN 7 AND 9 THEN 2
        WHEN MONTH(date_col) BETWEEN 10 AND 12 THEN 3
        ELSE 4
    END) AS short_label,
    -- Full label: "Fiscal Year 2024 - Quarter 2"
    CONCAT('Fiscal Year ', 
        CASE WHEN MONTH(date_col) >= 4 THEN YEAR(date_col) ELSE YEAR(date_col) - 1 END,
        ' - Quarter ',
        CASE 
            WHEN MONTH(date_col) BETWEEN 4 AND 6 THEN 1
            WHEN MONTH(date_col) BETWEEN 7 AND 9 THEN 2
            WHEN MONTH(date_col) BETWEEN 10 AND 12 THEN 3
            ELSE 4
        END) AS full_label,
    -- Period range: "Apr 2024 - Jun 2024"
    CASE 
        WHEN MONTH(date_col) BETWEEN 4 AND 6 THEN CONCAT('Apr ', YEAR(date_col), ' - Jun ', YEAR(date_col))
        WHEN MONTH(date_col) BETWEEN 7 AND 9 THEN CONCAT('Jul ', YEAR(date_col), ' - Sep ', YEAR(date_col))
        WHEN MONTH(date_col) BETWEEN 10 AND 12 THEN CONCAT('Oct ', YEAR(date_col), ' - Dec ', YEAR(date_col))
        ELSE CONCAT('Jan ', YEAR(date_col), ' - Mar ', YEAR(date_col))
    END AS period_range
FROM your_table;
*/

-- PostgreSQL: Fiscal period labels
/*
SELECT 
    date_col,
    -- Short label: "FY24 Q2"
    'FY' || TO_CHAR(
        CASE WHEN EXTRACT(MONTH FROM date_col) >= 4 THEN EXTRACT(YEAR FROM date_col) ELSE EXTRACT(YEAR FROM date_col) - 1 END,
        'FM00'
    ) || ' Q' || CASE 
        WHEN EXTRACT(MONTH FROM date_col) BETWEEN 4 AND 6 THEN 1
        WHEN EXTRACT(MONTH FROM date_col) BETWEEN 7 AND 9 THEN 2
        WHEN EXTRACT(MONTH FROM date_col) BETWEEN 10 AND 12 THEN 3
        ELSE 4
    END AS short_label,
    -- Quarter name
    CASE 
        WHEN EXTRACT(MONTH FROM date_col) BETWEEN 4 AND 6 THEN 'Q1 (Apr-Jun)'
        WHEN EXTRACT(MONTH FROM date_col) BETWEEN 7 AND 9 THEN 'Q2 (Jul-Sep)'
        WHEN EXTRACT(MONTH FROM date_col) BETWEEN 10 AND 12 THEN 'Q3 (Oct-Dec)'
        ELSE 'Q4 (Jan-Mar)'
    END AS quarter_name
FROM your_table;
*/

-- SQL Server: Fiscal period labels
/*
SELECT 
    date_col,
    -- Short label
    CONCAT('FY', RIGHT(CAST(
        CASE WHEN MONTH(date_col) >= 4 THEN YEAR(date_col) ELSE YEAR(date_col) - 1 END
    AS VARCHAR), 2), 
    ' Q', CASE 
        WHEN MONTH(date_col) BETWEEN 4 AND 6 THEN 1
        WHEN MONTH(date_col) BETWEEN 7 AND 9 THEN 2
        WHEN MONTH(date_col) BETWEEN 10 AND 12 THEN 3
        ELSE 4
    END) AS short_label,
    -- Full description
    FORMAT(date_col, 'MMMM yyyy') AS month_year,
    CASE 
        WHEN MONTH(date_col) BETWEEN 4 AND 6 THEN 'First Quarter'
        WHEN MONTH(date_col) BETWEEN 7 AND 9 THEN 'Second Quarter'
        WHEN MONTH(date_col) BETWEEN 10 AND 12 THEN 'Third Quarter'
        ELSE 'Fourth Quarter'
    END AS quarter_description
FROM your_table;
*/

-- ============================================================================
-- SECTION 9: STORED PROCEDURES AND FUNCTIONS
-- ============================================================================

-- MySQL: Stored function for fiscal year
/*
DELIMITER //
CREATE FUNCTION GetFiscalYear(
    input_date DATE,
    fiscal_start_month INT
) RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE fy INT;
    SET fy = CASE 
        WHEN MONTH(input_date) >= fiscal_start_month THEN YEAR(input_date)
        ELSE YEAR(input_date) - 1
    END;
    RETURN fy;
END //
DELIMITER ;

-- Usage:
SELECT GetFiscalYear('2024-03-15', 4) AS fiscal_year;  -- Returns 2023
SELECT GetFiscalYear('2024-05-15', 4) AS fiscal_year;  -- Returns 2024
*/

-- MySQL: Stored function for fiscal quarter
/*
DELIMITER //
CREATE FUNCTION GetFiscalQuarter(
    input_date DATE,
    fiscal_start_month INT
) RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE fq INT;
    SET fq = CASE 
        WHEN fiscal_start_month = 1 THEN QUARTER(input_date)
        WHEN fiscal_start_month = 4 THEN
            CASE 
                WHEN MONTH(input_date) BETWEEN 4 AND 6 THEN 1
                WHEN MONTH(input_date) BETWEEN 7 AND 9 THEN 2
                WHEN MONTH(input_date) BETWEEN 10 AND 12 THEN 3
                ELSE 4
            END
        WHEN fiscal_start_month = 7 THEN
            CASE 
                WHEN MONTH(input_date) BETWEEN 7 AND 9 THEN 1
                WHEN MONTH(input_date) BETWEEN 10 AND 12 THEN 2
                WHEN MONTH(input_date) BETWEEN 1 AND 3 THEN 3
                ELSE 4
            END
        WHEN fiscal_start_month = 10 THEN
            CASE 
                WHEN MONTH(input_date) BETWEEN 10 AND 12 THEN 1
                WHEN MONTH(input_date) BETWEEN 1 AND 3 THEN 2
                WHEN MONTH(input_date) BETWEEN 4 AND 6 THEN 3
                ELSE 4
            END
        ELSE 0
    END;
    RETURN fq;
END //
DELIMITER ;

-- Usage:
SELECT GetFiscalQuarter('2024-05-15', 4) AS fiscal_quarter;  -- Returns 1
SELECT GetFiscalQuarter('2024-11-15', 10) AS fiscal_quarter;  -- Returns 1 (US Federal)
*/

-- PostgreSQL: Function for fiscal period info
/*
CREATE OR REPLACE FUNCTION get_fiscal_period(
    input_date DATE,
    fiscal_start_month INT DEFAULT 4
) RETURNS TABLE (
    fiscal_year INT,
    fiscal_quarter INT,
    fiscal_month INT,
    fiscal_period_label TEXT,
    quarter_start_date DATE,
    quarter_end_date DATE
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        CASE 
            WHEN EXTRACT(MONTH FROM input_date) >= fiscal_start_month 
            THEN EXTRACT(YEAR FROM input_date)::INT
            ELSE (EXTRACT(YEAR FROM input_date) - 1)::INT
        END AS fiscal_year,
        CASE 
            WHEN fiscal_start_month = 1 THEN EXTRACT(QUARTER FROM input_date)::INT
            WHEN fiscal_start_month = 4 THEN
                CASE 
                    WHEN EXTRACT(MONTH FROM input_date) BETWEEN 4 AND 6 THEN 1
                    WHEN EXTRACT(MONTH FROM input_date) BETWEEN 7 AND 9 THEN 2
                    WHEN EXTRACT(MONTH FROM input_date) BETWEEN 10 AND 12 THEN 3
                    ELSE 4
                END
            WHEN fiscal_start_month = 7 THEN
                CASE 
                    WHEN EXTRACT(MONTH FROM input_date) BETWEEN 7 AND 9 THEN 1
                    WHEN EXTRACT(MONTH FROM input_date) BETWEEN 10 AND 12 THEN 2
                    WHEN EXTRACT(MONTH FROM input_date) BETWEEN 1 AND 3 THEN 3
                    ELSE 4
                END
            WHEN fiscal_start_month = 10 THEN
                CASE 
                    WHEN EXTRACT(MONTH FROM input_date) BETWEEN 10 AND 12 THEN 1
                    WHEN EXTRACT(MONTH FROM input_date) BETWEEN 1 AND 3 THEN 2
                    WHEN EXTRACT(MONTH FROM input_date) BETWEEN 4 AND 6 THEN 3
                    ELSE 4
                END
            ELSE 0
        END AS fiscal_quarter,
        CASE 
            WHEN EXTRACT(MONTH FROM input_date) >= fiscal_start_month 
            THEN (EXTRACT(MONTH FROM input_date) - fiscal_start_month + 1)::INT
            ELSE (EXTRACT(MONTH FROM input_date) + 12 - fiscal_start_month + 1)::INT
        END AS fiscal_month,
        'FY' || CASE 
            WHEN EXTRACT(MONTH FROM input_date) >= fiscal_start_month 
            THEN EXTRACT(YEAR FROM input_date)::INT
            ELSE (EXTRACT(YEAR FROM input_date) - 1)::INT
        END || '-Q' || CASE 
            WHEN fiscal_start_month = 4 THEN
                CASE 
                    WHEN EXTRACT(MONTH FROM input_date) BETWEEN 4 AND 6 THEN 1
                    WHEN EXTRACT(MONTH FROM input_date) BETWEEN 7 AND 9 THEN 2
                    WHEN EXTRACT(MONTH FROM input_date) BETWEEN 10 AND 12 THEN 3
                    ELSE 4
                END
            ELSE EXTRACT(QUARTER FROM input_date)::INT
        END AS fiscal_period_label,
        input_date AS quarter_start_date,  -- Simplified
        input_date AS quarter_end_date      -- Simplified
    ;
END;
$$ LANGUAGE plpgsql;

-- Usage:
SELECT * FROM get_fiscal_period('2024-05-15'::DATE, 4);
SELECT * FROM get_fiscal_period('2024-11-15'::DATE, 10);
*/

-- SQL Server: Function for fiscal period
/*
CREATE FUNCTION dbo.GetFiscalPeriod(
    @input_date DATE,
    @fiscal_start_month INT = 4
)
RETURNS TABLE
AS
RETURN
SELECT 
    CASE 
        WHEN MONTH(@input_date) >= @fiscal_start_month THEN YEAR(@input_date)
        ELSE YEAR(@input_date) - 1
    END AS fiscal_year,
    CASE 
        WHEN @fiscal_start_month = 1 THEN DATEPART(QUARTER, @input_date)
        WHEN @fiscal_start_month = 4 THEN
            CASE 
                WHEN MONTH(@input_date) BETWEEN 4 AND 6 THEN 1
                WHEN MONTH(@input_date) BETWEEN 7 AND 9 THEN 2
                WHEN MONTH(@input_date) BETWEEN 10 AND 12 THEN 3
                ELSE 4
            END
        WHEN @fiscal_start_month = 7 THEN
            CASE 
                WHEN MONTH(@input_date) BETWEEN 7 AND 9 THEN 1
                WHEN MONTH(@input_date) BETWEEN 10 AND 12 THEN 2
                WHEN MONTH(@input_date) BETWEEN 1 AND 3 THEN 3
                ELSE 4
            END
        WHEN @fiscal_start_month = 10 THEN
            CASE 
                WHEN MONTH(@input_date) BETWEEN 10 AND 12 THEN 1
                WHEN MONTH(@input_date) BETWEEN 1 AND 3 THEN 2
                WHEN MONTH(@input_date) BETWEEN 4 AND 6 THEN 3
                ELSE 4
            END
        ELSE 0
    END AS fiscal_quarter,
    CASE 
        WHEN MONTH(@input_date) >= @fiscal_start_month 
        THEN MONTH(@input_date) - @fiscal_start_month + 1
        ELSE MONTH(@input_date) + 12 - @fiscal_start_month + 1
    END AS fiscal_month,
    CONCAT('FY', RIGHT(CAST(
        CASE WHEN MONTH(@input_date) >= @fiscal_start_month THEN YEAR(@input_date) ELSE YEAR(@input_date) - 1 END
    AS VARCHAR), 2), '-Q', CASE 
        WHEN @fiscal_start_month = 4 THEN
            CASE 
                WHEN MONTH(@input_date) BETWEEN 4 AND 6 THEN 1
                WHEN MONTH(@input_date) BETWEEN 7 AND 9 THEN 2
                WHEN MONTH(@input_date) BETWEEN 10 AND 12 THEN 3
                ELSE 4
            END
        ELSE DATEPART(QUARTER, @input_date)
    END) AS fiscal_period_label;

-- Usage:
SELECT * FROM dbo.GetFiscalPeriod('2024-05-15', 4);
SELECT * FROM dbo.GetFiscalPeriod('2024-11-15', 10);
*/

-- ============================================================================
-- SECTION 10: PRACTICAL USE CASES
-- ============================================================================

-- Use Case 1: Get sales for current fiscal quarter vs previous quarter
-- MySQL:
/*
SET @fiscal_year_start = 4;
SET @current_date = CURDATE();
SET @current_fy = CASE WHEN MONTH(@current_date) >= @fiscal_year_start THEN YEAR(@current_date) ELSE YEAR(@current_date) - 1 END;
SET @current_fq = CASE 
    WHEN MONTH(@current_date) BETWEEN 4 AND 6 THEN 1
    WHEN MONTH(@current_date) BETWEEN 7 AND 9 THEN 2
    WHEN MONTH(@current_date) BETWEEN 10 AND 12 THEN 3
    ELSE 4
END;

SELECT 
    SUM(CASE WHEN 
        CASE WHEN MONTH(order_date) >= @fiscal_year_start THEN YEAR(order_date) ELSE YEAR(order_date) - 1 END = @current_fy
        AND CASE 
            WHEN MONTH(order_date) BETWEEN 4 AND 6 THEN 1
            WHEN MONTH(order_date) BETWEEN 7 AND 9 THEN 2
            WHEN MONTH(order_date) BETWEEN 10 AND 12 THEN 3
            ELSE 4
        END = @current_fq
    THEN amount ELSE 0 END) AS current_quarter_sales,
    SUM(CASE WHEN 
        CASE WHEN MONTH(order_date) >= @fiscal_year_start THEN YEAR(order_date) ELSE YEAR(order_date) - 1 END = @current_fy
        AND CASE 
            WHEN MONTH(order_date) BETWEEN 4 AND 6 THEN 1
            WHEN MONTH(order_date) BETWEEN 7 AND 9 THEN 2
            WHEN MONTH(order_date) BETWEEN 10 AND 12 THEN 3
            ELSE 4
        END = @current_fq - 1
    THEN amount ELSE 0 END) AS previous_quarter_sales
FROM orders;
*/

-- Use Case 2: Find records in a specific fiscal period
-- PostgreSQL:
/*
SELECT *
FROM transactions
WHERE 
    CASE WHEN EXTRACT(MONTH FROM trans_date) >= 4 THEN EXTRACT(YEAR FROM trans_date) ELSE EXTRACT(YEAR FROM trans_date) - 1 END = 2024
    AND CASE 
        WHEN EXTRACT(MONTH FROM trans_date) BETWEEN 4 AND 6 THEN 1
        WHEN EXTRACT(MONTH FROM trans_date) BETWEEN 7 AND 9 THEN 2
        WHEN EXTRACT(MONTH FROM trans_date) BETWEEN 10 AND 12 THEN 3
        ELSE 4
    END = 2;
-- This returns all transactions in FY2024 Q2 (Jul-Sep 2024)
*/

-- Use Case 3: Group by fiscal period with running totals
-- SQL Server:
/*
WITH FiscalPeriodData AS (
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
FiscalPeriodTotals AS (
    SELECT 
        fiscal_year,
        fiscal_quarter,
        SUM(amount) AS period_sales
    FROM FiscalPeriodData
    GROUP BY fiscal_year, fiscal_quarter
)
SELECT 
    fiscal_year,
    fiscal_quarter,
    period_sales,
    SUM(period_sales) OVER (
        ORDER BY fiscal_year, fiscal_quarter
    ) AS cumulative_sales,
    LAG(period_sales, 4) OVER (
        ORDER BY fiscal_year, fiscal_quarter
    ) AS same_quarter_last_year
FROM FiscalPeriodTotals
ORDER BY fiscal_year, fiscal_quarter;
*/

-- Use Case 4: Calculate fiscal year-to-date metrics
-- SQLite:
/*
SELECT 
    SUM(amount) AS ytd_sales,
    COUNT(*) AS ytd_transactions,
    AVG(amount) AS avg_transaction
FROM orders
WHERE 
    -- Fiscal year starts in April
    date(order_date) >= CASE 
        WHEN CAST(strftime('%m', 'now') AS INTEGER) >= 4 
        THEN date(strftime('%Y', 'now') || '-04-01')
        ELSE date((CAST(strftime('%Y', 'now') AS INTEGER) - 1) || '-04-01')
    END
    AND date(order_date) <= date('now');
*/

-- ============================================================================
-- SECTION 11: COMMON FISCAL YEAR CONFIGURATIONS QUICK REFERENCE
-- ============================================================================

-- Calendar Year (January 1 start) - Default
--   Fiscal Year = Calendar Year
--   Fiscal Q1 = Jan-Mar
--   Fiscal Q2 = Apr-Jun
--   Fiscal Q3 = Jul-Sep
--   Fiscal Q4 = Oct-Dec

-- US Federal Government (October 1 start)
--   FY2024 = Oct 1, 2023 to Sep 30, 2024
--   Fiscal Q1 = Oct-Dec (previous calendar year)
--   Fiscal Q2 = Jan-Mar
--   Fiscal Q3 = Apr-Jun
--   Fiscal Q4 = Jul-Sep

-- UK/India/Japan (April 1 start)
--   FY2024 = Apr 1, 2024 to Mar 31, 2025
--   Fiscal Q1 = Apr-Jun
--   Fiscal Q2 = Jul-Sep
--   Fiscal Q3 = Oct-Dec
--   Fiscal Q4 = Jan-Mar

-- Australia/New Zealand (July 1 start)
--   FY2024 = Jul 1, 2023 to Jun 30, 2024
--   Fiscal Q1 = Jul-Sep
--   Fiscal Q2 = Oct-Dec
--   Fiscal Q3 = Jan-Mar
--   Fiscal Q4 = Apr-Jun

-- ============================================================================
-- END OF MODULE
-- ============================================================================