"""
Roman Numeral Utils - 使用示例

本示例展示罗马数字工具包的各种用法，包括：
- 基本转换
- 验证
- 算术运算
- 链式构建
- 排序和范围生成
"""

from mod import (
    to_roman,
    from_roman,
    is_valid_roman,
    validate_roman,
    RomanNumeral,
    roman,
    roman_sort,
    roman_range,
    roman_sum,
    roman_list,
    RomanNumeralBuilder,
    InvalidRomanNumeralError,
    OutOfRangeError
)


def print_section(title: str):
    """打印章节标题"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print('='*60)


def example_basic_conversion():
    """基本转换示例"""
    print_section("基本转换")
    
    # 阿拉伯数字 → 罗马数字
    numbers = [1, 4, 9, 40, 90, 400, 900, 1994, 2023, 3999]
    print("\n阿拉伯数字 → 罗马数字:")
    for num in numbers:
        print(f"  {num:4d} → {to_roman(num)}")
    
    # 罗马数字 → 阿拉伯数字
    romans = ['I', 'IV', 'IX', 'XL', 'XC', 'CD', 'CM', 'MCMXCIV', 'MMMCMXCIX']
    print("\n罗马数字 → 阿拉伯数字:")
    for r in romans:
        print(f"  {r:10s} → {from_roman(r)}")


def example_validation():
    """验证示例"""
    print_section("验证")
    
    test_cases = ['MCMXCIV', 'IIII', 'ABC', 'MMXXIII', 'VV', '']
    print("\n验证罗马数字:")
    for case in test_cases:
        valid, msg = validate_roman(case)
        status = "✓ 有效" if valid else "✗ 无效"
        print(f"  {case or '(空)':10s} → {status}")
        if not valid:
            print(f"            错误: {msg}")


def example_roman_numeral_class():
    """RomanNumeral 类示例"""
    print_section("RomanNumeral 类")
    
    # 创建
    print("\n创建罗马数字:")
    r1 = RomanNumeral(10)
    r2 = RomanNumeral('V')
    print(f"  RomanNumeral(10) = {r1} (阿拉伯: {r1.arabic})")
    print(f"  RomanNumeral('V') = {r2} (阿拉伯: {r2.arabic})")
    
    # 算术运算
    print("\n算术运算:")
    print(f"  X + V = {r1 + r2}")
    print(f"  X - V = {r1 - r2}")
    print(f"  X * V = {r1 * r2}")
    print(f"  X / V = {r1 / r2}")
    print(f"  X ** 2 = {r1 ** 2}")
    
    # 与整数运算
    print("\n与整数运算:")
    print(f"  X + 5 = {r1 + 5}")
    print(f"  15 - V = {RomanNumeral(15) - r2}")
    
    # 比较
    print("\n比较:")
    print(f"  X > V = {r1 > r2}")
    print(f"  X == 10 = {r1 == 10}")
    print(f"  X == 'X' = {r1 == 'X'}")


def example_extended_numerals():
    """扩展罗马数字示例"""
    print_section("扩展罗马数字 (大数支持)")
    
    large_numbers = [4000, 5000, 10000, 50000, 100000, 500000, 1000000]
    print("\n大数转换 (使用括号表示上划线):")
    for num in large_numbers:
        roman_str = to_roman(num, extended=True)
        arabic = from_roman(roman_str, extended=True)
        print(f"  {num:10d} → {roman_str:15s} → {arabic}")


def example_builder():
    """构建器示例"""
    print_section("链式构建器")
    
    print("\n基本链式操作:")
    result = RomanNumeralBuilder().add(10).add(5).build()
    print(f"  add(10).add(5) = {result}")
    
    result = RomanNumeralBuilder().from_int(100).subtract(10).build()
    print(f"  from_int(100).subtract(10) = {result}")
    
    result = RomanNumeralBuilder().from_int(5).multiply(3).build()
    print(f"  from_int(5).multiply(3) = {result}")
    
    result = RomanNumeralBuilder().from_int(15).divide(3).build()
    print(f"  from_int(15).divide(3) = {result}")
    
    print("\n复杂链式操作:")
    result = (RomanNumeralBuilder()
              .from_roman('X')
              .add('V')
              .multiply(2)
              .build())
    print(f"  from_roman('X').add('V').multiply(2) = {result}")


def example_sort_and_range():
    """排序和范围示例"""
    print_section("排序和范围")
    
    # 排序
    unsorted = ['III', 'I', 'II', 'V', 'IV']
    print(f"\n排序前: {unsorted}")
    print(f"升序:   {roman_sort(unsorted)}")
    print(f"降序:   {roman_sort(unsorted, reverse=True)}")
    
    # 混合类型排序
    mixed = [10, 'V', RomanNumeral(1), 3]
    print(f"\n混合类型排序: {roman_sort(mixed)}")
    
    # 范围生成
    print("\n范围生成:")
    print(f"  1-10: {roman_range(1, 10)}")
    print(f"  步长为5: {roman_range(1, 20, step=5)}")


def example_sum_and_list():
    """求和和列表示例"""
    print_section("求和与列表")
    
    # 求和
    numbers = ['X', 'V', 'I']
    print(f"\n求和: {' + '.join(numbers)} = {roman_sum(numbers)}")
    
    numbers = [100, 50, 10, 5]
    print(f"求和: {' + '.join(map(str, numbers))} = {roman_sum(numbers)}")
    
    # 列表格式化
    print("\n格式化列表:")
    print(roman_list(roman_range(1, 5)))


def example_convenience():
    """便捷函数示例"""
    print_section("便捷函数")
    
    # roman() 函数
    print("\n使用 roman() 快捷函数:")
    r1 = roman(10)
    r2 = roman('V')
    r3 = roman(3)
    
    print(f"  roman(10) + roman('V') + roman(3) = {r1 + r2 + r3}")
    print(f"  总计: {(r1 + r2 + r3).arabic}")


def example_practical():
    """实际应用示例"""
    print_section("实际应用")
    
    # 年份转换
    print("\n年份转换:")
    years = [1776, 1984, 2000, 2023, 2024]
    for year in years:
        print(f"  {year} → {to_roman(year)}")
    
    # 书籍章节
    print("\n书籍章节编号:")
    for i, chapter in enumerate(['引言', '基础概念', '进阶技巧', '实战案例', '总结'], 1):
        print(f"  第{to_roman(i)}章 - {chapter}")
    
    # 序列号生成
    print("\n序列号生成 (I-X):")
    for i, r in enumerate(roman_range(1, 10), 1):
        print(f"  {r}序列 {i:02d}")


def example_error_handling():
    """错误处理示例"""
    print_section("错误处理")
    
    print("\n超出范围错误:")
    try:
        to_roman(4000)
    except OutOfRangeError as e:
        print(f"  ✗ to_roman(4000): {e}")
    
    try:
        to_roman(0)
    except OutOfRangeError as e:
        print(f"  ✗ to_roman(0): {e}")
    
    print("\n无效格式错误:")
    try:
        from_roman('IIII')
    except InvalidRomanNumeralError as e:
        print(f"  ✗ from_roman('IIII'): {e}")
    
    try:
        from_roman('ABC')
    except InvalidRomanNumeralError as e:
        print(f"  ✗ from_roman('ABC'): {e}")
    
    print("\n负数运算错误:")
    try:
        r = RomanNumeral(5) - RomanNumeral(10)
    except OutOfRangeError as e:
        print(f"  ✗ RomanNumeral(5) - RomanNumeral(10): {e}")


def main():
    """运行所有示例"""
    print("=" * 60)
    print(" 罗马数字工具包 (Roman Numeral Utils) - 使用示例")
    print("=" * 60)
    
    example_basic_conversion()
    example_validation()
    example_roman_numeral_class()
    example_extended_numerals()
    example_builder()
    example_sort_and_range()
    example_sum_and_list()
    example_convenience()
    example_practical()
    example_error_handling()
    
    print("\n" + "=" * 60)
    print(" 示例运行完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()