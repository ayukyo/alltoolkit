"""
罗马数字转换工具使用示例

展示各种功能的使用方法：
- 基本转换
- 验证功能
- 算术运算
- 工具函数
- 实际应用场景
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    to_roman, to_arabic, is_valid_roman,
    add, subtract, compare, range_to_roman,
    list_operations, quick_convert, parse_mixed,
    find_largest_smaller
)


def print_separator(title: str):
    """打印分隔线"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def example_basic_conversion():
    """基本转换示例"""
    print_separator("基本转换示例")
    
    # 阿拉伯数字转罗马数字
    numbers = [1, 5, 10, 50, 100, 500, 1000, 2024, 3999]
    print("\n阿拉伯数字 → 罗马数字:")
    for num in numbers:
        roman = to_roman(num)
        print(f"  {num:5d} → {roman}")
    
    # 罗马数字转阿拉伯数字
    romans = ['I', 'V', 'X', 'L', 'C', 'D', 'M', 'MMXXIV', 'MMMCMXCIX']
    print("\n罗马数字 → 阿拉伯数字:")
    for roman in romans:
        arabic = to_arabic(roman)
        print(f"  {roman:12s} → {arabic}")


def example_validation():
    """验证功能示例"""
    print_separator("验证功能示例")
    
    test_cases = [
        ('XIV', '有效的罗马数字'),
        ('MMXXIV', '有效的罗马数字'),
        ('IIII', '无效：I 重复 4 次'),
        ('VV', '无效：V 不能重复'),
        ('VX', '无效：错误的减法组合'),
        ('IC', '无效：I 只能减 V 或 X'),
        ('', '无效：空字符串'),
    ]
    
    print("\n罗马数字验证:")
    for roman, description in test_cases:
        valid = is_valid_roman(roman)
        status = "✓ 有效" if valid else "✗ 无效"
        print(f"  '{roman:10s}' → {status:8s} ({description})")


def example_subtractive_notation():
    """减法表示法示例"""
    print_separator("减法表示法示例")
    
    subtractive_pairs = [
        (4, 'IV'),
        (9, 'IX'),
        (40, 'XL'),
        (90, 'XC'),
        (400, 'CD'),
        (900, 'CM'),
    ]
    
    print("\n标准减法表示法:")
    print("  数字  罗马数字  说明")
    print("  " + "-"*40)
    for num, expected in subtractive_pairs:
        roman = to_roman(num)
        correct = "✓" if roman == expected else "✗"
        print(f"  {num:4d}  {roman:8s}   {expected:4s} {correct}")
    
    # 展示为什么使用减法表示法
    print("\n为什么使用减法表示法:")
    print("  4 = IV (不是 IIII) - 更简洁")
    print("  9 = IX (不是 VIIII) - 更简洁")
    print("  40 = XL (不是 XXXX) - 更简洁")
    print("  2024 = MMXXIV")
    print("  分解: M(1000) + M(1000) + X(10) + X(10) + IV(4)")


def example_arithmetic():
    """算术运算示例"""
    print_separator("算术运算示例")
    
    # 加法
    print("\n加法运算:")
    additions = [
        ('I', 'I'),
        ('V', 'V'),
        ('X', 'IV'),
        ('C', 'C'),
        ('CM', 'C'),
    ]
    for r1, r2 in additions:
        result = add(r1, r2)
        a1, a2 = to_arabic(r1), to_arabic(r2)
        print(f"  {r1} ({a1}) + {r2} ({a2}) = {result} ({a1 + a2})")
    
    # 减法
    print("\n减法运算:")
    subtractions = [
        ('II', 'I'),
        ('V', 'I'),
        ('X', 'V'),
        ('C', 'X'),
        ('M', 'C'),
    ]
    for r1, r2 in subtractions:
        result = subtract(r1, r2)
        a1, a2 = to_arabic(r1), to_arabic(r2)
        print(f"  {r1} ({a1}) - {r2} ({a2}) = {result} ({a1 - a2})")
    
    # 比较
    print("\n比较运算:")
    comparisons = [
        ('X', 'V'),
        ('V', 'X'),
        ('X', 'X'),
        ('MMXXIV', 'MMXXIII'),
    ]
    for r1, r2 in comparisons:
        cmp = compare(r1, r2)
        if cmp > 0:
            symbol = ">"
        elif cmp < 0:
            symbol = "<"
        else:
            symbol = "="
        print(f"  {r1} {symbol} {r2}")


