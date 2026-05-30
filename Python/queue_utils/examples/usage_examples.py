#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Queue Utilities Examples
======================================
Usage examples demonstrating queue data structures.

Author: AllToolkit
License: MIT
Date: 2026-05-30
"""

import sys
sys.path.insert(0, '..')

from mod import (
    Queue, ThreadSafeQueue, PriorityQueue, MaxPriorityQueue,
    Deque, CircularQueue, PriorityDeque,
    create_queue, create_circular_queue, create_priority_queue
)


def example_queue():
    """Basic FIFO Queue usage."""
    print("\n=== Basic Queue ===")
    
    # Create queue
    q = Queue[str]()
    
    # Enqueue items
    q.enqueue("first")
    q.enqueue("second")
    q.enqueue("third")
    
    print(f"Queue: {q}")
    print(f"Front: {q.front()}")
    print(f"Rear: {q.rear()}")
    print(f"Size: {q.size()}")
    
    # Dequeue items (FIFO)
    print("\nDequeuing:")
    while not q.is_empty():
        print(f"  Dequeued: {q.dequeue()}")


def example_circular_queue():
    """Circular Queue (Ring Buffer) usage."""
    print("\n=== Circular Queue ===")
    
    cq = CircularQueue[int](capacity=5)
    
    # Fill the queue
    print("Adding 1-5:")
    for i in range(1, 6):
        cq.enqueue(i)
        print(f"  Enqueued {i}, is_full: {cq.is_full()}")
    
    print(f"\nQueue contents: {list(cq)}")
    print(f"Front: {cq.front()}, Back: {cq.back()}")
    
    # Dequeue and add more
    print("\nDequeuing 2 items and adding 2 more:")
    print(f"  Dequeued: {cq.dequeue()}")
    print(f"  Dequeued: {cq.dequeue()}")
    
    cq.enqueue(99)
    cq.enqueue(100)
    
    print(f"Queue contents: {list(cq)}")
    
    # Stats
    print(f"\nStats: enqueue_count={cq.stats.enqueue_count}, dequeue_count={cq.stats.dequeue_count}")


def example_priority_queue():
    """Priority Queue usage."""
    print("\n=== Priority Queue ===")
    
    # Simple tuple priority
    pq = PriorityQueue[tuple]()  # (priority, task)
    
    tasks = [
        (3, "Low priority task"),
        (1, "Critical task"),
        (2, "Medium priority task"),
        (1, "Another critical task"),
    ]
    
    print("Adding tasks:")
    for priority, task in tasks:
        pq.enqueue((priority, task))
        print(f"  Added: [{priority}] {task}")
    
    print("\nDequeuing by priority:")
    while not pq.is_empty():
        priority, task = pq.dequeue()
        print(f"  [{priority}] {task}")


def example_priority_queue_custom():
    """Priority Queue with custom priority function."""
    print("\n=== Priority Queue (Custom Function) ===")
    
    # Custom priority: shorter strings have higher priority
    pq = PriorityQueue[str](priority_func=lambda s: len(s))
    
    strings = ["longest string", "short", "medium length", "tiny"]
    
    print("Adding strings (priority by length):")
    for s in strings:
        pq.enqueue(s)
        print(f"  Added: '{s}' (length={len(s)})")
    
    print("\nDequeuing (shortest first):")
    while not pq.is_empty():
        s = pq.dequeue()
        print(f"  '{s}'")


def example_max_priority_queue():
    """Max Priority Queue - highest priority first."""
    print("\n=== Max Priority Queue ===")
    
    pq = MaxPriorityQueue[tuple]()  # (score, item)
    
    items = [
        (100, "Gold medal"),
        (50, "Silver medal"),
        (75, "Bronze medal"),
    ]
    
    print("Adding items (higher score = higher priority):")
    for score, item in items:
        pq.enqueue((score, item))
    
    print("\nDequeuing (highest priority first):")
    while not pq.is_empty():
        score, item = pq.dequeue()
        print(f"  {score}: {item}")


def example_deque():
    """Double-Ended Queue usage."""
    print("\n=== Deque ===")
    
    dq = Deque[int]()
    
    # Add items to both ends
    dq.appendleft(0)
    dq.append(4)
    dq.append(5)
    dq.appendleft(-1)
    
    print(f"Deque: {dq}")
    print(f"Front: {dq.front()}, Back: {dq.back()}")
    
    # Remove from both ends
    print("\nRemoving from both ends:")
    print(f"  popleft: {dq.popleft()}")
    print(f"  pop: {dq.pop()}")
    print(f"  Remaining: {dq}")
    
    # Rotate
    dq.append(6)
    print(f"\nBefore rotate: {dq}")
    dq.rotate(2)
    print(f"After rotate(2): {dq}")


def example_deque_maxlen():
    """Deque with maxlen for fixed-size buffer."""
    print("\n=== Deque with maxlen ===")
    
    # Keep last 3 items
    dq = Deque[int](maxlen=3)
    
    for i in range(1, 6):
        dq.append(i)
        print(f"Added {i}, Deque: {dq}")
    
    print(f"\nFinal (last 3): {dq}")


def example_thread_safe_queue():
    """Thread-Safe Queue usage."""
    print("\n=== Thread-Safe Queue ===")
    
    tsq = ThreadSafeQueue[str]()
    
    # Simulate producer
    tsq.enqueue("task1")
    tsq.enqueue("task2")
    tsq.enqueue("task3")
    
    print(f"Thread-safe queue with {tsq.size()} items")
    
    # Simulate consumer
    while not tsq.is_empty():
        print(f"  Processing: {tsq.dequeue()}")
    
    print("Queue is now empty")


def example_priority_deque():
    """Priority Deque - combines priority queue and deque."""
    print("\n=== Priority Deque ===")
    
    pdq = PriorityDeque[int](priority_func=lambda x: -x)  # Higher values first
    
    pdq.append(1)
    pdq.append(10)
    pdq.append(5)
    pdq.append(8)
    
    print(f"Priority Deque: {pdq}")
    print("\nPop (highest priority):")
    print(f"  Pop: {pdq.pop()}")
    print(f"  Remaining: {pdq}")


def example_factory_functions():
    """Factory function usage."""
    print("\n=== Factory Functions ===")
    
    # Create basic queue
    q = create_queue(["a", "b", "c"])
    print(f"create_queue: {q}")
    
    # Create thread-safe queue
    tsq = create_queue(thread_safe=True)
    tsq.enqueue(1)
    print(f"create_queue(thread_safe=True): {tsq}")
    
    # Create circular queue
    cq = create_circular_queue(3)
    cq.enqueue(1)
    print(f"create_circular_queue(3): {cq}")
    
    # Create priority queue with custom priority
    pq = create_priority_queue(priority_func=lambda x: -x)
    pq.enqueue(10)
    pq.enqueue(5)
    print(f"create_priority_queue: {pq}")


def example_queue_stats():
    """Queue statistics tracking."""
    print("\n=== Queue Statistics ===")
    
    q = Queue[int]()
    
    # Track operations
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    q.dequeue()
    q.front()
    q.front()
    
    stats = q.stats
    print(f"Queue stats:")
    print(f"  Size: {stats.size}")
    print(f"  Enqueue count: {stats.enqueue_count}")
    print(f"  Dequeue count: {stats.dequeue_count}")
    print(f"  Peek count: {stats.peek_count}")


def example_work_queue():
    """Simulate a work queue pattern."""
    print("\n=== Work Queue Pattern ===")
    
    q = Queue[str]()
    
    # Add work items
    work_items = ["task1", "task2", "task3", "task4"]
    q.enqueue_all(work_items)
    
    print(f"Work queue has {q.size()} tasks")
    
    # Process tasks
    processed = 0
    while not q.is_empty():
        task = q.dequeue()
        print(f"  Processing: {task}")
        processed += 1
    
    print(f"Processed {processed} tasks")


def example_task_scheduler():
    """Simulate task scheduling with priority queue."""
    print("\n=== Task Scheduler ===")
    
    pq = PriorityQueue[tuple]()  # (time, task)
    
    # Add scheduled tasks
    tasks = [
        (10, "Low priority"),
        (1, "Urgent task"),
        (5, "Normal task"),
        (1, "Critical task"),
    ]
    
    for time, task in tasks:
        pq.enqueue((time, task))
    
    print("Task execution order (by time):")
    while not pq.is_empty():
        time, task = pq.dequeue()
        print(f"  Time {time}: {task}")


def example_buffer():
    """Simulate a fixed-size buffer using circular queue."""
    print("\n=== Fixed-Size Buffer ===")
    
    buffer = CircularQueue[str](capacity=3)
    
    # Producer simulation
    data = ["a", "b", "c", "d", "e", "f"]
    
    for item in data:
        if buffer.is_full():
            oldest = buffer.dequeue()
            print(f"  Buffer full, dropping: {oldest}")
        buffer.enqueue(item)
        print(f"  Added: {item}, Buffer: {list(buffer)}")


if __name__ == "__main__":
    print("=" * 60)
    print("Queue Utilities - Usage Examples")
    print("=" * 60)
    
    example_queue()
    example_circular_queue()
    example_priority_queue()
    example_priority_queue_custom()
    example_max_priority_queue()
    example_deque()
    example_deque_maxlen()
    example_thread_safe_queue()
    example_priority_deque()
    example_factory_functions()
    example_queue_stats()
    example_work_queue()
    example_task_scheduler()
    example_buffer()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)