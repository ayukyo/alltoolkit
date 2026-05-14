"""
速率限制器工具库使用示例

展示各种速率限制算法的使用场景。
"""

import time
import threading
from mod import (
    TokenBucket,
    SlidingWindow,
    FixedWindow,
    LeakyBucket,
    MultiLimiter,
    RateLimiterRegistry,
    rate_limit,
    rate_limit_context,
    RateLimitExceeded,
    create_token_bucket,
    create_sliding_window,
    create_fixed_window,
    create_leaky_bucket,
)


def example_01_token_bucket_basic():
    """示例 01：令牌桶基本用法"""
    print("\n=== 示例 01：令牌桶基本用法 ===")
    
    # 创建令牌桶：每秒生成 10 个令牌，最大容量 100
    bucket = TokenBucket(rate=10, capacity=100)
    
    print(f"初始令牌数: {bucket.tokens}")
    
    # 获取 5 个令牌
    result = bucket.acquire(5)
    print(f"获取 5 个令牌: allowed={result.allowed}, remaining={result.remaining}")
    
    # 获取 50 个令牌
    result = bucket.acquire(50)
    print(f"获取 50 个令牌: allowed={result.allowed}, remaining={result.remaining}")
    
    # 尝试获取超过剩余数量的令牌
    result = bucket.acquire(50)
    print(f"尝试获取 50 个令牌: allowed={result.allowed}, retry_after={result.retry_after:.2f}s")


def example_02_token_bucket_burst():
    """示例 02：令牌桶处理突发流量"""
    print("\n=== 示例 02：令牌桶处理突发流量 ===")
    
    # 允许突发：容量 100，但每秒只生成 10 个
    bucket = TokenBucket(rate=10, capacity=100)
    
    print("模拟突发流量...")
    
    # 突发请求
    for i in range(12):
        result = bucket.try_acquire(10)
        status = "✓ 允许" if result.allowed else "✗ 拒绝"
        print(f"  请求 {i+1}: {status}, 剩余: {result.remaining}")
        
        if not result.allowed:
            print(f"  等待 {result.retry_after:.2f}s 后重试...")
            break


def example_03_sliding_window():
    """示例 03：滑动窗口精确控制"""
    print("\n=== 示例 03：滑动窗口精确控制 ===")
    
    # 每秒最多 5 个请求
    window = SlidingWindow(max_requests=5, window_size=1.0)
    
    print("发送 10 个请求（窗口大小 1 秒，最大 5 个）：")
    for i in range(10):
        result = window.acquire(1)
        status = "✓" if result.allowed else "✗"
        print(f"  请求 {i+1}: {status} (窗口内请求: {window.current_count})")
    
    print(f"\n等待 1 秒后重试...")
    time.sleep(1.1)
    
    result = window.acquire(1)
    print(f"请求 11: {'✓' if result.allowed else '✗'} (窗口内请求: {window.current_count})")


def example_04_fixed_window():
    """示例 04：固定窗口简单高效"""
    print("\n=== 示例 04：固定窗口简单高效 ===")
    
    # 每 2 秒最多 10 个请求
    window = FixedWindow(max_requests=10, window_size=2.0)
    
    print("模拟 API 调用限流（每 2 秒 10 个请求）：")
    
    for i in range(15):
        result = window.acquire(1)
        status = "✓" if result.allowed else "✗"
        print(f"  调用 {i+1}: {status} (当前计数: {window.current_count})")
    
    print(f"\n重置窗口...")
    window.reset()
    print(f"重置后计数: {window.current_count}")


def example_05_leaky_bucket():
    """示例 05：漏桶平滑流量"""
    print("\n=== 示例 05：漏桶平滑流量 ===")
    
    # 漏桶：每秒处理 5 个请求，最大排队 10 个
    bucket = LeakyBucket(rate=5, capacity=10)
    
    print("模拟流量整形（入站突发，出站平滑）：")
    
    # 突发请求
    print("入站 15 个请求...")
    for i in range(15):
        result = bucket.try_acquire(1)
        status = "✓ 入队" if result.allowed else "✗ 拒绝"
        print(f"  请求 {i+1}: {status} (水位: {bucket.water_level:.1f})")
    
    print(f"\n等待 1 秒观察漏水...")
    time.sleep(1)
    print(f"当前水位: {bucket.water_level:.1f} (漏掉了约 5 个)")


