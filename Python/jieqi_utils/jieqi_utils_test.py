"""
节气工具模块测试 (Jieqi Utils Test)

测试节气计算、查询和相关功能。
"""

import unittest
from datetime import date
from mod import (
    get_jieqi_date,
    get_year_jieqi_list,
    get_current_jieqi,
    get_next_jieqi,
    get_days_to_next_jieqi,
    get_jieqi_health_advice,
    get_jieqi_traditions,
    get_jieqi_info,
    get_season_jieqi,
    is_jieqi_day,
    get_jieqi_by_month,
    format_jieqi_report,
    get_jieqi_name_list,
    get_current_season,
    get_quarter_jieqi,
    search_jieqi,
    JIEQI_NAMES,
    JieqiInfo,
)


class TestJieqiDateCalculation(unittest.TestCase):
    """测试节气日期计算"""
    
    def test_get_jieqi_date_lichun(self):
        """测试立春日期计算"""
        lichun_date = get_jieqi_date(2024, "立春")
        self.assertIsNotNone(lichun_date)
        self.assertEqual(lichun_date.year, 2024)
        self.assertEqual(lichun_date.month, 2)
        # 立春通常在2月3-5日
        self.assertIn(lichun_date.day, [3, 4, 5])
    
    def test_get_jieqi_date_dongzhi(self):
        """测试冬至日期计算"""
        dongzhi_date = get_jieqi_date(2024, "冬至")
        self.assertIsNotNone(dongzhi_date)
        self.assertEqual(dongzhi_date.year, 2024)
        self.assertEqual(dongzhi_date.month, 12)
        # 冬至通常在12月20-23日
        self.assertIn(dongzhi_date.day, [20, 21, 22, 23])
    
    def test_get_jieqi_date_invalid(self):
        """测试无效节气名称"""
        result = get_jieqi_date(2024, "无效节气")
        self.assertIsNone(result)
    
    def test_get_year_jieqi_list_length(self):
        """测试节气列表长度"""
        jieqi_list = get_year_jieqi_list(2024)
        self.assertEqual(len(jieqi_list), 24)
    
    def test_get_year_jieqi_list_order(self):
        """测试节气顺序"""
        jieqi_list = get_year_jieqi_list(2024)
        names = [j.name for j in jieqi_list]
        self.assertEqual(names, JIEQI_NAMES)


class TestJieqiInfo(unittest.TestCase):
    """测试节气信息"""
    
    def test_jieqi_info_structure(self):
        """测试节气信息结构"""
        jieqi_list = get_year_jieqi_list(2024)
        lichun = jieqi_list[2]  # 立春
        
        self.assertEqual(lichun.name, "立春")
        self.assertEqual(lichun.season, "春")
        self.assertEqual(lichun.month, 1)
        self.assertTrue(lichun.is_jieqi)  # 立春是节气（每月第一个）
        self.assertEqual(lichun.description, "春季开始，万物复苏")
    
    def test_jieqi_info_yushui(self):
        """测试雨水信息"""
        jieqi_list = get_year_jieqi_list(2024)
        yushui = jieqi_list[3]  # 雨水
        
        self.assertEqual(yushui.name, "雨水")
        self.assertEqual(yushui.season, "春")
        self.assertFalse(yushui.is_jieqi)  # 雨水是中气（每月第二个）
    
    def test_all_jieqi_have_season(self):
        """测试所有节气都有季节"""
        jieqi_list = get_year_jieqi_list(2024)
        seasons = set(["春", "夏", "秋", "冬"])
        for j in jieqi_list:
            self.assertIn(j.season, seasons)


