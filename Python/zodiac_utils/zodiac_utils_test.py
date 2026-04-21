"""
Zodiac Utilities 测试模块

Author: AllToolkit
Version: 1.0.0
"""

import unittest
from datetime import datetime, date, timedelta
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    ZodiacUtils, ChineseZodiacUtils, Zodiac, ChineseZodiac, Element, Quality,
    get_zodiac, get_zodiac_from_date, get_chinese_zodiac, get_chinese_zodiac_from_date,
    calculate_zodiac_compatibility, calculate_chinese_zodiac_compatibility
)


class TestZodiacUtils(unittest.TestCase):
    """西方星座工具测试"""

    def test_get_zodiac_aries(self):
        """测试白羊座判断"""
        self.assertEqual(ZodiacUtils.get_zodiac(3, 21), Zodiac.ARIES)
        self.assertEqual(ZodiacUtils.get_zodiac(3, 25), Zodiac.ARIES)
        self.assertEqual(ZodiacUtils.get_zodiac(4, 19), Zodiac.ARIES)

    def test_get_zodiac_taurus(self):
        """测试金牛座判断"""
        self.assertEqual(ZodiacUtils.get_zodiac(4, 20), Zodiac.TAURUS)
        self.assertEqual(ZodiacUtils.get_zodiac(5, 15), Zodiac.TAURUS)
        self.assertEqual(ZodiacUtils.get_zodiac(5, 20), Zodiac.TAURUS)

    def test_get_zodiac_capricorn(self):
        """测试摩羯座判断（跨年星座）"""
        self.assertEqual(ZodiacUtils.get_zodiac(12, 25), Zodiac.CAPRICORN)
        self.assertEqual(ZodiacUtils.get_zodiac(1, 1), Zodiac.CAPRICORN)
        self.assertEqual(ZodiacUtils.get_zodiac(1, 15), Zodiac.CAPRICORN)
        self.assertEqual(ZodiacUtils.get_zodiac(1, 19), Zodiac.CAPRICORN)

    def test_get_zodiac_all(self):
        """测试所有星座边界"""
        test_cases = [
            ((1, 20), Zodiac.AQUARIUS),
            ((2, 19), Zodiac.PISCES),
            ((3, 21), Zodiac.ARIES),
            ((4, 20), Zodiac.TAURUS),
            ((5, 21), Zodiac.GEMINI),
            ((6, 22), Zodiac.CANCER),
            ((7, 23), Zodiac.LEO),
            ((8, 23), Zodiac.VIRGO),
            ((9, 23), Zodiac.LIBRA),
            ((10, 24), Zodiac.SCORPIO),
            ((11, 23), Zodiac.SAGITTARIUS),
            ((12, 22), Zodiac.CAPRICORN),
        ]
        for (month, day), expected in test_cases:
            with self.subTest(month=month, day=day):
                self.assertEqual(ZodiacUtils.get_zodiac(month, day), expected)

    def test_get_zodiac_invalid_month(self):
        """测试无效月份"""
        with self.assertRaises(ValueError):
            ZodiacUtils.get_zodiac(0, 15)
        with self.assertRaises(ValueError):
            ZodiacUtils.get_zodiac(13, 15)

    def test_get_zodiac_invalid_day(self):
        """测试无效日期"""
        with self.assertRaises(ValueError):
            ZodiacUtils.get_zodiac(5, 0)
        with self.assertRaises(ValueError):
            ZodiacUtils.get_zodiac(5, 32)

    def test_get_zodiac_from_date_datetime(self):
        """测试从 datetime 对象获取星座"""
        dt = datetime(1990, 7, 15)
        self.assertEqual(ZodiacUtils.get_zodiac_from_date(dt), Zodiac.CANCER)

    def test_get_zodiac_from_date_date(self):
        """测试从 date 对象获取星座"""
        d = date(1985, 12, 25)
        self.assertEqual(ZodiacUtils.get_zodiac_from_date(d), Zodiac.CAPRICORN)

    def test_get_zodiac_from_date_string(self):
        """测试从字符串获取星座"""
        self.assertEqual(ZodiacUtils.get_zodiac_from_date("1990-07-15"), Zodiac.CANCER)
        self.assertEqual(ZodiacUtils.get_zodiac_from_date("1990/07/15"), Zodiac.CANCER)

    def test_get_zodiac_from_date_timestamp(self):
        """测试从时间戳获取星座"""
        ts = datetime(1990, 7, 15).timestamp()
        self.assertEqual(ZodiacUtils.get_zodiac_from_date(ts), Zodiac.CANCER)

    def test_get_zodiac_info(self):
        """测试获取星座信息"""
        info = ZodiacUtils.get_zodiac_info(Zodiac.LEO)
        self.assertEqual(info["name"], Zodiac.LEO)
        self.assertEqual(info["element"], "火象")
        self.assertEqual(info["quality"], "固定宫")
        self.assertEqual(info["ruling_planet"], "太阳")
        self.assertIn(1, info["lucky_numbers"])
        self.assertIn("自信", info["personality_traits"])

    def test_get_element(self):
        """测试获取星座元素"""
        self.assertEqual(ZodiacUtils.get_element(Zodiac.ARIES), "火象")
        self.assertEqual(ZodiacUtils.get_element(Zodiac.TAURUS), "土象")
        self.assertEqual(ZodiacUtils.get_element(Zodiac.GEMINI), "风象")
        self.assertEqual(ZodiacUtils.get_element(Zodiac.CANCER), "水象")

    def test_get_quality(self):
        """测试获取星座属性"""
        self.assertEqual(ZodiacUtils.get_quality(Zodiac.ARIES), "基本宫")
        self.assertEqual(ZodiacUtils.get_quality(Zodiac.TAURUS), "固定宫")
        self.assertEqual(ZodiacUtils.get_quality(Zodiac.GEMINI), "变动宫")

    def test_get_ruling_planet(self):
        """测试获取守护星"""
        self.assertEqual(ZodiacUtils.get_ruling_planet(Zodiac.ARIES), "火星")
        self.assertEqual(ZodiacUtils.get_ruling_planet(Zodiac.LEO), "太阳")

    def test_get_lucky_numbers(self):
        """测试获取幸运数字"""
        numbers = ZodiacUtils.get_lucky_numbers(Zodiac.ARIES)
        self.assertIn(1, numbers)
        self.assertIn(9, numbers)

    def test_get_lucky_colors(self):
        """测试获取幸运颜色"""
        colors = ZodiacUtils.get_lucky_colors(Zodiac.ARIES)
        self.assertIn("红色", colors)

    def test_get_personality_traits(self):
        """测试获取性格特点"""
        traits = ZodiacUtils.get_personality_traits(Zodiac.ARIES)
        self.assertIn("热情", traits)
        self.assertIn("勇敢", traits)

    def test_calculate_compatibility_high(self):
        """测试高兼容性配对"""
        result = ZodiacUtils.calculate_compatibility(Zodiac.ARIES, Zodiac.LEO)
        self.assertEqual(result["zodiac1"], Zodiac.ARIES)
        self.assertEqual(result["zodiac2"], Zodiac.LEO)
        self.assertGreaterEqual(result["score"], 90)
        self.assertIn("契合", result["level"])

    def test_calculate_compatibility_same_element(self):
        """测试同元素配对"""
        result = ZodiacUtils.calculate_compatibility(Zodiac.TAURUS, Zodiac.VIRGO)
        self.assertGreaterEqual(result["score"], 85)

    def test_calculate_compatibility_different_element(self):
        """测试不同元素配对"""
        result = ZodiacUtils.calculate_compatibility(Zodiac.ARIES, Zodiac.CANCER)
        self.assertIsInstance(result["score"], int)
        self.assertIn("elements", result)

    def test_get_all_zodiacs(self):
        """测试获取所有星座"""
        zodiacs = ZodiacUtils.get_all_zodiacs()
        self.assertEqual(len(zodiacs), 12)
        self.assertIn(Zodiac.ARIES, zodiacs)
        self.assertIn(Zodiac.PISCES, zodiacs)

    def test_get_zodiacs_by_element(self):
        """测试按元素获取星座"""
        fire_zodiacs = ZodiacUtils.get_zodiacs_by_element(Element.FIRE)
        self.assertEqual(len(fire_zodiacs), 3)
        self.assertIn(Zodiac.ARIES, fire_zodiacs)
        self.assertIn(Zodiac.LEO, fire_zodiacs)
        self.assertIn(Zodiac.SAGITTARIUS, fire_zodiacs)

        # 测试字符串参数
        water_zodiacs = ZodiacUtils.get_zodiacs_by_element("水象")
        self.assertEqual(len(water_zodiacs), 3)

    def test_get_zodiacs_by_quality(self):
        """测试按属性获取星座"""
        cardinal = ZodiacUtils.get_zodiacs_by_quality(Quality.CARDINAL)
        self.assertEqual(len(cardinal), 4)
        self.assertIn(Zodiac.ARIES, cardinal)
        self.assertIn(Zodiac.CANCER, cardinal)
        self.assertIn(Zodiac.LIBRA, cardinal)
        self.assertIn(Zodiac.CAPRICORN, cardinal)

    def test_get_best_matches(self):
        """测试获取最佳配对"""
        matches = ZodiacUtils.get_best_matches(Zodiac.ARIES)
        self.assertEqual(len(matches), 3)
        for match in matches:
            self.assertIn("zodiac", match)
            self.assertIn("score", match)


