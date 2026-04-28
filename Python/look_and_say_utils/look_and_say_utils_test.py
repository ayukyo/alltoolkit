"""
Look and Say Utils - 测试套件

测试外观数列工具的所有核心功能。
"""

import unittest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import LookAndSayUtils, next_term, generate, nth_term


class TestLookAndSayBasic(unittest.TestCase):
    """基础功能测试"""
    
    def test_next_term_basic(self):
        """测试基本下一项计算"""
        self.assertEqual(LookAndSayUtils.next_term("1"), "11")
        self.assertEqual(LookAndSayUtils.next_term("11"), "21")
        self.assertEqual(LookAndSayUtils.next_term("21"), "1211")
        self.assertEqual(LookAndSayUtils.next_term("1211"), "111221")
        self.assertEqual(LookAndSayUtils.next_term("111221"), "312211")
    
    def test_next_term_empty(self):
        """测试空字符串"""
        self.assertEqual(LookAndSayUtils.next_term(""), "")
    
    def test_next_term_single_digit(self):
        """测试单个数字"""
        self.assertEqual(LookAndSayUtils.next_term("2"), "12")
        self.assertEqual(LookAndSayUtils.next_term("3"), "13")
    
    def test_generate_basic(self):
        """测试生成数列"""
        terms = LookAndSayUtils.generate(5)
        expected = ["1", "11", "21", "1211", "111221"]
        self.assertEqual(terms, expected)
    
    def test_generate_zero(self):
        """测试生成0项"""
        self.assertEqual(LookAndSayUtils.generate(0), [])
    
    def test_generate_one(self):
        """测试生成1项"""
        self.assertEqual(LookAndSayUtils.generate(1), ["1"])
    
    def test_nth_term(self):
        """测试第n项"""
        self.assertEqual(LookAndSayUtils.nth_term(0), "1")
        self.assertEqual(LookAndSayUtils.nth_term(1), "11")
        self.assertEqual(LookAndSayUtils.nth_term(4), "111221")
    
    def test_nth_term_negative(self):
        """测试负数索引"""
        with self.assertRaises(ValueError):
            LookAndSayUtils.nth_term(-1)


class TestDifferentSeeds(unittest.TestCase):
    """不同种子测试"""
    
    def test_seed_22(self):
        """测试种子22（不动点）"""
        terms = LookAndSayUtils.generate(5, "22")
        self.assertEqual(terms, ["22", "22", "22", "22", "22"])
    
    def test_seed_3(self):
        """测试种子3"""
        terms = LookAndSayUtils.generate(4, "3")
        expected = ["3", "13", "1113", "3113"]
        self.assertEqual(terms, expected)
    
    def test_seed_111111(self):
        """测试种子111111"""
        terms = LookAndSayUtils.generate(3, "111111")
        self.assertEqual(terms[0], "111111")
        self.assertEqual(terms[1], "61")


class TestLengthAnalysis(unittest.TestCase):
    """长度分析测试"""
    
    def test_length_growth(self):
        """测试长度增长"""
        terms = LookAndSayUtils.generate(10)
        lengths = [len(t) for t in terms]
        # 长度应该单调非递减（除了开始可能相等）
        for i in range(2, len(lengths)):
            self.assertGreaterEqual(lengths[i], lengths[i-1])
    
    def test_length_ratio(self):
        """测试长度比趋近康威常数"""
        # 第10项的长度比应该接近康威常数
        ratio = LookAndSayUtils.length_ratio(10)
        self.assertGreater(ratio, 1.2)
        self.assertLess(ratio, 1.5)
    
    def test_length_ratio_bounds(self):
        """测试长度比边界"""
        # 康威常数约为 1.303577
        for n in range(5, 15):
            ratio = LookAndSayUtils.length_ratio(n)
            self.assertGreaterEqual(ratio, 1.0)
            self.assertLess(ratio, 2.0)
    
    def test_conway_constant_approximation(self):
        """测试康威常数近似"""
        approx = LookAndSayUtils.conway_constant_approximation(20)
        # 应该接近 1.303577（允许一定误差，因为早期项波动较大）
        self.assertGreater(approx, 1.2)
        self.assertLess(approx, 1.4)


