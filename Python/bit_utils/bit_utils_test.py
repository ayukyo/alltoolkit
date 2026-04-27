"""
位操作工具集测试 (Bit Utilities Test)
=====================================

全面测试位操作工具集的所有功能。

作者: AllToolkit
日期: 2026-04-16
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    BitVector, BitField, BitMask,
    count_bits, count_zeros, parity,
    find_first_set_bit, find_last_set_bit, find_nth_set_bit,
    most_significant_bit, least_significant_bit,
    reverse_bits, reverse_bytes,
    rotate_left, rotate_right,
    is_power_of_two, next_power_of_two, previous_power_of_two,
    gray_code, gray_to_binary,
    sign_extend, swap_bits,
    align_up, align_down,
    to_binary_string, from_binary_string, to_hex_string,
    create_bitset, bitset_union, bitset_intersection,
    bitset_difference, bitset_symmetric_difference,
    bitset_is_subset, bitset_is_superset, bitset_to_list,
    iterate_bits
)


def test_bit_vector():
    """测试 BitVector 类"""
    print("=== 测试 BitVector ===")
    
    # 初始化
    bv = BitVector(8, 0b10110101)
    assert len(bv) == 8
    assert bv.to_int() == 0b10110101
    print(f"✓ 初始化: {bv}")
    
    # 索引访问
    assert bv[0] == 1
    assert bv[1] == 0
    assert bv[2] == 1
    assert bv[7] == 1
    print("✓ 索引访问正常")
    
    # 设置和清除
    bv[0] = 0
    assert bv[0] == 0
    bv.set(0)
    assert bv[0] == 1
    bv.clear(0)
    assert bv[0] == 0
    print("✓ 设置/清除正常")
    
    # 翻转
    bv.flip(0)
    assert bv[0] == 1
    bv.flip_all()
    assert bv[0] == 0
    print("✓ 翻转正常")
    
    # 位运算
    bv1 = BitVector(4, 0b1010)
    bv2 = BitVector(4, 0b1100)
    assert (bv1 & bv2).to_int() == 0b1000
    assert (bv1 | bv2).to_int() == 0b1110
    assert (bv1 ^ bv2).to_int() == 0b0110
    assert (~bv1).to_int() == 0b0101
    print("✓ 位运算正常")
    
    # 计数
    assert BitVector(8, 0b10110101).count_set_bits() == 5
    assert BitVector(8, 0b10110101).count_clear_bits() == 3
    print("✓ 位计数正常")
    
    # 查找
    bv = BitVector(8, 0b10100000)
    assert bv.find_first_set() == 5
    assert bv.find_last_set() == 7
    print("✓ 位查找正常")
    
    # 转换
    assert BitVector.from_binary_string("1011").to_int() == 0b1011
    assert BitVector.from_list([1, 0, 1, 1]).to_int() == 0b1101
    print("✓ 转换正常")
    
    # 条件检查
    bv = BitVector(8)
    assert bv.none_set()
    assert not bv.any_set()
    assert not bv.all_set()
    
    bv.set(0)
    assert not bv.none_set()
    assert bv.any_set()
    
    bv = BitVector(8, 0xFF)  # 全1
    assert bv.all_set()
    
    bv = BitVector(8, 0)  # 全0
    bv.flip_all()  # 翻转全0变成全1
    assert bv.all_set()
    print("✓ 条件检查正常")
    
    print()


def test_bit_field():
    """测试 BitField 类"""
    print("=== 测试 BitField ===")
    
    # 提取位字段
    # 0b10110100 的位布局: 位2=1, 位3=0, 位4=1 -> 0b101 (5)
    assert BitField.extract(0b10110100, 2, 5) == 0b101
    # 位0-3: 0,0,1,0 -> 0b0010 (2) (从低位开始排列)
    assert BitField.extract(0b10110100, 0, 4) == 0b0100  # 位0-3的值是0100
    print("✓ 位字段提取正常")
    
    # 插入位字段
    result = BitField.insert(0b10110100, 2, 5, 0b111)
    assert result == 0b10111100
    print("✓ 位字段插入正常")
    
    # 单位操作
    value = 0
    value = BitField.set_bit(value, 3)
    assert value == 0b1000
    assert BitField.get_bit(value, 3) == 1
    value = BitField.clear_bit(value, 3)
    assert value == 0
    value = BitField.toggle_bit(value, 5)
    assert value == 0b100000
    print("✓ 单位操作正常")
    
    print()


def test_bit_mask():
    """测试 BitMask 类"""
    print("=== 测试 BitMask ===")
    
    # 创建掩码
    assert BitMask.create_mask([0, 2, 4]) == 0b10101
    assert BitMask.create_range_mask(2, 6) == 0b111100
    print("✓ 掩码创建正常")
    
    # 获取位位置
    assert BitMask.get_set_positions(0b10101) == [0, 2, 4]
    print("✓ 位位置获取正常")
    
    # 掩码操作
    assert BitMask.apply_mask(0b101101, 0b101) == 0b101
    assert BitMask.combine_masks(0b101, 0b011) == 0b111
    assert BitMask.invert_mask(0b101, 4) == 0b1010
    print("✓ 掩码操作正常")
    
    print()


def test_count_bits():
    """测试位计数函数"""
    print("=== 测试位计数 ===")
    
    assert count_bits(0b10110101) == 5
    assert count_bits(0) == 0
    assert count_bits(0xFFFFFFFF) == 32
    print("✓ count_bits 正常")
    
    assert count_zeros(0b10110101, 8) == 3
    assert count_zeros(0, 8) == 8
    print("✓ count_zeros 正常")
    
    assert parity(0b1011) == 1  # 奇数个1
    assert parity(0b1010) == 0  # 偶数个1
    print("✓ parity 正常")
    
    print()


def test_find_bits():
    """测试位查找函数"""
    print("=== 测试位查找 ===")
    
    assert find_first_set_bit(0b10100000) == 5
    assert find_first_set_bit(0b1) == 0
    assert find_first_set_bit(0) == -1
    print("✓ find_first_set_bit 正常")
    
    assert find_last_set_bit(0b10100000) == 7
    assert find_last_set_bit(0b1) == 0
    assert find_last_set_bit(0) == -1
    print("✓ find_last_set_bit 正常")
    
    assert find_nth_set_bit(0b10110100, 1) == 2
    assert find_nth_set_bit(0b10110100, 2) == 4
    assert find_nth_set_bit(0b10110100, 3) == 5
    assert find_nth_set_bit(0b10110100, 4) == 7
    assert find_nth_set_bit(0b10110100, 5) == -1
    print("✓ find_nth_set_bit 正常")
    
    assert most_significant_bit(0b10000) == 4
    assert least_significant_bit(0b10100) == 2
    print("✓ msb/lsb 正常")
    
    print()


def test_reverse_bits():
    """测试位反转函数"""
    print("=== 测试位反转 ===")
    
    assert reverse_bits(0b10110010, 8) == 0b01001101
    assert reverse_bits(0b1, 8) == 0b10000000
    assert reverse_bits(0, 8) == 0
    print("✓ reverse_bits 正常")
    
    assert reverse_bytes(0x12345678) == 0x78563412
    assert reverse_bytes(0x12) == 0x12
    print("✓ reverse_bytes 正常")
    
    print()


def test_rotate_bits():
    """测试位旋转函数"""
    print("=== 测试位旋转 ===")
    
    # 左旋
    assert rotate_left(0b10110001, 3, 8) == 0b10001101
    assert rotate_left(0b10110001, 0, 8) == 0b10110001
    assert rotate_left(0b10110001, 8, 8) == 0b10110001  # 旋转一个周期
    print("✓ rotate_left 正常")
    
    # 右旋
    assert rotate_right(0b10110001, 3, 8) == 0b00110110
    assert rotate_right(0b10110001, 0, 8) == 0b10110001
    print("✓ rotate_right 正常")
    
    # 左右旋互逆
    value = 0b10110100
    assert rotate_right(rotate_left(value, 5, 8), 5, 8) == value
    print("✓ 左右旋互逆正常")
    
    print()


def test_power_of_two():
    """测试2的幂函数"""
    print("=== 测试2的幂 ===")
    
    assert is_power_of_two(1) == True
    assert is_power_of_two(2) == True
    assert is_power_of_two(16) == True
    assert is_power_of_two(15) == False
    assert is_power_of_two(0) == False
    assert is_power_of_two(-1) == False
    print("✓ is_power_of_two 正常")
    
    assert next_power_of_two(1) == 1
    assert next_power_of_two(2) == 2
    assert next_power_of_two(15) == 16
    assert next_power_of_two(16) == 16
    assert next_power_of_two(17) == 32
    print("✓ next_power_of_two 正常")
    
    assert previous_power_of_two(1) == 1
    assert previous_power_of_two(16) == 16
    assert previous_power_of_two(17) == 16
    assert previous_power_of_two(31) == 16
    print("✓ previous_power_of_two 正常")
    
    print()


def test_gray_code():
    """测试格雷码"""
    print("=== 测试格雷码 ===")
    
    # 测试前几个格雷码
    expected = [0, 1, 3, 2, 6, 7, 5, 4]
    for i, exp in enumerate(expected):
        assert gray_code(i) == exp
        assert gray_to_binary(exp) == i
    print("✓ 格雷码转换正常")
    
    # 验证相邻格雷码只有一位不同
    for i in range(1, 100):
        g1 = gray_code(i - 1)
        g2 = gray_code(i)
        diff = count_bits(g1 ^ g2)
        assert diff == 1
    print("✓ 相邻格雷码只有一位不同")
    
    print()


def test_sign_extend():
    """测试符号扩展"""
    print("=== 测试符号扩展 ===")
    
    # 正数（符号位为0）
    assert sign_extend(0b010, 3, 8) == 0b010
    
    # 负数（符号位为1）
    assert sign_extend(0b101, 3, 8) == 0b11111101
    print("✓ 符号扩展正常")
    
    print()


def test_swap_bits():
    """测试位交换"""
    print("=== 测试位交换 ===")
    
    # 0b10100001: 位0=1, 位5=1 (相同)，交换后不变
    assert swap_bits(0b10100001, 0, 5) == 0b10100001
    # 0b101: 位0=1, 位2=1 (相同)，交换后不变
    assert swap_bits(0b101, 0, 2) == 0b101
    # 相同位置不改变
    assert swap_bits(0b101, 0, 0) == 0b101
    # 0b1000: 位0=0, 位3=1 (不同)，交换后 -> 0b0001
    assert swap_bits(0b1000, 0, 3) == 0b0001
    print("✓ 位交换正常")
    
    print()


def test_align():
    """测试对齐函数"""
    print("=== 测试对齐 ===")
    
    assert align_up(100, 16) == 112
    assert align_up(16, 16) == 16
    assert align_up(0, 16) == 0
    print("✓ align_up 正常")
    
    assert align_down(100, 16) == 96
    assert align_down(16, 16) == 16
    assert align_down(0, 16) == 0
    print("✓ align_down 正常")
    
    print()


def test_format():
    """测试格式化函数"""
    print("=== 测试格式化 ===")
    
    # 二进制字符串
    assert to_binary_string(0xABCD, width=16, group_size=4) == '1010 1011 1100 1101'
    assert to_binary_string(5, width=8) == '00000101'
    print("✓ to_binary_string 正常")
    
    # 从二进制字符串解析
    assert from_binary_string('1010 1011 1100 1101') == 0xABCD
    assert from_binary_string('0b1011') == 0b1011
    assert from_binary_string('1010_1011') == 0b10101011
    print("✓ from_binary_string 正常")
    
    # 十六进制字符串
    assert to_hex_string(255, width=4, uppercase=True) == '0x00FF'
    assert to_hex_string(255, prefix=False) == 'ff'
    print("✓ to_hex_string 正常")
    
    print()


def test_bitset():
    """测试位集合操作"""
    print("=== 测试位集合 ===")
    
    # 创建
    assert create_bitset([0, 2, 4]) == 0b10101
    print("✓ create_bitset 正常")
    
    # 并集
    assert bitset_union(0b101, 0b011) == 0b111
    assert bitset_union() == 0
    print("✓ bitset_union 正常")
    
    # 交集
    assert bitset_intersection(0b101, 0b011) == 0b001
    assert bitset_intersection() == 0
    print("✓ bitset_intersection 正常")
    
    # 差集
    assert bitset_difference(0b111, 0b011) == 0b100
    print("✓ bitset_difference 正常")
    
    # 对称差
    assert bitset_symmetric_difference(0b101, 0b011) == 0b110
    print("✓ bitset_symmetric_difference 正常")
    
    # 子集/超集
    assert bitset_is_subset(0b101, 0b111) == True
    assert bitset_is_subset(0b101, 0b110) == False
    assert bitset_is_superset(0b111, 0b101) == True
    print("✓ 子集/超集检查正常")
    
    # 转列表
    assert bitset_to_list(0b10101) == [0, 2, 4]
    print("✓ bitset_to_list 正常")
    
    print()


def test_iterate_bits():
    """测试位迭代"""
    print("=== 测试位迭代 ===")
    
    result = list(iterate_bits(0b101, 4))
    assert result == [(0, 1), (1, 0), (2, 1), (3, 0)]
    print("✓ iterate_bits 正常")
    
    print()


def test_edge_cases():
    """测试边界情况"""
    print("=== 测试边界情况 ===")
    
    # 空值
    assert count_bits(0) == 0
    assert find_first_set_bit(0) == -1
    assert bitset_to_list(0) == []
    print("✓ 空值处理正常")
    
    # 大数
    big = (1 << 100)
    assert count_bits(big) == 1
    assert find_first_set_bit(big) == 100
    assert find_last_set_bit(big) == 100
    print("✓ 大数处理正常")
    
    # 位向量边界
    bv = BitVector(0)
    assert len(bv) == 0
    assert bv.to_int() == 0
    print("✓ 零长度位向量正常")
    
    print()


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*50)
    print("位操作工具集测试报告")
    print("="*50 + "\n")
    
    test_bit_vector()
    test_bit_field()
    test_bit_mask()
    test_count_bits()
    test_find_bits()
    test_reverse_bits()
    test_rotate_bits()
    test_power_of_two()
    test_gray_code()
    test_sign_extend()
    test_swap_bits()
    test_align()
    test_format()
    test_bitset()
    test_iterate_bits()
    test_edge_cases()
    
    print("="*50)
    print("✅ 所有测试通过！")
    print("="*50)


if __name__ == '__main__':
    run_all_tests()