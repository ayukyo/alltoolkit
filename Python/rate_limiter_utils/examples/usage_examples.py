"""
rate_limiter_utils 使用示例

演示四种速率限制算法的实际应用场景。
"""

import time
import sys
sys.path.insert(0, '..')

from mod import (
    FixedWindowRateLimiter,
    SlidingWindowRateLimiter,
    TokenBucketRateLimiter,
    LeakyBucketRateLimiter,
    RateLimiterRegistry,
    rate_limit,
    create_limiter,
    RateLimitExceeded,
)


def example_fixed_window():
    """
    固定窗口算法示例
    
    场景：API 请求限制 - 每分钟最多 10 次请求
    特点：实现简单，但存在边界突发问题
    """
    print("=" * 60)
    print("固定窗口算法 - API 请求限制")
    print("=" * 60)
    
    # 每分钟最多 10 次请求
    limiter = FixedWindowRateLimiter(max_requests=10, window_seconds=60)
    
    print(f"\n配置: 每分钟最多 10 次请求")
    print("\n模拟连续请求:")
    
    for i in range(12):
        result = limiter.try_acquire()
        status = "✓ 允许" if result.allowed else "✗ 拒绝"
        print(f"  请求 {i+1:2d}: {status} | 剩余配额: {result.remaining:2d} | "
              f"重置时间: {result.reset_time - time.time():.1f}秒后")
        if not result.allowed:
            print(f"           → 需等待 {result.retry_after:.1f} 秒后重试")
    
    print("\n获取当前状态:")
    state = limiter.get_state()
    for key, value in state.items():
        print(f"  {key}: {value}")


def example_sliding_window():
    """
    滑动窗口算法示例
    
    场景：精确控制 - 防止边界突发
    特点：精确控制，无边界突发问题
    """
    print("\n" + "=" * 60)
    print("滑动窗口算法 - 精确速率控制")
    print("=" * 60)
    
    # 每 5 秒最多 3 次请求
    limiter = SlidingWindowRateLimiter(max_requests=3, window_seconds=5)
    
    print(f"\n配置: 每 5 秒最多 3 次请求")
    print("\n演示滑动窗口:")
    
    # 快速发送 3 次请求
    print("\n快速发送 3 次请求:")
    for i in range(3):
        result = limiter.try_acquire()
        print(f"  请求 {i+1}: {'✓ 允许' if result.allowed else '✗ 拒绝'}")
    
    # 立即再发，应该被拒绝
    print("\n立即发送第 4 次请求:")
    result = limiter.try_acquire()
    print(f"  请求 4: {'✓ 允许' if result.allowed else '✗ 拒绝'}")
    
    # 等待一段时间
    print("\n等待 2 秒后发送...")
    time.sleep(2)
    result = limiter.try_acquire()
    print(f"  请求 5: {'✓ 允许' if result.allowed else '✗ 拒绝'}")
    print("  (第一个请求仍在窗口内，所以仍被拒绝)")
    
    # 再等待
    print("\n再等待 3 秒后发送...")
    time.sleep(3)
    result = limiter.try_acquire()
    print(f"  请求 6: {'✓ 允许' if result.allowed else '✗ 拒绝'}")
    print("  (第一个请求已滑出窗口，有新配额)")
    
    print("\n当前窗口内的请求时间戳:")
    state = limiter.get_state()
    if state['oldest_request']:
        print(f"  最早: {state['oldest_request']}")
        print(f"  最新: {state['newest_request']}")