def example_06_multi_limiter():
    """示例 06：多维度限制"""
    print("\n=== 示例 06：多维度限制 ===")
    
    # 创建多维度限制器
    config = {
        "ip": (TokenBucket, {"rate": 100, "capacity": 1000}),  # IP 级别
        "user": (SlidingWindow, {"max_requests": 50, "window_size": 60}),  # 用户级别
        "api": (FixedWindow, {"max_requests": 1000, "window_size": 60}),  # API 级别
    }
    multi = MultiLimiter(config)
    
    print("多维度限流检查：")
    
    # 检查所有维度
    results = multi.acquire(1)
    for dim, result in results.items():
        status = "✓" if result.allowed else "✗"
        print(f"  {dim}: {status}, remaining={result.remaining}")
    
    # 检查是否全部允许
    print(f"\n全部维度允许: {multi.is_allowed(1)}")
    
    # 获取最长等待时间
    print(f"最长等待时间: {multi.get_retry_after():.2f}s")


def example_07_rate_limit_decorator():
    """示例 07：装饰器限流"""
    print("\n=== 示例 07：装饰器限流 ===")
    
    # 创建限制器
    api_limiter = TokenBucket(rate=2, capacity=10)
    
    # 使用装饰器
    @rate_limit(api_limiter, tokens=1)
    def call_api(endpoint):
        return f"API 调用成功: {endpoint}"
    
    print("模拟 API 调用限流（每秒 2 个，最大 10 个）：")
    
    for i in range(12):
        try:
            result = call_api(f"/users/{i}")
            print(f"  {result}")
        except RateLimitExceeded as e:
            print(f"  ✗ 调用 {i+1} 被限流: {e}")
            break
    
    # 带自定义回调
    def on_reject(result):
        return f"请求被限流，请 {result.retry_after:.2f}s 后重试"
    
    @rate_limit(api_limiter, tokens=1, on_reject=on_reject)
    def call_api_with_fallback(endpoint):
        return f"API 调用成功: {endpoint}"
    
    print("\n使用自定义回调：")
    result = call_api_with_fallback("/users/100")
    print(f"  {result}")


def example_08_context_manager():
    """示例 08：上下文管理器限流"""
    print("\n=== 示例 08：上下文管理器限流 ===")
    
    limiter = TokenBucket(rate=5, capacity=5)
    
    print("使用上下文管理器：")
    
    for i in range(7):
        try:
            with rate_limit_context(limiter) as result:
                print(f"  请求 {i+1}: ✓ 执行 (remaining: {result.remaining})")
        except RateLimitExceeded as e:
            print(f"  请求 {i+1}: ✗ 被限流")


def example_09_registry():
    """示例 09：注册表管理"""
    print("\n=== 示例 09：注册表管理 ===")
    
    registry = RateLimiterRegistry()
    registry.clear()
    
    # 注册多个限制器
    registry.register("api_global", TokenBucket(rate=1000, capacity=10000))
    registry.register("api_user", SlidingWindow(max_requests=100, window_size=60))
    registry.register("api_ip", FixedWindow(max_requests=500, window_size=60))
    
    print(f"已注册限制器: {registry.names()}")
    
    # 使用限制器
    api_limiter = registry.get("api_global")
    if api_limiter:
        result = api_limiter.acquire(1)
        print(f"api_global 请求: allowed={result.allowed}, remaining={result.remaining}")
    
    # 注销限制器
    registry.unregister("api_ip")
    print(f"注销后限制器: {registry.names()}")


def example_10_concurrent_access():
    """示例 10：并发访问"""
    print("\n=== 示例 10：并发访问 ===")
    
    limiter = TokenBucket(rate=100, capacity=100)
    success_count = 0
    fail_count = 0
    lock = threading.Lock()
    
    def worker(worker_id):
        nonlocal success_count, fail_count
        result = limiter.try_acquire(1)
        with lock:
            if result.allowed:
                success_count += 1
            else:
                fail_count += 1
    
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(150)]
    
    print(f"并发发送 150 个请求（容量 100）...")
    
    start = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    elapsed = time.time() - start
    
    print(f"  成功: {success_count}")
    print(f"  失败: {fail_count}")
    print(f"  耗时: {elapsed:.3f}s")


