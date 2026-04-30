"""
Delta Encoding 工具模块测试
"""

import unittest
from datetime import datetime, timedelta
from mod import (
    DeltaEncoder,
    FloatDeltaEncoder,
    TimestampDeltaEncoder,
    DictionaryEncoder,
    DeltaEncodingStats,
    delta_encode,
    delta_decode,
    dict_encode,
    dict_decode
)


class TestDeltaEncoder(unittest.TestCase):
    """整数差分编码器测试"""
    
    def test_empty_sequence(self):
        """测试空序列"""
        encoder = DeltaEncoder()
        self.assertEqual(encoder.encode([]), [])
        self.assertEqual(encoder.decode([]), [])
    
    def test_single_element(self):
        """测试单元素序列"""
        encoder = DeltaEncoder()
        self.assertEqual(encoder.encode([42]), [42])
        self.assertEqual(encoder.decode([42]), [42])
    
    def test_constant_sequence(self):
        """测试常量序列（差分全为0）"""
        encoder = DeltaEncoder()
        values = [100, 100, 100, 100, 100]
        encoded = encoder.encode(values)
        expected = [100, 0, 0, 0, 0]  # ZigZag(0) = 0
        self.assertEqual(encoded, expected)
        self.assertEqual(encoder.decode(encoded), values)
    
    def test_increasing_sequence(self):
        """测试递增序列"""
        encoder = DeltaEncoder()
        values = [10, 20, 30, 40, 50]
        encoded = encoder.encode(values)
        # ZigZag: 10->20, 10->20
        expected = [10, 20, 20, 20, 20]  # ZigZag(10)=20
        self.assertEqual(encoded, expected)
        self.assertEqual(encoder.decode(encoded), values)
    
    def test_decreasing_sequence(self):
        """测试递减序列"""
        encoder = DeltaEncoder()
        values = [50, 40, 30, 20, 10]
        encoded = encoder.encode(values)
        decoded = encoder.decode(encoded)
        self.assertEqual(decoded, values)
    
    def test_mixed_sequence(self):
        """测试混合序列"""
        encoder = DeltaEncoder()
        values = [100, 105, 103, 110, 108, 115]
        encoded = encoder.encode(values)
        decoded = encoder.decode(encoded)
        self.assertEqual(decoded, values)
    
    def test_negative_values(self):
        """测试负值"""
        encoder = DeltaEncoder()
        values = [-10, -5, -15, 0, 10]
        encoded = encoder.encode(values)
        decoded = encoder.decode(encoded)
        self.assertEqual(decoded, values)
    
    def test_without_zigzag(self):
        """测试不使用 ZigZag 编码"""
        encoder = DeltaEncoder(use_zigzag=False)
        values = [100, 105, 100, 95, 110]
        encoded = encoder.encode(values)
        # 原始差分: [5, -5, -5, 15]
        expected = [100, 5, -5, -5, 15]
        self.assertEqual(encoded, expected)
        self.assertEqual(encoder.decode(encoded), values)
    
    def test_zigzag_encoding(self):
        """测试 ZigZag 编码"""
        # ZigZag: 负数映射到正奇数，正数映射到正偶数
        self.assertEqual(DeltaEncoder.zigzag_encode(0), 0)
        self.assertEqual(DeltaEncoder.zigzag_encode(1), 2)
        self.assertEqual(DeltaEncoder.zigzag_encode(-1), 1)
        self.assertEqual(DeltaEncoder.zigzag_encode(2), 4)
        self.assertEqual(DeltaEncoder.zigzag_encode(-2), 3)
        self.assertEqual(DeltaEncoder.zigzag_encode(100), 200)
        self.assertEqual(DeltaEncoder.zigzag_encode(-100), 199)
    
    def test_zigzag_decoding(self):
        """测试 ZigZag 解码"""
        self.assertEqual(DeltaEncoder.zigzag_decode(0), 0)
        self.assertEqual(DeltaEncoder.zigzag_decode(1), -1)
        self.assertEqual(DeltaEncoder.zigzag_decode(2), 1)
        self.assertEqual(DeltaEncoder.zigzag_decode(3), -2)
        self.assertEqual(DeltaEncoder.zigzag_decode(4), 2)
        self.assertEqual(DeltaEncoder.zigzag_decode(200), 100)
        self.assertEqual(DeltaEncoder.zigzag_decode(199), -100)
    
    def test_roundtrip(self):
        """测试编解码往返"""
        encoder = DeltaEncoder()
        test_cases = [
            [1, 2, 3, 4, 5],
            [100, 95, 100, 105, 95],
            [0, 1000, 500, 1500, 750],
            [-100, 0, 100, -50, 50]
        ]
        
        for values in test_cases:
            with self.subTest(values=values):
                encoded = encoder.encode(values)
                decoded = encoder.decode(encoded)
                self.assertEqual(decoded, values)


