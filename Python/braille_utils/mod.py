"""
Braille Utilities - 盲文编码/解码工具

功能：
- 文本与盲文点字互转
- 支持多语言（英文、数字、基本标点）
- 盲文 Unicode 与点阵表示互转
- 盲文等级支持（Grade 1 / Grade 2 缩写）
- 音乐盲文基础支持

盲文基础：
- 盲文单元格由 6 个点组成（2列×3行）
- 点位编号：左列从上到下 1-2-3，右列从上到下 4-5-6
- Unicode 盲文字符范围: U+2800 - U+283F
"""

from typing import Dict, List, Tuple, Optional, Set
from enum import Enum


class BrailleGrade(Enum):
    """盲文等级"""
    GRADE_1 = 1  # 逐字母编码
    GRADE_2 = 2  # 包含缩写


class BrailleCell:
    """盲文单元格类"""
    
    def __init__(self, dots: Set[int] = None):
        """
        初始化盲文单元格
        
        Args:
            dots: 点亮的点位集合，范围 1-6
        """
        self.dots = dots if dots else set()
        self._validate_dots()
    
    def _validate_dots(self):
        """验证点位有效性"""
        for dot in self.dots:
            if dot < 1 or dot > 6:
                raise ValueError(f"点位必须在 1-6 之间，得到: {dot}")
    
    def to_unicode(self) -> str:
        """转换为 Unicode 盲文字符"""
        # Unicode 盲文从 U+2800 开始
        # 每个点位对应一个二进制位
        # 点 1 -> bit 0, 点 2 -> bit 1, ..., 点 6 -> bit 5
        code = 0x2800
        bit_mapping = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5}
        for dot in self.dots:
            code += (1 << bit_mapping[dot])
        return chr(code)
    
    @classmethod
    def from_unicode(cls, char: str) -> 'BrailleCell':
        """从 Unicode 盲文字符创建单元格"""
        if len(char) != 1:
            raise ValueError("必须为单个字符")
        
        code = ord(char)
        if code < 0x2800 or code > 0x28FF:
            raise ValueError(f"不是有效的盲文字符: U+{code:04X}")
        
        dots = set()
        bit_mapping = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6}
        
        for bit, dot in bit_mapping.items():
            if code & (1 << bit):
                dots.add(dot)
        
        return cls(dots)
    
    def to_dots_pattern(self) -> str:
        """转换为点位模式字符串，如 '⠓' -> '125'"""
        if not self.dots:
            return ''
        return ''.join(str(d) for d in sorted(self.dots))
    
    @classmethod
    def from_dots_pattern(cls, pattern: str) -> 'BrailleCell':
        """从点位模式创建，如 '125' -> '⠓'"""
        if not pattern:
            return cls()
        dots = set(int(c) for c in pattern if c.isdigit())
        return cls(dots)
    
    def to_binary_matrix(self) -> List[List[int]]:
        """转换为 2x3 二进制矩阵"""
        matrix = [[0, 0], [0, 0], [0, 0]]
        positions = {
            1: (0, 0), 2: (1, 0), 3: (2, 0),
            4: (0, 1), 5: (1, 1), 6: (2, 1)
        }
        for dot in self.dots:
            row, col = positions[dot]
            matrix[row][col] = 1
        return matrix
    
    def __repr__(self):
        return f"BrailleCell({self.to_dots_pattern() or 'empty'})"
    
    def __str__(self):
        return self.to_unicode()
    
    def __eq__(self, other):
        if isinstance(other, BrailleCell):
            return self.dots == other.dots
        return False
    
    def __hash__(self):
        return hash(frozenset(self.dots))


# 英文字母盲文映射（Grade 1）
ENGLISH_LETTERS: Dict[str, str] = {
    'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑',
    'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚',
    'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕',
    'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞',
    'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽',
    'z': '⠵'
}

