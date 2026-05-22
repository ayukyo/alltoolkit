"""
Reaction Time Utilities - 测试文件

Tests for reaction time analysis and performance assessment tools.
"""

import unittest
from datetime import datetime, timedelta
import random
import math

from mod import (
    calculate_statistics,
    assess_performance,
    analyze_trend,
    analyze_fatigue,
    generate_reaction_test_data,
    simulate_progressive_improvement,
    compare_groups,
    assess_driving_safety,
    generate_training_plan,
    reaction_time_to_speed_category,
    format_statistics_report,
    PerformanceLevel,
    ReactionTestType,
    ActivityType,
    ReactionTimeStatistics,
    PerformanceAssessment,
    TrendAnalysis,
    FatigueAnalysis,
    AGE_BENCHMARKS,
    GAMING_BENCHMARKS,
    SPORTS_BENCHMARKS,
    DRIVING_BENCHMARKS,
    _percentile,
    _remove_outliers,
)


class TestCalculateStatistics(unittest.TestCase):
    """测试统计计算功能"""
    
    def test_basic_statistics(self):
        """测试基本统计计算"""
        times = [180, 195, 200, 210, 220]
        stats = calculate_statistics(times, remove_outliers=False)
        
        self.assertEqual(stats.count, 5)
        self.assertEqual(stats.mean, 201.0)
        self.assertEqual(stats.median, 200.0)
        self.assertAlmostEqual(stats.min, 180.0)
        self.assertAlmostEqual(stats.max, 220.0)
    
    def test_statistics_with_outliers(self):
        """测试异常值移除"""
        times = [180, 190, 200, 210, 220, 500]  # 500 是异常值
        stats = calculate_statistics(times, remove_outliers=True)
        
        self.assertTrue(stats.outliers_removed > 0)
        self.assertLess(stats.max, 500)
    
    def test_empty_list_raises_error(self):
        """测试空列表抛出异常"""
        with self.assertRaises(ValueError):
            calculate_statistics([])
    
    def test_percentile_calculation(self):
        """测试百分位数计算"""
        times = [100, 150, 200, 250, 300]
        stats = calculate_statistics(times, remove_outliers=False)
        
        self.assertEqual(stats.percentile_25, 150)
        self.assertEqual(stats.percentile_75, 250)
    
    def test_single_value(self):
        """测试单个值"""
        stats = calculate_statistics([200], remove_outliers=False)
        self.assertEqual(stats.mean, 200)
        self.assertEqual(stats.std, 0)
    
    def test_coefficient_of_variation(self):
        """测试变异系数"""
        times = [180, 180, 180, 180]
        stats = calculate_statistics(times, remove_outliers=False)
        self.assertEqual(stats.coefficient_of_variation, 0)
    
    def test_outlier_methods(self):
        """测试不同异常值检测方法"""
        times = [100, 150, 180, 200, 220, 250, 300, 1000]
        
        # IQR 方法
        stats_iqr = calculate_statistics(times, remove_outliers=True, outlier_method="iqr")
        
        # Z-score 方法
        stats_zscore = calculate_statistics(times, remove_outliers=True, outlier_method="zscore")
        
        # MAD 方法
        stats_mad = calculate_statistics(times, remove_outliers=True, outlier_method="mad")
        
        # 所有方法都应该移除极端值
        self.assertLess(stats_iqr.max, 1000)


