"""
Bitmask Utils 测试文件
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Bitmask,
    create_bitmask,
    from_bits,
    from_binary,
    from_hex,
    combine_bitmasks,
    intersect_bitmasks,
    count_bits,
    parity,
    reverse_bits,
    next_power_of_2,
    is_power_of_2,
    get_lsb,
    get_msb,
    gray_code,
    from_gray_code,
)


def test_bitmask_basic_operations():
    """测试基本操作"""
    print("测试基本操作...")
    
    mask = Bitmask(bits=8)
    
    # 设置位
    mask.set(0).set(2).set(4)
    assert mask.has(0), "位0应该被设置"
    assert mask.has(2), "位2应该被设置"
    assert not mask.has(1), "位1不应该被设置"
    
    # 清除位
    mask.clear(0)
    assert not mask.has(0), "位0应该被清除"
    
    # 切换位
    mask.toggle(1)
    assert mask.has(1), "位1应该被设置（切换后）"
    mask.toggle(1)
    assert not mask.has(1), "位1应该被清除（再次切换）"
    
    print("✅ 基本操作测试通过")


def test_bitmask_multi_bit_operations():
    """测试多位操作"""
    print("测试多位操作...")
    
    mask = Bitmask(bits=8)
    
    # 设置多个位
    mask.set_all([0, 1, 2, 3])
    assert mask.has_all([0, 1, 2, 3])
    
    # 清除多个位
    mask.clear_all([0, 1])
    assert not mask.has_any([0, 1])
    assert mask.has_all([2, 3])
    
    # 切换多个位
    mask.toggle_all([2, 4])
    assert not mask.has(2)
    assert mask.has(4)
    
    # has_none
    mask.clear_all([0, 1, 2, 3, 4])
    assert mask.has_none([0, 1, 2, 3, 4])
    
    print("✅ 多位操作测试通过")


def test_bitmask_range_operations():
    """测试范围操作"""
    print("测试范围操作...")
    
    mask = Bitmask(bits=8)
    
    # 设置范围
    mask.set_range(0, 3)
    assert mask.has_all([0, 1, 2, 3])
    
    # 清除范围
    mask.clear_range(1, 2)
    assert mask.has(0)
    assert not mask.has(1)
    assert not mask.has(2)
    assert mask.has(3)
    
    # 范围错误
    try:
        mask.set_range(5, 2)  # start > end
        assert False, "应该抛出异常"
    except ValueError:
        pass
    
    print("✅ 范围操作测试通过")


def test_bitmask_query_operations():
    """测试查询操作"""
    print("测试查询操作...")
    
    mask = Bitmask(bits=8)
    mask.set_all([0, 2, 4, 6])
    
    # 计数
    assert mask.count_set() == 4
    assert mask.count_clear() == 4
    
    # 第一个和最后一个设置位
    assert mask.first_set() == 0
    assert mask.last_set() == 6
    
    # 获取设置/清除位列表
    assert mask.get_set_bits() == [0, 2, 4, 6]
    assert mask.get_clear_bits() == [1, 3, 5, 7]
    
    # 空掩码
    empty = Bitmask(bits=8)
    assert empty.first_set() is None
    assert empty.last_set() is None
    assert empty.get_set_bits() == []
    
    print("✅ 查询操作测试通过")


def test_bitmask_manipulation_operations():
    """测试操作操作"""
    print("测试操作操作...")
    
    mask = Bitmask(value=0b10101010, bits=8)
    
    # 反转
    inverted = mask.copy().invert()
    assert inverted.to_int() == 0b01010101
    
    # 左移
    shifted = Bitmask(value=0b00001111, bits=8).shift_left(2)
    assert shifted.to_int() == 0b00111100
    
    # 右移
    shifted = Bitmask(value=0b11110000, bits=8).shift_right(2)
    assert shifted.to_int() == 0b00111100
    
    # 旋转
    rotated = Bitmask(value=0b11000000, bits=8).rotate_left(2)
    assert rotated.to_int() == 0b00000011
    
    rotated = Bitmask(value=0b00000011, bits=8).rotate_right(2)
    assert rotated.to_int() == 0b11000000
    
    print("✅ 操作操作测试通过")


def test_bitmask_logical_operations():
    """测试逻辑操作"""
    print("测试逻辑操作...")
    
    mask1 = Bitmask(value=0b1100, bits=8)
    mask2 = Bitmask(value=0b1010, bits=8)
    
    # AND
    result = mask1.copy().and_with(mask2)
    assert result.to_int() == 0b1000
    
    # OR
    result = mask1.copy().or_with(mask2)
    assert result.to_int() == 0b1110
    
    # XOR
    result = mask1.copy().xor_with(mask2)
    assert result.to_int() == 0b0110
    
    print("✅ 逻辑操作测试通过")


def test_bitmask_comparison_operations():
    """测试比较操作"""
    print("测试比较操作...")
    
    mask1 = Bitmask(value=0b1100, bits=8)
    mask2 = Bitmask(value=0b1111, bits=8)
    mask3 = Bitmask(value=0b0011, bits=8)
    
    # 子集
    assert mask1.is_subset(mask2)  # 1100 是 1111 的子集
    assert not mask1.is_subset(mask3)
    
    # 超集
    assert mask2.is_superset(mask1)
    assert not mask1.is_superset(mask2)
    
    # 重叠
    # mask1 = 1100 (位2和位3设置), mask3 = 0011 (位0和位1设置) - 实际无重叠
    assert not mask1.overlaps(mask3)  # 1100 和 0011 没有重叠
    assert mask1.overlaps(mask2)  # 1100 和 1111 有重叠
    
    # 不相交
    mask4 = Bitmask(value=0b0011, bits=8)
    mask5 = Bitmask(value=0b1100, bits=8)
    # 注意: 这里实际上有重叠（位2和位3都设置了）
    # 让我们创建真正不相交的掩码
    mask6 = Bitmask(value=0b00001111, bits=8)
    mask7 = Bitmask(value=0b11110000, bits=8)
    assert mask6.is_disjoint(mask7)
    
    print("✅ 比较操作测试通过")


def test_bitmask_conversion_operations():
    """测试转换操作"""
    print("测试转换操作...")
    
    mask = Bitmask(value=0b10101010, bits=8)
    
    # 整数
    assert mask.to_int() == 0b10101010
    assert int(mask) == 0b10101010
    
    # 二进制
    assert mask.to_bin() == "0b10101010"
    assert mask.to_bin(pad=False) == "0b10101010"
    
    # 十六进制
    assert mask.to_hex() == "0xaa"
    
    # 列表
    lst = mask.to_list()
    assert lst == [0, 1, 0, 1, 0, 1, 0, 1]  # LSB first
    
    # 集合
    s = mask.to_set()
    assert s == {1, 3, 5, 7}  # 设置位的索引
    
    print("✅ 转换操作测试通过")


def test_bitmask_magic_methods():
    """测试魔法方法"""
    print("测试魔法方法...")
    
    mask = Bitmask(value=0b1010, bits=8)
    
    # __int__
    assert int(mask) == 0b1010
    
    # __str__
    assert "1010" in str(mask)
    
    # __len__
    assert len(mask) == 8
    
    # __getitem__
    assert mask[0] == 0
    assert mask[1] == 1
    
    # __setitem__
    mask[0] = 1
    assert mask.has(0)
    mask[0] = 0
    assert not mask.has(0)
    
    # __contains__
    assert 1 in mask
    assert 0 not in mask
    
    # __and__, __or__, __xor__
    other = Bitmask(value=0b1100, bits=8)
    assert (mask & other).to_int() == (0b1010 & 0b1100)
    assert (mask | other).to_int() == (0b1010 | 0b1100)
    assert (mask ^ other).to_int() == (0b1010 ^ 0b1100)
    
    # __invert__
    inverted = ~mask
    # 只检查8位内的反转
    assert inverted.to_int() == (0xff ^ 0b1010) & 0xff
    
    # __lshift__, __rshift__
    shifted = mask << 2
    assert shifted.to_int() == (0b1010 << 2) & 0xff
    
    # __eq__, __hash__
    mask1 = Bitmask(value=5, bits=8)
    mask2 = Bitmask(value=5, bits=8)
    mask3 = Bitmask(value=5, bits=16)
    assert mask1 == mask2
    assert mask1 != mask3
    assert hash(mask1) == hash(mask2)
    
    # __bool__
    assert bool(Bitmask(value=1, bits=8))
    assert not bool(Bitmask(value=0, bits=8))
    
    print("✅ 魔法方法测试通过")


def test_bitmask_copy_reset_fill():
    """测试复制、重置、填充"""
    print("测试复制、重置、填充...")
    
    mask = Bitmask(value=0b1010, bits=8)
    
    # 复制
    copy = mask.copy()
    assert copy.to_int() == 0b1010
    copy.set(0)
    assert mask.to_int() == 0b1010  # 原始不变
    
    # 重置
    mask.reset()
    assert mask.to_int() == 0
    
    # 填充
    mask.fill()
    assert mask.to_int() == 0b11111111
    
    print("✅ 复制、重置、填充测试通过")


def test_functional_api():
    """测试函数式API"""
    print("测试函数式API...")
    
    # create_bitmask
    mask = create_bitmask(5, bits=8)
    assert mask.to_int() == 5
    
    # from_bits
    mask = from_bits([0, 2, 4], total_bits=8)
    assert mask.has_all([0, 2, 4])
    assert mask.to_int() == 0b0010101
    
    # from_binary
    mask = from_binary("10101010")
    assert mask.to_int() == 0b10101010
    
    mask = from_binary("0b1100", total_bits=8)
    assert mask.to_int() == 0b1100
    
    # from_hex
    mask = from_hex("ff")
    assert mask.to_int() == 255
    
    mask = from_hex("0xaa", total_bits=8)
    assert mask.to_int() == 0xaa
    
    # combine_bitmasks
    m1 = Bitmask(value=0b1100, bits=8)
    m2 = Bitmask(value=0b0011, bits=8)
    combined = combine_bitmasks(m1, m2)
    assert combined.to_int() == 0b1111
    
    # intersect_bitmasks
    m1 = Bitmask(value=0b1110, bits=8)
    m2 = Bitmask(value=0b1010, bits=8)
    intersected = intersect_bitmasks(m1, m2)
    assert intersected.to_int() == 0b1010
    
    print("✅ 函数式API测试通过")


def test_utility_functions():
    """测试工具函数"""
    print("测试工具函数...")
    
    # count_bits
    assert count_bits(0) == 0
    assert count_bits(1) == 1
    assert count_bits(7) == 3
    assert count_bits(255) == 8
    
    # parity
    assert parity(0) == 0
    assert parity(1) == 1
    assert parity(3) == 0  # 11 -> XOR = 0
    assert parity(7) == 1  # 111 -> XOR = 1
    
    # reverse_bits
    assert reverse_bits(0b11010010, 8) == 0b01001011
    
    # next_power_of_2
    assert next_power_of_2(0) == 1
    assert next_power_of_2(1) == 1
    assert next_power_of_2(2) == 2
    assert next_power_of_2(3) == 4
    assert next_power_of_2(10) == 16
    assert next_power_of_2(16) == 16
    
    # is_power_of_2
    assert is_power_of_2(1)
    assert is_power_of_2(2)
    assert is_power_of_2(4)
    assert is_power_of_2(8)
    assert not is_power_of_2(0)
    assert not is_power_of_2(3)
    assert not is_power_of_2(6)
    
    # get_lsb
    assert get_lsb(0) == -1
    assert get_lsb(1) == 0
    assert get_lsb(2) == 1
    assert get_lsb(8) == 3
    
    # get_msb
    assert get_msb(0) == -1
    assert get_msb(1, bits=8) == 0
    assert get_msb(8, bits=8) == 3
    assert get_msb(255, bits=8) == 7
    
    # gray_code
    assert gray_code(0) == 0
    assert gray_code(1) == 1
    assert gray_code(2) == 3
    assert gray_code(3) == 2
    assert gray_code(4) == 6
    
    # from_gray_code
    assert from_gray_code(0) == 0
    assert from_gray_code(1) == 1
    assert from_gray_code(3) == 2
    assert from_gray_code(2) == 3
    assert from_gray_code(6) == 4
    
    print("✅ 工具函数测试通过")


def test_bitmask_edge_cases():
    """测试边界情况"""
    print("测试边界情况...")
    
    # 位数为0（应该失败）
    try:
        Bitmask(bits=0)
        assert False, "应该抛出异常"
    except ValueError:
        pass
    
    # 位数为负（应该失败）
    try:
        Bitmask(bits=-1)
        assert False, "应该抛出异常"
    except ValueError:
        pass
    
    # 位超出范围
    mask = Bitmask(bits=8)
    try:
        mask.set(8)  # 超出范围
        assert False, "应该抛出异常"
    except ValueError:
        pass
    
    try:
        mask.has(-1)
        assert False, "应该抛出异常"
    except ValueError:
        pass
    
    print("✅ 边界情况测试通过")


def test_bitmask_large_bits():
    """测试大位数"""
    print("测试大位数...")
    
    # 32位
    mask = Bitmask(bits=32)
    mask.set_all([0, 15, 31])
    assert mask.has_all([0, 15, 31])
    assert mask.count_set() == 3
    
    # 64位
    mask = Bitmask(bits=64)
    mask.set(63)
    assert mask.has(63)
    assert mask.first_set() == 63
    
    print("✅ 大位数测试通过")


def test_bitmask_initialization():
    """测试初始化"""
    print("测试初始化...")
    
    # 默认值
    mask = Bitmask()
    assert mask.to_int() == 0
    assert len(mask) == 32
    
    # 自定义值
    mask = Bitmask(value=255, bits=8)
    assert mask.to_int() == 255
    
    # 值被截断到位数范围内
    mask = Bitmask(value=256, bits=8)  # 256 = 0x100, 超出8位
    assert mask.to_int() == 0  # 截断后
    
    print("✅ 初始化测试通过")


def test_repr():
    """测试 repr"""
    print("测试 repr...")
    
    mask = Bitmask(value=5, bits=8)
    r = repr(mask)
    assert "Bitmask" in r
    assert "5" in r
    assert "8" in r
    
    print("✅ repr测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("Bitmask Utils 测试套件")
    print("=" * 50)
    
    tests = [
        test_bitmask_basic_operations,
        test_bitmask_multi_bit_operations,
        test_bitmask_range_operations,
        test_bitmask_query_operations,
        test_bitmask_manipulation_operations,
        test_bitmask_logical_operations,
        test_bitmask_comparison_operations,
        test_bitmask_conversion_operations,
        test_bitmask_magic_methods,
        test_bitmask_copy_reset_fill,
        test_functional_api,
        test_utility_functions,
        test_bitmask_edge_cases,
        test_bitmask_large_bits,
        test_bitmask_initialization,
        test_repr,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} 失败: {e}")
            failed += 1
    
    print("=" * 50)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)