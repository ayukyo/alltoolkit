#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Stress Utilities Test Suite
=========================================
Comprehensive tests for the stress_utils module.

Author: AllToolkit Contributors
License: MIT
"""

import unittest
import sys
import os

# Add module path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stress_utils.mod import (
    calculate_stress_index,
    get_stress_level,
    get_stress_level_info,
    get_relief_recommendations,
    get_dominant_stress_factors,
    perform_full_assessment,
    calculate_burnout_risk_simple,
    calculate_pss_score,
    interpret_pss_score,
    perform_pss_test,
    quick_stress_check,
    analyze_quick_check_breakdown,
    StressHistory,
    analyze_stress_trend,
    assess_burnout,
    suggest_relief_activities,
    get_stress_summary,
    calculate_stress_reduction_potential,
    get_pss_questions,
    format_assessment_report,
    StressLevel,
    StressType,
    ReliefCategory,
)


class TestStressIndexCalculation(unittest.TestCase):
    """压力指数计算测试"""
    
    def test_calculate_stress_index_basic(self):
        """测试基础压力指数计算"""
        # 正常范围 - 加权计算: (50*0.25 + 40*0.20 + 30*0.20 + 45*0.25 + 25*0.10) / 1.0
        index = calculate_stress_index(50, 40, 30, 45, 25)
        self.assertAlmostEqual(index, 40.25, places=1)
        
        # 高压力 - 计算: (80*0.25 + 70*0.20 + 60*0.20 + 75*0.25 + 50*0.10) = 20+14+12+18.75+5 = 69.75
        index = calculate_stress_index(80, 70, 60, 75, 50)
        self.assertAlmostEqual(index, 69.75, places=1)
        
        # 低压力
        index = calculate_stress_index(20, 15, 10, 20, 5)
        self.assertAlmostEqual(index, 15.5, places=1)
    
    def test_calculate_stress_index_custom_weights(self):
        """测试自定义权重"""
        custom_weights = {
            'work': 0.5,
            'life': 0.1,
            'health': 0.1,
            'psychological': 0.2,
            'environment': 0.1,
        }
        # 总权重 = 1.0, 计算: (80*0.5 + 20*0.1 + 20*0.1 + 30*0.2 + 20*0.1) = 40+2+2+6+2 = 52
        index = calculate_stress_index(80, 20, 20, 30, 20, custom_weights)
        self.assertAlmostEqual(index, 52.0, places=1)
    
    def test_calculate_stress_index_edge_cases(self):
        """测试边界情况"""
        # 全零
        index = calculate_stress_index(0, 0, 0, 0, 0)
        self.assertEqual(index, 0.0)
        
        # 全满分
        index = calculate_stress_index(100, 100, 100, 100, 100)
        self.assertEqual(index, 100.0)
    
    def test_calculate_stress_index_invalid_inputs(self):
        """测试无效输入"""
        # 超范围值
        with self.assertRaises(ValueError):
            calculate_stress_index(150, 40, 30, 50, 25)
        
        with self.assertRaises(ValueError):
            calculate_stress_index(-10, 40, 30, 50, 25)


class TestStressLevelClassification(unittest.TestCase):
    """压力等级分类测试"""
    
    def test_get_stress_level(self):
        """测试压力等级获取"""
        self.assertEqual(get_stress_level(10), 'very_low')
        self.assertEqual(get_stress_level(30), 'low')
        self.assertEqual(get_stress_level(50), 'moderate')
        self.assertEqual(get_stress_level(70), 'high')
        self.assertEqual(get_stress_level(90), 'very_high')
    
    def test_get_stress_level_boundary(self):
        """测试边界值"""
        self.assertEqual(get_stress_level(19.9), 'very_low')
        self.assertEqual(get_stress_level(20.0), 'low')
        self.assertEqual(get_stress_level(39.9), 'low')
        self.assertEqual(get_stress_level(40.0), 'moderate')
        self.assertEqual(get_stress_level(59.9), 'moderate')
        self.assertEqual(get_stress_level(60.0), 'high')
        self.assertEqual(get_stress_level(79.9), 'high')
        self.assertEqual(get_stress_level(80.0), 'very_high')
    
    def test_get_stress_level_info(self):
        """测试等级详细信息"""
        level, label, label_en, desc, action = get_stress_level_info(50)
        self.assertEqual(level, 'moderate')
        self.assertEqual(label, '中等')
        self.assertEqual(label_en, 'Moderate')
        self.assertIn('压力', desc)
        self.assertIn('建议', action)
    
    def test_get_stress_level_info_extreme(self):
        """测试极端等级"""
        level, label, label_en, desc, action = get_stress_level_info(95)
        self.assertEqual(level, 'very_high')
        self.assertIn('严重', desc)
        self.assertIn('专业', action)


class TestReliefRecommendations(unittest.TestCase):
    """缓解建议测试"""
    
    def test_get_relief_recommendations_basic(self):
        """测试基本建议获取"""
        recs = get_relief_recommendations('moderate')
        self.assertGreater(len(recs), 0)
        self.assertIn('放松', recs[0])
    
    def test_get_relief_recommendations_by_level(self):
        """测试不同等级的建议"""
        very_low_recs = get_relief_recommendations('very_low')
        very_high_recs = get_relief_recommendations('very_high')
        
        # 高压力应有更多专业建议
        self.assertIn('专业', ' '.join(very_high_recs))
        self.assertNotIn('专业', ' '.join(very_low_recs))


class TestDominantStressFactors(unittest.TestCase):
    """主要压力因素测试"""
    
    def test_get_dominant_stress_factors(self):
        """测试主要因素识别"""
        factors = get_dominant_stress_factors(70, 30, 40, 60, 20)
        self.assertIn('工作压力', factors)
        self.assertIn('心理压力', factors)
        self.assertNotIn('生活压力', factors)
    
    def test_get_dominant_stress_factors_all_low(self):
        """测试全部低压力"""
        factors = get_dominant_stress_factors(30, 20, 25, 30, 15)
        self.assertEqual(factors, ['综合因素'])
    
    def test_get_dominant_stress_factors_custom_threshold(self):
        """测试自定义阈值"""
        factors = get_dominant_stress_factors(45, 40, 38, 42, 30, threshold=40)
        self.assertIn('工作压力', factors)
        self.assertIn('生活压力', factors)


class TestFullAssessment(unittest.TestCase):
    """完整评估测试"""
    
    def test_perform_full_assessment(self):
        """测试完整评估"""
        result = perform_full_assessment(65, 40, 35, 55, 25)
        
        self.assertGreater(result.stress_index, 0)
        self.assertLess(result.stress_index, 100)
        self.assertEqual(result.level, 'moderate')
        self.assertEqual(result.level_label, '中等')
        self.assertGreater(len(result.recommendations), 0)
        self.assertIsNotNone(result.timestamp)
    
    def test_perform_full_assessment_high_stress(self):
        """测试高压力评估"""
        result = perform_full_assessment(85, 80, 70, 85, 60)
        
        self.assertGreater(result.stress_index, 70)
        self.assertIn('high', result.level)
        self.assertGreater(result.burnout_risk, 0.6)
    
    def test_assessment_factor_breakdown(self):
        """测试因素分解"""
        result = perform_full_assessment(60, 40, 30, 50, 20)
        
        self.assertIn('work', result.factor_breakdown)
        self.assertEqual(result.factor_breakdown['work'], 60)
        self.assertEqual(result.factor_breakdown['life'], 40)


class TestBurnoutRisk(unittest.TestCase):
    """燃尽风险测试"""
    
    def test_calculate_burnout_risk_simple(self):
        """测试简化燃尽风险计算"""
        risk = calculate_burnout_risk_simple(70, 65, 80)
        self.assertGreater(risk, 0.6)
        self.assertLess(risk, 1.0)
    
    def test_calculate_burnout_risk_low(self):
        """测试低燃尽风险"""
        risk = calculate_burnout_risk_simple(30, 25, 30)
        self.assertLess(risk, 0.4)
    
    def test_calculate_burnout_risk_max(self):
        """测试最大燃尽风险"""
        risk = calculate_burnout_risk_simple(100, 100, 100)
        self.assertEqual(risk, 1.0)


class TestPSS10(unittest.TestCase):
    """PSS-10 测试测试"""
    
    def test_calculate_pss_score(self):
        """测试 PSS 分数计算"""
        responses = {
            'q1': 3, 'q2': 2, 'q3': 3, 'q4': 1, 'q5': 2,
            'q6': 3, 'q7': 1, 'q8': 2, 'q9': 3, 'q10': 2
        }
        score = calculate_pss_score(responses)
        self.assertGreater(score, 0)
        self.assertLess(score, 40)
    
    def test_calculate_pss_score_reverse_scoring(self):
        """测试反向计分"""
        # 全选0，正向题0分，反向题4分
        responses = {f'q{i}': 0 for i in range(1, 11)}
        score = calculate_pss_score(responses)
        # q4, q5, q7 是反向题，应得 4 分
        self.assertEqual(score, 12)  # 3 * 4 = 12
    
    def test_calculate_pss_score_max(self):
        """测试最高压力分数（正向题全选4，反向题全选0）"""
        # 正向题选4（q1,q2,q3,q6,q8,q9,q10），反向题选0（q4,q5,q7）
        responses = {
            'q1': 4, 'q2': 4, 'q3': 4, 'q6': 4, 'q8': 4, 'q9': 4, 'q10': 4,  # 正向题
            'q4': 0, 'q5': 0, 'q7': 0,  # 反向题（选0时反向计分得4分）
        }
        score = calculate_pss_score(responses)
        self.assertEqual(score, 40)  # 7×4 + 3×4 = 40
    
    def test_calculate_pss_score_invalid_question(self):
        """测试无效问题ID"""
        with self.assertRaises(ValueError):
            calculate_pss_score({'q1': 3, 'q11': 2})
    
    def test_calculate_pss_score_invalid_response(self):
        """测试无效响应值"""
        with self.assertRaises(ValueError):
            calculate_pss_score({'q1': 5})
    
    def test_interpret_pss_score(self):
        """测试 PSS 分数解释"""
        level, interp, percentile = interpret_pss_score(15)
        self.assertEqual(level, 'moderate')
        self.assertGreater(percentile, 30)
        self.assertLess(percentile, 70)
    
    def test_interpret_pss_score_low(self):
        """测试低压力解释"""
        level, interp, percentile = interpret_pss_score(8)
        self.assertEqual(level, 'low')
        self.assertLess(percentile, 30)
    
    def test_interpret_pss_score_high(self):
        """测试高压力解释"""
        level, interp, percentile = interpret_pss_score(32)
        self.assertEqual(level, 'high')
        self.assertGreater(percentile, 70)
    
    def test_perform_pss_test(self):
        """测试完整 PSS 测试"""
        responses = {
            'q1': 2, 'q2': 2, 'q3': 2, 'q4': 2, 'q5': 2,
            'q6': 2, 'q7': 2, 'q8': 2, 'q9': 2, 'q10': 2
        }
        result = perform_pss_test(responses)
        
        self.assertEqual(result.total_score, 20)
        self.assertEqual(result.stress_level, 'moderate')
        self.assertGreater(len(result.recommendations), 0)


class TestQuickStressCheck(unittest.TestCase):
    """快速压力检查测试"""
    
    def test_quick_stress_check_basic(self):
        """测试基本快速检查"""
        index = quick_stress_check(8, 7, 7, 3, 8)
        self.assertLess(index, 40)  # 应为低压力
    
    def test_quick_stress_check_high(self):
        """测试高压力快速检查"""
        index = quick_stress_check(3, 4, 3, 9, 2)
        self.assertGreater(index, 60)  # 应为高压力
    
    def test_quick_stress_check_invalid(self):
        """测试无效输入"""
        with self.assertRaises(ValueError):
            quick_stress_check(0, 5, 5, 5, 5)
        
        with self.assertRaises(ValueError):
            quick_stress_check(11, 5, 5, 5, 5)
    
    def test_analyze_quick_check_breakdown(self):
        """测试快速检查分解"""
        breakdown = analyze_quick_check_breakdown(6, 5, 4, 7, 3)
        
        self.assertEqual(breakdown['sleep'], 40)
        self.assertEqual(breakdown['energy'], 50)
        self.assertEqual(breakdown['mood'], 60)
        self.assertEqual(breakdown['workload'], 70)
        self.assertEqual(breakdown['social'], 70)


class TestStressHistory(unittest.TestCase):
    """压力历史测试"""
    
    def test_stress_history_add_entry(self):
        """测试添加历史记录"""
        history = StressHistory()
        history.add_entry(45.5)
        
        self.assertEqual(len(history.get_entries()), 1)
        self.assertEqual(history.get_entries()[0].stress_index, 45.5)
    
    def test_stress_history_multiple_entries(self):
        """测试多条记录"""
        history = StressHistory()
        for i in range(5):
            history.add_entry(30 + i * 10)
        
        entries = history.get_entries()
        self.assertEqual(len(entries), 5)
    
    def test_stress_history_limit(self):
        """测试记录限制"""
        history = StressHistory()
        for i in range(10):
            history.add_entry(i)
        
        entries = history.get_entries(limit=3)
        self.assertEqual(len(entries), 3)
    
    def test_stress_history_json(self):
        """测试 JSON 导出导入"""
        history = StressHistory()
        history.add_entry(45, notes='test')
        
        json_str = history.to_json()
        
        new_history = StressHistory()
        new_history.from_json(json_str)
        
        self.assertEqual(len(new_history.get_entries()), 1)
        self.assertEqual(new_history.get_entries()[0].stress_index, 45)


class TestStressTrend(unittest.TestCase):
    """压力趋势测试"""
    
    def test_analyze_stress_trend_increasing(self):
        """测试上升趋势"""
        history = StressHistory()
        for i in range(5):
            history.add_entry(30 + i * 10)
        
        trend = analyze_stress_trend(history)
        
        self.assertEqual(trend.trend_direction, 'increasing')
        self.assertGreater(trend.trend_percentage, 0)
    
    def test_analyze_stress_trend_decreasing(self):
        """测试下降趋势"""
        history = StressHistory()
        for i in range(5):
            history.add_entry(70 - i * 10)
        
        trend = analyze_stress_trend(history)
        
        self.assertEqual(trend.trend_direction, 'decreasing')
        self.assertGreater(trend.trend_percentage, 0)
    
    def test_analyze_stress_trend_stable(self):
        """测试稳定趋势"""
        history = StressHistory()
        for i in range(5):
            history.add_entry(50 + (i % 3) * 2)
        
        trend = analyze_stress_trend(history)
        
        self.assertEqual(trend.trend_direction, 'stable')
    
    def test_analyze_stress_trend_single_entry(self):
        """测试单条记录"""
        history = StressHistory()
        history.add_entry(50)
        
        trend = analyze_stress_trend(history)
        
        self.assertEqual(trend.current_index, 50)
        self.assertEqual(trend.entries_count, 1)


class TestBurnoutAssessment(unittest.TestCase):
    """燃尽评估测试"""
    
    def test_assess_burnout_low(self):
        """测试低燃尽风险"""
        burnout = assess_burnout([1, 1, 1, 1, 1], [0, 0, 0], [0, 0, 0, 0, 0, 0, 0])
        
        self.assertLess(burnout.overall_risk, 0.3)
        self.assertEqual(burnout.risk_level, 'low')
    
    def test_assess_burnout_high(self):
        """测试高燃尽风险"""
        burnout = assess_burnout([5, 5, 5, 5, 5], [5, 5, 5], [5, 5, 5, 5, 5, 5, 5])
        
        self.assertGreater(burnout.overall_risk, 0.7)
        self.assertEqual(burnout.risk_level, 'critical')
    
    def test_assess_burnout_warning_signs(self):
        """测试警告信号"""
        burnout = assess_burnout([5, 5, 5], [4, 4], [3, 3])
        
        self.assertGreater(len(burnout.warning_signs), 0)
    
    def test_assess_burnout_interventions(self):
        """测试干预建议"""
        burnout = assess_burnout([5, 5, 5, 5, 5], [4, 4, 4], [4, 4, 4, 4])
        
        self.assertGreater(len(burnout.interventions), 0)


class TestReliefActivities(unittest.TestCase):
    """缓解活动测试"""
    
    def test_suggest_relief_activities_basic(self):
        """测试基本活动建议"""
        activities = suggest_relief_activities('moderate', 20)
        
        self.assertGreater(len(activities), 0)
        self.assertIn('name', activities[0])
        self.assertIn('duration', activities[0])
    
    def test_suggest_relief_activities_high_stress(self):
        """测试高压力活动建议"""
        activities = suggest_relief_activities('high', 30)
        
        # 应包含高强度活动
        high_effect_count = sum(1 for a in activities if a.get('effect') == 'high')
        self.assertGreater(high_effect_count, 0)
    
    def test_suggest_relief_activities_short_time(self):
        """测试短时间建议"""
        activities = suggest_relief_activities('moderate', 5)
        
        # 只应有短时活动
        for activity in activities:
            duration = activity['duration']
            min_time = int(duration.split('-')[0])
            self.assertLessEqual(min_time, 5)
    
    def test_suggest_relief_activities_preferences(self):
        """测试偏好活动"""
        activities = suggest_relief_activities('moderate', 30, ['physical'])
        
        # 应优先推荐运动类活动
        physical_count = sum(1 for a in activities if a.get('category') == 'physical')
        self.assertGreater(physical_count, 0)


class TestUtilityFunctions(unittest.TestCase):
    """辅助函数测试"""
    
    def test_get_stress_summary(self):
        """测试压力概要"""
        summary = get_stress_summary(45.0)
        self.assertIn('45.0', summary)
        self.assertIn('中等', summary)
    
    def test_calculate_stress_reduction_potential(self):
        """测试压力缓解潜力"""
        potential = calculate_stress_reduction_potential(70, [
            {'effect': 'high'},
            {'effect': 'medium'}
        ])
        
        self.assertGreater(potential, 0)
    
    def test_get_pss_questions(self):
        """测试 PSS 问题获取"""
        questions = get_pss_questions()
        
        self.assertEqual(len(questions), 10)
    
    def test_format_assessment_report(self):
        """测试报告格式化"""
        result = perform_full_assessment(60, 40, 30, 50, 20)
        report = format_assessment_report(result)
        
        self.assertIn('压力评估报告', report)
        self.assertIn('压力指数', report)
        self.assertIn('缓解建议', report)


class TestEnums(unittest.TestCase):
    """枚举测试"""
    
    def test_stress_level_enum(self):
        """测试压力等级枚举"""
        self.assertEqual(StressLevel.VERY_LOW.value, 'very_low')
        self.assertEqual(StressLevel.HIGH.value, 'high')
    
    def test_stress_type_enum(self):
        """测试压力类型枚举"""
        self.assertEqual(StressType.WORK.value, 'work')
        self.assertEqual(StressType.PSYCHOLOGICAL.value, 'psychological')
    
    def test_relief_category_enum(self):
        """测试缓解类别枚举"""
        self.assertEqual(ReliefCategory.PHYSICAL.value, 'physical')
        self.assertEqual(ReliefCategory.PROFESSIONAL.value, 'professional')


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)