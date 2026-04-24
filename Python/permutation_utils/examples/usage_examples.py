"""
Permutation Utils 使用示例

演示排列组合工具的各种应用场景。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    PermutationUtils,
    CombinationUtils,
    PermutationUtilsAdvanced,
    permutations,
    combinations,
    permutation_count,
    combination_count,
)


def example_basic_permutations():
    """基本排列示例"""
    print("=" * 50)
    print("示例 1: 基本排列")
    print("=" * 50)
    
    elements = ['A', 'B', 'C']
    
    # 全排列
    print(f"\n{elements} 的全排列:")
    for i, perm in enumerate(PermutationUtils.permutations(elements)):
        print(f"  {i+1}. {perm}")
    
    # 部分排列 (P(n, k))
    print(f"\n{elements} 的 2-排列:")
    for i, perm in enumerate(PermutationUtils.permutations(elements, 2)):
        print(f"  {i+1}. {perm}")
    
    # 排列数
    print(f"\n排列数:")
    print(f"  P(5, 3) = {permutation_count(5, 3)}")
    print(f"  P(4) = {permutation_count(4)} (全排列)")


def example_basic_combinations():
    """基本组合示例"""
    print("\n" + "=" * 50)
    print("示例 2: 基本组合")
    print("=" * 50)
    
    elements = ['A', 'B', 'C', 'D']
    
    # 2-组合
    print(f"\n{elements} 的 2-组合:")
    for i, comb in enumerate(CombinationUtils.combinations(elements, 2)):
        print(f"  {i+1}. {comb}")
    
    # 所有子集
    print(f"\n{['A', 'B', 'C']} 的所有子集:")
    for subset in CombinationUtils.all_subsets(['A', 'B', 'C']):
        print(f"  {subset}")
    
    # 组合数
    print(f"\n组合数:")
    print(f"  C(5, 2) = {combination_count(5, 2)}")
    print(f"  C(10, 5) = {combination_count(10, 5)}")


def example_permutation_rank():
    """排列序号示例"""
    print("\n" + "=" * 50)
    print("示例 3: 排列序号 (字典序)")
    print("=" * 50)
    
    elements = [1, 2, 3, 4]
    
    print(f"\n{elements} 的排列按字典序编号:")
    for i in range(permutation_count(4)):
        perm = PermutationUtils.permutation_unrank(i, elements)
        rank = PermutationUtils.permutation_rank(perm, elements)
        print(f"  序号 {i}: {perm} (验证: {rank})")
    
    # 实际应用：找出某个排列是第几个
    target = (2, 4, 1, 3)
    rank = PermutationUtils.permutation_rank(target, elements)
    print(f"\n排列 {target} 的字典序编号是: {rank}")


def example_combination_rank():
    """组合序号示例"""
    print("\n" + "=" * 50)
    print("示例 4: 组合序号 (字典序)")
    print("=" * 50)
    
    elements = [1, 2, 3, 4, 5]
    k = 3
    
    print(f"\n{elements} 的 {k}-组合按字典序编号:")
    for i in range(combination_count(5, 3)):
        comb = CombinationUtils.combination_unrank(i, elements, k)
        rank = CombinationUtils.combination_rank(comb, elements)
        print(f"  序号 {i}: {comb} (验证: {rank})")


def example_inversion():
    """逆序对示例"""
    print("\n" + "=" * 50)
    print("示例 5: 逆序对与排列奇偶性")
    print("=" * 50)
    
    perms = [
        (1, 2, 3, 4),
        (4, 3, 2, 1),
        (2, 1, 4, 3),
        (1, 3, 2, 4),
    ]
    
    for perm in perms:
        inv_count = PermutationUtils.inversion_count(perm)
        sign = PermutationUtils.permutation_sign(perm)
        parity = "偶" if PermutationUtils.is_even_permutation(perm) else "奇"
        print(f"  {perm}: 逆序对={inv_count}, {parity}排列, 符号={sign}")


def example_next_prev():
    """下一个/上一个排列示例"""
    print("\n" + "=" * 50)
    print("示例 6: 遍历排列 (下一个/上一个)")
    print("=" * 50)
    
    # 从第一个排列开始遍历
    arr = [1, 2, 3, 4]
    print(f"\n从 {arr} 开始遍历所有排列:")
    count = 1
    print(f"  {count}. {arr}")
    
    while True:
        result = PermutationUtils.next_permutation(arr)
        if result is None:
            break
        count += 1
        print(f"  {count}. {arr}")
    
    print(f"\n共 {count} 个排列")


def example_random():
    """随机排列组合示例"""
    print("\n" + "=" * 50)
    print("示例 7: 随机排列与组合")
    print("=" * 50)
    
    # 随机排列
    print("\n5 个随机排列 (n=8):")
    for i in range(5):
        perm = PermutationUtilsAdvanced.random_permutation(8, seed=i*100)
        print(f"  {i+1}. {perm}")
    
    # 随机组合
    print("\n5 个随机组合 (n=10, k=4):")
    for i in range(5):
        comb = PermutationUtilsAdvanced.random_combination(10, 4, seed=i*100)
        print(f"  {i+1}. {comb}")


def example_multiset():
    """多重集排列示例"""
    print("\n" + "=" * 50)
    print("示例 8: 多重集排列 (处理重复元素)")
    print("=" * 50)
    
    # 单词字母排列
    word = "MISSISSIPPI"
    letters = list(word)
    count = PermutationUtilsAdvanced.multiset_permutation_count(letters)
    print(f"\n'{word}' 的字母可组成 {count} 种不同的排列")
    
    # 显示前几个排列
    print("前 10 个排列:")
    for i, perm in enumerate(PermutationUtilsAdvanced.multiset_permutations(letters)):
        if i >= 10:
            break
        print(f"  {i+1}. {''.join(perm)}")


def example_derangement():
    """错排示例"""
    print("\n" + "=" * 50)
    print("示例 9: 错排 (Derangement)")
    print("=" * 50)
    
    print("\n错排：每个元素都不在原位置的排列")
    print("\n错排数 D(n):")
    for n in range(1, 8):
        d = PermutationUtilsAdvanced.derangement_count(n)
        print(f"  D({n}) = {d}")
    
    # 4 的所有错排
    print(f"\n4 的所有错排:")
    for d in PermutationUtilsAdvanced.derangements(4):
        print(f"  {d}")


def example_practical_password():
    """实际应用：密码生成"""
    print("\n" + "=" * 50)
    print("示例 10: 实际应用 - 生成不重复密码组合")
    print("=" * 50)
    
    import string
    
    # 从字符集中生成所有可能的密码
    chars = string.digits[:4]  # 使用 0-3 作为示例
    password_length = 2
    
    print(f"\n字符集: {list(chars)}")
    print(f"密码长度: {password_length}")
    print(f"可能的密码数: {permutation_count(len(chars), password_length)}")
    print("\n所有可能的密码:")
    
    for i, perm in enumerate(permutations(list(chars), password_length)):
        password = ''.join(perm)
        print(f"  {i+1}. {password}")


def example_practical_lottery():
    """实际应用：彩票分析"""
    print("\n" + "=" * 50)
    print("示例 11: 实际应用 - 彩票号码分析")
    print("=" * 50)
    
    # 双色球：从 33 个红球选 6 个，从 16 个蓝球选 1 个
    red_balls = 33
    blue_balls = 16
    select_red = 6
    
    total = combination_count(red_balls, select_red) * blue_balls
    print(f"\n双色球:")
    print(f"  红球: 从 {red_balls} 个选 {select_red} 个")
    print(f"  蓝球: 从 {blue_balls} 个选 1 个")
    print(f"  总组合数: {total:,}")
    print(f"  中一等奖概率: 1/{total:,}")
    
    # 显示一个随机选号
    import random
    random.seed(42)
    selected_red = sorted(random.sample(range(1, red_balls + 1), select_red))
    selected_blue = random.randint(1, blue_balls)
    print(f"\n随机选号示例:")
    print(f"  红球: {selected_red}")
    print(f"  蓝球: {selected_blue}")


def example_practical_schedule():
    """实际应用：排列任务"""
    print("\n" + "=" * 50)
    print("示例 12: 实际应用 - 任务排序分析")
    print("=" * 50)
    
    tasks = ['写报告', '开会', '回邮件', '写代码']
    
    print(f"\n任务列表: {tasks}")
    print(f"可能的执行顺序数: {permutation_count(len(tasks))}")
    
    # 分析特定顺序的逆序对（代表"优先级冲突"）
    schedule = ('写代码', '开会', '写报告', '回邮件')
    conflicts = PermutationUtils.inversion_count(schedule)
    print(f"\n执行顺序 {schedule}:")
    print(f"  优先级冲突数（逆序对）: {conflicts}")
    print(f"  排列类型: {'偶排列' if PermutationUtils.is_even_permutation(schedule) else '奇排列'}")


def main():
    """运行所有示例"""
    example_basic_permutations()
    example_basic_combinations()
    example_permutation_rank()
    example_combination_rank()
    example_inversion()
    example_next_prev()
    example_random()
    example_multiset()
    example_derangement()
    example_practical_password()
    example_practical_lottery()
    example_practical_schedule()
    
    print("\n" + "=" * 50)
    print("所有示例运行完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()