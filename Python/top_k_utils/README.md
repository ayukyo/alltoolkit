# Top-K 工具集 (Top-K Utilities)

提供全面的 Top-K 问题解决方案，零外部依赖，纯 Python 实现。

## 功能特性

### 基础算法

- **堆方法 Top-K** - `top_k_heap()` - O(n log k) 时间复杂度，适合 k << n
- **QuickSelect Top-K** - `top_k_quickselect()` - 平均 O(n) 时间复杂度，适合 k 较大
- **排序方法 Top-K** - `top_k_sort()` - O(n log n)，最简单直接

### 流式处理

- **StreamingTopK** - 流式 Top-K 处理器，实时维护 Top-K，内存 O(k)

### 频繁元素（Heavy Hitters）

- **FrequentItems** - Space-Saving 算法，高效追踪频繁元素，内存 O(k)
- **TopKFrequent** - 精确版本，完整统计所有元素频率

### 分布式合并

- `merge_top_k()` - 合并多个分片的 Top-K 结果
- `merge_top_k_weighted()` - 带权重的 Top-K 合并

### 特殊用途

- `top_k_unique()` - Top-K 唯一元素（去重）
- `top_k_with_threshold()` - 超过阈值的所有元素
- `top_k_percentile()` - 位于指定百分位的元素

### 工具函数

- `nth_element()` - 第 n 大/小元素（QuickSelect）
- `median()` - 计算中位数

## 快速开始

```python
from top_k_utils.mod import top_k_heap, StreamingTopK, FrequentItems

# 基本用法 - 找最大的3个元素
data = [3, 1, 4, 1, 5, 9, 2, 6]
print(top_k_heap(data, 3))  # [9, 6, 5]

# 找最小的3个元素
print(top_k_heap(data, 3, largest=False))  # [1, 1, 2]

# 流式处理
stream = StreamingTopK(3)
for x in [3, 1, 4, 1, 5, 9, 2, 6]:
    stream.add(x)
print(stream.get_top_k())  # [9, 6, 5]

# 频繁元素统计
freq = FrequentItems(3)
freq.add_all([1, 1, 1, 2, 2, 3, 4, 5])
print(freq.get_top_k())  # [(1, 3), (2, 2), (3, 1)]
```

## 使用示例

### 基础 Top-K 算法

```python
from top_k_utils.mod import top_k_heap, top_k_quickselect, top_k_sort

data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

# 堆方法 - O(n log k)，适合 k 较小
print(top_k_heap(data, 3))  # [9, 6, 5]

# QuickSelect - 平均 O(n)，适合 k 较大
result = top_k_quickselect(data, 5)
print(sorted(result, reverse=True))  # [9, 6, 5, 5, 5]

# 排序方法 - 最简单，适合小数据集
print(top_k_sort(data, 3))  # [9, 6, 5]
```

### 自定义键函数

```python
from top_k_utils.mod import top_k_heap

# 按对象的某个属性排序
students = [
    {'name': 'Alice', 'score': 85},
    {'name': 'Bob', 'score': 92},
    {'name': 'Charlie', 'score': 78},
    {'name': 'Diana', 'score': 95},
]

# 找成绩最高的3个学生
top_students = top_k_heap(students, 3, key=lambda x: x['score'])
for s in top_students:
    print(f"{s['name']}: {s['score']}")  # Diana: 95, Bob: 92, Alice: 85
```

### 流式 Top-K 处理

```python
from top_k_utils.mod import StreamingTopK

# 实时维护最大的10个元素
stream = StreamingTopK(10)

# 模拟数据流
import random
for _ in range(1000):
    stream.add(random.randint(1, 10000))

# 获取当前 Top-K
print(stream.get_top_k())  # 当前最大的10个元素

# 支持批量添加
stream.add_all(iter(range(10001, 10005)))
print(stream.get_top_k())  # 更新后的 Top-K
```

### 频繁元素统计（Heavy Hitters）

```python
from top_k_utils.mod import FrequentItems, TopKFrequent

# Space-Saving 算法 - 内存高效，适合大数据流
freq = FrequentItems(1000)  # 只追踪1000个最频繁元素
freq.add_all([1, 1, 1, 2, 2, 3, 4, 5, 1, 2, 1])
print(freq.get_top_k(3))  # [(1, 5), (2, 3), (3, 1)]

# 精确版本 - 适合元素种类不多的场景
exact_freq = TopKFrequent()
exact_freq.add_all(['apple', 'banana', 'apple', 'orange', 'banana', 'apple'])
print(exact_freq.get_top_k(2))  # [('apple', 3), ('banana', 2)]
print(exact_freq.get_frequency('apple'))  # 3
print(exact_freq.get_unique_count())  # 3 种不同水果
```

