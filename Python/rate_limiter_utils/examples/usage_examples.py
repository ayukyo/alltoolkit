"""
Rate Limiter Utils 使用示例

演示各种速率限制算法的使用场景。
"""

import time
import threading
from mod import (
    TokenBucket,
    LeakyBucket,
    SlidingWindow,
    FixedWindow,
    RateLimiter,
    MultiRateLimiter,
    create_token_bucket,
    create_sliding_window,
)


def example_token_bucket():
    """
    令牌桶示例 - API请求限流
    
    场景：允许一定程度的突发流量
    """
    print("=" * 50)
    print("令牌桶示例 - API请求限流")
    print("=" * 50)
    
    # 创建容量100，每秒填充10个令牌的桶
    bucket = TokenBucket(capacity=100, refill_rate=10.0)
    
    print(f"初始可用令牌: {bucket.available:.1f}")
    
    # 突发请求：一次消耗50个
    print("\n突发请求50个...")
    if bucket.acquire(50):
        print("✓ 成功获取50个令牌")
    print(f"剩余令牌: {bucket.available:.1f}")
    
    # 小请求
    print("\n小请求10个...")
    if bucket.acquire(10):
        print("✓ 成功获取10个令牌")
    print(f"剩余令牌: {bucket.available:.1f}")
    
    # 超出容量的请求
    print("\n尝试获取100个令牌...")
    if not bucket.acquire(100):
        print("✗ 令牌不足，请求被拒绝")
    
    # 等待令牌填充
    print("\n等待2秒让令牌填充...")
    time.sleep(2)
    print(f"当前可用令牌: {bucket.available:.1f}")
    
    # 再次尝试
    if bucket.acquire(20):
        print("✓ 成功获取20个令牌")


def example_leaky_bucket():
    """
    漏桶示例 - 网络流量整形
    
    场景：平滑输出，防止网络拥塞
    """
    print("\n" + "=" * 50)
    print("漏桶示例 - 网络流量整形")
    print("=" * 50)
    
    # 创建容量50，每秒漏出10个请求的桶
    bucket = LeakyBucket(capacity=50, leak_rate=10.0)
    
    print(f"初始可用容量: {bucket.available:.1f}")
    
    # 模拟请求到达
    print("\n模拟请求到达...")
    for i in range(15):
        if bucket.acquire(1):
            print(f"  请求 {i+1}: ✓ 已接受")
        else:
            print(f"  请求 {i+1}: ✗ 被拒绝（桶满）")
    
    print(f"\n当前水量: {50 - bucket.available:.1f}")
    
    # 等待漏水
    print("等待1秒让水漏出...")
    time.sleep(1)
    print(f"当前水量: {50 - bucket.available:.1f}")
    print(f"当前可用容量: {bucket.available:.1f}")


def example_sliding_window():
    """
    滑动窗口示例 - 用户请求限制
    
    场景：精确控制用户在时间窗口内的请求数
    """
    print("\n" + "=" * 50)
    print("滑动窗口示例 - 用户请求限制")
    print("=" * 50)
    
    # 限制：10秒内最多5个请求
    window = SlidingWindow(max_requests=5, window_seconds=10.0)
    
    print("限制：10秒内最多5个请求")
    print(f"窗口大小: {window.window_seconds}秒")
    
    # 模拟用户请求
    for i in range(7):
        result = "✓ 允许" if window.acquire(1) else "✗ 拒绝"
        count = window.current_count
        print(f"  请求 {i+1}: {result} (当前窗口: {count}个)")
    
    print(f"\n当前窗口内请求数: {window.current_count}")
    print(f"剩余可用: {window.available:.0f}")
    
    # 等待部分窗口时间
    print("\n等待5秒...")
    time.sleep(5)
    print(f"当前窗口内请求数: {window.current_count}")


def example_fixed_window():
    """
    固定窗口示例 - 简单的访问计数
    
    场景：简单的API配额限制
    """
    print("\n" + "=" * 50)
    print("固定窗口示例 - 简单的访问计数")
    print("=" * 50)
    
    # 限制：每分钟最多60个请求
    window = FixedWindow(max_requests=60, window_seconds=60.0)
    
    print("限制：每分钟最多60个请求")
    
    # 模拟一批请求
    print("\n发送30个请求...")
    for _ in range(30):
        window.acquire(1)
    
    print(f"当前窗口请求数: {window.current_count}")
    print(f"剩余配额: {window.available:.0f}")
    print(f"距窗口重置: {window.time_until_reset:.1f}秒")


