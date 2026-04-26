"""
cache_utils 测试文件
====================

测试内存缓存的各种功能。
"""

import time
import threading
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    MemoryCache, CacheEntry, cached, memoize,
    TimedCache, RateLimiter
)


def test_basic_operations():
    """测试基本操作"""
    print("测试基本操作...")
    cache = MemoryCache()
    
    # 测试set和get
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1", "set/get失败"
    
    # 测试默认值
    assert cache.get("missing", "default") == "default", "默认值失败"
    
    # 测试has
    assert cache.has("key1") == True, "has失败"
    assert cache.has("missing") == False, "has失败"
    
    # 测试delete
    assert cache.delete("key1") == True, "delete失败"
    assert cache.has("key1") == False, "delete后has失败"
    assert cache.delete("missing") == False, "删除不存在键应返回False"
    
    # 测试clear
    cache.set("a", 1)
    cache.set("b", 2)
    cache.clear()
    assert cache.size() == 0, "clear失败"
    
    print("✓ 基本操作测试通过")


def test_ttl():
    """测试过期时间"""
    print("测试过期时间...")
    cache = MemoryCache()
    
    # 测试短TTL
    cache.set("short", "value", ttl=0.1)
    assert cache.get("short") == "value", "设置后应能获取"
    
    time.sleep(0.15)
    assert cache.get("short") is None, "过期后应返回None"
    
    # 测试默认TTL
    cache_with_default = MemoryCache(default_ttl=0.1)
    cache_with_default.set("key", "value")
    assert cache_with_default.get("key") == "value"
    time.sleep(0.15)
    assert cache_with_default.get("key") is None
    
    # 测试永不过期（负数TTL）
    cache.set("permanent", "value", ttl=-1)
    time.sleep(0.1)
    assert cache.get("permanent") == "value", "负数TTL应永不过期"
    
    # 测试ttl方法
    cache.set("ttl_test", "value", ttl=10)
    remaining = cache.ttl("ttl_test")
    assert remaining is not None and remaining > 9, f"ttl应返回约10，实际: {remaining}"
    assert cache.ttl("missing") == -1, "不存在键应返回-1"
    
    # 测试extend_ttl
    cache.set("extend_test", "value", ttl=1)
    cache.extend_ttl("extend_test", 10)
    remaining = cache.ttl("extend_test")
    assert remaining > 10, f"extend_ttl后应大于10，实际: {remaining}"
    
    print("✓ 过期时间测试通过")


def test_lru():
    """测试LRU淘汰"""
    print("测试LRU淘汰...")
    cache = MemoryCache(max_size=3)
    
    cache.set("a", 1)
    cache.set("b", 2)
    cache.set("c", 3)
    assert cache.size() == 3
    
    # 添加第4个，应淘汰a
    cache.set("d", 4)
    assert cache.size() == 3
    assert not cache.has("a"), "应淘汰最早使用的a"
    assert cache.has("b") and cache.has("c") and cache.has("d")
    
    # 访问b，使其变为最近使用
    cache.get("b")
    # 添加第5个，应淘汰c（因为b刚被访问）
    cache.set("e", 5)
    assert not cache.has("c"), "应淘汰c而非b"
    assert cache.has("b")
    
    print("✓ LRU淘汰测试通过")


def test_batch_operations():
    """测试批量操作"""
    print("测试批量操作...")
    cache = MemoryCache()
    
    # 测试set_many
    cache.set_many({"a": 1, "b": 2, "c": 3})
    assert cache.get("a") == 1
    assert cache.get("b") == 2
    assert cache.get("c") == 3
    
    # 测试get_many
    result = cache.get_many(["a", "b", "missing"])
    assert result == {"a": 1, "b": 2}, f"get_many失败: {result}"
    
    # 测试delete_many
    count = cache.delete_many(["a", "b", "missing"])
    assert count == 2, f"delete_many应删除2个，实际: {count}"
    assert not cache.has("a") and not cache.has("b")
    
    print("✓ 批量操作测试通过")


