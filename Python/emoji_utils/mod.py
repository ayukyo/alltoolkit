"""
Emoji Utils - 零依赖的 Emoji 处理工具模块

功能：
- 检测文本中的 emoji
- 提取所有 emoji
- 移除 emoji
- 替换 emoji 为描述文本
- 统计 emoji 使用频率
- 按类别分组 emoji
"""

import re
from typing import Dict, List, Tuple, Set, Optional
from collections import Counter
from enum import Enum


class EmojiCategory(Enum):
    """Emoji 类别枚举"""
    FACES = "faces"  # 表情脸
    PEOPLE = "people"  # 人物
    ANIMALS = "animals"  # 动物
    NATURE = "nature"  # 自然
    FOOD = "food"  # 食物
    ACTIVITIES = "activities"  # 活动
    TRAVEL = "travel"  # 旅行
    OBJECTS = "objects"  # 物品
    SYMBOLS = "symbols"  # 符号
    FLAGS = "flags"  # 旗帜
    UNKNOWN = "unknown"  # 未知


# 组合字符和修饰符
COMBINING_CHARS = {
    0x200D,   # Zero Width Joiner (ZWJ) - 用于组合 emoji
    0xFE0F,   # Variation Selector-16 (emoji 变体)
    0xFE0E,   # Variation Selector-15 (text 变体)
    0x20E3,   # Combining Enclosing Keycap
}

# 肤色修饰符范围
SKIN_TONE_START = 0x1F3FB
SKIN_TONE_END = 0x1F3FF

# Emoji Unicode 范围（主要范围，涵盖大多数 emoji）
EMOJI_RANGES = [
    (0x1F600, 0x1F64F),  # Emoticons
    (0x1F300, 0x1F5FF),  # Misc Symbols and Pictographs
    (0x1F680, 0x1F6FF),  # Transport and Map
    (0x1F1E0, 0x1F1FF),  # Flags (regional indicator symbols)
    (0x2600, 0x26FF),    # Misc symbols
    (0x2700, 0x27BF),    # Dingbats
    (0x1F900, 0x1F9FF),  # Supplemental Symbols and Pictographs
    (0x1FA00, 0x1FA6F),  # Chess Symbols
    (0x1FA70, 0x1FAFF),  # Symbols and Pictographs Extended-A
    (0x231A, 0x231B),    # Watch, Hourglass
    (0x23E9, 0x23F3),    # Various
    (0x23F8, 0x23FA),    # Various
    (0x25AA, 0x25AB),    # Squares
    (0x25B6, 0x25C0),    # Play/Reverse buttons
    (0x25FB, 0x25FE),    # Squares
    (0x2614, 0x2615),    # Umbrella, Hot Beverage
    (0x2648, 0x2653),    # Zodiac
    (0x267F, 0x267F),    # Wheelchair
    (0x2693, 0x2693),    # Anchor
    (0x26A1, 0x26A1),    # High Voltage
    (0x26AA, 0x26AB),    # Circles
    (0x26BD, 0x26BE),    # Soccer, Baseball
    (0x26C4, 0x26C5),    # Snowman, Sun
    (0x26CE, 0x26CE),    # Ophiuchus
    (0x26D4, 0x26D4),    # No Entry
    (0x26EA, 0x26EA),    # Church
    (0x26F2, 0x26F3),    # Fountain, Golf
    (0x26F5, 0x26F5),    # Sailboat
    (0x26FA, 0x26FA),    # Tent
    (0x26FD, 0x26FD),    # Fuel Pump
    (0x2702, 0x2705),    # Scissors to Check Mark
    (0x2708, 0x270D),    # Various
    (0x270F, 0x2712),    # Pencil, Nib
    (0x2714, 0x2716),    # Check/Cross Marks
    (0x271D, 0x2721),    # Cross, Star of David
    (0x2728, 0x2728),    # Sparkles
    (0x2733, 0x2734),    # Asterisks
    (0x2744, 0x2747),    # Snowflake, Sparkle
    (0x274C, 0x274E),    # Cross Marks
    (0x2753, 0x2755),    # Question Marks
    (0x2757, 0x2757),    # Exclamation Mark
    (0x2763, 0x2764),    # Heart Exclamation, Heart
    (0x2795, 0x2797),    # Plus, Minus, Divide
    (0x27A1, 0x27A1),    # Right Arrow
    (0x27B0, 0x27BF),    # Curly Loops
    (0x2934, 0x2935),    # Arrows
    (0x2B05, 0x2B07),    # Arrows
    (0x2B1B, 0x2B1C),    # Squares
    (0x2B50, 0x2B50),    # Star
    (0x2B55, 0x2B55),    # Circle
    (0x3030, 0x3030),    # Wavy Dash
    (0x303D, 0x303D),    # Part Alternation Mark
    (0x3297, 0x3297),    # Circled Ideograph Congratulation
    (0x3299, 0x3299),    # Circled Ideograph Secret
    (0x1F3FB, 0x1F3FF),  # Skin tone modifiers
    # Tags for flag emojis
    (0xE0020, 0xE007F),
]


def _is_base_emoji(code_point: int) -> bool:
    """检查是否是基础 emoji（不含组合字符）"""
    # 肤色修饰符不是基础 emoji
    if SKIN_TONE_START <= code_point <= SKIN_TONE_END:
        return False
    # 组合字符不是基础 emoji
    if code_point in COMBINING_CHARS:
        return False
    # Tag characters 不是基础 emoji
    if 0xE0020 <= code_point <= 0xE007F:
        return False
    
    for start, end in EMOJI_RANGES:
        if start <= code_point <= end:
            return True
    return False


def _is_emoji_component(code_point: int) -> bool:
    """检查是否是 emoji 的组成部分（包括组合字符和修饰符）"""
    # 组合字符
    if code_point in COMBINING_CHARS:
        return True
    # 肤色修饰符
    if SKIN_TONE_START <= code_point <= SKIN_TONE_END:
        return True
    # Tag characters (用于旗帜 emoji)
    if 0xE0020 <= code_point <= 0xE007F:
        return True
    # 基础 emoji
    return _is_base_emoji(code_point)


