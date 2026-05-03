"""
LRU Cache Utility Module

A comprehensive LRU (Least Recently Used) cache implementation with zero external dependencies.
Provides efficient O(1) operations for get, put, and eviction.

Features:
- Generic key-value cache with configurable capacity
- O(1) time complexity for all operations using doubly linked list + hash map
- Optional TTL (Time-To-Live) support for automatic expiration
- Thread-safe mode with optional locking
- Statistics tracking (hits, misses, evictions)
- Batch operations (put_all, get_all)
- Decorator for function result caching
- Support for custom eviction callbacks
"""

from typing import Generic, TypeVar, Optional, Callable, Dict, List, Tuple, Any
from time import time
from threading import RLock
from functools import wraps

K = TypeVar('K')
V = TypeVar('V')


class Node(Generic[K, V]):
    """Doubly linked list node for LRU cache."""
    
    __slots__ = ['key', 'value', 'prev', 'next', 'expires_at', 'access_count']
    
    def __init__(self, key: K, value: V, ttl: Optional[float] = None):
        self.key = key
        self.value = value
        self.prev: Optional['Node[K, V]'] = None
        self.next: Optional['Node[K, V]'] = None
        self.expires_at = time() + ttl if ttl else None
        self.access_count = 0


class LRUCache(Generic[K, V]):
    """
    LRU Cache implementation with O(1) operations.
    
    Uses a doubly linked list for ordering and a hash map for O(1) access.
    Most recently used items are at the head, least recently used at the tail.
    
    Example:
        cache = LRUCache[str, int](capacity=3)
        cache.put('a', 1)
        cache.put('b', 2)
        cache.put('c', 3)
        cache.put('d', 4)  # 'a' is evicted
        print(cache.get('b'))  # 2
    """
    
    def __init__(self, capacity: int, 
                 ttl: Optional[float] = None,
                 thread_safe: bool = False,
                 on_evict: Optional[Callable[[K, V], None]] = None):
        """
        Initialize LRU cache.
        
        Args:
            capacity: Maximum number of items in cache
            ttl: Default time-to-live in seconds for items (None = no expiration)
            thread_safe: Enable thread-safe operations with locking
            on_evict: Callback function called when an item is evicted
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        
        self._capacity = capacity
        self._default_ttl = ttl
        self._thread_safe = thread_safe
        self._on_evict = on_evict
        
        # Hash map for O(1) access
        self._cache: Dict[K, Node[K, V]] = {}
        
        # Dummy head and tail for easier manipulation
        self._head = Node(None, None)  # type: ignore
        self._tail = Node(None, None)  # type: ignore
        self._head.next = self._tail
        self._tail.prev = self._head
        
        # Statistics
        self._hits = 0
        self._misses = 0
        self._evictions = 0
        self._expirations = 0
        
        # Lock for thread safety
        self._lock = RLock() if thread_safe else None
    
    def _remove_node(self, node: Node[K, V]) -> None:
        """Remove a node from the linked list."""
        prev_node = node.prev
        next_node = node.next
        if prev_node:
            prev_node.next = next_node
        if next_node:
            next_node.prev = prev_node
    
    def _add_to_head(self, node: Node[K, V]) -> None:
        """Add a node right after the head (most recently used)."""
        node.prev = self._head
        node.next = self._head.next
        if self._head.next:
            self._head.next.prev = node
        self._head.next = node
    
    def _move_to_head(self, node: Node[K, V]) -> None:
        """Move an existing node to the head."""
        self._remove_node(node)
        self._add_to_head(node)
    
    def _remove_tail(self) -> Node[K, V]:
        """Remove and return the tail node (least recently used)."""
        node = self._tail.prev
        if node and node != self._head:
            self._remove_node(node)
            return node
        raise IndexError("Cache is empty")
    
    def _is_expired(self, node: Node[K, V]) -> bool:
        """Check if a node has expired."""
        if node.expires_at is None:
            return False
        return time() > node.expires_at
    
    def _evict_expired(self) -> int:
        """Remove all expired items. Returns count of evicted items."""
        expired_keys = []
        for key, node in self._cache.items():
            if self._is_expired(node):
                expired_keys.append(key)
        
        for key in expired_keys:
            self._remove_node(self._cache[key])
            del self._cache[key]
            self._expirations += 1
        
        return len(expired_keys)
    
    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        """
        Get a value by key.
        
        Args:
            key: The key to look up
            default: Value to return if key not found
            
        Returns:
            The cached value or default
        """
        if self._lock:
            with self._lock:
                return self._get_internal(key, default)
        return self._get_internal(key, default)
    
    def _get_internal(self, key: K, default: Optional[V] = None) -> Optional[V]:
        """Internal get without locking."""
        if key not in self._cache:
            self._misses += 1
            return default
        
        node = self._cache[key]
        
        # Check expiration
        if self._is_expired(node):
            self._remove_node(node)
            del self._cache[key]
            self._expirations += 1
            self._misses += 1
            return default
        
        # Move to head (most recently used)
        self._move_to_head(node)
        node.access_count += 1
        self._hits += 1
        
        return node.value
    
    def put(self, key: K, value: V, ttl: Optional[float] = None) -> Optional[V]:
        """
        Put a key-value pair into the cache.
        
        Args:
            key: The key
            value: The value
            ttl: Time-to-live in seconds (overrides default TTL)
            
        Returns:
            The evicted value if capacity was exceeded, None otherwise
        """
        if self._lock:
            with self._lock:
                return self._put_internal(key, value, ttl)
        return self._put_internal(key, value, ttl)
    
    def _put_internal(self, key: K, value: V, ttl: Optional[float] = None) -> Optional[V]:
        """Internal put without locking."""
        # Check if key exists
        if key in self._cache:
            node = self._cache[key]
            
            # Check expiration
            if self._is_expired(node):
                self._remove_node(node)
                del self._cache[key]
                self._expirations += 1
            else:
                # Update existing node
                old_value = node.value
                node.value = value
                if ttl is not None or self._default_ttl is not None:
                    node.expires_at = time() + (ttl if ttl is not None else self._default_ttl)
                self._move_to_head(node)
                return old_value
        
        # Check capacity and evict if necessary
        evicted_value = None
        if len(self._cache) >= self._capacity:
            # Clean up expired items first
            self._evict_expired()
            
            # Still need to evict?
            if len(self._cache) >= self._capacity:
                tail_node = self._remove_tail()
                del self._cache[tail_node.key]
                evicted_value = tail_node.value
                self._evictions += 1
                if self._on_evict:
                    self._on_evict(tail_node.key, tail_node.value)
        
        # Create new node
        actual_ttl = ttl if ttl is not None else self._default_ttl
        new_node = Node(key, value, actual_ttl)
        self._cache[key] = new_node
        self._add_to_head(new_node)
        
        return evicted_value
    
    def delete(self, key: K) -> bool:
        """
        Delete a key from the cache.
        
        Args:
            key: The key to delete
            
        Returns:
            True if the key was found and deleted
        """
        if self._lock:
            with self._lock:
                return self._delete_internal(key)
        return self._delete_internal(key)
    
    def _delete_internal(self, key: K) -> bool:
        """Internal delete without locking."""
        if key not in self._cache:
            return False
        
        node = self._cache[key]
        self._remove_node(node)
        del self._cache[key]
        return True
    
    def contains(self, key: K) -> bool:
        """
        Check if a key exists in the cache.
        
        Args:
            key: The key to check
            
        Returns:
            True if the key exists and hasn't expired
        """
        if self._lock:
            with self._lock:
                return self._contains_internal(key)
        return self._contains_internal(key)
    
    def _contains_internal(self, key: K) -> bool:
        """Internal contains check without locking."""
        if key not in self._cache:
            return False
        
        node = self._cache[key]
        if self._is_expired(node):
            self._remove_node(node)
            del self._cache[key]
            self._expirations += 1
            return False
        
        return True
    
    def clear(self) -> None:
        """Clear all items from the cache."""
        if self._lock:
            with self._lock:
                self._cache.clear()
                self._head.next = self._tail
                self._tail.prev = self._head
                return
        self._cache.clear()
        self._head.next = self._tail
        self._tail.prev = self._head
    
    def size(self) -> int:
        """Get the current number of items in cache."""
        if self._lock:
            with self._lock:
                return len(self._cache)
        return len(self._cache)
    
    def is_empty(self) -> bool:
        """Check if the cache is empty."""
        return self.size() == 0
    
    def is_full(self) -> bool:
        """Check if the cache is at capacity."""
        return self.size() >= self._capacity
    
    def keys(self) -> List[K]:
        """Get all keys in LRU order (most recent first)."""
        if self._lock:
            with self._lock:
                return self._keys_internal()
        return self._keys_internal()
    
    def _keys_internal(self) -> List[K]:
        """Internal keys without locking."""
        keys = []
        node = self._head.next
        while node and node != self._tail:
            if not self._is_expired(node):
                keys.append(node.key)
            node = node.next
        return keys
    
    def values(self) -> List[V]:
        """Get all values in LRU order (most recent first)."""
        if self._lock:
            with self._lock:
                return self._values_internal()
        return self._values_internal()
    
    def _values_internal(self) -> List[V]:
        """Internal values without locking."""
        values = []
        node = self._head.next
        while node and node != self._tail:
            if not self._is_expired(node):
                values.append(node.value)
            node = node.next
        return values
    
    def items(self) -> List[Tuple[K, V]]:
        """Get all key-value pairs in LRU order (most recent first)."""
        if self._lock:
            with self._lock:
                return self._items_internal()
        return self._items_internal()
    
    def _items_internal(self) -> List[Tuple[K, V]]:
        """Internal items without locking."""
        items = []
        node = self._head.next
        while node and node != self._tail:
            if not self._is_expired(node):
                items.append((node.key, node.value))
            node = node.next
        return items
    
    def put_all(self, items: Dict[K, V], ttl: Optional[float] = None) -> None:
        """
        Put multiple items into the cache.
        
        Args:
            items: Dictionary of key-value pairs
            ttl: Time-to-live for all items
        """
        if self._lock:
            with self._lock:
                for key, value in items.items():
                    self._put_internal(key, value, ttl)
                return
        for key, value in items.items():
            self._put_internal(key, value, ttl)
    
    def get_all(self, keys: List[K]) -> Dict[K, V]:
        """
        Get multiple values by keys.
        
        Args:
            keys: List of keys to look up
            
        Returns:
            Dictionary of found key-value pairs
        """
        result = {}
        if self._lock:
            with self._lock:
                for key in keys:
                    value = self._get_internal(key)
                    if value is not None:
                        result[key] = value
                return result
        for key in keys:
            value = self._get_internal(key)
            if value is not None:
                result[key] = value
        return result
    
    def get_or_set(self, key: K, factory: Callable[[], V], ttl: Optional[float] = None) -> V:
        """
        Get a value, or compute and set it if not present.
        
        Args:
            key: The key to look up
            factory: Function to compute the value if not found
            ttl: Time-to-live for the computed value
            
        Returns:
            The cached or computed value
        """
        if self._lock:
            with self._lock:
                value = self._get_internal(key)
                if value is not None:
                    return value
                value = factory()
                self._put_internal(key, value, ttl)
                return value
        
        value = self.get(key)
        if value is not None:
            return value
        value = factory()
        self.put(key, value, ttl)
        return value
    
    def peek(self, key: K) -> Optional[V]:
        """
        Peek at a value without updating its LRU position.
        
        Args:
            key: The key to peek at
            
        Returns:
            The cached value or None
        """
        if self._lock:
            with self._lock:
                if key not in self._cache:
                    return None
                node = self._cache[key]
                if self._is_expired(node):
                    return None
                return node.value
        
        if key not in self._cache:
            return None
        node = self._cache[key]
        if self._is_expired(node):
            return None
        return node.value
    
    def touch(self, key: K) -> bool:
        """
        Touch a key to move it to the head (most recently used).
        
        Args:
            key: The key to touch
            
        Returns:
            True if the key was found and touched
        """
        if self._lock:
            with self._lock:
                if key not in self._cache:
                    return False
                node = self._cache[key]
                if self._is_expired(node):
                    return False
                self._move_to_head(node)
                node.access_count += 1
                return True
        
        if key not in self._cache:
            return False
        node = self._cache[key]
        if self._is_expired(node):
            return False
        self._move_to_head(node)
        node.access_count += 1
        return True
    
    def refresh_ttl(self, key: K, ttl: Optional[float] = None) -> bool:
        """
        Refresh the TTL for a key.
        
        Args:
            key: The key to refresh
            ttl: New TTL (uses default if None)
            
        Returns:
            True if the key was found and refreshed
        """
        if self._lock:
            with self._lock:
                if key not in self._cache:
                    return False
                node = self._cache[key]
                if self._is_expired(node):
                    return False
                actual_ttl = ttl if ttl is not None else self._default_ttl
                node.expires_at = time() + actual_ttl if actual_ttl else None
                return True
        
        if key not in self._cache:
            return False
        node = self._cache[key]
        if self._is_expired(node):
            return False
        actual_ttl = ttl if ttl is not None else self._default_ttl
        node.expires_at = time() + actual_ttl if actual_ttl else None
        return True
    
    @property
    def capacity(self) -> int:
        """Get the cache capacity."""
        return self._capacity
    
    @capacity.setter
    def capacity(self, new_capacity: int) -> None:
        """
        Set a new capacity (may trigger evictions).
        
        Args:
            new_capacity: New maximum capacity
        """
        if new_capacity <= 0:
            raise ValueError("Capacity must be positive")
        
        if self._lock:
            with self._lock:
                self._capacity = new_capacity
                while len(self._cache) > new_capacity:
                    tail_node = self._remove_tail()
                    del self._cache[tail_node.key]
                    self._evictions += 1
                    if self._on_evict:
                        self._on_evict(tail_node.key, tail_node.value)
                return
        
        self._capacity = new_capacity
        while len(self._cache) > new_capacity:
            tail_node = self._remove_tail()
            del self._cache[tail_node.key]
            self._evictions += 1
            if self._on_evict:
                self._on_evict(tail_node.key, tail_node.value)
    
    def stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with hit rate, hits, misses, evictions, expirations
        """
        total = self._hits + self._misses
        hit_rate = self._hits / total if total > 0 else 0.0
        
        return {
            'capacity': self._capacity,
            'size': len(self._cache),
            'hits': self._hits,
            'misses': self._misses,
            'evictions': self._evictions,
            'expirations': self._expirations,
            'hit_rate': hit_rate,
            'utilization': len(self._cache) / self._capacity,
        }
    
    def reset_stats(self) -> None:
        """Reset statistics counters."""
        self._hits = 0
        self._misses = 0
        self._evictions = 0
        self._expirations = 0
    
    def __len__(self) -> int:
        return self.size()
    
    def __contains__(self, key: K) -> bool:
        return self.contains(key)
    
    def __getitem__(self, key: K) -> V:
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value
    
    def __setitem__(self, key: K, value: V) -> None:
        self.put(key, value)
    
    def __delitem__(self, key: K) -> None:
        if not self.delete(key):
            raise KeyError(key)
    
    def __repr__(self) -> str:
        return f"LRUCache(capacity={self._capacity}, size={len(self._cache)}, hits={self._hits}, misses={self._misses})"


