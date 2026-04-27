"""
Tests for decorator_utils module
===============================

Comprehensive tests for all decorator utilities.
Run with: python decorator_utils_test.py
"""

import time
import threading
import sys
import os
import unittest
import warnings
import io
from contextlib import redirect_stdout, redirect_stderr

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    timer, timer_verbose, retry, memoize, singleton,
    deprecated, validate_types, rate_limit, log_calls,
    timeout, count_calls, once, throttle, wrap_exceptions,
    profile, timed_block, combine
)


class TestTimer(unittest.TestCase):
    """Tests for timer decorator"""
    
    def test_timer_basic(self):
        @timer
        def slow_function():
            time.sleep(0.01)
            return "done"
        
        with io.StringIO() as buf, redirect_stdout(buf):
            result = slow_function()
            output = buf.getvalue()
        
        self.assertEqual(result, "done")
        self.assertIn("slow_function took", output)
        self.assertIn("seconds", output)
    
    def test_timer_preserves_function_name(self):
        @timer
        def my_func():
            pass
        
        self.assertEqual(my_func.__name__, "my_func")
    
    def test_timer_verbose(self):
        @timer_verbose(include_args=True)
        def add(a, b):
            return a + b
        
        with io.StringIO() as buf, redirect_stdout(buf):
            result = add(1, 2)
            output = buf.getvalue()
        
        self.assertEqual(result, 3)
        self.assertIn("add", output)
        self.assertIn("took", output)


class TestRetry(unittest.TestCase):
    """Tests for retry decorator"""
    
    def test_retry_success_on_first_try(self):
        call_count = 0
        
        @retry(max_attempts=3, delay=0.01)
        def succeed_immediately():
            nonlocal call_count
            call_count += 1
            return "success"
        
        result = succeed_immediately()
        self.assertEqual(result, "success")
        self.assertEqual(call_count, 1)
    
    def test_retry_success_after_failures(self):
        call_count = 0
        
        @retry(max_attempts=3, delay=0.01, exceptions=(ValueError,))
        def fail_twice():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Not yet")
            return "success"
        
        result = fail_twice()
        self.assertEqual(result, "success")
        self.assertEqual(call_count, 3)
    
    def test_retry_max_attempts_exceeded(self):
        call_count = 0
        
        @retry(max_attempts=2, delay=0.01, exceptions=(ValueError,))
        def always_fail():
            nonlocal call_count
            call_count += 1
            raise ValueError("Always fails")
        
        with self.assertRaises(ValueError) as ctx:
            always_fail()
        
        self.assertEqual(str(ctx.exception), "Always fails")
        self.assertEqual(call_count, 2)
    
    def test_retry_on_retry_callback(self):
        attempts = []
        
        def on_retry(attempt, exception):
            attempts.append((attempt, str(exception)))
        
        @retry(max_attempts=3, delay=0.01, exceptions=(ValueError,), on_retry=on_retry)
        def fail_twice():
            if len(attempts) < 2:
                raise ValueError(f"Attempt {len(attempts)}")
            return "done"
        
        result = fail_twice()
        self.assertEqual(result, "done")
        self.assertEqual(len(attempts), 2)


class TestMemoize(unittest.TestCase):
    """Tests for memoize decorator"""
    
    def test_memoize_caches_result(self):
        call_count = 0
        
        @memoize()
        def expensive(n):
            nonlocal call_count
            call_count += 1
            return n * n
        
        self.assertEqual(expensive(5), 25)
        self.assertEqual(expensive(5), 25)
        self.assertEqual(call_count, 1)
        
        self.assertEqual(expensive(6), 36)
        self.assertEqual(call_count, 2)
    
    def test_memoize_maxsize(self):
        call_count = 0
        
        @memoize(maxsize=2)
        def compute(n):
            nonlocal call_count
            call_count += 1
            return n
        
        compute(1)
        compute(2)
        compute(3)
        compute(1)
        
        self.assertEqual(call_count, 4)
    
    def test_memoize_ttl(self):
        call_count = 0
        
        @memoize(maxsize=10, ttl=0.1)
        def compute(n):
            nonlocal call_count
            call_count += 1
            return n * 2
        
        self.assertEqual(compute(5), 10)
        self.assertEqual(compute(5), 10)
        self.assertEqual(call_count, 1)
        
        time.sleep(0.15)
        self.assertEqual(compute(5), 10)
        self.assertEqual(call_count, 2)
    
    def test_memoize_typed(self):
        @memoize(typed=True)
        def process(n):
            return type(n)
        
        self.assertEqual(process(3), int)
        self.assertEqual(process(3.0), float)
    
    def test_memoize_cache_clear(self):
        @memoize()
        def compute(n):
            return n * 2
        
        compute(1)
        compute(2)
        compute.cache_clear()
        
        self.assertEqual(compute.cache_info()["size"], 0)


