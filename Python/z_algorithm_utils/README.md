# Z Algorithm Utilities (z_algorithm_utils)

A comprehensive, zero-dependency implementation of the Z-algorithm for efficient string matching and pattern searching in Python.

## Features

- **Z-Array Computation**: O(n) algorithm for computing Z-values
- **Pattern Matching**: Find all/first occurrences using Z-algorithm
- **Substring Analysis**: Longest repeated substring, common prefixes
- **Period Detection**: Minimal period, rotation detection
- **Palindrome Extensions**: Longest palindromic prefix/suffix
- **String Similarity**: LCP-based similarity scoring
- **Compression**: Find repeating patterns for compression
- **Multi-Pattern Matching**: Batch search with ZPatternMatcher
- **Bytes Support**: Works with byte sequences too

## Quick Start

```python
from z_algorithm_utils import mod as z

# Compute Z-array
z_values = z.z_array("aabcaabxaaz")
print(z_values)  # [0, 1, 0, 0, 3, 1, 0, 0, 2, 1, 0]

# Find pattern occurrences
positions = z.find_all_occurrences("abc", "abcabcabc")
print(positions)  # [0, 3, 6]

# Find longest repeated substring
substr, positions = z.longest_repeated_substring("banana")
print(substr)  # "ana"

# Check string period
period = z.find_minimal_period("abcabcabc")
print(period.period)  # 3
print(period.is_periodic)  # True
```

## Z-Algorithm Explained

The Z-algorithm computes an array Z where Z[i] is the length of the longest substring starting at position i that matches the prefix of the string.

For example, for `"aabcaabxaaz"`:
- Z[1] = 1: `s[1:]` = `"abcaabxaaz"`, prefix match = `"a"` (length 1)
- Z[4] = 3: `s[4:]` = `"aabxaaz"`, prefix match = `"aab"` (length 3)
- Z[8] = 2: `s[8:]` = `"aaz"`, prefix match = `"aa"` (length 2)

This allows O(n) pattern matching when combined with sentinel concatenation.

## Core Functions

### Z-Array Computation

```python
from z_algorithm_utils import mod as z

# Basic Z-array
z_arr = z.z_array("abcabc")  # [0, 0, 0, 3, 0, 0]

# For bytes
z_arr = z.z_array_bytes(b"abcabc")

# With sentinel for pattern matching
z_arr = z.z_array_with_sentinel("pattern", "text")
```

### Pattern Matching

```python
from z_algorithm_utils import mod as z

# Find all occurrences
positions = z.find_all_occurrences("abc", "abcabcabc")
# [0, 3, 6]

# Find first occurrence
pos = z.find_first_occurrence("abc", "xyzabc")
# 3

# Count occurrences
count = z.count_occurrences("ana", "banana")
# 2

# Iterate (memory-efficient for large texts)
for pos in z.iter_occurrences("abc", "abcabcabc"):
    print(pos)

# Find matches with details
matches = z.find_matches("abc", "abcabc")
for m in matches:
    print(f"Found at {m.index}: '{m.matched_substring}'")
```

### Substring Analysis

```python
from z_algorithm_utils import mod as z

# Longest prefix that is also suffix
length = z.longest_prefix_suffix("ababa")
# 3 (prefix "aba" matches suffix "aba")

# Longest repeated substring
substr, positions = z.longest_repeated_substring("banana")
# substr = "ana", positions = [1, 3]

# All repeated substrings
repeats = z.find_all_repeated_substrings("banana", min_length=2)
for substr, positions in repeats:
    print(f"'{substr}' appears at {positions}")

# Longest common prefix
lcp = z.longest_common_prefix("abcdef", "abcxyz")
# 3
```

### Period Detection

```python
from z_algorithm_utils import mod as z

# Find minimal period
period = z.find_minimal_period("abcabcabc")
print(period.period)       # 3
print(period.is_periodic)  # True
print(period.period_string)  # "abc"

# Check rotation
z.is_rotation("abcde", "cdeab")  # True

# All unique rotations
rotations = z.find_all_rotations("abc")
# ["abc", "bca", "cab"]
```

