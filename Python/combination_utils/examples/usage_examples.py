"""
Combination Utilities 使用示例

展示组合数学工具的各种使用场景：
1. 组合数和排列数计算
2. 排列和组合生成
3. 幂集和子集生成
4. 康托编码（排列索引化）
5. 特殊数计算（卡特兰数、斯特林数、贝尔数）
6. 错位排列（乱序问题）
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    CombinationCalculator,
    PermutationGenerator,
    CantorEncoder,
    SpecialNumbers,
    CombinationUtils,
    C,
    P,
    factorial,
    catalan,
    generate_permutations,
    generate_combinations,
    generate_powerset,
)


def example_basic_calculations():
    """
    示例 1: 基本组合计算
    
    应用场景：
    - 概率计算
    - 抽样分析
    - 组合优化
    """
    print("=" * 60)
    print("示例 1: 基本组合计算")
    print("=" * 60)
    
    calc = CombinationCalculator()
    
    print("\n--- 阶乘 ---")
    for n in range(1, 11):
        print(f"{n}! = {calc.factorial(n)}")
    
    print("\n--- 组合数 C(n, k) ---")
    print("从 10 个元素中选取不同数量的组合数：")
    for k in range(0, 11):
        print(f"C(10, {k}) = {calc.combination(10, k)}")
    
    print("\n--- 排列数 P(n, k) ---")
    print("从 10 个元素中选取不同数量的排列数：")
    for k in range(0, 11):
        print(f"P(10, {k}) = {calc.permutation(10, k)}")
    
    print("\n--- 组合数性质 ---")
    print("对称性：C(n, k) = C(n, n-k)")
    print(f"C(20, 5) = {calc.combination(20, 5)}")
    print(f"C(20, 15) = {calc.combination(20, 15)}")
    
    print("\n--- 多重组合数 ---")
    print("将 6 个不同元素分成 2, 2, 2 三组：")
    print(f"多重组合数 = {calc.multinomial(2, 2, 2)}")
    
    print()


def example_permutation_generation():
    """
    示例 2: 排列生成
    
    应用场景：
    - 全排列生成
    - 调度问题
    - 序列分析
    """
    print("=" * 60)
    print("示例 2: 排列生成")
    print("=" * 60)
    
    gen = PermutationGenerator()
    
    print("\n--- 全排列 ---")
    items = [1, 2, 3]
    perms = gen.generate_permutations(items)
    print(f"{items} 的所有排列：")
    for p in perms:
        print(f"  {p}")
    
    print(f"\n总数量：{len(perms)} = 3! = {factorial(3)}")
    
    print("\n--- k-排列 ---")
    items = ['A', 'B', 'C', 'D']
    k = 2
    perms = gen.generate_k_permutations(items, k)
    print(f"从 {items} 中选取 {k} 个的排列：")
    for p in perms:
        print(f"  {p}")
    
    print(f"\n总数量：{len(perms)} = P(4, 2) = {P(4, 2)}")
    
    print("\n--- 有重复的排列 ---")
    items = [1, 2]
    k = 3
    perms = gen.generate_permutations_with_repetition(items, k)
    print(f"从 {items} 中选取 {k} 个（可重复）的排列：")
    for p in perms[:10]:  # 只显示前 10 个
        print(f"  {p}")
    
    print(f"\n总数量：{len(perms)} = 2^3 = {len(items) ** k}")
    
    print()


def example_combination_generation():
    """
    示例 3: 组合生成
    
    应用场景：
    - 子集枚举
    - 组合优化
    - 集合选择
    """
    print("=" * 60)
    print("示例 3: 组合生成")
    print("=" * 60)
    
    gen = PermutationGenerator()
    
    print("\n--- k-组合 ---")
    items = ['A', 'B', 'C', 'D', 'E']
    k = 3
    combs = gen.generate_combinations(items, k)
    print(f"从 {items} 中选取 {k} 个的组合：")
    for c in combs:
        print(f"  {c}")
    
    print(f"\n总数量：{len(combs)} = C(5, 3) = {C(5, 3)}")
    
    print("\n--- 所有组合 ---")
    items = [1, 2, 3, 4]
    all_combs = gen.generate_all_combinations(items)
    print(f"{items} 的所有组合（按大小）：")
    for c in all_combs:
        print(f"  {c}")
    
    print(f"\n总数量：{len(all_combs)} = 2^4 - 1 + 1（含空集）= {len(all_combs)}")
    
    print("\n--- 有重复的组合 ---")
    items = [1, 2, 3]
    k = 2
    combs = gen.generate_combinations_with_repetition(items, k)
    print(f"从 {items} 中选取 {k} 个（可重复）的组合：")
    for c in combs:
        print(f"  {c}")
    
    # 有重复组合公式：C(n+k-1, k)
    n = len(items)
    expected_count = C(n + k - 1, k)
    print(f"\n总数量：{len(combs)} = C({n+k-1}, {k}) = {expected_count}")
    
    print()


def example_powerset():
    """
    示例 4: 幂集生成
    
    应用场景：
    - 子集枚举
    - 组合优化（遍历所有可能性）
    - 特征选择
    """
    print("=" * 60)
    print("示例 4: 幂集生成")
    print("=" * 60)
    
    gen = PermutationGenerator()
    
    print("\n--- 幂集（所有子集）---")
    items = ['a', 'b', 'c']
    power = gen.generate_powerset(items)
    
    print(f"{items} 的幂集：")
    for subset in power:
        print(f"  {subset}")
    
    print(f"\n总数量：{len(power)} = 2^3 = {2 ** len(items)}")
    
    print("\n--- 使用迭代器节省内存 ---")
    count = 0
    for subset in gen.iter_powerset(items):
        count += 1
        if count <= 5:
            print(f"  {subset}")
    
    print(f"\n迭代完成，共 {count} 个子集")
    
    print("\n--- 大集合幂集 ---")
    items = [1, 2, 3, 4, 5]
    print(f"{items} 的幂集大小：{gen.count_powerset(len(items))}")
    # 实际生成会占用大量内存，这里只计数
    
    print()


def example_cantor_encoding():
    """
    示例 5: 康托编码
    
    应用场景：
    - 排列索引化（压缩存储）
    - 排列排名
    - 排列生成（从索引）
    
    康托展开可以将排列映射到唯一的索引。
    """
    print("=" * 60)
    print("示例 5: 康托编码")
    print("=" * 60)
    
    encoder = CantorEncoder()
    
    print("\n--- 排列到索引 ---")
    # 三个元素的排列索引
    elements = [0, 1, 2]
    
    perms = generate_permutations(elements)
    print(f"{elements} 的所有排列及其康托索引：")
    
    for perm in perms:
        idx = encoder.encode(perm)
        print(f"  排列 {perm} -> 索引 {idx}")
    
    print("\n--- 索引到排列 ---")
    for i in range(6):  # 3! = 6
        perm = encoder.decode(i, elements)
        print(f"  索引 {i} -> 排列 {perm}")
    
    print("\n--- 应用：排列压缩 ---")
    # 将排列压缩为整数索引
    perm = [3, 2, 1, 0]  # 4 个元素
    idx = encoder.encode(perm)
    print(f"排列 {perm} 压缩为索引 {idx}")
    print(f"存储大小：整数 {idx}（约 {len(str(idx))} 字节）")
    
    # 解压还原
    decoded = encoder.decode(idx, [0, 1, 2, 3])
    print(f"索引 {idx} 还原为排列 {decoded}")
    
    print()


def example_catalan_numbers():
    """
    示例 6: 卡特兰数
    
    应用场景：
    - 有效括号序列数量
    - 二叉树形态数量
    - 出栈序列数量
    - 路径计数问题
    """
    print("=" * 60)
    print("示例 6: 卡特兰数")
    print("=" * 60)
    
    special = SpecialNumbers()
    
    print("\n--- 卡特兰数序列 ---")
    print("Catalan(n) = C(2n, n) / (n+1)")
    
    for n in range(15):
        c = special.catalan(n)
        print(f"Catalan({n}) = {c}")
    
    print("\n--- 应用场景解释 ---")
    print("Catalan(3) = 5 的含义：")
    print("  1. 3 对括号的有效组合数：()()(), (())(), ()(()), (()()), ((()))")
    print("  2. 3 个节点的二叉树形态数：5 种不同的形态")
    print("  3. 3 个元素的出栈序列数：5 种合法的出栈顺序")
    
    print("\n--- 例子：括号组合 ---")
    # 生成 3 对括号的所有有效组合（简化展示）
    print("3 对括号的 5 种有效组合：")
    print("  ()()()")
    print("  (())()")
    print("  ()(())")
    print("  (()())")
    print("  ((()))")
    
    print()


def example_stirling_numbers():
    """
    示例 7: 斯特林数
    
    应用场景：
    - 第二类斯特林数：集合划分计数
    - 第一类斯特林数：圆排列计数
    - 组合分析
    """
    print("=" * 60)
    print("示例 7: 斯特林数")
    print("=" * 60)
    
    special = SpecialNumbers()
    
    print("\n--- 第二类斯特林数 S(n, k) ---")
    print("将 n 个元素分成 k 个非空集合的方案数")
    
    # 打印斯特林数表
    print("\nS(n, k) 表（n=1..6, k=1..n）：")
    print("n\\k |", end="")
    for k in range(1, 7):
        print(f" {k:4}", end="")
    print()
    
    for n in range(1, 7):
        print(f" {n}  |", end="")
        for k in range(1, n + 1):
            s = special.stirling_second(n, k)
            print(f" {s:4}", end="")
        print()
    
    print("\n例子：S(4, 2) = 7")
    print("将 {1,2,3,4} 分成 2 个非空集合的 7 种方式：")
    print("  {{1},{2,3,4}}, {{2},{1,3,4}}, {{3},{1,2,4}}, {{4},{1,2,3}}")
    print("  {{1,2},{3,4}}, {{1,3},{2,4}}, {{1,4},{2,3}}")
    
    print("\n--- 第一类斯特林数 ---")
    print("将 n 个元素排成 k 个圆排列的方案数")
    
    print("\n例子：S(4, 2) = 11")
    print("4 个元素排成 2 个圆排列有 11 种方式")
    
    print()


def example_bell_numbers():
    """
    示例 8: 贝尔数
    
    应用场景：
    - 集合划分总数
    - 组合分析
    """
    print("=" * 60)
    print("示例 8: 贝尔数")
    print("=" * 60)
    
    special = SpecialNumbers()
    
    print("\n--- 贝尔数序列 ---")
    print("B(n) = 将 n 个元素分成任意非空集合的总方案数")
    print("B(n) = S(n, 0) + S(n, 1) + ... + S(n, n)")
    
    for n in range(10):
        b = special.bell(n)
        print(f"B({n}) = {b}")
    
    print("\n例子：B(4) = 15")
    print("将 4 个元素分成任意非空集合的总方案数：")
    print("  分成 1 组：1 种")
    print("  分成 2 组：7 种")
    print("  分成 3 组：6 种")
    print("  分成 4 组：1 种")
    print("  总计：15 种")
    
    print()


def example_derangement():
    """
    示例 9: 错位排列
    
    应用场景：
    - 乱序问题
    - 信封问题（每个人收到错误的信）
    - 抽奖问题
    """
    print("=" * 60)
    print("示例 9: 错位排列")
    print("=" * 60)
    
    special = SpecialNumbers()
    
    print("\n--- 错位排列数 ---")
    print("D(n) = 所有元素都不在原位置的排列数")
    
    for n in range(11):
        d = special.derangement(n)
        print(f"D({n}) = {d}")
    
    print("\n例子：D(4) = 9")
    print("4 个元素的所有错位排列：")
    
    # 生成并验证错位排列
    items = [1, 2, 3, 4]
    perms = generate_permutations(items)
    
    derangements = []
    for perm in perms:
        # 检查是否所有位置都错位
        is_derangement = all(perm[i] != items[i] for i in range(len(perm)))
        if is_derangement:
            derangements.append(perm)
    
    print(f"找到 {len(derangements)} 个错位排列：")
    for d in derangements:
        print(f"  {d}")
    
    print()


def example_practical_usage():
    """
    示例 10: 实际应用场景
    
    应用场景：
    - 抽样计算
    - 调度优化
    - 数据分析
    """
    print("=" * 60)
    print("示例 10: 实际应用场景")
    print("=" * 60)
    
    print("\n--- 概率计算 ---")
    # 从 52 张扑克牌中抽取 5 张
    total_hands = C(52, 5)
    print(f"扑克牌 5 张牌的组合数：{total_hands}")
    
    # 计算特定牌型的概率
    # 同花顺：4 种花色 × 10 种顺子（A-5 到 10-A）
    straight_flush = 4 * 10
    prob = straight_flush / total_hands
    print(f"同花顺概率：{prob:.10f} ({straight_flush}/{total_hands})")
    
    print("\n--- 调度问题 ---")
    # 5 个任务，3 个工人，每个工人执行一个任务
    task_assignments = P(5, 3)
    print(f"5 个任务分配给 3 个工人的方案数：{task_assignments}")
    
    print("\n--- 分组问题 ---")
    # 12 个人分成 3 个 4 人小组
    group_divisions = C(12, 4) * C(8, 4) * C(4, 4) // factorial(3)  # 除以组数阶乘
    calc = CombinationCalculator()
    print(f"12 人分成 3 个 4 人小组的方案数：{group_divisions}")
    
    print()


def run_all_examples():
    """运行所有示例"""
    example_basic_calculations()
    example_permutation_generation()
    example_combination_generation()
    example_powerset()
    example_cantor_encoding()
    example_catalan_numbers()
    example_stirling_numbers()
    example_bell_numbers()
    example_derangement()
    example_practical_usage()
    
    print("=" * 60)
    print("所有示例完成！")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()