"""
Roman Numeral Utilities - 零外部依赖的罗马数字转换工具

功能:
- 阿拉伯数字转罗马数字 (1-3999)
- 罗马数字转阿拉伯数字
- 罗马数字验证
- 罗马数字算术运算 (加减乘除)
- 罗马数字比较和排序
- 支持扩展罗马数字 (使用上划线表示乘以1000)
- 链式调用 API
"""

from typing import Optional, List, Tuple, Union
from functools import total_ordering


class RomanNumeralError(Exception):
    """罗马数字相关错误的基类"""
    pass


class InvalidRomanNumeralError(RomanNumeralError):
    """无效的罗马数字格式"""
    pass


class OutOfRangeError(RomanNumeralError):
    """数值超出范围"""
    pass


# 基本罗马数字映射
ROMAN_MAP = {
    1000: 'M',
    900: 'CM',
    500: 'D',
    400: 'CD',
    100: 'C',
    90: 'XC',
    50: 'L',
    40: 'XL',
    10: 'X',
    9: 'IX',
    5: 'V',
    4: 'IV',
    1: 'I'
}

# 罗马数字到阿拉伯数字的映射
ROMAN_VALUES = {
    'I': 1,
    'V': 5,
    'X': 10,
    'L': 50,
    'C': 100,
    'D': 500,
    'M': 1000
}

# 扩展罗马数字映射（用于表示更大的数，上划线用括号表示）
EXTENDED_ROMAN_MAP = {
    1000000: '(M)',      # M with overline
    900000: '(CM)',
    500000: '(D)',       # D with overline
    400000: '(CD)',
    100000: '(C)',       # C with overline
    90000: '(XC)',
    50000: '(L)',         # L with overline
    40000: '(XL)',
    10000: '(X)',         # X with overline
    9000: '(IX)',
    5000: '(V)',          # V with overline
    4000: '(IV)',
    1000: 'M',
    900: 'CM',
    500: 'D',
    400: 'CD',
    100: 'C',
    90: 'XC',
    50: 'L',
    40: 'XL',
    10: 'X',
    9: 'IX',
    5: 'V',
    4: 'IV',
    1: 'I'
}

# 扩展罗马数字值
EXTENDED_ROMAN_VALUES = {
    'I': 1,
    'V': 5,
    'X': 10,
    'L': 50,
    'C': 100,
    'D': 500,
    'M': 1000,
    '(IV)': 4000,
    '(V)': 5000,
    '(IX)': 9000,
    '(X)': 10000,
    '(XL)': 40000,
    '(L)': 50000,
    '(XC)': 90000,
    '(C)': 100000,
    '(CD)': 400000,
    '(D)': 500000,
    '(CM)': 900000,
    '(M)': 1000000
}


def to_roman(num: int, extended: bool = False) -> str:
    """
    将阿拉伯数字转换为罗马数字
    
    Args:
        num: 要转换的阿拉伯数字
        extended: 是否使用扩展罗马数字（支持更大的数值）
    
    Returns:
        罗马数字字符串
    
    Raises:
        OutOfRangeError: 数值超出有效范围
        TypeError: 输入不是整数
    
    Examples:
        >>> to_roman(1)
        'I'
        >>> to_roman(1994)
        'MCMXCIV'
        >>> to_roman(4000, extended=True)
        '(IV)'
    """
    if not isinstance(num, int):
        raise TypeError(f"Expected int, got {type(num).__name__}")
    
    if extended:
        if num < 1 or num > 3999999:
            raise OutOfRangeError(f"Number {num} out of range for extended roman numerals (1-3999999)")
        mapping = EXTENDED_ROMAN_MAP
    else:
        if num < 1 or num > 3999:
            raise OutOfRangeError(f"Number {num} out of range for standard roman numerals (1-3999)")
        mapping = ROMAN_MAP
    
    result = []
    for value, symbol in mapping.items():
        while num >= value:
            result.append(symbol)
            num -= value
    
    return ''.join(result)


