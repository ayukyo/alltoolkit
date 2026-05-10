"""
Rate Limiter Utils 使用示例

演示各种限流算法和场景应用。
"""

import time
import threading
from mod import (
    TokenBucket, LeakyBucket, SlidingWindow, FixedWindow,
    RateLimiter, RateLimitExceeded, MultiRateLimiter,
    create_rate_limiter, rate_limit
)


def example_token_bucket():
    """令牌桶示例 - 适合需要突发流量的场景"""
    print("\n" + "="*60)
    print("=== 令牌桶 (Token Bucket) 示例 ===")
    print("特点：允许突发流量，平滑限流")
    print("="*60)
    
    # 创建容量10，每秒补充2个令牌的桶
    bucket = TokenBucket(capacity=10, refill_rate=2)
    
    print(f"\n初始状态：容量={bucket.capacity}, 可用={bucket.available:.0f}")
    
    # 突发请求演示
    print("\n--- 突发请求演示 ---")
    results = []
    for i in range(15):
        success = bucket.acquire(1)
        results.append((i+1, success, bucket.available))
        status = "✓ 成功" if success else "✗ 被限流"
        print(f"请求 {i+1:2d}: {status} (剩余: {bucket.available:.1f})")
    
    print("\n等待令牌补充...")
    time.sleep(2.0)  # 等待补充约4个令牌
    print(f"补充后可用: {bucket.available:.1f}")
    
    # 再次请求
    print("\n--- 等待后请求 ---")
    for i in range(5):
        success = bucket.acquire(1)
        status = "✓ 成功" if success else "✗ 被限流"
        print(f"请求 {i+1}: {status} (剩余: {bucket.available:.1f})")


def example_leaky_bucket():
    """漏桶示例 - 适合需要固定输出速率的场景"""
    print("\n" + "="*60)
    print("=== 漏桶 (Leaky Bucket) 示例 ===")
    print("特点：固定输出速率，严格限流")
    print("="*60)
    
    # 创建容量10，每秒处理2个请求的桶
    bucket = LeakyBucket(capacity=10, leak_rate=2)
    
    print(f"\n初始状态：容量={bucket.capacity}, 可用空间={bucket.available:.0f}")
    
    # 快速填满桶
    print("\n--- 快速填满桶 ---")
    for i in range(12):
        success = bucket.acquire(1)
        status = "✓ 成功" if success else "✗ 桶已满"
        print(f"请求 {i+1:2d}: {status} (可用空间: {bucket.available:.0f})")
    
    # 等待漏水
    print("\n等待桶处理请求...")
    time.sleep(1.0)  # 漏约2个请求
    print(f"处理后可用空间: {bucket.available:.1f}")


def example_sliding_window():
    """滑动窗口示例 - 适合需要精确限流的场景"""
    print("\n" + "="*60)
    print("=== 滑动窗口 (Sliding Window) 示例 ===")
    print("特点：精确计数，无边界突发问题")
    print("="*60)
    
    # 创建1秒内最多5个请求的窗口
    window = SlidingWindow(max_requests=5, window_seconds=1.0)
    
    print(f"\n初始状态：最大请求={window.max_requests}, 可用={window.available:.0f}")
    
    # 快速请求
    print("\n--- 快速请求 ---")
    for i in range(8):
        success = window.acquire(1)
        status = "✓ 成功" if success else "✗ 被限流"
        print(f"请求 {i+1}: {status} (剩余配额: {window.available:.0f})")
    
    # 等待窗口滑动
    print("\n等待窗口滑动...")
    time.sleep(1.1)
    print(f"窗口重置后可用: {window.available:.0f}")
    
    # 再次请求
    print("\n--- 窗口重置后请求 ---")
    for i in range(3):
        success = window.acquire(1)
        status = "✓ 成功" if success else "✗ 被限流"
        print(f"请求 {i+1}: {status} (剩余配额: {window.available:.0f})")


