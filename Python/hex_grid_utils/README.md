# Hex Grid Utils - 六边形网格工具

六边形坐标系统和网格操作工具集，零外部依赖，纯 Python 实现。

## 功能特性

### 基础坐标操作
- 六边形坐标类 `Hex` (轴向坐标)
- 坐标加减、缩放、取反运算
- 立方体坐标转换 `(x, y, z)`
- 支持两种朝向：尖顶 (POINTY_TOP) 和平顶 (FLAT_TOP)

### 方向和邻居
- 6 个方向的邻居获取
- 6 个对角邻居获取
- 方向索引和名称映射

### 距离计算
- 曼哈顿距离
- 切比雪夫距离

### 区域生成
- **圆形区域** `hex_range()` - 指定半径内的所有六边形
- **圆环** `hex_ring()` - 指定半径的边界
- **螺旋** `hex_spiral()` - 从中心向外螺旋排列
- **直线** `hex_line()` - 两点之间的直线
- **三角形** `hex_triangle()` - 三角形区域
- **平行四边形** `hex_parallelogram()` - 平行四边形区域
- **六边形** `hex_hexagon()` - 六边形形状区域
- **矩形** `hex_rectangle()` - 矩形区域 (偏移坐标)

### 旋转和镜像
- 顺时针/逆时针旋转 60°
- 旋转 180°
- 三轴镜像

### 坐标转换
- 轴向坐标 ↔ 偏移坐标 (偶数/奇数行)
- 六边形坐标 ↔ 像素坐标
- 浮点坐标四舍五入

### 视觉几何
- 六边形角点计算
- 像素坐标和角点坐标转换

### 路径查找
- **A* 算法** `hex_path_astar()` - 带障碍物的最优路径
- **BFS 算法** `hex_path_bfs()` - 广度优先搜索路径

### 视野计算
- **FOV** `hex_fov()` - 视野范围内的可见六边形
- **可见性检测** `hex_visible_from()` - 判断两点是否可见

### 区域操作
- **洪水填充** `hex_flood_fill()` - 可达区域计算
- **轮廓提取** `hex_region_outline()` - 区域边界
- **内部提取** `hex_region_interior()` - 区域内部

### 网格类
- `HexGrid` - 六边形网格管理类
  - 边界检查
  - 数据存储和获取
  - 路径查找
  - 视野计算
  - ASCII 可视化

### 可视化
- 单个六边形 ASCII 图案
- 网格 ASCII 图案
- 路径 ASCII 图案
- 范围 ASCII 图案

## 使用示例

### 基础坐标操作

```python
from hex_grid_utils.mod import Hex, hex_distance, hex_neighbors

# 创建六边形坐标
h1 = Hex(1, 2)
h2 = Hex(3, -1)

# 坐标运算
h3 = h1 + h2  # Hex(4, 1)
h4 = h1 - h2  # Hex(-2, 3)

# 获取立方体坐标
cube = h1.to_cube()  # (1, 2, -3)

# 计算距离
dist = hex_distance(h1, h2)  # 5

# 获取邻居
neighbors = hex_neighbors(Hex(0, 0))  # 6 个相邻六边形
```

### 区域生成

```python
from hex_grid_utils.mod import hex_range, hex_ring, hex_line, Hex

# 半径 2 的圆形区域
area = hex_range(Hex(0, 0), 2)  # 19 个六边形

# 半径 2 的圆环
ring = hex_ring(Hex(0, 0), 2)  # 12 个六边形

# 两点之间的直线
line = hex_line(Hex(0, 0), Hex(3, -2))
```

### 路径查找

```python
from hex_grid_utils.mod import hex_path_astar, Hex

start = Hex(0, 0)
goal = Hex(5, 3)
obstacles = {Hex(2, 1), Hex(2, 0), Hex(3, 1)}

path = hex_path_astar(start, goal, obstacles)
# 返回从起点到终点的路径列表
```

### 坐标转换

```python
from hex_grid_utils.mod import (
    Hex, HexOrientation, OffsetCoordType,
    hex_to_offset, offset_to_hex,
    hex_to_pixel, pixel_to_hex
)

h = Hex(2, 3)

# 轴向 -> 偏移坐标
offset = hex_to_offset(h, OffsetCoordType.ODD, HexOrientation.POINTY_TOP)
# (col, row)

# 像素坐标转换
pixel = hex_to_pixel(h, 30, HexOrientation.POINTY_TOP)
back = pixel_to_hex(pixel[0], pixel[1], 30, HexOrientation.POINTY_TOP)
```

