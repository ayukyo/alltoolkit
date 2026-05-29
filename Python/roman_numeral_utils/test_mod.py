"""
罗马数字工具测试套件
"""

import pytest
from roman_numeral_utils.mod import (
    to_roman,
    from_roman,
    is_valid_roman,
    validate_roman,
    RomanNumeral,
    RomanNumeralError,
    InvalidRomanNumeralError,
    OutOfRangeError,
    roman_sort,
    roman_range,
    roman_sum,
    roman_list,
    RomanNumeralBuilder,
    roman
)


class TestToRoman:
    """测试阿拉伯数字转罗马数字"""
    
    def test_basic_conversions(self):
        """测试基本转换"""
        assert to_roman(1) == 'I'
        assert to_roman(5) == 'V'
        assert to_roman(10) == 'X'
        assert to_roman(50) == 'L'
        assert to_roman(100) == 'C'
        assert to_roman(500) == 'D'
        assert to_roman(1000) == 'M'
    
    def test_subtractive_notation(self):
        """测试减法表示法"""
        assert to_roman(4) == 'IV'
        assert to_roman(9) == 'IX'
        assert to_roman(40) == 'XL'
        assert to_roman(90) == 'XC'
        assert to_roman(400) == 'CD'
        assert to_roman(900) == 'CM'
    
    def test_complex_numbers(self):
        """测试复杂数字"""
        assert to_roman(1994) == 'MCMXCIV'
        assert to_roman(2023) == 'MMXXIII'
        assert to_roman(3999) == 'MMMCMXCIX'
        assert to_roman(58) == 'LVIII'
        assert to_roman(1776) == 'MDCCLXXVI'
        assert to_roman(1954) == 'MCMLIV'
    
    def test_lower_bound(self):
        """测试下限"""
        with pytest.raises(OutOfRangeError):
            to_roman(0)
        with pytest.raises(OutOfRangeError):
            to_roman(-1)
    
    def test_upper_bound(self):
        """测试上限"""
        with pytest.raises(OutOfRangeError):
            to_roman(4000)
        with pytest.raises(OutOfRangeError):
            to_roman(10000)
    
    def test_extended_range(self):
        """测试扩展范围"""
        assert to_roman(4000, extended=True) == '(IV)'
        assert to_roman(5000, extended=True) == '(V)'
        assert to_roman(10000, extended=True) == '(X)'
        assert to_roman(100000, extended=True) == '(C)'
        assert to_roman(1000000, extended=True) == '(M)'
        assert to_roman(3999999, extended=True) == '(M)(M)(M)(CM)(XC)(IX)CMXCIX'
    
    def test_type_error(self):
        """测试类型错误"""
        with pytest.raises(TypeError):
            to_roman(1.5)
        with pytest.raises(TypeError):
            to_roman("10")


class TestFromRoman:
    """测试罗马数字转阿拉伯数字"""
    
    def test_basic_conversions(self):
        """测试基本转换"""
        assert from_roman('I') == 1
        assert from_roman('V') == 5
        assert from_roman('X') == 10
        assert from_roman('L') == 50
        assert from_roman('C') == 100
        assert from_roman('D') == 500
        assert from_roman('M') == 1000
    
    def test_subtractive_notation(self):
        """测试减法表示法"""
        assert from_roman('IV') == 4
        assert from_roman('IX') == 9
        assert from_roman('XL') == 40
        assert from_roman('XC') == 90
        assert from_roman('CD') == 400
        assert from_roman('CM') == 900
    
    def test_complex_numbers(self):
        """测试复杂数字"""
        assert from_roman('MCMXCIV') == 1994
        assert from_roman('MMXXIII') == 2023
        assert from_roman('MMMCMXCIX') == 3999
        assert from_roman('LVIII') == 58
        assert from_roman('MDCCLXXVI') == 1776
        assert from_roman('MCMLIV') == 1954
    
    def test_case_insensitive(self):
        """测试大小写不敏感"""
        assert from_roman('mcmxciv') == 1994
        assert from_roman('McmXcIv') == 1994
    
    def test_whitespace_handling(self):
        """测试空白处理"""
        assert from_roman('  MCMXCIV  ') == 1994
    
    def test_invalid_format(self):
        """测试无效格式"""
        with pytest.raises(InvalidRomanNumeralError):
            from_roman('IIII')  # 应该是 IV
        with pytest.raises(InvalidRomanNumeralError):
            from_roman('VV')  # 应该是 X
        with pytest.raises(InvalidRomanNumeralError):
            from_roman('IC')  # 无效
        with pytest.raises(InvalidRomanNumeralError):
            from_roman('ABC')  # 无效字符
    
    def test_empty_string(self):
        """测试空字符串"""
        with pytest.raises(InvalidRomanNumeralError):
            from_roman('')
    
    def test_type_error(self):
        """测试类型错误"""
        with pytest.raises(TypeError):
            from_roman(10)
        with pytest.raises(TypeError):
            from_roman(None)
    
    def test_extended_roman(self):
        """测试扩展罗马数字"""
        assert from_roman('(IV)', extended=True) == 4000
        assert from_roman('(V)', extended=True) == 5000
        assert from_roman('(X)', extended=True) == 10000


