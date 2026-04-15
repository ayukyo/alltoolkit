"""
Combinatorics Utils - 组合数学工具集

提供完整的组合数学函数和生成器，包括：
- 排列（Permutations）
- 组合（Combinations）
- 笛卡尔积（Cartesian Product）
- 幂集（Power Set）
- 二项式系数（Binomial Coefficients）
- 阶乘（Factorial）
- 斯特林数（Stirling Numbers）
- 卡塔兰数（Catalan Numbers）
- 分拆数（Partition Numbers）
- 抽屉原理解析

零依赖，纯 Python 标准库实现。
支持大整数运算，内存高效生成器实现。
"""

from typing import (
    List, Tuple, Iterator, Iterable, Optional, 
    Callable, TypeVar, Generic, Union, Any
)
from functools import lru_cache, reduce
from math import gcd
from operator import mul
import itertools

T = TypeVar('T')


# ============================================================================
# 基础计算函数
# ============================================================================

def factorial(n: int) -> int:
    """
    计算阶乘 n!
    
    Args:
        n: 非负整数
        
    Returns:
        n 的阶乘
        
    Raises:
        ValueError: 如果 n 为负数
        
    Examples:
        >>> factorial(5)
        120
        >>> factorial(0)
        1
    """
    if n < 0:
        raise ValueError("阶乘只支持非负整数")
    if n <= 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def factorial_range(n: int, k: int) -> int:
    """
    计算下降阶乘 n! / (n-k)! = n * (n-1) * ... * (n-k+1)
    
    Args:
        n: 上界
        k: 项数
        
    Returns:
        下降阶乘值
    """
    if k > n:
        return 0
    if k <= 0:
        return 1
    result = 1
    for i in range(n, n - k, -1):
        result *= i
    return result


@lru_cache(maxsize=1024)
def binomial(n: int, k: int) -> int:
    """
    计算二项式系数 C(n, k) = n! / (k! * (n-k)!)
    
    使用动态规划优化，支持大整数。
    
    Args:
        n: 总数
        k: 选取数
        
    Returns:
        组合数 C(n, k)
        
    Examples:
        >>> binomial(5, 2)
        10
        >>> binomial(10, 5)
        252
    """
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    # 利用对称性减少计算
    if k > n - k:
        k = n - k
    # 使用乘法公式避免大数阶乘
    result = 1
    for i in range(k):
        result = result * (n - i) // (i + 1)
    return result


def multinomial(*counts: int) -> int:
    """
    计算多项式系数
    
    多项式系数 = n! / (k1! * k2! * ... * km!)
    其中 n = k1 + k2 + ... + km
    
    Args:
        counts: 各组的元素数量
        
    Returns:
        多项式系数
        
    Examples:
        >>> multinomial(3, 2, 1)  # 6! / (3! * 2! * 1!)
        60
    """
    total = sum(counts)
    result = factorial(total)
    for c in counts:
        result //= factorial(c)
    return result


# ============================================================================
# 排列生成器
# ============================================================================

def permutations(
    iterable: Iterable[T],
    r: Optional[int] = None
) -> Iterator[Tuple[T, ...]]:
    """
    生成排列（按字典序）
    
    Args:
        iterable: 可迭代对象
        r: 排列长度，默认为全长
        
    Yields:
        排列元组
        
    Examples:
        >>> list(permutations([1, 2, 3], 2))
        [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]
    """
    return itertools.permutations(iterable, r)


def permutations_count(n: int, r: int) -> int:
    """
    计算排列数 P(n, r) = n! / (n-r)!
    
    Args:
        n: 元素总数
        r: 排列长度
        
    Returns:
        排列数
    """
    if r > n:
        return 0
    return factorial_range(n, r)


