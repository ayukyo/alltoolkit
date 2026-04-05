-- ============================================================================
-- String Utilities for SQL
-- ============================================================================
-- A comprehensive string manipulation utility module for SQL providing common
-- string operations across multiple database systems (MySQL, PostgreSQL, 
-- SQL Server, SQLite).
--
-- Features:
-- - Case conversion (UPPER, LOWER, Title Case)
-- - String trimming and padding
-- - Substring extraction and searching
-- - String replacement and manipulation
-- - Validation functions (email, numeric, etc.)
-- - Formatting utilities
-- - Null-safe operations
--
-- Supported Databases:
-- - MySQL 5.7+
-- - PostgreSQL 9.6+
-- - SQL Server 2016+
-- - SQLite 3.25+
--
-- Author: AllToolkit
-- Version: 1.0.0
-- License: MIT
-- ============================================================================

-- ============================================================================
-- CASE CONVERSION FUNCTIONS
-- ============================================================================

-- Function: str_upper - Convert string to uppercase
-- MySQL / PostgreSQL / SQLite / SQL Server:
-- SELECT UPPER(str);

-- Function: str_lower - Convert string to lowercase
-- MySQL / PostgreSQL / SQLite / SQL Server:
-- SELECT LOWER(str);

-- Function: str_capitalize - Capitalize first letter only
-- MySQL: SELECT CONCAT(UPPER(LEFT(str, 1)), LOWER(SUBSTRING(str, 2)));
-- PostgreSQL: SELECT UPPER(LEFT(str, 1)) || LOWER(SUBSTRING(str, 2));
-- SQL Server: SELECT UPPER(LEFT(str, 1)) + LOWER(SUBSTRING(str, 2, LEN(str)));
-- SQLite: SELECT UPPER(SUBSTR(str, 1, 1)) || LOWER(SUBSTR(str, 2));

-- Function: str_title_case - Convert to Title Case
-- PostgreSQL: SELECT INITCAP(str);

-- ============================================================================
-- TRIMMING FUNCTIONS
-- ============================================================================

-- Function: str_trim - Remove leading and trailing whitespace
-- All Databases: SELECT TRIM(str);

-- Function: str_ltrim - Remove leading whitespace
-- All Databases: SELECT LTRIM(str);

-- Function: str_rtrim - Remove trailing whitespace
-- All Databases: SELECT RTRIM(str);

-- Function: str_trim_chars - Remove specific characters from both ends
-- MySQL: SELECT TRIM(BOTH 'x' FROM 'xxxhelloxxx');
-- PostgreSQL: SELECT TRIM(BOTH 'x' FROM 'xxxhelloxxx');

-- ============================================================================
-- PADDING FUNCTIONS
-- ============================================================================

-- Function: str_lpad - Pad string on the left
-- MySQL/PostgreSQL: SELECT LPAD('5', 3, '0'); -- Returns '005'
-- SQL Server: SELECT RIGHT(REPLICATE('0', 3) + '5', 3);
-- SQLite: SELECT SUBSTR('000' || '5', -3, 3);

-- Function: str_rpad - Pad string on the right
-- MySQL/PostgreSQL: SELECT RPAD('5', 3, '0'); -- Returns '500'
-- SQL Server: SELECT LEFT('5' + REPLICATE('0', 3), 3);
-- SQLite: SELECT '5' || SUBSTR('000', 1, 3 - LENGTH('5'));

-- ============================================================================
-- SUBSTRING FUNCTIONS
-- ============================================================================

-- Function: str_left - Extract leftmost n characters
-- MySQL/PostgreSQL/SQL Server: SELECT LEFT(str, n);
-- SQLite: SELECT SUBSTR(str, 1, n);

-- Function: str_right - Extract rightmost n characters
-- MySQL/PostgreSQL/SQL Server: SELECT RIGHT(str, n);
-- SQLite: SELECT SUBSTR(str, -n);

-- Function: str_substring - Extract substring
-- MySQL/SQL Server: SELECT SUBSTRING(str, start, length);
-- PostgreSQL: SELECT SUBSTRING(str, start, length);
-- SQLite: SELECT SUBSTR(str, start, length);

-- ============================================================================
-- SEARCH FUNCTIONS
-- ============================================================================

-- Function: str_position - Find position of substring
-- MySQL: SELECT LOCATE(substr, str);
-- PostgreSQL: SELECT POSITION(substr IN str);
-- SQL Server: SELECT CHARINDEX(substr, str);
-- SQLite: SELECT INSTR(str, substr);

