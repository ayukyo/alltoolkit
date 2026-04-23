#!/usr/bin/env python3
"""
kmp_utils/mod.py - Knuth-Morris-Pratt (KMP) 字符串搜索算法工具集
零外部依赖，纯Python标准库实现

功能：
- KMP 字符串搜索（利用失败函数避免重复比较）
- 单次搜索、全部搜索、计数、替换
- 大小写敏感/不敏感搜索
- 支持搜索位置限制
- 搜索结果详情（位置、匹配文本、上下文）
- 批量模式搜索（多模式匹配）
- Aho-Corasick 简化版多模式匹配
- 边界检测（前缀/后缀/子串）
- 周期性字符串分析

算法特点：
- 时间复杂度 O(n + m)，n 为文本长度，m 为模式长度
- 预处理模式构建失败函数，匹配时无需回溯
- 适用于需要多次匹配同一模式或批量模式匹配的场景
"""

from typing import List, Dict, Tuple, Optional, Set, Generator, Any


# ==================== 核心算法 ====================

def build_failure_function(pattern: str) -> List[int]:
    """
    构建 KMP 失败函数（部分匹配表 / Next 数组）
    
    失败函数 fail[i] 表示 pattern[0:i] 的最长相等真前缀和真后缀的长度。
    当在位置 i 失配时，可以跳转到 fail[i-1] 继续匹配，无需回溯文本指针。
    
    Args:
        pattern: 搜索模式
    
    Returns:
        失败函数数组，长度为 len(pattern)
    
    示例:
        >>> build_failure_function("ABABAC")
        [0, 0, 1, 2, 3, 0]
        >>> build_failure_function("AAAA")
        [0, 1, 2, 3]
        >>> build_failure_function("ABCD")
        [0, 0, 0, 0]
    """
    m = len(pattern)
    if m == 0:
        return []
    
    fail = [0] * m
    j = 0  # 当前最长匹配前缀长度
    
    for i in range(1, m):
        # 回退到可以继续匹配的位置
        while j > 0 and pattern[i] != pattern[j]:
            j = fail[j - 1]
        
        if pattern[i] == pattern[j]:
            j += 1
            fail[i] = j
    
    return fail


def build_next_array(pattern: str) -> List[int]:
    """
    构建 KMP 的 next 数组（另一种表示形式）
    
    next[i] 表示 pattern[i] 失配时，模式串应该跳转到的位置。
    这是一种优化形式，直接给出跳转位置。
    
    Args:
        pattern: 搜索模式
    
    Returns:
        next 数组，next[i] 是失配时的跳转位置
    
    示例:
        >>> build_next_array("ABABAC")
        [-1, 0, 0, 1, 2, 3]
        >>> build_next_array("AAAA")
        [-1, 0, 1, 2]
    """
    m = len(pattern)
    if m == 0:
        return []
    
    # next[0] = -1 表示第一个字符失配时，文本指针前进
    next_arr = [-1] + [0] * (m - 1)
    j = -1
    
    for i in range(1, m):
        while j >= 0 and pattern[i - 1] != pattern[j]:
            j = next_arr[j] if j >= 0 else -1
        j += 1
        next_arr[i] = j
    
    return next_arr


# ==================== 搜索函数 ====================

def search(text: str, pattern: str, start: int = 0) -> int:
    """
    KMP 单次搜索 - 查找模式在文本中首次出现的位置
    
    Args:
        text: 待搜索的文本
        pattern: 搜索模式
        start: 开始搜索的位置，默认为 0
    
    Returns:
        模式首次出现的起始位置，未找到返回 -1
    
    示例:
        >>> search("ABABDABACDABABCABAB", "ABABCABAB")
        10
        >>> search("Hello World", "World")
        6
        >>> search("Hello World", "Python")
        -1
    """
    n, m = len(text), len(pattern)
    if m == 0:
        return start if start <= n else -1
    if m > n:
        return -1
    
    fail = build_failure_function(pattern)
    j = 0  # 模式指针
    
    for i in range(start, n):
        # 失配时利用失败函数回退
        while j > 0 and text[i] != pattern[j]:
            j = fail[j - 1]
        
        if text[i] == pattern[j]:
            j += 1
        
        if j == m:
            return i - m + 1  # 找到匹配
    
    return -1


