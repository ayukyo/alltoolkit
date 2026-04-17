"""
Tests for decorator_utils module
===============================

Comprehensive tests for all decorator utilities.
Run with: python -m pytest decorator_utils_test.py -v
Or: python decorator_utils_test.py
"""

import time
import threading
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from decorator_utils.mod import (
    timer, timer_verbose, retry, memoize, singleton,
    deprecated, validate_types, rate_limit, log_calls,
    timeout, count_calls, once, throttle, wrap_exceptions,
    profile, timed_block, combine
)


class TestTimer:
    """Tests for timer decorator"""
    
    def test_timer_basic(self, capsys):
        @timer
        def slow_function():
            time.sleep(0.1)
            return "done"
        
        result = slow_function()
        captured = capsys.readouterr()
        
        assert result == "done"
        assert "slow_function took" in captured.out
        assert "seconds" in captured.out
    
    def test_timer_preserves_function_name(self):
        @timer
        def my_func():
            pass
        
        assert my_func.__name__ == "my_func"
    
    def test_timer_verbose(self, capsys):
        @timer_verbose(include_args=True)
        def add(a, b):
            return a + b
        
        result = add(1, 2)
        captured = capsys.readouterr()
        
        assert result == 3
        assert "add" in captured.out
        assert "took" in captured.out


class TestRetry:
    """Tests for retry decorator"""
    
    def test_retry_success_on_first_try(self):
        call_count = 0
        
        @retry(max_attempts=3, delay=0.01)
        def succeed_immediately():
            nonlocal call_count
            call_count += 1
            return "success"
        
        result = succeed_immediately()
        assert result == "success"
        assert call_count == 1
    
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
        assert result == "success"
        assert call_count == 3
    
    def test_retry_max_attempts_exceeded(self):
        call_count = 0
        
        @retry(max_attempts=2, delay=0.01, exceptions=(ValueError,))
        def always_fail():
            nonlocal call_count
            call_count += 1
            raise ValueError("Always fails")
        
        try:
            always_fail()
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert str(e) == "Always fails"
            assert call_count == 2
    
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
        assert result == "done"
        assert len(attempts) == 2


class TestMemoize:
    """Tests for memoize decorator"""
    
    def test_memoize_caches_result(self):
        call_count = 0
        
        @memoize()
        def expensive(n):
            nonlocal call_count
            call_count += 1
            return n * n
        
        assert expensive(5) == 25
        assert expensive(5) == 25
        assert call_count == 1  # Only called once
        
        assert expensive(6) == 36
        assert call_count == 2  # Called again for new input
    
    def test_memoize_maxsize(self):
        call_count = 0
        
        @memoize(maxsize=2)
        def compute(n):
            nonlocal call_count
            call_count += 1
            return n
        
        compute(1)  # cache: [1]
        compute(2)  # cache: [1, 2]
        compute(3)  # cache: [2, 3] (1 evicted)
        compute(1)  # cache: [3, 1] (recalculated)
        
        assert call_count == 4  # 1 was recalculated
    
    def test_memoize_ttl(self):
        call_count = 0
        
        @memoize(maxsize=10, ttl=0.1)
        def compute(n):
            nonlocal call_count
            call_count += 1
            return n * 2
        
        assert compute(5) == 10
        assert compute(5) == 10
        assert call_count == 1
        
        time.sleep(0.15)
        assert compute(5) == 10
        assert call_count == 2  # Recalculated after TTL
    
    def test_memoize_typed(self):
        @memoize(typed=True)
        def process(n):
            return type(n)
        
        assert process(3) == int
        assert process(3.0) == float  # Different cache entry
    
    def test_memoize_cache_clear(self):
        @memoize()
        def compute(n):
            return n * 2
        
        compute(1)
        compute(2)
        compute.cache_clear()
        
        assert compute.cache_info()["size"] == 0


class TestSingleton:
    """Tests for singleton decorator"""
    
    def test_singleton_single_instance(self):
        @singleton
        class Database:
            def __init__(self):
                self.connections = 0
        
        db1 = Database()
        db1.connections = 5
        
        db2 = Database()
        
        assert db1 is db2
        assert db2.connections == 5
    
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
        
        # All instances should be the same
        assert all(inst is instances[0] for inst in instances)


