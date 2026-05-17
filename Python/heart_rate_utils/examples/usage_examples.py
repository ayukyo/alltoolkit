"""
Heart Rate Utils 使用示例

演示心率工具库的主要功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    HeartRateUtils,
    MaxHrFormula,
    calculate_max_hr,
    get_zones,
    get_fat_burning_hr,
    get_current_zone,
    estimate_calories,
    assess_fitness
)


def example_max_hr():
    """最大心率计算示例"""
    print("\n=== 最大心率计算示例 ===\n")
    
    age = 35
    
    # Tanaka公式（推荐）
    print(f"年龄: {age}岁")
    print(f"Tanaka公式最大心率: {HeartRateUtils.calculate_max_hr(age, MaxHrFormula.TANAKA)} bpm")
    
    # 所有公式对比
    print("\n各公式对比:")
    ranges = HeartRateUtils.calculate_max_hr_range(age)
    for formula, value in ranges.items():
        print(f"  {formula}: {value} bpm")
    
    # 不同年龄对比
    print("\n不同年龄最大心率:")
    for age in [20, 30, 40, 50, 60, 70]:
        max_hr = HeartRateUtils.calculate_max_hr(age, MaxHrFormula.TANAKA)
        print(f"  {age}岁: {max_hr} bpm")


def example_zones():
    """心率区间示例"""
    print("\n=== 心率区间示例 ===\n")
    
    age = 30
    resting_hr = 60
    
    # 简单百分比区间
    print(f"年龄: {age}岁, 静息心率: {resting_hr} bpm\n")
    
    result = HeartRateUtils.calculate_zones(age)
    print("心率训练区间（简单百分比）:")
    for zone_name, zone_info in result.zones.items():
        print(f"  {zone_name} ({zone_info.name}): {zone_info.hr_range.min_hr}-{zone_info.hr_range.max_hr} bpm")
        print(f"    描述: {zone_info.description}")
        print(f"    建议: {zone_info.duration_minutes[0]}-{zone_info.duration_minutes[1]}分钟")
    
    # Karvonen区间
    print("\n心率训练区间（Karvonen公式）:")
    result_karvonen = HeartRateUtils.calculate_zones(age, resting_hr, use_karvonen=True)
    print(f"心率储备: {result_karvonen.heart_rate_reserve} bpm")
    for zone_name, zone_info in result_karvonen.zones.items():
        print(f"  {zone_name}: {zone_info.hr_range.min_hr}-{zone_info.hr_range.max_hr} bpm")


def example_fat_burning():
    """燃脂区间示例"""
    print("\n=== 燃脂区间示例 ===\n")
    
    for age in [25, 35, 45, 55]:
        fat_zone = HeartRateUtils.calculate_fat_burning_zone(age)
        print(f"{age}岁:")
        print(f"  燃脂心率: {fat_zone['hr_range']['min']}-{fat_zone['hr_range']['max']} bpm")
        print(f"  最佳心率: {fat_zone['optimal_hr']} bpm")
        print()


def example_calories():
    """卡路里消耗示例"""
    print("\n=== 卡路里消耗示例 ===\n")
    
    scenarios = [
        {"activity": "慢跑", "hr": 130, "duration": 60, "weight": 70, "age": 30, "gender": "male"},
        {"activity": "快跑", "hr": 160, "duration": 30, "weight": 70, "age": 30, "gender": "male"},
        {"activity": "骑行", "hr": 140, "duration": 45, "weight": 65, "age": 28, "gender": "female"},
        {"activity": "游泳", "hr": 150, "duration": 40, "weight": 75, "age": 35, "gender": "male"},
    ]
    
    for scenario in scenarios:
        result = HeartRateUtils.estimate_calories_burned(
            scenario["hr"],
            scenario["duration"],
            scenario["weight"],
            scenario["age"],
            scenario["gender"]
        )
        print(f"{scenario['activity']} ({scenario['duration']}分钟, {result['intensity']}强度):")
        print(f"  平均心率: {scenario['hr']} bpm")
        print(f"  消耗卡路里: {result['calories']} kcal")
        print(f"  MET估算: {result['met_estimate']}")
        print()


def example_recovery():
    """恢复心率评估示例"""
    print("\n=== 恢复心率评估示例 ===\n")
    
    scenarios = [
        {"name": "运动员", "exercise": 170, "1min": 140, "2min": 115},
        {"name": "健康成年人", "exercise": 160, "1min": 145, "2min": 130},
        {"name": "需要改善", "exercise": 155, "1min": 150, "2min": 145},
    ]
    
    for scenario in scenarios:
        result = HeartRateUtils.calculate_recovery_hr(
            scenario["exercise"],
            scenario["1min"],
            scenario["2min"]
        )
        print(f"{scenario['name']}:")
        print(f"  运动心率: {scenario['exercise']} bpm")
        print(f"  1分钟后: {scenario['1min']} bpm (下降 {result['hr_drop_1min']} bpm)")
        print(f"  2分钟后: {scenario['2min']} bpm (下降 {result['hr_drop_2min']} bpm)")
        print(f"  1分钟评级: {result['recovery_rating']}")
        print(f"  2分钟评级: {result['rating_2min']}")
        print(f"  健康风险: {result['health_risk']}")
        print()


def example_fitness_assessment():
    """心血管健康评估示例"""
    print("\n=== 心血管健康评估示例 ===\n")
    
    scenarios = [
        {"name": "运动员", "resting_hr": 45, "age": 28, "gender": "male"},
        {"name": "健身者", "resting_hr": 58, "age": 35, "gender": "male"},
        {"name": "普通人", "resting_hr": 72, "age": 40, "gender": "male"},
        {"name": "女性运动员", "resting_hr": 48, "age": 26, "gender": "female"},
        {"name": "女性健身者", "resting_hr": 62, "age": 32, "gender": "female"},
    ]
    
    for scenario in scenarios:
        result = HeartRateUtils.assess_cardiovascular_fitness(
            scenario["resting_hr"],
            scenario["age"],
            scenario["gender"]
        )
        print(f"{scenario['name']}:")
        print(f"  静息心率: {scenario['resting_hr']} bpm")
        print(f"  健康水平: {result['fitness_level']}")
        print(f"  评级: {result['rating']}")
        print()


def example_intensity():
    """训练强度示例"""
    print("\n=== 训练强度计算示例 ===\n")
    
    age = 30
    resting_hr = 60
    
    hrs = [100, 120, 140, 160, 180]
    
    print(f"年龄: {age}岁, 静息心率: {resting_hr} bpm\n")
    
    for hr in hrs:
        result = HeartRateUtils.calculate_training_intensity(hr, age, resting_hr)
        print(f"心率 {hr} bpm:")
        print(f"  百分比: {result['percentage_of_max']}%")
        print(f"  Karvonen: {result['karvonen_percentage']}%")
        print(f"  强度: {result['intensity_level']} ({result['color_code']})")
        print(f"  区间: {result['zone']}")
        print()


def example_lactate_threshold():
    """乳酸阈值示例"""
    print("\n=== 乳酸阈值心率示例 ===\n")
    
    for age in [25, 35, 45]:
        result = HeartRateUtils.calculate_lactate_threshold_hr(age)
        print(f"{age}岁:")
        print(f"  乳酸阈值范围: {result['lactate_threshold_range']['min']}-{result['lactate_threshold_range']['max']} bpm")
        print(f"  最大心率: {result['max_hr']} bpm")
        print(f"  提示: {result['training_tip']}")
        print()


def example_pace_estimate():
    """配速估算示例"""
    print("\n=== 配速估算示例 ===\n")
    
    age = 30
    
    print("跑步配速估算:")
    for hr in [100, 120, 140, 160, 180]:
        result = HeartRateUtils.hr_to_pace_estimate(hr, age, 70, "running")
        print(f"  心率 {hr} bpm → {result['estimated_pace_min_per_km']} min/km ({result['intensity']})")
    
    print("\n骑行速度估算:")
    for hr in [100, 120, 140, 160, 180]:
        result = HeartRateUtils.hr_to_pace_estimate(hr, age, 70, "cycling")
        print(f"  心率 {hr} bpm → {result['estimated_speed_kmh']} km/h ({result['intensity']})")
    
    print("\n游泳配速估算:")
    for hr in [120, 140, 160]:
        result = HeartRateUtils.hr_to_pace_estimate(hr, age, 70, "swimming")
        print(f"  心率 {hr} bpm → {result['estimated_pace_min_per_100m']} min/100m ({result['intensity']})")


def example_trend_analysis():
    """心率趋势分析示例"""
    print("\n=== 心率趋势分析示例 ===\n")
    
    # 上升趋势
    rising = [100, 105, 110, 115, 120, 125, 130, 135, 140]
    result = HeartRateUtils.analyze_hr_trend(rising)
    print("上升趋势数据:")
    print(f"  平均心率: {result['average_hr']} bpm")
    print(f"  范围: {result['min_hr']}-{result['max_hr']} bpm")
    print(f"  标准差: {result['std_deviation']}")
    print(f"  趋势: {result['trend']}")
    print(f"  稳定性: {result['stability']}")
    
    # 稳定数据
    stable = [130, 132, 128, 131, 129, 130, 133, 127, 130]
    result = HeartRateUtils.analyze_hr_trend(stable)
    print("\n稳定数据:")
    print(f"  平均心率: {result['average_hr']} bpm")
    print(f"  变异系数: {result['coefficient_of_variation']}%")
    print(f"  RMSSD估算: {result['rmssd_estimate']}")
    print(f"  趋势: {result['trend']}")
    print(f"  稳定性: {result['stability']}")


def example_convenience_functions():
    """便捷函数示例"""
    print("\n=== 便捷函数示例 ===\n")
    
    age = 30
    
    # calculate_max_hr
    print(f"最大心率 (Tanaka): {calculate_max_hr(age)} bpm")
    print(f"最大心率 (Standard): {calculate_max_hr(age, 'standard')} bpm")
    
    # get_zones
    zones = get_zones(age)
    print(f"\n心率区间: Zone 2 范围 {zones['zones']['Zone 2']['hr_range']}")
    
    # get_fat_burning_hr
    fat = get_fat_burning_hr(age)
    print(f"\n燃脂心率: {fat['hr_range']['min']}-{fat['hr_range']['max']} bpm")
    
    # get_current_zone
    zone = get_current_zone(120, age)
    print(f"\n心率120 bpm 当前区间: {zone['name']}")
    
    # estimate_calories
    cal = estimate_calories(150, 45, 70, age, "male")
    print(f"\n45分钟运动卡路里消耗: {cal} kcal")
    
    # assess_fitness
    fitness = assess_fitness(55, age, "male")
    print(f"\n静息心率55 bpm 健康水平: {fitness['fitness_level']}")


def main():
    """运行所有示例"""
    example_max_hr()
    example_zones()
    example_fat_burning()
    example_calories()
    example_recovery()
    example_fitness_assessment()
    example_intensity()
    example_lactate_threshold()
    example_pace_estimate()
    example_trend_analysis()
    example_convenience_functions()
    
    print("\n=== 所有示例完成 ===\n")


if __name__ == "__main__":
    main()