def from_roman(roman: str, extended: bool = False) -> int:
    """
    将罗马数字转换为阿拉伯数字
    
    Args:
        roman: 罗马数字字符串
        extended: 是否解析扩展罗马数字
    
    Returns:
        对应的阿拉伯数字
    
    Raises:
        InvalidRomanNumeralError: 无效的罗马数字格式
        TypeError: 输入不是字符串
    
    Examples:
        >>> from_roman('I')
        1
        >>> from_roman('MCMXCIV')
        1994
        >>> from_roman('(IV)', extended=True)
        4000
    """
    if not isinstance(roman, str):
        raise TypeError(f"Expected str, got {type(roman).__name__}")
    
    roman = roman.strip().upper()
    
    if not roman:
        raise InvalidRomanNumeralError("Empty string is not a valid roman numeral")
    
    if extended:
        return _parse_extended_roman(roman)
    else:
        return _parse_standard_roman(roman)


def _parse_standard_roman(roman: str) -> int:
    """解析标准罗马数字"""
    # 验证字符
    valid_chars = set(ROMAN_VALUES.keys())
    if not all(c in valid_chars for c in roman):
        raise InvalidRomanNumeralError(f"Invalid character in roman numeral: {roman}")
    
    # 计算值
    result = 0
    prev_value = 0
    
    for char in reversed(roman):
        value = ROMAN_VALUES[char]
        if value < prev_value:
            result -= value
        else:
            result += value
        prev_value = value
    
    # 验证：转换回去应该得到相同的结果
    if to_roman(result) != roman:
        raise InvalidRomanNumeralError(f"Invalid roman numeral format: {roman}")
    
    return result


def _parse_extended_roman(roman: str) -> int:
    """解析扩展罗马数字（支持上划线表示法，用括号代替）"""
    result = 0
    i = 0
    
    while i < len(roman):
        # 尝试匹配扩展符号（括号包围的）
        if roman[i] == '(':
            end = roman.find(')', i)
            if end == -1:
                raise InvalidRomanNumeralError(f"Unmatched parenthesis in: {roman}")
            
            extended_symbol = roman[i:end+1]
            if extended_symbol not in EXTENDED_ROMAN_VALUES:
                raise InvalidRomanNumeralError(f"Invalid extended symbol: {extended_symbol}")
            
            result += EXTENDED_ROMAN_VALUES[extended_symbol]
            i = end + 1
        elif roman[i] in ROMAN_VALUES:
            # 标准罗马数字
            result += ROMAN_VALUES[roman[i]]
            i += 1
        else:
            raise InvalidRomanNumeralError(f"Invalid character in roman numeral: {roman[i]}")
    
    return result


def is_valid_roman(roman: str, extended: bool = False) -> bool:
    """
    检查字符串是否为有效的罗马数字
    
    Args:
        roman: 要检查的字符串
        extended: 是否支持扩展罗马数字
    
    Returns:
        如果有效返回True，否则返回False
    
    Examples:
        >>> is_valid_roman('MCMXCIV')
        True
        >>> is_valid_roman('ABC')
        False
        >>> is_valid_roman('IIII')
        False
    """
    try:
        from_roman(roman, extended=extended)
        return True
    except (InvalidRomanNumeralError, TypeError):
        return False


def validate_roman(roman: str, extended: bool = False) -> Tuple[bool, Optional[str]]:
    """
    验证罗马数字并返回详细信息
    
    Args:
        roman: 要验证的字符串
        extended: 是否支持扩展罗马数字
    
    Returns:
        (是否有效, 错误信息)
    
    Examples:
        >>> validate_roman('MCMXCIV')
        (True, None)
        >>> validate_roman('ABC')
        (False, 'Invalid character in roman numeral: ABC')
    """
    try:
        value = from_roman(roman, extended=extended)
        return True, f"Valid roman numeral for {value}"
    except InvalidRomanNumeralError as e:
        return False, str(e)
    except TypeError as e:
        return False, str(e)