def search_all(text: str, pattern: str, overlapping: bool = True) -> List[int]:
    """
    KMP 全部搜索 - 查找模式在文本中所有出现的位置
    
    Args:
        text: 待搜索的文本
        pattern: 搜索模式
        overlapping: 是否包含重叠匹配，默认 True
    
    Returns:
        所有匹配位置的列表
    
    示例:
        >>> search_all("ABABABA", "ABA")
        [0, 2, 4]
        >>> search_all("ABABABA", "ABA", overlapping=False)
        [0, 4]
        >>> search_all("AAAA", "AA")
        [0, 1, 2]
        >>> search_all("AAAA", "AA", overlapping=False)
        [0, 2]
    """
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1))
    if m > n:
        return []
    
    fail = build_failure_function(pattern)
    positions = []
    j = 0
    
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = fail[j - 1]
        
        if text[i] == pattern[j]:
            j += 1
        
        if j == m:
            positions.append(i - m + 1)
            if overlapping:
                j = fail[j - 1]  # 允许重叠匹配
            else:
                j = 0  # 不允许重叠，重新开始
    
    return positions


def count(text: str, pattern: str, overlapping: bool = True) -> int:
    """
    计算模式在文本中出现的次数
    
    Args:
        text: 待搜索的文本
        pattern: 搜索模式
        overlapping: 是否计算重叠匹配
    
    Returns:
        匹配次数
    
    示例:
        >>> count("AAAA", "AA")
        3
        >>> count("AAAA", "AA", overlapping=False)
        2
        >>> count("ABCABCABC", "ABC")
        3
    """
    return len(search_all(text, pattern, overlapping))


def replace(text: str, pattern: str, replacement: str, max_replace: int = -1) -> str:
    """
    替换文本中的模式
    
    Args:
        text: 原文本
        pattern: 要替换的模式
        replacement: 替换字符串
        max_replace: 最大替换次数，-1 表示全部替换
    
    Returns:
        替换后的文本
    
    示例:
        >>> replace("ABABAB", "AB", "XY")
        "XYXYXY"
        >>> replace("ABABAB", "AB", "XY", max_replace=2)
        "XYXYAB"
    """
    if pattern == "":
        return text
    
    positions = search_all(text, pattern, overlapping=False)
    if not positions:
        return text
    
    if max_replace > 0:
        positions = positions[:max_replace]
    
    # 从后向前替换，避免位置偏移问题
    result = text
    for pos in reversed(positions):
        result = result[:pos] + replacement + result[pos + len(pattern):]
    
    return result


# ==================== 大小写不敏感搜索 ====================

def search_ignore_case(text: str, pattern: str, start: int = 0) -> int:
    """
    大小写不敏感的单次搜索
    
    Args:
        text: 待搜索的文本
        pattern: 搜索模式
        start: 开始搜索的位置
    
    Returns:
        模式首次出现的起始位置，未找到返回 -1
    
    示例:
        >>> search_ignore_case("Hello World", "WORLD")
        6
        >>> search_ignore_case("Python", "PYTHON")
        0
    """
    return search(text.lower(), pattern.lower(), start)


def search_all_ignore_case(text: str, pattern: str, overlapping: bool = True) -> List[int]:
    """
    大小写不敏感的全部搜索
    
    Args:
        text: 待搜索的文本
        pattern: 搜索模式
        overlapping: 是否包含重叠匹配
    
    Returns:
        所有匹配位置的列表
    
    示例:
        >>> search_all_ignore_case("AbAbaBA", "aba")
        [0, 2, 4]
    """
    return search_all(text.lower(), pattern.lower(), overlapping)


# ==================== 匹配结果详情 ====================

class MatchResult:
    """匹配结果对象"""
    
    def __init__(self, text: str, pattern: str, start: int, end: int):
        self.text = text
        self.pattern = pattern
        self.start = start
        self.end = end
    
    @property
    def matched(self) -> str:
        """匹配的文本"""
        return self.text[self.start:self.end]
    
    def context(self, before: int = 10, after: int = 10) -> Tuple[str, str, str]:
        """
        获取匹配上下文
        
        Args:
            before: 匹配前的字符数
            after: 匹配后的字符数
        
        Returns:
            (前文, 匹配文本, 后文)
        """
        context_start = max(0, self.start - before)
        context_end = min(len(self.text), self.end + after)
        return (
            self.text[context_start:self.start],
            self.matched,
            self.text[self.end:context_end]
        )
    
    def __repr__(self) -> str:
        return f"MatchResult(start={self.start}, end={self.end}, matched='{self.matched}')"
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, MatchResult):
            return False
        return (self.start == other.start and 
                self.end == other.end and 
                self.matched == other.matched)


