"""
iter_utils - Iterator Utilities

A comprehensive collection of iterator utilities for Python.
Zero dependencies - uses only Python standard library.

Features:
- chunk: Split iterables into fixed-size chunks
- sliding_window: Sliding window over iterables
- flatten: Flatten nested iterables
- take/take_while/drop/drop_while: Iterator filtering
- unique/dedupe: Remove duplicates
- partition: Split based on predicate
- groupby_consecutive: Group consecutive equal elements
- pairwise/triplewise: Adjacent element iteration
- interleave/roundrobin: Mix multiple iterables
- peek/peekable: Look ahead without consuming
- is_empty: Check if iterable is empty
- first/last/nth: Get specific elements
- cycle: Infinite cycling
- batched: Python 3.12+ style batching

Author: AllToolkit
License: MIT
"""

from typing import (
    TypeVar, Iterable, Iterator, List, Tuple, Optional, Callable,
    Generator, Any, Union, Sequence, overload
)
from collections import deque
from itertools import islice, count as itertools_count

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')


def chunk(iterable: Iterable[T], size: int) -> Generator[Tuple[T, ...], None, None]:
    """
    Split an iterable into fixed-size chunks (tuples).
    
    Args:
        iterable: The iterable to chunk
        size: Size of each chunk (must be >= 1)
    
    Yields:
        Tuples of elements, each of length 'size' except possibly the last
    
    Raises:
        ValueError: If size < 1
    
    Examples:
        >>> list(chunk([1, 2, 3, 4, 5], 2))
        [(1, 2), (3, 4), (5,)]
        >>> list(chunk('abcdef', 3))
        [('a', 'b', 'c'), ('d', 'e', 'f')]
    """
    if size < 1:
        raise ValueError(f"Chunk size must be >= 1, got {size}")
    
    it = iter(iterable)
    while True:
        batch = tuple(islice(it, size))
        if not batch:
            break
        yield batch


def batched(iterable: Iterable[T], n: int) -> Generator[Tuple[T, ...], None, None]:
    """
    Batch data from the iterable into tuples of length n.
    Python 3.12+ itertools.batched backport.
    
    Args:
        iterable: The iterable to batch
        n: Batch size (must be >= 1)
    
    Yields:
        Tuples of n elements, last batch may be smaller
    
    Raises:
        ValueError: If n < 1
    
    Examples:
        >>> list(batched('ABCDEFG', 3))
        [('A', 'B', 'C'), ('D', 'E', 'F'), ('G',)]
    """
    return chunk(iterable, n)


def sliding_window(iterable: Iterable[T], size: int, step: int = 1) -> Generator[Tuple[T, ...], None, None]:
    """
    Generate sliding windows over an iterable.
    
    Args:
        iterable: The iterable to slide over
        size: Size of each window (must be >= 1)
        step: Step between windows (must be >= 1, default 1)
    
    Yields:
        Tuples of 'size' consecutive elements
    
    Raises:
        ValueError: If size < 1 or step < 1
    
    Examples:
        >>> list(sliding_window([1, 2, 3, 4, 5], 3))
        [(1, 2, 3), (2, 3, 4), (3, 4, 5)]
        >>> list(sliding_window([1, 2, 3, 4, 5], 2, step=2))
        [(1, 2), (3, 4)]
    """
    if size < 1:
        raise ValueError(f"Window size must be >= 1, got {size}")
    if step < 1:
        raise ValueError(f"Step must be >= 1, got {step}")
    
    it = iter(iterable)
    window = deque(maxlen=size)
    
    # Fill the first window
    for _ in range(size):
        try:
            window.append(next(it))
        except StopIteration:
            if window:
                yield tuple(window)
            return
    
    yield tuple(window)
    
    # Continue sliding
    while True:
        # Skip step-1 elements if step > 1
        if step > 1:
            for _ in range(step - 1):
                try:
                    window.append(next(it))
                except StopIteration:
                    return
        
        try:
            window.append(next(it))
            yield tuple(window)
        except StopIteration:
            return


