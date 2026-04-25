"""
Rabin-Karp 字符串匹配算法工具模块

Rabin-Karp 算法是一种基于哈希的字符串匹配算法，特别适合多模式匹配场景。
核心思想：使用滚动哈希快速计算子串哈希值，减少字符串比较次数。

时间复杂度:
- 单模式匹配: O(n + m) 平均，O(nm) 最坏
- 多模式匹配: O(n + km) 其中 k 为模式数量

空间复杂度: O(1) 单模式，O(k) 多模式

特点:
- 支持多模式同时匹配
- 支持扩展到二维模式匹配
- 适合检测抄袭、DNA序列分析等场景
"""

from typing import List, Tuple, Dict, Optional, Iterator
from dataclasses import dataclass
import random


@dataclass
class MatchResult:
    """匹配结果"""
    index: int          # 匹配起始位置
    pattern: str        # 匹配的模式串
    text_end: int        # 匹配结束位置
    
    def __repr__(self) -> str:
        return f"MatchResult(index={self.index}, pattern='{self.pattern}')"


class RollingHash:
    """
    滚动哈希类
    
    使用多项式滚动哈希实现高效的字符串哈希计算。
    支持在 O(1) 时间内滑动窗口更新哈希值。
    """
    
    def __init__(self, base: int = 256, modulus: int = 10**9 + 7):
        """
        初始化滚动哈希
        
        Args:
            base: 哈希基数（字符集大小，默认256）
            modulus: 哈希模数（大质数，默认10^9+7）
        """
        self.base = base
        self.modulus = modulus
        self._hash = 0
        self._length = 0
        self._base_powers: Dict[int, int] = {0: 1}
    
    def _get_base_power(self, n: int) -> int:
        """预计算并缓存 base^n % modulus"""
        if n not in self._base_powers:
            self._base_powers[n] = (self._get_base_power(n - 1) * self.base) % self.modulus
        return self._base_powers[n]
    
    def compute(self, text: str) -> int:
        """
        计算字符串的哈希值
        
        Args:
            text: 输入字符串
            
        Returns:
            哈希值
        """
        self._hash = 0
        self._length = len(text)
        for char in text:
            self._hash = (self._hash * self.base + ord(char)) % self.modulus
        return self._hash
    
    def slide(self, old_char: str, new_char: str, window_size: int) -> int:
        """
        滑动窗口，移除最左字符，添加新字符
        
        Args:
            old_char: 要移除的字符
            new_char: 要添加的字符
            window_size: 窗口大小
            
        Returns:
            更新后的哈希值
        """
        # 移除最左字符的影响
        old_value = ord(old_char) * self._get_base_power(window_size - 1)
        self._hash = (self._hash - old_value) % self.modulus
        # 添加新字符
        self._hash = (self._hash * self.base + ord(new_char)) % self.modulus
        return self._hash
    
    @property
    def hash(self) -> int:
        """获取当前哈希值"""
        return self._hash


def rabin_karp_search(text: str, pattern: str, 
                      base: int = 256, 
                      modulus: int = 10**9 + 7) -> List[int]:
    """
    单模式 Rabin-Karp 搜索
    
    在文本中查找所有模式出现的位置。
    
    Args:
        text: 被搜索的文本
        pattern: 搜索模式
        base: 哈希基数
        modulus: 哈希模数
        
    Returns:
        匹配起始位置的列表
        
    Example:
        >>> rabin_karp_search("abracadabra", "abra")
        [0, 7]
    """
    n, m = len(text), len(pattern)
    
    if m == 0 or m > n:
        return []
    
    if m == n:
        return [0] if text == pattern else []
    
    results = []
    roller = RollingHash(base, modulus)
    
    # 计算模式的哈希
    pattern_hash = roller.compute(pattern)
    
    # 计算文本第一个窗口的哈希
    window_hash = roller.compute(text[:m])
    
    # 预计算 base^(m-1) 用于滑动
    high_order = pow(base, m - 1, modulus)
    
    for i in range(n - m + 1):
        # 哈希匹配时验证
        if window_hash == pattern_hash:
            if text[i:i + m] == pattern:
                results.append(i)
        
        # 滑动窗口
        if i < n - m:
            # 移除 text[i]，添加 text[i+m]
            window_hash = (window_hash - ord(text[i]) * high_order) % modulus
            window_hash = (window_hash * base + ord(text[i + m])) % modulus
    
    return results


