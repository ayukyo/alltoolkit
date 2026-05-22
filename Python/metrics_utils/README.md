# Metrics Utils - 应用程序指标收集工具

提供 Counter、Gauge、Histogram、Summary、Meter 等核心指标类型，支持指标注册、导出、时间窗口统计等功能。类似 Prometheus metrics 的轻量级实现，零外部依赖。

## 功能特性

### 核心指标类型

- **Counter** - 计数器：只增不减的累计值（请求数、错误数等）
- **Gauge** - 仪表盘：可增可减的瞬时值（温度、内存使用等）
- **Histogram** - 直方图：观测值分布统计（延迟、响应大小等）
- **Summary** - 摘要：流式分位数计算（支持时间窗口）
- **Meter** - 计量器：速率测量（QPS、TPS 等）

### 其他功能

- 指标标签支持
- 指标注册表管理
- Prometheus 格式导出
- JSON 格式导出
- 线程安全
- 时间窗口统计
- 滑动窗口历史记录
- 上下文管理器（自动计时、跟踪进行中任务）

## 安装

```python
# 直接导入使用，零依赖
from metrics_utils.mod import Counter, Gauge, Histogram, Summary, Meter, MetricsRegistry
```

## 快速开始

### 基本使用

```python
from metrics_utils.mod import Counter, Gauge, Histogram

# 创建计数器
requests_counter = Counter('http_requests_total', 'Total HTTP requests')
requests_counter.inc()  # +1
requests_counter.inc(5)  # +5
print(f"Total requests: {requests_counter.value}")

# 创建仪表盘
memory_gauge = Gauge('memory_usage_bytes', 'Current memory usage')
memory_gauge.set(1024 * 1024)  # 设置为 1MB
memory_gauge.inc(100)  # 增加 100
memory_gauge.dec(50)  # 减少 50

# 创建直方图
latency_histogram = Histogram(
    'request_latency_seconds',
    'Request latency in seconds',
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0]
)
latency_histogram.observe(0.42)
latency_histogram.observe(1.23)
print(f"Average latency: {latency_histogram.get_mean():.3f}s")
print(f"P95 latency: {latency_histogram.get_quantile(0.95):.3f}s")
```

### 使用标签

```python
from metrics_utils.mod import Counter

# 创建带标签的计数器
counter = Counter('http_requests_total', 'Total HTTP requests')

# 为不同方法创建标签实例
get_counter = counter.with_labels(method='GET', path='/api')
post_counter = counter.with_labels(method='POST', path='/api')

get_counter.inc(10)
post_counter.inc(5)
```

### 使用注册表

```python
from metrics_utils.mod import MetricsRegistry

# 创建注册表（带命名空间）
registry = MetricsRegistry(namespace='myapp', subsystem='http')

# 注册指标
requests = registry.counter('requests_total', 'Total requests')
latency = registry.histogram('latency_seconds', 'Request latency')
memory = registry.gauge('memory_bytes', 'Memory usage')

# 使用指标
requests.inc()
latency.observe(0.5)
memory.set(1024 * 1024)

# 导出为 Prometheus 格式
print(registry.export_prometheus())

# 导出为 JSON 格式
data = registry.export_json()
print(data)
```

### 便捷函数

```python
from metrics_utils.mod import counter, gauge, histogram, meter, export_prometheus

# 使用默认注册表的便捷函数
c = counter('requests_total', 'Total requests')
c.inc(100)

g = gauge('memory_usage', 'Memory usage')
g.set(1024)

h = histogram('latency', 'Request latency')
h.observe(0.5)

m = meter('qps', 'Queries per second')
m.mark()

# 导出所有指标
print(export_prometheus())
```

## 详细用法

### Counter - 计数器

```python
from metrics_utils.mod import Counter

# 创建计数器
counter = Counter('errors_total', 'Total errors', labels={'service': 'api'})

# 增加计数
counter.inc()      # +1
counter.inc(5)     # +5
counter.inc(0.5)   # +0.5

# 获取当前值
print(counter.value)

# 获取快照
snapshot = counter.snapshot()
print(f"{snapshot.name}: {snapshot.value}")

# 重置
counter.reset()
```

