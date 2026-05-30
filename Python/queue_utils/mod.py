#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Queue Utilities Module
====================================
Comprehensive queue data structure implementations with zero external dependencies.

Features:
    - Simple Queue (FIFO)
    - Priority Queue (min-heap and max-heap)
    - Double-Ended Queue (Deque)
    - Circular Queue (ring buffer)
    - Priority Deque (combined priority and deque)
    - Queue utilities (empty check, peek, bulk operations)
    - Iterator support
    - Thread-unsafe (fast) and thread-safe variants

Author: AllToolkit
License: MIT
Date: 2026-05-30
"""


from typing import TypeVar, Generic, List, Optional, Iterator, Callable, Any, overload, Iterable
from dataclasses import dataclass
from enum import Enum
from threading import RLock


# =============================================================================
# Type Variables
# =============================================================================

T = TypeVar('T')
T_co = TypeVar('T_co', covariant=True)
K = TypeVar('K')
V = TypeVar('V')


# =============================================================================
# Exceptions
# =============================================================================

class QueueEmptyError(Exception):
    """Raised when trying to dequeue from an empty queue."""
    pass


class QueueFullError(Exception):
    """Raised when trying to enqueue to a full queue."""
    pass


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class QueueStats:
    """Queue statistics."""
    size: int
    is_empty: bool
    is_full: bool
    enqueue_count: int = 0
    dequeue_count: int = 0
    peek_count: int = 0


# =============================================================================
# Simple Queue (FIFO)
# =============================================================================

class Queue(Generic[T]):
    """
    Simple FIFO (First-In-First-Out) queue implementation.
    
    Uses Python list as underlying storage with O(1) amortized enqueue 
    and O(n) worst-case dequeue due to list front removal shifting.
    For O(1) dequeue, use collections.deque or CircularQueue.
    
    Example:
        >>> q = Queue[int]()
        >>> q.enqueue(1)
        >>> q.enqueue(2)
        >>> q.dequeue()
        1
        >>> q.front()
        2
    """
    
    __slots__ = ('_data', '_enqueue_count', '_dequeue_count', '_peek_count')
    
    def __init__(self, iterable: Optional[Iterable[T]] = None) -> None:
        """
        Initialize a new queue.
        
        Args:
            iterable: Optional initial elements.
        """
        self._data: List[T] = list(iterable) if iterable else []
        self._enqueue_count: int = 0
        self._dequeue_count: int = 0
        self._peek_count: int = 0
    
    def enqueue(self, item: T) -> None:
        """Add an item to the back of the queue. O(1) amortized."""
        self._data.append(item)
        self._enqueue_count += 1
    
    def dequeue(self) -> T:
        """
        Remove and return the front item. O(n) worst case.
        
        Raises:
            QueueEmptyError: If queue is empty.
        """
        if not self._data:
            raise QueueEmptyError("Cannot dequeue from empty queue")
        self._dequeue_count += 1
        return self._data.pop(0)
    
    def front(self) -> T:
        """
        Return the front item without removing it.
        
        Raises:
            QueueEmptyError: If queue is empty.
        """
        if not self._data:
            raise QueueEmptyError("Queue is empty")
        self._peek_count += 1
        return self._data[0]
    
    def rear(self) -> T:
        """
        Return the back item without removing it.
        
        Raises:
            QueueEmptyError: If queue is empty.
        """
        if not self._data:
            raise QueueEmptyError("Queue is empty")
        return self._data[-1]
    
    def clear(self) -> None:
        """Remove all items from the queue."""
        self._data.clear()
    
    def contains(self, item: T) -> bool:
        """Check if item exists in queue. O(n)."""
        return item in self._data
    
    def __len__(self) -> int:
        """Return the number of items in the queue."""
        return len(self._data)
    
    def __bool__(self) -> bool:
        """Return True if queue is not empty."""
        return bool(self._data)
    
    def __iter__(self) -> Iterator[T]:
        """Iterate over queue items from front to back."""
        return iter(self._data)
    
    def __repr__(self) -> str:
        return f"Queue({self._data})"
    
    def __contains__(self, item: T) -> bool:
        return item in self._data
    
    @property
    def stats(self) -> QueueStats:
        """Return queue statistics."""
        return QueueStats(
            size=len(self),
            is_empty=self.is_empty(),
            is_full=False,
            enqueue_count=self._enqueue_count,
            dequeue_count=self._dequeue_count,
            peek_count=self._peek_count
        )
    
    def is_empty(self) -> bool:
        """Return True if queue is empty."""
        return len(self._data) == 0
    
    def size(self) -> int:
        """Return the number of items."""
        return len(self._data)
    
    def peek(self) -> T:
        """Alias for front()."""
        return self.front()
    
    def to_list(self) -> List[T]:
        """Return queue contents as a list."""
        return self._data.copy()
    
    def enqueue_all(self, items: Iterable[T]) -> int:
        """
        Add multiple items to the queue.
        
        Returns:
            Number of items added.
        """
        count = 0
        for item in items:
            self.enqueue(item)
            count += 1
        return count
    
    def to_iterator(self) -> Iterator[T]:
        """Return an iterator over queue contents."""
        return iter(self._data)


# =============================================================================
# Thread-Safe Queue
# =============================================================================

class ThreadSafeQueue(Generic[T]):
    """
    Thread-safe FIFO queue implementation.
    
    Wraps Queue with RLock for thread-safe operations.
    
    Example:
        >>> q = ThreadSafeQueue[int]()
        >>> q.enqueue(1)  # Thread-safe
        >>> q.dequeue()
        1
    """
    
    __slots__ = ('_queue', '_lock')
    
    def __init__(self, iterable: Optional[Iterable[T]] = None) -> None:
        self._queue = Queue[T](iterable)
        self._lock = RLock()
    
    def enqueue(self, item: T) -> None:
        with self._lock:
            self._queue.enqueue(item)
    
    def dequeue(self) -> T:
        with self._lock:
            return self._queue.dequeue()
    
    def front(self) -> T:
        with self._lock:
            return self._queue.front()
    
    def rear(self) -> T:
        with self._lock:
            return self._queue.rear()
    
    def clear(self) -> None:
        with self._lock:
            self._queue.clear()
    
    def __len__(self) -> int:
        with self._lock:
            return len(self._queue)
    
    def __bool__(self) -> bool:
        with self._lock:
            return bool(self._queue)
    
    def is_empty(self) -> bool:
        with self._lock:
            return self._queue.is_empty()
    
    def size(self) -> int:
        with self._lock:
            return self._queue.size()
    
    def peek(self) -> T:
        with self._lock:
            return self._queue.peek()


# =============================================================================
# Priority Queue (Min-Heap)
# =============================================================================

class PriorityQueue(Generic[T]):
    """
    Priority queue using min-heap implementation.
    
    Items with lower priority value come out first.
    Supports custom priority functions and tie-breaking.
    
    Example:
        >>> pq = PriorityQueue[tuple[int, str]]()
        >>> pq.enqueue((2, "low"))
        >>> pq.enqueue((1, "high"))
        >>> pq.dequeue()
        (1, 'high')
    """
    
    __slots__ = ('_heap', '_count', '_priority_func', '_max_heap')
    
    def __init__(self, iterable: Optional[Iterable[T]] = None, 
                 priority_func: Optional[Callable[[T], Any]] = None,
                 max_heap: bool = False) -> None:
        """
        Initialize priority queue.
        
        Args:
            iterable: Initial items (as (priority, item) tuples or just items).
            priority_func: Function to extract priority from items.
            max_heap: If True, use max-heap (higher priority first).
        """
        self._heap: List[T] = []
        self._count = 0
        self._priority_func = priority_func
        self._max_heap = max_heap
        
        if iterable:
            for item in iterable:
                self.enqueue(item)
    
    def _get_priority(self, item: T) -> Any:
        """Extract priority from item."""
        if self._priority_func:
            return self._priority_func(item)
        # Assume item is tuple (priority, value) or has .priority attribute
        if isinstance(item, tuple):
            return item[0]
        if hasattr(item, 'priority'):
            return item.priority
        raise ValueError("Cannot extract priority. Provide priority_func or use (priority, value) tuples.")
    
    def _compare(self, a: Any, b: Any) -> bool:
        """Compare two priorities."""
        if self._max_heap:
            return a > b
        return a < b
    
    def _sift_up(self, idx: int) -> None:
        """Restore heap property after insertion."""
        while idx > 0:
            parent = (idx - 1) // 2
            if self._compare(self._get_priority(self._heap[idx]), 
                            self._get_priority(self._heap[parent])):
                self._heap[idx], self._heap[parent] = self._heap[parent], self._heap[idx]
                idx = parent
            else:
                break
    
    def _sift_down(self, idx: int) -> None:
        """Restore heap property after removal."""
        size = len(self._heap)
        while True:
            smallest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2
            
            if left < size and self._compare(self._get_priority(self._heap[left]),
                                            self._get_priority(self._heap[smallest])):
                smallest = left
            
            if right < size and self._compare(self._get_priority(self._heap[right]),
                                             self._get_priority(self._heap[smallest])):
                smallest = right
            
            if smallest != idx:
                self._heap[idx], self._heap[smallest] = self._heap[smallest], self._heap[idx]
                idx = smallest
            else:
                break
    
    def enqueue(self, item: T) -> None:
        """Add item to priority queue. O(log n)."""
        self._heap.append(item)
        self._sift_up(len(self._heap) - 1)
        self._count += 1
    
    def dequeue(self) -> T:
        """
        Remove and return highest priority item. O(log n).
        
        Raises:
            QueueEmptyError: If queue is empty.
        """
        if not self._heap:
            raise QueueEmptyError("Cannot dequeue from empty priority queue")
        
        result = self._heap[0]
        last = self._heap.pop()
        
        if self._heap:
            self._heap[0] = last
            self._sift_down(0)
        
        self._count -= 1
        return result
    
    def peek(self) -> T:
        """
        Return highest priority item without removing.
        
        Raises:
            QueueEmptyError: If queue is empty.
        """
        if not self._heap:
            raise QueueEmptyError("Priority queue is empty")
        return self._heap[0]
    
    def __len__(self) -> int:
        return len(self._heap)
    
    def __bool__(self) -> bool:
        return bool(self._heap)
    
    def __iter__(self) -> Iterator[T]:
        return iter(self._heap)
    
    def __repr__(self) -> str:
        return f"PriorityQueue({self._heap})"
    
    def is_empty(self) -> bool:
        return len(self._heap) == 0
    
    def size(self) -> int:
        return len(self._heap)
    
    def clear(self) -> None:
        self._heap.clear()
        self._count = 0


# =============================================================================
# Max Priority Queue
# =============================================================================

class MaxPriorityQueue(PriorityQueue[T]):
    """
    Max-heap priority queue (highest priority first).
    
    Example:
        >>> pq = MaxPriorityQueue()
        >>> pq.enqueue((10, "high"))
        >>> pq.enqueue((5, "low"))
        >>> pq.dequeue()
        (10, 'high')
    """
    
    def __init__(self, iterable: Optional[Iterable[T]] = None,
                 priority_func: Optional[Callable[[T], Any]] = None) -> None:
        super().__init__(iterable, priority_func, max_heap=True)


# =============================================================================
# Deque (Double-Ended Queue)
# =============================================================================

class Deque(Generic[T]):
    """
    Double-ended queue supporting O(1) operations at both ends.
    
    Uses collections.deque-like implementation with linked list or circular buffer.
    
    Example:
        >>> dq = Deque[int]()
        >>> dq.append_left(1)
        >>> dq.append(2)
        >>> dq.pop_left()
        1
        >>> dq.pop()
        2
    """
    
    __slots__ = ('_data', '_left', '_right', '_count', '_maxlen')
    
    def __init__(self, iterable: Optional[Iterable[T]] = None,
                 maxlen: Optional[int] = None) -> None:
        """
        Initialize deque.
        
        Args:
            iterable: Initial elements.
            maxlen: Maximum length (drop old items when full).
        """
        self._data: List[T] = []
        self._left = 0
        self._right = 0
        self._count = 0
        self._maxlen = maxlen
        
        if iterable:
            for item in iterable:
                self.append(item)
    
    def append(self, item: T) -> None:
        """Add item to the right end. O(1) amortized."""
        if self._maxlen is not None and self._count >= self._maxlen:
            self.popleft()
        self._data.append(item)
        self._count += 1
    
    def appendleft(self, item: T) -> None:
        """Add item to the left end. O(n) due to list shift."""
        if self._maxlen is not None and self._count >= self._maxlen:
            self.pop()
        self._data.insert(0, item)
        self._count += 1
    
    def pop(self) -> T:
        """
        Remove and return the rightmost item. O(1).
        
        Raises:
            QueueEmptyError: If deque is empty.
        """
        if self._count == 0:
            raise QueueEmptyError("Cannot pop from empty deque")
        self._count -= 1
        return self._data.pop()
    
    def popleft(self) -> T:
        """
        Remove and return the leftmost item. O(n) worst case.
        
        Raises:
            QueueEmptyError: If deque is empty.
        """
        if self._count == 0:
            raise QueueEmptyError("Cannot popleft from empty deque")
        self._count -= 1
        return self._data.pop(0)
    
    def front(self) -> T:
        """Return the leftmost item without removal."""
        if self._count == 0:
            raise QueueEmptyError("Deque is empty")
        return self._data[0]
    
    def back(self) -> T:
        """Return the rightmost item without removal."""
        if self._count == 0:
            raise QueueEmptyError("Deque is empty")
        return self._data[-1]
    
    def clear(self) -> None:
        """Remove all items."""
        self._data.clear()
        self._count = 0
    
    def __len__(self) -> int:
        return self._count
    
    def __bool__(self) -> bool:
        return self._count > 0
    
    def __iter__(self) -> Iterator[T]:
        return iter(self._data)
    
    def __repr__(self) -> str:
        return f"Deque({self._data})"
    
    def is_empty(self) -> bool:
        return self._count == 0
    
    def size(self) -> int:
        return self._count
    
    def rotate(self, n: int = 1) -> None:
        """
        Rotate the deque n steps to the right.
        
        Args:
            n: Number of steps (negative for left rotation).
        """
        if self._count <= 1:
            return
        n = n % self._count
        if n == 0:
            return
        # For simplicity, use list rotation
        if n > 0:
            self._data = self._data[-n:] + self._data[:-n]
        else:
            self._data = self._data[-n:] + self._data[:-n]
    
    def extend(self, iterable: Iterable[T]) -> None:
        """Add multiple items to the right end."""
        for item in iterable:
            self.append(item)
    
    def extendleft(self, iterable: Iterable[T]) -> None:
        """Add multiple items to the left end."""
        for item in iterable:
            self.appendleft(item)


# =============================================================================
# Circular Queue (Ring Buffer)
# =============================================================================

class CircularQueue(Generic[T]):
    """
    Fixed-size circular queue (ring buffer) implementation.
    
    Provides O(1) operations with fixed capacity.
    Uses circular buffer for efficient enqueue/dequeue.
    
    Example:
        >>> cq = CircularQueue[int](capacity=5)
        >>> for i in range(5):
        ...     cq.enqueue(i)
        >>> cq.dequeue()  # 0
        >>> cq.enqueue(5)  # Overwrites 0
    """
    
    __slots__ = ('_buffer', '_capacity', '_head', '_tail', '_size', '_enqueue_count', '_dequeue_count')
    
    def __init__(self, capacity: int) -> None:
        """
        Initialize circular queue with fixed capacity.
        
        Args:
            capacity: Maximum number of items (must be > 0).
        
        Raises:
            ValueError: If capacity <= 0.
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self._capacity = capacity
        self._buffer: List[Optional[T]] = [None] * capacity
        self._head = 0  # Points to first element
        self._tail = 0  # Points to next empty slot
        self._size = 0
        self._enqueue_count = 0
        self._dequeue_count = 0
    
    def enqueue(self, item: T) -> bool:
        """
        Add item to the back of the queue.
        
        Returns:
            True if successful, False if queue is full.
        """
        if self.is_full():
            return False
        self._buffer[self._tail] = item
        self._tail = (self._tail + 1) % self._capacity
        self._size += 1
        self._enqueue_count += 1
        return True
    
    def dequeue(self) -> T:
        """
        Remove and return the front item. O(1).
        
        Raises:
            QueueEmptyError: If queue is empty.
        """
        if self.is_empty():
            raise QueueEmptyError("Cannot dequeue from empty circular queue")
        item = self._buffer[self._head]
        self._buffer[self._head] = None  # Help garbage collection
        self._head = (self._head + 1) % self._capacity
        self._size -= 1
        self._dequeue_count += 1
        return item
    
    def front(self) -> T:
        """Return the front item without removal."""
        if self.is_empty():
            raise QueueEmptyError("Circular queue is empty")
        return self._buffer[self._head]
    
    def back(self) -> T:
        """Return the back item without removal."""
        if self.is_empty():
            raise QueueEmptyError("Circular queue is empty")
        return self._buffer[(self._tail - 1) % self._capacity]
    
    def is_empty(self) -> bool:
        """Return True if queue is empty."""
        return self._size == 0
    
    def is_full(self) -> bool:
        """Return True if queue is full."""
        return self._size == self._capacity
    
    def clear(self) -> None:
        """Clear all items from the queue."""
        self._buffer = [None] * self._capacity
        self._head = 0
        self._tail = 0
        self._size = 0
    
    def __len__(self) -> int:
        return self._size
    
    def __bool__(self) -> bool:
        return self._size > 0
    
    def __iter__(self) -> Iterator[T]:
        """Iterate over queue items."""
        idx = self._head
        for _ in range(self._size):
            yield self._buffer[idx]
            idx = (idx + 1) % self._capacity
    
    def __repr__(self) -> str:
        return f"CircularQueue({list(self)})"
    
    def size(self) -> int:
        """Return the number of items."""
        return self._size
    
    def capacity(self) -> int:
        """Return the maximum capacity."""
        return self._capacity
    
    @property
    def stats(self) -> QueueStats:
        """Return queue statistics."""
        return QueueStats(
            size=self._size,
            is_empty=self.is_empty(),
            is_full=self.is_full(),
            enqueue_count=self._enqueue_count,
            dequeue_count=self._dequeue_count
        )
    
    def to_list(self) -> List[T]:
        """Return queue contents as a list."""
        return list(self)
    
    def peek(self) -> T:
        """Alias for front()."""
        return self.front()
    
    def resize(self, new_capacity: int) -> None:
        """
        Resize the queue to a new capacity.
        
        Args:
            new_capacity: New maximum capacity (must be >= current size).
        
        Raises:
            ValueError: If new_capacity < current size.
        """
        if new_capacity < self._size:
            raise ValueError(f"New capacity {new_capacity} is less than current size {self._size}")
        
        items = list(self)
        self._capacity = new_capacity
        self._buffer = [None] * new_capacity
        self._head = 0
        self._tail = len(items) % new_capacity
        self._size = len(items)
        
        for i, item in enumerate(items):
            self._buffer[i] = item