### 网格类使用

```python
from hex_grid_utils.mod import HexGrid, Hex

grid = HexGrid(radius=5)

# 设置数据
grid.set(Hex(0, 0), "中心")
grid.set(Hex(1, 0), {"type": "tree"})

# 获取数据
value = grid.get(Hex(0, 0))

# 查找路径
path = grid.path(Hex(0, 0), Hex(4, 3), obstacles={Hex(2, 1)})

# 范围查询
area = grid.range(Hex(0, 0), 2)

# ASCII 可视化
print(grid.to_ascii())
```

### 可视化

```python
from hex_grid_utils.mod import visualize_hex_range, visualize_hex_path, Hex

# 可视化圆形范围
print(visualize_hex_range(Hex(0, 0), 3))

# 可视化路径
path = hex_line(Hex(0, 0), Hex(5, -3))
print(visualize_hex_path(path))
```

## API 参考

### 基础函数

| 函数 | 描述 |
|------|------|
| `hex_add(a, b)` | 六边形相加 |
| `hex_subtract(a, b)` | 六边形相减 |
| `hex_scale(h, scalar)` | 六边形缩放 |
| `hex_neighbor(h, orientation, direction)` | 获取相邻六边形 |
| `hex_neighbors(h, orientation)` | 获取所有邻居 |
| `hex_distance(a, b)` | 计算曼哈顿距离 |

### 区域生成函数

| 函数 | 描述 |
|------|------|
| `hex_range(center, radius)` | 圆形区域 |
| `hex_ring(center, radius)` | 圆环 |
| `hex_spiral(center, radius)` | 螺旋区域 |
| `hex_line(a, b)` | 直线 |
| `hex_triangle(size)` | 三角形 |
| `hex_parallelogram(q1, q2, r1, r2)` | 平行四边形 |
| `hex_hexagon(radius)` | 六边形区域 |
| `hex_rectangle(width, height)` | 矩形区域 |

### 坐标转换函数

| 函数 | 描述 |
|------|------|
| `hex_to_offset(h, coord_type, orientation)` | 轴向 → 偏移 |
| `offset_to_hex(col, row, coord_type, orientation)` | 偏移 → 轴向 |
| `hex_to_pixel(h, size, orientation)` | 六边形 → 像素 |
| `pixel_to_hex(x, y, size, orientation)` | 像素 → 六边形 |

### 路径查找函数

| 函数 | 描述 |
|------|------|
| `hex_path_astar(start, goal, obstacles)` | A* 路径查找 |
| `hex_path_bfs(start, goal, obstacles)` | BFS 路径查找 |

### 可视化函数

| 函数 | 描述 |
|------|------|
| `visualize_hex(h, size, char)` | 单个六边形可视化 |
| `visualize_hex_grid(hexes, char)` | 网格可视化 |
| `visualize_hex_path(path)` | 路径可视化 |
| `visualize_hex_range(center, radius)` | 范围可视化 |

## 应用场景

- **游戏开发** - 六边形地图、策略游戏
- **数据可视化** - 六边形热力图、地图投影
- **路径规划** - 六边形网格导航
- **蜂窝模拟** - 蜂窝结构模拟
- **地图生成** - 六边形地图生成器

## 设计说明

### 坐标系统

使用轴向坐标 (Axial Coordinates)，这是立方体坐标 `(x, y, z)` 的投影，其中 `x + y + z = 0`。
轴向坐标只需要两个分量 `(q, r)`，第三个分量 `s = -q - r` 可以计算得出。

### 朝向选择

- **尖顶 (POINTY_TOP)**: 适合大多数策略游戏，如 CIV、战棋
- **平顶 (FLAT_TOP)**: 适合某些特定视觉风格

## 测试

```bash
python test.py
```

## 文件结构

```
hex_grid_utils/
├── mod.py        # 主模块
├── test.py       # 测试文件
└── README.md     # 文档
```

## 依赖

无外部依赖，纯 Python 标准库实现。

## 版本

- v1.0.0 - 2025-05-11
  - 基础坐标操作
  - 区域生成
  - 路径查找
  - 视野计算
  - 坐标转换
  - ASCII 可视化