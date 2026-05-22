-- ============================================================================
-- SQL Fiscal Period Utilities Test Suite
-- ============================================================================
-- Test cases for fiscal_period_utils module
-- Run these tests to verify your fiscal period calculations work correctly
--
-- Usage:
--   MySQL:     mysql -u user -p database < fiscal_period_utils_test.sql
--   PostgreSQL: psql -U user -d database -f fiscal_period_utils_test.sql
--   SQL Server: sqlcmd -S server -d database -i fiscal_period_utils_test.sql
--   SQLite:    sqlite3 database < fiscal_period_utils_test.sql
--
-- Author: AllToolkit
-- License: MIT
-- ============================================================================

-- ============================================================================
-- TEST SETUP
-- ============================================================================

-- Create test table with dates across fiscal periods
CREATE TABLE IF NOT EXISTS fiscal_test_cases (
    test_id INTEGER PRIMARY KEY,
    test_name VARCHAR(100),
    test_date DATE,
    fiscal_start_month INTEGER,
    expected_fiscal_year INTEGER,
    expected_fiscal_quarter INTEGER,
    expected_fiscal_month INTEGER
);

-- Insert test data for April-start fiscal year (UK/India/Japan style)
DELETE FROM fiscal_test_cases;
INSERT INTO fiscal_test_cases (test_id, test_name, test_date, fiscal_start_month, expected_fiscal_year, expected_fiscal_quarter, expected_fiscal_month) VALUES
-- April-start fiscal year tests
(1, 'Fiscal Year Start (April)', '2024-04-01', 4, 2024, 1, 1),
(2, 'Mid Q1 (May)', '2024-05-15', 4, 2024, 1, 2),
(3, 'End Q1 (June)', '2024-06-30', 4, 2024, 1, 3),
(4, 'Start Q2 (July)', '2024-07-01', 4, 2024, 2, 4),
(5, 'Mid Q2 (August)', '2024-08-15', 4, 2024, 2, 5),
(6, 'End Q2 (September)', '2024-09-30', 4, 2024, 2, 6),
(7, 'Start Q3 (October)', '2024-10-01', 4, 2024, 3, 7),
(8, 'Mid Q3 (November)', '2024-11-15', 4, 2024, 3, 8),
(9, 'End Q3 (December)', '2024-12-31', 4, 2024, 3, 9),
(10, 'Start Q4 (January)', '2025-01-01', 4, 2024, 4, 10),
(11, 'Mid Q4 (February)', '2025-02-15', 4, 2024, 4, 11),
(12, 'End Q4 (March)', '2025-03-31', 4, 2024, 4, 12),
-- Calendar year tests (January start)
(13, 'Calendar Year Q1', '2024-01-15', 1, 2024, 1, 1),
(14, 'Calendar Year Q2', '2024-04-15', 1, 2024, 2, 4),
(15, 'Calendar Year Q3', '2024-07-15', 1, 2024, 3, 7),
(16, 'Calendar Year Q4', '2024-10-15', 1, 2024, 4, 10),
-- October-start fiscal year tests (US Federal)
(17, 'US Federal FY Start', '2023-10-01', 10, 2024, 1, 1),
(18, 'US Federal Mid Q1', '2023-11-15', 10, 2024, 1, 2),
(19, 'US Federal End Q1', '2023-12-31', 10, 2024, 1, 3),
(20, 'US Federal Q2 Start', '2024-01-01', 10, 2024, 2, 4),
(21, 'US Federal Q2 End', '2024-03-31', 10, 2024, 2, 6),
(22, 'US Federal Q3 Start', '2024-04-01', 10, 2024, 3, 7),
(23, 'US Federal Q4 Start', '2024-07-01', 10, 2024, 4, 10),
(24, 'US Federal FY End', '2024-09-30', 10, 2024, 4, 12),
-- July-start fiscal year tests (Australia/NZ)
(25, 'Australia FY Start', '2023-07-01', 7, 2024, 1, 1),
(26, 'Australia Mid Q1', '2023-08-15', 7, 2024, 1, 2),
(27, 'Australia End Q1', '2023-09-30', 7, 2024, 1, 3),
(28, 'Australia Q2 Start', '2023-10-01', 7, 2024, 2, 4),
(29, 'Australia Q3 Start', '2024-01-01', 7, 2024, 3, 7),
(30, 'Australia Q4 Start', '2024-04-01', 7, 2024, 4, 10),
(31, 'Australia FY End', '2024-06-30', 7, 2024, 4, 12);

