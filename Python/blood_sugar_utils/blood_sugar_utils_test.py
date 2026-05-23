"""
Blood Sugar Utils 测试文件

测试血糖工具的所有功能。
"""

import unittest
from datetime import datetime, timedelta
from mod import (
    GlucoseUnit, GlucoseStatus,
    convert_glucose, assess_glucose,
    hba1c_to_average_glucose, average_glucose_to_hba1c,
    estimate_average_glucose, analyze_glucose_trend,
    calculate_insulin_sensitivity, carbohydrate_to_insulin,
    glucose_report,
    mgdl_to_mmol, mmol_to_mgdl
)


class TestGlucoseConversion(unittest.TestCase):
    """测试血糖单位转换"""
    
    def test_mgdl_to_mmol(self):
        """测试 mg/dL 转 mmol/L"""
        result = convert_glucose(100, GlucoseUnit.MG_DL, GlucoseUnit.MMOL_L)
        self.assertAlmostEqual(result, 5.55, places=2)
        
        result = convert_glucose(140, GlucoseUnit.MG_DL, GlucoseUnit.MMOL_L)
        self.assertAlmostEqual(result, 7.77, places=2)
    
    def test_mmol_to_mgdl(self):
        """测试 mmol/L 转 mg/dL"""
        result = convert_glucose(5.5, GlucoseUnit.MMOL_L, GlucoseUnit.MG_DL)
        self.assertAlmostEqual(result, 99.1, places=1)
        
        result = convert_glucose(7.8, GlucoseUnit.MMOL_L, GlucoseUnit.MG_DL)
        self.assertAlmostEqual(result, 140.5, places=1)
    
    def test_same_unit_conversion(self):
        """测试同单位转换"""
        result = convert_glucose(100, GlucoseUnit.MG_DL, GlucoseUnit.MG_DL)
        self.assertEqual(result, 100)
        
        result = convert_glucose(5.5, GlucoseUnit.MMOL_L, GlucoseUnit.MMOL_L)
        self.assertEqual(result, 5.5)
    
    def test_convenience_functions(self):
        """测试便捷函数"""
        result = mgdl_to_mmol(100)
        self.assertAlmostEqual(result, 5.55, places=2)
        
        result = mmol_to_mgdl(5.5)
        self.assertAlmostEqual(result, 99.1, places=1)
    
    def test_edge_cases(self):
        """测试边界值"""
        # 低血糖值
        result = convert_glucose(50, GlucoseUnit.MG_DL, GlucoseUnit.MMOL_L)
        self.assertAlmostEqual(result, 2.77, places=1)
        
        # 高血糖值
        result = convert_glucose(300, GlucoseUnit.MG_DL, GlucoseUnit.MMOL_L)
        self.assertAlmostEqual(result, 16.65, places=1)


