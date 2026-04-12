-- ============================================================================
-- SQL JSON Utilities Module
-- ============================================================================
-- A comprehensive JSON manipulation utility module for SQL providing common
-- JSON operations across multiple database systems (MySQL, PostgreSQL, 
-- SQL Server, SQLite).
--
-- Features:
-- - JSON parsing and validation
-- - JSON path extraction and querying
-- - JSON creation and modification
-- - JSON merging and aggregation
-- - JSON type checking and conversion
-- - JSON array operations
-- - JSON object operations
--
-- Supported Databases:
-- - MySQL 5.7+ (JSON type supported)
-- - PostgreSQL 9.4+ (JSONB type supported)
-- - SQL Server 2016+ (JSON functions supported)
-- - SQLite 3.38+ (JSON1 extension)
--
-- Author: AllToolkit
-- Version: 1.0.0
-- License: MIT
-- ============================================================================

-- ============================================================================
-- SECTION 1: JSON VALIDATION AND TYPE CHECKING
-- ============================================================================

-- Check if string is valid JSON
-- MySQL:     JSON_VALID(json_str) returns 1 if valid
-- PostgreSQL: json_str::json IS NOT NULL (try casting)
-- SQL Server: ISJSON(json_str) returns 1 if valid
-- SQLite:    json_valid(json_str) returns 1 if valid

-- MySQL Example:
-- SELECT JSON_VALID('{"name": "John", "age": 30}') AS is_valid;
-- Returns: 1

-- PostgreSQL Example:
-- SELECT ('{"name": "John", "age": 30}'::json IS NOT NULL) AS is_valid;
-- Returns: true

-- SQL Server Example:
-- SELECT ISJSON('{"name": "John", "age": 30}') AS is_valid;
-- Returns: 1

-- SQLite Example:
-- SELECT json_valid('{"name": "John", "age": 30}') AS is_valid;
-- Returns: 1

-- Check JSON type (object, array, scalar)
-- MySQL:     JSON_TYPE(json_val)
-- PostgreSQL: json_typeof(json_val)
-- SQL Server: No direct equivalent - check structure
-- SQLite:    json_type(json_val)

-- MySQL Example:
-- SELECT JSON_TYPE('{"a": 1}') AS type;
-- Returns: OBJECT
-- SELECT JSON_TYPE('[1, 2, 3]') AS type;
-- Returns: ARRAY

-- PostgreSQL Example:
-- SELECT json_typeof('{"a": 1}'::json) AS type;
-- Returns: object

-- ============================================================================
-- SECTION 2: JSON VALUE EXTRACTION
-- ============================================================================

-- Extract value by key from JSON object
-- MySQL:     JSON_EXTRACT(json_doc, '$.key') or JSON_UNQUOTE(JSON_EXTRACT(...))
-- PostgreSQL: json_doc->'key' or json_doc->>'key' (as text)
-- SQL Server: JSON_VALUE(json_doc, '$.key')
-- SQLite:    json_extract(json_doc, '$.key')

-- MySQL Examples:
-- SELECT JSON_EXTRACT('{"name": "John", "age": 30}', '$.name') AS name;
-- Returns: "John"
-- SELECT JSON_UNQUOTE(JSON_EXTRACT('{"name": "John", "age": 30}', '$.name')) AS name;
-- Returns: John

-- PostgreSQL Examples:
-- SELECT '{"name": "John", "age": 30}'::json->'name' AS name;
-- Returns: "John"
-- SELECT '{"name": "John", "age": 30}'::json->>'name' AS name;
-- Returns: John (as text)

-- SQL Server Example:
-- SELECT JSON_VALUE('{"name": "John", "age": 30}', '$.name') AS name;
-- Returns: John

-- SQLite Example:
-- SELECT json_extract('{"name": "John", "age": 30}', '$.name') AS name;
-- Returns: John

