"""
Habit Tracker Utilities - 测试文件

测试习惯追踪工具的所有功能。
"""

import unittest
from datetime import date, timedelta
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from habit_tracker_utils.mod import (
    HabitTracker,
    Habit,
    HabitCompletion,
    HabitStats,
    HabitUtils,
    FrequencyType,
    DayOfWeek,
    create_habit,
    calculate_streak,
    completion_rate,
)


class TestHabitCompletion(unittest.TestCase):
    """测试 HabitCompletion 类"""
    
    def test_create_completion(self):
        """测试创建完成记录"""
        completion = HabitCompletion(
            date=date.today(),
            completed=True,
            value=30,
            note="测试",
            mood=4,
        )
        
        self.assertEqual(completion.date, date.today())
        self.assertTrue(completion.completed)
        self.assertEqual(completion.value, 30)
        self.assertEqual(completion.note, "测试")
        self.assertEqual(completion.mood, 4)
    
    def test_to_dict(self):
        """测试转换为字典"""
        completion = HabitCompletion(
            date=date(2024, 1, 15),
            completed=True,
            value=60,
            note="测试",
        )
        
        data = completion.to_dict()
        
        self.assertEqual(data['date'], '2024-01-15')
        self.assertTrue(data['completed'])
        self.assertEqual(data['value'], 60)
        self.assertEqual(data['note'], "测试")
    
    def test_from_dict(self):
        """测试从字典创建"""
        data = {
            'date': '2024-01-15',
            'completed': True,
            'value': 30,
            'note': '测试',
            'mood': 5,
        }
        
        completion = HabitCompletion.from_dict(data)
        
        self.assertEqual(completion.date, date(2024, 1, 15))
        self.assertTrue(completion.completed)
        self.assertEqual(completion.value, 30)
        self.assertEqual(completion.mood, 5)


class TestHabit(unittest.TestCase):
    """测试 Habit 类"""
    
    def test_create_habit(self):
        """测试创建习惯"""
        habit = Habit(name="测试习惯")
        
        self.assertEqual(habit.name, "测试习惯")
        self.assertEqual(habit.frequency, FrequencyType.DAILY)
        self.assertEqual(habit.color, "#4CAF50")
    
    def test_complete(self):
        """测试完成习惯"""
        habit = Habit(name="测试")
        target = date.today() - timedelta(days=1)
        
        completion = habit.complete(target_date=target, value=30, mood=4)
        
        self.assertTrue(habit.is_completed(target))
        self.assertTrue(completion.completed)
        self.assertEqual(completion.value, 30)
    
    def test_skip(self):
        """测试跳过习惯"""
        habit = Habit(name="测试")
        target = date.today() - timedelta(days=1)
        
        completion = habit.skip(target_date=target, note="生病")
        
        self.assertFalse(habit.is_completed(target))
        self.assertFalse(completion.completed)
        self.assertEqual(completion.note, "生病")
    
    def test_is_due_daily(self):
        """测试每日习惯的执行日期判断"""
        habit = Habit(name="每日测试", frequency=FrequencyType.DAILY)
        
        # 每天都需要执行
        self.assertTrue(habit.is_due(date.today()))
        self.assertTrue(habit.is_due(date.today() + timedelta(days=1)))
    
    def test_is_due_weekly(self):
        """测试每周习惯的执行日期判断"""
        habit = Habit(
            name="每周测试",
            frequency=FrequencyType.WEEKLY,
            target_days=[0, 2, 4],  # 周一三五
        )
        
        # 创建特定日期测试
        monday = date(2024, 1, 1)  # 周一
        tuesday = date(2024, 1, 2)  # 周二
        wednesday = date(2024, 1, 3)  # 周三
        
        self.assertTrue(habit.is_due(monday))
        self.assertFalse(habit.is_due(tuesday))
        self.assertTrue(habit.is_due(wednesday))
    
    def test_to_dict_and_from_dict(self):
        """测试序列化和反序列化"""
        habit = Habit(
            name="测试",
            description="测试描述",
            frequency=FrequencyType.WEEKLY,
            target_days=[0, 2, 4],
            target_value=60,
            color="#FF0000",
            icon="🏃",
            tags=["运动", "健康"],
            priority=3,
        )
        
        habit.complete(target_date=date.today(), value=30)
        
        # 序列化
        data = habit.to_dict()
        self.assertEqual(data['name'], "测试")
        self.assertEqual(data['frequency'], "weekly")
        self.assertEqual(data['target_days'], [0, 2, 4])
        
        # 反序列化
        restored = Habit.from_dict(data)
        self.assertEqual(restored.name, "测试")
        self.assertEqual(restored.frequency, FrequencyType.WEEKLY)
        self.assertEqual(restored.target_days, [0, 2, 4])
        self.assertEqual(len(restored.completions), 1)


