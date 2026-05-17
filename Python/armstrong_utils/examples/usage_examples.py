"""
阿姆斯特朗数与趣味数工具使用示例

本示例展示如何使用 armstrong_utils 工具进行各种趣味数的检测和分析。
"""

import sys
sys.path.insert(0, '..')

from mod import (
    is_armstrong, find_armstrong_numbers, get_armstrong_digits,
    is_happy, find_happy_numbers, get_happy_sequence,
    is_kaprekar, find_kaprekar_numbers, kaprekar_routine,
    is_perfect, find_perfect_numbers, get_proper_divisors,
    is_palindrome, find_palindrome_numbers, reverse_number, is_lychrel,
    analyze_number, find_special_numbers,
    digital_root, is_harshad, find_harshad_numbers
)


def demo_armstrong():
    """阿姆斯特朗数演示"""
    print("=" * 60)
    print("【阿姆斯特朗数 (Armstrong Number / Narcissistic Number)】")
    print("=" * 60)
    print("\n定义：一个 n 位数，其各位数字的 n 次方之和等于它本身")
    print("例如：153 = 1³ + 5³ + 3³ = 1 + 125 + 27 = 153")
    
    # 检测单个数
    test_numbers = [153, 370, 371, 407, 1634, 9474]
    print("\n--- 阿姆斯特朗数检测 ---")
    for num in test_numbers:
        if is_armstrong(num):
            digits, power_sum, diff = get_armstrong_digits(num)
            print(f"✓ {num} 是阿姆斯特朗数")
            print(f"  位数: {digits}, 幂和: {power_sum}, 差值: {diff}")
        else:
            print(f"✗ {num} 不是阿姆斯特朗数")
    
    # 查找范围内的阿姆斯特朗数
    print(f"\n--- 10000 以内的阿姆斯特朗数 ---")
    armstrong_nums = find_armstrong_numbers(10000)
    print(f"共 {len(armstrong_nums)} 个: {armstrong_nums}")
    
    # 水仙花数（特指 3 位阿姆斯特朗数）
    print(f"\n--- 水仙花数（3 位阿姆斯特朗数）---")
    narcissistic_3digit = [n for n in armstrong_nums if 100 <= n < 1000]
    print(f"水仙花数: {narcissistic_3digit}")


def demo_happy():
    """快乐数演示"""
    print("\n" + "=" * 60)
    print("【快乐数 (Happy Number)】")
    print("=" * 60)
    print("\n定义：反复计算各位数字的平方和，最终达到 1 的数为快乐数")
    
    # 检测单个数
    test_numbers = [1, 7, 10, 13, 19, 23, 28, 31]
    print("\n--- 快乐数检测 ---")
    for num in test_numbers:
        if is_happy(num):
            print(f"✓ {num} 是快乐数 😊")
        else:
            print(f"✗ {num} 不是快乐数 😢")
    
    # 显示变换序列
    print("\n--- 快乐数变换序列 ---")
    for num in [19, 7, 10]:
        sequence = get_happy_sequence(num)
        print(f"{num} → {' → '.join(map(str, sequence))}")
    
    # 查找快乐数
    print(f"\n--- 100 以内的快乐数 ---")
    happy_nums = find_happy_numbers(100)
    print(f"共 {len(happy_nums)} 个: {happy_nums}")