# 数字盲文映射（使用字母符号加数字标识）
NUMBERS: Dict[str, str] = {
    '1': '⠁', '2': '⠃', '3': '⠉', '4': '⠙', '5': '⠑',
    '6': '⠋', '7': '⠛', '8': '⠓', '9': '⠊', '0': '⠚'
}

# 标点符号盲文映射（标准英语盲文标点）
# 参考：https://www.brailleauthority.org/
PUNCTUATION: Dict[str, str] = {
    '.': '⠲',      # 句号
    ',': '⠂',      # 逗号
    ';': '⠆',      # 分号
    ':': '⠒',      # 冒号
    '!': '⠖',      # 感叹号
    '?': '⠦',      # 问号
    "'": '⠄',      # 撇号
    '"': '⠶',      # 引号 (开/闭相同)
    '(': '⠶',      # 左括号
    ')': '⠶',      # 右括号
    '-': '⠤',      # 连字符
    '/': '⠌',      # 斜杠
    '@': '⠜',      # at 符号
    '#': '⠼',      # 数字标识符
    '&': '⠯',      # 和号
    '*': '⠡',      # 星号
    '=': '⠶',      # 等号
    '+': '⠖',      # 加号
    '_': '⠤',      # 下划线
}

# 解码时使用的反向映射（解决冲突，选择最常用的符号）
# 例如 '⠖' 可以解码为 '!' 或 '+'，选择 '!' 作为默认

# 特殊符号标识符
NUMBER_SIGN = '⠼'  # 数字标识符
CAPITAL_SIGN = '⠠'  # 大写字母标识符
LETTER_SIGN = '⠰'  # 字母标识符（数字后跟字母时使用）
SPACE = ' '

# Grade 2 缩写映射
GRADE2_ABBREVIATIONS: Dict[str, str] = {
    'and': '⠯',
    'for': '⠿',
    'of': '⠷',
    'the': '⠮',
    'with': '⠺',
    'ch': '⠡',
    'gh': '⠣',
    'sh': '⠩',
    'th': '⠹',
    'wh': '⠱',
    'ed': '⠫',
    'er': '⠻',
    'ou': '⠳',
    'ow': '⠪',
    'st': '⠌',
    'ing': '⠬',
    'ble': '⠼',
    'ar': '⠜',
    'en': '⠰⠝',
    'in': '⠰⠔',
}


