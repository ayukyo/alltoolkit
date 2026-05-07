-- ============================================================================
-- Data Quality Utilities for SQL
-- ============================================================================
-- A comprehensive data quality utility module for SQL providing data
-- integrity checks, NULL handling, consistency validation, anomaly detection,
-- and statistical analysis across multiple database systems.
--
-- Features:
-- - NULL value analysis and handling strategies
-- - Data completeness metrics
-- - Uniqueness and duplication detection
-- - Data type validation
-- - Outlier detection
-- - Statistical summaries
-- - Data profiling utilities
-- - Data cleaning helpers
--
-- Supported Databases:
-- - MySQL 8.0+
-- - PostgreSQL 12+
-- - SQL Server 2019+
-- - SQLite 3.35+
--
-- Author: AllToolkit
-- Version: 1.0.0
-- License: MIT
-- Date: 2026-05-08
-- ============================================================================

-- ============================================================================
-- NULL VALUE ANALYSIS
-- ============================================================================

-- Query: null_count - Count NULL values in a column
-- Usage: Replace 'table_name' and 'column_name'
-- MySQL/PostgreSQL/SQLite:
-- SELECT COUNT(*) - COUNT(column_name) AS null_count FROM table_name;
-- SQL Server:
-- SELECT COUNT(*) - COUNT(column_name) AS null_count FROM table_name;

