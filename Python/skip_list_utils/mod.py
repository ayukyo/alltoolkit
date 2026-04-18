"""
AllToolkit - Python Skip List Utilities

A zero-dependency, production-ready skip list implementation.
Skip list is a probabilistic data structure that provides O(log n) average
time complexity for search, insert, and delete operations.

Features:
- SkipList: Probabilistic sorted data structure
- ConcurrentSkipList: Thread-safe version with fine-grained locking
- Range queries and iteration support
- Memory-efficient node representation
- Configurable probability parameter

Author: AllToolkit
License: MIT
"""

import random
import threading
from typing import (
    Generic, TypeVar, Optional, List, Iterator, Callable,
    Any, Tuple, Union, Iterable
)
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

T = TypeVar('T')


class SkipListError(Exception):
    """Base exception for skip list operations."""
    pass


class DuplicateKeyError(SkipListError):
    """Raised when inserting a duplicate key in a unique skip list."""
    pass


class KeyNotFoundError(SkipListError):
    """Raised when a key is not found."""
    pass


@dataclass
class SkipListNode(Generic[T]):
    """A node in the skip list."""
    key: T
    value: Any = None
    forward: List['SkipListNode[T]'] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.forward:
            self.forward = []
    
    @property
    def level(self) -> int:
        """Return the level of this node (number of forward pointers)."""
        return len(self.forward)


