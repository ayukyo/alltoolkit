"""
Memoization Utils 测试

Author: AllToolkit
Date: 2026-04-23
"""

import sys
import os
import time
import threading
import unittest

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    MemoCache,
    memoize,
    memoize_method,
    MemoizedFunction,
    lru_cache,
    ttl_cache,
    cached_property,
    expire_after,
)


class TestMemoCache(unittest.TestCase):
    """MemoCache 测试"""
    
    def test_basic_get_set(self):
        """测试基本的获取和设置"""
        cache = MemoCache(max_size=10)
        
        # 设置值
        cache.set((1,), {}, "value1")
        found, value = cache.get((1,), {})
        self.assertTrue(found)
        self.assertEqual(value, "value1")
        
        # 不存在的键
        found, value = cache.get((2,), {})
        self.assertFalse(found)
        self.assertIsNone(value)
    
    def test_ttl_expiration(self):
        """测试 TTL 过期"""
        cache = MemoCache(max_size=10, ttl=0.1)  # 100ms TTL
        
        cache.set(("key",), {}, "value")
        
        # 立即获取应该存在
        found, value = cache.get(("key",), {})
        self.assertTrue(found)
        self.assertEqual(value, "value")
        
        # 等待过期
        time.sleep(0.15)
        found, value = cache.get(("key",), {})
        self.assertFalse(found)
    
    def test_lru_eviction(self):
        """测试 LRU 淘汰"""
        cache = MemoCache(max_size=3)
        
        cache.set((1,), {}, "v1")
        cache.set((2,), {}, "v2")
        cache.set((3,), {}, "v3")
        
        # 添加第4个，应该淘汰第1个
        cache.set((4,), {}, "v4")
        
        found, _ = cache.get((1,), {})
        self.assertFalse(found)
        
        # 第2个应该还在
        found, _ = cache.get((2,), {})
        self.assertTrue(found)
    
    def test_lru_access_order(self):
        """测试 LRU 访问顺序"""
        cache = MemoCache(max_size=3)
        
        cache.set((1,), {}, "v1")
        cache.set((2,), {}, "v2")
        cache.set((3,), {}, "v3")
        
        # 访问第1个，使其变成最新
        cache.get((1,), {})
        
        # 添加第4个，应该淘汰第2个（最旧的）
        cache.set((4,), {}, "v4")
        
        found, _ = cache.get((1,), {})
        self.assertTrue(found)
        
        found, _ = cache.get((2,), {})
        self.assertFalse(found)
    
    def test_stats(self):
        """测试统计信息"""
        cache = MemoCache(max_size=10, ttl=60)
        
        cache.set((1,), {}, "v1")
        
        # 命中
        cache.get((1,), {})
        cache.get((1,), {})
        
        # 未命中
        cache.get((2,), {})
        
        stats = cache.stats()
        self.assertEqual(stats['hits'], 2)
        self.assertEqual(stats['misses'], 1)
        self.assertEqual(stats['size'], 1)
    
    def test_clear(self):
        """测试清空缓存"""
        cache = MemoCache(max_size=10)
        
        cache.set((1,), {}, "v1")
        cache.set((2,), {}, "v2")
        
        cache.clear()
        
        self.assertEqual(cache.size, 0)
        self.assertEqual(cache.hits, 0)
        self.assertEqual(cache.misses, 0)
    
    def test_kwargs(self):
        """测试关键字参数"""
        cache = MemoCache(max_size=10)
        
        cache.set((1, 2), {'a': 3, 'b': 4}, "value")
        
        found, value = cache.get((1, 2), {'a': 3, 'b': 4})
        self.assertTrue(found)
        self.assertEqual(value, "value")
        
        # 不同的 kwargs 应该是不同的键
        found, _ = cache.get((1, 2), {'a': 3, 'b': 5})
        self.assertFalse(found)


class TestMemoize(unittest.TestCase):
    """memoize 装饰器测试"""
    
    def test_basic_memoization(self):
        """测试基本记忆化"""
        call_count = 0
        
        @memoize()
        def expensive(n):
            nonlocal call_count
            call_count += 1
            return n * n
        
        # 第一次调用
        result1 = expensive(5)
        self.assertEqual(result1, 25)
        self.assertEqual(call_count, 1)
        
        # 第二次调用，应该使用缓存
        result2 = expensive(5)
        self.assertEqual(result2, 25)
        self.assertEqual(call_count, 1)  # 没有增加
        
        # 不同参数
        result3 = expensive(6)
        self.assertEqual(result3, 36)
        self.assertEqual(call_count, 2)
    
    def test_memoize_with_ttl(self):
        """测试带 TTL 的记忆化"""
        call_count = 0
        
        @memoize(ttl=0.1)
        def get_time():
            nonlocal call_count
            call_count += 1
            return time.time()
        
        t1 = get_time()
        t2 = get_time()
        self.assertEqual(t1, t2)
        
        time.sleep(0.15)
        t3 = get_time()
        self.assertNotEqual(t1, t3)
    
    def test_cache_interface(self):
        """测试缓存接口"""
        @memoize(max_size=10)
        def func(n):
            return n * 2
        
        func(1)
        func(2)
        func(1)  # 缓存命中
        
        stats = func.cache_stats()
        self.assertEqual(stats['hits'], 1)
        # 两个唯一参数，双重检查导致更多 misses（线程安全）
        self.assertGreaterEqual(stats['misses'], 2)
        
        func.cache_clear()
        stats = func.cache_stats()
        self.assertEqual(stats['size'], 0)


