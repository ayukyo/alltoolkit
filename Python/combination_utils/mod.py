"""
Combination Utilities - 组合数学工具

提供完整的组合数学计算和生成功能，包括：
- 组合数计算 C(n, k)
- 排列数计算 P(n, k)
- 全排列生成
- 组合生成（k组合）
- 幂集生成
- 康托编码（排列索引）
- 多重组合数
- 卡特兰数
- 斯特林数
- 贝尔数

零外部依赖，纯 Python 实现。
"""

from typing import List, Iterator, Optional, Tuple, Generic, TypeVar
from math import factorial, gcd
from functools import reduce
from itertools import permutations, combinations

T = TypeVar('T')


class CombinationCalculator:
    """
    组合数计算器
    
    高效计算组合数和排列数，支持大数。
    
    Example:
        >>> calc = CombinationCalculator()
        >>> calc.combination(10, 3)
        120
        >>> calc.permutation(10, 3)
        720
    """
    
    def __init__(self, use_cache: bool = True, cache_size: int = 1000):
        """
        初始化计算器
        
        Args:
            use_cache: 是否使用缓存加速计算
            cache_size: 缓存大小
        """
        self.use_cache = use_cache
        self.cache_size = cache_size
        self._factorial_cache: dict[int, int] = {0: 1, 1: 1}
        self._combination_cache: dict[Tuple[int, int], int] = {}
        self._permutation_cache: dict[Tuple[int, int], int] = {}
    
    def _get_factorial(self, n: int) -> int:
        """获取阶乘（使用缓存）"""
        if n < 0:
            raise ValueError("阶乘参数必须为非负整数")
        
        if not self.use_cache:
            return factorial(n)
        
        if n in self._factorial_cache:
            return self._factorial_cache[n]
        
        # 从缓存中最大的值开始计算
        max_cached = max(self._factorial_cache.keys())
        result = self._factorial_cache[max_cached]
        
        for i in range(max_cached + 1, n + 1):
            result *= i
            if len(self._factorial_cache) < self.cache_size:
                self._factorial_cache[i] = result
        
        return result
    
    def factorial(self, n: int) -> int:
        """
        计算 n 的阶乘
        
        Args:
            n: 非负整数
            
        Returns:
            n! = 1 * 2 * ... * n
            
        Example:
            >>> calc.factorial(5)
            120
        """
        return self._get_factorial(n)
    
    def permutation(self, n: int, k: int) -> int:
        """
        计算排列数 P(n, k) = n! / (n-k)!
        
        Args:
            n: 总元素数
            k: 选取元素数
            
        Returns:
            从 n 个元素中选取 k 个的排列数
            
        Example:
            >>> calc.permutation(5, 3)
            60  # 5! / 2! = 120 / 2 = 60
        """
        if n < 0 or k < 0:
            raise ValueError("参数必须为非负整数")
        if k > n:
            return 0
        
        # 使用缓存（使用排列专用缓存）
        key = (n, k)
        if self.use_cache and key in self._permutation_cache:
            return self._permutation_cache[key]
        
        # 优化计算：避免大数阶乘
        # P(n, k) = n * (n-1) * ... * (n-k+1)
        result = 1
        for i in range(n - k + 1, n + 1):
            result *= i
        
        if self.use_cache and len(self._permutation_cache) < self.cache_size:
            self._permutation_cache[key] = result
        
        return result
    
    def combination(self, n: int, k: int) -> int:
        """
        计算组合数 C(n, k) = n! / (k! * (n-k)!)
        
        Args:
            n: 总元素数
            k: 选取元素数
            
        Returns:
            从 n 个元素中选取 k 个的组合数
            
        Example:
            >>> calc.combination(5, 3)
            10  # 5! / (3! * 2!) = 120 / 12 = 10
        """
        if n < 0 or k < 0:
            raise ValueError("参数必须为非负整数")
        if k > n:
            return 0
        if k == 0 or k == n:
            return 1
        
        # 优化：利用 C(n, k) = C(n, n-k)
        k = min(k, n - k)
        
        # 使用缓存
        key = (n, k)
        if self.use_cache and key in self._combination_cache:
            return self._combination_cache[key]
        
        # 优化计算：避免阶乘溢出
        # C(n, k) = n * (n-1) * ... * (n-k+1) / (k * (k-1) * ... * 1)
        # 使用交替乘除来避免中间结果过大
        result = 1
        for i in range(k):
            result = result * (n - i) // (i + 1)
        
        if self.use_cache and len(self._combination_cache) < self.cache_size:
            self._combination_cache[key] = result
        
        return result
    
    def multinomial(self, *ks: int) -> int:
        """
        计算多重组合数 / 多项式系数
        
        (k1 + k2 + ... + km)! / (k1! * k2! * ... * km!)
        
        Args:
            ks: 各部分的大小
            
        Returns:
            多重组合数
            
        Example:
            >>> calc.multinomial(2, 3, 1)
            60  # 6! / (2! * 3! * 1!) = 720 / 12 = 60
        """
        total = sum(ks)
        result = self._get_factorial(total)
        
        for k in ks:
            result //= self._get_factorial(k)
        
        return result
    
    def clear_cache(self) -> None:
        """清空缓存"""
        self._factorial_cache = {0: 1, 1: 1}
        self._combination_cache = {}
        self._permutation_cache = {}


