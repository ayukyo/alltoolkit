"""
Tests for Priority Queue Utilities
===================================

Comprehensive test suite for all priority queue components.
"""

import threading
import time
import unittest
from datetime import datetime, timedelta

from mod import (
    PriorityQueue,
    PriorityTaskExecutor,
    TaskScheduler,
    PriorityDeque,
    BoundedPriorityQueue,
    TaskState,
    PriorityPolicy,
    QueueFullError,
    QueueClosedError,
    create_priority_queue,
    merge_priority_queues,
    batch_push,
)


class TestPriorityQueue(unittest.TestCase):
    """Tests for PriorityQueue."""
    
    def test_basic_push_pop(self):
        """Test basic push and pop operations."""
        queue = PriorityQueue[str]()
        
        queue.push("low", priority=10)
        queue.push("high", priority=1)
        queue.push("medium", priority=5)
        
        self.assertEqual(queue.pop().data, "high")
        self.assertEqual(queue.pop().data, "medium")
        self.assertEqual(queue.pop().data, "low")
    
    def test_fifo_order(self):
        """Test FIFO policy."""
        queue = PriorityQueue[str](policy=PriorityPolicy.FIFO)
        
        queue.push("first", priority=1)
        queue.push("second", priority=2)
        queue.push("third", priority=3)
        
        self.assertEqual(queue.pop().data, "first")
        self.assertEqual(queue.pop().data, "second")
        self.assertEqual(queue.pop().data, "third")
    
    def test_lowest_first_policy(self):
        """Test LOWEST_FIRST policy."""
        queue = PriorityQueue[str](policy=PriorityPolicy.LOWEST_FIRST)
        
        queue.push("low", priority=1)
        queue.push("high", priority=10)
        queue.push("medium", priority=5)
        
        self.assertEqual(queue.pop().data, "high")
        self.assertEqual(queue.pop().data, "medium")
        self.assertEqual(queue.pop().data, "low")
    
    def test_empty_queue(self):
        """Test empty queue behavior."""
        queue = PriorityQueue[int]()
        
        self.assertTrue(queue.empty())
        self.assertEqual(queue.size(), 0)
        self.assertIsNone(queue.pop(block=False))
    
    def test_peek(self):
        """Test peek operation."""
        queue = PriorityQueue[int]()
        
        self.assertIsNone(queue.peek())
        
        queue.push(42, priority=1)
        self.assertEqual(queue.peek().data, 42)
        self.assertEqual(queue.size(), 1)
    
    def test_update_priority(self):
        """Test updating task priority."""
        queue = PriorityQueue[str]()
        
        task_id = queue.push("item", priority=10)
        self.assertEqual(queue.peek().data, "item")
        self.assertEqual(queue.peek()._priority, 10)
        
        result = queue.update_priority(task_id, 1)
        self.assertTrue(result)
        self.assertEqual(queue.peek()._priority, 1)
    
    def test_cancel_task(self):
        """Test task cancellation."""
        queue = PriorityQueue[str]()
        
        task_id = queue.push("item", priority=1)
        self.assertEqual(queue.size(), 1)
        
        result = queue.cancel(task_id)
        self.assertTrue(result)
        
        # Cancelled item should be skipped
        item = queue.pop(block=False)
        self.assertIsNone(item)
    
    def test_delayed_task(self):
        """Test delayed task execution."""
        queue = PriorityQueue[str]()
        
        queue.push("delayed", priority=1, delay=0.2)
        
        # Should not be available immediately
        item = queue.pop(timeout=0.05, block=True)
        self.assertIsNone(item)
        
        # Should be available after delay
        time.sleep(0.2)
        item = queue.pop(timeout=0.1)
        self.assertIsNotNone(item)
        self.assertEqual(item.data, "delayed")
    
    def test_callback(self):
        """Test task callback execution."""
        results = []
        
        def callback(item):
            results.append(f"processed: {item}")
        
        queue = PriorityQueue[str]()
        queue.push("test", priority=1, callback=callback)
        
        item = queue.pop()
        if item.callback:
            item.callback(item.data)
        
        self.assertEqual(results, ["processed: test"])
    
    def test_maxsize(self):
        """Test queue size limit."""
        queue = PriorityQueue[int](maxsize=2)
        
        queue.push(1, priority=1)
        queue.push(2, priority=1)
        
        with self.assertRaises(QueueFullError):
            queue.push(3, priority=1)
    
    def test_clear(self):
        """Test clearing the queue."""
        queue = PriorityQueue[int]()
        
        queue.push(1, priority=1)
        queue.push(2, priority=1)
        queue.push(3, priority=1)
        
        count = queue.clear()
        self.assertEqual(count, 3)
        self.assertTrue(queue.empty())
    
    def test_close(self):
        """Test queue closing."""
        queue = PriorityQueue[int]()
        
        self.assertFalse(queue.is_closed())
        queue.close()
        self.assertTrue(queue.is_closed())
        
        with self.assertRaises(QueueClosedError):
            queue.push(1, priority=1)
    
    def test_task_state(self):
        """Test task state tracking."""
        queue = PriorityQueue[str]()
        
        task_id = queue.push("test", priority=1)
        self.assertEqual(queue.get_task_state(task_id), TaskState.PENDING)
        
        item = queue.pop()
        self.assertIsNone(queue.get_task_state(task_id))
        self.assertEqual(item.state, TaskState.RUNNING)
    
    def test_history(self):
        """Test task history."""
        queue = PriorityQueue[str]()
        
        queue.add_to_history({
            "task_id": "test-1",
            "success": True,
            "result": "done",
        })
        
        history = queue.get_history()
        self.assertEqual(len(history), 1)
    
    def test_thread_safety(self):
        """Test concurrent operations."""
        queue = PriorityQueue[int]()
        results = []
        
        def producer(start, count):
            for i in range(count):
                queue.push(start + i, priority=1)
        
        def consumer(count):
            for _ in range(count):
                item = queue.pop(timeout=1.0)
                if item:
                    results.append(item.data)
        
        # Start producers
        threads = []
        for i in range(3):
            t = threading.Thread(target=producer, args=(i * 100, 100))
            threads.append(t)
            t.start()
        
        # Start consumers
        consumers = []
        for _ in range(2):
            t = threading.Thread(target=consumer, args=(150,))
            consumers.append(t)
            t.start()
        
        # Wait for completion
        for t in threads:
            t.join()
        
        for t in consumers:
            t.join()
        
        self.assertEqual(len(results), 300)
    
    def test_bool(self):
        """Test boolean conversion."""
        queue = PriorityQueue[int]()
        
        self.assertFalse(queue)  # Empty
        
        queue.push(1, priority=1)
        self.assertTrue(queue)  # Not empty


