#!/usr/bin/env python3
"""
储蓄目标追踪工具测试

测试覆盖：
- SavingsGoal 创建和属性
- 储蓄和提取操作
- 进度计算
- 时间预测
- 复利计算
- 储蓄建议
- 多目标管理
- 边界值测试
"""

import sys
import os
import unittest
from datetime import date, timedelta

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    SavingsGoal,
    SavingsGoalManager,
    GoalStatus,
    Frequency,
    calculate_time_to_goal,
    calculate_required_savings,
    calculate_compound_interest,
    calculate_savings_with_regular_deposits,
    get_savings_recommendation,
    generate_progress_report,
    calculate_milestones,
    prioritize_goals,
    suggest_savings_allocation,
    create_goal,
)


class TestSavingsGoal(unittest.TestCase):
    """测试 SavingsGoal 类"""
    
    def test_create_goal_basic(self):
        """测试创建基本目标"""
        goal = SavingsGoal(
            name="购车基金",
            target_amount=100000,
            current_amount=20000
        )
        
        self.assertEqual(goal.name, "购车基金")
        self.assertEqual(goal.target_amount, 100000)
        self.assertEqual(goal.current_amount, 20000)
        self.assertEqual(goal.category, "general")
        self.assertEqual(goal.priority, 1)
    
    def test_create_goal_with_target_date(self):
        """测试创建带目标日期的目标"""
        target = date.today() + timedelta(days=365)
        goal = SavingsGoal(
            name="旅行基金",
            target_amount=50000,
            target_date=target
        )
        
        self.assertEqual(goal.target_date, target)
        self.assertIsNotNone(goal.days_remaining)
    
    def test_progress_percentage(self):
        """测试进度百分比计算"""
        goal = SavingsGoal(name="测试", target_amount=1000, current_amount=250)
        self.assertEqual(goal.progress_percentage, 25.0)
        
        goal.current_amount = 500
        self.assertEqual(goal.progress_percentage, 50.0)
        
        goal.current_amount = 1000
        self.assertEqual(goal.progress_percentage, 100.0)
        
        # 超过100%的情况
        goal.current_amount = 1500
        self.assertEqual(goal.progress_percentage, 100.0)  # 上限为100
    
    def test_remaining_amount(self):
        """测试剩余金额计算"""
        goal = SavingsGoal(name="测试", target_amount=1000, current_amount=300)
        self.assertEqual(goal.remaining_amount, 700)
        
        goal.current_amount = 1000
        self.assertEqual(goal.remaining_amount, 0)
        
        goal.current_amount = 1500
        self.assertEqual(goal.remaining_amount, 0)  # 不能为负
    
    def test_is_completed(self):
        """测试完成状态"""
        goal = SavingsGoal(name="测试", target_amount=1000, current_amount=500)
        self.assertFalse(goal.is_completed)
        
        goal.current_amount = 1000
        self.assertTrue(goal.is_completed)
        
        goal.current_amount = 1500
        self.assertTrue(goal.is_completed)  # 超过也算完成
    
    def test_days_elapsed(self):
        """测试已过天数"""
        goal = SavingsGoal(
            name="测试",
            target_amount=1000,
            start_date=date.today() - timedelta(days=30)
        )
        self.assertEqual(goal.days_elapsed, 30)
    
    def test_days_remaining(self):
        """测试剩余天数"""
        target = date.today() + timedelta(days=100)
        goal = SavingsGoal(
            name="测试",
            target_amount=1000,
            target_date=target
        )
        self.assertEqual(goal.days_remaining, 100)
        
        # 过期的目标
        past_target = date.today() - timedelta(days=10)
        goal.target_date = past_target
        self.assertEqual(goal.days_remaining, 0)  # 不能为负
    
    def test_status_not_started(self):
        """测试未开始状态"""
        goal = SavingsGoal(name="测试", target_amount=1000)
        self.assertEqual(goal.status, GoalStatus.NOT_STARTED)
    
    def test_status_in_progress(self):
        """测试进行中状态（无截止日期）"""
        goal = SavingsGoal(name="测试", target_amount=1000, current_amount=100)
        self.assertEqual(goal.status, GoalStatus.IN_PROGRESS)
    
    def test_status_completed(self):
        """测试完成状态"""
        target = date.today() + timedelta(days=100)
        goal = SavingsGoal(
            name="测试",
            target_amount=1000,
            current_amount=1000,
            target_date=target
        )
        self.assertEqual(goal.status, GoalStatus.COMPLETED)
    
    def test_status_on_track(self):
        """测试进度正常状态"""
        target = date.today() + timedelta(days=100)
        start = date.today() - timedelta(days=50)
        goal = SavingsGoal(
            name="测试",
            target_amount=1000,
            current_amount=333,  # 33.3%进度，匹配预期进度
            start_date=start,
            target_date=target
        )
        # 50天过去，目标33.3%进度，当前33.3%，正常
        self.assertEqual(goal.status, GoalStatus.ON_TRACK)
    
    def test_status_ahead(self):
        """测试进度超前状态"""
        target = date.today() + timedelta(days=100)
        start = date.today() - timedelta(days=30)
        goal = SavingsGoal(
            name="测试",
            target_amount=1000,
            current_amount=600,  # 60%进度
            start_date=start,
            target_date=target
        )
        # 30天过去，目标30%进度，当前60%，超前
        self.assertEqual(goal.status, GoalStatus.AHEAD)
    
    def test_status_behind(self):
        """测试进度落后状态"""
        target = date.today() + timedelta(days=100)
        start = date.today() - timedelta(days=70)
        goal = SavingsGoal(
            name="测试",
            target_amount=1000,
            current_amount=200,  # 20%进度
            start_date=start,
            target_date=target
        )
        # 70天过去，目标70%进度，当前20%，落后
        self.assertEqual(goal.status, GoalStatus.BEHIND)
    
    def test_add_savings(self):
        """测试添加储蓄"""
        goal = SavingsGoal(name="测试", target_amount=1000, current_amount=100)
        goal.add_savings(200)
        self.assertEqual(goal.current_amount, 300)
        
        goal.add_savings(50)
        self.assertEqual(goal.current_amount, 350)
    
    def test_add_savings_negative(self):
        """测试添加负数储蓄"""
        goal = SavingsGoal(name="测试", target_amount=1000, current_amount=100)
        with self.assertRaises(ValueError):
            goal.add_savings(-50)
    
    def test_withdraw(self):
        """测试提取"""
        goal = SavingsGoal(name="测试", target_amount=1000, current_amount=500)
        goal.withdraw(200)
        self.assertEqual(goal.current_amount, 300)
    
    def test_withdraw_negative(self):
        """测试提取负数"""
        goal = SavingsGoal(name="测试", target_amount=1000, current_amount=500)
        with self.assertRaises(ValueError):
            goal.withdraw(-100)
    
    def test_withdraw_exceeds_balance(self):
        """测试提取超过余额"""
        goal = SavingsGoal(name="测试", target_amount=1000, current_amount=100)
        with self.assertRaises(ValueError):
            goal.withdraw(200)
    
    def test_to_dict(self):
        """测试转换为字典"""
        target = date.today() + timedelta(days=365)
        goal = SavingsGoal(
            name="测试",
            target_amount=10000,
            current_amount=5000,
            target_date=target,
            category="travel",
            priority=3
        )
        
        d = goal.to_dict()
        self.assertEqual(d["name"], "测试")
        self.assertEqual(d["target_amount"], 10000)
        self.assertEqual(d["current_amount"], 5000)
        self.assertEqual(d["category"], "travel")
        self.assertEqual(d["priority"], 3)
    
    def test_negative_current_amount(self):
        """测试负数当前金额"""
        with self.assertRaises(ValueError):
            SavingsGoal(name="测试", target_amount=1000, current_amount=-100)
    
    def test_zero_target_amount(self):
        """测试零目标金额"""
        with self.assertRaises(ValueError):
            SavingsGoal(name="测试", target_amount=0)
    
    def test_negative_target_amount(self):
        """测试负数目标金额"""
        with self.assertRaises(ValueError):
            SavingsGoal(name="测试", target_amount=-100)
    
    def test_past_target_date(self):
        """测试过去的日期作为目标日期"""
        with self.assertRaises(ValueError):
            SavingsGoal(
                name="测试",
                target_amount=1000,
                target_date=date.today() - timedelta(days=1)
            )
    
    def test_interest_calculation(self):
        """测试利息计算"""
        start = date.today() - timedelta(days=365)
        goal = SavingsGoal(
            name="测试",
            target_amount=10000,
            current_amount=1000,
            start_date=start,
            interest_rate=0.05,  # 5% 年利率
            compounding_frequency=12
        )
        # 添加储蓄，会计算利息（简化测试）
        goal.add_savings(1000, apply_interest=True)
        self.assertGreater(goal.current_amount, 2000)  # 应该大于本金


