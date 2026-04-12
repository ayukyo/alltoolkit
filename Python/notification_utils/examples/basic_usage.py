#!/usr/bin/env python3
"""
AllToolkit - Notification Utils - Basic Usage Examples

演示 notification_utils 模块的基础用法。
"""

import sys
import os
# Add parent directory to path for importing mod
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    notify, notify_desktop, notify_webhook,
    notify_slack, notify_discord,
    Notification, Priority, NotificationUtils
)


def example_basic_notify():
    """基础通知示例"""
    print("\n" + "=" * 60)
    print("示例 1: 基础通知")
    print("=" * 60)
    
    # 普通通知
    notify("欢迎", "欢迎使用 AllToolkit 通知模块！")
    
    # 不同优先级的通知
    notify("调试", "这是一条调试信息", priority=Priority.LOW)
    notify("信息", "这是一条普通信息", priority=Priority.NORMAL)
    notify("警告", "这是一条警告信息", priority=Priority.HIGH)
    notify("紧急", "这是一条紧急通知", priority=Priority.URGENT)
    notify("严重", "这是一条严重警报", priority=Priority.CRITICAL)


def example_desktop_notify():
    """桌面通知示例"""
    print("\n" + "=" * 60)
    print("示例 2: 桌面通知")
    print("=" * 60)
    
    # 发送桌面通知
    success = notify_desktop("任务完成", "您的任务已成功完成！")
    print(f"桌面通知发送：{'成功' if success else '失败'}")
    
    # 高优先级桌面通知
    success = notify_desktop("系统警报", "检测到异常活动！", priority=Priority.HIGH)
    print(f"高优先级桌面通知：{'成功' if success else '失败'}")


def example_webhook_notify():
    """Webhook 通知示例"""
    print("\n" + "=" * 60)
    print("示例 3: Webhook 通知")
    print("=" * 60)
    
    # 注意：以下 URL 是示例，实际使用请替换为真实 Webhook
    webhook_url = "https://httpbin.org/post"  # 测试端点
    
    # 通用 Webhook
    success = notify_webhook(
        url=webhook_url,
        title="系统通知",
        message="这是一个测试通知",
        priority=Priority.NORMAL
    )
    print(f"通用 Webhook: {'成功' if success else '失败'}")
    
    # Slack Webhook (需要真实 URL)
    # success = notify_slack(
    #     url="https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
    #     message="🚀 新版本已部署",
    #     channel="#general"
    # )
    
    # Discord Webhook (需要真实 URL)
    # success = notify_discord(
    #     url="https://discord.com/api/webhooks/YOUR/WEBHOOK",
    #     title="构建成功",
    #     message="CI/CD 流水线完成",
    #     priority=Priority.NORMAL
    # )


def example_email_notify():
    """邮件通知示例"""
    print("\n" + "=" * 60)
    print("示例 4: 邮件通知")
    print("=" * 60)
    
    # 创建邮件通知器
    # 注意：以下是示例配置，实际使用请替换为真实 SMTP 信息
    print("""
# 邮件通知配置示例：
emailer = NotificationUtils.create_email_notifier(
    smtp_host="smtp.gmail.com",
    smtp_port=587,
    username="your@gmail.com",
    password="your-app-password",  # 使用应用专用密码
    use_tls=True
)

# 发送邮件
emailer.send(
    to="recipient@example.com",
    subject="系统警报",
    body="服务器 CPU 使用率超过 90%",
    from_name="监控系统",
    html=False
)
""")


def example_custom_channel():
    """自定义渠道示例"""
    print("\n" + "=" * 60)
    print("示例 5: 自定义通知渠道")
    print("=" * 60)
    
    # 注册自定义渠道
    def custom_handler(notification: Notification) -> bool:
        """自定义通知处理函数"""
        emoji = {
            Priority.LOW: "📝",
            Priority.NORMAL: "📢",
            Priority.HIGH: "⚠️",
            Priority.URGENT: "🚨",
            Priority.CRITICAL: "🔴"
        }.get(notification.priority, "📢")
        
        print(f"[自定义渠道] {emoji} [{notification.priority.name}] "
              f"{notification.title}: {notification.message}")
        return True
    
    # 注册渠道，带速率限制
    NotificationUtils.register_channel(
        name="custom",
        handler=custom_handler,
        rate_limit=(10, 60)  # 每分钟最多 10 条
    )
    
    # 使用自定义渠道
    notify("测试", "这是一条自定义渠道通知", channel="custom")
    notify("警告", "高优先级自定义通知", channel="custom", priority=Priority.HIGH)


def example_quiet_hours():
    """安静时段示例"""
    print("\n" + "=" * 60)
    print("示例 6: 安静时段配置")
    print("=" * 60)
    
    # 设置安静时段（晚 10 点到早 8 点）
    NotificationUtils.set_quiet_hours(22, 8)
    
    print("已设置安静时段：22:00 - 08:00")
    print("在此期间，LOW 和 NORMAL 优先级通知将被抑制")
    print("HIGH, URGENT, CRITICAL 仍会发送")
    
    # 测试通知
    notify("普通消息", "这条消息在安静时段可能被抑制", priority=Priority.NORMAL)
    notify("重要警报", "这条消息即使在安静时段也会发送", priority=Priority.HIGH)


def example_statistics():
    """统计信息示例"""
    print("\n" + "=" * 60)
    print("示例 7: 统计信息")
    print("=" * 60)
    
    # 发送一些通知
    for i in range(5):
        notify(f"通知{i+1}", f"这是第{i+1}条测试通知")
    
    # 获取统计
    stats = NotificationUtils.get_stats()
    print("\n📊 通知统计:")
    print(f"  总发送：{stats['total_sent']}")
    print(f"  总失败：{stats['total_failed']}")
    print(f"  总跳过：{stats['total_skipped']}")
    print(f"  速率限制：{stats['total_rate_limited']}")
    print(f"  成功率：{stats['success_rate']:.1f}%")
    
    # 重置统计
    NotificationUtils.reset_stats()
    print("\n统计已重置")


def example_batch_notify():
    """批量通知示例"""
    print("\n" + "=" * 60)
    print("示例 8: 批量发送")
    print("=" * 60)
    
    from mod import NotificationRouter
    
    router = NotificationUtils.get_router()
    
    # 创建多条通知
    notifications = [
        Notification(title="日报", message="今日工作完成", priority=Priority.LOW),
        Notification(title="提醒", message="明天有会议", priority=Priority.NORMAL),
        Notification(title="警告", message="存储空间不足", priority=Priority.HIGH),
    ]
    
    # 批量发送
    statuses = router.send_batch(notifications)
    
    print(f"批量发送 {len(notifications)} 条通知:")
    for n, s in zip(notifications, statuses):
        print(f"  - {n.title}: {s.name}")


def main():
    """运行所有示例"""
    print("\n" + "🔔" * 30)
    print("AllToolkit - Python Notification Utils 使用示例")
    print("🔔" * 30)
    
    example_basic_notify()
    example_desktop_notify()
    example_webhook_notify()
    example_email_notify()
    example_custom_channel()
    example_quiet_hours()
    example_statistics()
    example_batch_notify()
    
    print("\n" + "=" * 60)
    print("✅ 所有示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
