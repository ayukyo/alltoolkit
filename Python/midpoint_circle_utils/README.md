# midpoint_circle_utils - 中点画圆算法工具

[![Test Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](./midpoint_circle_utils_test.py)

零依赖的中点画圆算法实现，用于生成圆形像素坐标。

## 特性

- **中点画圆算法**: Bresenham 中点画圆算法
- **高效整数运算**: 仅使用整数加减和比较
- **多种输出格式**: 坐标列表、像素矩阵、SVG
- **圆弧绘制**: 支持绘制部分圆弧
- **填充圆**: 支持实心圆填充
- **多圆绘制**: 支持批量绘制同心圆
- **零依赖**: 纯 Python 实现

## 安装

```python
from midpoint_circle_utils import (
    draw_circle,
    draw_filled_circle,
    draw_arc,
    get_circle_points
)
```

## 快速开始

### 绘制圆形

```python
from midpoint_circle_utils import draw_circle

# 绘制半径为 10 的圆
points = draw_circle(center=(0, 0), radius=10)
print(f"圆上有 {len(points)} 个点")

# 绘制到特定坐标系
points = draw_circle(center=(100, 100), radius=50)
```

### 填充圆

```python
from midpoint_circle_utils import draw_filled_circle

# 绘制实心圆
points = draw_filled_circle(center=(50, 50), radius=20)
print(f"圆内共 {len(points)} 个点")
```

### 绘制圆弧

```python
from midpoint_circle_utils import draw_arc

# 绘制 0-90 度的圆弧
arc_points = draw_arc(center=(0, 0), radius=10, start_angle=0, end_angle=90)
```

### 输出为像素矩阵

```python
from midpoint_circle_utils import draw_circle_to_matrix

# 绘制到矩阵
matrix = draw_circle_to_matrix(
    center=(25, 25),
    radius=20,
    width=50,
    height=50
)

# matrix[y][x] == 1 表示圆上的点
```

## API 参考

### 主要函数

| 函数 | 说明 |
|-----|------|
| `draw_circle(center, radius)` | 绘制圆形轮廓 |
| `draw_filled_circle(center, radius)` | 绘制实心圆 |
| `draw_arc(center, radius, start_angle, end_angle)` | 绘制圆弧 |
| `get_circle_points(radius)` | 获取圆上相对坐标 |
| `draw_circle_to_matrix(center, radius, width, height)` | 输出到矩阵 |

### 参数说明

- `center`: 圆心坐标 (x, y)
- `radius`: 圆半径
- `start_angle`: 圆弧起始角度（度）
- `end_angle`: 圆弧结束角度（度）

## 算法原理

中点画圆算法是一种高效的整数算法：

1. 利用圆的八分对称性，只需计算 1/8 圆弧
2. 使用中点判断决定下一个像素位置
3. 仅使用整数运算（加减、比较）
4. 误差可控，最多偏离半个像素

### 决策参数

```
d = (x+1)^2 + (y-0.5)^2 - r^2
```

- `d < 0`: 下一点取 (x+1, y)
- `d >= 0`: 下一点取 (x+1, y-1)

## 测试

```bash
python -m pytest midpoint_circle_utils_test.py -v
```

## 许可证

MIT License