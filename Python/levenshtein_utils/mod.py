"""
Levenshtein Distance Utils - 编辑距离工具
计算字符串相似度的实用工具集，零外部依赖

功能：
- 计算两个字符串之间的编辑距离
- 计算字符串相似度 (0-1)
- 在候选列表中查找最相似的字符串
- 返回编辑距离及编辑操作序列
- 支持自定义替换/插入/删除成本
"""

from typing import List, Tuple, Optional, Union, Callable


def levenshtein_distance(
    s1: str,
    s2: str,
    *,
    insert_cost: float = 1,
    delete_cost: float = 1,
    replace_cost: float = 1
) -> int:
    """
    计算两个字符串之间的 Levenshtein 编辑距离
    
    编辑距离是将 s1 转换为 s2 所需的最少编辑操作次数
    编辑操作包括：插入、删除、替换
    
    Args:
        s1: 源字符串
        s2: 目标字符串
        insert_cost: 插入操作的成本
        delete_cost: 删除操作的成本
        replace_cost: 替换操作的成本
        
    Returns:
        编辑距离
        
    Examples:
        >>> levenshtein_distance("kitten", "sitting")
        3
        >>> levenshtein_distance("", "abc")
        3
        >>> levenshtein_distance("abc", "abc")
        0
    """
    if s1 == s2:
        return 0
    
    len1, len2 = len(s1), len(s2)
    
    # 边界情况
    if len1 == 0:
        return int(len2 * insert_cost)
    if len2 == 0:
        return int(len1 * delete_cost)
    
    # 使用一维数组优化空间复杂度
    # dp[j] 表示 s1[:i] 到 s2[:j] 的编辑距离
    prev = list(range(len2 + 1))
    
    for i in range(1, len1 + 1):
        curr = [i * delete_cost] + [0] * len2
        for j in range(1, len2 + 1):
            if s1[i - 1] == s2[j - 1]:
                # 字符相同，不需要操作
                curr[j] = prev[j - 1]
            else:
                # 选择成本最小的操作
                insert_op = curr[j - 1] + insert_cost
                delete_op = prev[j] + delete_cost
                replace_op = prev[j - 1] + replace_cost
                curr[j] = min(insert_op, delete_op, replace_op)
        prev = curr
    
    return int(prev[len2])


def similarity(s1: str, s2: str) -> float:
    """
    计算两个字符串的相似度 (0-1)
    
    相似度 = 1 - (编辑距离 / 较长字符串的长度)
    
    Args:
        s1: 源字符串
        s2: 目标字符串
        
    Returns:
        相似度，范围 [0, 1]，1 表示完全相同
        
    Examples:
        >>> similarity("kitten", "sitting")
        0.5714285714285714
        >>> similarity("abc", "abc")
        1.0
        >>> similarity("abc", "xyz")
        0.0
    """
    if s1 == s2:
        return 1.0
    
    if not s1 or not s2:
        return 0.0
    
    max_len = max(len(s1), len(s2))
    dist = levenshtein_distance(s1, s2)
    
    return 1.0 - (dist / max_len)


def find_closest(
    target: str,
    candidates: List[str],
    *,
    threshold: float = 0.0,
    return_distance: bool = False
) -> Union[str, Tuple[str, int], Tuple[str, float], None]:
    """
    在候选列表中查找与目标字符串最相似的字符串
    
    Args:
        target: 目标字符串
        candidates: 候选字符串列表
        threshold: 相似度阈值 (0-1)，低于此阈值返回 None
        return_distance: 如果为 True，返回 (匹配字符串, 距离)
                        如果为 False，返回 (匹配字符串, 相似度)
        
    Returns:
        最相似的字符串，或 (字符串, 距离/相似度) 元组
        如果没有满足阈值的匹配，返回 None
        
    Examples:
        >>> find_closest("appel", ["apple", "banana", "orange"])
        'apple'
        >>> find_closest("appel", ["apple", "banana", "orange"], return_distance=True)
        ('apple', 1)
        >>> find_closest("xyz", ["apple", "banana"], threshold=0.5)
        None
    """
    if not candidates:
        return None
    
    best_match = None
    best_distance = float('inf')
    
    for candidate in candidates:
        dist = levenshtein_distance(target, candidate)
        if dist < best_distance:
            best_distance = dist
            best_match = candidate
    
    if threshold > 0:
        sim = similarity(target, best_match) if best_match else 0
        if sim < threshold:
            return None
    
    if return_distance:
        return (best_match, int(best_distance)) if best_match else None
    
    return best_match


