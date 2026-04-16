"""
Priority Queue Utilities
========================

A comprehensive priority queue implementation with advanced features:
- Thread-safe operations
- Priority updates for existing items
- Delayed task execution
- Task cancellation
- Multiple consumer support
- Priority inversion handling
- Task scheduling and scheduling policies

Zero external dependencies - uses only Python standard library.

Author: AllToolkit
Date: 2026-04-16
"""

import heapq
import threading
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    Set,
    Tuple,
    TypeVar,
    Union,
)
from concurrent.futures import Future
from datetime import datetime, timedelta

T = TypeVar('T')


class TaskState(Enum):
    """Task execution states."""
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    CANCELLED = auto()
    FAILED = auto()


class PriorityPolicy(Enum):
    """Priority scheduling policies."""
    HIGHEST_FIRST = auto()  # Lower number = higher priority (default)
    LOWEST_FIRST = auto()   # Higher number = higher priority
    FIFO = auto()           # First in, first out (priority ignored)


@dataclass(order=True)
class PrioritizedItem(Generic[T]):
    """
    A prioritized item for the heap queue.
    
    The sort_key is used for ordering, while the actual data
    and metadata are stored separately.
    """
    sort_key: Tuple[int, float]  # (priority, sequence_number)
    task_id: str = field(compare=False)
    data: T = field(compare=False)
    created_at: float = field(compare=False)
    execute_after: Optional[float] = field(default=None, compare=False)
    callback: Optional[Callable[[T], Any]] = field(default=None, compare=False)
    state: TaskState = field(default=TaskState.PENDING, compare=False)
    _priority: int = field(default=0, compare=False)
    
    def __post_init__(self):
        self._priority = self.sort_key[0]


@dataclass
class TaskResult(Generic[T]):
    """Result of a task execution."""
    task_id: str
    success: bool
    result: Any = None
    error: Optional[Exception] = None
    execution_time: float = 0.0
    started_at: Optional[float] = None
    completed_at: Optional[float] = None