def multi_pattern_search(text: str, patterns: List[str],
                         base: int = 256,
                         modulus: int = 10**9 + 7) -> List[MatchResult]:
    """
    多模式 Rabin-Karp 搜索
    
    在文本中同时查找多个模式的所有出现位置。
    通过哈希分组，相同长度的模式共享哈希计算。
    
    Args:
        text: 被搜索的文本
        patterns: 搜索模式列表
        base: 哈希基数
        modulus: 哈希模数
        
    Returns:
        匹配结果列表，按位置排序
        
    Example:
        >>> multi_pattern_search("hello world", ["lo", "wor", "ld"])
        [MatchResult(index=3, pattern='lo'), MatchResult(index=6, pattern='wor'), MatchResult(index=9, pattern='ld')]
    """
    if not patterns or not text:
        return []
    
    n = len(text)
    results = []
    
    # 按长度分组
    patterns_by_length: Dict[int, List[str]] = {}
    for pattern in patterns:
        if pattern:  # 跳过空模式
            length = len(pattern)
            if length <= n:
                if length not in patterns_by_length:
                    patterns_by_length[length] = []
                patterns_by_length[length].append(pattern)
    
    # 对每个长度组进行搜索
    for length, group_patterns in patterns_by_length.items():
        if length > n:
            continue
        
        # 计算该组所有模式的哈希
        roller = RollingHash(base, modulus)
        pattern_hashes: Dict[int, List[str]] = {}
        
        for pattern in group_patterns:
            h = roller.compute(pattern)
            if h not in pattern_hashes:
                pattern_hashes[h] = []
            pattern_hashes[h].append(pattern)
        
        # 滑动窗口搜索
        window_hash = roller.compute(text[:length])
        high_order = pow(base, length - 1, modulus)
        
        for i in range(n - length + 1):
            if window_hash in pattern_hashes:
                # 哈希匹配，验证所有候选模式
                for pattern in pattern_hashes[window_hash]:
                    if text[i:i + length] == pattern:
                        results.append(MatchResult(i, pattern, i + length))
            
            # 滑动窗口
            if i < n - length:
                window_hash = (window_hash - ord(text[i]) * high_order) % modulus
                window_hash = (window_hash * base + ord(text[i + length])) % modulus
    
    # 按位置排序
    results.sort(key=lambda x: x.index)
    return results


def find_all_occurrences(text: str, pattern: str) -> List[MatchResult]:
    """
    查找模式在文本中的所有出现位置（便捷方法）
    
    Args:
        text: 被搜索的文本
        pattern: 搜索模式
        
    Returns:
        匹配结果列表
    """
    indices = rabin_karp_search(text, pattern)
    return [MatchResult(i, pattern, i + len(pattern)) for i in indices]


def contains_pattern(text: str, pattern: str) -> bool:
    """
    检查文本是否包含模式
    
    Args:
        text: 被搜索的文本
        pattern: 搜索模式
        
    Returns:
        是否包含
        
    Example:
        >>> contains_pattern("hello world", "world")
        True
    """
    return len(rabin_karp_search(text, pattern)) > 0


def count_occurrences(text: str, pattern: str) -> int:
    """
    统计模式在文本中出现的次数
    
    Args:
        text: 被搜索的文本
        pattern: 搜索模式
        
    Returns:
        出现次数
        
    Example:
        >>> count_occurrences("banana", "ana")
        2
    """
    return len(rabin_karp_search(text, pattern))


