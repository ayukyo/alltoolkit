"""
考拉兹猜想工具模块测试
"""

import unittest
from mod import (
    collatz_step,
    generate_sequence,
    get_steps_to_one,
    get_max_value,
    get_max_value_position,
    analyze,
    find_longest_sequence,
    find_highest_value,
    verify_conjecture,
    batch_analyze,
    get_odd_even_ratio,
    get_convergence_tree,
    get_stopping_time,
    is_in_4_2_1_cycle,
    get_total_stopping_time,
    get_eta,
    format_sequence,
    get_statistics,
    CollatzSequence,
)


class TestCollatzStep(unittest.TestCase):
    """测试单步考拉兹变换"""
    
    def test_even_number(self):
        """测试偶数"""
        self.assertEqual(collatz_step(6), 3)
        self.assertEqual(collatz_step(10), 5)
        self.assertEqual(collatz_step(2), 1)
        self.assertEqual(collatz_step(4), 2)
    
    def test_odd_number(self):
        """测试奇数"""
        self.assertEqual(collatz_step(3), 10)
        self.assertEqual(collatz_step(5), 16)
        self.assertEqual(collatz_step(7), 22)
        self.assertEqual(collatz_step(1), 4)
    
    def test_invalid_input(self):
        """测试无效输入"""
        with self.assertRaises(ValueError):
            collatz_step(0)
        with self.assertRaises(ValueError):
            collatz_step(-1)


class TestGenerateSequence(unittest.TestCase):
    """测试序列生成"""
    
    def test_simple_sequences(self):
        """测试简单序列"""
        # n=1 默认不包含循环
        self.assertEqual(generate_sequence(1), [1])
        # n=1 包含循环
        self.assertEqual(generate_sequence(1, include_cycle=True), [1, 4, 2, 1])
        self.assertEqual(generate_sequence(2), [2, 1])
        self.assertEqual(generate_sequence(4), [4, 2, 1])
    
    def test_medium_sequences(self):
        """测试中等长度序列"""
        self.assertEqual(
            generate_sequence(6),
            [6, 3, 10, 5, 16, 8, 4, 2, 1]
        )
        self.assertEqual(
            generate_sequence(3),
            [3, 10, 5, 16, 8, 4, 2, 1]
        )
    
    def test_long_sequence(self):
        """测试较长序列 (27是著名的例子)"""
        seq = generate_sequence(27)
        self.assertEqual(seq[0], 27)
        self.assertEqual(seq[-1], 1)
        self.assertEqual(len(seq), 112)  # 27的序列有112个元素
    
    def test_invalid_input(self):
        """测试无效输入"""
        with self.assertRaises(ValueError):
            generate_sequence(0)
        with self.assertRaises(ValueError):
            generate_sequence(-5)


class TestGetStepsToOne(unittest.TestCase):
    """测试步数计算"""
    
    def test_simple_cases(self):
        """测试简单情况"""
        self.assertEqual(get_steps_to_one(1), 0)
        self.assertEqual(get_steps_to_one(2), 1)
        self.assertEqual(get_steps_to_one(4), 2)
    
    def test_known_cases(self):
        """测试已知值"""
        # 数字6: [6, 3, 10, 5, 16, 8, 4, 2, 1] - 8步变换
        self.assertEqual(get_steps_to_one(6), 8)
        # 数字27: 111步（著名例子）
        self.assertEqual(get_steps_to_one(27), 111)
    
    def test_cached_results(self):
        """测试缓存功能"""
        # 多次调用应该返回相同结果
        for _ in range(5):
            self.assertEqual(get_steps_to_one(100), get_steps_to_one(100))


class TestGetMaxValue(unittest.TestCase):
    """测试最大值获取"""
    
    def test_simple_cases(self):
        """测试简单情况"""
        # n=1 不包含循环时最大值是1
        self.assertEqual(get_max_value(1), 1)
        self.assertEqual(get_max_value(2), 2)
        self.assertEqual(get_max_value(4), 4)
    
    def test_known_cases(self):
        """测试已知值"""
        self.assertEqual(get_max_value(6), 16)
        self.assertEqual(get_max_value(27), 9232)


class TestGetMaxValuePosition(unittest.TestCase):
    """测试最大值位置"""
    
    def test_position(self):
        """测试位置计算"""
        val, pos = get_max_value_position(6)
        self.assertEqual(val, 16)
        self.assertEqual(pos, 4)
        
        val, pos = get_max_value_position(27)
        self.assertEqual(val, 9232)
        # 27的序列有112个元素，最大值9232在位置77（索引从0开始）
        self.assertEqual(pos, 77)


