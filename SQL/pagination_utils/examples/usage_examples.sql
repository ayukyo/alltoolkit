-- ============================================================================
-- SQL Pagination Utilities - Usage Examples
-- ============================================================================
-- Practical examples demonstrating pagination patterns for different databases.
--
-- Author: AllToolkit
-- License: MIT
-- ============================================================================

-- ============================================================================
-- EXAMPLE 1: Basic Pagination (Page 1 of Users)
-- ============================================================================

-- MySQL:
--   SELECT * FROM users
--   ORDER BY created_at DESC
--   LIMIT 20 OFFSET 0;

-- PostgreSQL:
--   SELECT * FROM users
--   ORDER BY created_at DESC
--   LIMIT 20 OFFSET 0;

-- SQL Server:
--   SELECT * FROM users
--   ORDER BY created_at DESC
--   OFFSET 0 ROWS FETCH NEXT 20 ROWS ONLY;

-- SQLite:
--   SELECT * FROM users
--   ORDER BY created_at DESC
--   LIMIT 20 OFFSET 0;

-- ============================================================================
-- EXAMPLE 2: Pagination with Total Count
-- ============================================================================

-- MySQL 8.0+ (Single query):
--   SELECT 
--     u.*,
--     COUNT(*) OVER() AS total_count
--   FROM users u
--   ORDER BY u.id
--   LIMIT 20 OFFSET 0;

-- PostgreSQL (Single query):
--   SELECT 
--     u.*,
--     COUNT(*) OVER() AS total_count
--   FROM users u
--   ORDER BY u.id
--   LIMIT 20 OFFSET 0;

-- Alternative (Two queries - more efficient for large tables):
--   -- Query 1: Get total count
--   SELECT COUNT(*) AS total_count FROM users;
--   
--   -- Query 2: Get page data
--   SELECT * FROM users ORDER BY id LIMIT 20 OFFSET 0;

-- ============================================================================
-- EXAMPLE 3: Keyset/Cursor Pagination (Efficient for Large Data)
-- ============================================================================

-- MySQL (First page):
--   SELECT * FROM posts
--   ORDER BY id DESC
--   LIMIT 20;

-- MySQL (Next page - get items after cursor id=100):
--   SELECT * FROM posts
--   WHERE id < 100
--   ORDER BY id DESC
--   LIMIT 20;

-- PostgreSQL (First page):
--   SELECT * FROM posts
--   ORDER BY id DESC
--   LIMIT 20;

-- PostgreSQL (Next page):
--   SELECT * FROM posts
--   WHERE id < 100
--   ORDER BY id DESC
--   LIMIT 20;

-- SQL Server (First page):
--   SELECT TOP 20 * FROM posts
--   ORDER BY id DESC;

-- SQL Server (Next page):
--   SELECT TOP 20 * FROM posts
--   WHERE id < 100
--   ORDER BY id DESC;

-- ============================================================================
-- EXAMPLE 4: Pagination with Filters
-- ============================================================================

-- MySQL (Active users, page 2):
--   SELECT * FROM users
--   WHERE status = 'active'
--   ORDER BY created_at DESC
--   LIMIT 10 OFFSET 10;

-- PostgreSQL (Active users, page 2):
--   SELECT * FROM users
--   WHERE status = 'active'
--   ORDER BY created_at DESC
--   LIMIT 10 OFFSET 10;

-- SQL Server (Active users, page 2):
--   SELECT * FROM users
--   WHERE status = 'active'
--   ORDER BY created_at DESC
--   OFFSET 10 ROWS FETCH NEXT 10 ROWS ONLY;

-- ============================================================================
-- EXAMPLE 5: Keyset Pagination with Multiple Columns
-- ============================================================================

-- When sorting by (created_at DESC, id ASC), cursor contains both values

-- MySQL 8.0.2+:
--   -- First page
--   SELECT * FROM posts
--   ORDER BY created_at DESC, id ASC
--   LIMIT 20;
--   
--   -- Next page (after created_at='2024-01-15', id=500)
--   SELECT * FROM posts
--   WHERE (created_at, id) < ('2024-01-15', 500)
--   ORDER BY created_at DESC, id ASC
--   LIMIT 20;

-- PostgreSQL:
--   -- First page
--   SELECT * FROM posts
--   ORDER BY created_at DESC, id ASC
--   LIMIT 20;
--   
--   -- Next page (after created_at='2024-01-15', id=500)
--   SELECT * FROM posts
--   WHERE (created_at, id) < ('2024-01-15', 500)
--   ORDER BY created_at DESC, id ASC
--   LIMIT 20;

