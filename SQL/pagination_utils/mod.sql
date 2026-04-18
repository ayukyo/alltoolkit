-- ============================================================================
-- SQL Pagination Utilities Module
-- ============================================================================
-- A comprehensive collection of pagination and result limiting utilities for SQL.
-- Supports MySQL, PostgreSQL, SQL Server, and SQLite with portable syntax.
--
-- Features:
--   - Basic pagination (LIMIT/OFFSET)
--   - Keyset/Cursor pagination (efficient for large datasets)
--   - Page metadata calculation
--   - Total count optimization
--   - Row numbering for pagination
--   - Pagination with sorting
--   - Deep pagination optimization
--   - Seek method pagination
--
-- Usage:
--   Copy individual query patterns for your specific database.
--   Each section includes database-specific implementations.
--
-- Author: AllToolkit
-- License: MIT
-- ============================================================================

-- ============================================================================
-- SECTION 1: BASIC PAGINATION (LIMIT/OFFSET)
-- ============================================================================

-- Basic pagination: Get page N with M items per page
-- Page numbers start at 1
-- OFFSET = (page_number - 1) * page_size

-- MySQL:
--   SELECT * FROM users
--   ORDER BY id
--   LIMIT 10 OFFSET 0;  -- Page 1, 10 items
--
--   SELECT * FROM users
--   ORDER BY id
--   LIMIT 10 OFFSET 20;  -- Page 3, 10 items

-- PostgreSQL:
--   SELECT * FROM users
--   ORDER BY id
--   LIMIT 10 OFFSET 0;  -- Page 1, 10 items
--
--   -- Alternative syntax:
--   SELECT * FROM users
--   ORDER BY id
--   LIMIT 10;

-- SQL Server:
--   -- SQL Server 2012+ (OFFSET-FETCH)
--   SELECT * FROM users
--   ORDER BY id
--   OFFSET 0 ROWS FETCH NEXT 10 ROWS ONLY;  -- Page 1, 10 items
--
--   SELECT * FROM users
--   ORDER BY id
--   OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY;  -- Page 3, 10 items
--
--   -- SQL Server 2008 and earlier (ROW_NUMBER)
--   WITH NumberedUsers AS (
--     SELECT *, ROW_NUMBER() OVER (ORDER BY id) AS row_num
--     FROM users
--   )
--   SELECT * FROM NumberedUsers
--   WHERE row_num BETWEEN 1 AND 10;  -- Page 1, 10 items

-- SQLite:
--   SELECT * FROM users
--   ORDER BY id
--   LIMIT 10 OFFSET 0;  -- Page 1, 10 items

-- ============================================================================
-- SECTION 2: PAGINATION WITH TOTAL COUNT
-- ============================================================================

-- Get paginated results with total count for UI pagination controls

-- MySQL:
--   -- Method 1: Two queries (more accurate total)
--   SELECT COUNT(*) AS total_count FROM users;
--   SELECT * FROM users ORDER BY id LIMIT 10 OFFSET 0;
--
--   -- Method 2: Window function (MySQL 8.0+)
--   SELECT 
--     *,
--     COUNT(*) OVER() AS total_count
--   FROM users
--   ORDER BY id
--   LIMIT 10 OFFSET 0;

-- PostgreSQL:
--   -- Method 1: Two queries
--   SELECT COUNT(*) AS total_count FROM users;
--   SELECT * FROM users ORDER BY id LIMIT 10 OFFSET 0;
--
--   -- Method 2: Window function
--   SELECT 
--     *,
--     COUNT(*) OVER() AS total_count
--   FROM users
--   ORDER BY id
--   LIMIT 10 OFFSET 0;

-- SQL Server:
--   -- Method 1: Two queries
--   SELECT COUNT(*) AS total_count FROM users;
--   SELECT * FROM users ORDER BY id OFFSET 0 ROWS FETCH NEXT 10 ROWS ONLY;
--
--   -- Method 2: Window function
--   WITH NumberedUsers AS (
--     SELECT 
--       *,
--       COUNT(*) OVER() AS total_count,
--       ROW_NUMBER() OVER (ORDER BY id) AS row_num
--     FROM users
--   )
--   SELECT * FROM NumberedUsers
--   WHERE row_num BETWEEN 1 AND 10;

