"""
cache_utils 使用示例
====================

展示内存缓存工具的各种用法。
"""

import sys
import os
import time

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import MemoryCache, cached, memoize, TimedCache, RateLimiter


def example_basic_usage():
    """基本用法示例"""
    print("\n" + "=" * 50)
    print("示例1: 基本用法")
    print("=" * 50)
    
    # 创建缓存实例
    cache = MemoryCache()
    
    # 设置和获取值
    cache.set("name", "Alice")
    cache.set("age", 30)
    cache.set("city", "Beijing", ttl=60)  # 60秒后过期
    
    print(f"name: {cache.get('name')}")
    print(f"age: {cache.get('age')}")
    print(f"city: {cache.get('city')}")
    
    # 检查键是否存在
    print(f"has 'name': {cache.has('name')}")
    print(f"has 'missing': {cache.has('missing')}")
    
    # 删除键
    cache.delete("name")
    print(f"after delete, has 'name': {cache.has('name')}")
    
    # 清空缓存
    cache.clear()
    print(f"after clear, size: {cache.size()}")


def example_ttl():
    """TTL过期时间示例"""
    print("\n" + "=" * 50)
    print("示例2: 过期时间 (TTL)")
    print("=" * 50)
    
    cache = MemoryCache()
    
    # 设置10秒后过期
    cache.set("session", "abc123", ttl=10)
    
    # 检查剩余时间
    remaining = cache.ttl("session")
    print(f"session剩余时间: {remaining:.2f}秒")
    
    # 延长过期时间
    cache.extend_ttl("session", 20)
    remaining = cache.ttl("session")
    print(f"延长后剩余时间: {remaining:.2f}秒")
    
    # 设置永不过期
    cache.set("config", {"theme": "dark"}, ttl=-1)
    print(f"config永不过期: {cache.ttl('config')}")


def example_lru():
    """LRU淘汰示例"""
    print("\n" + "=" * 50)
    print("示例3: LRU淘汰")
    print("=" * 50)
    
    # 创建最大3个条目的缓存
    cache = MemoryCache(max_size=3)
    
    cache.set("a", 1)
    cache.set("b", 2)
    cache.set("c", 3)
    print(f"添加a, b, c后: {cache.keys()}")
    
    # 添加第4个，淘汰最早的a
    cache.set("d", 4)
    print(f"添加d后: {cache.keys()}")
    
    # 访问b使其变为最近使用
    cache.get("b")
    
    # 添加第5个，淘汰c（因为b刚被访问）
    cache.set("e", 5)
    print(f"添加e后(访问过b): {cache.keys()}")


def example_batch_operations():
    """批量操作示例"""
    print("\n" + "=" * 50)
    print("示例4: 批量操作")
    print("=" * 50)
    
    cache = MemoryCache()
    
    # 批量设置
    cache.set_many({
        "user:1": {"name": "Alice", "age": 30},
        "user:2": {"name": "Bob", "age": 25},
        "user:3": {"name": "Charlie", "age": 35},
    })
    print(f"设置后键: {cache.keys()}")
    
    # 批量获取
    users = cache.get_many(["user:1", "user:2", "user:4"])
    print(f"获取user:1, user:2, user:4: {users}")
    
    # 批量删除
    deleted = cache.delete_many(["user:1", "user:2"])
    print(f"删除了 {deleted} 个键")


def example_counter():
    """计数器示例"""
    print("\n" + "=" * 50)
    print("示例5: 计数器")
    print("=" * 50)
    
    cache = MemoryCache()
    
    # 设置初始值
    cache.set("page_views", 0)
    
    # 增加计数
    for _ in range(10):
        cache.incr("page_views")
    
    print(f"页面浏览量: {cache.get('page_views')}")
    
    # 批量增加
    cache.incr("page_views", 100)
    print(f"批量增加后: {cache.get('page_views')}")
    
    # 减少
    cache.decr("page_views", 5)
    print(f"减少5后: {cache.get('page_views')}")


def example_decorator():
    """装饰器示例"""
    print("\n" + "=" * 50)
    print("示例6: 函数结果缓存")
    print("=" * 50)
    
    # 使用memoize装饰器
    @memoize(ttl=60)
    def fibonacci(n):
        """计算斐波那契数（会被缓存）"""
        if n < 2:
            return n
        return fibonacci(n-1) + fibonacci(n-2)
    
    import time
    start = time.time()
    result1 = fibonacci(35)
    time1 = time.time() - start
    
    start = time.time()
    result2 = fibonacci(35)  # 从缓存获取
    time2 = time.time() - start
    
    print(f"fibonacci(35) = {result1}")
    print(f"第一次计算耗时: {time1:.6f}秒")
    print(f"第二次计算耗时: {time2:.6f}秒 (缓存)")
    
    # 使用cached装饰器（自定义缓存）
    api_cache = MemoryCache(max_size=100, default_ttl=300)
    
    @cached(cache=api_cache, key_prefix="api:")
    def fetch_user(user_id):
        """模拟API调用"""
        print(f"  实际调用API获取用户 {user_id}")
        return {"id": user_id, "name": f"User{user_id}"}
    
    print("\n调用fetch_user(1):")
    user1 = fetch_user(1)  # 实际调用
    print(f"  结果: {user1}")
    
    print("再次调用fetch_user(1):")
    user1_cached = fetch_user(1)  # 从缓存
    print(f"  结果: {user1_cached}")
    
    print(f"\n缓存统计: {fetch_user.cache_stats()}")


