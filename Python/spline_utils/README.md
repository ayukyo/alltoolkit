# Spline Utils - 样条曲线工具库

零依赖的样条曲线插值和生成工具，纯 Python 实现。

## 功能特性

- **Linear Spline**: 线性样条插值（折线连接）
- **Cubic Spline**: 三次样条插值（自然边界条件）
- **Catmull-Rom Spline**: 卡特穆-罗姆样条（曲线通过控制点）
- **B-Spline**: 均匀 B 样条曲线
- **Hermite Spline**: 埃尔米特样条（指定切线方向）
- **工具函数**: 曲线采样、长度计算、重采样、平滑

## 安装

无需安装，直接导入使用：

```python
from spline_utils.spline import (
    Point2D, Point3D,
    linear_spline, cubic_spline,
    catmull_rom_spline, b_spline,
    hermite_spline, hermite_spline_auto,
    interpolate
)
```

## 快速开始

### 创建控制点

```python
from spline_utils.spline import Point2D

# 方式1：使用 Point2D 对象
points = [
    Point2D(0, 0),
    Point2D(2, 3),
    Point2D(4, 1),
    Point2D(6, 4),
    Point2D(8, 0)
]

# 方式2：使用元组（便捷函数）
tuple_points = [(0, 0), (2, 3), (4, 1), (6, 4), (8, 0)]
```

### 便捷插值函数

```python
from spline_utils.spline import interpolate

# 一行代码完成插值
result = interpolate(tuple_points, method='cubic', num_points=100)

# 支持的方法: 'linear', 'cubic', 'catmull_rom', 'b_spline', 'hermite'
result = interpolate(tuple_points, method='catmull_rom', num_points=50)
```

### 线性样条

```python
from spline_utils.spline import linear_spline

# 连接各点的直线段
curve = linear_spline(points, num_points=50)
```

### 三次样条

```python
from spline_utils.spline import cubic_spline

# 平滑的三次样条插值（自然边界条件）
curve = cubic_spline(points, num_points=100)
```

### Catmull-Rom 样条

```python
from spline_utils.spline import catmull_rom_spline

# 曲线通过所有控制点
curve = catmull_rom_spline(points, num_points=100)

# 调整张力参数（0-1）
curve = catmull_rom_spline(points, num_points=100, tension=0.3)

# 闭合曲线
curve = catmull_rom_spline(points, num_points=100, close=True)
```

### B-Spline

```python
from spline_utils.spline import b_spline

# 三次 B 样条（默认）
curve = b_spline(points, degree=3, num_points=100)

# 二次 B 样条
curve = b_spline(points, degree=2, num_points=100)

# 闭合 B 样条
curve = b_spline(points, degree=3, num_points=100, close=True)
```

### Hermite 样条

```python
from spline_utils.spline import hermite_spline, hermite_spline_auto, Point2D

# 手动指定切线
tangents = [
    Point2D(1, 1),
    Point2D(0.5, -0.5),
    Point2D(-1, 0),
    Point2D(0, -1),
    Point2D(-1, 0)
]
curve = hermite_spline(points, tangents, num_points=100)

# 自动计算切线
curve = hermite_spline_auto(points, num_points=100)
```

### 工具函数

```python
from spline_utils.spline import (
    curve_length, sample_curve, 
    resample_curve, smooth_points
)

# 计算曲线长度
length = curve_length(curve)

# 按距离采样曲线
sampled = sample_curve(curve, sample_distance=0.5)

# 按点数重采样（均匀分布）
resampled = resample_curve(curve, num_points=50)

# 平滑点列（Laplacian 平滑）
smoothed = smooth_points(points, iterations=2, factor=0.5)
```

## API 参考

### Point2D

```python
class Point2D:
    def __init__(self, x: float, y: float)
    def distance_to(self, other: Point2D) -> float
    def to_tuple(self) -> Tuple[float, float]
```

### 插值函数

| 函数 | 参数 | 说明 |
|------|------|------|
| `linear_spline(points, num_points)` | points: 控制点列表 | 线性插值 |
| `cubic_spline(points, num_points)` | points: 至少2点，按x排序 | 三次样条插值 |
| `catmull_rom_spline(points, num_points, tension, close)` | tension: 0-1 | 通过控制点 |
| `b_spline(points, degree, num_points, close)` | degree: 1-3 | B样条曲线 |
| `hermite_spline(points, tangents, num_points)` | tangents: 切线向量 | 指定切线 |
| `interpolate(points, method, num_points)` | method: 方法名 | 便捷函数 |

### 工具函数

| 函数 | 说明 |
|------|------|
| `curve_length(points)` | 计算曲线总长度 |
| `sample_curve(points, distance)` | 按距离采样 |
| `resample_curve(points, num_points)` | 均匀重采样 |
| `smooth_points(points, iterations, factor)` | 平滑点列 |

## 使用示例

### 数据可视化平滑

```python
import matplotlib.pyplot as plt  # 外部依赖，仅示例
from spline_utils.spline import Point2D, catmull_rom_spline

# 原始数据点
data = [(0, 10), (1, 5), (2, 8), (3, 3), (4, 6), (5, 2)]
points = [Point2D(x, y) for x, y in data]

# 平滑曲线
smooth = catmull_rom_spline(points, num_points=100)

# 绘图
plt.plot([p.x for p in points], [p.y for p in points], 'ro', label='原始数据')
plt.plot([p.x for p in smooth], [p.y for p in smooth], 'b-', label='平滑曲线')
plt.legend()
plt.show()
```

### 动画路径

```python
from spline_utils.spline import Point2D, catmull_rom_spline

# 定义动画路径
waypoints = [
    Point2D(0, 0),
    Point2D(100, 50),
    Point2D(200, 100),
    Point2D(150, 200),
    Point2D(100, 150)
]

# 生成平滑路径（闭合）
path = catmull_rom_spline(waypoints, num_points=60, close=True)

# 动画循环
for frame, pos in enumerate(path):
    # 更新对象位置
    object.x = pos.x
    object.y = pos.y
    # ...渲染帧...
```

### 轨迹平滑

```python
from spline_utils.spline import smooth_points, Point2D

# GPS 轨迹点
gps_points = [
    Point2D(116.404, 39.915),
    Point2D(116.408, 39.920),  # 噪声点
    Point2D(116.412, 39.910),  # 噪声点
    Point2D(116.416, 39.925),
    Point2D(116.420, 39.930)
]

# 平滑轨迹
smooth_trajectory = smooth_points(gps_points, iterations=2, factor=0.5)
```

## 运行测试

```bash
cd Python
python -m spline_utils.spline_test
```

## 数学原理

### 三次样条

三次样条使用自然边界条件（端点二阶导数为0），通过求解三对角线性方程组得到每个控制点的二阶导数值，然后分段计算三次多项式。

### Catmull-Rom 样条

Catmull-Rom 样条是 Cardinal 样条的特殊情况，张力参数默认为 0.5。曲线保证通过所有控制点，常用于动画路径和相机路径。

### B-Spline

B-Spline 使用递归定义的基函数，曲线被控制点"拉"但不一定通过控制点。阶数决定曲线的平滑程度。

## 许可证

MIT License