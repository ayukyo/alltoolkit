"""
Emoji Utils - Emoji 工具集
零外部依赖的 Emoji 处理工具

功能：
- 解析文本中的 emoji
- 移除/替换 emoji
- 获取 emoji 的 Unicode 信息
- 生成随机 emoji
- 统计 emoji 使用频率
- 分类 emoji（表情、动物、食物等）

作者：AllToolkit 自动生成
日期：2026-05-27
"""

import re
import random
from typing import List, Dict, Tuple, Optional, Set
from collections import Counter
from unicodedata import name, category


# Emoji Unicode 范围（常用范围）
EMOJI_RANGES = [
    (0x1F600, 0x1F64F),  # Emoticons
    (0x1F300, 0x1F5FF),  # Misc Symbols and Pictographs
    (0x1F680, 0x1F6FF),  # Transport and Map
    (0x1F1E0, 0x1F1FF),  # Flags (regional indicator symbols)
    (0x2600, 0x26FF),    # Misc symbols
    (0x2700, 0x27BF),    # Dingbats
    (0xFE00, 0xFE0F),    # Variation Selectors
    (0x1F900, 0x1F9FF),  # Supplemental Symbols and Pictographs
    (0x1FA00, 0x1FA6F),  # Chess Symbols
    (0x1FA70, 0x1FAFF),  # Symbols and Pictographs Extended-A
    (0x231A, 0x231B),    # Watch, Hourglass
    (0x23E9, 0x23F3),    # Various
    (0x23F8, 0x23FA),    # Various
    (0x25AA, 0x25AB),    # Squares
    (0x25B6, 0x25B6),    # Play button
    (0x25C0, 0x25C0),    # Reverse button
    (0x25FB, 0x25FE),    # Squares
    (0x2614, 0x2615),    # Umbrella, Hot Beverage
    (0x2648, 0x2653),    # Zodiac
    (0x267F, 0x267F),    # Wheelchair
    (0x2693, 0x2693),    # Anchor
    (0x26A1, 0x26A1),    # High Voltage
    (0x26AA, 0x26AB),    # Circles
    (0x26BD, 0x26BE),    # Sports
    (0x26C4, 0x26C5),    # Snowman, Sun
    (0x26CE, 0x26CE),    # Ophiuchus
    (0x26D4, 0x26D4),    # No entry
    (0x26EA, 0x26EA),    # Church
    (0x26F2, 0x26F3),    # Fountain, Golf
    (0x26F5, 0x26F5),    # Sailboat
    (0x26FA, 0x26FA),    # Tent
    (0x26FD, 0x26FD),    # Fuel pump
    (0x2702, 0x2702),    # Scissors
    (0x2705, 0x2705),    # Check mark
    (0x2708, 0x270D),    # Various
    (0x270F, 0x270F),    # Pencil
    (0x2712, 0x2712),    # Black nib
    (0x2714, 0x2714),    # Check mark
    (0x2716, 0x2716),    # X mark
    (0x271D, 0x271D),    # Cross
    (0x2721, 0x2721),    # Star of David
    (0x2728, 0x2728),    # Sparkles
    (0x2733, 0x2734),    # Eight-pointed star
    (0x2744, 0x2744),    # Snowflake
    (0x2747, 0x2747),    # Sparkle
    (0x274C, 0x274C),    # Cross mark
    (0x274E, 0x274E),    # Cross mark
    (0x2753, 0x2755),    # Question marks
    (0x2757, 0x2757),    # Exclamation mark
    (0x2763, 0x2764),    # Heart exclamation, Heart
    (0x2795, 0x2797),    # Math symbols
    (0x27A1, 0x27A1),    # Right arrow
    (0x27B0, 0x27B0),    # Curly loop
    (0x27BF, 0x27BF),    # Double curly loop
    (0x2934, 0x2935),    # Arrows
    (0x2B05, 0x2B07),    # Arrows
    (0x2B1B, 0x2B1C),    # Squares
    (0x2B50, 0x2B50),    # Star
    (0x2B55, 0x2B55),    # Circle
    (0x3030, 0x3030),    # Wavy dash
    (0x303D, 0x303D),    # Part alternation mark
    (0x3297, 0x3297),    # Circled ideograph congratulation
    (0x3299, 0x3299),    # Circled ideograph secret
    (0x200D, 0x200D),    # Zero Width Joiner (for compound emojis)
    (0x20E3, 0x20E3),    # Combining Enclosing Keycap
]

