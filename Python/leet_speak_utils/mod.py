"""
Leet Speak Utils - 1337语言转换工具

Leet Speak (也称1337、leet、l33t)是一种网络俚语形式，
将标准英语字母替换为数字和特殊字符。

功能：
- 支持多级别转换（轻度、标准、重度）
- 支持编码（文本→leet）和解码（leet→文本）
- 支持自定义映射规则
- 零外部依赖
"""

from typing import Dict, List, Optional, Tuple
import re


# 默认映射表 - 按使用频率和可读性排序
DEFAULT_BASIC_MAP: Dict[str, List[str]] = {
    'a': ['4'],
    'e': ['3'],
    'i': ['1'],
    'o': ['0'],
    'l': ['1'],
    's': ['5'],
    't': ['7'],
}

DEFAULT_STANDARD_MAP: Dict[str, List[str]] = {
    'a': ['4', '@'],
    'b': ['8'],
    'e': ['3'],
    'g': ['6', '9'],
    'i': ['1', '!'],
    'l': ['1'],
    'o': ['0'],
    's': ['5', '$'],
    't': ['7'],
    'z': ['2'],
}

DEFAULT_ADVANCED_MAP: Dict[str, List[str]] = {
    'a': ['4', '@', '/\\', '∂'],
    'b': ['8', '|3', 'ß'],
    'c': ['(', '<', '©'],
    'd': ['|)', '|]', '∂'],
    'e': ['3', '€', 'ë'],
    'f': ['|=', 'ƒ', 'ph'],
    'g': ['6', '9', '&'],
    'h': ['#', '|-|', ']-['],
    'i': ['1', '!', '|'],
    'j': ['_|', ']', ';'],
    'k': ['|<', '|{', 'X'],
    'l': ['1', '|_', '£'],
    'm': ['|v|', '/\\/\\', '|\'|\'|'],
    'n': ['|\\|', '/\\/', '~'],
    'o': ['0', '()', '[]'],
    'p': ['|*', '|o', '¶'],
    'q': ['0_', '(', '9'],
    'r': ['|2', '®', 'I2'],
    's': ['5', '$', 'z'],
    't': ['7', '+', '-|-'],
    'u': ['|_|', 'µ', 'v'],
    'v': ['\\/', '|/', '\\\''],
    'w': ['\\/\\/', 'vv', '\\^/'],
    'x': ['><', ')(', '×'],
    'y': ['`/', '¥', 'j'],
    'z': ['2', '~/_', '7_'],
}

# 反向映射表（用于解码）
REVERSE_BASIC_MAP: Dict[str, str] = {
    '4': 'a', '@': 'a',
    '3': 'e',
    '1': 'i', '!': 'i',
    '0': 'o',
    '5': 's', '$': 's',
    '7': 't',
}

REVERSE_STANDARD_MAP: Dict[str, str] = {
    '4': 'a', '@': 'a',
    '8': 'b',
    '3': 'e',
    '6': 'g', '9': 'g',
    '1': 'i', '!': 'i',
    '0': 'o',
    '5': 's', '$': 's',
    '7': 't',
    '2': 'z',
}

REVERSE_ADVANCED_MAP: Dict[str, str] = {
    '4': 'a', '@': 'a', '/\\': 'a', '∂': 'a',
    '8': 'b', '|3': 'b', 'ß': 'b',
    '(': 'c', '<': 'c', '©': 'c',
    '|)': 'd', '|]': 'd', '∂': 'd',
    '3': 'e', '€': 'e', 'ë': 'e',
    '|=': 'f', 'ƒ': 'f', 'ph': 'f',
    '6': 'g', '9': 'g', '&': 'g',
    '#': 'h', '|-|': 'h', ']-[': 'h',
    '1': 'i', '!': 'i', '|': 'i',
    '_|': 'j', ']': 'j', ';': 'j',
    '|<': 'k', '|{': 'k', 'X': 'k',
    '|_': 'l', '£': 'l',
    '|v|': 'm', '/\\/\\': 'm', '|\'|\'|': 'm',
    '|\\|': 'n', '/\\/': 'n', '~': 'n',
    '0': 'o', '()': 'o', '[]': 'o',
    '|*': 'p', '|o': 'p', '¶': 'p',
    '0_': 'q', 'µ': 'u', 'v': 'u',
    '|2': 'r', '®': 'r', 'I2': 'r',
    '5': 's', '$': 's', 'z': 's',
    '7': 't', '+': 't', '-|-': 't',
    '|_|': 'u',
    '\\/': 'v', '|/': 'v', '\\\'': 'v',
    '\\/\\/': 'w', 'vv': 'w', '\\^/': 'w',
    '><': 'x', ')(': 'x', '×': 'x',
    '`/': 'y', '¥': 'y', 'j': 'y',
    '2': 'z', '~/_': 'z', '7_': 'z',
}


