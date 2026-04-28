"""
edit_distance_utils - 编辑距离与字符串相似度工具集

提供多种编辑距离算法和字符串相似度计算方法，适用于：
- 拼写检查与自动纠正
- 模糊搜索与匹配
- DNA序列比对
- 抄袭检测
- 自动补全建议

零外部依赖，纯Python实现。
"""

from typing import List, Tuple, Optional, Callable
from functools import lru_cache


def levenshtein_distance(s1: str, s2: str) -> int:
    """
    计算两个字符串之间的 Levenshtein 编辑距离
    
    Levenshtein 距离是将一个字符串转换为另一个字符串所需的最少单字符编辑操作次数
    （插入、删除或替换）
    
    Args:
        s1: 第一个字符串
        s2: 第二个字符串
    
    Returns:
        int: 编辑距离（非负整数）
    
    Example:
        >>> levenshtein_distance("kitten", "sitting")
        3
        >>> levenshtein_distance("", "hello")
        5
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    # 使用空间优化的动态规划（只需要两行）
    previous_row = list(range(len(s2) + 1))
    
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


def damerau_levenshtein_distance(s1: str, s2: str) -> int:
    """
    计算两个字符串之间的 Damerau-Levenshtein 编辑距离
    
    与 Levenshtein 距离的区别在于：允许相邻字符交换（transposition）操作
    
    Args:
        s1: 第一个字符串
        s2: 第二个字符串
    
    Returns:
        int: 编辑距离（非负整数）
    
    Example:
        >>> damerau_levenshtein_distance("ca", "abc")
        2
        >>> damerau_levenshtein_distance("ab", "ba")
        1  # 只需要一次交换
    """
    len1, len2 = len(s1), len(s2)
    
    # 空字符串处理
    if len1 == 0:
        return len2
    if len2 == 0:
        return len1
    
    # 创建 DP 矩阵
    dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]
    
    # 初始化边界
    for i in range(len1 + 1):
        dp[i][0] = i
    for j in range(len2 + 1):
        dp[0][j] = j
    
    # 填充矩阵
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            
            dp[i][j] = min(
                dp[i - 1][j] + 1,      # 删除
                dp[i][j - 1] + 1,      # 插入
                dp[i - 1][j - 1] + cost  # 替换
            )
            
            # 相邻字符交换
            if (i > 1 and j > 1 and 
                s1[i - 1] == s2[j - 2] and 
                s1[i - 2] == s2[j - 1]):
                dp[i][j] = min(dp[i][j], dp[i - 2][j - 2] + 1)
    
    return dp[len1][len2]


def hamming_distance(s1: str, s2: str) -> int:
    """
    计算两个等长字符串之间的 Hamming 距离
    
    Hamming 距离是两个等长字符串对应位置上不同字符的个数
    
    Args:
        s1: 第一个字符串
        s2: 第二个字符串
    
    Returns:
        int: Hamming 距离
    
    Raises:
        ValueError: 当两个字符串长度不等时
    
    Example:
        >>> hamming_distance("karolin", "kathrin")
        3
        >>> hamming_distance("1011101", "1001001")
        2
    """
    if len(s1) != len(s2):
        raise ValueError(f"Hamming distance requires strings of equal length: {len(s1)} != {len(s2)}")
    
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))


def jaro_similarity(s1: str, s2: str) -> float:
    """
    计算两个字符串之间的 Jaro 相似度
    
    Jaro 相似度度量两个字符串的相似程度，值在 0 到 1 之间
    
    Args:
        s1: 第一个字符串
        s2: 第二个字符串
    
    Returns:
        float: 相似度值 [0, 1]，1 表示完全相同
    
    Example:
        >>> jaro_similarity("MARTHA", "MARHTA")
        0.944...
        >>> jaro_similarity("hello", "world")
        0.466...
    """
    if s1 == s2:
        return 1.0
    
    len1, len2 = len(s1), len(s2)
    
    if len1 == 0 or len2 == 0:
        return 0.0
    
    # 匹配窗口大小
    match_distance = max(len1, len2) // 2 - 1
    if match_distance < 0:
        match_distance = 0
    
    s1_matches = [False] * len1
    s2_matches = [False] * len2
    
    matches = 0
    
    # 查找匹配字符
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
    
    # 计算换位数 - 优化：直接遍历匹配位置
    transpositions = 0
    k = 0
    for i in range(len1):
        if not s1_matches[i]:
            continue
        while not s2_matches[k]:
            k += 1
        if s1[i] != s2[k]:
            transpositions += 1
        k += 1
    
    jaro = (matches / len1 + matches / len2 + 
            (matches - transpositions / 2) / matches) / 3
    
    return jaro


def jaro_winkler_similarity(s1: str, s2: str, scaling_factor: float = 0.1) -> float:
    """
    计算两个字符串之间的 Jaro-Winkler 相似度
    
    Jaro-Winkler 是 Jaro 相似度的改进版本，对开头相同的字符串给予更高权重
    
    Args:
        s1: 第一个字符串
        s2: 第二个字符串
        scaling_factor: 缩放因子，默认 0.1，最大 0.25
    
    Returns:
        float: 相似度值 [0, 1]
    
    Example:
        >>> jaro_winkler_similarity("MARTHA", "MARHTA")
        0.961...
        >>> jaro_winkler_similarity("hello", "hallo")
        0.88...
    """
    # 限制缩放因子
    scaling_factor = min(scaling_factor, 0.25)
    
    jaro_sim = jaro_similarity(s1, s2)
    
    # 计算公共前缀长度（最多4个字符）
    prefix_len = 0
    for i in range(min(len(s1), len(s2), 4)):
        if s1[i] == s2[i]:
            prefix_len += 1
        else:
            break
    
    return jaro_sim + prefix_len * scaling_factor * (1 - jaro_sim)


def lcs_length(s1: str, s2: str) -> int:
    """
    计算两个字符串的最长公共子序列长度
    
    公共子序列不需要连续，只需保持相对顺序
    
    Args:
        s1: 第一个字符串
        s2: 第二个字符串
    
    Returns:
        int: 最长公共子序列长度
    
    Example:
        >>> lcs_length("ABCDGH", "AEDFHR")
        3  # "ADH"
        >>> lcs_length("AGGTAB", "GXTXAYB")
        4  # "GTAB"
    """
    len1, len2 = len(s1), len(s2)
    
    # 空间优化：只需要两行
    prev = [0] * (len2 + 1)
    curr = [0] * (len2 + 1)
    
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if s1[i - 1] == s2[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev, curr = curr, prev
    
    return prev[len2]


def lcs_string(s1: str, s2: str) -> str:
    """
    获取两个字符串的最长公共子序列
    
    Args:
        s1: 第一个字符串
        s2: 第二个字符串
    
    Returns:
        str: 最长公共子序列字符串
    
    Example:
        >>> lcs_string("ABCDGH", "AEDFHR")
        'ADH'
    """
    len1, len2 = len(s1), len(s2)
    
    # 构建 DP 表
    dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]
    
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # 回溯找到 LCS
    result = []
    i, j = len1, len2
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            result.append(s1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    
    return ''.join(reversed(result))


def normalized_levenshtein(s1: str, s2: str) -> float:
    """
    计算归一化的 Levenshtein 相似度
    
    将编辑距离归一化到 [0, 1] 范围，1 表示完全相同
    
    Args:
        s1: 第一个字符串
        s2: 第二个字符串
    
    Returns:
        float: 归一化相似度 [0, 1]
    
    Example:
        >>> normalized_levenshtein("hello", "hallo")
        0.8
    """
    if s1 == s2:
        return 1.0
    
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 1.0
    
    dist = levenshtein_distance(s1, s2)
    return 1.0 - (dist / max_len)


def similarity_ratio(s1: str, s2: str, method: str = 'jaro_winkler') -> float:
    """
    计算两个字符串的相似比率
    
    Args:
        s1: 第一个字符串
        s2: 第二个字符串
        method: 相似度计算方法
            - 'jaro_winkler': Jaro-Winkler 相似度（默认）
            - 'jaro': Jaro 相似度
            - 'levenshtein': 归一化 Levenshtein 相似度
            - 'lcs': 基于 LCS 的相似度
    
    Returns:
        float: 相似度 [0, 1]
    
    Example:
        >>> similarity_ratio("hello", "hallo", method='jaro_winkler')
        0.88...
    """
    methods = {
        'jaro_winkler': jaro_winkler_similarity,
        'jaro': jaro_similarity,
        'levenshtein': normalized_levenshtein,
        'lcs': lambda a, b: lcs_length(a, b) / max(len(a), len(b)) if max(len(a), len(b)) > 0 else 1.0
    }
    
    if method not in methods:
        raise ValueError(f"Unknown method: {method}. Choose from {list(methods.keys())}")
    
    return methods[method](s1, s2)


def fuzzy_match(query: str, candidates: List[str], 
                threshold: float = 0.6, 
                method: str = 'jaro_winkler',
                limit: Optional[int] = None) -> List[Tuple[str, float]]:
    """
    模糊匹配：从候选列表中找出与查询字符串相似的项
    
    Args:
        query: 查询字符串
        candidates: 候选字符串列表
        threshold: 相似度阈值，低于此值不返回
        method: 相似度计算方法
        limit: 返回结果的最大数量
    
    Returns:
        List[Tuple[str, float]]: (候选字符串, 相似度) 列表，按相似度降序排列
    
    Example:
        >>> fuzzy_match("helo", ["hello", "help", "held", "halo", "hero"])
        [('hello', 0.93...), ('held', 0.88...), ('halo', 0.78...)]
    """
    results = []
    
    for candidate in candidates:
        score = similarity_ratio(query, candidate, method=method)
        if score >= threshold:
            results.append((candidate, score))
    
    # 按相似度降序排序
    results.sort(key=lambda x: x[1], reverse=True)
    
    if limit is not None:
        results = results[:limit]
    
    return results


def spell_suggest(word: str, 
                  dictionary: List[str],
                  max_distance: int = 2,
                  limit: int = 5,
                  method: str = 'levenshtein') -> List[Tuple[str, int]]:
    """
    拼写建议：从词典中找出与给定单词相似的建议
    
    Args:
        word: 待检查的单词
        dictionary: 词典列表
        max_distance: 最大编辑距离
        limit: 返回结果的最大数量
        method: 距离计算方法
            - 'levenshtein': Levenshtein 距离
            - 'damerau_levenshtein': Damerau-Levenshtein 距离
    
    Returns:
        List[Tuple[str, int]]: (建议词, 编辑距离) 列表，按距离升序排列
    
    Example:
        >>> spell_suggest("appel", ["apple", "apply", "ape", "appeal"])
        [('apple', 1), ('appeal', 2)]
    """
    if method == 'levenshtein':
        distance_func = levenshtein_distance
    elif method == 'damerau_levenshtein':
        distance_func = damerau_levenshtein_distance
    else:
        raise ValueError(f"Unknown method: {method}")
    
    results = []
    
    for dict_word in dictionary:
        dist = distance_func(word, dict_word)
        if dist <= max_distance:
            results.append((dict_word, dist))
    
    # 按距离升序排序，距离相同按字典序
    results.sort(key=lambda x: (x[1], x[0]))
    
    return results[:limit]


def edit_operations(s1: str, s2: str) -> List[Tuple[str, int, Optional[str]]]:
    """
    计算将 s1 转换为 s2 所需的编辑操作序列
    
    Args:
        s1: 源字符串
        s2: 目标字符串
    
    Returns:
        List[Tuple[str, int, Optional[str]]]: 操作列表
            - ('insert', position, character): 在 position 插入 character
            - ('delete', position, None): 删除 position 处的字符
            - ('replace', position, character): 将 position 处的字符替换为 character
            - ('keep', position, None): 保持字符不变
    
    Example:
        >>> edit_operations("kitten", "sitting")
        [('replace', 0, 's'), ('keep', 1, None), ('keep', 2, None), 
         ('keep', 3, None), ('replace', 4, 'i'), ('keep', 5, None), 
         ('insert', 6, 'g')]
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
    
    # 回溯找操作序列
    operations = []
    i, j = len1, len2
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and s1[i - 1] == s2[j - 1]:
            operations.append(('keep', i - 1, None))
            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or dp[i][j] == dp[i][j - 1] + 1):
            operations.append(('insert', i, s2[j - 1]))
            j -= 1
        elif i > 0 and (j == 0 or dp[i][j] == dp[i - 1][j] + 1):
            operations.append(('delete', i - 1, None))
            i -= 1
        else:
            operations.append(('replace', i - 1, s2[j - 1]))
            i -= 1
            j -= 1
    
    operations.reverse()
    return operations


