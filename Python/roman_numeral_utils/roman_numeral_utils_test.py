"""
Roman Numeral Utils - 测试套件

测试覆盖：
- 基础转换功能
- 边界值测试
- 错误处理
- 批量操作
- 运算功能
- 文本搜索
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from roman_numeral_utils.mod import (
    to_roman, from_roman, convert,
    is_valid_roman, is_roman_numeral,
    batch_to_roman, batch_from_roman, get_roman_range,
    compare_roman, add_roman, subtract_roman, multiply_roman, divide_roman,
    find_roman_in_text, normalize_roman, roman_to_ordinal,
    get_roman_value_table, explain_roman,
    InvalidRomanError, OutOfRangeError, RomanNumeralError,
    MIN_VALUE, MAX_VALUE
)


class TestResult:
    """测试结果收集器"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def assert_equal(self, actual, expected, msg=""):
        if actual == expected:
            self.passed += 1
            return True
        else:
            self.failed += 1
            error_msg = f"期望 {expected!r}, 得到 {actual!r}"
            if msg:
                error_msg = f"{msg}: {error_msg}"
            self.errors.append(error_msg)
            return False
    
    def assert_true(self, value, msg=""):
        return self.assert_equal(value, True, msg)
    
    def assert_false(self, value, msg=""):
        return self.assert_equal(value, False, msg)
    
    def assert_raises(self, exc_type, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
            self.failed += 1
            self.errors.append(f"期望抛出 {exc_type.__name__}，但没有抛出异常")
            return False
        except exc_type:
            self.passed += 1
            return True
        except Exception as e:
            self.failed += 1
            self.errors.append(f"期望抛出 {exc_type.__name__}，但得到 {type(e).__name__}: {e}")
            return False
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"测试结果: {self.passed}/{total} 通过")
        print(f"{'='*60}")
        if self.errors:
            print("\n失败的测试:")
            for i, err in enumerate(self.errors, 1):
                print(f"  {i}. {err}")
        return self.failed == 0


def test_to_roman_basic(r):
    """测试基础转换"""
    print("\n[test_to_roman_basic]")
    
    # 基本数字
    r.assert_equal(to_roman(1), 'I', "1 -> I")
    r.assert_equal(to_roman(2), 'II', "2 -> II")
    r.assert_equal(to_roman(3), 'III', "3 -> III")
    r.assert_equal(to_roman(4), 'IV', "4 -> IV")
    r.assert_equal(to_roman(5), 'V', "5 -> V")
    r.assert_equal(to_roman(6), 'VI', "6 -> VI")
    r.assert_equal(to_roman(9), 'IX', "9 -> IX")
    r.assert_equal(to_roman(10), 'X', "10 -> X")
    
    # 复杂数字
    r.assert_equal(to_roman(40), 'XL', "40 -> XL")
    r.assert_equal(to_roman(50), 'L', "50 -> L")
    r.assert_equal(to_roman(90), 'XC', "90 -> XC")
    r.assert_equal(to_roman(100), 'C', "100 -> C")
    r.assert_equal(to_roman(400), 'CD', "400 -> CD")
    r.assert_equal(to_roman(500), 'D', "500 -> D")
    r.assert_equal(to_roman(900), 'CM', "900 -> CM")
    r.assert_equal(to_roman(1000), 'M', "1000 -> M")


def test_to_roman_special(r):
    """测试特殊值"""
    print("\n[test_to_roman_special]")
    
    # 年份
    r.assert_equal(to_roman(2024), 'MMXXIV', "2024 -> MMXXIV")
    r.assert_equal(to_roman(1999), 'MCMXCIX', "1999 -> MCMXCIX")
    r.assert_equal(to_roman(2023), 'MMXXIII', "2023 -> MMXXIII")
    
    # 边界值
    r.assert_equal(to_roman(MIN_VALUE), 'I', f"MIN_VALUE({MIN_VALUE}) -> I")
    r.assert_equal(to_roman(MAX_VALUE), 'MMMCMXCIX', f"MAX_VALUE({MAX_VALUE}) -> MMMCMXCIX")


def test_to_roman_errors(r):
    """测试错误处理"""
    print("\n[test_to_roman_errors]")
    
    # 超出范围
    r.assert_raises(OutOfRangeError, to_roman, 0)
    r.assert_raises(OutOfRangeError, to_roman, -1)
    r.assert_raises(OutOfRangeError, to_roman, 4000)
    r.assert_raises(OutOfRangeError, to_roman, 10000)
    
    # 类型错误
    r.assert_raises(TypeError, to_roman, "X")
    r.assert_raises(TypeError, to_roman, 1.5)
    r.assert_raises(TypeError, to_roman, None)