def demo_kaprekar():
    """卡普雷卡尔数演示"""
    print("\n" + "=" * 60)
    print("【卡普雷卡尔数 (Kaprekar Number)】")
    print("=" * 60)
    print("\n定义：一个数的平方可以分为两部分，使得这两部分的和等于原数")
    print("例如：45² = 2025，20 + 25 = 45")
    
    # 检测单个数
    test_numbers = [1, 9, 45, 55, 99, 297, 703, 999]
    print("\n--- 卡普雷卡尔数检测 ---")
    for num in test_numbers:
        if is_kaprekar(num):
            square = num * num
            print(f"✓ {num} 是卡普雷卡尔数 (平方: {square})")
        else:
            print(f"✗ {num} 不是卡普雷卡尔数")
    
    # 查找卡普雷卡尔数
    print(f"\n--- 1000 以内的卡普雷卡尔数 ---")
    kaprekar_nums = find_kaprekar_numbers(1000)
    print(f"共 {len(kaprekar_nums)} 个: {kaprekar_nums}")
    
    # 卡普雷卡尔程序
    print("\n--- 卡普雷卡尔程序 (达到常数 6174) ---")
    test_cases = [3524, 1234, 9876]
    for num in test_cases:
        sequence, reached = kaprekar_routine(num)
        status = "✓ 达到 6174" if reached else "✗ 未达到"
        print(f"{num}: {' → '.join(map(str, sequence))} {status}")


def demo_perfect():
    """完全数演示"""
    print("\n" + "=" * 60)
    print("【完全数 (Perfect Number)】")
    print("=" * 60)
    print("\n定义：一个数等于其所有真约数之和")
    print("例如：6 = 1 + 2 + 3，28 = 1 + 2 + 4 + 7 + 14")
    
    # 检测单个数
    test_numbers = [6, 28, 496, 8128, 12, 18]
    print("\n--- 完全数检测 ---")
    for num in test_numbers:
        divisors = get_proper_divisors(num)
        divisor_sum = sum(divisors)
        if is_perfect(num):
            print(f"✓ {num} 是完全数 (真约数: {divisors}, 和: {divisor_sum})")
        else:
            print(f"✗ {num} 不是完全数 (真约数: {divisors}, 和: {divisor_sum})")
    
    # 盈数和亏数
    print("\n--- 盈数和亏数 ---")
    test_numbers = [8, 12, 20, 24]
    for num in test_numbers:
        divisors = get_proper_divisors(num)
        divisor_sum = sum(divisors)
        if divisor_sum > num:
            print(f"盈数 {num}: 真约数和 {divisor_sum} > {num}")
        else:
            print(f"亏数 {num}: 真约数和 {divisor_sum} < {num}")
    
    # 查找完全数
    print(f"\n--- 10000 以内的完全数 ---")
    perfect_nums = find_perfect_numbers(10000)
    print(f"共 {len(perfect_nums)} 个: {perfect_nums}")


def demo_palindrome():
    """回文数演示"""
    print("\n" + "=" * 60)
    print("【回文数 (Palindrome Number)】")
    print("=" * 60)
    print("\n定义：正读和反读都相同的数")
    
    # 检测单个数
    test_numbers = [121, 12321, 123, 1234, 1001]
    print("\n--- 回文数检测 ---")
    for num in test_numbers:
        if is_palindrome(num):
            print(f"✓ {num} 是回文数")
        else:
            print(f"✗ {num} 不是回文数")
    
    # 数字反转
    print("\n--- 数字反转 ---")
    for num in [123, 100, 12345, 10000]:
        reversed_num = reverse_number(num)
        print(f"{num} 反转 → {reversed_num}")
    
    # 查找回文数
    print(f"\n--- 200 以内的回文数 ---")
    palindrome_nums = find_palindrome_numbers(200)
    print(f"共 {len(palindrome_nums)} 个: {palindrome_nums}")
    
    # Lychrel 数
    print("\n--- Lychrel 数候选 ---")
    lychrel_candidates = [196, 295, 394, 493, 592]
    for num in lychrel_candidates:
        if is_lychrel(num):
            print(f"✓ {num} 是 Lychrel 数候选（50 次迭代内未形成回文）")
        else:
            sequence, _ = get_lychrel_sequence(num)
            print(f"✗ {num} 可形成回文: {' → '.join(map(str, sequence[:5]))}...")