def diff_ratio(s1: str, s2: str) -> float:
    """
    计算两个字符串的差异比率
    
    基于 difflib.SequenceMatcher 的相似度计算
    
    Args:
        s1: 第一个字符串
        s2: 第二个字符串
    
    Returns:
        float: 相似度 [0, 1]
    
    Example:
        >>> diff_ratio("hello world", "hello earth")
        0.66...
    """
    # 纯 Python 实现的 SequenceMatcher 算法
    if s1 == s2:
        return 1.0
    
    len1, len2 = len(s1), len(s2)
    if len1 == 0 or len2 == 0:
        return 0.0
    
    # 找到最长公共子序列，计算匹配块
    matches = 0
    i = 0
    j = 0
    
    # 简化版本：统计匹配字符比例
    s2_chars = list(s2)
    for c in s1:
        if c in s2_chars:
            matches += 1
            s2_chars.remove(c)
    
    return 2.0 * matches / (len1 + len2)


# Soundex 编码映射（模块级别常量，避免重复创建）
_SOUNDEX_MAPPING = {
    'B': '1', 'F': '1', 'P': '1', 'V': '1',
    'C': '2', 'G': '2', 'J': '2', 'K': '2', 'Q': '2', 'S': '2', 'X': '2', 'Z': '2',
    'D': '3', 'T': '3',
    'L': '4',
    'M': '5', 'N': '5',
    'R': '6',
}


