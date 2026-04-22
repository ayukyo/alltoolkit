-- ============================================================================
-- SQL Ranking Utilities Module
-- ============================================================================
-- A comprehensive ranking and scoring utility module for SQL providing common
-- ranking operations across multiple database systems (MySQL, PostgreSQL, 
-- SQL Server, SQLite).
--
-- Features:
-- - Basic ranking (RANK, DENSE_RANK, ROW_NUMBER)
-- - Percentile ranking
-- - Weighted scoring
-- - Leaderboard generation
-- - Score normalization
-- - Competition ranking (dense, standard, ordinal)
-- - Rank with ties handling
-- - Running totals and cumulative scoring
-- - Z-score and standard deviation ranking
--
-- Supported Databases:
-- - MySQL 8.0+ (window functions)
-- - PostgreSQL 9.6+
-- - SQL Server 2012+
-- - SQLite 3.25+ (window functions)
--
-- Author: AllToolkit
-- Version: 1.0.0
-- License: MIT
-- ============================================================================

-- ============================================================================
-- BASIC RANKING FUNCTIONS
-- ============================================================================

-- Function: rank_basic - Standard ranking with gaps for ties
-- Example: Scores 100, 100, 90 -> Ranks 1, 1, 3
-- MySQL 8.0+ / PostgreSQL / SQL Server / SQLite 3.25+:
--   SELECT 
--     player_name,
--     score,
--     RANK() OVER (ORDER BY score DESC) as rank
--   FROM players;

-- Function: rank_dense - Dense ranking without gaps for ties
-- Example: Scores 100, 100, 90 -> Ranks 1, 1, 2
-- MySQL 8.0+ / PostgreSQL / SQL Server / SQLite 3.25+:
--   SELECT 
--     player_name,
--     score,
--     DENSE_RANK() OVER (ORDER BY score DESC) as dense_rank
--   FROM players;

-- Function: rank_row_number - Sequential numbering regardless of ties
-- Example: Scores 100, 100, 90 -> Ranks 1, 2, 3
-- MySQL 8.0+ / PostgreSQL / SQL Server / SQLite 3.25+:
--   SELECT 
--     player_name,
--     score,
--     ROW_NUMBER() OVER (ORDER BY score DESC, player_name ASC) as row_num
--   FROM players;

-- Function: rank_ntile - Divide into N equal groups (quartiles, deciles)
-- Example: 10 items NTILE(4) -> Groups of 3, 3, 2, 2
-- MySQL 8.0+ / PostgreSQL / SQL Server / SQLite 3.25+:
--   SELECT 
--     player_name,
--     score,
--     NTILE(4) OVER (ORDER BY score DESC) as quartile
--   FROM players;

-- ============================================================================
-- PERCENTILE RANKING
-- ============================================================================

-- Function: percentile_rank - Calculate percentile rank (0-1)
-- Formula: (rank - 1) / (total_count - 1)
-- MySQL 8.0+:
--   SELECT 
--     player_name,
--     score,
--     PERCENT_RANK() OVER (ORDER BY score ASC) as percentile_rank
--   FROM players;

-- PostgreSQL:
--   SELECT 
--     player_name,
--     score,
--     PERCENT_RANK() OVER (ORDER BY score ASC) as percentile_rank,
--     PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY score) OVER () as median
--   FROM players;

-- SQL Server:
--   SELECT 
--     player_name,
--     score,
--     PERCENT_RANK() OVER (ORDER BY score ASC) as percentile_rank,
--     PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY score) OVER () as median
--   FROM players;

-- SQLite 3.25+:
--   SELECT 
--     player_name,
--     score,
--     PERCENT_RANK() OVER (ORDER BY score ASC) as percentile_rank
--   FROM players;

-- Function: cumulative_distribution - Cumulative distribution function
-- MySQL 8.0+ / PostgreSQL / SQL Server / SQLite 3.25+:
--   SELECT 
--     player_name,
--     score,
--     CUME_DIST() OVER (ORDER BY score ASC) as cume_dist
--   FROM players;

