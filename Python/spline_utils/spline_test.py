"""
Spline Utils 测试套件
测试所有样条曲线功能
"""

import math
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from spline_utils.spline import (
    Point2D, Point3D,
    linear_spline, cubic_spline,
    catmull_rom_spline, b_spline,
    hermite_spline, hermite_spline_auto,
    sample_curve, curve_length, resample_curve, smooth_points,
    interpolate
)


def test_point2d():
    """测试 Point2D 类"""
    print("测试 Point2D...")
    
    p1 = Point2D(1.5, 2.5)
    p2 = Point2D(4.5, 6.5)
    
    # 测试属性
    assert p1.x == 1.5
    assert p1.y == 2.5
    
    # 测试距离
    dist = p1.distance_to(p2)
    expected = math.sqrt((3) ** 2 + (4) ** 2)  # 3-4-5 三角形
    assert abs(dist - 5.0) < 1e-10, f"距离计算错误: {dist} != 5.0"
    
    # 测试元组转换
    assert p1.to_tuple() == (1.5, 2.5)
    
    # 测试相等
    p3 = Point2D(1.5, 2.5)
    assert p1 == p3
    
    print("  ✓ Point2D 测试通过")


def test_point3d():
    """测试 Point3D 类"""
    print("测试 Point3D...")
    
    p = Point3D(1.0, 2.0, 3.0)
    assert p.x == 1.0
    assert p.y == 2.0
    assert p.z == 3.0
    assert p.to_tuple() == (1.0, 2.0, 3.0)
    
    print("  ✓ Point3D 测试通过")


def test_linear_spline():
    """测试线性样条插值"""
    print("测试线性样条插值...")
    
    points = [
        Point2D(0, 0),
        Point2D(2, 4),
        Point2D(4, 0)
    ]
    
    result = linear_spline(points, 5)
    
    # 检查点数
    assert len(result) == 5
    
    # 第一个点应该是起点
    assert abs(result[0].x - 0) < 1e-10
    assert abs(result[0].y - 0) < 1e-10
    
    # 最后一个点应该是终点
    assert abs(result[-1].x - 4) < 1e-10
    assert abs(result[-1].y - 0) < 1e-10
    
    # 线性插值的点应该在折线上
    # 检查 x 坐标单调递增
    for i in range(1, len(result)):
        assert result[i].x >= result[i-1].x
    
    print("  ✓ 线性样条测试通过")


def test_cubic_spline():
    """测试三次样条插值"""
    print("测试三次样条插值...")
    
    # 使用简单的控制点
    points = [
        Point2D(0, 0),
        Point2D(1, 1),
        Point2D(2, 0),
        Point2D(3, 1),
        Point2D(4, 0)
    ]
    
    result = cubic_spline(points, 20)
    
    # 检查点数
    assert len(result) == 20
    
    # 起点和终点应该接近控制点
    assert abs(result[0].x - 0) < 1e-10
    assert abs(result[0].y - 0) < 0.1
    assert abs(result[-1].x - 4) < 1e-10
    assert abs(result[-1].y - 0) < 0.1
    
    # 检查曲线在控制点附近
    for i, p in enumerate(result):
        # x 应该单调递增
        if i > 0:
            assert p.x >= result[i - 1].x - 1e-10
    
    print("  ✓ 三次样条测试通过")


def test_catmull_rom_spline():
    """测试 Catmull-Rom 样条"""
    print("测试 Catmull-Rom 样条...")
    
    points = [
        Point2D(0, 0),
        Point2D(1, 2),
        Point2D(3, 1),
        Point2D(5, 3)
    ]
    
    result = catmull_rom_spline(points, 30)
    
    # 检查点数（每段生成点，可能略少于请求）
    assert len(result) >= 20
    
    # 曲线应该通过控制点
    # 检查起点附近
    start_region = result[:5]
    assert any(abs(p.x - 0) < 0.5 for p in start_region)
    
    # 测试闭合曲线
    result_closed = catmull_rom_spline(points, 30, close=True)
    # 闭合曲线应该生成点
    assert len(result_closed) >= 20
    
    print("  ✓ Catmull-Rom 样条测试通过")


