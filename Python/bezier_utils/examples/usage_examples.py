"""
贝塞尔曲线工具使用示例

展示各种贝塞尔曲线的创建、计算和应用场景。
"""

import math
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Point, BezierCurve, LinearBezier, QuadraticBezier, CubicBezier,
    create_bezier, linear_bezier, quadratic_bezier, cubic_bezier,
    smooth_path, interpolate_points, find_t_for_x, distance_to_point
)


def example_01_linear_bezier():
    """示例1: 线性贝塞尔曲线（直线）"""
    print("=" * 50)
    print("示例1: 线性贝塞尔曲线")
    print("=" * 50)
    
    # 创建线性贝塞尔曲线
    curve = linear_bezier((0, 0), (10, 10))
    
    print(f"曲线阶数: {curve.degree}")
    print(f"起点: {curve.start_point}")
    print(f"终点: {curve.end_point}")
    print(f"曲线长度: {curve.length():.4f}")
    
    # 在曲线上采样
    print("\n曲线上的点:")
    for t in [0, 0.25, 0.5, 0.75, 1]:
        p = curve.point_at(t)
        print(f"  t={t:.2f}: {p}")


def example_02_quadratic_bezier():
    """示例2: 二次贝塞尔曲线"""
    print("\n" + "=" * 50)
    print("示例2: 二次贝塞尔曲线")
    print("=" * 50)
    
    # 创建一个抛物线形状的曲线
    curve = quadratic_bezier((0, 0), (5, 10), (10, 0))
    
    print(f"曲线阶数: {curve.degree}")
    print(f"起点: {curve.start_point}")
    print(f"控制点: {curve.control_points[1]}")
    print(f"终点: {curve.end_point}")
    
    # 计算曲线长度
    print(f"\n曲线长度: {curve.length(1000):.4f}")
    
    # 计算曲线上的点和切线
    print("\n曲线上的点和切线:")
    for t in [0, 0.25, 0.5, 0.75, 1]:
        p = curve.point_at(t)
        tangent = curve.tangent_at(t)
        normal = curve.normal_at(t)
        curvature = curve.curvature_at(t)
        print(f"  t={t:.2f}:")
        print(f"    点: ({p.x:.2f}, {p.y:.2f})")
        print(f"    切线: ({tangent.x:.3f}, {tangent.y:.3f})")
        print(f"    法线: ({normal.x:.3f}, {normal.y:.3f})")
        print(f"    曲率: {curvature:.4f}")


def example_03_cubic_bezier():
    """示例3: 三次贝塞尔曲线（最常用的贝塞尔曲线）"""
    print("\n" + "=" * 50)
    print("示例3: 三次贝塞尔曲线")
    print("=" * 50)
    
    # 创建 S 形曲线
    curve = cubic_bezier((0, 0), (2, 8), (8, 8), (10, 0))
    
    print("控制点:")
    for i, p in enumerate(curve.control_points):
        print(f"  P{i}: {p}")
    
    # 采样曲线
    print("\n曲线采样 (t 从 0 到 1):")
    points = curve.sample(11)
    for i, p in enumerate(points):
        t = i / 10
        print(f"  t={t:.1f}: ({p.x:.3f}, {p.y:.3f})")
    
    # 计算边界框
    min_p, max_p = curve.bounding_box(200)
    print(f"\n边界框:")
    print(f"  左下: ({min_p.x:.3f}, {min_p.y:.3f})")
    print(f"  右上: ({max_p.x:.3f}, {max_p.y:.3f})")


def example_04_curve_splitting():
    """示例4: 曲线分割"""
    print("\n" + "=" * 50)
    print("示例4: 曲线分割")
    print("=" * 50)
    
    curve = cubic_bezier((0, 0), (2, 8), (8, 8), (10, 0))
    
    # 在 t=0.5 处分割
    left, right = curve.split_at(0.5)
    
    print("原曲线控制点:")
    for i, p in enumerate(curve.control_points):
        print(f"  P{i}: {p}")
    
    print("\n左半部分控制点:")
    for i, p in enumerate(left.control_points):
        print(f"  P{i}: {p}")
    
    print("\n右半部分控制点:")
    for i, p in enumerate(right.control_points):
        print(f"  P{i}: {p}")
    
    # 验证分割点
    split_point = curve.point_at(0.5)
    print(f"\n分割点: {split_point}")
    print(f"左半部分终点: {left.end_point}")
    print(f"右半部分起点: {right.start_point}")


