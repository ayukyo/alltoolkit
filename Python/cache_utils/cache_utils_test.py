"""
cache_utils 测试文件

测试覆盖：
- 基本读写操作
- TTL 过期机制
- LRU 淘汰策略
- 线程安全性
- 缓存统计
- 装饰器功能
- 多级缓存
"""

import time
import threading
import random
import unittest
from mod import (
    MemoryCache, CacheStats, CacheEntry, TimedCache,
    MultiLevelCache, CacheManager, cached, create_cache
)


class TestCacheStats(unittest.TestCase):
    """测试 CacheStats"""
    
    def test_initial_state(self):
        """测试初始状态"""
        stats = CacheStats()
        self.assertEqual(stats.hits, 0)
        self.assertEqual(stats.misses, 0)
        self.assertEqual(stats.evictions, 0)
        self.assertEqual(stats.total_requests, 0)
        self.assertEqual(stats.hit_rate, 0.0)
    
    def test_record_operations(self):
        """测试记录操作"""
        stats = CacheStats()
        stats.record_hit()
        stats.record_hit()
        stats.record_miss()
        stats.record_eviction()
        stats.record_expiration()
        
        self.assertEqual(stats.hits, 2)
        self.assertEqual(stats.misses, 1)
        self.assertEqual(stats.evictions, 1)
        self.assertEqual(stats.expirations, 1)
        self.assertEqual(stats.total_requests, 3)
        self.assertAlmostEqual(stats.hit_rate, 2/3)
    
    def test_reset(self):
        """测试重置"""
        stats = CacheStats()
        stats.record_hit()
        stats.record_miss()
        stats.reset()
        self.assertEqual(stats.hits, 0)
        self.assertEqual(stats.misses, 0)
    
    def test_to_dict(self):
        """测试字典转换"""
        stats = CacheStats()
        stats.record_hit()
        d = stats.to_dict()
        self.assertIn('hits', d)
        self.assertIn('misses', d)
        self.assertIn('hit_rate', d)


class TestCacheEntry(unittest.TestCase):
    """测试 CacheEntry"""
    
    def test_basic_entry(self):
        """测试基本条目"""
        entry = CacheEntry("test_value")
        self.assertEqual(entry.value, "test_value")
        self.assertIsNone(entry.expires_at)
        self.assertFalse(entry.is_expired())
        self.assertIsNone(entry.remaining_ttl())
    
    def test_entry_with_ttl(self):
        """测试带 TTL 的条目"""
        entry = CacheEntry("test_value", ttl=2)
        self.assertIsNotNone(entry.expires_at)
        self.assertFalse(entry.is_expired())
        self.assertGreater(entry.remaining_ttl(), 1.9)
    
    def test_entry_expiration(self):
        """测试条目过期"""
        entry = CacheEntry("test_value", ttl=0.1)
        self.assertFalse(entry.is_expired())
        time.sleep(0.15)
        self.assertTrue(entry.is_expired())
        self.assertEqual(entry.remaining_ttl(), 0)
    
    def test_touch(self):
        """测试访问更新"""
        entry = CacheEntry("test")
        original_time = entry.last_access
        original_count = entry.access_count
        time.sleep(0.01)
        entry.touch()
        self.assertGreater(entry.last_access, original_time)
        self.assertEqual(entry.access_count, original_count + 1)