class TestGlucoseAssessment(unittest.TestCase):
    """测试血糖评估"""
    
    def test_normal_fasting(self):
        """测试正常空腹血糖"""
        result = assess_glucose(5.5, GlucoseUnit.MMOL_L, fasting=True)
        self.assertEqual(result['status'], GlucoseStatus.NORMAL_FASTING.value)
        self.assertEqual(result['risk_level'], 'low')
    
    def test_hypoglycemia(self):
        """测试低血糖"""
        result = assess_glucose(3.5, GlucoseUnit.MMOL_L, fasting=True)
        self.assertEqual(result['status'], GlucoseStatus.HYPOGLYCEMIA.value)
        self.assertEqual(result['risk_level'], 'high')
    
    def test_severe_hypoglycemia(self):
        """测试严重低血糖"""
        result = assess_glucose(2.5, GlucoseUnit.MMOL_L, fasting=True)
        self.assertEqual(result['status'], GlucoseStatus.SEVERE_HYPOGLYCEMIA.value)
        self.assertEqual(result['risk_level'], 'critical')
    
    def test_prediabetes_fasting(self):
        """测试糖尿病前期空腹血糖"""
        result = assess_glucose(6.0, GlucoseUnit.MMOL_L, fasting=True)
        self.assertEqual(result['status'], GlucoseStatus.PREDIABETES_FASTING.value)
        self.assertEqual(result['risk_level'], 'medium')
    
    def test_diabetes_fasting(self):
        """测试糖尿病空腹血糖"""
        result = assess_glucose(7.5, GlucoseUnit.MMOL_L, fasting=True)
        self.assertEqual(result['status'], GlucoseStatus.DIABETES_FASTING.value)
        self.assertEqual(result['risk_level'], 'high')
    
    def test_normal_post_meal(self):
        """测试正常餐后血糖"""
        result = assess_glucose(7.0, GlucoseUnit.MMOL_L, fasting=False)
        self.assertEqual(result['status'], GlucoseStatus.NORMAL_POST_MEAL.value)
        self.assertEqual(result['risk_level'], 'low')
    
    def test_prediabetes_post_meal(self):
        """测试糖尿病前期餐后血糖"""
        result = assess_glucose(9.0, GlucoseUnit.MMOL_L, fasting=False)
        self.assertEqual(result['status'], GlucoseStatus.PREDIABETES_POST_MEAL.value)
        self.assertEqual(result['risk_level'], 'medium')
    
    def test_diabetes_post_meal(self):
        """测试糖尿病餐后血糖"""
        result = assess_glucose(12.0, GlucoseUnit.MMOL_L, fasting=False)
        self.assertEqual(result['status'], GlucoseStatus.DIABETES_POST_MEAL.value)
        self.assertEqual(result['risk_level'], 'high')
    
    def test_mgdl_assessment(self):
        """测试 mg/dL 单位评估"""
        result = assess_glucose(100, GlucoseUnit.MG_DL, fasting=True)
        self.assertEqual(result['status'], GlucoseStatus.NORMAL_FASTING.value)
    
    def test_age_adjusted_assessment(self):
        """测试年龄调整评估"""
        # 老年人标准稍宽
        result = assess_glucose(6.0, GlucoseUnit.MMOL_L, fasting=True, age=70)
        self.assertEqual(result['status'], GlucoseStatus.NORMAL_FASTING.value)
        self.assertTrue(result['age_adjusted'])


class TestHbA1cConversion(unittest.TestCase):
    """测试糖化血红蛋白转换"""
    
    def test_hba1c_to_average_glucose(self):
        """测试 HbA1c 转平均血糖"""
        result = hba1c_to_average_glucose(6.5)
        self.assertAlmostEqual(result['avg_glucose_mmol'], 7.73, places=1)
        self.assertEqual(result['status'], '糖尿病（控制尚可）')
    
    def test_hba1c_normal(self):
        """测试正常 HbA1c"""
        result = hba1c_to_average_glucose(5.5)
        self.assertEqual(result['status'], '正常')
        self.assertEqual(result['risk'], 'low')
    
    def test_hba1c_prediabetes(self):
        """测试糖尿病前期 HbA1c"""
        result = hba1c_to_average_glucose(6.0)
        self.assertEqual(result['status'], '糖尿病前期')
        self.assertEqual(result['risk'], 'medium')
    
    def test_hba1c_poor_control(self):
        """测试控制不佳的 HbA1c"""
        result = hba1c_to_average_glucose(8.5)
        self.assertEqual(result['status'], '糖尿病（控制很差）')
        self.assertEqual(result['risk'], 'critical')
    
    def test_average_glucose_to_hba1c(self):
        """测试平均血糖转 HbA1c"""
        result = average_glucose_to_hba1c(7.8, GlucoseUnit.MMOL_L)
        self.assertAlmostEqual(result['hba1c'], 6.52, places=1)
    
    def test_mgdl_to_hba1c(self):
        """测试 mg/dL 转换 HbA1c"""
        result = average_glucose_to_hba1c(140, GlucoseUnit.MG_DL)
        self.assertAlmostEqual(result['hba1c'], 6.52, places=1)


