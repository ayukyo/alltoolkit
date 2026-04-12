-- ============================================================================
-- SQL JSON Utilities - Test Suite
-- ============================================================================
-- Comprehensive test suite for JSON utility functions.
-- Run these tests to verify functionality on your database system.
--
-- Note: Some tests are database-specific and marked accordingly.
-- ============================================================================

-- ============================================================================
-- TEST SETUP
-- ============================================================================

-- Create test table
CREATE TABLE IF NOT EXISTS json_utils_tests (
    test_id INT AUTO_INCREMENT PRIMARY KEY,
    test_name VARCHAR(255),
    test_category VARCHAR(100),
    input_value TEXT,
    expected_result TEXT,
    actual_result TEXT,
    passed BOOLEAN,
    test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Clear previous test results
TRUNCATE TABLE json_utils_tests;

-- ============================================================================
-- HELPER PROCEDURE FOR RUNNING TESTS
-- ============================================================================

DELIMITER //

CREATE PROCEDURE IF NOT EXISTS run_json_test(
    IN test_name VARCHAR(255),
    IN test_category VARCHAR(100),
    IN input_val TEXT,
    IN expected TEXT,
    IN actual TEXT
)
BEGIN
    INSERT INTO json_utils_tests (test_name, test_category, input_value, expected_result, actual_result, passed)
    VALUES (test_name, test_category, input_val, expected, actual, actual = expected);
END //

DELIMITER ;

-- ============================================================================
-- TEST 1: JSON VALIDATION
-- ============================================================================

-- Test JSON_VALID function
CALL run_json_test(
    'JSON_VALID returns 1 for valid JSON object',
    'Validation',
    '{"name": "John", "age": 30}',
    '1',
    CAST(JSON_VALID('{"name": "John", "age": 30}') AS CHAR)
);

CALL run_json_test(
    'JSON_VALID returns 1 for valid JSON array',
    'Validation',
    '[1, 2, 3, 4, 5]',
    '1',
    CAST(JSON_VALID('[1, 2, 3, 4, 5]') AS CHAR)
);

CALL run_json_test(
    'JSON_VALID returns 0 for invalid JSON',
    'Validation',
    '{name: John}',
    '0',
    CAST(JSON_VALID('{name: John}') AS CHAR)
);

CALL run_json_test(
    'JSON_VALID returns 0 for empty string',
    'Validation',
    '',
    '0',
    CAST(JSON_VALID('') AS CHAR)
);

-- ============================================================================
-- TEST 2: JSON TYPE CHECKING
-- ============================================================================

CALL run_json_test(
    'JSON_TYPE returns OBJECT for JSON object',
    'Type Check',
    '{"a": 1}',
    'OBJECT',
    JSON_TYPE('{"a": 1}')
);

CALL run_json_test(
    'JSON_TYPE returns ARRAY for JSON array',
    'Type Check',
    '[1, 2, 3]',
    'ARRAY',
    JSON_TYPE('[1, 2, 3]')
);

CALL run_json_test(
    'JSON_TYPE returns INTEGER for JSON number',
    'Type Check',
    '42',
    'INTEGER',
    JSON_TYPE('42')
);

CALL run_json_test(
    'JSON_TYPE returns STRING for JSON string',
    'Type Check',
    '"hello"',
    'STRING',
    JSON_TYPE('"hello"')
);

CALL run_json_test(
    'JSON_TYPE returns BOOLEAN for JSON boolean',
    'Type Check',
    'true',
    'BOOLEAN',
    JSON_TYPE('true')
);

CALL run_json_test(
    'JSON_TYPE returns NULL for JSON null',
    'Type Check',
    'null',
    'NULL',
    JSON_TYPE('null')
);

-- ============================================================================
-- TEST 3: JSON EXTRACTION - BASIC
-- ============================================================================

CALL run_json_test(
    'JSON_EXTRACT gets string value from object',
    'Extraction',
    '{"name": "John", "age": 30}',
    '"John"',
    JSON_EXTRACT('{"name": "John", "age": 30}', '$.name')
);

CALL run_json_test(
    'JSON_EXTRACT gets numeric value from object',
    'Extraction',
    '{"name": "John", "age": 30}',
    '30',
    CAST(JSON_EXTRACT('{"name": "John", "age": 30}', '$.age') AS CHAR)
);

CALL run_json_test(
    'JSON_UNQUOTE removes quotes from extracted string',
    'Extraction',
    '{"name": "John"}',
    'John',
    JSON_UNQUOTE(JSON_EXTRACT('{"name": "John"}', '$.name'))
);

CALL run_json_test(
    'JSON_EXTRACT returns NULL for missing key',
    'Extraction',
    '{"name": "John"}',
    'NULL',
    IFNULL(JSON_EXTRACT('{"name": "John"}', '$.age'), 'NULL')
);

-- ============================================================================
-- TEST 4: JSON EXTRACTION - NESTED
-- ============================================================================

CALL run_json_test(
    'JSON_EXTRACT gets nested value',
    'Nested Extraction',
    '{"user": {"profile": {"name": "Alice"}}}',
    '"Alice"',
    JSON_EXTRACT('{"user": {"profile": {"name": "Alice"}}}', '$.user.profile.name')
);

CALL run_json_test(
    'JSON_EXTRACT gets deeply nested array element',
    'Nested Extraction',
    '{"data": {"items": [{"id": 1}, {"id": 2}]}}',
    '2',
    CAST(JSON_EXTRACT('{"data": {"items": [{"id": 1}, {"id": 2}]}}', '$.data.items[1].id') AS CHAR)
);

CALL run_json_test(
    'JSON_EXTRACT handles multiple levels of nesting',
    'Nested Extraction',
    '{"a": {"b": {"c": {"d": "value"}}}}',
    '"value"',
    JSON_EXTRACT('{"a": {"b": {"c": {"d": "value"}}}}', '$.a.b.c.d')
);

-- ============================================================================
-- TEST 5: JSON ARRAY OPERATIONS
-- ============================================================================

CALL run_json_test(
    'JSON_EXTRACT gets first array element',
    'Array Operations',
    '[10, 20, 30]',
    '10',
    CAST(JSON_EXTRACT('[10, 20, 30]', '$[0]') AS CHAR)
);

CALL run_json_test(
    'JSON_EXTRACT gets middle array element',
    'Array Operations',
    '[10, 20, 30]',
    '20',
    CAST(JSON_EXTRACT('[10, 20, 30]', '$[1]') AS CHAR)
);

CALL run_json_test(
    'JSON_EXTRACT gets last array element',
    'Array Operations',
    '[10, 20, 30]',
    '30',
    CAST(JSON_EXTRACT('[10, 20, 30]', '$[2]') AS CHAR)
);

CALL run_json_test(
    'JSON_LENGTH returns correct array length',
    'Array Operations',
    '[1, 2, 3, 4, 5]',
    '5',
    CAST(JSON_LENGTH('[1, 2, 3, 4, 5]') AS CHAR)
);

CALL run_json_test(
    'JSON_LENGTH returns 1 for single object',
    'Array Operations',
    '{"a": 1}',
    '1',
    CAST(JSON_LENGTH('{"a": 1}') AS CHAR)
);

CALL run_json_test(
    'JSON_EXTRACT from nested array in object',
    'Array Operations',
    '{"tags": ["red", "blue", "green"]}',
    '"blue"',
    JSON_EXTRACT('{"tags": ["red", "blue", "green"]}', '$.tags[1]')
);

-- ============================================================================
-- TEST 6: JSON OBJECT OPERATIONS
-- ============================================================================

CALL run_json_test(
    'JSON_KEYS returns all keys from object',
    'Object Operations',
    '{"name": "John", "age": 30, "city": "NYC"}',
    '["name", "age", "city"]',
    JSON_KEYS('{"name": "John", "age": 30, "city": "NYC"}')
);

CALL run_json_test(
    'JSON_CONTAINS_PATH returns 1 for existing key',
    'Object Operations',
    '{"name": "John"}',
    '1',
    CAST(JSON_CONTAINS_PATH('{"name": "John"}', 'one', '$.name') AS CHAR)
);

CALL run_json_test(
    'JSON_CONTAINS_PATH returns 0 for missing key',
    'Object Operations',
    '{"name": "John"}',
    '0',
    CAST(JSON_CONTAINS_PATH('{"name": "John"}', 'one', '$.age') AS CHAR)
);

CALL run_json_test(
    'JSON_CONTAINS_PATH checks multiple paths',
    'Object Operations',
    '{"name": "John", "age": 30}',
    '1',
    CAST(JSON_CONTAINS_PATH('{"name": "John", "age": 30}', 'all', '$.name', '$.age') AS CHAR)
);

-- ============================================================================
-- TEST 7: JSON CREATION
-- ============================================================================

CALL run_json_test(
    'JSON_OBJECT creates valid object',
    'Creation',
    'name=Alice, age=25',
    '{"name": "Alice", "age": 25}',
    JSON_OBJECT('name', 'Alice', 'age', 25)
);

CALL run_json_test(
    'JSON_ARRAY creates valid array',
    'Creation',
    '1, 2, 3',
    '[1, 2, 3]',
    JSON_ARRAY(1, 2, 3)
);

CALL run_json_test(
    'JSON_ARRAY creates array with mixed types',
    'Creation',
    '1, "two", true',
    '[1, "two", true]',
    JSON_ARRAY(1, 'two', TRUE)
);

CALL run_json_test(
    'JSON_QUOTE wraps string in quotes',
    'Creation',
    'hello',
    '"hello"',
    JSON_QUOTE('hello')
);

-- ============================================================================
-- TEST 8: JSON MODIFICATION
-- ============================================================================

CALL run_json_test(
    'JSON_SET adds new key to object',
    'Modification',
    '{"name": "John"}',
    '{"name": "John", "age": 30}',
    JSON_SET('{"name": "John"}', '$.age', 30)
);

CALL run_json_test(
    'JSON_SET updates existing key',
    'Modification',
    '{"name": "John", "age": 30}',
    '{"name": "John", "age": 35}',
    JSON_SET('{"name": "John", "age": 30}', '$.age', 35)
);

CALL run_json_test(
    'JSON_REMOVE removes key from object',
    'Modification',
    '{"name": "John", "age": 30}',
    '{"name": "John"}',
    JSON_REMOVE('{"name": "John", "age": 30}', '$.age')
);

CALL run_json_test(
    'JSON_REMOVE removes array element',
    'Modification',
    '[10, 20, 30]',
    '[10, 30]',
    JSON_REMOVE('[10, 20, 30]', '$[1]')
);

CALL run_json_test(
    'JSON_ARRAY_APPEND adds element to array',
    'Modification',
    '[1, 2, 3]',
    '[1, 2, 3, 4]',
    JSON_ARRAY_APPEND('[1, 2, 3]', '$', 4)
);

-- ============================================================================
-- TEST 9: JSON SEARCH AND CONTAINS
-- ============================================================================

CALL run_json_test(
    'JSON_CONTAINS finds value in array',
    'Search',
    '{"tags": ["red", "blue", "green"]}',
    '1',
    CAST(JSON_CONTAINS('{"tags": ["red", "blue", "green"]}', '"red"', '$.tags') AS CHAR)
);

CALL run_json_test(
    'JSON_CONTAINS returns 0 for missing value',
    'Search',
    '{"tags": ["red", "blue", "green"]}',
    '0',
    CAST(JSON_CONTAINS('{"tags": ["red", "blue", "green"]}', '"yellow"', '$.tags') AS CHAR)
);

CALL run_json_test(
    'JSON_CONTAINS finds object in array',
    'Search',
    '{"items": [{"id": 1}, {"id": 2}]}',
    '1',
    CAST(JSON_CONTAINS('{"items": [{"id": 1}, {"id": 2}]}', '{"id": 1}', '$.items') AS CHAR)
);

CALL run_json_test(
    'JSON_SEARCH finds path to value',
    'Search',
    '{"name": "John", "city": "NYC"}',
    '"$.name"',
    JSON_SEARCH('{"name": "John", "city": "NYC"}', 'one', 'John')
);

CALL run_json_test(
    'JSON_SEARCH finds all paths to value',
    'Search',
    '{"a": "test", "b": "test"}',
    '["$.a", "$.b"]',
    JSON_SEARCH('{"a": "test", "b": "test"}', 'all', 'test')
);

-- ============================================================================
-- TEST 10: JSON MERGING
-- ============================================================================

CALL run_json_test(
    'JSON_MERGE_PRESERVE merges objects',
    'Merging',
    '{"a": 1}, {"b": 2}',
    '{"a": 1, "b": 2}',
    JSON_MERGE_PRESERVE('{"a": 1}', '{"b": 2}')
);

CALL run_json_test(
    'JSON_MERGE_PRESERVE concatenates arrays',
    'Merging',
    '{"arr": [1]}, {"arr": [2]}',
    '{"arr": [1, 2]}',
    JSON_MERGE_PRESERVE('{"arr": [1]}', '{"arr": [2]}')
);

CALL run_json_test(
    'JSON_MERGE_PATCH replaces arrays',
    'Merging',
    '{"arr": [1]}, {"arr": [2]}',
    '{"arr": [2]}',
    JSON_MERGE_PATCH('{"arr": [1]}', '{"arr": [2]}')
);

CALL run_json_test(
    'JSON_MERGE_PATCH updates values',
    'Merging',
    '{"name": "John", "age": 30}, {"age": 35}',
    '{"name": "John", "age": 35}',
    JSON_MERGE_PATCH('{"name": "John", "age": 30}', '{"age": 35}')
);

-- ============================================================================
-- TEST 11: CUSTOM STORED FUNCTIONS
-- ============================================================================

-- Test json_get_string
CALL run_json_test(
    'json_get_string extracts string value',
    'Custom Functions',
    '{"name": "Alice"}, key=name',
    'Alice',
    json_get_string('{"name": "Alice"}', 'name')
);

-- Test json_get_number
CALL run_json_test(
    'json_get_number extracts numeric value',
    'Custom Functions',
    '{"price": 99.99}, key=price',
    '99.99',
    CAST(json_get_number('{"price": 99.99}', 'price') AS CHAR)
);

-- Test json_has_key
CALL run_json_test(
    'json_has_key returns true for existing key',
    'Custom Functions',
    '{"name": "John"}, key=name',
    '1',
    CAST(json_has_key('{"name": "John"}', 'name') AS CHAR)
);

CALL run_json_test(
    'json_has_key returns false for missing key',
    'Custom Functions',
    '{"name": "John"}, key=age',
    '0',
    CAST(json_has_key('{"name": "John"}', 'age') AS CHAR)
);

-- Test json_add_key
CALL run_json_test(
    'json_add_key adds new key',
    'Custom Functions',
    '{"name": "John"}, key=age, value=30',
    '{"name": "John", "age": "30"}',
    json_add_key('{"name": "John"}', 'age', '30')
);

-- Test json_remove_key
CALL run_json_test(
    'json_remove_key removes key',
    'Custom Functions',
    '{"name": "John", "age": 30}, key=age',
    '{"name": "John"}',
    json_remove_key('{"name": "John", "age": 30}', 'age')
);

-- Test json_array_contains
CALL run_json_test(
    'json_array_contains finds value',
    'Custom Functions',
    '["red", "blue", "green"], value=blue',
    '1',
    CAST(json_array_contains('["red", "blue", "green"]', 'blue') AS CHAR)
);

CALL run_json_test(
    'json_array_contains returns false for missing',
    'Custom Functions',
    '["red", "blue", "green"], value=yellow',
    '0',
    CAST(json_array_contains('["red", "blue", "green"]', 'yellow') AS CHAR)
);

-- Test json_array_element
CALL run_json_test(
    'json_array_element gets first element',
    'Custom Functions',
    '[10, 20, 30], index=1',
    '10',
    json_array_element('[10, 20, 30]', 1)
);

CALL run_json_test(
    'json_array_element gets last element',
    'Custom Functions',
    '[10, 20, 30], index=3',
    '30',
    json_array_element('[10, 20, 30]', 3)
);

-- Test json_merge_objects
CALL run_json_test(
    'json_merge_objects merges two objects',
    'Custom Functions',
    '{"a": 1}, {"b": 2}',
    '{"a": 1, "b": 2}',
    json_merge_objects('{"a": 1}', '{"b": 2}')
);

-- Test json_is_valid
CALL run_json_test(
    'json_is_valid returns true for valid JSON',
    'Custom Functions',
    '{"name": "John"}',
    '1',
    CAST(json_is_valid('{"name": "John"}') AS CHAR)
);

CALL run_json_test(
    'json_is_valid returns false for invalid JSON',
    'Custom Functions',
    '{invalid json}',
    '0',
    CAST(json_is_valid('{invalid json}') AS CHAR)
);

-- Test json_type_check
CALL run_json_test(
    'json_type_check returns OBJECT for object',
    'Custom Functions',
    '{"a": 1}',
    'OBJECT',
    json_type_check('{"a": 1}')
);

CALL run_json_test(
    'json_type_check returns ARRAY for array',
    'Custom Functions',
    '[1, 2, 3]',
    'ARRAY',
    json_type_check('[1, 2, 3]')
);

-- ============================================================================
-- TEST 12: JSON PRETTY PRINTING
-- ============================================================================

-- Note: Pretty print output varies, so we check structure
CALL run_json_test(
    'JSON_PRETTY formats JSON with newlines',
    'Pretty Print',
    '{"name":"John"}',
    'contains_newlines',
    IF(JSON_PRETTY('{"name":"John"}') LIKE '%\n%', 'contains_newlines', 'no_newlines')
);

CALL run_json_test(
    'json_pretty_format adds indentation',
    'Pretty Print',
    '{"name":"John","age":30}',
    'contains_newlines',
    IF(json_pretty_format('{"name":"John","age":30}') LIKE '%\n%', 'contains_newlines', 'no_newlines')
);

-- ============================================================================
-- TEST 13: COMPLEX REAL-WORLD SCENARIOS
-- ============================================================================

CALL run_json_test(
    'Extract from complex nested structure',
    'Complex',
    '{"order": {"customer": {"id": 123, "name": "Alice"}, "items": [{"product": "Widget", "qty": 5}, {"product": "Gadget", "qty": 3}]}}',
    'Gadget',
    JSON_UNQUOTE(JSON_EXTRACT('{"order": {"customer": {"id": 123, "name": "Alice"}, "items": [{"product": "Widget", "qty": 5}, {"product": "Gadget", "qty": 3}]}}', '$.order.items[1].product'))
);

CALL run_json_test(
    'Update nested array element',
    'Complex',
    '{"data": {"values": [1, 2, 3]}}',
    '{"data": {"values": [1, 5, 3]}}',
    JSON_SET('{"data": {"values": [1, 2, 3]}}', '$.data.values[1]', 5)
);

CALL run_json_test(
    'Merge multiple levels of objects',
    'Complex',
    '{"config": {"db": {"host": "localhost"}}}, {"config": {"db": {"port": 3306}}}',
    '{"config": {"db": {"host": "localhost", "port": 3306}}}',
    JSON_MERGE_PATCH('{"config": {"db": {"host": "localhost"}}}', '{"config": {"db": {"port": 3306}}}')
);

-- ============================================================================
-- TEST RESULTS SUMMARY
-- ============================================================================

-- Display test summary
SELECT 
    test_category,
    COUNT(*) AS total_tests,
    SUM(CASE WHEN passed = 1 THEN 1 ELSE 0 END) AS passed_tests,
    SUM(CASE WHEN passed = 0 THEN 1 ELSE 0 END) AS failed_tests,
    CONCAT(ROUND(SUM(CASE WHEN passed = 1 THEN 1 ELSE 0 END) / COUNT(*) * 100, 1), '%') AS pass_rate
FROM json_utils_tests
GROUP BY test_category
ORDER BY test_category;

-- Display overall summary
SELECT 
    'OVERALL' AS summary,
    COUNT(*) AS total_tests,
    SUM(CASE WHEN passed = 1 THEN 1 ELSE 0 END) AS passed_tests,
    SUM(CASE WHEN passed = 0 THEN 1 ELSE 0 END) AS failed_tests,
    CONCAT(ROUND(SUM(CASE WHEN passed = 1 THEN 1 ELSE 0 END) / COUNT(*) * 100, 1), '%') AS pass_rate
FROM json_utils_tests;

-- Display failed tests (if any)
SELECT test_name, test_category, input_value, expected_result, actual_result
FROM json_utils_tests
WHERE passed = 0;

-- ============================================================================
-- CLEANUP (Optional)
-- ============================================================================

-- Drop test table when done
-- DROP TABLE IF EXISTS json_utils_tests;

-- Drop test procedure when done
-- DROP PROCEDURE IF EXISTS run_json_test;

-- ============================================================================
-- END OF TEST SUITE
-- ============================================================================