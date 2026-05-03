"""
罗马数字转换工具模块 (Roman Numeral Utilities)

功能：
- 阿拉伯数字转罗马数字
- 罗马数字转阿拉伯数字
- 罗马数字验证
- 罗马数字加减运算
- 支持范围：1-3999（标准罗马数字）

零外部依赖，纯 Python 实现。

Author: AllToolkit
Date: 2026-05-03
"""

from typing import Tuple, List, Optional


# 罗马数字符号映射
ROMAN_VALUES = {
    'I': 1,
    'V': 5,
    'X': 10,
    'L': 50,
    'C': 100,
    'D': 500,
    'M': 1000
}

# 阿拉伯数字转罗马数字的映射（按值降序排列）
ARABIC_TO_ROMAN = [
    (1000, 'M'),
    (900, 'CM'),
    (500, 'D'),
    (400, 'CD'),
    (100, 'C'),
    (90, 'XC'),
    (50, 'L'),
    (40, 'XL'),
    (10, 'X'),
    (9, 'IX'),
    (5, 'V'),
    (4, 'IV'),
    (1, 'I')
]

# 有效的减法组合
VALID_SUBTRACTIONS = {
    'I': {'V', 'X'},
    'X': {'L', 'C'},
    'C': {'D', 'M'}
}

# 不允许重复的符号
NO_REPEAT_SYMBOLS = {'V', 'L', 'D'}

# 最大连续重复次数
MAX_REPEAT = 3


def is_valid_roman(roman: str) -> bool:
    """
    验证罗马数字格式是否正确。
    
    Args:
        roman: 待验证的罗马数字字符串
        
    Returns:
        bool: 如果格式正确返回 True，否则返回 False
        
    Examples:
        >>> is_valid_roman('XIV')
        True
        >>> is_valid_roman('IIII')
        False
        >>> is_valid_roman('VX')
        False
    """
    if not roman:
        return False
    
    roman = roman.upper()
    
    # 检查是否只包含有效字符
    if not all(c in ROMAN_VALUES for c in roman):
        return False
    
    # 检查连续重复
    repeat_count = 1
    for i in range(1, len(roman)):
        if roman[i] == roman[i-1]:
            repeat_count += 1
            # V, L, D 不能重复
            if roman[i] in NO_REPEAT_SYMBOLS:
                return False
            # I, X, C, M 最多连续 3 次
            if repeat_count > MAX_REPEAT:
                return False
        else:
            repeat_count = 1
    
    # 检查减法规则
    i = 0
    while i < len(roman):
        if i + 1 < len(roman):
            current = roman[i]
            next_char = roman[i + 1]
            
            # 如果当前字符比下一个字符小，检查是否是有效的减法组合
            if ROMAN_VALUES[current] < ROMAN_VALUES[next_char]:
                if current not in VALID_SUBTRACTIONS:
                    return False
                if next_char not in VALID_SUBTRACTIONS[current]:
                    return False
                
                # 减法组合后不能跟随更大的字符
                if i + 2 < len(roman):
                    if ROMAN_VALUES[roman[i + 2]] >= ROMAN_VALUES[next_char]:
                        return False
                
                i += 2
                continue
        i += 1
    
    return True


def to_roman(num: int) -> str:
    """
    将阿拉伯数字转换为罗马数字。
    
    Args:
        num: 阿拉伯数字（1-3999）
        
    Returns:
        str: 对应的罗马数字
        
    Raises:
        ValueError: 如果数字超出范围或不是正整数
        
    Examples:
        >>> to_roman(1)
        'I'
        >>> to_roman(14)
        'XIV'
        >>> to_roman(2024)
        'MMXXIV'
    """
    if not isinstance(num, int):
        raise ValueError("输入必须是整数")
    
    if num < 1:
        raise ValueError("罗马数字最小为 1")
    
    if num > 3999:
        raise ValueError("标准罗马数字最大为 3999")
    
    result = []
    remaining = num
    
    for value, symbol in ARABIC_TO_ROMAN:
        count, remaining = divmod(remaining, value)
        result.append(symbol * count)
    
    return ''.join(result)


