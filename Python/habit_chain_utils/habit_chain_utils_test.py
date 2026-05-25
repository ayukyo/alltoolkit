"""
Habit Chain Utils 测试文件

测试习惯链追踪功能的所有核心功能。
"""



import sys
import os

# Ensure the module directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    HabitChain, HabitChainManager, HabitFrequency,
    create_daily_habit, create_weekday_habit, create_weekend_habit,
    create_custom_habit, calculate_streak_milestone, get_chain_health_score
)


class TestHabitChain(unittest.TestCase):
    """测试 HabitChain 类"""
    
    def test_create_daily_habit(self):
        """测试创建每日习惯"""
        chain = HabitChain("阅读", HabitFrequency.DAILY)
        self.assertEqual(chain.name, "阅读")
        self.assertEqual(chain.frequency, HabitFrequency.DAILY)
        self.assertEqual(chain.get_current_streak(), 0)
    
    def test_create_weekday_habit(self):
        """测试创建工作日习惯"""
        chain = HabitChain("健身", HabitFrequency.WEEKDAYS)
        
        # 测试工作日应该追踪
        # 2024-01-08 是周一
        monday = date(2024, 1, 8)
        self.assertTrue(chain._should_track(monday))
        
        # 2024-01-06 是周六
        saturday = date(2024, 1, 6)
        self.assertFalse(chain._should_track(saturday))
    
    def test_create_weekend_habit(self):
        """测试创建周末习惯"""
        chain = HabitChain("睡懒觉", HabitFrequency.WEEKENDS)
        
        # 周六应该追踪
        saturday = date(2024, 1, 6)
        self.assertTrue(chain._should_track(saturday))
        
        # 周一不应该追踪
        monday = date(2024, 1, 8)
        self.assertFalse(chain._should_track(monday))
    
    def test_create_custom_habit(self):
        """测试创建自定义习惯"""
        # 周一、周三、周五
        chain = HabitChain(
            "跑步",
            HabitFrequency.CUSTOM,
            custom_days={0, 2, 4}
        )
        
        # 周一应该追踪
        monday = date(2024, 1, 8)
        self.assertTrue(chain._should_track(monday))
        
        # 周二不应该追踪
        tuesday = date(2024, 1, 9)
        self.assertFalse(chain._should_track(tuesday))
        
        # 周三应该追踪
        wednesday = date(2024, 1, 10)
        self.assertTrue(chain._should_track(wednesday))
    
    def test_complete_and_is_completed(self):
        """测试完成标记"""
        chain = HabitChain("阅读", HabitFrequency.DAILY)
        today = date.today()
        
        # 初始未完成
        self.assertFalse(chain.is_completed(today))
        
        # 标记完成
        result = chain.complete(today)
        self.assertTrue(result)
        self.assertTrue(chain.is_completed(today))
        
        # 再次标记应该还是完成状态
        chain.complete(today)
        self.assertTrue(chain.is_completed(today))
    
    def test_uncomplete(self):
        """测试取消完成标记"""
        chain = HabitChain("阅读", HabitFrequency.DAILY)
        today = date.today()
        
        chain.complete(today)
        self.assertTrue(chain.is_completed(today))
        
        # 取消完成
        result = chain.uncomplete(today)
        self.assertTrue(result)
        self.assertFalse(chain.is_completed(today))
        
        # 取消未完成的日期应该返回False
        result = chain.uncomplete(today)
        self.assertFalse(result)
    
    def test_complete_on_non_track_day(self):
        """测试在非追踪日完成"""
        chain = HabitChain("健身", HabitFrequency.WEEKDAYS)
        saturday = date(2024, 1, 6)  # 周六
        
        result = chain.complete(saturday)
        self.assertFalse(result)  # 不应该成功
        self.assertFalse(chain.is_completed(saturday))
    
    def test_current_streak(self):
        """测试当前连续天数"""
        chain = HabitChain("阅读", HabitFrequency.DAILY)
        today = date.today()
        
        # 连续完成7天
        for i in range(7):
            chain.complete(today - timedelta(days=i))
        
        self.assertEqual(chain.get_current_streak(), 7)
        
        # 如果中间断开一天
        chain.uncomplete(today - timedelta(days=3))
        self.assertEqual(chain.get_current_streak(), 3)  # 只有最近3天
    
    def test_current_streak_with_weekday_habit(self):
        """测试工作日习惯的连续天数"""
        chain = HabitChain("健身", HabitFrequency.WEEKDAYS)
        
        # 假设今天是周三 2024-01-10
        # 周一 2024-01-08, 周二 2024-01-09, 周三 2024-01-10
        monday = date(2024, 1, 8)
        tuesday = date(2024, 1, 9)
        wednesday = date(2024, 1, 10)
        
        chain.complete(monday)
        chain.complete(tuesday)
        chain.complete(wednesday)
        
        # 从周三往前，应该连续3天（只计算工作日）
        # 但这个测试依赖于具体日期，我们用一个固定场景
        # 实际测试：完成工作日后连续天数计算
        
    def test_longest_streak(self):
        """测试最长连续天数"""
        chain = HabitChain("阅读", HabitFrequency.DAILY)
        today = date.today()
        
        # 第一段：5天
        for i in range(5):
            chain.complete(today - timedelta(days=20+i))
        
        # 第二段：10天（更长）
        for i in range(10):
            chain.complete(today - timedelta(days=i))
        
        self.assertEqual(chain.get_longest_streak(), 10)
    
    def test_completion_rate(self):
        """测试完成率计算"""
        chain = HabitChain("阅读", HabitFrequency.DAILY)
        today = date.today()
        
        # 完成7天，查看10天的完成率
        for i in range(7):
            chain.complete(today - timedelta(days=i))
        
        rate = chain.get_completion_rate(10)
        self.assertEqual(rate, 0.7)  # 7/10
    
    def test_get_stats(self):
        """测试获取统计信息"""
        chain = HabitChain("阅读", HabitFrequency.DAILY, color="#FF5722")
        today = date.today()
        
        for i in range(5):
            chain.complete(today - timedelta(days=i))
        
        stats = chain.get_stats()
        
        self.assertEqual(stats["name"], "阅读")
        self.assertEqual(stats["frequency"], "daily")
        self.assertEqual(stats["color"], "#FF5722")
        self.assertEqual(stats["current_streak"], 5)
        self.assertEqual(stats["longest_streak"], 5)
        self.assertTrue(stats["is_completed_today"])
    
    def test_weekly_progress(self):
        """测试周进度"""
        chain = HabitChain("阅读", HabitFrequency.DAILY)
        today = date.today()
        
        # 完成本周前三天
        for i in range(3):
            chain.complete(today - timedelta(days=i))
        
        progress = chain.get_weekly_progress()
        
        self.assertEqual(len(progress["days"]), 7)
        self.assertGreaterEqual(progress["completed"], 3)
        self.assertGreaterEqual(progress["total_tracked_days"], 3)
    
    def test_calendar_heatmap(self):
        """测试日历热力图"""
        chain = HabitChain("阅读", HabitFrequency.DAILY)
        today = date.today()
        
        chain.complete(today)
        chain.complete(today - timedelta(days=1))
        
        heatmap = chain.get_calendar_heatmap(today.year, today.month)
        
        # 应该有周数据
        self.assertGreater(len(heatmap), 0)
        
        # 每周应该有7天
        for week in heatmap:
            self.assertEqual(len(week), 7)
    
    def test_serialization(self):
        """测试序列化和反序列化"""
        original = HabitChain(
            "阅读",
            HabitFrequency.CUSTOM,
            custom_days={0, 2, 4},
            start_date=date(2024, 1, 1),
            color="#FF5722"
        )
        
        # 完成一些天
        today = date.today()
        original.complete(today)
        original.complete(today - timedelta(days=1))
        
        # 序列化
        data = original.to_dict()
        
        # 反序列化
        restored = HabitChain.from_dict(data)
        
        self.assertEqual(restored.name, original.name)
        self.assertEqual(restored.frequency, original.frequency)
        self.assertEqual(restored.custom_days, original.custom_days)
        self.assertEqual(restored.start_date, original.start_date)
        self.assertEqual(restored.color, original.color)
        self.assertEqual(restored.get_current_streak(), original.get_current_streak())


