"""
Tabata Utilities 测试文件

测试 Tabata 高强度间歇训练工具的所有功能。
"""

import unittest
import time
from typing import List, Tuple

# 导入被测试模块
from mod import (
    PhaseType,
    TabataRound,
    TabataSession,
    SessionStats,
    TabataTimer,
    TabataPresets,
    TabataBuilder,
    TabataFormatter,
    TabataCalculator,
    create_tabata,
    get_preset,
    list_presets,
)


class TestTabataRound(unittest.TestCase):
    """测试 TabataRound"""
    
    def test_round_creation(self):
        """测试创建轮次"""
        round_ = TabataRound(round_number=1, work_duration=20, rest_duration=10)
        self.assertEqual(round_.round_number, 1)
        self.assertEqual(round_.work_duration, 20)
        self.assertEqual(round_.rest_duration, 10)
    
    def test_total_duration(self):
        """测试轮次总时长"""
        round_ = TabataRound(round_number=1, work_duration=20, rest_duration=10)
        self.assertEqual(round_.total_duration, 30)


class TestTabataSession(unittest.TestCase):
    """测试 TabataSession"""
    
    def test_standard_session(self):
        """测试标准 Tabata 会话"""
        session = TabataSession(rounds=8, work_duration=20, rest_duration=10)
        
        self.assertEqual(session.rounds, 8)
        self.assertEqual(session.work_duration, 20)
        self.assertEqual(session.rest_duration, 10)
        self.assertEqual(session.prepare_duration, 10)  # 默认值
        self.assertEqual(session.name, "Tabata")  # 默认值
    
    def test_total_duration(self):
        """测试总时长计算"""
        session = TabataSession(
            rounds=8,
            work_duration=20,
            rest_duration=10,
            prepare_duration=10
        )
        # 准备10 + (运动20 + 休息10) × 8 = 10 + 240 = 250
        self.assertEqual(session.total_duration, 250)
    
    def test_total_work_time(self):
        """测试总运动时长"""
        session = TabataSession(rounds=8, work_duration=20, rest_duration=10)
        self.assertEqual(session.total_work_time, 160)  # 20 × 8
    
    def test_total_rest_time(self):
        """测试总休息时长"""
        session = TabataSession(rounds=8, work_duration=20, rest_duration=10)
        self.assertEqual(session.total_rest_time, 80)  # 10 × 8
    
    def test_get_exercise(self):
        """测试获取运动名称"""
        session = TabataSession(
            rounds=8,
            work_duration=20,
            rest_duration=10,
            exercises=["Push-ups", "Squats", "Burpees"]
        )
        
        self.assertEqual(session.get_exercise(1), "Push-ups")
        self.assertEqual(session.get_exercise(2), "Squats")
        self.assertEqual(session.get_exercise(3), "Burpees")
        self.assertEqual(session.get_exercise(4), "Push-ups")  # 循环
    
    def test_get_exercise_empty(self):
        """测试无运动列表时的获取"""
        session = TabataSession(rounds=8, work_duration=20, rest_duration=10)
        self.assertEqual(session.get_exercise(1), "Round 1")
        self.assertEqual(session.get_exercise(5), "Round 5")


class TestSessionStats(unittest.TestCase):
    """测试 SessionStats"""
    
    def test_stats_creation(self):
        """测试创建统计"""
        session = TabataSession(rounds=8, work_duration=20, rest_duration=10)
        stats = SessionStats(session=session)
        
        self.assertEqual(stats.session, session)
        self.assertEqual(stats.start_time, 0)
        self.assertEqual(stats.end_time, 0)
        self.assertEqual(stats.completed_rounds, 0)
    
    def test_actual_duration(self):
        """测试实际时长计算"""
        session = TabataSession(rounds=8, work_duration=20, rest_duration=10)
        stats = SessionStats(
            session=session,
            start_time=100,
            end_time=360,
            total_paused_time=10
        )
        # 实际时长 = 360 - 100 - 10 = 250
        self.assertEqual(stats.actual_duration, 250)
    
    def test_completion_rate(self):
        """测试完成率"""
        session = TabataSession(rounds=8, work_duration=20, rest_duration=10)
        
        stats_full = SessionStats(session=session, completed_rounds=8)
        self.assertEqual(stats_full.completion_rate, 100.0)
        
        stats_half = SessionStats(session=session, completed_rounds=4)
        self.assertEqual(stats_half.completion_rate, 50.0)
    
    def test_to_dict(self):
        """测试转换为字典"""
        session = TabataSession(rounds=8, work_duration=20, rest_duration=10, name="Test")
        stats = SessionStats(
            session=session,
            completed_rounds=6,
            start_time=100,
            end_time=300,
            calories_burned_estimate=50
        )
        
        result = stats.to_dict()
        self.assertIn('name', result)
        self.assertIn('completed_rounds', result)
        self.assertIn('completion_rate', result)


