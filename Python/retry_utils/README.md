# AllToolkit - Python Retry Utils 🔄

**零依赖重试机制工具 - 生产就绪**

---

## 📖 概述

`retry_utils` 提供功能完整的重试机制解决方案，支持指数退避、自定义重试条件、抖动、超时控制和统计追踪。完全使用 Python 标准库实现，无需任何外部依赖。

---

## ✨ 特性

- **指数退避** - 可配置的指数增长延迟
- **抖动支持** - 防止重试风暴
- **自定义异常** - 精确控制哪些异常触发重试
- **结果重试** - 基于返回值决定是否重试
- **超时控制** - 整体超时限制
- **回调支持** - 重试前回调用于日志/监控
- **统计追踪** - 成功率、平均重试次数等指标
- **预设配置** - 常用场景的预定义配置
- **装饰器模式** - `@retry` 一键添加重试
- **执行器模式** - `RetryExecutor` 复用配置

---

## 🚀 快速开始

### 基础使用

```python
from mod import retry

@retry(max_retries=3, base_delay=1.0)
def unstable_api():
    # 可能失败的 API 调用
    response = requests.get("https://api.example.com/data")
    return response.json()

# 自动重试最多 3 次
result = unstable_api()
```

### 自定义配置

```python
from mod import RetryConfig, RetryExecutor

config = RetryConfig(
    max_retries=5,
    base_delay=0.5,
    max_delay=30.0,
    jitter=True,
)

executor = RetryExecutor(config)
result = executor.execute(my_function, arg1, arg2)
```

---

## 📚 API 参考

### RetryConfig 类

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `max_retries` | int | 3 | 最大重试次数 |
| `base_delay` | float | 1.0 | 基础延迟（秒） |
| `max_delay` | float | 60.0 | 最大延迟（秒） |
| `exponential_base` | float | 2.0 | 指数退避基数 |
| `jitter` | bool | True | 启用抖动 |
| `jitter_factor` | float | 0.1 | 抖动因子 (0.0-1.0) |
| `retryable_exceptions` | Exception | Exception | 可重试的异常类型 |
| `retry_on_result` | Callable | None | 基于结果重试的条件 |
| `timeout` | float | None | 整体超时（秒） |
| `on_retry` | Callable | None | 重试前回调 |
| `stats` | RetryStats | None | 统计对象 |

### RetryExecutor 类

| 方法 | 描述 | 返回 |
|------|------|------|
| `execute(func, *args, **kwargs)` | 执行函数带重试 | `T` |
| `attempts` | 获取重试尝试记录 | `List[RetryAttempt]` |

### RetryStats 类

| 属性 | 描述 |
|------|------|
| `total_calls` | 总调用次数 |
| `successful_calls` | 成功调用次数 |
| `failed_calls` | 失败调用次数 |
| `total_retries` | 总重试次数 |
| `total_time` | 总耗时（秒） |
| `success_rate` | 成功率 (0.0-1.0) |
| `avg_retries` | 平均每次失败的重试次数 |
| `avg_time` | 平均每次调用耗时 |

### 装饰器

```python
@retry(
    max_retries=3,
    base_delay=1.0,
    retryable_exceptions=(ConnectionError, TimeoutError),
)
def my_function():
    pass
```

---

## 🎯 使用场景

### 1. 网络请求重试

```python
from mod import retry, NetworkError

@retry(
    max_retries=3,
    base_delay=1.0,
    retryable_exceptions=(NetworkError, ConnectionError, TimeoutError)
)
def fetch_data(url):
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()
```

### 2. 数据库连接重试

```python
from mod import RETRY_DATABASE, retry_with_config

def query_database(sql):
    conn = get_connection()
    return conn.execute(sql)

# 使用预设的数据库重试配置
result = retry_with_config(query_database, RETRY_DATABASE, "SELECT * FROM users")
```

### 3. API 速率限制处理

```python
from mod import retry, RateLimitError

def on_rate_limit(attempt, exception, delay):
    if isinstance(exception, RateLimitError):
        print(f"Rate limited, waiting {exception.retry_after}s")

@retry(
    max_retries=5,
    base_delay=2.0,
    retryable_exceptions=(RateLimitError,),
    on_retry=on_rate_limit,
)
def call_api():
    response = requests.post("https://api.example.com/endpoint")
    if response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 1))
        raise RateLimitError("Rate limited", retry_after=retry_after)
    return response.json()
```

### 4. 基于结果的重试

```python
from mod import retry

@retry(
    max_retries=5,
    base_delay=0.5,
    retry_on_result=lambda x: x is None or x == ""
)
def get_eventual_data():
    # 最终一致性场景：数据可能暂时不存在
    data = database.query("SELECT * FROM table WHERE id = 1")
    return data  # 如果为 None 会重试
```

### 5. 带超时的重试

```python
from mod import RetryConfig, RetryExecutor

config = RetryConfig(
    max_retries=10,
    base_delay=1.0,
    timeout=30.0,  # 总超时 30 秒
)

executor = RetryExecutor(config)
result = executor.execute(slow_operation)
```

### 6. 统计监控