class TestDigitAnalysis(unittest.TestCase):
    """数字分析测试"""
    
    def test_digit_frequency(self):
        """测试数字频率统计"""
        freq = LookAndSayUtils.digit_frequency("111221")
        self.assertEqual(freq["1"], 4)
        self.assertEqual(freq["2"], 2)
    
    def test_digit_distribution(self):
        """测试数字分布"""
        dist = LookAndSayUtils.digit_distribution(10)
        # 分布总和应为1
        total = sum(dist.values())
        self.assertAlmostEqual(total, 1.0, places=6)
    
    def test_count_unique_digits(self):
        """测试唯一数字计数"""
        counts = LookAndSayUtils.count_unique_digits(10)
        # 第一项只有1
        self.assertEqual(counts[0], 1)
        # 后续项最多有3种数字
        for count in counts:
            self.assertLessEqual(count, 3)
    
    def test_max_run_length(self):
        """测试最大连续长度"""
        self.assertEqual(LookAndSayUtils.max_run_length("111221"), 3)
        self.assertEqual(LookAndSayUtils.max_run_length("121212"), 1)
        self.assertEqual(LookAndSayUtils.max_run_length(""), 0)


class TestRunLengthEncoding(unittest.TestCase):
    """游程编码测试"""
    
    def test_run_length_encoding(self):
        """测试游程编码"""
        encoded = LookAndSayUtils.run_length_encoding("111221")
        expected = [("1", 3), ("2", 2), ("1", 1)]
        self.assertEqual(encoded, expected)
    
    def test_run_length_encoding_single(self):
        """测试单个字符"""
        self.assertEqual(LookAndSayUtils.run_length_encoding("111"), [("1", 3)])
    
    def test_run_length_encoding_empty(self):
        """测试空字符串"""
        self.assertEqual(LookAndSayUtils.run_length_encoding(""), [])
    
    def test_from_run_length(self):
        """测试游程解码"""
        encoded = [("1", 3), ("2", 2), ("1", 1)]
        result = LookAndSayUtils.from_run_length(encoded)
        self.assertEqual(result, "111221")
    
    def test_run_length_roundtrip(self):
        """测试编码解码往返"""
        original = "11122131111322"
        encoded = LookAndSayUtils.run_length_encoding(original)
        decoded = LookAndSayUtils.from_run_length(encoded)
        self.assertEqual(original, decoded)


class TestValidation(unittest.TestCase):
    """验证测试"""
    
    def test_is_valid_basic(self):
        """测试基本有效性检查"""
        self.assertTrue(LookAndSayUtils.is_valid_look_and_say_term("1"))
        self.assertTrue(LookAndSayUtils.is_valid_look_and_say_term("11"))
        self.assertTrue(LookAndSayUtils.is_valid_look_and_say_term("21"))
        self.assertTrue(LookAndSayUtils.is_valid_look_and_say_term("1211"))
    
    def test_is_valid_empty(self):
        """测试空字符串"""
        self.assertFalse(LookAndSayUtils.is_valid_look_and_say_term(""))
    
    def test_is_valid_non_digit(self):
        """测试非数字字符"""
        self.assertFalse(LookAndSayUtils.is_valid_look_and_say_term("abc"))
        self.assertFalse(LookAndSayUtils.is_valid_look_and_say_term("12a1"))
    
    def test_is_valid_four_consecutive(self):
        """测试4个连续相同数字"""
        # 外观数列中不会出现连续4个相同数字
        self.assertFalse(LookAndSayUtils.is_valid_look_and_say_term("1111"))
        self.assertFalse(LookAndSayUtils.is_valid_look_and_say_term("222211"))


class TestReverseStep(unittest.TestCase):
    """反向推导测试"""
    
    def test_reverse_step_basic(self):
        """测试基本反向推导"""
        result = LookAndSayUtils.reverse_step("11")
        self.assertIn("1", result)
    
    def test_reverse_step_21(self):
        """测试21的反向推导"""
        result = LookAndSayUtils.reverse_step("21")
        self.assertIn("11", result)
    
    def test_reverse_step_invalid(self):
        """测试无效输入的反向推导"""
        # 奇数长度无效
        result = LookAndSayUtils.reverse_step("1")
        self.assertEqual(result, [])
    
    def test_reverse_step_empty(self):
        """测试空字符串的反向推导"""
        self.assertEqual(LookAndSayUtils.reverse_step(""), [])


