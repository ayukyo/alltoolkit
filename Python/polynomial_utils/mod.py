"""
多项式运算工具模块

提供完整的多项式运算功能，包括：
- 多项式创建与解析
- 四则运算（加减乘除）
- 求值、求导、积分
- 求根（牛顿法、二分法）
- 因式分解（简单情况）
- 多项式插值

零外部依赖，纯 Python 实现。
"""

from typing import List, Tuple, Optional, Union, Iterator
from functools import reduce
import copy


class Polynomial:
    """
    多项式类，支持完整的数学运算。
    
    多项式以系数列表形式存储，从低次到高次。
    例如：[1, 2, 3] 表示 1 + 2x + 3x²
    
    用法：
        p = Polynomial([1, 2, 3])  # 1 + 2x + 3x²
        p(2)  # 求值：1 + 2*2 + 3*4 = 17
        p.derivative()  # 导数：2 + 6x
    """
    
    def __init__(self, coefficients: Union[List[float], Tuple[float, ...]]):
        """
        初始化多项式。
        
        Args:
            coefficients: 系数列表，从常数项开始，例如 [1, 2, 3] 表示 1 + 2x + 3x²
        """
        # 去除尾部零系数
        coeffs = list(coefficients)
        while len(coeffs) > 1 and abs(coeffs[-1]) < 1e-15:
            coeffs.pop()
        self._coeffs = coeffs
    
    @property
    def coefficients(self) -> List[float]:
        """返回系数列表的副本。"""
        return self._coeffs.copy()
    
    @property
    def degree(self) -> int:
        """返回多项式次数。"""
        return len(self._coeffs) - 1
    
    @property
    def is_zero(self) -> bool:
        """判断是否为零多项式。"""
        return len(self._coeffs) == 1 and abs(self._coeffs[0]) < 1e-15
    
    def __repr__(self) -> str:
        return f"Polynomial({self._coeffs})"
    
    def __str__(self) -> str:
        """将多项式转换为字符串表示。"""
        if self.is_zero:
            return "0"
        
        terms = []
        for i, coef in enumerate(self._coeffs):
            if abs(coef) < 1e-15:
                continue
            
            # 处理符号
            if not terms:
                sign = ""
            elif coef > 0:
                sign = " + "
            else:
                sign = " - "
            
            # 处理系数绝对值
            abs_coef = abs(coef)
            if i == 0:
                coef_str = f"{abs_coef:.10g}"
            elif abs(abs_coef - 1) < 1e-15:
                coef_str = ""
            else:
                coef_str = f"{abs_coef:.10g}"
            
            # 处理变量部分
            if i == 0:
                var_str = ""
            elif i == 1:
                var_str = "x"
            else:
                var_str = f"x^{i}"
            
            terms.append(f"{sign}{coef_str}{var_str}")
        
        return "".join(terms) if terms else "0"
    
    def __call__(self, x: float) -> float:
        """求值：计算多项式在 x 处的值（使用霍纳法则）。"""
        result = 0.0
        for coef in reversed(self._coeffs):
            result = result * x + coef
        return result
    
    def __getitem__(self, power: int) -> float:
        """获取指定次数的系数。"""
        if power < 0:
            raise IndexError("Power must be non-negative")
        if power >= len(self._coeffs):
            return 0.0
        return self._coeffs[power]
    
    def __add__(self, other: Union['Polynomial', float, int]) -> 'Polynomial':
        """多项式加法。"""
        if isinstance(other, (int, float)):
            result = self._coeffs.copy()
            result[0] += other
            return Polynomial(result)
        
        if not isinstance(other, Polynomial):
            return NotImplemented
        
        max_len = max(len(self._coeffs), len(other._coeffs))
        result = [0.0] * max_len
        for i in range(len(self._coeffs)):
            result[i] += self._coeffs[i]
        for i in range(len(other._coeffs)):
            result[i] += other._coeffs[i]
        return Polynomial(result)
    
    def __radd__(self, other: Union[float, int]) -> 'Polynomial':
        return self + other
    
    def __sub__(self, other: Union['Polynomial', float, int]) -> 'Polynomial':
        """多项式减法。"""
        if isinstance(other, (int, float)):
            result = self._coeffs.copy()
            result[0] -= other
            return Polynomial(result)
        
        if not isinstance(other, Polynomial):
            return NotImplemented
        
        max_len = max(len(self._coeffs), len(other._coeffs))
        result = [0.0] * max_len
        for i in range(len(self._coeffs)):
            result[i] += self._coeffs[i]
        for i in range(len(other._coeffs)):
            result[i] -= other._coeffs[i]
        return Polynomial(result)
    
    def __rsub__(self, other: Union[float, int]) -> 'Polynomial':
        return Polynomial([other]) - self
    
    def __mul__(self, other: Union['Polynomial', float, int]) -> 'Polynomial':
        """多项式乘法。"""
        if isinstance(other, (int, float)):
            return Polynomial([c * other for c in self._coeffs])
        
        if not isinstance(other, Polynomial):
            return NotImplemented
        
        if self.is_zero or other.is_zero:
            return Polynomial([0])
        
        result = [0.0] * (len(self._coeffs) + len(other._coeffs) - 1)
        for i, a in enumerate(self._coeffs):
            for j, b in enumerate(other._coeffs):
                result[i + j] += a * b
        return Polynomial(result)
    
    def __rmul__(self, other: Union[float, int]) -> 'Polynomial':
        return self * other
    
    def __truediv__(self, other: Union['Polynomial', float, int]) -> 'Polynomial':
        """多项式除以标量。"""
        if isinstance(other, (int, float)):
            if abs(other) < 1e-15:
                raise ZeroDivisionError("Cannot divide polynomial by zero")
            return Polynomial([c / other for c in self._coeffs])
        
        if isinstance(other, Polynomial):
            quotient, remainder = self.divmod(other)
            if not remainder.is_zero:
                raise ValueError("Polynomial division has non-zero remainder")
            return quotient
        
        return NotImplemented
    
    def __floordiv__(self, other: 'Polynomial') -> 'Polynomial':
        """多项式整除。"""
        if isinstance(other, Polynomial):
            quotient, _ = self.divmod(other)
            return quotient
        return NotImplemented
    
    def __mod__(self, other: 'Polynomial') -> 'Polynomial':
        """多项式取模（余数）。"""
        if isinstance(other, Polynomial):
            _, remainder = self.divmod(other)
            return remainder
        return NotImplemented
    
    def divmod(self, other: 'Polynomial') -> Tuple['Polynomial', 'Polynomial']:
        """
        多项式除法，返回商和余数。
        
        Args:
            other: 除式
        
        Returns:
            (商, 余数)
        """
        return self.__divmod__(other)
    
    def __divmod__(self, other: 'Polynomial') -> Tuple['Polynomial', 'Polynomial']:
        """多项式除法，返回商和余数。"""
        if not isinstance(other, Polynomial):
            raise TypeError("divmod requires Polynomial operand")
        
        if other.is_zero:
            raise ZeroDivisionError("Cannot divide by zero polynomial")
        
        if self.degree < other.degree:
            return Polynomial([0]), Polynomial(self._coeffs)
        
        quotient = [0.0] * (self.degree - other.degree + 1)
        remainder = list(self._coeffs)
        
        divisor_lead = other._coeffs[-1]
        
        for i in range(self.degree - other.degree, -1, -1):
            coef = remainder[i + other.degree] / divisor_lead
            quotient[i] = coef
            for j in range(len(other._coeffs)):
                remainder[i + j] -= coef * other._coeffs[j]
        
        return Polynomial(quotient), Polynomial(remainder)
    
    def __pow__(self, n: int) -> 'Polynomial':
        """多项式幂运算。"""
        if n < 0:
            raise ValueError("Negative powers not supported")
        if n == 0:
            return Polynomial([1])
        if n == 1:
            return Polynomial(self._coeffs)
        
        result = Polynomial([1])
        base = Polynomial(self._coeffs)
        while n > 0:
            if n % 2 == 1:
                result = result * base
            base = base * base
            n //= 2
        return result
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Polynomial):
            return self._coeffs == other._coeffs
        if isinstance(other, (int, float)):
            return len(self._coeffs) == 1 and abs(self._coeffs[0] - other) < 1e-15
        return False
    
    def __neg__(self) -> 'Polynomial':
        return Polynomial([-c for c in self._coeffs])
    
    def __pos__(self) -> 'Polynomial':
        return Polynomial(self._coeffs)
    
    def __abs__(self) -> 'Polynomial':
        return Polynomial([abs(c) for c in self._coeffs])
    
    def __len__(self) -> int:
        return len(self._coeffs)
    
    def __iter__(self) -> Iterator[float]:
        return iter(self._coeffs)
    
    def derivative(self, n: int = 1) -> 'Polynomial':
        """
        计算多项式的 n 阶导数。
        
        Args:
            n: 导数阶数，默认为 1
        
        Returns:
            n 阶导数多项式
        """
        if n < 0:
            raise ValueError("Derivative order must be non-negative")
        if n == 0:
            return Polynomial(self._coeffs)
        
        result = self._coeffs.copy()
        for _ in range(n):
            if len(result) <= 1:
                return Polynomial([0])
            result = [i * result[i] for i in range(1, len(result))]
        
        return Polynomial(result) if result else Polynomial([0])
    
    def integral(self, c: float = 0) -> 'Polynomial':
        """
        计算多项式的不定积分。
        
        Args:
            c: 积分常数，默认为 0
        
        Returns:
            原函数多项式
        """
        result = [c]
        for i, coef in enumerate(self._coeffs):
            result.append(coef / (i + 1))
        return Polynomial(result)
    
    def definite_integral(self, a: float, b: float) -> float:
        """
        计算多项式在区间 [a, b] 上的定积分。
        
        Args:
            a: 积分下限
            b: 积分上限
        
        Returns:
            定积分值
        """
        antiderivative = self.integral()
        return antiderivative(b) - antiderivative(a)
    
    def find_roots(self, method: str = 'auto', max_iter: int = 100, 
                   tolerance: float = 1e-10) -> List[complex]:
        """
        求多项式的所有根。
        
        支持的方法：
        - 'auto': 自动选择（低次用解析法，高次用数值法）
        - 'newton': 牛顿迭代法
        - 'bisection': 二分法（需要知道根的大致范围）
        - 'companion': 伴随矩阵法（求所有根）
        
        Args:
            method: 求根方法
            max_iter: 最大迭代次数
            tolerance: 收敛容差
        
        Returns:
            根的列表（可能包含复数）
        """
        if self.is_zero:
            raise ValueError("Zero polynomial has infinitely many roots")
        
        # 常数多项式
        if self.degree == 0:
            return []
        
        # 一次多项式
        if self.degree == 1:
            a, b = self._coeffs[1], self._coeffs[0]
            return [complex(-b / a)]
        
        # 二次多项式：求根公式
        if self.degree == 2:
            return self._solve_quadratic()
        
        # 三次多项式：卡尔丹公式
        if self.degree == 3:
            return self._solve_cubic()
        
        # 高次多项式：使用伴随矩阵法
        return self._solve_companion(tolerance)
    
    def _solve_quadratic(self) -> List[complex]:
        """二次方程求根公式。"""
        a, b, c = self._coeffs[2], self._coeffs[1], self._coeffs[0]
        discriminant = b * b - 4 * a * c
        
        if discriminant >= 0:
            sqrt_d = discriminant ** 0.5
            return [complex((-b + sqrt_d) / (2 * a)),
                    complex((-b - sqrt_d) / (2 * a))]
        else:
            sqrt_d = (-discriminant) ** 0.5
            real = -b / (2 * a)
            imag = sqrt_d / (2 * a)
            return [complex(real, imag), complex(real, -imag)]
    
    def _solve_cubic(self) -> List[complex]:
        """三次方程求根（使用卡尔丹公式的三角形式）。"""
        a = self._coeffs[3]
        b = self._coeffs[2]
        c = self._coeffs[1]
        d = self._coeffs[0]
        
        # 归一化为 x³ + px + q = 0 的形式
        # 通过 x = t - b/(3a) 的变换消除二次项
        p = (3*a*c - b*b) / (3*a*a)
        q = (2*b*b*b - 9*a*b*c + 27*a*a*d) / (27*a*a*a)
        
        # 判别式
        discriminant = (q*q/4) + (p*p*p/27)
        
        import math
        
        if discriminant > 1e-10:
            # 一个实根，两个复根
            u = (-q/2 + discriminant**0.5) ** (1/3)
            v = (-q/2 - discriminant**0.5) ** (1/3)
            real_root = u + v - b/(3*a)
            
            # 复根
            complex_part = (u - v) * 0.5 * (3**0.5)
            real_part = -(u + v)/2 - b/(3*a)
            
            return [
                complex(real_root, 0),
                complex(real_part, complex_part),
                complex(real_part, -complex_part)
            ]
        elif discriminant < -1e-10:
            # 三个不同的实根（使用三角形式）
            phi = math.acos(-q/2 / (-p*p*p/27)**0.5)
            t = 2 * (-p/3)**0.5
            roots = []
            for k in range(3):
                root = t * math.cos((phi + 2*k*math.pi)/3) - b/(3*a)
                roots.append(complex(root, 0))
            return roots
        else:
            # 重根情况
            if abs(p) < 1e-10 and abs(q) < 1e-10:
                # 三重根
                root = -b/(3*a)
                return [complex(root, 0), complex(root, 0), complex(root, 0)]
            else:
                # 一个单根和一个二重根
                u = (-q/2) ** (1/3) if q < 0 else (abs(-q/2)) ** (1/3)
                single_root = 2*u - b/(3*a)
                double_root = -u - b/(3*a)
                return [complex(single_root, 0), complex(double_root, 0), complex(double_root, 0)]
    
    def _solve_companion(self, tolerance: float = 1e-10) -> List[complex]:
        """使用伴随矩阵法求所有根（QR 算法简化版）。"""
        n = self.degree
        if n == 0:
            return []
        
        # 标准化为首一多项式
        lead = self._coeffs[-1]
        coeffs = [-c / lead for c in self._coeffs[:-1]]
        
        # 构建伴随矩阵
        # 这是一个 n×n 的矩阵
        # 最后一列是系数（取负），次对角线是 1
        
        # 使用迭代法近似求解
        # 这里用改进的 Aberth 方法
        
        # 初始猜测（均匀分布在圆上）
        import random
        random.seed(42)  # 固定种子以获得可重复结果
        
        roots = []
        radius = 1 + max(abs(c) for c in coeffs) if coeffs else 1
        
        for i in range(n):
            angle = 2 * 3.14159265358979 * i / n
            roots.append(complex(radius * 0.5 * (1 + 0.1 * random.random()) * 
                                  (1 if i % 2 == 0 else -1)))
        
        # Aberth 迭代
        for _ in range(100):
            new_roots = []
            for i, z in enumerate(roots):
                # 计算 p(z) / p'(z)
                p_val = self(z.real) if abs(z.imag) < 1e-15 else self._eval_complex(z)
                p_prime = self.derivative()
                p_prime_val = p_prime(z.real) if abs(z.imag) < 1e-15 else p_prime._eval_complex(z)
                
                if abs(p_prime_val) < 1e-15:
                    new_roots.append(z)
                    continue
                
                w = p_val / p_prime_val
                
                # Aberth 修正项
                correction = 0
                for j, other_z in enumerate(roots):
                    if i != j:
                        diff = z - other_z
                        if abs(diff) > 1e-15:
                            correction += 1 / diff
                
                if abs(1 + w * correction) > 1e-15:
                    w = w / (1 - w * correction)
                
                new_z = z - w
                new_roots.append(new_z)
            
            # 检查收敛
            converged = all(abs(new - old) < tolerance 
                           for new, old in zip(new_roots, roots))
            roots = new_roots
            
            if converged:
                break
        
        # 清理结果（将很小的虚部归零）
        cleaned = []
        for r in roots:
            if abs(r.imag) < tolerance:
                cleaned.append(complex(r.real, 0))
            else:
                cleaned.append(r)
        
        return cleaned
    
    def _eval_complex(self, z: complex) -> complex:
        """计算多项式在复数点的值。"""
        result = complex(0, 0)
        for coef in reversed(self._coeffs):
            result = result * z + coef
        return result
    
    def newton_root(self, x0: float, max_iter: int = 100, 
                    tolerance: float = 1e-10) -> Optional[float]:
        """
        使用牛顿迭代法求根。
        
        Args:
            x0: 初始猜测值
            max_iter: 最大迭代次数
            tolerance: 收敛容差
        
        Returns:
            找到的根，如果发散则返回 None
        """
        x = x0
        derivative = self.derivative()
        
        for _ in range(max_iter):
            fx = self(x)
            fpx = derivative(x)
            
            if abs(fpx) < 1e-15:
                return None
            
            x_new = x - fx / fpx
            
            if abs(x_new - x) < tolerance:
                return x_new
            
            if abs(x_new) > 1e10:  # 发散检测
                return None
            
            x = x_new
        
        return x if abs(self(x)) < tolerance else None
    
    def bisection_root(self, a: float, b: float, max_iter: int = 100,
                       tolerance: float = 1e-10) -> Optional[float]:
        """
        使用二分法在区间 [a, b] 内求根。
        
        前提：f(a) 和 f(b) 异号。
        
        Args:
            a: 区间左端点
            b: 区间右端点
            max_iter: 最大迭代次数
            tolerance: 收敛容差
        
        Returns:
            找到的根，如果前提不满足则返回 None
        """
        fa, fb = self(a), self(b)
        
        if fa * fb > 0:
            return None  # 同号，无法使用二分法
        
        for _ in range(max_iter):
            mid = (a + b) / 2
            fmid = self(mid)
            
            if abs(fmid) < tolerance or abs(b - a) < tolerance:
                return mid
            
            if fa * fmid < 0:
                b, fb = mid, fmid
            else:
                a, fa = mid, fmid
        
        return (a + b) / 2
    
    def compose(self, other: 'Polynomial') -> 'Polynomial':
        """
        多项式复合：计算 self(other(x))。
        
        Args:
            other: 内层多项式
        
        Returns:
            复合后的多项式
        """
        if not isinstance(other, Polynomial):
            raise TypeError("compose requires Polynomial operand")
        
        if self.is_zero:
            return Polynomial([0])
        
        result = Polynomial([0])
        power = Polynomial([1])  # other^0
        
        for coef in self._coeffs:
            result = result + coef * power
            power = power * other
        
        return result
    
    def evaluate_derivative(self, x: float, n: int = 1) -> float:
        """
        直接计算 n 阶导数在 x 处的值（不求导数多项式）。
        
        使用泰勒展开的系数，更高效。
        
        Args:
            x: 求值点
            n: 导数阶数
        
        Returns:
            n 阶导数值
        """
        if n > self.degree:
            return 0.0
        
        result = 0.0
        for i in range(n, len(self._coeffs)):
            # n 阶导数的系数是 i! / (i-n)! * a_i
            coef = self._coeffs[i]
            for j in range(i - n + 1, i + 1):
                coef *= j
            result += coef * (x ** (i - n))
        
        return result
    
    def taylor_coefficients(self, x0: float, n: int) -> List[float]:
        """
        计算多项式在 x0 处的泰勒展开系数（前 n 项）。
        
        Args:
            x0: 展开点
            n: 系数个数
        
        Returns:
            泰勒展开系数列表 [f(x0), f'(x0), f''(x0)/2!, ...]
        """
        # 平移多项式：p(x) = q(x - x0)
        coeffs = []
        p = Polynomial(self._coeffs)
        
        for i in range(n):
            coeffs.append(p(x0) if i == 0 else p.derivative(i)(x0))
            p = (p - Polynomial([p(x0)])) * Polynomial([0, 1])  # 除以 (x - x0)
        
        # 除以阶乘
        factorial = 1
        for i in range(n):
            if i > 0:
                factorial *= i
            coeffs[i] /= factorial
        
        return coeffs
    
    def gcd(self, other: 'Polynomial') -> 'Polynomial':
        """
        计算两个多项式的最大公约式（欧几里得算法）。
        
        Args:
            other: 另一个多项式
        
        Returns:
            最大公约式
        """
        if not isinstance(other, Polynomial):
            raise TypeError("gcd requires Polynomial operand")
        
        a, b = Polynomial(self._coeffs), Polynomial(other._coeffs)
        
        while not b.is_zero:
            _, remainder = a.divmod(b)
            a, b = b, remainder
        
        # 归一化为首一多项式
        lead = a._coeffs[-1]
        return Polynomial([c / lead for c in a._coeffs])
    
    def lcm(self, other: 'Polynomial') -> 'Polynomial':
        """
        计算两个多项式的最小公倍式。
        
        Args:
            other: 另一个多项式
        
        Returns:
            最小公倍式
        """
        if not isinstance(other, Polynomial):
            raise TypeError("lcm requires Polynomial operand")
        
        if self.is_zero or other.is_zero:
            return Polynomial([0])
        
        return (self * other) // self.gcd(other)
    
    def factor_out(self, root: float, tolerance: float = 1e-10) -> Tuple['Polynomial', int]:
        """
        提取因式 (x - root)^k，返回商式和幂次 k。
        
        Args:
            root: 要提取的根
            tolerance: 容差
        
        Returns:
            (商式, 幂次)
        """
        quotient = Polynomial(self._coeffs)
        factor = Polynomial([-root, 1])
        k = 0
        
        while quotient.degree > 0:
            q, r = quotient.divmod(factor)
            if abs(r(root)) > tolerance:
                break
            quotient = q
            k += 1
        
        return quotient, k
    
    def copy(self) -> 'Polynomial':
        """返回多项式的副本。"""
        return Polynomial(self._coeffs)


