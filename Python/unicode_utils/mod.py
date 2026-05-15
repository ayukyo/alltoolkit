"""
Unicode Utilities - Unicode 字符工具集

提供 Unicode 字符查询、转换、分类、验证等功能。
零外部依赖，仅使用 Python 标准库。

功能：
- Unicode 字符信息查询
- 字符分类（字母、数字、标点、符号等）
- 字符编码转换
- Unicode 范围检测
- 表情符号检测
- 零宽字符检测
- Unicode 规范化
- 字符脚本检测
"""

import unicodedata
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum


class UnicodeCategory(Enum):
    """Unicode 字符分类"""
    CONTROL = "Cc"           # 控制字符
    FORMAT = "Cf"            # 格式字符
    SURROGATE = "Cs"         # 代理字符
    PRIVATE_USE = "Co"       # 私用字符
    UNASSIGNED = "Cn"        # 未分配
    
    UPPERCASE_LETTER = "Lu"  # 大写字母
    LOWERCASE_LETTER = "Ll"  # 小写字母
    TITLECASE_LETTER = "Lt"  # 标题字母
    MODIFIER_LETTER = "Lm"   # 修饰字母
    OTHER_LETTER = "Lo"      # 其他字母
    
    NONSPACING_MARK = "Mn"   # 非间距标记
    SPACING_MARK = "Mc"      # 间距标记
    ENCLOSING_MARK = "Me"    # 封闭标记
    
    DECIMAL_NUMBER = "Nd"    # 十进制数字
    LETTER_NUMBER = "Nl"     # 字母数字
    OTHER_NUMBER = "No"      # 其他数字
    
    CONNECTOR_PUNCTUATION = "Pc"  # 连接标点
    DASH_PUNCTUATION = "Pd"       # 破折号
    OPEN_PUNCTUATION = "Ps"       # 开括号
    CLOSE_PUNCTUATION = "Pe"      # 闭括号
    INITIAL_PUNCTUATION = "Pi"    # 前引号
    FINAL_PUNCTUATION = "Pf"      # 后引号
    OTHER_PUNCTUATION = "Po"      # 其他标点
    
    MATH_SYMBOL = "Sm"       # 数学符号
    CURRENCY_SYMBOL = "Sc"   # 货币符号
    MODIFIER_SYMBOL = "Sk"   # 修饰符号
    OTHER_SYMBOL = "So"       # 其他符号
    
    LINE_SEPARATOR = "Zl"    # 行分隔符
    PARAGRAPH_SEPARATOR = "Zp"  # 段落分隔符
    SPACE_SEPARATOR = "Zs"   # 空格分隔符


class UnicodeScript(Enum):
    """Unicode 脚本（文字系统）"""
    LATIN = "Latin"
    CYRILLIC = "Cyrillic"
    GREEK = "Greek"
    ARABIC = "Arabic"
    HEBREW = "Hebrew"
    CHINESE = "Han"
    JAPANESE_HIRAGANA = "Hiragana"
    JAPANESE_KATAKANA = "Katakana"
    KOREAN_HANGUL = "Hangul"
    THAI = "Thai"
    DEVANAGARI = "Devanagari"
    BENGALI = "Bengali"
    TAMIL = "Tamil"
    TELUGU = "Telugu"
    KANNADA = "Kannada"
    MALAYALAM = "Malayalam"
    GUJARATI = "Gujarati"
    PUNJABI = "Gurmukhi"
    SINHALA = "Sinhala"
    TIBETAN = "Tibetan"
    MYANMAR = "Myanmar"
    GEORGIAN = "Georgian"
    ARMENIAN = "Armenian"
    ETHIOPIC = "Ethiopic"
    UNKNOWN = "Unknown"


@dataclass
class UnicodeCharInfo:
    """Unicode 字符信息"""
    char: str
    codepoint: int
    hex_code: str
    name: str
    category: str
    category_name: str
    script: str
    block: str
    is_letter: bool
    is_digit: bool
    is_punctuation: bool
    is_symbol: bool
    is_whitespace: bool
    is_control: bool
    is_emoji: bool
    is_zero_width: bool
    bidirectional: str
    combining_class: int
    numeric_value: Optional[float]
    mirrored: bool
    uppercase: Optional[str]
    lowercase: Optional[str]
    titlecase: Optional[str]
    decomposition: Optional[str]


