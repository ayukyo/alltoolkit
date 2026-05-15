# Top-N Utils

Efficient top-N selection utilities for Python with zero external dependencies.

## Features

- **Multiple Algorithms**: Heap-based (O(N log k)), QuickSelect (O(N) average), and streaming approaches
- **Time-Windowed Top-N**: Real-time analytics with sliding windows
- **Category-Based Top-N**: Track top items per category
- **Weighted Top-N**: Combine multiple scoring dimensions
- **Incremental Top-N**: Continuously update rankings with rank tracking
- **Zero Dependencies**: Pure Python standard library

## Installation

```python
from topn_utils import (
    TopNSelector,
    heap_top_n,
    quickselect_top_n,
    streaming_top_n,
    TimeWindowTopN,
    CategoryTopN,
    WeightedTopN,
    IncrementalTopN,
    top_n,
    bottom_n,
)
```

## Quick Start

### Basic Top-N Selection

```python
from topn_utils import top_n, bottom_n

data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

# Get top 3 items
top_3 = top_n(data, 3)
# [(9, 9), (6, 6), (5, 5)]

# Get bottom 3 items
bottom_3 = bottom_n(data, 3)
# [(1, 1), (1, 1), (2, 2)]

# With custom key function
words = ["apple", "banana", "cherry", "date", "elderberry"]
longest = top_n(words, 3, key=len)
# [('elderberry', 10), ('banana', 6), ('cherry', 6)]
```

### TopNSelector Class

For incremental item addition:

```python
from topn_utils import TopNSelector

selector = TopNSelector(lambda x: x, max_size=100)

# Add items one at a time
selector.add_item(42)
selector.add_item(100)

# Or add in bulk
selector.add_items(range(1000))

# Get top N
top_10 = selector.get_top_n(10)
```

### Time-Windowed Top-N

Track trending items within a time window:

```python
from topn_utils import TimeWindowTopN

# Track top 10 items in the last 60 seconds
window = TimeWindowTopN(window_seconds=60, n=10)

window.add("article_1", score=100)
window.add("article_2", score=150)

# Old items automatically expire
top_trending = window.get_top_n(5)
```

### Category-Based Top-N

Track top items per category:

```python
from topn_utils import CategoryTopN

leaderboard = CategoryTopN(n=10)  # Top 10 per category

leaderboard.add("fruit", "apple", score=85)
leaderboard.add("fruit", "banana", score=90)
leaderboard.add("vegetable", "carrot", score=75)

top_fruits = leaderboard.get_top_n("fruit")
top_vegetables = leaderboard.get_top_n("vegetable")
all_categories = leaderboard.get_top_n_all()
```

### Weighted Top-N

Combine multiple scoring dimensions:

```python
from topn_utils import WeightedTopN

weighted = WeightedTopN()
weighted.add_weight("popularity", 0.5)
weighted.add_weight("quality", 0.3)
weighted.add_weight("recency", 0.2)

weighted.add_item("item1", {"popularity": 80, "quality": 90, "recency": 100})
weighted.add_item("item2", {"popularity": 90, "quality": 70, "recency": 50})

ranked = weighted.get_top_n()
```

### Incremental Top-N

Continuously update rankings with rank tracking:

```python
from topn_utils import IncrementalTopN

tracker = IncrementalTopN(n=100, mode="max")  # "max" or "sum"

tracker.update("player_1", score=100)
tracker.update("player_2", score=95)
tracker.update("player_1", score=110)  # Update existing

# Get rank (1-indexed)
rank = tracker.get_rank("player_1")  # Returns 1

# Get percentile
percentile = tracker.get_percentile("player_2")
```

### Streaming for Large Datasets

Memory-efficient for huge datasets:

```python
from topn_utils import streaming_top_n

# Process millions of items with minimal memory
def data_generator():
    for i in range(10000000):
        yield i * 0.1

top_100 = streaming_top_n(
    data_generator(),
    n=100,
    checkpoint_func=lambda items: print(f"Checkpoint: {len(items)} items"),
    checkpoint_interval=100000
)
```

## Algorithm Comparison

| Algorithm | Time Complexity | Space Complexity | Best For |
|-----------|-----------------|------------------|----------|
| Heap | O(N log k) | O(k) | Small k, streaming data |
| QuickSelect | O(N) avg | O(N) | Full list available, small k |
| Streaming | O(N log k) | O(k) | Large/unbounded datasets |

## API Reference

### Functions

- `heap_top_n(items, n, key, keep_ties)` - Find top-N using min-heap
- `quickselect_top_n(items, n, key)` - Find top-N using QuickSelect
- `streaming_top_n(items, n, key, checkpoint_func, checkpoint_interval)` - Streaming top-N
- `top_n(items, n, key, algorithm)` - Unified interface
- `bottom_n(items, n, key)` - Find smallest N items
- `benchmark_top_n(size, n, algorithms)` - Benchmark algorithms

### Classes

- `TopNSelector(key_func, max_size)` - Incremental selector
- `TimeWindowTopN(window_seconds, n, key_func)` - Time-windowed tracker
- `CategoryTopN(n, key_func)` - Category-based tracker
- `WeightedTopN()` - Multi-dimensional scoring
- `IncrementalTopN(n, mode)` - Continuously updated rankings

## Running Tests

```bash
python -m pytest topn_utils_test.py -v
# Or
python topn_utils_test.py
```

## Use Cases

1. **Leaderboards**: Game scores, user rankings
2. **Recommendations**: Top products, articles, videos
3. **Analytics**: Trending topics, hot items
4. **Monitoring**: Top errors, slow queries
5. **Search**: Top search results
6. **Real-time Dashboards**: Live metrics

## License

MIT License - Part of AllToolkit collection.