def permutations_with_replacement(
    iterable: Iterable[T],
    r: int
) -> Iterator[Tuple[T, ...]]:
    """
    生成可重复排列（有序，元素可重复使用）
    
    长度为 r 的 n^r 种排列。
    
    Args:
        iterable: 可迭代对象
        r: 排列长度
        
    Yields:
        排列元组
        
    Examples:
        >>> list(permutations_with_replacement([1, 2], 2))
        [(1, 1), (1, 2), (2, 1), (2, 2)]
    """
    return itertools.product(iterable, repeat=r)


# ============================================================================
# 组合生成器
# ============================================================================

def combinations(
    iterable: Iterable[T],
    r: int
) -> Iterator[Tuple[T, ...]]:
    """
    生成组合（按字典序）
    
    Args:
        iterable: 可迭代对象
        r: 组合长度
        
    Yields:
        组合元组
        
    Examples:
        >>> list(combinations([1, 2, 3, 4], 2))
        [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
    """
    return itertools.combinations(iterable, r)


def combinations_count(n: int, r: int) -> int:
    """
    计算组合数 C(n, r) = n! / (r! * (n-r)!)
    
    Args:
        n: 元素总数
        r: 组合长度
        
    Returns:
        组合数
    """
    return binomial(n, r)


def combinations_with_replacement(
    iterable: Iterable[T],
    r: int
) -> Iterator[Tuple[T, ...]]:
    """
    生成可重复组合（无序，元素可重复使用）
    
    Args:
        iterable: 可迭代对象
        r: 组合长度
        
    Yields:
        组合元组
        
    Examples:
        >>> list(combinations_with_replacement([1, 2], 3))
        [(1, 1, 1), (1, 1, 2), (1, 2, 2), (2, 2, 2)]
    """
    return itertools.combinations_with_replacement(iterable, r)


def combinations_with_replacement_count(n: int, r: int) -> int:
    """
    计算可重复组合数 C(n+r-1, r)
    
    Args:
        n: 元素种类数
        r: 组合长度
        
    Returns:
        可重复组合数
    """
    return binomial(n + r - 1, r)


# ============================================================================
# 笛卡尔积
# ============================================================================

def cartesian_product(*iterables: Iterable[T], repeat: int = 1) -> Iterator[Tuple[T, ...]]:
    """
    生成笛卡尔积
    
    Args:
        *iterables: 多个可迭代对象
        repeat: 重复次数
        
    Yields:
        笛卡尔积元组
        
    Examples:
        >>> list(cartesian_product([1, 2], ['a', 'b']))
        [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]
    """
    return itertools.product(*iterables, repeat=repeat)


def cartesian_product_count(*sizes: int, repeat: int = 1) -> int:
    """
    计算笛卡尔积数量
    
    Args:
        *sizes: 各集合的大小
        repeat: 重复次数
        
    Returns:
        笛卡尔积数量
    """
    if repeat > 1:
        sizes = sizes * repeat
    if not sizes:
        return 1
    return reduce(mul, sizes, 1)


# ============================================================================
# 幂集
# ============================================================================

def powerset(iterable: Iterable[T]) -> Iterator[Tuple[T, ...]]:
    """
    生成幂集（所有子集）
    
    包括空集和全集，共 2^n 个子集。
    
    Args:
        iterable: 可迭代对象
        
    Yields:
        子集元组
        
    Examples:
        >>> list(powerset([1, 2]))
        [(), (1,), (2,), (1, 2)]
    """
    s = list(iterable)
    return itertools.chain.from_iterable(
        itertools.combinations(s, r) for r in range(len(s) + 1)
    )


def powerset_count(n: int) -> int:
    """
    计算幂集大小 2^n
    
    Args:
        n: 元素数量
        
    Returns:
        幂集大小
    """
    return 1 << n  # 2^n，使用位运算


def subsets_of_size(iterable: Iterable[T], size: int) -> Iterator[Tuple[T, ...]]:
    """
    生成指定大小的所有子集
    
    Args:
        iterable: 可迭代对象
        size: 子集大小
        
    Yields:
        子集元组
    """
    return itertools.combinations(iterable, size)


