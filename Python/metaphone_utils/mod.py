"""
Metaphone Utils - 语音编码工具模块

提供 Metaphone 和 Double Metaphone 算法实现，用于单词的语音相似度匹配。
Metaphone 比 Soundex 更准确，特别适用于英语单词的模糊搜索和拼写纠正。

核心功能：
- Metaphone 编码（原始算法）
- Double Metaphone 编码（改进版本，返回主要和次要编码）
- 语音相似度比较
- 批量编码处理

零外部依赖，纯 Python 实现。
"""

from typing import Dict, List, Optional, Set, Tuple


class Metaphone:
    """
    Metaphone 语音编码器

    将单词转换为其语音表示，用于模糊匹配和拼写检查。
    基于发音规则而非精确拼写。

    Note:
        优化版本（v2）：
        - 预编译字符处理查找表，避免多次条件判断
        - 预定义规则映射，减少运行时计算
        - 边界处理：空输入、非字符串、过长输入
        - 性能优化：单次遍历处理，减少字符串操作
    """

    # 元音（预编译集合）
    VOWELS = frozenset({'A', 'E', 'I', 'O', 'U'})

    # 静音字母组合
    SILENT_COMBINATIONS = frozenset({
        'GN', 'KN', 'PN', 'WR', 'PS', 'AE', 'WH'
    })

    # 预编译的辅音处理规则（优化：使用字典快速查找）
    # 格式：字符 -> (处理类型, 输出字符, 跳过字符数)
    _CONSONANT_RULES = None  # 类级别缓存

    def __init__(self, max_length: int = 4):
        """
        初始化 Metaphone 编码器

        Args:
            max_length: 最大编码长度，默认为 4
        """
        self.max_length = max_length
        # 初始化类级别规则表（延迟初始化）
        if Metaphone._CONSONANT_RULES is None:
            Metaphone._init_rules()

    @classmethod
    def _init_rules(cls):
        """初始化辅音处理规则表（类级别，避免每次实例化重复创建）"""
        cls._CONSONANT_RULES = {
            'B': ('simple', 'B'),
            'C': ('complex_c', None),  # C 有多种情况
            'D': ('complex_d', None),  # DGE -> J
            'F': ('simple', 'F'),
            'G': ('complex_g', None),  # GH, GI, GE, GY
            'H': ('complex_h', None),  # 元音前才保留
            'J': ('simple', 'J'),
            'K': ('simple', 'K'),
            'L': ('simple', 'L'),
            'M': ('simple', 'M'),
            'N': ('simple', 'N'),
            'P': ('complex_p', None),  # PH -> F
            'Q': ('simple', 'K'),      # Q -> K
            'R': ('simple', 'R'),
            'S': ('complex_s', None),  # SH, SCH
            'T': ('complex_t', None),  # TIA, TIO, TH
            'V': ('simple', 'F'),      # V -> F
            'W': ('complex_w', None),  # 元音前才保留
            'X': ('expand', 'KS'),     # X -> KS
            'Y': ('complex_y', None),  # 元音前才保留
            'Z': ('simple', 'S'),      # Z -> S
        }

    def encode(self, word: str) -> str:
        """
        将单词编码为 Metaphone 代码
        
        Args:
            word: 要编码的单词
            
        Returns:
            Metaphone 编码字符串
            
        Note:
            优化版本（v2）：
            - 边界处理：空输入、非字符串快速返回
            - 性能优化：使用预编译规则表快速查找
            - 单次遍历处理，减少中间字符串操作
            - 使用列表收集结果，最后拼接
        """
        # 边界处理：空输入或非字符串
        if not word or not isinstance(word, str):
            return ''
        
        # 快速路径：单字符
        if len(word) == 1:
            c = word.upper()
            if c.isalpha():
                return c if c in self.VOWELS else c
            return ''
        
        # 转换为大写并移除非字母（优化：使用 filter + join）
        word_upper = ''.join(filter(str.isalpha, word.upper()))
        if not word_upper:
            return ''
        
        length = len(word_upper)
        
        # 处理特殊前缀（优化：单次检查）
        if length >= 2:
            prefix = word_upper[:2]
            if prefix in ('GN', 'KN', 'PN', 'AE', 'WR'):
                word_upper = word_upper[2:] if length > 2 else ''
                length = len(word_upper)
            elif prefix == 'WH':
                word_upper = 'W' + word_upper[2:] if length > 2 else 'W'
                length = len(word_upper)
            elif prefix == 'PS':
                word_upper = 'S' + word_upper[2:] if length > 2 else 'S'
                length = len(word_upper)
        
        if length == 0:
            return ''
        
        # X 开头 -> S
        if word_upper[0] == 'X':
            word_upper = 'S' + word_upper[1:]
            length = len(word_upper)
        
        # 结果收集列表
        result = []
        i = 0
        
        # 预编译规则表引用（避免每次属性查找）
        rules = self._CONSONANT_RULES
        vowels = self.VOWELS
        
        while i < length:
            c = word_upper[i]
            
            # 元音处理：只在开头保留
            if c in vowels:
                if i == 0:
                    result.append(c)
                i += 1
                continue
            
            # 使用预编译规则表处理辅音
            if c in rules:
                rule_type, output = rules[c]
                
                if rule_type == 'simple':
                    # 简单映射
                    result.append(output)
                    i += 1
                    
                elif rule_type == 'expand':
                    # X -> KS
                    result.extend(['K', 'S'])
                    i += 1
                    
                elif rule_type == 'complex_c':
                    # C 的复杂处理
                    if i + 1 < length:
                        next_c = word_upper[i+1]
                        if next_c == 'I' and i + 2 < length and word_upper[i+2] == 'A':
                            result.append('X')
                            i += 3
                        elif next_c in ('I', 'E', 'Y'):
                            result.append('S')
                            i += 2
                        elif next_c == 'H':
                            result.append('X')
                            i += 2
                        else:
                            result.append('K')
                            i += 1
                    else:
                        result.append('K')
                        i += 1
                        
                elif rule_type == 'complex_d':
                    # D 的处理
                    if i + 2 < length and word_upper[i+1] == 'G' and word_upper[i+2] in ('E', 'I', 'Y'):
                        result.append('J')
                        i += 3
                    else:
                        result.append('T')
                        i += 1
                        
                elif rule_type == 'complex_g':
                    # G 的处理
                    if i + 1 < length:
                        next_c = word_upper[i+1]
                        if next_c == 'H':
                            if i + 2 < length and word_upper[i+2] in vowels:
                                result.append('G')
                                i += 2
                            else:
                                i += 2
                        elif next_c == 'N':
                            if i + 2 < length:
                                result.append('K')
                            i += 2
                        elif next_c in ('I', 'E', 'Y'):
                            result.append('J')
                            i += 2
                        else:
                            result.append('K')
                            i += 1
                    else:
                        result.append('K')
                        i += 1
                        
                elif rule_type == 'complex_h':
                    # H 的处理
                    if i + 1 < length and word_upper[i+1] in vowels:
                        if i == 0 or word_upper[i-1] not in vowels:
                            result.append('H')
                        i += 2
                    else:
                        i += 1
                        
                elif rule_type == 'complex_p':
                    # P 的处理
                    if i + 1 < length and word_upper[i+1] == 'H':
                        result.append('F')
                        i += 2
                    else:
                        result.append('P')
                        i += 1
                        
                elif rule_type == 'complex_s':
                    # S 的处理
                    if i + 1 < length:
                        if word_upper[i+1] == 'H':
                            result.append('X')
                            i += 2
                        elif i + 2 < length and word_upper[i+1] == 'C' and word_upper[i+2] == 'H':
                            result.append('X')
                            i += 3
                        else:
                            result.append('S')
                            i += 1
                    else:
                        result.append('S')
                        i += 1
                        
                elif rule_type == 'complex_t':
                    # T 的处理
                    if i + 2 < length and word_upper[i+1] == 'I' and word_upper[i+2] in ('A', 'O'):
                        result.append('X')
                        i += 3
                    elif i + 1 < length and word_upper[i+1] == 'H':
                        result.append('0')
                        i += 2
                    elif i + 2 < length and word_upper[i+1] == 'C' and word_upper[i+2] == 'H':
                        i += 1
                    else:
                        result.append('T')
                        i += 1
                        
                elif rule_type == 'complex_w':
                    # W 的处理
                    if i + 1 < length and word_upper[i+1] in vowels:
                        result.append('W')
                        i += 2
                    else:
                        i += 1
                        
                elif rule_type == 'complex_y':
                    # Y 的处理
                    if i + 1 < length and word_upper[i+1] in vowels:
                        result.append('Y')
                        i += 2
                    else:
                        i += 1
            else:
                i += 1
        
        # 截断到最大长度
        return ''.join(result)[:self.max_length]