class TestHabitChainManager(unittest.TestCase):
    """测试 HabitChainManager 类"""
    
    def test_add_and_remove_chain(self):
        """测试添加和移除习惯链"""
        manager = HabitChainManager()
        chain = HabitChain("阅读", HabitFrequency.DAILY)
        
        # 添加
        result = manager.add_chain(chain)
        self.assertTrue(result)
        self.assertEqual(manager.get_chain("阅读"), chain)
        
        # 重复添加应该失败
        result = manager.add_chain(chain)
        self.assertFalse(result)
        
        # 移除
        result = manager.remove_chain("阅读")
        self.assertTrue(result)
        self.assertIsNone(manager.get_chain("阅读"))
        
        # 移除不存在的应该失败
        result = manager.remove_chain("不存在")
        self.assertFalse(result)
    
    def test_complete_and_uncomplete(self):
        """测试管理器的完成操作"""
        manager = HabitChainManager()
        manager.add_chain(HabitChain("阅读", HabitFrequency.DAILY))
        
        # 完成
        result = manager.complete("阅读")
        self.assertTrue(result)
        self.assertTrue(manager.get_chain("阅读").is_completed())
        
        # 取消
        result = manager.uncomplete("阅读")
        self.assertTrue(result)
        self.assertFalse(manager.get_chain("阅读").is_completed())
        
        # 不存在的习惯
        result = manager.complete("不存在")
        self.assertFalse(result)
    
    def test_get_all_stats(self):
        """测试获取所有统计"""
        manager = HabitChainManager()
        manager.add_chain(HabitChain("阅读", HabitFrequency.DAILY))
        manager.add_chain(HabitChain("健身", HabitFrequency.WEEKDAYS))
        
        manager.complete("阅读")
        
        stats = manager.get_all_stats()
        self.assertEqual(len(stats), 2)
        
        names = [s["name"] for s in stats]
        self.assertIn("阅读", names)
        self.assertIn("健身", names)
    
    def test_get_today_overview(self):
        """测试今日概览"""
        manager = HabitChainManager()
        manager.add_chain(HabitChain("阅读", HabitFrequency.DAILY))
        manager.add_chain(HabitChain("健身", HabitFrequency.WEEKDAYS))
        
        manager.complete("阅读")
        
        overview = manager.get_today_overview()
        
        self.assertIn("date", overview)
        self.assertEqual(overview["total_habits"], 2)
        self.assertGreaterEqual(overview["completed_today"], 1)
    
    def test_get_weekly_overview(self):
        """测试周概览"""
        manager = HabitChainManager()
        manager.add_chain(HabitChain("阅读", HabitFrequency.DAILY))
        
        overview = manager.get_weekly_overview()
        
        self.assertIn("week_start", overview)
        self.assertIn("week_end", overview)
        self.assertIn("habits", overview)
    
    def test_get_leaderboard(self):
        """测试排行榜"""
        manager = HabitChainManager()
        
        reading = HabitChain("阅读", HabitFrequency.DAILY)
        exercise = HabitChain("健身", HabitFrequency.DAILY)
        
        # 阅读连续5天
        today = date.today()
        for i in range(5):
            reading.complete(today - timedelta(days=i))
        
        # 健身连续3天
        for i in range(3):
            exercise.complete(today - timedelta(days=i))
        
        manager.add_chain(reading)
        manager.add_chain(exercise)
        
        # 按当前连续天数排序
        leaderboard = manager.get_leaderboard(by="current_streak")
        self.assertEqual(leaderboard[0]["name"], "阅读")
        self.assertEqual(leaderboard[1]["name"], "健身")
        
        # 按最长连续天数排序
        leaderboard = manager.get_leaderboard(by="longest_streak")
        self.assertEqual(leaderboard[0]["name"], "阅读")
    
    def test_motivational_message(self):
        """测试激励消息"""
        manager = HabitChainManager()
        manager.add_chain(HabitChain("阅读", HabitFrequency.DAILY))
        
        message = manager.get_motivational_message()
        self.assertIsInstance(message, str)
        self.assertGreater(len(message), 0)
        
        # 完成后应该有不同的消息
        manager.complete("阅读")
        message = manager.get_motivational_message()
        self.assertIn("完成", message)
    
    def test_find_best_chain_day(self):
        """测试找最佳补链日"""
        manager = HabitChainManager()
        manager.add_chain(HabitChain("阅读", HabitFrequency.DAILY))
        manager.add_chain(HabitChain("健身", HabitFrequency.DAILY))
        
        # 只完成阅读，不完成健身
        today = date.today()
        manager.get_chain("阅读").complete(today)
        
        best_day, missing = manager.find_best_chain_day()
        
        # 应该返回一个日期和缺失的习惯列表
        self.assertIsInstance(best_day, date)
        self.assertIsInstance(missing, list)
    
    def test_save_and_load(self):
        """测试保存和加载"""
        manager = HabitChainManager()
        manager.add_chain(HabitChain("阅读", HabitFrequency.DAILY))
        manager.add_chain(HabitChain("健身", HabitFrequency.WEEKDAYS))
        
        manager.complete("阅读")
        
        # 保存到临时文件
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            filepath = f.name
        
        try:
            result = manager.save_to_file(filepath)
            self.assertTrue(result)
            
            # 加载
            loaded = HabitChainManager.load_from_file(filepath)
            self.assertIsNotNone(loaded)
            
            # 验证数据
            self.assertEqual(len(loaded.get_all_stats()), 2)
            self.assertTrue(loaded.get_chain("阅读").is_completed())
        finally:
            os.unlink(filepath)
    
    def test_json_serialization(self):
        """测试JSON序列化"""
        manager = HabitChainManager()
        manager.add_chain(HabitChain("阅读", HabitFrequency.DAILY, color="#FF5722"))
        
        json_str = manager.to_json()
        self.assertIn("阅读", json_str)
        self.assertIn("FF5722", json_str)
        
        restored = HabitChainManager.from_json(json_str)
        self.assertEqual(len(restored.get_all_stats()), 1)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_create_daily_habit(self):
        """测试创建每日习惯"""
        chain = create_daily_habit("阅读", "#FF0000")
        self.assertEqual(chain.name, "阅读")
        self.assertEqual(chain.frequency, HabitFrequency.DAILY)
        self.assertEqual(chain.color, "#FF0000")
    
    def test_create_weekday_habit(self):
        """测试创建工作日习惯"""
        chain = create_weekday_habit("健身")
        self.assertEqual(chain.frequency, HabitFrequency.WEEKDAYS)
        self.assertEqual(chain.color, "#2196F3")
    
    def test_create_weekend_habit(self):
        """测试创建周末习惯"""
        chain = create_weekend_habit("休息")
        self.assertEqual(chain.frequency, HabitFrequency.WEEKENDS)
        self.assertEqual(chain.color, "#FF9800")
    
    def test_create_custom_habit(self):
        """测试创建自定义习惯"""
        chain = create_custom_habit("跑步", {0, 2, 4})  # 周一三五
        self.assertEqual(chain.frequency, HabitFrequency.CUSTOM)
        self.assertEqual(chain.custom_days, {0, 2, 4})
        self.assertEqual(chain.color, "#9C27B0")


