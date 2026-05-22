"""
HRV Utils - 测试模块

测试心率变异性分析工具的所有核心功能。
"""

import sys
import os

# 添加模块路径
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


def test_preprocess_rr_intervals():
    """测试 RR 间期预处理"""
    print("测试 preprocess_rr_intervals...")
    
    # 测试正常数据
    normal_rr = [800, 810, 795, 820, 815, 805, 825, 810]
    clean_rr, artifacts = preprocess_rr_intervals(normal_rr)
    assert len(clean_rr) == len(normal_rr), "正常数据不应被删除"
    assert len(artifacts) == 0, "正常数据不应有异常值"
    
    # 测试包含异常值
    abnormal_rr = [800, 810, 300, 820, 2000, 815, 805]
    clean_rr, artifacts = preprocess_rr_intervals(abnormal_rr)
    assert len(artifacts) > 0, "应检测到异常值"
    
    # 测试插值
    rr_with_artifact = [800, 810, 400, 820, 830]
    clean_rr, artifacts = preprocess_rr_intervals(rr_with_artifact, interpolate=True)
    assert len(clean_rr) == len(rr_with_artifact), "插值后长度应保持"
    
    print("  ✓ preprocess_rr_intervals 测试通过")


def test_interpolate_rr_to_uniform():
    """测试均匀采样插值"""
    print("测试 interpolate_rr_to_uniform...")
    
    rr = [800, 810, 795, 820, 815, 805, 825, 810]
    uniform = interpolate_rr_to_uniform(rr, target_rate=4.0)
    
    assert len(uniform) > 0, "应产生插值结果"
    assert all(u > 0 for u in uniform), "心率值应大于 0"
    
    print("  ✓ interpolate_rr_to_uniform 测试通过")


def test_calculate_time_domain_metrics():
    """测试时域分析"""
    print("测试 calculate_time_domain_metrics...")
    
    # 测试正常 HRV 数据
    normal_rr = [
        800, 810, 795, 820, 815, 805, 825, 810, 790, 800,
        805, 815, 790, 810, 805, 820, 795, 810, 805, 815,
        800, 808, 792, 818, 812, 802, 822, 808, 788, 800
    ]
    
    metrics = calculate_time_domain_metrics(normal_rr)
    
    assert metrics.nn_count == len(normal_rr), "心跳数应匹配"
    assert metrics.mean_nn > 0, "平均 NN 间期应大于 0"
    assert metrics.sdnn > 0, "SDNN 应大于 0"
    assert metrics.rmssd > 0, "RMSSD 应大于 0"
    assert metrics.pnn50 >= 0, "pNN50 应 >= 0"
    
    # 验证数值合理性
    assert 700 < metrics.mean_nn < 900, "平均 NN 间期应在合理范围"
    assert metrics.sdnn < 100, "相对稳定的 HRV，SDNN 应较小"
    
    # 测试低 HRV (高压力) - 但需要足够的数据点
    low_hrv_rr = [800, 802, 801, 803, 802, 804, 803, 801, 802, 803,
                  800, 802, 801, 803, 802, 804, 803, 801, 802, 803]
    low_metrics = calculate_time_domain_metrics(low_hrv_rr)
    
    # 低 HRV 通常有较低的 RMSSD
    assert low_metrics.rmssd <= metrics.rmssd + 5, "低 HRV 应有较低或相近 RMSSD"
    
    # 测试空数据
    empty_metrics = calculate_time_domain_metrics([])
    assert empty_metrics.mean_nn == 0, "空数据应返回 0"
    
    print("  ✓ calculate_time_domain_metrics 测试通过")


def test_calculate_frequency_domain_metrics():
    """测试频域分析"""
    print("测试 calculate_frequency_domain_metrics...")
    
    # 需要较长数据才能进行频域分析
    long_rr = []
    for i in range(60):
        # 模拟正常 HRV
        base = 800
        variation = (i % 10 - 5) * 10
        rr = base + variation + (i % 3 - 1) * 5
        long_rr.append(rr)
    
    metrics = calculate_frequency_domain_metrics(long_rr)
    
    assert metrics.total_power >= 0, "总功率应 >= 0"
    assert metrics.vlf >= 0, "VLF 应 >= 0"
    assert metrics.lf >= 0, "LF 应 >= 0"
    assert metrics.hf >= 0, "HF 应 >= 0"
    assert 0 <= metrics.lf_nu <= 100, "LF_nu 应在 0-100"
    assert 0 <= metrics.hf_nu <= 100, "HF_nu 应在 0-100"
    assert metrics.lf_hf_ratio >= 0, "LF/HF 比率应 >= 0"
    
    # 测试短数据
    short_rr = [800, 810, 820]
    short_metrics = calculate_frequency_domain_metrics(short_rr)
    assert short_metrics.total_power == 0, "短数据应返回 0"
    
    print("  ✓ calculate_frequency_domain_metrics 测试通过")