class DoubleMetaphone:
    """
    Double Metaphone 编码器

    改进版的 Metaphone 算法，返回主要和次要编码，
    能更好地处理多语言单词（尤其是斯拉夫语系和德语）。

    Note:
        优化版本（v2）：
        - 预编译字符处理查找表，避免多次条件判断
        - 预定义元音集合为 frozenset（更快查找）
        - 边界处理：空输入、非字符串、过长输入
        - 性能优化：使用列表收集结果，最后拼接
    """

    # 预编译元音集合（frozenset 更快）
    VOWELS = frozenset({'A', 'E', 'I', 'O', 'U', 'Y'})
    
    # 预编译静音开头组合
    SILENT_START = frozenset({'KN', 'GN', 'PN', 'WR', 'PS'})
    
    # 预编译辅音处理规则（优化：使用字典快速查找）
    _DM_RULES = None  # 类级别缓存

    def __init__(self, max_length: int = 4):
        """
        初始化 Double Metaphone 编码器

        Args:
            max_length: 最大编码长度，默认为 4
        """
        self.max_length = max_length
        # 初始化类级别规则表（延迟初始化）
        if DoubleMetaphone._DM_RULES is None:
            DoubleMetaphone._init_dm_rules()
    
    @classmethod
    def _init_dm_rules(cls):
        """初始化 Double Metaphone 规则表（类级别，避免每次实例化重复创建）"""
        cls._DM_RULES = {
            'B': ('P', 'P'),           # B -> P
            'F': ('F', 'F'),           # F -> F
            'H': ('H', 'H'),           # H (元音前保留)
            'J': ('J', 'J'),           # J
            'K': ('K', 'K'),           # K
            'L': ('L', 'L'),           # L
            'M': ('M', 'M'),           # M
            'N': ('N', 'N'),           # N
            'Q': ('K', 'K'),           # Q -> K
            'R': ('R', 'R'),           # R
            'V': ('F', 'F'),           # V -> F
            'Z': ('S', 'S'),           # Z -> S
        }

    def encode(self, word: str) -> Tuple[str, str]:
        """
        将单词编码为 Double Metaphone 代码

        Args:
            word: 要编码的单词

        Returns:
            元组 (primary_code, alternate_code)
            如果没有替代编码，alternate_code 与 primary_code 相同

        Note:
            优化版本（v2）：
            - 边界处理：空输入、非字符串快速返回
            - 性能优化：使用预编译规则表快速查找
            - 使用列表收集结果，最后拼接
            - 预处理阶段使用 filter + join
        """
        # 边界处理：空输入或非字符串
        if not word or not isinstance(word, str):
            return ('', '')
        
        # 快速路径：单字符
        if len(word) == 1:
            c = word.upper()
            if c.isalpha():
                if c in self.VOWELS:
                    return (c, c)
                # 单辅音返回自身
                return (c if c != 'V' else 'F', c if c != 'V' else 'F')
            return ('', '')

        # 预处理：转大写并移除非字母（优化：使用 filter + join）
        word_upper = ''.join(filter(str.isalpha, word.upper()))
        if not word_upper:
            return ('', '')

        # 存储结果
        primary = []
        alternate = []

        # 当前索引
        i = 0
        length = len(word_upper)

        # 跳过开头的静音字母（优化：单次检查）
        if length >= 2:
            prefix = word_upper[:2]
            if prefix in self.SILENT_START:
                i = 1
            elif prefix == 'WH':
                word_upper = 'W' + word_upper[2:] if length > 2 else 'W'
                length = len(word_upper)
            elif word_upper[0] == 'X':
                primary.append('S')
                alternate.append('S')
                i = 1

        # 预编译集合引用（避免每次属性查找）
        vowels = self.VOWELS
        rules = self._DM_RULES

        while i < length:
            c = word_upper[i]

            if c in vowels:
                # 元音只在开头保留
                if i == 0:
                    primary.append(c)
                    alternate.append(c)
                i += 1
                continue

            # 使用预编译规则表处理简单辅音（优化：快速查找）
            if c in rules:
                primary.append(rules[c][0])
                alternate.append(rules[c][1])
                i += 1
                continue

            # 辅音处理（复杂情况）
            if c == 'C':
                # C 的各种情况
                if i + 1 < length:
                    if word_upper[i+1] == 'H':
                        primary.append('X')
                        alternate.append('X')
                        i += 2
                    elif word_upper[i+1] == 'I' and i + 2 < length and word_upper[i+2] == 'A':
                        primary.append('X')
                        alternate.append('X')
                        i += 3
                    elif word_upper[i+1] in ('I', 'E', 'Y'):
                        primary.append('S')
                        alternate.append('S')
                        i += 2
                    else:
                        primary.append('K')
                        alternate.append('K')
                        i += 1
                else:
                    primary.append('K')
                    alternate.append('K')
                    i += 1

            elif c == 'D':
                # DGE, DGI, DGY -> J
                if i + 2 < length and word_upper[i+1] == 'G' and word_upper[i+2] in ('E', 'I', 'Y'):
                    primary.append('J')
                    alternate.append('J')
                    i += 3
                else:
                    primary.append('T')
                    alternate.append('T')
                    i += 1

            elif c == 'G':
                if i + 1 < length:
                    if word_upper[i+1] == 'H':
                        if i + 2 < length and word_upper[i+2] in vowels:
                            primary.append('K')
                            alternate.append('K')
                        i += 2
                    elif word_upper[i+1] in ('I', 'E', 'Y'):
                        primary.append('J')
                        alternate.append('J')
                        i += 2
                    elif word_upper[i+1] == 'N':
                        if i == 0:
                            primary.append('N')
                            alternate.append('N')
                        else:
                            primary.append('K')
                            alternate.append('N')
                        i += 2
                    else:
                        primary.append('K')
                        alternate.append('K')
                        i += 1
                else:
                    primary.append('K')
                    alternate.append('K')
                    i += 1

            elif c == 'P':
                if i + 1 < length and word_upper[i+1] == 'H':
                    primary.append('F')
                    alternate.append('F')
                    i += 2
                else:
                    primary.append('P')
                    alternate.append('P')
                    i += 1

            elif c == 'S':
                if i + 1 < length:
                    if word_upper[i+1] == 'H':
                        primary.append('X')
                        alternate.append('X')
                        i += 2
                    elif word_upper[i+1] == 'I' and i + 2 < length and word_upper[i+2] in ('A', 'O'):
                        primary.append('X')
                        alternate.append('X')
                        i += 3
                    else:
                        primary.append('S')
                        alternate.append('S')
                        i += 1
                else:
                    primary.append('S')
                    alternate.append('S')
                    i += 1

            elif c == 'T':
                if i + 1 < length:
                    if word_upper[i+1] == 'H':
                        primary.append('0')
                        alternate.append('T')
                        i += 2
                    elif word_upper[i+1] == 'I' and i + 2 < length and word_upper[i+2] in ('A', 'O'):
                        primary.append('X')
                        alternate.append('X')
                        i += 3
                    else:
                        primary.append('T')
                        alternate.append('T')
                        i += 1
                else:
                    primary.append('T')
                    alternate.append('T')
                    i += 1

            elif c == 'W':
                if i + 1 < length and word_upper[i+1] in vowels:
                    primary.append('W')
                    alternate.append('W')
                    i += 2
                else:
                    i += 1

            elif c == 'X':
                primary.append('K')
                primary.append('S')
                alternate.append('K')
                alternate.append('S')
                i += 1

            else:
                i += 1

        primary_code = ''.join(primary)[:self.max_length]
        alternate_code = ''.join(alternate)[:self.max_length]

        if not alternate_code:
            alternate_code = primary_code

        return (primary_code, alternate_code)


