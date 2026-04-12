#!/usr/bin/env python3
"""
AllToolkit - Notification Utils - Advanced Examples

演示 notification_utils 模块的高级用法和实际应用场景。
"""

import sys
import os
import time
import random
# Add parent directory to path for importing mod
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Notification, NotificationRouter, NotificationStatus,
    Priority, RateLimiter, NotificationUtils,
    notify, notify_desktop, notify_slack, notify_discord
)


# ============================================================
# 场景 1: 系统监控告警系统
# ============================================================

class SystemMonitor:
    """系统监控器示例"""
    
    def __init__(self):
        self.router = NotificationUtils.get_router()
        
        # 配置安静时段
        NotificationUtils.set_quiet_hours(23, 7)
        
        # 告警阈值
        self.thresholds = {
            "cpu": {"warning": 70, "critical": 90},
            "memory": {"warning": 75, "critical": 95},
            "disk": {"warning": 80, "critical": 95},
        }
    
    def check_metric(self, name: str, value: float):
        """检查指标并发送相应通知"""
        thresholds = self.thresholds.get(name, {})
        
        if value >= thresholds.get("critical", 100):
            self._send_alert(name, value, Priority.CRITICAL)
        elif value >= thresholds.get("warning", 100):
            self._send_alert(name, value, Priority.HIGH)
        else:
            # 正常状态，仅记录日志
            notify(f"{name} 正常", f"当前值：{value}%", priority=Priority.LOW, channel="log")
    
    def _send_alert(self, name: str, value: float, priority: Priority):
        """发送告警通知"""
        message = f"{name.upper()} 使用率：{value:.1f}%"
        
        # 多渠道发送
        notify("系统告警", message, priority=priority, channel="console")
        notify_desktop("系统告警", message, priority=priority)
        
        # 严重告警发送到 Slack
        if priority >= Priority.CRITICAL:
            # notify_slack(
            #     url="YOUR_SLACK_WEBHOOK",
            #     message=f"🚨 严重告警：{message}"
            # )
            pass


def example_system_monitoring():
    """系统监控示例"""
    print("\n" + "=" * 60)
    print("场景 1: 系统监控告警系统")
    print("=" * 60)
    
    monitor = SystemMonitor()
    
    # 模拟监控数据
    test_data = [
        ("cpu", 45.2),    # 正常
        ("memory", 72.5), # 警告
        ("disk", 96.1),   # 严重
        ("cpu", 88.3),    # 警告
    ]
    
    for name, value in test_data:
        monitor.check_metric(name, value)
        time.sleep(0.5)


# ============================================================
# 场景 2: CI/CD 流水线通知
# ============================================================

class CICDNotifier:
    """CI/CD 通知器示例"""
    
    def __init__(self, slack_url: str = None, discord_url: str = None):
        self.slack_url = slack_url
        self.discord_url = discord_url
    
    def notify_build_started(self, project: str, branch: str):
        """构建开始通知"""
        notify(
            "🚧 构建开始",
            f"项目：{project}\n分支：{branch}",
            priority=Priority.NORMAL,
            channel="console"
        )
    
    def notify_build_success(self, project: str, duration: float, tests_passed: int):
        """构建成功通知"""
        message = (
            f"✅ 构建成功！\n"
            f"项目：{project}\n"
            f"耗时：{duration:.1f}s\n"
            f"通过测试：{tests_passed}"
        )
        
        notify("构建成功", message, priority=Priority.NORMAL)
        
        # 发送到 Slack
        if self.slack_url:
            notify_slack(
                url=self.slack_url,
                message=f"✅ *{project}* 构建成功！\n耗时：{duration:.1f}s"
            )
        
        # 发送到 Discord
        if self.discord_url:
            notify_discord(
                url=self.discord_url,
                title="✅ 构建成功",
                message=f"**{project}**\n耗时：{duration:.1f}s\n测试通过：{tests_passed}",
                priority=Priority.NORMAL
            )
    
    def notify_build_failed(self, project: str, error: str, failed_tests: list):
        """构建失败通知"""
        message = (
            f"❌ 构建失败！\n"
            f"项目：{project}\n"
            f"错误：{error}\n"
            f"失败测试：{', '.join(failed_tests)}"
        )
        
        notify("构建失败", message, priority=Priority.URGENT)
        notify_desktop("构建失败", f"{project}: {error}", priority=Priority.URGENT)
        
        # 紧急通知到 Slack
        if self.slack_url:
            notify_slack(
                url=self.slack_url,
                message=f"❌ *{project}* 构建失败！\n错误：{error}"
            )