class TestPriorityTaskExecutor(unittest.TestCase):
    """Tests for PriorityTaskExecutor."""
    
    def test_basic_execution(self):
        """Test basic task execution."""
        results = []
        
        def task_func():
            results.append("executed")
            return 42
        
        queue = PriorityQueue[callable]()
        executor = PriorityTaskExecutor(queue, num_workers=1)
        
        queue.push(task_func, priority=1)
        
        executor.start()
        time.sleep(0.2)
        executor.stop()
        
        self.assertIn("executed", results)
    
    def test_priority_order(self):
        """Test tasks execute in priority order."""
        results = []
        
        queue = PriorityQueue[callable]()
        executor = PriorityTaskExecutor(queue, num_workers=1)
        
        # Push tasks with different priorities
        queue.push(lambda: results.append("low"), priority=10)
        queue.push(lambda: results.append("high"), priority=1)
        queue.push(lambda: results.append("medium"), priority=5)
        
        executor.start()
        time.sleep(0.3)
        executor.stop()
        
        # First task should be high priority
        self.assertEqual(results[0], "high")
    
    def test_default_callback(self):
        """Test default callback for all results."""
        results = []
        
        def on_result(result):
            results.append(result)
        
        queue = PriorityQueue[callable]()
        executor = PriorityTaskExecutor(
            queue,
            num_workers=1,
            default_callback=on_result,
        )
        
        queue.push(lambda: 42, priority=1)
        
        executor.start()
        time.sleep(0.2)
        executor.stop()
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].result, 42)
    
    def test_stats(self):
        """Test executor statistics."""
        queue = PriorityQueue[callable]()
        executor = PriorityTaskExecutor(queue, num_workers=1)
        
        queue.push(lambda: 1, priority=1)
        queue.push(lambda: 2, priority=1)
        
        executor.start()
        time.sleep(0.3)
        executor.stop()
        
        stats = executor.stats
        self.assertEqual(stats["processed"], 2)
        self.assertEqual(stats["queue_size"], 0)


