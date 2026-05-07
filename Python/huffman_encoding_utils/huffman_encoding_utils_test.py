"""
Huffman Encoding Utils 测试文件

包含完整的单元测试，验证编码器各项功能
"""

import unittest
from huffman_encoding_utils import (
    HuffmanEncoder,
    HuffmanNode,
    huffman_encode,
    huffman_decode,
    analyze_text,
    compare_with_fixed_encoding
)


class TestHuffmanNode(unittest.TestCase):
    """测试哈夫曼节点"""
    
    def test_leaf_node(self):
        """测试叶子节点"""
        node = HuffmanNode(char='a', freq=10)
        self.assertTrue(node.is_leaf())
        self.assertEqual(node.char, 'a')
        self.assertEqual(node.freq, 10)
    
    def test_internal_node(self):
        """测试内部节点"""
        left = HuffmanNode(char='a', freq=5)
        right = HuffmanNode(char='b', freq=5)
        root = HuffmanNode(char=None, freq=10, left=left, right=right)
        
        self.assertFalse(root.is_leaf())
        self.assertIsNone(root.char)
        self.assertEqual(root.freq, 10)
    
    def test_comparison(self):
        """测试节点比较"""
        node1 = HuffmanNode(char='a', freq=5)
        node2 = HuffmanNode(char='b', freq=10)
        
        self.assertTrue(node1 < node2)
        self.assertFalse(node2 < node1)