class PermutationGenerator(Generic[T]):
    """
    排列生成器
    
    生成各种排列和组合。
    
    Example:
        >>> gen = PermutationGenerator()
        >>> gen.generate_permutations([1, 2, 3])
        [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
        >>> gen.generate_combinations([1, 2, 3, 4], 2)
        [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
    """
    
    def generate_permutations(self, items: List[T]) -> List[List[T]]:
        """
        生成全排列
        
        Args:
            items: 元素列表
            
        Returns:
            所有排列的列表
            
        Example:
            >>> gen.generate_permutations([1, 2, 3])
            [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
        """
        return [list(p) for p in permutations(items)]
    
    def iter_permutations(self, items: List[T]) -> Iterator[List[T]]:
        """
        迭代生成全排列（节省内存）
        
        Args:
            items: 元素列表
            
        Yields:
            每个排列
        """
        for p in permutations(items):
            yield list(p)
    
    def generate_k_permutations(self, items: List[T], k: int) -> List[List[T]]:
        """
        生成 k-排列（从 n 个元素中选取 k 个的排列）
        
        Args:
            items: 元素列表
            k: 选取数量
            
        Returns:
            所有 k-排列
            
        Example:
            >>> gen.generate_k_permutations([1, 2, 3, 4], 2)
            [[1, 2], [1, 3], ..., [4, 3]]
        """
        return [list(p) for p in permutations(items, k)]
    
    def iter_k_permutations(self, items: List[T], k: int) -> Iterator[List[T]]:
        """
        迭代生成 k-排列
        
        Args:
            items: 元素列表
            k: 选取数量
            
        Yields:
            每个 k-排列
        """
        for p in permutations(items, k):
            yield list(p)
    
    def generate_combinations(self, items: List[T], k: int) -> List[List[T]]:
        """
        生成 k-组合
        
        Args:
            items: 元素列表
            k: 选取数量
            
        Returns:
            所有 k-组合
            
        Example:
            >>> gen.generate_combinations([1, 2, 3, 4], 2)
            [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
        """
        return [list(c) for c in combinations(items, k)]
    
    def iter_combinations(self, items: List[T], k: int) -> Iterator[List[T]]:
        """
        迭代生成 k-组合
        
        Args:
            items: 元素列表
            k: 选取数量
            
        Yields:
            每个 k-组合
        """
        for c in combinations(items, k):
            yield list(c)
    
    def generate_all_combinations(self, items: List[T]) -> List[List[T]]:
        """
        生成所有组合（所有可能的 k-组合）
        
        Args:
            items: 元素列表
            
        Returns:
            所有的组合（包括空组合）
        """
        result = [[]]  # 空组合
        n = len(items)
        
        for k in range(1, n + 1):
            result.extend(self.generate_combinations(items, k))
        
        return result
    
    def generate_powerset(self, items: List[T]) -> List[List[T]]:
        """
        生成幂集（所有子集）
        
        Args:
            items: 元素列表
            
        Returns:
            所有子集
            
        Example:
            >>> gen.generate_powerset([1, 2])
            [[]], [1], [2], [1, 2]]
        """
        n = len(items)
        result = []
        
        # 使用位运算生成
        for i in range(2 ** n):
            subset = []
            for j in range(n):
                if i & (1 << j):
                    subset.append(items[j])
            result.append(subset)
        
        return result
    
    def iter_powerset(self, items: List[T]) -> Iterator[List[T]]:
        """
        迭代生成幂集
        
        Args:
            items: 元素列表
            
        Yields:
            每个子集
        """
        n = len(items)
        for i in range(2 ** n):
            subset = []
            for j in range(n):
                if i & (1 << j):
                    subset.append(items[j])
            yield subset
    
    def count_powerset(self, n: int) -> int:
        """
        计算幂集大小
        
        Args:
            n: 元素数量
            
        Returns:
            2^n
        """
        return 2 ** n
    
    def generate_permutations_with_repetition(
        self, 
        items: List[T], 
        k: int,
    ) -> List[List[T]]:
        """
        生成有重复的排列（每个元素可以被多次选取）
        
        Args:
            items: 元素列表
            k: 选取数量
            
        Returns:
            所有有重复的排列
            
        Example:
            >>> gen.generate_permutations_with_repetition([1, 2], 2)
            [[1, 1], [1, 2], [2, 1], [2, 2]]
        """
        if k == 0:
            return [[]]
        
        result = []
        n = len(items)
        
        # 递归生成
        for i in range(n ** k):
            perm = []
            temp = i
            for _ in range(k):
                perm.append(items[temp % n])
                temp //= n
            perm.reverse()
            result.append(perm)
        
        return result
    
    def iter_permutations_with_repetition(
        self, 
        items: List[T], 
        k: int,
    ) -> Iterator[List[T]]:
        """
        迭代生成有重复的排列
        
        Args:
            items: 元素列表
            k: 选取数量
            
        Yields:
            每个有重复的排列
        """
        if k == 0:
            yield []
            return
        
        n = len(items)
        for i in range(n ** k):
            perm = []
            temp = i
            for _ in range(k):
                perm.append(items[temp % n])
                temp //= n
            perm.reverse()
            yield perm
    
    def generate_combinations_with_repetition(
        self, 
        items: List[T], 
        k: int,
    ) -> List[List[T]]:
        """
        生成有重复的组合（每个元素可以被多次选取，但结果有序）
        
        Args:
            items: 元素列表
            k: 选取数量
            
        Returns:
            所有有重复的组合
            
        Example:
            >>> gen.generate_combinations_with_repetition([1, 2], 2)
            [[1, 1], [1, 2], [2, 2]]
        """
        if k == 0:
            return [[]]
        
        n = len(items)
        result = []
        
        # 递归生成
        def generate(start: int, current: List[T]):
            if len(current) == k:
                result.append(current.copy())
                return
            
            for i in range(start, n):
                current.append(items[i])
                generate(i, current)
                current.pop()
        
        generate(0, [])
        return result
    
    def iter_combinations_with_repetition(
        self, 
        items: List[T], 
        k: int,
    ) -> Iterator[List[T]]:
        """
        迭代生成有重复的组合
        
        Args:
            items: 元素列表
            k: 选取数量
            
        Yields:
            每个有重复的组合
        """
        if k == 0:
            yield []
            return
        
        n = len(items)
        
        def generate(start: int, current: List[T]):
            if len(current) == k:
                yield current.copy()
                return
            
            for i in range(start, n):
                current.append(items[i])
                yield from generate(i, current)
                current.pop()
        
        yield from generate(0, [])


