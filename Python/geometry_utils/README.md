# Geometry Utils - Python 几何工具模块

AllToolkit 的 Python 几何计算工具模块，提供全面的 2D/3D 几何运算功能，零外部依赖。

## 📦 功能特性

### 角度转换
- `degrees_to_radians()` - 角度转弧度
- `radians_to_degrees()` - 弧度转角度
- `normalize_angle_degrees()` - 规范化角度到 [0, 360)
- `normalize_angle_radians()` - 规范化角度到 [0, 2π)

### 距离计算
- `distance_2d()` - 2D 欧几里得距离
- `distance_3d()` - 3D 欧几里得距离
- `manhattan_distance_2d()` - 曼哈顿距离
- `chebyshev_distance_2d()` - 切比雪夫距离
- `distance_from_origin_2d()` / `distance_from_origin_3d()` - 到原点距离

### 2D 形状计算
- **圆形**: `circle_area()`, `circle_circumference()`, `circle_diameter()`
- **矩形**: `rectangle_area()`, `rectangle_perimeter()`
- **正方形**: `square_area()`, `square_perimeter()`
- **三角形**: `triangle_area()`, `triangle_area_heron()`, `triangle_perimeter()`, `equilateral_triangle_area()`
- **多边形**: `regular_polygon_area()`, `trapezoid_area()`, `rhombus_area()`, `parallelogram_area()`
- **椭圆**: `ellipse_area()`, `ellipse_circumference_approx()`

### 3D 形状计算
- **球体**: `sphere_volume()`, `sphere_surface_area()`
- **立方体**: `cube_volume()`, `cube_surface_area()`
- **长方体**: `rectangular_prism_volume()`, `rectangular_prism_surface_area()`
- **圆柱**: `cylinder_volume()`, `cylinder_surface_area()`
- **圆锥**: `cone_volume()`, `cone_surface_area()`
- **棱锥**: `pyramid_volume()`, `tetrahedron_volume()`, `tetrahedron_surface_area()`

### 向量运算
- **加减**: `vector_add_2d()`, `vector_subtract_2d()`, `vector_add_3d()`, `vector_subtract_3d()`
- **缩放**: `vector_scale_2d()`, `vector_scale_3d()`
- **点积**: `dot_product_2d()`, `dot_product_3d()`
- **叉积**: `cross_product_3d()`
- **模长**: `vector_magnitude_2d()`, `vector_magnitude_3d()`
- **归一化**: `normalize_vector_2d()`, `normalize_vector_3d()`
- **角度**: `vector_angle_2d()`, `angle_between_vectors_2d()`

### 几何变换
- `rotate_point_2d()` - 2D 点旋转
- `translate_point_2d()` - 2D 点平移
- `scale_point_2d()` - 2D 点缩放
- `reflect_point_x()` / `reflect_point_y()` / `reflect_point_origin()` - 反射变换

### 碰撞检测
- `point_in_rectangle()` - 点是否在矩形内
- `point_in_circle()` - 点是否在圆内
- `circles_intersect()` - 两圆是否相交
- `rectangles_intersect()` - 两矩形是否相交

### 坐标转换
- `cartesian_to_polar()` / `polar_to_cartesian()` - 笛卡尔↔极坐标
- `cartesian_to_cylindrical()` / `cylindrical_to_cartesian()` - 笛卡尔↔柱坐标
- `cartesian_to_spherical()` / `spherical_to_cartesian()` - 笛卡尔↔球坐标

### 三角形函数
- `triangle_type_by_sides()` - 按边长分类（等边/等腰/不等边）
- `triangle_type_by_angles()` - 按角度分类（锐角/直角/钝角）
- `triangle_angles()` - 计算三个角度
- `is_right_triangle()` - 是否直角三角形
- `pythagorean_triple_check()` - 是否勾股数

### 其他工具
- `midpoint_2d()` / `midpoint_3d()` - 中点计算
- `centroid_triangle()` - 三角形重心
- `polygon_area()` - 多边形面积（鞋带公式）
- `polygon_perimeter()` - 多边形周长
- `is_convex_polygon()` - 是否凸多边形
- `interpolate_points()` - 线性插值
- `slope()` - 直线斜率
- `line_equation()` - 直线方程
- `point_to_line_distance()` - 点到直线距离

### 数学常量
- `PI` - 圆周率
- `E` - 自然常数
- `GOLDEN_RATIO` - 黄金比例
- `SQRT2` - √2
- `SQRT3` - √3

## 🚀 快速开始

### 安装

无需安装，直接使用：

```python
import sys
sys.path.insert(0, '/path/to/AllToolkit/Python/geometry_utils')
from mod import *
```

### 基本用法

```python
from mod import *

# 距离计算
dist = distance_2d((0, 0), (3, 4))
print(dist)  # 5.0

# 圆形计算
r = 5
area = circle_area(r)
circumference = circle_circumference(r)
print(f"Circle (r={r}): Area={area:.2f}, Circumference={circumference:.2f}")

# 三角形计算
area = triangle_area_heron(3, 4, 5)
triangle_type = triangle_type_by_angles(3, 4, 5)
print(f"Triangle (3,4,5): Area={area}, Type={triangle_type}")  # Area=6.0, Type=right

# 向量运算
v1, v2 = (1, 2), (3, 4)
dot = dot_product_2d(v1, v2)
print(f"Dot product: {dot}")  # 11.0

# 旋转变换
point = (1, 0)
rotated = rotate_point_2d(point, 90)
print(f"Rotate (1,0) by 90°: ({rotated[0]:.2f}, {rotated[1]:.2f})")  # (0.00, 1.00)

# 碰撞检测
inside = point_in_circle((2, 2), (0, 0), 3)
print(f"Point (2,2) in circle (0,0) r=3: {inside}")  # True

# 坐标转换
polar = cartesian_to_polar((1, 1))
print(f"Cartesian (1,1) -> Polar: r={polar[0]:.4f}, θ={polar[1]:.4f} rad")
```

