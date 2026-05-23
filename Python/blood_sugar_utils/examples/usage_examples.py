"""
Blood Sugar Utils 使用示例

展示血糖工具的主要功能。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from blood_sugar_utils.mod import (
    GlucoseUnit,
    convert_glucose, assess_glucose,
    hba1c_to_average_glucose, average_glucose_to_hba1c,
    estimate_average_glucose, analyze_glucose_trend,
    calculate_insulin_sensitivity, carbohydrate_to_insulin,
    glucose_report,
    mgdl_to_mmol, mmol_to_mgdl
)


def example_unit_conversion():
    """示例：血糖单位转换"""
    print("\n=== 1. 血糖单位转换 ===")
    
    # mg/dL 转 mmol/L
    mgdl_value = 100
    mmol_value = mgdl_to_mmol(mgdl_value)
    print(f"{mgdl_value} mg/dL = {mmol_value} mmol/L")
    
    # mmol/L 转 mg/dL
    mmol_value = 7.8
    mgdl_value = mmol_to_mgdl(mmol_value)
    print(f"{mmol_value} mmol/L = {mgdl_value} mg/dL")
    
    # 使用通用转换函数
    value = 140
    converted = convert_glucose(value, GlucoseUnit.MG_DL, GlucoseUnit.MMOL_L)
    print(f"{value} mg/dL -> {converted} mmol/L")


def example_glucose_assessment():
    """示例：血糖状态评估"""
    print("\n=== 2. 血糖状态评估 ===")
    
    # 空腹血糖评估
    fasting_results = [
        (5.5, "正常人"),
        (6.2, "糖尿病前期患者"),
        (7.5, "糖尿病患者"),
        (3.2, "低血糖情况"),
    ]
    
    print("\n空腹血糖评估:")
    for value, description in fasting_results:
        result = assess_glucose(value, GlucoseUnit.MMOL_L, fasting=True)
        print(f"  {description} ({value} mmol/L): {result['status']}")
        print(f"    风险等级: {result['risk_level']}")
        print(f"    建议: {result['recommendation']}")
    
    # 餐后血糖评估
    print("\n餐后血糖评估:")
    post_meal_values = [6.5, 8.5, 11.5]
    for value in post_meal_values:
        result = assess_glucose(value, GlucoseUnit.MMOL_L, fasting=False)
        print(f"  {value} mmol/L: {result['status']}")


def example_hba1c_conversion():
    """示例：HbA1c 与平均血糖转换"""
    print("\n=== 3. HbA1c 与平均血糖转换 ===")
    
    # HbA1c 转平均血糖
    hba1c_values = [5.5, 6.0, 6.5, 7.0, 8.0]
    print("\nHbA1c -> 平均血糖:")
    for hba1c in hba1c_values:
        result = hba1c_to_average_glucose(hba1c)
        print(f"  HbA1c {hba1c}%:")
        print(f"    平均血糖: {result['avg_glucose_mmol']} mmol/L ({result['avg_glucose_mgdl']} mg/dL)")
        print(f"    状态: {result['status']}")
    
    # 平均血糖转 HbA1c
    avg_glucose = 8.5  # mmol/L
    result = average_glucose_to_hba1c(avg_glucose, GlucoseUnit.MMOL_L)
    print(f"\n平均血糖 {avg_glucose} mmol/L -> HbA1c {result['hba1c']}%")


def example_average_glucose():
    """示例：平均血糖估算"""
    print("\n=== 4. 多次读数平均血糖估算 ===")
    
    # 模拟一周血糖读数
    readings = [
        (5.2, GlucoseUnit.MMOL_L),
        (5.8, GlucoseUnit.MMOL_L),
        (6.1, GlucoseUnit.MMOL_L),
        (5.5, GlucoseUnit.MMOL_L),
        (6.3, GlucoseUnit.MMOL_L),
        (5.9, GlucoseUnit.MMOL_L),
        (5.7, GlucoseUnit.MMOL_L),
    ]
    
    result = estimate_average_glucose(readings)
    print(f"读数数量: {result['count']}")
    print(f"平均血糖: {result['avg_mmol']} mmol/L ({result['avg_mgdl']} mg/dL)")
    print(f"标准差: {result['std_dev_mmol']} mmol/L")
    print(f"变异系数: {result['cv_percent']}%")
    print(f"血糖波动程度: {result['glucose_variability']}")
    print(f"目标范围内时间: {result['time_in_range_percent']}%")
    print(f"估算 HbA1c: {result['estimated_hba1c']}% ({result['hba1c_status']})")


def example_trend_analysis():
    """示例：血糖趋势分析"""
    print("\n=== 5. 血糖趋势分析 ===")
    
    # 模拟连续血糖监测数据（上升趋势）
    now = datetime.now()
    rising_readings = [
        (5.5, GlucoseUnit.MMOL_L, now - timedelta(hours=3)),
        (6.0, GlucoseUnit.MMOL_L, now - timedelta(hours=2)),
        (6.5, GlucoseUnit.MMOL_L, now - timedelta(hours=1)),
        (7.0, GlucoseUnit.MMOL_L, now),
    ]
    
    result = analyze_glucose_trend(rising_readings)
    print(f"趋势: {result['trend']} {result['trend_arrow']}")
    print(f"变化速度: {result['slope_mmol_per_hour']} mmol/L/小时")
    print(f"当前血糖: {result['current_mmol']} mmol/L")
    print(f"预测下一小时: {result['predicted_next_mmol']} mmol/L ({result['predicted_status']})")
    
    # 下降趋势示例
    falling_readings = [
        (8.5, GlucoseUnit.MMOL_L, now - timedelta(hours=3)),
        (7.5, GlucoseUnit.MMOL_L, now - timedelta(hours=2)),
        (6.5, GlucoseUnit.MMOL_L, now - timedelta(hours=1)),
        (5.5, GlucoseUnit.MMOL_L, now),
    ]
    
    result = analyze_glucose_trend(falling_readings)
    print(f"\n下降趋势: {result['trend']} {result['trend_arrow']}")
    print(f"变化速度: {result['slope_mmol_per_hour']} mmol/L/小时")


def example_insulin_calculation():
    """示例：胰岛素剂量计算"""
    print("\n=== 6. 胰岛素剂量计算 ===")
    
    # 校正剂量计算
    print("\n校正剂量计算:")
    result = calculate_insulin_sensitivity(
        current_glucose=10.0,  # 当前血糖
        target_glucose=6.0,    # 目标血糖
        correction_factor=2.0, # ISF（每单位胰岛素降血糖2 mmol/L）
        unit=GlucoseUnit.MMOL_L
    )
    print(f"  当前血糖: {result['current_mmol']} mmol/L")
    print(f"  目标血糖: {result['target_mmol']} mmol/L")
    print(f"  需降血糖: {result['glucose_difference_mmol']} mmol/L")
    print(f"  校正剂量: {result['correction_units']} 单位")
    
    # 餐时胰岛素计算
    print("\n餐时胰岛素计算:")
    result = carbohydrate_to_insulin(
        carbs=60,  # 60克碳水
        icr=10     # 1:10 比例（每单位胰岛素处理10克碳水）
    )
    print(f"  碳水摄入: {result['carbs_grams']} 克")
    print(f"  ICR: {result['icr']} (1单位胰岛素处理 {result['icr']} 克碳水)")
    print(f"  餐时剂量: {result['carb_units']} 单位")
    print(f"  {result['recommendation']}")
    
    # 综合：餐时 + 校正
    print("\n综合计算（餐时 + 校正）:")
    result = carbohydrate_to_insulin(
        carbs=60, icr=10,
        current_glucose=10.0, target_glucose=6.0, isf=2.0,
        unit=GlucoseUnit.MMOL_L
    )
    print(f"  餐时剂量: {result['carb_units']} 单位")
    print(f"  校正剂量: {result['correction_units']} 单位")
    print(f"  总剂量: {result['total_units']} 单位")
    print(f"  {result['recommendation']}")


def example_glucose_report():
    """示例：完整血糖报告"""
    print("\n=== 7. 血糖报告生成 ===")
    
    # 模拟一天血糖数据
    now = datetime.now()
    readings = [
        # 早餐前
        (5.5, GlucoseUnit.MMOL_L, now - timedelta(hours=12)),
        # 早餐后
        (7.2, GlucoseUnit.MMOL_L, now - timedelta(hours=10)),
        # 午餐前
        (5.8, GlucoseUnit.MMOL_L, now - timedelta(hours=8)),
        # 午餐后
        (8.5, GlucoseUnit.MMOL_L, now - timedelta(hours=6)),
        # 下午
        (6.2, GlucoseUnit.MMOL_L, now - timedelta(hours=4)),
        # 晚餐前
        (5.6, GlucoseUnit.MMOL_L, now - timedelta(hours=2)),
        # 晚餐后
        (7.8, GlucoseUnit.MMOL_L, now),
    ]
    
    report = glucose_report(readings)
    
    print("\n摘要:")
    summary = report['summary']
    print(f"  总读数: {summary['total_readings']}")
    print(f"  时间跨度: {summary['time_span_hours']} 小时")
    
    print("\n统计数据:")
    stats = report['statistics']
    print(f"  平均血糖: {stats['average_mmol/L']} mmol/L")
    print(f"  最小值: {stats['min_mmol/L']} mmol/L")
    print(f"  最大值: {stats['max_mmol/L']} mmol/L")
    print(f"  波动范围: {stats['range_mmol/L']} mmol/L")
    print(f"  变异系数: {stats['cv_percent']}%")
    
    print("\n目标范围内时间:")
    tir = report['time_in_range']
    print(f"  目标范围: {tir['target_range']}")
    print(f"  在范围内: {tir['in_range_percent']}% ({tir['in_range_count']} 次)")
    print(f"  低于范围: {tir['below_range_percent']}% ({tir['below_range_count']} 次)")
    print(f"  高于范围: {tir['above_range_percent']}% ({tir['above_range_count']} 次)")
    
    print("\nHbA1c 估算:")
    hba1c = report['hba1c_estimate']
    print(f"  估算值: {hba1c['estimated_hba1c']}%")
    print(f"  状态: {hba1c['status']}")
    
    print("\n评估和建议:")
    assessment = report['assessment']
    print(f"  总体评价: {assessment['overall']}")
    for rec in assessment['recommendations']:
        print(f"  - {rec}")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("Blood Sugar Utils - 血糖计算工具使用示例")
    print("=" * 60)
    
    example_unit_conversion()
    example_glucose_assessment()
    example_hba1c_conversion()
    example_average_glucose()
    example_trend_analysis()
    example_insulin_calculation()
    example_glucose_report()
    
    print("\n" + "=" * 60)
    print("示例完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()