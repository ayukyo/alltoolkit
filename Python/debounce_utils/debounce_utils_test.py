"""
AllToolkit - Python Debounce Utilities Tests

Comprehensive tests for debounce and throttle utilities.
"""

import sys
import os
import time
import threading
import unittest

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    Debouncer,
    Throttler,
    debounce,
    throttle,
    MultiKeyDebouncer,
    MultiKeyThrottler,
    DebouncedFunction,
    ThrottledFunction,
    DebounceStats,
    generate_debounce_key,
)


class TestDebounceStats(unittest.TestCase):
    """Test DebounceStats class."""
    
    def test_initial_stats(self):
        """Test initial statistics are zero."""
        stats = DebounceStats()
        self.assertEqual(stats.total_calls, 0)
        self.assertEqual(stats.executed_calls, 0)
        self.assertEqual(stats.cancelled_calls, 0)
        self.assertEqual(stats.flushed_calls, 0)
        self.assertEqual(stats.pending_calls, 0)
    
    def test_record_operations(self):
        """Test recording various operations."""
        stats = DebounceStats()
        stats.record_call()
        stats.record_call()
        stats.record_execution()
        stats.record_cancellation()
        stats.record_flush()
        
        self.assertEqual(stats.total_calls, 2)
        self.assertEqual(stats.executed_calls, 1)
        self.assertEqual(stats.cancelled_calls, 1)
        self.assertEqual(stats.flushed_calls, 1)
    
    def test_suppression_rate(self):
        """Test suppression rate calculation."""
        stats = DebounceStats()
        
        # No calls
        self.assertEqual(stats.suppression_rate, 0.0)
        
        # 50% suppression
        stats.total_calls = 10
        stats.executed_calls = 5
        self.assertEqual(stats.suppression_rate, 0.5)
        
        # 90% suppression
        stats.executed_calls = 1
        self.assertAlmostEqual(stats.suppression_rate, 0.9)
    
    def test_to_dict(self):
        """Test converting stats to dictionary."""
        stats = DebounceStats()
        stats.total_calls = 100
        stats.executed_calls = 20
        
        result = stats.to_dict()
        self.assertEqual(result['total_calls'], 100)
        self.assertEqual(result['executed_calls'], 20)
        self.assertIn('suppression_rate', result)
    
    def test_reset(self):
        """Test resetting statistics."""
        stats = DebounceStats()
        stats.record_call()
        stats.record_execution()
        stats.reset()
        
        self.assertEqual(stats.total_calls, 0)
        self.assertEqual(stats.executed_calls, 0)


