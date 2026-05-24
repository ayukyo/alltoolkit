"""
Width Utilities - 字符串显示宽度计算工具

用于计算字符串在终端/等宽字体环境中的显示宽度。

核心功能:
- 计算字符串的显示宽度（考虑 CJK 宽字符、Emoji 等）
- 支持截断字符串到指定宽度
- 支持填充字符串到指定宽度
- 支持宽字符检测和分类

零外部依赖，纯 Python 实现。
"""

import unicodedata
from typing import Tuple, List, Optional
from enum import IntEnum


class Width(IntEnum):
    """字符宽度枚举"""
    NARROW = 1    # 窄字符（ASCII 等）
    WIDE = 2      # 宽字符（CJK 等）
    AMBIGUOUS = 1  # 宽度不明确的字符，默认视为窄字符


# East Asian Width 属性
# W: Wide - 宽字符
# F: Fullwidth - 全角字符
# H: Halfwidth - 半角字符
# Na: Narrow - 窄字符
# A: Ambiguous - 宽度不明确
# N: Neutral - 中性（宽度为 1）

# 宽字符的 Unicode 范围（W 和 F 类型）
_WIDE_RANGES = [
    # CJK 统一表意文字
    (0x4E00, 0x9FFF),    # CJK Unified Ideographs
    (0x3400, 0x4DBF),    # CJK Unified Ideographs Extension A
    (0x20000, 0x2A6DF),  # CJK Unified Ideographs Extension B
    (0x2A700, 0x2B73F),  # CJK Unified Ideographs Extension C
    (0x2B740, 0x2B81F),  # CJK Unified Ideographs Extension D
    (0x2B820, 0x2CEAF),  # CJK Unified Ideographs Extension E
    (0x2CEB0, 0x2EBEF),  # CJK Unified Ideographs Extension F
    (0x30000, 0x3134F),  # CJK Unified Ideographs Extension G
    # CJK 兼容表意文字
    (0xF900, 0xFAFF),    # CJK Compatibility Ideographs
    (0x2F800, 0x2FA1F),  # CJK Compatibility Ideographs Supplement
    # 日文假名
    (0x3040, 0x309F),    # Hiragana
    (0x30A0, 0x30FF),    # Katakana
    (0x31F0, 0x31FF),    # Katakana Phonetic Extensions
    (0x1B000, 0x1B0FF),  # Kana Supplement
    (0x1B100, 0x1B12F),  # Kana Extended-A
    # 韩文字母
    (0xAC00, 0xD7AF),    # Hangul Syllables
    (0x1100, 0x11FF),    # Hangul Jamo
    (0x3130, 0x318F),    # Hangul Compatibility Jamo
    (0xA960, 0xA97F),    # Hangul Jamo Extended-A
    (0xD7B0, 0xD7FF),    # Hangul Jamo Extended-B
    # 全角字符
    (0xFF00, 0xFF60),    # Fullwidth ASCII Variants
    (0xFFE0, 0xFFE6),    # Fullwidth Symbol Variants
    # 其他宽字符
    (0x3000, 0x303E),    # CJK Symbols and Punctuation
    (0xFF01, 0xFF5E),    # Fullwidth ASCII variants
]

# Emoji 宽度映射（部分 Emoji 在终端中宽度为 2）
_EMOJI_WIDE_RANGES = [
    # Emoji 表情符号（基本范围，实际宽度因终端而异）
    (0x1F600, 0x1F64F),  # Emoticons
    (0x1F300, 0x1F5FF),  # Miscellaneous Symbols and Pictographs
    (0x1F680, 0x1F6FF),  # Transport and Map Symbols
    (0x1F900, 0x1F9FF),  # Supplemental Symbols and Pictographs
    (0x1FA00, 0x1FA6F),  # Chess Symbols
    (0x1FA70, 0x1FAFF),  # Symbols and Pictographs Extended-A
    (0x2600, 0x26FF),    # Miscellaneous Symbols
    (0x2700, 0x27BF),    # Dingbats
]

