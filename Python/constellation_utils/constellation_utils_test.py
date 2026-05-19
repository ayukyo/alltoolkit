"""
Constellation Utilities 测试文件

测试所有星座和生肖相关功能
"""

import unittest
from datetime import date
from mod import (
    Zodiac, Element, Quality, ChineseZodiac,
    get_zodiac, get_zodiac_from_date, get_zodiac_info,
    get_element, get_quality, get_ruling_planet,
    calculate_compatibility,
    get_chinese_zodiac, get_chinese_zodiac_info,
    calculate_chinese_compatibility,
    estimate_rising_sign,
    get_daily_horoscope,
    get_all_zodiacs, get_all_chinese_zodiacs,
    get_zodiac_by_chinese_name, get_chinese_zodiac_by_name,
    get_element_relationship,
    calculate_triple_harmony, calculate_six_harm,
    CONSTELLATION_DATA, CHINESE_ZODIAC_DATA,
)


class TestZodiac(unittest.TestCase):
    """测试星座功能"""
    
    def test_get_zodiac_aries(self):
        """测试白羊座判断"""
        self.assertEqual(get_zodiac(3, 21), Zodiac.ARIES)
        self.assertEqual(get_zodiac(4, 1), Zodiac.ARIES)
        self.assertEqual(get_zodiac(4, 19), Zodiac.ARIES)
    
    def test_get_zodiac_taurus(self):
        """测试金牛座判断"""
        self.assertEqual(get_zodiac(4, 20), Zodiac.TAURUS)
        self.assertEqual(get_zodiac(5, 10), Zodiac.TAURUS)
        self.assertEqual(get_zodiac(5, 20), Zodiac.TAURUS)
    
    def test_get_zodiac_gemini(self):
        """测试双子座判断"""
        self.assertEqual(get_zodiac(5, 21), Zodiac.GEMINI)
        self.assertEqual(get_zodiac(6, 10), Zodiac.GEMINI)
        self.assertEqual(get_zodiac(6, 21), Zodiac.GEMINI)
    
    def test_get_zodiac_cancer(self):
        """测试巨蟹座判断"""
        self.assertEqual(get_zodiac(6, 22), Zodiac.CANCER)
        self.assertEqual(get_zodiac(7, 10), Zodiac.CANCER)
        self.assertEqual(get_zodiac(7, 22), Zodiac.CANCER)
    
    def test_get_zodiac_leo(self):
        """测试狮子座判断"""
        self.assertEqual(get_zodiac(7, 23), Zodiac.LEO)
        self.assertEqual(get_zodiac(8, 10), Zodiac.LEO)
        self.assertEqual(get_zodiac(8, 22), Zodiac.LEO)
    
    def test_get_zodiac_virgo(self):
        """测试处女座判断"""
        self.assertEqual(get_zodiac(8, 23), Zodiac.VIRGO)
        self.assertEqual(get_zodiac(9, 10), Zodiac.VIRGO)
        self.assertEqual(get_zodiac(9, 22), Zodiac.VIRGO)
    
    def test_get_zodiac_libra(self):
        """测试天秤座判断"""
        self.assertEqual(get_zodiac(9, 23), Zodiac.LIBRA)
        self.assertEqual(get_zodiac(10, 10), Zodiac.LIBRA)
        self.assertEqual(get_zodiac(10, 23), Zodiac.LIBRA)
    
    def test_get_zodiac_scorpio(self):
        """测试天蝎座判断"""
        self.assertEqual(get_zodiac(10, 24), Zodiac.SCORPIO)
        self.assertEqual(get_zodiac(11, 10), Zodiac.SCORPIO)
        self.assertEqual(get_zodiac(11, 22), Zodiac.SCORPIO)
    
    def test_get_zodiac_sagittarius(self):
        """测试射手座判断"""
        self.assertEqual(get_zodiac(11, 23), Zodiac.SAGITTARIUS)
        self.assertEqual(get_zodiac(12, 10), Zodiac.SAGITTARIUS)
        self.assertEqual(get_zodiac(12, 21), Zodiac.SAGITTARIUS)
    
    def test_get_zodiac_capricorn(self):
        """测试摩羯座判断（跨年）"""
        self.assertEqual(get_zodiac(12, 22), Zodiac.CAPRICORN)
        self.assertEqual(get_zodiac(12, 31), Zodiac.CAPRICORN)
        self.assertEqual(get_zodiac(1, 1), Zodiac.CAPRICORN)
        self.assertEqual(get_zodiac(1, 10), Zodiac.CAPRICORN)
        self.assertEqual(get_zodiac(1, 19), Zodiac.CAPRICORN)
    
    def test_get_zodiac_aquarius(self):
        """测试水瓶座判断"""
        self.assertEqual(get_zodiac(1, 20), Zodiac.AQUARIUS)
        self.assertEqual(get_zodiac(2, 10), Zodiac.AQUARIUS)
        self.assertEqual(get_zodiac(2, 18), Zodiac.AQUARIUS)
    
    def test_get_zodiac_pisces(self):
        """测试双鱼座判断"""
        self.assertEqual(get_zodiac(2, 19), Zodiac.PISCES)
        self.assertEqual(get_zodiac(3, 10), Zodiac.PISCES)
        self.assertEqual(get_zodiac(3, 20), Zodiac.PISCES)
    
    def test_get_zodiac_invalid_month(self):
        """测试无效月份"""
        with self.assertRaises(ValueError):
            get_zodiac(0, 15)
        with self.assertRaises(ValueError):
            get_zodiac(13, 15)
    
    def test_get_zodiac_invalid_day(self):
        """测试无效日期"""
        with self.assertRaises(ValueError):
            get_zodiac(2, 30)  # 2月没有30号
        with self.assertRaises(ValueError):
            get_zodiac(4, 31)  # 4月没有31号
    
    def test_get_zodiac_from_date(self):
        """测试从日期对象获取星座"""
        self.assertEqual(get_zodiac_from_date(date(1990, 4, 15)), Zodiac.ARIES)
        self.assertEqual(get_zodiac_from_date(date(2000, 8, 25)), Zodiac.VIRGO)
        self.assertEqual(get_zodiac_from_date(date(1985, 12, 25)), Zodiac.CAPRICORN)