-- Extract nested value using path
-- MySQL:     JSON_EXTRACT(json_doc, '$.path.to.value')
-- PostgreSQL: json_doc#>'{path,to,value}' or json_doc#>>'{path,to,value}'
-- SQL Server: JSON_VALUE(json_doc, '$.path.to.value')
-- SQLite:    json_extract(json_doc, '$.path.to.value')

-- MySQL Example:
-- SELECT JSON_EXTRACT('{"user": {"profile": {"name": "Alice"}}}', '$.user.profile.name') AS name;
-- Returns: "Alice"

-- PostgreSQL Example:
-- SELECT '{"user": {"profile": {"name": "Alice"}}}'::json#>>'{user,profile,name}' AS name;
-- Returns: Alice

-- SQL Server Example:
-- SELECT JSON_VALUE('{"user": {"profile": {"name": "Alice"}}}', '$.user.profile.name') AS name;
-- Returns: Alice

-- ============================================================================
-- SECTION 3: JSON ARRAY OPERATIONS
-- ============================================================================

-- Extract element from JSON array by index
-- MySQL:     JSON_EXTRACT(json_arr, '$[index]')
-- PostgreSQL: json_arr->index
-- SQL Server: JSON_VALUE(json_arr, '$[index]')
-- SQLite:    json_extract(json_arr, '$[index]')

-- MySQL Example:
-- SELECT JSON_EXTRACT('[10, 20, 30]', '$[1]') AS element;
-- Returns: 20

-- PostgreSQL Example:
-- SELECT '[10, 20, 30]'::json->1 AS element;
-- Returns: 20

-- SQL Server Example:
-- SELECT JSON_VALUE('[10, 20, 30]', '$[1]') AS element;
-- Returns: 20

-- SQLite Example:
-- SELECT json_extract('[10, 20, 30]', '$[1]') AS element;
-- Returns: 20

-- Get array length
-- MySQL:     JSON_LENGTH(json_arr)
-- PostgreSQL: json_array_length(json_arr)
-- SQL Server: No direct equivalent - use OPENJSON with COUNT
-- SQLite:    json_array_length(json_arr)

-- MySQL Example:
-- SELECT JSON_LENGTH('[1, 2, 3, 4, 5]') AS length;
-- Returns: 5

-- PostgreSQL Example:
-- SELECT json_array_length('[1, 2, 3, 4, 5]'::json) AS length;
-- Returns: 5

-- SQLite Example:
-- SELECT json_array_length('[1, 2, 3, 4, 5]') AS length;
-- Returns: 5

-- ============================================================================
-- SECTION 4: JSON OBJECT OPERATIONS
-- ============================================================================

-- Get all keys from JSON object
-- MySQL:     JSON_KEYS(json_obj)
-- PostgreSQL: No direct equivalent - need custom function
-- SQL Server: No direct equivalent
-- SQLite:    No direct equivalent - need custom approach

-- MySQL Example:
-- SELECT JSON_KEYS('{"name": "John", "age": 30, "city": "NYC"}') AS keys;
-- Returns: ["name", "age", "city"]

-- Check if key exists
-- MySQL:     JSON_CONTAINS_PATH(json_doc, 'one', '$.key')
-- PostgreSQL: json_obj ? 'key'
-- SQL Server: JSON_VALUE returns NULL if not exists
-- SQLite:    json_extract returns NULL if not exists

-- MySQL Example:
-- SELECT JSON_CONTAINS_PATH('{"name": "John"}', 'one', '$.name') AS exists;
-- Returns: 1
-- SELECT JSON_CONTAINS_PATH('{"name": "John"}', 'one', '$.age') AS exists;
-- Returns: 0

-- PostgreSQL Example:
-- SELECT '{"name": "John"}'::jsonb ? 'name' AS exists;
-- Returns: true
-- SELECT '{"name": "John"}'::jsonb ? 'age' AS exists;
-- Returns: false

-- ============================================================================
-- SECTION 5: JSON CREATION AND MODIFICATION
-- ============================================================================

