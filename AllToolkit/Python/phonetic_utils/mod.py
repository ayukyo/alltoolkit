"""
Phonetic Utils - 语音匹配工具

零依赖的语音编码库，支持：
- Soundex（经典语音算法）
- Metaphone（改进版语音算法）
- Double Metaphone（双语音编码）
- NYSIIS（纽约州识别系统）
- Caverphone（新西兰算法）
- Match Rating Approach（评级匹配）
- Lein（Lein名称匹配）
- Fuzzy matching（模糊匹配）

用于：
- 姓名模糊匹配
- 数据去重
- 搜索优化
- 历史研究/族谱研究

Author: AllToolkit
License: MIT
"""

from typing import Union, List, Tuple, Optional, Dict, Set
import re
import unicodedata


class PhoneticError(Exception):
    """语音编码错误基类"""
    pass


class InvalidInputError(PhoneticError):
    """无效输入错误"""
    pass


# ============== 辅助函数 ==============

def _normalize(text: str) -> str:
    """
    标准化文本：转大写、移除变音符号、保留字母
    
    Args:
        text: 输入文本
    
    Returns:
        标准化后的文本
    """
    if not text:
        return ''
    
    # 移除变音符号
    normalized = unicodedata.normalize('NFKD', text)
    ascii_text = ''.join(c for c in normalized if not unicodedata.combining(c))
    
    # 转大写，只保留字母
    return ''.join(c for c in ascii_text.upper() if c.isalpha())


def _is_vowel(c: str) -> bool:
    """检查是否为元音"""
    return c.upper() in 'AEIOU'


def _is_consonant(c: str) -> bool:
    """检查是否为辅音"""
    return c.upper() in 'BCDFGHJKLMNPQRSTVWXYZ'


# ============== SOUNDEX ==============

# Soundex 编码映射
SOUNDEX_MAP = {
    'B': '1', 'F': '1', 'P': '1', 'V': '1',
    'C': '2', 'G': '2', 'J': '2', 'K': '2', 'Q': '2', 'S': '2', 'X': '2', 'Z': '2',
    'D': '3', 'T': '3',
    'L': '4',
    'M': '5', 'N': '5',
    'R': '6',
}


def soundex(name: str, length: int = 4) -> str:
    """
    Soundex 语音编码算法
    
    将姓名转换为语音代码，用于模糊匹配。
    
    规则：
    1. 保留首字母
    2. 按映射表替换辅音
    3. 元音和H、W忽略
    4. 相邻相同数字合并
    5. 填充或截断到指定长度
    
    Args:
        name: 输入姓名
        length: 输出长度（默认4）
    
    Returns:
        Soundex编码
    
    Example:
        >>> soundex('Robert')
        'R163'
        >>> soundex('Rupert')
        'R163'
        >>> soundex('Smith')
        'S530'
        >>> soundex('Schmidt')
        'S530'
    """
    if not name:
        return '0' * length
    
    name = _normalize(name)
    
    if not name:
        return '0' * length
    
    # 保留首字母
    first_letter = name[0]
    
    # 编码剩余字母
    encoded = []
    prev_code = SOUNDEX_MAP.get(first_letter, '')
    
    for char in name[1:]:
        code = SOUNDEX_MAP.get(char, '')
        
        # 跳过元音和H、W
        if char in 'AEIOUHW':
            prev_code = ''
            continue
        
        # 相邻相同数字不重复
        if code and code != prev_code:
            encoded.append(code)
        
        prev_code = code
    
    # 组合结果
    result = first_letter + ''.join(encoded)
    
    # 填充或截断
    result = (result + '0' * length)[:length]
    
    return result


def soundex_words(text: str, length: int = 4) -> List[str]:
    """
    对文本中每个单词进行Soundex编码
    
    Args:
        text: 输入文本
        length: 输出长度
    
    Returns:
        Soundex编码列表
    
    Example:
        >>> soundex_words('John Smith')
        ['J500', 'S530']
    """
    words = text.split()
    return [soundex(word, length) for word in words]


# ============== METAPHONE ==============

# Metaphone 规则
METAPHONE_VOWELS = 'AEIOU'