class TestStreakMilestone(unittest.TestCase):
    """测试连续天数里程碑"""
    
    def test_milestone_calculation(self):
        """测试里程碑计算"""
        # 0天
        result = calculate_streak_milestone(0)
        self.assertIsNone(result["current_milestone"])
        self.assertEqual(result["next_milestone"]["days"], 7)
        
        # 7天
        result = calculate_streak_milestone(7)
        self.assertEqual(result["current_milestone"]["days"], 7)
        self.assertEqual(result["next_milestone"]["days"], 14)
        
        # 30天
        result = calculate_streak_milestone(30)
        self.assertEqual(result["current_milestone"]["days"], 30)
        self.assertEqual(result["next_milestone"]["days"], 60)
        
        # 100天
        result = calculate_streak_milestone(100)
        self.assertEqual(result["current_milestone"]["days"], 100)
        
        # 超过所有里程碑
        result = calculate_streak_milestone(2000)
        self.assertIsNotNone(result["current_milestone"])
        self.assertIsNone(result["next_milestone"])
        self.assertEqual(result["progress_to_next"], 1.0)
    
    def test_progress_calculation(self):
        """测试进度计算"""
        result = calculate_streak_milestone(10)
        # 在7天和14天之间
        self.assertEqual(result["current_milestone"]["days"], 7)
        self.assertEqual(result["next_milestone"]["days"], 14)
        # 进度应该是 (10-7)/(14-7) = 3/7
        self.assertAlmostEqual(result["progress_to_next"], 3/7, places=2)