class TestCurrentJieqi(unittest.TestCase):
    """测试当前节气查询"""
    
    def test_get_current_jieqi_lichun_period(self):
        """测试立春期间的当前节气"""
        # 假设立春是2月4日，测试2月10日应该返回立春
        current = get_current_jieqi(date(2024, 2, 10))
        self.assertIsNotNone(current)
        self.assertEqual(current.name, "立春")
    
    def test_get_current_jieqi_yushui_period(self):
        """测试雨水期间的当前节气"""
        # 雨水通常在2月18-20日
        current = get_current_jieqi(date(2024, 2, 25))
        self.assertIsNotNone(current)
        self.assertEqual(current.name, "雨水")
    
    def test_get_current_jieqi_dongzhi_period(self):
        """测试冬至期间的当前节气"""
        # 冬至通常在12月21-23日，测试12月25日
        current = get_current_jieqi(date(2024, 12, 25))
        self.assertIsNotNone(current)
        self.assertEqual(current.name, "冬至")


class TestNextJieqi(unittest.TestCase):
    """测试下一个节气"""
    
    def test_get_next_jieqi_before_lichun(self):
        """测试立春前的下一个节气"""
        next_jieqi = get_next_jieqi(date(2024, 2, 1))
        self.assertIsNotNone(next_jieqi)
        self.assertEqual(next_jieqi.name, "立春")
    
    def test_get_next_jieqi_after_lichun(self):
        """测试立春后的下一个节气"""
        next_jieqi = get_next_jieqi(date(2024, 2, 5))
        self.assertIsNotNone(next_jieqi)
        self.assertEqual(next_jieqi.name, "雨水")
    
    def test_get_next_jieqi_year_end(self):
        """测试年末的下一个节气"""
        next_jieqi = get_next_jieqi(date(2024, 12, 25))
        self.assertIsNotNone(next_jieqi)
        self.assertEqual(next_jieqi.name, "小寒")
        self.assertEqual(next_jieqi.date.year, 2025)


class TestDaysToNextJieqi(unittest.TestCase):
    """测试距离下一个节气的天数"""
    
    def test_days_to_next_jieqi(self):
        """测试天数计算"""
        # 假设立春是2月4日，从2月1日开始
        days = get_days_to_next_jieqi(date(2024, 2, 1))
        self.assertGreater(days, 0)
        self.assertLess(days, 5)
    
    def test_days_to_next_jieqi_same_day(self):
        """测试节气日当天"""
        lichun_date = get_jieqi_date(2024, "立春")
        days = get_days_to_next_jieqi(lichun_date)
        # 当天应该返回0或很小的值
        self.assertGreaterEqual(days, 0)


class TestJieqiAdvice(unittest.TestCase):
    """测试节气养生建议和习俗"""
    
    def test_get_health_advice_lichun(self):
        """测试立春养生建议"""
        advice = get_jieqi_health_advice("立春")
        self.assertIsNotNone(advice)
        self.assertEqual(len(advice), 3)
        self.assertIn("养肝护肝，调畅情志", advice)
    
    def test_get_health_advice_dongzhi(self):
        """测试冬至养生建议"""
        advice = get_jieqi_health_advice("冬至")
        self.assertIsNotNone(advice)
        self.assertEqual(len(advice), 3)
    
    def test_get_health_advice_invalid(self):
        """测试无效节气名称"""
        advice = get_jieqi_health_advice("无效节气")
        self.assertIsNone(advice)
    
    def test_get_traditions_qingming(self):
        """测试清明习俗"""
        traditions = get_jieqi_traditions("清明")
        self.assertIsNotNone(traditions)
        self.assertIn("扫墓祭祖", traditions)
    
    def test_get_traditions_dongzhi(self):
        """测试冬至习俗"""
        traditions = get_jieqi_traditions("冬至")
        self.assertIsNotNone(traditions)
        self.assertIn("吃饺子/汤圆", traditions)