### Gauge - 仪表盘

```python
from metrics_utils.mod import Gauge

# 创建仪表盘
gauge = Gauge('temperature', 'Current temperature')

# 设置值
gauge.set(25.5)

# 增减值
gauge.inc(2)   # 增加
gauge.dec(1)   # 减少

# 设置为当前时间戳
gauge.set_to_current_time()

# 获取历史记录
gauge.set(10)
gauge.set(20)
gauge.set(30)
history = gauge.get_history()
for point in history:
    print(f"{point.timestamp}: {point.value}")

# 跟踪进行中的任务
with gauge.track_inprogress():
    # 在此处 gauge 值 +1
    do_something()
# 离开上下文后 gauge 值 -1

# 计时
with gauge.time():
    do_something()
# gauge 值被设置为执行时间
```

### Histogram - 直方图

```python
from metrics_utils.mod import Histogram

# 创建直方图（自定义桶）
hist = Histogram(
    'response_size_bytes',
    'Response size in bytes',
    buckets=[100, 500, 1000, 5000, 10000, float('inf')]
)

# 记录观测值
hist.observe(150)
hist.observe(800)
hist.observe(5000)

# 获取统计
print(f"Count: {hist.get_count()}")
print(f"Sum: {hist.get_sum()}")
print(f"Mean: {hist.get_mean()}")

# 获取分位数
print(f"P50: {hist.get_quantile(0.5)}")
print(f"P90: {hist.get_quantile(0.9)}")
print(f"P95: {hist.get_quantile(0.95)}")

# 获取多个百分位数
percentiles = hist.get_percentiles([50, 90, 95, 99])
print(percentiles)

# 获取桶计数
buckets = hist.get_bucket_counts()
print(buckets)

# 计时
with hist.time():
    do_something()
# 自动记录执行时间
```

### Summary - 摘要

```python
from metrics_utils.mod import Summary

# 创建摘要（自定义分位数）
summary = Summary(
    'request_duration_seconds',
    'Request duration',
    quantiles=[0.5, 0.75, 0.9, 0.95, 0.99],
    max_age=60.0  # 观测值最多保留 60 秒
)

# 记录观测值
summary.observe(0.42)
summary.observe(1.23)

# 获取统计
print(f"Count: {summary.get_count()}")
print(f"Mean: {summary.get_mean()}")

# 获取分位数
quantiles = summary.get_quantiles()
print(f"Median: {quantiles[0.5]}")
print(f"P95: {quantiles[0.95]}")

# 计时
with summary.time():
    do_something()
```

### Meter - 计量器

```python
from metrics_utils.mod import Meter

# 创建计量器
meter = Meter('requests_per_second', 'Request rate', window_size=60.0)

# 记录事件
meter.mark()      # +1
meter.mark(10)    # +10

# 获取速率
print(f"Rate: {meter.get_rate():.2f}/s")

# 获取总计数
print(f"Total: {meter.get_count()}")

# 获取时间窗口内的事件数
print(f"Window count: {meter.get_window_count()}")
```

### MetricsRegistry - 注册表

```python
from metrics_utils.mod import MetricsRegistry

# 创建注册表
registry = MetricsRegistry(namespace='myapp', subsystem='api')

# 注册各种指标
counter = registry.counter('requests_total', 'Total requests')
gauge = registry.gauge('connections', 'Active connections')
histogram = registry.histogram('latency_seconds', 'Request latency')
summary = registry.summary('response_time', 'Response time')
meter = registry.meter('qps', 'Queries per second')

# 获取已注册的指标
metric = registry.get_metric('requests_total')

# 获取所有指标
all_metrics = registry.get_all_metrics()

# 获取所有快照
snapshots = registry.get_all_snapshots()

# Prometheus 格式导出
prom_output = registry.export_prometheus()
print(prom_output)

# JSON 格式导出
json_data = registry.export_json()
print(json_data)

# 重置所有指标
registry.reset_all()
```

