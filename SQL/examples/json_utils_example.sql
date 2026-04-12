-- ============================================================================
-- SQL JSON Utilities - Usage Examples
-- ============================================================================
-- Practical examples demonstrating JSON utility functions across different
-- database systems (MySQL, PostgreSQL, SQL Server, SQLite).
-- ============================================================================

-- ============================================================================
-- EXAMPLE 1: STORE USER DATA AS JSON
-- ============================================================================

-- Create table with JSON column
CREATE TABLE IF NOT EXISTS users_json (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    profile JSON,
    settings JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert user with JSON profile
INSERT INTO users_json (username, profile, settings) VALUES
('alice', 
    '{"name": "Alice Smith", "email": "alice@example.com", "age": 28, "location": {"city": "NYC", "country": "USA"}}',
    '{"theme": "dark", "notifications": {"email": true, "push": false}, "language": "en"}'
),
('bob',
    '{"name": "Bob Jones", "email": "bob@example.com", "age": 35, "location": {"city": "London", "country": "UK"}}',
    '{"theme": "light", "notifications": {"email": true, "push": true}, "language": "en-GB"}'
),
('charlie',
    '{"name": "Charlie Brown", "email": "charlie@example.com", "age": 42, "tags": ["developer", "manager", "remote"]}',
    '{"theme": "auto", "notifications": {"email": false, "push": true}}'
);

-- ============================================================================
-- EXAMPLE 2: EXTRACT VALUES FROM JSON
-- ============================================================================

-- MySQL: Extract user name from profile
SELECT 
    username,
    JSON_UNQUOTE(JSON_EXTRACT(profile, '$.name')) AS full_name,
    JSON_UNQUOTE(JSON_EXTRACT(profile, '$.email')) AS email,
    JSON_EXTRACT(profile, '$.age') AS age
FROM users_json;

-- MySQL: Extract nested location values
SELECT 
    username,
    JSON_UNQUOTE(JSON_EXTRACT(profile, '$.location.city')) AS city,
    JSON_UNQUOTE(JSON_EXTRACT(profile, '$.location.country')) AS country
FROM users_json;

-- MySQL: Extract settings values
SELECT 
    username,
    JSON_UNQUOTE(JSON_EXTRACT(settings, '$.theme')) AS theme,
    JSON_EXTRACT(settings, '$.notifications.email') AS email_notifications
FROM users_json;

-- PostgreSQL equivalents:
/*
SELECT 
    username,
    profile->>'name' AS full_name,
    profile->>'email' AS email,
    (profile->>'age')::int AS age
FROM users_json;

SELECT 
    username,
    profile#>>'{location,city}' AS city,
    profile#>>'{location,country}' AS country
FROM users_json;
*/

-- SQL Server equivalents:
/*
SELECT 
    username,
    JSON_VALUE(profile, '$.name') AS full_name,
    JSON_VALUE(profile, '$.email') AS email,
    JSON_VALUE(profile, '$.age') AS age
FROM users_json;

SELECT 
    username,
    JSON_VALUE(profile, '$.location.city') AS city,
    JSON_VALUE(profile, '$.location.country') AS country
FROM users_json;
*/

-- SQLite equivalents:
/*
SELECT 
    username,
    json_extract(profile, '$.name') AS full_name,
    json_extract(profile, '$.email') AS email,
    json_extract(profile, '$.age') AS age
FROM users_json;
*/

-- ============================================================================
-- EXAMPLE 3: USING CUSTOM FUNCTIONS
-- ============================================================================

-- Use json_get_string for cleaner syntax
SELECT 
    username,
    json_get_string(profile, 'name') AS full_name,
    json_get_string(profile, 'email') AS email,
    json_get_number(profile, 'age') AS age
FROM users_json;

-- Check if key exists
SELECT 
    username,
    json_has_key(profile, 'tags') AS has_tags,
    json_has_key(profile, 'location') AS has_location
FROM users_json;

-- Extract and check array elements
SELECT 
    username,
    json_array_element(profile, 1) AS first_tag,
    json_array_contains(profile, 'developer') AS is_developer
FROM users_json
WHERE json_has_key(profile, 'tags');

-- ============================================================================
-- EXAMPLE 4: FILTER BY JSON VALUES
-- ============================================================================

-- Filter users by theme setting
SELECT username, settings
FROM users_json
WHERE JSON_EXTRACT(settings, '$.theme') = 'dark';

-- Filter by nested boolean value
SELECT username
FROM users_json
WHERE JSON_EXTRACT(settings, '$.notifications.push') = true;

-- Filter by age range
SELECT username, JSON_UNQUOTE(JSON_EXTRACT(profile, '$.name')) AS name
FROM users_json
WHERE JSON_EXTRACT(profile, '$.age') >= 30;

-- Filter users with specific tag
SELECT username
FROM users_json
WHERE JSON_CONTAINS(JSON_EXTRACT(profile, '$.tags'), '"developer"');

-- ============================================================================
-- EXAMPLE 5: UPDATE JSON VALUES
-- ============================================================================

-- Update theme setting
UPDATE users_json
SET settings = JSON_SET(settings, '$.theme', 'light')
WHERE username = 'alice';

-- Add new key to profile
UPDATE users_json
SET profile = JSON_SET(profile, '$.verified', true)
WHERE username = 'bob';

-- Remove a setting
UPDATE users_json
SET settings = JSON_REMOVE(settings, '$.language')
WHERE username = 'alice';

-- Update nested value
UPDATE users_json
SET settings = JSON_SET(settings, '$.notifications.push', true)
WHERE username = 'alice';

-- Verify updates
SELECT username, profile, settings FROM users_json;

-- ============================================================================
-- EXAMPLE 6: JSON AGGREGATION
-- ============================================================================

-- Create orders table with JSON items
CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    items JSON,
    total DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO orders (customer_id, items, total) VALUES
(1, '[{"product": "Widget", "price": 10.00, "qty": 5}, {"product": "Gadget", "price": 25.00, "qty": 2}]', 100.00),
(2, '[{"product": "Widget", "price": 10.00, "qty": 3}, {"product": "Tool", "price": 15.00, "qty": 1}]', 45.00),
(1, '[{"product": "Gadget", "price": 25.00, "qty": 1}]', 25.00);

-- Aggregate customer names into JSON array
SELECT 
    JSON_ARRAYAGG(username) AS all_users
FROM users_json;

-- Group by and create JSON object
SELECT 
    JSON_OBJECTAGG(username, JSON_EXTRACT(profile, '$.age')) AS user_ages
FROM users_json;

-- ============================================================================
-- EXAMPLE 7: JSON MERGING AND COMBINATION
-- ============================================================================

-- Merge two settings objects
SELECT 
    JSON_MERGE_PATCH(
        '{"theme": "dark", "fontSize": 14}',
        '{"fontSize": 16, "notifications": true}'
    ) AS merged_settings;

-- Combine default and user settings
SET @default_settings = '{"theme": "light", "language": "en", "fontSize": 12}';
SET @user_settings = '{"theme": "dark"}';

SELECT 
    JSON_MERGE_PATCH(@default_settings, @user_settings) AS final_settings;

-- ============================================================================
-- EXAMPLE 8: JSON CREATION FROM DATA
-- ============================================================================

-- Create JSON from table data
SELECT 
    JSON_OBJECT(
        'id', id,
        'username', username,
        'profile', profile
    ) AS user_json
FROM users_json
LIMIT 2;

-- Create JSON array from column values
SELECT 
    JSON_ARRAY(username, JSON_UNQUOTE(JSON_EXTRACT(profile, '$.name'))) AS user_info
FROM users_json;

-- Build nested JSON
SELECT 
    JSON_OBJECT(
        'user', JSON_OBJECT(
            'id', id,
            'name', JSON_UNQUOTE(JSON_EXTRACT(profile, '$.name'))
        ),
        'settings', settings
    ) AS full_record
FROM users_json
WHERE username = 'alice';

-- ============================================================================
-- EXAMPLE 9: WORKING WITH JSON ARRAYS
-- ============================================================================

-- Create products table with JSON attributes
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    attributes JSON,
    tags JSON
);