def metaphone(name: str, length: int = 4) -> str:
    """
    Metaphone 语音编码算法
    
    Soundex的改进版本，对英语发音更准确。
    
    Args:
        name: 输入姓名
        length: 输出长度（默认4，0表示不限制）
    
    Returns:
        Metaphone编码
    
    Example:
        >>> metaphone('Smith')
        'SM0T'
        >>> metaphone('Schmidt')
        'SMTT'
        >>> metaphone('phone')
        'FN'
    """
    if not name:
        return ''
    
    name = _normalize(name)
    
    if not name:
        return ''
    
    # 处理特殊前缀
    if name.startswith('KN') or name.startswith('GN') or name.startswith('PN') or name.startswith('AE'):
        name = name[1:]
    elif name.startswith('WR'):
        name = name[1:]
    elif name.startswith('WH'):
        name = 'W' + name[2:]
    elif name.startswith('X'):
        name = 'S' + name[1:]
    
    result = []
    i = 0
    n = len(name)
    
    while i < n:
        char = name[i]
        next_char = name[i + 1] if i + 1 < n else ''
        prev_char = name[i - 1] if i > 0 else ''
        next_next = name[i + 2] if i + 2 < n else ''
        
        # 跳过元音（除了开头）
        if _is_vowel(char):
            if i == 0:
                result.append(char)
            i += 1
            continue
        
        # 处理辅音
        if char == 'B':
            # B -> B，除非在MB后面（在词尾）
            if not (i == n - 1 and prev_char == 'M'):
                result.append('B')
        
        elif char == 'C':
            # C -> X (SH) 在CIA或CH前
            # C -> S 在CI、CE、CY前
            # C -> K 其他情况
            if next_char == 'I' and next_next == 'A':
                result.append('X')
            elif next_char == 'H':
                result.append('X')
                i += 1
            elif next_char in 'IEY':
                result.append('S')
            else:
                result.append('K')
        
        elif char == 'D':
            # D -> J 在GE、GI、GY前
            # D -> T 其他情况
            if next_char == 'G' and next_next in 'IEY':
                result.append('J')
            else:
                result.append('T')
        
        elif char == 'F':
            result.append('F')
        
        elif char == 'G':
            # G -> F 在GH（不在词首）
            # G -> 静音 在GN或NGE前
            # G -> J 在GE、GI、GY前
            # G -> K 其他情况
            if next_char == 'H':
                if i + 2 < n and name[i + 2] not in 'AEIOU':
                    i += 1
                else:
                    result.append('F')
                    i += 1
            elif next_char == 'N':
                if next_next in 'EIY' or i + 2 >= n:
                    pass  # 静音
                else:
                    result.append('K')
            elif next_char in 'IEY':
                result.append('J')
            else:
                result.append('K')
        
        elif char == 'H':
            # H -> H 在元音前且不在C、G、P、S、T后
            if prev_char not in 'CGPST' and next_char and _is_vowel(next_char):
                result.append('H')
        
        elif char == 'J':
            result.append('J')
        
        elif char == 'K':
            # K -> 静音 在N后
            if prev_char != 'N':
                result.append('K')
        
        elif char == 'L':
            result.append('L')
        
        elif char == 'M':
            result.append('M')
        
        elif char == 'N':
            result.append('N')
        
        elif char == 'P':
            # P -> F 在H前
            # P -> P 其他情况
            if next_char == 'H':
                result.append('F')
                i += 1
            else:
                result.append('P')
        
        elif char == 'Q':
            result.append('K')
        
        elif char == 'R':
            result.append('R')
        
        elif char == 'S':
            # S -> X (SH) 在H前
            # S -> X 在IO、IA前
            # S -> S 其他情况
            if next_char == 'H':
                result.append('X')
                i += 1
            elif next_char == 'I' and next_next in 'AO':
                result.append('X')
            else:
                result.append('S')
        
        elif char == 'T':
            # T -> X 在IA、IO前
            # T -> 0 (TH) 在H前
            # T -> 静音 在CH后
            # T -> T 其他情况
            if next_char == 'I' and next_next in 'AO':
                result.append('X')
            elif next_char == 'H':
                result.append('0')  # TH sound
                i += 1
            elif prev_char != 'C':
                result.append('T')
        
        elif char == 'V':
            result.append('F')
        
        elif char == 'W':
            # W -> W 在元音前
            if next_char and _is_vowel(next_char):
                result.append('W')
        
        elif char == 'X':
            result.append('KS')
        
        elif char == 'Y':
            # Y -> Y 在元音前
            if next_char and _is_vowel(next_char):
                result.append('Y')
        
        elif char == 'Z':
            result.append('S')
        
        i += 1
    
    # 组合结果
    code = ''.join(result)
    
    # 截断到指定长度
    if length > 0:
        code = code[:length]
    
    return code