class TestHabitTracker(unittest.TestCase):
    """测试 HabitTracker 类"""
    
    def setUp(self):
        """每个测试前的设置"""
        self.tracker = HabitTracker()
    
    def test_add_habit(self):
        """测试添加习惯"""
        habit = self.tracker.add_habit("跑步", "每天跑步")
        
        self.assertIn("跑步", self.tracker.habits)
        self.assertEqual(habit.name, "跑步")
        self.assertEqual(habit.description, "每天跑步")
    
    def test_remove_habit(self):
        """测试删除习惯"""
        self.tracker.add_habit("跑步")
        
        result = self.tracker.remove_habit("跑步")
        
        self.assertTrue(result)
        self.assertNotIn("跑步", self.tracker.habits)
    
    def test_complete_habit(self):
        """测试完成习惯"""
        self.tracker.add_habit("跑步")
        
        completion = self.tracker.complete_habit("跑步", value=30, mood=4)
        
        self.assertIsNotNone(completion)
        self.assertTrue(completion.completed)
    
    def test_skip_habit(self):
        """测试跳过习惯"""
        self.tracker.add_habit("跑步")
        
        completion = self.tracker.skip_habit("跑步", note="生病")
        
        self.assertIsNotNone(completion)
        self.assertFalse(completion.completed)
        self.assertEqual(completion.note, "生病")
    
    def test_calculate_streak(self):
        """测试计算连续天数"""
        habit = self.tracker.add_habit("跑步")
        
        # 连续完成5天
        today = date.today()
        for i in range(5):
            d = today - timedelta(days=i)
            habit.complete(target_date=d)
        
        current, longest = self.tracker.calculate_streak(habit)
        
        self.assertEqual(current, 5)
        self.assertEqual(longest, 5)
    
    def test_calculate_streak_broken(self):
        """测试中断的连续天数"""
        habit = self.tracker.add_habit("跑步")
        
        today = date.today()
        
        # 今天完成
        habit.complete(target_date=today)
        
        # 昨天完成
        habit.complete(target_date=today - timedelta(days=1))
        
        # 前天未完成（中断）
        
        # 大前天完成
        habit.complete(target_date=today - timedelta(days=3))
        
        current, longest = self.tracker.calculate_streak(habit)
        
        self.assertEqual(current, 2)  # 当前连续2天
        self.assertEqual(longest, 2)  # 最长也是2天
    
    def test_get_stats(self):
        """测试获取统计数据"""
        self.tracker.add_habit("跑步")
        
        today = date.today()
        for i in range(7):
            d = today - timedelta(days=i)
            self.tracker.complete_habit("跑步", target_date=d, value=30, mood=4)
        
        stats = self.tracker.get_stats("跑步")
        
        self.assertIsNotNone(stats)
        self.assertEqual(stats.completed_days, 7)
        self.assertEqual(stats.current_streak, 7)
        self.assertEqual(stats.completion_rate, 1.0)
        self.assertEqual(stats.total_value, 210)  # 7 * 30
        self.assertEqual(stats.average_value, 30)
    
    def test_get_stats_with_missed(self):
        """测试包含未完成的统计数据"""
        # 创建习惯，并设置创建日期为7天前
        habit = self.tracker.add_habit("跑步")
        habit.created_at = date.today() - timedelta(days=7)
        
        today = date.today()
        
        # 完成5天（从今天往前5天）
        for i in range(5):
            d = today - timedelta(days=i)
            self.tracker.complete_habit("跑步", target_date=d)
        
        # 不完成第6天和第7天（由created_at决定）
        
        stats = self.tracker.get_stats("跑步")
        
        # completed_days应该是5（我们完成了5天）
        self.assertEqual(stats.completed_days, 5)
        # total_days应该大于5（因为created_at是7天前）
        self.assertGreater(stats.total_days, 5)
    
    def test_get_weekly_report(self):
        """测试周报告"""
        self.tracker.add_habit("跑步")
        
        today = date.today()
        for i in range(7):
            d = today - timedelta(days=i)
            self.tracker.complete_habit("跑步", target_date=d)
        
        report = self.tracker.get_weekly_report("跑步")
        
        self.assertIn('habit_name', report)
        self.assertEqual(report['habit_name'], "跑步")
        self.assertIn('daily_status', report)
        self.assertIn('stats', report)
    
    def test_get_monthly_calendar(self):
        """测试月度日历"""
        self.tracker.add_habit("跑步")
        
        # 完成本月前10天
        today = date.today()
        for i in range(10):
            d = today - timedelta(days=i)
            self.tracker.complete_habit("跑步", target_date=d)
        
        calendar = self.tracker.get_monthly_calendar("跑步", today.year, today.month)
        
        self.assertIn('calendar', calendar)
        self.assertIn('stats', calendar)
        self.assertGreater(len(calendar['calendar']), 0)
    
    def test_get_today_habits(self):
        """测试获取今日习惯"""
        self.tracker.add_habit("跑步")  # 每日
        self.tracker.add_habit(
            "每周运动",
            frequency=FrequencyType.WEEKLY,
            target_days=[date.today().weekday()],
        )
        
        habits = self.tracker.get_today_habits()
        
        self.assertEqual(len(habits), 2)
    
    def test_get_today_status(self):
        """测试今日状态"""
        self.tracker.add_habit("跑步")
        self.tracker.add_habit("阅读")
        
        # 只完成跑步
        self.tracker.complete_habit("跑步")
        
        status = self.tracker.get_today_status()
        
        self.assertIn("跑步", status)
        self.assertIn("阅读", status)
        self.assertTrue(status["跑步"]["completed"])
        self.assertFalse(status["阅读"]["completed"])
    
    def test_get_completion_heatmap(self):
        """测试热力图数据"""
        self.tracker.add_habit("跑步")
        
        today = date.today()
        for i in range(30):
            d = today - timedelta(days=i)
            if i % 2 == 0:  # 隔天完成
                self.tracker.complete_habit("跑步", target_date=d)
        
        heatmap = self.tracker.get_completion_heatmap("跑步")
        
        self.assertIn('year', heatmap)
        self.assertIn('heatmap', heatmap)
        self.assertGreater(len(heatmap['heatmap']), 0)
    
    def test_recommend_habits(self):
        """测试习惯推荐"""
        self.tracker.add_habit("跑步")
        self.tracker.add_habit("冥想")
        self.tracker.add_habit("阅读")
        
        recs = self.tracker.recommend_habits()
        
        self.assertIsInstance(recs, list)
        self.assertGreater(len(recs), 0)
        
        # 推荐不应该包含已存在的习惯
        existing_names = set(self.tracker.habits.keys())
        for rec in recs:
            self.assertNotIn(rec['name'], existing_names)
    
    def test_export_import_data(self):
        """测试数据导入导出"""
        self.tracker.add_habit("跑步", "每天跑步")
        self.tracker.complete_habit("跑步", value=30)
        
        # 导出
        json_data = self.tracker.export_data()
        self.assertIn("跑步", json_data)
        
        # 创建新追踪器导入
        new_tracker = HabitTracker()
        count = new_tracker.import_data(json_data)
        
        self.assertEqual(count, 1)
        self.assertIn("跑步", new_tracker.habits)
    
    def test_best_worst_day_analysis(self):
        """测试最佳/最差星期分析"""
        self.tracker.add_habit("跑步")
        
        today = date.today()
        
        # 模拟4周的数据
        # 周一完成率高
        for i in range(28):
            d = today - timedelta(days=i)
            # 周一总是完成
            if d.weekday() == 0:
                self.tracker.complete_habit("跑步", target_date=d)
            # 其他日子随机（这里简化为完成一半）
            elif i % 2 == 0:
                self.tracker.complete_habit("跑步", target_date=d)
        
        stats = self.tracker.get_stats("跑步")
        
        # 应该有最佳/最差星期数据
        self.assertIsNotNone(stats.best_day)


