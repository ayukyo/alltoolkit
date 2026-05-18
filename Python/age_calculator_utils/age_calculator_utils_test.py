"""
Age Calculator Utilities 测试模块

Author: AllToolkit
Version: 1.0.0
"""

import unittest
from datetime import datetime, date, timedelta
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    AgeCalculatorUtils, Generation,
    calculate_age, calculate_exact_age, days_until_birthday,
    get_generation, format_age
)


class TestAgeCalculator(unittest.TestCase):
    """年龄计算基础测试"""
    
    def test_calculate_age_simple(self):
        """测试基本年龄计算"""
        # 假设今天是测试运行当天
        birth = date(1990, 5, 15)
        today = date(2024, 5, 20)
        age = AgeCalculatorUtils.calculate_age(birth, today)
        self.assertEqual(age, 34)
    
    def test_calculate_age_birthday_passed(self):
        """测试生日已过的情况"""
        birth = "1990-01-15"
        ref = "2024-06-01"
        age = calculate_age(birth, ref)
        self.assertEqual(age, 34)
    
    def test_calculate_age_birthday_not_passed(self):
        """测试生日未到的情况"""
        birth = "1990-12-15"
        ref = "2024-06-01"
        age = calculate_age(birth, ref)
        self.assertEqual(age, 33)
    
    def test_calculate_age_on_birthday(self):
        """测试生日当天"""
        birth = "1990-05-15"
        ref = "2024-05-15"
        age = calculate_age(birth, ref)
        self.assertEqual(age, 34)
    
    def test_calculate_age_day_before_birthday(self):
        """测试生日前一天"""
        birth = "1990-05-15"
        ref = "2024-05-14"
        age = calculate_age(birth, ref)
        self.assertEqual(age, 33)
    
    def test_calculate_age_newborn(self):
        """测试新生儿"""
        birth = date.today() - timedelta(days=10)
        age = calculate_age(birth)
        self.assertEqual(age, 0)
    
    def test_calculate_age_string_format(self):
        """测试字符串日期格式"""
        birth = "1990/05/15"
        ref = "2024/05/20"
        age = calculate_age(birth, ref, date_format="%Y/%m/%d")
        self.assertEqual(age, 34)


class TestExactAge(unittest.TestCase):
    """精确年龄计算测试"""
    
    def test_calculate_exact_age_basic(self):
        """测试基本精确年龄"""
        birth = "1990-03-15"
        ref = "2024-05-20"
        years, months, days = calculate_exact_age(birth, ref)
        self.assertEqual(years, 34)
        self.assertEqual(months, 2)
        self.assertEqual(days, 5)
    
    def test_calculate_exact_age_same_month(self):
        """测试同月精确年龄"""
        birth = "1990-03-15"
        ref = "2024-03-20"
        years, months, days = calculate_exact_age(birth, ref)
        self.assertEqual(years, 34)
        self.assertEqual(months, 0)
        self.assertEqual(days, 5)
    
    def test_calculate_exact_age_before_birthday_in_month(self):
        """测试生日月内但生日未到"""
        birth = "1990-03-20"
        ref = "2024-03-15"
        years, months, days = calculate_exact_age(birth, ref)
        self.assertEqual(years, 33)
        self.assertEqual(months, 11)
        self.assertEqual(days, 24)
    
    def test_calculate_exact_age_exact_birthday(self):
        """测试生日当天精确年龄"""
        birth = "1990-05-15"
        ref = "2024-05-15"
        years, months, days = calculate_exact_age(birth, ref)
        self.assertEqual(years, 34)
        self.assertEqual(months, 0)
        self.assertEqual(days, 0)


class TestAgeInDifferentUnits(unittest.TestCase):
    """不同单位年龄计算测试"""
    
    def test_age_in_days(self):
        """测试天数计算"""
        birth = "2024-01-01"
        ref = "2024-01-11"
        days = AgeCalculatorUtils.calculate_age_in_days(birth, ref)
        self.assertEqual(days, 10)
    
    def test_age_in_weeks(self):
        """测试周数计算"""
        birth = "2024-01-01"
        ref = "2024-01-22"  # 21天 = 3周
        weeks, days = AgeCalculatorUtils.calculate_age_in_weeks(birth, ref)
        self.assertEqual(weeks, 3)
        self.assertEqual(days, 0)
    
    def test_age_in_weeks_with_remainder(self):
        """测试带余数的周数计算"""
        birth = "2024-01-01"
        ref = "2024-01-25"  # 24天 = 3周3天
        weeks, days = AgeCalculatorUtils.calculate_age_in_weeks(birth, ref)
        self.assertEqual(weeks, 3)
        self.assertEqual(days, 3)
    
    def test_age_in_months(self):
        """测试月数计算"""
        birth = "2024-01-15"
        ref = "2024-06-20"
        months = AgeCalculatorUtils.calculate_age_in_months(birth, ref)
        self.assertEqual(months, 5)
    
    def test_age_in_hours(self):
        """测试小时计算"""
        birth = "2024-01-01"
        ref = "2024-01-02"
        hours = AgeCalculatorUtils.calculate_age_in_hours(birth, ref)
        self.assertEqual(hours, 24)


