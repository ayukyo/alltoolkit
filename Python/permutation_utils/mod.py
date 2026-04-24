"""
Permutation Utils - 排列组合工具集

提供排列、组合的生成、计算、序号转换等功能。
零外部依赖，纯 Python 标准库实现。

功能:
- 排列生成 (全排列、部分排列)
- 组合生成 (n选k)
- 排列序号计算 (字典序转数字)
- 排列逆序计算 (数字转字典序)
- 组合序号计算
- 排列/组合迭代器 (惰性生成)
- 排列性质判断 (奇偶性、逆序对)
"""

from typing import List, Iterator, Tuple, Optional, Any
from math import factorial


class PermutationUtils:
    """排列工具类"""
    
    @staticmethod
    def permutations(elements: List[Any], k: Optional[int] = None) -> Iterator[Tuple[Any, ...]]:
        """
        生成排列
        
        Args:
            elements: 元素列表
            k: 排列长度，None表示全排列
        
        Yields:
            排列元组
        
        Examples:
            >>> list(PermutationUtils.permutations([1, 2, 3], 2))
            [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]
        """
        n = len(elements)
        if k is None:
            k = n
        if k > n:
            return
        if k == 0:
            yield ()
            return
        
        # 使用迭代算法生成排列
        indices = list(range(n))
        cycles = list(range(n, n - k, -1))
        yield tuple(elements[i] for i in indices[:k])
        
        while True:
            for i in range(k - 1, -1, -1):
                cycles[i] -= 1
                if cycles[i] == 0:
                    indices[i:] = indices[i+1:] + indices[i:i+1]
                    cycles[i] = n - i
                else:
                    j = cycles[i]
                    indices[i], indices[-j] = indices[-j], indices[i]
                    yield tuple(elements[i] for i in indices[:k])
                    break
            else:
                return
    
    @staticmethod
    def all_permutations(elements: List[Any]) -> Iterator[Tuple[Any, ...]]:
        """生成全排列（简写）"""
        return PermutationUtils.permutations(elements)
    
    @staticmethod
    def permutation_count(n: int, k: Optional[int] = None) -> int:
        """
        计算排列数 P(n, k)
        
        Args:
            n: 总元素数
            k: 排列长度，None表示全排列
        
        Returns:
            排列数
        
        Examples:
            >>> PermutationUtils.permutation_count(5, 3)
            60
            >>> PermutationUtils.permutation_count(4)
            24
        """
        if k is None:
            k = n
        if k > n or k < 0:
            return 0
        result = 1
        for i in range(n, n - k, -1):
            result *= i
        return result
    
    @staticmethod
    def permutation_rank(perm: Tuple[Any, ...], elements: Optional[List[Any]] = None) -> int:
        """
        计算排列的字典序编号（从0开始）
        
        Args:
            perm: 排列元组
            elements: 可选的元素列表（用于确定顺序），默认使用sorted(perm)
        
        Returns:
            字典序编号
        
        Examples:
            >>> PermutationUtils.permutation_rank((1, 2, 3))
            0
            >>> PermutationUtils.permutation_rank((3, 2, 1))
            5
        """
        n = len(perm)
        if elements is None:
            elements = sorted(perm)
        else:
            elements = sorted(elements)
        
        rank = 0
        remaining = list(elements)
        
        for i, elem in enumerate(perm):
            idx = remaining.index(elem)
            rank += idx * factorial(n - i - 1)
            remaining.pop(idx)
        
        return rank
    
    @staticmethod
    def permutation_unrank(rank: int, elements: List[Any]) -> Tuple[Any, ...]:
        """
        根据字典序编号生成排列
        
        Args:
            rank: 字典序编号（从0开始）
            elements: 元素列表
        
        Returns:
            排列元组
        
        Examples:
            >>> PermutationUtils.permutation_unrank(0, [1, 2, 3])
            (1, 2, 3)
            >>> PermutationUtils.permutation_unrank(5, [1, 2, 3])
            (3, 2, 1)
        """
        n = len(elements)
        remaining = list(elements)
        result = []
        
        for i in range(n):
            fact = factorial(n - i - 1)
            idx = rank // fact
            rank = rank % fact
            result.append(remaining.pop(idx))
        
        return tuple(result)
    
    @staticmethod
    def next_permutation(elements: List[Any]) -> Optional[List[Any]]:
        """
        获取字典序下一个排列（原地修改后返回）
        
        Args:
            elements: 元素列表
        
        Returns:
            下一个排列，如果已是最后一个则返回None
        
        Examples:
            >>> PermutationUtils.next_permutation([1, 2, 3])
            [1, 3, 2]
        """
        n = len(elements)
        
        # 找到第一个降序位置
        i = n - 2
        while i >= 0 and elements[i] >= elements[i + 1]:
            i -= 1
        
        if i < 0:
            return None
        
        # 找到比 elements[i] 大的最小元素
        j = n - 1
        while elements[j] <= elements[i]:
            j -= 1
        
        # 交换
        elements[i], elements[j] = elements[j], elements[i]
        
        # 反转 i+1 到末尾
        elements[i+1:] = elements[i+1:][::-1]
        
        return elements
    
    @staticmethod
    def prev_permutation(elements: List[Any]) -> Optional[List[Any]]:
        """
        获取字典序上一个排列
        
        Args:
            elements: 元素列表
        
        Returns:
            上一个排列，如果已是第一个则返回None
        
        Examples:
            >>> PermutationUtils.prev_permutation([1, 3, 2])
            [1, 2, 3]
        """
        n = len(elements)
        
        # 找到第一个升序位置
        i = n - 2
        while i >= 0 and elements[i] <= elements[i + 1]:
            i -= 1
        
        if i < 0:
            return None
        
        # 找到比 elements[i] 小的最大元素
        j = n - 1
        while elements[j] >= elements[i]:
            j -= 1
        
        # 交换
        elements[i], elements[j] = elements[j], elements[i]
        
        # 反转 i+1 到末尾
        elements[i+1:] = elements[i+1:][::-1]
        
        return elements
    
    @staticmethod
    def inversion_count(perm: Tuple[Any, ...]) -> int:
        """
        计算排列的逆序对数量
        
        Args:
            perm: 排列元组（元素应该是可比较的）
        
        Returns:
            逆序对数量
        
        Examples:
            >>> PermutationUtils.inversion_count((3, 2, 1))
            3
            >>> PermutationUtils.inversion_count((1, 2, 3))
            0
        """
        # 使用归并排序计算逆序对
        arr = list(perm)
        
        def merge_count(arr: List, temp: List, left: int, right: int) -> int:
            if left >= right:
                return 0
            
            mid = (left + right) // 2
            count = merge_count(arr, temp, left, mid)
            count += merge_count(arr, temp, mid + 1, right)
            
            # 归并
            i, j, k = left, mid + 1, left
            while i <= mid and j <= right:
                if arr[i] <= arr[j]:
                    temp[k] = arr[i]
                    i += 1
                else:
                    temp[k] = arr[j]
                    count += (mid - i + 1)  # 逆序对
                    j += 1
                k += 1
            
            while i <= mid:
                temp[k] = arr[i]
                i += 1
                k += 1
            while j <= right:
                temp[k] = arr[j]
                j += 1
                k += 1
            
            for i in range(left, right + 1):
                arr[i] = temp[i]
            
            return count
        
        n = len(arr)
        return merge_count(arr, [0] * n, 0, n - 1)
    
    @staticmethod
    def is_even_permutation(perm: Tuple[int, ...]) -> bool:
        """
        判断是否为偶排列
        
        Args:
            perm: 排列元组（元素为 1 到 n 或 0 到 n-1）
        
        Returns:
            是否为偶排列
        
        Examples:
            >>> PermutationUtils.is_even_permutation((1, 2, 3))
            True
            >>> PermutationUtils.is_even_permutation((2, 1, 3))
            False
        """
        return PermutationUtils.inversion_count(perm) % 2 == 0
    
    @staticmethod
    def is_odd_permutation(perm: Tuple[int, ...]) -> bool:
        """判断是否为奇排列"""
        return PermutationUtils.inversion_count(perm) % 2 == 1
    
    @staticmethod
    def permutation_sign(perm: Tuple[int, ...]) -> int:
        """
        返回排列的符号 (+1 或 -1)
        偶排列返回 1，奇排列返回 -1
        
        Examples:
            >>> PermutationUtils.permutation_sign((1, 2, 3))
            1
            >>> PermutationUtils.permutation_sign((2, 1, 3))
            -1
        """
        return 1 if PermutationUtils.is_even_permutation(perm) else -1


