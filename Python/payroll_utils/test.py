#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Payroll Utilities Tests
=====================================
Tests for payroll calculation module.

Author: AllToolkit Contributors
License: MIT
"""

import unittest
from decimal import Decimal

from mod import (
    # Enums
    SalaryType, CityCode, OvertimeType, BonusTaxMethod,
    
    # Data Classes
    SalaryParams, TaxResult, SocialInsuranceResult, HousingFundResult, PayrollResult,
    
    # Basic Functions
    calculate_hourly_rate, calculate_daily_rate, convert_salary,
    
    # Overtime Functions
    calculate_overtime_pay, calculate_overtime_pay_from_monthly,
    
    # Social Insurance Functions
    get_social_insurance_base, calculate_social_insurance,
    
    # Housing Fund Functions
    get_housing_fund_base, calculate_housing_fund,
    
    # Tax Functions
    find_tax_rate, calculate_monthly_tax, calculate_simple_monthly_tax,
    
    # Year-End Bonus Functions
    calculate_year_end_bonus_separate, compare_year_end_bonus_methods,
    find_year_end_bonus_optimal_split,
    
    # Payroll Functions
    calculate_payroll, calculate_payroll_from_params,
    
    # Summary Functions
    calculate_annual_summary,
    
    # Utility Functions
    format_salary_report, calculate_salary_increase_effect,
    
    # Constants
    BASIC_DEDUCTION, IIT_ANNUAL_RATES, OVERTIME_MULTIPLIERS,
)


class TestBasicSalaryFunctions(unittest.TestCase):
    """基础薪资函数测试"""
    
    def test_calculate_hourly_rate(self):
        """测试小时工资率计算"""
        result = calculate_hourly_rate(10000)
        self.assertAlmostEqual(result, 57.47, places=2)
        
        # 边界测试
        result = calculate_hourly_rate(0)
        self.assertEqual(result, 0)
    
    def test_calculate_daily_rate(self):
        """测试日工资率计算"""
        result = calculate_daily_rate(10000)
        self.assertAlmostEqual(result, 459.77, places=2)
    
    def test_convert_salary_monthly_to_hourly(self):
        """测试月薪转小时工资"""
        result = convert_salary(10000, SalaryType.MONTHLY, SalaryType.HOURLY)
        self.assertAlmostEqual(result, 57.47, places=2)
    
    def test_convert_salary_hourly_to_monthly(self):
        """测试小时工资转月薪"""
        result = convert_salary(50, SalaryType.HOURLY, SalaryType.MONTHLY)
        self.assertEqual(result, 8700)
    
    def test_convert_salary_daily_to_monthly(self):
        """测试日薪转月薪"""
        result = convert_salary(500, SalaryType.DAILY, SalaryType.MONTHLY)
        self.assertAlmostEqual(result, 10875, places=2)


class TestOvertimeFunctions(unittest.TestCase):
    """加班费函数测试"""
    
    def test_calculate_overtime_pay_weekday(self):
        """测试工作日加班费"""
        result = calculate_overtime_pay(50, {'weekday': 10})
        expected = 50 * 10 * 1.5
        self.assertEqual(result, expected)
    
    def test_calculate_overtime_pay_weekend(self):
        """测试周末加班费"""
        result = calculate_overtime_pay(50, {'weekend': 8})
        expected = 50 * 8 * 2.0
        self.assertEqual(result, expected)
    
    def test_calculate_overtime_pay_holiday(self):
        """测试节假日加班费"""
        result = calculate_overtime_pay(50, {'holiday': 4})
        expected = 50 * 4 * 3.0
        self.assertEqual(result, expected)
    
    def test_calculate_overtime_pay_mixed(self):
        """测试混合加班"""
        result = calculate_overtime_pay(50, {'weekday': 10, 'weekend': 8, 'holiday': 4})
        expected = 50 * (10 * 1.5 + 8 * 2.0 + 4 * 3.0)
        self.assertEqual(result, expected)
    
    def test_calculate_overtime_pay_from_monthly(self):
        """测试从月薪计算加班费"""
        result = calculate_overtime_pay_from_monthly(10000, {'weekday': 10})
        hourly = calculate_hourly_rate(10000)
        expected = hourly * 10 * 1.5
        self.assertAlmostEqual(result, expected, places=2)


class TestSocialInsuranceFunctions(unittest.TestCase):
    """社保函数测试"""
    
    def test_get_social_insurance_base_normal(self):
        """测试正常工资基数"""
        result = get_social_insurance_base(10000, CityCode.SHANGHAI)
        self.assertEqual(result, 10000)
    
    def test_get_social_insurance_base_below_min(self):
        """测试低于下限"""
        result = get_social_insurance_base(5000, CityCode.SHANGHAI)
        # 上海社保下限约 7310
        self.assertGreaterEqual(result, 7310)
    
    def test_get_social_insurance_base_above_max(self):
        """测试超过上限"""
        result = get_social_insurance_base(50000, CityCode.SHANGHAI)
        # 上海社保上限约 36549
        self.assertLessEqual(result, 36549)
    
    def test_calculate_social_insurance_shanghai(self):
        """测试上海社保计算"""
        result = calculate_social_insurance(10000, CityCode.SHANGHAI)
        
        # 上海个人社保比例：养老8% + 医疗2% + 失业0.5% = 10.5%
        self.assertAlmostEqual(result.pension_employee, 800, places=2)
        self.assertAlmostEqual(result.medical_employee, 200, places=2)
        self.assertAlmostEqual(result.unemployment_employee, 50, places=2)
        self.assertAlmostEqual(result.total_employee, 1050, places=2)
    
    def test_calculate_social_insurance_beijing(self):
        """测试北京社保计算"""
        result = calculate_social_insurance(10000, CityCode.BEIJING)
        
        # 北京个人社保比例：养老8% + 医疗2% + 失业0.2% = 10.2%
        self.assertAlmostEqual(result.pension_employee, 800, places=2)
        self.assertAlmostEqual(result.medical_employee, 200, places=2)
        self.assertAlmostEqual(result.unemployment_employee, 20, places=2)
        self.assertAlmostEqual(result.total_employee, 1020, places=2)
    
    def test_social_insurance_employer_part(self):
        """测试单位社保部分"""
        result = calculate_social_insurance(10000, CityCode.SHANGHAI)
        
        # 上海单位社保比例：养老16% + 医疗9.5% + 失业0.5% + 工伤0.26%
        self.assertAlmostEqual(result.pension_employer, 1600, places=2)
        self.assertGreater(result.total_employer, result.total_employee)


class TestHousingFundFunctions(unittest.TestCase):
    """公积金函数测试"""
    
    def test_calculate_housing_fund_shanghai(self):
        """测试上海公积金"""
        result = calculate_housing_fund(10000, CityCode.SHANGHAI)
        
        # 上海公积金比例：个人7%，单位7%
        self.assertAlmostEqual(result.amount_employee, 700, places=2)
        self.assertAlmostEqual(result.amount_employer, 700, places=2)
        self.assertAlmostEqual(result.total, 1400, places=2)
    
    def test_calculate_housing_fund_beijing(self):
        """测试北京公积金"""
        result = calculate_housing_fund(10000, CityCode.BEIJING)
        
        # 北京公积金比例：个人12%，单位12%
        self.assertAlmostEqual(result.amount_employee, 1200, places=2)
        self.assertAlmostEqual(result.amount_employer, 1200, places=2)
    
    def test_calculate_housing_fund_custom_rate(self):
        """测试自定义公积金比例"""
        result = calculate_housing_fund(10000, CityCode.SHANGHAI, custom_rate=0.05)
        
        self.assertAlmostEqual(result.amount_employee, 500, places=2)
        self.assertAlmostEqual(result.rate_employee, 0.05)


class TestTaxFunctions(unittest.TestCase):
    """个税函数测试"""
    
    def test_find_tax_rate_low(self):
        """测试低档税率"""
        limit, rate, deduction = find_tax_rate(2000)
        self.assertEqual(rate, 3)
        self.assertEqual(deduction, 0)
    
    def test_find_tax_rate_medium(self):
        """测试中档税率"""
        limit, rate, deduction = find_tax_rate(10000)
        self.assertEqual(rate, 10)
        self.assertEqual(deduction, 210)
    
    def test_find_tax_rate_high(self):
        """测试高档税率"""
        limit, rate, deduction = find_tax_rate(50000)
        self.assertEqual(rate, 30)
        self.assertEqual(deduction, 4410)
    
    def test_calculate_simple_monthly_tax_no_tax(self):
        """测试免税情况"""
        # 收入低于起征点
        result = calculate_simple_monthly_tax(4000)
        self.assertEqual(result, 0)
    
    def test_calculate_simple_monthly_tax_basic(self):
        """测试基础个税计算"""
        # 15000 - 5000 = 10000 应纳税所得额
        # 10000 * 10% - 210 = 790
        result = calculate_simple_monthly_tax(15000)
        self.assertEqual(result, 790)
    
    def test_calculate_simple_monthly_tax_with_deductions(self):
        """测试有扣除的个税"""
        # 15000 - 5000 - 1050 - 700 = 8250 应纳税所得额
        # 8250 * 10% - 210 = 615
        result = calculate_simple_monthly_tax(15000, 1050, 700)
        self.assertEqual(result, 615)
    
    def test_calculate_simple_monthly_tax_with_special_deduction(self):
        """测试有专项附加扣除"""
        # 15000 - 5000 - 1050 - 700 - 1000 = 7250 应纳税所得额
        # 7250 * 10% - 210 = 515
        result = calculate_simple_monthly_tax(15000, 1050, 700, 1000)
        self.assertEqual(result, 515)
    
    def test_calculate_monthly_tax_cumulative(self):
        """测试累计预扣预缴"""
        result = calculate_monthly_tax(15000, social_insurance=1050, housing_fund=700)
        
        self.assertGreater(result.gross_income, 0)
        self.assertGreater(result.tax_amount, 0)


class TestYearEndBonusFunctions(unittest.TestCase):
    """年终奖函数测试"""
    
    def test_calculate_year_end_bonus_separate_low(self):
        """测试低档年终奖"""
        # 30000 / 12 = 2500，适用3%税率
        result = calculate_year_end_bonus_separate(30000)
        self.assertEqual(result.tax_rate, 3)
        self.assertEqual(result.tax_amount, 900)  # 30000 * 3%
    
    def test_calculate_year_end_bonus_separate_medium(self):
        """测试中档年终奖"""
        # 120000 / 12 = 10000，适用10%税率
        result = calculate_year_end_bonus_separate(120000)
        self.assertEqual(result.tax_rate, 10)
        self.assertEqual(result.tax_amount, 11790)  # 120000 * 10% - 210
    
    def test_compare_year_end_bonus_methods(self):
        """测试年终奖计税方式比较"""
        comparison = compare_year_end_bonus_methods(30000, 10000)
        
        self.assertIn('separate', comparison)
        self.assertIn('combined', comparison)
        self.assertIn('recommended_method', comparison)
        self.assertIn('tax_saved', comparison)
    
    def test_find_year_end_bonus_optimal_split_critical_point(self):
        """测试年终奖临界点拆分"""
        # 36001 处于临界点
        optimal = find_year_end_bonus_optimal_split(36001, 10000)
        
        # 36000 和 36001 的税额差异显著
        self.assertIsNotNone(optimal)
    
    def test_year_end_bonus_net_calculation(self):
        """测试年终奖税后金额"""
        result = calculate_year_end_bonus_separate(36000)
        
        # 36000 / 12 = 3000，适用3%税率
        expected_net = 36000 - (36000 * 0.03)
        self.assertAlmostEqual(result.net_bonus, expected_net, places=2)


class TestPayrollFunctions(unittest.TestCase):
    """完整薪资计算测试"""
    
    def test_calculate_payroll_basic(self):
        """测试基础薪资计算"""
        params = SalaryParams(basic_salary=15000, city=CityCode.SHANGHAI)
        result = calculate_payroll(params)
        
        self.assertEqual(result.basic_salary, 15000)
        self.assertGreater(result.gross_salary, 0)
        self.assertGreater(result.social_insurance, 0)
        self.assertGreater(result.housing_fund, 0)
        self.assertGreater(result.net_salary, 0)
    
    def test_calculate_payroll_with_overtime(self):
        """测试含加班费计算"""
        params = SalaryParams(
            basic_salary=10000,
            overtime_hours={'weekday': 10, 'weekend': 8},
            city=CityCode.SHANGHAI
        )
        result = calculate_payroll(params)
        
        self.assertGreater(result.overtime_pay, 0)
        self.assertGreater(result.gross_salary, 10000)
    
    def test_calculate_payroll_with_bonus(self):
        """测试含奖金计算"""
        params = SalaryParams(
            basic_salary=15000,
            bonus=2000,
            city=CityCode.SHANGHAI
        )
        result = calculate_payroll(params)
        
        self.assertEqual(result.bonus, 2000)
    
    def test_calculate_payroll_employer_cost(self):
        """测试单位用工成本"""
        params = SalaryParams(basic_salary=10000, city=CityCode.SHANGHAI)
        result = calculate_payroll(params)
        
        # 单位成本应大于工资
        self.assertGreater(result.employer_cost, 10000)
    
    def test_calculate_payroll_from_params(self):
        """测试便捷计算函数"""
        result = calculate_payroll_from_params(15000, city='shanghai')
        
        self.assertIn('gross_salary', result)
        self.assertIn('net_salary', result)
        self.assertIn('income_tax', result)
    
    def test_calculate_payroll_different_cities(self):
        """测试不同城市计算"""
        shanghai = calculate_payroll_from_params(10000, city='shanghai')
        beijing = calculate_payroll_from_params(10000, city='beijing')
        
        # 不同城市社保公积金不同，税后工资不同
        self.assertNotEqual(shanghai['social_insurance'], beijing['social_insurance'])


class TestAnnualSummaryFunctions(unittest.TestCase):
    """年度汇总测试"""
    
    def test_calculate_annual_summary_basic(self):
        """测试年度汇总"""
        result = calculate_annual_summary(15000, 30000)
        
        # 年度税前 = 15000 * 12 + 30000 = 210000
        self.assertEqual(result['annual_gross'], 210000)
        self.assertGreater(result['annual_net'], 0)
        self.assertGreater(result['annual_income_tax'], 0)
    
    def test_calculate_annual_summary_with_bonus(self):
        """测试含年终奖年度汇总"""
        result = calculate_annual_summary(10000, 50000)
        
        self.assertIn('year_end_bonus_net', result)
        self.assertIn('bonus_tax_method', result)
    
    def test_calculate_annual_summary_partial_year(self):
        """测试非全年工作"""
        result = calculate_annual_summary(15000, 0, work_months=6)
        
        # 6个月税前 = 15000 * 6 = 90000
        self.assertEqual(result['annual_gross'], 90000)


class TestUtilityFunctions(unittest.TestCase):
    """辅助函数测试"""
    
    def test_format_salary_report(self):
        """测试薪资报告格式化"""
        params = SalaryParams(basic_salary=15000, city=CityCode.SHANGHAI)
        result = calculate_payroll(params)
        report = format_salary_report(result)
        
        self.assertIn('薪资计算报告', report)
        self.assertIn('基本工资', report)
        self.assertIn('税后工资', report)
    
    def test_calculate_salary_increase_effect(self):
        """测试涨薪效果"""
        effect = calculate_salary_increase_effect(15000, 5000)
        
        self.assertEqual(effect['gross_increase'], 5000)
        self.assertGreater(effect['net_increase'], 0)
        self.assertLess(effect['net_ratio'], 100)  # 实际到手比例小于100%
    
    def test_salary_increase_tax_impact(self):
        """测试涨薪对税的影响"""
        effect = calculate_salary_increase_effect(10000, 10000)
        
        # 涨薪会增加税额
        self.assertGreater(effect['tax_increase'], 0)
        # 实际到手比例会因为社保公积金等扣除低于100%
        self.assertLess(effect['net_ratio'], 100)
        self.assertGreater(effect['net_ratio'], 50)  # 但仍大于50%


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_zero_salary(self):
        """测试零工资"""
        result = calculate_payroll_from_params(0)
        
        self.assertEqual(result['gross_salary'], 0)
        self.assertEqual(result['income_tax'], 0)
    
    def test_very_high_salary(self):
        """测试高工资"""
        result = calculate_payroll_from_params(100000)
        
        # 高工资应适用较高税率
        self.assertGreater(result['income_tax'], 10000)
    
    def test_negative_bonus_validation(self):
        """测试负奖金参数校验"""
        with self.assertRaises(ValueError):
            params = SalaryParams(basic_salary=10000, bonus=-1000)
    
    def test_custom_social_insurance_base(self):
        """测试自定义社保基数"""
        params = SalaryParams(
            basic_salary=20000,
            social_insurance_base=15000,
            city=CityCode.SHANGHAI
        )
        result = calculate_payroll(params)
        
        # 自定义基数15000
        self.assertEqual(result.social_insurance_detail.base, 15000)
    
    def test_custom_housing_fund_base(self):
        """测试自定义公积金基数"""
        params = SalaryParams(
            basic_salary=20000,
            housing_fund_base=10000,
            city=CityCode.SHANGHAI
        )
        result = calculate_payroll(params)
        
        self.assertEqual(result.housing_fund_detail.base, 10000)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_payroll_workflow(self):
        """完整薪资计算流程"""
        # 创建薪资参数
        params = SalaryParams(
            basic_salary=20000,
            overtime_hours={'weekday': 20, 'weekend': 10},
            bonus=5000,
            allowances=1000,
            city=CityCode.SHANGHAI,
            special_deductions=2000,
        )
        
        # 计算薪资
        result = calculate_payroll(params)
        
        # 生成报告
        report = format_salary_report(result)
        
        # 验证完整性
        self.assertGreater(result.gross_salary, 20000)
        self.assertGreater(result.overtime_pay, 0)
        self.assertGreater(result.social_insurance, 0)
        self.assertGreater(result.housing_fund, 0)
        self.assertGreater(result.income_tax, 0)
        self.assertGreater(result.net_salary, 0)
        self.assertIn('税前合计', report)
    
    def test_year_end_bonus_optimization(self):
        """年终奖优化流程"""
        bonus = 100000
        monthly_salary = 15000
        
        # 比较计税方式
        comparison = compare_year_end_bonus_methods(bonus, monthly_salary)
        
        # 检查临界点
        optimal = find_year_end_bonus_optimal_split(bonus, monthly_salary)
        
        # 计算年度汇总
        annual = calculate_annual_summary(monthly_salary, bonus)
        
        self.assertIsNotNone(comparison['recommended_method'])
        self.assertIn('bonus_tax_saved', annual)


if __name__ == '__main__':
    # 运行测试
    unittest.main(verbosity=2)