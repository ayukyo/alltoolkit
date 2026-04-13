# Circuit Breaker Utilities

熔断器（Circuit Breaker）工具模块，用于分布式系统的容错保护。

## 功能特性

- **三种状态**：CLOSED、OPEN、HALF_OPEN
- **可配置阈值**：连续失败阈值、失败率阈值
- **自动恢复**：超时后自动尝试恢复
- **指数退避**：支持可选的指数退避策略
- **事件监听**：完整的事件系统用于监控
- **装饰器模式**：简洁的函数保护方式
- **上下文管理器**：Pythonic 的使用方式
- **注册表管理**：多熔断器集中管理
- **异步支持**：AsyncCircuitBreaker 类
- **零外部依赖**：仅使用 Python 标准库

## 快速开始

### 基本使用

```python
from circuit_breaker_utils.mod import CircuitBreaker, CircuitOpenError

# 创建熔断器
breaker = CircuitBreaker(
    name="api_service",
    failure_threshold=3,    # 3次失败后熔断
    timeout=60.0,           # 60秒后尝试恢复
    success_threshold=2     # 半开状态下2次成功后关闭
)

# 使用 call 方法
try:
    result = breaker.call(lambda: api_request())
except CircuitOpenError:
    # 断器开启，请求被拒绝
    handle_failure()
```

### 装饰器模式

```python
@breaker.protect
def call_external_api():
    return api_client.get("/data")

# 使用
result = call_external_api()  # 自动受熔断器保护
```

### 上下文管理器

```python
with breaker:
    result = database.query()
```

## 状态说明

| 状态 | 说明 |
|------|------|
| CLOSED | 正常状态，所有请求正常执行 |
| OPEN | 熔断状态，请求被立即拒绝 |
| HALF_OPEN | 恢复测试状态，有限请求被允许执行 |

## 配置选项

```python
CircuitBreaker(
    name="service_name",
    
    # 失败阈值
    failure_threshold=5,          # 连续失败次数触发熔断
    failure_rate_threshold=0.5,   # 失败率阈值（可选）
    minimum_calls_for_rate=10,    # 计算失败率的最小调用次数
    
    # 恢复设置
    timeout=60.0,                 # 熔断后等待恢复的时间
    success_threshold=3,          # 半开状态下成功次数恢复到关闭
    half_open_max_calls=3,        # 半开状态允许的最大调用数
    
    # 指数退避
    exponential_backoff=False,    # 启用指数退避
    backoff_multiplier=2.0,       # 退避倍数
    max_timeout=300.0,            # 最大退避时间
    
    # 异常处理
    excluded_exceptions=(ValueError,),  # 不计入失败的异常
    include_exceptions=(ConnectionError,),  # 仅这些异常计入失败
)
```

## 事件系统

```python
# 监听状态变化
def on_state_change(event, state, details):
    print(f"State: {details['state_before']} -> {details['state_after']}")

breaker.on(CircuitEvent.STATE_CHANGE, on_state_change)

# 监听所有事件
breaker.on_any(lambda event, state, details: log_event(event))
```

可用事件：
- `STATE_CHANGE` - 状态变化
- `SUCCESS` - 成功调用
- `FAILURE` - 失败调用
- `REJECTION` - 请求被拒绝
- `TIMEOUT` - 调用超时
- `HALF_OPEN_SUCCESS` - 半开状态下成功
- `HALF_OPEN_FAILURE` - 半开状态下失败

## 注册表管理

```python
from circuit_breaker_utils.mod import get_registry

registry = get_registry()

# 创建多个熔断器
api_breaker = registry.get_or_create('api', failure_threshold=10)
db_breaker = registry.get_or_create('database', failure_threshold=5)

# 获取健康状态
health = registry.get_health()
for name, status in health.items():
    print(f"{name}: {status['state']}")
```

## 异步支持

```python
from circuit_breaker_utils.mod import AsyncCircuitBreaker

async_breaker = AsyncCircuitBreaker(failure_threshold=3)

@async_breaker.protect
async def async_api_call():
    await api_client.get_async("/data")

# 或者直接调用
result = await async_breaker.call(my_async_function)
```

## 生产模式示例

```python
breaker = CircuitBreaker(
    name="production_api",
    failure_threshold=3,
    timeout=30.0
)

def fallback_handler():
    return get_cached_data()

def call_with_fallback():
    if not breaker.allow_request():
        return fallback_handler()
    
    try:
        return breaker.call(lambda: api_request())
    except Exception:
        return fallback_handler()
```

## API 参考

### CircuitBreaker

| 方法 | 说明 |
|------|------|
| `call(func, *args, **kwargs)` | 执行受保护的函数 |
| `protect(func)` | 装饰器保护函数 |
| `allow_request()` | 检查是否允许请求 |
| `reset()` | 重置熔断器 |
| `force_open()` | 手动开启熔断器 |
| `force_close()` | 手动关闭熔断器 |
| `on(event, handler)` | 注册事件处理器 |
| `get_failure_history()` | 获取失败历史 |

### 属性

| 属性 | 说明 |
|------|------|
| `state` | 当前状态 |
| `stats` | 统计数据 |
| `config` | 配置信息 |
| `is_closed` | 是否关闭状态 |
| `is_open` | 是否开启状态 |
| `is_half_open` | 是否半开状态 |
| `time_until_retry` | 重试等待时间 |

## 文件结构

```
circuit_breaker_utils/
├── mod.py                  # 主模块
├── circuit_breaker_utils_test.py  # 测试文件
├── README.md               # 说明文档
└── examples/
    └── usage_examples.py   # 使用示例
```

## 运行测试

```bash
python circuit_breaker_utils_test.py
```

## 运行示例

```bash
python examples/usage_examples.py
```

## 许可证

MIT License - AllToolkit