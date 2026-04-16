"""
nanoid_utils - 轻量级唯一ID生成工具

NanoID 是一个小巧、安全、URL友好的唯一字符串ID生成器。
- 默认长度21字符
- 使用加密安全的随机数生成器
- URL安全字符集: A-Za-z0-9_-
- 零外部依赖，纯Python实现

特性:
- generate(): 生成标准NanoID
- generate_custom(): 自定义长度和字符集
- generate_number(): 纯数字ID
- generate_lowercase(): 小写字母+数字ID
- generate_alphabet(): 纯字母ID
- validate(): 验证ID格式
- batch(): 批量生成ID
"""

import secrets
import string
from typing import Optional, List


# 默认URL安全字符集
DEFAULT_ALPHABET = '_-0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

# 预定义字符集
ALPHABET_LOWERCASE = 'abcdefghijklmnopqrstuvwxyz'
ALPHABET_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALPHABET_ALPHA = ALPHABET_LOWERCASE + ALPHABET_UPPERCASE
ALPHABET_ALPHANUMERIC = ALPHABET_ALPHA + string.digits
ALPHABET_NUMBERS = string.digits
ALPHABET_NO_LOOKALIKES = '_-23456789abcdefghjkmnpqrstvwxyzABCDEFGHJKMNPQRSTVWXYZ'  # 移除易混淆字符: 0O1lI
ALPHABET_LOWERCASE_ALPHANUMERIC = ALPHABET_LOWERCASE + string.digits


def _random_bytes(size: int) -> bytes:
    """生成加密安全的随机字节"""
    return secrets.token_bytes(size)


