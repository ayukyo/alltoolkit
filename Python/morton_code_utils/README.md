# Morton Code Utils

Morton编码工具（Z-order曲线）- 用于空间索引的多维坐标编码。

## 概述

Morton编码（又称Z-order曲线）是一种将多维坐标映射到一维值的技术。通过交替排列各坐标分量的二进制位，生成一个单一的Morton码。广泛应用于：

- **数据库索引** - 多维数据的快速范围查询
- **地理空间查询** - GPS坐标的邻居查找
- **图像处理** - 像素邻域操作、分块处理
- **游戏开发** - 格子地图的空间索引
- **科学计算** - 网格数据的局部性优化

## 特性

- ✅ 2D和3D坐标的Morton编码/解码
- ✅ 支持不同位宽（16位、32位、64位）
- ✅ 相邻区域查询（4邻域/8邻域）
- ✅ 层级结构操作（父/子节点）
- ✅ 范围编码支持
- ✅ Morton排序（空间局部性优化）
- ✅ **零外部依赖** - 仅使用Python标准库
- ✅ 完整的测试覆盖

## 快速开始

### 基础2D编码

```python
from mod import encode_2d, decode_2d

# 编码坐标
morton_code = encode_2d(100, 200)  # -> 6800

# 解码Morton码
x, y = decode_2d(6800)  # -> (100, 200)
```

### 基础3D编码

```python
from mod import encode_3d, decode_3d

# 编码3D坐标
morton_code = encode_3d(10, 20, 30)  # -> 混合码

# 解码3D Morton码
x, y, z = decode_3d(morton_code)  # -> (10, 20, 30)
```

### Morton排序

```python
from mod import sort_positions_2d

positions = [(10, 5), (3, 8), (7, 2), (1, 1)]
sorted_positions = sort_positions_2d(positions)
# Morton排序保持空间局部性，相邻的点在排序后通常仍然相邻
```

### 使用编码器类

```python
from mod import MortonEncoder2D

encoder = MortonEncoder2D(depth=10)  # 坐标范围 0-1023

# 编码
code = encoder.encode(100, 200)

# 解码
x, y = encoder.decode(code)

# 获取邻居
neighbors = encoder.get_neighbors(code)

# 获取范围内的所有码
codes = encoder.get_range_codes(0, 0, 10, 10)
```

## API参考

### 2D编码函数

| 函数 | 描述 | 示例 |
|------|------|------|
| `encode_2d(x, y)` | 编码2D坐标为Morton码 | `encode_2d(1, 1) -> 3` |
| `decode_2d(code)` | 解码Morton码为坐标 | `decode_2d(3) -> (1, 1)` |
| `encode_with_depth_2d(x, y, depth)` | 指定深度的编码 | `encode_with_depth_2d(100, 200, 10)` |
| `decode_with_depth_2d(code, depth)` | 指定深度的解码 | `decode_with_depth_2d(code, 10)` |

### 3D编码函数

| 函数 | 描述 | 示例 |
|------|------|------|
| `encode_3d(x, y, z)` | 编码3D坐标为Morton码 | `encode_3d(1, 1, 1) -> 7` |
| `decode_3d(code)` | 解码Morton码为坐标 | `decode_3d(7) -> (1, 1, 1)` |

### 邻居查询

| 函数 | 描述 | 示例 |
|------|------|------|
| `get_neighbors_2d(x, y, include_diagonal)` | 获取坐标邻居 | `get_neighbors_2d(5, 5)` |
| `get_neighbors_morton_2d(code, include_diagonal)` | 获取Morton码邻居 | `get_neighbors_morton_2d(7)` |

### 层级操作

| 函数 | 描述 | 示例 |
|------|------|------|
| `get_parent_2d(code)` | 获取父级Morton码 | `get_parent_2d(7) -> 1` |
| `get_children_2d(code)` | 获取所有子级码 | `get_children_2d(0) -> [0, 1, 2, 3]` |
| `is_ancestor_2d(ancestor, code)` | 检查祖先关系 | `is_ancestor_2d(0, 7) -> True` |
| `get_cell_level_2d(code)` | 获取单元层级 | `get_cell_level_2d(15) -> 2` |

### 范围和排序

| 函数 | 描述 | 示例 |
|------|------|------|
| `range_to_morton_codes_2d(x1, y1, x2, y2)` | 范围转Morton码列表 | `range_to_morton_codes_2d(0, 0, 3, 3)` |
| `sort_positions_2d(positions)` | Morton排序坐标列表 | `sort_positions_2d([(3,0), (0,0)])` |
| `compare_positions_2d(x1, y1, x2, y2)` | 比较空间顺序 | `compare_positions_2d(0, 0, 1, 0)` |

### 工具函数

| 函数 | 描述 | 示例 |
|------|------|------|
| `morton_code_to_binary_string(code)` | 转二进制字符串 | `morton_code_to_binary_string(5, 8)` |
| `morton_code_to_grid_position(code, size)` | 转网格位置 | `morton_code_to_grid_position(3, 4)` |
| `generate_morton_sequence_2d(count)` | 生成Morton序列 | `generate_morton_sequence_2d(16)` |
| `get_quadrant_2d(x, y, cx, cy)` | 判断象限 | `get_quadrant_2d(5, 5, 10, 10)` |