class TestHabitUtils(unittest.TestCase):
    """测试 HabitUtils 类"""
    
    def test_calculate_streak(self):
        """测试静态连续计算"""
        today = date.today()
        completions = {}
        
        # 连续5天
        for i in range(5):
            d = today - timedelta(days=i)
            completions[d] = True
        
        current, longest = HabitUtils.calculate_streak(completions)
        
        self.assertEqual(current, 5)
        self.assertEqual(longest, 5)
    
    def test_completion_rate(self):
        """测试静态完成率计算"""
        today = date.today()
        completions = {}
        
        # 10天中完成7天
        for i in range(10):
            d = today - timedelta(days=i)
            completions[d] = (i < 7)
        
        rate = HabitUtils.completion_rate(completions)
        
        self.assertEqual(rate, 0.7)
    
    def test_completion_rate_with_range(self):
        """测试指定范围的完成率"""
        today = date.today()
        completions = {}
        
        # 创建20天的数据
        for i in range(20):
            d = today - timedelta(days=i)
            completions[d] = (i < 15)  # 前15天完成
        
        # 只计算最近10天
        start = today - timedelta(days=9)
        rate = HabitUtils.completion_rate(completions, start_date=start, end_date=today)
        
        self.assertEqual(rate, 1.0)  # 最近10天都完成了


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_create_habit(self):
        """测试创建习惯便捷函数"""
        habit = create_habit("测试", description="测试描述")
        
        self.assertEqual(habit.name, "测试")
        self.assertEqual(habit.description, "测试描述")
    
    def test_calculate_streak_function(self):
        """测试连续计算便捷函数"""
        today = date.today()
        completions = {}
        
        for i in range(3):
            d = today - timedelta(days=i)
            completions[d] = True
        
        current, longest = calculate_streak(completions)
        
        self.assertEqual(current, 3)
    
    def test_completion_rate_function(self):
        """测试完成率便捷函数"""
        today = date.today()
        completions = {}
        
        for i in range(10):
            d = today - timedelta(days=i)
            completions[d] = (i < 8)
        
        rate = completion_rate(completions)
        
        self.assertEqual(rate, 0.8)