# ============== DOUBLE METAPHONE ==============

# Double Metaphone 规则更复杂，返回主要和备选编码

def double_metaphone(name: str, length: int = 4) -> Tuple[str, str]:
    """
    Double Metaphone 双语音编码算法
    
    返回主要编码和备选编码，提高匹配准确度。
    
    Args:
        name: 输入姓名
        length: 输出长度（默认4，0表示不限制）
    
    Returns:
        (主要编码, 备选编码)
    
    Example:
        >>> double_metaphone('Smith')
        ('SM0T', 'XMTT')
        >>> double_metaphone('Schmidt')
        ('SMTT', 'XMTT')
    """
    if not name:
        return ('', '')
    
    name = _normalize(name)
    
    if not name:
        return ('', '')
    
    # 简化版实现：基于Metaphone规则
    # 完整实现需要处理更多边缘情况
    
    primary = []
    alternate = []
    i = 0
    n = len(name)
    
    # 处理特殊前缀
    if name.startswith('KN') or name.startswith('GN') or name.startswith('PN'):
        name = name[1:]
        n = len(name)
    elif name.startswith('WR'):
        name = name[1:]
        n = len(name)
    elif name.startswith('WH'):
        name = 'W' + name[2:]
        n = len(name)
    elif name.startswith('X'):
        name = 'S' + name[1:]
    
    while i < n:
        char = name[i]
        next_char = name[i + 1] if i + 1 < n else ''
        prev_char = name[i - 1] if i > 0 else ''
        next_next = name[i + 2] if i + 2 < n else ''
        
        if _is_vowel(char):
            if i == 0:
                primary.append(char)
                alternate.append(char)
            i += 1
            continue
        
        if char == 'B':
            if not (i == n - 1 and prev_char == 'M'):
                primary.append('B')
                alternate.append('B')
        
        elif char == 'C':
            if next_char == 'H':
                primary.append('X')
                alternate.append('X')
                i += 1
            elif next_char in 'IEY':
                primary.append('S')
                alternate.append('S')
            else:
                primary.append('K')
                alternate.append('K')
        
        elif char == 'D':
            if next_char == 'G' and next_next in 'IEY':
                primary.append('J')
                alternate.append('J')
            else:
                primary.append('T')
                alternate.append('T')
        
        elif char == 'F':
            primary.append('F')
            alternate.append('F')
        
        elif char == 'G':
            if next_char == 'H':
                if i + 2 < n and name[i + 2] not in 'AEIOU':
                    pass
                else:
                    primary.append('F')
                    alternate.append('F')
                    i += 1
            elif next_char in 'IEY':
                primary.append('J')
                alternate.append('K')  # 备选
            else:
                primary.append('K')
                alternate.append('K')
        
        elif char == 'H':
            if prev_char not in 'CGPST' and next_char and _is_vowel(next_char):
                primary.append('H')
                alternate.append('H')
        
        elif char == 'J':
            primary.append('J')
            alternate.append('J')
        
        elif char == 'K':
            primary.append('K')
            alternate.append('K')
        
        elif char == 'L':
            primary.append('L')
            alternate.append('L')
        
        elif char == 'M':
            primary.append('M')
            alternate.append('M')
        
        elif char == 'N':
            primary.append('N')
            alternate.append('N')
        
        elif char == 'P':
            if next_char == 'H':
                primary.append('F')
                alternate.append('F')
                i += 1
            else:
                primary.append('P')
                alternate.append('P')
        
        elif char == 'Q':
            primary.append('K')
            alternate.append('K')
        
        elif char == 'R':
            primary.append('R')
            alternate.append('R')
        
        elif char == 'S':
            if next_char == 'H':
                primary.append('X')
                alternate.append('X')
                i += 1
            elif next_char == 'I' and next_next in 'AO':
                primary.append('X')
                alternate.append('X')
            else:
                primary.append('S')
                alternate.append('S')
        
        elif char == 'T':
            if next_char == 'H':
                primary.append('0')  # TH
                alternate.append('T')
                i += 1
            elif next_char == 'I' and next_next in 'AO':
                primary.append('X')
                alternate.append('X')
            else:
                primary.append('T')
                alternate.append('T')
        
        elif char == 'V':
            primary.append('F')
            alternate.append('F')
        
        elif char == 'W':
            if next_char and _is_vowel(next_char):
                primary.append('W')
                alternate.append('W')
        
        elif char == 'X':
            primary.append('KS')
            alternate.append('KS')
        
        elif char == 'Y':
            if next_char and _is_vowel(next_char):
                primary.append('Y')
                alternate.append('Y')
        
        elif char == 'Z':
            primary.append('S')
            alternate.append('S')
        
        i += 1
    
    p_code = ''.join(primary)
    a_code = ''.join(alternate)
    
    if length > 0:
        p_code = p_code[:length]
        a_code = a_code[:length]
    
    return (p_code, a_code)


