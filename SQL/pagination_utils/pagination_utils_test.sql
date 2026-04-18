-- ============================================================================
-- SQL Pagination Utilities Test Suite
-- ============================================================================
-- Test cases for pagination utilities module.
-- Each test is designed to work with MySQL, PostgreSQL, SQL Server, and SQLite.
--
-- Test Categories:
--   1. Basic Pagination Tests
--   2. Keyset/Cursor Pagination Tests
--   3. Pagination Metadata Tests
--   4. Pagination with Filtering Tests
--   5. Pagination with Sorting Tests
--   6. Pagination with Total Count Tests
--   7. Deep Pagination Tests
--   8. Seek Method Tests
--   9. Row Numbering Tests
--   10. Edge Case Tests
--
-- Author: AllToolkit
-- License: MIT
-- ============================================================================

-- ============================================================================
-- SECTION 1: TEST SETUP - Create sample tables
-- ============================================================================

-- MySQL:
/*
CREATE TABLE IF NOT EXISTS test_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    score INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS test_posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    author_id INT,
    status VARCHAR(20) DEFAULT 'draft',
    views INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_created_at (created_at)
);

-- Insert test data
INSERT INTO test_users (name, email, score, status) VALUES
    ('User1', 'user1@test.com', 100, 'active'),
    ('User2', 'user2@test.com', 90, 'active'),
    ('User3', 'user3@test.com', 80, 'inactive'),
    ('User4', 'user4@test.com', 70, 'active'),
    ('User5', 'user5@test.com', 60, 'active'),
    ('User6', 'user6@test.com', 50, 'inactive'),
    ('User7', 'user7@test.com', 40, 'active'),
    ('User8', 'user8@test.com', 30, 'active'),
    ('User9', 'user9@test.com', 20, 'inactive'),
    ('User10', 'user10@test.com', 10, 'active');
*/

-- PostgreSQL:
/*
CREATE TABLE IF NOT EXISTS test_users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    score INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS test_posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    author_id INTEGER,
    status VARCHAR(20) DEFAULT 'draft',
    views INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_created_at ON test_posts(created_at);

-- Insert test data
INSERT INTO test_users (name, email, score, status) VALUES
    ('User1', 'user1@test.com', 100, 'active'),
    ('User2', 'user2@test.com', 90, 'active'),
    ('User3', 'user3@test.com', 80, 'inactive'),
    ('User4', 'user4@test.com', 70, 'active'),
    ('User5', 'user5@test.com', 60, 'active'),
    ('User6', 'user6@test.com', 50, 'inactive'),
    ('User7', 'user7@test.com', 40, 'active'),
    ('User8', 'user8@test.com', 30, 'active'),
    ('User9', 'user9@test.com', 20, 'inactive'),
    ('User10', 'user10@test.com', 10, 'active');
*/

-- SQL Server:
/*
CREATE TABLE test_users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    score INT DEFAULT 0,
    created_at DATETIME DEFAULT GETDATE()
);

CREATE TABLE test_posts (
    id INT IDENTITY(1,1) PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content NVARCHAR(MAX),
    author_id INT,
    status VARCHAR(20) DEFAULT 'draft',
    views INT DEFAULT 0,
    created_at DATETIME DEFAULT GETDATE()
);

CREATE INDEX idx_created_at ON test_posts(created_at);

-- Insert test data
INSERT INTO test_users (name, email, score, status) VALUES
    ('User1', 'user1@test.com', 100, 'active'),
    ('User2', 'user2@test.com', 90, 'active'),
    ('User3', 'user3@test.com', 80, 'inactive'),
    ('User4', 'user4@test.com', 70, 'active'),
    ('User5', 'user5@test.com', 60, 'active'),
    ('User6', 'user6@test.com', 50, 'inactive'),
    ('User7', 'user7@test.com', 40, 'active'),
    ('User8', 'user8@test.com', 30, 'active'),
    ('User9', 'user9@test.com', 20, 'inactive'),
    ('User10', 'user10@test.com', 10, 'active');
*/