class TestDeprecated:
    """Tests for deprecated decorator"""
    
    def test_deprecated_warning(self):
        @deprecated(reason="Use new_func instead")
        def old_func():
            return "result"
        
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = old_func()
            
            assert result == "result"
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "old_func is deprecated" in str(w[0].message)
    
    def test_deprecated_with_version(self):
        @deprecated(version="2.0.0", replacement="new_func")
        def old_func():
            pass
        
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            old_func()
            
            assert "since version 2.0.0" in str(w[0].message)
            assert "Use new_func instead" in str(w[0].message)


class TestValidateTypes:
    """Tests for validate_types decorator"""
    
    def test_validate_types_correct(self):
        @validate_types(name=str, age=int)
        def create_person(name, age):
            return {"name": name, "age": age}
        
        result = create_person("Alice", 30)
        assert result == {"name": "Alice", "age": 30}
    
    def test_validate_types_incorrect(self):
        @validate_types(name=str, age=int)
        def create_person(name, age):
            return {"name": name, "age": age}
        
        try:
            create_person("Alice", "30")
            assert False, "Should have raised TypeError"
        except TypeError as e:
            assert "age" in str(e)
            assert "int" in str(e)
    
    def test_validate_types_with_kwargs(self):
        @validate_types(data=list, count=int)
        def process(data, count=10):
            return len(data) * count
        
        assert process([1, 2, 3], count=2) == 6


class TestRateLimit:
    """Tests for rate_limit decorator"""
    
    def test_rate_limit_allows_within_limit(self):
        @rate_limit(calls=3, period=1.0)
        def api_call(n):
            return n * 2
        
        # Should allow 3 calls immediately
        for i in range(3):
            assert api_call(i) == i * 2
    
    def test_rate_limit_blocks_over_limit(self):
        @rate_limit(calls=2, period=0.5, raise_on_limit=True)
        def limited_call():
            return "ok"
        
        limited_call()
        limited_call()
        
        try:
            limited_call()
            assert False, "Should have raised RuntimeError"
        except RuntimeError as e:
            assert "Rate limit exceeded" in str(e)
    
    def test_rate_limit_waits(self):
        @rate_limit(calls=2, period=0.2)
        def limited_call(n):
            return n
        
        start = time.time()
        for i in range(4):
            limited_call(i)
        elapsed = time.time() - start
        
        # Should have waited at least 0.2 seconds for extra calls
        assert elapsed >= 0.15  # Some tolerance


class TestLogCalls:
    """Tests for log_calls decorator"""
    
    def test_log_calls_basic(self, capsys):
        @log_calls()
        def greet(name):
            return f"Hello, {name}!"
        
        result = greet("World")
        captured = capsys.readouterr()
        
        assert result == "Hello, World!"
        assert "CALL greet" in captured.out
        assert "'World'" in captured.out
    
    def test_log_calls_with_result(self, capsys):
        @log_calls(include_result=True)
        def add(a, b):
            return a + b
        
        add(1, 2)
        captured = capsys.readouterr()
        
        assert "CALL add" in captured.out
        assert "RETURN add -> 3" in captured.out
    
    def test_log_calls_with_custom_logger(self):
        logs = []
        
        def custom_logger(msg):
            logs.append(msg)
        
        @log_calls(logger=custom_logger, include_time=False)
        def process(data):
            return data.upper()
        
        process("hello")
        
        assert len(logs) == 1
        assert "CALL process" in logs[0]


class TestTimeout:
    """Tests for timeout decorator"""
    
    def test_timeout_completes_within_limit(self):
        @timeout(2.0)
        def fast_function():
            return "done"
        
        assert fast_function() == "done"
    
    def test_timeout_exceeds_limit(self):
        @timeout(0.1)
        def slow_function():
            time.sleep(1)
            return "done"
        
        try:
            slow_function()
            assert False, "Should have raised TimeoutError"
        except TimeoutError as e:
            assert "slow_function" in str(e)
            assert "timeout" in str(e).lower()


class TestCountCalls:
    """Tests for count_calls decorator"""
    
    def test_count_calls_basic(self):
        @count_calls
        def my_func():
            return "result"
        
        assert my_func.call_count == 0
        
        my_func()
        assert my_func.call_count == 1
        
        my_func()
        my_func()
        assert my_func.call_count == 3


class TestOnce:
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
        
        assert result1 == "initialized"
        assert result2 == "initialized"
        assert result3 == "initialized"
        assert call_count == 1
    
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
        
        assert call_count == 1
        assert all(r == 1 for r in results)