class TestFrequencyType(unittest.TestCase):
    """测试频率类型"""
    
    def test_frequency_values(self):
        """测试频率枚举值"""
        self.assertEqual(FrequencyType.DAILY.value, "daily")
        self.assertEqual(FrequencyType.WEEKLY.value, "weekly")
        self.assertEqual(FrequencyType.MONTHLY.value, "monthly")
        self.assertEqual(FrequencyType.CUSTOM.value, "custom")


class TestEdgeCases(unittest.TestCase):
    """测试边缘情况"""
    
    def test_empty_tracker(self):
        """测试空追踪器"""
        tracker = HabitTracker()
        
        self.assertEqual(len(tracker.habits), 0)
        self.assertEqual(tracker.get_stats("不存在"), None)
        self.assertEqual(tracker.get_habit("不存在"), None)
    
    def test_empty_completions_streak(self):
        """测试无完成记录的连续天数"""
        tracker = HabitTracker()
        habit = tracker.add_habit("测试")
        
        current, longest = tracker.calculate_streak(habit)
        
        self.assertEqual(current, 0)
        self.assertEqual(longest, 0)
    
    def test_empty_completions_rate(self):
        """测试无完成记录的完成率"""
        rate = HabitUtils.completion_rate({})
        
        self.assertEqual(rate, 0.0)
    
    def test_habit_with_no_due_dates(self):
        """测试无执行日期的习惯"""
        tracker = HabitTracker()
        habit = tracker.add_habit(
            "测试",
            frequency=FrequencyType.WEEKLY,
            target_days=[],  # 空列表
        )
        
        stats = tracker.get_stats("测试")
        
        self.assertEqual(stats.total_days, 0)
    
    def test_future_completion(self):
        """测试未来日期的完成"""
        tracker = HabitTracker()
        tracker.add_habit("测试")
        
        future = date.today() + timedelta(days=10)
        tracker.complete_habit("测试", target_date=future)
        
        stats = tracker.get_stats("测试", end_date=date.today())
        
        # 统计到今天，不包含未来
        self.assertEqual(stats.completed_days, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)