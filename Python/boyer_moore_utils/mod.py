#!/usr/bin/env python3
"""
boyer_moore_utils/mod.py - Boyer-Moore 字符串搜索算法工具集
零外部依赖，纯Python标准库实现

功能：
- Boyer-Moore 字符串搜索（坏字符规则 + 好后缀规则）
- 单次搜索、全部搜索、计数、替换
- 大小写敏感/不敏感搜索
- 支持搜索位置限制
- 搜索结果详情（位置、匹配文本、上下文）
- 批量模式搜索（多模式匹配）
- 性能统计和对比工具

算法特点：
- 平均时间复杂度 O(n/m)，最坏 O(n)
- 从右向左匹配，利用跳过规则大幅减少比较次数
- 适用于长模式文本搜索，效率极高
"""

from typing import List, Dict, Tuple, Optional, Set
from collections import defaultdict


# ==================== 核心算法 ====================

def _build_bad_char_table(pattern: str) -> Dict[str, int]:
    """构建坏字符表（Bad Character Table）
    
    对于模式中的每个字符，记录其在模式中最右出现位置距离模式末尾的距离。
    如果字符不在模式中，则跳过整个模式长度。
    
    Args:
        pattern: 搜索模式
    
    Returns:
        坏字符跳跃距离表
    """
    table = {}
    pattern_len = len(pattern)
    
    for i in range(pattern_len - 1):
        # 字符最右出现位置到模式末尾的距离
        table[pattern[i]] = pattern_len - 1 - i
    
    return table


def _build_good_suffix_table(pattern: str) -> List[int]:
    """构建好后缀表（Good Suffix Table）
    
    当好后缀匹配但前面的字符不匹配时，根据好后缀规则决定跳跃距离。
    
    Args:
        pattern: 搜索模式
    
    Returns:
        好后缀跳跃距离表
    """
    pattern_len = len(pattern)
    table = [0] * pattern_len
    
    # 后缀匹配长度从1到pattern_len-1
    for suffix_len in range(1, pattern_len):
        # 查找好后缀在模式中其他位置的最右出现
        suffix = pattern[pattern_len - suffix_len:]
        found = False
        
        # 从右向左搜索后缀的其他出现
        for i in range(pattern_len - suffix_len - 1, -1, -1):
            if pattern[i:i + suffix_len] == suffix:
                table[pattern_len - 1 - (pattern_len - suffix_len)] = pattern_len - 1 - i
                found = True
                break
        
        if not found:
            # 检查后缀的后缀是否匹配模式的前缀
            for prefix_len in range(suffix_len - 1, 0, -1):
                if pattern[:prefix_len] == suffix[suffix_len - prefix_len:]:
                    table[pattern_len - 1 - (pattern_len - suffix_len)] = pattern_len - prefix_len
                    found = True
                    break
        
        if not found:
            table[pattern_len - 1 - (pattern_len - suffix_len)] = pattern_len
    
    return table


def _build_full_good_suffix_table(pattern: str) -> List[int]:
    """构建完整的好后缀跳跃表
    
    Args:
        pattern: 搜索模式
    
    Returns:
        好后缀跳跃距离表，索引为失配位置
    """
    pattern_len = len(pattern)
    if pattern_len == 0:
        return []
    
    table = [0] * pattern_len
    
    # 计算每个位置失配时的跳跃距离
    for i in range(pattern_len):
        suffix_len = pattern_len - 1 - i
        
        if suffix_len == 0:
            table[i] = 1
            continue
        
        suffix = pattern[i + 1:]
        found = False
        
        # 在模式左侧寻找相同的子串
        for j in range(i, -1, -1):
            if j >= suffix_len and pattern[j - suffix_len + 1:j + 1] == suffix:
                table[i] = i + 1 - (j - suffix_len + 1)
                found = True
                break
        
        if not found:
            # 检查后缀是否匹配模式前缀
            for prefix_len in range(suffix_len - 1, 0, -1):
                if pattern[:prefix_len] == suffix[suffix_len - prefix_len:]:
                    table[i] = pattern_len - prefix_len
                    found = True
                    break
        
        if not found:
            table[i] = pattern_len
    
    return table