-- SQLite:
/*
CREATE TABLE IF NOT EXISTS test_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    status TEXT DEFAULT 'active',
    score INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS test_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT,
    author_id INTEGER,
    status TEXT DEFAULT 'draft',
    views INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_created_at ON test_posts(created_at);

-- Insert test data
INSERT INTO test_users (name, email, score, status) VALUES
    ('User1', 'user1@test.com', 100, 'active'),
    ('User2', 'user2@test.com', 90, 'active'),
    ('User3', 'user3@test.com', 80, 'inactive'),
    ('User4', 'user4@test.com', 70, 'active'),
    ('User5', 'user5@test.com', 60, 'active'),
    ('User6', 'user6@test.com', 50, 'inactive'),
    ('User7', 'user7@test.com', 40, 'active'),
    ('User8', 'user8@test.com', 30, 'active'),
    ('User9', 'user9@test.com', 20, 'inactive'),
    ('User10', 'user10@test.com', 10, 'active');
*/

-- ============================================================================
-- SECTION 2: BASIC PAGINATION TESTS (Test Cases 1-10)
-- ============================================================================

-- Test 1: First page with 5 items
-- Expected: Returns first 5 users ordered by id
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users ORDER BY id LIMIT 5 OFFSET 0;
-- Expected: id = 1, 2, 3, 4, 5

-- Test 2: Second page with 5 items
-- Expected: Returns users 6-10
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users ORDER BY id LIMIT 5 OFFSET 5;
-- Expected: id = 6, 7, 8, 9, 10

-- Test 3: Third page with 5 items (empty result)
-- Expected: Returns empty set
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users ORDER BY id LIMIT 5 OFFSET 10;
-- Expected: 0 rows

-- Test 4: SQL Server style pagination
-- Expected: Returns first 5 users
-- SQL Server:
--   SELECT * FROM test_users ORDER BY id OFFSET 0 ROWS FETCH NEXT 5 ROWS ONLY;
-- Expected: id = 1, 2, 3, 4, 5

-- Test 5: Pagination with page size larger than total items
-- Expected: Returns all 10 users
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users ORDER BY id LIMIT 20 OFFSET 0;
-- Expected: All 10 users

-- Test 6: Pagination with zero offset
-- Expected: Returns first 5 users
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users ORDER BY id LIMIT 5;
-- Expected: id = 1, 2, 3, 4, 5

-- Test 7: Pagination with different order (DESC)
-- Expected: Returns last 5 users in reverse order
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users ORDER BY id DESC LIMIT 5;
-- Expected: id = 10, 9, 8, 7, 6

-- Test 8: Pagination sorted by score
-- Expected: Returns top 5 users by score
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users ORDER BY score DESC LIMIT 5;
-- Expected: scores = 100, 90, 80, 70, 60

-- Test 9: Pagination sorted by multiple columns
-- Expected: Sorted by status then by score DESC
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users ORDER BY status, score DESC LIMIT 5;
-- Expected: active users first, sorted by score

-- Test 10: Pagination without ORDER BY (unpredictable but valid)
-- Expected: Returns some 5 users
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users LIMIT 5;

-- ============================================================================
-- SECTION 3: KEYSET/CURSOR PAGINATION TESTS (Test Cases 11-20)
-- ============================================================================

-- Test 11: Keyset pagination - first page
-- Expected: Returns first 5 users
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users WHERE id > 0 ORDER BY id LIMIT 5;
-- Expected: id = 1, 2, 3, 4, 5

-- Test 12: Keyset pagination - second page (after id=5)
-- Expected: Returns users 6-10
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users WHERE id > 5 ORDER BY id LIMIT 5;
-- Expected: id = 6, 7, 8, 9, 10

-- Test 13: Keyset pagination - beyond last item
-- Expected: Returns empty set
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users WHERE id > 10 ORDER BY id LIMIT 5;
-- Expected: 0 rows

-- Test 14: Keyset pagination DESC order - first page
-- Expected: Returns highest IDs first
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users WHERE id < 100 ORDER BY id DESC LIMIT 5;
-- Expected: id = 10, 9, 8, 7, 6

-- Test 15: Keyset pagination DESC - next page (before id=6)
-- Expected: Returns id 5-1 in DESC order
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users WHERE id < 6 ORDER BY id DESC LIMIT 5;
-- Expected: id = 5, 4, 3, 2, 1

-- Test 16: Keyset pagination with filtering
-- Expected: Active users only, paginated
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users WHERE status = 'active' AND id > 0 ORDER BY id LIMIT 3;
-- Expected: active users only