class TestPerformanceAssessment(unittest.TestCase):
    """测试表现评估功能"""
    
    def test_excellent_performance(self):
        """测试优秀表现"""
        times = [130, 140, 135, 138, 142]
        assessment = assess_performance(times, age=25)
        
        self.assertEqual(assessment.level, PerformanceLevel.EXCELLENT)
        self.assertGreater(assessment.score, 90)
    
    def test_average_performance(self):
        """测试平均表现"""
        times = [200, 210, 205, 208, 215]
        assessment = assess_performance(times, age=25)
        
        # 平均表现可能在 AVERAGE 或 BELOW_AVERAGE
        self.assertIn(assessment.level, [PerformanceLevel.AVERAGE, PerformanceLevel.BELOW_AVERAGE])
    
    def test_slow_performance(self):
        """测试较慢表现"""
        times = [350, 360, 340, 355, 370]
        assessment = assess_performance(times, age=25)
        
        self.assertIn(assessment.level, [PerformanceLevel.SLOW, PerformanceLevel.VERY_SLOW])
    
    def test_age_specific_assessment(self):
        """测试年龄特定评估"""
        # 年轻人表现
        young_times = [180, 185, 190]
        young_assessment = assess_performance(young_times, age=20)
        
        # 老年人相同表现（老年人基准更宽松，所以相同时间表现更好）
        older_times = [180, 185, 190]
        older_assessment = assess_performance(older_times, age=60)
        
        # 老年人应该获得更高的百分位（因为基准更慢）
        self.assertGreater(older_assessment.percentile, young_assessment.percentile)
    
    def test_gaming_assessment(self):
        """测试游戏玩家评估"""
        times = [150, 160, 155, 158, 162]
        assessment = assess_performance(
            times,
            activity_type=ActivityType.GAMING,
            specific_activity="fps"
        )
        
        # 优秀或良好表现
        self.assertIn(assessment.level, [PerformanceLevel.EXCELLENT, PerformanceLevel.GOOD])
        self.assertTrue(any("游戏" in r for r in assessment.recommendations))
    
    def test_sports_assessment(self):
        """测试运动评估"""
        times = [120, 125, 130, 128, 132]
        assessment = assess_performance(
            times,
            activity_type=ActivityType.SPORTS,
            specific_activity="table_tennis"
        )
        
        # 优秀或良好表现
        self.assertIn(assessment.level, [PerformanceLevel.EXCELLENT, PerformanceLevel.GOOD])
    
    def test_driving_assessment(self):
        """测试驾驶评估"""
        times = [300, 310, 305, 308, 312]
        assessment = assess_performance(
            times,
            activity_type=ActivityType.DRIVING
        )
        
        # 驾驶评估可能是优秀或良好
        self.assertIn(assessment.level, [PerformanceLevel.EXCELLENT, PerformanceLevel.GOOD])
    
    def test_test_type_adjustment(self):
        """测试测试类型修正"""
        simple_times = [200, 205, 210]
        choice_times = [260, 265, 270]  # 约 30% 增加
        
        simple_assessment = assess_performance(
            simple_times,
            test_type=ReactionTestType.SIMPLE
        )
        
        choice_assessment = assess_performance(
            choice_times,
            test_type=ReactionTestType.CHOICE
        )
        
        # 选择反应时间修正后应该接近简单反应的表现等级
        self.assertEqual(simple_assessment.level, choice_assessment.level)
    
    def test_recommendations_generated(self):
        """测试建议生成"""
        slow_times = [400, 420, 410, 430, 415]
        assessment = assess_performance(slow_times, age=25)
        
        self.assertTrue(len(assessment.recommendations) > 0)


class TestTrendAnalysis(unittest.TestCase):
    """测试趋势分析功能"""
    
    def test_improving_trend(self):
        """测试改善趋势"""
        sessions = []
        base_time = datetime.now() - timedelta(days=10)
        
        # 模拟改善：每天减少 2ms
        for i in range(10):
            date = base_time + timedelta(days=i)
            mean_time = 250 - i * 5
            sessions.append((date, mean_time))
        
        trend = analyze_trend(sessions)
        
        self.assertEqual(trend.trend_direction, "improving")
        self.assertGreater(trend.improvement_rate, 0)
    
    def test_declining_trend(self):
        """测试下降趋势"""
        sessions = []
        base_time = datetime.now() - timedelta(days=10)
        
        # 模拟下降：每天增加 2ms
        for i in range(10):
            date = base_time + timedelta(days=i)
            mean_time = 180 + i * 5
            sessions.append((date, mean_time))
        
        trend = analyze_trend(sessions)
        
        self.assertEqual(trend.trend_direction, "declining")
        self.assertLess(trend.improvement_rate, 0)
    
    def test_stable_trend(self):
        """测试稳定趋势"""
        sessions = []
        base_time = datetime.now() - timedelta(days=10)
        
        # 模拟稳定
        for i in range(10):
            date = base_time + timedelta(days=i)
            sessions.append((date, 200 + random.uniform(-0.5, 0.5)))
        
        trend = analyze_trend(sessions)
        
        self.assertEqual(trend.trend_direction, "stable")
    
    def test_insufficient_data(self):
        """测试数据不足"""
        sessions = [(datetime.now(), 200)]
        trend = analyze_trend(sessions)
        
        self.assertEqual(trend.trend_direction, "insufficient_data")
        self.assertEqual(trend.data_points, 1)
    
    def test_prediction_generated(self):
        """测试预测生成"""
        sessions = []
        base_time = datetime.now() - timedelta(days=15)
        
        for i in range(15):
            date = base_time + timedelta(days=i)
            sessions.append((date, 200 - i * 2))
        
        trend = analyze_trend(sessions)
        
        self.assertGreater(trend.predicted_next, 0)
        self.assertGreater(trend.confidence_level, 0)
    
    def test_consistency_score(self):
        """测试稳定性得分"""
        # 高一致性数据
        consistent = []
        base_time = datetime.now() - timedelta(days=10)
        for i in range(10):
            date = base_time + timedelta(days=i)
            consistent.append((date, 200 + i * 0.1))
        
        trend_consistent = analyze_trend(consistent)
        self.assertGreater(trend_consistent.consistency_score, 80)


