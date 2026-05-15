"""
Top-N Utils - Efficient Top-N Selection Utilities

Provides efficient algorithms for finding top-N items without full sorting.
Useful for leaderboards, recommendations, hotspot analysis, etc.

Features:
- Multiple selection algorithms (heap-based, quickselect, threshold)
- Streaming top-N for large datasets
- Time-windowed top-N (sliding window)
- Category-based top-N
- Weighted top-N
- Zero external dependencies

Author: AllToolkit
Date: 2026-05-16
"""

import heapq
import random
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    Iterator,
    List,
    Optional,
    Tuple,
    TypeVar,
    Union,
)
from dataclasses import dataclass, field
from collections import defaultdict
from abc import ABC, abstractmethod
from time import time

T = TypeVar('T')
K = TypeVar('K')


@dataclass
class TopNResult(Generic[T]):
    """Result container for top-N operations."""
    items: List[Tuple[T, float]]  # (item, score) pairs in descending order
    algorithm: str
    comparisons: int = 0
    time_ms: float = 0.0


class TopNSelector(Generic[T]):
    """
    Efficient top-N selector using various algorithms.
    
    Examples:
        >>> selector = TopNSelector(lambda x: x)
        >>> selector.add_items([5, 2, 8, 1, 9, 3])
        >>> selector.get_top_n(3)
        [(9, 9), (8, 8), (5, 5)]
    """
    
    def __init__(
        self,
        key_func: Callable[[T], float],
        max_size: Optional[int] = None
    ):
        """
        Initialize the selector.
        
        Args:
            key_func: Function to extract score from item
            max_size: Maximum items to store (None for unlimited)
        """
        self.key_func = key_func
        self.max_size = max_size
        self._items: List[Tuple[float, T]] = []  # (score, item) pairs
        self._comparisons = 0
    
    def add_item(self, item: T) -> bool:
        """
        Add a single item.
        
        Returns:
            True if item was added, False if rejected (not in top-N)
        """
        score = self.key_func(item)
        self._comparisons += 1
        
        if self.max_size is None or len(self._items) < self.max_size:
            heapq.heappush(self._items, (score, item))
            return True
        
        # Only add if score is better than the minimum
        if score > self._items[0][0]:
            heapq.heapreplace(self._items, (score, item))
            self._comparisons += 1
            return True
        
        return False
    
    def add_items(self, items: Iterable[T]) -> int:
        """
        Add multiple items.
        
        Returns:
            Number of items actually added
        """
        added = 0
        for item in items:
            if self.add_item(item):
                added += 1
        return added
    
    def get_top_n(self, n: Optional[int] = None) -> List[Tuple[T, float]]:
        """
        Get top-N items in descending order by score.
        
        Args:
            n: Number of items to return (None for all stored items)
        
        Returns:
            List of (item, score) tuples in descending order
        """
        if n is None:
            n = len(self._items)
        
        # Sort in descending order
        sorted_items = sorted(self._items, key=lambda x: x[0], reverse=True)
        return [(item, score) for score, item in sorted_items[:n]]
    
    def clear(self) -> None:
        """Clear all stored items."""
        self._items.clear()
        self._comparisons = 0
    
    @property
    def size(self) -> int:
        """Current number of stored items."""
        return len(self._items)
    
    @property
    def comparisons(self) -> int:
        """Number of comparisons made."""
        return self._comparisons


def heap_top_n(
    items: Iterable[T],
    n: int,
    key: Callable[[T], float] = lambda x: x,
    keep_ties: bool = False
) -> List[Tuple[T, float]]:
    """
    Find top-N items using min-heap algorithm.
    
    Time complexity: O(N log k) where k is n
    Space complexity: O(k)
    
    Args:
        items: Iterable of items
        n: Number of top items to find
        key: Function to extract score from item
        keep_ties: If True, keep all items with the same score as the nth item
    
    Returns:
        List of (item, score) tuples in descending order
    
    Examples:
        >>> heap_top_n([3, 1, 4, 1, 5, 9, 2, 6], 3)
        [(9, 9), (6, 6), (5, 5)]
    """
    if n <= 0:
        return []
    
    heap: List[Tuple[float, int, T]] = []  # (score, tiebreaker, item)
    tiebreaker = 0
    
    for item in items:
        score = key(item)
        
        if len(heap) < n:
            heapq.heappush(heap, (score, tiebreaker, item))
        elif score > heap[0][0]:
            heapq.heapreplace(heap, (score, tiebreaker, item))
        elif keep_ties and score == heap[0][0]:
            heapq.heappush(heap, (score, tiebreaker, item))
        
        tiebreaker += 1
    
    # Sort in descending order
    result = sorted(heap, key=lambda x: x[0], reverse=True)
    return [(item, score) for score, _, item in result]