-- Test 17: Keyset pagination with score-based cursor
-- Expected: Users with score < 100
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users WHERE score < 100 ORDER BY score DESC LIMIT 5;
-- Expected: scores = 90, 80, 70, 60, 50

-- Test 18: Keyset pagination - next page after score=50
-- Expected: Users with score < 50
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users WHERE score < 50 ORDER BY score DESC LIMIT 5;
-- Expected: scores = 40, 30, 20, 10

-- Test 19: Keyset pagination with composite key
-- Expected: Paginated by status + id
-- MySQL 8.0.2+/PostgreSQL:
--   SELECT * FROM test_users WHERE (status, id) > ('active', 0) ORDER BY status, id LIMIT 5;

-- Test 20: Keyset pagination bidirectional - get items before cursor
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM (
--     SELECT * FROM test_users WHERE id < 6 ORDER BY id DESC LIMIT 5
--   ) sub ORDER BY id ASC;
-- Expected: id = 1, 2, 3, 4, 5

-- ============================================================================
-- SECTION 4: PAGINATION METADATA TESTS (Test Cases 21-30)
-- ============================================================================

-- Test 21: Calculate total items
-- Expected: Returns 10
-- MySQL/PostgreSQL/SQLite/SQL Server:
--   SELECT COUNT(*) AS total_items FROM test_users;
-- Expected: 10

-- Test 22: Calculate total pages (10 items, 5 per page)
-- Expected: Returns 2 pages
-- MySQL:
--   SELECT CEIL(COUNT(*) / 5.0) AS total_pages FROM test_users;
-- PostgreSQL:
--   SELECT CEILING(COUNT(*)::DECIMAL / 5) AS total_pages FROM test_users;
-- SQL Server:
--   SELECT CEILING(COUNT(*) * 1.0 / 5) AS total_pages FROM test_users;
-- SQLite:
--   SELECT CAST(CEIL(COUNT(*) * 1.0 / 5) AS INTEGER) AS total_pages FROM test_users;
-- Expected: 2

-- Test 23: Calculate total pages (10 items, 3 per page)
-- Expected: Returns 4 pages (ceil(10/3) = 4)
-- MySQL:
--   SELECT CEIL(COUNT(*) / 3.0) AS total_pages FROM test_users;
-- Expected: 4

-- Test 24: Calculate offset for page 3 (10 items per page)
-- Expected: Returns 20
-- Formula: (page - 1) * page_size = (3 - 1) * 10 = 20

-- Test 25: Check if page exists
-- Expected: Page 3 with 5 items does not exist
-- MySQL/PostgreSQL/SQLite:
--   SELECT CASE WHEN (SELECT COUNT(*) FROM test_users) > 10 THEN 1 ELSE 0 END AS page_exists;
-- Expected: 0

-- Test 26: Pagination metadata in one query
-- MySQL 8.0+/PostgreSQL:
--   SELECT 
--     COUNT(*) AS total_items,
--     CEILING(COUNT(*)::DECIMAL / 5) AS total_pages,
--     5 AS items_per_page
--   FROM test_users;

-- Test 27: Check if current page is last page
-- Expected: Page 2 of 2 is last page
-- MySQL:
--   SELECT CASE WHEN 2 >= CEIL(COUNT(*) / 5.0) THEN 1 ELSE 0 END AS is_last_page FROM test_users;

-- Test 28: Check if current page is first page
-- Expected: Page 1 is first page
-- MySQL:
--   SELECT CASE WHEN 1 = 1 THEN 1 ELSE 0 END AS is_first_page FROM dual;

-- Test 29: Calculate remaining items after current page
-- Expected: After page 1 (5 items), 5 items remain
-- MySQL:
--   SELECT COUNT(*) - 5 AS remaining_items FROM test_users;

-- Test 30: Calculate next page number
-- Expected: Next page after page 1 is 2
-- MySQL:
--   SELECT CASE WHEN 1 < CEIL(COUNT(*) / 5.0) THEN 2 ELSE NULL END AS next_page FROM test_users;

-- ============================================================================
-- SECTION 5: PAGINATION WITH FILTERING TESTS (Test Cases 31-40)
-- ============================================================================

-- Test 31: Filter pagination - active users only
-- Expected: Returns active users paginated
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users WHERE status = 'active' ORDER BY id LIMIT 3;
-- Expected: 7 active users (User1, User2, User4, User5, User7, User8, User10)