class LeetSpeakEncoder:
    """Leet Speak 编码器"""
    
    def __init__(
        self, 
        level: str = 'standard',
        custom_map: Optional[Dict[str, List[str]]] = None
    ):
        """
        初始化编码器
        
        Args:
            level: 转换级别 ('basic', 'standard', 'advanced')
            custom_map: 自定义映射表，会覆盖默认映射
        """
        self.level = level
        self._map = self._get_map(level)
        if custom_map:
            self._map.update(custom_map)
    
    def _get_map(self, level: str) -> Dict[str, List[str]]:
        """获取指定级别的映射表"""
        maps = {
            'basic': DEFAULT_BASIC_MAP,
            'standard': DEFAULT_STANDARD_MAP,
            'advanced': DEFAULT_ADVANCED_MAP,
        }
        return dict(maps.get(level, DEFAULT_STANDARD_MAP))
    
    def encode(
        self, 
        text: str, 
        randomize: bool = False,
        seed: Optional[int] = None
    ) -> str:
        """
        将文本编码为 Leet Speak
        
        Args:
            text: 要编码的文本
            randomize: 是否随机选择替换字符（同一字母可能有不同替换）
            seed: 随机种子（用于可重现的随机替换）
        
        Returns:
            编码后的 Leet Speak 文本
        """
        if seed is not None:
            import random
            random.seed(seed)
            randomize = True
        
        result = []
        for char in text:
            lower_char = char.lower()
            if lower_char in self._map:
                replacements = self._map[lower_char]
                if randomize:
                    import random
                    replacement = random.choice(replacements)
                else:
                    replacement = replacements[0]
                # 保留原始大小写风格
                if char.isupper() and len(replacement) == 1:
                    result.append(replacement.upper())
                else:
                    result.append(replacement)
            else:
                result.append(char)
        
        return ''.join(result)
    
    def encode_word_variants(self, word: str, max_variants: int = 10) -> List[str]:
        """
        生成单词的所有可能变体
        
        Args:
            word: 要编码的单词
            max_variants: 最大变体数量
        
        Returns:
            变体列表
        """
        import itertools
        import random
        
        word = word.lower()
        options = []
        
        for char in word:
            if char in self._map:
                options.append(self._map[char])
            else:
                options.append([char])
        
        # 计算总变体数
        total = 1
        for opt in options:
            total *= len(opt)
        
        if total <= max_variants:
            variants = [''.join(combo) for combo in itertools.product(*options)]
        else:
            # 随机采样
            variants = set()
            for _ in range(max_variants):
                combo = [random.choice(opt) for opt in options]
                variants.add(''.join(combo))
            variants = list(variants)
        
        return variants[:max_variants]


class LeetSpeakDecoder:
    """Leet Speak 解码器"""
    
    def __init__(self, level: str = 'standard'):
        """
        初始化解码器
        
        Args:
            level: 解码级别 ('basic', 'standard', 'advanced')
        """
        self.level = level
        self._reverse_map = self._get_reverse_map(level)
    
    def _get_reverse_map(self, level: str) -> Dict[str, str]:
        """获取指定级别的反向映射表"""
        maps = {
            'basic': REVERSE_BASIC_MAP,
            'standard': REVERSE_STANDARD_MAP,
            'advanced': REVERSE_ADVANCED_MAP,
        }
        return maps.get(level, REVERSE_STANDARD_MAP)
    
    def decode(self, text: str) -> str:
        """
        将 Leet Speak 解码为普通文本
        
        Args:
            text: Leet Speak 文本
        
        Returns:
            解码后的普通文本
        """
        result = []
        i = 0
        while i < len(text):
            char = text[i]
            matched = False
            
            # 尝试最长匹配（优先匹配多字符替换）
            for length in range(5, 0, -1):
                if i + length <= len(text):
                    substr = text[i:i + length]
                    if substr in self._reverse_map:
                        result.append(self._reverse_map[substr])
                        i += length
                        matched = True
                        break
            
            if not matched:
                # 单字符匹配
                if char in self._reverse_map:
                    result.append(self._reverse_map[char])
                else:
                    result.append(char)
                i += 1
        
        return ''.join(result)
    
    def decode_all_possible(self, text: str) -> List[str]:
        """
        解码所有可能的结果（处理歧义字符）
        
        Args:
            text: Leet Speak 文本
        
        Returns:
            所有可能的解码结果列表
        """
        def decode_recursive(pos: int) -> List[str]:
            if pos >= len(text):
                return ['']
            
            results = []
            
            # 尝试最长匹配
            for length in range(5, 0, -1):
                if pos + length <= len(text):
                    substr = text[pos:pos + length]
                    if substr in self._reverse_map:
                        decoded_char = self._reverse_map[substr]
                        for suffix in decode_recursive(pos + length):
                            results.append(decoded_char + suffix)
            
            # 单字符处理
            char = text[pos]
            if char in self._reverse_map:
                decoded_char = self._reverse_map[char]
                for suffix in decode_recursive(pos + 1):
                    results.append(decoded_char + suffix)
            else:
                for suffix in decode_recursive(pos + 1):
                    results.append(char + suffix)
            
            return results if results else ['']
        
        all_results = decode_recursive(0)
        # 去重并限制数量
        return list(set(all_results))[:20]