-- SQL Server:
--   -- First page
--   SELECT TOP 20 * FROM posts
--   ORDER BY created_at DESC, id ASC;
--   
--   -- Next page
--   SELECT TOP 20 * FROM posts
--   WHERE created_at < '2024-01-15'
--      OR (created_at = '2024-01-15' AND id < 500)
--   ORDER BY created_at DESC, id ASC;

-- ============================================================================
-- EXAMPLE 6: ROW_NUMBER Pagination
-- ============================================================================

-- MySQL 8.0+:
--   WITH NumberedRows AS (
--     SELECT 
--       *,
--       ROW_NUMBER() OVER (ORDER BY score DESC) AS row_num
--     FROM players
--   )
--   SELECT * FROM NumberedRows
--   WHERE row_num BETWEEN 11 AND 20;

-- PostgreSQL:
--   WITH NumberedRows AS (
--     SELECT 
--       *,
--       ROW_NUMBER() OVER (ORDER BY score DESC) AS row_num
--     FROM players
--   )
--   SELECT * FROM NumberedRows
--   WHERE row_num BETWEEN 11 AND 20;

-- SQL Server:
--   WITH NumberedRows AS (
--     SELECT 
--       *,
--       ROW_NUMBER() OVER (ORDER BY score DESC) AS row_num
--     FROM players
--   )
--   SELECT * FROM NumberedRows
--   WHERE row_num BETWEEN 11 AND 20;

-- SQLite 3.25+:
--   WITH NumberedRows AS (
--     SELECT 
--       *,
--       ROW_NUMBER() OVER (ORDER BY score DESC) AS row_num
--     FROM players
--   )
--   SELECT * FROM NumberedRows
--   WHERE row_num BETWEEN 11 AND 20;

-- ============================================================================
-- EXAMPLE 7: Top N Per Group (Rank Pagination)
-- ============================================================================

-- Get top 3 posts per category

-- MySQL 8.0+:
--   WITH RankedPosts AS (
--     SELECT 
--       *,
--       ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY views DESC) AS rank
--     FROM posts
--   )
--   SELECT * FROM RankedPosts
--   WHERE rank <= 3;

-- PostgreSQL:
--   WITH RankedPosts AS (
--     SELECT 
--       *,
--       ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY views DESC) AS rank
--     FROM posts
--   )
--   SELECT * FROM RankedPosts
--   WHERE rank <= 3;

-- SQL Server:
--   WITH RankedPosts AS (
--     SELECT 
--       *,
--       ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY views DESC) AS rank
--     FROM posts
--   )
--   SELECT * FROM RankedPosts
--   WHERE rank <= 3;

-- ============================================================================
-- EXAMPLE 8: Search Results Pagination
-- ============================================================================

-- MySQL (Full-text search):
--   SELECT 
--     *,
--     MATCH(title, content) AGAINST('database optimization' IN NATURAL LANGUAGE MODE) AS relevance
--   FROM articles
--   WHERE MATCH(title, content) AGAINST('database optimization' IN NATURAL LANGUAGE MODE)
--   ORDER BY relevance DESC
--   LIMIT 20 OFFSET 0;

-- PostgreSQL (Full-text search):
--   SELECT 
--     *,
--     ts_rank(to_tsvector(title || ' ' || content), to_tsquery('database & optimization')) AS relevance
--   FROM articles
--   WHERE to_tsvector(title || ' ' || content) @@ to_tsquery('database & optimization')
--   ORDER BY relevance DESC
--   LIMIT 20 OFFSET 0;

-- SQL Server (LIKE search):
--   SELECT *
--   FROM articles
--   WHERE title LIKE '%database%' OR content LIKE '%database%'
--   ORDER BY 
--     CASE WHEN title LIKE '%database%' THEN 1 ELSE 2 END,
--     created_at DESC
--   OFFSET 0 ROWS FETCH NEXT 20 ROWS ONLY;

-- ============================================================================
-- EXAMPLE 9: Pagination with Joins
-- ============================================================================

-- MySQL:
--   SELECT 
--     p.id,
--     p.title,
--     p.created_at,
--     a.name AS author_name,
--     c.name AS category_name
--   FROM posts p
--   JOIN authors a ON p.author_id = a.id
--   JOIN categories c ON p.category_id = c.id
--   WHERE p.status = 'published'
--   ORDER BY p.created_at DESC
--   LIMIT 20 OFFSET 0;

