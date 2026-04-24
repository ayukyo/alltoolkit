"""
Permutation Utils 测试文件
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    PermutationUtils,
    CombinationUtils,
    PermutationUtilsAdvanced,
    permutations,
    combinations,
    permutation_count,
    combination_count,
    factorial_val,
)


def test_permutation_basic():
    """测试基本排列功能"""
    print("=== 测试基本排列 ===")
    
    # 测试全排列
    perm_list = list(PermutationUtils.permutations([1, 2, 3]))
    print(f"[1,2,3] 的全排列 ({len(perm_list)} 个):")
    for p in perm_list:
        print(f"  {p}")
    assert len(perm_list) == 6
    
    # 测试部分排列
    perm_list = list(PermutationUtils.permutations([1, 2, 3, 4], 2))
    print(f"\n[1,2,3,4] 的 2-排列 ({len(perm_list)} 个):")
    for p in perm_list:
        print(f"  {p}")
    assert len(perm_list) == 12
    
    print("✅ 基本排列测试通过")


def test_permutation_count():
    """测试排列数计算"""
    print("\n=== 测试排列数计算 ===")
    
    assert permutation_count(5, 3) == 60
    assert permutation_count(4) == 24
    assert permutation_count(4, 0) == 1
    assert permutation_count(4, 4) == 24
    assert permutation_count(4, 5) == 0
    
    print(f"P(5, 3) = {permutation_count(5, 3)}")
    print(f"P(4) = {permutation_count(4)}")
    print("✅ 排列数计算测试通过")


def test_permutation_rank():
    """测试排列序号"""
    print("\n=== 测试排列序号 ===")
    
    # 测试字典序编号
    assert PermutationUtils.permutation_rank((1, 2, 3)) == 0
    assert PermutationUtils.permutation_rank((3, 2, 1)) == 5
    
    print("(1,2,3) 的序号: 0")
    print("(3,2,1) 的序号: 5")
    
    # 测试逆序
    assert PermutationUtils.permutation_unrank(0, [1, 2, 3]) == (1, 2, 3)
    assert PermutationUtils.permutation_unrank(5, [1, 2, 3]) == (3, 2, 1)
    
    print("序号 0 -> (1,2,3)")
    print("序号 5 -> (3,2,1)")
    
    # 验证双向转换
    for i in range(6):
        perm = PermutationUtils.permutation_unrank(i, [1, 2, 3])
        rank = PermutationUtils.permutation_rank(perm)
        assert rank == i, f"序号 {i} 转换失败: {perm} -> {rank}"
    print("✅ 双向转换验证通过")
    
    print("✅ 排列序号测试通过")


def test_next_prev_permutation():
    """测试下一个/上一个排列"""
    print("\n=== 测试下一个/上一个排列 ===")
    
    # 测试下一个排列
    arr = [1, 2, 3]
    result = PermutationUtils.next_permutation(arr)
    assert result == [1, 3, 2]
    print(f"[1,2,3] -> {result}")
    
    result = PermutationUtils.next_permutation(arr)
    assert result == [2, 1, 3]
    print(f"[1,3,2] -> {result}")
    
    # 测试上一个排列
    arr = [3, 2, 1]
    result = PermutationUtils.prev_permutation(arr)
    assert result == [3, 1, 2]
    print(f"[3,2,1] -> {result}")
    
    # 最后一个排列的下一个应该是 None
    arr = [3, 2, 1]
    assert PermutationUtils.next_permutation(arr.copy()) is None
    print("[3,2,1] 的下一个: None ✅")
    
    print("✅ 下一个/上一个排列测试通过")


def test_inversion():
    """测试逆序对"""
    print("\n=== 测试逆序对 ===")
    
    assert PermutationUtils.inversion_count((1, 2, 3)) == 0
    assert PermutationUtils.inversion_count((3, 2, 1)) == 3
    assert PermutationUtils.inversion_count((2, 1, 3)) == 1
    assert PermutationUtils.inversion_count((2, 3, 1)) == 2
    
    print("(1,2,3) 逆序对: 0")
    print("(3,2,1) 逆序对: 3")
    print("(2,1,3) 逆序对: 1")
    print("(2,3,1) 逆序对: 2")
    
    # 测试奇偶性
    assert PermutationUtils.is_even_permutation((1, 2, 3)) == True
    assert PermutationUtils.is_odd_permutation((2, 1, 3)) == True
    assert PermutationUtils.permutation_sign((1, 2, 3)) == 1
    assert PermutationUtils.permutation_sign((2, 1, 3)) == -1
    
    print("✅ 逆序对测试通过")


def test_combination_basic():
    """测试基本组合功能"""
    print("\n=== 测试基本组合 ===")
    
    # 测试组合
    comb_list = list(CombinationUtils.combinations([1, 2, 3, 4], 2))
    print(f"[1,2,3,4] 的 2-组合 ({len(comb_list)} 个):")
    for c in comb_list:
        print(f"  {c}")
    assert len(comb_list) == 6
    
    # 测试组合数
    assert combination_count(5, 2) == 10
    assert combination_count(10, 5) == 252
    assert combination_count(5, 0) == 1
    assert combination_count(5, 5) == 1
    
    print(f"\nC(5, 2) = {combination_count(5, 2)}")
    print(f"C(10, 5) = {combination_count(10, 5)}")
    
    print("✅ 基本组合测试通过")


def test_combination_rank():
    """测试组合序号"""
    print("\n=== 测试组合序号 ===")
    
    elements = [1, 2, 3, 4]
    
    # 测试字典序编号
    rank = CombinationUtils.combination_rank((1, 2), elements)
    assert rank == 0
    print(f"(1, 2) 的序号: 0")
    
    rank = CombinationUtils.combination_rank((3, 4), elements)
    assert rank == 5
    print(f"(3, 4) 的序号: 5")
    
    # 测试逆序
    assert CombinationUtils.combination_unrank(0, elements, 2) == (1, 2)
    assert CombinationUtils.combination_unrank(5, elements, 2) == (3, 4)
    
    # 验证双向转换
    comb_list = list(CombinationUtils.combinations(elements, 2))
    for i, comb in enumerate(comb_list):
        rank = CombinationUtils.combination_rank(comb, elements)
        unrank = CombinationUtils.combination_unrank(i, elements, 2)
        assert rank == i, f"组合 {comb} 序号错误: {rank} != {i}"
        assert unrank == comb, f"序号 {i} 组合错误: {unrank} != {comb}"
    
    print("✅ 双向转换验证通过")
    print("✅ 组合序号测试通过")


def test_all_subsets():
    """测试所有子集"""
    print("\n=== 测试所有子集 ===")
    
    subsets = list(CombinationUtils.all_subsets([1, 2, 3]))
    print(f"[1,2,3] 的所有子集 ({len(subsets)} 个):")
    for s in subsets:
        print(f"  {s}")
    
    assert len(subsets) == 8
    assert () in subsets
    assert (1,) in subsets
    assert (1, 2, 3) in subsets
    
    assert CombinationUtils.subset_count(3) == 8
    assert CombinationUtils.subset_count(4) == 16
    
    print("✅ 子集测试通过")


def test_random_permutation():
    """测试随机排列"""
    print("\n=== 测试随机排列 ===")
    
    p1 = PermutationUtilsAdvanced.random_permutation(10, seed=42)
    p2 = PermutationUtilsAdvanced.random_permutation(10, seed=42)
    assert p1 == p2, "相同种子应产生相同结果"
    print(f"随机排列 (seed=42): {p1}")
    
    # 验证包含 1-10
    assert sorted(p1) == list(range(1, 11))
    print("✅ 排列包含 1-10")
    
    print("✅ 随机排列测试通过")


def test_random_combination():
    """测试随机组合"""
    print("\n=== 测试随机组合 ===")
    
    c1 = PermutationUtilsAdvanced.random_combination(10, 3, seed=42)
    c2 = PermutationUtilsAdvanced.random_combination(10, 3, seed=42)
    assert c1 == c2, "相同种子应产生相同结果"
    print(f"随机组合 (seed=42): {c1}")
    
    # 验证大小和元素范围
    assert len(c1) == 3
    assert all(1 <= x <= 10 for x in c1)
    print("✅ 组合大小正确，元素在范围内")
    
    print("✅ 随机组合测试通过")


def test_multiset_permutations():
    """测试多重集排列"""
    print("\n=== 测试多重集排列 ===")
    
    perm_list = list(PermutationUtilsAdvanced.multiset_permutations([1, 1, 2]))
    print(f"[1,1,2] 的多重集排列 ({len(perm_list)} 个):")
    for p in perm_list:
        print(f"  {p}")
    
    assert len(perm_list) == 3
    assert (1, 1, 2) in perm_list
    assert (1, 2, 1) in perm_list
    assert (2, 1, 1) in perm_list
    
    # 测试多重集排列数
    count = PermutationUtilsAdvanced.multiset_permutation_count([1, 1, 2])
    assert count == 3
    print(f"多重集排列数: {count}")
    
    count = PermutationUtilsAdvanced.multiset_permutation_count([1, 1, 1, 2, 2])
    assert count == 10
    print(f"[1,1,1,2,2] 多重集排列数: {count}")
    
    print("✅ 多重集排列测试通过")


def test_derangements():
    """测试错排"""
    print("\n=== 测试错排 ===")
    
    # 测试错排生成
    der_list = list(PermutationUtilsAdvanced.derangements(3))
    print(f"3 的错排 ({len(der_list)} 个):")
    for d in der_list:
        print(f"  {d}")
    
    assert len(der_list) == 2
    assert (2, 3, 1) in der_list
    assert (3, 1, 2) in der_list
    
    # 测试错排数
    assert PermutationUtilsAdvanced.derangement_count(0) == 1
    assert PermutationUtilsAdvanced.derangement_count(1) == 0
    assert PermutationUtilsAdvanced.derangement_count(2) == 1
    assert PermutationUtilsAdvanced.derangement_count(3) == 2
    assert PermutationUtilsAdvanced.derangement_count(4) == 9
    assert PermutationUtilsAdvanced.derangement_count(5) == 44
    
    print(f"D(0) = 1")
    print(f"D(1) = 0")
    print(f"D(2) = 1")
    print(f"D(3) = 2")
    print(f"D(4) = 9")
    print(f"D(5) = 44")
    
    # 测试错排判断
    assert PermutationUtilsAdvanced.is_derangement((2, 3, 1)) == True
    assert PermutationUtilsAdvanced.is_derangement((3, 1, 2)) == True
    assert PermutationUtilsAdvanced.is_derangement((1, 2, 3)) == False
    
    print("✅ 错排测试通过")


def test_factorial():
    """测试阶乘"""
    print("\n=== 测试阶乘 ===")
    
    assert factorial_val(0) == 1
    assert factorial_val(1) == 1
    assert factorial_val(5) == 120
    assert factorial_val(10) == 3628800
    
    print(f"0! = 1")
    print(f"5! = 120")
    print(f"10! = 3628800")
    
    print("✅ 阶乘测试通过")


def test_convenience_functions():
    """测试便捷函数"""
    print("\n=== 测试便捷函数 ===")
    
    # 测试 permutations
    perm_list = list(permutations([1, 2, 3], 2))
    assert len(perm_list) == 6
    print(f"permutations([1,2,3], 2): {perm_list}")
    
    # 测试 combinations
    comb_list = list(combinations([1, 2, 3, 4], 2))
    assert len(comb_list) == 6
    print(f"combinations([1,2,3,4], 2): {comb_list}")
    
    print("✅ 便捷函数测试通过")


def test_edge_cases():
    """测试边界情况"""
    print("\n=== 测试边界情况 ===")
    
    # 空列表
    assert list(permutations([])) == [()]
    assert list(combinations([], 0)) == [()]
    assert list(combinations([], 1)) == []
    
    # k=0
    assert list(combinations([1, 2, 3], 0)) == [()]
    assert list(permutations([1, 2, 3], 0)) == [()]
    
    # k > n
    assert list(combinations([1, 2], 5)) == []
    assert list(permutations([1, 2], 5)) == []
    
    # 单元素
    assert list(permutations([1])) == [(1,)]
    assert list(combinations([1], 1)) == [(1,)]
    
    print("✅ 边界情况测试通过")


def test_performance():
    """测试性能"""
    print("\n=== 测试性能 ===")
    import time
    
    # 大规模排列序号计算
    start = time.time()
    for i in range(100):
        perm = PermutationUtils.permutation_unrank(i, list(range(10)))
        rank = PermutationUtils.permutation_rank(perm)
        assert rank == i
    elapsed = time.time() - start
    print(f"100次排列序号转换: {elapsed:.4f}s")
    
    # 大规模组合序号计算
    start = time.time()
    for i in range(100):
        comb = CombinationUtils.combination_unrank(i, list(range(20)), 5)
        rank = CombinationUtils.combination_rank(comb, list(range(20)))
        assert rank == i
    elapsed = time.time() - start
    print(f"100次组合序号转换: {elapsed:.4f}s")
    
    # 逆序对计算
    start = time.time()
    inv = PermutationUtils.inversion_count(tuple(range(1000, 0, -1)))
    expected = 1000 * 999 // 2
    assert inv == expected
    elapsed = time.time() - start
    print(f"1000元素逆序对计算: {elapsed:.4f}s (逆序对数: {inv})")
    
    print("✅ 性能测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("Permutation Utils 测试套件")
    print("=" * 50)
    
    test_permutation_basic()
    test_permutation_count()
    test_permutation_rank()
    test_next_prev_permutation()
    test_inversion()
    test_combination_basic()
    test_combination_rank()
    test_all_subsets()
    test_random_permutation()
    test_random_combination()
    test_multiset_permutations()
    test_derangements()
    test_factorial()
    test_convenience_functions()
    test_edge_cases()
    test_performance()
    
    print("\n" + "=" * 50)
    print("🎉 所有测试通过!")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()