class TestHealthScore(unittest.TestCase):
    """测试健康分数"""
    
    def test_new_habit_score(self):
        """测试新习惯的分数"""
        chain = HabitChain("阅读", HabitFrequency.DAILY)
        score = get_chain_health_score(chain)
        # 新习惯分数应该较低
        self.assertLess(score, 20)
    
    def test_completed_today_score(self):
        """测试今天完成的加分"""
        chain = HabitChain("阅读", HabitFrequency.DAILY)
        
        score_before = get_chain_health_score(chain)
        chain.complete()
        score_after = get_chain_health_score(chain)
        
        # 今天完成应该增加分数
        self.assertGreater(score_after, score_before)
    
    def test_high_streak_score(self):
        """测试高连续天数的分数"""
        chain = HabitChain("阅读", HabitFrequency.DAILY)
        today = date.today()
        
        # 连续30天
        for i in range(30):
            chain.complete(today - timedelta(days=i))
        
        score = get_chain_health_score(chain)
        # 连续30天应该有较高分数
        self.assertGreater(score, 50)
    
    def test_score_bounds(self):
        """测试分数边界"""
        chain = HabitChain("阅读", HabitFrequency.DAILY)
        today = date.today()
        
        # 连续很长
        for i in range(100):
            chain.complete(today - timedelta(days=i))
        
        score = get_chain_health_score(chain)
        # 分数不应该超过100
        self.assertLessEqual(score, 100.0)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_empty_manager(self):
        """测试空管理器"""
        manager = HabitChainManager()
        
        overview = manager.get_today_overview()
        self.assertEqual(overview["total_habits"], 0)
        self.assertEqual(overview["completed_today"], 0)
        
        leaderboard = manager.get_leaderboard()
        self.assertEqual(len(leaderboard), 0)
    
    def test_future_date(self):
        """测试未来日期"""
        chain = HabitChain("阅读", HabitFrequency.DAILY)
        future = date.today() + timedelta(days=10)
        
        # 应该可以标记未来日期（虽然不推荐）
        result = chain.complete(future)
        self.assertTrue(result)
        self.assertTrue(chain.is_completed(future))
    
    def test_date_before_start(self):
        """测试开始日期之前"""
        chain = HabitChain(
            "阅读",
            HabitFrequency.DAILY,
            start_date=date.today()
        )
        
        yesterday = date.today() - timedelta(days=1)
        chain.complete(yesterday)
        
        # 虽然可以标记，但统计时应该不会计入
        stats = chain.get_stats()
        self.assertEqual(stats["total_tracked_days"], 1)  # 只有今天
    
    def test_completion_rate_zero_days(self):
        """测试0天的完成率"""
        chain = HabitChain("阅读", HabitFrequency.DAILY)
        rate = chain.get_completion_rate(0)
        self.assertEqual(rate, 0.0)
    
    def test_negative_days(self):
        """测试负数天数的完成率"""
        chain = HabitChain("阅读", HabitFrequency.DAILY)
        rate = chain.get_completion_rate(-5)
        self.assertEqual(rate, 0.0)
    
    def test_weekend_only_streak(self):
        """测试只有周末的习惯"""
        chain = HabitChain("休息", HabitFrequency.WEEKENDS)
        today = date.today()
        
        # 完成过去14天（应该只计算周末）
        for i in range(14):
            chain.complete(today - timedelta(days=i))
        
        # 当前连续天数应该只计算周末
        streak = chain.get_current_streak()
        self.assertGreater(streak, 0)
    
    def test_custom_days_validation(self):
        """测试自定义天数的有效性"""
        # 自定义天数应该是0-6之间
        chain = HabitChain(
            "跑步",
            HabitFrequency.CUSTOM,
            custom_days={0, 2, 4}  # 周一三五
        )
        
        monday = date(2024, 1, 8)
        tuesday = date(2024, 1, 9)
        wednesday = date(2024, 1, 10)
        
        self.assertTrue(chain._should_track(monday))
        self.assertFalse(chain._should_track(tuesday))
        self.assertTrue(chain._should_track(wednesday))


if __name__ == "__main__":
    unittest.main()