# 零宽度字符（控制字符、组合字符等）
_ZERO_WIDTH_RANGES = [
    (0x0000, 0x001F),    # 控制字符
    (0x007F, 0x009F),    # 控制字符
    (0x200B, 0x200F),    # 零宽字符和方向控制
    (0x202A, 0x202E),    # 双向文本控制
    (0x2060, 0x206F),    # 字符格式控制
    (0xFE00, 0xFE0F),    # Variation Selectors
    (0xE0100, 0xE01EF), # Variation Selectors Supplement
    (0xFEFF, 0xFEFF),    # BOM
    (0x200E, 0x200E),    # LRM
    (0x200F, 0x200F),    # RLM
    (0x061C, 0x061C),    # ALM
]

# 组合字符（零宽度，修饰前一个字符）
_COMBINING_RANGES = [
    (0x0300, 0x036F),    # Combining Diacritical Marks
    (0x0483, 0x0489),    # Combining Cyrillic Letters
    (0x0591, 0x05BD),    # Hebrew combining marks
    (0x05BF, 0x05BF),
    (0x05C1, 0x05C2),
    (0x05C4, 0x05C5),
    (0x05C7, 0x05C7),
    (0x0610, 0x061A),    # Arabic combining marks
    (0x064B, 0x065F),
    (0x0670, 0x0670),
    (0x06D6, 0x06DC),
    (0x06DF, 0x06E4),
    (0x06E7, 0x06E8),
    (0x06EA, 0x06ED),
    (0x0711, 0x0711),
    (0x0730, 0x074A),
    (0x07A6, 0x07B0),
    (0x07EB, 0x07F3),
    (0x0816, 0x0819),
    (0x081B, 0x0823),
    (0x0825, 0x0827),
    (0x0829, 0x082D),
    (0x0859, 0x085B),
    (0x08D4, 0x08E1),
    (0x08E3, 0x0903),
    (0x093A, 0x093C),
    (0x093E, 0x094F),
    (0x0951, 0x0957),
    (0x0962, 0x0963),
    (0x0981, 0x0983),
    (0x09BC, 0x09BC),
    (0x09BE, 0x09C4),
    (0x09C7, 0x09C8),
    (0x09CB, 0x09CD),
    (0x09D7, 0x09D7),
    (0x09E2, 0x09E3),
    (0x0A01, 0x0A03),
    (0x0A3C, 0x0A3C),
    (0x0A3E, 0x0A42),
    (0x0A47, 0x0A48),
    (0x0A4B, 0x0A4D),
    (0x0A51, 0x0A51),
    (0x0A70, 0x0A71),
    (0x0A75, 0x0A75),
    (0x0A81, 0x0A83),
    (0x0ABC, 0x0ABC),
    (0x0ABE, 0x0AC5),
    (0x0AC7, 0x0AC9),
    (0x0ACB, 0x0ACD),
    (0x0AE2, 0x0AE3),
    (0x0B01, 0x0B03),
    (0x0B3C, 0x0B3C),
    (0x0B3E, 0x0B44),
    (0x0B47, 0x0B48),
    (0x0B4B, 0x0B4D),
    (0x0B56, 0x0B57),
    (0x0B62, 0x0B63),
    (0x0B82, 0x0B82),
    (0x0BBE, 0x0BC2),
    (0x0BC6, 0x0BC8),
    (0x0BCA, 0x0BCD),
    (0x0BD7, 0x0BD7),
    (0x0C00, 0x0C03),
    (0x0C3E, 0x0C44),
    (0x0C46, 0x0C48),
    (0x0C4A, 0x0C4D),
    (0x0C55, 0x0C56),
    (0x0C62, 0x0C63),
    (0x0C81, 0x0C83),
    (0x0CBC, 0x0CBC),
    (0x0CBE, 0x0CC4),
    (0x0CC6, 0x0CC8),
    (0x0CCA, 0x0CCD),
    (0x0CD5, 0x0CD6),
    (0x0CE2, 0x0CE3),
    (0x0D01, 0x0D03),
    (0x0D3E, 0x0D44),
    (0x0D46, 0x0D48),
    (0x0D4A, 0x0D4D),
    (0x0D57, 0x0D57),
    (0x0D62, 0x0D63),
    (0x0D82, 0x0D83),
    (0x0DCA, 0x0DCA),
    (0x0DCF, 0x0DD4),
    (0x0DD6, 0x0DD6),
    (0x0DD8, 0x0DDF),
    (0x0DF2, 0x0DF3),
    (0x0E31, 0x0E31),
    (0x0E34, 0x0E3A),
    (0x0E47, 0x0E4E),
    (0x0EB1, 0x0EB1),
    (0x0EB4, 0x0EB9),
    (0x0EBB, 0x0EBC),
    (0x0EC8, 0x0ECD),
    (0x0F18, 0x0F19),
    (0x0F35, 0x0F35),
    (0x0F37, 0x0F37),
    (0x0F39, 0x0F39),
    (0x0F3E, 0x0F3F),
    (0x0F71, 0x0F84),
    (0x0F86, 0x0F87),
    (0x0F8D, 0x0F97),
    (0x0F99, 0x0FBC),
    (0x0FC6, 0x0FC6),
    (0x102B, 0x103E),
    (0x1056, 0x1059),
    (0x105E, 0x1060),
    (0x1062, 0x1064),
    (0x1067, 0x106D),
    (0x1071, 0x1074),
    (0x1082, 0x108D),
    (0x108F, 0x108F),
    (0x109A, 0x109D),
    (0x135D, 0x135F),
    (0x1712, 0x1714),
    (0x1732, 0x1734),
    (0x1752, 0x1753),
    (0x1772, 0x1773),
    (0x17B4, 0x17D3),
    (0x17DD, 0x17DD),
    (0x180B, 0x180D),
    (0x1885, 0x1886),
    (0x18A9, 0x18A9),
    (0x1920, 0x192B),
    (0x1930, 0x193B),
    (0x1A17, 0x1A1B),
    (0x1A55, 0x1A5E),
    (0x1A60, 0x1A7C),
    (0x1A7F, 0x1A7F),
    (0x1AB0, 0x1ABE),
    (0x1B00, 0x1B04),
    (0x1B34, 0x1B44),
    (0x1B6B, 0x1B73),
    (0x1B80, 0x1B82),
    (0x1BA1, 0x1BAD),
    (0x1BE6, 0x1BF3),
    (0x1C24, 0x1C37),
    (0x1CD0, 0x1CD2),
    (0x1CD4, 0x1CE8),
    (0x1CED, 0x1CED),
    (0x1CF2, 0x1CF4),
    (0x1CF8, 0x1CF9),
    (0x1DC0, 0x1DF9),
    (0x1DFB, 0x1DFF),
    (0x20D0, 0x20F0),
    (0x2CEF, 0x2CF1),
    (0x2D7F, 0x2D7F),
    (0x2DE0, 0x2DFF),
    (0x302A, 0x302F),
    (0x3099, 0x309A),
    (0xA66F, 0xA672),
    (0xA674, 0xA67D),
    (0xA69E, 0xA69F),
    (0xA6F0, 0xA6F1),
    (0xA802, 0xA802),
    (0xA806, 0xA806),
    (0xA80B, 0xA80B),
    (0xA823, 0xA827),
    (0xA880, 0xA881),
    (0xA8B4, 0xA8C5),
    (0xA8E0, 0xA8F1),
    (0xA926, 0xA92D),
    (0xA947, 0xA953),
    (0xA980, 0xA983),
    (0xA9B3, 0xA9C0),
    (0xA9E5, 0xA9E5),
    (0xAA29, 0xAA36),
    (0xAA43, 0xAA43),
    (0xAA4C, 0xAA4D),
    (0xAA7B, 0xAA7D),
    (0xAAB0, 0xAAB0),
    (0xAAB2, 0xAAB4),
    (0xAAB7, 0xAAB8),
    (0xAABE, 0xAABF),
    (0xAAC1, 0xAAC1),
    (0xAAEB, 0xAAF5),
    (0xABE3, 0xABEA),
    (0xABEC, 0xABED),
    (0xFB1E, 0xFB1E),
    (0xFE00, 0xFE0F),
    (0xFE20, 0xFE2F),
    (0x101FD, 0x101FD),
    (0x102E0, 0x102E0),
    (0x10376, 0x1037A),
    (0x10A01, 0x10A03),
    (0x10A05, 0x10A06),
    (0x10A0C, 0x10A0F),
    (0x10A38, 0x10A3A),
    (0x10A3F, 0x10A3F),
    (0x10AE5, 0x10AE6),
    (0x10D24, 0x10D27),
    (0x10EAB, 0x10EAC),
    (0x10F46, 0x10F50),
    (0x11000, 0x11002),
    (0x11038, 0x11046),
    (0x11070, 0x11070),
    (0x11073, 0x11074),
    (0x1107F, 0x11082),
    (0x110B0, 0x110BA),
    (0x110C2, 0x110C2),
    (0x11100, 0x11102),
    (0x11127, 0x11134),
    (0x11145, 0x11146),
    (0x11173, 0x11173),
    (0x11180, 0x11182),
    (0x111B3, 0x111C0),
    (0x111C9, 0x111CC),
    (0x111CE, 0x111CF),
    (0x1122C, 0x11237),
    (0x1123E, 0x1123E),
    (0x112DF, 0x112EA),
    (0x11300, 0x11303),
    (0x1133C, 0x1133C),
    (0x1133E, 0x11344),
    (0x11347, 0x11348),
    (0x1134B, 0x1134D),
    (0x11357, 0x11357),
    (0x11362, 0x11363),
    (0x11366, 0x1136C),
    (0x11370, 0x11374),
    (0x11435, 0x11446),
    (0x1145E, 0x1145E),
    (0x114B0, 0x114C3),
    (0x115AF, 0x115B5),
    (0x115B8, 0x115C0),
    (0x115DC, 0x115DD),
    (0x11630, 0x11640),
    (0x116AB, 0x116B7),
    (0x1171D, 0x1172B),
    (0x1182C, 0x1183A),
    (0x11930, 0x11935),
    (0x11937, 0x11938),
    (0x1193B, 0x1193E),
    (0x11940, 0x11940),
    (0x11942, 0x11943),
    (0x119D1, 0x119D7),
    (0x119DA, 0x119E0),
    (0x119E4, 0x119E4),
    (0x11A01, 0x11A0A),
    (0x11A33, 0x11A39),
    (0x11A3B, 0x11A3E),
    (0x11A47, 0x11A47),
    (0x11A51, 0x11A5B),
    (0x11A8A, 0x11A99),
    (0x11C2F, 0x11C36),
    (0x11C38, 0x11C3F),
    (0x11C92, 0x11CA7),
    (0x11CA9, 0x11CB6),
    (0x11D31, 0x11D36),
    (0x11D3A, 0x11D3A),
    (0x11D3C, 0x11D3D),
    (0x11D3F, 0x11D45),
    (0x11D47, 0x11D47),
    (0x11D8A, 0x11D8E),
    (0x11D90, 0x11D91),
    (0x11D93, 0x11D97),
    (0x11EF3, 0x11EF6),
    (0x16AF0, 0x16AF4),
    (0x16B30, 0x16B36),
    (0x16F4F, 0x16F4F),
    (0x16F51, 0x16F87),
    (0x16F8F, 0x16F92),
    (0x1BC9D, 0x1BC9E),
    (0x1D165, 0x1D169),
    (0x1D16D, 0x1D172),
    (0x1D17B, 0x1D182),
    (0x1D185, 0x1D18B),
    (0x1D1AA, 0x1D1AD),
    (0x1D242, 0x1D244),
    (0x1DA00, 0x1DA36),
    (0x1DA3B, 0x1DA6C),
    (0x1DA75, 0x1DA75),
    (0x1DA84, 0x1DA84),
    (0x1DA9B, 0x1DA9F),
    (0x1DAA1, 0x1DAAF),
    (0x1E000, 0x1E006),
    (0x1E008, 0x1E018),
    (0x1E01B, 0x1E021),
    (0x1E023, 0x1E024),
    (0x1E026, 0x1E02A),
    (0x1E130, 0x1E136),
    (0x1E2EC, 0x1E2EF),
    (0x1E8D0, 0x1E8D6),
    (0x1E944, 0x1E94A),
    (0xE0100, 0xE01EF),
]


