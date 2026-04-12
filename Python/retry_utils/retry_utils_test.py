"""
AllToolkit - Python Retry Utilities Test Suite

Comprehensive test coverage for retry_utils module.
"""

import unittest
import time
import threading
from typing import List
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    RetryError,
    RetryStats,
    RetryAttempt,
    RetryConfig,
    RetryExecutor,
    retry,
    retry_with_config,
    BackoffStrategies,
    get_global_stats,
    reset_global_stats,
    TransientError,
    NetworkError,
    ServiceUnavailableError,
    RateLimitError,
    RETRY_NETWORK,
    RETRY_DATABASE,
    RETRY_API,
    RETRY_QUICK,
)


class TestRetryError(unittest.TestCase):
    """Test RetryError exception."""
    
    def test_basic_error(self):
        """Test basic RetryError creation."""
        error = RetryError("Test error")
        self.assertIn("Test error", str(error))
        self.assertIsNone(error.last_exception)
        self.assertEqual(error.attempts, 0)
        self.assertEqual(error.total_time, 0.0)
    
    def test_error_with_exception(self):
        """Test RetryError with last exception."""
        original = ValueError("Original error")
        error = RetryError("All attempts failed", last_exception=original, attempts=3, total_time=5.5)
        self.assertEqual(error.last_exception, original)
        self.assertEqual(error.attempts, 3)
        self.assertEqual(error.total_time, 5.5)
        self.assertIn("ValueError", str(error))