-- Query: null_percentage - Calculate NULL percentage
-- SELECT 
--     COUNT(*) AS total_rows,
--     SUM(CASE WHEN column_name IS NULL THEN 1 ELSE 0 END) AS null_count,
--     ROUND(100.0 * SUM(CASE WHEN column_name IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS null_percentage
-- FROM table_name;

-- Query: null_summary_all_columns - NULL summary for all columns
-- MySQL: 
-- SELECT 
--     SUM(CASE WHEN col1 IS NULL THEN 1 ELSE 0 END) AS col1_nulls,
--     SUM(CASE WHEN col2 IS NULL THEN 1 ELSE 0 END) AS col2_nulls,
--     SUM(CASE WHEN col3 IS NULL THEN 1 ELSE 0 END) AS col3_nulls
-- FROM table_name;

-- PostgreSQL (dynamic):
-- SELECT column_name, 
--        (SELECT COUNT(*) FROM table_name WHERE column_name IS NULL) AS null_count
-- FROM information_schema.columns 
-- WHERE table_name = 'your_table';

-- ============================================================================
-- DATA COMPLETENESS METRICS
-- ============================================================================

-- Query: completeness_score - Overall data completeness
-- SELECT 
--     COUNT(*) AS total_rows,
--     COUNT(column_name) AS non_null_rows,
--     ROUND(100.0 * COUNT(column_name) / COUNT(*), 2) AS completeness_pct
-- FROM table_name;

-- Query: multi_column_completeness - Completeness across multiple columns
-- SELECT 
--     COUNT(*) AS total_rows,
--     SUM(CASE WHEN col1 IS NOT NULL AND col2 IS NOT NULL AND col3 IS NOT NULL THEN 1 ELSE 0 END) AS complete_rows,
--     ROUND(100.0 * SUM(CASE WHEN col1 IS NOT NULL AND col2 IS NOT NULL AND col3 IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS complete_pct
-- FROM table_name;

-- ============================================================================
-- UNIQUENESS AND DUPLICATION DETECTION
-- ============================================================================

-- Query: duplicate_count - Find duplicate values
-- SELECT column_name, COUNT(*) AS duplicate_count
-- FROM table_name
-- GROUP BY column_name
-- HAVING COUNT(*) > 1
-- ORDER BY duplicate_count DESC;

-- Query: duplicate_rows - Get all duplicate rows
-- SELECT t.*
-- FROM table_name t
-- INNER JOIN (
--     SELECT column_name
--     FROM table_name
--     GROUP BY column_name
--     HAVING COUNT(*) > 1
-- ) dup ON t.column_name = dup.column_name;

-- Query: uniqueness_ratio - Calculate uniqueness percentage
-- SELECT 
--     COUNT(*) AS total_rows,
--     COUNT(DISTINCT column_name) AS unique_values,
--     ROUND(100.0 * COUNT(DISTINCT column_name) / COUNT(*), 2) AS uniqueness_pct
-- FROM table_name;

-- Query: find_exact_duplicates - Find exact duplicate rows (all columns)
-- SELECT col1, col2, col3, COUNT(*) AS duplicate_count
-- FROM table_name
-- GROUP BY col1, col2, col3
-- HAVING COUNT(*) > 1;

-- ============================================================================
-- DATA TYPE VALIDATION
-- ============================================================================

-- Query: validate_numeric - Find non-numeric values in string column
-- MySQL: 
-- SELECT column_name
-- FROM table_name
-- WHERE column_name IS NOT NULL 
--   AND column_name NOT REGEXP '^[+-]?[0-9]*\\.?[0-9]+$';

-- PostgreSQL:
-- SELECT column_name
-- FROM table_name
-- WHERE column_name IS NOT NULL 
--   AND column_name !~ '^[+-]?[0-9]*\.?[0-9]+$';

-- SQL Server:
-- SELECT column_name
-- FROM table_name
-- WHERE column_name IS NOT NULL 
--   AND TRY_CAST(column_name AS DECIMAL) IS NULL;

-- Query: validate_email_format - Find invalid email formats
-- MySQL:
-- SELECT email_column
-- FROM table_name
-- WHERE email_column IS NOT NULL
--   AND email_column NOT REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$';

-- PostgreSQL:
-- SELECT email_column
-- FROM table_name
-- WHERE email_column IS NOT NULL
--   AND email_column !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$';

-- Query: validate_date_format - Find invalid dates in string column
-- MySQL:
-- SELECT date_column
-- FROM table_name
-- WHERE date_column IS NOT NULL
--   AND STR_TO_DATE(date_column, '%Y-%m-%d') IS NULL;

-- PostgreSQL:
-- SELECT date_column
-- FROM table_name
-- WHERE date_column IS NOT NULL
--   AND date_column !~ '^\d{4}-\d{2}-\d{2}$';

-- Query: validate_phone_format - Basic phone validation
-- MySQL:
-- SELECT phone_column
-- FROM table_name
-- WHERE phone_column IS NOT NULL
--   AND phone_column NOT REGEXP '^[+]?[0-9]{10,15}$';

-- PostgreSQL:
-- SELECT phone_column
-- FROM table_name
-- WHERE phone_column IS NOT NULL
--   AND phone_column !~ '^\+?[0-9]{10,15}$';

-- ============================================================================
-- OUTLIER DETECTION
-- ============================================================================

-- Query: iqr_outliers - Detect outliers using IQR method
-- WITH stats AS (
--     SELECT 
--         PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY column_name) AS q1,
--         PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY column_name) AS q3
--     FROM table_name
-- )
-- SELECT t.*
-- FROM table_name t, stats s
-- WHERE column_name < s.q1 - 1.5 * (s.q3 - s.q1)
--    OR column_name > s.q3 + 1.5 * (s.q3 - s.q1);

-- Query: zscore_outliers - Detect outliers using Z-score (MySQL 8.0+)
-- WITH stats AS (
--     SELECT 
--         AVG(column_name) AS mean_val,
--         STDDEV(column_name) AS std_val
--     FROM table_name
-- )
-- SELECT t.*, ABS(t.column_name - s.mean_val) / NULLIF(s.std_val, 0) AS z_score
-- FROM table_name t, stats s
-- WHERE ABS(t.column_name - s.mean_val) / NULLIF(s.std_val, 0) > 3;

-- Query: range_check - Values outside expected range
-- SELECT *
-- FROM table_name
-- WHERE column_name < min_expected OR column_name > max_expected;

-- ============================================================================
-- STATISTICAL SUMMARIES
-- ============================================================================

-- Query: column_statistics - Comprehensive column statistics
-- SELECT 
--     COUNT(*) AS row_count,
--     COUNT(column_name) AS non_null_count,
--     COUNT(DISTINCT column_name) AS distinct_count,
--     MIN(column_name) AS min_value,
--     MAX(column_name) AS max_value,
--     AVG(column_name) AS avg_value,
--     STDDEV(column_name) AS std_dev,
--     SUM(column_name) AS total_sum
-- FROM table_name;

-- Query: distribution_histogram - Value frequency distribution
-- SELECT 
--     column_name,
--     COUNT(*) AS frequency,
--     ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM table_name), 2) AS percentage
-- FROM table_name
-- GROUP BY column_name
-- ORDER BY frequency DESC;

