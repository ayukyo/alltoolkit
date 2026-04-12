#!/usr/bin/env python3
"""
Webhook Utils - Basic Usage Examples

演示 webhook_utils 模块的基本用法。
"""

import sys
import os

# 导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    WebhookSender,
    WebhookConfig,
    WebhookEvent,
    WebhookSigner,
    WebhookManager,
    RetryStrategy,
    send_webhook,
)


def example_basic_send():
    """基础发送示例"""
    print("=" * 60)
    print("示例 1: 基础 Webhook 发送")
    print("=" * 60)
    
    # 创建发送器
    sender = WebhookSender()
    
    # 配置 Webhook
    config = WebhookConfig(
        url="https://httpbin.org/post",  # 测试端点
        timeout=10.0,
        max_retries=1,
    )
    
    # 创建事件
    event = WebhookEvent(
        event_type="user.created",
        payload={
            "user_id": 12345,
            "email": "test@example.com",
            "name": "Test User",
        },
    )
    
    print(f"发送事件：{event.event_type}")
    print(f"Payload: {event.payload}")
    print(f"事件 ID: {event.id}")
    
    # 发送
    result = sender.send(event, config)
    
    print(f"\n结果:")
    print(f"  成功：{result.success}")
    print(f"  状态码：{result.status_code}")
    print(f"  尝试次数：{result.attempts}")
    print(f"  耗时：{result.duration_ms:.2f}ms")
    
    return result


def example_signed_webhook():
    """带签名的 Webhook 示例"""
    print("\n" + "=" * 60)
    print("示例 2: 带 HMAC 签名的 Webhook")
    print("=" * 60)
    
    secret = "my-super-secret-key-12345"
    
    # 创建签名器
    signer = WebhookSigner(secret, "sha256")
    
    # 签名 payload
    payload = {"event": "payment.completed", "amount": 99.99}
    signature = signer.sign(payload)
    
    print(f"Payload: {payload}")
    print(f"签名：{signature[:32]}...")
    
    # 验证签名
    is_valid = signer.verify(payload, signature)
    print(f"验证结果：{'✓ 有效' if is_valid else '✗ 无效'}")
    
    # 验证篡改的 payload
    tampered = {"event": "payment.completed", "amount": 999.99}
    is_valid_tampered = signer.verify(tampered, signature)
    print(f"篡改后验证：{'✓ 有效' if is_valid_tampered else '✗ 无效 (预期)'}")
    
    # 获取签名头
    headers = signer.get_signature_header(payload)
    print(f"\n签名头：{headers}")
    
    # 发送带签名的 webhook
    config = WebhookConfig(
        url="https://httpbin.org/post",
        secret=secret,
        timeout=10.0,
    )
    
    event = WebhookEvent(event_type="payment.completed", payload=payload)
    sender = WebhookSender()
    result = sender.send(event, config)
    
    print(f"\n发送结果：{'✓ 成功' if result.success else '✗ 失败'}")
    
    return result


def example_retry_strategies():
    """重试策略示例"""
    print("\n" + "=" * 60)
    print("示例 3: 重试策略")
    print("=" * 60)
    
    strategies = [
        (RetryStrategy.NONE, "无重试"),
        (RetryStrategy.FIXED, "固定延迟"),
        (RetryStrategy.LINEAR, "线性退避"),
        (RetryStrategy.EXPONENTIAL, "指数退避"),
    ]
    
    for strategy, name in strategies:
        print(f"\n策略：{name}")
        
        config = WebhookConfig(
            url="https://httpbin.org/status/500",  # 故意返回 500
            max_retries=2,
            retry_strategy=strategy,
            retry_delay=0.1,  # 缩短延迟以便快速测试
            timeout=5.0,
        )
        
        event = WebhookEvent(event_type="test.retry", payload={"strategy": strategy.value})
        sender = WebhookSender()
        result = sender.send(event, config)
        
        print(f"  最终状态：{'成功' if result.success else '失败'}")
        print(f"  尝试次数：{result.attempts}")
        print(f"  总耗时：{result.duration_ms:.2f}ms")


