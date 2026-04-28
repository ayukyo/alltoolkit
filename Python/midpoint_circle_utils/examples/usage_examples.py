"""
中点画圆算法工具模块使用示例

展示如何使用该模块的各种功能：
1. 基本圆形绘制
2. 椭圆绘制
3. 圆弧绘制
4. 填充形状
5. 抗锯齿圆形
6. 圆环绘制
7. 高级功能
"""

import sys
import os
# 正确设置路径
current_dir = os.path.dirname(os.path.abspath(__file__))
module_dir = os.path.dirname(current_dir)
sys.path.insert(0, module_dir)

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


def example_basic_circle():
    """基本圆形绘制示例"""
    print("\n" + "=" * 50)
    print("示例 1: 基本圆形绘制")
    print("=" * 50)
    
    # 绘制半径为 5 的圆
    radius = 5
    points = midpoint_circle(radius)
    print(f"半径为 {radius} 的圆，共有 {len(points)} 个像素点")
    
    # 显示部分点
    print("部分像素坐标（前 10 个）:")
    for i, (x, y) in enumerate(points[:10]):
        print(f"  ({x:3d}, {y:3d})")
    
    # 带圆心偏移的圆
    cx, cy = 10, 20
    points_offset = midpoint_circle(3, cx, cy)
    print(f"\n圆心在 ({cx}, {cy})，半径为 3 的圆:")
    print(f"  共有 {len(points_offset)} 个像素点")


def example_visualize_circle():
    """可视化圆形（ASCII 艺术）"""
    print("\n" + "=" * 50)
    print("示例 2: ASCII 艺术可视化圆形")
    print("=" * 50)
    
    radius = 5
    points = midpoint_circle(radius)
    point_set = set(points)
    
    # 创建画布
    size = radius * 2 + 3
    canvas = [[' ' for _ in range(size)] for _ in range(size)]
    
    # 绘制圆
    for x, y in points:
        # 转换坐标（圆心在画布中心）
        canvas_x = x + radius + 1
        canvas_y = size - (y + radius + 1)
        if 0 <= canvas_x < size and 0 <= canvas_y < size:
            canvas[canvas_y][canvas_x] = '●'
    
    # 打印画布
    print(f"半径为 {radius} 的圆（ASCII 艺术）:")
    for row in canvas:
        print(''.join(row))


def example_filled_circle():
    """填充圆形示例"""
    print("\n" + "=" * 50)
    print("示例 3: 填充圆形")
    print("=" * 50)
    
    radius = 4
    boundary = midpoint_circle(radius)
    filled = midpoint_circle_filled(radius)
    
    print(f"半径为 {radius} 的圆:")
    print(f"  边界像素数: {len(boundary)}")
    print(f"  填充像素数: {len(filled)}")
    print(f"  填充/边界比例: {len(filled) / len(boundary):.2f}")
    
    # 可视化填充圆
    size = radius * 2 + 3
    canvas = [[' ' for _ in range(size)] for _ in range(size)]
    filled_set = set(filled)
    boundary_set = set(boundary)
    
    for x, y in filled:
        canvas_x = x + radius + 1
        canvas_y = size - (y + radius + 1)
        if 0 <= canvas_x < size and 0 <= canvas_y < size:
            if (x, y) in boundary_set:
                canvas[canvas_y][canvas_x] = '○'  # 边界
            else:
                canvas[canvas_y][canvas_x] = '·'  # 内部
    
    print("\n填充圆形可视化（○=边界，·=内部）:")
    for row in canvas:
        print(''.join(row))


def example_ellipse():
    """椭圆绘制示例"""
    print("\n" + "=" * 50)
    print("示例 4: 椭圆绘制")
    print("=" * 50)
    
    # 绘制不同形状的椭圆
    ellipses = [
        (6, 3, "横向椭圆"),
        (3, 6, "纵向椭圆"),
        (5, 5, "圆形椭圆"),
        (8, 2, "扁平椭圆"),
    ]
    
    for a, b, name in ellipses:
        points = midpoint_ellipse(a, b)
        print(f"{name} (a={a}, b={b}): {len(points)} 个像素点")
    
    # 可视化一个椭圆
    a, b = 6, 3
    points = midpoint_ellipse(a, b)
    point_set = set(points)
    
    size_a = a * 2 + 3
    size_b = b * 2 + 3
    canvas = [[' ' for _ in range(size_a)] for _ in range(size_b)]
    
    for x, y in points:
        canvas_x = x + a + 1
        canvas_y = size_b - (y + b + 1)
        if 0 <= canvas_x < size_a and 0 <= canvas_y < size_b:
            canvas[canvas_y][canvas_x] = '●'
    
    print(f"\n椭圆 (a={a}, b={b}) 可视化:")
    for row in canvas:
        print(''.join(row))


