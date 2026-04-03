-- ============================================================================
-- SQL Date/Time Utilities Module
-- ============================================================================
-- A comprehensive collection of date and time utility functions for SQL databases.
-- Supports MySQL, PostgreSQL, SQL Server, and SQLite with portable syntax.
--
-- Features:
--   - Date formatting and parsing
--   - Date arithmetic (add/subtract days, months, years)
--   - Date difference calculations
--   - Age calculation
--   - Quarter, week, and period calculations
--   - Business day calculations
--   - Date validation
--
-- Usage:
--   Copy individual query patterns for your specific database.
--   Each section includes database-specific implementations.
--
-- Author: AllToolkit
-- License: MIT
-- ============================================================================

-- ============================================================================
-- SECTION 1: DATE FORMATTING
-- ============================================================================

-- Format date to ISO 8601 (YYYY-MM-DD)
-- MySQL:     DATE_FORMAT(date_col, '%Y-%m-%d')
-- PostgreSQL: TO_CHAR(date_col, 'YYYY-MM-DD')
-- SQL Server: CONVERT(VARCHAR(10), date_col, 23)
-- SQLite:    strftime('%Y-%m-%d', date_col)

-- Format datetime to ISO 8601 (YYYY-MM-DD HH:MM:SS)
-- MySQL:     DATE_FORMAT(datetime_col, '%Y-%m-%d %H:%i:%s')
-- PostgreSQL: TO_CHAR(datetime_col, 'YYYY-MM-DD HH24:MI:SS')
-- SQL Server: CONVERT(VARCHAR(19), datetime_col, 120)
-- SQLite:    strftime('%Y-%m-%d %H:%M:%S', datetime_col)

-- Format to common patterns
-- Pattern: YYYY-MM-DD
-- MySQL:     DATE_FORMAT(date_col, '%Y-%m-%d')
-- PostgreSQL: TO_CHAR(date_col, 'YYYY-MM-DD')
-- SQL Server: FORMAT(date_col, 'yyyy-MM-dd')
-- SQLite:    strftime('%Y-%m-%d', date_col)

-- Pattern: DD/MM/YYYY
-- MySQL:     DATE_FORMAT(date_col, '%d/%m/%Y')
-- PostgreSQL: TO_CHAR(date_col, 'DD/MM/YYYY')
-- SQL Server: FORMAT(date_col, 'dd/MM/yyyy')
-- SQLite:    strftime('%d/%m/%Y', date_col)

-- Pattern: MM/DD/YYYY
-- MySQL:     DATE_FORMAT(date_col, '%m/%d/%Y')
-- PostgreSQL: TO_CHAR(date_col, 'MM/DD/YYYY')
-- SQL Server: FORMAT(date_col, 'MM/dd/yyyy')
-- SQLite:    strftime('%m/%d/%Y', date_col)

-- Pattern: YYYY年MM月DD日 (Chinese)
-- MySQL:     DATE_FORMAT(date_col, '%Y年%m月%d日')
-- PostgreSQL: TO_CHAR(date_col, 'YYYY"年"MM"月"DD"日"')
-- SQL Server: FORMAT(date_col, 'yyyy年MM月dd日')
-- SQLite:    strftime('%Y年%m月%d日', date_col)

-- ============================================================================
-- SECTION 2: DATE PARSING
-- ============================================================================

-- Parse string to date
-- MySQL:     STR_TO_DATE('2024-01-15', '%Y-%m-%d')
-- PostgreSQL: TO_DATE('2024-01-15', 'YYYY-MM-DD')
-- SQL Server: CONVERT(DATE, '2024-01-15', 23)
-- SQLite:    date('2024-01-15')

-- Parse various formats
-- Format: '15/01/2024'
-- MySQL:     STR_TO_DATE('15/01/2024', '%d/%m/%Y')
-- PostgreSQL: TO_DATE('15/01/2024', 'DD/MM/YYYY')
-- SQL Server: CONVERT(DATE, '15/01/2024', 103)
-- SQLite:    date('15/01/2024')

