"""
lottery_utils 测试模块

测试双色球、大乐透、排列三/五、七星彩的号码生成、中奖判断等功能。
"""

import unittest
from lottery_utils import (
    LotteryType, LotteryResult, PrizeInfo,
    SSQUtils, DLTUtils, P3P5Utils, QXCUtils,
    LotteryAnalyzer, LotterySimulator,
    generate_lucky_numbers, quick_pick, format_prize_amount
)


class TestSSQUtils(unittest.TestCase):
    """双色球工具测试"""
    
    def test_generate_single(self):
        """测试生成单注号码"""
        result = SSQUtils.generate(seed=42)
        
        self.assertEqual(result.lottery_type, LotteryType.SSQ)
        self.assertEqual(len(result.numbers), 6)  # 6个红球
        self.assertEqual(len(result.special_numbers), 1)  # 1个蓝球
        
        # 验证红球范围
        for num in result.numbers:
            self.assertGreaterEqual(num, 1)
            self.assertLessEqual(num, 33)
        
        # 验证蓝球范围
        for num in result.special_numbers:
            self.assertGreaterEqual(num, 1)
            self.assertLessEqual(num, 16)
        
        # 验证红球不重复
        self.assertEqual(len(result.numbers), len(set(result.numbers)))
        
        # 验证红球已排序
        self.assertEqual(result.numbers, sorted(result.numbers))
    
    def test_generate_multiple(self):
        """测试生成多注号码"""
        results = SSQUtils.generate_multiple(5)
        
        self.assertEqual(len(results), 5)
        for result in results:
            self.assertEqual(result.lottery_type, LotteryType.SSQ)
    
    def test_reproducible_with_seed(self):
        """测试相同种子生成相同号码"""
        result1 = SSQUtils.generate(seed=12345)
        result2 = SSQUtils.generate(seed=12345)
        
        self.assertEqual(result1.numbers, result2.numbers)
        self.assertEqual(result1.special_numbers, result2.special_numbers)
    
    def test_check_prize_first(self):
        """测试一等奖判断"""
        winning = LotteryResult(
            lottery_type=LotteryType.SSQ,
            numbers=[1, 2, 3, 4, 5, 6],
            special_numbers=[7]
        )
        my_numbers = LotteryResult(
            lottery_type=LotteryType.SSQ,
            numbers=[1, 2, 3, 4, 5, 6],
            special_numbers=[7]
        )
        
        prize = SSQUtils.check_prize(my_numbers, winning)
        
        self.assertIsNotNone(prize)
        self.assertEqual(prize.prize_name, "一等奖")
    
    def test_check_prize_second(self):
        """测试二等奖判断"""
        winning = LotteryResult(
            lottery_type=LotteryType.SSQ,
            numbers=[1, 2, 3, 4, 5, 6],
            special_numbers=[7]
        )
        my_numbers = LotteryResult(
            lottery_type=LotteryType.SSQ,
            numbers=[1, 2, 3, 4, 5, 6],
            special_numbers=[8]  # 蓝球不中
        )
        
        prize = SSQUtils.check_prize(my_numbers, winning)
        
        self.assertIsNotNone(prize)
        self.assertEqual(prize.prize_name, "二等奖")
    
    def test_check_prize_sixth(self):
        """测试六等奖判断（只中蓝球）"""
        winning = LotteryResult(
            lottery_type=LotteryType.SSQ,
            numbers=[1, 2, 3, 4, 5, 6],
            special_numbers=[7]
        )
        my_numbers = LotteryResult(
            lottery_type=LotteryType.SSQ,
            numbers=[10, 11, 12, 13, 14, 15],  # 红球全不中
            special_numbers=[7]  # 蓝球中
        )
        
        prize = SSQUtils.check_prize(my_numbers, winning)
        
        self.assertIsNotNone(prize)
        self.assertEqual(prize.prize_name, "六等奖")
    
    def test_check_prize_no_win(self):
        """测试未中奖判断"""
        winning = LotteryResult(
            lottery_type=LotteryType.SSQ,
            numbers=[1, 2, 3, 4, 5, 6],
            special_numbers=[7]
        )
        my_numbers = LotteryResult(
            lottery_type=LotteryType.SSQ,
            numbers=[10, 11, 12, 13, 14, 15],
            special_numbers=[8]
        )
        
        prize = SSQUtils.check_prize(my_numbers, winning)
        
        self.assertIsNone(prize)
    
    def test_probability_calculation(self):
        """测试概率计算"""
        prob_first = SSQUtils.calculate_probability(1)
        self.assertGreater(prob_first, 0)
        self.assertLess(prob_first, 1)
        
        # 一等奖概率约为 1/17721088
        expected = 1 / 17721088
        self.assertAlmostEqual(prob_first, expected, places=10)


