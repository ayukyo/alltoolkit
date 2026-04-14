# Debounce Utilities - 防抖与节流工具

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

零依赖、生产就绪的防抖（Debounce）和节流（Throttle）工具模块。

## 功能特性

### Debouncer（防抖器）
- **延迟执行**：在指定等待时间后才执行函数
- **前缘执行**：在第一次调用时立即执行
- **后缘执行**：在等待时间结束后执行
- **取消与刷新**：支持取消待执行的调用或立即执行
- **统计信息**：追踪调用、执行、取消次数

### Throttler（节流器）
- **固定间隔执行**：限制函数在指定时间间隔内只执行一次
- **前缘/后缘模式**：支持在间隔开始或结束时执行
- **取消与刷新**：支持取消或立即执行

### 高级功能
- **多键支持**：MultiKeyDebouncer 和 MultiKeyThrottler
- **装饰器模式**：`@debounce` 和 `@throttle` 装饰器
- **线程安全**：所有操作都是线程安全的

## 安装

```bash
# 直接使用
from debounce_utils import Debouncer, Throttler, debounce, throttle

# 或安装为包
pip install alltoolkit-debounce-utils
```

## 快速开始

### 基本防抖

```python
from debounce_utils import Debouncer

# 创建防抖器（等待0.5秒后执行）
debouncer = Debouncer(wait_seconds=0.5)

def save_data(data):
    print(f"保存数据: {data}")

# 多次调用只会执行最后一次
debouncer.call(save_data, "数据1")
debouncer.call(save_data, "数据2")
debouncer.call(save_data, "数据3")  # 只有这次会执行
```

### 基本节流

```python
from debounce_utils import Throttler

# 创建节流器（每秒最多执行一次）
throttler = Throttler(interval_seconds=1.0)

def update_ui():
    print("更新UI")

# 快速调用多次，但每秒只执行一次
for _ in range(10):
    throttler.call(update_ui)
```

### 装饰器用法

```python
from debounce_utils import debounce, throttle

@debounce(wait_seconds=0.3)
def search(query):
    print(f"搜索: {query}")

@throttle(interval_seconds=1.0)
def track_event(event_name):
    print(f"追踪事件: {event_name}")
```

### 前缘执行

```python
from debounce_utils import Debouncer

# 第一次调用立即执行，后续调用被忽略
debouncer = Debouncer(wait_seconds=1.0, leading=True)

def handle_click():
    print("处理点击")

# 立即执行
debouncer.call(handle_click)
```

### 多键防抖

```python
from debounce_utils import MultiKeyDebouncer

multi_debouncer = MultiKeyDebouncer(wait_seconds=0.5)

# 不同键独立防抖
multi_debouncer.call("user1", callback1)
multi_debouncer.call("user2", callback2)  # 独立的防抖周期
```

## API 参考

### Debouncer

```python
Debouncer(
    wait_seconds: float,        # 等待时间（秒）
    leading: bool = False,      # 是否在前缘执行
    trailing: bool = True,      # 是否在后缘执行
    max_wait: float = None      # 最大等待时间
)
```

**方法**:
- `call(func, *args, **kwargs)` - 调用防抖函数
- `cancel()` - 取消待执行的调用
- `flush()` - 立即执行待执行的调用
- `pending()` - 检查是否有待执行的调用
- `get_stats()` - 获取统计信息

### Throttler

```python
Throttler(
    interval_seconds: float,    # 间隔时间（秒）
    leading: bool = True,       # 是否在前缘执行
    trailing: bool = True        # 是否在后缘执行
)
```

**方法**:
- `call(func, *args, **kwargs)` - 调用节流函数
- `cancel()` - 取消待执行的调用
- `flush()` - 立即执行待执行的调用

### 装饰器

```python
@debounce(wait_seconds: float, leading: bool = False, trailing: bool = True)
@throttle(interval_seconds: float, leading: bool = True, trailing: bool = True)
```

## 使用场景

| 场景 | 推荐工具 | 说明 |
|------|----------|------|
| 搜索框输入 | Debouncer | 用户停止输入后再搜索 |
| 窗口调整大小 | Debouncer | 用户停止调整后再重新布局 |
| 按钮点击防抖 | Debouncer + leading=True | 首次点击立即响应 |
| 滚动事件 | Throttler | 限制处理频率 |
| API 请求限制 | Throttler | 控制请求频率 |
| 实时数据更新 | Throttler | 固定间隔更新UI |

## 测试

```bash
python debounce_utils_test.py
```

## 许可证

MIT License