-- ============================================================================
-- SQL String Utilities - Usage Examples
-- ============================================================================
-- This file demonstrates how to use the string utility functions across
-- different SQL database systems.
--
-- Copy and run the examples for your specific database.
-- ============================================================================

-- ============================================================================
-- EXAMPLE 1: Case Conversion
-- ============================================================================

-- Convert to uppercase
SELECT UPPER('hello world');  -- Result: 'HELLO WORLD'

-- Convert to lowercase
SELECT LOWER('HELLO WORLD');  -- Result: 'hello world'

-- Capitalize first letter only (MySQL)
SELECT CONCAT(UPPER(LEFT('hello', 1)), LOWER(SUBSTRING('hello', 2)));
-- Result: 'Hello'

-- Title Case (PostgreSQL)
SELECT INITCAP('hello world');  -- Result: 'Hello World'

-- ============================================================================
-- EXAMPLE 2: String Trimming
-- ============================================================================

-- Remove leading and trailing whitespace
SELECT TRIM('  hello world  ');  -- Result: 'hello world'

-- Remove leading whitespace only
SELECT LTRIM('  hello world  ');  -- Result: 'hello world  '

-- Remove trailing whitespace only
SELECT RTRIM('  hello world  ');  -- Result: '  hello world'

-- Remove specific characters from both ends
SELECT TRIM(BOTH 'x' FROM 'xxxhelloxxx');  -- Result: 'hello'

-- ============================================================================
-- EXAMPLE 3: String Padding
-- ============================================================================

-- Left pad with zeros (MySQL/PostgreSQL)
SELECT LPAD('5', 3, '0');  -- Result: '005'
SELECT LPAD('42', 5, '0'); -- Result: '00042'

-- Right pad with spaces (MySQL/PostgreSQL)
SELECT RPAD('hi', 5, ' ');  -- Result: 'hi   '

-- Left pad (SQL Server)
SELECT RIGHT(REPLICATE('0', 3) + '5', 3);  -- Result: '005'

-- Right pad (SQL Server)
SELECT LEFT('5' + REPLICATE('0', 3), 3);   -- Result: '500'

-- ============================================================================
-- EXAMPLE 4: Substring Extraction
-- ============================================================================

-- Extract leftmost characters
SELECT LEFT('hello world', 5);  -- Result: 'hello'

-- Extract rightmost characters
SELECT RIGHT('hello world', 5);  -- Result: 'world'

-- Extract substring from position
SELECT SUBSTRING('hello world', 7, 5);  -- Result: 'world'

-- Extract substring (SQLite)
SELECT SUBSTR('hello world', 7, 5);  -- Result: 'world'

-- ============================================================================
-- EXAMPLE 5: String Searching
-- ============================================================================

-- Find position of substring (MySQL)
SELECT LOCATE('world', 'hello world');  -- Result: 7

-- Find position (PostgreSQL)
SELECT POSITION('world' IN 'hello world');  -- Result: 7

-- Find position (SQL Server)
SELECT CHARINDEX('world', 'hello world');  -- Result: 7

-- Find position (SQLite)
SELECT INSTR('hello world', 'world');  -- Result: 7

-- Check if string contains substring
SELECT LOCATE('world', 'hello world') > 0;  -- Result: TRUE

-- ============================================================================
-- EXAMPLE 6: String Replacement
-- ============================================================================

-- Replace all occurrences
SELECT REPLACE('hello world', 'world', 'SQL');  -- Result: 'hello SQL'

-- Remove all spaces
SELECT REPLACE('hello world', ' ', '');  -- Result: 'helloworld'

-- ============================================================================
-- EXAMPLE 7: String Validation
-- ============================================================================

-- Check if NULL or empty (MySQL)
SELECT col IS NULL OR col = '' FROM mytable;

-- Check if numeric (MySQL)
SELECT '12345' REGEXP '^[0-9]+$';  -- Result: TRUE
SELECT 'abc' REGEXP '^[0-9]+$';    -- Result: FALSE

-- Check if numeric (PostgreSQL)
SELECT '12345' ~ '^[0-9]+$';  -- Result: TRUE

-- Check if numeric (SQL Server)
SELECT '12345' NOT LIKE '%[^0-9]%';  -- Result: TRUE

-- Email validation (MySQL)
SELECT 'user@example.com' REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$';
-- Result: TRUE

-- Email validation (PostgreSQL)
SELECT 'user@example.com' ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$';
-- Result: TRUE

-- ============================================================================
-- EXAMPLE 8: String Reversal and Repetition
-- ============================================================================

-- Reverse string (MySQL/PostgreSQL)
SELECT REVERSE('hello');  -- Result: 'olleh'

-- Repeat string (MySQL/PostgreSQL)
SELECT REPEAT('ab', 3);   -- Result: 'ababab'

-- Repeat string (SQL Server)
SELECT REPLICATE('ab', 3);  -- Result: 'ababab'

-- ============================================================================
-- EXAMPLE 9: String Length
-- ============================================================================

-- Get string length
SELECT LENGTH('hello');  -- Result: 5 (MySQL/PostgreSQL/SQLite)
SELECT LEN('hello');     -- Result: 5 (SQL Server)

-- ============================================================================
-- EXAMPLE 10: Practical Use Cases
-- ============================================================================

-- Format phone number (add dashes)
SELECT CONCAT(
    LEFT('1234567890', 3), '-',
    SUBSTRING('1234567890', 4, 3), '-',
    RIGHT('1234567890', 4)
);
-- Result: '123-456-7890'

-- Format ID with leading zeros
SELECT LPAD(CAST(id AS CHAR), 6, '0') AS formatted_id FROM users;

-- Extract domain from email
SELECT SUBSTRING(email, LOCATE('@', email) + 1) AS domain FROM users;

-- Extract username from email
SELECT LEFT(email, LOCATE('@', email) - 1) AS username FROM users;

-- Mask sensitive data (show last 4 digits only)
SELECT CONCAT('****', RIGHT(credit_card, 4)) AS masked_card FROM payments;

-- Remove all non-numeric characters
-- MySQL: Use multiple REPLACE calls or REGEXP_REPLACE (8.0+)
SELECT REGEXP_REPLACE('(123) 456-7890', '[^0-9]', '');  -- Result: '1234567890'

-- ============================================================================
-- EXAMPLE 11: Using MySQL Stored Functions
-- ============================================================================

-- After creating the stored functions from mod.sql:

-- Capitalize a string
SELECT str_capitalize('hello world');  -- Result: 'Hello world'

-- Check if email is valid
SELECT str_is_email('user@example.com');  -- Result: TRUE
SELECT str_is_email('invalid-email');      -- Result: FALSE

-- Check if string is numeric
SELECT str_is_numeric('12345');  -- Result: TRUE
SELECT str_is_numeric('abc');    -- Result: FALSE

-- Check if NULL or empty
SELECT str_is_null_or_empty('');       -- Result: TRUE
SELECT str_is_null_or_empty(NULL);     -- Result: TRUE
SELECT str_is_null_or_empty('hello');  -- Result: FALSE

-- Check if string contains substring
SELECT str_contains('hello world', 'world');  -- Result: TRUE
SELECT str_contains('hello world', 'foo');    -- Result: FALSE

-- Extract left/right portions
SELECT str_left('hello world', 5);   -- Result: 'hello'
SELECT str_right('hello world', 5);  -- Result: 'world'

-- ============================================================================
-- EXAMPLE 12: Batch Update Examples
-- ============================================================================

-- Update: Trim all email addresses
UPDATE users SET email = TRIM(email);

-- Update: Convert all names to uppercase
UPDATE