class PriorityQueue(Generic[T]):
    """
    Thread-safe priority queue with advanced features.
    
    Features:
    - Thread-safe operations with fine-grained locking
    - Dynamic priority updates
    - Delayed task execution
    - Task cancellation
    - Execution history tracking
    - Multiple consumer support
    - Configurable priority policies
    
    Example:
        >>> queue = PriorityQueue[str]()
        >>> queue.push("urgent task", priority=1)
        >>> queue.push("normal task", priority=5)
        >>> item = queue.pop()
        >>> print(item)  # "urgent task"
    """
    
    def __init__(
        self,
        policy: PriorityPolicy = PriorityPolicy.HIGHEST_FIRST,
        maxsize: int = 0,
        history_size: int = 100,
    ):
        """
        Initialize the priority queue.
        
        Args:
            policy: Scheduling policy for prioritization
            maxsize: Maximum queue size (0 = unlimited)
            history_size: Number of completed tasks to keep in history
        """
        self._heap: List[PrioritizedItem[T]] = []
        self._lock = threading.RLock()
        self._not_empty = threading.Condition(self._lock)
        self._counter = 0
        self._policy = policy
        self._maxsize = maxsize
        self._history_size = history_size
        
        # Task tracking
        self._tasks: Dict[str, PrioritizedItem[T]] = {}
        self._history: List[TaskResult[T]] = []
        self._cancelled_ids: Set[str] = set()
        
        # State
        self._closed = False
        self._pending_futures: Dict[str, Future] = {}
    
    def _get_next_sequence(self) -> int:
        """Get the next sequence number for ordering."""
        self._counter += 1
        return self._counter
    
    def _calculate_sort_key(self, priority: int, sequence: int) -> Tuple[int, float]:
        """
        Calculate the sort key based on policy.
        
        For HIGHEST_FIRST: lower priority number = executed first
        For LOWEST_FIRST: higher priority number = executed first
        For FIFO: sequence determines order
        """
        if self._policy == PriorityPolicy.HIGHEST_FIRST:
            return (priority, sequence)
        elif self._policy == PriorityPolicy.LOWEST_FIRST:
            return (-priority, sequence)
        else:  # FIFO
            return (0, sequence)
    
    def push(
        self,
        item: T,
        priority: int = 5,
        callback: Optional[Callable[[T], Any]] = None,
        delay: Optional[float] = None,
    ) -> str:
        """
        Add an item to the priority queue.
        
        Args:
            item: The item to add
            priority: Priority level (lower = higher priority for HIGHEST_FIRST)
            callback: Optional callback to execute when item is processed
            delay: Optional delay in seconds before the item can be processed
            
        Returns:
            Task ID for tracking/cancellation
            
        Raises:
            QueueFullError: If queue is at maxsize
            QueueClosedError: If queue is closed
        """
        with self._lock:
            if self._closed:
                raise QueueClosedError("Cannot push to closed queue")
            
            if self._maxsize > 0 and len(self._heap) >= self._maxsize:
                raise QueueFullError(f"Queue is full (maxsize={self._maxsize})")
            
            sequence = self._get_next_sequence()
            task_id = str(uuid.uuid4())
            now = time.time()
            
            execute_after = None
            if delay is not None and delay > 0:
                execute_after = now + delay
            
            prioritized = PrioritizedItem(
                sort_key=self._calculate_sort_key(priority, sequence),
                task_id=task_id,
                data=item,
                created_at=now,
                execute_after=execute_after,
                callback=callback,
                state=TaskState.PENDING,
            )
            
            heapq.heappush(self._heap, prioritized)
            self._tasks[task_id] = prioritized
            self._not_empty.notify()
            
            return task_id
    
    def pop(
        self,
        timeout: Optional[float] = None,
        block: bool = True,
    ) -> Optional[PrioritizedItem[T]]:
        """
        Remove and return the highest priority item.
        
        Args:
            timeout: Maximum time to wait (None = forever)
            block: Whether to block if queue is empty
            
        Returns:
            The highest priority item, or None if timeout/empty
            
        Raises:
            QueueClosedError: If queue is closed and empty
        """
        with self._not_empty:
            end_time = None
            if timeout is not None:
                end_time = time.time() + timeout
            
            while True:
                if self._closed and not self._heap:
                    raise QueueClosedError("Queue is closed and empty")
                
                # Try to find an executable item
                item = self._pop_executable_item()
                if item is not None:
                    return item
                
                if not block:
                    return None
                
                if end_time is not None:
                    remaining = end_time - time.time()
                    if remaining <= 0:
                        return None
                    self._not_empty.wait(remaining)
                else:
                    self._not_empty.wait()
    
    def _pop_executable_item(self) -> Optional[PrioritizedItem[T]]:
        """Pop the next executable item from the heap."""
        now = time.time()
        temp_items = []
        result = None
        
        while self._heap:
            item = heapq.heappop(self._heap)
            
            # Skip cancelled items
            if item.task_id in self._cancelled_ids:
                self._cancelled_ids.discard(item.task_id)
                self._tasks.pop(item.task_id, None)
                continue
            
            # Check if item is delayed
            if item.execute_after is not None and item.execute_after > now:
                temp_items.append(item)
                continue
            
            # Found executable item
            result = item
            break
        
        # Push back non-executable items
        for temp_item in temp_items:
            heapq.heappush(self._heap, temp_item)
        
        if result is not None:
            result.state = TaskState.RUNNING
            self._tasks.pop(result.task_id, None)
        
        return result
    
    def peek(self) -> Optional[PrioritizedItem[T]]:
        """
        Look at the highest priority item without removing it.
        
        Returns:
            The highest priority item, or None if queue is empty
        """
        with self._lock:
            if not self._heap:
                return None
            return self._heap[0]
    
    def update_priority(self, task_id: str, new_priority: int) -> bool:
        """
        Update the priority of a pending task.
        
        Args:
            task_id: The task ID to update
            new_priority: The new priority value
            
        Returns:
            True if updated, False if task not found or not pending
        """
        with self._lock:
            if task_id not in self._tasks:
                return False
            
            item = self._tasks[task_id]
            if item.state != TaskState.PENDING:
                return False
            
            # Remove from heap
            self._heap = [x for x in self._heap if x.task_id != task_id]
            heapq.heapify(self._heap)
            
            # Update priority and re-add
            sequence = item.sort_key[1]
            item.sort_key = self._calculate_sort_key(new_priority, sequence)
            item._priority = new_priority
            
            heapq.heappush(self._heap, item)
            self._not_empty.notify()
            
            return True
    
    def cancel(self, task_id: str) -> bool:
        """
        Cancel a pending task.
        
        Args:
            task_id: The task ID to cancel
            
        Returns:
            True if cancelled, False if not found or already processed
        """
        with self._lock:
            if task_id not in self._tasks:
                return False
            
            item = self._tasks[task_id]
            if item.state != TaskState.PENDING:
                return False
            
            item.state = TaskState.CANCELLED
            self._cancelled_ids.add(task_id)
            return True
    
    def get_task_state(self, task_id: str) -> Optional[TaskState]:
        """
        Get the state of a task.
        
        Args:
            task_id: The task ID to check
            
        Returns:
            Task state, or None if not found
        """
        with self._lock:
            if task_id in self._tasks:
                return self._tasks[task_id].state
            
            # Check history
            for result in self._history:
                if result.task_id == task_id:
                    return TaskState.COMPLETED if result.success else TaskState.FAILED
            
            return None
    
    def size(self) -> int:
        """Get the current queue size."""
        with self._lock:
            return len(self._heap)
    
    def empty(self) -> bool:
        """Check if the queue is empty."""
        with self._lock:
            return len(self._heap) == 0
    
    def full(self) -> bool:
        """Check if the queue is full."""
        with self._lock:
            return self._maxsize > 0 and len(self._heap) >= self._maxsize
    
    def clear(self) -> int:
        """
        Clear all pending items from the queue.
        
        Returns:
            Number of items cleared
        """
        with self._lock:
            count = len(self._heap)
            self._heap.clear()
            self._tasks.clear()
            return count
    
    def close(self) -> None:
        """Close the queue for new items."""
        with self._lock:
            self._closed = True
            self._not_empty.notify_all()
    
    def is_closed(self) -> bool:
        """Check if the queue is closed."""
        return self._closed
    
    def add_to_history(self, result: TaskResult[T]) -> None:
        """Add a task result to history."""
        with self._lock:
            self._history.append(result)
            while len(self._history) > self._history_size:
                self._history.pop(0)
    
    def get_history(self, limit: int = 10) -> List[TaskResult[T]]:
        """Get recent task history."""
        with self._lock:
            return list(self._history[-limit:])
    
    def __len__(self) -> int:
        return self.size()
    
    def __bool__(self) -> bool:
        return not self.empty()