-- ============================================================================
-- WEIGHTED SCORING
-- ============================================================================

-- Function: weighted_score - Calculate weighted score from multiple components
-- Example: Final = 0.4 * score1 + 0.3 * score2 + 0.3 * score3
-- All Databases:
--   SELECT 
--     player_name,
--     score1,
--     score2,
--     score3,
--     (0.4 * score1 + 0.3 * score2 + 0.3 * score3) as weighted_score
--   FROM players;

-- Function: normalized_score - Normalize score to 0-100 scale
-- Formula: 100 * (score - min) / (max - min)
-- MySQL 8.0+ / PostgreSQL:
--   SELECT 
--     player_name,
--     score,
--     100.0 * (score - MIN(score) OVER ()) / 
--       NULLIF(MAX(score) OVER () - MIN(score) OVER (), 0) as normalized_score
--   FROM players;

-- SQL Server:
--   SELECT 
--     player_name,
--     score,
--     100.0 * (score - MIN(score) OVER ()) / 
--       NULLIF(MAX(score) OVER () - MIN(score) OVER (), 0) as normalized_score
--   FROM players;

-- SQLite 3.25+:
--   SELECT 
--     player_name,
--     score,
--     100.0 * (score - MIN(score) OVER ()) / 
--       NULLIF(MAX(score) OVER () - MIN(score) OVER (), 0) as normalized_score
--   FROM players;

-- ============================================================================
-- Z-SCORE AND STANDARD DEVIATION RANKING
-- ============================================================================

-- Function: z_score - Calculate z-score (standard deviations from mean)
-- Formula: (score - mean) / stddev
-- MySQL 8.0+:
--   SELECT 
--     player_name,
--     score,
--     (score - AVG(score) OVER ()) / NULLIF(STDDEV_SAMP(score) OVER (), 0) as z_score
--   FROM players;

-- PostgreSQL:
--   SELECT 
--     player_name,
--     score,
--     (score - AVG(score) OVER ()) / NULLIF(STDDEV_SAMP(score) OVER (), 0) as z_score
--   FROM players;

-- SQL Server:
--   SELECT 
--     player_name,
--     score,
--     (score - AVG(score) OVER ()) / NULLIF(STDEV(score) OVER (), 0) as z_score
--   FROM players;

-- SQLite 3.25+:
--   SELECT 
--     player_name,
--     score,
--     (score - AVG(score) OVER ()) / 
--       NULLIF(SQRT(SUM((score - AVG(score) OVER ()) * (score - AVG(score) OVER ())) OVER () / 
--         (COUNT(*) OVER () - 1)), 0) as z_score
--   FROM players;

-- ============================================================================
-- LEADERBOARD GENERATION
-- ============================================================================

-- Function: leaderboard_with_stats - Generate leaderboard with ranking statistics
-- MySQL 8.0+ / PostgreSQL / SQLite 3.25+:
--   SELECT 
--     player_name,
--     score,
--     RANK() OVER (ORDER BY score DESC) as rank,
--     DENSE_RANK() OVER (ORDER BY score DESC) as dense_rank,
--     ROW_NUMBER() OVER (ORDER BY score DESC, created_at ASC) as position,
--     PERCENT_RANK() OVER (ORDER BY score ASC) as percentile,
--     COUNT(*) OVER () as total_players,
--     LAG(score) OVER (ORDER BY score DESC) as prev_score,
--     LEAD(score) OVER (ORDER BY score DESC) as next_score
--   FROM players
--   ORDER BY score DESC;

-- SQL Server:
--   SELECT 
--     player_name,
--     score,
--     RANK() OVER (ORDER BY score DESC) as rank,
--     DENSE_RANK() OVER (ORDER BY score DESC) as dense_rank,
--     ROW_NUMBER() OVER (ORDER BY score DESC, created_at ASC) as position,
--     PERCENT_RANK() OVER (ORDER BY score ASC) as percentile,
--     COUNT(*) OVER () as total_players,
--     LAG(score) OVER (ORDER BY score DESC) as prev_score,
--     LEAD(score) OVER (ORDER BY score DESC) as next_score
--   FROM players
--   ORDER BY score DESC;