class TestMemoryCache(unittest.TestCase):
    """测试 MemoryCache"""
    
    def test_basic_operations(self):
        """测试基本操作"""
        cache = MemoryCache()
        cache.set('key1', 'value1')
        self.assertEqual(cache.get('key1'), 'value1')
        self.assertIsNone(cache.get('nonexistent'))
        self.assertEqual(cache.get('nonexistent', 'default'), 'default')
    
    def test_delete(self):
        """测试删除"""
        cache = MemoryCache()
        cache.set('key', 'value')
        self.assertTrue(cache.delete('key'))
        self.assertFalse(cache.delete('key'))
        self.assertIsNone(cache.get('key'))
    
    def test_exists(self):
        """测试存在检查"""
        cache = MemoryCache()
        cache.set('key', 'value')
        self.assertTrue(cache.exists('key'))
        self.assertFalse(cache.exists('nonexistent'))
    
    def test_clear(self):
        """测试清空"""
        cache = MemoryCache()
        cache.set('a', 1)
        cache.set('b', 2)
        cache.clear()
        self.assertEqual(cache.size(), 0)
    
    def test_size(self):
        """测试大小"""
        cache = MemoryCache()
        self.assertEqual(cache.size(), 0)
        cache.set('a', 1)
        self.assertEqual(cache.size(), 1)
        cache.set('b', 2)
        self.assertEqual(cache.size(), 2)
    
    def test_lru_eviction(self):
        """测试 LRU 淘汰"""
        cache = MemoryCache(max_size=3)
        cache.set('a', 1)
        cache.set('b', 2)
        cache.set('c', 3)
        
        # 访问 'a'，使其成为最近使用
        cache.get('a')
        
        # 添加 'd'，应该淘汰 'b'（最久未使用）
        cache.set('d', 4)
        
        self.assertTrue(cache.exists('a'))
        self.assertFalse(cache.exists('b'))
        self.assertTrue(cache.exists('c'))
        self.assertTrue(cache.exists('d'))
        
        stats = cache.get_stats()
        self.assertEqual(stats.evictions, 1)
    
    def test_ttl_expiration(self):
        """测试 TTL 过期"""
        cache = MemoryCache(default_ttl=0.5)
        cache.set('key', 'value')
        self.assertEqual(cache.get('key'), 'value')
        time.sleep(0.6)
        self.assertIsNone(cache.get('key'))
    
    def test_per_key_ttl(self):
        """测试单键 TTL"""
        cache = MemoryCache()
        cache.set('short', 'value', ttl=0.3)
        cache.set('long', 'value', ttl=10)
        
        time.sleep(0.4)
        self.assertIsNone(cache.get('short'))
        self.assertEqual(cache.get('long'), 'value')
    
    def test_cleanup_expired(self):
        """测试过期清理"""
        cache = MemoryCache()
        cache.set('a', 1, ttl=0.1)
        cache.set('b', 2, ttl=0.1)
        cache.set('c', 3, ttl=10)
        
        time.sleep(0.15)
        cleaned = cache.cleanup_expired()
        
        self.assertEqual(cleaned, 2)
        self.assertEqual(cache.size(), 1)
    
    def test_get_or_set(self):
        """测试 get_or_set"""
        cache = MemoryCache()
        call_count = [0]
        
        def factory():
            call_count[0] += 1
            return 'computed'
        
        # 第一次调用，应该执行 factory
        result1 = cache.get_or_set('key', factory)
        self.assertEqual(result1, 'computed')
        self.assertEqual(call_count[0], 1)
        
        # 第二次调用，应该从缓存获取
        result2 = cache.get_or_set('key', factory)
        self.assertEqual(result2, 'computed')
        self.assertEqual(call_count[0], 1)
    
    def test_dict_interface(self):
        """测试字典接口"""
        cache = MemoryCache()
        
        # __setitem__, __getitem__
        cache['key'] = 'value'
        self.assertEqual(cache['key'], 'value')
        
        # __contains__
        self.assertTrue('key' in cache)
        self.assertFalse('nonexistent' in cache)
        
        # __delitem__
        del cache['key']
        with self.assertRaises(KeyError):
            _ = cache['key']
        
        # __len__
        cache['a'] = 1
        cache['b'] = 2
        self.assertEqual(len(cache), 2)
    
    def test_stats_tracking(self):
        """测试统计追踪"""
        cache = MemoryCache()
        
        cache.set('key', 'value')
        
        # 命中
        cache.get('key')
        cache.get('key')
        
        # 未命中
        cache.get('nonexistent')
        
        stats = cache.get_stats()
        self.assertEqual(stats.hits, 2)
        self.assertEqual(stats.misses, 1)