# ============================================================================
# 特殊数列
# ============================================================================

@lru_cache(maxsize=256)
def catalan(n: int) -> int:
    """
    计算第 n 个卡塔兰数
    
    C_n = (2n)! / ((n+1)! * n!) = C(2n, n) / (n+1)
    
    应用场景：
    - 合法括号序列数量
    - 二叉树形态数量
    - 出栈序列数量
    
    Args:
        n: 卡塔兰数索引
        
    Returns:
        第 n 个卡塔兰数
        
    Examples:
        >>> [catalan(i) for i in range(6)]
        [1, 1, 2, 5, 14, 42]
    """
    if n < 0:
        raise ValueError("卡塔兰数只支持非负整数")
    if n <= 1:
        return 1
    # 使用递推公式: C_n = C_(n-1) * 2(2n-1) / (n+1)
    result = 1
    for i in range(1, n + 1):
        result = result * 2 * (2 * i - 1) // (i + 1)
    return result


@lru_cache(maxsize=256)
def stirling_first(n: int, k: int) -> int:
    """
    计算第一类斯特林数 s(n, k)
    
    将 n 个元素分成 k 个非空轮换的方法数。
    
    递推关系：s(n, k) = s(n-1, k-1) + (n-1) * s(n-1, k)
    
    Args:
        n: 元素数量
        k: 轮换数量
        
    Returns:
        第一类斯特林数
    """
    if n < 0 or k < 0:
        raise ValueError("斯特林数只支持非负整数")
    if k > n:
        return 0
    if n == k == 0:
        return 1
    if k == 0:
        return 0
    if n == k:
        return 1
    if k == 1:
        return factorial(n - 1)
    return stirling_first(n - 1, k - 1) + (n - 1) * stirling_first(n - 1, k)


@lru_cache(maxsize=256)
def stirling_second(n: int, k: int) -> int:
    """
    计算第二类斯特林数 S(n, k)
    
    将 n 个元素分成 k 个非空子集的方法数。
    
    递推关系：S(n, k) = S(n-1, k-1) + k * S(n-1, k)
    
    Args:
        n: 元素数量
        k: 子集数量
        
    Returns:
        第二类斯特林数
        
    Examples:
        >>> stirling_second(4, 2)
        7
    """
    if n < 0 or k < 0:
        raise ValueError("斯特林数只支持非负整数")
    if k > n:
        return 0
    if n == k == 0:
        return 1
    if k == 0:
        return 0
    if n == k:
        return 1
    if k == 1:
        return 1
    return stirling_second(n - 1, k - 1) + k * stirling_second(n - 1, k)


@lru_cache(maxsize=256)
def bell_number(n: int) -> int:
    """
    计算第 n 个贝尔数
    
    贝尔数是将 n 个元素分成非空子集的总方法数。
    B_n = sum(S(n, k) for k in 0..n)
    
    Args:
        n: 元素数量
        
    Returns:
        第 n 个贝尔数
        
    Examples:
        >>> [bell_number(i) for i in range(6)]
        [1, 1, 2, 5, 15, 52]
    """
    if n < 0:
        raise ValueError("贝尔数只支持非负整数")
    return sum(stirling_second(n, k) for k in range(n + 1))


@lru_cache(maxsize=256)
def partition_number(n: int) -> int:
    """
    计算整数分拆数 p(n)
    
    将 n 分拆成正整数之和的方法数（顺序不重要）。
    
    使用欧拉五角数定理计算。
    
    Args:
        n: 要分拆的整数
        
    Returns:
        分拆数
        
    Examples:
        >>> [partition_number(i) for i in range(6)]
        [1, 1, 2, 3, 5, 7]
    """
    if n < 0:
        raise ValueError("分拆数只支持非负整数")
    if n <= 1:
        return 1
    
    # 使用动态规划
    partitions = [0] * (n + 1)
    partitions[0] = 1
    
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            partitions[j] += partitions[j - i]
    
    return partitions[n]


