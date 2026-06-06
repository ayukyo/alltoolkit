"""
Menstrual Cycle Calculator Tests - 月经周期计算工具测试

零外部依赖测试套件
"""

import unittest
from datetime import datetime, timedelta
from menstrual_cycle import (
    MenstrualCycleCalculator,
    CyclePhase,
    FertilityLevel,
    CycleDay,
    calculate_next_period,
    get_fertile_days,
    get_ovulation_date,
    format_date
)


class TestMenstrualCycleCalculator(unittest.TestCase):
    """月经周期计算器测试"""
    
    def setUp(self):
        """测试初始化"""
        self.base_date = datetime(2024, 1, 1)
        self.calculator = MenstrualCycleCalculator(
            self.base_date,
            cycle_length=28,
            period_length=5
        )
    
    def test_default_values(self):
        """测试默认值"""
        self.assertEqual(self.calculator.DEFAULT_CYCLE_LENGTH, 28)
        self.assertEqual(self.calculator.DEFAULT_PERIOD_LENGTH, 5)
        self.assertEqual(self.calculator.DEFAULT_LUTEAL_LENGTH, 14)
    
    def test_get_phase_menstrual(self):
        """测试月经期判断"""
        # 第1-5天应该是月经期
        for day in range(1, 6):
            phase = self.calculator.get_phase(day)
            self.assertEqual(phase, CyclePhase.MENSTRUAL, 
                           f"Day {day} should be menstrual phase")
    
    def test_get_phase_follicular(self):
        """测试卵泡期判断"""
        # 第6-10天应该是卵泡期（排卵在28-14=14天，排卵窗口12-16天）
        for day in range(6, 12):
            phase = self.calculator.get_phase(day)
            self.assertEqual(phase, CyclePhase.FOLLICULAR,
                           f"Day {day} should be follicular phase")
    
    def test_get_phase_ovulation(self):
        """测试排卵期判断"""
        # 第12-16天应该是排卵期（排卵日14天，窗口前后各2天）
        for day in range(12, 17):
            phase = self.calculator.get_phase(day)
            self.assertEqual(phase, CyclePhase.OVULATION,
                           f"Day {day} should be ovulation phase")
    
    def test_get_phase_luteal(self):
        """测试黄体期判断"""
        # 第17-28天应该是黄体期
        for day in range(17, 29):
            phase = self.calculator.get_phase(day)
            self.assertEqual(phase, CyclePhase.LUTEAL,
                           f"Day {day} should be luteal phase")
    
    def test_get_fertility_low(self):
        """测试低生育能力期"""
        # 月经期和黄体期后半段应该是低生育能力
        fertility = self.calculator.get_fertility(1)  # 经期
        self.assertEqual(fertility, FertilityLevel.LOW)
        
        fertility = self.calculator.get_fertility(25)  # 黄体期后期
        self.assertEqual(fertility, FertilityLevel.LOW)
    
    def test_get_fertility_high(self):
        """测试高生育能力期（排卵窗口）"""
        # 排卵日前后2天应该是高生育能力
        ovulation_day = 28 - 14  # 第14天
        # 高生育能力期：排卵窗口内（第12-16天）且在易孕期（第9-15天）内
        # 所以高生育能力期 = 第12-15天
        for day in range(12, 16):  # 排卵窗口与易孕期重叠部分
            fertility = self.calculator.get_fertility(day)
            self.assertEqual(fertility, FertilityLevel.HIGH,
                           f"Day {day} should have high fertility")
    
    def test_get_fertility_medium(self):
        """测试中等生育能力期"""
        # 排卵前5天开始，排卵窗口之前（第9-11天）
        for day in range(9, 12):
            fertility = self.calculator.get_fertility(day)
            self.assertEqual(fertility, FertilityLevel.MEDIUM,
                           f"Day {day} should have medium fertility")
    
    def test_is_period_day(self):
        """测试经期判断"""
        for day in range(1, 6):
            self.assertTrue(self.calculator.is_period_day(day),
                          f"Day {day} should be period day")
        
        self.assertFalse(self.calculator.is_period_day(6))
        self.assertFalse(self.calculator.is_period_day(10))
    
    def test_is_ovulation_day(self):
        """测试排卵日判断"""
        ovulation_day = 28 - 14  # 第14天
        self.assertTrue(self.calculator.is_ovulation_day(ovulation_day))
        self.assertFalse(self.calculator.is_ovulation_day(ovulation_day - 1))
        self.assertFalse(self.calculator.is_ovulation_day(ovulation_day + 1))
    
    def test_is_fertile_day(self):
        """测试易孕期判断"""
        # 排卵前5天到排卵后1天是易孕期
        for day in range(9, 16):  # 第9-15天
            self.assertTrue(self.calculator.is_fertile_day(day),
                          f"Day {day} should be fertile day")
        
        self.assertFalse(self.calculator.is_fertile_day(1))  # 经期
        self.assertFalse(self.calculator.is_fertile_day(25))  # 黄体期后期
    
    def test_is_safe_day(self):
        """测试安全期判断"""
        # 经期后安全期（第6-8天）
        for day in range(6, 9):
            self.assertTrue(self.calculator.is_safe_day(day),
                          f"Day {day} should be safe day")
        
        # 经期前安全期（第21-27天，排除易孕期后）
        self.assertTrue(self.calculator.is_safe_day(25))
        
        # 经期不是安全期
        self.assertFalse(self.calculator.is_safe_day(1))
        
        # 易孕期不是安全期
        self.assertFalse(self.calculator.is_safe_day(14))
    
    def test_get_day_info(self):
        """测试获取日期详细信息"""
        day_info = self.calculator.get_day_info(self.base_date)
        
        self.assertEqual(day_info.date, self.base_date)
        self.assertEqual(day_info.day_of_cycle, 1)
        self.assertEqual(day_info.phase, CyclePhase.MENSTRUAL)
        self.assertEqual(day_info.fertility, FertilityLevel.LOW)
        self.assertTrue(day_info.is_period)
        self.assertFalse(day_info.is_ovulation)
        self.assertFalse(day_info.is_fertile)
        self.assertFalse(day_info.is_safe)
    
    def test_predict(self):
        """测试周期预测"""
        pred = self.calculator.predict()
        
        # 下次月经应该在28天后
        expected_next = self.base_date + timedelta(days=28)
        self.assertEqual(pred.next_period_start, expected_next)
        
        # 经期结束应该在开始后4天（5天经期）
        expected_end = expected_next + timedelta(days=4)
        self.assertEqual(pred.next_period_end, expected_end)
        
        # 排卵日应该在第14天
        expected_ovulation = self.base_date + timedelta(days=14)
        self.assertEqual(pred.ovulation_date, expected_ovulation)
    
    def test_predict_fertile_window(self):
        """测试易孕期预测"""
        pred = self.calculator.predict()
        
        # 易孕期应该是排卵前5天到排卵后1天
        ovulation = pred.ovulation_date
        
        self.assertEqual(pred.fertile_window_start, ovulation - timedelta(days=5))
        self.assertEqual(pred.fertile_window_end, ovulation + timedelta(days=1))
    
    def test_predict_multiple(self):
        """测试多周期预测"""
        predictions = self.calculator.predict_multiple(num_cycles=3)
        
        self.assertEqual(len(predictions), 3)
        
        # 检查周期连续性
        for i in range(1, 3):
            self.assertEqual(
                predictions[i].next_period_start,
                predictions[i-1].next_period_start + timedelta(days=28)
            )
    
    def test_analyze_regularity_regular(self):
        """测试规律周期分析"""
        history = [28, 28, 28, 28, 28]
        calc = MenstrualCycleCalculator(
            self.base_date,
            cycle_history=history
        )
        
        analysis = calc.analyze_regularity()
        
        self.assertEqual(analysis.average_length, 28)
        self.assertEqual(analysis.min_length, 28)
        self.assertEqual(analysis.max_length, 28)
        self.assertEqual(analysis.variance, 0)
        self.assertTrue(analysis.is_regular)
        self.assertEqual(analysis.regularity_score, 100)
    
    def test_analyze_regularity_irregular(self):
        """测试不规律周期分析"""
        history = [25, 35, 22, 38, 26, 40]
        calc = MenstrualCycleCalculator(
            self.base_date,
            cycle_history=history
        )
        
        analysis = calc.analyze_regularity()
        
        self.assertEqual(analysis.min_length, 22)
        self.assertEqual(analysis.max_length, 40)
        self.assertFalse(analysis.is_regular)
        self.assertLess(analysis.regularity_score, 100)
    
    def test_analyze_regularity_empty_history(self):
        """测试空历史数据分析"""
        calc = MenstrualCycleCalculator(self.base_date)
        analysis = calc.analyze_regularity()
        
        self.assertEqual(analysis.average_length, 28)
        self.assertTrue(analysis.is_regular)
        self.assertEqual(analysis.regularity_score, 100)
    
    def test_get_cycle_calendar(self):
        """测试周期日历生成"""
        calendar = self.calculator.get_cycle_calendar(
            start_date=self.base_date,
            num_days=10
        )
        
        self.assertEqual(len(calendar), 10)
        
        # 检查第一天的信息
        first_day = calendar[0]
        self.assertEqual(first_day.date, self.base_date)
        self.assertEqual(first_day.day_of_cycle, 1)
        
        # 检查连续性
        for i, day in enumerate(calendar):
            expected_date = self.base_date + timedelta(days=i)
            self.assertEqual(day.date, expected_date)
    
    def test_get_phase_description(self):
        """测试阶段描述"""
        desc = self.calculator.get_phase_description(CyclePhase.MENSTRUAL)
        self.assertIn("月经期", desc)
        
        desc = self.calculator.get_phase_description(CyclePhase.FOLLICULAR)
        self.assertIn("卵泡期", desc)
        
        desc = self.calculator.get_phase_description(CyclePhase.OVULATION)
        self.assertIn("排卵期", desc)
        
        desc = self.calculator.get_phase_description(CyclePhase.LUTEAL)
        self.assertIn("黄体期", desc)
    
    def test_get_recommendations(self):
        """测试获取建议"""
        # 月经期建议
        recs = self.calculator.get_recommendations(self.base_date)
        self.assertIn("饮食", recs)
        self.assertIn("运动", recs)
        self.assertIn("生活", recs)
        self.assertTrue(len(recs["饮食"]) > 0)
        
        # 排卵期建议
        ovulation_date = self.base_date + timedelta(days=14)
        recs = self.calculator.get_recommendations(ovulation_date)
        self.assertTrue(len(recs["饮食"]) > 0)
    
    def test_custom_cycle_length(self):
        """测试自定义周期长度"""
        calc = MenstrualCycleCalculator(
            self.base_date,
            cycle_length=35,  # 较长周期
            period_length=6
        )
        
        pred = calc.predict()
        
        # 下次月经应该在35天后
        expected = self.base_date + timedelta(days=35)
        self.assertEqual(pred.next_period_start, expected)
        
        # 排卵日应该在35-14=21天
        ovulation_day = 35 - 14
        expected_ovulation = self.base_date + timedelta(days=ovulation_day)
        self.assertEqual(pred.ovulation_date, expected_ovulation)
    
    def test_short_cycle(self):
        """测试短周期（21天）"""
        calc = MenstrualCycleCalculator(
            self.base_date,
            cycle_length=21,
            period_length=4
        )
        
        pred = calc.predict()
        
        expected = self.base_date + timedelta(days=21)
        self.assertEqual(pred.next_period_start, expected)
    
    def test_long_cycle(self):
        """测试长周期（40天）"""
        calc = MenstrualCycleCalculator(
            self.base_date,
            cycle_length=40,
            period_length=5
        )
        
        pred = calc.predict()
        
        expected = self.base_date + timedelta(days=40)
        self.assertEqual(pred.next_period_start, expected)


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def setUp(self):
        self.base_date = datetime(2024, 1, 1)
    
    def test_calculate_next_period(self):
        """测试计算下次月经"""
        next_start, next_end = calculate_next_period(
            self.base_date,
            cycle_length=28,
            period_length=5
        )
        
        expected_start = self.base_date + timedelta(days=28)
        expected_end = expected_start + timedelta(days=4)
        
        self.assertEqual(next_start, expected_start)
        self.assertEqual(next_end, expected_end)
    
    def test_get_fertile_days(self):
        """测试获取易孕期"""
        start, end = get_fertile_days(self.base_date, cycle_length=28)
        
        # 易孕期：排卵前5天到排卵后1天
        ovulation = self.base_date + timedelta(days=14)
        expected_start = ovulation - timedelta(days=5)
        expected_end = ovulation + timedelta(days=1)
        
        self.assertEqual(start, expected_start)
        self.assertEqual(end, expected_end)
    
    def test_get_ovulation_date(self):
        """测试获取排卵日期"""
        ovulation = get_ovulation_date(self.base_date, cycle_length=28)
        
        # 28天周期，排卵在14天
        expected = self.base_date + timedelta(days=14)
        self.assertEqual(ovulation, expected)
    
    def test_format_date(self):
        """测试日期格式化"""
        date = datetime(2024, 1, 15)
        formatted = format_date(date)
        self.assertEqual(formatted, "2024-01-15")


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_cycle_boundary_day1(self):
        """测试周期第1天"""
        base = datetime(2024, 1, 1)
        calc = MenstrualCycleCalculator(base, cycle_length=28)
        
        day_info = calc.get_day_info(base)
        self.assertEqual(day_info.day_of_cycle, 1)
        self.assertEqual(day_info.phase, CyclePhase.MENSTRUAL)
    
    def test_cycle_boundary_last_day(self):
        """测试周期最后一天"""
        base = datetime(2024, 1, 1)
        calc = MenstrualCycleCalculator(base, cycle_length=28)
        
        last_day = base + timedelta(days=27)
        day_info = calc.get_day_info(last_day)
        self.assertEqual(day_info.day_of_cycle, 28)
        self.assertEqual(day_info.phase, CyclePhase.LUTEAL)
    
    def test_cross_month_cycle(self):
        """测试跨月周期"""
        base = datetime(2024, 1, 25)
        calc = MenstrualCycleCalculator(base, cycle_length=28)
        
        pred = calc.predict()
        
        # 下次月经应该在2月
        self.assertEqual(pred.next_period_start.month, 2)
    
    def test_leap_year(self):
        """测试闰年"""
        base = datetime(2024, 2, 27)
        calc = MenstrualCycleCalculator(base, cycle_length=28)
        
        pred = calc.predict()
        
        # 2024年是闰年，2月有29天
        # 27 + 28 = 55，所以下次月经应该在3月
        self.assertEqual(pred.next_period_start.month, 3)
    
    def test_year_boundary(self):
        """测试跨年边界"""
        base = datetime(2024, 12, 20)
        calc = MenstrualCycleCalculator(base, cycle_length=28)
        
        pred = calc.predict()
        
        # 下次月经应该在2025年
        self.assertEqual(pred.next_period_start.year, 2025)


class TestCycleDayDataClass(unittest.TestCase):
    """CycleDay数据类测试"""
    
    def test_cycle_day_creation(self):
        """测试CycleDay创建"""
        day = datetime(2024, 1, 1)
        cycle_day = CycleDay(
            date=day,
            day_of_cycle=1,
            phase=CyclePhase.MENSTRUAL,
            fertility=FertilityLevel.LOW,
            is_period=True,
            is_ovulation=False,
            is_fertile=False,
            is_safe=False,
            description="周期第1天 | 月经期 | 经期中"
        )
        
        self.assertEqual(cycle_day.date, day)
        self.assertEqual(cycle_day.day_of_cycle, 1)
        self.assertEqual(cycle_day.phase, CyclePhase.MENSTRUAL)
        self.assertEqual(cycle_day.fertility, FertilityLevel.LOW)


if __name__ == "__main__":
    unittest.main()