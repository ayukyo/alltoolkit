"""
emoji_utils - 表情符号处理工具

功能：
- 检测文本中的 emoji
- 移除/替换 emoji
- 统计 emoji 使用
- 获取 emoji 的 Unicode 信息
- 文本与 emoji 分离
- emoji 分类（表情、手势、动物、食物等）
- 文本转换为 emoji（关键词映射）

零外部依赖，纯 Python 标准库实现
"""

import re
import unicodedata
from typing import Optional


class EmojiUtils:
    """表情符号处理工具类"""
    
    # Emoji Unicode 范围（主要范围）
    EMOJI_RANGES = [
        (0x1F600, 0x1F64F),   # 表情符号
        (0x1F300, 0x1F5FF),   # 杂项符号和图标
        (0x1F680, 0x1F6FF),   # 交通和地图符号
        (0x1F700, 0x1F77F),   # 炼金术符号
        (0x1F780, 0x1F7FF),   # 几何图形扩展
        (0x1F800, 0x1F8FF),   # 补充箭头-C
        (0x1F900, 0x1F9FF),   # 补充符号和图标
        (0x1FA00, 0x1FA6F),   # 棋类符号
        (0x1FA70, 0x1FAFF),   # 符号和图标扩展-A
        (0x2600, 0x26FF),     # 杂项符号
        (0x2700, 0x27BF),     # 装饰符号
        (0xFE00, 0xFE0F),     # 变体选择符
        (0x1F000, 0x1F02F),   # 麻将牌
        (0x1F0A0, 0x1F0FF),   # 扑克牌
        (0x2300, 0x23FF),     # 杂项技术符号
        (0x2B50, 0x2B55),     # 星星等符号
        (0x203C, 0x3299),     # 其他符号
    ]
    
    # Emoji 分类
    EMOJI_CATEGORIES = {
        'smileys': list(range(0x1F600, 0x1F64F + 1)),
        'people': list(range(0x1F930, 0x1F9FF + 1)) + [0x1F44D, 0x1F44E, 0x1F44C],
        'animals': list(range(0x1F400, 0x1F44F + 1)),
        'food': list(range(0x1F300, 0x1F37F + 1)),
        'nature': [0x1F33E, 0x1F343, 0x1F344, 0x2600, 0x1F31E, 0x2B50],
        'objects': list(range(0x1F4A0, 0x1F4FF + 1)),
        'travel': list(range(0x1F680, 0x1F6FF + 1)) + [0x2708, 0x1F691],
        'activities': list(range(0x26BD, 0x26BE + 1)) + [0x1F3AE, 0x1F3AF],
        'symbols': [0x2764, 0x1F494, 0x1F495, 0x1F496, 0x2714, 0x2716, 0x26A0],
        'flags': list(range(0x1F1E6, 0x1F1FF + 1)),
    }
    
    # 关键词到 emoji 的映射
    KEYWORD_EMOJI_MAP = {
        # 表情
        'happy': '😊', 'smile': '😊', 'joy': '😂', 'laugh': '😂',
        'sad': '😢', 'cry': '😭', 'tear': '😢',
        'love': '❤️', 'heart': '❤️', 'like': '👍',
        'angry': '😠', 'mad': '😡', 'hate': '😤',
        'cool': '😎', 'star': '⭐', 'fire': '🔥',
        'think': '🤔', 'thinking': '🤔', 'wonder': '🤔',
        'wink': '😉', 'kiss': '😘', 'hug': '🤗',
        'surprise': '😮', 'shock': '😲', 'wow': '😲',
        
        # 手势
        'ok': '👌', 'yes': '✅', 'no': '❌', 'good': '👍',
        'bad': '👎', 'clap': '👏', 'wave': '👋', 'peace': '✌️',
        
        # 动物
        'cat': '🐱', 'dog': '🐶', 'bird': '🐦', 'fish': '🐟',
        'lion': '🦁', 'tiger': '🐯', 'bear': '🐻', 'fox': '🦊',
        'rabbit': '🐰', 'monkey': '🐵', 'panda': '🐼', 'koala': '🐨',
        
        # 食物
        'apple': '🍎', 'banana': '🍌', 'pizza': '🍕', 'burger': '🍔',
        'cake': '🎂', 'coffee': '☕', 'beer': '🍺', 'wine': '🍷',
        'water': '💧', 'milk': '🥛', 'bread': '🍞', 'egg': '🥚',
        
        # 自然
        'sun': '☀️', 'moon': '🌙', 'cloud': '☁️', 'rain': '🌧️',
        'snow': '❄️', 'flower': '🌸', 'tree': '🌳', 'leaf': '🍃',
        
        # 物品
        'book': '📖', 'phone': '📱', 'computer': '💻', 'car': '🚗',
        'house': '🏠', 'key': '🔑', 'light': '💡', 'clock': '⏰',
        'gift': '🎁', 'party': '🎉', 'music': '🎵', 'movie': '🎬',
        
        # 活动
        'sport': '⚽', 'game': '🎮', 'run': '🏃', 'swim': '🏊',
        'travel': '✈️', 'work': '💼', 'study': '📚', 'sleep': '😴',
    }
    
    @classmethod
    def is_emoji(cls, char: str) -> bool:
        """检查单个字符是否为 emoji"""
        if not char:
            return False
        
        code_point = ord(char[0])
        
        # 检查是否在 emoji 范围内
        for start, end in cls.EMOJI_RANGES:
            if start <= code_point <= end:
                return True
        
        # 检查变体选择符（跟随在其他字符后面）
        if 0xFE00 <= code_point <= 0xFE0F:
            return True
        
        # 检查零宽连接符（用于组合 emoji）
        if code_point == 0x200D:
            return True
        
        # 检查肤色修饰符
        if 0x1F3FB <= code_point <= 0x1F3FF:
            return True
        
        return False
    
    @classmethod
    def is_emoji_base(cls, char: str) -> bool:
        """检查是否为基础 emoji（非修饰符）"""
        if not char:
            return False
        code_point = ord(char)
        # 排除变体选择符、零宽连接符、肤色修饰符
        if 0xFE00 <= code_point <= 0xFE0F:  # 变体选择符
            return False
        if code_point == 0x200D:  # 零宽连接符
            return False
        if 0x1F3FB <= code_point <= 0x1F3FF:  # 肤色修饰符
            return False
        return cls.is_emoji(char)
    
    @classmethod
    def extract_next_emoji(cls, text: str, start: int = 0) -> tuple:
        """
        从指定位置提取一个完整的 emoji 序列
        
        Args:
            text: 输入文本
            start: 起始位置
            
        Returns:
            tuple: (emoji序列, 结束位置) 或 (None, start)
        """
        if start >= len(text):
            return None, start
        
        char = text[start]
        if not cls.is_emoji_base(char):
            return None, start
        
        # 开始构建 emoji 序列
        emoji = char
        pos = start + 1
        
        while pos < len(text):
            next_char = text[pos]
            next_code = ord(next_char)
            
            # 变体选择符 - 继续附加
            if 0xFE00 <= next_code <= 0xFE0F:
                emoji += next_char
                pos += 1
                continue
            
            # 零宽连接符 - 组合 emoji
            if next_code == 0x200D:
                emoji += next_char
                pos += 1
                # ZWJ 后面必须跟一个基础 emoji
                if pos < len(text) and cls.is_emoji_base(text[pos]):
                    emoji += text[pos]
                    pos += 1
                continue
            
            # 肤色修饰符 - 继续附加
            if 0x1F3FB <= next_code <= 0x1F3FF:
                emoji += next_char
                pos += 1
                continue
            
            # 其他字符 - 结束序列
            break
        
        return emoji, pos
    
    @classmethod
    def detect_emojis(cls, text: str) -> list:
        """
        检测文本中的所有 emoji
        
        Args:
            text: 输入文本
            
        Returns:
            list: 包含的 emoji 列表（按出现顺序，去重）
        """
        emojis = []
        seen = set()
        
        i = 0
        while i < len(text):
            emoji, next_pos = cls.extract_next_emoji(text, i)
            if emoji:
                if emoji not in seen:
                    emojis.append(emoji)
                    seen.add(emoji)
                i = next_pos
            else:
                i += 1
        
        return emojis
    
    @classmethod
    def remove_emojis(cls, text: str, replacement: str = '') -> str:
        """
        从文本中移除所有 emoji
        
        Args:
            text: 输入文本
            replacement: 替换文本（默认为空）
            
        Returns:
            str: 移除 emoji 后的文本
        """
        result = []
        i = 0
        
        while i < len(text):
            emoji, next_pos = cls.extract_next_emoji(text, i)
            if emoji:
                result.append(replacement)
                i = next_pos
            else:
                result.append(text[i])
                i += 1
        
        return ''.join(result)
    
    @classmethod
    def replace_emojis(cls, text: str, replacement_map: dict, default: str = '') -> str:
        """
        替换文本中的 emoji
        
        Args:
            text: 输入文本
            replacement_map: emoji 到替换文本的映射
            default: 未映射 emoji 的默认替换
            
        Returns:
            str: 替换后的文本
        """
        result = []
        i = 0
        
        while i < len(text):
            emoji, next_pos = cls.extract_next_emoji(text, i)
            if emoji:
                result.append(replacement_map.get(emoji, default))
                i = next_pos
            else:
                result.append(text[i])
                i += 1
        
        return ''.join(result)
    
    @classmethod
    def count_emojis(cls, text: str) -> dict:
        """
        统计文本中各 emoji 的出现次数
        
        Args:
            text: 输入文本
            
        Returns:
            dict: emoji 到出现次数的映射
        """
        counts = {}
        i = 0
        
        while i < len(text):
            emoji, next_pos = cls.extract_next_emoji(text, i)
            if emoji:
                counts[emoji] = counts.get(emoji, 0) + 1
                i = next_pos
            else:
                i += 1
        
        return counts
    
    @classmethod
    def get_emoji_info(cls, emoji: str) -> dict:
        """
        获取 emoji 的详细信息
        
        Args:
            emoji: 单个 emoji
            
        Returns:
            dict: 包含 unicode、名称、分类等信息
        """
        if not emoji:
            return {}
        
        info = {
            'emoji': emoji,
            'unicode': 'U+' + ' U+'.join(f'{ord(c):04X}' for c in emoji),
            'name': '',
            'category': 'unknown',
        }
        
        # 获取 Unicode 名称
        try:
            names = []
            for char in emoji:
                try:
                    name = unicodedata.name(char, '')
                    if name:
                        names.append(name)
                except ValueError:
                    pass
            info['name'] = ' / '.join(names) if names else 'Unknown'
        except Exception:
            info['name'] = 'Unknown'
        
        # 确定分类
        for category, code_points in cls.EMOJI_CATEGORIES.items():
            for char in emoji:
                if ord(char) in code_points:
                    info['category'] = category
                    break
            if info['category'] != 'unknown':
                break
        
        # 计算视觉长度
        info['visual_length'] = len(emoji.rstrip('\ufe0f'))
        
        return info
    
    @classmethod
    def separate_text_emoji(cls, text: str) -> tuple:
        """
        分离文本和 emoji
        
        Args:
            text: 输入文本
            
        Returns:
            tuple: (纯文本, emoji列表)
        """
        emojis = cls.detect_emojis(text)
        pure_text = cls.remove_emojis(text)
        
        # 清理多余空格
        pure_text = re.sub(r'\s+', ' ', pure_text).strip()
        
        return pure_text, emojis
    
    @classmethod
    def categorize_emojis(cls, emojis: list) -> dict:
        """
        对 emoji 进行分类
        
        Args:
            emojis: emoji 列表
            
        Returns:
            dict: 分类到 emoji 列表的映射
        """
        categories = {cat: [] for cat in cls.EMOJI_CATEGORIES.keys()}
        categories['unknown'] = []
        
        for emoji in emojis:
            categorized = False
            for char in emoji:
                code = ord(char)
                for cat, codes in cls.EMOJI_CATEGORIES.items():
                    if code in codes:
                        categories[cat].append(emoji)
                        categorized = True
                        break
                if categorized:
                    break
            
            if not categorized:
                categories['unknown'].append(emoji)
        
        # 移除空分类
        return {k: v for k, v in categories.items() if v}
    
    @classmethod
    def text_to_emoji(cls, text: str, keep_unmatched: bool = True) -> str:
        """
        将文本中的关键词转换为 emoji
        
        Args:
            text: 输入文本
            keep_unmatched: 是否保留未匹配的文本
            
        Returns:
            str: 转换后的文本
        """
        result = text.lower()
        
        # 按关键词长度降序排序，避免短关键词先匹配
        sorted_keywords = sorted(
            cls.KEYWORD_EMOJI_MAP.keys(),
            key=lambda x: len(x),
            reverse=True
        )
        
        for keyword in sorted_keywords:
            emoji = cls.KEYWORD_EMOJI_MAP[keyword]
            if keep_unmatched:
                result = re.sub(
                    rf'\b{keyword}\b',
                    emoji,
                    result,
                    flags=re.IGNORECASE
                )
            else:
                result = re.sub(
                    rf'\b{keyword}\b',
                    '',
                    result,
                    flags=re.IGNORECASE
                )
        
        return result.strip()
    
    @classmethod
    def emoji_density(cls, text: str) -> float:
        """
        计算文本中 emoji 的密度
        
        Args:
            text: 输入文本
            
        Returns:
            float: emoji 字符占总字符的比例
        """
        if not text:
            return 0.0
        
        emoji_count = 0
        i = 0
        
        while i < len(text):
            emoji, next_pos = cls.extract_next_emoji(text, i)
            if emoji:
                emoji_count += 1
                i = next_pos
            else:
                i += 1
        
        return emoji_count / len(text)
    
    @classmethod
    def extract_emoji_positions(cls, text: str) -> list:
        """
        提取文本中 emoji 的位置信息
        
        Args:
            text: 输入文本
            
        Returns:
            list: 包含 (emoji, start_pos, end_pos) 的列表
        """
        positions = []
        i = 0
        
        while i < len(text):
            emoji, next_pos = cls.extract_next_emoji(text, i)
            if emoji:
                positions.append((emoji, i, next_pos))
                i = next_pos
            else:
                i += 1
        
        return positions
    
    @classmethod
    def is_only_emojis(cls, text: str) -> bool:
        """
        检查文本是否仅由 emoji 组成
        
        Args:
            text: 输入文本
            
        Returns:
            bool: 是否仅包含 emoji
        """
        # 移除所有 emoji 后检查是否为空
        cleaned = cls.remove_emojis(text)
        return len(cleaned.strip()) == 0


# 便捷函数
def detect_emojis(text: str) -> list:
    """检测文本中的所有 emoji"""
    return EmojiUtils.detect_emojis(text)


def remove_emojis(text: str, replacement: str = '') -> str:
    """从文本中移除所有 emoji"""
    return EmojiUtils.remove_emojis(text, replacement)


def count_emojis(text: str) -> dict:
    """统计文本中各 emoji 的出现次数"""
    return EmojiUtils.count_emojis(text)


def get_emoji_info(emoji: str) -> dict:
    """获取 emoji 的详细信息"""
    return EmojiUtils.get_emoji_info(emoji)


def separate_text_emoji(text: str) -> tuple:
    """分离文本和 emoji"""
    return EmojiUtils.separate_text_emoji(text)


def text_to_emoji(text: str, keep_unmatched: bool = True) -> str:
    """将文本中的关键词转换为 emoji"""
    return EmojiUtils.text_to_emoji(text, keep_unmatched)


def emoji_density(text: str) -> float:
    """计算文本中 emoji 的密度"""
    return EmojiUtils.emoji_density(text)


def is_only_emojis(text: str) -> bool:
    """检查文本是否仅由 emoji 组成"""
    return EmojiUtils.is_only_emojis(text)