def _is_in_ranges(code_point: int, ranges: List[Tuple[int, int]]) -> bool:
    """检查代码点是否在指定的范围内"""
    for start, end in ranges:
        if start <= code_point <= end:
            return True
    return False


def char_width(char: str, ambiguous_as_wide: bool = False, emoji_as_wide: bool = False) -> int:
    """
    计算单个字符的显示宽度。

    Args:
        char: 单个字符
        ambiguous_as_wide: 是否将宽度不明确的字符视为宽字符
        emoji_as_wide: 是否将 Emoji 视为宽字符

    Returns:
        字符的显示宽度（0、1 或 2）

    Examples:
        >>> char_width('A')
        1
        >>> char_width('中')
        2
        >>> char_width('\\n')
        0
        >>> char_width('\\u0301')  # 组合重音符号
        0
    """
    if len(char) == 0:
        return 0

    code_point = ord(char)

    # 零宽度字符
    if _is_in_ranges(code_point, _ZERO_WIDTH_RANGES):
        return 0

    # 组合字符（零宽度，修饰前一个字符）
    if _is_in_ranges(code_point, _COMBINING_RANGES):
        return 0

    # 宽字符（CJK 等）
    if _is_in_ranges(code_point, _WIDE_RANGES):
        return 2

    # Emoji
    if emoji_as_wide and _is_in_ranges(code_point, _EMOJI_WIDE_RANGES):
        return 2

    # 使用 unicodedata 检查 East Asian Width 属性
    try:
        eaw = unicodedata.east_asian_width(char)
        if eaw in ('W', 'F'):  # Wide, Fullwidth
            return 2
        elif eaw == 'A':  # Ambiguous
            return 2 if ambiguous_as_wide else 1
    except (ValueError, TypeError):
        pass

    return 1