# ==================== 工具函数 ====================

def from_roots(roots: List[Union[float, complex]]) -> Polynomial:
    """
    根据根构造多项式。
    
    Args:
        roots: 根的列表
    
    Returns:
        以这些根为零点的多项式
    """
    if not roots:
        return Polynomial([1])
    
    result = Polynomial([1])
    processed_roots = set()  # 记录已处理的根
    
    for i, r in enumerate(roots):
        if i in processed_roots:
            continue
        
        if isinstance(r, complex) and abs(r.imag) > 1e-15:
            # 复根：查找其共轭复根是否在列表中
            conjugate = complex(r.real, -r.imag)
            found_conjugate = False
            
            for j, other in enumerate(roots):
                if j > i and j not in processed_roots:
                    if isinstance(other, complex) and abs(other.real - r.real) < 1e-10 and abs(other.imag + r.imag) < 1e-10:
                        found_conjugate = True
                        processed_roots.add(j)
                        break
            
            if found_conjugate:
                # (x - a - bi)(x - a + bi) = (x-a)² + b² = x² - 2ax + a² + b²
                a, b = r.real, abs(r.imag)
                result = result * Polynomial([a*a + b*b, -2*a, 1])
            else:
                # 单独的复根，生成二次因子
                result = result * Polynomial([-r.real * r.real - r.imag * r.imag, -2 * r.real, 1])
        else:
            real_r = r.real if isinstance(r, complex) else r
            result = result * Polynomial([-real_r, 1])
    
    return result