-- Format: '01/15/2024'
-- MySQL:     STR_TO_DATE('01/15/2024', '%m/%d/%Y')
-- PostgreSQL: TO_DATE('01/15/2024', 'MM/DD/YYYY')
-- SQL Server: CONVERT(DATE, '01/15/2024', 101)
-- SQLite:    date('01/15/2024')

-- ============================================================================
-- SECTION 3: DATE ARITHMETIC
-- ============================================================================

-- Add days to date
-- MySQL:     DATE_ADD(date_col, INTERVAL 7 DAY)
-- PostgreSQL: date_col + INTERVAL '7 days'
-- SQL Server: DATEADD(DAY, 7, date_col)
-- SQLite:    date(date_col, '+7 days')

-- Subtract days from date
-- MySQL:     DATE_SUB(date_col, INTERVAL 7 DAY)
-- PostgreSQL: date_col - INTERVAL '7 days'
-- SQL Server: DATEADD(DAY, -7, date_col)
-- SQLite:    date(date_col, '-7 days')

-- Add months to date
-- MySQL:     DATE_ADD(date_col, INTERVAL 3 MONTH)
-- PostgreSQL: date_col + INTERVAL '3 months'
-- SQL Server: DATEADD(MONTH, 3, date_col)
-- SQLite:    date(date_col, '+3 months')

-- Add years to date
-- MySQL:     DATE_ADD(date_col, INTERVAL 1 YEAR)
-- PostgreSQL: date_col + INTERVAL '1 year'
-- SQL Server: DATEADD(YEAR, 1, date_col)
-- SQLite:    date(date_col, '+1 year')

-- First day of month
-- MySQL:     DATE_FORMAT(date_col, '%Y-%m-01')
-- PostgreSQL: DATE_TRUNC('month', date_col)::DATE
-- SQL Server: DATEFROMPARTS(YEAR(date_col), MONTH(date_col), 1)
-- SQLite:    date(date_col, 'start of month')

-- Last day of month
-- MySQL:     LAST_DAY(date_col)
-- PostgreSQL: (DATE_TRUNC('month', date_col) + INTERVAL '1 month' - INTERVAL '1 day')::DATE
-- SQL Server: EOMONTH(date_col)
-- SQLite:    date(date_col, 'start of month', '+1 month', '-1 day')

-- First day of year
-- MySQL:     DATE_FORMAT(date_col, '%Y-01-01')
-- PostgreSQL: DATE_TRUNC('year', date_col)::DATE
-- SQL Server: DATEFROMPARTS(YEAR(date_col), 1, 1)
-- SQLite:    date(date_col, 'start of year')

-- Last day of year
-- MySQL:     DATE_FORMAT(date_col, '%Y-12-31')
-- PostgreSQL: (DATE_TRUNC('year', date_col) + INTERVAL '1 year' - INTERVAL '1 day')::DATE
-- SQL Server: DATEFROMPARTS(YEAR(date_col), 12, 31)
-- SQLite:    date(date_col, 'start of year', '+1 year', '-1 day')

-- ============================================================================
-- SECTION 4: DATE DIFFERENCES
-- ============================================================================

-- Days between two dates
-- MySQL:     DATEDIFF(date1, date2)
-- PostgreSQL: date1 - date2
-- SQL Server: DATEDIFF(DAY, date2, date1)
-- SQLite:    julianday(date1) - julianday(date2)

-- Months between two dates
-- MySQL:     TIMESTAMPDIFF(MONTH, date2, date1)
-- PostgreSQL: EXTRACT(YEAR FROM AGE(date1, date2)) * 12 + EXTRACT(MONTH FROM AGE(date1, date2))
-- SQL Server: DATEDIFF(MONTH, date2, date1)
-- SQLite:    (strftime('%Y', date1) - strftime('%Y', date2)) * 12 + (strftime('%m', date1) - strftime('%m', date2))

-- Years between two dates
-- MySQL:     TIMESTAMPDIFF(YEAR, date2, date1)
-- PostgreSQL: EXTRACT(YEAR FROM AGE(date1, date2))
-- SQL Server: DATEDIFF(YEAR, date2, date1)
-- SQLite:    strftime('%Y', date1) - strftime('%Y', date2)

