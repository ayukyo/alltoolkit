# Grapheme Cluster Utilities

A pure Python implementation for handling Unicode grapheme clusters. Correctly processes emoji, combining characters, and complex scripts. Zero external dependencies.

## What is a Grapheme Cluster?

A "grapheme cluster" is what users perceive as a single character. For example:

- The family emoji "👨‍👩‍👧‍👦" is **7 code points** but **1 grapheme cluster**
- The Hindi word "नमस्ते" is **6 code points** but **4 grapheme clusters**
- The letter "é" can be **1 code point** (U+00E9) or **2 code points** ('e' + U+0301 combining accent), but both are **1 grapheme cluster**

## Features

- ✅ Count grapheme clusters (not code points)
- ✅ Split strings by grapheme clusters
- ✅ Slice strings by grapheme index
- ✅ Reverse strings by grapheme
- ✅ Find and replace by grapheme
- ✅ Detect combining characters, emoji, ZWJ sequences
- ✅ Truncate and pad by grapheme count
- ✅ Get detailed grapheme information
- ✅ Unicode normalization support
- ✅ Zero external dependencies

## Installation

Copy the `grapheme_utils` folder to your project.

## Quick Start

```python
from grapheme_utils.mod import (
    grapheme_count, grapheme_split, grapheme_slice,
    grapheme_reverse, grapheme_info
)

# Count graphemes
text = "👨‍👩‍👧‍👦"  # Family emoji
print(f"Code points: {len(text)}")  # 7
print(f"Graphemes: {grapheme_count(text)}")  # 1

# Split string
print(grapheme_split("café"))  # ['c', 'a', 'f', 'é']

# Slice by grapheme index
text = "👨‍👩‍👧‍👦Hello"
print(grapheme_slice(text, 0, 1))  # '👨‍👩‍👧‍👦'
print(grapheme_slice(text, 1, 3))  # 'He'

# Reverse
print(grapheme_reverse("hello"))  # 'olleh'
print(grapheme_reverse("👋👨‍👩‍👧‍👦"))  # '👨‍👩‍👧‍👦👋'

# Get detailed info
info = grapheme_info("👨‍👩‍👧‍👦")
print(info[0]['is_emoji'])  # True
print(info[0]['has_zwj'])    # True
```

## API Reference

### Core Functions

| Function | Description |
|----------|-------------|
| `grapheme_count(text)` | Count grapheme clusters in a string |
| `grapheme_split(text)` | Split string into list of grapheme clusters |
| `grapheme_slice(text, start, end)` | Slice string by grapheme indices |
| `grapheme_reverse(text)` | Reverse string by grapheme clusters |
| `grapheme_at(text, index)` | Get grapheme at specific index |
| `graphemes(text)` | Iterator over grapheme clusters |

### Search Functions

| Function | Description |
|----------|-------------|
| `grapheme_find(text, substring)` | Find substring, return grapheme index |
| `grapheme_contains(text, substring)` | Check if substring exists |
| `grapheme_index(text, grapheme)` | Find index of specific grapheme |
| `grapheme_replace(text, old, new, count)` | Replace occurrences |

### Utility Functions

| Function | Description |
|----------|-------------|
| `grapheme_info(text)` | Get detailed info about each grapheme |
| `truncate_graphemes(text, max, ellipsis)` | Truncate to max graphemes |
| `pad_graphemes(text, length, char, side)` | Pad string to grapheme length |
| `grapheme_equal(text1, text2, normalize)` | Compare strings by grapheme |
| `normalize_graphemes(text, form)` | Normalize Unicode (NFC/NFD/NFKC/NFKD) |

### Detection Functions

| Function | Description |
|----------|-------------|
| `is_combining_mark(char)` | Check if character is a combining mark |
| `is_variation_selector(char)` | Check if character is a variation selector |
| `is_zwj(char)` | Check if character is zero-width joiner |
| `is_regional_indicator(char)` | Check if character is a regional indicator |
| `is_emoji_modifier(char)` | Check if character is an emoji modifier |

### Conversion Functions

| Function | Description |
|----------|-------------|
| `graphemes_to_code_points(text)` | Convert string to code point list |
| `code_points_to_graphemes(code_points)` | Convert code points to string |
| `grapheme_length_in_bytes(text, encoding)` | Get byte length of each grapheme |

## Examples

### Handling Emoji

```python
from grapheme_utils.mod import grapheme_count, grapheme_split

# Family emoji (ZWJ sequence)
family = "👨‍👩‍👧‍👦"
print(grapheme_count(family))  # 1 (one grapheme cluster)

# Flag emoji (two regional indicators)
flag = "🇺🇸"
print(grapheme_count(flag))  # 1 (one grapheme cluster)

# Emoji with skin tone
thumbs = "👍🏽"
print(grapheme_count(thumbs))  # 1 (one grapheme cluster)
```

### Handling Combining Characters

```python
from grapheme_utils.mod import grapheme_equal, normalize_graphemes

# Two ways to write é
precomposed = "é"           # U+00E9
decomposed = "e\u0301"      # 'e' + combining acute accent

print(len(precomposed))      # 1 code point
print(len(decomposed))       # 2 code points

# But they're grapheme-equivalent
print(grapheme_equal(precomposed, decomposed))  # True

# Normalize for consistent comparison
print(normalize_graphemes(decomposed, 'NFC') == precomposed)  # True
```

### Text Processing

```python
from grapheme_utils.mod import truncate_graphemes, pad_graphemes

# Truncate long text
long_text = "This is a very long sentence with emoji 👨‍👩‍👧‍👦"
short = truncate_graphemes(long_text, 10)
print(short)  # "This is a ..."

# Pad text
print(pad_graphemes("Hi", 10))              # "Hi        "
print(pad_graphemes("Hi", 10, side='left'))  # "        Hi"
print(pad_graphemes("Hi", 10, side='center')) # "    Hi    "
```

## Use Cases

1. **Text Editors** - Proper cursor movement and text selection
2. **Social Media** - Character limits that match user perception
3. **Search** - Correct substring matching
4. **Data Validation** - Accurate length validation
5. **Internationalization** - Proper handling of complex scripts

## Unicode Standard

This implementation follows [UAX #29: Unicode Text Segmentation](https://unicode.org/reports/tr29/) for grapheme cluster boundaries, with simplified rules for common use cases.

## Running Tests

```bash
python -m pytest grapheme_utils_test.py -v
```

## License

MIT License - Part of AllToolkit