def boyer_moore_search(text: str, pattern: str, 
                       case_sensitive: bool = True,
                       start: int = 0,
                       end: Optional[int] = None) -> int:
    """使用 Boyer-Moore 算法搜索模式在文本中首次出现的位置
    
    Args:
        text: 被搜索的文本
        pattern: 要搜索的模式
        case_sensitive: 是否区分大小写（默认 True）
        start: 搜索起始位置（默认 0）
        end: 搜索结束位置（默认 None，表示到文本末尾）
    
    Returns:
        模式首次出现的索引位置，未找到返回 -1
    
    Examples:
        >>> boyer_moore_search("hello world", "world")
        6
        >>> boyer_moore_search("Hello World", "world", case_sensitive=False)
        6
        >>> boyer_moore_search("hello world", "xyz")
        -1
    """
    if not pattern:
        return 0 if start <= len(text) else -1
    
    # 处理大小写
    search_text = text if case_sensitive else text.lower()
    search_pattern = pattern if case_sensitive else pattern.lower()
    
    text_len = len(search_text)
    pattern_len = len(search_pattern)
    
    # 边界检查
    if pattern_len > text_len:
        return -1
    
    # 设置搜索范围
    search_end = text_len if end is None else min(end, text_len)
    if start >= search_end:
        return -1
    
    # 构建跳跃表
    bad_char = _build_bad_char_table(search_pattern)
    good_suffix = _build_full_good_suffix_table(search_pattern)
    
    # Boyer-Moore 搜索
    i = start  # 文本中的当前位置
    while i <= search_end - pattern_len:
        # 从右向左匹配模式
        j = pattern_len - 1
        while j >= 0 and search_text[i + j] == search_pattern[j]:
            j -= 1
        
        if j < 0:
            # 完全匹配
            return i
        
        # 计算跳跃距离
        # 坏字符跳跃
        bad_char_skip = bad_char.get(search_text[i + j], pattern_len)
        bad_char_skip = max(1, bad_char_skip - (pattern_len - 1 - j))
        
        # 好后缀跳跃
        good_suffix_skip = good_suffix[j] if j < len(good_suffix) else 1
        
        # 取较大跳跃
        i += max(bad_char_skip, good_suffix_skip)
    
    return -1


def boyer_moore_find_all(text: str, pattern: str,
                         case_sensitive: bool = True,
                         start: int = 0,
                         end: Optional[int] = None,
                         overlap: bool = False) -> List[int]:
    """查找模式在文本中所有出现的位置
    
    Args:
        text: 被搜索的文本
        pattern: 要搜索的模式
        case_sensitive: 是否区分大小写
        start: 搜索起始位置
        end: 搜索结束位置
        overlap: 是否允许重叠匹配（默认 False）
    
    Returns:
        所有匹配位置的列表（按升序排列）
    
    Examples:
        >>> boyer_moore_find_all("abababab", "aba")
        [0, 2, 4]
        >>> boyer_moore_find_all("abababab", "aba", overlap=True)
        [0, 2, 4]
        >>> boyer_moore_find_all("abababab", "aba", overlap=False)
        [0, 4]
    """
    if not pattern:
        return list(range(start, len(text) + 1)) if end is None else list(range(start, min(end, len(text) + 1)))
    
    positions = []
    search_end = len(text) if end is None else min(end, len(text))
    pattern_len = len(pattern)
    
    pos = start
    while pos <= search_end - pattern_len:
        found_pos = boyer_moore_search(text, pattern, case_sensitive, pos, search_end)
        if found_pos == -1:
            break
        positions.append(found_pos)
        # 跳到下一个搜索位置
        pos = found_pos + (1 if overlap else pattern_len)
    
    return positions


def boyer_moore_count(text: str, pattern: str,
                      case_sensitive: bool = True,
                      start: int = 0,
                      end: Optional[int] = None) -> int:
    """统计模式在文本中出现的次数
    
    Args:
        text: 被搜索的文本
        pattern: 要搜索的模式
        case_sensitive: 是否区分大小写
        start: 搜索起始位置
        end: 搜索结束位置
    
    Returns:
        模式出现的次数
    
    Examples:
        >>> boyer_moore_count("hello hello hello", "hello")
        3
        >>> boyer_moore_count("Hello hello HELLO", "hello", case_sensitive=False)
        3
    """
    return len(boyer_moore_find_all(text, pattern, case_sensitive, start, end, overlap=False))