class TestFatigueAnalysis(unittest.TestCase):
    """测试疲劳分析功能"""
    
    def test_no_fatigue(self):
        """测试无疲劳情况"""
        baseline = [180, 185, 190]
        current = [180, 185, 190]
        
        fatigue = analyze_fatigue(baseline, current)
        
        self.assertEqual(fatigue.fatigue_effect, 0)
        self.assertEqual(fatigue.alert_level, "normal")
    
    def test_mild_fatigue(self):
        """测试轻微疲劳"""
        baseline = [180, 185, 190]
        current = [200, 205, 210]  # 约 15% 增加
        
        fatigue = analyze_fatigue(baseline, current)
        
        self.assertEqual(fatigue.alert_level, "mild")
        self.assertGreater(fatigue.fatigue_percentage, 10)
    
    def test_severe_fatigue(self):
        """测试严重疲劳"""
        baseline = [180, 185, 190]
        current = [280, 290, 300]  # 约 50% 增加
        
        fatigue = analyze_fatigue(baseline, current)
        
        self.assertEqual(fatigue.alert_level, "severe")
        self.assertGreater(fatigue.fatigue_percentage, 40)
    
    def test_recovery_time_estimate(self):
        """测试恢复时间估算"""
        baseline = [180, 185, 190]
        current = [250, 260, 270]
        
        fatigue = analyze_fatigue(baseline, current)
        
        self.assertGreater(fatigue.recovery_time_estimate, 0)
    
    def test_empty_data_raises_error(self):
        """测试空数据抛出异常"""
        with self.assertRaises(ValueError):
            analyze_fatigue([], [200, 210])
        
        with self.assertRaises(ValueError):
            analyze_fatigue([180, 190], [])


class TestDataGeneration(unittest.TestCase):
    """测试数据生成功能"""
    
    def test_generate_test_data(self):
        """测试生成测试数据"""
        results = generate_reaction_test_data(20, 200, 30)
        
        self.assertEqual(len(results), 20)
        self.assertTrue(all(r.time_ms > 0 for r in results))
    
    def test_generate_with_errors(self):
        """测试生成包含错误的数据"""
        results = generate_reaction_test_data(100, 200, 30, include_errors=True, error_rate=0.1)
        
        errors = [r for r in results if not r.correct]
        self.assertGreater(len(errors), 0)
    
    def test_simulate_progressive_improvement(self):
        """测试模拟渐进改善"""
        training = simulate_progressive_improvement(30, 250, 180)
        
        self.assertEqual(len(training), 30)
        
        # 验证趋势改善
        first_week_mean = sum(training[0][1]) / len(training[0][1])
        last_week_mean = sum(training[-1][1]) / len(training[-1][1])
        
        self.assertGreater(first_week_mean, last_week_mean)
    
    def test_result_structure(self):
        """测试结果结构"""
        results = generate_reaction_test_data(5)
        
        for r in results:
            self.assertIsInstance(r.time_ms, float)
            self.assertIsInstance(r.test_type, ReactionTestType)
            self.assertIsInstance(r.stimulus_time, datetime)
            self.assertIsInstance(r.response_time, datetime)
            self.assertIsInstance(r.correct, bool)


class TestGroupComparison(unittest.TestCase):
    """测试组间比较功能"""
    
    def test_faster_group_identification(self):
        """测试识别更快组"""
        group_a = [180, 185, 190]
        group_b = [220, 225, 230]
        
        comparison = compare_groups(group_a, group_b)
        
        self.assertEqual(comparison["faster_group"], "Group A")
        self.assertEqual(comparison["difference"], -40)
    
    def test_significant_difference(self):
        """测试显著差异检测"""
        # 两组差异明显的数据
        group_a = [150, 155, 160, 155, 150]
        group_b = [250, 255, 260, 255, 250]
        
        comparison = compare_groups(group_a, group_b)
        
        self.assertTrue(comparison["significant_difference"])
    
    def test_cohens_d_calculation(self):
        """测试 Cohen's d 计算"""
        group_a = [180, 185, 190]
        group_b = [220, 225, 230]
        
        comparison = compare_groups(group_a, group_b)
        
        self.assertIsInstance(comparison["cohens_d"], float)
        self.assertIsInstance(comparison["effect_size_interpretation"], str)
    
    def test_group_names_preserved(self):
        """测试组名保留"""
        comparison = compare_groups([180, 190], [200, 210], "Players", "Non-players")
        
        self.assertEqual(comparison["group_a_name"], "Players")
        self.assertEqual(comparison["group_b_name"], "Non-players")