def test_from_roman_basic(r):
    """测试罗马数字转阿拉伯数字"""
    print("\n[test_from_roman_basic]")
    
    # 基本转换
    r.assert_equal(from_roman('I'), 1, "I -> 1")
    r.assert_equal(from_roman('II'), 2, "II -> 2")
    r.assert_equal(from_roman('III'), 3, "III -> 3")
    r.assert_equal(from_roman('IV'), 4, "IV -> 4")
    r.assert_equal(from_roman('V'), 5, "V -> 5")
    r.assert_equal(from_roman('VI'), 6, "VI -> 6")
    r.assert_equal(from_roman('IX'), 9, "IX -> 9")
    r.assert_equal(from_roman('X'), 10, "X -> 10")
    
    # 复杂转换
    r.assert_equal(from_roman('XL'), 40, "XL -> 40")
    r.assert_equal(from_roman('XC'), 90, "XC -> 90")
    r.assert_equal(from_roman('CD'), 400, "CD -> 400")
    r.assert_equal(from_roman('CM'), 900, "CM -> 900")
    
    # 年份
    r.assert_equal(from_roman('MMXXIV'), 2024, "MMXXIV -> 2024")
    r.assert_equal(from_roman('MCMXCIX'), 1999, "MCMXCIX -> 1999")
    r.assert_equal(from_roman('MMMCMXCIX'), 3999, "MMMCMXCIX -> 3999")


def test_from_roman_case(r):
    """测试大小写处理"""
    print("\n[test_from_roman_case]")
    
    r.assert_equal(from_roman('i'), 1, "小写 i")
    r.assert_equal(from_roman('iv'), 4, "小写 iv")
    r.assert_equal(from_roman('MmXxIv'), 2024, "混合大小写")
    r.assert_equal(from_roman('  X  '), 10, "带空格")


def test_from_roman_errors(r):
    """测试错误处理"""
    print("\n[test_from_roman_errors]")
    
    # 无效字符
    r.assert_raises(InvalidRomanError, from_roman, 'ABC')
    r.assert_raises(InvalidRomanError, from_roman, '123')
    r.assert_raises(InvalidRomanError, from_roman, 'XIZ')  # Z不是罗马数字
    
    # 无效格式
    r.assert_raises(InvalidRomanError, from_roman, 'IIII', strict=True)
    r.assert_raises(InvalidRomanError, from_roman, 'VV', strict=True)
    r.assert_raises(InvalidRomanError, from_roman, 'VX', strict=True)
    
    # 空值
    r.assert_raises(InvalidRomanError, from_roman, '')
    r.assert_raises(TypeError, from_roman, 123)
    r.assert_raises(TypeError, from_roman, None)


def test_is_valid_roman(r):
    """测试罗马数字验证"""
    print("\n[test_is_valid_roman]")
    
    # 有效值
    r.assert_true(is_valid_roman('I'), "I 有效")
    r.assert_true(is_valid_roman('IV'), "IV 有效")
    r.assert_true(is_valid_roman('XIX'), "XIX 有效")
    r.assert_true(is_valid_roman('MMXXIV'), "MMXXIV 有效")
    r.assert_true(is_valid_roman('MMMCMXCIX'), "MMMCMXCIX 有效")
    
    # 无效值
    r.assert_false(is_valid_roman('IIII'), "IIII 无效（4个I）")
    r.assert_false(is_valid_roman('VV'), "VV 无效")
    r.assert_false(is_valid_roman('VX'), "VX 无效")
    r.assert_false(is_valid_roman(''), "空字符串无效")
    r.assert_false(is_valid_roman('ABC'), "ABC 无效")
    r.assert_false(is_valid_roman('123'), "123 无效")
    r.assert_false(is_valid_roman(None), "None 无效")


def test_is_roman_numeral(r):
    """测试宽松验证"""
    print("\n[test_is_roman_numeral]")
    
    r.assert_true(is_roman_numeral('I'), "I 可能是")
    r.assert_true(is_roman_numeral('IIII'), "IIII 可能是（宽松检查）")
    r.assert_true(is_roman_numeral('MMXX'), "MMXX 可能是")
    r.assert_false(is_roman_numeral('ABC'), "ABC 不是")
    r.assert_false(is_roman_numeral(''), "空字符串不是")


def test_convert(r):
    """测试智能转换"""
    print("\n[test_convert]")
    
    # 整数转罗马
    r.assert_equal(convert(1), 'I', "convert(1)")
    r.assert_equal(convert(2024), 'MMXXIV', "convert(2024)")
    
    # 罗马转整数
    r.assert_equal(convert('I'), 1, "convert('I')")
    r.assert_equal(convert('MMXXIV'), 2024, "convert('MMXXIV')")
    
    # 类型错误
    r.assert_raises(TypeError, convert, 1.5)
    r.assert_raises(TypeError, convert, [])


