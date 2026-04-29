"""
LFU Cache Utils - Least Frequently Used Cache Implementation

A thread-safe LFU (Least Frequently Used) cache implementation with O(1) 
time complexity for get, put, and eviction operations.

Features:
- O(1) get, put, and eviction operations
- Thread-safe operations
- Configurable capacity
- Frequency-based eviction with LRU tiebreaker
- Statistics tracking (hits, misses, evictions)
- Zero external dependencies

Author: AllToolkit
Date: 2026-04-30
"""

from collections import defaultdict
from threading import RLock
from typing import Any, Generic, Hashable, Optional, TypeVar, List, Tuple, Dict
from dataclasses import dataclass, field
import time

K = TypeVar('K', bound=Hashable)
V = TypeVar('V')


@dataclass
class CacheStats:
    """Cache statistics container."""
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    current_size: int = 0
    
    @property
    def hit_rate(self) -> float:
        """Calculate cache hit rate."""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0
    
    def reset(self) -> None:
        """Reset all statistics."""
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.current_size = 0


class Node(Generic[K, V]):
    """Doubly linked list node for cache entries."""
    
    __slots__ = ['key', 'value', 'freq', 'prev', 'next', 'access_time']
    
    def __init__(self, key: K, value: V):
        self.key: K = key
        self.value: V = value
        self.freq: int = 1
        self.prev: Optional['Node[K, V]'] = None
        self.next: Optional['Node[K, V]'] = None
        self.access_time: float = time.time()


class DoublyLinkedList(Generic[K, V]):
    """Doubly linked list for nodes with same frequency."""
    
    __slots__ = ['head', 'tail', 'size']
    
    def __init__(self):
        self.head: Optional[Node[K, V]] = None
        self.tail: Optional[Node[K, V]] = None
        self.size: int = 0
    
    def append(self, node: Node[K, V]) -> None:
        """Add node to the end of the list."""
        node.prev = None
        node.next = None
        
        if self.tail is None:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        
        self.size += 1
    
    def remove(self, node: Node[K, V]) -> None:
        """Remove node from the list."""
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        
        node.prev = None
        node.next = None
        self.size -= 1
    
    def pop_head(self) -> Optional[Node[K, V]]:
        """Remove and return the head node (oldest/least recently used)."""
        if self.head is None:
            return None
        
        node = self.head
        self.remove(node)
        return node
    
    def is_empty(self) -> bool:
        """Check if list is empty."""
        return self.size == 0


