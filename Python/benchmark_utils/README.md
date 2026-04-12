# AllToolkit - Python Benchmark Utils ⏱️

**零依赖性能基准测试工具 - 生产就绪**

---

## 📖 概述

`benchmark_utils` 提供功能完整的性能基准测试和测量解决方案。支持高精度计时、统计分析、多实现对比和报告生成。完全使用 Python 标准库实现，无需任何外部依赖。

---

## ✨ 特性

- **高精度计时** - 使用 `perf_counter()` 实现纳秒级精度
- **统计分析** - 自动计算平均值、中位数、标准差、方差
- **LRU 淘汰** - 自动淘汰最少使用条目
- **多线程安全** - 支持并发基准测试
- **对比分析** - 多实现性能对比，计算相对性能
- **装饰器支持** - `@benchmark` 一键测试函数性能
- **上下文管理器** - `with measure_time()` 简洁计时
- **报告导出** - 支持 JSON 和 Markdown 格式导出
- **性能分析器** - 长期追踪函数调用性能
- **内存分析** - 可选的内存使用分析（tracemalloc）

---

## 🚀 快速开始

### 基础使用

```python
from mod import BenchmarkRunner

# 创建运行器
runner = BenchmarkRunner(warmup_iterations=3, verbose=True)

# 定义要测试的函数
def my_function():
    return sum(range(1000))

# 运行基准测试
result = runner.run(
    "sum_test",
    my_function,
    iterations=1000,
)

# 查看结果
print(f"平均时间：{result.avg_time*1000:.3f}ms")
print(f"每秒操作：{result.ops_per_sec:.2f}")
```

### 使用装饰器

```python
from mod import benchmark

@benchmark(name="cached_sum", iterations=1000)
def cached_sum():
    return sum(range(1000))

# 调用函数（自动运行基准测试）
result = cached_sum()

# 查看基准结果
bench_result = cached_sum.benchmark_result()
print(bench_result)
```

### 对比多个实现

```python
from mod import BenchmarkRunner

runner = BenchmarkRunner(warmup_iterations=3)

# 定义多个实现
def impl_for_loop():
    total = 0
    for i in range(1000):
        total += i
    return total

def impl_sum():
    return sum(range(1000))

def impl_reduce():
    from functools import reduce
    return reduce(lambda x, y: x + y, range(1000))

# 运行对比
comparison = runner.run_comparison({
    'for_loop': impl_for_loop,
    'sum': impl_sum,
    'reduce': impl_reduce,
}, iterations=1000)

# 设置基线并查看相对性能
comparison.set_baseline('sum')
relative = comparison.get_relative_performance()
print(relative)  # {'for_loop': 0.5, 'sum': 1.0, 'reduce': 0.8}
```

---

## 📚 API 参考

### Timer 类

高精度计时器。

```python
from mod import Timer

# 手动使用
timer = Timer()
timer.start()
# ... 执行代码 ...
timer.stop()
print(f"耗时：{timer.elapsed_ms:.3f}ms")

# 上下文管理器
with Timer() as timer:
    # ... 执行代码 ...
print(f"耗时：{timer.elapsed_ms:.3f}ms")
```

**属性：**
- `elapsed` - 经过时间（秒）
- `elapsed_ms` - 经过时间（毫秒）

### BenchmarkResult 类

单次基准测试结果。

**属性：**
- `name` - 基准测试名称
- `iterations` - 迭代次数
- `times` - 每次迭代的时间列表
- `total_time` - 总时间
- `avg_time` - 平均时间
- `min_time` - 最短时间
- `max_time` - 最长时间
- `median_time` - 中位数时间
- `std_dev` - 标准差
- `variance` - 方差
- `ops_per_sec` - 每秒操作数
- `metadata` - 附加元数据

**方法：**
- `calculate_stats()` - 计算统计数据
- `to_dict()` - 转换为字典

### BenchmarkRunner 类

主要基准测试运行器。

**构造函数参数：**
- `warmup_iterations` - 预热迭代次数（默认：1）
- `verbose` - 是否打印结果（默认：True）

**方法：**
- `run(name, func, iterations, args, kwargs, warmup, metadata)` - 运行基准测试
- `run_comparison(benchmarks, iterations, args, kwargs)` - 运行多个基准对比
- `get_result(name)` - 获取指定结果
- `get_all_results()` - 获取所有结果
- `export_json(filepath)` - 导出为 JSON
- `export_markdown(filepath)` - 导出为 Markdown
- `clear()` - 清除所有结果

### 装饰器

#### @benchmark

```python
from mod import benchmark

@benchmark(name="my_test", iterations=1000, warmup=3)
def my_function():
    return 42
```

**参数：**
- `name` - 基准测试名称（默认：函数名）
- `iterations` - 迭代次数（默认：1000）
- `warmup` - 预热次数（默认：1）
- `runner` - BenchmarkRunner 实例（可选）

### 上下文管理器

#### measure_time

带输出的计时上下文管理器。

```python
from mod import measure_time

with measure_time("Database Query"):
    result = db.query("SELECT * FROM users")
# 输出：⏱ Database Query: 45.231ms
```

#### measure_time_silent

静默计时上下文管理器。

```python
from mod import measure_time_silent

with measure_time_silent() as timer:
    result = expensive_operation()

if timer.elapsed > 1.0:
    print(f"警告：操作耗时 {timer.elapsed:.2f}s")
```

### time_func 函数

快速计时单个函数。