def _extract_emoji_sequences(text: str) -> List[str]:
    """
    提取文本中的所有 emoji 序列
    
    正确处理：
    - 简单 emoji (👋)
    - 带肤色修饰符的 emoji (👋🏻)
    - ZWJ 组合 emoji (👨‍👩‍👧‍👦)
    - 旗帜 emoji (🇺🇸)
    """
    if not text:
        return []
    
    emojis = []
    i = 0
    
    while i < len(text):
        char = text[i]
        code_point = ord(char)
        
        # 检查是否是基础 emoji
        if _is_base_emoji(code_point):
            # 开始一个 emoji 序列
            emoji_start = i
            emoji_end = i + 1
            
            # 检查后续的组成字符
            j = i + 1
            while j < len(text):
                next_cp = ord(text[j])
                
                # 如果是组成字符，继续扩展 emoji
                if next_cp in COMBINING_CHARS or \
                   (SKIN_TONE_START <= next_cp <= SKIN_TONE_END) or \
                   _is_base_emoji(next_cp):
                    # ZWJ 连接下一个 emoji，继续组合
                    if next_cp == 0x200D:  # ZWJ
                        emoji_end = j + 1
                        j += 1
                        # 继续查找 ZWJ 后的下一个 emoji 或修饰符
                        while j < len(text):
                            next_cp2 = ord(text[j])
                            if _is_base_emoji(next_cp2) or \
                               (SKIN_TONE_START <= next_cp2 <= SKIN_TONE_END):
                                emoji_end = j + 1
                                j += 1
                            elif next_cp2 == 0x200D:
                                emoji_end = j + 1
                                j += 1
                            else:
                                break
                    # 肤色修饰符
                    elif SKIN_TONE_START <= next_cp <= SKIN_TONE_END:
                        emoji_end = j + 1
                        j += 1
                    # 变体选择器
                    elif next_cp in (0xFE0F, 0xFE0E):
                        emoji_end = j + 1
                        j += 1
                    # 另一个基础 emoji - 不组合（除非前面有 ZWJ）
                    elif _is_base_emoji(next_cp):
                        # 检查是否有 ZWJ 在前面
                        if j > emoji_start and ord(text[j-1]) == 0x200D:
                            emoji_end = j + 1
                            j += 1
                        else:
                            break
                    else:
                        break
                else:
                    break
            
            # 提取 emoji
            emoji = text[emoji_start:emoji_end]
            emojis.append(emoji)
            i = emoji_end
        elif code_point in COMBINING_CHARS or \
             (SKIN_TONE_START <= code_point <= SKIN_TONE_END):
            # 单独的组合字符（没有前面的 emoji），跳过
            i += 1
        else:
            # 非 emoji 字符
            i += 1
    
    return emojis


def detect_emoji(text: str) -> bool:
    """
    检测文本中是否包含 emoji
    
    Args:
        text: 要检测的文本
        
    Returns:
        bool: 如果包含 emoji 返回 True，否则返回 False
        
    Example:
        >>> detect_emoji("Hello! 👋")
        True
        >>> detect_emoji("Hello World")
        False
    """
    if not text:
        return False
    return len(_extract_emoji_sequences(text)) > 0


def extract_emoji(text: str) -> List[str]:
    """
    从文本中提取所有 emoji
    
    Args:
        text: 要提取的文本
        
    Returns:
        List[str]: emoji 列表
        
    Example:
        >>> extract_emoji("Hello! 👋😊 World! 🌍")
        ['👋', '😊', '🌍']
    """
    return _extract_emoji_sequences(text)


def remove_emoji(text: str, replacement: str = "") -> str:
    """
    从文本中移除 emoji
    
    Args:
        text: 要处理的文本
        replacement: 替换文本（默认为空字符串）
        
    Returns:
        str: 移除 emoji 后的文本
        
    Example:
        >>> remove_emoji("Hello! 👋😊 World! 🌍")
        'Hello!  World! '
    """
    if not text:
        return ""
    
    emojis = _extract_emoji_sequences(text)
    result = text
    
    for emoji in emojis:
        result = result.replace(emoji, replacement)
    
    return result


def replace_emoji(text: str, replacement_map: Optional[Dict[str, str]] = None,
                  default_replacement: str = "[emoji]") -> str:
    """
    将文本中的 emoji 替换为描述文本
    
    Args:
        text: 要处理的文本
        replacement_map: 自定义 emoji 替换映射（可选）
        default_replacement: 默认替换文本
        
    Returns:
        str: 替换后的文本
        
    Example:
        >>> replace_emoji("Hello! 👋")
        "Hello! [waving hand]"
    """
    if not text:
        return ""
    
    if replacement_map is None:
        replacement_map = EMOJI_DESCRIPTIONS
    
    emojis = _extract_emoji_sequences(text)
    result = text
    
    for emoji in emojis:
        # 尝试完整匹配
        description = replacement_map.get(emoji)
        if description is None:
            # 对于组合 emoji，取第一个基础 emoji
            for char in emoji:
                if _is_base_emoji(ord(char)):
                    description = replacement_map.get(char, default_replacement)
                    break
            if description is None:
                description = default_replacement
        result = result.replace(emoji, f"[{description}]")
    
    return result


def count_emoji(text: str) -> int:
    """
    统计文本中 emoji 的数量
    
    Args:
        text: 要统计的文本
        
    Returns:
        int: emoji 数量
        
    Example:
        >>> count_emoji("Hello! 👋😊 World! 🌍")
        3
    """
    return len(_extract_emoji_sequences(text))


def get_emoji_frequency(text: str) -> Dict[str, int]:
    """
    获取文本中 emoji 的频率统计
    
    Args:
        text: 要统计的文本
        
    Returns:
        Dict[str, int]: emoji 频率字典
        
    Example:
        >>> get_emoji_frequency("Hello! 👋😊👋")
        {'👋': 2, '😊': 1}
    """
    emojis = _extract_emoji_sequences(text)
    return dict(Counter(emojis))


