"""
Roman Numeral Utils - 罗马数字转换工具

零依赖的罗马数字转换库，支持：
- 阿拉伯数字转罗马数字
- 罗马数字转阿拉伯数字
- 罗马数字验证
- 批量转换
- 范围限制检查

Author: AllToolkit
License: MIT
"""

from typing import Union, List, Tuple, Optional


# 罗马数字基础映射
ROMAN_VALUES = {
    'I': 1, 'V': 5, 'X': 10, 'L': 50,
    'C': 100, 'D': 500, 'M': 1000
}

# 标准转换表（从大到小）
ROMAN_SYMBOLS = [
    (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
    (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
    (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'),
    (1, 'I')
]

# 支持的范围
MIN_VALUE = 1
MAX_VALUE = 3999


class RomanNumeralError(Exception):
    """罗马数字相关错误的基类"""
    pass


class InvalidRomanError(RomanNumeralError):
    """无效的罗马数字格式"""
    pass


class OutOfRangeError(RomanNumeralError):
    """数值超出支持范围"""
    pass


def to_roman(num: int, strict: bool = True) -> str:
    """
    将阿拉伯数字转换为罗马数字
    
    Args:
        num: 要转换的整数 (1-3999)
        strict: 是否严格检查范围，默认True
    
    Returns:
        罗马数字字符串
    
    Raises:
        OutOfRangeError: 数值超出范围
        TypeError: 输入不是整数
    
    Examples:
        >>> to_roman(1)
        'I'
        >>> to_roman(2024)
        'MMXXIV'
        >>> to_roman(3999)
        'MMMCMXCIX'
    """
    if not isinstance(num, int):
        raise TypeError(f"期望整数，得到 {type(num).__name__}")
    
    if strict and (num < MIN_VALUE or num > MAX_VALUE):
        raise OutOfRangeError(
            f"数值 {num} 超出支持范围 ({MIN_VALUE}-{MAX_VALUE})"
        )
    
    if num <= 0:
        raise OutOfRangeError(f"数值必须大于0，得到 {num}")
    
    result = []
    remaining = num
    
    for value, symbol in ROMAN_SYMBOLS:
        count, remaining = divmod(remaining, value)
        result.append(symbol * count)
        if remaining == 0:
            break
    
    return ''.join(result)


def from_roman(roman: str, strict: bool = True) -> int:
    """
    将罗马数字转换为阿拉伯数字
    
    Args:
        roman: 罗马数字字符串
        strict: 是否严格验证格式，默认True
    
    Returns:
        整数值
    
    Raises:
        InvalidRomanError: 无效的罗马数字格式
        TypeError: 输入不是字符串
    
    Examples:
        >>> from_roman('I')
        1
        >>> from_roman('MMXXIV')
        2024
        >>> from_roman('MMMCMXCIX')
        3999
    """
    if not isinstance(roman, str):
        raise TypeError(f"期望字符串，得到 {type(roman).__name__}")
    
    if not roman:
        raise InvalidRomanError("空字符串不是有效的罗马数字")
    
    roman = roman.upper().strip()
    
    if strict and not is_valid_roman(roman):
        raise InvalidRomanError(f"'{roman}' 不是有效的罗马数字")
    
    total = 0
    prev_value = 0
    
    for char in reversed(roman):
        if char not in ROMAN_VALUES:
            raise InvalidRomanError(f"无效字符: '{char}'")
        
        value = ROMAN_VALUES[char]
        
        # 如果当前值小于前一个值，需要减去（如 IV = 5-1=4）
        if value < prev_value:
            total -= value
        else:
            total += value
        
        prev_value = value
    
    return total


def is_valid_roman(roman: str) -> bool:
    """
    验证字符串是否为有效的罗马数字
    
    Args:
        roman: 要验证的字符串
    
    Returns:
        是否有效
    
    Examples:
        >>> is_valid_roman('MMXXIV')
        True
        >>> is_valid_roman('IIII')
        False  # 不能有连续4个I
        >>> is_valid_roman('VX')
        False  # V不能被X减去
    """
    if not isinstance(roman, str) or not roman:
        return False
    
    roman = roman.upper().strip()
    
    # 检查所有字符是否有效
    valid_chars = set(ROMAN_VALUES.keys())
    if not all(c in valid_chars for c in roman):
        return False
    
    # 使用正则验证标准格式
    import re
    pattern = r'^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$'
    return bool(re.match(pattern, roman))


def is_roman_numeral(text: str) -> bool:
    """
    检查文本是否可能是罗马数字（宽松检查）
    
    Args:
        text: 要检查的文本
    
    Returns:
        是否可能是罗马数字
    
    Examples:
        >>> is_roman_numeral('MMXXIV')
        True
        >>> is_roman_numeral('Hello')
        False
    """
    if not isinstance(text, str) or not text:
        return False
    
    text = text.upper().strip()
    valid_chars = set(ROMAN_VALUES.keys())
    
    return all(c in valid_chars for c in text) and len(text) > 0


def convert(
    value: Union[int, str],
    strict: bool = True
) -> Union[str, int]:
    """
    智能转换：自动识别输入类型并转换
    
    Args:
        value: 整数或罗马数字字符串
        strict: 是否严格验证
    
    Returns:
        转换结果
    
    Examples:
        >>> convert(2024)
        'MMXXIV'
        >>> convert('MMXXIV')
        2024
    """
    if isinstance(value, int):
        return to_roman(value, strict=strict)
    elif isinstance(value, str):
        return from_roman(value, strict=strict)
    else:
        raise TypeError(f"不支持类型: {type(value).__name__}")


def batch_to_roman(
    numbers: List[int],
    strict: bool = True,
    skip_invalid: bool = False
) -> List[Tuple[int, Union[str, None], Union[str, None]]]:
    """
    批量转换阿拉伯数字到罗马数字
    
    Args:
        numbers: 整数列表
        strict: 是否严格检查范围
        skip_invalid: 是否跳过无效值（返回None而不是抛出异常）
    
    Returns:
        列表，每项为 (原值, 结果, 错误信息)
    
    Examples:
        >>> batch_to_roman([1, 2, 3])
        [(1, 'I', None), (2, 'II', None), (3, 'III', None)]
    """
    results = []
    
    for num in numbers:
        try:
            roman = to_roman(num, strict=strict)
            results.append((num, roman, None))
        except Exception as e:
            if skip_invalid:
                results.append((num, None, str(e)))
            else:
                raise
    
    return results


def batch_from_roman(
    romans: List[str],
    strict: bool = True,
    skip_invalid: bool = False
) -> List[Tuple[str, Union[int, None], Union[str, None]]]:
    """
    批量转换罗马数字到阿拉伯数字
    
    Args:
        romans: 罗马数字字符串列表
        strict: 是否严格验证格式
        skip_invalid: 是否跳过无效值
    
    Returns:
        列表，每项为 (原值, 结果, 错误信息)
    
    Examples:
        >>> batch_from_roman(['I', 'II', 'III'])
        [('I', 1, None), ('II', 2, None), ('III', 3, None)]
    """
    results = []
    
    for roman in romans:
        try:
            num = from_roman(roman, strict=strict)
            results.append((roman, num, None))
        except Exception as e:
            if skip_invalid:
                results.append((roman, None, str(e)))
            else:
                raise
    
    return results


def get_roman_range(start: int, end: int) -> List[Tuple[int, str]]:
    """
    生成指定范围内的罗马数字列表
    
    Args:
        start: 起始值（包含）
        end: 结束值（包含）
    
    Returns:
        列表，每项为 (阿拉伯数字, 罗马数字)
    
    Examples:
        >>> get_roman_range(1, 5)
        [(1, 'I'), (2, 'II'), (3, 'III'), (4, 'IV'), (5, 'V')]
    """
    if start < MIN_VALUE:
        start = MIN_VALUE
    if end > MAX_VALUE:
        end = MAX_VALUE
    
    return [(i, to_roman(i)) for i in range(start, end + 1)]


def compare_roman(roman1: str, roman2: str) -> int:
    """
    比较两个罗马数字的大小
    
    Args:
        roman1: 第一个罗马数字
        roman2: 第二个罗马数字
    
    Returns:
        负数表示roman1<roman2，0表示相等，正数表示roman1>roman2
    
    Examples:
        >>> compare_roman('X', 'V')
        5
        >>> compare_roman('V', 'X')
        -5
        >>> compare_roman('X', 'X')
        0
    """
    num1 = from_roman(roman1)
    num2 = from_roman(roman2)
    return num1 - num2


def add_roman(roman1: str, roman2: str) -> str:
    """
    两个罗马数字相加
    
    Args:
        roman1: 第一个罗马数字
        roman2: 第二个罗马数字
    
    Returns:
        结果的罗马数字
    
    Examples:
        >>> add_roman('X', 'V')
        'XV'
        >>> add_roman('IV', 'I')
        'V'
    """
    result = from_roman(roman1) + from_roman(roman2)
    return to_roman(result)


def subtract_roman(roman1: str, roman2: str) -> str:
    """
    两个罗马数字相减
    
    Args:
        roman1: 被减数
        roman2: 减数
    
    Returns:
        结果的罗马数字
    
    Raises:
        OutOfRangeError: 结果小于等于0
    
    Examples:
        >>> subtract_roman('X', 'V')
        'V'
        >>> subtract_roman('V', 'I')
        'IV'
    """
    result = from_roman(roman1) - from_roman(roman2)
    return to_roman(result)


def multiply_roman(roman1: str, roman2: str) -> str:
    """
    两个罗马数字相乘
    
    Args:
        roman1: 第一个罗马数字
        roman2: 第二个罗马数字
    
    Returns:
        结果的罗马数字
    
    Raises:
        OutOfRangeError: 结果超出范围
    
    Examples:
        >>> multiply_roman('X', 'X')
        'C'
        >>> multiply_roman('V', 'II')
        'X'
    """
    result = from_roman(roman1) * from_roman(roman2)
    return to_roman(result)


def divide_roman(
    roman1: str,
    roman2: str,
    remainder: bool = False
) -> Union[str, Tuple[str, str]]:
    """
    两个罗马数字相除
    
    Args:
        roman1: 被除数
        roman2: 除数
        remainder: 是否返回余数
    
    Returns:
        商的罗马数字，或 (商, 余数) 元组
    
    Examples:
        >>> divide_roman('X', 'II')
        'V'
        >>> divide_roman('X', 'III', remainder=True)
        ('III', 'I')
    """
    num1 = from_roman(roman1)
    num2 = from_roman(roman2)
    
    quotient = num1 // num2
    rem = num1 % num2
    
    if remainder:
        return (to_roman(quotient), to_roman(rem))
    return to_roman(quotient)


def find_roman_in_text(text: str) -> List[Tuple[str, int, int]]:
    """
    在文本中查找所有罗马数字
    
    Args:
        text: 要搜索的文本
    
    Returns:
        列表，每项为 (罗马数字, 起始位置, 结束位置)
    
    Examples:
        >>> find_roman_in_text("Chapter XIV continues from Chapter XIII")
        [('XIV', 8, 11), ('XIII', 30, 33)]
    """
    import re
    
    # 匹配可能的罗马数字（宽松模式）
    pattern = r'\b[MCDXLVI]+\b'
    matches = []
    
    for match in re.finditer(pattern, text, re.IGNORECASE):
        candidate = match.group().upper()
        if is_valid_roman(candidate):
            matches.append((candidate, match.start(), match.end()))
    
    return matches


def normalize_roman(roman: str) -> str:
    """
    规范化罗马数字（转换为标准形式）
    
    Args:
        roman: 罗马数字字符串
    
    Returns:
        规范化后的标准形式
    
    Examples:
        >>> normalize_roman('iiii')
        'IV'
        >>> normalize_roman('VIIII')
        'IX'
    """
    # 先转换为数字，再转回罗马数字
    num = from_roman(roman, strict=False)
    return to_roman(num)


def roman_to_ordinal(roman: str) -> str:
    """
    将罗马数字转换为序数词（英文）
    
    Args:
        roman: 罗马数字字符串
    
    Returns:
        英文序数词
    
    Examples:
        >>> roman_to_ordinal('I')
        '1st'
        >>> roman_to_ordinal('II')
        '2nd'
        >>> roman_to_ordinal('III')
        '3rd'
        >>> roman_to_ordinal('IV')
        '4th'
    """
    num = from_roman(roman)
    
    if 11 <= num <= 13:
        suffix = 'th'
    else:
        last_digit = num % 10
        if last_digit == 1:
            suffix = 'st'
        elif last_digit == 2:
            suffix = 'nd'
        elif last_digit == 3:
            suffix = 'rd'
        else:
            suffix = 'th'
    
    return f"{num}{suffix}"


def get_roman_value_table() -> List[Tuple[str, int]]:
    """
    获取罗马数字符号值对照表
    
    Returns:
        符号值对照表
    
    Examples:
        >>> get_roman_value_table()
        [('I', 1), ('V', 5), ('X', 10), ('L', 50), ('C', 100), ('D', 500), ('M', 1000)]
    """
    return list(ROMAN_VALUES.items())


def explain_roman(roman: str) -> List[Tuple[str, int, str]]:
    """
    解释罗马数字的构成
    
    Args:
        roman: 罗马数字字符串
    
    Returns:
        列表，每项为 (符号, 值, 说明)
    
    Examples:
        >>> explain_roman('XIV')
        [('X', 10, '加'), ('IV', 4, '减法组合'), ('总计', 14, '')]
    """
    roman = roman.upper().strip()
    result = []
    total = 0
    i = 0
    
    # 减法组合列表
    subtractive = {'IV', 'IX', 'XL', 'XC', 'CD', 'CM'}
    subtractive_values = {
        'IV': 4, 'IX': 9, 'XL': 40, 'XC': 90, 'CD': 400, 'CM': 900
    }
    
    while i < len(roman):
        # 检查是否是减法组合
        if i + 1 < len(roman):
            pair = roman[i:i+2]
            if pair in subtractive:
                value = subtractive_values[pair]
                result.append((pair, value, '减法组合'))
                total += value
                i += 2
                continue
        
        # 单个符号
        char = roman[i]
        value = ROMAN_VALUES[char]
        result.append((char, value, '加'))
        total += value
        i += 1
    
    result.append(('总计', total, ''))
    return result


# 导出的公共API
__all__ = [
    # 常量
    'MIN_VALUE',
    'MAX_VALUE',
    'ROMAN_VALUES',
    'ROMAN_SYMBOLS',
    # 异常
    'RomanNumeralError',
    'InvalidRomanError',
    'OutOfRangeError',
    # 核心函数
    'to_roman',
    'from_roman',
    'convert',
    'is_valid_roman',
    'is_roman_numeral',
    # 批量操作
    'batch_to_roman',
    'batch_from_roman',
    'get_roman_range',
    # 比较和运算
    'compare_roman',
    'add_roman',
    'subtract_roman',
    'multiply_roman',
    'divide_roman',
    # 工具函数
    'find_roman_in_text',
    'normalize_roman',
    'roman_to_ordinal',
    'get_roman_value_table',
    'explain_roman',
]