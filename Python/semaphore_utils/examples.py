"""
Semaphore Utils Examples

This file demonstrates various use cases for the semaphore utilities:
- Concurrency limiting for API calls
- Database connection pooling
- Rate limiting
- Resource allocation
- Async operations

Author: AllToolkit
Date: 2026-04-29
"""

import threading
import time
import asyncio
import random
from concurrent.futures import ThreadPoolExecutor

from semaphore_utils.semaphore_utils import (
    Semaphore,
    WeightedSemaphore,
    SemaphorePool,
    AsyncSemaphore,
    RateLimiter,
    ConcurrencyLimit,
    PrioritySemaphore,
    run_with_semaphore,
    acquire_all,
)


def example_basic_semaphore():
    """Example: Basic semaphore for limiting concurrent operations."""
    print("\n" + "=" * 50)
    print("Example 1: Basic Semaphore")
    print("=" * 50)
    
    # Create a semaphore that allows max 3 concurrent operations
    sem = Semaphore(3)
    
    def process_item(item_id):
        print(f"  Starting item {item_id}")
        with sem:
            print(f"  Processing item {item_id} (semaphore acquired)")
            time.sleep(0.5)  # Simulate work
            print(f"  Finished item {item_id}")
    
    # Run 10 items with limited concurrency
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_item, i) for i in range(1, 11)]
        for f in futures:
            f.result()
    
    print("All items processed!")


def example_weighted_semaphore():
    """Example: Weighted semaphore for variable resource allocation."""
    print("\n" + "=" * 50)
    print("Example 2: Weighted Semaphore")
    print("=" * 50)
    
    # Create a weighted semaphore with total capacity of 100 units
    # Simulate a system with 100MB of memory for tasks
    memory_sem = WeightedSemaphore(100)
    
    def run_task(task_name, memory_needed):
        print(f"  Task '{task_name}' requesting {memory_needed}MB...")
        with memory_sem.acquire_context(memory_needed):
            print(f"  Task '{task_name}' running with {memory_needed}MB allocated")
            time.sleep(0.3)
            print(f"  Task '{task_name}' completed, memory released")
    
    # Tasks with different memory requirements
    tasks = [
        ("Small Task A", 10),
        ("Medium Task B", 30),
        ("Large Task C", 50),
        ("Tiny Task D", 5),
        ("Big Task E", 40),
    ]
    
    threads = [threading.Thread(target=run_task, args=(name, mem)) 
               for name, mem in tasks]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    print("All tasks completed!")


def example_rate_limiter():
    """Example: Rate limiting for API calls."""
    print("\n" + "=" * 50)
    print("Example 3: Rate Limiter")
    print("=" * 50)
    
    # Create a rate limiter: 5 API calls per second
    limiter = RateLimiter(5, 1.0)
    
    def api_call(call_id):
        limiter.acquire()
        print(f"  API call {call_id} at {time.strftime('%H:%M:%S')}")
    
    print("Making 10 API calls (max 5/sec):")
    start = time.time()
    for i in range(1, 11):
        api_call(i)
    elapsed = time.time() - start
    
    print(f"  10 calls completed in {elapsed:.2f}s")
    print(f"  Expected: ~2s (10 calls / 5 calls/sec)")
    
    # With burst
    print("\nWith burst capacity of 5:")
    limiter_burst = RateLimiter(5, 1.0, burst=5)
    
    for i in range(1, 6):  # Burst calls
        limiter_burst.try_acquire()
        print(f"  Burst call {i} (immediate)")
    
    print("  Next call must wait...")


def example_semaphore_pool():
    """Example: Semaphore pool for multiple resources."""
    print("\n" + "=" * 50)
    print("Example 4: Semaphore Pool")
    print("=" * 50)
    
    # Create a pool for different services
    pool = SemaphorePool(5)
    
    # Configure different capacities
    pool.get('database', capacity=10)
    pool.get('api', capacity=5)
    pool.get('cache', capacity=20)
    
    print("Semaphore pool created:")
    for key, stats in pool.stats().items():
        print(f"  {key}: capacity={stats['capacity']}, available={stats['available']}")
    
    def use_resource(resource_name, duration):
        sem = pool.get(resource_name)
        with sem:
            print(f"  Using {resource_name} for {duration}s")
            time.sleep(duration)
            print(f"  Released {resource_name}")
    
    # Use multiple resources concurrently
    threads = [
        threading.Thread(target=use_resource, args=('database', 0.2)),
        threading.Thread(target=use_resource, args=('api', 0.2)),
        threading.Thread(target=use_resource, args=('cache', 0.2)),
    ]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    print("Pool stats after use:")
    for key, stats in pool.stats().items():
        print(f"  {key}: in_use={stats['in_use']}, available={stats['available']}")