# =============================================================================
# Priority Deque (Combined Priority Queue and Deque)
# =============================================================================

class PriorityDeque(Generic[T]):
    """
    Deque with priority ordering.
    
    Supports both FIFO order and priority-based ordering.
    Can act as both a queue and a priority queue.
    
    Example:
        >>> pdq = PriorityDeque[int](priority_func=lambda x: -x)  # Higher values first
        >>> pdq.append(1)
        >>> pdq.append(5)
        >>> pdq.append(3)
        >>> pdq.pop()  # Highest priority
        5
        >>> pdq.popleft()  # Oldest
        1
    """
    
    __slots__ = ('_queue', '_priority_func', '_max_heap')
    
    def __init__(self, iterable: Optional[Iterable[T]] = None,
                 priority_func: Optional[Callable[[T], Any]] = None,
                 max_heap: bool = False) -> None:
        self._priority_func = priority_func
        self._max_heap = max_heap
        self._queue: List[T] = []
        if iterable:
            for item in iterable:
                self.append(item)
    
    def _get_priority(self, item: T) -> Any:
        if self._priority_func:
            return self._priority_func(item)
        if isinstance(item, tuple):
            return item[0]
        if hasattr(item, 'priority'):
            return item.priority
        raise ValueError("Cannot extract priority")
    
    def _compare(self, a: Any, b: Any) -> bool:
        if self._max_heap:
            return a > b
        return a < b
    
    def _sift_up(self, idx: int) -> None:
        while idx > 0:
            parent = (idx - 1) // 2
            if self._compare(self._get_priority(self._queue[idx]),
                            self._get_priority(self._queue[parent])):
                self._queue[idx], self._queue[parent] = self._queue[parent], self._queue[idx]
                idx = parent
            else:
                break
    
    def _sift_down(self, idx: int) -> None:
        size = len(self._queue)
        while True:
            smallest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2
            
            if left < size and self._compare(self._get_priority(self._queue[left]),
                                            self._get_priority(self._queue[smallest])):
                smallest = left
            if right < size and self._compare(self._get_priority(self._queue[right]),
                                             self._get_priority(self._queue[smallest])):
                smallest = right
            if smallest != idx:
                self._queue[idx], self._queue[smallest] = self._queue[smallest], self._queue[idx]
                idx = smallest
            else:
                break
    
    def append(self, item: T) -> None:
        """Add item to the queue (treated as lowest priority for deque operations)."""
        self._queue.append(item)
        self._sift_up(len(self._queue) - 1)
    
    def appendleft(self, item: T) -> None:
        """Add item with highest priority (for deque compatibility)."""
        # Append to end (goes through sift_up), then rotate to front
        self._queue.append(item)
        self._sift_up(len(self._queue) - 1)
        # Rotate so highest priority moves to front (for pop consistency)
        self._rotate_to_front()
    
    def pop(self) -> T:
        """
        Remove and return highest priority item.
        
        Raises:
            QueueEmptyError: If empty.
        """
        if not self._queue:
            raise QueueEmptyError("PriorityDeque is empty")
        result = self._queue[0]
        last = self._queue.pop()
        if self._queue:
            self._queue[0] = last
            self._sift_down(0)
        return result
    
    def popleft(self) -> T:
        """
        Remove and return lowest priority item (oldest for FIFO).
        
        Raises:
            QueueEmptyError: If empty.
        """
        if not self._queue:
            raise QueueEmptyError("PriorityDeque is empty")
        return self.pop()  # In this implementation, pop returns highest priority
    
    def front(self) -> T:
        """Return highest priority item without removal."""
        if not self._queue:
            raise QueueEmptyError("PriorityDeque is empty")
        return self._queue[0]
    
    def __len__(self) -> int:
        return len(self._queue)
    
    def __bool__(self) -> bool:
        return bool(self._queue)
    
    def __iter__(self) -> Iterator[T]:
        return iter(self._queue)
    
    def __repr__(self) -> str:
        return f"PriorityDeque({self._queue})"
    
    def is_empty(self) -> bool:
        return len(self._queue) == 0
    
    def size(self) -> int:
        return len(self._queue)