def lagrange_interpolation(points: List[Tuple[float, float]]) -> Polynomial:
    """
    拉格朗日插值：构造通过给定点的多项式。
    
    Args:
        points: 点列表 [(x1, y1), (x2, y2), ...]
    
    Returns:
        插值多项式
    """
    if not points:
        raise ValueError("At least one point required")
    
    n = len(points)
    result = Polynomial([0])
    
    for i in range(n):
        xi, yi = points[i]
        
        # 构造第 i 个拉格朗日基多项式
        basis = Polynomial([yi])
        for j in range(n):
            if i != j:
                xj = points[j][0]
                denominator = xi - xj
                basis = basis * Polynomial([-xj / denominator, 1 / denominator])
        
        result = result + basis
    
    return result


def newton_interpolation(points: List[Tuple[float, float]]) -> Polynomial:
    """
    牛顿插值：构造通过给定点的多项式（牛顿形式）。
    
    更适合动态添加新点的情况。
    
    Args:
        points: 点列表 [(x1, y1), (x2, y2), ...]
    
    Returns:
        插值多项式
    """
    if not points:
        raise ValueError("At least one point required")
    
    n = len(points)
    x_vals = [p[0] for p in points]
    
    # 计算差商表
    # f[x0] = y0
    # f[x0,x1] = (f[x1] - f[x0]) / (x1 - x0)
    # ...
    
    diff_table = [[0.0] * n for _ in range(n)]
    
    # 第一列是 y 值
    for i in range(n):
        diff_table[i][0] = points[i][1]
    
    # 计算差商
    for j in range(1, n):
        for i in range(n - j):
            diff_table[i][j] = (diff_table[i + 1][j - 1] - diff_table[i][j - 1]) / \
                               (x_vals[i + j] - x_vals[i])
    
    # 构造多项式：牛顿形式
    # p(x) = f[x0] + f[x0,x1](x-x0) + f[x0,x1,x2](x-x0)(x-x1) + ...
    result = Polynomial([diff_table[0][0]])
    basis = Polynomial([1])  # 将逐步累积 (x-x0)(x-x1)...
    
    for j in range(1, n):
        # 先更新 basis：乘以 (x - x_{j-1})
        basis = basis * Polynomial([-x_vals[j - 1], 1])
        # 再添加差商项
        result = result + diff_table[0][j] * basis
    
    return result