class TestFloatDeltaEncoder(unittest.TestCase):
    """浮点数 XOR 差分编码器测试"""
    
    def test_empty_sequence(self):
        """测试空序列"""
        encoder = FloatDeltaEncoder()
        self.assertEqual(encoder.encode([]), [])
        self.assertEqual(encoder.decode([]), [])
        self.assertEqual(encoder.encode_compact([]), {'first_value': None, 'xor_deltas': []})
        self.assertEqual(encoder.decode_compact({'first_value': None, 'xor_deltas': []}), [])
    
    def test_single_element(self):
        """测试单元素序列"""
        encoder = FloatDeltaEncoder()
        encoded = encoder.encode([3.14])
        self.assertEqual(len(encoded), 1)
        self.assertEqual(encoded[0][1], None)  # 第一个元素没有 XOR 差分
        decoded = encoder.decode(encoded)
        self.assertAlmostEqual(decoded[0], 3.14, places=10)
    
    def test_constant_sequence(self):
        """测试常量序列"""
        encoder = FloatDeltaEncoder()
        values = [2.5, 2.5, 2.5, 2.5]
        encoded = encoder.encode(values)
        
        # XOR 差分应该为 0（相同值的 XOR 为 0）
        for i in range(1, len(encoded)):
            self.assertEqual(encoded[i][1], 0)
        
        decoded = encoder.decode(encoded)
        for v1, v2 in zip(values, decoded):
            self.assertAlmostEqual(v1, v2, places=10)
    
    def test_increasing_sequence(self):
        """测试递增序列"""
        encoder = FloatDeltaEncoder()
        values = [1.0, 2.0, 3.0, 4.0, 5.0]
        encoded = encoder.encode(values)
        decoded = encoder.decode(encoded)
        
        for v1, v2 in zip(values, decoded):
            self.assertAlmostEqual(v1, v2, places=10)
    
    def test_compact_encoding(self):
        """测试紧凑编码"""
        encoder = FloatDeltaEncoder()
        values = [1.5, 1.5, 2.0, 2.0, 3.0]
        
        compact = encoder.encode_compact(values)
        self.assertIsNotNone(compact['first_value'])
        self.assertEqual(len(compact['xor_deltas']), len(values) - 1)
        
        decoded = encoder.decode_compact(compact)
        for v1, v2 in zip(values, decoded):
            self.assertAlmostEqual(v1, v2, places=10)
    
    def test_precision_preservation(self):
        """测试精度保持"""
        encoder = FloatDeltaEncoder()
        values = [0.1 + 0.2, 0.3 + 0.4, 0.5 + 0.6]  # 浮点精度测试
        
        encoded = encoder.encode(values)
        decoded = encoder.decode(encoded)
        
        for v1, v2 in zip(values, decoded):
            self.assertEqual(v1, v2)  # 精确相等，因为 XOR 保持精确
    
    def test_negative_values(self):
        """测试负值"""
        encoder = FloatDeltaEncoder()
        values = [-1.5, -2.5, -1.0, 0.0, 1.0]
        encoded = encoder.encode(values)
        decoded = encoder.decode(encoded)
        
        for v1, v2 in zip(values, decoded):
            self.assertAlmostEqual(v1, v2, places=10)


