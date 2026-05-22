#!/usr/bin/env python3
"""
HRV Utils 测试套件

测试 HRV (心率变异性) 分析功能
"""

import unittest
import math
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    preprocess_rr_intervals,
    interpolate_rr_to_uniform,
    calculate_time_domain_metrics,
    calculate_frequency_domain_metrics,
    calculate_nonlinear_metrics,
    detect_arrhythmias,
    assess_health_status,
    analyze_hrv,
    get_hrv_summary,
    calculate_stress_index,
    calculate_recovery_score,
    check_readiness,
    TimeDomainMetrics,
    FrequencyDomainMetrics,
    NonlinearMetrics,
    HealthAssessment,
    ArrhythmiaDetection
)


class TestPreprocessRRIntervals(unittest.TestCase):
    """RR 间期预处理测试"""
    
    def test_preprocess_normal_data(self):
        """测试正常数据预处理"""
        rr = [800, 810, 795, 820, 815, 805, 825, 810]
        clean_rr, artifacts = preprocess_rr_intervals(rr)
        
        self.assertEqual(len(clean_rr), len(rr))
        self.assertEqual(len(artifacts), 0)
    
    def test_preprocess_artifact_detection(self):
        """测试伪影检测"""
        # 包含一个明显异常值
        rr = [800, 810, 400, 820, 830]  # 400 明显偏离
        clean_rr, artifacts = preprocess_rr_intervals(rr)
        
        self.assertGreater(len(artifacts), 0)
    
    def test_preprocess_physiological_limits(self):
        """测试生理范围过滤"""
        # 包含超出范围的值
        rr = [800, 100, 2000, 810, 820]  # 100 和 2000 超出范围
        clean_rr, artifacts = preprocess_rr_intervals(rr, min_rr=300, max_rr=2000)
        
        self.assertTrue(len(artifacts) > 0)
    
    def test_preprocess_interpolation(self):
        """测试插值功能"""
        rr = [800, 400, 810, 820]  # 400 是异常值
        clean_rr1, _ = preprocess_rr_intervals(rr, interpolate=True)
        clean_rr2, _ = preprocess_rr_intervals(rr, interpolate=False)
        
        # 两种模式都应返回有效数据
        self.assertTrue(len(clean_rr1) > 0)
    
    def test_preprocess_short_data(self):
        """测试短数据"""
        rr = [800, 810]
        clean_rr, artifacts = preprocess_rr_intervals(rr)
        
        self.assertEqual(len(clean_rr), 2)
        self.assertEqual(len(artifacts), 0)


class TestInterpolateRRToUniform(unittest.TestCase):
    """RR 间期插值测试"""
    
    def test_interpolate_basic(self):
        """测试基本插值"""
        rr = [800, 810, 795, 820, 815]
        uniform = interpolate_rr_to_uniform(rr, target_rate=4.0)
        
        self.assertIsInstance(uniform, list)
        self.assertTrue(len(uniform) > 0)
    
    def test_interpolate_target_rate(self):
        """测试不同目标采样率"""
        rr = [800, 810, 795, 820, 815, 805, 825, 810]
        
        uniform_2 = interpolate_rr_to_uniform(rr, target_rate=2.0)
        uniform_4 = interpolate_rr_to_uniform(rr, target_rate=4.0)
        
        # 4Hz 应产生更多采样点
        self.assertTrue(len(uniform_4) >= len(uniform_2))
    
    def test_interpolate_short_data(self):
        """测试短数据插值"""
        rr = [800]
        uniform = interpolate_rr_to_uniform(rr)
        
        self.assertEqual(len(uniform), 1)


class TestTimeDomainMetrics(unittest.TestCase):
    """时域分析指标测试"""
    
    def test_calculate_time_domain_basic(self):
        """测试基本时域计算"""
        nn = [800, 810, 795, 820, 815, 805, 825, 810]
        metrics = calculate_time_domain_metrics(nn)
        
        self.assertIsInstance(metrics, TimeDomainMetrics)
        self.assertGreater(metrics.mean_nn, 0)
        self.assertGreater(metrics.sdnn, 0)
        self.assertGreater(metrics.rmssd, 0)
    
    def test_calculate_time_domain_values(self):
        """测试计算值正确性"""
        nn = [800, 800, 800, 800]  # 完全稳定
        metrics = calculate_time_domain_metrics(nn)
        
        # SDNN 应为 0（无变异）
        self.assertAlmostEqual(metrics.sdnn, 0, places=1)
        self.assertEqual(metrics.mean_nn, 800)
    
    def test_calculate_time_domain_nn50(self):
        """测试 NN50 计算"""
        # 创建相邻间期差异超过50ms的数据
        nn = [800, 900, 700, 800, 900, 700, 800, 900]
        metrics = calculate_time_domain_metrics(nn)
        
        self.assertGreater(metrics.nn50, 0)
    
    def test_calculate_time_domain_pnn50(self):
        """测试 pNN50 计算"""
        nn = [800, 900, 700, 800, 900, 700, 800, 900]
        metrics = calculate_time_domain_metrics(nn)
        
        self.assertGreater(metrics.pnn50, 0)
        self.assertLessEqual(metrics.pnn50, 100)
    
    def test_calculate_time_domain_short_data(self):
        """测试短数据"""
        nn = [800]
        metrics = calculate_time_domain_metrics(nn)
        
        self.assertEqual(metrics.nn_count, 1)
        self.assertEqual(metrics.sdnn, 0)