# ============== NYSIIS ==============

def nysiis(name: str) -> str:
    """
    NYSIIS (New York State Identification and Intelligence System) 编码
    
    纽约州开发的姓名编码系统，比Soundex更准确。
    
    Args:
        name: 输入姓名
    
    Returns:
        NYSIIS编码
    
    Example:
        >>> nysiis('Smith')
        'SNAT'
        >>> nysiis('Schmidt')
        'SNAT'
    """
    if not name:
        return ''
    
    name = _normalize(name)
    
    if not name:
        return ''
    
    # 处理前缀
    if name.startswith('MAC'):
        name = 'MCC' + name[3:]
    elif name.startswith('KN'):
        name = 'NN' + name[2:]
    elif name.startswith('K'):
        name = 'C' + name[1:]
    elif name.startswith('PH'):
        name = 'FF' + name[2:]
    elif name.startswith('PF'):
        name = 'FF' + name[2:]
    elif name.startswith('SCH'):
        name = 'SSS' + name[3:]
    
    # 处理后缀
    if name.endswith('EE'):
        name = name[:-2] + 'Y'
    elif name.endswith('IE'):
        name = name[:-2] + 'Y'
    elif name.endswith('DT') or name.endswith('RT') or name.endswith('RD') or name.endswith('NT') or name.endswith('ND'):
        name = name[:-1]
    
    result = []
    n = len(name)
    
    for i in range(n):
        char = name[i]
        next_char = name[i + 1] if i + 1 < n else ''
        prev_char = name[i - 1] if i > 0 else ''
        
        # 转换EV为AF
        if char == 'E' and next_char == 'V':
            result.append('A')
            result.append('F')
            continue
        
        # 元音处理
        if _is_vowel(char):
            result.append('A')
            continue
        
        if char == 'Q':
            result.append('G')
        elif char == 'Z':
            result.append('S')
        elif char == 'M':
            result.append('N')
        elif char == 'K':
            if next_char == 'N':
                result.append('N')
            else:
                result.append('C')
        elif char == 'S' and next_char == 'C':
            result.append('S')
        elif char == 'P' and next_char == 'H':
            result.append('F')
        elif char == 'H' and prev_char and not _is_vowel(prev_char):
            result.append(prev_char)
        elif char == 'W' and prev_char and _is_vowel(prev_char):
            result.append(prev_char)
        elif char in 'BCDFGJKLMNPSTV':
            result.append(char)
    
    # 合并重复字符
    merged = []
    for c in result:
        if not merged or merged[-1] != c:
            merged.append(c)
    
    # 移除尾部的S或A
    while merged and merged[-1] in 'SA':
        merged.pop()
    
    # 添加尾部A
    merged.append('A')
    
    return ''.join(merged)


# ============== CAVERPHONE ==============