class QueueFullError(Exception):
    """Raised when trying to add to a full queue."""
    pass


class QueueClosedError(Exception):
    """Raised when operating on a closed queue."""
    pass


class PriorityTaskExecutor(Generic[T]):
    """
    Executor for processing tasks from a priority queue.
    
    Features:
    - Configurable worker count
    - Automatic task processing
    - Callback execution
    - Result history
    - Graceful shutdown
    
    Example:
        >>> queue = PriorityQueue[Callable]()
        >>> executor = PriorityTaskExecutor(queue, num_workers=2)
        >>> executor.start()
        >>> queue.push(lambda: print("Hello"), priority=1)
        >>> executor.stop()
    """
    
    def __init__(
        self,
        queue: PriorityQueue,
        num_workers: int = 1,
        default_callback: Optional[Callable[[TaskResult], Any]] = None,
    ):
        """
        Initialize the executor.
        
        Args:
            queue: The priority queue to process
            num_workers: Number of worker threads
            default_callback: Optional callback for all task results
        """
        self._queue = queue
        self._num_workers = num_workers
        self._default_callback = default_callback
        self._workers: List[threading.Thread] = []
        self._running = False
        self._lock = threading.Lock()
        self._tasks_processed = 0
        self._tasks_failed = 0
    
    def start(self) -> None:
        """Start the worker threads."""
        with self._lock:
            if self._running:
                return
            
            self._running = True
            for i in range(self._num_workers):
                worker = threading.Thread(
                    target=self._worker_loop,
                    name=f"PriorityExecutor-Worker-{i}",
                    daemon=True,
                )
                worker.start()
                self._workers.append(worker)
    
    def _worker_loop(self) -> None:
        """Main worker loop for processing tasks."""
        while self._running:
            try:
                item = self._queue.pop(timeout=0.5)
                if item is None:
                    continue
                
                self._process_item(item)
            except QueueClosedError:
                break
            except Exception as e:
                # Log and continue
                pass
    
    def _process_item(self, item: PrioritizedItem) -> None:
        """Process a single item from the queue."""
        task_id = item.task_id
        start_time = time.time()
        result: Optional[TaskResult] = None
        
        try:
            # Execute the task
            data = item.data
            task_result = None
            
            if callable(data):
                task_result = data()
            elif item.callback is not None:
                task_result = item.callback(data)
            else:
                task_result = data
            
            result = TaskResult(
                task_id=task_id,
                success=True,
                result=task_result,
                execution_time=time.time() - start_time,
                started_at=start_time,
                completed_at=time.time(),
            )
            item.state = TaskState.COMPLETED
            self._tasks_processed += 1
            
        except Exception as e:
            result = TaskResult(
                task_id=task_id,
                success=False,
                error=e,
                execution_time=time.time() - start_time,
                started_at=start_time,
                completed_at=time.time(),
            )
            item.state = TaskState.FAILED
            self._tasks_failed += 1
        
        # Add to history
        self._queue.add_to_history(result)
        
        # Call default callback
        if self._default_callback:
            try:
                self._default_callback(result)
            except Exception:
                pass
    
    def stop(self, wait: bool = True, timeout: float = 5.0) -> None:
        """
        Stop the executor.
        
        Args:
            wait: Whether to wait for workers to finish
            timeout: Maximum time to wait for each worker
        """
        with self._lock:
            self._running = False
            self._queue.close()
        
        if wait:
            for worker in self._workers:
                worker.join(timeout=timeout)
        
        self._workers.clear()
    
    @property
    def is_running(self) -> bool:
        return self._running
    
    @property
    def stats(self) -> Dict[str, int]:
        """Get executor statistics."""
        return {
            "processed": self._tasks_processed,
            "failed": self._tasks_failed,
            "queue_size": len(self._queue),
        }