class TestFrequencyDomainMetrics(unittest.TestCase):
    """频域分析指标测试"""
    
    def test_calculate_frequency_domain_basic(self):
        """测试基本频域计算"""
        nn = [800, 810, 795, 820, 815, 805, 825, 810, 790, 800,
              805, 815, 790, 810, 805, 820, 795, 810, 805, 815]
        metrics = calculate_frequency_domain_metrics(nn)
        
        self.assertIsInstance(metrics, FrequencyDomainMetrics)
        self.assertGreater(metrics.total_power, 0)
    
    def test_calculate_frequency_domain_components(self):
        """测试频域分量"""
        nn = [800 + i * 0.5 - (i % 3) * 0.2 for i in range(50)]
        metrics = calculate_frequency_domain_metrics(nn)
        
        # 各分量应有合理值
        self.assertGreaterEqual(metrics.lf, 0)
        self.assertGreaterEqual(metrics.hf, 0)
        self.assertGreater(metrics.lf_hf_ratio, 0)
    
    def test_calculate_frequency_domain_normalized(self):
        """测试标准化功率"""
        nn = [800, 810, 795, 820] * 15
        metrics = calculate_frequency_domain_metrics(nn)
        
        # 标准化功率应在合理范围
        self.assertGreaterEqual(metrics.lf_nu, 0)
        self.assertLessEqual(metrics.lf_nu, 100)
        self.assertGreaterEqual(metrics.hf_nu, 0)
        self.assertLessEqual(metrics.hf_nu, 100)
    
    def test_calculate_frequency_domain_short_data(self):
        """测试短数据"""
        nn = [800, 810, 795]
        metrics = calculate_frequency_domain_metrics(nn)
        
        # 数据不足时应返回默认值
        self.assertEqual(metrics.total_power, 0)


class TestNonlinearMetrics(unittest.TestCase):
    """非线性分析指标测试"""
    
    def test_calculate_nonlinear_basic(self):
        """测试基本非线性计算"""
        nn = [800, 810, 795, 820, 815, 805, 825, 810]
        metrics = calculate_nonlinear_metrics(nn)
        
        self.assertIsInstance(metrics, NonlinearMetrics)
        self.assertGreater(metrics.sd1, 0)
        self.assertGreater(metrics.sd2, 0)
    
    def test_calculate_nonlinear_sd1_sd2(self):
        """测试 SD1 和 SD2 关系"""
        nn = [800, 810, 795, 820, 815, 805, 825, 810]
        metrics = calculate_nonlinear_metrics(nn)
        
        # SD2 通常应大于 SD1
        self.assertGreaterEqual(metrics.sd2, metrics.sd1)
    
    def test_calculate_nonlinear_ratio(self):
        """测试 SD1/SD2 比率"""
        nn = [800, 810, 795, 820, 815, 805, 825, 810]
        metrics = calculate_nonlinear_metrics(nn)
        
        self.assertGreater(metrics.sd1_sd2_ratio, 0)
        self.assertLessEqual(metrics.sd1_sd2_ratio, 1)  # 通常小于或等于1
    
    def test_calculate_nonlinear_entropy(self):
        """测试熵计算"""
        nn = [800, 810, 795, 820, 815, 805, 825, 810, 790, 800,
              805, 815, 790, 810, 805, 820]
        metrics = calculate_nonlinear_metrics(nn)
        
        # 近似熵和样本熵可能有值（可以是负值）
        if metrics.apen is not None:
            self.assertIsInstance(metrics.apen, float)
        if metrics.sampen is not None:
            self.assertIsInstance(metrics.sampen, float)
    
    def test_calculate_nonlinear_short_data(self):
        """测试短数据"""
        nn = [800, 810]
        metrics = calculate_nonlinear_metrics(nn)
        
        # 短数据时指标应为 0
        self.assertEqual(metrics.sd1, 0)
        self.assertEqual(metrics.sd2, 0)


