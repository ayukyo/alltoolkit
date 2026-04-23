"""
SOUNDEX 语音编码工具模块

提供标准 SOUNDEX 编码、相似度计算、姓名匹配等功能。
"""

from .mod import (
    SoundexEncoder,
    SoundexRefinedEncoder,
    SoundexSQL,
    encode,
    similarity,
    matches,
    find_similar,
    group_by_sound,
    COMMON_NAMES,
    get_common_code,
)

__all__ = [
    'SoundexEncoder',
    'SoundexRefinedEncoder',
    'SoundexSQL',
    'encode',
    'similarity',
    'matches',
    'find_similar',
    'group_by_sound',
    'COMMON_NAMES',
    'get_common_code',
]