class TestIsValidRoman:
    """测试罗马数字验证"""
    
    def test_valid_numerals(self):
        """测试有效的罗马数字"""
        assert is_valid_roman('I') is True
        assert is_valid_roman('IV') is True
        assert is_valid_roman('MCMXCIV') is True
        assert is_valid_roman('MMMCMXCIX') is True
    
    def test_invalid_numerals(self):
        """测试无效的罗马数字"""
        assert is_valid_roman('IIII') is False
        assert is_valid_roman('ABC') is False
        assert is_valid_roman('') is False
        assert is_valid_roman('VV') is False
    
    def test_type_handling(self):
        """测试类型处理"""
        assert is_valid_roman(10) is False
        assert is_valid_roman(None) is False


class TestValidateRoman:
    """测试罗马数字验证（详细版本）"""
    
    def test_valid_numerals(self):
        """测试有效罗马数字"""
        valid, msg = validate_roman('MCMXCIV')
        assert valid is True
        assert '1994' in msg
    
    def test_invalid_numerals(self):
        """测试无效罗马数字"""
        valid, msg = validate_roman('ABC')
        assert valid is False
        assert 'Invalid' in msg


class TestRomanNumeral:
    """测试罗马数字类"""
    
    def test_from_int(self):
        """测试从整数创建"""
        r = RomanNumeral(10)
        assert r.arabic == 10
        assert r.roman == 'X'
    
    def test_from_string(self):
        """测试从字符串创建"""
        r = RomanNumeral('X')
        assert r.arabic == 10
        assert r.roman == 'X'
    
    def test_addition(self):
        """测试加法"""
        r1 = RomanNumeral(10)
        r2 = RomanNumeral(5)
        result = r1 + r2
        assert result.arabic == 15
        assert result.roman == 'XV'
    
    def test_addition_with_int(self):
        """测试与整数相加"""
        r = RomanNumeral(10)
        result = r + 5
        assert result.arabic == 15
    
    def test_subtraction(self):
        """测试减法"""
        r1 = RomanNumeral(10)
        r2 = RomanNumeral(5)
        result = r1 - r2
        assert result.arabic == 5
    
    def test_subtraction_error(self):
        """测试减法结果为零或负数"""
        r1 = RomanNumeral(5)
        r2 = RomanNumeral(10)
        with pytest.raises(OutOfRangeError):
            r1 - r2
    
    def test_multiplication(self):
        """测试乘法"""
        r1 = RomanNumeral(10)
        r2 = RomanNumeral(5)
        result = r1 * r2
        assert result.arabic == 50
    
    def test_division(self):
        """测试除法"""
        r1 = RomanNumeral(10)
        r2 = RomanNumeral(5)
        result = r1 / r2
        assert result.arabic == 2
    
    def test_modulo(self):
        """测试取模"""
        r1 = RomanNumeral(10)
        r2 = RomanNumeral(3)
        result = r1 % r2
        assert result.arabic == 1
    
    def test_power(self):
        """测试幂运算"""
        r = RomanNumeral(2)
        result = r ** 3
        assert result.arabic == 8
    
    def test_comparison(self):
        """测试比较"""
        r1 = RomanNumeral(10)
        r2 = RomanNumeral(5)
        assert r1 > r2
        assert r1 >= r2
        assert r2 < r1
        assert r2 <= r1
        assert r1 != r2
    
    def test_equality(self):
        """测试相等"""
        r1 = RomanNumeral(10)
        r2 = RomanNumeral(10)
        assert r1 == r2
        assert r1 == 10
        assert r1 == 'X'
    
    def test_str_representation(self):
        """测试字符串表示"""
        r = RomanNumeral(1994)
        assert str(r) == 'MCMXCIV'
        assert repr(r) == "RomanNumeral('MCMXCIV')"
    
    def test_int_conversion(self):
        """测试整数转换"""
        r = RomanNumeral(1994)
        assert int(r) == 1994
    
    def test_hash(self):
        """测试哈希"""
        r1 = RomanNumeral(10)
        r2 = RomanNumeral(10)
        assert hash(r1) == hash(r2)
        # 可以用作字典键
        d = {r1: 'value'}
        assert d[r2] == 'value'