class TestArrhythmiaDetection(unittest.TestCase):
    """心律异常检测测试"""
    
    def test_detect_arrhythmias_normal(self):
        """测试正常心律"""
        nn = [800, 810, 795, 820, 815, 805, 825, 810]
        detection = detect_arrhythmias(nn)
        
        self.assertIsInstance(detection, ArrhythmiaDetection)
        self.assertFalse(detection.has_arrhythmia)
    
    def test_detect_arrhythmias_ectopic(self):
        """测试异位搏动"""
        # 包含短间期后长间期（典型异位搏动模式）
        nn = [800, 400, 1200, 800, 810]  # 400-1200 可能是 PVC
        detection = detect_arrhythmias(nn)
        
        self.assertGreater(detection.ectopic_beats, 0)
    
    def test_detect_arrhythmias_pause(self):
        """测试暂停"""
        # 包含长间期（可能的漏搏）
        nn = [800, 1600, 810, 820]  # 1600 是两倍长度
        detection = detect_arrhythmias(nn)
        
        self.assertGreater(detection.missed_beats, 0)
    
    def test_detect_arrhythmias_irregular(self):
        """测试不规则心律"""
        nn = [800, 400, 1200, 500, 1500, 700]
        detection = detect_arrhythmias(nn)
        
        self.assertGreater(detection.irregularity_score, 0)
    
    def test_detect_arrhythmias_short_data(self):
        """测试短数据"""
        nn = [800]
        detection = detect_arrhythmias(nn)
        
        self.assertFalse(detection.has_arrhythmia)


class TestHealthAssessment(unittest.TestCase):
    """健康评估测试"""
    
    def test_assess_health_status_basic(self):
        """测试基本健康评估"""
        nn = [800, 810, 795, 820, 815, 805, 825, 810]
        time_m = calculate_time_domain_metrics(nn)
        assessment = assess_health_status(time_m)
        
        self.assertIsInstance(assessment, HealthAssessment)
        self.assertGreater(assessment.stress_index, 0)
        self.assertIn(assessment.stress_level, ['低', '中等', '高', '很高'])
    
    def test_assess_health_status_with_age(self):
        """测试带年龄的健康评估"""
        nn = [800, 810, 795, 820, 815, 805, 825, 810]
        time_m = calculate_time_domain_metrics(nn)
        assessment = assess_health_status(time_m, age=30)
        
        self.assertIsNotNone(assessment.hrv_age)
    
    def test_assess_health_status_recovery(self):
        """测试恢复状态"""
        # 高 HRV 数据
        nn = [800, 850, 780, 900, 750, 850, 800, 900]
        time_m = calculate_time_domain_metrics(nn)
        assessment = assess_health_status(time_m)
        
        self.assertIn(assessment.recovery_status, 
                      ['优秀恢复', '良好恢复', '一般恢复', '恢复不足'])
    
    def test_assess_health_status_recommendations(self):
        """测试建议生成"""
        nn = [800, 805, 810, 808]  # 低变异
        time_m = calculate_time_domain_metrics(nn)
        assessment = assess_health_status(time_m)
        
        self.assertIsInstance(assessment.recommendations, list)
        self.assertTrue(len(assessment.recommendations) > 0)


class TestAnalyzeHRV(unittest.TestCase):
    """综合分析测试"""
    
    def test_analyze_hrv_basic(self):
        """测试基本综合分析"""
        rr = [800, 810, 795, 820, 815, 805, 825, 810, 790, 800,
              805, 815, 790, 810, 805, 820, 795, 810, 805, 815]
        result = analyze_hrv(rr)
        
        self.assertIn('time_domain', result)
        self.assertIn('health_assessment', result)
        self.assertIn('arrhythmia', result)
    
    def test_analyze_hrv_with_age(self):
        """测试带年龄的分析"""
        rr = [800, 810, 795, 820, 815, 805, 825, 810] * 5
        result = analyze_hrv(rr, age=30)
        
        self.assertIsNotNone(result['health_assessment']['hrv_age'])
    
    def test_analyze_hrv_frequency(self):
        """测试频域分析"""
        rr = [800 + i * 0.5 - (i % 3) * 0.2 for i in range(60)]
        result = analyze_hrv(rr, include_frequency=True)
        
        self.assertIsNotNone(result['frequency_domain'])
    
    def test_analyze_hrv_nonlinear(self):
        """测试非线性分析"""
        rr = [800, 810, 795, 820, 815, 805, 825, 810] * 5
        result = analyze_hrv(rr, include_nonlinear=True)
        
        self.assertIsNotNone(result['nonlinear'])
    
    def test_analyze_hrv_metadata(self):
        """测试元数据"""
        rr = [800, 810, 795, 820, 815, 805, 825, 810]
        result = analyze_hrv(rr)
        
        self.assertIn('metadata', result)
        self.assertEqual(result['metadata']['input_count'], len(rr))


