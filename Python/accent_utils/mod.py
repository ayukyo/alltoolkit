"""
Accent Utils - 文本重音/变音符号处理工具

功能：
1. 移除文本中的变音符号（如 café -> cafe）
2. 标准化文本用于搜索和比较
3. 支持多种语言的变音符号处理
4. 保留特定语言的特殊字符选项
5. Unicode 规范化支持

零外部依赖，纯 Python 标准库实现。
"""

import unicodedata
from typing import Optional, Set, Dict, Tuple


# 常见变音符号的 Unicode 范围
DIACRITIC_RANGES = [
    (0x0300, 0x036F),  # Combining Diacritical Marks
    (0x1AB0, 0x1AFF),  # Combining Diacritical Marks Extended
    (0x1DC0, 0x1DFF),  # Combining Diacritical Marks Supplement
    (0x20D0, 0x20FF),  # Combining Diacritical Marks for Symbols
    (0xFE20, 0xFE2F),  # Combining Half Marks
]

# 特定语言的字符映射（不使用变音符号的替代）
LANGUAGE_MAPPINGS: Dict[str, Dict[str, str]] = {
    'german': {
        'ä': 'ae', 'ö': 'oe', 'ü': 'ue',
        'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue',
        'ß': 'ss',
    },
    'french': {
        'œ': 'oe', 'Œ': 'Oe',
        'æ': 'ae', 'Æ': 'Ae',
    },
    'turkish': {
        'İ': 'I', 'ı': 'i',
    },
}


def is_diacritic(char: str) -> bool:
    """
    检查字符是否为变音符号（组合字符）
    
    Args:
        char: 要检查的字符
        
    Returns:
        bool: 是否为变音符号
        
    Example:
        >>> is_diacritic('\u0301')  # 组合重音符
        True
        >>> is_diacritic('a')
        False
    """
    if not char:
        return False
    
    code_point = ord(char)
    
    # 检查是否在变音符号范围内
    for start, end in DIACRITIC_RANGES:
        if start <= code_point <= end:
            return True
    
    # 检查 Unicode 类别
    category = unicodedata.category(char)
    return category == 'Mn'  # Mark, Nonspacing


def remove_accents(
    text: str,
    language: Optional[str] = None,
    keep_chars: Optional[Set[str]] = None,
    normalize: bool = True
) -> str:
    """
    移除文本中的变音符号
    
    Args:
        text: 要处理的文本
        language: 语言代码，用于特定语言的映射 ('german', 'french', 'turkish')
        keep_chars: 要保留的完整字符集合（如 {'é', 'ö'}，使用预组合形式）
        normalize: 是否先进行 Unicode 规范化
        
    Returns:
        str: 移除变音符号后的文本
        
    Example:
        >>> remove_accents('café')
        'cafe'
        >>> remove_accents('über', language='german')
        'ueber'
        >>> remove_accents('naïve')
        'naive'
    """
    if not text:
        return text
    
    keep_chars = keep_chars or set()
    
    # 先应用特定语言的映射
    if language and language.lower() in LANGUAGE_MAPPINGS:
        mapping = LANGUAGE_MAPPINGS[language.lower()]
        for old, new in mapping.items():
            if old not in keep_chars:  # 如果在保留集合中则跳过映射
                text = text.replace(old, new)
    
    # Unicode 规范化（NFD 将组合字符分离）
    if normalize:
        # 收集要保留的字符位置
        preserved_positions = {}
        for i, char in enumerate(text):
            if char in keep_chars:
                # 规范化后找到对应位置
                nfd_char = unicodedata.normalize('NFD', char)
                preserved_positions[len(unicodedata.normalize('NFD', text[:i]))] = char
        
        normalized = unicodedata.normalize('NFD', text)
        
        # 移除变音符号，但保留在 keep_chars 中的原始字符
        result = []
        current_base_pos = 0
        
        for char in normalized:
            if is_diacritic(char):
                # 检查是否属于要保留的字符
                if current_base_pos in preserved_positions:
                    # 不移除这个变音符号，稍后会用原字符替换
                    pass
                else:
                    continue  # 移除变音符号
            else:
                # 检查当前位置是否需要用保留字符替换
                if current_base_pos in preserved_positions:
                    # 用原始预组合字符替换
                    result.append(preserved_positions[current_base_pos])
                    # 跳过后续的变音符号（已被包含在预组合字符中）
                else:
                    result.append(char)
                current_base_pos += 1
        
        return ''.join(result)
    
    # 不规范化时直接处理
    result = []
    for char in text:
        if char in keep_chars:
            result.append(char)
        elif not is_diacritic(char):
            result.append(char)
    
    return ''.join(result)