class TestAverageGlucoseEstimation(unittest.TestCase):
    """测试平均血糖估算"""
    
    def test_basic_estimation(self):
        """测试基本估算"""
        readings = [
            (5.5, GlucoseUnit.MMOL_L),
            (6.0, GlucoseUnit.MMOL_L),
            (5.8, GlucoseUnit.MMOL_L)
        ]
        result = estimate_average_glucose(readings)
        self.assertAlmostEqual(result['avg_mmol'], 5.77, places=2)
        self.assertEqual(result['count'], 3)
    
    def test_mixed_units(self):
        """测试混合单位"""
        readings = [
            (5.5, GlucoseUnit.MMOL_L),
            (100, GlucoseUnit.MG_DL),  # ~5.55 mmol/L
            (6.0, GlucoseUnit.MMOL_L)
        ]
        result = estimate_average_glucose(readings)
        self.assertAlmostEqual(result['avg_mmol'], 5.68, places=2)
    
    def test_time_in_range(self):
        """测试目标范围内时间计算"""
        readings = [
            (4.0, GlucoseUnit.MMOL_L),  # 在范围
            (5.0, GlucoseUnit.MMOL_L),  # 在范围
            (11.0, GlucoseUnit.MMOL_L), # 超范围
            (6.0, GlucoseUnit.MMOL_L),  # 在范围
        ]
        result = estimate_average_glucose(readings)
        self.assertEqual(result['time_in_range_percent'], 75.0)
    
    def test_variability_assessment(self):
        """测试血糖波动评估"""
        # 低波动
        readings_low = [(5.5, GlucoseUnit.MMOL_L) for _ in range(5)]
        result = estimate_average_glucose(readings_low)
        self.assertEqual(result['glucose_variability'], '低')
        
        # 高波动
        readings_high = [(3.0, GlucoseUnit.MMOL_L), (10.0, GlucoseUnit.MMOL_L)]
        result = estimate_average_glucose(readings_high)
        self.assertEqual(result['glucose_variability'], '高')
    
    def test_empty_readings(self):
        """测试空读数"""
        result = estimate_average_glucose([])
        self.assertIn('error', result)


class TestGlucoseTrendAnalysis(unittest.TestCase):
    """测试血糖趋势分析"""
    
    def test_rising_trend(self):
        """测试上升趋势"""
        now = datetime.now()
        readings = [
            (5.5, GlucoseUnit.MMOL_L, now - timedelta(hours=2)),
            (6.0, GlucoseUnit.MMOL_L, now - timedelta(hours=1)),
            (6.5, GlucoseUnit.MMOL_L, now)
        ]
        result = analyze_glucose_trend(readings)
        self.assertEqual(result['trend'], '上升')
        self.assertEqual(result['trend_arrow'], '↑')
    
    def test_falling_trend(self):
        """测试下降趋势"""
        now = datetime.now()
        readings = [
            (7.5, GlucoseUnit.MMOL_L, now - timedelta(hours=2)),
            (7.0, GlucoseUnit.MMOL_L, now - timedelta(hours=1)),
            (6.5, GlucoseUnit.MMOL_L, now)
        ]
        result = analyze_glucose_trend(readings)
        self.assertEqual(result['trend'], '下降')
        self.assertEqual(result['trend_arrow'], '↓')
    
    def test_stable_trend(self):
        """测试平稳趋势"""
        now = datetime.now()
        readings = [
            (5.5, GlucoseUnit.MMOL_L, now - timedelta(hours=2)),
            (5.5, GlucoseUnit.MMOL_L, now - timedelta(hours=1)),
            (5.5, GlucoseUnit.MMOL_L, now)
        ]
        result = analyze_glucose_trend(readings)
        self.assertEqual(result['trend'], '平稳')
        self.assertEqual(result['trend_arrow'], '→')
    
    def test_prediction(self):
        """测试预测功能"""
        now = datetime.now()
        readings = [
            (5.5, GlucoseUnit.MMOL_L, now - timedelta(hours=2)),
            (6.0, GlucoseUnit.MMOL_L, now - timedelta(hours=1)),
            (6.5, GlucoseUnit.MMOL_L, now)
        ]
        result = analyze_glucose_trend(readings)
        self.assertAlmostEqual(result['predicted_next_mmol'], 7.0, places=2)
    
    def test_insufficient_data(self):
        """测试数据不足"""
        now = datetime.now()
        readings = [(5.5, GlucoseUnit.MMOL_L, now)]
        result = analyze_glucose_trend(readings)
        self.assertIn('error', result)


