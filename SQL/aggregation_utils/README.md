# SQL Aggregation Utilities Module

A comprehensive aggregation utility module for SQL providing advanced aggregation operations across multiple database systems (MySQL, PostgreSQL, SQL Server, SQLite).

## Features

### 1. Conditional Aggregation
- **conditional_count**: Count rows meeting specific conditions
- **conditional_sum**: Sum values meeting specific conditions
- **conditional_avg**: Average values meeting specific conditions
- **pivot_aggregation**: Create pivot table style results
- **percentage_breakdown**: Calculate percentage distribution

### 2. Statistical Aggregation
- **variance_stddev**: Variance and standard deviation (sample/population)
- **median**: Calculate median value
- **mode**: Find most frequent value
- **percentile**: Calculate any percentile (P25, P50, P75, P90, P95)
- **coefficient_of_variation**: CV (stddev/mean * 100)

### 3. String Aggregation
- **string_agg_concat**: Concatenate strings from multiple rows
- **string_agg_with_limit**: Concatenate with max length limit
- **distinct_string_agg**: Concatenate unique values only
- **conditional_string_agg**: Concatenate based on condition

### 4. JSON Aggregation
- **json_array_agg**: Build JSON array from rows
- **json_object_agg**: Build JSON object with keys
- **json_nested_agg**: Build nested JSON structure

### 5. Time-Series Aggregation
- **period_aggregation**: Aggregate by time period (month, quarter, year)
- **hourly_aggregation**: Aggregate by hour of day
- **day_of_week_aggregation**: Aggregate by day of week
- **sliding_window_aggregation**: Moving averages/sums
- **month_over_month**: Compare current vs previous period

### 6. Grouping Enhancements
- **rollup_aggregation**: Hierarchical subtotals
- **cube_aggregation**: All dimension combinations
- **grouping_sets**: Custom grouping combinations

### 7. Aggregate Filtering
- **filter_clause**: FILTER clause for selective aggregation
- **having_with_aggregate**: HAVING with aggregate conditions
- **multiple_having_conditions**: Complex HAVING conditions

### 8. Cumulative Aggregations
- **running_total**: Cumulative sum over ordered rows
- **running_count**: Cumulative count
- **running_average**: Moving/cumulative average
- **partitioned_running_total**: Running total within groups
- **year_to_date**: YTD aggregations

### 9. Advanced Grouping
- **hierarchical_aggregation**: Group by hierarchical levels
- **bucket_aggregation**: Group values into buckets/ranges
- **ntile_bucketing**: Divide into N equal-sized buckets
- **first_last_aggregation**: First and last values in groups
- **lag_lead_aggregation**: Compare with previous/next rows

### 10. Utility Functions
- **count_distinct_combinations**: Count unique combinations
- **null_handling_in_aggregates**: NULL-aware aggregation
- **weighted_average**: Calculate weighted average
- **deduplicated_count**: Count distinct with conditions
- **top_n_per_group**: Get top N items per group
- **bottom_n_per_group**: Get bottom N items per group

## Supported Databases

| Feature | MySQL 8.0+ | PostgreSQL 9.6+ | SQL Server 2012+ | SQLite 3.25+ |
|---------|------------|-----------------|------------------|---------------|
| Window Functions | ✅ | ✅ | ✅ | ✅ |
| ROLLUP/CUBE | ✅ | ✅ | ✅ | ⚠️ Limited |
| FILTER Clause | ❌ (use CASE) | ✅ | ❌ (use CASE) | ❌ (use CASE) |
| PERCENTILE_CONT | ✅ | ✅ | ✅ | ❌ (manual) |
| STRING_AGG | GROUP_CONCAT | STRING_AGG | STRING_AGG | GROUP_CONCAT |
| JSON Aggregation | ✅ | ✅ | ✅ | ❌ |
| LAG/LEAD | ✅ | ✅ | ✅ | ✅ |

## Quick Examples

### Conditional Aggregation (Pivot Table)
```sql
SELECT 
    product,
    SUM(CASE WHEN EXTRACT(MONTH FROM sale_date) = 1 THEN quantity ELSE 0 END) as jan_sales,
    SUM(CASE WHEN EXTRACT(MONTH FROM sale_date) = 2 THEN quantity ELSE 0 END) as feb_sales,
    SUM(CASE WHEN EXTRACT(MONTH FROM sale_date) = 3 THEN quantity ELSE 0 END) as mar_sales
FROM sales
GROUP BY product;
```

### Running Total with Partition
```sql
SELECT 
    department,
    employee_name,
    salary,
    SUM(salary) OVER (
        PARTITION BY department 
        ORDER BY salary DESC
    ) as dept_running_total
FROM employees
ORDER BY department, salary DESC;
```

### Month-over-Month Comparison
```sql
WITH monthly AS (
    SELECT 
        STRFTIME('%Y-%m', sale_date) as month,
        SUM(amount) as total_sales
    FROM sales
    GROUP BY STRFTIME('%Y-%m', sale_date)
),
with_previous AS (
    SELECT 
        month,
        total_sales,
        LAG(total_sales) OVER (ORDER BY month) as prev_month
    FROM monthly
)
SELECT 
    month,
    total_sales,
    ROUND((total_sales - prev_month) * 100.0 / NULLIF(prev_month, 0), 2) as pct_change
FROM with_previous;
```

### Top N Per Group
```sql
WITH ranked AS (
    SELECT 
        department,
        employee_name,
        salary,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rn
    FROM employees
)
SELECT department, employee_name, salary
FROM ranked
WHERE rn <= 3
ORDER BY department, rn;
```

### ROLLUP for Subtotals
```sql
SELECT 
    COALESCE(region, 'ALL REGIONS') as region,
    COALESCE(product, 'ALL PRODUCTS') as product,
    SUM(amount) as total_sales,
    GROUPING(region) as is_region_total,
    GROUPING(product) as is_product_total
FROM sales_data
GROUP BY ROLLUP(region, product)
ORDER BY region, product;
```

## Files

- `mod.sql` - Main module with all function implementations and examples
- `aggregation_utils_test.sql` - Comprehensive test suite
- `README.md` - This documentation

## Usage

1. Choose the appropriate SQL syntax for your database
2. Copy the relevant function pattern from `mod.sql`
3. Adapt table names and column names to your schema
4. Run and verify results

## Testing

Execute the test suite:
```bash
# SQLite
sqlite3 your_database.db < aggregation_utils_test.sql

# PostgreSQL
psql -d your_database -f aggregation_utils_test.sql

# MySQL
mysql your_database < aggregation_utils_test.sql

# SQL Server
sqlcmd -S server -d database -i aggregation_utils_test.sql
```

## Notes

- Most functions use standard SQL window functions
- Some syntax variations exist between databases (noted in comments)
- SQLite has limited support for ROLLUP/CUBE (use UNION ALL for older versions)
- JSON aggregation requires MySQL 5.7+, PostgreSQL, or SQL Server 2016+
- Performance may vary based on data size and indexing

## Author

AllToolkit

## Version

1.0.0

## License

MIT

## Date

2026-05-07