class TestTimestampDeltaEncoder(unittest.TestCase):
    """时间戳差分编码器测试"""
    
    def test_empty_sequence(self):
        """测试空序列"""
        encoder = TimestampDeltaEncoder()
        base_ts, deltas = encoder.encode([])
        self.assertEqual(base_ts, 0)
        self.assertEqual(deltas, [])
        self.assertEqual(encoder.decode(0, []), [])
    
    def test_single_timestamp(self):
        """测试单个时间戳"""
        encoder = TimestampDeltaEncoder()
        dt = datetime(2024, 1, 1, 12, 0, 0)
        base_ts, deltas = encoder.encode([dt])
        
        self.assertGreater(base_ts, 0)
        self.assertEqual(deltas, [0])
        
        decoded = encoder.decode(base_ts, deltas)
        self.assertEqual(len(decoded), 1)
        self.assertEqual(decoded[0], dt)
    
    def test_regular_intervals(self):
        """测试等间隔时间戳"""
        encoder = TimestampDeltaEncoder()
        base = datetime(2024, 1, 1, 0, 0, 0)
        datetimes = [base + timedelta(seconds=i) for i in range(5)]
        
        base_ts, deltas = encoder.encode(datetimes)
        
        # 差分应该全部相同（除了第一个）
        self.assertEqual(len(deltas), 5)
        self.assertEqual(deltas[0], 0)  # 第一个为 0
        
        # 检查等间隔（毫秒单位）
        for i in range(1, len(deltas)):
            self.assertEqual(deltas[i], 1000)  # 1秒 = 1000毫秒
        
        decoded = encoder.decode(base_ts, deltas)
        self.assertEqual(decoded, datetimes)
    
    def test_irregular_intervals(self):
        """测试不等间隔时间戳"""
        encoder = TimestampDeltaEncoder()
        datetimes = [
            datetime(2024, 1, 1, 0, 0, 0),
            datetime(2024, 1, 1, 0, 0, 5),
            datetime(2024, 1, 1, 0, 0, 7),
            datetime(2024, 1, 1, 0, 1, 0)
        ]
        
        base_ts, deltas = encoder.encode(datetimes)
        decoded = encoder.decode(base_ts, deltas)
        
        self.assertEqual(decoded, datetimes)
    
    def test_different_units(self):
        """测试不同时间单位"""
        # 秒级
        encoder_s = TimestampDeltaEncoder(unit='s')
        datetimes = [datetime(2024, 1, 1, 0, 0, i) for i in range(3)]
        base_s, deltas_s = encoder_s.encode(datetimes)
        self.assertEqual(deltas_s[1], 1)
        self.assertEqual(deltas_s[2], 1)
        
        # 微秒级
        encoder_us = TimestampDeltaEncoder(unit='us')
        base_us, deltas_us = encoder_us.encode(datetimes)
        self.assertEqual(deltas_us[1], 1000000)  # 1秒 = 1000000微秒
    
    def test_delta_of_delta_encoding(self):
        """测试二阶差分编码"""
        encoder = TimestampDeltaEncoder()
        base = datetime(2024, 1, 1, 0, 0, 0)
        
        # 等间隔序列的二阶差分应该全部为 0
        datetimes = [base + timedelta(seconds=i) for i in range(5)]
        encoded = encoder.encode_with_delta_of_delta(datetimes)
        
        # 对于 N 个元素，二阶差分有 N-1 个（第一个是 0，后面 N-2 个是相邻差分的差）
        self.assertEqual(len(encoded['dod']), 4)  # 5 个元素 -> 4 个一阶差分 -> 4 个二阶差分
        self.assertEqual(encoded['first_delta'], 1000)  # 毫秒
        
        # 等间隔时，二阶差分除第一个外都应为 0
        self.assertEqual(encoded['dod'][0], 0)  # 第一个二阶差分默认为 0
        for i in range(1, len(encoded['dod'])):
            self.assertEqual(encoded['dod'][i], 0)
        
        # 解码
        decoded = encoder.decode_with_delta_of_delta(encoded)
        self.assertEqual(decoded, datetimes)
    
    def test_delta_of_delta_irregular(self):
        """测试不等间隔的二阶差分编码"""
        encoder = TimestampDeltaEncoder()
        datetimes = [
            datetime(2024, 1, 1, 0, 0, 0),
            datetime(2024, 1, 1, 0, 0, 10),
            datetime(2024, 1, 1, 0, 0, 15),  # 间隔从 10 变为 5
            datetime(2024, 1, 1, 0, 0, 25),  # 间隔从 5 变为 10
        ]
        
        encoded = encoder.encode_with_delta_of_delta(datetimes)
        decoded = encoder.decode_with_delta_of_delta(encoded)
        
        self.assertEqual(decoded, datetimes)