class TestJieqiInfoQuery(unittest.TestCase):
    """测试节气详细信息查询"""
    
    def test_get_jieqi_info_lichun(self):
        """测试立春详细信息"""
        info = get_jieqi_info("立春")
        self.assertIsNotNone(info)
        self.assertEqual(info["name"], "立春")
        self.assertEqual(info["season"], "春")
        self.assertEqual(info["month"], 1)
        self.assertTrue(info["is_jieqi"])
    
    def test_get_jieqi_info_complete(self):
        """测试节气信息完整性"""
        for name in JIEQI_NAMES:
            info = get_jieqi_info(name)
            self.assertIsNotNone(info)
            self.assertIn("name", info)
            self.assertIn("season", info)
            self.assertIn("month", info)
            self.assertIn("description", info)
            self.assertIn("health_advice", info)
            self.assertIn("traditions", info)


class TestSeasonJieqi(unittest.TestCase):
    """测试季节节气查询"""
    
    def test_get_season_jieqi_spring(self):
        """测试春季节气"""
        spring_jieqi = get_season_jieqi("春")
        self.assertEqual(len(spring_jieqi), 6)
        self.assertIn("立春", spring_jieqi)
        self.assertIn("春分", spring_jieqi)
    
    def test_get_season_jieqi_summer(self):
        """测试夏季节气"""
        summer_jieqi = get_season_jieqi("夏")
        self.assertEqual(len(summer_jieqi), 6)
        self.assertIn("立夏", summer_jieqi)
        self.assertIn("夏至", summer_jieqi)
    
    def test_get_season_jieqi_autumn(self):
        """测试秋季节气"""
        autumn_jieqi = get_season_jieqi("秋")
        self.assertEqual(len(autumn_jieqi), 6)
        self.assertIn("立秋", autumn_jieqi)
        self.assertIn("秋分", autumn_jieqi)
    
    def test_get_season_jieqi_winter(self):
        """测试冬季节气"""
        winter_jieqi = get_season_jieqi("冬")
        self.assertEqual(len(winter_jieqi), 6)
        self.assertIn("立冬", winter_jieqi)
        self.assertIn("冬至", winter_jieqi)
    
    def test_get_season_jieqi_invalid(self):
        """测试无效季节"""
        result = get_season_jieqi("无效季节")
        self.assertEqual(len(result), 0)


class TestJieqiDay(unittest.TestCase):
    """测试节气日判断"""
    
    def test_is_jieqi_day_true(self):
        """测试节气日"""
        lichun_date = get_jieqi_date(2024, "立春")
        self.assertTrue(is_jieqi_day(lichun_date))
    
    def test_is_jieqi_day_false(self):
        """测试非节气日"""
        self.assertFalse(is_jieqi_day(date(2024, 2, 10)))
    
    def test_is_jieqi_day_multiple(self):
        """测试多个节气日"""
        for name in ["立春", "夏至", "冬至"]:
            jieqi_date = get_jieqi_date(2024, name)
            if jieqi_date:
                self.assertTrue(is_jieqi_day(jieqi_date))


class TestJieqiByMonth(unittest.TestCase):
    """测试月份节气查询"""
    
    def test_get_jieqi_by_month_february(self):
        """测试2月节气"""
        feb_jieqi = get_jieqi_by_month(2)
        self.assertEqual(len(feb_jieqi), 2)
        self.assertIn("立春", feb_jieqi)
        self.assertIn("雨水", feb_jieqi)
    
    def test_get_jieqi_by_month_june(self):
        """测试6月节气"""
        jun_jieqi = get_jieqi_by_month(6)
        self.assertEqual(len(jun_jieqi), 2)
        self.assertIn("芒种", jun_jieqi)
        self.assertIn("夏至", jun_jieqi)
    
    def test_get_jieqi_by_month_all(self):
        """测试所有月份都有节气"""
        for month in range(1, 13):
            jieqi = get_jieqi_by_month(month)
            self.assertEqual(len(jieqi), 2)


class TestJieqiReport(unittest.TestCase):
    """测试节气报告格式化"""
    
    def test_format_jieqi_report(self):
        """测试节气报告格式化"""
        jieqi_list = get_year_jieqi_list(2024)
        lichun = jieqi_list[2]
        
        report = format_jieqi_report(lichun)
        
        self.assertIn("【立春】", report)
        self.assertIn("春季开始，万物复苏", report)
        self.assertIn("养生建议", report)
        self.assertIn("传统习俗", report)