def quickselect_top_n(
    items: List[T],
    n: int,
    key: Callable[[T], float] = lambda x: x
) -> List[Tuple[T, float]]:
    """
    Find top-N items using QuickSelect algorithm.
    
    Time complexity: O(N) average case
    Space complexity: O(N)
    
    Better for small n and when you have the full list.
    
    Args:
        items: List of items (will be modified)
        n: Number of top items to find
        key: Function to extract score from item
    
    Returns:
        List of (item, score) tuples in descending order
    
    Examples:
        >>> quickselect_top_n([3, 1, 4, 1, 5, 9, 2, 6], 3)
        [(9, 9), (6, 6), (5, 5)]
    """
    if n <= 0:
        return []
    
    if len(items) <= n:
        scored = [(item, key(item)) for item in items]
        return sorted(scored, key=lambda x: x[1], reverse=True)
    
    # Work with indices and scores
    scored_items = [(key(item), item) for item in items]
    
    def partition(arr: List[Tuple[float, T]], left: int, right: int, pivot_idx: int) -> int:
        """Partition around pivot, return final pivot position."""
        pivot_val = arr[pivot_idx][0]
        arr[pivot_idx], arr[right] = arr[right], arr[pivot_idx]
        store_idx = left
        
        for i in range(left, right):
            if arr[i][0] > pivot_val:  # We want descending order
                arr[store_idx], arr[i] = arr[i], arr[store_idx]
                store_idx += 1
        
        arr[right], arr[store_idx] = arr[store_idx], arr[right]
        return store_idx
    
    left, right = 0, len(scored_items) - 1
    
    while left <= right:
        # Random pivot selection
        pivot_idx = random.randint(left, right)
        pivot_idx = partition(scored_items, left, right, pivot_idx)
        
        if pivot_idx == n - 1:
            break
        elif pivot_idx < n - 1:
            left = pivot_idx + 1
        else:
            right = pivot_idx - 1
    
    # Get top n and sort
    top_n = scored_items[:n]
    top_n.sort(key=lambda x: x[0], reverse=True)
    return [(item, score) for score, item in top_n]


def streaming_top_n(
    items: Iterable[T],
    n: int,
    key: Callable[[T], float] = lambda x: x,
    checkpoint_func: Optional[Callable[[List[Tuple[T, float]]], None]] = None,
    checkpoint_interval: int = 10000
) -> List[Tuple[T, float]]:
    """
    Streaming top-N for large datasets with optional checkpointing.
    
    Memory-efficient: only keeps top-N items in memory.
    
    Args:
        items: Iterable of items
        n: Number of top items to find
        key: Function to extract score from item
        checkpoint_func: Optional function to save checkpoints
        checkpoint_interval: How often to checkpoint (in items processed)
    
    Returns:
        List of (item, score) tuples in descending order
    
    Examples:
        >>> # Process a large file
        >>> def save_checkpoint(top_items):
        ...     print(f"Checkpoint: {len(top_items)} items")
        >>> result = streaming_top_n(range(100000), 5, checkpoint_func=save_checkpoint)
    """
    if n <= 0:
        return []
    
    heap: List[Tuple[float, int, T]] = []
    tiebreaker = 0
    processed = 0
    
    for item in items:
        score = key(item)
        
        if len(heap) < n:
            heapq.heappush(heap, (score, tiebreaker, item))
        elif score > heap[0][0]:
            heapq.heapreplace(heap, (score, tiebreaker, item))
        
        tiebreaker += 1
        processed += 1
        
        # Checkpoint
        if checkpoint_func and processed % checkpoint_interval == 0:
            current_top = [(item, score) for score, _, item in 
                          sorted(heap, key=lambda x: x[0], reverse=True)]
            checkpoint_func(current_top)
    
    # Sort in descending order
    result = sorted(heap, key=lambda x: x[0], reverse=True)
    return [(item, score) for score, _, item in result]