class TestDLTUtils(unittest.TestCase):
    """大乐透工具测试"""
    
    def test_generate_single(self):
        """测试生成单注号码"""
        result = DLTUtils.generate(seed=42)
        
        self.assertEqual(result.lottery_type, LotteryType.DLT)
        self.assertEqual(len(result.numbers), 5)  # 5个前区
        self.assertEqual(len(result.special_numbers), 2)  # 2个后区
        
        # 验证前区范围
        for num in result.numbers:
            self.assertGreaterEqual(num, 1)
            self.assertLessEqual(num, 35)
        
        # 验证后区范围
        for num in result.special_numbers:
            self.assertGreaterEqual(num, 1)
            self.assertLessEqual(num, 12)
    
    def test_check_prize_first(self):
        """测试一等奖判断"""
        winning = LotteryResult(
            lottery_type=LotteryType.DLT,
            numbers=[1, 2, 3, 4, 5],
            special_numbers=[6, 7]
        )
        my_numbers = LotteryResult(
            lottery_type=LotteryType.DLT,
            numbers=[1, 2, 3, 4, 5],
            special_numbers=[6, 7]
        )
        
        prize = DLTUtils.check_prize(my_numbers, winning)
        
        self.assertIsNotNone(prize)
        self.assertEqual(prize.prize_name, "一等奖")
    
    def test_probability_calculation(self):
        """测试概率计算"""
        prob_first = DLTUtils.calculate_probability(1)
        self.assertGreater(prob_first, 0)
        self.assertLess(prob_first, 1)


class TestP3P5Utils(unittest.TestCase):
    """排列三/五工具测试"""
    
    def test_generate_p3(self):
        """测试生成排列三号码"""
        result = P3P5Utils.generate_p3(seed=42)
        
        self.assertEqual(result.lottery_type, LotteryType.P3)
        self.assertEqual(len(result.numbers), 3)
        
        for num in result.numbers:
            self.assertGreaterEqual(num, 0)
            self.assertLessEqual(num, 9)
    
    def test_generate_p5(self):
        """测试生成排列五号码"""
        result = P3P5Utils.generate_p5(seed=42)
        
        self.assertEqual(result.lottery_type, LotteryType.P5)
        self.assertEqual(len(result.numbers), 5)
    
    def test_check_prize_p3_direct(self):
        """测试排列三直选中奖"""
        winning = LotteryResult(
            lottery_type=LotteryType.P3,
            numbers=[1, 2, 3],
            special_numbers=[]
        )
        my_numbers = LotteryResult(
            lottery_type=LotteryType.P3,
            numbers=[1, 2, 3],
            special_numbers=[]
        )
        
        prize = P3P5Utils.check_prize_p3(my_numbers, winning)
        
        self.assertIsNotNone(prize)
        self.assertEqual(prize.prize_name, "直选")
    
    def test_check_prize_p3_group3(self):
        """测试排列三组选三中奖"""
        winning = LotteryResult(
            lottery_type=LotteryType.P3,
            numbers=[1, 1, 2],
            special_numbers=[]
        )
        my_numbers = LotteryResult(
            lottery_type=LotteryType.P3,
            numbers=[1, 2, 1],  # 顺序不同
            special_numbers=[]
        )
        
        prize = P3P5Utils.check_prize_p3(my_numbers, winning)
        
        self.assertIsNotNone(prize)
        self.assertEqual(prize.prize_name, "组选三")
    
    def test_check_prize_p3_group6(self):
        """测试排列三组选六中奖"""
        winning = LotteryResult(
            lottery_type=LotteryType.P3,
            numbers=[1, 2, 3],
            special_numbers=[]
        )
        my_numbers = LotteryResult(
            lottery_type=LotteryType.P3,
            numbers=[3, 2, 1],  # 顺序不同
            special_numbers=[]
        )
        
        prize = P3P5Utils.check_prize_p3(my_numbers, winning)
        
        self.assertIsNotNone(prize)
        self.assertEqual(prize.prize_name, "组选六")
    
    def test_check_prize_p5(self):
        """测试排列五中奖"""
        winning = LotteryResult(
            lottery_type=LotteryType.P5,
            numbers=[1, 2, 3, 4, 5],
            special_numbers=[]
        )
        my_numbers = LotteryResult(
            lottery_type=LotteryType.P5,
            numbers=[1, 2, 3, 4, 5],
            special_numbers=[]
        )
        
        prize = P3P5Utils.check_prize_p5(my_numbers, winning)
        
        self.assertIsNotNone(prize)
        self.assertEqual(prize.prize_name, "直选")
    
    def test_probability_p3(self):
        """测试排列三概率"""
        prob_direct = P3P5Utils.calculate_probability_p3('direct')
        self.assertAlmostEqual(prob_direct, 1/1000, places=6)
        
        prob_group3 = P3P5Utils.calculate_probability_p3('group3')
        self.assertAlmostEqual(prob_group3, 3/1000, places=6)
        
        prob_group6 = P3P5Utils.calculate_probability_p3('group6')
        self.assertAlmostEqual(prob_group6, 6/1000, places=6)
    
    def test_probability_p5(self):
        """测试排列五概率"""
        prob = P3P5Utils.calculate_probability_p5()
        self.assertAlmostEqual(prob, 1/100000, places=8)