class TestCurrentSeason(unittest.TestCase):
    """测试当前季节"""
    
    def test_get_current_season_spring(self):
        """测试春季"""
        season = get_current_season(date(2024, 3, 15))
        self.assertEqual(season, "春")
    
    def test_get_current_season_summer(self):
        """测试夏季"""
        season = get_current_season(date(2024, 7, 15))
        self.assertEqual(season, "夏")
    
    def test_get_current_season_autumn(self):
        """测试秋季"""
        season = get_current_season(date(2024, 10, 15))
        self.assertEqual(season, "秋")
    
    def test_get_current_season_winter(self):
        """测试冬季"""
        season = get_current_season(date(2024, 12, 25))
        self.assertEqual(season, "冬")


class TestQuarterJieqi(unittest.TestCase):
    """测试四时八节"""
    
    def test_get_quarter_jieqi(self):
        """测试四时八节"""
        quarter = get_quarter_jieqi()
        self.assertEqual(len(quarter), 8)
        self.assertIn("立春", quarter)
        self.assertIn("春分", quarter)
        self.assertIn("立夏", quarter)
        self.assertIn("夏至", quarter)
        self.assertIn("立秋", quarter)
        self.assertIn("秋分", quarter)
        self.assertIn("立冬", quarter)
        self.assertIn("冬至", quarter)


class TestSearchJieqi(unittest.TestCase):
    """测试节气搜索"""
    
    def test_search_jieqi_by_character(self):
        """测试按汉字搜索"""
        result = search_jieqi("春")
        self.assertEqual(len(result), 2)
        self.assertIn("立春", result)
        self.assertIn("春分", result)
    
    def test_search_jieqi_by_part(self):
        """测试按部分名称搜索"""
        result = search_jieqi("立")
        self.assertEqual(len(result), 4)
        self.assertIn("立春", result)
        self.assertIn("立夏", result)
        self.assertIn("立秋", result)
        self.assertIn("立冬", result)
    
    def test_search_jieqi_full_name(self):
        """测试按完整名称搜索"""
        result = search_jieqi("立春")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "立春")
    
    def test_search_jieqi_no_match(self):
        """测试无匹配"""
        result = search_jieqi("不存在")
        self.assertEqual(len(result), 0)


class TestJieqiNameList(unittest.TestCase):
    """测试节气名称列表"""
    
    def test_get_jieqi_name_list(self):
        """测试节气名称列表"""
        names = get_jieqi_name_list()
        self.assertEqual(len(names), 24)
        self.assertEqual(names[0], "小寒")
        self.assertEqual(names[23], "冬至")
    
    def test_jieqi_names_order(self):
        """测试节气名称顺序"""
        names = get_jieqi_name_list()
        # 检查季节顺序
        spring_start = names.index("立春")
        summer_start = names.index("立夏")
        autumn_start = names.index("立秋")
        winter_start = names.index("立冬")
        
        self.assertEqual(spring_start, 2)
        self.assertEqual(summer_start, 8)
        self.assertEqual(autumn_start, 14)
        self.assertEqual(winter_start, 20)


class TestMultipleYears(unittest.TestCase):
    """测试多年节气计算"""
    
    def test_different_years(self):
        """测试不同年份"""
        for year in [2020, 2021, 2022, 2023, 2024, 2025]:
            lichun = get_jieqi_date(year, "立春")
            self.assertIsNotNone(lichun)
            self.assertEqual(lichun.month, 2)
            self.assertIn(lichun.day, [3, 4, 5, 6])
            
            dongzhi = get_jieqi_date(year, "冬至")
            self.assertIsNotNone(dongzhi)
            self.assertEqual(dongzhi.month, 12)
            self.assertIn(dongzhi.day, [20, 21, 22, 23])


if __name__ == "__main__":
    unittest.main(verbosity=2)