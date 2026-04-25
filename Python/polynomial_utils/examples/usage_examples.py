"""
多项式运算工具使用示例

演示 Polynomial 类和相关工具函数的各种用法。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from polynomial_utils.mod import (
    Polynomial, from_roots, lagrange_interpolation, newton_interpolation,
    chebyshev_polynomial, legendre_polynomial, hermite_polynomial,
    bernstein_polynomial, parse, horner, synthetic_division,
    X, ONE, ZERO
)


def example_basic_operations():
    """基本运算示例。"""
    print("\n" + "="*60)
    print("基本运算示例")
    print("="*60)
    
    # 创建多项式
    print("\n1. 创建多项式")
    p1 = Polynomial([1, 2, 3])  # 1 + 2x + 3x²
    print(f"   p1 = {p1}")
    print(f"   系数: {p1.coefficients}")
    print(f"   次数: {p1.degree}")
    
    # 使用预定义常量
    p2 = 1 + 2*X + 3*X**2  # 同样的多项式
    print(f"   p2 = 1 + 2*X + 3*X**2 = {p2}")
    
    # 求值
    print("\n2. 多项式求值")
    print(f"   p1(0) = {p1(0)}")
    print(f"   p1(1) = {p1(1)}")
    print(f"   p1(2) = {p1(2)}")
    print(f"   p1(-1) = {p1(-1)}")
    
    # 四则运算
    print("\n3. 四则运算")
    p3 = Polynomial([1, 1])  # 1 + x
    p4 = Polynomial([1, -1])  # 1 - x
    print(f"   p3 = {p3}")
    print(f"   p4 = {p4}")
    print(f"   p3 + p4 = {p3 + p4}")
    print(f"   p3 - p4 = {p3 - p4}")
    print(f"   p3 * p4 = {p3 * p4}")
    print(f"   p3 / 2 = {p3 / 2}")
    
    # 多项式除法
    print("\n4. 多项式除法")
    p5 = Polynomial([1, 2, 1])  # (x+1)²
    p6 = Polynomial([1, 1])  # x + 1
    quotient, remainder = p5.divmod(p6)
    print(f"   p5 = {p5} = (x+1)²")
    print(f"   p6 = {p6} = x + 1")
    print(f"   p5 ÷ p6 = {quotient}")
    print(f"   余数 = {remainder}")
    
    # 幂运算
    print("\n5. 幂运算")
    p7 = Polynomial([1, 1])  # 1 + x
    print(f"   p7 = {p7}")
    print(f"   p7^2 = {p7**2}")
    print(f"   p7^3 = {p7**3}")
    print(f"   p7^5 = {p7**5}")


def example_derivative_integral():
    """求导和积分示例。"""
    print("\n" + "="*60)
    print("求导和积分示例")
    print("="*60)
    
    # 求导
    print("\n1. 多项式求导")
    p = Polynomial([1, 2, 3, 4])  # 1 + 2x + 3x² + 4x³
    print(f"   p(x) = {p}")
    print(f"   p'(x) = {p.derivative()}")
    print(f"   p''(x) = {p.derivative(2)}")
    print(f"   p'''(x) = {p.derivative(3)}")
    print(f"   p''''(x) = {p.derivative(4)}")
    
    # 积分
    print("\n2. 多项式积分")
    p = Polynomial([2, 6, 12])  # 2 + 6x + 12x²
    print(f"   p(x) = {p}")
    print(f"   ∫p(x)dx = {p.integral()}")
    print(f"   ∫p(x)dx + C = {p.integral(5)}")
    
    # 定积分
    print("\n3. 定积分")
    p = Polynomial([0, 3])  # 3x
    print(f"   p(x) = {p}")
    print(f"   ∫₀¹ 3x dx = {p.definite_integral(0, 1)}")
    print(f"   ∫₀² 3x dx = {p.definite_integral(0, 2)}")


def example_find_roots():
    """求根示例。"""
    print("\n" + "="*60)
    print("求根示例")
    print("="*60)
    
    # 一次方程
    print("\n1. 一次方程")
    p = Polynomial([-3, 1])  # x - 3 = 0
    print(f"   {p} = 0")
    roots = p.find_roots()
    print(f"   根: x = {roots[0].real:.2f}")
    
    # 二次方程
    print("\n2. 二次方程")
    p = Polynomial([-4, 0, 1])  # x² - 4 = 0
    print(f"   {p} = 0")
    roots = p.find_roots()
    print(f"   根: x = {roots[0].real:.2f}, x = {roots[1].real:.2f}")
    
    # 复根
    print("\n3. 复根")
    p = Polynomial([1, 0, 1])  # x² + 1 = 0
    print(f"   {p} = 0")
    roots = p.find_roots()
    for i, r in enumerate(roots):
        print(f"   根{i+1}: x = {r}")
    
    # 三次方程
    print("\n4. 三次方程")
    p = Polynomial([-8, 0, 0, 1])  # x³ - 8 = 0
    print(f"   {p} = 0")
    roots = p.find_roots()
    for i, r in enumerate(roots):
        print(f"   根{i+1}: x = {r.real:.4f} + {r.imag:.4f}i")
    
    # 牛顿法
    print("\n5. 牛顿法求根")
    p = Polynomial([-2, 0, 1])  # x² - 2 = 0
    print(f"   {p} = 0")
    root = p.newton_root(2)
    print(f"   牛顿法从 x=2 开始: x ≈ {root:.10f}")
    print(f"   验证: √2 = {2**0.5:.10f}")
    
    # 二分法
    print("\n6. 二分法求根")
    p = Polynomial([-2, 0, 1])  # x² - 2 = 0
    print(f"   {p} = 0")
    root = p.bisection_root(1, 2)
    print(f"   二分法在 [1, 2]: x ≈ {root:.10f}")


def example_interpolation():
    """插值示例。"""
    print("\n" + "="*60)
    print("多项式插值示例")
    print("="*60)
    
    # 拉格朗日插值
    print("\n1. 拉格朗日插值")
    points = [(0, 0), (1, 1), (2, 4), (3, 9)]
    print(f"   已知点: {points}")
    p = lagrange_interpolation(points)
    print(f"   插值多项式: {p}")
    print(f"   验证:")
    for x, y in points:
        print(f"     p({x}) = {p(x):.2f} (期望: {y})")
    
    # 牛顿插值
    print("\n2. 牛顿插值")
    points = [(0, 1), (1, 2), (2, 5), (3, 10)]
    print(f"   已知点: {points}")
    p = newton_interpolation(points)
    print(f"   插值多项式: {p}")
    print(f"   验证:")
    for x, y in points:
        print(f"     p({x}) = {p(x):.2f} (期望: {y})")
    
    # 与拉格朗日对比
    print("\n3. 拉格朗日 vs 牛顿插值")
    points = [(1, 1), (2, 4), (3, 9), (4, 16)]
    p_lag = lagrange_interpolation(points)
    p_new = newton_interpolation(points)
    print(f"   两种方法应该给出相同的结果:")
    print(f"   p(2.5) = {p_lag(2.5):.6f} (拉格朗日)")
    print(f"   p(2.5) = {p_new(2.5):.6f} (牛顿)")


def example_special_polynomials():
    """特殊多项式示例。"""
    print("\n" + "="*60)
    print("特殊多项式示例")
    print("="*60)
    
    # 切比雪夫多项式
    print("\n1. 切比雪夫多项式 T_n(x)")
    for n in range(6):
        t = chebyshev_polynomial(n)
        print(f"   T_{n}(x) = {t}")
    
    print("\n   切比雪夫多项式的值:")
    print(f"   {'n':<5}", end="")
    for x in [-1, -0.5, 0, 0.5, 1]:
        print(f"{x:<10}", end="")
    print()
    for n in range(6):
        t = chebyshev_polynomial(n)
        print(f"   {n:<5}", end="")
        for x in [-1, -0.5, 0, 0.5, 1]:
            print(f"{t(x):<10.4f}", end="")
        print()
    
    # 勒让德多项式
    print("\n2. 勒让德多项式 P_n(x)")
    for n in range(5):
        p = legendre_polynomial(n)
        print(f"   P_{n}(x) = {p}")
    
    # 埃尔米特多项式
    print("\n3. 埃尔米特多项式 H_n(x)")
    for n in range(5):
        h = hermite_polynomial(n)
        print(f"   H_{n}(x) = {h}")
    
    # 伯恩斯坦基多项式
    print("\n4. 伯恩斯坦基多项式 B_{n,k}(x)")
    print("   n=3 时的所有基函数:")
    for k in range(4):
        b = bernstein_polynomial(3, k)
        print(f"   B_{{3,{k}}}(x) = {b}")
    
    print("\n   基函数之和在 x=0.5 时:")
    total = sum(bernstein_polynomial(3, k)(0.5) for k in range(4))
    print(f"   Σ B_{{3,k}}(0.5) = {total:.4f} (应为 1)")


def example_parse():
    """字符串解析示例。"""
    print("\n" + "="*60)
    print("字符串解析示例")
    print("="*60)
    
    examples = [
        "1 + 2x + 3x^2",
        "x^2 - 2x + 1",
        "x^3 - 1",
        "x",
        "5",
        "2x^4 - 3x^2 + x - 7"
    ]
    
    for s in examples:
        p = parse(s)
        print(f"   '{s}' → {p}")


def example_advanced():
    """高级应用示例。"""
    print("\n" + "="*60)
    print("高级应用示例")
    print("="*60)
    
    # 多项式复合
    print("\n1. 多项式复合")
    p = Polynomial([0, 0, 1])  # x²
    q = Polynomial([1, 1])     # 1 + x
    print(f"   p(x) = {p}")
    print(f"   q(x) = {q}")
    print(f"   p(q(x)) = {p.compose(q)}")
    print(f"   q(p(x)) = {q.compose(p)}")
    
    # 最大公约式
    print("\n2. 最大公约式")
    p1 = Polynomial([-1, 0, 1])  # x² - 1 = (x-1)(x+1)
    p2 = Polynomial([-1, 1])     # x - 1
    print(f"   p1(x) = {p1} = (x-1)(x+1)")
    print(f"   p2(x) = {p2}")
    print(f"   gcd(p1, p2) = {p1.gcd(p2)}")
    
    # 因式分解
    print("\n3. 因式提取")
    p = Polynomial([1, -3, 3, -1])  # (x-1)³
    print(f"   p(x) = {p}")
    quotient, k = p.factor_out(1)
    print(f"   p(x) = (x-1)^{k} × {quotient}")
    
    # 从根构造多项式
    print("\n4. 从根构造多项式")
    roots = [1, 2, -1]
    p = from_roots(roots)
    print(f"   根: {roots}")
    print(f"   多项式: {p}")
    print(f"   验证:")
    for r in roots:
        print(f"     p({r}) = {p(r):.2f}")
    
    # 霍纳法则
    print("\n5. 霍纳法则高效求值")
    coeffs = [1, -5, 10, -10, 5, -1]  # (x-1)^5
    x = 2
    result = horner(coeffs, x)
    p = Polynomial(coeffs)
    print(f"   多项式: {p}")
    print(f"   p({x}) = {result}")
    print(f"   验证: (2-1)^5 = {(x-1)**5}")
    
    # 综合除法
    print("\n6. 综合除法")
    coeffs = [-1, 0, 0, 1]  # x³ - 1
    root = 1
    quotient, remainder = synthetic_division(coeffs, root)
    print(f"   被除式: x³ - 1")
    print(f"   除式: x - 1")
    print(f"   商: {Polynomial(quotient)}")
    print(f"   余数: {remainder}")


def example_real_world():
    """实际应用示例。"""
    print("\n" + "="*60)
    print("实际应用示例")
    print("="*60)
    
    # 曲线拟合
    print("\n1. 曲线拟合")
    print("   根据实验数据点拟合曲线:")
    data_points = [
        (0, 2.1),
        (1, 7.8),
        (2, 14.2),
        (3, 22.5),
        (4, 31.8)
    ]
    p = lagrange_interpolation(data_points)
    print(f"   插值多项式: {p}")
    print(f"   预测 x=2.5 时的值: y ≈ {p(2.5):.2f}")
    
    # 泰勒展开近似
    print("\n2. 泰勒展开近似")
    # e^x ≈ 1 + x + x²/2! + x³/3! + x⁴/4!
    # 用多项式逼近
    print("   e^x 的泰勒展开 (前5项):")
    import math
    coeffs = [1, 1, 0.5, 1/6, 1/24]
    p = Polynomial(coeffs)
    print(f"   p(x) = {p}")
    for x in [0, 0.5, 1]:
        approx = p(x)
        exact = math.exp(x)
        print(f"   x={x}: 近似值={approx:.6f}, 精确值={exact:.6f}, 误差={abs(approx-exact):.6f}")
    
    # 数值积分
    print("\n3. 数值积分")
    p = Polynomial([0, 1, 1])  # x + x²
    print(f"   计算 ∫₀² (x + x²) dx")
    print(f"   被积函数: {p}")
    result = p.definite_integral(0, 2)
    exact = 0.5 * 2**2 + 2**3 / 3
    print(f"   多项式积分结果: {result:.6f}")
    print(f"   精确值: {exact:.6f}")
    
    # 方程求解
    print("\n4. 方程求解应用")
    print("   圆柱体体积 V = πr²h，给定 V=100π，求 r=h 时的尺寸")
    print("   r² × r = 100 → r³ = 100 → r = ∛100")
    p = Polynomial([-100, 0, 0, 1])
    root = p.newton_root(4.5)
    print(f"   使用牛顿法求解 r³ - 100 = 0")
    print(f"   r ≈ {root:.6f}")
    print(f"   验证: {root:.6f}³ = {root**3:.6f} ≈ 100")


def main():
    """运行所有示例。"""
    print("\n" + "="*60)
    print("多项式运算工具模块 - 使用示例")
    print("="*60)
    
    example_basic_operations()
    example_derivative_integral()
    example_find_roots()
    example_interpolation()
    example_special_polynomials()
    example_parse()
    example_advanced()
    example_real_world()
    
    print("\n" + "="*60)
    print("示例运行完成!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()