class TestThreadSafety(unittest.TestCase):
    """测试线程安全性"""
    
    def test_concurrent_writes(self):
        """测试并发写入"""
        cache = MemoryCache(max_size=1000, thread_safe=True)
        errors = []
        
        def writer(start):
            try:
                for i in range(100):
                    cache.set(f'key_{start}_{i}', i)
            except Exception as e:
                errors.append(e)
        
        threads = [
            threading.Thread(target=writer, args=(i,))
            for i in range(10)
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        self.assertEqual(len(errors), 0)
    
    def test_concurrent_reads_writes(self):
        """测试并发读写"""
        cache = MemoryCache(max_size=1000, thread_safe=True)
        
        # 预填充
        for i in range(100):
            cache.set(f'key_{i}', i)
        
        errors = []
        
        def reader():
            try:
                for _ in range(100):
                    key = f'key_{random.randint(0, 99)}'
                    cache.get(key)
            except Exception as e:
                errors.append(e)
        
        def writer():
            try:
                for i in range(100):
                    cache.set(f'key_{i}', i * 2)
            except Exception as e:
                errors.append(e)
        
        threads = [
            threading.Thread(target=reader) for _ in range(5)
        ] + [
            threading.Thread(target=writer) for _ in range(2)
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        self.assertEqual(len(errors), 0)


class TestCachedDecorator(unittest.TestCase):
    """测试 cached 装饰器"""
    
    def test_basic_caching(self):
        """测试基本缓存功能"""
        call_count = [0]
        
        @cached(ttl=60)
        def expensive_func(x):
            call_count[0] += 1
            return x * x
        
        # 第一次调用
        result1 = expensive_func(5)
        self.assertEqual(result1, 25)
        self.assertEqual(call_count[0], 1)
        
        # 第二次调用（缓存）
        result2 = expensive_func(5)
        self.assertEqual(result2, 25)
        self.assertEqual(call_count[0], 1)
        
        # 不同参数
        result3 = expensive_func(6)
        self.assertEqual(result3, 36)
        self.assertEqual(call_count[0], 2)
    
    def test_cache_expiration(self):
        """测试缓存过期"""
        @cached(ttl=0.3)
        def func(x):
            return x
        
        func(1)
        time.sleep(0.4)
        func.cache.cleanup_expired()
        
        # 应该重新计算
        stats = func.cache_stats()
        self.assertEqual(stats.misses, 1)
    
    def test_cache_clear(self):
        """测试缓存清除"""
        call_count = [0]
        
        @cached()
        def func(x):
            call_count[0] += 1
            return x
        
        func(1)
        func(1)  # 缓存命中
        self.assertEqual(call_count[0], 1)
        
        func.cache_clear()
        func(1)  # 重新计算
        self.assertEqual(call_count[0], 2)


class TestTimedCache(unittest.TestCase):
    """测试 TimedCache"""
    
    def test_window_caching(self):
        """测试时间窗口缓存"""
        cache = TimedCache(window_seconds=0.5)
        call_count = [0]
        
        def refresh():
            call_count[0] += 1
            return 'data'
        
        # 第一次调用
        result1 = cache.get_or_refresh('key', refresh)
        self.assertEqual(result1, 'data')
        self.assertEqual(call_count[0], 1)
        
        # 窗口内，不刷新
        result2 = cache.get_or_refresh('key', refresh)
        self.assertEqual(result2, 'data')
        self.assertEqual(call_count[0], 1)
        
        # 窗口后，刷新
        time.sleep(0.6)
        result3 = cache.get_or_refresh('key', refresh)
        self.assertEqual(result3, 'data')
        self.assertEqual(call_count[0], 2)
    
    def test_invalidate(self):
        """测试失效"""
        cache = TimedCache(window_seconds=60)
        call_count = [0]
        
        def refresh():
            call_count[0] += 1
            return 'data'
        
        cache.get_or_refresh('key', refresh)
        self.assertEqual(call_count[0], 1)
        
        cache.invalidate('key')
        cache.get_or_refresh('key', refresh)
        self.assertEqual(call_count[0], 2)


class TestMultiLevelCache(unittest.TestCase):
    """测试 MultiLevelCache"""
    
    def test_l1_caching(self):
        """测试 L1 缓存"""
        cache = MultiLevelCache(l1_size=100, l1_ttl=60)
        cache.set('key', 'value')
        self.assertEqual(cache.get('key'), 'value')
    
    def test_l2_fallback(self):
        """测试 L2 回退"""
        l2_data = {'remote_key': 'remote_value'}
        
        cache = MultiLevelCache()
        cache.set_l2_handlers(
            get_handler=lambda k: l2_data.get(k),
            set_handler=lambda k, v, t: l2_data.update({k: v})
        )
        
        # L1 未命中，从 L2 获取
        result = cache.get('remote_key')
        self.assertEqual(result, 'remote_value')
        
        # 应该回填到 L1
        self.assertEqual(cache._l1.get('remote_key'), 'remote_value')
    
    def test_l1_l2_sync(self):
        """测试 L1 L2 同步"""
        l2_data = {}
        
        cache = MultiLevelCache()
        cache.set_l2_handlers(
            get_handler=lambda k: l2_data.get(k),
            set_handler=lambda k, v, t: l2_data.update({k: v})
        )
        
        cache.set('key', 'value')
        
        # 两个级别都应该有
        self.assertEqual(cache._l1.get('key'), 'value')
        self.assertEqual(l2_data['key'], 'value')


class TestCacheManager(unittest.TestCase):
    """测试 CacheManager"""
    
    def test_singleton(self):
        """测试单例模式"""
        manager1 = CacheManager()
        manager2 = CacheManager()
        self.assertIs(manager1, manager2)
    
    def test_named_cache(self):
        """测试命名缓存"""
        manager = CacheManager()
        
        cache1 = manager.get_cache('cache1', max_size=100)
        cache2 = manager.get_cache('cache2', max_size=200)
        
        cache1.set('key', 'value1')
        cache2.set('key', 'value2')
        
        self.assertEqual(cache1.get('key'), 'value1')
        self.assertEqual(cache2.get('key'), 'value2')
    
    def test_get_all_stats(self):
        """测试获取所有统计"""
        manager = CacheManager()
        manager.clear_all()
        
        cache = manager.get_cache('stats_test')
        cache.set('a', 1)
        cache.get('a')
        cache.get('nonexistent')
        
        stats = manager.get_all_stats()
        self.assertIn('stats_test', stats)
        self.assertEqual(stats['stats_test']['hits'], 1)
        self.assertEqual(stats['stats_test']['misses'], 1)
    
    def test_remove_cache(self):
        """测试删除缓存"""
        manager = CacheManager()
        manager.get_cache('to_remove')
        
        self.assertTrue(manager.remove_cache('to_remove'))
        self.assertFalse(manager.remove_cache('to_remove'))


class TestCreateCache(unittest.TestCase):
    """测试便捷函数"""
    
    def test_create_cache(self):
        """测试创建缓存"""
        cache = create_cache(max_size=50, ttl=100)
        self.assertEqual(cache._max_size, 50)
        self.assertEqual(cache._default_ttl, 100)


if __name__ == '__main__':
    unittest.main(verbosity=2)