def search_detailed(text: str, pattern: str, start: int = 0) -> Optional[MatchResult]:
    """
    详细搜索 - 返回匹配结果对象
    
    Args:
        text: 待搜索的文本
        pattern: 搜索模式
        start: 开始搜索的位置
    
    Returns:
        MatchResult 对象，未找到返回 None
    
    示例:
        >>> result = search_detailed("Hello World", "World")
        >>> result.start, result.end
        (6, 11)
        >>> result.context(2, 2)
        ('o ', 'World', '')
    """
    pos = search(text, pattern, start)
    if pos == -1:
        return None
    return MatchResult(text, pattern, pos, pos + len(pattern))


def search_all_detailed(text: str, pattern: str, overlapping: bool = True) -> List[MatchResult]:
    """
    详细全部搜索 - 返回所有匹配结果对象
    
    Args:
        text: 待搜索的文本
        pattern: 搜索模式
        overlapping: 是否包含重叠匹配
    
    Returns:
        MatchResult 对象列表
    
    示例:
        >>> results = search_all_detailed("ABABAB", "ABA")
        >>> len(results)
        2
        >>> results[0].matched
        'ABA'
    """
    positions = search_all(text, pattern, overlapping)
    return [MatchResult(text, pattern, pos, pos + len(pattern)) for pos in positions]


# ==================== 批量模式匹配 ====================

def search_multiple_patterns(text: str, patterns: List[str]) -> Dict[str, List[int]]:
    """
    批量模式搜索 - 在文本中搜索多个模式
    
    对每个模式分别使用 KMP 搜索，返回每个模式的所有匹配位置。
    
    Args:
        text: 待搜索的文本
        patterns: 模式列表
    
    Returns:
        字典: {模式: [位置列表]}
    
    示例:
        >>> search_multiple_patterns("ABCDEFABC", ["ABC", "DEF", "XYZ"])
        {'ABC': [0, 6], 'DEF': [3], 'XYZ': []}
    """
    result = {}
    for pattern in patterns:
        result[pattern] = search_all(text, pattern)
    return result


def search_any_pattern(text: str, patterns: List[str]) -> Tuple[int, str]:
    """
    搜索多个模式中最早出现的任意一个
    
    Args:
        text: 待搜索的文本
        patterns: 模式列表
    
    Returns:
        (最早位置, 匹配的模式)，均未找到返回 (-1, "")
    
    示例:
        >>> search_any_pattern("Hello World", ["World", "Hello"])
        (0, 'Hello')
        >>> search_any_pattern("ABC", ["X", "Y", "Z"])
        (-1, '')
    """
    min_pos = len(text) + 1
    matched_pattern = ""
    
    for pattern in patterns:
        pos = search(text, pattern)
        if pos != -1 and pos < min_pos:
            min_pos = pos
            matched_pattern = pattern
    
    if min_pos <= len(text):
        return (min_pos, matched_pattern)
    return (-1, "")


# ==================== Aho-Corasick 简化版 ====================

class AhoCorasickNode:
    """Aho-Corasick 自动机节点"""
    
    def __init__(self):
        self.children: Dict[str, 'AhoCorasickNode'] = {}
        self.fail: Optional['AhoCorasickNode'] = None
        self.output: List[str] = []  # 在此节点结束的模式