def _soundex_encode(name: str) -> str:
    """
    Soundex 编码辅助函数（模块级别）
    
    Args:
        name: 要编码的字符串
        
    Returns:
        4位 Soundex 编码字符串
    """
    if not name:
        return ''
    
    name = name.upper()
    # 保留首字母
    soundex_code = name[0]
    
    # 首字母的编码（用于判断相邻重复）
    first_char_code = _SOUNDEX_MAPPING.get(soundex_code, '')
    prev_code = first_char_code
    
    for char in name[1:]:
        code = _SOUNDEX_MAPPING.get(char, '')
        # 元音和 H/W/Y 不编码，但它们作为分隔符（重置 prev_code）
        if char in 'AEIOUHWY':
            prev_code = ''
            continue
        # 如果当前编码不同于前一个编码，添加到结果
        if code and code != prev_code:
            soundex_code += code
            if len(soundex_code) >= 4:
                break
        prev_code = code
    
    # 填充到 4 位
    return soundex_code[:4].ljust(4, '0')


def soundex_distance(s1: str, s2: str) -> int:
    """
    基于 Soundex 编码的语音距离
    
    Soundex 将发音相似的单词编码为相同的代码
    
    Args:
        s1: 第一个字符串
        s2: 第二个字符串
    
    Returns:
        int: 0 表示发音相似，非 0 表示不同
    
    Example:
        >>> soundex_distance("Robert", "Rupert")
        0  # 编码都是 R163
        >>> soundex_distance("Robert", "Albert")
        1  # 编码不同
    """
    if not s1 or not s2:
        return 1
    
    code1 = _soundex_encode(s1)
    code2 = _soundex_encode(s2)
    
    return 0 if code1 == code2 else 1