-- SQLite:
--   -- Method 1: Two queries
--   SELECT COUNT(*) AS total_count FROM users;
--   SELECT * FROM users ORDER BY id LIMIT 10 OFFSET 0;
--
--   -- Method 2: Window function (SQLite 3.25+)
--   SELECT 
--     *,
--     COUNT(*) OVER() AS total_count
--   FROM users
--   ORDER BY id
--   LIMIT 10 OFFSET 0;

-- ============================================================================
-- SECTION 3: KEYSET/CURSOR PAGINATION (EFFICIENT)
-- ============================================================================

-- Keyset pagination uses the last value from the previous page to fetch the next
-- Much more efficient than OFFSET for large datasets

-- MySQL:
--   -- First page
--   SELECT * FROM users
--   WHERE active = 1
--   ORDER BY id ASC
--   LIMIT 10;
--
--   -- Next page (after id = 100)
--   SELECT * FROM users
--   WHERE active = 1 AND id > 100
--   ORDER BY id ASC
--   LIMIT 10;
--
--   -- Previous page (before id = 91)
--   SELECT * FROM (
--     SELECT * FROM users
--     WHERE active = 1 AND id < 91
--     ORDER BY id DESC
--     LIMIT 10
--   ) AS sub
--   ORDER BY id ASC;

-- PostgreSQL:
--   -- First page
--   SELECT * FROM users
--   WHERE active = TRUE
--   ORDER BY id ASC
--   LIMIT 10;
--
--   -- Next page (after id = 100)
--   SELECT * FROM users
--   WHERE active = TRUE AND id > 100
--   ORDER BY id ASC
--   LIMIT 10;
--
--   -- Previous page (before id = 91) - using subquery
--   SELECT * FROM (
--     SELECT * FROM users
--     WHERE active = TRUE AND id < 91
--     ORDER BY id DESC
--     LIMIT 10
--   ) sub
--   ORDER BY id ASC;

-- SQL Server:
--   -- First page
--   SELECT TOP 10 * FROM users
--   WHERE active = 1
--   ORDER BY id ASC;
--
--   -- Next page (after id = 100)
--   SELECT TOP 10 * FROM users
--   WHERE active = 1 AND id > 100
--   ORDER BY id ASC;
--
--   -- Previous page (before id = 91)
--   SELECT * FROM (
--     SELECT TOP 10 * FROM users
--     WHERE active = 1 AND id < 91
--     ORDER BY id DESC
--   ) sub
--   ORDER BY id ASC;

-- SQLite:
--   -- First page
--   SELECT * FROM users
--   WHERE active = 1
--   ORDER BY id ASC
--   LIMIT 10;
--
--   -- Next page (after id = 100)
--   SELECT * FROM users
--   WHERE active = 1 AND id > 100
--   ORDER BY id ASC
--   LIMIT 10;

-- ============================================================================
-- SECTION 4: KEYSET PAGINATION WITH MULTIPLE COLUMNS
-- ============================================================================

-- When sorting by multiple columns, keyset pagination needs all sort columns

-- MySQL / PostgreSQL / SQLite:
--   -- First page (sort by created_at DESC, id ASC)
--   SELECT * FROM posts
--   ORDER BY created_at DESC, id ASC
--   LIMIT 10;
--
--   -- Next page (after created_at = '2024-01-15', id = 500)
--   SELECT * FROM posts
--   WHERE (created_at, id) < ('2024-01-15', 500)
--      OR (created_at = '2024-01-15' AND id < 500)
--      OR created_at < '2024-01-15'
--   ORDER BY created_at DESC, id ASC
--   LIMIT 10;
--
--   -- Alternative: using tuple comparison (PostgreSQL, MySQL 8.0.2+)
--   SELECT * FROM posts
--   WHERE (created_at, id) < ('2024-01-15', 500)
--   ORDER BY created_at DESC, id ASC
--   LIMIT 10;

