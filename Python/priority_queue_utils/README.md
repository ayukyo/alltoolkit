# Priority Queue Utilities

A comprehensive, thread-safe priority queue implementation with advanced features for Python applications. **Zero external dependencies** - uses only Python standard library.

## Features

- **Thread-Safe Operations**: Fine-grained locking for concurrent access
- **Dynamic Priority Updates**: Modify priority of pending tasks
- **Delayed Execution**: Schedule tasks with configurable delays
- **Task Cancellation**: Cancel pending tasks before execution
- **Execution History**: Track completed task results
- **Multiple Priority Policies**: Highest-first, lowest-first, FIFO
- **Task Scheduler**: One-time and recurring task scheduling
- **Double-Ended Priority Queue**: Access both min and max efficiently
- **Bounded Queue**: Size-limited queue with overflow policies

## Installation

No installation required - just copy the `mod.py` file to your project.

```python
from priority_queue_utils import PriorityQueue, TaskScheduler
```

## Quick Start

### Basic Priority Queue

```python
from mod import PriorityQueue

# Create a queue
queue = PriorityQueue[str]()

# Add items with different priorities (lower number = higher priority)
queue.push("urgent", priority=1)
queue.push("normal", priority=5)
queue.push("low", priority=10)

# Pop items - they come out in priority order
print(queue.pop().data)  # "urgent"
print(queue.pop().data)  # "normal"
print(queue.pop().data)  # "low"
```

### Task Scheduler

```python
from mod import TaskScheduler
import time

scheduler = TaskScheduler(num_workers=2)

# Schedule one-time task
scheduler.schedule_once(
    lambda: print("Hello!"),
    delay=5  # Run after 5 seconds
)

# Schedule recurring task
scheduler.schedule_interval(
    lambda: print("Ping!"),
    interval=10  # Run every 10 seconds
)

# Schedule at specific time
from datetime import datetime, timedelta
scheduler.schedule_once(
    lambda: print("Time's up!"),
    execute_at=datetime.now() + timedelta(hours=1)
)

# Start processing
scheduler.start()

# Later...
scheduler.stop()
```

### With Task Executor

```python
from mod import PriorityQueue, PriorityTaskExecutor

def process_result(result):
    print(f"Task completed: {result}")

queue = PriorityQueue()
executor = PriorityTaskExecutor(
    queue,
    num_workers=4,
    default_callback=process_result
)

# Add tasks
queue.push(lambda: sum(range(1000)), priority=1)
queue.push(lambda: "hello world", priority=2)

executor.start()
# ... tasks are processed automatically
executor.stop()
```

## API Reference

### PriorityQueue

The core priority queue implementation.

```python
queue = PriorityQueue[T](
    policy=PriorityPolicy.HIGHEST_FIRST,  # or LOWEST_FIRST, FIFO
    maxsize=0,      # 0 = unlimited
    history_size=100
)
```

#### Methods

| Method | Description |
|--------|-------------|
| `push(item, priority=5, callback=None, delay=None)` | Add item, returns task ID |
| `pop(timeout=None, block=True)` | Remove and return highest priority item |
| `peek()` | View highest priority item without removing |
| `update_priority(task_id, new_priority)` | Change priority of pending task |
| `cancel(task_id)` | Cancel a pending task |
| `get_task_state(task_id)` | Get state of a task |
| `size()` | Current queue size |
| `empty()` | Check if empty |
| `full()` | Check if at maxsize |
| `clear()` | Remove all pending items |
| `close()` | Close queue for new items |
| `get_history(limit=10)` | Get recent task results |

### PriorityTaskExecutor

Process tasks from a queue with worker threads.

```python
executor = PriorityTaskExecutor(
    queue,
    num_workers=1,
    default_callback=None  # Called for each result
)
```

#### Methods

| Method | Description |
|--------|-------------|
| `start()` | Start worker threads |
| `stop(wait=True, timeout=5.0)` | Stop workers |
| `stats` | Get statistics dict |

### TaskScheduler

High-level scheduling with delays and intervals.

```python
scheduler = TaskScheduler(num_workers=2)
```

#### Methods

| Method | Description |
|--------|-------------|
| `schedule_once(func, args, kwargs, priority, delay, execute_at)` | One-time task |
| `schedule_interval(func, interval, args, kwargs, priority, initial_delay, max_runs)` | Recurring task |
| `cancel_task(task_id)` | Cancel a task |
| `start()` | Start scheduler |
| `stop(wait=True)` | Stop scheduler |

### PriorityDeque

Double-ended priority queue for accessing both min and max.

```python
deque = PriorityDeque[int]()
deque.push(5, priority=5)
deque.push(1, priority=1)
deque.push(10, priority=10)

deque.peek_min()  # 1
deque.peek_max()  # 10
deque.pop_min()   # 1
deque.pop_max()   # 10
```

### BoundedPriorityQueue

Size-limited queue with overflow handling.

```python
queue = BoundedPriorityQueue[int](
    maxsize=100,
    policy=OverflowPolicy.REJECT  # or DROP_LOWEST, DROP_OLDEST
)
```

## Utility Functions

```python
from mod import create_priority_queue, merge_priority_queues, batch_push

# Create from list
queue = create_priority_queue([
    ("item1", 1),  # (item, priority)
    ("item2", 2),
])

# Merge queues
merged = merge_priority_queues(q1, q2, q3)

# Batch push
task_ids = batch_push(queue, [
    (item1, 1),
    (item2, 2),
])
```

## Examples

### Priority Inversion Handling

```python
from mod import PriorityQueue

queue = PriorityQueue[str]()

# Add high-priority task
task_id = queue.push("urgent", priority=1)

# Later, update if needed
queue.update_priority(task_id, 10)  # Demote to low priority
```

### Delayed Execution

```python
from mod import TaskScheduler

scheduler = TaskScheduler()

# Run after 5 minutes
scheduler.schedule_once(
    send_email,
    args=[user, "Welcome!"],
    delay=300  # seconds
)

scheduler.start()
```

### Task Cancellation

```python
queue = PriorityQueue()

# Schedule a task
task_id = queue.push(long_running_task, priority=1)

# Cancel if needed
if should_cancel:
    queue.cancel(task_id)
```

### Concurrent Consumers

```python
from mod import PriorityQueue, PriorityTaskExecutor

queue = PriorityQueue()

# Multiple workers consuming from same queue
executor = PriorityTaskExecutor(queue, num_workers=8)
executor.start()

# Producers can push from anywhere
for i in range(1000):
    queue.push(process_item, priority=i % 10)

executor.stop()
```

## Thread Safety

All operations are thread-safe. The queue uses `threading.RLock` for
fine-grained locking, and `threading.Condition` for efficient blocking
operations.

```python
# Safe for concurrent use
import threading

queue = PriorityQueue()

def producer():
    for i in range(100):
        queue.push(f"item-{i}", priority=i)

def consumer():
    while True:
        item = queue.pop(timeout=1.0)
        if item:
            process(item)

# Multiple producers and consumers can work simultaneously
```

## Performance

- **Push**: O(log n)
- **Pop**: O(log n) amortized
- **Peek**: O(1)
- **Update Priority**: O(n) - requires heap reorganization
- **Memory**: O(n) for n items

## Use Cases

1. **Job Processing**: Prioritize critical tasks
2. **Task Scheduling**: Delay and repeat execution
3. **Event Systems**: Order events by importance
4. **Request Handling**: Process high-priority requests first
5. **Resource Allocation**: Manage limited resources by priority

## License

MIT License - Free for personal and commercial use.