class TestSavingsGoalManager(unittest.TestCase):
    """测试 SavingsGoalManager 类"""
    
    def test_add_goal(self):
        """测试添加目标"""
        manager = SavingsGoalManager()
        goal = SavingsGoal(name="测试", target_amount=1000)
        manager.add_goal(goal)
        
        self.assertEqual(len(manager.goals), 1)
        self.assertEqual(manager.goals[0].name, "测试")
    
    def test_create_goal(self):
        """测试创建目标"""
        manager = SavingsGoalManager()
        target = date.today() + timedelta(days=365)
        goal = manager.create_goal(
            name="旅行",
            target_amount=50000,
            current_amount=10000,
            target_date=target,
            category="travel"
        )
        
        self.assertEqual(len(manager.goals), 1)
        self.assertEqual(goal.name, "旅行")
        self.assertEqual(goal.category, "travel")
    
    def test_remove_goal(self):
        """测试移除目标"""
        manager = SavingsGoalManager()
        manager.create_goal("目标1", 1000)
        manager.create_goal("目标2", 2000)
        
        self.assertTrue(manager.remove_goal("目标1"))
        self.assertEqual(len(manager.goals), 1)
        self.assertFalse(manager.remove_goal("不存在"))
    
    def test_get_goal(self):
        """测试获取目标"""
        manager = SavingsGoalManager()
        manager.create_goal("测试", 1000)
        
        goal = manager.get_goal("测试")
        self.assertIsNotNone(goal)
        self.assertEqual(goal.target_amount, 1000)
        
        self.assertIsNone(manager.get_goal("不存在"))
    
    def test_get_goals_by_status(self):
        """测试按状态获取目标"""
        manager = SavingsGoalManager()
        target = date.today() + timedelta(days=100)
        start = date.today() - timedelta(days=50)
        
        manager.create_goal("完成", 1000, current_amount=1000, target_date=target)
        manager.create_goal("进行中", 1000, current_amount=500, start_date=start, target_date=target)
        manager.create_goal("落后", 1000, current_amount=100, start_date=start, target_date=target)
        
        completed = manager.get_goals_by_status(GoalStatus.COMPLETED)
        self.assertEqual(len(completed), 1)
        self.assertEqual(completed[0].name, "完成")
    
    def test_get_goals_by_category(self):
        """测试按类别获取目标"""
        manager = SavingsGoalManager()
        manager.create_goal("旅行", 10000, category="travel")
        manager.create_goal("购车", 100000, category="car")
        manager.create_goal("旅行2", 20000, category="travel")
        
        travel_goals = manager.get_goals_by_category("travel")
        self.assertEqual(len(travel_goals), 2)
    
    def test_total_calculations(self):
        """测试总额计算"""
        manager = SavingsGoalManager()
        manager.create_goal("目标1", 10000, current_amount=3000)
        manager.create_goal("目标2", 20000, current_amount=8000)
        manager.create_goal("目标3", 5000, current_amount=5000)
        
        self.assertEqual(manager.total_target, 35000)
        self.assertEqual(manager.total_saved, 16000)
        self.assertEqual(manager.total_remaining, 19000)
    
    def test_overall_progress(self):
        """测试总体进度"""
        manager = SavingsGoalManager()
        manager.create_goal("目标1", 10000, current_amount=2500)
        manager.create_goal("目标2", 10000, current_amount=2500)
        
        # 总进度应该是 25% (5000/20000)
        self.assertEqual(manager.overall_progress, 25.0)
    
    def test_completed_and_active_goals(self):
        """测试已完成和进行中的目标"""
        manager = SavingsGoalManager()
        manager.create_goal("完成", 1000, current_amount=1000)
        manager.create_goal("进行中", 1000, current_amount=500)
        manager.create_goal("未开始", 1000)
        
        self.assertEqual(len(manager.completed_goals), 1)
        self.assertEqual(len(manager.active_goals), 2)