def find_with_wildcards(text: str, pattern: str, 
                        wildcard: str = '?') -> List[int]:
    """
    支持通配符的 Rabin-Karp 搜索
    
    通配符可以匹配任意单个字符。通过枚举通配符位置来处理。
    注意：多个通配符会导致性能下降。
    
    Args:
        text: 被搜索的文本
        pattern: 带通配符的模式
        wildcard: 通配符字符
        
    Returns:
        匹配起始位置的列表
        
    Example:
        >>> find_with_wildcards("hello", "h?llo")
        [0]
    """
    wildcard_count = pattern.count(wildcard)
    
    if wildcard_count == 0:
        return rabin_karp_search(text, pattern)
    
    if wildcard_count > 10:
        # 通配符太多，使用暴力匹配
        return _wildcard_brute_force(text, pattern, wildcard)
    
    n, m = len(text), len(pattern)
    if m == 0 or m > n:
        return []
    
    results = []
    non_wildcard_pattern = pattern.replace(wildcard, '')
    
    # 对每个可能的起始位置验证
    for i in range(n - m + 1):
        match = True
        for j, pc in enumerate(pattern):
            if pc != wildcard and text[i + j] != pc:
                match = False
                break
        if match:
            results.append(i)
    
    return results


def _wildcard_brute_force(text: str, pattern: str, wildcard: str) -> List[int]:
    """通配符暴力匹配"""
    n, m = len(text), len(pattern)
    results = []
    for i in range(n - m + 1):
        match = True
        for j, pc in enumerate(pattern):
            if pc != wildcard and text[i + j] != pc:
                match = False
                break
        if match:
            results.append(i)
    return results


def find_longest_repeated_substring(text: str, min_length: int = 2) -> Optional[Tuple[str, List[int]]]:
    """
    查找最长重复子串
    
    使用 Rabin-Karp 配合二分搜索查找文本中最长的重复子串。
    
    Args:
        text: 输入文本
        min_length: 最小长度要求
        
    Returns:
        (子串, 所有出现位置列表) 或 None
        
    Example:
        >>> find_longest_repeated_substring("banana")
        ('ana', [1, 3])
    """
    n = len(text)
    if n < min_length * 2:
        return None
    
    def check_length(length: int) -> Optional[Tuple[str, List[int]]]:
        """检查是否存在长度为 length 的重复子串"""
        roller = RollingHash()
        seen: Dict[int, Tuple[str, int]] = {}  # hash -> (substring, first_index)
        
        window_hash = roller.compute(text[:length])
        high_order = pow(roller.base, length - 1, roller.modulus)
        
        for i in range(n - length + 1):
            if window_hash in seen:
                substring, first_idx = seen[window_hash]
                if text[i:i + length] == substring:
                    return (substring, [first_idx, i])
            else:
                seen[window_hash] = (text[i:i + length], i)
            
            if i < n - length:
                window_hash = (window_hash - ord(text[i]) * high_order) % roller.modulus
                window_hash = (window_hash * roller.base + ord(text[i + length])) % roller.modulus
        
        return None
    
    # 二分搜索最长长度
    left, right = min_length, n // 2
    result = None
    
    while left <= right:
        mid = (left + right) // 2
        found = check_length(mid)
        if found:
            result = found
            left = mid + 1
        else:
            right = mid - 1
    
    return result


def find_common_substring(strings: List[str], min_length: int = 2) -> Optional[str]:
    """
    查找多个字符串的最长公共子串
    
    Args:
        strings: 字符串列表
        min_length: 最小长度
        
    Returns:
        最长公共子串或None
        
    Example:
        >>> find_common_substring(["programming", "programmer", "program"])
        'program'
    """
    if len(strings) < 2:
        return strings[0] if strings else None
    
    # 以最短字符串为基准
    shortest = min(strings, key=len)
    other_strings = [s for s in strings if s != shortest]
    
    n = len(shortest)
    if n < min_length:
        return None
    
    def check_length(length: int) -> Optional[str]:
        roller = RollingHash()
        seen: Dict[int, str] = {}
        
        window_hash = roller.compute(shortest[:length])
        high_order = pow(roller.base, length - 1, roller.modulus)
        
        for i in range(n - length + 1):
            if window_hash not in seen:
                substring = shortest[i:i + length]
                # 检查是否在所有字符串中出现
                if all(substring in s for s in other_strings):
                    seen[window_hash] = substring
                    return substring
                seen[window_hash] = shortest[i:i + length]
            
            if i < n - length:
                window_hash = (window_hash - ord(shortest[i]) * high_order) % roller.modulus
                window_hash = (window_hash * roller.base + ord(shortest[i + length])) % roller.modulus
        
        return None
    
    # 二分搜索
    left, right = min_length, n
    result = None
    
    while left <= right:
        mid = (left + right) // 2
        found = check_length(mid)
        if found:
            result = found
            left = mid + 1
        else:
            right = mid - 1
    
    return result