class BrailleEncoder:
    """盲文编码器"""
    
    def __init__(self, grade: BrailleGrade = BrailleGrade.GRADE_1):
        """
        初始化编码器
        
        Args:
            grade: 盲文等级
        """
        self.grade = grade
        self._build_reverse_maps()
    
    def _build_reverse_maps(self):
        """构建反向映射表"""
        self.reverse_letters = {v: k for k, v in ENGLISH_LETTERS.items()}
        self.reverse_numbers = {v: k for k, v in NUMBERS.items()}
        self.reverse_punctuation = {v: k for k, v in PUNCTUATION.items()}
    
    def encode(self, text: str) -> str:
        """
        将文本编码为盲文
        
        Args:
            text: 要编码的文本
            
        Returns:
            盲文字符串
        """
        result = []
        in_number = False
        i = 0
        
        while i < len(text):
            char = text[i]
            
            # 处理空格
            if char == ' ':
                result.append(SPACE)
                in_number = False
                i += 1
                continue
            
            # 处理数字
            if char.isdigit():
                if not in_number:
                    result.append(NUMBER_SIGN)
                    in_number = True
                result.append(NUMBERS[char])
                i += 1
                continue
            
            # 重置数字状态
            if in_number and char.isalpha():
                in_number = False
            
            # 处理大写字母
            if char.isupper():
                result.append(CAPITAL_SIGN)
                char = char.lower()
            
            # 处理字母
            if char in ENGLISH_LETTERS:
                # 尝试 Grade 2 缩写
                if self.grade == BrailleGrade.GRADE_2:
                    matched = False
                    # 检查更长的匹配
                    for length in [5, 4, 3, 2]:
                        if i + length <= len(text):
                            substr = text[i:i+length].lower()
                            if substr in GRADE2_ABBREVIATIONS:
                                result.append(GRADE2_ABBREVIATIONS[substr])
                                i += length
                                matched = True
                                break
                    if matched:
                        continue
                
                result.append(ENGLISH_LETTERS[char])
                i += 1
                continue
            
            # 处理标点符号
            if char in PUNCTUATION:
                result.append(PUNCTUATION[char])
                i += 1
                continue
            
            # 未知字符，保留原样
            result.append(char)
            i += 1
        
        return ''.join(result)
    
    def decode(self, braille: str) -> str:
        """
        将盲文解码为文本
        
        Args:
            braille: 盲文字符串
            
        Returns:
            解码后的文本
        """
        result = []
        i = 0
        in_number = False
        next_upper = False
        
        while i < len(braille):
            char = braille[i]
            
            # 处理空格
            if char == ' ':
                result.append(' ')
                in_number = False
                i += 1
                continue
            
            # 处理数字标识符
            if char == NUMBER_SIGN:
                in_number = True
                i += 1
                continue
            
            # 处理大写标识符
            if char == CAPITAL_SIGN:
                next_upper = True
                i += 1
                continue
            
            # 处理数字
            if in_number and char in self.reverse_numbers:
                result.append(self.reverse_numbers[char])
                i += 1
                continue
            
            # 重置数字状态
            if in_number:
                in_number = False
            
            # 处理字母
            if char in self.reverse_letters:
                letter = self.reverse_letters[char]
                if next_upper:
                    letter = letter.upper()
                    next_upper = False
                result.append(letter)
                i += 1
                continue
            
            # 处理标点符号
            if char in self.reverse_punctuation:
                result.append(self.reverse_punctuation[char])
                i += 1
                continue
            
            # 未知字符，保留原样
            result.append(char)
            next_upper = False
            i += 1
        
        return ''.join(result)


class BrailleUtils:
    """盲文工具类"""
    
    @staticmethod
    def text_to_braille(text: str, grade: BrailleGrade = BrailleGrade.GRADE_1) -> str:
        """
        文本转盲文
        
        Args:
            text: 要转换的文本
            grade: 盲文等级
            
        Returns:
            盲文字符串
        """
        encoder = BrailleEncoder(grade)
        return encoder.encode(text)
    
    @staticmethod
    def braille_to_text(braille: str) -> str:
        """
        盲文转文本
        
        Args:
            braille: 盲文字符串
            
        Returns:
            解码后的文本
        """
        encoder = BrailleEncoder()
        return encoder.decode(braille)
    
    @staticmethod
    def dots_to_unicode(dots_pattern: str) -> str:
        """
        点位模式转 Unicode
        
        Args:
            dots_pattern: 点位模式，如 '125'
            
        Returns:
            盲文字符
        """
        cell = BrailleCell.from_dots_pattern(dots_pattern)
        return cell.to_unicode()
    
    @staticmethod
    def unicode_to_dots(char: str) -> str:
        """
        Unicode 盲文转点位模式
        
        Args:
            char: 盲文字符
            
        Returns:
            点位模式字符串
        """
        cell = BrailleCell.from_unicode(char)
        return cell.to_dots_pattern()
    
    @staticmethod
    def is_braille_char(char: str) -> bool:
        """
        检查是否为盲文字符
        
        Args:
            char: 要检查的字符
            
        Returns:
            是否为盲文字符
        """
        if len(char) != 1:
            return False
        code = ord(char)
        return 0x2800 <= code <= 0x28FF
    
    @staticmethod
    def get_braille_cells(braille: str) -> List[BrailleCell]:
        """
        将盲文字符串转换为单元格列表
        
        Args:
            braille: 盲文字符串
            
        Returns:
            单元格列表
        """
        return [BrailleCell.from_unicode(c) for c in braille if BrailleUtils.is_braille_char(c)]
    
    @staticmethod
    def display_braille_matrix(char: str, filled: str = '●', empty: str = '○') -> str:
        """
        以矩阵形式显示盲文字符
        
        Args:
            char: 盲文字符
            filled: 填充字符
            empty: 空字符
            
        Returns:
            矩阵形式的字符串
        """
        if not BrailleUtils.is_braille_char(char):
            return ''
        
        cell = BrailleCell.from_unicode(char)
        matrix = cell.to_binary_matrix()
        
        lines = []
        for row in matrix:
            lines.append(' '.join(filled if v else empty for v in row))
        
        return '\n'.join(lines)
    
    @staticmethod
    def create_empty_cell() -> BrailleCell:
        """创建空白盲文单元格"""
        return BrailleCell()
    
    @staticmethod
    def create_full_cell() -> BrailleCell:
        """创建满点盲文单元格（所有6个点）"""
        return BrailleCell({1, 2, 3, 4, 5, 6})
    
    @staticmethod
    def get_all_braille_chars() -> List[str]:
        """获取所有可能的盲文字符（64个）"""
        chars = []
        for code in range(0x2800, 0x2840):
            chars.append(chr(code))
        return chars
    
    @staticmethod
    def count_braille_dots(char: str) -> int:
        """
        统计盲文字符的点数
        
        Args:
            char: 盲文字符
            
        Returns:
            点数
        """
        if not BrailleUtils.is_braille_char(char):
            return 0
        cell = BrailleCell.from_unicode(char)
        return len(cell.dots)
    
    @staticmethod
    def invert_braille(char: str) -> str:
        """
        反转盲文字符（空点变实点，实点变空点）
        
        Args:
            char: 盲文字符
            
        Returns:
            反转后的盲文字符
        """
        if not BrailleUtils.is_braille_char(char):
            return char
        
        cell = BrailleCell.from_unicode(char)
        all_dots = {1, 2, 3, 4, 5, 6}
        inverted = all_dots - cell.dots
        return BrailleCell(inverted).to_unicode()