@total_ordering
class RomanNumeral:
    """
    罗马数字类，支持算术运算和比较
    
    Examples:
        >>> r1 = RomanNumeral(10)
        >>> r2 = RomanNumeral('V')
        >>> r1 + r2
        RomanNumeral('XV')
        >>> r1 * r2
        RomanNumeral('L')
        >>> r1 > r2
        True
    """
    
    def __init__(self, value: Union[int, str], extended: bool = False):
        """
        初始化罗马数字
        
        Args:
            value: 阿拉伯数字(int)或罗马数字(str)
            extended: 是否使用扩展罗马数字
        """
        self._extended = extended
        
        if isinstance(value, int):
            self._arabic = value
            self._roman = to_roman(value, extended=extended)
        elif isinstance(value, str):
            self._arabic = from_roman(value, extended=extended)
            self._roman = to_roman(self._arabic, extended=extended)
        else:
            raise TypeError(f"Expected int or str, got {type(value).__name__}")
    
    @property
    def arabic(self) -> int:
        """返回阿拉伯数字表示"""
        return self._arabic
    
    @property
    def roman(self) -> str:
        """返回罗马数字表示"""
        return self._roman
    
    @property
    def extended(self) -> bool:
        """是否使用扩展罗马数字"""
        return self._extended
    
    def __repr__(self) -> str:
        return f"RomanNumeral('{self._roman}')"
    
    def __str__(self) -> str:
        return self._roman
    
    def __int__(self) -> int:
        return self._arabic
    
    def __add__(self, other: Union['RomanNumeral', int]) -> 'RomanNumeral':
        if isinstance(other, RomanNumeral):
            return RomanNumeral(self._arabic + other._arabic, extended=self._extended)
        elif isinstance(other, int):
            return RomanNumeral(self._arabic + other, extended=self._extended)
        return NotImplemented
    
    def __radd__(self, other: int) -> 'RomanNumeral':
        return self.__add__(other)
    
    def __sub__(self, other: Union['RomanNumeral', int]) -> 'RomanNumeral':
        if isinstance(other, RomanNumeral):
            result = self._arabic - other._arabic
        elif isinstance(other, int):
            result = self._arabic - other
        else:
            return NotImplemented
        
        if result < 1:
            raise OutOfRangeError("Roman numerals cannot represent zero or negative numbers")
        return RomanNumeral(result, extended=self._extended)
    
    def __rsub__(self, other: int) -> 'RomanNumeral':
        result = other - self._arabic
        if result < 1:
            raise OutOfRangeError("Roman numerals cannot represent zero or negative numbers")
        return RomanNumeral(result, extended=self._extended)
    
    def __mul__(self, other: Union['RomanNumeral', int]) -> 'RomanNumeral':
        if isinstance(other, RomanNumeral):
            return RomanNumeral(self._arabic * other._arabic, extended=self._extended)
        elif isinstance(other, int):
            return RomanNumeral(self._arabic * other, extended=self._extended)
        return NotImplemented
    
    def __rmul__(self, other: int) -> 'RomanNumeral':
        return self.__mul__(other)
    
    def __truediv__(self, other: Union['RomanNumeral', int]) -> 'RomanNumeral':
        if isinstance(other, RomanNumeral):
            result = self._arabic // other._arabic
        elif isinstance(other, int):
            result = self._arabic // other
        else:
            return NotImplemented
        
        if result < 1:
            raise OutOfRangeError("Roman numerals cannot represent zero or negative numbers")
        return RomanNumeral(result, extended=self._extended)
    
    def __floordiv__(self, other: Union['RomanNumeral', int]) -> 'RomanNumeral':
        return self.__truediv__(other)
    
    def __mod__(self, other: Union['RomanNumeral', int]) -> 'RomanNumeral':
        if isinstance(other, RomanNumeral):
            result = self._arabic % other._arabic
        elif isinstance(other, int):
            result = self._arabic % other
        else:
            return NotImplemented
        
        if result < 1:
            raise OutOfRangeError("Roman numerals cannot represent zero or negative numbers")
        return RomanNumeral(result, extended=self._extended)
    
    def __pow__(self, other: int) -> 'RomanNumeral':
        if not isinstance(other, int):
            return NotImplemented
        return RomanNumeral(self._arabic ** other, extended=self._extended)
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, RomanNumeral):
            return self._arabic == other._arabic
        elif isinstance(other, int):
            return self._arabic == other
        elif isinstance(other, str):
            try:
                return self._arabic == from_roman(other, extended=self._extended)
            except InvalidRomanNumeralError:
                return False
        return NotImplemented
    
    def __lt__(self, other: Union['RomanNumeral', int]) -> bool:
        if isinstance(other, RomanNumeral):
            return self._arabic < other._arabic
        elif isinstance(other, int):
            return self._arabic < other
        return NotImplemented
    
    def __hash__(self) -> int:
        return hash(self._arabic)