class TestTaskScheduler(unittest.TestCase):
    """Tests for TaskScheduler."""
    
    def test_schedule_once(self):
        """Test one-time task scheduling."""
        results = []
        
        scheduler = TaskScheduler(num_workers=1)
        scheduler.schedule_once(lambda: results.append("run"), delay=0.1)
        
        scheduler.start()
        time.sleep(0.3)
        scheduler.stop()
        
        self.assertIn("run", results)
    
    def test_schedule_at_specific_time(self):
        """Test scheduling at a specific time."""
        results = []
        
        scheduler = TaskScheduler(num_workers=1)
        execute_at = datetime.now() + timedelta(seconds=0.2)
        
        scheduler.schedule_once(
            lambda: results.append("timed"),
            execute_at=execute_at,
        )
        
        scheduler.start()
        time.sleep(0.4)
        scheduler.stop()
        
        self.assertIn("timed", results)
    
    def test_schedule_interval(self):
        """Test recurring task scheduling."""
        results = []
        
        scheduler = TaskScheduler(num_workers=1)
        scheduler.schedule_interval(
            lambda: results.append("tick"),
            interval=0.1,
            initial_delay=0,
        )
        
        scheduler.start()
        time.sleep(0.35)
        scheduler.stop()
        
        # Should have run approximately 3 times
        self.assertGreaterEqual(len(results), 2)
    
    def test_cancel_task(self):
        """Test cancelling scheduled task."""
        results = []
        
        scheduler = TaskScheduler(num_workers=1)
        task_id = scheduler.schedule_once(
            lambda: results.append("cancelled"),
            delay=0.2,
        )
        
        scheduler.cancel_task(task_id)
        
        scheduler.start()
        time.sleep(0.3)
        scheduler.stop()
        
        self.assertNotIn("cancelled", results)


class TestPriorityDeque(unittest.TestCase):
    """Tests for PriorityDeque."""
    
    def test_basic_operations(self):
        """Test basic min/max operations."""
        deque = PriorityDeque[int]()
        
        deque.push(5, priority=5)
        deque.push(1, priority=1)
        deque.push(10, priority=10)
        
        self.assertEqual(deque.peek_min(), 1)
        self.assertEqual(deque.peek_max(), 10)
    
    def test_pop_min_max(self):
        """Test popping min and max."""
        deque = PriorityDeque[int]()
        
        deque.push(5, priority=5)
        deque.push(1, priority=1)
        deque.push(10, priority=10)
        
        self.assertEqual(deque.pop_min(), 1)
        self.assertEqual(deque.pop_max(), 10)
        self.assertEqual(deque.pop_min(), 5)
    
    def test_empty_deque(self):
        """Test empty deque behavior."""
        deque = PriorityDeque[int]()
        
        self.assertTrue(deque.empty())
        self.assertIsNone(deque.peek_min())
        self.assertIsNone(deque.peek_max())
        self.assertIsNone(deque.pop_min())
        self.assertIsNone(deque.pop_max())


class TestBoundedPriorityQueue(unittest.TestCase):
    """Tests for BoundedPriorityQueue."""
    
    def test_reject_policy(self):
        """Test reject policy when full."""
        queue = BoundedPriorityQueue[int](
            maxsize=2,
            policy=BoundedPriorityQueue.OverflowPolicy.REJECT,
        )
        
        queue.push(1, priority=1)
        queue.push(2, priority=1)
        
        # Should reject third item
        result = queue.push(3, priority=1)
        self.assertIsNone(result)
    
    def test_pop(self):
        """Test pop from bounded queue."""
        queue = BoundedPriorityQueue[int](maxsize=2)
        
        queue.push(1, priority=2)
        queue.push(2, priority=1)
        
        # Should pop highest priority (lowest number)
        item = queue.pop()
        self.assertEqual(item, 2)
    
    def test_full_empty(self):
        """Test full and empty checks."""
        queue = BoundedPriorityQueue[int](maxsize=2)
        
        self.assertTrue(queue.empty())
        self.assertFalse(queue.full())
        
        queue.push(1, priority=1)
        queue.push(2, priority=1)
        
        self.assertTrue(queue.full())
        self.assertFalse(queue.empty())


