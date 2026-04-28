#!/usr/bin/env python3
"""
Morton Code Utils 测试文件

测试覆盖：
- 2D Morton编码/解码
- 3D Morton编码/解码
- 位操作函数
- 邻居查询
- 层级操作
- 范围查询
- 编码器类
- 边界值测试
"""

import sys
import os

# 添加父目录到路径以导入模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    spread_bits_2d, compact_bits_2d,
    spread_bits_3d, compact_bits_3d,
    encode_2d, decode_2d,
    encode_3d, decode_3d,
    encode_with_depth_2d, decode_with_depth_2d,
    get_neighbors_2d, get_neighbors_morton_2d,
    get_cell_level_2d,
    get_parent_2d, get_children_2d,
    is_ancestor_2d,
    range_to_morton_codes_2d,
    morton_code_to_binary_string,
    compare_positions_2d,
    sort_positions_2d,
    get_morton_distance_2d,
    get_quadrant_2d,
    morton_code_to_grid_position,
    generate_morton_sequence_2d,
    MortonEncoder2D, MortonEncoder3D,
)


def test_spread_bits_2d():
    """测试2D位分散函数"""
    print("测试 spread_bits_2d...")
    
    # 基本测试
    assert spread_bits_2d(0) == 0, "0应该返回0"
    assert spread_bits_2d(1) == 1, "1应该返回1"
    assert spread_bits_2d(2) == 4, "2应该返回4 (0b10 -> 0b100)"
    assert spread_bits_2d(3) == 5, "3应该返回5 (0b11 -> 0b101)"
    
    # 边界值
    assert spread_bits_2d(0xFFFF) == 0x55555555, "最大16位值测试"
    
    # 验证分散后的模式
    # 0b111 -> 0b010101 = 21
    assert spread_bits_2d(7) == 21, "7应该分散为21"
    
    print("  ✓ spread_bits_2d 测试通过")


def test_compact_bits_2d():
    """测试2D位压缩函数"""
    print("测试 compact_bits_2d...")
    
    # 基本测试（与spread_bits_2d互逆）
    assert compact_bits_2d(0) == 0, "0应该返回0"
    assert compact_bits_2d(1) == 1, "1应该返回1"
    assert compact_bits_2d(4) == 2, "4应该返回2"
    assert compact_bits_2d(5) == 3, "5应该返回3"
    
    # 互逆性测试
    for i in range(256):
        assert compact_bits_2d(spread_bits_2d(i)) == i, f"互逆测试失败: {i}"
    
    print("  ✓ compact_bits_2d 测试通过")


def test_spread_bits_3d():
    """测试3D位分散函数"""
    print("测试 spread_bits_3d...")
    
    # 基本测试
    assert spread_bits_3d(0) == 0, "0应该返回0"
    assert spread_bits_3d(1) == 1, "1应该返回1"
    assert spread_bits_3d(2) == 8, "2应该返回8"
    assert spread_bits_3d(3) == 9, "3应该返回9"
    
    print("  ✓ spread_bits_3d 测试通过")


def test_compact_bits_3d():
    """测试3D位压缩函数"""
    print("测试 compact_bits_3d...")
    
    # 基本测试
    assert compact_bits_3d(0) == 0, "0应该返回0"
    assert compact_bits_3d(1) == 1, "1应该返回1"
    assert compact_bits_3d(8) == 2, "8应该返回2"
    
    # 互逆性测试
    for i in range(128):
        assert compact_bits_3d(spread_bits_3d(i)) == i, f"3D互逆测试失败: {i}"
    
    print("  ✓ compact_bits_3d 测试通过")