class TestChineseZodiacUtils(unittest.TestCase):
    """中国生肖工具测试"""

    def test_get_zodiac_2020(self):
        """测试2020年（鼠年）"""
        self.assertEqual(ChineseZodiacUtils.get_zodiac(2020), ChineseZodiac.RAT)

    def test_get_zodiac_2021(self):
        """测试2021年（牛年）"""
        self.assertEqual(ChineseZodiacUtils.get_zodiac(2021), ChineseZodiac.OX)

    def test_get_zodiac_2024(self):
        """测试2024年（龙年）"""
        self.assertEqual(ChineseZodiacUtils.get_zodiac(2024), ChineseZodiac.DRAGON)

    def test_get_zodiac_all(self):
        """测试所有生肖年份"""
        test_cases = [
            (2020, ChineseZodiac.RAT),
            (2021, ChineseZodiac.OX),
            (2022, ChineseZodiac.TIGER),
            (2023, ChineseZodiac.RABBIT),
            (2024, ChineseZodiac.DRAGON),
            (2025, ChineseZodiac.SNAKE),
            (2026, ChineseZodiac.HORSE),
            (2027, ChineseZodiac.GOAT),
            (2028, ChineseZodiac.MONKEY),
            (2029, ChineseZodiac.ROOSTER),
            (2030, ChineseZodiac.DOG),
            (2031, ChineseZodiac.PIG),
        ]
        for year, expected in test_cases:
            with self.subTest(year=year):
                self.assertEqual(ChineseZodiacUtils.get_zodiac(year), expected)

    def test_get_zodiac_invalid_year(self):
        """测试无效年份"""
        with self.assertRaises(ValueError):
            ChineseZodiacUtils.get_zodiac(0)

    def test_get_zodiac_from_date(self):
        """测试从日期获取生肖"""
        dt = datetime(1990, 6, 15)
        self.assertEqual(ChineseZodiacUtils.get_zodiac_from_date(dt), ChineseZodiac.HORSE)

    def test_get_zodiac_year(self):
        """测试获取生肖年份列表"""
        years = ChineseZodiacUtils.get_zodiac_year(ChineseZodiac.DRAGON)
        self.assertIn(2024, years)
        self.assertIn(2012, years)
        self.assertIn(2000, years)
        # 相差12年
        for i in range(len(years) - 1):
            self.assertEqual(years[i + 1] - years[i], 12)

    def test_get_wuxing(self):
        """测试获取五行"""
        self.assertEqual(ChineseZodiacUtils.get_wuxing(2024), "木")  # 甲辰年
        self.assertEqual(ChineseZodiacUtils.get_wuxing(2025), "木")  # 乙巳年（乙属木）
        self.assertEqual(ChineseZodiacUtils.get_wuxing(2026), "火")  # 丙午年（丙属火）
        self.assertEqual(ChineseZodiacUtils.get_wuxing(2027), "火")  # 丁未年（丁属火）

    def test_get_benming_nian(self):
        """测试本命年判断"""
        current_year = datetime.now().year
        zodiac, is_benming = ChineseZodiacUtils.get_benming_nian(current_year)
        self.assertTrue(is_benming)

    def test_get_zodiac_info(self):
        """测试获取生肖信息"""
        info = ChineseZodiacUtils.get_zodiac_info(ChineseZodiac.DRAGON)
        self.assertEqual(info["name"], ChineseZodiac.DRAGON)
        self.assertIn("自信", info["personality"])
        self.assertIn("lucky_numbers", info)
        self.assertIn("lucky_colors", info)

    def test_get_all_zodiacs(self):
        """测试获取所有生肖"""
        zodiacs = ChineseZodiacUtils.get_all_zodiacs()
        self.assertEqual(len(zodiacs), 12)
        self.assertEqual(zodiacs[0], ChineseZodiac.RAT)
        self.assertEqual(zodiacs[11], ChineseZodiac.PIG)

    def test_calculate_compatibility_best(self):
        """测试最佳配对"""
        # 鼠和龙是六合
        result = ChineseZodiacUtils.calculate_compatibility(ChineseZodiac.RAT, ChineseZodiac.DRAGON)
        self.assertEqual(result["score"], 95)
        self.assertIn("合", result["level"])

    def test_calculate_compatibility_conflict(self):
        """测试相冲配对"""
        # 鼠和马相冲（相差6位）
        result = ChineseZodiacUtils.calculate_compatibility(ChineseZodiac.RAT, ChineseZodiac.HORSE)
        self.assertEqual(result["score"], 45)
        self.assertIn("冲", result["level"])

    def test_get_ganzhi(self):
        """测试干支纪年"""
        self.assertEqual(ChineseZodiacUtils.get_ganzhi(2024), "甲辰")
        self.assertEqual(ChineseZodiacUtils.get_ganzhi(2025), "乙巳")
        self.assertEqual(ChineseZodiacUtils.get_ganzhi(1984), "甲子")


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""

    def test_get_zodiac_function(self):
        """测试 get_zodiac 函数"""
        self.assertEqual(get_zodiac(7, 15), Zodiac.CANCER)

    def test_get_zodiac_from_date_function(self):
        """测试 get_zodiac_from_date 函数"""
        self.assertEqual(get_zodiac_from_date("1990-07-15"), Zodiac.CANCER)

    def test_get_chinese_zodiac_function(self):
        """测试 get_chinese_zodiac 函数"""
        self.assertEqual(get_chinese_zodiac(1990), ChineseZodiac.HORSE)

    def test_get_chinese_zodiac_from_date_function(self):
        """测试 get_chinese_zodiac_from_date 函数"""
        self.assertEqual(get_chinese_zodiac_from_date("1990-06-15"), ChineseZodiac.HORSE)

    def test_calculate_zodiac_compatibility_function(self):
        """测试 calculate_zodiac_compatibility 函数"""
        result = calculate_zodiac_compatibility(Zodiac.ARIES, Zodiac.LEO)
        self.assertGreaterEqual(result["score"], 90)

    def test_calculate_chinese_zodiac_compatibility_function(self):
        """测试 calculate_chinese_zodiac_compatibility 函数"""
        result = calculate_chinese_zodiac_compatibility(ChineseZodiac.RAT, ChineseZodiac.DRAGON)
        self.assertEqual(result["score"], 95)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""

    def test_leap_year_date(self):
        """测试闰年日期"""
        # 2000年是闰年
        self.assertEqual(ZodiacUtils.get_zodiac_from_date("2000-02-29"), Zodiac.PISCES)

    def test_year_boundary(self):
        """测试年份边界（摩羯座）"""
        # 12月31日
        self.assertEqual(ZodiacUtils.get_zodiac_from_date("2000-12-31"), Zodiac.CAPRICORN)
        # 1月1日
        self.assertEqual(ZodiacUtils.get_zodiac_from_date("2001-01-01"), Zodiac.CAPRICORN)

    def test_zodiac_boundary_dates(self):
        """测试星座边界日期"""
        # 白羊座结束，金牛座开始
        self.assertEqual(ZodiacUtils.get_zodiac(4, 19), Zodiac.ARIES)
        self.assertEqual(ZodiacUtils.get_zodiac(4, 20), Zodiac.TAURUS)

    def test_chinese_zodiac_cycle(self):
        """测试生肖周期（12年一循环）"""
        for base_year in [2000, 1980, 1960]:
            zodiac1 = ChineseZodiacUtils.get_zodiac(base_year)
            zodiac2 = ChineseZodiacUtils.get_zodiac(base_year + 12)
            zodiac3 = ChineseZodiacUtils.get_zodiac(base_year + 24)
            self.assertEqual(zodiac1, zodiac2)
            self.assertEqual(zodiac2, zodiac3)

    def test_datetime_with_time(self):
        """测试带时间的 datetime"""
        dt = datetime(1990, 7, 15, 14, 30, 0)
        self.assertEqual(ZodiacUtils.get_zodiac_from_date(dt), Zodiac.CANCER)


if __name__ == "__main__":
    unittest.main()