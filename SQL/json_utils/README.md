# SQL JSON Utilities Module

A comprehensive JSON manipulation utility module for SQL providing common JSON operations across multiple database systems.

## Features

- **JSON Validation and Type Checking**: Validate JSON strings, check JSON types (object, array, scalar)
- **JSON Value Extraction**: Extract values by key, path, and array index
- **JSON Array Operations**: Array length, element access, contains check
- **JSON Object Operations**: Keys listing, key existence checking
- **JSON Creation**: Create JSON objects and arrays from values
- **JSON Modification**: Set, update, remove keys and array elements
- **JSON Search and Contains**: Search for values, contains checks
- **JSON Merging**: Merge objects and arrays
- **JSON Pretty Printing**: Format JSON with indentation

## Supported Databases

| Database | Minimum Version | Notes |
|----------|----------------|-------|
| MySQL | 5.7+ | Full JSON type support |
| PostgreSQL | 9.4+ | JSON and JSONB types |
| SQL Server | 2016+ | JSON functions (no native JSON type) |
| SQLite | 3.38+ | JSON1 extension required |

## Installation

### MySQL

```sql
-- Run the module file to create stored functions
SOURCE mod.sql;

-- Or execute directly
mysql -u user -p database < mod.sql
```

### PostgreSQL

```sql
-- Most functions are built-in
-- Custom functions can be created using the PostgreSQL section in mod.sql
```

### SQL Server

```sql
-- JSON functions are built-in (JSON_VALUE, JSON_MODIFY, etc.)
-- No additional installation needed
```

### SQLite

```sql
-- JSON functions require JSON1 extension
-- Available in SQLite 3.38+ by default
```

## Quick Start

### Validation

```sql
-- MySQL
SELECT JSON_VALID('{"name": "John"}') AS is_valid;  -- Returns: 1

-- PostgreSQL
SELECT '{"name": "John"}'::json IS NOT NULL AS is_valid;

-- SQL Server
SELECT ISJSON('{"name": "John"}') AS is_valid;

-- SQLite
SELECT json_valid('{"name": "John"}') AS is_valid;
```

### Extraction

```sql
-- MySQL
SELECT JSON_UNQUOTE(JSON_EXTRACT('{"name": "John"}', '$.name')) AS name;

-- PostgreSQL
SELECT '{"name": "John"}'::json->>'name' AS name;

-- SQL Server
SELECT JSON_VALUE('{"name": "John"}', '$.name') AS name;

-- SQLite
SELECT json_extract('{"name": "John"}', '$.name') AS name;
```

### Creation

```sql
-- MySQL
SELECT JSON_OBJECT('name', 'Alice', 'age', 25) AS json_obj;

-- PostgreSQL
SELECT json_build_object('name', 'Alice', 'age', 25) AS json_obj;

-- SQLite
SELECT json_object('name', 'Alice', 'age', 25) AS json_obj;
```

### Modification

```sql
-- MySQL
SELECT JSON_SET('{"name": "John"}', '$.age', 30) AS updated;

-- PostgreSQL
SELECT jsonb_set('{"name": "John"}'::jsonb, '{age}', '30'::jsonb) AS updated;

-- SQL Server
SELECT JSON_MODIFY('{"name": "John"}', '$.age', 30) AS updated;

-- SQLite
SELECT json_set('{"name": "John"}', '$.age', 30) AS updated;
```

## Custom Functions (MySQL)

The module provides custom stored functions for convenience:

| Function | Description | Example |
|----------|-------------|---------|
| `json_get_string(json, key)` | Extract string value | `json_get_string('{"name": "John"}', 'name')` |
| `json_get_number(json, key)` | Extract numeric value | `json_get_number('{"age": 30}', 'age')` |
| `json_get_bool(json, key)` | Extract boolean value | `json_get_bool('{"active": true}', 'active')` |
| `json_has_key(json, key)` | Check if key exists | `json_has_key('{"name": "John"}', 'name')` |
| `json_add_key(json, key, value)` | Add/update key | `json_add_key('{"a": 1}', 'b', 2)` |
| `json_remove_key(json, key)` | Remove key | `json_remove_key('{"a": 1, "b": 2}', 'b')` |
| `json_array_contains(arr, value)` | Check array contains | `json_array_contains('[1,2,3]', '2')` |
| `json_array_append(arr, value)` | Append to array | `json_array_append('[1,2]', 3)` |
| `json_array_element(arr, index)` | Get array element | `json_array_element('[10,20,30]', 2)` |
| `json_merge_objects(obj1, obj2)` | Merge objects | `json_merge_objects('{"a":1}', '{"b":2}')` |
| `json_is_valid(str)` | Validate JSON string | `json_is_valid('{"a": 1}')` |
| `json_type_check(json)` | Get JSON type | `json_type_check('{"a": 1}')` |
| `json_pretty_format(json)` | Pretty print JSON | `json_pretty_format('{"a":1}')` |

## JSON Path Syntax

### MySQL Path Syntax

- `$` - Root of the document
- `$.key` - Value of object member "key"
- `$[n]` - Value of array element at index n (0-based)
- `$[*]` - All elements of an array
- `$.path.to.key` - Nested path navigation
- `$.**` - All paths (wildcard)

### PostgreSQL Operators

- `->` - Get JSON element by key (returns JSON)
- `->>` - Get JSON element by key (returns text)
- `#>` - Get JSON element at path (returns JSON)
- `#>>` - Get JSON element at path (returns text)
- `@>` - Contains check (jsonb only)
- `?` - Key exists check (jsonb only)

## Testing

Run the test suite to verify all functions:

```sql
-- MySQL
SOURCE json_utils_test.sql;

-- View results
SELECT * FROM json_utils_tests;
```

## Examples

See `examples/json_utils_example.sql` for practical usage examples.

## Comparison: JSON vs JSONB (PostgreSQL)

| Feature | JSON | JSONB |
|---------|------|-------|
| Storage | Text | Binary |
| Speed (read) | Slower | Faster |
| Speed (write) | Faster | Slower |
| Indexing | Limited | Full GIN index |
| Ordering | Preserved | Not preserved |
| Duplicate keys | Allowed | Last value kept |

**Recommendation**: Use JSONB for most operations (better performance, indexing support).

## Common Use Cases

### Store user preferences

```sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    settings JSON
);

INSERT INTO users (id, name, settings) 
VALUES (1, 'Alice', '{"theme": "dark", "notifications": true}');
```

### Query JSON fields

```sql
-- MySQL
SELECT * FROM users WHERE JSON_EXTRACT(settings, '$.theme') = 'dark';

-- PostgreSQL
SELECT * FROM users WHERE settings->>'theme' = 'dark';
```

### Aggregate into JSON

```sql
-- MySQL
SELECT JSON_ARRAYAGG(name) FROM users;

-- PostgreSQL
SELECT json_agg(name) FROM users;
```

## License

MIT License

## Author

AllToolkit

## Version

1.0.0