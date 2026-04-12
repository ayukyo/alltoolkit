#!/usr/bin/env python3
"""
Webhook Utils - Advanced Usage Examples

演示 webhook_utils 模块的高级用法和实际应用场景。
"""

import sys
import os
import time
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    WebhookSender,
    WebhookConfig,
    WebhookEvent,
    WebhookSigner,
    WebhookManager,
    AsyncWebhookSender,
    RetryStrategy,
    webhook_decorator,
)


# ============================================================
# 场景 1: Slack 通知
# ============================================================

def send_slack_message(webhook_url: str, message: str, channel: str = "#general",
                       username: str = "Bot", icon: str = ":robot_face:") -> bool:
    """
    发送 Slack 消息
    
    Args:
        webhook_url: Slack Incoming Webhook URL
        message: 消息内容
        channel: 频道
        username: 用户名
        icon: 表情图标
    
    Returns:
        是否成功
    """
    payload = {
        "channel": channel,
        "username": username,
        "icon_emoji": icon,
        "text": message,
    }
    
    # 使用便捷函数发送
    from mod import send_webhook
    
    result = send_webhook(
        url=webhook_url,
        event_type="slack.message",
        payload=payload,
        timeout=10.0,
    )
    
    return result.success


def send_slack_alert(webhook_url: str, title: str, message: str, 
                     level: str = "info") -> bool:
    """
    发送 Slack 告警消息（带附件）
    
    Args:
        webhook_url: Slack Incoming Webhook URL
        title: 告警标题
        message: 告警内容
        level: 级别 (info/warning/error/critical)
    
    Returns:
        是否成功
    """
    colors = {
        "info": "#36a64f",      # 绿色
        "warning": "#ff9800",   # 橙色
        "error": "#ff0000",     # 红色
        "critical": "#7b1fa2",  # 紫色
    }
    
    icons = {
        "info": ":information_source:",
        "warning": ":warning:",
        "error": ":x:",
        "critical": ":rotating_light:",
    }
    
    payload = {
        "username": "Alert Bot",
        "icon_emoji": icons.get(level, ":bell:"),
        "attachments": [{
            "color": colors.get(level, "#808080"),
            "title": title,
            "text": message,
            "footer": "AllToolkit Webhook Utils",
            "ts": int(time.time()),
        }]
    }
    
    from mod import send_webhook
    
    result = send_webhook(
        url=webhook_url,
        event_type="slack.alert",
        payload=payload,
        timeout=10.0,
    )
    
    return result.success


# ============================================================
# 场景 2: Discord 通知
# ============================================================

def send_discord_message(webhook_url: str, content: str) -> bool:
    """
    发送 Discord 简单消息
    
    Args:
        webhook_url: Discord Webhook URL
        content: 消息内容
    
    Returns:
        是否成功
    """
    payload = {"content": content}
    
    from mod import send_webhook
    
    result = send_webhook(
        url=webhook_url,
        event_type="discord.message",
        payload=payload,
        timeout=10.0,
    )
    
    return result.success