# 常用 Unicode 范围定义
UNICODE_RANGES: Dict[str, Tuple[int, int]] = {
    # ASCII
    "ASCII": (0x0000, 0x007F),
    "Latin-1 Supplement": (0x0080, 0x00FF),
    "Latin Extended-A": (0x0100, 0x017F),
    "Latin Extended-B": (0x0180, 0x024F),
    
    # 欧洲字母
    "Greek": (0x0370, 0x03FF),
    "Cyrillic": (0x0400, 0x04FF),
    "Cyrillic Supplement": (0x0500, 0x052F),
    "Armenian": (0x0530, 0x058F),
    "Hebrew": (0x0590, 0x05FF),
    "Arabic": (0x0600, 0x06FF),
    "Arabic Supplement": (0x0750, 0x077F),
    
    # 南亚文字
    "Devanagari": (0x0900, 0x097F),
    "Bengali": (0x0980, 0x09FF),
    "Gurmukhi": (0x0A00, 0x0A7F),
    "Gujarati": (0x0A80, 0x0AFF),
    "Oriya": (0x0B00, 0x0B7F),
    "Tamil": (0x0B80, 0x0BFF),
    "Telugu": (0x0C00, 0x0C7F),
    "Kannada": (0x0C80, 0x0CFF),
    "Malayalam": (0x0D00, 0x0D7F),
    "Thai": (0x0E00, 0x0E7F),
    "Lao": (0x0E80, 0x0EFF),
    "Tibetan": (0x0F00, 0x0FFF),
    
    # CJK
    "Hiragana": (0x3040, 0x309F),
    "Katakana": (0x30A0, 0x30FF),
    "CJK Unified Ideographs": (0x4E00, 0x9FFF),
    "CJK Compatibility": (0x3300, 0x33FF),
    "Hangul Syllables": (0xAC00, 0xD7AF),
    
    # 符号
    "General Punctuation": (0x2000, 0x206F),
    "Currency Symbols": (0x20A0, 0x20CF),
    "Letterlike Symbols": (0x2100, 0x214F),
    "Number Forms": (0x2150, 0x218F),
    "Arrows": (0x2190, 0x21FF),
    "Mathematical Operators": (0x2200, 0x22FF),
    "Miscellaneous Symbols": (0x2600, 0x26FF),
    "Dingbats": (0x2700, 0x27BF),
    
    # 表情符号范围
    "Emoticons": (0x1F600, 0x1F64F),
    "Miscellaneous Symbols and Pictographs": (0x1F300, 0x1F5FF),
    "Transport and Map Symbols": (0x1F680, 0x1F6FF),
    "Supplemental Symbols and Pictographs": (0x1F900, 0x1F9FF),
    "Symbols and Pictographs Extended-A": (0x1FA00, 0x1FA6F),
    
    # 私用区
    "Private Use Area": (0xE000, 0xF8FF),
    "Supplementary Private Use Area-A": (0xF0000, 0xFFFFD),
    "Supplementary Private Use Area-B": (0x100000, 0x10FFFD),
}

# 零宽字符
ZERO_WIDTH_CHARS: Set[int] = {
    0x0000,  # Null
    0x200B,  # Zero Width Space
    0x200C,  # Zero Width Non-Joiner
    0x200D,  # Zero Width Joiner
    0x200E,  # Left-to-Right Mark
    0x200F,  # Right-to-Left Mark
    0x2060,  # Word Joiner
    0x2061,  # Function Application
    0x2062,  # Invisible Times
    0x2063,  # Invisible Separator
    0x2064,  # Invisible Plus
    0xFEFF,  # Zero Width No-Break Space (BOM)
    0x00AD,  # Soft Hyphen
}

# 表情符号范围（完整列表）
EMOJI_RANGES: List[Tuple[int, int]] = [
    (0x1F600, 0x1F64F),  # Emoticons
    (0x1F300, 0x1F5FF),  # Misc Symbols and Pictographs
    (0x1F680, 0x1F6FF),  # Transport and Map
    (0x1F900, 0x1F9FF),  # Supplemental Symbols and Pictographs
    (0x1FA00, 0x1FA6F),  # Chess Symbols
    (0x1FA70, 0x1FAFF),  # Symbols and Pictographs Extended-A
    (0x2600, 0x26FF),    # Misc symbols (部分是emoji)
    (0x2700, 0x27BF),    # Dingbats (部分是emoji)
    (0x1F1E0, 0x1F1FF),  # Regional Indicator Symbols (国旗)
    (0x2300, 0x23FF),    # Miscellaneous Technical (部分emoji)
    (0x2B50, 0x2B55),    # 星星等
    (0x1F004, 0x1F004),  # Mahjong
    (0x1F0CF, 0x1F0CF),  # Playing cards
]