### 编码器类

#### MortonEncoder2D

```python
class MortonEncoder2D:
    def __init__(self, depth: int = 16): ...
    def encode(self, x: int, y: int) -> int: ...
    def decode(self, code: int) -> Tuple[int, int]: ...
    def get_neighbors(self, code: int) -> List[int]: ...
    def get_parent(self, code: int) -> int: ...
    def get_children(self, code: int) -> List[int]: ...
    def get_range_codes(self, x1, y1, x2, y2) -> List[int]: ...
```

#### MortonEncoder3D

```python
class MortonEncoder3D:
    def __init__(self, depth: int = 10): ...
    def encode(self, x: int, y: int, z: int) -> int: ...
    def decode(self, code: int) -> Tuple[int, int, int]: ...
```

## Morton编码原理

### 位交错

Morton编码通过交替排列坐标分量的二进制位来工作：

```
2D编码示例：
x = 01 (二进制)
y = 10 (二进制)
Morton码 = 011 (y0x0y1x1交错)

详细过程：
位位置:  5  4  3  2  1  0
x位:        x1    x0     (分散后)
y位:     y1    y0        (分散后)
结果:   y1 x1 y0 x0      (交错)
```

### Z字形填充

Morton编码产生Z字形的空间填充顺序：

```
深度1 (2x2网格):
0 → 1
    ↗
2 → 3

深度2 (4x4网格):
0→1  4→5
↓ ↗  ↓ ↗
2→3  6→7
      ↖ ↓
8→9 10→11
↓ ↗  ↓ ↗
12→13 14→15
```

这种填充顺序保证了相邻坐标的Morton码值也相近，有利于：
- 缓存优化（处理相邻数据）
- 范围查询（连续的码值范围）
- 数据压缩（相似值的压缩效率更高）

## 坐标范围

| 维度 | 默认深度 | 最大坐标值 | Morton码位数 |
|------|----------|------------|--------------|
| 2D | 16 | 65535 (0xFFFF) | 32位 |
| 3D | 10 | 1023 (0x3FF) | 30位 |

可通过 `depth` 参数调整范围：

```python
# 小范围应用
encoder = MortonEncoder2D(depth=8)  # 坐标范围 0-255

# 大范围应用
encoder = MortonEncoder2D(depth=20)  # 坐标范围 0-1048575
```

## 应用场景

### 1. 地理位置索引

```python
# 大量GPS坐标的快速邻居查找
locations = [(lat1, lon1), (lat2, lon2), ...]

# Morton排序后，相邻位置的数据在内存中也相邻
sorted_locations = sort_positions_2d(locations)

# 快速查找附近点
center_code = encode_2d(center_lat, center_lon)
neighbors = get_neighbors_morton_2d(center_code)
```

### 2. 图像分块处理

```python
# 将图像分成16块进行并行处理
blocks = list(generate_morton_sequence_2d(16))
# Morton顺序最大化缓存利用率

for code in blocks:
    row, col = morton_code_to_grid_position(code, 4)
    process_block(image[row*block_size:(row+1)*block_size, 
                        col*block_size:(col+1)*block_size])
```

### 3. 矩形范围查询

```python
# 查找矩形区域内的所有数据点
codes = range_to_morton_codes_2d(x_min, y_min, x_max, y_max)
# 这些码在数据库索引中可以快速检索
```

### 4. 游戏格子地图

```python
# 格子地图的空间索引
class GameMap:
    def __init__(self, size):
        self.encoder = MortonEncoder2D(depth=int(math.log2(size)))
    
    def get_nearby_units(self, x, y):
        code = self.encoder.encode(x, y)
        neighbor_codes = self.encoder.get_neighbors(code)
        return [self.units[c] for c in neighbor_codes if c in self.units]
```

## 测试

```bash
# 运行测试
python morton_code_utils_test.py

# 运行示例
python examples/usage_examples.py
```

测试覆盖：
- ✅ 位操作函数（分散/压缩）
- ✅ 2D编码解码（含边界值）
- ✅ 3D编码解码（含边界值）
- ✅ 邻居查询
- ✅ 层级操作
- ✅ 范围编码
- ✅ Morton排序
- ✅ 编码器类
- ✅ 性能测试

## 性能

- 2D编码/解码：约100万次/秒
- 3D编码/解码：约100万次/秒
- 位操作使用位运算技巧，效率极高

## 限制

1. 坐标必须为正整数（不支持负坐标）
2. 2D最大深度32位（坐标范围0-65535）
3. 3D最大深度10位（坐标范围0-1023）
4. Morton距离不是真实几何距离

## 参考资料

- [Morton order (Z-order curve)](https://en.wikipedia.org/wiki/Z-order_curve)
- [Geohash and related spatial indexing methods](https://en.wikipedia.org/wiki/Geohash)

## 许可证

MIT License