def example_05_curve_degree_elevation():
    """示例5: 曲线升阶"""
    print("\n" + "=" * 50)
    print("示例5: 曲线升阶")
    print("=" * 50)
    
    # 二次曲线升阶为三次
    quad = quadratic_bezier((0, 0), (5, 10), (10, 0))
    cubic = quad.elevate_degree()
    
    print(f"原曲线阶数: {quad.degree}")
    print(f"升阶后阶数: {cubic.degree}")
    
    print("\n原曲线控制点:")
    for i, p in enumerate(quad.control_points):
        print(f"  P{i}: {p}")
    
    print("\n升阶后控制点:")
    for i, p in enumerate(cubic.control_points):
        print(f"  P{i}: {p}")
    
    # 验证形状不变
    print("\n验证形状不变 (t=0.5 处的点):")
    p1 = quad.point_at(0.5)
    p2 = cubic.point_at(0.5)
    print(f"  原曲线: {p1}")
    print(f"  升阶后: {p2}")
    print(f"  差值: ({abs(p1.x - p2.x):.10f}, {abs(p1.y - p2.y):.10f})")


def example_06_smooth_path():
    """示例6: 平滑路径生成"""
    print("\n" + "=" * 50)
    print("示例6: 平滑路径生成")
    print("=" * 50)
    
    # 创建一条经过多个点的平滑曲线
    points = [
        Point(0, 0),
        Point(3, 5),
        Point(7, 2),
        Point(10, 8),
        Point(15, 0)
    ]
    
    curves = smooth_path(points, tension=0.3)
    
    print(f"输入点数: {len(points)}")
    print(f"生成曲线数: {len(curves)}")
    
    print("\n输入点:")
    for i, p in enumerate(points):
        print(f"  点{i}: ({p.x:.1f}, {p.y:.1f})")
    
    print("\n生成的曲线段:")
    for i, curve in enumerate(curves):
        print(f"  段{i}: 起点 ({curve.start_point.x:.2f}, {curve.start_point.y:.2f}), "
              f"终点 ({curve.end_point.x:.2f}, {curve.end_point.y:.2f})")


def example_07_distance_calculation():
    """示例7: 点到曲线的距离计算"""
    print("\n" + "=" * 50)
    print("示例7: 点到曲线的距离计算")
    print("=" * 50)
    
    curve = quadratic_bezier((0, 0), (5, 10), (10, 0))
    
    # 曲线上的点
    point_on_curve = curve.point_at(0.5)  # (5, 5)
    dist, t = distance_to_point(curve, point_on_curve)
    print(f"曲线上的点 ({point_on_curve.x:.2f}, {point_on_curve.y:.2f}):")
    print(f"  距离: {dist:.6f}")
    print(f"  参数 t: {t:.6f}")
    
    # 曲线外的点
    external_point = Point(5, 15)
    dist, t = distance_to_point(curve, external_point)
    closest = curve.point_at(t)
    print(f"\n曲线外的点 ({external_point.x:.2f}, {external_point.y:.2f}):")
    print(f"  最近距离: {dist:.4f}")
    print(f"  最近点参数 t: {t:.4f}")
    print(f"  最近点: ({closest.x:.4f}, {closest.y:.4f})")


def example_08_find_t_for_x():
    """示例8: 根据x坐标找参数t"""
    print("\n" + "=" * 50)
    print("示例8: 根据x坐标找参数t")
    print("=" * 50)
    
    curve = quadratic_bezier((0, 0), (5, 10), (10, 0))
    
    for target_x in [0, 2.5, 5, 7.5, 10]:
        t = find_t_for_x(curve, target_x)
        if t is not None:
            p = curve.point_at(t)
            print(f"target_x={target_x}: t={t:.4f}, point=({p.x:.4f}, {p.y:.4f})")
        else:
            print(f"target_x={target_x}: 未找到")


