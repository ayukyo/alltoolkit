"""
Tests for Mortgage Calculator Utilities

Author: AllToolkit
Date: 2026-05-10
"""

import unittest
from datetime import datetime
from mortgage_utils import (
    MortgageCalculator,
    PrepaymentCalculator,
    calculate_affordability,
    calculate_lpr_spread,
    estimate_property_value,
    calc_equal_principal_interest,
    calc_equal_principal,
    compare_repayment_methods
)


class TestMortgageCalculator(unittest.TestCase):
    """房贷计算器测试"""
    
    def setUp(self):
        """测试初始化"""
        self.calc = MortgageCalculator(1000000, 4.9, 30)  # 100万，4.9%，30年
    
    def test_equal_principal_interest_monthly(self):
        """测试等额本息月供计算"""
        monthly = self.calc.equal_principal_interest_monthly()
        # 100万，4.9%，30年，月供应该在5300左右
        self.assertAlmostEqual(float(monthly), 5307.27, places=2)
    
    def test_equal_principal_interest_schedule_length(self):
        """测试等额本息还款计划表长度"""
        schedule = self.calc.equal_principal_interest_schedule()
        self.assertEqual(len(schedule), 360)  # 30年 = 360个月
    
    def test_equal_principal_interest_schedule_first_month(self):
        """测试等额本息第一期还款"""
        schedule = self.calc.equal_principal_interest_schedule()
        first = schedule[0]
        self.assertAlmostEqual(first['payment'], 5307.27, places=2)
        # 第一期利息 = 1000000 * 4.9% / 12
        self.assertAlmostEqual(first['interest'], 4083.33, places=2)
        # 第一期本金 = 月供 - 利息
        self.assertAlmostEqual(first['principal'], 1223.94, places=2)
    
    def test_equal_principal_interest_schedule_last_month(self):
        """测试等额本息最后一期还款"""
        schedule = self.calc.equal_principal_interest_schedule()
        last = schedule[-1]
        # 最后一期剩余本金应该接近0
        self.assertLess(last['remaining'], 1)
    
    def test_equal_principal_interest_total(self):
        """测试等额本息总还款"""
        summary = self.calc.equal_principal_interest_summary()
        # 总还款应该在191万左右（允许误差）
        self.assertAlmostEqual(summary['total_payment'], 1910615, places=-2)
        # 总利息应该在91万左右
        self.assertAlmostEqual(summary['total_interest'], 910615, places=-2)
    
    def test_equal_principal_schedule(self):
        """测试等额本金还款计划"""
        schedule = self.calc.equal_principal_schedule()
        self.assertEqual(len(schedule), 360)
        
        # 每月本金应该相同
        monthly_principal = 1000000 / 360
        for item in schedule:
            self.assertAlmostEqual(item['principal'], monthly_principal, places=2)
    
    def test_equal_principal_first_last_payment(self):
        """测试等额本金首末月还款"""
        summary = self.calc.equal_principal_summary()
        # 首月还款最高
        self.assertAlmostEqual(summary['first_month_payment'], 6861.11, places=2)
        # 末月还款最低（约2789）
        self.assertAlmostEqual(summary['last_month_payment'], 2789, places=0)
        # 总利息应该比等额本息少
        self.assertLess(summary['total_interest'], 
                       self.calc.equal_principal_interest_summary()['total_interest'])
    
    def test_compare_methods(self):
        """测试还款方式对比"""
        comparison = self.calc.compare_methods()
        self.assertIn('equal_principal_interest', comparison)
        self.assertIn('equal_principal', comparison)
        self.assertIn('comparison', comparison)
        # 等额本金应该节省利息
        self.assertGreater(comparison['comparison']['equal_principal_saves'], 0)
    
    def test_zero_interest_rate(self):
        """测试零利率情况"""
        calc_zero = MortgageCalculator(1000000, 0, 30)
        # 零利率时，月供 = 本金 / 期数
        monthly = calc_zero.equal_principal_interest_monthly()
        self.assertAlmostEqual(float(monthly), 2777.78, places=2)
    
    def test_short_term_loan(self):
        """测试短期贷款"""
        calc_short = MortgageCalculator(100000, 4.35, 1)  # 10万，4.35%，1年
        summary = calc_short.equal_principal_interest_summary()
        self.assertEqual(summary['years'], 1)
        # 12期月供约8531
        self.assertAlmostEqual(summary['monthly_payment'], 8531, places=0)
    
    def test_high_value_loan(self):
        """测试高额贷款"""
        calc_high = MortgageCalculator(5000000, 4.9, 30)  # 500万
        summary = calc_high.equal_principal_interest_summary()
        # 总还款应该在955万左右
        self.assertAlmostEqual(summary['total_payment'], 9553000, places=-3)


