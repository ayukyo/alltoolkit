"""
Comprehensive tests for memoization_utils.

Tests all memoization types: basic, LRU, TTL, disk, and async.
"""

import asyncio
import os
import shutil
import tempfile
import time
import unittest
from pathlib import Path

# Compatibility for Python 3.6 (asyncio.run not available)
def run_async(coro):
    """Run async coroutine (compatible with Python 3.6+)."""
    try:
        # Python 3.7+
        return asyncio.run(coro)
    except AttributeError:
        # Python 3.6 fallback
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()

from memoize import (
    memoize,
    memoize_method,
    MemoizeStats,
    MemoizeStore,
)

from lru_memoize import (
    lru_memoize,
    lru_memoize_method,
    LRUCache,
    clear_lru_caches,
    get_lru_cache_info,
)

from ttl_memoize import (
    ttl_memoize,
    ttl_memoize_method,
    TTLCache,
    clear_ttl_caches,
    get_ttl_cache_info,
    TTLMemoizeContext,
)

from disk_memoize import (
    disk_memoize,
    disk_memoize_method,
    DiskCache,
    clear_disk_cache,
    get_disk_cache_stats,
)

from async_memoize import (
    async_memoize,
    async_ttl_memoize,
    async_lru_memoize,
    AsyncLRUCache,
    AsyncTTLCache,
    clear_async_caches,
    AsyncMemoizeContext,
)


class TestMemoize(unittest.TestCase):
    """Tests for basic memoization."""
    
    def test_memoize_basic(self):
        """Test basic memoization."""
        call_count = [0]  # Use list to allow modification in closure
        
        @memoize()
        def expensive_func(x, y):
            call_count[0] += 1
            return x + y
        
        # First call
        result1 = expensive_func(1, 2)
        self.assertEqual(result1, 3)
        self.assertEqual(call_count[0], 1)
        
        # Second call (cached)
        result2 = expensive_func(1, 2)
        self.assertEqual(result2, 3)
        self.assertEqual(call_count[0], 1)
        
        # Different args
        result3 = expensive_func(2, 3)
        self.assertEqual(result3, 5)
        self.assertEqual(call_count[0], 2)
    
    def test_memoize_with_kwargs(self):
        """Test memoization with keyword arguments."""
        call_count = [0]  # Use list for closure
        
        @memoize()
        def func(a, b=10, c=20):
            call_count[0] += 1
            return a + b + c
        
        result1 = func(1)
        self.assertEqual(result1, 31)
        self.assertEqual(call_count[0], 1)
        
        result2 = func(1)
        self.assertEqual(call_count[0], 1)
        
        result3 = func(1, b=5)
        self.assertEqual(result3, 26)
        self.assertEqual(call_count[0], 2)
    
    def test_memoize_maxsize(self):
        """Test memoization with maxsize limit."""
        @memoize(maxsize=3)
        def func(x):
            return x * 2
        
        # Fill cache
        func(1)
        func(2)
        func(3)
        
        info = func.cache_info()
        self.assertEqual(info['size'], 3)
        
        # Add one more (should evict oldest)
        func(4)
        self.assertEqual(info['size'], 3)
    
    def test_memoize_method(self):
        """Test memoization for instance methods."""
        class Calculator:
            def __init__(self):
                self.call_count = 0
            
            @memoize_method()
            def compute(self, x, y):
                self.call_count += 1
                return x ** y
        
        calc1 = Calculator()
        calc2 = Calculator()
        
        # First call
        result1 = calc1.compute(2, 3)
        self.assertEqual(result1, 8)
        self.assertEqual(calc1.call_count, 1)
        
        # Cached call
        result2 = calc1.compute(2, 3)
        self.assertEqual(calc1.call_count, 1)
        
        # Different instance
        result3 = calc2.compute(2, 3)
        self.assertEqual(result3, 8)
        self.assertEqual(calc2.call_count, 1)
    
    def test_memoize_stats(self):
        """Test memoization statistics."""
        stats = MemoizeStats()
        
        @memoize(stats=stats)
        def func(x):
            return x
        
        func(1)
        func(1)
        func(2)
        func(1)
        
        self.assertEqual(stats.hits, 2)
        self.assertEqual(stats.misses, 2)
        self.assertEqual(stats.hit_rate, 0.5)
    
    def test_memoize_store(self):
        """Test MemoizeStore directly."""
        store = MemoizeStore(maxsize=2)
        
        store.set('a', 1)
        store.set('b', 2)
        
        found, value = store.get('a')
        self.assertTrue(found)
        self.assertEqual(value, 1)
        
        # Add third item (should evict oldest)
        store.set('c', 3)
        
        found, value = store.get('b')  # 'b' was evicted
        self.assertFalse(found)
    
    def test_cache_clear(self):
        """Test cache clearing."""
        @memoize()
        def func(x):
            return x
        
        func(1)
        func(2)
        
        info = func.cache_info()
        self.assertEqual(info['size'], 2)
        
        func.cache_clear()
        info = func.cache_info()
        self.assertEqual(info['size'], 0)