-- Function: top_n_with_ties - Get top N results including ties
-- MySQL 8.0+ / PostgreSQL / SQLite 3.25+:
--   WITH ranked AS (
--     SELECT 
--       player_name,
--       score,
--       RANK() OVER (ORDER BY score DESC) as rank
--     FROM players
--   )
--   SELECT player_name, score, rank
--   FROM ranked
--   WHERE rank <= 3
--   ORDER BY rank;

-- SQL Server:
--   WITH ranked AS (
--     SELECT 
--       player_name,
--       score,
--       RANK() OVER (ORDER BY score DESC) as rank
--     FROM players
--   )
--   SELECT player_name, score, rank
--   FROM ranked
--   WHERE rank <= 3
--   ORDER BY rank;

-- ============================================================================
-- RUNNING TOTALS AND CUMULATIVE SCORING
-- ============================================================================

-- Function: running_total - Calculate cumulative sum
-- MySQL 8.0+ / PostgreSQL / SQLite 3.25+:
--   SELECT 
--     player_name,
--     score,
--     SUM(score) OVER (ORDER BY created_at) as running_total
--   FROM players;

-- SQL Server:
--   SELECT 
--     player_name,
--     score,
--     SUM(score) OVER (ORDER BY created_at) as running_total
--   FROM players;

-- Function: running_average - Calculate moving average
-- MySQL 8.0+ / PostgreSQL / SQL Server / SQLite 3.25+:
--   SELECT 
--     player_name,
--     score,
--     AVG(score) OVER (
--       ORDER BY created_at 
--       ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
--     ) as moving_avg_3
--   FROM players;

-- Function: cumulative_score_by_group - Cumulative sum within group
-- MySQL 8.0+ / PostgreSQL / SQL Server / SQLite 3.25+:
--   SELECT 
--     team_name,
--     player_name,
--     score,
--     SUM(score) OVER (
--       PARTITION BY team_name 
--       ORDER BY created_at
--     ) as team_cumulative_score
--   FROM players;

-- ============================================================================
-- COMPETITION RANKING VARIANTS
-- ============================================================================

-- Function: competition_rank - "1224" ranking (competition style)
-- Scores: 100, 100, 90, 80 -> Ranks: 1, 1, 3, 4
-- This is the default RANK() behavior in SQL

-- Function: modified_competition_rank - "1223" ranking
-- Scores: 100, 100, 90, 80 -> Ranks: 1, 1, 2, 3
-- This is DENSE_RANK() behavior

-- Function: ordinal_ranking - Sequential ranking ignoring ties
-- This is ROW_NUMBER() behavior

-- Function: fractional_ranking - Assign fractional ranks to ties
-- Scores: 100, 100, 90, 80 -> Ranks: 1.5, 1.5, 3, 4
-- MySQL 8.0+ / PostgreSQL / SQLite 3.25+:
--   SELECT 
--     player_name,
--     score,
--     AVG(ROW_NUMBER() OVER (ORDER BY score DESC)) OVER (
--       PARTITION BY score
--     ) as fractional_rank
--   FROM players;

-- ============================================================================
-- GROUP RANKING
-- ============================================================================

-- Function: rank_within_group - Rank items within each group
-- MySQL 8.0+ / PostgreSQL / SQL Server / SQLite 3.25+:
--   SELECT 
--     team_name,
--     player_name,
--     score,
--     RANK() OVER (
--       PARTITION BY team_name 
--       ORDER BY score DESC
--     ) as team_rank
--   FROM players;

-- Function: top_n_per_group - Get top N from each group
-- MySQL 8.0+ / PostgreSQL / SQLite 3.25+:
--   WITH ranked AS (
--     SELECT 
--       team_name,
--       player_name,
--       score,
--       ROW_NUMBER() OVER (
--         PARTITION BY team_name 
--         ORDER BY score DESC
--       ) as team_rank
--     FROM players
--   )
--   SELECT team_name, player_name, score, team_rank
--   FROM ranked
--   WHERE team_rank <= 3
--   ORDER BY team_name, team_rank;

