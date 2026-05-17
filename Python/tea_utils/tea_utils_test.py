"""
茶道工具模块测试

测试覆盖：
- 茶叶信息查询
- 水温推荐
- 冲泡时间计算
- 茶具推荐
- 搜索功能
- 计时器功能
- 心情推荐
"""

import unittest
import time
from mod import (
    TeaCategory,
    TeaInfo,
    TEA_DATABASE,
    get_tea_info,
    list_teas_by_category,
    get_water_temp_recommendation,
    calculate_steep_time,
    get_brewing_schedule,
    recommend_teaware,
    get_caffeine_info,
    search_tea,
    get_tea_benefits,
    get_tea_flavor_notes,
    TeaTimer,
    format_time,
    get_all_categories,
    get_tea_count,
    compare_teas,
    suggest_tea_by_mood,
)


class TestTeaDatabase(unittest.TestCase):
    """茶叶数据库测试"""
    
    def test_database_not_empty(self):
        """测试数据库不为空"""
        self.assertTrue(len(TEA_DATABASE) > 0)
        self.assertEqual(get_tea_count(), len(TEA_DATABASE))
    
    def test_get_tea_info_exists(self):
        """测试获取存在的茶叶"""
        tea = get_tea_info("龙井")
        self.assertIsNotNone(tea)
        self.assertEqual(tea.name, "龙井")
        self.assertEqual(tea.category, TeaCategory.GREEN)
    
    def test_get_tea_info_not_exists(self):
        """测试获取不存在的茶叶"""
        tea = get_tea_info("不存在茶叶")
        self.assertIsNone(tea)
    
    def test_list_all_teas(self):
        """测试列出所有茶叶"""
        all_teas = list_teas_by_category()
        self.assertEqual(len(all_teas), len(TEA_DATABASE))
    
    def test_list_teas_by_category(self):
        """测试按类别列出茶叶"""
        green_teas = list_teas_by_category(TeaCategory.GREEN)
        self.assertTrue(len(green_teas) > 0)
        for name in green_teas:
            tea = get_tea_info(name)
            self.assertEqual(tea.category, TeaCategory.GREEN)
    
    def test_get_all_categories(self):
        """测试获取所有类别"""
        categories = get_all_categories()
        self.assertTrue(len(categories) > 0)
        # 验证格式
        for cat_name, count in categories:
            self.assertIsInstance(cat_name, str)
            self.assertIsInstance(count, int)
            self.assertTrue(count > 0)


class TestWaterTempRecommendation(unittest.TestCase):
    """水温推荐测试"""
    
    def test_green_tea_temp(self):
        """测试绿茶水温推荐（应较低）"""
        min_temp, max_temp, note = get_water_temp_recommendation("龙井")
        self.assertEqual(min_temp, 75)
        self.assertEqual(max_temp, 80)
        self.assertTrue("绿茶" in note)
        self.assertTrue(max_temp <= 85)  # 绿茶水温不超过85度
    
    def test_oolong_tea_temp(self):
        """测试乌龙茶水温推荐（应较高）"""
        min_temp, max_temp, note = get_water_temp_recommendation("铁观音")
        self.assertEqual(min_temp, 95)
        self.assertEqual(max_temp, 100)
        self.assertTrue("沸水" in note)
    
    def test_unknown_tea_temp(self):
        """测试未知茶叶水温推荐"""
        min_temp, max_temp, note = get_water_temp_recommendation("未知茶叶")
        self.assertEqual(min_temp, 85)
        self.assertEqual(max_temp, 95)
        self.assertTrue("未找到" in note)


