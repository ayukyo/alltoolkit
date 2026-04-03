-- ============================================================================
-- SQL Date/Time Utilities Example
-- ============================================================================
-- Practical examples demonstrating date_utils module usage
--
-- Author: AllToolkit
-- License: MIT
-- ============================================================================

-- ============================================================================
-- EXAMPLE 1: Create a Sample Table
-- ============================================================================

-- Create employees table with date columns
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    birth_date DATE,
    hire_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO employees (name, email, birth_date, hire_date) VALUES
('Alice Johnson', 'alice@example.com', '1990-05-15', '2020-03-01'),
('Bob Smith', 'bob@example.com', '1985-08-22', '2019-07-15'),
('Carol White', 'carol@example.com', '1992-11-30', '2021-01-10'),
('David Brown', 'david@example.com', '1988-03-08', '2018-11-20'),
('Eve Davis', 'eve@example.com', '1995-12-25', '2022-06-01');

-- ============================================================================
-- EXAMPLE 2: Format Dates for Display
-- ============================================================================

-- Format dates in different styles
SELECT
    name,
    -- ISO format (YYYY-MM-DD)
    DATE_FORMAT(birth_date, '%Y-%m-%d') AS birth_iso,
    -- UK format (DD/MM/YYYY)
    DATE_FORMAT(birth_date, '%d/%m/%Y') AS birth_uk,
    -- US format (MM/DD/YYYY)
    DATE_FORMAT(birth_date, '%m/%d/%Y') AS birth_us,
    -- Chinese format (YYYY年MM月DD日)
    DATE_FORMAT(birth_date, '%Y年%m月%d日') AS birth_cn,
    -- Full format (Monday, January 1, 2024)
    DATE_FORMAT(birth_date, '%W, %M %d, %Y') AS birth_full
FROM employees;

-- ============================================================================
-- EXAMPLE 3: Calculate Age
-- ============================================================================

-- Calculate age of employees
SELECT
    name,
    birth_date,
    TIMESTAMPDIFF(YEAR, birth_date, CURDATE()) AS age,
    CONCAT(
        TIMESTAMPDIFF(YEAR, birth_date, CURDATE()),
        ' years old'
    ) AS age_description
FROM employees
ORDER BY age DESC;

-- ============================================================================
-- EXAMPLE 4: Find Employees with Birthdays This Month
-- ============================================================================

-- Get employees with birthdays in the current month
SELECT
    name,
    birth_date,
    DATE_FORMAT(birth_date, '%m') AS birth_month,
    DATE_FORMAT(CURDATE(), '%m') AS current_month
FROM employees
WHERE MONTH(birth_date) = MONTH(CURDATE());

-- ============================================================================
-- EXAMPLE 5: Calculate Years of Service
-- ============================================================================

-- Calculate how long each employee has been with the company
SELECT
    name,
    hire_date,
    TIMESTAMPDIFF(YEAR, hire_date, CURDATE()) AS years_of_service,
    TIMESTAMPDIFF(MONTH, hire_date, CURDATE()) % 12 AS months_of_service,
    CONCAT(
        TIMESTAMPDIFF(YEAR, hire_date, CURDATE()),
        ' years, ',
        TIMESTAMPDIFF(MONTH, hire_date, CURDATE()) % 12,
        ' months'
    ) AS tenure
FROM employees
ORDER BY years_of_service DESC, months_of_service DESC;

-- ============================================================================
-- EXAMPLE 6: Group by Year/Month
-- ============================================================================

-- Count hires by year
SELECT
    YEAR(hire_date) AS hire_year,
    COUNT(*) AS total_hires
FROM employees
GROUP BY YEAR(hire_date)
ORDER BY hire_year;

-- Count hires by year and month
SELECT
    DATE_FORMAT(hire_date, '%Y-%m') AS hire_month,
    COUNT(*) AS total_hires
FROM employees
GROUP BY DATE_FORMAT(hire_date, '%Y-%m')
ORDER BY hire_month;

-- ============================================================================
-- EXAMPLE 7: Find Upcoming Birthdays
-- ============================================================================

-- Calculate days until next birthday
SELECT
    name,
    birth_date,
    DATE_FORMAT(birth_date, '%m-%d') AS birth_month_day,
    CASE
        WHEN DATE_FORMAT(CURDATE(), '%m%d') <= DATE_FORMAT(birth_date, '%m%d')
        THEN DATEDIFF(
            STR_TO_DATE(CONCAT(YEAR(CURDATE()), '-', DATE_FORMAT(birth_date, '%m-%d')), '%Y-%m-%d'),
            CURDATE()
        )
        ELSE DATEDIFF(
            STR_TO_DATE(CONCAT(YEAR(CURDATE()) + 1, '-', DATE_FORMAT(birth_date, '%m-%d')), '%Y-%m-%d'),
            CURDATE()
        )
    END AS days_until_birthday
FROM employees
ORDER BY days_until_birthday;

-- ============================================================================
-- EXAMPLE 8: Date Range Queries
-- ============================================================================

