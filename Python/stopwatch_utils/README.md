# StopWatch Utils - 秒表计时工具模块

提供精确计时、性能测量、多计时器管理等功能。零外部依赖，纯 Python 标准库实现。

## 安装

```python
from stopwatch_utils.mod import StopWatch, LapTimer, Timer, PerformanceTimer
```

## 核心功能

### 1. StopWatch - 精确秒表

```python
from stopwatch_utils.mod import StopWatch

# 基本用法
sw = StopWatch()
sw.start()
# ... 执行代码 ...
print(f"耗时: {sw.elapsed_str()}")  # 自动选择合适单位
sw.pause()   # 暂停
sw.resume()  # 恢复
sw.reset()   # 重置

# 上下文管理器
with StopWatch() as sw:
    # ... 执行代码 ...
    pass
print(f"耗时: {sw.elapsed_str()}")

# 不同时间单位
sw.elapsed('seconds')      # 秒
sw.elapsed('milliseconds') # 毫秒
sw.elapsed('microseconds') # 微秒
sw.elapsed('minutes')      # 分钟
sw.elapsed('hours')        # 小时
```

### 2. LapTimer - 圈计时器

```python
from stopwatch_utils.mod import LapTimer

timer = LapTimer(auto_start=True)
time.sleep(0.8)
timer.lap("第一圈")
time.sleep(0.6)
timer.lap("第二圈")

# 获取统计
print(timer.summary())
# 输出: 总计时间、圈数、平均圈时、最快/最慢圈等
```

### 3. Timer - 倒计时器

```python
from stopwatch_utils.mod import Timer

def on_timeout():
    print("时间到!")

timer = Timer(10.0, callback=on_timeout)  # 10秒倒计时
timer.start()
timer.pause()   # 暂停
timer.resume()  # 恢复
timer.cancel()  # 取消
timer.remaining()  # 剩余时间
```

### 4. PerformanceTimer - 性能测量

```python
from stopwatch_utils.mod import PerformanceTimer

# 单次测量
with PerformanceTimer("数据库查询"):
    # ... 执行代码 ...
    pass

# 多次测量
perf = PerformanceTimer("API调用")
for _ in range(10):
    with perf.measure():
        # ... 执行代码 ...
        pass

print(perf.summary())
# 输出: 测量次数、总时间、平均时间、最短/最长时间
```

### 5. 计时装饰器

```python
from stopwatch_utils.mod import timed, timed_async

@timed("数据处理")
def process_data(size):
    # ... 处理数据 ...
    return result
# 自动打印: [数据处理] 耗时: 123.456 ms

@timed_async("异步操作")
async def async_operation():
    await asyncio.sleep(1)
    return "done"
```

### 6. 便捷函数

```python
from stopwatch_utils.mod import measure_time, countdown

# 测量函数执行时间
result, elapsed = measure_time(slow_function, arg1, arg2)
print(f"结果: {result}, 耗时: {elapsed:.3f}s")

# 倒计时
countdown(10, callback=lambda s: print(f"剩余 {s} 秒"))
```

## API 参考

### StopWatch

| 方法 | 说明 |
|------|------|
| `start()` | 启动秒表 |
| `pause()` | 暂停秒表 |
| `resume()` | 恢复秒表 |
| `reset()` | 重置秒表 |
| `elapsed(unit)` | 获取已用时间 |
| `elapsed_str()` | 获取格式化时间字符串 |
| `is_running` | 是否正在运行 |
| `is_paused` | 是否已暂停 |

### LapTimer (继承 StopWatch)

| 方法 | 说明 |
|------|------|
| `lap(label)` | 记录一圈 |
| `get_laps()` | 获取所有圈记录 |
| `get_fastest_lap()` | 获取最快圈 |
| `get_slowest_lap()` | 获取最慢圈 |
| `get_average_lap()` | 获取平均圈时 |
| `summary()` | 生成摘要 |

### Timer

| 方法 | 说明 |
|------|------|
| `start()` | 启动倒计时 |
| `pause()` | 暂停倒计时 |
| `resume()` | 恢复倒计时 |
| `cancel()` | 取消倒计时 |
| `remaining()` | 获取剩余时间 |
| `is_running` | 是否正在运行 |

### PerformanceTimer

| 方法 | 说明 |
|------|------|
| `measure()` | 上下文管理器，测量代码块 |
| `elapsed()` | 最近一次测量时间 |
| `count()` | 测量次数 |
| `total()` | 总时间 |
| `average()` | 平均时间 |
| `min_time()` | 最短时间 |
| `max_time()` | 最长时间 |
| `statistics()` | 统计数据字典 |
| `summary()` | 摘要字符串 |

## 特点

- **零依赖**: 仅使用 Python 标准库
- **高精度**: 使用 `time.perf_counter()` 实现
- **线程安全**: Timer 类支持多线程
- **灵活**: 支持多种时间单位
- **易用**: 支持上下文管理器和装饰器