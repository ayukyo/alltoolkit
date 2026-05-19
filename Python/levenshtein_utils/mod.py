"""
Levenshtein 距离工具模块
提供编辑距离计算、相似度比较、模糊匹配等功能
零外部依赖，纯 Python 实现
"""

from typing import List, Tuple, Optional, Callable


def levenshtein_distance(s1: str, s2: str) -> int:
    """
    计算两个字符串之间的 Levenshtein 编辑距离
    
    编辑距离是指将一个字符串转换为另一个字符串所需的最少单字符编辑操作次数
    允许的操作包括：插入、删除、替换
    
    Args:
        s1: 第一个字符串
        s2: 第二个字符串
        
    Returns:
        int: 编辑距离值
        
    Examples:
        >>> levenshtein_distance("kitten", "sitting")
        3
        >>> levenshtein_distance("", "abc")
        3
        >>> levenshtein_distance("same", "same")
        0
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # 插入、删除、替换的代价
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def levenshtein_distance_optimized(s1: str, s2: str) -> int:
    """
    优化版的 Levenshtein 距离计算，使用更少的内存
    
    对于长字符串更高效，只保留两行数据
    
    Args:
        s1: 第一个字符串
        s2: 第二个字符串
        
    Returns:
        int: 编辑距离值
    """
    if s1 == s2:
        return 0
    if len(s1) == 0:
        return len(s2)
    if len(s2) == 0:
        return len(s1)
    
    # 使用两个一维数组代替二维矩阵
    v0 = list(range(len(s2) + 1))
    v1 = [0] * (len(s2) + 1)
    
    for i in range(len(s1)):
        v1[0] = i + 1
        for j in range(len(s2)):
            cost = 0 if s1[i] == s2[j] else 1
            v1[j + 1] = min(
                v1[j] + 1,      # 插入
                v0[j + 1] + 1,  # 删除
                v0[j] + cost    # 替换
            )
        v0, v1 = v1, v0
    
    return v0[len(s2)]


def similarity_ratio(s1: str, s2: str) -> float:
    """
    计算两个字符串的相似度比率（0-1之间）
    
    基于 Levenshtein 距离，返回标准化后的相似度
    1.0 表示完全相同，0.0 表示完全不同
    
    Args:
        s1: 第一个字符串
        s2: 第二个字符串
        
    Returns:
        float: 相似度比率 [0.0, 1.0]
        
    Examples:
        >>> similarity_ratio("hello", "hello")
        1.0
        >>> similarity_ratio("hello", "hallo")
        0.8
        >>> similarity_ratio("abc", "xyz")
        0.0
    """
    if not s1 and not s2:
        return 1.0
    
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 1.0
    
    distance = levenshtein_distance(s1, s2)
    return 1.0 - (distance / max_len)


def normalized_levenshtein(s1: str, s2: str) -> float:
    """
    归一化的 Levenshtein 距离（0-1之间）
    
    0.0 表示完全相同，1.0 表示完全不同
    与 similarity_ratio 互补
    
    Args:
        s1: 第一个字符串
        s2: 第二个字符串
        
    Returns:
        float: 归一化距离 [0.0, 1.0]
    """
    return 1.0 - similarity_ratio(s1, s2)


def damerau_levenshtein_distance(s1: str, s2: str) -> int:
    """
    计算 Damerau-Levenshtein 距离
    
    相比标准 Levenshtein 距离，额外允许相邻字符交换操作
    更适合处理打字错误
    
    Args:
        s1: 第一个字符串
        s2: 第二个字符串
        
    Returns:
        int: Damerau-Levenshtein 距离
        
    Examples:
        >>> damerau_levenshtein_distance("ca", "abc")
        2
        >>> damerau_levenshtein_distance("abcd", "acbd")
        1  # 只需交换 b 和 c
    """
    len1, len2 = len(s1), len(s2)
    
    if len1 == 0:
        return len2
    if len2 == 0:
        return len1
    
    # 创建距离矩阵
    d = [[0] * (len2 + 1) for _ in range(len1 + 1)]
    
    for i in range(len1 + 1):
        d[i][0] = i
    for j in range(len2 + 1):
        d[0][j] = j
    
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            d[i][j] = min(
                d[i - 1][j] + 1,      # 删除
                d[i][j - 1] + 1,      # 插入
                d[i - 1][j - 1] + cost  # 替换
            )
            # 相邻字符交换
            if i > 1 and j > 1 and s1[i - 1] == s2[j - 2] and s1[i - 2] == s2[j - 1]:
                d[i][j] = min(d[i][j], d[i - 2][j - 2] + cost)
    
    return d[len1][len2]


def fuzzy_search(
    query: str,
    candidates: List[str],
    threshold: float = 0.6,
    limit: Optional[int] = None
) -> List[Tuple[str, float]]:
    """
    在候选列表中进行模糊搜索
    
    返回相似度超过阈值的候选项，按相似度降序排列
    
    Args:
        query: 查询字符串
        candidates: 候选字符串列表
        threshold: 相似度阈值（默认 0.6）
        limit: 返回结果数量限制（None 表示不限制）
        
    Returns:
        List[Tuple[str, float]]: (候选字符串, 相似度) 元组列表
        
    Examples:
        >>> fuzzy_search("apple", ["apply", "orange", "app", "apple pie"], threshold=0.5)
        [('apple pie', 0.8), ('apply', 0.8), ('app', 0.6)]
    """
    results = []
    for candidate in candidates:
        ratio = similarity_ratio(query, candidate)
        if ratio >= threshold:
            results.append((candidate, ratio))
    
    # 按相似度降序排序
    results.sort(key=lambda x: x[1], reverse=True)
    
    if limit:
        results = results[:limit]
    
    return results


def fuzzy_match_one(
    query: str,
    candidates: List[str],
    threshold: float = 0.6
) -> Optional[Tuple[str, float]]:
    """
    查找最佳模糊匹配项
    
    Args:
        query: 查询字符串
        candidates: 候选字符串列表
        threshold: 相似度阈值
        
    Returns:
        Optional[Tuple[str, float]]: 最佳匹配及其相似度，无匹配返回 None
        
    Examples:
        >>> fuzzy_match_one("helo", ["hello", "world", "help"])
        ('hello', 0.8)
    """
    results = fuzzy_search(query, candidates, threshold, limit=1)
    return results[0] if results else None


def edit_sequence(s1: str, s2: str) -> List[Tuple[str, int, int, Optional[str]]]:
    """
    生成将 s1 转换为 s2 的编辑操作序列
    
    Args:
        s1: 源字符串
        s2: 目标字符串
        
    Returns:
        List[Tuple[str, int, int, Optional[str]]]: 编辑操作列表
            每个元组为 (操作类型, 源位置, 目标位置, 字符)
            操作类型: 'insert', 'delete', 'replace', 'match'
            
    Examples:
        >>> edit_sequence("kitten", "sitting")
        [('replace', 0, 0, 's'), ('match', 1, 1, 'i'), ...]
    """
    len1, len2 = len(s1), len(s2)
    
    # 构建完整的距离矩阵
    d = [[0] * (len2 + 1) for _ in range(len1 + 1)]
    
    for i in range(len1 + 1):
        d[i][0] = i
    for j in range(len2 + 1):
        d[0][j] = j
    
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            d[i][j] = min(
                d[i - 1][j] + 1,      # 删除
                d[i][j - 1] + 1,      # 插入
                d[i - 1][j - 1] + cost  # 替换或匹配
            )
    
    # 回溯找到编辑序列
    operations = []
    i, j = len1, len2
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and s1[i - 1] == s2[j - 1]:
            operations.append(('match', i - 1, j - 1, s1[i - 1]))
            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or d[i][j] == d[i][j - 1] + 1):
            operations.append(('insert', i, j - 1, s2[j - 1]))
            j -= 1
        elif i > 0 and (j == 0 or d[i][j] == d[i - 1][j] + 1):
            operations.append(('delete', i - 1, j, s1[i - 1]))
            i -= 1
        else:
            operations.append(('replace', i - 1, j - 1, f"{s1[i - 1]}→{s2[j - 1]}"))
            i -= 1
            j -= 1
    
    operations.reverse()
    return operations


def jaro_winkler_similarity(s1: str, s2: str) -> float:
    """
    计算 Jaro-Winkler 相似度
    
    对于短字符串的模糊匹配更准确，特别是处理前缀相似的情况
    
    Args:
        s1: 第一个字符串
        s2: 第二个字符串
        
    Returns:
        float: Jaro-Winkler 相似度 [0.0, 1.0]
        
    Examples:
        >>> round(jaro_winkler_similarity("MARTHA", "MARHTA"), 3)
        0.961
    """
    if s1 == s2:
        return 1.0
    
    len1, len2 = len(s1), len(s2)
    
    if len1 == 0 or len2 == 0:
        return 0.0
    
    # 计算匹配窗口大小
    match_distance = max(len1, len2) // 2 - 1
    if match_distance < 0:
        match_distance = 0
    
    s1_matches = [False] * len1
    s2_matches = [False] * len2
    
    matches = 0
    transpositions = 0
    
    # 找匹配字符
    for i in range(len1):
        start = max(0, i - match_distance)
        end = min(i + match_distance + 1, len2)
        
        for j in range(start, end):
            if s2_matches[j] or s1[i] != s2[j]:
                continue
            s1_matches[i] = True
            s2_matches[j] = True
            matches += 1
            break
    
    if matches == 0:
        return 0.0
    
    # 计算换位数
    k = 0
    for i in range(len1):
        if not s1_matches[i]:
            continue
        while not s2_matches[k]:
            k += 1
        if s1[i] != s2[k]:
            transpositions += 1
        k += 1
    
    jaro = (
        matches / len1 +
        matches / len2 +
        (matches - transpositions / 2) / matches
    ) / 3
    
    # 计算 Winkler 修正
    prefix = 0
    for i in range(min(len1, len2, 4)):
        if s1[i] == s2[i]:
            prefix += 1
        else:
            break
    
    return jaro + prefix * 0.1 * (1 - jaro)


def hamming_distance(s1: str, s2: str) -> int:
    """
    计算 Hamming 距离
    
    只适用于等长字符串，计算对应位置不同字符的数量
    
    Args:
        s1: 第一个字符串
        s2: 第二个字符串
        
    Returns:
        int: Hamming 距离
        
    Raises:
        ValueError: 当字符串长度不等时
        
    Examples:
        >>> hamming_distance("karolin", "kathrin")
        3
        >>> hamming_distance("1011101", "1001001")
        2
    """
    if len(s1) != len(s2):
        raise ValueError(f"字符串长度必须相等: {len(s1)} != {len(s2)}")
    
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))


def longest_common_subsequence(s1: str, s2: str) -> str:
    """
    找出两个字符串的最长公共子序列
    
    Args:
        s1: 第一个字符串
        s2: 第二个字符串
        
    Returns:
        str: 最长公共子序列
        
    Examples:
        >>> longest_common_subsequence("ABCBDAB", "BDCABA")
        'BCBA'
    """
    len1, len2 = len(s1), len(s2)
    
    # 构建 LCS 长度表
    dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]
    
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # 回溯找出 LCS
    lcs = []
    i, j = len1, len2
    
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


def longest_common_substring(s1: str, s2: str) -> str:
    """
    找出两个字符串的最长公共子串
    
    与子序列不同，子串必须是连续的
    
    Args:
        s1: 第一个字符串
        s2: 第二个字符串
        
    Returns:
        str: 最长公共子串
        
    Examples:
        >>> longest_common_substring("ABABC", "BABCA")
        'BABC'
    """
    len1, len2 = len(s1), len(s2)
    
    # 使用一维数组优化空间
    dp = [0] * (len2 + 1)
    max_len = 0
    end_pos = 0
    
    for i in range(1, len1 + 1):
        prev = 0
        for j in range(1, len2 + 1):
            temp = dp[j]
            if s1[i - 1] == s2[j - 1]:
                dp[j] = prev + 1
                if dp[j] > max_len:
                    max_len = dp[j]
                    end_pos = i
            else:
                dp[j] = 0
            prev = temp
    
    return s1[end_pos - max_len:end_pos]


def fuzzy_replace(
    text: str,
    old: str,
    new: str,
    threshold: float = 0.8
) -> Tuple[str, int]:
    """
    模糊替换文本中的字符串
    
    将文本中与 old 相似的子串替换为 new
    
    Args:
        text: 原文本
        old: 要替换的模式
        new: 替换后的文本
        threshold: 相似度阈值
        
    Returns:
        Tuple[str, int]: (替换后的文本, 替换次数)
        
    Examples:
        >>> fuzzy_replace("I have an aplpe and an appel", "apple", "orange", 0.6)
        ('I have an orange and an orange', 2)
    """
    if not old or not text:
        return text, 0
    
    old_len = len(old)
    result = []
    i = 0
    replace_count = 0
    
    while i < len(text):
        # 检查所有可能的子串
        best_match = None
        best_ratio = threshold
        best_end = i
        
        for j in range(i, min(i + old_len * 2, len(text)) + 1):
            substring = text[i:j]
            ratio = similarity_ratio(old, substring)
            if ratio >= best_ratio and (best_match is None or j - i > best_end - i):
                best_match = substring
                best_ratio = ratio
                best_end = j
        
        if best_match and best_end - i >= old_len // 2:
            result.append(new)
            replace_count += 1
            i = best_end
        else:
            result.append(text[i])
            i += 1
    
    return ''.join(result), replace_count


def spell_check_suggestions(
    word: str,
    dictionary: List[str],
    max_suggestions: int = 5,
    threshold: float = 0.6
) -> List[Tuple[str, float]]:
    """
    拼写检查建议
    
    从字典中找出与给定单词最相似的候选词
    
    Args:
        word: 待检查的单词
        dictionary: 正确单词字典
        max_suggestions: 最大建议数
        threshold: 最低相似度阈值
        
    Returns:
        List[Tuple[str, float]]: 建议列表，按相似度降序排列
        
    Examples:
        >>> dictionary = ["apple", "orange", "banana", "grape"]
        >>> spell_check_suggestions("aple", dictionary, max_suggestions=3)
        [('apple', 0.8), ('grape', 0.6)]
    """
    suggestions = []
    
    for dict_word in dictionary:
        # 使用 Jaro-Winkler 更适合拼写检查
        similarity = jaro_winkler_similarity(word, dict_word)
        if similarity >= threshold:
            suggestions.append((dict_word, similarity))
    
    suggestions.sort(key=lambda x: x[1], reverse=True)
    return suggestions[:max_suggestions]


class FuzzyMatcher:
    """
    模糊匹配器类，支持批量模糊匹配和缓存优化
    """
    
    def __init__(
        self,
        candidates: List[str],
        similarity_func: Optional[Callable[[str, str], float]] = None
    ):
        """
        初始化模糊匹配器
        
        Args:
            candidates: 候选字符串列表
            similarity_func: 自定义相似度函数，默认使用 similarity_ratio
        """
        self.candidates = candidates
        self.similarity_func = similarity_func or similarity_ratio
        self._cache: dict = {}
    
    def find_best(
        self,
        query: str,
        threshold: float = 0.6
    ) -> Optional[Tuple[str, float]]:
        """
        找出最佳匹配
        
        Args:
            query: 查询字符串
            threshold: 相似度阈值
            
        Returns:
            Optional[Tuple[str, float]]: 最佳匹配及其相似度
        """
        if query in self._cache:
            return self._cache[query]
        
        best_match = None
        best_similarity = threshold
        
        for candidate in self.candidates:
            similarity = self.similarity_func(query, candidate)
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = candidate
        
        result = (best_match, best_similarity) if best_match else None
        self._cache[query] = result
        return result
    
    def find_all(
        self,
        query: str,
        threshold: float = 0.6,
        limit: Optional[int] = None
    ) -> List[Tuple[str, float]]:
        """
        找出所有满足阈值的匹配
        
        Args:
            query: 查询字符串
            threshold: 相似度阈值
            limit: 最大返回数量
            
        Returns:
            List[Tuple[str, float]]: 匹配列表
        """
        results = []
        for candidate in self.candidates:
            similarity = self.similarity_func(query, candidate)
            if similarity >= threshold:
                results.append((candidate, similarity))
        
        results.sort(key=lambda x: x[1], reverse=True)
        
        if limit:
            results = results[:limit]
        
        return results
    
    def clear_cache(self) -> None:
        """清除缓存"""
        self._cache.clear()
    
    def add_candidate(self, candidate: str) -> None:
        """添加候选"""
        if candidate not in self.candidates:
            self.candidates.append(candidate)
    
    def remove_candidate(self, candidate: str) -> bool:
        """移除候选"""
        try:
            self.candidates.remove(candidate)
            return True
        except ValueError:
            return False


# 便捷函数
def distance(s1: str, s2: str) -> int:
    """levenshtein_distance 的简写"""
    return levenshtein_distance(s1, s2)


def similarity(s1: str, s2: str) -> float:
    """similarity_ratio 的简写"""
    return similarity_ratio(s1, s2)


def is_similar(s1: str, s2: str, threshold: float = 0.8) -> bool:
    """
    判断两个字符串是否相似
    
    Args:
        s1: 第一个字符串
        s2: 第二个字符串
        threshold: 相似度阈值
        
    Returns:
        bool: 是否相似
    """
    return similarity_ratio(s1, s2) >= threshold


if __name__ == "__main__":
    # 简单测试
    print("=== Levenshtein 距离测试 ===")
    print(f"'kitten' -> 'sitting': {levenshtein_distance('kitten', 'sitting')}")
    print(f"'hello' -> 'hello': {levenshtein_distance('hello', 'hello')}")
    print(f"'hello' -> '': {levenshtein_distance('hello', '')}")
    
    print("\n=== 相似度测试 ===")
    print(f"'apple' vs 'aple': {similarity_ratio('apple', 'aple'):.2f}")
    print(f"'test' vs 'best': {similarity_ratio('test', 'best'):.2f}")
    
    print("\n=== 模糊搜索测试 ===")
    candidates = ["apple", "banana", "orange", "grape", "apricot"]
    results = fuzzy_search("aple", candidates, threshold=0.5)
    print(f"搜索 'aple': {results}")
    
    print("\n=== Jaro-Winkler 测试 ===")
    print(f"'MARTHA' vs 'MARHTA': {jaro_winkler_similarity('MARTHA', 'MARHTA'):.3f}")
    
    print("\n=== 编辑序列测试 ===")
    ops = edit_sequence("kitten", "sitting")
    for op in ops:
        print(f"  {op}")