-- Age calculation (in years)
-- MySQL:     TIMESTAMPDIFF(YEAR, birth_date, CURDATE())
-- PostgreSQL: EXTRACT(YEAR FROM AGE(CURRENT_DATE, birth_date))
-- SQL Server: DATEDIFF(YEAR, birth_date, GETDATE())
-- SQLite:    CAST((julianday('now') - julianday(birth_date)) / 365.25 AS INTEGER)

-- ============================================================================
-- SECTION 5: DATE EXTRACTION
-- ============================================================================

-- Extract year
-- MySQL:     YEAR(date_col)
-- PostgreSQL: EXTRACT(YEAR FROM date_col)
-- SQL Server: YEAR(date_col)
-- SQLite:    strftime('%Y', date_col)

-- Extract month
-- MySQL:     MONTH(date_col)
-- PostgreSQL: EXTRACT(MONTH FROM date_col)
-- SQL Server: MONTH(date_col)
-- SQLite:    strftime('%m', date_col)

-- Extract day
-- MySQL:     DAY(date_col)
-- PostgreSQL: EXTRACT(DAY FROM date_col)
-- SQL Server: DAY(date_col)
-- SQLite:    strftime('%d', date_col)

-- Extract day of week (1=Sunday in MySQL)
-- MySQL:     DAYOFWEEK(date_col)  -- 1=Sunday, 7=Saturday
-- PostgreSQL: EXTRACT(DOW FROM date_col) + 1  -- 1=Sunday, 7=Saturday
-- SQL Server: DATEPART(WEEKDAY, date_col)
-- SQLite:    CAST(strftime('%w', date_col) AS INTEGER) + 1

-- Extract day of year
-- MySQL:     DAYOFYEAR(date_col)
-- PostgreSQL: EXTRACT(DOY FROM date_col)
-- SQL Server: DATEPART(DAYOFYEAR, date_col)
-- SQLite:    strftime('%j', date_col)

-- Extract week number
-- MySQL:     WEEK(date_col)
-- PostgreSQL: EXTRACT(WEEK FROM date_col)
-- SQL Server: DATEPART(WEEK, date_col)
-- SQLite:    strftime('%W', date_col)

-- Extract quarter
-- MySQL:     QUARTER(date_col)
-- PostgreSQL: EXTRACT(QUARTER FROM date_col)
-- SQL Server: DATEPART(QUARTER, date_col)
-- SQLite:    (strftime('%m', date_col) + 2) / 3

-- Extract hour
-- MySQL:     HOUR(datetime_col)
-- PostgreSQL: EXTRACT(HOUR FROM datetime_col)
-- SQL Server: DATEPART(HOUR, datetime_col)
-- SQLite:    strftime('%H', datetime_col)

-- Extract minute
-- MySQL:     MINUTE(datetime_col)
-- PostgreSQL: EXTRACT(MINUTE FROM datetime_col)
-- SQL Server: DATEPART(MINUTE, datetime_col)
-- SQLite:    strftime('%M', datetime_col)

-- Extract second
-- MySQL:     SECOND(datetime_col)
-- PostgreSQL: EXTRACT(SECOND FROM datetime_col)
-- SQL Server: DATEPART(SECOND, datetime_col)
-- SQLite:    strftime('%S', datetime_col)

-- ============================================================================
-- SECTION 6: DATE VALIDATION
-- ============================================================================

-- Check if date is valid
-- MySQL:     Check if STR_TO_DATE returns NULL
-- PostgreSQL: Use ISFINITE() or check for valid date
-- SQL Server: Use ISDATE()
-- SQLite:    Use date() function and check for NULL

-- Check if year is leap year
-- MySQL:     (YEAR(date_col) % 4 = 0 AND YEAR(date_col) % 100 != 0) OR (YEAR(date_col) % 400 = 0)
-- PostgreSQL: EXTRACT(YEAR FROM date_col) % 4 = 0 AND (EXTRACT(YEAR FROM date_col) % 100 != 0 OR EXTRACT(YEAR FROM date_col) % 400 = 0)
-- SQL Server: (YEAR(date_col) % 4 = 0 AND YEAR(date_col) % 100 != 0) OR (YEAR(date_col) % 400 = 0)
-- SQLite:    (CAST(strftime('%Y', date_col) AS INTEGER) % 4 = 0 AND CAST(strftime('%Y', date_col) AS INTEGER) % 100 != 0) OR (CAST(strftime('%Y', date_col) AS INTEGER) % 400 = 0)

