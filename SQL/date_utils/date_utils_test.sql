-- ============================================================================
-- SQL Date/Time Utilities Test Suite
-- ============================================================================
-- Test cases for date_utils module
-- Run these tests to verify your database date functions work correctly
--
-- Usage:
--   MySQL:     mysql -u user -p database < date_utils_test.sql
--   PostgreSQL: psql -U user -d database -f date_utils_test.sql
--   SQL Server: sqlcmd -S server -d database -i date_utils_test.sql
--   SQLite:    sqlite3 database < date_utils_test.sql
--
-- Author: AllToolkit
-- License: MIT
-- ============================================================================

-- ============================================================================
-- TEST SETUP
-- ============================================================================

-- Create test table
CREATE TABLE IF NOT EXISTS date_test_cases (
    test_id INTEGER PRIMARY KEY,
    test_name VARCHAR(100),
    test_date DATE,
    expected_result VARCHAR(100)
);

-- Insert test data
DELETE FROM date_test_cases;
INSERT INTO date_test_cases (test_id, test_name, test_date, expected_result) VALUES
(1, 'New Year 2024', '2024-01-01', '2024-01-01'),
(2, 'Leap Day 2024', '2024-02-29', '2024-02-29'),
(3, 'Mid Year 2024', '2024-06-15', '2024-06-15'),
(4, 'Year End 2024', '2024-12-31', '2024-12-31'),
(5, 'Regular Date', '2023-05-15', '2023-05-15');

-- ============================================================================
-- TEST 1: Date Formatting
-- ============================================================================

-- Test ISO format
-- MySQL:
SELECT 'Test 1.1: ISO Format' AS test,
       DATE_FORMAT(test_date, '%Y-%m-%d') AS result,
       expected_result,
       CASE WHEN DATE_FORMAT(test_date, '%Y-%m-%d') = expected_result THEN 'PASS' ELSE 'FAIL' END AS status
FROM date_test_cases WHERE test_id = 1;

-- PostgreSQL:
-- SELECT 'Test 1.1: ISO Format' AS test,
--        TO_CHAR(test_date, 'YYYY-MM-DD') AS result,
--        expected_result,
--        CASE WHEN TO_CHAR(test_date, 'YYYY-MM-DD') = expected_result THEN 'PASS' ELSE 'FAIL' END AS status
-- FROM date_test_cases WHERE test_id = 1;

-- SQL Server:
-- SELECT 'Test 1.1: ISO Format' AS test,
--        CONVERT(VARCHAR(10), test_date, 23) AS result,
--        expected_result,
--        CASE WHEN CONVERT(VARCHAR(10), test_date, 23) = expected_result THEN 'PASS' ELSE 'FAIL' END AS status
-- FROM date_test_cases WHERE test_id = 1;

-- SQLite:
-- SELECT 'Test 1.1: ISO Format' AS test,
--        strftime('%Y-%m-%d', test_date) AS result,
--        expected_result,
--        CASE WHEN strftime('%Y-%m-%d', test_date) = expected_result THEN 'PASS' ELSE 'FAIL' END AS status
-- FROM date_test_cases WHERE test_id = 1;

-- ============================================================================
-- TEST 2: Date Arithmetic
-- ============================================================================

-- Test adding days
-- MySQL:
SELECT 'Test 2.1: Add 7 Days' AS test,
       DATE_ADD(test_date, INTERVAL 7 DAY) AS result,
       '2024-01-08' AS expected,
       CASE WHEN DATE_ADD(test_date, INTERVAL 7 DAY) = '2024-01-08' THEN 'PASS' ELSE 'FAIL' END AS status
FROM date_test_cases WHERE test_id = 1;

-- Test subtracting days
-- MySQL:
SELECT 'Test 2.2: Subtract 7 Days' AS test,
       DATE_SUB(test_date, INTERVAL 7 DAY) AS result,
       '2023-12-25' AS expected,
       CASE WHEN DATE_SUB(test_date, INTERVAL 7 DAY) = '2023-12-25' THEN 'PASS' ELSE 'FAIL' END AS status
FROM date_test_cases WHERE test_id = 1;

-- ============================================================================
-- TEST 3: Date Extraction
-- ============================================================================

