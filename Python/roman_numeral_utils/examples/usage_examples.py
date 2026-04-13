"""
Roman Numeral Utils - 使用示例

演示罗马数字转换工具的各种用法
"""

import sys
import os
# 添加 AllToolkit 目录到路径
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, base_dir)

from Python.roman_numeral_utils.mod import (
    to_roman, from_roman, convert,
    is_valid_roman, is_roman_numeral,
    batch_to_roman, batch_from_roman, get_roman_range,
    compare_roman, add_roman, subtract_roman, multiply_roman, divide_roman,
    find_roman_in_text, normalize_roman, roman_to_ordinal,
    get_roman_value_table, explain_roman,
    MIN_VALUE, MAX_VALUE
)


def print_section(title):
    """打印章节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def example_basic_conversion():
    """基础转换示例"""
    print_section("1. 基础转换")
    
    # 阿拉伯数字转罗马数字
    print("阿拉伯数字 → 罗马数字:")
    numbers = [1, 4, 9, 40, 90, 400, 900, 2024, 1999]
    for num in numbers:
        print(f"  {num:4d} → {to_roman(num)}")
    
    print("\n罗马数字 → 阿拉伯数字:")
    romans = ['I', 'IV', 'IX', 'XL', 'XC', 'CD', 'CM', 'MMXXIV', 'MCMXCIX']
    for roman in romans:
        print(f"  {roman:10s} → {from_roman(roman)}")


def example_smart_convert():
    """智能转换示例"""
    print_section("2. 智能转换")
    
    # convert 函数自动识别输入类型
    print("convert() 智能识别:")
    print(f"  convert(2024) → {convert(2024)}")
    print(f"  convert('MMXXIV') → {convert('MMXXIV')}")


def example_validation():
    """验证示例"""
    print_section("3. 验证功能")
    
    # 严格验证
    print("严格验证 (is_valid_roman):")
    test_cases = ['IV', 'IX', 'IIII', 'VV', 'VX', 'MMXXIV']
    for case in test_cases:
        valid = is_valid_roman(case)
        print(f"  '{case:8s}' → {'✓ 有效' if valid else '✗ 无效'}")
    
    # 宽松检查
    print("\n宽松检查 (is_roman_numeral):")
    print(f"  'IIII' → {'✓ 可能是' if is_roman_numeral('IIII') else '✗ 不是'}")


def example_batch_operations():
    """批量操作示例"""
    print_section("4. 批量操作")
    
    # 批量转罗马
    print("批量转罗马数字:")
    numbers = [1, 5, 10, 50, 100, 500, 1000]
    results = batch_to_roman(numbers)
    for num, roman, _ in results:
        print(f"  {num:4d} → {roman}")
    
    # 批量转阿拉伯
    print("\n批量转阿拉伯数字:")
    romans = ['I', 'V', 'X', 'L', 'C', 'D', 'M']
    results = batch_from_roman(romans)
    for roman, num, _ in results:
        print(f"  {roman:4s} → {num}")
    
    # 生成范围
    print("\n生成 1-10 的罗马数字:")
    range_result = get_roman_range(1, 10)
    for num, roman in range_result:
        print(f"  {num:2d} → {roman}")


def example_arithmetic():
    """算术运算示例"""
    print_section("5. 算术运算")
    
    print("加法:")
    print(f"  X + V = {add_roman('X', 'V')}")
    print(f"  IV + I = {add_roman('IV', 'I')}")
    
    print("\n减法:")
    print(f"  X - V = {subtract_roman('X', 'V')}")
    print(f"  V - I = {subtract_roman('V', 'I')}")
    
    print("\n乘法:")
    print(f"  X × X = {multiply_roman('X', 'X')}")
    print(f"  V × II = {multiply_roman('V', 'II')}")
    
    print("\n除法:")
    print(f"  X ÷ II = {divide_roman('X', 'II')}")
    q, r = divide_roman('X', 'III', remainder=True)
    print(f"  X ÷ III = {q} 余 {r}")
    
    print("\n比较:")
    print(f"  X vs V: {compare_roman('X', 'V')} (正数=大于)")
    print(f"  V vs X: {compare_roman('V', 'X')} (负数=小于)")
    print(f"  X vs X: {compare_roman('X', 'X')} (零=相等)")


def example_text_search():
    """文本搜索示例"""
    print_section("6. 文本搜索")
    
    text = "King Henry VIII succeeded his father Henry VII. Chapter XIV continues..."
    print(f"原文: {text}")
    print("\n找到的罗马数字:")
    
    results = find_roman_in_text(text)
    for roman, start, end in results:
        print(f"  '{roman}' at position {start}-{end}")


def example_normalize():
    """规范化示例"""
    print_section("7. 规范化")
    
    # 非标准形式
    non_standard = ['iiii', 'viiii', 'IIIIII']
    print("非标准形式 → 标准形式:")
    for ns in non_standard:
        std = normalize_roman(ns)
        print(f"  '{ns}' → '{std}'")


def example_ordinal():
    """序数词示例"""
    print_section("8. 序数词转换")
    
    romans = ['I', 'II', 'III', 'IV', 'V', 'XI', 'XII', 'XIII', 'XXI']
    print("罗马数字 → 英文序数词:")
    for roman in romans:
        ordinal = roman_to_ordinal(roman)
        print(f"  {roman:4s} → {ordinal}")


def example_explain():
    """解释示例"""
    print_section("9. 罗马数字解释")
    
    examples = ['XIV', 'MCMXCIX', 'MMMCMXCIX']
    
    for roman in examples:
        print(f"\n解释 '{roman}':")
        result = explain_roman(roman)
        for symbol, value, note in result:
            if note:
                print(f"  {symbol:4s} = {value:4d} ({note})")
            else:
                print(f"  {symbol:4s} = {value:4d}")


def example_reference():
    """参考表示例"""
    print_section("10. 值对照表")
    
    print("罗马数字符号对照表:")
    table = get_roman_value_table()
    for symbol, value in table:
        print(f"  {symbol} = {value}")


def example_practical():
    """实际应用示例"""
    print_section("11. 实际应用")
    
    # 年份转换
    print("年份转换:")
    years = [1776, 1989, 2024, 2000]
    for year in years:
        print(f"  {year} → {to_roman(year)}")
    
    # 版权年份
    print(f"\n版权年份: © {to_roman(2024)}")
    
    # 书籍章节
    print("\n书籍章节编号:")
    for chapter in range(1, 11):
        print(f"  Chapter {to_roman(chapter)}")
    
    # 序列号
    print("\n游戏/电影系列:")
    series = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX']
    for s in series:
        print(f"  Star Wars Episode {s} = {from_roman(s)}")


def main():
    """运行所有示例"""
    print("="*60)
    print("  Roman Numeral Utils - 使用示例")
    print("="*60)
    
    example_basic_conversion()
    example_smart_convert()
    example_validation()
    example_batch_operations()
    example_arithmetic()
    example_text_search()
    example_normalize()
    example_ordinal()
    example_explain()
    example_reference()
    example_practical()
    
    print_section("完成!")
    print("所有示例已运行完成。")
    print(f"\n支持范围: {MIN_VALUE} - {MAX_VALUE}")


if __name__ == '__main__':
    main()