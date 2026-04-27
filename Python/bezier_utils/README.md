# Bezier Utils


贝塞尔曲线工具模块

提供贝塞尔曲线的计算、插值、分割等功能。
零外部依赖，纯 Python 实现。

支持：
- 一阶（线性）、二阶（二次）、三阶（三次）及任意阶贝塞尔曲线
- 曲线上的点计算
- 曲线长度近似计算
- 曲线切线和法线向量
- 曲线分割
- 曲线平滑（生成多点路径）


## 功能

### 类

- **Point**: 二维点类
  方法: distance_to, magnitude, normalize, perpendicular, to_tuple ... (6 个方法)
- **BezierCurve**: 贝塞尔曲线类

支持任意阶数的贝塞尔曲线计算。
  方法: degree, start_point, end_point, point_at, derivative_at ... (16 个方法)
- **LinearBezier**: 一阶（线性）贝塞尔曲线
  方法: point_at, length
- **QuadraticBezier**: 二阶（二次）贝塞尔曲线
  方法: point_at
- **CubicBezier**: 三阶（三次）贝塞尔曲线
  方法: point_at

### 函数

- **create_bezier(points**) - 从坐标元组列表创建贝塞尔曲线
- **linear_bezier(p0, p1**) - 创建线性贝塞尔曲线
- **quadratic_bezier(p0, p1, p2**) - 创建二次贝塞尔曲线
- **cubic_bezier(p0, p1, p2**, ...) - 创建三次贝塞尔曲线
- **smooth_path(points, tension**) - 通过一组点生成平滑的贝塞尔曲线路径
- **interpolate_points(points, tension**) - 在点之间插值生成平滑路径
- **find_t_for_x(curve, target_x, tolerance**, ...) - 找到曲线上 x 坐标等于 target_x 的参数 t
- **distance_to_point(curve, point, num_samples**) - 计算点到曲线的最短距离
- **distance_to(self, other**) - 计算到另一个点的距离
- **magnitude(self**) - 向量的模

... 共 35 个函数

## 使用示例

```python
from mod import create_bezier

# 使用 create_bezier
result = create_bezier()
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