-- Test 32: Filter pagination with total count
-- Expected: Returns 7 active users total
-- MySQL/PostgreSQL/SQLite:
--   SELECT COUNT(*) AS total FROM test_users WHERE status = 'active';
-- Expected: 7

-- Test 33: Filter pagination - second page of active users
-- Expected: Returns next 3 active users
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users WHERE status = 'active' ORDER BY id LIMIT 3 OFFSET 3;

-- Test 34: Filter with multiple conditions
-- Expected: Active users with score >= 50
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users WHERE status = 'active' AND score >= 50 ORDER BY score DESC LIMIT 5;
-- Expected: User1(100), User2(90), User4(70), User5(60)

-- Test 35: Filter with range condition
-- Expected: Users with score between 40 and 80
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users WHERE score BETWEEN 40 AND 80 ORDER BY score LIMIT 5;
-- Expected: User7(40), User6(50), User5(60), User4(70), User3(80)

-- Test 36: Filter with LIKE condition
-- Expected: Users with email containing 'test'
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users WHERE email LIKE '%test%' ORDER BY id LIMIT 5;
-- Expected: All users match

-- Test 37: Filter with IN condition
-- Expected: Users with specific statuses
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users WHERE status IN ('active', 'pending') ORDER BY id LIMIT 5;

-- Test 38: Filter pagination - empty result
-- Expected: No users match condition
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users WHERE score > 200 ORDER BY id LIMIT 5;
-- Expected: 0 rows

-- Test 39: Filter pagination with sort
-- Expected: Active users sorted by score DESC
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users WHERE status = 'active' ORDER BY score DESC LIMIT 5;
-- Expected: User1(100), User2(90), User4(70), User5(60), User7(40)

-- Test 40: Keyset pagination with filter
-- Expected: Active users after id=4
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users WHERE status = 'active' AND id > 4 ORDER BY id LIMIT 5;
-- Expected: Active users with id > 4

-- ============================================================================
-- SECTION 6: PAGINATION WITH TOTAL COUNT TESTS (Test Cases 41-50)
-- ============================================================================

-- Test 41: Window function total count
-- MySQL 8.0+/PostgreSQL:
--   SELECT *, COUNT(*) OVER() AS total_count FROM test_users ORDER BY id LIMIT 5;
-- Expected: Each row has total_count = 10

-- Test 42: Total count with filter
-- MySQL 8.0+/PostgreSQL:
--   SELECT *, COUNT(*) OVER() AS total_count FROM test_users WHERE status = 'active' ORDER BY id LIMIT 5;
-- Expected: Each row has total_count = 7

-- Test 43: Combined query for page + total
-- MySQL:
--   SELECT 
--     (SELECT COUNT(*) FROM test_users) AS total_count,
--     (SELECT JSON_ARRAYAGG(JSON_OBJECT('id', id, 'name', name)) FROM (
--       SELECT id, name FROM test_users ORDER BY id LIMIT 5
--     ) sub) AS items;
-- PostgreSQL:
--   SELECT 
--     (SELECT COUNT(*) FROM test_users) AS total_count,
--     json_agg(json_build_object('id', id, 'name', name)) AS items
--   FROM (SELECT id, name FROM test_users ORDER BY id LIMIT 5) sub;

-- Test 44: Total count for filtered pagination
-- MySQL:
--   SELECT COUNT(*) AS total FROM test_users WHERE status = 'active';
--   SELECT * FROM test_users WHERE status = 'active' ORDER BY id LIMIT 5 OFFSET 0;

-- Test 45: Has_more indicator
-- MySQL:
--   SELECT CASE WHEN (SELECT COUNT(*) FROM test_users) > 5 THEN 1 ELSE 0 END AS has_more;
-- Expected: 1 (more items exist)

-- Test 46: Remaining pages calculation
-- MySQL:
--   SELECT CEIL(COUNT(*) / 5.0) - 1 AS remaining_pages FROM test_users;
-- Expected: 1 remaining page after page 1

-- Test 47: Pagination with estimated count
-- PostgreSQL:
--   SELECT reltuples::BIGINT AS estimate FROM pg_class WHERE relname = 'test_users';

-- Test 48: Count distinct values in pagination
-- MySQL:
--   SELECT COUNT(DISTINCT status) AS unique_statuses FROM test_users;
-- Expected: 2 (active, inactive)

