# Prefix Sum Utils (前缀和与差分数组工具模块)

高效的前缀和与差分数组数据结构，用于区间查询和区间更新操作。零外部依赖，纯 Python 实现。

## 功能特性

### 一维前缀和 (PrefixSum)
- **O(1)** 区间求和查询
- 支持 `prefix_sum(index)` 计算 [0, index] 的和
- 支持 `range_sum(left, right)` 计算 [left, right] 的和
- 支持负数和浮点数

### 二维前缀和 (PrefixSum2D)
- **O(1)** 矩阵区域求和查询
- 支持 `region_sum(row1, col1, row2, col2)` 矩形区域求和
- 支持行和列单独求和
- 适用于图像处理、矩阵统计等场景

### 一维差分数组 (DifferenceArray)
- **O(1)** 区间更新
- 支持 `range_add(left, right, value)` 区间加值
- 支持 `point_add(index, value)` 单点加值
- 支持 **链式调用**，便于多次操作
- **O(n)** 还原数组

### 二维差分数组 (DifferenceArray2D)
- **O(1)** 矩阵区域更新
- 支持 `region_add(row1, col1, row2, col2, value)` 区域加值
- 支持 **链式调用**
- **O(n*m)** 还原矩阵

## 安装

无需安装，直接导入 `mod.py` 即可使用。

## 快速开始

### 一维前缀和

```python
from mod import PrefixSum

# 创建前缀和数组
arr = [1, 2, 3, 4, 5]
ps = PrefixSum(arr)

# 计算区间和
print(ps.range_sum(0, 2))  # 6 (1+2+3)
print(ps.range_sum(1, 4))  # 14 (2+3+4+5)

# 计算前缀和
print(ps.prefix_sum(3))  # 10 (1+2+3+4)

# 获取总和
print(ps.total())  # 15
```

### 二维前缀和

```python
from mod import PrefixSum2D

# 创建二维前缀和
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
ps2d = PrefixSum2D(matrix)

# 计算矩形区域和
print(ps2d.region_sum(0, 0, 1, 1))  # 12 (1+2+4+5)
print(ps2d.region_sum(1, 1, 2, 2))  # 28 (5+6+8+9)

# 计算行和、列和
print(ps2d.row_sum(0))  # 6 (1+2+3)
print(ps2d.col_sum(0))  # 12 (1+4+7)
```

### 一维差分数组

```python
from mod import DifferenceArray

# 从现有数组创建
da = DifferenceArray([1, 2, 3, 4, 5])

# 区间加值
da.range_add(1, 3, 10)  # 在 [1, 3] 区间每个元素加 10
print(da.to_array())  # [1, 12, 13, 14, 5]

# 支持链式调用
da2 = DifferenceArray(size=5)
result = (da2
    .range_add(0, 2, 1)
    .range_add(2, 4, 2)
    .point_add(3, 5)
    .to_array())
print(result)  # [1, 1, 3, 7, 2]
```

### 二维差分数组

```python
from mod import DifferenceArray2D

# 创建 3x3 差分数组
da2d = DifferenceArray2D(rows=3, cols=3)

# 区域加值
da2d.region_add(0, 0, 1, 1, 5)  # 左上角 2x2 区域加 5
da2d.region_add(1, 1, 2, 2, 10)  # 右下角 2x2 区域加 10

# 还原矩阵
result = da2d.to_matrix()
# [[5, 5, 0],
#  [5, 15, 10],  # 中心重叠区域 5+10=15
#  [0, 10, 10]]
```

### 便捷函数

```python
from mod import build_prefix_sum, range_sum, build_difference_array, restore_from_difference

# 快速构建前缀和数组
prefix = build_prefix_sum([1, 2, 3, 4, 5])
print(prefix)  # [0, 1, 3, 6, 10, 15]

# 使用前缀和数组计算区间和
print(range_sum(prefix, 1, 3))  # 9 (2+3+4)

# 快速构建差分数组
diff = build_difference_array([1, 3, 6, 10, 15])
print(diff)  # [1, 2, 3, 4, 5]

# 从差分数组还原
original = restore_from_difference(diff)
print(original)  # [1, 3, 6, 10, 15]
```

