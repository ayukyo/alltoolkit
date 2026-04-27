"""
RLE Utilities 测试套件

测试游程编码工具的所有功能。
"""

import sys
import os
import unittest

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    RLEEncoder, RLEDecoder, RLE, RLERun,
    StreamingRLEEncoder,
    rle_encode, rle_decode, rle_compress, rle_decompress
)


class TestRLERun(unittest.TestCase):
    """测试 RLERun 数据类"""
    
    def test_create_run(self):
        """测试创建游程"""
        run = RLERun(value='A', count=3)
        self.assertEqual(run.value, 'A')
        self.assertEqual(run.count, 3)
    
    def test_repr(self):
        """测试字符串表示"""
        run = RLERun(value='X', count=5)
        self.assertIn("RLERun", repr(run))
        self.assertIn("X", repr(run))
        self.assertIn("5", repr(run))


class TestRLEEncoder(unittest.TestCase):
    """测试游程编码器"""
    
    def test_encode_string_empty(self):
        """测试空字符串编码"""
        encoder = RLEEncoder()
        self.assertEqual(encoder.encode_string(""), [])
    
    def test_encode_string_single(self):
        """测试单字符编码"""
        encoder = RLEEncoder()
        runs = encoder.encode_string("A")
        self.assertEqual(len(runs), 1)
        self.assertEqual(runs[0].value, 'A')
        self.assertEqual(runs[0].count, 1)
    
    def test_encode_string_simple(self):
        """测试简单字符串编码"""
        encoder = RLEEncoder()
        runs = encoder.encode_string("AAABBC")
        self.assertEqual(len(runs), 3)
        self.assertEqual(runs[0], RLERun('A', 3))
        self.assertEqual(runs[1], RLERun('B', 2))
        self.assertEqual(runs[2], RLERun('C', 1))
    
    def test_encode_string_no_repeats(self):
        """测试无重复字符编码"""
        encoder = RLEEncoder()
        runs = encoder.encode_string("ABCDEF")
        self.assertEqual(len(runs), 6)
        for i, run in enumerate(runs):
            self.assertEqual(run.count, 1)
            self.assertEqual(run.value, chr(ord('A') + i))
    
    def test_encode_string_all_same(self):
        """测试全部相同字符编码"""
        encoder = RLEEncoder()
        runs = encoder.encode_string("AAAAAA")
        self.assertEqual(len(runs), 1)
        self.assertEqual(runs[0].value, 'A')
        self.assertEqual(runs[0].count, 6)
    
    def test_encode_bytes_empty(self):
        """测试空字节编码"""
        encoder = RLEEncoder()
        self.assertEqual(encoder.encode_bytes(b""), [])
    
    def test_encode_bytes_simple(self):
        """测试简单字节编码"""
        encoder = RLEEncoder()
        runs = encoder.encode_bytes(b'\x00\x00\x00\xFF\xFF')
        self.assertEqual(len(runs), 2)
        self.assertEqual(runs[0].value, 0)
        self.assertEqual(runs[0].count, 3)
        self.assertEqual(runs[1].value, 255)
        self.assertEqual(runs[1].count, 2)
    
    def test_encode_iterable(self):
        """测试可迭代对象编码"""
        encoder = RLEEncoder()
        runs = encoder.encode_iterable([1, 1, 1, 2, 3, 3])
        self.assertEqual(len(runs), 3)
        self.assertEqual(runs[0], RLERun(1, 3))
        self.assertEqual(runs[1], RLERun(2, 1))
        self.assertEqual(runs[2], RLERun(3, 2))
    
    def test_encode_to_tuples(self):
        """测试元组列表编码"""
        encoder = RLEEncoder()
        tuples = encoder.encode_to_tuples("AABB")
        self.assertEqual(tuples, [('A', 2), ('B', 2)])
    
    def test_encode_compact(self):
        """测试紧凑编码"""
        encoder = RLEEncoder(min_run_length=2)
        result = encoder.encode_compact("AAABBCDDD")
        self.assertEqual(result, "3A2BC3D")
    
    def test_encode_compact_no_repeats(self):
        """测试无重复紧凑编码"""
        encoder = RLEEncoder(min_run_length=2)
        result = encoder.encode_compact("ABC")
        self.assertEqual(result, "ABC")
    
    def test_encode_compact_with_singles(self):
        """测试混合单字符紧凑编码"""
        encoder = RLEEncoder(min_run_length=2)
        result = encoder.encode_compact("AAABCDDE")
        # AAA -> 3A, B -> B, C -> C, DD -> 2D, E -> E
        self.assertEqual(result, "3ABC2DE")
    
    def test_encode_bytes_packed(self):
        """测试字节打包编码"""
        encoder = RLEEncoder()
        # 3个0, 2个255 -> [2, 0, 1, 255]
        result = encoder.encode_bytes_packed(b'\x00\x00\x00\xFF\xFF')
        self.assertEqual(result, b'\x02\x00\x01\xFF')
    
    def test_min_run_length_validation(self):
        """测试最小游程长度验证"""
        with self.assertRaises(ValueError):
            RLEEncoder(min_run_length=1)
        
        with self.assertRaises(ValueError):
            RLEEncoder(min_run_length=0)
    
    def test_max_count(self):
        """测试最大计数限制"""
        encoder = RLEEncoder(max_count=3)
        runs = encoder.encode_string("AAAAA")
        # 应该分成两段：3 + 2
        self.assertEqual(len(runs), 2)
        self.assertEqual(runs[0].count, 3)
        self.assertEqual(runs[1].count, 2)


