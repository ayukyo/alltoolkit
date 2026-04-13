"""
数学工具模块 - 提供常用数学运算功能
零外部依赖，纯 Python 标准库实现

功能：
- 基础数学运算（阶乘、斐波那契、GCD、LCM）
- 数论工具（素数检测、素数生成、因数分解）
- 几何计算（面积、距离、角度）
- 统计扩展（标准差、方差、中位数、众数）
- 数值处理（四舍五入、取整、百分比）
- 向量和矩阵基础运算
- 插值和序列生成
"""

import math
import random
from typing import List, Tuple, Optional, Union, Iterator
from functools import reduce
from collections import Counter


Number = Union[int, float]


class MathUtils:
    """数学工具类"""
    
    # ==================== 基础运算 ====================
    
    @staticmethod
    def factorial(n: int) -> int:
        """
        计算阶乘
        
        Args:
            n: 非负整数
            
        Returns:
            n! 的值
            
        Raises:
            ValueError: n 为负数时
            
        Example:
            >>> MathUtils.factorial(5)
            120
        """
        if n < 0:
            raise ValueError("阶乘不支持负数")
        if n <= 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    @staticmethod
    def fibonacci(n: int) -> int:
        """
        计算第 n 个斐波那契数（从 0 开始）
        
        Args:
            n: 索引位置（非负整数）
            
        Returns:
            第 n 个斐波那契数
            
        Example:
            >>> MathUtils.fibonacci(10)
            55
        """
        if n < 0:
            raise ValueError("斐波那契数列索引不支持负数")
        if n <= 1:
            return n
        
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    
    @staticmethod
    def fibonacci_sequence(n: int) -> List[int]:
        """
        生成前 n 个斐波那契数列
        
        Args:
            n: 数列长度
            
        Returns:
            斐波那契数列
            
        Example:
            >>> MathUtils.fibonacci_sequence(10)
            [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        """
        if n <= 0:
            return []
        if n == 1:
            return [0]
        if n == 2:
            return [0, 1]
        
        result = [0, 1]
        for _ in range(2, n):
            result.append(result[-1] + result[-2])
        return result
    
    @staticmethod
    def gcd(*numbers: int) -> int:
        """
        计算最大公约数
        
        Args:
            *numbers: 两个或多个整数
            
        Returns:
            最大公约数
            
        Example:
            >>> MathUtils.gcd(48, 18)
            6
            >>> MathUtils.gcd(48, 18, 12)
            6
        """
        if not numbers:
            raise ValueError("至少需要一个数")
        return reduce(math.gcd, numbers)
    
    @staticmethod
    def lcm(*numbers: int) -> int:
        """
        计算最小公倍数
        
        Args:
            *numbers: 两个或多个整数
            
        Returns:
            最小公倍数
            
        Example:
            >>> MathUtils.lcm(4, 6)
            12
            >>> MathUtils.lcm(4, 6, 8)
            24
        """
        if not numbers:
            raise ValueError("至少需要一个数")
        
        def _lcm(a: int, b: int) -> int:
            return abs(a * b) // math.gcd(a, b) if a and b else 0
        
        return reduce(_lcm, numbers)
    
    @staticmethod
    def power(base: Number, exponent: Number) -> Number:
        """
        幂运算
        
        Args:
            base: 底数
            exponent: 指数
            
        Returns:
            base^exponent
            
        Example:
            >>> MathUtils.power(2, 10)
            1024
        """
        return base ** exponent
    
    @staticmethod
    def sqrt(n: Number) -> float:
        """
        平方根
        
        Args:
            n: 非负数
            
        Returns:
            平方根
            
        Raises:
            ValueError: n 为负数时
            
        Example:
            >>> MathUtils.sqrt(16)
            4.0
        """
        if n < 0:
            raise ValueError("不支持负数的平方根")
        return math.sqrt(n)
    
    @staticmethod
    def cbrt(n: Number) -> float:
        """
        立方根
        
        Args:
            n: 任意实数
            
        Returns:
            立方根
            
        Example:
            >>> MathUtils.cbrt(27)
            3.0
        """
        if n >= 0:
            return n ** (1/3)
        return -(-n) ** (1/3)
    
    @staticmethod
    def root(n: Number, index: int) -> float:
        """
        n 次方根
        
        Args:
            n: 被开方数
            index: 根指数
            
        Returns:
            n 的 index 次方根
            
        Example:
            >>> MathUtils.root(16, 4)
            2.0
        """
        if index <= 0:
            raise ValueError("根指数必须为正整数")
        if n < 0 and index % 2 == 0:
            raise ValueError("负数的偶数次方根不是实数")
        return n ** (1/index)
    
    @staticmethod
    def abs(n: Number) -> Number:
        """
        绝对值
        
        Args:
            n: 任意数
            
        Returns:
            绝对值
            
        Example:
            >>> MathUtils.abs(-5)
            5
        """
        return abs(n)
    
    @staticmethod
    def sign(n: Number) -> int:
        """
        符号函数
        
        Args:
            n: 任意数
            
        Returns:
            -1, 0, 或 1
            
        Example:
            >>> MathUtils.sign(-5)
            -1
            >>> MathUtils.sign(0)
            0
            >>> MathUtils.sign(5)
            1
        """
        if n > 0:
            return 1
        elif n < 0:
            return -1
        return 0
    
    # ==================== 数论工具 ====================
    
    @staticmethod
    def is_prime(n: int) -> bool:
        """
        判断是否为素数
        
        Args:
            n: 整数
            
        Returns:
            是否为素数
            
        Example:
            >>> MathUtils.is_prime(17)
            True
            >>> MathUtils.is_prime(18)
            False
        """
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    @staticmethod
    def primes_up_to(n: int) -> List[int]:
        """
        生成小于等于 n 的所有素数（埃拉托斯特尼筛法）
        
        Args:
            n: 上限
            
        Returns:
            素数列表
            
        Example:
            >>> MathUtils.primes_up_to(20)
            [2, 3, 5, 7, 11, 13, 17, 19]
        """
        if n < 2:
            return []
        
        sieve = [True] * (n + 1)
        sieve[0] = sieve[1] = False
        
        for i in range(2, int(math.sqrt(n)) + 1):
            if sieve[i]:
                for j in range(i*i, n + 1, i):
                    sieve[j] = False
        
        return [i for i, is_prime in enumerate(sieve) if is_prime]
    
    @staticmethod
    def prime_factors(n: int) -> List[int]:
        """
        分解质因数
        
        Args:
            n: 正整数
            
        Returns:
            质因数列表（包含重复）
            
        Raises:
            ValueError: n <= 1 时
            
        Example:
            >>> MathUtils.prime_factors(60)
            [2, 2, 3, 5]
        """
        if n <= 1:
            raise ValueError("输入必须大于 1")
        
        factors = []
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors.append(d)
                n //= d
            d += 1
        if n > 1:
            factors.append(n)
        return factors
    
    @staticmethod
    def divisors(n: int) -> List[int]:
        """
        获取所有因数
        
        Args:
            n: 正整数
            
        Returns:
            因数列表（升序）
            
        Example:
            >>> MathUtils.divisors(12)
            [1, 2, 3, 4, 6, 12]
        """
        if n <= 0:
            raise ValueError("输入必须为正整数")
        
        result = set()
        for i in range(1, int(math.sqrt(n)) + 1):
            if n % i == 0:
                result.add(i)
                result.add(n // i)
        return sorted(result)
    
    @staticmethod
    def count_divisors(n: int) -> int:
        """
        计算因数个数
        
        Args:
            n: 正整数
            
        Returns:
            因数个数
            
        Example:
            >>> MathUtils.count_divisors(12)
            6
        """
        return len(MathUtils.divisors(n))
    
    @staticmethod
    def euler_totient(n: int) -> int:
        """
        欧拉函数（小于 n 且与 n 互质的正整数个数）
        
        Args:
            n: 正整数
            
        Returns:
            φ(n)
            
        Example:
            >>> MathUtils.euler_totient(9)
            6
        """
        if n <= 0:
            raise ValueError("输入必须为正整数")
        
        result = n
        p = 2
        temp = n
        
        while p * p <= temp:
            if temp % p == 0:
                while temp % p == 0:
                    temp //= p
                result -= result // p
            p += 1
        
        if temp > 1:
            result -= result // temp
        
        return result
    
    @staticmethod
    def is_perfect_number(n: int) -> bool:
        """
        判断是否为完全数
        
        Args:
            n: 正整数
            
        Returns:
            是否为完全数
            
        Example:
            >>> MathUtils.is_perfect_number(28)
            True
        """
        if n <= 1:
            return False
        
        divisors_sum = sum(MathUtils.divisors(n)[:-1])
        return divisors_sum == n
    
    # ==================== 几何计算 ====================
    
    @staticmethod
    def distance_2d(p1: Tuple[Number, Number], p2: Tuple[Number, Number]) -> float:
        """
        计算两点间的欧几里得距离
        
        Args:
            p1: 第一个点 (x, y)
            p2: 第二个点 (x, y)
            
        Returns:
            两点间距离
            
        Example:
            >>> MathUtils.distance_2d((0, 0), (3, 4))
            5.0
        """
        return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
    
    @staticmethod
    def distance_3d(p1: Tuple[Number, Number, Number], 
                    p2: Tuple[Number, Number, Number]) -> float:
        """
        计算三维空间两点间的距离
        
        Args:
            p1: 第一个点 (x, y, z)
            p2: 第二个点 (x, y, z)
            
        Returns:
            两点间距离
            
        Example:
            >>> MathUtils.distance_3d((0, 0, 0), (1, 2, 2))
            3.0
        """
        return math.sqrt((p2[0] - p1[0])**2 + 
                        (p2[1] - p1[1])**2 + 
                        (p2[2] - p1[2])**2)
    
    @staticmethod
    def circle_area(radius: Number) -> float:
        """
        计算圆的面积
        
        Args:
            radius: 半径
            
        Returns:
            面积
            
        Example:
            >>> MathUtils.circle_area(1)
            3.141592653589793
        """
        if radius < 0:
            raise ValueError("半径不能为负数")
        return math.pi * radius ** 2
    
    @staticmethod
    def circle_circumference(radius: Number) -> float:
        """
        计算圆的周长
        
        Args:
            radius: 半径
            
        Returns:
            周长
            
        Example:
            >>> MathUtils.circle_circumference(1)
            6.283185307179586
        """
        if radius < 0:
            raise ValueError("半径不能为负数")
        return 2 * math.pi * radius
    
    @staticmethod
    def sphere_volume(radius: Number) -> float:
        """
        计算球的体积
        
        Args:
            radius: 半径
            
        Returns:
            体积
            
        Example:
            >>> MathUtils.sphere_volume(1)
            4.188790204786391
        """
        if radius < 0:
            raise ValueError("半径不能为负数")
        return (4/3) * math.pi * radius ** 3
    
    @staticmethod
    def sphere_surface_area(radius: Number) -> float:
        """
        计算球的表面积
        
        Args:
            radius: 半径
            
        Returns:
            表面积
            
        Example:
            >>> MathUtils.sphere_surface_area(1)
            12.566370614359172
        """
        if radius < 0:
            raise ValueError("半径不能为负数")
        return 4 * math.pi * radius ** 2
    
    @staticmethod
    def rectangle_area(width: Number, height: Number) -> Number:
        """
        计算矩形面积
        
        Args:
            width: 宽度
            height: 高度
            
        Returns:
            面积
            
        Example:
            >>> MathUtils.rectangle_area(5, 3)
            15
        """
        if width < 0 or height < 0:
            raise ValueError("宽度和高度不能为负数")
        return width * height
    
    @staticmethod
    def triangle_area(base: Number, height: Number) -> Number:
        """
        计算三角形面积（底高法）
        
        Args:
            base: 底边
            height: 高
            
        Returns:
            面积
            
        Example:
            >>> MathUtils.triangle_area(6, 4)
            12.0
        """
        if base < 0 or height < 0:
            raise ValueError("底和高不能为负数")
        return 0.5 * base * height
    
    @staticmethod
    def triangle_area_heron(a: Number, b: Number, c: Number) -> float:
        """
        使用海伦公式计算三角形面积
        
        Args:
            a: 边长 a
            b: 边长 b
            c: 边长 c
            
        Returns:
            面积
            
        Example:
            >>> MathUtils.triangle_area_heron(3, 4, 5)
            6.0
        """
        if a <= 0 or b <= 0 or c <= 0:
            raise ValueError("边长必须为正数")
        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError("无法构成三角形")
        
        s = (a + b + c) / 2
        return math.sqrt(s * (s - a) * (s - b) * (s - c))
    
    @staticmethod
    def cylinder_volume(radius: Number, height: Number) -> float:
        """
        计算圆柱体体积
        
        Args:
            radius: 底面半径
            height: 高度
            
        Returns:
            体积
            
        Example:
            >>> MathUtils.cylinder_volume(3, 5)
            141.3716694115407
        """
        if radius < 0 or height < 0:
            raise ValueError("半径和高度不能为负数")
        return math.pi * radius ** 2 * height
    
    @staticmethod
    def cone_volume(radius: Number, height: Number) -> float:
        """
        计算圆锥体体积
        
        Args:
            radius: 底面半径
            height: 高度
            
        Returns:
            体积
            
        Example:
            >>> MathUtils.cone_volume(3, 5)
            47.12388980384689
        """
        if radius < 0 or height < 0:
            raise ValueError("半径和高度不能为负数")
        return (1/3) * math.pi * radius ** 2 * height
    
    @staticmethod
    def angle_between_vectors(v1: Tuple[Number, Number], 
                              v2: Tuple[Number, Number]) -> float:
        """
        计算两向量夹角（弧度）
        
        Args:
            v1: 向量1 (x, y)
            v2: 向量2 (x, y)
            
        Returns:
            夹角（弧度）
            
        Example:
            >>> round(MathUtils.angle_between_vectors((1, 0), (0, 1)), 4)
            1.5708
        """
        dot = v1[0] * v2[0] + v1[1] * v2[1]
        mag1 = math.sqrt(v1[0]**2 + v1[1]**2)
        mag2 = math.sqrt(v2[0]**2 + v2[1]**2)
        
        if mag1 == 0 or mag2 == 0:
            raise ValueError("零向量无法计算夹角")
        
        cos_angle = max(-1, min(1, dot / (mag1 * mag2)))
        return math.acos(cos_angle)
    
    # ==================== 统计扩展 ====================
    
    @staticmethod
    def mean(values: List[Number]) -> float:
        """
        计算平均值
        
        Args:
            values: 数值列表
            
        Returns:
            平均值
            
        Example:
            >>> MathUtils.mean([1, 2, 3, 4, 5])
            3.0
        """
        if not values:
            raise ValueError("列表不能为空")
        return sum(values) / len(values)
    
    @staticmethod
    def median(values: List[Number]) -> float:
        """
        计算中位数
        
        Args:
            values: 数值列表
            
        Returns:
            中位数
            
        Example:
            >>> MathUtils.median([1, 2, 3, 4, 5])
            3
            >>> MathUtils.median([1, 2, 3, 4])
            2.5
        """
        if not values:
            raise ValueError("列表不能为空")
        
        sorted_values = sorted(values)
        n = len(sorted_values)
        mid = n // 2
        
        if n % 2 == 0:
            return (sorted_values[mid - 1] + sorted_values[mid]) / 2
        return sorted_values[mid]
    
    @staticmethod
    def mode(values: List[Number]) -> List[Number]:
        """
        计算众数（可能有多个）
        
        Args:
            values: 数值列表
            
        Returns:
            众数列表
            
        Example:
            >>> MathUtils.mode([1, 2, 2, 3, 3, 3])
            [3]
            >>> MathUtils.mode([1, 1, 2, 2])
            [1, 2]
        """
        if not values:
            raise ValueError("列表不能为空")
        
        counter = Counter(values)
        max_count = max(counter.values())
        return sorted([v for v, c in counter.items() if c == max_count])
    
    @staticmethod
    def variance(values: List[Number], population: bool = True) -> float:
        """
        计算方差
        
        Args:
            values: 数值列表
            population: 是否为总体方差（默认 True）
            
        Returns:
            方差
            
        Example:
            >>> MathUtils.variance([1, 2, 3, 4, 5])
            2.0
        """
        if not values:
            raise ValueError("列表不能为空")
        
        n = len(values)
        avg = MathUtils.mean(values)
        squared_diff_sum = sum((x - avg) ** 2 for x in values)
        
        if population:
            return squared_diff_sum / n
        return squared_diff_sum / (n - 1)  # 样本方差
    
    @staticmethod
    def standard_deviation(values: List[Number], population: bool = True) -> float:
        """
        计算标准差
        
        Args:
            values: 数值列表
            population: 是否为总体标准差（默认 True）
            
        Returns:
            标准差
            
        Example:
            >>> MathUtils.standard_deviation([1, 2, 3, 4, 5])
            1.4142135623730951
        """
        return math.sqrt(MathUtils.variance(values, population))
    
    @staticmethod
    def range_value(values: List[Number]) -> Number:
        """
        计算极差（全距）
        
        Args:
            values: 数值列表
            
        Returns:
            极差
            
        Example:
            >>> MathUtils.range_value([1, 2, 3, 4, 5])
            4
        """
        if not values:
            raise ValueError("列表不能为空")
        return max(values) - min(values)
    
    @staticmethod
    def percentile(values: List[Number], p: Number) -> float:
        """
        计算百分位数
        
        Args:
            values: 数值列表
            p: 百分位（0-100）
            
        Returns:
            百分位数
            
        Example:
            >>> MathUtils.percentile([1, 2, 3, 4, 5], 50)
            3.0
        """
        if not values:
            raise ValueError("列表不能为空")
        if not 0 <= p <= 100:
            raise ValueError("百分位必须在 0-100 之间")
        
        sorted_values = sorted(values)
        n = len(sorted_values)
        index = (p / 100) * (n - 1)
        
        lower = int(index)
        upper = lower + 1
        
        if upper >= n:
            return sorted_values[-1]
        
        weight = index - lower
        return sorted_values[lower] * (1 - weight) + sorted_values[upper] * weight
    
    @staticmethod
    def quartiles(values: List[Number]) -> Tuple[float, float, float]:
        """
        计算四分位数
        
        Args:
            values: 数值列表
            
        Returns:
            (Q1, Q2, Q3)
            
        Example:
            >>> MathUtils.quartiles([1, 2, 3, 4, 5, 6, 7])
            (2.0, 4.0, 6.0)
        """
        q1 = MathUtils.percentile(values, 25)
        q2 = MathUtils.percentile(values, 50)
        q3 = MathUtils.percentile(values, 75)
        return (q1, q2, q3)
    
    @staticmethod
    def iqr(values: List[Number]) -> float:
        """
        计算四分位距（IQR）
        
        Args:
            values: 数值列表
            
        Returns:
            IQR 值
            
        Example:
            >>> MathUtils.iqr([1, 2, 3, 4, 5, 6, 7])
            4.0
        """
        q1, _, q3 = MathUtils.quartiles(values)
        return q3 - q1
    
    @staticmethod
    def covariance(x: List[Number], y: List[Number], population: bool = True) -> float:
        """
        计算协方差
        
        Args:
            x: 第一组数值
            y: 第二组数值
            population: 是否为总体协方差
            
        Returns:
            协方差
            
        Example:
            >>> MathUtils.covariance([1, 2, 3], [4, 5, 6])
            0.6666666666666666
        """
        if len(x) != len(y):
            raise ValueError("两组数据长度必须相同")
        if not x:
            raise ValueError("数据不能为空")
        
        n = len(x)
        mean_x = MathUtils.mean(x)
        mean_y = MathUtils.mean(y)
        
        cov_sum = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        
        if population:
            return cov_sum / n
        return cov_sum / (n - 1)
    
    @staticmethod
    def correlation(x: List[Number], y: List[Number]) -> float:
        """
        计算皮尔逊相关系数
        
        Args:
            x: 第一组数值
            y: 第二组数值
            
        Returns:
            相关系数（-1 到 1）
            
        Example:
            >>> MathUtils.correlation([1, 2, 3], [2, 4, 6])
            1.0
        """
        if len(x) != len(y):
            raise ValueError("两组数据长度必须相同")
        if not x:
            raise ValueError("数据不能为空")
        
        n = len(x)
        mean_x = MathUtils.mean(x)
        mean_y = MathUtils.mean(y)
        
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = math.sqrt(
            sum((xi - mean_x) ** 2 for xi in x) * 
            sum((yi - mean_y) ** 2 for yi in y)
        )
        
        if denominator == 0:
            return 0.0
        
        return numerator / denominator
    
    # ==================== 数值处理 ====================
    
    @staticmethod
    def round_to(value: Number, decimals: int = 0) -> Number:
        """
        四舍五入到指定小数位
        
        Args:
            value: 数值
            decimals: 小数位数
            
        Returns:
            四舍五入后的值
            
        Example:
            >>> MathUtils.round_to(3.14159, 2)
            3.14
        """
        return round(value, decimals)
    
    @staticmethod
    def round_up(value: Number, decimals: int = 0) -> Number:
        """
        向上取整到指定小数位
        
        Args:
            value: 数值
            decimals: 小数位数
            
        Returns:
            向上取整后的值
            
        Example:
            >>> MathUtils.round_up(3.14, 1)
            3.2
        """
        multiplier = 10 ** decimals
        return math.ceil(value * multiplier) / multiplier
    
    @staticmethod
    def round_down(value: Number, decimals: int = 0) -> Number:
        """
        向下取整到指定小数位
        
        Args:
            value: 数值
            decimals: 小数位数
            
        Returns:
            向下取整后的值
            
        Example:
            >>> MathUtils.round_down(3.19, 1)
            3.1
        """
        multiplier = 10 ** decimals
        return math.floor(value * multiplier) / multiplier
    
    @staticmethod
    def truncate(value: Number, decimals: int = 0) -> Number:
        """
        截断到指定小数位
        
        Args:
            value: 数值
            decimals: 小数位数
            
        Returns:
            截断后的值
            
        Example:
            >>> MathUtils.truncate(3.14159, 2)
            3.14
        """
        multiplier = 10 ** decimals
        return int(value * multiplier) / multiplier
    
    @staticmethod
    def clamp(value: Number, min_val: Number, max_val: Number) -> Number:
        """
        将值限制在指定范围内
        
        Args:
            value: 数值
            min_val: 最小值
            max_val: 最大值
            
        Returns:
            限制后的值
            
        Example:
            >>> MathUtils.clamp(10, 0, 5)
            5
            >>> MathUtils.clamp(-1, 0, 5)
            0
        """
        return max(min_val, min(value, max_val))
    
    @staticmethod
    def percentage(value: Number, total: Number, decimals: int = 2) -> float:
        """
        计算百分比
        
        Args:
            value: 部分值
            total: 总值
            decimals: 小数位数
            
        Returns:
            百分比值（0-100）
            
        Example:
            >>> MathUtils.percentage(25, 200)
            12.5
        """
        if total == 0:
            raise ValueError("总值不能为 0")
        return round((value / total) * 100, decimals)
    
    @staticmethod
    def percentage_change(old: Number, new: Number, decimals: int = 2) -> float:
        """
        计算百分比变化
        
        Args:
            old: 原值
            new: 新值
            decimals: 小数位数
            
        Returns:
            百分比变化（正为增加，负为减少）
            
        Example:
            >>> MathUtils.percentage_change(100, 150)
            50.0
            >>> MathUtils.percentage_change(100, 80)
            -20.0
        """
        if old == 0:
            raise ValueError("原值不能为 0")
        return round(((new - old) / old) * 100, decimals)
    
    @staticmethod
    def ratio_to_percentage(ratio: Number, decimals: int = 2) -> float:
        """
        比率转百分比
        
        Args:
            ratio: 比率（0-1）
            decimals: 小数位数
            
        Returns:
            百分比
            
        Example:
            >>> MathUtils.ratio_to_percentage(0.75)
            75.0
        """
        return round(ratio * 100, decimals)
    
    # ==================== 向量运算 ====================
    
    @staticmethod
    def vector_add(v1: Tuple[Number, ...], v2: Tuple[Number, ...]) -> Tuple[Number, ...]:
        """
        向量加法
        
        Args:
            v1: 向量1
            v2: 向量2
            
        Returns:
            和向量
            
        Example:
            >>> MathUtils.vector_add((1, 2, 3), (4, 5, 6))
            (5, 7, 9)
        """
        if len(v1) != len(v2):
            raise ValueError("向量维度必须相同")
        return tuple(a + b for a, b in zip(v1, v2))
    
    @staticmethod
    def vector_subtract(v1: Tuple[Number, ...], v2: Tuple[Number, ...]) -> Tuple[Number, ...]:
        """
        向量减法
        
        Args:
            v1: 向量1
            v2: 向量2
            
        Returns:
            差向量
            
        Example:
            >>> MathUtils.vector_subtract((4, 5, 6), (1, 2, 3))
            (3, 3, 3)
        """
        if len(v1) != len(v2):
            raise ValueError("向量维度必须相同")
        return tuple(a - b for a, b in zip(v1, v2))
    
    @staticmethod
    def vector_scale(v: Tuple[Number, ...], scalar: Number) -> Tuple[Number, ...]:
        """
        向量数乘
        
        Args:
            v: 向量
            scalar: 标量
            
        Returns:
            缩放后的向量
            
        Example:
            >>> MathUtils.vector_scale((1, 2, 3), 2)
            (2, 4, 6)
        """
        return tuple(a * scalar for a in v)
    
    @staticmethod
    def vector_dot(v1: Tuple[Number, ...], v2: Tuple[Number, ...]) -> Number:
        """
        向量点积
        
        Args:
            v1: 向量1
            v2: 向量2
            
        Returns:
            点积
            
        Example:
            >>> MathUtils.vector_dot((1, 2, 3), (4, 5, 6))
            32
        """
        if len(v1) != len(v2):
            raise ValueError("向量维度必须相同")
        return sum(a * b for a, b in zip(v1, v2))
    
    @staticmethod
    def vector_cross_3d(v1: Tuple[Number, Number, Number], 
                        v2: Tuple[Number, Number, Number]) -> Tuple[Number, Number, Number]:
        """
        三维向量叉积
        
        Args:
            v1: 向量1 (x, y, z)
            v2: 向量2 (x, y, z)
            
        Returns:
            叉积向量
            
        Example:
            >>> MathUtils.vector_cross_3d((1, 0, 0), (0, 1, 0))
            (0, 0, 1)
        """
        return (
            v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0]
        )
    
    @staticmethod
    def vector_magnitude(v: Tuple[Number, ...]) -> float:
        """
        向量模长
        
        Args:
            v: 向量
            
        Returns:
            模长
            
        Example:
            >>> MathUtils.vector_magnitude((3, 4))
            5.0
        """
        return math.sqrt(sum(a ** 2 for a in v))
    
    @staticmethod
    def vector_normalize(v: Tuple[Number, ...]) -> Tuple[float, ...]:
        """
        向量归一化（单位向量）
        
        Args:
            v: 向量
            
        Returns:
            单位向量
            
        Example:
            >>> MathUtils.vector_normalize((3, 4))
            (0.6, 0.8)
        """
        mag = MathUtils.vector_magnitude(v)
        if mag == 0:
            raise ValueError("零向量无法归一化")
        return tuple(a / mag for a in v)
    
    # ==================== 序列生成 ====================
    
    @staticmethod
    def arithmetic_sequence(start: Number, diff: Number, n: int) -> List[Number]:
        """
        生成等差数列
        
        Args:
            start: 首项
            diff: 公差
            n: 项数
            
        Returns:
            等差数列
            
        Example:
            >>> MathUtils.arithmetic_sequence(1, 2, 5)
            [1, 3, 5, 7, 9]
        """
        if n <= 0:
            return []
        return [start + i * diff for i in range(n)]
    
    @staticmethod
    def arithmetic_sum(start: Number, diff: Number, n: int) -> Number:
        """
        计算等差数列前 n 项和
        
        Args:
            start: 首项
            diff: 公差
            n: 项数
            
        Returns:
            前 n 项和
            
        Example:
            >>> MathUtils.arithmetic_sum(1, 2, 5)
            25
        """
        if n <= 0:
            return 0
        return n * (2 * start + (n - 1) * diff) / 2
    
    @staticmethod
    def geometric_sequence(start: Number, ratio: Number, n: int) -> List[Number]:
        """
        生成等比数列
        
        Args:
            start: 首项
            ratio: 公比
            n: 项数
            
        Returns:
            等比数列
            
        Example:
            >>> MathUtils.geometric_sequence(1, 2, 5)
            [1, 2, 4, 8, 16]
        """
        if n <= 0:
            return []
        return [start * (ratio ** i) for i in range(n)]
    
    @staticmethod
    def geometric_sum(start: Number, ratio: Number, n: int) -> Number:
        """
        计算等比数列前 n 项和
        
        Args:
            start: 首项
            ratio: 公比
            n: 项数
            
        Returns:
            前 n 项和
            
        Example:
            >>> MathUtils.geometric_sum(1, 2, 5)
            31
        """
        if n <= 0:
            return 0
        if ratio == 1:
            return start * n
        return start * (1 - ratio ** n) / (1 - ratio)
    
    @staticmethod
    def range_float(start: Number, stop: Number, step: Number) -> List[float]:
        """
        生成浮点数范围
        
        Args:
            start: 起始值
            stop: 结束值（不包含）
            step: 步长
            
        Returns:
            浮点数列表
            
        Example:
            >>> MathUtils.range_float(0, 1, 0.2)
            [0.0, 0.2, 0.4, 0.6000000000000001, 0.8]
        """
        if step == 0:
            raise ValueError("步长不能为 0")
        
        result = []
        current = start
        
        if step > 0:
            while current < stop:
                result.append(float(current))
                current += step
        else:
            while current > stop:
                result.append(float(current))
                current += step
        
        return result
    
    @staticmethod
    def linspace(start: Number, stop: Number, num: int) -> List[float]:
        """
        生成等间距数列
        
        Args:
            start: 起始值
            stop: 结束值
            num: 数量
            
        Returns:
            等间距数列
            
        Example:
            >>> MathUtils.linspace(0, 10, 5)
            [0.0, 2.5, 5.0, 7.5, 10.0]
        """
        if num <= 1:
            return [float(start)]
        
        step = (stop - start) / (num - 1)
        return [float(start + i * step) for i in range(num)]
    
    # ==================== 数值检查 ====================
    
    @staticmethod
    def is_even(n: int) -> bool:
        """判断是否为偶数"""
        return n % 2 == 0
    
    @staticmethod
    def is_odd(n: int) -> bool:
        """判断是否为奇数"""
        return n % 2 != 0
    
    @staticmethod
    def is_integer(n: Number, tolerance: float = 1e-9) -> bool:
        """
        判断浮点数是否为整数
        
        Args:
            n: 数值
            tolerance: 容差
            
        Returns:
            是否为整数
        """
        return abs(n - round(n)) < tolerance
    
    @staticmethod
    def is_power_of(n: int, base: int) -> bool:
        """
        判断 n 是否是 base 的幂次
        
        Args:
            n: 待判断数
            base: 底数
            
        Returns:
            是否为 base 的幂次
        """
        if n <= 0 or base <= 1:
            return False
        while n % base == 0:
            n //= base
        return n == 1
    
    @staticmethod
    def is_perfect_square(n: int) -> bool:
        """
        判断是否为完全平方数
        
        Args:
            n: 待判断数
            
        Returns:
            是否为完全平方数
        """
        if n < 0:
            return False
        root = int(math.sqrt(n))
        return root * root == n
    
    @staticmethod
    def is_perfect_cube(n: int) -> bool:
        """
        判断是否为完全立方数
        
        Args:
            n: 待判断数
            
        Returns:
            是否为完全立方数
        """
        root = round(n ** (1/3))
        return root ** 3 == n
    
    @staticmethod
    def is_armstrong(n: int) -> bool:
        """
        判断是否为阿姆斯特朗数
        
        Args:
            n: 待判断数
            
        Returns:
            是否为阿姆斯特朗数
        """
        if n < 0:
            return False
        digits = [int(d) for d in str(n)]
        power = len(digits)
        return sum(d ** power for d in digits) == n
    
    @staticmethod
    def is_palindrome_number(n: int) -> bool:
        """
        判断是否为回文数
        
        Args:
            n: 待判断数
            
        Returns:
            是否为回文数
        """
        if n < 0:
            return False
        return str(n) == str(n)[::-1]
    
    # ==================== 随机数 ====================
    
    @staticmethod
    def random_int(min_val: int, max_val: int) -> int:
        """生成指定范围内的随机整数"""
        return random.randint(min_val, max_val)
    
    @staticmethod
    def random_float(min_val: float = 0.0, max_val: float = 1.0) -> float:
        """生成指定范围内的随机浮点数"""
        return random.uniform(min_val, max_val)
    
    @staticmethod
    def random_choice(values: List) -> any:
        """从列表中随机选择一个元素"""
        if not values:
            raise ValueError("列表不能为空")
        return random.choice(values)
    
    @staticmethod
    def random_sample(values: List, k: int) -> List:
        """从列表中随机选择 k 个不重复的元素"""
        if k > len(values):
            raise ValueError("k 不能大于列表长度")
        return random.sample(values, k)
    
    @staticmethod
    def shuffle(values: List) -> List:
        """打乱列表（返回新列表）"""
        result = values.copy()
        random.shuffle(result)
        return result


# 便捷函数导出
factorial = MathUtils.factorial
fibonacci = MathUtils.fibonacci
gcd = MathUtils.gcd
lcm = MathUtils.lcm
is_prime = MathUtils.is_prime
primes_up_to = MathUtils.primes_up_to
prime_factors = MathUtils.prime_factors
distance_2d = MathUtils.distance_2d
distance_3d = MathUtils.distance_3d
mean = MathUtils.mean
median = MathUtils.median
mode = MathUtils.mode
variance = MathUtils.variance
standard_deviation = MathUtils.standard_deviation
percentile = MathUtils.percentile