def test_encode_decode_2d():
    """测试2D Morton编码和解码"""
    print("测试 encode_2d 和 decode_2d...")
    
    # 基本编码测试
    assert encode_2d(0, 0) == 0, "(0, 0) -> 0"
    assert encode_2d(1, 0) == 1, "(1, 0) -> 1"
    assert encode_2d(0, 1) == 2, "(0, 1) -> 2"
    assert encode_2d(1, 1) == 3, "(1, 1) -> 3"
    assert encode_2d(2, 0) == 4, "(2, 0) -> 4"
    assert encode_2d(3, 0) == 5, "(3, 0) -> 5"
    assert encode_2d(2, 1) == 6, "(2, 1) -> 6"
    assert encode_2d(3, 1) == 7, "(3, 1) -> 7"
    
    # 解码测试
    assert decode_2d(0) == (0, 0), "0 -> (0, 0)"
    assert decode_2d(1) == (1, 0), "1 -> (1, 0)"
    assert decode_2d(2) == (0, 1), "2 -> (0, 1)"
    assert decode_2d(3) == (1, 1), "3 -> (1, 1)"
    
    # 编码解码互逆性
    for x in range(100):
        for y in range(100):
            code = encode_2d(x, y)
            dx, dy = decode_2d(code)
            assert (dx, dy) == (x, y), f"互逆失败: ({x}, {y}) -> {code} -> ({dx}, {dy})"
    
    print("  ✓ encode_2d 和 decode_2d 测试通过")


def test_encode_decode_2d_boundary():
    """测试2D编码边界值"""
    print("测试 2D编码边界值...")
    
    # 最大值测试
    max_coord = 65535
    code = encode_2d(max_coord, max_coord)
    x, y = decode_2d(code)
    assert (x, y) == (max_coord, max_coord), "最大坐标测试失败"
    
    # 边界值
    assert encode_2d(0, 0) == 0, "原点测试"
    assert encode_2d(0, 65535) != 0, "Y轴最大值"
    assert encode_2d(65535, 0) != 0, "X轴最大值"
    
    # 错误处理
    try:
        encode_2d(-1, 0)
        assert False, "应该抛出异常"
    except ValueError:
        pass
    
    try:
        encode_2d(0, 65536)
        assert False, "应该抛出异常"
    except ValueError:
        pass
    
    try:
        decode_2d(-1)
        assert False, "应该抛出异常"
    except ValueError:
        pass
    
    print("  ✓ 2D编码边界值测试通过")


def test_encode_decode_3d():
    """测试3D Morton编码和解码"""
    print("测试 encode_3d 和 decode_3d...")
    
    # 基本编码测试
    assert encode_3d(0, 0, 0) == 0, "(0, 0, 0) -> 0"
    assert encode_3d(1, 0, 0) == 1, "(1, 0, 0) -> 1"
    assert encode_3d(0, 1, 0) == 2, "(0, 1, 0) -> 2"
    assert encode_3d(1, 1, 0) == 3, "(1, 1, 0) -> 3"
    assert encode_3d(0, 0, 1) == 4, "(0, 0, 1) -> 4"
    assert encode_3d(1, 1, 1) == 7, "(1, 1, 1) -> 7"
    
    # 解码测试
    assert decode_3d(0) == (0, 0, 0), "0 -> (0, 0, 0)"
    assert decode_3d(1) == (1, 0, 0), "1 -> (1, 0, 0)"
    assert decode_3d(4) == (0, 0, 1), "4 -> (0, 0, 1)"
    assert decode_3d(7) == (1, 1, 1), "7 -> (1, 1, 1)"
    
    # 编码解码互逆性
    for x in range(50):
        for y in range(50):
            for z in range(50):
                code = encode_3d(x, y, z)
                dx, dy, dz = decode_3d(code)
                assert (dx, dy, dz) == (x, y, z), \
                    f"互逆失败: ({x}, {y}, {z}) -> {code} -> ({dx}, {dy}, {dz})"
    
    print("  ✓ encode_3d 和 decode_3d 测试通过")