class TestMemoizeMethod(unittest.TestCase):
    """memoize_method 装饰器测试"""
    
    def test_method_memoization(self):
        """测试方法记忆化"""
        
        class Calculator:
            def __init__(self):
                self.call_count = 0
            
            @memoize_method()
            def fibonacci(self, n):
                self.call_count += 1
                if n <= 1:
                    return n
                return self.fibonacci(n-1) + self.fibonacci(n-2)
        
        calc = Calculator()
        result = calc.fibonacci(10)
        self.assertEqual(result, 55)
        
        # 第二次调用，应该全部使用缓存
        first_count = calc.call_count
        result2 = calc.fibonacci(10)
        self.assertEqual(result2, 55)
        self.assertEqual(calc.call_count, first_count)
    
    def test_multiple_instances(self):
        """测试多实例独立缓存"""
        
        class Counter:
            def __init__(self, base):
                self.base = base
            
            @memoize_method()
            def add(self, n):
                return self.base + n
        
        c1 = Counter(10)
        c2 = Counter(20)
        
        self.assertEqual(c1.add(5), 15)
        self.assertEqual(c2.add(5), 25)


class TestMemoizedFunction(unittest.TestCase):
    """MemoizedFunction 类测试"""
    
    def test_class_decorator(self):
        """测试类装饰器"""
        
        @MemoizedFunction(ttl=60)
        def compute(n):
            return n ** 3
        
        self.assertEqual(compute(3), 27)
        self.assertEqual(compute(3), 27)  # 缓存
        
        stats = compute.cache.stats()
        self.assertEqual(stats['hits'], 1)
    
    def test_wrap_method(self):
        """测试 wrap 方法"""
        def func(n):
            return n * 10
        
        mf = MemoizedFunction(max_size=5)
        wrapped = mf.wrap(func)
        
        self.assertEqual(wrapped(5), 50)


class TestLRUCache(unittest.TestCase):
    """lru_cache 装饰器测试"""
    
    def test_lru_cache(self):
        """测试 LRU 缓存"""
        call_count = 0
        
        @lru_cache(max_size=3)
        def func(n):
            nonlocal call_count
            call_count += 1
            return n
        
        func(1)
        func(2)
        func(3)
        func(4)  # 淘汰 1
        
        # 1 需要重新计算
        func(1)
        self.assertEqual(call_count, 5)


class TestTTLCache(unittest.TestCase):
    """ttl_cache 装饰器测试"""
    
    def test_ttl_cache(self):
        """测试 TTL 缓存"""
        call_count = 0
        
        @ttl_cache(ttl=0.1)
        def func():
            nonlocal call_count
            call_count += 1
            return call_count
        
        self.assertEqual(func(), 1)
        self.assertEqual(func(), 1)  # 缓存
        
        time.sleep(0.15)
        self.assertEqual(func(), 2)  # 重新计算


class TestCachedProperty(unittest.TestCase):
    """cached_property 装饰器测试"""
    
    def test_cached_property(self):
        """测试缓存属性"""
        
        class Data:
            @cached_property
            def expensive(self):
                return [1, 2, 3]
        
        d = Data()
        v1 = d.expensive
        v2 = d.expensive
        self.assertIs(v1, v2)


class TestExpireAfter(unittest.TestCase):
    """expire_after 装饰器测试"""
    
    def test_expire_after(self):
        """测试定时过期"""
        
        @expire_after(0.1)
        def func():
            return time.time()
        
        t1 = func()
        time.sleep(0.05)
        t2 = func()
        self.assertEqual(t1, t2)
        
        time.sleep(0.1)
        t3 = func()
        self.assertNotEqual(t1, t3)


class TestThreadSafety(unittest.TestCase):
    """线程安全测试"""
    
    def test_concurrent_access(self):
        """测试并发访问"""
        call_count = 0
        
        @memoize(thread_safe=True)
        def func(n):
            nonlocal call_count
            call_count += 1
            time.sleep(0.01)
            return n * 2
        
        threads = []
        results = []
        lock = threading.Lock()
        
        def worker(n):
            result = func(n)
            with lock:
                results.append(result)
        
        # 创建多个线程同时访问
        for i in range(10):
            t = threading.Thread(target=worker, args=(i % 5,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        # 应该只有 5 次实际调用（每个唯一参数一次）
        self.assertEqual(call_count, 5)
        self.assertEqual(len(results), 10)


if __name__ == '__main__':
    unittest.main(verbosity=2)