class TestLRUMemoize(unittest.TestCase):
    """Tests for LRU memoization."""
    
    def test_lru_memoize_basic(self):
        """Test basic LRU memoization."""
        call_count = [0]  # Use list for closure
        
        @lru_memoize(maxsize=3)
        def func(x):
            call_count[0] += 1
            return x * 2
        
        func(1)
        func(2)
        func(3)
        self.assertEqual(call_count[0], 3)
        
        # Access 1 (makes it most recent)
        func(1)
        self.assertEqual(call_count[0], 3)  # Cached
        
        # Add new item (evicts 2, which is now oldest)
        func(4)
        
        # 2 should be evicted
        func(2)
        self.assertEqual(call_count[0], 5)  # Computed again
    
    def test_lru_cache_info(self):
        """Test LRU cache info."""
        @lru_memoize(maxsize=5)
        def func(x):
            return x
        
        func(1)
        func(1)
        func(2)
        
        info = func.cache_info()
        self.assertEqual(info['hits'], 1)
        self.assertEqual(info['misses'], 2)
        self.assertEqual(info['size'], 2)
    
    def test_lru_memoize_method(self):
        """Test LRU memoization for methods."""
        class Counter:
            def __init__(self):
                self.calls = {}
            
            @lru_memoize_method(maxsize=10)
            def count(self, x):
                self.calls[x] = self.calls.get(x, 0) + 1
                return x
        
        c = Counter()
        c.count(1)
        c.count(1)
        c.count(2)
        
        self.assertEqual(c.calls[1], 1)  # Only called once
        self.assertEqual(c.calls[2], 1)
    
    def test_lru_cache_direct(self):
        """Test LRUCache directly."""
        cache = LRUCache(maxsize=3)
        
        cache.set('a', 1)
        cache.set('b', 2)
        cache.set('c', 3)
        
        found, val = cache.get('a')
        self.assertTrue(found)
        self.assertEqual(val, 1)
        
        cache.set('d', 4)  # Evicts 'b'
        
        found, _ = cache.get('b')
        self.assertFalse(found)
    
    def test_clear_lru_caches(self):
        """Test clearing all LRU caches."""
        @lru_memoize(maxsize=5, name='test_func')
        def func1(x):
            return x
        
        @lru_memoize(maxsize=5, name='test_func2')
        def func2(x):
            return x
        
        func1(1)
        func2(2)
        
        clear_lru_caches()
        
        info = get_lru_cache_info()
        for name, cache_info in info.items():
            self.assertEqual(cache_info['hits'], 0)


