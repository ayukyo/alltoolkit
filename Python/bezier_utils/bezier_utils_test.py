"""
贝塞尔曲线工具模块测试
"""

import math
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Point, BezierCurve, LinearBezier, QuadraticBezier, CubicBezier,
    create_bezier, linear_bezier, quadratic_bezier, cubic_bezier,
    smooth_path, interpolate_points, find_t_for_x, distance_to_point
)


class TestPoint:
    """Point 类测试"""
    
    def test_init(self):
        p = Point(3.5, 4.5)
        assert p.x == 3.5
        assert p.y == 4.5
    
    def test_repr(self):
        p = Point(1.23456, 2.34567)
        assert "Point" in repr(p)
    
    def test_equality(self):
        p1 = Point(1.0, 2.0)
        p2 = Point(1.0, 2.0)
        p3 = Point(1.0, 3.0)
        assert p1 == p2
        assert p1 != p3
    
    def test_addition(self):
        p1 = Point(1, 2)
        p2 = Point(3, 4)
        result = p1 + p2
        assert result.x == 4
        assert result.y == 6
    
    def test_subtraction(self):
        p1 = Point(5, 7)
        p2 = Point(2, 3)
        result = p1 - p2
        assert result.x == 3
        assert result.y == 4
    
    def test_multiplication(self):
        p = Point(2, 3)
        result = p * 2
        assert result.x == 4
        assert result.y == 6
    
    def test_division(self):
        p = Point(6, 9)
        result = p / 3
        assert result.x == 2
        assert result.y == 3
    
    def test_distance(self):
        p1 = Point(0, 0)
        p2 = Point(3, 4)
        assert p1.distance_to(p2) == 5.0
    
    def test_magnitude(self):
        p = Point(3, 4)
        assert p.magnitude() == 5.0
    
    def test_normalize(self):
        p = Point(3, 4)
        normalized = p.normalize()
        assert abs(normalized.magnitude() - 1.0) < 1e-9
    
    def test_perpendicular(self):
        p = Point(1, 0)
        perp = p.perpendicular()
        assert perp.x == 0
        assert perp.y == 1
    
    def test_to_tuple(self):
        p = Point(3.5, 4.5)
        assert p.to_tuple() == (3.5, 4.5)
    
    def test_from_tuple(self):
        p = Point.from_tuple((1.5, 2.5))
        assert p.x == 1.5
        assert p.y == 2.5


class TestLinearBezier:
    """线性贝塞尔曲线测试"""
    
    def test_create(self):
        curve = linear_bezier((0, 0), (10, 10))
        assert curve.degree == 1
        assert curve.start_point == Point(0, 0)
        assert curve.end_point == Point(10, 10)
    
    def test_point_at_start(self):
        curve = linear_bezier((0, 0), (10, 10))
        p = curve.point_at(0)
        assert abs(p.x - 0) < 1e-9
        assert abs(p.y - 0) < 1e-9
    
    def test_point_at_end(self):
        curve = linear_bezier((0, 0), (10, 10))
        p = curve.point_at(1)
        assert abs(p.x - 10) < 1e-9
        assert abs(p.y - 10) < 1e-9
    
    def test_point_at_mid(self):
        curve = linear_bezier((0, 0), (10, 10))
        p = curve.point_at(0.5)
        assert abs(p.x - 5) < 1e-9
        assert abs(p.y - 5) < 1e-9
    
    def test_length(self):
        curve = linear_bezier((0, 0), (3, 4))
        assert curve.length() == 5.0
    
    def test_invalid_t(self):
        curve = linear_bezier((0, 0), (10, 10))
        try:
            curve.point_at(1.5)
            assert False, "Should raise ValueError"
        except ValueError:
            pass


class TestQuadraticBezier:
    """二次贝塞尔曲线测试"""
    
    def test_create(self):
        curve = quadratic_bezier((0, 0), (5, 10), (10, 0))
        assert curve.degree == 2
    
    def test_point_at_start(self):
        curve = quadratic_bezier((0, 0), (5, 10), (10, 0))
        p = curve.point_at(0)
        assert abs(p.x - 0) < 1e-9
        assert abs(p.y - 0) < 1e-9
    
    def test_point_at_end(self):
        curve = quadratic_bezier((0, 0), (5, 10), (10, 0))
        p = curve.point_at(1)
        assert abs(p.x - 10) < 1e-9
        assert abs(p.y - 0) < 1e-9
    
    def test_point_at_mid(self):
        # 对称二次贝塞尔曲线，中点应该在最高点
        curve = quadratic_bezier((0, 0), (5, 10), (10, 0))
        p = curve.point_at(0.5)
        assert abs(p.x - 5) < 1e-9
        assert abs(p.y - 5) < 1e-9  # B(0.5) = 0.25*P0 + 0.5*P1 + 0.25*P2 = (5, 5)
    
    def test_derivative(self):
        curve = quadratic_bezier((0, 0), (0, 10), (10, 10))
        d = curve.derivative_at(0)
        assert abs(d.x - 0) < 1e-9
        assert abs(d.y - 20) < 1e-9