def caverphone(name: str, version: int = 2) -> str:
    """
    Caverphone 语音编码算法
    
    新西兰开发的算法，用于匹配方言姓名。
    
    Args:
        name: 输入姓名
        version: 版本（1或2，默认2）
    
    Returns:
        Caverphone编码
    
    Example:
        >>> caverphone('Smith')
        'SMT11111'
        >>> caverphone('Schmidt')
        'SKMT1111'
    """
    if not name:
        return '1' * 10
    
    name = _normalize(name)
    
    if not name:
        return '1' * 10
    
    # 只保留字母
    name = ''.join(c for c in name if c.isalpha())
    
    # 移除尾部的e
    if name.endswith('e'):
        name = name[:-1]
    
    # 版本2的额外规则
    if version >= 2:
        # 移除尾部的s
        if name.endswith('s'):
            name = name[:-1]
    
    # 替换规则
    replacements = [
        ('CK', 'K'),
        ('CI', 'S'),
        ('CY', 'S'),
        ('CE', 'S'),
        ('CH', 'K'),
        ('SH', 'S'),
        ('PH', 'F'),
        ('TH', '0'),
        ('V', 'F'),
        ('Q', 'K'),
        ('X', 'K'),
        ('Z', 'S'),
        ('DG', 'J'),
        ('TCH', 'CH'),
        ('SCH', 'SK'),
    ]
    
    for old, new in replacements:
        name = name.replace(old, new)
    
    # 移除元音
    name = ''.join(c for c in name if not _is_vowel(c))
    
    # 替换W
    name = name.replace('W', '')
    
    # 合并重复
    result = []
    for c in name:
        if not result or result[-1] != c:
            result.append(c)
    
    # 填充到10位
    code = ''.join(result) + '1' * 10
    return code[:10]


# ============== MATCH RATING APPROACH ==============

def match_rating(name: str) -> str:
    """
    Match Rating Approach 编码
    
    简单的语音匹配算法，用于美国人口统计局。
    
    Args:
        name: 输入姓名
    
    Returns:
        MRA编码
    
    Example:
        >>> match_rating('Smith')
        'SMTH'
        >>> match_rating('Schmidt')
        'SCHMDT'
    """
    if not name:
        return ''
    
    name = _normalize(name)
    
    if not name:
        return ''
    
    # 移除所有元音
    result = [name[0]] if name else []
    
    for i, c in enumerate(name[1:], 1):
        if not _is_vowel(c):
            result.append(c)
    
    return ''.join(result)


def match_rating_compare(name1: str, name2: str) -> Tuple[bool, int]:
    """
    使用MRA比较两个姓名
    
    Args:
        name1: 第一个姓名
        name2: 第二个姓名
    
    Returns:
        (是否匹配, 最小匹配长度)
    
    Example:
        >>> match_rating_compare('Smith', 'Schmidt')
        (True, 4)
    """
    code1 = match_rating(name1)
    code2 = match_rating(name2)
    
    # 计算最小匹配长度
    min_len = min(len(code1), len(code2))
    
    # 规则：如果编码长度差大于3，不匹配
    if abs(len(code1) - len(code2)) > 3:
        return (False, min_len)
    
    # 确定最小匹配长度
    total_len = len(code1) + len(code2)
    if total_len <= 4:
        min_match = 1
    elif total_len <= 7:
        min_match = 2
    elif total_len <= 11:
        min_match = 3
    else:
        min_match = 4
    
    # 比较前缀和后缀
    prefix_match = sum(1 for a, b in zip(code1, code2) if a == b)
    
    return (prefix_match >= min_match, min_match)


# ============== LEIN ==============

def lein(name: str) -> str:
    """
    Lein 名称匹配编码
    
    简单的名称匹配算法，保留首字母和辅音。
    
    Args:
        name: 输入姓名
    
    Returns:
        Lein编码
    
    Example:
        >>> lein('Smith')
        'SMTH'
    """
    if not name:
        return ''
    
    name = _normalize(name)
    
    if not name:
        return ''
    
    # 保留首字母
    result = [name[0]]
    
    # 添加辅音
    for c in name[1:]:
        if _is_consonant(c):
            result.append(c)
    
    return ''.join(result)


# ============== 综合比较函数 ==============