-- Check if date is weekend
-- MySQL:     DAYOFWEEK(date_col) IN (1, 7)
-- PostgreSQL: EXTRACT(DOW FROM date_col) IN (0, 6)
-- SQL Server: DATEPART(WEEKDAY, date_col) IN (1, 7)
-- SQLite:    CAST(strftime('%w', date_col) AS INTEGER) IN (0, 6)

-- Check if date is weekday
-- MySQL:     DAYOFWEEK(date_col) BETWEEN 2 AND 6
-- PostgreSQL: EXTRACT(DOW FROM date_col) BETWEEN 1 AND 5
-- SQL Server: DATEPART(WEEKDAY, date_col) BETWEEN 2 AND 6
-- SQLite:    CAST(strftime('%w', date_col) AS INTEGER) BETWEEN 1 AND 5

-- ============================================================================
-- SECTION 7: CURRENT DATE/TIME
-- ============================================================================

-- Current date
-- MySQL:     CURDATE() or CURRENT_DATE
-- PostgreSQL: CURRENT_DATE
-- SQL Server: CAST(GETDATE() AS DATE)
-- SQLite:    date('now')

-- Current datetime
-- MySQL:     NOW() or CURRENT_TIMESTAMP
-- PostgreSQL: CURRENT_TIMESTAMP
-- SQL Server: GETDATE()
-- SQLite:    datetime('now')

-- Current time
-- MySQL:     CURTIME() or CURRENT_TIME
-- PostgreSQL: CURRENT_TIME
-- SQL Server: CAST(GETDATE() AS TIME)
-- SQLite:    time('now')

-- Current timestamp (Unix)
-- MySQL:     UNIX_TIMESTAMP()
-- PostgreSQL: EXTRACT(EPOCH FROM CURRENT_TIMESTAMP)
-- SQL Server: DATEDIFF(SECOND, '1970-01-01', GETDATE())
-- SQLite:    strftime('%s', 'now')

-- ============================================================================
-- SECTION 8: PRACTICAL EXAMPLES
-- ============================================================================

-- Example 1: Calculate age from birth date
-- MySQL:
--   SELECT TIMESTAMPDIFF(YEAR, birth_date, CURDATE()) AS age FROM users;
-- PostgreSQL:
--   SELECT EXTRACT(YEAR FROM AGE(CURRENT_DATE, birth_date)) AS age FROM users;
-- SQL Server:
--   SELECT DATEDIFF(YEAR, birth_date, GETDATE()) AS age FROM users;
-- SQLite:
--   SELECT CAST((julianday('now') - julianday(birth_date)) / 365.25 AS INTEGER) AS age FROM users;

-- Example 2: Get records from last 7 days
-- MySQL:
--   SELECT * FROM orders WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY);
-- PostgreSQL:
--   SELECT * FROM orders WHERE order_date >= CURRENT_DATE - INTERVAL '7 days';
-- SQL Server:
--   SELECT * FROM orders WHERE order_date >= DATEADD(DAY, -7, GETDATE());
-- SQLite:
--   SELECT * FROM orders WHERE order_date >= date('now', '-7 days');

-- Example 3: Get records from current month
-- MySQL:
--   SELECT * FROM orders WHERE order_date >= DATE_FORMAT(CURDATE(), '%Y-%m-01');
-- PostgreSQL:
--   SELECT * FROM orders WHERE order_date >= DATE_TRUNC('month', CURRENT_DATE);
-- SQL Server:
--   SELECT * FROM orders WHERE order_date >= DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1);
-- SQLite:
--   SELECT * FROM orders WHERE order_date >= date('now', 'start of month');

