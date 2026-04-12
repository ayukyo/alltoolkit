# Webhook Utils 🎣

**零依赖、生产就绪的 Python Webhook 工具库**

支持发送 Webhook、HMAC 签名验证、重试机制、异步发送等功能。

---

## ✨ 特性

- **多种发送方式** - 同步、异步、批量发送
- **HMAC 签名** - 安全的请求签名与验证
- **自动重试** - 支持固定、线性、指数退避策略
- **线程安全** - 所有操作支持多线程并发
- **事件日志** - 内置发送统计和日志记录
- **装饰器支持** - 一行代码为函数添加 Webhook 发送
- **完整测试** - 100+ 测试用例，覆盖所有场景

---

## 📦 安装

无需安装，直接复制 `mod.py` 到你的项目即可使用。

```bash
# 或者从 AllToolkit 克隆
git clone https://github.com/ayukyo/alltoolkit.git
cp AllToolkit/Python/webhook_utils/mod.py your_project/
```

---

## 🚀 快速开始

### 基础用法

```python
from mod import WebhookSender, WebhookConfig, WebhookEvent

# 创建发送器
sender = WebhookSender()

# 配置 Webhook
config = WebhookConfig(
    url="https://example.com/webhook",
    secret="my-secret-key",  # 可选，用于签名
    max_retries=3,
    timeout=30.0,
)

# 创建事件
event = WebhookEvent(
    event_type="user.created",
    payload={"user_id": 123, "email": "test@example.com"},
)

# 发送
result = sender.send(event, config)

if result.success:
    print(f"发送成功！状态码：{result.status_code}")
else:
    print(f"发送失败：{result.error}")
```

### 便捷函数

```python
from mod import send_webhook

# 一行代码发送
result = send_webhook(
    url="https://example.com/webhook",
    event_type="order.completed",
    payload={"order_id": "ORD-123"},
    secret="my-secret",
)
```

---

## 🔐 签名与验证

### 生成签名

```python
from mod import WebhookSigner

signer = WebhookSigner("my-secret-key")

# 签名 payload
payload = {"event": "user.created", "user_id": 123}
signature = signer.sign(payload)

print(f"签名：{signature}")
# 输出：sha256=abc123...

# 获取签名头
headers = signer.get_signature_header(payload)
print(headers)
# {'X-Webhook-Signature': 'sha256=abc123...'}
```

### 验证签名

```python
from mod import WebhookSigner

signer = WebhookSigner("my-secret-key")

# 验证签名
is_valid = signer.verify(payload, signature)

if is_valid:
    print("签名有效")
else:
    print("签名无效")
```

### 接收端验证示例

```python
from mod import WebhookSigner, verify_signature

def handle_webhook(request):
    # 获取请求体和签名
    payload = request.get_data()
    signature = request.headers.get('X-Webhook-Signature')
    
    # 验证签名
    signer = WebhookSigner("my-secret-key")
    
    # 从 header 中提取算法和签名
    if signature and '=' in signature:
        algorithm, sig = signature.split('=', 1)
        signer = WebhookSigner("my-secret-key", algorithm)
        
        if not signer.verify(payload, sig):
            return "Invalid signature", 401
    
    # 处理 webhook
    process_webhook(request.json)
    return "OK", 200
```

---

## 🔄 重试策略

```python
from mod import WebhookConfig, RetryStrategy

# 指数退避（默认）- 1s, 2s, 4s, 8s...
config = WebhookConfig(
    url="https://example.com/webhook",
    max_retries=3,
    retry_strategy=RetryStrategy.EXPONENTIAL,
    retry_delay=1.0,
)

# 固定延迟
config = WebhookConfig(
    url="https://example.com/webhook",
    retry_strategy=RetryStrategy.FIXED,
    retry_delay=2.0,  # 每次重试等待 2 秒
)

# 线性退避 - 1s, 2s, 3s, 4s...
config = WebhookConfig(
    url="https://example.com/webhook",
    retry_strategy=RetryStrategy.LINEAR,
    retry_delay=1.0,
)

# 不重试
config = WebhookConfig(
    url="https://example.com/webhook",
    retry_strategy=RetryStrategy.NONE,
)
```

---

## ⚡ 异步发送

```python
from mod import AsyncWebhookSender, WebhookConfig, WebhookEvent

sender = AsyncWebhookSender(max_workers=10)

config = WebhookConfig(url="https://example.com/webhook")
event = WebhookEvent(event_type="test", payload={})

# 异步发送
future = sender.send_async(event, config)

# 等待结果
result = future.result(timeout=30)
print(f"完成：{result.success}")

# 或使用回调
def on_complete(result):
    if result.success:
        print("发送成功！")
    else:
        print(f"失败：{result.error}")

sender.send_async(event, config, callback=on_complete)
```

---

## 📊 多端点管理