def normalize_text(
    text: str,
    lowercase: bool = True,
    remove_accents_flag: bool = True,
    remove_punctuation: bool = False,
    collapse_whitespace: bool = True,
    language: Optional[str] = None
) -> str:
    """
    标准化文本用于搜索和比较
    
    Args:
        text: 要标准化的文本
        lowercase: 是否转换为小写
        remove_accents_flag: 是否移除变音符号
        remove_punctuation: 是否移除标点符号
        collapse_whitespace: 是否合并多个空白字符
        language: 语言代码
        
    Returns:
        str: 标准化后的文本
        
    Example:
        >>> normalize_text('Café au Lait!')
        'cafe au lait'
        >>> normalize_text('  Café   au  Lait  ', collapse_whitespace=True)
        'cafe au lait'
    """
    if not text:
        return text
    
    result = text
    
    # 移除变音符号
    if remove_accents_flag:
        result = remove_accents(result, language=language)
    
    # 转换为小写
    if lowercase:
        result = result.lower()
    
    # 移除标点符号
    if remove_punctuation:
        result = ''.join(c for c in result if c.isalnum() or c.isspace())
    
    # 合并空白字符
    if collapse_whitespace:
        result = ' '.join(result.split())
    
    return result


def has_accents(text: str) -> bool:
    """
    检查文本是否包含变音符号
    
    Args:
        text: 要检查的文本
        
    Returns:
        bool: 是否包含变音符号
        
    Example:
        >>> has_accents('café')
        True
        >>> has_accents('cafe')
        False
    """
    if not text:
        return False
    
    # 规范化并检查
    normalized = unicodedata.normalize('NFD', text)
    for char in normalized:
        if is_diacritic(char):
            return True
    return False


def count_accents(text: str) -> int:
    """
    统计文本中变音符号的数量
    
    Args:
        text: 要统计的文本
        
    Returns:
        int: 变音符号的数量
        
    Example:
        >>> count_accents('café résumé')
        2
    """
    if not text:
        return 0
    
    count = 0
    normalized = unicodedata.normalize('NFD', text)
    for char in normalized:
        if is_diacritic(char):
            count += 1
    return count


def get_accent_positions(text: str) -> list:
    """
    获取文本中变音符号的位置信息
    
    Args:
        text: 要分析的文本
        
    Returns:
        list: 包含 (位置, 原字符, 基字符) 的列表
        
    Example:
        >>> get_accent_positions('café')
        [(3, 'é', 'e')]
    """
    if not text:
        return []
    
    positions = []
    normalized = unicodedata.normalize('NFD', text)
    
    # 追踪原始字符串位置和规范化字符串位置
    orig_pos = 0
    norm_pos = 0
    base_char = None
    
    for i, char in enumerate(normalized):
        if is_diacritic(char):
            if base_char is not None:
                positions.append((orig_pos - 1, text[orig_pos - 1], base_char))
        else:
            base_char = char
            orig_pos += 1
        norm_pos += 1
    
    return positions


def find_accented_words(text: str) -> list:
    """
    找出文本中包含变音符号的单词
    
    Args:
        text: 要分析的文本
        
    Returns:
        list: 包含变音符号的单词列表
        
    Example:
        >>> find_accented_words('The café has a résumé')
        ['café', 'résumé']
    """
    if not text:
        return []
    
    words = text.split()
    return [word for word in words if has_accents(word)]


def compare_accent_insensitive(text1: str, text2: str, case_insensitive: bool = True) -> bool:
    """
    忽略变音符号比较两个字符串
    
    Args:
        text1: 第一个字符串
        text2: 第二个字符串
        case_insensitive: 是否忽略大小写
        
    Returns:
        bool: 两个字符串是否相等（忽略变音符号）
        
    Example:
        >>> compare_accent_insensitive('café', 'cafe')
        True
        >>> compare_accent_insensitive('Café', 'cafe', case_insensitive=True)
        True
    """
    if case_insensitive:
        text1 = text1.lower()
        text2 = text2.lower()
    
    return remove_accents(text1) == remove_accents(text2)


def accent_insensitive_search(text: str, query: str, case_insensitive: bool = True) -> list:
    """
    在文本中进行忽略变音符号的搜索
    
    Args:
        text: 要搜索的文本
        query: 搜索词
        case_insensitive: 是否忽略大小写
        
    Returns:
        list: 匹配位置的列表 [(start, end, matched_text), ...]
        
    Example:
        >>> accent_insensitive_search('I love café and Café au lait', 'cafe')
        [(7, 11, 'café'), (16, 20, 'Café')]
    """
    results = []
    
    # 标准化搜索词
    normalized_query = remove_accents(query)
    if case_insensitive:
        normalized_query = normalized_query.lower()
    
    # 遍历文本查找匹配
    words = text.split()
    current_pos = 0
    
    for word in words:
        word_start = text.find(word, current_pos)
        word_end = word_start + len(word)
        
        normalized_word = remove_accents(word)
        if case_insensitive:
            normalized_word = normalized_word.lower()
        
        if normalized_word == normalized_query:
            results.append((word_start, word_end, word))
        
        current_pos = word_end
    
    return results


