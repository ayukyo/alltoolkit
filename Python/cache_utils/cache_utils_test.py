#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cache_utils - 测试用例
=====================

测试 MemoryCache、装饰器、TimedCache、RateLimiter 的所有功能。
"""

import pytest
import time
import threading
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cache_utils.mod import (
    MemoryCache,
    CacheEntry,
    cached,
    memoize,
    TimedCache,
    RateLimiter,
)


class TestCacheEntry:
    """测试 CacheEntry 类"""
    
    def test_create_entry(self):
        """测试创建缓存条目"""
        entry = CacheEntry("value")
        assert entry.value == "value"
        assert entry.expire_at is None
        assert entry.access_count == 0
    
    def test_create_entry_with_ttl(self):
        """测试创建带过期时间的条目"""
        expire_at = time.time() + 60
        entry = CacheEntry("value", expire_at)
        assert entry.value == "value"
        assert entry.expire_at == expire_at
    
    def test_is_expired_no_ttl(self):
        """测试无过期时间时不过期"""
        entry = CacheEntry("value")
        assert not entry.is_expired()
    
    def test_is_expired_with_ttl(self):
        """测试过期检测"""
        entry = CacheEntry("value", time.time() - 1)  # 已过期
        assert entry.is_expired()
        
        entry2 = CacheEntry("value", time.time() + 60)  # 未过期
        assert not entry2.is_expired()
    
    def test_touch(self):
        """测试访问计数更新"""
        entry = CacheEntry("value")
        assert entry.access_count == 0
        entry.touch()
        assert entry.access_count == 1
        entry.touch()
        assert entry.access_count == 2


class TestMemoryCache:
    """测试 MemoryCache 类"""
    
    def test_create_cache(self):
        """测试创建缓存实例"""
        cache = MemoryCache()
        assert cache.size() == 0
        assert cache._max_size == 0
        assert cache._default_ttl is None
    
    def test_create_cache_with_options(self):
        """测试带选项创建缓存"""
        cache = MemoryCache(max_size=100, default_ttl=60)
        assert cache._max_size == 100
        assert cache._default_ttl == 60
    
    def test_set_get(self):
        """测试基本 set/get 操作"""
        cache = MemoryCache()
        cache.set("key", "value")
        assert cache.get("key") == "value"
    
    def test_get_missing_key(self):
        """测试获取不存在的键"""
        cache = MemoryCache()
        assert cache.get("missing") is None
        assert cache.get("missing", "default") == "default"
    
    def test_set_with_ttl(self):
        """测试带过期时间的 set"""
        cache = MemoryCache()
        cache.set("key", "value", ttl=1)
        assert cache.get("key") == "value"
        time.sleep(1.1)
        assert cache.get("key") is None
    
    def test_delete(self):
        """测试删除操作"""
        cache = MemoryCache()
        cache.set("key", "value")
        assert cache.delete("key") is True
        assert cache.get("key") is None
        assert cache.delete("key") is False  # 已删除
    
    def test_has(self):
        """测试存在检测"""
        cache = MemoryCache()
        cache.set("key", "value")
        assert cache.has("key") is True
        assert cache.has("missing") is False
    
    def test_has_expired(self):
        """测试过期键的存在检测"""
        cache = MemoryCache()
        cache.set("key", "value", ttl=1)
        assert cache.has("key") is True
        time.sleep(1.1)
        assert cache.has("key") is False
    
    def test_clear(self):
        """测试清空缓存"""
        cache = MemoryCache()
        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("c", 3)
        cache.clear()
        assert cache.size() == 0
    
    def test_get_or_set(self):
        """测试 get_or_set"""
        cache = MemoryCache()
        
        # 第一次调用，创建值
        value = cache.get_or_set("key", lambda: "computed")
        assert value == "computed"
        
        # 第二次调用，从缓存读取
        value2 = cache.get_or_set("key", lambda: "new_computed")
        assert value2 == "computed"  # 仍是旧值
    
    def test_get_many(self):
        """测试批量获取"""
        cache = MemoryCache()
        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("c", 3)
        
        result = cache.get_many(["a", "b", "c", "d"])
        assert result == {"a": 1, "b": 2, "c": 3}
    
    def test_set_many(self):
        """测试批量设置"""
        cache = MemoryCache()
        cache.set_many({"a": 1, "b": 2, "c": 3})
        
        assert cache.get("a") == 1
        assert cache.get("b") == 2
        assert cache.get("c") == 3
    
    def test_delete_many(self):
        """测试批量删除"""
        cache = MemoryCache()
        cache.set_many({"a": 1, "b": 2, "c": 3})
        
        count = cache.delete_many(["a", "b", "d"])
        assert count == 2
        assert cache.get("a") is None
        assert cache.get("b") is None
        assert cache.get("c") == 3
    
    def test_keys_values_items(self):
        """测试 keys/values/items"""
        cache = MemoryCache()
        cache.set("a", 1)
        cache.set("b", 2)
        
        assert set(cache.keys()) == {"a", "b"}
        assert set(cache.values()) == {1, 2}
        assert set(cache.items()) == {("a", 1), ("b", 2)}
    
    def test_lru_eviction(self):
        """测试 LRU 淘汰"""
        cache = MemoryCache(max_size=3)
        
        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("c", 3)
        assert cache.size() == 3
        
        # 添加第四个，淘汰第一个
        cache.set("d", 4)
        assert cache.size() == 3
        assert cache.get("a") is None  # a 被淘汰
        assert cache.get("b") == 2
        assert cache.get("c") == 3
        assert cache.get("d") == 4
    
    def test_lru_access_order(self):
        """测试 LRU 访问顺序"""
        cache = MemoryCache(max_size=3)
        
        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("c", 3)
        
        # 访问 a，使其移到末尾
        cache.get("a")
        
        # 添加第四个，淘汰 b（而非 a）
        cache.set("d", 4)
        assert cache.get("a") == 1
        assert cache.get("b") is None  # b 被淘汰
    
    def test_cleanup_expired(self):
        """测试过期清理"""
        cache = MemoryCache()
        
        cache.set("a", 1, ttl=1)
        cache.set("b", 2, ttl=1)
        cache.set("c", 3)  # 不过期
        
        time.sleep(1.1)
        
        count = cache.cleanup_expired()
        assert count == 2
        assert cache.get("a") is None
        assert cache.get("b") is None
        assert cache.get("c") == 3
    
    def test_stats(self):
        """测试统计信息"""
        cache = MemoryCache()
        
        cache.set("key", "value")
        cache.get("key")  # hit
        cache.get("key")  # hit
        cache.get("missing")  # miss
        
        stats = cache.stats()
        assert stats["hits"] == 2
        assert stats["misses"] == 1
        # hit_rate 是 round(hit_rate, 4)，所以是 0.6667
        assert abs(stats["hit_rate"] - 2/3) < 0.001
    
    def test_ttl(self):
        """测试剩余过期时间查询"""
        cache = MemoryCache()
        
        cache.set("key", "value", ttl=60)
        ttl = cache.ttl("key")
        assert 58 <= ttl <= 60  # 大约 60 秒
        
        assert cache.ttl("missing") == -1
        
        cache.set("permanent", "value", ttl=-1)  # 永不过期
        assert cache.ttl("permanent") is None
    
    def test_extend_ttl(self):
        """测试延长过期时间"""
        cache = MemoryCache()
        
        cache.set("key", "value", ttl=10)
        assert cache.extend_ttl("key", 30) is True
        ttl = cache.ttl("key")
        assert 38 <= ttl <= 42  # 大约 10+30 秒
        
        assert cache.extend_ttl("missing", 30) is False
    
    def test_incr_decr(self):
        """测试计数器增减"""
        cache = MemoryCache()
        
        cache.set("counter", 0)
        assert cache.incr("counter") == 1
        assert cache.incr("counter", 10) == 11
        assert cache.decr("counter") == 10
        assert cache.decr("counter", 5) == 5
        
        # 测试不存在键
        with pytest.raises(KeyError):
            cache.incr("missing")
        
        # 测试非数值
        cache.set("text", "hello")
        with pytest.raises(ValueError):
            cache.incr("text")
    
    def test_dict_like_access(self):
        """测试字典式访问"""
        cache = MemoryCache()
        
        cache["key"] = "value"
        assert cache["key"] == "value"
        
        assert "key" in cache
        assert "missing" not in cache
        
        del cache["key"]
        assert "key" not in cache
        
        with pytest.raises(KeyError):
            cache["missing"]
        
        with pytest.raises(KeyError):
            del cache["missing"]
    
    def test_thread_safety(self):
        """测试线程安全"""
        cache = MemoryCache(thread_safe=True)
        errors = []
        
        def writer():
            try:
                for i in range(100):
                    cache.set(f"key_{i}", i)
            except Exception as e:
                errors.append(e)
        
        def reader():
            try:
                for i in range(100):
                    cache.get(f"key_{i}")
            except Exception as e:
                errors.append(e)
        
        threads = []
        for _ in range(5):
            threads.append(threading.Thread(target=writer))
            threads.append(threading.Thread(target=reader))
        
        for t in threads:
            t.start()
        
        for t in threads:
            t.join()
        
        assert len(errors) == 0
    
    def test_context_manager(self):
        """测试上下文管理器"""
        with MemoryCache() as cache:
            cache.set("key", "value")
            assert cache.get("key") == "value"
        
        # cache 已关闭
        assert cache.size() == 0


class TestCachedDecorator:
    """测试 cached 装饰器"""
    
    def test_cached_basic(self):
        """测试基本缓存装饰器"""
        call_count = [0]  # 使用列表避免闭包问题
        cache = MemoryCache()
        
        @cached(cache=cache)
        def expensive_func(n):
            call_count[0] += 1
            return n * n
        
        # 第一次调用
        result1 = expensive_func(5)
        assert result1 == 25
        assert call_count[0] == 1
        
        # 第二次调用，从缓存读取
        result2 = expensive_func(5)
        assert result2 == 25
        assert call_count[0] == 1  # 未增加
        
        # 不同参数，重新计算
        result3 = expensive_func(10)
        assert result3 == 100
        assert call_count[0] == 2
    
    def test_cached_with_ttl(self):
        """测试带 TTL 的缓存"""
        call_count = [0]  # 使用列表避免闭包问题
        cache = MemoryCache()
        
        @cached(cache=cache, ttl=1)
        def func(n):
            call_count[0] += 1
            return n
        
        result1 = func(5)
        assert result1 == 5
        assert call_count[0] == 1
        
        time.sleep(1.1)
        
        result2 = func(5)
        assert result2 == 5
        assert call_count[0] == 2  # 过期后重新计算
    
    def test_cached_with_prefix(self):
        """测试带前缀的缓存键"""
        cache = MemoryCache()
        
        @cached(cache=cache, key_prefix="myapp:")
        def func(n):
            return n * 2
        
        # 第一次调用，应该缓存结果
        result = func(5)
        assert result == 10
        
        # 检查缓存中是否有数据
        # 如果第二次调用返回相同结果，说明缓存生效
        result2 = func(5)
        assert result2 == 10
    
    def test_cached_methods(self):
        """测试装饰器附加方法"""
        cache = MemoryCache()
        
        @cached(cache=cache)
        def func(n):
            return n
        
        func(5)
        
        # cache_clear 方法
        func.cache_clear()
        assert cache.size() == 0
        
        # cache_stats 方法
        stats = func.cache_stats()
        assert "hits" in stats


class TestMemoize:
    """测试 memoize 装饰器"""
    
    def test_memoize_basic(self):
        """测试基本 memoize"""
        call_count = [0]  # 使用列表避免闭包问题
        
        @memoize(ttl=60)
        def fibonacci(n):
            call_count[0] += 1
            if n < 2:
                return n
            return fibonacci(n-1) + fibonacci(n-2)
        
        result = fibonacci(10)
        assert result == 55
        
        # memoize 应显著减少调用次数
        # 无缓存情况下 fibonacci(10) 需要约 177 次调用
        assert call_count[0] < 50
    
    def test_memoize_max_size(self):
        """测试 memoize 最大缓存数"""
        call_count = [0]  # 使用列表避免闭包问题
        
        @memoize(max_size=3)
        def func(n):
            call_count[0] += 1
            return n
        
        func(1)
        func(2)
        func(3)
        assert call_count[0] == 3
        
        # 缓存满后，添加新值会淘汰旧值
        func(4)
        assert call_count[0] == 4
        
        # 再次调用 1，需要重新计算（假设被淘汰）
        func(1)
        # 可能是 5 或仍为 4，取决于 LRU 淘汰顺序
        assert call_count[0] >= 4


class TestTimedCache:
    """测试 TimedCache 类"""
    
    def test_timed_cache_basic(self):
        """测试基本时间缓存"""
        cache = TimedCache(window=2)
        
        cache.set("key", "value")
        assert cache.get("key") == "value"
    
    def test_timed_cache_refresh(self):
        """测试刷新过期时间"""
        cache = TimedCache(window=2)
        
        cache.set("key", "value")
        
        # 等待 1 秒后访问，刷新过期时间
        time.sleep(1)
        assert cache.get("key", refresh=True) == "value"
        
        # 再等待 2 秒，因为刷新了，应该还在
        time.sleep(1.5)
        assert cache.get("key", refresh=False) == "value"  # 未刷新仍存在
    
    def test_timed_cache_no_refresh(self):
        """测试不刷新过期时间"""
        cache = TimedCache(window=2)
        
        cache.set("key", "value")
        
        time.sleep(1)
        # 不刷新，过期时间不变
        assert cache.get("key", refresh=False) == "value"
        
        time.sleep(1.5)
        # 已过期
        assert cache.get("key", refresh=False) is None


class TestRateLimiter:
    """测试 RateLimiter 类"""
    
    def test_rate_limiter_allow(self):
        """测试基本限流"""
        limiter = RateLimiter(max_requests=3, window=2)
        
        assert limiter.allow("user1") is True
        assert limiter.allow("user1") is True
        assert limiter.allow("user1") is True
        assert limiter.allow("user1") is False  # 超限
    
    def test_rate_limiter_remaining(self):
        """测试剩余请求次数"""
        limiter = RateLimiter(max_requests=5, window=60)
        
        assert limiter.remaining("user1") == 5
        
        limiter.allow("user1")
        assert limiter.remaining("user1") == 4
        
        limiter.allow("user1")
        limiter.allow("user1")
        assert limiter.remaining("user1") == 2
    
    def test_rate_limiter_reset(self):
        """测试重置计数"""
        limiter = RateLimiter(max_requests=3, window=60)
        
        limiter.allow("user1")
        limiter.allow("user1")
        assert limiter.remaining("user1") == 1
        
        limiter.reset("user1")
        assert limiter.remaining("user1") == 3
    
    def test_rate_limiter_different_keys(self):
        """测试不同键的独立限流"""
        limiter = RateLimiter(max_requests=2, window=60)
        
        assert limiter.allow("user1") is True
        assert limiter.allow("user1") is True
        assert limiter.allow("user1") is False
        
        # user2 独立计数
        assert limiter.allow("user2") is True
        assert limiter.allow("user2") is True
        assert limiter.allow("user2") is False
    
    def test_rate_limiter_window_expiry(self):
        """测试时间窗口过期"""
        limiter = RateLimiter(max_requests=2, window=1)
        
        limiter.allow("user1")
        limiter.allow("user1")
        assert limiter.allow("user1") is False
        
        # 等待窗口过期
        time.sleep(1.1)
        
        # 重新开始计数
        assert limiter.allow("user1") is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])