```python
from mod import WebhookManager, WebhookConfig, WebhookEvent

manager = WebhookManager()

# 注册多个端点
manager.register("slack", WebhookConfig(
    url="https://hooks.slack.com/services/xxx",
))

manager.register("discord", WebhookConfig(
    url="https://discord.com/api/webhooks/xxx",
))

manager.register("custom", WebhookConfig(
    url="https://api.example.com/webhook",
    secret="my-secret",
))

# 发送到特定端点
event = WebhookEvent("alert", {"message": "Server down!"})
result = manager.send("slack", event)

# 广播到所有端点
results = manager.broadcast(event)

for name, result in results.items():
    status = "✓" if result.success else "✗"
    print(f"{status} {name}: {result.status_code}")
```

---

## 📝 事件日志与统计

```python
from mod import WebhookSender, WebhookLogger

# 创建带日志的发送器
logger = WebhookLogger(max_events=1000)
sender = WebhookSender(logger=logger)

# 发送一些 webhook
config = WebhookConfig(url="https://example.com/webhook")
for i in range(10):
    event = WebhookEvent("test", {"id": i})
    sender.send(event, config)

# 获取统计
stats = sender.get_stats()
print(f"总发送：{stats['total_sent']}")
print(f"成功：{stats['total_success']}")
print(f"失败：{stats['total_failed']}")
print(f"成功率：{stats['success_rate']:.2%}")

# 获取最近事件
recent = sender.get_recent_events(limit=5)
for event in recent:
    print(f"{event['type']}: {event.get('status_code')} - {event.get('error', 'OK')}")

# 清除日志
logger.clear()
```

---

## 🎭 装饰器用法

```python
from mod import webhook_decorator

# 自动发送 webhook
@webhook_decorator(
    event_type="user.created",
    url="https://example.com/webhook",
    secret="my-secret",
    payload_fn=lambda result: {"user_id": result["id"], "email": result["email"]},
)
def create_user(name, email):
    # 创建用户逻辑
    user = {"id": 123, "name": name, "email": email}
    return user

# 调用函数会自动发送 webhook（后台线程）
user = create_user("Alice", "alice@example.com")
print(f"创建用户：{user}")
```

---

## 📁 完整示例

### Slack 通知

```python
from mod import send_webhook

def send_slack_alert(message, channel="#general"):
    """发送 Slack 通知"""
    payload = {
        "channel": channel,
        "username": "Alert Bot",
        "icon_emoji": ":warning:",
        "attachments": [{
            "color": "danger" if "ERROR" in message else "good",
            "text": message,
        }]
    }
    
    result = send_webhook(
        url="https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK",
        event_type="slack.alert",
        payload=payload,
    )
    
    return result.success

# 使用
send_slack_alert("ERROR: Database connection failed!")
```

### Discord 通知

```python
from mod import send_webhook

def send_discord_embed(title, description, color=0xff0000):
    """发送 Discord 嵌入消息"""
    payload = {
        "embeds": [{
            "title": title,
            "description": description,
            "color": color,
            "timestamp": __import__('datetime').datetime.utcnow().isoformat(),
        }]
    }
    
    result = send_webhook(
        url="https://discord.com/api/webhooks/YOUR/DISCORD/WEBHOOK",
        event_type="discord.notify",
        payload=payload,
    )
    
    return result.success

# 使用
send_discord_embed("🚀 部署完成", "新版本已上线", color=0x00ff00)
```

### GitHub 风格签名验证

```python
from mod import WebhookSigner

def verify_github_webhook(payload, signature, secret):
    """
    验证 GitHub Webhook 签名
    
    GitHub 签名格式：sha256=abc123...
    """
    signer = WebhookSigner(secret, "sha256")
    
    if signature and signature.startswith("sha256="):
        sig = signature[7:]  # 移除 'sha256=' 前缀
        return signer.verify(payload, sig)
    
    return False

# Flask 示例
from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.get_data()
    signature = request.headers.get('X-Hub-Signature-256')
    secret = "your-github-secret"
    
    if not verify_github_webhook(payload, signature, secret):
        return "Invalid signature", 401
    
    # 处理事件
    event = request.json
    print(f"收到事件：{event['action']}")
    
    return "OK", 200
```

---

## 🧪 运行测试

```bash
cd webhook_utils
python webhook_utils_test.py
```

---

## 📊 测试覆盖

- ✅ WebhookEvent 创建与序列化
- ✅ WebhookSigner 签名与验证
- ✅ WebhookConfig 配置选项
- ✅ WebhookResult 结果处理
- ✅ WebhookLogger 日志与统计
- ✅ WebhookSender 发送与重试
- ✅ WebhookManager 多端点管理
- ✅ AsyncWebhookSender 异步发送
- ✅ 装饰器自动发送
- ✅ 边界情况处理（大 payload、Unicode、网络错误等）

---

## 🔒 安全建议

1. **使用 HTTPS** - 生产环境始终使用 HTTPS URL
2. **保护密钥** - 不要将 secret 硬编码在代码中，使用环境变量
3. **验证签名** - 接收端始终验证签名
4. **限制重试** - 避免无限重试导致资源耗尽
5. **设置超时** - 防止请求挂起

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

仓库：https://github.com/ayukyo/alltoolkit