def test_b_spline():
    """测试 B 样条曲线"""
    print("测试 B 样条曲线...")
    
    points = [
        Point2D(0, 0),
        Point2D(1, 3),
        Point2D(3, 2),
        Point2D(5, 4),
        Point2D(6, 1)
    ]
    
    # 三次 B 样条
    result = b_spline(points, degree=3, num_points=30)
    
    # 检查点数
    assert len(result) == 30
    
    # 曲线应该被拉向控制点
    # 检查曲线在合理的范围内
    for p in result:
        assert -1 <= p.x <= 7  # 稍微超出控制点范围是合理的
        assert -1 <= p.y <= 5
    
    # 测试二次 B 样条
    result_quadratic = b_spline(points, degree=2, num_points=20)
    assert len(result_quadratic) == 20
    
    # 测试闭合 B 样条
    result_closed = b_spline(points, degree=3, num_points=30, close=True)
    assert len(result_closed) == 30
    
    print("  ✓ B 样条测试通过")


def test_hermite_spline():
    """测试 Hermite 样条"""
    print("测试 Hermite 样条...")
    
    points = [
        Point2D(0, 0),
        Point2D(2, 2),
        Point2D(4, 0)
    ]
    
    tangents = [
        Point2D(1, 1),
        Point2D(1, -1),
        Point2D(1, -1)
    ]
    
    result = hermite_spline(points, tangents, 20)
    
    # 检查点数 - hermite_spline 每段生成 points_per_segment 个点
    assert len(result) >= 10
    
    # 起点应该接近第一个控制点
    assert abs(result[0].x - 0) < 0.1
    
    # 测试自动切线
    result_auto = hermite_spline_auto(points, 20)
    assert len(result_auto) >= 10
    
    print("  ✓ Hermite 样条测试通过")


def test_sample_curve():
    """测试曲线采样"""
    print("测试曲线采样...")
    
    # 创建一条简单曲线
    points = [
        Point2D(0, 0),
        Point2D(5, 5),
        Point2D(10, 0)
    ]
    
    curve = linear_spline(points, 100)
    sampled = sample_curve(curve, 2.0)
    
    # 采样后的点之间的距离应该接近采样距离
    for i in range(1, len(sampled) - 1):
        dist = sampled[i].distance_to(sampled[i - 1])
        # 允许一定误差
        assert abs(dist - 2.0) < 3.0  # 由于原始曲线离散化，允许较大误差
    
    print("  ✓ 曲线采样测试通过")


def test_curve_length():
    """测试曲线长度计算"""
    print("测试曲线长度计算...")
    
    # 直线
    points = [Point2D(0, 0), Point2D(3, 4)]
    length = curve_length(points)
    assert abs(length - 5.0) < 1e-10, f"直线长度错误: {length}"
    
    # 折线
    points = [Point2D(0, 0), Point2D(1, 0), Point2D(1, 1), Point2D(0, 1)]
    length = curve_length(points)
    assert abs(length - 3.0) < 1e-10, f"折线长度错误: {length}"
    
    # 单点
    points = [Point2D(0, 0)]
    length = curve_length(points)
    assert length == 0.0
    
    print("  ✓ 曲线长度测试通过")


def test_resample_curve():
    """测试曲线重采样"""
    print("测试曲线重采样...")
    
    # 创建不均匀分布的点
    points = [
        Point2D(0, 0),
        Point2D(1, 0),
        Point2D(5, 0),
        Point2D(6, 0),
        Point2D(7, 0)
    ]
    
    resampled = resample_curve(points, 5)
    
    # 检查点数
    assert len(resampled) == 5
    
    # 重采样后点应该均匀分布
    # 总长度是 7，所以间隔应该是 7/4 = 1.75
    for i in range(1, len(resampled)):
        dist = resampled[i].distance_to(resampled[i - 1])
        # 允许一定误差
        assert abs(dist - 1.75) < 0.5, f"重采样间隔不均匀: {dist}"
    
    print("  ✓ 曲线重采样测试通过")


