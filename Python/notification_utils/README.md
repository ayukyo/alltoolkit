# AllToolkit - Python Notification Utilities 🔔

**零依赖、生产就绪的通知工具模块**

支持多种通知渠道：桌面通知、日志、Webhook、邮件和控制台。具备优先级、速率限制、批量发送和通知路由功能。

---

## 📦 功能特性

- ✅ **多通道支持**: 控制台、桌面、日志、Webhook、邮件
- ✅ **优先级系统**: LOW, NORMAL, HIGH, URGENT, CRITICAL
- ✅ **速率限制**: 防止通知轰炸
- ✅ **安静时段**: 自动抑制非紧急通知
- ✅ **通知过滤**: 自定义过滤规则
- ✅ **批量发送**: 高效处理多条通知
- ✅ **统计分析**: 追踪发送成功率
- ✅ **零依赖**: 仅使用 Python 标准库

---

## 🚀 快速开始

### 基础使用

```python
from mod import notify, Priority

# 发送控制台通知
notify("标题", "消息内容")

# 发送高优先级通知
notify("警告", "系统负载过高", priority=Priority.HIGH)

# 发送桌面通知
from mod import notify_desktop
notify_desktop("完成", "任务已完成")
```

### 输出示例

```
[07:06:21] 📢 [NORMAL] 标题：消息内容
[07:06:22] ⚠️ [HIGH] 警告：系统负载过高
```

---

## 📖 详细用法

### 1. 优先级系统

```python
from mod import notify, Priority

# 5 个优先级级别
notify("日志", "调试信息", priority=Priority.LOW)       # 📝
notify("通知", "普通消息", priority=Priority.NORMAL)    # 📢
notify("警告", "需要注意", priority=Priority.HIGH)      # ⚠️
notify("紧急", "立即处理", priority=Priority.URGENT)    # 🚨
notify("严重", "系统故障", priority=Priority.CRITICAL)  # 🔴
```

### 2. 桌面通知

```python
from mod import notify_desktop, Priority

# 跨平台桌面通知（Linux/macOS/Windows）
notify_desktop("下载完成", "文件已保存到下载文件夹")

# 高优先级通知（更醒目的提示）
notify_desktop("安全警告", "检测到异常登录", priority=Priority.HIGH)
```

### 3. Webhook 通知

```python
from mod import notify_webhook, notify_slack, notify_discord, Priority

# 通用 Webhook
notify_webhook(
    url="https://your-webhook.com/notify",
    title="系统通知",
    message="服务器已重启",
    priority=Priority.NORMAL
)

# Slack 通知
notify_slack(
    url="https://hooks.slack.com/services/xxx/yyy/zzz",
    message="🚀 新版本已部署",
    channel="#deployments"  # 可选
)

# Discord 通知（带颜色编码）
notify_discord(
    url="https://discord.com/api/webhooks/xxx/yyy",
    title="构建成功",
    message="CI/CD 流水线完成",
    priority=Priority.NORMAL  # 自动映射颜色
)
```

### 4. 邮件通知

```python
from mod import NotificationUtils

# 创建邮件通知器
emailer = NotificationUtils.create_email_notifier(
    smtp_host="smtp.gmail.com",
    smtp_port=587,
    username="your@gmail.com",
    password="your-app-password",
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
```

### 5. 自定义通知渠道

```python
from mod import NotificationUtils, Notification, NotificationStatus

# 注册自定义渠道（如钉钉、企业微信）
def dingtalk_handler(notification: Notification) -> bool:
    # 实现钉钉 Webhook 发送逻辑
    print(f"发送到钉钉：{notification.title}")
    return True

NotificationUtils.register_channel(
    name="dingtalk",
    handler=dingtalk_handler,
    rate_limit=(10, 60)  # 每分钟最多 10 条
)

# 使用自定义渠道
from mod import notify
notify("通知", "消息", channel="dingtalk")
```

### 6. 速率限制

```python
from mod import NotificationUtils

# 设置渠道速率限制（已在桌面渠道默认启用）
# 桌面通知：每分钟最多 5 条

# 设置安静时段（晚 10 点到早 8 点）
NotificationUtils.set_quiet_hours(22, 8)

# 安静时段内，LOW 和 NORMAL 优先级通知会被抑制
# HIGH, URGENT, CRITICAL 仍会发送
```

### 7. 通知过滤

```python
from mod import NotificationUtils, Notification, Priority

# 添加过滤器：只发送包含特定关键词的通知
NotificationUtils.get_router().add_filter(
    lambda n: "警报" in n.title or n.priority >= Priority.HIGH
)

# 添加过滤器：屏蔽特定渠道
NotificationUtils.get_router().add_filter(
    lambda n: n.channel != "test"
)
```

### 8. 批量发送

```python
from mod import NotificationRouter, Notification, Priority

router = NotificationUtils.get_router()

notifications = [
    Notification(title="通知 1", message="内容 1", priority=Priority.NORMAL),
    Notification(title="通知 2", message="内容 2", priority=Priority.HIGH),
    Notification(title="通知 3", message="内容 3", priority=Priority.URGENT),
]

statuses = router.send_batch(notifications)
```

### 9. 统计信息

