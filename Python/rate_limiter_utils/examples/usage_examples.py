"""
Rate Limiter Utils 使用示例

展示各种限流算法的实际应用场景：
1. API 请求限流
2. 用户操作频率控制
3. 多维度限流
4. 与装饰器配合使用
5. 限流器状态监控
"""

import time
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rate_limiter_utils.mod import (
    TokenBucket,
    LeakyBucket,
    SlidingWindow,
    FixedWindow,
    RateLimiterRegistry,
    rate_limit,
    create_token_bucket,
    create_sliding_window,
)


def example_1_basic_api_limit():
    """
    示例1：基本 API 限流
    
    场景：限制 API 每秒最多 10 次请求
    """
    print("\n" + "=" * 50)
    print("示例1：基本 API 限流（每秒10次）")
    print("=" * 50)
    
    # 创建限流器
    limiter = TokenBucket(max_requests=10, window_seconds=1.0, refill_rate=10)
    
    # 模拟请求
    print("\n模拟连续请求:")
    for i in range(15):
        result = limiter.acquire()
        status = "✓ 通过" if result.allowed else f"✗ 拒绝 (等待 {result.retry_after:.2f}s)"
        print(f"  请求 {i+1:2d}: {status} | 剩余配额: {result.remaining}")
    
    print("\n限流器状态:", limiter.get_status())


def example_2_burst_handling():
    """
    示例2：突发流量处理
    
    场景：允许一定程度的突发流量，但总体限制在 QPS
    """
    print("\n" + "=" * 50)
    print("示例2：突发流量处理")
    print("=" * 50)
    
    # 允许突发到 50，但持续 QPS 只有 20
    limiter = create_token_bucket(qps=20, burst=50)
    
    print("\n配置: 持续 QPS=20, 突发容量=50")
    print("\n模拟突发流量（连续50个请求）:")
    
    allowed = 0
    denied = 0
    for i in range(60):
        result = limiter.acquire()
        if result.allowed:
            allowed += 1
        else:
            denied += 1
    
    print(f"  结果: 通过 {allowed} 次, 拒绝 {denied} 次")
    
    # 等待令牌补充
    print("\n等待 2 秒后再次请求:")
    time.sleep(2)
    result = limiter.acquire()
    print(f"  结果: {'✓ 通过' if result.allowed else '✗ 拒绝'}")
    print(f"  当前令牌数: {limiter.get_status()['tokens']:.1f}")


def example_3_user_rate_limit():
    """
    示例3：用户级限流
    
    场景：每个用户每分钟最多 100 次请求
    """
    print("\n" + "=" * 50)
    print("示例3：用户级限流（每用户每分钟100次）")
    print("=" * 50)
    
    # 创建用户级限流器注册表
    user_limiters = RateLimiterRegistry(
        SlidingWindow,
        max_requests=100,
        window_seconds=60.0
    )
    
    # 模拟不同用户的请求
    users = ["alice", "bob", "alice", "charlie", "alice", "bob"]
    
    print("\n模拟多用户请求:")
    for user in users:
        result = user_limiters.acquire(user)
        status = "✓ 通过" if result.allowed else "✗ 拒绝"
        print(f"  用户 {user:8s}: {status}")
    
    # 查看各用户状态
    print("\n各用户限流状态:")
    for user, status in user_limiters.get_all_status().items():
        print(f"  {user:8s}: 已用 {status['current_count']}/{status['max_requests']}")


def example_4_decorator_usage():
    """
    示例4：使用装饰器限流
    
    场景：为函数添加限流保护
    """
    print("\n" + "=" * 50)
    print("示例4：装饰器限流")
    print("=" * 50)
    
    # 创建限流器
    api_limiter = TokenBucket(max_requests=3, window_seconds=1.0, refill_rate=3)
    
    # 定义被拒绝时的处理
    def on_rate_limited(result):
        return {
            "error": "rate_limit_exceeded",
            "retry_after": result.retry_after,
            "message": result.message
        }
    
    # 使用装饰器保护函数
    @rate_limit(api_limiter, on_reject=on_rate_limited)
    def send_email(to: str, subject: str):
        """模拟发送邮件"""
        return {"success": True, "to": to, "subject": subject}
    
    print("\n模拟发送邮件（限流3次/秒）:")
    for i in range(5):
        result = send_email(f"user{i}@example.com", f"Test {i}")
        if result.get("success"):
            print(f"  邮件 {i+1}: ✓ 发送成功 -> {result['to']}")
        else:
            print(f"  邮件 {i+1}: ✗ 被限流，等待 {result['retry_after']:.2f}s")


