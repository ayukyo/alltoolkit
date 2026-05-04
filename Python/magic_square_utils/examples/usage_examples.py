"""
Magic Square Utils - 使用示例

演示魔方阵工具集的各种功能，包括：
- 基本魔方阵生成
- 魔方阵验证
- 魔方阵变换
- 特殊魔方阵
- 泛对角线魔方阵
- 实际应用场景

Author: AllToolkit
License: MIT
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from magic_square_utils.mod import (
    magic_constant,
    magic_constant_formula,
    is_magic_square,
    is_pandiagonal,
    get_square_properties,
    generate,
    generate_odd,
    generate_doubly_even,
    generate_singly_even,
    generate_pandiagonal,
    generate_lo_shu,
    generate_durer,
    generate_franklin,
    rotate_90,
    rotate_180,
    rotate_270,
    flip_horizontal,
    flip_vertical,
    flip_diagonal,
    get_all_variations,
    are_equivalent,
    square_to_string,
    count_magic_squares,
    find_element,
    get_row_sum,
    get_col_sum,
    get_diagonal_sums,
)


def example_basic_generation():
    """基本魔方阵生成示例"""
    print("\n" + "=" * 60)
    print("示例 1: 基本魔方阵生成")
    print("=" * 60)
    
    # 生成 3 阶魔方阵（洛书）
    print("\n生成 3 阶魔方阵（洛书）：")
    square_3 = generate(3)
    print(square_to_string(square_3))
    print(f"魔方常数: {magic_constant(3)}")
    
    # 生成 4 阶魔方阵
    print("\n生成 4 阶魔方阵：")
    square_4 = generate(4)
    print(square_to_string(square_4))
    print(f"魔方常数: {magic_constant(4)}")
    
    # 生成 5 阶魔方阵
    print("\n生成 5 阶魔方阵：")
    square_5 = generate(5)
    print(square_to_string(square_5))
    print(f"魔方常数: {magic_constant(5)}")
    
    # 生成 6 阶魔方阵
    print("\n生成 6 阶魔方阵（单偶数阶）：")
    square_6 = generate(6)
    print(square_to_string(square_6, padding=1))
    print(f"魔方常数: {magic_constant(6)}")


def example_magic_constant():
    """魔方常数计算示例"""
    print("\n" + "=" * 60)
    print("示例 2: 魔方常数计算")
    print("=" * 60)
    
    print("\n各阶魔方阵的魔方常数：")
    print("-" * 30)
    for n in range(3, 15):
        constant = magic_constant(n)
        formula = magic_constant_formula(n)
        print(f"{n:2d} 阶: {constant:6d}  ({formula})")


def example_validation():
    """魔方阵验证示例"""
    print("\n" + "=" * 60)
    print("示例 3: 魔方阵验证")
    print("=" * 60)
    
    # 有效的魔方阵
    print("\n验证洛书（有效魔方阵）：")
    lo_shu = [[8, 1, 6], [3, 5, 7], [4, 9, 2]]
    print(square_to_string(lo_shu))
    print(f"是否为有效魔方阵: {is_magic_square(lo_shu)}")
    
    props = get_square_properties(lo_shu)
    print(f"阶数: {props['order']}")
    print(f"魔方常数: {props['magic_constant']}")
    print(f"行和: {props['sum_rows']}")
    print(f"列和: {props['sum_cols']}")
    print(f"对角线和: {props['sum_diagonals']}")
    
    # 无效的魔方阵
    print("\n验证无效魔方阵：")
    invalid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(square_to_string(invalid))
    print(f"是否为有效魔方阵: {is_magic_square(invalid)}")
    
    props = get_square_properties(invalid)
    print(f"行和: {props['sum_rows']}")
    print(f"列和: {props['sum_cols']}")


def example_transformations():
    """魔方阵变换示例"""
    print("\n" + "=" * 60)
    print("示例 4: 魔方阵变换")
    print("=" * 60)
    
    lo_shu = [[8, 1, 6], [3, 5, 7], [4, 9, 2]]
    
    print("\n原始魔方阵：")
    print(square_to_string(lo_shu))
    
    print("\n旋转 90°：")
    print(square_to_string(rotate_90(lo_shu)))
    
    print("\n旋转 180°：")
    print(square_to_string(rotate_180(lo_shu)))
    
    print("\n旋转 270°：")
    print(square_to_string(rotate_270(lo_shu)))
    
    print("\n水平翻转：")
    print(square_to_string(flip_horizontal(lo_shu)))
    
    print("\n垂直翻转：")
    print(square_to_string(flip_vertical(lo_shu)))
    
    print("\n主对角线翻转（转置）：")
    print(square_to_string(flip_diagonal(lo_shu)))
    
    print("\n获取所有 8 种变换形式：")
    variations = get_all_variations(lo_shu)
    for i, v in enumerate(variations):
        print(f"\n变换 {i + 1}:")
        print(square_to_string(v))


def test_equivalence():
    """魔方阵等价性判断示例"""
    print("\n" + "=" * 60)
    print("示例 5: 等价性判断")
    print("=" * 60)
    
    lo_shu = [[8, 1, 6], [3, 5, 7], [4, 9, 2]]
    rotated = rotate_90(lo_shu)
    flipped = flip_horizontal(lo_shu)
    
    print("\n原始魔方阵：")
    print(square_to_string(lo_shu))
    
    print("\n旋转后的魔方阵：")
    print(square_to_string(rotated))
    print(f"是否与原始等价: {are_equivalent(lo_shu, rotated)}")
    
    print("\n翻转后的魔方阵：")
    print(square_to_string(flipped))
    print(f"是否与原始等价: {are_equivalent(lo_shu, flipped)}")
    
    # 生成另一个不同的魔方阵
    different = generate(5)
    print(f"\n不同阶数的魔方阵是否等价: {are_equivalent(lo_shu, different[:3])}")


def example_special_squares():
    """特殊魔方阵示例"""
    print("\n" + "=" * 60)
    print("示例 6: 特殊魔方阵")
    print("=" * 60)
    
    # 洛书
    print("\n洛书（中国古代传说中的 3 阶魔方阵）：")
    lo_shu = generate_lo_shu()
    print(square_to_string(lo_shu))
    print("特点：唯一的标准 3 阶魔方阵（不计变换）")
    print("中心数字 5 代表五行之中央")
    
    # 丢勒魔方阵
    print("\n丢勒魔方阵（1514 年）：")
    durer = generate_durer()
    print(square_to_string(durer))
    print("特点：")
    print(f"  - 泛对角线魔方阵: {is_pandiagonal(durer)}")
    print(f"  - 魔方常数: {magic_constant(4)}")
    print("  - 底行中间数字 15 和 14 代表创作年份 1514")
    corners = durer[0][0] + durer[0][3] + durer[3][0] + durer[3][3]
    print(f"  - 四角数字之和: {corners}")
    
    # 富兰克林魔方阵
    print("\n富兰克林魔方阵（8 阶）：")
    franklin = generate_franklin()
    print(square_to_string(franklin, padding=1))
    print("特点：")
    print("  - 行和列和都是 260")
    print("  - 不是标准魔方阵（对角线和不正确）")
    print("  - 由本杰明·富兰克林创造")


def example_pandiagonal():
    """泛对角线魔方阵示例"""
    print("\n" + "=" * 60)
    print("示例 7: 泛对角线魔方阵（完美魔方阵）")
    print("=" * 60)
    
    print("\n泛对角线魔方阵的所有折对角线之和也等于魔方常数")
    
    # 5 阶泛对角线魔方阵
    print("\n5 阶泛对角线魔方阵：")
    p5 = generate_pandiagonal(5)
    if p5:
        print(square_to_string(p5, padding=1))
        print(f"是否为泛对角线魔方阵: {is_pandiagonal(p5)}")
    
    # 7 阶泛对角线魔方阵
    print("\n7 阶泛对角线魔方阵：")
    p7 = generate_pandiagonal(7)
    if p7:
        print(square_to_string(p7, padding=1))
        print(f"是否为泛对角线魔方阵: {is_pandiagonal(p7)}")
    
    # 对比普通魔方阵
    print("\n普通 5 阶魔方阵：")
    normal_5 = generate(5)
    print(square_to_string(normal_5, padding=1))
    print(f"是否为泛对角线魔方阵: {is_pandiagonal(normal_5)}")


def example_find_element():
    """元素查找示例"""
    print("\n" + "=" * 60)
    print("示例 8: 元素查找")
    print("=" * 60)
    
    square = generate(5)
    print("\n5 阶魔方阵：")
    print(square_to_string(square, padding=1))
    
    print("\n查找特定数字的位置：")
    for num in [1, 13, 25]:
        pos = find_element(square, num)
        if pos:
            row, col = pos
            print(f"  数字 {num:2d} 位于第 {row + 1} 行第 {col + 1} 列")
    
    # 验证中心数字
    center_pos = find_element(square, 13)
    print(f"\n中心数字 13 位于: {center_pos}")
    
    # 行列和验证
    row_sum = get_row_sum(square, 2)
    col_sum = get_col_sum(square, 2)
    diag_sums = get_diagonal_sums(square)
    
    print(f"\n中心行（第 3 行）的和: {row_sum}")
    print(f"中心列（第 3 列）的和: {col_sum}")
    print(f"对角线和: 主对角线={diag_sums[0]}, 副对角线={diag_sums[1]}")


def example_statistics():
    """魔方阵统计示例"""
    print("\n" + "=" * 60)
    print("示例 9: 魔方阵统计")
    print("=" * 60)
    
    print("\n各阶魔方阵的数量：")
    print("-" * 35)
    print(f"{'阶数':<8}{'数量':<15}{'说明'}")
    print("-" * 35)
    
    counts = {1: 1, 2: 0, 3: 8, 4: 880, 5: 275305224}
    
    for n in range(1, 7):
        count = count_magic_squares(n)
        if count == -1:
            print(f"{n:<8}{'未知':<15}{'计算过于复杂'}")
        elif count == 0:
            print(f"{n:<8}{count:<15}{'不存在'}")
        elif count == 1:
            print(f"{n:<8}{count:<15}{'唯一'}")
        elif count == 8:
            print(f"{n:<8}{count:<15}{'洛书及其变换'}")
        else:
            print(f"{n:<8}{count:<15,}{'已知数量'}")


def example_comparison():
    """不同生成方法对比"""
    print("\n" + "=" * 60)
    print("示例 10: 不同生成方法对比")
    print("=" * 60)
    
    # 奇数阶
    print("\n奇数阶魔方阵（Siamese 方法）：")
    odd = generate_odd(5)
    print(square_to_string(odd, padding=1))
    
    # 双偶数阶
    print("\n双偶数阶魔方阵（Strachey 方法）：")
    doubly_even = generate_doubly_even(4)
    print(square_to_string(doubly_even))
    
    # 单偶数阶
    print("\n单偶数阶魔方阵（Conway 方法）：")
    singly_even = generate_singly_even(6)
    print(square_to_string(singly_even, padding=1))


def example_practical_applications():
    """实际应用示例"""
    print("\n" + "=" * 60)
    print("示例 11: 实际应用场景")
    print("=" * 60)
    
    # 1. 数字谜题
    print("\n应用 1: 数字谜题生成")
    print("-" * 30)
    puzzle = generate(4)
    print("4×4 魔方阵谜题：")
    print(square_to_string(puzzle))
    print("\n提示：每行、每列、每条对角线的和都相等")
    print(f"答案：魔方常数为 {magic_constant(4)}")
    
    # 2. 艺术图案
    print("\n应用 2: 艺术图案设计")
    print("-" * 30)
    square = generate(8)
    print("8×8 魔方阵可视化：")
    for row in square:
        line = ""
        for num in row:
            # 用不同符号表示不同范围
            if num <= 16:
                line += "░░"
            elif num <= 32:
                line += "▒▒"
            elif num <= 48:
                line += "▓▓"
            else:
                line += "██"
        print(line)
    
    # 3. 加密应用
    print("\n应用 3: 简单加密")
    print("-" * 30)
    message = "HELLO WORLD MAGIC"
    square = generate(5)
    
    # 根据魔方阵重新排列消息
    print(f"原始消息: {message}")
    print("使用 5 阶魔方阵重新排列...")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("Magic Square Utils 使用示例")
    print("=" * 60)
    
    example_basic_generation()
    example_magic_constant()
    example_validation()
    example_transformations()
    test_equivalence()
    example_special_squares()
    example_pandiagonal()
    example_find_element()
    example_statistics()
    example_comparison()
    example_practical_applications()
    
    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()