def flatten(iterable: Iterable[Any], depth: int = 1) -> Generator[Any, None, None]:
    """
    Flatten nested iterables to specified depth.
    
    Args:
        iterable: The nested iterable to flatten
        depth: How many levels to flatten (default 1, -1 for unlimited)
    
    Yields:
        Flattened elements
    
    Examples:
        >>> list(flatten([[1, 2], [3, 4]]))
        [1, 2, 3, 4]
        >>> list(flatten([[[1, 2]], [[3, 4]]], depth=2))
        [1, 2, 3, 4]
        >>> list(flatten([[[[1]]]], depth=-1))
        [1]
    """
    if depth == 0:
        yield from iterable
        return
    
    for item in iterable:
        # Check if item is iterable but not string/bytes
        if isinstance(item, (str, bytes)):
            yield item
        elif hasattr(item, '__iter__'):
            if depth == -1:
                yield from flatten(item, -1)
            else:
                yield from flatten(item, depth - 1)
        else:
            yield item


def deep_flatten(iterable: Iterable[Any]) -> Generator[Any, None, None]:
    """
    Fully flatten all nested iterables (unlimited depth).
    
    Args:
        iterable: The nested iterable to flatten
    
    Yields:
        Fully flattened elements (strings and bytes are preserved as atoms)
    
    Examples:
        >>> list(deep_flatten([1, [2, [3, [4, [5]]]]]))
        [1, 2, 3, 4, 5]
    """
    yield from flatten(iterable, depth=-1)


def take(n: int, iterable: Iterable[T]) -> List[T]:
    """
    Take the first n elements from an iterable.
    
    Args:
        n: Number of elements to take (can be negative for all elements)
        iterable: The iterable to take from
    
    Returns:
        List of up to n elements
    
    Examples:
        >>> take(3, range(10))
        [0, 1, 2]
        >>> take(5, [1, 2])
        [1, 2]
    """
    if n < 0:
        return list(iterable)
    return list(islice(iterable, n))


def take_while(predicate: Callable[[T], bool], iterable: Iterable[T]) -> Generator[T, None, None]:
    """
    Take elements while predicate is true.
    
    Args:
        predicate: Function that returns True to continue taking
        iterable: The iterable to take from
    
    Yields:
        Elements until predicate returns False
    
    Examples:
        >>> list(take_while(lambda x: x < 5, [1, 2, 3, 4, 5, 6]))
        [1, 2, 3, 4]
    """
    for item in iterable:
        if not predicate(item):
            break
        yield item


def drop(n: int, iterable: Iterable[T]) -> Generator[T, None, None]:
    """
    Drop the first n elements from an iterable.
    
    Args:
        n: Number of elements to drop
        iterable: The iterable to drop from
    
    Yields:
        Elements after the first n
    
    Examples:
        >>> list(drop(3, range(6)))
        [3, 4, 5]
    """
    it = iter(iterable)
    for _ in range(n):
        try:
            next(it)
        except StopIteration:
            return
    yield from it


def drop_while(predicate: Callable[[T], bool], iterable: Iterable[T]) -> Generator[T, None, None]:
    """
    Drop elements while predicate is true.
    
    Args:
        predicate: Function that returns True to continue dropping
        iterable: The iterable to drop from
    
    Yields:
        Elements starting from when predicate returns False
    
    Examples:
        >>> list(drop_while(lambda x: x < 3, [1, 2, 3, 4, 5]))
        [3, 4, 5]
    """
    dropping = True
    for item in iterable:
        if dropping and predicate(item):
            continue
        dropping = False
        yield item


def unique(iterable: Iterable[T], key: Optional[Callable[[T], Any]] = None) -> Generator[T, None, None]:
    """
    Yield unique elements, preserving order of first occurrence.
    
    Args:
        iterable: The iterable to filter
        key: Optional function to compute comparison key
    
    Yields:
        Unique elements in order of first occurrence
    
    Examples:
        >>> list(unique([1, 2, 1, 3, 2, 4]))
        [1, 2, 3, 4]
        >>> list(unique(['a', 'A', 'b', 'B'], key=str.lower))
        ['a', 'b']
    """
    seen = set()
    seen_add = seen.add
    
    if key is None:
        for item in iterable:
            if item not in seen:
                seen_add(item)
                yield item
    else:
        for item in iterable:
            k = key(item)
            if k not in seen:
                seen_add(k)
                yield item


def dedupe(iterable: Iterable[T]) -> Generator[T, None, None]:
    """
    Remove consecutive duplicates (like Unix uniq command).
    
    Args:
        iterable: The iterable to filter
    
    Yields:
        Elements with consecutive duplicates removed
    
    Examples:
        >>> list(dedupe([1, 1, 2, 2, 2, 3, 2, 2, 4]))
        [1, 2, 3, 2, 4]
    """
    it = iter(iterable)
    try:
        prev = next(it)
        yield prev
        for item in it:
            if item != prev:
                yield item
                prev = item
    except StopIteration:
        pass


