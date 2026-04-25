"""
Fibonacci Utils - 斐波那契数列工具集

提供斐波那契数列的生成、计算、验证等功能。
零外部依赖，纯Python实现。

功能：
- 生成斐波那契数列
- 计算第N个斐波那契数（迭代/递归/矩阵快速幂）
- 验证数字是否为斐波那契数
- 找到最接近的斐波那契数
- 斐波那契编码（Zeckendorf表示）
- 黄金比例相关计算
"""

from typing import List, Tuple, Optional, Iterator
import math


class FibonacciUtils:
    """斐波那契数列工具类"""
    
    # 预计算的小型缓存（前100个斐波那契数）
    _CACHE: List[int] = [0, 1]
    _CACHE_SIZE = 100
    
    @classmethod
    def _ensure_cache(cls, n: int) -> None:
        """确保缓存足够大"""
        while len(cls._CACHE) <= n:
            cls._CACHE.append(cls._CACHE[-1] + cls._CACHE[-2])
    
    @staticmethod
    def generate(n: int) -> List[int]:
        """
        生成前n个斐波那契数
        
        Args:
            n: 要生成的斐波那契数数量
            
        Returns:
            包含前n个斐波那契数的列表
            
        Examples:
            >>> FibonacciUtils.generate(10)
            [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        """
        if n <= 0:
            return []
        if n == 1:
            return [0]
        
        result = [0, 1]
        for i in range(2, n):
            result.append(result[-1] + result[-2])
        return result
    
    @staticmethod
    def nth_iterative(n: int) -> int:
        """
        使用迭代法计算第n个斐波那契数
        
        时间复杂度: O(n)
        空间复杂度: O(1)
        
        Args:
            n: 索引（从0开始）
            
        Returns:
            第n个斐波那契数
            
        Examples:
            >>> FibonacciUtils.nth_iterative(10)
            55
        """
        if n < 0:
            raise ValueError("n must be non-negative")
        if n == 0:
            return 0
        if n == 1:
            return 1
        
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    
    @staticmethod
    def nth_recursive(n: int) -> int:
        """
        使用递归法计算第n个斐波那契数（带记忆化）
        
        注意：纯递归无记忆化复杂度为O(2^n)，此版本带记忆化
        
        Args:
            n: 索引（从0开始）
            
        Returns:
            第n个斐波那契数
            
        Examples:
            >>> FibonacciUtils.nth_recursive(10)
            55
        """
        if n < 0:
            raise ValueError("n must be non-negative")
        
        memo = {0: 0, 1: 1}
        
        def fib(k: int) -> int:
            if k in memo:
                return memo[k]
            memo[k] = fib(k - 1) + fib(k - 2)
            return memo[k]
        
        return fib(n)
    
    @staticmethod
    def nth_matrix(n: int) -> int:
        """
        使用矩阵快速幂计算第n个斐波那契数
        
        时间复杂度: O(log n)
        空间复杂度: O(1)
        
        利用矩阵恒等式:
        |F(n+1)|   |1 1|^n   |F(1)|
        |F(n)  | = |1 0|   * |F(0)|
        
        Args:
            n: 索引（从0开始）
            
        Returns:
            第n个斐波那契数
            
        Examples:
            >>> FibonacciUtils.nth_matrix(10)
            55
        """
        if n < 0:
            raise ValueError("n must be non-negative")
        if n == 0:
            return 0
        if n == 1:
            return 1
        
        def matrix_mult(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
            return [
                [A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]],
                [A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]]
            ]
        
        def matrix_pow(M: List[List[int]], p: int) -> List[List[int]]:
            result = [[1, 0], [0, 1]]  # 单位矩阵
            while p > 0:
                if p % 2 == 1:
                    result = matrix_mult(result, M)
                M = matrix_mult(M, M)
                p //= 2
            return result
        
        base = [[1, 1], [1, 0]]
        result = matrix_pow(base, n)
        return result[0][1]
    
    @staticmethod
    def nth_binet(n: int) -> int:
        """
        使用比内公式（Binet's formula）计算第n个斐波那契数
        
        注意：由于浮点精度限制，仅适用于较小的n值
        
        Args:
            n: 索引（从0开始）
            
        Returns:
            第n个斐波那契数
            
        Examples:
            >>> FibonacciUtils.nth_binet(10)
            55
        """
        if n < 0:
            raise ValueError("n must be non-negative")
        
        phi = (1 + math.sqrt(5)) / 2
        psi = (1 - math.sqrt(5)) / 2
        
        return int(round((phi ** n - psi ** n) / math.sqrt(5)))
    
    @staticmethod
    def is_fibonacci(num: int) -> bool:
        """
        判断一个数是否为斐波那契数
        
        利用数学性质：n是斐波那契数当且仅当 5*n^2+4 或 5*n^2-4 是完全平方数
        
        Args:
            num: 要检查的数字
            
        Returns:
            是否为斐波那契数
            
        Examples:
            >>> FibonacciUtils.is_fibonacci(55)
            True
            >>> FibonacciUtils.is_fibonacci(56)
            False
        """
        if num < 0:
            return False
        
        def is_perfect_square(x: int) -> bool:
            if x < 0:
                return False
            root = int(math.sqrt(x))
            return root * root == x
        
        return is_perfect_square(5 * num * num + 4) or is_perfect_square(5 * num * num - 4)
    
    @staticmethod
    def nearest_fibonacci(num: int) -> Tuple[int, int]:
        """
        找到最接近给定数字的斐波那契数
        
        Args:
            num: 目标数字
            
        Returns:
            (最近的斐波那契数, 该数的索引)
            
        Examples:
            >>> FibonacciUtils.nearest_fibonacci(50)
            (55, 10)
            >>> FibonacciUtils.nearest_fibonacci(60)
            (55, 10)
        """
        if num <= 0:
            return (0, 0)
        
        a, b = 0, 1
        index = 1
        
        while b < num:
            a, b = b, a + b
            index += 1
        
        # 比较b和a哪个更接近
        if abs(b - num) < abs(a - num):
            return (b, index)
        else:
            return (a, index - 1)
    
    @staticmethod
    def find_index(num: int) -> int:
        """
        找到斐波那契数的索引（如果存在）
        
        Args:
            num: 斐波那契数
            
        Returns:
            索引（从0开始），如果不是斐波那契数则返回-1
            
        Examples:
            >>> FibonacciUtils.find_index(55)
            10
            >>> FibonacciUtils.find_index(56)
            -1
        """
        if num < 0:
            return -1
        if num == 0:
            return 0
        if num == 1:
            return 1
        
        a, b = 0, 1
        index = 1
        
        while b < num:
            a, b = b, a + b
            index += 1
        
        return index if b == num else -1
    
    @staticmethod
    def range(start: int, end: int) -> List[int]:
        """
        生成指定范围内的斐波那契数
        
        Args:
            start: 起始值（包含）
            end: 结束值（不包含）
            
        Returns:
            范围内的斐波那契数列表
            
        Examples:
            >>> FibonacciUtils.range(10, 100)
            [13, 21, 34, 55, 89]
        """
        if start >= end:
            return []
        
        result = []
        a, b = 0, 1
        
        # 先找到大于等于start的数
        while a < start:
            a, b = b, a + b
        
        # 收集范围内的数
        while a < end:
            result.append(a)
            a, b = b, a + b
        
        return result
    
    @staticmethod
    def sum_first_n(n: int) -> int:
        """
        计算前n个斐波那契数的和
        
        利用公式: F(0) + F(1) + ... + F(n) = F(n+2) - 1
        
        Args:
            n: 斐波那契数数量
            
        Returns:
            前n个斐波那契数的和
            
        Examples:
            >>> FibonacciUtils.sum_first_n(10)
            88  # 0+1+1+2+3+5+8+13+21+34 = 88
        """
        if n <= 0:
            return 0
        
        # F(n+2) - 1
        return FibonacciUtils.nth_iterative(n + 1) - 1
    
    @staticmethod
    def zeckendorf(num: int) -> List[int]:
        """
        将数字表示为斐波那契数的和（Zeckendorf表示）
        
        每个正整数都可以唯一地表示为不相邻的斐波那契数之和
        
        Args:
            num: 要表示的正整数
            
        Returns:
            构成该数的斐波那契数列表（降序）
            
        Examples:
            >>> FibonacciUtils.zeckendorf(100)
            [89, 8, 3]  # 89 + 8 + 3 = 100
        """
        if num <= 0:
            return []
        
        # 生成足够大的斐波那契数列
        fibs = [1, 2]
        while fibs[-1] < num:
            fibs.append(fibs[-1] + fibs[-2])
        
        result = []
        remaining = num
        
        # 贪心算法：从最大的斐波那契数开始
        for fib in reversed(fibs):
            if fib <= remaining:
                result.append(fib)
                remaining -= fib
                if remaining == 0:
                    break
        
        return result
    
    @staticmethod
    def zeckendorf_representation(num: int) -> str:
        """
        返回Zeckendorf表示的字符串形式
        
        Args:
            num: 要表示的正整数
            
        Returns:
            字符串表示
            
        Examples:
            >>> FibonacciUtils.zeckendorf_representation(100)
            '100 = 89 + 8 + 3'
        """
        if num <= 0:
            return f"{num} (无效输入)"
        
        fibs = FibonacciUtils.zeckendorf(num)
        return f"{num} = {' + '.join(map(str, fibs))}"
    
    @staticmethod
    def golden_ratio(precision: int = 10) -> float:
        """
        使用斐波那契数列近似计算黄金比例
        
        黄金比例 φ = (1 + √5) / 2 ≈ 1.6180339887...
        
        Args:
            precision: 使用前n个斐波那契数进行近似
            
        Returns:
            黄金比例的近似值
            
        Examples:
            >>> round(FibonacciUtils.golden_ratio(50), 6)
            1.618034
        """
        if precision < 2:
            return 1.0
        
        fibs = FibonacciUtils.generate(precision + 1)
        return fibs[-1] / fibs[-2]
    
    @staticmethod
    def fibonacci_iterator() -> Iterator[int]:
        """
        返回斐波那契数列的无穷迭代器
        
        Yields:
            斐波那契数
            
        Examples:
            >>> it = FibonacciUtils.fibonacci_iterator()
            >>> [next(it) for _ in range(10)]
            [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        """
        a, b = 0, 1
        yield a
        yield b
        while True:
            a, b = b, a + b
            yield b
    
    @staticmethod
    def lucas_number(n: int) -> int:
        """
        计算第n个卢卡斯数
        
        卢卡斯数列定义: L(0)=2, L(1)=1, L(n)=L(n-1)+L(n-2)
        与斐波那契数列的关系: L(n) = F(n-1) + F(n+1)
        
        Args:
            n: 索引（从0开始）
            
        Returns:
            第n个卢卡斯数
            
        Examples:
            >>> FibonacciUtils.lucas_number(10)
            123
        """
        if n < 0:
            raise ValueError("n must be non-negative")
        if n == 0:
            return 2
        if n == 1:
            return 1
        
        a, b = 2, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    
    @staticmethod
    def pisano_period(m: int) -> int:
        """
        计算斐波那契数列模m的周期（皮萨诺周期）
        
        Args:
            m: 模数
            
        Returns:
            皮萨诺周期长度
            
        Examples:
            >>> FibonacciUtils.pisano_period(10)
            60
            >>> FibonacciUtils.pisano_period(3)
            8
        """
        if m <= 0:
            raise ValueError("m must be positive")
        
        previous, current = 0, 1
        
        for i in range(m * m + 1):
            previous, current = current, (previous + current) % m
            if previous == 0 and current == 1:
                return i + 1
        
        return -1  # 理论上不会到达这里
    
    @staticmethod
    def nth_mod(n: int, m: int) -> int:
        """
        计算第n个斐波那契数模m的值（高效实现）
        
        利用皮萨诺周期优化大数计算
        
        Args:
            n: 斐波那契数索引
            m: 模数
            
        Returns:
            F(n) mod m
            
        Examples:
            >>> FibonacciUtils.nth_mod(100, 7)
            4
        """
        if m <= 0:
            raise ValueError("m must be positive")
        if n < 0:
            raise ValueError("n must be non-negative")
        
        period = FibonacciUtils.pisano_period(m)
        return FibonacciUtils.nth_iterative(n % period) % m
    
    @staticmethod
    def count_digits(n: int) -> int:
        """
        计算第n个斐波那契数的位数
        
        利用比内公式估算: 位数 ≈ n * log10(φ) - log10(√5) + 1
        
        Args:
            n: 斐波那契数索引
            
        Returns:
            F(n)的位数
            
        Examples:
            >>> FibonacciUtils.count_digits(100)
            21  # F(100)有21位数字
        """
        if n <= 0:
            return 1
        if n == 1:
            return 1
        
        # log10(F(n)) ≈ n * log10(φ) - log10(√5)
        phi = (1 + math.sqrt(5)) / 2
        log_fib = n * math.log10(phi) - math.log10(math.sqrt(5))
        return int(log_fib) + 1
    
    @staticmethod
    def gcd_fibonacci(a: int, b: int) -> int:
        """
        计算两个斐波那契数的最大公约数
        
        利用性质: gcd(F(a), F(b)) = F(gcd(a, b))
        
        Args:
            a: 第一个斐波那契数的索引
            b: 第二个斐波那契数的索引
            
        Returns:
            gcd(F(a), F(b))
            
        Examples:
            >>> FibonacciUtils.gcd_fibonacci(12, 18)
            8  # F(gcd(12, 18)) = F(6) = 8
        """
        def gcd(x: int, y: int) -> int:
            while y:
                x, y = y, x % y
            return x
        
        return FibonacciUtils.nth_iterative(gcd(a, b))