class CombinationUtils:
    """组合工具类"""
    
    @staticmethod
    def combinations(elements: List[Any], k: int) -> Iterator[Tuple[Any, ...]]:
        """
        生成组合
        
        Args:
            elements: 元素列表
            k: 组合大小
        
        Yields:
            组合元组
        
        Examples:
            >>> list(CombinationUtils.combinations([1, 2, 3, 4], 2))
            [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
        """
        n = len(elements)
        if k > n or k < 0:
            return
        if k == 0:
            yield ()
            return
        
        # 使用索引数组生成
        indices = list(range(k))
        yield tuple(elements[i] for i in indices)
        
        while True:
            # 找到可以递增的位置
            for i in range(k - 1, -1, -1):
                if indices[i] != i + n - k:
                    break
            else:
                return
            
            indices[i] += 1
            for j in range(i + 1, k):
                indices[j] = indices[j - 1] + 1
            
            yield tuple(elements[i] for i in indices)
    
    @staticmethod
    def combination_count(n: int, k: int) -> int:
        """
        计算组合数 C(n, k)
        
        Args:
            n: 总元素数
            k: 选取数
        
        Returns:
            组合数
        
        Examples:
            >>> CombinationUtils.combination_count(5, 2)
            10
            >>> CombinationUtils.combination_count(10, 5)
            252
        """
        if k < 0 or k > n:
            return 0
        if k == 0 or k == n:
            return 1
        
        # 使用较小的 k 计算
        k = min(k, n - k)
        result = 1
        for i in range(k):
            result = result * (n - i) // (i + 1)
        return result
    
    @staticmethod
    def combination_rank(comb: Tuple[Any, ...], elements: List[Any]) -> int:
        """
        计算组合的字典序编号（从0开始）
        
        Args:
            comb: 组合元组
            elements: 元素列表（需排序后）
        
        Returns:
            字典序编号
        
        Examples:
            >>> CombinationUtils.combination_rank((1, 2), [1, 2, 3, 4])
            0
            >>> CombinationUtils.combination_rank((3, 4), [1, 2, 3, 4])
            5
        """
        # 使用组合数公式计算序号
        # 序号 = C(n-1, k) + ... 迭代计算
        sorted_elements = sorted(elements)
        sorted_comb = tuple(sorted(comb))
        k = len(sorted_comb)
        
        rank = 0
        prev = -1
        
        for i, elem in enumerate(sorted_comb):
            idx = sorted_elements.index(elem)
            # 累加从 prev+1 到 idx-1 的组合数
            for j in range(prev + 1, idx):
                remaining = len(sorted_elements) - j - 1
                needed = k - i - 1
                rank += CombinationUtils.combination_count(remaining, needed)
            prev = idx
        
        return rank
    
    @staticmethod
    def combination_unrank(rank: int, elements: List[Any], k: int) -> Tuple[Any, ...]:
        """
        根据字典序编号生成组合
        
        Args:
            rank: 字典序编号（从0开始）
            elements: 元素列表
            k: 组合大小
        
        Returns:
            组合元组
        
        Examples:
            >>> CombinationUtils.combination_unrank(0, [1, 2, 3, 4], 2)
            (1, 2)
            >>> CombinationUtils.combination_unrank(5, [1, 2, 3, 4], 2)
            (3, 4)
        """
        sorted_elements = sorted(elements)
        n = len(sorted_elements)
        result = []
        prev = -1
        
        for i in range(k):
            for j in range(prev + 1, n):
                remaining = n - j - 1
                needed = k - i - 1
                cnt = CombinationUtils.combination_count(remaining, needed)
                
                if rank < cnt:
                    result.append(sorted_elements[j])
                    prev = j
                    break
                rank -= cnt
        
        return tuple(result)
    
    @staticmethod
    def all_subsets(elements: List[Any]) -> Iterator[Tuple[Any, ...]]:
        """
        生成所有子集（幂集）
        
        Args:
            elements: 元素列表
        
        Yields:
            子集元组
        
        Examples:
            >>> list(CombinationUtils.all_subsets([1, 2]))
            [(), (1,), (2,), (1, 2)]
        """
        n = len(elements)
        for k in range(n + 1):
            yield from CombinationUtils.combinations(elements, k)
    
    @staticmethod
    def subset_count(n: int) -> int:
        """计算子集数量（幂集大小）"""
        return 2 ** n