def example_stats():
    """统计信息示例"""
    print("\n" + "=" * 50)
    print("示例7: 统计信息")
    print("=" * 50)
    
    cache = MemoryCache()
    
    # 模拟一些操作
    cache.set("a", 1)
    cache.set("b", 2)
    cache.set("c", 3)
    
    # 命中
    for _ in range(10):
        cache.get("a")
        cache.get("b")
    
    # 未命中
    for _ in range(5):
        cache.get("missing")
    
    stats = cache.stats()
    print(f"缓存大小: {stats['size']}")
    print(f"命中次数: {stats['hits']}")
    print(f"未命中次数: {stats['misses']}")
    print(f"命中率: {stats['hit_rate']:.2%}")
    print(f"淘汰次数: {stats['evictions']}")
    print(f"过期次数: {stats['expirations']}")


def example_timed_cache():
    """时间窗口缓存示例"""
    print("\n" + "=" * 50)
    print("示例8: 时间窗口缓存")
    print("=" * 50)
    
    # 1分钟窗口缓存
    cache = TimedCache(window=60)
    
    # 存储用户最近活动
    cache.set("user:123:last_activity", {"page": "home", "time": time.time()})
    
    # 获取并刷新过期时间
    activity = cache.get("user:123:last_activity", refresh=True)
    print(f"用户活动: {activity}")


def example_rate_limiter():
    """速率限制器示例"""
    print("\n" + "=" * 50)
    print("示例9: 速率限制器")
    print("=" * 50)
    
    # 每分钟最多5次请求
    limiter = RateLimiter(max_requests=5, window=60)
    
    user_id = "user:123"
    
    print("模拟API请求:")
    for i in range(8):
        if limiter.allow(user_id):
            print(f"  请求 {i+1}: 允许 (剩余: {limiter.remaining(user_id)})")
        else:
            print(f"  请求 {i+1}: 拒绝 (超出速率限制)")
    
    # 重置限制
    limiter.reset(user_id)
    print(f"\n重置后: 剩余 {limiter.remaining(user_id)} 次")


def example_get_or_set():
    """get_or_set示例"""
    print("\n" + "=" * 50)
    print("示例10: 懒加载 (get_or_set)")
    print("=" * 50)
    
    cache = MemoryCache()
    
    def expensive_computation():
        """模拟耗时计算"""
        print("  执行耗时计算...")
        time.sleep(0.1)
        return "computed_value"
    
    print("第一次调用:")
    result1 = cache.get_or_set("key", expensive_computation, ttl=60)
    print(f"  结果: {result1}")
    
    print("第二次调用:")
    result2 = cache.get_or_set("key", expensive_computation, ttl=60)
    print(f"  结果: {result2} (从缓存)")


def example_context_manager():
    """上下文管理器示例"""
    print("\n" + "=" * 50)
    print("示例11: 上下文管理器")
    print("=" * 50)
    
    with MemoryCache() as cache:
        cache.set("temp", "value")
        print(f"缓存中: {cache.get('temp')}")
    
    print(f"退出后缓存大小: {cache.size()}")


def example_api_cache():
    """API缓存实战示例"""
    print("\n" + "=" * 50)
    print("示例12: API缓存实战")
    print("=" * 50)
    
    # 创建缓存实例
    api_cache = MemoryCache(
        max_size=1000,
        default_ttl=300,  # 5分钟默认过期
        cleanup_interval=60,  # 每分钟清理过期
        thread_safe=True
    )
    
    # 模拟API调用
    def get_user_info(user_id):
        """获取用户信息（带缓存）"""
        cache_key = f"user:{user_id}"
        
        def fetch():
            print(f"  从数据库获取用户 {user_id}...")
            return {
                "id": user_id,
                "name": f"User{user_id}",
                "email": f"user{user_id}@example.com"
            }
        
        return api_cache.get_or_set(cache_key, fetch, ttl=600)
    
    # 使用
    print("第一次获取:")
    user1 = get_user_info(1)
    print(f"  用户: {user1['name']}")
    
    print("\n第二次获取（从缓存）:")
    user1 = get_user_info(1)
    print(f"  用户: {user1['name']}")
    
    print(f"\n缓存统计: {api_cache.stats()}")


def run_all_examples():
    """运行所有示例"""
    print("=" * 50)
    print("cache_utils 使用示例")
    print("=" * 50)
    
    example_basic_usage()
    example_ttl()
    example_lru()
    example_batch_operations()
    example_counter()
    example_decorator()
    example_stats()
    example_timed_cache()
    example_rate_limiter()
    example_get_or_set()
    example_context_manager()
    example_api_cache()
    
    print("\n" + "=" * 50)
    print("所有示例运行完成!")
    print("=" * 50)


if __name__ == "__main__":
    run_all_examples()