def test_encode_decode_3d_boundary():
    """测试3D编码边界值"""
    print("测试 3D编码边界值...")
    
    # 最大值测试
    max_coord = 1023
    code = encode_3d(max_coord, max_coord, max_coord)
    x, y, z = decode_3d(code)
    assert (x, y, z) == (max_coord, max_coord, max_coord), "最大坐标测试失败"
    
    # 错误处理
    try:
        encode_3d(-1, 0, 0)
        assert False, "应该抛出异常"
    except ValueError:
        pass
    
    try:
        encode_3d(0, 0, 1024)
        assert False, "应该抛出异常"
    except ValueError:
        pass
    
    print("  ✓ 3D编码边界值测试通过")


def test_encode_decode_with_depth_2d():
    """测试带深度的编码解码"""
    print("测试 encode_with_depth_2d 和 decode_with_depth_2d...")
    
    # 深度1
    assert encode_with_depth_2d(0, 0, 1) == 0
    assert encode_with_depth_2d(1, 0, 1) == 1
    assert encode_with_depth_2d(0, 1, 1) == 2
    assert encode_with_depth_2d(1, 1, 1) == 3
    
    # 深度10
    for x in range(100):
        for y in range(100):
            code = encode_with_depth_2d(x, y, 10)
            dx, dy = decode_with_depth_2d(code, 10)
            assert (dx, dy) == (x, y), f"深度10互逆失败: ({x}, {y})"
    
    # 深度边界
    try:
        encode_with_depth_2d(0, 0, 0)
        assert False, "深度0应该抛出异常"
    except ValueError:
        pass
    
    try:
        encode_with_depth_2d(0, 0, 33)
        assert False, "深度33应该抛出异常"
    except ValueError:
        pass
    
    # 坐标超出范围
    try:
        encode_with_depth_2d(4, 0, 2)  # 深度2最大坐标是3
        assert False, "坐标超出范围应该抛出异常"
    except ValueError:
        pass
    
    print("  ✓ 带深度的编码解码测试通过")


def test_get_neighbors_2d():
    """测试获取邻居"""
    print("测试 get_neighbors_2d...")
    
    # 原点邻居（4邻域）
    neighbors = get_neighbors_2d(0, 0, include_diagonal=False)
    assert (1, 0) in neighbors, "应该包含右边邻居"
    assert (0, 1) in neighbors, "应该包含上边邻居"
    assert len(neighbors) == 2, "原点应该有2个邻居（不含对角）"
    
    # 中心点邻居（4邻域）
    neighbors = get_neighbors_2d(5, 5, include_diagonal=False)
    assert (4, 5) in neighbors, "应该包含左边邻居"
    assert (6, 5) in neighbors, "应该包含右边邻居"
    assert (5, 4) in neighbors, "应该包含下边邻居"
    assert (5, 6) in neighbors, "应该包含上边邻居"
    assert len(neighbors) == 4, "中心点应该有4个邻居"
    
    # 包含对角邻居
    neighbors = get_neighbors_2d(5, 5, include_diagonal=True)
    assert len(neighbors) == 8, "中心点应该有8个邻居（含对角）"
    assert (4, 4) in neighbors, "应该包含左下邻居"
    assert (6, 6) in neighbors, "应该包含右上邻居"
    
    print("  ✓ get_neighbors_2d 测试通过")


def test_get_neighbors_morton_2d():
    """测试获取Morton码邻居"""
    print("测试 get_neighbors_morton_2d...")
    
    # 原点的Morton码邻居
    code = encode_2d(0, 0)
    neighbors = get_neighbors_morton_2d(code, include_diagonal=False)
    assert len(neighbors) == 2, "原点应该有2个邻居"
    assert encode_2d(1, 0) in neighbors, "应该包含(1, 0)"
    assert encode_2d(0, 1) in neighbors, "应该包含(0, 1)"
    
    print("  ✓ get_neighbors_morton_2d 测试通过")


def test_get_cell_level_2d():
    """测试获取单元层级"""
    print("测试 get_cell_level_2d...")
    
    assert get_cell_level_2d(0) == 0, "0的层级应该是0"
    assert get_cell_level_2d(1) == 1, "1的层级应该是1"
    assert get_cell_level_2d(3) == 1, "3的层级应该是1"
    assert get_cell_level_2d(15) == 2, "15的层级应该是2"
    
    print("  ✓ get_cell_level_2d 测试通过")


