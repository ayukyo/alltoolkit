"""
LRU Cache Utils 测试文件

测试覆盖：
- 基础操作（get/set/delete）
- LRU 淘汰策略
- TTL 过期机制
- 线程安全性
- 统计信息
- 装饰器功能
- 特殊缓存类型（TTLCache, BoundedLRUCache, WeightedLRUCache, ExpiringPriorityCache）
"""

import sys
import os
import time
import threading
import unittest

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    LRUCache, TTLCache, BoundedLRUCache, WeightedLRUCache, 
    ExpiringPriorityCache, lru_cache, CacheEntry
)


class TestCacheEntry(unittest.TestCase):
    """CacheEntry 测试"""
    
    def test_basic_creation(self):
        """测试基本创建"""
        entry = CacheEntry('key', 'value')
        self.assertEqual(entry.key, 'key')
        self.assertEqual(entry.value, 'value')
        self.assertIsNone(entry.expires_at)
        self.assertEqual(entry.access_count, 0)
    
    def test_with_ttl(self):
        """测试 TTL 设置"""
        entry = CacheEntry('key', 'value', ttl=10)
        self.assertIsNotNone(entry.expires_at)
        self.assertAlmostEqual(entry.remaining_ttl, 10, delta=0.1)
    
    def test_is_expired_no_ttl(self):
        """测试无 TTL 时不过期"""
        entry = CacheEntry('key', 'value')
        self.assertFalse(entry.is_expired())
    
    def test_is_expired_with_ttl(self):
        """测试 TTL 过期"""
        entry = CacheEntry('key', 'value', ttl=0.1)
        self.assertFalse(entry.is_expired())
        time.sleep(0.15)
        self.assertTrue(entry.is_expired())
    
    def test_touch(self):
        """测试访问更新"""
        entry = CacheEntry('key', 'value')
        initial_access = entry.last_access
        initial_count = entry.access_count
        
        time.sleep(0.01)
        entry.touch()
        
        self.assertGreater(entry.last_access, initial_access)
        self.assertEqual(entry.access_count, initial_count + 1)
    
    def test_age(self):
        """测试存活时间"""
        entry = CacheEntry('key', 'value')
        time.sleep(0.1)
        self.assertGreaterEqual(entry.age, 0.1)


class TestLRUCache(unittest.TestCase):
    """LRUCache 基础测试"""
    
    def test_basic_set_get(self):
        """测试基本设置和获取"""
        cache = LRUCache(max_size=3)
        cache.set('a', 1)
        self.assertEqual(cache.get('a'), 1)
    
    def test_get_missing_key(self):
        """测试获取不存在的键"""
        cache = LRUCache()
        self.assertIsNone(cache.get('missing'))
        self.assertEqual(cache.get('missing', 'default'), 'default')
    
    def test_delete(self):
        """测试删除"""
        cache = LRUCache()
        cache.set('a', 1)
        self.assertTrue(cache.delete('a'))
        self.assertIsNone(cache.get('a'))
        self.assertFalse(cache.delete('a'))
    
    def test_exists(self):
        """测试存在性检查"""
        cache = LRUCache()
        cache.set('a', 1)
        self.assertTrue(cache.exists('a'))
        self.assertFalse(cache.exists('b'))
    
    def test_clear(self):
        """测试清空"""
        cache = LRUCache()
        cache.set('a', 1)
        cache.set('b', 2)
        cache.clear()
        self.assertEqual(cache.size(), 0)
    
    def test_size(self):
        """测试大小"""
        cache = LRUCache(max_size=10)
        self.assertEqual(cache.size(), 0)
        cache.set('a', 1)
        self.assertEqual(cache.size(), 1)
    
    def test_keys_values_items(self):
        """测试键、值、键值对获取"""
        cache = LRUCache()
        cache.set('a', 1)
        cache.set('b', 2)
        
        self.assertEqual(set(cache.keys()), {'a', 'b'})
        self.assertEqual(set(cache.values()), {1, 2})
        self.assertEqual(dict(cache.items()), {'a': 1, 'b': 2})
    
    def test_dict_interface(self):
        """测试字典接口"""
        cache = LRUCache()
        cache['a'] = 1
        self.assertEqual(cache['a'], 1)
        self.assertIn('a', cache)
        del cache['a']
        self.assertNotIn('a', cache)
    
    def test_iteration(self):
        """测试迭代"""
        cache = LRUCache()
        cache.set('a', 1)
        cache.set('b', 2)
        keys = list(cache)
        self.assertEqual(set(keys), {'a', 'b'})
    
    def test_len(self):
        """测试 len"""
        cache = LRUCache()
        cache.set('a', 1)
        cache.set('b', 2)
        self.assertEqual(len(cache), 2)