# Emoji 描述映射（常用 emoji）
EMOJI_DESCRIPTIONS = {
    # 表情脸
    "😀": "grinning face", "😃": "grinning face with big eyes", "😄": "grinning face with smiling eyes",
    "😁": "beaming face with smiling eyes", "😅": "grinning face with sweat", "😂": "face with tears of joy",
    "🤣": "rolling on the floor laughing", "😊": "smiling face with smiling eyes", "😇": "smiling face with halo",
    "🙂": "slightly smiling face", "🙃": "upside-down face", "😉": "winking face",
    "😌": "relieved face", "😍": "smiling face with heart-eyes", "🥰": "smiling face with hearts",
    "😘": "face blowing a kiss", "😗": "kissing face", "😙": "kissing face with smiling eyes",
    "😚": "kissing face with closed eyes", "😋": "face savoring food", "😛": "face with tongue",
    "😜": "winking face with tongue", "🤪": "zany face", "😝": "squinting face with tongue",
    "🤑": "money-mouth face", "🤗": "hugging face", "🤭": "face with hand over mouth",
    "🤫": "shushing face", "🤔": "thinking face", "🤐": "zipper-mouth face",
    "🤨": "face with raised eyebrow", "😐": "neutral face", "😑": "expressionless face",
    "😶": "face without mouth", "😏": "smirking face", "😒": "unamused face",
    "🙄": "face with rolling eyes", "😬": "grimacing face",
    "🤥": "lying face", "😔": "pensive face",
    "😪": "sleepy face", "🤤": "drooling face", "😴": "sleeping face",
    "😷": "face with medical mask", "🤒": "face with thermometer", "🤕": "face with head-bandage",
    "🤢": "nauseated face", "🤮": "face vomiting", "🤧": "sneezing face",
    "🥵": "hot face", "🥶": "cold face", "🥴": "woozy face",
    "😵": "dizzy face", "🤯": "exploding head",
    "🤠": "cowboy hat face", "🥳": "partying face", "🥸": "disguised face",
    "😎": "smiling face with sunglasses", "🤓": "nerd face", "🧐": "face with monocle",
    
    # 常用符号
    "❤": "red heart", "❤️": "red heart", "🧡": "orange heart", "💛": "yellow heart",
    "💚": "green heart", "💙": "blue heart", "💜": "purple heart",
    "🖤": "black heart", "🤍": "white heart", "🤎": "brown heart",
    "💔": "broken heart", "❣": "heart exclamation", "❣️": "heart exclamation", "💕": "two hearts",
    "💞": "revolving hearts", "💓": "beating heart", "💗": "growing heart",
    "💖": "sparkling heart", "💘": "heart with arrow", "💝": "heart with ribbon",
    "💟": "heart decoration", "☮": "peace symbol", "☮️": "peace symbol",
    "✝": "latin cross", "✝️": "latin cross", "☪": "star and crescent", "☪️": "star and crescent",
    "🕉": "om", "🕉️": "om", "✡": "star of david", "✡️": "star of david",
    "☸": "wheel of dharma", "☸️": "wheel of dharma", "☯": "yin yang", "☯️": "yin yang",
    "☦": "orthodox cross", "☦️": "orthodox cross", "⛩": "shinto shrine", "⛩️": "shinto shrine",
    "🕎": "menorah", "🔯": "dotted six-pointed star",
    
    # 手势
    "👋": "waving hand", "🤚": "raised back of hand", "🖐": "hand with fingers splayed", "🖐️": "hand with fingers splayed",
    "✋": "raised hand", "🖖": "vulcan salute", "👌": "OK hand",
    "🤌": "pinched fingers", "🤏": "pinching hand", "✌": "victory hand", "✌️": "victory hand",
    "🤞": "crossed fingers", "🤟": "love-you gesture", "🤘": "sign of the horns",
    "🤙": "call me hand", "👈": "backhand index pointing left", "👉": "backhand index pointing right",
    "👆": "backhand index pointing up", "🖕": "middle finger", "👇": "backhand index pointing down",
    "☝": "index pointing up", "☝️": "index pointing up", "👍": "thumbs up", "👎": "thumbs down",
    "✊": "raised fist", "👊": "oncoming fist", "🤛": "left-facing fist",
    "🤜": "right-facing fist", "👏": "clapping hands", "🙌": "raising hands",
    "👐": "open hands", "🤲": "palms up together", "🤝": "handshake",
    "🙏": "folded hands",
    
    # 动物
    "🐶": "dog face", "🐱": "cat face", "🐭": "mouse face",
    "🐹": "hamster", "🐰": "rabbit face", "🦊": "fox",
    "🐻": "bear", "🐼": "panda", "🐨": "koala",
    "🐯": "tiger face", "🦁": "lion", "🐮": "cow face",
    "🐷": "pig face", "🐸": "frog", "🐵": "monkey face",
    "🙈": "see-no-evil monkey", "🙉": "hear-no-evil monkey", "🙊": "speak-no-evil monkey",
    "🐒": "monkey", "🐔": "chicken", "🐧": "penguin",
    "🐦": "bird", "🐤": "baby chick", "🦆": "duck",
    "🦅": "eagle", "🦉": "owl", "🦇": "bat",
    "🐺": "wolf", "🐗": "boar", "🐴": "horse face",
    "🦄": "unicorn", "🐝": "honeybee", "🪲": "beetle",
    "🐛": "bug", "🦋": "butterfly", "🐌": "snail",
    "🐞": "lady beetle", "🐜": "ant", "🪰": "fly",
    "🦟": "mosquito", "🪱": "worm", "🐢": "turtle",
    "🐍": "snake", "🦎": "lizard", "🦖": "T-Rex",
    "🦕": "sauropod", "🐙": "octopus", "🦑": "squid",
    "🦐": "shrimp", "🦞": "lobster", "🦀": "crab",
    "🐡": "blowfish", "🐠": "tropical fish", "🐟": "fish",
    "🐬": "dolphin", "🐳": "whale", "🐋": "whale",
    "🦈": "shark", "🐊": "crocodile", "🐅": "tiger",
    "🐆": "leopard", "🦓": "zebra", "🦍": "gorilla",
    "🦧": "orangutan", "🦣": "mammoth", "🐘": "elephant",
    "🦛": "hippopotamus", "🦏": "rhinoceros", "🐪": "camel",
    "🐫": "two-hump camel", "🦒": "giraffe", "🦘": "kangaroo",
    "🦬": "bison", "🐃": "water buffalo", "🐂": "ox",
    "🐄": "cow", "🐎": "horse", "🐖": "pig",
    "_RAM": "ram", "🐑": "ewe", "🦙": "llama",
    "🐐": "goat", "🦌": "deer", "🐕": "dog",
    "🐩": "poodle", "🦮": "guide dog", "🐈": "cat",
    
    # 食物
    "🍎": "red apple", "🍐": "pear", "🍊": "tangerine",
    "🍋": "lemon", "🍌": "banana", "🍉": "watermelon",
    "🍇": "grapes", "🍓": "strawberry", "🫐": "blueberries",
    "🍈": "melon", "🍒": "cherries", "🍑": "peach",
    "🥭": "mango", "🍍": "pineapple", "🥥": "coconut",
    "🥝": "kiwi fruit", "🍅": "tomato", "🍆": "eggplant",
    "🥑": "avocado", "🥦": "broccoli", "🥬": "leafy green",
    "🥒": "cucumber", "🌶": "hot pepper", "🌶️": "hot pepper", "🫑": "bell pepper",
    "🌽": "ear of corn", "🥕": "carrot", "🫒": "olive",
    "🧄": "garlic", "🧅": "onion", "🥔": "potato",
    "🍠": "roasted sweet potato", "🥐": "croissant", "🥯": "bagel",
    "🍞": "bread", "🥖": "baguette bread", "🥨": "pretzel",
    "🧀": "cheese wedge", "🥚": "egg", "🍳": "cooking",
    "🧈": "butter", "🥞": "pancakes", "🧇": "waffle",
    "🥓": "bacon", "🥩": "cut of meat", "🍗": "poultry leg",
    "🍖": "meat on bone", "🦴": "bone", "🌭": "hot dog",
    "🍔": "hamburger", "🍟": "french fries", "🍕": "pizza",
    "🥪": "sandwich", "🥙": "stuffed flatbread", "🧆": "falafel",
    "🌮": "taco", "🌯": "burrito", "🫔": "tamale",
    "🥗": "green salad", "🥘": "shallow pan of food", "🫕": "fondue",
    "🍝": "spaghetti", "🍜": "steaming bowl", "🍲": "pot of food",
    "🍛": "curry rice", "🍣": "sushi", "🍱": "bento box",
    "🥟": "dumpling", "🦪": "oyster", "🍤": "fried shrimp",
    "🍙": "rice ball", "🍘": "rice cracker", "🍥": "fish cake with swirl",
    "🥠": "fortune cookie", "🥡": "takeout box", "🍦": "soft ice cream",
    "🍧": "shaved ice", "🍨": "ice cream", "🍩": "doughnut",
    "🍪": "cookie", "🎂": "birthday cake", "🍰": "shortcake",
    "🧁": "cupcake", "🥧": "pie", "🍫": "chocolate bar",
    "🍬": "candy", "🍭": "lollipop", "🍮": "custard",
    "🍯": "honey pot", "🍼": "baby bottle", "🥛": "glass of milk",
    "☕": "hot beverage", "🍵": "teacup without handle", "🧃": "beverage box",
    "🥤": "cup with straw", "🧋": "bubble tea", "🫖": "teapot",
    "🍶": "sake", "🍺": "beer mug", "🍻": "clinking beer mugs",
    "🥂": "clinking glasses", "🥃": "tumbler glass", "🫗": "pouring liquid",
    "🍷": "wine glass",
    
    # 活动和运动
    "⚽": "soccer ball", "🏀": "basketball", "🏈": "american football",
    "⚾": "baseball", "🥎": "softball", "🎾": "tennis",
    "🏐": "volleyball", "🏉": "rugby football", "🥏": "flying disc",
    "🎱": "pool 8 ball", "🪀": "yo-yo", "🏓": "ping pong",
    "🏸": "badminton", "🏒": "ice hockey", "🏑": "field hockey",
    "🥍": "lacrosse", "🏏": "cricket game", "🥅": "goal net",
    "⛳": "flag in hole", "🪁": "kite", "🛹": "skateboard",
    "🛼": "roller skate", "🎿": "skis", "⛷": "skier", "⛷️": "skier",
    "🏂": "snowboarder", "🤺": "person fencing",
    "🤼": "people wrestling", "🤽": "person playing water polo",
    "🤾": "person playing handball", "🏌": "person golfing", "🏌️": "person golfing",
    "🏇": "horse racing", "🧘": "person in lotus position",
    "🏄": "person surfing", "🏊": "person swimming", "🤳": "selfie",
    "🏋": "person lifting weights", "🏋️": "person lifting weights",
    "🚴": "person biking", "🚵": "person mountain biking",
    "🤸": "person cartwheeling",
    
    # 旅行和地点
    "🚗": "automobile", "🚕": "taxi", "🚙": "sport utility vehicle",
    "🚌": "bus", "🚎": "trolleybus", "🏎": "racing car", "🏎️": "racing car",
    "🚓": "police car", "🚑": "ambulance", "🚒": "fire engine",
    "🚐": "minibus", "🚚": "delivery truck", "🚛": "articulated lorry",
    "🚜": "tractor", "🦯": "probing cane", "🦽": "manual wheelchair",
    "🦼": "motorized wheelchair", "🛴": "kick scooter", "🚲": "bicycle",
    "🛵": "motor scooter", "🏍": "motorcycle", "🏍️": "motorcycle",
    "🛺": "auto rickshaw", "🚨": "police car light",
    "🚔": "oncoming police car", "🚍": "oncoming bus",
    "🚘": "oncoming automobile", "🚖": "oncoming taxi",
    "🚡": "aerial tramway", "🚠": "mountain cableway",
    "🚟": "suspension railway", "🚃": "railway car",
    "🚋": "tram car", "🚞": "mountain railway", "🚝": "monorail",
    "🚄": "high-speed train", "🚅": "bullet train", "🚈": "light rail",
    "🚂": "locomotive", "🚆": "train", "🚇": "metro",
    "🚊": "tram", "🚉": "station", "✈": "airplane", "✈️": "airplane",
    "🛫": "airplane departure", "🛬": "airplane arrival", "🛩": "small airplane", "🛩️": "small airplane",
    "💺": "seat", "🛰": "satellite", "🛰️": "satellite", "🚀": "rocket",
    "🛸": "flying saucer", "🚁": "helicopter", "🛶": "canoe",
    "⛵": "sailboat", "🚤": "speedboat", "🛥": "motor boat", "🛥️": "motor boat",
    "🛳": "passenger ship", "🛳️": "passenger ship", "⛴": "ferry", "⛴️": "ferry",
    "🚢": "ship", "⚓": "anchor", "⛽": "fuel pump",
    "🏗": "building construction", "🏗️": "building construction",
    "🏢": "office building", "🏣": "Japanese post office", "🏤": "post office",
    "🏥": "hospital", "🏦": "bank", "🏨": "hotel",
    "🏩": "love hotel", "🏪": "convenience store", "🏫": "school",
    "🏬": "department store", "🏭": "factory", "🏯": "Japanese castle",
    "🏰": "castle", "💒": "wedding", "🗼": "Tokyo tower",
    "🗽": "Statue of Liberty", "⛪": "church", " mosque": "mosque",
    "🛤": "synagogue", "🛤️": "synagogue", "🛕": "hindu temple", "🕋": "kaaba",
    "⛲": "fountain", "⛺": "tent", "🌁": "foggy",
    "🌃": "night with stars", "🏙": "cityscape", "🏙️": "cityscape",
    "🌄": "sunrise over mountains", "🌅": "sunrise", "🌆": "cityscape at dusk",
    "🌇": "sunset", "🌉": "bridge at night", "♨": "hot springs", "♨️": "hot springs",
    "🎠": "carousel horse", "🎡": "ferris wheel", "🎢": "roller coaster",
    "💈": "barber pole", "🎪": "circus tent",
    
    # 物品
    "⌚": "watch", "📱": "mobile phone", "📲": "mobile phone with arrow",
    "💻": "laptop", "⌨": "keyboard", "⌨️": "keyboard",
    "🖥": "desktop computer", "🖥️": "desktop computer",
    "🖨": "printer", "🖨️": "printer", "🖱": "computer mouse", "🖱️": "computer mouse",
    "🖲": "trackball", "🖲️": "trackball", "🕹": "joystick", "🕹️": "joystick",
    "🗜": "clamp", "🗜️": "clamp", "💽": "computer disk", "💾": "floppy disk",
    "💿": "optical disk", "📀": "dvd", "📼": "videocassette",
    "📷": "camera", "📸": "camera with flash", "📹": "video camera",
    "🎥": "movie camera", "📽": "film projector", "📽️": "film projector",
    "🎬": "clapper board", "📺": "television", "📻": "radio",
    "🎙": "studio microphone", "🎙️": "studio microphone",
    "🎚": "level slider", "🎚️": "level slider", "🎛": "control knobs", "🎛️": "control knobs",
    "🧭": "compass", "⏱": "stopwatch", "⏱️": "stopwatch",
    "⏲": "timer clock", "⏲️": "timer clock", "⏰": "alarm clock",
    "🕰": "mantelpiece clock", "🕰️": "mantelpiece clock",
    "⌛": "hourglass done", "⏳": "hourglass not done",
    "📡": "satellite antenna", "🔋": "battery", "🔌": "electric plug",
    "💡": "light bulb", "🔦": "flashlight", "🕯": "candle", "🕯️": "candle",
    "🪔": "diya lamp", "🧯": "fire extinguisher",
    "🛢": "oil drum", "🛢️": "oil drum", "💸": "money with wings",
    "💵": "dollar banknote", "💴": "yen banknote", "💶": "euro banknote",
    "💷": "pound banknote", "💰": "money bag", "💳": "credit card",
    "🧾": "receipt", "💎": "gem stone", "⚖": "balance scale", "⚖️": "balance scale",
    "🧰": "toolbox", "🔧": "wrench", "🔨": "hammer",
    "⚒": "hammer and pick", "⚒️": "hammer and pick",
    "🛠": "hammer and wrench", "🛠️": "hammer and wrench",
    "⛏": "pick", "⛏️": "pick", "🔩": "nut and bolt",
    "⚙": "gear", "⚙️": "gear", "🧱": "brick",
    "⛓": "chains", "⛓️": "chains", "🧲": "magnet",
    "🔫": "water pistol", "💣": "bomb", "🧨": "firecracker",
    "🪓": "axe", "🔪": "kitchen knife", "🗡": "dagger", "🗡️": "dagger",
    "⚔": "crossed swords", "⚔️": "crossed swords", "🛡": "shield", "🛡️": "shield",
    "🚬": "cigarette", "⚰": "coffin", "⚰️": "coffin", "🪦": "headstone",
    "⚱": "funeral urn", "⚱️": "funeral urn", "🏺": "amphora",
    "🔮": "crystal ball", "📿": "prayer beads", "🧿": "nazar amulet",
    
    # 符号
    "🏧": "ATM sign", "🚮": "litter in bin sign", "🚰": "potable water",
    "♿": "wheelchair symbol", "🚹": "men's room", "🚺": "women's room",
    "🚻": "restroom", "🚼": "baby symbol", "🚾": "water closet",
    "🛂": "passport control", "🛃": "customs", "🛄": "baggage claim",
    "🛅": "left luggage", "⚠": "warning", "⚠️": "warning",
    "🚸": "children crossing", "⛔": "no entry", "🚫": "prohibited",
    "🚳": "no bicycles", "🚭": "no smoking", "🚯": "no littering",
    "🚱": "non-potable water", "🚷": "no pedestrians", "📵": "no mobile phones",
    "🔞": "no one under eighteen", "☢": "radioactive", "☢️": "radioactive",
    "☣": "biohazard", "☣️": "biohazard",
    "⬆": "up arrow", "⬆️": "up arrow", "↗": "up-right arrow", "↗️": "up-right arrow",
    "➡": "right arrow", "➡️": "right arrow", "↘": "down-right arrow", "↘️": "down-right arrow",
    "⬇": "down arrow", "⬇️": "down arrow", "↙": "down-left arrow", "↙️": "down-left arrow",
    "⬅": "left arrow", "⬅️": "left arrow", "↖": "up-left arrow", "↖️": "up-left arrow",
    "↕": "up-down arrow", "↕️": "up-down arrow", "↔": "left-right arrow", "↔️": "left-right arrow",
    "↩": "right arrow curving left", "↩️": "right arrow curving left",
    "↪": "left arrow curving right", "↪️": "left arrow curving right",
    "⤴": "right arrow curving up", "⤴️": "right arrow curving up",
    "⤵": "right arrow curving down", "⤵️": "right arrow curving down",
    "🔃": "clockwise vertical arrows", "🔄": "counterclockwise arrows button",
    "🔙": "BACK arrow", "🔚": "END arrow", "🔛": "ON! arrow",
    "🔜": "SOON arrow", "🔝": "TOP arrow", "🛐": "place of worship",
    "⚛": "atom symbol", "⚛️": "atom symbol",
    "✡": "star of David", "✡️": "star of David",
    "☮": "peace symbol", "☮️": "peace symbol",
    "🕎": "menorah", "🔯": "dotted six-pointed star",
    "♈": "Aries", "♉": "Taurus", "♊": "Gemini", "♋": "Cancer",
    "♌": "Leo", "♍": "Virgo", "♎": "Libra", "♏": "Scorpio",
    "♐": "Sagittarius", "♑": "Capricorn", "♒": "Aquarius", "♓": "Pisces",
    "⛎": "Ophiuchus",
    "🔀": "shuffle tracks button", "🔁": "repeat button", "🔂": "repeat single",
    "▶": "play button", "▶️": "play button", "⏩": "fast-forward button",
    "⏭": "next track button", "⏭️": "next track button",
    "⏯": "play or pause button", "⏯️": "play or pause button",
    "◀": "reverse button", "◀️": "reverse button", "⏪": "fast reverse button",
    "⏮": "last track button", "⏮️": "last track button",
    "🔼": "upwards button", "⏫": "fast up button",
    "🔽": "downwards button", "⏬": "fast down button",
    "⏸": "pause button", "⏸️": "pause button",
    "⏹": "stop button", "⏹️": "stop button",
    "⏺": "record button", "⏺️": "record button",
    "⏏": "eject button", "⏏️": "eject button",
    "🎦": "cinema", "🔅": "dim button", "🔆": "bright button",
    "📶": "antenna bars", "📳": "vibration mode", "📴": "mobile phone off",
    "♀": "female sign", "♀️": "female sign", "♂": "male sign", "♂️": "male sign",
    "⚕": "medical symbol", "⚕️": "medical symbol",
    "♾": "infinity", "♾️": "infinity", "♻": "recycling symbol", "♻️": "recycling symbol",
    "⚜": "fleur-de-lis", "⚜️": "fleur-de-lis", "🔱": "trident emblem",
    "📛": "name badge", "🔰": "Japanese symbol for beginner",
    "⭕": "hollow red circle", "✅": "check mark button", "☑": "check box with check", "☑️": "check box with check",
    "✔": "check mark", "✔️": "check mark", "✖": "multiply", "✖️": "multiply",
    "❌": "cross mark", "❎": "cross mark button",
    "➕": "plus", "➖": "minus", "➗": "divide",
    "➰": "curly loop", "➿": "double curly loop",
    "〽": "part alternation mark", "〽️": "part alternation mark",
    "✳": "eight-spoked asterisk", "✳️": "eight-spoked asterisk",
    "✴": "eight-pointed star", "✴️": "eight-pointed star",
    "❇": "sparkle", "❇️": "sparkle",
    "‼": "double exclamation mark", "‼️": "double exclamation mark",
    "⁉": "exclamation question mark", "⁉️": "exclamation question mark",
    "❓": "question mark", "❔": "white question mark",
    "❕": "white exclamation mark", "❗": "exclamation mark",
    "〰": "wavy dash", "〰️": "wavy dash",
    "©": "copyright", "©️": "copyright", "®": "registered", "®️": "registered",
    "™": "trade mark", "™️": "trade mark",
    "#️⃣": "keycap: #", "*️⃣": "keycap: *",
    "0️⃣": "keycap: 0", "1️⃣": "keycap: 1", "2️⃣": "keycap: 2",
    "3️⃣": "keycap: 3", "4️⃣": "keycap: 4", "5️⃣": "keycap: 5",
    "6️⃣": "keycap: 6", "7️⃣": "keycap: 7", "8️⃣": "keycap: 8",
    "9️⃣": "keycap: 9", "🔟": "keycap: 10",
    "🔠": "input latin uppercase", "🔡": "input latin lowercase",
    "🔢": "input numbers", "🔣": "input symbols", "🔤": "input latin letters",
    "🅰": "A button (blood type)", "🅰️": "A button (blood type)",
    "🆎": "AB button (blood type)", "🅱": "B button (blood type)", "🅱️": "B button (blood type)",
    "🆑": "CL button", "🆒": "COOL button", "🆓": "FREE button",
    "ℹ": "information", "ℹ️": "information", "🆔": "ID button",
    "Ⓜ": "circled M", "Ⓜ️": "circled M", "🆕": "NEW button",
    "🆖": "NG button", "🅾": "O button (blood type)", "🅾️": "O button (blood type)",
    "🆗": "OK button", "🅿": "P button", "🅿️": "P button",
    "🆘": "SOS button", "🆙": "UP! button", "🆚": "VS button",
    "🈁": 'Japanese "here" button', "🈂": 'Japanese "service charge" button', "🈂️": 'Japanese "service charge" button',
    "🈷": 'Japanese "monthly amount" button', "🈷️": 'Japanese "monthly amount" button',
    "🈶": 'Japanese "not free of charge" button',
    "🈯": 'Japanese "reserved" button', "🉐": 'Japanese "bargain" button',
    "🈹": 'Japanese "discount" button', "🈚": 'Japanese "free of charge" button',
    "🈲": 'Japanese "prohibited" button', "🉑": 'Japanese "acceptable" button',
    "🈸": 'Japanese "application" button', "🈴": 'Japanese "passing grade" button',
    "🈳": 'Japanese "vacancy" button', "㊗": 'Japanese "congratulations" button', "㊗️": 'Japanese "congratulations" button',
    "㊙": 'Japanese "secret" button', "㊙️": 'Japanese "secret" button',
    "🈺": 'Japanese "open for business" button',
    "🈵": 'Japanese "no vacancy" button',
    "🔴": "red circle", "🟠": "orange circle", "🟡": "yellow circle",
    "🟢": "green circle", "🔵": "blue circle", "🟣": "purple circle",
    "🟤": "brown circle", "⚫": "black circle", "⚪": "white circle",
    "🟥": "red square", "🟧": "orange square", "🟨": "yellow square",
    "🟩": "green square", "🟦": "blue square", "🟪": "purple square",
    "🟫": "brown square", "⬛": "black large square", "⬜": "white large square",
    "◼": "black medium square", "◼️": "black medium square",
    "◻": "white medium square", "◻️": "white medium square",
    "◾": "black medium-small square", "◽": "white medium-small square",
    "▪": "black small square", "▪️": "black small square",
    "▫": "white small square", "▫️": "white small square",
    "🔶": "large orange diamond", "🔷": "large blue diamond",
    "🔸": "small orange diamond", "🔹": "small blue diamond",
    "🔺": "red triangle pointed up", "🔻": "red triangle pointed down",
    "💠": "diamond with a dot", "🔘": "radio button",
    "🔳": "white square button", "🔲": "black square button",
    
    # 旗帜
    "🏁": "chequered flag", "🚩": "triangular flag", "🎌": "crossed flags",
    "🏴": "black flag", "🏳": "white flag", "🏳️": "white flag",
    "🏳️‍🌈": "rainbow flag", "🏳️‍⚧️": "transgender flag", "🏴‍☠️": "pirate flag",
    
    # 世界
    "🌍": "earth globe Europe-Africa", "🌎": "earth globe Americas", "🌏": "earth globe Asia-Australia",
    "🌐": "globe with meridians", "🗺": "world map", "🗺️": "world map",
    "🌑": "new moon", "🌒": "waxing crescent moon", "🌓": "first quarter moon",
    "🌔": "waxing gibbous moon", "🌕": "full moon", "🌖": "waning gibbous moon",
    "🌗": "last quarter moon", "🌘": "waning crescent moon",
    "🌙": "crescent moon", "🌚": "new moon face", "🌛": "first quarter moon face",
    "🌜": "last quarter moon face", "☀": "sun", "☀️": "sun",
    "🌝": "full moon face", "🌞": "sun with face",
    "⭐": "star", "🌟": "glowing star", "💫": "dizzy",
    "✨": "sparkles", " Meteor": "meteor", "🌠": "shooting star",
    "🔥": "fire", "💯": "hundred points", "🎉": "party popper",
    "🎊": "confetti ball", "🎈": "balloon", "🎁": "wrapped gift",
    "🎄": "Christmas tree", "🎃": "jack-o-lantern", "👻": "ghost",
    "🎅": "Santa Claus", "🤶": "Mrs. Claus", "🥶": "cold face",
    "❄": "snowflake", "❄️": "snowflake", "☃": "snowman", "☃️": "snowman",
    "⛄": "snowman without snow", "🌬": "wind face", "🌬️": "wind face",
    "💨": "dashing away", "💧": "droplet", "💦": "sweat droplets",
    "☔": "umbrella with rain drops", "🌈": "rainbow", "⚡": "high voltage", "⚡️": "high voltage",
    "💥": "collision", "💣": "bomb", "💭": "thought balloon",
    "💬": "speech balloon", "💬": "speech balloon", "🗨": "left speech bubble", "🗨️": "left speech bubble",
    "🗯": "right anger bubble", "🗯️": "right anger bubble", "💭": "thought balloon",
    "💤": "sleeping sign", "🌀": "cyclone", " Spider": "spider", "🕷": "spider", "🕷️": "spider",
    "🕸": "spider web", "🕸️": "spider web", "🐸": "frog",
}