class TestBirthdayCountdown(unittest.TestCase):
    """生日倒计时测试"""
    
    def test_days_until_birthday_future(self):
        """测试未来生日倒计时"""
        birth = "1990-12-25"
        ref = "2024-06-01"
        days = days_until_birthday(birth, ref)
        # 从6月1日到12月25日大约207天
        self.assertGreater(days, 200)
    
    def test_days_until_birthday_passed(self):
        """测试已过生日的下次倒计时"""
        birth = "1990-03-01"
        ref = "2024-06-01"
        days = days_until_birthday(birth, ref)
        # 3月1日已过，计算到明年3月1日
        self.assertGreater(days, 250)
    
    def test_days_until_birthday_today(self):
        """测试生日当天"""
        birth = "1990-06-01"
        ref = "2024-06-01"
        days = days_until_birthday(birth, ref)
        self.assertEqual(days, 0)
    
    def test_next_birthday_date(self):
        """测试下一个生日日期"""
        birth = "1990-06-15"
        ref = "2024-06-01"
        next_bday = AgeCalculatorUtils.next_birthday_date(birth, ref)
        self.assertEqual(next_bday, date(2024, 6, 15))


class TestGeneration(unittest.TestCase):
    """代际分类测试"""
    
    def test_greatest_generation(self):
        """测试最伟大一代"""
        birth = "1920-05-15"
        gen = get_generation(birth)
        self.assertEqual(gen, Generation.GREATEST)
    
    def test_silent_generation(self):
        """测试沉默一代"""
        birth = "1935-05-15"
        gen = get_generation(birth)
        self.assertEqual(gen, Generation.SILENT)
    
    def test_baby_boomer(self):
        """测试婴儿潮一代"""
        birth = "1955-05-15"
        gen = get_generation(birth)
        self.assertEqual(gen, Generation.BABY_BOOMER)
    
    def test_generation_x(self):
        """测试X世代"""
        birth = "1975-05-15"
        gen = get_generation(birth)
        self.assertEqual(gen, Generation.GENERATION_X)
    
    def test_millennial(self):
        """测试千禧一代"""
        birth = "1990-05-15"
        gen = get_generation(birth)
        self.assertEqual(gen, Generation.MILLENNIAL)
    
    def test_generation_z(self):
        """测试Z世代"""
        birth = "2005-05-15"
        gen = get_generation(birth)
        self.assertEqual(gen, Generation.GENERATION_Z)
    
    def test_generation_alpha(self):
        """测试阿尔法世代"""
        birth = "2018-05-15"
        gen = get_generation(birth)
        self.assertEqual(gen, Generation.GENERATION_ALPHA)
    
    def test_get_generation_info(self):
        """测试代际详细信息"""
        birth = "1990-05-15"
        info = AgeCalculatorUtils.get_generation_info(birth)
        self.assertEqual(info["generation"], Generation.MILLENNIAL)
        self.assertEqual(info["year_range"], (1981, 1996))
        self.assertIn("characteristics", info)


class TestAgeDifference(unittest.TestCase):
    """年龄差异计算测试"""
    
    def test_age_difference(self):
        """测试年龄差计算"""
        date1 = "1990-05-15"
        date2 = "1985-05-15"
        diff = AgeCalculatorUtils.calculate_age_difference(date1, date2)
        self.assertEqual(diff["difference_years"], 5)
        self.assertEqual(diff["difference_months"], 0)
        self.assertEqual(diff["difference_days"], 365 * 5 + 1)  # 考虑闰年
    
    def test_age_difference_reversed(self):
        """测试反向日期差计算（结果应相同）"""
        date1 = "1985-05-15"
        date2 = "1990-05-15"
        diff = AgeCalculatorUtils.calculate_age_difference(date1, date2)
        self.assertEqual(diff["difference_years"], 5)


class TestAgeMilestones(unittest.TestCase):
    """年龄里程碑测试"""
    
    def test_get_age_milestones(self):
        """测试获取年龄里程碑"""
        birth = "1990-05-15"
        milestones = AgeCalculatorUtils.get_age_milestones(birth)
        self.assertGreater(len(milestones), 10)
        
        # 检查里程碑类型
        types = set(m["type"] for m in milestones)
        self.assertIn("年龄生日", types)
        self.assertIn("天数里程碑", types)
        self.assertIn("周数里程碑", types)
    
    def test_get_next_milestone(self):
        """测试获取下一个里程碑"""
        birth = "1990-05-15"
        milestone = AgeCalculatorUtils.get_next_milestone(birth)
        self.assertIsNotNone(milestone)
        self.assertIn("days_until", milestone)
        self.assertEqual(milestone["status"], "未到")


