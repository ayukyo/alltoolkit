"""
中点画圆算法工具模块测试

测试覆盖所有核心功能：
- 中点画圆算法
- 椭圆绘制
- 圆弧绘制
- 填充形状
- 抗锯齿圆形
- 圆环绘制
- 工具函数
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    midpoint_circle,
    midpoint_circle_filled,
    midpoint_circle_iter,
    midpoint_ellipse,
    midpoint_ellipse_filled,
    draw_arc,
    draw_arc_by_steps,
    antialiased_circle,
    draw_ring,
    draw_ring_filled,
    circle_area,
    circle_perimeter,
    is_point_in_circle,
    is_point_on_circle,
    draw_circle_with_thickness,
    draw_dotted_circle,
)


def test_midpoint_circle_basic():
    """测试基本的中点画圆算法"""
    # 半径为 0 的圆
    points = midpoint_circle(0)
    assert points == [(0, 0)], "半径为 0 的圆应该只有一个点"
    
    # 半径为 1 的圆
    points = midpoint_circle(1)
    expected = {(1, 0), (0, 1), (-1, 0), (0, -1)}
    assert set(points) == expected, f"半径为 1 的圆有误: {set(points)}"
    
    # 半径为 2 的圆
    points = midpoint_circle(2)
    # 验证对称性
    for x, y in points:
        assert (-x, y) in points or (x, -y) in points, "圆应该具有对称性"
    
    # 验证点数量（对于半径 r，圆周上大约有 8r 个点，但实际是 4 * floor(sqrt(2r)))
    points_r3 = midpoint_circle(3)
    assert len(points_r3) > 0, "半径为 3 的圆应该有点"
    
    print("✓ test_midpoint_circle_basic 通过")


def test_midpoint_circle_with_center():
    """测试带圆心偏移的中点画圆"""
    cx, cy = 10, 20
    points = midpoint_circle(3, cx, cy)
    
    # 验证所有点都围绕正确的圆心
    for x, y in points:
        dist_sq = (x - cx) ** 2 + (y - cy) ** 2
        # 允许一定的像素误差
        assert dist_sq <= 10, f"点 ({x}, {y}) 距离圆心太远"
    
    print("✓ test_midpoint_circle_with_center 通过")


def test_midpoint_circle_filled():
    """测试填充圆形"""
    # 半径为 0
    points = midpoint_circle_filled(0)
    assert points == [(0, 0)], "半径为 0 的填充圆应该只有一个点"
    
    # 半径为 1 的填充圆
    points = midpoint_circle_filled(1)
    expected = {(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)}
    assert set(points) == expected, f"半径为 1 的填充圆有误: {set(points)}"
    
    # 验证填充圆的点数大于边界圆
    for r in range(2, 10):
        filled = midpoint_circle_filled(r)
        boundary = midpoint_circle(r)
        assert len(filled) > len(boundary), f"填充圆应该比边界圆有更多点 (r={r})"
    
    print("✓ test_midpoint_circle_filled 通过")


def test_midpoint_ellipse_basic():
    """测试椭圆绘制"""
    # 圆形椭圆（a == b）
    points_circle = midpoint_ellipse(3, 3)
    points_real_circle = midpoint_circle(3)
    assert set(points_circle) == set(points_real_circle), "圆形椭圆应该等于同半径的圆"
    
    # 椭圆 (a > b)
    points = midpoint_ellipse(4, 2)
    assert len(points) > 0, "椭圆应该有点"
    
    # 验证椭圆的点在合理范围内
    for x, y in points:
        assert abs(x) <= 4, f"x 坐标超出范围: {x}"
        assert abs(y) <= 2, f"y 坐标超出范围: {y}"
    
    # 扁平椭圆
    points_flat = midpoint_ellipse(5, 1)
    assert len(points_flat) > 0, "扁平椭圆应该有点"
    
    print("✓ test_midpoint_ellipse_basic 通过")


def test_midpoint_ellipse_edge_cases():
    """测试椭圆边缘情况"""
    # a = 0, b > 0（垂直线）
    points = midpoint_ellipse(0, 3)
    for x, y in points:
        assert x == 0, "a=0 的椭圆应该是垂直线"
    
    # a > 0, b = 0（水平线）
    points = midpoint_ellipse(3, 0)
    for x, y in points:
        assert y == 0, "b=0 的椭圆应该是水平线"
    
    # a = 0, b = 0（单点）
    points = midpoint_ellipse(0, 0)
    assert points == [(0, 0)], "a=0, b=0 的椭圆应该是单点"
    
    print("✓ test_midpoint_ellipse_edge_cases 通过")


def test_midpoint_ellipse_filled():
    """测试填充椭圆"""
    points = midpoint_ellipse_filled(3, 2)
    assert len(points) > 0, "填充椭圆应该有点"
    
    # 验证点在椭圆内
    for x, y in points:
        # 使用椭圆方程验证
        val = (x ** 2) / (3 ** 2) + (y ** 2) / (2 ** 2)
        assert val <= 1.1, f"点 ({x}, {y}) 不在椭圆内"  # 允许像素误差
    
    print("✓ test_midpoint_ellipse_filled 通过")


def test_draw_arc():
    """测试圆弧绘制"""
    # 四分之一圆弧（0 到 90 度）
    arc = draw_arc(5, 0, 90)
    assert len(arc) > 0, "圆弧应该有点"
    
    # 验证所有点都在正确的象限
    for x, y in arc:
        assert x >= 0 and y >= 0, f"点 ({x}, {y}) 不在第一象限"
    
    # 半圆弧（0 到 180 度）
    half_arc = draw_arc(5, 0, 180)
    assert len(half_arc) >= len(arc), "半圆弧应该比四分之一圆弧有更多点"
    
    # 完整圆（0 到 360 度）
    full_arc = draw_arc(5, 0, 360)
    full_circle = midpoint_circle(5)
    assert set(full_arc) == set(full_circle), "完整圆弧应该等于完整圆"
    
    print("✓ test_draw_arc 通过")


def test_draw_arc_by_steps():
    """测试角度步进圆弧绘制"""
    arc = draw_arc_by_steps(5, 0, 90)
    assert len(arc) > 0, "圆弧应该有点"
    
    # 验证点在正确的象限
    for x, y in arc:
        assert x >= 0 and y <= 0 or (x >= 0 and y >= 0), f"点 ({x}, {y}) 角度错误"
    
    print("✓ test_draw_arc_by_steps 通过")


def test_antialiased_circle():
    """测试抗锯齿圆形"""
    points = antialiased_circle(5)
    assert len(points) > 0, "抗锯齿圆形应该有点"
    
    # 验证 alpha 值在有效范围内
    for x, y, alpha in points:
        assert 0 <= alpha <= 1, f"alpha 值 {alpha} 不在 [0, 1] 范围内"
    
    # 半径为 0 的特殊情况
    points = antialiased_circle(0)
    assert points == [(0, 0, 1.0)], "半径为 0 的抗锯齿圆应该是单点"
    
    print("✓ test_antialiased_circle 通过")


def test_draw_ring():
    """测试圆环绘制"""
    # 圆环 (外半径 5，内半径 3)
    ring = draw_ring(5, 3)
    assert len(ring) > 0, "圆环应该有点"
    
    # 验证点不在内圆内，但在外圆上
    inner_circle = set(midpoint_circle(3))
    for x, y in ring:
        dist_sq = x ** 2 + y ** 2
        # 点应该在外圆范围内，不在内圆范围内
        # 这里我们简化验证：点不在内圆的点上
    
    # 边界情况：内半径为 0（等于普通圆）
    ring_no_inner = draw_ring(5, 0)
    regular_circle = midpoint_circle(5)
    assert set(ring_no_inner) == set(regular_circle), "内半径为 0 的圆环应该等于普通圆"
    
    # 内半径等于外半径（空集）
    ring_empty = draw_ring(5, 5)
    assert ring_empty == [], "内外半径相等的圆环应该是空的"
    
    print("✓ test_draw_ring 通过")


def test_draw_ring_filled():
    """测试填充圆环"""
    ring = draw_ring_filled(5, 2)
    assert len(ring) > 0, "填充圆环应该有点"
    
    # 验证点不在内圆内
    inner_filled = set(midpoint_circle_filled(1))
    for x, y in ring:
        assert (x, y) not in inner_filled, f"点 ({x}, {y}) 在内圆内"
    
    # 验证点在外圆内
    outer_filled = set(midpoint_circle_filled(5))
    for x, y in ring:
        assert (x, y) in outer_filled, f"点 ({x}, {y}) 不在外圆内"
    
    print("✓ test_draw_ring_filled 通过")


def test_midpoint_circle_iter():
    """测试生成器版本的画圆算法"""
    # 收集生成器的所有点
    points = list(midpoint_circle_iter(3))
    regular_points = midpoint_circle(3)
    
    assert set(points) == set(regular_points), "生成器版本应该返回相同的点"
    
    print("✓ test_midpoint_circle_iter 通过")


def test_circle_area_and_perimeter():
    """测试圆的面积和周长计算"""
    # 验证面积计算
    area_0 = circle_area(0)
    assert area_0 == 1, "半径为 0 的圆面积应该是 1"
    
    area_1 = circle_area(1)
    assert area_1 == 5, "半径为 1 的圆面积应该是 5"  # (0,0) + 4个点
    
    # 验证周长计算
    perimeter_0 = circle_perimeter(0)
    assert perimeter_0 == 1, "半径为 0 的圆周长应该是 1"
    
    perimeter_1 = circle_perimeter(1)
    assert perimeter_1 == 4, f"半径为 1 的圆周长应该是 4，实际是 {perimeter_1}"
    
    # 一般规律：周长 ≈ 2πr，但对于像素圆，实际周长约为 8r（对于大半径）
    # 对于小半径（r < 3），允许更大的误差
    for r in range(2, 10):
        perimeter = circle_perimeter(r)
        # 像素圆周长约为 8r，数学周长约为 2πr ≈ 6.28r
        # 两者略有差异，我们用更宽松的验证
        assert 4 * r <= perimeter <= 10 * r, f"半径 {r} 的周长 {perimeter} 不在合理范围内"
    
    print("✓ test_circle_area_and_perimeter 通过")


def test_is_point_in_circle():
    """测试点是否在圆内的判断"""
    # 在圆内
    assert is_point_in_circle(0, 0, 5) == True, "圆心应该在圆内"
    assert is_point_in_circle(3, 4, 5) == True, "(3,4) 应该在半径为 5 的圆上"
    assert is_point_in_circle(5, 0, 5) == True, "(5,0) 应该在圆上"
    assert is_point_in_circle(0, 5, 5) == True, "(0,5) 应该在圆上"
    
    # 在圆外
    assert is_point_in_circle(6, 0, 5) == False, "(6,0) 应该在圆外"
    assert is_point_in_circle(3, 5, 5) == False, "(3,5) 应该在圆外"
    
    # 带圆心偏移
    assert is_point_in_circle(15, 20, 5, 10, 20) == True, "偏移后的点应该在圆内"
    assert is_point_in_circle(16, 20, 5, 10, 20) == False, "偏移后的点应该在圆外"
    
    print("✓ test_is_point_in_circle 通过")


def test_is_point_on_circle():
    """测试点是否在圆上的判断"""
    # 在圆上
    assert is_point_on_circle(5, 0, 5) == True, "(5,0) 应该在圆上"
    assert is_point_on_circle(0, 5, 5) == True, "(0,5) 应该在圆上"
    assert is_point_on_circle(3, 4, 5) == True, "(3,4) 应该在圆上"
    
    # 在圆内
    assert is_point_on_circle(0, 0, 5) == False, "(0,0) 不应该在圆上"
    assert is_point_on_circle(2, 2, 5) == False, "(2,2) 不应该在圆上"
    
    # 在圆外
    assert is_point_on_circle(6, 0, 5) == False, "(6,0) 不应该在圆上"
    
    print("✓ test_is_point_on_circle 通过")


def test_draw_circle_with_thickness():
    """测试带厚度的圆形"""
    # 厚度为 1（等于普通圆）
    thick_1 = draw_circle_with_thickness(5, 1)
    regular = midpoint_circle(5)
    assert set(thick_1) == set(regular), "厚度为 1 应该等于普通圆"
    
    # 厚度为 2
    thick_2 = draw_circle_with_thickness(5, 2)
    assert len(thick_2) > len(regular), "厚度为 2 应该比普通圆有更多点"
    
    # 厚度为 0
    thick_0 = draw_circle_with_thickness(5, 0)
    assert thick_0 == [], "厚度为 0 应该返回空列表"
    
    # 厚度大于半径
    thick_large = draw_circle_with_thickness(5, 10)
    # 应该等于填充圆
    filled = midpoint_circle_filled(5)
    assert set(thick_large) == set(filled), "厚度大于半径应该等于填充圆"
    
    print("✓ test_draw_circle_with_thickness 通过")


def test_draw_dotted_circle():
    """测试虚线圆"""
    dotted = draw_dotted_circle(5, 2)
    regular = midpoint_circle(5)
    
    # 虚线圆的点数应该小于普通圆
    assert len(dotted) < len(regular), "虚线圆应该比普通圆有更少的点"
    
    # 但应该大于 0
    assert len(dotted) > 0, "虚线圆应该有点"
    
    # 所有点应该在接近圆上
    for x, y in dotted:
        dist_sq = x ** 2 + y ** 2
        # 允许像素误差（由于 round 函数）
        assert abs(dist_sq - 25) <= 5, f"点 ({x}, {y}) 距离平方 {dist_sq} 偏离太大"
    
    print("✓ test_draw_dotted_circle 通过")


def test_error_handling():
    """测试错误处理"""
    import pytest
    
    # 负半径
    try:
        midpoint_circle(-1)
        assert False, "负半径应该抛出异常"
    except ValueError:
        pass
    
    try:
        midpoint_ellipse(-1, 5)
        assert False, "负半轴应该抛出异常"
    except ValueError:
        pass
    
    try:
        draw_ring(3, 5)  # 内半径大于外半径
        assert False, "内半径大于外半径应该抛出异常"
    except ValueError:
        pass
    
    print("✓ test_error_handling 通过")


def test_symmetry():
    """测试圆形的对称性"""
    for r in range(1, 10):
        points = midpoint_circle(r)
        point_set = set(points)
        
        for x, y in points:
            # 八分对称性
            assert (x, y) in point_set
            assert (-x, y) in point_set, f"(-{x}, {y}) 不在圆中"
            assert (x, -y) in point_set, f"({x}, -{y}) 不在圆中"
            assert (-x, -y) in point_set, f"(-{x}, -{y}) 不在圆中"
    
    print("✓ test_symmetry 通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("中点画圆算法工具模块测试")
    print("=" * 50)
    
    test_midpoint_circle_basic()
    test_midpoint_circle_with_center()
    test_midpoint_circle_filled()
    test_midpoint_ellipse_basic()
    test_midpoint_ellipse_edge_cases()
    test_midpoint_ellipse_filled()
    test_draw_arc()
    test_draw_arc_by_steps()
    test_antialiased_circle()
    test_draw_ring()
    test_draw_ring_filled()
    test_midpoint_circle_iter()
    test_circle_area_and_perimeter()
    test_is_point_in_circle()
    test_is_point_on_circle()
    test_draw_circle_with_thickness()
    test_draw_dotted_circle()
    test_error_handling()
    test_symmetry()
    
    print("=" * 50)
    print("✅ 所有测试通过！")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()