class TestLRUEviction(unittest.TestCase):
    """LRU 淘汰策略测试"""
    
    def test_eviction_order(self):
        """测试淘汰顺序"""
        cache = LRUCache(max_size=3)
        cache.set('a', 1)
        cache.set('b', 2)
        cache.set('c', 3)
        cache.set('d', 4)  # 应淘汰 'a'
        
        self.assertIsNone(cache.get('a'))
        self.assertEqual(cache.get('b'), 2)
        self.assertEqual(cache.get('c'), 3)
        self.assertEqual(cache.get('d'), 4)
    
    def test_access_updates_order(self):
        """测试访问更新顺序"""
        cache = LRUCache(max_size=3)
        cache.set('a', 1)
        cache.set('b', 2)
        cache.set('c', 3)
        
        # 访问 'a'，使其成为最近使用
        cache.get('a')
        
        # 添加新条目，应淘汰 'b' 而非 'a'
        cache.set('d', 4)
        
        self.assertEqual(cache.get('a'), 1)
        self.assertIsNone(cache.get('b'))
    
    def test_update_moves_to_end(self):
        """测试更新移到末尾"""
        cache = LRUCache(max_size=3)
        cache.set('a', 1)
        cache.set('b', 2)
        cache.set('c', 3)
        
        # 更新 'a'
        cache.set('a', 10)
        
        # 添加新条目，应淘汰 'b'
        cache.set('d', 4)
        
        self.assertEqual(cache.get('a'), 10)
        self.assertIsNone(cache.get('b'))
    
    def test_max_size_one(self):
        """测试容量为 1 的情况"""
        cache = LRUCache(max_size=1)
        cache.set('a', 1)
        self.assertEqual(cache.size(), 1)
        cache.set('b', 2)
        self.assertEqual(cache.size(), 1)
        self.assertIsNone(cache.get('a'))
        self.assertEqual(cache.get('b'), 2)
    
    def test_invalid_max_size(self):
        """测试无效容量"""
        with self.assertRaises(ValueError):
            LRUCache(max_size=0)
        
        with self.assertRaises(ValueError):
            LRUCache(max_size=-1)


class TestTTL(unittest.TestCase):
    """TTL 过期测试"""
    
    def test_entry_expiration(self):
        """测试条目过期"""
        cache = LRUCache(default_ttl=0.1)
        cache.set('a', 1)
        
        self.assertEqual(cache.get('a'), 1)
        time.sleep(0.15)
        self.assertIsNone(cache.get('a'))
    
    def test_custom_ttl(self):
        """测试自定义 TTL"""
        cache = LRUCache()
        cache.set('a', 1, ttl=0.1)
        cache.set('b', 2, ttl=10)  # 长 TTL
        
        time.sleep(0.15)
        self.assertIsNone(cache.get('a'))
        self.assertEqual(cache.get('b'), 2)
    
    def test_ttl_method(self):
        """测试 ttl() 方法"""
        cache = LRUCache()
        cache.set('a', 1, ttl=10)
        
        ttl = cache.ttl('a')
        self.assertGreater(ttl, 9)
        self.assertLessEqual(ttl, 10)
        
        # 不存在的键
        self.assertEqual(cache.ttl('missing'), -1)
    
    def test_no_ttl(self):
        """测试无 TTL（永不过期）"""
        cache = LRUCache()
        cache.set('a', 1)
        
        ttl = cache.ttl('a')
        self.assertIsNone(ttl)
    
    def test_exists_with_expired(self):
        """测试存在性检查过期条目"""
        cache = LRUCache()
        cache.set('a', 1, ttl=0.1)
        
        self.assertTrue(cache.exists('a'))
        time.sleep(0.15)
        self.assertFalse(cache.exists('a'))
    
    def test_touch_with_ttl(self):
        """测试 touch 更新 TTL"""
        cache = LRUCache()
        cache.set('a', 1, ttl=0.1)
        
        # 在过期前更新 TTL
        time.sleep(0.05)
        cache.touch('a', ttl=0.2)
        
        time.sleep(0.1)  # 原本应该过期
        self.assertEqual(cache.get('a'), 1)


