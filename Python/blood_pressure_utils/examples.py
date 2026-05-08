#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Blood Pressure Utilities Examples
===============================================
Practical examples demonstrating blood pressure analysis capabilities.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Python.blood_pressure_utils.mod import (
    # Unit conversion
    mmhg_to_kpa, kpa_to_mmhg, BPUnit,
    
    # Core functions
    calculate_pulse_pressure, calculate_map, get_map_status,
    classify_bp, get_pulse_pressure_category,
    get_age_normal_range, is_bp_age_appropriate,
    analyze_bp, BPResult,
    
    # Statistics
    calculate_bp_statistics, analyze_bp_trend,
    
    # Pediatric
    analyze_child_bp, Gender,
    
    # Utility
    get_bp_summary, calculate_hypertension_stage,
)


def example_basic_bp_analysis():
    """示例：基本血压分析"""
    print("\n" + "-" * 50)
    print("示例 1: 基本血压分析")
    print("-" * 50)
    
    # 分析一次血压读数
    result = analyze_bp(120, 80, 35)
    
    print(f"血压: {result.systolic}/{result.diastolic} mmHg")
    print(f"分类: {result.category_label}")
    print(f"风险等级: {result.risk_level}")
    print(f"脉压差: {result.pulse_pressure} mmHg")
    print(f"平均动脉压: {result.map} mmHg")
    print(f"\n健康建议:")
    for rec in result.recommendations:
        print(f"  - {rec}")


def example_high_bp_analysis():
    """示例：高血压分析"""
    print("\n" + "-" * 50)
    print("示例 2: 高血压分析")
    print("-" * 50)
    
    # 分析高血压读数
    result = analyze_bp(155, 95, 50)
    
    print(f"血压: {result.systolic}/{result.diastolic} mmHg")
    print(f"分类: {result.category_label} ({result.category_label_en})")
    print(f"风险: {result.risk_description}")
    print(f"脉压差: {result.pulse_pressure} mmHg - {result.pulse_pressure_label}")
    print(f"\n重要建议:")
    for rec in result.recommendations[:3]:
        print(f"  ⚠ {rec}")


def example_isolated_systolic():
    """示例：单纯收缩期高血压"""
    print("\n" + "-" * 50)
    print("示例 3: 单纯收缩期高血压")
    print("-" * 50)
    
    # 老年人常见：收缩压高但舒张压正常
    result = analyze_bp(150, 80, 70)
    
    print(f"血压: {result.systolic}/{result.diastolic} mmHg")
    print(f"分类: {result.category_label}")
    print(f"脉压差: {result.pulse_pressure} mmHg")
    
    cat, label, desc = get_pulse_pressure_category(result.pulse_pressure)
    print(f"脉压差状态: {label}")
    print(f"说明: {desc}")
    print(f"\n特别提醒:")
    print("  - 单纯收缩期高血压常见于老年人")
    print("  - 脉压差增大提示动脉硬化风险")


def example_bp_statistics():
    """示例：血压统计分析"""
    print("\n" + "-" * 50)
    print("示例 4: 血压统计分析")
    print("-" * 50)
    
    # 一周的血压读数
    week_readings = [
        (120, 80), (118, 78), (122, 82), (119, 79),
        (125, 83), (121, 81), (117, 77)
    ]
    
    stats = calculate_bp_statistics(week_readings)
    
    print(f"统计周期: 7天")
    print(f"读数数量: {stats.readings_count}")
    print(f"\n收缩压:")
    print(f"  平均值: {stats.systolic_mean} mmHg")
    print(f"  范围: {stats.systolic_min} - {stats.systolic_max} mmHg")
    print(f"  标准差: {stats.systolic_std}")
    print(f"\n舒张压:")
    print(f"  平均值: {stats.diastolic_mean} mmHg")
    print(f"  范围: {stats.diastolic_min} - {stats.diastolic_max} mmHg")
    print(f"  标准差: {stats.diastolic_std}")
    print(f"\n其他指标:")
    print(f"  脉压差均值: {stats.pulse_pressure_mean} mmHg")
    print(f"  MAP均值: {stats.map_mean} mmHg")
    print(f"  主要分类: {stats.dominant_category}")
    print(f"  变化趋势: {stats.trend}")


def example_bp_trend():
    """示例：血压趋势分析"""
    print("\n" + "-" * 50)
    print("示例 5: 血压趋势分析")
    print("-" * 50)
    
    # 两周的血压读数（有上升趋势）
    readings = [
        (120, 80), (122, 81), (124, 83),
        (126, 84), (128, 86), (130, 87)
    ]
    
    trend = analyze_bp_trend([(s, d, None) for s, d in readings])
    
    print(f"监测周期: 6次读数")
    print(f"收缩压趋势: {trend['systolic_trend']}")
    print(f"舒张压趋势: {trend['diastolic_trend']}")
    print(f"收缩压变化: {trend['systolic_change']} mmHg")
    print(f"舒张压变化: {trend['diastolic_change']} mmHg")
    
    if trend['systolic_trend'] == 'increasing':
        print("\n⚠ 警告: 血压呈上升趋势，建议关注")