def get_char_info(char: str) -> UnicodeCharInfo:
    """
    获取单个字符的完整 Unicode 信息
    
    Args:
        char: 单个字符
        
    Returns:
        UnicodeCharInfo 对象
    """
    if len(char) != 1:
        raise ValueError(f"Expected single character, got {len(char)} characters")
    
    codepoint = ord(char)
    category = unicodedata.category(char)
    
    # 获取脚本
    script = _detect_script(char)
    
    # 获取 Unicode 块
    block = _get_unicode_block(codepoint)
    
    # 获取名称
    try:
        name = unicodedata.name(char, "UNKNOWN")
    except ValueError:
        name = "UNKNOWN"
    
    # 获取大小写映射
    try:
        uppercase = char.upper() if char.upper() != char else None
    except:
        uppercase = None
    
    try:
        lowercase = char.lower() if char.lower() != char else None
    except:
        lowercase = None
    
    try:
        titlecase = char.title() if char.title() != char else None
    except:
        titlecase = None
    
    # 获取数值
    try:
        numeric_value = unicodedata.numeric(char, None)
    except:
        numeric_value = None
    
    # 获取分解
    try:
        decomp = unicodedata.decomposition(char)
        decomposition = decomp if decomp else None
    except:
        decomposition = None
    
    return UnicodeCharInfo(
        char=char,
        codepoint=codepoint,
        hex_code=f"U+{codepoint:04X}",
        name=name,
        category=category,
        category_name=_get_category_name(category),
        script=script,
        block=block,
        is_letter=category.startswith('L'),
        is_digit=category.startswith('N'),
        is_punctuation=category.startswith('P'),
        is_symbol=category.startswith('S'),
        is_whitespace=char.isspace(),
        is_control=category.startswith('C'),
        is_emoji=is_emoji(char),
        is_zero_width=is_zero_width(char),
        bidirectional=unicodedata.bidirectional(char),
        combining_class=unicodedata.combining(char),
        numeric_value=numeric_value,
        mirrored=bool(unicodedata.mirrored(char)),
        uppercase=uppercase,
        lowercase=lowercase,
        titlecase=titlecase,
        decomposition=decomposition,
    )


def _detect_script(char: str) -> str:
    """检测字符所属的脚本"""
    codepoint = ord(char)
    
    # CJK 汉字
    if 0x4E00 <= codepoint <= 0x9FFF or 0x3400 <= codepoint <= 0x4DBF:
        return "Han"
    
    # 日文平假名
    if 0x3040 <= codepoint <= 0x309F:
        return "Hiragana"
    
    # 日文片假名
    if 0x30A0 <= codepoint <= 0x30FF:
        return "Katakana"
    
    # 韩文
    if 0xAC00 <= codepoint <= 0xD7AF or 0x1100 <= codepoint <= 0x11FF:
        return "Hangul"
    
    # 希腊文
    if 0x0370 <= codepoint <= 0x03FF:
        return "Greek"
    
    # 西里尔文
    if 0x0400 <= codepoint <= 0x04FF:
        return "Cyrillic"
    
    # 阿拉伯文
    if 0x0600 <= codepoint <= 0x06FF:
        return "Arabic"
    
    # 希伯来文
    if 0x0590 <= codepoint <= 0x05FF:
        return "Hebrew"
    
    # 泰文
    if 0x0E00 <= codepoint <= 0x0E7F:
        return "Thai"
    
    # 藏文
    if 0x0F00 <= codepoint <= 0x0FFF:
        return "Tibetan"
    
    # 梵文
    if 0x0900 <= codepoint <= 0x097F:
        return "Devanagari"
    
    # 孟加拉文
    if 0x0980 <= codepoint <= 0x09FF:
        return "Bengali"
    
    # 亚美尼亚文
    if 0x0530 <= codepoint <= 0x058F:
        return "Armenian"
    
    # 格鲁吉亚文
    if 0x10A0 <= codepoint <= 0x10FF:
        return "Georgian"
    
    # 拉丁字母
    if (0x0041 <= codepoint <= 0x007A or 
        0x00C0 <= codepoint <= 0x00FF or
        0x0100 <= codepoint <= 0x017F or
        0x0180 <= codepoint <= 0x024F):
        return "Latin"
    
    return "Unknown"