class PermutationUtilsAdvanced:
    """排列高级工具"""
    
    @staticmethod
    def random_permutation(n: int, seed: Optional[int] = None) -> Tuple[int, ...]:
        """
        生成随机排列（Fisher-Yates 洗牌算法）
        
        Args:
            n: 排列长度
            seed: 随机种子
        
        Returns:
            随机排列
        
        Examples:
            >>> p = PermutationUtilsAdvanced.random_permutation(5, seed=42)
            >>> len(p)
            5
        """
        import random
        if seed is not None:
            random.seed(seed)
        
        arr = list(range(1, n + 1))
        for i in range(n - 1, 0, -1):
            j = random.randint(0, i)
            arr[i], arr[j] = arr[j], arr[i]
        
        return tuple(arr)
    
    @staticmethod
    def random_combination(n: int, k: int, seed: Optional[int] = None) -> Tuple[int, ...]:
        """
        生成随机组合
        
        Args:
            n: 总元素数 (1到n)
            k: 组合大小
            seed: 随机种子
        
        Returns:
            随机组合
        
        Examples:
            >>> c = PermutationUtilsAdvanced.random_combination(10, 3, seed=42)
            >>> len(c)
            3
        """
        import random
        if seed is not None:
            random.seed(seed)
        
        # 蓄水池抽样算法
        result = list(range(1, k + 1))
        for i in range(k + 1, n + 1):
            j = random.randint(1, i)
            if j <= k:
                result[j - 1] = i
        
        return tuple(sorted(result))
    
    @staticmethod
    def multiset_permutations(elements: List[Any]) -> Iterator[Tuple[Any, ...]]:
        """
        生成多重集排列（处理重复元素）
        
        Args:
            elements: 元素列表（可能有重复）
        
        Yields:
            排列元组
        
        Examples:
            >>> list(PermutationUtilsAdvanced.multiset_permutations([1, 1, 2]))
            [(1, 1, 2), (1, 2, 1), (2, 1, 1)]
        """
        # 使用计数器方法
        from collections import Counter
        counter = Counter(elements)
        n = len(elements)
        
        def backtrack(path: List, counter: Counter) -> Iterator[Tuple]:
            if len(path) == n:
                yield tuple(path)
                return
            
            for elem in sorted(counter.keys()):
                if counter[elem] > 0:
                    counter[elem] -= 1
                    path.append(elem)
                    yield from backtrack(path, counter)
                    path.pop()
                    counter[elem] += 1
        
        yield from backtrack([], counter)
    
    @staticmethod
    def multiset_permutation_count(elements: List[Any]) -> int:
        """
        计算多重集排列数
        
        Args:
            elements: 元素列表（可能有重复）
        
        Returns:
            多重集排列数
        
        Examples:
            >>> PermutationUtilsAdvanced.multiset_permutation_count([1, 1, 2])
            3
            >>> PermutationUtilsAdvanced.multiset_permutation_count([1, 1, 1, 2, 2])
            10
        """
        from collections import Counter
        n = len(elements)
        counter = Counter(elements)
        
        result = factorial(n)
        for count in counter.values():
            result //= factorial(count)
        
        return result
    
    @staticmethod
    def kth_permutation_with_duplicates(elements: List[Any], k: int) -> Tuple[Any, ...]:
        """
        获取多重集的第k个排列（字典序）
        
        Args:
            elements: 元素列表
            k: 序号（从0开始）
        
        Returns:
            第k个排列
        
        Examples:
            >>> PermutationUtilsAdvanced.kth_permutation_with_duplicates([1, 1, 2], 1)
            (1, 2, 1)
        """
        from collections import Counter
        n = len(elements)
        counter = Counter(elements)
        sorted_elements = sorted(counter.keys())
        result = []
        
        for i in range(n):
            for elem in sorted_elements:
                if counter[elem] == 0:
                    continue
                
                # 选择 elem 后，剩余排列数
                counter[elem] -= 1
                count = PermutationUtilsAdvanced.multiset_permutation_count(
                    [e for e in elements if e not in result + [elem] or counter.get(e, 0) > 0]
                )
                
                # 重新计算
                remaining = []
                temp_counter = counter.copy()
                for e, c in counter.items():
                    remaining.extend([e] * c)
                count = PermutationUtilsAdvanced.multiset_permutation_count(remaining)
                
                if k < count:
                    result.append(elem)
                    break
                else:
                    k -= count
                    counter[elem] += 1
        
        return tuple(result)
    
    @staticmethod
    def derangements(n: int) -> Iterator[Tuple[int, ...]]:
        """
        生成错排（每个元素都不在原位置的排列）
        
        Args:
            n: 排列长度
        
        Yields:
            错排元组
        
        Examples:
            >>> list(PermutationUtilsAdvanced.derangements(3))
            [(2, 3, 1), (3, 1, 2)]
        """
        for perm in PermutationUtils.permutations(list(range(1, n + 1))):
            if all(perm[i] != i + 1 for i in range(n)):
                yield perm
    
    @staticmethod
    def derangement_count(n: int) -> int:
        """
        计算错排数 D(n)
        
        使用公式: D(n) = n! * (1 - 1/1! + 1/2! - 1/3! + ... + (-1)^n/n!)
        
        Examples:
            >>> PermutationUtilsAdvanced.derangement_count(3)
            2
            >>> PermutationUtilsAdvanced.derangement_count(4)
            9
        """
        if n == 0:
            return 1
        if n == 1:
            return 0
        
        # 使用递推公式: D(n) = (n-1) * (D(n-1) + D(n-2))
        d = [1, 0]
        for i in range(2, n + 1):
            d.append((i - 1) * (d[i-1] + d[i-2]))
        
        return d[n]
    
    @staticmethod
    def is_derangement(perm: Tuple[int, ...]) -> bool:
        """
        判断是否为错排
        
        Args:
            perm: 排列元组（元素为 1 到 n 或 0 到 n-1）
        
        Returns:
            是否为错排
        
        Examples:
            >>> PermutationUtilsAdvanced.is_derangement((2, 3, 1))
            True
            >>> PermutationUtilsAdvanced.is_derangement((1, 2, 3))
            False
        """
        # 判断是否为 1-indexed
        min_val = min(perm)
        for i, val in enumerate(perm):
            expected = i + 1 if min_val == 1 else i
            if val == expected:
                return False
        return True


# 便捷函数
def permutations(elements: List[Any], k: Optional[int] = None) -> Iterator[Tuple[Any, ...]]:
    """生成排列"""
    return PermutationUtils.permutations(elements, k)


def combinations(elements: List[Any], k: int) -> Iterator[Tuple[Any, ...]]:
    """生成组合"""
    return CombinationUtils.combinations(elements, k)


def permutation_count(n: int, k: Optional[int] = None) -> int:
    """计算排列数"""
    return PermutationUtils.permutation_count(n, k)


def combination_count(n: int, k: int) -> int:
    """计算组合数"""
    return CombinationUtils.combination_count(n, k)


def factorial_val(n: int) -> int:
    """计算阶乘"""
    if n < 0:
        raise ValueError("阶乘不支持负数")
    return factorial(n)


# 导出
__all__ = [
    'PermutationUtils',
    'CombinationUtils', 
    'PermutationUtilsAdvanced',
    'permutations',
    'combinations',
    'permutation_count',
    'combination_count',
    'factorial_val',
]