class AhoCorasick:
    """
    Aho-Corasick 多模式匹配自动机
    
    基于 KMP 的失败函数思想构建 Trie 树自动机，
    实现一次扫描匹配多个模式的高效搜索。
    
    时间复杂度: O(n + m + k)，其中 n 是文本长度，m 是模式总长度，k 是匹配数
    
    示例:
        >>> ac = AhoCorasick(["he", "she", "his", "hers"])
        >>> ac.search("ushers")
        [(2, 'he'), (2, 'she'), (3, 'hers')]
    """
    
    def __init__(self, patterns: List[str]):
        """
        初始化 Aho-Corasick 自动机
        
        Args:
            patterns: 要匹配的模式列表
        """
        self.patterns = patterns
        self.root = AhoCorasickNode()
        self._build_trie()
        self._build_fail_links()
    
    def _build_trie(self) -> None:
        """构建 Trie 树"""
        for pattern in self.patterns:
            node = self.root
            for char in pattern:
                if char not in node.children:
                    node.children[char] = AhoCorasickNode()
                node = node.children[char]
            node.output.append(pattern)
    
    def _build_fail_links(self) -> None:
        """构建失败链接（BFS）"""
        from collections import deque
        
        queue = deque()
        
        # 根节点的子节点失败链接指向根
        for char, child in self.root.children.items():
            child.fail = self.root
            queue.append(child)
        
        # BFS 构建失败链接
        while queue:
            current = queue.popleft()
            
            for char, child in current.children.items():
                queue.append(child)
                
                # 沿着失败链接找到可以匹配当前字符的节点
                fail_node = current.fail
                while fail_node and char not in fail_node.children:
                    fail_node = fail_node.fail
                
                child.fail = fail_node.children[char] if fail_node and char in fail_node.children else self.root
                child.output.extend(child.fail.output)
    
    def search(self, text: str) -> List[Tuple[int, str]]:
        """
        在文本中搜索所有模式
        
        Args:
            text: 待搜索的文本
        
        Returns:
            列表: [(结束位置, 匹配的模式), ...]
        
        示例:
            >>> ac = AhoCorasick(["AB", "BC", "ABC"])
            >>> ac.search("ABCABC")
            [(1, 'AB'), (2, 'BC'), (2, 'ABC'), (4, 'AB'), (5, 'BC'), (5, 'ABC')]
        """
        results = []
        node = self.root
        
        for i, char in enumerate(text):
            # 沿着失败链接找到可以匹配的节点
            while node and char not in node.children:
                node = node.fail
            
            if node is None:
                node = self.root
                continue
            
            node = node.children[char]
            
            # 收集所有匹配的模式
            for pattern in node.output:
                results.append((i, pattern))
        
        return results
    
    def search_with_positions(self, text: str) -> List[Tuple[int, int, str]]:
        """
        在文本中搜索所有模式，返回起止位置
        
        Args:
            text: 待搜索的文本
        
        Returns:
            列表: [(起始位置, 结束位置, 匹配的模式), ...]
        
        示例:
            >>> ac = AhoCorasick(["AB", "BC"])
            >>> ac.search_with_positions("ABC")
            [(0, 2, 'AB'), (1, 3, 'BC')]
        """
        results = []
        node = self.root
        
        for i, char in enumerate(text):
            while node and char not in node.children:
                node = node.fail
            
            if node is None:
                node = self.root
                continue
            
            node = node.children[char]
            
            for pattern in node.output:
                start = i - len(pattern) + 1
                results.append((start, i + 1, pattern))
        
        return results


# ==================== 边界检测 ====================

def is_prefix(text: str, pattern: str) -> bool:
    """
    检测模式是否为文本的前缀
    
    Args:
        text: 文本
        pattern: 模式
    
    Returns:
        是否为前缀
    
    示例:
        >>> is_prefix("Hello World", "Hello")
        True
        >>> is_prefix("Hello World", "World")
        False
    """
    if len(pattern) > len(text):
        return False
    return text[:len(pattern)] == pattern


def is_suffix(text: str, pattern: str) -> bool:
    """
    检测模式是否为文本的后缀
    
    Args:
        text: 文本
        pattern: 模式
    
    Returns:
        是否为后缀
    
    示例:
        >>> is_suffix("Hello World", "World")
        True
        >>> is_suffix("Hello World", "Hello")
        False
    """
    if len(pattern) > len(text):
        return False
    return text[-len(pattern):] == pattern


def is_substring(text: str, pattern: str) -> bool:
    """
    检测模式是否为文本的子串
    
    Args:
        text: 文本
        pattern: 模式
    
    Returns:
        是否为子串
    
    示例:
        >>> is_substring("Hello World", "lo Wo")
        True
        >>> is_substring("Hello World", "xyz")
        False
    """
    return search(text, pattern) != -1


