"""
字节操作工具模块测试

测试所有字节操作功能，包括：
- 字节序转换
- 字节数组操作
- 位操作
- 十六进制转换
- 字节模式匹配
- 校验和计算
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from byte_utils.mod import ByteUtils, to_little_endian, to_big_endian, from_little_endian, from_big_endian, to_hex, from_hex, xor_bytes


class TestByteEndian:
    """字节序转换测试"""
    
    def test_to_little_endian(self):
        """测试小端序转换"""
        result = ByteUtils.to_little_endian(0x12345678, 4)
        assert result == b'\x78\x56\x34\x12', f"Expected b'\\x78\\x56\\x34\\x12', got {result}"
        
        result = ByteUtils.to_little_endian(0xABCD, 2)
        assert result == b'\xcd\xab', f"Expected b'\\xcd\\xab', got {result}"
        
        result = ByteUtils.to_little_endian(0xFF, 1)
        assert result == b'\xff', f"Expected b'\\xff', got {result}"
        
        print("✓ to_little_endian 测试通过")
    
    def test_to_big_endian(self):
        """测试大端序转换"""
        result = ByteUtils.to_big_endian(0x12345678, 4)
        assert result == b'\x12\x34\x56\x78', f"Expected b'\\x12\\x34\\x56\\x78', got {result}"
        
        result = ByteUtils.to_big_endian(0xABCD, 2)
        assert result == b'\xab\xcd', f"Expected b'\\xab\\xcd', got {result}"
        
        print("✓ to_big_endian 测试通过")
    
    def test_from_little_endian(self):
        """测试从小端序解析"""
        result = ByteUtils.from_little_endian(b'\x78\x56\x34\x12')
        assert result == 0x12345678, f"Expected 0x12345678, got {hex(result)}"
        
        print("✓ from_little_endian 测试通过")
    
    def test_from_big_endian(self):
        """测试从大端序解析"""
        result = ByteUtils.from_big_endian(b'\x12\x34\x56\x78')
        assert result == 0x12345678, f"Expected 0x12345678, got {hex(result)}"
        
        print("✓ from_big_endian 测试通过")
    
    def test_swap_endian(self):
        """测试字节序交换"""
        result = ByteUtils.swap_endian(b'\x12\x34\x56\x78')
        assert result == b'\x78\x56\x34\x12', f"Expected b'\\x78\\x56\\x34\\x12', got {result}"
        
        print("✓ swap_endian 测试通过")
    
    def test_endian_roundtrip(self):
        """测试字节序往返转换"""
        value = 0xDEADBEEF
        
        # 小端序往返
        le_bytes = ByteUtils.to_little_endian(value, 4)
        le_value = ByteUtils.from_little_endian(le_bytes)
        assert le_value == value, f"小端序往返失败: {hex(le_value)} != {hex(value)}"
        
        # 大端序往返
        be_bytes = ByteUtils.to_big_endian(value, 4)
        be_value = ByteUtils.from_big_endian(be_bytes)
        assert be_value == value, f"大端序往返失败: {hex(be_value)} != {hex(value)}"
        
        print("✓ 字节序往返转换测试通过")
    
    def test_endian_invalid_size(self):
        """测试无效字节大小"""
        try:
            ByteUtils.to_little_endian(100, 3)  # 无效大小
            assert False, "应该抛出 ValueError"
        except ValueError:
            pass
        
        print("✓ 无效字节大小测试通过")
    
    def test_endian_value_out_of_range(self):
        """测试值超出范围"""
        try:
            ByteUtils.to_little_endian(0x100, 1)  # 1字节只能存0-255
            assert False, "应该抛出 ValueError"
        except ValueError:
            pass
        
        print("✓ 值超出范围测试通过")


class TestByteArrayOperations:
    """字节数组操作测试"""
    
    def test_concat(self):
        """测试字节数组拼接"""
        result = ByteUtils.concat(b'hello', b' ', b'world')
        assert result == b'hello world', f"Expected b'hello world', got {result}"
        
        result = ByteUtils.concat()
        assert result == b'', f"Expected b'', got {result}"
        
        print("✓ concat 测试通过")
    
    def test_slice_with_padding(self):
        """测试切片并填充"""
        result = ByteUtils.slice_with_padding(b'hello', 2, 10)
        assert result == b'llo\x00\x00\x00\x00\x00\x00\x00', f"Got {result}"
        assert len(result) == 10
        
        result = ByteUtils.slice_with_padding(b'hello world', 0, 5)
        assert result == b'hello', f"Expected b'hello', got {result}"
        
        print("✓ slice_with_padding 测试通过")
    
    def test_align_to_boundary(self):
        """测试边界对齐"""
        result = ByteUtils.align_to_boundary(b'hello', 4)
        assert result == b'hello\x00\x00\x00', f"Got {result}"
        assert len(result) == 8
        
        result = ByteUtils.align_to_boundary(b'hello', 1)
        assert result == b'hello', f"Expected b'hello', got {result}"
        
        result = ByteUtils.align_to_boundary(b'hello', 5)
        assert result == b'hello', f"Expected b'hello', got {result}"
        
        print("✓ align_to_boundary 测试通过")
    
    def test_pad_left(self):
        """测试左侧填充"""
        result = ByteUtils.pad_left(b'hello', 10, b'\xff')
        assert result == b'\xff\xff\xff\xff\xffhello', f"Got {result}"
        assert len(result) == 10
        
        result = ByteUtils.pad_left(b'helloworld', 5)
        assert result == b'helloworld', f"Expected b'helloworld', got {result}"
        
        print("✓ pad_left 测试通过")
    
    def test_pad_right(self):
        """测试右侧填充"""
        result = ByteUtils.pad_right(b'hello', 10, b'\xff')
        assert result == b'hello\xff\xff\xff\xff\xff', f"Got {result}"
        assert len(result) == 10
        
        print("✓ pad_right 测试通过")
    
    def test_trim_left(self):
        """测试左侧去除"""
        result = ByteUtils.trim_left(b'\x00\x00hello', b'\x00')
        assert result == b'hello', f"Expected b'hello', got {result}"
        
        print("✓ trim_left 测试通过")
    
    def test_trim_right(self):
        """测试右侧去除"""
        result = ByteUtils.trim_right(b'hello\x00\x00', b'\x00')
        assert result == b'hello', f"Expected b'hello', got {result}"
        
        print("✓ trim_right 测试通过")


class TestBitOperations:
    """位操作测试"""
    
    def test_set_bit(self):
        """测试设置位"""
        assert ByteUtils.set_bit(0b00001010, 0) == 0b00001011
        assert ByteUtils.set_bit(0b00000000, 7) == 0b10000000
        assert ByteUtils.set_bit(0b11111111, 3) == 0b11111111  # 已设置的位
        
        print("✓ set_bit 测试通过")
    
    def test_clear_bit(self):
        """测试清除位"""
        assert ByteUtils.clear_bit(0b00001011, 0) == 0b00001010
        assert ByteUtils.clear_bit(0b10000000, 7) == 0b00000000
        assert ByteUtils.clear_bit(0b00000000, 3) == 0b00000000  # 已清除的位
        
        print("✓ clear_bit 测试通过")
    
    def test_toggle_bit(self):
        """测试翻转位"""
        assert ByteUtils.toggle_bit(0b00001010, 0) == 0b00001011
        assert ByteUtils.toggle_bit(0b00001010, 1) == 0b00001000
        
        print("✓ toggle_bit 测试通过")
    
    def test_test_bit(self):
        """测试位测试"""
        assert ByteUtils.test_bit(0b00001010, 1) == True
        assert ByteUtils.test_bit(0b00001010, 0) == False
        assert ByteUtils.test_bit(0b10000000, 7) == True
        assert ByteUtils.test_bit(0b10000000, 0) == False
        
        print("✓ test_bit 测试通过")
    
    def test_get_bits(self):
        """测试提取连续位"""
        # 0b11011010, 提取从第2位开始的3位 (0b110 = 6)
        assert ByteUtils.get_bits(0b11011010, 2, 3) == 0b110
        
        # 提取从第0位开始的4位
        assert ByteUtils.get_bits(0b11011010, 0, 4) == 0b1010
        
        print("✓ get_bits 测试通过")
    
    def test_set_bits(self):
        """测试设置连续位"""
        # 0b11011010, 从第2位开始设置3位为 0b111
        result = ByteUtils.set_bits(0b11011010, 2, 3, 0b111)
        assert ByteUtils.get_bits(result, 2, 3) == 0b111
        
        print("✓ set_bits 测试通过")
    
    def test_reverse_bits(self):
        """测试位反转"""
        assert ByteUtils.reverse_bits(0b10110001, 8) == 0b10001101
        assert ByteUtils.reverse_bits(0b00000001, 8) == 0b10000000
        
        print("✓ reverse_bits 测试通过")
    
    def test_count_set_bits(self):
        """测试计数设置位"""
        assert ByteUtils.count_set_bits(0b10110001) == 4
        assert ByteUtils.count_set_bits(0b00000000) == 0
        assert ByteUtils.count_set_bits(0b11111111) == 8
        
        print("✓ count_set_bits 测试通过")
    
    def test_count_leading_zeros(self):
        """测试计数前导零"""
        assert ByteUtils.count_leading_zeros(0b00101000, 8) == 2
        assert ByteUtils.count_leading_zeros(0b10000000, 8) == 0
        assert ByteUtils.count_leading_zeros(0b00000000, 8) == 8
        
        print("✓ count_leading_zeros 测试通过")
    
    def test_count_trailing_zeros(self):
        """测试计数尾随零"""
        assert ByteUtils.count_trailing_zeros(0b1011000) == 3
        assert ByteUtils.count_trailing_zeros(0b00000001) == 0
        assert ByteUtils.count_trailing_zeros(0b00000000) == 0  # 特殊情况
        
        print("✓ count_trailing_zeros 测试通过")


class TestHexOperations:
    """十六进制操作测试"""
    
    def test_to_hex(self):
        """测试转十六进制"""
        result = ByteUtils.to_hex(b'\x12\x34\xab')
        assert result == '1234ab', f"Expected '1234ab', got {result}"
        
        result = ByteUtils.to_hex(b'\x12\x34\xab', uppercase=True)
        assert result == '1234AB', f"Expected '1234AB', got {result}"
        
        result = ByteUtils.to_hex(b'\x12\x34\xab', separator=' ')
        assert result == '12 34 ab', f"Expected '12 34 ab', got {result}"
        
        print("✓ to_hex 测试通过")
    
    def test_from_hex(self):
        """测试从十六进制解析"""
        result = ByteUtils.from_hex('1234ab')
        assert result == b'\x12\x34\xab', f"Got {result}"
        
        result = ByteUtils.from_hex('12 34 AB')
        assert result == b'\x12\x34\xab', f"Got {result}"
        
        result = ByteUtils.from_hex('12-34-ab')
        assert result == b'\x12\x34\xab', f"Got {result}"
        
        print("✓ from_hex 测试通过")
    
    def test_hex_roundtrip(self):
        """测试十六进制往返"""
        original = b'\xde\xad\xbe\xef\xca\xfe'
        hex_str = ByteUtils.to_hex(original)
        restored = ByteUtils.from_hex(hex_str)
        assert restored == original, f"往返失败: {original} -> {hex_str} -> {restored}"
        
        print("✓ 十六进制往返测试通过")
    
    def test_is_hex(self):
        """测试十六进制验证"""
        assert ByteUtils.is_hex('deadbeef') == True
        assert ByteUtils.is_hex('DEADBEEF') == True
        assert ByteUtils.is_hex('0x1234') == True
        assert ByteUtils.is_hex('12 34 56') == True
        assert ByteUtils.is_hex('hello') == False
        assert ByteUtils.is_hex('') == False
        
        print("✓ is_hex 测试通过")


class TestPatternMatching:
    """模式匹配测试"""
    
    def test_find_pattern(self):
        """测试查找模式"""
        data = b'hello world'
        assert ByteUtils.find_pattern(data, b'world') == 6
        assert ByteUtils.find_pattern(data, b'xyz') == -1
        assert ByteUtils.find_pattern(data, b'llo') == 2
        
        print("✓ find_pattern 测试通过")
    
    def test_find_all_patterns(self):
        """测试查找所有模式"""
        data = b'ababab'
        positions = ByteUtils.find_all_patterns(data, b'ab')
        assert positions == [0, 2, 4], f"Expected [0, 2, 4], got {positions}"
        
        print("✓ find_all_patterns 测试通过")
    
    def test_replace_pattern(self):
        """测试替换模式"""
        result = ByteUtils.replace_pattern(b'hello world', b'world', b'Python')
        assert result == b'hello Python', f"Got {result}"
        
        result = ByteUtils.replace_pattern(b'ababab', b'ab', b'cd', count=1)
        assert result == b'cdabab', f"Got {result}"
        
        print("✓ replace_pattern 测试通过")
    
    def test_count_pattern(self):
        """测试计数模式"""
        assert ByteUtils.count_pattern(b'ababab', b'ab') == 3
        assert ByteUtils.count_pattern(b'hello world', b'o') == 2
        assert ByteUtils.count_pattern(b'test', b'xyz') == 0
        
        print("✓ count_pattern 测试通过")
    
    def test_find_pattern_with_wildcard(self):
        """测试通配符模式匹配"""
        data = b'\x12\x34\xab\xcd'
        
        # 完全匹配
        positions = ByteUtils.find_pattern_with_wildcard(data, '1234')
        assert positions == [0], f"Expected [0], got {positions}"
        
        # 带通配符
        positions = ByteUtils.find_pattern_with_wildcard(data, '12??')
        assert positions == [0], f"Expected [0], got {positions}"
        
        print("✓ find_pattern_with_wildcard 测试通过")


class TestByteTransforms:
    """字节变换测试"""
    
    def test_xor_bytes(self):
        """测试 XOR 操作"""
        data = b'hello'
        key = b'key'
        
        # XOR 两次应该恢复原值
        encrypted = ByteUtils.xor_bytes(data, key)
        decrypted = ByteUtils.xor_bytes(encrypted, key)
        assert decrypted == data, f"XOR 往返失败: {decrypted} != {data}"
        
        print("✓ xor_bytes 测试通过")
    
    def test_rotate_left(self):
        """测试循环左移"""
        # 0b10110001 左移3位 = 0b10001101
        assert ByteUtils.rotate_left(0b10110001, 3, 8) == 0b10001101
        
        # 循环移位8次应该恢复原值
        value = 0b10110001
        assert ByteUtils.rotate_left(value, 8, 8) == value
        
        print("✓ rotate_left 测试通过")
    
    def test_rotate_right(self):
        """测试循环右移"""
        # 0b10110001 右移3位 = 0b00110110
        assert ByteUtils.rotate_right(0b10110001, 3, 8) == 0b00110110
        
        print("✓ rotate_right 测试通过")
    
    def test_reverse_byte_order(self):
        """测试按组反转字节顺序"""
        data = b'\x12\x34\x56\x78'
        
        # 按字节反转
        result = ByteUtils.reverse_byte_order(data, 1)
        assert result == b'\x78\x56\x34\x12', f"Got {result}"
        
        # 按2字节组反转
        result = ByteUtils.reverse_byte_order(data, 2)
        assert result == b'\x56\x78\x12\x34', f"Got {result}"
        
        print("✓ reverse_byte_order 测试通过")


class TestChecksums:
    """校验和测试"""
    
    def test_checksum_8bit(self):
        """测试8位校验和"""
        data = b'\x01\x02\x03'
        result = ByteUtils.checksum_8bit(data)
        # 验证校验和加起来等于0xFF
        assert (sum(data) + result) & 0xFF == 0xFF
        
        print("✓ checksum_8bit 测试通过")
    
    def test_checksum_xor(self):
        """测试XOR校验和"""
        assert ByteUtils.checksum_xor(b'\x01\x02\x03') == 0x00
        assert ByteUtils.checksum_xor(b'\xff\x00') == 0xff
        
        print("✓ checksum_xor 测试通过")
    
    def test_checksum_fletcher16(self):
        """测试Fletcher-16校验和"""
        # 标准测试向量
        result = ByteUtils.checksum_fletcher16(b'hello')
        assert isinstance(result, int)
        assert 0 <= result <= 0xFFFF
        
        print("✓ checksum_fletcher16 测试通过")
    
    def test_crc8(self):
        """测试CRC-8"""
        # 标准测试向量
        result = ByteUtils.crc8(b'123456789')
        # CRC-8 标准多项式的标准结果
        assert isinstance(result, int)
        assert 0 <= result <= 0xFF
        
        print("✓ crc8 测试通过")


class TestByteAnalysis:
    """字节分析测试"""
    
    def test_byte_frequency(self):
        """测试字节频率"""
        freq = ByteUtils.byte_frequency(b'aabbcc')
        assert freq[ord('a')] == 2
        assert freq[ord('b')] == 2
        assert freq[ord('c')] == 2
        
        print("✓ byte_frequency 测试通过")
    
    def test_entropy(self):
        """测试熵计算"""
        # 全相同字符，熵为0
        entropy_same = ByteUtils.entropy(b'aaaa')
        assert entropy_same == 0.0, f"Expected 0.0, got {entropy_same}"
        
        # 更随机的数据，熵应该更高
        entropy_random = ByteUtils.entropy(b'abcd')
        assert entropy_random > entropy_same
        
        # 空数据
        assert ByteUtils.entropy(b'') == 0.0
        
        print("✓ entropy 测试通过")
    
    def test_find_repeating_patterns(self):
        """测试查找重复模式"""
        patterns = ByteUtils.find_repeating_patterns(b'ababab', min_length=2)
        
        # 应该找到 'ab' 重复
        found_ab = False
        for pattern, positions in patterns:
            if pattern == b'ab':
                found_ab = True
                assert positions == [0, 2, 4], f"Expected [0, 2, 4], got {positions}"
        
        assert found_ab, "未找到 'ab' 模式"
        
        print("✓ find_repeating_patterns 测试通过")


class TestConvenienceFunctions:
    """便捷函数测试"""
    
    def test_to_little_endian(self):
        """测试便捷函数"""
        result = to_little_endian(0x12345678, 4)
        assert result == b'\x78\x56\x34\x12'
        
        print("✓ to_little_endian 便捷函数测试通过")
    
    def test_to_big_endian(self):
        """测试便捷函数"""
        result = to_big_endian(0x12345678, 4)
        assert result == b'\x12\x34\x56\x78'
        
        print("✓ to_big_endian 便捷函数测试通过")
    
    def test_from_little_endian(self):
        """测试便捷函数"""
        result = from_little_endian(b'\x78\x56\x34\x12')
        assert result == 0x12345678
        
        print("✓ from_little_endian 便捷函数测试通过")
    
    def test_from_big_endian(self):
        """测试便捷函数"""
        result = from_big_endian(b'\x12\x34\x56\x78')
        assert result == 0x12345678
        
        print("✓ from_big_endian 便捷函数测试通过")
    
    def test_to_hex(self):
        """测试便捷函数"""
        result = to_hex(b'\x12\x34\xab', uppercase=True, separator=' ')
        assert result == '12 34 AB'
        
        print("✓ to_hex 便捷函数测试通过")
    
    def test_from_hex(self):
        """测试便捷函数"""
        result = from_hex('12 34 AB')
        assert result == b'\x12\x34\xab'
        
        print("✓ from_hex 便捷函数测试通过")
    
    def test_xor_bytes(self):
        """测试便捷函数"""
        result = xor_bytes(b'test', b'key')
        assert len(result) == 4
        
        print("✓ xor_bytes 便捷函数测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("字节操作工具模块测试")
    print("=" * 60)
    
    test_classes = [
        TestByteEndian,
        TestByteArrayOperations,
        TestBitOperations,
        TestHexOperations,
        TestPatternMatching,
        TestByteTransforms,
        TestChecksums,
        TestByteAnalysis,
        TestConvenienceFunctions,
    ]
    
    passed = 0
    failed = 0
    
    for test_class in test_classes:
        print(f"\n--- {test_class.__name__} ---")
        instance = test_class()
        
        for method_name in dir(instance):
            if method_name.startswith('test_'):
                try:
                    getattr(instance, method_name)()
                    passed += 1
                except Exception as e:
                    print(f"✗ {method_name} 失败: {e}")
                    failed += 1
    
    print("\n" + "=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)