### Palindrome Operations

```python
from z_algorithm_utils import mod as z

# Longest palindromic prefix
prefix = z.longest_palindromic_prefix("abaxyz")
# "aba"

# Longest palindromic suffix
suffix = z.longest_palindromic_suffix("xyzaba")
# "aba"
```

### Similarity

```python
from z_algorithm_utils import mod as z

# Similarity score (based on LCP)
score = z.similarity_score("abcdef", "abcxyz")
# 0.5 (3 common prefix chars / 6 max length)

# Batch similarity
scores = z.batch_similarity("base", ["match", "base", "xyz"])
```

### Compression

```python
from z_algorithm_utils import mod as z

# Find repeating pattern
pattern, count = z.compress_string("abcabcabc")
# pattern = "abc", count = 3

# Decompress
restored = z.decompress_string("abc", 3)
# "abcabcabc"

# Distinct substring count
count = z.distinct_substring_count("abc")
# 6 (a, b, c, ab, bc, abc)
```

## ZPatternMatcher Class

For multi-pattern matching:

```python
from z_algorithm_utils import mod as z

matcher = z.ZPatternMatcher(["error", "warning", "info"])

# Search all patterns
results = matcher.search("error: file not found, warning: deprecated")
for pattern_idx, pos, pattern in results:
    print(f"'{pattern}' at position {pos}")

# Find first match
first = matcher.search_first("warning: check error")
# (pattern_idx=1, pos=0, pattern="warning")

# Count all
counts = matcher.count_all("error error warning info info info")
# {"error": 2, "warning": 1, "info": 3}
```

## Advanced Features

### Z-Array Visualization

```python
from z_algorithm_utils import mod as z

print(z.visualize_z_array("aaaa"))
# String: aaaa
# Index:   0  1  2  3
# Char:    a  a  a  a
# Z:       0  3  2  1
```

### Border Array Conversion

```python
from z_algorithm_utils import mod as z

# Convert Z-array to border array (KMP failure function)
z_arr = z.z_array("abcabcabc")
border = z.z_to_border(z_arr)

# Convert back
z_back = z.border_to_z(border)
```

## Time Complexity

| Operation | Time | Space |
|-----------|------|-------|
| z_array | O(n) | O(n) |
| find_all_occurrences | O(n+m) | O(n+m) |
| find_first_occurrence | O(n+m) | O(n+m) |
| longest_prefix_suffix | O(n) | O(n) |
| longest_repeated_substring | O(n²) | O(n) |
| find_minimal_period | O(n) | O(n) |
| is_rotation | O(n) | O(n) |

## Use Cases

- **Text Search**: Efficient pattern matching in documents
- **DNA Sequence Analysis**: Finding repeated sequences in DNA
- **Data Compression**: Identifying repeating patterns
- **Spell Checking**: Similarity-based word matching
- **Code Analysis**: Finding repeated code patterns
- **Log Analysis**: Multi-pattern log search
- **String Validation**: Period and rotation checks

## Zero Dependencies

This module uses only Python standard library:
- `typing` - Type hints
- `dataclasses` - Result objects
- No external packages required

## Algorithm Background

The Z-algorithm was introduced by Dan Gusfield in 1997. It provides a linear-time method for computing the Z-array, which encodes information about all substring matches with the prefix.

The key insight is that by maintaining a "Z-box" (the rightmost interval [l, r] where s[l:r+1] is a prefix match), we can compute subsequent Z-values efficiently:

1. If position i is within a Z-box, we can use previous Z-value as a starting estimate
2. Otherwise, we compare characters directly
3. We then extend the match as far as possible

This elegant algorithm has applications in:
- Pattern matching (via sentinel concatenation)
- Finding all border lengths
- Computing prefix-suffix matches
- Period detection

## License

MIT License - Part of AllToolkit