```python
from mod import RetryConfig, RetryStats

stats = RetryStats()
config = RetryConfig(stats=stats)
executor = RetryExecutor(config)

# 使用缓存...
for i in range(100):
    try:
        executor.execute(api_call)
    except:
        pass

# 查看统计
print(f"成功率：{stats.success_rate:.1%}")
print(f"平均重试：{stats.avg_retries:.2f}")
print(f"详细统计：{stats.to_dict()}")
```

### 7. 重试回调

```python
from mod import RetryConfig, RetryExecutor
import logging

def on_retry(attempt, exception, delay):
    logging.warning(
        f"Retry {attempt}: {type(exception).__name__} - {exception}. "
        f"Waiting {delay:.2f}s"
    )

config = RetryConfig(
    max_retries=3,
    base_delay=1.0,
    on_retry=on_retry,
)

executor = RetryExecutor(config)
executor.execute(risky_operation)
```

---

## 🔧 预设配置

```python
from mod import (
    RETRY_NETWORK,    # 网络请求重试
    RETRY_DATABASE,   # 数据库操作重试
    RETRY_API,        # API 调用重试
    RETRY_QUICK,      # 快速重试（低延迟场景）
)

# 使用预设配置
@retry(**RETRY_NETWORK.__dict__)
def network_call():
    pass
```

### 预设配置详情

| 配置 | 最大重试 | 基础延迟 | 适用场景 |
|------|---------|---------|----------|
| `RETRY_NETWORK` | 3 | 1.0s | 网络请求、HTTP 调用 |
| `RETRY_DATABASE` | 5 | 0.5s | 数据库连接、查询 |
| `RETRY_API` | 3 | 2.0s | 第三方 API 调用 |
| `RETRY_QUICK` | 2 | 0.1s | 低延迟内部服务 |

---

## 📊 退避策略

```python
from mod import BackoffStrategies

# 恒定延迟
constant = BackoffStrategies.constant(delay=2.0)

# 线性退避
linear = BackoffStrategies.linear(base_delay=1.0, max_delay=60.0)

# 指数退避（推荐）
exponential = BackoffStrategies.exponential(
    base_delay=1.0,
    max_delay=60.0,
    jitter=True,
)

# 斐波那契退避
fibonacci = BackoffStrategies.fibonacci(max_delay=60.0)
```

---

## 🧪 运行测试

```bash
cd retry_utils
python retry_utils_test.py -v
```

### 测试覆盖

- ✅ RetryError 异常类
- ✅ RetryStats 统计类
- ✅ RetryConfig 配置类
- ✅ RetryExecutor 执行器
- ✅ @retry 装饰器
- ✅ retry_with_config 函数
- ✅ BackoffStrategies 策略
- ✅ 预设配置常量
- ✅ 便捷异常类
- ✅ 线程安全
- ✅ 超时控制
- ✅ 回调机制
- ✅ 边界情况
- ✅ 集成测试

---

## ⚠️ 注意事项

1. **重试风暴**: 生产环境务必启用 jitter 防止重试同步
2. **超时设置**: 始终设置合理的 timeout 避免无限重试
3. **异常过滤**: 明确指定 retryable_exceptions，避免重试不可恢复错误
4. **幂等性**: 确保重试操作是幂等的，避免副作用
5. **资源泄漏**: 重试时注意清理资源（连接、文件句柄等）
6. **监控告警**: 使用 stats 追踪重试率，设置告警阈值

---

## 💡 最佳实践

### 1. 选择合适的重试次数

```python
# 外部 API：较多重试
@retry(max_retries=5, base_delay=2.0)
def external_api():
    pass

# 内部服务：较少重试
@retry(max_retries=2, base_delay=0.5)
def internal_service():
    pass
```

### 2. 区分异常类型

```python
# 只重试瞬态错误
@retry(retryable_exceptions=(
    ConnectionError,
    TimeoutError,
    NetworkError,
))
def make_request():
    pass

# 不重试业务错误（如 404、400）
```

### 3. 添加监控

```python
stats = RetryStats()
config = RetryConfig(stats=stats, on_retry=log_retry)

def check_health():
    if stats.success_rate < 0.5:
        alert("High failure rate!")
```

### 4. 使用装饰器简化代码

```python
# 推荐：装饰器
@retry(max_retries=3)
def fetch():
    pass

# 不推荐：手动重试循环
for i in range(4):
    try:
        return fetch()
    except:
        if i == 3:
            raise
        time.sleep(1)
```

---

## 📁 文件结构

```
retry_utils/
├── mod.py                      # 主要实现
├── retry_utils_test.py         # 测试套件 (80+ 测试用例)
├── README.md                   # 本文档
└── examples/
    ├── basic_usage.py          # 基础使用示例 (10 个)
    └── advanced_example.py     # 高级使用示例 (7 个)
```

---

## 🔗 相关资源

- 指数退避算法：https://en.wikipedia.org/wiki/Exponential_backoff
- 重试模式：https://docs.microsoft.com/en-us/azure/architecture/patterns/retry
- 断路器模式：https://docs.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

仓库：https://github.com/ayukyo/alltoolkit
