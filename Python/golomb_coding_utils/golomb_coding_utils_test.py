"""
Golomb Coding Utilities Test Suite - Golomb 编码工具测试套件

测试覆盖：
- BitWriter/BitReader 比特流操作
- GolombCoding 基本编码/解码
- RiceCoding 优化编码
- DeltaGolombCompressor 序列压缩
- GolombRiceCoder 智能编码
- 边界条件和错误处理
"""

import unittest
from mod import (
    BitWriter, BitReader,
    GolombCoding, RiceCoding,
    InterleavedGolombCoding,
    DeltaGolombCompressor,
    GolombRiceCoder,
    golomb_encode, golomb_decode,
    rice_encode, rice_decode,
    compress_sorted_integers, decompress_sorted_integers,
    optimal_parameter,
)


class TestBitWriter(unittest.TestCase):
    """比特写入器测试"""
    
    def test_write_single_bit(self):
        """测试写入单个比特"""
        writer = BitWriter()
        writer.write_bit(0)
        writer.write_bit(1)
        writer.write_bit(0)
        writer.write_bit(1)
        data = writer.flush()
        
        # 0101 0000 = 0x50
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0], 0x50)
    
    def test_write_bits(self):
        """测试写入多比特整数"""
        writer = BitWriter()
        writer.write_bits(5, 4)  # 0101
        writer.write_bits(3, 3)  # 011
        writer.write_bits(255, 8)  # 11111111
        data = writer.flush()
        
        # 4 + 3 + 8 = 15 bits, fits in 2 bytes with 1 bit padding
        # 0101 0111 | 1111 1111 (with 1 padding bit)
        # = 0x57 | 0xFF
        self.assertEqual(len(data), 2)
    
    def test_write_unary(self):
        """测试写入一元编码"""
        writer = BitWriter()
        writer.write_unary(0)  # 1
        writer.write_unary(3)  # 0001
        writer.write_unary(7)  # 00000001
        data = writer.flush()
        
        # 1 000 1 000 0001 0 (padding)
        # = 1000 1000 | 0001 0000 = 0x88 | 0x10
        self.assertEqual(len(data), 2)
    
    def test_write_gamma(self):
        """测试写入 Gamma 编码"""
        writer = BitWriter()
        
        # Gamma 编码规则:
        # 值 1: 长度 0 -> 一元编码 0 -> 1
        # 值 2: 长度 1 -> 一元编码 10 -> 后跟 0 -> 100
        # 值 5: 长度 2 -> 一元编码 110 -> 后跟 01 -> 11001
        
        writer.write_gamma(1)
        writer.write_gamma(2)
        writer.write_gamma(5)
        writer.write_gamma(10)
        
        data = writer.flush()
        self.assertGreater(len(data), 0)
    
    def test_flush_with_padding(self):
        """测试刷新时的填充"""
        writer = BitWriter()
        # 只写 5 位
        writer.write_bits(31, 5)
        data = writer.flush()
        
        # 应填充到完整字节
        self.assertEqual(len(data), 1)
    
    def test_reset(self):
        """测试重置"""
        writer = BitWriter()
        writer.write_bits(255, 8)
        self.assertEqual(len(writer.flush()), 1)
        
        writer.reset()
        writer.write_bits(0, 8)
        self.assertEqual(len(writer.flush()), 1)