def test_batch_operations(r):
    """测试批量操作"""
    print("\n[test_batch_operations]")
    
    # 批量转罗马
    result = batch_to_roman([1, 2, 3, 4, 5])
    r.assert_equal(len(result), 5, "批量转罗马数量")
    r.assert_equal(result[0], (1, 'I', None), "batch 1 -> I")
    r.assert_equal(result[4], (5, 'V', None), "batch 5 -> V")
    
    # 批量转阿拉伯
    result = batch_from_roman(['I', 'II', 'III'])
    r.assert_equal(len(result), 3, "批量转阿拉伯数量")
    r.assert_equal(result[0], ('I', 1, None), "batch I -> 1")
    r.assert_equal(result[2], ('III', 3, None), "batch III -> 3")
    
    # 跳过无效
    result = batch_to_roman([1, 0, 3], skip_invalid=True)
    r.assert_equal(result[0], (1, 'I', None), "skip_invalid 第一个")
    r.assert_equal(result[1][0], 0, "skip_invalid 第二个原值")
    r.assert_equal(result[1][1], None, "skip_invalid 第二个结果为None")
    r.assert_equal(result[2], (3, 'III', None), "skip_invalid 第三个")


def test_get_roman_range(r):
    """测试范围生成"""
    print("\n[test_get_roman_range]")
    
    result = get_roman_range(1, 5)
    r.assert_equal(len(result), 5, "范围长度")
    r.assert_equal(result[0], (1, 'I'), "范围第一项")
    r.assert_equal(result[4], (5, 'V'), "范围最后一项")
    
    # 边界截断
    result = get_roman_range(0, 4000)
    r.assert_equal(result[0][0], MIN_VALUE, "最小值截断")
    r.assert_equal(result[-1][0], MAX_VALUE, "最大值截断")


def test_compare_roman(r):
    """测试比较功能"""
    print("\n[test_compare_roman]")
    
    r.assert_equal(compare_roman('X', 'V'), 5, "X > V")
    r.assert_equal(compare_roman('V', 'X'), -5, "V < X")
    r.assert_equal(compare_roman('X', 'X'), 0, "X == X")
    r.assert_equal(compare_roman('M', 'I'), 999, "M > I (999)")


def test_arithmetic_operations(r):
    """测试算术运算"""
    print("\n[test_arithmetic_operations]")
    
    # 加法
    r.assert_equal(add_roman('X', 'V'), 'XV', "X + V = XV")
    r.assert_equal(add_roman('IV', 'I'), 'V', "IV + I = V")
    r.assert_equal(add_roman('I', 'I'), 'II', "I + I = II")
    
    # 减法
    r.assert_equal(subtract_roman('X', 'V'), 'V', "X - V = V")
    r.assert_equal(subtract_roman('V', 'I'), 'IV', "V - I = IV")
    
    # 乘法
    r.assert_equal(multiply_roman('X', 'X'), 'C', "X * X = C")
    r.assert_equal(multiply_roman('V', 'II'), 'X', "V * II = X")
    
    # 除法
    r.assert_equal(divide_roman('X', 'II'), 'V', "X / II = V")
    
    # 除法带余数
    quotient, remainder = divide_roman('X', 'III', remainder=True)
    r.assert_equal(quotient, 'III', "X / III 商 = III")
    r.assert_equal(remainder, 'I', "X / III 余 = I")
    
    # 减法错误（结果<=0）
    r.assert_raises(OutOfRangeError, subtract_roman, 'I', 'I')
    r.assert_raises(OutOfRangeError, subtract_roman, 'V', 'X')


def test_find_roman_in_text(r):
    """测试文本搜索"""
    print("\n[test_find_roman_in_text]")
    
    text = "Chapter XIV continues from Chapter XIII"
    result = find_roman_in_text(text)
    r.assert_equal(len(result), 2, "找到2个罗马数字")
    r.assert_equal(result[0], ('XIV', 8, 11), "第一个XIV")
    r.assert_equal(result[1], ('XIII', 35, 39), "第二个XIII")
    
    # 无罗马数字
    result = find_roman_in_text("Hello World")
    r.assert_equal(len(result), 0, "无罗马数字")
    
    # 混合文本
    text = "King Henry VIII had 6 wives"
    result = find_roman_in_text(text)
    r.assert_equal(len(result), 1, "找到VIII")
    r.assert_equal(result[0][0], 'VIII', "找到VIII")