# ==================== 周期性字符串分析 ====================

def find_smallest_period(s: str) -> int:
    """
    找到字符串的最小周期长度
    
    利用 KMP 的失败函数计算字符串的最小周期。
    如果字符串可以由某个子串重复构成，返回该子串的长度。
    
    Args:
        s: 输入字符串
    
    Returns:
        最小周期长度，若不存在周期则返回字符串长度
    
    示例:
        >>> find_smallest_period("ABCABCABC")
        3
        >>> find_smallest_period("AAAA")
        1
        >>> find_smallest_period("ABCD")
        4
        >>> find_smallest_period("ABABAB")
        2
    """
    n = len(s)
    if n == 0:
        return 0
    
    fail = build_failure_function(s)
    last_fail = fail[-1]
    
    # 如果 n % (n - last_fail) == 0，则存在周期
    period = n - last_fail
    if n % period == 0:
        return period
    return n


def is_periodic(s: str) -> bool:
    """
    检测字符串是否具有周期性
    
    Args:
        s: 输入字符串
    
    Returns:
        是否具有周期性
    
    示例:
        >>> is_periodic("ABABAB")
        True
        >>> is_periodic("ABABABC")
        False
        >>> is_periodic("AAAA")
        True
    """
    n = len(s)
    if n <= 1:
        return False
    
    period = find_smallest_period(s)
    return period < n


def get_period_unit(s: str) -> str:
    """
    获取字符串的周期单元
    
    Args:
        s: 输入字符串
    
    Returns:
        周期单元字符串，若无周期则返回原字符串
    
    示例:
        >>> get_period_unit("ABCABCABC")
        'ABC'
        >>> get_period_unit("AAAA")
        'A'
        >>> get_period_unit("ABCD")
        'ABCD'
    """
    period = find_smallest_period(s)
    return s[:period]


def count_repetitions(s: str) -> int:
    """
    计算字符串由周期单元重复的次数
    
    Args:
        s: 输入字符串
    
    Returns:
        重复次数，若无周期则返回 1
    
    示例:
        >>> count_repetitions("ABABAB")
        3
        >>> count_repetitions("AAAA")
        4
        >>> count_repetitions("ABCD")
        1
    """
    n = len(s)
    if n == 0:
        return 0
    
    period = find_smallest_period(s)
    return n // period


# ==================== 边界分析 ====================

def get_borders(s: str) -> List[str]:
    """
    获取字符串的所有边界（border）
    
    边界是既是前缀又是后缀的子串（不包含字符串本身）。
    
    Args:
        s: 输入字符串
    
    Returns:
        所有边界字符串列表，按长度降序排列
    
    示例:
        >>> get_borders("ABABAB")
        ['ABAB', 'AB', '']
        >>> get_borders("AAAA")
        ['AAA', 'AA', 'A', '']
        >>> get_borders("ABCD")
        ['']
    """
    if not s:
        return [""]
    
    borders = [""]
    fail = build_failure_function(s)
    
    # 从失败函数中提取边界长度
    current_len = fail[-1]
    while current_len > 0:
        borders.append(s[:current_len])
        current_len = fail[current_len - 1]
    
    return borders


def get_longest_border(s: str) -> str:
    """
    获取字符串的最长边界
    
    Args:
        s: 输入字符串
    
    Returns:
        最长边界字符串，若无边界返回空字符串
    
    示例:
        >>> get_longest_border("ABABAB")
        'ABAB'
        >>> get_longest_border("ABCD")
        ''
    """
    if not s:
        return ""
    
    fail = build_failure_function(s)
    longest_len = fail[-1]
    return s[:longest_len] if longest_len > 0 else ""


# ==================== 回文相关 ====================

def longest_palindromic_prefix(s: str) -> str:
    """
    找到字符串的最长回文前缀
    
    使用 KMP 技巧：将字符串翻转后拼接，求最长边界。
    
    Args:
        s: 输入字符串
    
    Returns:
        最长回文前缀
    
    示例:
        >>> longest_palindromic_prefix("ABACABA")
        'ABACABA'
        >>> longest_palindromic_prefix("ABACABD")
        'ABA'
        >>> longest_palindromic_prefix("ABC")
        'A'
    """
    if not s:
        return ""
    
    # 使用特殊字符分隔，避免干扰
    combined = s + "#" + s[::-1]
    fail = build_failure_function(combined)
    
    # 最长边界即为最长回文前缀
    longest_len = fail[-1]
    return s[:longest_len]