class TestQXCUtils(unittest.TestCase):
    """七星彩工具测试"""
    
    def test_generate(self):
        """测试生成七星彩号码"""
        result = QXCUtils.generate(seed=42)
        
        self.assertEqual(result.lottery_type, LotteryType.QXC)
        self.assertEqual(len(result.numbers), 6)  # 前6位
        self.assertEqual(len(result.special_numbers), 1)  # 第7位
        
        for num in result.numbers + result.special_numbers:
            self.assertGreaterEqual(num, 0)
            self.assertLessEqual(num, 9)
    
    def test_check_prize_first(self):
        """测试七星彩一等奖（全部7位连续匹配）"""
        winning = LotteryResult(
            lottery_type=LotteryType.QXC,
            numbers=[1, 2, 3, 4, 5, 6],
            special_numbers=[7]
        )
        my_numbers = LotteryResult(
            lottery_type=LotteryType.QXC,
            numbers=[1, 2, 3, 4, 5, 6],
            special_numbers=[7]
        )
        
        prize = QXCUtils.check_prize(my_numbers, winning)
        
        self.assertIsNotNone(prize)
        self.assertEqual(prize.prize_name, "一等奖")
    
    def test_check_prize_partial(self):
        """测试部分匹配"""
        winning = LotteryResult(
            lottery_type=LotteryType.QXC,
            numbers=[1, 2, 3, 4, 5, 6],
            special_numbers=[7]
        )
        my_numbers = LotteryResult(
            lottery_type=LotteryType.QXC,
            numbers=[0, 2, 3, 4, 5, 6],  # 后5位匹配（从后向前连续5位）
            special_numbers=[7]
        )
        
        prize = QXCUtils.check_prize(my_numbers, winning)
        
        self.assertIsNotNone(prize)
        self.assertEqual(prize.prize_name, "二等奖")  # 连续5位匹配（从后向前）
    
    def test_probability(self):
        """测试七星彩概率"""
        # 匹配后1位
        prob = QXCUtils.calculate_probability(1)
        self.assertAlmostEqual(prob, 1/10, places=6)
        
        # 匹配后2位
        prob = QXCUtils.calculate_probability(2)
        self.assertAlmostEqual(prob, 1/100, places=6)


