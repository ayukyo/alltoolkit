"""
Bitmap Utils 测试套件

测试覆盖：
- 基本位操作
- 统计与查询
- 位图运算
- 序列化与反序列化
- 迭代器
- 稀疏位图
"""

import sys
sys.path.insert(0, '..')

from mod import (
    Bitmap, 
    SparseBitmap,
    create_bitmap,
    bitmap_from_string,
    bitmap_union,
    bitmap_intersection,
    bitmap_difference
)


def test_basic_operations():
    """测试基本位操作"""
    print("测试基本位操作...")
    
    # 创建与设置
    bm = Bitmap(16)
    assert len(bm) == 16
    assert not bm.any_set()
    
    # 设置位
    bm.set(0)
    bm.set(5)
    bm.set(15)
    assert bm[0] == True
    assert bm[5] == True
    assert bm[15] == True
    assert bm[1] == False
    
    # 清除位
    bm.clear(5)
    assert bm[5] == False
    
    # 翻转位
    bm.flip(0)
    assert bm[0] == False
    bm.flip(0)
    assert bm[0] == True
    
    # 通过索引设置
    bm[7] = True
    assert bm[7] == True
    
    print("  ✓ 基本操作测试通过")


def test_range_operations():
    """测试范围操作"""
    print("测试范围操作...")
    
    bm = Bitmap(32)
    
    # 设置范围
    bm.set_range(5, 15)
    for i in range(5, 15):
        assert bm[i] == True
    assert bm[4] == False
    assert bm[15] == False
    
    # 清除范围
    bm.set_range(5, 15, False)
    for i in range(5, 15):
        assert bm[i] == False
    
    # 翻转范围
    bm.set_range(0, 8)
    bm.flip_range(4, 12)
    for i in range(4):
        assert bm[i] == True
    for i in range(4, 8):
        assert bm[i] == False
    for i in range(8, 12):
        assert bm[i] == True
    
    print("  ✓ 范围操作测试通过")


def test_statistics():
    """测试统计功能"""
    print("测试统计功能...")
    
    bm = Bitmap(64)
    
    # 计数
    bm.set(0)
    bm.set(10)
    bm.set(20)
    bm.set(30)
    assert bm.count_set() == 4
    assert bm.count_clear() == 60
    
    # 查找
    assert bm.find_first_set() == 0
    assert bm.find_first_set(1) == 10
    assert bm.find_next_set(0) == 10
    assert bm.find_first_clear() == 1
    
    # 查找第n个设置位
    assert bm.find_nth_set(0) == 0
    assert bm.find_nth_set(1) == 10
    assert bm.find_nth_set(2) == 20
    assert bm.find_nth_set(3) == 30
    assert bm.find_nth_set(4) == -1
    
    # 空位图测试
    bm2 = Bitmap(10)
    assert bm2.find_first_set() == -1
    assert bm2.count_set() == 0
    
    print("  ✓ 统计功能测试通过")


def test_any_all_none():
    """测试any/all/none方法"""
    print("测试any/all/none...")
    
    # 全0
    bm = Bitmap(16)
    assert not bm.any_set()
    assert not bm.all_set()
    assert bm.none_set()
    
    # 部分设置
    bm.set(5)
    assert bm.any_set()
    assert not bm.all_set()
    assert not bm.none_set()
    
    # 全部设置
    bm.set_range(0, 16)
    assert bm.any_set()
    assert bm.all_set()
    assert not bm.none_set()
    
    print("  ✓ any/all/none测试通过")


def test_bitmap_operations():
    """测试位图运算"""
    print("测试位图运算...")
    
    bm1 = bitmap_from_string("10101010")  # 0xAA
    bm2 = bitmap_from_string("11001100")  # 0xCC
    
    # AND
    result = bm1.and_(bm2)
    assert result.to_bit_string() == "10001000"
    
    # OR
    result = bm1.or_(bm2)
    assert result.to_bit_string() == "11101110"
    
    # XOR
    result = bm1.xor(bm2)
    assert result.to_bit_string() == "01100110"
    
    # NOT
    result = bm1.not_()
    assert result.to_bit_string() == "01010101"
    
    # 差集
    result = bm1.difference(bm2)
    assert result.to_bit_string() == "00100010"
    
    print("  ✓ 位图运算测试通过")


def test_operators():
    """测试运算符重载"""
    print("测试运算符重载...")
    
    bm1 = bitmap_from_string("10101010")
    bm2 = bitmap_from_string("11001100")
    
    # AND (&)
    result = bm1 & bm2
    assert result.to_bit_string() == "10001000"
    
    # OR (|)
    result = bm1 | bm2
    assert result.to_bit_string() == "11101110"
    
    # XOR (^)
    result = bm1 ^ bm2
    assert result.to_bit_string() == "01100110"
    
    # NOT (~)
    result = ~bm1
    assert result.to_bit_string() == "01010101"
    
    # 差集 (-)
    result = bm1 - bm2
    assert result.to_bit_string() == "00100010"
    
    print("  ✓ 运算符重载测试通过")