def partitions(n: int) -> Iterator[List[int]]:
    """
    生成整数的所有分拆
    
    Args:
        n: 要分拆的整数
        
    Yields:
        分拆列表（按降序排列）
        
    Examples:
        >>> list(partitions(4))
        [[4], [3, 1], [2, 2], [2, 1, 1], [1, 1, 1, 1]]
    """
    def _partitions(n: int, max_val: int) -> Iterator[List[int]]:
        if n == 0:
            yield []
            return
        for i in range(min(n, max_val), 0, -1):
            for p in _partitions(n - i, i):
                yield [i] + p
    
    yield from _partitions(n, n)


# ============================================================================
# 抽屉原理
# ============================================================================

def pigeonhole_count(items: int, boxes: int) -> int:
    """
    计算抽屉原理保证的最小重叠
    
    根据抽屉原理，将 items 个物品放入 boxes 个盒子，
    至少有一个盒子中有 ceil(items/boxes) 个物品。
    
    Args:
        items: 物品数量
        boxes: 盒子数量
        
    Returns:
        至少有一个盒子中的物品数量
        
    Examples:
        >>> pigeonhole_count(13, 12)
        2
    """
    return (items + boxes - 1) // boxes


def pigeonhole_min_max(items: int, boxes: int) -> Tuple[int, int]:
    """
    计算抽屉原理的范围
    
    将 items 个物品放入 boxes 个盒子，
    最少和最多盒子中的物品数量范围。
    
    Args:
        items: 物品数量
        boxes: 盒子数量
        
    Returns:
        (最少盒子物品数, 至少一个盒子的物品数)
    """
    min_count = items // boxes
    max_count = pigeonhole_count(items, boxes)
    return (min_count, max_count)


# ============================================================================
# 鸽巢原理验证
# ============================================================================

def check_pigeonhole_violation(
    items: List[T],
    boxes: int,
    max_per_box: int
) -> bool:
    """
    检查是否存在抽屉原理冲突
    
    Args:
        items: 物品列表
        boxes: 盒子数量
        max_per_box: 每个盒子最大容量
        
    Returns:
        True 如果存在冲突（无法满足条件）
    """
    return len(items) > boxes * max_per_box


# ============================================================================
# 组合搜索辅助
# ============================================================================

def nth_combination(
    iterable: Iterable[T],
    r: int,
    index: int
) -> Tuple[T, ...]:
    """
    获取第 index 个组合（按字典序，0-indexed）
    
    用于大规模组合的直接访问，无需生成前面所有组合。
    
    Args:
        iterable: 可迭代对象
        r: 组合长度
        index: 组合索引
        
    Returns:
        第 index 个组合
        
    Raises:
        IndexError: 如果 index 超出范围
        
    Examples:
        >>> nth_combination([1, 2, 3, 4, 5], 3, 0)
        (1, 2, 3)
        >>> nth_combination([1, 2, 3, 4, 5], 3, 5)
        (1, 4, 5)
    """
    pool = tuple(iterable)
    n = len(pool)
    
    if r < 0 or r > n:
        raise ValueError(f"r must be in range [0, {n}]")
    
    total = binomial(n, r)
    if index < 0 or index >= total:
        raise IndexError(f"index must be in range [0, {total})")
    
    if r == 0:
        return ()
    
    result = []
    current_index = index
    
    # 逐位确定元素
    start = 0
    for remaining in range(r, 0, -1):
        # 找到当前位置应该选择的元素
        for i in range(start, n - remaining + 1):
            count = binomial(n - i - 1, remaining - 1)
            if current_index < count:
                result.append(pool[i])
                start = i + 1
                break
            current_index -= count
    
    return tuple(result)