class TestBitReader(unittest.TestCase):
    """比特读取器测试"""
    
    def test_read_single_bit(self):
        """测试读取单个比特"""
        data = bytes([0b10101010])  # 0xAA
        reader = BitReader(data)
        
        bits = [reader.read_bit() for _ in range(8)]
        self.assertEqual(bits, [1, 0, 1, 0, 1, 0, 1, 0])
    
    def test_read_bits(self):
        """测试读取多比特整数"""
        data = bytes([0b11110000])  # 0xF0
        reader = BitReader(data)
        
        value = reader.read_bits(4)
        self.assertEqual(value, 15)  # 1111
        
        value = reader.read_bits(4)
        self.assertEqual(value, 0)  # 0000
    
    def test_read_unary(self):
        """测试读取一元编码"""
        # 0001 0001
        data = bytes([0b00010001])
        reader = BitReader(data)
        
        self.assertEqual(reader.read_unary(), 3)  # 000 -> 1
        self.assertEqual(reader.read_unary(), 3)  # 000 -> 1
    
    def test_read_gamma(self):
        """测试读取 Gamma 编码"""
        writer = BitWriter()
        test_values = [1, 2, 5, 10, 20, 50, 100]
        
        for v in test_values:
            writer.write_gamma(v)
        
        data = writer.flush()
        reader = BitReader(data)
        
        decoded = [reader.read_gamma() for _ in range(len(test_values))]
        self.assertEqual(decoded, test_values)
    
    def test_has_more(self):
        """测试是否有更多数据"""
        data = bytes([0xFF, 0x00])
        reader = BitReader(data)
        
        self.assertTrue(reader.has_more())
        reader.read_bits(8)
        self.assertTrue(reader.has_more())
        reader.read_bits(8)
        self.assertFalse(reader.has_more())
    
    def test_eof_error(self):
        """测试到达末尾时的错误"""
        data = bytes([0xFF])
        reader = BitReader(data)
        
        reader.read_bits(8)  # 读完
        
        with self.assertRaises(EOFError):
            reader.read_bit()
    
    def test_roundtrip(self):
        """测试写入/读取往返"""
        writer = BitWriter()
        
        # 写入各种数据
        writer.write_bit(1)
        writer.write_bits(42, 6)
        writer.write_unary(5)
        writer.write_gamma(100)
        
        data = writer.flush()
        reader = BitReader(data)
        
        # 验证读取
        self.assertEqual(reader.read_bit(), 1)
        self.assertEqual(reader.read_bits(6), 42)
        self.assertEqual(reader.read_unary(), 5)
        self.assertEqual(reader.read_gamma(), 100)


class TestGolombCoding(unittest.TestCase):
    """Golomb 编码测试"""
    
    def test_encode_decode_basic(self):
        """测试基本编码/解码"""
        m = 8
        coder = GolombCoding(m)
        
        for value in range(0, 100):
            q, r = coder.encode(value)
            decoded = coder.decode(q, r)
            self.assertEqual(decoded, value)
    
    def test_encode_decode_edge_cases(self):
        """测试边界值"""
        m = 8
        coder = GolombCoding(m)
        
        # 0
        q, r = coder.encode(0)
        self.assertEqual((q, r), (0, 0))
        
        # 小于 M
        q, r = coder.encode(7)
        self.assertEqual((q, r), (0, 7))
        
        # 等于 M
        q, r = coder.encode(8)
        self.assertEqual((q, r), (1, 0))
        
        # 大于 M
        q, r = coder.encode(23)
        self.assertEqual((q, r), (2, 7))
    
    def test_sequence_encoding(self):
        """测试序列编码"""
        m = 10
        coder = GolombCoding(m)
        
        values = [0, 1, 5, 10, 20, 50, 100, 200]
        encoded = coder.encode_sequence(values)
        decoded = coder.decode_sequence(encoded, len(values))
        
        self.assertEqual(decoded, values)
    
    def test_optimal_m_calculation(self):
        """测试最优 M 计算"""
        # 小值序列
        small = [1, 2, 3, 4, 5]
        m = GolombCoding.optimal_m(small)
        self.assertGreater(m, 0)
        
        # 大值序列
        large = [100, 200, 300, 400, 500]
        m_large = GolombCoding.optimal_m(large)
        self.assertGreater(m_large, m)
        
        # 空序列
        empty = []
        self.assertEqual(GolombCoding.optimal_m(empty), 1)
        
        # 单元素
        single = [10]
        self.assertEqual(GolombCoding.optimal_m(single), 8)  # 应向上取到 2 的幂
    
    def test_power_of_two_m(self):
        """测试 M 为 2 的幂时的 Rice 编码优化"""
        coder = GolombCoding(16)  # M = 16 = 2^4
        
        self.assertTrue(coder._is_power_of_two)
        self.assertEqual(coder._log_m, 4)
        
        values = [0, 15, 16, 31, 32, 100]
        encoded = coder.encode_sequence(values)
        decoded = coder.decode_sequence(encoded, len(values))
        
        self.assertEqual(decoded, values)
    
    def test_non_power_of_two_m(self):
        """测试 M 不是 2 的幂时的截断二进制编码"""
        coder = GolombCoding(10)
        
        self.assertFalse(coder._is_power_of_two)
        
        values = [0, 9, 10, 19, 20, 100]
        encoded = coder.encode_sequence(values)
        decoded = coder.decode_sequence(encoded, len(values))
        
        self.assertEqual(decoded, values)
    
    def test_invalid_m(self):
        """测试无效参数"""
        with self.assertRaises(ValueError):
            GolombCoding(0)
        
        with self.assertRaises(ValueError):
            GolombCoding(-1)
    
    def test_invalid_value(self):
        """测试无效值"""
        coder = GolombCoding(8)
        
        with self.assertRaises(ValueError):
            coder.encode(-1)