def example_5_multiple_limiters():
    """
    示例5：多级限流
    
    场景：同时限制秒级和分钟级请求
    """
    print("\n" + "=" * 50)
    print("示例5：多级限流")
    print("=" * 50)
    
    # 秒级限流
    second_limiter = SlidingWindow(max_requests=10, window_seconds=1.0)
    # 分钟级限流
    minute_limiter = SlidingWindow(max_requests=100, window_seconds=60.0)
    
    def check_rate_limit():
        """检查多级限流"""
        second_result = second_limiter.acquire()
        if not second_result:
            return second_result, "秒级限流"
        
        minute_result = minute_limiter.acquire()
        if not minute_result:
            return minute_result, "分钟级限流"
        
        return minute_result, "通过"
    
    print("\n模拟请求（秒级10次 + 分钟级100次）:")
    for i in range(12):
        result, reason = check_rate_limit()
        status = "✓ 通过" if result.allowed else f"✗ {reason}"
        print(f"  请求 {i+1:2d}: {status}")


def example_6_leaky_bucket_shaping():
    """
    示例6：漏桶流量整形
    
    场景：平滑输出，避免突发
    """
    print("\n" + "=" * 50)
    print("示例6：漏桶流量整形")
    print("=" * 50)
    
    # 每秒处理5个请求，桶容量10
    lb = LeakyBucket(max_requests=10, window_seconds=1.0, leak_rate=5)
    
    print("\n配置: 桶容量=10, 处理速率=5/秒")
    print("\n模拟突发请求（连续15个）:")
    
    results = []
    for i in range(15):
        result = lb.acquire()
        results.append(result.allowed)
        status = "✓ 入队" if result.allowed else "✗ 拒绝"
        print(f"  请求 {i+1:2d}: {status} | 队列长度: {lb.get_status()['queue_size']}")
    
    print(f"\n统计: 入队 {sum(results)} 次, 拒绝 {len(results) - sum(results)} 次")
    
    # 等待处理
    print("\n等待 1 秒让队列处理...")
    time.sleep(1)
    print(f"处理后队列长度: {lb.get_status()['queue_size']}")


def example_7_fixed_window():
    """
    示例7：固定窗口限流
    
    场景：简单高效的限流，适合一般场景
    """
    print("\n" + "=" * 50)
    print("示例7：固定窗口限流")
    print("=" * 50)
    
    # 自然对齐的固定窗口
    fw = FixedWindow(max_requests=5, window_seconds=1.0, window_alignment="natural")
    
    print("\n配置: 每秒5次，自然时间对齐")
    print("\n模拟请求:")
    
    for i in range(7):
        result = fw.acquire()
        status = fw.get_status()
        msg = f"✓ 通过" if result.allowed else "✗ 拒绝"
        print(f"  请求 {i+1}: {msg} | 窗口已用: {status['current_count']}/{status['max_requests']}")