-- SQL Server:
--   -- First page (sort by created_at DESC, id ASC)
--   SELECT TOP 10 * FROM posts
--   ORDER BY created_at DESC, id ASC;
--
--   -- Next page (after created_at = '2024-01-15', id = 500)
--   SELECT TOP 10 * FROM posts
--   WHERE created_at < '2024-01-15'
--      OR (created_at = '2024-01-15' AND id < 500)
--   ORDER BY created_at DESC, id ASC;

-- ============================================================================
-- SECTION 5: ROW NUMBERING PAGINATION
-- ============================================================================

-- Use ROW_NUMBER() for complex pagination with multiple sort orders

-- MySQL 8.0+:
--   WITH NumberedRows AS (
--     SELECT 
--       *,
--       ROW_NUMBER() OVER (ORDER BY created_at DESC) AS row_num
--     FROM posts
--     WHERE status = 'published'
--   )
--   SELECT * FROM NumberedRows
--   WHERE row_num BETWEEN 11 AND 20;  -- Page 2, 10 items

-- PostgreSQL:
--   WITH NumberedRows AS (
--     SELECT 
--       *,
--       ROW_NUMBER() OVER (ORDER BY created_at DESC) AS row_num
--     FROM posts
--     WHERE status = 'published'
--   )
--   SELECT * FROM NumberedRows
--   WHERE row_num BETWEEN 11 AND 20;

-- SQL Server:
--   WITH NumberedRows AS (
--     SELECT 
--       *,
--       ROW_NUMBER() OVER (ORDER BY created_at DESC) AS row_num
--     FROM posts
--     WHERE status = 'published'
--   )
--   SELECT * FROM NumberedRows
--   WHERE row_num BETWEEN 11 AND 20;

-- SQLite 3.25+:
--   WITH NumberedRows AS (
--     SELECT 
--       *,
--       ROW_NUMBER() OVER (ORDER BY created_at DESC) AS row_num
--     FROM posts
--     WHERE status = 'published'
--   )
--   SELECT * FROM NumberedRows
--   WHERE row_num BETWEEN 11 AND 20;

-- ============================================================================
-- SECTION 6: PAGINATION WITH RANK/DENSE_RANK
-- ============================================================================

-- Use RANK() or DENSE_RANK() when dealing with ties

-- MySQL 8.0+ / PostgreSQL / SQL Server / SQLite 3.25+:
--   WITH RankedRows AS (
--     SELECT 
--       *,
--       RANK() OVER (ORDER BY score DESC) AS rank_position,
--       DENSE_RANK() OVER (ORDER BY score DESC) AS dense_rank_position,
--       ROW_NUMBER() OVER (ORDER BY score DESC, id ASC) AS row_num
--     FROM leaderboard
--   )
--   SELECT * FROM RankedRows
--   WHERE rank_position <= 100;  -- Top 100 (may include ties for 100th place)

-- ============================================================================
-- SECTION 7: DEEP PAGINATION OPTIMIZATION
-- ============================================================================

-- For deep pagination (high OFFSET values), use alternative methods

-- MySQL:
--   -- Problem: Large OFFSET is slow
--   SELECT * FROM users ORDER BY id LIMIT 10 OFFSET 1000000;
--
--   -- Solution 1: Use JOIN with derived table
--   SELECT u.* FROM users u
--   INNER JOIN (SELECT id FROM users ORDER BY id LIMIT 10 OFFSET 1000000) AS tmp
--   ON u.id = tmp.id;
--
--   -- Solution 2: Use keyset pagination instead
--   SELECT * FROM users WHERE id > 1000000 ORDER BY id LIMIT 10;

