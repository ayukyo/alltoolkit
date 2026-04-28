"""
中点画圆算法工具模块 (Midpoint Circle Algorithm Utils)

提供高效的圆形、椭圆、弧线绘制算法，基于经典的 Bresenham 中点算法。
所有函数返回像素坐标列表，适用于图形渲染、图像处理等场景。

核心功能：
1. 中点画圆算法 - 高效生成圆形像素坐标
2. 中点椭圆算法 - 生成椭圆像素坐标
3. 圆弧绘制 - 生成部分圆弧的像素坐标
4. 填充圆/椭圆 - 生成填充形状的所有像素坐标
5. 抗锯齿圆形 - 使用 Xiaolin Wu 算法的抗锯齿圆形

零外部依赖，纯 Python 实现。
"""

from typing import List, Tuple, Generator
import math


def midpoint_circle(radius: int, cx: int = 0, cy: int = 0) -> List[Tuple[int, int]]:
    """
    使用中点画圆算法生成圆形的像素坐标。
    
    基于 Bresenham 算法，仅使用整数运算，效率极高。
    利用八分对称性，一次计算八个对称点。
    
    Args:
        radius: 圆的半径（必须为非负整数）
        cx: 圆心 X 坐标，默认 0
        cy: 圆心 Y 坐标，默认 0
    
    Returns:
        圆形上所有像素坐标的列表 [(x, y), ...]
    
    Raises:
        ValueError: 如果半径为负数
    
    Example:
        >>> points = midpoint_circle(3)
        >>> len(points)
        16
        >>> (3, 0) in points
        True
    """
    if radius < 0:
        raise ValueError("半径必须为非负整数")
    
    if radius == 0:
        return [(cx, cy)]
    
    points = set()
    x = 0
    y = radius
    d = 1 - radius  # 决策参数
    
    while x <= y:
        # 利用八分对称性，添加八个对称点
        points.update([
            (cx + x, cy + y),
            (cx + y, cy + x),
            (cx - x, cy + y),
            (cx - y, cy + x),
            (cx + x, cy - y),
            (cx + y, cy - x),
            (cx - x, cy - y),
            (cx - y, cy - x),
        ])
        
        x += 1
        if d < 0:
            d += 2 * x + 1
        else:
            y -= 1
            d += 2 * (x - y) + 1
    
    return list(points)


def midpoint_circle_filled(radius: int, cx: int = 0, cy: int = 0) -> List[Tuple[int, int]]:
    """
    生成填充圆形的所有像素坐标。
    
    Args:
        radius: 圆的半径（必须为非负整数）
        cx: 圆心 X 坐标，默认 0
        cy: 圆心 Y 坐标，默认 0
    
    Returns:
        填充圆形内所有像素坐标的列表
    
    Example:
        >>> points = midpoint_circle_filled(2)
        >>> len(points)
        13
    """
    if radius < 0:
        raise ValueError("半径必须为非负整数")
    
    if radius == 0:
        return [(cx, cy)]
    
    points = set()
    
    for r in range(radius + 1):
        x = 0
        y = r
        d = 1 - r
        
        while x <= y:
            # 对于填充圆，我们需要画水平线而不是点
            for i in range(-x, x + 1):
                points.add((cx + i, cy + y))
                points.add((cx + i, cy - y))
            for i in range(-y, y + 1):
                points.add((cx + i, cy + x))
                points.add((cx + i, cy - x))
            
            x += 1
            if d < 0:
                d += 2 * x + 1
            else:
                y -= 1
                d += 2 * (x - y) + 1
    
    return list(points)


