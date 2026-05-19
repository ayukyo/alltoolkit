"""
Roman Numeral Utils - 基本使用示例

演示罗马数字转换工具的基本用法。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    int_to_roman,
    roman_to_int,
    is_valid_roman,
    roman_add,
    roman_subtract,
    roman_multiply,
    roman_divide,
    roman_compare,
    get_roman_info,
    find_roman_range,
    COMMON_ROMANS,
)


def print_section(title):
    """打印分节标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def main():
    print("\n🏛️  Roman Numeral Utils - 罗马数字转换工具演示 🏛️")
    
    # 1. 基本转换
    print_section("1. 基本转换")
    
    numbers = [1, 4, 9, 49, 99, 2024, 3999]
    print("\n阿拉伯数字 → 罗马数字:")
    for num in numbers:
        roman = int_to_roman(num)
        print(f"  {num:4d} → {roman}")
    
    romans = ['I', 'IV', 'IX', 'XLIX', 'XCIX', 'MMXXIV', 'MMMCMXCIX']
    print("\n罗马数字 → 阿拉伯数字:")
    for roman in romans:
        num = roman_to_int(roman)
        print(f"  {roman:12s} → {num}")
    
    # 2. 验证功能
    print_section("2. 验证功能")
    
    test_cases = ['IV', 'IIII', 'VV', 'MMXXIV', 'ABC', '123', 'mcmlxxxiv']
    print("\n罗马数字验证:")
    for test in test_cases:
        valid = is_valid_roman(test)
        status = "✅ 有效" if valid else "❌ 无效"
        print(f"  '{test:12s}' → {status}")
    
    # 3. 算术运算
    print_section("3. 算术运算")
    
    print("\n加法:")
    additions = [('I', 'I'), ('IV', 'VI'), ('X', 'V'), ('C', 'D')]
    for a, b in additions:
        result = roman_add(a, b)
        va, vb = roman_to_int(a), roman_to_int(b)
        vr = roman_to_int(result)
        print(f"  {a} + {b} = {result}  ({va} + {vb} = {vr})")
    
    print("\n减法:")
    subtractions = [('V', 'I'), ('X', 'V'), ('X', 'I'), ('C', 'X')]
    for a, b in subtractions:
        result = roman_subtract(a, b)
        va, vb = roman_to_int(a), roman_to_int(b)
        vr = roman_to_int(result)
        print(f"  {a} - {b} = {result}  ({va} - {vb} = {vr})")
    
    print("\n乘法:")
    multiplications = [('V', 'II'), ('X', 'X'), ('II', 'II'), ('V', 'V')]
    for a, b in multiplications:
        result = roman_multiply(a, b)
        va, vb = roman_to_int(a), roman_to_int(b)
        vr = roman_to_int(result)
        print(f"  {a} × {b} = {result}  ({va} × {vb} = {vr})")
    
    print("\n除法:")
    divisions = [('X', 'II'), ('X', 'III'), ('C', 'X'), ('XXV', 'V')]
    for a, b in divisions:
        quotient, remainder = roman_divide(a, b)
        va, vb = roman_to_int(a), roman_to_int(b)
        vq = roman_to_int(quotient)
        vr_msg = f"余 {roman_to_int(remainder)}" if remainder else ""
        print(f"  {a} ÷ {b} = {quotient} {vr_msg}  ({va} ÷ {vb} = {vq})")
    
    # 4. 比较功能
    print_section("4. 比较功能")
    
    print("\n大小比较:")
    pairs = [('I', 'V'), ('X', 'V'), ('V', 'V'), ('MMXXIV', 'MMXXV')]
    for a, b in pairs:
        result = roman_compare(a, b)
        if result < 0:
            symbol = '<'
        elif result > 0:
            symbol = '>'
        else:
            symbol = '='
        print(f"  {a} {symbol} {b}")
    
    # 5. 详细信息
    print_section("5. 详细信息")
    
    examples = ['MMXXIV', 'MCMLXXXIV', 'IV', 'MMMCMXCIX']
    print("\n罗马数字信息:")
    for roman in examples:
        info = get_roman_info(roman)
        print(f"\n  原始: {info['original']}")
        print(f"  数值: {info['value']}")
        print(f"  有效: {info['valid']}")
        print(f"  长度: {info['length']}")
        print(f"  组成: {' + '.join(info['components'])}")
    
    # 6. 批量生成
    print_section("6. 批量生成")
    
    print("\n1-20 的罗马数字:")
    for value, roman in find_roman_range(1, 20):
        print(f"  {value:2d}: {roman:6s}", end='')
        if value % 5 == 0:
            print()  # 每5个换行
    
    # 7. 预定义常见数字
    print_section("7. 预定义常见数字")
    
    print("\n常见年份罗马数字:")
    years = [1984, 1999, 2000, 2024, 2025, 3000, 3999]
    for year in years:
        if year in COMMON_ROMANS:
            print(f"  {year}: {COMMON_ROMANS[year]}")
    
    print("\n" + "=" * 60)
    print("  演示结束！感谢使用 Roman Numeral Utils 🏛️")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()