def find_all_closest(
    target: str,
    candidates: List[str],
    *,
    top_n: int = 5,
    threshold: float = 0.0
) -> List[Tuple[str, float]]:
    """
    查找所有相似度较高的字符串，按相似度排序
    
    Args:
        target: 目标字符串
        candidates: 候选字符串列表
        top_n: 返回前 N 个最相似的
        threshold: 相似度阈值 (0-1)
        
    Returns:
        [(字符串, 相似度), ...] 列表，按相似度降序排列
        
    Examples:
        >>> find_all_closest("color", ["colour", "color", "colors", "column"], top_n=3)
        [('color', 1.0), ('colour', 0.8333333333333334), ('colors', 0.8)]
    """
    if not candidates:
        return []
    
    results = []
    for candidate in candidates:
        sim = similarity(target, candidate)
        if sim >= threshold:
            results.append((candidate, sim))
    
    # 按相似度降序排序
    results.sort(key=lambda x: x[1], reverse=True)
    
    return results[:top_n]


def edit_sequence(
    s1: str,
    s2: str
) -> Tuple[int, List[Tuple[str, Union[str, int]]]]:
    """
    计算编辑距离并返回编辑操作序列
    
    Args:
        s1: 源字符串
        s2: 目标字符串
        
    Returns:
        (编辑距离, 操作列表)
        操作列表格式:
        - ('equal', (i, j, length)): 相同的字符片段
        - ('replace', (i, char)): 在位置 i 替换字符为 char
        - ('insert', (i, char)): 在位置 i 插入字符 char
        - ('delete', (i, length)): 从位置 i 删除 length 个字符
        
    Examples:
        >>> distance, ops = edit_sequence("kitten", "sitting")
        >>> distance
        3
        >>> ops[0]
        ('replace', (0, 's'))
    """
    len1, len2 = len(s1), len(s2)
    
    # 构建 DP 表
    dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]
    
    for i in range(len1 + 1):
        dp[i][0] = i
    for j in range(len2 + 1):
        dp[0][j] = j
    
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(
                    dp[i - 1][j] + 1,      # 删除
                    dp[i][j - 1] + 1,      # 插入
                    dp[i - 1][j - 1] + 1   # 替换
                )
    
    # 回溯构建操作序列
    operations = []
    i, j = len1, len2
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and s1[i - 1] == s2[j - 1]:
            operations.append(('equal', (i - 1, j - 1, 1)))
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            operations.append(('replace', (i - 1, s2[j - 1])))
            i -= 1
            j -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + 1:
            operations.append(('insert', (i, s2[j - 1])))
            j -= 1
        else:  # i > 0 and dp[i][j] == dp[i - 1][j] + 1
            operations.append(('delete', (i - 1, 1)))
            i -= 1
    
    operations.reverse()
    return dp[len1][len2], operations


def apply_edits(s: str, operations: List[Tuple[str, Union[str, int, Tuple]]]) -> str:
    """
    将编辑操作序列应用到字符串
    
    Args:
        s: 源字符串
        operations: 编辑操作序列
        
    Returns:
        编辑后的字符串
        
    Examples:
        >>> dist, ops = edit_sequence("kitten", "sitting")
        >>> result = apply_edits("kitten", ops)
        >>> result
        'sitting'
    """
    result = list(s)
    offset = 0  # 由于插入/删除导致的偏移量
    
    for op, data in operations:
        if op == 'equal':
            continue
        elif op == 'replace':
            pos, char = data
            result[pos + offset] = char
        elif op == 'insert':
            pos, char = data
            result.insert(pos + offset, char)
            offset += 1
        elif op == 'delete':
            pos, length = data
            for _ in range(length):
                del result[pos + offset]
            offset -= length
    
    return ''.join(result)


def normalized_distance(s1: str, s2: str) -> float:
    """
    计算归一化的编辑距离 (0-1)
    
    归一化距离 = 编辑距离 / (两个字符串长度之和)
    
    Args:
        s1: 源字符串
        s2: 目标字符串
        
    Returns:
        归一化距离，范围 [0, 1]，0 表示完全相同
        
    Examples:
        >>> normalized_distance("abc", "abc")
        0.0
        >>> normalized_distance("", "abc")
        1.0
    """
    if not s1 and not s2:
        return 0.0
    
    max_dist = len(s1) + len(s2)
    if max_dist == 0:
        return 0.0
    
    dist = levenshtein_distance(s1, s2)
    return dist / max_dist


def ratio(s1: str, s2: str) -> float:
    """
    计算两个字符串的匹配比率 (与 fuzzywuzzy 兼容)
    
    ratio = (总长度 - 编辑距离) / 总长度 * 100
    
    Args:
        s1: 源字符串
        s2: 目标字符串
        
    Returns:
        匹配比率，范围 [0, 100]
        
    Examples:
        >>> ratio("hello world", "hello")
        54.54545454545455
    """
    if not s1 and not s2:
        return 100.0
    
    total_len = len(s1) + len(s2)
    dist = levenshtein_distance(s1, s2)
    
    return ((total_len - dist) / total_len) * 100