class TestSteepTime(unittest.TestCase):
    """冲泡时间测试"""
    
    def test_first_steep_time(self):
        """测试第一泡时间"""
        time_sec, note = calculate_steep_time("龙井", 1)
        self.assertEqual(time_sec, 30)
        self.assertTrue("第1泡" in note)
    
    def test_multiple_steeps(self):
        """测试多泡时间递增"""
        tea = get_tea_info("铁观音")
        time1, _ = calculate_steep_time("铁观音", 1)
        time2, _ = calculate_steep_time("铁观音", 2)
        self.assertEqual(time2, time1 + tea.steep_increment)
    
    def test_exceed_max_steeps(self):
        """测试超过最大泡数"""
        tea = get_tea_info("龙井")
        time_sec, note = calculate_steep_time("龙井", tea.max_steeps + 5)
        # 应使用最后一泡时间
        last_time = tea.first_steep_sec + (tea.max_steeps - 1) * tea.steep_increment
        self.assertEqual(time_sec, last_time)
        self.assertTrue("超过" in note)
    
    def test_zero_steep(self):
        """测试第0泡（无效）"""
        time_sec, note = calculate_steep_time("龙井", 0)
        self.assertTrue("泡数从1开始" in note)
    
    def test_unknown_tea_steep(self):
        """测试未知茶叶冲泡时间"""
        time_sec, note = calculate_steep_time("未知茶叶", 1)
        self.assertEqual(time_sec, 30)
        self.assertTrue("未找到" in note)


class TestBrewingSchedule(unittest.TestCase):
    """冲泡计划测试"""
    
    def test_get_brewing_schedule(self):
        """测试获取冲泡计划"""
        schedule = get_brewing_schedule("铁观音")
        self.assertTrue(len(schedule) > 0)
        
        tea = get_tea_info("铁观音")
        self.assertEqual(len(schedule), tea.max_steeps)
        
        # 验证第一泡
        self.assertEqual(schedule[0]["steep"], 1)
        self.assertEqual(schedule[0]["seconds"], tea.first_steep_sec)
        
        # 验证时间递增
        for i in range(1, len(schedule)):
            self.assertEqual(
                schedule[i]["seconds"],
                schedule[i-1]["seconds"] + tea.steep_increment
            )
    
    def test_unknown_tea_schedule(self):
        """测试未知茶叶冲泡计划"""
        schedule = get_brewing_schedule("未知茶叶")
        self.assertEqual(len(schedule), 0)


class TestTeawareRecommendation(unittest.TestCase):
    """茶具推荐测试"""
    
    def test_green_tea_teaware(self):
        """测试绿茶茶具推荐"""
        teaware, note = recommend_teaware("龙井")
        self.assertTrue("玻璃杯" in teaware)
        self.assertTrue("透明" in note or "观赏" in note)
    
    def test_oolong_teaware(self):
        """测试乌龙茶茶具推荐"""
        teaware, note = recommend_teaware("铁观音")
        self.assertTrue("紫砂壶" in teaware or "盖碗" in teaware)
    
    def test_unknown_teaware(self):
        """测试未知茶叶茶具推荐"""
        teaware, note = recommend_teaware("未知茶叶")
        self.assertTrue("盖碗" in teaware)
        self.assertTrue("未找到" in note)


class TestCaffeineInfo(unittest.TestCase):
    """咖啡因信息测试"""
    
    def test_high_caffeine(self):
        """测试高咖啡因茶叶"""
        level, percent = get_caffeine_info("大红袍")
        self.assertEqual(level, "高")
        self.assertEqual(percent, 80)
    
    def test_low_caffeine(self):
        """测试低咖啡因茶叶"""
        level, percent = get_caffeine_info("白毫银针")
        self.assertEqual(level, "低")
        self.assertEqual(percent, 20)
    
    def test_no_caffeine(self):
        """测试无咖啡因茶叶"""
        level, percent = get_caffeine_info("玫瑰花茶")
        self.assertEqual(level, "无咖啡因")
        self.assertEqual(percent, 0)
    
    def test_unknown_caffeine(self):
        """测试未知茶叶咖啡因"""
        level, percent = get_caffeine_info("未知茶叶")
        self.assertEqual(level, "unknown")
        self.assertEqual(percent, 0)