def roman_sort(romans: List[Union[str, 'RomanNumeral', int]], 
               reverse: bool = False,
               extended: bool = False) -> List[str]:
    """
    对罗马数字列表进行排序
    
    Args:
        romans: 罗马数字列表（可以是字符串、RomanNumeral对象或整数）
        reverse: 是否降序排列
        extended: 是否使用扩展罗马数字
    
    Returns:
        排序后的罗马数字字符串列表
    
    Examples:
        >>> roman_sort(['III', 'I', 'II'])
        ['I', 'II', 'III']
        >>> roman_sort(['M', 'I', 'C'], reverse=True)
        ['M', 'C', 'I']
    """
    def to_sort_key(item):
        if isinstance(item, RomanNumeral):
            return item.arabic
        elif isinstance(item, int):
            return item
        elif isinstance(item, str):
            return from_roman(item, extended=extended)
        else:
            raise TypeError(f"Unsupported type: {type(item)}")
    
    sorted_items = sorted(romans, key=to_sort_key, reverse=reverse)
    
    # 转换为罗马数字字符串
    result = []
    for item in sorted_items:
        if isinstance(item, RomanNumeral):
            result.append(item.roman)
        elif isinstance(item, int):
            result.append(to_roman(item, extended=extended))
        else:
            result.append(item)
    
    return result


def roman_range(start: int, end: int, step: int = 1, extended: bool = False) -> List[str]:
    """
    生成罗马数字范围内的列表
    
    Args:
        start: 起始值（阿拉伯数字）
        end: 结束值（阿拉伯数字）
        step: 步长
        extended: 是否使用扩展罗马数字
    
    Returns:
        罗马数字字符串列表
    
    Examples:
        >>> roman_range(1, 5)
        ['I', 'II', 'III', 'IV', 'V']
    """
    max_val = 3999999 if extended else 3999
    if start < 1 or end > max_val:
        raise OutOfRangeError(f"Range must be within 1-{max_val}")
    
    return [to_roman(i, extended=extended) for i in range(start, end + 1, step)]


def roman_sum(romans: List[Union[str, 'RomanNumeral', int]], extended: bool = False) -> str:
    """
    计算罗马数字列表的和
    
    Args:
        romans: 罗马数字列表
        extended: 是否使用扩展罗马数字
    
    Returns:
        和的罗马数字表示
    
    Examples:
        >>> roman_sum(['X', 'V'])
        'XV'
    """
    total = 0
    for item in romans:
        if isinstance(item, RomanNumeral):
            total += item.arabic
        elif isinstance(item, int):
            total += item
        elif isinstance(item, str):
            total += from_roman(item, extended=extended)
        else:
            raise TypeError(f"Unsupported type: {type(item)}")
    
    return to_roman(total, extended=extended)