def test_get_parent_2d():
    """测试获取父级"""
    print("测试 get_parent_2d...")
    
    assert get_parent_2d(0) == 0, "0的父级是0"
    assert get_parent_2d(1) == 0, "1的父级是0"
    assert get_parent_2d(2) == 0, "2的父级是0"
    assert get_parent_2d(3) == 0, "3的父级是0"
    assert get_parent_2d(4) == 1, "4的父级是1"
    assert get_parent_2d(7) == 1, "7的父级是1"
    
    print("  ✓ get_parent_2d 测试通过")


def test_get_children_2d():
    """测试获取子级"""
    print("测试 get_children_2d...")
    
    # 0的子节点
    children = get_children_2d(0)
    assert children == [0, 1, 2, 3], f"0的子节点应该是[0,1,2,3]，得到 {children}"
    
    # 1的子节点
    children = get_children_2d(1)
    assert children == [4, 5, 6, 7], f"1的子节点应该是[4,5,6,7]，得到 {children}"
    
    # 验证父子关系
    for parent in range(10):
        children = get_children_2d(parent)
        for child in children:
            assert get_parent_2d(child) == parent, \
                f"子节点{child}的父节点应该是{parent}"
    
    print("  ✓ get_children_2d 测试通过")


def test_is_ancestor_2d():
    """测试祖先关系检查"""
    print("测试 is_ancestor_2d...")
    
    # 0是所有码的祖先
    assert is_ancestor_2d(0, 1) == True, "0是1的祖先"
    assert is_ancestor_2d(0, 7) == True, "0是7的祖先"
    assert is_ancestor_2d(0, 15) == True, "0是15的祖先"
    
    # 1是其子节点的祖先
    assert is_ancestor_2d(1, 4) == True, "1是4的祖先"
    assert is_ancestor_2d(1, 5) == True, "1是5的祖先"
    assert is_ancestor_2d(1, 6) == True, "1是6的祖先"
    assert is_ancestor_2d(1, 7) == True, "1是7的祖先"
    
    # 不是祖先
    assert is_ancestor_2d(1, 2) == False, "1不是2的祖先"
    assert is_ancestor_2d(1, 8) == False, "1不是8的祖先"
    assert is_ancestor_2d(2, 1) == False, "2不是1的祖先"
    
    # 自己不是自己的祖先
    assert is_ancestor_2d(0, 0) == False, "自己不是自己的祖先"
    assert is_ancestor_2d(1, 1) == False, "自己不是自己的祖先"
    
    print("  ✓ is_ancestor_2d 测试通过")


def test_range_to_morton_codes_2d():
    """测试范围转换为Morton码"""
    print("测试 range_to_morton_codes_2d...")
    
    # 单点范围
    codes = range_to_morton_codes_2d(0, 0, 0, 0)
    assert codes == [0], "单点(0,0)应该是[0]"
    
    # 2x2范围
    codes = range_to_morton_codes_2d(0, 0, 1, 1, max_depth=1)
    assert sorted(codes) == [0, 1, 2, 3], "2x2范围应该是[0,1,2,3]"
    
    # 较大范围
    codes = range_to_morton_codes_2d(0, 0, 3, 0, max_depth=3)
    expected = [encode_2d(0, 0), encode_2d(1, 0), encode_2d(2, 0), encode_2d(3, 0)]
    assert sorted(codes) == sorted(expected), f"范围测试失败"
    
    # 错误处理
    try:
        range_to_morton_codes_2d(-1, 0, 1, 1)
        assert False, "负坐标应该抛出异常"
    except ValueError:
        pass
    
    try:
        range_to_morton_codes_2d(2, 0, 1, 1)
        assert False, "最小>最大应该抛出异常"
    except ValueError:
        pass
    
    print("  ✓ range_to_morton_codes_2d 测试通过")


