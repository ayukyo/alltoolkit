# iter_utils - Iterator Utilities

A comprehensive collection of iterator utilities for Python. Zero dependencies, production-ready.

## Features

- **Chunking**: Split iterables into fixed-size chunks
- **Sliding Windows**: Generate sliding windows with configurable step
- **Flattening**: Flatten nested iterables to any depth
- **Filtering**: Take, drop, take_while, drop_while
- **Deduplication**: Remove all duplicates or consecutive duplicates
- **Partitioning**: Split iterables based on predicates
- **Grouping**: Group consecutive elements
- **Adjacent Elements**: Pairwise, triplewise for adjacent iteration
- **Interleaving**: Mix multiple iterables together
- **Peeking**: Look ahead without consuming elements
- **Infinite Sequences**: Cycle, repeat, count
- **Zip Variants**: zip_with, enumerate_with custom parameters
- **Splitting**: Split at/after specific conditions
- **Min/Max**: Single-pass minimum and maximum

## Installation

```python
# Copy mod.py into your project or import directly
from iter_utils import chunk, flatten, unique
```

## Quick Start

```python
from iter_utils import chunk, flatten, unique, pairwise

# Chunk data
for batch in chunk(range(10), 3):
    print(batch)  # (0, 1, 2), (3, 4, 5), (6, 7, 8), (9,)

# Flatten nested lists
flat = list(flatten([[1, 2], [3, [4, 5]]], depth=2))
# [1, 2, 3, 4, 5]

# Remove duplicates (preserving order)
unique_items = list(unique([1, 2, 1, 3, 2]))
# [1, 2, 3]

# Get adjacent pairs
changes = [(prev, curr) for prev, curr in pairwise(prices)]
```

## API Reference

### Chunking

| Function | Description |
|----------|-------------|
| `chunk(iterable, size)` | Split into fixed-size tuples |
| `batched(iterable, n)` | Python 3.12+ itertools.batched backport |
| `sliding_window(iterable, size, step=1)` | Generate sliding windows |

### Flattening

| Function | Description |
|----------|-------------|
| `flatten(iterable, depth=1)` | Flatten to specified depth |
| `deep_flatten(iterable)` | Fully flatten all nesting |

### Filtering

| Function | Description |
|----------|-------------|
| `take(n, iterable)` | Take first n elements |
| `take_while(predicate, iterable)` | Take while predicate true |
| `drop(n, iterable)` | Drop first n elements |
| `drop_while(predicate, iterable)` | Drop while predicate true |

### Deduplication

| Function | Description |
|----------|-------------|
| `unique(iterable, key=None)` | Remove duplicates (preserve order) |
| `dedupe(iterable)` | Remove consecutive duplicates |

### Partitioning

| Function | Description |
|----------|-------------|
| `partition(predicate, iterable)` | Split into two lists |
| `groupby_consecutive(iterable, key=None)` | Group consecutive equal elements |
| `split_at(predicate, iterable)` | Split at matching element |
| `split_after(predicate, iterable)` | Split after matching element |

### Adjacent Elements

| Function | Description |
|----------|-------------|
| `pairwise(iterable)` | Generate pairs of adjacent elements |
| `triplewise(iterable)` | Generate triples of adjacent elements |
| `stagger(iterable, offsets=(-1,0,1))` | Elements at specified offsets |

### Interleaving

| Function | Description |
|----------|-------------|
| `interleave(*iterables)` | Interleave (stops at shortest) |
| `roundrobin(*iterables)` | Round-robin (continues until all exhausted) |

### Peeking

| Function | Description |
|----------|-------------|
| `Peekable(iterable)` | Iterator wrapper with peek() |
| `peek(iterable)` | Peek at first element |
| `is_empty(iterable)` | Check if empty without consuming |

### Element Access

| Function | Description |
|----------|-------------|
| `first(iterable, default=None)` | Get first element |
| `last(iterable, default=None)` | Get last element |
| `nth(n, iterable, default=None)` | Get nth element (supports negative) |

### Infinite Sequences

| Function | Description |
|----------|-------------|
| `cycle(iterable)` | Infinite cycle through iterable |
| `repeat(item, times=None)` | Repeat item n times or infinitely |
| `count(start=0, step=1)` | Infinite counting sequence |

### Utilities

| Function | Description |
|----------|-------------|
| `zip_with(func, *iterables)` | Zip and apply function |
| `enumerate_with(iterable, start=0, step=1)` | Custom enumerate |
| `unzip(iterable)` | Unzip to tuples |
| `unzip_list(iterable)` | Unzip to lists |
| `minmax(iterable, key=None)` | Min and max in single pass |

## Examples

### Batch Processing

```python
# Process records in batches of 100
for batch in chunk(records, 100):
    process_batch(batch)
```

### Moving Average

```python
# 7-day moving average
temps = [20, 22, 24, 23, 25, 27, 26, 28]
avg = [sum(w)/7 for w in sliding_window(temps, 7)]
```

### Consecutive Deduplication

```python
# Dedupe log messages (only consecutive duplicates)
logs = ['INFO', 'INFO', 'INFO', 'ERROR', 'ERROR', 'INFO']
cleaned = list(dedupe(logs))  # ['INFO', 'ERROR', 'INFO']
```

### Peekable Iterator

```python
p = Peekable(tokens)
if p.peek() == 'KEYWORD':
    handle_keyword(p)
else:
    handle_default(p)
```

### Single-pass Min/Max

```python
# Efficient for large or infinite iterables
min_val, max_val = minmax(stream)
```

## Testing

```bash
python iter_utils_test.py
```

## License

MIT License - Part of AllToolkit

## Author

AllToolkit