def test_normalize_roman(r):
    """测试规范化"""
    print("\n[test_normalize_roman]")
    
    # 已经是标准形式
    r.assert_equal(normalize_roman('IV'), 'IV', "IV 标准形式")
    r.assert_equal(normalize_roman('IX'), 'IX', "IX 标准形式")
    
    # 非标准形式（宽松模式接受，然后规范化）
    r.assert_equal(normalize_roman('iiii'), 'IV', "iiii -> IV")
    r.assert_equal(normalize_roman('viiii'), 'IX', "viiii -> IX")


def test_roman_to_ordinal(r):
    """测试序数词转换"""
    print("\n[test_roman_to_ordinal]")
    
    r.assert_equal(roman_to_ordinal('I'), '1st', "I -> 1st")
    r.assert_equal(roman_to_ordinal('II'), '2nd', "II -> 2nd")
    r.assert_equal(roman_to_ordinal('III'), '3rd', "III -> 3rd")
    r.assert_equal(roman_to_ordinal('IV'), '4th', "IV -> 4th")
    r.assert_equal(roman_to_ordinal('XI'), '11th', "XI -> 11th")
    r.assert_equal(roman_to_ordinal('XII'), '12th', "XII -> 12th")
    r.assert_equal(roman_to_ordinal('XIII'), '13th', "XIII -> 13th")
    r.assert_equal(roman_to_ordinal('XXI'), '21st', "XXI -> 21st")


def test_get_roman_value_table(r):
    """测试值对照表"""
    print("\n[test_get_roman_value_table]")
    
    table = get_roman_value_table()
    r.assert_equal(len(table), 7, "7个基本符号")
    r.assert_true(('I', 1) in table, "包含 I")
    r.assert_true(('V', 5) in table, "包含 V")
    r.assert_true(('M', 1000) in table, "包含 M")


def test_explain_roman(r):
    """测试罗马数字解释"""
    print("\n[test_explain_roman]")
    
    result = explain_roman('XIV')
    r.assert_equal(len(result), 3, "XIV 分解为2部分+总计")
    r.assert_equal(result[0], ('X', 10, '加'), "X = 10")
    r.assert_equal(result[1], ('IV', 4, '减法组合'), "IV = 4")
    r.assert_equal(result[2][0], '总计', "最后一项是总计")
    r.assert_equal(result[2][1], 14, "总计 = 14")


def test_roundtrip(r):
    """测试往返转换"""
    print("\n[test_roundtrip]")
    
    # 测试所有值
    for i in range(1, 100):
        roman = to_roman(i)
        back = from_roman(roman)
        r.assert_equal(back, i, f"往返测试 {i} -> {roman} -> {back}")
    
    # 边界值
    for val in [1, 10, 100, 500, 1000, 3999]:
        roman = to_roman(val)
        back = from_roman(roman)
        r.assert_equal(back, val, f"边界往返 {val}")


def test_edge_cases(r):
    """测试边界情况"""
    print("\n[test_edge_cases]")
    
    # 最小值
    r.assert_equal(to_roman(1), 'I', "最小值 1")
    r.assert_equal(from_roman('I'), 1, "最小罗马数字 I")
    
    # 最大值
    r.assert_equal(to_roman(3999), 'MMMCMXCIX', "最大值 3999")
    r.assert_equal(from_roman('MMMCMXCIX'), 3999, "最大罗马数字")
    
    # 特殊组合
    r.assert_equal(to_roman(4), 'IV', "4 = IV")
    r.assert_equal(to_roman(9), 'IX', "9 = IX")
    r.assert_equal(to_roman(40), 'XL', "40 = XL")
    r.assert_equal(to_roman(90), 'XC', "90 = XC")
    r.assert_equal(to_roman(400), 'CD', "400 = CD")
    r.assert_equal(to_roman(900), 'CM', "900 = CM")


def run_all_tests():
    """运行所有测试"""
    r = TestResult()
    
    print("="*60)
    print("Roman Numeral Utils 测试套件")
    print("="*60)
    
    test_to_roman_basic(r)
    test_to_roman_special(r)
    test_to_roman_errors(r)
    test_from_roman_basic(r)
    test_from_roman_case(r)
    test_from_roman_errors(r)
    test_is_valid_roman(r)
    test_is_roman_numeral(r)
    test_convert(r)
    test_batch_operations(r)
    test_get_roman_range(r)
    test_compare_roman(r)
    test_arithmetic_operations(r)
    test_find_roman_in_text(r)
    test_normalize_roman(r)
    test_roman_to_ordinal(r)
    test_get_roman_value_table(r)
    test_explain_roman(r)
    test_roundtrip(r)
    test_edge_cases(r)
    
    return r.summary()


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)