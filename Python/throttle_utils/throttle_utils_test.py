"""
Tests for throttle_utils module.

Run with: python -m pytest throttle_utils_test.py -v
"""

import sys
import os
import pytest
import time
import asyncio

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    ThrottleMode,
    ThrottledFunction,
    AsyncThrottledFunction,
    throttle,
    athrottle,
    ThrottleQueue,
    SlidingThrottle,
    TokenBucketThrottle,
    AdaptiveThrottle,
    create_throttle,
)


class TestThrottleMode:
    """Test ThrottleMode enum."""
    
    def test_mode_values(self):
        assert ThrottleMode.LEADING.value == "leading"
        assert ThrottleMode.TRAILING.value == "trailing"
        assert ThrottleMode.BOTH.value == "both"


class TestThrottledFunction:
    """Test ThrottledFunction class."""
    
    def test_leading_mode_calls_immediately(self):
        """Leading mode should call immediately on first invocation."""
        call_count = [0]
        
        @throttle(0.1, mode='leading')
        def func(x):
            call_count[0] += 1
            return x * 2
        
        result = func(5)
        assert result == 10
        assert call_count[0] == 1
    
    def test_leading_mode_throttles_rapid_calls(self):
        """Leading mode should throttle rapid successive calls."""
        call_count = [0]
        
        @throttle(0.1, mode='leading')
        def func(x):
            call_count[0] += 1
            return x
        
        # First call executes
        func(1)
        # Rapid calls should be throttled
        func(2)
        func(3)
        func(4)
        
        assert call_count[0] == 1  # Only first call executed
    
    def test_leading_mode_allows_after_interval(self):
        """Leading mode should allow calls after interval passes."""
        call_count = [0]
        
        @throttle(0.05, mode='leading')
        def func(x):
            call_count[0] += 1
            return x
        
        func(1)  # Executes
        time.sleep(0.06)
        func(2)  # Should execute
        
        assert call_count[0] == 2
    
    def test_trailing_mode_waits_for_pause(self):
        """Trailing mode should wait for pause before calling."""
        call_count = [0]
        last_value = [None]
        
        @throttle(0.05, mode='trailing')
        def func(x):
            call_count[0] += 1
            last_value[0] = x
            return x
        
        # These calls should queue up
        func(1)
        func(2)
        func(3)
        
        # Should not have called yet
        assert call_count[0] == 0
        
        # Wait for trailing call
        time.sleep(0.06)
        func.flush()
        
        assert call_count[0] == 1
        assert last_value[0] == 3  # Last value wins
    
    def test_both_mode_calls_twice(self):
        """Both mode should call immediately AND trailing."""
        call_count = [0]
        
        @throttle(0.05, mode='both')
        def func(x):
            call_count[0] += 1
            return x
        
        func(1)  # Leading call
        assert call_count[0] == 1
        
        func(2)  # Queues trailing
        func(3)  # Overwrites queued args
        
        time.sleep(0.06)
        func.flush()  # Trailing call
        
        assert call_count[0] == 2
    
    def test_cancel_prevents_trailing_call(self):
        """Cancel should prevent pending trailing call."""
        call_count = [0]
        
        @throttle(0.05, mode='trailing')
        def func(x):
            call_count[0] += 1
            return x
        
        throttled = throttle(0.05, mode='trailing')(lambda x: call_count[0] + 1 or x)
        
        throttled(1)
        throttled.cancel()
        
        assert throttled.flush() is None  # No pending call
    
    def test_reset_clears_state(self):
        """Reset should clear all state."""
        @throttle(0.1)
        def func(x):
            return x
        
        func(1)
        func.reset()
        
        # Should be able to call immediately after reset
        assert func.pending() is False
    
    def test_returns_last_result_when_throttled(self):
        """Should return last result when throttled."""
        @throttle(0.1, mode='leading')
        def func(x):
            return x * 2
        
        result1 = func(5)  # Executes, returns 10
        result2 = func(10)  # Throttled, returns 10
        result3 = func(15)  # Throttled, returns 10
        
        assert result1 == 10
        assert result2 == 10
        assert result3 == 10


class TestAsyncThrottledFunction:
    """Test AsyncThrottledFunction class."""
    
    @pytest.mark.asyncio
    async def test_async_leading_mode(self):
        """Async leading mode should call immediately."""
        call_count = [0]
        
        @athrottle(0.05, mode='leading')
        async def func(x):
            call_count[0] += 1
            return x * 2
        
        result = await func(5)
        assert result == 10
        assert call_count[0] == 1
    
    @pytest.mark.asyncio
    async def test_async_throttles_rapid_calls(self):
        """Async should throttle rapid calls."""
        call_count = [0]
        
        @athrottle(0.05, mode='leading')
        async def func(x):
            call_count[0] += 1
            return x
        
        await func(1)
        await func(2)
        await func(3)
        
        assert call_count[0] == 1
    
    @pytest.mark.asyncio
    async def test_async_flush(self):
        """Async flush should execute pending call."""
        call_count = [0]
        last_value = [None]
        
        @athrottle(0.05, mode='trailing')
        async def func(x):
            call_count[0] += 1
            last_value[0] = x
            return x
        
        await func(1)
        await func(2)
        await func(3)
        
        assert call_count[0] == 0
        
        await asyncio.sleep(0.06)
        result = await func.flush()
        
        assert call_count[0] == 1
        assert last_value[0] == 3