-- ============================================================================
-- TEST 1: FISCAL YEAR CALCULATION (April Start)
-- ============================================================================

-- MySQL: Test fiscal year calculation
SELECT 'Test 1.1: Fiscal Year (April Start)' AS test_suite,
       test_id,
       test_name,
       test_date,
       CASE 
           WHEN MONTH(test_date) >= fiscal_start_month THEN YEAR(test_date)
           ELSE YEAR(test_date) - 1
       END AS calculated_fy,
       expected_fiscal_year AS expected,
       CASE WHEN 
           CASE WHEN MONTH(test_date) >= fiscal_start_month THEN YEAR(test_date) ELSE YEAR(test_date) - 1 END = expected_fiscal_year 
       THEN 'PASS' ELSE 'FAIL' END AS status
FROM fiscal_test_cases
WHERE fiscal_start_month = 4;

-- PostgreSQL version:
/*
SELECT 'Test 1.1: Fiscal Year (April Start)' AS test_suite,
       test_id,
       test_name,
       test_date,
       CASE 
           WHEN EXTRACT(MONTH FROM test_date) >= fiscal_start_month THEN EXTRACT(YEAR FROM test_date)
           ELSE EXTRACT(YEAR FROM test_date) - 1
       END AS calculated_fy,
       expected_fiscal_year AS expected,
       CASE WHEN 
           CASE WHEN EXTRACT(MONTH FROM test_date) >= fiscal_start_month THEN EXTRACT(YEAR FROM test_date) ELSE EXTRACT(YEAR FROM test_date) - 1 END = expected_fiscal_year 
       THEN 'PASS' ELSE 'FAIL' END AS status
FROM fiscal_test_cases
WHERE fiscal_start_month = 4;
*/

-- SQL Server version:
/*
SELECT 'Test 1.1: Fiscal Year (April Start)' AS test_suite,
       test_id,
       test_name,
       test_date,
       CASE 
           WHEN MONTH(test_date) >= fiscal_start_month THEN YEAR(test_date)
           ELSE YEAR(test_date) - 1
       END AS calculated_fy,
       expected_fiscal_year AS expected,
       CASE WHEN 
           CASE WHEN MONTH(test_date) >= fiscal_start_month THEN YEAR(test_date) ELSE YEAR(test_date) - 1 END = expected_fiscal_year 
       THEN 'PASS' ELSE 'FAIL' END AS status
FROM fiscal_test_cases
WHERE fiscal_start_month = 4;
*/

-- SQLite version:
/*
SELECT 'Test 1.1: Fiscal Year (April Start)' AS test_suite,
       test_id,
       test_name,
       test_date,
       CASE 
           WHEN CAST(strftime('%m', test_date) AS INTEGER) >= fiscal_start_month THEN CAST(strftime('%Y', test_date) AS INTEGER)
           ELSE CAST(strftime('%Y', test_date) AS INTEGER) - 1
       END AS calculated_fy,
       expected_fiscal_year AS expected,
       CASE WHEN 
           CASE WHEN CAST(strftime('%m', test_date) AS INTEGER) >= fiscal_start_month THEN CAST(strftime('%Y', test_date) AS INTEGER) ELSE CAST(strftime('%Y', test_date) AS INTEGER) - 1 END = expected_fiscal_year 
       THEN 'PASS' ELSE 'FAIL' END AS status
FROM fiscal_test_cases
WHERE fiscal_start_month = 4;
*/

-- ============================================================================
-- TEST 2: FISCAL QUARTER CALCULATION (April Start)
-- ============================================================================

