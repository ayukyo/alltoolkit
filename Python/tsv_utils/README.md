# TSV Utilities

A comprehensive, zero-dependency Python library for reading, writing, and manipulating TSV (Tab-Separated Values) files and data.

## Features

- **Read TSV files** into lists or dictionaries
- **Write data to TSV files** with full control over formatting
- **Parse TSV strings** without file I/O
- **Convert data to TSV format**
- **Handle BOM (Byte Order Mark)** automatically
- **Support various line endings** (Unix, Windows, old Mac)
- **Streaming support** for large files
- **Type inference and conversion** for automatic type detection
- **Header handling** with flexible options
- **Field quoting** for special characters
- **Validation** for TSV file integrity
- **File info** retrieval
- **File merging** capabilities
- **Unicode support** for internationalization

## Installation

No installation required - this is a zero-dependency module. Simply copy `tsv_utils.py` to your project.

## Quick Start

### Reading TSV Files

```python
from tsv_utils import read_tsv, read_tsv_as_dicts

# Read as lists
headers, rows = read_tsv('data.tsv')
print(headers)  # ['name', 'age', 'city']
print(rows)     # [['Alice', '30', 'NYC'], ['Bob', '25', 'LA']]

# Read as dictionaries
data = read_tsv_as_dicts('data.tsv')
print(data)  # [{'name': 'Alice', 'age': '30', 'city': 'NYC'}, ...]
```

### Writing TSV Files

```python
from tsv_utils import write_tsv, write_tsv_from_dicts

# Write from lists
headers = ['name', 'age', 'city']
rows = [['Alice', '30', 'NYC'], ['Bob', '25', 'LA']]
write_tsv('output.tsv', headers, rows)

# Write from dictionaries
data = [
    {'name': 'Alice', 'age': '30', 'city': 'NYC'},
    {'name': 'Bob', 'age': '25', 'city': 'LA'},
]
write_tsv_from_dicts('output.tsv', data)
```

### String Operations

```python
from tsv_utils import parse_tsv_string, to_tsv_string, dicts_to_tsv_string

# Parse TSV string
tsv_content = "name\tage\nAlice\t30\nBob\t25"
headers, rows = parse_tsv_string(tsv_content)

# Convert to TSV string
headers = ['name', 'age']
rows = [['Alice', '30'], ['Bob', '25']]
tsv_output = to_tsv_string(headers, rows)

# Dictionaries to TSV string
data = [{'name': 'Alice', 'age': '30'}]
tsv_output = dicts_to_tsv_string(data)
```

## API Reference

### Reading Functions

#### `read_tsv(filepath, ...)`

Read a TSV file and return headers and rows.

```python
headers, rows = read_tsv(
    'data.tsv',
    delimiter='\t',        # Field delimiter
    has_header=True,        # First row is header
    encoding='utf-8',       # File encoding
    skip_empty_lines=True,  # Skip empty lines
    strip_whitespace=True,  # Strip field whitespace
    type_inference=False,   # Auto-convert types
    quote_char=None         # Quoting character
)
```

#### `read_tsv_as_dicts(filepath, ...)`

Read a TSV file and return a list of dictionaries.

```python
data = read_tsv_as_dicts('data.tsv', type_inference=True)
# [{'name': 'Alice', 'age': 30, 'active': True}, ...]
```

#### `read_tsv_streaming(filepath, ...)`

Stream read a TSV file in chunks for large files.

```python
for headers, chunk in read_tsv_streaming('large.tsv', chunk_size=1000):
    process_chunk(chunk)
```

#### `parse_tsv_string(content, ...)`

Parse a TSV string.

```python
headers, rows = parse_tsv_string("a\tb\n1\t2\n3\t4")
```

### Writing Functions

#### `write_tsv(filepath, headers, rows, ...)`

Write data to a TSV file.

```python
rows_written = write_tsv(
    'output.tsv',
    headers=['name', 'age'],
    rows=[['Alice', '30']],
    delimiter='\t',
    encoding='utf-8',
    newline='\n',
    quote_char='"',
    include_bom=False
)
```

#### `write_tsv_from_dicts(filepath, data, ...)`

Write a list of dictionaries to a TSV file.

```python
write_tsv_from_dicts(
    'output.tsv',
    data=[{'name': 'Alice', 'age': '30'}],
    fieldnames=['name', 'age'],  # Optional field order
    include_header=True
)
```

#### `to_tsv_string(headers, rows, ...)`

Convert data to a TSV string.

```python
tsv_string = to_tsv_string(['a', 'b'], [['1', '2']])
```

#### `dicts_to_tsv_string(data, ...)`

Convert a list of dictionaries to a TSV string.

```python
tsv_string = dicts_to_tsv_string([{'a': 1, 'b': 2}])
```

### Utility Functions

#### `validate_tsv(filepath, ...)`

Validate a TSV file for common issues.

```python
is_valid, issues = validate_tsv('data.tsv')
# is_valid: True/False
# issues: ['Inconsistent field counts: [3, 2]', ...]
```

#### `get_tsv_info(filepath, ...)`

Get information about a TSV file.

```python
info = get_tsv_info('data.tsv')
# {
#     'filepath': 'data.tsv',
#     'row_count': 100,
#     'column_count': 5,
#     'headers': ['col1', 'col2', ...],
#     'has_header': True,
#     'file_size_bytes': 2048,
#     'delimiter': '\t'
# }
```

#### `merge_tsv_files(output_filepath, input_filepaths, ...)`

Merge multiple TSV files into one.

```python
rows_written = merge_tsv_files(
    'merged.tsv',
    ['part1.tsv', 'part2.tsv', 'part3.tsv']
)
```

## Type Inference

When `type_inference=True`, the module automatically converts values:

```python
# Without type inference
['Alice', '30', '95.5', 'true', 'null']
# [str, str, str, str, str]

# With type inference
['Alice', 30, 95.5, True, None]
# [str, int, float, bool, None]
```

Supported conversions:
- Empty string → `None`
- 'null', 'none', 'nil', '~' → `None`
- 'true', 'yes', 'on', '1' → `True`
- 'false', 'no', 'off', '0' → `False`
- Integer strings → `int`
- Float strings → `float`

## Special Characters

Fields containing special characters are automatically quoted:

```python
data = [
    {'text': 'Line 1\nLine 2'},      # Newline in field
    {'text': 'Say "hello"'},         # Quotes in field
    {'text': 'Tab\there'},           # Tab in field
]
```

Output:
```
text
"Line 1\nLine 2"
"Say ""hello"""
"Tab\there"
```

## Unicode Support

Full Unicode support for internationalization:

```python
data = [
    {'language': '日本語', 'hello': 'こんにちは'},
    {'language': '中文', 'hello': '你好'},
    {'language': 'العربية', 'hello': 'مرحبا'},
]
write_tsv_from_dicts('i18n.tsv', data, encoding='utf-8')
```

## BOM Handling

Automatically detects and handles UTF-8 BOM:

```python
# Reading files with BOM
headers, rows = read_tsv('file_with_bom.tsv')  # BOM stripped automatically

# Writing files with BOM
write_tsv('output.tsv', headers, rows, include_bom=True)
```

## Custom Delimiters

While designed for TSV, the module supports other delimiters:

```python
# CSV (comma-separated)
parse_tsv_string(csv_data, delimiter=',')

# Pipe-delimited
to_tsv_string(headers, rows, delimiter='|')
```

## Running Tests

```bash
python -m unittest test_tsv_utils -v
```

## Running Examples

```bash
python examples.py
```

## License

MIT License

## Author

AllToolkit Auto-Generated Module