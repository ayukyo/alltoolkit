"""
Bitstream Utils 测试套件

测试位流读写、变长编码、位操作等功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bitstream_utils.mod import (
    BitReader, BitWriter, BitArray,
    count_bits, count_set_bits, reverse_bits,
    rotate_left, rotate_right, get_bit, set_bit, clear_bit, toggle_bit,
    create_bitmask, extract_bits, insert_bits, parity,
    gray_encode, gray_decode,
    encode_varint, decode_varint,
    encode_leb128_signed, decode_leb128_signed
)


def test_bit_reader_basic():
    """测试BitReader基本功能"""
    print("测试 BitReader 基本功能...")
    
    # 测试读取单个位
    data = bytes([0b10101010, 0b11001100])
    reader = BitReader(data)
    
    bits = [reader.read_bit() for _ in range(16)]
    expected = [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0]
    assert bits == expected, f"位读取错误: {bits} != {expected}"
    print("  ✓ 单位读取正确")
    
    # 测试读取多位
    reader = BitReader(bytes([0b11110000, 0b10101010]))
    value = reader.read_bits(4)
    assert value == 0b1111, f"多位读取错误: {value} != 15"
    print("  ✓ 多位读取正确")
    
    # 测试读取字节
    reader = BitReader(bytes([0xAB, 0xCD, 0xEF]))
    b1 = reader.read_byte()
    b2 = reader.read_byte()
    b3 = reader.read_byte()
    assert (b1, b2, b3) == (0xAB, 0xCD, 0xEF), "字节读取错误"
    print("  ✓ 字节读取正确")
    
    # 测试读取布尔值
    reader = BitReader(bytes([0b10000000]))
    assert reader.read_bool() == True
    assert reader.read_bool() == False
    print("  ✓ 布尔值读取正确")
    
    print("✅ BitReader 基本功能测试通过")


def test_bit_writer_basic():
    """测试BitWriter基本功能"""
    print("测试 BitWriter 基本功能...")
    
    # 测试写入单个位
    writer = BitWriter()
    for bit in [1, 0, 1, 0, 1, 0, 1, 0]:
        writer.write_bit(bit)
    
    result = writer.get_bytes()
    assert result == bytes([0b10101010]), f"位写入错误: {result}"
    print("  ✓ 单位写入正确")
    
    # 测试写入多位
    writer = BitWriter()
    writer.write_bits(0xABCD, 16)
    result = writer.get_bytes()
    assert result == bytes([0xAB, 0xCD]), f"多位写入错误: {result}"
    print("  ✓ 多位写入正确")
    
    # 测试写入字节
    writer = BitWriter()
    writer.write_bytes(bytes([0x12, 0x34, 0x56]))
    result = writer.get_bytes()
    assert result == bytes([0x12, 0x34, 0x56]), "字节写入错误"
    print("  ✓ 字节写入正确")
    
    print("✅ BitWriter 基本功能测试通过")


def test_read_write_roundtrip():
    """测试读写往返"""
    print("测试读写往返...")
    
    # 测试各种整数类型
    test_values = [
        (0, 8),
        (255, 8),
        (12345, 16),
        (65535, 16),
        (123456789, 32),
        (0xFFFFFFFF, 32),
    ]
    
    writer = BitWriter()
    for value, bits in test_values:
        writer.write_bits(value, bits)
    
    data = writer.get_bytes()
    reader = BitReader(data)
    
    for value, bits in test_values:
        read_value = reader.read_bits(bits)
        assert read_value == value, f"往返错误: {read_value} != {value}"
    
    print("  ✓ 整数往返正确")
    
    # 测试大端序/小端序
    writer = BitWriter()
    writer.write_uint16_be(0x1234)
    writer.write_uint16_le(0x1234)
    writer.write_uint32_be(0x12345678)
    writer.write_uint32_le(0x12345678)
    
    data = writer.get_bytes()
    reader = BitReader(data)
    
    assert reader.read_uint16_be() == 0x1234
    assert reader.read_uint16_le() == 0x1234
    assert reader.read_uint32_be() == 0x12345678
    assert reader.read_uint32_le() == 0x12345678
    print("  ✓ 大小端序正确")
    
    print("✅ 读写往返测试通过")


def test_varint():
    """测试变长整数编码"""
    print("测试变长整数编码...")
    
    test_values = [0, 1, 127, 128, 255, 256, 16383, 16384, 65535, 65536, 
                   1000000, 100000000, 2**63 - 1]
    
    for value in test_values:
        # 编码
        encoded = encode_varint(value)
        
        # 解码
        decoded, consumed = decode_varint(encoded)
        
        assert decoded == value, f"Varint编解码错误: {decoded} != {value}"
    
    print("  ✓ Varint编解码正确")
    
    # 测试使用BitReader/BitWriter
    writer = BitWriter()
    for value in [1, 300, 16384, 1000000]:
        writer.write_varint(value)
    
    data = writer.get_bytes()
    reader = BitReader(data)
    
    for value in [1, 300, 16384, 1000000]:
        decoded = reader.read_varint()
        assert decoded == value, f"Varint读写错误: {decoded} != {value}"
    
    print("  ✓ BitReader/BitWriter Varint正确")
    print("✅ 变长整数编码测试通过")


def test_leb128_signed():
    """测试LEB128有符号编码"""
    print("测试LEB128有符号编码...")
    
    test_values = [0, 1, -1, 127, -127, 128, -128, 32767, -32768,
                   100000, -100000, 2**30 - 1, -(2**30)]
    
    for value in test_values:
        encoded = encode_leb128_signed(value)
        decoded, _ = decode_leb128_signed(encoded)
        assert decoded == value, f"LEB128有符号编解码错误: {decoded} != {value}"
    
    print("  ✓ LEB128有符号编解码正确")
    print("✅ LEB128有符号编码测试通过")


def test_elias_codes():
    """测试Elias编码"""
    print("测试Elias编码...")
    
    # 测试Gamma编码
    writer = BitWriter()
    test_gamma = [1, 2, 3, 4, 5, 10, 100, 255]
    for value in test_gamma:
        writer.write_gamma(value)
    
    data = writer.get_bytes()
    reader = BitReader(data)
    
    for value in test_gamma:
        decoded = reader.read_gamma()
        assert decoded == value, f"Gamma编解码错误: {decoded} != {value}"
    
    print("  ✓ Gamma编码正确")
    
    # 测试Delta编码
    writer = BitWriter()
    test_delta = [1, 2, 3, 4, 5, 10, 100, 255, 1000]
    for value in test_delta:
        writer.write_delta(value)
    
    data = writer.get_bytes()
    reader = BitReader(data)
    
    for value in test_delta:
        decoded = reader.read_delta()
        assert decoded == value, f"Delta编解码错误: {decoded} != {value}"
    
    print("  ✓ Delta编码正确")
    print("✅ Elias编码测试通过")


def test_rice_coding():
    """测试Rice编码"""
    print("测试Rice编码...")
    
    k = 4  # Rice参数
    test_values = [0, 1, 15, 16, 17, 31, 32, 100, 255]
    
    writer = BitWriter()
    for value in test_values:
        writer.write_rice(value, k)
    
    data = writer.get_bytes()
    reader = BitReader(data)
    
    for value in test_values:
        decoded = reader.read_rice(k)
        assert decoded == value, f"Rice编解码错误: {decoded} != {value}"
    
    print("  ✓ Rice编码正确")
    print("✅ Rice编码测试通过")


def test_unary_coding():
    """测试一元编码"""
    print("测试一元编码...")
    
    test_values = [0, 1, 2, 5, 10, 15]
    
    writer = BitWriter()
    for value in test_values:
        writer.write_unary(value)
    
    data = writer.get_bytes()
    reader = BitReader(data)
    
    for value in test_values:
        decoded = reader.read_unary()
        assert decoded == value, f"一元编解码错误: {decoded} != {value}"
    
    print("  ✓ 一元编码正确")
    print("✅ 一元编码测试通过")


def test_bit_operations():
    """测试位操作函数"""
    print("测试位操作函数...")
    
    # count_bits
    assert count_bits(0) == 1
    assert count_bits(1) == 1
    assert count_bits(255) == 8
    assert count_bits(256) == 9
    print("  ✓ count_bits正确")
    
    # count_set_bits
    assert count_set_bits(0) == 0
    assert count_set_bits(255) == 8
    assert count_set_bits(0b10101010) == 4
    print("  ✓ count_set_bits正确")
    
    # reverse_bits
    assert reverse_bits(0b10100000, 8) == 0b00000101
    assert reverse_bits(0b11110000, 8) == 0b00001111
    print("  ✓ reverse_bits正确")
    
    # rotate_left / rotate_right
    assert rotate_left(0b11000000, 2, 8) == 0b00000011
    assert rotate_right(0b00000011, 2, 8) == 0b11000000
    print("  ✓ rotate_left/rotate_right正确")
    
    # get_bit / set_bit / clear_bit / toggle_bit
    assert get_bit(0b1010, 0) == 0
    assert get_bit(0b1010, 1) == 1
    assert set_bit(0, 3) == 0b1000
    assert clear_bit(0b1111, 2) == 0b1011
    assert toggle_bit(0b1010, 0) == 0b1011
    print("  ✓ 基本位操作正确")
    
    # create_bitmask / extract_bits / insert_bits
    assert create_bitmask(2, 5) == 0b11100
    assert extract_bits(0b11001100, 2, 4) == 0b0011
    assert insert_bits(0b11000011, 0b1010, 2, 4) == 0b11101011
    print("  ✓ 位掩码操作正确")
    
    # parity
    assert parity(0b1111) == 0  # 偶校验
    assert parity(0b1110) == 1  # 奇校验
    print("  ✓ parity正确")
    
    # gray_encode / gray_decode
    for i in range(256):
        gray = gray_encode(i)
        decoded = gray_decode(gray)
        assert decoded == i, f"格雷码错误: {i} -> {gray} -> {decoded}"
    print("  ✓ gray_encode/gray_decode正确")
    
    print("✅ 位操作函数测试通过")


def test_bit_array():
    """测试位数组"""
    print("测试BitArray...")
    
    # 基本操作
    arr = BitArray(16)
    assert len(arr) == 16
    assert arr.count_set() == 0
    
    arr[0] = 1
    arr[5] = 1
    arr[15] = 1
    assert arr[0] == 1
    assert arr[5] == 1
    assert arr[15] == 1
    assert arr.count_set() == 3
    print("  ✓ 基本操作正确")
    
    # set / clear / toggle
    arr.set(10)
    assert arr[10] == 1
    arr.clear(10)
    assert arr[10] == 0
    arr.toggle(10)
    assert arr[10] == 1
    print("  ✓ set/clear/toggle正确")
    
    # find_first_set / find_first_clear
    assert arr.find_first_set() == 0
    arr[0] = 0
    assert arr.find_first_set() == 5
    assert arr.find_first_clear() == 0
    print("  ✓ find_first_set/find_first_clear正确")
    
    # 初始化为全1
    arr2 = BitArray(16, initial=1)
    assert arr2.count_set() == 16
    print("  ✓ 初始化正确")
    
    # to_bytes / from_bytes
    arr3 = BitArray(16)
    arr3[0] = 1
    arr3[8] = 1
    data = arr3.to_bytes()
    
    arr4 = BitArray.from_bytes(data, 16)
    assert arr4[0] == 1
    assert arr4[8] == 1
    print("  ✓ 序列化/反序列化正确")
    
    print("✅ BitArray测试通过")


def test_bit_reader_seek():
    """测试BitReader定位"""
    print("测试BitReader定位...")
    
    data = bytes([0b10101010, 0b11001100, 0b11110000])
    reader = BitReader(data)
    
    # 读取一些数据
    assert reader.read_bits(4) == 0b1010
    assert reader.bit_position == 4
    
    # 跳转
    reader.seek(12)
    assert reader.read_bits(4) == 0b1100
    
    # 预览
    reader.seek(0)
    assert reader.peek_bits(8) == 0b10101010
    assert reader.read_bits(4) == 0b1010  # 位置未变
    
    # 对齐到字节
    reader.seek(10)
    reader.align_to_byte()
    assert reader.bit_position == 0
    assert reader.byte_position == 2
    
    print("✅ BitReader定位测试通过")


def test_complex_scenario():
    """测试复杂场景"""
    print("测试复杂场景...")
    
    # 模拟一个简单的压缩协议
    writer = BitWriter()
    
    # 写入头部
    writer.write_bits(1, 1)  # 版本
    writer.write_bits(3, 3)  # 类型
    writer.write_bool(True)   # 压缩标志
    writer.write_varint(150)  # 长度
    
    # 写入数据
    writer.write_bits(0xDEADBEEF, 32)
    writer.write_gamma(100)
    writer.write_delta(1000)
    writer.write_bytes(b"hello")
    
    # 对齐到字节
    writer.align_to_byte()
    
    # 读取
    data = writer.get_bytes()
    reader = BitReader(data)
    
    assert reader.read_bits(1) == 1
    assert reader.read_bits(3) == 3
    assert reader.read_bool() == True
    assert reader.read_varint() == 150
    assert reader.read_bits(32) == 0xDEADBEEF
    assert reader.read_gamma() == 100
    assert reader.read_delta() == 1000
    assert reader.read_bytes(5) == b"hello"
    
    print("✅ 复杂场景测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("Bitstream Utils 测试套件")
    print("=" * 50)
    
    test_bit_reader_basic()
    test_bit_writer_basic()
    test_read_write_roundtrip()
    test_varint()
    test_leb128_signed()
    test_elias_codes()
    test_rice_coding()
    test_unary_coding()
    test_bit_operations()
    test_bit_array()
    test_bit_reader_seek()
    test_complex_scenario()
    
    print("=" * 50)
    print("✅ 所有测试通过!")
    print("=" * 50)
    
    return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)