class TimeWindowTopN(Generic[T]):
    """
    Top-N items within a sliding time window.
    
    Useful for real-time analytics, trending items, etc.
    
    Examples:
        >>> window = TimeWindowTopN(window_seconds=60, n=10)
        >>> window.add("item1", score=5.0)
        >>> window.add("item2", score=3.0)
        >>> top_items = window.get_top_n(2)
    """
    
    def __init__(
        self,
        window_seconds: float,
        n: int,
        key_func: Optional[Callable[[T], float]] = None
    ):
        """
        Initialize time-windowed top-N tracker.
        
        Args:
            window_seconds: Time window in seconds
            n: Maximum number of items to track
            key_func: Optional function to transform items before scoring
        """
        self.window_seconds = window_seconds
        self.n = n
        self.key_func = key_func or (lambda x: x)
        self._items: List[Tuple[float, float, T]] = []  # (score, timestamp, item)
    
    def add(self, item: T, score: float, timestamp: Optional[float] = None) -> None:
        """
        Add an item with a score.
        
        Args:
            item: The item to add
            score: The score for this item
            timestamp: Optional timestamp (defaults to current time)
        """
        if timestamp is None:
            timestamp = time()
        
        # Add item
        self._items.append((score, timestamp, item))
        
        # Prune old items
        self._prune(timestamp)
        
        # Keep only top N
        if len(self._items) > self.n * 2:  # Threshold to avoid frequent sorting
            self._items.sort(key=lambda x: x[0], reverse=True)
            self._items = self._items[:self.n]
    
    def _prune(self, current_time: float) -> None:
        """Remove items outside the time window."""
        cutoff = current_time - self.window_seconds
        self._items = [(s, t, i) for s, t, i in self._items if t > cutoff]
    
    def get_top_n(self, n: Optional[int] = None) -> List[Tuple[T, float]]:
        """
        Get current top-N items.
        
        Args:
            n: Number of items to return (None for all tracked items)
        
        Returns:
            List of (item, score) tuples in descending order
        """
        if n is None:
            n = len(self._items)
        
        # Prune and sort
        self._prune(time())
        sorted_items = sorted(self._items, key=lambda x: x[0], reverse=True)
        return [(item, score) for score, _, item in sorted_items[:n]]
    
    def clear(self) -> None:
        """Clear all items."""
        self._items.clear()


class CategoryTopN(Generic[T, K]):
    """
    Top-N items per category.
    
    Examples:
        >>> top_by_category = CategoryTopN(n=3)
        >>> top_by_category.add("fruit", "apple", 5.0)
        >>> top_by_category.add("fruit", "banana", 3.0)
        >>> top_by_category.add("vegetable", "carrot", 4.0)
        >>> top_by_category.get_top_n("fruit", 2)
        [('apple', 5.0), ('banana', 3.0)]
    """
    
    def __init__(
        self,
        n: int = 10,
        key_func: Optional[Callable[[T], float]] = None
    ):
        """
        Initialize category-based top-N tracker.
        
        Args:
            n: Maximum items per category
            key_func: Optional function to extract score from item
        """
        self.n = n
        self.key_func = key_func
        self._use_explicit_score = key_func is None
        self._categories: Dict[K, TopNSelector] = {}
    
    def _get_selector(self, category: K) -> TopNSelector:
        """Get or create selector for a category."""
        if category not in self._categories:
            if self._use_explicit_score:
                # Store (item, score) tuples, key by score
                self._categories[category] = TopNSelector(
                    lambda x: x[1], max_size=self.n
                )
            else:
                self._categories[category] = TopNSelector(
                    self.key_func, max_size=self.n
                )
        return self._categories[category]
    
    def add(self, category: K, item: T, score: Optional[float] = None) -> bool:
        """
        Add an item to a category.
        
        Args:
            category: The category key
            item: The item to add
            score: The score (used if key_func is None)
        
        Returns:
            True if item was added to top-N
        """
        selector = self._get_selector(category)
        if self._use_explicit_score:
            if score is None:
                score = 0.0
            return selector.add_item((item, score))
        else:
            return selector.add_item(item)
    
    def get_top_n(self, category: K, n: Optional[int] = None) -> List[Tuple[T, float]]:
        """
        Get top-N items for a category.
        
        Args:
            category: The category key
            n: Number of items (None for all)
        
        Returns:
            List of (item, score) tuples
        """
        if category not in self._categories:
            return []
        
        raw_result = self._categories[category].get_top_n(n)
        
        # Unwrap if we stored tuples
        if self._use_explicit_score:
            return [(pair[0], pair[1]) for pair, _ in raw_result]
        else:
            return raw_result
    
    def get_all_categories(self) -> List[K]:
        """Get all category keys."""
        return list(self._categories.keys())
    
    def get_top_n_all(self, n: Optional[int] = None) -> Dict[K, List[Tuple[T, float]]]:
        """
        Get top-N for all categories.
        
        Returns:
            Dictionary mapping categories to their top-N items
        """
        return {cat: self.get_top_n(cat, n) for cat in self._categories}
    
    def clear(self, category: Optional[K] = None) -> None:
        """Clear a specific category or all categories."""
        if category is not None:
            if category in self._categories:
                self._categories[category].clear()
        else:
            self._categories.clear()