def example_cicd_pipeline():
    """CI/CD 流水线示例"""
    print("\n" + "=" * 60)
    print("场景 2: CI/CD 流水线通知")
    print("=" * 60)
    
    notifier = CICDNotifier()
    
    # 模拟构建流程
    project = "my-awesome-app"
    branch = "main"
    
    notifier.notify_build_started(project, branch)
    time.sleep(1)
    
    # 模拟构建结果
    if random.random() > 0.3:
        notifier.notify_build_success(project, 45.3, 128)
    else:
        notifier.notify_build_failed(
            project,
            "单元测试失败",
            ["test_login", "test_api"]
        )


# ============================================================
# 场景 3: 定时任务提醒
# ============================================================

class TaskScheduler:
    """任务调度器示例"""
    
    def __init__(self):
        self.router = NotificationUtils.get_router()
        self.rate_limiter = RateLimiter(max_notifications=5, window_seconds=60)
    
    def schedule_reminder(self, title: str, message: str, delay_seconds: float):
        """安排延迟提醒"""
        print(f"⏰ 已安排提醒：{title} ({delay_seconds}s 后)")
        
        # 实际应用中这里应该使用真正的调度器
        # 这里仅做演示
        time.sleep(delay_seconds)
        
        if self.rate_limiter.is_allowed("reminder"):
            notify(title, message, priority=Priority.NORMAL)
        else:
            wait_time = self.rate_limiter.get_wait_time("reminder")
            print(f"⏳ 速率限制，等待 {wait_time:.1f}s")
            time.sleep(wait_time)
            notify(title, message, priority=Priority.NORMAL)
    
    def daily_report(self, stats: dict):
        """发送日报"""
        message = (
            "📊 今日统计:\n"
            f"  - 处理请求：{stats.get('requests', 0)}\n"
            f"  - 成功：{stats.get('success', 0)}\n"
            f"  - 失败：{stats.get('failed', 0)}\n"
            f"  - 平均响应：{stats.get('avg_response', 0):.2f}ms"
        )
        
        notify("日报", message, priority=Priority.NORMAL, channel="desktop")
        notify("日报", message, priority=Priority.NORMAL, channel="log")


def example_task_scheduler():
    """任务调度器示例"""
    print("\n" + "=" * 60)
    print("场景 3: 定时任务提醒")
    print("=" * 60)
    
    scheduler = TaskScheduler()
    
    # 模拟多个提醒
    reminders = [
        ("会议提醒", "10 分钟后有团队会议", 0.5),
        ("喝水提醒", "该起来活动一下了", 0.5),
        ("提交提醒", "记得提交今日代码", 0.5),
    ]
    
    for title, message, delay in reminders:
        scheduler.schedule_reminder(title, message, delay)
    
    # 发送日报
    scheduler.daily_report({
        "requests": 1234,
        "success": 1198,
        "failed": 36,
        "avg_response": 45.6
    })


# ============================================================
# 场景 4: 多渠道路由策略
# ============================================================

class SmartRouter:
    """智能路由示例 - 根据通知类型选择最佳渠道"""
    
    def __init__(self):
        self.router = NotificationUtils.get_router()
        self._setup_smart_routing()
    
    def _setup_smart_routing(self):
        """设置智能路由规则"""
        
        # 根据优先级路由
        def priority_filter(notification: Notification) -> bool:
            # CRITICAL 通知发送到所有渠道
            if notification.priority == Priority.CRITICAL:
                notification.metadata["broadcast"] = True
                return True
            
            # 安静时段只允许 HIGH 及以上
            hour = time.localtime().tm_hour
            if 22 <= hour or hour < 7:
                return notification.priority >= Priority.HIGH
            
            return True
        
        self.router.add_filter(priority_filter)
    
    def send_smart_notification(self, notification: Notification):
        """智能发送通知"""
        # 根据优先级决定渠道
        if notification.priority == Priority.CRITICAL:
            # 严重通知：所有渠道
            channels = ["console", "desktop", "log"]
            for channel in channels:
                notification.channel = channel
                self.router.send(Notification(
                    title=notification.title,
                    message=notification.message,
                    priority=notification.priority,
                    channel=channel
                ))
        elif notification.priority == Priority.URGENT:
            # 紧急通知：桌面 + 控制台
            notification.channel = "desktop"
            self.router.send(notification)
            notification.channel = "console"
            self.router.send(notification)
        else:
            # 普通通知：仅控制台
            notification.channel = "console"
            self.router.send(notification)