def example_priority_semaphore():
    """Example: Priority semaphore for prioritized access."""
    print("\n" + "=" * 50)
    print("Example 5: Priority Semaphore")
    print("=" * 50)
    
    # Single permit semaphore with priority
    sem = PrioritySemaphore(1)
    
    def priority_task(name, priority):
        sem.acquire(priority=priority)
        print(f"  {name} (priority {priority}) acquired semaphore")
        time.sleep(0.1)
        sem.release()
        print(f"  {name} released")
    
    # Create tasks with different priorities
    # Lower number = higher priority
    tasks = [
        ("Critical Task", 0),     # Highest priority
        ("Normal Task", 5),       # Medium priority  
        ("Background Task", 10),  # Lowest priority
    ]
    
    # Acquire semaphore first
    sem.acquire()
    
    threads = [threading.Thread(target=priority_task, args=(name, pri)) 
               for name, pri in tasks]
    
    print("Starting threads (all will queue up):")
    for t in threads:
        t.start()
        time.sleep(0.05)  # Ensure they queue
    
    print("Releasing initial permit...")
    sem.release()
    
    for t in threads:
        t.join()
    
    print("Priority order served correctly!")


def example_concurrency_limit():
    """Example: Combined concurrency and rate limiting."""
    print("\n" + "=" * 50)
    print("Example 6: Concurrency Limit")
    print("=" * 50)
    
    # Limit to 3 concurrent operations, max 10/sec
    limit = ConcurrencyLimit(max_concurrent=3, rate=10, period=1.0)
    
    def limited_operation(op_id):
        with limit:
            print(f"  Operation {op_id} started")
            time.sleep(0.2)
            print(f"  Operation {op_id} completed")
    
    print("Running 10 operations (max 3 concurrent, 10/sec):")
    
    threads = [threading.Thread(target=limited_operation, args=(i,)) 
               for i in range(1, 11)]
    
    start = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    elapsed = time.time() - start
    print(f"Completed in {elapsed:.2f}s")


def example_acquire_all():
    """Example: Acquiring multiple semaphores atomically."""
    print("\n" + "=" * 50)
    print("Example 7: Acquire All")
    print("=" * 50)
    
    # Two resources needed for an operation
    db_sem = Semaphore(1)
    cache_sem = Semaphore(1)
    
    print("Acquiring both database and cache semaphores atomically...")
    
    acquire_all(db_sem, cache_sem)
    
    print(f"  Database semaphore: in_use={db_sem.in_use()}")
    print(f"  Cache semaphore: in_use={cache_sem.in_use()}")
    
    print("Performing operation with both resources...")
    time.sleep(0.1)
    
    db_sem.release()
    cache_sem.release()
    
    print("Both resources released")


def example_run_with_semaphore():
    """Example: Running function with semaphore."""
    print("\n" + "=" * 50)
    print("Example 8: Run With Semaphore")
    print("=" * 50)
    
    sem = Semaphore(1)
    
    def expensive_computation(n):
        print(f"  Computing sum of 1 to {n}...")
        time.sleep(0.1)
        return sum(range(1, n + 1))
    
    result = run_with_semaphore(sem, expensive_computation, 100, timeout=5.0)
    print(f"  Result: {result}")
    print(f"  Semaphore available: {sem.available()}")


async def example_async_semaphore():
    """Example: Async semaphore for async operations."""
    print("\n" + "=" * 50)
    print("Example 9: Async Semaphore")
    print("=" * 50)
    
    sem = AsyncSemaphore(3)
    
    async def async_task(task_id):
        async with sem:
            print(f"  Async task {task_id} started")
            await asyncio.sleep(0.2)
            print(f"  Async task {task_id} completed")
            return task_id
    
    print("Running 5 async tasks (max 3 concurrent):")
    
    results = await asyncio.gather(
        async_task(1),
        async_task(2),
        async_task(3),
        async_task(4),
        async_task(5),
    )
    
    print(f"Completed tasks: {results}")


def example_thread_safe_counter():
    """Example: Thread-safe counter using semaphore."""
    print("\n" + "=" * 50)
    print("Example 10: Thread-Safe Counter")
    print("=" * 50)
    
    sem = Semaphore(1)  # Mutex-like behavior
    counter = {'value': 0}
    
    def increment(thread_id, times):
        for _ in range(times):
            with sem:
                counter['value'] += 1
    
    threads = [threading.Thread(target=increment, args=(i, 100)) 
               for i in range(10)]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    expected = 10 * 100
    print(f"  Counter value: {counter['value']}")
    print(f"  Expected: {expected}")
    print(f"  Correct: {counter['value'] == expected}")


def run_all_examples():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Semaphore Utils Examples")
    print("=" * 60)
    
    example_basic_semaphore()
    example_weighted_semaphore()
    example_rate_limiter()
    example_semaphore_pool()
    example_priority_semaphore()
    example_concurrency_limit()
    example_acquire_all()
    example_run_with_semaphore()
    asyncio.run(example_async_semaphore())
    example_thread_safe_counter()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()