class CantorEncoder:
    """
    康托编码
    
    将排列映射到唯一索引，支持双向转换。
    
    康托展开：排列 -> 索引
    康托逆展开：索引 -> 排列
    
    Example:
        >>> encoder = CantorEncoder()
        >>> encoder.encode([1, 2, 3])  # 第一个排列
        0
        >>> encoder.encode([3, 2, 1])  # 最后一个排列
        5
        >>> encoder.decode(0, [1, 2, 3])
        [1, 2, 3]
    """
    
    def __init__(self, use_cache: bool = True):
        """
        初始化编码器
        
        Args:
            use_cache: 是否使用缓存
        """
        self.use_cache = use_cache
        self._calculator = CombinationCalculator(use_cache=use_cache)
    
    def encode(self, permutation: List[int]) -> int:
        """
        康托展开：排列转索引
        
        Args:
            permutation: 排列（元素为 0 到 n-1 或任意可排序元素）
            
        Returns:
            排列的唯一索引（0 到 n!-1）
            
        Example:
            >>> encoder.encode([0, 1, 2])  # 第一个排列
            0
            >>> encoder.encode([2, 1, 0])  # 最后一个排列（3! - 1 = 5）
            5
        """
        n = len(permutation)
        if n == 0:
            return 0
        
        # 创建排序后的元素列表
        sorted_items = sorted(permutation)
        visited = [False] * n
        
        index = 0
        
        for i in range(n):
            # 找到当前元素在排序列表中的位置
            current = permutation[i]
            pos = sorted_items.index(current)
            
            # 计算比当前元素小且未被访问的元素数量
            count = 0
            for j in range(pos):
                if not visited[j]:
                    count += 1
            
            visited[pos] = True
            
            # 康托展开公式
            remaining = n - i - 1
            index += count * self._calculator.factorial(remaining)
        
        return index
    
    def decode(self, index: int, elements: Optional[List[int]] = None) -> List[int]:
        """
        康托逆展开：索引转排列
        
        Args:
            index: 排列索引（0 到 n!-1）
            elements: 元素列表（可选，默认为 0 到 n-1）
            
        Returns:
            对应的排列
            
        Example:
            >>> encoder.decode(0, n=3)  # n 是隐式的
            [0, 1, 2]
        """
        if elements is None:
            raise ValueError("需要提供元素列表")
        
        n = len(elements)
        if n == 0:
            return []
        
        max_index = self._calculator.factorial(n) - 1
        if index < 0 or index > max_index:
            raise ValueError(f"索引必须在 0 到 {max_index} 之间")
        
        # 复制元素列表
        available = sorted(elements)
        result = []
        
        remaining_index = index
        
        for i in range(n):
            remaining = n - i - 1
            fact = self._calculator.factorial(remaining)
            
            # 计算当前位置的元素索引
            pos = remaining_index // fact
            remaining_index = remaining_index % fact
            
            # 选择元素
            result.append(available[pos])
            available.pop(pos)
        
        return result
    
    def encode_with_elements(self, permutation: List[T], elements: List[T]) -> int:
        """
        对任意元素排列进行康托编码
        
        Args:
            permutation: 排列
            elements: 原始元素列表
            
        Returns:
            排列索引
        """
        # 将元素映射到整数
        sorted_elements = sorted(elements)
        int_permutation = [sorted_elements.index(x) for x in permutation]
        
        return self.encode(int_permutation)
    
    def decode_with_elements(self, index: int, elements: List[T]) -> List[T]:
        """
        从索引解码任意元素的排列
        
        Args:
            index: 排列索引
            elements: 原始元素列表
            
        Returns:
            对应的排列
        """
        sorted_elements = sorted(elements)
        int_permutation = self.decode(index, list(range(len(elements))))
        
        return [sorted_elements[i] for i in int_permutation]