-- SQL Server:
--   WITH ranked AS (
--     SELECT 
--       team_name,
--       player_name,
--       score,
--       ROW_NUMBER() OVER (
--         PARTITION BY team_name 
--         ORDER BY score DESC
--       ) as team_rank
--     FROM players
--   )
--   SELECT team_name, player_name, score, team_rank
--   FROM ranked
--   WHERE team_rank <= 3
--   ORDER BY team_name, team_rank;

-- ============================================================================
-- MYSQL STORED FUNCTIONS (MySQL 8.0+)
-- ============================================================================

DELIMITER //

-- Function: rank_score - Return rank for a given score
CREATE FUNCTION IF NOT EXISTS rank_score(
    p_score DECIMAL(10,2),
    p_table_name VARCHAR(100),
    p_score_column VARCHAR(100)
) RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_rank INT;
    SET @sql = CONCAT(
        'SELECT COUNT(*) + 1 INTO @rank FROM ', p_table_name, 
        ' WHERE ', p_score_column, ' > ', p_score
    );
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    RETURN @rank;
END //

-- Function: percentile_for_score - Return percentile for a given score
CREATE FUNCTION IF NOT EXISTS percentile_for_score(
    p_score DECIMAL(10,2),
    p_min_score DECIMAL(10,2),
    p_max_score DECIMAL(10,2)
) RETURNS DECIMAL(5,2)
DETERMINISTIC
BEGIN
    IF p_max_score = p_min_score THEN
        RETURN 100.00;
    END IF;
    RETURN ROUND(
        100.0 * (p_score - p_min_score) / (p_max_score - p_min_score), 
        2
    );
END //

-- Function: z_score_calc - Calculate z-score
CREATE FUNCTION IF NOT EXISTS z_score_calc(
    p_score DECIMAL(10,2),
    p_mean DECIMAL(10,2),
    p_stddev DECIMAL(10,2)
) RETURNS DECIMAL(10,4)
DETERMINISTIC
BEGIN
    IF p_stddev = 0 THEN
        RETURN 0;
    END IF;
    RETURN ROUND((p_score - p_mean) / p_stddev, 4);
END //

-- Function: weighted_score_calc - Calculate weighted score from JSON components
-- Requires: MySQL 5.7+ for JSON functions
CREATE FUNCTION IF NOT EXISTS weighted_score_calc(
    p_scores JSON,
    p_weights JSON
) RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE v_result DECIMAL(10,2) DEFAULT 0;
    DECLARE v_i INT DEFAULT 0;
    DECLARE v_count INT;
    DECLARE v_score DECIMAL(10,2);
    DECLARE v_weight DECIMAL(10,2);
    
    SET v_count = JSON_LENGTH(p_scores);
    
    WHILE v_i < v_count DO
        SET v_score = JSON_EXTRACT(p_scores, CONCAT('$[', v_i, ']'));
        SET v_weight = JSON_EXTRACT(p_weights, CONCAT('$[', v_i, ']'));
        SET v_result = v_result + (v_score * v_weight);
        SET v_i = v_i + 1;
    END WHILE;
    
    RETURN ROUND(v_result, 2);
END //

DELIMITER ;

-- ============================================================================
-- POSTGRESQL FUNCTIONS
-- ============================================================================

-- Function: rank_score_postgres - Return rank for a given score
-- CREATE OR REPLACE FUNCTION rank_score(
--     p_score DECIMAL(10,2),
--     p_table_name TEXT,
--     p_score_column TEXT
-- ) RETURNS INTEGER AS $$
-- DECLARE
--     v_rank INTEGER;
-- BEGIN
--     EXECUTE format(
--         'SELECT COUNT(*) + 1 FROM %I WHERE %I > %s',
--         p_table_name, p_score_column, p_score
--     ) INTO v_rank;
--     RETURN v_rank;
-- END;
-- $$ LANGUAGE plpgsql;