-- Example 4: Format date for display
-- MySQL:
--   SELECT DATE_FORMAT(order_date, '%d/%m/%Y') AS formatted_date FROM orders;
-- PostgreSQL:
--   SELECT TO_CHAR(order_date, 'DD/MM/YYYY') AS formatted_date FROM orders;
-- SQL Server:
--   SELECT FORMAT(order_date, 'dd/MM/yyyy') AS formatted_date FROM orders;
-- SQLite:
--   SELECT strftime('%d/%m/%Y', order_date) AS formatted_date FROM orders;

-- Example 5: Group by year and month
-- MySQL:
--   SELECT DATE_FORMAT(order_date, '%Y-%m') AS month, COUNT(*) FROM orders GROUP BY month;
-- PostgreSQL:
--   SELECT TO_CHAR(order_date, 'YYYY-MM') AS month, COUNT(*) FROM orders GROUP BY month;
-- SQL Server:
--   SELECT FORMAT(order_date, 'yyyy-MM') AS month, COUNT(*) FROM orders GROUP BY month;
-- SQLite:
--   SELECT strftime('%Y-%m', order_date) AS month, COUNT(*) FROM orders GROUP BY month;

-- Example 6: Find records between two dates
-- MySQL:
--   SELECT * FROM orders WHERE order_date BETWEEN '2024-01-01' AND '2024-01-31';
-- PostgreSQL:
--   SELECT * FROM orders WHERE order_date BETWEEN '2024-01-01' AND '2024-01-31';
-- SQL Server:
--   SELECT * FROM orders WHERE order_date BETWEEN '2024-01-01' AND '2024-01-31';
-- SQLite:
--   SELECT * FROM orders WHERE order_date BETWEEN '2024-01-01' AND '2024-01-31';

-- Example 7: Calculate days until next birthday
-- MySQL:
--   SELECT DATEDIFF(
--     DATE_ADD(birth_date, INTERVAL TIMESTAMPDIFF(YEAR, birth_date, CURDATE()) + 1 YEAR),
--     CURDATE()
--   ) AS days_until_birthday FROM users;
-- PostgreSQL:
--   SELECT (DATE_TRUNC('year', CURRENT_DATE) + INTERVAL '1 year' + (birth_date - DATE_TRUNC('year', birth_date)) - CURRENT_DATE)::INT
--   AS days_until_birthday FROM users;
-- SQL Server:
--   SELECT DATEDIFF(DAY, GETDATE(), DATEADD(YEAR, DATEDIFF(YEAR, birth_date, GETDATE()) + 1, birth_date))
--   AS days_until_birthday FROM users;
-- SQLite:
--   SELECT CAST(julianday(date(strftime('%Y', 'now') || substr(birth_date, 5), '+1 year')) - julianday('now') AS INTEGER)
--   AS days_until_birthday FROM users;

-- ============================================================================
-- SECTION 9: DATE FORMAT REFERENCE
-- ============================================================================

-- MySQL DATE_FORMAT specifiers:
--   %Y = Year (4 digits)
--   %y = Year (2 digits)
--   %m = Month (01-12)
--   %c = Month (1-12)
--   %M = Month name (January-December)
--   %b = Abbreviated month name (Jan-Dec)
--   %d = Day of month (01-31)
--   %e = Day of month (1-31)
--   %D = Day with suffix (1st, 2nd, etc.)
--   %W = Weekday name (Sunday-Saturday)
--   %a = Abbreviated weekday name (Sun-Sat)
--   %H = Hour (00-23)
--   %h = Hour (01-12)
--   %i = Minutes (00-59)
--   %s = Seconds (00-59)
--   %p = AM/PM

-- PostgreSQL TO_CHAR format patterns:
--   YYYY = Year (4 digits)
--   YY = Year (2 digits)
--   MM = Month (01-12)
--   Mon = Abbreviated month name
--   Month = Full month name
--   DD = Day (01-31)
--   Day = Full weekday name
--   Dy = Abbreviated weekday name
--   HH24 = Hour (00-23)
--   HH12 = Hour (01-12)
--   MI = Minutes (00-59)
--   SS = Seconds (00-59)
--   AM/PM = Meridian indicator