def to_arabic(roman: str) -> int:
    """
    将罗马数字转换为阿拉伯数字。
    
    Args:
        roman: 罗马数字字符串
        
    Returns:
        int: 对应的阿拉伯数字
        
    Raises:
        ValueError: 如果罗马数字格式无效
        
    Examples:
        >>> to_arabic('I')
        1
        >>> to_arabic('XIV')
        14
        >>> to_arabic('MMXXIV')
        2024
    """
    if not roman:
        raise ValueError("输入不能为空")
    
    roman = roman.upper()
    
    if not is_valid_roman(roman):
        raise ValueError(f"无效的罗马数字格式: {roman}")
    
    result = 0
    i = 0
    
    while i < len(roman):
        # 如果当前字符比下一个字符小，执行减法
        if i + 1 < len(roman) and ROMAN_VALUES[roman[i]] < ROMAN_VALUES[roman[i + 1]]:
            result += ROMAN_VALUES[roman[i + 1]] - ROMAN_VALUES[roman[i]]
            i += 2
        else:
            result += ROMAN_VALUES[roman[i]]
            i += 1
    
    return result


def add(roman1: str, roman2: str) -> str:
    """
    两个罗马数字相加。
    
    Args:
        roman1: 第一个罗马数字
        roman2: 第二个罗马数字
        
    Returns:
        str: 相加结果的罗马数字
        
    Examples:
        >>> add('X', 'V')
        'XV'
        >>> add('IV', 'I')
        'V'
    """
    arabic1 = to_arabic(roman1)
    arabic2 = to_arabic(roman2)
    return to_roman(arabic1 + arabic2)


def subtract(roman1: str, roman2: str) -> str:
    """
    两个罗马数字相减（roman1 - roman2）。
    
    Args:
        roman1: 被减数罗马数字
        roman2: 减数罗马数字
        
    Returns:
        str: 相减结果的罗马数字
        
    Raises:
        ValueError: 如果结果小于等于 0
        
    Examples:
        >>> subtract('X', 'V')
        'V'
        >>> subtract('X', 'X')
        ValueError
    """
    arabic1 = to_arabic(roman1)
    arabic2 = to_arabic(roman2)
    return to_roman(arabic1 - arabic2)


def compare(roman1: str, roman2: str) -> int:
    """
    比较两个罗马数字的大小。
    
    Args:
        roman1: 第一个罗马数字
        roman2: 第二个罗马数字
        
    Returns:
        int: 如果 roman1 > roman2 返回 1，相等返回 0，小于返回 -1
        
    Examples:
        >>> compare('X', 'V')
        1
        >>> compare('V', 'V')
        0
        >>> compare('I', 'X')
        -1
    """
    arabic1 = to_arabic(roman1)
    arabic2 = to_arabic(roman2)
    
    if arabic1 > arabic2:
        return 1
    elif arabic1 < arabic2:
        return -1
    return 0


def find_largest_smaller(roman: str, candidates: List[str]) -> Optional[str]:
    """
    在候选列表中找出小于给定罗马数字的最大值。
    
    Args:
        roman: 目标罗马数字
        candidates: 候选罗马数字列表
        
    Returns:
        Optional[str]: 最大的小于目标的候选值，如果没有则返回 None
        
    Examples:
        >>> find_largest_smaller('X', ['V', 'VII', 'XV', 'III'])
        'VII'
    """
    target = to_arabic(roman)
    valid_candidates = [c for c in candidates if to_arabic(c) < target]
    
    if not valid_candidates:
        return None
    
    return max(valid_candidates, key=to_arabic)


def range_to_roman(start: int, end: int) -> List[str]:
    """
    生成指定范围内所有数字的罗马数字列表。
    
    Args:
        start: 起始数字（包含）
        end: 结束数字（包含）
        
    Returns:
        List[str]: 罗马数字列表
        
    Examples:
        >>> range_to_roman(1, 5)
        ['I', 'II', 'III', 'IV', 'V']
    """
    return [to_roman(i) for i in range(start, end + 1)]


def get_value(roman: str) -> int:
    """
    获取罗马数字对应的阿拉伯数字值（to_arabic 的别名）。
    
    Args:
        roman: 罗马数字字符串
        
    Returns:
        int: 对应的阿拉伯数字
    """
    return to_arabic(roman)


def get_roman(num: int) -> str:
    """
    获取阿拉伯数字对应的罗马数字（to_roman 的别名）。
    
    Args:
        num: 阿拉伯数字
        
    Returns:
        str: 对应的罗马数字
    """
    return to_roman(num)