-- Function: percentile_for_score - Return percentile for a given score
-- CREATE OR REPLACE FUNCTION percentile_for_score(
--     p_score DECIMAL(10,2),
--     p_min_score DECIMAL(10,2),
--     p_max_score DECIMAL(10,2)
-- ) RETURNS DECIMAL(5,2) AS $$
-- BEGIN
--     IF p_max_score = p_min_score THEN
--         RETURN 100.00;
--     END IF;
--     RETURN ROUND(
--         100.0 * (p_score - p_min_score) / (p_max_score - p_min_score), 
--         2
--     );
-- END;
-- $$ LANGUAGE plpgsql;

-- Function: z_score_calc - Calculate z-score
-- CREATE OR REPLACE FUNCTION z_score_calc(
--     p_score DECIMAL(10,2),
--     p_mean DECIMAL(10,2),
--     p_stddev DECIMAL(10,2)
-- ) RETURNS DECIMAL(10,4) AS $$
-- BEGIN
--     IF p_stddev = 0 THEN
--         RETURN 0;
--     END IF;
--     RETURN ROUND((p_score - p_mean) / p_stddev, 4);
-- END;
-- $$ LANGUAGE plpgsql;

-- ============================================================================
-- SQL SERVER FUNCTIONS
-- ============================================================================

-- Function: percentile_for_score - Return percentile for a given score
-- CREATE FUNCTION dbo.percentile_for_score(
--     @score DECIMAL(10,2),
--     @min_score DECIMAL(10,2),
--     @max_score DECIMAL(10,2)
-- ) RETURNS DECIMAL(5,2)
-- AS
-- BEGIN
--     DECLARE @result DECIMAL(5,2);
--     IF @max_score = @min_score
--         SET @result = 100.00;
--     ELSE
--         SET @result = ROUND(
--             100.0 * (@score - @min_score) / (@max_score - @min_score), 
--             2
--         );
--     RETURN @result;
-- END;
-- GO

-- Function: z_score_calc - Calculate z-score
-- CREATE FUNCTION dbo.z_score_calc(
--     @score DECIMAL(10,2),
--     @mean DECIMAL(10,2),
--     @stddev DECIMAL(10,2)
-- ) RETURNS DECIMAL(10,4)
-- AS
-- BEGIN
--     DECLARE @result DECIMAL(10,4);
--     IF @stddev = 0
--         SET @result = 0;
--     ELSE
--         SET @result = ROUND((@score - @mean) / @stddev, 4);
--     RETURN @result;
-- END;
-- GO

-- ============================================================================
-- USAGE EXAMPLES
-- ============================================================================

-- Example 1: Basic leaderboard
-- SELECT player_name, score,
--   RANK() OVER (ORDER BY score DESC) as rank
-- FROM players
-- ORDER BY rank;

-- Example 2: Leaderboard with percentiles
-- SELECT player_name, score,
--   RANK() OVER (ORDER BY score DESC) as rank,
--   PERCENT_RANK() OVER (ORDER BY score) as percentile
-- FROM players
-- ORDER BY rank;

-- Example 3: Team rankings
-- SELECT team_name, player_name, score,
--   RANK() OVER (PARTITION BY team_name ORDER BY score DESC) as team_rank,
--   RANK() OVER (ORDER BY score DESC) as overall_rank
-- FROM players
-- ORDER BY team_name, team_rank;

-- Example 4: Top 10 with ties
-- WITH ranked AS (
--   SELECT player_name, score,
--     RANK() OVER (ORDER BY score DESC) as rank
--   FROM players
-- )
-- SELECT * FROM ranked WHERE rank <= 10;

-- Example 5: Running totals
-- SELECT date, score,
--   SUM(score) OVER (ORDER BY date) as cumulative_score
-- FROM daily_scores;

-- Example 6: Moving average (3-day window)
-- SELECT date, score,
--   AVG(score) OVER (
--     ORDER BY date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
--   ) as moving_avg
-- FROM daily_scores;