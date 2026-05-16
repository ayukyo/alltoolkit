"""
LZ77 Utils Test Suite - LZ77 压缩算法测试

测试覆盖：
- 编码器基础功能
- 解码器基础功能
- 字符串和字节数据处理
- 令牌创建和属性
- 流式编码
- 压缩结果分析
- 边界条件
- 数据完整性验证
- 预设配置
"""

import unittest
from mod import (
    LZ77Token,
    LZ77Result,
    LZ77Encoder,
    LZ77Decoder,
    LZ77Compressor,
    StreamingLZ77Encoder,
    lz77_encode,
    lz77_decode,
    lz77_decode_to_string,
    lz77_compress,
    analyze_lz77,
    compare_presets,
    TokenType,
)


class TestLZ77Token(unittest.TestCase):
    """测试 LZ77Token 类"""
    
    def test_literal_token_creation(self):
        """测试字面量令牌创建"""
        token = LZ77Token.literal(65)  # 'A'
        self.assertEqual(token.offset, 0)
        self.assertEqual(token.length, 0)
        self.assertEqual(token.value, 65)
        self.assertTrue(token.is_literal)
        self.assertFalse(token.is_match)
    
    def test_literal_token_string(self):
        """测试字符串字面量令牌"""
        token = LZ77Token.literal('A')
        self.assertEqual(token.value, 'A')
        self.assertTrue(token.is_literal)
    
    def test_match_token_creation(self):
        """测试匹配令牌创建"""
        token = LZ77Token.match(10, 5)
        self.assertEqual(token.offset, 10)
        self.assertEqual(token.length, 5)
        self.assertIsNone(token.value)
        self.assertFalse(token.is_literal)
        self.assertTrue(token.is_match)
    
    def test_token_to_tuple(self):
        """测试令牌转元组"""
        literal = LZ77Token.literal(65)
        self.assertEqual(literal.to_tuple(), (0, 0, 65))
        
        match = LZ77Token.match(10, 5)
        self.assertEqual(match.to_tuple(), (10, 5, None))
    
    def test_token_repr(self):
        """测试令牌字符串表示"""
        literal = LZ77Token.literal(65)
        self.assertIn('literal', repr(literal))
        
        match = LZ77Token.match(10, 5)
        self.assertIn('offset=10', repr(match))
        self.assertIn('length=5', repr(match))


class TestLZ77Encoder(unittest.TestCase):
    """测试 LZ77Encoder 类"""
    
    def test_encoder_creation(self):
        """测试编码器创建"""
        encoder = LZ77Encoder(window_size=1024, look_ahead_size=15, min_match_length=3)
        self.assertEqual(encoder.window_size, 1024)
        self.assertEqual(encoder.look_ahead_size, 15)
        self.assertEqual(encoder.min_match_length, 3)
    
    def test_encoder_default_params(self):
        """测试默认参数"""
        encoder = LZ77Encoder()
        self.assertEqual(encoder.window_size, 4096)
        self.assertEqual(encoder.look_ahead_size, 18)
        self.assertEqual(encoder.min_match_length, 3)
    
    def test_encoder_invalid_params(self):
        """测试无效参数"""
        with self.assertRaises(ValueError):
            LZ77Encoder(window_size=0)
        
        with self.assertRaises(ValueError):
            LZ77Encoder(look_ahead_size=0)
        
        with self.assertRaises(ValueError):
            LZ77Encoder(min_match_length=1)
        
        with self.assertRaises(ValueError):
            LZ77Encoder(min_match_length=20, look_ahead_size=10)
    
    def test_encoder_from_preset(self):
        """测试从预设创建"""
        encoder = LZ77Encoder.from_preset('fast')
        self.assertEqual(encoder.window_size, 1024)
        
        encoder = LZ77Encoder.from_preset('maximum')
        self.assertEqual(encoder.window_size, 32768)
        
        with self.assertRaises(ValueError):
            LZ77Encoder.from_preset('invalid')
    
    def test_encode_simple_string(self):
        """测试简单字符串编码"""
        encoder = LZ77Encoder(window_size=100, min_match_length=3)
        # 无重复的字符串应该全部为字面量
        result = encoder.encode("abcdefghij")
        self.assertEqual(result.literal_count, 10)
        self.assertEqual(result.match_count, 0)
    
    def test_encode_repeated_string(self):
        """测试重复字符串编码"""
        encoder = LZ77Encoder(window_size=100, min_match_length=3)
        # 重复字符串应该产生匹配
        result = encoder.encode("abcabcabcabc")
        self.assertGreater(result.match_count, 0)
    
    def test_encode_bytes(self):
        """测试字节编码"""
        encoder = LZ77Encoder(window_size=100)
        data = b"hellohellohello"
        result = encoder.encode(data)
        self.assertGreater(result.match_count, 0)
    
    def test_encode_empty(self):
        """测试空数据编码"""
        encoder = LZ77Encoder()
        result = encoder.encode("")
        self.assertEqual(len(result.tokens), 0)
        self.assertEqual(result.original_size, 0)
    
    def test_encode_long_repeated(self):
        """测试长重复序列"""
        encoder = LZ77Encoder(window_size=100, look_ahead_size=50)
        data = "a" * 100
        result = encoder.encode(data)
        # 应该产生至少一个长匹配
        self.assertGreater(result.match_count, 0)
        # 验证压缩率
        self.assertGreater(result.compression_ratio, 1.0)
    
    def test_encode_to_tuples(self):
        """测试编码为元组"""
        encoder = LZ77Encoder(window_size=100)
        tuples = encoder.encode_to_tuples("abcabcabc")
        self.assertIsInstance(tuples, list)
        # 检查元组格式
        for t in tuples:
            self.assertEqual(len(t), 3)
    
    def test_encode_iter(self):
        """测试流式编码"""
        encoder = LZ77Encoder(window_size=100)
        tokens = list(encoder.encode_iter("abcabcabc"))
        self.assertGreater(len(tokens), 0)
        for token in tokens:
            self.assertIsInstance(token, LZ77Token)
    
    def test_overlapping_match(self):
        """测试重叠匹配"""
        encoder = LZ77Encoder(window_size=10, min_match_length=2)
        # "abab" - 第二个 "ab" 匹配第一个 "ab"（重叠）
        data = "abababab"
        result = encoder.encode(data)
        tokens = result.tokens
        
        # 验证解码正确
        decoder = LZ77Decoder()
        decoded = decoder.decode(tokens)
        self.assertEqual(decoded.decode('utf-8'), data)