def test_incr_decr():
    """测试数值增加减少"""
    print("测试数值增加减少...")
    cache = MemoryCache()
    
    cache.set("counter", 0)
    assert cache.incr("counter") == 1
    assert cache.incr("counter", 5) == 6
    assert cache.decr("counter") == 5
    assert cache.decr("counter", 3) == 2
    
    # 测试非数值错误
    cache.set("text", "hello")
    try:
        cache.incr("text")
        assert False, "应对非数值抛出错误"
    except ValueError:
        pass
    
    # 测试不存在键错误
    try:
        cache.incr("missing")
        assert False, "应对不存在键抛出错误"
    except KeyError:
        pass
    
    print("✓ 数值增减测试通过")


def test_stats():
    """测试统计信息"""
    print("测试统计信息...")
    cache = MemoryCache()
    
    cache.set("key", "value")
    cache.get("key")  # hit
    cache.get("missing")  # miss
    
    stats = cache.stats()
    assert stats["size"] == 1
    assert stats["hits"] == 1
    assert stats["misses"] == 1
    assert abs(stats["hit_rate"] - 0.5) < 0.001
    
    cache.reset_stats()
    stats = cache.stats()
    assert stats["hits"] == 0
    assert stats["misses"] == 0
    
    print("✓ 统计信息测试通过")


def test_decorator():
    """测试装饰器"""
    print("测试装饰器...")
    
    call_count = 0
    
    @memoize(ttl=60)
    def expensive_function(n):
        nonlocal call_count
        call_count += 1
        return n * n
    
    # 第一次调用
    result1 = expensive_function(5)
    assert result1 == 25
    assert call_count == 1
    
    # 第二次调用应从缓存获取
    result2 = expensive_function(5)
    assert result2 == 25
    assert call_count == 1, "应从缓存获取，不重新计算"
    
    # 不同参数应重新计算
    result3 = expensive_function(10)
    assert result3 == 100
    assert call_count == 2
    
    # 测试stats
    assert expensive_function.cache_stats()["hits"] >= 1
    
    print("✓ 装饰器测试通过")


def test_cached_decorator():
    """测试cached装饰器"""
    print("测试cached装饰器...")
    
    cache = MemoryCache(max_size=10)
    call_count = 0
    
    @cached(cache=cache, key_prefix="test:", ttl=60)
    def compute(x, y):
        nonlocal call_count
        call_count += 1
        return x + y
    
    result1 = compute(1, 2)
    assert result1 == 3
    assert call_count == 1
    
    result2 = compute(1, 2)  # 应从缓存获取
    assert result2 == 3
    assert call_count == 1
    
    result3 = compute(2, 3)  # 不同参数
    assert result3 == 5
    assert call_count == 2
    
    # 测试cache_clear
    compute.cache_clear()
    result4 = compute(1, 2)  # 缓存已清空，应重新计算
    assert result4 == 3
    assert call_count == 3
    
    print("✓ cached装饰器测试通过")


def test_thread_safety():
    """测试线程安全"""
    print("测试线程安全...")
    cache = MemoryCache(thread_safe=True)
    
    def worker(cache, key, iterations):
        for i in range(iterations):
            cache.set(f"{key}_{i}", i)
            cache.get(f"{key}_{i}")
    
    threads = []
    for i in range(10):
        t = threading.Thread(target=worker, args=(cache, f"thread_{i}", 100))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    # 如果没有崩溃和死锁，测试通过
    print("✓ 线程安全测试通过")


def test_timed_cache():
    """测试时间窗口缓存"""
    print("测试时间窗口缓存...")
    cache = TimedCache(window=0.2)  # 200ms窗口
    
    cache.set("key", "value")
    assert cache.get("key") == "value"
    
    time.sleep(0.25)
    assert cache.get("key") is None, "应已过期"
    
    print("✓ 时间窗口缓存测试通过")


def test_rate_limiter():
    """测试速率限制器"""
    print("测试速率限制器...")
    limiter = RateLimiter(max_requests=3, window=1)
    
    key = "user:123"
    
    # 前3次应该允许
    assert limiter.allow(key) == True
    assert limiter.allow(key) == True
    assert limiter.allow(key) == True
    
    # 第4次应该拒绝
    assert limiter.allow(key) == False
    
    # 检查剩余次数
    assert limiter.remaining(key) == 0
    
    # 重置后应允许
    limiter.reset(key)
    assert limiter.allow(key) == True
    assert limiter.remaining(key) == 2
    
    print("✓ 速率限制器测试通过")