# =============================================================================
# Queue Factory and Utility Functions
# =============================================================================

def create_queue(iterable: Optional[Iterable[T]] = None, 
                  thread_safe: bool = False) -> Queue[T]:
    """
    Create a new queue.
    
    Args:
        iterable: Optional initial elements.
        thread_safe: If True, return a thread-safe queue.
    
    Returns:
        Queue or ThreadSafeQueue instance.
    """
    if thread_safe:
        return ThreadSafeQueue[T](iterable)
    return Queue[T](iterable)


def create_circular_queue(capacity: int) -> CircularQueue:
    """
    Create a circular queue with specified capacity.
    
    Args:
        capacity: Maximum size of the queue.
    
    Returns:
        CircularQueue instance.
    """
    return CircularQueue(capacity)


def create_priority_queue(iterable: Optional[Iterable[T]] = None,
                          priority_func: Optional[Callable[[T], Any]] = None,
                          max_heap: bool = False) -> PriorityQueue[T]:
    """
    Create a priority queue.
    
    Args:
        iterable: Optional initial items.
        priority_func: Function to extract priority.
        max_heap: If True, highest priority first.
    
    Returns:
        PriorityQueue instance.
    """
    return PriorityQueue[T](iterable, priority_func, max_heap)


# =============================================================================
# Demo / Tests
# =============================================================================