class TestTTLMemoize(unittest.TestCase):
    """Tests for TTL memoization."""
    
    def test_ttl_memoize_basic(self):
        """Test basic TTL memoization."""
        call_count = [0]  # Use list for closure
        
        @ttl_memoize(ttl=1.0)
        def func(x):
            call_count[0] += 1
            return x
        
        result1 = func(1)
        self.assertEqual(result1, 1)
        self.assertEqual(call_count[0], 1)
        
        # Cached
        result2 = func(1)
        self.assertEqual(call_count[0], 1)
        
        # Wait for expiration
        time.sleep(1.1)
        
        result3 = func(1)
        self.assertEqual(call_count[0], 2)
    
    def test_ttl_cache_info(self):
        """Test TTL cache info."""
        @ttl_memoize(ttl=5.0)
        def func(x):
            return x
        
        func(1)
        func(1)
        func(2)
        
        info = func.cache_info()
        self.assertEqual(info['stats'].hits, 1)
        self.assertEqual(info['stats'].misses, 2)
    
    def test_ttl_cache_direct(self):
        """Test TTLCache directly."""
        cache = TTLCache(default_ttl=0.5)
        
        cache.set('a', 1)
        
        found, val = cache.get('a')
        self.assertTrue(found)
        self.assertEqual(val, 1)
        
        time.sleep(0.6)
        
        found, _ = cache.get('a')
        self.assertFalse(found)
    
    def test_ttl_memoize_method(self):
        """Test TTL memoization for methods."""
        class Service:
            def __init__(self):
                self.calls = 0
            
            @ttl_memoize_method(ttl=1.0)
            def get_data(self, id):
                self.calls += 1
                return {'id': id}
        
        s = Service()
        s.get_data(1)
        s.get_data(1)
        
        self.assertEqual(s.calls, 1)
        
        time.sleep(1.1)
        
        s.get_data(1)
        self.assertEqual(s.calls, 2)
    
    def test_ttl_context(self):
        """Test TTLMemoizeContext."""
        with TTLMemoizeContext(ttl=0.5) as cache:
            @cache.decorate
            def func(x):
                return x * 2
            
            result = func(5)
            self.assertEqual(result, 10)
            
            result = func(5)  # Cached
            self.assertEqual(result, 10)