def example_child_bp():
    """示例：儿童血压分析"""
    print("\n" + "-" * 50)
    print("示例 6: 儿童血压分析")
    print("-" * 50)
    
    # 10岁男孩
    result = analyze_child_bp(108, 72, 10, Gender.MALE)
    
    print(f"年龄: 10岁, 性别: 男")
    print(f"血压: {result.systolic}/{result.diastolic} mmHg")
    print(f"百分位数: {result.percentile}%")
    print(f"分类: {result.percentile_label}")
    print(f"风险等级: {result.risk_level}")
    
    # 获取年龄正常范围
    sys_min, sys_max, dia_min, dia_max = get_age_normal_range(10)
    print(f"\n10岁正常范围:")
    print(f"  收缩压: {sys_min}-{sys_max} mmHg")
    print(f"  舒张压: {dia_min}-{dia_max} mmHg")
    
    # 高血压儿童
    high_result = analyze_child_bp(130, 85, 10, Gender.MALE)
    print(f"\n高血压儿童示例:")
    print(f"  血压: {high_result.systolic}/{high_result.diastolic} mmHg")
    print(f"  百分位数: {high_result.percentile}%")
    print(f"  分类: {high_result.percentile_label}")


def example_unit_conversion():
    """示例：单位转换"""
    print("\n" + "-" * 50)
    print("示例 7: 血压单位转换")
    print("-" * 50)
    
    # mmHg 转 kPa
    print("mmHg → kPa:")
    values = [120, 80, 140, 90]
    for v in values:
        print(f"  {v} mmHg = {mmhg_to_kpa(v)} kPa")
    
    # kPa 转 mmHg
    print("\nkPa → mmHg:")
    kpa_values = [16, 10.6, 18.6]
    for v in kpa_values:
        print(f"  {v} kPa = {kpa_to_mmhg(v)} mmHg")


def example_age_ranges():
    """示例：不同年龄血压范围"""
    print("\n" + "-" * 50)
    print("示例 8: 不同年龄正常血压范围")
    print("-" * 50)
    
    ages = [5, 10, 15, 25, 45, 65, 80]
    
    print("年龄   收缩压范围    舒张压范围")
    print("-" * 40)
    for age in ages:
        sys_min, sys_max, dia_min, dia_max = get_age_normal_range(age)
        print(f"{age}岁   {sys_min}-{sys_max}      {dia_min}-{dia_max}")


def example_map_calculation():
    """示例：MAP（平均动脉压）计算"""
    print("\n" + "-" * 50)
    print("示例 9: 平均动脉压(MAP)分析")
    print("-" * 50)
    
    print("MAP是评估器官灌注的重要指标")
    print("公式: MAP = 舒张压 + (收缩压 - 舒张压) / 3")
    print("正常范围: 70-105 mmHg")
    print()
    
    bp_readings = [
        (120, 80, "正常血压"),
        (90, 60, "低血压"),
        (150, 95, "高血压"),
        (180, 100, "严重高血压"),
    ]
    
    for sys, dia, desc in bp_readings:
        map_val = calculate_map(sys, dia)
        status = get_map_status(map_val)
        print(f"{desc} ({sys}/{dia}):")
        print(f"  MAP = {map_val} mmHg - {status}")


def example_hypertension_stages():
    """示例：高血压分期"""
    print("\n" + "-" * 50)
    print("示例 10: 高血压分期（美国标准）")
    print("-" * 50)
    
    readings = [
        (118, 76, "正常"),
        (128, 82, "偏高"),
        (135, 88, "临界高血压"),
        (145, 92, "高血压1期"),
        (165, 105, "高血压2期"),
        (185, 120, "高血压危象"),
    ]
    
    for sys, dia, desc in readings:
        stage = calculate_hypertension_stage(sys, dia)
        print(f"{sys}/{dia} mmHg ({desc}): {stage}")


def example_pulse_pressure_analysis():
    """示例：脉压差分析"""
    print("\n" + "-" * 50)
    print("示例 11: 脉压差临床意义")
    print("-" * 50)
    
    print("脉压差 = 收缩压 - 舒张压")
    print("正常范围: 30-50 mmHg")
    print()
    
    examples = [
        (40, "正常脉压差"),
        (25, "偏低 - 可能心输出量不足"),
        (55, "增大 - 可能动脉硬化"),
        (70, "过高 - 严重动脉硬化风险"),
    ]
    
    for pp, desc in examples:
        cat, label, info = get_pulse_pressure_category(pp)
        print(f"脉压差 {pp} mmHg:")
        print(f"  分类: {label}")
        print(f"  临床意义: {info}")
        print()


def run_all_examples():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("AllToolkit - Blood Pressure Utilities Examples")
    print("=" * 60)
    
    example_basic_bp_analysis()
    example_high_bp_analysis()
    example_isolated_systolic()
    example_bp_statistics()
    example_bp_trend()
    example_child_bp()
    example_unit_conversion()
    example_age_ranges()
    example_map_calculation()
    example_hypertension_stages()
    example_pulse_pressure_analysis()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    run_all_examples()