class TestAnalyze(unittest.TestCase):
    """测试全面分析"""
    
    def test_analyze_6(self):
        """测试数字6的分析"""
        result = analyze(6)
        self.assertEqual(result['start_value'], 6)
        # 步数 = 序列长度 - 1 = 9 - 1 = 8
        self.assertEqual(result['steps'], 8)
        self.assertEqual(result['max_value'], 16)
        self.assertEqual(result['sequence_length'], 9)
        # 序列 [6, 3, 10, 5, 16, 8, 4, 2, 1]
        # 奇数: 3, 5, 1 (不包括起始值) - 实际包括所有
        # 奇数: 6,3,10,5,16,8,4,2,1 中奇数有 3,5,1 = 3个
        # 但分析中的计数是基于整个序列
        self.assertEqual(result['odd_count'], 3)  # 3, 5, 1
        self.assertEqual(result['even_count'], 6)  # 6, 10, 16, 8, 4, 2
    
    def test_analyze_1(self):
        """测试数字1的分析"""
        result = analyze(1)
        self.assertEqual(result['start_value'], 1)
        self.assertEqual(result['steps'], 0)
        # n=1 不包含循环，最大值是1
        self.assertEqual(result['max_value'], 1)


class TestFindLongestSequence(unittest.TestCase):
    """测试查找最长序列"""
    
    def test_small_range(self):
        """测试小范围"""
        n, steps = find_longest_sequence(10)
        self.assertEqual(n, 9)
        self.assertEqual(steps, 19)
    
    def test_medium_range(self):
        """测试中等范围"""
        n, steps = find_longest_sequence(100)
        self.assertEqual(n, 97)
        self.assertEqual(steps, 118)


class TestFindHighestValue(unittest.TestCase):
    """测试查找最高值"""
    
    def test_small_range(self):
        """测试小范围"""
        n, val = find_highest_value(10)
        # 数字9产生最大值52，但数字7产生最大值22的序列有更高的峰值
        # 让我们检查实际值
        # 7 -> 22 -> 11 -> 34 -> 17 -> 52 -> ...
        # 实际上数字7的序列峰值是9232(通过27的路径)? 不对，让我们重新计算
        # 7的序列: [7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
        # 峰值是52
        # 9的序列: [9, 28, 14, 7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
        # 峰值也是52
        self.assertEqual(val, 52)


class TestVerifyConjecture(unittest.TestCase):
    """测试猜想验证"""
    
    def test_verification(self):
        """测试验证功能"""
        verified, count = verify_conjecture(100)
        self.assertTrue(verified)
        self.assertEqual(count, 100)
        
        verified, count = verify_conjecture(1000)
        self.assertTrue(verified)


class TestBatchAnalyze(unittest.TestCase):
    """测试批量分析"""
    
    def test_batch(self):
        """测试批量分析"""
        results = batch_analyze([1, 2, 3, 4, 5])
        self.assertEqual(len(results), 5)
        self.assertEqual(results[0]['start_value'], 1)
        self.assertEqual(results[4]['start_value'], 5)


class TestGetOddEvenRatio(unittest.TestCase):
    """测试奇偶比例"""
    
    def test_ratio(self):
        """测试比例计算"""
        # 序列 [6, 3, 10, 5, 16, 8, 4, 2, 1]
        # 奇数: 3, 5, 1 = 3个
        # 偶数: 6, 10, 16, 8, 4, 2 = 6个
        ratio = get_odd_even_ratio(6)
        self.assertAlmostEqual(ratio, 0.5)  # 3/6 = 0.5
        
        # n=1: [1], 奇数1个，偶数0个，比例为无穷大
        # 但我们的实现会返回特殊值


class TestGetConvergenceTree(unittest.TestCase):
    """测试收敛树"""
    
    def test_tree_structure(self):
        """测试树结构"""
        tree = get_convergence_tree(1, max_depth=2)
        self.assertEqual(tree['value'], 1)
        self.assertTrue(len(tree['children']) > 0)
    
    def test_tree_contains_2(self):
        """测试树包含2"""
        tree = get_convergence_tree(1, max_depth=2)
        values = [child['value'] for child in tree['children']]
        self.assertIn(2, values)


class TestGetStoppingTime(unittest.TestCase):
    """测试停止时间"""
    
    def test_stopping_time(self):
        """测试停止时间"""
        # 数字6: 第一步就降到起始值以下 (6->3)
        self.assertEqual(get_stopping_time(6), 1)
        # 数字7: 序列需要多少步才能降到7以下？
        # [7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, ...]
        # 第11步到达5 (< 7)
        self.assertEqual(get_stopping_time(7), 11)
    
    def test_stopping_time_one(self):
        """测试1的停止时间"""
        self.assertEqual(get_stopping_time(1), 0)