class SpecialNumbers:
    """
    特殊数计算
    
    计算卡特兰数、斯特林数、贝尔数等。
    
    Example:
        >>> special = SpecialNumbers()
        >>> special.catalan(5)
        42
        >>> special.stirling_second(5, 3)
        25
        >>> special.bell(5)
        52
    """
    
    def __init__(self, use_cache: bool = True):
        """
        初始化
        
        Args:
            use_cache: 是否使用缓存
        """
        self.use_cache = use_cache
        self._catalan_cache: dict[int, int] = {0: 1, 1: 1}
        self._stirling_first_cache: dict[Tuple[int, int], int] = {}
        self._stirling_second_cache: dict[Tuple[int, int], int] = {}
        self._bell_cache: dict[int, int] = {0: 1}
        self._calculator = CombinationCalculator(use_cache=use_cache)
    
    def catalan(self, n: int) -> int:
        """
        计算第 n 个卡特兰数
        
        Catalan(n) = C(2n, n) / (n + 1)
        
        应用场景：
        - 有效括号序列数量
        - 二叉树形态数量
        - 出栈序列数量
        
        Args:
            n: 卡特兰数序号
            
        Returns:
            Catalan(n)
            
        Example:
            >>> special.catalan(0)
            1
            >>> special.catalan(1)
            1
            >>> special.catalan(2)
            2
            >>> special.catalan(3)
            5
        """
        if n < 0:
            raise ValueError("卡特兰数序号必须为非负整数")
        
        if self.use_cache and n in self._catalan_cache:
            return self._catalan_cache[n]
        
        # 使用公式：C(2n, n) / (n + 1)
        # 但使用递推公式避免大数：C(n) = C(n-1) * 2(2n-1) / (n+1)
        result = self._catalan_cache.get(max(self._catalan_cache.keys()))
        start = max(self._catalan_cache.keys())
        
        for i in range(start + 1, n + 1):
            result = result * 2 * (2 * i - 1) // (i + 1)
            if self.use_cache:
                self._catalan_cache[i] = result
        
        return result
    
    def stirling_first(self, n: int, k: int) -> int:
        """
        计算第一类斯特林数 S(n, k)
        
        第一类斯特林数：将 n 个元素排成 k 个圆排列的方案数
        
        Args:
            n: 元素数
            k: 圆排列数
            
        Returns:
            S(n, k)
            
        Example:
            >>> special.stirling_first(4, 2)
            11
        """
        if n < 0 or k < 0:
            raise ValueError("参数必须为非负整数")
        if k > n:
            return 0
        if k == 0:
            return 0 if n > 0 else 1
        if k == n:
            return 1
        
        key = (n, k)
        if self.use_cache and key in self._stirling_first_cache:
            return self._stirling_first_cache[key]
        
        # 使用递推公式：S(n, k) = S(n-1, k-1) + (n-1) * S(n-1, k)
        # 递归计算（可以优化为迭代）
        result = self.stirling_first(n - 1, k - 1) + (n - 1) * self.stirling_first(n - 1, k)
        
        if self.use_cache:
            self._stirling_first_cache[key] = result
        
        return result
    
    def stirling_second(self, n: int, k: int) -> int:
        """
        计算第二类斯特林数 S(n, k)
        
        第二类斯特林数：将 n 个元素分成 k 个非空集合的方案数
        
        Args:
            n: 元素数
            k: 集合数
            
        Returns:
            S(n, k)
            
        Example:
            >>> special.stirling_second(4, 2)
            7
        """
        if n < 0 or k < 0:
            raise ValueError("参数必须为非负整数")
        if k > n:
            return 0
        if k == 0:
            return 0 if n > 0 else 1
        if k == 1:
            return 1
        if k == n:
            return 1
        
        key = (n, k)
        if self.use_cache and key in self._stirling_second_cache:
            return self._stirling_second_cache[key]
        
        # 使用递推公式：S(n, k) = S(n-1, k-1) + k * S(n-1, k)
        result = self.stirling_second(n - 1, k - 1) + k * self.stirling_second(n - 1, k)
        
        if self.use_cache:
            self._stirling_second_cache[key] = result
        
        return result
    
    def bell(self, n: int) -> int:
        """
        计算第 n 个贝尔数
        
        贝尔数：将 n 个元素分成任意非空集合的方案数总和
        
        B(n) = S(n, 0) + S(n, 1) + ... + S(n, n)
        
        Args:
            n: 贝尔数序号
            
        Returns:
            B(n)
            
        Example:
            >>> special.bell(0)
            1
            >>> special.bell(3)
            5
            >>> special.bell(5)
            52
        """
        if n < 0:
            raise ValueError("贝尔数序号必须为非负整数")
        
        if self.use_cache and n in self._bell_cache:
            return self._bell_cache[n]
        
        # B(n) = sum(S(n, k) for k in 0..n)
        result = sum(self.stirling_second(n, k) for k in range(n + 1))
        
        if self.use_cache:
            self._bell_cache[n] = result
        
        return result
    
    def derangement(self, n: int) -> int:
        """
        计算错位排列数
        
        错位排列：所有元素都不在原位置的排列数
        
        D(n) = n! * (1 - 1/1! + 1/2! - 1/3! + ... + (-1)^n * 1/n!)
        
        Args:
            n: 元素数
            
        Returns:
            错位排列数
            
        Example:
            >>> special.derangement(4)
            9
        """
        if n < 0:
            raise ValueError("元素数必须为非负整数")
        if n == 0:
            return 1
        if n == 1:
            return 0
        
        # 使用递推：D(n) = (n-1) * (D(n-1) + D(n-2))
        d = [1, 0]  # D(0), D(1)
        
        for i in range(2, n + 1):
            d.append((i - 1) * (d[i - 1] + d[i - 2]))
        
        return d[n]
    
    def clear_cache(self) -> None:
        """清空缓存"""
        self._catalan_cache = {0: 1, 1: 1}
        self._stirling_first_cache = {}
        self._stirling_second_cache = {}
        self._bell_cache = {0: 1}