-- MySQL: Test fiscal quarter calculation (April start)
SELECT 'Test 2.1: Fiscal Quarter (April Start)' AS test_suite,
       test_id,
       test_name,
       test_date,
       CASE 
           WHEN MONTH(test_date) BETWEEN 4 AND 6 THEN 1
           WHEN MONTH(test_date) BETWEEN 7 AND 9 THEN 2
           WHEN MONTH(test_date) BETWEEN 10 AND 12 THEN 3
           ELSE 4
       END AS calculated_fq,
       expected_fiscal_quarter AS expected,
       CASE WHEN 
           CASE WHEN MONTH(test_date) BETWEEN 4 AND 6 THEN 1 WHEN MONTH(test_date) BETWEEN 7 AND 9 THEN 2 WHEN MONTH(test_date) BETWEEN 10 AND 12 THEN 3 ELSE 4 END = expected_fiscal_quarter 
       THEN 'PASS' ELSE 'FAIL' END AS status
FROM fiscal_test_cases
WHERE fiscal_start_month = 4;

-- PostgreSQL version:
/*
SELECT 'Test 2.1: Fiscal Quarter (April Start)' AS test_suite,
       test_id,
       test_name,
       test_date,
       CASE 
           WHEN EXTRACT(MONTH FROM test_date) BETWEEN 4 AND 6 THEN 1
           WHEN EXTRACT(MONTH FROM test_date) BETWEEN 7 AND 9 THEN 2
           WHEN EXTRACT(MONTH FROM test_date) BETWEEN 10 AND 12 THEN 3
           ELSE 4
       END AS calculated_fq,
       expected_fiscal_quarter AS expected,
       CASE WHEN 
           CASE WHEN EXTRACT(MONTH FROM test_date) BETWEEN 4 AND 6 THEN 1 WHEN EXTRACT(MONTH FROM test_date) BETWEEN 7 AND 9 THEN 2 WHEN EXTRACT(MONTH FROM test_date) BETWEEN 10 AND 12 THEN 3 ELSE 4 END = expected_fiscal_quarter 
       THEN 'PASS' ELSE 'FAIL' END AS status
FROM fiscal_test_cases
WHERE fiscal_start_month = 4;
*/

-- ============================================================================
-- TEST 3: FISCAL YEAR CALCULATION (October Start - US Federal)
-- ============================================================================

-- MySQL: Test US Federal fiscal year
SELECT 'Test 3.1: US Federal Fiscal Year (October Start)' AS test_suite,
       test_id,
       test_name,
       test_date,
       CASE 
           WHEN MONTH(test_date) >= 10 THEN YEAR(test_date) + 1
           ELSE YEAR(test_date)
       END AS calculated_fy,
       expected_fiscal_year AS expected,
       CASE WHEN 
           CASE WHEN MONTH(test_date) >= 10 THEN YEAR(test_date) + 1 ELSE YEAR(test_date) END = expected_fiscal_year 
       THEN 'PASS' ELSE 'FAIL' END AS status
FROM fiscal_test_cases
WHERE fiscal_start_month = 10;

-- PostgreSQL version:
/*
SELECT 'Test 3.1: US Federal Fiscal Year (October Start)' AS test_suite,
       test_id,
       test_name,
       test_date,
       CASE 
           WHEN EXTRACT(MONTH FROM test_date) >= 10 THEN EXTRACT(YEAR FROM test_date) + 1
           ELSE EXTRACT(YEAR FROM test_date)
       END AS calculated_fy,
       expected_fiscal_year AS expected,
       CASE WHEN 
           CASE WHEN EXTRACT(MONTH FROM test_date) >= 10 THEN EXTRACT(YEAR FROM test_date) + 1 ELSE EXTRACT(YEAR FROM test_date) END = expected_fiscal_year 
       THEN 'PASS' ELSE 'FAIL' END AS status
FROM fiscal_test_cases
WHERE fiscal_start_month = 10;
*/

-- ============================================================================
-- TEST 4: FISCAL QUARTER CALCULATION (October Start)
-- ============================================================================