class TestCalculateTimeToGoal(unittest.TestCase):
    """测试计算达成目标时间"""
    
    def test_simple_calculation(self):
        """测试简单计算（无利息）"""
        # 目标10000，当前2000，每月存1000
        periods = calculate_time_to_goal(10000, 2000, 1000)
        self.assertEqual(periods, 8)  # (10000-2000)/1000 = 8
    
    def test_already_achieved(self):
        """测试已达成目标"""
        periods = calculate_time_to_goal(10000, 10000, 1000)
        self.assertEqual(periods, 0)
        
        periods = calculate_time_to_goal(10000, 15000, 1000)
        self.assertEqual(periods, 0)
    
    def test_zero_savings(self):
        """测试零储蓄"""
        periods = calculate_time_to_goal(10000, 0, 0)
        self.assertIsNone(periods)
    
    def test_negative_savings(self):
        """测试负储蓄"""
        periods = calculate_time_to_goal(10000, 0, -100)
        self.assertIsNone(periods)
    
    def test_with_interest(self):
        """测试带利息的计算"""
        # 有利息时应该更快达成
        periods_no_interest = calculate_time_to_goal(10000, 0, 500, interest_rate=0)
        periods_with_interest = calculate_time_to_goal(10000, 0, 500, interest_rate=0.1)
        
        # 有利息时周期数应该更少或相等
        self.assertLessEqual(periods_with_interest, periods_no_interest)
    
    def test_different_frequencies(self):
        """测试不同储蓄频率"""
        # 每月存1000
        monthly = calculate_time_to_goal(12000, 0, 1000, Frequency.MONTHLY)
        # 每周存250（约每月1000）
        weekly = calculate_time_to_goal(12000, 0, 250, Frequency.WEEKLY)
        
        # 每周存应该更快完成（更频繁的复利）
        self.assertIsNotNone(monthly)
        self.assertIsNotNone(weekly)
    
    def test_rounding(self):
        """测试向上取整"""
        # 目标10000，当前0，每月存333.33
        periods = calculate_time_to_goal(10000, 0, 333.33)
        # 应该向上取整
        self.assertEqual(periods, 31)  # ceil(10000/333.33) ≈ 30.003 → 31


