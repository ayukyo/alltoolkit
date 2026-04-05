-- ============================================================================
-- SQL String Utilities - Test Suite
-- ============================================================================
-- Comprehensive test suite for string utility functions.
-- Run these tests to verify functionality on your database system.
--
-- Note: Some tests are database-specific and marked accordingly.
-- ============================================================================

-- ============================================================================
-- TEST SETUP
-- ============================================================================

-- Create test table
CREATE TABLE IF NOT EXISTS string_utils_tests (
    test_id INT AUTO_INCREMENT PRIMARY KEY,
    test_name VARCHAR(255),
    test_function VARCHAR(100),
    input_value VARCHAR(255),
    expected_result VARCHAR(255),
    actual_result VARCHAR(255),
    passed BOOLEAN,
    test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Clear previous test results
TRUNCATE TABLE string_utils_tests;

-- ============================================================================
-- HELPER PROCEDURE FOR RUNNING TESTS
-- ============================================================================

DELIMITER //

CREATE PROCEDURE IF NOT EXISTS run_string_test(
    IN test_name VARCHAR(255),
    IN test_function VARCHAR(100),
    IN input_val VARCHAR(255),
    IN expected VARCHAR(255),
    IN actual VARCHAR(255)
)
BEGIN
    INSERT INTO string_utils_tests (test_name, test_function, input_value, expected_result, actual_result, passed)
    VALUES (test_name, test_function, input_val, expected, actual, actual = expected);
END //

DELIMITER ;

-- ============================================================================
-- TEST 1: Case Conversion Functions
-- ============================================================================

-- Test UPPER function
CALL run_string_test(
    'UPPER converts lowercase to uppercase',
    'UPPER',
    'hello world',
    'HELLO WORLD',
    UPPER('hello world')
);

-- Test LOWER function
CALL run_string_test(
    'LOWER converts uppercase to lowercase',
    'LOWER',
    'HELLO WORLD',
    'hello world',
    LOWER('HELLO WORLD')
);

-- Test mixed case
CALL run_string_test(
    'UPPER handles mixed case',
    'UPPER',
    'Hello World',
    'HELLO WORLD',
    UPPER('Hello World')
);

-- ============================================================================
-- TEST 2: Trimming Functions
-- ============================================================================

-- Test TRIM function
CALL run_string_test(
    'TRIM removes leading and trailing spaces',
    'TRIM',
    '  hello world  ',
    'hello world',
    TRIM('  hello world  ')
);

-- Test LTRIM function
CALL run_string_test(
    'LTRIM removes leading spaces only',
    'LTRIM',
    '  hello world  ',
    'hello world  ',
    LTRIM('  hello world  ')
);

-- Test RTRIM function
CALL run_string_test(
    'RTRIM removes trailing spaces only',
    'RTRIM',
    '  hello world  ',
    '  hello world',
    RTRIM('  hello world  ')
);

-- Test TRIM with specific characters
CALL run_string_test(
    'TRIM removes specific characters from both ends',
    'TRIM',
    'xxxhelloxxx',
    'hello',
    TRIM(BOTH 'x' FROM 'xxxhelloxxx')
);

-- ============================================================================
-- TEST 3: Padding Functions
-- ============================================================================

-- Test LPAD function
CALL run_string_test(
    'LPAD left pads with zeros',
    'LPAD',
    '5',
    '005',
    LPAD('5', 3, '0')
);

-- Test LPAD with longer string
CALL run_string_test(
    'LPAD handles string longer than pad length',
    'LPAD',
    'hello',
    'hello',
    LPAD('hello', 3, '0')
);

-- Test RPAD function
CALL run_string_test(
    'RPAD right pads with spaces',
    'RPAD',
    'hi',
    'hi   ',
    RPAD('hi', 5, ' ')
);

-- ============================================================================
-- TEST 4: Substring Functions
-- ============================================================================

-- Test LEFT function
CALL run_string_test(
    'LEFT extracts leftmost characters',
    'LEFT',
    'hello world',
    'hello',
    LEFT('hello world', 5)
);

-- Test RIGHT function
CALL run_string_test(
    'RIGHT extracts rightmost characters',
    'RIGHT',
    'hello world',
    'world',
    RIGHT('hello world', 5)
);

-- Test SUBSTRING function
CALL run_string_test(
    'SUBSTRING extracts from position',
    'SUBSTRING',
    'hello world',
    'world',
    SUBSTRING('hello world', 7, 5)
);

-- ============================================================================
-- TEST 5: Search Functions
-- ============================================================================

-- Test LOCATE function
CALL run_string_test(
    'LOCATE finds substring position',
    'LOCATE',
    'world',
    '7',
    CAST(LOCATE('world', 'hello world') AS CHAR)
);

-- Test LOCATE not found
CALL run_string_test(
    'LOCATE returns 0 when not found',
    'LOCATE',
    'foo',
    '0',
    CAST(LOCATE('foo', 'hello world') AS CHAR)
);

-- ============================================================================
-- TEST 6: Replacement Functions
-- ============================================================================

-- Test REPLACE function
CALL run_string_test(
    'REPLACE substitutes all occurrences',
    'REPLACE',
    'hello world',
    'hello SQL',
    REPLACE('hello world', 'world', 'SQL')
);

-- Test REPLACE with multiple occurrences
CALL run_string_test(
    'REPLACE handles multiple occurrences',
    'REPLACE',
    'hello hello',
    'hi hi',
    REPLACE('hello hello', 'hello', 'hi')
);

-- ============================================================================
-- TEST 7: Validation Functions
-- ============================================================================

-- Test IS NULL OR EMPTY
CALL run_string_test(
    'Empty string is null or empty',
    'IS NULL OR EMPTY',
    '',
    '1',
    CAST(('' IS NULL OR '' = '') AS CHAR)
);

-- Test numeric validation
CALL run_string_test(
    'Numeric string passes validation',
    'REGEXP',
    '12345',
    '1',
    CAST(('12345' REGEXP '^[0-9]+$') AS CHAR)
);

-- Test non-numeric fails validation
CALL run_string_test(
    'Non-numeric string fails validation',
    'REGEXP',
    'abc',
    '0',
    CAST(('abc' REGEXP '^[0-9]+$') AS CHAR)
);

-- Test email validation
CALL run_string_test(
    'Valid email passes validation',
    'REGEXP',
    'user@example.com',
    '1',
    CAST(('user@example.com' REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$') AS CHAR)
);

-- Test invalid email fails validation
CALL run_string_test(
    'Invalid email fails validation',
    'REGEXP',
    'invalid-email',
    '0',
    CAST(('invalid-email' REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$') AS CHAR)
);

-- ============================================================================
-- TEST 8: Formatting Functions
-- ============================================================================

-- Test REVERSE function
CALL run_string_test(
    'REVERSE reverses string',
    'REVERSE',
    'hello',
    'olleh',
    REVERSE('hello')
);

-- Test LENGTH function
CALL run_string_test(
    'LENGTH returns correct count',
    'LENGTH',
    'hello',
    '5',
    CAST(LENGTH('hello') AS CHAR)
);

-- Test REPEAT function
CALL run_string_test(
    'REPEAT duplicates string',
    'REPEAT',
    'ab',
    'ababab',
    REPEAT('ab', 3)
);

-- ============================================================================
-- TEST RESULTS
--