"""
Roman Numeral Utils - 罗马数字转换工具

提供阿拉伯数字与罗马数字之间的相互转换，以及罗马数字的验证和运算功能。

Features:
- 阿拉伯数字转罗马数字 (int_to_roman)
- 罗马数字转阿拉伯数字 (roman_to_int)
- 罗马数字验证 (is_valid_roman)
- 罗马数字加减运算 (roman_add, roman_subtract)
- 罗马数字比较 (roman_compare)
- 转换大型数字（使用上划线表示法，如 V̄ = 5000）

Example:
    >>> from mod import int_to_roman, roman_to_int
    >>> int_to_roman(2024)
    'MMXXIV'
    >>> roman_to_int('MMXXIV')
    2024
"""

from typing import Tuple, Optional
import re


# 基本罗马数字映射
ROMAN_NUMERALS = {
    1: 'I',
    4: 'IV',
    5: 'V',
    9: 'IX',
    10: 'X',
    40: 'XL',
    50: 'L',
    90: 'XC',
    100: 'C',
    400: 'CD',
    500: 'D',
    900: 'CM',
    1000: 'M',
}

# 反向映射：罗马数字到阿拉伯数字
ROMAN_TO_INT_MAP = {
    'I': 1,
    'V': 5,
    'X': 10,
    'L': 50,
    'C': 100,
    'D': 500,
    'M': 1000,
}

# 扩展映射（用于大于3999的数字）
EXTENDED_ROMAN = {
    5000: 'V̄',
    10000: 'X̄',
    50000: 'L̄',
    100000: 'C̄',
    500000: 'D̄',
    1000000: 'M̄',
}

# 有效罗马数字的正则表达式
VALID_ROMAN_PATTERN = re.compile(
    '^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$',
    re.IGNORECASE
)


class RomanNumeralError(Exception):
    """罗马数字相关错误基类"""
    pass


class InvalidRomanError(RomanNumeralError):
    """无效的罗马数字"""
    pass


class OutOfRangeError(RomanNumeralError):
    """数字超出可表示范围"""
    pass


def int_to_roman(num: int, use_overline: bool = False) -> str:
    """
    将阿拉伯数字转换为罗马数字。

    Args:
        num: 要转换的整数（标准模式下支持1-3999）
        use_overline: 是否使用上划线表示法支持更大数字

    Returns:
        str: 罗马数字字符串

    Raises:
        OutOfRangeError: 数字小于1或超出可表示范围
        TypeError: 输入不是整数

    Examples:
        >>> int_to_roman(1)
        'I'
        >>> int_to_roman(4)
        'IV'
        >>> int_to_roman(2024)
        'MMXXIV'
        >>> int_to_roman(3999)
        'MMMCMXCIX'
    """
    if not isinstance(num, int):
        raise TypeError(f"输入必须是整数，当前类型: {type(num).__name__}")
    
    if num < 1:
        raise OutOfRangeError(f"罗马数字不能表示0或负数: {num}")
    
    if not use_overline and num > 3999:
        raise OutOfRangeError(
            f"标准罗马数字最大支持3999，当前: {num}。"
            "使用 use_overline=True 启用扩展表示法。"
        )
    
    result = []
    
    # 如果启用上划线且数字大于3999
    if use_overline and num >= 4000:
        # 扩展表示法
        extended_values = sorted(EXTENDED_ROMAN.items(), key=lambda x: x[0], reverse=True)
        standard_values = sorted(ROMAN_NUMERALS.items(), key=lambda x: x[0], reverse=True)
        
        for value, numeral in extended_values:
            while num >= value:
                result.append(numeral)
                num -= value
        
        for value, numeral in standard_values:
            while num >= value:
                result.append(numeral)
                num -= value
    else:
        # 标准转换
        values = sorted(ROMAN_NUMERALS.items(), key=lambda x: x[0], reverse=True)
        
        for value, numeral in values:
            while num >= value:
                result.append(numeral)
                num -= value
    
    return ''.join(result)


def roman_to_int(roman: str) -> int:
    """
    将罗马数字转换为阿拉伯数字。

    Args:
        roman: 罗马数字字符串

    Returns:
        int: 对应的阿拉伯数字

    Raises:
        InvalidRomanError: 输入不是有效的罗马数字
        TypeError: 输入不是字符串

    Examples:
        >>> roman_to_int('I')
        1
        >>> roman_to_int('IV')
        4
        >>> roman_to_int('MMXXIV')
        2024
    """
    if not isinstance(roman, str):
        raise TypeError(f"输入必须是字符串，当前类型: {type(roman).__name__}")
    
    roman = roman.strip().upper()
    
    if not roman:
        raise InvalidRomanError("空字符串不是有效的罗马数字")
    
    # 验证罗马数字格式
    if not is_valid_roman(roman):
        raise InvalidRomanError(f"无效的罗马数字: '{roman}'")
    
    result = 0
    prev_value = 0
    
    for char in reversed(roman):
        if char not in ROMAN_TO_INT_MAP:
            raise InvalidRomanError(f"无效的罗马数字字符: '{char}'")
        
        current_value = ROMAN_TO_INT_MAP[char]
        
        # 如果当前值小于前一个值，则减去（处理减法原则）
        if current_value < prev_value:
            result -= current_value
        else:
            result += current_value
        
        prev_value = current_value
    
    return result