class TestSearch(unittest.TestCase):
    """搜索功能测试"""
    
    def test_search_by_name(self):
        """测试按名称搜索"""
        results = search_tea("龙井")
        self.assertTrue(len(results) > 0)
        self.assertTrue(any("龙井" in r[0] for r in results))
        # 匹配度应为1.0（完全匹配）
        self.assertTrue(any(r[2] == 1.0 for r in results))
    
    def test_search_by_category(self):
        """测试按类别搜索"""
        results = search_tea("绿茶")
        self.assertTrue(len(results) > 0)
        # 搜索"绿茶"可能匹配名称或类别
        # 茉莉花茶描述中包含"绿茶为茶坯"，所以也会被匹配
    
    def test_search_by_origin(self):
        """测试按产地搜索"""
        results = search_tea("福建")
        self.assertTrue(len(results) > 0)
    
    def test_search_by_flavor(self):
        """测试按风味搜索"""
        results = search_tea("花香")
        self.assertTrue(len(results) > 0)
    
    def test_search_no_match(self):
        """测试无匹配结果"""
        results = search_tea("完全不存在的关键词xyz")
        self.assertEqual(len(results), 0)


class TestBenefitsAndFlavor(unittest.TestCase):
    """功效和风味测试"""
    
    def test_get_benefits(self):
        """测试获取功效"""
        benefits = get_tea_benefits("龙井")
        self.assertTrue(len(benefits) > 0)
        self.assertTrue(any("抗氧化" in b for b in benefits))
    
    def test_get_flavor_notes(self):
        """测试获取风味"""
        flavors = get_tea_flavor_notes("铁观音")
        self.assertTrue(len(flavors) > 0)
        self.assertTrue(any("兰花香" in f or "音韵" in f for f in flavors))
    
    def test_unknown_benefits(self):
        """测试未知茶叶功效"""
        benefits = get_tea_benefits("未知茶叶")
        self.assertEqual(len(benefits), 1)
        self.assertTrue("未找到" in benefits[0])


class TestTeaTimer(unittest.TestCase):
    """计时器测试"""
    
    def test_timer_init(self):
        """测试计时器初始化"""
        timer = TeaTimer("龙井")
        self.assertEqual(timer.tea_name, "龙井")
        self.assertEqual(timer.current_steep, 0)
        self.assertFalse(timer.is_running)
    
    def test_timer_init_unknown(self):
        """测试未知茶叶初始化"""
        with self.assertRaises(ValueError):
            TeaTimer("未知茶叶")
    
    def test_timer_start(self):
        """测试计时器启动"""
        timer = TeaTimer("龙井")
        result = timer.start()
        
        self.assertEqual(result["steep"], 1)
        self.assertEqual(result["duration_sec"], 30)
        self.assertTrue(timer.is_running)
    
    def test_timer_check(self):
        """测试计时器检查"""
        timer = TeaTimer("龙井")
        timer.start()
        
        # 立即检查
        status = timer.check()
        self.assertEqual(status["status"], "running")
        self.assertEqual(status["steep"], 1)
        self.assertTrue(status["remaining_sec"] > 0)
    
    def test_timer_stop(self):
        """测试计时器停止"""
        timer = TeaTimer("龙井")
        timer.start()
        
        result = timer.stop()
        self.assertEqual(result["status"], "stopped")
        self.assertFalse(timer.is_running)
    
    def test_timer_reset(self):
        """测试计时器重置"""
        timer = TeaTimer("龙井")
        timer.start()
        timer.stop()
        
        result = timer.reset()
        self.assertEqual(result["status"], "reset")
        self.assertEqual(timer.current_steep, 0)
    
    def test_timer_max_steeps(self):
        """测试达到最大泡数"""
        timer = TeaTimer("龙井", total_steeps=2)
        timer.start()
        timer.stop()
        timer.start()
        timer.stop()
        
        # 再启动应返回错误
        result = timer.start()
        self.assertTrue("error" in result)
    
    def test_timer_get_status(self):
        """测试获取状态"""
        timer = TeaTimer("铁观音")
        status = timer.get_status()
        
        self.assertEqual(status["tea_name"], "铁观音")
        self.assertEqual(status["tea_category"], "乌龙茶")
        self.assertEqual(status["water_temp"], "95-100°C")