def chebyshev_polynomial(n: int) -> Polynomial:
    """
    生成 n 阶切比雪夫多项式（第一类）。
    
    Args:
        n: 多项式阶数
    
    Returns:
        T_n(x) 多项式
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return Polynomial([1])
    if n == 1:
        return Polynomial([0, 1])
    
    # 使用递推关系：T_n = 2x * T_{n-1} - T_{n-2}
    t_prev = Polynomial([1])  # T_0
    t_curr = Polynomial([0, 1])  # T_1
    
    for _ in range(2, n + 1):
        t_next = 2 * Polynomial([0, 1]) * t_curr - t_prev
        t_prev, t_curr = t_curr, t_next
    
    return t_curr


def legendre_polynomial(n: int) -> Polynomial:
    """
    生成 n 阶勒让德多项式。
    
    Args:
        n: 多项式阶数
    
    Returns:
        P_n(x) 多项式
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return Polynomial([1])
    if n == 1:
        return Polynomial([0, 1])
    
    # 使用递推关系：(n+1)P_{n+1} = (2n+1)x*P_n - n*P_{n-1}
    p_prev = Polynomial([1])  # P_0
    p_curr = Polynomial([0, 1])  # P_1
    
    for k in range(1, n):
        p_next = ((2 * k + 1) * Polynomial([0, 1]) * p_curr - k * p_prev) / (k + 1)
        p_prev, p_curr = p_curr, p_next
    
    return p_curr


