"""
Persian Calendar Utilities - 测试用例

测试所有波斯历工具函数的正确性。
"""

import unittest
import sys
import os
from datetime import date, datetime

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from persian_calendar_utils import (
    is_leap_year_persian,
    days_in_persian_month,
    validate_persian_date,
    persian_to_jd,
    jd_to_persian,
    gregorian_to_jd,
    jd_to_gregorian,
    persian_to_gregorian,
    gregorian_to_persian,
    persian_from_date,
    persian_from_datetime,
    persian_to_date,
    format_persian_date,
    get_persian_month_name,
    get_persian_weekday_name,
    get_persian_weekday,
    persian_day_of_year,
    persian_days_in_year,
    persian_week_of_year,
    now_persian,
    persian_add_days,
    persian_diff_days,
    is_valid_persian_date,
    gregorian_year_to_persian_year,
    persian_year_to_gregorian_year,
)


class TestLeapYear(unittest.TestCase):
    """测试闰年判断"""
    
    def test_leap_year_basic(self):
        """测试基本闰年判断"""
        # 1403 是闰年（在33年周期的第1位）
        self.assertTrue(is_leap_year_persian(1403))
        # 1402 是平年
        self.assertFalse(is_leap_year_persian(1402))
    
    def test_leap_year_cycle(self):
        """测试33年周期中的闰年"""
        # 周期位置：1, 5, 9, 13, 17, 22, 26, 30
        leap_years_in_cycle = [1, 5, 9, 13, 17, 22, 26, 30]
        for pos in leap_years_in_cycle:
            self.assertTrue(is_leap_year_persian(pos))
            self.assertTrue(is_leap_year_persian(pos + 33))
        
        # 检查一些平年
        non_leap_years = [2, 3, 4, 6, 7, 8, 10, 11, 12]
        for year in non_leap_years:
            self.assertFalse(is_leap_year_persian(year))


class TestDaysInMonth(unittest.TestCase):
    """测试月份天数"""
    
    def test_first_six_months(self):
        """测试前6个月（31天）"""
        for month in range(1, 7):
            self.assertEqual(days_in_persian_month(1403, month), 31)
    
    def test_months_7_to_11(self):
        """测试7-11月（30天）"""
        for month in range(7, 12):
            self.assertEqual(days_in_persian_month(1403, month), 30)
    
    def test_esfand_leap_year(self):
        """测试闰年Esfand（第12月）"""
        self.assertEqual(days_in_persian_month(1403, 12), 30)  # 闰年
        self.assertEqual(days_in_persian_month(1402, 12), 29)  # 平年
    
    def test_invalid_month(self):
        """测试无效月份"""
        with self.assertRaises(ValueError):
            days_in_persian_month(1403, 0)
        with self.assertRaises(ValueError):
            days_in_persian_month(1403, 13)


class TestValidatePersianDate(unittest.TestCase):
    """测试日期验证"""
    
    def test_valid_dates(self):
        """测试有效日期"""
        self.assertTrue(validate_persian_date(1403, 1, 1))
        self.assertTrue(validate_persian_date(1403, 6, 31))
        self.assertTrue(validate_persian_date(1403, 12, 30))  # 闰年
    
    def test_invalid_month(self):
        """测试无效月份"""
        with self.assertRaises(ValueError):
            validate_persian_date(1403, 0, 1)
        with self.assertRaises(ValueError):
            validate_persian_date(1403, 13, 1)
    
    def test_invalid_day(self):
        """测试无效日期"""
        with self.assertRaises(ValueError):
            validate_persian_date(1403, 1, 0)
        with self.assertRaises(ValueError):
            validate_persian_date(1403, 1, 32)
        with self.assertRaises(ValueError):
            validate_persian_date(1402, 12, 30)  # 平年只有29天


