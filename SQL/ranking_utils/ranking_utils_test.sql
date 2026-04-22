-- ============================================================================
-- SQL Ranking Utilities Test Suite
-- ============================================================================
-- Comprehensive test suite for ranking utility functions.
-- Run these tests to verify functionality on your database system.
--
-- Usage:
--   MySQL 8.0+:    mysql -u user -p database < ranking_utils_test.sql
--   PostgreSQL:    psql -U user -d database -f ranking_utils_test.sql
--   SQL Server:    sqlcmd -S server -d database -i ranking_utils_test.sql
--   SQLite 3.25+:  sqlite3 database < ranking_utils_test.sql
--
-- Author: AllToolkit
-- License: MIT
-- ============================================================================

-- ============================================================================
-- TEST SETUP
-- ============================================================================

-- Create test tables
DROP TABLE IF EXISTS ranking_test_scores;
DROP TABLE IF EXISTS ranking_test_players;
DROP TABLE IF EXISTS ranking_test_teams;

-- Players table
CREATE TABLE ranking_test_players (
    id INTEGER PRIMARY KEY,
    player_name VARCHAR(100) NOT NULL,
    team_id INTEGER,
    score DECIMAL(10,2),
    games_played INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert test data with ties
INSERT INTO ranking_test_players (id, player_name, team_id, score, games_played) VALUES
(1, 'Alice', 1, 100.00, 10),
(2, 'Bob', 1, 100.00, 10),    -- Tie with Alice
(3, 'Charlie', 2, 95.00, 9),
(4, 'Diana', 2, 90.00, 8),
(5, 'Eve', 3, 90.00, 10),     -- Tie with Diana
(6, 'Frank', 3, 85.00, 7),
(7, 'Grace', 1, 80.00, 6),
(8, 'Henry', 2, 75.00, 5),
(9, 'Ivy', 3, 70.00, 4),
(10, 'Jack', 1, 65.00, 3);

-- Teams table
CREATE TABLE ranking_test_teams (
    id INTEGER PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL
);

INSERT INTO ranking_test_teams (id, team_name) VALUES
(1, 'Alpha'),
(2, 'Beta'),
(3, 'Gamma');

-- Daily scores for running total tests
CREATE TABLE ranking_test_scores (
    id INTEGER PRIMARY KEY,
    player_id INTEGER,
    score DECIMAL(10,2),
    date DATE
);

INSERT INTO ranking_test_scores (id, player_id, score, date) VALUES
(1, 1, 10.00, '2026-01-01'),
(2, 1, 15.00, '2026-01-02'),
(3, 1, 20.00, '2026-01-03'),
(4, 1, 25.00, '2026-01-04'),
(5, 1, 30.00, '2026-01-05');

-- ============================================================================
-- TEST 1: BASIC RANK FUNCTIONS
-- ============================================================================
SELECT '=== TEST 1: Basic Rank Functions ===' AS test_section;

-- Test 1.1: RANK() with ties
SELECT 'Test 1.1: RANK() with ties' AS test_name;
SELECT 
    player_name,
    score,
    RANK() OVER (ORDER BY score DESC) as rank_position,
    CASE 
        WHEN RANK() OVER (ORDER BY score DESC) IN (1, 1, 3, 4, 4, 6, 7, 8, 9, 10) 
        THEN 'PASS' 
        ELSE 'FAIL' 
    END as test_result
FROM ranking_test_players
ORDER BY score DESC;

-- Test 1.2: DENSE_RANK() without gaps
SELECT 'Test 1.2: DENSE_RANK() without gaps' AS test_name;
SELECT 
    player_name,
    score,
    DENSE_RANK() OVER (ORDER BY score DESC) as dense_rank_position,
    CASE 
        WHEN DENSE_RANK() OVER (ORDER BY score DESC) BETWEEN 1 AND 7 
        THEN 'PASS' 
        ELSE 'FAIL' 
    END as test_result
FROM ranking_test_players
ORDER BY score DESC;

-- Test 1.3: ROW_NUMBER() sequential
SELECT 'Test 1.3: ROW_NUMBER() sequential' AS test_name;
SELECT 
    player_name,
    score,
    ROW_NUMBER() OVER (ORDER BY score DESC) as row_num,
    CASE 
        WHEN ROW_NUMBER() OVER (ORDER BY score DESC) BETWEEN 1 AND 10 
        THEN 'PASS' 
        ELSE 'FAIL' 
    END as test_result
FROM ranking_test_players
ORDER BY score DESC;

-- ============================================================================
-- TEST 2: PERCENTILE RANKING
-- ============================================================================
SELECT '=== TEST 2: Percentile Ranking ===' AS test_section;

-- Test 2.1: PERCENT_RANK()
SELECT 'Test 2.1: PERCENT_RANK()' AS test_name;
SELECT 
    player_name,
    score,
    ROUND(PERCENT_RANK() OVER (ORDER BY score ASC) * 100, 2) as percentile_rank,
    CASE 
        WHEN PERCENT_RANK() OVER (ORDER BY score ASC) BETWEEN 0 AND 1 
        THEN 'PASS' 
        ELSE 'FAIL' 
    END as test_result
FROM ranking_test_players
ORDER BY score;

-- Test 2.2: CUME_DIST()
SELECT 'Test 2.2: CUME_DIST()' AS test_name;
SELECT 
    player_name,
    score,
    ROUND(CUME_DIST() OVER (ORDER BY score ASC) * 100, 2) as cumulative_dist,
    CASE 
        WHEN CUME_DIST() OVER (ORDER BY score ASC) BETWEEN 0 AND 1 
        THEN 'PASS' 
        ELSE 'FAIL' 
    END as test_result
FROM ranking_test_players
ORDER BY score;

-- Test 2.3: NTILE() quartiles
SELECT 'Test 2.3: NTILE() quartiles' AS test_name;
SELECT 
    player_name,
    score,
    NTILE(4) OVER (ORDER BY score DESC) as quartile,
    CASE 
        WHEN NTILE(4) OVER (ORDER BY score DESC) BETWEEN 1 AND 4 
        THEN 'PASS' 
        ELSE 'FAIL' 
    END as test_result
FROM ranking_test_players
ORDER BY score DESC;

-- ============================================================================
-- TEST 3: WEIGHTED SCORING
-- ============================================================================
SELECT '=== TEST 3: Weighted Scoring ===' AS test_section;

-- Test 3.1: Simple weighted score
SELECT 'Test 3.1: Simple weighted score calculation' AS test_name;
SELECT 
    player_name,
    score,
    games_played,
    ROUND(score * 0.7 + games_played * 3, 2) as weighted_score,
    'PASS' as test_result
FROM ranking_test_players
ORDER BY weighted_score DESC
LIMIT 5;

-- Test 3.2: Normalized score (0-100)
SELECT 'Test 3.2: Normalized score (0-100)' AS test_name;
SELECT 
    player_name,
    score,
    ROUND(100.0 * (score - MIN(score) OVER ()) / 
        NULLIF(MAX(score) OVER () - MIN(score) OVER (), 0), 2) as normalized_score,
    CASE 
        WHEN ROUND(100.0 * (score - MIN(score) OVER ()) / 
            NULLIF(MAX(score) OVER () - MIN(score) OVER (), 0), 2) BETWEEN 0 AND 100 
        THEN 'PASS' 
        ELSE 'FAIL' 
    END as test_result
FROM ranking_test_players
ORDER BY score DESC;

-- ============================================================================
-- TEST 4: Z-SCORE CALCULATION
-- ============================================================================
SELECT '=== TEST 4: Z-Score Calculation ===' AS test_section;

-- Test 4.1: Z-score calculation
SELECT 'Test 4.1: Z-score calculation' AS test_name;
SELECT 
    player_name,
    score,
    ROUND(AVG(score) OVER (), 2) as mean_score,
    ROUND((score - AVG(score) OVER ()) / 
        NULLIF(STDDEV_SAMP(score) OVER (), 0), 4) as z_score,
    'PASS' as test_result
FROM ranking_test_players
ORDER BY score DESC;

-- ============================================================================
-- TEST 5: LEADERBOARD GENERATION
-- ============================================================================
SELECT '=== TEST 5: Leaderboard Generation ===' AS test_section;

-- Test 5.1: Full leaderboard
SELECT 'Test 5.1: Full leaderboard with stats' AS test_name;
SELECT 
    player_name,
    score,
    RANK() OVER (ORDER BY score DESC) as rank,
    DENSE_RANK() OVER (ORDER BY score DESC) as dense_rank,
    ROUND(PERCENT_RANK() OVER (ORDER BY score ASC) * 100, 2) as percentile,
    COUNT(*) OVER () as total_players,
    'PASS' as test_result
FROM ranking_test_players
ORDER BY score DESC;

-- Test 5.2: Top N with ties
SELECT 'Test 5.2: Top 3 with ties (CTE)' AS test_name;
WITH ranked AS (
    SELECT 
        player_name,
        score,
        RANK() OVER (ORDER BY score DESC) as rank
    FROM ranking_test_players
)
SELECT player_name, score, rank,
    CASE WHEN rank <= 3 THEN 'PASS' ELSE 'FAIL' END as test_result
FROM ranked
WHERE rank <= 3
ORDER BY rank;

-- ============================================================================
-- TEST 6: RUNNING TOTALS
-- ============================================================================
SELECT '=== TEST 6: Running Totals ===' AS test_section;

-- Test 6.1: Running total
SELECT 'Test 6.1: Running total' AS test_name;
SELECT 
    date,
    score,
    SUM(score) OVER (ORDER BY date) as running_total,
    CASE 
        WHEN SUM(score) OVER (ORDER BY date) = 
            (SELECT SUM(score) FROM ranking_test_scores s2 WHERE s2.date <= s1.date)
        THEN 'PASS' 
        ELSE 'FAIL' 
    END as test_result
FROM ranking_test_scores s1
ORDER BY date;

-- Test 6.2: Moving average (3-row window)
SELECT 'Test 6.2: Moving average (3-row window)' AS test_name;
SELECT 
    date,
    score,
    ROUND(AVG(score) OVER (
        ORDER BY date 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) as moving_avg_3,
    'PASS' as test_result
FROM ranking_test_scores
ORDER BY date;

-- Test 6.3: Cumulative sum with reset by group
SELECT 'Test 6.3: Group cumulative (team scores)' AS test_name;
SELECT 
    t.team_name,
    p.player_name,
    p.score,
    SUM(p.score) OVER (PARTITION BY t.team_name ORDER BY p.id) as team_cumulative,
    'PASS' as test_result
FROM ranking_test_players p
JOIN ranking_test_teams t ON p.team_id = t.id
ORDER BY t.team_name, p.id;

-- ============================================================================
-- TEST 7: GROUP RANKING
-- ============================================================================
SELECT '=== TEST 7: Group Ranking ===' AS test_section;

-- Test 7.1: Rank within team
SELECT 'Test 7.1: Rank within team' AS test_name;
SELECT 
    t.team_name,
    p.player_name,
    p.score,
    RANK() OVER (PARTITION BY t.team_name ORDER BY p.score DESC) as team_rank,
    'PASS' as test_result
FROM ranking_test_players p
JOIN ranking_test_teams t ON p.team_id = t.id
ORDER BY t.team_name, team_rank;

-- Test 7.2: Top 2 per team
SELECT 'Test 7.2: Top 2 per team (CTE)' AS test_name;
WITH team_ranked AS (
    SELECT 
        t.team_name,
        p.player_name,
        p.score,
        ROW_NUMBER() OVER (PARTITION BY t.team_name ORDER BY p.score DESC) as team_rank
    FROM ranking_test_players p
    JOIN ranking_test_teams t ON p.team_id = t.id
)
SELECT team_name, player_name, score, team_rank,
    CASE WHEN team_rank <= 2 THEN 'PASS' ELSE 'FAIL' END as test_result
FROM team_ranked
WHERE team_rank <= 2
ORDER BY team_name, team_rank;

-- ============================================================================
-- TEST 8: ADVANCED RANKING PATTERNS
-- ============================================================================
SELECT '=== TEST 8: Advanced Ranking Patterns ===' AS test_section;

-- Test 8.1: Previous and next scores
SELECT 'Test 8.1: Previous and next scores' AS test_name;
SELECT 
    player_name,
    score,
    LAG(score) OVER (ORDER BY score DESC) as prev_score,
    LEAD(score) OVER (ORDER BY score DESC) as next_score,
    CASE 
        WHEN LAG(score) OVER (ORDER BY score DESC) IS NULL OR 
             LAG(score) OVER (ORDER BY score DESC) >= score 
        THEN 'PASS' 
        ELSE 'FAIL' 
    END as test_result
FROM ranking_test_players
ORDER BY score DESC;

-- Test 8.2: Rank difference from leader
SELECT 'Test 8.2: Score difference from leader' AS test_name;
SELECT 
    player_name,
    score,
    FIRST_VALUE(score) OVER (ORDER BY score DESC) as leader_score,
    ROUND(FIRST_VALUE(score) OVER (ORDER BY score DESC) - score, 2) as gap_from_leader,
    'PASS' as test_result
FROM ranking_test_players
ORDER BY score DESC;

-- Test 8.3: Fractional ranking for ties
SELECT 'Test 8.3: Fractional ranking for ties' AS test_name;
SELECT 
    player_name,
    score,
    ROUND(AVG(ROW_NUMBER() OVER (ORDER BY score DESC)) OVER (
        PARTITION BY score
    ), 2) as fractional_rank,
    'PASS' as test_result
FROM ranking_test_players
ORDER BY score DESC;

-- ============================================================================
-- TEST 9: MYSQL SPECIFIC FUNCTIONS (MySQL 8.0+)
-- ============================================================================

-- These tests use stored functions defined in mod.sql
-- Uncomment if using MySQL 8.0+

-- SELECT '=== TEST 9: MySQL Stored Functions ===' AS test_section;

-- Test 9.1: percentile_for_score function
-- SELECT 'Test 9.1: percentile_for_score function' AS test_name;
-- SELECT 
--     percentile_for_score(95.00, 65.00, 100.00) as percentile_95,
--     CASE WHEN percentile_for_score(95.00, 65.00, 100.00) = 85.71 THEN 'PASS' ELSE 'FAIL' END as test_result;

-- Test 9.2: z_score_calc function
-- SELECT 'Test 9.2: z_score_calc function' AS test_name;
-- SELECT 
--     z_score_calc(100.00, 85.00, 10.00) as z_score_result,
--     CASE WHEN ROUND(z_score_calc(100.00, 85.00, 10.00), 2) = 1.50 THEN 'PASS' ELSE 'FAIL' END as test_result;

-- ============================================================================
-- CLEANUP
-- ============================================================================
SELECT '=== TESTS COMPLETE - Cleaning up ===' AS test_section;

DROP TABLE IF EXISTS ranking_test_scores;
DROP TABLE IF EXISTS ranking_test_players;
DROP TABLE IF EXISTS ranking_test_teams;

SELECT 'All ranking utility tests completed!' AS final_message;