class TestTabataPresets(unittest.TestCase):
    """测试 TabataPresets"""
    
    def test_standard_preset(self):
        """测试标准预设"""
        preset = TabataPresets.STANDARD
        
        self.assertEqual(preset.rounds, 8)
        self.assertEqual(preset.work_duration, 20)
        self.assertEqual(preset.rest_duration, 10)
        self.assertEqual(preset.name, "Standard Tabata")
    
    def test_double_preset(self):
        """测试双倍预设"""
        preset = TabataPresets.DOUBLE
        self.assertEqual(preset.rounds, 16)
    
    def test_half_preset(self):
        """测试半程预设"""
        preset = TabataPresets.HALF
        self.assertEqual(preset.rounds, 4)
    
    def test_extended_preset(self):
        """测试延长预设"""
        preset = TabataPresets.EXTENDED
        self.assertEqual(preset.work_duration, 30)
        self.assertEqual(preset.rest_duration, 15)
    
    def test_get_all_presets(self):
        """测试获取所有预设"""
        presets = TabataPresets.get_all_presets()
        self.assertGreater(len(presets), 0)
    
    def test_get_by_name(self):
        """测试按名称获取"""
        preset = TabataPresets.get_by_name("Standard Tabata")
        self.assertIsNotNone(preset)
        self.assertEqual(preset.rounds, 8)
        
        preset_lower = TabataPresets.get_by_name("standard tabata")
        self.assertIsNotNone(preset_lower)
    
    def test_get_by_name_not_found(self):
        """测试不存在的预设"""
        preset = TabataPresets.get_by_name("Non-existent")
        self.assertIsNone(preset)


class TestTabataBuilder(unittest.TestCase):
    """测试 TabataBuilder"""
    
    def test_build_basic(self):
        """测试基本构建"""
        session = TabataBuilder().build()
        
        self.assertEqual(session.rounds, 8)  # 默认
        self.assertEqual(session.work_duration, 20)  # 默认
        self.assertEqual(session.rest_duration, 10)  # 默认
    
    def test_build_custom(self):
        """测试自定义构建"""
        session = (TabataBuilder()
                  .rounds(10)
                  .work(30)
                  .rest(15)
                  .prepare(5)
                  .name("My Workout")
                  .build())
        
        self.assertEqual(session.rounds, 10)
        self.assertEqual(session.work_duration, 30)
        self.assertEqual(session.rest_duration, 15)
        self.assertEqual(session.prepare_duration, 5)
        self.assertEqual(session.name, "My Workout")
    
    def test_build_with_exercises(self):
        """测试带运动的构建"""
        session = (TabataBuilder()
                  .exercises("Push-ups", "Squats", "Burpees")
                  .build())
        
        self.assertEqual(len(session.exercises), 3)
        self.assertIn("Push-ups", session.exercises)
    
    def test_invalid_rounds(self):
        """测试无效轮数"""
        with self.assertRaises(ValueError):
            TabataBuilder().rounds(0).build()
        
        with self.assertRaises(ValueError):
            TabataBuilder().rounds(-1).build()
    
    def test_invalid_work_duration(self):
        """测试无效运动时长"""
        with self.assertRaises(ValueError):
            TabataBuilder().work(0).build()
        
        with self.assertRaises(ValueError):
            TabataBuilder().work(-5).build()
    
    def test_invalid_rest_duration(self):
        """测试无效休息时长"""
        with self.assertRaises(ValueError):
            TabataBuilder().rest(-1).build()