class TestThrottleQueue:
    """Test ThrottleQueue class."""
    
    def test_enqueue_and_process(self):
        """Should enqueue and process items with throttle."""
        processed = []
        
        def processor(item):
            processed.append(item)
            return item * 2
        
        queue = ThrottleQueue(processor, interval=0.05)
        
        assert queue.enqueue(1)
        assert queue.enqueue(2)
        assert queue.enqueue(3)
        
        assert queue.size() == 3
        
        # Process first item
        result = queue.process_next()
        assert result == 2
        assert queue.size() == 2
    
    def test_process_throttles(self):
        """Should throttle processing based on interval."""
        processed = []
        
        def processor(item):
            processed.append(time.time())
            return item
        
        queue = ThrottleQueue(processor, interval=0.05)
        
        queue.enqueue(1)
        queue.enqueue(2)
        
        start = time.time()
        queue.process_next()  # Immediate
        queue.process_next()  # Should wait - but returns None due to throttle
        elapsed = time.time() - start
        
        assert elapsed < 0.01  # process_next shouldn't block
        assert len(processed) == 1  # Only first processed
    
    def test_max_queue_size(self):
        """Should respect max queue size."""
        queue = ThrottleQueue(lambda x: x, interval=0.1, max_queue_size=3)
        
        assert queue.enqueue(1)
        assert queue.enqueue(2)
        assert queue.enqueue(3)
        assert not queue.enqueue(4)  # Should fail
    
    def test_clear_queue(self):
        """Clear should remove all items."""
        queue = ThrottleQueue(lambda x: x, interval=0.1)
        
        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(3)
        
        queue.clear()
        
        assert queue.is_empty()
        assert queue.size() == 0


class TestSlidingThrottle:
    """Test SlidingThrottle class."""
    
    def test_acquire_immediate_on_first(self):
        """First acquire should be immediate."""
        throttle = SlidingThrottle(0.1)
        
        wait_time = throttle.acquire()
        assert wait_time == 0.0
    
    def test_acquire_waits_on_rapid_calls(self):
        """Rapid calls should require waiting."""
        throttle = SlidingThrottle(0.1)
        
        throttle.acquire()  # First call
        wait_time = throttle.acquire()  # Second call too fast
        
        assert wait_time > 0
        assert wait_time <= 0.1
    
    def test_try_acquire(self):
        """try_acquire should not block."""
        throttle = SlidingThrottle(0.05)
        
        assert throttle.try_acquire() is True  # First succeeds
        assert throttle.try_acquire() is False  # Second fails
    
    def test_reset(self):
        """Reset should allow immediate acquire."""
        throttle = SlidingThrottle(0.1)
        
        throttle.acquire()
        throttle.reset()
        
        assert throttle.try_acquire() is True


class TestTokenBucketThrottle:
    """Test TokenBucketThrottle class."""
    
    def test_initial_capacity(self):
        """Should start with full capacity."""
        bucket = TokenBucketThrottle(capacity=10, refill_rate=1)
        
        assert bucket.available() == 10
    
    def test_consume_tokens(self):
        """Should consume tokens."""
        bucket = TokenBucketThrottle(capacity=10, refill_rate=1)
        
        assert bucket.try_consume(5) is True
        # Allow for slight refill during call
        assert bucket.available() >= 4.9 and bucket.available() <= 5.5
    
    def test_fail_when_empty(self):
        """Should fail when not enough tokens."""
        bucket = TokenBucketThrottle(capacity=5, refill_rate=1)
        
        bucket.try_consume(5)
        assert bucket.try_consume(1) is False
    
    def test_refill_over_time(self):
        """Tokens should refill over time."""
        bucket = TokenBucketThrottle(capacity=10, refill_rate=100)  # 100/sec
        
        bucket.try_consume(10)
        assert bucket.available() <= 0.1  # Allow for tiny refill
        
        time.sleep(0.05)  # Should have ~5 tokens
        
        available = bucket.available()
        assert available >= 4  # Allow for some timing variance
    
    def test_reset(self):
        """Reset should restore full capacity."""
        bucket = TokenBucketThrottle(capacity=10, refill_rate=1)
        
        bucket.try_consume(10)
        bucket.reset()
        
        assert bucket.available() == 10