def example_arc():
    """圆弧绘制示例"""
    print("\n" + "=" * 50)
    print("示例 5: 圆弧绘制")
    print("=" * 50)
    
    # 不同角度的圆弧
    arcs = [
        (5, 0, 90, "四分之一圆弧"),
        (5, 0, 180, "半圆弧"),
        (5, 90, 180, "第二象限弧"),
        (5, 45, 135, "扇形弧"),
    ]
    
    for radius, start, end, name in arcs:
        points = draw_arc(radius, start, end)
        print(f"{name} (半径={radius}, {start}°-{end}°): {len(points)} 个像素点")
    
    # 可视化四分之一圆弧
    radius = 6
    arc = draw_arc(radius, 0, 90)
    arc_set = set(arc)
    
    size = radius * 2 + 3
    canvas = [[' ' for _ in range(size)] for _ in range(size)]
    
    # 绘制完整圆（浅色）
    full_circle = midpoint_circle(radius)
    for x, y in full_circle:
        canvas_x = x + radius + 1
        canvas_y = size - (y + radius + 1)
        if 0 <= canvas_x < size and 0 <= canvas_y < size:
            canvas[canvas_y][canvas_x] = '·'
    
    # 绘制圆弧（高亮）
    for x, y in arc:
        canvas_x = x + radius + 1
        canvas_y = size - (y + radius + 1)
        if 0 <= canvas_x < size and 0 <= canvas_y < size:
            canvas[canvas_y][canvas_x] = '●'
    
    print(f"\n圆弧可视化（●=圆弧，·=完整圆轮廓）:")
    for row in canvas:
        print(''.join(row))


def example_antialiased():
    """抗锯齿圆形示例"""
    print("\n" + "=" * 50)
    print("示例 6: 抗锯齿圆形")
    print("=" * 50)
    
    radius = 5
    points = antialiased_circle(radius)
    
    print(f"抗锯齿圆形（半径={radius}）:")
    print(f"  总像素点: {len(points)}")
    
    # 显示部分点的 alpha 值
    print("部分像素及其透明度:")
    count = 0
    for x, y, alpha in sorted(points):
        if alpha < 1.0 and count < 10:
            print(f"  ({x:3d}, {y:3d}): alpha = {alpha:.3f}")
            count += 1
    
    # 统计 alpha 分布
    full_alpha = sum(1 for _, _, a in points if a == 1.0)
    partial_alpha = sum(1 for _, _, a in points if 0 < a < 1)
    print(f"\nAlpha 分布:")
    print(f"  完全不透明 (alpha=1.0): {full_alpha} 个")
    print(f"  部分透明 (0<alpha<1): {partial_alpha} 个")


def example_ring():
    """圆环绘制示例"""
    print("\n" + "=" * 50)
    print("示例 7: 圆环绘制")
    print("=" * 50)
    
    outer, inner = 5, 3
    ring = draw_ring(outer, inner)
    print(f"圆环（外半径={outer}, 内半径={inner}）: {len(ring)} 个像素点")
    
    # 填充圆环
    filled_ring = draw_ring_filled(outer, inner)
    print(f"填充圆环（外半径={outer}, 内半径={inner}）: {len(filled_ring)} 个像素点")
    
    # 可视化填充圆环
    size = outer * 2 + 3
    canvas = [[' ' for _ in range(size)] for _ in range(size)]
    filled_set = set(filled_ring)
    ring_set = set(ring)
    
    for x, y in filled_ring:
        canvas_x = x + outer + 1
        canvas_y = size - (y + outer + 1)
        if 0 <= canvas_x < size and 0 <= canvas_y < size:
            if (x, y) in ring_set:
                canvas[canvas_y][canvas_x] = '○'  # 边界
            else:
                canvas[canvas_y][canvas_x] = '·'  # 内部
    
    print("\n填充圆环可视化（○=边界，·=内部）:")
    for row in canvas:
        print(''.join(row))