def midpoint_ellipse(a: int, b: int, cx: int = 0, cy: int = 0) -> List[Tuple[int, int]]:
    """
    使用中点椭圆算法生成椭圆的像素坐标。
    
    将椭圆分为两个区域分别处理，保证在任意长宽比下都能正确绘制。
    
    Args:
        a: 椭圆的长半轴（X方向半径，必须为非负整数）
        b: 椭圆的短半轴（Y方向半径，必须为非负整数）
        cx: 椭圆中心 X 坐标，默认 0
        cy: 椭圆中心 Y 坐标，默认 0
    
    Returns:
        椭圆上所有像素坐标的列表
    
    Raises:
        ValueError: 如果任一半径为负数
    
    Example:
        >>> points = midpoint_ellipse(4, 2)
        >>> len(points) > 0
        True
    """
    if a < 0 or b < 0:
        raise ValueError("半轴必须为非负整数")
    
    if a == 0 and b == 0:
        return [(cx, cy)]
    if a == 0:
        return [(cx, cy + i) for i in range(-b, b + 1)]
    if b == 0:
        return [(cx + i, cy) for i in range(-a, a + 1)]
    
    points = []
    x = 0
    y = b
    
    a_sq = a * a
    b_sq = b * b
    
    # 区域1: 斜率 |dy/dx| < 1
    d1 = b_sq - a_sq * b + 0.25 * a_sq
    
    while a_sq * (y - 0.5) > b_sq * (x + 1):
        points.extend([
            (cx + x, cy + y),
            (cx - x, cy + y),
            (cx + x, cy - y),
            (cx - x, cy - y),
        ])
        
        x += 1
        if d1 < 0:
            d1 += b_sq * (2 * x + 1)
        else:
            y -= 1
            d1 += b_sq * (2 * x + 1) + a_sq * (-2 * y + 2)
    
    # 区域2: 斜率 |dy/dx| >= 1
    d2 = b_sq * (x + 0.5) ** 2 + a_sq * (y - 1) ** 2 - a_sq * b_sq
    
    while y >= 0:
        points.extend([
            (cx + x, cy + y),
            (cx - x, cy + y),
            (cx + x, cy - y),
            (cx - x, cy - y),
        ])
        
        y -= 1
        if d2 > 0:
            d2 += a_sq * (-2 * y + 3)
        else:
            x += 1
            d2 += b_sq * (2 * x + 2) + a_sq * (-2 * y + 3)
    
    return points


def midpoint_ellipse_filled(a: int, b: int, cx: int = 0, cy: int = 0) -> List[Tuple[int, int]]:
    """
    生成填充椭圆的所有像素坐标。
    
    Args:
        a: 椭圆的长半轴（X方向半径）
        b: 椭圆的短半轴（Y方向半径）
        cx: 椭圆中心 X 坐标，默认 0
        cy: 椭圆中心 Y 坐标，默认 0
    
    Returns:
        填充椭圆内所有像素坐标的列表
    
    Example:
        >>> points = midpoint_ellipse_filled(3, 2)
        >>> len(points) > 0
        True
    """
    if a < 0 or b < 0:
        raise ValueError("半轴必须为非负整数")
    
    if a == 0 and b == 0:
        return [(cx, cy)]
    
    points = set()
    
    # 使用扫描线填充
    for y in range(-b, b + 1):
        # 根据椭圆方程计算每个 y 值对应的 x 范围
        if b == 0:
            continue
        x_range = a * math.sqrt(1 - (y * y) / (b * b))
        x_max = int(math.floor(x_range))
        
        for x in range(-x_max, x_max + 1):
            points.add((cx + x, cy + y))
    
    return list(points)


def draw_arc(radius: int, start_angle: float, end_angle: float, 
             cx: int = 0, cy: int = 0) -> List[Tuple[int, int]]:
    """
    绘制圆弧，支持任意角度范围。
    
    Args:
        radius: 圆弧半径（必须为非负整数）
        start_angle: 起始角度（度数，0度为右侧，逆时针为正）
        end_angle: 结束角度（度数）
        cx: 圆心 X 坐标，默认 0
        cy: 圆心 Y 坐标，默认 0
    
    Returns:
        圆弧上所有像素坐标的列表
    
    Example:
        >>> # 绘制四分之一圆弧（从0度到90度）
        >>> arc = draw_arc(5, 0, 90)
        >>> len(arc) > 0
        True
    """
    if radius < 0:
        raise ValueError("半径必须为非负整数")
    
    if radius == 0:
        return [(cx, cy)]
    
    # 计算角度差，判断是否为完整圆
    angle_diff = end_angle - start_angle
    
    # 如果角度差是 360 的整数倍，返回完整圆
    if abs(angle_diff) >= 360 and abs(angle_diff % 360) < 0.001:
        return midpoint_circle(radius, cx, cy)
    
    # 标准化角度到 0-360 范围
    start_angle = start_angle % 360
    end_angle = end_angle % 360
    
    points = set()
    
    # 遍历圆上的所有点
    full_circle = midpoint_circle(radius, 0, 0)
    
    for px, py in full_circle:
        # 计算点相对于圆心的角度
        angle = math.degrees(math.atan2(py, px))
        if angle < 0:
            angle += 360
        
        # 检查角度是否在弧线范围内
        if start_angle <= end_angle:
            if start_angle <= angle <= end_angle:
                points.add((cx + px, cy + py))
        else:
            # 跨越 0 度的情况
            if angle >= start_angle or angle <= end_angle:
                points.add((cx + px, cy + py))
    
    return list(points)