def nth_permutation(
    iterable: Iterable[T],
    r: Optional[int] = None,
    index: int = 0
) -> Tuple[T, ...]:
    """
    获取第 index 个排列（按字典序，0-indexed）
    
    Args:
        iterable: 可迭代对象
        r: 排列长度，默认为全长
        index: 排列索引
        
    Returns:
        第 index 个排列
    """
    pool = tuple(iterable)
    n = len(pool)
    
    if r is None:
        r = n
    
    if r < 0 or r > n:
        raise ValueError(f"r must be in range [0, {n}]")
    
    total = permutations_count(n, r)
    if index < 0 or index >= total:
        raise IndexError(f"index must be in range [0, {total})")
    
    if r == 0:
        return ()
    
    # 使用阶乘数系计算
    result = []
    available = list(pool)
    current_index = index
    
    for remaining in range(r, 0, -1):
        # 计算当前位置的选项
        fact = factorial(remaining - 1) if remaining > 1 else 1
        pos = current_index // fact
        current_index = current_index % fact
        result.append(available.pop(pos))
    
    return tuple(result)


def combination_index(combination: Tuple[T, ...], iterable: Iterable[T]) -> int:
    """
    计算给定组合在字典序中的索引
    
    Args:
        combination: 组合元组
        iterable: 原始可迭代对象
        
    Returns:
        组合的索引（0-indexed）
    """
    pool = tuple(iterable)
    n = len(pool)
    r = len(combination)
    
    index = 0
    combination = tuple(sorted(combination, key=lambda x: pool.index(x) if x in pool else n))
    
    for i, elem in enumerate(combination):
        pos = pool.index(elem) if elem in pool else n
        # 计算前面跳过的组合数
        for j in range((pool.index(combination[i-1]) + 1) if i > 0 else 0, pos):
            index += binomial(n - j - 1, r - i - 1)
    
    return index


# ============================================================================
# 实用函数
# ============================================================================

def generate_random_combination(
    n: int,
    r: int,
    seed: Optional[int] = None
) -> List[int]:
    """
    生成一个随机组合
    
    使用蓄水池抽样算法，O(n) 时间复杂度。
    
    Args:
        n: 元素范围 [0, n)
        r: 组合大小
        seed: 随机种子
        
    Returns:
        随机组合（排序后）
    """
    import random
    if seed is not None:
        random.seed(seed)
    
    if r > n:
        raise ValueError(f"Cannot select {r} elements from {n}")
    
    # 蓄水池抽样
    reservoir = list(range(r))
    
    for i in range(r, n):
        j = random.randint(0, i)
        if j < r:
            reservoir[j] = i
    
    return sorted(reservoir)


def generate_random_permutation(
    n: int,
    seed: Optional[int] = None
) -> List[int]:
    """
    生成一个随机排列（Fisher-Yates 洗牌）
    
    Args:
        n: 元素范围 [0, n)
        seed: 随机种子
        
    Returns:
        随机排列
    """
    import random
    if seed is not None:
        random.seed(seed)
    
    result = list(range(n))
    for i in range(n - 1, 0, -1):
        j = random.randint(0, i)
        result[i], result[j] = result[j], result[i]
    
    return result


def count_anagrams(word: str) -> int:
    """
    计算单词的变位词数量
    
    考虑重复字母的排列数。
    
    Args:
        word: 单词字符串
        
    Returns:
        变位词数量
    """
    from collections import Counter
    counts = Counter(word)
    return multinomial(*counts.values())


def derangements(n: int) -> int:
    """
    计算错排数 D(n)
    
    错排是完全没有任何元素在原始位置的排列。
    
    使用公式：D(n) = n! * (1 - 1/1! + 1/2! - 1/3! + ... + (-1)^n/n!)
    
    Args:
        n: 元素数量
        
    Returns:
        错排数
        
    Examples:
        >>> [derangements(i) for i in range(6)]
        [1, 0, 1, 2, 9, 44]
    """
    if n < 0:
        raise ValueError("错排数只支持非负整数")
    if n == 0:
        return 1
    if n == 1:
        return 0
    
    # 使用递推: D(n) = (n-1) * (D(n-1) + D(n-2))
    d0, d1 = 1, 0
    for i in range(2, n + 1):
        d0, d1 = d1, (i - 1) * (d1 + d0)
    return d1


