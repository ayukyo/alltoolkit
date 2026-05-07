# NaN Handler Utilities

A comprehensive NaN/None value handling utility module for Python with **zero external dependencies**.

## Features

### NaN Detection
- Detect NaN/None values in various data types (float, string, None)
- Detect NaN indices in lists
- Detect NaN keys in dictionaries
- Custom NaN pattern support

### NaN Statistics
- Count NaN values in collections
- Calculate NaN percentage
- Generate NaN summary reports

### NaN Conversion
- Convert NaN to None
- Convert NaN to custom default values
- Batch conversion for lists and dictionaries

### NaN Filling Strategies
- Fill with mean (for numeric data)
- Fill with median
- Fill with mode
- Fill with constant value
- Linear interpolation
- Forward/backward fill
- Custom filling function

### NaN Dropping
- Drop NaN values from lists
- Drop NaN rows/columns from 2D tables
- Drop NaN dictionary entries

### Nested Structure Handling
- Handle NaN in nested lists, dicts, tuples
- Deep NaN detection and counting

### Safe Serialization
- JSON-safe serialization (replace NaN with null)
- Safe JSON string generation

### Decorators
- `validate_no_nan` - Validate function arguments contain no NaN
- `nan_safe` - Return default value for NaN inputs

## Installation

No installation needed - part of AllToolkit. Just import:

```python
from nan_handler_utils.mod import *
```

## Quick Usage

### Detection

```python
from nan_handler_utils.mod import is_nan, nan_count, detect_nan_indices

# Check single value
is_nan(float('nan'))  # True
is_nan('N/A')         # True
is_nan(None)          # True
is_nan(42)            # False

# Detect in list
data = [1, None, 3, float('nan'), 5]
indices = detect_nan_indices(data)  # [1, 3]
count = nan_count(data)             # 2
```

### Conversion

```python
from nan_handler_utils.mod import nan_to_none, convert_nan_list

# Single value
nan_to_none(float('nan'))  # None
nan_to_none(42)            # 42

# List conversion
data = [1, None, 3, float('nan')]
convert_nan_list(data, target='none')           # [1, None, 3, None]
convert_nan_list(data, target='default', default=0)  # [1, 0, 3, 0]
convert_nan_list(data, target='remove')         # [1, 3]
```

### Filling Strategies

```python
from nan_handler_utils.mod import fill_nan_mean, fill_nan_interpolate

# Fill with mean
data = [1, float('nan'), 3, float('nan')]
fill_nan_mean(data)  # [1, 2.0, 3, 2.0]

# Interpolate
data = [1, float('nan'), 3]
fill_nan_interpolate(data, method='linear')  # [1, 2.0, 3]
fill_nan_interpolate(data, method='forward')  # [1, 1, 3]
```

### Nested Structures

```python
from nan_handler_utils.mod import convert_nan_nested, count_nan_nested

nested = {'a': 1, 'b': [None, 3], 'c': {'x': float('nan')}}
convert_nan_nested(nested, target='default', default=0)
# {'a': 1, 'b': [0, 3], 'c': {'x': 0}}

count_nan_nested(nested)  # 2
```

### Safe Serialization

```python
from nan_handler_utils.mod import safe_json_dumps

data = {'value': float('nan'), 'count': 5}
safe_json_dumps(data)  # '{"value": null, "count": 5}'
```

### Decorators

```python
from nan_handler_utils.mod import validate_no_nan, nan_safe

@validate_no_nan
def calculate(x, y):
    return x + y

calculate(1, 2)  # 3
calculate(1, float('nan'))  # Raises ValueError

@nan_safe(default=0)
def safe_square(x):
    return x * x

safe_square(4)  # 16
safe_square(float('nan'))  # 0
```

## API Reference

### Detection Functions

| Function | Description |
|----------|-------------|
| `is_nan(value, ...)` | Check if value is NaN/NaN-like |
| `is_not_nan(value, ...)` | Check if value is NOT NaN |
| `detect_nan_indices(list)` | Get indices of NaN values |
| `detect_nan_keys(dict)` | Get keys with NaN values |

### Statistics Functions

| Function | Description |
|----------|-------------|
| `nan_count(collection)` | Count NaN values |
| `nan_percentage(collection)` | Calculate NaN percentage |
| `nan_summary(collection)` | Generate NaN summary |

### Conversion Functions

| Function | Description |
|----------|-------------|
| `nan_to_none(value)` | Convert NaN to None |
| `nan_to_default(value, default)` | Convert NaN to default |
| `convert_nan_list(list, target)` | Convert NaN in list |
| `convert_nan_dict(dict, target)` | Convert NaN in dict |

### Filling Functions

| Function | Description |
|----------|-------------|
| `fill_nan_mean(list)` | Fill with mean |
| `fill_nan_median(list)` | Fill with median |
| `fill_nan_mode(list)` | Fill with mode |
| `fill_nan_constant(list, constant)` | Fill with constant |
| `fill_nan_interpolate(list, method)` | Interpolate NaN |
| `fill_nan_custom(list, func)` | Custom fill function |

### Dropping Functions

| Function | Description |
|----------|-------------|
| `drop_nan_values(list)` | Drop NaN from list |
| `drop_nan_rows(table, how)` | Drop NaN rows |
| `drop_nan_columns(table, how)` | Drop NaN columns |
| `drop_nan_dict_keys(dict)` | Drop NaN entries |

### Utility Functions

| Function | Description |
|----------|-------------|
| `get_valid_values(list)` | Extract valid values |
| `get_nan_values(list)` | Extract NaN values |
| `first_valid_index(list)` | Find first valid index |
| `last_valid_index(list)` | Find last valid index |

## Supported NaN Representations

The module recognizes these NaN string patterns:
- `nan`, `NaN`, `NAN`
- `NA`, `N/A`, `na`, `n/a`
- `null`, `NULL`, `Null`
- `none`, `NONE`, `None`
- `undefined`, `UNDEFINED`
- `-`, `--`, `---`, `.`, `..`, `...`
- `#N/A`, `#NA`, `#NULL`
- `missing`, `MISSING`
- `empty`, `EMPTY`

Plus Python's `float('nan')` and `None` by default.

## Custom NaN Patterns

```python
# Add custom NaN patterns
is_nan('CUSTOM_MISSING', custom_patterns=['CUSTOM_MISSING'])  # True

# Replace custom strings
replace_nan_strings('MY_NULL', replacement=0, patterns=['MY_NULL'])  # 0
```

## Test Results

Run tests:
```bash
python nan_handler_utils_test.py
```

## License

MIT License - Part of AllToolkit

## Author

AllToolkit Contributors

## Date

2026-05-07