-- SQL Server FORMAT patterns:
--   yyyy = Year (4 digits)
--   yy = Year (2 digits)
--   MM = Month (01-12)
--   MMM = Abbreviated month name
--   dd = Day (01-31)
--   ddd = Abbreviated weekday name
--   dddd = Full weekday name
--   HH = Hour (00-23)
--   hh = Hour (01-12)
--   mm = Minutes (00-59)
--   ss = Seconds (00-59)
--   tt = AM/PM

-- SQLite strftime specifiers:
--   %Y = Year (0000-9999)
--   %m = Month (01-12)
--   %d = Day (01-31)
--   %H = Hour (00-23)
--   %M = Minute (00-59)
--   %S = Second (00-59)
--   %j = Day of year (001-366)
--   %W = Week of year (00-53)
--   %w = Day of week (0-6, 0=Sunday)
--   %s = Unix timestamp

-- ============================================================================
-- SECTION 10: STORED PROCEDURE EXAMPLES
-- ============================================================================

-- MySQL stored procedure for date calculations
/*
DELIMITER //
CREATE PROCEDURE GetDateInfo(IN input_date DATE)
BEGIN
    SELECT
        input_date AS original_date,
        DATE_FORMAT(input_date, '%Y-%m-%d') AS iso_format,
        DATE_FORMAT(input_date, '%d/%m/%Y') AS uk_format,
        DATE_FORMAT(input_date, '%m/%d/%Y') AS us_format,
        YEAR(input_date) AS year,
        MONTH(input_date) AS month,
        DAY(input_date) AS day,
        DAYOFWEEK(input_date) AS day_of_week,
        DATE_FORMAT(input_date, '%Y-%m-01') AS first_day_of_month,
        LAST_DAY(input_date) AS last_day_of_month,
        DATE_ADD(input_date, INTERVAL 1 MONTH) AS next_month,
        DATE_SUB(input_date, INTERVAL 1 MONTH) AS prev_month;
END //
DELIMITER ;
*/

-- PostgreSQL function for date calculations
/*
CREATE OR REPLACE FUNCTION get_date_info(input_date DATE)
RETURNS TABLE (
    original_date DATE,
    iso_format TEXT,
    uk_format TEXT,
    us_format TEXT,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    day_of_week INTEGER,
    first_day_of_month DATE,
    last_day_of_month DATE,
    next_month DATE,
    prev_month DATE
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        input_date,
        TO_CHAR(input_date, 'YYYY-MM-DD'),
        TO_CHAR(input_date, 'DD/MM/YYYY'),
        TO_CHAR(input_date, 'MM/DD/YYYY'),
        EXTRACT(YEAR FROM input_date)::INTEGER,
        EXTRACT(MONTH FROM input_date)::INTEGER,
        EXTRACT(DAY FROM input_date)::INTEGER,
        EXTRACT(DOW FROM input_date)::INTEGER + 1,
        DATE_TRUNC('month', input_date)::DATE,
        (DATE_TRUNC('month', input_date) + INTERVAL '1 month' - INTERVAL '1 day')::DATE,
        (input_date + INTERVAL '1 month')::DATE,
        (input_date - INTERVAL '1 month')::DATE;
END;
$$ LANGUAGE plpgsql;
*/

-- SQL Server stored procedure for date calculations
/*
CREATE PROCEDURE GetDateInfo
    @input_date DATE
AS
BEGIN
    SELECT
        @input_date AS original_date,
        CONVERT(VARCHAR(10), @input_date, 23) AS iso_format,
        FORMAT(@input_date, 'dd/MM/yyyy') AS uk_format,
        FORMAT(@input_date, 'MM/dd/yyyy') AS us_format,
        YEAR(@input_date) AS year,
        MONTH(@input_date) AS month,
        DAY(@input_date) AS day,
        DATEPART(WEEKDAY, @input_date) AS day_of_week,
        DATEFROMPARTS(YEAR(@input_date), MONTH(@input_date), 1) AS first_day_of_month,
        EOMONTH(@input_date) AS last_day_of_month,
        DATEADD(MONTH, 1, @input_date) AS next_month,
        DATEADD(MONTH, -1, @input_date) AS prev_month;
END;
*/

-- ============================================================================
-- END OF MODULE
-- ============================================================================