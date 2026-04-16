"""
Business Day Utils 测试文件

测试工作日计算工具库的所有功能
"""

import unittest
from datetime import date, timedelta
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    BusinessDayCalculator,
    BusinessDayConfig,
    Holiday,
    BusinessDayError,
    create_china_holiday_calculator,
    create_us_holiday_calculator,
    is_business_day,
    add_business_days,
    business_days_between,
    next_business_day,
    previous_business_day,
    _nth_weekday_of_month,
    _last_weekday_of_month
)


class TestBusinessDayConfig(unittest.TestCase):
    """测试工作日配置"""
    
    def test_default_config(self):
        """测试默认配置"""
        config = BusinessDayConfig()
        self.assertEqual(config.workdays, {0, 1, 2, 3, 4})
        self.assertEqual(config.weekends, {5, 6})
        self.assertEqual(len(config.holidays), 0)
    
    def test_add_holiday(self):
        """测试添加节假日"""
        config = BusinessDayConfig()
        config.add_holiday("元旦", date(2024, 1, 1))
        self.assertEqual(len(config.holidays), 1)
        self.assertEqual(config.holidays[0].name, "元旦")
        self.assertFalse(config.holidays[0].is_recurring)
    
    def test_add_recurring_holiday(self):
        """测试添加重复节假日"""
        config = BusinessDayConfig()
        config.add_holiday("元旦", date(2024, 1, 1), is_recurring=True)
        self.assertTrue(config.holidays[0].is_recurring)
    
    def test_add_adjusted_workday(self):
        """测试添加调休工作日"""
        config = BusinessDayConfig()
        config.add_adjusted_workday(date(2024, 1, 6))  # 周六调休
        self.assertIn(date(2024, 1, 6), config.adjusted_workdays)
    
    def test_remove_holiday(self):
        """测试移除节假日"""
        config = BusinessDayConfig()
        config.add_holiday("元旦", date(2024, 1, 1))
        config.add_holiday("春节", date(2024, 2, 10))
        config.remove_holiday("元旦")
        self.assertEqual(len(config.holidays), 1)
        self.assertEqual(config.holidays[0].name, "春节")


class TestHoliday(unittest.TestCase):
    """测试节假日类"""
    
    def test_fixed_holiday(self):
        """测试固定节假日"""
        holiday = Holiday("元旦", date(2024, 1, 1))
        self.assertTrue(holiday.matches(date(2024, 1, 1)))
        self.assertFalse(holiday.matches(date(2025, 1, 1)))
    
    def test_recurring_holiday(self):
        """测试重复节假日"""
        holiday = Holiday("元旦", date(2024, 1, 1), is_recurring=True)
        self.assertTrue(holiday.matches(date(2024, 1, 1)))
        self.assertTrue(holiday.matches(date(2025, 1, 1)))
        self.assertTrue(holiday.matches(date(2026, 1, 1)))
        self.assertFalse(holiday.matches(date(2024, 1, 2)))