def test_morton_code_to_binary_string():
    """测试Morton码转二进制字符串"""
    print("测试 morton_code_to_binary_string...")
    
    assert morton_code_to_binary_string(0, 4) == "0000", "0应该是0000"
    assert morton_code_to_binary_string(1, 4) == "0001", "1应该是0001"
    assert morton_code_to_binary_string(15, 4) == "1111", "15应该是1111"
    assert morton_code_to_binary_string(5, 8) == "00000101", "5应该是00000101"
    
    print("  ✓ morton_code_to_binary_string 测试通过")


def test_compare_positions_2d():
    """测试位置比较"""
    print("测试 compare_positions_2d...")
    
    assert compare_positions_2d(0, 0, 1, 0) == -1, "(0,0) < (1,0)"
    assert compare_positions_2d(1, 0, 0, 0) == 1, "(1,0) > (0,0)"
    assert compare_positions_2d(0, 0, 0, 0) == 0, "(0,0) = (0,0)"
    
    # Morton顺序：(0,1) > (1,0) 因为 encode_2d(0,1)=2 > encode_2d(1,0)=1
    assert compare_positions_2d(1, 0, 0, 1) == -1, "(1,0) < (0,1) in Morton order"
    
    print("  ✓ compare_positions_2d 测试通过")


def test_sort_positions_2d():
    """测试Morton排序"""
    print("测试 sort_positions_2d...")
    
    # 基本排序
    positions = [(0, 1), (1, 0), (0, 0)]
    sorted_pos = sort_positions_2d(positions)
    # Morton码顺序: (0,0)=0, (1,0)=1, (0,1)=2
    assert sorted_pos == [(0, 0), (1, 0), (0, 1)], f"排序错误: {sorted_pos}"
    
    # 更多测试
    positions = [(3, 0), (0, 0), (1, 1), (0, 3), (2, 2)]
    sorted_pos = sort_positions_2d(positions)
    
    # 验证排序后的Morton码是递增的
    codes = [encode_2d(x, y) for x, y in sorted_pos]
    assert codes == sorted(codes), "排序后Morton码应该是递增的"
    
    print("  ✓ sort_positions_2d 测试通过")


def test_get_morton_distance_2d():
    """测试Morton距离"""
    print("测试 get_morton_distance_2d...")
    
    assert get_morton_distance_2d(0, 0) == 0, "相同点的距离为0"
    assert get_morton_distance_2d(5, 10) == 5, "距离应该为5"
    assert get_morton_distance_2d(10, 5) == 5, "距离应该为5（绝对值）"
    
    print("  ✓ get_morton_distance_2d 测试通过")


def test_get_quadrant_2d():
    """测试象限判断"""
    print("测试 get_quadrant_2d...")
    
    # 以(10, 10)为中心
    center_x, center_y = 10, 10
    
    # 右下 (x >= cx, y < cy)
    assert get_quadrant_2d(15, 5, center_x, center_y) == 0, "右下象限"
    assert get_quadrant_2d(10, 5, center_x, center_y) == 0, "右下象限（边界）"
    
    # 左下 (x < cx, y < cy)
    assert get_quadrant_2d(5, 5, center_x, center_y) == 1, "左下象限"
    
    # 右上 (x >= cx, y >= cy)
    assert get_quadrant_2d(15, 15, center_x, center_y) == 2, "右上象限"
    assert get_quadrant_2d(10, 10, center_x, center_y) == 2, "右上象限（边界）"
    
    # 左上 (x < cx, y >= cy)
    assert get_quadrant_2d(5, 15, center_x, center_y) == 3, "左上象限"
    
    print("  ✓ get_quadrant_2d 测试通过")