def hamming_distance(s1: str, s2: str) -> int:
    """
    计算汉明距离（仅适用于等长字符串）
    
    汉明距离是两个等长字符串对应位置不同字符的个数
    
    Args:
        s1: 源字符串
        s2: 目标字符串
        
    Returns:
        汉明距离
        
    Raises:
        ValueError: 如果两个字符串长度不同
        
    Examples:
        >>> hamming_distance("karolin", "kathrin")
        3
        >>> hamming_distance("1011101", "1001001")
        2
    """
    if len(s1) != len(s2):
        raise ValueError("Strings must be of equal length for Hamming distance")
    
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))


def damerau_levenshtein_distance(s1: str, s2: str) -> int:
    """
    计算 Damerau-Levenshtein 距离
    
    在 Levenshtein 距离的基础上，增加了相邻字符交换操作
    
    Args:
        s1: 源字符串
        s2: 目标字符串
        
    Returns:
        Damerau-Levenshtein 距离
        
    Examples:
        >>> damerau_levenshtein_distance("ca", "abc")
        2
        >>> damerau_levenshtein_distance("abcd", "acbd")
        1
    """
    len1, len2 = len(s1), len(s2)
    
    if len1 == 0:
        return len2
    if len2 == 0:
        return len1
    
    # 使用字典存储距离值，避免稀疏数组
    d = {}
    
    for i in range(-1, len1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, len2 + 1):
        d[(-1, j)] = j + 1
    
    for i in range(len1):
        for j in range(len2):
            cost = 0 if s1[i] == s2[j] else 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1,      # 删除
                d[(i, j - 1)] + 1,      # 插入
                d[(i - 1, j - 1)] + cost  # 替换
            )
            
            # 相邻字符交换
            if i > 0 and j > 0 and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[(i - 2, j - 2)] + 1)
    
    return d[(len1 - 1, len2 - 1)]


if __name__ == "__main__":
    # 简单示例
    print("=== Levenshtein Distance Utils Demo ===\n")
    
    # 1. 基本编辑距离
    print("1. 基本编辑距离:")
    words = [
        ("kitten", "sitting"),
        ("book", "back"),
        ("algorithm", "logarithm"),
        ("", "hello"),
        ("python", "python")
    ]
    for w1, w2 in words:
        dist = levenshtein_distance(w1, w2)
        print(f"   '{w1}' -> '{w2}': {dist}")
    
    # 2. 相似度计算
    print("\n2. 相似度计算:")
    for w1, w2 in words:
        sim = similarity(w1, w2)
        print(f"   '{w1}' vs '{w2}': {sim:.2%}")
    
    # 3. 查找最相似字符串
    print("\n3. 查找最相似字符串:")
    target = "appel"
    candidates = ["apple", "application", "applet", "appeal", "applepie"]
    closest = find_closest(target, candidates)
    print(f"   目标: '{target}'")
    print(f"   候选: {candidates}")
    print(f"   最佳匹配: '{closest}'")
    
    # 4. 查找所有相似字符串
    print("\n4. 查找所有相似字符串 (Top 3):")
    results = find_all_closest(target, candidates, top_n=3)
    for word, sim in results:
        print(f"   '{word}': {sim:.2%}")
    
    # 5. 编辑操作序列
    print("\n5. 编辑操作序列:")
    s1, s2 = "kitten", "sitting"
    dist, ops = edit_sequence(s1, s2)
    print(f"   '{s1}' -> '{s2}'")
    print(f"   编辑距离: {dist}")
    print(f"   操作序列:")
    for op, data in ops[:5]:
        print(f"     - {op}: {data}")
    
    # 6. Damerau-Levenshtein 距离
    print("\n6. Damerau-Levenshtein 距离 (支持相邻字符交换):")
    pairs = [("abcd", "acbd"), ("ca", "abc"), ("abcdef", "abcdfe")]
    for w1, w2 in pairs:
        dl_dist = damerau_levenshtein_distance(w1, w2)
        l_dist = levenshtein_distance(w1, w2)
        print(f"   '{w1}' -> '{w2}': DL={dl_dist}, L={l_dist}")
    
    # 7. 匹配比率
    print("\n7. 匹配比率 (fuzzywuzzy 兼容):")
    pairs = [("hello world", "hello"), ("fuzzy string matching", "fuzzy matching")]
    for w1, w2 in pairs:
        r = ratio(w1, w2)
        print(f"   '{w1}' vs '{w2}': {r:.2f}%")
    
    print("\n" + "=" * 40)