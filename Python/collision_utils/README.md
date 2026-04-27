# Collision Utils


Collision Detection Utilities - 碰撞检测工具模块

提供全面的2D碰撞检测功能，包括矩形、圆形、多边形、射线等碰撞检测。
零依赖，仅使用 Python 标准库。

Author: AllToolkit
Version: 1.0.0


## 功能

### 类

- **Rectangle**: 矩形类
  方法: left, right, top, bottom, center ... (9 个方法)
- **Circle**: 圆形类
  方法: center, contains_point, get_bounding_box
- **Line**: 线段类
  方法: start, end, length, length_squared, get_bounding_box
- **Polygon**: 多边形类
  方法: center, get_edges, get_bounding_box
- **Ray**: 射线类
  方法: origin, direction, get_point
- **RaycastHit**: 射线碰撞结果
- **CollisionUtils**: 碰撞检测工具类
  方法: point_in_circle, point_in_rectangle, point_in_polygon, point_on_line, rectangle_rectangle ... (21 个方法)

### 函数

- **point_in_circle(px, py, x**, ...) - 检查点是否在圆内
- **point_in_rect(px, py, x**, ...) - 检查点是否在矩形内
- **circles_collide(x1, y1, r1**, ...) - 检查两个圆是否碰撞
- **rects_collide(x1, y1, w1**, ...) - 检查两个矩形是否碰撞
- **rect_circle_collide(rx, ry, rw**, ...) - 检查矩形和圆是否碰撞
- **lines_intersect(x1, y1, x2**, ...) - 检查两条线段是否相交
- **distance(x1, y1, x2**, ...) - 计算两点之间的距离
- **distance_squared(x1, y1, x2**, ...) - 计算两点之间距离的平方
- **left(self**)
- **right(self**)

... 共 55 个函数

## 使用示例

```python
from mod import point_in_circle

# 使用 point_in_circle
result = point_in_circle()
```

## 测试

运行测试：

```bash
python *_test.py
```

## 文件结构

```
{module_name}/
├── mod.py              # 主模块
├── *_test.py           # 测试文件
├── README.md           # 本文档
└── examples/           # 示例代码
    └── usage_examples.py
```

---

**Last updated**: 2026-04-28
