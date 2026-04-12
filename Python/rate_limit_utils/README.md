# Rate Limit Utils 🚦

**零依赖、生产就绪的 Python 速率限制工具库**

---

## ✨ 特性

- **多种限流策略** - Token Bucket、Sliding Window、Fixed Window
- **零依赖** - 仅使用 Python 标准库
- **线程安全** - 所有操作都支持多线程并发
- **灵活的 Key 管理** - 支持按用户、IP、API Key 等维度限流
- **装饰器支持** - 一行代码为函数添加限流
- **完整测试** - 70+ 测试用例，覆盖所有场景

---

## 📦 安装

无需安装，直接复制 `mod.py` 到你的项目即可使用。

```bash
# 或者从 AllToolkit 克隆
git clone https://github.com/ayukyo/alltoolkit.git
cp AllToolkit/Python/rate_limit_utils/mod.py your_project/
```

---

## 🚀 快速开始

### 基础用法 - Token Bucket

```python
from mod import TokenBucket

# 创建限流器：容量 10 个令牌，每秒补充 2 个
bucket = TokenBucket(capacity=10, refill_rate=2.0)

# 尝试消费令牌
if bucket.consume():
    # 请求被允许
    process_request()
else:
    # 请求被限制
    handle_rate_limit()
```

### 滑动窗口限流

```python
from mod import SlidingWindowCounter

# 每分钟最多 100 个请求
limiter = SlidingWindowCounter(max_requests=100, window_seconds=60)

if limiter.allow():
    # 允许请求
    pass
else:
    # 限流中
    pass
```

### 多 Key 限流（按用户限流）

```python
from mod import RateLimiter

# 创建限流器，每个用户独立限流
limiter = RateLimiter(
    strategy='token_bucket',
    capacity=10,
    refill_rate=1.0,
)

# 检查用户请求
user_id = "user_123"
if limiter.allow(user_id):
    # 该用户的请求被允许
    pass
```

### 使用装饰器

```python
from mod import rate_limit

# 限制函数每分钟最多调用 10 次
@rate_limit(max_requests=10, window_seconds=60)
def api_call():
    return "API response"

# 按用户限流
@rate_limit(
    max_requests=100,
    window_seconds=60,
    key_func=lambda user_id, **kwargs: user_id
)
def user_action(user_id: str, action: str):
    return f"Action {action} for user {user_id}"
```

---

## 📚 API 参考

### TokenBucket

令牌桶限流器，适合需要平滑限流的场景。

```python
TokenBucket(capacity: int, refill_rate: float)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| capacity | int | 桶容量（最大令牌数） |
| refill_rate | float | 令牌补充速率（个/秒） |

**方法：**

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `consume(tokens=1)` | 消费令牌 | bool - 是否成功 |
| `check(tokens=1)` | 检查状态（不消费） | RateLimitResult |
| `wait_time(tokens=1)` | 计算等待时间 | float - 秒数 |
| `reset()` | 重置为满容量 | None |
| `tokens` | 当前令牌数（property） | float |

**示例：**

```python
bucket = TokenBucket(capacity=10, refill_rate=2.0)

# 消费 3 个令牌
bucket.consume(3)

# 检查状态
result = bucket.check()
print(f"剩余：{result.remaining}")
print(f"是否允许：{result.allowed}")

# 计算等待时间
wait = bucket.wait_time(5)
print(f"需要等待 {wait} 秒才能获得 5 个令牌")
```

---

### SlidingWindowCounter

滑动窗口计数器，平衡精度和内存使用。

```python
SlidingWindowCounter(max_requests: int, window_seconds: float)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| max_requests | int | 窗口内最大请求数 |
| window_seconds | float | 窗口时长（秒） |

**方法：**

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `allow()` | 允许并记录请求 | bool |
| `check()` | 检查状态 | RateLimitResult |
| `reset()` | 重置计数器 | None |

---

### SlidingWindowLog

精确滑动窗口日志，最准确但内存占用较高。

```python
SlidingWindowLog(max_requests: int, window_seconds: float)
```

**额外属性：**

| 属性 | 说明 |
|------|------|
| `count` | 当前窗口内请求数 |

---

### FixedWindowCounter

固定窗口计数器，简单但有边界突刺问题。

```python
FixedWindowCounter(max_requests: int, window_seconds: float)
```

---

### RateLimiter

多 Key 限流器，支持按不同维度限流。

```python
RateLimiter(
    strategy: str = 'token_bucket',
    max_requests: int = 100,
    window_seconds: float = 60.0,
    capacity: int = 10,
    refill_rate: float = 1.0,
    cleanup_interval: float = 300.0,
)
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| strategy | 'token_bucket' | 限流策略 |
| max_requests | 100 | 窗口最大请求数 |
| window_seconds | 60.0 | 窗口时长 |
| capacity | 10 | Token Bucket 容量 |
| refill_rate | 1.0 | Token Bucket 补充速率 |
| cleanup_interval | 300.0 | 清理过期 Key 间隔（秒） |

**支持策略：**

- `'token_bucket'` - 令牌桶
- `'sliding_window'` - 滑动窗口计数器
- `'sliding_window_log'` - 滑动窗口日志
- `'fixed_window'` - 固定窗口

**方法：**

| 方法 | 说明 |
|------|------|
| `allow(key: str)` | 检查并记录请求 |
| `check(key: str)` | 检查状态 |
| `reset(key: str)` | 重置指定 Key |
| `reset_all()` | 重置所有 Key |

---

### 装饰器

#### rate_limit

宽松限流装饰器，超限时返回 None 或调用回调。

```python
@rate_limit(
    max_requests: int = 100,
    window_seconds: float = 60.0,
    key_func: Optional[Callable] = None,
    strategy: str = 'sliding_window',
    on_limit: Optional[Callable] = None,
)
```

**示例：**

```python
# 基础用法
@rate_limit(max_requests=10, window_seconds=60)
def my_function():
    pass