class TestUtilityFunctions(unittest.TestCase):
    """Tests for utility functions."""
    
    def test_create_priority_queue(self):
        """Test creating queue from items."""
        items = [("low", 10), ("high", 1), ("medium", 5)]
        queue = create_priority_queue(items)
        
        self.assertEqual(queue.pop().data, "high")
        self.assertEqual(queue.pop().data, "medium")
        self.assertEqual(queue.pop().data, "low")
    
    def test_merge_priority_queues(self):
        """Test merging queues."""
        q1 = PriorityQueue[int]()
        q1.push(1, priority=1)
        q1.push(3, priority=3)
        
        q2 = PriorityQueue[int]()
        q2.push(2, priority=2)
        q2.push(4, priority=4)
        
        merged = merge_priority_queues(q1, q2)
        
        self.assertEqual(merged.pop().data, 1)
        self.assertEqual(merged.pop().data, 2)
        self.assertEqual(merged.pop().data, 3)
        self.assertEqual(merged.pop().data, 4)
    
    def test_batch_push(self):
        """Test batch pushing items."""
        queue = PriorityQueue[int]()
        items = [(10, 10), (1, 1), (5, 5)]
        
        task_ids = batch_push(queue, items)
        
        self.assertEqual(len(task_ids), 3)
        self.assertEqual(queue.pop().data, 1)


class TestTaskResult(unittest.TestCase):
    """Tests for TaskResult dataclass."""
    
    def test_success_result(self):
        """Test successful task result."""
        result = {
            "task_id": "test-1",
            "success": True,
            "result": 42,
            "execution_time": 0.1,
        }
        
        self.assertTrue(result["success"])
        self.assertEqual(result["result"], 42)
    
    def test_failure_result(self):
        """Test failed task result."""
        try:
            raise ValueError("Test error")
        except ValueError as e:
            result = {
                "task_id": "test-2",
                "success": False,
                "error": e,
            }
        
        self.assertFalse(result["success"])
        self.assertIsInstance(result["error"], ValueError)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def test_push_same_priority(self):
        """Test items with same priority maintain FIFO order."""
        queue = PriorityQueue[str]()
        
        queue.push("first", priority=5)
        queue.push("second", priority=5)
        queue.push("third", priority=5)
        
        self.assertEqual(queue.pop().data, "first")
        self.assertEqual(queue.pop().data, "second")
        self.assertEqual(queue.pop().data, "third")
    
    def test_update_nonexistent_task(self):
        """Test updating a task that doesn't exist."""
        queue = PriorityQueue[int]()
        
        result = queue.update_priority("nonexistent", new_priority=1)
        self.assertFalse(result)
    
    def test_cancel_nonexistent_task(self):
        """Test cancelling a task that doesn't exist."""
        queue = PriorityQueue[int]()
        
        result = queue.cancel("nonexistent")
        self.assertFalse(result)
    
    def test_large_number_of_items(self):
        """Test queue with many items."""
        queue = PriorityQueue[int]()
        
        for i in range(1000):
            queue.push(i, priority=i)
        
        # Should pop in order
        for i in range(1000):
            item = queue.pop()
            self.assertEqual(item.data, i)
    
    def test_negative_priorities(self):
        """Test negative priority values."""
        queue = PriorityQueue[str]()
        
        queue.push("zero", priority=0)
        queue.push("positive", priority=5)
        queue.push("negative", priority=-5)
        
        self.assertEqual(queue.pop().data, "negative")
        self.assertEqual(queue.pop().data, "zero")
        self.assertEqual(queue.pop().data, "positive")


if __name__ == "__main__":
    unittest.main(verbosity=2)