class TestRetryStats(unittest.TestCase):
    """Test RetryStats class."""
    
    def test_initial_state(self):
        """Test initial stats state."""
        stats = RetryStats()
        self.assertEqual(stats.total_calls, 0)
        self.assertEqual(stats.successful_calls, 0)
        self.assertEqual(stats.failed_calls, 0)
        self.assertEqual(stats.total_retries, 0)
        self.assertEqual(stats.total_time, 0.0)
        self.assertEqual(stats.success_rate, 0.0)
    
    def test_record_success(self):
        """Test recording successful calls."""
        stats = RetryStats()
        stats.record_success(1.5)
        stats.record_success(2.5)
        
        self.assertEqual(stats.total_calls, 2)
        self.assertEqual(stats.successful_calls, 2)
        self.assertEqual(stats.failed_calls, 0)
        self.assertEqual(stats.total_time, 4.0)
        self.assertEqual(stats.success_rate, 1.0)
    
    def test_record_failure(self):
        """Test recording failed calls."""
        stats = RetryStats()
        stats.record_failure(3, 5.0)  # 3 retries, 5 seconds
        stats.record_failure(2, 3.0)  # 2 retries, 3 seconds
        
        self.assertEqual(stats.total_calls, 2)
        self.assertEqual(stats.successful_calls, 0)
        self.assertEqual(stats.failed_calls, 2)
        self.assertEqual(stats.total_retries, 5)
        self.assertEqual(stats.total_time, 8.0)
        self.assertEqual(stats.success_rate, 0.0)
        self.assertEqual(stats.avg_retries, 2.5)
    
    def test_mixed_results(self):
        """Test mixed success and failure."""
        stats = RetryStats()
        stats.record_success(1.0)
        stats.record_success(2.0)
        stats.record_failure(3, 4.0)
        
        self.assertEqual(stats.total_calls, 3)
        self.assertEqual(stats.successful_calls, 2)
        self.assertEqual(stats.failed_calls, 1)
        self.assertAlmostEqual(stats.success_rate, 0.667, places=2)
    
    def test_to_dict(self):
        """Test converting stats to dictionary."""
        stats = RetryStats()
        stats.record_success(1.0)
        stats.record_failure(2, 3.0)
        
        result = stats.to_dict()
        self.assertEqual(result['total_calls'], 2)
        self.assertEqual(result['successful_calls'], 1)
        self.assertEqual(result['failed_calls'], 1)
        self.assertIn('success_rate', result)
    
    def test_reset(self):
        """Test resetting stats."""
        stats = RetryStats()
        stats.record_success(1.0)
        stats.record_failure(2, 3.0)
        stats.reset()
        
        self.assertEqual(stats.total_calls, 0)
        self.assertEqual(stats.success_rate, 0.0)
    
    def test_thread_safety(self):
        """Test thread safety of stats."""
        stats = RetryStats()
        errors = []
        
        def record_many():
            try:
                for _ in range(100):
                    stats.record_success(0.1)
                    stats.record_failure(1, 0.2)
            except Exception as e:
                errors.append(e)
        
        threads = [threading.Thread(target=record_many) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        self.assertEqual(len(errors), 0)
        self.assertEqual(stats.total_calls, 1000)


class TestRetryConfig(unittest.TestCase):
    """Test RetryConfig class."""
    
    def test_default_config(self):
        """Test default configuration."""
        config = RetryConfig()
        self.assertEqual(config.max_retries, 3)
        self.assertEqual(config.base_delay, 1.0)
        self.assertEqual(config.max_delay, 60.0)
        self.assertEqual(config.exponential_base, 2.0)
        self.assertTrue(config.jitter)
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = RetryConfig(
            max_retries=5,
            base_delay=0.5,
            max_delay=30.0,
            jitter=False,
        )
        self.assertEqual(config.max_retries, 5)
        self.assertEqual(config.base_delay, 0.5)
        self.assertEqual(config.max_delay, 30.0)
        self.assertFalse(config.jitter)
    
    def test_calculate_delay_exponential(self):
        """Test exponential delay calculation."""
        config = RetryConfig(base_delay=1.0, exponential_base=2.0, jitter=False)
        
        self.assertEqual(config.calculate_delay(0), 1.0)
        self.assertEqual(config.calculate_delay(1), 2.0)
        self.assertEqual(config.calculate_delay(2), 4.0)
        self.assertEqual(config.calculate_delay(3), 8.0)
    
    def test_calculate_delay_max(self):
        """Test delay is capped at max_delay."""
        config = RetryConfig(base_delay=1.0, max_delay=10.0, exponential_base=2.0, jitter=False)
        
        # 2^10 = 1024, but should be capped at 10
        delay = config.calculate_delay(10)
        self.assertLessEqual(delay, 10.0)
    
    def test_calculate_delay_jitter(self):
        """Test jitter adds randomness."""
        config = RetryConfig(base_delay=1.0, jitter=True, jitter_factor=0.5)
        
        delays = [config.calculate_delay(0) for _ in range(10)]
        # With 50% jitter, delays should vary
        self.assertNotEqual(len(set(delays)), 1)
    
    def test_is_retryable_exception(self):
        """Test exception filtering."""
        config = RetryConfig(retryable_exceptions=(ValueError, TypeError))
        
        self.assertTrue(config.is_retryable_exception(ValueError("test")))
        self.assertTrue(config.is_retryable_exception(TypeError("test")))
        self.assertFalse(config.is_retryable_exception(RuntimeError("test")))
    
    def test_retry_on_result(self):
        """Test result-based retry."""
        config = RetryConfig(retry_on_result=lambda x: x is None)
        
        self.assertTrue(config.should_retry_result(None))
        self.assertFalse(config.should_retry_result("value"))


class TestBackoffStrategies(unittest.TestCase):
    """Test predefined backoff strategies."""
    
    def test_constant_strategy(self):
        """Test constant backoff strategy."""
        config = BackoffStrategies.constant(delay=2.0)
        
        self.assertEqual(config.calculate_delay(0), 2.0)
        self.assertEqual(config.calculate_delay(5), 2.0)
        self.assertFalse(config.jitter)
    
    def test_linear_strategy(self):
        """Test linear backoff strategy."""
        config = BackoffStrategies.linear(base_delay=1.0, max_delay=10.0)
        
        self.assertEqual(config.exponential_base, 1.0)
        self.assertFalse(config.jitter)
    
    def test_exponential_strategy(self):
        """Test exponential backoff strategy."""
        config = BackoffStrategies.exponential(base_delay=1.0, max_delay=60.0, jitter=True)
        
        self.assertEqual(config.exponential_base, 2.0)
        self.assertTrue(config.jitter)
    
    def test_fibonacci_strategy(self):
        """Test fibonacci backoff strategy."""
        config = BackoffStrategies.fibonacci(max_delay=60.0)
        
        # Golden ratio approximation
        self.assertAlmostEqual(config.exponential_base, 1.618, places=2)
        self.assertFalse(config.jitter)


class TestRetryExecutor(unittest.TestCase):
    """Test RetryExecutor class."""
    
    def test_immediate_success(self):
        """Test function that succeeds immediately."""
        config = RetryConfig(max_retries=3)
        executor = RetryExecutor(config)
        
        call_count = 0
        
        def success_func():
            nonlocal call_count
            call_count += 1
            return "success"
        
        result = executor.execute(success_func)
        
        self.assertEqual(result, "success")
        self.assertEqual(call_count, 1)
    
    def test_success_after_retries(self):
        """Test function that succeeds after some failures."""
        config = RetryConfig(max_retries=3, base_delay=0.01, jitter=False)
        executor = RetryExecutor(config)
        
        call_count = 0
        
        def flaky_func():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Temporary failure")
            return "success"
        
        result = executor.execute(flaky_func)
        
        self.assertEqual(result, "success")
        self.assertEqual(call_count, 3)
    
    def test_all_retries_exhausted(self):
        """Test function that always fails."""
        config = RetryConfig(max_retries=2, base_delay=0.01, jitter=False)
        executor = RetryExecutor(config)
        
        def always_fail():
            raise ValueError("Always fails")
        
        with self.assertRaises(RetryError) as context:
            executor.execute(always_fail)
        
        self.assertEqual(context.exception.attempts, 3)  # 1 initial + 2 retries
        self.assertIsInstance(context.exception.last_exception, ValueError)
    
    def test_non_retryable_exception(self):
        """Test that non-retryable exceptions are raised immediately."""
        config = RetryConfig(
            max_retries=3,
            retryable_exceptions=(ValueError,),
        )
        executor = RetryExecutor(config)
        
        call_count = 0
        
        def raise_type_error():
            nonlocal call_count
            call_count += 1
            raise TypeError("Not retryable")
        
        with self.assertRaises(TypeError):
            executor.execute(raise_type_error)
        
        self.assertEqual(call_count, 1)  # Should only be called once
    
    def test_retry_on_result(self):
        """Test retry based on result value."""
        config = RetryConfig(
            max_retries=3,
            base_delay=0.01,
            jitter=False,
            retry_on_result=lambda x: x is None,
        )
        executor = RetryExecutor(config)
        
        call_count = 0
        
        def returns_none_then_value():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                return None
            return "value"
        
        result = executor.execute(returns_none_then_value)
        
        self.assertEqual(result, "value")
        self.assertEqual(call_count, 3)
    
    def test_timeout(self):
        """Test timeout enforcement."""
        config = RetryConfig(
            max_retries=10,
            base_delay=1.0,
            timeout=0.1,
            jitter=False,
        )
        executor = RetryExecutor(config)
        
        def always_fail():
            raise ValueError("Fails")
        
        start = time.time()
        with self.assertRaises(RetryError) as context:
            executor.execute(always_fail)
        elapsed = time.time() - start
        
        self.assertLess(elapsed, 0.5)  # Should timeout quickly
        self.assertIn("Timeout", str(context.exception))
    
    def test_on_retry_callback(self):
        """Test on_retry callback."""
        call_count = 0
        callbacks = []
        
        def on_retry(attempt, exception, delay):
            callbacks.append((attempt, type(exception).__name__ if exception else None, delay))
        
        config = RetryConfig(
            max_retries=2,
            base_delay=0.01,
            jitter=False,
            on_retry=on_retry,
        )
        executor = RetryExecutor(config)
        
        def fail_twice():
            nonlocal call_count
            call_count += 1
            if call_count < 3:  # First two calls fail
                raise ValueError("Fail")
            return "success"
        
        executor.execute(fail_twice)
        
        self.assertEqual(len(callbacks), 2)
        self.assertEqual(callbacks[0][0], 1)  # First retry
        self.assertEqual(callbacks[1][0], 2)  # Second retry
    
    def test_attempts_tracking(self):
        """Test that attempts are tracked."""
        config = RetryConfig(max_retries=2, base_delay=0.01, jitter=False)
        executor = RetryExecutor(config)
        
        def fail_twice():
            if len(executor.attempts) < 2:
                raise ValueError("Fail")
            return "success"
        
        executor.execute(fail_twice)
        
        self.assertEqual(len(executor.attempts), 2)
        self.assertEqual(executor.attempts[0].attempt_number, 1)
        self.assertEqual(executor.attempts[1].attempt_number, 2)


class TestRetryDecorator(unittest.TestCase):
    """Test retry decorator."""
    
    def test_decorator_success(self):
        """Test decorator with successful function."""
        @retry(max_retries=3, base_delay=0.01)
        def success():
            return "ok"
        
        self.assertEqual(success(), "ok")
    
    def test_decorator_retry(self):
        """Test decorator with retry behavior."""
        call_count = 0
        
        @retry(max_retries=3, base_delay=0.01, jitter=False)
        def flaky():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Temporary")
            return "ok"
        
        result = flaky()
        
        self.assertEqual(result, "ok")
        self.assertEqual(call_count, 3)
    
    def test_decorator_exhausted(self):
        """Test decorator with exhausted retries."""
        @retry(max_retries=2, base_delay=0.01, jitter=False)
        def always_fail():
            raise ValueError("Always")
        
        with self.assertRaises(RetryError):
            always_fail()
    
    def test_decorator_preserves_metadata(self):
        """Test that decorator preserves function metadata."""
        @retry(max_retries=3)
        def documented_func():
            """This is documentation."""
            pass
        
        self.assertEqual(documented_func.__name__, "documented_func")
        self.assertEqual(documented_func.__doc__, "This is documentation.")


class TestRetryWithConfig(unittest.TestCase):
    """Test retry_with_config function."""
    
    def test_basic_usage(self):
        """Test basic retry_with_config usage."""
        config = RetryConfig(max_retries=2, base_delay=0.01, jitter=False)
        
        call_count = 0
        
        def flaky():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("Fail")
            return "success"
        
        result = retry_with_config(flaky, config)
        
        self.assertEqual(result, "success")
        self.assertEqual(call_count, 2)


class TestGlobalStats(unittest.TestCase):
    """Test global statistics tracking."""
    
    def setUp(self):
        """Reset global stats before each test."""
        reset_global_stats()
    
    def test_get_global_stats(self):
        """Test getting global stats."""
        stats = get_global_stats()
        self.assertIsInstance(stats, RetryStats)
    
    def test_reset_global_stats(self):
        """Test resetting global stats."""
        stats = get_global_stats()
        stats.record_success(1.0)
        reset_global_stats()
        
        stats = get_global_stats()
        self.assertEqual(stats.total_calls, 0)


class TestConvenienceExceptions(unittest.TestCase):
    """Test convenience exception classes."""
    
    def test_transient_error(self):
        """Test TransientError."""
        error = TransientError("Transient")
        self.assertIsInstance(error, Exception)
    
    def test_network_error(self):
        """Test NetworkError."""
        error = NetworkError("Network issue")
        self.assertIsInstance(error, TransientError)
    
    def test_service_unavailable(self):
        """Test ServiceUnavailableError."""
        error = ServiceUnavailableError("Service down")
        self.assertIsInstance(error, TransientError)
    
    def test_rate_limit_error(self):
        """Test RateLimitError with retry_after."""
        error = RateLimitError("Rate limited", retry_after=30.0)
        self.assertIsInstance(error, TransientError)
        self.assertEqual(error.retry_after, 30.0)


class TestPredefinedConfigs(unittest.TestCase):
    """Test predefined retry configurations."""
    
    def test_retry_network(self):
        """Test RETRY_NETWORK config."""
        self.assertEqual(RETRY_NETWORK.max_retries, 3)
        self.assertTrue(RETRY_NETWORK.is_retryable_exception(ConnectionError("test")))
    
    def test_retry_database(self):
        """Test RETRY_DATABASE config."""
        self.assertEqual(RETRY_DATABASE.max_retries, 5)
        self.assertEqual(RETRY_DATABASE.base_delay, 0.5)
    
    def test_retry_api(self):
        """Test RETRY_API config."""
        self.assertEqual(RETRY_API.max_retries, 3)
        self.assertEqual(RETRY_API.base_delay, 2.0)
    
    def test_retry_quick(self):
        """Test RETRY_QUICK config."""
        self.assertEqual(RETRY_QUICK.max_retries, 2)
        self.assertFalse(RETRY_QUICK.jitter)


class TestIntegration(unittest.TestCase):
    """Integration tests."""
    
    def test_full_workflow(self):
        """Test complete retry workflow."""
        stats = RetryStats()
        config = RetryConfig(
            max_retries=3,
            base_delay=0.01,
            jitter=False,
            stats=stats,
        )
        executor = RetryExecutor(config)
        
        # Simulate API call with transient failures
        call_count = 0
        
        def api_call():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise NetworkError("Connection timeout")
            if call_count == 2:
                raise ServiceUnavailableError("Service busy")
            return {"data": "success"}
        
        result = executor.execute(api_call)
        
        self.assertEqual(result, {"data": "success"})
        self.assertEqual(call_count, 3)
        self.assertEqual(stats.successful_calls, 1)
    
    def test_concurrent_retries(self):
        """Test concurrent retry operations."""
        config = RetryConfig(max_retries=2, base_delay=0.01, jitter=False)
        executor = RetryExecutor(config)
        
        results = []
        errors = []
        
        def worker(id):
            try:
                call_count = 0
                
                def flaky():
                    nonlocal call_count
                    call_count += 1
                    if call_count < 2:
                        raise ValueError(f"Worker {id} fail")
                    return f"Worker {id} success"
                
                result = executor.execute(flaky)
                results.append(result)
            except Exception as e:
                errors.append(e)
        
        threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        self.assertEqual(len(errors), 0)
        self.assertEqual(len(results), 5)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_zero_retries(self):
        """Test with zero retries."""
        config = RetryConfig(max_retries=0, base_delay=0.01)
        executor = RetryExecutor(config)
        
        call_count = 0
        
        def fail():
            nonlocal call_count
            call_count += 1
            raise ValueError("Fail")
        
        with self.assertRaises(RetryError):
            executor.execute(fail)
        
        self.assertEqual(call_count, 1)  # Only initial attempt
    
    def test_zero_delay(self):
        """Test with zero delay."""
        config = RetryConfig(max_retries=2, base_delay=0.0, jitter=False)
        executor = RetryExecutor(config)
        
        call_count = 0
        
        def fail():
            nonlocal call_count
            call_count += 1
            raise ValueError("Fail")
        
        start = time.time()
        with self.assertRaises(RetryError):
            executor.execute(fail)
        elapsed = time.time() - start
        
        self.assertEqual(call_count, 3)
        self.assertLess(elapsed, 0.1)  # Should be very fast
    
    def test_very_large_max_delay(self):
        """Test with very large max_delay."""
        config = RetryConfig(base_delay=1.0, max_delay=3600.0, jitter=False)
        
        # Should not crash and should cap properly
        delay = config.calculate_delay(20)
        self.assertLessEqual(delay, 3600.0)
    
    def test_negative_jitter_factor(self):
        """Test with negative jitter factor (should be handled)."""
        config = RetryConfig(base_delay=1.0, jitter=True, jitter_factor=-0.5)
        
        # Should still produce non-negative delays
        delay = config.calculate_delay(0)
        self.assertGreaterEqual(delay, 0.0)
    
    def test_exception_chain(self):
        """Test exception chaining in RetryError."""
        original = ValueError("Original")
        retry_error = RetryError("Retry failed", last_exception=original)
        
        self.assertEqual(retry_error.last_exception, original)
        self.assertEqual(retry_error.last_exception.args[0], "Original")


if __name__ == '__main__':
    unittest.main(verbosity=2)
