#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Levenshtein Utils - 编辑距离工具模块
=====================================
提供 Levenshtein 编辑距离及相关字符串相似度计算功能。
零外部依赖，仅使用 Python 标准库。

主要功能:
- Levenshtein 距离计算（经典动态规划）
- 优化距离算法（空间优化、限制阈值）
- 相似度比率计算（0-1 范围）
- 相似字符串搜索（模糊匹配）
- 编辑序列回溯（具体操作步骤）
- Damerau-Levenshtein 距离（含相邻交换）
- 最长公共子序列（LCS）
- 批量相似度计算

作者: AllToolkit
日期: 2026-05-20
"""

from typing import List, Tuple, Optional, Callable, Dict, Any
from dataclasses import dataclass
from enum import Enum


class EditOperation(Enum):
    """编辑操作类型"""
    INSERT = "insert"
    DELETE = "delete"
    REPLACE = "replace"
    MATCH = "match"
    TRANSPOSE = "transpose"  # Damerau-Levenshtein 特有


@dataclass
class EditStep:
    """单步编辑操作"""
    operation: EditOperation
    position: int           # 在源字符串中的位置
    source_char: Optional[str] = None   # 源字符（删除、替换时有）
    target_char: Optional[str] = None   # 目标字符（插入、替换时有）
    
    def describe(self) -> str:
        """描述编辑操作"""
        if self.operation == EditOperation.MATCH:
            return f"保持 '{self.source_char}' 在位置 {self.position}"
        elif self.operation == EditOperation.INSERT:
            return f"在位置 {self.position} 插入 '{self.target_char}'"
        elif self.operation == EditOperation.DELETE:
            return f"删除位置 {self.position} 的 '{self.source_char}'"
        elif self.operation == EditOperation.REPLACE:
            return f"将位置 {self.position} 的 '{self.source_char}' 替换为 '{self.target_char}'"
        elif self.operation == EditOperation.TRANSPOSE:
            return f"交换位置 {self.position} 和 {self.position + 1} 的字符"
        return "未知操作"


@dataclass
class SimilarityResult:
    """相似度计算结果"""
    distance: int          # 编辑距离
    max_length: int        # 较长字符串长度
    similarity: float      # 相似度 (0-1)
    ratio: float           # 比率 (distance / max_length)
    
    def is_similar(self, threshold: float = 0.8) -> bool:
        """判断是否相似"""
        return self.similarity >= threshold


# ==================== 基础 Levenshtein 距离 ====================

def levenshtein_distance(s1: str, s2: str) -> int:
    """
    计算两个字符串的 Levenshtein 编辑距离
    
    经典动态规划实现，时间复杂度 O(m*n)，空间复杂度 O(m*n)
    
    Args:
        s1: 源字符串
        s2: 目标字符串
    
    Returns:
        编辑距离（将 s1 转换为 s2 所需的最少操作数）
    
    Examples:
        >>> levenshtein_distance("kitten", "sitting")
        3
        >>> levenshtein_distance("", "abc")
        3
        >>> levenshtein_distance("hello", "hello")
        0
    """
    m, n = len(s1), len(s2)
    
    # 空字符串处理
    if m == 0:
        return n
    if n == 0:
        return m
    
    # 创建 DP 表
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # 初始化边界
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    # 填充 DP 表
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # 删除
                    dp[i][j - 1],      # 插入
                    dp[i - 1][j - 1]   # 替换
                )
    
    return dp[m][n]


def levenshtein_distance_optimized(s1: str, s2: str) -> int:
    """
    空间优化版 Levenshtein 距离计算
    
    仅使用两行空间，空间复杂度 O(min(m, n))
    
    Args:
        s1: 源字符串
        s2: 目标字符串
    
    Returns:
        编辑距离
    
    Examples:
        >>> levenshtein_distance_optimized("kitten", "sitting")
        3
    """
    # 确保 s1 是较短的字符串
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    
    m, n = len(s1), len(s2)
    
    if m == 0:
        return n
    
    # 使用两行
    prev = list(range(m + 1))
    curr = [0] * (m + 1)
    
    for j in range(1, n + 1):
        curr[0] = j
        for i in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                curr[i] = prev[i - 1]
            else:
                curr[i] = 1 + min(
                    prev[i],      # 插入（从 s2 视角）
                    curr[i - 1],  # 删除
                    prev[i - 1]   # 替换
                )
        prev, curr = curr, prev
    
    return prev[m]


def levenshtein_distance_threshold(s1: str, s2: str, threshold: int) -> int:
    """
    带阈值的 Levenshtein 距离计算
    
    如果距离超过阈值，提前终止并返回阈值+1
    
    Args:
        s1: 源字符串
        s2: 目标字符串
        threshold: 最大允许距离
    
    Returns:
        编辑距离（如果超过阈值，返回 threshold + 1）
    
    Examples:
        >>> levenshtein_distance_threshold("hello", "hallo", 2)
        1
        >>> levenshtein_distance_threshold("hello", "world", 2)
        3  # 超过阈值，返回 3 (threshold + 1)
    """
    m, n = len(s1), len(s2)
    
    # 长度差异超过阈值，直接返回
    if abs(m - n) > threshold:
        return threshold + 1
    
    if m == 0:
        return n if n <= threshold else threshold + 1
    if n == 0:
        return m if m <= threshold else threshold + 1
    
    # 空间优化 + 阈值剪枝
    prev = list(range(m + 1))
    
    for j in range(1, n + 1):
        curr = [j] + [0] * m
        min_val = j
        
        for i in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                curr[i] = prev[i - 1]
            else:
                curr[i] = 1 + min(prev[i], curr[i - 1], prev[i - 1])
            
            min_val = min(min_val, curr[i])
        
        # 如果当前行最小值超过阈值，提前终止
        if min_val > threshold:
            return threshold + 1
        
        prev = curr
    
    return prev[m] if prev[m] <= threshold else threshold + 1


# ==================== 相似度计算 ====================

def similarity_ratio(s1: str, s2: str) -> float:
    """
    计算两个字符串的相似度比率
    
    基于编辑距离计算，返回 0-1 范围的相似度
    
    Args:
        s1: 源字符串
        s2: 目标字符串
    
    Returns:
        相似度（1 表示完全相同，0 表示完全不同）
    
    Examples:
        >>> similarity_ratio("hello", "hello")
        1.0
        >>> similarity_ratio("kitten", "sitting")
        0.571...
    """
    if not s1 and not s2:
        return 1.0
    
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 1.0
    
    distance = levenshtein_distance_optimized(s1, s2)
    return 1.0 - (distance / max_len)


def similarity_result(s1: str, s2: str) -> SimilarityResult:
    """
    计算完整的相似度结果
    
    Args:
        s1: 源字符串
        s2: 目标字符串
    
    Returns:
        SimilarityResult 对象，包含距离、相似度等信息
    
    Examples:
        >>> result = similarity_result("kitten", "sitting")
        >>> result.distance
        3
        >>> result.similarity
        0.571...
    """
    distance = levenshtein_distance_optimized(s1, s2)
    max_len = max(len(s1), len(s2))
    
    if max_len == 0:
        similarity = 1.0
        ratio = 0.0
    else:
        similarity = 1.0 - (distance / max_len)
        ratio = distance / max_len
    
    return SimilarityResult(
        distance=distance,
        max_length=max_len,
        similarity=similarity,
        ratio=ratio
    )


def jaro_similarity(s1: str, s2: str) -> float:
    """
    计算 Jaro 相似度
    
    一种更宽松的字符串相似度度量，适合姓名匹配等场景
    
    Args:
        s1: 源字符串
        s2: 目标字符串
    
    Returns:
        Jaro 相似度 (0-1)
    
    Examples:
        >>> jaro_similarity("MARTHA", "MARHTA")
        0.944...
    """
    m, n = len(s1), len(s2)
    
    if m == 0 and n == 0:
        return 1.0
    if m == 0 or n == 0:
        return 0.0
    
    # 匹配窗口大小
    match_distance = max(m, n) // 2 - 1
    if match_distance < 0:
        match_distance = 0
    
    s1_matches = [False] * m
    s2_matches = [False] * n
    
    matches = 0
    transpositions = 0
    
    # 查找匹配字符
    for i in range(m):
        start = max(0, i - match_distance)
        end = min(i + match_distance + 1, n)
        
        for j in range(start, end):
            if s2_matches[j] or s1[i] != s2[j]:
                continue
            s1_matches[i] = True
            s2_matches[j] = True
            matches += 1
            break
    
    if matches == 0:
        return 0.0
    
    # 计算转置
    k = 0
    for i in range(m):
        if not s1_matches[i]:
            continue
        while not s2_matches[k]:
            k += 1
        if s1[i] != s2[k]:
            transpositions += 1
        k += 1
    
    jaro = (matches / m + matches / n + 
            (matches - transpositions / 2) / matches) / 3
    
    return jaro


def jaro_winkler_similarity(s1: str, s2: str, 
                            prefix_scale: float = 0.1) -> float:
    """
    计算 Jaro-Winkler 相似度
    
    Jaro 的改进版本，对公共前缀给予更高权重
    
    Args:
        s1: 源字符串
        s2: 目标字符串
        prefix_scale: 前缀权重因子（默认 0.1，最大 0.25）
    
    Returns:
        Jaro-Winkler 相似度 (0-1)
    
    Examples:
        >>> jaro_winkler_similarity("MARTHA", "MARHTA")
        0.961...
    """
    jaro = jaro_similarity(s1, s2)
    
    # 计算公共前缀长度（最多 4 个字符）
    prefix_len = 0
    for i in range(min(len(s1), len(s2), 4)):
        if s1[i] == s2[i]:
            prefix_len += 1
        else:
            break
    
    # 限制 prefix_scale
    prefix_scale = min(prefix_scale, 0.25)
    
    return jaro + prefix_len * prefix_scale * (1 - jaro)


# ==================== 编辑序列回溯 ====================

def levenshtein_operations(s1: str, s2: str) -> List[EditStep]:
    """
    获取将 s1 转换为 s2 的编辑操作序列
    
    Args:
        s1: 源字符串
        s2: 目标字符串
    
    Returns:
        编辑操作步骤列表
    
    Examples:
        >>> ops = levenshtein_operations("kitten", "sitting")
        >>> [op.operation for op in ops[:3]]
        [<EditOperation.REPLACE: 'replace'>, ...]
    """
    m, n = len(s1), len(s2)
    
    # 特殊情况处理
    if m == 0:
        return [EditStep(EditOperation.INSERT, 0, None, c) for c in s2]
    if n == 0:
        return [EditStep(EditOperation.DELETE, i, s1[i], None) for i in range(m)]
    
    # 创建 DP 表
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    
    # 回溯
    operations: List[EditStep] = []
    i, j = m, n
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and s1[i - 1] == s2[j - 1]:
            operations.append(EditStep(EditOperation.MATCH, i - 1, s1[i - 1], s2[j - 1]))
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            operations.append(EditStep(EditOperation.REPLACE, i - 1, s1[i - 1], s2[j - 1]))
            i -= 1
            j -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + 1:
            operations.append(EditStep(EditOperation.INSERT, i, None, s2[j - 1]))
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            operations.append(EditStep(EditOperation.DELETE, i - 1, s1[i - 1], None))
            i -= 1
    
    operations.reverse()
    return operations


def apply_operations(s1: str, operations: List[EditStep]) -> str:
    """
    将编辑操作应用到字符串
    
    Args:
        s1: 源字符串
        operations: 编辑操作列表
    
    Returns:
        转换后的字符串
    
    Examples:
        >>> ops = levenshtein_operations("kitten", "sitting")
        >>> apply_operations("kitten", ops)
        'sitting'
    """
    result = list(s1)
    offset = 0
    
    for op in operations:
        pos = op.position + offset
        
        if op.operation == EditOperation.INSERT:
            result.insert(pos, op.target_char)
            offset += 1
        elif op.operation == EditOperation.DELETE:
            if pos < len(result):
                result.pop(pos)
                offset -= 1
        elif op.operation == EditOperation.REPLACE:
            if pos < len(result):
                result[pos] = op.target_char
    
    return ''.join(result)


# ==================== Damerau-Levenshtein 距离 ====================

def damerau_levenshtein_distance(s1: str, s2: str) -> int:
    """
    计算 Damerau-Levenshtein 距离
    
    在 Levenshtein 基础上增加了相邻字符交换操作
    
    Args:
        s1: 源字符串
        s2: 目标字符串
    
    Returns:
        Damerau-Levenshtein 距离
    
    Examples:
        >>> damerau_levenshtein_distance("ab", "ba")
        1  # 只需交换一次
        >>> levenshtein_distance("ab", "ba")
        2  # 普通算法需要两次替换
    """
    m, n = len(s1), len(s2)
    
    if m == 0:
        return n
    if n == 0:
        return m
    
    # 创建 DP 表
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # 删除
                    dp[i][j - 1],      # 插入
                    dp[i - 1][j - 1]   # 替换
                )
            
            # 相邻交换
            if (i > 1 and j > 1 and 
                s1[i - 1] == s2[j - 2] and 
                s1[i - 2] == s2[j - 1]):
                dp[i][j] = min(dp[i][j], dp[i - 2][j - 2] + 1)
    
    return dp[m][n]


# ==================== 最长公共子序列 (LCS) ====================

def longest_common_subsequence(s1: str, s2: str) -> str:
    """
    计算两个字符串的最长公共子序列
    
    Args:
        s1: 源字符串
        s2: 目标字符串
    
    Returns:
        最长公共子序列
    
    Examples:
        >>> longest_common_subsequence("ABCBDAB", "BDCABA")
        'BCBA'
    """
    m, n = len(s1), len(s2)
    
    if m == 0 or n == 0:
        return ""
    
    # DP 表
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # 填充
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # 回溯
    lcs = []
    i, j = m, n
    
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            lcs.append(s1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    
    return ''.join(reversed(lcs))


def lcs_length(s1: str, s2: str) -> int:
    """
    计算最长公共子序列的长度（空间优化版）
    
    Args:
        s1: 源字符串
        s2: 目标字符串
    
    Returns:
        LCS 长度
    
    Examples:
        >>> lcs_length("ABCBDAB", "BDCABA")
        4
    """
    m, n = len(s1), len(s2)
    
    if m == 0 or n == 0:
        return 0
    
    # 使用两行
    prev = [0] * (n + 1)
    curr = [0] * (n + 1)
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev, curr = curr, prev
    
    return prev[n]


# ==================== 模糊匹配搜索 ====================

def find_similar(query: str, candidates: List[str], 
                 threshold: float = 0.6,
                 limit: int = 10) -> List[Tuple[str, float]]:
    """
    在候选列表中查找相似字符串
    
    Args:
        query: 查询字符串
        candidates: 候选字符串列表
        threshold: 相似度阈值（0-1）
        limit: 返回结果数量限制
    
    Returns:
        [(字符串, 相似度), ...] 按相似度降序排列
    
    Examples:
        >>> find_similar("hello", ["hallo", "helloo", "world", "hell"], 0.5)
        [('helloo', 0.888...), ('hallo', 0.8), ('hell', 0.8)]
    """
    results: List[Tuple[str, float]] = []
    
    for candidate in candidates:
        sim = similarity_ratio(query, candidate)
        if sim >= threshold:
            results.append((candidate, sim))
    
    # 按相似度降序排列
    results.sort(key=lambda x: x[1], reverse=True)
    
    return results[:limit]


def find_nearest(query: str, candidates: List[str]) -> Tuple[str, int]:
    """
    查找编辑距离最近的字符串
    
    Args:
        query: 查询字符串
        candidates: 候选字符串列表
    
    Returns:
        (最近字符串, 编辑距离)
    
    Examples:
        >>> find_nearest("hello", ["hallo", "world", "help"])
        ('hallo', 1)
    """
    if not candidates:
        return "", len(query)
    
    best = candidates[0]
    best_dist = levenshtein_distance_optimized(query, best)
    
    for candidate in candidates[1:]:
        dist = levenshtein_distance_optimized(query, candidate)
        if dist < best_dist:
            best = candidate
            best_dist = dist
    
    return best, best_dist


def fuzzy_search(query: str, text: str, 
                 max_distance: int = 2) -> List[Tuple[int, int, str]]:
    """
    在文本中模糊搜索字符串
    
    Args:
        query: 查询字符串
        text: 被搜索文本
        max_distance: 最大允许编辑距离
    
    Returns:
        [(起始位置, 编辑距离, 匹配子串), ...]
    
    Examples:
        >>> fuzzy_search("hello", "hallo world helloo", 2)
        [(0, 1, 'hallo'), (12, 1, 'helloo')]
    """
    results: List[Tuple[int, int, str]] = []
    query_len = len(query)
    
    # 滑动窗口
    for i in range(len(text) - query_len + 1):
        substr = text[i:i + query_len]
        dist = levenshtein_distance_threshold(query, substr, max_distance)
        
        if dist <= max_distance:
            results.append((i, dist, substr))
    
    # 扩展搜索（查询长度 ±max_distance）
    for delta in range(1, max_distance + 1):
        for i in range(len(text) - query_len - delta + 1):
            substr = text[i:i + query_len + delta]
            dist = levenshtein_distance_threshold(query, substr, max_distance)
            if dist <= max_distance:
                results.append((i, dist, substr))
        
        for i in range(len(text) - query_len + delta + 1):
            substr = text[i:i + query_len - delta]
            if len(substr) > 0:
                dist = levenshtein_distance_threshold(query, substr, max_distance)
                if dist <= max_distance:
                    results.append((i, dist, substr))
    
    # 去重并排序
    seen = set()
    unique_results = []
    for r in results:
        if r[0] not in seen:
            seen.add(r[0])
            unique_results.append(r)
    
    return sorted(unique_results, key=lambda x: (x[1], x[0]))


# ==================== 批量计算 ====================

def batch_similarity(pairs: List[Tuple[str, str]]) -> List[float]:
    """
    批量计算相似度
    
    Args:
        pairs: 字符串对列表
    
    Returns:
        相似度列表
    
    Examples:
        >>> batch_similarity([("hello", "hallo"), ("world", "word")])
        [0.8, 0.8]
    """
    return [similarity_ratio(s1, s2) for s1, s2 in pairs]


def batch_distance(pairs: List[Tuple[str, str]]) -> List[int]:
    """
    批量计算编辑距离
    
    Args:
        pairs: 字符串对列表
    
    Returns:
        编辑距离列表
    
    Examples:
        >>> batch_distance([("kitten", "sitting"), ("hello", "hello")])
        [3, 0]
    """
    return [levenshtein_distance_optimized(s1, s2) for s1, s2 in pairs]


def similarity_matrix(strings: List[str]) -> List[List[float]]:
    """
    计算字符串列表的相似度矩阵
    
    Args:
        strings: 字符串列表
    
    Returns:
        N x N 相似度矩阵
    
    Examples:
        >>> similarity_matrix(["hello", "hallo", "world"])
        [[1.0, 0.8, 0.2], [0.8, 1.0, 0.2], [0.2, 0.2, 1.0]]
    """
    n = len(strings)
    matrix = [[0.0] * n for _ in range(n)]
    
    for i in range(n):
        matrix[i][i] = 1.0
        for j in range(i + 1, n):
            sim = similarity_ratio(strings[i], strings[j])
            matrix[i][j] = sim
            matrix[j][i] = sim
    
    return matrix


# ==================== 工具函数 ====================

def normalized_levenshtein(s1: str, s2: str) -> float:
    """
    归一化 Levenshtein 距离（0-1 范围）
    
    0 表示完全相同，1 表示完全不同
    
    Args:
        s1: 源字符串
        s2: 目标字符串
    
    Returns:
        归一化距离
    
    Examples:
        >>> normalized_levenshtein("hello", "hello")
        0.0
        >>> normalized_levenshtein("", "hello")
        1.0
    """
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 0.0
    
    return levenshtein_distance_optimized(s1, s2) / max_len


def hamming_distance(s1: str, s2: str) -> int:
    """
    计算汉明距离（仅适用于等长字符串）
    
    Args:
        s1: 源字符串
        s2: 目标字符串
    
    Returns:
        汉明距离
    
    Raises:
        ValueError: 如果字符串长度不等
    
    Examples:
        >>> hamming_distance("karolin", "kathrin")
        3
    """
    if len(s1) != len(s2):
        raise ValueError("汉明距离要求字符串长度相等")
    
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))


def is_one_edit_away(s1: str, s2: str) -> bool:
    """
    判断两个字符串是否只差一次编辑
    
    Args:
        s1: 源字符串
        s2: 目标字符串
    
    Returns:
        是否只差一次编辑
    
    Examples:
        >>> is_one_edit_away("hello", "hallo")
        True
        >>> is_one_edit_away("hello", "helo")
        True
        >>> is_one_edit_away("hello", "world")
        False
    """
    m, n = len(s1), len(s2)
    
    # 长度差超过 1
    if abs(m - n) > 1:
        return False
    
    # 使用阈值优化
    return levenshtein_distance_threshold(s1, s2, 1) <= 1


def spell_check_suggestions(word: str, dictionary: List[str], 
                             max_suggestions: int = 5,
                             max_distance: int = 2) -> List[Tuple[str, int]]:
    """
    拼写检查建议
    
    Args:
        word: 待检查单词
        dictionary: 词典列表
        max_suggestions: 最大建议数
        max_distance: 最大编辑距离
    
    Returns:
        [(建议词, 编辑距离), ...]
    
    Examples:
        >>> spell_check_suggestions("helo", ["hello", "help", "held", "hero"])
        [('hello', 1), ('help', 1), ('held', 1)]
    """
    candidates: List[Tuple[str, int]] = []
    
    for dict_word in dictionary:
        dist = levenshtein_distance_threshold(word, dict_word, max_distance)
        if dist <= max_distance:
            candidates.append((dict_word, dist))
    
    # 按距离排序
    candidates.sort(key=lambda x: x[1])
    
    return candidates[:max_suggestions]


def align_strings(s1: str, s2: str, 
                  gap_char: str = '-') -> Tuple[str, str]:
    """
    字符串对齐（基于编辑距离）
    
    Args:
        s1: 源字符串
        s2: 目标字符串
        gap_char: 填充字符
    
    Returns:
        (对齐后的 s1, 对齐后的 s2)
    
    Examples:
        >>> align_strings("kitten", "sitting")
        ('kitten--', 'sitting')
    """
    m, n = len(s1), len(s2)
    
    if m == 0:
        return gap_char * n, s2
    if n == 0:
        return s1, gap_char * m
    
    # DP 表
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    
    # 回溯构建对齐
    aligned1: List[str] = []
    aligned2: List[str] = []
    i, j = m, n
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and s1[i - 1] == s2[j - 1]:
            aligned1.append(s1[i - 1])
            aligned2.append(s2[j - 1])
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            aligned1.append(s1[i - 1])
            aligned2.append(s2[j - 1])
            i -= 1
            j -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + 1:
            aligned1.append(gap_char)
            aligned2.append(s2[j - 1])
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            aligned1.append(s1[i - 1])
            aligned2.append(gap_char)
            i -= 1
    
    return ''.join(reversed(aligned1)), ''.join(reversed(aligned2))


if __name__ == "__main__":
    print("Levenshtein Utils 演示")
    print("=" * 50)
    
    # 基础距离计算
    print("\n1. 基础 Levenshtein 距离:")
    s1, s2 = "kitten", "sitting"
    dist = levenshtein_distance(s1, s2)
    print(f"   '{s1}' -> '{s2}': {dist}")
    
    # 相似度
    print("\n2. 相似度计算:")
    sim = similarity_ratio(s1, s2)
    print(f"   相似度: {sim:.4f}")
    
    # Jaro-Winkler
    jw = jaro_winkler_similarity("MARTHA", "MARHTA")
    print(f"   Jaro-Winkler ('MARTHA', 'MARHTA'): {jw:.4f}")
    
    # 编辑操作
    print("\n3. 编辑操作序列:")
    ops = levenshtein_operations("kitten", "sitting")
    for op in ops[:5]:
        print(f"   {op.describe()}")
    
    # 模糊搜索
    print("\n4. 模糊搜索:")
    results = find_similar("hello", ["hallo", "helloo", "world", "hell", "help"], 0.5)
    for word, score in results:
        print(f"   '{word}': {score:.4f}")
    
    # LCS
    print("\n5. 最长公共子序列:")
    lcs = longest_common_subsequence("ABCBDAB", "BDCABA")
    print(f"   LCS('ABCBDAB', 'BDCABA'): '{lcs}'")
    
    # Damerau-Levenshtein
    print("\n6. Damerau-Levenshtein:")
    dl_dist = damerau_levenshtein_distance("ab", "ba")
    l_dist = levenshtein_distance("ab", "ba")
    print(f"   Damerau-Levenshtein('ab', 'ba'): {dl_dist}")
    print(f"   普通 Levenshtein('ab', 'ba'): {l_dist}")
    
    # 对齐
    print("\n7. 字符串对齐:")
    a1, a2 = align_strings("kitten", "sitting")
    print(f"   {a1}")
    print(f"   {a2}")
    
    print("\n" + "=" * 50)
    print("演示完成")