def draw_arc_by_steps(radius: int, start_angle: float, end_angle: float,
                      cx: int = 0, cy: int = 0) -> List[Tuple[int, int]]:
    """
    使用角度步进方式绘制圆弧（更精确但可能较慢）。
    
    Args:
        radius: 圆弧半径
        start_angle: 起始角度（度数）
        end_angle: 结束角度（度数）
        cx: 圆心 X 坐标
        cy: 圆心 Y 坐标
    
    Returns:
        圆弧上所有像素坐标的列表
    """
    if radius < 0:
        raise ValueError("半径必须为非负整数")
    
    if radius == 0:
        return [(cx, cy)]
    
    points = set()
    
    # 转换为弧度
    start_rad = math.radians(start_angle)
    end_rad = math.radians(end_angle)
    
    # 计算弧长，决定采样点数量
    angle_diff = abs(end_rad - start_rad)
    arc_length = radius * angle_diff
    num_steps = max(int(arc_length * 2), 20)  # 每单位弧长至少2个采样点
    
    for i in range(num_steps + 1):
        t = i / num_steps
        angle = start_rad + t * (end_rad - start_rad)
        
        x = cx + int(round(radius * math.cos(angle)))
        y = cy + int(round(radius * math.sin(angle)))
        points.add((x, y))
    
    return list(points)


def antialiased_circle(radius: int, cx: int = 0, cy: int = 0) -> List[Tuple[int, int, float]]:
    """
    使用 Xiaolin Wu 算法生成抗锯齿圆形。
    
    返回像素坐标及其对应的 alpha 值（0.0-1.0），
    可用于平滑渲染圆形边缘。
    
    Args:
        radius: 圆的半径
        cx: 圆心 X 坐标
        cy: 圆心 Y 坐标
    
    Returns:
        列表，每个元素为 (x, y, alpha) 元组
    
    Example:
        >>> points = antialiased_circle(5)
        >>> all(0 <= alpha <= 1 for _, _, alpha in points)
        True
    """
    if radius < 0:
        raise ValueError("半径必须为非负整数")
    
    if radius == 0:
        return [(cx, cy, 1.0)]
    
    points = []
    
    def plot_aa(x: int, y: int, alpha: float):
        """添加抗锯齿点，利用对称性"""
        if 0 < alpha < 1:
            points.extend([
                (cx + x, cy + y, alpha),
                (cx + y, cy + x, alpha),
                (cx - x, cy + y, alpha),
                (cx - y, cy + x, alpha),
                (cx + x, cy - y, alpha),
                (cx + y, cy - x, alpha),
                (cx - x, cy - y, alpha),
                (cx - y, cy - x, alpha),
            ])
    
    x = 0
    y = radius
    
    while x <= y:
        # 计算精确的 y 值
        y_exact = math.sqrt(radius * radius - x * x)
        y_int = int(y_exact)
        y_frac = y_exact - y_int
        
        # 绘制整数部分
        points.extend([
            (cx + x, cy + y_int, 1.0 - y_frac),
            (cx + y_int, cy + x, 1.0 - y_frac),
            (cx - x, cy + y_int, 1.0 - y_frac),
            (cx - y_int, cy + x, 1.0 - y_frac),
            (cx + x, cy - y_int, 1.0 - y_frac),
            (cx + y_int, cy - x, 1.0 - y_frac),
            (cx - x, cy - y_int, 1.0 - y_frac),
            (cx - y_int, cy - x, 1.0 - y_frac),
        ])
        
        # 如果有小数部分，绘制额外的点
        if y_frac > 0 and y_int > 0:
            plot_aa(x, y_int - 1, y_frac)
        
        x += 1
    
    return points