-- PostgreSQL:
--   SELECT 
--     p.id,
--     p.title,
--     p.created_at,
--     a.name AS author_name,
--     c.name AS category_name
--   FROM posts p
--   JOIN authors a ON p.author_id = a.id
--   JOIN categories c ON p.category_id = c.id
--   WHERE p.status = 'published'
--   ORDER BY p.created_at DESC
--   LIMIT 20 OFFSET 0;

-- ============================================================================
-- EXAMPLE 10: Infinite Scroll (has_more Indicator)
-- ============================================================================

-- MySQL:
--   -- Fetch 21 items to check if there's more
--   SELECT * FROM posts
--   ORDER BY created_at DESC
--   LIMIT 21;
--   
--   -- In application: if 21 items returned, there's more data
--   -- Return only 20 items, set has_more = true

-- PostgreSQL:
--   -- Same approach: fetch N+1 items
--   SELECT * FROM posts
--   ORDER BY created_at DESC
--   LIMIT 21;

-- Alternative with explicit has_more:
-- MySQL:
--   SELECT 
--     (SELECT COUNT(*) FROM posts) > 20 AS has_more;
--   
--   SELECT * FROM posts
--   ORDER BY created_at DESC
--   LIMIT 20;

-- ============================================================================
-- EXAMPLE 11: Deep Pagination Optimization
-- ============================================================================

-- Problem: Large OFFSET is slow
-- Bad: SELECT * FROM users ORDER BY id LIMIT 10 OFFSET 1000000;

-- MySQL (Optimization 1 - JOIN with derived table):
--   SELECT u.* FROM users u
--   INNER JOIN (
--     SELECT id FROM users ORDER BY id LIMIT 10 OFFSET 1000000
--   ) AS tmp ON u.id = tmp.id;

-- MySQL (Optimization 2 - Keyset pagination):
--   SELECT * FROM users
--   WHERE id > 1000000
--   ORDER BY id
--   LIMIT 10;

-- PostgreSQL (Keyset pagination):
--   SELECT * FROM users
--   WHERE id > 1000000
--   ORDER BY id
--   LIMIT 10;

-- ============================================================================
-- EXAMPLE 12: Pagination Metadata Calculation
-- ============================================================================

-- MySQL:
--   SELECT 
--     COUNT(*) AS total_items,
--     CEIL(COUNT(*) / 20.0) AS total_pages,
--     20 AS items_per_page,
--     1 AS current_page,
--     CASE WHEN 1 > 1 THEN 1 - 1 ELSE NULL END AS prev_page,
--     CASE WHEN 1 < CEIL(COUNT(*) / 20.0) THEN 1 + 1 ELSE NULL END AS next_page
--   FROM users
--   WHERE status = 'active';

-- PostgreSQL:
--   SELECT 
--     COUNT(*) AS total_items,
--     CEILING(COUNT(*)::DECIMAL / 20) AS total_pages,
--     20 AS items_per_page,
--     1 AS current_page,
--     CASE WHEN 1 > 1 THEN 1 - 1 ELSE NULL END AS prev_page,
--     CASE WHEN 1 < CEILING(COUNT(*)::DECIMAL / 20) THEN 1 + 1 ELSE NULL END AS next_page
--   FROM users
--   WHERE status = 'active';

-- ============================================================================
-- EXAMPLE 13: Bidirectional Cursor Pagination
-- ============================================================================

-- Navigate forward and backward through results

-- MySQL (First page):
--   SELECT * FROM posts
--   ORDER BY created_at DESC, id ASC
--   LIMIT 20;

-- MySQL (Next page - forward):
--   SELECT * FROM posts
--   WHERE created_at < '2024-01-15'
--      OR (created_at = '2024-01-15' AND id < 500)
--   ORDER BY created_at DESC, id ASC
--   LIMIT 20;

-- MySQL (Previous page - backward):
--   SELECT * FROM (
--     SELECT * FROM posts
--     WHERE created_at > '2024-01-15'
--        OR (created_at = '2024-01-15' AND id > 500)
--     ORDER BY created_at ASC, id DESC
--     LIMIT 20
--   ) AS sub
--   ORDER BY created_at DESC, id ASC;

-- ============================================================================
-- EXAMPLE 14: Time-Based Pagination
-- ============================================================================

-- MySQL:
--   -- Get posts from current month, paginated
--   SELECT * FROM posts
--   WHERE created_at >= DATE_FORMAT(NOW(), '%Y-%m-01')
--   ORDER BY created_at DESC
--   LIMIT 20 OFFSET 0;

-- PostgreSQL:
--   SELECT * FROM posts
--   WHERE created_at >= DATE_TRUNC('month', CURRENT_DATE)
--   ORDER BY created_at DESC
--   LIMIT 20 OFFSET 0;