def example_09_uniform_sampling():
    """示例9: 按弧长均匀采样"""
    print("\n" + "=" * 50)
    print("示例9: 按弧长均匀采样")
    print("=" * 50)
    
    curve = cubic_bezier((0, 0), (2, 8), (8, 8), (10, 0))
    
    # 参数均匀采样
    param_samples = curve.sample(6)
    print("参数均匀采样 (6个点):")
    for i, p in enumerate(param_samples):
        print(f"  点{i}: ({p.x:.4f}, {p.y:.4f})")
    
    # 弧长均匀采样
    uniform_samples = curve.sample_uniform(2.0)
    print(f"\n弧长均匀采样 (每段约2.0单位, 共{len(uniform_samples)}个点):")
    for i, p in enumerate(uniform_samples):
        print(f"  点{i}: ({p.x:.4f}, {p.y:.4f})")
    
    # 计算相邻点距离
    print("\n相邻点距离:")
    for i in range(len(uniform_samples) - 1):
        dist = uniform_samples[i].distance_to(uniform_samples[i+1])
        print(f"  段{i}: {dist:.4f}")


def example_10_to_polyline():
    """示例10: 曲线转多段线"""
    print("\n" + "=" * 50)
    print("示例10: 曲线转多段线")
    print("=" * 50)
    
    curve = cubic_bezier((0, 0), (2, 8), (8, 8), (10, 0))
    
    for tolerance in [0.5, 0.1, 0.01]:
        polyline = curve.to_polyline(tolerance=tolerance)
        print(f"容差 {tolerance}: {len(polyline)} 个顶点")
    
    # 显示最精细的多段线
    polyline = curve.to_polyline(tolerance=0.1)
    print(f"\n容差 0.1 的多段线顶点:")
    for i, p in enumerate(polyline[:10]):  # 只显示前10个
        print(f"  顶点{i}: ({p.x:.4f}, {p.y:.4f})")
    if len(polyline) > 10:
        print(f"  ... 共 {len(polyline)} 个顶点")


def example_11_animation_easing():
    """示例11: 动画缓动函数应用"""
    print("\n" + "=" * 50)
    print("示例11: 动画缓动函数应用")
    print("=" * 50)
    
    # ease-in-out 曲线 (缓动函数)
    # 控制点形成 S 形，用于动画加速减速
    ease_in_out = cubic_bezier((0, 0), (0.42, 0), (0.58, 1), (1, 1))
    
    print("Ease-In-Out 缓动曲线:")
    print("动画进度 (t) -> 实际进度 (y)")
    for t in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
        p = ease_in_out.point_at(t)
        print(f"  {t:.1f} -> {p.y:.4f}")
    
    print("\n特点: 开始和结束缓慢，中间快速")


def example_12_higher_degree():
    """示例12: 高阶贝塞尔曲线"""
    print("\n" + "=" * 50)
    print("示例12: 高阶贝塞尔曲线")
    print("=" * 50)
    
    # 四阶贝塞尔曲线
    curve = create_bezier([(0, 0), (2, 5), (4, 8), (6, 5), (8, 0)])
    
    print(f"曲线阶数: {curve.degree}")
    print(f"控制点数: {len(curve.control_points)}")
    
    print("\n控制点:")
    for i, p in enumerate(curve.control_points):
        print(f"  P{i}: ({p.x:.1f}, {p.y:.1f})")
    
    print("\n曲线长度:", curve.length(1000))
    
    print("\n曲线采样:")
    for t in [0, 0.25, 0.5, 0.75, 1]:
        p = curve.point_at(t)
        print(f"  t={t:.2f}: ({p.x:.3f}, {p.y:.3f})")


def main():
    """运行所有示例"""
    example_01_linear_bezier()
    example_02_quadratic_bezier()
    example_03_cubic_bezier()
    example_04_curve_splitting()
    example_05_curve_degree_elevation()
    example_06_smooth_path()
    example_07_distance_calculation()
    example_08_find_t_for_x()
    example_09_uniform_sampling()
    example_10_to_polyline()
    example_11_animation_easing()
    example_12_higher_degree()
    
    print("\n" + "=" * 50)
    print("所有示例运行完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()