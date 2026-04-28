#!/usr/bin/env python3
"""
Morton Code Utils 使用示例

本文件展示 Morton编码工具的主要功能和典型应用场景：
1. 基础2D/3D编码解码
2. Morton排序（空间局部性优化）
3. 邻居查询
4. 范围编码
5. 层级结构操作
6. 网格坐标转换
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    encode_2d, decode_2d,
    encode_3d, decode_3d,
    MortonEncoder2D, MortonEncoder3D,
    sort_positions_2d,
    get_neighbors_2d, get_neighbors_morton_2d,
    get_children_2d, get_parent_2d, is_ancestor_2d,
    range_to_morton_codes_2d,
    morton_code_to_grid_position,
    generate_morton_sequence_2d,
    morton_code_to_binary_string,
)


def example_basic_2d():
    """基础2D编码示例"""
    print("\n" + "=" * 50)
    print("示例1: 基础2D Morton编码")
    print("=" * 50)
    
    # 编码坐标
    print("\n编码2D坐标:")
    coordinates = [(0, 0), (1, 0), (0, 1), (1, 1), (3, 5), (100, 200)]
    for x, y in coordinates:
        code = encode_2d(x, y)
        print(f"  encode_2d({x}, {y}) = {code}")
    
    # 解码Morton码
    print("\n解码Morton码:")
    codes = [0, 1, 2, 3, 43, 6800]
    for code in codes:
        x, y = decode_2d(code)
        print(f"  decode_2d({code}) = ({x}, {y})")
    
    # 编码解码互逆性
    print("\n编码解码互逆验证:")
    for x in range(10):
        for y in range(10):
            code = encode_2d(x, y)
            dx, dy = decode_2d(code)
            assert (dx, dy) == (x, y)
    print("  ✓ 100个坐标互逆验证通过")


def example_basic_3d():
    """基础3D编码示例"""
    print("\n" + "=" * 50)
    print("示例2: 基础3D Morton编码")
    print("=" * 50)
    
    # 编码3D坐标
    print("\n编码3D坐标:")
    coordinates = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)]
    for x, y, z in coordinates:
        code = encode_3d(x, y, z)
        print(f"  encode_3d({x}, {y}, {z}) = {code}")
    
    # 解码Morton码
    print("\n解码3D Morton码:")
    codes = [0, 1, 2, 3, 4, 7]
    for code in codes:
        x, y, z = decode_3d(code)
        print(f"  decode_3d({code}) = ({x}, {y}, {z})")
    
    # 8个立方体角的编码
    print("\n2x2x2立方体的8个角:")
    for x in range(2):
        for y in range(2):
            for z in range(2):
                code = encode_3d(x, y, z)
                print(f"  ({x}, {y}, {z}) -> {code}")


def example_morton_sorting():
    """Morton排序示例"""
    print("\n" + "=" * 50)
    print("示例3: Morton排序（空间局部性优化）")
    print("=" * 50)
    
    # 随机坐标
    positions = [(10, 5), (3, 8), (7, 2), (1, 1), (5, 9), (0, 0)]
    
    print("\n原始坐标列表:")
    for pos in positions:
        print(f"  {pos}, Morton码={encode_2d(pos[0], pos[1])}")
    
    # Morton排序
    sorted_pos = sort_positions_2d(positions)
    
    print("\nMorton排序后的坐标:")
    for pos in sorted_pos:
        print(f"  {pos}, Morton码={encode_2d(pos[0], pos[1])}")
    
    print("\nMorton排序的优势:")
    print("  - 保持空间局部性：相邻的点在排序后通常仍然相邻")
    print("  - 提高缓存命中率：处理大规模空间数据时更高效")
    print("  - 优化范围查询：可以快速定位连续的区域")


def example_neighbors():
    """邻居查询示例"""
    print("\n" + "=" * 50)
    print("示例4: 邻居查询")
    print("=" * 50)
    
    # 坐标邻居
    x, y = 5, 5
    print(f"\n坐标 ({x}, {y}) 的邻居:")
    
    neighbors_4 = get_neighbors_2d(x, y, include_diagonal=False)
    print(f"\n  4邻域（上下左右）: {neighbors_4}")
    
    neighbors_8 = get_neighbors_2d(x, y, include_diagonal=True)
    print(f"\n  8邻域（含对角）: {neighbors_8}")
    
    # Morton码邻居
    code = encode_2d(x, y)
    neighbors_morton = get_neighbors_morton_2d(code)
    print(f"\n  Morton码 {code} 的邻居Morton码: {neighbors_morton}")
    
    # 应用场景
    print("\n应用场景:")
    print("  - 地理空间查询：查找附近的点/区域")
    print("  - 图像处理：像素邻域操作")
    print("  - 游戏开发：格子地图的邻居检测")


def example_hierarchy():
    """层级结构示例"""
    print("\n" + "=" * 50)
    print("示例5: 层级结构操作")
    print("=" * 50)
    
    # 父子关系
    code = 7  # 代表坐标(1,1)
    print(f"\nMorton码 {code} (坐标 {decode_2d(code)}) 的层级关系:")
    
    parent = get_parent_2d(code)
    print(f"  父级: {parent} (坐标 {decode_2d(parent)})")
    
    children = get_children_2d(code)
    print(f"  子级: {children}")
    for child in children:
        print(f"    {child} -> 坐标 {decode_2d(child)}")
    
    # 祖先检查
    print("\n祖先关系检查:")
    print(f"  is_ancestor_2d(0, {code}) = {is_ancestor_2d(0, code)}")
    print(f"  is_ancestor_2d(1, {code}) = {is_ancestor_2d(1, code)}")
    print(f"  is_ancestor_2d(2, {code}) = {is_ancestor_2d(2, code)}")
    
    # 多层级展示
    print("\n层级树展示（深度3）:")
    for level in range(4):
        codes_at_level = [i << (2 * level) for i in range(4)]
        print(f"  深度{level}: Morton码 {codes_at_level}")


def example_range_encoding():
    """范围编码示例"""
    print("\n" + "=" * 50)
    print("示例6: 范围编码")
    print("=" * 50)
    
    # 矩形范围
    print("\n矩形范围 (0,0) 到 (3,3):")
    codes = range_to_morton_codes_2d(0, 0, 3, 3, max_depth=4)
    print(f"  Morton码数量: {len(codes)}")
    print(f"  Morton码列表: {sorted(codes)}")
    
    # 验证覆盖
    print("\n覆盖验证:")
    for code in sorted(codes)[:8]:
        x, y = decode_2d(code)
        print(f"  {code} -> ({x}, {y})")
    
    # 应用场景
    print("\n应用场景:")
    print("  - 地理范围查询：给定矩形区域查找所有点")
    print("  - 图像区域处理：批量处理特定区域")
    print("  - 数据库索引：范围查询优化")


def example_encoder_class():
    """编码器类示例"""
    print("\n" + "=" * 50)
    print("示例7: MortonEncoder2D 类使用")
    print("=" * 50)
    
    # 创建编码器
    encoder = MortonEncoder2D(depth=10)
    print(f"\n编码器信息: {encoder}")
    print(f"  深度: {encoder.depth}")
    print(f"  最大坐标: {encoder.max_coord}")
    
    # 编码解码
    x, y = 100, 200
    code = encoder.encode(x, y)
    print(f"\nencode({x}, {y}) = {code}")
    
    dx, dy = encoder.decode(code)
    print(f"decode({code}) = ({dx}, {dy})")
    
    # 邻居
    neighbors = encoder.get_neighbors(code, include_diagonal=False)
    print(f"\n邻居Morton码: {neighbors}")
    
    # 范围
    range_codes = encoder.get_range_codes(0, 0, 10, 10)
    print(f"\n范围(0,0)-(10,10)的码数量: {len(range_codes)}")
    
    # 3D编码器
    print("\n" + "-" * 30)
    encoder_3d = MortonEncoder3D(depth=8)
    print(f"3D编码器: {encoder_3d}")
    
    x, y, z = 10, 20, 30
    code_3d = encoder_3d.encode(x, y, z)
    print(f"encode({x}, {y}, {z}) = {code_3d}")
    
    dx, dy, dz = encoder_3d.decode(code_3d)
    print(f"decode({code_3d}) = ({dx}, {dy}, {dz})")


def example_grid_position():
    """网格位置示例"""
    print("\n" + "=" * 50)
    print("示例8: 网格坐标转换")
    print("=" * 50)
    
    # Morton码到网格位置
    print("\n4x4网格中的位置映射:")
    for code in range(16):
        try:
            row, col = morton_code_to_grid_position(code, 4)
            print(f"  Morton码 {code:2d} -> 网格({row}, {col})")
        except ValueError as e:
            print(f"  Morton码 {code:2d} -> 错误: {e}")
    
    # 应用场景
    print("\n应用场景:")
    print("  - 矩阵索引转换")
    print("  - 图像分块处理")
    print("  - 游戏棋盘坐标")


def example_sequence_generation():
    """序列生成示例"""
    print("\n" + "=" * 50)
    print("示例9: Morton序列生成")
    print("=" * 50)
    
    # 生成前16个坐标
    print("\nMorton顺序的前16个坐标:")
    seq = list(generate_morton_sequence_2d(16))
    for i, (x, y) in enumerate(seq):
        print(f"  {i:2d}: ({x}, {y}), Morton码={encode_2d(x, y)}")
    
    print("\nZ字形填充顺序可视化:")
    print("  深度1 (2x2):")
    print("    0→1")
    print("    ↓ ↗")
    print("    2→3")
    
    print("\n  深度2 (4x4):")
    print("    0→1  4→5")
    print("    ↓ ↗  ↓ ↗")
    print("    2→3  6→7")
    print("          ↖ ↓")
    print("    8→9 10→11")
    print("    ↓ ↗  ↓ ↗")
    print("   12→13 14→15")


def example_binary_visualization():
    """二进制可视化示例"""
    print("\n" + "=" * 50)
    print("示例10: Morton码二进制表示")
    print("=" * 50)
    
    # 二进制表示
    print("\nMorton码的二进制表示（交错模式）:")
    codes = [0, 1, 2, 3, 4, 5]
    for code in codes:
        x, y = decode_2d(code)
        binary = morton_code_to_binary_string(code, 8)
        x_bin = format(x, '04b')
        y_bin = format(y, '04b')
        print(f"  ({x}, {y}): x={x_bin}, y={y_bin} -> Morton={binary}")
    
    print("\n位交错原理:")
    print("  Morton码通过交错x和y的位来编码:")
    print("  例如: x=01, y=10 -> Morton=011 (y0x0y1x1)")
    print("  这使得相邻坐标的Morton码值也相近")


def example_real_world_use():
    """实际应用示例"""
    print("\n" + "=" * 50)
    print("示例11: 实际应用场景")
    print("=" * 50)
    
    # 场景1: 地理位置索引
    print("\n场景1: 地理位置索引")
    print("  问题: 在大量地理点数据中快速查找附近点")
    print("  解决方案:")
    
    # 模拟位置数据（假设坐标范围0-100）
    locations = [(23, 45), (67, 12), (10, 89), (55, 55), (78, 78)]
    print(f"  原始位置: {locations}")
    
    # Morton排序后
    sorted_locations = sort_positions_2d(locations)
    print(f"  Morton排序后: {sorted_locations}")
    
    # 查找(55,55)附近的点
    center_code = encode_2d(55, 55)
    neighbor_codes = get_neighbors_morton_2d(center_code)
    print(f"  (55,55)的邻居Morton码: {neighbor_codes}")
    
    # 场景2: 图像分块处理
    print("\n场景2: 图像分块处理")
    print("  问题: 将图像分成4x4块进行并行处理")
    print("  解决方案: 使用Morton码对块进行排序")
    
    blocks = list(generate_morton_sequence_2d(16))
    print(f"  16个块的处理顺序: {blocks}")
    print("  Morton顺序可以最大化缓存利用率")
    
    # 场景3: 范围查询优化
    print("\n场景3: 矩形范围查询")
    print("  问题: 查找矩形区域内的所有数据点")
    print("  解决方案: 将范围转换为Morton码列表")
    
    codes = range_to_morton_codes_2d(10, 10, 15, 15, max_depth=8)
    print(f"  区域(10,10)-(15,15)包含 {len(codes)} 个Morton码")
    print("  这些码在数据库索引中可以快速检索")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("Morton Code Utils 使用示例")
    print("=" * 60)
    
    example_basic_2d()
    example_basic_3d()
    example_morton_sorting()
    example_neighbors()
    example_hierarchy()
    example_range_encoding()
    example_encoder_class()
    example_grid_position()
    example_sequence_generation()
    example_binary_visualization()
    example_real_world_use()
    
    print("\n" + "=" * 60)
    print("示例完成!")
    print("=" * 60)
    print("\nMorton编码的核心优势:")
    print("  1. 将多维坐标映射为一维值，便于索引和排序")
    print("  2. 保持空间局部性，相邻坐标的Morton码值相近")
    print("  3. 支持高效的范围查询和邻居查找")
    print("  4. 层级结构便于空间分解和递归处理")


if __name__ == "__main__":
    main()