def partition(predicate: Callable[[T], bool], iterable: Iterable[T]) -> Tuple[List[T], List[T]]:
    """
    Split iterable into two lists based on predicate.
    
    Args:
        predicate: Function that returns True/False
        iterable: The iterable to partition
    
    Returns:
        Tuple of (truthy_list, falsy_list)
    
    Examples:
        >>> partition(lambda x: x % 2 == 0, [1, 2, 3, 4, 5])
        ([2, 4], [1, 3, 5])
    """
    truthy = []
    falsy = []
    for item in iterable:
        if predicate(item):
            truthy.append(item)
        else:
            falsy.append(item)
    return truthy, falsy


def groupby_consecutive(iterable: Iterable[T], key: Optional[Callable[[T], K]] = None) -> Generator[Tuple[K, List[T]], None, None]:
    """
    Group consecutive elements with the same key.
    Unlike itertools.groupby, this returns lists instead of iterators.
    
    Args:
        iterable: The iterable to group
        key: Optional function to compute group key (default: identity)
    
    Yields:
        Tuples of (key, list_of_elements)
    
    Examples:
        >>> list(groupby_consecutive([1, 1, 2, 2, 2, 1, 3, 3]))
        [(1, [1, 1]), (2, [2, 2, 2]), (1, [1]), (3, [3, 3])]
    """
    it = iter(iterable)
    try:
        first = next(it)
    except StopIteration:
        return
    
    if key is None:
        key = lambda x: x
    
    current_key = key(first)
    current_group = [first]
    
    for item in it:
        k = key(item)
        if k == current_key:
            current_group.append(item)
        else:
            yield (current_key, current_group)
            current_key = k
            current_group = [item]
    
    yield (current_key, current_group)


def pairwise(iterable: Iterable[T]) -> Generator[Tuple[T, T], None, None]:
    """
    Generate pairs of consecutive elements.
    itertoolz.recipe backport of Python 3.10+ itertools.pairwise.
    
    Args:
        iterable: The iterable to pair
    
    Yields:
        Tuples of (prev, curr) for consecutive pairs
    
    Examples:
        >>> list(pairwise([1, 2, 3, 4]))
        [(1, 2), (2, 3), (3, 4)]
    """
    it = iter(iterable)
    try:
        prev = next(it)
    except StopIteration:
        return
    
    for curr in it:
        yield (prev, curr)
        prev = curr


def triplewise(iterable: Iterable[T]) -> Generator[Tuple[T, T, T], None, None]:
    """
    Generate triples of consecutive elements.
    
    Args:
        iterable: The iterable to triple
    
    Yields:
        Tuples of three consecutive elements
    
    Examples:
        >>> list(triplewise([1, 2, 3, 4, 5]))
        [(1, 2, 3), (2, 3, 4), (3, 4, 5)]
    """
    it = iter(iterable)
    try:
        a = next(it)
        b = next(it)
        c = next(it)
        yield (a, b, c)
        
        while True:
            a, b, c = b, c, next(it)
            yield (a, b, c)
    except StopIteration:
        pass


def interleave(*iterables: Iterable[T]) -> Generator[T, None, None]:
    """
    Interleave elements from multiple iterables.
    Stops when the shortest iterable is exhausted.
    
    Args:
        *iterables: Multiple iterables to interleave
    
    Yields:
        Interleaved elements
    
    Examples:
        >>> list(interleave([1, 2, 3], ['a', 'b', 'c']))
        [1, 'a', 2, 'b', 3, 'c']
    """
    iterators = [iter(it) for it in iterables]
    while iterators:
        for it in iterators:
            try:
                yield next(it)
            except StopIteration:
                # Stop immediately when any iterator is exhausted
                return


def roundrobin(*iterables: Iterable[T]) -> Generator[T, None, None]:
    """
    Round-robin iteration over multiple iterables.
    Continues until all iterables are exhausted.
    
    Args:
        *iterables: Multiple iterables to cycle through
    
    Yields:
        Elements in round-robin order
    
    Examples:
        >>> list(roundrobin('ABC', 'D', 'EF'))
        ['A', 'D', 'E', 'B', 'F', 'C']
    """
    iterators = deque(iter(it) for it in iterables)
    while iterators:
        it = iterators.popleft()
        try:
            yield next(it)
            iterators.append(it)
        except StopIteration:
            pass


# Sentinel object for default parameter detection (must be defined before Peekable)
_sentinel = object()