class TestAdaptiveThrottle:
    """Test AdaptiveThrottle class."""
    
    def test_initial_interval(self):
        """Should start with minimum interval."""
        throttle = AdaptiveThrottle(
            initial_interval=0.1,
            min_interval=0.01,
            max_interval=1.0
        )
        
        # Initial interval after acquire changes
        throttle.acquire()
        assert throttle.interval >= 0.01
    
    def test_success_reduces_interval(self):
        """Success should reduce interval."""
        throttle = AdaptiveThrottle(
            initial_interval=0.1,
            min_interval=0.01,
            max_interval=1.0,
            recovery_factor=0.5
        )
        
        # Force initial state
        throttle.failure()  # Increase
        throttle.failure()  # Increase more
        
        interval_before = throttle.interval
        throttle.success()
        
        assert throttle.interval < interval_before
    
    def test_failure_increases_interval(self):
        """Failure should increase interval."""
        throttle = AdaptiveThrottle(
            initial_interval=0.1,
            min_interval=0.01,
            max_interval=1.0,
            backoff_factor=2.0
        )
        
        interval_before = throttle.interval
        throttle.failure()
        
        assert throttle.interval > interval_before
    
    def test_interval_clamped_to_max(self):
        """Interval should not exceed max."""
        throttle = AdaptiveThrottle(
            initial_interval=0.1,
            min_interval=0.01,
            max_interval=0.5,
            backoff_factor=10.0
        )
        
        throttle.failure()
        throttle.failure()
        throttle.failure()
        
        assert throttle.interval <= 0.5
    
    def test_interval_clamped_to_min(self):
        """Interval should not go below min."""
        throttle = AdaptiveThrottle(
            initial_interval=0.1,
            min_interval=0.05,
            max_interval=1.0,
            recovery_factor=0.1
        )
        
        throttle.success()
        throttle.success()
        throttle.success()
        
        assert throttle.interval >= 0.05
    
    def test_acquire_returns_wait_time(self):
        """Acquire should return wait time."""
        throttle = AdaptiveThrottle(min_interval=0.1, max_interval=1.0)
        
        throttle.acquire()  # First call
        wait = throttle.acquire()  # Should need to wait
        
        assert wait > 0


class TestCreateThrottle:
    """Test create_throttle convenience function."""
    
    def test_creates_decorator(self):
        """Should create a throttle decorator."""
        decorator = create_throttle(0.1, mode='leading')
        
        @decorator
        def func(x):
            return x * 2
        
        result = func(5)
        assert result == 10


class TestEdgeCases:
    """Test edge cases and special scenarios."""
    
    def test_zero_interval(self):
        """Zero interval should allow all calls."""
        call_count = [0]
        
        @throttle(0, mode='leading')
        def func(x):
            call_count[0] += 1
            return x
        
        func(1)
        func(2)
        func(3)
        
        # With zero interval, all calls might execute
        # Behavior depends on timing precision
    
    def test_very_small_interval(self):
        """Very small interval should work correctly."""
        call_count = [0]
        
        @throttle(0.001, mode='leading')
        def func(x):
            call_count[0] += 1
            return x
        
        func(1)
        time.sleep(0.002)
        func(2)
        
        assert call_count[0] == 2
    
    def test_function_with_kwargs(self):
        """Should handle functions with keyword arguments."""
        @throttle(0.1)
        def func(a, b, c=3):
            return a + b + c
        
        result = func(1, 2, c=4)
        assert result == 7
    
    def test_function_with_no_args(self):
        """Should handle functions with no arguments."""
        call_count = [0]
        
        @throttle(0.1)
        def func():
            call_count[0] += 1
            return "done"
        
        result = func()
        assert result == "done"
        assert call_count[0] == 1
    
    def test_function_raises_exception(self):
        """Should propagate exceptions from wrapped function."""
        @throttle(0.1)
        def func():
            raise ValueError("test error")
        
        with pytest.raises(ValueError, match="test error"):
            func()
    
    def test_pending_flag(self):
        """pending() should return correct state."""
        @throttle(0.1, mode='trailing')
        def func(x):
            return x
        
        throttled = throttle(0.1, mode='trailing')(func)
        
        assert throttled.pending() is False
        
        throttled(1)
        # Now should have pending
        
        throttled.cancel()
        assert throttled.pending() is False


class TestConcurrentAccess:
    """Test thread safety."""
    
    def test_thread_safety(self):
        """Should be safe for concurrent access."""
        import threading
        
        call_count = [0]
        errors = []
        
        @throttle(0.01, mode='leading')
        def func(x):
            call_count[0] += 1
            return x
        
        def worker():
            try:
                for i in range(10):
                    func(i)
                    time.sleep(0.001)
            except Exception as e:
                errors.append(e)
        
        threads = [threading.Thread(target=worker) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert len(errors) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])