## API 参考

### Counter

| 方法 | 描述 |
|------|------|
| `inc(amount)` | 增加计数（amount 必须为正） |
| `labels(**kwargs)` | 创建带标签的实例 |
| `reset()` | 重置计数器 |
| `snapshot()` | 获取快照 |

属性：`name`, `description`, `value`

### Gauge

| 方法 | 描述 |
|------|------|
| `set(value)` | 设置值 |
| `inc(amount)` | 增加值 |
| `dec(amount)` | 减少值 |
| `set_to_current_time()` | 设置为当前时间戳 |
| `track_inprogress()` | 跟踪进行中任务的上下文管理器 |
| `time()` | 计时的上下文管理器 |
| `labels(**kwargs)` | 创建带标签的实例 |
| `get_history(since)` | 获取历史记录 |
| `reset()` | 重置仪表盘 |
| `snapshot()` | 获取快照 |

属性：`name`, `description`, `value`

### Histogram

| 方法 | 描述 |
|------|------|
| `observe(value)` | 记录观测值 |
| `time()` | 计时的上下文管理器 |
| `labels(**kwargs)` | 创建带标签的实例 |
| `get_count()` | 获取观测次数 |
| `get_sum()` | 获取观测值总和 |
| `get_mean()` | 获取平均值 |
| `get_quantile(q)` | 获取分位数（0-1） |
| `get_percentiles(percentiles)` | 获取多个百分位数 |
| `get_bucket_counts()` | 获取桶计数 |
| `reset()` | 重置直方图 |
| `snapshot()` | 获取快照 |

属性：`name`, `description`

### Summary

| 方法 | 描述 |
|------|------|
| `observe(value)` | 记录观测值 |
| `time()` | 计时的上下文管理器 |
| `labels(**kwargs)` | 创建带标签的实例 |
| `get_count()` | 获取观测次数 |
| `get_sum()` | 获取观测值总和 |
| `get_mean()` | 获取平均值 |
| `get_quantile(q)` | 获取分位数（0-1） |
| `get_quantiles()` | 获取所有配置的分位数 |
| `reset()` | 重置摘要 |
| `snapshot()` | 获取快照 |

属性：`name`, `description`

### Meter

| 方法 | 描述 |
|------|------|
| `mark(count)` | 记录事件 |
| `labels(**kwargs)` | 创建带标签的实例 |
| `get_rate()` | 获取当前速率（事件/秒） |
| `get_count()` | 获取总事件数 |
| `get_window_count()` | 获取时间窗口内的事件数 |
| `reset()` | 重置计量器 |
| `snapshot()` | 获取快照 |

属性：`name`, `description`

### MetricsRegistry

| 方法 | 描述 |
|------|------|
| `counter(name, description, labels)` | 注册计数器 |
| `gauge(name, description, labels)` | 注册仪表盘 |
| `histogram(name, description, buckets, labels)` | 注册直方图 |
| `summary(name, description, quantiles, labels)` | 注册摘要 |
| `meter(name, description, window_size, labels)` | 注册计量器 |
| `get_metric(name)` | 获取已注册的指标 |
| `get_all_metrics()` | 获取所有指标 |
| `get_all_snapshots()` | 获取所有快照 |
| `export_prometheus()` | 导出为 Prometheus 格式 |
| `export_json()` | 导出为 JSON 格式 |
| `reset_all()` | 重置所有指标 |

### 便捷函数

```python
counter(name, description, labels) -> Counter
gauge(name, description, labels) -> Gauge
histogram(name, description, buckets, labels) -> Histogram
summary(name, description, quantiles, labels) -> Summary
meter(name, description, window_size, labels) -> Meter
export_prometheus() -> str
export_json() -> dict
get_default_registry() -> MetricsRegistry
set_default_registry(registry) -> None
```

