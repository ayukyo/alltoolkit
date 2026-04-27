# DOI Utils - Digital Object Identifier Utilities Module

## Overview

DOI (Digital Object Identifier) is an ISO standard (ANSI/NISO Z39.84) for persistent identifiers used primarily in academic publishing and research. This module provides comprehensive utilities for DOI validation, parsing, and manipulation with zero external dependencies.

## Features

- **DOI Validation**: Format validation with detailed error reporting
- **DOI Parsing**: Extract prefix, suffix, and generate URLs
- **URL Conversion**: Convert between DOI formats and resolvable URLs
- **Text Extraction**: Extract DOIs from text and HTML content
- **Short DOI Support**: Handle short DOI codes (base62 encoded)
- **Type Inference**: Infer resource type from DOI prefix
- **Batch Operations**: Validate multiple DOIs at once

## Installation

This module is part of AllToolkit and has zero external dependencies. Simply import:

```python
from doi_utils.mod import DOIUtils
```

## Quick Start

```python
from doi_utils.mod import validate, parse, to_url, extract_from_text

# Validate a DOI
is_valid = validate('10.1000/182')  # True

# Parse a DOI with URL prefix
result = parse('https://doi.org/10.1038/nphys1170')
print(result.doi)      # 10.1038/nphys1170
print(result.prefix)   # 10.1038
print(result.url)      # https://doi.org/10.1038/nphys1170

# Convert to URL
url = to_url('10.1000/182')  # https://doi.org/10.1000/182

# Extract DOIs from text
text = "See doi:10.1000/182 and https://doi.org/10.1038/nphys1170"
dois = extract_from_text(text)  # ['10.1000/182', '10.1038/nphys1170']
```

## Core Functions

### Validation

```python
from doi_utils.mod import validate, validate_strict

# Quick validation
if validate('10.1000/182'):
    print("Valid DOI")

# Strict validation with details
try:
    result = validate_strict('10.1000/182')
    print(f"DOI: {result['doi']}")
    print(f"Prefix: {result['prefix']}")
    print(f"Suffix: {result['suffix']}")
    print(f"URL: {result['url']}")
except InvalidDOIError as e:
    print(f"Invalid: {e}")
```

### Parsing

```python
from doi_utils.mod import parse

result = parse('doi:10.1126/science.169.3946.635')
if result.valid:
    print(f"DOI: {result.doi}")
    print(f"Prefix: {result.prefix}")
    print(f"Suffix: {result.suffix}")
    print(f"URL: {result.url}")
```

### URL Conversion

```python
from doi_utils.mod import to_url, from_url

# Convert DOI to URL
url = to_url('10.1000/182')
# https://doi.org/10.1000/182

# Legacy URL
url_legacy = to_url('10.1000/182', use_legacy=True)
# https://dx.doi.org/10.1000/182

# Extract DOI from URL
doi = from_url('https://doi.org/10.1000/182')
# 10.1000/182
```

### Text Extraction

```python
from doi_utils.mod import extract_from_text, extract_from_html

# Extract from plain text
text = """
This paper (doi:10.1038/nphys1170) discusses quantum physics.
Data: https://doi.org/10.5281/zenodo.12345
"""
dois = extract_from_text(text)
# ['10.1038/nphys1170', '10.5281/zenodo.12345']

# Extract from HTML
html = '<a href="https://doi.org/10.1000/182">Paper</a>'
dois = extract_from_html(html)
# ['10.1000/182']
```

### Type Inference

```python
from doi_utils.mod import get_doi_type

# Infer resource type from DOI prefix
print(get_doi_type('10.1038/nphys1170'))  # journal
print(get_doi_type('10.5281/zenodo.123')) # dataset
print(get_doi_type('10.1101/abc123'))     # preprint
print(get_doi_type('10.5072/thesis123'))  # thesis
```

### Short DOI

```python
from doi_utils.mod import is_short_doi, short_doi_to_url, encode_base62, decode_base62

# Check if code is a short DOI
if is_short_doi('abc'):
    url = short_doi_to_url('abc')
    # https://shortdoi.org/abc

# Base62 encoding/decoding
encoded = encode_base62(12345)  # 'd7c'
decoded = decode_base62('d7c')  # 12345
```

### Batch Operations

```python
from doi_utils.mod import validate_batch

# Validate multiple DOIs
results = validate_batch([
    '10.1000/182',
    '10.1038/nphys1170',
    'invalid'
])

for r in results:
    print(f"{r['original']}: {r['valid']}")
```

## DOI Structure

A DOI consists of two parts:
- **Prefix**: `10.XXXX` where XXXX is a 4-9 digit registrant number
- **Suffix**: `/YYYY` where YYYY can be almost any printable characters

Example: `10.1038/nphys1170`
- Prefix: `10.1038` (Nature Publishing Group)
- Suffix: `/nphys1170` (Article identifier)

## Supported DOI Formats

| Format | Example |
|--------|---------|
| Plain DOI | `10.1000/182` |
| doi: prefix | `doi:10.1000/182` |
| DOI: prefix | `DOI:10.1000/182` |
| URL (doi.org) | `https://doi.org/10.1000/182` |
| URL (dx.doi.org) | `https://dx.doi.org/10.1000/182` |

## Known DOI Registrants

Common registrant numbers and their types:
- `1038` - Nature Publishing Group (journal)
- `1126` - Science/AAAS (journal)
- `1101` - bioRxiv (preprint)
- `5281` - Zenodo (dataset)
- `5252` - figshare (dataset)
- `3310` - Dryad (dataset)
- `5072-5079` - Various universities (thesis)

## API Reference

| Function | Description |
|----------|-------------|
| `clean(doi)` | Remove URL/prefix and normalize |
| `validate(doi)` | Quick boolean validation |
| `validate_strict(doi)` | Detailed validation |
| `parse(doi)` | Parse and return DOIResult |
| `normalize(doi)` | Normalize to canonical form |
| `to_url(doi)` | Convert to resolvable URL |
| `from_url(url)` | Extract DOI from URL |
| `extract_from_text(text)` | Extract DOIs from text |
| `extract_from_html(html)` | Extract DOIs from HTML |
| `get_doi_type(doi)` | Infer resource type |
| `is_short_doi(code)` | Check short DOI pattern |
| `validate_batch(dois)` | Batch validation |

## Examples

See `examples/` directory for more usage examples.

## Testing

Run tests with:
```bash
python doi_utils_test.py
```

## License

MIT License - Part of AllToolkit

## Author

AllToolkit Contributors