# Emoji 分类
EMOJI_CATEGORIES = {
    'smileys': {
        'name': '表情符号',
        'ranges': [(0x1F600, 0x1F64F)],
    },
    'animals': {
        'name': '动物与自然',
        'ranges': [(0x1F400, 0x1F4FF)],
    },
    'food': {
        'name': '食物与饮料',
        'ranges': [(0x1F300, 0x1F3FF)],
    },
    'activities': {
        'name': '活动与运动',
        'ranges': [(0x26BD, 0x26BE), (0x26F3, 0x26F3), (0x1F380, 0x1F39F)],
    },
    'objects': {
        'name': '物品',
        'ranges': [(0x1F4A0, 0x1F4FF)],
    },
    'symbols': {
        'name': '符号',
        'ranges': [(0x2600, 0x26FF), (0x2700, 0x27BF)],
    },
    'flags': {
        'name': '旗帜',
        'ranges': [(0x1F1E0, 0x1F1FF)],
    },
    'travel': {
        'name': '旅行与地点',
        'ranges': [(0x1F680, 0x1F6FF)],
    },
}


def is_emoji(char: str) -> bool:
    """
    判断字符是否为 Emoji
    
    Args:
        char: 单个字符
        
    Returns:
        bool: 是否为 Emoji
        
    Example:
        >>> is_emoji('😀')
        True
        >>> is_emoji('A')
        False
    """
    if len(char) == 0:
        return False
    
    code_point = ord(char[0])
    
    # 检查是否在已知 Emoji 范围内
    for start, end in EMOJI_RANGES:
        if start <= code_point <= end:
            return True
    
    # 检查是否是组合 Emoji（如 🏳️‍🌈）
    if len(char) > 1:
        for c in char:
            if ord(c) in range(0x1F1E0, 0x1F1FF + 1):  # 区域指示符
                return True
            if 0x200D <= ord(c) <= 0x200D:  # 零宽连接符
                return True
    
    return False


def extract_emojis(text: str) -> List[str]:
    """
    从文本中提取所有 Emoji
    
    Args:
        text: 输入文本
        
    Returns:
        List[str]: Emoji 列表
        
    Example:
        >>> extract_emojis('Hello 😀 World 🎉')
        ['😀', '🎉']
    """
    emojis = []
    i = 0
    
    while i < len(text):
        char = text[i]
        
        # 检查是否是代理对（4字节 UTF-16）
        if 0xD800 <= ord(char) <= 0xDBFF and i + 1 < len(text):
            low = text[i + 1]
            if 0xDC00 <= ord(low) <= 0xDFFF:
                # 组合代理对
                code_point = ((ord(char) - 0xD800) << 10) + (ord(low) - 0xDC00) + 0x10000
                
                # 检查是否在 Emoji 范围
                for start, end in EMOJI_RANGES:
                    if start <= code_point <= end:
                        emojis.append(char + low)
                        i += 2
                        break
                else:
                    i += 2
                continue
        
        # 检查单个字符
        if is_emoji(char):
            # 检查是否是组合 Emoji
            j = i + 1
            while j < len(text):
                next_char = text[j]
                # 零宽连接符或变体选择器
                if ord(next_char) in [0x200D, 0xFE0F, 0x20E3]:
                    j += 1
                elif 0x1F3FB <= ord(next_char) <= 0x1F3FF:  # 肤色修饰符
                    j += 1
                elif 0x1F1E0 <= ord(next_char) <= 0x1F1FF:  # 区域指示符（旗帜）
                    j += 1
                else:
                    break
            
            if j > i + 1:
                emojis.append(text[i:j])
                i = j
            else:
                emojis.append(char)
                i += 1
        else:
            i += 1
    
    return emojis