class TestZodiacInfo(unittest.TestCase):
    """测试星座信息功能"""
    
    def test_get_zodiac_info(self):
        """测试获取星座详细信息"""
        info = get_zodiac_info(Zodiac.LEO)
        self.assertEqual(info.zodiac, Zodiac.LEO)
        self.assertEqual(info.element, Element.FIRE)
        self.assertEqual(info.quality, Quality.FIXED)
        self.assertEqual(info.ruling_planet, "太阳")
        self.assertIn("慷慨", info.strengths)
    
    def test_get_element(self):
        """测试获取元素"""
        self.assertEqual(get_element(Zodiac.ARIES), Element.FIRE)
        self.assertEqual(get_element(Zodiac.TAURUS), Element.EARTH)
        self.assertEqual(get_element(Zodiac.GEMINI), Element.AIR)
        self.assertEqual(get_element(Zodiac.CANCER), Element.WATER)
    
    def test_get_quality(self):
        """测试获取特质"""
        self.assertEqual(get_quality(Zodiac.ARIES), Quality.CARDINAL)
        self.assertEqual(get_quality(Zodiac.TAURUS), Quality.FIXED)
        self.assertEqual(get_quality(Zodiac.GEMINI), Quality.MUTABLE)
    
    def test_get_ruling_planet(self):
        """测试获取守护星"""
        self.assertEqual(get_ruling_planet(Zodiac.ARIES), "火星")
        self.assertEqual(get_ruling_planet(Zodiac.TAURUS), "金星")
        self.assertEqual(get_ruling_planet(Zodiac.CANCER), "月亮")
        self.assertEqual(get_ruling_planet(Zodiac.LEO), "太阳")
    
    def test_all_zodiacs_have_complete_info(self):
        """测试所有星座都有完整信息"""
        for zodiac in Zodiac:
            info = get_zodiac_info(zodiac)
            self.assertIsNotNone(info.date_range)
            self.assertIsNotNone(info.element)
            self.assertIsNotNone(info.quality)
            self.assertGreater(len(info.lucky_numbers), 0)
            self.assertGreater(len(info.strengths), 0)
            self.assertGreater(len(info.compatible_signs), 0)


