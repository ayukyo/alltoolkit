#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Queue Utilities Test Module
=========================================
Comprehensive tests for queue data structure implementations.

Author: AllToolkit
License: MIT
Date: 2026-05-30
"""

import pytest
from mod import (
    Queue, ThreadSafeQueue, PriorityQueue, MaxPriorityQueue,
    Deque, CircularQueue, PriorityDeque,
    QueueEmptyError, QueueFullError,
    create_queue, create_circular_queue, create_priority_queue
)


class TestQueue:
    """Tests for basic FIFO Queue."""
    
    def test_empty_queue(self):
        """Test empty queue operations."""
        q = Queue[int]()
        assert len(q) == 0
        assert q.is_empty()
        assert q.size() == 0
    
    def test_enqueue_dequeue(self):
        """Test basic enqueue/dequeue."""
        q = Queue[int]()
        q.enqueue(1)
        q.enqueue(2)
        assert len(q) == 2
        assert q.dequeue() == 1
        assert q.dequeue() == 2
    
    def test_front_rear(self):
        """Test front and rear peek."""
        q = Queue[int]()
        q.enqueue(1)
        q.enqueue(2)
        assert q.front() == 1
        assert q.rear() == 2
    
    def test_front_empty_error(self):
        """Test front on empty queue raises error."""
        q = Queue[int]()
        with pytest.raises(QueueEmptyError):
            q.front()
    
    def test_dequeue_empty_error(self):
        """Test dequeue on empty queue raises error."""
        q = Queue[int]()
        with pytest.raises(QueueEmptyError):
            q.dequeue()
    
    def test_init_from_iterable(self):
        """Test initialization from iterable."""
        q = Queue([1, 2, 3])
        assert q.dequeue() == 1
        assert q.dequeue() == 2
        assert q.dequeue() == 3
    
    def test_clear(self):
        """Test clear operation."""
        q = Queue([1, 2, 3])
        q.clear()
        assert len(q) == 0
        assert q.is_empty()
    
    def test_contains(self):
        """Test contains check."""
        q = Queue([1, 2, 3])
        assert 2 in q
        assert 99 not in q
    
    def test_to_list(self):
        """Test to_list conversion."""
        q = Queue([1, 2, 3])
        assert q.to_list() == [1, 2, 3]
    
    def test_enqueue_all(self):
        """Test bulk enqueue."""
        q = Queue[int]()
        count = q.enqueue_all([1, 2, 3])
        assert count == 3
        assert len(q) == 3
    
    def test_iteration(self):
        """Test iteration over queue."""
        q = Queue([1, 2, 3])
        items = list(q)
        assert items == [1, 2, 3]
    
    def test_repr(self):
        """Test string representation."""
        q = Queue([1, 2, 3])
        assert "Queue" in repr(q)
        assert "[1, 2, 3]" in repr(q)
    
    def test_stats(self):
        """Test queue statistics."""
        q = Queue[int]()
        q.enqueue(1)
        q.enqueue(2)
        q.dequeue()
        q.front()
        
        stats = q.stats
        assert stats.size == 1
        assert stats.is_empty is False
        assert stats.enqueue_count == 2
        assert stats.dequeue_count == 1
        assert stats.peek_count == 1


class TestThreadSafeQueue:
    """Tests for Thread-Safe Queue."""
    
    def test_basic_operations(self):
        """Test basic thread-safe operations."""
        q = ThreadSafeQueue[int]()
        q.enqueue(1)
        q.enqueue(2)
        assert q.dequeue() == 1
        assert q.size() == 1
    
    def test_init_from_iterable(self):
        """Test initialization from iterable."""
        q = ThreadSafeQueue([1, 2, 3])
        assert len(q) == 3
        assert q.dequeue() == 1
    
    def test_is_empty(self):
        """Test empty check."""
        q = ThreadSafeQueue[int]()
        assert q.is_empty()
        q.enqueue(1)
        assert not q.is_empty()


class TestPriorityQueue:
    """Tests for Priority Queue."""
    
    def test_empty_priority_queue(self):
        """Test empty priority queue."""
        pq = PriorityQueue[tuple]()
        assert len(pq) == 0
        assert pq.is_empty()
    
    def test_enqueue_dequeue(self):
        """Test priority queue ordering."""
        pq = PriorityQueue[tuple]()  # (priority, value)
        pq.enqueue((2, "low"))
        pq.enqueue((1, "high"))
        pq.enqueue((3, "medium"))
        
        assert pq.dequeue() == (1, "high")
        assert pq.dequeue() == (2, "low")
        assert pq.dequeue() == (3, "medium")
    
    def test_peek(self):
        """Test peek without removal."""
        pq = PriorityQueue[tuple]()
        pq.enqueue((5, "five"))
        pq.enqueue((1, "one"))
        
        assert pq.peek() == (1, "one")
        assert len(pq) == 2  # Still has both items
    
    def test_priority_function(self):
        """Test custom priority function."""
        pq = PriorityQueue[str](priority_func=lambda s: -len(s))  # Longer strings first
        pq.enqueue("a")
        pq.enqueue("abc")
        pq.enqueue("ab")
        
        assert pq.dequeue() == "abc"
        assert pq.dequeue() == "ab"
        assert pq.dequeue() == "a"
    
    def test_clear(self):
        """Test clear operation."""
        pq = PriorityQueue[tuple]()
        pq.enqueue((1, "a"))
        pq.enqueue((2, "b"))
        pq.clear()
        assert len(pq) == 0
    
    def test_iteration(self):
        """Test iteration (no guaranteed order)."""
        pq = PriorityQueue[tuple]()
        for i, v in enumerate([5, 3, 1, 4, 2]):
            pq.enqueue((v, i))
        items = list(pq)
        assert len(items) == 5


class TestMaxPriorityQueue:
    """Tests for Max Priority Queue."""
    
    def test_max_heap_ordering(self):
        """Test that highest priority comes first."""
        pq = MaxPriorityQueue[tuple]()
        pq.enqueue((10, "high"))
        pq.enqueue((5, "low"))
        pq.enqueue((15, "highest"))
        
        assert pq.dequeue() == (15, "highest")
        assert pq.dequeue() == (10, "high")
        assert pq.dequeue() == (5, "low")


class TestDeque:
    """Tests for Double-Ended Queue."""
    
    def test_empty_deque(self):
        """Test empty deque."""
        dq = Deque[int]()
        assert len(dq) == 0
        assert dq.is_empty()
    
    def test_append_pop(self):
        """Test append and pop."""
        dq = Deque[int]()
        dq.append(1)
        dq.append(2)
        assert dq.pop() == 2
        assert dq.pop() == 1
    
    def test_appendleft_popleft(self):
        """Test appendleft and popleft."""
        dq = Deque[int]()
        dq.appendleft(1)
        dq.appendleft(2)
        assert dq.popleft() == 2
        assert dq.popleft() == 1
    
    def test_front_back(self):
        """Test front and back."""
        dq = Deque[int]()
        dq.append(1)
        dq.append(2)
        assert dq.front() == 1
        assert dq.back() == 2
    
    def test_mixed_operations(self):
        """Test mixed queue operations."""
        dq = Deque[int]()
        dq.append(1)
        dq.appendleft(0)
        dq.append(2)
        assert list(dq) == [0, 1, 2]
        assert dq.pop() == 2
        assert dq.popleft() == 0
        assert list(dq) == [1]
    
    def test_rotate(self):
        """Test rotate operation."""
        dq = Deque[int]()
        for i in range(1, 5):
            dq.append(i)
        dq.rotate(1)
        assert list(dq) == [4, 1, 2, 3]
    
    def test_rotate_negative(self):
        """Test rotate with negative steps."""
        dq = Deque[int]()
        for i in range(1, 5):
            dq.append(i)
        dq.rotate(-1)
        assert list(dq) == [2, 3, 4, 1]
    
    def test_maxlen(self):
        """Test maxlen parameter."""
        dq = Deque[int](maxlen=3)
        dq.append(1)
        dq.append(2)
        dq.append(3)
        dq.append(4)  # Should drop 1
        assert list(dq) == [2, 3, 4]
    
    def test_extend(self):
        """Test extend operation."""
        dq = Deque[int]()
        dq.append(1)
        dq.extend([2, 3])
        assert list(dq) == [1, 2, 3]


class TestCircularQueue:
    """Tests for Circular Queue (Ring Buffer)."""
    
    def test_empty_circular_queue(self):
        """Test empty circular queue."""
        cq = CircularQueue[int](capacity=5)
        assert len(cq) == 0
        assert cq.is_empty()
        assert not cq.is_full()
    
    def test_enqueue_dequeue(self):
        """Test basic circular queue operations."""
        cq = CircularQueue[int](capacity=3)
        assert cq.enqueue(1) is True
        assert cq.enqueue(2) is True
        assert cq.dequeue() == 1
        assert cq.dequeue() == 2
    
    def test_wrap_around(self):
        """Test circular wrap-around."""
        cq = CircularQueue[int](capacity=3)
        for i in range(3):
            cq.enqueue(i + 1)
        assert cq.is_full()
        
        assert cq.dequeue() == 1
        assert cq.dequeue() == 2
        
        # Add more after wrap
        assert cq.enqueue(4) is True
        assert cq.dequeue() == 3
        assert cq.dequeue() == 4
    
    def test_full_reject(self):
        """Test that full queue rejects new items."""
        cq = CircularQueue[int](capacity=2)
        cq.enqueue(1)
        cq.enqueue(2)
        assert cq.is_full()
        assert cq.enqueue(3) is False
    
    def test_front_back(self):
        """Test front and back peek."""
        cq = CircularQueue[int](capacity=5)
        cq.enqueue(1)
        cq.enqueue(2)
        cq.enqueue(3)
        assert cq.front() == 1
        assert cq.back() == 3
    
    def test_front_empty_error(self):
        """Test front on empty queue raises error."""
        cq = CircularQueue[int](capacity=5)
        with pytest.raises(QueueEmptyError):
            cq.front()
    
    def test_dequeue_empty_error(self):
        """Test dequeue on empty queue raises error."""
        cq = CircularQueue[int](capacity=5)
        with pytest.raises(QueueEmptyError):
            cq.dequeue()
    
    def test_clear(self):
        """Test clear operation."""
        cq = CircularQueue[int](capacity=5)
        cq.enqueue(1)
        cq.enqueue(2)
        cq.clear()
        assert len(cq) == 0
        assert cq.is_empty()
    
    def test_capacity(self):
        """Test capacity method."""
        cq = CircularQueue[int](capacity=10)
        assert cq.capacity() == 10
    
    def test_resize(self):
        """Test resize operation."""
        cq = CircularQueue[int](capacity=3)
        cq.enqueue(1)
        cq.enqueue(2)
        cq.enqueue(3)
        
        cq.resize(5)
        assert cq.capacity() == 5
        assert cq.size() == 3
        
        cq.enqueue(4)
        cq.enqueue(5)
        assert list(cq) == [1, 2, 3, 4, 5]
    
    def test_resize_too_small(self):
        """Test resize to smaller capacity raises error."""
        cq = CircularQueue[int](capacity=3)
        cq.enqueue(1)
        cq.enqueue(2)
        
        with pytest.raises(ValueError):
            cq.resize(1)
    
    def test_iteration(self):
        """Test iteration."""
        cq = CircularQueue[int](capacity=5)
        for i in range(1, 4):
            cq.enqueue(i)
        items = list(cq)
        assert items == [1, 2, 3]
    
    def test_to_list(self):
        """Test to_list conversion."""
        cq = CircularQueue[int](capacity=5)
        cq.enqueue(1)
        cq.enqueue(2)
        assert cq.to_list() == [1, 2]
    
    def test_stats(self):
        """Test queue statistics."""
        cq = CircularQueue[int](capacity=5)
        cq.enqueue(1)
        cq.enqueue(2)
        cq.dequeue()
        
        stats = cq.stats
        assert stats.size == 1
        assert stats.enqueue_count == 2
        assert stats.dequeue_count == 1
    
    def test_peek(self):
        """Test peek alias."""
        cq = CircularQueue[int](capacity=5)
        cq.enqueue(1)
        assert cq.peek() == 1
    
    def test_repr(self):
        """Test string representation."""
        cq = CircularQueue[int](capacity=5)
        cq.enqueue(1)
        cq.enqueue(2)
        assert "CircularQueue" in repr(cq)


class TestPriorityDeque:
    """Tests for Priority Deque."""
    
    def test_empty_priority_deque(self):
        """Test empty priority deque."""
        pdq = PriorityDeque[int]()
        assert len(pdq) == 0
    
    def test_append_pop(self):
        """Test append and pop ordering."""
        pdq = PriorityDeque[int](priority_func=lambda x: -x)  # Higher values first
        pdq.append(1)
        pdq.append(5)
        pdq.append(3)
        
        assert pdq.pop() == 5
        assert pdq.pop() == 3
        assert pdq.pop() == 1
    
    def test_max_heap(self):
        """Test max_heap mode with priority function."""
        pdq = PriorityDeque[int](priority_func=lambda x: -x)
        pdq.append(1)
        pdq.append(10)
        pdq.append(5)
        
        assert pdq.pop() == 10
        assert pdq.pop() == 5
        assert pdq.pop() == 1


class TestFactoryFunctions:
    """Tests for factory functions."""
    
    def test_create_queue(self):
        """Test create_queue factory."""
        q = create_queue([1, 2, 3])
        assert isinstance(q, Queue)
        assert len(q) == 3
    
    def test_create_thread_safe_queue(self):
        """Test create_thread_safe_queue."""
        q = create_queue([1, 2], thread_safe=True)
        assert isinstance(q, ThreadSafeQueue)
        assert len(q) == 2
    
    def test_create_circular_queue(self):
        """Test create_circular_queue."""
        cq = create_circular_queue(5)
        assert isinstance(cq, CircularQueue)
        assert cq.capacity() == 5
    
    def test_create_priority_queue(self):
        """Test create_priority_queue."""
        pq = create_priority_queue(priority_func=lambda x: -x)
        assert isinstance(pq, PriorityQueue)


class TestEdgeCases:
    """Edge case tests."""
    
    def test_queue_with_none(self):
        """Test queue with None values."""
        q = Queue[object]()
        q.enqueue(None)
        assert q.dequeue() is None
    
    def test_queue_with_duplicates(self):
        """Test queue with duplicate values."""
        q = Queue[int]()
        q.enqueue(1)
        q.enqueue(1)
        assert q.dequeue() == 1
        assert q.dequeue() == 1
    
    def test_priority_queue_duplicates(self):
        """Test priority queue with same priority."""
        pq = PriorityQueue[tuple]()
        pq.enqueue((1, "a"))
        pq.enqueue((1, "b"))
        # Both have same priority, order is implementation-dependent
        items = [pq.dequeue(), pq.dequeue()]
        assert set(items) == {(1, "a"), (1, "b")}
    
    def test_deque_empty_error(self):
        """Test deque operations on empty raise errors."""
        dq = Deque[int]()
        with pytest.raises(QueueEmptyError):
            dq.pop()
        with pytest.raises(QueueEmptyError):
            dq.popleft()
    
    def test_circular_queue_zero_capacity(self):
        """Test circular queue with zero capacity raises error."""
        with pytest.raises(ValueError):
            CircularQueue[int](capacity=0)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])