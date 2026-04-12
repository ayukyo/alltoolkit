"""
AllToolkit - Rate Limit Utils 使用示例

演示各种限流场景的实际用法。
"""

import time
import sys
sys.path.insert(0, '..')
from mod import (
    TokenBucket,
    SlidingWindowCounter,
    SlidingWindowLog,
    FixedWindowCounter,
    RateLimiter,
    rate_limit,
    rate_limit_strict,
    RateLimitExceeded,
    rate_limit_context,
)


def example_token_bucket():
    """Token Bucket 基础示例"""
    print("\n" + "="*60)
    print("示例 1: Token Bucket 基础用法")
    print("="*60)
    
    # 创建限流器：容量 10，每秒补充 2 个令牌
    bucket = TokenBucket(capacity=10, refill_rate=2.0)
    
    print(f"初始令牌数：{bucket.tokens:.1f}")
    print(f"桶容量：{bucket.capacity}")
    print(f"补充速率：{bucket.refill_rate} 个/秒")
    
    # 消费令牌
    print("\n消费令牌:")
    for i in range(12):
        if bucket.consume():
            print(f"  请求 {i+1}: ✅ 允许 (剩余：{bucket.tokens:.1f})")
        else:
            print(f"  请求 {i+1}: ❌ 限流")
    
    # 等待补充
    print("\n等待 2 秒让令牌补充...")
    time.sleep(2)
    print(f"当前令牌数：{bucket.tokens:.1f}")
    
    # 检查状态
    result = bucket.check()
    print(f"\n状态检查:")
    print(f"  允许：{result.allowed}")
    print(f"  剩余：{result.remaining}")
    print(f"  重置时间：{time.strftime('%H:%M:%S', time.localtime(result.reset_at))}")


def example_sliding_window():
    """滑动窗口示例"""
    print("\n" + "="*60)
    print("示例 2: 滑动窗口限流")
    print("="*60)
    
    # 每 5 秒最多 3 个请求
    limiter = SlidingWindowCounter(max_requests=3, window_seconds=5.0)
    
    print("限制：每 5 秒最多 3 个请求\n")
    
    # 发送请求
    for i in range(5):
        if limiter.allow():
            print(f"请求 {i+1}: ✅ 允许")
        else:
            result = limiter.check()
            print(f"请求 {i+1}: ❌ 限流 (剩余：{result.remaining}, 重试：{result.retry_after:.1f}秒)")
    
    # 等待窗口过期
    print("\n等待 5 秒...")
    time.sleep(5)
    
    # 再次尝试
    if limiter.allow():
        print("新请求：✅ 允许（窗口已重置）")


def example_multi_key():
    """多 Key 限流示例"""
    print("\n" + "="*60)
    print("示例 3: 多用户限流")
    print("="*60)
    
    # 每个用户独立限流
    limiter = RateLimiter(
        strategy='token_bucket',
        capacity=5,
        refill_rate=1.0,
    )
    
    users = ['alice', 'bob', 'charlie']
    
    print("每个用户限制：5 个令牌，每秒补充 1 个\n")
    
    # 模拟多个用户的请求
    for user in users:
        print(f"\n用户 {user} 的请求:")
        for i in range(7):
            if limiter.allow(user):
                print(f"  请求 {i+1}: ✅")
            else:
                result = limiter.check(user)
                print(f"  请求 {i+1}: ❌ (等待 {result.retry_after:.1f}秒)")


def example_decorator():
    """装饰器示例"""
    print("\n" + "="*60)
    print("示例 4: 装饰器限流")
    print("="*60)
    
    # 基础装饰器
    @rate_limit(max_requests=3, window_seconds=10)
    def api_call():
        return "API 响应"
    
    print("限制：每 10 秒最多 3 次调用\n")
    
    for i in range(5):
        result = api_call()
        if result:
            print(f"调用 {i+1}: ✅ {result}")
        else:
            print(f"调用 {i+1}: ❌ 限流")
    
    # 带自定义 Key 的装饰器
    @rate_limit(
        max_requests=2,
        window_seconds=10,
        key_func=lambda user_id, **kwargs: user_id
    )
    def user_action(user_id: str):
        return f"用户 {user_id} 的操作成功"
    
    print("\n按用户限流（每用户 2 次/10 秒）:\n")
    
    for user in ['user_a', 'user_b', 'user_a']:
        for i in range(3):
            result = user_action(user)
            status = "✅" if result else "❌"
            print(f"  {user} 请求 {i+1}: {status}")


def example_strict_decorator():
    """严格装饰器示例"""
    print("\n" + "="*60)
    print("示例 5: 严格限流（抛出异常）")
    print("="*60)
    
    @rate_limit_strict(max_requests=3, window_seconds=10)
    def critical_operation():
        return "操作成功"
    
    print("限制：每 10 秒最多 3 次，超限抛出异常\n")
    
    for i in range(5):
        try:
            result = critical_operation()
            print(f"操作 {i+1}: ✅ {result}")
        except RateLimitExceeded as e:
            print(f"操作 {i+1}: ❌ 限流 (等待 {e.retry_after:.1f}秒)")