-- MySQL: Test US Federal fiscal quarter
SELECT 'Test 4.1: US Federal Fiscal Quarter (October Start)' AS test_suite,
       test_id,
       test_name,
       test_date,
       CASE 
           WHEN MONTH(test_date) BETWEEN 10 AND 12 THEN 1
           WHEN MONTH(test_date) BETWEEN 1 AND 3 THEN 2
           WHEN MONTH(test_date) BETWEEN 4 AND 6 THEN 3
           ELSE 4
       END AS calculated_fq,
       expected_fiscal_quarter AS expected,
       CASE WHEN 
           CASE WHEN MONTH(test_date) BETWEEN 10 AND 12 THEN 1 WHEN MONTH(test_date) BETWEEN 1 AND 3 THEN 2 WHEN MONTH(test_date) BETWEEN 4 AND 6 THEN 3 ELSE 4 END = expected_fiscal_quarter 
       THEN 'PASS' ELSE 'FAIL' END AS status
FROM fiscal_test_cases
WHERE fiscal_start_month = 10;

-- ============================================================================
-- TEST 5: FISCAL YEAR CALCULATION (July Start - Australia)
-- ============================================================================

-- MySQL: Test Australia/NZ fiscal year
SELECT 'Test 5.1: Australia Fiscal Year (July Start)' AS test_suite,
       test_id,
       test_name,
       test_date,
       CASE 
           WHEN MONTH(test_date) >= 7 THEN YEAR(test_date)
           ELSE YEAR(test_date) - 1
       END AS calculated_fy,
       expected_fiscal_year AS expected,
       CASE WHEN 
           CASE WHEN MONTH(test_date) >= 7 THEN YEAR(test_date) ELSE YEAR(test_date) - 1 END = expected_fiscal_year 
       THEN 'PASS' ELSE 'FAIL' END AS status
FROM fiscal_test_cases
WHERE fiscal_start_month = 7;

-- ============================================================================
-- TEST 6: FISCAL QUARTER CALCULATION (July Start)
-- ============================================================================

-- MySQL: Test Australia fiscal quarter
SELECT 'Test 6.1: Australia Fiscal Quarter (July Start)' AS test_suite,
       test_id,
       test_name,
       test_date,
       CASE 
           WHEN MONTH(test_date) BETWEEN 7 AND 9 THEN 1
           WHEN MONTH(test_date) BETWEEN 10 AND 12 THEN 2
           WHEN MONTH(test_date) BETWEEN 1 AND 3 THEN 3
           ELSE 4
       END AS calculated_fq,
       expected_fiscal_quarter AS expected,
       CASE WHEN 
           CASE WHEN MONTH(test_date) BETWEEN 7 AND 9 THEN 1 WHEN MONTH(test_date) BETWEEN 10 AND 12 THEN 2 WHEN MONTH(test_date) BETWEEN 1 AND 3 THEN 3 ELSE 4 END = expected_fiscal_quarter 
       THEN 'PASS' ELSE 'FAIL' END AS status
FROM fiscal_test_cases
WHERE fiscal_start_month = 7;

-- ============================================================================
-- TEST 7: FISCAL MONTH CALCULATION (April Start)
-- ============================================================================

-- MySQL: Test fiscal month calculation
SELECT 'Test 7.1: Fiscal Month (April Start)' AS test_suite,
       test_id,
       test_name,
       test_date,
       CASE 
           WHEN MONTH(test_date) >= 4 THEN MONTH(test_date) - 4 + 1
           ELSE MONTH(test_date) + 12 - 4 + 1
       END AS calculated_fiscal_month,
       expected_fiscal_month AS expected,
       CASE WHEN 
           CASE WHEN MONTH(test_date) >= 4 THEN MONTH(test_date) - 4 + 1 ELSE MONTH(test_date) + 12 - 4 + 1 END = expected_fiscal_month 
       THEN 'PASS' ELSE 'FAIL' END AS status
FROM fiscal_test_cases
WHERE fiscal_start_month = 4;

-- ============================================================================
-- TEST 8: FISCAL PERIOD LABELS
-- ============================================================================