class TestBatchOperations(unittest.TestCase):
    """批量操作测试"""
    
    def test_get_many(self):
        """测试批量获取"""
        cache = LRUCache()
        cache.set('a', 1)
        cache.set('b', 2)
        cache.set('c', 3)
        
        result = cache.get_many(['a', 'b', 'missing'])
        self.assertEqual(result, {'a': 1, 'b': 2})
    
    def test_set_many(self):
        """测试批量设置"""
        cache = LRUCache()
        cache.set_many({'a': 1, 'b': 2, 'c': 3})
        
        self.assertEqual(cache.get('a'), 1)
        self.assertEqual(cache.get('b'), 2)
        self.assertEqual(cache.get('c'), 3)
    
    def test_delete_many(self):
        """测试批量删除"""
        cache = LRUCache()
        cache.set('a', 1)
        cache.set('b', 2)
        cache.set('c', 3)
        
        count = cache.delete_many(['a', 'b', 'missing'])
        self.assertEqual(count, 2)
        self.assertEqual(cache.size(), 1)


class TestGetOrSet(unittest.TestCase):
    """get_or_set 测试"""
    
    def test_existing_key(self):
        """测试已存在的键"""
        cache = LRUCache()
        cache.set('a', 1)
        
        result = cache.get_or_set('a', lambda: 999)
        self.assertEqual(result, 1)
    
    def test_missing_key(self):
        """测试不存在的键"""
        cache = LRUCache()
        
        result = cache.get_or_set('a', lambda: 42)
        self.assertEqual(result, 42)
        self.assertEqual(cache.get('a'), 42)
    
    def test_with_ttl(self):
        """测试带 TTL"""
        cache = LRUCache()
        
        cache.get_or_set('a', lambda: 1, ttl=0.1)
        self.assertEqual(cache.get('a'), 1)
        
        time.sleep(0.15)
        self.assertIsNone(cache.get('a'))


class TestPeek(unittest.TestCase):
    """peek 测试"""
    
    def test_peek_no_update(self):
        """测试 peek 不更新访问信息"""
        cache = LRUCache(max_size=3)
        cache.set('a', 1)
        cache.set('b', 2)
        cache.set('c', 3)
        
        # peek 不应该改变访问顺序
        cache.peek('a')
        cache.set('d', 4)
        
        # 'a' 应该被淘汰（peek 不更新顺序）
        self.assertIsNone(cache.get('a'))
    
    def test_peek_missing(self):
        """测试 peek 不存在的键"""
        cache = LRUCache()
        self.assertIsNone(cache.peek('missing'))


class TestStatistics(unittest.TestCase):
    """统计信息测试"""
    
    def test_hits_misses(self):
        """测试命中和未命中统计"""
        cache = LRUCache()
        cache.set('a', 1)
        
        cache.get('a')   # hit
        cache.get('a')   # hit
        cache.get('b')   # miss
        
        stats = cache.stats()
        self.assertEqual(stats['hits'], 2)
        self.assertEqual(stats['misses'], 1)
        self.assertAlmostEqual(stats['hit_rate'], 2/3)
    
    def test_evictions(self):
        """测试淘汰统计"""
        cache = LRUCache(max_size=2)
        cache.set('a', 1)
        cache.set('b', 2)
        cache.set('c', 3)  # 淘汰 'a'
        
        stats = cache.stats()
        self.assertEqual(stats['evictions'], 1)
    
    def test_expirations(self):
        """测试过期统计"""
        cache = LRUCache()
        cache.set('a', 1, ttl=0.1)
        
        time.sleep(0.15)
        cache.get('a')  # 触发过期
        
        stats = cache.stats()
        self.assertEqual(stats['expirations'], 1)
    
    def test_reset_stats(self):
        """测试重置统计"""
        cache = LRUCache()
        cache.set('a', 1)
        cache.get('a')
        
        cache.reset_stats()
        stats = cache.stats()
        
        self.assertEqual(stats['hits'], 0)
        self.assertEqual(stats['misses'], 0)


