"""
HRV Utils - 使用示例

展示心率变异性分析工具的各种使用场景。
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    preprocess_rr_intervals,
    calculate_time_domain_metrics,
    calculate_frequency_domain_metrics,
    calculate_nonlinear_metrics,
    detect_arrhythmias,
    assess_health_status,
    analyze_hrv,
    get_hrv_summary,
    calculate_stress_index,
    calculate_recovery_score,
    check_readiness
)


def example_basic_analysis():
    """示例1: 基础 HRV 分析"""
    print("\n" + "=" * 60)
    print("示例1: 基础 HRV 分析")
    print("=" * 60)
    
    # 模拟 5 分钟的 RR 间期数据 (约 300 个心跳)
    # 正常成年人的典型数据
    import random
    random.seed(42)
    
    rr_intervals = []
    base_rr = 800  # 基准 RR 间期 (ms), 对应心率约 75 bpm
    
    for i in range(300):
        # 添加自然变异
        variation = random.gauss(0, 15)  # 正态分布变异
        slow_wave = 10 * math.sin(i * 0.02)  # 慢波调制 (呼吸影响)
        rr = base_rr + variation + slow_wave
        rr_intervals.append(round(rr))
    
    # 执行综合分析
    result = analyze_hrv(rr_intervals, age=35)
    
    print(f"\n数据概览:")
    print(f"  有效心跳数: {result['metadata']['valid_count']}")
    print(f"  异常值数量: {result['metadata']['artifact_count']}")
    
    print(f"\n时域指标:")
    print(f"  平均心率: {60000 / result['time_domain']['mean_nn']:.1f} bpm")
    print(f"  SDNN: {result['time_domain']['sdnn']:.2f} ms")
    print(f"  RMSSD: {result['time_domain']['rmssd']:.2f} ms")
    print(f"  pNN50: {result['time_domain']['pnn50']:.1f}%")
    
    print(f"\n健康评估:")
    print(f"  压力指数: {result['health_assessment']['stress_index']}/100")
    print(f"  压力等级: {result['health_assessment']['stress_level']}")
    print(f"  恢复状态: {result['health_assessment']['recovery_status']}")


def example_stress_monitoring():
    """示例2: 压力监测"""
    print("\n" + "=" * 60)
    print("示例2: 实时压力监测")
    print("=" * 60)
    
    # 模拟不同压力状态下的 HRV 数据
    
    # 放松状态 (高 HRV)
    relaxed_rr = generate_hrv_data(base_rr=900, variability=30, count=60)
    relaxed_stress = calculate_stress_index(relaxed_rr)
    relaxed_recovery = calculate_recovery_score(relaxed_rr)
    
    print(f"\n放松状态:")
    print(f"  基准心率: {60000 / 900:.1f} bpm")
    print(f"  压力指数: {relaxed_stress:.1f}/100")
    print(f"  恢复分数: {relaxed_recovery:.1f}/100")
    
    # 正常工作状态 (中等 HRV)
    normal_rr = generate_hrv_data(base_rr=800, variability=20, count=60)
    normal_stress = calculate_stress_index(normal_rr)
    normal_recovery = calculate_recovery_score(normal_rr)
    
    print(f"\n正常工作状态:")
    print(f"  基准心率: {60000 / 800:.1f} bpm")
    print(f"  压力指数: {normal_stress:.1f}/100")
    print(f"  恢复分数: {normal_recovery:.1f}/100")
    
    # 高压状态 (低 HRV)
    stressed_rr = generate_hrv_data(base_rr=750, variability=5, count=60)
    stressed_stress = calculate_stress_index(stressed_rr)
    stressed_recovery = calculate_recovery_score(stressed_rr)
    
    print(f"\n高压状态:")
    print(f"  基准心率: {60000 / 750:.1f} bpm")
    print(f"  压力指数: {stressed_stress:.1f}/100")
    print(f"  恢复分数: {stressed_recovery:.1f}/100")
    
    print(f"\n结论: 高压状态明显增加了压力指数，降低了恢复分数")


def example_training_readiness():
    """示例3: 训练准备状态检查"""
    print("\n" + "=" * 60)
    print("示例3: 训练准备状态检查")
    print("=" * 60)
    
    # 运动员早晨 HRV 数据示例
    
    # 充分恢复后的状态
    recovered_rr = generate_hrv_data(base_rr=850, variability=25, count=50)
    recovered_status = check_readiness(recovered_rr)
    
    print(f"\n充分恢复状态:")
    print(f"  准备状态: {recovered_status['readiness_level']}")
    print(f"  准备分数: {recovered_status['readiness_score']}/100")
    print(f"  RMSSD: {recovered_status['rmssd']:.2f} ms")
    print(f"  建议: 可以进行高强度训练")
    
    # 恢复不足状态
    fatigued_rr = generate_hrv_data(base_rr=780, variability=8, count=50)
    fatigued_status = check_readiness(fatigued_rr)
    
    print(f"\n恢复不足状态:")
    print(f"  准备状态: {fatigued_status['readiness_level']}")
    print(f"  准备分数: {fatigued_status['readiness_score']}/100")
    print(f"  RMSSD: {fatigued_status['rmssd']:.2f} ms")
    if fatigued_status['warning']:
        print(f"  警告: {fatigued_status['warning']}")
    print(f"  建议: 降低训练强度或休息")


def example_arrhythmia_detection():
    """示例4: 心律异常检测"""
    print("\n" + "=" * 60)
    print("示例4: 心律异常检测")
    print("=" * 60)
    
    # 正常心律
    normal_rr = generate_hrv_data(base_rr=800, variability=12, count=30)
    normal_detection = detect_arrhythmias(normal_rr)
    
    print(f"\n正常心律:")
    print(f"  检测到异常: {normal_detection.has_arrhythmia}")
    print(f"  不规则指数: {normal_detection.irregularity_score:.2%}")
    
    # 包含偶发 PVC (室性早搏)
    # PVC 特征: 短间期后跟代偿性长间期
    pvc_rr = generate_hrv_data(base_rr=800, variability=12, count=30)
    # 在中间插入 PVC
    pvc_rr[10] = 400  # 早搏 - 短间期
    pvc_rr[11] = 1200  # 代偿间歇 - 长间期
    
    pvc_detection = detect_arrhythmias(pvc_rr)
    
    print(f"\n包含 PVC (室性早搏):")
    print(f"  检测到异常: {pvc_detection.has_arrhythmia}")
    print(f"  异位搏动数: {pvc_detection.ectopic_beats}")
    print(f"  不规则指数: {pvc_detection.irregularity_score:.2%}")
    
    # 包含漏搏
    pause_rr = generate_hrv_data(base_rr=800, variability=12, count=30)
    pause_rr[15] = 1800  # 显著长间期 (漏搏)
    
    pause_detection = detect_arrhythmias(pause_rr)
    
    print(f"\n包含漏搏:")
    print(f"  检测到异常: {pause_detection.has_arrhythmia}")
    print(f"  漏搏数: {pause_detection.missed_beats}")
    print(f"  不规则指数: {pause_detection.irregularity_score:.2%}")


def example_complete_report():
    """示例5: 完整分析报告"""
    print("\n" + "=" * 60)
    print("示例5: 完整 HRV 分析报告")
    print("=" * 60)
    
    # 模拟 5 分钟测量数据
    rr_intervals = generate_hrv_data(base_rr=800, variability=15, count=300, seed=123)
    
    # 添加一些自然波动
    import random
    random.seed(123)
    for i in range(len(rr_intervals)):
        rr_intervals[i] += random.randint(-10, 10)
    
    summary = get_hrv_summary(rr_intervals, age=32)
    print(summary)


def example_frequency_analysis():
    """示例6: 频域分析详解"""
    print("\n" + "=" * 60)
    print("示例6: 频域分析详解")
    print("=" * 60)
    
    # 长时间测量 (5 分钟以上适合频域分析)
    rr_intervals = generate_hrv_data(base_rr=800, variability=20, count=400)
    
    freq_metrics = calculate_frequency_domain_metrics(rr_intervals)
    
    print(f"\n频域指标解读:")
    print(f"  总功率: {freq_metrics.total_power:.2f} ms²")
    print(f"  VLF (极低频): {freq_metrics.vlf:.2f} ms²")
    print(f"  LF (低频): {freq_metrics.lf:.2f} ms²")
    print(f"  HF (高频): {freq_metrics.hf:.2f} ms²")
    
    print(f"\n标准化功率:")
    print(f"  LF_nu: {freq_metrics.lf_nu:.1f}%")
    print(f"  HF_nu: {freq_metrics.hf_nu:.1f}%")
    
    print(f"\n自律神经平衡指标:")
    print(f"  LF/HF 比率: {freq_metrics.lf_hf_ratio:.2f}")
    
    print(f"\n解读:")
    if freq_metrics.lf_hf_ratio > 3:
        print("  交感神经活动较强，可能处于紧张或高压状态")
    elif freq_metrics.lf_hf_ratio < 1:
        print("  副交感神经活动较强，处于放松状态")
    else:
        print("  自律神经相对平衡")


def example_data_preprocessing():
    """示例7: 数据预处理"""
    print("\n" + "=" * 60)
    print("示例7: 数据预处理 (去除异常值)")
    print("=" * 60)
    
    # 包含测量伪影的原始数据
    raw_rr = [
        800, 810, 795,  # 正常
        250,  # 伪影 (过短)
        820, 815, 805,  # 正常
        2500,  # 伪影 (过长)
        825, 810, 790, 800,  # 正常
        150,  # 伪影 (严重过短)
        805, 815
    ]
    
    print(f"\n原始数据 ({len(raw_rr)} 个 RR 间期):")
    print(f"  包含明显异常值: 250, 2500, 150")
    
    # 预处理
    clean_rr, artifacts = preprocess_rr_intervals(
        raw_rr,
        artifact_threshold=0.3,
        interpolate=True
    )
    
    print(f"\n预处理结果:")
    print(f"  有效数据点: {len(clean_rr)}")
    print(f"  检测到的伪影: {len(artifacts)} 个")
    print(f"  伪影位置: {artifacts}")
    
    print(f"\n处理后数据:")
    print(f"  {clean_rr}")


def example_nonlinear_analysis():
    """示例8: Poincaré 图分析"""
    print("\n" + "=" * 60)
    print("示例8: Poincaré 图非线性分析")
    print("=" * 60)
    
    # 高变异性数据
    high_var_rr = generate_hrv_data(base_rr=800, variability=30, count=100)
    high_nl = calculate_nonlinear_metrics(high_var_rr)
    
    print(f"\n高变异性状态:")
    print(f"  SD1 (短期变异性): {high_nl.sd1:.2f} ms")
    print(f"  SD2 (长期变异性): {high_nl.sd2:.2f} ms")
    print(f"  SD1/SD2 比率: {high_nl.sd1_sd2_ratio:.3f}")
    if high_nl.apen:
        print(f"  近似熵: {high_nl.apen:.3f}")
    
    # 低变异性数据
    low_var_rr = generate_hrv_data(base_rr=800, variability=5, count=100)
    low_nl = calculate_nonlinear_metrics(low_var_rr)
    
    print(f"\n低变异性状态:")
    print(f"  SD1 (短期变异性): {low_nl.sd1:.2f} ms")
    print(f"  SD2 (长期变异性): {low_nl.sd2:.2f} ms")
    print(f"  SD1/SD2 比率: {low_nl.sd1_sd2_ratio:.3f}")
    if low_nl.apen:
        print(f"  近似熵: {low_nl.apen:.3f}")
    
    print(f"\n解读:")
    print(f"  SD1 反映短期心跳间变异 (呼吸性窦性心律不齐)")
    print(f"  SD2 反映长期整体变异")
    print(f"  高 SD1/SD2 比率表示副交感神经活跃")


def generate_hrv_data(base_rr: float, variability: float, count: int, seed: int = None):
    """生成模拟 HRV 数据"""
    import random
    import math
    
    if seed:
        random.seed(seed)
    
    rr_intervals = []
    for i in range(count):
        # 基础变异
        variation = random.gauss(0, variability)
        # 呼吸调制 (约 0.25 Hz)
        slow_wave = variability * 0.5 * math.sin(i * 0.05)
        rr = base_rr + variation + slow_wave
        rr_intervals.append(round(rr))
    
    return rr_intervals


# 导入 math 模块
import math


def main():
    """运行所有示例"""
    print("\n" + "#" * 60)
    print("# HRV Utils 使用示例集")
    print("#" * 60)
    
    example_basic_analysis()
    example_stress_monitoring()
    example_training_readiness()
    example_arrhythmia_detection()
    example_frequency_analysis()
    example_data_preprocessing()
    example_nonlinear_analysis()
    example_complete_report()
    
    print("\n" + "#" * 60)
    print("# 所有示例完成")
    print("#" * 60 + "\n")


if __name__ == '__main__':
    main()