class TestCompatibility(unittest.TestCase):
    """测试配对功能"""
    
    def test_same_element_compatibility(self):
        """测试同元素星座配对"""
        # 火象星座之间
        result = calculate_compatibility(Zodiac.ARIES, Zodiac.LEO)
        self.assertGreaterEqual(result["score"], 60)
        self.assertTrue(result["element_match"])
    
    def test_compatible_signs(self):
        """测试最佳配对星座"""
        result = calculate_compatibility(Zodiac.ARIES, Zodiac.SAGITTARIUS)
        self.assertTrue(result["compatible"])
        self.assertGreaterEqual(result["score"], 70)
    
    def test_different_element_compatibility(self):
        """测试不同元素星座配对"""
        result = calculate_compatibility(Zodiac.ARIES, Zodiac.TAURUS)
        self.assertLess(result["score"], 80)
    
    def test_compatibility_return_values(self):
        """测试配对返回值结构"""
        result = calculate_compatibility(Zodiac.GEMINI, Zodiac.LIBRA)
        self.assertIn("zodiac1", result)
        self.assertIn("zodiac2", result)
        self.assertIn("score", result)
        self.assertIn("description", result)
        self.assertIn("element_match", result)
        self.assertIn("compatible", result)
        self.assertGreaterEqual(result["score"], 0)
        self.assertLessEqual(result["score"], 100)