def lru_cache(capacity: int, ttl: Optional[float] = None, 
              thread_safe: bool = False) -> Callable:
    """
    Decorator for caching function results.
    
    Args:
        capacity: Maximum number of results to cache
        ttl: Time-to-live for cached results
        thread_safe: Enable thread-safe operations
        
    Returns:
        Decorator function
        
    Example:
        @lru_cache(capacity=100)
        def fibonacci(n):
            if n < 2:
                return n
            return fibonacci(n-1) + fibonacci(n-2)
    """
    cache = LRUCache(capacity=capacity, ttl=ttl, thread_safe=thread_safe)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create a hashable key from arguments
            key = (args, tuple(sorted(kwargs.items())))
            
            # Try to get from cache
            result = cache.get(key)
            if result is not None or cache.contains(key):
                return result
            
            # Compute and cache
            result = func(*args, **kwargs)
            cache.put(key, result)
            return result
        
        # Attach cache to wrapper for external access
        wrapper.cache = cache  # type: ignore
        wrapper.cache_clear = cache.clear  # type: ignore
        wrapper.cache_stats = cache.stats  # type: ignore
        
        return wrapper
    
    return decorator


def memoize(func: Callable) -> Callable:
    """
    Simple memoization decorator with unlimited cache.
    
    Unlike lru_cache, this never evicts items.
    
    Example:
        @memoize
        def expensive_computation(n):
            return sum(range(n))
    """
    cache: Dict = {}
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    
    wrapper.cache = cache  # type: ignore
    wrapper.cache_clear = cache.clear  # type: ignore
    
    return wrapper


