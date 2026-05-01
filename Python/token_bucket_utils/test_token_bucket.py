"""
Unit tests for Token Bucket Utils

Tests all components:
- TokenBucket: Basic implementation
- ThreadSafeTokenBucket: Thread-safe version
- HierarchicalTokenBucket: Multi-level rate limiting
- SlidingWindowBucket: Hybrid sliding window

Run with: python -m pytest test_token_bucket.py -v
"""

import time
import threading
import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from token_bucket_utils import (
    TokenBucket,
    ThreadSafeTokenBucket,
    HierarchicalTokenBucket,
    SlidingWindowBucket
)


class TestTokenBucket(unittest.TestCase):
    """Tests for basic TokenBucket."""
    
    def test_initial_state(self):
        """Bucket starts full."""
        bucket = TokenBucket(capacity=10, refill_rate=1)
        self.assertEqual(bucket.available(), 10.0)
    
    def test_consume_reduces_tokens(self):
        """Consuming tokens reduces available count."""
        bucket = TokenBucket(capacity=10, refill_rate=1)
        self.assertTrue(bucket.consume(3))
        self.assertAlmostEqual(bucket.available(), 7.0, places=1)
    
    def test_consume_insufficient_tokens(self):
        """Cannot consume more tokens than available."""
        bucket = TokenBucket(capacity=10, refill_rate=1)
        self.assertTrue(bucket.consume(8))
        self.assertFalse(bucket.consume(5))  # Only 2 left
    
    def test_refill_over_time(self):
        """Tokens refill over time."""
        bucket = TokenBucket(capacity=10, refill_rate=10)  # 10 tokens/sec
        bucket.consume(10)  # Empty the bucket
        self.assertAlmostEqual(bucket.available(), 0.0, places=2)
        
        time.sleep(0.5)  # Should refill 5 tokens
        self.assertAlmostEqual(bucket.available(), 5.0, places=0)
    
    def test_capacity_limit(self):
        """Bucket cannot exceed capacity."""
        bucket = TokenBucket(capacity=10, refill_rate=100)
        time.sleep(0.1)  # Would refill 10 tokens, but already full
        self.assertEqual(bucket.available(), 10.0)
    
    def test_wait_time(self):
        """Wait time calculation is correct."""
        bucket = TokenBucket(capacity=10, refill_rate=10)  # 10 tokens/sec
        bucket.consume(10)  # Empty
        self.assertAlmostEqual(bucket.wait_time(5), 0.5, places=1)
    
    def test_wait_time_available(self):
        """Wait time is zero when tokens available."""
        bucket = TokenBucket(capacity=10, refill_rate=1)
        self.assertEqual(bucket.wait_time(5), 0.0)
    
    def test_reset(self):
        """Reset restores full capacity."""
        bucket = TokenBucket(capacity=10, refill_rate=1)
        bucket.consume(10)
        bucket.reset()
        self.assertEqual(bucket.available(), 10.0)
    
    def test_invalid_capacity(self):
        """Invalid capacity raises error."""
        with self.assertRaises(ValueError):
            TokenBucket(capacity=0, refill_rate=1)
        with self.assertRaises(ValueError):
            TokenBucket(capacity=-1, refill_rate=1)
    
    def test_invalid_refill_rate(self):
        """Invalid refill rate raises error."""
        with self.assertRaises(ValueError):
            TokenBucket(capacity=10, refill_rate=0)
        with self.assertRaises(ValueError):
            TokenBucket(capacity=10, refill_rate=-1)
    
    def test_consume_zero_tokens(self):
        """Consuming zero tokens raises error."""
        bucket = TokenBucket(capacity=10, refill_rate=1)
        with self.assertRaises(ValueError):
            bucket.consume(0)
    
    def test_consume_negative_tokens(self):
        """Consuming negative tokens raises error."""
        bucket = TokenBucket(capacity=10, refill_rate=1)
        with self.assertRaises(ValueError):
            bucket.consume(-1)