def _get_unicode_block(codepoint: int) -> str:
    """获取 Unicode 块名称"""
    for name, (start, end) in UNICODE_RANGES.items():
        if start <= codepoint <= end:
            return name
    return "Unknown Block"


def _get_category_name(category: str) -> str:
    """获取分类的可读名称"""
    category_names = {
        "Cc": "Control Character",
        "Cf": "Format Character",
        "Cs": "Surrogate",
        "Co": "Private Use",
        "Cn": "Unassigned",
        "Lu": "Uppercase Letter",
        "Ll": "Lowercase Letter",
        "Lt": "Titlecase Letter",
        "Lm": "Modifier Letter",
        "Lo": "Other Letter",
        "Mn": "Nonspacing Mark",
        "Mc": "Spacing Mark",
        "Me": "Enclosing Mark",
        "Nd": "Decimal Number",
        "Nl": "Letter Number",
        "No": "Other Number",
        "Pc": "Connector Punctuation",
        "Pd": "Dash Punctuation",
        "Ps": "Open Punctuation",
        "Pe": "Close Punctuation",
        "Pi": "Initial Punctuation",
        "Pf": "Final Punctuation",
        "Po": "Other Punctuation",
        "Sm": "Math Symbol",
        "Sc": "Currency Symbol",
        "Sk": "Modifier Symbol",
        "So": "Other Symbol",
        "Zl": "Line Separator",
        "Zp": "Paragraph Separator",
        "Zs": "Space Separator",
    }
    return category_names.get(category, f"Unknown ({category})")


def is_emoji(char: str) -> bool:
    """
    判断字符是否为表情符号
    
    Args:
        char: 单个字符
        
    Returns:
        是否为表情符号
    """
    codepoint = ord(char)
    
    for start, end in EMOJI_RANGES:
        if start <= codepoint <= end:
            return True
    
    return False


def is_zero_width(char: str) -> bool:
    """
    判断字符是否为零宽字符
    
    Args:
        char: 单个字符
        
    Returns:
        是否为零宽字符
    """
    return ord(char) in ZERO_WIDTH_CHARS


def contains_emoji(text: str) -> bool:
    """
    判断字符串是否包含表情符号
    
    Args:
        text: 输入字符串
        
    Returns:
        是否包含表情符号
    """
    for char in text:
        if is_emoji(char):
            return True
    return False


def contains_zero_width(text: str) -> bool:
    """
    判断字符串是否包含零宽字符
    
    Args:
        text: 输入字符串
        
    Returns:
        是否包含零宽字符
    """
    for char in text:
        if is_zero_width(char):
            return True
    return False


def remove_zero_width(text: str) -> str:
    """
    移除字符串中的零宽字符
    
    Args:
        text: 输入字符串
        
    Returns:
        移除零宽字符后的字符串
    """
    return ''.join(char for char in text if not is_zero_width(char))


def get_all_emojis(text: str) -> List[str]:
    """
    获取字符串中的所有表情符号
    
    Args:
        text: 输入字符串
        
    Returns:
        表情符号列表
    """
    emojis = []
    i = 0
    while i < len(text):
        char = text[i]
        
        # 处理组合表情（如带肤色修饰符的表情）
        if i + 1 < len(text) and text[i + 1] == '\u200D':
            # Zero Width Joiner - 组合表情
            combined = char
            j = i + 1
            while j < len(text):
                combined += text[j]
                j += 1
                if j >= len(text) or text[j] != '\u200D':
                    break
                if j + 1 < len(text):
                    combined += text[j + 1]
                    j += 1
            if is_emoji(char):
                emojis.append(combined)
            i = j
            continue
        
        if is_emoji(char):
            emojis.append(char)
        i += 1
    
    return emojis


def normalize_text(text: str, form: str = 'NFC') -> str:
    """
    Unicode 规范化
    
    Args:
        text: 输入文本
        form: 规范化形式 ('NFC', 'NFD', 'NFKC', 'NFKD')
        
    Returns:
        规范化后的文本
    """
    return unicodedata.normalize(form, text)