class TestPrepaymentCalculator(unittest.TestCase):
    """提前还款计算器测试"""
    
    def setUp(self):
        """测试初始化"""
        self.calc = MortgageCalculator(1000000, 4.9, 30)
        self.prepay_calc = PrepaymentCalculator(self.calc)
    
    def test_prepay_lump_sum_reduce_term(self):
        """测试一次性提前还款-缩短年限"""
        result = self.prepay_calc.prepay_lump_sum(
            paid_months=60,  # 已还5年
            prepay_amount=200000,  # 提前还20万
            reduce_term=True
        )
        self.assertIn('new_term', result)
        self.assertIn('term_saved', result)
        self.assertIn('interest_saved', result)
        self.assertGreater(result['interest_saved'], 0)
    
    def test_prepay_lump_sum_reduce_payment(self):
        """测试一次性提前还款-减少月供"""
        result = self.prepay_calc.prepay_lump_sum(
            paid_months=60,
            prepay_amount=200000,
            reduce_term=False
        )
        self.assertIn('remaining_term', result)
        self.assertIn('new_monthly_payment', result)
        self.assertIn('monthly_payment_saved', result)
        # 新月供应该小于原月供
        self.assertLess(result['new_monthly_payment'], result['original_monthly_payment'])
    
    def test_prepay_exceeds_principal(self):
        """测试提前还款金额超过剩余本金"""
        result = self.prepay_calc.prepay_lump_sum(
            paid_months=60,
            prepay_amount=10000000,  # 1000万
            reduce_term=False
        )
        self.assertIn('error', result)
    
    def test_prepay_partial_every_month(self):
        """测试每月额外还款"""
        result = self.prepay_calc.prepay_partial_every_month(
            paid_months=60,
            extra_monthly=1000  # 每月多还1000
        )
        self.assertIn('new_term', result)
        self.assertIn('term_saved', result)
        self.assertGreater(result['term_saved'], 0)
    
    def test_prepay_equal_principal(self):
        """测试等额本金方式的提前还款"""
        calc_ep = MortgageCalculator(1000000, 4.9, 30)
        prepay_ep = PrepaymentCalculator(calc_ep, 'equal_principal')
        result = prepay_ep.prepay_lump_sum(
            paid_months=60,
            prepay_amount=200000,
            reduce_term=False
        )
        self.assertIn('new_monthly_payment', result)


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_calc_equal_principal_interest(self):
        """测试等额本息便捷函数"""
        result = calc_equal_principal_interest(1000000, 4.9, 30)
        self.assertEqual(result['type'], '等额本息')
        self.assertEqual(result['years'], 30)
        self.assertAlmostEqual(result['monthly_payment'], 5307.27, places=2)
    
    def test_calc_equal_principal(self):
        """测试等额本金便捷函数"""
        result = calc_equal_principal(1000000, 4.9, 30)
        self.assertEqual(result['type'], '等额本金')
        self.assertGreater(result['first_month_payment'], result['last_month_payment'])
    
    def test_compare_repayment_methods(self):
        """测试对比便捷函数"""
        result = compare_repayment_methods(1000000, 4.9, 30)
        self.assertIn('equal_principal_interest', result)
        self.assertIn('equal_principal', result)


class TestAffordabilityCalculator(unittest.TestCase):
    """可负担性计算测试"""
    
    def test_calculate_affordability(self):
        """测试可负担贷款金额计算"""
        result = calculate_affordability(
            monthly_income=15000,
            monthly_debt=2000,
            annual_rate=4.9,
            years=30
        )
        self.assertIn('max_loan_amount', result)
        self.assertGreater(result['max_loan_amount'], 0)
    
    def test_affordability_insufficient_income(self):
        """测试收入不足情况"""
        result = calculate_affordability(
            monthly_income=3000,
            monthly_debt=2000,
            annual_rate=4.9,
            years=30
        )
        self.assertIn('error', result)
    
    def test_affordability_zero_debt(self):
        """测试无负债情况"""
        result = calculate_affordability(
            monthly_income=10000,
            monthly_debt=0,
            annual_rate=4.9,
            years=30
        )
        # 无负债时，可贷款金额应该更高
        self.assertGreater(result['max_loan_amount'], 0)


class TestLPRCalculator(unittest.TestCase):
    """LPR利率计算测试"""
    
    def test_lpr_calculation(self):
        """测试LPR利率房贷计算"""
        result = calculate_lpr_spread(
            base_rate=4.3,
            spread=0.6,
            principal=1000000,
            years=30
        )
        self.assertEqual(result['lpr_base_rate'], 4.3)
        self.assertEqual(result['spread_bp'], 60)  # 60个基点
        # 实际利率应为4.9（浮点精度问题）
        self.assertAlmostEqual(result['actual_rate'], 4.9, places=1)
    
    def test_lpr_negative_spread(self):
        """测试LPR负加点（利率优惠）"""
        result = calculate_lpr_spread(
            base_rate=4.3,
            spread=-0.2,  # 减20个基点
            principal=1000000,
            years=30
        )
        self.assertEqual(result['actual_rate'], 4.1)
        self.assertEqual(result['spread_bp'], -20)