class TestIsIn421Cycle(unittest.TestCase):
    """测试4-2-1循环检测"""
    
    def test_in_cycle(self):
        """测试在循环中的数字"""
        self.assertTrue(is_in_4_2_1_cycle(1))
        self.assertTrue(is_in_4_2_1_cycle(2))
        self.assertTrue(is_in_4_2_1_cycle(4))
    
    def test_not_in_cycle(self):
        """测试不在循环中的数字"""
        self.assertFalse(is_in_4_2_1_cycle(3))
        self.assertFalse(is_in_4_2_1_cycle(6))
        self.assertFalse(is_in_4_2_1_cycle(27))


class TestGetTotalStoppingTime(unittest.TestCase):
    """测试总停止时间"""
    
    def test_total_stopping_time(self):
        """测试总停止时间"""
        self.assertEqual(get_total_stopping_time(27), 111)
        self.assertEqual(get_total_stopping_time(1), 0)


class TestGetEta(unittest.TestCase):
    """测试Eta函数"""
    
    def test_eta(self):
        """测试Eta值"""
        # 27的序列：最大值9232在索引77
        self.assertEqual(get_eta(27), 77)
        # 6的序列：[6, 3, 10, 5, 16, 8, 4, 2, 1]
        # 最大值16在索引4
        self.assertEqual(get_eta(6), 4)


class TestFormatSequence(unittest.TestCase):
    """测试序列格式化"""
    
    def test_format(self):
        """测试格式化输出"""
        self.assertEqual(
            format_sequence(6),
            "6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1"
        )
        # n=1 默认不包含循环
        self.assertEqual(
            format_sequence(1),
            "1"
        )
    
    def test_custom_separator(self):
        """测试自定义分隔符"""
        result = format_sequence(6, separator=", ")
        self.assertEqual(result, "6, 3, 10, 5, 16, 8, 4, 2, 1")


class TestGetStatistics(unittest.TestCase):
    """测试统计信息"""
    
    def test_statistics(self):
        """测试统计功能"""
        stats = get_statistics(10)
        self.assertEqual(stats['total_numbers'], 10)
        self.assertGreater(stats['average_steps'], 0)
        self.assertEqual(stats['max_steps_number'], 9)
        self.assertEqual(stats['max_steps'], 19)


class TestCollatzSequenceClass(unittest.TestCase):
    """测试 CollatzSequence 类"""
    
    def test_iteration(self):
        """测试迭代"""
        seq = CollatzSequence(6)
        self.assertEqual(list(seq), [6, 3, 10, 5, 16, 8, 4, 2, 1])
    
    def test_length(self):
        """测试长度"""
        seq = CollatzSequence(6)
        self.assertEqual(len(seq), 9)
    
    def test_indexing(self):
        """测试索引"""
        seq = CollatzSequence(6)
        self.assertEqual(seq[0], 6)
        self.assertEqual(seq[-1], 1)
        self.assertEqual(seq[4], 16)
    
    def test_properties(self):
        """测试属性"""
        seq = CollatzSequence(6)
        self.assertEqual(seq.start, 6)
        # 步数 = 序列长度 - 1 = 9 - 1 = 8
        self.assertEqual(seq.steps, 8)
        self.assertEqual(seq.max_value, 16)
        # 序列 [6, 3, 10, 5, 16, 8, 4, 2, 1]
        # 奇数: 3, 5, 1 = 3个
        self.assertEqual(seq.odd_count, 3)
        self.assertEqual(seq.even_count, 6)
    
    def test_repr(self):
        """测试字符串表示"""
        seq = CollatzSequence(6)
        self.assertEqual(repr(seq), "CollatzSequence(6)")
        self.assertEqual(str(seq), "6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1")
    
    def test_invalid_input(self):
        """测试无效输入"""
        with self.assertRaises(ValueError):
            CollatzSequence(0)
        with self.assertRaises(ValueError):
            CollatzSequence(-1)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_power_of_two(self):
        """测试2的幂次"""
        for i in range(1, 10):
            n = 2 ** i
            # 2^i 的步数应该是 i（直接除以2到底）
            self.assertEqual(get_steps_to_one(n), i)
    
    def test_sequence_always_ends_at_one(self):
        """测试序列总是以1结束"""
        for n in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 27, 100, 1000]:
            seq = generate_sequence(n)
            self.assertEqual(seq[-1], 1, f"序列 {n} 应该以 1 结束")
    
    def test_sequence_contains_start(self):
        """测试序列包含起始值"""
        for n in [1, 2, 3, 6, 27, 100]:
            seq = generate_sequence(n)
            self.assertEqual(seq[0], n)


if __name__ == "__main__":
    unittest.main(verbosity=2)