class TestRLEDecoder(unittest.TestCase):
    """测试游程解码器"""
    
    def test_decode_string(self):
        """测试字符串解码"""
        decoder = RLEDecoder()
        runs = [RLERun('A', 3), RLERun('B', 2), RLERun('C', 1)]
        result = decoder.decode_string(runs)
        self.assertEqual(result, "AAABBC")
    
    def test_decode_string_empty(self):
        """测试空游程解码"""
        decoder = RLEDecoder()
        self.assertEqual(decoder.decode_string([]), "")
    
    def test_decode_bytes(self):
        """测试字节解码"""
        decoder = RLEDecoder()
        runs = [RLERun(0, 3), RLERun(255, 2)]
        result = decoder.decode_bytes(runs)
        self.assertEqual(result, b'\x00\x00\x00\xFF\xFF')
    
    def test_decode_tuples(self):
        """测试元组解码"""
        decoder = RLEDecoder()
        tuples = [('A', 3), ('B', 2)]
        result = decoder.decode_tuples(tuples)
        self.assertEqual(result, "AAABB")
    
    def test_decode_tuples_bytes(self):
        """测试元组字节解码"""
        decoder = RLEDecoder()
        tuples = [(0, 3), (255, 1)]
        result = decoder.decode_tuples(tuples, as_bytes=True)
        self.assertEqual(result, b'\x00\x00\x00\xFF')
    
    def test_decode_compact(self):
        """测试紧凑解码"""
        decoder = RLEDecoder()
        result = decoder.decode_compact("3A2BC3D")
        self.assertEqual(result, "AAABBCDDD")
    
    def test_decode_compact_single(self):
        """测试单字符紧凑解码"""
        decoder = RLEDecoder()
        result = decoder.decode_compact("ABC")
        self.assertEqual(result, "ABC")
    
    def test_decode_compact_multidigit(self):
        """测试多位数紧凑解码"""
        decoder = RLEDecoder()
        result = decoder.decode_compact("12A")
        self.assertEqual(result, "A" * 12)
    
    def test_decode_bytes_packed(self):
        """测试字节打包解码"""
        decoder = RLEDecoder()
        # [2, 0] 表示 3个0, [1, 255] 表示 2个255
        result = decoder.decode_bytes_packed(b'\x02\x00\x01\xFF')
        self.assertEqual(result, b'\x00\x00\x00\xFF\xFF')


class TestRLE(unittest.TestCase):
    """测试高级接口"""
    
    def test_encode_decode_string(self):
        """测试字符串编解码"""
        original = "AAABBBCCCCD"
        encoded = RLE.encode(original)
        decoded = RLE.decode(encoded)
        self.assertEqual(decoded, original)
    
    def test_encode_decode_bytes(self):
        """测试字节编解码"""
        original = b'\x00\x00\x00\xFF\xFF'
        encoded = RLE.encode(original)
        decoded = RLE.decode(encoded, as_bytes=True)
        self.assertEqual(decoded, original)
    
    def test_compact_encode_decode(self):
        """测试紧凑编解码"""
        original = "AAABBBCCCCD"
        encoded = RLE.encode_compact(original)
        decoded = RLE.decode_compact(encoded)
        self.assertEqual(decoded, original)
    
    def test_bytes_packed_encode_decode(self):
        """测试字节打包编解码"""
        original = b'\x00\x00\x00\x00\x00\xFF\xFF\x80'
        encoded = RLE.encode_bytes(original)
        decoded = RLE.decode_bytes(encoded)
        self.assertEqual(decoded, original)
    
    def test_compress_ratio(self):
        """测试压缩比计算"""
        original = "AAAAAABBBBBB"  # 12 字符
        encoded = RLE.encode_compact(original)  # "6A6B" = 4 字符
        ratio = RLE.compress_ratio(original, encoded)
        self.assertEqual(ratio, 3.0)  # 12 / 4 = 3
    
    def test_analyze(self):
        """测试数据分析"""
        analysis = RLE.analyze("AAABBC")
        self.assertEqual(analysis['total_runs'], 3)
        self.assertEqual(analysis['max_run_length'], 3)
        self.assertGreater(analysis['avg_run_length'], 0)
        # 5/6 可压缩，使用近似比较
        self.assertAlmostEqual(analysis['compression_potential'], 5/6, places=2)
    
    def test_analyze_empty(self):
        """测试空数据分析"""
        analysis = RLE.analyze("")
        self.assertEqual(analysis['total_runs'], 0)
        self.assertEqual(analysis['max_run_length'], 0)
    
    def test_analyze_bytes(self):
        """测试字节数据分析"""
        analysis = RLE.analyze(b'\x00\x00\x00\xFF')
        self.assertEqual(analysis['total_runs'], 2)
        self.assertEqual(analysis['max_run_length'], 3)