class TestBusinessDayCalculator(unittest.TestCase):
    """测试工作日计算器"""
    
    def setUp(self):
        """设置测试环境"""
        self.config = BusinessDayConfig()
        self.calc = BusinessDayCalculator(self.config)
    
    def test_is_weekend(self):
        """测试周末判断"""
        # 2024年1月6日是周六
        self.assertTrue(self.calc.is_weekend(date(2024, 1, 6)))
        # 2024年1月7日是周日
        self.assertTrue(self.calc.is_weekend(date(2024, 1, 7)))
        # 2024年1月8日是周一
        self.assertFalse(self.calc.is_weekend(date(2024, 1, 8)))
    
    def test_is_business_day_weekday(self):
        """测试普通工作日判断"""
        # 2024年1月8日是周一
        self.assertTrue(self.calc.is_business_day(date(2024, 1, 8)))
        # 2024年1月6日是周六
        self.assertFalse(self.calc.is_business_day(date(2024, 1, 6)))
    
    def test_is_business_day_holiday(self):
        """测试节假日判断"""
        self.config.add_holiday("元旦", date(2024, 1, 1))
        # 2024年1月1日本是周一，但因为是节假日
        self.assertFalse(self.calc.is_business_day(date(2024, 1, 1)))
    
    def test_is_business_day_adjusted_workday(self):
        """测试调休工作日"""
        # 2024年1月6日是周六
        self.assertFalse(self.calc.is_business_day(date(2024, 1, 6)))
        
        # 添加调休
        self.config.add_adjusted_workday(date(2024, 1, 6))
        self.assertTrue(self.calc.is_business_day(date(2024, 1, 6)))
    
    def test_add_business_days_positive(self):
        """测试添加工作日（正向）"""
        # 2024年1月8日（周一）+ 5个工作日 = 2024年1月15日（周一）
        result = self.calc.add_business_days(date(2024, 1, 8), 5)
        self.assertEqual(result, date(2024, 1, 15))
        
        # 跨周末
        result = self.calc.add_business_days(date(2024, 1, 5), 3)  # 周五
        self.assertEqual(result, date(2024, 1, 10))  # 周三
    
    def test_add_business_days_negative(self):
        """测试添加工作日（负向）"""
        # 2024年1月15日（周一）- 5个工作日 = 2024年1月8日（周一）
        result = self.calc.add_business_days(date(2024, 1, 15), -5)
        self.assertEqual(result, date(2024, 1, 8))
    
    def test_add_business_days_zero(self):
        """测试添加0个工作日"""
        result = self.calc.add_business_days(date(2024, 1, 8), 0)
        self.assertEqual(result, date(2024, 1, 8))
    
    def test_business_days_between(self):
        """测试计算工作日数量"""
        # 2024年1月8日（周一）到2024年1月15日（周一）之间有4个工作日
        count = self.calc.business_days_between(date(2024, 1, 8), date(2024, 1, 15))
        self.assertEqual(count, 4)  # 9, 10, 11, 12 (周二到周五)
        
        # 反向计算
        count = self.calc.business_days_between(date(2024, 1, 15), date(2024, 1, 8))
        self.assertEqual(count, -4)
    
    def test_business_days_inclusive(self):
        """测试计算工作日数量（包含边界）"""
        # 2024年1月8日（周一）到2024年1月12日（周五）= 5个工作日
        count = self.calc.business_days_inclusive(date(2024, 1, 8), date(2024, 1, 12))
        self.assertEqual(count, 5)
    
    def test_next_business_day(self):
        """测试获取下一个工作日"""
        # 周五的下一个工作日是周一
        result = self.calc.next_business_day(date(2024, 1, 5))  # 周五
        self.assertEqual(result, date(2024, 1, 8))  # 周一
    
    def test_previous_business_day(self):
        """测试获取上一个工作日"""
        # 周一的上一个工作日是周五
        result = self.calc.previous_business_day(date(2024, 1, 8))  # 周一
        self.assertEqual(result, date(2024, 1, 5))  # 周五
    
    def test_get_business_days_in_range(self):
        """测试获取范围内的所有工作日"""
        # 2024年1月8日到2024年1月14日（跨越周末）
        days = self.calc.get_business_days_in_range(date(2024, 1, 8), date(2024, 1, 14))
        self.assertEqual(len(days), 5)  # 周一到周五
        self.assertEqual(days[0], date(2024, 1, 8))
        self.assertEqual(days[-1], date(2024, 1, 12))
    
    def test_nth_business_day_of_month(self):
        """测试获取某月第n个工作日"""
        # 2024年1月第1个工作日
        result = self.calc.nth_business_day_of_month(2024, 1, 1)
        self.assertEqual(result, date(2024, 1, 1))  # 周一
        
        # 2024年1月第5个工作日
        result = self.calc.nth_business_day_of_month(2024, 1, 5)
        self.assertEqual(result, date(2024, 1, 5))  # 周五
        
        # 2024年1月最后一个工作日
        result = self.calc.nth_business_day_of_month(2024, 1, -1)
        self.assertEqual(result, date(2024, 1, 31))  # 周三
    
    def test_business_days_in_month(self):
        """测试计算某月工作日数量"""
        # 2024年1月有31天，跨5周，工作日应该是23天
        count = self.calc.business_days_in_month(2024, 1)
        self.assertEqual(count, 23)
        
        # 2024年2月（闰年）29天
        count = self.calc.business_days_in_month(2024, 2)
        # 2024年2月1日是周四，2月29日是周四
        self.assertEqual(count, 21)
    
    def test_is_end_of_month_business_day(self):
        """测试是否为月末最后一个工作日"""
        # 2024年1月31日是周三，是最后一个工作日
        self.assertTrue(self.calc.is_end_of_month_business_day(date(2024, 1, 31)))
        
        # 2024年1月30日不是最后一个工作日
        self.assertFalse(self.calc.is_end_of_month_business_day(date(2024, 1, 30)))
    
    def test_get_month_end_business_day(self):
        """测试获取月末最后一个工作日"""
        result = self.calc.get_month_end_business_day(2024, 1)
        self.assertEqual(result, date(2024, 1, 31))  # 周三
        
        # 假设月末是周末的情况 - 2024年3月31日是周日
        result = self.calc.get_month_end_business_day(2024, 3)
        self.assertEqual(result, date(2024, 3, 29))  # 周五
    
    def test_get_week_start_end(self):
        """测试获取周开始和结束日期"""
        # 2024年1月10日是周三
        start, end = self.calc.get_week_start_end(date(2024, 1, 10))
        self.assertEqual(start, date(2024, 1, 8))  # 周一
        self.assertEqual(end, date(2024, 1, 14))  # 周日
    
    def test_business_days_in_week(self):
        """测试获取某周的所有工作日"""
        days = self.calc.business_days_in_week(date(2024, 1, 10))
        self.assertEqual(len(days), 5)
    
    def test_get_next_n_business_days(self):
        """测试获取接下来n个工作日"""
        # 从周五开始获取接下来3个工作日
        days = self.calc.get_next_n_business_days(date(2024, 1, 5), 3)
        self.assertEqual(len(days), 3)
        self.assertEqual(days[0], date(2024, 1, 8))  # 周一
        self.assertEqual(days[1], date(2024, 1, 9))  # 周二
        self.assertEqual(days[2], date(2024, 1, 10))  # 周三
    
    def test_get_previous_n_business_days(self):
        """测试获取之前n个工作日"""
        # 从周一开始获取之前3个工作日
        days = self.calc.get_previous_n_business_days(date(2024, 1, 8), 3)
        self.assertEqual(len(days), 3)
        self.assertEqual(days[0], date(2024, 1, 3))  # 周三
        self.assertEqual(days[1], date(2024, 1, 4))  # 周四
        self.assertEqual(days[2], date(2024, 1, 5))  # 周五
    
    def test_find_next_business_day_matching(self):
        """测试查找满足条件的下一个工作日"""
        # 找下一个15号（如果是工作日）
        result = self.calc.find_next_business_day_matching(
            date(2024, 1, 1),
            lambda d: d.day == 15
        )
        # 2024年1月15日是周一
        self.assertEqual(result, date(2024, 1, 15))
    
    def test_list_holidays_in_range(self):
        """测试列出范围内的节假日"""
        self.config.add_holiday("元旦", date(2024, 1, 1))
        self.config.add_holiday("春节", date(2024, 2, 10))
        
        holidays = self.calc.list_holidays_in_range(
            date(2024, 1, 1), date(2024, 2, 28)
        )
        self.assertEqual(len(holidays), 2)
    
    def test_custom_holiday_checker(self):
        """测试自定义节假日判断函数"""
        def custom_checker(d: date) -> bool:
            return d.day == 13 and d.month == 1  # 1月13日放假
        
        self.config.custom_holiday_checker = custom_checker
        self.assertFalse(self.calc.is_business_day(date(2024, 1, 13)))