def remove_emojis(text: str, replacement: str = '') -> str:
    """
    移除文本中的 Emoji
    
    Args:
        text: 输入文本
        replacement: 替换字符串，默认为空字符串
        
    Returns:
        str: 移除 Emoji 后的文本
        
    Example:
        >>> remove_emojis('Hello 😀 World 🎉')
        'Hello  World '
        >>> remove_emojis('Hello 😀 World 🎉', '[emoji]')
        'Hello [emoji] World [emoji]'
    """
    emojis = extract_emojis(text)
    result = text
    
    for emoji in emojis:
        result = result.replace(emoji, replacement)
    
    return result


def count_emojis(text: str) -> int:
    """
    统计文本中 Emoji 的数量
    
    Args:
        text: 输入文本
        
    Returns:
        int: Emoji 数量
        
    Example:
        >>> count_emojis('Hello 😀 World 🎉 Test 🌟')
        3
    """
    return len(extract_emojis(text))


def get_emoji_stats(text: str) -> Dict[str, int]:
    """
    统计文本中各 Emoji 的使用频率
    
    Args:
        text: 输入文本
        
    Returns:
        Dict[str, int]: Emoji 使用频率字典
        
    Example:
        >>> get_emoji_stats('😀 👍 😀 👍 🎉')
        {'😀': 2, '👍': 2, '🎉': 1}
    """
    emojis = extract_emojis(text)
    return dict(Counter(emojis))


def get_emoji_info(emoji: str) -> Dict:
    """
    获取 Emoji 的详细信息
    
    Args:
        emoji: Emoji 字符
        
    Returns:
        Dict: Emoji 信息字典，包含：
            - char: Emoji 字符
            - code_point: Unicode 码点
            - hex: 十六进制表示
            - name: Unicode 名称
            - category: Unicode 类别
            - emoji_category: Emoji 分类
            
    Example:
        >>> info = get_emoji_info('😀')
        >>> info['name']
        'GRINNING FACE'
    """
    if not is_emoji(emoji):
        return {
            'char': emoji,
            'code_point': None,
            'hex': None,
            'name': None,
            'category': None,
            'emoji_category': None,
            'is_emoji': False,
        }
    
    # 获取第一个字符的码点
    if len(emoji) >= 1:
        if 0xD800 <= ord(emoji[0]) <= 0xDBFF and len(emoji) >= 2:
            # 代理对
            high = ord(emoji[0])
            low = ord(emoji[1])
            code_point = ((high - 0xD800) << 10) + (low - 0xDC00) + 0x10000
        else:
            code_point = ord(emoji[0])
    else:
        code_point = 0
    
    try:
        unicode_name = name(emoji[0], 'Unknown')
    except ValueError:
        unicode_name = 'Unknown'
    
    try:
        unicode_category = category(emoji[0])
    except ValueError:
        unicode_category = 'Unknown'
    
    # 确定 Emoji 分类
    emoji_category = 'other'
    for cat_name, cat_info in EMOJI_CATEGORIES.items():
        for start, end in cat_info['ranges']:
            if start <= code_point <= end:
                emoji_category = cat_name
                break
        if emoji_category != 'other':
            break
    
    return {
        'char': emoji,
        'code_point': code_point,
        'hex': f'U+{code_point:04X}',
        'name': unicode_name,
        'category': unicode_category,
        'emoji_category': emoji_category,
        'is_emoji': True,
    }


def random_emoji(category: Optional[str] = None) -> str:
    """
    生成随机 Emoji
    
    Args:
        category: 可选的分类名称，支持：
            - 'smileys': 表情符号
            - 'animals': 动物与自然
            - 'food': 食物与饮料
            - 'activities': 活动与运动
            - 'objects': 物品
            - 'symbols': 符号
            - 'flags': 旗帜
            - 'travel': 旅行与地点
            
    Returns:
        str: 随机 Emoji
        
    Example:
        >>> random_emoji()  # 随机 Emoji
        '😀'
        >>> random_emoji('smileys')  # 表情符号
        '😊'
    """
    if category and category in EMOJI_CATEGORIES:
        ranges = EMOJI_CATEGORIES[category]['ranges']
    else:
        ranges = EMOJI_RANGES
    
    # 随机选择一个范围
    start, end = random.choice(ranges)
    code_point = random.randint(start, end)
    
    try:
        return chr(code_point)
    except ValueError:
        # 如果码点无效，返回一个安全的 Emoji
        return '😀'