def phonetic_similarity(name1: str, name2: str, algorithm: str = 'soundex') -> float:
    """
    计算两个姓名的语音相似度
    
    Args:
        name1: 第一个姓名
        name2: 第二个姓名
        algorithm: 算法名称（soundex, metaphone, nysiis, caverphone）
    
    Returns:
        相似度分数（0.0-1.0）
    
    Example:
        >>> phonetic_similarity('Smith', 'Schmidt')
        1.0
        >>> phonetic_similarity('John', 'Jon')
        1.0
    """
    algorithms = {
        'soundex': soundex,
        'metaphone': metaphone,
        'nysiis': nysiis,
        'caverphone': lambda x: caverphone(x),
        'match_rating': match_rating,
        'lein': lein,
    }
    
    if algorithm not in algorithms:
        raise ValueError(f"未知算法: {algorithm}")
    
    encode_fn = algorithms[algorithm]
    code1 = encode_fn(name1)
    code2 = encode_fn(name2)
    
    # 完全匹配返回1.0
    if code1 == code2:
        return 1.0
    
    # 计算编辑距离
    def edit_distance(s1: str, s2: str) -> int:
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i-1] == s2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
        
        return dp[m][n]
    
    dist = edit_distance(code1, code2)
    max_len = max(len(code1), len(code2))
    
    if max_len == 0:
        return 1.0
    
    return 1.0 - (dist / (2 * max_len))


def match_names(
    name: str,
    candidates: List[str],
    algorithm: str = 'soundex',
    threshold: float = 0.8
) -> List[Tuple[str, float]]:
    """
    在候选列表中查找匹配的姓名
    
    Args:
        name: 目标姓名
        candidates: 候选姓名列表
        algorithm: 算法名称
        threshold: 相似度阈值
    
    Returns:
        匹配结果列表 [(姓名, 相似度), ...]
    
    Example:
        >>> match_names('Smith', ['Schmidt', 'Smyth', 'Johnson'], threshold=0.8)
        [('Schmidt', 1.0), ('Smyth', 1.0)]
    """
    results = []
    
    for candidate in candidates:
        similarity = phonetic_similarity(name, candidate, algorithm)
        if similarity >= threshold:
            results.append((candidate, similarity))
    
    # 按相似度排序
    results.sort(key=lambda x: x[1], reverse=True)
    
    return results


def get_all_encodings(name: str) -> Dict[str, str]:
    """
    获取所有语音编码
    
    Args:
        name: 输入姓名
    
    Returns:
        所有编码的字典
    
    Example:
        >>> get_all_encodings('Smith')
        {'soundex': 'S530', 'metaphone': 'SM0T', ...}
    """
    return {
        'soundex': soundex(name),
        'metaphone': metaphone(name),
        'double_metaphone_primary': double_metaphone(name)[0],
        'double_metaphone_alternate': double_metaphone(name)[1],
        'nysiis': nysiis(name),
        'caverphone': caverphone(name),
        'match_rating': match_rating(name),
        'lein': lein(name),
    }


# ============== 工具函数 ==============

def batch_encode(
    names: List[str],
    algorithm: str = 'soundex'
) -> Dict[str, str]:
    """
    批量编码姓名
    
    Args:
        names: 姓名列表
        algorithm: 算法名称
    
    Returns:
        {姓名: 编码} 字典
    
    Example:
        >>> batch_encode(['Smith', 'Johnson', 'Williams'])
        {'Smith': 'S530', 'Johnson': 'J525', 'Williams': 'W452'}
    """
    algorithms = {
        'soundex': soundex,
        'metaphone': metaphone,
        'nysiis': nysiis,
        'caverphone': lambda x: caverphone(x),
        'match_rating': match_rating,
        'lein': lein,
    }
    
    if algorithm not in algorithms:
        raise ValueError(f"未知算法: {algorithm}")
    
    encode_fn = algorithms[algorithm]
    
    return {name: encode_fn(name) for name in names}


def group_by_phonetic(
    names: List[str],
    algorithm: str = 'soundex'
) -> Dict[str, List[str]]:
    """
    按语音编码分组姓名
    
    Args:
        names: 姓名列表
        algorithm: 算法名称
    
    Returns:
        {编码: [姓名列表]} 字典
    
    Example:
        >>> group_by_phonetic(['Smith', 'Schmidt', 'Johnson'])
        {'S530': ['Smith', 'Schmidt'], 'J525': ['Johnson']}
    """
    algorithms = {
        'soundex': soundex,
        'metaphone': metaphone,
        'nysiis': nysiis,
        'caverphone': lambda x: caverphone(x),
        'match_rating': match_rating,
        'lein': lein,
    }
    
    if algorithm not in algorithms:
        raise ValueError(f"未知算法: {algorithm}")
    
    encode_fn = algorithms[algorithm]
    groups = {}
    
    for name in names:
        code = encode_fn(name)
        if code not in groups:
            groups[code] = []
        groups[code].append(name)
    
    return groups