class TestTabataFormatter(unittest.TestCase):
    """测试 TabataFormatter"""
    
    def test_format_duration_seconds(self):
        """测试秒格式化"""
        self.assertEqual(TabataFormatter.format_duration(30), "30s")
        self.assertEqual(TabataFormatter.format_duration(59), "59s")
    
    def test_format_duration_minutes(self):
        """测试分钟格式化"""
        self.assertEqual(TabataFormatter.format_duration(60), "1m")
        self.assertEqual(TabataFormatter.format_duration(90), "1m 30s")
        self.assertEqual(TabataFormatter.format_duration(120), "2m")
        self.assertEqual(TabataFormatter.format_duration(150), "2m 30s")
    
    def test_format_countdown(self):
        """测试倒计时格式化"""
        self.assertEqual(TabataFormatter.format_countdown(30), "30.0")
        self.assertEqual(TabataFormatter.format_countdown(90), "01:30.0")
        self.assertEqual(TabataFormatter.format_countdown(0), "00.0")
        self.assertEqual(TabataFormatter.format_countdown(-1), "00.0")
    
    def test_format_session(self):
        """测试会话格式化"""
        session = TabataSession(
            rounds=8,
            work_duration=20,
            rest_duration=10,
            prepare_duration=10,
            name="Test Session"
        )
        
        result = TabataFormatter.format_session(session)
        self.assertIn("Test Session", result)
        self.assertIn("Rounds: 8", result)
        self.assertIn("Work: 20s", result)
        self.assertIn("Rest: 10s", result)
    
    def test_format_stats(self):
        """测试统计格式化"""
        session = TabataSession(rounds=8, work_duration=20, rest_duration=10, name="Test")
        stats = SessionStats(
            session=session,
            completed_rounds=8,
            start_time=100,
            end_time=360,
            calories_burned_estimate=50
        )
        
        result = TabataFormatter.format_stats(stats)
        self.assertIn("Test Complete", result)
        self.assertIn("8/8", result)
        self.assertIn("100.0%", result)
    
    def test_format_progress(self):
        """测试进度条"""
        result = TabataFormatter.format_progress(5, 10, width=10)
        self.assertIn("█", result)
        self.assertIn("50%", result)
        
        result_full = TabataFormatter.format_progress(10, 10, width=10)
        self.assertIn("100%", result_full)
        
        result_zero = TabataFormatter.format_progress(0, 10, width=10)
        self.assertIn("0%", result_zero)


class TestTabataCalculator(unittest.TestCase):
    """测试 TabataCalculator"""
    
    def test_calories_burned(self):
        """测试卡路里计算"""
        session = TabataSession(rounds=8, work_duration=20, rest_duration=10)
        calories = TabataCalculator.calories_burned(session, weight_kg=70)
        
        # 标准Tabata：160秒运动 ≈ 2.67分钟
        # 卡路里 = 10 MET × 70kg × 2.67分钟 × 0.0175 ≈ 32 kcal
        self.assertGreater(calories, 0)
        self.assertLess(calories, 100)  # 合理范围
    
    def test_calories_burned_with_intensity(self):
        """测试不同强度的卡路里"""
        session = TabataSession(rounds=8, work_duration=20, rest_duration=10)
        
        calories_low = TabataCalculator.calories_burned(session, 70, intensity=0.8)
        calories_high = TabataCalculator.calories_burned(session, 70, intensity=1.2)
        
        self.assertLess(calories_low, calories_high)
    
    def test_heart_rate_zones(self):
        """测试心率区间"""
        zones = TabataCalculator.heart_rate_zones(30)
        
        self.assertIn("recovery", zones)
        self.assertIn("aerobic", zones)
        self.assertIn("tempo", zones)
        self.assertIn("threshold", zones)
        self.assertIn("vo2max", zones)
        
        # 30岁最大心率 = 190
        # recovery: 95-114
        self.assertEqual(zones["recovery"][0], 95)
        self.assertEqual(zones["recovery"][1], 114)
    
    def test_recommended_rounds(self):
        """测试推荐轮数"""
        self.assertEqual(TabataCalculator.recommended_rounds("beginner"), 4)
        self.assertEqual(TabataCalculator.recommended_rounds("intermediate"), 6)
        self.assertEqual(TabataCalculator.recommended_rounds("advanced"), 8)
        self.assertEqual(TabataCalculator.recommended_rounds("elite"), 10)
        self.assertEqual(TabataCalculator.recommended_rounds("unknown"), 8)  # 默认
    
    def test_work_rest_ratio(self):
        """测试运动休息比"""
        session = TabataSession(rounds=8, work_duration=20, rest_duration=10)
        ratio = TabataCalculator.work_rest_ratio(session)
        self.assertEqual(ratio, 2.0)
    
    def test_work_rest_ratio_zero_rest(self):
        """测试零休息的比率"""
        session = TabataSession(rounds=8, work_duration=60, rest_duration=0)
        ratio = TabataCalculator.work_rest_ratio(session)
        self.assertEqual(ratio, float('inf'))