class WeightedTopN(Generic[T]):
    """
    Top-N items with weighted scoring.
    
    Combines multiple scores with weights to produce final ranking.
    
    Examples:
        >>> weighted = WeightedTopN()
        >>> weighted.add_weight("popularity", 0.4)
        >>> weighted.add_weight("recency", 0.3)
        >>> weighted.add_weight("quality", 0.3)
        >>> weighted.add_item("item1", {"popularity": 8, "recency": 9, "quality": 7})
        >>> weighted.get_top_n(1)
        [('item1', 8.0)]
    """
    
    def __init__(self):
        """Initialize weighted top-N tracker."""
        self._weights: Dict[str, float] = {}
        self._items: List[Tuple[T, float, Dict[str, float]]] = []  # (item, final_score, raw_scores)
    
    def add_weight(self, name: str, weight: float) -> None:
        """
        Add a scoring dimension with weight.
        
        Args:
            name: Name of the scoring dimension
            weight: Weight (will be normalized)
        """
        self._weights[name] = weight
    
    def set_weights(self, weights: Dict[str, float]) -> None:
        """Set all weights at once."""
        self._weights = weights.copy()
    
    def _normalize_weights(self) -> Dict[str, float]:
        """Normalize weights to sum to 1."""
        total = sum(self._weights.values())
        if total == 0:
            return {k: 1.0 / len(self._weights) for k in self._weights}
        return {k: v / total for k, v in self._weights.items()}
    
    def add_item(
        self,
        item: T,
        scores: Dict[str, float],
        n: int = 100
    ) -> None:
        """
        Add an item with scores for each dimension.
        
        Args:
            item: The item to add
            scores: Dictionary of dimension -> score
            n: Maximum items to keep
        """
        # Calculate weighted score
        normalized = self._normalize_weights()
        final_score = sum(
            scores.get(name, 0) * weight
            for name, weight in normalized.items()
        )
        
        # Add to items
        self._items.append((item, final_score, scores))
        
        # Keep only top N
        if len(self._items) > n:
            self._items.sort(key=lambda x: x[1], reverse=True)
            self._items = self._items[:n]
    
    def get_top_n(self, n: Optional[int] = None) -> List[Tuple[T, float, Dict[str, float]]]:
        """
        Get top-N items with all scores.
        
        Returns:
            List of (item, final_score, raw_scores) tuples
        """
        sorted_items = sorted(self._items, key=lambda x: x[1], reverse=True)
        if n is not None:
            sorted_items = sorted_items[:n]
        return sorted_items
    
    def clear(self) -> None:
        """Clear all items."""
        self._items.clear()