class TestJulianDayConversion(unittest.TestCase):
    """测试儒略日转换"""
    
    def test_persian_to_jd_known_dates(self):
        """测试已知日期的儒略日"""
        # 波斯历1403年1月1日 = 2024年3月20日
        self.assertEqual(persian_to_jd(1403, 1, 1), gregorian_to_jd(2024, 3, 20))
        # 波斯历1402年12月29日 = 2024年3月19日
        self.assertEqual(persian_to_jd(1402, 12, 29), gregorian_to_jd(2024, 3, 19))
    
    def test_gregorian_to_jd_known_dates(self):
        """测试公历到儒略日"""
        # 2024年3月20日
        jd = gregorian_to_jd(2024, 3, 20)
        self.assertEqual(jd_to_gregorian(jd), (2024, 3, 20))
    
    def test_jd_to_persian_roundtrip(self):
        """测试儒略日到波斯历的往返转换"""
        for year in [1400, 1401, 1402, 1403, 1404]:
            for month in [1, 6, 12]:
                day = days_in_persian_month(year, month) // 2
                jd = persian_to_jd(year, month, day)
                result = jd_to_persian(jd)
                self.assertEqual(result, (year, month, day))
    
    def test_gregorian_jd_roundtrip(self):
        """测试公历儒略日往返"""
        dates = [(2024, 1, 1), (2024, 3, 20), (2024, 12, 31)]
        for y, m, d in dates:
            jd = gregorian_to_jd(y, m, d)
            result = jd_to_gregorian(jd)
            self.assertEqual(result, (y, m, d))


class TestDateConversion(unittest.TestCase):
    """测试日期转换"""
    
    def test_persian_to_gregorian_known(self):
        """测试已知日期转换"""
        # 波斯历1403年1月1日 = 公历2024年3月20日
        self.assertEqual(persian_to_gregorian(1403, 1, 1), (2024, 3, 20))
        # 波斯历1402年12月29日 = 公历2024年3月19日
        self.assertEqual(persian_to_gregorian(1402, 12, 29), (2024, 3, 19))
        # 波斯历1403年12月30日 = 公历2025年3月20日（闰年）
        self.assertEqual(persian_to_gregorian(1403, 12, 30), (2025, 3, 20))
    
    def test_gregorian_to_persian_known(self):
        """测试已知日期反向转换"""
        # 公历2024年3月20日 = 波斯历1403年1月1日
        self.assertEqual(gregorian_to_persian(2024, 3, 20), (1403, 1, 1))
        # 公历2024年3月19日 = 波斯历1402年12月29日
        self.assertEqual(gregorian_to_persian(2024, 3, 19), (1402, 12, 29))
        # 公历2025年3月20日 = 波斯历1403年12月30日（闰年最后一天）
        self.assertEqual(gregorian_to_persian(2025, 3, 20), (1403, 12, 30))
    
    def test_conversion_roundtrip(self):
        """测试转换往返"""
        # 波斯历 -> 公历 -> 波斯历
        persian_dates = [
            (1403, 1, 1),
            (1403, 6, 15),
            (1403, 12, 30),
            (1402, 12, 29),
        ]
        for py, pm, pd in persian_dates:
            gy, gm, gd = persian_to_gregorian(py, pm, pd)
            result = gregorian_to_persian(gy, gm, gd)
            self.assertEqual(result, (py, pm, pd))
        
        # 公历 -> 波斯历 -> 公历
        gregorian_dates = [
            (2024, 3, 20),
            (2024, 6, 15),
            (2024, 12, 31),
            (2025, 1, 1),
        ]
        for gy, gm, gd in gregorian_dates:
            py, pm, pd = gregorian_to_persian(gy, gm, gd)
            result = persian_to_gregorian(py, pm, pd)
            self.assertEqual(result, (gy, gm, gd))
    
    def test_new_year_2024(self):
        """测试2024年新年转换"""
        # 2024年春分大约在3月20日
        # 波斯历1403年开始于2024年3月20日
        for day in range(20, 25):
            persian = gregorian_to_persian(2024, 3, day)
            if day == 20:
                self.assertEqual(persian[0], 1403)
                self.assertEqual(persian[1], 1)
                self.assertEqual(persian[2], 1)
            else:
                self.assertEqual(persian[0], 1403)
                self.assertEqual(persian[1], 1)
                self.assertEqual(persian[2], day - 20 + 1)