INSERT INTO products (name, attributes, tags) VALUES
('Laptop', '{"specs": {"cpu": "Intel i7", "ram": 16, "storage": 512}, "colors": ["silver", "black"]}', '["electronics", "computer", "premium"]'),
('Phone', '{"specs": {"cpu": "Apple A15", "ram": 8, "storage": 128}, "colors": ["white", "black", "blue"]}', '["electronics", "mobile", "popular"]');

-- Get array length
SELECT 
    name,
    JSON_LENGTH(tags) AS tag_count,
    JSON_LENGTH(JSON_EXTRACT(attributes, '$.colors')) AS color_count
FROM products;

-- Extract array elements
SELECT 
    name,
    JSON_UNQUOTE(JSON_EXTRACT(tags, '$[0]')) AS first_tag,
    JSON_UNQUOTE(JSON_EXTRACT(tags, '$[1]')) AS second_tag
FROM products;

-- Check if array contains value
SELECT 
    name,
    JSON_CONTAINS(tags, '"electronics"') AS is_electronics,
    JSON_CONTAINS(tags, '"premium"') AS is_premium
FROM products;

-- Append to array
UPDATE products
SET tags = JSON_ARRAY_APPEND(tags, '$', 'new-arrival')
WHERE name = 'Laptop';

SELECT name, tags FROM products;