class TestSplitElements(unittest.TestCase):
    """元素分割测试"""
    
    def test_split_basic(self):
        """测试基本分割"""
        result = LookAndSayUtils.split_into_elements("111221")
        expected = ["111", "22", "1"]
        self.assertEqual(result, expected)
    
    def test_split_single(self):
        """测试单一元素"""
        self.assertEqual(LookAndSayUtils.split_into_elements("111"), ["111"])
    
    def test_split_alternating(self):
        """测试交替元素"""
        result = LookAndSayUtils.split_into_elements("121212")
        expected = ["1", "2", "1", "2", "1", "2"]
        self.assertEqual(result, expected)


class TestEstimation(unittest.TestCase):
    """估算测试"""
    
    def test_estimate_nth_length(self):
        """测试长度估算"""
        estimated = LookAndSayUtils.estimate_nth_length(10)
        actual = len(LookAndSayUtils.nth_term(10))
        # 估算应该在合理范围内（误差50%以内）
        self.assertGreater(estimated, actual * 0.5)
        self.assertLess(estimated, actual * 1.5)
    
    def test_estimate_growth_rate(self):
        """测试估算增长率"""
        # 验证估算的增长率合理（早期项误差可能较大）
        for n in range(10, 15):
            est = LookAndSayUtils.estimate_nth_length(n)
            actual = len(LookAndSayUtils.nth_term(n))
            # 允许一定误差（早期项波动大）
            error_rate = abs(est - actual) / actual
            self.assertLess(error_rate, 0.6)  # 60%误差以内（早期项波动大）


class TestIterator(unittest.TestCase):
    """迭代器测试"""
    
    def test_iterator(self):
        """测试迭代器"""
        it = LookAndSayUtils.iterator()
        terms = [next(it) for _ in range(5)]
        expected = ["1", "11", "21", "1211", "111221"]
        self.assertEqual(terms, expected)
    
    def test_iterator_custom_start(self):
        """测试自定义起始的迭代器"""
        it = LookAndSayUtils.iterator("3")
        terms = [next(it) for _ in range(3)]
        expected = ["3", "13", "1113"]
        self.assertEqual(terms, expected)


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_next_term_function(self):
        """测试next_term便捷函数"""
        self.assertEqual(next_term("1"), "11")
        self.assertEqual(next_term("21"), "1211")
    
    def test_generate_function(self):
        """测试generate便捷函数"""
        terms = generate(3)
        self.assertEqual(terms, ["1", "11", "21"])
    
    def test_nth_term_function(self):
        """测试nth_term便捷函数"""
        self.assertEqual(nth_term(3), "1211")
    
    def test_conway_constant_function(self):
        """测试conway_constant便捷函数"""
        from mod import conway_constant
        const = conway_constant()
        self.assertGreater(const, 1.3)
        self.assertLess(const, 1.31)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_large_n(self):
        """测试较大的n值"""
        # 生成第30项，确保不会出错
        term = LookAndSayUtils.nth_term(30)
        self.assertGreater(len(term), 0)
        # 第30项应该相当长
        self.assertGreater(len(term), 500)
    
    def test_different_seed_special(self):
        """测试特殊种子"""
        # 种子"22"是不动点
        terms = LookAndSayUtils.different_seed("22", 10)
        self.assertTrue(all(t == "22" for t in terms))
    
    def test_growth_analysis(self):
        """测试增长分析"""
        analysis = LookAndSayUtils.analyze_growth(10)
        self.assertEqual(len(analysis), 10)
        # 第一项的长度应该是1
        self.assertEqual(analysis[0][1], 1)
    
    def test_cosmological_decay(self):
        """测试宇宙学衰减"""
        decay = LookAndSayUtils.cosmological_decay(20)
        # 应该返回一个字典
        self.assertIsInstance(decay, dict)
        # 应该包含基本的模式
        self.assertIn("111", decay)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_sequence_consistency(self):
        """测试完整序列一致性"""
        # 生成序列并验证每一步
        terms = LookAndSayUtils.generate(15)
        for i in range(1, len(terms)):
            self.assertEqual(LookAndSayUtils.next_term(terms[i-1]), terms[i])
    
    def test_sequence_properties(self):
        """测试序列性质"""
        terms = LookAndSayUtils.generate(20)
        
        # 性质1：只包含数字1、2、3
        for term in terms:
            for char in term:
                self.assertIn(char, "123")
        
        # 性质2：长度单调非递减（从某点开始）
        lengths = [len(t) for t in terms]
        for i in range(2, len(lengths)):
            self.assertGreaterEqual(lengths[i], lengths[i-1])


if __name__ == "__main__":
    unittest.main(verbosity=2)