class TestLotteryAnalyzer(unittest.TestCase):
    """彩票分析工具测试"""
    
    def setUp(self):
        """创建测试数据"""
        self.test_results = [
            LotteryResult(LotteryType.SSQ, [1, 2, 3, 4, 5, 6], [7]),
            LotteryResult(LotteryType.SSQ, [2, 3, 4, 5, 6, 7], [8]),
            LotteryResult(LotteryType.SSQ, [3, 4, 5, 6, 7, 8], [9]),
            LotteryResult(LotteryType.SSQ, [1, 3, 5, 7, 9, 11], [7]),
            LotteryResult(LotteryType.SSQ, [2, 4, 6, 8, 10, 12], [7]),
        ]
    
    def test_analyze_frequency(self):
        """测试频率分析"""
        freq = LotteryAnalyzer.analyze_frequency(self.test_results, LotteryType.SSQ)
        
        self.assertIn("main", freq)
        self.assertIn("special", freq)
        
        # 数字7在蓝球出现3次
        self.assertEqual(freq["special"][7], 3)
    
    def test_find_hot_cold_numbers(self):
        """测试热号冷号"""
        result = LotteryAnalyzer.find_hot_cold_numbers(self.test_results, LotteryType.SSQ)
        
        self.assertIn("hot", result)
        self.assertIn("cold", result)
    
    def test_calculate_odd_even_ratio(self):
        """测试奇偶比"""
        result = LotteryResult(LotteryType.SSQ, [1, 2, 3, 4, 5, 6], [7])
        ratio = LotteryAnalyzer.calculate_odd_even_ratio(result)
        
        self.assertEqual(ratio["odd"], 4)  # 1,3,5,7
        self.assertEqual(ratio["even"], 3)  # 2,4,6
    
    def test_calculate_sum(self):
        """测试和值"""
        result = LotteryResult(LotteryType.SSQ, [1, 2, 3, 4, 5, 6], [7])
        total = LotteryAnalyzer.calculate_sum(result)
        
        self.assertEqual(total, 28)  # 1+2+3+4+5+6+7
    
    def test_calculate_span(self):
        """测试跨度"""
        result = LotteryResult(LotteryType.SSQ, [1, 5, 10, 15, 20, 25], [7])
        span = LotteryAnalyzer.calculate_span(result)
        
        self.assertEqual(span, 24)  # 25-1
    
    def test_find_consecutive(self):
        """测试连号"""
        result = LotteryResult(LotteryType.SSQ, [1, 2, 3, 5, 6, 10], [7])
        consecutive = LotteryAnalyzer.find_consecutive(result)
        
        self.assertEqual(len(consecutive), 2)  # [1,2,3] 和 [5,6]


class TestLotterySimulator(unittest.TestCase):
    """彩票模拟器测试"""
    
    def test_simulate_ssq(self):
        """测试双色球模拟"""
        result = LotterySimulator.simulate_ssq(100, seed=42)
        
        self.assertIn("winning_numbers", result)
        self.assertEqual(result["tickets"], 100)
        self.assertEqual(result["cost"], 20000)  # 100注 * 200分
        self.assertIn("prize_breakdown", result)
    
    def test_simulate_dlt(self):
        """测试大乐透模拟"""
        result = LotterySimulator.simulate_dlt(50, seed=42)
        
        self.assertIn("winning_numbers", result)
        self.assertEqual(result["tickets"], 50)


class TestHelperFunctions(unittest.TestCase):
    """辅助函数测试"""
    
    def test_format_prize_amount(self):
        """测试金额格式化"""
        # 大于100万
        self.assertIn("万", format_prize_amount(500_0000_00))
        
        # 大于1万小于100万
        self.assertIn("元", format_prize_amount(5_0000_00))
        
        # 小于1万
        self.assertIn("元", format_prize_amount(500_00))
    
    def test_generate_lucky_numbers(self):
        """测试统一生成接口"""
        for lot_type in LotteryType:
            result = generate_lucky_numbers(lot_type, seed=42)
            self.assertEqual(result.lottery_type, lot_type)
    
    def test_quick_pick(self):
        """测试快速选号"""
        results = quick_pick("双色球", 3)
        
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertEqual(result.lottery_type, LotteryType.SSQ)
    
    def test_quick_pick_invalid_type(self):
        """测试无效彩票类型"""
        with self.assertRaises(ValueError):
            quick_pick("无效彩票", 1)


class TestLotteryResult(unittest.TestCase):
    """LotteryResult 测试"""
    
    def test_to_dict(self):
        """测试转换为字典"""
        result = LotteryResult(
            lottery_type=LotteryType.SSQ,
            numbers=[1, 2, 3, 4, 5, 6],
            special_numbers=[7],
            draw_date="2024-01-01"
        )
        
        d = result.to_dict()
        
        self.assertEqual(d["lottery_type"], "双色球")
        self.assertEqual(d["numbers"], [1, 2, 3, 4, 5, 6])
        self.assertEqual(d["special_numbers"], [7])
        self.assertEqual(d["draw_date"], "2024-01-01")
    
    def test_str(self):
        """测试字符串表示"""
        result = LotteryResult(
            lottery_type=LotteryType.SSQ,
            numbers=[1, 2, 3, 4, 5, 6],
            special_numbers=[7]
        )
        
        s = str(result)
        
        self.assertIn("双色球", s)
        self.assertIn("7", s)


if __name__ == "__main__":
    unittest.main(verbosity=2)