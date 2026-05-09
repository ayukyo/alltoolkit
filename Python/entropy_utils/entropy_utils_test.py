#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - 熵计算工具模块测试
Entropy Utilities Test Suite

@module: entropy_utils
"""

import sys
import os
import math
import tempfile
import unittest

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    EntropyUtils, PasswordEntropy, PasswordAnalysis, DataEntropyAnalyzer,
    shannon_entropy, analyze_password, entropy_report
)


class TestEntropyUtils(unittest.TestCase):
    """测试 EntropyUtils 类"""
    
    def test_shannon_entropy_empty(self):
        """测试空数据"""
        self.assertEqual(EntropyUtils.shannon_entropy(""), 0.0)
        self.assertEqual(EntropyUtils.shannon_entropy([]), 0.0)
        self.assertEqual(EntropyUtils.shannon_entropy(b""), 0.0)
    
    def test_shannon_entropy_single_char(self):
        """测试单字符"""
        self.assertEqual(EntropyUtils.shannon_entropy("a"), 0.0)
        self.assertEqual(EntropyUtils.shannon_entropy("aaaaaa"), 0.0)
    
    def test_shannon_entropy_uniform(self):
        """测试均匀分布"""
        # "ab" 应该有熵 1.0 (每个字符概率0.5, -log2(0.5)=1)
        self.assertAlmostEqual(EntropyUtils.shannon_entropy("ab"), 1.0, places=10)
        # "abc" 应该有熵 ~1.585 (log2(3))
        self.assertAlmostEqual(EntropyUtils.shannon_entropy("abc"), math.log2(3), places=10)
    
    def test_shannon_entropy_general(self):
        """测试一般情况"""
        # "aabb" 每个字符概率0.5, 熵应该是1.0
        self.assertAlmostEqual(EntropyUtils.shannon_entropy("aabb"), 1.0, places=10)
        # "aab" p(a)=2/3, p(b)=1/3
        expected = -(2/3) * math.log2(2/3) - (1/3) * math.log2(1/3)
        self.assertAlmostEqual(EntropyUtils.shannon_entropy("aab"), expected, places=10)
    
    def test_shannon_entropy_bytes(self):
        """测试字节数据"""
        data = b"\x00\x01\x02\x03"
        entropy = EntropyUtils.shannon_entropy(data)
        self.assertAlmostEqual(entropy, 2.0, places=10)
    
    def test_shannon_entropy_list(self):
        """测试列表数据"""
        data = [1, 1, 2, 2, 3, 3]
        entropy = EntropyUtils.shannon_entropy(data)
        self.assertAlmostEqual(entropy, math.log2(3), places=10)
    
    def test_shannon_entropy_normalized(self):
        """测试归一化熵"""
        # 均匀分布应该归一化为1
        self.assertAlmostEqual(EntropyUtils.shannon_entropy_normalized("ab"), 1.0, places=10)
        self.assertAlmostEqual(EntropyUtils.shannon_entropy_normalized("abc"), 1.0, places=10)
        # 单字符应该为0
        self.assertEqual(EntropyUtils.shannon_entropy_normalized("a"), 0.0)
    
    def test_renyi_entropy(self):
        """测试Rényi熵"""
        data = "aab"
        
        # α=0: Hartley熵 = log2(|X|)
        renyi_0 = EntropyUtils.renyi_entropy(data, 0)
        self.assertAlmostEqual(renyi_0, math.log2(2), places=10)  # 2个唯一符号
        
        # α=1: 应该等于香农熵
        renyi_1 = EntropyUtils.renyi_entropy(data, 1)
        shannon = EntropyUtils.shannon_entropy(data)
        self.assertAlmostEqual(renyi_1, shannon, places=10)
        
        # α=2: 碰撞熵
        renyi_2 = EntropyUtils.renyi_entropy(data, 2)
        self.assertTrue(renyi_2 > 0)
    
    def test_min_entropy(self):
        """测试最小熵"""
        # "aaa" 最小熵应该是0（最大概率为1）
        self.assertEqual(EntropyUtils.min_entropy("aaa"), 0.0)
        # "ab" 最小熵应该是1（最大概率为0.5，-log2(0.5)=1）
        self.assertAlmostEqual(EntropyUtils.min_entropy("ab"), 1.0, places=10)
        # "aab" 最小概率是2/3
        self.assertAlmostEqual(EntropyUtils.min_entropy("aab"), -math.log2(2/3), places=10)
    
    def test_gini_impurity(self):
        """测试基尼不纯度"""
        # 单一类别
        self.assertAlmostEqual(EntropyUtils.gini_impurity("aaa"), 0.0, places=10)
        # 均匀分布
        self.assertAlmostEqual(EntropyUtils.gini_impurity("ab"), 0.5, places=10)
        # 三个均匀类别
        expected = 1 - 3 * (1/3) ** 2
        self.assertAlmostEqual(EntropyUtils.gini_impurity("abc"), expected, places=10)
    
    def test_kl_divergence(self):
        """测试KL散度"""
        p = {'A': 0.5, 'B': 0.5}
        q = {'A': 0.5, 'B': 0.5}
        # 相同分布KL散度为0
        self.assertAlmostEqual(EntropyUtils.kl_divergence(p, q), 0.0, places=10)
        
        p = {'A': 0.5, 'B': 0.5}
        q = {'A': 0.7, 'B': 0.3}
        kl = EntropyUtils.kl_divergence(p, q)
        self.assertTrue(kl > 0)
        
        # KL散度非对称性
        kl_reverse = EntropyUtils.kl_divergence(q, p)
        self.assertNotAlmostEqual(kl, kl_reverse, places=5)
    
    def test_kl_divergence_error(self):
        """测试KL散度错误情况"""
        p = {'A': 1.0}
        q = {'B': 1.0}  # q没有A
        with self.assertRaises(ValueError):
            EntropyUtils.kl_divergence(p, q)
    
    def test_cross_entropy(self):
        """测试交叉熵"""
        p = {'A': 0.5, 'B': 0.5}
        q = {'A': 0.5, 'B': 0.5}
        # 相同分布交叉熵等于香农熵
        ce = EntropyUtils.cross_entropy(p, q)
        shannon = EntropyUtils.shannon_entropy("AB")
        self.assertAlmostEqual(ce, shannon, places=10)
    
    def test_mutual_information(self):
        """测试互信息"""
        # 完全独立的变量
        x = [1, 2, 1, 2, 1, 2]
        y = [1, 1, 2, 2, 1, 1]
        mi = EntropyUtils.mutual_information(x, y)
        self.assertTrue(mi >= 0)
        
        # 完全相关的变量
        x = [1, 2, 3, 4, 5]
        y = [1, 2, 3, 4, 5]
        mi = EntropyUtils.mutual_information(x, y)
        h_x = EntropyUtils.shannon_entropy(x)
        self.assertAlmostEqual(mi, h_x, places=10)
    
    def test_mutual_information_error(self):
        """测试互信息错误情况"""
        with self.assertRaises(ValueError):
            EntropyUtils.mutual_information([1, 2], [1])
    
    def test_joint_entropy(self):
        """测试联合熵"""
        x = [1, 1, 2, 2]
        y = [1, 2, 1, 2]
        h_joint = EntropyUtils.joint_entropy(x, y)
        self.assertTrue(h_joint >= 0)
    
    def test_conditional_entropy(self):
        """测试条件熵"""
        # 如果X=Y，则H(X|Y)=0
        x = [1, 2, 3, 4]
        y = [1, 2, 3, 4]
        h_cond = EntropyUtils.conditional_entropy(x, y)
        self.assertAlmostEqual(h_cond, 0.0, places=10)
    
    def test_compression_potential(self):
        """测试压缩潜力"""
        # 高重复数据应该有高压缩潜力
        high_rep = "aaaaaaaaaa"
        self.assertGreater(EntropyUtils.compression_potential(high_rep), 0.8)
        
        # 随机数据应该有低压缩潜力
        random_data = "abcdefghij"
        self.assertLess(EntropyUtils.compression_potential(random_data), 0.5)
    
    def test_randomness_score(self):
        """测试随机性得分"""
        # 均匀随机数据得分应该较高
        score = EntropyUtils.randomness_score("abcdefghijklmnopqrstuvwxyz")
        self.assertGreater(score, 0.8)
        
        # 重复数据得分应该较低
        score = EntropyUtils.randomness_score("aaaaaaaaaa")
        self.assertLessEqual(score, 0.5)
    
    def test_file_entropy(self):
        """测试文件熵计算"""
        # 创建临时测试文件
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            # 写入均匀分布的字节
            f.write(bytes(range(256)))
            temp_path = f.name
        
        try:
            entropy = EntropyUtils.file_entropy(temp_path)
            # 256个不同字节，熵应该接近8
            self.assertAlmostEqual(entropy, 8.0, places=1)
        finally:
            os.unlink(temp_path)
    
    def test_analyze_distribution(self):
        """测试分布分析"""
        result = EntropyUtils.analyze_distribution("aabbc")
        
        self.assertIn('shannon_entropy', result)
        self.assertIn('min_entropy', result)
        self.assertIn('gini_impurity', result)
        self.assertIn('unique_count', result)
        self.assertIn('total_count', result)
        self.assertEqual(result['unique_count'], 3)
        self.assertEqual(result['total_count'], 5)


class TestPasswordEntropy(unittest.TestCase):
    """测试密码熵分析"""
    
    def setUp(self):
        """设置测试"""
        self.analyzer = PasswordEntropy()
    
    def test_charset_detection(self):
        """测试字符集检测"""
        self.assertEqual(self.analyzer.calculate_charset_size("abc"), 26)
        self.assertEqual(self.analyzer.calculate_charset_size("ABC"), 26)
        self.assertEqual(self.analyzer.calculate_charset_size("123"), 10)
        self.assertEqual(self.analyzer.calculate_charset_size("abcABC"), 52)
        self.assertEqual(self.analyzer.calculate_charset_size("abc123"), 36)
        self.assertEqual(self.analyzer.calculate_charset_size("abc123!"), 68)
    
    def test_entropy_calculation(self):
        """测试熵计算"""
        # 长度为6的纯小写密码
        entropy = self.analyzer.calculate_entropy("abcdef")
        expected = 6 * math.log2(26)
        self.assertAlmostEqual(entropy, expected, places=10)
        
        # 包含大小写和数字
        entropy = self.analyzer.calculate_entropy("Abc123")
        expected = 6 * math.log2(62)  # 26+26+10
        self.assertAlmostEqual(entropy, expected, places=10)
    
    def test_common_password_detection(self):
        """测试常见密码检测"""
        result = self.analyzer.analyze("password")
        self.assertTrue(result.is_common)
        
        result = self.analyzer.analyze("MyUniqueP@ss2024!")
        self.assertFalse(result.is_common)
    
    def test_password_strength_levels(self):
        """测试密码强度等级"""
        # 弱密码
        result = self.analyzer.analyze("123456")
        self.assertIn(result.strength, ["非常弱", "弱"])
        
        # 强密码
        result = self.analyzer.analyze("MyStr0ng!Pass#2024")
        self.assertIn(result.strength, ["强", "非常强"])
    
    def test_crack_time_estimate(self):
        """测试破解时间估计"""
        # 弱密码应该是瞬间
        time = self.analyzer.estimate_crack_time(10)
        self.assertEqual(time, "瞬间")
        
        # 中等熵值
        time = self.analyzer.estimate_crack_time(40)
        self.assertIn("秒", time)
        
        # 高熵值应该是年
        time = self.analyzer.estimate_crack_time(80)
        self.assertIn("年", time)
    
    def test_password_analysis_structure(self):
        """测试分析结果结构"""
        result = self.analyzer.analyze("Test123!")
        
        self.assertIsInstance(result, PasswordAnalysis)
        self.assertEqual(result.length, 8)
        self.assertTrue(result.has_lowercase)
        self.assertTrue(result.has_uppercase)
        self.assertTrue(result.has_digits)
        self.assertTrue(result.has_special)
        self.assertIsInstance(result.entropy, float)
        self.assertIsInstance(result.strength, str)
        self.assertIsInstance(result.suggestions, list)
    
    def test_pattern_detection(self):
        """测试模式检测"""
        patterns = self.analyzer.check_patterns("qwerty123")
        self.assertTrue(len(patterns) > 0)
        
        patterns = self.analyzer.check_patterns("abcd123")
        # 可能检测到键盘模式
    
    def test_suggestions(self):
        """测试改进建议"""
        result = self.analyzer.analyze("abc")
        self.assertTrue(len(result.suggestions) > 0)


class TestDataEntropyAnalyzer(unittest.TestCase):
    """测试数据熵分析器"""
    
    def setUp(self):
        """设置测试"""
        self.analyzer = DataEntropyAnalyzer(window_size=32)
    
    def test_analyze_sequence(self):
        """测试序列分析"""
        result = self.analyzer.analyze_sequence("hello world")
        
        self.assertIn('length', result)
        self.assertIn('unique_symbols', result)
        self.assertIn('shannon_entropy', result)
        self.assertIn('randomness_score', result)
        self.assertEqual(result['length'], 11)
    
    def test_analyze_sequence_empty(self):
        """测试空序列分析"""
        result = self.analyzer.analyze_sequence("")
        self.assertIn('error', result)
    
    def test_sliding_window_entropy(self):
        """测试滑动窗口熵"""
        # 创建测试数据：前半部分重复，后半部分随机
        data = b"aaaaaaaa" + b"abcdefgh"
        
        results = self.analyzer.sliding_window_entropy(data, step=8)
        
        self.assertIsInstance(results, list)
        if len(results) > 0:
            # 第一个窗口应该有低熵（重复）
            # 最后一个窗口应该有较高熵
            self.assertTrue(all(isinstance(r, tuple) and len(r) == 2 for r in results))
    
    def test_find_high_entropy_regions(self):
        """测试高熵区域检测"""
        # 创建测试数据 - 使用更长的重复区域和合适的窗口
        # 窗口大小为32，需要足够长的低熵和高熵区域
        low_entropy = b"a" * 64  # 两个窗口长度
        high_entropy_data = bytes(range(32)) * 8  # 高熵数据，足够长
        low_entropy2 = b"b" * 64
        
        data = low_entropy + high_entropy_data + low_entropy2
        
        regions = self.analyzer.find_high_entropy_regions(data, threshold=5.0, min_length=32)
        
        self.assertIsInstance(regions, list)
        # 应该检测到中间的高熵区域
        # 如果没检测到，检查数据是否确实有足够长度的高熵部分
        self.assertTrue(len(regions) > 0, f"No regions found for data length {len(data)}, window {self.analyzer.window_size}")


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_shannon_entropy_convenience(self):
        """测试便捷香农熵函数"""
        result = shannon_entropy("abc")
        expected = EntropyUtils.shannon_entropy("abc")
        self.assertAlmostEqual(result, expected, places=10)
    
    def test_analyze_password_convenience(self):
        """测试便捷密码分析函数"""
        result = analyze_password("Test123!")
        self.assertIsInstance(result, PasswordAnalysis)
    
    def test_entropy_report_convenience(self):
        """测试便捷熵报告函数"""
        result = entropy_report("hello")
        self.assertIn('shannon_entropy', result)
        self.assertIn('gini_impurity', result)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_unicode_support(self):
        """测试Unicode支持"""
        # 中文字符
        entropy = EntropyUtils.shannon_entropy("你好世界")
        self.assertTrue(entropy > 0)
        
        # 表情符号
        entropy = EntropyUtils.shannon_entropy("😀🎉🎊")
        self.assertTrue(entropy > 0)
    
    def test_large_data(self):
        """测试大数据"""
        # 生成大量数据
        data = list(range(1000))
        entropy = EntropyUtils.shannon_entropy(data)
        # 1000个唯一符号
        expected = math.log2(1000)
        self.assertAlmostEqual(entropy, expected, places=5)
    
    def test_binary_data(self):
        """测试二进制数据"""
        data = bytes(range(256))
        entropy = EntropyUtils.shannon_entropy(data)
        self.assertAlmostEqual(entropy, 8.0, places=10)
    
    def test_single_element(self):
        """测试单个元素"""
        entropy = EntropyUtils.shannon_entropy([1])
        self.assertEqual(entropy, 0.0)
    
    def test_type_handling(self):
        """测试类型处理"""
        # 字符串
        e1 = EntropyUtils.shannon_entropy("abc")
        # 列表
        e2 = EntropyUtils.shannon_entropy(['a', 'b', 'c'])
        # 应该相同
        self.assertAlmostEqual(e1, e2, places=10)


if __name__ == "__main__":
    # 运行测试
    unittest.main(verbosity=2)