# 类别映射
CATEGORY_RANGES = {
    EmojiCategory.FACES: [(0x1F600, 0x1F64F)],
    EmojiCategory.PEOPLE: [(0x1F9D0, 0x1F9FF)],
    EmojiCategory.ANIMALS: [(0x1F400, 0x1F43F), (0x1F980, 0x1F9CF)],
    EmojiCategory.NATURE: [(0x1F300, 0x1F30F), (0x1F330, 0x1F35F)],
    EmojiCategory.FOOD: [(0x1F345, 0x1F37F), (0x1F95D, 0x1F9FF)],
    EmojiCategory.ACTIVITIES: [(0x1F3A0, 0x1F3CF), (0x1F938, 0x1F94F)],
    EmojiCategory.TRAVEL: [(0x1F680, 0x1F6FF), (0x1F3D0, 0x1F3DF)],
    EmojiCategory.OBJECTS: [(0x1F4A0, 0x1F4FF), (0x1F50D, 0x1F5FF)],
    EmojiCategory.SYMBOLS: [(0x2600, 0x26FF), (0x2700, 0x27BF), (0x1F100, 0x1F1FF)],
    EmojiCategory.FLAGS: [(0x1F1E0, 0x1F1FF)],
}


def get_emoji_description(emoji: str) -> str:
    """
    获取 emoji 的描述文本
    
    Args:
        emoji: 要查询的 emoji
        
    Returns:
        str: emoji 描述
        
    Example:
        >>> get_emoji_description("👋")
        'waving hand'
    """
    if emoji in EMOJI_DESCRIPTIONS:
        return EMOJI_DESCRIPTIONS[emoji]
    
    # 对于组合 emoji，取第一个基础 emoji
    for char in emoji:
        if _is_base_emoji(ord(char)):
            if char in EMOJI_DESCRIPTIONS:
                return EMOJI_DESCRIPTIONS[char]
    
    return "unknown emoji"