-- PostgreSQL:
--   -- Problem: Large OFFSET is slow
--   SELECT * FROM users ORDER BY id LIMIT 10 OFFSET 1000000;
--
--   -- Solution: Use keyset pagination
--   SELECT * FROM users WHERE id > 1000000 ORDER BY id LIMIT 10;

-- SQL Server:
--   -- Problem: Large OFFSET is slow
--   SELECT * FROM users ORDER BY id OFFSET 1000000 ROWS FETCH NEXT 10 ROWS ONLY;
--
--   -- Solution: Use keyset pagination
--   SELECT TOP 10 * FROM users WHERE id > 1000000 ORDER BY id;

-- SQLite:
--   -- Problem: Large OFFSET is slow
--   SELECT * FROM users ORDER BY id LIMIT 10 OFFSET 1000000;
--
--   -- Solution: Use keyset pagination
--   SELECT * FROM users WHERE id > 1000000 ORDER BY id LIMIT 10;

-- ============================================================================
-- SECTION 8: PAGINATION METADATA CALCULATION
-- ============================================================================

-- Calculate pagination metadata for UI

-- MySQL:
--   SELECT 
--     COUNT(*) AS total_items,
--     CEIL(COUNT(*) / 10.0) AS total_pages,
--     10 AS items_per_page,
--     1 AS current_page
--   FROM users;

-- PostgreSQL:
--   SELECT 
--     COUNT(*) AS total_items,
--     CEILING(COUNT(*)::DECIMAL / 10) AS total_pages,
--     10 AS items_per_page,
--     1 AS current_page
--   FROM users;

-- SQL Server:
--   SELECT 
--     COUNT(*) AS total_items,
--     CEILING(COUNT(*) * 1.0 / 10) AS total_pages,
--     10 AS items_per_page,
--     1 AS current_page
--   FROM users;

-- SQLite:
--   SELECT 
--     COUNT(*) AS total_items,
--     CAST(CEIL(COUNT(*) * 1.0 / 10) AS INTEGER) AS total_pages,
--     10 AS items_per_page,
--     1 AS current_page
--   FROM users;

-- ============================================================================
-- SECTION 9: SEEK METHOD PAGINATION
-- ============================================================================

-- Seek method: Remember the position of the last item for next page

-- MySQL / PostgreSQL / SQLite:
--   -- First page (get oldest items first)
--   SELECT id, name, created_at
--   FROM items
--   ORDER BY created_at ASC, id ASC
--   LIMIT 10;
--
--   -- Next page (seek from last item: created_at='2024-01-15', id=500)
--   SELECT id, name, created_at
--   FROM items
--   WHERE (created_at, id) > ('2024-01-15', 500)
--   ORDER BY created_at ASC, id ASC
--   LIMIT 10;

-- SQL Server:
--   -- First page
--   SELECT TOP 10 id, name, created_at
--   FROM items
--   ORDER BY created_at ASC, id ASC;
--
--   -- Next page (seek from last item)
--   SELECT TOP 10 id, name, created_at
--   FROM items
--   WHERE created_at > '2024-01-15'
--      OR (created_at = '2024-01-15' AND id > 500)
--   ORDER BY created_at ASC, id ASC;

-- ============================================================================
-- SECTION 10: INFINITE SCROLL PAGINATION
-- ============================================================================

-- For infinite scroll UI, return has_more indicator

-- MySQL 8.0+:
--   SELECT 
--     *,
--     CASE WHEN ROW_NUMBER() OVER (ORDER BY id) = 10 THEN 1 ELSE 0 END AS has_more
--   FROM (
--     SELECT * FROM posts
--     ORDER BY id
--     LIMIT 11  -- Fetch one extra to check for more
--   ) AS sub
--   LIMIT 10;

-- PostgreSQL:
--   -- Fetch 11 items, return 10 + has_more flag
--   WITH FetchedItems AS (
--     SELECT * FROM posts
--     ORDER BY id
--     LIMIT 11
--   )
--   SELECT 
--     *,
--     CASE WHEN (SELECT COUNT(*) FROM FetchedItems) > 10 THEN TRUE ELSE FALSE END AS has_more
--   FROM FetchedItems
--   LIMIT 10;

