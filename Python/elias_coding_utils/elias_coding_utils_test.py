"""
Elias 编码工具测试模块

测试覆盖：
- Elias Gamma 编码/解码
- Elias Delta 编码/解码
- Elias Omega 编码/解码
- 序列编码/解码
- 字节格式转换
- 边界条件和异常处理
- 性能测试
"""

import unittest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # Gamma 编码
    elias_gamma_encode, elias_gamma_decode,
    elias_gamma_encode_sequence, elias_gamma_decode_sequence,
    # Delta 编码
    elias_delta_encode, elias_delta_decode,
    elias_delta_encode_sequence, elias_delta_decode_sequence,
    # Omega 编码
    elias_omega_encode, elias_omega_decode,
    elias_omega_encode_sequence, elias_omega_decode_sequence,
    # 工具类
    BitWriter, BitReader,
    compare_encodings, optimal_encode, get_encoding_stats,
    EliasEncoder, EliasDecoder
)


class TestBitWriterReader(unittest.TestCase):
    """测试位写入器和读取器"""
    
    def test_write_single_bits(self):
        """测试写入单个位"""
        writer = BitWriter()
        writer.write_bit(0)
        writer.write_bit(1)
        writer.write_bit(0)
        writer.write_bit(1)
        self.assertEqual(writer.to_bitstring(), "0101")
    
    def test_write_bits(self):
        """测试写入多个位"""
        writer = BitWriter()
        writer.write_bits("10110")
        self.assertEqual(writer.to_bitstring(), "10110")
    
    def test_to_bytes(self):
        """测试转换为字节"""
        writer = BitWriter()
        writer.write_bits("10110010")  # 刚好 8 位
        result = writer.to_bytes()
        # 无填充
        self.assertEqual(len(result), 1)
    
    def test_to_bytes_with_padding(self):
        """测试带填充的字节转换"""
        writer = BitWriter()
        writer.write_bits("10110")  # 5 位，需要 3 位填充
        result = writer.to_bytes()
        self.assertIsInstance(result, bytes)
    
    def test_reader_from_bitstring(self):
        """测试从二进制字符串读取"""
        reader = BitReader("10110")
        self.assertEqual(reader.read_bit(), 1)
        self.assertEqual(reader.read_bit(), 0)
        self.assertEqual(reader.read_bits(2), "11")
        self.assertEqual(reader.read_bit(), 0)
    
    def test_reader_from_bytes(self):
        """测试从字节读取"""
        writer = BitWriter()
        writer.write_bits("10110010")
        data = writer.to_bytes()
        
        reader = BitReader(data)
        self.assertEqual(reader.read_bits(8), "10110010")
    
    def test_invalid_bit_value(self):
        """测试无效的位值"""
        writer = BitWriter()
        with self.assertRaises(ValueError):
            writer.write_bit(2)
    
    def test_eof_error(self):
        """测试读取超出范围"""
        reader = BitReader("10")
        reader.read_bits(2)
        with self.assertRaises(EOFError):
            reader.read_bit()