class TestLZ77Decoder(unittest.TestCase):
    """测试 LZ77Decoder 类"""
    
    def test_decode_literals(self):
        """测试字面量解码"""
        decoder = LZ77Decoder()
        tokens = [LZ77Token.literal(65), LZ77Token.literal(66), LZ77Token.literal(67)]
        result = decoder.decode(tokens)
        self.assertEqual(result, b"ABC")
    
    def test_decode_single_match(self):
        """测试单个匹配解码"""
        decoder = LZ77Decoder()
        # "abcab" - 最后的 "ab" 匹配前面的
        tokens = [
            LZ77Token.literal(97),   # 'a'
            LZ77Token.literal(98),   # 'b'
            LZ77Token.literal(99),   # 'c'
            LZ77Token.match(3, 2),   # 匹配 "ab"（offset=3, length=2）
        ]
        result = decoder.decode(tokens)
        self.assertEqual(result.decode('utf-8'), "abcab")
    
    def test_decode_overlapping_match(self):
        """测试重叠匹配解码"""
        decoder = LZ77Decoder()
        # "aaaa" - 第一个 'a' 后面三个 'a' 匹配第一个（offset=1）
        tokens = [
            LZ77Token.literal(97),   # 'a'
            LZ77Token.match(1, 3),   # 匹配3个（重叠复制）
        ]
        result = decoder.decode(tokens)
        self.assertEqual(result.decode('utf-8'), "aaaa")
    
    def test_decode_to_string(self):
        """测试解码为字符串"""
        decoder = LZ77Decoder()
        tokens = [LZ77Token.literal(65), LZ77Token.literal(66)]
        result = decoder.decode_to_string(tokens)
        self.assertEqual(result, "AB")
    
    def test_decode_tuples(self):
        """测试从元组解码"""
        decoder = LZ77Decoder()
        tuples = [(0, 0, 65), (0, 0, 66), (2, 2, None)]
        # "ABAB" - 最后的 "AB" 匹配前面的
        result = decoder.decode_tuples(tuples)
        # 注意：需要验证这个逻辑
        self.assertEqual(result[:2], b"AB")
    
    def test_decode_invalid_offset(self):
        """测试无效偏移"""
        decoder = LZ77Decoder()
        tokens = [LZ77Token.match(100, 5)]  # offset=100 但缓冲区为空
        with self.assertRaises(ValueError):
            decoder.decode(tokens)


