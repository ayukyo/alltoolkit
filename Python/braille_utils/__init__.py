"""
Braille Utilities - 盲文编码/解码工具

提供文本与盲文的相互转换功能，支持：
- 英文字母、数字、标点符号
- Unicode 盲文字符与点位模式互转
- Grade 1 和 Grade 2 编码
- 盲文矩阵可视化
"""

from .mod import (
    BrailleGrade,
    BrailleCell,
    BrailleEncoder,
    BrailleUtils,
    text_to_braille,
    braille_to_text,
    dots_to_unicode,
    unicode_to_dots,
    display_braille,
    ENGLISH_LETTERS,
    NUMBERS,
    PUNCTUATION,
    GRADE2_ABBREVIATIONS,
    MUSIC_BRAILLE,
    NUMBER_SIGN,
    CAPITAL_SIGN,
)

__version__ = '1.0.0'
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