class TestCleanup(unittest.TestCase):
    """清理机制测试"""
    
    def test_manual_cleanup(self):
        """测试手动清理"""
        cache = LRUCache(auto_cleanup=False)
        cache.set('a', 1, ttl=0.1)
        cache.set('b', 2, ttl=0.1)
        cache.set('c', 3)  # 不过期
        
        time.sleep(0.15)
        count = cache.cleanup()
        
        self.assertEqual(count, 2)
        self.assertEqual(cache.size(), 1)
    
    def test_auto_cleanup(self):
        """测试自动清理"""
        cache = LRUCache(cleanup_interval=2)
        cache.set('a', 1, ttl=0.1)
        
        time.sleep(0.15)
        
        # 第一次操作不触发清理
        cache.get('b')
        # 第二次操作触发清理
        cache.get('b')
        
        # 过期条目应该被清理
        stats = cache.stats()
        self.assertEqual(stats['expirations'], 1)


class TestThreadSafety(unittest.TestCase):
    """线程安全测试"""
    
    def test_concurrent_reads(self):
        """测试并发读"""
        cache = LRUCache(max_size=100)
        for i in range(50):
            cache.set(f'key_{i}', i)
        
        errors = []
        
        def read_values():
            for i in range(50):
                try:
                    cache.get(f'key_{i}')
                except Exception as e:
                    errors.append(e)
        
        threads = [threading.Thread(target=read_values) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        self.assertEqual(len(errors), 0)
    
    def test_concurrent_writes(self):
        """测试并发写"""
        cache = LRUCache(max_size=1000)
        errors = []
        
        def write_values(start):
            for i in range(start, start + 100):
                try:
                    cache.set(f'key_{i}', i)
                except Exception as e:
                    errors.append(e)
        
        threads = [threading.Thread(target=write_values, args=(i*100,)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        self.assertEqual(len(errors), 0)
        self.assertLessEqual(cache.size(), 1000)
    
    def test_concurrent_read_write(self):
        """测试并发读写"""
        cache = LRUCache(max_size=100)
        for i in range(50):
            cache.set(f'key_{i}', i)
        
        errors = []
        
        def read_values():
            for i in range(50):
                try:
                    cache.get(f'key_{i}')
                except Exception as e:
                    errors.append(e)
        
        def write_values():
            for i in range(50, 100):
                try:
                    cache.set(f'key_{i}', i)
                except Exception as e:
                    errors.append(e)
        
        threads = (
            [threading.Thread(target=read_values) for _ in range(5)] +
            [threading.Thread(target=write_values) for _ in range(5)]
        )
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        self.assertEqual(len(errors), 0)


class TestLRUCacheDecorator(unittest.TestCase):
    """lru_cache 装饰器测试"""
    
    def test_basic_caching(self):
        """测试基本缓存功能"""
        call_count = 0
        
        @lru_cache(max_size=10)
        def expensive_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        
        self.assertEqual(expensive_function(5), 10)
        self.assertEqual(call_count, 1)
        
        # 相同参数应返回缓存
        self.assertEqual(expensive_function(5), 10)
        self.assertEqual(call_count, 1)
        
        # 不同参数应重新计算
        self.assertEqual(expensive_function(6), 12)
        self.assertEqual(call_count, 2)
    
    def test_with_ttl(self):
        """测试装饰器 TTL"""
        call_count = 0
        
        @lru_cache(max_size=10, ttl=0.1)
        def timed_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        
        self.assertEqual(timed_function(5), 10)
        self.assertEqual(call_count, 1)
        
        time.sleep(0.15)
        self.assertEqual(timed_function(5), 10)
        self.assertEqual(call_count, 2)  # 过期后重新计算
    
    def test_cache_operations(self):
        """测试装饰器缓存操作"""
        @lru_cache(max_size=10)
        def func(x):
            return x
        
        func(1)
        func(2)
        
        self.assertEqual(func.cache.size(), 2)
        func.cache_clear()
        self.assertEqual(func.cache.size(), 0)
    
    def test_with_kwargs(self):
        """测试带关键字参数"""
        call_count = 0
        
        @lru_cache(max_size=10)
        def func(a, b=0):
            nonlocal call_count
            call_count += 1
            return a + b
        
        self.assertEqual(func(1, b=2), 3)
        self.assertEqual(call_count, 1)
        
        # 相同参数组合
        self.assertEqual(func(1, b=2), 3)
        self.assertEqual(call_count, 1)
        
        # 不同参数组合
        self.assertEqual(func(1, b=3), 4)
        self.assertEqual(call_count, 2)


class TestTTLCache(unittest.TestCase):
    """TTLCache 测试"""
    
    def test_required_ttl(self):
        """测试必须设置 TTL"""
        TTLCache(max_size=10, default_ttl=100)
        
        with self.assertRaises(ValueError):
            TTLCache(max_size=10, default_ttl=None)
        
        with self.assertRaises(ValueError):
            TTLCache(max_size=10, default_ttl=0)
        
        with self.assertRaises(ValueError):
            TTLCache(max_size=10, default_ttl=-1)
    
    def test_refresh_ttl(self):
        """测试刷新 TTL"""
        cache = TTLCache(max_size=10, default_ttl=0.2)
        cache.set('a', 1)
        
        time.sleep(0.15)
        self.assertTrue(cache.refresh_ttl('a'))
        
        time.sleep(0.15)  # 原本应该过期
        self.assertEqual(cache.get('a'), 1)
    
    def test_refresh_all(self):
        """测试刷新所有 TTL"""
        cache = TTLCache(max_size=10, default_ttl=0.2)
        cache.set('a', 1)
        cache.set('b', 2)
        
        time.sleep(0.1)
        count = cache.refresh_all()
        
        self.assertEqual(count, 2)
        
        time.sleep(0.15)  # 原本应该过期
        self.assertEqual(cache.get('a'), 1)
        self.assertEqual(cache.get('b'), 2)


class TestBoundedLRUCache(unittest.TestCase):
    """BoundedLRUCache 测试"""
    
    def test_min_size(self):
        """测试最小保留数量"""
        cache = BoundedLRUCache(max_size=5, min_size=2)
        
        # 填满缓存
        for i in range(10):
            cache.set(i, i)
        
        # 应至少保留 min_size 个条目
        self.assertGreaterEqual(cache.size(), 2)
    
    def test_invalid_min_size(self):
        """测试无效最小保留数量"""
        with self.assertRaises(ValueError):
            BoundedLRUCache(max_size=5, min_size=-1)
        
        with self.assertRaises(ValueError):
            BoundedLRUCache(max_size=5, min_size=5)
        
        with self.assertRaises(ValueError):
            BoundedLRUCache(max_size=5, min_size=6)


class TestWeightedLRUCache(unittest.TestCase):
    """WeightedLRUCache 测试"""
    
    def test_weight_eviction(self):
        """测试加权淘汰"""
        cache = WeightedLRUCache(max_weight=10)
        
        cache.set('a', 1, weight=3)
        cache.set('b', 2, weight=3)
        cache.set('c', 3, weight=3)
        
        # 总权重 9，添加权重 5 应淘汰 'a' (权重3)
        # 最终权重: 3 + 3 + 5 = 8 (可能还要淘汰 'b')
        cache.set('d', 4, weight=5)
        
        self.assertIsNone(cache.get('a'))
        # 当前权重应不超过 max_weight
        self.assertLessEqual(cache.current_weight(), cache._max_weight)
    
    def test_default_weight(self):
        """测试默认权重"""
        cache = WeightedLRUCache(max_weight=10, default_weight=2)
        
        cache.set('a', 1)
        self.assertEqual(cache.current_weight(), 2)
    
    def test_weight_update(self):
        """测试权重更新"""
        cache = WeightedLRUCache(max_weight=10)
        
        cache.set('a', 1, weight=3)
        self.assertEqual(cache.current_weight(), 3)
        
        # 更新同一键，新权重
        cache.set('a', 2, weight=5)
        self.assertEqual(cache.current_weight(), 5)
    
    def test_available_weight(self):
        """测试可用权重"""
        cache = WeightedLRUCache(max_weight=10)
        
        cache.set('a', 1, weight=3)
        self.assertEqual(cache.available_weight(), 7)
    
    def test_delete_updates_weight(self):
        """测试删除更新权重"""
        cache = WeightedLRUCache(max_weight=10)
        
        cache.set('a', 1, weight=3)
        cache.delete('a')
        
        self.assertEqual(cache.current_weight(), 0)


class TestExpiringPriorityCache(unittest.TestCase):
    """ExpiringPriorityCache 测试"""
    
    def test_priority_eviction(self):
        """测试优先淘汰即将过期的"""
        cache = ExpiringPriorityCache(max_size=3)
        
        cache.set('a', 1, ttl=10)  # 长过期
        cache.set('b', 2, ttl=0.1)  # 短过期
        cache.set('c', 3, ttl=10)
        
        time.sleep(0.15)  # 'b' 即将过期
        
        # 添加新条目应优先淘汰 'b'
        cache.set('d', 4)
        
        # 'b' 应该被淘汰
        self.assertIsNone(cache.get('b'))
    
    def test_stats(self):
        """测试统计信息"""
        cache = ExpiringPriorityCache()
        
        cache.set('a', 1)
        cache.get('a')
        cache.get('missing')
        
        stats = cache.stats()
        self.assertEqual(stats['hits'], 1)
        self.assertEqual(stats['misses'], 1)
    
    def test_no_ttl_entries(self):
        """测试无 TTL 条目"""
        cache = ExpiringPriorityCache(max_size=3)
        
        # 无 TTL 条目
        cache.set('a', 1)
        cache.set('b', 2)
        cache.set('c', 3)
        
        # 当容量满时，淘汰某个条目
        cache.set('d', 4)
        
        self.assertEqual(cache.size(), 3)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_empty_cache(self):
        """测试空缓存"""
        cache = LRUCache()
        
        self.assertIsNone(cache.get('a'))
        self.assertFalse(cache.exists('a'))
        self.assertEqual(cache.size(), 0)
        self.assertEqual(len(cache), 0)
    
    def test_none_values(self):
        """测试 None 值"""
        cache = LRUCache()
        
        cache.set('a', None)
        # get 返回 None 可能是值或不存在，需要用 exists 区分
        self.assertIsNone(cache.get('a'))
        self.assertTrue(cache.exists('a'))
    
    def test_complex_keys(self):
        """测试复杂键"""
        cache = LRUCache()
        
        # 元组键
        cache.set((1, 2), 'tuple')
        self.assertEqual(cache.get((1, 2)), 'tuple')
        
        # 字符串键
        cache.set('中文', 'chinese')
        self.assertEqual(cache.get('中文'), 'chinese')
    
    def test_overwrite(self):
        """测试覆盖"""
        cache = LRUCache()
        
        cache.set('a', 1)
        cache.set('a', 2)
        cache.set('a', 3)
        
        self.assertEqual(cache.get('a'), 3)
        self.assertEqual(cache.size(), 1)
    
    def test_large_cache(self):
        """测试大容量缓存"""
        cache = LRUCache(max_size=10000)
        
        for i in range(10000):
            cache.set(i, i)
        
        self.assertEqual(cache.size(), 10000)
        self.assertEqual(cache.get(5000), 5000)


if __name__ == '__main__':
    unittest.main(verbosity=2)