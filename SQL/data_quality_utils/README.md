# SQL Data Quality Utilities

A comprehensive SQL data quality utility module providing data integrity checks, NULL handling, consistency validation, anomaly detection, and statistical analysis across multiple database systems.

## Features

- **NULL Value Analysis** - Count, percentage, and summary of NULL values
- **Data Completeness Metrics** - Overall and multi-column completeness scoring
- **Duplication Detection** - Find duplicates and calculate uniqueness ratios
- **Data Type Validation** - Email, phone, numeric, date format validation
- **Outlier Detection** - IQR and Z-score methods for anomaly detection
- **Statistical Summaries** - Column statistics, distributions, percentiles
- **Data Profiling** - Pattern analysis, length distribution
- **Data Cleaning Helpers** - Trim, standardize, remove duplicates

## Supported Databases

- MySQL 8.0+
- PostgreSQL 12+
- SQL Server 2019+
- SQLite 3.35+

## Quick Start

### NULL Analysis

```sql
-- Count NULL values
SELECT COUNT(*) - COUNT(column_name) AS null_count FROM table_name;

-- Calculate NULL percentage
SELECT 
    COUNT(*) AS total_rows,
    SUM(CASE WHEN column_name IS NULL THEN 1 ELSE 0 END) AS null_count,
    ROUND(100.0 * SUM(CASE WHEN column_name IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS null_percentage
FROM table_name;
```

### Duplicate Detection

```sql
-- Find duplicate values
SELECT column_name, COUNT(*) AS duplicate_count
FROM table_name
GROUP BY column_name
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC;
```

### Data Validation

```sql
-- Find invalid emails (MySQL)
SELECT email
FROM customers
WHERE email NOT REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$';
```

### Outlier Detection

```sql
-- Using Z-score method
WITH stats AS (
    SELECT AVG(column_name) AS mean, STDDEV(column_name) AS std
    FROM table_name
)
SELECT t.*, ABS(t.column_name - s.mean) / NULLIF(s.std, 0) AS z_score
FROM table_name t, stats s
WHERE ABS(t.column_name - s.mean) / NULLIF(s.std, 0) > 3;
```

## File Structure

```
data_quality_utils/
├── mod.sql                      # Main module with all utilities
├── data_quality_utils_test.sql  # Comprehensive test suite
├── examples/
│   └── basic_examples.sql       # Real-world usage examples
└── README.md                    # This file
```

## Testing

Run the test suite to verify functionality:

```bash
# MySQL
mysql -u username -p database_name < data_quality_utils_test.sql

# PostgreSQL
psql -d database_name -f data_quality_utils_test.sql
```

## Use Cases

1. **Data Migration** - Validate data quality before and after migrations
2. **ETL Processes** - Monitor data quality through transformation pipelines
3. **Regular Audits** - Schedule periodic quality checks
4. **Data Governance** - Track quality metrics over time
5. **Debugging** - Quickly identify data issues

## Contributing

Contributions are welcome! Please ensure all queries:
- Work across multiple database systems where possible
- Include comments explaining functionality
- Follow the existing code style

## License

MIT License - See LICENSE file for details.

## Author

AllToolkit - 2026-05-08