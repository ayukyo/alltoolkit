#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - BMI Utilities Examples
====================================
Practical usage examples for the bmi_utils module.

Author: AllToolkit Contributors
License: MIT
"""

import sys
import os

# Add module path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from bmi_utils.mod import (
    calculate_bmi,
    calculate_full_bmi,
    get_bmi_category_info,
    calculate_bmi_prime,
    calculate_ideal_weight_range,
    estimate_full_body_fat,
    calculate_child_full_bmi,
    calculate_full_bmr,
    calculate_waist_height_ratio,
    get_waist_height_category,
    calculate_weight_recommendation,
    convert_weight,
    convert_height,
    get_bmi_summary,
    UnitSystem,
    Gender,
)


def example_basic_bmi():
    """基础 BMI 计算示例"""
    print("\n" + "=" * 60)
    print("示例 1: 基础 BMI 计算")
    print("=" * 60)
    
    # 使用 metric 单位
    weight_kg = 70
    height_m = 1.75
    
    bmi = calculate_bmi(weight_kg, height_m)
    print(f"\n体重: {weight_kg} kg, 身高: {height_m} m")
    print(f"BMI: {bmi}")
    
    # 使用 imperial 单位
    weight_lb = 154
    height_ft = 5
    height_in = 10
    
    bmi_imperial = calculate_bmi(weight_lb, height_ft, UnitSystem.IMPERIAL, height_in)
    print(f"\n体重: {weight_lb} lb, 身高: {height_ft}'{height_in}\"")
    print(f"BMI: {bmi_imperial}")


def example_full_bmi_analysis():
    """完整 BMI 分析示例"""
    print("\n" + "=" * 60)
    print("示例 2: 完整 BMI 分析")
    print("=" * 60)
    
    # 不同体重状况的对比
    test_cases = [
        (50, 1.75, "偏瘦"),
        (70, 1.75, "正常"),
        (85, 1.75, "超重"),
        (100, 1.75, "肥胖"),
    ]
    
    print("\n身高 1.75m 的不同体重分析:")
    print("-" * 50)
    
    for weight, height, desc in test_cases:
        result = calculate_full_bmi(weight, height)
        print(f"\n{desc} ({weight}kg):")
        print(f"  BMI: {result.bmi}")
        print(f"  分类: {result.category_label} ({result.category_label_en})")
        print(f"  风险等级: {result.risk_level}")
        print(f"  BMI Prime: {result.bmi_prime}")
        print(f"  理想体重范围: {result.ideal_weight_min}-{result.ideal_weight_max} kg")
        
        if result.weight_difference > 0:
            print(f"  建议: 需要减重 {result.weight_difference} kg")
        elif result.weight_difference < 0:
            print(f"  建议: 需要增重 {abs(result.weight_difference)} kg")


def example_body_fat_estimation():
    """体脂率估算示例"""
    print("\n" + "=" * 60)
    print("示例 3: 体脂率估算")
    print("=" * 60)
    
    # 不同年龄和性别
    test_profiles = [
        (25, 22, Gender.MALE, 25),
        (35, 25, Gender.MALE, 35),
        (25, 22, Gender.FEMALE, 25),
        (35, 28, Gender.FEMALE, 40),
    ]
    
    print("\n不同人群的体脂率估算:")
    print("-" * 50)
    
    for bmi, age, gender, expected in test_profiles:
        result = estimate_full_body_fat(bmi, age, gender)
        gender_str = "男性" if gender == Gender.MALE else "女性"
        print(f"\n{gender_str}, {age}岁, BMI {bmi}:")
        print(f"  估算体脂率: {result.body_fat_percent}%")
        print(f"  分类: {result.category_label}")
        print(f"  健康范围: {result.healthy_range[0]}-{result.healthy_range[1]}%")
        
        if result.body_fat_percent < result.healthy_range[0]:
            print(f"  提示: 体脂偏低")
        elif result.body_fat_percent > result.healthy_range[1]:
            print(f"  提示: 体脂偏高，建议减脂")


def example_child_bmi():
    """儿童 BMI 计算示例"""
    print("\n" + "=" * 60)
    print("示例 4: 儿童 BMI 计算")
    print("=" * 60)
    
    # 不同年龄儿童
    children = [
        (20, 1.10, 8, Gender.MALE),
        (25, 1.20, 9, Gender.MALE),
        (35, 1.40, 10, Gender.MALE),
        (40, 1.50, 12, Gender.FEMALE),
        (55, 1.65, 15, Gender.FEMALE),
    ]
    
    print("\n儿童 BMI 百分位数分析:")
    print("-" * 50)
    
    for weight, height, age, gender in children:
        result = calculate_child_full_bmi(weight, height, age, gender)
        gender_str = "男孩" if gender == Gender.MALE else "女孩"
        print(f"\n{age}岁{gender_str}, {weight}kg, {height}m:")
        print(f"  BMI: {result.bmi}")
        print(f"  百分位数: {result.percentile}%")
        print(f"  分类: {result.percentile_category_label}")
        print(f"  理想体重范围: {result.ideal_weight_range[0]}-{result.ideal_weight_range[1]} kg")


def example_bmr_tdee():
    """基础代谢率和 TDEE 示例"""
    print("\n" + "=" * 60)
    print("示例 5: 基础代谢率和总能量消耗")
    print("=" * 60)
    
    # 不同活动水平
    activity_levels = [
        ('sedentary', '久坐 (办公室工作)'),
        ('light', '轻度活动 (每周1-3天运动)'),
        ('moderate', '中度活动 (每周3-5天运动)'),
        ('active', '高度活动 (每周6-7天运动)'),
        ('very_active', '非常活跃 (体力劳动/每天两次训练)'),
    ]
    
    print("\n30岁男性, 70kg, 175cm 的能量需求:")
    print("-" * 50)
    
    base_bmr = calculate_full_bmr(70, 1.75, 30, Gender.MALE, 'sedentary')
    print(f"\n基础代谢率 (BMR): {base_bmr.bmr} kcal/day")
    
    for level, desc in activity_levels:
        result = calculate_full_bmr(70, 1.75, 30, Gender.MALE, level)
        print(f"\n{desc}:")
        print(f"  TDEE: {result.tdee} kcal/day")
        print(f"  维持当前体重所需热量: {result.tdee} kcal/day")
        print(f"  减重 (-500 kcal/day): {result.tdee - 500} kcal/day")
        print(f"  增重 (+500 kcal/day): {result.tdee + 500} kcal/day")


def example_waist_height_ratio():
    """腰围身高比示例"""
    print("\n" + "=" * 60)
    print("示例 6: 腰围身高比分析")
    print("=" * 60)
    
    waist_height_cases = [
        (70, 175, Gender.MALE),
        (85, 175, Gender.MALE),
        (95, 175, Gender.MALE),
        (105, 175, Gender.MALE),
    ]
    
    print("\n身高 175cm 的不同腰围分析:")
    print("-" * 50)
    
    for waist, height, gender in waist_height_cases:
        ratio = calculate_waist_height_ratio(waist, height)
        category, label, advice = get_waist_height_category(ratio, gender)
        
        print(f"\n腰围 {waist}cm:")
        print(f"  WHtR: {ratio}")
        print(f"  分类: {label}")
        print(f"  建议: {advice}")


def example_weight_recommendation():
    """减重建议示例"""
    print("\n" + "=" * 60)
    print("示例 7: 减重/增重建议")
    print("=" * 60)
    
    cases = [
        (85, 1.75, "超重"),
        (95, 1.75, "肥胖"),
        (55, 1.75, "偏瘦"),
    ]
    
    print("\n身高 175cm 的体重管理建议:")
    print("-" * 50)
    
    for weight, height, status in cases:
        rec = calculate_weight_recommendation(weight, height, timeframe_weeks=12)
        
        print(f"\n{status} ({weight}kg):")
        print(f"  目标体重: {rec['target_weight']}kg")
        print(f"  需要{rec['recommendation']}: {abs(rec['weight_change'])}kg")
        print(f"  12周计划，每周变化: {abs(rec['weekly_change'])}kg")
        print(f"  速率健康: {'是' if rec['is_healthy_rate'] else '否，建议延长时间'}")


def example_unit_conversion():
    """单位转换示例"""
    print("\n" + "=" * 60)
    print("示例 8: 单位转换")
    print("=" * 60)
    
    # 体重转换
    print("\n体重转换:")
    print("-" * 50)
    kg = 70
    lb = convert_weight(kg, UnitSystem.METRIC, UnitSystem.IMPERIAL)
    print(f"{kg} kg = {lb} lb")
    
    lb_back = 154.32
    kg_back = convert_weight(lb_back, UnitSystem.IMPERIAL, UnitSystem.METRIC)
    print(f"{lb_back} lb = {kg_back} kg")
    
    # 身高转换
    print("\n身高转换:")
    print("-" * 50)
    m = 1.75
    ft, in_ = convert_height(m, UnitSystem.METRIC, UnitSystem.IMPERIAL)
    print(f"{m} m = {ft}'{in_}\"")
    
    ft, in_ = 5, 10
    m_back = convert_height(ft, UnitSystem.IMPERIAL, UnitSystem.METRIC, in_)
    print(f"{ft}'{in_}\" = {m_back} m")


def example_bmi_summary():
    """BMI 概要示例"""
    print("\n" + "=" * 60)
    print("示例 9: BMI 快速概要")
    print("=" * 60)
    
    bmis = [16, 18, 22, 28, 35]
    
    print("\n不同 BMI 的快速概要:")
    print("-" * 50)
    
    for bmi in bmis:
        summary = get_bmi_summary(bmi)
        print(f"BMI {bmi}: {summary}")


def example_real_world_scenario():
    """真实场景示例"""
    print("\n" + "=" * 60)
    print("示例 10: 综合健康评估")
    print("=" * 60)
    
    # 用户输入
    name = "张三"
    weight = 85
    height = 1.75
    age = 35
    gender = Gender.MALE
    waist = 92
    activity = 'moderate'
    
    print(f"\n{age}岁{gender == Gender.MALE and '男性' or '女性'} {name} 的健康报告:")
    print("=" * 50)
    
    # BMI 分析
    bmi_result = calculate_full_bmi(weight, height)
    print(f"\n【体重分析】")
    print(f"  当前体重: {weight} kg")
    print(f"  BMI: {bmi_result.bmi} ({bmi_result.category_label})")
    print(f"  理想范围: {bmi_result.ideal_weight_min}-{bmi_result.ideal_weight_max} kg")
    print(f"  需减重: {abs(bmi_result.weight_difference)} kg")
    
    # 体脂估算
    fat_result = estimate_full_body_fat(bmi_result.bmi, age, gender)
    print(f"\n【体脂分析】")
    print(f"  估算体脂率: {fat_result.body_fat_percent}%")
    print(f"  分类: {fat_result.category_label}")
    print(f"  健康范围: {fat_result.healthy_range[0]}-{fat_result.healthy_range[1]}%")
    
    # 腰围身高比
    whtr = calculate_waist_height_ratio(waist, height * 100)
    whtr_cat, whtr_label, whtr_advice = get_waist_height_category(whtr, gender)
    print(f"\n【腰围分析】")
    print(f"  腰围: {waist} cm")
    print(f"  WHtR: {whtr}")
    print(f"  评估: {whtr_label}")
    
    # 能量需求
    bmr_result = calculate_full_bmr(weight, height, age, gender, activity)
    print(f"\n【能量需求】")
    print(f"  BMR: {bmr_result.bmr} kcal/day")
    print(f"  TDEE: {bmr_result.tdee} kcal/day")
    print(f"  减重建议热量: {bmr_result.tdee - 500} kcal/day")
    
    # 减重建议
    rec = calculate_weight_recommendation(weight, height, timeframe_weeks=16)
    print(f"\n【减重计划】")
    print(f"  目标体重: {rec['target_weight']} kg")
    print(f"  总减重: {abs(rec['weight_change'])} kg")
    print(f"  16周计划，每周减重: {abs(rec['weekly_change'])} kg")
    
    print("\n" + "=" * 50)
    print("综合建议:")
    print("  1. 将每日热量控制在 {} kcal 左右".format(bmr_result.tdee - 500))
    print("  2. 每周运动 3-5 次，每次 30-60 分钟")
    print("  3. 增加蛋白质摄入，减少精制碳水")
    print("  4. 定期监测体重和腰围变化")


def main():
    """运行所有示例"""
    example_basic_bmi()
    example_full_bmi_analysis()
    example_body_fat_estimation()
    example_child_bmi()
    example_bmr_tdee()
    example_waist_height_ratio()
    example_weight_recommendation()
    example_unit_conversion()
    example_bmi_summary()
    example_real_world_scenario()
    
    print("\n" + "=" * 60)
    print("所有示例完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()