class TestEliasGammaEncoding(unittest.TestCase):
    """测试 Elias Gamma 编码"""
    
    def test_encode_1(self):
        """测试编码 1"""
        self.assertEqual(elias_gamma_encode(1), "1")
    
    def test_encode_2(self):
        """测试编码 2"""
        self.assertEqual(elias_gamma_encode(2), "010")
    
    def test_encode_3(self):
        """测试编码 3"""
        self.assertEqual(elias_gamma_encode(3), "011")
    
    def test_encode_4(self):
        """测试编码 4"""
        self.assertEqual(elias_gamma_encode(4), "00100")
    
    def test_encode_5(self):
        """测试编码 5"""
        self.assertEqual(elias_gamma_encode(5), "00101")
    
    def test_encode_7(self):
        """测试编码 7"""
        self.assertEqual(elias_gamma_encode(7), "00111")
    
    def test_encode_8(self):
        """测试编码 8"""
        self.assertEqual(elias_gamma_encode(8), "0001000")
    
    def test_encode_15(self):
        """测试编码 15"""
        self.assertEqual(elias_gamma_encode(15), "0001111")
    
    def test_encode_16(self):
        """测试编码 16"""
        self.assertEqual(elias_gamma_encode(16), "000010000")
    
    def test_encode_large_number(self):
        """测试编码大数"""
        result = elias_gamma_encode(1000)
        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith('0' * 9))  # 1000 需要 10 位，所以 9 个前导零
    
    def test_decode_1(self):
        """测试解码 1"""
        self.assertEqual(elias_gamma_decode("1"), 1)
    
    def test_decode_2(self):
        """测试解码 2"""
        self.assertEqual(elias_gamma_decode("010"), 2)
    
    def test_decode_roundtrip(self):
        """测试编解码往返"""
        for n in range(1, 100):
            encoded = elias_gamma_encode(n)
            decoded = elias_gamma_decode(encoded)
            self.assertEqual(decoded, n, f"Gamma 往返失败: {n}")
    
    def test_encode_sequence(self):
        """测试序列编码"""
        numbers = [1, 2, 3, 5, 8, 13]
        encoded = elias_gamma_encode_sequence(numbers)
        
        # 验证可以解码回来
        decoded = elias_gamma_decode_sequence(encoded, len(numbers))
        self.assertEqual(decoded, numbers)
    
    def test_encode_as_bytes(self):
        """测试返回字节格式"""
        result = elias_gamma_encode(100, as_bytes=True)
        self.assertIsInstance(result, bytes)
        
        # 验证字节可以解码
        decoded = elias_gamma_decode(result)
        self.assertEqual(decoded, 100)
    
    def test_invalid_input_zero(self):
        """测试无效输入：0"""
        with self.assertRaises(ValueError):
            elias_gamma_encode(0)
    
    def test_invalid_input_negative(self):
        """测试无效输入：负数"""
        with self.assertRaises(ValueError):
            elias_gamma_encode(-5)


class TestEliasDeltaEncoding(unittest.TestCase):
    """测试 Elias Delta 编码"""
    
    def test_encode_1(self):
        """测试编码 1"""
        self.assertEqual(elias_delta_encode(1), "1")
    
    def test_encode_2(self):
        """测试编码 2"""
        self.assertEqual(elias_delta_encode(2), "0100")
    
    def test_encode_3(self):
        """测试编码 3"""
        self.assertEqual(elias_delta_encode(3), "0101")
    
    def test_encode_4(self):
        """测试编码 4"""
        self.assertEqual(elias_delta_encode(4), "01100")
    
    def test_encode_5(self):
        """测试编码 5"""
        self.assertEqual(elias_delta_encode(5), "01101")
    
    def test_encode_7(self):
        """测试编码 7"""
        self.assertEqual(elias_delta_encode(7), "01111")
    
    def test_encode_8(self):
        """测试编码 8"""
        self.assertEqual(elias_delta_encode(8), "00100000")
    
    def test_encode_16(self):
        """测试编码 16"""
        self.assertEqual(elias_delta_encode(16), "001010000")
    
    def test_decode_1(self):
        """测试解码 1"""
        self.assertEqual(elias_delta_decode("1"), 1)
    
    def test_decode_2(self):
        """测试解码 2"""
        self.assertEqual(elias_delta_decode("0100"), 2)
    
    def test_decode_roundtrip(self):
        """测试编解码往返"""
        for n in range(1, 100):
            encoded = elias_delta_encode(n)
            decoded = elias_delta_decode(encoded)
            self.assertEqual(decoded, n, f"Delta 往返失败: {n}")
    
    def test_decode_roundtrip_large(self):
        """测试大数编解码往返"""
        test_numbers = [100, 1000, 10000, 65535, 100000, 1000000]
        for n in test_numbers:
            encoded = elias_delta_encode(n)
            decoded = elias_delta_decode(encoded)
            self.assertEqual(decoded, n, f"Delta 大数往返失败: {n}")
    
    def test_encode_sequence(self):
        """测试序列编码"""
        numbers = [1, 2, 3, 5, 8, 13, 21, 34]
        encoded = elias_delta_encode_sequence(numbers)
        decoded = elias_delta_decode_sequence(encoded, len(numbers))
        self.assertEqual(decoded, numbers)
    
    def test_encode_as_bytes(self):
        """测试返回字节格式"""
        result = elias_delta_encode(500, as_bytes=True)
        self.assertIsInstance(result, bytes)
        decoded = elias_delta_decode(result)
        self.assertEqual(decoded, 500)
    
    def test_invalid_input(self):
        """测试无效输入"""
        with self.assertRaises(ValueError):
            elias_delta_encode(0)
        with self.assertRaises(ValueError):
            elias_delta_encode(-1)