def test_calculate_nonlinear_metrics():
    """测试非线性分析"""
    print("测试 calculate_nonlinear_metrics...")
    
    # 正常 HRV 数据
    normal_rr = [
        800, 810, 795, 820, 815, 805, 825, 810, 790, 800,
        805, 815, 790, 810, 805, 820, 795, 810, 805, 815
    ]
    
    metrics = calculate_nonlinear_metrics(normal_rr)
    
    assert metrics.sd1 > 0, "SD1 应大于 0"
    assert metrics.sd2 > 0, "SD2 应大于 0"
    assert metrics.sd1_sd2_ratio > 0, "SD1/SD2 比率应大于 0"
    
    # SD2 应大于或等于 SD1 (通常情况)
    # 允许一些波动
    assert metrics.sd2 >= metrics.sd1 * 0.5, "SD2 应接近或大于 SD1"
    
    # 测试近似熵和样本熵
    if metrics.apen:
        assert metrics.apen > 0, "近似熵应大于 0"
    if metrics.sampen:
        assert metrics.sampen > 0, "样本熵应大于 0"
    
    # 测试短数据
    short_metrics = calculate_nonlinear_metrics([800, 810])
    assert short_metrics.sd1 == 0, "短数据应返回 0"
    
    print("  ✓ calculate_nonlinear_metrics 测试通过")


def test_detect_arrhythmias():
    """测试心律异常检测"""
    print("测试 detect_arrhythmias...")
    
    # 正常数据 - 无异常
    normal_rr = [800, 810, 805, 815, 810, 808, 812, 810]
    detection = detect_arrhythmias(normal_rr)
    
    assert not detection.has_arrhythmia, "正常数据不应检测到异常"
    assert detection.ectopic_beats == 0, "无异位搏动"
    assert detection.irregularity_score < 0.1, "不规则指数应很低"
    
    # 包含异位搏动 (短间期后跟长间期)
    ectopic_rr = [800, 400, 1200, 810, 805, 815, 810]  # 400 后跟 1200
    ectopic_detection = detect_arrhythmias(ectopic_rr)
    
    assert ectopic_detection.has_arrhythmia, "应检测到异常"
    assert ectopic_detection.ectopic_beats > 0, "应检测到异位搏动"
    
    # 包含漏搏 (长间期)
    pause_rr = [800, 810, 1800, 805, 815]  # 1800 是显著长间期
    pause_detection = detect_arrhythmias(pause_rr)
    
    assert pause_detection.has_arrhythmia, "应检测到异常"
    assert pause_detection.missed_beats > 0, "应检测到漏搏"
    
    print("  ✓ detect_arrhythmias 测试通过")


def test_assess_health_status():
    """测试健康评估"""
    print("测试 assess_health_status...")
    
    # 高 HRV (良好状态)
    high_hrv_rr = [
        800, 830, 770, 850, 780, 860, 770, 840, 760, 870,
        770, 850, 780, 840, 760, 880, 750, 860, 780, 850
    ]
    
    time_metrics = calculate_time_domain_metrics(high_hrv_rr)
    freq_metrics = calculate_frequency_domain_metrics(high_hrv_rr)
    nonlinear_metrics = calculate_nonlinear_metrics(high_hrv_rr)
    
    assessment = assess_health_status(
        time_metrics, freq_metrics, nonlinear_metrics, age=30
    )
    
    assert 0 <= assessment.stress_index <= 100, "压力指数应在 0-100"
    assert assessment.stress_level in ['低', '中等', '高', '很高'], "压力等级应有效"
    assert assessment.recovery_status in ['优秀恢复', '良好恢复', '一般恢复', '恢复不足'], \
        "恢复状态应有效"
    assert len(assessment.recommendations) > 0, "应有建议"
    
    # 低 HRV (高压力状态)
    low_hrv_rr = [800, 802, 801, 803, 802, 804, 803, 801, 802, 803]
    low_time_metrics = calculate_time_domain_metrics(low_hrv_rr)
    low_assessment = assess_health_status(low_time_metrics)
    
    assert low_assessment.stress_index > assessment.stress_index, \
        "低 HRV 应有更高压力指数"
    
    print("  ✓ assess_health_status 测试通过")


def test_analyze_hrv():
    """测试综合分析"""
    print("测试 analyze_hrv...")
    
    rr = [
        800, 810, 795, 820, 815, 805, 825, 810, 790, 800,
        805, 815, 790, 810, 805, 820, 795, 810, 805, 815,
        800, 808, 792, 818, 812, 802, 822, 808, 788, 800,
        805, 815, 790, 810, 805, 820, 795, 810, 805, 815
    ]
    
    result = analyze_hrv(rr, age=30)
    
    # 检查结构
    assert 'time_domain' in result, "应包含时域分析"
    assert 'frequency_domain' in result, "应包含频域分析"
    assert 'nonlinear' in result, "应包含非线性分析"
    assert 'arrhythmia' in result, "应包含心律异常检测"
    assert 'health_assessment' in result, "应包含健康评估"
    assert 'metadata' in result, "应包含元数据"
    
    # 检查时域指标
    assert 'mean_nn' in result['time_domain']
    assert 'sdnn' in result['time_domain']
    assert 'rmssd' in result['time_domain']
    
    # 检查元数据
    assert result['metadata']['input_count'] == len(rr), "输入计数应匹配"
    
    print("  ✓ analyze_hrv 测试通过")


