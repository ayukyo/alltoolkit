"""
Water Intake Utils 使用示例
==========================================

展示饮水量计算工具的各种用法。

作者: AllToolkit 自动化生成
日期: 2026-05-23
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    WaterIntakeCalculator,
    ActivityLevel,
    ClimateType,
    HydrationStatus,
    calculate_daily_water,
    get_quick_schedule
)
from datetime import datetime


def example_basic_calculation():
    """示例：基础饮水量计算"""
    print("\n" + "="*50)
    print("示例 1：基础饮水量计算")
    print("="*50)
    
    calc = WaterIntakeCalculator()
    
    # 70kg 成年人，中度活动，温和气候
    result = calc.calculate_daily_intake(weight_kg=70)
    
    print(f"体重: {result['weight_kg']} kg")
    print(f"基础饮水量: {result['base_intake_ml']} ml")
    print(f"活动水平: {result['activity_level']}")
    print(f"活动调整系数: {result['activity_multiplier']}")
    print(f"气候: {result['climate']}")
    print(f"气候调整系数: {result['climate_multiplier']}")
    print(f"\n✨ 每日建议饮水量: {result['total_intake_ml']} ml ({result['total_intake_liters']} L)")
    print(f"   相当于约 {int(result['glasses_of_water'])} 杯水（每杯250ml）")


def example_activity_levels():
    """示例：不同活动水平的饮水需求"""
    print("\n" + "="*50)
    print("示例 2：不同活动水平的饮水需求")
    print("="*50)
    
    calc = WaterIntakeCalculator()
    weight = 70  # kg
    
    levels = [
        (ActivityLevel.SEDENTARY, "久坐（很少运动）"),
        (ActivityLevel.LIGHT, "轻度活动（每周1-3天轻度运动）"),
        (ActivityLevel.MODERATE, "中度活动（每周3-5天中度运动）"),
        (ActivityLevel.ACTIVE, "活跃（每周6-7天运动）"),
        (ActivityLevel.VERY_ACTIVE, "非常活跃（剧烈运动/体力劳动）")
    ]
    
    print(f"\n体重: {weight} kg\n")
    print(f"{'活动水平':<30} {'调整系数':<10} {'每日饮水量':<15}")
    print("-" * 55)
    
    for level, desc in levels:
        result = calc.calculate_daily_intake(
            weight_kg=weight,
            activity_level=level
        )
        print(f"{desc:<30} {result['activity_multiplier']:<10.1f} {result['total_intake_ml']} ml")


def example_climate_effects():
    """示例：气候对饮水量的影响"""
    print("\n" + "="*50)
    print("示例 3：气候对饮水量的影响")
    print("="*50)
    
    calc = WaterIntakeCalculator()
    weight = 70  # kg
    
    climates = [
        (ClimateType.COLD, "寒冷 (<10°C)"),
        (ClimateType.MILD, "温和 (10-20°C)"),
        (ClimateType.WARM, "温暖 (20-25°C)"),
        (ClimateType.HOT, "炎热 (25-35°C)"),
        (ClimateType.VERY_HOT, "酷热 (>35°C)"),
        (ClimateType.HUMID, "潮湿（高湿度）")
    ]
    
    print(f"\n体重: {weight} kg, 活动水平: 中度\n")
    print(f"{'气候':<20} {'调整系数':<10} {'每日饮水量':<15}")
    print("-" * 45)
    
    for climate, desc in climates:
        result = calc.calculate_daily_intake(
            weight_kg=weight,
            climate=climate
        )
        print(f"{desc:<20} {result['climate_multiplier']:<10.1f} {result['total_intake_ml']} ml")


def example_exercise_adjustment():
    """示例：运动对饮水量的影响"""
    print("\n" + "="*50)
    print("示例 4：运动对饮水量的影响")
    print("="*50)
    
    calc = WaterIntakeCalculator()
    
    # 不同运动时间
    exercise_times = [0, 30, 60, 90, 120]
    
    print(f"\n体重: 70 kg\n")
    print(f"{'运动时间':<15} {'额外补水':<15} {'总饮水量':<15}")
    print("-" * 45)
    
    for minutes in exercise_times:
        result = calc.calculate_daily_intake(
            weight_kg=70,
            exercise_minutes=minutes
        )
        print(f"{minutes} 分钟{' '*8} {result['exercise_addition_ml']} ml{' '*7} {result['total_intake_ml']} ml")


def example_special_conditions():
    """示例：特殊情况下的饮水需求"""
    print("\n" + "="*50)
    print("示例 5：特殊情况下的饮水需求")
    print("="*50)
    
    calc = WaterIntakeCalculator()
    
    conditions = [
        ([], "正常人"),
        (['pregnancy'], "孕期"),
        (['breastfeeding'], "哺乳期"),
        (['illness_fever'], "发烧"),
        (['altitude_high'], "高海拔"),
        (['alcohol'], "饮酒后"),
        (['pregnancy', 'altitude_high'], "孕期 + 高海拔")
    ]
    
    print(f"\n体重: 70 kg\n")
    print(f"{'特殊情况':<25} {'额外水量':<15} {'总饮水量':<15}")
    print("-" * 55)
    
    for condition_list, desc in conditions:
        result = calc.calculate_daily_intake(
            weight_kg=70,
            special_conditions=condition_list
        )
        print(f"{desc:<25} +{result['special_addition_ml']} ml{' '*7} {result['total_intake_ml']} ml")


def example_drinking_schedule():
    """示例：生成饮水时间表"""
    print("\n" + "="*50)
    print("示例 6：饮水时间表")
    print("="*50)
    
    calc = WaterIntakeCalculator()
    
    # 计算每日饮水量
    daily = calc.calculate_daily_intake(
        weight_kg=70,
        activity_level=ActivityLevel.ACTIVE,
        climate=ClimateType.WARM
    )
    
    print(f"\n每日建议饮水量: {daily['total_intake_ml']} ml\n")
    
    # 生成时间表
    schedule = calc.generate_drinking_schedule(
        daily_intake_ml=daily['total_intake_ml'],
        wake_time=(7, 0),
        sleep_time=(23, 0),
        num_reminders=8
    )
    
    print(f"{'时间':<10} {'饮水量':<12} {'累计':<12} {'进度':<10} {'说明'}")
    print("-" * 60)
    
    for s in schedule:
        print(f"{s['time']:<10} {s['amount_ml']} ml{' '*4} {s['cumulative_ml']} ml{' '*4} {s['percentage']}%{' '*5} {s['note']}")


def example_record_and_track():
    """示例：记录和追踪饮水"""
    print("\n" + "="*50)
    print("示例 7：记录和追踪饮水")
    print("="*50)
    
    calc = WaterIntakeCalculator()
    
    # 计算目标
    target = calc.calculate_daily_intake(weight_kg=70)['total_intake_ml']
    print(f"\n今日目标: {target} ml\n")
    
    # 模拟一天的饮水记录
    drinks = [
        (250, "water", "起床后"),
        (300, "water", "早餐时"),
        (200, "tea", "上午"),
        (500, "water", "午餐后"),
        (300, "coffee", "下午"),
        (400, "water", "运动后"),
        (250, "water", "晚餐时")
    ]
    
    print("饮水记录:")
    print("-" * 40)
    for amount, beverage, note in drinks:
        record = calc.record_intake(
            amount_ml=amount,
            beverage_type=beverage,
            note=note
        )
        print(f"  {record['time']} - {amount}ml {beverage} ({note})")
    
    # 获取摘要
    summary = calc.get_daily_summary(target_intake_ml=target)
    
    print(f"\n今日汇总:")
    print(f"  总饮水量: {summary['total_intake_ml']} ml ({summary['total_intake_liters']} L)")
    print(f"  记录次数: {summary['record_count']} 次")
    print(f"  进度: {summary['progress_percentage']}%")
    print(f"  剩余: {summary['remaining_ml']} ml")
    
    print(f"\n按饮料类型:")
    for beverage, amount in summary['by_beverage_type'].items():
        print(f"  {beverage}: {amount} ml")


def example_hydration_assessment():
    """示例：补水状态评估"""
    print("\n" + "="*50)
    print("示例 8：补水状态评估")
    print("="*50)
    
    calc = WaterIntakeCalculator()
    
    target = 2500  # ml
    
    scenarios = [
        (500, "pale_yellow", "早上刚起床"),
        (1200, "yellow", "上午"),
        (1800, "pale_yellow", "下午"),
        (2500, "pale_yellow", "晚上达标"),
        (3000, "clear", "饮水过量")
    ]
    
    print(f"\n目标饮水量: {target} ml\n")
    
    for intake, urine_color, desc in scenarios:
        assessment = calc.assess_hydration(
            current_intake_ml=intake,
            target_intake_ml=target,
            urine_color=urine_color
        )
        
        print(f"场景: {desc}")
        print(f"  饮水量: {intake} ml ({assessment['progress_ratio']*100:.0f}%)")
        print(f"  状态: {assessment['status_display']}")
        if assessment['urine_color_assessment']:
            print(f"  尿液颜色: {assessment['urine_color_assessment']['assessment']}")
        print(f"  建议: {assessment['recommendations'][0]}")
        print()


def example_sweat_loss():
    """示例：运动出汗量计算"""
    print("\n" + "="*50)
    print("示例 9：运动出汗量计算")
    print("="*50)
    
    calc = WaterIntakeCalculator()
    
    result = calc.calculate_sweat_loss(
        weight_before_kg=70,
        weight_after_kg=69.2,
        fluid_intake_ml=400,
        urine_output_ml=0,
        duration_minutes=60
    )
    
    print(f"\n运动前后体重变化:")
    print(f"  运动前: {result['weight_before_kg']} kg")
    print(f"  运动后: {result['weight_after_kg']} kg")
    print(f"  体重减少: {result['weight_loss_kg']} kg ({result['weight_loss_percent']}%)")
    
    print(f"\n出汗量分析:")
    print(f"  估算出汗量: {result['sweat_loss_ml']} ml")
    print(f"  出汗率: {result['sweat_rate_ml_per_hour']} ml/小时")
    print(f"  运动中补水: {result['fluid_intake_ml']} ml")
    
    print(f"\n补水建议:")
    print(f"  需要补充: {result['rehydration_needed_ml']} ml")
    print(f"  脱水程度: {result['dehydration_severity']}")
    print(f"\n建议:")
    for rec in result['recommendations']:
        if rec:
            print(f"  • {rec}")


def example_beverage_equivalents():
    """示例：饮料等效量"""
    print("\n" + "="*50)
    print("示例 10：饮料等效量")
    print("="*50)
    
    calc = WaterIntakeCalculator()
    
    water_needed = 2000  # ml
    equivalents = calc.get_beverage_equivalent(water_needed)
    
    print(f"\n要达到 {water_needed} ml 纯水的补水效果，需要:\n")
    
    beverages_order = ['water', 'tea', 'coconut_water', 'sports_drink', 
                       'juice', 'milk', 'coffee', 'soda', 'beer']
    
    for beverage in beverages_order:
        if beverage in equivalents:
            info = equivalents[beverage]
            print(f"  {beverage:<15} {info['equivalent_ml']} ml  (补水系数: {info['hydration_factor']})")
            print(f"                  {info['note']}")
            print()


def example_sport_hydration():
    """示例：运动补水方案"""
    print("\n" + "="*50)
    print("示例 11：运动补水方案")
    print("="*50)
    
    calc = WaterIntakeCalculator()
    
    sports = [
        ('running', 'high', 60),
        ('cycling', 'moderate', 90),
        ('yoga', 'low', 45),
        ('basketball', 'high', 90),
        ('swimming', 'moderate', 60)
    ]
    
    print(f"\n体重: 70 kg, 温度: 25°C\n")
    
    for sport, intensity, duration in sports:
        result = calc.calculate_for_sport(
            sport_type=sport,
            duration_minutes=duration,
            intensity=intensity,
            weight_kg=70,
            temperature_c=25
        )
        
        print(f"🏃 {sport.upper()} ({duration}分钟, {intensity}强度)")
        print(f"   预计出汗量: {result['estimated_sweat_loss_ml']} ml")
        print(f"   补水计划:")
        print(f"     • 运动前: {result['hydration_plan']['before_exercise_ml']} ml")
        print(f"     • 运动中: 每15分钟 {result['hydration_plan']['during_exercise']['per_15_minutes_ml']} ml")
        print(f"     • 运动后: {result['hydration_plan']['after_exercise_ml']} ml")
        print(f"   总补水量: {result['total_recommended_ml']} ml\n")


def example_quick_functions():
    """示例：快速便捷函数"""
    print("\n" + "="*50)
    print("示例 12：快速便捷函数")
    print("="*50)
    
    # 快速计算每日饮水量
    result = calculate_daily_water(
        weight_kg=75,
        activity_level='active',
        climate='hot',
        exercise_minutes=45
    )
    
    print(f"\n快速计算:")
    print(f"  体重: 75 kg")
    print(f"  活动水平: active")
    print(f"  气候: hot")
    print(f"  运动时间: 45 分钟")
    print(f"  → 每日建议: {result['total_intake_ml']} ml\n")
    
    # 快速生成时间表
    schedule = get_quick_schedule(total_ml=2500, wake_hour=6)
    
    print(f"快速时间表 (6:00 起床):")
    for s in schedule[:5]:
        print(f"  {s['time']} - {s['amount_ml']} ml")


def main():
    """运行所有示例"""
    print("\n" + "="*60)
    print("💧 Water Intake Utils - 饮水量计算工具 使用示例")
    print("="*60)
    
    example_basic_calculation()
    example_activity_levels()
    example_climate_effects()
    example_exercise_adjustment()
    example_special_conditions()
    example_drinking_schedule()
    example_record_and_track()
    example_hydration_assessment()
    example_sweat_loss()
    example_beverage_equivalents()
    example_sport_hydration()
    example_quick_functions()
    
    print("\n" + "="*60)
    print("✨ 所有示例运行完成!")
    print("="*60)


if __name__ == "__main__":
    main()