def longest_palindromic_suffix(s: str) -> str:
    """
    找到字符串的最长回文后缀
    
    Args:
        s: 输入字符串
    
    Returns:
        最长回文后缀
    
    示例:
        >>> longest_palindromic_suffix("ABACABA")
        'ABACABA'
        >>> longest_palindromic_suffix("DBACABA")
        'ABACABA'
    """
    if not s:
        return ""
    
    combined = s[::-1] + "#" + s
    fail = build_failure_function(combined)
    
    longest_len = fail[-1]
    return s[-longest_len:] if longest_len > 0 else ""


# ==================== 字符串匹配工具 ====================

def minimum_append_for_palindrome(s: str) -> str:
    """
    计算需要在字符串末尾添加的最少字符，使其成为回文
    
    策略：找到最长回文后缀，将前缀部分反转后追加。
    
    Args:
        s: 输入字符串
    
    Returns:
        需要添加的字符
    
    示例:
        >>> minimum_append_for_palindrome("ABAC")
        'ABA'
        >>> minimum_append_for_palindrome("ABACABA")
        ''
    """
    if not s:
        return ""
    
    # 找到最长回文后缀
    lps = longest_palindromic_suffix(s)
    
    if lps == s:
        return ""  # 已经是回文
    
    # 需要添加的是前缀部分的反转（不包括最长回文后缀部分）
    return s[:len(s) - len(lps)][::-1]


def minimum_prepend_for_palindrome(s: str) -> str:
    """
    计算需要在字符串开头添加的最少字符，使其成为回文
    
    策略：找到最长回文前缀，将剩余部分反转后添加到开头。
    
    Args:
        s: 输入字符串
    
    Returns:
        需要添加的字符
    
    示例:
        >>> minimum_prepend_for_palindrome("CABA")
        'ABA'
        >>> minimum_prepend_for_palindrome("ABACABA")
        ''
    """
    if not s:
        return ""
    
    # 找到最长回文前缀
    lpp = longest_palindromic_prefix(s)
    
    if lpp == s:
        return ""
    
    # 需要添加的是剩余部分的反转
    return s[len(lpp):][::-1]


# ==================== 高级功能 ====================

def find_all_occurrences_with_context(
    text: str, 
    pattern: str, 
    context_length: int = 20
) -> List[Dict[str, Any]]:
    """
    查找所有匹配位置及其上下文
    
    Args:
        text: 文本
        pattern: 模式
        context_length: 上下文长度
    
    Returns:
        包含位置、匹配文本、前后文的字典列表
    
    示例:
        >>> find_all_occurrences_with_context("The quick brown fox", "brown", 5)
        [{'position': 10, 'match': 'brown', 'before': 'quick ', 'after': ' fox'}]
    """
    results = []
    positions = search_all(text, pattern, overlapping=False)
    
    for pos in positions:
        before_start = max(0, pos - context_length)
        after_end = min(len(text), pos + len(pattern) + context_length)
        
        results.append({
            'position': pos,
            'match': text[pos:pos + len(pattern)],
            'before': text[before_start:pos],
            'after': text[pos + len(pattern):after_end]
        })
    
    return results


def highlight_matches(text: str, pattern: str, 
                     highlight_start: str = "[[", 
                     highlight_end: str = "]]") -> str:
    """
    高亮显示文本中的所有匹配
    
    Args:
        text: 原文本
        pattern: 搜索模式
        highlight_start: 高亮开始标记
        highlight_end: 高亮结束标记
    
    Returns:
        高亮后的文本
    
    示例:
        >>> highlight_matches("Hello World", "World")
        'Hello [[World]]'
        >>> highlight_matches("ABABAB", "AB", "<b>", "</b>")
        '<b>AB</b><b>AB</b><b>AB</b>'
    """
    positions = search_all(text, pattern, overlapping=False)
    if not positions:
        return text
    
    result = []
    last_end = 0
    
    for pos in positions:
        result.append(text[last_end:pos])
        result.append(highlight_start)
        result.append(text[pos:pos + len(pattern)])
        result.append(highlight_end)
        last_end = pos + len(pattern)
    
    result.append(text[last_end:])
    return "".join(result)