-- Create JSON object from values
-- MySQL:     JSON_OBJECT('key1', val1, 'key2', val2, ...)
-- PostgreSQL: json_build_object('key1', val1, 'key2', val2, ...)
-- SQL Server: No direct equivalent - construct string or use FOR JSON
-- SQLite:    json_object('key1', val1, 'key2', val2, ...)

-- MySQL Example:
-- SELECT JSON_OBJECT('name', 'Alice', 'age', 25, 'active', true) AS json_obj;
-- Returns: {"name": "Alice", "age": 25, "active": true}

-- PostgreSQL Example:
-- SELECT json_build_object('name', 'Alice', 'age', 25, 'active', true) AS json_obj;
-- Returns: {"name": "Alice", "age": 25, "active": true}

-- SQLite Example:
-- SELECT json_object('name', 'Alice', 'age', 25) AS json_obj;
-- Returns: {"name": "Alice", "age": 25}

-- Create JSON array from values
-- MySQL:     JSON_ARRAY(val1, val2, val3, ...)
-- PostgreSQL: json_build_array(val1, val2, val3, ...) or array_to_json
-- SQL Server: No direct equivalent - construct string or use FOR JSON
-- SQLite:    json_array(val1, val2, val3, ...)

-- MySQL Example:
-- SELECT JSON_ARRAY(1, 2, 3, 'four', true) AS json_arr;
-- Returns: [1, 2, 3, "four", true]

-- PostgreSQL Example:
-- SELECT json_build_array(1, 2, 3, 'four', true) AS json_arr;
-- Returns: [1, 2, 3, "four", true]

-- SQLite Example:
-- SELECT json_array(1, 2, 3, 'four') AS json_arr;
-- Returns: [1, 2, 3, "four"]

-- Insert or update value in JSON object
-- MySQL:     JSON_SET(json_doc, '$.key', value)
-- PostgreSQL: jsonb_set(json_doc, '{key}', value)
-- SQL Server: JSON_MODIFY(json_doc, '$.key', value)
-- SQLite:    json_set(json_doc, '$.key', value)

-- MySQL Example:
-- SELECT JSON_SET('{"name": "John"}', '$.age', 30) AS updated;
-- Returns: {"name": "John", "age": 30}

-- PostgreSQL Example:
-- SELECT jsonb_set('{"name": "John"}'::jsonb, '{age}', '30'::jsonb) AS updated;
-- Returns: {"name": "John", "age": 30}

-- SQL Server Example:
-- SELECT JSON_MODIFY('{"name": "John"}', '$.age', 30) AS updated;
-- Returns: {"name": "John", "age": 30}

-- SQLite Example:
-- SELECT json_set('{"name": "John"}', '$.age', 30) AS updated;
-- Returns: {"name": "John", "age": 30}

-- Remove key from JSON object
-- MySQL:     JSON_REMOVE(json_doc, '$.key')
-- PostgreSQL: json_doc - 'key' (for jsonb)
-- SQL Server: JSON_MODIFY(json_doc, '$.key', NULL)
-- SQLite:    json_remove(json_doc, '$.key')

-- MySQL Example:
-- SELECT JSON_REMOVE('{"name": "John", "age": 30}', '$.age') AS removed;
-- Returns: {"name": "John"}

-- PostgreSQL Example:
-- SELECT '{"name": "John", "age": 30}'::jsonb - 'age' AS removed;
-- Returns: {"name": "John"}

-- SQL Server Example:
-- SELECT JSON_MODIFY('{"name": "John", "age": 30}', '$.age', NULL) AS removed;
-- Returns: {"name": "John"}

-- SQLite Example:
-- SELECT json_remove('{"name": "John", "age": 30}', '$.age') AS removed;
-- Returns: {"name": "John"}

-- ============================================================================
-- SECTION 6: JSON SEARCH AND CONTAINS
-- ============================================================================

