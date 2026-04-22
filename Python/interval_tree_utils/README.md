# Interval Tree Utils - 区间树工具模块

[English](#english) | [中文](#中文)

---

## 中文

### 概述

`interval_tree_utils` 是一个高效的区间树（Interval Tree）实现，用于快速查询区间重叠、点包含等问题。零外部依赖，纯 Python 实现。

### 核心功能

- **区间管理**：插入、删除、批量创建区间
- **点查询**：查找包含指定点的所有区间
- **重叠查询**：查找与指定区间重叠的所有区间
- **包含查询**：查找包含/被包含指定区间的区间
- **空白检测**：找出范围内未被覆盖的空白区域

### 安装

```python
# 无需安装，直接导入使用
from interval_tree_utils import IntervalTree, Interval
```

### 快速开始

```python
from interval_tree_utils import IntervalTree, Interval

# 创建区间树
tree = IntervalTree()

# 插入区间
tree.insert(Interval(1, 10, value="区间A"))
tree.insert(Interval(5, 15, value="区间B"))
tree.insert(Interval(20, 30, value="区间C"))

# 点查询
results = tree.query_point(7)
print([r.value for r in results])  # ['区间A', '区间B']

# 重叠查询
results = tree.query_overlaps(Interval(8, 25))
print([r.value for r in results])  # ['区间A', '区间B', '区间C']
```

### API 参考

#### Interval 类

| 方法 | 说明 |
|------|------|
| `Interval(start, end, value=None)` | 创建区间 |
| `overlaps(other)` | 检查是否与另一区间重叠 |
| `contains(other)` | 检查是否包含另一区间 |
| `contains_point(point)` | 检查是否包含指定点 |
| `intersection(other)` | 返回交集区间 |
| `union(other)` | 返回并集区间（需相邻或重叠） |
| `length` | 区间长度 |
| `center` | 区间中心点 |

#### IntervalTree 类

| 方法 | 说明 |
|------|------|
| `insert(interval)` | 插入区间 |
| `remove(interval)` | 移除区间 |
| `query_point(point)` | 查询包含指定点的所有区间 |
| `query_overlaps(interval)` | 查询与指定区间重叠的所有区间 |
| `query_contains(interval)` | 查询完全包含指定区间的区间 |
| `query_contained_by(interval)` | 查询被指定区间完全包含的区间 |
| `find_first_overlapping(interval)` | 查找第一个重叠区间 |
| `find_all_gaps(start, end)` | 找出空白区域 |
| `clear()` | 清空区间树 |
| `to_list()` | 转为区间列表 |
| `get_statistics()` | 获取统计信息 |
| `from_tuples(tuples)` | 从元组列表创建（类方法） |

### 时间复杂度

| 操作 | 平均时间复杂度 |
|------|--------------|
| 插入 | O(log n) |
| 删除 | O(log n) |
| 点查询 | O(log n + k) |
| 重叠查询 | O(log n + k) |

其中 n 为区间总数，k 为结果数量。

### 应用场景

1. **会议调度**：检测时间冲突
2. **资源分配**：管理资源使用时段
3. **基因组分析**：基因区域重叠查询
4. **日历管理**：事件冲突检测
5. **IP地址管理**：地址段分配和查询

### 测试

```bash
python -m pytest interval_tree_utils/test_interval_tree.py -v
```

---

## English

### Overview

`interval_tree_utils` is an efficient Interval Tree implementation for fast interval overlap and point containment queries. Zero external dependencies, pure Python implementation.

### Core Features

- **Interval Management**: Insert, delete, and bulk create intervals
- **Point Query**: Find all intervals containing a specific point
- **Overlap Query**: Find all intervals overlapping with a given interval
- **Containment Query**: Find intervals that contain/are contained by a given interval
- **Gap Detection**: Find uncovered gaps within a range

### Installation

```python
# No installation needed, just import
from interval_tree_utils import IntervalTree, Interval
```

### Quick Start

```python
from interval_tree_utils import IntervalTree, Interval

# Create interval tree
tree = IntervalTree()

# Insert intervals
tree.insert(Interval(1, 10, value="Interval A"))
tree.insert(Interval(5, 15, value="Interval B"))
tree.insert(Interval(20, 30, value="Interval C"))

# Point query
results = tree.query_point(7)
print([r.value for r in results])  # ['Interval A', 'Interval B']

# Overlap query
results = tree.query_overlaps(Interval(8, 25))
print([r.value for r in results])  # ['Interval A', 'Interval B', 'Interval C']
```

### API Reference

#### Interval Class

| Method | Description |
|--------|-------------|
| `Interval(start, end, value=None)` | Create an interval |
| `overlaps(other)` | Check if overlaps with another interval |
| `contains(other)` | Check if contains another interval |
| `contains_point(point)` | Check if contains a point |
| `intersection(other)` | Return intersection interval |
| `union(other)` | Return union interval (must be adjacent or overlapping) |
| `length` | Interval length |
| `center` | Interval center point |

#### IntervalTree Class

| Method | Description |
|--------|-------------|
| `insert(interval)` | Insert an interval |
| `remove(interval)` | Remove an interval |
| `query_point(point)` | Find all intervals containing the point |
| `query_overlaps(interval)` | Find all intervals overlapping with given interval |
| `query_contains(interval)` | Find intervals that fully contain the given interval |
| `query_contained_by(interval)` | Find intervals fully contained by the given interval |
| `find_first_overlapping(interval)` | Find first overlapping interval |
| `find_all_gaps(start, end)` | Find uncovered gaps |
| `clear()` | Clear the tree |
| `to_list()` | Convert to list of intervals |
| `get_statistics()` | Get tree statistics |
| `from_tuples(tuples)` | Create from list of tuples (class method) |

### Time Complexity

| Operation | Average Time Complexity |
|-----------|------------------------|
| Insert | O(log n) |
| Delete | O(log n) |
| Point Query | O(log n + k) |
| Overlap Query | O(log n + k) |

Where n is the total number of intervals and k is the number of results.

### Use Cases

1. **Meeting Scheduling**: Detect time conflicts
2. **Resource Allocation**: Manage resource usage periods
3. **Genomic Analysis**: Gene region overlap queries
4. **Calendar Management**: Event conflict detection
5. **IP Address Management**: Address range allocation and queries

### Testing

```bash
python -m pytest interval_tree_utils/test_interval_tree.py -v
```

### License

MIT License

### Author

AllToolkit

### Date

2026-04-22