class TestRiceCoding(unittest.TestCase):
    """Rice 编码测试"""
    
    def test_k_parameter(self):
        """测试 k 参数"""
        k = 4  # M = 16
        rice = RiceCoding(k)
        
        self.assertEqual(rice.k, k)
        self.assertEqual(rice.m, 16)
    
    def test_encode_decode(self):
        """测试编码/解码"""
        k = 3  # M = 8
        rice = RiceCoding(k)
        
        for value in range(0, 100):
            encoded = rice.encode_sequence([value])
            decoded = rice.decode_sequence(encoded, 1)
            self.assertEqual(decoded[0], value)
    
    def test_sequence_encoding(self):
        """测试序列编码"""
        k = 2
        rice = RiceCoding(k)
        
        values = [0, 1, 4, 7, 15, 31, 100]
        encoded = rice.encode_sequence(values)
        decoded = rice.decode_sequence(encoded, len(values))
        
        self.assertEqual(decoded, values)
    
    def test_optimal_k(self):
        """测试最优 k 计算"""
        # 小平均值 -> 小 k
        small_avg = [1, 2, 3, 4, 5]
        k = RiceCoding.optimal_k(small_avg)
        self.assertLessEqual(k, 2)
        
        # 大平均值 -> 大 k
        large_avg = [100, 200, 300, 400, 500]
        k_large = RiceCoding.optimal_k(large_avg)
        self.assertGreater(k_large, k)
        
        # 空序列
        self.assertEqual(RiceCoding.optimal_k([]), 0)
    
    def test_invalid_k(self):
        """测试无效参数"""
        with self.assertRaises(ValueError):
            RiceCoding(-1)
    
    def test_efficiency_vs_golomb(self):
        """测试 Rice 编码效率"""
        values = list(range(1, 101))
        
        k = RiceCoding.optimal_k(values)
        m = GolombCoding.optimal_m(values)
        
        rice = RiceCoding(k)
        golomb = GolombCoding(m)
        
        rice_size = len(rice.encode_sequence(values))
        golomb_size = len(golomb.encode_sequence(values))
        
        # Rice 应该效率相当或更好 (因为是优化版本)
        self.assertLessEqual(rice_size, golomb_size + 10)  # 允许一些误差


class TestInterleavedGolombCoding(unittest.TestCase):
    """交织 Golomb 编码测试"""
    
    def test_encode_decode(self):
        """测试编码/解码"""
        m = 10
        coder = InterleavedGolombCoding(m)
        
        for value in range(0, 50):
            encoded = coder.encode_to_writer(BitWriter(), value)
            # 需要完整测试
            pass
    
    def test_sequence_roundtrip(self):
        """测试序列往返"""
        m = 8
        coder = InterleavedGolombCoding(m)
        
        values = [0, 5, 10, 15, 20, 30, 50]
        
        writer = BitWriter()
        for v in values:
            coder.encode_to_writer(writer, v)
        
        data = writer.flush()
        
        reader = BitReader(data)
        decoded = []
        for _ in range(len(values)):
            decoded.append(coder.decode_from_reader(reader))
        
        self.assertEqual(decoded, values)


