"""
Memoization Utils 使用示例

展示函数缓存、TTL 过期、方法缓存等场景的实际应用。

Author: AllToolkit
Date: 2026-04-23
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from mod import (
    memoize,
    memoize_method,
    MemoizedFunction,
    lru_cache,
    ttl_cache,
    cached_property,
    MemoCache,
)


def example_basic_memoization():
    """基本记忆化示例"""
    print("=" * 50)
    print("基本记忆化示例")
    print("=" * 50)
    
    call_count = 0
    
    @memoize(max_size=128)
    def fibonacci(n):
        """递归斐波那契，带缓存"""
        nonlocal call_count
        call_count += 1
        if n <= 1:
            return n
        return fibonacci(n-1) + fibonacci(n-2)
    
    start = time.time()
    result = fibonacci(30)
    elapsed = time.time() - start
    
    print(f"fibonacci(30) = {result}")
    print(f"实际计算次数: {call_count}")
    print(f"耗时: {elapsed:.4f}s")
    print(f"缓存统计: {fibonacci.cache_stats()}")
    print()


def example_ttl_cache():
    """TTL 缓存示例"""
    print("=" * 50)
    print("TTL 缓存示例 - 模拟 API 调用")
    print("=" * 50)
    
    @ttl_cache(ttl=2)  # 2秒过期
    def fetch_user(user_id):
        """模拟 API 调用"""
        print(f"  -> 实际调用 API 获取用户 {user_id}")
        return {"id": user_id, "name": f"User{user_id}"}
    
    print("第一次调用:")
    user1 = fetch_user(1)
    print(f"  结果: {user1}")
    
    print("\n第二次调用（使用缓存）:")
    user2 = fetch_user(1)
    print(f"  结果: {user2}")
    
    print("\n等待 2 秒后调用（缓存过期）:")
    time.sleep(2)
    user3 = fetch_user(1)
    print(f"  结果: {user3}")
    print()


def example_method_memoization():
    """方法记忆化示例"""
    print("=" * 50)
    print("方法记忆化示例 - 数据分析器")
    print("=" * 50)
    
    class DataAnalyzer:
        def __init__(self, data):
            self.data = data
        
        @memoize_method(max_size=100)
        def moving_average(self, window):
            """计算移动平均"""
            print(f"  -> 计算窗口大小 {window} 的移动平均")
            if window > len(self.data):
                return None
            result = []
            for i in range(len(self.data) - window + 1):
                avg = sum(self.data[i:i+window]) / window
                result.append(avg)
            return result
        
        @memoize_method()
        def statistics(self):
            """计算统计信息"""
            print("  -> 计算统计信息")
            return {
                "mean": sum(self.data) / len(self.data),
                "min": min(self.data),
                "max": max(self.data),
                "sum": sum(self.data)
            }
    
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    analyzer = DataAnalyzer(data)
    
    print("第一次计算:")
    ma1 = analyzer.moving_average(3)
    print(f"  移动平均: {ma1}")
    
    print("\n第二次计算（使用缓存）:")
    ma2 = analyzer.moving_average(3)
    print(f"  移动平均: {ma2}")
    
    print("\n不同参数:")
    ma3 = analyzer.moving_average(5)
    print(f"  移动平均: {ma3}")
    print()


def example_lru_cache():
    """LRU 缓存示例"""
    print("=" * 50)
    print("LRU 缓存示例 - 计算密集型任务")
    print("=" * 50)
    
    @lru_cache(max_size=5)
    def expensive_computation(n):
        """模拟耗时计算"""
        print(f"  -> 计算中: {n}^10")
        return n ** 10
    
    # 填充缓存
    for i in range(1, 6):
        expensive_computation(i)
    
    print(f"\n缓存状态: {expensive_computation.cache_stats()}")
    
    # 访问最旧的元素，使其变为最新
    print("\n访问 n=1:")
    expensive_computation(1)
    
    # 添加新元素，应该淘汰 n=2（现在是最旧的）
    print("\n添加 n=6（触发淘汰）:")
    expensive_computation(6)
    
    print(f"\n缓存状态: {expensive_computation.cache_stats()}")
    
    # n=2 需要重新计算
    print("\n再次访问 n=2（已被淘汰）:")
    expensive_computation(2)
    print()


def example_cached_property():
    """缓存属性示例"""
    print("=" * 50)
    print("缓存属性示例")
    print("=" * 50)
    
    class Config:
        def __init__(self, values):
            self._values = values
        
        @cached_property
        def processed_data(self):
            """延迟计算并缓存的数据"""
            print("  -> 处理数据...")
            return [v * 2 for v in self._values]
        
        @cached_property
        def summary(self):
            """数据摘要"""
            print("  -> 生成摘要...")
            return {
                "count": len(self._values),
                "total": sum(self._values)
            }
    
    config = Config([1, 2, 3, 4, 5])
    
    print("第一次访问:")
    data = config.processed_data
    print(f"  processed_data = {data}")
    
    print("\n第二次访问（使用缓存）:")
    data = config.processed_data
    print(f"  processed_data = {data}")
    print()


def example_memo_cache_class():
    """MemoCache 类使用示例"""
    print("=" * 50)
    print("MemoCache 类示例 - 手动缓存控制")
    print("=" * 50)
    
    # 创建缓存实例
    cache = MemoCache(max_size=10, ttl=60)
    
    # 手动设置缓存
    cache.set(("user", 1), {}, {"name": "Alice", "age": 30})
    cache.set(("user", 2), {}, {"name": "Bob", "age": 25})
    
    print("缓存内容:")
    found, user = cache.get(("user", 1), {})
    if found:
        print(f"  user:1 = {user}")
    
    found, user = cache.get(("user", 2), {})
    if found:
        print(f"  user:2 = {user}")
    
    print(f"\n缓存统计: {cache.stats()}")
    
    # 清理缓存
    cache.cleanup()
    print(f"\n清理后统计: {cache.stats()}")
    print()


def example_api_cache():
    """API 响应缓存示例"""
    print("=" * 50)
    print("API 响应缓存示例")
    print("=" * 50)
    
    class APIClient:
        def __init__(self):
            self.request_count = 0
        
        @memoize(ttl=10, max_size=100)
        def get_user(self, user_id):
            """获取用户信息（缓存10秒）"""
            self.request_count += 1
            print(f"  -> 请求 API: /users/{user_id}")
            return {
                "id": user_id,
                "name": f"User{user_id}",
                "email": f"user{user_id}@example.com"
            }
        
        @memoize(ttl=30, max_size=50)
        def get_posts(self, user_id, limit=10):
            """获取用户帖子"""
            self.request_count += 1
            print(f"  -> 请求 API: /users/{user_id}/posts?limit={limit}")
            return [
                {"id": i, "title": f"Post {i}"}
                for i in range(1, limit + 1)
            ]
    
    client = APIClient()
    
    print("第一次请求:")
    user1 = client.get_user(1)
    print(f"  用户: {user1['name']}")
    
    print("\n第二次请求（使用缓存）:")
    user2 = client.get_user(1)
    print(f"  用户: {user2['name']}")
    
    print(f"\n总请求次数: {client.request_count}")
    print(f"用户缓存: {client.get_user.cache_stats()}")
    print()


def example_recursion_optimization():
    """递归优化示例"""
    print("=" * 50)
    print("递归优化示例 - 动态规划风格")
    print("=" * 50)
    
    # 无缓存版本
    def fib_slow(n):
        if n <= 1:
            return n
        return fib_slow(n-1) + fib_slow(n-2)
    
    # 有缓存版本
    @memoize(max_size=1000)
    def fib_fast(n):
        if n <= 1:
            return n
        return fib_fast(n-1) + fib_fast(n-2)
    
    n = 35
    
    print(f"计算 fibonacci({n}):")
    
    start = time.time()
    result_fast = fib_fast(n)
    elapsed_fast = time.time() - start
    print(f"  有缓存版本: {result_fast} ({elapsed_fast:.4f}s)")
    print(f"  缓存统计: {fib_fast.cache_stats()}")
    
    start = time.time()
    result_slow = fib_slow(n)
    elapsed_slow = time.time() - start
    print(f"  无缓存版本: {result_slow} ({elapsed_slow:.4f}s)")
    
    speedup = elapsed_slow / elapsed_fast if elapsed_fast > 0 else float('inf')
    print(f"  加速比: {speedup:.0f}x")
    print()


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print(" Memoization Utils 使用示例")
    print("=" * 60 + "\n")
    
    example_basic_memoization()
    example_ttl_cache()
    example_method_memoization()
    example_lru_cache()
    example_cached_property()
    example_memo_cache_class()
    example_api_cache()
    example_recursion_optimization()
    
    print("=" * 60)
    print(" 示例运行完成")
    print("=" * 60)


if __name__ == "__main__":
    main()