def _generate_with_alphabet(size: int, alphabet: str) -> str:
    """使用指定字符集生成ID (unbiased算法)"""
    if not alphabet:
        raise ValueError("字符集不能为空")
    
    if size <= 0:
        raise ValueError("ID长度必须大于0")
    
    alphabet_len = len(alphabet)
    
    # 计算避免偏差所需的掩码
    # 找到 >= alphabet_len 的最小 2^n - 1
    mask = 1
    while mask < alphabet_len:
        mask = (mask << 1) | 1
    
    # 计算每批次需要多少随机字节
    # 每个字节8位，mask可能需要更多位
    step = max(1, (mask.bit_length() + 7) // 8)
    
    result = []
    while len(result) < size:
        random_bytes = _random_bytes(step * max(1, size // step + 1))
        
        for byte in random_bytes:
            # 使用掩码获取均匀分布的索引
            idx = byte & mask
            if idx < alphabet_len:
                result.append(alphabet[idx])
                if len(result) >= size:
                    break
    
    return ''.join(result)


def generate(size: int = 21) -> str:
    """
    生成标准NanoID
    
    Args:
        size: ID长度，默认21字符
        
    Returns:
        URL安全的唯一ID字符串
        
    Example:
        >>> nanoid = generate()
        >>> len(nanoid)
        21
        >>> nanoid2 = generate(10)
        >>> len(nanoid2)
        10
    """
    return _generate_with_alphabet(size, DEFAULT_ALPHABET)


def generate_custom(size: int, alphabet: str) -> str:
    """
    使用自定义字符集生成ID
    
    Args:
        size: ID长度
        alphabet: 自定义字符集
        
    Returns:
        基于自定义字符集的唯一ID
        
    Example:
        >>> # 使用十六进制字符
        >>> nanoid = generate_custom(16, '0123456789abcdef')
        >>> all(c in '0123456789abcdef' for c in nanoid)
        True
    """
    return _generate_with_alphabet(size, alphabet)


def generate_number(size: int = 16) -> str:
    """
    生成纯数字ID
    
    Args:
        size: ID长度，默认16
        
    Returns:
        纯数字字符串
        
    Example:
        >>> nanoid = generate_number()
        >>> len(nanoid)
        16
        >>> nanoid.isdigit()
        True
    """
    return _generate_with_alphabet(size, ALPHABET_NUMBERS)


def generate_lowercase(size: int = 21) -> str:
    """
    生成小写字母+数字ID
    
    Args:
        size: ID长度，默认21
        
    Returns:
        小写字母和数字组成的字符串
        
    Example:
        >>> nanoid = generate_lowercase()
        >>> nanoid.islower() or nanoid.isdigit()
        True
    """
    return _generate_with_alphabet(size, ALPHABET_LOWERCASE_ALPHANUMERIC)


def generate_alphabet(size: int = 21) -> str:
    """
    生成纯字母ID (大小写混合)
    
    Args:
        size: ID长度，默认21
        
    Returns:
        纯字母字符串 (A-Za-z)
        
    Example:
        >>> nanoid = generate_alphabet()
        >>> nanoid.isalpha()
        True
    """
    return _generate_with_alphabet(size, ALPHABET_ALPHA)


def generate_no_lookalikes(size: int = 21) -> str:
    """
    生成无易混淆字符的ID
    移除了 l, 1, I, O, 0 等容易混淆的字符
    
    Args:
        size: ID长度，默认21
        
    Returns:
        无易混淆字符的URL安全ID
        
    Example:
        >>> nanoid = generate_no_lookalikes()
        >>> # 不包含 l, 1, I, O, 0
        >>> 'l' not in nanoid and 'I' not in nanoid and 'O' not in nanoid
        True
    """
    return _generate_with_alphabet(size, ALPHABET_NO_LOOKALIKES)


def batch(count: int, size: int = 21) -> List[str]:
    """
    批量生成NanoID
    
    Args:
        count: 生成数量
        size: 每个ID的长度
        
    Returns:
        ID列表
        
    Example:
        >>> ids = batch(100, 10)
        >>> len(ids)
        100
        >>> all(len(id_) == 10 for id_ in ids)
        True
    """
    if count <= 0:
        return []
    return [generate(size) for _ in range(count)]


def validate(nanoid: str, 
             size: Optional[int] = None, 
             alphabet: Optional[str] = None) -> bool:
    """
    验证NanoID格式
    
    Args:
        nanoid: 要验证的ID字符串
        size: 期望的长度，None表示不检查长度
        alphabet: 允许的字符集，None表示使用默认字符集
        
    Returns:
        True 如果格式有效，否则 False
        
    Example:
        >>> validate("V1StGXR8_Z5jdHi6B-myT")
        True
        >>> validate("invalid@id!", alphabet=DEFAULT_ALPHABET)
        False
        >>> validate("V1StGXR8_Z5jdHi6B-myT", size=10)
        False
    """
    if not isinstance(nanoid, str):
        return False
    
    if not nanoid:
        return False
    
    if size is not None and len(nanoid) != size:
        return False
    
    allowed_chars = alphabet if alphabet is not None else DEFAULT_ALPHABET
    
    return all(c in allowed_chars for c in nanoid)


def is_unique(nanoid: str, existing_ids: set) -> bool:
    """
    检查ID在现有集合中是否唯一
    
    Args:
        nanoid: 要检查的ID
        existing_ids: 已存在的ID集合
        
    Returns:
        True 如果ID唯一，否则 False
        
    Example:
        >>> existing = {"abc123", "xyz789"}
        >>> is_unique("new_id", existing)
        True
        >>> is_unique("abc123", existing)
        False
    """
    return nanoid not in existing_ids


def generate_unique(size: int = 21, 
                    existing_ids: Optional[set] = None, 
                    max_attempts: int = 100) -> str:
    """
    生成确保唯一的NanoID (在给定集合中不重复)
    
    Args:
        size: ID长度
        existing_ids: 已存在的ID集合
        max_attempts: 最大尝试次数
        
    Returns:
        唯一的NanoID
        
    Raises:
        RuntimeError: 如果在最大尝试次数内无法生成唯一ID
        
    Example:
        >>> existing = {"abc123", "xyz789"}
        >>> new_id = generate_unique(21, existing)
        >>> new_id not in existing
        True
    """
    if existing_ids is None:
        existing_ids = set()
    
    for _ in range(max_attempts):
        nanoid = generate(size)
        if nanoid not in existing_ids:
            return nanoid
    
    raise RuntimeError(f"无法在 {max_attempts} 次尝试内生成唯一ID")


def estimate_collision_probability(size: int, alphabet_len: int, count: int) -> float:
    """
    估算碰撞概率 (生日悖论)
    
    Args:
        size: ID长度
        alphabet_len: 字符集大小
        count: 生成的ID数量
        
    Returns:
        碰撞概率 (0-1之间)
        
    Example:
        >>> # 生成100万个21字符的标准NanoID，碰撞概率极低
        >>> prob = estimate_collision_probability(21, 64, 1000000)
        >>> prob < 0.001
        True
    """
    import math
    
    if size <= 0 or alphabet_len <= 0 or count <= 0:
        return 0.0
    
    # 总可能性
    total = alphabet_len ** size
    
    # 使用近似公式: p ≈ 1 - e^(-n²/(2*N))
    if total == 0:
        return 1.0
    
    try:
        probability = 1 - math.exp(-(count ** 2) / (2 * total))
    except OverflowError:
        probability = 0.0
    
    return probability


# 便捷别名
nanoid = generate