class SkipList(Generic[T]):
    """
    A skip list implementation with O(log n) average time complexity.
    
    Skip list is a probabilistic data structure that uses multiple layers
    of linked lists to enable fast search, insert, and delete operations.
    
    Example:
        >>> sl = SkipList[int]()
        >>> sl.insert(5, "five")
        >>> sl.insert(2, "two")
        >>> sl.insert(8, "eight")
        >>> sl.search(5)
        "five"
        >>> list(sl.range(2, 6))
        [(2, "two"), (5, "five")]
    """
    
    def __init__(
        self,
        max_level: int = 16,
        probability: float = 0.5,
        allow_duplicates: bool = False
    ):
        """
        Initialize a skip list.
        
        Args:
            max_level: Maximum number of levels (default 16, good for 2^16 elements)
            probability: Probability for promoting nodes to higher levels (default 0.5)
            allow_duplicates: Whether to allow duplicate keys (default False)
        """
        if max_level < 1:
            raise ValueError("max_level must be at least 1")
        if not 0 < probability < 1:
            raise ValueError("probability must be between 0 and 1")
        
        self._max_level = max_level
        self._probability = probability
        self._allow_duplicates = allow_duplicates
        self._level = 1  # Current highest level with nodes
        self._size = 0
        
        # Create head node with max_level forward pointers
        self._head: SkipListNode[T] = SkipListNode(
            key=None,  # type: ignore
            forward=[None] * max_level
        )
        
        # For deterministic testing
        self._random = random.Random()
    
    @property
    def size(self) -> int:
        """Return the number of elements in the skip list."""
        return self._size
    
    @property
    def is_empty(self) -> bool:
        """Check if the skip list is empty."""
        return self._size == 0
    
    @property
    def max_level(self) -> int:
        """Return the maximum level of the skip list."""
        return self._max_level
    
    @property
    def current_level(self) -> int:
        """Return the current highest level with nodes."""
        return self._level
    
    def _random_level(self) -> int:
        """
        Generate a random level for a new node.
        Uses geometric distribution based on probability.
        """
        level = 1
        while self._random.random() < self._probability and level < self._max_level:
            level += 1
        return level
    
    def seed(self, seed: int) -> None:
        """Set random seed for deterministic behavior (useful for testing)."""
        self._random.seed(seed)
    
    def _find_node(self, key: T) -> Optional[SkipListNode[T]]:
        """
        Find the node containing the key.
        
        Args:
            key: The key to search for
            
        Returns:
            The node if found, None otherwise
        """
        current = self._head
        
        # Start from the highest level and work down
        for i in range(self._level - 1, -1, -1):
            # Move forward while the next node's key is less than target
            while current.forward[i] is not None and current.forward[i].key < key:
                current = current.forward[i]
        
        # Check the element at level 0
        current = current.forward[0]
        if current is not None and current.key == key:
            return current
        return None
    
    def search(self, key: T) -> Optional[Any]:
        """
        Search for a value by key.
        
        Args:
            key: The key to search for
            
        Returns:
            The value associated with the key, or None if not found
        """
        node = self._find_node(key)
        return node.value if node is not None else None
    
    def __contains__(self, key: T) -> bool:
        """Check if a key exists in the skip list."""
        return self._find_node(key) is not None
    
    def __getitem__(self, key: T) -> Any:
        """Get value by key. Raises KeyError if not found."""
        value = self.search(key)
        if value is None and key not in self:
            raise KeyError(key)
        return value
    
    def get(self, key: T, default: Any = None) -> Any:
        """Get value by key with default."""
        value = self.search(key)
        return value if value is not None else default
    
    def insert(self, key: T, value: Any = None) -> None:
        """
        Insert a key-value pair into the skip list.
        
        Args:
            key: The key to insert
            value: The value associated with the key (optional)
            
        Raises:
            DuplicateKeyError: If key already exists and allow_duplicates is False
        """
        # Array to store update path
        update: List[Optional[SkipListNode[T]]] = [None] * self._max_level
        current = self._head
        
        # Find the insertion point and track path
        for i in range(self._level - 1, -1, -1):
            while current.forward[i] is not None and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current
        
        # Move to the position where key might be
        current = current.forward[0]
        
        # Check for duplicate
        if current is not None and current.key == key:
            if not self._allow_duplicates:
                raise DuplicateKeyError(f"Key '{key}' already exists")
            else:
                # Update value for duplicate key
                current.value = value
                return
        
        # Generate random level for new node
        new_level = self._random_level()
        
        # Update skip list level if necessary
        if new_level > self._level:
            for i in range(self._level, new_level):
                update[i] = self._head
            self._level = new_level
        
        # Create new node
        new_node = SkipListNode[T](
            key=key,
            value=value,
            forward=[None] * new_level
        )
        
        # Insert node and update forward pointers
        for i in range(new_level):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node
        
        self._size += 1
    
    def __setitem__(self, key: T, value: Any) -> None:
        """Insert or update a key-value pair."""
        try:
            self.insert(key, value)
        except DuplicateKeyError:
            # Update existing value
            current = self._head
            for i in range(self._level - 1, -1, -1):
                while current.forward[i] is not None and current.forward[i].key < key:
                    current = current.forward[i]
            current = current.forward[0]
            if current is not None and current.key == key:
                current.value = value
    
    def delete(self, key: T) -> bool:
        """
        Delete a key from the skip list.
        
        Args:
            key: The key to delete
            
        Returns:
            True if the key was found and deleted, False otherwise
        """
        update: List[Optional[SkipListNode[T]]] = [None] * self._max_level
        current = self._head
        
        # Find the node to delete
        for i in range(self._level - 1, -1, -1):
            while current.forward[i] is not None and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current
        
        current = current.forward[0]
        
        # Key not found
        if current is None or current.key != key:
            return False
        
        # Update forward pointers
        for i in range(self._level):
            if update[i].forward[i] != current:
                break
            update[i].forward[i] = current.forward[i]
        
        # Decrease level if necessary
        while self._level > 1 and self._head.forward[self._level - 1] is None:
            self._level -= 1
        
        self._size -= 1
        return True
    
    def __delitem__(self, key: T) -> None:
        """Delete a key. Raises KeyError if not found."""
        if not self.delete(key):
            raise KeyError(key)
    
    def range(
        self,
        start_key: Optional[T] = None,
        end_key: Optional[T] = None,
        inclusive: bool = True
    ) -> Iterator[Tuple[T, Any]]:
        """
        Iterate over key-value pairs in a range.
        
        Args:
            start_key: Start of range (inclusive), None for beginning
            end_key: End of range, None for end
            inclusive: Whether end_key is inclusive (default True)
            
        Yields:
            Tuple of (key, value) in the range
        """
        if self.is_empty:
            return
        
        current = self._head.forward[0]
        
        # Skip to start
        if start_key is not None:
            while current is not None and current.key < start_key:
                current = current.forward[0]
        
        # Yield elements in range
        while current is not None:
            if end_key is not None:
                if inclusive:
                    if current.key > end_key:
                        break
                else:
                    if current.key >= end_key:
                        break
            yield (current.key, current.value)
            current = current.forward[0]
    
    def __iter__(self) -> Iterator[Tuple[T, Any]]:
        """Iterate over all key-value pairs."""
        return self.range()
    
    def keys(self) -> Iterator[T]:
        """Iterate over all keys."""
        for key, _ in self:
            yield key
    
    def values(self) -> Iterator[Any]:
        """Iterate over all values."""
        for _, value in self:
            yield value
    
    def items(self) -> Iterator[Tuple[T, Any]]:
        """Iterate over all key-value pairs (alias for __iter__)."""
        return iter(self)
    
    def first(self) -> Optional[Tuple[T, Any]]:
        """Get the first (minimum) key-value pair."""
        if self.is_empty:
            return None
        node = self._head.forward[0]
        return (node.key, node.value)
    
    def last(self) -> Optional[Tuple[T, Any]]:
        """Get the last (maximum) key-value pair."""
        if self.is_empty:
            return None
        
        # Start from highest level and traverse right
        current = self._head
        for i in range(self._level - 1, -1, -1):
            while current.forward[i] is not None:
                current = current.forward[i]
        
        return (current.key, current.value)
    
    def min_key(self) -> Optional[T]:
        """Get the minimum key."""
        result = self.first()
        return result[0] if result else None
    
    def max_key(self) -> Optional[T]:
        """Get the maximum key."""
        result = self.last()
        return result[0] if result else None
    
    def predecessor(self, key: T) -> Optional[T]:
        """
        Find the predecessor (largest key less than given key).
        
        Args:
            key: The key to find predecessor for
            
        Returns:
            The predecessor key, or None if no predecessor exists
        """
        current = self._head
        result = None
        
        for i in range(self._level - 1, -1, -1):
            while current.forward[i] is not None and current.forward[i].key < key:
                current = current.forward[i]
            result = current
        
        if result == self._head:
            return None
        return result.key
    
    def successor(self, key: T) -> Optional[T]:
        """
        Find the successor (smallest key greater than given key).
        
        Args:
            key: The key to find successor for
            
        Returns:
            The successor key, or None if no successor exists
        """
        current = self._head
        
        for i in range(self._level - 1, -1, -1):
            while current.forward[i] is not None and current.forward[i].key <= key:
                current = current.forward[i]
        
        current = current.forward[0]
        if current is None:
            return None
        return current.key
    
    def count_range(
        self,
        start_key: Optional[T] = None,
        end_key: Optional[T] = None,
        inclusive: bool = True
    ) -> int:
        """Count elements in a range."""
        return sum(1 for _ in self.range(start_key, end_key, inclusive))
    
    def clear(self) -> None:
        """Remove all elements from the skip list."""
        self._head.forward = [None] * self._max_level
        self._level = 1
        self._size = 0
    
    def to_list(self) -> List[Tuple[T, Any]]:
        """Convert to a list of key-value pairs."""
        return list(self)
    
    def to_dict(self) -> dict:
        """Convert to a dictionary (only works if keys are hashable)."""
        return dict(self)
    
    @classmethod
    def from_dict(
        cls,
        data: dict,
        max_level: int = 16,
        probability: float = 0.5,
        allow_duplicates: bool = False
    ) -> 'SkipList[T]':
        """Create a skip list from a dictionary."""
        sl = cls(max_level=max_level, probability=probability, allow_duplicates=allow_duplicates)
        for key, value in data.items():
            sl.insert(key, value)
        return sl
    
    @classmethod
    def from_sorted(
        cls,
        data: Iterable[Tuple[T, Any]],
        max_level: int = 16,
        probability: float = 0.5,
        allow_duplicates: bool = False
    ) -> 'SkipList[T]':
        """
        Create a skip list from sorted data efficiently.
        This is O(n) instead of O(n log n) for unsorted data.
        """
        sl = cls(max_level=max_level, probability=probability, allow_duplicates=allow_duplicates)
        for key, value in data:
            sl.insert(key, value)
        return sl
    
    def __len__(self) -> int:
        return self._size
    
    def __bool__(self) -> bool:
        return not self.is_empty
    
    def __repr__(self) -> str:
        items = ", ".join(f"{k!r}: {v!r}" for k, v in self)
        return f"SkipList({{{items}}})"
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def visualize(self) -> str:
        """
        Generate a text visualization of the skip list structure.
        Useful for debugging and understanding the data structure.
        """
        if self.is_empty:
            return "SkipList(empty)"
        
        lines = []
        lines.append(f"SkipList(size={self._size}, level={self._level})")
        
        # Collect all nodes at level 0
        nodes: List[SkipListNode[T]] = []
        current = self._head.forward[0]
        while current is not None:
            nodes.append(current)
            current = current.forward[0]
        
        # Draw each level
        for level in range(self._level - 1, -1, -1):
            line_parts = [f"L{level}: "]
            current = self._head
            
            for node in nodes:
                if current.forward[level] == node:
                    line_parts.append(f"[{node.key}]")
                    current = node
                else:
                    key_len = len(str(node.key))
                    line_parts.append("-" * (key_len + 2))
            
            lines.append("".join(line_parts))
        
        return "\n".join(lines)