def split_by_pattern(text: str, pattern: str) -> List[str]:
    """
    使用模式作为分隔符分割文本
    
    Args:
        text: 原文本
        pattern: 分隔符模式
    
    Returns:
        分割后的字符串列表
    
    示例:
        >>> split_by_pattern("A,B,C", ",")
        ['A', 'B', 'C']
        >>> split_by_pattern("ABXABYAB", "AB")
        ['', 'X', 'Y', '']
    """
    if not pattern:
        return list(text)
    
    positions = search_all(text, pattern, overlapping=False)
    if not positions:
        return [text]
    
    result = []
    last_end = 0
    
    for pos in positions:
        result.append(text[last_end:pos])
        last_end = pos + len(pattern)
    
    result.append(text[last_end:])
    return result


# ==================== 生成器版本（内存优化）====================

def search_iter(text: str, pattern: str, overlapping: bool = True) -> Generator[int, None, None]:
    """
    KMP 搜索生成器版本 - 惰性返回匹配位置
    
    适用于大文本搜索，避免一次性存储所有结果。
    
    Args:
        text: 待搜索的文本
        pattern: 搜索模式
        overlapping: 是否包含重叠匹配
    
    Yields:
        匹配位置
    
    示例:
        >>> list(search_iter("ABABABA", "ABA"))
        [0, 2, 4]
    """
    n, m = len(text), len(pattern)
    if m == 0:
        yield from range(n + 1)
        return
    if m > n:
        return
    
    fail = build_failure_function(pattern)
    j = 0
    
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = fail[j - 1]
        
        if text[i] == pattern[j]:
            j += 1
        
        if j == m:
            yield i - m + 1
            if overlapping:
                j = fail[j - 1]
            else:
                j = 0


# ==================== 性能统计 ====================

def search_with_stats(text: str, pattern: str) -> Dict[str, Any]:
    """
    搜索并返回统计信息
    
    Args:
        text: 文本
        pattern: 模式
    
    Returns:
        包含匹配结果和统计信息的字典
    
    示例:
        >>> result = search_with_stats("ABABABAB", "AB")
        >>> result['count']
        4
        >>> result['positions']
        [0, 2, 4, 6]
    """
    import time
    
    # 构建失败函数的时间
    start = time.perf_counter()
    fail = build_failure_function(pattern)
    build_time = time.perf_counter() - start
    
    # 搜索时间
    start = time.perf_counter()
    positions = search_all(text, pattern)
    search_time = time.perf_counter() - start
    
    return {
        'pattern': pattern,
        'pattern_length': len(pattern),
        'text_length': len(text),
        'positions': positions,
        'count': len(positions),
        'build_time_seconds': build_time,
        'search_time_seconds': search_time,
        'total_time_seconds': build_time + search_time,
        'failure_function': fail
    }


# 导出公共接口
__all__ = [
    # 核心算法
    'build_failure_function',
    'build_next_array',
    
    # 搜索函数
    'search',
    'search_all',
    'count',
    'replace',
    
    # 大小写不敏感
    'search_ignore_case',
    'search_all_ignore_case',
    
    # 详细结果
    'MatchResult',
    'search_detailed',
    'search_all_detailed',
    
    # 批量模式
    'search_multiple_patterns',
    'search_any_pattern',
    
    # Aho-Corasick
    'AhoCorasick',
    'AhoCorasickNode',
    
    # 边界检测
    'is_prefix',
    'is_suffix',
    'is_substring',
    
    # 周期性分析
    'find_smallest_period',
    'is_periodic',
    'get_period_unit',
    'count_repetitions',
    
    # 边界分析
    'get_borders',
    'get_longest_border',
    
    # 回文相关
    'longest_palindromic_prefix',
    'longest_palindromic_suffix',
    'minimum_append_for_palindrome',
    'minimum_prepend_for_palindrome',
    
    # 高级功能
    'find_all_occurrences_with_context',
    'highlight_matches',
    'split_by_pattern',
    
    # 生成器
    'search_iter',
    
    # 统计
    'search_with_stats',
]