def draw_ring(outer_radius: int, inner_radius: int, 
              cx: int = 0, cy: int = 0) -> List[Tuple[int, int]]:
    """
    绘制圆环（环形）的像素坐标。
    
    Args:
        outer_radius: 外圆半径
        inner_radius: 内圆半径（孔的半径）
        cx: 圆心 X 坐标
        cy: 圆心 Y 坐标
    
    Returns:
        圆环上所有像素坐标的列表
    
    Raises:
        ValueError: 如果内半径大于外半径或半径为负
    
    Example:
        >>> ring = draw_ring(5, 3)
        >>> len(ring) > 0
        True
    """
    if outer_radius < 0 or inner_radius < 0:
        raise ValueError("半径必须为非负整数")
    
    if inner_radius > outer_radius:
        raise ValueError("内半径不能大于外半径")
    
    if inner_radius == outer_radius:
        return []
    
    if inner_radius == 0:
        return midpoint_circle(outer_radius, cx, cy)
    
    outer_points = set(midpoint_circle(outer_radius, 0, 0))
    inner_points = set(midpoint_circle(inner_radius, 0, 0))
    
    # 计算圆环上的点（在外圆上但不在内圆内）
    ring_points = []
    
    for r in range(inner_radius, outer_radius + 1):
        if r == 0:
            continue
        circle_at_r = midpoint_circle(r, 0, 0)
        for px, py in circle_at_r:
            ring_points.append((cx + px, cy + py))
    
    # 去重
    return list(set(ring_points))


def draw_ring_filled(outer_radius: int, inner_radius: int,
                     cx: int = 0, cy: int = 0) -> List[Tuple[int, int]]:
    """
    绘制填充圆环（环形区域）的所有像素坐标。
    
    Args:
        outer_radius: 外圆半径
        inner_radius: 内圆半径
        cx: 圆心 X 坐标
        cy: 圆心 Y 坐标
    
    Returns:
        填充圆环内所有像素坐标的列表
    
    Example:
        >>> ring = draw_ring_filled(5, 2)
        >>> len(ring) > 0
        True
    """
    if outer_radius < 0 or inner_radius < 0:
        raise ValueError("半径必须为非负整数")
    
    if inner_radius > outer_radius:
        raise ValueError("内半径不能大于外半径")
    
    outer_points = set(midpoint_circle_filled(outer_radius, 0, 0))
    inner_points = set()
    
    if inner_radius > 0:
        inner_points = set(midpoint_circle_filled(inner_radius - 1, 0, 0))
    
    # 返回在外圆内但不在内圆内的点
    result = []
    for px, py in outer_points:
        if (px, py) not in inner_points:
            result.append((cx + px, cy + py))
    
    return result


def midpoint_circle_iter(radius: int, cx: int = 0, cy: int = 0) -> Generator[Tuple[int, int], None, None]:
    """
    中点画圆算法的生成器版本，适用于流式处理或大半径圆形。
    
    Args:
        radius: 圆的半径
        cx: 圆心 X 坐标
        cy: 圆心 Y 坐标
    
    Yields:
        每次迭代产生一个像素坐标元组 (x, y)
    
    Example:
        >>> points = list(midpoint_circle_iter(3))
        >>> len(points)
        16
    """
    if radius < 0:
        raise ValueError("半径必须为非负整数")
    
    if radius == 0:
        yield (cx, cy)
        return
    
    x = 0
    y = radius
    d = 1 - radius
    
    while x <= y:
        yield (cx + x, cy + y)
        yield (cx + y, cy + x)
        yield (cx - x, cy + y)
        yield (cx - y, cy + x)
        yield (cx + x, cy - y)
        yield (cx + y, cy - x)
        yield (cx - x, cy - y)
        yield (cx - y, cy - x)
        
        x += 1
        if d < 0:
            d += 2 * x + 1
        else:
            y -= 1
            d += 2 * (x - y) + 1


def circle_area(radius: int) -> int:
    """
    计算填充圆形的像素数量（使用 Pick 定理的近似）。
    
    Args:
        radius: 圆的半径
    
    Returns:
        填充圆形的像素数量
    
    Example:
        >>> circle_area(5)
        81
    """
    if radius < 0:
        raise ValueError("半径必须为非负整数")
    
    if radius == 0:
        return 1
    
    # 使用精确公式: π * r² 的整数近似
    # 实际像素数可能与这个值略有不同
    return len(midpoint_circle_filled(radius))


def circle_perimeter(radius: int) -> int:
    """
    计算圆形周长的像素数量。
    
    Args:
        radius: 圆的半径
    
    Returns:
        圆形周长的像素数量
    
    Example:
        >>> circle_perimeter(5)
        32
    """
    if radius < 0:
        raise ValueError("半径必须为非负整数")
    
    if radius == 0:
        return 1
    
    return len(midpoint_circle(radius))


