# SQL Ranking Utilities

A comprehensive ranking and scoring utility module for SQL databases. Zero dependencies - uses only standard SQL window functions.

## Features

### Basic Ranking
- **RANK()** - Standard ranking with gaps for ties (e.g., 1, 1, 3, 4)
- **DENSE_RANK()** - Dense ranking without gaps (e.g., 1, 1, 2, 3)
- **ROW_NUMBER()** - Sequential numbering regardless of ties
- **NTILE()** - Divide results into N equal groups (quartiles, deciles)

### Percentile Ranking
- **PERCENT_RANK()** - Calculate percentile rank (0-1 scale)
- **CUME_DIST()** - Cumulative distribution function

### Weighted Scoring
- Custom weighted score calculations
- Score normalization (0-100 scale)
- Multi-component score aggregation

### Statistical Ranking
- **Z-score** - Standard deviations from mean
- Mean and standard deviation calculations
- Statistical ranking positions

### Leaderboard Generation
- Full leaderboard with multiple ranking types
- Top N with ties included
- Previous/next score comparisons
- Gap from leader calculations

### Running Totals
- Cumulative sum calculations
- Moving averages (configurable window)
- Group-based running totals

### Competition Ranking
- Standard competition ranking (RANK)
- Modified competition ranking (DENSE_RANK)
- Ordinal ranking (ROW_NUMBER)
- Fractional ranking for ties

### Group Ranking
- Rank within groups (teams, categories)
- Top N per group
- Group-based leaderboards

## Supported Databases

| Database | Minimum Version | Notes |
|----------|----------------|-------|
| MySQL | 8.0+ | Window functions required |
| PostgreSQL | 9.6+ | Full support |
| SQL Server | 2012+ | Full support |
| SQLite | 3.25+ | Window functions required |

## Quick Start

### Basic Leaderboard

```sql
SELECT 
    player_name,
    score,
    RANK() OVER (ORDER BY score DESC) as rank
FROM players
ORDER BY rank;
```

### Leaderboard with Percentiles

```sql
SELECT 
    player_name,
    score,
    RANK() OVER (ORDER BY score DESC) as rank,
    ROUND(PERCENT_RANK() OVER (ORDER BY score ASC) * 100, 2) as percentile
FROM players
ORDER BY rank;
```

### Top 10 with Ties

```sql
WITH ranked AS (
    SELECT 
        player_name,
        score,
        RANK() OVER (ORDER BY score DESC) as rank
    FROM players
)
SELECT * FROM ranked WHERE rank <= 10;
```

### Team Rankings

```sql
SELECT 
    team_name,
    player_name,
    score,
    RANK() OVER (PARTITION BY team_name ORDER BY score DESC) as team_rank,
    RANK() OVER (ORDER BY score DESC) as overall_rank
FROM players
ORDER BY team_name, team_rank;
```

### Running Total

```sql
SELECT 
    date,
    score,
    SUM(score) OVER (ORDER BY date) as cumulative_score
FROM daily_scores;
```

### Moving Average (3-day window)

```sql
SELECT 
    date,
    score,
    AVG(score) OVER (
        ORDER BY date 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) as moving_avg_3
FROM daily_scores;
```

### Z-Score Calculation

```sql
SELECT 
    player_name,
    score,
    (score - AVG(score) OVER ()) / 
        NULLIF(STDDEV_SAMP(score) OVER (), 0) as z_score
FROM players;
```

### Normalized Score (0-100)

```sql
SELECT 
    player_name,
    score,
    100.0 * (score - MIN(score) OVER ()) / 
        NULLIF(MAX(score) OVER () - MIN(score) OVER (), 0) as normalized_score
FROM players;
```

### Top N Per Group

```sql
WITH team_ranked AS (
    SELECT 
        team_name,
        player_name,
        score,
        ROW_NUMBER() OVER (PARTITION BY team_name ORDER BY score DESC) as team_rank
    FROM players
)
SELECT * FROM team_ranked WHERE team_rank <= 3;
```

## MySQL Stored Functions

For MySQL 8.0+, the module includes stored functions:

```sql
-- Calculate percentile for a given score
SELECT percentile_for_score(95.00, 65.00, 100.00);
-- Returns: 85.71

-- Calculate z-score
SELECT z_score_calc(100.00, 85.00, 10.00);
-- Returns: 1.5000

-- Calculate weighted score from JSON arrays
SELECT weighted_score_calc('[80, 90, 85]', '[0.4, 0.3, 0.3]');
-- Returns: 84.50
```

## Testing

Run the test suite to verify functionality:

```bash
# MySQL
mysql -u user -p database < ranking_utils_test.sql

# PostgreSQL
psql -U user -d database -f ranking_utils_test.sql

# SQL Server
sqlcmd -S server -d database -i ranking_utils_test.sql

# SQLite
sqlite3 database < ranking_utils_test.sql
```

## Test Categories

1. **Basic Rank Functions** - RANK, DENSE_RANK, ROW_NUMBER
2. **Percentile Ranking** - PERCENT_RANK, CUME_DIST, NTILE
3. **Weighted Scoring** - Custom weighted scores, normalization
4. **Z-Score Calculation** - Statistical deviation ranking
5. **Leaderboard Generation** - Full leaderboards with stats
6. **Running Totals** - Cumulative sums, moving averages
7. **Group Ranking** - Rank within groups, top N per group
8. **Advanced Patterns** - Previous/next values, fractional ranking

## Performance Tips

1. **Index your sort columns** - Window functions benefit from indexes on ORDER BY columns
2. **Limit result sets** - Use WHERE clauses before window functions
3. **Consider partition size** - Large partitions may impact performance
4. **Use CTEs for complex queries** - Improve readability and sometimes performance

## License

MIT License - Part of AllToolkit