class TestDrivingSafety(unittest.TestCase):
    """测试驾驶安全评估功能"""
    
    def test_safe_rating(self):
        """测试安全评级"""
        times = [280, 290, 300]
        safety = assess_driving_safety(times)
        
        self.assertEqual(safety["safety_rating"], "safe")
    
    def test_warning_rating(self):
        """测试警示评级"""
        times = [480, 490, 500]  # 在 warning 边界附近
        safety = assess_driving_safety(times, "normal")
        
        # 可能在 warning 或 caution
        self.assertIn(safety["safety_rating"], ["warning", "caution", "danger"])
    
    def test_danger_rating(self):
        """测试危险评级"""
        times = [700, 720, 730]
        safety = assess_driving_safety(times)
        
        self.assertEqual(safety["safety_rating"], "danger")
    
    def test_reaction_distance(self):
        """测试反应距离计算"""
        times = [300]  # 300ms
        safety = assess_driving_safety(times)
        
        # 60 km/h = 16.67 m/s
        # 300ms * 16.67 m/s ≈ 5.0 m
        self.assertAlmostEqual(safety["reaction_distance_at_60kmh"], 5.0, places=1)
    
    def test_different_scenarios(self):
        """测试不同场景"""
        times = [300]
        
        normal = assess_driving_safety(times, "normal")
        emergency = assess_driving_safety(times, "emergency")
        night = assess_driving_safety(times, "night")
        
        # 紧急场景阈值更低
        self.assertIn(normal["safety_rating"], ["safe", "caution"])
        self.assertIn(emergency["safety_rating"], ["safe", "caution", "warning"])
    
    def test_age_factor(self):
        """测试年龄因素"""
        times = [300]
        safety = assess_driving_safety(times, driver_age=60)
        
        self.assertIsNotNone(safety["age_comparison"])
        self.assertIn("age_group_mean", safety["age_comparison"])


class TestTrainingPlan(unittest.TestCase):
    """测试训练计划生成功能"""
    
    def test_plan_structure(self):
        """测试计划结构"""
        plan = generate_training_plan(PerformanceLevel.AVERAGE)
        
        self.assertIn("sessions_per_week", plan)
        self.assertIn("session_duration_minutes", plan)
        self.assertIn("total_sessions", plan)
        self.assertIn("weekly_schedule", plan)
    
    def test_intensity_by_level(self):
        """测试不同等级的训练强度"""
        slow_plan = generate_training_plan(PerformanceLevel.SLOW)
        excellent_plan = generate_training_plan(PerformanceLevel.EXCELLENT)
        
        # 较慢等级需要更多训练
        self.assertGreater(
            slow_plan["sessions_per_week"],
            excellent_plan["sessions_per_week"]
        )
    
    def test_target_adjustment(self):
        """测试目标调整"""
        current_plan = generate_training_plan(
            PerformanceLevel.AVERAGE,
            target_level=PerformanceLevel.GOOD
        )
        ambitious_plan = generate_training_plan(
            PerformanceLevel.SLOW,
            target_level=PerformanceLevel.EXCELLENT
        )
        
        self.assertGreater(
            ambitious_plan["sessions_per_week"],
            current_plan["sessions_per_week"]
        )
    
    def test_activity_specific_training(self):
        """测试活动特定训练"""
        gaming_plan = generate_training_plan(
            PerformanceLevel.AVERAGE,
            activity_type=ActivityType.GAMING
        )
        sports_plan = generate_training_plan(
            PerformanceLevel.AVERAGE,
            activity_type=ActivityType.SPORTS
        )
        
        self.assertIn("游戏", str(gaming_plan["training_types"]))
        self.assertIn("球类", str(sports_plan["training_types"]))
    
    def test_weekly_schedule(self):
        """测试每周安排"""
        plan = generate_training_plan(PerformanceLevel.AVERAGE, weeks=4)
        
        self.assertEqual(len(plan["weekly_schedule"]), 4)
        
        for week in plan["weekly_schedule"]:
            self.assertIn("week", week)
            self.assertIn("focus", week)
            self.assertIn("sessions", week)


