"""
Running Pace Utils - 使用示例

展示跑步配速计算工具的主要功能：
1. 基本配速计算
2. 比赛预测
3. 训练区间
4. 分段计时
5. 坡度调整配速
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    DistanceUnit, PaceUnit,
    calculate_pace, calculate_time, calculate_distance,
    convert_distance, convert_pace,
    generate_splits, predict_race_time,
    calculate_vdot, calculate_age_grade,
    calculate_training_zones, calculate_running_economy,
    generate_race_pace_table, calculate_interval_pace,
    estimate_finish_time_from_splits,
    calculate_grade_adjusted_pace,
    pace_to_speed, speed_to_pace, format_pace, format_time,
)


def example_basic_pace():
    """基本配速计算示例"""
    print("\n" + "="*60)
    print("示例 1: 基本配速计算")
    print("="*60)
    
    # 10公里跑了 45 分钟
    distance = 10  # 公里
    time_minutes = 45
    
    result = calculate_pace(distance, time_minutes * 60, DistanceUnit.KILOMETERS)
    
    print(f"\n距离: {distance} 公里")
    print(f"时间: {time_minutes} 分钟")
    print(f"配速: {format_pace(result.pace_min_per_km)}")
    print(f"速度: {result.speed_kmh:.1f} km/h")
    print(f"英里配速: {format_pace(result.pace_min_per_mile)}/mile")
    
    # 反向计算：给定配速，计算时间
    pace = 4.5  # 4:30/km
    distance = 21.1  # 半程马拉松
    
    time_seconds = calculate_time(distance, pace, DistanceUnit.KILOMETERS, PaceUnit.MIN_PER_KM)
    print(f"\n半马 @ {format_pace(pace)}")
    print(f"预计时间: {format_time(time_seconds)}")


def example_race_prediction():
    """比赛预测示例"""
    print("\n" + "="*60)
    print("示例 2: 比赛预测（基于 10km 成绩）")
    print("="*60)
    
    # 10km 40 分钟成绩
    reference_time = 40 * 60
    reference_distance = 10
    
    # 预测不同距离
    distances = [
        ("5公里", 5),
        ("10公里", 10),
        ("半程马拉松", 21.0975),
        ("全程马拉松", 42.195),
    ]
    
    print(f"\n参考成绩: 10公里 {format_time(reference_time)}")
    print("\n预测成绩:")
    print("-" * 50)
    
    for name, dist in distances:
        pred = predict_race_time(dist, reference_time, reference_distance)
        print(f"{name:12} | {pred.predicted_time_formatted:>10} | {pred.pace_formatted}")


def example_splits():
    """分段计时示例"""
    print("\n" + "="*60)
    print("示例 3: 分段计时表")
    print("="*60)
    
    # 马拉松 3:30 目标
    distance = 42.195
    time_minutes = 210
    
    splits = generate_splits(distance, time_minutes * 60, 5.0)  # 每 5km
    
    print(f"\n马拉松 {format_time(time_minutes * 60)} 目标分段:")
    print("-" * 40)
    print(f"{'距离':>8} | {'累计时间':>10} | {'分段用时':>10}")
    print("-" * 40)
    
    for split in splits:
        print(f"{split.distance:>6.1f}km | {format_time(split.cumulative_time):>10} | {format_time(split.split_time):>10}")


def example_vdot():
    """VDOT 跑力值计算示例"""
    print("\n" + "="*60)
    print("示例 4: VDOT 跑力值计算")
    print("="*60)
    
    results = [
        ("5公里", 5, 20 * 60),
        ("10公里", 10, 42 * 60),
        ("半程马拉松", 21.0975, 1.5 * 3600),
        ("全程马拉松", 42.195, 3.5 * 3600),
    ]
    
    print("\nVDOT 跑力值:")
    print("-" * 50)
    
    for name, dist, time in results:
        vdot = calculate_vdot(dist, time)
        print(f"{name:12} | {format_time(time):>10} | VDOT: {vdot:.1f}")


def example_age_grade():
    """年龄分级示例"""
    print("\n" + "="*60)
    print("示例 5: 年龄分级")
    print("="*60)
    
    # 10km 40 分钟，不同年龄
    ages = [25, 35, 45, 55, 65]
    time = 40 * 60
    distance = 10
    
    print(f"\n10公里 {format_time(time)} 年龄分级:")
    print("-" * 50)
    
    for age in ages:
        factor, percent = calculate_age_grade(time, distance, age, "M")
        print(f"{age}岁 | 系数: {factor:.3f} | 分级: {percent:.1f}%")


def example_training_zones():
    """训练区间示例"""
    print("\n" + "="*60)
    print("示例 6: 训练区间")
    print("="*60)
    
    max_hr = 180
    threshold_pace = 4.5  # 4:30/km
    
    zones = calculate_training_zones(max_hr, threshold_pace)
    
    print(f"\n最大心率: {max_hr} bpm")
    print(f"阈值配速: {format_pace(threshold_pace)}")
    print("\n训练区间:")
    print("-" * 70)
    print(f"{'区间':>4} | {'名称':>10} | {'心率':>12} | {'配速':>15} | 说明")
    print("-" * 70)
    
    for zone in zones:
        hr_str = f"{zone.hr_min}-{zone.hr_max}"
        pace_str = f"{format_pace(zone.pace_min_per_km[0])}-{format_pace(zone.pace_min_per_km[1])}"
        print(f"Z{zone.zone}   | {zone.name:>10} | {hr_str:>12} | {pace_str:>15} | {zone.description}")


def example_interval_paces():
    """间歇训练配速示例"""
    print("\n" + "="*60)
    print("示例 7: 间歇训练配速")
    print("="*60)
    
    goal_pace = 4.0  # 目标 4:00/km
    
    paces = calculate_interval_pace(goal_pace, "threshold")
    
    print(f"\n目标配速: {format_pace(goal_pace)}")
    print("\n训练配速建议:")
    print("-" * 50)
    
    train_names = {
        "repetition": "重复跑 (最快)",
        "interval": "间歇跑",
        "threshold": "阈值跑",
        "tempo": "节奏跑",
        "marathon": "马拉松配速",
        "easy": "轻松跑",
        "recovery": "恢复跑 (最慢)",
    }
    
    for pace_type, pace_info in paces.items():
        name = train_names.get(pace_type, pace_type)
        print(f"{name:>16} | {pace_info['pace_formatted']}")


def example_running_economy():
    """跑步经济性示例"""
    print("\n" + "="*60)
    print("示例 8: 跑步经济性")
    print("="*60)
    
    # 10km 40 分钟，体重 70kg
    distance = 10
    time = 40 * 60
    weight = 70
    
    eco = calculate_running_economy(distance, time, weight, vo2max=55)
    
    print(f"\n跑步数据: {distance}km / {format_time(time)} / {weight}kg / VO2max: 55")
    print("-" * 50)
    print(f"速度: {eco['speed_kmh']} km/h")
    print(f"VO2: {eco['vo2_ml_kg_min']} ml/kg/min")
    print(f"能量消耗: {eco['total_kcal']} kcal")
    print(f"每公里消耗: {eco['kcal_per_km']} kcal/km")
    print(f"相对强度: {eco['intensity_percent_vo2max']}% VO2max")


def example_grade_adjusted_pace():
    """坡度调整配速示例"""
    print("\n" + "="*60)
    print("示例 9: 坡度调整配速 (GAP)")
    print("="*60)
    
    actual_pace = 5.0  # 5:00/km
    grades = [
        ("平地", 0),
        ("缓上坡 3%", 3),
        ("陡上坡 10%", 10),
        ("缓下坡 -3%", -3),
        ("陡下坡 -10%", -10),
    ]
    
    print(f"\n实际配速: {format_pace(actual_pace)}")
    print("\n坡度调整配速:")
    print("-" * 50)
    
    for name, grade in grades:
        gap = calculate_grade_adjusted_pace(actual_pace, grade)
        print(f"{name:>12} | GAP: {format_pace(gap)}")


def example_race_pace_table():
    """比赛配速表示例"""
    print("\n" + "="*60)
    print("示例 10: 比赛配速表")
    print("="*60)
    
    # 半程马拉松 1:45 目标
    distance = 21.0975
    time_minutes = 105
    
    table = generate_race_pace_table(distance, time_minutes)
    
    print(f"\n半程马拉松目标: {table['target_time']}")
    print(f"目标配速: {table['pace_formatted']}")
    print(f"平均速度: {table['speed_kmh']} km/h")
    print("\n每 5km 分段:")
    print("-" * 40)
    
    for split in table['km_splits']:
        if split['km'] % 5 < 0.1:  # 每 5km 显示一次
            print(f"{split['km']:>5.1f}km | {split['time']}")


def example_progress_prediction():
    """比赛进度预测示例"""
    print("\n" + "="*60)
    print("示例 11: 比赛进度预测")
    print("="*60)
    
    # 已跑 15km，用时 1:15，预测全程马拉松
    splits = [
        (5, 25 * 60),   # 5km 25 分钟
        (5, 25 * 60),   # 5-10km 25 分钟
        (5, 25 * 60),   # 10-15km 25 分钟
    ]
    
    result = estimate_finish_time_from_splits(splits, 42.195)
    
    print(f"\n当前状态:")
    print(f"已完成距离: {result['completed_distance_km']} km")
    print(f"剩余距离: {result['remaining_distance_km']} km")
    print(f"已用时间: {result['elapsed_time']}")
    print(f"进度: {result['progress_percent']}%")
    print(f"\n预测:")
    print(f"剩余时间: {result['predicted_remaining_time']}")
    print(f"总完赛时间: {result['predicted_total_time']}")
    print(f"平均配速: {result['predicted_average_pace']}")


def main():
    """运行所有示例"""
    print("\n" + "#"*60)
    print("# Running Pace Utils - 使用示例")
    print("#"*60)
    
    example_basic_pace()
    example_race_prediction()
    example_splits()
    example_vdot()
    example_age_grade()
    example_training_zones()
    example_interval_paces()
    example_running_economy()
    example_grade_adjusted_pace()
    example_race_pace_table()
    example_progress_prediction()
    
    print("\n" + "#"*60)
    print("# 所有示例运行完成")
    print("#"*60 + "\n")


if __name__ == "__main__":
    main()