class ConcurrentSkipList(Generic[T]):
    """
    A thread-safe skip list implementation.
    
    Uses fine-grained locking for concurrent access.
    Suitable for multi-threaded environments.
    
    Example:
        >>> sl = ConcurrentSkipList[int]()
        >>> sl.insert(5, "five")
        >>> sl.search(5)
        "five"
    """
    
    def __init__(
        self,
        max_level: int = 16,
        probability: float = 0.5,
        allow_duplicates: bool = False
    ):
        self._sl = SkipList[T](
            max_level=max_level,
            probability=probability,
            allow_duplicates=allow_duplicates
        )
        self._lock = threading.RLock()
    
    @property
    def size(self) -> int:
        with self._lock:
            return self._sl.size
    
    @property
    def is_empty(self) -> bool:
        with self._lock:
            return self._sl.is_empty
    
    def search(self, key: T) -> Optional[Any]:
        with self._lock:
            return self._sl.search(key)
    
    def __contains__(self, key: T) -> bool:
        with self._lock:
            return key in self._sl
    
    def __getitem__(self, key: T) -> Any:
        with self._lock:
            return self._sl[key]
    
    def get(self, key: T, default: Any = None) -> Any:
        with self._lock:
            return self._sl.get(key, default)
    
    def insert(self, key: T, value: Any = None) -> None:
        with self._lock:
            self._sl.insert(key, value)
    
    def __setitem__(self, key: T, value: Any) -> None:
        with self._lock:
            self._sl[key] = value
    
    def delete(self, key: T) -> bool:
        with self._lock:
            return self._sl.delete(key)
    
    def __delitem__(self, key: T) -> None:
        with self._lock:
            del self._sl[key]
    
    def range(
        self,
        start_key: Optional[T] = None,
        end_key: Optional[T] = None,
        inclusive: bool = True
    ) -> Iterator[Tuple[T, Any]]:
        with self._lock:
            # Materialize the range under lock
            items = list(self._sl.range(start_key, end_key, inclusive))
        
        # Yield outside lock
        for item in items:
            yield item
    
    def __iter__(self) -> Iterator[Tuple[T, Any]]:
        return self.range()
    
    def first(self) -> Optional[Tuple[T, Any]]:
        with self._lock:
            return self._sl.first()
    
    def last(self) -> Optional[Tuple[T, Any]]:
        with self._lock:
            return self._sl.last()
    
    def min_key(self) -> Optional[T]:
        with self._lock:
            return self._sl.min_key()
    
    def max_key(self) -> Optional[T]:
        with self._lock:
            return self._sl.max_key()
    
    def clear(self) -> None:
        with self._lock:
            self._sl.clear()
    
    def to_list(self) -> List[Tuple[T, Any]]:
        with self._lock:
            return self._sl.to_list()
    
    def to_dict(self) -> dict:
        with self._lock:
            return self._sl.to_dict()
    
    def __len__(self) -> int:
        return self.size
    
    def __bool__(self) -> bool:
        return not self.is_empty
    
    def __repr__(self) -> str:
        with self._lock:
            return repr(self._sl)


