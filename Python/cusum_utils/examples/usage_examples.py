"""
CUSUM控制图工具模块使用示例

CUSUM（累积和）控制图是统计质量控制中的重要工具，
用于检测过程均值的微小偏移。本示例展示如何使用 cusum_utils 进行过程监控。

应用领域：
- 制造业质量控制
- 金融市场异常检测
- 医疗健康监测
- 网络流量监控
- 环境监测
"""

import os
import sys
import random
# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    calculate_mean_std,
    estimate_control_parameters,
    standard_cusum,
    tabular_cusum,
    standardized_cusum,
    detect_change_points,
    cusum_for_variance,
    cusum_for_proportion,
    design_cusum,
    cusum_score,
    ewma_cusum,
    cusum_control_limits,
    analyze_process,
    format_cusum_report,
    CUSUMMonitor,
)


def example_basic_cusum():
    """示例1：基本CUSUM计算"""
    print("\n" + "=" * 60)
    print("示例1：基本CUSUM计算")
    print("=" * 60)
    
    # 模拟生产数据：稳定在100左右
    stable_data = [100, 101, 99, 100, 100, 101, 99, 100, 100, 101]
    
    # 计算基本统计
    mean, std = calculate_mean_std(stable_data)
    print(f"\n过程统计:")
    print(f"  • 均值: {mean:.2f}")
    print(f"  • 标准差: {std:.2f}")
    
    # 执行CUSUM分析
    result = standard_cusum(stable_data, target=100, h=5, k=0.5)
    
    print(f"\nCUSUM分析结果:")
    print(f"  • 状态: {'✅ 受控' if not result.has_signal else '⚠️ 失控'}")
    print(f"  • 中心线: {result.center_line}")
    print(f"  • 决策阈值(h): {result.h}")
    print(f"  • 参考值(k): {result.k}")
    
    if result.has_signal:
        print(f"  • 信号类型: {result.signal_type}")
        print(f"  • 信号位置: 第 {result.signal_index} 个数据点")


def example_shift_detection():
    """示例2：过程偏移检测"""
    print("\n" + "=" * 60)
    print("示例2：过程偏移检测")
    print("=" * 60)
    
    # 前10个数据稳定在100，后10个数据偏移到105
    data = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
            105, 106, 104, 105, 107, 105, 106, 104, 105, 106]
    
    print("\n数据序列:")
    print(f"  前10个值: {data[:10]}")
    print(f"  后10个值: {data[10:]}")
    
    # 执行CUSUM分析
    result = standard_cusum(data, target=100, h=10, k=1)
    
    print(f"\n检测结果:")
    print(f"  • 状态: {'⚠️ 检测到偏移!' if result.has_signal else '✅ 未检测到偏移'}")
    
    if result.has_signal:
        print(f"  • 信号位置: 第 {result.signal_index} 个数据点")
        print(f"  • 变化点估计: 第 {result.change_point} 个数据点")
        print(f"  • 估计偏移量: {result.estimated_shift:.2f}")
        
    # 打印完整报告
    print("\n详细报告:")
    print(format_cusum_report(result))


def example_parameter_design():
    """示例3：CUSUM参数设计"""
    print("\n" + "=" * 60)
    print("示例3：CUSUM参数设计")
    print("=" * 60)
    
    print("\n设计场景:")
    print("  • 目标：检测1个标准差的偏移")
    print("  • 要求：受控状态下平均运行500个样本才发出信号")
    
    # 设计CUSUM参数
    h, k = design_cusum(target_arl_0=500, delta_to_detect=1.0)
    
    print(f"\n设计结果:")
    print(f"  • 决策阈值(h): {h}")
    print(f"  • 参考值(k): {k}")
    
    # 不同ARL需求的设计对比
    print("\n不同ARL需求的设计对比:")
    for arl in [100, 500, 1000, 2000]:
        h, k = design_cusum(target_arl_0=arl, delta_to_detect=1.0)
        print(f"  • ARL={arl}: h={h}, k={k}")
    
    # 不同检测偏移的设计对比
    print("\n不同检测偏移的设计对比:")
    for delta in [0.5, 1.0, 1.5, 2.0]:
        h, k = design_cusum(target_arl_0=500, delta_to_detect=delta)
        print(f"  • 检测{delta}σ偏移: h={h}, k={k}")