## 📁 文件结构

```
geometry_utils/
├── mod.py                      # 主模块（所有工具函数）
├── geometry_utils_test.py      # 测试套件（130+ 个测试）
├── README.md                   # 本文档
└── examples/
    └── usage_examples.py       # 使用示例
```

## ✅ 测试

运行测试套件：

```bash
cd /path/to/AllToolkit/Python/geometry_utils
python3 geometry_utils_test.py
```

预期输出：
```
Running AllToolkit Geometry Utils Test Suite
==================================================
✓ Constants tests completed
✓ Angle conversion tests completed
✓ Distance calculation tests completed
✓ 2D shape tests completed
✓ 3D shape tests completed
✓ Vector operation tests completed
✓ Transformation tests completed
✓ Collision detection tests completed
✓ Coordinate conversion tests completed
✓ Triangle function tests completed
✓ Miscellaneous tests completed
✓ Edge case tests completed
==================================================
Tests: 130+ | Passed: 130+ | Failed: 0

✅ All tests passed!
```

## 📖 示例

运行使用示例：

```bash
cd /path/to/AllToolkit/Python/geometry_utils/examples
python3 usage_examples.py
```

## 💡 实际应用场景

### 1. 游戏开发 - 碰撞检测

```python
def check_player_collision(player_pos, enemy_pos, attack_range):
    """检查玩家是否在敌人攻击范围内"""
    return point_in_circle(player_pos, enemy_pos, attack_range)

def check_bullet_hit(bullet_pos, target_rect):
    """检查子弹是否命中目标"""
    return point_in_rectangle(bullet_pos, target_rect[0], target_rect[1])
```

### 2. 图形处理 - 坐标变换

```python
def rotate_shape(vertices, angle, center):
    """旋转多边形"""
    return [rotate_point_2d(v, angle, center) for v in vertices]

def scale_shape(vertices, scale_factor, origin=(0, 0)):
    """缩放多边形"""
    return [scale_point_2d(v, scale_factor, scale_factor, origin) for v in vertices]
```

### 3. 物理模拟 - 向量运算

```python
def calculate_velocity(position1, position2, time_delta):
    """计算速度向量"""
    displacement = vector_subtract_2d(position2, position1)
    return vector_scale_2d(displacement, 1.0 / time_delta)

def calculate_kinetic_energy(mass, velocity_vector):
    """计算动能"""
    speed = vector_magnitude_2d(velocity_vector)
    return 0.5 * mass * speed * speed
```

### 4. 地图应用 - 距离计算

```python
def calculate_distance_km(lat1, lon1, lat2, lon2):
    """近似计算两点距离（简化版，不考虑地球曲率）"""
    # 注意：实际应用中应使用 Haversine 公式
    return distance_2d((lat1, lon1), (lat2, lon2)) * 111  # 约略转换

def find_nearby_points(user_location, points, max_distance):
    """查找指定范围内的点"""
    return [p for p in points if distance_2d(user_location, p) <= max_distance]
```

### 5. CAD/设计 - 几何计算

```python
def calculate_material_area(shape_vertices):
    """计算材料面积"""
    return polygon_area(shape_vertices)

def calculate_cutting_length(shape_vertices):
    """计算切割长度（周长）"""
    return polygon_perimeter(shape_vertices)

def is_valid_convex_part(vertices):
    """检查零件是否为凸多边形（便于加工）"""
    return is_convex_polygon(vertices)
```

### 6. 机器人学 - 路径规划

```python
def interpolate_path(start, end, num_points):
    """生成路径插值点"""
    return [interpolate_points(start, end, i / (num_points - 1)) 
            for i in range(num_points)]

def calculate_turn_angle(current_dir, target_dir):
    """计算机器人需要转向的角度"""
    return angle_between_vectors_2d(current_dir, target_dir)
```

## 🔒 安全特性

- **输入验证** - 所有函数处理负值和零值安全
- **类型转换** - 自动将字符串等转换为浮点数
- **边界处理** - 无效输入返回 0 或空值，不抛出异常
- **浮点容差** - 比较操作使用 epsilon 容差

## 📊 性能特点

- **零依赖** - 仅使用 Python 标准库（math 模块）
- **高效实现** - 使用内置数学函数
- **内存友好** - 无大型数据结构
- **类型提示** - 完整的类型注解支持 IDE 智能提示

## 🧪 测试覆盖

测试套件包含 130+ 个测试用例，覆盖：

- ✅ 正常场景
- ✅ 边界值（零、负数、极大值）
- ✅ 特殊情况（垂直线、重合点等）
- ✅ 坐标转换往返验证
- ✅ 三角形分类完整性
- ✅ 碰撞检测各种情况

## 📝 许可证

MIT License - 详见 AllToolkit 主项目 LICENSE 文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 支持

如有问题，请在 AllToolkit 仓库提交 Issue。

## 🔗 相关模块

- `text_utils` - 文本处理工具
- `math_utils` - 数学工具（如实现）
- `physics_utils` - 物理计算工具（如实现）
