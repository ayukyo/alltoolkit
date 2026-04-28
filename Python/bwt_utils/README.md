# BWT (Burrows-Wheeler Transform) Utilities

A comprehensive, zero-dependency Python implementation of the Burrows-Wheeler Transform and related algorithms for compression and text processing.

## Features

- **BWT Transform**: Forward and inverse Burrows-Wheeler Transform
- **MTF Encoding**: Move-to-Front encoding and decoding
- **Combined Pipeline**: BWT + MTF compression preprocessing
- **Pattern Search**: BWT-based pattern matching (FM-index style)
- **Compression Analysis**: Analyze compression potential of data

## Installation

No installation required. Simply copy the `bwt_utils` folder to your project.

## Quick Start

```python
from bwt_utils.mod import bwt_transform, bwt_inverse

# Basic transform
original = "banana"
transformed, index = bwt_transform(original)
recovered = bwt_inverse(transformed, index)
print(recovered)  # "banana"
```

## API Reference

### Core Functions

#### `bwt_transform(data: str | bytes) -> Tuple[str | bytes, int]`

Perform Burrows-Wheeler Transform on input data.

```python
transformed, index = bwt_transform("mississippi")
# transformed: "ipsm$pissii", index: 4
```

#### `bwt_inverse(transformed: str | bytes, index: int) -> str | bytes`

Perform inverse Burrows-Wheeler Transform.

```python
original = bwt_inverse("ipsm$pissii", 4)
# original: "mississippi"
```

### MTF Functions

#### `mtf_encode(data: str | bytes, alphabet: Optional[str | bytes] = None) -> List[int]`

Perform Move-to-Front encoding.

```python
codes = mtf_encode("aaabbbaaa")
# codes: [0, 0, 0, 1, 1, 1, 1, 1, 1]
```

#### `mtf_decode(codes: List[int], alphabet: str | bytes) -> str | bytes`

Perform Move-to-Front decoding.

```python
result = mtf_decode([0, 0, 0, 1, 1, 1, 1, 1, 1], "ab")
# result: "aaabbbaaa"
```

### Combined Pipeline

#### `bwt_mtf_compress(data: str | bytes) -> Tuple[List[int], int, str | bytes]`

Combined BWT + MTF transform (first stage of bzip2-like compression).

```python
codes, index, alphabet = bwt_mtf_compress("banana")
recovered = bwt_mtf_decompress(codes, index, alphabet)
```

### Pattern Search

#### `bwt_search(text: str, pattern: str) -> List[int]`

Search for pattern using BWT-based approach.

```python
positions = bwt_search("banana", "ana")
# positions: [1, 3]
```

### Analysis

#### `bwt_compress_ratio(data: str | bytes) -> dict`

Analyze compression potential.

```python
analysis = bwt_compress_ratio("aaaa")
# {
#   'compression_potential': 'high',
#   'small_code_ratio': 1.0,
#   ...
# }
```

### Object-Oriented Interface

```python
from bwt_utils.mod import BWT

bwt = BWT("mississippi")
transformed = bwt.transform()
positions = bwt.search("iss")
analysis = bwt.analyze()
recovered = BWT.inverse(transformed, bwt.index)
```

## How It Works

### Burrows-Wheeler Transform

The BWT rearranges characters to group similar characters together:

```
Input:  "banana"
Step 1: Add sentinel character -> "banana$"
Step 2: Generate all rotations
Step 3: Sort rotations lexicographically
Step 4: Take last column -> "annb$aa"
Step 5: Remember position of original string -> index 3
```

The transformed text has many repeated characters adjacent, making it highly compressible.

### Move-to-Front Encoding

MTF converts repeated characters into smaller integers:

```
Input:     "aaabbb"
Alphabet:  "ab"
Codes:     [0, 0, 0, 1, 1, 1]

'a' is at index 0 in alphabet -> output 0
'b' moves to front -> 'a' now at index 1
'b' is now at index 0 -> output 1
```

Small integers compress very well with entropy coding (Huffman, Arithmetic).

## Compression Pipeline

A typical bzip2-style compression pipeline:

```
Input → BWT → MTF → RLE → Huffman → Output
```

This module provides the BWT and MTF stages.

## Performance

| Operation | Time | Space |
|-----------|------|-------|
| Transform | O(n² log n)* | O(n) |
| Inverse | O(n) | O(n) |
| Search | O(m + k) | O(n) |

*This implementation uses naive sorting. Production systems use O(n) suffix arrays.

## Use Cases

- **Data Compression**: Preprocessing for bzip2-like compressors
- **Genomics**: DNA sequence compression and search
- **Text Indexing**: Full-text search with FM-index
- **Pattern Matching**: Efficient substring search

## Running Tests

```bash
python -m pytest Python/bwt_utils/bwt_utils_test.py -v
```

Or directly:

```bash
python Python/bwt_utils/bwt_utils_test.py
```

## Examples

See `examples/usage_examples.py` for comprehensive usage demonstrations.

## License

Part of the AllToolkit project.