-- ============================================================================
-- EXAMPLE 10: PRACTICAL E-COMMERCE SCENARIO
-- ============================================================================

-- Complete order processing example
CREATE TABLE IF NOT EXISTS ecommerce_orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_number VARCHAR(50),
    customer JSON,
    items JSON,
    shipping JSON,
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert complete order
INSERT INTO ecommerce_orders (order_number, customer, items, shipping, status) VALUES
('ORD-2024-001',
    '{"id": 1001, "name": "John Doe", "email": "john@example.com", "phone": "+1-555-0100"}',
    '[{"sku": "WIDGET-001", "name": "Widget", "price": 25.00, "qty": 2}, {"sku": "GADGET-002", "name": "Gadget", "price": 50.00, "qty": 1}]',
    '{"method": "express", "address": {"street": "123 Main St", "city": "NYC", "zip": "10001"}}',
    'pending'
);

-- Calculate order total from items array
SELECT 
    order_number,
    JSON_UNQUOTE(JSON_EXTRACT(customer, '$.name')) AS customer_name,
    -- Sum up item prices * quantities (using custom logic)
    (
        JSON_EXTRACT(items, '$[0].price') * JSON_EXTRACT(items, '$[0].qty') +
        JSON_EXTRACT(items, '$[1].price') * JSON_EXTRACT(items, '$[1].qty')
    ) AS calculated_total
FROM ecommerce_orders;

-- Get shipping details
SELECT 
    order_number,
    JSON_UNQUOTE(JSON_EXTRACT(shipping, '$.method')) AS shipping_method,
    JSON_UNQUOTE(JSON_EXTRACT(shipping, '$.address.city')) AS shipping_city
FROM ecommerce_orders;

-- Update order status and add tracking
UPDATE ecommerce_orders
SET 
    status = 'shipped',
    shipping = JSON_SET(shipping, '$.tracking', 'TRK123456')
WHERE order_number = 'ORD-2024-001';

SELECT 
    order_number,
    status,
    JSON_UNQUOTE(JSON_EXTRACT(shipping, '$.tracking')) AS tracking_number
FROM ecommerce_orders;

-- ============================================================================
-- EXAMPLE 11: JSON VALIDATION AND ERROR HANDLING
-- ============================================================================

-- Validate JSON before processing
SELECT 
    id,
    username,
    CASE 
        WHEN JSON_VALID(profile) = 1 THEN 'Valid'
        ELSE 'Invalid'
    END AS profile_status,
    CASE 
        WHEN JSON_VALID(settings) = 1 THEN 'Valid'
        ELSE 'Invalid'
    END AS settings_status
FROM users_json;

-- Safe extraction with fallback
SELECT 
    username,
    COALESCE(
        JSON_UNQUOTE(JSON_EXTRACT(profile, '$.nickname')),
        JSON_UNQUOTE(JSON_EXTRACT(profile, '$.name')),
        'Unknown'
    ) AS display_name
FROM users_json;

-- ============================================================================
-- EXAMPLE 12: PRETTY PRINTING FOR DISPLAY
-- ============================================================================

-- Format JSON for readability
SELECT 
    username,
    JSON_PRETTY(profile) AS formatted_profile
FROM users_json
WHERE username = 'alice';

-- Pretty print complex JSON
SELECT JSON_PRETTY(
    '{"user": {"profile": {"name": "Alice", "settings": {"theme": "dark", "notifications": true}}}}'
) AS formatted;

-- ============================================================================
-- EXAMPLE 13: SEARCH IN JSON
-- ============================================================================

-- Find path to a value
SELECT 
    JSON_SEARCH(profile, 'one', 'Alice') AS found_path
FROM users_json;

-- Find all paths containing a value
SELECT 
    JSON_SEARCH(settings, 'all', 'true') AS all_true_paths
FROM users_json;

-- ============================================================================
-- CLEANUP
-- ============================================================================

-- Drop example tables (when done)
-- DROP TABLE IF EXISTS users_json;
-- DROP TABLE IF EXISTS orders;
-- DROP TABLE IF EXISTS products;
-- DROP TABLE IF EXISTS ecommerce_orders;

-- ============================================================================
-- END OF EXAMPLES
-- ============================================================================