def is_valid_roman(roman: str) -> bool:
    """
    验证字符串是否为有效的罗马数字。

    Args:
        roman: 要验证的字符串

    Returns:
        bool: 是否为有效的罗马数字

    Examples:
        >>> is_valid_roman('IV')
        True
        >>> is_valid_roman('IIII')
        False
        >>> is_valid_roman('ABC')
        False
    """
    if not isinstance(roman, str):
        return False
    
    roman = roman.strip().upper()
    
    if not roman:
        return False
    
    # 检查所有字符是否有效
    valid_chars = set(ROMAN_TO_INT_MAP.keys())
    if not all(char in valid_chars for char in roman):
        return False
    
    # 使用正则表达式验证格式
    return bool(VALID_ROMAN_PATTERN.match(roman))


def roman_add(roman1: str, roman2: str) -> str:
    """
    两个罗马数字相加。

    Args:
        roman1: 第一个罗马数字
        roman2: 第二个罗马数字

    Returns:
        str: 相加结果的罗马数字

    Raises:
        InvalidRomanError: 输入不是有效的罗马数字
        OutOfRangeError: 结果超出可表示范围

    Examples:
        >>> roman_add('X', 'V')
        'XV'
        >>> roman_add('IV', 'VI')
        'X'
    """
    num1 = roman_to_int(roman1)
    num2 = roman_to_int(roman2)
    return int_to_roman(num1 + num2)


def roman_subtract(roman1: str, roman2: str) -> str:
    """
    两个罗马数字相减。

    Args:
        roman1: 被减数（罗马数字）
        roman2: 减数（罗马数字）

    Returns:
        str: 相减结果的罗马数字

    Raises:
        InvalidRomanError: 输入不是有效的罗马数字
        OutOfRangeError: 结果小于或等于0

    Examples:
        >>> roman_subtract('X', 'V')
        'V'
        >>> roman_subtract('X', 'I')
        'IX'
    """
    num1 = roman_to_int(roman1)
    num2 = roman_to_int(roman2)
    return int_to_roman(num1 - num2)


def roman_multiply(roman1: str, roman2: str) -> str:
    """
    两个罗马数字相乘。

    Args:
        roman1: 第一个罗马数字
        roman2: 第二个罗马数字

    Returns:
        str: 相乘结果的罗马数字

    Raises:
        InvalidRomanError: 输入不是有效的罗马数字
        OutOfRangeError: 结果超出可表示范围

    Examples:
        >>> roman_multiply('V', 'II')
        'X'
        >>> roman_multiply('X', 'X')
        'C'
    """
    num1 = roman_to_int(roman1)
    num2 = roman_to_int(roman2)
    return int_to_roman(num1 * num2)


def roman_divide(roman1: str, roman2: str) -> Tuple[str, str]:
    """
    两个罗马数字相除。

    Args:
        roman1: 被除数（罗马数字）
        roman2: 除数（罗马数字）

    Returns:
        Tuple[str, str]: (商, 余数) 都是罗马数字

    Raises:
        InvalidRomanError: 输入不是有效的罗马数字
        ZeroDivisionError: 除数为0

    Examples:
        >>> roman_divide('X', 'III')
        ('III', 'I')
        >>> roman_divide('X', 'II')
        ('V', '')
    """
    num1 = roman_to_int(roman1)
    num2 = roman_to_int(roman2)
    
    if num2 == 0:
        raise ZeroDivisionError("罗马数字不能被零整除")
    
    quotient = num1 // num2
    remainder = num1 % num2
    
    if quotient == 0:
        raise OutOfRangeError("商为0，罗马数字无法表示0")
    
    result = int_to_roman(quotient)
    remainder_roman = int_to_roman(remainder) if remainder > 0 else ''
    
    return (result, remainder_roman)


def roman_compare(roman1: str, roman2: str) -> int:
    """
    比较两个罗马数字的大小。

    Args:
        roman1: 第一个罗马数字
        roman2: 第二个罗马数字

    Returns:
        int: 负数表示roman1<roman2，0表示相等，正数表示roman1>roman2

    Raises:
        InvalidRomanError: 输入不是有效的罗马数字

    Examples:
        >>> roman_compare('V', 'X')
        -1
        >>> roman_compare('X', 'X')
        0
        >>> roman_compare('X', 'V')
        1
    """
    num1 = roman_to_int(roman1)
    num2 = roman_to_int(roman2)
    
    if num1 < num2:
        return -1
    elif num1 > num2:
        return 1
    else:
        return 0