### 分布式 Top-K 合并

```python
from top_k_utils.mod import merge_top_k, merge_top_k_weighted

# 合并多个分片的 Top-K 结果（分布式场景）
 shard1 = [98, 95, 90]
 shard2 = [99, 87, 85]
 shard3 = [100, 92, 88]

global_top_k = merge_top_k([shard1, shard2, shard3], 5)
print(global_top_k)  # [100, 99, 98, 95, 92]

# 带权重的合并（不同数据源重要性不同）
weighted_merge = merge_top_k_weighted([
    ([100, 90], 1.0),    # 权重 1.0
    ([95, 85], 2.0),     # 权重 2.0（更重要）
], 2)
print(weighted_merge)  # 按加权值排序
```

### 特殊用途 Top-K

```python
from top_k_utils.mod import top_k_unique, top_k_with_threshold, top_k_percentile

data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 9]

# 唯一元素 Top-K（忽略重复）
print(top_k_unique(data, 3))  # [9, 6, 5]

# 超过阈值的所有元素
print(top_k_with_threshold(data, 5))  # [9, 9, 6, 5, 5]

# 位于80百分位之上的元素
print(top_k_percentile([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 80))  # [9, 10]
```

### 工具函数

```python
from top_k_utils.mod import nth_element, median

data = [3, 1, 4, 1, 5, 9, 2, 6]

# 第3大的元素
print(nth_element(data, 3))  # 5

# 中位数
print(median([1, 2, 3, 4, 5]))  # 3.0
print(median([1, 2, 3, 4]))    # 2.5
```

## 算法选择指南

| 场景 | 推荐算法 | 原因 |
|------|----------|------|
| k << n (k很小) | `top_k_heap` | O(n log k)，内存仅 O(k) |
| k ≈ n (k较大) | `top_k_quickselect` | 平均 O(n)，效率更高 |
| 数据流/实时 | `StreamingTopK` | 在线算法，随时查询 |
| 频繁元素 | `FrequentItems` | Space-Saving，内存高效 |
| 小数据集 | `top_k_sort` | 最简单，一行搞定 |
| 分布式 | `merge_top_k` | 分片合并 |

## 时间复杂度对比

| 方法 | 时间复杂度 | 空间复杂度 | 特点 |
|------|------------|------------|------|
| `top_k_heap` | O(n log k) | O(k) | k 小时最优 |
| `top_k_quickselect` | O(n) 平均 | O(n) | k 大时最优 |
| `top_k_sort` | O(n log n) | O(n) | 最简单 |
| `StreamingTopK` | O(log k) per item | O(k) | 流式处理 |
| `FrequentItems` | O(1) per item | O(k) | Heavy Hitters |

## API 参考

### 基础函数

#### `top_k_heap(data, k, key=None, largest=True)`
使用堆方法找出 Top-K 元素。

#### `top_k_quickselect(data, k, key=None, largest=True)`
使用 QuickSelect 算法找出 Top-K 元素。

#### `top_k_sort(data, k, key=None, largest=True)`
使用排序找出 Top-K 元素。

### StreamingTopK 类

| 方法 | 描述 |
|------|------|
| `add(item)` | 添加元素，返回是否加入 Top-K |
| `add_all(items)` | 批量添加 |
| `get_top_k(sorted_=True)` | 获取 Top-K 结果 |
| `__len__()` | 当前堆大小 |

### FrequentItems 类

| 方法 | 描述 |
|------|------|
| `add(item, count=1)` | 添加元素（可指定计数） |
| `add_all(items)` | 批量添加 |
| `get_top_k(sorted_=True)` | 获取 Top-K 频繁元素 |
| `get_frequency(item)` | 获取某元素估计频率 |
| `get_total()` | 总计数 |

### TopKFrequent 类

| 方法 | 描述 |
|------|------|
| `add(item, count=1)` | 添加元素 |
| `get_top_k(k)` | 获取 Top-K 频繁元素 |
| `get_frequency(item)` | 获取精确频率 |
| `get_all()` | 获取所有元素频率 |
| `get_unique_count()` | 唯一元素数量 |

## 测试

```bash
# 运行所有测试
python -m pytest top_k_utils_test.py -v

# 或直接运行
python top_k_utils_test.py
```

## 许可证

MIT License