def example_real_time_monitoring():
    """示例4：实时过程监控"""
    print("\n" + "=" * 60)
    print("示例4：实时过程监控")
    print("=" * 60)
    
    # 创建监控器（目标值100，标准差2）
    monitor = CUSUMMonitor(target=100, std=2, h=10, k=1)
    
    print("\n模拟生产过程监控...")
    print("  阶段1：正常运行（均值100）")
    
    random.seed(42)
    
    # 正常运行阶段
    normal_values = []
    for i in range(20):
        value = random.gauss(100, 2)
        normal_values.append(round(value, 1))
        signal = monitor.update(value)
        
        if i % 5 == 4:
            stats = monitor.get_statistics()
            print(f"    第{i+1}次检查: 当前值={value:.1f}, "
                  f"C+={stats['max_cusum_pos']:.2f}")
    
    print("\n  阶段2：偏移发生（均值提升到105）")
    
    # 偏移阶段
    for i in range(20):
        value = random.gauss(105, 2)
        signal = monitor.update(value)
        
        if signal:
            print(f"    ⚠️ 第{i+1}次检查: 检测到偏移信号!")
            print(f"    信号类型: {monitor.get_signal_type()}")
            print(f"    信号位置: 第 {monitor.get_signal_index()} 个数据点")
            break
        
        if i % 5 == 4:
            stats = monitor.get_statistics()
            print(f"    第{i+1}次检查: 当前值={value:.1f}, "
                  f"C+={stats['max_cusum_pos']:.2f}")
    
    print("\n监控统计信息:")
    stats = monitor.get_statistics()
    print(f"  • 总样本数: {stats['n']}")
    print(f"  • 样本均值: {stats['mean']:.2f}")
    print(f"  • 样本标准差: {stats['std']:.2f}")
    print(f"  • 最大正向CUSUM: {stats['max_cusum_pos']:.2f}")


def example_tabular_cusum():
    """示例5：表格形式CUSUM"""
    print("\n" + "=" * 60)
    print("示例5：表格形式CUSUM（便于可视化）")
    print("=" * 60)
    
    # 制造数据
    data = [100] * 10 + [110, 112, 115, 118, 120]
    
    print(f"\n数据序列: 前10个=100，后5个逐渐增加")
    
    # 计算表格CUSUM
    result = tabular_cusum(data, target=100, h=15, k=1)
    
    print("\n表格CUSUM结果:")
    print(f"{'序号':<6} {'观测值':<10} {'C+':<10} {'C-':<10} {'状态':<10}")
    
    for i in range(len(data)):
        c_pos = result['c_positive'][i]
        c_neg = result['c_negative'][i]
        status = '正常'
        
        if c_pos >= result['h']:
            status = '⚠️ 上限'
        elif c_neg <= -result['h']:
            status = '⚠️ 下限'
        
        print(f"{i:<6} {data[i]:<10.1f} {c_pos:<10.2f} {c_neg:<10.2f} {status:<10}")
    
    print(f"\n信号检测: {'有信号' if result['has_signal'] else '无信号'}")


def example_change_points():
    """示例6：多变化点检测"""
    print("\n" + "=" * 60)
    print("示例6：多变化点检测")
    print("=" * 60)
    
    # 创建包含多个变化点的数据
    random.seed(123)
    
    # 三段数据：均值10 → 均值15 → 均值12
    segment1 = [random.gauss(10, 0.5) for _ in range(20)]
    segment2 = [random.gauss(15, 0.5) for _ in range(20)]
    segment3 = [random.gauss(12, 0.5) for _ in range(20)]
    
    data = segment1 + segment2 + segment3
    
    print(f"\n数据构成:")
    print(f"  • 第1段 (0-19): 均值约10")
    print(f"  • 第2段 (20-39): 均值约15")
    print(f"  • 第3段 (40-59): 均值约12")
    
    # 检测变化点
    changes = detect_change_points(data, min_segment_size=10)
    
    print(f"\n检测结果: 找到 {len(changes)} 个变化点")
    
    for i, cp in enumerate(changes):
        print(f"\n  变化点 #{i+1}:")
        print(f"    • 位置: 第 {cp.index} 个数据点")
        print(f"    • 方向: {cp.direction}")
        print(f"    • 幅度: {cp.magnitude:.2f}")
        print(f"    • 置信度: {cp.confidence:.2f}")
        print(f"    • 之前均值: {cp.before_mean:.2f}")
        print(f"    • 之后均值: {cp.after_mean:.2f}")