class TestHolidayCalculatorFactories(unittest.TestCase):
    """测试节假日计算器工厂函数"""
    
    def test_create_china_holiday_calculator(self):
        """测试创建中国节假日计算器"""
        calc = create_china_holiday_calculator(2024)
        
        # 元旦
        is_hol, name = calc.is_holiday(date(2024, 1, 1))
        self.assertTrue(is_hol)
        self.assertEqual(name, "元旦")
        
        # 劳动节
        is_hol, name = calc.is_holiday(date(2024, 5, 1))
        self.assertTrue(is_hol)
        
        # 国庆节
        is_hol, name = calc.is_holiday(date(2024, 10, 1))
        self.assertTrue(is_hol)
    
    def test_create_us_holiday_calculator(self):
        """测试创建美国节假日计算器"""
        calc = create_us_holiday_calculator(2024)
        
        # 新年
        is_hol, name = calc.is_holiday(date(2024, 1, 1))
        self.assertTrue(is_hol)
        self.assertEqual(name, "New Year's Day")
        
        # 独立日
        is_hol, name = calc.is_holiday(date(2024, 7, 4))
        self.assertTrue(is_hol)
        
        # 圣诞节
        is_hol, name = calc.is_holiday(date(2024, 12, 25))
        self.assertTrue(is_hol)