```python
from mod import NotificationUtils

# 获取统计
stats = NotificationUtils.get_stats()
print(stats)
# {
#     "total_sent": 10,
#     "total_failed": 1,
#     "total_skipped": 2,
#     "total_rate_limited": 0,
#     "success_rate": 90.9,
#     "by_channel": {...},
#     "by_priority": {...}
# }

# 重置统计
NotificationUtils.reset_stats()
```

---

## 🎯 实际应用场景

### 系统监控

```python
from mod import notify, Priority, notify_desktop

def check_system_health():
    cpu_usage = get_cpu_usage()
    
    if cpu_usage > 90:
        notify("严重警报", f"CPU 使用率：{cpu_usage}%", priority=Priority.CRITICAL)
        notify_desktop("严重警报", "CPU 使用率超过 90%!", priority=Priority.CRITICAL)
    elif cpu_usage > 70:
        notify("警告", f"CPU 使用率：{cpu_usage}%", priority=Priority.HIGH)
    else:
        notify("状态", f"CPU 使用率：{cpu_usage}%", priority=Priority.LOW)
```

### CI/CD 通知

```python
from mod import notify_slack, notify_discord, Priority

def notify_build_result(success: bool, duration: float):
    if success:
        notify_slack(
            url=SLACK_WEBHOOK,
            message=f"✅ 构建成功！耗时：{duration:.1f}s"
        )
        notify_discord(
            url=DISCORD_WEBHOOK,
            title="构建成功",
            message=f"耗时：{duration:.1f}s",
            priority=Priority.NORMAL
        )
    else:
        notify_slack(
            url=SLACK_WEBHOOK,
            message=f"❌ 构建失败！请检查日志"
        )
        notify_discord(
            url=DISCORD_WEBHOOK,
            title="构建失败",
            message="请检查构建日志",
            priority=Priority.URGENT
        )
```

### 定时任务提醒

```python
from mod import notify, Priority, NotificationUtils

# 设置安静时段
NotificationUtils.set_quiet_hours(23, 7)

def daily_report():
    # 生成日报
    report = generate_daily_report()
    
    # 工作时间发送桌面通知，非工作时间仅记录
    notify("日报完成", report, priority=Priority.NORMAL, channel="desktop")
    notify("日报完成", report, priority=Priority.NORMAL, channel="log")
```

---

## 📊 通知渠道对比

| 渠道 | 适用场景 | 速率限制 | 跨平台 |
|------|----------|----------|--------|
| `console` | 开发调试、CLI 应用 | 无 | ✅ |
| `desktop` | 用户提醒、本地应用 | 5 条/分钟 | ✅ |
| `log` | 生产环境、审计 | 无 | ✅ |
| `webhook` | 集成第三方服务 | 自定义 | ✅ |
| `slack` | 团队协作 | 自定义 | ✅ |
| `discord` | 社区通知 | 自定义 | ✅ |
| `email` | 重要通知、报告 | 自定义 | ✅ |

---

## 🔧 高级配置

### 完整路由配置示例

```python
from mod import (
    NotificationRouter, Notification, NotificationStatus,
    Priority, RateLimiter
)

# 创建路由器
router = NotificationRouter()

# 注册多个渠道
router.register_channel("console", console_handler)
router.register_channel("desktop", desktop_handler, rate_limit=(5, 60))
router.register_channel("slack", slack_handler, rate_limit=(10, 60))
router.register_channel("email", email_handler, rate_limit=(5, 300))

# 设置安静时段
router.set_quiet_hours(23, 7)

# 添加过滤器：只允许 HIGH 及以上优先级在安静时段发送
router.add_filter(lambda n: n.priority >= Priority.HIGH)

# 发送通知
notification = Notification(
    title="系统警报",
    message="内存使用率超过 85%",
    priority=Priority.HIGH,
    channel="slack",
    metadata={"server": "prod-01", "metric": "memory"}
)

status = router.send(notification)
print(f"发送状态：{status.name}")
```

### 通知对象完整属性

```python
from mod import Notification, Priority, NotificationStatus

notification = Notification(
    title="通知标题",
    message="通知内容",
    priority=Priority.HIGH,          # 优先级
    channel="slack",                 # 渠道
    timestamp=time.time(),           # 时间戳
    metadata={                       # 元数据
        "user_id": 123,
        "action": "deploy",
        "environment": "production"
    },
    status=NotificationStatus.PENDING,  # 状态
    error=None                       # 错误信息
)
```

---

## 🧪 运行测试

```bash
cd notification_utils
python notification_utils_test.py
```

---

## 📁 模块结构

```
notification_utils/
├── mod.py                          # 主要实现
├── notification_utils_test.py      # 测试套件
└── README.md                       # 本文档
```

---

## 🔒 注意事项

1. **桌面通知**: 需要系统支持（Linux: notify-send, macOS: osascript, Windows: PowerShell）
2. **邮件通知**: 建议使用应用专用密码，不要硬编码密码
3. **Webhook**: 注意保护 Webhook URL，避免泄露
4. **速率限制**: 生产环境请根据服务限制调整速率
5. **安静时段**: 根据用户时区配置合适的时间

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

仓库：https://github.com/ayukyo/alltoolkit