def send_discord_embed(webhook_url: str, title: str, description: str,
                       color: int = 0x00ff00, fields: list = None) -> bool:
    """
    发送 Discord 嵌入消息
    
    Args:
        webhook_url: Discord Webhook URL
        title: 嵌入标题
        description: 嵌入描述
        color: 颜色 (十进制)
        fields: 附加字段列表
    
    Returns:
        是否成功
    """
    embed = {
        "title": title,
        "description": description,
        "color": color,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    
    if fields:
        embed["fields"] = fields
    
    payload = {"embeds": [embed]}
    
    from mod import send_webhook
    
    result = send_webhook(
        url=webhook_url,
        event_type="discord.embed",
        payload=payload,
        timeout=10.0,
    )
    
    return result.success


# ============================================================
# 场景 3: 服务器监控告警
# ============================================================

class ServerMonitor:
    """服务器监控器，发送告警到多个平台"""
    
    def __init__(self, slack_url: str = None, discord_url: str = None):
        self.manager = WebhookManager()
        
        if slack_url:
            self.manager.register("slack", WebhookConfig(
                url=slack_url,
                timeout=10.0,
                max_retries=2,
            ))
        
        if discord_url:
            self.manager.register("discord", WebhookConfig(
                url=discord_url,
                timeout=10.0,
                max_retries=2,
            ))
    
    def alert_cpu_high(self, hostname: str, usage: float):
        """CPU 使用率过高告警"""
        event = WebhookEvent(
            event_type="monitor.cpu_high",
            payload={
                "hostname": hostname,
                "cpu_usage": usage,
                "threshold": 80.0,
                "timestamp": time.time(),
            }
        )
        
        results = self.manager.broadcast(event)
        return all(r.success for r in results.values())
    
    def alert_disk_space(self, hostname: str, partition: str, 
                         used_percent: float):
        """磁盘空间不足告警"""
        event = WebhookEvent(
            event_type="monitor.disk_low",
            payload={
                "hostname": hostname,
                "partition": partition,
                "used_percent": used_percent,
                "threshold": 90.0,
            }
        )
        
        results = self.manager.broadcast(event)
        return all(r.success for r in results.values())
    
    def alert_service_down(self, service_name: str, hostname: str):
        """服务宕机告警"""
        event = WebhookEvent(
            event_type="monitor.service_down",
            payload={
                "service": service_name,
                "hostname": hostname,
                "severity": "critical",
            }
        )
        
        results = self.manager.broadcast(event)
        return all(r.success for r in results.values())


# ============================================================
# 场景 4: CI/CD 通知
# ============================================================

class CINotifier:
    """CI/CD 构建通知器"""
    
    def __init__(self, webhook_url: str, secret: str = None):
        self.sender = WebhookSender()
        self.config = WebhookConfig(
            url=webhook_url,
            secret=secret,
            timeout=30.0,
            max_retries=3,
            retry_strategy=RetryStrategy.EXPONENTIAL,
        )
    
    def notify_build_started(self, repo: str, branch: str, 
                             commit: str, build_id: str):
        """构建开始通知"""
        event = WebhookEvent(
            event_type="ci.build_started",
            payload={
                "status": "started",
                "repo": repo,
                "branch": branch,
                "commit": commit,
                "build_id": build_id,
                "timestamp": time.time(),
            }
        )
        return self.sender.send(event, self.config)
    
    def notify_build_success(self, repo: str, branch: str,
                             commit: str, build_id: str, duration: float):
        """构建成功通知"""
        event = WebhookEvent(
            event_type="ci.build_success",
            payload={
                "status": "success",
                "repo": repo,
                "branch": branch,
                "commit": commit,
                "build_id": build_id,
                "duration": duration,
            }
        )
        return self.sender.send(event, self.config)
    
    def notify_build_failed(self, repo: str, branch: str,
                            commit: str, build_id: str, error: str):
        """构建失败通知"""
        event = WebhookEvent(
            event_type="ci.build_failed",
            payload={
                "status": "failed",
                "repo": repo,
                "branch": branch,
                "commit": commit,
                "build_id": build_id,
                "error": error,
            }
        )
        return self.sender.send(event, self.config)


# ============================================================
# 场景 5: 使用装饰器自动发送
# ============================================================

def demo_decorator():
    """演示装饰器用法"""
    print("\n" + "=" * 60)
    print("场景 5: 装饰器自动发送 Webhook")
    print("=" * 60)
    
    # 注意：这里使用 httpbin 作为测试端点
    @webhook_decorator(
        event_type="user.registered",
        url="https://httpbin.org/post",
        payload_fn=lambda user: {
            "user_id": user.get("id"),
            "username": user.get("username"),
            "email": user.get("email"),
        },
        max_retries=0,
    )
    def register_user(username: str, email: str) -> dict:
        """注册用户（会自动发送 webhook）"""
        # 模拟用户创建
        user = {
            "id": int(time.time() % 10000),
            "username": username,
            "email": email,
            "created_at": time.time(),
        }
        return user
    
    # 调用函数会自动发送 webhook
    print("注册用户...")
    user = register_user("alice", "alice@example.com")
    print(f"用户已创建：{user}")
    print("Webhook 已异步发送！")


# ============================================================
# 场景 6: 批量异步发送
# ============================================================

def demo_batch_async():
    """演示批量异步发送"""
    print("\n" + "=" * 60)
    print("场景 6: 批量异步发送")
    print("=" * 60)
    
    sender = AsyncWebhookSender(max_workers=10)
    
    config = WebhookConfig(
        url="https://httpbin.org/post",
        timeout=10.0,
    )
    
    # 创建 20 个事件
    events = [
        WebhookEvent(
            event_type="batch.event",
            payload={"index": i, "timestamp": time.time()}
        )
        for i in range(20)
    ]
    
    print(f"发送 {len(events)} 个异步请求...")
    
    # 批量发送
    futures = []
    for event in events:
        future = sender.send_async(event, config)
        futures.append(future)
    
    # 等待所有完成
    success_count = 0
    fail_count = 0
    
    for i, future in enumerate(futures):
        try:
            result = future.result(timeout=30)
            if result.success:
                success_count += 1
            else:
                fail_count += 1
        except Exception as e:
            fail_count += 1
            print(f"  事件 {i} 异常：{e}")
    
    print(f"\n完成：成功 {success_count}, 失败 {fail_count}")


# ============================================================
# 场景 7: GitHub 风格签名验证
# ============================================================

def demo_github_signature():
    """演示 GitHub 风格签名验证"""
    print("\n" + "=" * 60)
    print("场景 7: GitHub 风格签名验证")
    print("=" * 60)
    
    secret = "github-webhook-secret"
    signer = WebhookSigner(secret, "sha256")
    
    # 模拟 GitHub payload
    payload = {
        "action": "opened",
        "pull_request": {
            "id": 12345,
            "number": 42,
            "title": "Fix bug in webhook utils",
        }
    }
    
    # 生成签名（模拟 GitHub）
    payload_json = json.dumps(payload, separators=(',', ':'), sort_keys=True)
    signature = "sha256=" + signer.sign(payload_json)
    
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print(f"签名：{signature[:50]}...")
    
    # 验证签名（模拟接收端）
    def verify_github_webhook(payload_str: str, signature: str, secret: str) -> bool:
        """验证 GitHub Webhook 签名"""
        if not signature or not signature.startswith("sha256="):
            return False
        
        sig = signature[7:]  # 移除 'sha256=' 前缀
        verifier = WebhookSigner(secret, "sha256")
        return verifier.verify(payload_str, sig)
    
    is_valid = verify_github_webhook(payload_json, signature, secret)
    print(f"验证结果：{'✓ 有效' if is_valid else '✗ 无效'}")
    
    # 测试错误密钥
    is_valid_wrong = verify_github_webhook(payload_json, signature, "wrong-secret")
    print(f"错误密钥验证：{'✓ 有效' if is_valid_wrong else '✗ 无效 (预期)'}")


# ============================================================
# 主函数
# ============================================================

def main():
    """运行所有高级示例"""
    print("\n" + "🎣" * 30)
    print("Webhook Utils 高级示例")
    print("🎣" * 30 + "\n")
    
    # 运行演示
    demo_decorator()
    demo_batch_async()
    demo_github_signature()
    
    print("\n" + "=" * 60)
    print("注意：Slack/Discord/监控示例需要真实的 Webhook URL")
    print("请替换示例中的 URL 后运行")
    print("=" * 60 + "\n")
    
    # 打印使用示例代码
    print("\nSlack 通知示例代码:")
    print("-" * 40)
    print("""
from mod import send_webhook

# 发送 Slack 消息
result = send_webhook(
    url="https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK",
    event_type="slack.message",
    payload={
        "channel": "#general",
        "username": "Bot",
        "text": "Hello from AllToolkit!",
    },
)
""")
    
    print("\nDiscord 通知示例代码:")
    print("-" * 40)
    print("""
from mod import send_webhook

# 发送 Discord 嵌入消息
result = send_webhook(
    url="https://discord.com/api/webhooks/YOUR/DISCORD/WEBHOOK",
    event_type="discord.embed",
    payload={
        "embeds": [{
            "title": "🚀 部署完成",
            "description": "新版本已上线",
            "color": 0x00ff00,
        }]
    },
)
""")
    
    print("\n所有高级示例完成！\n")


if __name__ == "__main__":
    main()