## Prometheus 导出格式

```python
from metrics_utils.mod import MetricsRegistry

registry = MetricsRegistry(namespace='app')
registry.counter('requests_total', 'Total requests').inc(100)
registry.gauge('memory_bytes', 'Memory usage').set(1024)
registry.histogram('latency_seconds', 'Latency').observe(0.5)

print(registry.export_prometheus())
```

输出示例：

```
# HELP app_requests_total Total requests
# TYPE app_requests_total counter
app_requests_total 100

# HELP app_memory_bytes Memory usage
# TYPE app_memory_bytes gauge
app_memory_bytes 1024

# HELP app_latency_seconds Latency
# TYPE app_latency_seconds histogram
app_latency_seconds_count 1
app_latency_seconds_sum 0.5
app_latency_seconds_bucket{le="0.005"} 0
app_latency_seconds_bucket{le="0.01"} 0
...
app_latency_seconds_bucket{le="+Inf"} 1
```

## 使用示例

### Web 服务监控

```python
from metrics_utils.mod import MetricsRegistry, Histogram, Counter

registry = MetricsRegistry(namespace='webapp', subsystem='http')

# 请求计数
request_counter = registry.counter('requests_total', 'Total HTTP requests')
error_counter = registry.counter('errors_total', 'Total HTTP errors')

# 响应延迟
latency_hist = registry.histogram('latency_seconds', 'Request latency')

# 活跃连接
active_connections = registry.gauge('active_connections', 'Active connections')

def handle_request(request):
    request_counter.with_labels(method=request.method, path=request.path).inc()
    
    with active_connections.track_inprogress():
        with latency_hist.time():
            try:
                return process_request(request)
            except Exception:
                error_counter.with_labels(type='server_error').inc()
                raise
```

### 性能基准测试

```python
from metrics_utils.mod import Histogram, Meter
import time

# 执行时间
exec_time = Histogram('execution_time', 'Execution time', 
                      buckets=[0.001, 0.01, 0.1, 1.0, 10.0])

# 执行速率
exec_rate = Meter('execution_rate', 'Execution rate', window_size=10.0)

def benchmark(func, iterations=1000):
    for _ in range(iterations):
        start = time.time()
        func()
        elapsed = time.time() - start
        exec_time.observe(elapsed)
        exec_rate.mark()
    
    print(f"Total: {exec_time.get_count()}")
    print(f"Mean: {exec_time.get_mean():.4f}s")
    print(f"P50: {exec_time.get_quantile(0.5):.4f}s")
    print(f"P95: {exec_time.get_quantile(0.95):.4f}s")
    print(f"Rate: {exec_rate.get_rate():.2f}/s")
```

### 任务队列监控

```python
from metrics_utils.mod import MetricsRegistry

registry = MetricsRegistry(namespace='queue')

# 队列大小
queue_size = registry.gauge('size', 'Current queue size')

# 处理统计
processed = registry.counter('processed_total', 'Total processed tasks')
failed = registry.counter('failed_total', 'Total failed tasks')

# 处理时间
process_time = registry.summary('process_time_seconds', 'Task processing time',
                                quantiles=[0.5, 0.9, 0.95, 0.99])

# 处理速率
process_rate = registry.meter('process_rate', 'Processing rate')

def process_task(task):
    queue_size.inc()  # 任务入队
    
    with process_time.time():
        try:
            do_process(task)
            processed.inc()
        except Exception:
            failed.inc()
        finally:
            queue_size.dec()  # 任务出队
            process_rate.mark()
```

## 测试

```bash
cd Python/metrics_utils
python metrics_utils_test.py
```

测试覆盖：
- Counter、Gauge、Histogram、Summary、Meter 所有功能
- MetricsRegistry 注册和导出
- 线程安全
- 上下文管理器
- 标签支持
- 便捷函数
- 边界情况处理

## 依赖

无外部依赖，仅使用 Python 标准库。

## 作者

AllToolkit

## 版本

1.0.0