def find_duplicates(
    names: List[str],
    algorithm: str = 'soundex',
    threshold: float = 0.8
) -> List[List[str]]:
    """
    查找可能的重复姓名
    
    Args:
        names: 姓名列表
        algorithm: 算法名称
        threshold: 相似度阈值
    
    Returns:
        重复姓名组列表
    
    Example:
        >>> find_duplicates(['Smith', 'Schmidt', 'Smyth', 'Johnson'])
        [['Smith', 'Schmidt', 'Smyth']]
    """
    groups = group_by_phonetic(names, algorithm)
    duplicates = []
    
    for code, group in groups.items():
        if len(group) > 1:
            # 进一步验证
            verified = []
            for name in group:
                if all(phonetic_similarity(name, n, algorithm) >= threshold 
                       for n in verified if n != name):
                    verified.append(name)
            
            if len(verified) > 1:
                duplicates.append(verified)
    
    return duplicates


class PhoneticEncoder:
    """
    语音编码器类，提供面向对象的API
    """
    
    def __init__(self, algorithm: str = 'soundex', length: int = 4):
        """
        初始化编码器
        
        Args:
            algorithm: 算法名称
            length: 编码长度
        """
        self.algorithm = algorithm
        self.length = length
        
        self._algorithms = {
            'soundex': lambda x: soundex(x, length),
            'metaphone': lambda x: metaphone(x, length),
            'double_metaphone': lambda x: double_metaphone(x, length),
            'nysiis': nysiis,
            'caverphone': lambda x: caverphone(x),
            'match_rating': match_rating,
            'lein': lein,
        }
    
    def encode(self, name: str) -> str:
        """编码姓名"""
        if self.algorithm not in self._algorithms:
            raise ValueError(f"未知算法: {self.algorithm}")
        return self._algorithms[self.algorithm](name)
    
    def batch_encode(self, names: List[str]) -> List[str]:
        """批量编码"""
        return [self.encode(name) for name in names]
    
    def similarity(self, name1: str, name2: str) -> float:
        """计算相似度"""
        return phonetic_similarity(name1, name2, self.algorithm)
    
    def match(self, name: str, candidates: List[str], threshold: float = 0.8) -> List[Tuple[str, float]]:
        """匹配姓名"""
        return match_names(name, candidates, self.algorithm, threshold)
    
    def __repr__(self):
        return f'PhoneticEncoder(algorithm={self.algorithm!r}, length={self.length})'


if __name__ == '__main__':
    # 演示
    print("=== 语音编码工具演示 ===\n")
    
    names = ['Smith', 'Schmidt', 'Smyth', 'Johnson', 'Johnston', 'Williams']
    
    print("Soundex 编码:")
    for name in names:
        print(f"  {name}: {soundex(name)}")
    
    print("\nMetaphone 编码:")
    for name in names:
        print(f"  {name}: {metaphone(name)}")
    
    print("\nDouble Metaphone 编码:")
    for name in names:
        primary, alternate = double_metaphone(name)
        print(f"  {name}: {primary} / {alternate}")
    
    print("\nNYSIIS 编码:")
    for name in names:
        print(f"  {name}: {nysiis(name)}")
    
    print("\nCaverphone 编码:")
    for name in names:
        print(f"  {name}: {caverphone(name)}")
    
    print("\n匹配测试:")
    matches = match_names('Smith', names, threshold=0.8)
    for name, score in matches:
        print(f"  Smith -> {name}: {score:.2f}")
    
    print("\n所有编码:")
    all_codes = get_all_encodings('Schmidt')
    for algo, code in all_codes.items():
        print(f"  {algo}: {code}")
    
    print("\n重复检测:")
    duplicates = find_duplicates(names)
    for group in duplicates:
        print(f"  {group}")
    
    print("\n=== 演示完成 ===")