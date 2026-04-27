# Ring Buffer Utils


Ring Buffer Utils - 循环缓冲区工具集

提供循环缓冲区（环形缓冲区）的实现，适用于：
- 固定大小队列
- 滚动窗口统计
- 事件缓冲
- 数据流处理

特点：
- 零外部依赖
- 线程安全选项
- 支持迭代和切片
- 支持统计操作


## 功能

### 类

- **RingBuffer**: 循环缓冲区（环形缓冲区）

当缓冲区满时，新元素会覆盖最旧的元素。
支持随机访问、迭代和切片操作。

示例:
    >>> rb = RingBuffer[int](5)
    >>> rb
  方法: capacity, is_full, is_empty, append, extend ... (14 个方法)
- **NumericRingBuffer**: 数值型循环缓冲区

提供额外的统计功能：均值、方差、标准差、最大值、最小值等
  方法: append, clear, mean, variance, std_dev ... (10 个方法)
- **EventBuffer**: 事件缓冲区

带时间戳的事件缓冲，支持时间窗口查询和过期清理。
适用于事件日志、监控数据等场景。
  方法: add, get_events, get_event_data, cleanup_expired, count ... (6 个方法)

### 函数

- **create_ring_buffer(capacity, initial_data, thread_safe**) - 创建循环缓冲区的便捷函数
- **create_numeric_buffer(capacity, initial_data, thread_safe**) - 创建数值型循环缓冲区的便捷函数
- **sliding_window(data, window_size**) - 滑动窗口迭代器
- **batch_process(data, batch_size, processor**) - 批量处理数据
- **capacity(self**) - 缓冲区容量
- **is_full(self**) - 缓冲区是否已满
- **is_empty(self**) - 缓冲区是否为空
- **append(self, item**) - 添加一个元素
- **extend(self, items**) - 批量添加元素
- **appendleft(self, item**) - 在缓冲区开头添加元素（覆盖最新的元素）

... 共 34 个函数

## 使用示例

```python
from mod import create_ring_buffer

# 使用 create_ring_buffer
result = create_ring_buffer()
```

## 测试

运行测试：

```bash
python *_test.py
```

## 文件结构

```
{module_name}/
├── mod.py              # 主模块
├── *_test.py           # 测试文件
├── README.md           # 本文档
└── examples/           # 示例代码
    └── usage_examples.py
```

---

**Last updated**: 2026-04-28
