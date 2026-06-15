# Convex Hull Utils 📐

凸包计算工具模块，提供多种凸包算法实现。

## 特性

- ✅ **多种算法** - Graham Scan、Jarvis March、QuickHull、Chan's Algorithm
- ✅ **统一接口** - ConvexHull 类封装所有算法
- ✅ **O(n log h)** 最优复杂度 - Chan's Algorithm
- ✅ **几何计算** - 面积、周长、点包含检测
- ✅ **零依赖** - 仅使用 Python 标准库

## 快速开始

### 计算凸包

```python
from convex_hull_utils import convex_hull, Point

# 使用默认算法（Graham Scan）
points = [(0, 0), (1, 1), (2, 0), (1.5, 1.5)]
hull = convex_hull(points)
print(hull)  # [Point(0, 0), Point(2, 0), Point(1.5, 1.5)]
```

### 使用不同算法

```python
from convex_hull_utils import convex_hull, HullAlgorithm

# Jarvis March
hull = convex_hull(points, algorithm=HullAlgorithm.JARVIS_MARCH)

# Chan's Algorithm
hull = convex_hull(points, algorithm=HullAlgorithm.CHAN)
```

### 几何计算

```python
from convex_hull_utils import convex_hull_area, convex_hull_perimeter

area = convex_hull_area(points)
print(f"面积: {area:.2f}")

perimeter = convex_hull_perimeter(points)
print(f"周长: {perimeter:.2f}")
```

### 点包含检测

```python
from convex_hull_utils import point_in_convex_hull

hull = [(0, 0), (2, 0), (1, 1)]
inside = point_in_convex_hull((1, 0.5), hull)
print(inside)  # True
```

## API 参考

### 算法枚举

| 算法 | 复杂度 | 适用场景 |
|------|--------|----------|
| `GRAHAM_SCAN` | O(n log n) | 大多数情况 |
| `JARVIS_MARCH` | O(nh) | 点数少、凸包小 |
| `QUICKHULL` | O(n log n) 平均 | 实践中最快 |
| `CHAN` | O(n log h) | 最优输出敏感 |

### 核心函数

| 函数 | 说明 |
|------|------|
| `convex_hull(points, algorithm)` | 计算凸包 |
| `convex_hull_area(points)` | 计算凸包面积 |
| `convex_hull_perimeter(points)` | 计算凸包周长 |
| `point_in_convex_hull(point, hull)` | 检测点是否在凸包内 |
| `merge_convex_hulls(hull1, hull2)` | 合并两个凸包 |