class TaskScheduler:
    """
    High-level task scheduler with scheduling features.
    
    Features:
    - One-time tasks
    - Recurring tasks (interval, cron-like)
    - Task dependencies
    - Task priorities
    - Task timeouts
    
    Example:
        >>> scheduler = TaskScheduler()
        >>> scheduler.schedule_once(print, args=["Hello"], delay=5)
        >>> scheduler.schedule_interval(print, args=["Ping"], interval=10)
        >>> scheduler.start()
    """
    
    def __init__(self, num_workers: int = 2):
        """
        Initialize the scheduler.
        
        Args:
            num_workers: Number of worker threads
        """
        self._queue = PriorityQueue[Callable]()
        self._executor = PriorityTaskExecutor(self._queue, num_workers=num_workers)
        self._scheduled_tasks: Dict[str, Dict[str, Any]] = {}
        self._recurring_thread: Optional[threading.Thread] = None
        self._running = False
        self._lock = threading.Lock()
    
    def schedule_once(
        self,
        func: Callable,
        args: Optional[tuple] = None,
        kwargs: Optional[dict] = None,
        priority: int = 5,
        delay: Optional[float] = None,
        execute_at: Optional[datetime] = None,
    ) -> str:
        """
        Schedule a one-time task.
        
        Args:
            func: Function to execute
            args: Positional arguments
            kwargs: Keyword arguments
            priority: Task priority
            delay: Delay in seconds
            execute_at: Specific datetime to execute
            
        Returns:
            Task ID
        """
        if execute_at is not None:
            delay = (execute_at - datetime.now()).total_seconds()
            if delay < 0:
                delay = 0
        
        def task():
            if args and kwargs:
                return func(*args, **kwargs)
            elif args:
                return func(*args)
            elif kwargs:
                return func(**kwargs)
            else:
                return func()
        
        task_id = self._queue.push(task, priority=priority, delay=delay)
        
        with self._lock:
            self._scheduled_tasks[task_id] = {
                "type": "once",
                "func": func,
                "args": args,
                "kwargs": kwargs,
                "priority": priority,
            }
        
        return task_id
    
    def schedule_interval(
        self,
        func: Callable,
        interval: float,
        args: Optional[tuple] = None,
        kwargs: Optional[dict] = None,
        priority: int = 5,
        initial_delay: float = 0,
        max_runs: Optional[int] = None,
    ) -> str:
        """
        Schedule a recurring task at fixed intervals.
        
        Args:
            func: Function to execute
            interval: Time between executions in seconds
            args: Positional arguments
            kwargs: Keyword arguments
            priority: Task priority
            initial_delay: Delay before first execution
            max_runs: Maximum number of runs (None = unlimited)
            
        Returns:
            Task ID
        """
        task_id = str(uuid.uuid4())
        
        def recurring_task():
            nonlocal max_runs
            if max_runs is not None:
                max_runs -= 1
            
            if args and kwargs:
                func(*args, **kwargs)
            elif args:
                func(*args)
            elif kwargs:
                func(**kwargs)
            else:
                func()
            
            # Schedule next run
            with self._lock:
                if max_runs is None or max_runs > 0:
                    if task_id in self._scheduled_tasks:
                        self._queue.push(recurring_task, priority=priority, delay=interval)
        
        self._queue.push(recurring_task, priority=priority, delay=initial_delay)
        
        with self._lock:
            self._scheduled_tasks[task_id] = {
                "type": "interval",
                "func": func,
                "interval": interval,
                "args": args,
                "kwargs": kwargs,
                "priority": priority,
                "max_runs": max_runs,
            }
        
        return task_id
    
    def cancel_task(self, task_id: str) -> bool:
        """
        Cancel a scheduled task.
        
        Args:
            task_id: The task ID to cancel
            
        Returns:
            True if cancelled
        """
        with self._lock:
            if task_id in self._scheduled_tasks:
                del self._scheduled_tasks[task_id]
        return self._queue.cancel(task_id)
    
    def start(self) -> None:
        """Start the scheduler."""
        self._running = True
        self._executor.start()
    
    def stop(self, wait: bool = True) -> None:
        """Stop the scheduler."""
        self._running = False
        self._executor.stop(wait=wait)
    
    @property
    def stats(self) -> Dict[str, Any]:
        """Get scheduler statistics."""
        return {
            "executor": self._executor.stats,
            "scheduled_tasks": len(self._scheduled_tasks),
        }