class TestTabataTimer(unittest.TestCase):
    """测试 TabataTimer"""
    
    def test_timer_creation(self):
        """测试创建计时器"""
        session = TabataSession(rounds=2, work_duration=5, rest_duration=3, prepare_duration=2)
        timer = TabataTimer(session)
        
        self.assertFalse(timer.is_running)
        self.assertFalse(timer.is_paused)
        self.assertEqual(timer.current_phase, PhaseType.PREPARE)
        self.assertEqual(timer.current_round, 0)
    
    def test_remaining_time_prepare(self):
        """测试准备阶段剩余时间"""
        session = TabataSession(rounds=2, work_duration=5, rest_duration=3, prepare_duration=10)
        timer = TabataTimer(session)
        
        # 准备阶段
        timer._current_phase = PhaseType.PREPARE
        timer._elapsed_in_phase = 3
        self.assertEqual(timer.remaining_time, 7)
    
    def test_remaining_time_work(self):
        """测试运动阶段剩余时间"""
        session = TabataSession(rounds=2, work_duration=20, rest_duration=10)
        timer = TabataTimer(session)
        
        timer._current_phase = PhaseType.WORK
        timer._current_round = 1
        timer._elapsed_in_phase = 10
        self.assertEqual(timer.remaining_time, 10)
    
    def test_remaining_time_rest(self):
        """测试休息阶段剩余时间"""
        session = TabataSession(rounds=2, work_duration=20, rest_duration=10)
        timer = TabataTimer(session)
        
        timer._current_phase = PhaseType.REST
        timer._current_round = 1
        timer._elapsed_in_phase = 5
        self.assertEqual(timer.remaining_time, 5)
    
    def test_total_remaining(self):
        """测试总剩余时间"""
        session = TabataSession(rounds=2, work_duration=5, rest_duration=3, prepare_duration=2)
        timer = TabataTimer(session)
        
        # 准备阶段开始，总剩余 = 准备2 + (运动5 + 休息3) × 2 = 2 + 16 = 18
        timer._current_phase = PhaseType.PREPARE
        timer._current_round = 0
        timer._elapsed_in_phase = 0
        self.assertEqual(timer.total_remaining, 18)
    
    def test_set_callbacks(self):
        """测试设置回调"""
        session = TabataSession(rounds=1, work_duration=1, rest_duration=1)
        timer = TabataTimer(session)
        
        phase_changes: List[Tuple[PhaseType, int]] = []
        ticks: List[Tuple[PhaseType, int, float]] = []
        completions: List[SessionStats] = []
        
        timer.set_callbacks(
            on_phase_change=lambda p, r: phase_changes.append((p, r)),
            on_tick=lambda p, r, t: ticks.append((p, r, t)),
            on_complete=lambda s: completions.append(s)
        )
        
        # 回调已设置，不会报错
        timer._notify_phase_change()
        self.assertEqual(len(phase_changes), 1)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_create_tabata(self):
        """测试快速创建"""
        session = create_tabata()
        self.assertEqual(session.rounds, 8)
        self.assertEqual(session.work_duration, 20)
        
        custom = create_tabata(rounds=4, work=30, rest=15, prepare=5, name="Test")
        self.assertEqual(custom.rounds, 4)
        self.assertEqual(custom.work_duration, 30)
        self.assertEqual(custom.rest_duration, 15)
        self.assertEqual(custom.prepare_duration, 5)
        self.assertEqual(custom.name, "Test")
    
    def test_get_preset(self):
        """测试获取预设"""
        preset = get_preset("Standard Tabata")
        self.assertIsNotNone(preset)
        self.assertEqual(preset.rounds, 8)
        
        not_found = get_preset("Not Found")
        self.assertIsNone(not_found)
    
    def test_list_presets(self):
        """测试列出预设"""
        presets = list_presets()
        self.assertIsInstance(presets, list)
        self.assertIn("Standard Tabata", presets)
        self.assertIn("Double Tabata", presets)
        self.assertIn("Half Tabata", presets)


if __name__ == "__main__":
    unittest.main(verbosity=2)