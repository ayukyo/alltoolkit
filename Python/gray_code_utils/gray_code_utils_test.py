#!/usr/bin/env python3
"""
gray_code_utils_test.py - Gray码工具集测试

测试内容：
- 基础转换测试
- Gray码序列生成测试
- Johnson码测试
- 相邻检测测试
- n维Gray码测试
- 位置编码器测试
- 汉诺塔测试
- 循环验证测试
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    binary_to_gray, gray_to_binary,
    binary_to_gray_bits, gray_bits_to_binary,
    generate_gray_codes, generate_gray_codes_iterative,
    gray_code_generator, generate_gray_codes_binary,
    generate_johnson_codes, generate_johnson_codes_binary,
    gray_distance, are_adjacent_gray, find_changed_bit,
    gray_hamming_weight,
    generate_n_dimensional_gray, generate_2d_gray,
    sort_by_gray, sort_by_gray_binary,
    is_cyclic_gray_sequence, complete_gray_cycle,
    gray_code_position_encoder, decode_gray_position,
    hanoi_moves_gray, gray_code_kmap_index,
    generate_balanced_gray_codes, generate_beckett_gray_codes,
    count_transitions, is_valid_gray_sequence, get_transition_sequence,
    invert_bit_at_position
)


def test_basic_conversion():
    """测试基础转换"""
    print("\n[测试] 基础转换")
    
    # 测试 binary_to_gray
    test_cases = [
        (0, 0), (1, 1), (2, 3), (3, 2), (4, 6), (5, 7), (6, 5), (7, 4),
        (8, 12), (9, 13), (10, 15), (11, 14), (12, 10), (13, 11), (14, 9), (15, 8)
    ]
    
    for binary, expected_gray in test_cases:
        result = binary_to_gray(binary)
        assert result == expected_gray, f"binary_to_gray({binary}) = {result}, 期望 {expected_gray}"
    
    print("  ✓ binary_to_gray 测试通过")
    
    # 测试 gray_to_binary
    for binary, gray in test_cases:
        result = gray_to_binary(gray)
        assert result == binary, f"gray_to_binary({gray}) = {result}, 期望 {binary}"
    
    print("  ✓ gray_to_binary 测试通过")
    
    # 测试往返转换
    for i in range(100):
        gray = binary_to_gray(i)
        recovered = gray_to_binary(gray)
        assert recovered == i, f"往返转换失败: {i} -> {gray} -> {recovered}"
    
    print("  ✓ 往返转换测试通过（0-99）")


def test_bit_conversion():
    """测试位列表转换"""
    print("\n[测试] 位列表转换")
    
    test_cases = [
        ([0, 0], [0, 0]),
        ([0, 1], [0, 1]),
        ([1, 0], [1, 1]),
        ([1, 1], [1, 0]),
        ([1, 0, 1, 1], [1, 1, 1, 0]),
    ]
    
    for binary, expected_gray in test_cases:
        result = binary_to_gray_bits(binary)
        assert result == expected_gray, f"binary_to_gray_bits({binary}) = {result}, 期望 {expected_gray}"
        # 往返测试
        recovered = gray_bits_to_binary(result)
        assert recovered == binary, f"gray_bits_to_binary 往返失败"
    
    print("  ✓ 位列表转换测试通过")


def test_gray_code_generation():
    """测试Gray码生成"""
    print("\n[测试] Gray码生成")
    
    # 测试不同位数
    for n in range(1, 6):
        codes = generate_gray_codes(n)
        expected_count = 2 ** n
        assert len(codes) == expected_count, f"{n}位Gray码应有{expected_count}个，得到{len(codes)}"
        
        # 验证所有值唯一
        assert len(set(codes)) == expected_count, f"{n}位Gray码有重复值"
        
        # 验证相邻性
        for i in range(len(codes) - 1):
            assert are_adjacent_gray(codes[i], codes[i+1]), f"{n}位Gray码位置{i}和{i+1}不相邻"
        
        # 验证循环性（首尾相邻）
        assert are_adjacent_gray(codes[-1], codes[0]), f"{n}位Gray码首尾不相邻"
    
    print("  ✓ generate_gray_codes 测试通过（1-5位）")
    
    # 测试迭代版本
    for n in range(1, 6):
        recursive = generate_gray_codes(n)
        iterative = generate_gray_codes_iterative(n)
        assert recursive == iterative, f"递归和迭代版本结果不一致（n={n}）"
    
    print("  ✓ 迭代版本与递归版本一致性测试通过")
    
    # 测试生成器
    for n in range(1, 5):
        codes_list = list(gray_code_generator(n))
        expected = generate_gray_codes(n)
        assert codes_list == expected, f"生成器结果不一致（n={n}）"
    
    print("  ✓ 生成器测试通过")
    
    # 测试二进制字符串输出
    binary_codes = generate_gray_codes_binary(3)
    expected_binary = ['000', '001', '011', '010', '110', '111', '101', '100']
    assert binary_codes == expected_binary, f"二进制输出: {binary_codes}, 期望 {expected_binary}"
    
    print("  ✓ 二进制字符串输出测试通过")


def test_johnson_codes():
    """测试Johnson计数器码"""
    print("\n[测试] Johnson计数器码")
    
    # 测试3位Johnson码
    codes_3 = generate_johnson_codes(3)
    expected_3 = [0, 1, 3, 7, 6, 4]  # 000, 001, 011, 111, 110, 100
    assert codes_3 == expected_3, f"3位Johnson码: {codes_3}, 期望 {expected_3}"
    
    print("  ✓ Johnson码生成测试通过")
    
    # 测试二进制输出
    binary = generate_johnson_codes_binary(2)
    expected_binary = ['00', '01', '11', '10']
    assert binary == expected_binary, f"Johnson二进制: {binary}, 期望 {expected_binary}"
    
    print("  ✓ Johnson二进制输出测试通过")


def test_adjacency():
    """测试相邻检测"""
    print("\n[测试] 相邻检测")
    
    # 测试相邻码（相邻 = 只差一位）
    assert are_adjacent_gray(0, 1) == True   # 000 vs 001 - 只差1位
    assert are_adjacent_gray(1, 3) == True   # 001 vs 011 - 只差1位
    assert are_adjacent_gray(3, 2) == True   # 011 vs 010 - 只差1位
    assert are_adjacent_gray(0, 2) == True   # 000 vs 010 - 只差1位！
    assert are_adjacent_gray(0, 3) == False  # 000 vs 011 - 差2位，不相邻
    assert are_adjacent_gray(0, 0) == False  # 相同
    
    print("  ✓ are_adjacent_gray 测试通过")
    
    # 测试距离
    assert gray_distance(0, 1) == 1
    assert gray_distance(0, 3) == 2
    assert gray_distance(0, 7) == 3
    assert gray_distance(5, 5) == 0
    
    print("  ✓ gray_distance 测试通过")
    
    # 测试改变位
    assert find_changed_bit(0, 1) == 0   # 第0位改变
    assert find_changed_bit(1, 3) == 1   # 第1位改变
    assert find_changed_bit(0, 2) == 1   # 第1位改变（000->010）
    assert find_changed_bit(0, 3) is None  # 不相邻（差2位）
    assert find_changed_bit(5, 5) is None  # 相同
    
    print("  ✓ find_changed_bit 测试通过")
    
    # 测试汉明重量
    assert gray_hamming_weight(7) == 3   # 111
    assert gray_hamming_weight(5) == 2   # 101
    assert gray_hamming_weight(0) == 0
    
    print("  ✓ gray_hamming_weight 测试通过")


def test_n_dimensional():
    """测试n维Gray码"""
    print("\n[测试] n维Gray码")
    
    # 测试2维（顺序取决于维度映射，两种都是有效的Gray序列）
    coords_2d = generate_n_dimensional_gray(2, 1)
    # 验证序列有效性：相邻坐标只在一个维度变化
    for i in range(len(coords_2d) - 1):
        prev, curr = coords_2d[i], coords_2d[i+1]
        changes = sum(1 for a, b in zip(prev, curr) if a != b)
        assert changes == 1, f"相邻坐标应只变一个维度: {prev} -> {curr}"
    # 验证首尾循环性
    changes = sum(1 for a, b in zip(coords_2d[-1], coords_2d[0]) if a != b)
    assert changes == 1, f"首尾应只变一个维度"
    
    print("  ✓ 2维Gray码测试通过")
    
    # 测试3维
    coords_3d = generate_n_dimensional_gray(3, 1)
    assert len(coords_3d) == 8, f"3维Gray码应有8个点，得到{len(coords_3d)}"
    
    print("  ✓ 3维Gray码测试通过")


def test_sorting():
    """测试Gray码排序"""
    print("\n[测试] Gray码排序")
    
    values = [3, 0, 2, 1]
    sorted_vals = sort_by_gray(values)
    expected = [0, 1, 3, 2]  # Gray码顺序
    assert sorted_vals == expected, f"排序结果: {sorted_vals}, 期望 {expected}"
    
    print("  ✓ sort_by_gray 测试通过")
    
    # 测试二进制排序
    bin_values = ['11', '00', '10', '01']
    sorted_bin = sort_by_gray_binary(bin_values)
    expected_bin = ['00', '01', '11', '10']
    assert sorted_bin == expected_bin, f"二进制排序: {sorted_bin}, 期望 {expected_bin}"
    
    print("  ✓ sort_by_gray_binary 测试通过")


def test_cycle_validation():
    """测试循环验证"""
    print("\n[测试] 循环验证")
    
    # 有效循环
    codes_3 = generate_gray_codes(3)
    assert is_cyclic_gray_sequence(codes_3, 3) == True
    
    print("  ✓ 有效循环检测通过")
    
    # 无效循环（不完整的序列）
    partial = [0, 1, 3]
    assert is_cyclic_gray_sequence(partial, 3) == False
    
    print("  ✓ 无效循环检测通过")
    
    # 测试完整循环
    cycle = complete_gray_cycle(3, 2)
    assert cycle[0] == 2, f"循环应从2开始: {cycle[0]}"
    assert are_adjacent_gray(cycle[-1], cycle[0]), "循环首尾应相邻"
    
    print("  ✓ complete_gray_cycle 测试通过")


def test_position_encoder():
    """测试位置编码器"""
    print("\n[测试] 位置编码器")
    
    # 测试编码
    for pos in range(16):
        gray_str = gray_code_position_encoder(pos, 4)
        assert len(gray_str) == 4, f"编码长度应为4，得到{len(gray_str)}"
        
        # 测试解码
        decoded = decode_gray_position(gray_str)
        assert decoded == pos, f"解码错误: {pos} -> {gray_str} -> {decoded}"
    
    print("  ✓ 位置编码器编码/解码测试通过")
    
    # 测试边界
    try:
        gray_code_position_encoder(16, 4)  # 超出范围
        assert False, "应抛出异常"
    except ValueError:
        pass
    
    print("  ✓ 边界检查测试通过")


def test_hanoi():
    """测试汉诺塔"""
    print("\n[测试] 汉诺塔")
    
    # 测试不同盘子数量
    for n in range(1, 5):
        moves = hanoi_moves_gray(n)
        expected_moves = 2 ** n - 1
        assert len(moves) == expected_moves, f"{n}盘汉诺塔应有{expected_moves}步，得到{len(moves)}"
        
        # 验证移动有效性
        # 每个移动应在0, 1, 2范围内
        for src, dst in moves:
            assert 0 <= src <= 2 and 0 <= dst <= 2, f"无效移动: ({src}, {dst})"
            assert src != dst, f"源和目标相同: {src}"
    
    print("  ✓ 汉诺塔测试通过")


def test_kmap():
    """测试Karnaugh图索引"""
    print("\n[测试] Karnaugh图索引")
    
    # 测试不同变量数
    for vars in range(1, 5):
        idx = gray_code_kmap_index(vars)
        expected_count = 2 ** vars
        assert len(idx) == expected_count, f"{vars}变量Kmap应有{expected_count}索引"
        
        # 验证相邻性
        for i in range(len(idx) - 1):
            assert are_adjacent_gray(idx[i], idx[i+1]), f"Kmap索引{i}和{i+1}不相邻"
    
    print("  ✓ Karnaugh图索引测试通过")


def test_transitions():
    """测试跳变统计"""
    print("\n[测试] 跳变统计")
    
    codes = generate_gray_codes(4)
    transitions = count_transitions(codes)
    # 16个码，15个跳变，每个跳变1位
    assert transitions == 15, f"4位Gray码应有15次跳变，得到{transitions}"
    
    print("  ✓ count_transitions 测试通过")
    
    # 验证序列有效性
    assert is_valid_gray_sequence(codes) == True
    
    print("  ✓ is_valid_gray_sequence 测试通过")
    
    # 测试跳变序列
    trans_seq = get_transition_sequence(codes)
    assert len(trans_seq) == 15, f"跳变序列长度应为15"
    
    # 所有跳变应在有效范围内（0-3）
    for t in trans_seq:
        assert 0 <= t <= 3, f"无效跳变位: {t}"
    
    print("  ✓ get_transition_sequence 测试通过")


def test_invert_bit():
    """测试位反转"""
    print("\n[测试] 位反转")
    
    # 反转第0位
    assert invert_bit_at_position(0, 0) == 1   # 000 -> 001
    assert invert_bit_at_position(1, 0) == 0   # 001 -> 000
    
    # 反转第1位
    assert invert_bit_at_position(0, 1) == 2   # 000 -> 010
    assert invert_bit_at_position(3, 1) == 1   # 011 -> 001
    
    # 反转第2位
    assert invert_bit_at_position(0, 2) == 4   # 000 -> 100
    assert invert_bit_at_position(7, 2) == 3   # 111 -> 011
    
    print("  ✓ invert_bit_at_position 测试通过")


def test_special_gray_codes():
    """测试特殊Gray码"""
    print("\n[测试] 特殊Gray码")
    
    # 测试平衡Gray码
    balanced = generate_balanced_gray_codes(3)
    standard = generate_gray_codes(3)
    assert balanced == standard, "3位平衡Gray码应与标准相同"
    
    print("  ✓ generate_balanced_gray_codes 测试通过")
    
    # 测试Beckett-Gray码
    beckett = generate_beckett_gray_codes(2)
    expected = [0, 1, 3, 2]
    assert beckett == expected, f"Beckett码: {beckett}, 期望 {expected}"
    
    print("  ✓ generate_beckett_gray_codes 测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Gray码工具集测试")
    print("=" * 60)
    
    test_basic_conversion()
    test_bit_conversion()
    test_gray_code_generation()
    test_johnson_codes()
    test_adjacency()
    test_n_dimensional()
    test_sorting()
    test_cycle_validation()
    test_position_encoder()
    test_hanoi()
    test_kmap()
    test_transitions()
    test_invert_bit()
    test_special_gray_codes()
    
    print("\n" + "=" * 60)
    print("所有测试通过！ ✓")
    print("=" * 60)


if __name__ == '__main__':
    run_all_tests()