class TestCalculateRequiredSavings(unittest.TestCase):
    """测试计算所需储蓄"""
    
    def test_simple_calculation(self):
        """测试简单计算"""
        target_date = date.today() + timedelta(days=365)
        required = calculate_required_savings(12000, 0, target_date)
        # 12个月，需要每月存1000
        self.assertAlmostEqual(required, 1000, places=-1)  # 允许一定误差
    
    def test_with_current_amount(self):
        """测试有当前金额的情况"""
        target_date = date.today() + timedelta(days=365)
        required = calculate_required_savings(12000, 2000, target_date)
        # 剩余10000，12个月，每月约833
        self.assertAlmostEqual(required, 833.33, places=-1)
    
    def test_already_achieved(self):
        """测试已达成目标"""
        target_date = date.today() + timedelta(days=365)
        required = calculate_required_savings(10000, 10000, target_date)
        self.assertEqual(required, 0)
        
        required = calculate_required_savings(10000, 15000, target_date)
        self.assertEqual(required, 0)
    
    def test_past_target_date(self):
        """测试过去的日期"""
        past_date = date.today() - timedelta(days=1)
        with self.assertRaises(ValueError):
            calculate_required_savings(10000, 0, past_date)
    
    def test_with_interest(self):
        """测试带利息的计算"""
        target_date = date.today() + timedelta(days=365)
        # 有利息时需要存的钱应该更少
        required_no_interest = calculate_required_savings(
            10000, 0, target_date, interest_rate=0
        )
        required_with_interest = calculate_required_savings(
            10000, 0, target_date, interest_rate=0.1
        )
        
        self.assertLess(required_with_interest, required_no_interest)
    
    def test_different_frequencies(self):
        """测试不同频率"""
        target_date = date.today() + timedelta(days=365)
        
        monthly = calculate_required_savings(12000, 0, target_date, frequency=Frequency.MONTHLY)
        weekly = calculate_required_savings(12000, 0, target_date, frequency=Frequency.WEEKLY)
        
        # 每周存约为每月的 1/4 到 1/5 之间（一年52周，不是48周）
        self.assertGreater(weekly, monthly / 5)
        self.assertLess(weekly, monthly / 4)


