#!/usr/bin/env python3
"""
Basic usage examples for Priority Queue Utilities.
"""

import sys
sys.path.insert(0, '..')

import time
from mod import (
    PriorityQueue,
    PriorityTaskExecutor,
    TaskScheduler,
    PriorityPolicy,
)


def example_basic_queue():
    """Basic priority queue usage."""
    print("\n=== Basic Priority Queue ===")
    
    queue = PriorityQueue[str]()
    
    # Add items with different priorities
    queue.push("Low priority task", priority=10)
    queue.push("High priority task", priority=1)
    queue.push("Medium priority task", priority=5)
    
    # Process in priority order
    while not queue.empty():
        item = queue.pop()
        print(f"  Processing: {item.data}")


def example_delayed_tasks():
    """Tasks with execution delays."""
    print("\n=== Delayed Tasks ===")
    
    queue = PriorityQueue[str]()
    
    # Add task with 2 second delay
    queue.push("Delayed task", priority=1, delay=2)
    queue.push("Immediate task", priority=1)
    
    print("  Waiting for delayed task...")
    
    # Immediate task comes first
    item = queue.pop(timeout=0.1)
    if item:
        print(f"  Got: {item.data}")
    
    # Delayed task not ready yet
    item = queue.pop(timeout=0.1)
    print(f"  Delayed ready: {item is not None}")
    
    # Wait for delay
    time.sleep(2)
    item = queue.pop(timeout=0.1)
    if item:
        print(f"  Got: {item.data}")


def example_priority_update():
    """Update task priority dynamically."""
    print("\n=== Priority Update ===")
    
    queue = PriorityQueue[str]()
    
    task_id = queue.push("Originally low priority", priority=10)
    print(f"  Added with priority 10")
    
    # Update to high priority
    queue.update_priority(task_id, 1)
    print(f"  Updated to priority 1")
    
    item = queue.pop()
    print(f"  Popped: {item.data}")


def example_task_cancellation():
    """Cancel pending tasks."""
    print("\n=== Task Cancellation ===")
    
    queue = PriorityQueue[str]()
    
    task_id1 = queue.push("Task 1", priority=1)
    task_id2 = queue.push("Task 2", priority=2)
    
    print(f"  Queue size: {queue.size()}")
    
    # Cancel first task
    queue.cancel(task_id1)
    print(f"  Cancelled task 1")
    
    # Pop remaining
    while not queue.empty():
        item = queue.pop(block=False)
        if item:
            print(f"  Got: {item.data}")
    
    print(f"  Queue size after: {queue.size()}")


def example_executor():
    """Using PriorityTaskExecutor."""
    print("\n=== Task Executor ===")
    
    results = []
    
    def task(n):
        result = n * n
        results.append(result)
        return result
    
    def on_result(result):
        print(f"  Task completed: {result.result}")
    
    queue = PriorityQueue()
    executor = PriorityTaskExecutor(
        queue,
        num_workers=2,
        default_callback=on_result
    )
    
    # Add tasks
    for i in range(5):
        queue.push(lambda n=i: task(n), priority=i)
    
    print("  Starting executor...")
    executor.start()
    time.sleep(0.5)
    executor.stop()
    
    print(f"  Results: {sorted(results)}")
    print(f"  Stats: {executor.stats}")


def example_scheduler():
    """Using TaskScheduler."""
    print("\n=== Task Scheduler ===")
    
    results = []
    
    scheduler = TaskScheduler(num_workers=1)
    
    # One-time task
    scheduler.schedule_once(
        lambda: results.append("one-time"),
        delay=0.1
    )
    
    # Recurring task
    scheduler.schedule_interval(
        lambda: results.append("recurring"),
        interval=0.1,
        initial_delay=0,
        max_runs=3
    )
    
    print("  Starting scheduler...")
    scheduler.start()
    time.sleep(0.5)
    scheduler.stop()
    
    print(f"  Results: {results}")


def example_policy():
    """Different priority policies."""
    print("\n=== Priority Policies ===")
    
    # HIGHEST_FIRST (default): lower number = higher priority
    queue_high = PriorityQueue[str](policy=PriorityPolicy.HIGHEST_FIRST)
    queue_high.push("A", priority=1)
    queue_high.push("B", priority=5)
    print(f"  HIGHEST_FIRST: {queue_high.pop().data}")  # A
    
    # LOWEST_FIRST: higher number = higher priority
    queue_low = PriorityQueue[str](policy=PriorityPolicy.LOWEST_FIRST)
    queue_low.push("A", priority=1)
    queue_low.push("B", priority=5)
    print(f"  LOWEST_FIRST: {queue_low.pop().data}")  # B
    
    # FIFO: ignore priority
    queue_fifo = PriorityQueue[str](policy=PriorityPolicy.FIFO)
    queue_fifo.push("First", priority=10)
    queue_fifo.push("Second", priority=1)
    print(f"  FIFO: {queue_fifo.pop().data}")  # First


def example_callbacks():
    """Task callbacks."""
    print("\n=== Task Callbacks ===")
    
    queue = PriorityQueue[str]()
    
    def callback(item):
        print(f"  Callback received: {item}")
    
    queue.push("Important task", priority=1, callback=callback)
    
    item = queue.pop()
    if item.callback:
        item.callback(item.data)


def example_thread_safety():
    """Thread-safe concurrent access."""
    print("\n=== Thread Safety ===")
    
    import threading
    
    queue = PriorityQueue[int]()
    results = []
    
    def producer(start, count):
        for i in range(count):
            queue.push(start + i, priority=i)
    
    def consumer(count):
        for _ in range(count):
            item = queue.pop(timeout=1.0)
            if item:
                results.append(item.data)
    
    # Create producers
    threads = []
    for i in range(3):
        t = threading.Thread(target=producer, args=(i * 100, 100))
        threads.append(t)
        t.start()
    
    # Wait for producers
    for t in threads:
        t.join()
    
    print(f"  Queue size: {queue.size()}")
    
    # Consume all
    while not queue.empty():
        item = queue.pop(timeout=0.1)
        if item:
            results.append(item.data)
    
    print(f"  Items processed: {len(results)}")


if __name__ == "__main__":
    print("Priority Queue Utilities - Examples")
    print("=" * 40)
    
    example_basic_queue()
    example_delayed_tasks()
    example_priority_update()
    example_task_cancellation()
    example_executor()
    example_scheduler()
    example_policy()
    example_callbacks()
    example_thread_safety()
    
    print("\n" + "=" * 40)
    print("All examples completed!")