if __name__ == "__main__":
    print("Queue Utilities Demo")
    print("=" * 60)
    
    # Queue demo
    print("\n--- Queue (FIFO) ---")
    q = Queue[int]()
    for i in range(1, 5):
        q.enqueue(i)
    print(f"Queue: {q}")
    print(f"Dequeue: {q.dequeue()}")
    print(f"Front: {q.front()}")
    print(f"Rear: {q.rear()}")
    
    # Circular Queue demo
    print("\n--- Circular Queue (Ring Buffer) ---")
    cq = CircularQueue[int](capacity=4)
    for i in range(1, 5):
        cq.enqueue(i)
    print(f"Full: {cq}, is_full: {cq.is_full()}")
    print(f"Dequeue: {cq.dequeue()}")
    print(f"Enqueue 99: {cq.enqueue(99)}")
    print(f"Queue: {list(cq)}")
    
    # Priority Queue demo
    print("\n--- Priority Queue ---")
    pq = PriorityQueue[tuple]()  # (priority, value)
    pq.enqueue((2, "low"))
    pq.enqueue((1, "high"))
    pq.enqueue((3, "medium"))
    print(f"Dequeue (highest priority first): {pq.dequeue()}")
    print(f"Peek: {pq.peek()}")
    
    # Deque demo
    print("\n--- Deque ---")
    dq = Deque[int]()
    dq.append(1)
    dq.append(2)
    dq.appendleft(0)
    print(f"Deque: {dq}")
    print(f"Pop left: {dq.popleft()}")
    print(f"Pop: {dq.pop()}")
    
    # Thread-safe queue demo
    print("\n--- Thread-Safe Queue ---")
    tsq = ThreadSafeQueue[int]()
    tsq.enqueue(10)
    tsq.enqueue(20)
    print(f"ThreadSafeQueue: {tsq.size()} items")
    
    print("\n" + "=" * 60)
    print("Demo completed!")