-- Query: percentile_analysis - Percentile distribution
-- SELECT 
--     PERCENTILE_CONT(0.1) WITHIN GROUP (ORDER BY column_name) AS p10,
--     PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY column_name) AS q1,
--     PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY column_name) AS median,
--     PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY column_name) AS q3,
--     PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY column_name) AS p90
-- FROM table_name;

-- MySQL 8.0+ alternative:
-- SELECT 
--     PERCENTILE_CONT(column_name, 0.1) AS p10,
--     PERCENTILE_CONT(column_name, 0.5) AS median,
--     PERCENTILE_CONT(column_name, 0.9) AS p90
-- FROM table_name;

-- ============================================================================
-- DATA PROFILING UTILITIES
-- ============================================================================

-- Query: table_profile - Complete table profile
-- SELECT 
--     'Total Rows' AS metric, COUNT(*) AS value FROM table_name
-- UNION ALL
-- SELECT 'Distinct Values', COUNT(DISTINCT column_name) FROM table_name
-- UNION ALL
-- SELECT 'NULL Count', SUM(CASE WHEN column_name IS NULL THEN 1 ELSE 0 END) FROM table_name
-- UNION ALL
-- SELECT 'Empty String Count', SUM(CASE WHEN column_name = '' THEN 1 ELSE 0 END) FROM table_name
-- UNION ALL
-- SELECT 'Whitespace Only', SUM(CASE WHEN TRIM(column_name) = '' AND column_name IS NOT NULL THEN 1 ELSE 0 END) FROM table_name;

-- Query: pattern_analysis - Analyze string patterns
-- MySQL:
-- SELECT 
--     CASE 
--         WHEN column_name REGEXP '^[A-Z]' THEN 'Starts with uppercase'
--         WHEN column_name REGEXP '^[a-z]' THEN 'Starts with lowercase'
--         WHEN column_name REGEXP '^[0-9]' THEN 'Starts with digit'
--         ELSE 'Starts with special char'
--     END AS pattern_type,
--     COUNT(*) AS count
-- FROM table_name
-- WHERE column_name IS NOT NULL
-- GROUP BY pattern_type;

-- Query: length_analysis - String length distribution
-- SELECT 
--     LENGTH(column_name) AS string_length,
--     COUNT(*) AS frequency
-- FROM table_name
-- WHERE column_name IS NOT NULL
-- GROUP BY LENGTH(column_name)
-- ORDER BY string_length;

-- ============================================================================
-- DATA CLEANING HELPERS
-- ============================================================================

-- Query: trim_all_whitespace - Remove leading/trailing whitespace
-- UPDATE table_name 
-- SET column_name = TRIM(column_name)
-- WHERE column_name != TRIM(column_name);

-- Query: standardize_case - Standardize to lowercase
-- UPDATE table_name 
-- SET column_name = LOWER(column_name)
-- WHERE column_name != LOWER(column_name);

-- Query: remove_duplicates - Keep only first occurrence
-- MySQL:
-- DELETE t1 FROM table_name t1
-- INNER JOIN table_name t2 
-- WHERE t1.id > t2.id AND t1.column_name = t2.column_name;

-- PostgreSQL:
-- DELETE FROM table_name
-- WHERE id NOT IN (
--     SELECT MIN(id)
--     FROM table_name
--     GROUP BY column_name
-- );

-- Query: fill_null_with_default - Replace NULL with default value
-- UPDATE table_name 
-- SET column_name = 'default_value'
-- WHERE column_name IS NULL;

-- Query: fill_null_with_mean - Replace NULL with average (numeric)
-- UPDATE table_name t
-- SET column_name = (SELECT AVG(column_name) FROM table_name WHERE column_name IS NOT NULL)
-- WHERE column_name IS NULL;