class CombinationUtils:
    """
    组合数学工具高级接口
    
    提供简化的静态方法和工厂方法。
    """
    
    _calculator: CombinationCalculator = CombinationCalculator()
    _generator: PermutationGenerator = PermutationGenerator()
    _encoder: CantorEncoder = CantorEncoder()
    _special: SpecialNumbers = SpecialNumbers()
    
    @staticmethod
    def C(n: int, k: int) -> int:
        """组合数 C(n, k)"""
        return CombinationUtils._calculator.combination(n, k)
    
    @staticmethod
    def P(n: int, k: int) -> int:
        """排列数 P(n, k)"""
        return CombinationUtils._calculator.permutation(n, k)
    
    @staticmethod
    def factorial(n: int) -> int:
        """阶乘 n!"""
        return CombinationUtils._calculator.factorial(n)
    
    @staticmethod
    def permutations(items: List[T]) -> List[List[T]]:
        """生成全排列"""
        return CombinationUtils._generator.generate_permutations(items)
    
    @staticmethod
    def combinations(items: List[T], k: int) -> List[List[T]]:
        """生成 k-组合"""
        return CombinationUtils._generator.generate_combinations(items, k)
    
    @staticmethod
    def powerset(items: List[T]) -> List[List[T]]:
        """生成幂集"""
        return CombinationUtils._generator.generate_powerset(items)
    
    @staticmethod
    def catalan(n: int) -> int:
        """卡特兰数"""
        return CombinationUtils._special.catalan(n)
    
    @staticmethod
    def stirling(n: int, k: int, kind: int = 2) -> int:
        """
        斯特林数
        
        Args:
            n: 元素数
            k: 分组数
            kind: 1 或 2（第一类或第二类）
        """
        if kind == 1:
            return CombinationUtils._special.stirling_first(n, k)
        else:
            return CombinationUtils._special.stirling_second(n, k)
    
    @staticmethod
    def bell(n: int) -> int:
        """贝尔数"""
        return CombinationUtils._special.bell(n)
    
    @staticmethod
    def derangement(n: int) -> int:
        """错位排列数"""
        return CombinationUtils._special.derangement(n)