class TestPythonDateConversion(unittest.TestCase):
    """测试Python date对象转换"""
    
    def test_persian_from_date(self):
        """测试从date对象转换"""
        d = date(2024, 3, 20)
        result = persian_from_date(d)
        self.assertEqual(result, (1403, 1, 1))
    
    def test_persian_from_datetime(self):
        """测试从datetime对象转换"""
        dt = datetime(2024, 3, 20, 12, 30)
        result = persian_from_datetime(dt)
        self.assertEqual(result, (1403, 1, 1))
    
    def test_persian_to_date(self):
        """测试转换为date对象"""
        result = persian_to_date(1403, 1, 1)
        self.assertEqual(result, date(2024, 3, 20))
    
    def test_date_roundtrip(self):
        """测试date对象往返转换"""
        original = date(2024, 6, 15)
        persian = persian_from_date(original)
        result = persian_to_date(*persian)
        self.assertEqual(result, original)


class TestFormatPersianDate(unittest.TestCase):
    """测试日期格式化"""
    
    def test_short_format(self):
        """测试短格式"""
        self.assertEqual(format_persian_date(1403, 1, 1), "1403/01/01")
        self.assertEqual(format_persian_date(1403, 12, 30), "1403/12/30")
    
    def test_long_format(self):
        """测试长格式"""
        result = format_persian_date(1403, 1, 1, "long")
        self.assertIn("1403", result)
        self.assertIn("فروردین", result)
    
    def test_full_format(self):
        """测试完整格式"""
        result = format_persian_date(1403, 1, 1, "full")
        self.assertIn("1", result)
        self.assertIn("فروردین", result)
        self.assertIn("1403", result)
    
    def test_english_format(self):
        """测试英语格式"""
        result = format_persian_date(1403, 1, 1, "long", "en")
        self.assertEqual(result, "1403 Farvardin 1")
        
        result = format_persian_date(1403, 1, 1, "full", "en")
        self.assertEqual(result, "1 Farvardin 1403")
    
    def test_invalid_format(self):
        """测试无效格式类型"""
        with self.assertRaises(ValueError):
            format_persian_date(1403, 1, 1, "invalid")


class TestMonthNames(unittest.TestCase):
    """测试月份名称"""
    
    def test_persian_month_names(self):
        """测试波斯语月份名称"""
        self.assertEqual(get_persian_month_name(1), "فروردین")
        self.assertEqual(get_persian_month_name(12), "اسفند")
    
    def test_english_month_names(self):
        """测试英语月份名称"""
        self.assertEqual(get_persian_month_name(1, "en"), "Farvardin")
        self.assertEqual(get_persian_month_name(12, "en"), "Esfand")
    
    def test_invalid_month_name(self):
        """测试无效月份"""
        with self.assertRaises(ValueError):
            get_persian_month_name(0)
        with self.assertRaises(ValueError):
            get_persian_month_name(13)


class TestWeekdayNames(unittest.TestCase):
    """测试星期名称"""
    
    def test_persian_weekday_names(self):
        """测试波斯语星期名称"""
        self.assertEqual(get_persian_weekday_name(0), "شنبه")  # Saturday
        self.assertEqual(get_persian_weekday_name(6), "جمعه")  # Friday
    
    def test_english_weekday_names(self):
        """测试英语星期名称"""
        self.assertEqual(get_persian_weekday_name(0, "en"), "Shanbeh")
        self.assertEqual(get_persian_weekday_name(6, "en"), "Jomeh")
    
    def test_invalid_weekday_name(self):
        """测试无效星期"""
        with self.assertRaises(ValueError):
            get_persian_weekday_name(-1)
        with self.assertRaises(ValueError):
            get_persian_weekday_name(7)


class TestPersianWeekday(unittest.TestCase):
    """测试星期计算"""
    
    def test_known_weekdays(self):
        """测试已知星期"""
        # 2024年3月20日是星期三
        # 波斯历中星期三对应索引4
        weekday = get_persian_weekday(1403, 1, 1)
        self.assertEqual(weekday, 4)  # Wednesday = Chaharshanbeh
    
    def test_weekday_consistency(self):
        """测试星期一致性"""
        # 连续几天的星期应该连续递增
        for day in range(1, 8):
            weekday = get_persian_weekday(1403, 1, day)
            expected = (4 + day - 1) % 7  # 从周三开始
            self.assertEqual(weekday, expected)