def example_thickness():
    """带厚度的圆形示例"""
    print("\n" + "=" * 50)
    print("示例 8: 带厚度的圆形")
    print("=" * 50)
    
    radius = 5
    for thickness in [1, 2, 3]:
        points = draw_circle_with_thickness(radius, thickness)
        print(f"厚度 {thickness} 的圆（半径={radius}）: {len(points)} 个像素点")
    
    # 可视化厚度为 2 的圆
    points = draw_circle_with_thickness(5, 2)
    size = 5 * 2 + 3
    canvas = [[' ' for _ in range(size)] for _ in range(size)]
    
    for x, y in points:
        canvas_x = x + 5 + 1
        canvas_y = size - (y + 5 + 1)
        if 0 <= canvas_x < size and 0 <= canvas_y < size:
            canvas[canvas_y][canvas_x] = '●'
    
    print("\n厚度为 2 的圆可视化:")
    for row in canvas:
        print(''.join(row))


def example_dotted():
    """虚线圆示例"""
    print("\n" + "=" * 50)
    print("示例 9: 虚线圆")
    print("=" * 50)
    
    radius = 6
    for spacing in [2, 4, 6]:
        points = draw_dotted_circle(radius, spacing)
        print(f"虚线圆（半径={radius}, 间距={spacing}）: {len(points)} 个像素点")
    
    # 可视化
    points = draw_dotted_circle(6, 4)
    size = 6 * 2 + 3
    canvas = [[' ' for _ in range(size)] for _ in range(size)]
    
    # 完整圆（浅色）
    full = midpoint_circle(6)
    for x, y in full:
        canvas_x = x + 6 + 1
        canvas_y = size - (y + 6 + 1)
        if 0 <= canvas_x < size and 0 <= canvas_y < size:
            canvas[canvas_y][canvas_x] = '·'
    
    # 虚线圆（高亮）
    for x, y in points:
        canvas_x = x + 6 + 1
        canvas_y = size - (y + 6 + 1)
        if 0 <= canvas_x < size and 0 <= canvas_y < size:
            canvas[canvas_y][canvas_x] = '●'
    
    print("\n虚线圆可视化（●=虚线点，·=完整圆轮廓）:")
    for row in canvas:
        print(''.join(row))


def example_point_checks():
    """点检测示例"""
    print("\n" + "=" * 50)
    print("示例 10: 点检测")
    print("=" * 50)
    
    radius = 5
    test_points = [
        (0, 0, "圆心"),
        (5, 0, "圆上（右）"),
        (3, 4, "圆上（右上）"),
        (3, 3, "圆内"),
        (6, 0, "圆外"),
        (-5, 0, "圆上（左）"),
    ]
    
    print(f"半径为 {radius} 的圆的检测结果:")
    print(f"{'点':<15} {'在圆内':<10} {'在圆上':<10}")
    print("-" * 35)
    
    for x, y, desc in test_points:
        in_circle = is_point_in_circle(x, y, radius)
        on_circle = is_point_on_circle(x, y, radius)
        print(f"{desc:<15} {str(in_circle):<10} {str(on_circle):<10}")


def example_generator():
    """生成器版本示例"""
    print("\n" + "=" * 50)
    print("示例 11: 生成器版本")
    print("=" * 50)
    
    radius = 5
    print(f"使用生成器迭代半径为 {radius} 的圆的前 10 个点:")
    
    count = 0
    for x, y in midpoint_circle_iter(radius):
        if count < 10:
            print(f"  ({x:3d}, {y:3d})")
        count += 1
    
    print(f"\n总共 {count} 个点")


def example_statistics():
    """统计信息示例"""
    print("\n" + "=" * 50)
    print("示例 12: 圆的统计信息")
    print("=" * 50)
    
    print(f"{'半径':<8} {'周长像素':<12} {'面积像素':<12} {'周长/面积':<12}")
    print("-" * 50)
    
    for r in range(1, 11):
        perimeter = circle_perimeter(r)
        area = circle_area(r)
        ratio = perimeter / area if area > 0 else 0
        print(f"{r:<8} {perimeter:<12} {area:<12} {ratio:<12.3f}")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("       中点画圆算法工具模块 - 使用示例")
    print("=" * 60)
    
    example_basic_circle()
    example_visualize_circle()
    example_filled_circle()
    example_ellipse()
    example_arc()
    example_antialiased()
    example_ring()
    example_thickness()
    example_dotted()
    example_point_checks()
    example_generator()
    example_statistics()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()