-- SQL Server:
--   SELECT * FROM posts
--   WHERE created_at >= DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1)
--   ORDER BY created_at DESC
--   OFFSET 0 ROWS FETCH NEXT 20 ROWS ONLY;

-- ============================================================================
-- EXAMPLE 15: Pagination with Estimated Count (Large Tables)
-- ============================================================================

-- MySQL (Use table statistics):
--   SELECT TABLE_ROWS AS estimated_total
--   FROM information_schema.TABLES
--   WHERE TABLE_NAME = 'users' AND TABLE_SCHEMA = DATABASE();

-- PostgreSQL (Use pg_class):
--   SELECT reltuples::BIGINT AS estimated_total
--   FROM pg_class
--   WHERE relname = 'users';

-- SQL Server (Use sys.partitions):
--   SELECT SUM(p.rows) AS estimated_total
--   FROM sys.partitions p
--   WHERE p.object_id = OBJECT_ID('users') AND p.index_id IN (0, 1);

-- ============================================================================
-- EXAMPLE 16: Pagination for API Response
-- ============================================================================

-- MySQL 8.0+ (JSON format):
--   SELECT JSON_OBJECT(
--     'success', TRUE,
--     'data', JSON_ARRAYAGG(
--       JSON_OBJECT(
--         'id', id,
--         'name', name,
--         'email', email
--       )
--     ),
--     'pagination', JSON_OBJECT(
--       'total', (SELECT COUNT(*) FROM users),
--       'page', 1,
--       'pageSize', 20,
--       'totalPages', CEIL((SELECT COUNT(*) FROM users) / 20.0)
--     )
--   ) AS response
--   FROM (SELECT * FROM users ORDER BY id LIMIT 20 OFFSET 0) AS sub;

-- PostgreSQL (JSON format):
--   SELECT json_build_object(
--     'success', TRUE,
--     'data', json_agg(json_build_object(
--       'id', id,
--       'name', name,
--       'email', email
--     )),
--     'pagination', json_build_object(
--       'total', (SELECT COUNT(*) FROM users),
--       'page', 1,
--       'pageSize', 20,
--       'totalPages', CEILING((SELECT COUNT(*)::DECIMAL FROM users) / 20)
--     )
--   ) AS response
--   FROM (SELECT id, name, email FROM users ORDER BY id LIMIT 20 OFFSET 0) sub;

-- ============================================================================
-- EXAMPLE 17: Deduplication with ROW_NUMBER
-- ============================================================================

-- Keep only the latest record per user

-- MySQL 8.0+:
--   WITH RankedRecords AS (
--     SELECT 
--       *,
--       ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC) AS rn
--     FROM activities
--   )
--   SELECT * FROM RankedRecords
--   WHERE rn = 1
--   ORDER BY user_id
--   LIMIT 50;

-- PostgreSQL:
--   WITH RankedRecords AS (
--     SELECT 
--       *,
--       ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC) AS rn
--     FROM activities
--   )
--   SELECT * FROM RankedRecords
--   WHERE rn = 1
--   ORDER BY user_id
--   LIMIT 50;

-- ============================================================================
-- EXAMPLE 18: Stored Procedure for Dynamic Pagination
-- ============================================================================

-- MySQL:
/*
DELIMITER //
CREATE PROCEDURE GetPaginatedProducts(
    IN category_id INT,
    IN page_num INT,
    IN page_size INT,
    IN sort_by VARCHAR(50),
    IN sort_dir VARCHAR(4)
)
BEGIN
    DECLARE offset_val INT;
    SET offset_val = (page_num - 1) * page_size;
    
    -- Get total count
    SELECT COUNT(*) AS total_count
    FROM products
    WHERE category_id = category_id OR category_id IS NULL;
    
    -- Get paginated data
    SET @sql = CONCAT(
        'SELECT * FROM products WHERE ', 
        IFNULL(category_id, 'TRUE'), 
        ' = ', IFNULL(category_id, 'TRUE'),
        ' ORDER BY ', sort_by, ' ', sort_dir,
        ' LIMIT ', page_size, ' OFFSET ', offset_val
    );
    
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;

-- Usage:
CALL GetPaginatedProducts(NULL, 2, 10, 'price', 'ASC');
*/

