#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Geometry Utilities Module
========================================
A comprehensive geometry calculation utility module for Python with zero external dependencies.

Features:
    - 2D/3D point operations
    - Distance calculations (Euclidean, Manhattan, Chebyshev)
    - Area and perimeter calculations for various shapes
    - Volume calculations for 3D shapes
    - Angle calculations and conversions
    - Vector operations (dot product, cross product, normalization)
    - Geometric transformations (rotation, translation, scaling)
    - Collision detection helpers
    - Coordinate system conversions

Author: AllToolkit Contributors
License: MIT
"""

import math
from typing import Any, Dict, List, Optional, Tuple, Union


# ============================================================================
# Type Aliases
# ============================================================================

Point2D = Tuple[float, float]
Point3D = Tuple[float, float, float]
Vector2D = Tuple[float, float]
Vector3D = Tuple[float, float, float]


# ============================================================================
# Constants
# ============================================================================

PI = math.pi
E = math.e
GOLDEN_RATIO = (1 + math.sqrt(5)) / 2
SQRT2 = math.sqrt(2)
SQRT3 = math.sqrt(3)


# ============================================================================
# Utility Functions
# ============================================================================

def _to_float(value: Any) -> float:
    """Convert value to float safely."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _is_number(value: Any) -> bool:
    """Check if value is a number."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


# ============================================================================
# Angle Conversions
# ============================================================================

def degrees_to_radians(degrees: float) -> float:
    """
    Convert degrees to radians.
    
    Args:
        degrees: Angle in degrees
    
    Returns:
        Angle in radians
    
    Example:
        >>> degrees_to_radians(180)
        3.141592653589793
        >>> degrees_to_radians(90)
        1.5707963267948966
    """
    return math.radians(degrees)


def radians_to_degrees(radians: float) -> float:
    """
    Convert radians to degrees.
    
    Args:
        radians: Angle in radians
    
    Returns:
        Angle in degrees
    
    Example:
        >>> radians_to_degrees(PI)
        180.0
        >>> radians_to_degrees(PI / 2)
        90.0
    """
    return math.degrees(radians)


def normalize_angle_degrees(angle: float) -> float:
    """
    Normalize angle to range [0, 360).
    
    Args:
        angle: Angle in degrees
    
    Returns:
        Normalized angle in degrees
    
    Example:
        >>> normalize_angle_degrees(450)
        90.0
        >>> normalize_angle_degrees(-90)
        270.0
    """
    return angle % 360.0


def normalize_angle_radians(angle: float) -> float:
    """
    Normalize angle to range [0, 2π).
    
    Args:
        angle: Angle in radians
    
    Returns:
        Normalized angle in radians
    
    Example:
        >>> round(normalize_angle_radians(2 * PI), 10)
        0.0
        >>> round(normalize_angle_radians(PI / 2), 10)
        1.5707963268
    """
    return angle % (2 * PI)


# ============================================================================
# Distance Calculations
# ============================================================================

def distance_2d(p1: Point2D, p2: Point2D) -> float:
    """
    Calculate Euclidean distance between two 2D points.
    
    Args:
        p1: First point (x, y)
        p2: Second point (x, y)
    
    Returns:
        Euclidean distance
    
    Example:
        >>> distance_2d((0, 0), (3, 4))
        5.0
    """
    x1, y1 = _to_float(p1[0]), _to_float(p1[1])
    x2, y2 = _to_float(p2[0]), _to_float(p2[1])
    # math.hypot is optimized for numerical stability and performance
    return math.hypot(x2 - x1, y2 - y1)


def distance_3d(p1: Point3D, p2: Point3D) -> float:
    """
    Calculate Euclidean distance between two 3D points.
    
    Args:
        p1: First point (x, y, z)
        p2: Second point (x, y, z)
    
    Returns:
        Euclidean distance
    
    Example:
        >>> distance_3d((0, 0, 0), (1, 2, 2))
        3.0
    
    Note:
        优化版本：Python 3.8+ 支持多参数 hypot，
        数值稳定性更好且性能更高。自动适配旧版本。
    """
    x1, y1, z1 = _to_float(p1[0]), _to_float(p1[1]), _to_float(p1[2])
    x2, y2, z2 = _to_float(p2[0]), _to_float(p2[1]), _to_float(p2[2])
    
    # Python 3.8+ 支持多参数 hypot，数值稳定性更好
    # 尝试使用多参数版本，失败则回退到嵌套版本
    try:
        return math.hypot(x2 - x1, y2 - y1, z2 - z1)
    except TypeError:
        # Python < 3.8 回退方案
        return math.hypot(math.hypot(x2 - x1, y2 - y1), z2 - z1)


def manhattan_distance_2d(p1: Point2D, p2: Point2D) -> float:
    """
    Calculate Manhattan (taxicab) distance between two 2D points.
    
    Args:
        p1: First point (x, y)
        p2: Second point (x, y)
    
    Returns:
        Manhattan distance
    
    Example:
        >>> manhattan_distance_2d((0, 0), (3, 4))
        7.0
    """
    x1, y1 = _to_float(p1[0]), _to_float(p1[1])
    x2, y2 = _to_float(p2[0]), _to_float(p2[1])
    return abs(x2 - x1) + abs(y2 - y1)


def chebyshev_distance_2d(p1: Point2D, p2: Point2D) -> float:
    """
    Calculate Chebyshev (chessboard) distance between two 2D points.
    
    Args:
        p1: First point (x, y)
        p2: Second point (x, y)
    
    Returns:
        Chebyshev distance
    
    Example:
        >>> chebyshev_distance_2d((0, 0), (3, 4))
        4.0
    """
    x1, y1 = _to_float(p1[0]), _to_float(p1[1])
    x2, y2 = _to_float(p2[0]), _to_float(p2[1])
    return max(abs(x2 - x1), abs(y2 - y1))


def distance_from_origin_2d(point: Point2D) -> float:
    """
    Calculate distance from origin to a 2D point.
    
    Args:
        point: Point (x, y)
    
    Returns:
        Distance from origin
    
    Example:
        >>> distance_from_origin_2d((3, 4))
        5.0
    """
    return distance_2d((0, 0), point)


def distance_from_origin_3d(point: Point3D) -> float:
    """
    Calculate distance from origin to a 3D point.
    
    Args:
        point: Point (x, y, z)
    
    Returns:
        Distance from origin
    
    Example:
        >>> distance_from_origin_3d((1, 2, 2))
        3.0
    """
    return distance_3d((0, 0, 0), point)


# ============================================================================
# 2D Shape Calculations
# ============================================================================

def circle_area(radius: float) -> float:
    """
    Calculate area of a circle.
    
    Args:
        radius: Circle radius
    
    Returns:
        Circle area
    
    Example:
        >>> round(circle_area(1), 10)
        3.1415926536
        >>> round(circle_area(2), 10)
        12.5663706144
    """
    r = _to_float(radius)
    if r < 0:
        return 0.0
    return PI * r * r


def circle_circumference(radius: float) -> float:
    """
    Calculate circumference of a circle.
    
    Args:
        radius: Circle radius
    
    Returns:
        Circle circumference
    
    Example:
        >>> round(circle_circumference(1), 10)
        6.2831853072
    """
    r = _to_float(radius)
    if r < 0:
        return 0.0
    return 2 * PI * r


def circle_diameter(radius: float) -> float:
    """
    Calculate diameter of a circle.
    
    Args:
        radius: Circle radius
    
    Returns:
        Circle diameter
    
    Example:
        >>> circle_diameter(5)
        10.0
    """
    r = _to_float(radius)
    if r < 0:
        return 0.0
    return 2 * r


def rectangle_area(width: float, height: float) -> float:
    """
    Calculate area of a rectangle.
    
    Args:
        width: Rectangle width
        height: Rectangle height
    
    Returns:
        Rectangle area
    
    Example:
        >>> rectangle_area(5, 3)
        15.0
    """
    w, h = _to_float(width), _to_float(height)
    if w < 0 or h < 0:
        return 0.0
    return w * h


def rectangle_perimeter(width: float, height: float) -> float:
    """
    Calculate perimeter of a rectangle.
    
    Args:
        width: Rectangle width
        height: Rectangle height
    
    Returns:
        Rectangle perimeter
    
    Example:
        >>> rectangle_perimeter(5, 3)
        16.0
    """
    w, h = _to_float(width), _to_float(height)
    if w < 0 or h < 0:
        return 0.0
    return 2 * (w + h)


def square_area(side: float) -> float:
    """
    Calculate area of a square.
    
    Args:
        side: Square side length
    
    Returns:
        Square area
    
    Example:
        >>> square_area(4)
        16.0
    """
    return rectangle_area(side, side)


def square_perimeter(side: float) -> float:
    """
    Calculate perimeter of a square.
    
    Args:
        side: Square side length
    
    Returns:
        Square perimeter
    
    Example:
        >>> square_perimeter(4)
        16.0
    """
    s = _to_float(side)
    if s < 0:
        return 0.0
    return 4 * s


def triangle_area(base: float, height: float) -> float:
    """
    Calculate area of a triangle using base and height.
    
    Args:
        base: Triangle base length
        height: Triangle height
    
    Returns:
        Triangle area
    
    Example:
        >>> triangle_area(6, 4)
        12.0
    """
    b, h = _to_float(base), _to_float(height)
    if b < 0 or h < 0:
        return 0.0
    return 0.5 * b * h


def triangle_area_heron(a: float, b: float, c: float) -> float:
    """
    Calculate area of a triangle using Heron's formula (three sides).
    
    Args:
        a: First side length
        b: Second side length
        c: Third side length
    
    Returns:
        Triangle area, or 0 if sides don't form a valid triangle
    
    Example:
        >>> round(triangle_area_heron(3, 4, 5), 10)
        6.0
        >>> triangle_area_heron(1, 2, 10)  # Invalid triangle
        0.0
    
    Note:
        优化版本：减少重复计算，使用提前返回优化，
        边界处理：负值和无效三角形快速返回 0。
    """
    a, b, c = _to_float(a), _to_float(b), _to_float(c)
    
    # 边界处理：快速检查无效输入（提前返回）
    if a <= 0 or b <= 0 or c <= 0:
        return 0.0
    
    # 三角形不等式验证（排序后只需一次比较）
    # 优化：找出最大边，只需一次比较验证
    max_side = max(a, b, c)
    sum_other = a + b + c - max_side
    if sum_other <= max_side:
        return 0.0
    
    # Heron's formula - 优化：减少乘法次数
    s = (a + b + c) * 0.5  # Semi-perimeter (避免除法)
    # 使用 s - max_side 来减少计算
    s_minus_max = s - max_side
    
    # 计算面积平方值（避免多次减法）
    area_squared = s * s_minus_max * (s - a) * (s - b)
    
    # 简化：如果 area_squared < 0 说明数值精度问题，返回 0
    return math.sqrt(max(area_squared, 0.0))


def triangle_perimeter(a: float, b: float, c: float) -> float:
    """
    Calculate perimeter of a triangle.
    
    Args:
        a: First side length
        b: Second side length
        c: Third side length
    
    Returns:
        Triangle perimeter
    
    Example:
        >>> triangle_perimeter(3, 4, 5)
        12.0
    """
    a, b, c = _to_float(a), _to_float(b), _to_float(c)
    if a <= 0 or b <= 0 or c <= 0:
        return 0.0
    return a + b + c


def equilateral_triangle_area(side: float) -> float:
    """
    Calculate area of an equilateral triangle.
    
    Args:
        side: Side length
    
    Returns:
        Triangle area
    
    Example:
        >>> round(equilateral_triangle_area(4), 10)
        6.9282032303
    """
    s = _to_float(side)
    if s < 0:
        return 0.0
    return (SQRT3 / 4) * s * s


def regular_polygon_area(n_sides: int, side_length: float) -> float:
    """
    Calculate area of a regular polygon.
    
    Args:
        n_sides: Number of sides (must be >= 3)
        side_length: Length of each side
    
    Returns:
        Polygon area
    
    Example:
        >>> round(regular_polygon_area(6, 4), 4)  # Hexagon
        41.5692
    """
    n = int(n_sides)
    s = _to_float(side_length)
    
    if n < 3 or s < 0:
        return 0.0
    
    # Area = (n * s²) / (4 * tan(π/n))
    return (n * s * s) / (4 * math.tan(PI / n))


def trapezoid_area(base1: float, base2: float, height: float) -> float:
    """
    Calculate area of a trapezoid.
    
    Args:
        base1: First base length
        base2: Second base length
        height: Height
    
    Returns:
        Trapezoid area
    
    Example:
        >>> trapezoid_area(5, 7, 4)
        24.0
    """
    b1, b2, h = _to_float(base1), _to_float(base2), _to_float(height)
    if b1 <= 0 or b2 <= 0 or h <= 0:
        return 0.0
    return 0.5 * (b1 + b2) * h


def ellipse_area(major_axis: float, minor_axis: float) -> float:
    """
    Calculate area of an ellipse.
    
    Args:
        major_axis: Major axis length (2a)
        minor_axis: Minor axis length (2b)
    
    Returns:
        Ellipse area
    
    Example:
        >>> round(ellipse_area(10, 6), 10)
        47.1238898038
    """
    a, b = _to_float(major_axis) / 2, _to_float(minor_axis) / 2
    if a < 0 or b < 0:
        return 0.0
    return PI * a * b


def ellipse_circumference_approx(major_axis: float, minor_axis: float) -> float:
    """
    Calculate approximate circumference of an ellipse (Ramanujan's formula).
    
    Args:
        major_axis: Major axis length (2a)
        minor_axis: Minor axis length (2b)
    
    Returns:
        Approximate ellipse circumference
    
    Example:
        >>> round(ellipse_circumference_approx(10, 6), 4)
        51.0539
    """
    a = _to_float(major_axis) / 2
    b = _to_float(minor_axis) / 2
    
    if a < 0 or b < 0:
        return 0.0
    
    h = ((a - b) ** 2) / ((a + b) ** 2)
    return PI * (a + b) * (1 + 3 * h / (10 + math.sqrt(4 - 3 * h)))


def rhombus_area(diagonal1: float, diagonal2: float) -> float:
    """
    Calculate area of a rhombus using diagonals.
    
    Args:
        diagonal1: First diagonal length
        diagonal2: Second diagonal length
    
    Returns:
        Rhombus area
    
    Example:
        >>> rhombus_area(8, 6)
        24.0
    """
    d1, d2 = _to_float(diagonal1), _to_float(diagonal2)
    if d1 < 0 or d2 < 0:
        return 0.0
    return 0.5 * d1 * d2


def parallelogram_area(base: float, height: float) -> float:
    """
    Calculate area of a parallelogram.
    
    Args:
        base: Base length
        height: Height
    
    Returns:
        Parallelogram area
    
    Example:
        >>> parallelogram_area(8, 5)
        40.0
    """
    b, h = _to_float(base), _to_float(height)
    if b < 0 or h < 0:
        return 0.0
    return b * h


# ============================================================================
# 3D Shape Calculations
# ============================================================================

def sphere_volume(radius: float) -> float:
    """
    Calculate volume of a sphere.
    
    Args:
        radius: Sphere radius
    
    Returns:
        Sphere volume
    
    Example:
        >>> round(sphere_volume(3), 10)
        113.0973355292
    """
    r = _to_float(radius)
    if r < 0:
        return 0.0
    return (4 / 3) * PI * r ** 3


def sphere_surface_area(radius: float) -> float:
    """
    Calculate surface area of a sphere.
    
    Args:
        radius: Sphere radius
    
    Returns:
        Sphere surface area
    
    Example:
        >>> round(sphere_surface_area(3), 10)
        113.0973355292
    """
    r = _to_float(radius)
    if r < 0:
        return 0.0
    return 4 * PI * r * r


def cube_volume(side: float) -> float:
    """
    Calculate volume of a cube.
    
    Args:
        side: Cube side length
    
    Returns:
        Cube volume
    
    Example:
        >>> cube_volume(3)
        27.0
    """
    s = _to_float(side)
    if s < 0:
        return 0.0
    return s ** 3


def cube_surface_area(side: float) -> float:
    """
    Calculate surface area of a cube.
    
    Args:
        side: Cube side length
    
    Returns:
        Cube surface area
    
    Example:
        >>> cube_surface_area(3)
        54.0
    """
    s = _to_float(side)
    if s < 0:
        return 0.0
    return 6 * s * s


def rectangular_prism_volume(length: float, width: float, height: float) -> float:
    """
    Calculate volume of a rectangular prism.
    
    Args:
        length: Prism length
        width: Prism width
        height: Prism height
    
    Returns:
        Prism volume
    
    Example:
        >>> rectangular_prism_volume(4, 3, 2)
        24.0
    """
    l, w, h = _to_float(length), _to_float(width), _to_float(height)
    if l < 0 or w < 0 or h < 0:
        return 0.0
    return l * w * h


def rectangular_prism_surface_area(length: float, width: float, height: float) -> float:
    """
    Calculate surface area of a rectangular prism.
    
    Args:
        length: Prism length
        width: Prism width
        height: Prism height
    
    Returns:
        Prism surface area
    
    Example:
        >>> rectangular_prism_surface_area(4, 3, 2)
        52.0
    """
    l, w, h = _to_float(length), _to_float(width), _to_float(height)
    if l < 0 or w < 0 or h < 0:
        return 0.0
    return 2 * (l * w + l * h + w * h)


def cylinder_volume(radius: float, height: float) -> float:
    """
    Calculate volume of a cylinder.
    
    Args:
        radius: Cylinder base radius
        height: Cylinder height
    
    Returns:
        Cylinder volume
    
    Example:
        >>> round(cylinder_volume(3, 5), 10)
        141.3716694115
    """
    r, h = _to_float(radius), _to_float(height)
    if r < 0 or h < 0:
        return 0.0
    return PI * r * r * h


def cylinder_surface_area(radius: float, height: float) -> float:
    """
    Calculate total surface area of a cylinder.
    
    Args:
        radius: Cylinder base radius
        height: Cylinder height
    
    Returns:
        Cylinder surface area
    
    Example:
        >>> round(cylinder_surface_area(3, 5), 10)
        150.7964473723
    """
    r, h = _to_float(radius), _to_float(height)
    if r < 0 or h < 0:
        return 0.0
    return 2 * PI * r * (r + h)


def cone_volume(radius: float, height: float) -> float:
    """
    Calculate volume of a cone.
    
    Args:
        radius: Cone base radius
        height: Cone height
    
    Returns:
        Cone volume
    
    Example:
        >>> round(cone_volume(3, 5), 10)
        47.1238898038
    """
    r, h = _to_float(radius), _to_float(height)
    if r < 0 or h < 0:
        return 0.0
    return (1 / 3) * PI * r * r * h


def cone_surface_area(radius: float, height: float) -> float:
    """
    Calculate total surface area of a cone (including base).
    
    Args:
        radius: Cone base radius
        height: Cone height
    
    Returns:
        Cone surface area
    
    Example:
        >>> round(cone_surface_area(3, 4), 10)
        75.3982236862
    """
    r, h = _to_float(radius), _to_float(height)
    if r < 0 or h < 0:
        return 0.0
    
    slant_height = math.sqrt(r * r + h * h)
    return PI * r * (r + slant_height)


def pyramid_volume(base_area: float, height: float) -> float:
    """
    Calculate volume of a pyramid.
    
    Args:
        base_area: Base area
        height: Pyramid height
    
    Returns:
        Pyramid volume
    
    Example:
        >>> pyramid_volume(25, 9)
        75.0
    """
    b, h = _to_float(base_area), _to_float(height)
    if b < 0 or h < 0:
        return 0.0
    return (1 / 3) * b * h


def tetrahedron_volume(edge: float) -> float:
    """
    Calculate volume of a regular tetrahedron.
    
    Args:
        edge: Edge length
    
    Returns:
        Tetrahedron volume
    
    Example:
        >>> round(tetrahedron_volume(4), 10)
        7.5424723327
    """
    e = _to_float(edge)
    if e < 0:
        return 0.0
    return (e ** 3) / (6 * SQRT2)


def tetrahedron_surface_area(edge: float) -> float:
    """
    Calculate surface area of a regular tetrahedron.
    
    Args:
        edge: Edge length
    
    Returns:
        Tetrahedron surface area
    
    Example:
        >>> round(tetrahedron_surface_area(4), 10)
        27.7128129211
    """
    e = _to_float(edge)
    if e < 0:
        return 0.0
    return SQRT3 * e * e


# ============================================================================
# Vector Operations
# ============================================================================

def vector_add_2d(v1: Vector2D, v2: Vector2D) -> Vector2D:
    """
    Add two 2D vectors.
    
    Args:
        v1: First vector (x, y)
        v2: Second vector (x, y)
    
    Returns:
        Result vector (x, y)
    
    Example:
        >>> vector_add_2d((1, 2), (3, 4))
        (4.0, 6.0)
    """
    return (_to_float(v1[0]) + _to_float(v2[0]), _to_float(v1[1]) + _to_float(v2[1]))


def vector_subtract_2d(v1: Vector2D, v2: Vector2D) -> Vector2D:
    """
    Subtract two 2D vectors.
    
    Args:
        v1: First vector (x, y)
        v2: Second vector (x, y)
    
    Returns:
        Result vector (x, y)
    
    Example:
        >>> vector_subtract_2d((5, 7), (2, 3))
        (3.0, 4.0)
    """
    return (_to_float(v1[0]) - _to_float(v2[0]), _to_float(v1[1]) - _to_float(v2[1]))


def vector_add_3d(v1: Vector3D, v2: Vector3D) -> Vector3D:
    """
    Add two 3D vectors.
    
    Args:
        v1: First vector (x, y, z)
        v2: Second vector (x, y, z)
    
    Returns:
        Result vector (x, y, z)
    
    Example:
        >>> vector_add_3d((1, 2, 3), (4, 5, 6))
        (5.0, 7.0, 9.0)
    """
    return (
        _to_float(v1[0]) + _to_float(v2[0]),
        _to_float(v1[1]) + _to_float(v2[1]),
        _to_float(v1[2]) + _to_float(v2[2])
    )


def vector_subtract_3d(v1: Vector3D, v2: Vector3D) -> Vector3D:
    """
    Subtract two 3D vectors.
    
    Args:
        v1: First vector (x, y, z)
        v2: Second vector (x, y, z)
    
    Returns:
        Result vector (x, y, z)
    
    Example:
        >>> vector_subtract_3d((5, 7, 9), (1, 2, 3))
        (4.0, 5.0, 6.0)
    """
    return (
        _to_float(v1[0]) - _to_float(v2[0]),
        _to_float(v1[1]) - _to_float(v2[1]),
        _to_float(v1[2]) - _to_float(v2[2])
    )


def vector_scale_2d(v: Vector2D, scalar: float) -> Vector2D:
    """
    Scale a 2D vector by a scalar.
    
    Args:
        v: Vector (x, y)
        scalar: Scaling factor
    
    Returns:
        Scaled vector (x, y)
    
    Example:
        >>> vector_scale_2d((2, 3), 2)
        (4.0, 6.0)
    """
    s = _to_float(scalar)
    return (_to_float(v[0]) * s, _to_float(v[1]) * s)


def vector_scale_3d(v: Vector3D, scalar: float) -> Vector3D:
    """
    Scale a 3D vector by a scalar.
    
    Args:
        v: Vector (x, y, z)
        scalar: Scaling factor
    
    Returns:
        Scaled vector (x, y, z)
    
    Example:
        >>> vector_scale_3d((2, 3, 4), 2)
        (4.0, 6.0, 8.0)
    """
    s = _to_float(scalar)
    return (
        _to_float(v[0]) * s,
        _to_float(v[1]) * s,
        _to_float(v[2]) * s
    )


def dot_product_2d(v1: Vector2D, v2: Vector2D) -> float:
    """
    Calculate dot product of two 2D vectors.
    
    Args:
        v1: First vector (x, y)
        v2: Second vector (x, y)
    
    Returns:
        Dot product
    
    Example:
        >>> dot_product_2d((1, 2), (3, 4))
        11.0
    """
    return _to_float(v1[0]) * _to_float(v2[0]) + _to_float(v1[1]) * _to_float(v2[1])


def dot_product_3d(v1: Vector3D, v2: Vector3D) -> float:
    """
    Calculate dot product of two 3D vectors.
    
    Args:
        v1: First vector (x, y, z)
        v2: Second vector (x, y, z)
    
    Returns:
        Dot product
    
    Example:
        >>> dot_product_3d((1, 2, 3), (4, 5, 6))
        32.0
    """
    return (
        _to_float(v1[0]) * _to_float(v2[0]) +
        _to_float(v1[1]) * _to_float(v2[1]) +
        _to_float(v1[2]) * _to_float(v2[2])
    )


def cross_product_3d(v1: Vector3D, v2: Vector3D) -> Vector3D:
    """
    Calculate cross product of two 3D vectors.
    
    Args:
        v1: First vector (x, y, z)
        v2: Second vector (x, y, z)
    
    Returns:
        Cross product vector (x, y, z)
    
    Example:
        >>> cross_product_3d((1, 0, 0), (0, 1, 0))
        (0.0, 0.0, 1.0)
    """
    x1, y1, z1 = _to_float(v1[0]), _to_float(v1[1]), _to_float(v1[2])
    x2, y2, z2 = _to_float(v2[0]), _to_float(v2[1]), _to_float(v2[2])
    
    return (
        y1 * z2 - z1 * y2,
        z1 * x2 - x1 * z2,
        x1 * y2 - y1 * x2
    )


def vector_magnitude_2d(v: Vector2D) -> float:
    """
    Calculate magnitude (length) of a 2D vector.
    
    Args:
        v: Vector (x, y)
    
    Returns:
        Vector magnitude
    
    Example:
        >>> vector_magnitude_2d((3, 4))
        5.0
    """
    # math.hypot is optimized for numerical stability and performance
    return math.hypot(_to_float(v[0]), _to_float(v[1]))


def vector_magnitude_3d(v: Vector3D) -> float:
    """
    Calculate magnitude (length) of a 3D vector.
    
    Args:
        v: Vector (x, y, z)
    
    Returns:
        Vector magnitude
    
    Example:
        >>> vector_magnitude_3d((1, 2, 2))
        3.0
    """
    # For Python < 3.8, use nested hypot which is still optimized for numerical stability
    return math.hypot(math.hypot(_to_float(v[0]), _to_float(v[1])), _to_float(v[2]))


def normalize_vector_2d(v: Vector2D) -> Vector2D:
    """
    Normalize a 2D vector to unit length.
    
    Args:
        v: Vector (x, y)
    
    Returns:
        Normalized vector (x, y), or (0, 0) if zero vector
    
    Example:
        >>> normalize_vector_2d((3, 4))
        (0.6, 0.8)
    """
    mag = vector_magnitude_2d(v)
    if mag == 0:
        return (0.0, 0.0)
    return (_to_float(v[0]) / mag, _to_float(v[1]) / mag)


def normalize_vector_3d(v: Vector3D) -> Vector3D:
    """
    Normalize a 3D vector to unit length.
    
    Args:
        v: Vector (x, y, z)
    
    Returns:
        Normalized vector (x, y, z), or (0, 0, 0) if zero vector
    
    Example:
        >>> normalize_vector_3d((1, 2, 2))
        (0.3333333333333333, 0.6666666666666666, 0.6666666666666666)
    """
    mag = vector_magnitude_3d(v)
    if mag == 0:
        return (0.0, 0.0, 0.0)
    return (
        _to_float(v[0]) / mag,
        _to_float(v[1]) / mag,
        _to_float(v[2]) / mag
    )


def vector_angle_2d(v: Vector2D) -> float:
    """
    Calculate angle of a 2D vector from positive x-axis (in radians).
    
    Args:
        v: Vector (x, y)
    
    Returns:
        Angle in radians [-π, π]
    
    Example:
        >>> round(vector_angle_2d((1, 0)), 10)
        0.0
        >>> round(vector_angle_2d((0, 1)), 10)
        1.5707963268
    """
    return math.atan2(_to_float(v[1]), _to_float(v[0]))


def angle_between_vectors_2d(v1: Vector2D, v2: Vector2D) -> float:
    """
    Calculate angle between two 2D vectors (in radians).
    
    Args:
        v1: First vector (x, y)
        v2: Second vector (x, y)
    
    Returns:
        Angle in radians [0, π]
    
    Example:
        >>> round(angle_between_vectors_2d((1, 0), (0, 1)), 10)
        1.5707963268
    """
    dot = dot_product_2d(v1, v2)
    mag1 = vector_magnitude_2d(v1)
    mag2 = vector_magnitude_2d(v2)
    
    if mag1 == 0 or mag2 == 0:
        return 0.0
    
    cos_angle = dot / (mag1 * mag2)
    # Clamp to [-1, 1] to handle floating point errors
    cos_angle = max(-1, min(1, cos_angle))
    return math.acos(cos_angle)


# ============================================================================
# Geometric Transformations
# ============================================================================

def rotate_point_2d(point: Point2D, angle_degrees: float, origin: Point2D = (0, 0)) -> Point2D:
    """
    Rotate a 2D point around an origin.
    
    Args:
        point: Point to rotate (x, y)
        angle_degrees: Rotation angle in degrees (counter-clockwise)
        origin: Rotation origin (default: (0, 0))
    
    Returns:
        Rotated point (x, y)
    
    Example:
        >>> # Rotate (1, 0) by 90 degrees around origin
        >>> rotated = rotate_point_2d((1, 0), 90)
        >>> round(rotated[0], 10), round(rotated[1], 10)
        (0.0, 1.0)
    """
    x, y = _to_float(point[0]), _to_float(point[1])
    ox, oy = _to_float(origin[0]), _to_float(origin[1])
    angle = degrees_to_radians(angle_degrees)
    
    # Translate to origin
    tx, ty = x - ox, y - oy
    
    # Rotate
    cos_a, sin_a = math.cos(angle), math.sin(angle)
    rx = tx * cos_a - ty * sin_a
    ry = tx * sin_a + ty * cos_a
    
    # Translate back
    return (rx + ox, ry + oy)


def translate_point_2d(point: Point2D, dx: float, dy: float) -> Point2D:
    """
    Translate a 2D point by a vector.
    
    Args:
        point: Point to translate (x, y)
        dx: X translation
        dy: Y translation
    
    Returns:
        Translated point (x, y)
    
    Example:
        >>> translate_point_2d((1, 2), 3, 4)
        (4.0, 6.0)
    """
    return (_to_float(point[0]) + _to_float(dx), _to_float(point[1]) + _to_float(dy))


def scale_point_2d(point: Point2D, scale_x: float, scale_y: float, origin: Point2D = (0, 0)) -> Point2D:
    """
    Scale a 2D point from an origin.
    
    Args:
        point: Point to scale (x, y)
        scale_x: X scale factor
        scale_y: Y scale factor
        origin: Scale origin (default: (0, 0))
    
    Returns:
        Scaled point (x, y)
    
    Example:
        >>> scale_point_2d((2, 3), 2, 2)
        (4.0, 6.0)
    """
    x, y = _to_float(point[0]), _to_float(point[1])
    ox, oy = _to_float(origin[0]), _to_float(origin[1])
    sx, sy = _to_float(scale_x), _to_float(scale_y)
    
    return ((x - ox) * sx + ox, (y - oy) * sy + oy)


def reflect_point_x(point: Point2D) -> Point2D:
    """
    Reflect a 2D point across the x-axis.
    
    Args:
        point: Point to reflect (x, y)
    
    Returns:
        Reflected point (x, -y)
    
    Example:
        >>> reflect_point_x((3, 4))
        (3.0, -4.0)
    """
    return (_to_float(point[0]), -_to_float(point[1]))


def reflect_point_y(point: Point2D) -> Point2D:
    """
    Reflect a 2D point across the y-axis.
    
    Args:
        point: Point to reflect (x, y)
    
    Returns:
        Reflected point (-x, y)
    
    Example:
        >>> reflect_point_y((3, 4))
        (-3.0, 4.0)
    """
    return (-_to_float(point[0]), _to_float(point[1]))


def reflect_point_origin(point: Point2D) -> Point2D:
    """
    Reflect a 2D point across the origin.
    
    Args:
        point: Point to reflect (x, y)
    
    Returns:
        Reflected point (-x, -y)
    
    Example:
        >>> reflect_point_origin((3, 4))
        (-3.0, -4.0)
    """
    return (-_to_float(point[0]), -_to_float(point[1]))


# ============================================================================
# Collision Detection
# ============================================================================

def point_in_rectangle(point: Point2D, rect_top_left: Point2D, rect_bottom_right: Point2D) -> bool:
    """
    Check if a point is inside a rectangle (axis-aligned).
    
    Args:
        point: Point to check (x, y)
        rect_top_left: Rectangle top-left corner (x, y)
        rect_bottom_right: Rectangle bottom-right corner (x, y)
    
    Returns:
        True if point is inside or on edge
    
    Example:
        >>> point_in_rectangle((2, 2), (0, 0), (4, 4))
        True
        >>> point_in_rectangle((5, 5), (0, 0), (4, 4))
        False
    """
    px, py = _to_float(point[0]), _to_float(point[1])
    x1, y1 = _to_float(rect_top_left[0]), _to_float(rect_top_left[1])
    x2, y2 = _to_float(rect_bottom_right[0]), _to_float(rect_bottom_right[1])
    
    min_x, max_x = min(x1, x2), max(x1, x2)
    min_y, max_y = min(y1, y2), max(y1, y2)
    
    return min_x <= px <= max_x and min_y <= py <= max_y


def point_in_circle(point: Point2D, center: Point2D, radius: float) -> bool:
    """
    Check if a point is inside a circle.
    
    Args:
        point: Point to check (x, y)
        center: Circle center (x, y)
        radius: Circle radius
    
    Returns:
        True if point is inside or on edge
    
    Example:
        >>> point_in_circle((2, 2), (0, 0), 3)
        True
        >>> point_in_circle((4, 4), (0, 0), 3)
        False
    """
    return distance_2d(point, center) <= _to_float(radius)


def circles_intersect(c1_center: Point2D, c1_radius: float, c2_center: Point2D, c2_radius: float) -> bool:
    """
    Check if two circles intersect.
    
    Args:
        c1_center: First circle center (x, y)
        c1_radius: First circle radius
        c2_center: Second circle center (x, y)
        c2_radius: Second circle radius
    
    Returns:
        True if circles intersect or touch
    
    Example:
        >>> circles_intersect((0, 0), 2, (3, 0), 2)
        True
        >>> circles_intersect((0, 0), 1, (5, 0), 1)
        False
    """
    r1, r2 = _to_float(c1_radius), _to_float(c2_radius)
    dist = distance_2d(c1_center, c2_center)
    return dist <= (r1 + r2)


def rectangles_intersect(rect1_tl: Point2D, rect1_br: Point2D, rect2_tl: Point2D, rect2_br: Point2D) -> bool:
    """
    Check if two axis-aligned rectangles intersect.
    
    Args:
        rect1_tl: First rectangle top-left (x, y)
        rect1_br: First rectangle bottom-right (x, y)
        rect2_tl: Second rectangle top-left (x, y)
        rect2_br: Second rectangle bottom-right (x, y)
    
    Returns:
        True if rectangles intersect
    
    Example:
        >>> rectangles_intersect((0, 0), (4, 4), (2, 2), (6, 6))
        True
        >>> rectangles_intersect((0, 0), (2, 2), (3, 3), (5, 5))
        False
    """
    x1_min, y1_min = _to_float(rect1_tl[0]), _to_float(rect1_tl[1])
    x1_max, y1_max = _to_float(rect1_br[0]), _to_float(rect1_br[1])
    x2_min, y2_min = _to_float(rect2_tl[0]), _to_float(rect2_tl[1])
    x2_max, y2_max = _to_float(rect2_br[0]), _to_float(rect2_br[1])
    
    # Normalize coordinates
    x1_min, x1_max = min(x1_min, x1_max), max(x1_min, x1_max)
    y1_min, y1_max = min(y1_min, y1_max), max(y1_min, y1_max)
    x2_min, x2_max = min(x2_min, x2_max), max(x2_min, x2_max)
    y2_min, y2_max = min(y2_min, y2_max), max(y2_min, y2_max)
    
    # Check for overlap
    return not (x1_max < x2_min or x2_max < x1_min or y1_max < y2_min or y2_max < y1_min)


# ============================================================================
# Coordinate Conversions
# ============================================================================

def cartesian_to_polar(point: Point2D) -> Tuple[float, float]:
    """
    Convert Cartesian coordinates to polar coordinates.
    
    Args:
        point: Point in Cartesian (x, y)
    
    Returns:
        Polar coordinates (radius, angle_in_radians)
    
    Example:
        >>> cartesian_to_polar((1, 1))
        (1.4142135623730951, 0.7853981633974483)
    """
    x, y = _to_float(point[0]), _to_float(point[1])
    r = math.sqrt(x * x + y * y)
    theta = math.atan2(y, x)
    return (r, theta)


def polar_to_cartesian(radius: float, angle_radians: float) -> Point2D:
    """
    Convert polar coordinates to Cartesian coordinates.
    
    Args:
        radius: Distance from origin
        angle_radians: Angle in radians
    
    Returns:
        Cartesian coordinates (x, y)
    
    Example:
        >>> polar_to_cartesian(1, 0)
        (1.0, 0.0)
        >>> round(polar_to_cartesian(1, PI/2)[0], 10), round(polar_to_cartesian(1, PI/2)[1], 10)
        (0.0, 1.0)
    """
    r = _to_float(radius)
    theta = _to_float(angle_radians)
    return (r * math.cos(theta), r * math.sin(theta))


def cartesian_to_cylindrical(point: Point3D) -> Tuple[float, float, float]:
    """
    Convert Cartesian coordinates to cylindrical coordinates.
    
    Args:
        point: Point in Cartesian (x, y, z)
    
    Returns:
        Cylindrical coordinates (rho, phi, z)
    
    Example:
        >>> cartesian_to_cylindrical((1, 1, 2))
        (1.4142135623730951, 0.7853981633974483, 2.0)
    """
    x, y, z = _to_float(point[0]), _to_float(point[1]), _to_float(point[2])
    rho = math.sqrt(x * x + y * y)
    phi = math.atan2(y, x)
    return (rho, phi, z)


def cylindrical_to_cartesian(rho: float, phi: float, z: float) -> Point3D:
    """
    Convert cylindrical coordinates to Cartesian coordinates.
    
    Args:
        rho: Radial distance
        phi: Angle in radians
        z: Height
    
    Returns:
        Cartesian coordinates (x, y, z)
    
    Example:
        >>> cylindrical_to_cartesian(1, 0, 2)
        (1.0, 0.0, 2.0)
    """
    r, p, z = _to_float(rho), _to_float(phi), _to_float(z)
    return (r * math.cos(p), r * math.sin(p), z)


def cartesian_to_spherical(point: Point3D) -> Tuple[float, float, float]:
    """
    Convert Cartesian coordinates to spherical coordinates.
    
    Args:
        point: Point in Cartesian (x, y, z)
    
    Returns:
        Spherical coordinates (r, theta, phi)
        - r: radial distance
        - theta: polar angle (from positive z-axis)
        - phi: azimuthal angle (from positive x-axis in xy-plane)
    
    Example:
        >>> cartesian_to_spherical((0, 0, 1))
        (1.0, 0.0, 0.0)
    """
    x, y, z = _to_float(point[0]), _to_float(point[1]), _to_float(point[2])
    r = math.sqrt(x * x + y * y + z * z)
    
    if r == 0:
        return (0, 0, 0)
    
    theta = math.acos(z / r)  # Polar angle
    phi = math.atan2(y, x)    # Azimuthal angle
    
    return (r, theta, phi)


def spherical_to_cartesian(r: float, theta: float, phi: float) -> Point3D:
    """
    Convert spherical coordinates to Cartesian coordinates.
    
    Args:
        r: Radial distance
        theta: Polar angle (from positive z-axis) in radians
        phi: Azimuthal angle (from positive x-axis) in radians
    
    Returns:
        Cartesian coordinates (x, y, z)
    
    Example:
        >>> spherical_to_cartesian(1, 0, 0)
        (0.0, 0.0, 1.0)
    """
    r, t, p = _to_float(r), _to_float(theta), _to_float(phi)
    x = r * math.sin(t) * math.cos(p)
    y = r * math.sin(t) * math.sin(p)
    z = r * math.cos(t)
    return (x, y, z)


# ============================================================================
# Triangle Functions
# ============================================================================

def triangle_type_by_sides(a: float, b: float, c: float) -> str:
    """
    Classify triangle by side lengths.
    
    Args:
        a: First side length
        b: Second side length
        c: Third side length
    
    Returns:
        'equilateral', 'isosceles', 'scalene', or 'invalid'
    
    Example:
        >>> triangle_type_by_sides(3, 3, 3)
        'equilateral'
        >>> triangle_type_by_sides(3, 4, 5)
        'scalene'
        >>> triangle_type_by_sides(3, 3, 5)
        'isosceles'
    """
    a, b, c = _to_float(a), _to_float(b), _to_float(c)
    
    # Check validity
    if a <= 0 or b <= 0 or c <= 0:
        return 'invalid'
    if a + b <= c or a + c <= b or b + c <= a:
        return 'invalid'
    
    if a == b == c:
        return 'equilateral'
    elif a == b or b == c or a == c:
        return 'isosceles'
    else:
        return 'scalene'


def triangle_type_by_angles(a: float, b: float, c: float) -> str:
    """
    Classify triangle by angles (using side lengths).
    
    Args:
        a: First side length
        b: Second side length
        c: Third side length
    
    Returns:
        'acute', 'right', 'obtuse', or 'invalid'
    
    Example:
        >>> triangle_type_by_angles(3, 4, 5)
        'right'
        >>> triangle_type_by_angles(5, 5, 5)
        'acute'
    """
    a, b, c = _to_float(a), _to_float(b), _to_float(c)
    
    # Check validity
    if a <= 0 or b <= 0 or c <= 0:
        return 'invalid'
    if a + b <= c or a + c <= b or b + c <= a:
        return 'invalid'
    
    # Sort sides
    sides = sorted([a, b, c])
    a, b, c = sides[0], sides[1], sides[2]
    
    # Use law of cosines to determine angle type
    # c² = a² + b² - 2ab*cos(C)
    # If c² = a² + b², right triangle
    # If c² < a² + b², acute triangle
    # If c² > a² + b², obtuse triangle
    
    c_squared = c * c
    ab_sum = a * a + b * b
    
    # Use small epsilon for floating point comparison
    epsilon = 1e-10
    
    if abs(c_squared - ab_sum) < epsilon:
        return 'right'
    elif c_squared < ab_sum:
        return 'acute'
    else:
        return 'obtuse'


def triangle_angles(a: float, b: float, c: float) -> Tuple[float, float, float]:
    """
    Calculate all three angles of a triangle (in degrees).
    
    Args:
        a: First side length (opposite to angle A)
        b: Second side length (opposite to angle B)
        c: Third side length (opposite to angle C)
    
    Returns:
        Tuple of angles (A, B, C) in degrees
    
    Example:
        >>> angles = triangle_angles(3, 4, 5)
        >>> round(angles[0], 6), round(angles[1], 6), round(angles[2], 6)
        (36.869898, 53.130102, 90.0)
    """
    a, b, c = _to_float(a), _to_float(b), _to_float(c)
    
    # Check validity
    if a <= 0 or b <= 0 or c <= 0:
        return (0.0, 0.0, 0.0)
    if a + b <= c or a + c <= b or b + c <= a:
        return (0.0, 0.0, 0.0)
    
    # Law of cosines
    def angle_opposite(x, y, z):
        """Calculate angle opposite to side z, given sides x, y, z."""
        cos_val = (x * x + y * y - z * z) / (2 * x * y)
        cos_val = max(-1, min(1, cos_val))  # Clamp for floating point errors
        return math.degrees(math.acos(cos_val))
    
    angle_a = angle_opposite(b, c, a)
    angle_b = angle_opposite(a, c, b)
    angle_c = angle_opposite(a, b, c)
    
    return (angle_a, angle_b, angle_c)


def is_right_triangle(a: float, b: float, c: float) -> bool:
    """
    Check if a triangle is a right triangle.
    
    Args:
        a: First side length
        b: Second side length
        c: Third side length
    
    Returns:
        True if right triangle
    
    Example:
        >>> is_right_triangle(3, 4, 5)
        True
        >>> is_right_triangle(5, 12, 13)
        True
    """
    return triangle_type_by_angles(a, b, c) == 'right'


def pythagorean_triple_check(a: int, b: int, c: int) -> bool:
    """
    Check if three integers form a Pythagorean triple.
    
    Args:
        a: First integer
        b: Second integer
        c: Third integer
    
    Returns:
        True if a² + b² = c² (in any order)
    
    Example:
        >>> pythagorean_triple_check(3, 4, 5)
        True
        >>> pythagorean_triple_check(5, 12, 13)
        True
    """
    sides = sorted([abs(int(a)), abs(int(b)), abs(int(c))])
    return sides[0] ** 2 + sides[1] ** 2 == sides[2] ** 2


# ============================================================================
# Miscellaneous Functions
# ============================================================================

def midpoint_2d(p1: Point2D, p2: Point2D) -> Point2D:
    """
    Calculate midpoint between two 2D points.
    
    Args:
        p1: First point (x, y)
        p2: Second point (x, y)
    
    Returns:
        Midpoint (x, y)
    
    Example:
        >>> midpoint_2d((0, 0), (4, 6))
        (2.0, 3.0)
    """
    return (
        (_to_float(p1[0]) + _to_float(p2[0])) / 2,
        (_to_float(p1[1]) + _to_float(p2[1])) / 2
    )


def midpoint_3d(p1: Point3D, p2: Point3D) -> Point3D:
    """
    Calculate midpoint between two 3D points.
    
    Args:
        p1: First point (x, y, z)
        p2: Second point (x, y, z)
    
    Returns:
        Midpoint (x, y, z)
    
    Example:
        >>> midpoint_3d((0, 0, 0), (4, 6, 8))
        (2.0, 3.0, 4.0)
    """
    return (
        (_to_float(p1[0]) + _to_float(p2[0])) / 2,
        (_to_float(p1[1]) + _to_float(p2[1])) / 2,
        (_to_float(p1[2]) + _to_float(p2[2])) / 2
    )


def centroid_triangle(p1: Point2D, p2: Point2D, p3: Point2D) -> Point2D:
    """
    Calculate centroid (center of mass) of a triangle.
    
    Args:
        p1: First vertex (x, y)
        p2: Second vertex (x, y)
        p3: Third vertex (x, y)
    
    Returns:
        Centroid (x, y)
    
    Example:
        >>> centroid_triangle((0, 0), (3, 0), (0, 3))
        (1.0, 1.0)
    """
    return (
        (_to_float(p1[0]) + _to_float(p2[0]) + _to_float(p3[0])) / 3,
        (_to_float(p1[1]) + _to_float(p2[1]) + _to_float(p3[1])) / 3
    )


def polygon_area(vertices: List[Point2D]) -> float:
    """
    Calculate area of a polygon using the Shoelace formula.
    
    Args:
        vertices: List of vertices in order [(x1, y1), (x2, y2), ...]
    
    Returns:
        Polygon area (always positive)
    
    Example:
        >>> # Square with side 2
        >>> polygon_area([(0, 0), (2, 0), (2, 2), (0, 2)])
        4.0
    """
    if len(vertices) < 3:
        return 0.0
    
    n = len(vertices)
    area = 0.0
    
    for i in range(n):
        j = (i + 1) % n
        xi, yi = _to_float(vertices[i][0]), _to_float(vertices[i][1])
        xj, yj = _to_float(vertices[j][0]), _to_float(vertices[j][1])
        area += xi * yj - xj * yi
    
    return abs(area) / 2


def polygon_perimeter(vertices: List[Point2D]) -> float:
    """
    Calculate perimeter of a polygon.
    
    Args:
        vertices: List of vertices in order [(x1, y1), (x2, y2), ...]
    
    Returns:
        Polygon perimeter
    
    Example:
        >>> # Square with side 2
        >>> polygon_perimeter([(0, 0), (2, 0), (2, 2), (0, 2)])
        8.0
    """
    if len(vertices) < 3:
        return 0.0
    
    n = len(vertices)
    perimeter = 0.0
    
    for i in range(n):
        j = (i + 1) % n
        perimeter += distance_2d(vertices[i], vertices[j])
    
    return perimeter


def is_convex_polygon(vertices: List[Point2D]) -> bool:
    """
    Check if a polygon is convex.
    
    Args:
        vertices: List of vertices in order [(x1, y1), (x2, y2), ...]
    
    Returns:
        True if polygon is convex
    
    Example:
        >>> is_convex_polygon([(0, 0), (2, 0), (2, 2), (0, 2)])
        True
    """
    if len(vertices) < 3:
        return False
    
    n = len(vertices)
    sign = None
    
    for i in range(n):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % n]
        p3 = vertices[(i + 2) % n]
        
        # Cross product of vectors (p2-p1) and (p3-p2)
        cross = (
            (_to_float(p2[0]) - _to_float(p1[0])) * (_to_float(p3[1]) - _to_float(p2[1])) -
            (_to_float(p2[1]) - _to_float(p1[1])) * (_to_float(p3[0]) - _to_float(p2[0]))
        )
        
        if cross != 0:
            current_sign = cross > 0
            if sign is None:
                sign = current_sign
            elif sign != current_sign:
                return False
    
    return True


def interpolate_points(p1: Point2D, p2: Point2D, t: float) -> Point2D:
    """
    Linearly interpolate between two points.
    
    Args:
        p1: Start point (x, y)
        p2: End point (x, y)
        t: Interpolation factor (0 = p1, 1 = p2)
    
    Returns:
        Interpolated point (x, y)
    
    Example:
        >>> interpolate_points((0, 0), (10, 10), 0.5)
        (5.0, 5.0)
    """
    t = _to_float(t)
    return (
        _to_float(p1[0]) + t * (_to_float(p2[0]) - _to_float(p1[0])),
        _to_float(p1[1]) + t * (_to_float(p2[1]) - _to_float(p1[1]))
    )


def slope(p1: Point2D, p2: Point2D) -> Optional[float]:
    """
    Calculate slope of line through two points.
    
    Args:
        p1: First point (x, y)
        p2: Second point (x, y)
    
    Returns:
        Slope, or None if vertical line
    
    Example:
        >>> slope((0, 0), (2, 4))
        2.0
        >>> slope((1, 1), (1, 5))  # Vertical line
        None
    """
    x1, y1 = _to_float(p1[0]), _to_float(p1[1])
    x2, y2 = _to_float(p2[0]), _to_float(p2[1])
    
    dx = x2 - x1
    if dx == 0:
        return None  # Vertical line
    
    return (y2 - y1) / dx


def line_equation(p1: Point2D, p2: Point2D) -> Tuple[Optional[float], Optional[float]]:
    """
    Get line equation in slope-intercept form (y = mx + b).
    
    Args:
        p1: First point on line (x, y)
        p2: Second point on line (x, y)
    
    Returns:
        Tuple (slope, y_intercept), or (None, x_value) for vertical lines
    
    Example:
        >>> line_equation((0, 0), (2, 4))
        (2.0, 0.0)
    """
    m = slope(p1, p2)
    
    if m is None:
        # Vertical line
        return (None, _to_float(p1[0]))
    
    # y = mx + b => b = y - mx
    b = _to_float(p1[1]) - m * _to_float(p1[0])
    return (m, b)


def point_to_line_distance(point: Point2D, line_p1: Point2D, line_p2: Point2D) -> float:
    """
    Calculate perpendicular distance from a point to a line.
    
    Args:
        point: Point (x, y)
        line_p1: First point on line (x, y)
        line_p2: Second point on line (x, y)
    
    Returns:
        Perpendicular distance
    
    Example:
        >>> round(point_to_line_distance((0, 0), (1, 1), (2, 2)), 10)
        0.0
    """
    x0, y0 = _to_float(point[0]), _to_float(point[1])
    x1, y1 = _to_float(line_p1[0]), _to_float(line_p1[1])
    x2, y2 = _to_float(line_p2[0]), _to_float(line_p2[1])
    
    # Line equation: (y2-y1)x - (x2-x1)y + x2*y1 - y2*x1 = 0
    a = y2 - y1
    b = -(x2 - x1)
    c = x2 * y1 - y2 * x1
    
    denominator = math.sqrt(a * a + b * b)
    if denominator == 0:
        return distance_2d(point, line_p1)
    
    return abs(a * x0 + b * y0 + c) / denominator


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    # Constants
    'PI', 'E', 'GOLDEN_RATIO', 'SQRT2', 'SQRT3',
    
    # Type aliases
    'Point2D', 'Point3D', 'Vector2D', 'Vector3D',
    
    # Angle conversions
    'degrees_to_radians', 'radians_to_degrees',
    'normalize_angle_degrees', 'normalize_angle_radians',
    
    # Distance calculations
    'distance_2d', 'distance_3d',
    'manhattan_distance_2d', 'chebyshev_distance_2d',
    'distance_from_origin_2d', 'distance_from_origin_3d',
    
    # 2D shapes
    'circle_area', 'circle_circumference', 'circle_diameter',
    'rectangle_area', 'rectangle_perimeter',
    'square_area', 'square_perimeter',
    'triangle_area', 'triangle_area_heron', 'triangle_perimeter',
    'equilateral_triangle_area', 'regular_polygon_area',
    'trapezoid_area', 'ellipse_area', 'ellipse_circumference_approx',
    'rhombus_area', 'parallelogram_area',
    
    # 3D shapes
    'sphere_volume', 'sphere_surface_area',
    'cube_volume', 'cube_surface_area',
    'rectangular_prism_volume', 'rectangular_prism_surface_area',
    'cylinder_volume', 'cylinder_surface_area',
    'cone_volume', 'cone_surface_area',
    'pyramid_volume', 'tetrahedron_volume', 'tetrahedron_surface_area',
    
    # Vector operations
    'vector_add_2d', 'vector_subtract_2d', 'vector_scale_2d',
    'vector_add_3d', 'vector_subtract_3d', 'vector_scale_3d',
    'dot_product_2d', 'dot_product_3d', 'cross_product_3d',
    'vector_magnitude_2d', 'vector_magnitude_3d',
    'normalize_vector_2d', 'normalize_vector_3d',
    'vector_angle_2d', 'angle_between_vectors_2d',
    
    # Transformations
    'rotate_point_2d', 'translate_point_2d', 'scale_point_2d',
    'reflect_point_x', 'reflect_point_y', 'reflect_point_origin',
    
    # Collision detection
    'point_in_rectangle', 'point_in_circle',
    'circles_intersect', 'rectangles_intersect',
    
    # Coordinate conversions
    'cartesian_to_polar', 'polar_to_cartesian',
    'cartesian_to_cylindrical', 'cylindrical_to_cartesian',
    'cartesian_to_spherical', 'spherical_to_cartesian',
    
    # Triangle functions
    'triangle_type_by_sides', 'triangle_type_by_angles',
    'triangle_angles', 'is_right_triangle', 'pythagorean_triple_check',
    
    # Miscellaneous
    'midpoint_2d', 'midpoint_3d', 'centroid_triangle',
    'polygon_area', 'polygon_perimeter', 'is_convex_polygon',
    'interpolate_points', 'slope', 'line_equation',
    'point_to_line_distance',
]


if __name__ == '__main__':
    # Quick demo
    print("AllToolkit Geometry Utils Demo")
    print("=" * 40)
    
    # Distance
    p1, p2 = (0, 0), (3, 4)
    print(f"Distance between {p1} and {p2}: {distance_2d(p1, p2)}")
    
    # Circle
    r = 5
    print(f"Circle (r={r}): Area={circle_area(r):.2f}, Circumference={circle_circumference(r):.2f}")
    
    # Triangle
    print(f"Triangle (3,4,5): Area={triangle_area_heron(3, 4, 5)}, Type={triangle_type_by_angles(3, 4, 5)}")
    
    # Vector
    v1, v2 = (1, 2), (3, 4)
    print(f"Dot product of {v1} and {v2}: {dot_product_2d(v1, v2)}")
    
    # Rotation
    point = (1, 0)
    rotated = rotate_point_2d(point, 90)
    print(f"Rotate {point} by 90°: ({rotated[0]:.2f}, {rotated[1]:.2f})")
    
    print("\nFor full documentation, see README.md")