def transliterate_to_ascii(text: str, language: Optional[str] = None) -> str:
    """
    将文本音译为纯 ASCII 字符
    
    Args:
        text: 要处理的文本
        language: 语言代码
        
    Returns:
        str: ASCII 文本
        
    Example:
        >>> transliterate_to_ascii('你好世界')  # 中文会被移除
        ''
        >>> transliterate_to_ascii('café résumé')
        'cafe resume'
        >>> transliterate_to_ascii('über', language='german')
        'ueber'
    """
    if not text:
        return text
    
    # 先移除变音符号
    result = remove_accents(text, language=language)
    
    # 移除非 ASCII 字符
    result = ''.join(c for c in result if ord(c) < 128)
    
    return result


def detect_language_from_accents(text: str) -> list:
    """
    根据变音符号推测文本语言
    
    Args:
        text: 要分析的文本
        
    Returns:
        list: 可能的语言列表，按可能性排序
        
    Example:
        >>> detect_language_from_accents('über')
        ['german']
        >>> detect_language_from_accents('café')
        ['french']
    """
    if not text:
        return []
    
    languages = []
    
    # 检查德语特征
    if 'ü' in text or 'ä' in text or 'ö' in text or 'ß' in text:
        languages.append('german')
    
    # 检查法语特征
    if 'é' in text or 'è' in text or 'ê' in text or 'ç' in text or 'œ' in text:
        languages.append('french')
    
    # 检查西班牙语特征
    if 'ñ' in text or '¿' in text or '¡' in text:
        languages.append('spanish')
    
    # 检查葡萄牙语特征
    if 'ã' in text or 'õ' in text:
        languages.append('portuguese')
    
    # 检查波兰语特征
    if 'ł' in text or 'ż' in text or 'ś' in text:
        languages.append('polish')
    
    # 检查捷克语特征
    if 'ř' in text or 'ů' in text:
        languages.append('czech')
    
    # 检查土耳其语特征
    if 'İ' in text or 'ı' in text or 'ğ' in text or 'ş' in text:
        languages.append('turkish')
    
    # 检查北欧语言特征
    if 'å' in text or 'ø' in text:
        if 'æ' in text:
            languages.append('norwegian')
        else:
            languages.append('swedish')
    
    # 检查中文特征
    try:
        if any('\u4e00' <= c <= '\u9fff' for c in text):
            languages.append('chinese')
    except:
        pass
    
    return languages


class AccentNormalizer:
    """
    变音符号规范化器类，用于批量处理文本
    
    Example:
        >>> normalizer = AccentNormalizer(language='german')
        >>> normalizer.normalize('über')
        'ueber'
    """
    
    def __init__(
        self,
        language: Optional[str] = None,
        keep_chars: Optional[Set[str]] = None,
        lowercase: bool = False,
        remove_punctuation: bool = False
    ):
        """
        初始化规范化器
        
        Args:
            language: 语言代码
            keep_chars: 要保留的字符集合
            lowercase: 是否转换为小写
            remove_punctuation: 是否移除标点符号
        """
        self.language = language
        self.keep_chars = keep_chars or set()
        self.lowercase = lowercase
        self.remove_punctuation = remove_punctuation
    
    def normalize(self, text: str) -> str:
        """
        规范化文本
        
        Args:
            text: 要规范化的文本
            
        Returns:
            str: 规范化后的文本
        """
        return normalize_text(
            text,
            lowercase=self.lowercase,
            remove_accents_flag=True,
            remove_punctuation=self.remove_punctuation,
            language=self.language
        )
    
    def compare(self, text1: str, text2: str) -> bool:
        """
        比较两个字符串是否相等（忽略变音符号）
        
        Args:
            text1: 第一个字符串
            text2: 第二个字符串
            
        Returns:
            bool: 是否相等
        """
        return compare_accent_insensitive(text1, text2, case_insensitive=self.lowercase)
    
    def search(self, text: str, query: str) -> list:
        """
        在文本中搜索（忽略变音符号）
        
        Args:
            text: 要搜索的文本
            query: 搜索词
            
        Returns:
            list: 匹配结果
        """
        return accent_insensitive_search(text, query, case_insensitive=self.lowercase)


# 导出的公共 API
__all__ = [
    'is_diacritic',
    'remove_accents',
    'normalize_text',
    'has_accents',
    'count_accents',
    'get_accent_positions',
    'find_accented_words',
    'compare_accent_insensitive',
    'accent_insensitive_search',
    'transliterate_to_ascii',
    'detect_language_from_accents',
    'AccentNormalizer',
    'DIACRITIC_RANGES',
    'LANGUAGE_MAPPINGS',
]