def example_11_wait_for_token():
    """示例 11：等待令牌"""
    print("\n=== 示例 11：等待令牌 ===")
    
    # 每秒生成 10 个令牌，初始为空
    limiter = TokenBucket(rate=10, capacity=100, initial_tokens=0)
    
    print("等待令牌可用（初始为空，每秒生成 10 个）...")
    
    # 阻塞等待
    start = time.time()
    success = limiter.wait_for_token(5, timeout=2.0)
    elapsed = time.time() - start
    
    print(f"  成功获取 5 个令牌: {success}")
    print(f"  等待时间: {elapsed:.2f}s")


def example_12_api_rate_limiter():
    """示例 12：API 限流实战"""
    print("\n=== 示例 12：API 限流实战 ===")
    
    # 模拟 API 限流配置
    # - 每个 IP 每分钟最多 100 请求
    # - 每个用户每分钟最多 50 请求
    # - 全局每秒最多 1000 请求
    
    limiter_registry = {
        "ip": (SlidingWindow, {"max_requests": 100, "window_size": 60}),
        "user": (SlidingWindow, {"max_requests": 50, "window_size": 60}),
        "global": (TokenBucket, {"rate": 1000, "capacity": 10000}),
    }
    
    class APIClient:
        def __init__(self, registry):
            self.limiter = MultiLimiter(registry)
        
        def request(self, endpoint, ip, user_id):
            # 检查所有维度
            results = self.limiter.try_acquire(1)
            
            # 收集被拒绝的维度
            blocked = [dim for dim, r in results.items() if not r.allowed]
            
            if blocked:
                retry_after = self.limiter.get_retry_after()
                return {
                    "success": False,
                    "error": f"Rate limit exceeded for: {blocked}",
                    "retry_after": retry_after
                }
            
            # 执行请求
            return {
                "success": True,
                "endpoint": endpoint,
                "ip": ip,
                "user_id": user_id
            }
    
    client = APIClient(limiter_registry)
    
    # 模拟请求
    print("模拟 API 客户端请求：")
    
    for i in range(55):
        result = client.request(f"/api/data/{i}", "192.168.1.1", "user_001")
        if i < 3 or i >= 48:  # 只显示前几个和后几个
            status = "✓" if result["success"] else "✗"
            print(f"  请求 {i+1}: {status}")
            if not result["success"]:
                print(f"    错误: {result['error']}")
                print(f"    重试等待: {result['retry_after']:.2f}s")
        elif i == 3:
            print("  ...")


def example_13_rate_limiter_comparison():
    """示例 13：算法对比"""
    print("\n=== 示例 13：算法对比 ===")
    
    print("不同速率限制算法的特点：\n")
    
    print("1. 令牌桶 (Token Bucket)")
    print("   - 允许突发流量")
    print("   - 令牌按固定速率生成")
    print("   - 适合需要处理突发流量的场景")
    print("   - 示例：API 网关、图片处理服务")
    
    print("\n2. 滑动窗口 (Sliding Window)")
    print("   - 精确控制，无边界效应")
    print("   - 内存使用与请求数成正比")
    print("   - 适合需要精确限制的场景")
    print("   - 示例：支付系统、短信验证码")
    
    print("\n3. 固定窗口 (Fixed Window)")
    print("   - 简单高效，内存占用低")
    print("   - 存在边界效应")
    print("   - 适合简单限流场景")
    print("   - 示例：日志系统、监控数据")
    
    print("\n4. 漏桶 (Leaky Bucket)")
    print("   - 严格限制流出速率")
    print("   - 平滑流量，不允许突发")
    print("   - 适合需要稳定输出的场景")
    print("   - 示例：网络流量整形、消息队列消费")


if __name__ == "__main__":
    print("=" * 60)
    print("速率限制器工具库 - 使用示例")
    print("=" * 60)
    
    example_01_token_bucket_basic()
    example_02_token_bucket_burst()
    example_03_sliding_window()
    example_04_fixed_window()
    example_05_leaky_bucket()
    example_06_multi_limiter()
    example_07_rate_limit_decorator()
    example_08_context_manager()
    example_09_registry()
    example_10_concurrent_access()
    example_11_wait_for_token()
    example_12_api_rate_limiter()
    example_13_rate_limiter_comparison()
    
    print("\n" + "=" * 60)
    print("示例运行完成")
    print("=" * 60)