## API 文档

### PrefixSum

| 方法 | 说明 | 时间复杂度 |
|------|------|-----------|
| `__init__(arr)` | 从数组构建前缀和 | O(n) |
| `length` | 返回数组长度 | O(1) |
| `total()` | 返回总和 | O(1) |
| `prefix_sum(index)` | 计算 [0, index] 的和 | O(1) |
| `range_sum(left, right)` | 计算 [left, right] 的和 | O(1) |
| `original` | 返回原始数组的副本 | O(n) |
| `prefix_array` | 返回前缀和数组 | O(n) |

### PrefixSum2D

| 方法 | 说明 | 时间复杂度 |
|------|------|-----------|
| `__init__(matrix)` | 从矩阵构建二维前缀和 | O(n*m) |
| `rows`, `cols` | 返回矩阵行列数 | O(1) |
| `shape` | 返回矩阵形状 (rows, cols) | O(1) |
| `total()` | 返回总和 | O(1) |
| `prefix_sum(row, col)` | 计算 [0,0] 到 [row,col] 的和 | O(1) |
| `region_sum(r1, c1, r2, c2)` | 计算矩形区域的和 | O(1) |
| `row_sum(row)` | 计算指定行的和 | O(1) |
| `col_sum(col)` | 计算指定列的和 | O(1) |

### DifferenceArray

| 方法 | 说明 | 时间复杂度 |
|------|------|-----------|
| `__init__(arr)` 或 `__init__(size=n)` | 从数组创建或创建指定大小 | O(n) |
| `range_add(left, right, value)` | 区间加值 | O(1) |
| `point_add(index, value)` | 单点加值 | O(1) |
| `to_array()` | 还原为数组 | O(n) |
| `reset(arr?)` | 重置差分数组 | O(n) |

### DifferenceArray2D

| 方法 | 说明 | 时间复杂度 |
|------|------|-----------|
| `__init__(matrix)` 或 `__init__(rows=n, cols=m)` | 从矩阵创建或创建指定大小 | O(n*m) |
| `rows`, `cols` | 返回矩阵行列数 | O(1) |
| `shape` | 返回矩阵形状 | O(1) |
| `region_add(r1, c1, r2, c2, value)` | 区域加值 | O(1) |
| `point_add(row, col, value)` | 单点加值 | O(1) |
| `to_matrix()` | 还原为矩阵 | O(n*m) |
| `reset()` | 重置差分数组 | O(n*m) |

## 应用场景

### 前缀和
- 区间求和查询（高频场景）
- 子数组和问题
- 二维矩阵区域统计
- 图像处理（积分图）
- 统计数据分析

### 差分数组
- 区间批量更新（高频场景）
- 差分前缀和问题
- 航班预订问题
- 时间区间调度
- 多次区间修改后一次性查询

## 复杂度分析

| 操作 | 前缀和 | 差分数组 |
|------|--------|---------|
| 构建 | O(n) / O(n*m) | O(n) / O(n*m) |
| 单点查询 | O(1) | O(n) / O(n*m) |
| 区间/区域查询 | O(1) | O(n) / O(n*m) |
| 单点更新 | O(n) / O(n*m) | O(1) |
| 区间/区域更新 | O(n) / O(n*m) | O(1) |

**选择建议**：
- 查询多、更新少 → 使用前缀和
- 更新多、查询少 → 使用差分数组
- 更新和查询都多 → 考虑线段树或树状数组

## 运行测试

```bash
python -m pytest prefix_sum_utils_test.py -v
```

或

```bash
python prefix_sum_utils_test.py
```

## 许可证

MIT License

## 作者

AllToolkit