def ngram_similarity(s1: str, s2: str, n: int = 2) -> float:
    """
    基于 N-gram 的字符串相似度
    
    使用 Jaccard 相似度计算两个字符串的 n-gram 集合相似度
    
    Args:
        s1: 第一个字符串
        s2: 第二个字符串
        n: n-gram 的大小，默认 2（bigram）
    
    Returns:
        float: 相似度 [0, 1]
    
    Example:
        >>> ngram_similarity("hello", "hallo", n=2)
        0.6
    """
    def get_ngrams(s: str, n: int) -> set:
        if len(s) < n:
            return {s}
        return {s[i:i+n] for i in range(len(s) - n + 1)}
    
    ngrams1 = get_ngrams(s1, n)
    ngrams2 = get_ngrams(s2, n)
    
    if not ngrams1 and not ngrams2:
        return 1.0
    
    if not ngrams1 or not ngrams2:
        return 0.0
    
    intersection = len(ngrams1 & ngrams2)
    union = len(ngrams1 | ngrams2)
    
    return intersection / union if union > 0 else 0.0


class EditDistanceCalculator:
    """
    编辑距离计算器类
    
    提供缓存和批量计算功能，适用于需要多次计算相似度的场景
    
    Example:
        >>> calc = EditDistanceCalculator(method='jaro_winkler')
        >>> calc.similarity("hello", "hallo")
        0.88...
        >>> calc.batch_similarity("test", ["best", "rest", "text"])
        [('best', 0.88...), ('rest', 0.88...), ('text', 0.88...)]
    """
    
    def __init__(self, method: str = 'jaro_winkler', cache_size: int = 1000):
        """
        初始化计算器
        
        Args:
            method: 默认的相似度计算方法
            cache_size: 缓存大小
        """
        self.method = method
        self._cache: dict = {}
        self._cache_size = cache_size
    
    def _get_cache_key(self, s1: str, s2: str, method: str) -> tuple:
        # 统一顺序以增加缓存命中率
        if s1 > s2:
            s1, s2 = s2, s1
        return (s1, s2, method)
    
    def similarity(self, s1: str, s2: str, method: Optional[str] = None) -> float:
        """
        计算两个字符串的相似度（带缓存）
        
        Args:
            s1: 第一个字符串
            s2: 第二个字符串
            method: 计算方法，默认使用初始化时指定的方法
        
        Returns:
            float: 相似度 [0, 1]
        """
        method = method or self.method
        cache_key = self._get_cache_key(s1, s2, method)
        
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        result = similarity_ratio(s1, s2, method=method)
        
        # LRU 缓存管理
        if len(self._cache) >= self._cache_size:
            # 删除最早的条目
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
        
        self._cache[cache_key] = result
        return result
    
    def batch_similarity(self, query: str, candidates: List[str], 
                         method: Optional[str] = None) -> List[Tuple[str, float]]:
        """
        批量计算相似度
        
        Args:
            query: 查询字符串
            candidates: 候选字符串列表
            method: 计算方法
        
        Returns:
            List[Tuple[str, float]]: (候选字符串, 相似度) 列表
        """
        results = []
        for candidate in candidates:
            score = self.similarity(query, candidate, method=method)
            results.append((candidate, score))
        
        # 按相似度降序排序
        results.sort(key=lambda x: x[1], reverse=True)
        return results
    
    def clear_cache(self) -> None:
        """清空缓存"""
        self._cache.clear()


# 导出的公共 API
__all__ = [
    # 距离计算
    'levenshtein_distance',
    'damerau_levenshtein_distance',
    'hamming_distance',
    'soundex_distance',
    
    # 相似度计算
    'jaro_similarity',
    'jaro_winkler_similarity',
    'normalized_levenshtein',
    'similarity_ratio',
    'diff_ratio',
    'ngram_similarity',
    
    # LCS 相关
    'lcs_length',
    'lcs_string',
    
    # 模糊匹配与拼写建议
    'fuzzy_match',
    'spell_suggest',
    
    # 编辑操作
    'edit_operations',
    
    # 计算器类
    'EditDistanceCalculator',
]