"""
位操作工具集使用示例
===================

展示位操作工具集的主要功能和典型用法。

作者: AllToolkit
日期: 2026-04-16
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    BitVector, BitField, BitMask,
    count_bits, find_first_set_bit, find_last_set_bit,
    reverse_bits, rotate_left, rotate_right,
    is_power_of_two, next_power_of_two,
    gray_code, gray_to_binary,
    to_binary_string, to_hex_string,
    bitset_union, bitset_intersection, bitset_to_list,
    align_up, align_down
)


def example_bit_vector():
    """BitVector 示例：位数组操作"""
    print("=" * 60)
    print("示例 1: BitVector - 位数组操作")
    print("=" * 60)
    
    # 创建一个8位的位向量
    bv = BitVector(8, 0b10110101)
    print(f"初始值: {bv.to_binary_string()} (十进制: {bv.to_int()})")
    
    # 位操作
    bv.clear(0)  # 清除第0位
    print(f"清除第0位: {bv.to_binary_string()}")
    
    bv.set(1)    # 设置第1位
    print(f"设置第1位: {bv.to_binary_string()}")
    
    bv.flip(2)   # 翻转第2位
    print(f"翻转第2位: {bv.to_binary_string()}")
    
    # 统计
    print(f"1的个数: {bv.count_set_bits()}")
    print(f"0的个数: {bv.count_clear_bits()}")
    
    # 位运算
    bv1 = BitVector(4, 0b1010)
    bv2 = BitVector(4, 0b1100)
    print(f"\n位运算示例:")
    print(f"  {bv1.to_binary_string()} AND {bv2.to_binary_string()} = {(bv1 & bv2).to_binary_string()}")
    print(f"  {bv1.to_binary_string()} OR  {bv2.to_binary_string()} = {(bv1 | bv2).to_binary_string()}")
    print(f"  {bv1.to_binary_string()} XOR {bv2.to_binary_string()} = {(bv1 ^ bv2).to_binary_string()}")
    print(f"  NOT {bv1.to_binary_string()} = {(~bv1).to_binary_string()}")
    
    print()


def example_bit_field():
    """BitField 示例：位字段操作"""
    print("=" * 60)
    print("示例 2: BitField - 位字段操作")
    print("=" * 60)
    
    # 模拟一个32位的网络数据包头部
    # [31:16] 源端口 (16位)
    # [15:0]  目标端口 (16位)
    
    header = 0
    source_port = 8080
    dest_port = 80
    
    # 设置源端口 (位16-31)
    header = BitField.insert(header, 16, 32, source_port)
    # 设置目标端口 (位0-15)
    header = BitField.insert(header, 0, 16, dest_port)
    
    print(f"数据包头部: {to_hex_string(header, width=8)}")
    print(f"源端口: {BitField.extract(header, 16, 32)}")
    print(f"目标端口: {BitField.extract(header, 0, 16)}")
    
    # 模拟CPU标志寄存器
    flags = 0
    flags = BitField.set_bit(flags, 0)   # 进位标志
    flags = BitField.set_bit(flags, 6)   # 零标志
    flags = BitField.set_bit(flags, 7)   # 符号标志
    
    print(f"\nCPU标志寄存器: {to_binary_string(flags, width=8, group_size=4)}")
    print(f"进位标志 (位0): {BitField.get_bit(flags, 0)}")
    print(f"零标志 (位6): {BitField.get_bit(flags, 6)}")
    print(f"符号标志 (位7): {BitField.get_bit(flags, 7)}")
    
    print()


def example_bit_mask():
    """BitMask 示例：位掩码操作"""
    print("=" * 60)
    print("示例 3: BitMask - 位掩码操作")
    print("=" * 60)
    
    # 创建权限掩码
    # 位0: 读取
    # 位1: 写入
    # 位2: 执行
    # 位3: 删除
    # 位4: 管理
    
    read_mask = BitMask.create_mask([0])
    write_mask = BitMask.create_mask([1])
    execute_mask = BitMask.create_mask([2])
    delete_mask = BitMask.create_mask([3])
    admin_mask = BitMask.create_mask([4])
    
    # 创建权限组合
    editor_permissions = BitMask.combine_masks(read_mask, write_mask)
    admin_permissions = BitMask.combine_masks(read_mask, write_mask, delete_mask, admin_mask)
    
    print("权限掩码:")
    print(f"  读取:   {to_binary_string(read_mask, width=5)}")
    print(f"  写入:   {to_binary_string(write_mask, width=5)}")
    print(f"  执行:   {to_binary_string(execute_mask, width=5)}")
    print(f"  删除:   {to_binary_string(delete_mask, width=5)}")
    print(f"  管理:   {to_binary_string(admin_mask, width=5)}")
    
    print(f"\n编辑者权限: {to_binary_string(editor_permissions, width=5)}")
    print(f"管理员权限: {to_binary_string(admin_permissions, width=5)}")
    
    # 检查权限
    user_permissions = admin_permissions
    print(f"\n用户权限检查:")
    print(f"  可读取: {bool(user_permissions & read_mask)}")
    print(f"  可写入: {bool(user_permissions & write_mask)}")
    print(f"  可执行: {bool(user_permissions & execute_mask)}")
    print(f"  可删除: {bool(user_permissions & delete_mask)}")
    print(f"  可管理: {bool(user_permissions & admin_mask)}")
    
    print()


def example_bit_counting():
    """位计数示例"""
    print("=" * 60)
    print("示例 4: 位计数")
    print("=" * 60)
    
    numbers = [0, 1, 7, 15, 255, 256, 0xFFFFFFFF]
    
    print("数值的二进制分析:")
    for n in numbers:
        bits = count_bits(n)
        width = max(1, n.bit_length())
        print(f"  {n:12} = {to_binary_string(n, width=min(width, 16), group_size=4):>20}  (1的个数: {bits})")
    
    # 找第一个/最后一个设置的位
    print("\n位查找示例:")
    value = 0b10100000
    print(f"  {to_binary_string(value, width=8)}:")
    print(f"    第一个1的位置: {find_first_set_bit(value)}")
    print(f"    最后一个1的位置: {find_last_set_bit(value)}")
    
    print()


def example_power_of_two():
    """2的幂操作示例"""
    print("=" * 60)
    print("示例 5: 2的幂操作")
    print("=" * 60)
    
    # 检查是否是2的幂
    test_values = [1, 2, 3, 4, 5, 8, 16, 31, 32, 64, 100]
    
    print("检查2的幂:")
    for n in test_values:
        is_pow = is_power_of_two(n)
        next_pow = next_power_of_two(n)
        prev_pow = previous_power_of_two(n)
        print(f"  {n:3}: 2的幂? {'是' if is_pow else '否':<3} | 上一个: {prev_pow:3} | 下一个: {next_pow:3}")
    
    # 内存分配对齐示例
    print("\n内存对齐示例:")
    allocations = [100, 255, 1000, 4095, 4096]
    for size in allocations:
        aligned = align_up(size, 4096)  # 4KB页对齐
        print(f"  {size:5} 字节 -> {aligned:5} 字节 (4KB对齐)")
    
    print()


def example_gray_code():
    """格雷码示例"""
    print("=" * 60)
    print("示例 6: 格雷码")
    print("=" * 60)
    
    print("二进制 vs 格雷码 (0-15):")
    print("-" * 40)
    print(f"{'十进制':<8} {'二进制':<10} {'格雷码':<10}")
    print("-" * 40)
    
    for i in range(16):
        gray = gray_code(i)
        print(f"{i:<8} {to_binary_string(i, width=4):<10} {to_binary_string(gray, width=4):<10}")
    
    # 验证格雷码特性：相邻值只有一位不同
    print("\n验证格雷码特性 (相邻值只有一位不同):")
    for i in range(1, 16):
        diff = count_bits(gray_code(i-1) ^ gray_code(i))
        assert diff == 1, f"格雷码验证失败: {i-1} 和 {i}"
    print("✓ 所有相邻格雷码值只有一位不同")
    
    print()


def example_rotate_bits():
    """位旋转示例"""
    print("=" * 60)
    print("示例 7: 位旋转")
    print("=" * 60)
    
    value = 0b10110001
    width = 8
    
    print(f"原始值: {to_binary_string(value, width=width)}")
    print()
    
    # 循环左移
    print("循环左移:")
    for shift in range(1, 5):
        rotated = rotate_left(value, shift, width)
        print(f"  左移{shift}位: {to_binary_string(rotated, width=width)}")
    
    print()
    
    # 循环右移
    print("循环右移:")
    for shift in range(1, 5):
        rotated = rotate_right(value, shift, width)
        print(f"  右移{shift}位: {to_binary_string(rotated, width=width)}")
    
    print()


def example_bitset_operations():
    """位集合操作示例"""
    print("=" * 60)
    print("示例 8: 位集合操作")
    print("=" * 60)
    
    # 使用位集合表示集合
    set_a = 0b101011  # {0, 1, 3, 5}
    set_b = 0b011101  # {0, 2, 3, 4}
    
    print(f"集合A: {bitset_to_list(set_a)} -> {to_binary_string(set_a, width=6)}")
    print(f"集合B: {bitset_to_list(set_b)} -> {to_binary_string(set_b, width=6)}")
    
    # 集合操作
    union = bitset_union(set_a, set_b)
    intersection = bitset_intersection(set_a, set_b)
    
    print(f"\n并集 (A|B):  {bitset_to_list(union)} -> {to_binary_string(union, width=6)}")
    print(f"交集 (A&B): {bitset_to_list(intersection)} -> {to_binary_string(intersection, width=6)}")
    
    print()


def example_bit_manipulation_tricks():
    """位操作技巧示例"""
    print("=" * 60)
    print("示例 9: 实用位操作技巧")
    print("=" * 60)
    
    # 1. 快速乘除2
    print("1. 快速乘除2:")
    n = 5
    print(f"   {n} << 1 = {n << 1} (乘以2)")
    print(f"   {n} >> 1 = {n >> 1} (除以2)")
    
    # 2. 交换两个数（不用临时变量）
    print("\n2. 交换两个数:")
    a, b = 5, 7
    print(f"   原始: a={a}, b={b}")
    a ^= b
    b ^= a
    a ^= b
    print(f"   交换后: a={a}, b={b}")
    
    # 3. 检查奇偶性
    print("\n3. 检查奇偶性:")
    for n in [1, 2, 3, 4, 5]:
        is_even = (n & 1) == 0
        print(f"   {n} 是 {'偶数' if is_even else '奇数'}")
    
    # 4. 取绝对值（不使用条件）
    print("\n4. 计算整数绝对值:")
    for n in [-5, 0, 5]:
        # 注意：这个技巧只适用于固定位宽
        mask = n >> 31  # 负数全1，正数全0
        abs_n = (n ^ mask) - mask
        print(f"   |{n}| = {abs_n}")
    
    # 5. 判断两数异号
    print("\n5. 判断两数异号:")
    pairs = [(1, -1), (-1, -2), (3, 4), (0, -1)]
    for x, y in pairs:
        opposite_signs = (x ^ y) < 0
        print(f"   {x} 和 {y}: {'异号' if opposite_signs else '同号'}")
    
    print()


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("位操作工具集使用示例")
    print("=" * 60 + "\n")
    
    example_bit_vector()
    example_bit_field()
    example_bit_mask()
    example_bit_counting()
    example_power_of_two()
    example_gray_code()
    example_rotate_bits()
    example_bitset_operations()
    example_bit_manipulation_tricks()
    
    print("=" * 60)
    print("所有示例演示完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()