-- Find employees hired in the last 6 months
SELECT
    name,
    hire_date,
    DATE_FORMAT(hire_date, '%Y-%m-%d') AS formatted_hire_date
FROM employees
WHERE hire_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH);

-- Find employees hired in a specific quarter
SELECT
    name,
    hire_date,
    QUARTER(hire_date) AS hire_quarter
FROM employees
WHERE QUARTER(hire_date) = 1 AND YEAR(hire_date) = 2021;

-- ============================================================================
-- EXAMPLE 9: First and Last Day Calculations
-- ============================================================================

-- Get first and last day of current month
SELECT
    CURDATE() AS today,
    DATE_FORMAT(CURDATE(), '%Y-%m-01') AS first_day_of_month,
    LAST_DAY(CURDATE()) AS last_day_of_month;

-- Get first and last day of current year
SELECT
    CURDATE() AS today,
    DATE_FORMAT(CURDATE(), '%Y-01-01') AS first_day_of_year,
    DATE_FORMAT(CURDATE(), '%Y-12-31') AS last_day_of_year;

-- ============================================================================
-- EXAMPLE 10: Weekend and Weekday Detection
-- ============================================================================

-- Check if hire dates fall on weekends
SELECT
    name,
    hire_date,
    DAYNAME(hire_date) AS day_name,
    CASE
        WHEN DAYOFWEEK(hire_date) IN (1, 7) THEN 'Weekend'
        ELSE 'Weekday'
    END AS day_type
FROM employees;

-- ============================================================================
-- EXAMPLE 11: Date Arithmetic
-- ============================================================================

-- Calculate probation end date (90 days after hire)
SELECT
    name,
    hire_date,
    DATE_ADD(hire_date, INTERVAL 90 DAY) AS probation_end_date,
    DATEDIFF(DATE_ADD(hire_date, INTERVAL 90 DAY), CURDATE()) AS days_remaining
FROM employees
WHERE DATE_ADD(hire_date, INTERVAL 90 DAY) > CURDATE();

-- Calculate anniversary dates
SELECT
    name,
    hire_date,
    DATE_FORMAT(hire_date, '%Y-%m-%d') AS original_hire_date,
    CONCAT(
        YEAR(CURDATE()),
        DATE_FORMAT(hire_date, '-%m-%d')
    ) AS this_year_anniversary,
    CASE
        WHEN DATE_FORMAT(hire_date, '%m%d') >= DATE_FORMAT(CURDATE(), '%m%d')
        THEN YEAR(CURDATE())
        ELSE YEAR(CURDATE()) + 1
    END AS next_anniversary_year
FROM employees;

-- ============================================================================
-- EXAMPLE 12: Leap Year Handling
-- ============================================================================

-- Check for leap year birthdays (Feb 29)
SELECT
    name,
    birth_date,
    CASE
        WHEN MONTH(birth_date) = 2 AND DAY(birth_date) = 29 THEN 'Leap Day Baby'
        ELSE 'Regular Birthday'
    END AS birthday_type
FROM employees;

-- ============================================================================
-- EXAMPLE 13: Time Zone Handling (if supported)
-- ============================================================================

-- Convert to UTC (MySQL)
SELECT
    NOW() AS local_time,
    UTC_TIMESTAMP() AS utc_time;

-- ============================================================================
-- EXAMPLE 14: Date Validation
-- ============================================================================

-- Check if dates are valid
SELECT
    '2024-02-29' AS test_date,
    CASE
        WHEN STR_TO_DATE('2024-02-29', '%Y-%m-%d') IS NOT NULL THEN 'Valid'
        ELSE 'Invalid'
    END AS is_valid;

SELECT
    '2023-02-29' AS test_date,
    CASE
        WHEN STR_TO_DATE('2023-02-29', '%Y-%m-%d') IS NOT NULL THEN 'Valid'
        ELSE 'Invalid'
    END AS is_valid;

-- ============================================================================
-- EXAMPLE 15: Complex Date Report
-- ============================================================================

-- Generate a comprehensive employee date report
SELECT
    name,
    DATE_FORMAT(birth_date, '%Y-%m-%d') AS birth_date,
    TIMESTAMPDIFF(YEAR, birth_date, CURDATE()) AS age,
    DATE_FORMAT(hire_date, '%Y-%m-%d') AS hire_date,
    TIMESTAMPDIFF(YEAR, hire_date, CURDATE()) AS years_of_service,
    DATE_FORMAT(DATE_ADD(hire_date, INTERVAL 1 YEAR), '%Y-%m-%d') AS first_anniversary,
    QUARTER(hire_date) AS hire_quarter,
    MONTHNAME(hire_date) AS hire_month,
    DAYNAME(hire_date) AS hire_day_of_week,
    CASE
        WHEN DAYOFWEEK(hire_date) IN (1, 7) THEN 'Weekend Hire'
        ELSE 'Weekday Hire'
    END AS hire_day_type
FROM employees
ORDER BY hire_date;

-- ============================================================================
-- CLEANUP (uncomment to remove sample data)
-- ============================================================================

-- DROP TABLE IF EXISTS employees;

-- ============================================================================
-- END OF EXAMPLES
-- ============================================================================