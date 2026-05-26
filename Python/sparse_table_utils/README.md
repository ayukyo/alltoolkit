# Sparse Table Utils - 稀疏表工具库

稀疏表（Sparse Table）是一种高效的静态区间查询数据结构，支持 O(1) 时间复杂度的区间最值、GCD 等查询。

## 特性

- **高效查询**: 预处理 O(n log n)，查询 O(1)
- **多种操作**: 支持 MIN、MAX、GCD、LCM、AND、OR、XOR
- **二维支持**: 提供二维稀疏表用于矩阵查询
- **不相交稀疏表**: 支持任意可结合操作（如求和）
- **零依赖**: 纯 Python 标准库实现
- **类型安全**: 完整的类型注解

## 安装

```python
from sparse_table_utils.mod import SparseTable, OperationType
```

## 快速开始

### 基本用法

```python
from sparse_table_utils.mod import SparseTable, OperationType

# 最小值查询
data = [3, 1, 4, 1, 5, 9, 2, 6]
st = SparseTable(data, OperationType.MIN)
print(st.query(0, 7))   # 输出: 1 (整个数组的最小值)
print(st.query(2, 5))   # 输出: 1 ([4, 1, 5, 9] 的最小值)

# 最大值查询
st_max = SparseTable(data, OperationType.MAX)
print(st_max.query(0, 7))  # 输出: 9

# GCD 查询
st_gcd = SparseTable([12, 18, 24, 36], OperationType.GCD)
print(st_gcd.query(0, 3))  # 输出: 6
```

### 使用构建器

```python
from sparse_table_utils.mod import SparseTableBuilder

st = (SparseTableBuilder()
      .with_data([5, 2, 8, 1, 9, 3])
      .for_min()
      .build())
print(st.query(0, 5))  # 输出: 1
```

### 便捷函数

```python
from sparse_table_utils.mod import range_min, range_max, range_gcd

# 一次性查询
print(range_min([3, 1, 4, 1, 5], 0, 4))   # 输出: 1
print(range_max([3, 1, 4, 1, 5], 0, 4))   # 输出: 5
print(range_gcd([12, 18, 24], 0, 2))       # 输出: 6
```

### 批量查询

```python
from sparse_table_utils.mod import batch_queries, OperationType

data = [3, 1, 4, 1, 5, 9, 2, 6]
queries = [(0, 3), (2, 5), (4, 7)]
results = batch_queries(data, queries, OperationType.MIN)
print(results)  # 输出: [1, 1, 2]
```

### 二维稀疏表

```python
from sparse_table_utils.mod import SparseTable2D, OperationType

matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16]
]

st2d = SparseTable2D(matrix, OperationType.MAX)
print(st2d.query(0, 0, 2, 2))  # 输出: 9 (左上角 3x3 子矩阵最大值)
```

### 不相交稀疏表（支持求和等操作）

```python
from sparse_table_utils.mod import DisjointSparseTable

# 求和操作
data = [1, 2, 3, 4, 5]
st = DisjointSparseTable(data, lambda a, b: a + b, 0)
print(st.query(0, 4))  # 输出: 15
print(st.query(1, 3))  # 输出: 9 (2 + 3 + 4)
```

## API 文档

### SparseTable

| 方法 | 说明 | 时间复杂度 |
|------|------|-----------|
| `__init__(data, op_type)` | 构造函数 | O(n log n) |
| `query(left, right)` | 区间查询 | O(1) |
| `range_min(left, right)` | 区间最小值 | O(1) |
| `range_max(left, right)` | 区间最大值 | O(1) |
| `range_gcd(left, right)` | 区间 GCD | O(1) |
| `data` | 获取原始数据 | - |
| `op_type` | 获取操作类型 | - |

### OperationType 枚举

- `MIN`: 最小值
- `MAX`: 最大值
- `GCD`: 最大公约数
- `LCM`: 最小公倍数
- `AND`: 按位与
- `OR`: 按位或
- `XOR`: 按位异或

### SparseTable2D

二维稀疏表，支持矩阵的矩形区域查询。

### DisjointSparseTable

不相交稀疏表，支持任意可结合操作，查询时间 O(log n)。

## 时间复杂度比较

| 数据结构 | 预处理 | 查询 | 更新 | 适用操作 |
|---------|--------|------|------|---------|
| Sparse Table | O(n log n) | O(1) | ❌ | 幂等操作 |
| Disjoint ST | O(n log n) | O(log n) | ❌ | 可结合操作 |
| Segment Tree | O(n) | O(log n) | O(log n) | 任意操作 |

## 使用场景

1. **静态 RMQ**: 当数据不修改时，稀疏表是最佳选择
2. **频繁查询**: 需要大量区间最值查询
3. **算法竞赛**: LCA、区间最值等问题
4. **数据分析**: 时间序列数据的最值统计

## 注意事项

- Sparse Table **不支持更新**，适用于静态数据
- 仅支持**可重复贡献操作**（幂等操作），如 min、max、gcd
- 对于求和等非幂等操作，请使用 `DisjointSparseTable` 或线段树

## 作者

AllToolkit 自动化生成

## 日期

2026-05-26