class Peekable:
    """
    A wrapper around an iterator that allows peeking at the next element.
    
    Examples:
        >>> p = Peekable(range(3))
        >>> p.peek()
        0
        >>> next(p)
        0
        >>> list(p)
        [1, 2]
    """
    
    def __init__(self, iterable: Iterable[T]):
        self._it = iter(iterable)
        self._cache: deque = deque()
        self._exhausted = False
    
    def __iter__(self) -> 'Peekable':
        return self
    
    def __next__(self) -> T:
        if self._cache:
            return self._cache.popleft()
        return next(self._it)
    
    def peek(self, default: Any = _sentinel) -> Any:
        """
        Peek at the next element without consuming it.
        
        Args:
            default: Value to return if exhausted (raises StopIteration if not provided)
        
        Returns:
            The next element without advancing the iterator
        
        Raises:
            StopIteration: If exhausted and no default provided
        """
        if not self._cache:
            try:
                self._cache.append(next(self._it))
            except StopIteration:
                self._exhausted = True
                if default is not _sentinel:
                    return default
                raise
        return self._cache[0]
    
    def is_empty(self) -> bool:
        """Check if the iterator is exhausted."""
        if self._cache:
            return False
        try:
            self._cache.append(next(self._it))
            return False
        except StopIteration:
            return True
    
    def take(self, n: int) -> List[T]:
        """Take n elements from the peekable."""
        return take(n, self)
    
    def drop(self, n: int) -> None:
        """Drop n elements from the peekable."""
        for _ in range(n):
            try:
                next(self)
            except StopIteration:
                break


def peek(iterable: Iterable[T]) -> Tuple[Optional[T], Iterator[T]]:
    """
    Peek at the first element of an iterable without consuming it.
    
    Args:
        iterable: The iterable to peek into
    
    Returns:
        Tuple of (first_element_or_None, original_iterator)
    
    Examples:
        >>> first, it = peek([1, 2, 3])
        >>> first
        1
        >>> list(it)
        [1, 2, 3]
    """
    it = iter(iterable)
    try:
        first = next(it)
        return first, _chain([first], it)
    except StopIteration:
        return None, it


def _chain(first: Iterable[T], rest: Iterable[T]) -> Iterator[T]:
    """Helper to chain first element back with rest of iterator."""
    yield from first
    yield from rest


def is_empty(iterable: Iterable[T]) -> Tuple[bool, Iterator[T]]:
    """
    Check if an iterable is empty without losing elements.
    
    Args:
        iterable: The iterable to check
    
    Returns:
        Tuple of (is_empty_bool, original_iterator)
    
    Examples:
        >>> empty, it = is_empty([])
        >>> empty
        True
        >>> empty, it = is_empty([1, 2])
        >>> empty
        False
        >>> list(it)
        [1, 2]
    """
    it = iter(iterable)
    try:
        first = next(it)
        return False, _chain([first], it)
    except StopIteration:
        return True, it


def first(iterable: Iterable[T], default: Any = _sentinel) -> Any:
    """
    Get the first element of an iterable.
    
    Args:
        iterable: The iterable to get from
        default: Value to return if empty (raises ValueError if not provided)
    
    Returns:
        The first element
    
    Raises:
        ValueError: If iterable is empty and no default provided
    
    Examples:
        >>> first([1, 2, 3])
        1
        >>> first([], default=0)
        0
    """
    it = iter(iterable)
    try:
        return next(it)
    except StopIteration:
        if default is not _sentinel:
            return default
        raise ValueError("first() called on empty iterable")


def last(iterable: Iterable[T], default: Any = _sentinel) -> Any:
    """
    Get the last element of an iterable.
    
    Args:
        iterable: The iterable to get from
        default: Value to return if empty (raises ValueError if not provided)
    
    Returns:
        The last element
    
    Raises:
        ValueError: If iterable is empty and no default provided
    
    Examples:
        >>> last([1, 2, 3])
        3
        >>> last([], default=0)
        0
    """
    result = default
    found = False
    for item in iterable:
        result = item
        found = True
    
    if not found:
        if default is not _sentinel:
            return default
        raise ValueError("last() called on empty iterable")
    
    return result