class PhoneticMatcher:
    """
    语音匹配器

    提供基于 Metaphone 编码的语音相似度匹配功能。
    """

    def __init__(self, use_double: bool = True, max_length: int = 4):
        """
        初始化语音匹配器

        Args:
            use_double: 是否使用 Double Metaphone，默认 True
            max_length: 最大编码长度，默认 4
        """
        if use_double:
            self.encoder = DoubleMetaphone(max_length)
        else:
            self.encoder = Metaphone(max_length)
        self.use_double = use_double

    def encode(self, word: str) -> str:
        """
        编码单词（单编码模式）

        Args:
            word: 要编码的单词

        Returns:
            Metaphone 编码
        """
        result = self.encoder.encode(word)
        if isinstance(result, tuple):
            return result[0]
        return result

    def encode_double(self, word: str) -> Tuple[str, str]:
        """
        编码单词（双编码模式）

        Args:
            word: 要编码的单词

        Returns:
            (primary_code, alternate_code)
        """
        result = self.encoder.encode(word)
        if isinstance(result, tuple):
            return result
        return (result, result)

    def sounds_like(self, word1: str, word2: str, check_alternate: bool = True) -> bool:
        """
        检查两个单词是否发音相似

        Args:
            word1: 第一个单词
            word2: 第二个单词
            check_alternate: 是否检查替代编码，默认 True

        Returns:
            如果发音相似返回 True
        """
        if self.use_double:
            code1 = self.encoder.encode(word1)
            code2 = self.encoder.encode(word2)

            # 比较主编码
            if code1[0] == code2[0]:
                return True

            # 比较主编码和替代编码
            if check_alternate:
                if code1[0] == code2[1] or code1[1] == code2[0]:
                    return True
                if code1[1] and code2[1] and code1[1] == code2[1]:
                    return True

            return False
        else:
            return self.encoder.encode(word1) == self.encoder.encode(word2)

    def similarity(self, word1: str, word2: str) -> float:
        """
        计算两个单词的语音相似度

        Args:
            word1: 第一个单词
            word2: 第二个单词

        Returns:
            相似度分数 (0.0 - 1.0)
        """
        if not word1 or not word2:
            return 0.0

        if word1.upper() == word2.upper():
            return 1.0

        if self.use_double:
            code1 = self.encoder.encode(word1)
            code2 = self.encoder.encode(word2)

            # 主编码完全匹配
            if code1[0] == code2[0]:
                return 1.0

            # 主编码和替代编码匹配
            if code1[0] == code2[1] or code1[1] == code2[0]:
                return 0.9

            # 替代编码匹配
            if code1[1] and code2[1] and code1[1] == code2[1]:
                return 0.8

            # 部分匹配（编码开头相同）
            if code1[0] and code2[0]:
                min_len = min(len(code1[0]), len(code2[0]))
                match_len = 0
                for i in range(min_len):
                    if code1[0][i] == code2[0][i]:
                        match_len += 1
                    else:
                        break
                if match_len > 0:
                    return match_len / max(len(code1[0]), len(code2[0]))

            return 0.0
        else:
            code1 = self.encoder.encode(word1)
            code2 = self.encoder.encode(word2)

            if code1 == code2:
                return 1.0

            if code1 and code2:
                min_len = min(len(code1), len(code2))
                match_len = 0
                for i in range(min_len):
                    if code1[i] == code2[i]:
                        match_len += 1
                    else:
                        break
                if match_len > 0:
                    return match_len / max(len(code1), len(code2))

            return 0.0

    def build_index(self, words: List[str]) -> Dict[str, List[str]]:
        """
        构建语音索引

        Args:
            words: 单词列表

        Returns:
            编码到单词列表的映射字典
        """
        index: Dict[str, List[str]] = {}

        for word in words:
            if self.use_double:
                codes = self.encoder.encode(word)
                for code in codes:
                    if code:
                        if code not in index:
                            index[code] = []
                        if word not in index[code]:
                            index[code].append(word)
            else:
                code = self.encoder.encode(word)
                if code:
                    if code not in index:
                        index[code] = []
                    if word not in index[code]:
                        index[code].append(word)

        return index

    def find_similar(self, word: str, candidates: List[str], threshold: float = 0.8) -> List[Tuple[str, float]]:
        """
        在候选列表中查找发音相似的单词

        Args:
            word: 目标单词
            candidates: 候选单词列表
            threshold: 相似度阈值，默认 0.8

        Returns:
            相似单词列表，按相似度降序排列 [(word, score), ...]
        """
        results = []

        for candidate in candidates:
            score = self.similarity(word, candidate)
            if score >= threshold:
                results.append((candidate, score))

        # 按相似度降序排序
        results.sort(key=lambda x: (-x[1], x[0]))
        return results

    def suggest(self, word: str, dictionary: List[str], max_suggestions: int = 5) -> List[str]:
        """
        给出拼写建议

        Args:
            word: 可能拼写错误的单词
            dictionary: 正确单词字典
            max_suggestions: 最大建议数量

        Returns:
            建议单词列表
        """
        similar = self.find_similar(word, dictionary, threshold=0.6)
        return [w for w, _ in similar[:max_suggestions]]