class TestChineseZodiac(unittest.TestCase):
    """中国生肖测试"""
    
    def test_chinese_zodiac_rat(self):
        """测试鼠年"""
        birth = "2020-01-01"  # 2020是鼠年
        zodiac = AgeCalculatorUtils.get_chinese_zodiac(birth)
        self.assertEqual(zodiac, "鼠")
    
    def test_chinese_zodiac_ox(self):
        """测试牛年"""
        birth = "2021-01-01"  # 2021是牛年
        zodiac = AgeCalculatorUtils.get_chinese_zodiac(birth)
        self.assertEqual(zodiac, "牛")
    
    def test_chinese_zodiac_dragon(self):
        """测试龙年"""
        birth = "2024-01-01"  # 2024是龙年
        zodiac = AgeCalculatorUtils.get_chinese_zodiac(birth)
        self.assertEqual(zodiac, "龙")
    
    def test_chinese_zodiac_cycle(self):
        """测试生肖周期"""
        # 2008是鼠年，2020也是鼠年
        zodiac_2008 = AgeCalculatorUtils.get_chinese_zodiac("2008-01-01")
        zodiac_2020 = AgeCalculatorUtils.get_chinese_zodiac("2020-01-01")
        self.assertEqual(zodiac_2008, zodiac_2020)


class TestLeapYearBaby(unittest.TestCase):
    """闰年生日宝宝测试"""
    
    def test_is_leap_year_baby_true(self):
        """测试闰年宝宝判定 - True"""
        birth = "2000-02-29"
        self.assertTrue(AgeCalculatorUtils.is_leap_year_baby(birth))
    
    def test_is_leap_year_baby_false(self):
        """测试闰年宝宝判定 - False"""
        birth = "2000-03-01"
        self.assertFalse(AgeCalculatorUtils.is_leap_year_baby(birth))
    
    def test_leap_year_baby_info(self):
        """测试闰年宝宝信息"""
        birth = "2000-02-29"
        ref = "2024-03-01"
        info = AgeCalculatorUtils.get_leap_year_birthday_info(birth, ref)
        self.assertTrue(info["is_leap_year_baby"])
        self.assertGreater(info["real_birthday_count"], 5)
    
    def test_non_leap_year_baby_info(self):
        """测试非闰年宝宝信息"""
        birth = "2000-03-01"
        info = AgeCalculatorUtils.get_leap_year_birthday_info(birth)
        self.assertFalse(info["is_leap_year_baby"])


class TestFormatAge(unittest.TestCase):
    """年龄格式化测试"""
    
    def test_format_age_full(self):
        """测试完整格式"""
        birth = "1990-03-15"
        ref = "2024-05-20"
        formatted = format_age(birth, ref, format_type="full")
        self.assertIn("岁", formatted)
        self.assertIn("个月", formatted)
        self.assertIn("天", formatted)
    
    def test_format_age_simple(self):
        """测试简单格式"""
        birth = "1990-05-15"
        ref = "2024-05-20"
        formatted = format_age(birth, ref, format_type="simple")
        self.assertEqual(formatted, "34岁")
    
    def test_format_age_days(self):
        """测试天数格式"""
        birth = "2024-01-01"
        ref = "2024-01-11"
        formatted = format_age(birth, ref, format_type="days")
        self.assertEqual(formatted, "10天")
    
    def test_format_age_weeks(self):
        """测试周数格式"""
        birth = "2024-01-01"
        ref = "2024-01-22"
        formatted = format_age(birth, ref, format_type="weeks")
        self.assertEqual(formatted, "3周0天")


class TestBirthdayInfo(unittest.TestCase):
    """生日信息测试"""
    
    def test_get_birthday_info(self):
        """测试获取生日信息"""
        birth = "1990-06-15"
        ref = "2024-06-01"
        info = AgeCalculatorUtils.get_birthday_info(birth, ref)
        
        self.assertEqual(info["current_age"], 33)
        self.assertEqual(info["days_until_birthday"], 14)
        self.assertFalse(info["is_birthday_today"])
        self.assertIn("total_days_lived", info)
    
    def test_get_birthday_info_today(self):
        """测试生日当天的信息"""
        birth = "1990-06-01"
        ref = "2024-06-01"
        info = AgeCalculatorUtils.get_birthday_info(birth, ref)
        
        self.assertEqual(info["current_age"], 34)
        self.assertEqual(info["days_until_birthday"], 0)
        self.assertTrue(info["is_birthday_today"])


if __name__ == "__main__":
    unittest.main(verbosity=2)