def test_morton_code_to_grid_position():
    """测试Morton码转网格位置"""
    print("测试 morton_code_to_grid_position...")
    
    # 4x4网格
    assert morton_code_to_grid_position(0, 4) == (0, 0), "码0 -> (0, 0)"
    assert morton_code_to_grid_position(3, 4) == (1, 1), "码3 -> (1, 1)"
    assert morton_code_to_grid_position(4, 4) == (0, 2), "码4 -> (0, 2)"
    
    # 错误处理
    try:
        morton_code_to_grid_position(0, 3)  # 3不是2的幂
        assert False, "非2的幂网格应该抛出异常"
    except ValueError:
        pass
    
    print("  ✓ morton_code_to_grid_position 测试通过")


def test_generate_morton_sequence_2d():
    """测试Morton序列生成"""
    print("测试 generate_morton_sequence_2d...")
    
    # 生成前4个坐标
    seq = list(generate_morton_sequence_2d(4))
    assert seq == [(0, 0), (1, 0), (0, 1), (1, 1)], f"序列错误: {seq}"
    
    # 生成更多坐标并验证Morton码顺序
    seq = list(generate_morton_sequence_2d(100))
    for i, (x, y) in enumerate(seq):
        assert encode_2d(x, y) == i, f"序列位置{i}的坐标({x},{y})Morton码应该是{i}"
    
    print("  ✓ generate_morton_sequence_2d 测试通过")


def test_morton_encoder_2d():
    """测试MortonEncoder2D类"""
    print("测试 MortonEncoder2D...")
    
    # 默认深度
    encoder = MortonEncoder2D()
    assert encoder.depth == 16, "默认深度应该是16"
    
    # 自定义深度
    encoder = MortonEncoder2D(depth=10)
    assert encoder.depth == 10, "深度应该是10"
    assert encoder.max_coord == 1023, "最大坐标应该是1023"
    
    # 编码解码
    for x in range(100):
        for y in range(100):
            code = encoder.encode(x, y)
            dx, dy = encoder.decode(code)
            assert (dx, dy) == (x, y), f"互逆失败: ({x}, {y})"
    
    # 邻居
    code = encoder.encode(5, 5)
    neighbors = encoder.get_neighbors(code)
    assert len(neighbors) == 8, "应该有8个邻居"
    
    # 父子节点
    children = encoder.get_children(code)
    parent = encoder.get_parent(code)
    assert parent == get_parent_2d(code), "父节点应该一致"
    assert children == get_children_2d(code), "子节点应该一致"
    
    # 范围编码
    codes = encoder.get_range_codes(0, 0, 1, 1)
    assert sorted(codes) == [0, 1, 2, 3], "范围编码错误"
    
    # 错误处理
    try:
        MortonEncoder2D(depth=0)
        assert False, "深度0应该抛出异常"
    except ValueError:
        pass
    
    try:
        MortonEncoder2D(depth=33)
        assert False, "深度33应该抛出异常"
    except ValueError:
        pass
    
    # 字符串表示
    encoder = MortonEncoder2D(depth=8)
    assert "MortonEncoder2D" in repr(encoder), "repr应该包含类名"
    assert "depth=8" in repr(encoder), "repr应该包含深度"
    
    print("  ✓ MortonEncoder2D 测试通过")


def test_morton_encoder_3d():
    """测试MortonEncoder3D类"""
    print("测试 MortonEncoder3D...")
    
    # 默认深度
    encoder = MortonEncoder3D()
    assert encoder.depth == 10, "默认深度应该是10"
    
    # 自定义深度
    encoder = MortonEncoder3D(depth=8)
    assert encoder.depth == 8, "深度应该是8"
    assert encoder.max_coord == 255, "最大坐标应该是255"
    
    # 编码解码
    for x in range(20):
        for y in range(20):
            for z in range(20):
                code = encoder.encode(x, y, z)
                dx, dy, dz = encoder.decode(code)
                assert (dx, dy, dz) == (x, y, z), f"互逆失败: ({x}, {y}, {z})"
    
    # 错误处理
    try:
        MortonEncoder3D(depth=0)
        assert False, "深度0应该抛出异常"
    except ValueError:
        pass
    
    try:
        MortonEncoder3D(depth=11)
        assert False, "深度11应该抛出异常"
    except ValueError:
        pass
    
    # 坐标超出范围
    try:
        encoder.encode(256, 0, 0)  # 超过max_coord=255
        assert False, "坐标超出范围应该抛出异常"
    except ValueError:
        pass
    
    # 字符串表示
    encoder = MortonEncoder3D(depth=5)
    assert "MortonEncoder3D" in repr(encoder), "repr应该包含类名"
    assert "depth=5" in repr(encoder), "repr应该包含深度"
    
    print("  ✓ MortonEncoder3D 测试通过")