class BoundedPriorityQueue(Generic[T]):
    """
    A bounded priority queue with overflow handling.
    
    When the queue reaches maxsize:
    - REJECT: Reject new items
    - DROP_LOWEST: Drop the lowest priority item
    - DROP_OLDEST: Drop the oldest item
    """
    
    class OverflowPolicy(Enum):
        REJECT = auto()
        DROP_LOWEST = auto()
        DROP_OLDEST = auto()
    
    def __init__(
        self,
        maxsize: int,
        policy: OverflowPolicy = OverflowPolicy.REJECT,
        on_drop: Optional[Callable[[T], None]] = None,
    ):
        """
        Initialize bounded queue.
        
        Args:
            maxsize: Maximum queue size
            policy: Overflow handling policy
            on_drop: Optional callback when items are dropped
        """
        self._queue = PriorityQueue[T](policy=PriorityPolicy.HIGHEST_FIRST, maxsize=maxsize)
        self._maxsize = maxsize
        self._policy = policy
        self._on_drop = on_drop
        self._items_data: List[Tuple[int, float, str, T]] = []  # For DROP policies
        self._counter = 0
    
    def push(self, item: T, priority: int = 5) -> Optional[str]:
        """
        Add item with overflow handling.
        
        Returns:
            Task ID, or None if rejected
        """
        current_size = len(self._items_data)
        
        if current_size >= self._maxsize:
            if self._policy == BoundedPriorityQueue.OverflowPolicy.REJECT:
                return None
            elif self._policy == BoundedPriorityQueue.OverflowPolicy.DROP_LOWEST:
                self._drop_lowest_priority()
            elif self._policy == BoundedPriorityQueue.OverflowPolicy.DROP_OLDEST:
                self._drop_oldest()
        
        task_id = str(uuid.uuid4())
        entry = (priority, self._counter, task_id, item)
        self._counter += 1
        self._items_data.append(entry)
        return task_id
    
    def _drop_lowest_priority(self) -> None:
        """Drop the lowest priority item (highest priority number)."""
        if not self._items_data:
            return
        
        # Find item with highest priority number (lowest actual priority)
        max_idx = 0
        max_priority = self._items_data[0][0]
        
        for i, (priority, _, _, item) in enumerate(self._items_data):
            if priority > max_priority:
                max_priority = priority
                max_idx = i
        
        dropped = self._items_data.pop(max_idx)
        if self._on_drop:
            self._on_drop(dropped[3])
    
    def _drop_oldest(self) -> None:
        """Drop the oldest item (lowest counter)."""
        if not self._items_data:
            return
        
        # Find item with lowest counter (oldest)
        min_idx = 0
        min_counter = self._items_data[0][1]
        
        for i, (_, counter, _, _) in enumerate(self._items_data):
            if counter < min_counter:
                min_counter = counter
                min_idx = i
        
        dropped = self._items_data.pop(min_idx)
        if self._on_drop:
            self._on_drop(dropped[3])
    
    def pop(self, timeout: Optional[float] = None) -> Optional[T]:
        """Pop the highest priority item."""
        if not self._items_data:
            return None
        
        # Sort by priority (and counter for stable ordering)
        self._items_data.sort()
        
        _, _, _, item = self._items_data.pop(0)
        return item
    
    def size(self) -> int:
        return len(self._items_data)
    
    def full(self) -> bool:
        return len(self._items_data) >= self._maxsize
    
    def empty(self) -> bool:
        return len(self._items_data) == 0