def boyer_moore_replace(text: str, pattern: str, replacement: str,
                        case_sensitive: bool = True,
                        count: int = -1) -> str:
    """替换文本中所有匹配的模式
    
    Args:
        text: 被搜索的文本
        pattern: 要搜索的模式
        replacement: 替换字符串
        case_sensitive: 是否区分大小写
        count: 最大替换次数（-1 表示全部替换）
    
    Returns:
        替换后的文本
    
    Examples:
        >>> boyer_moore_replace("hello world hello", "hello", "hi")
        'hi world hi'
        >>> boyer_moore_replace("hello world hello", "hello", "hi", count=1)
        'hi world hello'
    """
    if not pattern:
        return text
    
    positions = boyer_moore_find_all(text, pattern, case_sensitive)
    
    if count > 0:
        positions = positions[:count]
    
    if not positions:
        return text
    
    result = []
    last_end = 0
    pattern_len = len(pattern)
    
    # 处理大小写敏感替换
    search_pattern = pattern if case_sensitive else pattern.lower()
    
    for pos in positions:
        result.append(text[last_end:pos])
        result.append(replacement)
        last_end = pos + pattern_len
    
    result.append(text[last_end:])
    
    return ''.join(result)


# ==================== 搜索结果详情 ====================

class SearchResult:
    """搜索结果对象"""
    
    def __init__(self, position: int, matched: str, 
                 context_before: str = "", context_after: str = ""):
        self.position = position
        self.matched = matched
        self.context_before = context_before
        self.context_after = context_after
    
    @property
    def start(self) -> int:
        return self.position
    
    @property
    def end(self) -> int:
        return self.position + len(self.matched)
    
    def __repr__(self) -> str:
        return f"SearchResult(position={self.position}, matched='{self.matched}')"
    
    def to_dict(self) -> Dict:
        return {
            'position': self.position,
            'start': self.start,
            'end': self.end,
            'matched': self.matched,
            'context_before': self.context_before,
            'context_after': self.context_after
        }


def boyer_moore_find_with_context(text: str, pattern: str,
                                   context_len: int = 20,
                                   case_sensitive: bool = True,
                                   start: int = 0,
                                   end: Optional[int] = None) -> List[SearchResult]:
    """查找所有匹配并返回包含上下文的详细信息
    
    Args:
        text: 被搜索的文本
        pattern: 要搜索的模式
        context_len: 上下文长度（前后各取的字符数）
        case_sensitive: 是否区分大小写
        start: 搜索起始位置
        end: 搜索结束位置
    
    Returns:
        SearchResult 对象列表
    
    Examples:
        >>> results = boyer_moore_find_with_context("Hello world, hello universe", "hello")
        >>> results[0].context_before
        ''
        >>> results[1].context_before
        'Hello world, '
    """
    positions = boyer_moore_find_all(text, pattern, case_sensitive, start, end)
    results = []
    pattern_len = len(pattern) if pattern else 0
    
    for pos in positions:
        context_start = max(0, pos - context_len)
        context_end = min(len(text), pos + pattern_len + context_len)
        
        result = SearchResult(
            position=pos,
            matched=text[pos:pos + pattern_len] if pattern else "",
            context_before=text[context_start:pos],
            context_after=text[pos + pattern_len:context_end]
        )
        results.append(result)
    
    return results


# ==================== 多模式搜索 ====================

def boyer_moore_multi_search(text: str, patterns: List[str],
                              case_sensitive: bool = True) -> Dict[str, List[int]]:
    """在文本中搜索多个模式
    
    对每个模式使用 Boyer-Moore 算法进行搜索。
    
    Args:
        text: 被搜索的文本
        patterns: 要搜索的模式列表
        case_sensitive: 是否区分大小写
    
    Returns:
        字典，键为模式，值为该模式所有出现位置的列表
    
    Examples:
        >>> boyer_moore_multi_search("hello world, hello universe", ["hello", "world"])
        {'hello': [0, 13], 'world': [6]}
    """
    results = {}
    for pattern in patterns:
        results[pattern] = boyer_moore_find_all(text, pattern, case_sensitive)
    return results


def boyer_moore_multi_find_first(text: str, patterns: List[str],
                                  case_sensitive: bool = True) -> Tuple[Optional[str], int]:
    """查找多个模式中最早出现的那个
    
    Args:
        text: 被搜索的文本
        patterns: 要搜索的模式列表
        case_sensitive: 是否区分大小写
    
    Returns:
        (模式, 位置) 元组，如果都没找到则返回 (None, -1)
    
    Examples:
        >>> boyer_moore_multi_find_first("hello world", ["world", "hello"])
        ('hello', 0)
        >>> boyer_moore_multi_find_first("hello world", ["xyz", "abc"])
        (None, -1)
    """
    first_pattern = None
    first_position = -1
    
    for pattern in patterns:
        pos = boyer_moore_search(text, pattern, case_sensitive)
        if pos != -1:
            if first_position == -1 or pos < first_position:
                first_pattern = pattern
                first_position = pos
    
    return (first_pattern, first_position)