class TestThreadSafeTokenBucket(unittest.TestCase):
    """Tests for thread-safe TokenBucket."""
    
    def test_initial_state(self):
        """Bucket starts full."""
        bucket = ThreadSafeTokenBucket(capacity=10, refill_rate=1)
        self.assertEqual(bucket.available(), 10.0)
    
    def test_consume_thread_safe(self):
        """Consume works correctly."""
        bucket = ThreadSafeTokenBucket(capacity=10, refill_rate=1)
        self.assertTrue(bucket.consume(5))
        self.assertAlmostEqual(bucket.available(), 5.0, places=1)
    
    def test_concurrent_access(self):
        """Multiple threads can safely access bucket."""
        bucket = ThreadSafeTokenBucket(capacity=100, refill_rate=10)
        success_count = [0]
        lock = threading.Lock()
        
        def consumer():
            for _ in range(20):
                if bucket.consume(1):
                    with lock:
                        success_count[0] += 1
        
        threads = [threading.Thread(target=consumer) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Should have ~100 successes (initial capacity)
        self.assertGreaterEqual(success_count[0], 90)
        self.assertLessEqual(success_count[0], 100)
    
    def test_consume_blocking(self):
        """Blocking consume waits for tokens."""
        bucket = ThreadSafeTokenBucket(capacity=5, refill_rate=20)  # 20 tokens/sec
        self.assertTrue(bucket.consume(5))  # Empty bucket
        # Need 5 tokens, at 20/sec = 0.25s, give 1s timeout
        self.assertTrue(bucket.consume_blocking(5, timeout=1.0))  # Wait for refill
    
    def test_consume_blocking_timeout(self):
        """Blocking consume respects timeout."""
        bucket = ThreadSafeTokenBucket(capacity=1, refill_rate=0.1)  # Very slow
        bucket.consume(1)
        self.assertFalse(bucket.consume_blocking(100, timeout=0.1))
    
    def test_callback_on_limited(self):
        """Callback is called when rate limited."""
        calls = []
        
        def on_limited(needed, wait):
            calls.append((needed, wait))
        
        bucket = ThreadSafeTokenBucket(
            capacity=5, 
            refill_rate=1,
            on_limited=on_limited
        )
        bucket.consume(5)  # Empty
        bucket.consume_blocking(10, timeout=0.1)  # Trigger callback
        
        self.assertTrue(len(calls) > 0)
    
    def test_context_manager(self):
        """Context manager works correctly."""
        bucket = ThreadSafeTokenBucket(capacity=10, refill_rate=1)
        
        with bucket.consume_or_wait(5) as acquired:
            self.assertTrue(acquired)
        
        self.assertAlmostEqual(bucket.available(), 5.0, places=1)


class TestHierarchicalTokenBucket(unittest.TestCase):
    """Tests for hierarchical token bucket."""
    
    def test_empty_hierarchy(self):
        """Empty hierarchy raises error on consume."""
        bucket = HierarchicalTokenBucket()
        with self.assertRaises(RuntimeError):
            bucket.consume(1)
    
    def test_single_level(self):
        """Single level works like basic bucket."""
        bucket = HierarchicalTokenBucket()
        bucket.add_level(capacity=10, refill_rate=1)
        
        success, failed = bucket.consume(5)
        self.assertTrue(success)
        self.assertIsNone(failed)
    
    def test_multi_level_pass(self):
        """Request passes all levels."""
        bucket = HierarchicalTokenBucket()
        bucket.add_level(capacity=100, refill_rate=10)  # Global
        bucket.add_level(capacity=10, refill_rate=2)     # User
        
        success, failed = bucket.consume(5)
        self.assertTrue(success)
        self.assertIsNone(failed)
    
    def test_multi_level_fail_first(self):
        """Request fails at first level."""
        bucket = HierarchicalTokenBucket()
        bucket.add_level(capacity=5, refill_rate=1, name="global")
        bucket.add_level(capacity=100, refill_rate=10, name="user")
        
        success, failed = bucket.consume(10)
        self.assertFalse(success)
        self.assertEqual(failed, "global")
    
    def test_multi_level_fail_second(self):
        """Request fails at second level."""
        bucket = HierarchicalTokenBucket()
        bucket.add_level(capacity=100, refill_rate=10, name="global")
        bucket.add_level(capacity=5, refill_rate=1, name="user")
        
        success, failed = bucket.consume(10)
        self.assertFalse(success)
        self.assertEqual(failed, "user")
    
    def test_available_all_levels(self):
        """Available returns minimum across levels."""
        bucket = HierarchicalTokenBucket()
        bucket.add_level(capacity=100, refill_rate=10)
        bucket.add_level(capacity=10, refill_rate=1)
        
        self.assertEqual(bucket.available(), 10.0)
    
    def test_status(self):
        """Status shows all levels."""
        bucket = HierarchicalTokenBucket()
        bucket.add_level(capacity=100, refill_rate=10, name="global")
        bucket.add_level(capacity=10, refill_rate=2, name="user")
        
        status = bucket.status()
        self.assertEqual(len(status), 2)
        self.assertEqual(status[0]['name'], 'global')
        self.assertEqual(status[1]['name'], 'user')
    
    def test_reset_all(self):
        """Reset all levels."""
        bucket = HierarchicalTokenBucket()
        bucket.add_level(capacity=10, refill_rate=1)
        bucket.consume(10)
        bucket.reset()
        self.assertEqual(bucket.available(), 10.0)
    
    def test_reset_specific_level(self):
        """Reset specific level."""
        bucket = HierarchicalTokenBucket()
        bucket.add_level(capacity=10, refill_rate=1, name="level1")
        bucket.add_level(capacity=5, refill_rate=1, name="level2")
        
        bucket.consume(3)
        bucket.reset(level=0)  # Reset first level only
        
        status = bucket.status()
        self.assertEqual(status[0]['tokens'], 10.0)  # Reset
        self.assertLess(status[1]['tokens'], 5.0)     # Not reset


class TestSlidingWindowBucket(unittest.TestCase):
    """Tests for sliding window bucket."""
    
    def test_initial_state(self):
        """Bucket starts full."""
        bucket = SlidingWindowBucket(capacity=10, rate=5, window_size=1.0)
        self.assertEqual(bucket.available(), 10.0)
    
    def test_consume_within_limit(self):
        """Consume within limit succeeds."""
        bucket = SlidingWindowBucket(capacity=10, rate=10, window_size=1.0)
        
        for _ in range(5):
            self.assertTrue(bucket.consume(1))
    
    def test_consume_exceeds_burst(self):
        """Consume exceeding burst capacity fails."""
        bucket = SlidingWindowBucket(capacity=10, rate=10, window_size=1.0)
        self.assertFalse(bucket.consume(20))
    
    def test_sliding_window_enforcement(self):
        """Sliding window correctly tracks requests."""
        bucket = SlidingWindowBucket(capacity=100, rate=10, window_size=0.5)
        
        # Make 5 requests (within window limit of 5 for 0.5s window)
        for _ in range(5):
            self.assertTrue(bucket.consume(1))
        
        # Wait for window to slide
        time.sleep(0.6)
        
        # Should be able to make more requests
        self.assertTrue(bucket.consume(1))
    
    def test_requests_in_window(self):
        """Request count is tracked."""
        bucket = SlidingWindowBucket(capacity=100, rate=10, window_size=1.0)
        
        for _ in range(5):
            bucket.consume(1)
        
        self.assertEqual(bucket.requests_in_window(), 5)
    
    def test_reset(self):
        """Reset clears all requests."""
        bucket = SlidingWindowBucket(capacity=10, rate=5, window_size=1.0)
        
        for _ in range(5):
            bucket.consume(1)
        
        bucket.reset()
        self.assertEqual(bucket.available(), 10.0)
        self.assertEqual(bucket.requests_in_window(), 0)
    
    def test_invalid_parameters(self):
        """Invalid parameters raise errors."""
        with self.assertRaises(ValueError):
            SlidingWindowBucket(capacity=0, rate=1, window_size=1)
        with self.assertRaises(ValueError):
            SlidingWindowBucket(capacity=10, rate=0, window_size=1)
        with self.assertRaises(ValueError):
            SlidingWindowBucket(capacity=10, rate=1, window_size=0)


class TestIntegration(unittest.TestCase):
    """Integration tests for real-world scenarios."""
    
    def test_api_rate_limiting(self):
        """Simulate API rate limiting scenario."""
        # 100 requests per minute = 1.67/sec, burst of 10
        bucket = TokenBucket(capacity=10, refill_rate=100/60)
        
        # Burst of 10 requests
        for _ in range(10):
            self.assertTrue(bucket.consume(1))
        
        # 11th request denied
        self.assertFalse(bucket.consume(1))
        
        # Wait for refill
        time.sleep(0.6)  # ~1 token refilled
        self.assertTrue(bucket.consume(1))
    
    def test_thread_safe_web_server(self):
        """Simulate web server with rate limiting."""
        bucket = ThreadSafeTokenBucket(capacity=100, refill_rate=10)
        results = []
        
        def handler():
            if bucket.consume(1):
                results.append('success')
            else:
                results.append('limited')
        
        threads = [threading.Thread(target=handler) for _ in range(150)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Exactly 100 successes (burst capacity)
        self.assertEqual(results.count('success'), 100)
        self.assertEqual(results.count('limited'), 50)
    
    def test_hierarchical_api_limits(self):
        """Simulate global + per-user rate limiting."""
        bucket = HierarchicalTokenBucket()
        bucket.add_level(capacity=1000, refill_rate=100, name="global")
        bucket.add_level(capacity=10, refill_rate=2, name="user")
        
        # Within both limits
        success, _ = bucket.consume(5)
        self.assertTrue(success)
        
        # Exceeds user limit
        success, level = bucket.consume(20)
        self.assertFalse(success)
        self.assertEqual(level, "user")


if __name__ == '__main__':
    unittest.main()