-- Check if JSON contains a value
-- MySQL:     JSON_CONTAINS(json_doc, value, path)
-- PostgreSQL: jsonb @> value_json (contains check)
-- SQL Server: No direct equivalent - use OPENJSON and compare
-- SQLite:    No direct equivalent - extract and compare

-- MySQL Example:
-- SELECT JSON_CONTAINS('{"tags": ["red", "blue", "green"]}', '"red"', '$.tags') AS contains_red;
-- Returns: 1

-- PostgreSQL Example:
-- SELECT '{"tags": ["red", "blue", "green"]}'::jsonb @> '{"tags": ["red"]}'::jsonb AS contains_red;
-- Returns: true

-- Search for value in JSON and return path
-- MySQL:     JSON_SEARCH(json_doc, 'one'/'all', search_str)
-- PostgreSQL: No direct equivalent
-- SQL Server: No direct equivalent
-- SQLite:    No direct equivalent

-- MySQL Example:
-- SELECT JSON_SEARCH('{"name": "John", "city": "NYC"}', 'one', 'John') AS path;
-- Returns: "$.name"

-- ============================================================================
-- SECTION 7: JSON MERGING AND AGGREGATION
-- ============================================================================

-- Merge two JSON objects
-- MySQL:     JSON_MERGE_PRESERVE(obj1, obj2) or JSON_MERGE_PATCH(obj1, obj2)
-- PostgreSQL: obj1 || obj2 (for jsonb)
-- SQL Server: No direct equivalent
-- SQLite:    No direct equivalent - custom approach needed

-- MySQL Example (preserve - keeps both arrays):
-- SELECT JSON_MERGE_PRESERVE('{"a": [1]}', '{"a": [2]}') AS merged;
-- Returns: {"a": [1, 2]}

-- MySQL Example (patch - replaces arrays):
-- SELECT JSON_MERGE_PATCH('{"a": [1]}', '{"a": [2]}') AS merged;
-- Returns: {"a": [2]}

-- PostgreSQL Example:
-- SELECT '{"a": 1}'::jsonb || '{"b": 2}'::jsonb AS merged;
-- Returns: {"a": 1, "b": 2}

-- Aggregate rows into JSON array
-- MySQL:     JSON_ARRAYAGG(column)
-- PostgreSQL: json_agg(column)
-- SQL Server: No direct equivalent - use FOR JSON PATH
-- SQLite:    json_group_array(column)

-- MySQL Example:
-- SELECT JSON_ARRAYAGG(name) FROM users;
-- Returns: ["John", "Alice", "Bob"]

-- PostgreSQL Example:
-- SELECT json_agg(name) FROM users;
-- Returns: ["John", "Alice", "Bob"]

-- SQLite Example:
-- SELECT json_group_array(name) FROM users;
-- Returns: ["John", "Alice", "Bob"]

-- Aggregate rows into JSON object
-- MySQL:     JSON_OBJECTAGG(key_col, val_col)
-- PostgreSQL: json_object_agg(key_col, val_col)
-- SQL Server: No direct equivalent
-- SQLite:    json_group_object(key_col, val_col)

-- MySQL Example:
-- SELECT JSON_OBJECTAGG(name, age) FROM users;
-- Returns: {"John": 30, "Alice": 25, "Bob": 35}

-- PostgreSQL Example:
-- SELECT json_object_agg(name, age) FROM users;
-- Returns: {"John": 30, "Alice": 25, "Bob": 35}

-- SQLite Example:
-- SELECT json_group_object(name, age) FROM users;
-- Returns: {"John": 30, "Alice": 25, "Bob": 35}

-- ============================================================================
-- SECTION 8: JSON TYPE CONVERSION
-- ============================================================================

-- Cast value to JSON type
-- MySQL:     CAST(str AS JSON)
-- PostgreSQL: str::json or str::jsonb
-- SQL Server: No explicit cast needed
-- SQLite:    json(str)