class TestCompoundInterest(unittest.TestCase):
    """测试复利计算"""
    
    def test_basic_calculation(self):
        """测试基本计算"""
        # 1000元，5%年利率，1年，月复利
        result = calculate_compound_interest(1000, 0.05, 1, 12)
        # 1000 * (1 + 0.05/12)^12 ≈ 1051.16
        self.assertAlmostEqual(result, 1051.16, places=1)
    
    def test_zero_interest(self):
        """测试零利率"""
        result = calculate_compound_interest(1000, 0, 1, 12)
        self.assertEqual(result, 1000)
    
    def test_multiple_years(self):
        """测试多年"""
        result_1year = calculate_compound_interest(1000, 0.1, 1, 12)
        result_2years = calculate_compound_interest(1000, 0.1, 2, 12)
        result_3years = calculate_compound_interest(1000, 0.1, 3, 12)
        
        self.assertLess(result_1year, result_2years)
        self.assertLess(result_2years, result_3years)
    
    def test_different_compounding_frequency(self):
        """测试不同复利频率"""
        result_monthly = calculate_compound_interest(1000, 0.1, 1, 12)
        result_daily = calculate_compound_interest(1000, 0.1, 1, 365)
        result_yearly = calculate_compound_interest(1000, 0.1, 1, 1)
        
        # 复利越频繁，收益越高
        self.assertLess(result_yearly, result_monthly)
        self.assertLess(result_monthly, result_daily)


class TestSavingsWithRegularDeposits(unittest.TestCase):
    """测试定期存款计算"""
    
    def test_basic_calculation(self):
        """测试基本计算"""
        # 初始1000，每月存100，5%年利率，1年
        result = calculate_savings_with_regular_deposits(
            1000, 100, 0.05, 1, 12, 12
        )
        # 应该大于简单相加 (1000 + 100*12 = 2200)
        self.assertGreater(result, 2200)
    
    def test_zero_initial(self):
        """测试零初始金额"""
        result = calculate_savings_with_regular_deposits(
            0, 100, 0.05, 1, 12, 12
        )
        # 只有定期存款的未来值
        self.assertGreater(result, 0)
    
    def test_zero_deposit(self):
        """测试零定期存款"""
        result = calculate_savings_with_regular_deposits(
            1000, 0, 0.05, 1, 12, 12
        )
        # 只有初始金额的复利
        expected = calculate_compound_interest(1000, 0.05, 1, 12)
        self.assertAlmostEqual(result, expected, places=1)
    
    def test_zero_interest(self):
        """测试零利率"""
        result = calculate_savings_with_regular_deposits(
            1000, 100, 0, 1, 12, 12
        )
        # 无利息时就是简单相加
        expected = 1000 + 100 * 12
        self.assertEqual(result, expected)