# 便捷函数
def generate(n: int) -> List[int]:
    """生成前n个斐波那契数"""
    return FibonacciUtils.generate(n)


def nth(n: int) -> int:
    """计算第n个斐波那契数（自动选择最优算法）"""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n < 1000:
        return FibonacciUtils.nth_iterative(n)
    return FibonacciUtils.nth_matrix(n)


def is_fibonacci(num: int) -> bool:
    """判断是否为斐波那契数"""
    return FibonacciUtils.is_fibonacci(num)


def zeckendorf(num: int) -> List[int]:
    """Zeckendorf表示"""
    return FibonacciUtils.zeckendorf(num)


def golden_ratio(precision: int = 10) -> float:
    """计算黄金比例近似值"""
    return FibonacciUtils.golden_ratio(precision)


if __name__ == "__main__":
    # 简单演示
    print("斐波那契数列前15项:", FibonacciUtils.generate(15))
    print(f"第20个斐波那契数: {FibonacciUtils.nth_iterative(20)}")
    print(f"55是斐波那契数吗? {FibonacciUtils.is_fibonacci(55)}")
    print(f"56是斐波那契数吗? {FibonacciUtils.is_fibonacci(56)}")
    print(f"100的Zeckendorf表示: {FibonacciUtils.zeckendorf_representation(100)}")
    print(f"黄金比例近似值: {FibonacciUtils.golden_ratio(50)}")
    print(f"模10的皮萨诺周期: {FibonacciUtils.pisano_period(10)}")
    print(f"F(100) mod 7 = {FibonacciUtils.nth_mod(100, 7)}")
    print(f"F(100)的位数: {FibonacciUtils.count_digits(100)}")