-- SQL Server:
--   WITH FetchedItems AS (
--     SELECT *, ROW_NUMBER() OVER (ORDER BY id) AS rn
--     FROM posts
--   )
--   SELECT *, CASE WHEN (SELECT MAX(rn) FROM FetchedItems) > 10 THEN 1 ELSE 0 END AS has_more
--   FROM FetchedItems
--   WHERE rn <= 10;

-- SQLite:
--   -- Simple approach: check if there are more items
--   SELECT * FROM posts ORDER BY id LIMIT 10;
--   SELECT EXISTS(SELECT 1 FROM posts ORDER BY id LIMIT 1 OFFSET 10) AS has_more;

-- ============================================================================
-- SECTION 11: PAGINATION WITH FILTERS
-- ============================================================================

-- Pagination with WHERE conditions

-- MySQL / PostgreSQL / SQLite:
--   -- Basic filtered pagination
--   SELECT * FROM products
--   WHERE category = 'electronics'
--     AND price BETWEEN 100 AND 500
--     AND stock > 0
--   ORDER BY price ASC, id ASC
--   LIMIT 20 OFFSET 0;
--
--   -- With total count
--   SELECT COUNT(*) AS total FROM products
--   WHERE category = 'electronics'
--     AND price BETWEEN 100 AND 500
--     AND stock > 0;

-- SQL Server:
--   SELECT * FROM products
--   WHERE category = 'electronics'
--     AND price BETWEEN 100 AND 500
--     AND stock > 0
--   ORDER BY price ASC, id ASC
--   OFFSET 0 ROWS FETCH NEXT 20 ROWS ONLY;

-- ============================================================================
-- SECTION 12: DYNAMIC PAGINATION (STORED PROCEDURES)
-- ============================================================================

-- MySQL stored procedure for dynamic pagination
/*
DELIMITER //
CREATE PROCEDURE PaginateUsers(
    IN page_num INT,
    IN page_size INT,
    IN sort_column VARCHAR(50),
    IN sort_direction VARCHAR(4)
)
BEGIN
    DECLARE offset_val INT;
    SET offset_val = (page_num - 1) * page_size;
    
    SET @sql = CONCAT(
        'SELECT * FROM users ORDER BY ', 
        sort_column, ' ', sort_direction,
        ' LIMIT ', page_size, ' OFFSET ', offset_val
    );
    
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;

-- Usage:
CALL PaginateUsers(2, 10, 'created_at', 'DESC');
*/

-- PostgreSQL function for dynamic pagination
/*
CREATE OR REPLACE FUNCTION paginate_users(
    page_num INTEGER,
    page_size INTEGER,
    sort_col TEXT DEFAULT 'id',
    sort_dir TEXT DEFAULT 'ASC'
)
RETURNS TABLE (
    id INTEGER,
    name VARCHAR(255),
    email VARCHAR(255),
    created_at TIMESTAMP
) AS $$
DECLARE
    offset_val INTEGER;
    sort_expr TEXT;
BEGIN
    offset_val := (page_num - 1) * page_size;
    sort_expr := sort_col || ' ' || sort_dir;
    
    RETURN QUERY EXECUTE format(
        'SELECT id, name, email, created_at FROM users ORDER BY %s LIMIT $1 OFFSET $2',
        sort_expr
    ) USING page_size, offset_val;
END;
$$ LANGUAGE plpgsql;

-- Usage:
SELECT * FROM paginate_users(2, 10, 'created_at', 'DESC');
*/