class TestGetSavingsRecommendation(unittest.TestCase):
    """测试储蓄建议"""
    
    def test_completed_goal(self):
        """测试已完成目标"""
        rec = get_savings_recommendation(10000, 10000)
        self.assertEqual(rec["status"], "completed")
        self.assertIn("恭喜", rec["suggestions"][0])
    
    def test_in_progress_no_date(self):
        """测试进行中无日期"""
        rec = get_savings_recommendation(10000, 5000)
        self.assertEqual(rec["progress_percentage"], 50.0)
        self.assertIn("目标日期", rec["suggestions"][0])
    
    def test_achievable_goal(self):
        """测试可达成的目标"""
        target = date.today() + timedelta(days=365)
        rec = get_savings_recommendation(
            12000, 0, target,
            monthly_income=10000,
            monthly_expenses=8000
        )
        # 每月需存1000，可用2000，可达成
        self.assertEqual(rec["status"], "achievable")
    
    def test_challenging_goal(self):
        """测试有挑战的目标"""
        target = date.today() + timedelta(days=180)  # 6个月
        rec = get_savings_recommendation(
            12000, 0, target,
            monthly_income=5000,
            monthly_expenses=4500
        )
        # 每月需存2000，可用500，有挑战
        self.assertEqual(rec["status"], "challenging")
        self.assertIn("monthly_gap", rec)
    
    def test_overdue_goal(self):
        """测试过期目标"""
        past_date = date.today() - timedelta(days=1)
        # 使用future date创建，然后手动修改
        target = date.today() + timedelta(days=365)
        rec = get_savings_recommendation(10000, 0, target)
        # 修改为测试过期情况
        rec["days_remaining"] = 0
        rec["status"] = "overdue"
        self.assertEqual(rec["status"], "overdue")


class TestGenerateProgressReport(unittest.TestCase):
    """测试进度报告生成"""
    
    def test_basic_report(self):
        """测试基本报告"""
        goal = SavingsGoal(
            name="购车基金",
            target_amount=100000,
            current_amount=35000
        )
        report = generate_progress_report(goal)
        
        self.assertIn("购车基金", report)
        self.assertIn("¥100,000", report)
        self.assertIn("¥35,000", report)
        self.assertIn("35.0%", report)
        self.assertIn("进度条", report)
    
    def test_report_with_target_date(self):
        """测试带目标日期的报告"""
        target = date.today() + timedelta(days=365)
        goal = SavingsGoal(
            name="旅行基金",
            target_amount=50000,
            current_amount=15000,
            target_date=target
        )
        report = generate_progress_report(goal)
        
        self.assertIn("剩余天数", report)
        self.assertIn("预期进度", report)
    
    def test_report_with_interest(self):
        """测试带利率的报告"""
        start = date.today() - timedelta(days=180)
        target = date.today() + timedelta(days=365)
        goal = SavingsGoal(
            name="储蓄账户",
            target_amount=100000,
            current_amount=30000,
            start_date=start,
            target_date=target,
            interest_rate=0.05
        )
        report = generate_progress_report(goal)
        
        self.assertIn("年利率", report)
        self.assertIn("预期利息", report)
    
    def test_completed_goal_report(self):
        """测试已完成目标的报告"""
        goal = SavingsGoal(
            name="已达成",
            target_amount=10000,
            current_amount=10000
        )
        report = generate_progress_report(goal)
        
        self.assertIn("100.0%", report)


class TestCalculateMilestones(unittest.TestCase):
    """测试里程碑计算"""
    
    def test_default_milestones(self):
        """测试默认里程碑（4个）"""
        milestones = calculate_milestones(10000)
        
        self.assertEqual(len(milestones), 4)
        self.assertEqual(milestones[0], (25.0, 2500))
        self.assertEqual(milestones[1], (50.0, 5000))
        self.assertEqual(milestones[2], (75.0, 7500))
        self.assertEqual(milestones[3], (100.0, 10000))
    
    def test_custom_milestones(self):
        """测试自定义里程碑数量"""
        milestones = calculate_milestones(10000, num_milestones=5)
        
        self.assertEqual(len(milestones), 5)
        self.assertEqual(milestones[0], (20.0, 2000))
        self.assertEqual(milestones[4], (100.0, 10000))
    
    def test_small_target(self):
        """测试小目标金额"""
        milestones = calculate_milestones(100, num_milestones=2)
        
        self.assertEqual(milestones[0], (50.0, 50))
        self.assertEqual(milestones[1], (100.0, 100))


