"""
fractal_utils 使用示例

展示各种分形的生成和可视化。

Author: AllToolkit
Date: 2026-05-24
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    FractalConfig,
    MandelbrotSet, JuliaSet, SierpinskiTriangle, KochCurve,
    BarnsleyFern, DragonCurve, HilbertCurve, CantorSet,
    CellularAutomaton,
    mandelbrot_ascii, julia_ascii, sierpinski_ascii,
    barnsley_fern_ascii, dragon_curve_ascii, hilbert_curve_ascii,
    cantor_set_ascii, cellular_automaton_ascii,
    get_fractal_info
)


def example_mandelbrot():
    """Mandelbrot 集示例"""
    print("=" * 60)
    print("Mandelbrot 集")
    print("=" * 60)
    
    # 默认配置
    config = FractalConfig()
    print("\n默认配置的 Mandelbrot 集:")
    print(mandelbrot_ascii(config))
    
    # 缩放到有趣区域
    print("\n缩放到 'Seahorse Valley' 区域:")
    zoom_config = MandelbrotSet.zoom(-0.7435, 0.1314, 0.002)
    zoom_config.height = 30
    print(MandelbrotSet.generate_ascii(zoom_config))
    
    # 计算特定点的迭代次数
    print("\n特定点的迭代次数:")
    points = [
        (0.0, 0.0, "集合中心"),
        (-0.5, 0.0, "边界附近"),
        (2.0, 2.0, "集合外"),
    ]
    for x, y, desc in points:
        iterations = MandelbrotSet.iterate(x, y, 100)
        print(f"  c = ({x}, {y}) [{desc}]: {iterations} 次迭代")


def example_julia():
    """Julia 集示例"""
    print("\n" + "=" * 60)
    print("Julia 集")
    print("=" * 60)
    
    # 经典参数
    classic_params = JuliaSet.CLASSIC_PARAMS
    
    for name, (c_real, c_imag) in list(classic_params.items())[:3]:
        print(f"\nJulia 集 '{name}' (c = {c_real} + {c_imag}i):")
        config = FractalConfig(width=40, height=20)
        print(JuliaSet.generate_ascii(c_real, c_imag, config))
    
    # 自定义参数
    print("\n自定义 Julia 集 (c = 0.28 + 0.008i):")
    print(julia_ascii(0.28, 0.008, FractalConfig(width=40, height=20)))


def example_sierpinski():
    """Sierpinski 三角形示例"""
    print("\n" + "=" * 60)
    print("Sierpinski 三角形")
    print("=" * 60)
    
    # 不同尺寸
    print("\n小尺寸 (size=16):")
    print(sierpinski_ascii(16))
    
    print("\n中等尺寸 (size=32):")
    print(sierpinski_ascii(32))
    
    # 面积和三角形数量
    print("\n迭代属性:")
    for iterations in [1, 2, 3, 4]:
        area_ratio = SierpinskiTriangle.calculate_area_ratio(iterations)
        triangle_count = SierpinskiTriangle.calculate_triangle_count(iterations)
        print(f"  iterations={iterations}: 面积比例={area_ratio:.4f}, 三角形数={triangle_count}")


def example_koch():
    """Koch 曲线示例"""
    print("\n" + "=" * 60)
    print("Koch 曲线")
    print("=" * 60)
    
    # 不同迭代次数的点数
    print("\n不同迭代次数的长度变化:")
    for iterations in [1, 2, 3, 4]:
        ratio = KochCurve.calculate_length_ratio(iterations)
        points = KochCurve.generate_points(iterations, length=100.0)
        print(f"  iterations={iterations}: 长度比例={ratio:.4f}, 点数={len(points)}")
    
    # Koch 雪花
    print("\nKoch 雪花 (iterations=2):")
    points = KochCurve.generate_koch_snowflake(iterations=2, size=60.0)
    print(f"  生成了 {len(points)} 个点")


def example_barnsley_fern():
    """Barnsley 羊齿草示例"""
    print("\n" + "=" * 60)
    print("Barnsley 羊齿草")
    print("=" * 60)
    
    print("\n生成的羊齿草图案:")
    print(barnsley_fern_ascii(width=50, height=30, num_points=3000))
    
    # 点的范围
    points = BarnsleyFern.generate_points(1000)
    x_values = [p.x for p in points]
    y_values = [p.y for p in points]
    print(f"\n点范围: x=[{min(x_values):.2f}, {max(x_values):.2f}], y=[{min(y_values):.2f}, {max(y_values):.2f}]")


def example_dragon():
    """Dragon 曲线示例"""
    print("\n" + "=" * 60)
    print("Dragon 曲线")
    print("=" * 60)
    
    # 不同迭代次数
    print("\n转向序列:")
    for iterations in [1, 2, 3]:
        turns = DragonCurve.generate_turns(iterations)
        print(f"  iterations={iterations}: {turns[:10]}... (共{len(turns)}个转向)")
    
    print("\nDragon 曲线图案:")
    print(dragon_curve_ascii(10))


def example_hilbert():
    """Hilbert 曲线示例"""
    print("\n" + "=" * 60)
    print("Hilbert 曲线")
    print("=" * 60)
    
    # 不同阶数
    print("\n不同阶数的点数:")
    for order in [1, 2, 3]:
        points = HilbertCurve.generate_points(order)
        print(f"  order={order}: {len(points)} 个点 (4^order)")
    
    print("\nHilbert 曲线图案 (order=3):")
    print(hilbert_curve_ascii(3))
    
    # 坐标转换示例
    print("\n坐标转换示例 (order=2):")
    n = 4
    for d in range(n * n):
        x, y = HilbertCurve._d2xy(n, d)
        print(f"  索引 {d} -> 坐标 ({x}, {y})")


def example_cantor():
    """Cantor 集示例"""
    print("\n" + "=" * 60)
    print("Cantor 集")
    print("=" * 60)
    
    print("\nCantor 集演化过程:")
    print(cantor_set_ascii(5, width=80))
    
    # 线段数量
    print("\n不同迭代的属性:")
    for iterations in [1, 2, 3, 4]:
        length_ratio = CantorSet.calculate_length_ratio(iterations)
        segment_count = CantorSet.calculate_segment_count(iterations)
        print(f"  iterations={iterations}: 长度比例={length_ratio:.4f}, 线段数={segment_count}")


def example_cellular_automaton():
    """细胞自动机示例"""
    print("\n" + "=" * 60)
    print("细胞自动机")
    print("=" * 60)
    
    # Sierpinski 规则
    print("\nRule 90 (生成 Sierpinski 三角形):")
    print(cellular_automaton_ascii(rule=90, iterations=15, width=60))
    
    # 复杂规则
    print("\nRule 30 (复杂图案):")
    print(cellular_automaton_ascii(rule=30, iterations=15, width=60))
    
    # 条纹规则
    print("\nRule 15 (条纹图案):")
    print(cellular_automaton_ascii(rule=15, iterations=15, width=60))
    
    # 经典规则列表
    print("\n经典规则:")
    rules = CellularAutomaton.get_classic_rules()
    for name, rule in rules.items():
        print(f"  {name}: Rule {rule}")


def example_fractal_info():
    """分形信息示例"""
    print("\n" + "=" * 60)
    print("分形信息")
    print("=" * 60)
    
    info = get_fractal_info()
    
    print("\n各种分形的维度:")
    for name, data in info.items():
        print(f"  {data['name_cn']} ({name}):")
        print(f"    维度: {data['dimension']:.3f}")
        print(f"    描述: {data['description']}")


def main():
    """运行所有示例"""
    example_mandelbrot()
    example_julia()
    example_sierpinski()
    example_koch()
    example_barnsley_fern()
    example_dragon()
    example_hilbert()
    example_cantor()
    example_cellular_automaton()
    example_fractal_info()
    
    print("\n" + "=" * 60)
    print("示例完成")
    print("=" * 60)


if __name__ == "__main__":
    main()