def categorize_emoji(emoji: str) -> EmojiCategory:
    """
    获取 emoji 的类别
    
    Args:
        emoji: 要分类的 emoji
        
    Returns:
        EmojiCategory: emoji 类别
        
    Example:
        >>> categorize_emoji("😊")
        <EmojiCategory.FACES: 'faces'>
    """
    if not emoji:
        return EmojiCategory.UNKNOWN
    
    # 获取第一个基础 emoji 的代码点
    for char in emoji:
        if _is_base_emoji(ord(char)):
            base_code = ord(char)
            for category, ranges in CATEGORY_RANGES.items():
                for start, end in ranges:
                    if start <= base_code <= end:
                        return category
            break
    
    return EmojiCategory.UNKNOWN


def group_emoji_by_category(emojis: List[str]) -> Dict[EmojiCategory, List[str]]:
    """
    按类别分组 emoji
    
    Args:
        emojis: emoji 列表
        
    Returns:
        Dict[EmojiCategory, List[str]]: 分组后的字典
    """
    result = {category: [] for category in EmojiCategory}
    
    for emoji in emojis:
        category = categorize_emoji(emoji)
        result[category].append(emoji)
    
    return {k: v for k, v in result.items() if v}


def extract_unique_emoji(text: str) -> Set[str]:
    """
    提取文本中唯一的 emoji（去重）
    
    Args:
        text: 要提取的文本
        
    Returns:
        Set[str]: 唯一 emoji 集合
    """
    return set(_extract_emoji_sequences(text))