def example_utility_functions():
    """工具函数示例"""
    print_separator("工具函数示例")
    
    # 范围生成
    print("\n生成 1-20 的罗马数字:")
    romans = range_to_roman(1, 20)
    for i in range(0, len(romans), 5):
        row = romans[i:i+5]
        line = '  '.join(f"{i+j+1:2d}={r:4s}" for j, r in enumerate(row))
        print(f"  {line}")
    
    # 查找最大较小值
    print("\n查找最大较小值:")
    candidates = ['III', 'V', 'VII', 'X', 'XV']
    target = 'XII'
    result = find_largest_smaller(target, candidates)
    print(f"  目标: {target} ({to_arabic(target)})")
    print(f"  候选: {candidates}")
    print(f"  结果: {result} ({to_arabic(result) if result else 'None'})")
    
    # 综合运算
    print("\n综合运算:")
    ops = list_operations('MMXXIV', 'X')
    print(f"  MMXXIV 和 X:")
    for key, value in ops.items():
        print(f"    {key}: {value}")


def example_parsing():
    """解析功能示例"""
    print_separator("文本解析示例")
    
    texts = [
        "Chapter XII: The Beginning",
        "Henry VIII was king of England",
        "Super Bowl LVI was held in 2022",
        "Star Wars Episode IV: A New Hope",
        "World War II ended in 1945",
        "Page 1 has no roman numerals",
    ]
    
    for text in texts:
        matches = parse_mixed(text)
        print(f"\n  文本: '{text}'")
        if matches:
            for roman, value in matches:
                print(f"    发现: '{roman}' = {value}")
        else:
            print("    未发现罗马数字")


def example_practical_applications():
    """实际应用示例"""
    print_separator("实际应用示例")
    
    # 1. 生成章节编号
    print("\n1. 书籍章节编号生成器:")
    num_chapters = 15
    print(f"  生成 {num_chapters} 章的章节编号:")
    for i in range(1, min(num_chapters + 1, 11)):
        roman = to_roman(i)
        print(f"    章节 {roman}: [章节标题]")
    if num_chapters > 10:
        print(f"    ... 还有 {num_chapters - 10} 章")
    
    # 2. 年份转换
    print("\n2. 历史年份转换:")
    years = [1776, 1789, 1865, 1945, 1969, 2000, 2024]
    print("  重要历史年份:")
    for year in years:
        roman = to_roman(year)
        print(f"    公元 {year} = Anno {roman}")
    
    # 3. 钟表数字
    print("\n3. 钟表表盘数字:")
    clock_numbers = range_to_roman(1, 12)
    print("  钟表表盘: " + " ".join(clock_numbers))
    
    # 4. 统治者编号
    print("\n4. 统治者/教皇编号:")
    rulers = [
        ("亨利八世", "Henry VIII", 8),
        ("路易十四", "Louis XIV", 14),
        ("伊丽莎白二世", "Elizabeth II", 2),
        ("教皇约翰·保罗二世", "Pope John Paul II", 2),
    ]
    for cn, en, num in rulers:
        roman = to_roman(num)
        print(f"    {cn} ({en}) - {roman}")
    
    # 5. 体育赛事编号
    print("\n5. 体育赛事编号:")
    events = [
        ("超级碗", "Super Bowl", 57),
        ("奥运会", "Olympics", 33),  # 第33届夏季奥运会 (2024巴黎)
    ]
    for cn, en, num in events:
        roman = to_roman(num)
        print(f"    {cn} {roman} ({en} {roman})")


def example_quick_reference():
    """快速参考示例"""
    print_separator("快速参考")
    
    print("\n罗马数字基本符号:")
    print("  I = 1    V = 5    X = 10   L = 50")
    print("  C = 100  D = 500  M = 1000")
    
    print("\n减法规则:")
    print("  I 可以放在 V 或 X 前面: IV(4), IX(9)")
    print("  X 可以放在 L 或 C 前面: XL(40), XC(90)")
    print("  C 可以放在 D 或 M 前面: CD(400), CM(900)")
    
    print("\n重复规则:")
    print("  I, X, C, M 可以连续出现最多 3 次")
    print("  V, L, D 不能重复")
    
    print("\n数值范围:")
    print("  标准罗马数字支持: 1 - 3999")
    print("  最大值: MMMCMXCIX = 3999")


def main():
    """运行所有示例"""
    example_basic_conversion()
    example_validation()
    example_subtractive_notation()
    example_arithmetic()
    example_utility_functions()
    example_parsing()
    example_practical_applications()
    example_quick_reference()
    
    print("\n" + "="*60)
    print("  示例完成!")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()