-- SQL Server stored procedure for dynamic pagination
/*
CREATE PROCEDURE PaginateUsers
    @PageNum INT,
    @PageSize INT,
    @SortColumn NVARCHAR(50) = 'id',
    @SortDirection NVARCHAR(4) = 'ASC'
AS
BEGIN
    DECLARE @OffsetVal INT = (@PageNum - 1) * @PageSize;
    DECLARE @SQL NVARCHAR(MAX);
    
    SET @SQL = N'
        SELECT * FROM users
        ORDER BY ' + QUOTENAME(@SortColumn) + ' ' + @SortDirection + '
        OFFSET ' + CAST(@OffsetVal AS NVARCHAR) + ' ROWS
        FETCH NEXT ' + CAST(@PageSize AS NVARCHAR) + ' ROWS ONLY';
    
    EXEC sp_executesql @SQL;
END;

-- Usage:
EXEC PaginateUsers @PageNum = 2, @PageSize = 10, @SortColumn = 'created_at', @SortDirection = 'DESC';
*/

-- ============================================================================
-- SECTION 13: PAGINATION HELPER FUNCTIONS
-- ============================================================================

-- Calculate page offset from page number

-- MySQL:
/*
DELIMITER //
CREATE FUNCTION GetPageOffset(page_num INT, page_size INT)
RETURNS INT
DETERMINISTIC
BEGIN
    RETURN (page_num - 1) * page_size;
END //
DELIMITER ;

-- Usage:
SELECT * FROM users
ORDER BY id
LIMIT 10 OFFSET GetPageOffset(3, 10);
*/

-- PostgreSQL:
/*
CREATE OR REPLACE FUNCTION get_page_offset(page_num INTEGER, page_size INTEGER)
RETURNS INTEGER AS $$
BEGIN
    RETURN (page_num - 1) * page_size;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Usage:
SELECT * FROM users
ORDER BY id
LIMIT 10 OFFSET get_page_offset(3, 10);
*/

-- SQL Server:
/*
CREATE FUNCTION GetPageOffset(@PageNum INT, @PageSize INT)
RETURNS INT
AS
BEGIN
    RETURN (@PageNum - 1) * @PageSize;
END;

-- Usage:
SELECT * FROM users
ORDER BY id
OFFSET dbo.GetPageOffset(3, 10) ROWS
FETCH NEXT 10 ROWS ONLY;
*/

-- ============================================================================
-- SECTION 14: TOTAL PAGES CALCULATION
-- ============================================================================

-- Calculate total pages from total items

-- MySQL:
/*
DELIMITER //
CREATE FUNCTION GetTotalPages(total_items BIGINT, page_size INT)
RETURNS INT
DETERMINISTIC
BEGIN
    RETURN CEIL(total_items / CAST(page_size AS DECIMAL));
END //
DELIMITER ;
*/

-- PostgreSQL:
/*
CREATE OR REPLACE FUNCTION get_total_pages(total_items BIGINT, page_size INTEGER)
RETURNS INTEGER AS $$
BEGIN
    RETURN CEILING(total_items::DECIMAL / page_size);
END;
$$ LANGUAGE plpgsql IMMUTABLE;
*/

-- SQL Server:
/*
CREATE FUNCTION GetTotalPages(@TotalItems BIGINT, @PageSize INT)
RETURNS INT
AS
BEGIN
    RETURN CEILING(CAST(@TotalItems AS DECIMAL) / @PageSize);
END;
*/

-- ============================================================================
-- SECTION 15: PRACTICAL EXAMPLES
-- ============================================================================

-- Example 1: Blog post pagination with author info
-- MySQL 8.0+:
--   WITH PostCounts AS (
--     SELECT COUNT(*) AS total_count FROM posts WHERE published = 1
--   )
--   SELECT 
--     p.*,
--     a.name AS author_name,
--     pc.total_count
--   FROM posts p
--   JOIN authors a ON p.author_id = a.id
--   CROSS JOIN PostCounts pc
--   WHERE p.published = 1
--   ORDER BY p.published_at DESC
--   LIMIT 10 OFFSET 0;