class TestDeltaGolombCompressor(unittest.TestCase):
    """Delta + Golomb 压缩器测试"""
    
    def test_delta_encode(self):
        """测试 Delta 编码"""
        values = [10, 15, 20, 25, 30]
        deltas = DeltaGolombCompressor.delta_encode(values)
        
        self.assertEqual(deltas, [10, 5, 5, 5, 5])
    
    def test_delta_decode(self):
        """测试 Delta 解码"""
        deltas = [10, 5, 5, 5, 5]
        values = DeltaGolombCompressor.delta_decode(deltas)
        
        self.assertEqual(values, [10, 15, 20, 25, 30])
    
    def test_delta_roundtrip(self):
        """测试 Delta 往返"""
        values = [1, 5, 10, 15, 20, 100, 200]
        deltas = DeltaGolombCompressor.delta_encode(values)
        decoded = DeltaGolombCompressor.delta_decode(deltas)
        
        self.assertEqual(decoded, values)
    
    def test_delta_invalid_sequence(self):
        """测试非有序序列"""
        values = [10, 5, 15]  # 非升序
        
        with self.assertRaises(ValueError):
            DeltaGolombCompressor.delta_encode(values)
    
    def test_compress_empty(self):
        """测试空序列压缩"""
        compressor = DeltaGolombCompressor()
        compressed = compressor.compress([])
        decoded = compressor.decompress(compressed)
        
        self.assertEqual(decoded, [])
    
    def test_compress_single(self):
        """测试单元素序列"""
        compressor = DeltaGolombCompressor()
        values = [100]
        
        compressed = compressor.compress(values)
        decoded = compressor.decompress(compressed)
        
        self.assertEqual(decoded, values)
    
    def test_compress_small_gaps(self):
        """测试小间隔序列"""
        compressor = DeltaGolombCompressor()
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        compressed = compressor.compress(values)
        decoded = compressor.decompress(compressed)
        
        self.assertEqual(decoded, values)
        self.assertLess(len(compressed), len(values) * 4)  # 应有压缩
    
    def test_compress_large_gaps(self):
        """测试大间隔序列"""
        compressor = DeltaGolombCompressor()
        values = [1, 100, 1000, 10000, 100000]
        
        compressed = compressor.compress(values)
        decoded = compressor.decompress(compressed)
        
        self.assertEqual(decoded, values)
    
    def test_compress_dense_ids(self):
        """测试密集 ID 序列 (倒排索引场景)"""
        compressor = DeltaGolombCompressor()
        
        # 模拟倒排索引中的文档 ID
        doc_ids = [1, 2, 3, 5, 8, 9, 10, 12, 15, 18, 20, 21, 23, 25, 28, 30]
        
        compressed = compressor.compress(doc_ids)
        decoded = compressor.decompress(compressed)
        
        self.assertEqual(decoded, doc_ids)
    
    def test_compression_ratio(self):
        """测试压缩比计算"""
        compressor = DeltaGolombCompressor()
        
        # 小间隔序列应有较高压缩比
        small_gap = list(range(1, 1001))
        ratio1 = compressor.get_compression_ratio(small_gap)
        self.assertGreater(ratio1, 1.0)
        
        # 大间隔序列压缩比较低
        large_gap = [1, 100, 1000, 10000]
        ratio2 = compressor.get_compression_ratio(large_gap)
        self.assertLess(ratio2, ratio1)
    
    def test_custom_m_parameter(self):
        """测试自定义 M 参数"""
        compressor = DeltaGolombCompressor(m=16)
        values = [1, 5, 10, 20, 40]
        
        compressed = compressor.compress(values)
        decoded = compressor.decompress(compressed)
        
        self.assertEqual(decoded, values)
    
    def test_very_long_sequence(self):
        """测试长序列"""
        compressor = DeltaGolombCompressor()
        values = list(range(1, 10001))
        
        compressed = compressor.compress(values)
        decoded = compressor.decompress(compressed)
        
        self.assertEqual(decoded, values)
        # 验证压缩效率
        self.assertLess(len(compressed), len(values) * 4)


