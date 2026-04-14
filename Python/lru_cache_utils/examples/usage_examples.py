"""
LRU Cache Utils 使用示例

展示各种使用场景和最佳实践。
"""

import time
from mod import (
    LRUCache, TTLCache, BoundedLRUCache, WeightedLRUCache,
    ExpiringPriorityCache, lru_cache
)


def example_basic_usage():
    """基本使用示例"""
    print("=== 基本使用 ===")
    
    # 创建缓存
    cache = LRUCache(max_size=3)
    
    # 设置值
    cache.set('a', 1)
    cache.set('b', 2)
    cache.set('c', 3)
    print(f"设置 a=1, b=2, c=3, 大小: {cache.size()}")
    
    # 获取值
    print(f"获取 a: {cache.get('a')}")
    print(f"获取 missing: {cache.get('missing', 'default')}")
    
    # 字典接口
    cache['d'] = 4
    print(f"通过字典设置 d=4, 大小: {cache.size()}")
    
    # 当超过容量时淘汰最久未使用
    print(f"淘汰后 a 的值: {cache.get('a')} (应为 None)")


def example_lru_eviction():
    """LRU 淘汰策略示例"""
    print("\n=== LRU 淘汰策略 ===")
    
    cache = LRUCache(max_size=3)
    cache.set('a', 1)
    cache.set('b', 2)
    cache.set('c', 3)
    print(f"初始: {dict(cache.items())}")
    
    # 访问 'a' 使其成为最近使用
    cache.get('a')
    print("访问 'a' 后")
    
    # 添加新条目
    cache.set('d', 4)
    print(f"添加 'd' 后: {dict(cache.items())}")
    print("'b' 应被淘汰，因为 'a' 刚被访问过")


def example_ttl():
    """TTL 过期示例"""
    print("\n=== TTL 过期 ===")
    
    cache = LRUCache(default_ttl=2)  # 2 秒 TTL
    
    cache.set('a', 1)
    cache.set('b', 2, ttl=5)  # 自定义 5 秒
    
    print(f"初始: a={cache.get('a')}, b={cache.get('b')}")
    print(f"a 的剩余 TTL: {cache.ttl('a'):.1f}秒")
    print(f"b 的剩余 TTL: {cache.ttl('b'):.1f}秒")
    
    time.sleep(2.5)
    print("\n2.5 秒后...")
    print(f"a={cache.get('a')} (应过期)")
    print(f"b={cache.get('b')} (仍有效)")


def example_decorator():
    """装饰器使用示例"""
    print("\n=== 装饰器缓存 ===")
    
    call_count = 0
    
    @lru_cache(max_size=100, ttl=10)
    def fibonacci(n):
        """带缓存的斐波那契"""
        nonlocal call_count
        call_count += 1
        
        if n <= 1:
            return n
        return fibonacci(n-1) + fibonacci(n-2)
    
    # 第一次计算
    result1 = fibonacci(20)
    print(f"fibonacci(20) = {result1}, 函数调用次数: {call_count}")
    
    # 重置计数
    call_count = 0
    
    # 第二次相同参数，使用缓存
    result2 = fibonacci(20)
    print(f"fibonacci(20) = {result2}, 函数调用次数: {call_count} (应从缓存)")
    
    # 查看缓存统计
    stats = fibonacci.cache_stats()
    print(f"缓存统计: 命中={stats['hits']}, 未命中={stats['misses']}")


def example_batch_operations():
    """批量操作示例"""
    print("\n=== 批量操作 ===")
    
    cache = LRUCache(max_size=100)
    
    # 批量设置
    data = {f'key_{i}': i * 10 for i in range(10)}
    cache.set_many(data)
    print(f"批量设置 10 个条目，大小: {cache.size()}")
    
    # 批量获取
    keys = ['key_0', 'key_5', 'key_9', 'missing']
    result = cache.get_many(keys)
    print(f"批量获取结果: {result}")
    
    # 批量删除
    deleted = cache.delete_many(['key_0', 'key_1', 'missing'])
    print(f"批量删除 {deleted} 个条目，剩余: {cache.size()}")


def example_get_or_set():
    """get_or_set 模式示例"""
    print("\n=== get_or_set 模式 ===")
    
    cache = LRUCache()
    
    def expensive_operation():
        print("执行昂贵计算...")
        time.sleep(0.1)
        return 42
    
    # 第一次调用，执行计算
    result1 = cache.get_or_set('result', expensive_operation)
    print(f"第一次: {result1}")
    
    # 第二次调用，使用缓存
    result2 = cache.get_or_set('result', expensive_operation)
    print(f"第二次: {result2} (从缓存)")