class TestDictionaryEncoder(unittest.TestCase):
    """字典编码器测试"""
    
    def test_empty_sequence(self):
        """测试空序列"""
        encoder = DictionaryEncoder()
        ids, dictionary = encoder.encode([])
        self.assertEqual(ids, [])
        self.assertEqual(dictionary, {})
    
    def test_unique_strings(self):
        """测试唯一字符串序列"""
        encoder = DictionaryEncoder()
        strings = ['apple', 'banana', 'cherry']
        ids, dictionary = encoder.encode(strings)
        
        self.assertEqual(len(ids), 3)
        self.assertEqual(len(dictionary), 3)
        self.assertEqual(len(set(ids)), 3)  # 所有 ID 唯一
        
        decoded = encoder.decode(ids)
        self.assertEqual(decoded, strings)
    
    def test_duplicate_strings(self):
        """测试重复字符串序列"""
        encoder = DictionaryEncoder()
        strings = ['apple', 'banana', 'apple', 'apple', 'banana']
        ids, dictionary = encoder.encode(strings)
        
        self.assertEqual(len(ids), 5)
        self.assertEqual(len(dictionary), 2)  # 只有 2 个唯一字符串
        self.assertEqual(ids[0], ids[2])  # 'apple' ID 相同
        self.assertEqual(ids[0], ids[3])  # 'apple' ID 相同
        self.assertEqual(ids[1], ids[4])  # 'banana' ID 相同
        
        decoded = encoder.decode(ids)
        self.assertEqual(decoded, strings)
    
    def test_id_assignment(self):
        """测试 ID 按出现顺序分配"""
        encoder = DictionaryEncoder()
        strings = ['first', 'second', 'third']
        ids, dictionary = encoder.encode(strings)
        
        # 验证 ID 按顺序分配
        self.assertEqual(dictionary['first'], 0)
        self.assertEqual(dictionary['second'], 1)
        self.assertEqual(dictionary['third'], 2)
    
    def test_decode_with_external_dictionary(self):
        """测试使用外部字典解码"""
        encoder = DictionaryEncoder()
        ids, dictionary = encoder.encode(['a', 'b', 'c'])
        
        # 使用返回的字典解码
        new_encoder = DictionaryEncoder()
        decoded = new_encoder.decode(ids, dictionary)
        self.assertEqual(decoded, ['a', 'b', 'c'])
    
    def test_get_dictionary(self):
        """测试获取字典"""
        encoder = DictionaryEncoder()
        encoder.encode(['x', 'y', 'z'])
        
        dictionary = encoder.get_dictionary()
        self.assertIn('x', dictionary)
        self.assertIn('y', dictionary)
        self.assertIn('z', dictionary)
    
    def test_vocabulary_size(self):
        """测试词汇表大小"""
        encoder = DictionaryEncoder()
        self.assertEqual(encoder.get_vocabulary_size(), 0)
        
        encoder.encode(['a', 'b', 'a', 'c', 'b'])
        self.assertEqual(encoder.get_vocabulary_size(), 3)
    
    def test_clear(self):
        """测试清空字典"""
        encoder = DictionaryEncoder()
        encoder.encode(['a', 'b', 'c'])
        self.assertEqual(encoder.get_vocabulary_size(), 3)
        
        encoder.clear()
        self.assertEqual(encoder.get_vocabulary_size(), 0)
        
        # 再次编码，ID 应该从 0 开始
        ids, _ = encoder.encode(['x', 'y'])
        self.assertEqual(ids, [0, 1])
    
    def test_unicode_strings(self):
        """测试 Unicode 字符串"""
        encoder = DictionaryEncoder()
        strings = ['你好', '世界', '你好', '🎉', '世界']
        ids, dictionary = encoder.encode(strings)
        
        self.assertEqual(len(dictionary), 3)
        decoded = encoder.decode(ids)
        self.assertEqual(decoded, strings)