-- MySQL Example:
-- SELECT CAST('{"name": "John"}' AS JSON) AS json_col;
-- Returns: {"name": "John"}

-- PostgreSQL Example:
-- SELECT '{"name": "John"}'::jsonb AS json_col;
-- Returns: {"name": "John"}

-- Convert JSON to string
-- MySQL:     JSON_UNQUOTE(JSON_EXTRACT(...)) or CAST(json_col AS CHAR)
-- PostgreSQL: json_col::text
-- SQL Server: CAST(json_col AS NVARCHAR(MAX))
-- SQLite:    json(json_col) or just the column

-- MySQL Example:
-- SELECT CAST(JSON_OBJECT('name', 'John') AS CHAR) AS json_str;
-- Returns: {"name": "John"}

-- PostgreSQL Example:
-- SELECT '{"name": "John"}'::json::text AS json_str;
-- Returns: {"name": "John"}

-- ============================================================================
-- SECTION 9: JSON PRETTY PRINTING
-- ============================================================================

-- Pretty format JSON with indentation
-- MySQL:     JSON_PRETTY(json_doc)
-- PostgreSQL: No direct equivalent - use custom function
-- SQL Server: No direct equivalent
-- SQLite:    No direct equivalent

-- MySQL Example:
-- SELECT JSON_PRETTY('{"name": "John", "age": 30, "city": "NYC"}') AS pretty_json;
-- Returns:
-- {
--   "name": "John",
--   "age": 30,
--   "city": "NYC"
-- }

-- ============================================================================
-- SECTION 10: MYSQL STORED FUNCTIONS
-- ============================================================================

DELIMITER //

-- Function: json_get_string - Extract string value by key
-- Usage: SELECT json_get_string('{"name": "John"}', 'name');
-- Returns: John
CREATE FUNCTION IF NOT EXISTS json_get_string(json_doc JSON, path VARCHAR(255))
RETURNS VARCHAR(4000)
DETERMINISTIC
NO SQL
BEGIN
    RETURN JSON_UNQUOTE(JSON_EXTRACT(json_doc, CONCAT('$.', path)));
END //

-- Function: json_get_number - Extract numeric value by key
-- Usage: SELECT json_get_number('{"age": 30}', 'age');
-- Returns: 30
CREATE FUNCTION IF NOT EXISTS json_get_number(json_doc JSON, path VARCHAR(255))
RETURNS DECIMAL(38, 10)
DETERMINISTIC
NO SQL
BEGIN
    DECLARE result DECIMAL(38, 10);
    SET result = JSON_EXTRACT(json_doc, CONCAT('$.', path));
    RETURN result;
END //

-- Function: json_get_bool - Extract boolean value by key
-- Usage: SELECT json_get_bool('{"active": true}', 'active');
-- Returns: 1 (true)
CREATE FUNCTION IF NOT EXISTS json_get_bool(json_doc JSON, path VARCHAR(255))
RETURNS BOOLEAN
DETERMINISTIC
NO SQL
BEGIN
    DECLARE result VARCHAR(10);
    SET result = JSON_UNQUOTE(JSON_EXTRACT(json_doc, CONCAT('$.', path)));
    RETURN result = 'true';
END //

-- Function: json_has_key - Check if key exists in JSON object
-- Usage: SELECT json_has_key('{"name": "John"}', 'name');
-- Returns: 1 (true)
CREATE FUNCTION IF NOT EXISTS json_has_key(json_doc JSON, key_name VARCHAR(255))
RETURNS BOOLEAN
DETERMINISTIC
NO SQL
BEGIN
    RETURN JSON_CONTAINS_PATH(json_doc, 'one', CONCAT('$.', key_name));
END //

-- Function: json_add_key - Add or update a key in JSON object
-- Usage: SELECT json_add_key('{"name": "John"}', 'age', 30);
-- Returns: {"name": "John", "age": 30}
CREATE FUNCTION IF NOT EXISTS json_add_key(json_doc JSON, key_name VARCHAR(255), value_val VARCHAR(4000))
RETURNS JSON
DETERMINISTIC
NO SQL
BEGIN
    RETURN JSON_SET(json_doc, CONCAT('$.', key_name), CAST(value_val AS JSON));