def example_statistics():
    """统计信息示例"""
    print("\n=== 统计信息 ===")
    
    cache = LRUCache(max_size=100)
    
    # 填充缓存
    for i in range(100):
        cache.set(f'key_{i}', i)
    
    # 执行一些操作
    for i in range(50):
        cache.get(f'key_{i}')  # 命中
    
    for i in range(100, 150):
        cache.get(f'key_{i}')  # 未命中
    
    stats = cache.stats()
    print(f"缓存大小: {stats['size']}/{stats['max_size']}")
    print(f"命中: {stats['hits']}")
    print(f"未命中: {stats['misses']}")
    print(f"命中率: {stats['hit_rate']:.2%}")


def example_ttl_cache():
    """TTLCache 专用示例"""
    print("\n=== TTLCache 专用 ===")
    
    cache = TTLCache(max_size=100, default_ttl=5)
    
    cache.set('session_1', {'user': 'alice', 'role': 'admin'})
    cache.set('session_2', {'user': 'bob', 'role': 'user'})
    
    print(f"会话数: {cache.size()}")
    
    # 刷新单个会话 TTL
    cache.refresh_ttl('session_1')
    print("已刷新 session_1 的 TTL")
    
    # 刷新所有会话
    cache.refresh_all()
    print("已刷新所有会话 TTL")


def example_bounded_cache():
    """有界缓存示例"""
    print("\n=== 有界缓存 ===")
    
    # 最大 100，最小保留 20
    cache = BoundedLRUCache(max_size=100, min_size=20)
    
    # 填充超过容量
    for i in range(150):
        cache.set(i, f'value_{i}')
    
    print(f"添加 150 条目后，大小: {cache.size()}")
    print(f"最小保留: {cache.min_size}")
    print("即使压力很大，也至少保留 min_size 个条目")


def example_weighted_cache():
    """加权缓存示例"""
    print("\n=== 加权缓存 ===")
    
    # 模拟内存限制
    cache = WeightedLRUCache(max_weight=1000)
    
    # 小对象
    cache.set('small_1', 'x' * 10, weight=10)
    cache.set('small_2', 'x' * 20, weight=20)
    
    # 大对象
    cache.set('large_1', 'x' * 500, weight=500)
    
    print(f"当前权重: {cache.current_weight()}/1000")
    print(f"可用权重: {cache.available_weight()}")
    
    # 添加会触发淘汰的大对象
    cache.set('large_2', 'x' * 400, weight=400)
    print(f"\n添加 large_2 后:")
    print(f"当前权重: {cache.current_weight()}/1000")


def example_expiring_priority():
    """过期优先缓存示例"""
    print("\n=== 过期优先缓存 ===")
    
    cache = ExpiringPriorityCache(max_size=5)
    
    # 添加不同 TTL 的条目
    cache.set('long_1', 1, ttl=60)
    cache.set('short_1', 2, ttl=0.5)
    cache.set('long_2', 3, ttl=60)
    cache.set('short_2', 4, ttl=0.5)
    cache.set('long_3', 5, ttl=60)
    
    print(f"添加 5 个条目，大小: {cache.size()}")
    
    time.sleep(0.6)
    print("等待短 TTL 条目过期...")
    
    # 添加新条目会优先淘汰即将过期的
    cache.set('new', 6)
    print(f"添加新条目后，大小: {cache.size()}")
    print(f"短 TTL 条目应已被淘汰")


def example_thread_safety():
    """线程安全示例"""
    print("\n=== 线程安全 ===")
    
    import threading
    
    cache = LRUCache(max_size=1000)
    errors = []
    
    def writer(start):
        for i in range(start, start + 100):
            try:
                cache.set(f'key_{i}', i)
            except Exception as e:
                errors.append(e)
    
    def reader():
        for i in range(200):
            try:
                cache.get(f'key_{i}')
            except Exception as e:
                errors.append(e)
    
    threads = [
        threading.Thread(target=writer, args=(0,)),
        threading.Thread(target=writer, args=(200,)),
        threading.Thread(target=reader),
        threading.Thread(target=reader),
    ]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    print(f"并发操作完成，错误数: {len(errors)}")
    print(f"最终缓存大小: {cache.size()}")


def main():
    """运行所有示例"""
    example_basic_usage()
    example_lru_eviction()
    example_ttl()
    example_decorator()
    example_batch_operations()
    example_get_or_set()
    example_statistics()
    example_ttl_cache()
    example_bounded_cache()
    example_weighted_cache()
    example_expiring_priority()
    example_thread_safety()
    
    print("\n=== 所有示例完成 ===")


if __name__ == '__main__':
    main()