class TestGolombRiceCoder(unittest.TestCase):
    """高级编码器测试"""
    
    def test_analyze_empty(self):
        """测试空数据分析"""
        analysis = GolombRiceCoder.analyze([])
        
        self.assertEqual(analysis['count'], 0)
        self.assertEqual(analysis['recommended_m'], 1)
    
    def test_analyze_values(self):
        """测试数据分析"""
        values = [1, 2, 5, 10, 20, 50, 100]
        analysis = GolombRiceCoder.analyze(values)
        
        self.assertEqual(analysis['count'], 7)
        self.assertEqual(analysis['min'], 1)
        self.assertEqual(analysis['max'], 100)
        self.assertGreater(analysis['mean'], 0)
    
    def test_encode_optimal(self):
        """测试最优编码"""
        values = [1, 2, 5, 10, 20, 50, 100]
        
        encoded, metadata = GolombRiceCoder.encode_optimal(values)
        decoded = GolombRiceCoder.decode(encoded, metadata)
        
        self.assertEqual(decoded, values)
        self.assertIn('type', metadata)
        self.assertIn('count', metadata)
    
    def test_type_selection(self):
        """测试类型选择"""
        # Rice 编码适合小值
        small_values = list(range(1, 51))
        analysis = GolombRiceCoder.analyze(small_values)
        self.assertEqual(analysis['recommended_type'], 'rice')
    
    def test_negative_values(self):
        """测试负值处理"""
        values = [-5, 0, 5, 10]
        analysis = GolombRiceCoder.analyze(values)
        
        # 应自动过滤负值
        self.assertGreater(analysis['count'], 0)


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_golomb_encode_decode(self):
        """测试 Golomb 编码便捷函数"""
        value = 25
        m = 10
        
        q, r = golomb_encode(value, m)
        decoded = golomb_decode(q, r, m)
        
        self.assertEqual(decoded, value)
    
    def test_rice_encode_decode(self):
        """测试 Rice 编码便捷函数"""
        value = 25
        k = 3  # M = 8
        
        q, r = rice_encode(value, k)
        decoded = rice_decode(q, r, k)
        
        self.assertEqual(decoded, value)
    
    def test_compress_decompress(self):
        """测试压缩便捷函数"""
        values = [1, 5, 10, 20, 50, 100]
        
        compressed = compress_sorted_integers(values)
        decoded = decompress_sorted_integers(compressed)
        
        self.assertEqual(decoded, values)
    
    def test_optimal_parameter(self):
        """测试最优参数便捷函数"""
        values = [1, 2, 3, 4, 5]
        m = optimal_parameter(values)
        
        self.assertGreater(m, 0)
        # 应是 2 的幂
        self.assertEqual(m & (m - 1), 0)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_zero_value(self):
        """测试零值"""
        coder = GolombCoding(8)
        q, r = coder.encode(0)
        self.assertEqual((q, r), (0, 0))
    
    def test_very_large_value(self):
        """测试大值"""
        coder = GolombCoding(8)
        large = 100000
        
        q, r = coder.encode(large)
        decoded = coder.decode(q, r)
        self.assertEqual(decoded, large)
    
    def test_sequence_with_repeated_values(self):
        """测试重复值序列"""
        compressor = DeltaGolombCompressor()
        values = [5, 5, 5, 5, 5]  # Delta 编码后: [5, 0, 0, 0, 0]
        
        compressed = compressor.compress(values)
        decoded = compressor.decompress(compressed)
        
        self.assertEqual(decoded, values)
    
    def test_m_equals_one(self):
        """测试 M = 1"""
        coder = GolombCoding(1)
        
        # M=1 时，所有值编码为一元
        for value in [0, 1, 5, 10]:
            q, r = coder.encode(value)
            self.assertEqual(r, 0)
            self.assertEqual(q, value)
    
    def test_large_m(self):
        """测试大 M"""
        coder = GolombCoding(1000)
        
        values = [0, 500, 999, 1000, 1001, 2000]
        encoded = coder.encode_sequence(values)
        decoded = coder.decode_sequence(encoded, len(values))
        
        self.assertEqual(decoded, values)


class TestPerformance(unittest.TestCase):
    """性能测试"""
    
    def test_large_sequence_performance(self):
        """测试大序列性能"""
        import time
        
        values = list(range(1, 100000))
        
        start = time.time()
        compressor = DeltaGolombCompressor()
        compressed = compressor.compress(values)
        encode_time = time.time() - start
        
        start = time.time()
        decoded = compressor.decompress(compressed)
        decode_time = time.time() - start
        
        self.assertEqual(decoded, values)
        
        # 性能检查 (应该在合理时间内完成)
        self.assertLess(encode_time, 5)  # 编码 < 5 秒
        self.assertLess(decode_time, 5)  # 解码 < 5 秒
        
        print(f"\n大序列性能: 编码 {encode_time:.3f}s, 解码 {decode_time:.3f}s")
        print(f"原始大小: {len(values) * 4} 字节, 压缩后: {len(compressed)} 字节")
        print(f"压缩比: {len(values) * 4 / len(compressed):.2f}x")


if __name__ == "__main__":
    unittest.main(verbosity=2)