-- Test 49: Group count with pagination
-- MySQL:
--   SELECT status, COUNT(*) AS count FROM test_users GROUP BY status ORDER BY status LIMIT 10;
-- Expected: active=7, inactive=3

-- Test 50: Running total in pagination
-- MySQL 8.0+:
--   SELECT id, name, score, SUM(score) OVER (ORDER BY id) AS running_total FROM test_users LIMIT 5;

-- ============================================================================
-- SECTION 7: DEEP PAGINATION TESTS (Test Cases 51-60)
-- ============================================================================

-- Test 51: Simulate deep pagination (requires more data)
-- Insert additional test data for deep pagination testing
/*
-- Insert 1000 more users for deep pagination test
INSERT INTO test_users (name, email, score, status)
SELECT 
    CONCAT('User', n + 10),
    CONCAT('user', n + 10, '@test.com'),
    (100 - n % 100),
    CASE WHEN n % 3 = 0 THEN 'inactive' ELSE 'active' END
FROM (
    SELECT ROW_NUMBER() OVER () AS n FROM information_schema.columns LIMIT 1000
) nums;
*/

-- Test 52: Deep pagination with OFFSET
-- MySQL:
--   SELECT * FROM test_users ORDER BY id LIMIT 10 OFFSET 500;

-- Test 53: Deep pagination optimization - JOIN method
-- MySQL:
--   SELECT u.* FROM test_users u
--   INNER JOIN (SELECT id FROM test_users ORDER BY id LIMIT 10 OFFSET 500) AS tmp
--   ON u.id = tmp.id;

-- Test 54: Keyset pagination for deep pages (fast)
-- MySQL:
--   SELECT * FROM test_users WHERE id > 500 ORDER BY id LIMIT 10;

-- Test 55: Compare OFFSET vs keyset performance
-- Run both and compare execution time
-- OFFSET method:
--   SELECT * FROM test_users ORDER BY id LIMIT 10 OFFSET 500;
-- Keyset method:
--   SELECT * FROM test_users WHERE id > 500 ORDER BY id LIMIT 10;

-- Test 56: Deep pagination with filter
-- MySQL:
--   SELECT * FROM test_users WHERE status = 'active' ORDER BY id LIMIT 10 OFFSET 250;

-- Test 57: Deep keyset pagination with filter
-- MySQL:
--   SELECT * FROM test_users WHERE status = 'active' AND id > 250 ORDER BY id LIMIT 10;

-- Test 58: Deep pagination with subquery optimization
-- MySQL 8.0+:
--   WITH FilteredIDs AS (
--     SELECT id FROM test_users WHERE status = 'active' ORDER BY id LIMIT 10 OFFSET 250
--   )
--   SELECT u.* FROM test_users u JOIN FilteredIDs f ON u.id = f.id;

-- Test 59: Estimate count for large table
-- MySQL:
--   SELECT TABLE_ROWS FROM information_schema.TABLES WHERE TABLE_NAME = 'test_users';

-- Test 60: Deep pagination with ROW_NUMBER
-- MySQL 8.0+:
--   WITH NumberedRows AS (
--     SELECT *, ROW_NUMBER() OVER (ORDER BY id) AS rn FROM test_users
--   )
--   SELECT * FROM NumberedRows WHERE rn BETWEEN 501 AND 510;

-- ============================================================================
-- SECTION 8: ROW NUMBERING TESTS (Test Cases 61-70)
-- ============================================================================

-- Test 61: ROW_NUMBER basic usage
-- MySQL 8.0+/PostgreSQL/SQL Server/SQLite 3.25+:
--   SELECT *, ROW_NUMBER() OVER (ORDER BY id) AS row_num FROM test_users LIMIT 10;
-- Expected: row_num 1-10

-- Test 62: ROW_NUMBER with partitioning
-- MySQL 8.0+/PostgreSQL/SQL Server/SQLite 3.25+:
--   SELECT *, ROW_NUMBER() OVER (PARTITION BY status ORDER BY score DESC) AS row_num FROM test_users;
-- Expected: Each status group has its own row numbering

-- Test 63: RANK function
-- MySQL 8.0+/PostgreSQL/SQL Server/SQLite 3.25+:
--   SELECT *, RANK() OVER (ORDER BY score DESC) AS rank FROM test_users;
-- Expected: Ranks with ties (same score = same rank)