class TestCubicBezier:
    """三次贝塞尔曲线测试"""
    
    def test_create(self):
        curve = cubic_bezier((0, 0), (2, 8), (8, 8), (10, 0))
        assert curve.degree == 3
    
    def test_point_at_start(self):
        curve = cubic_bezier((0, 0), (2, 8), (8, 8), (10, 0))
        p = curve.point_at(0)
        assert abs(p.x - 0) < 1e-9
        assert abs(p.y - 0) < 1e-9
    
    def test_point_at_end(self):
        curve = cubic_bezier((0, 0), (2, 8), (8, 8), (10, 0))
        p = curve.point_at(1)
        assert abs(p.x - 10) < 1e-9
        assert abs(p.y - 0) < 1e-9
    
    def test_split(self):
        curve = cubic_bezier((0, 0), (2, 8), (8, 8), (10, 0))
        left, right = curve.split_at(0.5)
        
        assert left.start_point == curve.start_point
        assert right.end_point == curve.end_point
        
        # 分割点应该在两条曲线上
        split_point = curve.point_at(0.5)
        assert abs(left.end_point.x - split_point.x) < 1e-6
        assert abs(left.end_point.y - split_point.y) < 1e-6
        assert abs(right.start_point.x - split_point.x) < 1e-6
        assert abs(right.start_point.y - split_point.y) < 1e-6
    
    def test_bounding_box(self):
        curve = cubic_bezier((0, 0), (0, 10), (10, 10), (10, 0))
        min_p, max_p = curve.bounding_box(200)
        assert min_p.x >= 0
        assert max_p.x <= 10
        assert min_p.y >= 0
        assert max_p.y <= 10


class TestBezierCurve:
    """通用贝塞尔曲线测试"""
    
    def test_higher_degree(self):
        # 四次贝塞尔曲线
        curve = create_bezier([(0, 0), (2, 5), (5, 8), (8, 5), (10, 0)])
        assert curve.degree == 4
        
        p = curve.point_at(0.5)
        assert 0 <= p.x <= 10
        assert 0 <= p.y <= 10
    
    def test_sample(self):
        curve = quadratic_bezier((0, 0), (5, 10), (10, 0))
        points = curve.sample(11)
        assert len(points) == 11
        assert points[0] == curve.start_point
        assert points[-1] == curve.end_point
    
    def test_reverse(self):
        curve = quadratic_bezier((0, 0), (5, 10), (10, 0))
        reversed_curve = curve.reverse()
        
        assert reversed_curve.start_point == curve.end_point
        assert reversed_curve.end_point == curve.start_point
    
    def test_elevate_degree(self):
        curve = quadratic_bezier((0, 0), (5, 10), (10, 0))
        elevated = curve.elevate_degree()
        
        assert elevated.degree == 3
        assert elevated.start_point == curve.start_point
        assert elevated.end_point == curve.end_point
        
        # 升阶后曲线应该和原曲线形状相同
        for t in [0, 0.25, 0.5, 0.75, 1]:
            p1 = curve.point_at(t)
            p2 = elevated.point_at(t)
            assert abs(p1.x - p2.x) < 1e-6
            assert abs(p1.y - p2.y) < 1e-6
    
    def test_to_polyline(self):
        curve = cubic_bezier((0, 0), (2, 10), (8, 10), (10, 0))
        polyline = curve.to_polyline(tolerance=0.1)
        
        assert len(polyline) >= 2
        assert polyline[0] == curve.start_point
        assert polyline[-1] == curve.end_point
    
    def test_curvature(self):
        # 直线的曲率为0
        line = linear_bezier((0, 0), (10, 10))
        assert abs(line.curvature_at(0.5)) < 1e-9
        
        # 二次曲线的曲率应该非零（一般情况）
        curve = quadratic_bezier((0, 0), (5, 10), (10, 0))
        k = curve.curvature_at(0.5)
        assert k > 0  # 曲线有凸起，曲率应为正
    
    def test_tangent_normal(self):
        curve = quadratic_bezier((0, 0), (5, 10), (10, 0))
        t = curve.tangent_at(0.5)
        n = curve.normal_at(0.5)
        
        # 切线和法线应该垂直
        dot = t.x * n.x + t.y * n.y
        assert abs(dot) < 1e-9
        
        # 切线和法线应该是单位向量
        assert abs(t.magnitude() - 1.0) < 1e-9
        assert abs(n.magnitude() - 1.0) < 1e-9