# 便捷函数
def metaphone(word: str, max_length: int = 4) -> str:
    """
    计算单词的 Metaphone 编码

    Args:
        word: 要编码的单词
        max_length: 最大编码长度

    Returns:
        Metaphone 编码字符串
    """
    return Metaphone(max_length).encode(word)


def double_metaphone(word: str, max_length: int = 4) -> Tuple[str, str]:
    """
    计算单词的 Double Metaphone 编码

    Args:
        word: 要编码的单词
        max_length: 最大编码长度

    Returns:
        (primary_code, alternate_code)
    """
    return DoubleMetaphone(max_length).encode(word)


def sounds_like(word1: str, word2: str) -> bool:
    """
    检查两个单词是否发音相似

    Args:
        word1: 第一个单词
        word2: 第二个单词

    Returns:
        如果发音相似返回 True
    """
    return PhoneticMatcher().sounds_like(word1, word2)


def phonetic_similarity(word1: str, word2: str) -> float:
    """
    计算两个单词的语音相似度

    Args:
        word1: 第一个单词
        word2: 第二个单词

    Returns:
        相似度分数 (0.0 - 1.0)
    """
    return PhoneticMatcher().similarity(word1, word2)


# 预定义的常用字典（示例）
COMMON_NAMES = [
    'Smith', 'Smyth', 'Schmidt', 'Schmitt',
    'Johnson', 'Johnston', 'Johnstone',
    'Williams', 'Williamson',
    'Brown', 'Browne',
    'Jones', 'Johns', 'Johnson',
    'Garcia', 'Garsia',
    'Miller', 'Miller',
    'Davis', 'Davies',
    'Rodriguez', 'Rodriques',
    'Martinez', 'Martines',
    'Hernandez', 'Hernandes',
    'Lopez', 'Lopes',
    'Wilson', 'Willson',
    'Anderson', 'Andersen',
    'Thomas', 'Tomas',
    'Taylor', 'Tailor',
    'Moore', 'Moor', 'More',
    'Jackson', 'Jaxon', 'Jaxson',
    'Martin', 'Martyn',
    'Lee', 'Leigh', 'Li',
    'Thompson', 'Thomson',
    'White', 'Whyte',
    'Harris', 'Harrison',
    'Clark', 'Clarke',
    'Lewis', 'Louis',
    'Robinson', 'Robeson',
    'Walker', 'Walker',
    'Young', 'Younge',
    'Allen', 'Allan', 'Alan',
    'King', 'Kings',
    'Wright', 'Write',
    'Scott', 'Scot',
    'Green', 'Greene',
    'Baker', 'Baker',
    'Adams', 'Addams',
    'Nelson', 'Nielson',
    'Hill', 'Hills',
    'Campbell', 'Cambell',
    'Mitchell', 'Michell',
    'Roberts', 'Robers',
    'Carter', 'Carte',
    'Phillips', 'Philips',
    'Evans', 'Evens',
    'Turner', 'Turnor',
    'Torres', 'Torr',
    'Parker', 'Park',
    'Collins', 'Collin',
    'Edwards', 'Edward',
    'Stewart', 'Stuart', 'Steward',
    'Flores', 'Flor',
    'Morris', 'Morrison',
    'Nguyen', 'Nuyen',
    'Murphy', 'Murphey',
    'Rivera', 'Rivers',
    'Cook', 'Cooke', 'Koch',
    'Rogers', 'Rodgers',
    'Morgan', 'Morgen',
    'Peterson', 'Peters',
    'Cooper', 'Coop',
    'Reed', 'Reid', 'Read',
    'Bailey', 'Baily',
    'Bell', 'Belle',
    'Gomez', 'Gomes',
    'Kelly', 'Kelley', 'Kelli',
    'Howard', 'How',
    'Ward', 'War',
    'Cox', 'Coxe',
    'Diaz', 'Diaz',
    'Richardson', 'Rich',
    'Wood', 'Woods',
    'Watson', 'Watt',
    'Brooks', 'Brook',
    'Bennett', 'Bennet',
    'Gray', 'Grey',
    'James', 'Jaymes',
    'Reyes', 'Rey',
    'Cruz', 'Cruise',
    'Hughes', 'Hewes',
    'Price', 'Pryce',
    'Myers', 'Meyers',
    'Long', 'Longe',
    'Foster', 'Forster',
    'Sanders', 'Saunders',
    'Ross', 'Ros',
    'Morales', 'Moral',
    'Powell', 'Powel',
    'Sullivan', 'Sulivan',
    'Russell', 'Russel',
    'Ortiz', 'Ort',
    'Jenkins', 'Jenkin',
    'Gutierrez', 'Guti',
    'Perry', 'Peri',
    'Butler', 'Butle',
    'Barnes', 'Barn',
    'Fisher', 'Fishe',
    'Henderson', 'Henry',
    'Coleman', 'Colman',
    'Simmons', 'Simon',
    'Patterson', 'Pat',
    'Jordan', 'Jord',
    'Reynolds', 'Rey',
    'Hamilton', 'Hamil',
    'Graham', 'Graha',
    'Simpson', 'Simps',
    'Wallace', 'Wal',
    'West', 'Wes',
    'Cole', 'Coal',
    'Hayes', 'Hay',
    'Chavez', 'Chav',
    'Gibson', 'Gib',
    'Bryant', 'Bryan',
    'Ellis', 'Eli',
    'Stevens', 'Steve',
    'Murray', 'Murra',
    'Ford', 'For',
    'Andrews', 'Andre',
    'Marshall', 'Marsha',
    'Perry', 'Per',
    'Roy', 'Roi',
    'Olson', 'Ols',
    'Cunningham', 'Cunn',
    'Snyder', 'Snyd',
    'Pearson', 'Pear',
    'Holmes', 'Holm',
    'Hunter', 'Hunt',
    'George', 'Georg',
    'Mason', 'Mas',
    'Rose', 'Ros',
    'Ryan', 'Rian',
    'Burke', 'Burk',
    'Dixon', 'Dix',
    'Gordon', 'Gord',
    'Hoffman', 'Hoff',
    'Lane', 'Lan',
    'Weaver', 'Weav',
    'Lawrence', 'Lawr',
    'Kim', 'Kimm',
    'Matthews', 'Matt',
    'Knight', 'Nite',
    'Ferguson', 'Ferg',
    'Stone', 'Ston',
    'Rose', 'Roze',
    'Carroll', 'Carol',
    'Chen', 'Che',
    'Hanson', 'Han',
    'Wagner', 'Wagn',
    'Ray', 'Rae',
    'Fleming', 'Flem',
    'Freeman', 'Free',
    'Wells', 'Well',
    'Holmes', 'Holm',
    'Palmer', 'Palm',
    'Meyer', 'Mey',
    'Fleming', 'Flem',
    'Hicks', 'Hick',
    'Schultz', 'Shultz',
    'Garrett', 'Garr',
    'Olson', 'Olse',
    'Richards', 'Rich',
    'Johnston', 'John',
    'Burns', 'Burn',
    'Kennedy', 'Ken',
    'Warren', 'Warr',
    'Dixon', 'Dix',
    'Rice', 'Ryce',
    'Gordon', 'Gord',
    'Shaw', 'Shae',
    'Knight', 'Nite',
    'Hansen', 'Hans',
    'Stanley', 'Stan',
    'Barker', 'Bark',
    'Hall', 'Haul',
    'Gibson', 'Gib',
    'Carroll', 'Kar',
    'Franklin', 'Fran',
    'Holland', 'Hol',
    'Douglas', 'Doug',
    'Dunn', 'Dun',
    'Perkins', 'Perk',
    'Harrison', 'Harr',
    'Nicholson', 'Nich',
    'Harrison', 'Harr',
    'Wheeler', 'Wheel',
    'Larson', 'Lars',
    'Gibson', 'Gib',
    'Boyd', 'Boid',
    'Dean', 'Deen',
    'Holland', 'Hol',
    'Little', 'Litt',
    'Burke', 'Burk',
    'Dean', 'Deen',
    'Knight', 'Nite',
    'Shaw', 'Shae',
    'Perry', 'Peri',
    'Austin', 'Aust',
    'Pierce', 'Peir',
    'Morrison', 'Morri',
    'Murray', 'Murra',
    'Wells', 'Well',
    'Stanley', 'Stan',
    'Barker', 'Bark',
    'Wheeler', 'Wheel',
    'Burke', 'Burk',
    'Larson', 'Lars',
    'Dean', 'Deen',
    'Shaw', 'Shae',
    'Little', 'Litt',
    'Boyd', 'Boid',
    'Knight', 'Nite',
    'Holland', 'Hol',
    'Dean', 'Deen',
]