class IncrementalTopN(Generic[T]):
    """
    Incremental top-N tracker for continuously updating rankings.
    
    Supports incremental updates, score adjustments, and removal.
    
    Examples:
        >>> tracker = IncrementalTopN(n=10)
        >>> tracker.update("player1", score=100)
        >>> tracker.update("player2", score=95)
        >>> tracker.update("player1", score=110)  # Update existing
        >>> tracker.get_top_n(2)
        [('player1', 110), ('player2', 95)]
    """
    
    def __init__(
        self,
        n: int = 10,
        mode: str = "max"  # "max" or "sum"
    ):
        """
        Initialize incremental top-N tracker.
        
        Args:
            n: Maximum number of items to track
            mode: "max" for max score, "sum" for cumulative score
        """
        self.n = n
        self.mode = mode
        self._scores: Dict[T, float] = {}
        self._dirty = True
        self._cached_top: List[Tuple[T, float]] = []
    
    def update(self, item: T, score: float) -> None:
        """
        Update score for an item.
        
        Args:
            item: The item to update
            score: The new score (max mode) or score to add (sum mode)
        """
        if self.mode == "max":
            if item not in self._scores or score > self._scores[item]:
                self._scores[item] = score
                self._dirty = True
        else:  # sum
            self._scores[item] = self._scores.get(item, 0) + score
            self._dirty = True
    
    def remove(self, item: T) -> bool:
        """
        Remove an item.
        
        Returns:
            True if item was removed
        """
        if item in self._scores:
            del self._scores[item]
            self._dirty = True
            return True
        return False
    
    def get_score(self, item: T) -> Optional[float]:
        """Get current score for an item."""
        return self._scores.get(item)
    
    def get_rank(self, item: T) -> Optional[int]:
        """
        Get current rank of an item (1-indexed).
        
        Returns:
            Rank (1 = highest score) or None if not tracked
        """
        self._refresh_cache()
        for i, (it, _) in enumerate(self._cached_top):
            if it == item:
                return i + 1
        return None
    
    def _refresh_cache(self) -> None:
        """Refresh the cached top-N list."""
        if self._dirty:
            sorted_items = sorted(
                self._scores.items(),
                key=lambda x: x[1],
                reverse=True
            )
            self._cached_top = sorted_items[:self.n]
            self._dirty = False
    
    def get_top_n(self, n: Optional[int] = None) -> List[Tuple[T, float]]:
        """
        Get top-N items.
        
        Args:
            n: Number of items (None for all tracked items, max self.n)
        
        Returns:
            List of (item, score) tuples in descending order
        """
        self._refresh_cache()
        if n is None:
            n = len(self._cached_top)
        return self._cached_top[:n]
    
    def get_percentile(self, item: T) -> Optional[float]:
        """
        Get percentile rank of an item (0-100).
        
        Returns:
            Percentile (100 = highest) or None if not tracked
        """
        if item not in self._scores:
            return None
        
        score = self._scores[item]
        scores = sorted(self._scores.values(), reverse=True)
        rank = scores.index(score) + 1
        return (1 - (rank - 1) / max(len(scores) - 1, 1)) * 100
    
    def clear(self) -> None:
        """Clear all items."""
        self._scores.clear()
        self._cached_top.clear()
        self._dirty = True
    
    @property
    def size(self) -> int:
        """Number of tracked items."""
        return len(self._scores)


# Convenience functions

def top_n(
    items: Iterable[T],
    n: int,
    key: Callable[[T], float] = lambda x: x,
    algorithm: str = "heap"
) -> List[Tuple[T, float]]:
    """
    Find top-N items using the specified algorithm.
    
    Args:
        items: Iterable of items
        n: Number of top items to find
        key: Function to extract score from item
        algorithm: "heap" or "quickselect" (requires list input)
    
    Returns:
        List of (item, score) tuples in descending order
    
    Examples:
        >>> top_n([3, 1, 4, 1, 5, 9, 2, 6], 3)
        [(9, 9), (6, 6), (5, 5)]
        >>> top_n([3, 1, 4, 1, 5, 9, 2, 6], 3, key=lambda x: -x)  # Bottom 3
        [(1, -1), (1, -1), (2, -2)]
    """
    if algorithm == "quickselect":
        if not isinstance(items, list):
            items = list(items)
        return quickselect_top_n(items, n, key)
    else:
        return heap_top_n(items, n, key)