-- PostgreSQL:
/*
CREATE OR REPLACE FUNCTION get_paginated_products(
    p_category_id INTEGER DEFAULT NULL,
    p_page_num INTEGER DEFAULT 1,
    p_page_size INTEGER DEFAULT 20,
    p_sort_by TEXT DEFAULT 'id',
    p_sort_dir TEXT DEFAULT 'ASC'
)
RETURNS TABLE (
    total_count BIGINT,
    products JSONB
) AS $$
DECLARE
    v_offset INTEGER;
    v_total BIGINT;
BEGIN
    v_offset := (p_page_num - 1) * p_page_size;
    
    -- Get total count
    SELECT COUNT(*) INTO v_total
    FROM products
    WHERE p_category_id IS NULL OR category_id = p_category_id;
    
    -- Return results
    RETURN QUERY
    SELECT 
        v_total AS total_count,
        jsonb_agg(row_to_json(p)) AS products
    FROM (
        SELECT * FROM products
        WHERE p_category_id IS NULL OR category_id = p_category_id
        ORDER BY 
            CASE WHEN p_sort_dir = 'ASC' THEN 
                CASE p_sort_by
                    WHEN 'price' THEN price
                    WHEN 'name' THEN name
                    ELSE id
                END
            END ASC,
            CASE WHEN p_sort_dir = 'DESC' THEN 
                CASE p_sort_by
                    WHEN 'price' THEN price
                    WHEN 'name' THEN name
                    ELSE id
                END
            END DESC
        LIMIT p_page_size OFFSET v_offset
    ) p;
END;
$$ LANGUAGE plpgsql;

-- Usage:
SELECT * FROM get_paginated_products(5, 2, 10, 'price', 'DESC');
*/

-- ============================================================================
-- EXAMPLE 19: Leaderboard Pagination with Rank
-- ============================================================================

-- MySQL 8.0+:
--   WITH Leaderboard AS (
--     SELECT 
--       u.id,
--       u.name,
--       u.score,
--       RANK() OVER (ORDER BY score DESC) AS rank,
--       DENSE_RANK() OVER (ORDER BY score DESC) AS dense_rank,
--       ROW_NUMBER() OVER (ORDER BY score DESC, id ASC) AS position
--     FROM users u
--     WHERE u.status = 'active'
--   )
--   SELECT * FROM Leaderboard
--   WHERE position BETWEEN 1 AND 100;

-- PostgreSQL:
--   WITH Leaderboard AS (
--     SELECT 
--       u.id,
--       u.name,
--       u.score,
--       RANK() OVER (ORDER BY score DESC) AS rank,
--       DENSE_RANK() OVER (ORDER BY score DESC) AS dense_rank,
--       ROW_NUMBER() OVER (ORDER BY score DESC, id ASC) AS position
--     FROM users u
--     WHERE u.status = 'active'
--   )
--   SELECT * FROM Leaderboard
--   WHERE position BETWEEN 1 AND 100;

-- ============================================================================
-- EXAMPLE 20: Comment Thread Pagination (Nested Structure)
-- ============================================================================

-- MySQL 8.0+:
--   WITH RECURSIVE CommentTree AS (
--     -- Base case: top-level comments
--     SELECT 
--       id, parent_id, content, author_id, created_at, 
--       1 AS depth,
--       CAST(id AS CHAR(1000)) AS path
--     FROM comments
--     WHERE post_id = 123 AND parent_id IS NULL
--     
--     UNION ALL
--     
--     -- Recursive case: child comments
--     SELECT 
--       c.id, c.parent_id, c.content, c.author_id, c.created_at,
--       ct.depth + 1,
--       CONCAT(ct.path, '/', c.id)
--     FROM comments c
--     JOIN CommentTree ct ON c.parent_id = ct.id
--     WHERE c.post_id = 123 AND ct.depth < 10  -- Limit depth
--   )
--   SELECT * FROM CommentTree
--   ORDER BY path
--   LIMIT 50;

-- PostgreSQL:
--   WITH RECURSIVE CommentTree AS (
--     SELECT 
--       id, parent_id, content, author_id, created_at,
--       1 AS depth,
--       ARRAY[id] AS path
--     FROM comments
--     WHERE post_id = 123 AND parent_id IS NULL
--     
--     UNION ALL
--     
--     SELECT 
--       c.id, c.parent_id, c.content, c.author_id, c.created_at,
--       ct.depth + 1,
--       ct.path || c.id
--     FROM comments c
--     JOIN CommentTree ct ON c.parent_id = ct.id
--     WHERE c.post_id = 123 AND ct.depth < 10
--   )
--   SELECT * FROM CommentTree
--   ORDER BY path
--   LIMIT 50;

-- ============================================================================
-- END OF EXAMPLES
-- ============================================================================