def example_webhook_manager():
    """多端点管理示例"""
    print("\n" + "=" * 60)
    print("示例 4: 多端点管理")
    print("=" * 60)
    
    manager = WebhookManager()
    
    # 注册多个端点
    manager.register("httpbin", WebhookConfig(
        url="https://httpbin.org/post",
        timeout=10.0,
    ))
    
    manager.register("httpbin_status", WebhookConfig(
        url="https://httpbin.org/status/201",
        timeout=10.0,
    ))
    
    print(f"已注册端点：{manager.list_endpoints()}")
    
    # 发送到特定端点
    event = WebhookEvent(
        event_type="system.alert",
        payload={"message": "Test alert", "severity": "info"},
    )
    
    print(f"\n发送到 'httpbin' 端点...")
    result = manager.send("httpbin", event)
    print(f"  结果：{'✓ 成功' if result.success else '✗ 失败'} (状态码：{result.status_code})")
    
    # 广播到所有端点
    print(f"\n广播到所有端点...")
    broadcast_event = WebhookEvent(
        event_type="broadcast.test",
        payload={"test": True},
    )
    
    results = manager.broadcast(broadcast_event)
    
    for name, result in results.items():
        status = "✓" if result.success else "✗"
        print(f"  {status} {name}: 状态码 {result.status_code}")


def example_convenience_functions():
    """便捷函数示例"""
    print("\n" + "=" * 60)
    print("示例 5: 便捷函数")
    print("=" * 60)
    
    # 使用 send_webhook 便捷函数
    print("使用 send_webhook() 发送...")
    
    result = send_webhook(
        url="https://httpbin.org/post",
        event_type="quick.test",
        payload={"quick": True, "test": "data"},
        timeout=10.0,
        max_retries=0,
    )
    
    print(f"结果：{'✓ 成功' if result.success else '✗ 失败'}")
    print(f"状态码：{result.status_code}")
    print(f"耗时：{result.duration_ms:.2f}ms")


def example_async_send():
    """异步发送示例"""
    print("\n" + "=" * 60)
    print("示例 6: 异步发送")
    print("=" * 60)
    
    from mod import AsyncWebhookSender
    
    sender = AsyncWebhookSender(max_workers=5)
    
    config = WebhookConfig(
        url="https://httpbin.org/post",
        timeout=10.0,
    )
    
    # 创建多个事件
    events = [
        WebhookEvent(event_type=f"async.test.{i}", payload={"index": i})
        for i in range(5)
    ]
    
    print("发送 5 个异步请求...")
    
    futures = []
    for event in events:
        future = sender.send_async(event, config)
        futures.append(future)
    
    # 等待所有完成
    print("等待结果...")
    for i, future in enumerate(futures):
        result = future.result(timeout=30)
        status = "✓" if result.success else "✗"
        print(f"  {status} 事件 {i}: 状态码 {result.status_code}")


def example_logging():
    """日志记录示例"""
    print("\n" + "=" * 60)
    print("示例 7: 日志与统计")
    print("=" * 60)
    
    from mod import WebhookLogger
    
    logger = WebhookLogger(max_events=100)
    sender = WebhookSender(logger=logger)
    
    config = WebhookConfig(
        url="https://httpbin.org/post",
        timeout=10.0,
    )
    
    # 发送一些事件
    print("发送 5 个事件...")
    for i in range(5):
        event = WebhookEvent(event_type="log.test", payload={"index": i})
        result = sender.send(event, config)
        print(f"  事件 {i}: {'✓' if result.success else '✗'}")
    
    # 获取统计
    stats = sender.get_stats()
    print(f"\n统计信息:")
    print(f"  总发送：{stats['total_sent']}")
    print(f"  成功：{stats['total_success']}")
    print(f"  失败：{stats['total_failed']}")
    print(f"  成功率：{stats['success_rate']:.1%}")
    print(f"  总重试：{stats['total_retries']}")
    
    # 获取最近事件
    print(f"\n最近事件:")
    recent = sender.get_recent_events(limit=3)
    for event in recent:
        print(f"  - {event['type']}: {event.get('status_code', 'N/A')}")


def main():
    """运行所有示例"""
    print("\n" + "🎣" * 30)
    print("Webhook Utils 使用示例")
    print("🎣" * 30 + "\n")
    
    try:
        example_basic_send()
        example_signed_webhook()
        example_retry_strategies()
        example_webhook_manager()
        example_convenience_functions()
        example_async_send()
        example_logging()
        
        print("\n" + "=" * 60)
        print("所有示例运行完成！")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"\n❌ 示例运行出错：{e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