def get_roman_info(roman: str) -> dict:
    """
    获取罗马数字的详细信息。

    Args:
        roman: 罗马数字字符串

    Returns:
        dict: 包含各种信息的字典

    Examples:
        >>> info = get_roman_info('MMXXIV')
        >>> info['value']
        2024
        >>> info['valid']
        True
    """
    try:
        value = roman_to_int(roman)
        valid = True
        length = len(roman.strip().upper())
        
        # 分析组成
        components = []
        temp_value = value
        for val, numeral in sorted(ROMAN_NUMERALS.items(), key=lambda x: x[0], reverse=True):
            while temp_value >= val:
                components.append(numeral)
                temp_value -= val
        
        return {
            'original': roman.strip().upper(),
            'value': value,
            'valid': valid,
            'length': length,
            'components': components,
            'digit_count': len(str(value)),
        }
    except RomanNumeralError:
        return {
            'original': roman.strip().upper() if isinstance(roman, str) else str(roman),
            'value': None,
            'valid': False,
            'error': '无效的罗马数字',
        }


def find_roman_range(start: int, end: int) -> list:
    """
    生成指定范围内所有整数的罗马数字列表。

    Args:
        start: 起始整数
        end: 结束整数

    Returns:
        list: 包含(value, roman)元组的列表

    Raises:
        OutOfRangeError: 范围超出可表示范围

    Examples:
        >>> find_roman_range(1, 5)
        [(1, 'I'), (2, 'II'), (3, 'III'), (4, 'IV'), (5, 'V')]
    """
    if start < 1 or end > 3999:
        raise OutOfRangeError("范围必须在1到3999之间")
    
    if start > end:
        start, end = end, start
    
    return [(i, int_to_roman(i)) for i in range(start, end + 1)]


def search_by_value(value: int) -> Optional[str]:
    """
    根据阿拉伯数字值搜索对应的罗马数字。

    Args:
        value: 要搜索的值

    Returns:
        Optional[str]: 对应的罗马数字，如果超出范围则返回None

    Examples:
        >>> search_by_value(10)
        'X'
        >>> search_by_value(5000)
        None
    """
    try:
        return int_to_roman(value)
    except OutOfRangeError:
        return None


# 预定义的常见罗马数字
COMMON_ROMANS = {
    1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V',
    6: 'VI', 7: 'VII', 8: 'VIII', 9: 'IX', 10: 'X',
    20: 'XX', 30: 'XXX', 40: 'XL', 50: 'L',
    60: 'LX', 70: 'LXX', 80: 'LXXX', 90: 'XC', 100: 'C',
    200: 'CC', 300: 'CCC', 400: 'CD', 500: 'D',
    600: 'DC', 700: 'DCC', 800: 'DCCC', 900: 'CM', 1000: 'M',
    1984: 'MCMLXXXIV', 1999: 'MCMXCIX', 
    2000: 'MM', 2024: 'MMXXIV', 
    2025: 'MMXXV', 3000: 'MMM', 3999: 'MMMCMXCIX',
}


if __name__ == '__main__':
    # 演示功能
    print("=" * 50)
    print("Roman Numeral Utils - 罗马数字转换工具演示")
    print("=" * 50)
    
    # 基本转换
    print("\n【基本转换】")
    test_numbers = [1, 4, 9, 49, 99, 2024, 3999]
    for num in test_numbers:
        roman = int_to_roman(num)
        back = roman_to_int(roman)
        print(f"  {num} → {roman} → {back}")
    
    # 验证
    print("\n【验证功能】")
    test_romans = ['IV', 'IIII', 'ABC', 'MMXXIV', 'MCMLXXXIV']
    for r in test_romans:
        valid = is_valid_roman(r)
        print(f"  '{r}': {'有效' if valid else '无效'}")
    
    # 运算
    print("\n【运算功能】")
    print(f"  X + V = {roman_add('X', 'V')}")
    print(f"  X - I = {roman_subtract('X', 'I')}")
    print(f"  V × II = {roman_multiply('V', 'II')}")
    print(f"  X ÷ III = {roman_divide('X', 'III')}")
    
    # 比较
    print("\n【比较功能】")
    pairs = [('V', 'X'), ('X', 'X'), ('X', 'V')]
    for a, b in pairs:
        result = roman_compare(a, b)
        symbol = '<' if result < 0 else ('=' if result == 0 else '>')
        print(f"  {a} {symbol} {b}")
    
    print("\n" + "=" * 50)