-- Test 64: DENSE_RANK function
-- MySQL 8.0+/PostgreSQL/SQL Server/SQLite 3.25+:
--   SELECT *, DENSE_RANK() OVER (ORDER BY score DESC) AS dense_rank FROM test_users;
-- Expected: Dense ranks (no gaps for ties)

-- Test 65: ROW_NUMBER for pagination filtering
-- MySQL 8.0+/PostgreSQL/SQL Server/SQLite 3.25+:
--   WITH Numbered AS (
--     SELECT *, ROW_NUMBER() OVER (ORDER BY score DESC) AS rn FROM test_users
--   )
--   SELECT * FROM Numbered WHERE rn BETWEEN 3 AND 5;
-- Expected: 3 rows (positions 3-5)

-- Test 66: ROW_NUMBER with complex ordering
-- MySQL 8.0+/PostgreSQL/SQL Server/SQLite 3.25+:
--   SELECT *, ROW_NUMBER() OVER (ORDER BY status DESC, score DESC) AS rn FROM test_users;

-- Test 67: ROW_NUMBER for deduplication
-- MySQL 8.0+/PostgreSQL:
--   WITH Ranked AS (
--     SELECT *, ROW_NUMBER() OVER (PARTITION BY email ORDER BY id) AS rn
--     FROM test_users
--   )
--   SELECT * FROM Ranked WHERE rn = 1;  -- Keep only first occurrence per email

-- Test 68: ROW_NUMBER for top N per group
-- MySQL 8.0+/PostgreSQL:
--   WITH Ranked AS (
--     SELECT *, ROW_NUMBER() OVER (PARTITION BY status ORDER BY score DESC) AS rn
--     FROM test_users
--   )
--   SELECT * FROM Ranked WHERE rn <= 2;  -- Top 2 per status

-- Test 69: ROW_NUMBER for nth item
-- MySQL 8.0+/PostgreSQL:
--   WITH Numbered AS (
--     SELECT *, ROW_NUMBER() OVER (ORDER BY score DESC) AS rn FROM test_users
--   )
--   SELECT * FROM Numbered WHERE rn = 5;  -- 5th highest score

-- Test 70: ROW_NUMBER with CTE pagination
-- MySQL 8.0+/PostgreSQL:
--   WITH Paginated AS (
--     SELECT *, ROW_NUMBER() OVER (ORDER BY id) AS rn,
--              COUNT(*) OVER() AS total_count
--     FROM test_users
--   )
--   SELECT * FROM Paginated WHERE rn BETWEEN 1 AND 5;

-- ============================================================================
-- SECTION 9: EDGE CASE TESTS (Test Cases 71-80)
-- ============================================================================

-- Test 71: Empty table pagination
-- Expected: Returns empty result
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_posts WHERE id > 1000 ORDER BY id LIMIT 10;
-- Expected: 0 rows

-- Test 72: Single row pagination
-- Expected: Returns one row
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users WHERE id = 1 ORDER BY id LIMIT 10;
-- Expected: 1 row

-- Test 73: Page size of 1
-- Expected: Returns one item
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users ORDER BY id LIMIT 1;
-- Expected: id = 1

-- Test 74: Negative offset (invalid, should error or return first page)
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users ORDER BY id LIMIT 5 OFFSET -1;
-- Expected: Error or treated as OFFSET 0

-- Test 75: Zero limit
-- Expected: Returns empty result
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users ORDER BY id LIMIT 0;
-- Expected: 0 rows (MySQL returns empty, PostgreSQL returns 0 rows)

-- Test 76: NULL values in sort column
-- Expected: NULLs sorted first or last depending on database
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_posts ORDER BY views DESC LIMIT 5;
-- Note: NULL handling varies by database

-- Test 77: Pagination with duplicate sort values
-- Expected: Predictable secondary sort needed
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users ORDER BY status LIMIT 5;
-- Expected: Add secondary sort (id) for predictability

-- Test 78: Pagination with non-integer offset
-- Expected: Converted to integer or error
-- MySQL:
--   SELECT * FROM test_users ORDER BY id LIMIT 5 OFFSET 0.5;
-- Expected: Rounded or error

-- Test 79: Very large limit value
-- Expected: Returns all available rows
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users ORDER BY id LIMIT 999999999;
-- Expected: All 10 rows