# 便捷函数
def C(n: int, k: int) -> int:
    """组合数便捷函数"""
    return CombinationUtils.C(n, k)


def P(n: int, k: int) -> int:
    """排列数便捷函数"""
    return CombinationUtils.P(n, k)


def factorial(n: int) -> int:
    """阶乘便捷函数"""
    return CombinationUtils.factorial(n)


def catalan(n: int) -> int:
    """卡特兰数便捷函数"""
    return CombinationUtils.catalan(n)


def generate_permutations(items: List[T]) -> List[List[T]]:
    """生成排列便捷函数"""
    return CombinationUtils.permutations(items)


def generate_combinations(items: List[T], k: int) -> List[List[T]]:
    """生成组合便捷函数"""
    return CombinationUtils.combinations(items, k)


def generate_powerset(items: List[T]) -> List[List[T]]:
    """生成幂集便捷函数"""
    return CombinationUtils.powerset(items)


if __name__ == "__main__":
    # 简单演示
    print("=== 组合数学工具演示 ===")
    
    # 1. 组合数和排列数
    print("\n--- 组合数和排列数 ---")
    print(f"C(10, 3) = {C(10, 3)}")
    print(f"P(10, 3) = {P(10, 3)}")
    print(f"5! = {factorial(5)}")
    
    # 2. 排列生成
    print("\n--- 排列生成 ---")
    perms = generate_permutations([1, 2, 3])
    print(f"[1, 2, 3] 的所有排列: {perms}")
    
    # 3. 组合生成
    print("\n--- 组合生成 ---")
    combs = generate_combinations([1, 2, 3, 4], 2)
    print(f"[1, 2, 3, 4] 的 2-组合: {combs}")
    
    # 4. 幂集
    print("\n--- 幂集 ---")
    power = generate_powerset([1, 2])
    print(f"[1, 2] 的幂集: {power}")
    
    # 5. 卡特兰数
    print("\n--- 卡特兰数 ---")
    for i in range(10):
        print(f"Catalan({i}) = {catalan(i)}")
    
    # 6. 康托编码
    print("\n--- 康托编码 ---")
    encoder = CantorEncoder()
    perm = [0, 1, 2]
    idx = encoder.encode(perm)
    print(f"排列 {perm} 的索引: {idx}")
    
    decoded = encoder.decode(idx, [0, 1, 2])
    print(f"索引 {idx} 解码为: {decoded}")
    
    # 7. 特殊数
    print("\n--- 特殊数 ---")
    special = SpecialNumbers()
    print(f"斯特林数 S(5, 3) = {special.stirling_second(5, 3)}")
    print(f"贝尔数 B(5) = {special.bell(5)}")
    print(f"错位排列 D(4) = {special.derangement(4)}")