def example_proportion_cusum():
    """示例7：比例CUSUM（良品率监控）"""
    print("\n" + "=" * 60)
    print("示例7：比例CUSUM（良品率监控）")
    print("=" * 60)
    
    print("\n场景：生产线良品率监控")
    print("  • 目标良品率: 98%")
    
    # 模拟不同情况的检测
    test_cases = [
        ("正常批次", 98, 100),
        ("轻微下降", 95, 100),
        ("严重下降", 90, 100),
        ("优秀批次", 99, 100),
    ]
    
    print("\n检测结果:")
    print(f"{'批次':<12} {'良品数':<10} {'良品率':<10} {'信号':<10}")
    
    for name, successes, trials in test_cases:
        result = cusum_for_proportion(successes, trials, target_p=0.98)
        
        signal = "⚠️ 有信号" if result['has_signal'] else "✅ 正常"
        
        print(f"{name:<12} {successes:<10} {result['proportion']*100:.1f}%  {signal:<10}")


def example_variance_cusum():
    """示例8：方差CUSUM（波动性监控）"""
    print("\n" + "=" * 60)
    print("示例8：方差CUSUM（波动性监控）")
    print("=" * 60)
    
    print("\n场景：金融收益率波动性监控")
    
    # 创建数据：稳定方差 → 高方差
    random.seed(456)
    
    stable = [random.gauss(0, 1) for _ in range(30)]
    volatile = [random.gauss(0, 3) for _ in range(30)]
    
    data = stable + volatile
    
    print(f"  • 前30个数据: 标准差≈1 (稳定)")
    print(f"  • 后30个数据: 标准差≈3 (高波动)")
    
    # 方差CUSUM
    result = cusum_for_variance(data)
    
    print(f"\n检测结果:")
    print(f"  • 目标方差: {result['target_variance']:.2f}")
    print(f"  • 决策阈值: {result['h']:.2f}")
    print(f"  • 是否检测到方差变化: {'是' if result['has_signal'] else '否'}")
    
    if result['signals']:
        print(f"  • 信号位置: {result['signals']}")


def example_ewma_cusum():
    """示例9：EWMA-CUSUM混合方法"""
    print("\n" + "=" * 60)
    print("示例9：EWMA-CUSUM混合方法")
    print("=" * 60)
    
    print("\nEWMA平滑系数的作用:")
    print("  • 较小的lambda: 更平滑，反应慢")
    print("  • 较大的lambda: 反应快，噪声敏感")
    
    # 创建测试数据
    data = [100] * 5 + [105, 106, 107, 108, 109]
    
    # 测试不同lambda
    print("\n不同lambda的EWMA值:")
    for lambda_val in [0.1, 0.2, 0.5]:
        result = ewma_cusum(data, lambda_=lambda_val, target=100)
        ewma_final = result['ewma_values'][-1]
        print(f"  lambda={lambda_val}: 最终EWMA={ewma_final:.2f}")
    
    print("\n完整EWMA-CUSUM分析(lambda=0.2):")
    result = ewma_cusum(data, lambda_=0.2, target=100)
    
    print(f"\n{'序号':<6} {'观测值':<10} {'EWMA':<10} {'C+':<10}")
    for i in range(len(data)):
        print(f"{i:<6} {data[i]:<10.1f} {result['ewma_values'][i]:<10.2f} "
              f"{result['cusum_positive'][i]:<10.2f}")
    
    print(f"\n是否检测到偏移: {'是' if result['has_signal'] else '否'}")


def example_process_analysis():
    """示例10：全面过程分析"""
    print("\n" + "=" * 60)
    print("示例10：全面过程分析")
    print("=" * 60)
    
    # 创建真实生产数据模拟
    random.seed(789)
    
    # 稳定运行30个样本，然后偏移+2σ
    stable = [random.gauss(100, 2) for _ in range(30)]
    shifted = [random.gauss(104, 2) for _ in range(30)]
    
    data = stable + shifted
    
    print(f"\n数据概况:")
    print(f"  • 总样本数: {len(data)}")
    print(f"  • 前30个样本均值约100")
    print(f"  • 后30个样本均值约104")
    
    # 全面分析
    analysis = analyze_process(data)
    
    print("\n分析结果:")
    
    # 基本统计
    stats = analysis['statistics']
    print(f"\n  基本统计:")
    print(f"    • 均值: {stats['mean']:.2f}")
    print(f"    • 标准差: {stats['std']:.2f}")
    print(f"    • 最小值: {stats['min']:.2f}")
    print(f"    • 最大值: {stats['max']:.2f}")
    
    # CUSUM结果
    cusum = analysis['cusum']
    print(f"\n  CUSUM分析:")
    print(f"    • 状态: {analysis['status']}")
    print(f"    • 信号类型: {cusum['signal_type'] or '无信号'}")
    if cusum['change_point']:
        print(f"    • 变化点: 第 {cusum['change_point']} 个样本")
        print(f"    • 估计偏移: {cusum['estimated_shift']:.2f}")
    
    # 过程能力
    capability = analysis['process_capability']
    print(f"\n  过程能力:")
    print(f"    • Cp: {capability['cp']:.3f}")
    print(f"    • Cpk: {capability['cpk']:.3f}")
    print(f"    • 规格上限: {capability['usl']:.2f}")
    print(f"    • 规格下限: {capability['lsl']:.2f}")
    
    # 趋势分析
    trend = analysis['trend']
    print(f"\n  趋势分析:")
    print(f"    • 方向: {trend['direction']}")
    print(f"    • 斜率: {trend['slope']:.4f}")
    print(f"    • R²: {trend['r_squared']:.4f}")
    
    # 变化点
    changes = analysis['change_points']
    if changes:
        print(f"\n  变化点检测:")
        for cp in changes:
            print(f"    • 位置 {cp['index']}: 方向={cp['direction']}, "
                  f"幅度={cp['magnitude']:.2f}, 置信度={cp['confidence']:.2f}")