# ==================== 性能分析工具 ====================

class SearchStats:
    """搜索统计信息"""
    
    def __init__(self):
        self.algorithm = "Boyer-Moore"
        self.text_length = 0
        self.pattern_length = 0
        self.comparisons = 0
        self.skips = 0
        self.matches = 0
        self.execution_time_ms = 0.0
    
    def __repr__(self) -> str:
        return (f"SearchStats(algorithm='{self.algorithm}', "
                f"text_length={self.text_length}, pattern_length={self.pattern_length}, "
                f"comparisons={self.comparisons}, skips={self.skips}, "
                f"matches={self.matches}, time={self.execution_time_ms:.3f}ms)")
    
    def to_dict(self) -> Dict:
        return {
            'algorithm': self.algorithm,
            'text_length': self.text_length,
            'pattern_length': self.pattern_length,
            'comparisons': self.comparisons,
            'skips': self.skips,
            'matches': self.matches,
            'execution_time_ms': self.execution_time_ms
        }
    
    @property
    def efficiency(self) -> float:
        """计算搜索效率（跳过次数/总扫描）"""
        if self.text_length == 0:
            return 0.0
        return self.skips / self.text_length


def boyer_moore_search_with_stats(text: str, pattern: str,
                                   case_sensitive: bool = True) -> Tuple[int, SearchStats]:
    """搜索并返回详细统计信息
    
    Args:
        text: 被搜索的文本
        pattern: 要搜索的模式
        case_sensitive: 是否区分大小写
    
    Returns:
        (位置, 统计信息) 元组
    
    Examples:
        >>> pos, stats = boyer_moore_search_with_stats("hello world", "world")
        >>> stats.algorithm
        'Boyer-Moore'
    """
    import time
    
    stats = SearchStats()
    start_time = time.perf_counter()
    
    if not pattern:
        stats.text_length = len(text)
        stats.pattern_length = 0
        stats.execution_time_ms = 0.0
        return (0, stats)
    
    search_text = text if case_sensitive else text.lower()
    search_pattern = pattern if case_sensitive else pattern.lower()
    
    stats.text_length = len(search_text)
    stats.pattern_length = len(search_pattern)
    
    if stats.pattern_length > stats.text_length:
        stats.execution_time_ms = (time.perf_counter() - start_time) * 1000
        return (-1, stats)
    
    # 构建跳跃表
    bad_char = _build_bad_char_table(search_pattern)
    good_suffix = _build_full_good_suffix_table(search_pattern)
    
    pattern_len = stats.pattern_length
    text_len = stats.text_length
    pos = -1
    
    i = 0
    while i <= text_len - pattern_len:
        stats.skips += 1
        
        j = pattern_len - 1
        while j >= 0:
            stats.comparisons += 1
            if search_text[i + j] != search_pattern[j]:
                break
            j -= 1
        
        if j < 0:
            pos = i
            stats.matches += 1
            break
        
        bad_char_skip = bad_char.get(search_text[i + j], pattern_len)
        bad_char_skip = max(1, bad_char_skip - (pattern_len - 1 - j))
        good_suffix_skip = good_suffix[j] if j < len(good_suffix) else 1
        
        i += max(bad_char_skip, good_suffix_skip)
    
    stats.execution_time_ms = (time.perf_counter() - start_time) * 1000
    return (pos, stats)


def compare_with_naive(text: str, pattern: str) -> Dict[str, SearchStats]:
    """比较 Boyer-Moore 与朴素搜索的性能
    
    Args:
        text: 被搜索的文本
        pattern: 要搜索的模式
    
    Returns:
        包含两种算法统计信息的字典
    
    Examples:
        >>> result = compare_with_naive("hello world", "world")
        >>> 'boyer_moore' in result and 'naive' in result
        True
    """
    import time
    
    # Boyer-Moore 搜索
    bm_pos, bm_stats = boyer_moore_search_with_stats(text, pattern)
    bm_stats.algorithm = "Boyer-Moore"
    
    # 朴素搜索
    naive_stats = SearchStats()
    naive_stats.algorithm = "Naive"
    naive_stats.text_length = len(text)
    naive_stats.pattern_length = len(pattern)
    
    start_time = time.perf_counter()
    
    naive_pos = -1
    if pattern:
        for i in range(len(text) - len(pattern) + 1):
            match = True
            for j in range(len(pattern)):
                naive_stats.comparisons += 1
                if text[i + j] != pattern[j]:
                    match = False
                    break
            if match:
                naive_pos = i
                naive_stats.matches += 1
                break
    else:
        naive_pos = 0
    
    naive_stats.execution_time_ms = (time.perf_counter() - start_time) * 1000
    
    return {
        'boyer_moore': bm_stats,
        'naive': naive_stats
    }


