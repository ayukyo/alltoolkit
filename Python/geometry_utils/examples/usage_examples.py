#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit Geometry Utils - Usage Examples
============================================
Demonstration of various geometry utility functions.

Run: python3 usage_examples.py
"""

import sys
import math

# Import the geometry utils module
sys.path.insert(0, '..')
from mod import *


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def example_basic_calculations():
    """Demonstrate basic geometry calculations."""
    print_section("基础几何计算")
    
    # 距离计算
    p1, p2 = (0, 0), (3, 4)
    dist = distance_2d(p1, p2)
    print(f"\n📏 距离计算:")
    print(f"   点 {p1} 到 {p2} 的欧几里得距离：{dist}")
    print(f"   曼哈顿距离：{manhattan_distance_2d(p1, p2)}")
    print(f"   切比雪夫距离：{chebyshev_distance_2d(p1, p2)}")
    
    # 圆形计算
    print(f"\n⭕ 圆形计算 (半径=5):")
    r = 5
    print(f"   面积：{circle_area(r):.4f}")
    print(f"   周长：{circle_circumference(r):.4f}")
    print(f"   直径：{circle_diameter(r)}")
    
    # 三角形计算
    print(f"\n🔺 三角形计算 (边长 3,4,5):")
    print(f"   面积 (海伦公式): {triangle_area_heron(3, 4, 5)}")
    print(f"   周长：{triangle_perimeter(3, 4, 5)}")
    print(f"   类型 (按边): {triangle_type_by_sides(3, 4, 5)}")
    print(f"   类型 (按角): {triangle_type_by_angles(3, 4, 5)}")
    
    # 角度
    print(f"\n📐 角度转换:")
    print(f"   180° = {degrees_to_radians(180):.6f} 弧度")
    print(f"   π 弧度 = {radians_to_degrees(PI)}°")
    print(f"   450° 规范化 = {normalize_angle_degrees(450)}°")


def example_vector_operations():
    """Demonstrate vector operations."""
    print_section("向量运算")
    
    v1, v2 = (1, 2), (3, 4)
    
    print(f"\n向量 v1={v1}, v2={v2}:")
    print(f"   加法：{vector_add_2d(v1, v2)}")
    print(f"   减法：{vector_subtract_2d(v1, v2)}")
    print(f"   v1 × 2: {vector_scale_2d(v1, 2)}")
    print(f"   点积：{dot_product_2d(v1, v2)}")
    print(f"   v1 模长：{vector_magnitude_2d(v1):.4f}")
    print(f"   v1 归一化：{normalize_vector_2d(v1)}")
    print(f"   v1 角度：{vector_angle_2d(v1):.4f} 弧度 ({degrees_to_radians(vector_angle_2d(v1)):.2f}°)")
    
    # 3D 向量
    print(f"\n3D 向量 v1=(1,2,3), v2=(4,5,6):")
    v1_3d, v2_3d = (1, 2, 3), (4, 5, 6)
    print(f"   叉积：{cross_product_3d(v1_3d, v2_3d)}")
    print(f"   点积：{dot_product_3d(v1_3d, v2_3d)}")


def example_transformations():
    """Demonstrate geometric transformations."""
    print_section("几何变换")
    
    point = (1, 0)
    print(f"\n点 {point} 的变换:")
    
    # 旋转
    for angle in [90, 180, 270, 360]:
        rotated = rotate_point_2d(point, angle)
        print(f"   旋转 {angle}°: ({rotated[0]:.4f}, {rotated[1]:.4f})")
    
    # 平移
    translated = translate_point_2d(point, 2, 3)
    print(f"\n   平移 (+2, +3): {translated}")
    
    # 缩放
    scaled = scale_point_2d(point, 3, 3)
    print(f"   缩放 (×3): {scaled}")
    
    # 反射
    print(f"\n   关于 X 轴反射：{reflect_point_x(point)}")
    print(f"   关于 Y 轴反射：{reflect_point_y(point)}")
    print(f"   关于原点反射：{reflect_point_origin(point)}")


def example_collision_detection():
    """Demonstrate collision detection."""
    print_section("碰撞检测")
    
    # 点在矩形内
    print(f"\n📍 点是否在矩形内:")
    rect_tl, rect_br = (0, 0), (10, 10)
    test_points = [(5, 5), (0, 0), (10, 10), (11, 11), (-1, -1)]
    for p in test_points:
        inside = point_in_rectangle(p, rect_tl, rect_br)
        status = "✓ 在内" if inside else "✗ 在外"
        print(f"   点 {p}: {status}")
    
    # 点在圆内
    print(f"\n📍 点是否在圆内 (圆心=(0,0), 半径=5):")
    center, radius = (0, 0), 5
    test_points = [(3, 3), (0, 0), (5, 0), (4, 4), (6, 6)]
    for p in test_points:
        inside = point_in_circle(p, center, radius)
        status = "✓ 在内" if inside else "✗ 在外"
        print(f"   点 {p}: {status}")
    
    # 圆相交
    print(f"\n⭕ 圆相交检测:")
    circles = [
        ((0, 0), 3, (4, 0), 3, "相交"),
        ((0, 0), 2, (10, 0), 2, "分离"),
        ((0, 0), 5, (0, 0), 3, "包含"),
        ((0, 0), 2, (4, 0), 2, "外切"),
    ]
    for c1, r1, c2, r2, expected in circles:
        intersects = circles_intersect(c1, r1, c2, r2)
        status = "✓" if intersects == (expected == "相交" or expected == "外切" or expected == "包含") else "✗"
        print(f"   圆{c1}(r={r1}) vs 圆{c2}(r={r2}): {'相交' if intersects else '不相交'} {status}")
    
    # 矩形相交
    print(f"\n⬜ 矩形相交检测:")
    rects = [
        (((0, 0), (4, 4)), ((2, 2), (6, 6)), True),
        (((0, 0), (2, 2)), ((3, 3), (5, 5)), False),
        (((0, 0), (4, 4)), ((4, 4), (6, 6)), True),  # 角接触
    ]
    for r1, r2, expected in rects:
        intersects = rectangles_intersect(r1[0], r1[1], r2[0], r2[1])
        status = "✓" if intersects == expected else "✗"
        print(f"   矩形{r1} vs {r2}: {'相交' if intersects else '不相交'} {status}")


def example_coordinate_conversions():
    """Demonstrate coordinate system conversions."""
    print_section("坐标系转换")
    
    # 笛卡尔 ↔ 极坐标
    print(f"\n🔄 笛卡尔坐标 ↔ 极坐标:")
    cartesian_points = [(1, 0), (0, 1), (1, 1), (-1, 0)]
    for p in cartesian_points:
        polar = cartesian_to_polar(p)
        back = polar_to_cartesian(polar[0], polar[1])
        print(f"   {p} → (r={polar[0]:.4f}, θ={polar[1]:.4f}) → {back}")
    
    # 笛卡尔 ↔ 柱坐标
    print(f"\n🔄 笛卡尔坐标 ↔ 柱坐标:")
    point_3d = (1, 1, 2)
    cylindrical = cartesian_to_cylindrical(point_3d)
    back = cylindrical_to_cartesian(*cylindrical)
    print(f"   {point_3d} → (ρ={cylindrical[0]:.4f}, φ={cylindrical[1]:.4f}, z={cylindrical[2]}) → {back}")
    
    # 笛卡尔 ↔ 球坐标
    print(f"\n🔄 笛卡尔坐标 ↔ 球坐标:")
    point_3d = (0, 0, 1)
    spherical = cartesian_to_spherical(point_3d)
    back = spherical_to_cartesian(*spherical)
    print(f"   {point_3d} → (r={spherical[0]:.4f}, θ={spherical[1]:.4f}, φ={spherical[2]:.4f}) → {back}")


def example_triangle_analysis():
    """Demonstrate triangle analysis."""
    print_section("三角形分析")
    
    triangles = [
        (3, 4, 5, "勾股三角形"),
        (5, 5, 5, "等边三角形"),
        (5, 5, 6, "等腰三角形"),
        (2, 3, 4, "钝角三角形"),
    ]
    
    for a, b, c, name in triangles:
        print(f"\n🔺 {name} (边长 {a},{b},{c}):")
        print(f"   类型 (按边): {triangle_type_by_sides(a, b, c)}")
        print(f"   类型 (按角): {triangle_type_by_angles(a, b, c)}")
        print(f"   面积：{triangle_area_heron(a, b, c):.4f}")
        print(f"   周长：{triangle_perimeter(a, b, c)}")
        angles = triangle_angles(a, b, c)
        print(f"   角度：A={angles[0]:.2f}°, B={angles[1]:.2f}°, C={angles[2]:.2f}°")
        print(f"   是直角三角形：{is_right_triangle(a, b, c)}")
        print(f"   是勾股数：{pythagorean_triple_check(a, b, c)}")


def example_3d_shapes():
    """Demonstrate 3D shape calculations."""
    print_section("3D 形状计算")
    
    # 球体
    print(f"\n🔵 球体 (半径=3):")
    r = 3
    print(f"   体积：{sphere_volume(r):.4f}")
    print(f"   表面积：{sphere_surface_area(r):.4f}")
    
    # 立方体
    print(f"\n📦 立方体 (边长=4):")
    s = 4
    print(f"   体积：{cube_volume(s)}")
    print(f"   表面积：{cube_surface_area(s)}")
    
    # 圆柱
    print(f"\n🛢️ 圆柱 (半径=3, 高=5):")
    r, h = 3, 5
    print(f"   体积：{cylinder_volume(r, h):.4f}")
    print(f"   表面积：{cylinder_surface_area(r, h):.4f}")
    
    # 圆锥
    print(f"\n🔺 圆锥 (半径=3, 高=4):")
    r, h = 3, 4
    print(f"   体积：{cone_volume(r, h):.4f}")
    print(f"   表面积：{cone_surface_area(r, h):.4f}")
    
    # 四面体
    print(f"\n🔶 正四面体 (边长=4):")
    e = 4
    print(f"   体积：{tetrahedron_volume(e):.4f}")
    print(f"   表面积：{tetrahedron_surface_area(e):.4f}")


def example_polygon_operations():
    """Demonstrate polygon operations."""
    print_section("多边形操作")
    
    # 正方形
    square = [(0, 0), (4, 0), (4, 4), (0, 4)]
    print(f"\n⬜ 正方形 (边长=4):")
    print(f"   面积：{polygon_area(square)}")
    print(f"   周长：{polygon_perimeter(square)}")
    print(f"   是凸多边形：{is_convex_polygon(square)}")
    
    # 三角形
    triangle = [(0, 0), (3, 0), (0, 4)]
    print(f"\n🔺 三角形:")
    print(f"   面积：{polygon_area(triangle)}")
    print(f"   周长：{polygon_perimeter(triangle)}")
    print(f"   重心：{centroid_triangle(*triangle)}")
    
    # 五边形
    pentagon = [(math.cos(2 * PI * i / 5), math.sin(2 * PI * i / 5)) for i in range(5)]
    print(f"\n⭐ 正五边形 (外接圆半径=1):")
    print(f"   面积：{polygon_area(pentagon):.4f}")
    print(f"   周长：{polygon_perimeter(pentagon):.4f}")
    print(f"   是凸多边形：{is_convex_polygon(pentagon)}")
    
    # 插值
    print(f"\n📍 线性插值:")
    p1, p2 = (0, 0), (10, 10)
    print(f"   从 {p1} 到 {p2}:")
    for t in [0, 0.25, 0.5, 0.75, 1]:
        p = interpolate_points(p1, p2, t)
        print(f"   t={t}: {p}")


def example_practical_applications():
    """Demonstrate practical applications."""
    print_section("实际应用场景")
    
    # 游戏开发
    print(f"\n🎮 游戏开发 - 碰撞检测:")
    player_pos = (100, 100)
    enemy_pos = (110, 105)
    attack_range = 15
    in_range = point_in_circle(player_pos, enemy_pos, attack_range)
    print(f"   玩家 {player_pos} 在敌人 {enemy_pos} 攻击范围 {attack_range} 内：{in_range}")
    
    # 地图应用
    print(f"\n🗺️ 地图应用 - 附近搜索:")
    user_loc = (31.2304, 121.4737)  # 上海
    pois = [
        (31.2350, 121.4800, "东方明珠"),
        (31.2200, 121.4600, "人民广场"),
        (31.2500, 121.5000, "浦东机场"),
    ]
    max_dist = 0.02  # 约 2km
    nearby = [(name, distance_2d(user_loc, (lat, lon))) for lat, lon, name in pois if distance_2d(user_loc, (lat, lon)) <= max_dist]
    print(f"   用户位置：{user_loc}")
    print(f"   附近地点 (距离≤{max_dist}):")
    for name, dist in nearby:
        print(f"     - {name}: {dist:.4f}")
    
    # 物理模拟
    print(f"\n⚛️ 物理模拟 - 速度和动能:")
    mass = 10  # kg
    velocity = (3, 4)  # m/s
    speed = vector_magnitude_2d(velocity)
    ke = 0.5 * mass * speed * speed
    print(f"   质量：{mass} kg")
    print(f"   速度向量：{velocity} m/s")
    print(f"   速率：{speed} m/s")
    print(f"   动能：{ke} J")


def example_math_constants():
    """Demonstrate mathematical constants."""
    print_section("数学常量")
    
    print(f"\n📐 AllToolkit 数学常量:")
    print(f"   PI (π)        = {PI:.15f}")
    print(f"   E (e)         = {E:.15f}")
    print(f"   GOLDEN_RATIO  = {GOLDEN_RATIO:.15f}")
    print(f"   SQRT2 (√2)    = {SQRT2:.15f}")
    print(f"   SQRT3 (√3)    = {SQRT3:.15f}")
    
    print(f"\n💡 黄金比例应用:")
    print(f"   如果短边 = 100，长边 = {100 * GOLDEN_RATIO:.2f}")
    print(f"   如果长边 = 100，短边 = {100 / GOLDEN_RATIO:.2f}")


def main():
    """Run all examples."""
    print("\n" + "🔷" * 30)
    print("  AllToolkit Geometry Utils - 使用示例")
    print("🔷" * 30)
    
    example_basic_calculations()
    example_vector_operations()
    example_transformations()
    example_collision_detection()
    example_coordinate_conversions()
    example_triangle_analysis()
    example_3d_shapes()
    example_polygon_operations()
    example_practical_applications()
    example_math_constants()
    
    print("\n" + "=" * 60)
    print("  示例演示完成!")
    print("=" * 60)
    print("\n💡 提示：运行 geometry_utils_test.py 查看完整测试套件")
    print("📖 更多文档请查看 README.md\n")


if __name__ == '__main__':
    main()
