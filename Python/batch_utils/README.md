# batch_utils - 批处理工具模块

提供多种批处理策略，用于将大数据集分批处理。
零外部依赖，纯 Python 标准库实现。

## 功能列表

| 功能 | 说明 |
|------|------|
| `batched()` | 固定大小分批（类似 itertools.batched） |
| `chunked()` | 均匀分块（分成 N 个块） |
| `sliding_window()` | 滑动窗口遍历 |
| `BatchProcessor` | 带回调的批处理队列 |
| `TimeWindowBatcher` | 时间窗口批处理 |
| `ParallelBatchProcessor` | 并行批处理 |
| `BatchAggregator` | 结果聚合器 |
| `AdaptiveBatcher` | 自适应批处理 |
| `process_in_batches()` | 便捷批处理函数 |
| `batch_by_key()` | 按键分组批处理 |

## 快速开始

### 简单分批

```python
from batch_utils import batched

# 固定大小分批
for batch in batched([1, 2, 3, 4, 5], size=2):
    print(batch)
# [1, 2], [3, 4], [5]

# 丢弃不完整批次
for batch in batched([1, 2, 3, 4, 5], size=2, drop_last=True):
    print(batch)
# [1, 2], [3, 4]
```

### 均匀分块

```python
from batch_utils import chunked

# 分成 3 个块
for chunk in chunked([1, 2, 3, 4, 5, 6], 3):
    print(chunk)
# [1, 2], [3, 4], [5, 6]
```

### 滑动窗口

```python
from batch_utils import sliding_window

# 滑动窗口遍历
for window in sliding_window([1, 2, 3, 4, 5], size=3):
    print(window)
# [1, 2, 3], [2, 3, 4], [3, 4, 5]

# 带步长
for window in sliding_window([1, 2, 3, 4, 5], size=3, step=2):
    print(window)
# [1, 2, 3], [3, 4, 5]
```

### 批处理器

```python
from batch_utils import BatchProcessor

# 创建批处理器
processor = BatchProcessor(
    handler=lambda batch: sum(batch),
    batch_size=10,
    auto_flush=True
)

# 添加数据
processor.add_many([1, 2, 3, 4, 5])
processor.flush()  # 手动刷新
```

### 时间窗口批处理

```python
from batch_utils import TimeWindowBatcher

# 创建时间窗口批处理器
batcher = TimeWindowBatcher(
    handler=lambda batch: print(f"处理 {len(batch)} 项"),
    window_seconds=5,
    max_size=100
)

batcher.add(1)
batcher.add(2)
# 5 秒后或达到 100 项时自动触发处理
```

### 并行批处理

```python
from batch_utils import ParallelBatchProcessor

# 并行处理
processor = ParallelBatchProcessor(
    handler=lambda batch: process_item(batch),
    batch_size=10,
    max_workers=4
)

results = processor.process(items)
```

## 测试覆盖

- **53 个单元测试，100% 通过率**
- 测试内容：
  - 基本分批、边界值（空输入、单个元素）
  - 时间窗口、并行处理
  - 错误处理、上下文管理器
  - 自适应批处理

## API 参考

### `batched(iterable, size, drop_last=False)`

将可迭代对象按固定大小分批。

**参数：**
- `iterable`: 可迭代对象
- `size`: 每批大小（必须 >= 1）
- `drop_last`: 是否丢弃最后不完整的批次

**异常：**
- `ValueError`: 当 size < 1 时抛出

### `chunked(iterable, n_chunks)`

将可迭代对象均匀分成 N 个块。

**参数：**
- `iterable`: 可迭代对象
- `n_chunks`: 块数（必须 >= 1）

### `sliding_window(iterable, size, step=1)`

滑动窗口遍历。

**参数：**
- `iterable`: 可迭代对象
- `size`: 窗口大小
- `step`: 步长

## 许可证

MIT License