def permutations_with_sign(iterable: Iterable[T]) -> Iterator[Tuple[Tuple[T, ...], int]]:
    """
    生成排列及其符号
    
    符号表示排列的奇偶性：
    - +1: 偶排列
    - -1: 奇排列
    
    Args:
        iterable: 可迭代对象
        
    Yields:
        (排列元组, 符号)
    """
    pool = list(iterable)
    n = len(pool)
    
    for perm in itertools.permutations(pool):
        # 计算逆序数
        inversions = 0
        for i in range(n):
            for j in range(i + 1, n):
                if perm.index(pool[i]) > perm.index(pool[j]):
                    inversions += 1
        sign = 1 if inversions % 2 == 0 else -1
        yield (perm, sign)


def subset_sum(
    numbers: List[int],
    target: int
) -> Optional[List[int]]:
    """
    寻找子集和问题的一个解
    
    使用动态规划，时间复杂度 O(n * target)。
    
    Args:
        numbers: 数字列表
        target: 目标和
        
    Returns:
        满足条件的子集，或 None
    """
    n = len(numbers)
    
    # dp[i][j] 表示前 i 个数能否凑出和 j
    dp = [[False] * (target + 1) for _ in range(n + 1)]
    dp[0][0] = True
    
    for i in range(1, n + 1):
        for j in range(target + 1):
            dp[i][j] = dp[i - 1][j]
            if j >= numbers[i - 1] and not dp[i][j]:
                dp[i][j] = dp[i - 1][j - numbers[i - 1]]
    
    if not dp[n][target]:
        return None
    
    # 回溯找解
    result = []
    j = target
    for i in range(n, 0, -1):
        if j >= numbers[i - 1] and dp[i - 1][j - numbers[i - 1]]:
            result.append(numbers[i - 1])
            j -= numbers[i - 1]
    
    return result


# ============================================================================
# 预计算表生成
# ============================================================================

def generate_pascal_triangle(rows: int) -> List[List[int]]:
    """
    生成帕斯卡三角形
    
    Args:
        rows: 行数
        
    Returns:
        帕斯卡三角形（二维列表）
        
    Examples:
        >>> generate_pascal_triangle(5)
        [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
    """
    triangle = []
    for i in range(rows):
        row = [1] * (i + 1)
        for j in range(1, i):
            row[j] = triangle[i - 1][j - 1] + triangle[i - 1][j]
        triangle.append(row)
    return triangle


def generate_catalan_sequence(n: int) -> List[int]:
    """
    生成前 n 个卡塔兰数
    
    Args:
        n: 数量
        
    Returns:
        卡塔兰数列表
    """
    return [catalan(i) for i in range(n)]


def generate_stirling_first_table(n: int) -> List[List[int]]:
    """
    生成第一类斯特林数表
    
    Args:
        n: 最大 n 值
        
    Returns:
        斯特林数表 s[i][j] = s(i, j)
    """
    table = [[0] * (n + 1) for _ in range(n + 1)]
    table[0][0] = 1
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            table[i][j] = table[i - 1][j - 1] + (i - 1) * table[i - 1][j]
    return table


def generate_stirling_second_table(n: int) -> List[List[int]]:
    """
    生成第二类斯特林数表
    
    Args:
        n: 最大 n 值
        
    Returns:
        斯特林数表 S[i][j] = S(i, j)
    """
    table = [[0] * (n + 1) for _ in range(n + 1)]
    table[0][0] = 1
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            table[i][j] = table[i - 1][j - 1] + j * table[i - 1][j]
    return table