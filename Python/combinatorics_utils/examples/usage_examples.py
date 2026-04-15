"""
Combinatorics Utils - 使用示例

展示组合数学工具集的各种使用场景。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    # 基础计算
    factorial, binomial, multinomial,
    # 排列组合
    permutations, combinations, permutations_count, combinations_count,
    permutations_with_replacement, combinations_with_replacement,
    # 笛卡尔积和幂集
    cartesian_product, powerset, powerset_count,
    # 特殊数列
    catalan, stirling_first, stirling_second, bell_number,
    partition_number, partitions, derangements,
    # 抽屉原理
    pigeonhole_count,
    # 组合搜索
    nth_combination, nth_permutation,
    # 实用函数
    generate_random_combination, generate_random_permutation,
    count_anagrams, subset_sum,
    # 预计算表
    generate_pascal_triangle, generate_catalan_sequence,
)


def example_basic_calculations():
    """基础计算示例"""
    print("=" * 50)
    print("基础计算示例")
    print("=" * 50)
    
    # 阶乘
    print(f"\n5! = {factorial(5)}")
    print(f"10! = {factorial(10)}")
    print(f"20! = {factorial(20)}")
    
    # 二项式系数
    print(f"\nC(10, 3) = {binomial(10, 3)}")
    print(f"C(100, 50) = {binomial(100, 50)}")
    
    # 多项式系数
    print(f"\n多项式系数 (3,2,1)! = {multinomial(3, 2, 1)}")


def example_permutations():
    """排列示例"""
    print("\n" + "=" * 50)
    print("排列示例")
    print("=" * 50)
    
    items = ['A', 'B', 'C']
    
    # 全排列
    print(f"\n{items} 的全排列:")
    for p in permutations(items):
        print(f"  {p}")
    
    # 部分排列
    print(f"\n{items} 取 2 个的排列:")
    for p in permutations(items, 2):
        print(f"  {p}")
    
    # 排列数
    print(f"\nP(5, 3) = {permutations_count(5, 3)}")
    
    # 可重复排列
    print(f"\n[1, 2] 取 3 个的可重复排列:")
    for p in permutations_with_replacement([1, 2], 3):
        print(f"  {p}")


def example_combinations():
    """组合示例"""
    print("\n" + "=" * 50)
    print("组合示例")
    print("=" * 50)
    
    items = ['A', 'B', 'C', 'D']
    
    # 组合
    print(f"\n{items} 取 2 个的组合:")
    for c in combinations(items, 2):
        print(f"  {c}")
    
    # 组合数
    print(f"\nC(10, 4) = {combinations_count(10, 4)}")
    
    # 可重复组合
    print(f"\n[1, 2, 3] 取 2 个的可重复组合:")
    for c in combinations_with_replacement([1, 2, 3], 2):
        print(f"  {c}")


def example_cartesian_and_powerset():
    """笛卡尔积和幂集示例"""
    print("\n" + "=" * 50)
    print("笛卡尔积和幂集示例")
    print("=" * 50)
    
    # 笛卡尔积
    print("\n[1, 2] × ['a', 'b'] 的笛卡尔积:")
    for p in cartesian_product([1, 2], ['a', 'b']):
        print(f"  {p}")
    
    # 幂集
    items = [1, 2, 3]
    print(f"\n{items} 的幂集 (共 {powerset_count(len(items))} 个子集):")
    for s in powerset(items):
        print(f"  {set(s) if s else '{}'}")


def example_special_sequences():
    """特殊数列示例"""
    print("\n" + "=" * 50)
    print("特殊数列示例")
    print("=" * 50)
    
    # 卡塔兰数
    print(f"\n前 10 个卡塔兰数: {generate_catalan_sequence(10)}")
    print("应用: 合法括号序列、二叉树形态、出栈序列等")
    
    # 斯特林数
    print(f"\n第二类斯特林数 S(5, k): {[stirling_second(5, k) for k in range(6)]}")
    print("应用: 将 5 个元素分成 k 个非空子集的方法数")
    
    # 贝尔数
    print(f"\n前 8 个贝尔数: {[bell_number(i) for i in range(8)]}")
    print("应用: 将 n 个元素分成非空子集的总方法数")
    
    # 错排数
    print(f"\n前 8 个错排数: {[derangements(i) for i in range(8)]}")
    print("应用: 完全没有元素在原始位置的排列数")
    
    # 分拆数
    print(f"\n前 10 个分拆数: {[partition_number(i) for i in range(10)]}")
    print("应用: 将 n 分拆成正整数之和的方法数")


def example_partition_generator():
    """整数分拆生成器示例"""
    print("\n" + "=" * 50)
    print("整数分拆生成器示例")
    print("=" * 50)
    
    n = 5
    print(f"\n{n} 的所有分拆:")
    for p in partitions(n):
        print(f"  {p} = {' + '.join(map(str, p))}")


def example_pigeonhole():
    """抽屉原理示例"""
    print("\n" + "=" * 50)
    print("抽屉原理示例")
    print("=" * 50)
    
    # 经典问题：13 个人中至少有 2 个人生日在同一月
    people = 13
    months = 12
    min_shared = pigeonhole_count(people, months)
    print(f"\n{people} 个人分到 {months} 个月")
    print(f"至少有 {min_shared} 个人生日在同一月")
    
    # 另一个例子
    socks = 10
    drawers = 3
    min_socks = pigeonhole_count(socks, drawers)
    print(f"\n{socks} 只袜子放入 {drawers} 个抽屉")
    print(f"至少有一个抽屉有 {min_socks} 只袜子")


def example_nth_access():
    """第 N 个元素访问示例"""
    print("\n" + "=" * 50)
    print("第 N 个元素直接访问")
    print("=" * 50)
    
    elements = list(range(1, 11))  # [1, 2, ..., 10]
    
    # 第 100 个组合
    idx = 100
    comb = nth_combination(elements, 3, idx)
    print(f"\n{elements} 取 3 的第 {idx} 个组合: {comb}")
    
    # 第 1000 个排列
    idx = 1000
    perm = nth_permutation(elements, None, idx)
    print(f"{elements} 的第 {idx} 个排列: {perm}")


def example_random_generation():
    """随机生成示例"""
    print("\n" + "=" * 50)
    print("随机生成示例")
    print("=" * 50)
    
    # 随机组合
    print(f"\n从 100 个元素中随机选 5 个: {generate_random_combination(100, 5)}")
    
    # 随机排列
    print(f"0-9 的随机排列: {generate_random_permutation(10)}")


def example_anagrams():
    """变位词计数示例"""
    print("\n" + "=" * 50)
    print("变位词计数示例")
    print("=" * 50)
    
    words = ['abc', 'aab', 'MISSISSIPPI', 'hello']
    for word in words:
        count = count_anagrams(word)
        print(f"\n'{word}' 的变位词数量: {count}")


def example_subset_sum():
    """子集和问题示例"""
    print("\n" + "=" * 50)
    print("子集和问题示例")
    print("=" * 50)
    
    numbers = [3, 34, 4, 12, 5, 2]
    target = 9
    
    result = subset_sum(numbers, target)
    print(f"\n从 {numbers} 中找和为 {target} 的子集")
    if result:
        print(f"找到: {result} (和为 {sum(result)})")
    else:
        print("无解")


def example_pascal_triangle():
    """帕斯卡三角形示例"""
    print("\n" + "=" * 50)
    print("帕斯卡三角形")
    print("=" * 50)
    
    rows = 8
    triangle = generate_pascal_triangle(rows)
    
    print()
    for i, row in enumerate(triangle):
        # 居中格式化
        padding = ' ' * (rows - i - 1)
        print(f"{padding}{' '.join(f'{n:3}' for n in row)}")


def example_practical_problem():
    """实际问题示例：彩票计算"""
    print("\n" + "=" * 50)
    print("实际问题：彩票中奖概率")
    print("=" * 50)
    
    # 双色球：从 33 个红球选 6 个，从 16 个蓝球选 1 个
    red_total = 33
    red_select = 6
    blue_total = 16
    
    total_combinations = binomial(red_total, red_select) * blue_total
    print(f"\n双色球总组合数: {total_combinations:,}")
    print(f"约 1/{total_combinations:,} 的中奖概率")
    
    # 中一等奖概率
    first_prize_prob = 1 / total_combinations
    print(f"一等奖概率: {first_prize_prob:.10e}")
    
    # 中红球 6 个的方法数
    print(f"\n只考虑红球，C({red_total}, {red_select}) = {binomial(red_total, red_select):,}")


def example_bracket_sequences():
    """实际问题示例：括号序列"""
    print("\n" + "=" * 50)
    print("实际问题：合法括号序列")
    print("=" * 50)
    
    n = 4  # n 对括号
    count = catalan(n)
    print(f"\n{n} 对括号的合法序列数量: {count}")
    print("(卡塔兰数 C_n)")
    
    # 应用
    print("\n卡塔兰数的其他应用:")
    print(f"  - {n} 个节点的二叉搜索树形态数: {catalan(n)}")
    print(f"  - {n} 对括号的合法序列数: {catalan(n)}")
    print(f"  - {n+1} 个叶子的满二叉树数: {catalan(n)}")


if __name__ == '__main__':
    example_basic_calculations()
    example_permutations()
    example_combinations()
    example_cartesian_and_powerset()
    example_special_sequences()
    example_partition_generator()
    example_pigeonhole()
    example_nth_access()
    example_random_generation()
    example_anagrams()
    example_subset_sum()
    example_pascal_triangle()
    example_practical_problem()
    example_bracket_sequences()
    
    print("\n" + "=" * 50)
    print("所有示例运行完成！")
    print("=" * 50)