def nth(n: int, iterable: Iterable[T], default: Any = _sentinel) -> Any:
    """
    Get the nth element (0-indexed) of an iterable.
    
    Args:
        n: Index of element to get (0-indexed)
        iterable: The iterable to get from
        default: Value to return if not found (raises IndexError if not provided)
    
    Returns:
        The nth element
    
    Raises:
        IndexError: If n >= len(iterable) and no default provided
    
    Examples:
        >>> nth(2, [10, 20, 30, 40])
        30
        >>> nth(10, [1, 2, 3], default=0)
        0
    """
    if n < 0:
        # Try to get from the end if possible
        items = list(iterable)
        try:
            return items[n]
        except IndexError:
            if default is not _sentinel:
                return default
            raise IndexError(f"Index {n} out of range for iterable of length {len(items)}")
    
    it = iter(iterable)
    try:
        for _ in range(n + 1):
            result = next(it)
        return result
    except StopIteration:
        if default is not _sentinel:
            return default
        raise IndexError(f"Index {n} out of range")


def cycle(iterable: Iterable[T]) -> Generator[T, None, None]:
    """
    Infinite cycle through an iterable.
    
    Args:
        iterable: The iterable to cycle through
    
    Yields:
        Elements repeatedly
    
    Examples:
        >>> from itertools import islice
        >>> list(islice(cycle([1, 2, 3]), 7))
        [1, 2, 3, 1, 2, 3, 1]
    """
    saved = []
    for item in iterable:
        saved.append(item)
        yield item
    
    if not saved:
        return
    
    while True:
        for item in saved:
            yield item


def repeat(item: T, times: Optional[int] = None) -> Generator[T, None, None]:
    """
    Repeat an item a specified number of times (or infinitely).
    
    Args:
        item: The item to repeat
        times: Number of times to repeat (None for infinite)
    
    Yields:
        The item repeatedly
    
    Examples:
        >>> list(repeat('x', 3))
        ['x', 'x', 'x']
    """
    if times is None:
        while True:
            yield item
    else:
        for _ in range(times):
            yield item


def count(start: int = 0, step: int = 1) -> Generator[int, None, None]:
    """
    Generate an infinite sequence of numbers.
    
    Args:
        start: Starting value (default 0)
        step: Step increment (default 1)
    
    Yields:
        Infinite sequence of numbers
    
    Examples:
        >>> from itertools import islice
        >>> list(islice(count(10, 2), 5))
        [10, 12, 14, 16, 18]
    """
    yield from itertools_count(start, step)


def zip_with(func: Callable, *iterables: Iterable) -> Generator[Any, None, None]:
    """
    Zip iterables and apply a function to each tuple.
    
    Args:
        func: Function to apply to each zipped tuple
        *iterables: Iterables to zip
    
    Yields:
        Results of applying func to each zipped tuple
    
    Examples:
        >>> list(zip_with(lambda x, y: x + y, [1, 2, 3], [10, 20, 30]))
        [11, 22, 33]
    """
    for items in zip(*iterables):
        yield func(*items)


def enumerate_with(iterable: Iterable[T], start: int = 0, step: int = 1) -> Generator[Tuple[int, T], None, None]:
    """
    Enumerate with custom start and step.
    
    Args:
        iterable: The iterable to enumerate
        start: Starting index (default 0)
        step: Step between indices (default 1)
    
    Yields:
        Tuples of (index, element)
    
    Examples:
        >>> list(enumerate_with(['a', 'b', 'c'], start=1, step=2))
        [(1, 'a'), (3, 'b'), (5, 'c')]
    """
    index = start
    for item in iterable:
        yield (index, item)
        index += step


def unzip(iterable: Iterable[Tuple]) -> Tuple[Tuple, ...]:
    """
    Unzip an iterable of tuples into separate tuples.
    The reverse of zip().
    
    Args:
        iterable: Iterable of tuples to unzip
    
    Returns:
        Tuple of tuples with elements separated
    
    Examples:
        >>> unzip([(1, 'a'), (2, 'b'), (3, 'c')])
        ((1, 2, 3), ('a', 'b', 'c'))
    """
    # Collect all items first
    items = list(iterable)
    if not items:
        return ()
    
    # Transpose
    return tuple(zip(*items))


def unzip_list(iterable: Iterable[Tuple]) -> Tuple[List, ...]:
    """
    Unzip an iterable of tuples into separate lists.
    
    Args:
        iterable: Iterable of tuples to unzip
    
    Returns:
        Tuple of lists with elements separated
    
    Examples:
        >>> unzip_list([(1, 'a'), (2, 'b'), (3, 'c')])
        ([1, 2, 3], ['a', 'b', 'c'])
    """
    items = list(iterable)
    if not items:
        return ([],)
    
    result = tuple([] for _ in range(len(items[0])))
    for tup in items:
        for i, val in enumerate(tup):
            result[i].append(val)
    return result