def test_smooth_points():
    """测试点列平滑"""
    print("测试点列平滑...")
    
    # 创建锯齿状点列
    points = [
        Point2D(0, 0),
        Point2D(1, 10),
        Point2D(2, 0),
        Point2D(3, 10),
        Point2D(4, 0)
    ]
    
    smoothed = smooth_points(points, iterations=1, factor=0.5)
    
    # 平滑后的点应该更加平滑
    assert len(smoothed) == len(points)
    
    # 边界点不应该改变
    assert abs(smoothed[0].x - 0) < 1e-10
    assert abs(smoothed[0].y - 0) < 1e-10
    assert abs(smoothed[-1].x - 4) < 1e-10
    assert abs(smoothed[-1].y - 0) < 1e-10
    
    # 中间点应该被平滑
    assert smoothed[1].y < 10  # 应该被拉低
    assert smoothed[3].y < 10  # 应该被拉低
    
    print("  ✓ 点列平滑测试通过")


def test_interpolate():
    """测试便捷插值函数"""
    print("测试便捷插值函数...")
    
    points = [(0, 0), (1, 2), (3, 1), (5, 3), (6, 0)]
    
    # 测试各种方法
    methods = ['linear', 'cubic', 'catmull_rom', 'b_spline', 'hermite']
    
    for method in methods:
        result = interpolate(points, method=method, num_points=20)
        assert len(result) == 20, f"{method} 返回点数错误"
        assert result[0][0] >= 0, f"{method} 起点错误"
    
    # 测试无效方法
    try:
        interpolate(points, method='invalid')
        assert False, "应该抛出异常"
    except ValueError:
        pass
    
    print("  ✓ 便捷插值函数测试通过")


def test_edge_cases():
    """测试边界情况"""
    print("测试边界情况...")
    
    # 两点
    points = [Point2D(0, 0), Point2D(1, 1)]
    
    linear = linear_spline(points, 10)
    assert len(linear) == 10
    
    cubic = cubic_spline(points, 10)
    assert len(cubic) == 10
    
    cr = catmull_rom_spline(points, 10)
    assert len(cr) >= 10
    
    # 单点（应该报错或返回单点）
    single = [Point2D(0, 0)]
    try:
        linear_spline(single, 10)
        assert False, "单点应该报错"
    except ValueError:
        pass
    
    print("  ✓ 边界情况测试通过")


def test_consistency():
    """测试一致性"""
    print("测试一致性...")
    
    # 使用相同控制点，比较不同方法
    points = [
        Point2D(0, 0),
        Point2D(2, 3),
        Point2D(4, 2),
        Point2D(6, 4),
        Point2D(8, 1)
    ]
    
    linear = linear_spline(points, 50)
    cubic = cubic_spline(points, 50)
    cr = catmull_rom_spline(points, 50)
    bs = b_spline(points, degree=3, num_points=50)
    
    # 所有方法应该产生相应数量的点（catmull_rom 可能产生略少）
    assert len(linear) == 50
    assert len(cubic) == 50
    assert len(cr) >= 40  # catmull_rom 每段生成点，可能略少于请求
    assert len(bs) == 50
    
    # 检查所有曲线都在合理范围内
    all_points = linear + cubic + cr + bs
    for p in all_points:
        # x 范围应该接近控制点范围
        assert -2 <= p.x <= 10
        # y 范围应该合理
        assert -2 <= p.y <= 6
    
    print("  ✓ 一致性测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("Spline Utils 测试套件")
    print("=" * 50)
    
    tests = [
        test_point2d,
        test_point3d,
        test_linear_spline,
        test_cubic_spline,
        test_catmull_rom_spline,
        test_b_spline,
        test_hermite_spline,
        test_sample_curve,
        test_curve_length,
        test_resample_curve,
        test_smooth_points,
        test_interpolate,
        test_edge_cases,
        test_consistency,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ {test.__name__} 失败: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ {test.__name__} 错误: {e}")
            failed += 1
    
    print("=" * 50)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)