def bottom_n(
    items: Iterable[T],
    n: int,
    key: Callable[[T], float] = lambda x: x
) -> List[Tuple[T, float]]:
    """
    Find bottom-N items (smallest scores).
    
    Args:
        items: Iterable of items
        n: Number of bottom items to find
        key: Function to extract score from item
    
    Returns:
        List of (item, score) tuples in ascending order
    
    Examples:
        >>> bottom_n([3, 1, 4, 1, 5, 9, 2, 6], 3)
        [(1, 1), (1, 1), (2, 2)]
    """
    # Negate scores to find bottom N, then negate back
    negated = [(-key(item), item) for item in items]
    result = heap_top_n(negated, n, key=lambda x: x[0])
    # Result format is ((neg_score, item), neg_score) from heap_top_n
    # We need to convert back to original scores
    return [(pair[1], -pair[0]) for pair, _ in result]


# Utility for benchmarking

def benchmark_top_n(
    size: int = 100000,
    n: int = 100,
    algorithms: Optional[List[str]] = None
) -> Dict[str, Dict[str, float]]:
    """
    Benchmark different top-N algorithms.
    
    Args:
        size: Number of items to process
        n: Number of top items to find
        algorithms: List of algorithms to benchmark
    
    Returns:
        Dictionary with timing results
    """
    import time
    
    if algorithms is None:
        algorithms = ["heap", "quickselect", "sorted"]
    
    # Generate random data
    random.seed(42)
    data = [random.random() * 1000 for _ in range(size)]
    
    results = {}
    
    for algo in algorithms:
        start = time.perf_counter()
        
        if algo == "heap":
            heap_top_n(data, n)
        elif algo == "quickselect":
            quickselect_top_n(data.copy(), n)
        elif algo == "sorted":
            sorted([(x, x) for x in data], key=lambda x: x[1], reverse=True)[:n]
        
        elapsed = time.perf_counter() - start
        results[algo] = {
            "time_seconds": elapsed,
            "items_per_second": size / elapsed if elapsed > 0 else 0
        }
    
    return results


if __name__ == "__main__":
    # Demo
    print("=" * 60)
    print("Top-N Utils Demo")
    print("=" * 60)
    
    # Basic top-N
    data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    print(f"\nData: {data}")
    print(f"Top 3: {top_n(data, 3)}")
    print(f"Bottom 3: {bottom_n(data, 3)}")
    
    # Using selector
    selector = TopNSelector(lambda x: x, max_size=5)
    selector.add_items(data)
    print(f"\nTopNSelector (max 5): {selector.get_top_n()}")
    
    # Time-windowed
    window = TimeWindowTopN(window_seconds=60, n=5)
    for i, val in enumerate(data[:5]):
        window.add(f"item_{i}", score=val)
    print(f"\nTimeWindowTopN: {window.get_top_n()}")
    
    # Category-based
    cat_top = CategoryTopN(n=3)
    cat_top.add("fruit", "apple", 5.0)
    cat_top.add("fruit", "banana", 3.0)
    cat_top.add("fruit", "cherry", 7.0)
    cat_top.add("vegetable", "carrot", 4.0)
    cat_top.add("vegetable", "broccoli", 6.0)
    print(f"\nCategoryTopN - Fruit: {cat_top.get_top_n('fruit')}")
    print(f"CategoryTopN - Vegetable: {cat_top.get_top_n('vegetable')}")
    
    # Weighted
    weighted = WeightedTopN()
    weighted.add_weight("popularity", 0.5)
    weighted.add_weight("quality", 0.5)
    weighted.add_item("item1", {"popularity": 80, "quality": 90})
    weighted.add_item("item2", {"popularity": 90, "quality": 70})
    print(f"\nWeightedTopN: {weighted.get_top_n()}")
    
    # Incremental
    inc = IncrementalTopN(n=3)
    inc.update("player1", 100)
    inc.update("player2", 95)
    inc.update("player1", 110)  # Update
    print(f"\nIncrementalTopN: {inc.get_top_n()}")
    print(f"Rank of player2: {inc.get_rank('player2')}")
    
    print("\n" + "=" * 60)