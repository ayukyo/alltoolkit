"""
多项式运算工具模块测试

测试覆盖：
- 多项式创建与基本属性
- 四则运算
- 求值、求导、积分
- 求根
- 插值
- 特殊多项式
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polynomial_utils.mod import (
    Polynomial, from_roots, lagrange_interpolation, newton_interpolation,
    chebyshev_polynomial, legendre_polynomial, hermite_polynomial,
    bernstein_polynomial, parse, horner, synthetic_division,
    X, ONE, ZERO
)


def test_polynomial_creation():
    """测试多项式创建。"""
    print("测试多项式创建...")
    
    # 基本创建
    p = Polynomial([1, 2, 3])  # 1 + 2x + 3x²
    assert p.degree == 2
    assert p[0] == 1
    assert p[1] == 2
    assert p[2] == 3
    
    # 尾部零系数被去除
    p = Polynomial([1, 2, 0, 0])
    assert p.degree == 1
    assert len(p) == 2
    
    # 零多项式
    p = Polynomial([0, 0, 0])
    assert p.is_zero
    assert p.degree == 0
    
    # 常数多项式
    p = Polynomial([5])
    assert p.degree == 0
    assert not p.is_zero
    
    print("  ✓ 多项式创建测试通过")


def test_polynomial_evaluation():
    """测试多项式求值。"""
    print("测试多项式求值...")
    
    # 基本求值
    p = Polynomial([1, 2, 3])  # 1 + 2x + 3x²
    assert p(0) == 1
    assert p(1) == 6
    assert p(2) == 17  # 1 + 4 + 12
    
    # 高次多项式
    p = Polynomial([1, 0, 0, 1])  # 1 + x³
    assert p(2) == 9
    assert p(-1) == 0
    
    # 霍纳法则验证
    # (x-1)^5 = x^5 - 5x^4 + 10x^3 - 10x^2 + 5x - 1
    p = Polynomial([-1, 5, -10, 10, -5, 1])  # (x-1)^5
    assert abs(p(1)) < 1e-10
    assert abs(p(2) - 1) < 1e-10  # (2-1)^5 = 1
    
    print("  ✓ 多项式求值测试通过")


def test_polynomial_string():
    """测试多项式字符串表示。"""
    print("测试多项式字符串表示...")
    
    # 基本格式
    p = Polynomial([1, 2, 3])
    s = str(p)
    assert "1" in s
    assert "2x" in s
    assert "3x^2" in s
    
    # 零多项式
    assert str(Polynomial([0])) == "0"
    
    # 负系数
    p = Polynomial([1, -2, 3])
    s = str(p)
    assert "1" in s
    
    # 系数为 1
    p = Polynomial([0, 1, 1])  # x + x²
    s = str(p)
    assert "x + x^2" in s or "x^2 + x" in s
    
    print("  ✓ 多项式字符串表示测试通过")


def test_polynomial_addition():
    """测试多项式加法。"""
    print("测试多项式加法...")
    
    # 基本加法
    p1 = Polynomial([1, 2, 3])  # 1 + 2x + 3x²
    p2 = Polynomial([1, 1, 1])  # 1 + x + x²
    result = p1 + p2
    assert result[0] == 2
    assert result[1] == 3
    assert result[2] == 4
    
    # 不同次数
    p1 = Polynomial([1, 2])  # 1 + 2x
    p2 = Polynomial([1, 0, 1])  # 1 + x²
    result = p1 + p2
    assert result.degree == 2
    assert result[0] == 2
    assert result[1] == 2
    assert result[2] == 1
    
    # 加标量
    p = Polynomial([1, 2, 3])
    result = p + 5
    assert result[0] == 6
    
    # 标量加多项式
    result = 5 + p
    assert result[0] == 6
    
    print("  ✓ 多项式加法测试通过")


def test_polynomial_subtraction():
    """测试多项式减法。"""
    print("测试多项式减法...")
    
    # 基本减法
    p1 = Polynomial([3, 4, 5])
    p2 = Polynomial([1, 2, 3])
    result = p1 - p2
    assert result[0] == 2
    assert result[1] == 2
    assert result[2] == 2
    
    # 减标量
    p = Polynomial([5, 3])
    result = p - 2
    assert result[0] == 3
    
    # 标量减多项式
    result = 10 - Polynomial([1, 2])
    assert result[0] == 9
    assert result[1] == -2
    
    # 结果为零多项式
    p = Polynomial([1, 2, 3])
    result = p - Polynomial([1, 2, 3])
    assert result.is_zero
    
    print("  ✓ 多项式减法测试通过")


def test_polynomial_multiplication():
    """测试多项式乘法。"""
    print("测试多项式乘法...")
    
    # 基本乘法
    p1 = Polynomial([1, 1])  # 1 + x
    p2 = Polynomial([1, 1])  # 1 + x
    result = p1 * p2
    assert result.degree == 2
    assert result[0] == 1
    assert result[1] == 2
    assert result[2] == 1  # (1+x)² = 1 + 2x + x²
    
    # (x-1)(x+1) = x² - 1
    p1 = Polynomial([-1, 1])  # x - 1
    p2 = Polynomial([1, 1])   # x + 1
    result = p1 * p2
    assert result[0] == -1
    assert result[1] == 0
    assert result[2] == 1
    
    # 乘标量
    p = Polynomial([1, 2, 3])
    result = p * 2
    assert result[0] == 2
    assert result[1] == 4
    assert result[2] == 6
    
    # 零多项式乘法
    p = Polynomial([1, 2, 3])
    result = p * Polynomial([0])
    assert result.is_zero
    
    print("  ✓ 多项式乘法测试通过")


def test_polynomial_division():
    """测试多项式除法。"""
    print("测试多项式除法...")
    
    # 整除
    p1 = Polynomial([1, 2, 1])  # (x+1)² = 1 + 2x + x²
    p2 = Polynomial([1, 1])     # x + 1
    quotient, remainder = p1.divmod(p2)
    assert quotient.degree == 1
    assert quotient[0] == 1
    assert quotient[1] == 1  # x + 1
    assert remainder.is_zero
    
    # 有余数的除法
    p1 = Polynomial([1, 2, 3])  # 1 + 2x + 3x²
    p2 = Polynomial([1, 1])     # 1 + x
    quotient, remainder = p1.divmod(p2)
    # 3x² + 2x + 1 = (x+1)(3x-1) + 2
    assert remainder.degree == 0
    
    # 除以标量
    p = Polynomial([2, 4, 6])
    result = p / 2
    assert result[0] == 1
    assert result[1] == 2
    assert result[2] == 3
    
    # 整除运算符
    p1 = Polynomial([1, 2, 1])
    p2 = Polynomial([1, 1])
    result = p1 // p2
    assert result[0] == 1
    assert result[1] == 1
    
    # 取模运算符
    result = p1 % p2
    assert result.is_zero
    
    print("  ✓ 多项式除法测试通过")


def test_polynomial_power():
    """测试多项式幂运算。"""
    print("测试多项式幂运算...")
    
    # (1+x)^0 = 1
    p = Polynomial([1, 1])
    result = p ** 0
    assert result == ONE
    
    # (1+x)^1 = 1+x
    result = p ** 1
    assert result[0] == 1
    assert result[1] == 1
    
    # (1+x)^2 = 1 + 2x + x²
    result = p ** 2
    assert result[0] == 1
    assert result[1] == 2
    assert result[2] == 1
    
    # (1+x)^3 = 1 + 3x + 3x² + x³
    result = p ** 3
    assert result[0] == 1
    assert result[1] == 3
    assert result[2] == 3
    assert result[3] == 1
    
    # (x-1)^5
    p = Polynomial([-1, 1])
    result = p ** 5
    assert abs(result(1)) < 1e-10
    
    print("  ✓ 多项式幂运算测试通过")


def test_polynomial_derivative():
    """测试多项式求导。"""
    print("测试多项式求导...")
    
    # 基本导数
    p = Polynomial([1, 2, 3])  # 1 + 2x + 3x²
    d = p.derivative()
    assert d.degree == 1
    assert d[0] == 2
    assert d[1] == 6  # 2 + 6x
    
    # 常数的导数为零
    p = Polynomial([5])
    d = p.derivative()
    assert d.is_zero
    
    # x^n 的导数是 nx^(n-1)
    p = Polynomial([0, 0, 0, 1])  # x³
    d = p.derivative()
    assert d[2] == 3  # 3x²
    
    # 高阶导数
    p = Polynomial([1, 2, 3, 4])  # 1 + 2x + 3x² + 4x³
    d2 = p.derivative(2)
    assert d2[0] == 6   # 6 + 24x
    assert d2[1] == 24
    
    d3 = p.derivative(3)
    assert d3[0] == 24  # 常数
    
    d4 = p.derivative(4)
    assert d4.is_zero
    
    print("  ✓ 多项式求导测试通过")


def test_polynomial_integral():
    """测试多项式积分。"""
    print("测试多项式积分...")
    
    # 基本积分
    p = Polynomial([2, 3])  # 2 + 3x
    integral = p.integral()
    assert integral[0] == 0  # 积分常数
    assert integral[1] == 2  # 2x
    assert integral[2] == 1.5  # 1.5x²
    
    # 带积分常数
    integral = p.integral(5)
    assert integral[0] == 5
    
    # 定积分
    p = Polynomial([0, 1])  # x
    result = p.definite_integral(0, 1)  # ∫₀¹ x dx = 0.5
    assert abs(result - 0.5) < 1e-10
    
    # 积分和导数互逆
    p = Polynomial([1, 2, 3, 4])
    integral = p.integral()
    d = integral.derivative()
    for i in range(len(p)):
        assert abs(p[i] - d[i]) < 1e-10
    
    print("  ✓ 多项式积分测试通过")


def test_polynomial_roots():
    """测试多项式求根。"""
    print("测试多项式求根...")
    
    # 一次方程
    p = Polynomial([-2, 1])  # x - 2
    roots = p.find_roots()
    assert len(roots) == 1
    assert abs(roots[0].real - 2) < 1e-6
    
    # 二次方程（实根）
    p = Polynomial([-1, 0, 1])  # x² - 1 = (x-1)(x+1)
    roots = p.find_roots()
    assert len(roots) == 2
    root_values = sorted([r.real for r in roots])
    assert abs(root_values[0] + 1) < 1e-6
    assert abs(root_values[1] - 1) < 1e-6
    
    # 二次方程（复根）
    p = Polynomial([1, 0, 1])  # x² + 1
    roots = p.find_roots()
    assert len(roots) == 2
    assert all(abs(r.imag) > 0.1 for r in roots)  # 复根
    
    # 三次方程
    p = Polynomial([-1, 0, 0, 1])  # x³ - 1
    roots = p.find_roots()
    assert len(roots) == 3
    # 至少有一个实根 1
    has_root_one = any(abs(r.real - 1) < 0.1 and abs(r.imag) < 0.1 for r in roots)
    assert has_root_one
    
    print("  ✓ 多项式求根测试通过")


def test_newton_root():
    """测试牛顿法求根。"""
    print("测试牛顿法求根...")
    
    # x² - 2 = 0, 根是 √2
    p = Polynomial([-2, 0, 1])
    root = p.newton_root(1.5)
    assert root is not None
    assert abs(root - 2**0.5) < 1e-6
    
    # x³ - 2 = 0, 根是 ∛2
    p = Polynomial([-2, 0, 0, 1])
    root = p.newton_root(1.5)
    assert root is not None
    assert abs(root - 2**(1/3)) < 1e-6
    
    # 发散情况
    p = Polynomial([1, 0, 1])  # x² + 1 无实根
    root = p.newton_root(0)
    # 牛顿法无法找到复根
    assert root is None or abs(p(root)) > 1e-6
    
    print("  ✓ 牛顿法求根测试通过")


def test_bisection_root():
    """测试二分法求根。"""
    print("测试二分法求根...")
    
    # x² - 2 在 [1, 2] 上的根
    p = Polynomial([-2, 0, 1])
    root = p.bisection_root(1, 2)
    assert root is not None
    assert abs(root - 2**0.5) < 1e-6
    
    # x³ - 2 在 [1, 2] 上的根
    p = Polynomial([-2, 0, 0, 1])
    root = p.bisection_root(1, 2)
    assert root is not None
    assert abs(root - 2**(1/3)) < 1e-6
    
    # 同号区间，无根
    p = Polynomial([1, 1])  # x + 1, 在 [0, 1] 上同正
    root = p.bisection_root(0, 1)
    assert root is None
    
    print("  ✓ 二分法求根测试通过")


def test_polynomial_composition():
    """测试多项式复合。"""
    print("测试多项式复合...")
    
    # p(x) = x², q(x) = x+1
    # p(q(x)) = (x+1)² = 1 + 2x + x²
    p = Polynomial([0, 0, 1])
    q = Polynomial([1, 1])
    result = p.compose(q)
    assert result[0] == 1
    assert result[1] == 2
    assert result[2] == 1
    
    # q(p(x)) = x² + 1
    result = q.compose(p)
    assert result[0] == 1
    assert result[2] == 1
    
    print("  ✓ 多项式复合测试通过")


def test_polynomial_gcd():
    """测试多项式最大公约式。"""
    print("测试多项式最大公约式...")
    
    # gcd(x²-1, x-1) = x-1
    p1 = Polynomial([-1, 0, 1])  # x² - 1
    p2 = Polynomial([-1, 1])      # x - 1
    g = p1.gcd(p2)
    # 归一化后应该是 x - 1 或常数倍
    assert abs(g(1)) < 1e-10
    
    # gcd(x²-1, x²+1) = 1
    p1 = Polynomial([-1, 0, 1])
    p2 = Polynomial([1, 0, 1])
    g = p1.gcd(p2)
    assert g.degree == 0  # 常数多项式
    
    print("  ✓ 多项式最大公约式测试通过")


def test_factor_out():
    """测试因式提取。"""
    print("测试因式提取...")
    
    # (x-1)² = x² - 2x + 1
    p = Polynomial([1, -2, 1])
    quotient, k = p.factor_out(1)
    assert k == 2
    assert quotient.degree == 0
    
    # x³ - 1 有因子 (x-1)
    p = Polynomial([-1, 0, 0, 1])
    quotient, k = p.factor_out(1)
    assert k == 1
    assert quotient.degree == 2
    
    print("  ✓ 因式提取测试通过")


def test_from_roots():
    """测试从根构造多项式。"""
    print("测试从根构造多项式...")
    
    # 根为 1, -1 的多项式是 (x-1)(x+1) = x² - 1
    p = from_roots([1, -1])
    assert p[0] == -1
    assert p[2] == 1
    
    # 根为 0, 1, 2 的多项式是 x(x-1)(x-2)
    p = from_roots([0, 1, 2])
    assert abs(p(0)) < 1e-10
    assert abs(p(1)) < 1e-10
    assert abs(p(2)) < 1e-10
    
    # 复根成对出现
    p = from_roots([complex(0, 1), complex(0, -1)])
    assert p.degree == 2
    
    print("  ✓ 从根构造多项式测试通过")


def test_lagrange_interpolation():
    """测试拉格朗日插值。"""
    print("测试拉格朗日插值...")
    
    # 通过 (0,0), (1,1), (2,4) 的抛物线
    points = [(0, 0), (1, 1), (2, 4)]
    p = lagrange_interpolation(points)
    
    assert abs(p(0) - 0) < 1e-10
    assert abs(p(1) - 1) < 1e-10
    assert abs(p(2) - 4) < 1e-10
    
    # 三次多项式
    points = [(0, 1), (1, 2), (2, 9), (3, 28)]
    p = lagrange_interpolation(points)
    
    for x, y in points:
        assert abs(p(x) - y) < 1e-6
    
    print("  ✓ 拉格朗日插值测试通过")


def test_newton_interpolation():
    """测试牛顿插值。"""
    print("测试牛顿插值...")
    
    # 与拉格朗日插值结果应相同
    points = [(0, 0), (1, 1), (2, 4)]
    p_newton = newton_interpolation(points)
    p_lagrange = lagrange_interpolation(points)
    
    for x in [0, 0.5, 1, 1.5, 2, 3]:
        assert abs(p_newton(x) - p_lagrange(x)) < 1e-10
    
    print("  ✓ 牛顿插值测试通过")


def test_chebyshev_polynomial():
    """测试切比雪夫多项式。"""
    print("测试切比雪夫多项式...")
    
    # T_0(x) = 1
    t0 = chebyshev_polynomial(0)
    assert t0 == ONE
    
    # T_1(x) = x
    t1 = chebyshev_polynomial(1)
    assert t1 == X
    
    # T_2(x) = 2x² - 1
    t2 = chebyshev_polynomial(2)
    assert abs(t2(0) - (-1)) < 1e-10
    assert abs(t2(1) - 1) < 1e-10
    
    # 验证递推关系：T_{n+1} = 2x*T_n - T_{n-1}
    t3 = chebyshev_polynomial(3)
    expected_t3 = 2 * X * t2 - t1
    for x in [-1, 0, 0.5, 1]:
        assert abs(t3(x) - expected_t3(x)) < 1e-10
    
    print("  ✓ 切比雪夫多项式测试通过")


def test_legendre_polynomial():
    """测试勒让德多项式。"""
    print("测试勒让德多项式...")
    
    # P_0(x) = 1
    p0 = legendre_polynomial(0)
    assert p0 == ONE
    
    # P_1(x) = x
    p1 = legendre_polynomial(1)
    assert p1 == X
    
    # P_2(x) = (3x² - 1)/2
    p2 = legendre_polynomial(2)
    assert abs(p2(0) - (-0.5)) < 1e-10
    assert abs(p2(1) - 1) < 1e-10
    
    # 验证正交性
    p3 = legendre_polynomial(3)
    # ∫_{-1}^{1} P_m(x)P_n(x)dx = 2/(2n+1) δ_{mn}
    integral = p2.definite_integral(-1, 1)
    assert abs(integral - 0) < 1e-6  # P_2 在 [-1,1] 上积分不为 0，但我们检查对称性
    
    print("  ✓ 勒让德多项式测试通过")


def test_hermite_polynomial():
    """测试埃尔米特多项式。"""
    print("测试埃尔米特多项式...")
    
    # H_0(x) = 1
    h0 = hermite_polynomial(0)
    assert h0 == ONE
    
    # H_1(x) = 2x
    h1 = hermite_polynomial(1)
    assert h1(0) == 0
    assert h1(1) == 2
    
    # H_2(x) = 4x² - 2
    h2 = hermite_polynomial(2)
    assert h2(0) == -2
    assert h2(1) == 2
    
    # 验证递推关系
    h3 = hermite_polynomial(3)
    expected_h3 = 2 * X * h2 - 4 * h1
    for x in [-1, 0, 1]:
        assert abs(h3(x) - expected_h3(x)) < 1e-10
    
    print("  ✓ 埃尔米特多项式测试通过")


def test_bernstein_polynomial():
    """测试伯恩斯坦基多项式。"""
    print("测试伯恩斯坦基多项式...")
    
    # B_{2,0}(x) = (1-x)²
    b20 = bernstein_polynomial(2, 0)
    assert abs(b20(0) - 1) < 1e-10
    assert abs(b20(1) - 0) < 1e-10
    
    # B_{2,1}(x) = 2x(1-x)
    b21 = bernstein_polynomial(2, 1)
    assert abs(b21(0) - 0) < 1e-10
    assert abs(b21(1) - 0) < 1e-10
    assert abs(b21(0.5) - 0.5) < 1e-10
    
    # B_{2,2}(x) = x²
    b22 = bernstein_polynomial(2, 2)
    assert abs(b22(0) - 0) < 1e-10
    assert abs(b22(1) - 1) < 1e-10
    
    # 伯恩斯坦基函数之和为 1
    for x in [0, 0.25, 0.5, 0.75, 1]:
        total = sum(bernstein_polynomial(3, k)(x) for k in range(4))
        assert abs(total - 1) < 1e-10
    
    print("  ✓ 伯恩斯坦基多项式测试通过")


def test_parse():
    """测试多项式解析。"""
    print("测试多项式解析...")
    
    # 简单多项式
    p = parse("1 + 2x + 3x^2")
    assert p[0] == 1
    assert p[1] == 2
    assert p[2] == 3
    
    # 带负系数
    p = parse("x^2 - 2x + 1")
    assert p[0] == 1
    assert p[1] == -2
    assert p[2] == 1
    
    # 只有 x
    p = parse("x")
    assert p[0] == 0
    assert p[1] == 1
    
    # 简单因式展开
    p = parse("(x+1)(x-1)")
    # (x+1)(x-1) = x² - 1
    assert p[0] == -1 or abs(p[0] + 1) < 1e-10
    
    print("  ✓ 多项式解析测试通过")


def test_horner():
    """测试霍纳法则。"""
    print("测试霍纳法则...")
    
    # 与 Polynomial 求值对比
    p = Polynomial([1, 2, 3, 4, 5])
    coeffs = p.coefficients
    
    for x in [0, 1, 2, -1, 0.5, 10]:
        assert abs(horner(coeffs, x) - p(x)) < 1e-10
    
    print("  ✓ 霍纳法则测试通过")


def test_synthetic_division():
    """测试综合除法。"""
    print("测试综合除法...")
    
    # (x³ - 1) / (x - 1) = x² + x + 1
    coeffs = [-1, 0, 0, 1]
    q, r = synthetic_division(coeffs, 1)
    assert len(q) == 3
    assert q[0] == 1
    assert q[1] == 1
    assert q[2] == 1
    assert abs(r) < 1e-10
    
    # 与 Polynomial.divmod 对比
    p = Polynomial([1, 2, 3, 4])
    divisor = Polynomial([1, 1])  # x + 1
    
    q1, r1 = p.divmod(divisor)
    q2, r2 = synthetic_division(p.coefficients, -1)
    
    for i in range(len(q1)):
        assert abs(q1[i] - q2[i]) < 1e-10
    
    print("  ✓ 综合除法测试通过")


def test_special_cases():
    """测试边界情况和特殊场景。"""
    print("测试边界情况和特殊场景...")
    
    # 零多项式运算
    zero = ZERO
    p = Polynomial([1, 2, 3])
    
    assert (zero + p) == p
    assert (p + zero) == p
    assert (zero * p).is_zero
    assert (p * zero).is_zero
    
    # 一元多项式
    p = X
    assert p(5) == 5
    assert (p ** 2)(3) == 9
    assert (p ** 3)(2) == 8
    
    # 大系数
    p = Polynomial([1e10, 2e10, 3e10])
    assert p[0] == 1e10
    
    # 小系数
    p = Polynomial([1e-10, 2e-10, 3e-10])
    assert p.degree == 2
    
    # 负指数（应抛出异常）
    try:
        p = Polynomial([1, 2, 3])
        result = p ** (-1)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    print("  ✓ 边界情况和特殊场景测试通过")


def run_all_tests():
    """运行所有测试。"""
    print("\n" + "="*50)
    print("多项式运算工具模块测试")
    print("="*50 + "\n")
    
    test_polynomial_creation()
    test_polynomial_evaluation()
    test_polynomial_string()
    test_polynomial_addition()
    test_polynomial_subtraction()
    test_polynomial_multiplication()
    test_polynomial_division()
    test_polynomial_power()
    test_polynomial_derivative()
    test_polynomial_integral()
    test_polynomial_roots()
    test_newton_root()
    test_bisection_root()
    test_polynomial_composition()
    test_polynomial_gcd()
    test_factor_out()
    test_from_roots()
    test_lagrange_interpolation()
    test_newton_interpolation()
    test_chebyshev_polynomial()
    test_legendre_polynomial()
    test_hermite_polynomial()
    test_bernstein_polynomial()
    test_parse()
    test_horner()
    test_synthetic_division()
    test_special_cases()
    
    print("\n" + "="*50)
    print("所有测试通过! ✓")
    print("="*50 + "\n")


if __name__ == "__main__":
    run_all_tests()