class TTLCache(Generic[K, V]):
    """
    TTL-only cache (no LRU eviction, only expiration).
    
    Items are only removed when they expire, not based on access order.
    """
    
    def __init__(self, ttl: float, cleanup_interval: Optional[float] = None):
        """
        Initialize TTL cache.
        
        Args:
            ttl: Default time-to-live in seconds
            cleanup_interval: How often to clean up expired items (default: ttl)
        """
        self._ttl = ttl
        self._cleanup_interval = cleanup_interval or ttl
        self._cache: Dict[K, Tuple[V, float]] = {}  # key -> (value, expires_at)
        self._last_cleanup = time()
        self._lock = RLock()
    
    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        """Get a value by key."""
        with self._lock:
            self._maybe_cleanup()
            
            if key not in self._cache:
                return default
            
            value, expires_at = self._cache[key]
            if time() > expires_at:
                del self._cache[key]
                return default
            
            return value
    
    def put(self, key: K, value: V, ttl: Optional[float] = None) -> None:
        """Put a key-value pair."""
        with self._lock:
            actual_ttl = ttl if ttl is not None else self._ttl
            self._cache[key] = (value, time() + actual_ttl)
    
    def delete(self, key: K) -> bool:
        """Delete a key."""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False
    
    def _maybe_cleanup(self) -> None:
        """Clean up expired items if cleanup interval has passed."""
        now = time()
        if now - self._last_cleanup >= self._cleanup_interval:
            expired = [k for k, (_, exp) in self._cache.items() if now > exp]
            for k in expired:
                del self._cache[k]
            self._last_cleanup = now
    
    def clear(self) -> None:
        """Clear all items."""
        with self._lock:
            self._cache.clear()
    
    def size(self) -> int:
        """Get current size."""
        with self._lock:
            self._maybe_cleanup()
            return len(self._cache)