def is_only_emoji(text: str) -> bool:
    """
    检查文本是否只包含 emoji
    
    Args:
        text: 要检查的文本
        
    Returns:
        bool: 如果只包含 emoji 返回 True
    """
    if not text:
        return False
    
    text_no_space = text.strip()
    if not text_no_space:
        return False
    
    # 移除所有 emoji 后应该只剩下空白
    remaining = remove_emoji(text_no_space)
    return remaining.strip() == ""


def get_text_emoji_ratio(text: str) -> float:
    """
    获取文本中 emoji 的比例
    
    Args:
        text: 要计算的文本
        
    Returns:
        float: emoji 比例（0.0 到 1.0）
    """
    if not text:
        return 0.0
    
    emojis = _extract_emoji_sequences(text)
    emoji_count = len(emojis)
    
    # 计算总字符数（每个 emoji 序列算一个字符）
    total_chars = emoji_count + len(remove_emoji(text))
    
    return emoji_count / total_chars if total_chars > 0 else 0.0


def sanitize_text(text: str, max_emoji_ratio: float = 0.3) -> str:
    """
    清理文本，移除过多 emoji
    
    Args:
        text: 要处理的文本
        max_emoji_ratio: 允许的最大 emoji 比例
        
    Returns:
        str: 清理后的文本
    """
    if not text:
        return ""
    
    ratio = get_text_emoji_ratio(text)
    
    if ratio > max_emoji_ratio:
        return remove_emoji(text)
    
    return text