class TestDebouncer(unittest.TestCase):
    """Test Debouncer class."""
    
    def test_basic_debounce(self):
        """Test basic debounce functionality."""
        results = []
        
        def callback(value):
            results.append(value)
        
        debouncer = Debouncer(wait_seconds=0.1)
        
        debouncer.call(callback, "a")
        debouncer.call(callback, "b")
        debouncer.call(callback, "c")
        
        # Nothing executed yet
        self.assertEqual(len(results), 0)
        
        # Wait for debounce
        time.sleep(0.2)
        
        # Only last value executed
        self.assertEqual(results, ["c"])
    
    def test_leading_edge(self):
        """Test leading edge execution."""
        results = []
        
        def callback(value):
            results.append(value)
        
        debouncer = Debouncer(wait_seconds=0.1, leading=True, trailing=False)
        
        result = debouncer.call(callback, "first")
        self.assertEqual(result, "first")  # Leading edge returns immediately
        self.assertEqual(results, ["first"])
        
        # Subsequent calls within wait time don't execute
        debouncer.call(callback, "second")
        debouncer.call(callback, "third")
        
        time.sleep(0.2)
        self.assertEqual(results, ["first"])  # No trailing execution
    
    def test_leading_and_trailing(self):
        """Test both leading and trailing edge."""
        results = []
        
        def callback(value):
            results.append(value)
            return value
        
        debouncer = Debouncer(wait_seconds=0.1, leading=True, trailing=True)
        
        # First call executes immediately (leading)
        result = debouncer.call(callback, "a")
        self.assertEqual(result, "a")
        self.assertEqual(results, ["a"])
        
        # Reset to test sequence
        results.clear()
        debouncer.reset()
        
        debouncer.call(callback, "b")
        debouncer.call(callback, "c")
        
        time.sleep(0.15)
        
        # Leading executes first call, trailing executes last
        self.assertEqual(len(results), 2)
    
    def test_cancel(self):
        """Test cancelling pending execution."""
        results = []
        
        def callback(value):
            results.append(value)
        
        debouncer = Debouncer(wait_seconds=0.2)
        
        debouncer.call(callback, "test")
        cancelled = debouncer.cancel()
        
        self.assertTrue(cancelled)
        
        time.sleep(0.3)
        self.assertEqual(len(results), 0)  # Nothing executed after cancel
    
    def test_flush(self):
        """Test flushing pending execution."""
        results = []
        
        def callback(value):
            results.append(value)
            return value
        
        debouncer = Debouncer(wait_seconds=0.5)
        
        debouncer.call(callback, "immediate")
        
        # Flush executes immediately
        result = debouncer.flush()
        
        self.assertEqual(result, "immediate")
        self.assertEqual(results, ["immediate"])
    
    def test_max_wait(self):
        """Test max_wait forces execution."""
        results = []
        
        def callback(value):
            results.append(value)
        
        debouncer = Debouncer(wait_seconds=0.1, max_wait=0.3)
        
        # Multiple calls
        start = time.time()
        for i in range(5):
            debouncer.call(callback, f"call_{i}")
            time.sleep(0.08)  # Keep within wait_seconds
        
        # Wait for max_wait to trigger
        time.sleep(0.25)
        
        # Should have executed due to max_wait
        self.assertTrue(len(results) >= 1)
    
    def test_is_pending(self):
        """Test checking pending state."""
        debouncer = Debouncer(wait_seconds=0.2)
        
        self.assertFalse(debouncer.is_pending)
        
        debouncer.call(lambda x: x, "test")
        self.assertTrue(debouncer.is_pending)
        
        debouncer.cancel()
        self.assertFalse(debouncer.is_pending)
    
    def test_stats_tracking(self):
        """Test statistics tracking."""
        debouncer = Debouncer(wait_seconds=0.1)
        
        # Multiple calls
        for i in range(5):
            debouncer.call(lambda: i)
        
        time.sleep(0.2)
        
        stats = debouncer.stats
        self.assertEqual(stats.total_calls, 5)
        self.assertEqual(stats.executed_calls, 1)  # Only trailing executed
    
    def test_thread_safety(self):
        """Test concurrent calls are handled safely."""
        results = []
        debouncer = Debouncer(wait_seconds=0.05)
        
        def callback(value):
            results.append(value)
        
        def make_call(value):
            debouncer.call(callback, value)
        
        threads = []
        for i in range(10):
            t = threading.Thread(target=make_call, args=(i,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        time.sleep(0.1)
        
        # Should only have one execution
        self.assertEqual(len(results), 1)
    
    def test_invalid_wait_seconds(self):
        """Test invalid wait_seconds raises error."""
        with self.assertRaises(ValueError):
            Debouncer(wait_seconds=0)
        
        with self.assertRaises(ValueError):
            Debouncer(wait_seconds=-1)
    
    def test_invalid_max_wait(self):
        """Test invalid max_wait raises error."""
        with self.assertRaises(ValueError):
            Debouncer(wait_seconds=0.1, max_wait=0)
        
        with self.assertRaises(ValueError):
            Debouncer(wait_seconds=0.1, max_wait=-1)


class TestThrottler(unittest.TestCase):
    """Test Throttler class."""
    
    def test_basic_throttle(self):
        """Test basic throttle functionality."""
        results = []
        
        def callback(value):
            results.append(value)
        
        throttler = Throttler(interval_seconds=0.2)
        
        throttler.call(callback, "a")  # Executes immediately (leading)
        throttler.call(callback, "b")  # Dropped
        throttler.call(callback, "c")  # Dropped
        
        self.assertEqual(results, ["a"])
        
        # Wait for interval
        time.sleep(0.25)
        
        throttler.call(callback, "d")  # Executes now
        self.assertEqual(results, ["a", "d"])
    
    def test_trailing_throttle(self):
        """Test trailing edge throttling."""
        results = []
        
        def callback(value):
            results.append(value)
        
        throttler = Throttler(
            interval_seconds=0.1,
            leading=False,
            trailing=True
        )
        
        throttler.call(callback, "a")
        throttler.call(callback, "b")
        throttler.call(callback, "c")
        
        # Nothing executes immediately (no leading)
        self.assertEqual(len(results), 0)
        
        # Wait for trailing to execute
        time.sleep(0.15)
        
        # Last call executes on trailing edge
        self.assertEqual(results, ["c"])
    
    def test_is_throttled(self):
        """Test checking throttled state."""
        throttler = Throttler(interval_seconds=0.5)
        
        self.assertFalse(throttler.is_throttled)
        
        throttler.call(lambda: None)
        self.assertTrue(throttler.is_throttled)
        
        time.sleep(0.6)
        self.assertFalse(throttler.is_throttled)
    
    def test_time_until_next(self):
        """Test time until next execution."""
        throttler = Throttler(interval_seconds=0.5)
        
        throttler.call(lambda: None)
        
        remaining = throttler.time_until_next
        self.assertTrue(0 < remaining <= 0.5)
        
        time.sleep(0.3)
        remaining = throttler.time_until_next
        self.assertTrue(0 < remaining < 0.3)
    
    def test_throttle_cancel(self):
        """Test cancelling trailing execution."""
        results = []
        
        def callback(value):
            results.append(value)
        
        throttler = Throttler(
            interval_seconds=0.2,
            leading=False,
            trailing=True
        )
        
        throttler.call(callback, "test")
        cancelled = throttler.cancel()
        
        self.assertTrue(cancelled)
        
        time.sleep(0.3)
        self.assertEqual(len(results), 0)
    
    def test_throttle_flush(self):
        """Test flushing pending trailing call."""
        results = []
        
        def callback(value):
            results.append(value)
            return value
        
        throttler = Throttler(
            interval_seconds=0.5,
            leading=False,
            trailing=True
        )
        
        throttler.call(callback, "immediate")
        
        result = throttler.flush()
        
        self.assertEqual(result, "immediate")
        self.assertEqual(results, ["immediate"])
    
    def test_invalid_interval(self):
        """Test invalid interval raises error."""
        with self.assertRaises(ValueError):
            Throttler(interval_seconds=0)
        
        with self.assertRaises(ValueError):
            Throttler(interval_seconds=-1)


class TestDebounceDecorator(unittest.TestCase):
    """Test debounce decorator."""
    
    def test_debounce_decorator(self):
        """Test decorated function is debounced."""
        results = []
        
        @debounce(wait_seconds=0.1)
        def add_value(value):
            results.append(value)
        
        add_value("a")
        add_value("b")
        add_value("c")
        
        time.sleep(0.2)
        
        self.assertEqual(results, ["c"])
    
    def test_decorator_cancel(self):
        """Test decorated function has cancel method."""
        results = []
        
        @debounce(wait_seconds=0.2)
        def add_value(value):
            results.append(value)
        
        add_value("test")
        add_value.cancel()
        
        time.sleep(0.3)
        self.assertEqual(len(results), 0)
    
    def test_decorator_flush(self):
        """Test decorated function has flush method."""
        results = []
        
        @debounce(wait_seconds=0.5)
        def add_value(value):
            results.append(value)
            return value
        
        add_value("test")
        result = add_value.flush()
        
        self.assertEqual(result, "test")
        self.assertEqual(results, ["test"])


class TestThrottleDecorator(unittest.TestCase):
    """Test throttle decorator."""
    
    def test_throttle_decorator(self):
        """Test decorated function is throttled."""
        results = []
        
        @throttle(interval_seconds=0.2)
        def add_value(value):
            results.append(value)
        
        add_value("a")  # Executes
        add_value("b")  # Dropped
        add_value("c")  # Dropped
        
        self.assertEqual(results, ["a"])
        
        time.sleep(0.25)
        add_value("d")  # Executes
        
        self.assertEqual(results, ["a", "d"])
    
    def test_decorator_has_cancel_and_flush(self):
        """Test decorated function has cancel and flush methods."""
        @throttle(interval_seconds=0.2, trailing=True)
        def test_func():
            return "test"
        
        # Should have these methods
        self.assertTrue(hasattr(test_func, 'cancel'))
        self.assertTrue(hasattr(test_func, 'flush'))


class TestMultiKeyDebouncer(unittest.TestCase):
    """Test MultiKeyDebouncer class."""
    
    def test_independent_keys(self):
        """Test different keys are debounced independently."""
        results_a = []
        results_b = []
        
        def callback_a(value):
            results_a.append(value)
        
        def callback_b(value):
            results_b.append(value)
        
        debouncer = MultiKeyDebouncer(wait_seconds=0.1)
        
        debouncer.call("key_a", callback_a, "a1")
        debouncer.call("key_a", callback_a, "a2")
        debouncer.call("key_b", callback_b, "b1")
        
        time.sleep(0.15)
        
        # Each key debounces independently
        self.assertEqual(results_a, ["a2"])
        self.assertEqual(results_b, ["b1"])
    
    def test_cancel_specific_key(self):
        """Test cancelling specific key."""
        results = []
        
        def callback(value):
            results.append(value)
        
        debouncer = MultiKeyDebouncer(wait_seconds=0.2)
        
        debouncer.call("key1", callback, "value1")
        debouncer.call("key2", callback, "value2")
        
        debouncer.cancel("key1")
        
        time.sleep(0.25)
        
        # key2 executes, key1 was cancelled
        self.assertEqual(results, ["value2"])
    
    def test_cancel_all(self):
        """Test cancelling all keys."""
        results = []
        
        def callback(value):
            results.append(value)
        
        debouncer = MultiKeyDebouncer(wait_seconds=0.2)
        
        debouncer.call("key1", callback, "value1")
        debouncer.call("key2", callback, "value2")
        
        count = debouncer.cancel_all()
        self.assertEqual(count, 2)
        
        time.sleep(0.25)
        self.assertEqual(len(results), 0)
    
    def test_flush_all(self):
        """Test flushing all pending executions."""
        results = []
        
        def callback(value):
            results.append(value)
            return value
        
        debouncer = MultiKeyDebouncer(wait_seconds=0.5)
        
        debouncer.call("key1", callback, "value1")
        debouncer.call("key2", callback, "value2")
        
        flushed = debouncer.flush_all()
        
        self.assertEqual(len(flushed), 2)
        self.assertEqual(set(results), {"value1", "value2"})
    
    def test_pending_keys(self):
        """Test getting pending keys."""
        debouncer = MultiKeyDebouncer(wait_seconds=0.5)
        
        debouncer.call("key1", lambda: None)
        debouncer.call("key2", lambda: None)
        
        pending = debouncer.pending_keys()
        self.assertEqual(set(pending), {"key1", "key2"})


class TestMultiKeyThrottler(unittest.TestCase):
    """Test MultiKeyThrottler class."""
    
    def test_independent_keys(self):
        """Test different keys are throttled independently."""
        results_a = []
        results_b = []
        
        def callback_a(value):
            results_a.append(value)
        
        def callback_b(value):
            results_b.append(value)
        
        throttler = MultiKeyThrottler(interval_seconds=0.1)
        
        throttler.call("key_a", callback_a, "a1")  # Executes
        throttler.call("key_a", callback_a, "a2")  # Dropped
        throttler.call("key_b", callback_b, "b1")  # Executes (different key)
        
        self.assertEqual(results_a, ["a1"])
        self.assertEqual(results_b, ["b1"])
    
    def test_is_throttled_per_key(self):
        """Test checking throttled state per key."""
        throttler = MultiKeyThrottler(interval_seconds=0.5)
        
        throttler.call("key1", lambda: None)
        
        self.assertTrue(throttler.is_throttled("key1"))
        self.assertFalse(throttler.is_throttled("key2"))  # Different key
    
    def test_time_until_next_per_key(self):
        """Test time until next execution per key."""
        throttler = MultiKeyThrottler(interval_seconds=0.5)
        
        throttler.call("key1", lambda: None)
        throttler.call("key2", lambda: None)
        
        # Both keys should have remaining time
        self.assertTrue(throttler.time_until_next("key1") > 0)
        self.assertTrue(throttler.time_until_next("key2") > 0)


class TestDebouncedFunction(unittest.TestCase):
    """Test DebouncedFunction wrapper."""
    
    def test_basic_usage(self):
        """Test basic debounced function usage."""
        results = []
        
        def save(data):
            results.append(data)
            return data
        
        debounced = DebouncedFunction(save, wait_seconds=0.1)
        
        debounced("data1")
        debounced("data2")
        
        time.sleep(0.2)
        
        self.assertEqual(results, ["data2"])
    
    def test_context_manager(self):
        """Test context manager flushes on exit."""
        results = []
        
        def save(data):
            results.append(data)
            return data
        
        with DebouncedFunction(save, wait_seconds=0.5) as debounced:
            debounced("data1")
            debounced("data2")
        
        # Context exit flushes pending
        self.assertEqual(len(results), 1)


class TestThrottledFunction(unittest.TestCase):
    """Test ThrottledFunction wrapper."""
    
    def test_basic_usage(self):
        """Test basic throttled function usage."""
        results = []
        
        def send(data):
            results.append(data)
            return data
        
        throttled = ThrottledFunction(send, interval_seconds=0.2)
        
        throttled("data1")  # Executes
        throttled("data2")  # Dropped
        throttled("data3")  # Dropped
        
        self.assertEqual(results, ["data1"])
    
    def test_context_manager(self):
        """Test context manager flushes on exit."""
        results = []
        
        def send(data):
            results.append(data)
            return data
        
        with ThrottledFunction(
            send,
            interval_seconds=0.2,
            leading=False,
            trailing=True
        ) as throttled:
            throttled("data1")
        
        # Context exit flushes trailing
        self.assertEqual(results, ["data1"])
    
    def test_time_until_next(self):
        """Test time_until_next property."""
        throttled = ThrottledFunction(lambda: None, interval_seconds=1.0)
        
        throttled()
        
        remaining = throttled.time_until_next
        self.assertTrue(0 < remaining <= 1.0)


class TestGenerateDebounceKey(unittest.TestCase):
    """Test generate_debounce_key function."""
    
    def test_key_generation(self):
        """Test key is generated from arguments."""
        key1 = generate_debounce_key("a", "b")
        key2 = generate_debounce_key("a", "b")
        key3 = generate_debounce_key("a", "c")
        
        # Same args produce same key
        self.assertEqual(key1, key2)
        
        # Different args produce different key
        self.assertNotEqual(key1, key3)
    
    def test_key_with_kwargs(self):
        """Test key generation with keyword arguments."""
        key1 = generate_debounce_key("a", b=1)
        key2 = generate_debounce_key("a", b=2)
        
        self.assertNotEqual(key1, key2)
    
    def test_key_length(self):
        """Test key has reasonable length."""
        key = generate_debounce_key("arg1", "arg2", kwarg="value")
        
        # Hash is truncated to 16 characters
        self.assertEqual(len(key), 16)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and special scenarios."""
    
    def test_debounce_with_exception(self):
        """Test debounced function with exception."""
        debouncer = Debouncer(wait_seconds=0.1)
        
        def failing_func():
            raise ValueError("Test error")
        
        debouncer.call(failing_func)
        
        # Should raise on trailing execution
        with self.assertRaises(ValueError):
            time.sleep(0.2)
    
    def test_debounce_zero_calls(self):
        """Test debouncer with no calls."""
        debouncer = Debouncer(wait_seconds=0.1)
        
        # No pending
        self.assertFalse(debouncer.is_pending)
        
        # Cancel returns False
        self.assertFalse(debouncer.cancel())
        
        # Flush returns None
        self.assertIsNone(debouncer.flush())
    
    def test_throttle_zero_calls(self):
        """Test throttler with no calls."""
        throttler = Throttler(interval_seconds=0.1)
        
        # Not throttled
        self.assertFalse(throttler.is_throttled)
        
        # Cancel returns False
        self.assertFalse(throttler.cancel())
        
        # Flush returns None
        self.assertIsNone(throttler.flush())
    
    def test_debounce_with_none_result(self):
        """Test debounced function returning None."""
        results = []
        
        def returns_none():
            results.append("called")
            return None
        
        debouncer = Debouncer(wait_seconds=0.1)
        
        debouncer.call(returns_none)
        time.sleep(0.2)
        
        # Function was called
        self.assertEqual(results, ["called"])
    
    def test_rapid_debounce_calls(self):
        """Test very rapid calls."""
        results = []
        
        def callback(value):
            results.append(value)
        
        debouncer = Debouncer(wait_seconds=0.01)
        
        for i in range(100):
            debouncer.call(callback, i)
        
        time.sleep(0.05)
        
        # Only last call executes
        self.assertEqual(results, [99])


if __name__ == "__main__":
    unittest.main(verbosity=2)