def roman_list(romans: List[Union[str, 'RomanNumeral', int]], extended: bool = False) -> str:
    """
    将罗马数字列表格式化为带编号的字符串
    
    Args:
        romans: 罗马数字列表
        extended: 是否使用扩展罗马数字
    
    Returns:
        格式化的字符串
    
    Examples:
        >>> print(roman_list(['I', 'II', 'III']))
        I. 第一项
        II. 第二项
        III. 第三项
    """
    chinese_nums = ['第一项', '第二项', '第三项', '第四项', '第五项',
                    '第六项', '第七项', '第八项', '第九项', '第十项']
    
    lines = []
    for i, item in enumerate(romans):
        if isinstance(item, RomanNumeral):
            r = item.roman
        elif isinstance(item, int):
            r = to_roman(item, extended=extended)
        else:
            r = item
        
        desc = chinese_nums[i] if i < len(chinese_nums) else f"第{i+1}项"
        lines.append(f"{r}. {desc}")
    
    return '\n'.join(lines)


class RomanNumeralBuilder:
    """
    罗马数字构建器，支持链式调用
    
    Examples:
        >>> builder = RomanNumeralBuilder()
        >>> builder.add(10).add(5).build()
        'XV'
        >>> builder.reset().from_int(1994).build()
        'MCMXCIV'
    """
    
    def __init__(self, extended: bool = False):
        self._extended = extended
        self._value = 0
    
    def reset(self) -> 'RomanNumeralBuilder':
        """重置累加值为0"""
        self._value = 0
        return self
    
    def add(self, value: Union[int, str, RomanNumeral]) -> 'RomanNumeralBuilder':
        """添加一个值到累加器"""
        if isinstance(value, RomanNumeral):
            self._value += value.arabic
        elif isinstance(value, int):
            self._value += value
        elif isinstance(value, str):
            self._value += from_roman(value, extended=self._extended)
        else:
            raise TypeError(f"Unsupported type: {type(value)}")
        return self
    
    def subtract(self, value: Union[int, str, RomanNumeral]) -> 'RomanNumeralBuilder':
        """从累加器减去一个值"""
        if isinstance(value, RomanNumeral):
            self._value -= value.arabic
        elif isinstance(value, int):
            self._value -= value
        elif isinstance(value, str):
            self._value -= from_roman(value, extended=self._extended)
        else:
            raise TypeError(f"Unsupported type: {type(value)}")
        
        if self._value < 1:
            raise OutOfRangeError("Value cannot be less than 1")
        return self
    
    def multiply(self, value: int) -> 'RomanNumeralBuilder':
        """将累加器乘以一个整数"""
        self._value *= value
        return self
    
    def divide(self, value: int) -> 'RomanNumeralBuilder':
        """将累加器除以一个整数（整数除法）"""
        self._value //= value
        if self._value < 1:
            raise OutOfRangeError("Value cannot be less than 1")
        return self
    
    def from_int(self, value: int) -> 'RomanNumeralBuilder':
        """从整数设置值"""
        self._value = value
        return self
    
    def from_roman(self, roman: str) -> 'RomanNumeralBuilder':
        """从罗马数字字符串设置值"""
        self._value = from_roman(roman, extended=self._extended)
        return self
    
    def build(self) -> str:
        """构建并返回罗马数字字符串"""
        return to_roman(self._value, extended=self._extended)
    
    def build_numeral(self) -> RomanNumeral:
        """构建并返回RomanNumeral对象"""
        return RomanNumeral(self._value, extended=self._extended)


# 便捷函数
def roman(num: Union[int, str], extended: bool = False) -> RomanNumeral:
    """
    创建罗马数字对象的便捷函数
    
    Args:
        num: 整数或罗马数字字符串
        extended: 是否使用扩展罗马数字
    
    Returns:
        RomanNumeral对象
    
    Examples:
        >>> roman(10) + roman('V')
        RomanNumeral('XV')
    """
    return RomanNumeral(num, extended=extended)


# 导出的公共API
__all__ = [
    'to_roman',
    'from_roman',
    'is_valid_roman',
    'validate_roman',
    'RomanNumeral',
    'RomanNumeralError',
    'InvalidRomanNumeralError',
    'OutOfRangeError',
    'roman_sort',
    'roman_range',
    'roman_sum',
    'roman_list',
    'RomanNumeralBuilder',
    'roman',
]