def is_point_in_circle(x: int, y: int, radius: int, cx: int = 0, cy: int = 0) -> bool:
    """
    判断点是否在圆内或圆上。
    
    Args:
        x: 点的 X 坐标
        y: 点的 Y 坐标
        radius: 圆的半径
        cx: 圆心 X 坐标
        cy: 圆心 Y 坐标
    
    Returns:
        如果点在圆内或圆上返回 True，否则返回 False
    
    Example:
        >>> is_point_in_circle(2, 2, 5)
        True
        >>> is_point_in_circle(6, 0, 5)
        False
    """
    if radius < 0:
        raise ValueError("半径必须为非负整数")
    
    dx = x - cx
    dy = y - cy
    return dx * dx + dy * dy <= radius * radius


def is_point_on_circle(x: int, y: int, radius: int, cx: int = 0, cy: int = 0) -> bool:
    """
    判断点是否恰好在圆上。
    
    Args:
        x: 点的 X 坐标
        y: 点的 Y 坐标
        radius: 圆的半径
        cx: 圆心 X 坐标
        cy: 圆心 Y 坐标
    
    Returns:
        如果点在圆上返回 True，否则返回 False
    
    Example:
        >>> is_point_on_circle(5, 0, 5)
        True
        >>> is_point_on_circle(3, 4, 5)
        True
    """
    if radius < 0:
        raise ValueError("半径必须为非负整数")
    
    dx = x - cx
    dy = y - cy
    return dx * dx + dy * dy == radius * radius


def draw_circle_with_thickness(radius: int, thickness: int = 1,
                               cx: int = 0, cy: int = 0) -> List[Tuple[int, int]]:
    """
    绘制指定线宽的圆形。
    
    Args:
        radius: 圆的半径（外半径）
        thickness: 线宽（像素数，从外向内计算）
        cx: 圆心 X 坐标
        cy: 圆心 Y 坐标
    
    Returns:
        所有像素坐标的列表
    
    Example:
        >>> circle = draw_circle_with_thickness(5, 2)
        >>> len(circle) > len(midpoint_circle(5))
        True
    """
    if radius < 0:
        raise ValueError("半径必须为非负整数")
    
    if thickness <= 0:
        return []
    
    # 如果厚度大于半径，返回填充圆
    if thickness > radius:
        return midpoint_circle_filled(radius, cx, cy)
    
    points = set()
    
    for r in range(max(0, radius - thickness + 1), radius + 1):
        circle_points = midpoint_circle(r, 0, 0)
        for px, py in circle_points:
            points.add((cx + px, cy + py))
    
    return list(points)


def draw_dotted_circle(radius: int, dot_spacing: int = 2,
                       cx: int = 0, cy: int = 0) -> List[Tuple[int, int]]:
    """
    绘制虚线圆（点状圆）。
    
    Args:
        radius: 圆的半径
        dot_spacing: 点之间的间距（像素数）
        cx: 圆心 X 坐标
        cy: 圆心 Y 坐标
    
    Returns:
        虚线圆的像素坐标列表
    
    Example:
        >>> dotted = draw_dotted_circle(5, 3)
        >>> len(dotted) < len(midpoint_circle(5))
        True
    """
    if radius < 0:
        raise ValueError("半径必须为非负整数")
    
    if radius == 0:
        return [(cx, cy)]
    
    if dot_spacing < 1:
        dot_spacing = 1
    
    # 使用角度步进绘制
    circumference = 2 * math.pi * radius
    num_dots = max(1, int(circumference / (dot_spacing + 1)))
    
    points = []
    for i in range(num_dots):
        angle = 2 * math.pi * i / num_dots
        x = cx + int(round(radius * math.cos(angle)))
        y = cy + int(round(radius * math.sin(angle)))
        points.append((x, y))
    
    return points


# 模块信息
__all__ = [
    'midpoint_circle',
    'midpoint_circle_filled',
    'midpoint_circle_iter',
    'midpoint_ellipse',
    'midpoint_ellipse_filled',
    'draw_arc',
    'draw_arc_by_steps',
    'antialiased_circle',
    'draw_ring',
    'draw_ring_filled',
    'circle_area',
    'circle_perimeter',
    'is_point_in_circle',
    'is_point_on_circle',
    'draw_circle_with_thickness',
    'draw_dotted_circle',
]

__version__ = '1.0.0'
__author__ = 'AllToolkit'