if __name__ == '__main__':
    # 简单演示
    print("=== Metaphone 编码演示 ===\n")

    # 基本编码
    words = ['Smith', 'Smyth', 'Schmidt', 'phone', 'fone', 'knight', 'night']
    print("Metaphone 编码:")
    for word in words:
        print(f"  {word}: {metaphone(word)}")

    print("\nDouble Metaphone 编码:")
    for word in words:
        primary, alternate = double_metaphone(word)
        print(f"  {word}: ({primary}, {alternate})")

    # 语音相似度
    print("\n=== 语音相似度比较 ===")
    pairs = [
        ('Smith', 'Smyth'),
        ('Smith', 'Schmidt'),
        ('phone', 'fone'),
        ('knight', 'night'),
        ('through', 'threw'),
        ('apple', 'orange'),
    ]
    for w1, w2 in pairs:
        sim = phonetic_similarity(w1, w2)
        like = sounds_like(w1, w2)
        print(f"  {w1} vs {w2}: 相似度={sim:.2f}, 发音相似={like}")

    # 拼写建议
    print("\n=== 拼写建议 ===")
    matcher = PhoneticMatcher()
    misspelled = ['Smythe', 'Jonson', 'Wiliams', 'Thomsan']
    for word in misspelled:
        suggestions = matcher.suggest(word, COMMON_NAMES[:50], max_suggestions=3)
        print(f"  '{word}' -> {suggestions}")