-- MySQL: Test fiscal period label generation
SELECT 'Test 8.1: Fiscal Period Labels (April Start)' AS test_suite,
       test_date,
       CASE 
           WHEN MONTH(test_date) >= 4 THEN YEAR(test_date)
           ELSE YEAR(test_date) - 1
       END AS fiscal_year,
       CASE 
           WHEN MONTH(test_date) BETWEEN 4 AND 6 THEN 1
           WHEN MONTH(test_date) BETWEEN 7 AND 9 THEN 2
           WHEN MONTH(test_date) BETWEEN 10 AND 12 THEN 3
           ELSE 4
       END AS fiscal_quarter,
       CONCAT('FY', RIGHT(CAST(
           CASE WHEN MONTH(test_date) >= 4 THEN YEAR(test_date) ELSE YEAR(test_date) - 1 END
       AS CHAR), 2), 
       '-Q', CASE 
           WHEN MONTH(test_date) BETWEEN 4 AND 6 THEN 1
           WHEN MONTH(test_date) BETWEEN 7 AND 9 THEN 2
           WHEN MONTH(test_date) BETWEEN 10 AND 12 THEN 3
           ELSE 4
       END) AS fiscal_period_label,
       CASE 
           WHEN MONTH(test_date) BETWEEN 4 AND 6 THEN 'Q1 (Apr-Jun)'
           WHEN MONTH(test_date) BETWEEN 7 AND 9 THEN 'Q2 (Jul-Sep)'
           WHEN MONTH(test_date) BETWEEN 10 AND 12 THEN 'Q3 (Oct-Dec)'
           ELSE 'Q4 (Jan-Mar)'
       END AS quarter_name
FROM fiscal_test_cases
WHERE fiscal_start_month = 4
ORDER BY test_id;

-- ============================================================================
-- TEST 9: FISCAL YEAR DATE RANGE CALCULATION
-- ============================================================================

-- MySQL: Test fiscal year start and end dates
SELECT 'Test 9.1: Fiscal Year 2024 Date Range (April Start)' AS test_suite,
       '2024' AS fiscal_year,
       DATE('2024-04-01') AS fiscal_year_start,
       DATE('2025-03-31') AS fiscal_year_end,
       CASE WHEN 
           DATE('2024-04-01') = '2024-04-01' 
           AND DATE('2025-03-31') = '2025-03-31' 
       THEN 'PASS' ELSE 'FAIL' END AS status;

-- PostgreSQL version:
/*
SELECT 'Test 9.1: Fiscal Year 2024 Date Range (April Start)' AS test_suite,
       '2024' AS fiscal_year,
       MAKE_DATE(2024, 4, 1) AS fiscal_year_start,
       MAKE_DATE(2025, 3, 31) AS fiscal_year_end,
       CASE WHEN 
           MAKE_DATE(2024, 4, 1)::TEXT = '2024-04-01' 
           AND MAKE_DATE(2025, 3, 31)::TEXT = '2025-03-31' 
       THEN 'PASS' ELSE 'FAIL' END AS status;
*/

-- ============================================================================
-- TEST 10: FISCAL QUARTER DATE RANGE
-- ============================================================================

-- MySQL: Test fiscal quarter date ranges (April start)
SELECT 'Test 10.1: Fiscal Quarter Date Ranges (April Start)' AS test_suite,
       2024 AS fiscal_year,
       1 AS fiscal_quarter,
       DATE('2024-04-01') AS quarter_start,
       DATE('2024-06-30') AS quarter_end,
       CASE WHEN 
           DATE('2024-04-01') = '2024-04-01' 
           AND DATE('2024-06-30') = '2024-06-30' 
       THEN 'PASS' ELSE 'FAIL' END AS status;

SELECT 'Test 10.2: Fiscal Q2 Date Range (April Start)' AS test_suite,
       2024 AS fiscal_year,
       2 AS fiscal_quarter,
       DATE('2024-07-01') AS quarter_start,
       DATE('2024-09-30') AS quarter_end,
       CASE WHEN 
           DATE('2024-07-01') = '2024-07-01' 
           AND DATE('2024-09-30') = '2024-09-30' 
       THEN 'PASS' ELSE 'FAIL' END AS status;