def width(text: str, ambiguous_as_wide: bool = False, emoji_as_wide: bool = False) -> int:
    """
    计算字符串的显示宽度。

    Args:
        text: 输入字符串
        ambiguous_as_wide: 是否将宽度不明确的字符视为宽字符
        emoji_as_wide: 是否将 Emoji 视为宽字符

    Returns:
        字符串的显示宽度

    Examples:
        >>> width('Hello')
        5
        >>> width('你好')
        4
        >>> width('Hello, 世界!')
        11
        >>> width('café')  # e + 组合重音符号
        4
    """
    total_width = 0
    for char in text:
        total_width += char_width(char, ambiguous_as_wide, emoji_as_wide)
    return total_width


def is_wide(char: str) -> bool:
    """
    检查字符是否为宽字符。

    Args:
        char: 单个字符

    Returns:
        是否为宽字符

    Examples:
        >>> is_wide('A')
        False
        >>> is_wide('中')
        True
    """
    return char_width(char) == 2


def is_combining(char: str) -> bool:
    """
    检查字符是否为组合字符。

    Args:
        char: 单个字符

    Returns:
        是否为组合字符

    Examples:
        >>> is_combining('\\u0301')  # 组合重音符号
        True
        >>> is_combining('A')
        False
    """
    if len(char) == 0:
        return False
    code_point = ord(char)
    return _is_in_ranges(code_point, _COMBINING_RANGES)