class EmojiUtils:
    """Emoji 工具类，提供面向对象的接口"""
    
    def __init__(self, text: str):
        self._text = text
        self._emojis: Optional[List[str]] = None
    
    @property
    def text(self) -> str:
        return self._text
    
    @text.setter
    def text(self, value: str):
        self._text = value
        self._emojis = None
    
    @property
    def emojis(self) -> List[str]:
        if self._emojis is None:
            self._emojis = _extract_emoji_sequences(self._text)
        return self._emojis
    
    @property
    def has_emoji(self) -> bool:
        return len(self.emojis) > 0
    
    @property
    def emoji_count(self) -> int:
        return len(self.emojis)
    
    @property
    def unique_emojis(self) -> Set[str]:
        return set(self.emojis)
    
    @property
    def emoji_frequency(self) -> Dict[str, int]:
        return dict(Counter(self.emojis))
    
    def remove_emoji(self, replacement: str = "") -> str:
        return remove_emoji(self._text, replacement)
    
    def replace_emoji(self, replacement_map: Optional[Dict[str, str]] = None,
                      default_replacement: str = "[emoji]") -> str:
        return replace_emoji(self._text, replacement_map, default_replacement)
    
    def categorize(self) -> Dict[EmojiCategory, List[str]]:
        return group_emoji_by_category(self.emojis)
    
    def is_only_emoji(self) -> bool:
        return is_only_emoji(self._text)
    
    def emoji_ratio(self) -> float:
        return get_text_emoji_ratio(self._text)
    
    def sanitize(self, max_ratio: float = 0.3) -> str:
        return sanitize_text(self._text, max_ratio)