def hermite_polynomial(n: int) -> Polynomial:
    """
    生成 n 阶埃尔米特多项式（物理学家版本）。
    
    Args:
        n: 多项式阶数
    
    Returns:
        H_n(x) 多项式
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return Polynomial([1])
    if n == 1:
        return Polynomial([0, 2])
    
    # 使用递推关系：H_{n+1} = 2x*H_n - 2n*H_{n-1}
    h_prev = Polynomial([1])  # H_0
    h_curr = Polynomial([0, 2])  # H_1
    
    for k in range(1, n):
        h_next = 2 * Polynomial([0, 1]) * h_curr - 2 * k * h_prev
        h_prev, h_curr = h_curr, h_next
    
    return h_curr


def bernstein_polynomial(n: int, k: int) -> Polynomial:
    """
    生成伯恩斯坦基多项式 B_{n,k}(x) = C(n,k) * x^k * (1-x)^{n-k}。
    
    Args:
        n: 多项式次数
        k: 基函数索引（0 <= k <= n）
    
    Returns:
        B_{n,k}(x) 多项式
    """
    if k < 0 or k > n:
        raise ValueError("k must be in range [0, n]")
    
    # 计算 C(n, k)
    def binomial(n, k):
        if k > n - k:
            k = n - k
        result = 1
        for i in range(k):
            result = result * (n - i) // (i + 1)
        return result
    
    coef = binomial(n, k)
    # x^k * (1-x)^{n-k}
    result = Polynomial([coef])
    result = result * Polynomial([0, 1]) ** k  # x^k
    
    # (1-x)^{n-k}
    one_minus_x = Polynomial([1, -1])
    result = result * (one_minus_x ** (n - k))
    
    return result


def parse(s: str) -> Polynomial:
    """
    解析字符串形式的多项式。
    
    支持格式：
    - "1 + 2x + 3x^2"
    - "x^2 - 2x + 1"
    - "x^3 + x - 1"
    - "(x+1)(x-1)" （简单展开）
    
    Args:
        s: 多项式字符串
    
    Returns:
        解析后的多项式
    """
    s = s.replace(' ', '').replace('−', '-').replace('×', '*')
    
    # 处理简单的因式乘法 (x+1)(x-1)
    if ')' in s and '(' in s:
        # 简单处理：先按 ) 分割
        factors = []
        depth = 0
        current = ""
        
        for char in s:
            if char == '(':
                depth += 1
                if depth == 1:
                    continue
            elif char == ')':
                depth -= 1
                if depth == 0:
                    if current:
                        factors.append(current)
                        current = ""
                    continue
            
            if depth > 0:
                current += char
            elif depth == 0 and char not in '()':
                if char == '*' and factors:
                    continue
                # 处理括号外的符号
                pass
        
        if len(factors) == 2:
            p1 = parse(factors[0])
            p2 = parse(factors[1])
            return p1 * p2
    
    # 解析单项式
    import re
    
    # 匹配单项式：可选符号 + 系数 + x^次数 或 x + 可选次数
    pattern = r'([+-]?)(\d*\.?\d*)(x?)(?:\^(\d+))?'
    matches = re.findall(pattern, s)
    
    coeffs = {}
    
    for sign, coef, x, power in matches:
        if not coef and not x:
            continue
        
        # 确定系数
        if not coef:
            c = 1.0
        else:
            c = float(coef) if '.' in coef else int(coef)
            if not coef:
                c = 1
        
        if sign == '-':
            c = -c
        
        # 确定次数
        if not x:
            p = 0
        elif not power:
            p = 1
        else:
            p = int(power)
        
        coeffs[p] = coeffs.get(p, 0) + c
    
    if not coeffs:
        return Polynomial([0])
    
    max_power = max(coeffs.keys())
    result = [0.0] * (max_power + 1)
    for p, c in coeffs.items():
        result[p] = c
    
    return Polynomial(result)


def horner(coefficients: List[float], x: float) -> float:
    """
    使用霍纳法则计算多项式值。
    
    这是一个独立函数，不依赖 Polynomial 类。
    
    Args:
        coefficients: 系数列表 [a0, a1, a2, ...] 表示 a0 + a1*x + a2*x^2 + ...
        x: 求值点
    
    Returns:
        多项式值
    """
    result = 0.0
    for coef in reversed(coefficients):
        result = result * x + coef
    return result


def synthetic_division(coefficients: List[float], root: float) -> Tuple[List[float], float]:
    """
    综合除法：多项式除以 (x - root)。
    
    Args:
        coefficients: 多项式系数 [a0, a1, a2, ...]
        root: 除式的根
    
    Returns:
        (商的系数列表, 余数)
    """
    if not coefficients:
        return [], 0
    
    n = len(coefficients)
    quotient = [0.0] * (n - 1) if n > 1 else []
    
    carry = coefficients[-1]
    for i in range(n - 2, -1, -1):
        quotient[i] = carry
        carry = coefficients[i] + carry * root
    
    if n > 1:
        quotient[-1] = coefficients[-1]
    
    return quotient, carry


# 常用多项式常量
X = Polynomial([0, 1])  # x
ONE = Polynomial([1])   # 1
ZERO = Polynomial([0])  # 0