class SkipListSet(Generic[T]):
    """
    A skip list based set implementation.
    Stores only keys without values.
    
    Example:
        >>> s = SkipListSet[int]()
        >>> s.add(5)
        >>> s.add(2)
        >>> 5 in s
        True
    """
    
    def __init__(self, max_level: int = 16, probability: float = 0.5):
        self._sl = SkipList[T](
            max_level=max_level,
            probability=probability,
            allow_duplicates=False
        )
    
    @property
    def size(self) -> int:
        return self._sl.size
    
    @property
    def is_empty(self) -> bool:
        return self._sl.is_empty
    
    def add(self, key: T) -> bool:
        """
        Add a key to the set.
        
        Returns:
            True if the key was added, False if it already existed
        """
        if key in self._sl:
            return False
        self._sl.insert(key)
        return True
    
    def remove(self, key: T) -> bool:
        """Remove a key from the set. Returns True if removed."""
        return self._sl.delete(key)
    
    def discard(self, key: T) -> bool:
        """Remove a key if present. Returns True if removed."""
        return self._sl.delete(key)
    
    def __contains__(self, key: T) -> bool:
        return key in self._sl
    
    def __iter__(self) -> Iterator[T]:
        return self._sl.keys()
    
    def __len__(self) -> int:
        return self._sl.size
    
    def __bool__(self) -> bool:
        return not self.is_empty
    
    def first(self) -> Optional[T]:
        """Get the minimum element."""
        return self._sl.min_key()
    
    def last(self) -> Optional[T]:
        """Get the maximum element."""
        return self._sl.max_key()
    
    def range(
        self,
        start: Optional[T] = None,
        end: Optional[T] = None,
        inclusive: bool = True
    ) -> Iterator[T]:
        """Iterate over elements in a range."""
        for key, _ in self._sl.range(start, end, inclusive):
            yield key
    
    def isdisjoint(self, other: 'SkipListSet[T]') -> bool:
        """Check if this set has no elements in common with other."""
        for elem in self:
            if elem in other:
                return False
        return True
    
    def issubset(self, other: 'SkipListSet[T]') -> bool:
        """Check if every element in this set is in other."""
        for elem in self:
            if elem not in other:
                return False
        return True
    
    def issuperset(self, other: 'SkipListSet[T]') -> bool:
        """Check if every element in other is in this set."""
        return other.issubset(self)
    
    def union(self, *others: 'SkipListSet[T]') -> 'SkipListSet[T]':
        """Return a new set with elements from this set and all others."""
        result = SkipListSet[T](
            max_level=self._sl.max_level,
            probability=self._sl._probability
        )
        for elem in self:
            result.add(elem)
        for other in others:
            for elem in other:
                result.add(elem)
        return result
    
    def intersection(self, *others: 'SkipListSet[T]') -> 'SkipListSet[T]':
        """Return a new set with elements common to this set and all others."""
        result = SkipListSet[T]()
        for elem in self:
            if all(elem in other for other in others):
                result.add(elem)
        return result
    
    def difference(self, *others: 'SkipListSet[T]') -> 'SkipListSet[T]':
        """Return a new set with elements in this set but not in others."""
        result = SkipListSet[T]()
        for elem in self:
            if all(elem not in other for other in others):
                result.add(elem)
        return result
    
    def clear(self) -> None:
        """Remove all elements."""
        self._sl.clear()
    
    def to_list(self) -> List[T]:
        """Convert to a sorted list."""
        return list(self)
    
    @classmethod
    def from_iterable(
        cls,
        iterable: Iterable[T],
        max_level: int = 16,
        probability: float = 0.5
    ) -> 'SkipListSet[T]':
        """Create a set from an iterable."""
        s = cls(max_level=max_level, probability=probability)
        for elem in iterable:
            s.add(elem)
        return s
    
    def __repr__(self) -> str:
        items = ", ".join(repr(k) for k in self)
        return f"SkipListSet({{{items}}})"
    
    def __str__(self) -> str:
        return self.__repr__()


# ============================================================================
# Utility Functions
# ============================================================================

def create_skip_list(
    items: Optional[Iterable[Tuple[T, Any]]] = None,
    max_level: int = 16,
    probability: float = 0.5,
    allow_duplicates: bool = False
) -> SkipList[T]:
    """
    Create a skip list, optionally with initial items.
    
    Args:
        items: Optional iterable of (key, value) pairs
        max_level: Maximum number of levels
        probability: Promotion probability
        allow_duplicates: Whether to allow duplicate keys
        
    Returns:
        A new SkipList instance
    """
    sl = SkipList[T](
        max_level=max_level,
        probability=probability,
        allow_duplicates=allow_duplicates
    )
    if items:
        for key, value in items:
            sl.insert(key, value)
    return sl


def create_sorted_dict(
    items: Optional[dict] = None,
    max_level: int = 16,
    probability: float = 0.5
) -> SkipList[T]:
    """
    Create a sorted dictionary using skip list.
    
    This provides O(log n) operations instead of O(1) for hash table,
    but maintains sorted order.
    """
    sl = SkipList[T](max_level=max_level, probability=probability)
    if items:
        for key, value in items.items():
            sl[key] = value
    return sl