def demo_harshad():
    """Harshad 数演示"""
    print("\n" + "=" * 60)
    print("【Harshad 数 (Niven Number)】")
    print("=" * 60)
    print("\n定义：能被其数位之和整除的数")
    print("例如：18 ÷ (1+8) = 18 ÷ 9 = 2")
    
    # 检测单个数
    test_numbers = [1, 2, 3, 10, 12, 18, 20, 21, 24]
    print("\n--- Harshad 数检测 ---")
    for num in test_numbers:
        digit_sum = sum(int(d) for d in str(num))
        if is_harshad(num):
            print(f"✓ {num} 是 Harshad 数 ({num} ÷ {digit_sum} = {num // digit_sum})")
        else:
            print(f"✗ {num} 不是 Harshad 数 ({num} ÷ {digit_sum} ≠ 整数)")
    
    # 查找 Harshad 数
    print(f"\n--- 50 以内的 Harshad 数 ---")
    harshad_nums = find_harshad_numbers(50)
    print(f"共 {len(harshad_nums)} 个: {harshad_nums}")


def demo_digital_root():
    """数字根演示"""
    print("\n" + "=" * 60)
    print("【数字根 (Digital Root)】")
    print("=" * 60)
    print("\n定义：反复求数位之和直到只剩一位数")
    
    test_numbers = [0, 1, 9, 10, 38, 12345, 999, 999999999]
    print("\n--- 数字根计算 ---")
    for num in test_numbers:
        root = digital_root(num)
        print(f"digital_root({num}) = {root}")


def demo_analyze():
    """综合分析演示"""
    print("\n" + "=" * 60)
    print("【综合分析】")
    print("=" * 60)
    
    # 分析一些有趣的数
    interesting_numbers = [6, 28, 153, 370, 496, 9474]
    
    for num in interesting_numbers:
        result = analyze_number(num)
        print(f"\n--- 分析 {num} ---")
        print(f"  位数: {result['digits']}")
        print(f"  数位和: {result['digit_sum']}")
        
        properties = []
        if result['is_armstrong']:
            properties.append("阿姆斯特朗数")
        if result['is_happy']:
            properties.append("快乐数")
        if result['is_kaprekar']:
            properties.append("卡普雷卡尔数")
        if result['is_perfect']:
            properties.append("完全数")
        if result['is_palindrome']:
            properties.append("回文数")
        if result['is_abundant']:
            properties.append("盈数")
        if result['is_deficient']:
            properties.append("亏数")
        
        if properties:
            print(f"  特殊属性: {', '.join(properties)}")
        else:
            print("  特殊属性: 无")
        
        print(f"  真约数: {result['proper_divisors']}")


def demo_special_numbers():
    """查找特殊数演示"""
    print("\n" + "=" * 60)
    print("【查找特殊数】")
    print("=" * 60)
    
    limit = 1000
    result = find_special_numbers(limit)
    
    print(f"\n--- {limit} 以内的特殊数统计 ---")
    print(f"阿姆斯特朗数: {len(result['armstrong'])} 个")
    print(f"快乐数: {len(result['happy'])} 个")
    print(f"卡普雷卡尔数: {len(result['kaprekar'])} 个")
    print(f"完全数: {len(result['perfect'])} 个")
    print(f"回文数: {len(result['palindrome'])} 个")
    
    # 找出同时是多种特殊数的数
    all_nums = set()
    for nums in result.values():
        all_nums.update(nums)
    
    multi_special = []
    for num in sorted(all_nums):
        count = 0
        types = []
        for key, nums in result.items():
            if num in nums:
                count += 1
                types.append(key)
        if count >= 3:
            multi_special.append((num, types))
    
    print(f"\n--- 同时是 3 种以上特殊数的数 ---")
    for num, types in multi_special[:10]:
        print(f"{num}: {', '.join(types)}")


def main():
    """主函数"""
    demo_armstrong()
    demo_happy()
    demo_kaprekar()
    demo_perfect()
    demo_palindrome()
    demo_harshad()
    demo_digital_root()
    demo_analyze()
    demo_special_numbers()
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()