class TestPropertyValueEstimator(unittest.TestCase):
    """房产估值估算测试"""
    
    def test_estimate_property_value(self):
        """测试根据月供反推房价"""
        result = estimate_property_value(
            monthly_payment=5000,
            annual_rate=4.9,
            years=30,
            down_payment_ratio=0.3
        )
        self.assertIn('max_loan_amount', result)
        self.assertIn('estimated_property_value', result)
        self.assertIn('down_payment', result)
        # 房价应该是贷款金额的约1.43倍（1/0.7）
        self.assertAlmostEqual(
            result['estimated_property_value'],
            result['max_loan_amount'] / 0.7,
            places=0
        )
    
    def test_estimate_with_different_down_payment(self):
        """测试不同首付比例"""
        result_30 = estimate_property_value(5000, 4.9, 30, 0.3)
        result_20 = estimate_property_value(5000, 4.9, 30, 0.2)
        # 验证房价计算公式正确
        self.assertAlmostEqual(
            result_30['estimated_property_value'],
            result_30['max_loan_amount'] / 0.7,
            places=0
        )
        # 两种比例下贷款金额相同
        self.assertAlmostEqual(result_30['max_loan_amount'], result_20['max_loan_amount'], places=0)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_very_small_loan(self):
        """测试小额贷款"""
        calc = MortgageCalculator(10000, 4.9, 1)
        summary = calc.equal_principal_interest_summary()
        self.assertEqual(summary['principal'], 10000)
    
    def test_high_interest_rate(self):
        """测试高利率"""
        calc = MortgageCalculator(100000, 10, 10)
        summary = calc.equal_principal_interest_summary()
        # 高利率下总利息应该显著高于本金
        self.assertGreater(summary['total_interest'], summary['principal'] * 0.5)
    
    def test_long_term_loan(self):
        """测试超长贷款期限"""
        calc = MortgageCalculator(1000000, 4.9, 30)
        schedule = calc.equal_principal_interest_schedule()
        self.assertEqual(len(schedule), 360)
    
    def test_equal_principal_interest_total_matches(self):
        """验证等额本息总还款 = 月供 * 期数（近似）"""
        calc = MortgageCalculator(1000000, 4.9, 30)
        summary = calc.equal_principal_interest_summary()
        # 总还款应该约等于月供 * 期数
        expected_total = summary['monthly_payment'] * 360
        # 允许一定误差（由于最后期尾差）
        self.assertAlmostEqual(summary['total_payment'], expected_total, places=-2)


class TestScheduleIntegrity(unittest.TestCase):
    """还款计划完整性测试"""
    
    def test_schedule_dates_sequential(self):
        """验证还款日期连续"""
        calc = MortgageCalculator(100000, 4.9, 5)
        schedule = calc.equal_principal_interest_schedule()
        
        for i in range(1, len(schedule)):
            prev_date = datetime.strptime(schedule[i-1]['date'], '%Y-%m-%d')
            curr_date = datetime.strptime(schedule[i]['date'], '%Y-%m-%d')
            # 相邻日期应该相差约1个月
            diff_days = (curr_date - prev_date).days
            self.assertGreaterEqual(diff_days, 28)
            self.assertLessEqual(diff_days, 31)
    
    def test_remaining_principal_decreasing(self):
        """验证剩余本金递减"""
        calc = MortgageCalculator(100000, 4.9, 5)
        schedule = calc.equal_principal_interest_schedule()
        
        for i in range(1, len(schedule)):
            self.assertLessEqual(
                schedule[i]['remaining'],
                schedule[i-1]['remaining']
            )
    
    def test_interest_decreasing(self):
        """验证等额本息利息递减"""
        calc = MortgageCalculator(100000, 4.9, 5)
        schedule = calc.equal_principal_interest_schedule()
        
        for i in range(1, len(schedule)):
            self.assertLessEqual(
                schedule[i]['interest'],
                schedule[i-1]['interest']
            )
    
    def test_principal_increasing(self):
        """验证等额本息本金递增"""
        calc = MortgageCalculator(100000, 4.9, 5)
        schedule = calc.equal_principal_interest_schedule()
        
        for i in range(1, len(schedule)):
            self.assertGreaterEqual(
                schedule[i]['principal'],
                schedule[i-1]['principal']
            )


if __name__ == '__main__':
    unittest.main()