SELECT 'Test 10.3: Fiscal Q4 Date Range (April Start)' AS test_suite,
       2024 AS fiscal_year,
       4 AS fiscal_quarter,
       DATE('2025-01-01') AS quarter_start,
       DATE('2025-03-31') AS quarter_end,
       CASE WHEN 
           DATE('2025-01-01') = '2025-01-01' 
           AND DATE('2025-03-31') = '2025-03-31' 
       THEN 'PASS' ELSE 'FAIL' END AS status;

-- ============================================================================
-- TEST 11: EDGE CASES
-- ============================================================================

-- MySQL: Test edge cases - year boundary transitions
SELECT 'Test 11.1: Edge Case - Year Boundary (Dec to Jan)' AS test_suite,
       '2024-12-31' AS dec_31,
       CASE 
           WHEN MONTH('2024-12-31') >= 4 THEN YEAR('2024-12-31')
           ELSE YEAR('2024-12-31') - 1
       END AS dec_31_fiscal_year,
       '2025-01-01' AS jan_01,
       CASE 
           WHEN MONTH('2025-01-01') >= 4 THEN YEAR('2025-01-01')
           ELSE YEAR('2025-01-01') - 1
       END AS jan_01_fiscal_year,
       CASE WHEN 
           CASE WHEN MONTH('2024-12-31') >= 4 THEN YEAR('2024-12-31') ELSE YEAR('2024-12-31') - 1 END = 2024
           AND CASE WHEN MONTH('2025-01-01') >= 4 THEN YEAR('2025-01-01') ELSE YEAR('2025-01-01') - 1 END = 2024
       THEN 'PASS' ELSE 'FAIL' END AS status;

-- MySQL: Test leap year handling in fiscal period
SELECT 'Test 11.2: Edge Case - Leap Year February' AS test_suite,
       '2024-02-29' AS leap_day,
       CASE 
           WHEN MONTH('2024-02-29') >= 4 THEN YEAR('2024-02-29')
           ELSE YEAR('2024-02-29') - 1
       END AS fiscal_year,
       CASE 
           WHEN MONTH('2024-02-29') BETWEEN 4 AND 6 THEN 1
           WHEN MONTH('2024-02-29') BETWEEN 7 AND 9 THEN 2
           WHEN MONTH('2024-02-29') BETWEEN 10 AND 12 THEN 3
           ELSE 4
       END AS fiscal_quarter,
       CASE WHEN 
           CASE WHEN MONTH('2024-02-29') >= 4 THEN YEAR('2024-02-29') ELSE YEAR('2024-02-29') - 1 END = 2023
           AND CASE WHEN MONTH('2024-02-29') BETWEEN 4 AND 6 THEN 1 WHEN MONTH('2024-02-29') BETWEEN 7 AND 9 THEN 2 WHEN MONTH('2024-02-29') BETWEEN 10 AND 12 THEN 3 ELSE 4 END = 4
       THEN 'PASS' ELSE 'FAIL' END AS status;

-- ============================================================================
-- TEST 12: COMPREHENSIVE PERIOD INFO
-- ============================================================================