def example_token_bucket():
    """
    令牌桶算法示例
    
    场景：允许突发流量
    特点：支持流量突发，平滑限流
    """
    print("\n" + "=" * 60)
    print("令牌桶算法 - 突发流量处理")
    print("=" * 60)
    
    # 容量 10，每 2 秒填满（每秒补充 5 个令牌）
    limiter = TokenBucketRateLimiter(max_requests=10, window_seconds=2)
    
    print(f"\n配置: 桶容量 10，每 2 秒填满（每秒补充 5 个令牌）")
    print("\n模拟突发流量:")
    
    # 突发请求
    print("\n突发发送 12 个请求:")
    for i in range(12):
        result = limiter.try_acquire()
        status = "✓ 允许" if result.allowed else "✗ 拒绝"
        state = limiter.get_state()
        print(f"  请求 {i+1:2d}: {status} | 剩余令牌: {state['tokens']:.1f}")
    
    # 等待令牌补充
    print("\n等待 0.5 秒（应补充约 2.5 个令牌）...")
    time.sleep(0.5)
    state = limiter.get_state()
    print(f"  当前令牌数: {state['tokens']:.2f}")
    
    print("\n继续发送请求:")
    for i in range(3):
        result = limiter.try_acquire()
        state = limiter.get_state()
        status = "✓ 允许" if result.allowed else "✗ 拒绝"
        print(f"  请求 {i+1}: {status} | 剩余令牌: {state['tokens']:.1f}")


def example_leaky_bucket():
    """
    漏桶算法示例
    
    场景：恒定流出速率
    特点：严格限制流出速率，无突发
    """
    print("\n" + "=" * 60)
    print("漏桶算法 - 恒定速率处理")
    print("=" * 60)
    
    # 容量 5，每秒漏出 2 个（即每秒最多处理 2 个请求）
    limiter = LeakyBucketRateLimiter(capacity=5, leak_rate=2)
    
    print(f"\n配置: 桶容量 5，每秒处理 2 个请求")
    print("\n模拟请求队列:")
    
    # 快速填充
    print("\n快速发送 6 个请求:")
    for i in range(6):
        result = limiter.try_acquire()
        status = "✓ 允许" if result.allowed else "✗ 拒绝"
        state = limiter.get_state()
        print(f"  请求 {i+1}: {status} | 桶中水量: {state['water']:.1f}")
    
    # 等待漏出
    print("\n等待 1 秒（应漏出 2 个）...")
    time.sleep(1)
    state = limiter.get_state()
    print(f"  当前水量: {state['water']:.1f}")
    
    print("\n继续发送请求:")
    for i in range(3):
        result = limiter.try_acquire()
        state = limiter.get_state()
        status = "✓ 允许" if result.allowed else "✗ 拒绝"
        print(f"  请求 {i+1}: {status} | 桶中水量: {state['water']:.1f}")


def example_multi_user():
    """
    多用户限制示例
    
    场景：API 网关为不同用户独立限流
    """
    print("\n" + "=" * 60)
    print("多用户限流 - API 网关场景")
    print("=" * 60)
    
    # 每个用户每分钟最多 5 次请求
    registry = RateLimiterRegistry(
        SlidingWindowRateLimiter,
        max_requests=5,
        window_seconds=60
    )
    
    print(f"\n配置: 每用户每分钟最多 5 次请求")
    
    users = ['user_alice', 'user_bob', 'user_charlie']
    
    print("\n模拟多用户请求:")
    for user in users:
        print(f"\n{user}:")
        for i in range(4):
            result = registry.try_acquire(user)
            status = "✓" if result.allowed else "✗"
            print(f"  请求 {i+1}: {status}")
    
    print("\n\nAlice 继续请求（将达到限制）:")
    for i in range(3):
        result = registry.try_acquire('user_alice')
        status = "✓" if result.allowed else "✗ 已达限制"
        print(f"  请求 {i+1}: {status}")