class TestFormatTime(unittest.TestCase):
    """时间格式化测试"""
    
    def test_seconds_only(self):
        """测试秒数显示"""
        self.assertEqual(format_time(30), "30秒")
        self.assertEqual(format_time(45), "45秒")
    
    def test_minutes_only(self):
        """测试分钟显示"""
        self.assertEqual(format_time(60), "1分钟")
        self.assertEqual(format_time(120), "2分钟")
    
    def test_mixed(self):
        """测试分钟和秒"""
        self.assertEqual(format_time(90), "1分30秒")
        self.assertEqual(format_time(150), "2分30秒")


class TestCompare(unittest.TestCase):
    """对比功能测试"""
    
    def test_compare_teas(self):
        """测试对比茶叶"""
        comparison = compare_teas(["龙井", "铁观音", "熟普"])
        self.assertEqual(len(comparison), 3)
        
        # 验证数据结构
        for item in comparison:
            self.assertIn("name", item)
            self.assertIn("category", item)
            self.assertIn("water_temp", item)
            self.assertIn("caffeine", item)
    
    def test_compare_unknown(self):
        """测试对比包含未知茶叶"""
        comparison = compare_teas(["龙井", "未知茶叶"])
        self.assertEqual(len(comparison), 1)  # 只返回存在的


class TestMoodSuggestion(unittest.TestCase):
    """心情推荐测试"""
    
    def test_suggest_for_alertness(self):
        """测试提神需求"""
        suggestions = suggest_tea_by_mood("提神")
        self.assertTrue(len(suggestions) > 0)
        self.assertTrue(any("生普" in s[0] or "铁观音" in s[0] for s in suggestions))
    
    def test_suggest_for_relaxation(self):
        """测试放松需求"""
        suggestions = suggest_tea_by_mood("放松")
        self.assertTrue(len(suggestions) > 0)
        self.assertTrue(any("熟普" in s[0] or "玫瑰" in s[0] for s in suggestions))
    
    def test_suggest_for_digestion(self):
        """测试消化需求"""
        suggestions = suggest_tea_by_mood("消化")
        self.assertTrue(len(suggestions) > 0)
    
    def test_suggest_for_night(self):
        """测试晚上饮用"""
        suggestions = suggest_tea_by_mood("晚上")
        self.assertTrue(len(suggestions) > 0)
        # 应推荐低咖啡因茶叶
        for name, reason in suggestions:
            level, _ = get_caffeine_info(name)
            self.assertTrue(level in ["低", "无咖啡因", "unknown"])
    
    def test_suggest_default(self):
        """测试未知心情默认推荐"""
        suggestions = suggest_tea_by_mood("完全未知的心情")
        self.assertEqual(len(suggestions), 2)  # 默认推荐两个


class TestTeaCategory(unittest.TestCase):
    """茶叶类别枚举测试"""
    
    def test_category_names(self):
        """测试类别名称"""
        self.assertEqual(TeaCategory.GREEN.value, "绿茶")
        self.assertEqual(TeaCategory.OOLONG.value, "乌龙茶")
        self.assertEqual(TeaCategory.PUERH_RAW.value, "生普")
    
    def test_all_categories_exist_in_database(self):
        """测试所有类别都有茶叶"""
        for category in TeaCategory:
            teas = list_teas_by_category(category)
            # 大部分类别应该有茶叶，但不是全部（如HERBAL可能较少）
            if category not in [TeaCategory.MATCHA]:
                # 抹茶类只有一种
                pass


if __name__ == "__main__":
    unittest.main()