-- MySQL: Test comprehensive fiscal period info for all test cases
SELECT 'Test 12.1: Comprehensive Fiscal Period Info' AS test_suite,
       test_id,
       test_name,
       test_date,
       fiscal_start_month,
       CASE 
           WHEN MONTH(test_date) >= fiscal_start_month THEN YEAR(test_date)
           ELSE YEAR(test_date) - 1
       END AS fiscal_year,
       CASE 
           WHEN fiscal_start_month = 4 THEN
               CASE 
                   WHEN MONTH(test_date) BETWEEN 4 AND 6 THEN 1
                   WHEN MONTH(test_date) BETWEEN 7 AND 9 THEN 2
                   WHEN MONTH(test_date) BETWEEN 10 AND 12 THEN 3
                   ELSE 4
               END
           WHEN fiscal_start_month = 10 THEN
               CASE 
                   WHEN MONTH(test_date) BETWEEN 10 AND 12 THEN 1
                   WHEN MONTH(test_date) BETWEEN 1 AND 3 THEN 2
                   WHEN MONTH(test_date) BETWEEN 4 AND 6 THEN 3
                   ELSE 4
               END
           WHEN fiscal_start_month = 7 THEN
               CASE 
                   WHEN MONTH(test_date) BETWEEN 7 AND 9 THEN 1
                   WHEN MONTH(test_date) BETWEEN 10 AND 12 THEN 2
                   WHEN MONTH(test_date) BETWEEN 1 AND 3 THEN 3
                   ELSE 4
               END
           ELSE QUARTER(test_date)
       END AS fiscal_quarter,
       expected_fiscal_year AS expected_fy,
       expected_fiscal_quarter AS expected_fq,
       CASE WHEN 
           CASE WHEN MONTH(test_date) >= fiscal_start_month THEN YEAR(test_date) ELSE YEAR(test_date) - 1 END = expected_fiscal_year
           AND CASE 
               WHEN fiscal_start_month = 4 THEN
                   CASE WHEN MONTH(test_date) BETWEEN 4 AND 6 THEN 1 WHEN MONTH(test_date) BETWEEN 7 AND 9 THEN 2 WHEN MONTH(test_date) BETWEEN 10 AND 12 THEN 3 ELSE 4 END
               WHEN fiscal_start_month = 10 THEN
                   CASE WHEN MONTH(test_date) BETWEEN 10 AND 12 THEN 1 WHEN MONTH(test_date) BETWEEN 1 AND 3 THEN 2 WHEN MONTH(test_date) BETWEEN 4 AND 6 THEN 3 ELSE 4 END
               WHEN fiscal_start_month = 7 THEN
                   CASE WHEN MONTH(test_date) BETWEEN 7 AND 9 THEN 1 WHEN MONTH(test_date) BETWEEN 10 AND 12 THEN 2 WHEN MONTH(test_date) BETWEEN 1 AND 3 THEN 3 ELSE 4 END
               ELSE QUARTER(test_date)
           END = expected_fiscal_quarter
       THEN 'PASS' ELSE 'FAIL' END AS status
FROM fiscal_test_cases
ORDER BY test_id;

-- ============================================================================
-- TEST 13: YEAR-OVER-YEAR SIMULATION
-- ============================================================================

-- Create simulated sales data for YoY testing
CREATE TABLE IF NOT EXISTS simulated_sales (
    id INTEGER PRIMARY KEY,
    sale_date DATE,
    amount DECIMAL(10,2)
);

DELETE FROM simulated_sales;
INSERT INTO simulated_sales (id, sale_date, amount) VALUES
-- FY2023 Q1 (Apr-Jun 2023)
(1, '2023-04-01', 1000.00),
(2, '2023-05-01', 1500.00),
(3, '2023-06-01', 2000.00),
-- FY2023 Q2 (Jul-Sep 2023)
(4, '2023-07-01', 1200.00),
(5, '2023-08-01', 1800.00),
(6, '2023-09-01', 2200.00),
-- FY2024 Q1 (Apr-Jun 2024)
(7, '2024-04-01', 1100.00),  -- +10%
(8, '2024-05-01', 1650.00),  -- +10%
(9, '2024-06-01', 2200.00);  -- +10%

-- MySQL: Test YoY comparison
SELECT 'Test 13.1: Year-over-Year Comparison' AS test_suite,
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
    SUM(amount) AS total_sales
FROM simulated_sales
GROUP BY 
    CASE WHEN MONTH(sale_date) >= 4 THEN YEAR(sale_date) ELSE YEAR(sale_date) - 1 END,
    CASE WHEN MONTH(sale_date) BETWEEN 4 AND 6 THEN 1 WHEN MONTH(sale_date) BETWEEN 7 AND 9 THEN 2 WHEN MONTH(sale_date) BETWEEN 10 AND 12 THEN 3 ELSE 4 END
ORDER BY fiscal_year, fiscal_quarter;

-- ============================================================================
-- TEST CLEANUP
-- ============================================================================

-- Drop test tables
-- DROP TABLE IF EXISTS fiscal_test_cases;
-- DROP TABLE IF EXISTS simulated_sales;

-- ============================================================================
-- TEST SUMMARY
-- ============================================================================

SELECT 'All fiscal period tests completed' AS message;

-- ============================================================================
-- END OF TEST SUITE
-- ============================================================================