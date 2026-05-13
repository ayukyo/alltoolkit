"""
模糊时钟工具模块测试
"""

import unittest
from datetime import datetime, timedelta
from mod import (
    FuzzyClock,
    fuzzy_time,
    colloquial_time,
    time_range,
    approximate_time,
    relative_time,
)


# 类型别名，兼容各版本 Python
LanguageType = str
PrecisionType = str


class TestFuzzyClock(unittest.TestCase):
    """FuzzyClock 类测试"""
    
    def test_fuzzy_time_chinese(self):
        """测试中文模糊时间"""
        clock = FuzzyClock(language="zh", precision="fuzzy")
        
        # 测试整点
        self.assertEqual(clock.fuzzy_time(hour=3, minute=0), "三点整")
        self.assertEqual(clock.fuzzy_time(hour=12, minute=0), "十二点整")
        
        # 测试一刻
        self.assertEqual(clock.fuzzy_time(hour=3, minute=15), "三点一刻")
        
        # 测试半点
        self.assertEqual(clock.fuzzy_time(hour=3, minute=30), "三点半")
        
        # 测试差一刻
        self.assertEqual(clock.fuzzy_time(hour=3, minute=45), "差一刻四点")
    
    def test_fuzzy_time_english(self):
        """测试英文模糊时间"""
        clock = FuzzyClock(language="en", precision="fuzzy")
        
        # 测试整点
        self.assertEqual(clock.fuzzy_time(hour=3, minute=0), "three o'clock")
        
        # 测试一刻
        self.assertEqual(clock.fuzzy_time(hour=3, minute=15), "quarter past three")
        
        # 测试半点
        self.assertEqual(clock.fuzzy_time(hour=3, minute=30), "half past three")
        
        # 测试差一刻
        self.assertEqual(clock.fuzzy_time(hour=3, minute=45), "quarter to four")
    
    def test_exact_precision(self):
        """测试精确精度"""
        clock = FuzzyClock(language="zh", precision="exact")
        
        self.assertEqual(clock.fuzzy_time(hour=3, minute=5), "三点过五分")
        self.assertEqual(clock.fuzzy_time(hour=3, minute=10), "三点过十分")
        self.assertEqual(clock.fuzzy_time(hour=3, minute=40), "差二十分四点")
        self.assertEqual(clock.fuzzy_time(hour=3, minute=55), "差五分四点")
    
    def test_colloquial_chinese(self):
        """测试中文口语化时间"""
        clock = FuzzyClock(language="zh")
        
        # 测试凌晨
        self.assertIn("凌晨", clock.to_colloquial(hour=3, minute=0))
        
        # 测试早上
        self.assertIn("早上", clock.to_colloquial(hour=8, minute=0))
        
        # 测试上午
        self.assertIn("上午", clock.to_colloquial(hour=10, minute=0))
        
        # 测试中午
        self.assertIn("中午", clock.to_colloquial(hour=12, minute=0))
        
        # 测试下午
        self.assertIn("下午", clock.to_colloquial(hour=15, minute=0))
        
        # 测试晚上
        self.assertIn("晚上", clock.to_colloquial(hour=20, minute=0))
    
    def test_colloquial_english(self):
        """测试英文口语化时间"""
        clock = FuzzyClock(language="en")
        
        # 测试早上的表达
        result = clock.to_colloquial(hour=8, minute=0)
        self.assertIn("morning", result)
        
        # 测试下午的表达
        result = clock.to_colloquial(hour=15, minute=0)
        self.assertIn("afternoon", result)
        
        # 测试晚上的表达
        result = clock.to_colloquial(hour=20, minute=0)
        self.assertIn("evening", result)
    
    def test_time_range(self):
        """测试时间范围描述"""
        clock = FuzzyClock(language="zh")
        
        self.assertEqual(clock.time_range(hour=2, minute=0), "深夜")
        self.assertEqual(clock.time_range(hour=6, minute=0), "清晨")
        self.assertEqual(clock.time_range(hour=9, minute=0), "上午")
        self.assertEqual(clock.time_range(hour=12, minute=0), "中午")
        self.assertEqual(clock.time_range(hour=15, minute=0), "下午")
        self.assertEqual(clock.time_range(hour=18, minute=0), "傍晚")
        self.assertEqual(clock.time_range(hour=20, minute=0), "晚上")
        self.assertEqual(clock.time_range(hour=23, minute=0), "深夜")
    
    def test_approximate_time(self):
        """测试近似时间"""
        clock = FuzzyClock(language="zh", precision="approximate")
        
        # 刚过
        result = clock.to_approximate_time(hour=3, minute=5)
        self.assertIn("刚过", result)
        
        # 左右
        result = clock.to_approximate_time(hour=3, minute=15)
        self.assertIn("左右", result)
        
        # 半左右
        result = clock.to_approximate_time(hour=3, minute=30)
        self.assertIn("半左右", result)
        
        # 快...点了
        result = clock.to_approximate_time(hour=3, minute=50)
        self.assertIn("快", result)
    
    def test_relative_time(self):
        """测试相对时间"""
        clock = FuzzyClock(language="zh")
        
        now = datetime.now()
        
        # 测试刚刚
        past_moment = now - timedelta(seconds=30)
        self.assertEqual(clock.relative_time(past_moment), "刚刚")
        
        # 测试几分钟前
        past_minutes = now - timedelta(minutes=5)
        self.assertEqual(clock.relative_time(past_minutes), "5分钟前")
        
        # 测试几小时前
        past_hours = now - timedelta(hours=3)
        self.assertEqual(clock.relative_time(past_hours), "3小时前")
        
        # 测试几天前
        past_days = now - timedelta(days=2)
        self.assertEqual(clock.relative_time(past_days), "2天前")
        
        # 测试几周前
        past_weeks = now - timedelta(weeks=2)
        self.assertEqual(clock.relative_time(past_weeks), "2周前")
    
    def test_relative_time_english(self):
        """测试英文相对时间"""
        clock = FuzzyClock(language="en")
        
        now = datetime.now()
        
        # 测试 just now
        past_moment = now - timedelta(seconds=30)
        self.assertEqual(clock.relative_time(past_moment), "just now")
        
        # 测试 minutes ago
        past_minutes = now - timedelta(minutes=5)
        self.assertEqual(clock.relative_time(past_minutes), "5 minutes ago")
        
        # 测试 hours ago
        past_hours = now - timedelta(hours=3)
        self.assertEqual(clock.relative_time(past_hours), "3 hours ago")
    
    def test_datetime_input(self):
        """测试 datetime 输入"""
        clock = FuzzyClock(language="zh")
        
        dt = datetime(2024, 1, 1, 15, 30)
        result = clock.fuzzy_time(dt)
        self.assertEqual(result, "三点半")
        
        result = clock.to_colloquial(dt)
        self.assertIn("下午", result)
    
    def test_hour_rollover(self):
        """测试小时进位"""
        clock = FuzzyClock(language="zh", precision="fuzzy")
        
        # 3:45 应该显示 "差一刻四点"
        self.assertEqual(clock.fuzzy_time(hour=3, minute=45), "差一刻四点")
        
        # 11:45 应该显示 "差一刻十二点"
        self.assertEqual(clock.fuzzy_time(hour=11, minute=45), "差一刻十二点")
        
        # 23:45 应该显示 "差一刻十二点" (午夜)
        result = clock.fuzzy_time(hour=23, minute=45)
        self.assertIn("十二", result)


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_fuzzy_time_function(self):
        """测试 fuzzy_time 便捷函数"""
        result = fuzzy_time(hour=3, minute=30, language="zh")
        self.assertEqual(result, "三点半")
        
        result = fuzzy_time(hour=3, minute=30, language="en")
        self.assertEqual(result, "half past three")
    
    def test_colloquial_time_function(self):
        """测试 colloquial_time 便捷函数"""
        result = colloquial_time(hour=15, minute=30, language="zh")
        self.assertIn("下午", result)
        
        result = colloquial_time(hour=15, minute=30, language="en")
        self.assertIn("afternoon", result)
    
    def test_time_range_function(self):
        """测试 time_range 便捷函数"""
        result = time_range(hour=15, minute=0, language="zh")
        self.assertEqual(result, "下午")
        
        result = time_range(hour=15, minute=0, language="en")
        self.assertEqual(result, "afternoon")
    
    def test_approximate_time_function(self):
        """测试 approximate_time 便捷函数"""
        result = approximate_time(hour=3, minute=30, language="zh")
        self.assertIn("半", result)
    
    def test_relative_time_function(self):
        """测试 relative_time 便捷函数"""
        now = datetime.now()
        past = now - timedelta(minutes=30)
        result = relative_time(past, language="zh")
        self.assertEqual(result, "30分钟前")


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_midnight(self):
        """测试午夜时间"""
        clock = FuzzyClock(language="zh")
        
        # 00:00
        result = clock.fuzzy_time(hour=0, minute=0)
        self.assertEqual(result, "十二点整")
        
        # 口语化午夜
        result = clock.to_colloquial(hour=0, minute=0)
        self.assertIn("半夜", result)
    
    def test_noon(self):
        """测试中午时间"""
        clock = FuzzyClock(language="zh")
        
        result = clock.to_colloquial(hour=12, minute=0)
        self.assertIn("中午", result)
    
    def test_minute_59(self):
        """测试分钟为59的情况"""
        clock = FuzzyClock(language="zh", precision="exact")
        
        # 3:55 应该是 "差五分四点"
        result = clock.fuzzy_time(hour=3, minute=55)
        self.assertEqual(result, "差五分四点")
        
        # 口语化测试
        result = clock.to_approximate_time(hour=3, minute=58)
        self.assertIn("快", result)
    
    def test_24_hour_format(self):
        """测试24小时制处理"""
        clock = FuzzyClock(language="zh")
        
        # 下午3点
        result = clock.fuzzy_time(hour=15, minute=0)
        self.assertEqual(result, "三点整")
        
        # 晚上9点
        result = clock.fuzzy_time(hour=21, minute=0)
        self.assertEqual(result, "九点整")


if __name__ == "__main__":
    unittest.main()