def get_string_stats(text: str) -> Dict:
    """
    获取字符串的 Unicode 统计信息
    
    Args:
        text: 输入字符串
        
    Returns:
        统计信息字典
    """
    stats = {
        "length": len(text),
        "codepoints": len(text),
        "byte_length_utf8": len(text.encode('utf-8')),
        "byte_length_utf16": len(text.encode('utf-16')),
        "byte_length_utf32": len(text.encode('utf-32')),
        "letters": 0,
        "digits": 0,
        "punctuation": 0,
        "symbols": 0,
        "whitespace": 0,
        "control": 0,
        "emoji_count": 0,
        "zero_width_count": 0,
        "scripts": {},
        "categories": {},
        "unique_chars": len(set(text)),
    }
    
    for char in text:
        category = unicodedata.category(char)
        
        # 分类统计
        if category.startswith('L'):
            stats["letters"] += 1
        elif category.startswith('N'):
            stats["digits"] += 1
        elif category.startswith('P'):
            stats["punctuation"] += 1
        elif category.startswith('S'):
            stats["symbols"] += 1
        elif category.startswith('Z'):
            stats["whitespace"] += 1
        elif category.startswith('C'):
            stats["control"] += 1
        
        # 脚本统计
        script = _detect_script(char)
        stats["scripts"][script] = stats["scripts"].get(script, 0) + 1
        
        # 分类统计
        stats["categories"][category] = stats["categories"].get(category, 0) + 1
        
        # 特殊字符统计
        if is_emoji(char):
            stats["emoji_count"] += 1
        if is_zero_width(char):
            stats["zero_width_count"] += 1
    
    return stats


def codepoint_to_char(codepoint: int) -> str:
    """
    将 Unicode 码点转换为字符
    
    Args:
        codepoint: Unicode 码点（整数或十六进制字符串）
        
    Returns:
        对应的字符
    """
    return chr(codepoint)


def char_to_codepoint(char: str) -> int:
    """
    将字符转换为 Unicode 码点
    
    Args:
        char: 单个字符
        
    Returns:
        Unicode 码点
    """
    if len(char) != 1:
        raise ValueError(f"Expected single character, got {len(char)} characters")
    return ord(char)


def string_to_codepoints(text: str) -> List[int]:
    """
    将字符串转换为码点列表
    
    Args:
        text: 输入字符串
        
    Returns:
        码点列表
    """
    return [ord(char) for char in text]


def codepoints_to_string(codepoints: List[int]) -> str:
    """
    将码点列表转换为字符串
    
    Args:
        codepoints: 码点列表
        
    Returns:
        对应的字符串
    """
    return ''.join(chr(cp) for cp in codepoints)


def hex_to_char(hex_str: str) -> str:
    """
    将十六进制字符串转换为字符
    
    Args:
        hex_str: 十六进制字符串（如 "1F600" 或 "U+1F600"）
        
    Returns:
        对应的字符
    """
    # 移除前缀
    hex_str = hex_str.upper().replace('U+', '').replace('0X', '')
    return chr(int(hex_str, 16))


def char_to_hex(char: str, prefix: bool = True) -> str:
    """
    将字符转换为十六进制表示
    
    Args:
        char: 单个字符
        prefix: 是否添加 U+ 前缀
        
    Returns:
        十六进制字符串
    """
    if len(char) != 1:
        raise ValueError(f"Expected single character, got {len(char)} characters")
    codepoint = ord(char)
    hex_str = f"{codepoint:04X}" if codepoint < 0x10000 else f"{codepoint:05X}"
    return f"U+{hex_str}" if prefix else hex_str


def is_valid_unicode(codepoint: int) -> bool:
    """
    判断码点是否为有效的 Unicode 码点
    
    Args:
        codepoint: Unicode 码点
        
    Returns:
        是否有效
    """
    # Unicode 范围: U+0000 到 U+10FFFF
    # 但排除代理区 (U+D800-U+DFFF)
    if codepoint < 0 or codepoint > 0x10FFFF:
        return False
    if 0xD800 <= codepoint <= 0xDFFF:
        return False
    return True