class TestEliasOmegaEncoding(unittest.TestCase):
    """测试 Elias Omega 编码"""
    
    def test_encode_1(self):
        """测试编码 1"""
        self.assertEqual(elias_omega_encode(1), "0")
    
    def test_encode_2(self):
        """测试编码 2"""
        self.assertEqual(elias_omega_encode(2), "100")
    
    def test_encode_3(self):
        """测试编码 3"""
        self.assertEqual(elias_omega_encode(3), "110")
    
    def test_encode_4(self):
        """测试编码 4"""
        self.assertEqual(elias_omega_encode(4), "111000")
    
    def test_encode_7(self):
        """测试编码 7"""
        self.assertEqual(elias_omega_encode(7), "111110")
    
    def test_encode_8(self):
        """测试编码 8"""
        self.assertEqual(elias_omega_encode(8), "1110010000")
    
    def test_encode_15(self):
        """测试编码 15"""
        self.assertEqual(elias_omega_encode(15), "1110011110")
    
    def test_encode_16(self):
        """测试编码 16"""
        self.assertEqual(elias_omega_encode(16), "11101100000")
    
    def test_decode_1(self):
        """测试解码 1"""
        self.assertEqual(elias_omega_decode("0"), 1)
    
    def test_decode_2(self):
        """测试解码 2"""
        self.assertEqual(elias_omega_decode("100"), 2)
    
    def test_decode_roundtrip(self):
        """测试编解码往返"""
        for n in range(1, 100):
            encoded = elias_omega_encode(n)
            decoded = elias_omega_decode(encoded)
            self.assertEqual(decoded, n, f"Omega 往返失败: {n}")
    
    def test_decode_roundtrip_large(self):
        """测试大数编解码往返"""
        test_numbers = [100, 1000, 10000, 65535, 100000]
        for n in test_numbers:
            encoded = elias_omega_encode(n)
            decoded = elias_omega_decode(encoded)
            self.assertEqual(decoded, n, f"Omega 大数往返失败: {n}")
    
    def test_encode_sequence(self):
        """测试序列编码"""
        numbers = [1, 2, 3, 5, 8, 13]
        encoded = elias_omega_encode_sequence(numbers)
        decoded = elias_omega_decode_sequence(encoded, len(numbers))
        self.assertEqual(decoded, numbers)
    
    def test_encode_as_bytes(self):
        """测试返回字节格式"""
        result = elias_omega_encode(200, as_bytes=True)
        self.assertIsInstance(result, bytes)
        decoded = elias_omega_decode(result)
        self.assertEqual(decoded, 200)
    
    def test_invalid_input(self):
        """测试无效输入"""
        with self.assertRaises(ValueError):
            elias_omega_encode(0)
        with self.assertRaises(ValueError):
            elias_omega_encode(-1)