class TestDiskMemoize(unittest.TestCase):
    """Tests for disk-based memoization."""
    
    def setUp(self):
        """Create temp directory for tests."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up temp directory."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_disk_memoize_basic(self):
        """Test basic disk memoization."""
        call_count = [0]  # Use list for closure
        
        @disk_memoize(cache_dir=self.temp_dir, ttl=None)
        def func(x):
            call_count[0] += 1
            return x * 2
        
        result1 = func(5)
        self.assertEqual(result1, 10)
        self.assertEqual(call_count[0], 1)
        
        # Cached from disk
        result2 = func(5)
        self.assertEqual(call_count[0], 1)
    
    def test_disk_cache_persistence(self):
        """Test that disk cache persists."""
        cache_dir = self.temp_dir
        
        # Define function with disk cache
        @disk_memoize(cache_dir=cache_dir, ttl=None)
        def func(x):
            return x * 3
        
        # Call and cache
        result1 = func(3)
        self.assertEqual(result1, 9)
        
        # Check file exists
        cache_files = list(Path(cache_dir).glob('*.pkl'))
        self.assertTrue(len(cache_files) > 0)
    
    def test_disk_cache_ttl(self):
        """Test disk cache TTL."""
        @disk_memoize(cache_dir=self.temp_dir, ttl=0.5)
        def func(x):
            return x
        
        func(1)
        
        # Cached
        info = func.cache_info()
        self.assertEqual(info['size'], 1)
        
        # Wait for expiration
        time.sleep(0.6)
        
        func(1)
        # Entry should be expired
        info = func.cache_info()
        # After cleanup, expired entries are removed
    
    def test_disk_cache_clear(self):
        """Test disk cache clearing."""
        @disk_memoize(cache_dir=self.temp_dir)
        def func(x):
            return x
        
        func(1)
        func(2)
        
        info = func.cache_info()
        self.assertEqual(info['size'], 2)
        
        func.cache_clear()
        info = func.cache_info()
        self.assertEqual(info['size'], 0)
    
    def test_disk_cache_json_serializer(self):
        """Test disk cache with JSON serializer."""
        @disk_memoize(cache_dir=self.temp_dir, serializer="json")
        def func(x):
            return {"value": x}
        
        result = func(10)
        self.assertEqual(result["value"], 10)
        
        # Cached
        result2 = func(10)
        self.assertEqual(result2["value"], 10)


class TestAsyncMemoize(unittest.TestCase):
    """Tests for async memoization."""
    
    def test_async_memoize_basic(self):
        """Test basic async memoization."""
        call_count = [0]  # Use list for closure
        
        @async_memoize(maxsize=10)
        async def async_func(x):
            call_count[0] += 1
            await asyncio.sleep(0.01)
            return x * 2
        
        async def run():
            result1 = await async_func(5)
            self.assertEqual(result1, 10)
            self.assertEqual(call_count[0], 1)
            
            # Cached
            result2 = await async_func(5)
            self.assertEqual(call_count[0], 1)
            
            # Different args
            result3 = await async_func(3)
            self.assertEqual(result3, 6)
            self.assertEqual(call_count[0], 2)
        
        run_async(run())
    
    def test_async_ttl_memoize(self):
        """Test async TTL memoization."""
        call_count = [0]  # Use list for closure
        
        @async_ttl_memoize(ttl=0.5)
        async def async_func(x):
            call_count[0] += 1
            return x
        
        async def run():
            await async_func(1)
            self.assertEqual(call_count[0], 1)
            
            await async_func(1)
            self.assertEqual(call_count[0], 1)
            
            await asyncio.sleep(0.6)
            
            await async_func(1)
            self.assertEqual(call_count[0], 2)
        
        run_async(run())
    
    def test_async_cache_info(self):
        """Test async cache info."""
        @async_memoize(maxsize=10)
        async def func(x):
            return x
        
        async def run():
            await func(1)
            await func(1)
            await func(2)
            
            info = func.cache_info()
            self.assertEqual(info['hits'], 1)
            self.assertEqual(info['misses'], 2)
        
        run_async(run())
    
    def test_async_context(self):
        """Test AsyncMemoizeContext."""
        async def run():
            async with AsyncMemoizeContext(maxsize=10) as cache:
                @cache.decorate
                async def func(x):
                    await asyncio.sleep(0.01)
                    return x * 2
                
                result = await func(5)
                self.assertEqual(result, 10)
                
                result2 = await func(5)  # Cached
                self.assertEqual(result2, 10)
        
        run_async(run())
    
    def test_async_lru_cache_direct(self):
        """Test AsyncLRUCache directly."""
        cache = AsyncLRUCache(maxsize=3)
        
        async def run():
            await cache.set('a', 1)
            await cache.set('b', 2)
            
            found, val = await cache.get('a')
            self.assertTrue(found)
            self.assertEqual(val, 1)
            
            info = cache.info()
            self.assertEqual(info['hits'], 1)
        
        run_async(run())


class TestIntegration(unittest.TestCase):
    """Integration tests combining multiple memoization types."""
    
    def test_mixed_decorators(self):
        """Test using multiple memoization types together."""
        @memoize()
        def basic_func(x):
            return x
        
        @lru_memoize(maxsize=5)
        def lru_func(x):
            return x
        
        @ttl_memoize(ttl=60)
        def ttl_func(x):
            return x
        
        basic_func(1)
        lru_func(1)
        ttl_func(1)
        
        # All should cache
        self.assertEqual(basic_func.cache_info()['size'], 1)
        self.assertEqual(lru_func.cache_info()['size'], 1)
        self.assertEqual(ttl_func.cache_info()['size'], 1)
    
    def test_fibonacci_memoized(self):
        """Test Fibonacci with memoization."""
        @memoize()
        def fib(n):
            if n < 2:
                return n
            return fib(n-1) + fib(n-2)
        
        result = fib(20)
        self.assertEqual(result, 6765)
        
        # Should be very fast due to memoization
        result2 = fib(20)
        self.assertEqual(result2, 6765)


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and error handling."""
    
    def test_memoize_unhashable_args(self):
        """Test memoization with unhashable arguments using hash key."""
        @memoize(use_hash=True)
        def func(data):
            return len(data)
        
        # Lists are unhashable normally
        result = func([1, 2, 3])
        self.assertEqual(result, 3)
        
        # Should cache via hash
        result2 = func([1, 2, 3])
        self.assertEqual(result2, 3)
    
    def test_lru_cache_zero_maxsize(self):
        """Test that LRU cache rejects zero maxsize."""
        with self.assertRaises(ValueError):
            LRUCache(maxsize=0)
    
    def test_memoize_none_result(self):
        """Test memoization of None results."""
        call_count = [0]  # Use list for closure
        
        @memoize()
        def func(x):
            call_count[0] += 1
            return None
        
        result1 = func(1)
        self.assertIsNone(result1)
        self.assertEqual(call_count[0], 1)
        
        # Should still cache None
        result2 = func(1)
        self.assertEqual(call_count[0], 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)