def example_decorator():
    """
    装饰器使用示例
    
    场景：为函数添加速率限制
    """
    print("\n" + "=" * 60)
    print("装饰器模式 - 函数限流")
    print("=" * 60)
    
    # 创建限制器
    limiter = create_limiter('token_bucket', max_requests=3, window_seconds=10)
    
    # 定义拒绝时的回调
    def on_rate_limit_exceeded(result):
        return {
            'error': 'rate_limit_exceeded',
            'retry_after': f"{result.retry_after:.2f}s",
            'message': '请求过于频繁，请稍后重试'
        }
    
    # 使用装饰器
    @rate_limit(limiter, on_reject=on_rate_limit_exceeded)
    def api_endpoint(user_id: int):
        """模拟 API 端点"""
        return {
            'success': True,
            'data': f'用户 {user_id} 的数据'
        }
    
    print(f"\n配置: 每次最多 3 个请求")
    print("\n调用 API:")
    
    for i in range(5):
        result = api_endpoint(user_id=123)
        print(f"  调用 {i+1}: {result}")


def example_api_middleware():
    """
    API 中间件示例
    
    场景：Web 框架中间件集成
    """
    print("\n" + "=" * 60)
    print("Web API 中间件模式")
    print("=" * 60)
    
    # 创建多用户限流器
    limiter_registry = RateLimiterRegistry(
        TokenBucketRateLimiter,
        max_requests=100,
        window_seconds=60  # 每分钟 100 次
    )
    
    def get_client_ip(request):
        """模拟获取客户端 IP"""
        return request.get('ip', '127.0.0.1')
    
    def rate_limit_middleware(request, next_handler):
        """速率限制中间件"""
        client_ip = get_client_ip(request)
        result = limiter_registry.try_acquire(client_ip)
        
        # 添加速率限制头
        headers = {
            'X-RateLimit-Limit': '100',
            'X-RateLimit-Remaining': str(result.remaining),
            'X-RateLimit-Reset': str(int(result.reset_time))
        }
        
        if not result.allowed:
            return {
                'status': 429,
                'body': {'error': 'Too Many Requests', 'retry_after': result.retry_after},
                'headers': {**headers, 'Retry-After': str(int(result.retry_after))}
            }
        
        # 继续处理请求
        response = next_handler(request)
        response['headers'] = {**response.get('headers', {}), **headers}
        return response
    
    def api_handler(request):
        """实际的处理函数"""
        return {
            'status': 200,
            'body': {'message': 'Success', 'data': request.get('data')}
        }
    
    print("\n模拟多个请求:")
    
    # 模拟 5 个请求
    for i in range(5):
        request = {'ip': f'192.168.1.{i % 2}', 'data': f'request_{i}'}
        response = rate_limit_middleware(request, api_handler)
        print(f"\n请求 {i+1} (IP: {request['ip']}):")
        print(f"  状态码: {response['status']}")
        print(f"  响应体: {response['body']}")
        if 'X-RateLimit-Remaining' in response.get('headers', {}):
            print(f"  剩余配额: {response['headers']['X-RateLimit-Remaining']}")


def example_comparison():
    """
    算法对比示例
    
    展示四种算法在相同配置下的行为差异
    """
    print("\n" + "=" * 60)
    print("四种算法对比")
    print("=" * 60)
    
    configs = {
        '固定窗口': FixedWindowRateLimiter(5, 10),
        '滑动窗口': SlidingWindowRateLimiter(5, 10),
        '令牌桶': TokenBucketRateLimiter(5, 10),
        '漏桶': LeakyBucketRateLimiter(5, 0.5),  # 每秒漏 0.5 个
    }
    
    print("\n配置: 时间窗口 10 秒，最大请求 5 次")
    print("\n连续发送 7 次请求的结果:")
    
    for name, limiter in configs.items():
        print(f"\n{name}:")
        for i in range(7):
            result = limiter.try_acquire()
            status = "✓" if result.allowed else "✗"
            print(f"  请求 {i+1}: {status}")


def main():
    """运行所有示例"""
    example_fixed_window()
    example_sliding_window()
    example_token_bucket()
    example_leaky_bucket()
    example_multi_user()
    example_decorator()
    example_api_middleware()
    example_comparison()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()