def example_fixed_window():
    """固定窗口示例 - 适合简单高效的限流场景"""
    print("\n" + "="*60)
    print("=== 固定窗口 (Fixed Window) 示例 ===")
    print("特点：实现简单，内存消耗低")
    print("注意：存在边界突发问题")
    print("="*60)
    
    # 创建1秒内最多5个请求的窗口
    window = FixedWindow(max_requests=5, window_seconds=1.0)
    
    print(f"\n初始状态：最大请求={window.max_requests}, 可用={window.available:.0f}")
    
    # 快速请求
    print("\n--- 快速请求 ---")
    for i in range(8):
        success = window.acquire(1)
        status = "✓ 成功" if success else "✗ 被限流"
        print(f"请求 {i+1}: {status} (剩余配额: {window.available:.0f})")
    
    # 等待新窗口
    print("\n等待新窗口...")
    time.sleep(1.1)
    print(f"新窗口可用: {window.available:.0f}")


def example_universal_rate_limiter():
    """通用速率限制器示例"""
    print("\n" + "="*60)
    print("=== 通用速率限制器 (RateLimiter) 示例 ===")
    print("="*60)
    
    algorithms = ['token_bucket', 'sliding_window', 'fixed_window', 'leaky_bucket']
    
    for algo in algorithms:
        print(f"\n--- {algo} 算法 ---")
        limiter = RateLimiter(max_requests=5, window_seconds=1.0, algorithm=algo)
        
        for i in range(7):
            success = limiter.acquire(1)
            status = "✓" if success else "✗"
            print(f"  请求 {i+1}: {status}")


def example_context_manager():
    """上下文管理器示例"""
    print("\n" + "="*60)
    print("=== 上下文管理器模式 ===")
    print("="*60)
    
    limiter = RateLimiter(3, 10.0)  # 10秒内最多3次
    
    print("\n使用 with 语句自动限流:")
    
    for i in range(4):
        try:
            with limiter:
                print(f"  执行操作 {i+1}: 成功")
        except RateLimitExceeded:
            print(f"  执行操作 {i+1}: 被限流 (配额用完)")


def example_decorator():
    """装饰器模式示例"""
    print("\n" + "="*60)
    print("=== 装饰器模式 ===")
    print("="*60)
    
    # 简单装饰器
    @rate_limit(3, 10.0)  # 10秒内最多3次
    def api_call():
        return "API 响应"
    
    print("\n使用装饰器限制函数调用频率:")
    for i in range(5):
        try:
            result = api_call()
            print(f"  调用 {i+1}: {result}")
        except RateLimitExceeded:
            print(f"  调用 {i+1}: 被限流")
    
    # 带参数装饰器
    print("\n使用带参数装饰器 (消耗2个令牌):")
    limiter = RateLimiter(6, 10.0)
    
    @limiter.decorate(tokens=2)
    def heavy_api_call():
        return "重型 API 响应"
    
    for i in range(4):
        try:
            result = heavy_api_call()
            print(f"  调用 {i+1}: {result} (剩余: {limiter.available:.0f})")
        except RateLimitExceeded:
            print(f"  调用 {i+1}: 被限流")


def example_multi_key():
    """多键限流示例 - 多租户场景"""
    print("\n" + "="*60)
    print("=== 多键速率限制器 (MultiRateLimiter) ===")
    print("适合多租户、多用户场景")
    print("="*60)
    
    # 每个用户每秒最多3次请求
    limiter = MultiRateLimiter(max_requests=3, window_seconds=1.0, algorithm='sliding_window')
    
    users = ['alice', 'bob', 'charlie']
    
    print("\n各用户独立限流:")
    for user in users:
        print(f"\n--- {user} ---")
        for i in range(5):
            success = limiter.acquire(user)
            status = "✓" if success else "✗"
            print(f"  请求 {i+1}: {status} (剩余: {limiter.available(user):.0f})")
    
    print(f"\n活跃用户: {limiter.keys()}")
    
    # 清除特定用户
    limiter.clear('alice')
    print(f"清除 alice 后: {limiter.keys()}")