def split_at(predicate: Callable[[T], bool], iterable: Iterable[T]) -> Tuple[List[T], List[T]]:
    """
    Split an iterable at the first element where predicate is true.
    
    Args:
        predicate: Function that returns True to split at
        iterable: The iterable to split
    
    Returns:
        Tuple of (before_split, after_and_including_split)
    
    Examples:
        >>> split_at(lambda x: x == 3, [1, 2, 3, 4, 5])
        ([1, 2], [3, 4, 5])
    """
    before = []
    after = []
    found = False
    
    for item in iterable:
        if found:
            after.append(item)
        elif predicate(item):
            after.append(item)
            found = True
        else:
            before.append(item)
    
    return before, after


def split_after(predicate: Callable[[T], bool], iterable: Iterable[T]) -> Tuple[List[T], List[T]]:
    """
    Split an iterable after the first element where predicate is true.
    
    Args:
        predicate: Function that returns True to split after
        iterable: The iterable to split
    
    Returns:
        Tuple of (before_and_including_match, after_match)
    
    Examples:
        >>> split_after(lambda x: x == 3, [1, 2, 3, 4, 5])
        ([1, 2, 3], [4, 5])
    """
    before = []
    after = []
    found = False
    
    for item in iterable:
        if found:
            after.append(item)
        else:
            before.append(item)
            if predicate(item):
                found = True
    
    return before, after


def stagger(iterable: Iterable[T], offsets: Sequence[int] = (-1, 0, 1)) -> Generator[Tuple, None, None]:
    """
    Generate tuples with elements at given offsets.
    
    Args:
        iterable: The iterable to stagger
        offsets: Sequence of offsets for each position (default (-1, 0, 1))
    
    Yields:
        Tuples with elements at specified offsets
    
    Examples:
        >>> list(stagger([1, 2, 3, 4, 5]))
        [(None, 1, 2), (1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, None)]
    """
    it = iter(iterable)
    min_offset = min(offsets)
    max_offset = max(offsets)
    size = max_offset - min_offset + 1
    
    # Initialize the window
    window = deque(maxlen=size)
    
    # Fill with None for negative offsets
    for _ in range(-min_offset):
        window.append(None)
    
    # Fill the rest from iterator
    for _ in range(size + min_offset):
        try:
            window.append(next(it))
        except StopIteration:
            break
    
    # Yield tuples
    while True:
        yield tuple(window[i + min_offset] if i + min_offset < len(window) else None 
                   for i in offsets)
        try:
            window.append(next(it))
        except StopIteration:
            # Shift window
            for i in range(-min_offset):
                window.append(None)
            break


def minmax(iterable: Iterable[T], key: Optional[Callable[[T], Any]] = None) -> Tuple[T, T]:
    """
    Get both minimum and maximum in a single pass.
    
    Args:
        iterable: The iterable to process
        key: Optional function for comparison
    
    Returns:
        Tuple of (minimum, maximum)
    
    Raises:
        ValueError: If iterable is empty
    
    Examples:
        >>> minmax([3, 1, 4, 1, 5, 9, 2, 6])
        (1, 9)
    """
    it = iter(iterable)
    try:
        first = next(it)
    except StopIteration:
        raise ValueError("minmax() called on empty iterable")
    
    current_min = current_max = first
    key_func = key if key else lambda x: x
    current_min_key = current_max_key = key_func(first)
    
    for item in it:
        k = key_func(item)
        if k < current_min_key:
            current_min = item
            current_min_key = k
        if k > current_max_key:
            current_max = item
            current_max_key = k
    
    return current_min, current_max


# Convenience function aliases
chunks = chunk
windows = sliding_window
flatten_one = lambda it: flatten(it, depth=1)


if __name__ == "__main__":
    # Simple demo
    print("iter_utils demo:")
    print(f"chunk([1,2,3,4,5], 2) = {list(chunk([1,2,3,4,5], 2))}")
    print(f"sliding_window([1,2,3,4,5], 3) = {list(sliding_window([1,2,3,4,5], 3))}")
    print(f"flatten([[1,2],[3,4]]) = {list(flatten([[1,2],[3,4]]))}")
    print(f"unique([1,2,1,3,2]) = {list(unique([1,2,1,3,2]))}")
    print(f"pairwise([1,2,3,4]) = {list(pairwise([1,2,3,4]))}")
    print(f"partition(lambda x: x%2, [1,2,3,4,5]) = {partition(lambda x: x%2, [1,2,3,4,5])}")