class LFUCache(Generic[K, V]):
    """
    Thread-safe LFU (Least Frequently Used) Cache.
    
    Evicts the least frequently accessed items when capacity is reached.
    Uses LRU (Least Recently Used) as a tiebreaker for items with the same frequency.
    
    Time Complexity:
        - get: O(1)
        - put: O(1)
        - eviction: O(1)
    
    Example:
        >>> cache = LFUCache(capacity=3)
        >>> cache.put('a', 1)
        >>> cache.put('b', 2)
        >>> cache.put('c', 3)
        >>> cache.get('a')  # 'a' now has frequency 2
        1
        >>> cache.put('d', 4)  # Evicts 'b' (frequency 1, oldest)
        >>> 'b' in cache
        False
    """
    
    def __init__(self, capacity: int = 128):
        """
        Initialize LFU cache.
        
        Args:
            capacity: Maximum number of items to store. Must be positive.
        
        Raises:
            ValueError: If capacity is not positive.
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        
        self._capacity: int = capacity
        self._min_freq: int = 0
        self._cache: Dict[K, Node[K, V]] = {}
        self._freq_map: Dict[int, DoublyLinkedList[K, V]] = defaultdict(DoublyLinkedList)
        self._lock = RLock()
        self._stats = CacheStats()
    
    @property
    def capacity(self) -> int:
        """Get cache capacity."""
        return self._capacity
    
    @property
    def size(self) -> int:
        """Get current cache size."""
        with self._lock:
            return len(self._cache)
    
    @property
    def stats(self) -> CacheStats:
        """Get cache statistics (copy)."""
        with self._lock:
            return CacheStats(
                hits=self._stats.hits,
                misses=self._stats.misses,
                evictions=self._stats.evictions,
                current_size=len(self._cache)
            )
    
    def get(self, key: K) -> Optional[V]:
        """
        Get value by key, updating frequency.
        
        Args:
            key: Cache key.
        
        Returns:
            Value if found, None otherwise.
        """
        with self._lock:
            node = self._cache.get(key)
            
            if node is None:
                self._stats.misses += 1
                return None
            
            self._stats.hits += 1
            self._update_freq(node)
            return node.value
    
    def put(self, key: K, value: V) -> Optional[V]:
        """
        Put key-value pair into cache.
        
        If cache is at capacity, evicts the least frequently used item.
        If multiple items have the same minimum frequency, evicts the 
        least recently used among them.
        
        Args:
            key: Cache key.
            value: Cache value.
        
        Returns:
            Evicted value if eviction occurred, None otherwise.
        """
        with self._lock:
            if key in self._cache:
                node = self._cache[key]
                old_value = node.value
                node.value = value
                self._update_freq(node)
                return None
            
            evicted_value = None
            
            if len(self._cache) >= self._capacity:
                evicted_value = self._evict()
            
            node = Node(key, value)
            self._cache[key] = node
            self._freq_map[1].append(node)
            self._min_freq = 1
            self._stats.current_size = len(self._cache)
            
            return evicted_value
    
    def delete(self, key: K) -> Optional[V]:
        """
        Delete key from cache.
        
        Args:
            key: Cache key to delete.
        
        Returns:
            Deleted value if key existed, None otherwise.
        """
        with self._lock:
            node = self._cache.pop(key, None)
            
            if node is None:
                return None
            
            freq_list = self._freq_map[node.freq]
            freq_list.remove(node)
            
            if freq_list.is_empty() and node.freq == self._min_freq:
                self._min_freq += 1
            
            self._stats.current_size = len(self._cache)
            return node.value
    
    def clear(self) -> None:
        """Clear all items from cache."""
        with self._lock:
            self._cache.clear()
            self._freq_map.clear()
            self._min_freq = 0
            self._stats.current_size = 0
    
    def reset_stats(self) -> None:
        """Reset cache statistics."""
        with self._lock:
            self._stats.reset()
            self._stats.current_size = len(self._cache)
    
    def contains(self, key: K) -> bool:
        """Check if key exists in cache."""
        with self._lock:
            return key in self._cache
    
    def peek(self, key: K) -> Optional[V]:
        """Get value without updating frequency or stats."""
        with self._lock:
            node = self._cache.get(key)
            return node.value if node else None
    
    def get_freq(self, key: K) -> int:
        """Get access frequency for a key."""
        with self._lock:
            node = self._cache.get(key)
            return node.freq if node else 0
    
    def keys(self) -> List[K]:
        """Get all keys in cache."""
        with self._lock:
            return list(self._cache.keys())
    
    def values(self) -> List[V]:
        """Get all values in cache."""
        with self._lock:
            return [node.value for node in self._cache.values()]
    
    def items(self) -> List[Tuple[K, V]]:
        """Get all key-value pairs in cache."""
        with self._lock:
            return [(key, node.value) for key, node in self._cache.items()]
    
    def _update_freq(self, node: Node[K, V]) -> None:
        """Update node frequency (internal method)."""
        old_freq = node.freq
        new_freq = old_freq + 1
        
        old_list = self._freq_map[old_freq]
        old_list.remove(node)
        
        if old_list.is_empty() and old_freq == self._min_freq:
            self._min_freq = new_freq
        
        node.freq = new_freq
        node.access_time = time.time()
        self._freq_map[new_freq].append(node)
    
    def _evict(self) -> V:
        """Evict least frequently used item (internal method)."""
        min_list = self._freq_map[self._min_freq]
        node = min_list.pop_head()
        
        if node:
            del self._cache[node.key]
            self._stats.evictions += 1
            self._stats.current_size = len(self._cache)
            return node.value
        
        return None
    
    def __contains__(self, key: K) -> bool:
        return self.contains(key)
    
    def __len__(self) -> int:
        return self.size
    
    def __repr__(self) -> str:
        return f"LFUCache(capacity={self._capacity}, size={self.size}, hit_rate={self.stats.hit_rate:.2%})"


class LFUCacheBuilder(Generic[K, V]):
    """Builder pattern for creating LFU caches with custom configuration."""
    
    def __init__(self):
        self._capacity: int = 128
        self._initial_items: Dict[K, V] = {}
    
    def capacity(self, capacity: int) -> 'LFUCacheBuilder[K, V]':
        """Set cache capacity."""
        self._capacity = capacity
        return self
    
    def initial_items(self, items: Dict[K, V]) -> 'LFUCacheBuilder[K, V]':
        """Set initial items to populate cache."""
        self._initial_items = items
        return self
    
    def build(self) -> LFUCache[K, V]:
        """Build the LFU cache."""
        cache = LFUCache(capacity=self._capacity)
        for key, value in self._initial_items.items():
            cache.put(key, value)
        return cache


def create_lfu_cache(capacity: int = 128) -> LFUCache:
    """Factory function to create an LFU cache."""
    return LFUCache(capacity=capacity)


def lfu_cache_decorator(capacity: int = 128):
    """
    Decorator to memoize function results using LFU cache.
    
    Args:
        capacity: Maximum cache size.
    
    Returns:
        Decorator function.
    
    Example:
        >>> @lfu_cache_decorator(capacity=100)
        ... def expensive_function(n):
        ...     return n ** 2
        >>> expensive_function(5)  # Computed
        25
        >>> expensive_function(5)  # Cached
        25
    """
    cache = LFUCache(capacity=capacity)
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Create hashable key from arguments
            key = (args, tuple(sorted(kwargs.items())))
            
            result = cache.get(key)
            if result is not None:
                return result
            
            result = func(*args, **kwargs)
            cache.put(key, result)
            return result
        
        wrapper.cache = cache
        wrapper.cache_clear = cache.clear
        wrapper.cache_stats = lambda: cache.stats
        
        return wrapper
    
    return decorator


if __name__ == "__main__":
    # Quick demo
    cache = LFUCache(capacity=3)
    
    cache.put('a', 1)
    cache.put('b', 2)
    cache.put('c', 3)
    
    print(f"Cache: {cache}")
    print(f"get('a'): {cache.get('a')}")  # freq=2
    print(f"get('a'): {cache.get('a')}")  # freq=3
    print(f"get('b'): {cache.get('b')}")  # freq=2
    
    print("\nAdding 'd' - should evict 'c' (lowest frequency)")
    evicted = cache.put('d', 4)
    print(f"Evicted: {evicted}")
    print(f"'c' in cache: {'c' in cache}")
    print(f"'a' in cache: {'a' in cache}")
    
    print(f"\nStats: {cache.stats}")