END //

-- Function: json_remove_key - Remove a key from JSON object
-- Usage: SELECT json_remove_key('{"name": "John", "age": 30}', 'age');
-- Returns: {"name": "John"}
CREATE FUNCTION IF NOT EXISTS json_remove_key(json_doc JSON, key_name VARCHAR(255))
RETURNS JSON
DETERMINISTIC
NO SQL
BEGIN
    RETURN JSON_REMOVE(json_doc, CONCAT('$.', key_name));
END //

-- Function: json_array_contains - Check if array contains value
-- Usage: SELECT json_array_contains('["red", "blue", "green"]', 'red');
-- Returns: 1 (true)
CREATE FUNCTION IF NOT EXISTS json_array_contains(json_arr JSON, search_val VARCHAR(255))
RETURNS BOOLEAN
DETERMINISTIC
NO SQL
BEGIN
    RETURN JSON_CONTAINS(json_arr, JSON_QUOTE(search_val));
END //

-- Function: json_array_append_val - Append value to JSON array
-- Usage: SELECT json_array_append_val('[1, 2, 3]', 4);
-- Returns: [1, 2, 3, 4]
CREATE FUNCTION IF NOT EXISTS json_array_append_val(json_arr JSON, new_val VARCHAR(4000))
RETURNS JSON
DETERMINISTIC
NO SQL
BEGIN
    RETURN JSON_ARRAY_APPEND(json_arr, '$', CAST(new_val AS JSON));
END //

-- Function: json_array_element - Get element at index (1-based for convenience)
-- Usage: SELECT json_array_element('[10, 20, 30]', 1);
-- Returns: 10
CREATE FUNCTION IF NOT EXISTS json_array_element(json_arr JSON, index_val INT)
RETURNS VARCHAR(4000)
DETERMINISTIC
NO SQL
BEGIN
    IF index_val <= 0 OR index_val > JSON_LENGTH(json_arr) THEN
        RETURN NULL;
    END IF;
    RETURN JSON_UNQUOTE(JSON_EXTRACT(json_arr, CONCAT('$[', index_val - 1, ']')));
END //

-- Function: json_merge_objects - Merge two JSON objects
-- Usage: SELECT json_merge_objects('{"a": 1}', '{"b": 2}');
-- Returns: {"a": 1, "b": 2}
CREATE FUNCTION IF NOT EXISTS json_merge_objects(obj1 JSON, obj2 JSON)
RETURNS JSON
DETERMINISTIC
NO SQL
BEGIN
    RETURN JSON_MERGE_PATCH(obj1, obj2);
END //

-- Function: json_is_valid - Check if string is valid JSON
-- Usage: SELECT json_is_valid('{"name": "John"}');
-- Returns: 1 (true)
CREATE FUNCTION IF NOT EXISTS json_is_valid(json_str VARCHAR(4000))
RETURNS BOOLEAN
DETERMINISTIC
NO SQL
BEGIN
    RETURN JSON_VALID(json_str) = 1;
END //

-- Function: json_type_check - Get JSON type as string
-- Usage: SELECT json_type_check('{"a": 1}');
-- Returns: OBJECT
CREATE FUNCTION IF NOT EXISTS json_type_check(json_doc JSON)
RETURNS VARCHAR(20)
DETERMINISTIC
NO SQL
BEGIN
    RETURN JSON_TYPE(json_doc);
END //

-- Function: json_pretty_format - Format JSON with indentation
-- Usage: SELECT json_pretty_format('{"name":"John","age":30}');
-- Returns formatted JSON
CREATE FUNCTION IF NOT EXISTS json_pretty_format(json_doc JSON)
RETURNS TEXT
DETERMINISTIC
NO SQL
BEGIN
    RETURN JSON_PRETTY(json_doc);