class TestDayOfYear(unittest.TestCase):
    """测试年日计算"""
    
    def test_first_day(self):
        """测试第一天"""
        self.assertEqual(persian_day_of_year(1403, 1, 1), 1)
    
    def test_last_day_leap(self):
        """测试闰年最后一天"""
        self.assertEqual(persian_day_of_year(1403, 12, 30), 366)
    
    def test_last_day_normal(self):
        """测试平年最后一天"""
        self.assertEqual(persian_day_of_year(1402, 12, 29), 365)
    
    def test_boundary_months(self):
        """测试月份边界"""
        self.assertEqual(persian_day_of_year(1403, 1, 31), 31)
        self.assertEqual(persian_day_of_year(1403, 7, 1), 187)


class TestDaysInYear(unittest.TestCase):
    """测试年天数"""
    
    def test_leap_year(self):
        """测试闰年"""
        self.assertEqual(persian_days_in_year(1403), 366)
    
    def test_normal_year(self):
        """测试平年"""
        self.assertEqual(persian_days_in_year(1402), 365)


class TestWeekOfYear(unittest.TestCase):
    """测试周数计算"""
    
    def test_first_week(self):
        """测试第一周"""
        self.assertEqual(persian_week_of_year(1403, 1, 1), 1)
        self.assertEqual(persian_week_of_year(1403, 1, 7), 1)
    
    def test_last_week(self):
        """测试最后一周"""
        last_week = persian_week_of_year(1403, 12, 30)
        self.assertTrue(last_week >= 52)


class TestNowPersian(unittest.TestCase):
    """测试当前日期"""
    
    def test_now_persian(self):
        """测试获取当前波斯历日期"""
        result = now_persian()
        self.assertEqual(len(result), 3)
        self.assertTrue(result[0] > 1300)  # 年份应该在合理范围
        self.assertTrue(1 <= result[1] <= 12)
        self.assertTrue(1 <= result[2] <= 31)
        
        # 与公历往返验证
        g_date = persian_to_gregorian(*result)
        today = date.today()
        self.assertEqual(g_date[0], today.year)
        self.assertEqual(g_date[1], today.month)
        self.assertEqual(g_date[2], today.day)


class TestAddDays(unittest.TestCase):
    """测试日期加减"""
    
    def test_add_positive_days(self):
        """测试增加天数"""
        # 1403年1月1日 + 30天 = 1403年1月31日（第1月有31天）
        result = persian_add_days(1403, 1, 1, 30)
        self.assertEqual(result, (1403, 1, 31))
        
        # 1403年1月1日 + 31天 = 1403年2月1日
        result = persian_add_days(1403, 1, 1, 31)
        self.assertEqual(result, (1403, 2, 1))
    
    def test_add_negative_days(self):
        """测试减少天数"""
        # 1403年1月1日 - 1天 = 1402年12月29日
        result = persian_add_days(1403, 1, 1, -1)
        self.assertEqual(result, (1402, 12, 29))
    
    def test_add_year_boundary(self):
        """测试跨年"""
        # 1402年12月29日 + 1天 = 1403年1月1日
        result = persian_add_days(1402, 12, 29, 1)
        self.assertEqual(result, (1403, 1, 1))
    
    def test_add_large_days(self):
        """测试增加大量天数"""
        # 增加366天（闰年天数）应该增加一年
        result = persian_add_days(1403, 1, 1, 366)
        self.assertEqual(result[0], 1404)


class TestDiffDays(unittest.TestCase):
    """测试天数差"""
    
    def test_same_date(self):
        """测试相同日期"""
        self.assertEqual(persian_diff_days(1403, 1, 1, 1403, 1, 1), 0)
    
    def test_positive_diff(self):
        """测试正差值"""
        self.assertEqual(persian_diff_days(1403, 1, 1, 1403, 1, 11), 10)
    
    def test_negative_diff(self):
        """测试负差值"""
        self.assertEqual(persian_diff_days(1403, 1, 11, 1403, 1, 1), -10)
    
    def test_cross_year_diff(self):
        """测试跨年差值"""
        diff = persian_diff_days(1402, 12, 29, 1403, 1, 1)
        self.assertEqual(diff, 1)