def example_cusum_scoring():
    """示例11：CUSUM异常评分"""
    print("\n" + "=" * 60)
    print("示例11：CUSUM异常评分")
    print("=" * 60)
    
    # 创建数据序列
    data = [10, 10, 10, 10, 10, 12, 14, 16, 18, 20]
    
    # 计算CUSUM得分
    scores = cusum_score(data)
    
    print("\n数据与CUSUM得分:")
    print(f"{'序号':<6} {'观测值':<10} {'CUSUM得分':<10} {'异常程度':<12}")
    
    for i in range(len(data)):
        anomaly = "正常"
        if scores[i] > 0.7:
            anomaly = "⚠️ 高异常"
        elif scores[i] > 0.4:
            anomaly = "中度异常"
        elif scores[i] > 0.1:
            anomaly = "轻微异常"
        
        print(f"{i:<6} {data[i]:<10.1f} {scores[i]:<10.2f} {anomaly:<12}")
    
    print("\n得分越高表示越偏离稳定状态")


def example_standardized_cusum():
    """示例12：标准化CUSUM"""
    print("\n" + "=" * 60)
    print("示例12：标准化CUSUM（对尺度不敏感）")
    print("=" * 60)
    
    print("\n标准化CUSUM的优点:")
    print("  • 使用标准化的z值，对不同尺度的数据都适用")
    print("  • 参数设置基于ARL理论，有统一标准")
    
    # 创建不同尺度的数据
    small_scale = [10, 10, 11, 10, 15, 16, 17, 18]
    large_scale = [1000, 1000, 1010, 1000, 1050, 1060, 1070, 1080]
    
    print("\n对比分析:")
    
    # 小尺度数据
    result_small = standardized_cusum(small_scale)
    print(f"\n  小尺度数据 (均值≈10):")
    print(f"    • 原始均值: {result_small.center_line:.2f}")
    print(f"    • 参数: h={result_small.h}, k={result_small.k}")
    print(f"    • 检测到信号: {'是' if result_small.has_signal else '否'}")
    
    # 大尺度数据
    result_large = standardized_cusum(large_scale)
    print(f"\n  大尺度数据 (均值≈1000):")
    print(f"    • 原始均值: {result_large.center_line:.2f}")
    print(f"    • 参数: h={result_large.h}, k={result_large.k}")
    print(f"    • 检测到信号: {'是' if result_large.has_signal else '否'}")
    
    print("\n结论: 相同的相对偏移(约50%)产生相似的检测结果")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("CUSUM控制图工具模块使用示例")
    print("=" * 60)
    
    example_basic_cusum()
    example_shift_detection()
    example_parameter_design()
    example_real_time_monitoring()
    example_tabular_cusum()
    example_change_points()
    example_proportion_cusum()
    example_variance_cusum()
    example_ewma_cusum()
    example_process_analysis()
    example_cusum_scoring()
    example_standardized_cusum()
    
    print("\n" + "=" * 60)
    print("示例演示完成!")
    print("=" * 60)
    print("\nCUSUM控制图应用场景:")
    print("  • 制造业: 产品尺寸、重量、成分监控")
    print("  • 金融: 收益率、波动性异常检测")
    print("  • 医疗: 生命体征、治疗效果监控")
    print("  • 网络: 流量异常、性能监控")
    print("  • 环境: 气温、水质、空气质量监测")
    print("\n提示: 使用 CUSUMMonitor 类可实现实时数据流监控")


if __name__ == '__main__':
    main()