-- Test 80: Pagination without results
-- Expected: Empty result set
-- MySQL/PostgreSQL/SQLite:
--   SELECT * FROM test_users WHERE score > 1000 ORDER BY id LIMIT 10;
-- Expected: 0 rows

-- ============================================================================
-- SECTION 10: PERFORMANCE TESTS (Test Cases 81-90)
-- ============================================================================

-- Test 81: Measure OFFSET pagination time
-- MySQL:
/*
SET @start_time = NOW();
SELECT * FROM test_users ORDER BY id LIMIT 10 OFFSET 5;
SELECT TIMESTAMPDIFF(MICROSECOND, @start_time, NOW()) AS execution_time_us;
*/

-- Test 82: Measure keyset pagination time
-- MySQL:
/*
SET @start_time = NOW();
SELECT * FROM test_users WHERE id > 5 ORDER BY id LIMIT 10;
SELECT TIMESTAMPDIFF(MICROSECOND, @start_time, NOW()) AS execution_time_us;
*/

-- Test 83: Compare COUNT(*) performance
-- MySQL:
/*
SET @start_time = NOW();
SELECT COUNT(*) FROM test_users;
SELECT TIMESTAMPDIFF(MICROSECOND, @start_time, NOW()) AS count_time_us;
*/

-- Test 84: Window function performance
-- MySQL 8.0+:
/*
SELECT *, COUNT(*) OVER() AS total FROM test_users ORDER BY id LIMIT 10;
-- Compare with separate COUNT(*) + SELECT
*/

-- Test 85: Index usage check
-- MySQL:
--   EXPLAIN SELECT * FROM test_users ORDER BY id LIMIT 10;
-- Expected: Using PRIMARY index

-- Test 86: Index usage for filtered pagination
-- MySQL:
--   EXPLAIN SELECT * FROM test_users WHERE status = 'active' ORDER BY id LIMIT 10;
-- Expected: Using index if available

-- Test 87: Deep pagination index usage
-- MySQL:
--   EXPLAIN SELECT * FROM test_users ORDER BY id LIMIT 10 OFFSET 1000;
-- Expected: Full scan or index scan

-- Test 88: Keyset pagination index usage
-- MySQL:
--   EXPLAIN SELECT * FROM test_users WHERE id > 1000 ORDER BY id LIMIT 10;
-- Expected: Using PRIMARY index with range

-- Test 89: Covering index for pagination
-- MySQL:
--   CREATE INDEX idx_covering ON test_users(status, score, id);
--   EXPLAIN SELECT id, status, score FROM test_users WHERE status = 'active' ORDER BY score LIMIT 10;
-- Expected: Using covering index

-- Test 90: Pagination query plan analysis
-- PostgreSQL:
--   EXPLAIN ANALYZE SELECT * FROM test_users ORDER BY id LIMIT 10 OFFSET 5;

-- ============================================================================
-- SECTION 11: INTEGRATION TESTS (Test Cases 91-100)
-- ============================================================================

-- Test 91: Complete pagination workflow
-- MySQL:
/*
-- Step 1: Get total count
SELECT COUNT(*) AS total_items FROM test_users WHERE status = 'active';

-- Step 2: Calculate pagination metadata
SELECT 
    CEIL(7 / 5.0) AS total_pages,
    5 AS page_size;

-- Step 3: Get first page
SELECT * FROM test_users WHERE status = 'active' ORDER BY id LIMIT 5 OFFSET 0;

-- Step 4: Get next page
SELECT * FROM test_users WHERE status = 'active' ORDER BY id LIMIT 5 OFFSET 5;
*/

-- Test 92: Pagination with sorting options
-- MySQL:
/*
-- Sort by name ASC
SELECT * FROM test_users ORDER BY name ASC LIMIT 5;

-- Sort by name DESC
SELECT * FROM test_users ORDER BY name DESC LIMIT 5;

-- Sort by score DESC then name ASC
SELECT * FROM test_users ORDER BY score DESC, name ASC LIMIT 5;
*/

-- Test 93: Pagination for search results
-- MySQL:
/*
-- Search with count
SELECT COUNT(*) AS total FROM test_users WHERE name LIKE 'User%';

-- Search with pagination
SELECT * FROM test_users WHERE name LIKE 'User%' ORDER BY id LIMIT 5 OFFSET 0;
*/