END //

DELIMITER ;

-- ============================================================================
-- SECTION 11: POSTGRESQL STORED FUNCTIONS
-- ============================================================================

-- Note: PostgreSQL uses jsonb for most operations (better performance)
-- These functions are example definitions for PostgreSQL

/*
-- Function: json_get_text - Extract text value by key (PostgreSQL)
CREATE OR REPLACE FUNCTION json_get_text(json_doc jsonb, key_name text)
RETURNS text AS $$
BEGIN
    RETURN json_doc->>key_name;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function: json_get_int - Extract integer value by key (PostgreSQL)
CREATE OR REPLACE FUNCTION json_get_int(json_doc jsonb, key_name text)
RETURNS integer AS $$
BEGIN
    RETURN (json_doc->>key_name)::integer;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function: json_has_key - Check if key exists (PostgreSQL)
CREATE OR REPLACE FUNCTION json_has_key(json_doc jsonb, key_name text)
RETURNS boolean AS $$
BEGIN
    RETURN json_doc ? key_name;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function: json_add_key - Add or update key (PostgreSQL)
CREATE OR REPLACE FUNCTION json_add_key(json_doc jsonb, key_name text, value_val jsonb)
RETURNS jsonb AS $$
BEGIN
    RETURN jsonb_set(json_doc, ARRAY[key_name], value_val);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function: json_remove_key - Remove key from object (PostgreSQL)
CREATE OR REPLACE FUNCTION json_remove_key(json_doc jsonb, key_name text)
RETURNS jsonb AS $$
BEGIN
    RETURN json_doc - key_name;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function: json_array_contains - Check if array contains value (PostgreSQL)
CREATE OR REPLACE FUNCTION json_array_contains(json_arr jsonb, search_val text)
RETURNS boolean AS $$
BEGIN
    RETURN json_arr @> jsonb_build_array(search_val);
END;
$$ LANGUAGE plpgsql IMMUTABLE;
*/

-- ============================================================================
-- SECTION 12: PRACTICAL EXAMPLES
-- ============================================================================

-- Example 1: Extract user name from JSON column
-- MySQL:
--   SELECT JSON_UNQUOTE(JSON_EXTRACT(user_data, '$.name')) AS name FROM users;
-- PostgreSQL:
--   SELECT user_data->>'name' AS name FROM users;
-- SQL Server:
--   SELECT JSON_VALUE(user_data, '$.name') AS name FROM users;
-- SQLite:
--   SELECT json_extract(user_data, '$.name') AS name FROM users;

-- Example 2: Filter rows by JSON value
-- MySQL:
--   SELECT * FROM orders WHERE JSON_EXTRACT(metadata, '$.priority') = 'high';
-- PostgreSQL:
--   SELECT * FROM orders WHERE metadata->>'priority' = 'high';
-- SQL Server:
--   SELECT * FROM orders WHERE JSON_VALUE(metadata, '$.priority') = 'high';
-- SQLite:
--   SELECT * FROM orders WHERE json_extract(metadata, '$.priority') = 'high';

-- Example 3: Update JSON field
-- MySQL:
--   UPDATE users SET settings = JSON_SET(settings, '$.theme', 'dark') WHERE id = 1;
-- PostgreSQL:
--   UPDATE users SET settings = jsonb_set(settings, '{theme}', '"dark"'::jsonb) WHERE id = 1;
-- SQL Server:
--   UPDATE users SET settings = JSON_MODIFY(settings, '$.theme', 'dark') WHERE id = 1;
-- SQLite:
--   UPDATE users SET settings = json_set(settings, '$.theme', 'dark') WHERE id = 1;

