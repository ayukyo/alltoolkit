# Fenwick Tree Utils - 树状数组工具库

树状数组（Fenwick Tree / Binary Indexed Tree）是一种高效的数据结构，用于处理前缀和查询和动态更新。

## 特点

- **高效**: 前缀和查询 O(log n)，单点更新 O(log n)
- **零依赖**: 纯 Python 标准库实现
- **多功能**: 支持多种扩展形式

## 功能列表

### 核心类

| 类 | 描述 |
|---|---|
| `FenwickTree` | 基本树状数组，支持单点更新、前缀和/区间和查询 |
| `FenwickTreeRangeUpdate` | 区间更新树状数组，支持 O(log n) 区间加值 |
| `FenwickTree2D` | 二维树状数组，支持矩阵前缀和/区间和查询 |
| `FenwickTreeMax` | 最大值树状数组，支持前缀最大值查询 |
| `FenwickTreeMin` | 最小值树状数组，支持前缀最小值查询 |

### 便捷函数

| 函数 | 描述 |
|---|---|
| `create_fenwick_tree(data)` | 从数据创建树状数组 |
| `fenwick_prefix_sums(data)` | 计算所有前缀和 |
| `fenwick_range_sums(data, queries)` | 批量计算区间和 |
| `count_inversions(arr)` | 计算逆序对数量 |
| `find_kth_element(ft, k)` | 查找第 k 小元素 |

## 使用示例

### 基本操作

```python
from fenwick_tree_utils.mod import FenwickTree

# 创建树状数组
ft = FenwickTree([1, 2, 3, 4, 5])

# 前缀和查询
print(ft.prefix_sum(2))  # 6 (前三个元素的和)

# 区间和查询
print(ft.range_sum(1, 3))  # 9 (第2-4元素的和)

# 单点更新
ft.add(0, 10)  # 第一个元素加10
print(ft.prefix_sum(0))  # 11
```

### 区间更新

```python
from fenwick_tree_utils.mod import FenwickTreeRangeUpdate

ft = FenwickTreeRangeUpdate(5)
ft.range_add(0, 2, 10)  # [10, 10, 10, 0, 0]
ft.range_add(1, 4, 5)   # [10, 15, 15, 5, 5]

print(ft.get(1))  # 15
print(ft.range_sum(0, 4))  # 50
```

### 二维树状数组

```python
from fenwick_tree_utils.mod import FenwickTree2D

ft = FenwickTree2D(4, 4)
ft.add(1, 1, 10)
ft.add(2, 2, 20)

print(ft.prefix_sum(2, 2))  # 30
print(ft.range_sum(0, 0, 2, 2))  # 30
```

### 逆序对计数

```python
from fenwick_tree_utils.mod import count_inversions

arr = [5, 4, 3, 2, 1]
print(count_inversions(arr))  # 10 (完全逆序)
```

## 时间复杂度

| 操作 | FenwickTree | FenwickTreeRangeUpdate | FenwickTree2D |
|---|---|---|---|
| 构建 | O(n) | O(1) | O(1) |
| 前缀和 | O(log n) | O(log n) | O(log m × log n) |
| 单点更新 | O(log n) | - | O(log m × log n) |
| 区间更新 | O(n log n) | O(log n) | - |
| 区间和 | O(log n) | O(log n) | O(log m × log n) |

## 作者

AllToolkit Contributors

## 许可证

MIT License