def test_inplace_operators():
    """测试原地运算符"""
    print("测试原地运算符...")
    
    bm1 = bitmap_from_string("10101010")
    bm2 = bitmap_from_string("11001100")
    
    # &=
    bm1 &= bm2
    assert bm1.to_bit_string() == "10001000"
    
    bm1 = bitmap_from_string("10101010")
    bm2 = bitmap_from_string("11001100")
    
    # |=
    bm1 |= bm2
    assert bm1.to_bit_string() == "11101110"
    
    bm1 = bitmap_from_string("10101010")
    bm2 = bitmap_from_string("11001100")
    
    # ^=
    bm1 ^= bm2
    assert bm1.to_bit_string() == "01100110"
    
    print("  ✓ 原地运算符测试通过")


def test_serialization():
    """测试序列化"""
    print("测试序列化...")
    
    bm = Bitmap(24)
    bm.set(0)
    bm.set(7)
    bm.set(15)
    bm.set(23)
    
    # to_bytes / from_bytes
    data = bm.to_bytes()
    bm2 = Bitmap.from_bytes(data, 24)
    assert bm.to_bit_string() == bm2.to_bit_string()
    
    # to_hex_string / from_hex_string
    hex_str = bm.to_hex_string()
    bm3 = Bitmap.from_hex_string(hex_str, 24)
    assert bm.to_bit_string() == bm3.to_bit_string()
    
    # to_int / from_int
    int_val = bm.to_int()
    bm4 = Bitmap.from_int(int_val, 24)
    assert bm.to_bit_string() == bm4.to_bit_string()
    
    # to_bit_string / from_bit_string
    bit_str = bm.to_bit_string()
    bm5 = Bitmap.from_bit_string(bit_str)
    assert bm.to_bit_string() == bm5.to_bit_string()
    
    # from_indices
    bm6 = Bitmap.from_indices([0, 7, 15, 23], 24)
    assert bm.to_bit_string() == bm6.to_bit_string()
    
    print("  ✓ 序列化测试通过")


def test_iterators():
    """测试迭代器"""
    print("测试迭代器...")
    
    bm = Bitmap(16)
    bm.set(1)
    bm.set(5)
    bm.set(10)
    
    # iter_set_bits
    set_bits = list(bm.iter_set_bits())
    assert set_bits == [1, 5, 10]
    
    # iter_clear_bits
    clear_bits = list(bm.iter_clear_bits())
    expected_clear = [i for i in range(16) if i not in [1, 5, 10]]
    assert clear_bits == expected_clear
    
    # to_list
    assert bm.to_list() == [1, 5, 10]
    
    # iter_runs
    bm2 = bitmap_from_string("11100011110000")
    runs = list(bm2.iter_runs())
    assert runs == [(0, 3, True), (3, 6, False), (6, 10, True), (10, 14, False)]
    
    print("  ✓ 迭代器测试通过")


def test_set_operations():
    """测试集合操作"""
    print("测试集合操作...")
    
    bm1 = bitmap_from_string("11110000")
    bm2 = bitmap_from_string("11001100")
    
    # intersect
    assert bm1.intersect(bm2) == True
    bm3 = bitmap_from_string("00001111")
    assert bm1.intersect(bm3) == False
    
    # is_subset
    bm4 = bitmap_from_string("11000000")
    assert bm4.is_subset(bm1) == True
    assert bm1.is_subset(bm4) == False
    
    # is_superset
    assert bm1.is_superset(bm4) == True
    
    print("  ✓ 集合操作测试通过")


def test_resize():
    """测试调整大小"""
    print("测试调整大小...")
    
    bm = Bitmap(16)
    bm.set_range(0, 16)
    
    # 扩展
    bm.resize(32)
    assert len(bm) == 32
    for i in range(16):
        assert bm[i] == True
    for i in range(16, 32):
        assert bm[i] == False
    
    # 收缩
    bm.resize(8)
    assert len(bm) == 8
    for i in range(8):
        assert bm[i] == True
    
    print("  ✓ 调整大小测试通过")


def test_copy():
    """测试复制"""
    print("测试复制...")
    
    bm = Bitmap(16)
    bm.set_range(0, 8)
    
    bm_copy = bm.copy()
    assert bm_copy.to_bit_string() == bm.to_bit_string()
    
    # 修改副本不影响原位图
    bm_copy.clear(0)
    assert bm[0] == True
    assert bm_copy[0] == False
    
    print("  ✓ 复制测试通过")


def test_leading_trailing_zeros():
    """测试前导零和后导零"""
    print("测试前导零和后导零...")
    
    bm = bitmap_from_string("00001010")
    assert bm.count_leading_zeros() == 4
    assert bm.count_trailing_zeros() == 1
    
    bm2 = bitmap_from_string("00000000")
    assert bm2.count_leading_zeros() == 8
    assert bm2.count_trailing_zeros() == 8
    
    bm3 = bitmap_from_string("11111111")
    assert bm3.count_leading_zeros() == 0
    assert bm3.count_trailing_zeros() == 0
    
    print("  ✓ 前导零和后导零测试通过")