-- Test 94: Pagination for API response format
-- MySQL 8.0+:
/*
SELECT JSON_OBJECT(
    'total', (SELECT COUNT(*) FROM test_users),
    'page', 1,
    'pageSize', 5,
    'items', (SELECT JSON_ARRAYAGG(JSON_OBJECT('id', id, 'name', name, 'score', score))
              FROM (SELECT id, name, score FROM test_users ORDER BY id LIMIT 5) sub)
) AS response;
*/

-- Test 95: Pagination with joins
-- MySQL:
/*
SELECT p.*, u.name AS author_name
FROM test_posts p
JOIN test_users u ON p.author_id = u.id
ORDER BY p.created_at DESC
LIMIT 5;
*/

-- Test 96: Pagination with aggregations
-- MySQL:
/*
SELECT 
    u.id,
    u.name,
    COUNT(p.id) AS post_count
FROM test_users u
LEFT JOIN test_posts p ON u.id = p.author_id
GROUP BY u.id, u.name
ORDER BY post_count DESC
LIMIT 5;
*/

-- Test 97: Nested pagination (posts per user)
-- MySQL 8.0+:
/*
WITH UserPosts AS (
    SELECT 
        u.id AS user_id,
        u.name,
        p.id AS post_id,
        p.title,
        ROW_NUMBER() OVER (PARTITION BY u.id ORDER BY p.created_at DESC) AS post_rank
    FROM test_users u
    LEFT JOIN test_posts p ON u.id = p.author_id
)
SELECT * FROM UserPosts WHERE post_rank <= 3;  -- 3 most recent posts per user
*/

-- Test 98: Pagination with calculated fields
-- MySQL:
/*
SELECT 
    id,
    name,
    score,
    CASE 
        WHEN score >= 80 THEN 'High'
        WHEN score >= 50 THEN 'Medium'
        ELSE 'Low'
    END AS score_category
FROM test_users
ORDER BY score DESC
LIMIT 5;
*/

-- Test 99: Pagination cache simulation
-- MySQL:
/*
-- Cache first page results
CREATE TEMPORARY TABLE cached_page AS
SELECT * FROM test_users ORDER BY id LIMIT 5;

-- Retrieve cached page
SELECT * FROM cached_page;

-- Clear cache
DROP TEMPORARY TABLE cached_page;
*/

-- Test 100: Full pagination system test
-- MySQL:
/*
-- Setup: Clear and repopulate
DELETE FROM test_users;
INSERT INTO test_users (name, email, score, status) VALUES
    ('Alice', 'alice@test.com', 95, 'active'),
    ('Bob', 'bob@test.com', 85, 'active'),
    ('Carol', 'carol@test.com', 75, 'inactive'),
    ('Dave', 'dave@test.com', 65, 'active'),
    ('Eve', 'eve@test.com', 55, 'active');

-- Test: Verify pagination works correctly
SELECT * FROM test_users ORDER BY score DESC LIMIT 2;  -- Should return Alice, Bob
SELECT COUNT(*) FROM test_users;  -- Should return 5

-- Cleanup
DELETE FROM test_users;
*/

-- ============================================================================
-- SECTION 12: TEST CLEANUP
-- ============================================================================

-- MySQL:
/*
DROP TABLE IF EXISTS test_users;
DROP TABLE IF EXISTS test_posts;
*/

-- PostgreSQL:
/*
DROP TABLE IF EXISTS test_users;
DROP TABLE IF EXISTS test_posts;
*/

-- SQL Server:
/*
DROP TABLE IF EXISTS test_users;
DROP TABLE IF EXISTS test_posts;
*/

-- SQLite:
/*
DROP TABLE IF EXISTS test_users;
DROP TABLE IF EXISTS test_posts;
*/

-- ============================================================================
-- TEST SUMMARY
-- ============================================================================
-- Total Test Cases: 100
-- Categories:
--   - Basic Pagination: 10 tests (1-10)
--   - Keyset/Cursor Pagination: 10 tests (11-20)
--   - Pagination Metadata: 10 tests (21-30)
--   - Pagination with Filtering: 10 tests (31-40)
--   - Pagination with Total Count: 10 tests (41-50)
--   - Deep Pagination: 10 tests (51-60)
--   - Row Numbering: 10 tests (61-70)
--   - Edge Cases: 10 tests (71-80)
--   - Performance: 10 tests (81-90)
--   - Integration: 10 tests (91-100)
-- ============================================================================
-- END OF TEST MODULE
-- ============================================================================