def compute_similarity(text1: str, text2: str, k: int = 5) -> float:
    """
    基于公共子串的文本相似度计算
    
    使用 k-gram 和 Rabin-Karp 计算 Jaccard 相似度。
    
    Args:
        text1: 第一个文本
        text2: 第二个文本
        k: k-gram 大小
        
    Returns:
        相似度值 [0, 1]
        
    Example:
        >>> compute_similarity("hello world", "hello there")
        0.5
    """
    if not text1 or not text2:
        return 0.0
    
    if text1 == text2:
        return 1.0
    
    def get_kgrams(text: str, k: int) -> set:
        """获取所有 k-gram 的哈希集合"""
        if len(text) < k:
            return {hash(text)}
        
        roller = RollingHash()
        grams = set()
        
        h = roller.compute(text[:k])
        high_order = pow(roller.base, k - 1, roller.modulus)
        
        for i in range(len(text) - k + 1):
            grams.add(h)
            if i < len(text) - k:
                h = (h - ord(text[i]) * high_order) % roller.modulus
                h = (h * roller.base + ord(text[i + k])) % roller.modulus
        
        return grams
    
    set1 = get_kgrams(text1, k)
    set2 = get_kgrams(text2, k)
    
    if not set1 or not set2:
        return 0.0
    
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    return intersection / union if union > 0 else 0.0


def detect_plagiarism(documents: List[str], threshold: float = 0.5, 
                      k: int = 10) -> List[Tuple[int, int, float]]:
    """
    检测文档之间的抄袭嫌疑
    
    Args:
        documents: 文档列表
        threshold: 相似度阈值
        k: k-gram 大小
        
    Returns:
        (文档1索引, 文档2索引, 相似度) 的列表
        
    Example:
        >>> docs = ["Hello world", "Hello there", "Completely different"]
        >>> detect_plagiarism(docs, threshold=0.3)
        [(0, 1, 0.5)]
    """
    results = []
    n = len(documents)
    
    for i in range(n):
        for j in range(i + 1, n):
            similarity = compute_similarity(documents[i], documents[j], k)
            if similarity >= threshold:
                results.append((i, j, similarity))
    
    # 按相似度降序排序
    results.sort(key=lambda x: x[2], reverse=True)
    return results


# ============== 高级功能 ==============

def two_d_pattern_search(text_grid: List[str], pattern_grid: List[str]) -> List[Tuple[int, int]]:
    """
    二维模式搜索
    
    在二维文本网格中搜索二维模式。
    
    Args:
        text_grid: 文本网格（字符串列表）
        pattern_grid: 模式网格（字符串列表）
        
    Returns:
        匹配位置 (行, 列) 列表
        
    Example:
        >>> text = ["abcde", "fghij", "klmno"]
        >>> pattern = ["ghi", "lmn"]
        >>> two_d_pattern_search(text, pattern)
        [(1, 1)]
    """
    if not text_grid or not pattern_grid:
        return []
    
    text_rows = len(text_grid)
    text_cols = len(text_grid[0])
    pattern_rows = len(pattern_grid)
    pattern_cols = len(pattern_grid[0])
    
    if pattern_rows > text_rows or pattern_cols > text_cols:
        return []
    
    # 验证网格一致性
    for row in text_grid:
        if len(row) != text_cols:
            raise ValueError("文本网格所有行必须等长")
    for row in pattern_grid:
        if len(row) != pattern_cols:
            raise ValueError("模式网格所有行必须等长")
    
    results = []
    
    # 对每一行使用 Rabin-Karp 进行模式搜索
    for start_row in range(text_rows - pattern_rows + 1):
        # 获取文本子网格的行哈希
        roller = RollingHash()
        pattern_row_hashes = [roller.compute(row) for row in pattern_grid]
        
        for start_col in range(text_cols - pattern_cols + 1):
            # 提取子网格并验证
            match = True
            for pi, pr in enumerate(pattern_grid):
                text_segment = text_grid[start_row + pi][start_col:start_col + pattern_cols]
                if text_segment != pr:
                    match = False
                    break
            
            if match:
                results.append((start_row, start_col))
    
    return results