# ==================== 便捷函数 ====================

def search(text: str, pattern: str, case_sensitive: bool = True) -> int:
    """boyer_moore_search 的简写形式
    
    Args:
        text: 被搜索的文本
        pattern: 要搜索的模式
        case_sensitive: 是否区分大小写
    
    Returns:
        模式首次出现的索引位置
    """
    return boyer_moore_search(text, pattern, case_sensitive)


def find_all(text: str, pattern: str, case_sensitive: bool = True) -> List[int]:
    """boyer_moore_find_all 的简写形式
    
    Args:
        text: 被搜索的文本
        pattern: 要搜索的模式
        case_sensitive: 是否区分大小写
    
    Returns:
        所有匹配位置的列表
    """
    return boyer_moore_find_all(text, pattern, case_sensitive)


def contains(text: str, pattern: str, case_sensitive: bool = True) -> bool:
    """检查文本是否包含模式
    
    Args:
        text: 被搜索的文本
        pattern: 要搜索的模式
        case_sensitive: 是否区分大小写
    
    Returns:
        是否包含模式
    
    Examples:
        >>> contains("hello world", "world")
        True
        >>> contains("hello world", "WORLD", case_sensitive=False)
        True
    """
    return boyer_moore_search(text, pattern, case_sensitive) != -1


def starts_with(text: str, pattern: str, case_sensitive: bool = True) -> bool:
    """检查文本是否以模式开头
    
    Args:
        text: 被搜索的文本
        pattern: 要搜索的模式
        case_sensitive: 是否区分大小写
    
    Returns:
        是否以模式开头
    
    Examples:
        >>> starts_with("hello world", "hello")
        True
        >>> starts_with("hello world", "world")
        False
    """
    if not pattern:
        return True
    pos = boyer_moore_search(text, pattern, case_sensitive, 0, len(pattern))
    return pos == 0


def ends_with(text: str, pattern: str, case_sensitive: bool = True) -> bool:
    """检查文本是否以模式结尾
    
    Args:
        text: 被搜索的文本
        pattern: 要搜索的模式
        case_sensitive: 是否区分大小写
    
    Returns:
        是否以模式结尾
    
    Examples:
        >>> ends_with("hello world", "world")
        True
        >>> ends_with("hello world", "hello")
        False
    """
    if not pattern:
        return True
    if len(pattern) > len(text):
        return False
    start_pos = len(text) - len(pattern)
    pos = boyer_moore_search(text, pattern, case_sensitive, start_pos)
    return pos == start_pos


# ==================== 导出 ====================

__all__ = [
    # 核心搜索函数
    'boyer_moore_search',
    'boyer_moore_find_all',
    'boyer_moore_count',
    'boyer_moore_replace',
    
    # 搜索结果详情
    'SearchResult',
    'boyer_moore_find_with_context',
    
    # 多模式搜索
    'boyer_moore_multi_search',
    'boyer_moore_multi_find_first',
    
    # 性能分析
    'SearchStats',
    'boyer_moore_search_with_stats',
    'compare_with_naive',
    
    # 便捷函数
    'search',
    'find_all',
    'contains',
    'starts_with',
    'ends_with',
]


if __name__ == "__main__":
    # 简单演示
    text = "The quick brown fox jumps over the lazy dog. The fox was very quick."
    pattern = "fox"
    
    print(f"文本: {text}")
    print(f"模式: {pattern}")
    print(f"首次出现位置: {boyer_moore_search(text, pattern)}")
    print(f"所有位置: {boyer_moore_find_all(text, pattern)}")
    print(f"出现次数: {boyer_moore_count(text, pattern)}")
    print(f"替换后: {boyer_moore_replace(text, pattern, 'cat')}")
    
    # 性能对比
    stats = compare_with_naive(text, pattern)
    print(f"\n性能对比:")
    print(f"  Boyer-Moore: {stats['boyer_moore'].comparisons} 次比较")
    print(f"  朴素搜索: {stats['naive'].comparisons} 次比较")