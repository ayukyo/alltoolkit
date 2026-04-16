"""
nanoid_utils - 轻量级唯一ID生成工具

使用示例:
    from nanoid_utils import generate, generate_number
    
    # 生成标准NanoID
    id1 = generate()
    
    # 生成纯数字ID
    id2 = generate_number(16)
"""

from .mod import (
    generate,
    generate_custom,
    generate_number,
    generate_lowercase,
    generate_alphabet,
    generate_no_lookalikes,
    batch,
    validate,
    is_unique,
    generate_unique,
    estimate_collision_probability,
    nanoid,
    DEFAULT_ALPHABET,
    ALPHABET_NUMBERS,
    ALPHABET_LOWERCASE_ALPHANUMERIC,
    ALPHABET_ALPHA,
    ALPHABET_NO_LOOKALIKES,
)

__all__ = [
    'generate',
    'generate_custom',
    'generate_number',
    'generate_lowercase',
    'generate_alphabet',
    'generate_no_lookalikes',
    'batch',
    'validate',
    'is_unique',
    'generate_unique',
    'estimate_collision_probability',
    'nanoid',
    'DEFAULT_ALPHABET',
    'ALPHABET_NUMBERS',
    'ALPHABET_LOWERCASE_ALPHANUMERIC',
    'ALPHABET_ALPHA',
    'ALPHABET_NO_LOOKALIKES',
]

__version__ = '1.0.0'