def analyze(text: str) -> Dict:
    """
    分析文本中的 emoji，返回完整统计信息
    
    Args:
        text: 要分析的文本
        
    Returns:
        Dict: 包含各种统计信息的字典
    """
    emojis = _extract_emoji_sequences(text)
    unique = set(emojis)
    
    return {
        'has_emoji': len(emojis) > 0,
        'emoji_count': len(emojis),
        'unique_count': len(unique),
        'emojis': emojis,
        'unique_emojis': list(unique),
        'frequency': dict(Counter(emojis)),
        'ratio': get_text_emoji_ratio(text),
        'is_only_emoji': is_only_emoji(text),
        'categories': {k.value: v for k, v in group_emoji_by_category(emojis).items()}
    }


if __name__ == "__main__":
    test_text = "Hello! 👋 I'm feeling 😊 today! 🌍🚀❤️"
    
    print(f"文本: {test_text}")
    print(f"包含 emoji: {detect_emoji(test_text)}")
    print(f"emoji 列表: {extract_emoji(test_text)}")
    print(f"emoji 数量: {count_emoji(test_text)}")
    print(f"移除 emoji: {remove_emoji(test_text)}")
    print(f"替换 emoji: {replace_emoji(test_text)}")
    print(f"emoji 频率: {get_emoji_frequency(test_text)}")
    print(f"完整分析: {analyze(test_text)}")