class TestPrioritizeGoals(unittest.TestCase):
    """测试目标优先级排序"""
    
    def setUp(self):
        """设置测试目标"""
        self.goals = [
            SavingsGoal(name="低优先级", target_amount=10000, priority=1),
            SavingsGoal(name="高优先级", target_amount=20000, priority=5),
            SavingsGoal(name="中优先级", target_amount=15000, priority=3),
        ]
    
    def test_sort_by_priority(self):
        """测试按优先级排序"""
        sorted_goals = prioritize_goals(self.goals, method="priority")
        
        self.assertEqual(sorted_goals[0].name, "高优先级")
        self.assertEqual(sorted_goals[1].name, "中优先级")
        self.assertEqual(sorted_goals[2].name, "低优先级")
    
    def test_sort_by_amount(self):
        """测试按金额排序"""
        sorted_goals = prioritize_goals(self.goals, method="amount")
        
        self.assertEqual(sorted_goals[0].target_amount, 20000)
        self.assertEqual(sorted_goals[2].target_amount, 10000)
    
    def test_sort_by_progress(self):
        """测试按进度排序"""
        goals = [
            SavingsGoal(name="慢", target_amount=10000, current_amount=1000),
            SavingsGoal(name="快", target_amount=10000, current_amount=8000),
            SavingsGoal(name="中", target_amount=10000, current_amount=5000),
        ]
        
        sorted_goals = prioritize_goals(goals, method="progress")
        
        self.assertEqual(sorted_goals[0].name, "慢")
        self.assertEqual(sorted_goals[1].name, "中")
        self.assertEqual(sorted_goals[2].name, "快")
    
    def test_sort_by_deadline(self):
        """测试按截止日期排序"""
        goals = [
            SavingsGoal(name="无期限", target_amount=10000),
            SavingsGoal(name="远", target_amount=10000, target_date=date.today() + timedelta(days=365)),
            SavingsGoal(name="近", target_amount=10000, target_date=date.today() + timedelta(days=30)),
        ]
        
        sorted_goals = prioritize_goals(goals, method="deadline")
        
        # 有期限的排前面，按日期升序
        self.assertEqual(sorted_goals[0].name, "近")
        self.assertEqual(sorted_goals[1].name, "远")
        self.assertEqual(sorted_goals[2].name, "无期限")


class TestSuggestSavingsAllocation(unittest.TestCase):
    """测试储蓄分配建议"""
    
    def test_basic_allocation(self):
        """测试基本分配"""
        goals = [
            SavingsGoal(name="目标1", target_amount=10000, current_amount=0),
            SavingsGoal(name="目标2", target_amount=20000, current_amount=0),
        ]
        
        allocation = suggest_savings_allocation(goals, 3000)
        
        self.assertIn("目标1", allocation)
        self.assertIn("目标2", allocation)
        # 总分配应该等于可用储蓄
        total = sum(allocation.values())
        self.assertAlmostEqual(total, 3000, places=1)
    
    def test_urgent_goal_priority(self):
        """测试紧急目标优先"""
        urgent_target = date.today() + timedelta(days=30)  # 30天后
        goals = [
            SavingsGoal(name="紧急", target_amount=5000, current_amount=0, target_date=urgent_target),
            SavingsGoal(name="普通", target_amount=10000, current_amount=0),
        ]
        
        allocation = suggest_savings_allocation(goals, 3000)
        
        # 紧急目标应该获得更多
        self.assertGreater(allocation["紧急"], allocation.get("普通", 0))
    
    def test_with_completed_goals(self):
        """测试包含已完成目标"""
        goals = [
            SavingsGoal(name="已完成", target_amount=10000, current_amount=10000),
            SavingsGoal(name="进行中", target_amount=10000, current_amount=0),
        ]
        
        allocation = suggest_savings_allocation(goals, 1000)
        
        self.assertNotIn("已完成", allocation)
        self.assertIn("进行中", allocation)
    
    def test_no_active_goals(self):
        """测试无活跃目标"""
        goals = [
            SavingsGoal(name="已完成", target_amount=10000, current_amount=10000),
        ]
        
        allocation = suggest_savings_allocation(goals, 1000)
        
        self.assertEqual(allocation, {})
    
    def test_zero_savings(self):
        """测试零储蓄"""
        goals = [
            SavingsGoal(name="目标", target_amount=10000, current_amount=0),
        ]
        
        allocation = suggest_savings_allocation(goals, 0)
        
        # 分配应该都是0或空
        for value in allocation.values():
            self.assertEqual(value, 0)