class TestComparisonFunctions(unittest.TestCase):
    """测试比较和统计函数"""
    
    def test_compare_encodings_small(self):
        """测试小编数的编码比较"""
        result = compare_encodings(5)
        self.assertEqual(result['number'], 5)
        self.assertIn('gamma', result)
        self.assertIn('delta', result)
        self.assertIn('omega', result)
        self.assertIn('recommendation', result)
    
    def test_compare_encodings_large(self):
        """测试大数的编码比较"""
        result = compare_encodings(10000)
        self.assertEqual(result['number'], 10000)
        # 对于大数，delta 和 omega 通常比 gamma 更短
        self.assertIsInstance(result['recommendation'], str)
    
    def test_optimal_encode(self):
        """测试最优编码选择"""
        result, method = optimal_encode(5)
        self.assertIn(method, ('gamma', 'delta', 'omega'))
        
        # 验证可以解码
        if method == 'gamma':
            decoded = elias_gamma_decode(result)
        elif method == 'delta':
            decoded = elias_delta_decode(result)
        else:
            decoded = elias_omega_decode(result)
        self.assertEqual(decoded, 5)
    
    def test_get_encoding_stats(self):
        """测试编码统计"""
        numbers = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
        stats = get_encoding_stats(numbers)
        
        self.assertEqual(stats['count'], 10)
        self.assertEqual(stats['min'], 1)
        self.assertEqual(stats['max'], 89)
        self.assertGreater(stats['average'], 0)
        self.assertIn('best_method', stats)


class TestEliasEncoderDecoder(unittest.TestCase):
    """测试流式编码器和解码器"""
    
    def test_gamma_encoder_decoder(self):
        """测试 Gamma 流式编解码"""
        encoder = EliasEncoder(method='gamma')
        encoder.encode(1).encode(5).encode(10)
        
        result = encoder.get_result()
        self.assertEqual(encoder.count, 3)
        
        decoder = EliasDecoder(result, method='gamma')
        numbers = decoder.decode_all()
        self.assertEqual(numbers, [1, 5, 10])
    
    def test_delta_encoder_decoder(self):
        """测试 Delta 流式编解码"""
        encoder = EliasEncoder(method='delta')
        numbers = [1, 10, 100, 1000]
        encoder.encode_all(numbers)
        
        result = encoder.get_result()
        self.assertEqual(encoder.count, 4)
        
        decoder = EliasDecoder(result, method='delta')
        decoded = decoder.decode_all()
        self.assertEqual(decoded, numbers)
    
    def test_omega_encoder_decoder(self):
        """测试 Omega 流式编解码"""
        encoder = EliasEncoder(method='omega')
        numbers = [1, 2, 4, 8, 16, 32]
        encoder.encode_all(numbers)
        
        result = encoder.get_result(as_bytes=True)
        self.assertEqual(encoder.count, 6)
        
        decoder = EliasDecoder(result, method='omega')
        decoded = decoder.decode_all()
        self.assertEqual(decoded, numbers)
    
    def test_decode_count(self):
        """测试指定数量解码"""
        encoder = EliasEncoder(method='gamma')
        encoder.encode_all([1, 2, 3, 4, 5])
        
        decoder = EliasDecoder(encoder.get_result(), method='gamma')
        numbers = decoder.decode_count(3)
        self.assertEqual(numbers, [1, 2, 3])
        self.assertEqual(decoder.decoded_count, 3)
        self.assertTrue(decoder.has_more)
    
    def test_invalid_method(self):
        """测试无效的编码方法"""
        with self.assertRaises(ValueError):
            EliasEncoder(method='invalid')
        with self.assertRaises(ValueError):
            EliasDecoder("1", method='invalid')


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_empty_sequence(self):
        """测试空序列"""
        gamma_encoded = elias_gamma_encode_sequence([])
        self.assertEqual(gamma_encoded, "")
        
        delta_encoded = elias_delta_encode_sequence([])
        self.assertEqual(delta_encoded, "")
        
        omega_encoded = elias_omega_encode_sequence([])
        self.assertEqual(omega_encoded, "")
    
    def test_single_number_sequence(self):
        """测试单个数字的序列"""
        numbers = [42]
        
        gamma_encoded = elias_gamma_encode_sequence(numbers)
        gamma_decoded = elias_gamma_decode_sequence(gamma_encoded, 1)
        self.assertEqual(gamma_decoded, numbers)
        
        delta_encoded = elias_delta_encode_sequence(numbers)
        delta_decoded = elias_delta_decode_sequence(delta_encoded, 1)
        self.assertEqual(delta_decoded, numbers)
        
        omega_encoded = elias_omega_encode_sequence(numbers)
        omega_decoded = elias_omega_decode_sequence(omega_encoded, 1)
        self.assertEqual(omega_decoded, numbers)
    
    def test_large_numbers(self):
        """测试大数"""
        large = 2**30 - 1  # 约 10 亿
        
        for n in [1000000, 10000000, large]:
            gamma_encoded = elias_gamma_encode(n)
            self.assertEqual(elias_gamma_decode(gamma_encoded), n)
            
            delta_encoded = elias_delta_encode(n)
            self.assertEqual(elias_delta_decode(delta_encoded), n)
            
            omega_encoded = elias_omega_encode(n)
            self.assertEqual(elias_omega_decode(omega_encoded), n)
    
    def test_consecutive_powers_of_two(self):
        """测试连续的 2 的幂"""
        powers = [2**i for i in range(10)]
        
        for encode_func, decode_func in [
            (elias_gamma_encode, elias_gamma_decode),
            (elias_delta_encode, elias_delta_decode),
            (elias_omega_encode, elias_omega_decode),
        ]:
            for n in powers:
                encoded = encode_func(n)
                decoded = decode_func(encoded)
                self.assertEqual(decoded, n, f"Failed for {n} with {encode_func.__name__}")
    
    def test_fibonacci_sequence(self):
        """测试斐波那契序列"""
        fibs = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
        
        gamma_encoded = elias_gamma_encode_sequence(fibs)
        gamma_decoded = elias_gamma_decode_sequence(gamma_encoded, len(fibs))
        self.assertEqual(gamma_decoded, fibs)
        
        delta_encoded = elias_delta_encode_sequence(fibs)
        delta_decoded = elias_delta_decode_sequence(delta_encoded, len(fibs))
        self.assertEqual(delta_decoded, fibs)
        
        omega_encoded = elias_omega_encode_sequence(fibs)
        omega_decoded = elias_omega_decode_sequence(omega_encoded, len(fibs))
        self.assertEqual(omega_decoded, fibs)