class TestHuffmanEncoder(unittest.TestCase):
    """测试哈夫曼编码器"""
    
    def test_build_tree_simple(self):
        """测试简单文本的树构建"""
        encoder = HuffmanEncoder()
        root = encoder.build_tree("aab")
        
        self.assertIsNotNone(root)
        self.assertEqual(root.freq, 3)
    
    def test_build_tree_single_char(self):
        """测试单字符文本"""
        encoder = HuffmanEncoder()
        root = encoder.build_tree("aaaaa")
        
        self.assertIsNotNone(root)
        self.assertEqual(len(encoder.codes), 1)
        self.assertEqual(encoder.codes['a'], '0')
    
    def test_build_tree_empty(self):
        """测试空文本"""
        encoder = HuffmanEncoder()
        
        with self.assertRaises(ValueError):
            encoder.build_tree("")
    
    def test_encode_decode_basic(self):
        """测试基本编解码"""
        text = "this is a test"
        
        encoder = HuffmanEncoder()
        encoded = encoder.encode(text)
        decoded = encoder.decode(encoded)
        
        self.assertEqual(decoded, text)
    
    def test_encode_decode_chinese(self):
        """测试中文编解码"""
        text = "你好世界，这是一个测试"
        
        encoder = HuffmanEncoder()
        encoded = encoder.encode(text)
        decoded = encoder.decode(encoded)
        
        self.assertEqual(decoded, text)
    
    def test_encode_decode_special_chars(self):
        """测试特殊字符编解码"""
        text = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        
        encoder = HuffmanEncoder()
        encoded = encoder.encode(text)
        decoded = encoder.decode(encoded)
        
        self.assertEqual(decoded, text)
    
    def test_encode_decode_long_text(self):
        """测试长文本编解码"""
        text = "The quick brown fox jumps over the lazy dog. " * 100
        
        encoder = HuffmanEncoder()
        encoded = encoder.encode(text)
        decoded = encoder.decode(encoded)
        
        self.assertEqual(decoded, text)
    
    def test_get_frequency_table(self):
        """测试频率表生成"""
        encoder = HuffmanEncoder()
        freq_table = encoder.get_frequency_table("aabbbc")
        
        self.assertEqual(freq_table['a'], (2, 33.33333333333333))
        self.assertEqual(freq_table['b'], (3, 50.0))
        self.assertEqual(freq_table['c'], (1, 16.666666666666664))
    
    def test_get_code_table(self):
        """测试编码表获取"""
        encoder = HuffmanEncoder()
        encoder.build_tree("aab")
        
        codes = encoder.get_code_table()
        
        self.assertEqual(len(codes), 2)
        self.assertIn('a', codes)
        self.assertIn('b', codes)
    
    def test_compression_stats(self):
        """测试压缩统计"""
        text = "aaaaabbbbbcccccddddeee"  # 22字符
        encoder = HuffmanEncoder()
        stats = encoder.calculate_compression_stats(text)
        
        self.assertEqual(stats['original_size_bits'], 22 * 8)
        self.assertGreater(stats['encoded_size_bits'], 0)
        self.assertGreater(stats['compression_ratio'], 0)
        self.assertLess(stats['compression_ratio'], 1)
        self.assertGreater(stats['space_saved_percent'], 0)
        self.assertGreater(stats['average_code_length'], 0)
        self.assertEqual(stats['unique_characters'], 5)  # a, b, c, d, e
    
    def test_visualize_tree(self):
        """测试树可视化"""
        encoder = HuffmanEncoder()
        encoder.build_tree("aab")
        
        visualization = encoder.visualize_tree()
        
        self.assertIsInstance(visualization, str)
        self.assertIn('(', visualization)  # 包含频率标记
    
    def test_serialization(self):
        """测试序列化和反序列化"""
        text = "hello world"
        encoder = HuffmanEncoder()
        encoder.build_tree(text)
        
        # 序列化
        data = encoder.to_dict()
        
        # 反序列化
        restored = HuffmanEncoder.from_dict(data)
        
        # 验证编解码一致
        encoded1 = encoder.encode(text)
        encoded2 = restored.encode(text)
        
        self.assertEqual(encoder.codes, restored.codes)
    
    def test_decode_without_tree(self):
        """测试未构建树时解码"""
        encoder = HuffmanEncoder()
        
        with self.assertRaises(ValueError):
            encoder.decode("010101")


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_huffman_encode(self):
        """测试快捷编码函数"""
        text = "test encoding"
        encoded, encoder = huffman_encode(text)
        
        self.assertIsInstance(encoded, str)
        self.assertIsInstance(encoder, HuffmanEncoder)
        self.assertTrue(all(c in '01' for c in encoded))
    
    def test_huffman_decode(self):
        """测试快捷解码函数"""
        text = "test decoding"
        encoded, encoder = huffman_encode(text)
        decoded = huffman_decode(encoded, encoder)
        
        self.assertEqual(decoded, text)
    
    def test_analyze_text(self):
        """测试文本分析函数"""
        text = "aaaaabbbbbccccc"
        analysis = analyze_text(text)
        
        self.assertIn('text_length', analysis)
        self.assertIn('frequency_table', analysis)
        self.assertIn('code_table', analysis)
        self.assertIn('compression_stats', analysis)
        self.assertIn('tree_visualization', analysis)
        
        self.assertEqual(analysis['text_length'], 15)
        self.assertEqual(len(analysis['frequency_table']), 3)
    
    def test_compare_with_fixed_encoding(self):
        """测试与固定长度编码比较"""
        text = "aabbbc"  # 3种不同字符
        comparison = compare_with_fixed_encoding(text)
        
        self.assertIn('huffman_bits', comparison)
        self.assertIn('fixed_bits', comparison)
        self.assertIn('huffman_avg_length', comparison)
        self.assertIn('fixed_bits_per_char', comparison)
        self.assertIn('huffman_savings_vs_fixed', comparison)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_repeated_char(self):
        """测试重复字符"""
        text = "aaaaaaaa"
        encoder = HuffmanEncoder()
        encoded = encoder.encode(text)
        decoded = encoder.decode(encoded)
        
        self.assertEqual(decoded, text)
    
    def test_binary_pattern(self):
        """测试二进制模式文本"""
        text = "01010101"
        encoder = HuffmanEncoder()
        encoded = encoder.encode(text)
        decoded = encoder.decode(encoded)
        
        self.assertEqual(decoded, text)
    
    def test_whitespace_only(self):
        """测试纯空白文本"""
        text = "   \t\n\r  "
        encoder = HuffmanEncoder()
        encoded = encoder.encode(text)
        decoded = encoder.decode(encoded)
        
        self.assertEqual(decoded, text)
    
    def test_unicode_emoji(self):
        """测试Unicode表情"""
        text = "Hello 👋 World 🌍 Test 🧪"
        encoder = HuffmanEncoder()
        encoded = encoder.encode(text)
        decoded = encoder.decode(encoded)
        
        self.assertEqual(decoded, text)
    
    def test_mixed_case(self):
        """测试混合大小写"""
        text = "AbCdEfGhIjKlMnOpQrStUvWxYz"
        encoder = HuffmanEncoder()
        encoded = encoder.encode(text)
        decoded = encoder.decode(encoded)
        
        self.assertEqual(decoded, text)
    
    def test_numbers(self):
        """测试数字"""
        text = "0123456789" * 10
        encoder = HuffmanEncoder()
        encoded = encoder.encode(text)
        decoded = encoder.decode(encoded)
        
        self.assertEqual(decoded, text)


class TestPerformance(unittest.TestCase):
    """测试性能"""
    
    def test_large_text(self):
        """测试大文本处理"""
        import random
        import string
        
        # 生成10000个随机字符
        text = ''.join(random.choices(string.ascii_letters + string.digits, k=10000))
        
        encoder = HuffmanEncoder()
        encoded = encoder.encode(text)
        decoded = encoder.decode(encoded)
        
        self.assertEqual(decoded, text)
        self.assertGreater(len(encoded), 0)
    
    def test_many_unique_chars(self):
        """测试大量不同字符"""
        # 生成所有可打印ASCII字符
        text = ''.join(chr(i) for i in range(32, 127))
        
        encoder = HuffmanEncoder()
        encoded = encoder.encode(text)
        decoded = encoder.decode(encoded)
        
        self.assertEqual(decoded, text)


if __name__ == '__main__':
    unittest.main(verbosity=2)