# Voronoi Utils 🔷

Voronoi 图计算工具模块，提供泰森多边形生成、邻居查找等功能。

## 特性

- ✅ **Voronoi 图生成** - Fortune 算法实现
- ✅ **最近点查询** - 快速查找最近邻居
- ✅ **Lloyd 松弛** - 生成更均匀的 Voronoi 图
- ✅ **德洛奈三角网** - 获取邻居关系
- ✅ **可视化输出** - ASCII 和 SVG 格式

## 快速开始

### 生成 Voronoi 图

```python
from voronoi_utils import compute_voronoi, Point

points = [(0, 0), (3, 0), (1.5, 3)]
diagram = compute_voronoi(points)

for cell in diagram.cells:
    print(f"Cell for {cell.site}: {[e.p1 for e in cell.edges]}")
```

### 查找最近点

```python
from voronoi_utils import nearest_point

points = [(0, 0), (1, 1), (2, 2)]
nearest = nearest_point(points, (1.1, 1.1))
print(nearest)  # (1, 1)
```

### Lloyd 松弛

```python
from voronoi_utils import relax_points, compute_voronoi

points = [(0, 0), (1, 0), (0, 1)]
relaxed = relax_points(points, iterations=5)
```

## API 参考

| 函数 | 说明 |
|------|------|
| `compute_voronoi(points)` | 计算 Voronoi 图 |
| `nearest_point(points, target)` | 查找最近点 |
| `relax_points(points)` | Lloyd 松弛 |
| `delaunay_neighbors(points)` | 德洛奈邻居 |
| `voronoi_ascii(points)` | ASCII 可视化 |
| `voronoi_svg(points)` | SVG 可视化 |