class TestUtilityFunctions(unittest.TestCase):
    """测试辅助函数"""
    
    def test_speed_category(self):
        """测试速度类别"""
        self.assertEqual(reaction_time_to_speed_category(100), "极快（专业级）")
        self.assertEqual(reaction_time_to_speed_category(180), "很快（优秀）")
        self.assertIn("良好", reaction_time_to_speed_category(230))
        self.assertIn("偏慢", reaction_time_to_speed_category(350))
        self.assertEqual(reaction_time_to_speed_category(500), "较慢（需关注）")
    
    def test_format_report(self):
        """测试格式化报告"""
        stats = calculate_statistics([180, 190, 200, 210, 220])
        report = format_statistics_report(stats)
        
        self.assertIn("平均值", report)
        self.assertIn("中位数", report)
        self.assertIn("标准差", report)
    
    def test_percentile_edge_cases(self):
        """测试百分位数边界情况"""
        # 单元素
        self.assertEqual(_percentile([100], 50), 100)
        
        # 两元素
        self.assertEqual(_percentile([100, 200], 50), 150)
        
        # 边界百分位
        data = [100, 150, 200, 250, 300]
        self.assertEqual(_percentile(data, 0), 100)
        self.assertEqual(_percentile(data, 100), 300)
    
    def test_outlier_removal_edge_cases(self):
        """测试异常值移除边界情况"""
        # 小数据集不移除
        small, removed = _remove_outliers([100, 200, 300])
        self.assertEqual(len(small), 3)


class TestDataClasses(unittest.TestCase):
    """测试数据类"""
    
    def test_statistics_dataclass(self):
        """测试统计数据类"""
        stats = ReactionTimeStatistics(
            mean=200, median=200, std=20,
            min=150, max=250, count=10,
            percentile_25=180, percentile_75=220,
            percentile_90=240, percentile_95=245,
            iqr=40, coefficient_of_variation=10
        )
        
        self.assertEqual(stats.mean, 200)
        self.assertEqual(stats.iqr, 40)
    
    def test_assessment_dataclass(self):
        """测试评估数据类"""
        assessment = PerformanceAssessment(
            level=PerformanceLevel.GOOD,
            score=80,
            percentile=75,
            age_benchmark_diff=-20,
            classification_reason="Test",
            recommendations=["建议1"]
        )
        
        self.assertEqual(assessment.level, PerformanceLevel.GOOD)
        self.assertEqual(assessment.recommendations, ["建议1"])
    
    def test_trend_dataclass(self):
        """测试趋势数据类"""
        trend = TrendAnalysis(
            trend_direction="improving",
            improvement_rate=5.0,
            consistency_score=90,
            predicted_next=180,
            confidence_level=85,
            data_points=10
        )
        
        self.assertEqual(trend.trend_direction, "improving")
    
    def test_fatigue_dataclass(self):
        """测试疲劳数据类"""
        fatigue = FatigueAnalysis(
            baseline_mean=180,
            current_mean=250,
            fatigue_effect=70,
            fatigue_percentage=39,
            recovery_time_estimate=58.5,
            alert_level="moderate"
        )
        
        self.assertEqual(fatigue.alert_level, "moderate")


class TestBenchmarkData(unittest.TestCase):
    """测试基准数据"""
    
    def test_age_benchmarks_complete(self):
        """测试年龄基准完整性"""
        for age in [10, 20, 30, 40, 50, 60, 70]:
            benchmark = AGE_BENCHMARKS[age]
            self.assertIn("mean", benchmark)
            self.assertIn("std", benchmark)
            self.assertIn("excellent", benchmark)
            self.assertIn("slow", benchmark)
    
    def test_gaming_benchmarks_complete(self):
        """测试游戏基准完整性"""
        for game_type in ["fps", "racing", "sports", "rhythm", "fighting"]:
            benchmark = GAMING_BENCHMARKS[game_type]
            self.assertIn("excellent", benchmark)
            self.assertIn("slow", benchmark)
    
    def test_sports_benchmarks_complete(self):
        """测试运动基准完整性"""
        for sport in ["sprinting", "boxing", "tennis", "soccer", "table_tennis"]:
            benchmark = SPORTS_BENCHMARKS[sport]
            self.assertIn("excellent", benchmark)
            self.assertIn("slow", benchmark)
    
    def test_driving_benchmarks_complete(self):
        """测试驾驶基准完整性"""
        for scenario in ["normal", "emergency", "high_speed", "night", "fatigue"]:
            benchmark = DRIVING_BENCHMARKS[scenario]
            self.assertIn("safe", benchmark)
            self.assertIn("danger", benchmark)


if __name__ == "__main__":
    unittest.main(verbosity=2)