class TestIsValidPersianDate(unittest.TestCase):
    """测试日期有效性检查"""
    
    def test_valid_dates(self):
        """测试有效日期"""
        self.assertTrue(is_valid_persian_date(1403, 1, 1))
        self.assertTrue(is_valid_persian_date(1403, 12, 30))
    
    def test_invalid_dates(self):
        """测试无效日期"""
        self.assertFalse(is_valid_persian_date(1403, 0, 1))
        self.assertFalse(is_valid_persian_date(1403, 13, 1))
        self.assertFalse(is_valid_persian_date(1402, 12, 30))  # 平年
        self.assertFalse(is_valid_persian_date(1403, 1, 32))


class TestYearRangeConversion(unittest.TestCase):
    """测试年份范围转换"""
    
    def test_gregorian_to_persian_year_range(self):
        """测试公历到波斯历年份范围"""
        # 2024年跨越1402和1403年
        start, end = gregorian_year_to_persian_year(2024)
        self.assertEqual(start, 1402)
        self.assertEqual(end, 1403)
    
    def test_persian_to_gregorian_year_range(self):
        """测试波斯历到公历年份范围"""
        # 1403年跨越2024和2025年
        start, end = persian_year_to_gregorian_year(1403)
        self.assertEqual(start, 2024)
        self.assertEqual(end, 2025)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_conversion_cycle(self):
        """测试完整转换周期"""
        # 从波斯历开始，经过多种转换后返回
        original = (1403, 6, 15)
        
        # 波斯历 -> 公历
        g_date = persian_to_gregorian(*original)
        
        # 公历 -> date对象
        py_date = persian_to_date(*original)
        
        # date对象 -> 波斯历
        p_from_date = persian_from_date(py_date)
        
        # 波斯历 -> 公历（从date转换的结果）
        g_from_persian = persian_to_gregorian(*p_from_date)
        
        # 所有公历结果应该相同
        self.assertEqual(g_date, g_from_persian)
        self.assertEqual(original, p_from_date)
    
    def test_leap_year_consistency(self):
        """测试闰年一致性"""
        for year in range(1395, 1410):
            is_leap = is_leap_year_persian(year)
            days = persian_days_in_year(year)
            esfand_days = days_in_persian_month(year, 12)
            
            if is_leap:
                self.assertEqual(days, 366)
                self.assertEqual(esfand_days, 30)
            else:
                self.assertEqual(days, 365)
                self.assertEqual(esfand_days, 29)
    
    def test_month_names_all(self):
        """测试所有月份名称"""
        for month in range(1, 13):
            name_fa = get_persian_month_name(month)
            name_en = get_persian_month_name(month, "en")
            
            self.assertTrue(len(name_fa) > 0)
            self.assertTrue(len(name_en) > 0)


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestLeapYear))
    suite.addTests(loader.loadTestsFromTestCase(TestDaysInMonth))
    suite.addTests(loader.loadTestsFromTestCase(TestValidatePersianDate))
    suite.addTests(loader.loadTestsFromTestCase(TestJulianDayConversion))
    suite.addTests(loader.loadTestsFromTestCase(TestDateConversion))
    suite.addTests(loader.loadTestsFromTestCase(TestPythonDateConversion))
    suite.addTests(loader.loadTestsFromTestCase(TestFormatPersianDate))
    suite.addTests(loader.loadTestsFromTestCase(TestMonthNames))
    suite.addTests(loader.loadTestsFromTestCase(TestWeekdayNames))
    suite.addTests(loader.loadTestsFromTestCase(TestPersianWeekday))
    suite.addTests(loader.loadTestsFromTestCase(TestDayOfYear))
    suite.addTests(loader.loadTestsFromTestCase(TestDaysInYear))
    suite.addTests(loader.loadTestsFromTestCase(TestWeekOfYear))
    suite.addTests(loader.loadTestsFromTestCase(TestNowPersian))
    suite.addTests(loader.loadTestsFromTestCase(TestAddDays))
    suite.addTests(loader.loadTestsFromTestCase(TestDiffDays))
    suite.addTests(loader.loadTestsFromTestCase(TestIsValidPersianDate))
    suite.addTests(loader.loadTestsFromTestCase(TestYearRangeConversion))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    run_tests()