if __name__ == '__main__':
    # Demo
    print("=== LRU Cache Utility Demo ===\n")
    
    # Basic usage
    cache = LRUCache[str, int](capacity=3)
    
    print("Basic Operations:")
    cache.put('a', 1)
    cache.put('b', 2)
    cache.put('c', 3)
    print(f"  Added a=1, b=2, c=3")
    print(f"  Cache: {cache.items()}")
    
    cache.put('d', 4)  # 'a' should be evicted
    print(f"  Added d=4 (a should be evicted)")
    print(f"  Cache: {cache.items()}")
    print(f"  Get 'a': {cache.get('a')} (should be None)")
    print(f"  Get 'b': {cache.get('b')}")
    
    # Statistics
    print(f"\nStatistics:")
    stats = cache.stats()
    for k, v in stats.items():
        print(f"  {k}: {v}")
    
    # TTL example
    print("\nTTL Example:")
    ttl_cache = LRUCache[str, str](capacity=10, ttl=0.1)  # 100ms TTL
    ttl_cache.put('temp', 'will expire')
    print(f"  Added temp with 100ms TTL")
    print(f"  Immediate get: {ttl_cache.get('temp')}")
    import time as time_module
    time_module.sleep(0.15)
    print(f"  After 150ms: {ttl_cache.get('temp')} (should be None)")
    
    # Decorator example
    print("\nDecorator Example:")
    
    @lru_cache(capacity=5)
    def fib(n: int) -> int:
        if n < 2:
            return n
        return fib(n - 1) + fib(n - 2)
    
    print(f"  fib(10) = {fib(10)}")
    print(f"  Cache stats: {fib.cache.stats()}")  # type: ignore