class TestThrottle:
    """Tests for throttle decorator"""
    
    def test_throttle_limits_calls(self):
        call_count = 0
        
        @throttle(interval=0.2)
        def throttled_func(n):
            nonlocal call_count
            call_count += 1
            return n
        
        # Rapid calls
        throttled_func(1)
        throttled_func(2)
        throttled_func(3)
        
        # Should have limited the actual executions
        assert call_count <= 2
    
    def test_throttle_returns_cached_result(self):
        @throttle(interval=0.3, trailing=False)
        def get_value():
            return time.time()
        
        r1 = get_value()
        time.sleep(0.05)
        r2 = get_value()
        
        # During throttle period, should return same result
        assert r1 == r2


class TestWrapExceptions:
    """Tests for wrap_exceptions decorator"""
    
    def test_wrap_exceptions_converts_type(self):
        @wrap_exceptions(catch=(ValueError,), raise_as=RuntimeError)
        def raise_value_error():
            raise ValueError("Original error")
        
        try:
            raise_value_error()
            assert False, "Should have raised RuntimeError"
        except RuntimeError as e:
            assert "Original error" in str(e)
    
    def test_wrap_exceptions_with_message(self):
        @wrap_exceptions(catch=(KeyError,), raise_as=ValueError, message="Config error")
        def get_config():
            return {}["missing_key"]
        
        try:
            get_config()
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Config error" in str(e)


class TestProfile:
    """Tests for profile decorator"""
    
    def test_profile_outputs_timing(self, capsys):
        @profile
        def compute():
            return sum(range(1000))
        
        result = compute()
        captured = capsys.readouterr()
        
        assert result == sum(range(1000))
        assert "PROFILE: compute" in captured.out
        assert "Execution time:" in captured.out


class TestTimedBlock:
    """Tests for timed_block context manager"""
    
    def test_timed_block(self, capsys):
        with timed_block("my operation"):
            time.sleep(0.1)
        
        captured = capsys.readouterr()
        assert "my operation took" in captured.out
        assert "seconds" in captured.out


class TestCombine:
    """Tests for combine decorator"""
    
    def test_combine_multiple_decorators(self):
        @combine(count_calls, timer)
        def my_func():
            time.sleep(0.01)
            return "done"
        
        result = my_func()
        
        assert result == "done"
        assert my_func.call_count == 1
    
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
        assert result == "success"
        # count_calls counts from wrapper perspective
        assert might_fail.call_count == 1


def run_tests():
    """Run all tests with pytest-style output"""
    import traceback
    
    test_classes = [
        TestTimer, TestRetry, TestMemoize, TestSingleton, TestDeprecated,
        TestValidateTypes, TestRateLimit, TestLogCalls, TestTimeout,
        TestCountCalls, TestOnce, TestThrottle, TestWrapExceptions,
        TestProfile, TestTimedBlock, TestCombine
    ]
    
    total_tests = 0
    passed = 0
    failed = 0
    
    for test_class in test_classes:
        instance = test_class()
        
        for method_name in dir(instance):
            if method_name.startswith('test_'):
                total_tests += 1
                test_name = f"{test_class.__name__}::{method_name}"
                
                # Create capsys fixture
                class CapturedOutput:
                    def __init__(self):
                        self.out = ""
                        self.err = ""
                    
                    def readouterr(self):
                        result = type('obj', (object,), {
                            'out': self.out,
                            'err': self.err
                        })()
                        self.out = ""
                        self.err = ""
                        return result
                
                capsys = CapturedOutput()
                
                # Capture output for tests that need it
                import io
                import sys as sys_module
                
                old_stdout = sys_module.stdout
                old_stderr = sys_module.stderr
                sys_module.stdout = io.StringIO()
                sys_module.stderr = io.StringIO()
                
                try:
                    # Inject capsys if needed
                    import inspect
                    sig = inspect.signature(getattr(instance, method_name))
                    if 'capsys' in sig.parameters:
                        getattr(instance, method_name)(capsys)
                    else:
                        getattr(instance, method_name)()
                    
                    passed += 1
                    print(f"✓ {test_name}")
                except Exception as e:
                    failed += 1
                    print(f"✗ {test_name}")
                    print(f"  Error: {e}")
                finally:
                    # Capture output
                    capsys.out = sys_module.stdout.getvalue()
                    capsys.err = sys_module.stderr.getvalue()
                    sys_module.stdout = old_stdout
                    sys_module.stderr = old_stderr
    
    print(f"\n{'='*60}")
    print(f"Tests: {total_tests}, Passed: {passed}, Failed: {failed}")
    print(f"{'='*60}")
    
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)