def example_context_manager():
    """上下文管理器示例"""
    print("\n" + "="*60)
    print("示例 6: 上下文管理器")
    print("="*60)
    
    limiter = RateLimiter(strategy='token_bucket', capacity=3, refill_rate=0.0)
    
    print("限制：3 次请求（不补充）\n")
    
    for i in range(5):
        with rate_limit_context(limiter, 'default', on_limit=lambda: None):
            print(f"请求 {i+1}: ✅ 执行中...")
            # 这里可以放置需要限流的代码


def example_api_rate_limiting():
    """API 限流完整示例"""
    print("\n" + "="*60)
    print("示例 7: API 限流完整场景")
    print("="*60)
    
    # 模拟 API 限流
    api_limiter = RateLimiter(
        strategy='sliding_window',
        max_requests=10,
        window_seconds=60,
    )
    
    def mock_api_endpoint(client_id: str):
        """模拟 API 端点"""
        result = api_limiter.check(client_id)
        
        if not result.allowed:
            return {
                'status': 429,
                'error': 'Rate Limited',
                'retry_after': result.retry_after,
                'limit': result.limit,
                'remaining': result.remaining,
            }
        
        api_limiter.allow(client_id)
        
        return {
            'status': 200,
            'data': 'API response data',
            'limit': result.limit,
            'remaining': result.remaining - 1,
        }
    
    # 模拟多个客户端请求
    clients = ['client_a', 'client_b']
    
    for client in clients:
        print(f"\n客户端 {client}:")
        for i in range(12):
            response = mock_api_endpoint(client)
            if response['status'] == 200:
                print(f"  请求 {i+1}: ✅ (剩余：{response['remaining']})")
            else:
                print(f"  请求 {i+1}: ❌ 429 (等待：{response['retry_after']:.1f}秒)")


def example_crawler():
    """爬虫限流示例"""
    print("\n" + "="*60)
    print("示例 8: 网络爬虫限流")
    print("="*60)
    
    # 爬虫限流：每秒最多 1 个请求
    crawler_limiter = SlidingWindowLog(max_requests=1, window_seconds=1.0)
    
    urls = [
        'https://example.com/page1',
        'https://example.com/page2',
        'https://example.com/page3',
        'https://example.com/page4',
        'https://example.com/page5',
    ]
    
    print("限制：每秒最多 1 个请求\n")
    
    for i, url in enumerate(urls):
        # 等待限流允许
        while not crawler_limiter.allow():
            time.sleep(0.1)
        
        print(f"请求 {i+1}: 抓取 {url}")
        # 模拟抓取时间
        time.sleep(0.3)


def example_burst_handling():
    """突发流量处理示例"""
    print("\n" + "="*60)
    print("示例 9: 突发流量处理（Token Bucket）")
    print("="*60)
    
    # Token Bucket 允许一定程度的突发
    bucket = TokenBucket(capacity=10, refill_rate=1.0)
    
    print("配置：容量 10，补充速率 1/秒")
    print("特点：允许突发，但长期平均速率受限\n")
    
    # 模拟突发请求
    print("突发请求（10 个连续请求）:")
    for i in range(10):
        if bucket.consume():
            print(f"  请求 {i+1}: ✅")
        else:
            print(f"  请求 {i+1}: ❌")
    
    print(f"\n当前令牌：{bucket.tokens:.1f}")
    print("等待 5 秒补充令牌...")
    time.sleep(5)
    print(f"补充后令牌：{bucket.tokens:.1f}")


def example_comparison():
    """不同策略对比"""
    print("\n" + "="*60)
    print("示例 10: 不同限流策略对比")
    print("="*60)
    
    strategies = {
        'Token Bucket': TokenBucket(capacity=5, refill_rate=1.0),
        'Sliding Window': SlidingWindowCounter(max_requests=5, window_seconds=5.0),
        'Fixed Window': FixedWindowCounter(max_requests=5, window_seconds=5.0),
    }
    
    print("配置：5 个请求/5 秒窗口\n")
    
    for name, limiter in strategies.items():
        print(f"{name}:")
        
        allowed = 0
        for i in range(7):
            if hasattr(limiter, 'consume'):
                result = limiter.consume()
            else:
                result = limiter.allow()
            
            if result:
                allowed += 1
        
        print(f"  允许 {allowed}/7 个请求")
        
        # 等待窗口过期
        time.sleep(5.5)


def main():
    """运行所有示例"""
    print("\n" + "🚦"*30)
    print("AllToolkit Rate Limit Utils - 使用示例")
    print("🚦"*30)
    
    example_token_bucket()
    example_sliding_window()
    example_multi_key()
    example_decorator()
    example_strict_decorator()
    example_context_manager()
    example_api_rate_limiting()
    example_crawler()
    example_burst_handling()
    example_comparison()
    
    print("\n" + "="*60)
    print("所有示例运行完成！")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