-- Example 2: Search results pagination
-- MySQL:
--   -- Full-text search with pagination
--   SELECT 
--     p.*,
--     MATCH(p.title, p.content) AGAINST('search term' IN NATURAL LANGUAGE MODE) AS relevance
--   FROM posts p
--   WHERE MATCH(p.title, p.content) AGAINST('search term' IN NATURAL LANGUAGE MODE)
--   ORDER BY relevance DESC
--   LIMIT 20 OFFSET 0;

-- PostgreSQL:
--   -- Full-text search with pagination
--   SELECT 
--     p.*,
--     ts_rank(to_tsvector(p.title || ' ' || p.content), to_tsquery('search & term')) AS relevance
--   FROM posts p
--   WHERE to_tsvector(p.title || ' ' || p.content) @@ to_tsquery('search & term')
--   ORDER BY relevance DESC
--   LIMIT 20 OFFSET 0;

-- Example 3: Comment thread pagination (nested)
-- MySQL 8.0+:
--   WITH RECURSIVE CommentTree AS (
--     SELECT id, parent_id, content, created_at, 1 AS depth
--     FROM comments
--     WHERE post_id = 123 AND parent_id IS NULL
--     
--     UNION ALL
--     
--     SELECT c.id, c.parent_id, c.content, c.created_at, ct.depth + 1
--     FROM comments c
--     JOIN CommentTree ct ON c.parent_id = ct.id
--     WHERE ct.depth < 5  -- Limit depth
--   )
--   SELECT * FROM CommentTree
--   ORDER BY created_at ASC
--   LIMIT 50;

-- Example 4: Time-based pagination (news feed)
-- MySQL:
--   -- Get posts from last 7 days, paginated
--   SELECT * FROM posts
--   WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
--   ORDER BY created_at DESC
--   LIMIT 20 OFFSET 0;
--
--   -- Cursor-based: Get posts older than a specific timestamp
--   SELECT * FROM posts
--   WHERE created_at < '2024-01-15 10:30:00'
--   ORDER BY created_at DESC
--   LIMIT 20;

-- Example 5: Activity feed pagination
-- PostgreSQL:
--   WITH ActivityWithTotal AS (
--     SELECT 
--       a.*,
--       COUNT(*) OVER() AS total_count
--     FROM activities a
--     WHERE a.user_id = 123
--     ORDER BY a.created_at DESC
--   )
--   SELECT * FROM ActivityWithTotal
--   LIMIT 25 OFFSET 0;

-- ============================================================================
-- SECTION 16: PAGINATION PERFORMANCE TIPS
-- ============================================================================

-- 1. Always use ORDER BY with pagination
--    Without ORDER BY, pagination results are unpredictable

-- 2. Index your sort columns
--    MySQL: CREATE INDEX idx_posts_created_at ON posts(created_at);
--    PostgreSQL: CREATE INDEX idx_posts_created_at ON posts(created_at);
--    SQL Server: CREATE INDEX idx_posts_created_at ON posts(created_at);

-- 3. Use keyset pagination for large datasets
--    OFFSET 1000000 is slow; WHERE id > 1000000 is fast

-- 4. Consider covering indexes for pagination queries
--    MySQL: CREATE INDEX idx_posts_covering ON posts(category, created_at, id) INCLUDE (title, content);
--    PostgreSQL: CREATE INDEX idx_posts_covering ON posts(category, created_at, id) INCLUDE (title, content);

-- 5. Use FETCH FIRST instead of TOP for standard SQL
--    Standard SQL: SELECT * FROM users ORDER BY id FETCH FIRST 10 ROWS ONLY;

-- 6. Estimate total count instead of exact count for large tables
--    PostgreSQL: 
--      SELECT reltuples::BIGINT AS estimate FROM pg_class WHERE relname = 'users';
--    MySQL:
--      SELECT TABLE_ROWS FROM information_schema.TABLES WHERE TABLE_NAME = 'users';
--    SQL Server:
--      SELECT SUM(p.rows) FROM sys.partitions p WHERE p.object_id = OBJECT_ID('users') AND p.index_id IN (0, 1);

-- ============================================================================
-- END OF MODULE
-- ============================================================================