def is_zero_width(char: str) -> bool:
    """
    检查字符是否为零宽度字符。

    Args:
        char: 单个字符

    Returns:
        是否为零宽度字符

    Examples:
        >>> is_zero_width('\\u200B')  # 零宽空格
        True
        >>> is_zero_width('A')
        False
    """
    if len(char) == 0:
        return True
    code_point = ord(char)
    return _is_in_ranges(code_point, _ZERO_WIDTH_RANGES) or _is_in_ranges(code_point, _COMBINING_RANGES)


def truncate(text: str, max_width: int, ellipsis: str = '...', 
             ambiguous_as_wide: bool = False, emoji_as_wide: bool = False) -> str:
    """
    将字符串截断到指定的显示宽度。

    Args:
        text: 输入字符串
        max_width: 最大显示宽度
        ellipsis: 截断时添加的省略号
        ambiguous_as_wide: 是否将宽度不明确的字符视为宽字符
        emoji_as_wide: 是否将 Emoji 视为宽字符

    Returns:
        截断后的字符串

    Examples:
        >>> truncate('Hello, 世界!', 8)
        'Hello...'
        >>> truncate('你好世界', 5)
        '你好...'
        >>> truncate('Hello World', 8, ellipsis='…')
        'Hello W…'
    """
    if max_width <= 0:
        return ''
    
    ellipsis_width = width(ellipsis, ambiguous_as_wide, emoji_as_wide)
    
    if width(text, ambiguous_as_wide, emoji_as_wide) <= max_width:
        return text
    
    target_width = max_width - ellipsis_width
    if target_width <= 0:
        return ellipsis[:max_width] if ellipsis_width > max_width else ellipsis
    
    result = []
    current_width = 0
    
    for char in text:
        char_w = char_width(char, ambiguous_as_wide, emoji_as_wide)
        if current_width + char_w > target_width:
            break
        result.append(char)
        current_width += char_w
    
    return ''.join(result) + ellipsis