class TestLZ77Compressor(unittest.TestCase):
    """测试 LZ77Compressor 高级接口"""
    
    def test_compress_string(self):
        """测试字符串压缩"""
        compressor = LZ77Compressor()
        result = compressor.compress("hellohellohello")
        self.assertGreater(result.compression_ratio, 1.0)
    
    def test_compress_bytes(self):
        """测试字节压缩"""
        compressor = LZ77Compressor()
        result = compressor.compress(b"abcabcabc")
        self.assertGreater(result.match_count, 0)
    
    def test_roundtrip_string(self):
        """测试字符串往返压缩"""
        compressor = LZ77Compressor()
        data = "This is a test string with some repetition repetition repetition."
        result, success = compressor.roundtrip(data)
        self.assertTrue(success)
        decompressed = compressor.decompress_to_string(result.tokens)
        self.assertEqual(decompressed, data)
    
    def test_roundtrip_bytes(self):
        """测试字节往返压缩"""
        compressor = LZ77Compressor()
        data = b"binary\x00binary\x00binary"
        result, success = compressor.roundtrip(data)
        self.assertTrue(success)
    
    def test_presets(self):
        """测试预设创建"""
        fast = LZ77Compressor.fast()
        self.assertEqual(fast.encoder.window_size, 1024)
        
        balanced = LZ77Compressor.balanced()
        self.assertEqual(balanced.encoder.window_size, 4096)
        
        maximum = LZ77Compressor.maximum()
        self.assertEqual(maximum.encoder.window_size, 32768)
    
    def test_compare_presets(self):
        """测试预设效果对比"""
        data = "a" * 1000
        fast_result = LZ77Compressor.fast().compress(data)
        max_result = LZ77Compressor.maximum().compress(data)
        # 最大压缩应该有更好的压缩率（或相近）
        self.assertGreaterEqual(max_result.compression_ratio, fast_result.compression_ratio)


class TestStreamingLZ77Encoder(unittest.TestCase):
    """测试流式编码器"""
    
    def test_streaming_encode(self):
        """测试流式编码"""
        encoder = StreamingLZ77Encoder(window_size=50, min_match_length=3)
        
        # 分块输入
        chunk1 = encoder.feed("abcabcabc")
        # 可能需要更多数据才能产生匹配
        chunk2 = encoder.feed("abcabcabc")
        remaining = encoder.flush()
        
        # 收集所有令牌
        all_tokens = chunk1 + chunk2 + remaining
        
        # 验证解码正确
        decoder = LZ77Decoder()
        decoded = decoder.decode(all_tokens)
        self.assertEqual(decoded.decode('utf-8'), "abcabcabcabcabcabc")
    
    def test_streaming_reset(self):
        """测试流式编码器重置"""
        encoder = StreamingLZ77Encoder()
        encoder.feed("hello")
        encoder.reset()
        self.assertEqual(len(encoder.buffer), 0)
        self.assertEqual(encoder.processed, 0)
    
    def test_streaming_large_data(self):
        """测试流式处理大数据"""
        encoder = StreamingLZ77Encoder(window_size=100, min_match_length=3)
        
        # 分多次输入重复数据
        all_data = ""
        all_tokens = []
        for _ in range(10):
            chunk = "abcdefghabcdefgh"
            all_data += chunk
            tokens = encoder.feed(chunk)
            all_tokens.extend(tokens)
        
        # 刷新剩余
        all_tokens.extend(encoder.flush())
        
        # 验证完整性
        decoder = LZ77Decoder()
        decoded = decoder.decode(all_tokens)
        self.assertEqual(decoded.decode('utf-8'), all_data)


class TestLZ77Result(unittest.TestCase):
    """测试 LZ77Result 类"""
    
    def test_result_properties(self):
        """测试结果属性"""
        tokens = [
            LZ77Token.literal(65),
            LZ77Token.literal(66),
            LZ77Token.match(2, 2),
        ]
        result = LZ77Result(
            tokens=tokens,
            original_size=10,
            compressed_size=5,
            literal_count=2,
            match_count=1,
            window_size=100,
            min_match_length=3
        )
        
        self.assertEqual(result.total_tokens, 3)
        self.assertEqual(result.compression_ratio, 2.0)
        self.assertEqual(result.space_saving, 50.0)
        self.assertEqual(result.match_ratio, 1/3)
    
    def test_result_zero_sizes(self):
        """测试零大小情况"""
        result = LZ77Result(
            tokens=[],
            original_size=0,
            compressed_size=0,
            literal_count=0,
            match_count=0,
            window_size=100,
            min_match_length=3
        )
        
        self.assertEqual(result.compression_ratio, 0.0)
        self.assertEqual(result.space_saving, 0.0)
        self.assertEqual(result.match_ratio, 0.0)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_lz77_encode(self):
        """测试 lz77_encode 函数"""
        result = lz77_encode("abcabcabc", window_size=100)
        self.assertIsInstance(result, LZ77Result)
        self.assertGreater(result.match_count, 0)
    
    def test_lz77_decode(self):
        """测试 lz77_decode 函数"""
        encoder = LZ77Encoder()
        result = encoder.encode("abcabcabc")
        decoded = lz77_decode(result.tokens)
        self.assertEqual(decoded.decode('utf-8'), "abcabcabc")
    
    def test_lz77_decode_to_string(self):
        """测试 lz77_decode_to_string 函数"""
        encoder = LZ77Encoder()
        result = encoder.encode("hellohello")
        decoded = lz77_decode_to_string(result.tokens)
        self.assertEqual(decoded, "hellohello")
    
    def test_lz77_compress(self):
        """测试 lz77_compress 函数"""
        result = lz77_compress("repeatedrepeatedrepeated", preset='fast')
        self.assertGreater(result.compression_ratio, 1.0)
    
    def test_analyze_lz77(self):
        """测试 analyze_lz77 函数"""
        analysis = analyze_lz77("abcabcabcabcabcabc")
        self.assertIn('compression_ratio', analysis)
        self.assertIn('space_saving', analysis)
        self.assertIn('match_lengths_distribution', analysis)
        self.assertGreater(analysis['match_count'], 0)
    
    def test_compare_presets(self):
        """测试 compare_presets 函数"""
        comparison = compare_presets("aaaa" * 100)
        self.assertIn('fast', comparison)
        self.assertIn('balanced', comparison)
        self.assertIn('maximum', comparison)
        self.assertIn('small', comparison)
        
        # 验证各预设都有有效结果
        for preset, result in comparison.items():
            self.assertIn('compression_ratio', result)