def random_emojis(count: int = 5, category: Optional[str] = None) -> List[str]:
    """
    生成多个随机 Emoji
    
    Args:
        count: 数量
        category: 可选的分类
        
    Returns:
        List[str]: 随机 Emoji 列表
        
    Example:
        >>> random_emojis(3)
        ['😀', '🎉', '🌟']
    """
    return [random_emoji(category) for _ in range(count)]


def emoji_to_code_points(emoji: str) -> List[int]:
    """
    将 Emoji 转换为 Unicode 码点列表
    
    Args:
        emoji: Emoji 字符
        
    Returns:
        List[int]: 码点列表
        
    Example:
        >>> emoji_to_code_points('😀')
        [128512]
        >>> emoji_to_code_points('🏳️‍🌈')  # 彩虹旗
        [127987, 65039, 8205, 127752]
    """
    code_points = []
    for char in emoji:
        code_points.append(ord(char))
    return code_points


def code_points_to_emoji(code_points: List[int]) -> str:
    """
    将 Unicode 码点列表转换为 Emoji
    
    Args:
        code_points: 码点列表
        
    Returns:
        str: Emoji 字符
        
    Example:
        >>> code_points_to_emoji([128512])
        '😀'
    """
    return ''.join(chr(cp) for cp in code_points)


def categorize_emoji(emoji: str) -> Tuple[str, str]:
    """
    获取 Emoji 的分类
    
    Args:
        emoji: Emoji 字符
        
    Returns:
        Tuple[str, str]: (分类键, 分类名称)
        
    Example:
        >>> categorize_emoji('😀')
        ('smileys', '表情符号')
    """
    info = get_emoji_info(emoji)
    cat_key = info.get('emoji_category', 'other')
    cat_name = EMOJI_CATEGORIES.get(cat_key, {}).get('name', '其他')
    return (cat_key, cat_name)


def categorize_text_emojis(text: str) -> Dict[str, List[str]]:
    """
    按分类归组文本中的 Emoji
    
    Args:
        text: 输入文本
        
    Returns:
        Dict[str, List[str]]: 分类 -> Emoji 列表
        
    Example:
        >>> categorize_text_emojis('😀 🐱 🍕 ⚽')
        {'smileys': ['😀'], 'animals': ['🐱'], 'food': ['🍕'], 'activities': ['⚽']}
    """
    emojis = extract_emojis(text)
    result = {}
    
    for emoji in emojis:
        cat_key, _ = categorize_emoji(emoji)
        if cat_key not in result:
            result[cat_key] = []
        result[cat_key].append(emoji)
    
    return result


def is_emoji_only(text: str) -> bool:
    """
    判断文本是否只包含 Emoji（和空白字符）
    
    Args:
        text: 输入文本
        
    Returns:
        bool: 是否只包含 Emoji
        
    Example:
        >>> is_emoji_only('😀 🎉 🌟')
        True
        >>> is_emoji_only('Hello 😀')
        False
    """
    # 移除空白字符
    text_no_space = text.replace(' ', '').replace('\t', '').replace('\n', '')
    if not text_no_space:
        return False
    
    emojis = extract_emojis(text_no_space)
    emoji_text = ''.join(emojis)
    
    return emoji_text == text_no_space


def find_emoji_positions(text: str) -> List[Tuple[int, int, str]]:
    """
    找出文本中所有 Emoji 的位置
    
    Args:
        text: 输入文本
        
    Returns:
        List[Tuple[int, int, str]]: (开始位置, 结束位置, Emoji)
        
    Example:
        >>> find_emoji_positions('Hello 😀 World 🎉')
        [(6, 7, '😀'), (15, 16, '🎉')]
    """
    positions = []
    i = 0
    
    while i < len(text):
        char = text[i]
        
        if is_emoji(char):
            # 检查是否是组合 Emoji
            j = i + 1
            while j < len(text):
                next_char = text[j]
                if ord(next_char) in [0x200D, 0xFE0F, 0x20E3]:
                    j += 1
                elif 0x1F3FB <= ord(next_char) <= 0x1F3FF:  # 肤色修饰符
                    j += 1
                elif 0x1F1E0 <= ord(next_char) <= 0x1F1FF:  # 区域指示符
                    j += 1
                else:
                    break
            
            positions.append((i, j, text[i:j]))
            i = j
        else:
            i += 1
    
    return positions