-- Test year extraction
-- MySQL:
SELECT 'Test 3.1: Extract Year' AS test,
       YEAR(test_date) AS result,
       2024 AS expected,
       CASE WHEN YEAR(test_date) = 2024 THEN 'PASS' ELSE 'FAIL' END AS status
FROM date_test_cases WHERE test_id = 1;

-- Test month extraction
-- MySQL:
SELECT 'Test 3.2: Extract Month' AS test,
       MONTH(test_date) AS result,
       1 AS expected,
       CASE WHEN MONTH(test_date) = 1 THEN 'PASS' ELSE 'FAIL' END AS status
FROM date_test_cases WHERE test_id = 1;

-- Test day extraction
-- MySQL:
SELECT 'Test 3.3: Extract Day' AS test,
       DAY(test_date) AS result,
       1 AS expected,
       CASE WHEN DAY(test_date) = 1 THEN 'PASS' ELSE 'FAIL' END AS status
FROM date_test_cases WHERE test_id = 1;

-- ============================================================================
-- TEST 4: Date Differences
-- ============================================================================

-- Test days between dates
-- MySQL:
SELECT 'Test 4.1: Days Between' AS test,
       DATEDIFF('2024-01-15', '2024-01-01') AS result,
       14 AS expected,
       CASE WHEN DATEDIFF('2024-01-15', '2024-01-01') = 14 THEN 'PASS' ELSE 'FAIL' END AS status;

-- Test age calculation
-- MySQL:
SELECT 'Test 4.2: Age Calculation' AS test,
       TIMESTAMPDIFF(YEAR, '1990-05-15', CURDATE()) AS result,
       CASE WHEN TIMESTAMPDIFF(YEAR, '1990-05-15', CURDATE()) >= 30 THEN 'PASS' ELSE 'FAIL' END AS status;

-- ============================================================================
-- TEST 5: First/Last Day Calculations
-- ============================================================================

-- Test first day of month
-- MySQL:
SELECT 'Test 5.1: First Day of Month' AS test,
       DATE_FORMAT(test_date, '%Y-%m-01') AS result,
       '2024-01-01' AS expected,
       CASE WHEN DATE_FORMAT(test_date, '%Y-%m-01') = '2024-01-01' THEN 'PASS' ELSE 'FAIL' END AS status
FROM date_test_cases WHERE test_id = 1;

-- Test last day of month
-- MySQL:
SELECT 'Test 5.2: Last Day of Month' AS test,
       LAST_DAY(test_date) AS result,
       '2024-01-31' AS expected,
       CASE WHEN LAST_DAY(test_date) = '2024-01-31' THEN 'PASS' ELSE 'FAIL' END AS status
FROM date_test_cases WHERE test_id = 1;

-- ============================================================================
-- TEST 6: Leap Year Detection
-- ============================================================================

-- Test leap year (2024)
-- MySQL:
SELECT 'Test 6.1: Leap Year 2024' AS test,
       CASE WHEN (2024 % 4 = 0 AND 2024 % 100 != 0) OR (2024 % 400 = 0) THEN 'YES' ELSE 'NO' END AS result,
       'YES' AS expected,
       CASE WHEN (2024 % 4 = 0 AND 2024 % 100 != 0) OR (2024 % 400 = 0) THEN 'PASS' ELSE 'FAIL' END AS status;

-- Test non-leap year (2023)
-- MySQL:
SELECT 'Test 6.2: Non-Leap Year 2023' AS test,
       CASE WHEN (2023 % 4 = 0 AND 2023 % 100 != 0) OR (2023 % 400 = 0) THEN 'YES' ELSE 'NO' END AS result,
       'NO' AS expected,
       CASE WHEN NOT ((2023 % 4 = 0 AND 2023 % 100 != 0) OR (2023 % 400 = 0)) THEN 'PASS' ELSE 'FAIL' END AS status;

-- ============================================================================
-- TEST 7: Weekend/Weekday Detection
-- ============================================================================