def example_rate_limiter():
    """
    综合速率限制器示例 - 装饰器用法
    """
    print("\n" + "=" * 50)
    print("综合速率限制器示例 - 装饰器用法")
    print("=" * 50)
    
    # 创建限制器：每秒最多3个请求
    limiter = RateLimiter(max_requests=3, window_seconds=1.0,
                          algorithm=RateLimiter.ALGORITHM_TOKEN_BUCKET)
    
    @limiter.limit(on_limit=lambda: {"status": "rate_limited", "retry_after": 1})
    def api_endpoint():
        return {"status": "success", "data": "some data"}
    
    print("模拟API调用...")
    for i in range(5):
        result = api_endpoint()
        status = result.get("status")
        if status == "success":
            print(f"  调用 {i+1}: ✓ 成功")
        else:
            print(f"  调用 {i+1}: ✗ 限流")


def example_multi_key():
    """
    多键速率限制器示例 - 多用户API限流
    """
    print("\n" + "=" * 50)
    print("多键速率限制器示例 - 多用户API限流")
    print("=" * 50)
    
    # 每个用户每秒最多5个请求
    limiter = MultiRateLimiter(max_requests=5, window_seconds=1.0,
                               algorithm=RateLimiter.ALGORITHM_SLIDING_WINDOW)
    
    users = ["alice", "bob", "alice", "charlie", "alice", "bob"]
    
    print("模拟多用户请求...")
    for user in users:
        if limiter.acquire(user, 1):
            print(f"  {user}: ✓ 允许")
        else:
            print(f"  {user}: ✗ 限流")
    
    print(f"\n活跃用户数: {limiter.key_count}")
    
    # 查看各用户剩余配额
    print("\n各用户剩余配额:")
    for user in ["alice", "bob", "charlie"]:
        available = limiter.available(user)
        print(f"  {user}: {available:.0f}")


def example_wait_for():
    """
    等待获取示例 - 阻塞等待
    """
    print("\n" + "=" * 50)
    print("等待获取示例 - 阻塞等待")
    print("=" * 50)
    
    # 创建一个很快会耗尽的限制器
    limiter = create_sliding_window(max_requests=2, window_seconds=1.0)
    
    # 先用完配额
    print("用完配额...")
    limiter.acquire(1)
    limiter.acquire(1)
    print(f"剩余配额: {limiter.available:.0f}")
    
    # 尝试等待获取（带超时）
    print("\n尝试等待获取（超时0.5秒）...")
    start = time.time()
    result = limiter.wait_for(1, timeout=0.5)
    elapsed = time.time() - start
    print(f"结果: {'成功' if result else '超时'}")
    print(f"耗时: {elapsed:.2f}秒")
    
    # 等待足够长时间让窗口滑动
    print("\n等待1.5秒让窗口滑动...")
    time.sleep(1.5)
    
    print(f"剩余配额: {limiter.available:.0f}")
    result = limiter.wait_for(1, timeout=1.0)
    print(f"等待获取: {'成功' if result else '失败'}")


def example_concurrent_access():
    """
    并发访问示例 - 多线程安全
    """
    print("\n" + "=" * 50)
    print("并发访问示例 - 多线程安全")
    print("=" * 50)
    
    bucket = TokenBucket(capacity=100, refill_rate=50.0)
    
    success_count = [0]
    fail_count = [0]
    lock = threading.Lock()
    
    def worker(thread_id):
        for _ in range(10):
            if bucket.acquire(1):
                with lock:
                    success_count[0] += 1
            else:
                with lock:
                    fail_count[0] += 1
    
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
    
    print("启动10个线程，每个尝试10次获取...")
    start = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    elapsed = time.time() - start
    print(f"完成时间: {elapsed:.3f}秒")
    print(f"成功: {success_count[0]}, 失败: {fail_count[0]}")
    print(f"最终可用令牌: {bucket.available:.1f}")


def example_rate_limiting_strategies():
    """
    不同策略对比
    """
    print("\n" + "=" * 50)
    print("不同策略对比")
    print("=" * 50)
    
    strategies = [
        ("令牌桶", TokenBucket(10, 2.0)),
        ("漏桶", LeakyBucket(10, 2.0)),
        ("滑动窗口", SlidingWindow(10, 5.0)),
        ("固定窗口", FixedWindow(10, 5.0)),
    ]
    
    print("连续请求测试（每策略10个请求）:\n")
    
    for name, limiter in strategies:
        results = []
        for _ in range(15):
            results.append("✓" if limiter.acquire(1) else "✗")
        
        available = limiter.available
        print(f"{name}:")
        print(f"  结果: {' '.join(results)}")
        print(f"  剩余: {available:.1f}\n")


def main():
    """运行所有示例"""
    print("Rate Limiter Utils 使用示例")
    print("=" * 50)
    
    example_token_bucket()
    example_leaky_bucket()
    example_sliding_window()
    example_fixed_window()
    example_rate_limiter()
    example_multi_key()
    example_wait_for()
    example_concurrent_access()
    example_rate_limiting_strategies()
    
    print("\n所有示例完成！")


if __name__ == "__main__":
    main()