def get_chars_in_range(start: int, end: int, skip_invalid: bool = True) -> List[str]:
    """
    获取指定 Unicode 范围内的所有字符
    
    Args:
        start: 起始码点
        end: 结束码点
        skip_invalid: 是否跳过无效字符
        
    Returns:
        字符列表
    """
    chars = []
    for codepoint in range(start, end + 1):
        if skip_invalid and not is_valid_unicode(codepoint):
            continue
        try:
            chars.append(chr(codepoint))
        except ValueError:
            continue
    return chars


def get_chars_by_category(category: str) -> List[str]:
    """
    获取指定分类的所有字符（常见范围）
    
    Args:
        category: Unicode 分类（如 'Lu' 大写字母）
        
    Returns:
        字符列表
    """
    # 只返回基本多语言平面内的字符
    chars = []
    for codepoint in range(0x0000, 0xFFFF):
        try:
            char = chr(codepoint)
            if unicodedata.category(char) == category:
                chars.append(char)
        except:
            continue
    return chars


def get_name(char: str) -> str:
    """
    获取 Unicode 字符名称
    
    Args:
        char: 单个字符
        
    Returns:
        字符名称
    """
    try:
        return unicodedata.name(char, "UNKNOWN")
    except ValueError:
        return "UNKNOWN"


def get_chars_by_name(keyword: str, case_sensitive: bool = False) -> List[Tuple[str, str]]:
    """
    按名称关键词搜索 Unicode 字符
    
    Args:
        keyword: 搜索关键词
        case_sensitive: 是否区分大小写
        
    Returns:
        (字符, 名称) 列表
    """
    results = []
    
    if not case_sensitive:
        keyword = keyword.upper()
    
    # 搜索基本多语言平面
    for codepoint in range(0x0000, 0xFFFF):
        try:
            char = chr(codepoint)
            name = unicodedata.name(char, "")
            
            if not name:
                continue
            
            search_name = name if case_sensitive else name.upper()
            
            if keyword in search_name:
                results.append((char, name))
        except:
            continue
    
    return results


def detect_encoding(text: str) -> Dict[str, int]:
    """
    检测字符串中字符编码分布
    
    Args:
        text: 输入字符串
        
    Returns:
        编码分布字典
    """
    encoding_dist = {
        "ASCII": 0,
        "Latin-1": 0,
        "Latin-Extended": 0,
        "Greek": 0,
        "Cyrillic": 0,
        "CJK": 0,
        "Hangul": 0,
        "Hiragana": 0,
        "Katakana": 0,
        "Arabic": 0,
        "Hebrew": 0,
        "Thai": 0,
        "Emoji": 0,
        "Other": 0,
    }
    
    for char in text:
        cp = ord(char)
        
        if cp <= 0x7F:
            encoding_dist["ASCII"] += 1
        elif cp <= 0xFF:
            encoding_dist["Latin-1"] += 1
        elif 0x0100 <= cp <= 0x024F:
            encoding_dist["Latin-Extended"] += 1
        elif 0x0370 <= cp <= 0x03FF:
            encoding_dist["Greek"] += 1
        elif 0x0400 <= cp <= 0x04FF:
            encoding_dist["Cyrillic"] += 1
        elif 0x4E00 <= cp <= 0x9FFF:
            encoding_dist["CJK"] += 1
        elif 0xAC00 <= cp <= 0xD7AF:
            encoding_dist["Hangul"] += 1
        elif 0x3040 <= cp <= 0x309F:
            encoding_dist["Hiragana"] += 1
        elif 0x30A0 <= cp <= 0x30FF:
            encoding_dist["Katakana"] += 1
        elif 0x0600 <= cp <= 0x06FF:
            encoding_dist["Arabic"] += 1
        elif 0x0590 <= cp <= 0x05FF:
            encoding_dist["Hebrew"] += 1
        elif 0x0E00 <= cp <= 0x0E7F:
            encoding_dist["Thai"] += 1
        elif is_emoji(char):
            encoding_dist["Emoji"] += 1
        else:
            encoding_dist["Other"] += 1
    
    return encoding_dist


def strip_invisible(text: str) -> str:
    """
    移除不可见字符
    
    Args:
        text: 输入字符串
        
    Returns:
        移除不可见字符后的字符串
    """
    result = []
    for char in text:
        category = unicodedata.category(char)
        # 移除控制字符、格式字符（但保留空格）
        if category in ('Cc', 'Cf') and char not in (' ', '\t', '\n', '\r'):
            continue
        result.append(char)
    return ''.join(result)