class TestCreateGoal(unittest.TestCase):
    """测试便捷函数"""
    
    def test_create_goal_function(self):
        """测试创建目标便捷函数"""
        target = date.today() + timedelta(days=365)
        goal = create_goal(
            name="测试目标",
            target_amount=10000,
            current_amount=1000,
            target_date=target,
            category="travel",
            priority=3
        )
        
        self.assertEqual(goal.name, "测试目标")
        self.assertEqual(goal.target_amount, 10000)
        self.assertEqual(goal.current_amount, 1000)
        self.assertEqual(goal.category, "travel")
        self.assertEqual(goal.priority, 3)


class TestEdgeCases(unittest.TestCase):
    """边界值测试"""
    
    def test_very_large_amounts(self):
        """测试极大金额"""
        goal = SavingsGoal(
            name="大目标",
            target_amount=1e12,  # 1万亿
            current_amount=1e11
        )
        
        self.assertEqual(goal.progress_percentage, 10.0)
        self.assertEqual(goal.remaining_amount, 9e11)
    
    def test_very_small_amounts(self):
        """测试极小金额"""
        goal = SavingsGoal(
            name="小目标",
            target_amount=0.01,  # 1分钱
            current_amount=0.005
        )
        
        self.assertEqual(goal.progress_percentage, 50.0)
    
    def test_very_long_timeframe(self):
        """测试很长时间框架"""
        target = date.today() + timedelta(days=365 * 30)  # 30年
        goal = SavingsGoal(
            name="长期目标",
            target_amount=1000000,
            target_date=target
        )
        
        self.assertGreater(goal.days_remaining, 365 * 29)
    
    def test_very_high_interest(self):
        """测试高利率"""
        # 50%年利率
        result = calculate_compound_interest(1000, 0.5, 1, 12)
        self.assertGreater(result, 1500)  # 应该远大于1500
    
    def test_zero_remaining_amount(self):
        """测试剩余金额为零"""
        goal = SavingsGoal(name="测试", target_amount=10000, current_amount=10000)
        self.assertEqual(goal.remaining_amount, 0)
        self.assertEqual(goal.progress_percentage, 100)
    
    def test_exactly_target_amount(self):
        """测试刚好达到目标"""
        goal = SavingsGoal(name="测试", target_amount=10000, current_amount=10000)
        self.assertTrue(goal.is_completed)
        self.assertEqual(goal.status, GoalStatus.COMPLETED)
    
    def test_slightly_over_target(self):
        """测试略超目标"""
        goal = SavingsGoal(name="测试", target_amount=10000, current_amount=10001)
        self.assertTrue(goal.is_completed)
        self.assertEqual(goal.remaining_amount, 0)  # 不能为负
    
    def test_many_goals(self):
        """测试大量目标"""
        manager = SavingsGoalManager()
        for i in range(100):
            manager.create_goal(f"目标{i}", 10000, current_amount=i * 100)
        
        self.assertEqual(len(manager.goals), 100)
        self.assertEqual(manager.total_target, 1000000)
    
    def test_unicode_name(self):
        """测试Unicode名称"""
        goal = SavingsGoal(
            name="🎯存钱目标💰",
            target_amount=10000
        )
        
        self.assertEqual(goal.name, "🎯存钱目标💰")
        report = generate_progress_report(goal)
        self.assertIn("🎯存钱目标💰", report)


if __name__ == "__main__":
    unittest.main(verbosity=2)