```python
from mod import time_func

def slow_function():
    time.sleep(0.1)

result, elapsed = time_func(slow_function, iterations=10)
print(f"总耗时：{elapsed*1000:.3f}ms")
```

### PerformanceProfiler 类

长期性能追踪器。

```python
from mod import PerformanceProfiler

profiler = PerformanceProfiler()

@profiler.profile(name="api_call")
def api_call():
    # ... API 调用 ...
    pass

# 多次调用
for _ in range(100):
    api_call()

# 查看统计
stats = profiler.get_stats("api_call")
print(f"调用次数：{stats['count']}")
print(f"平均耗时：{stats['avg']*1000:.3f}ms")
print(f"最慢调用：{stats['max']*1000:.3f}ms")
```

### compare_implementations 函数

便捷对比函数。

```python
from mod import compare_implementations

def impl1(data):
    return sorted(data)

def impl2(data):
    data.sort()
    return data

comparison = compare_implementations(
    {'sorted': impl1, 'sort': impl2},
    test_data=[3, 1, 4, 1, 5, 9, 2, 6],
    iterations=100,
)
```

---

## 📊 报告导出

### JSON 导出

```python
runner = BenchmarkRunner()
runner.run("test", lambda: sum(range(1000)), iterations=1000)
runner.export_json("benchmark_results.json")
```

**输出示例：**
```json
{
  "timestamp": "2026-04-10T18:00:00.000000",
  "results": {
    "test": {
      "name": "test",
      "iterations": 1000,
      "total_time": 0.045,
      "avg_time": 0.000045,
      "min_time": 0.000042,
      "max_time": 0.000051,
      "ops_per_sec": 22222.22
    }
  }
}
```

### Markdown 导出

```python
runner.export_markdown("benchmark_report.md")
```

**输出示例：**
```markdown
# Benchmark Results

Generated: 2026-04-10 18:00:00

## Summary

| Benchmark | Iterations | Avg (ms) | Min (ms) | Max (ms) | Ops/sec |
|-----------|------------|----------|----------|----------|---------|
| test | 1000 | 0.045 | 0.042 | 0.051 | 22222.22 |
```

---

## 🎯 使用场景

### 1. 算法性能对比

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

comparison = compare_implementations(
    {'bubble': bubble_sort, 'quick': quick_sort},
    test_data=[3, 6, 8, 10, 1, 2, 1],
    iterations=100,
)
```

### 2. API 响应时间监控

```python
profiler = PerformanceProfiler()

@profiler.profile(name="user_api")
def get_user(user_id):
    return requests.get(f"/api/users/{user_id}")

@profiler.profile(name="order_api")
def get_orders(user_id):
    return requests.get(f"/api/users/{user_id}/orders")

# 生产环境中调用
for user_id in user_ids:
    get_user(user_id)
    get_orders(user_id)

# 定期查看性能
stats = profiler.get_all_stats()
for name, s in stats.items():
    if s['avg'] > 0.5:  # 超过 500ms 告警
        print(f"⚠️ {name} 平均响应时间过长：{s['avg']*1000:.0f}ms")
```

### 3. 优化前后对比

```python
# 优化前
def process_data_v1(data):
    result = []
    for item in data:
        processed = expensive_transform(item)
        if processed is not None:
            result.append(processed)
    return result

# 优化后
def process_data_v2(data):
    return [
        processed for item in data
        if (processed := expensive_transform(item)) is not None
    ]

runner = BenchmarkRunner()
runner.run("v1", process_data_v1, iterations=1000, args=(test_data,))
runner.run("v2", process_data_v2, iterations=1000, args=(test_data,))

runner.export_markdown("optimization_comparison.md")
```

---

## 🔧 最佳实践

### 1. 适当的预热

```python
# 推荐：至少 1-3 次预热
runner = BenchmarkRunner(warmup_iterations=3)

# JIT 编译的语言（如 PyPy）需要更多预热
runner = BenchmarkRunner(warmup_iterations=10)
```

### 2. 足够的迭代次数

```python
# 快速函数：1000+ 次迭代
runner.run("fast", fast_func, iterations=10000)

# 慢速函数：10-100 次迭代
runner.run("slow", slow_func, iterations=50)
```

### 3. 隔离测试环境

```python
# 避免在基准测试中做其他事情
def clean_benchmark():
    # 不要在测试函数中打印或做 I/O
    return sum(range(1000))

# 关闭 verbose 以减少输出干扰
runner = BenchmarkRunner(verbose=False)
```

### 4. 统计显著性

```python
result = runner.run("test", func, iterations=1000)

# 检查标准差
if result.std_dev / result.avg_time > 0.1:  # 变异系数 > 10%
    print("⚠️ 结果波动较大，建议增加迭代次数")

# 使用中位数作为参考（对异常值更鲁棒）
print(f"中位数时间：{result.median_time*1000:.3f}ms")
```

---

## 🧪 运行测试

```bash
cd /path/to/benchmark_utils
python benchmark_utils_test.py
```

测试覆盖：
- Timer 类基本功能
- BenchmarkResult 统计计算
- BenchmarkComparison 对比分析
- BenchmarkRunner 完整流程
- 装饰器功能
- 上下文管理器
- 性能分析器
- 线程安全性
- 边界情况处理

---

## 📝 示例代码

查看 `examples/` 目录获取更多使用示例：

- `basic_usage.py` - 基础使用示例
- `comparison.py` - 多实现对比
- `profiling.py` - 长期性能追踪
- `export.py` - 报告导出示例

---

## ⚖️ 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！