def pad_left(text: str, target_width: int, fill_char: str = ' ',
             ambiguous_as_wide: bool = False, emoji_as_wide: bool = False) -> str:
    """
    在字符串左侧填充到指定的显示宽度。

    Args:
        text: 输入字符串
        target_width: 目标显示宽度
        fill_char: 填充字符（必须是窄字符）
        ambiguous_as_wide: 是否将宽度不明确的字符视为宽字符
        emoji_as_wide: 是否将 Emoji 视为宽字符

    Returns:
        填充后的字符串

    Examples:
        >>> pad_left('你好', 6)
        '  你好'
        >>> pad_left('Hello', 10)
        '     Hello'
    """
    if len(fill_char) != 1 or char_width(fill_char) != 1:
        raise ValueError("fill_char 必须是单个窄字符")
    
    current_width = width(text, ambiguous_as_wide, emoji_as_wide)
    padding = max(0, target_width - current_width)
    
    return fill_char * padding + text


def pad_right(text: str, target_width: int, fill_char: str = ' ',
              ambiguous_as_wide: bool = False, emoji_as_wide: bool = False) -> str:
    """
    在字符串右侧填充到指定的显示宽度。

    Args:
        text: 输入字符串
        target_width: 目标显示宽度
        fill_char: 填充字符（必须是窄字符）
        ambiguous_as_wide: 是否将宽度不明确的字符视为宽字符
        emoji_as_wide: 是否将 Emoji 视为宽字符

    Returns:
        填充后的字符串

    Examples:
        >>> pad_right('你好', 6)
        '你好  '
        >>> pad_right('Hello', 10)
        'Hello     '
    """
    if len(fill_char) != 1 or char_width(fill_char) != 1:
        raise ValueError("fill_char 必须是单个窄字符")
    
    current_width = width(text, ambiguous_as_wide, emoji_as_wide)
    padding = max(0, target_width - current_width)
    
    return text + fill_char * padding


def center(text: str, target_width: int, fill_char: str = ' ',
           ambiguous_as_wide: bool = False, emoji_as_wide: bool = False) -> str:
    """
    将字符串居中对齐到指定的显示宽度。

    Args:
        text: 输入字符串
        target_width: 目标显示宽度
        fill_char: 填充字符（必须是窄字符）
        ambiguous_as_wide: 是否将宽度不明确的字符视为宽字符
        emoji_as_wide: 是否将 Emoji 视为宽字符

    Returns:
        居中对齐后的字符串

    Examples:
        >>> center('你好', 8)
        '  你好  '
        >>> center('Hi', 6)
        '  Hi  '
    """
    if len(fill_char) != 1 or char_width(fill_char) != 1:
        raise ValueError("fill_char 必须是单个窄字符")
    
    current_width = width(text, ambiguous_as_wide, emoji_as_wide)
    total_padding = max(0, target_width - current_width)
    left_padding = total_padding // 2
    right_padding = total_padding - left_padding
    
    return fill_char * left_padding + text + fill_char * right_padding


def align_columns(rows: List[List[str]], separator: str = ' | ',
                  truncate_width: Optional[int] = None,
                  ambiguous_as_wide: bool = False, emoji_as_wide: bool = False) -> List[str]:
    """
    对齐多列文本，生成格式化的表格行。

    Args:
        rows: 行数据列表，每行是一个字符串列表
        separator: 列分隔符
        truncate_width: 每列的最大宽度（None 表示不截断）
        ambiguous_as_wide: 是否将宽度不明确的字符视为宽字符
        emoji_as_wide: 是否将 Emoji 视为宽字符

    Returns:
        格式化后的行列表

    Examples:
        >>> rows = [['Name', 'Age'], ['Alice', '25'], ['Bob', '30']]
        >>> align_columns(rows)
        ['Name  | Age', 'Alice | 25', 'Bob   | 30']
    """
    if not rows:
        return []
    
    num_cols = max(len(row) for row in rows)
    col_widths = [0] * num_cols
    
    # 计算每列的最大宽度
    for row in rows:
        for i, cell in enumerate(row):
            cell_width = width(str(cell), ambiguous_as_wide, emoji_as_wide)
            if truncate_width is not None:
                cell_width = min(cell_width, truncate_width)
            col_widths[i] = max(col_widths[i], cell_width)
    
    result = []
    for row in rows:
        padded_cells = []
        for i, cell in enumerate(row):
            cell_str = str(cell)
            if truncate_width is not None:
                cell_str = truncate(cell_str, truncate_width, 
                                   ambiguous_as_wide=ambiguous_as_wide, 
                                   emoji_as_wide=emoji_as_wide)
            padded_cells.append(pad_right(cell_str, col_widths[i], 
                                         ambiguous_as_wide=ambiguous_as_wide, 
                                         emoji_as_wide=emoji_as_wide))
        result.append(separator.join(padded_cells))
    
    return result