-- Query: fill_null_with_median - Replace NULL with median
-- MySQL 8.0+:
-- UPDATE table_name t
-- SET column_name = (
--     SELECT MEDIAN(column_name) FROM table_name WHERE column_name IS NOT NULL
-- )
-- WHERE column_name IS NULL;

-- Query: remove_special_chars - Remove non-alphanumeric characters
-- MySQL:
-- UPDATE table_name
-- SET column_name = REGEXP_REPLACE(column_name, '[^a-zA-Z0-9]', '')
-- WHERE column_name REGEXP '[^a-zA-Z0-9]';

-- PostgreSQL:
-- UPDATE table_name
-- SET column_name = REGEXP_REPLACE(column_name, '[^a-zA-Z0-9]', '', 'g')
-- WHERE column_name ~ '[^a-zA-Z0-9]';

-- ============================================================================
-- MYSQL STORED PROCEDURES
-- ============================================================================

DELIMITER //

-- Procedure: analyze_table_quality - Comprehensive table quality report
CREATE PROCEDURE IF NOT EXISTS analyze_table_quality(
    IN table_name_param VARCHAR(255)
)
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE col_name VARCHAR(255);
    DECLARE col_type VARCHAR(255);
    DECLARE cur CURSOR FOR 
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = table_name_param;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN cur;
    
    read_loop: LOOP
        FETCH cur INTO col_name, col_type;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        SET @sql = CONCAT('SELECT 
            ''', col_name, ''' AS column_name,
            ''', col_type, ''' AS data_type,
            COUNT(*) AS total_rows,
            SUM(CASE WHEN `', col_name, '` IS NULL THEN 1 ELSE 0 END) AS null_count,
            ROUND(100.0 * SUM(CASE WHEN `', col_name, '` IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS null_pct,
            COUNT(DISTINCT `', col_name, '`) AS distinct_count,
            ROUND(100.0 * COUNT(DISTINCT `', col_name, '`) / COUNT(*), 2) AS uniqueness_pct
        FROM `', table_name_param, '`');
        
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
    END LOOP;
    
    CLOSE cur;
END //

-- Procedure: find_anomalies - Detect data anomalies
CREATE PROCEDURE IF NOT EXISTS find_anomalies(
    IN table_name_param VARCHAR(255),
    IN column_name_param VARCHAR(255)
)
BEGIN
    SET @sql = CONCAT('
        WITH stats AS (
            SELECT 
                AVG(`', column_name_param, '`) AS mean_val,
                STDDEV(`', column_name_param, '`) AS std_val,
                MIN(`', column_name_param, '`) AS min_val,
                MAX(`', column_name_param, '`) AS max_val
            FROM `', table_name_param, '`
            WHERE `', column_name_param, '` IS NOT NULL
        )
        SELECT 
            t.*,
            ABS(t.`', column_name_param, '` - s.mean_val) / NULLIF(s.std_val, 0) AS z_score
        FROM `', table_name_param, '` t, stats s
        WHERE ABS(t.`', column_name_param, '` - s.mean_val) / NULLIF(s.std_val, 0) > 3
    ');
    
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //

-- Procedure: data_quality_score - Calculate overall quality score
CREATE PROCEDURE IF NOT EXISTS data_quality_score(
    IN table_name_param VARCHAR(255)
)
BEGIN
    DECLARE total_columns INT DEFAULT 0;
    DECLARE complete_columns INT DEFAULT 0;
    DECLARE unique_columns INT DEFAULT 0;
    DECLARE quality_score DECIMAL(5,2);
    
    -- Count columns with < 5% nulls
    SELECT COUNT(*) INTO complete_columns
    FROM information_schema.columns c
    WHERE c.table_name = table_name_param
      AND EXISTS (
          SELECT 1 FROM (
              SELECT 
                  c.column_name,
                  SUM(CASE WHEN c.column_name IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS null_pct
              FROM table_name_param
          ) t
          WHERE t.null_pct < 5
      );
    
    SELECT COUNT(*) INTO total_columns
    FROM information_schema.columns 
    WHERE table_name = table_name_param;
    
    SET quality_score = (complete_columns * 100.0) / NULLIF(total_columns, 0);
    
    SELECT 
        table_name_param AS table_name,
        total_columns AS total_columns,
        complete_columns AS complete_columns,
        quality_score AS quality_score_pct;
END //

DELIMITER ;

-- ============================================================================
-- POSTGRESQL FUNCTIONS
-- ============================================================================

-- Function: detect_duplicates - Return duplicate records
-- CREATE OR REPLACE FUNCTION detect_duplicates(
--     table_name TEXT,
--     column_name TEXT
-- ) RETURNS TABLE (duplicate_value TEXT, count BIGINT) AS $$
-- BEGIN
--     RETURN QUERY EXECUTE format('
--         SELECT %I::TEXT, COUNT(*)
--         FROM %I
--         WHERE %I IS NOT NULL
--         GROUP BY %I
--         HAVING COUNT(*) > 1
--         ORDER BY COUNT(*) DESC
--     ', column_name, table_name, column_name, column_name);
-- END;
-- $$ LANGUAGE plpgsql;

-- Function: completeness_report - Generate completeness report
-- CREATE OR REPLACE FUNCTION completeness_report(
--     table_name TEXT
-- ) RETURNS TABLE (
--     column_name TEXT,
--     data_type TEXT,
--     null_count BIGINT,
--     null_pct NUMERIC,
--     distinct_count BIGINT
-- ) AS $$
-- BEGIN
--     RETURN QUERY EXECUTE format('
--         SELECT 
--             column_name::TEXT,
--             data_type::TEXT,
--             (SELECT COUNT(*) FROM %I WHERE column_name IS NULL),
--             (SELECT ROUND(100.0 * COUNT(CASE WHEN column_name IS NULL THEN 1 END) / COUNT(*), 2) FROM %I),
--             (SELECT COUNT(DISTINCT column_name) FROM %I WHERE column_name IS NOT NULL)
--         FROM information_schema.columns
--         WHERE table_name = %L
--     ', table_name, table_name, table_name, table_name);
-- END;
-- $$ LANGUAGE plpgsql;

-- ============================================================================
-- SQL SERVER STORED PROCEDURES
-- ============================================================================

-- Procedure: sp_analyze_nulls
-- CREATE PROCEDURE sp_analyze_nulls
--     @table_name NVARCHAR(255)
-- AS
-- BEGIN
--     DECLARE @sql NVARCHAR(MAX);
--     
--     SELECT @sql = STRING_AGG(
--         'SELECT ''' + COLUMN_NAME + ''' AS column_name, 
--             SUM(CASE WHEN ' + QUOTENAME(COLUMN_NAME) + ' IS NULL THEN 1 ELSE 0 END) AS null_count,
--             COUNT(*) AS total_rows
--          FROM ' + QUOTENAME(@table_name), 
--         ' UNION ALL '
--     )
--     FROM information_schema.columns
--     WHERE table_name = @table_name;
--     
--     EXEC sp_executesql @sql;
-- END;

-- Procedure: sp_data_quality_report
-- CREATE PROCEDURE sp_data_quality_report
--     @table_name NVARCHAR(255),
--     @column_name NVARCHAR(255)
-- AS
-- BEGIN
--     DECLARE @sql NVARCHAR(MAX);
--     
--     SET @sql = N'
--         SELECT 
--             ''' + @column_name + ''' AS column_name,
--             COUNT(*) AS total_rows,
--             SUM(CASE WHEN ' + QUOTENAME(@column_name) + ' IS NULL THEN 1 ELSE 0 END) AS null_count,
--             ROUND(100.0 * SUM(CASE WHEN ' + QUOTENAME(@column_name) + ' IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS null_pct,
--             COUNT(DISTINCT ' + QUOTENAME(@column_name) + ') AS distinct_values,
--             ROUND(100.0 * COUNT(DISTINCT ' + QUOTENAME(@column_name) + ') / COUNT(*), 2) AS uniqueness_pct
--         FROM ' + QUOTENAME(@table_name);
--     
--     EXEC sp_executesql @sql;
-- END;