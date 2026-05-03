"""
Leet Speak Utils 测试文件
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from leet_speak_utils.mod import (
    LeetSpeakEncoder,
    LeetSpeakDecoder,
    LeetSpeakGenerator,
    encode,
    decode,
    is_leet,
    detect_level,
    to_leet,
    from_leet,
    create_custom_encoder,
)


class TestLeetSpeakEncoder(unittest.TestCase):
    """编码器测试"""
    
    def test_basic_encoding(self):
        """测试基础级别编码"""
        encoder = LeetSpeakEncoder(level='basic')
        result = encoder.encode("hello")
        # h -> h, e -> 3, l -> 1, l -> 1, o -> 0
        self.assertIn('3', result)  # e -> 3
        self.assertIn('1', result)  # l -> 1
        self.assertIn('0', result)  # o -> 0
    
    def test_standard_encoding(self):
        """测试标准级别编码"""
        encoder = LeetSpeakEncoder(level='standard')
        result = encoder.encode("leet")
        self.assertIn('3', result)  # e -> 3
        self.assertIn('7', result)  # t -> 7
    
    def test_advanced_encoding(self):
        """测试高级级别编码"""
        encoder = LeetSpeakEncoder(level='advanced')
        result = encoder.encode("hacker")
        # 应该包含更多特殊字符
        self.assertNotEqual(result, "hacker")
    
    def test_preserve_non_alpha(self):
        """测试保留非字母字符"""
        encoder = LeetSpeakEncoder(level='basic')
        result = encoder.encode("Hello, World! 123")
        self.assertIn(',', result)
        self.assertIn('!', result)
        self.assertIn('123', result)
    
    def test_empty_string(self):
        """测试空字符串"""
        encoder = LeetSpeakEncoder(level='basic')
        result = encoder.encode("")
        self.assertEqual(result, "")
    
    def test_randomize_encoding(self):
        """测试随机编码"""
        encoder = LeetSpeakEncoder(level='standard')
        # 使用固定种子，结果应该可重现
        result1 = encoder.encode("elite", randomize=True, seed=42)
        result2 = encoder.encode("elite", randomize=True, seed=42)
        self.assertEqual(result1, result2)
    
    def test_custom_map(self):
        """测试自定义映射"""
        custom_map = {'x': ['X', 'XX'], 'y': ['Y']}
        encoder = LeetSpeakEncoder(level='basic', custom_map=custom_map)
        result = encoder.encode("xyz")
        self.assertIn('X', result)  # x should be replaced
    
    def test_encode_word_variants(self):
        """测试单词变体生成"""
        encoder = LeetSpeakEncoder(level='standard')
        variants = encoder.encode_word_variants("leet", max_variants=10)
        self.assertIsInstance(variants, list)
        self.assertTrue(len(variants) > 0)
        # 所有变体都应该不是原始单词
        for v in variants:
            self.assertNotEqual(v, "leet")


class TestLeetSpeakDecoder(unittest.TestCase):
    """解码器测试"""
    
    def test_basic_decoding(self):
        """测试基础级别解码"""
        decoder = LeetSpeakDecoder(level='basic')
        result = decoder.decode("h3ll0")
        self.assertEqual(result.lower(), "hello")
    
    def test_standard_decoding(self):
        """测试标准级别解码"""
        decoder = LeetSpeakDecoder(level='standard')
        result = decoder.decode("l33t")
        self.assertEqual(result.lower(), "leet")
    
    def test_preserve_non_leet(self):
        """测试保留非leet字符"""
        decoder = LeetSpeakDecoder(level='basic')
        result = decoder.decode("H3ll0, W0rld!")
        self.assertIn(',', result)
        # 注意: ! 在某些级别中可能被解码，这里测试空格和逗号
        self.assertIn(' ', result)
    
    def test_decode_all_possible(self):
        """测试所有可能解码"""
        decoder = LeetSpeakDecoder(level='standard')
        results = decoder.decode_all_possible("l33t")
        self.assertIsInstance(results, list)
        self.assertTrue(any('leet' in r.lower() for r in results))
    
    def test_empty_string(self):
        """测试空字符串解码"""
        decoder = LeetSpeakDecoder(level='basic')
        result = decoder.decode("")
        self.assertEqual(result, "")


class TestUtilityFunctions(unittest.TestCase):
    """工具函数测试"""
    
    def test_encode_function(self):
        """测试 encode 函数"""
        result = encode("leet", level='basic')
        self.assertIn('3', result)
        self.assertIn('0', result) if 'o' in "leet" else None
    
    def test_decode_function(self):
        """测试 decode 函数"""
        result = decode("l33t", level='standard')
        self.assertEqual(result.lower(), "leet")
    
    def test_is_leet_detection(self):
        """测试 Leet 检测"""
        self.assertTrue(is_leet("l33t h4ck3r"))
        self.assertTrue(is_leet("H3LL0"))
        self.assertFalse(is_leet("hello world"))
        self.assertFalse(is_leet("normal text"))
    
    def test_is_leet_threshold(self):
        """测试 Leet 检测阈值"""
        # 高比例应该检测到
        self.assertTrue(is_leet("12345678", threshold=0.5))
        # 低比例不应该检测到
        self.assertFalse(is_leet("hello world", threshold=0.5))
    
    def test_detect_level(self):
        """测试级别检测"""
        self.assertEqual(detect_level("h3ll0"), 'basic')
        self.assertEqual(detect_level("l33t @h4ck3r"), 'standard')
        # advanced 级别包含更复杂的字符
        self.assertIn(detect_level("h4x0r"), ['basic', 'standard', 'advanced'])
    
    def test_to_from_leet_aliases(self):
        """测试别名函数"""
        self.assertEqual(to_leet("leet", level='basic'), encode("leet", level='basic'))
        self.assertEqual(from_leet("l33t", level='standard'), decode("l33t", level='standard'))


class TestLeetSpeakGenerator(unittest.TestCase):
    """生成器测试"""
    
    def test_generate_username_variants(self):
        """测试用户名变体生成"""
        generator = LeetSpeakGenerator()
        variants = generator.generate_username_variants("hacker", count=5)
        self.assertIsInstance(variants, list)
        self.assertTrue(len(variants) <= 5)
        # 应该至少有一些变体
        self.assertTrue(len(variants) > 0)
    
    def test_generate_password_hints(self):
        """测试密码提示生成"""
        generator = LeetSpeakGenerator()
        hints = generator.generate_password_hints("secret")
        self.assertIsInstance(hints, list)
        self.assertTrue(len(hints) == 3)  # basic, standard, advanced
        
        for variant, desc in hints:
            self.assertIsInstance(variant, str)
            self.assertIsInstance(desc, str)


class TestCreateCustomEncoder(unittest.TestCase):
    """自定义编码器测试"""
    
    def test_create_custom_encoder(self):
        """测试创建自定义编码器"""
        custom_map = {'a': ['@'], 'b': ['8']}
        encoder = create_custom_encoder(custom_map, base_level='basic')
        result = encoder.encode("abc")
        self.assertIn('@', result)  # a -> @
        self.assertIn('8', result)  # b -> 8


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_all_uppercase(self):
        """测试全大写"""
        encoder = LeetSpeakEncoder(level='basic')
        result = encoder.encode("HELLO")
        # 应该包含替换
        self.assertNotEqual(result, "HELLO")
    
    def test_mixed_case(self):
        """测试混合大小写"""
        encoder = LeetSpeakEncoder(level='basic')
        result = encoder.encode("HeLLo")
        self.assertIn('3', result)  # e -> 3
    
    def test_numbers_only(self):
        """测试纯数字"""
        encoder = LeetSpeakEncoder(level='basic')
        result = encoder.encode("12345")
        self.assertEqual(result, "12345")
    
    def test_special_chars_only(self):
        """测试纯特殊字符"""
        encoder = LeetSpeakEncoder(level='basic')
        result = encoder.encode("!@#$%")
        self.assertEqual(result, "!@#$%")
    
    def test_whitespace_preservation(self):
        """测试空白保留"""
        encoder = LeetSpeakEncoder(level='basic')
        result = encoder.encode("hello world")
        self.assertIn(' ', result)
    
    def test_unicode_characters(self):
        """测试Unicode字符"""
        encoder = LeetSpeakEncoder(level='basic')
        result = encoder.encode("hello 世界")
        self.assertIn('世界', result)
    
    def test_invalid_level(self):
        """测试无效级别"""
        encoder = LeetSpeakEncoder(level='invalid')
        result = encoder.encode("leet")
        # 应该使用默认级别
        self.assertIsInstance(result, str)


class TestRoundTrip(unittest.TestCase):
    """往返测试"""
    
    def test_roundtrip_basic(self):
        """测试基础级别往返（注意：leet speak有固有歧义，如l/i都映射到1）"""
        # 使用不包含歧义字符的单词
        original = "hate"  # h->h, a->4, t->7, e->3
        encoded = encode(original, level='basic')
        decoded = decode(encoded, level='basic')
        self.assertEqual(decoded.lower(), original)
    
    def test_roundtrip_standard(self):
        """测试标准级别往返（注意：leet speak有固有歧义）"""
        # 使用不包含歧义字符的单词
        original = "goes"  # g->6, o->0, e->3, s->5
        encoded = encode(original, level='standard')
        decoded = decode(encoded, level='standard')
        self.assertEqual(decoded.lower(), original)
    
    def test_roundtrip_preserves_structure(self):
        """测试往返保留文本结构"""
        original = "test"
        encoded = encode(original, level='basic')
        decoded = decode(encoded, level='basic')
        # 长度应该相同
        self.assertEqual(len(decoded), len(original))


if __name__ == '__main__':
    unittest.main(verbosity=2)