class TestUtilityFunctions(unittest.TestCase):
    """测试工具函数"""
    
    def test_nth_weekday_of_month(self):
        """测试计算某月第n个某星期几"""
        # 2024年1月第3个周一
        result = _nth_weekday_of_month(2024, 1, 0, 3)  # weekday=0 是周一
        self.assertEqual(result, date(2024, 1, 15))
        
        # 2024年11月第4个周四（感恩节）
        result = _nth_weekday_of_month(2024, 11, 3, 4)  # weekday=3 是周四
        self.assertEqual(result, date(2024, 11, 28))
    
    def test_last_weekday_of_month(self):
        """测试计算某月最后一个某星期几"""
        # 2024年5月最后一个周一（阵亡将士纪念日）
        result = _last_weekday_of_month(2024, 5, 0)  # weekday=0 是周一
        self.assertEqual(result, date(2024, 5, 27))


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_is_business_day(self):
        """测试is_business_day便捷函数"""
        self.assertTrue(is_business_day(date(2024, 1, 8)))  # 周一
        self.assertFalse(is_business_day(date(2024, 1, 6)))  # 周六
    
    def test_add_business_days(self):
        """测试add_business_days便捷函数"""
        result = add_business_days(date(2024, 1, 8), 5)
        self.assertEqual(result, date(2024, 1, 15))
    
    def test_business_days_between(self):
        """测试business_days_between便捷函数"""
        count = business_days_between(date(2024, 1, 8), date(2024, 1, 15))
        self.assertEqual(count, 4)
    
    def test_next_business_day(self):
        """测试next_business_day便捷函数"""
        result = next_business_day(date(2024, 1, 5))  # 周五
        self.assertEqual(result, date(2024, 1, 8))  # 周一
    
    def test_previous_business_day(self):
        """测试previous_business_day便捷函数"""
        result = previous_business_day(date(2024, 1, 8))  # 周一
        self.assertEqual(result, date(2024, 1, 5))  # 周五


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def setUp(self):
        self.calc = BusinessDayCalculator()
    
    def test_year_boundary(self):
        """测试跨年边界"""
        # 从2024年12月31日（周二）加1个工作日
        result = self.calc.add_business_days(date(2024, 12, 31), 1)
        self.assertEqual(result, date(2025, 1, 1))  # 周三
    
    def test_month_boundary(self):
        """测试跨月边界"""
        # 从2024年1月31日（周三）加1个工作日
        result = self.calc.add_business_days(date(2024, 1, 31), 1)
        self.assertEqual(result, date(2024, 2, 1))  # 周四
    
    def test_large_offset(self):
        """测试大偏移量"""
        # 加100个工作日
        result = self.calc.add_business_days(date(2024, 1, 1), 100)
        # 100个工作日约等于20周
        self.assertTrue(result > date(2024, 1, 1))
    
    def test_consecutive_holidays(self):
        """测试连续节假日"""
        config = BusinessDayConfig()
        config.add_holiday("春节", date(2024, 2, 10))
        config.add_holiday("春节", date(2024, 2, 11))
        config.add_holiday("春节", date(2024, 2, 12))
        calc = BusinessDayCalculator(config)
        
        # 从春节前一天加1个工作日应该跳过春节假期
        result = calc.add_business_days(date(2024, 2, 9), 1)
        self.assertEqual(result, date(2024, 2, 13))


class TestDifferentWorkWeeks(unittest.TestCase):
    """测试不同的工作周配置"""
    
    def test_six_day_work_week(self):
        """测试六天工作制（周日休息）"""
        config = BusinessDayConfig(
            workdays={0, 1, 2, 3, 4, 5},  # 周一到周六
            weekends={6}  # 周日
        )
        calc = BusinessDayCalculator(config)
        
        # 周六应该是工作日
        self.assertTrue(calc.is_business_day(date(2024, 1, 6)))  # 周六
        # 周日应该不是工作日
        self.assertFalse(calc.is_business_day(date(2024, 1, 7)))  # 周日
    
    def test_middle_east_work_week(self):
        """测试中东工作周（周日到周四）"""
        config = BusinessDayConfig(
            workdays={0, 1, 2, 3, 6},  # 周一到周四 + 周日
            weekends={4, 5}  # 周五、周六
        )
        calc = BusinessDayCalculator(config)
        
        # 周五应该不是工作日
        self.assertFalse(calc.is_business_day(date(2024, 1, 5)))  # 周五
        # 周日应该是工作日
        self.assertTrue(calc.is_business_day(date(2024, 1, 7)))  # 周日


if __name__ == '__main__':
    unittest.main(verbosity=2)