class TestStreamingRLEEncoder(unittest.TestCase):
    """测试流式编码器"""
    
    def test_feed_single_chunk(self):
        """测试单块输入"""
        encoder = StreamingRLEEncoder()
        completed = encoder.feed("AAAB")
        self.assertEqual(len(completed), 1)
        self.assertEqual(completed[0], RLERun('A', 3))
    
    def test_feed_multiple_chunks(self):
        """测试多块输入"""
        encoder = StreamingRLEEncoder()
        
        # 第一块
        encoder.feed("AA")
        # 第二块继续 A
        encoder.feed("A")
        # 第三块不同字符
        completed = encoder.feed("BB")
        # 应该完成 A 的游程
        self.assertEqual(len(completed), 1)
        self.assertEqual(completed[0], RLERun('A', 3))
    
    def test_flush(self):
        """测试刷新"""
        encoder = StreamingRLEEncoder()
        encoder.feed("AAA")
        last_run = encoder.flush()
        self.assertEqual(last_run, RLERun('A', 3))
        self.assertIsNone(encoder.flush())
    
    def test_reset(self):
        """测试重置"""
        encoder = StreamingRLEEncoder()
        encoder.feed("AAA")
        encoder.reset()
        self.assertIsNone(encoder.flush())


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_rle_encode(self):
        """测试便捷编码函数"""
        result = rle_encode("AABB")
        self.assertEqual(result, [('A', 2), ('B', 2)])
    
    def test_rle_decode(self):
        """测试便捷解码函数"""
        result = rle_decode([('A', 2), ('B', 2)])
        self.assertEqual(result, "AABB")
    
    def test_rle_compress(self):
        """测试便捷压缩函数"""
        result = rle_compress("AABB")
        self.assertEqual(result, "2A2B")
    
    def test_rle_decompress(self):
        """测试便捷解压函数"""
        result = rle_decompress("2A2B")
        self.assertEqual(result, "AABB")


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_unicode_string(self):
        """测试 Unicode 字符串"""
        text = "你好你好好好好"
        encoded = rle_encode(text)
        decoded = rle_decode(encoded)
        self.assertEqual(decoded, text)
    
    def test_large_run(self):
        """测试大游程"""
        text = "A" * 1000
        encoded = rle_encode(text)
        self.assertEqual(len(encoded), 1)
        self.assertEqual(encoded[0], ('A', 1000))
        decoded = rle_decode(encoded)
        self.assertEqual(decoded, text)
    
    def test_alternating(self):
        """测试交替字符"""
        text = "ABABAB"
        encoded = rle_encode(text)
        self.assertEqual(len(encoded), 6)
        for _, count in encoded:
            self.assertEqual(count, 1)
    
    def test_binary_data(self):
        """测试二进制数据"""
        data = bytes([i % 256 for i in range(256)])
        encoded = RLE.encode(data)
        decoded = RLE.decode(encoded, as_bytes=True)
        self.assertEqual(decoded, data)


class TestCompressionEfficiency(unittest.TestCase):
    """测试压缩效率"""
    
    def test_highly_compressible(self):
        """测试高压缩数据"""
        # 高度可压缩：大量重复
        text = "A" * 1000 + "B" * 1000
        encoded = rle_compress(text)
        # 编码后应该很短
        self.assertLess(len(encoded), 20)
        decoded = rle_decompress(encoded)
        self.assertEqual(decoded, text)
    
    def test_low_compressibility(self):
        """测试低压缩数据"""
        # 低压缩性：无重复
        import string
        text = string.ascii_letters[:50]
        encoded = rle_compress(text)
        # 应该几乎无压缩
        self.assertGreaterEqual(len(encoded), len(text))
        decoded = rle_decompress(encoded)
        self.assertEqual(decoded, text)
    
    def test_mixed_data(self):
        """测试混合数据"""
        text = "AAA" + "BCDEF" + "GGGG" + "HIJ" + "KKKKK"
        analysis = RLE.analyze(text)
        # 应该有合理的压缩潜力
        self.assertGreater(analysis['compression_potential'], 0)


if __name__ == "__main__":
    unittest.main()