class TestDeltaEncodingStats(unittest.TestCase):
    """差分编码统计测试"""
    
    def test_analyze_empty_integers(self):
        """测试空整数序列分析"""
        stats = DeltaEncodingStats.analyze_integers([])
        self.assertEqual(stats['original_count'], 0)
        self.assertEqual(stats['original_size_bytes'], 0)
        self.assertEqual(stats['compression_ratio'], 0)
    
    def test_analyze_constant_sequence(self):
        """测试常量序列分析"""
        stats = DeltaEncodingStats.analyze_integers([100, 100, 100, 100, 100])
        
        self.assertEqual(stats['original_count'], 5)
        self.assertEqual(stats['avg_delta'], 0)
        self.assertEqual(stats['max_delta'], 0)
        self.assertEqual(stats['min_delta'], 0)
        # 常量序列压缩效果应该很好
        self.assertGreater(stats['compression_ratio'], 1)
    
    def test_analyze_small_deltas(self):
        """测试小差分序列"""
        stats = DeltaEncodingStats.analyze_integers([100, 101, 102, 103, 104])
        
        self.assertEqual(stats['avg_delta'], 1)
        self.assertEqual(stats['max_delta'], 1)
        self.assertEqual(stats['min_delta'], 1)
        # 小差分压缩效果好
        self.assertGreater(stats['compression_ratio'], 1)
    
    def test_analyze_large_deltas(self):
        """测试大差分序列"""
        stats = DeltaEncodingStats.analyze_integers([0, 1000000, 2000000, 3000000])
        
        self.assertEqual(stats['avg_delta'], 1000000)
        self.assertEqual(stats['max_delta'], 1000000)
        self.assertEqual(stats['min_delta'], 1000000)
    
    def test_analyze_empty_strings(self):
        """测试空字符串序列分析"""
        stats = DeltaEncodingStats.analyze_strings([])
        self.assertEqual(stats['original_count'], 0)
        self.assertEqual(stats['unique_count'], 0)
        self.assertEqual(stats['redundancy_ratio'], 0)
    
    def test_analyze_unique_strings(self):
        """测试唯一字符串分析"""
        stats = DeltaEncodingStats.analyze_strings(['a', 'b', 'c', 'd'])
        
        self.assertEqual(stats['original_count'], 4)
        self.assertEqual(stats['unique_count'], 4)
        self.assertEqual(stats['redundancy_ratio'], 0)
    
    def test_analyze_redundant_strings(self):
        """测试冗余字符串分析"""
        stats = DeltaEncodingStats.analyze_strings(['a', 'a', 'a', 'a'])
        
        self.assertEqual(stats['original_count'], 4)
        self.assertEqual(stats['unique_count'], 1)
        self.assertEqual(stats['redundancy_ratio'], 0.75)  # 75% 冗余
    
    def test_analyze_mixed_strings(self):
        """测试混合字符串分析"""
        stats = DeltaEncodingStats.analyze_strings(['apple', 'banana', 'apple', 'cherry', 'banana', 'apple'])
        
        self.assertEqual(stats['original_count'], 6)
        self.assertEqual(stats['unique_count'], 3)
        # 6个元素，3个唯一，冗余率 = (6-3)/6 = 0.5
        self.assertEqual(stats['redundancy_ratio'], 0.5)


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_delta_encode_decode(self):
        """测试 delta_encode 和 delta_decode 函数"""
        values = [100, 105, 110, 108, 115]
        encoded = delta_encode(values)
        decoded = delta_decode(encoded)
        self.assertEqual(decoded, values)
    
    def test_delta_encode_decode_without_zigzag(self):
        """测试不使用 ZigZag 的便捷函数"""
        values = [100, 95, 105, 90, 110]
        encoded = delta_encode(values, use_zigzag=False)
        decoded = delta_decode(encoded, use_zigzag=False)
        self.assertEqual(decoded, values)
    
    def test_dict_encode_decode(self):
        """测试 dict_encode 和 dict_decode 函数"""
        strings = ['x', 'y', 'x', 'z', 'y']
        ids, dictionary = dict_encode(strings)
        decoded = dict_decode(ids, dictionary)
        self.assertEqual(decoded, strings)


if __name__ == "__main__":
    unittest.main()