# 音乐盲文映射（基础）
MUSIC_BRAILLE: Dict[str, str] = {
    'C': '⠉',  # Do
    'D': '⠙',  # Re
    'E': '⠑',  # Mi
    'F': '⠋',  # Fa
    'G': '⠛',  # Sol
    'A': '⠁',  # La
    'B': '⠃',  # Si
    'whole': '⠽',  # 全音符
    'half': '⠓',   # 二分音符
    'quarter': '⠟', # 四分音符
    'eighth': '⠱',  # 八分音符
    'rest': '⠄',    # 休止符
}


def text_to_braille(text: str, grade: BrailleGrade = BrailleGrade.GRADE_1) -> str:
    """文本转盲文（便捷函数）"""
    return BrailleUtils.text_to_braille(text, grade)


def braille_to_text(braille: str) -> str:
    """盲文转文本（便捷函数）"""
    return BrailleUtils.braille_to_text(braille)


def dots_to_unicode(dots_pattern: str) -> str:
    """点位转 Unicode（便捷函数）"""
    return BrailleUtils.dots_to_unicode(dots_pattern)


def unicode_to_dots(char: str) -> str:
    """Unicode 转点位（便捷函数）"""
    return BrailleUtils.unicode_to_dots(char)


def display_braille(char: str) -> str:
    """显示盲文矩阵（便捷函数）"""
    return BrailleUtils.display_braille_matrix(char)


# 导出
__all__ = [
    'BrailleGrade',
    'BrailleCell',
    'BrailleEncoder',
    'BrailleUtils',
    'text_to_braille',
    'braille_to_text',
    'dots_to_unicode',
    'unicode_to_dots',
    'display_braille',
    'ENGLISH_LETTERS',
    'NUMBERS',
    'PUNCTUATION',
    'GRADE2_ABBREVIATIONS',
    'MUSIC_BRAILLE',
    'NUMBER_SIGN',
    'CAPITAL_SIGN',
]