# 自定义 Key
@rate_limit(
    max_requests=100,
    key_func=lambda user_id, **kwargs: user_id
)
def user_api(user_id: str):
    pass

# 超限回调
def handle_limit(*args, **kwargs):
    return {"error": "rate limited"}

@rate_limit(
    max_requests=10,
    window_seconds=60,
    on_limit=handle_limit
)
def api_endpoint():
    return {"data": "response"}
```

#### rate_limit_strict

严格限流装饰器，超限时抛出异常。

```python
@rate_limit_strict(
    max_requests: int = 100,
    window_seconds: float = 60.0,
    key_func: Optional[Callable] = None,
    strategy: str = 'sliding_window',
)
```

**示例：**

```python
from mod import rate_limit_strict, RateLimitExceeded

@rate_limit_strict(max_requests=10, window_seconds=60)
def strict_api():
    pass

try:
    strict_api()
except RateLimitExceeded as e:
    print(f"限流！{e.retry_after} 秒后重试")
    print(f"详情：{e.to_dict()}")
```

---

### RateLimitResult

限流检查结果。

```python
@dataclass
class RateLimitResult:
    allowed: bool          # 是否允许
    remaining: int         # 剩余配额
    reset_at: float        # 重置时间戳
    retry_after: float     # 建议重试时间（秒）
    limit: int             # 总配额
    window_seconds: float  # 窗口时长
```

**方法：**

| 方法 | 说明 |
|------|------|
| `to_dict()` | 转换为字典 |
| `__bool__()` | 支持布尔判断 |

---

### rate_limit_context

限流上下文管理器。

```python
from mod import rate_limit_context, RateLimiter

limiter = RateLimiter()

with rate_limit_context(limiter, 'user_123'):
    # 限流内的代码
    process_request()

# 带回调
with rate_limit_context(limiter, 'user_123', on_limit=lambda: log_limit()):
    process_request()
```

---

## 🎯 使用场景

### API 限流

```python
from mod import RateLimiter

api_limiter = RateLimiter(
    strategy='sliding_window',
    max_requests=1000,
    window_seconds=3600,  # 每小时 1000 次
)

def api_endpoint(request):
    client_ip = request.remote_addr
    if not api_limiter.allow(client_ip):
        return {"error": "Rate limited"}, 429
    return process_api(request)
```

### 用户操作限流

```python
from mod import TokenBucket

# 每个用户每秒最多 2 次操作
user_buckets: Dict[str, TokenBucket] = {}

def get_user_bucket(user_id: str) -> TokenBucket:
    if user_id not in user_buckets:
        user_buckets[user_id] = TokenBucket(capacity=5, refill_rate=2.0)
    return user_buckets[user_id]

def user_action(user_id: str):
    bucket = get_user_bucket(user_id)
    if not bucket.consume():
        wait = bucket.wait_time()
        return f"请等待 {wait:.1f} 秒"
    return "操作成功"
```

### 爬虫限流

```python
from mod import SlidingWindowLog

# 每秒最多 1 个请求，避免被封
crawler_limiter = SlidingWindowLog(max_requests=1, window_seconds=1.0)

def crawl_page(url: str):
    while not crawler_limiter.allow():
        time.sleep(0.1)
    return fetch(url)
```

### 批量任务限流

```python
from mod import FixedWindowCounter

# 每分钟最多 100 个任务
task_limiter = FixedWindowCounter(max_requests=100, window_seconds=60)

def submit_task(task):
    if not task_limiter.allow():
        queue_task(task)  # 加入队列等待
    else:
        process_task(task)
```

---

## 🧪 测试

运行完整测试套件：

```bash
cd AllToolkit/Python/rate_limit_utils
python rate_limit_utils_test.py
```

**测试覆盖：**

- ✅ TokenBucket 基础功能
- ✅ TokenBucket 令牌补充
- ✅ TokenBucket 状态检查
- ✅ TokenBucket 多线程安全
- ✅ SlidingWindowCounter 窗口过期
- ✅ SlidingWindowLog 精确计数
- ✅ FixedWindowCounter 基础功能
- ✅ RateLimiter 多 Key 管理
- ✅ 装饰器功能
- ✅ 异常处理
- ✅ 边界值测试

---

## 📊 策略选择指南

| 场景 | 推荐策略 | 理由 |
|------|----------|------|
| API 限流 | SlidingWindow | 平衡精度和性能 |
| 用户操作限流 | TokenBucket | 平滑限流，允许突发 |
| 爬虫限流 | SlidingWindowLog | 精确控制请求间隔 |
| 简单限流 | FixedWindow | 实现简单，性能好 |
| 高并发场景 | TokenBucket | 线程安全，低锁竞争 |

---

## ⚠️ 注意事项

1. **时钟依赖** - 所有限流器依赖系统时钟，时钟跳变可能影响精度
2. **内存使用** - SlidingWindowLog 会存储时间戳，高并发场景注意内存
3. **分布式限流** - 本模块为单机限流，分布式场景需使用 Redis 等
4. **时间精度** - 使用 `time.time()`，精度约毫秒级

---

## 📄 许可证

MIT License

---

## 🔗 相关链接

- [AllToolkit 主页](https://github.com/ayukyo/alltoolkit)
- [Python 模块列表](../README.md)
- [贡献指南](../../docs/contributing.md)