class TestPerformance(unittest.TestCase):
    """性能测试"""
    
    def test_large_sequence(self):
        """测试大序列编解码"""
        # 生成测试数据
        import random
        random.seed(42)
        numbers = [random.randint(1, 10000) for _ in range(1000)]
        
        # Gamma
        gamma_encoded = elias_gamma_encode_sequence(numbers)
        gamma_decoded = elias_gamma_decode_sequence(gamma_encoded, len(numbers))
        self.assertEqual(gamma_decoded, numbers)
        
        # Delta
        delta_encoded = elias_delta_encode_sequence(numbers)
        delta_decoded = elias_delta_decode_sequence(delta_encoded, len(numbers))
        self.assertEqual(delta_decoded, numbers)
        
        # Omega
        omega_encoded = elias_omega_encode_sequence(numbers)
        omega_decoded = elias_omega_decode_sequence(omega_encoded, len(numbers))
        self.assertEqual(omega_decoded, numbers)
        
        # 比较长度
        self.assertGreater(len(gamma_encoded), 0)
        self.assertGreater(len(delta_encoded), 0)
        self.assertGreater(len(omega_encoded), 0)
    
    def test_compression_efficiency(self):
        """测试压缩效率"""
        # 对于小数字序列，比较不同编码的效率
        small_numbers = list(range(1, 101))
        large_numbers = list(range(1000, 1100))  # 100 个数字
        
        small_stats = get_encoding_stats(small_numbers)
        large_stats = get_encoding_stats(large_numbers)
        
        # 验证统计信息合理
        self.assertEqual(small_stats['count'], 100)
        self.assertEqual(large_stats['count'], 100)
        
        # 打印统计信息（用于观察）
        # print(f"\n小数字序列统计: {small_stats}")
        # print(f"大数字序列统计: {large_stats}")


if __name__ == '__main__':
    unittest.main(verbosity=2)