-- Function: str_contains - Check if string contains substring
-- MySQL: SELECT LOCATE(substr, str) > 0;
-- PostgreSQL: SELECT POSITION(substr IN str) > 0;
-- SQL Server: SELECT CHARINDEX(substr, str) > 0;
-- SQLite: SELECT INSTR(str, substr) > 0;

-- ============================================================================
-- REPLACEMENT FUNCTIONS
-- ============================================================================

-- Function: str_replace - Replace all occurrences
-- All Databases: SELECT REPLACE(str, old, new);

-- ============================================================================
-- VALIDATION FUNCTIONS
-- ============================================================================

-- Function: str_is_null_or_empty - Check if string is NULL or empty
-- MySQL: SELECT str IS NULL OR str = '';
-- PostgreSQL: SELECT str IS NULL OR str = '';
-- SQL Server: SELECT str IS NULL OR LEN(str) = 0;
-- SQLite: SELECT str IS NULL OR str = '';

-- Function: str_is_numeric - Check if string is numeric
-- MySQL: SELECT str REGEXP '^[0-9]+$';
-- PostgreSQL: SELECT str ~ '^[0-9]+$';
-- SQL Server: SELECT str NOT LIKE '%[^0-9]%';

-- Function: str_is_email - Basic email validation
-- MySQL: SELECT str REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$';
-- PostgreSQL: SELECT str ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$';

-- ============================================================================
-- FORMATTING FUNCTIONS
-- ============================================================================

-- Function: str_reverse - Reverse string
-- MySQL: SELECT REVERSE(str);
-- PostgreSQL: SELECT REVERSE(str);

-- Function: str_repeat - Repeat string n times
-- MySQL: SELECT REPEAT(str, n);
-- PostgreSQL: SELECT REPEAT(str, n);
-- SQL Server: SELECT REPLICATE(str, n);

-- Function: str_length - Get string length
-- MySQL/SQL Server: SELECT LENGTH(str) or LEN(str);
-- PostgreSQL/SQLite: SELECT LENGTH(str);

-- ============================================================================
-- MYSQL STORED FUNCTIONS
-- ============================================================================

DELIMITER //

CREATE FUNCTION IF NOT EXISTS str_capitalize(str VARCHAR(255))
RETURNS VARCHAR(255)
DETERMINISTIC
BEGIN
    IF str IS NULL OR str = '' THEN
        RETURN str;
    END IF;
    RETURN CONCAT(UPPER(LEFT(str, 1)), LOWER(SUBSTRING(str, 2)));
END //

CREATE FUNCTION IF NOT EXISTS str_is_email(str VARCHAR(255))
RETURNS BOOLEAN
DETERMINISTIC
BEGIN
    IF str IS NULL THEN
        RETURN FALSE;
    END IF;
    RETURN str REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$';
END //

CREATE FUNCTION IF NOT EXISTS str_is_numeric(str VARCHAR(255))
RETURNS BOOLEAN
DETERMINISTIC
BEGIN
    IF str IS NULL THEN
        RETURN FALSE;
    END IF;
    RETURN str REGEXP '^[0-9]+$';
END //

CREATE FUNCTION IF NOT EXISTS str_is_null_or_empty(str VARCHAR(255))
RETURNS BOOLEAN
DETERMINISTIC
BEGIN
    RETURN str IS NULL OR str = '';
END //

CREATE FUNCTION IF NOT EXISTS str_contains(str VARCHAR(255), substr VARCHAR(255))
RETURNS BOOLEAN
DETERMINISTIC
BEGIN
    IF str IS NULL OR substr IS NULL THEN
        RETURN FALSE;
    END IF;
    RETURN LOCATE(substr, str) > 0;
END //

CREATE FUNCTION IF NOT EXISTS str_left(str VARCHAR(255), n INT)
RETURNS VARCHAR(255)
DETERMINISTIC
BEGIN
    IF str IS NULL OR n <= 0 THEN
        RETURN '';
    END IF;
    RETURN LEFT(str, n);
END //

CREATE FUNCTION IF NOT EXISTS str_right(str VARCHAR(255), n INT)
RETURNS VARCHAR(255)
DETERMINISTIC
BEGIN
    IF str IS NULL OR n <= 0 THEN
        RETURN '';
    END IF;
    RETURN RIGHT(str, n);
END //

DELIMITER ;