def strip_ansi(text: str) -> str:
    """
    移除字符串中的 ANSI 转义序列。

    Args:
        text: 输入字符串

    Returns:
        移除 ANSI 转义序列后的字符串

    Examples:
        >>> strip_ansi('\\x1b[31mHello\\x1b[0m')
        'Hello'
        >>> strip_ansi('\\x1b[1;32;40mColored\\x1b[0m')
        'Colored'
    """
    import re
    ansi_pattern = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]|\x1b\].*?\x07|\x1b[PX^_].*?\x1b\\')
    return ansi_pattern.sub('', text)


def width_with_ansi(text: str, ambiguous_as_wide: bool = False, emoji_as_wide: bool = False) -> int:
    """
    计算包含 ANSI 转义序列的字符串的显示宽度（忽略 ANSI 序列）。

    Args:
        text: 输入字符串（可能包含 ANSI 转义序列）
        ambiguous_as_wide: 是否将宽度不明确的字符视为宽字符
        emoji_as_wide: 是否将 Emoji 视为宽字符

    Returns:
        显示宽度

    Examples:
        >>> width_with_ansi('\\x1b[31mHello\\x1b[0m')
        5
        >>> width_with_ansi('\\x1b[1;32m你好\\x1b[0m')
        4
    """
    clean_text = strip_ansi(text)
    return width(clean_text, ambiguous_as_wide, emoji_as_wide)


def split_by_width(text: str, max_width: int, 
                   ambiguous_as_wide: bool = False, emoji_as_wide: bool = False) -> List[str]:
    """
    按显示宽度分割字符串。

    Args:
        text: 输入字符串
        max_width: 每段的最大宽度
        ambiguous_as_wide: 是否将宽度不明确的字符视为宽字符
        emoji_as_wide: 是否将 Emoji 视为宽字符

    Returns:
        分割后的字符串列表

    Examples:
        >>> split_by_width('Hello你好World', 5)
        ['Hello', '你好', 'Worl', 'd']
    """
    if max_width <= 0:
        return [text]
    
    segments = []
    current_segment = []
    current_width = 0
    
    for char in text:
        char_w = char_width(char, ambiguous_as_wide, emoji_as_wide)
        
        if current_width + char_w > max_width:
            if current_segment:
                segments.append(''.join(current_segment))
            current_segment = [char]
            current_width = char_w
        else:
            current_segment.append(char)
            current_width += char_w
    
    if current_segment:
        segments.append(''.join(current_segment))
    
    return segments


def wrap_text(text: str, width_limit: int, 
              ambiguous_as_wide: bool = False, emoji_as_wide: bool = False,
              break_long_words: bool = True) -> List[str]:
    """
    按指定宽度换行文本。

    Args:
        text: 输入字符串
        width_limit: 每行的最大宽度
        ambiguous_as_wide: 是否将宽度不明确的字符视为宽字符
        emoji_as_wide: 是否将 Emoji 视为宽字符
        break_long_words: 是否允许打断单词

    Returns:
        换行后的行列表

    Examples:
        >>> wrap_text('Hello, 世界! This is a test.', 10)
        ['Hello, ', '世界! ', 'This is ', 'a test.']
    """
    if width_limit <= 0:
        return [text]
    
    lines = []
    words = text.split(' ')
    current_line = []
    current_width = 0
    
    for word in words:
        word_width = width(word, ambiguous_as_wide, emoji_as_wide)
        
        # 空格宽度
        space_width = 1 if current_line else 0
        
        if current_width + space_width + word_width <= width_limit:
            current_line.append(word)
            current_width += space_width + word_width
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = []
                current_width = 0
            
            # 检查单词是否需要进一步分割
            if word_width > width_limit:
                if break_long_words:
                    # 按宽度分割单词
                    word_segments = split_by_width(word, width_limit, 
                                                   ambiguous_as_wide, emoji_as_wide)
                    lines.extend(word_segments[:-1] if len(word_segments) > 1 else word_segments)
                    if word_segments:
                        last_segment = word_segments[-1]
                        current_line = [last_segment]
                        current_width = width(last_segment, ambiguous_as_wide, emoji_as_wide)
                else:
                    lines.append(word)
            else:
                current_line = [word]
                current_width = word_width
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines


def chars_with_width(text: str, 
                     ambiguous_as_wide: bool = False, emoji_as_wide: bool = False) -> List[Tuple[str, int]]:
    """
    返回字符串中每个字符及其宽度的列表。

    Args:
        text: 输入字符串
        ambiguous_as_wide: 是否将宽度不明确的字符视为宽字符
        emoji_as_wide: 是否将 Emoji 视为宽字符

    Returns:
        (字符, 宽度) 元组列表

    Examples:
        >>> chars_with_width('你好A')
        [('你', 2), ('好', 2), ('A', 1)]
    """
    return [(char, char_width(char, ambiguous_as_wide, emoji_as_wide)) for char in text]


def visualize_width(text: str, 
                    narrow_char: str = '·', wide_char: str = '██', zero_char: str = '',
                    ambiguous_as_wide: bool = False, emoji_as_wide: bool = False) -> str:
    """
    可视化字符串的宽度分布。

    Args:
        text: 输入字符串
        narrow_char: 窄字符的可视化表示
        wide_char: 宽字符的可视化表示
        zero_char: 零宽度字符的可视化表示
        ambiguous_as_wide: 是否将宽度不明确的字符视为宽字符
        emoji_as_wide: 是否将 Emoji 视为宽字符

    Returns:
        可视化宽度字符串

    Examples:
        >>> visualize_width('你好A')
        '████████·'
    """
    result = []
    for char in text:
        w = char_width(char, ambiguous_as_wide, emoji_as_wide)
        if w == 0:
            result.append(zero_char)
        elif w == 1:
            result.append(narrow_char)
        else:
            result.append(wide_char)
    return ''.join(result)


# 便捷函数别名
swidth = width  # string width
cwidth = char_width  # character width


if __name__ == '__main__':
    # 演示用法
    print("=== Width Utils Demo ===\n")
    
    test_strings = [
        "Hello, World!",
        "你好，世界！",
        "Hello, 世界!",
        "café",  # with combining character
        "🎉🎊🎁",  # emoji
        "Hello\tWorld\n",
        "\x1b[31mColored\x1b[0m",  # ANSI color
    ]
    
    for s in test_strings:
        print(f"字符串: {repr(s)}")
        print(f"  显示宽度: {width(s)}")
        print(f"  字符详情: {chars_with_width(s)}")
        print(f"  宽度可视化: {visualize_width(s)}")
        print()
    
    # 截断演示
    print("=== 截断演示 ===")
    text = "Hello, 世界! This is a test."
    print(f"原文本: {text}")
    print(f"截断到 15: {truncate(text, 15)}")
    print(f"截断到 10 (ellipsis='…'): {truncate(text, 10, ellipsis='…')}")
    print()
    
    # 对齐演示
    print("=== 对齐演示 ===")
    print(f"左对齐: |{pad_left('你好', 10)}|")
    print(f"右对齐: |{pad_right('你好', 10)}|")
    print(f"居中:   |{center('你好', 10)}|")
    print()
    
    # 表格演示
    print("=== 表格对齐 ===")
    rows = [
        ['姓名', '年龄', '城市'],
        ['张三', '25', '北京'],
        ['Alice', '30', 'New York'],
        ['李四', '28', '上海'],
    ]
    for row in align_columns(rows):
        print(row)
    print()
    
    # 分割演示
    print("=== 按宽度分割 ===")
    text = "Hello你好World世界"
    print(f"原文本: {text}")
    print(f"按宽度 5 分割: {split_by_width(text, 5)}")
    print()
    
    # 换行演示
    print("=== 文本换行 ===")
    text = "Hello, 世界! This is a long text that needs to be wrapped."
    print(f"原文本: {text}")
    print(f"按宽度 15 换行:")
    for line in wrap_text(text, 15):
        print(f"  {line}")