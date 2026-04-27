"""
AllToolkit - Python Rate Limit Utilities Test Suite

Comprehensive tests for rate limiting utilities.
Covers normal scenarios, edge cases, and error conditions.

Run: python rate_limit_utils_test.py
"""

import os
import time
import threading
import sys
from typing import List

# Import the module under test

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    TokenBucket,
    SlidingWindowCounter,
    SlidingWindowLog,
    FixedWindowCounter,
    RateLimiter,
    RateLimitResult,
    rate_limit,
    rate_limit_strict,
    RateLimitExceeded,
    rate_limit_context,
    generate_rate_limit_key,
)


class TestResult:
    """Simple test result tracker."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors: List[str] = []
    
    def record_pass(self, name: str):
        self.passed += 1
        print(f"  ✅ {name}")
    
    def record_fail(self, name: str, message: str):
        self.failed += 1
        self.errors.append(f"{name}: {message}")
        print(f"  ❌ {name}: {message}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Tests: {total} | Passed: {self.passed} | Failed: {self.failed}")
        if self.errors:
            print(f"\nFailures:")
            for error in self.errors[:10]:  # Show first 10
                print(f"  - {error}")
        print(f"{'='*60}")
        return self.failed == 0


def assert_true(condition: bool, name: str, message: str = ""):
    """Assert condition is true."""
    if condition:
        return True
    raise AssertionError(message or f"{name} failed")


def test_token_bucket_basic(result: TestResult):
    """Test basic token bucket functionality."""
    print("\n📦 TokenBucket - Basic Tests")
    
    # Test initialization
    bucket = TokenBucket(capacity=10, refill_rate=2.0)
    assert_true(bucket.capacity == 10, "capacity check")
    assert_true(bucket.refill_rate == 2.0, "refill rate check")
    result.record_pass("Initialization")
    
    # Test consume
    bucket = TokenBucket(capacity=5, refill_rate=1.0)
    for i in range(5):
        assert_true(bucket.consume(), f"consume #{i+1}")
    result.record_pass("Consume all tokens")
    
    # Test exhaustion
    assert_true(not bucket.consume(), "exhausted bucket")
    result.record_pass("Exhaustion detection")
    
    # Test reset
    bucket.reset()
    assert_true(bucket.consume(), "after reset")
    result.record_pass("Reset functionality")


def test_token_bucket_refill(result: TestResult):
    """Test token bucket refill mechanism."""
    print("\n📦 TokenBucket - Refill Tests")
    
    bucket = TokenBucket(capacity=10, refill_rate=10.0)  # 10 tokens/sec
    
    # Consume all tokens
    for _ in range(10):
        bucket.consume()
    
    assert_true(not bucket.consume(), "empty after consume")
    
    # Wait for refill
    time.sleep(0.5)  # Should refill ~5 tokens
    
    tokens = bucket.tokens
    assert_true(tokens >= 4 and tokens <= 6, f"refill after 0.5s: {tokens}")
    result.record_pass("Token refill")
    
    # Test wait_time
    bucket = TokenBucket(capacity=10, refill_rate=2.0)
    for _ in range(10):
        bucket.consume()
    
    wait = bucket.wait_time()
    assert_true(0.4 <= wait <= 0.6, f"wait_time: {wait}")
    result.record_pass("Wait time calculation")


def test_token_bucket_check(result: TestResult):
    """Test token bucket check method."""
    print("\n📦 TokenBucket - Check Tests")
    
    bucket = TokenBucket(capacity=10, refill_rate=1.0)
    
    # Check when full
    check_result = bucket.check()
    assert_true(check_result.allowed, "allowed when full")
    assert_true(check_result.remaining == 10, f"remaining: {check_result.remaining}")
    assert_true(check_result.limit == 10, "limit correct")
    result.record_pass("Check when full")
    
    # Check when partially empty
    for _ in range(5):
        bucket.consume()
    
    check_result = bucket.check()
    assert_true(check_result.remaining == 5, f"remaining after 5 consumes: {check_result.remaining}")
    result.record_pass("Check partial")
    
    # Check when empty
    for _ in range(5):
        bucket.consume()
    
    check_result = bucket.check()
    assert_true(not check_result.allowed, "not allowed when empty")
    assert_true(check_result.retry_after is not None, "retry_after set")
    assert_true(check_result.retry_after > 0, "retry_after positive")
    result.record_pass("Check empty")


def test_token_bucket_multi_consume(result: TestResult):
    """Test consuming multiple tokens at once."""
    print("\n📦 TokenBucket - Multi-token Consume")
    
    bucket = TokenBucket(capacity=10, refill_rate=1.0)
    
    # Consume multiple tokens
    assert_true(bucket.consume(3), "consume 3 tokens")
    assert_true(bucket.tokens == 7, f"remaining: {bucket.tokens}")
    result.record_pass("Multi-token consume")
    
    # Consume more than available
    assert_true(not bucket.consume(8), "reject over-consume")
    result.record_pass("Over-consume rejection")


def test_token_bucket_threading(result: TestResult):
    """Test thread safety of token bucket."""
    print("\n📦 TokenBucket - Thread Safety")
    
    bucket = TokenBucket(capacity=100, refill_rate=0.0)  # No refill
    success_count = [0]
    lock = threading.Lock()
    
    def consume_tokens():
        for _ in range(10):
            if bucket.consume():
                with lock:
                    success_count[0] += 1
    
    threads = [threading.Thread(target=consume_tokens) for _ in range(20)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    # Should have exactly 100 successes (capacity)
    assert_true(success_count[0] == 100, f"thread-safe count: {success_count[0]}")
    result.record_pass("Thread safety")


def test_sliding_window_counter_basic(result: TestResult):
    """Test basic sliding window counter functionality."""
    print("\n🪟 SlidingWindowCounter - Basic Tests")
    
    limiter = SlidingWindowCounter(max_requests=5, window_seconds=1.0)
    
    # Allow up to max
    for i in range(5):
        assert_true(limiter.allow(), f"allow #{i+1}")
    result.record_pass("Allow up to max")
    
    # Reject over limit
    assert_true(not limiter.allow(), "reject over limit")
    result.record_pass("Over-limit rejection")
    
    # Reset and try again
    limiter.reset()
    assert_true(limiter.allow(), "after reset")
    result.record_pass("Reset functionality")


def test_sliding_window_counter_window(result: TestResult):
    """Test sliding window counter window expiration."""
    print("\n🪟 SlidingWindowCounter - Window Tests")
    
    limiter = SlidingWindowCounter(max_requests=3, window_seconds=0.5)
    
    # Use all requests
    for _ in range(3):
        limiter.allow()
    
    assert_true(not limiter.allow(), "limited")
    
    # Wait for window to pass
    time.sleep(0.6)
    
    assert_true(limiter.allow(), "after window")
    result.record_pass("Window expiration")


def test_sliding_window_counter_check(result: TestResult):
    """Test sliding window counter check method."""
    print("\n🪟 SlidingWindowCounter - Check Tests")
    
    limiter = SlidingWindowCounter(max_requests=10, window_seconds=60.0)
    
    check_result = limiter.check()
    assert_true(check_result.allowed, "allowed initially")
    assert_true(check_result.remaining == 10, f"remaining: {check_result.remaining}")
    assert_true(check_result.limit == 10, "limit correct")
    result.record_pass("Check method")


def test_sliding_window_log_basic(result: TestResult):
    """Test basic sliding window log functionality."""
    print("\n📜 SlidingWindowLog - Basic Tests")
    
    limiter = SlidingWindowLog(max_requests=5, window_seconds=1.0)
    
    for i in range(5):
        assert_true(limiter.allow(), f"allow #{i+1}")
    result.record_pass("Allow up to max")
    
    assert_true(not limiter.allow(), "reject over limit")
    result.record_pass("Over-limit rejection")


def test_sliding_window_log_precision(result: TestResult):
    """Test sliding window log precision."""
    print("\n📜 SlidingWindowLog - Precision Tests")
    
    limiter = SlidingWindowLog(max_requests=3, window_seconds=0.5)
    
    for _ in range(3):
        limiter.allow()
    
    assert_true(not limiter.allow(), "limited")
    
    # Wait for oldest to expire
    time.sleep(0.6)
    
    assert_true(limiter.allow(), "after oldest expires")
    result.record_pass("Precise expiration")
    
    # Test count property
    assert_true(limiter.count == 1, f"count: {limiter.count}")
    result.record_pass("Count property")


def test_fixed_window_basic(result: TestResult):
    """Test basic fixed window counter functionality."""
    print("\n🔲 FixedWindowCounter - Basic Tests")
    
    limiter = FixedWindowCounter(max_requests=5, window_seconds=60.0)
    
    for i in range(5):
        assert_true(limiter.allow(), f"allow #{i+1}")
    result.record_pass("Allow up to max")
    
    assert_true(not limiter.allow(), "reject over limit")
    result.record_pass("Over-limit rejection")
    
    limiter.reset()
    assert_true(limiter.allow(), "after reset")
    result.record_pass("Reset functionality")


def test_fixed_window_expiration(result: TestResult):
    """Test fixed window expiration."""
    print("\n🔲 FixedWindowCounter - Window Expiration")
    
    limiter = FixedWindowCounter(max_requests=2, window_seconds=0.3)
    
    limiter.allow()
    limiter.allow()
    
    assert_true(not limiter.allow(), "limited")
    
    time.sleep(0.4)
    
    assert_true(limiter.allow(), "after window")
    result.record_pass("Window expiration")


def test_rate_limiter_multi_key(result: TestResult):
    """Test multi-key rate limiter."""
    print("\n🔑 RateLimiter - Multi-key Tests")
    
    limiter = RateLimiter(
        strategy='token_bucket',
        capacity=3,
        refill_rate=0.0,  # No refill for testing
    )
    
    # Different keys have independent limits
    for key in ['user_a', 'user_b', 'user_c']:
        for i in range(3):
            assert_true(limiter.allow(key), f"{key} allow #{i+1}")
        assert_true(not limiter.allow(key), f"{key} limited")
    result.record_pass("Independent key limits")
    
    # Reset specific key
    limiter.reset('user_a')
    assert_true(limiter.allow('user_a'), "after key reset")
    assert_true(not limiter.allow('user_b'), "other key still limited")
    result.record_pass("Per-key reset")
    
    # Reset all
    limiter.reset_all()
    assert_true(limiter.allow('user_b'), "after reset all")
    result.record_pass("Reset all")


def test_rate_limiter_strategies(result: TestResult):
    """Test different rate limiting strategies."""
    print("\n🔑 RateLimiter - Strategy Tests")
    
    strategies = ['token_bucket', 'sliding_window', 'sliding_window_log', 'fixed_window']
    
    for strategy in strategies:
        limiter = RateLimiter(
            strategy=strategy,
            max_requests=5,
            window_seconds=60.0,
            capacity=5,
            refill_rate=1.0,
        )
        
        for i in range(5):
            assert_true(limiter.allow(f'key_{strategy}'), f"{strategy} allow #{i+1}")
        
        assert_true(not limiter.allow(f'key_{strategy}'), f"{strategy} limited")
        result.record_pass(f"Strategy: {strategy}")


def test_rate_limit_decorator(result: TestResult):
    """Test rate limit decorator."""
    print("\n🎭 Rate Limit Decorator Tests")
    
    call_count = [0]
    limited_count = [0]
    
    def on_limited(*args, **kwargs):
        limited_count[0] += 1
        return "limited"
    
    @rate_limit(
        max_requests=3,
        window_seconds=60.0,
        on_limit=on_limited,
    )
    def test_function():
        call_count[0] += 1
        return "ok"
    
    # Should allow 3 calls
    for i in range(3):
        assert_true(test_function() == "ok", f"call #{i+1}")
    
    # 4th should be limited
    assert_true(test_function() == "limited", "4th call limited")
    
    assert_true(call_count[0] == 3, f"call count: {call_count[0]}")
    assert_true(limited_count[0] == 1, f"limited count: {limited_count[0]}")
    result.record_pass("Decorator functionality")


def test_rate_limit_decorator_key_func(result: TestResult):
    """Test rate limit decorator with custom key function."""
    print("\n🎭 Rate Limit Decorator - Key Function")
    
    @rate_limit(
        max_requests=2,
        window_seconds=60.0,
        key_func=lambda user_id, **kwargs: user_id,
    )
    def user_action(user_id: str):
        return f"action for {user_id}"
    
    # Each user gets their own limit
    assert_true(user_action("user_a") == "action for user_a")
    assert_true(user_action("user_a") == "action for user_a")
    assert_true(user_action("user_b") == "action for user_b")
    assert_true(user_action("user_b") == "action for user_b")
    
    # Both users should be limited now
    assert_true(user_action("user_a") is None, "user_a limited")
    assert_true(user_action("user_b") is None, "user_b limited")
    
    result.record_pass("Custom key function")


def test_rate_limit_strict(result: TestResult):
    """Test strict rate limit decorator."""
    print("\n🎭 Rate Limit Strict Decorator")
    
    @rate_limit_strict(max_requests=2, window_seconds=60.0)
    def strict_function():
        return "ok"
    
    # Should allow 2 calls
    assert_true(strict_function() == "ok", "1st call")
    assert_true(strict_function() == "ok", "2nd call")
    
    # 3rd should raise exception
    try:
        strict_function()
        result.record_fail("Exception raised", "No exception raised")
    except RateLimitExceeded as e:
        assert_true(e.retry_after is not None, "retry_after in exception")
        assert_true('limit_info' in e.to_dict(), "to_dict works")
        result.record_pass("Exception on limit")


def test_rate_limit_context(result: TestResult):
    """Test rate limit context manager."""
    print("\n🎭 Rate Limit Context Manager")
    
    limiter = RateLimiter(strategy='token_bucket', capacity=2, refill_rate=0.0)
    
    entered_count = [0]
    limited_count = [0]
    
    def on_limit():
        limited_count[0] += 1
    
    # First two should enter
    with rate_limit_context(limiter, 'key1'):
        entered_count[0] += 1
    
    with rate_limit_context(limiter, 'key1'):
        entered_count[0] += 1
    
    # Third should not enter
    with rate_limit_context(limiter, 'key1', on_limit=on_limit):
        pass  # Should not reach here
    
    assert_true(entered_count[0] == 2, f"entered count: {entered_count[0]}")
    assert_true(limited_count[0] == 1, f"limited count: {limited_count[0]}")
    result.record_pass("Context manager")


def test_rate_limit_result(result: TestResult):
    """Test RateLimitResult class."""
    print("\n📊 RateLimitResult Tests")
    
    result_obj = RateLimitResult(
        allowed=True,
        remaining=5,
        reset_at=time.time() + 60,
        limit=10,
        window_seconds=60.0,
    )
    
    assert_true(bool(result_obj), "bool conversion")
    assert_true(result_obj.to_dict()['allowed'], "to_dict")
    assert_true(result_obj.to_dict()['remaining'] == 5, "to_dict remaining")
    result.record_pass("Result object")
    
    # Test false result
    result_obj = RateLimitResult(
        allowed=False,
        remaining=0,
        reset_at=time.time() + 60,
        retry_after=30.0,
    )
    
    assert_true(not bool(result_obj), "bool conversion false")
    assert_true(result_obj.retry_after == 30.0, "retry_after")
    result.record_pass("False result")


def test_generate_rate_limit_key(result: TestResult):
    """Test key generation function."""
    print("\n🔑 Key Generation Tests")
    
    key1 = generate_rate_limit_key("arg1", kwarg1="value1")
    key2 = generate_rate_limit_key("arg1", kwarg1="value1")
    key3 = generate_rate_limit_key("arg2", kwarg1="value1")
    
    assert_true(key1 == key2, "same args produce same key")
    assert_true(key1 != key3, "different args produce different key")
    assert_true(len(key1) == 16, f"key length: {len(key1)}")
    result.record_pass("Key generation")


def test_error_handling(result: TestResult):
    """Test error handling for invalid inputs."""
    print("\n⚠️ Error Handling Tests")
    
    # TokenBucket invalid capacity
    try:
        TokenBucket(capacity=0, refill_rate=1.0)
        result.record_fail("Zero capacity", "No exception raised")
    except ValueError:
        result.record_pass("Zero capacity rejected")
    
    # TokenBucket invalid refill rate
    try:
        TokenBucket(capacity=10, refill_rate=0)
        result.record_fail("Zero refill rate", "No exception raised")
    except ValueError:
        result.record_pass("Zero refill rate rejected")
    
    # SlidingWindowCounter invalid max_requests
    try:
        SlidingWindowCounter(max_requests=-1, window_seconds=60)
        result.record_fail("Negative max requests", "No exception raised")
    except ValueError:
        result.record_pass("Negative max requests rejected")
    
    # Invalid strategy
    try:
        RateLimiter(strategy='invalid_strategy')
        result.record_fail("Invalid strategy", "No exception raised")
    except ValueError:
        result.record_pass("Invalid strategy rejected")


def test_consume_multiple_tokens(result: TestResult):
    """Test consuming multiple tokens at once."""
    print("\n📦 Multi-token Operations")
    
    bucket = TokenBucket(capacity=10, refill_rate=1.0)
    
    # Consume 5 tokens
    assert_true(bucket.consume(5), "consume 5")
    assert_true(bucket.tokens == 5, f"remaining: {bucket.tokens}")
    result.record_pass("Consume multiple")
    
    # Try to consume more than available
    assert_true(not bucket.consume(6), "reject over-consume")
    result.record_pass("Reject over-consume")
    
    # Consume exact remaining
    assert_true(bucket.consume(5), "consume exact remaining")
    assert_true(bucket.tokens == 0, "empty")
    result.record_pass("Consume exact")


def test_wait_time_calculation(result: TestResult):
    """Test wait time calculations."""
    print("\n⏱️ Wait Time Tests")
    
    bucket = TokenBucket(capacity=10, refill_rate=2.0)
    
    # Empty the bucket
    for _ in range(10):
        bucket.consume()
    
    # Calculate wait time for 1 token
    wait = bucket.wait_time(1)
    assert_true(0.4 <= wait <= 0.6, f"wait for 1 token: {wait}")
    result.record_pass("Wait time for 1 token")
    
    # Calculate wait time for 5 tokens
    wait = bucket.wait_time(5)
    assert_true(2.4 <= wait <= 2.6, f"wait for 5 tokens: {wait}")
    result.record_pass("Wait time for multiple tokens")


def run_all_tests():
    """Run all tests and report results."""
    print("="*60)
    print("AllToolkit - Rate Limit Utilities Test Suite")
    print("="*60)
    
    result = TestResult()
    
    # TokenBucket tests
    test_token_bucket_basic(result)
    test_token_bucket_refill(result)
    test_token_bucket_check(result)
    test_token_bucket_multi_consume(result)
    test_token_bucket_threading(result)
    
    # SlidingWindowCounter tests
    test_sliding_window_counter_basic(result)
    test_sliding_window_counter_window(result)
    test_sliding_window_counter_check(result)
    
    # SlidingWindowLog tests
    test_sliding_window_log_basic(result)
    test_sliding_window_log_precision(result)
    
    # FixedWindowCounter tests
    test_fixed_window_basic(result)
    test_fixed_window_expiration(result)
    
    # RateLimiter tests
    test_rate_limiter_multi_key(result)
    test_rate_limiter_strategies(result)
    
    # Decorator tests
    test_rate_limit_decorator(result)
    test_rate_limit_decorator_key_func(result)
    test_rate_limit_strict(result)
    test_rate_limit_context(result)
    
    # Utility tests
    test_rate_limit_result(result)
    test_generate_rate_limit_key(result)
    test_error_handling(result)
    test_consume_multiple_tokens(result)
    test_wait_time_calculation(result)
    
    # Summary
    success = result.summary()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