class TestChineseZodiac(unittest.TestCase):
    """测试生肖功能"""
    
    def test_get_chinese_zodiac_rat(self):
        """测试鼠年"""
        self.assertEqual(get_chinese_zodiac(2020), ChineseZodiac.RAT)
        self.assertEqual(get_chinese_zodiac(2008), ChineseZodiac.RAT)
        self.assertEqual(get_chinese_zodiac(1996), ChineseZodiac.RAT)
    
    def test_get_chinese_zodiac_ox(self):
        """测试牛年"""
        self.assertEqual(get_chinese_zodiac(2021), ChineseZodiac.OX)
        self.assertEqual(get_chinese_zodiac(2009), ChineseZodiac.OX)
    
    def test_get_chinese_zodiac_tiger(self):
        """测试虎年"""
        self.assertEqual(get_chinese_zodiac(2022), ChineseZodiac.TIGER)
        self.assertEqual(get_chinese_zodiac(2010), ChineseZodiac.TIGER)
    
    def test_get_chinese_zodiac_dragon(self):
        """测试龙年"""
        self.assertEqual(get_chinese_zodiac(2024), ChineseZodiac.DRAGON)
        self.assertEqual(get_chinese_zodiac(2012), ChineseZodiac.DRAGON)
        self.assertEqual(get_chinese_zodiac(2000), ChineseZodiac.DRAGON)
    
    def test_get_chinese_zodiac_all(self):
        """测试所有生肖"""
        expected = [
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
        for year, zodiac in expected:
            self.assertEqual(get_chinese_zodiac(year), zodiac)
    
    def test_get_chinese_zodiac_invalid_year(self):
        """测试无效年份"""
        with self.assertRaises(ValueError):
            get_chinese_zodiac(1899)
        with self.assertRaises(ValueError):
            get_chinese_zodiac(2101)
    
    def test_get_chinese_zodiac_info(self):
        """测试获取生肖详细信息"""
        info = get_chinese_zodiac_info(ChineseZodiac.DRAGON)
        self.assertEqual(info.zodiac, ChineseZodiac.DRAGON)
        self.assertIn(2024, info.years)
        self.assertIn("龙", ChineseZodiac.DRAGON.value)
        self.assertGreater(len(info.strengths), 0)
    
    def test_all_chinese_zodiacs_have_complete_info(self):
        """测试所有生肖都有完整信息"""
        for zodiac in ChineseZodiac:
            info = get_chinese_zodiac_info(zodiac)
            self.assertIsNotNone(info.element)
            self.assertGreater(len(info.years), 0)
            self.assertGreater(len(info.compatible_signs), 0)


class TestChineseCompatibility(unittest.TestCase):
    """测试生肖配对功能"""
    
    def test_compatible_chinese_zodiacs(self):
        """测试相合生肖"""
        # 鼠和牛相合
        result = calculate_chinese_compatibility(ChineseZodiac.RAT, ChineseZodiac.OX)
        self.assertTrue(result["compatible"])
    
    def test_incompatible_chinese_zodiacs(self):
        """测试相冲生肖"""
        # 鼠和马相冲
        result = calculate_chinese_compatibility(ChineseZodiac.RAT, ChineseZodiac.HORSE)
        self.assertTrue(result["incompatible"])
        self.assertLess(result["score"], 50)
    
    def test_chinese_compatibility_return_values(self):
        """测试生肖配对返回值结构"""
        result = calculate_chinese_compatibility(ChineseZodiac.DRAGON, ChineseZodiac.MONKEY)
        self.assertIn("zodiac1", result)
        self.assertIn("zodiac2", result)
        self.assertIn("score", result)
        self.assertIn("description", result)
        self.assertGreaterEqual(result["score"], 0)
        self.assertLessEqual(result["score"], 100)


class TestRisingSign(unittest.TestCase):
    """测试上升星座功能"""
    
    def test_estimate_rising_sign_morning(self):
        """测试早晨出生的上升星座"""
        rising = estimate_rising_sign((7, 30), Zodiac.ARIES)
        self.assertIsInstance(rising, Zodiac)
    
    def test_estimate_rising_sign_noon(self):
        """测试中午出生的上升星座"""
        rising = estimate_rising_sign((12, 0), Zodiac.TAURUS)
        self.assertIsInstance(rising, Zodiac)
    
    def test_estimate_rising_sign_evening(self):
        """测试晚上出生的上升星座"""
        rising = estimate_rising_sign((20, 30), Zodiac.GEMINI)
        self.assertIsInstance(rising, Zodiac)
    
    def test_estimate_rising_sign_midnight(self):
        """测试午夜出生的上升星座"""
        rising = estimate_rising_sign((0, 0), Zodiac.CANCER)
        self.assertIsInstance(rising, Zodiac)
    
    def test_estimate_rising_sign_invalid_time(self):
        """测试无效时间"""
        with self.assertRaises(ValueError):
            estimate_rising_sign((25, 0), Zodiac.LEO)
        with self.assertRaises(ValueError):
            estimate_rising_sign((12, 60), Zodiac.LEO)


class TestHoroscope(unittest.TestCase):
    """测试运势功能"""
    
    def test_get_daily_horoscope(self):
        """测试获取每日运势"""
        horoscope = get_daily_horoscope(Zodiac.LEO)
        self.assertEqual(horoscope["zodiac"], "狮子座")
        self.assertIn("overall", horoscope)
        self.assertIn("love", horoscope)
        self.assertIn("career", horoscope)
        self.assertIn("wealth", horoscope)
        self.assertIn("health", horoscope)
        self.assertIn("lucky_color", horoscope)
        self.assertIn("lucky_number", horoscope)
        self.assertIn("tip", horoscope)
    
    def test_get_daily_horoscope_with_seed(self):
        """测试带种子的运势（可重复）"""
        horoscope1 = get_daily_horoscope(Zodiac.ARIES, seed=42)
        horoscope2 = get_daily_horoscope(Zodiac.ARIES, seed=42)
        self.assertEqual(horoscope1["overall"], horoscope2["overall"])
    
    def test_get_daily_horoscope_all_zodiacs(self):
        """测试所有星座的运势"""
        for zodiac in Zodiac:
            horoscope = get_daily_horoscope(zodiac)
            self.assertEqual(horoscope["zodiac"], zodiac.value)


class TestUtilityFunctions(unittest.TestCase):
    """测试工具函数"""
    
    def test_get_all_zodiacs(self):
        """测试获取所有星座"""
        zodiacs = get_all_zodiacs()
        self.assertEqual(len(zodiacs), 12)
        self.assertIn(Zodiac.ARIES, zodiacs)
        self.assertIn(Zodiac.PISCES, zodiacs)
    
    def test_get_all_chinese_zodiacs(self):
        """测试获取所有生肖"""
        zodiacs = get_all_chinese_zodiacs()
        self.assertEqual(len(zodiacs), 12)
        self.assertIn(ChineseZodiac.RAT, zodiacs)
        self.assertIn(ChineseZodiac.PIG, zodiacs)
    
    def test_get_zodiac_by_chinese_name(self):
        """测试根据中文名获取星座"""
        self.assertEqual(get_zodiac_by_chinese_name("白羊座"), Zodiac.ARIES)
        self.assertEqual(get_zodiac_by_chinese_name("狮子座"), Zodiac.LEO)
        self.assertEqual(get_zodiac_by_chinese_name("双鱼座"), Zodiac.PISCES)
        self.assertIsNone(get_zodiac_by_chinese_name("不存在的星座"))
    
    def test_get_chinese_zodiac_by_name(self):
        """测试根据中文名获取生肖"""
        self.assertEqual(get_chinese_zodiac_by_name("鼠"), ChineseZodiac.RAT)
        self.assertEqual(get_chinese_zodiac_by_name("龙"), ChineseZodiac.DRAGON)
        self.assertEqual(get_chinese_zodiac_by_name("猪"), ChineseZodiac.PIG)
        self.assertIsNone(get_chinese_zodiac_by_name("猫"))


class TestElementRelationship(unittest.TestCase):
    """测试元素关系"""
    
    def test_same_element(self):
        """测试同元素关系"""
        result = get_element_relationship(Element.FIRE, Element.FIRE)
        self.assertIn("同元素", result)
    
    def test_harmonious_elements(self):
        """测试和谐元素"""
        result = get_element_relationship(Element.FIRE, Element.AIR)
        self.assertIn("和谐", result)
    
    def test_conflicting_elements(self):
        """测试冲突元素"""
        result = get_element_relationship(Element.FIRE, Element.WATER)
        self.assertIn("相冲", result)


class TestTripleHarmony(unittest.TestCase):
    """测试三合功能"""
    
    def test_fire_trine(self):
        """测试火象三合"""
        trine = calculate_triple_harmony(Zodiac.ARIES)
        self.assertIn(Zodiac.ARIES, trine)
        self.assertIn(Zodiac.LEO, trine)
        self.assertIn(Zodiac.SAGITTARIUS, trine)
    
    def test_earth_trine(self):
        """测试土象三合"""
        trine = calculate_triple_harmony(Zodiac.TAURUS)
        self.assertIn(Zodiac.TAURUS, trine)
        self.assertIn(Zodiac.VIRGO, trine)
        self.assertIn(Zodiac.CAPRICORN, trine)
    
    def test_air_trine(self):
        """测试风象三合"""
        trine = calculate_triple_harmony(Zodiac.GEMINI)
        self.assertIn(Zodiac.GEMINI, trine)
        self.assertIn(Zodiac.LIBRA, trine)
        self.assertIn(Zodiac.AQUARIUS, trine)
    
    def test_water_trine(self):
        """测试水象三合"""
        trine = calculate_triple_harmony(Zodiac.CANCER)
        self.assertIn(Zodiac.CANCER, trine)
        self.assertIn(Zodiac.SCORPIO, trine)
        self.assertIn(Zodiac.PISCES, trine)


class TestSixHarm(unittest.TestCase):
    """测试六害功能"""
    
    def test_six_harm_exists(self):
        """测试六害存在"""
        harm = calculate_six_harm(Zodiac.ARIES)
        self.assertEqual(harm, Zodiac.CANCER)
        
        harm = calculate_six_harm(Zodiac.CANCER)
        self.assertEqual(harm, Zodiac.ARIES)
    
    def test_six_harm_all_zodiacs(self):
        """测试所有星座都有六害"""
        for zodiac in Zodiac:
            harm = calculate_six_harm(zodiac)
            self.assertIsInstance(harm, Zodiac)


if __name__ == "__main__":
    unittest.main()