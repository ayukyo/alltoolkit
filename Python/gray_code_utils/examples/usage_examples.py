#!/usr/bin/env python3
"""
usage_examples.py - Gray码工具集使用示例

示例内容：
1. 基础转换示例
2. Gray码序列生成示例
3. Johnson计数器示例
4. 位置编码器应用
5. 汉诺塔解法示例
6. 多维Gray码遍历示例
7. Karnaugh图应用
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    binary_to_gray, gray_to_binary,
    binary_to_gray_bits, gray_bits_to_binary,
    generate_gray_codes, generate_gray_codes_binary,
    generate_johnson_codes, generate_johnson_codes_binary,
    gray_distance, are_adjacent_gray, find_changed_bit,
    generate_n_dimensional_gray,
    gray_code_position_encoder, decode_gray_position,
    hanoi_moves_gray, gray_code_kmap_index,
    count_transitions, get_transition_sequence,
    complete_gray_cycle, sort_by_gray
)


def example_basic_conversion():
    """示例1: 基础转换"""
    print("\n" + "=" * 50)
    print("示例1: 基础转换")
    print("=" * 50)
    
    print("\n--- 十进制 <-> Gray码 ---")
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 10, 15, 20, 31]
    print(f"原始数值: {numbers}")
    
    gray_values = [binary_to_gray(n) for n in numbers]
    print(f"Gray码值: {gray_values}")
    
    recovered = [gray_to_binary(g) for g in gray_values]
    print(f"还原数值: {recovered}")
    
    # 显示二进制表示
    print("\n--- 详细转换表（5位）---")
    print("十进制 | 二进制 | Gray码 | Gray二进制")
    print("-" * 40)
    for n in range(16):
        binary = format(n, '05b')
        gray = binary_to_gray(n)
        gray_binary = format(gray, '05b')
        recovered = gray_to_binary(gray)
        print(f"  {n:2d}   | {binary} |  {gray:2d}   | {gray_binary}  -> 还原: {recovered}")
    
    print("\n--- 位列表转换 ---")
    binary_bits = [1, 0, 1, 1, 0]
    gray_bits = binary_to_gray_bits(binary_bits)
    recovered_bits = gray_bits_to_binary(gray_bits)
    print(f"二进制位: {binary_bits}")
    print(f"Gray码位: {gray_bits}")
    print(f"还原位:   {recovered_bits}")


def example_gray_code_sequence():
    """示例2: Gray码序列生成"""
    print("\n" + "=" * 50)
    print("示例2: Gray码序列生成")
    print("=" * 50)
    
    print("\n--- 4位Gray码完整序列 ---")
    codes = generate_gray_codes(4)
    binaries = generate_gray_codes_binary(4)
    
    print("序号 | 十进制 | 二进制")
    print("-" * 25)
    for i, (code, binary) in enumerate(zip(codes, binaries)):
        print(f" {i:2d}  |   {code:2d}   |  {binary}")
    
    print("\n--- 跳变分析 ---")
    transitions = get_transition_sequence(codes)
    print(f"跳变位序列: {transitions}")
    print(f"总跳变次数: {count_transitions(codes)}")
    
    print("\n--- 相邻性验证 ---")
    for i in range(len(codes) - 1):
        adj = are_adjacent_gray(codes[i], codes[i+1])
        dist = gray_distance(codes[i], codes[i+1])
        bit = find_changed_bit(codes[i], codes[i+1])
        print(f"{binaries[i]} -> {binaries[i+1]}: 相邻={adj}, 距离={dist}, 改变位={bit}")
    
    print("\n--- 循环验证 ---")
    first_last_adj = are_adjacent_gray(codes[-1], codes[0])
    print(f"首尾相邻: {codes[-1]} ({binaries[-1]}) <-> {codes[0]} ({binaries[0]}) = {first_last_adj}")
    
    print("\n--- 从指定值开始的循环 ---")
    cycle = complete_gray_cycle(4, start=8)
    print(f"从8开始的循环: {cycle}")
    print(f"二进制: {[format(c, '04b') for c in cycle]}")


def example_johnson_counter():
    """示例3: Johnson计数器"""
    print("\n" + "=" * 50)
    print("示例3: Johnson计数器")
    print("=" * 50)
    
    print("\nJohnson计数器是一种特殊的Gray码计数器，")
    print("常用于硬件设计中的状态机实现。")
    
    print("\n--- 4位Johnson码 ---")
    codes = generate_johnson_codes(4)
    binaries = generate_johnson_codes_binary(4)
    
    print("步骤 | 状态 | 二进制 | 说明")
    print("-" * 40)
    for i, (code, binary) in enumerate(zip(codes, binaries)):
        ones = binary.count('1')
        desc = f"{ones}个位置1" if ones > 0 else "全零"
        print(f" {i:2d}  | {code:2d}   | {binary} | {desc}")
    
    print("\n--- Johnson码特点 ---")
    print("• 每次只改变一位")
    print("• 1从左向右填充，然后从左向右清除")
    print("• 形成2n个状态的循环")
    print(f"• 4位Johnson码有{len(codes)}个状态")


def example_position_encoder():
    """示例4: 位置编码器应用"""
    print("\n" + "=" * 50)
    print("示例4: 位置编码器应用")
    print("=" * 50)
    
    print("\nGray码位置编码器用于绝对位置测量，")
    print("避免读取时的毛刺问题。")
    
    print("\n--- 旋转编码器模拟（8位，256位置）---")
    positions = [0, 32, 64, 96, 128, 160, 192, 224, 255]
    
    print("位置 | Gray码 | 二进制 | 说明")
    print("-" * 45)
    for pos in positions:
        gray = gray_code_position_encoder(pos, 8)
        decoded = decode_gray_position(gray)
        # 检查与前一个位置的跳变
        bits_changed = gray_distance(binary_to_gray(pos), binary_to_gray(pos-32)) if pos > 0 else 0
        note = "起点" if pos == 0 else f"跳变{bits_changed}位" if bits_changed == 1 else "多步跳变"
        print(f" {pos:3d} | {gray} | 解码:{decoded:3d} | {note}")
    
    print("\n--- Gray码编码器优势 ---")
    print("• 避免读取瞬间的多位变化导致的错误")
    print("• 相邻位置只有一位不同")
    print("• 适合高速旋转场景")
    print("• 可检测方向（知道哪位变化了）")
    
    print("\n--- 方向检测示例 ---")
    pos1, pos2 = 63, 64
    gray1 = binary_to_gray(pos1)
    gray2 = binary_to_gray(pos2)
    bit_changed = find_changed_bit(gray1, gray2)
    print(f"位置 {pos1} -> {pos2}")
    print(f"Gray码 {gray1} ({format(gray1, '08b')}) -> {gray2} ({format(gray2, '08b')})")
    print(f"改变位: 第{bit_changed}位")


def example_hanoi():
    """示例5: 汉诺塔解法"""
    print("\n" + "=" * 50)
    print("示例5: 汉诺塔解法")
    print("=" * 50)
    
    print("\n使用Gray码生成汉诺塔最优解法")
    print("柱编号: 0(源), 1(辅助), 2(目标)")
    
    print("\n--- 3盘汉诺塔 ---")
    moves = hanoi_moves_gray(3)
    
    print("步骤 | 移动 | 说明")
    print("-" * 30)
    for i, (src, dst) in enumerate(moves):
        src_name = ['A', 'B', 'C'][src]
        dst_name = ['A', 'B', 'C'][dst]
        print(f" {i+1:2d}  | {src_name} -> {dst_name} | 从柱{src}移到柱{dst}")
    
    print(f"\n总步数: {len(moves)} (理论最优: 2^3-1 = 7)")
    
    print("\n--- 4盘汉诺塔 ---")
    moves_4 = hanoi_moves_gray(4)
    print(f"总步数: {len(moves_4)} (理论最优: 2^4-1 = 15)")
    
    # 只显示前5步和后5步
    print("前5步:")
    for i, (src, dst) in enumerate(moves_4[:5]):
        print(f"  {i+1}. 柱{src} -> 柱{dst}")
    print("...")
    print("后5步:")
    for i, (src, dst) in enumerate(moves_4[-5:]):
        print(f"  {len(moves_4)-4+i}. 柱{src} -> 柱{dst}")


def example_n_dimensional():
    """示例6: 多维Gray码遍历"""
    print("\n" + "=" * 50)
    print("示例6: 多维Gray码遍历")
    print("=" * 50)
    
    print("\n多维Gray码用于空间遍历，")
    print("保证相邻点只在一个维度变化一位。")
    
    print("\n--- 2x2网格遍历 ---")
    coords_2x2 = generate_n_dimensional_gray(2, 1)
    print(f"坐标序列: {coords_2x2}")
    print("\n可视化:")
    grid = [['  ' for _ in range(2)] for _ in range(2)]
    for i, (x, y) in enumerate(coords_2x2):
        grid[y][x] = f'{i}'
    for row in reversed(grid):
        print(' '.join(row))
    
    print("\n--- 4x4网格遍历 ---")
    coords_4x4 = generate_n_dimensional_gray(2, 2)
    print(f"坐标序列: {coords_4x4}")
    print("\n可视化（按顺序标记）：")
    grid = [['  ' for _ in range(4)] for _ in range(4)]
    for i, (x, y) in enumerate(coords_4x4):
        grid[y][x] = f'{i:2d}'
    for row in reversed(grid):
        print(' ' + ' '.join(row))
    
    print("\n--- 3维空间遍历 ---")
    coords_3d = generate_n_dimensional_gray(3, 1)
    print(f"8个顶点遍历顺序: {coords_3d}")
    print("(x, y, z) 坐标")
    for coord in coords_3d:
        print(f"  {coord}")


def example_karnaugh_map():
    """示例7: Karnaugh图应用"""
    print("\n" + "=" * 50)
    print("示例7: Karnaugh图应用")
    print("=" * 50)
    
    print("\nKarnaugh图(K-map)用于逻辑电路简化，")
    print("使用Gray码排列以最大化相邻方格的优化。")
    
    print("\n--- 2变量K-map索引 ---")
    idx_2var = gray_code_kmap_index(2)
    print(f"索引: {idx_2var}")
    print("二进制: " + ', '.join([format(i, '02b') for i in idx_2var]))
    
    print("\nK-map布局:")
    print("       B=0  B=1")
    print("A=0 |  00 | 01")
    print("A=1 |  10 | 11")
    
    print("\n--- 4变量K-map索引 ---")
    idx_4var = gray_code_kmap_index(4)
    print(f"行索引(2位): {[idx_4var[i] for i in range(4)]}")
    print(f"列索引(2位): {[idx_4var[i+4] for i in range(4)]}")
    
    print("\n完整K-map布局:")
    rows = gray_code_kmap_index(2)
    cols = gray_code_kmap_index(2)
    print("       " + " | ".join([format(c, '02b') for c in cols]))
    print("-" * 20)
    for r in rows:
        row_str = format(r, '02b') + " | "
        row_str += " | ".join([f'{r:02b}{c:02b}' for c in cols])
        print(row_str)
    
    print("\n--- Gray码在K-map中的优势 ---")
    print("• 相邻方格只有一位不同")
    print("• 可以合并相邻的1形成简化表达式")
    print("• 边界相邻（循环性）也能合并")


def example_sorting():
    """示例8: Gray码排序"""
    print("\n" + "=" * 50)
    print("示例8: Gray码排序")
    print("=" * 50)
    
    print("\n按Gray码值排序可用于特定应用场景。")
    
    print("\n--- 数值排序 ---")
    values = [0, 7, 3, 1, 5, 2, 6, 4]
    print(f"原始序列: {values}")
    sorted_values = sort_by_gray(values)
    print(f"Gray排序: {sorted_values}")
    
    print("\n详细对比:")
    print("十进制 | Gray码 | Gray二进制")
    print("-" * 30)
    for v in values:
        gray = binary_to_gray(v)
        print(f"  {v}    |   {gray}   |   {format(gray, '03b')}")
    
    print("\n--- 应用场景 ---")
    print("• 信号处理中的频率排序")
    print("• 硬件设计中的地址优化")
    print("• 最小化跳变的序列优化")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("Gray码工具集使用示例")
    print("=" * 60)
    
    example_basic_conversion()
    example_gray_code_sequence()
    example_johnson_counter()
    example_position_encoder()
    example_hanoi()
    example_n_dimensional()
    example_karnaugh_map()
    example_sorting()
    
    print("\n" + "=" * 60)
    print("示例演示完成")
    print("=" * 60)


if __name__ == '__main__':
    main()