"""
iter_utils - Usage Examples

This file demonstrates common use cases for the iter_utils module.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    chunk, batched, sliding_window, flatten, deep_flatten,
    take, take_while, drop, drop_while, unique, dedupe,
    partition, groupby_consecutive, pairwise, triplewise,
    interleave, roundrobin, Peekable, peek, is_empty,
    first, last, nth, cycle, repeat, count,
    zip_with, enumerate_with, unzip, unzip_list,
    split_at, split_after, minmax
)
from itertools import islice


def example_chunking():
    """Example: Chunking data for batch processing."""
    print("\n" + "="*60)
    print("Example 1: Chunking Data")
    print("="*60)
    
    # Processing data in batches
    data = range(1, 11)
    print(f"Original data: {list(data)}")
    
    # Split into chunks of 3
    chunks = list(chunk(range(1, 11), 3))
    print(f"Chunks of size 3: {chunks}")
    
    # Processing each chunk
    for i, batch in enumerate(chunk(range(1, 11), 3), 1):
        print(f"  Batch {i}: {batch}, sum = {sum(batch)}")
    
    # batched (Python 3.12+ backport)
    print(f"\nbatched('ABCDEFG', 3): {list(batched('ABCDEFG', 3))}")


def example_sliding_window():
    """Example: Sliding window for time series analysis."""
    print("\n" + "="*60)
    print("Example 2: Sliding Window Analysis")
    print("="*60)
    
    # Daily temperatures
    temps = [20, 22, 24, 23, 25, 27, 26, 28, 29, 30]
    print(f"Temperatures: {temps}")
    
    # 3-day moving average
    windows = sliding_window(temps, 3)
    moving_avg = [sum(w) / 3 for w in windows]
    print(f"3-day moving average: {[f'{x:.1f}' for x in moving_avg]}")
    
    # Step of 2 (every other window)
    windows_step = sliding_window(temps, 3, step=2)
    print(f"Windows with step=2: {list(windows_step)}")


def example_flatten():
    """Example: Flattening nested data structures."""
    print("\n" + "="*60)
    print("Example 3: Flattening Nested Data")
    print("="*60)
    
    # Nested lists
    nested = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
    print(f"Nested: {nested}")
    print(f"Flattened: {list(flatten(nested))}")
    
    # Deeply nested
    deep_nested = [1, [2, [3, [4, [5]]]], 6]
    print(f"\nDeeply nested: {deep_nested}")
    print(f"Deep flattened: {list(deep_flatten(deep_nested))}")
    
    # Control depth
    multi_level = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
    print(f"\nMulti-level: {multi_level}")
    print(f"Flatten depth=1: {list(flatten(multi_level, depth=1))}")
    print(f"Flatten depth=2: {list(flatten(multi_level, depth=2))}")


def example_take_drop():
    """Example: Taking and dropping elements."""
    print("\n" + "="*60)
    print("Example 4: Taking and Dropping Elements")
    print("="*60)
    
    numbers = list(range(1, 11))
    print(f"Numbers: {numbers}")
    
    # Take first 5
    print(f"Take first 5: {take(5, numbers)}")
    
    # Take while condition
    print(f"Take while < 5: {list(take_while(lambda x: x < 5, numbers))}")
    
    # Drop first 5
    print(f"Drop first 5: {list(drop(5, numbers))}")
    
    # Drop while condition
    print(f"Drop while < 5: {list(drop_while(lambda x: x < 5, numbers))}")


def example_unique_dedupe():
    """Example: Removing duplicates."""
    print("\n" + "="*60)
    print("Example 5: Removing Duplicates")
    print("="*60)
    
    # All duplicates (preserve first occurrence)
    data = [1, 2, 1, 3, 2, 4, 3, 5]
    print(f"Original: {data}")
    print(f"Unique: {list(unique(data))}")
    
    # Case-insensitive unique
    words = ['Hello', 'hello', 'World', 'WORLD', 'Test']
    print(f"\nWords: {words}")
    print(f"Unique (case-insensitive): {list(unique(words, key=str.lower))}")
    
    # Consecutive duplicates only
    log_levels = ['INFO', 'INFO', 'INFO', 'ERROR', 'ERROR', 'INFO', 'INFO']
    print(f"\nLog levels: {log_levels}")
    print(f"Dedupe (consecutive): {list(dedupe(log_levels))}")


def example_partition_groupby():
    """Example: Partitioning and grouping."""
    print("\n" + "="*60)
    print("Example 6: Partitioning and Grouping")
    print("="*60)
    
    # Partition by predicate
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    evens, odds = partition(lambda x: x % 2 == 0, numbers)
    print(f"Numbers: {numbers}")
    print(f"Evens: {evens}")
    print(f"Odds: {odds}")
    
    # Partition by sign
    values = [-3, -1, 0, 1, 2, -4, 5]
    positive, not_positive = partition(lambda x: x > 0, values)
    print(f"\nValues: {values}")
    print(f"Positive: {positive}")
    print(f"Not positive: {not_positive}")
    
    # Group consecutive
    grades = ['A', 'A', 'B', 'B', 'B', 'A', 'C', 'C']
    print(f"\nGrades: {grades}")
    grouped = list(groupby_consecutive(grades))
    for grade, items in grouped:
        print(f"  {grade}: {items}")


def example_pairwise_triplewise():
    """Example: Adjacent element iteration."""
    print("\n" + "="*60)
    print("Example 7: Adjacent Elements")
    print("="*60)
    
    # Pairwise - compare adjacent elements
    prices = [100, 105, 103, 108, 110]
    print(f"Prices: {prices}")
    
    changes = [(prev, curr, curr - prev) for prev, curr in pairwise(prices)]
    print(f"Changes: {changes}")
    
    # Triplewise - three-element patterns
    numbers = [1, 2, 3, 4, 5, 6]
    print(f"\nNumbers: {numbers}")
    triples = list(triplewise(numbers))
    print(f"Triples: {triples}")
    sums = [sum(t) for t in triples]
    print(f"Triple sums: {sums}")


def example_interleave():
    """Example: Mixing iterables."""
    print("\n" + "="*60)
    print("Example 8: Interleaving Iterables")
    print("="*60)
    
    # Interleave two sequences
    letters = ['a', 'b', 'c']
    numbers = [1, 2, 3]
    print(f"Letters: {letters}")
    print(f"Numbers: {numbers}")
    print(f"Interleaved: {list(interleave(letters, numbers))}")
    
    # Round-robin (handles different lengths)
    colors = ['red', 'green', 'blue']
    sizes = ['small']
    print(f"\nColors: {colors}")
    print(f"Sizes: {sizes}")
    print(f"Roundrobin: {list(roundrobin(colors, sizes))}")


def example_peekable():
    """Example: Peekable iterator."""
    print("\n" + "="*60)
    print("Example 9: Peekable Iterator")
    print("="*60)
    
    # Create peekable iterator
    p = Peekable(range(1, 6))
    print(f"Iterator: range(1, 6)")
    
    # Peek ahead
    print(f"Peek: {p.peek()}")
    print(f"Peek again (still 1): {p.peek()}")
    
    # Consume elements
    print(f"Next: {next(p)}")
    print(f"Next: {next(p)}")
    print(f"Peek now: {p.peek()}")
    
    # Check if empty
    print(f"\nIs empty? {p.is_empty()}")
    p.take(10)  # Take all remaining
    print(f"After take(10), is empty? {p.is_empty()}")


def example_first_last_nth():
    """Example: Getting specific elements."""
    print("\n" + "="*60)
    print("Example 10: Specific Elements")
    print("="*60)
    
    data = [10, 20, 30, 40, 50]
    print(f"Data: {data}")
    
    print(f"First: {first(data)}")
    print(f"Last: {last(data)}")
    print(f"Nth(2): {nth(2, data)}")
    print(f"Nth(-1): {nth(-1, data)}")
    
    # With default values
    empty = []
    print(f"\nEmpty list: {empty}")
    print(f"First with default: {first(empty, default='N/A')}")
    print(f"Last with default: {last(empty, default='N/A')}")
    print(f"Nth(5) with default: {nth(5, data, default='out of range')}")


def example_cycle_repeat_count():
    """Example: Infinite sequences."""
    print("\n" + "="*60)
    print("Example 11: Infinite Sequences")
    print("="*60)
    
    # Cycle
    states = ['on', 'off']
    print(f"States: {states}")
    cycled = list(islice(cycle(states), 6))
    print(f"Cycled (6): {cycled}")
    
    # Repeat
    print(f"\nRepeat('x', 5): {list(repeat('x', 5))}")
    
    # Count
    counted = list(islice(count(start=1, step=2), 5))
    print(f"Count(1, step=2) (5): {counted}")


def example_zip_enumerate():
    """Example: Zip and enumerate variations."""
    print("\n" + "="*60)
    print("Example 12: Zip and Enumerate Variations")
    print("="*60)
    
    # Zip with function
    a = [1, 2, 3]
    b = [10, 20, 30]
    print(f"a: {a}, b: {b}")
    sums = list(zip_with(lambda x, y: x + y, a, b))
    print(f"zip_with(add): {sums}")
    
    products = list(zip_with(lambda x, y: x * y, a, b))
    print(f"zip_with(multiply): {products}")
    
    # Enumerate with custom start/step
    items = ['a', 'b', 'c', 'd']
    print(f"\nItems: {items}")
    indexed = list(enumerate_with(items, start=1, step=1))
    print(f"enumerate_with(start=1): {indexed}")
    
    even_indexed = list(enumerate_with(items, start=2, step=2))
    print(f"enumerate_with(start=2, step=2): {even_indexed}")


def example_split():
    """Example: Splitting iterables."""
    print("\n" + "="*60)
    print("Example 13: Splitting Iterables")
    print("="*60)
    
    # Split at delimiter
    data = [1, 2, 3, 'delimiter', 4, 5, 6]
    print(f"Data: {data}")
    before, after = split_at(lambda x: x == 'delimiter', data)
    print(f"Split at 'delimiter': before={before}, after={after}")
    
    # Split after delimiter
    before, after = split_after(lambda x: x == 'delimiter', data)
    print(f"Split after 'delimiter': before={before}, after={after}")
    
    # Split at condition
    numbers = [1, 2, 3, 4, 5, 6, 7, 8]
    print(f"\nNumbers: {numbers}")
    before, after = split_at(lambda x: x >= 5, numbers)
    print(f"Split at >=5: before={before}, after={after}")


def example_minmax():
    """Example: Min and max in single pass."""
    print("\n" + "="*60)
    print("Example 14: Min and Max")
    print("="*60)
    
    data = [3, 1, 4, 1, 5, 9, 2, 6]
    print(f"Data: {data}")
    print(f"Minmax: {minmax(data)}")
    
    # With key function
    words = ['apple', 'banana', 'pear', 'kiwi', 'watermelon']
    print(f"\nWords: {words}")
    shortest, longest = minmax(words, key=len)
    print(f"Shortest: '{shortest}', Longest: '{longest}'")


def example_unzip():
    """Example: Unzipping tuples."""
    print("\n" + "="*60)
    print("Example 15: Unzipping")
    print("="*60)
    
    # Zipped data
    zipped = [(1, 'a'), (2, 'b'), (3, 'c')]
    print(f"Zipped: {zipped}")
    
    # Unzip to tuples
    numbers, letters = unzip(zipped)
    print(f"Unzipped: numbers={numbers}, letters={letters}")
    
    # Unzip to lists
    numbers_list, letters_list = unzip_list(zipped)
    print(f"Unzipped lists: numbers={numbers_list}, letters={letters_list}")


def example_pipeline():
    """Example: Real-world data processing pipeline."""
    print("\n" + "="*60)
    print("Example 16: Data Processing Pipeline")
    print("="*60)
    
    # Raw data: list of readings
    raw_data = [
        10.5, 10.5, 10.5, 11.2, 11.2, 12.0, 12.1, 12.0, 
        10.5, 10.5, 13.5, 13.5, 13.5
    ]
    
    print("Raw sensor readings:", raw_data)
    
    # Step 1: Remove consecutive duplicates
    deduped = list(dedupe(raw_data))
    print("After dedupe:", deduped)
    
    # Step 2: Partition into low/high values
    threshold = 12.0
    low, high = partition(lambda x: x < threshold, deduped)
    print(f"Below {threshold}: {low}")
    print(f"Above {threshold}: {high}")
    
    # Step 3: Calculate min/max for each partition
    if low:
        print(f"Low range: {minmax(low)}")
    if high:
        print(f"High range: {minmax(high)}")
    
    # Step 4: Moving average with window
    windows = sliding_window(deduped, 3)
    averages = [round(sum(w)/3, 2) for w in windows]
    print("Moving averages (window=3):", averages)


def run_all_examples():
    """Run all examples."""
    example_chunking()
    example_sliding_window()
    example_flatten()
    example_take_drop()
    example_unique_dedupe()
    example_partition_groupby()
    example_pairwise_triplewise()
    example_interleave()
    example_peekable()
    example_first_last_nth()
    example_cycle_repeat_count()
    example_zip_enumerate()
    example_split()
    example_minmax()
    example_unzip()
    example_pipeline()
    
    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60)


if __name__ == "__main__":
    run_all_examples()