def test_performance():
    """性能测试"""
    print("测试性能...")
    
    import time
    
    # 2D编码性能
    start = time.time()
    for x in range(1000):
        for y in range(1000):
            code = encode_2d(x, y)
            dx, dy = decode_2d(code)
    elapsed = time.time() - start
    print(f"  2D编码解码 1,000,000 次: {elapsed:.3f}秒")
    
    # 3D编码性能
    start = time.time()
    for x in range(100):
        for y in range(100):
            for z in range(100):
                code = encode_3d(x, y, z)
                dx, dy, dz = decode_3d(code)
    elapsed = time.time() - start
    print(f"  3D编码解码 1,000,000 次: {elapsed:.3f}秒")
    
    print("  ✓ 性能测试通过")


def test_special_cases():
    """特殊情况测试"""
    print("测试特殊情况...")
    
    # 零值
    assert encode_2d(0, 0) == 0, "原点应该编码为0"
    assert decode_2d(0) == (0, 0), "0应该解码为原点"
    assert encode_3d(0, 0, 0) == 0, "原点应该编码为0"
    assert decode_3d(0) == (0, 0, 0), "0应该解码为原点"
    
    # 对称性测试
    assert encode_2d(100, 200) != encode_2d(200, 100), "坐标顺序不同应该产生不同的码"
    
    # Morton码的Z字形模式
    # 第一个Z字(0-3): (0,0), (1,0), (0,1), (1,1)
    expected = [(0, 0), (1, 0), (0, 1), (1, 1)]
    for i, pos in enumerate(expected):
        assert decode_2d(i) == pos, f"Morton码{i}应该是{pos}"
    
    # 第二个Z字(4-7): 从(2,0)开始
    expected = [(2, 0), (3, 0), (2, 1), (3, 1)]
    for i, pos in enumerate(expected):
        assert decode_2d(i + 4) == pos, f"Morton码{i+4}应该是{pos}"
    
    print("  ✓ 特殊情况测试通过")


def main():
    """运行所有测试"""
    print("=" * 60)
    print("Morton Code Utils 测试")
    print("=" * 60)
    
    # 位操作测试
    test_spread_bits_2d()
    test_compact_bits_2d()
    test_spread_bits_3d()
    test_compact_bits_3d()
    
    # 2D编码测试
    test_encode_decode_2d()
    test_encode_decode_2d_boundary()
    
    # 3D编码测试
    test_encode_decode_3d()
    test_encode_decode_3d_boundary()
    
    # 深度测试
    test_encode_decode_with_depth_2d()
    
    # 功能测试
    test_get_neighbors_2d()
    test_get_neighbors_morton_2d()
    test_get_cell_level_2d()
    test_get_parent_2d()
    test_get_children_2d()
    test_is_ancestor_2d()
    test_range_to_morton_codes_2d()
    test_morton_code_to_binary_string()
    test_compare_positions_2d()
    test_sort_positions_2d()
    test_get_morton_distance_2d()
    test_get_quadrant_2d()
    test_morton_code_to_grid_position()
    test_generate_morton_sequence_2d()
    
    # 类测试
    test_morton_encoder_2d()
    test_morton_encoder_3d()
    
    # 性能和特殊测试
    test_performance()
    test_special_cases()
    
    print()
    print("=" * 60)
    print("✅ 所有测试通过!")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())