class TestHRVSummary(unittest.TestCase):
    """HRV 摘要测试"""
    
    def test_get_hrv_summary_basic(self):
        """测试基本摘要生成"""
        rr = [800, 810, 795, 820, 815, 805, 825, 810]
        summary = get_hrv_summary(rr)
        
        self.assertIn("HRV", summary)
        self.assertIn("时域分析", summary)
    
    def test_get_hrv_summary_with_age(self):
        """测试带年龄的摘要"""
        rr = [800, 810, 795, 820, 815, 805, 825, 810]
        summary = get_hrv_summary(rr, age=30)
        
        self.assertIn("心脏年龄", summary)


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_calculate_stress_index(self):
        """测试压力指数计算"""
        rr = [800, 810, 795, 820, 815, 805, 825, 810]
        stress = calculate_stress_index(rr)
        
        self.assertGreaterEqual(stress, 0)
        self.assertLessEqual(stress, 100)
    
    def test_calculate_recovery_score(self):
        """测试恢复分数计算"""
        rr = [800, 810, 795, 820, 815, 805, 825, 810]
        recovery = calculate_recovery_score(rr)
        
        self.assertGreaterEqual(recovery, 0)
        self.assertLessEqual(recovery, 100)
    
    def test_check_readiness(self):
        """测试准备状态检查"""
        rr = [800, 810, 795, 820, 815, 805, 825, 810]
        status = check_readiness(rr)
        
        self.assertIn('ready', status)
        self.assertIn('readiness_score', status)
        self.assertIn('readiness_level', status)


class TestEdgeCases(unittest.TestCase):
    """边界值测试"""
    
    def test_constant_intervals(self):
        """测试完全恒定间期"""
        rr = [800] * 20
        result = analyze_hrv(rr)
        
        # SDNN 应接近 0
        self.assertLess(result['time_domain']['sdnn'], 5)
    
    def test_extreme_intervals(self):
        """测试极端间期"""
        rr = [300, 2000] * 10
        detection = detect_arrhythmias(rr)
        
        # 应检测到异常
        self.assertTrue(detection.has_arrhythmia)
    
    def test_empty_data(self):
        """测试空数据"""
        rr = []
        metrics = calculate_time_domain_metrics(rr)
        
        self.assertEqual(metrics.nn_count, 0)
    
    def test_single_interval(self):
        """测试单个间期"""
        rr = [800]
        metrics = calculate_time_domain_metrics(rr)
        
        self.assertEqual(metrics.nn_count, 1)
        self.assertEqual(metrics.sdnn, 0)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_analysis_workflow(self):
        """测试完整分析流程"""
        # 模拟30秒心率数据
        rr = [800 + i * 0.5 - (i % 3) * 0.2 for i in range(30)]
        
        # 预处理
        clean_rr, artifacts = preprocess_rr_intervals(rr)
        
        # 时域分析
        time_m = calculate_time_domain_metrics(clean_rr)
        
        # 频域分析
        freq_m = calculate_frequency_domain_metrics(clean_rr)
        
        # 非线性分析
        nonlinear_m = calculate_nonlinear_metrics(clean_rr)
        
        # 异常检测
        arrhythmia = detect_arrhythmias(clean_rr)
        
        # 健康评估
        health = assess_health_status(time_m, freq_m, nonlinear_m, age=30)
        
        # 验证所有步骤
        self.assertGreater(time_m.mean_nn, 0)
        self.assertGreater(freq_m.total_power, 0)
        self.assertGreater(nonlinear_m.sd1, 0)
        self.assertIsInstance(health.stress_level, str)


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestPreprocessRRIntervals))
    suite.addTests(loader.loadTestsFromTestCase(TestInterpolateRRToUniform))
    suite.addTests(loader.loadTestsFromTestCase(TestTimeDomainMetrics))
    suite.addTests(loader.loadTestsFromTestCase(TestFrequencyDomainMetrics))
    suite.addTests(loader.loadTestsFromTestCase(TestNonlinearMetrics))
    suite.addTests(loader.loadTestsFromTestCase(TestArrhythmiaDetection))
    suite.addTests(loader.loadTestsFromTestCase(TestHealthAssessment))
    suite.addTests(loader.loadTestsFromTestCase(TestAnalyzeHRV))
    suite.addTests(loader.loadTestsFromTestCase(TestHRVSummary))
    suite.addTests(loader.loadTestsFromTestCase(TestConvenienceFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    run_tests()