class RabinKarpMatcher:
    """
    Rabin-Karp 匹配器类
    
    预编译模式，支持高效的多文本搜索。
    适合需要多次搜索相同模式的场景。
    """
    
    def __init__(self, patterns: List[str], base: int = 256, modulus: int = 10**9 + 7):
        """
        初始化匹配器
        
        Args:
            patterns: 要匹配的模式列表
            base: 哈希基数
            modulus: 哈希模数
        """
        self.base = base
        self.modulus = modulus
        self.patterns = [p for p in patterns if p]
        self._build_index()
    
    def _build_index(self):
        """构建模式索引"""
        self._length_groups: Dict[int, Dict[int, List[str]]] = {}
        roller = RollingHash(self.base, self.modulus)
        
        for pattern in self.patterns:
            length = len(pattern)
            if length not in self._length_groups:
                self._length_groups[length] = {}
            
            h = roller.compute(pattern)
            if h not in self._length_groups[length]:
                self._length_groups[length][h] = []
            self._length_groups[length][h].append(pattern)
    
    def search(self, text: str) -> List[MatchResult]:
        """
        在文本中搜索所有预编译模式
        
        Args:
            text: 输入文本
            
        Returns:
            匹配结果列表
        """
        if not text or not self.patterns:
            return []
        
        results = []
        n = len(text)
        roller = RollingHash(self.base, self.modulus)
        
        for length, hash_map in self._length_groups.items():
            if length > n:
                continue
            
            window_hash = roller.compute(text[:length])
            high_order = pow(self.base, length - 1, self.modulus)
            
            for i in range(n - length + 1):
                if window_hash in hash_map:
                    for pattern in hash_map[window_hash]:
                        if text[i:i + length] == pattern:
                            results.append(MatchResult(i, pattern, i + length))
                
                if i < n - length:
                    window_hash = (window_hash - ord(text[i]) * high_order) % self.modulus
                    window_hash = (window_hash * self.base + ord(text[i + length])) % self.modulus
        
        results.sort(key=lambda x: x.index)
        return results
    
    def search_iter(self, text: str) -> Iterator[MatchResult]:
        """
        迭代器版本的搜索
        
        Args:
            text: 输入文本
            
        Yields:
            匹配结果
        """
        for result in self.search(text):
            yield result
    
    def add_pattern(self, pattern: str):
        """动态添加模式"""
        if pattern and pattern not in self.patterns:
            self.patterns.append(pattern)
            self._build_index()
    
    def remove_pattern(self, pattern: str):
        """移除模式"""
        if pattern in self.patterns:
            self.patterns.remove(pattern)
            self._build_index()


# 双哈希（降低冲突概率）

def double_hash_search(text: str, pattern: str) -> List[int]:
    """
    双哈希 Rabin-Karp 搜索
    
    使用两个不同的哈希函数降低冲突概率，
    提高匹配可靠性。
    
    Args:
        text: 输入文本
        pattern: 搜索模式
        
    Returns:
        匹配位置列表
    """
    n, m = len(text), len(pattern)
    
    if m == 0 or m > n:
        return []
    
    # 两个不同的质数模数
    mod1 = 10**9 + 7
    mod2 = 10**9 + 9
    base = 256
    
    results = []
    
    # 计算模式的双哈希
    h1 = h2 = 0
    for char in pattern:
        h1 = (h1 * base + ord(char)) % mod1
        h2 = (h2 * base + ord(char)) % mod2
    
    # 计算文本窗口的双哈希
    w1 = w2 = 0
    for i in range(m):
        w1 = (w1 * base + ord(text[i])) % mod1
        w2 = (w2 * base + ord(text[i])) % mod2
    
    high1 = pow(base, m - 1, mod1)
    high2 = pow(base, m - 1, mod2)
    
    for i in range(n - m + 1):
        # 双哈希匹配
        if w1 == h1 and w2 == h2:
            results.append(i)
        
        if i < n - m:
            # 更新窗口哈希
            w1 = (w1 - ord(text[i]) * high1) % mod1
            w1 = (w1 * base + ord(text[i + m])) % mod1
            
            w2 = (w2 - ord(text[i]) * high2) % mod2
            w2 = (w2 * base + ord(text[i + m])) % mod2
    
    return results