def encode(
    text: str, 
    level: str = 'standard', 
    randomize: bool = False,
    seed: Optional[int] = None
) -> str:
    """
    快捷编码函数
    
    Args:
        text: 要编码的文本
        level: 转换级别 ('basic', 'standard', 'advanced')
        randomize: 是否随机选择替换字符
        seed: 随机种子
    
    Returns:
        编码后的 Leet Speak 文本
    """
    encoder = LeetSpeakEncoder(level=level)
    return encoder.encode(text, randomize=randomize, seed=seed)


def decode(text: str, level: str = 'standard') -> str:
    """
    快捷解码函数
    
    Args:
        text: Leet Speak 文本
        level: 解码级别
    
    Returns:
        解码后的普通文本
    """
    decoder = LeetSpeakDecoder(level=level)
    return decoder.decode(text)


def is_leet(text: str, threshold: float = 0.3) -> bool:
    """
    检测文本是否可能是 Leet Speak
    
    Args:
        text: 要检测的文本
        threshold: Leet 字符比例阈值
    
    Returns:
        是否可能是 Leet Speak
    """
    if not text:
        return False
    
    leet_chars = set('0123456789!@#$%^&*()_+-={}[]|\\:";\'<>?,./~`')
    leet_count = sum(1 for c in text if c in leet_chars)
    
    # 计算比例
    ratio = leet_count / len(text)
    
    # 同时检查是否有足够的数字替换
    digit_count = sum(1 for c in text if c.isdigit())
    letter_count = sum(1 for c in text if c.isalpha())
    
    # 如果数字比字母多，或者 leet 字符比例高于阈值
    return ratio >= threshold or (digit_count > letter_count * 0.5)


def detect_level(text: str) -> str:
    """
    检测 Leet Speak 的级别
    
    Args:
        text: Leet Speak 文本
    
    Returns:
        检测到的级别 ('basic', 'standard', 'advanced', 'unknown')
    """
    advanced_chars = set('/\\|∂ß()[]€#|-|_|µ><¥')
    standard_chars = set('@8!')
    basic_chars = set('431057')
    
    has_advanced = any(c in text for c in advanced_chars)
    has_standard = any(c in text for c in standard_chars)
    has_basic = any(c in text for c in basic_chars)
    
    if has_advanced:
        return 'advanced'
    elif has_standard:
        return 'standard'
    elif has_basic:
        return 'basic'
    else:
        return 'unknown'


class LeetSpeakGenerator:
    """Leet Speak 变体生成器"""
    
    def __init__(self):
        pass
    
    def generate_username_variants(self, username: str, count: int = 5) -> List[str]:
        """
        生成用户名变体
        
        Args:
            username: 原始用户名
            count: 生成数量
        
        Returns:
            变体列表
        """
        variants = set()
        
        # 不同级别的变体
        for level in ['basic', 'standard', 'advanced']:
            encoder = LeetSpeakEncoder(level=level)
            variants.add(encoder.encode(username))
        
        # 随机变体
        for seed in range(count):
            encoder = LeetSpeakEncoder(level='standard')
            variants.add(encoder.encode(username, randomize=True, seed=seed))
        
        return list(variants)[:count]
    
    def generate_password_hints(self, word: str) -> List[Tuple[str, str]]:
        """
        生成密码提示变体
        
        Args:
            word: 原始单词
        
        Returns:
            (变体, 说明) 元组列表
        """
        results = []
        
        # 不同级别
        levels = [
            ('basic', '基础替换'),
            ('standard', '标准替换'),
            ('advanced', '高级替换'),
        ]
        
        for level, desc in levels:
            encoder = LeetSpeakEncoder(level=level)
            encoded = encoder.encode(word)
            results.append((encoded, f"{desc}: {word}"))
        
        return results


def create_custom_encoder(
    custom_map: Dict[str, List[str]],
    base_level: str = 'basic'
) -> LeetSpeakEncoder:
    """
    创建自定义编码器
    
    Args:
        custom_map: 自定义映射 {原始字符: [替换字符列表]}
        base_level: 基础映射级别
    
    Returns:
        配置好的编码器
    """
    return LeetSpeakEncoder(level=base_level, custom_map=custom_map)


# 便捷函数
def to_leet(text: str, level: str = 'standard') -> str:
    """转换为 Leet Speak（encode 的别名）"""
    return encode(text, level=level)


def from_leet(text: str, level: str = 'standard') -> str:
    """从 Leet Speak 转换回普通文本（decode 的别名）"""
    return decode(text, level=level)


if __name__ == '__main__':
    # 简单演示
    print("=== Leet Speak Utils Demo ===\n")
    
    text = "Hello World"
    
    print(f"原文: {text}")
    print(f"基础转换: {encode(text, 'basic')}")
    print(f"标准转换: {encode(text, 'standard')}")
    print(f"高级转换: {encode(text, 'advanced')}")
    
    leet_text = "H3ll0 W0rld"
    print(f"\nLeet 文本: {leet_text}")
    print(f"解码: {decode(leet_text)}")
    
    print(f"\n是否为 Leet: {is_leet(leet_text)}")
    print(f"检测级别: {detect_level(leet_text)}")