def list_operations(roman1: str, roman2: str) -> dict:
    """
    获取两个罗马数字之间的所有运算结果。
    
    Args:
        roman1: 第一个罗马数字
        roman2: 第二个罗马数字
        
    Returns:
        dict: 包含加法、减法、比较等结果的字典
        
    Examples:
        >>> list_operations('X', 'V')
        {'add': 'XV', 'subtract': 'V', 'compare': 1, 'sum_arabic': 15, 'diff_arabic': 5}
    """
    arabic1 = to_arabic(roman1)
    arabic2 = to_arabic(roman2)
    
    result = {
        'roman1': roman1.upper(),
        'roman2': roman2.upper(),
        'arabic1': arabic1,
        'arabic2': arabic2,
        'sum_arabic': arabic1 + arabic2,
        'diff_arabic': abs(arabic1 - arabic2),
        'compare': compare(roman1, roman2)
    }
    
    result['add'] = to_roman(arabic1 + arabic2)
    
    if arabic1 > arabic2:
        result['subtract'] = to_roman(arabic1 - arabic2)
    elif arabic1 < arabic2:
        result['subtract'] = to_roman(arabic2 - arabic1)
    else:
        result['subtract'] = None
    
    return result


# 预定义的常用罗马数字
COMMON_ROMANS = {
    1: 'I',
    2: 'II',
    3: 'III',
    4: 'IV',
    5: 'V',
    6: 'VI',
    7: 'VII',
    8: 'VIII',
    9: 'IX',
    10: 'X',
    20: 'XX',
    30: 'XXX',
    40: 'XL',
    50: 'L',
    100: 'C',
    500: 'D',
    1000: 'M'
}


def quick_convert(num: int) -> str:
    """
    快速转换常用数字（使用预定义映射）。
    如果不在预定义映射中，则调用标准转换函数。
    
    Args:
        num: 阿拉伯数字
        
    Returns:
        str: 对应的罗马数字
        
    Examples:
        >>> quick_convert(10)
        'X'
        >>> quick_convert(11)
        'XI'
    """
    if num in COMMON_ROMANS:
        return COMMON_ROMANS[num]
    return to_roman(num)


def parse_mixed(text: str) -> List[Tuple[str, int]]:
    """
    解析混合文本，提取其中的罗马数字。
    
    Args:
        text: 包含罗马数字的文本
        
    Returns:
        List[Tuple[str, int]]: 匹配到的罗马数字及其值的列表
        
    Examples:
        >>> parse_mixed('Chapter XII and Section IV')
        [('XII', 12), ('IV', 4)]
    """
    import re
    
    # 匹配罗马数字的正则表达式
    # 只匹配有效的罗马数字模式
    pattern = r'\b(?=[MDCLXVI]+\b)(M{0,3})(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\b'
    
    matches = re.finditer(pattern, text, re.IGNORECASE)
    results = []
    
    for match in matches:
        roman = match.group(0)
        try:
            value = to_arabic(roman)
            results.append((roman.upper(), value))
        except ValueError:
            # 跳过无效匹配
            continue
    
    return results


if __name__ == '__main__':
    # 简单测试
    print("=== 罗马数字转换工具测试 ===")
    print()
    
    # 测试转换
    test_numbers = [1, 4, 9, 14, 49, 99, 100, 444, 999, 2024, 3999]
    print("阿拉伯数字 → 罗马数字:")
    for num in test_numbers:
        roman = to_roman(num)
        print(f"  {num:4d} → {roman}")
    
    print()
    print("罗马数字 → 阿拉伯数字:")
    test_romans = ['I', 'IV', 'IX', 'XIV', 'XLIX', 'XCIX', 'C', 'CDXLIV', 'CMXCIX', 'MMXXIV', 'MMMCMXCIX']
    for roman in test_romans:
        arabic = to_arabic(roman)
        print(f"  {roman:10s} → {arabic}")
    
    print()
    print("验证测试:")
    valid_tests = ['XIV', 'MMXXIV', 'MMMCMXCIX']
    invalid_tests = ['IIII', 'VV', 'VX', 'IC', '']
    for test in valid_tests:
        print(f"  '{test}' 有效: {is_valid_roman(test)}")
    for test in invalid_tests:
        print(f"  '{test}' 有效: {is_valid_roman(test)}")
    
    print()
    print("运算测试:")
    print(f"  X + V = {add('X', 'V')}")
    print(f"  X - V = {subtract('X', 'V')}")
    print(f"  比较 X 和 V: {compare('X', 'V')}")
    
    print()
    print("范围生成:")
    print(f"  1-10: {range_to_roman(1, 10)}")