-- Example 4: Aggregate rows into JSON array
-- MySQL:
--   SELECT category, JSON_ARRAYAGG(product_name) AS products FROM products GROUP BY category;
-- PostgreSQL:
--   SELECT category, json_agg(product_name) AS products FROM products GROUP BY category;
-- SQL Server:
--   SELECT category, STRING_AGG(product_name, ',') AS products FROM products GROUP BY category;
-- SQLite:
--   SELECT category, json_group_array(product_name) AS products FROM products GROUP BY category;

-- Example 5: Create JSON object from table columns
-- MySQL:
--   SELECT JSON_OBJECT('id', id, 'name', name, 'email', email) AS user_json FROM users;
-- PostgreSQL:
--   SELECT json_build_object('id', id, 'name', name, 'email', email) AS user_json FROM users;
-- SQLite:
--   SELECT json_object('id', id, 'name', name, 'email', email) AS user_json FROM users;

-- Example 6: Extract nested JSON value
-- MySQL:
--   SELECT JSON_EXTRACT(data, '$.user.profile.settings.theme') AS theme FROM records;
-- PostgreSQL:
--   SELECT data#>>'{user,profile,settings,theme}' AS theme FROM records;
-- SQL Server:
--   SELECT JSON_VALUE(data, '$.user.profile.settings.theme') AS theme FROM records;
-- SQLite:
--   SELECT json_extract(data, '$.user.profile.settings.theme') AS theme FROM records;

-- Example 7: Check if JSON array contains a tag
-- MySQL:
--   SELECT * FROM posts WHERE JSON_CONTAINS(tags, '"javascript"', '$');
-- PostgreSQL:
--   SELECT * FROM posts WHERE tags @> '"javascript"'::jsonb;
-- SQL Server:
--   SELECT * FROM posts WHERE EXISTS (SELECT 1 FROM OPENJSON(tags) WHERE value = 'javascript');
-- SQLite:
--   SELECT * FROM posts WHERE json_extract(tags, '$') LIKE '%javascript%';

-- Example 8: Parse JSON array into rows (OPENJSON equivalent)
-- MySQL:
--   SELECT jt.value AS item FROM JSON_TABLE('[1,2,3]', '$[*]' COLUMNS(value INT PATH '$')) AS jt;
-- PostgreSQL:
--   SELECT json_array_elements('[1,2,3]'::json) AS item;
-- SQL Server:
--   SELECT value FROM OPENJSON('[1,2,3]');
-- SQLite:
--   SELECT value FROM json_each('[1,2,3]');

-- ============================================================================
-- SECTION 13: JSON PATH SYNTAX REFERENCE
-- ============================================================================

-- MySQL JSON Path Syntax:
--   $        - Root of the document
--   $.key    - Value of object member "key"
--   $[n]     - Value of array element at index n (0-based)
--   $[*]     - All elements of an array
--   $.path.to.key - Nested path navigation
--   $.**     - All paths (wildcard)

-- PostgreSQL JSON Path Operators:
--   ->       - Get JSON element by key (returns JSON)
--   ->>      - Get JSON element by key (returns text)
--   #>       - Get JSON element at path (returns JSON)
--   #>>      - Get JSON element at path (returns text)
--   @>       - Contains check (jsonb only)
--   ?        - Key exists check (jsonb only)

-- SQL Server JSON Path Syntax:
--   $        - Root of the document
--   $.key    - Value of object member "key"
--   $[n]     - Value of array element at index n
--   $.path.to.key - Nested path
--   strict   - Strict mode (error if path not found)
--   lax      - Lax mode (returns NULL if not found) - default

-- SQLite JSON Functions:
--   json(json)         - Parse JSON
--   json_extract()     - Extract value by path
--   json_array_length  - Get array length
--   json_object()      - Create JSON object
--   json_array()       - Create JSON array
--   json_set()         - Insert/update value
--   json_remove()      - Remove value
--   json_type()        - Get JSON type
--   json_valid()       - Validate JSON
--   json_each()        - Iterate over JSON elements
--   json_tree()        - Recursive JSON traversal

-- ============================================================================
-- END OF MODULE
-- ============================================================================