def example_wait_for_acquire():
    """等待获取许可示例"""
    print("\n" + "="*60)
    print("=== wait_for_acquire 示例 ===")
    print("等待直到获取许可或超时")
    print("="*60)
    
    limiter = TokenBucket(capacity=2, refill_rate=1)
    
    # 先用完配额
    limiter.acquire(2)
    print(f"配额已用完，可用: {limiter.available:.0f}")
    
    print("\n尝试获取许可（最多等待3秒）...")
    start = time.time()
    success = limiter.wait_for_acquire(1, timeout=3.0)
    elapsed = time.time() - start
    
    if success:
        print(f"成功获取许可（等待 {elapsed:.2f} 秒）")
    else:
        print(f"获取许可超时（等待 {elapsed:.2f} 秒）")


def example_concurrent_access():
    """并发访问示例"""
    print("\n" + "="*60)
    print("=== 并发访问示例 ===")
    print("="*60)
    
    limiter = TokenBucket(capacity=20, refill_rate=5)
    results = []
    lock = threading.Lock()
    
    def worker(worker_id):
        successes = 0
        fails = 0
        for _ in range(10):
            if limiter.acquire(1):
                successes += 1
            else:
                fails += 1
            time.sleep(0.01)
        with lock:
            results.append((worker_id, successes, fails))
    
    print("\n启动4个并发线程，每个线程尝试10次请求...")
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    print("\n各线程结果:")
    total_success = 0
    total_fail = 0
    for worker_id, successes, fails in sorted(results):
        total_success += successes
        total_fail += fails
        print(f"  线程 {worker_id}: 成功={successes}, 失败={fails}")
    
    print(f"\n总计: 成功={total_success}, 失败={total_fail}")
    print(f"成功请求不超过容量: {'✓' if total_success <= 20 else '✗'}")


def example_api_rate_limiting():
    """API 限流实战示例"""
    print("\n" + "="*60)
    print("=== API 限流实战示例 ===")
    print("="*60)
    
    # 创建一个模拟 API 限流器
    # 规则：每秒最多 10 次请求，突发最大 20 次
    api_limiter = RateLimiter(
        max_requests=10,
        window_seconds=1.0,
        algorithm='token_bucket',
        capacity=20  # 允许突发到20
    )
    
    # 模拟用户请求
    def handle_request(request_id):
        if api_limiter.acquire(1):
            return f"请求 {request_id}: 处理成功"
        else:
            return f"请求 {request_id}: 429 Too Many Requests"
    
    print("\n模拟用户快速发起25个请求:")
    for i in range(25):
        print(handle_request(i + 1))
    
    print(f"\n剩余可用配额: {api_limiter.available:.1f}")


def example_choose_algorithm():
    """算法选择指南"""
    print("\n" + "="*60)
    print("=== 限流算法选择指南 ===")
    print("="*60)
    
    guide = """
    ┌─────────────────┬─────────────────────────────────────────────┐
    │ 算法            │ 适用场景                                     │
    ├─────────────────┼─────────────────────────────────────────────┤
    │ Token Bucket    │ 需要允许突发流量的API、网络流量控制         │
    │ (令牌桶)        │ 优点：平滑限流、允许突发                      │
    ├─────────────────┼─────────────────────────────────────────────┤
    │ Leaky Bucket    │ 需要严格固定输出速率的场景                  │
    │ (漏桶)          │ 优点：流量整形、强制恒定速率                  │
    ├─────────────────┼─────────────────────────────────────────────┤
    │ Sliding Window  │ 需要精确限流的API、计费系统                  │
    │ (滑动窗口)      │ 优点：精确计数、无边界突发                   │
    ├─────────────────┼─────────────────────────────────────────────┤
    │ Fixed Window    │ 简单限流需求、资源受限环境                   │
    │ (固定窗口)      │ 优点：简单高效、内存消耗低                   │
    └─────────────────┴─────────────────────────────────────────────┘
    """
    print(guide)


def main():
    """运行所有示例"""
    print("="*60)
    print("Rate Limiter Utils - 完整使用示例")
    print("="*60)
    
    example_token_bucket()
    example_leaky_bucket()
    example_sliding_window()
    example_fixed_window()
    example_universal_rate_limiter()
    example_context_manager()
    example_decorator()
    example_multi_key()
    example_wait_for_acquire()
    example_concurrent_access()
    example_api_rate_limiting()
    example_choose_algorithm()
    
    print("\n" + "="*60)
    print("所有示例运行完成！")
    print("="*60)


if __name__ == '__main__':
    main()