def example_smart_routing():
    """智能路由示例"""
    print("\n" + "=" * 60)
    print("场景 4: 多渠道智能路由")
    print("=" * 60)
    
    router = SmartRouter()
    
    # 测试不同优先级的路由
    test_notifications = [
        Notification("日志", "普通日志信息", priority=Priority.LOW),
        Notification("提醒", "会议即将开始", priority=Priority.NORMAL),
        Notification("警告", "磁盘空间不足", priority=Priority.HIGH),
        Notification("紧急", "服务不可用", priority=Priority.URGENT),
        Notification("严重", "数据库连接丢失", priority=Priority.CRITICAL),
    ]
    
    for n in test_notifications:
        print(f"\n发送 {n.priority.name} 通知：{n.title}")
        router.send_smart_notification(n)
        time.sleep(0.3)


# ============================================================
# 场景 5: 通知聚合与去重
# ============================================================

class NotificationAggregator:
    """通知聚合器 - 防止重复通知"""
    
    def __init__(self, window_seconds: float = 60.0):
        self.window_seconds = window_seconds
        self._recent_notifications = {}  # hash -> timestamp
    
    def _get_hash(self, title: str, message: str) -> str:
        """生成通知哈希"""
        import hashlib
        content = f"{title}:{message}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def should_send(self, title: str, message: str) -> bool:
        """检查是否应该发送（去重）"""
        hash_key = self._get_hash(title, message)
        now = time.time()
        
        # 清理过期记录
        cutoff = now - self.window_seconds
        self._recent_notifications = {
            k: v for k, v in self._recent_notifications.items()
            if v > cutoff
        }
        
        # 检查是否重复
        if hash_key in self._recent_notifications:
            last_sent = self._recent_notifications[hash_key]
            if now - last_sent < self.window_seconds:
                return False
        
        # 记录发送时间
        self._recent_notifications[hash_key] = now
        return True
    
    def notify(self, title: str, message: str, **kwargs):
        """发送通知（带去重）"""
        if self.should_send(title, message):
            notify(title, message, **kwargs)
            return True
        else:
            print(f"⏭️  跳过重复通知：{title}")
            return False


def example_notification_aggregation():
    """通知聚合示例"""
    print("\n" + "=" * 60)
    print("场景 5: 通知聚合与去重")
    print("=" * 60)
    
    aggregator = NotificationAggregator(window_seconds=5.0)
    
    # 模拟重复通知
    print("发送 5 条相同通知（5 秒窗口去重）:")
    for i in range(5):
        aggregator.notify("警报", "CPU 使用率过高", priority=Priority.HIGH)
        time.sleep(1)
    
    # 发送不同通知
    print("\n发送不同通知:")
    aggregator.notify("警报", "内存使用率过高", priority=Priority.HIGH)
    aggregator.notify("警报", "磁盘使用率过高", priority=Priority.HIGH)


# ============================================================
# 主函数
# ============================================================

def main():
    """运行所有高级示例"""
    print("\n" + "🔔" * 30)
    print("AllToolkit - Python Notification Utils 高级示例")
    print("🔔" * 30)
    
    example_system_monitoring()
    example_cicd_pipeline()
    example_task_scheduler()
    example_smart_routing()
    example_notification_aggregation()
    
    print("\n" + "=" * 60)
    print("✅ 所有高级示例运行完成！")
    print("=" * 60)
    
    # 显示最终统计
    stats = NotificationUtils.get_stats()
    print("\n📊 最终统计:")
    print(f"  总发送：{stats['total_sent']}")
    print(f"  总失败：{stats['total_failed']}")
    print(f"  成功率：{stats['success_rate']:.1f}%")


if __name__ == "__main__":
    main()