def test_sparse_bitmap():
    """测试稀疏位图"""
    print("测试稀疏位图...")
    
    sbm = SparseBitmap(1000)
    
    # 基本操作
    assert len(sbm) == 1000
    assert sbm.count_set() == 0
    
    sbm.set(100)
    sbm.set(500)
    sbm.set(999)
    
    assert sbm[100] == True
    assert sbm[500] == True
    assert sbm[999] == True
    assert sbm[0] == False
    assert sbm.count_set() == 3
    
    # 翻转
    sbm.flip(100)
    assert sbm[100] == False
    assert sbm.count_set() == 2
    
    # 迭代
    set_bits = list(sbm.iter_set_bits())
    assert set_bits == [500, 999]
    
    # 复制
    sbm_copy = sbm.copy()
    assert sbm_copy.count_set() == 2
    
    # 与密集位图转换
    dense = sbm.to_bitmap()
    assert dense.count_set() == 2
    assert dense[500] == True
    assert dense[999] == True
    
    # 从密集位图转换
    dense2 = Bitmap(100)
    dense2.set(10)
    dense2.set(50)
    sbm2 = SparseBitmap.from_bitmap(dense2)
    assert sbm2.count_set() == 2
    assert sbm2[10] == True
    
    print("  ✓ 稀疏位图测试通过")


def test_convenience_functions():
    """测试便捷函数"""
    print("测试便捷函数...")
    
    # create_bitmap
    bm = create_bitmap(16, [0, 5, 10, 15])
    assert bm.count_set() == 4
    assert bm.to_list() == [0, 5, 10, 15]
    
    # bitmap_from_string
    bm = bitmap_from_string("10101010")
    assert bm.to_bit_string() == "10101010"
    
    # bitmap_union
    bm1 = bitmap_from_string("10101010")
    bm2 = bitmap_from_string("11001100")
    result = bitmap_union(bm1, bm2)
    assert result.to_bit_string() == "11101110"
    
    # bitmap_intersection
    result = bitmap_intersection(bm1, bm2)
    assert result.to_bit_string() == "10001000"
    
    # bitmap_difference
    result = bitmap_difference(bm1, bm2)
    assert result.to_bit_string() == "00100010"
    
    print("  ✓ 便捷函数测试通过")


def test_edge_cases():
    """测试边界情况"""
    print("测试边界情况...")
    
    # 空位图
    bm = Bitmap(0)
    assert len(bm) == 0
    assert bm.count_set() == 0
    assert bm.any_set() == False
    assert bm.all_set() == True
    assert bm.none_set() == True
    
    # 单位
    bm = Bitmap(1)
    assert bm[0] == False
    bm.set(0)
    assert bm[0] == True
    
    # 大位图
    bm = Bitmap(10000)
    bm.set(0)
    bm.set(9999)
    assert bm.count_set() == 2
    
    # 边界位操作
    bm = Bitmap(16)
    bm.set(15)  # 最后一位
    assert bm[15] == True
    
    print("  ✓ 边界情况测试通过")


def test_string_representation():
    """测试字符串表示"""
    print("测试字符串表示...")
    
    bm = bitmap_from_string("10101010")
    
    # __str__
    assert str(bm) == "Bitmap(10101010)"
    
    # __repr__
    assert "Bitmap" in repr(bm)
    assert "8" in repr(bm)
    
    print("  ✓ 字符串表示测试通过")


def test_comparison():
    """测试比较"""
    print("测试比较...")
    
    bm1 = bitmap_from_string("10101010")
    bm2 = bitmap_from_string("10101010")
    bm3 = bitmap_from_string("01010101")
    
    assert bm1 == bm2
    assert bm1 != bm3
    assert bm1 != "not a bitmap"
    
    print("  ✓ 比较测试通过")


def test_contains():
    """测试包含操作"""
    print("测试包含操作...")
    
    bm = Bitmap(16)
    bm.set(5)
    bm.set(10)
    
    assert 5 in bm
    assert 10 in bm
    assert 0 not in bm
    assert 15 not in bm
    
    print("  ✓ 包含操作测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("Bitmap Utils 测试套件")
    print("=" * 50)
    print()
    
    tests = [
        test_basic_operations,
        test_range_operations,
        test_statistics,
        test_any_all_none,
        test_bitmap_operations,
        test_operators,
        test_inplace_operators,
        test_serialization,
        test_iterators,
        test_set_operations,
        test_resize,
        test_copy,
        test_leading_trailing_zeros,
        test_sparse_bitmap,
        test_convenience_functions,
        test_edge_cases,
        test_string_representation,
        test_comparison,
        test_contains,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  ✗ {test.__name__} 失败: {e}")
            failed += 1
    
    print()
    print("=" * 50)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)