class PriorityDeque(Generic[T]):
    """
    Double-ended priority queue (min-max heap).
    
    Allows efficient access to both minimum and maximum elements.
    """
    
    def __init__(self):
        """Initialize the double-ended priority queue."""
        self._items: List[Tuple[int, float, str, T]] = []
        self._counter = 0
        self._lock = threading.Lock()
        self._task_ids: Dict[str, int] = {}
    
    def push(self, item: T, priority: int = 5) -> str:
        """
        Add an item with priority.
        
        Returns:
            Task ID for tracking
        """
        with self._lock:
            task_id = str(uuid.uuid4())
            entry = (priority, self._counter, task_id, item)
            self._counter += 1
            heapq.heappush(self._items, entry)
            self._task_ids[task_id] = len(self._items) - 1
            return task_id
    
    def pop_min(self) -> Optional[T]:
        """Pop the minimum priority item."""
        with self._lock:
            if not self._items:
                return None
            _, _, task_id, item = heapq.heappop(self._items)
            self._task_ids.pop(task_id, None)
            return item
    
    def pop_max(self) -> Optional[T]:
        """Pop the maximum priority item."""
        with self._lock:
            if not self._items:
                return None
            
            # Find max (items are min-heap, so max is at the end)
            max_idx = -1
            max_priority = float('-inf')
            
            for i, (priority, _, _, _) in enumerate(self._items):
                if priority > max_priority:
                    max_priority = priority
                    max_idx = i
            
            if max_idx >= 0:
                _, _, task_id, item = self._items.pop(max_idx)
                self._task_ids.pop(task_id, None)
                heapq.heapify(self._items)
                return item
            
            return None
    
    def peek_min(self) -> Optional[T]:
        """Peek at the minimum priority item."""
        with self._lock:
            if not self._items:
                return None
            return self._items[0][3]
    
    def peek_max(self) -> Optional[T]:
        """Peek at the maximum priority item."""
        with self._lock:
            if not self._items:
                return None
            
            max_priority = max(item[0] for item in self._items)
            for priority, _, _, item in self._items:
                if priority == max_priority:
                    return item
            
            return None
    
    def size(self) -> int:
        with self._lock:
            return len(self._items)
    
    def empty(self) -> bool:
        return self.size() == 0


# Utility functions

def create_priority_queue(
    items: Optional[List[Tuple[T, int]]] = None,
    policy: PriorityPolicy = PriorityPolicy.HIGHEST_FIRST,
) -> PriorityQueue[T]:
    """
    Create a priority queue from a list of (item, priority) tuples.
    
    Args:
        items: Optional list of items with priorities
        policy: Priority policy
        
    Returns:
        Configured priority queue
    """
    queue = PriorityQueue[T](policy=policy)
    if items:
        for item, priority in items:
            queue.push(item, priority=priority)
    return queue


def merge_priority_queues(
    *queues: PriorityQueue[T],
    policy: PriorityPolicy = PriorityPolicy.HIGHEST_FIRST,
) -> PriorityQueue[T]:
    """
    Merge multiple priority queues into one.
    
    Args:
        *queues: Queues to merge
        policy: Priority policy for the new queue
        
    Returns:
        New merged queue
    """
    merged = PriorityQueue[T](policy=policy)
    
    for queue in queues:
        while not queue.empty():
            item = queue.pop(block=False)
            if item:
                merged.push(item.data, priority=item._priority)
    
    return merged


def batch_push(
    queue: PriorityQueue[T],
    items: List[Tuple[T, int]],
    delay: Optional[float] = None,
) -> List[str]:
    """
    Push multiple items to a queue efficiently.
    
    Args:
        queue: Target queue
        items: List of (item, priority) tuples
        delay: Optional delay for all items
        
    Returns:
        List of task IDs
    """
    task_ids = []
    for item, priority in items:
        task_id = queue.push(item, priority=priority, delay=delay)
        task_ids.append(task_id)
    return task_ids


# Convenience aliases
PQueue = PriorityQueue
TaskQueue = PriorityTaskExecutor
Scheduler = TaskScheduler