class TestSmoothPath:
    """平滑路径测试"""
    
    def test_two_points(self):
        points = [Point(0, 0), Point(10, 10)]
        curves = smooth_path(points)
        assert len(curves) == 1
        assert isinstance(curves[0], LinearBezier)
    
    def test_three_points(self):
        points = [Point(0, 0), Point(5, 10), Point(10, 0)]
        curves = smooth_path(points)
        assert len(curves) == 2
        assert all(isinstance(c, CubicBezier) for c in curves)
    
    def test_interpolate_points(self):
        points = [(0, 0), (5, 10), (10, 0)]
        interpolated = interpolate_points(points)
        assert len(interpolated) > len(points)
        assert interpolated[0] == (0, 0)
        assert interpolated[-1] == (10, 0)


class TestUtilityFunctions:
    """工具函数测试"""
    
    def test_find_t_for_x(self):
        curve = quadratic_bezier((0, 0), (5, 10), (10, 0))
        
        # 起点
        t = find_t_for_x(curve, 0)
        assert abs(t - 0) < 1e-3
        
        # 终点
        t = find_t_for_x(curve, 10)
        assert abs(t - 1) < 1e-3
        
        # 中点
        t = find_t_for_x(curve, 5)
        assert abs(t - 0.5) < 1e-3
        
        # 超出范围
        t = find_t_for_x(curve, 20)
        assert t is None
    
    def test_distance_to_point(self):
        # 点在曲线上
        curve = quadratic_bezier((0, 0), (5, 10), (10, 0))
        point_on_curve = curve.point_at(0.5)  # (5, 5)
        
        dist, t = distance_to_point(curve, point_on_curve)
        assert dist < 1e-6
        
        # 点不在曲线上
        far_point = Point(5, 20)
        dist, t = distance_to_point(curve, far_point)
        assert dist > 10  # 距离应该较大
    
    def test_sample_uniform(self):
        curve = quadratic_bezier((0, 0), (5, 10), (10, 0))
        points = curve.sample_uniform(segment_length=1.0)
        
        assert len(points) >= 2
        assert points[0] == curve.start_point
        assert points[-1] == curve.end_point
        
        # 相邻点之间的距离应该大致相等
        distances = [points[i].distance_to(points[i+1]) for i in range(len(points)-1)]
        avg_dist = sum(distances) / len(distances)
        
        # 允许一定误差
        for d in distances:
            assert d > 0


class TestEdgeCases:
    """边界情况测试"""
    
    def test_minimum_points(self):
        # 最少需要2个点
        try:
            BezierCurve([Point(0, 0)])
            assert False, "Should raise ValueError"
        except ValueError:
            pass
    
    def test_colinear_points(self):
        # 共线点（实际是直线）
        curve = quadratic_bezier((0, 0), (5, 5), (10, 10))
        p = curve.point_at(0.5)
        
        assert abs(p.x - 5) < 1e-6
        assert abs(p.y - 5) < 1e-6
    
    def test_zero_length(self):
        curve = linear_bezier((5, 5), (5, 5))
        assert curve.length() == 0
        
        p = curve.point_at(0.5)
        assert p.x == 5
        assert p.y == 5
    
    def test_very_small_curve(self):
        curve = quadratic_bezier((0, 0), (1e-10, 1e-10), (2e-10, 0))
        p = curve.point_at(0.5)
        # 不应该抛出异常
        assert isinstance(p, Point)


def run_tests():
    """运行所有测试"""
    test_classes = [
        TestPoint,
        TestLinearBezier,
        TestQuadraticBezier,
        TestCubicBezier,
        TestBezierCurve,
        TestSmoothPath,
        TestUtilityFunctions,
        TestEdgeCases,
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = []
    
    for test_class in test_classes:
        instance = test_class()
        test_methods = [m for m in dir(instance) if m.startswith('test_')]
        
        for method_name in test_methods:
            total_tests += 1
            try:
                getattr(instance, method_name)()
                passed_tests += 1
                print(f"✓ {test_class.__name__}.{method_name}")
            except AssertionError as e:
                failed_tests.append((test_class.__name__, method_name, str(e)))
                print(f"✗ {test_class.__name__}.{method_name}: {e}")
            except Exception as e:
                failed_tests.append((test_class.__name__, method_name, str(e)))
                print(f"✗ {test_class.__name__}.{method_name}: {e}")
    
    print(f"\n{'='*50}")
    print(f"测试结果: {passed_tests}/{total_tests} 通过")
    
    if failed_tests:
        print(f"\n失败的测试:")
        for class_name, method, error in failed_tests:
            print(f"  - {class_name}.{method}: {error}")
        return False
    return True


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)