def example_8_ip_rate_limit():
    """
    示例8：IP 级别限流
    
    场景：防止 DDoS 攻击
    """
    print("\n" + "=" * 50)
    print("示例8：IP 级别限流")
    print("=" * 50)
    
    # 每个IP每秒最多20次请求
    ip_limiters = RateLimiterRegistry(
        TokenBucket,
        max_requests=20,
        window_seconds=1.0,
        refill_rate=20
    )
    
    # 模拟不同IP的请求
    requests = [
        ("192.168.1.1", 15),  # 正常用户
        ("10.0.0.1", 25),     # 异常请求
        ("192.168.1.1", 5),   # 同一用户继续
        ("10.0.0.2", 10),     # 另一个正常用户
    ]
    
    print("\n模拟不同IP的请求:")
    for ip, count in requests:
        print(f"\nIP {ip} 请求 {count} 次:")
        allowed = 0
        for _ in range(count):
            result = ip_limiters.acquire(ip)
            if result.allowed:
                allowed += 1
        print(f"  通过: {allowed}, 拒绝: {count - allowed}")
    
    # 显示统计
    print("\nIP限流统计:")
    stats = ip_limiters.get_stats()
    print(f"  活跃IP数: {stats['limiter_count']}")
    for ip, status in ip_limiters.get_all_status().items():
        print(f"  {ip}: 剩余令牌 {status['tokens']:.0f}/{status['capacity']}")


def example_9_resource_protection():
    """
    示例9：资源访问保护
    
    场景：保护数据库或外部API
    """
    print("\n" + "=" * 50)
    print("示例9：资源访问保护")
    print("=" * 50)
    
    # 数据库限流器
    db_limiter = SlidingWindow(max_requests=50, window_seconds=1.0)
    # API限流器
    api_limiter = TokenBucket(max_requests=100, window_seconds=1.0, refill_rate=100)
    
    def query_database(query: str):
        """模拟数据库查询"""
        result = db_limiter.acquire()
        if not result.allowed:
            return {"error": "数据库限流", "retry_after": result.retry_after}
        return {"result": f"查询结果: {query}"}
    
    def call_external_api(endpoint: str):
        """模拟外部API调用"""
        result = api_limiter.acquire()
        if not result.allowed:
            return {"error": "API限流", "retry_after": result.retry_after}
        return {"data": f"API响应: {endpoint}"}
    
    print("\n模拟数据库查询（50次/秒）:")
    for i in range(55):
        result = query_database(f"SELECT * FROM users WHERE id = {i}")
        if i < 5 or i >= 50:
            status = "✓" if "result" in result else "✗"
            print(f"  查询 {i+1}: {status}")
        elif i == 50:
            print("  ... (省略中间结果)")
    
    print("\n数据库限流器状态:", db_limiter.get_status())
    print("\nAPI限流器状态:", api_limiter.get_status())


def example_10_monitoring():
    """
    示例10：限流器状态监控
    
    场景：实时监控限流状态
    """
    print("\n" + "=" * 50)
    print("示例10：限流器状态监控")
    print("=" * 50)
    
    limiter = TokenBucket(max_requests=100, window_seconds=1.0, refill_rate=50)
    
    print("\n初始状态:")
    print(f"  {limiter.get_status()}")
    
    # 消耗一些令牌
    print("\n消耗30个令牌...")
    for _ in range(30):
        limiter.acquire()
    
    status = limiter.get_status()
    print(f"\n消耗后状态:")
    print(f"  类型: {status['type']}")
    print(f"  容量: {status['capacity']}")
    print(f"  剩余令牌: {status['tokens']:.1f}")
    print(f"  使用率: {status['utilization']*100:.1f}%")
    print(f"  补充速率: {status['refill_rate']}/秒")
    
    # 等待补充
    print("\n等待 0.5 秒...")
    time.sleep(0.5)
    
    status = limiter.get_status()
    print(f"\n等待后状态:")
    print(f"  剩余令牌: {status['tokens']:.1f}")
    print(f"  使用率: {status['utilization']*100:.1f}%")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("       Rate Limiter Utils 使用示例")
    print("=" * 60)
    
    examples = [
        example_1_basic_api_limit,
        example_2_burst_handling,
        example_3_user_rate_limit,
        example_4_decorator_usage,
        example_5_multiple_limiters,
        example_6_leaky_bucket_shaping,
        example_7_fixed_window,
        example_8_ip_rate_limit,
        example_9_resource_protection,
        example_10_monitoring,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n示例执行错误: {e}")
    
    print("\n" + "=" * 60)
    print("所有示例执行完成")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()