class TestEdgeCases(unittest.TestCase):
    """测试边界条件"""
    
    def test_single_character(self):
        """测试单个字符"""
        encoder = LZ77Encoder()
        result = encoder.encode("a")
        self.assertEqual(len(result.tokens), 1)
        self.assertTrue(result.tokens[0].is_literal)
    
    def test_two_characters(self):
        """测试两个字符"""
        encoder = LZ77Encoder(min_match_length=3)
        result = encoder.encode("ab")
        self.assertEqual(result.literal_count, 2)
    
    def test_short_match(self):
        """测试短匹配（低于最小长度）"""
        encoder = LZ77Encoder(min_match_length=3)
        result = encoder.encode("abab")  # 长度2的匹配会被忽略
        self.assertEqual(result.literal_count, 4)
    
    def test_exact_min_match(self):
        """测试恰好等于最小匹配长度"""
        encoder = LZ77Encoder(min_match_length=3)
        result = encoder.encode("abcabc")  # 长度3的匹配
        self.assertGreater(result.match_count, 0)
    
    def test_unicode_string(self):
        """测试 Unicode 字符串"""
        compressor = LZ77Compressor()
        data = "你好你好你好"
        result, success = compressor.roundtrip(data)
        self.assertTrue(success)
    
    def test_binary_data(self):
        """测试二进制数据"""
        compressor = LZ77Compressor()
        # 包含各种字节值
        data = bytes(range(256)) + bytes(range(256))
        result = compressor.compress(data)
        # 应该能处理
        self.assertGreater(len(result.tokens), 0)
    
    def test_all_same_bytes(self):
        """测试全相同字节"""
        encoder = LZ77Encoder(window_size=50, look_ahead_size=20)
        result = encoder.encode(b"\x00" * 100)
        # 应有极高的压缩率
        self.assertGreater(result.compression_ratio, 5.0)
    
    def test_no_repetition(self):
        """测试无重复数据"""
        encoder = LZ77Encoder()
        # 随机序列（这里用伪随机）
        import hashlib
        data = hashlib.sha256(b"test").hexdigest()
        result = encoder.encode(data)
        # 应全部为字面量
        self.assertEqual(result.match_count, 0)


class TestIntegrity(unittest.TestCase):
    """测试数据完整性"""
    
    def test_various_patterns(self):
        """测试各种模式的完整性"""
        compressor = LZ77Compressor()
        
        patterns = [
            "aaaaaaaaaa",
            "abcabcabcabc",
            "ababababab",
            "aabaabaabaab",
            "xyzxyzxyzxyzxyzxyz",
            "The quick brown fox jumps over the lazy dog. The quick brown fox jumps.",
            "Python is great! Python is great! Python is great!",
        ]
        
        for pattern in patterns:
            result, success = compressor.roundtrip(pattern)
            self.assertTrue(success, f"Failed for pattern: {pattern}")
    
    def test_large_data_integrity(self):
        """测试大数据完整性"""
        compressor = LZ77Compressor.maximum()
        
        # 生成大重复数据
        data = "Lorem ipsum dolor sit amet. " * 100
        result, success = compressor.roundtrip(data)
        self.assertTrue(success)
    
    def test_preserve_exact_bytes(self):
        """测试精确字节保留"""
        compressor = LZ77Compressor()
        data = bytes([0, 1, 2, 127, 128, 255, 0, 1, 2, 127, 128, 255])
        result = compressor.compress(data)
        decoded = compressor.decompress(result.tokens)
        self.assertEqual(decoded, data)


if __name__ == '__main__':
    unittest.main(verbosity=2)