def test_cleanup():
    """测试过期清理"""
    print("测试过期清理...")
    cache = MemoryCache()
    
    # 添加多个条目
    cache.set("a", 1, ttl=0.1)
    cache.set("b", 2, ttl=0.1)
    cache.set("c", 3, ttl=10)  # 长期
    
    time.sleep(0.15)
    
    # 清理过期
    cleaned = cache.cleanup_expired()
    assert cleaned == 2, f"应清理2个过期条目，实际: {cleaned}"
    assert cache.has("c")
    assert not cache.has("a")
    assert not cache.has("b")
    
    print("✓ 过期清理测试通过")


def test_get_or_set():
    """测试get_or_set"""
    print("测试get_or_set...")
    cache = MemoryCache()
    
    call_count = 0
    
    def factory():
        nonlocal call_count
        call_count += 1
        return "computed"
    
    # 第一次调用，应执行factory
    result1 = cache.get_or_set("key", factory)
    assert result1 == "computed"
    assert call_count == 1
    
    # 第二次调用，应从缓存获取
    result2 = cache.get_or_set("key", factory)
    assert result2 == "computed"
    assert call_count == 1, "应从缓存获取，不执行factory"
    
    print("✓ get_or_set测试通过")


def test_magic_methods():
    """测试魔术方法"""
    print("测试魔术方法...")
    cache = MemoryCache()
    
    # __setitem__ / __getitem__
    cache["key"] = "value"
    assert cache["key"] == "value"
    
    # __contains__
    assert "key" in cache
    assert "missing" not in cache
    
    # __delitem__
    del cache["key"]
    assert "key" not in cache
    
    # __len__
    cache["a"] = 1
    cache["b"] = 2
    assert len(cache) == 2
    
    print("✓ 魔术方法测试通过")


def test_context_manager():
    """测试上下文管理器"""
    print("测试上下文管理器...")
    
    with MemoryCache() as cache:
        cache.set("key", "value")
        assert cache.get("key") == "value"
    
    # 退出上下文后缓存应清空
    assert cache.size() == 0
    
    print("✓ 上下文管理器测试通过")


def test_keys_values_items():
    """测试keys/values/items方法"""
    print("测试keys/values/items方法...")
    cache = MemoryCache()
    
    cache.set("a", 1, ttl=0.1)
    cache.set("b", 2)
    cache.set("c", 3, ttl=0.1)
    
    time.sleep(0.15)
    
    # keys应自动清理过期
    keys = cache.keys()
    assert keys == ["b"], f"keys应为['b']，实际: {keys}"
    
    values = cache.values()
    assert values == [2], f"values应为[2]，实际: {values}"
    
    items = cache.items()
    assert items == [("b", 2)], f"items应为[('b', 2)]，实际: {items}"
    
    print("✓ keys/values/items测试通过")


def test_touch():
    """测试touch方法"""
    print("测试touch方法...")
    cache = MemoryCache()
    
    cache.set("key", "value", ttl=1)
    time.sleep(0.1)
    
    # touch应更新LRU顺序
    assert cache.touch("key") == True
    
    # touch不存在的键
    assert cache.touch("missing") == False
    
    print("✓ touch测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("cache_utils 测试套件")
    print("=" * 50)
    
    tests = [
        test_basic_operations,
        test_ttl,
        test_lru,
        test_batch_operations,
        test_incr_decr,
        test_stats,
        test_decorator,
        test_cached_decorator,
        test_thread_safety,
        test_timed_cache,
        test_rate_limiter,
        test_cleanup,
        test_get_or_set,
        test_magic_methods,
        test_context_manager,
        test_keys_values_items,
        test_touch,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} 失败: {e}")
            failed += 1
    
    print("=" * 50)
    print(f"测试完成: {passed} 通过, {failed} 失败")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)