def replace_emojis_with_text(text: str, emoji_text_map: Optional[Dict[str, str]] = None) -> str:
    """
    将 Emoji 替换为文本描述
    
    Args:
        text: 输入文本
        emoji_text_map: Emoji 到文本的映射字典，如果为 None 则使用 Unicode 名称
        
    Returns:
        str: 替换后的文本
        
    Example:
        >>> replace_emojis_with_text('Hello 😀', {'😀': '[开心]'})
        'Hello [开心]'
    """
    emojis = extract_emojis(text)
    result = text
    
    for emoji in emojis:
        if emoji_text_map and emoji in emoji_text_map:
            replacement = emoji_text_map[emoji]
        else:
            # 使用 Unicode 名称
            info = get_emoji_info(emoji)
            replacement = f'[{info["name"]}]' if info['name'] else ''
        
        result = result.replace(emoji, replacement, 1)
    
    return result


def filter_by_category(emojis: List[str], category: str) -> List[str]:
    """
    筛选指定分类的 Emoji
    
    Args:
        emojis: Emoji 列表
        category: 分类名称
        
    Returns:
        List[str]: 筛选后的 Emoji 列表
        
    Example:
        >>> filter_by_category(['😀', '🐱', '🍕'], 'smileys')
        ['😀']
    """
    result = []
    for emoji in emojis:
        cat_key, _ = categorize_emoji(emoji)
        if cat_key == category:
            result.append(emoji)
    return result


def get_all_emojis_in_category(category: str, limit: int = 100) -> List[str]:
    """
    获取指定分类中的所有 Emoji（样本）
    
    Args:
        category: 分类名称
        limit: 最大返回数量
        
    Returns:
        List[str]: Emoji 列表
        
    Example:
        >>> get_all_emojis_in_category('smileys', 10)
        ['😀', '😃', '😄', ...]
    """
    if category not in EMOJI_CATEGORIES:
        return []
    
    emojis = []
    for start, end in EMOJI_CATEGORIES[category]['ranges']:
        for cp in range(start, min(end + 1, start + limit)):
            try:
                char = chr(cp)
                # 简单验证是否为有效字符
                if is_emoji(char):
                    emojis.append(char)
                    if len(emojis) >= limit:
                        return emojis
            except (ValueError, OverflowError):
                continue
    
    return emojis


# 常用 Emoji 快捷常量
COMMON_EMOJIS = {
    'smile': '😊',
    'laugh': '😂',
    'love': '❤️',
    'fire': '🔥',
    'star': '⭐',
    'thumbs_up': '👍',
    'thumbs_down': '👎',
    'check': '✅',
    'cross': '❌',
    'warning': '⚠️',
    'rocket': '🚀',
    'party': '🎉',
    'cool': '😎',
    'sad': '😢',
    'angry': '😠',
    'think': '🤔',
    'pray': '🙏',
    'clap': '👏',
    'ok': '👌',
    'wave': '👋',
}


def get_common_emoji(name: str) -> Optional[str]:
    """
    根据名称获取常用 Emoji
    
    Args:
        name: Emoji 名称键
        
    Returns:
        Optional[str]: Emoji 字符，如果不存在返回 None
        
    Example:
        >>> get_common_emoji('smile')
        '😊'
    """
    return COMMON_EMOJIS.get(name.lower())


# 导出公共 API
__all__ = [
    # 核心函数
    'is_emoji',
    'extract_emojis',
    'remove_emojis',
    'count_emojis',
    'get_emoji_stats',
    
    # 信息函数
    'get_emoji_info',
    'categorize_emoji',
    'emoji_to_code_points',
    'code_points_to_emoji',
    
    # 生成函数
    'random_emoji',
    'random_emojis',
    
    # 文本处理
    'is_emoji_only',
    'find_emoji_positions',
    'replace_emojis_with_text',
    'categorize_text_emojis',
    
    # 分类筛选
    'filter_by_category',
    'get_all_emojis_in_category',
    
    # 常量
    'EMOJI_RANGES',
    'EMOJI_CATEGORIES',
    'COMMON_EMOJIS',
    'get_common_emoji',
]