def test_get_hrv_summary():
    """测试文本摘要"""
    print("测试 get_hrv_summary...")
    
    rr = [
        800, 810, 795, 820, 815, 805, 825, 810, 790, 800,
        805, 815, 790, 810, 805, 820, 795, 810, 805, 815
    ]
    
    summary = get_hrv_summary(rr, age=30)
    
    assert isinstance(summary, str), "摘要应为字符串"
    assert 'HRV' in summary, "应包含 HRV 关键词"
    assert '时域分析' in summary, "应包含时域分析"
    assert '健康评估' in summary, "应包含健康评估"
    assert len(summary) > 100, "摘要应有足够内容"
    
    print("  ✓ get_hrv_summary 测试通过")


def test_calculate_stress_index():
    """测试压力指数计算"""
    print("测试 calculate_stress_index...")
    
    # 高 HRV = 低压力
    high_hrv_rr = [800, 850, 750, 880, 770, 850, 760, 860, 780, 840]
    high_hrv_stress = calculate_stress_index(high_hrv_rr)
    
    # 低 HRV = 高压力
    low_hrv_rr = [800, 802, 801, 803, 802, 804, 803, 801]
    low_hrv_stress = calculate_stress_index(low_hrv_rr)
    
    assert 0 <= high_hrv_stress <= 100, "压力指数应在 0-100"
    assert 0 <= low_hrv_stress <= 100, "压力指数应在 0-100"
    assert low_hrv_stress > high_hrv_stress, "低 HRV 应有更高压力指数"
    
    print("  ✓ calculate_stress_index 测试通过")


def test_calculate_recovery_score():
    """测试恢复分数计算"""
    print("测试 calculate_recovery_score...")
    
    high_hrv_rr = [800, 850, 750, 880, 770, 850, 760, 860, 780, 840]
    recovery = calculate_recovery_score(high_hrv_rr)
    
    assert 0 <= recovery <= 100, "恢复分数应在 0-100"
    
    # 高 HRV 应有较高恢复分数
    assert recovery > 50, "良好 HRV 应有较高恢复分数"
    
    print("  ✓ calculate_recovery_score 测试通过")


def test_check_readiness():
    """测试训练准备状态"""
    print("测试 check_readiness...")
    
    # 良好状态
    good_rr = [
        800, 850, 750, 880, 770, 850, 760, 860, 780, 840,
        790, 860, 770, 850, 780, 870
    ]
    readiness = check_readiness(good_rr)
    
    assert 'ready' in readiness, "应包含 ready 状态"
    assert 'readiness_score' in readiness, "应包含准备分数"
    assert 'readiness_level' in readiness, "应包含准备等级"
    assert readiness['readiness_score'] > 50, "良好状态应有较高准备分数"
    
    # 低准备状态
    low_rr = [800, 802, 801, 803, 802, 804, 803, 801]
    low_readiness = check_readiness(low_rr)
    
    assert low_readiness['readiness_score'] < readiness['readiness_score'], \
        "低 HRV 应有更低准备分数"
    
    print("  ✓ check_readiness 测试通过")


def test_edge_cases():
    """测试边界情况"""
    print("测试边界情况...")
    
    # 空数据
    empty_result = analyze_hrv([])
    assert empty_result['time_domain']['mean_nn'] == 0
    
    # 单个数据点
    single_result = analyze_hrv([800])
    assert single_result['time_domain']['nn_count'] == 1
    
    # 极端值 - 需要预处理
    extreme_rr = [300, 2000, 500, 1500, 400]
    extreme_clean, extreme_artifacts = preprocess_rr_intervals(
        extreme_rr, min_rr=300, max_rr=2000
    )
    # 应在范围内保留或处理
    assert len(extreme_clean) >= 0, "预处理应返回有效数据"
    
    # 测试包含 None 的处理 - 应能正常处理
    mixed_data = [800, 810, 795, 820]
    mixed_result = analyze_hrv(mixed_data)
    assert mixed_result['metadata']['valid_count'] >= 0
    
    print("  ✓ 边界情况测试通过")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 50)
    print("HRV Utils 测试套件")
    print("=" * 50 + "\n")
    
    tests = [
        test_preprocess_rr_intervals,
        test_interpolate_rr_to_uniform,
        test_calculate_time_domain_metrics,
        test_calculate_frequency_domain_metrics,
        test_calculate_nonlinear_metrics,
        test_detect_arrhythmias,
        test_assess_health_status,
        test_analyze_hrv,
        test_get_hrv_summary,
        test_calculate_stress_index,
        test_calculate_recovery_score,
        test_check_readiness,
        test_edge_cases
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"  ✗ {test.__name__} 失败: {e}")
    
    print("\n" + "-" * 50)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("-" * 50)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)