-- Test weekend detection
-- MySQL:
SELECT 'Test 7.1: Weekend Detection' AS test,
       DAYOFWEEK('2024-01-07') AS day_of_week,
       CASE WHEN DAYOFWEEK('2024-01-07') IN (1, 7) THEN 'WEEKEND' ELSE 'WEEKDAY' END AS result,
       'WEEKEND' AS expected,
       CASE WHEN DAYOFWEEK('2024-01-07') IN (1, 7) THEN 'PASS' ELSE 'FAIL' END AS status;

-- Test weekday detection
-- MySQL:
SELECT 'Test 7.2: Weekday Detection' AS test,
       DAYOFWEEK('2024-01-08') AS day_of_week,
       CASE WHEN DAYOFWEEK('2024-01-08') BETWEEN 2 AND 6 THEN 'WEEKDAY' ELSE 'WEEKEND' END AS result,
       'WEEKDAY' AS expected,
       CASE WHEN DAYOFWEEK('2024-01-08') BETWEEN 2 AND 6 THEN 'PASS' ELSE 'FAIL' END AS status;

-- ============================================================================
-- TEST 8: Quarter Calculations
-- ============================================================================

-- Test quarter extraction
-- MySQL:
SELECT 'Test 8.1: Quarter Q1' AS test,
       QUARTER('2024-01-15') AS result,
       1 AS expected,
       CASE WHEN QUARTER('2024-01-15') = 1 THEN 'PASS' ELSE 'FAIL' END AS status;

-- MySQL:
SELECT 'Test 8.2: Quarter Q2' AS test,
       QUARTER('2024-04-15') AS result,
       2 AS expected,
       CASE WHEN QUARTER('2024-04-15') = 2 THEN 'PASS' ELSE 'FAIL' END AS status;

-- MySQL:
SELECT 'Test 8.3: Quarter Q3' AS test,
       QUARTER('2024-07-15') AS result,
       3 AS expected,
       CASE WHEN QUARTER('2024-07-15') = 3 THEN 'PASS' ELSE 'FAIL' END AS status;

-- MySQL:
SELECT 'Test 8.4: Quarter Q4' AS test,
       QUARTER('2024-10-15') AS result,
       4 AS expected,
       CASE WHEN QUARTER('2024-10-15') = 4 THEN 'PASS' ELSE 'FAIL' END AS status;

-- ============================================================================
-- TEST 9: Week Number Calculations
-- ============================================================================

-- Test week number
-- MySQL:
SELECT 'Test 9.1: Week Number' AS test,
       WEEK('2024-01-15') AS result,
       CASE WHEN WEEK('2024-01-15') > 0 THEN 'PASS' ELSE 'FAIL' END AS status;

-- ============================================================================
-- TEST 10: Date Parsing
-- ============================================================================

-- Test date parsing
-- MySQL:
SELECT 'Test 10.1: Parse ISO Date' AS test,
       STR_TO_DATE('2024-01-15', '%Y-%m-%d') AS result,
       '2024-01-15' AS expected,
       CASE WHEN STR_TO_DATE('2024-01-15', '%Y-%m-%d') = '2024-01-15' THEN 'PASS' ELSE 'FAIL' END AS status;

-- MySQL:
SELECT 'Test 10.2: Parse UK Date' AS test,
       STR_TO_DATE('15/01/2024', '%d/%m/%Y') AS result,
       '2024-01-15' AS expected,
       CASE WHEN STR_TO_DATE('15/01/2024', '%d/%m/%Y') = '2024-01-15' THEN 'PASS' ELSE 'FAIL' END AS status;

-- MySQL:
SELECT 'Test 10.3: Parse US Date' AS test,
       STR_TO_DATE('01/15/2024', '%m/%d/%Y') AS result,
       '2024-01-15' AS expected,
       CASE WHEN STR_TO_DATE('01/15/2024', '%m/%d/%Y') = '2024-01-15' THEN 'PASS' ELSE 'FAIL' END AS status;

-- ============================================================================
-- TEST CLEANUP
-- ============================================================================

-- Drop test table
-- DROP TABLE IF EXISTS date_test_cases;

-- ============================================================================
-- TEST SUMMARY
-- ============================================================================

-- Run all tests and count results
-- MySQL:
SELECT 'All tests completed' AS message;

-- ============================================================================
-- END OF TEST SUITE
-- ============================================================================