class TestInsulinCalculation(unittest.TestCase):
    """测试胰岛素计算"""
    
    def test_correction_dose(self):
        """测试校正剂量"""
        result = calculate_insulin_sensitivity(10.0, 6.0, 2.0, GlucoseUnit.MMOL_L)
        self.assertAlmostEqual(result['correction_units'], 2.0, places=2)
    
    def test_no_correction_needed(self):
        """测试无需校正"""
        result = calculate_insulin_sensitivity(6.0, 6.0, 2.0, GlucoseUnit.MMOL_L)
        self.assertAlmostEqual(result['correction_units'], 0.0, places=2)
    
    def test_mgdl_calculation(self):
        """测试 mg/dL 单位计算"""
        result = calculate_insulin_sensitivity(180, 108, 36, GlucoseUnit.MG_DL)
        # 180 mg/dL - 108 mg/dL = 72 mg/dL / 36 = 2 units
        self.assertAlmostEqual(result['correction_units'], 2.0, places=2)
    
    def test_carb_to_insulin(self):
        """测试碳水转胰岛素"""
        result = carbohydrate_to_insulin(60, 10)
        self.assertEqual(result['carb_units'], 6.0)
        self.assertEqual(result['total_units'], 6.0)
    
    def test_carb_with_correction(self):
        """测试碳水加校正"""
        result = carbohydrate_to_insulin(
            carbs=60, icr=10,
            current_glucose=10.0, target_glucose=6.0, isf=2.0,
            unit=GlucoseUnit.MMOL_L
        )
        self.assertEqual(result['carb_units'], 6.0)
        self.assertEqual(result['correction_units'], 2.0)
        self.assertEqual(result['total_units'], 8.0)


class TestGlucoseReport(unittest.TestCase):
    """测试血糖报告"""
    
    def test_basic_report(self):
        """测试基本报告"""
        now = datetime.now()
        readings = [
            (5.5, GlucoseUnit.MMOL_L, now - timedelta(hours=i))
            for i in range(10)
        ]
        report = glucose_report(readings)
        
        self.assertEqual(report['summary']['total_readings'], 10)
        self.assertAlmostEqual(report['statistics']['average_mmol/L'], 5.5, places=2)
        self.assertEqual(report['time_in_range']['in_range_percent'], 100.0)
    
    def test_mixed_range_report(self):
        """测试混合范围报告"""
        now = datetime.now()
        readings = [
            (4.0, GlucoseUnit.MMOL_L, now - timedelta(hours=9)),  # 在范围
            (5.5, GlucoseUnit.MMOL_L, now - timedelta(hours=8)),  # 在范围
            (11.0, GlucoseUnit.MMOL_L, now - timedelta(hours=7)), # 超范围
            (6.0, GlucoseUnit.MMOL_L, now - timedelta(hours=6)),  # 在范围
            (8.0, GlucoseUnit.MMOL_L, now - timedelta(hours=5)),  # 在范围
            (2.5, GlucoseUnit.MMOL_L, now - timedelta(hours=4)),  # 低血糖
            (7.0, GlucoseUnit.MMOL_L, now - timedelta(hours=3)),  # 在范围
            (9.0, GlucoseUnit.MMOL_L, now - timedelta(hours=2)),  # 在范围
            (12.0, GlucoseUnit.MMOL_L, now - timedelta(hours=1)), # 超范围
            (5.0, GlucoseUnit.MMOL_L, now),                       # 在范围
        ]
        report = glucose_report(readings)
        
        self.assertEqual(report['time_in_range']['in_range_count'], 7)
        self.assertEqual(report['time_in_range']['below_range_count'], 1)
        self.assertEqual(report['time_in_range']['above_range_count'], 2)
    
    def test_empty_report(self):
        """测试空报告"""
        report = glucose_report([])
        self.assertIn('error', report)
    
    def test_hba1c_estimate_in_report(self):
        """测试报告中的 HbA1c 估算"""
        now = datetime.now()
        # 平均血糖约 7.8 mmol/L
        readings = [(7.8, GlucoseUnit.MMOL_L, now - timedelta(hours=i)) for i in range(5)]
        report = glucose_report(readings)
        
        self.assertAlmostEqual(report['hba1c_estimate']['estimated_hba1c'], 6.52, places=1)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_zero_values(self):
        """测试零值"""
        result = convert_glucose(0, GlucoseUnit.MMOL_L, GlucoseUnit.MG_DL)
        self.assertEqual(result, 0)
    
    def test_negative_values(self):
        """测试负值"""
        # 系统应该能处理，但在实际场景中不应该出现
        result = convert_glucose(-1, GlucoseUnit.MMOL_L, GlucoseUnit.MG_DL)
        self.assertAlmostEqual(result, -18.02, places=1)
    
    def test_very_high_values(self):
        """测试极高血糖值"""
        result = assess_glucose(30, GlucoseUnit.MMOL_L, fasting=True)
        self.assertEqual(result['risk_level'], 'high')


if __name__ == '__main__':
    unittest.main(verbosity=2)