def is_printable(char: str) -> bool:
    """
    判断字符是否可打印
    
    Args:
        char: 单个字符
        
    Returns:
        是否可打印
    """
    if len(char) != 1:
        raise ValueError(f"Expected single character, got {len(char)} characters")
    category = unicodedata.category(char)
    return category not in ('Cc', 'Cf', 'Cs', 'Co', 'Cn')


def get_bidirectional_type(char: str) -> str:
    """
    获取字符的双向类型
    
    Args:
        char: 单个字符
        
    Returns:
        双向类型代码
    """
    return unicodedata.bidirectional(char)


def is_rtl(text: str) -> bool:
    """
    判断字符串是否包含从右到左文字
    
    Args:
        text: 输入字符串
        
    Returns:
        是否包含RTL文字
    """
    rtl_types = {'R', 'AL', 'AN'}
    for char in text:
        if unicodedata.bidirectional(char) in rtl_types:
            return True
    return False


def get_combining_class(char: str) -> int:
    """
    获取字符的组合类
    
    Args:
        char: 单个字符
        
    Returns:
        组合类值
    """
    return unicodedata.combining(char)


def is_combining(char: str) -> bool:
    """
    判断字符是否为组合字符（变音符号等）
    
    Args:
        char: 单个字符
        
    Returns:
        是否为组合字符
    """
    return unicodedata.combining(char) > 0


def strip_diacritics(text: str) -> str:
    """
    移除字符串中的变音符号
    
    Args:
        text: 输入字符串
        
    Returns:
        移除变音符号后的字符串
    """
    # 使用 NFD 分解，然后过滤组合字符
    normalized = unicodedata.normalize('NFD', text)
    return ''.join(char for char in normalized if unicodedata.combining(char) == 0)


def get_unicode_version(char: str) -> Optional[str]:
    """
    估算字符引入的 Unicode 版本（基于码点范围）
    
    Args:
        char: 单个字符
        
    Returns:
        Unicode 版本字符串
    """
    cp = ord(char)
    
    # 简化版本检测，基于主要码点范围
    if cp <= 0x007F:
        return "1.0"
    elif cp <= 0x00FF:
        return "1.0"
    elif cp <= 0x017F:
        return "1.0"
    elif cp <= 0x03FF:
        return "1.0"
    elif cp <= 0x04FF:
        return "1.0"
    elif cp <= 0x05FF:
        return "1.0"
    elif cp <= 0x06FF:
        return "1.0"
    elif cp <= 0x0FFF:
        return "1.1"
    elif cp <= 0x1FFF:
        return "2.0"
    elif cp <= 0x2FFF:
        return "2.0"
    elif cp <= 0x3FFF:
        return "3.0"
    elif cp <= 0x4FFF:
        return "3.0"
    elif cp <= 0x9FFF:
        return "1.0"
    elif cp <= 0xD7FF:
        return "1.0"
    elif cp <= 0xF8FF:
        return "1.0"
    elif cp <= 0xFFFF:
        return "2.0"
    elif cp <= 0x1FFFF:
        return "3.1"
    elif cp <= 0x2FFFF:
        return "3.1"
    elif cp <= 0x3FFFF:
        return "3.2"
    elif cp <= 0x4FFFF:
        return "4.0"
    elif cp <= 0x5FFFF:
        return "4.1"
    elif cp <= 0x6FFFF:
        return "5.0"
    elif cp <= 0x7FFFF:
        return "5.1"
    elif cp <= 0x8FFFF:
        return "5.2"
    elif cp <= 0x9FFFF:
        return "6.0"
    elif cp <= 0xAFFFF:
        return "6.1"
    elif cp <= 0xBFFFF:
        return "7.0"
    elif cp <= 0xCFFFF:
        return "8.0"
    elif cp <= 0xDFFFF:
        return "9.0"
    elif cp <= 0xEFFFF:
        return "10.0"
    elif cp <= 0xFFFFF:
        return "11.0"
    else:
        return "12.0+"


# 便捷函数别名
def info(char: str) -> UnicodeCharInfo:
    """get_char_info 的简写"""
    return get_char_info(char)


def search(keyword: str) -> List[Tuple[str, str]]:
    """get_chars_by_name 的简写"""
    return get_chars_by_name(keyword)


def stats(text: str) -> Dict:
    """get_string_stats 的简写"""
    return get_string_stats(text)