class TestRomanSort:
    """测试罗马数字排序"""
    
    def test_ascending_sort(self):
        """测试升序排序"""
        result = roman_sort(['III', 'I', 'II'])
        assert result == ['I', 'II', 'III']
    
    def test_descending_sort(self):
        """测试降序排序"""
        result = roman_sort(['I', 'II', 'III'], reverse=True)
        assert result == ['III', 'II', 'I']
    
    def test_mixed_types(self):
        """测试混合类型"""
        result = roman_sort([10, 'V', RomanNumeral(1)])
        assert result == ['I', 'V', 'X']


class TestRomanRange:
    """测试罗马数字范围生成"""
    
    def test_basic_range(self):
        """测试基本范围"""
        result = roman_range(1, 5)
        assert result == ['I', 'II', 'III', 'IV', 'V']
    
    def test_range_with_step(self):
        """测试带步长的范围"""
        result = roman_range(1, 10, step=2)
        assert result == ['I', 'III', 'V', 'VII', 'IX']
    
    def test_out_of_range(self):
        """测试超出范围"""
        with pytest.raises(OutOfRangeError):
            roman_range(0, 10)
        with pytest.raises(OutOfRangeError):
            roman_range(1, 5000)


class TestRomanSum:
    """测试罗马数字求和"""
    
    def test_basic_sum(self):
        """测试基本求和"""
        result = roman_sum(['X', 'V', 'I'])
        assert result == 'XVI'
    
    def test_mixed_types_sum(self):
        """测试混合类型求和"""
        result = roman_sum([10, 'V', RomanNumeral(1)])
        assert result == 'XVI'


class TestRomanList:
    """测试罗马数字列表格式化"""
    
    def test_basic_list(self):
        """测试基本列表"""
        result = roman_list(['I', 'II', 'III'])
        lines = result.split('\n')
        assert 'I.' in lines[0]
        assert 'II.' in lines[1]
        assert 'III.' in lines[2]


class TestRomanNumeralBuilder:
    """测试罗马数字构建器"""
    
    def test_basic_build(self):
        """测试基本构建"""
        builder = RomanNumeralBuilder()
        result = builder.from_int(15).build()
        assert result == 'XV'
    
    def test_add_operations(self):
        """测试添加操作"""
        builder = RomanNumeralBuilder()
        result = builder.add(10).add('V').build()
        assert result == 'XV'
    
    def test_subtract_operations(self):
        """测试减法操作"""
        builder = RomanNumeralBuilder()
        result = builder.from_int(20).subtract(5).build()
        assert result == 'XV'
    
    def test_multiply_operations(self):
        """测试乘法操作"""
        builder = RomanNumeralBuilder()
        result = builder.from_int(5).multiply(3).build()
        assert result == 'XV'
    
    def test_divide_operations(self):
        """测试除法操作"""
        builder = RomanNumeralBuilder()
        result = builder.from_int(15).divide(3).build()
        assert result == 'V'
    
    def test_reset(self):
        """测试重置"""
        builder = RomanNumeralBuilder()
        result = builder.from_int(100).reset().from_int(5).build()
        assert result == 'V'
    
    def test_build_numeral(self):
        """测试构建RomanNumeral对象"""
        builder = RomanNumeralBuilder()
        result = builder.from_int(10).build_numeral()
        assert isinstance(result, RomanNumeral)
        assert result.arabic == 10


class TestConvenienceFunction:
    """测试便捷函数"""
    
    def test_roman_function(self):
        """测试roman便捷函数"""
        r1 = roman(10)
        r2 = roman('V')
        result = r1 + r2
        assert result.arabic == 15


class TestRoundTrip:
    """测试往返转换"""
    
    @pytest.mark.parametrize("num", [1, 4, 9, 10, 40, 50, 90, 100, 400, 500, 
                                      900, 1000, 1994, 2023, 3999])
    def test_round_trip(self, num):
        """测试所有基本数字的往返转换"""
        roman_str = to_roman(num)
        result = from_roman(roman_str)
        assert result == num


if __name__ == '__main__':
    pytest.main([__file__, '-v'])