class TestSingleton(unittest.TestCase):
    """Tests for singleton decorator"""
    
    def test_singleton_single_instance(self):
        @singleton
        class Database:
            def __init__(self):
                self.connections = 0
        
        db1 = Database()
        db1.connections = 5
        
        db2 = Database()
        
        self.assertIs(db1, db2)
        self.assertEqual(db2.connections, 5)
    
    def test_singleton_thread_safety(self):
        @singleton
        class Counter:
            def __init__(self):
                self.value = 0
        
        instances = []
        
        def create_instance():
            instances.append(Counter())
        
        threads = [threading.Thread(target=create_instance) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        self.assertTrue(all(inst is instances[0] for inst in instances))


class TestDeprecated(unittest.TestCase):
    """Tests for deprecated decorator"""
    
    def test_deprecated_warning(self):
        @deprecated(reason="Use new_func instead")
        def old_func():
            return "result"
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = old_func()
            
            self.assertEqual(result, "result")
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            self.assertIn("old_func is deprecated", str(w[0].message))
    
    def test_deprecated_with_version(self):
        @deprecated(version="2.0.0", replacement="new_func")
        def old_func():
            pass
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            old_func()
            
            self.assertIn("since version 2.0.0", str(w[0].message))
            self.assertIn("Use new_func instead", str(w[0].message))


class TestValidateTypes(unittest.TestCase):
    """Tests for validate_types decorator"""
    
    def test_validate_types_correct(self):
        @validate_types(name=str, age=int)
        def create_person(name, age):
            return {"name": name, "age": age}
        
        result = create_person("Alice", 30)
        self.assertEqual(result, {"name": "Alice", "age": 30})
    
    def test_validate_types_incorrect(self):
        @validate_types(name=str, age=int)
        def create_person(name, age):
            return {"name": name, "age": age}
        
        with self.assertRaises(TypeError) as ctx:
            create_person("Alice", "30")
        
        self.assertIn("age", str(ctx.exception))
        self.assertIn("int", str(ctx.exception))
    
    def test_validate_types_with_kwargs(self):
        @validate_types(data=list, count=int)
        def process(data, count=10):
            return len(data) * count
        
        self.assertEqual(process([1, 2, 3], count=2), 6)


class TestRateLimit(unittest.TestCase):
    """Tests for rate_limit decorator"""
    
    def test_rate_limit_allows_within_limit(self):
        @rate_limit(calls=3, period=1.0)
        def api_call(n):
            return n * 2
        
        for i in range(3):
            self.assertEqual(api_call(i), i * 2)
    
    def test_rate_limit_blocks_over_limit(self):
        @rate_limit(calls=2, period=0.5, raise_on_limit=True)
        def limited_call():
            return "ok"
        
        limited_call()
        limited_call()
        
        with self.assertRaises(RuntimeError) as ctx:
            limited_call()
        
        self.assertIn("Rate limit exceeded", str(ctx.exception))
    
    def test_rate_limit_waits(self):
        @rate_limit(calls=2, period=0.2)
        def limited_call(n):
            return n
        
        start = time.time()
        for i in range(4):
            limited_call(i)
        elapsed = time.time() - start
        
        self.assertGreaterEqual(elapsed, 0.15)


class TestLogCalls(unittest.TestCase):
    """Tests for log_calls decorator"""
    
    def test_log_calls_basic(self):
        @log_calls()
        def greet(name):
            return f"Hello, {name}!"
        
        with io.StringIO() as buf, redirect_stdout(buf):
            result = greet("World")
            output = buf.getvalue()
        
        self.assertEqual(result, "Hello, World!")
        self.assertIn("CALL greet", output)
        self.assertIn("'World'", output)
    
    def test_log_calls_with_result(self):
        @log_calls(include_result=True)
        def add(a, b):
            return a + b
        
        with io.StringIO() as buf, redirect_stdout(buf):
            add(1, 2)
            output = buf.getvalue()
        
        self.assertIn("CALL add", output)
        self.assertIn("RETURN add -> 3", output)
    
    def test_log_calls_with_custom_logger(self):
        logs = []
        
        def custom_logger(msg):
            logs.append(msg)
        
        @log_calls(logger=custom_logger, include_time=False)
        def process(data):
            return data.upper()
        
        process("hello")
        
        self.assertEqual(len(logs), 1)
        self.assertIn("CALL process", logs[0])


class TestTimeout(unittest.TestCase):
    """Tests for timeout decorator"""
    
    def test_timeout_completes_within_limit(self):
        @timeout(2.0)
        def fast_function():
            return "done"
        
        self.assertEqual(fast_function(), "done")
    
    def test_timeout_exceeds_limit(self):
        @timeout(0.1)
        def slow_function():
            time.sleep(1)
            return "done"
        
        with self.assertRaises(TimeoutError) as ctx:
            slow_function()
        
        self.assertIn("slow_function", str(ctx.exception))
        self.assertIn("timeout", str(ctx.exception).lower())


class TestCountCalls(unittest.TestCase):
    """Tests for count_calls decorator"""
    
    def test_count_calls_basic(self):
        @count_calls
        def my_func():
            return "result"
        
        self.assertEqual(my_func.call_count, 0)
        
        my_func()
        self.assertEqual(my_func.call_count, 1)
        
        my_func()
        my_func()
        self.assertEqual(my_func.call_count, 3)


class TestOnce(unittest.TestCase):
    """Tests for once decorator"""
    
    def test_once_executes_only_once(self):
        call_count = 0
        
        @once
        def initialize():
            nonlocal call_count
            call_count += 1
            return "initialized"
        
        result1 = initialize()
        result2 = initialize()
        result3 = initialize()
        
        self.assertEqual(result1, "initialized")
        self.assertEqual(result2, "initialized")
        self.assertEqual(result3, "initialized")
        self.assertEqual(call_count, 1)
    
    def test_once_thread_safety(self):
        call_count = 0
        
        @once
        def init():
            nonlocal call_count
            call_count += 1
            return call_count
        
        results = []
        
        def call_init():
            results.append(init())
        
        threads = [threading.Thread(target=call_init) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        self.assertEqual(call_count, 1)
        self.assertTrue(all(r == 1 for r in results))


class TestThrottle(unittest.TestCase):
    """Tests for throttle decorator"""
    
    def test_throttle_limits_calls(self):
        call_count = 0
        
        @throttle(interval=0.2)
        def throttled_func(n):
            nonlocal call_count
            call_count += 1
            return n
        
        throttled_func(1)
        throttled_func(2)
        throttled_func(3)
        
        self.assertLessEqual(call_count, 2)
    
    def test_throttle_returns_cached_result(self):
        @throttle(interval=0.3, trailing=False)
        def get_value():
            return time.time()
        
        r1 = get_value()
        time.sleep(0.05)
        r2 = get_value()
        
        self.assertEqual(r1, r2)


class TestWrapExceptions(unittest.TestCase):
    """Tests for wrap_exceptions decorator"""
    
    def test_wrap_exceptions_converts_type(self):
        @wrap_exceptions(catch=(ValueError,), raise_as=RuntimeError)
        def raise_value_error():
            raise ValueError("Original error")
        
        with self.assertRaises(RuntimeError) as ctx:
            raise_value_error()
        
        self.assertIn("Original error", str(ctx.exception))
    
    def test_wrap_exceptions_with_message(self):
        @wrap_exceptions(catch=(KeyError,), raise_as=ValueError, message="Config error")
        def get_config():
            return {}["missing_key"]
        
        with self.assertRaises(ValueError) as ctx:
            get_config()
        
        self.assertIn("Config error", str(ctx.exception))


class TestProfile(unittest.TestCase):
    """Tests for profile decorator"""
    
    def test_profile_outputs_timing(self):
        @profile
        def compute():
            return sum(range(1000))
        
        with io.StringIO() as buf, redirect_stdout(buf):
            result = compute()
            output = buf.getvalue()
        
        self.assertEqual(result, sum(range(1000)))
        self.assertIn("PROFILE: compute", output)
        self.assertIn("Execution time:", output)


class TestTimedBlock(unittest.TestCase):
    """Tests for timed_block context manager"""
    
    def test_timed_block(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            with timed_block("my operation"):
                time.sleep(0.01)
            output = buf.getvalue()
        
        self.assertIn("my operation took", output)
        self.assertIn("seconds", output)


class TestCombine(unittest.TestCase):
    """Tests for combine decorator"""
    
    def test_combine_multiple_decorators(self):
        @combine(count_calls, timer)
        def my_func():
            time.sleep(0.01)
            return "done"
        
        with io.StringIO() as buf, redirect_stdout(buf):
            result = my_func()
        
        self.assertEqual(result, "done")
        self.assertEqual(my_func.call_count, 1)
    
    def test_combine_retry_and_count(self):
        call_count = 0
        
        @combine(count_calls, retry(max_attempts=3, delay=0.01, exceptions=(ValueError,)))
        def might_fail():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("Fail")
            return "success"
        
        result = might_fail()
        self.assertEqual(result, "success")
        self.assertEqual(might_fail.call_count, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)