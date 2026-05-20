#!/usr/bin/env python3
"""
Water Intake Utils - 使用示例

演示饮水追踪工具的各种功能。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, time, timedelta
from mod import (
    WaterIntakeCalculator,
    WaterTracker,
    DrinkReminder,
    ActivityLevel,
    Climate,
    DrinkType,
    calculate_water_needs,
    format_water_amount,
    get_water_percentage,
)


def example_basic_calculation():
    """示例 1: 基础饮水量计算"""
    print("=" * 50)
    print("示例 1: 基础饮水量计算")
    print("=" * 50)
    
    # 70公斤，中等活动，温和气候
    calculator = WaterIntakeCalculator(
        weight_kg=70,
        activity_level=ActivityLevel.MODERATE,
        climate=Climate.MILD,
    )
    
    target = calculator.calculate_daily_target()
    print(f"\n个人信息:")
    print(f"  体重: 70kg")
    print(f"  活动水平: 中等")
    print(f"  气候: 温和")
    print(f"\n每日建议饮水量: {format_water_amount(target)}")
    
    # 获取饮水建议
    print(f"\n饮水建议:")
    for i, rec in enumerate(calculator.get_recommendations(), 1):
        print(f"  {i}. {rec}")


def example_different_scenarios():
    """示例 2: 不同场景的饮水量需求"""
    print("\n" + "=" * 50)
    print("示例 2: 不同场景的饮水量需求")
    print("=" * 50)
    
    scenarios = [
        ("久坐办公室", 65, ActivityLevel.SEDENTARY, Climate.MILD, None, False, False),
        ("健身爱好者", 75, ActivityLevel.ACTIVE, Climate.MILD, None, False, False),
        ("户外工作者", 70, ActivityLevel.MODERATE, Climate.HOT, None, False, False),
        ("孕妇", 60, ActivityLevel.LIGHT, Climate.MILD, None, True, False),
        ("哺乳期妈妈", 58, ActivityLevel.LIGHT, Climate.MILD, None, False, True),
        ("老年人", 68, ActivityLevel.SEDENTARY, Climate.MILD, 70, False, False),
        ("青少年运动员", 55, ActivityLevel.VERY_ACTIVE, Climate.WARM, 16, False, False),
    ]
    
    print(f"\n{'场景':<15} {'体重':>6} {'活动':<10} {'气候':<8} {'建议饮水量':>10}")
    print("-" * 60)
    
    for name, weight, activity, climate, age, pregnant, breastfeeding in scenarios:
        calc = WaterIntakeCalculator(
            weight_kg=weight,
            activity_level=activity,
            climate=climate,
            age=age,
            is_pregnant=pregnant,
            is_breastfeeding=breastfeeding,
        )
        target = calc.calculate_daily_target()
        activity_name = {
            ActivityLevel.SEDENTARY: "久坐",
            ActivityLevel.LIGHT: "轻度",
            ActivityLevel.MODERATE: "中等",
            ActivityLevel.ACTIVE: "活跃",
            ActivityLevel.VERY_ACTIVE: "非常活跃",
        }[activity]
        climate_name = {
            Climate.COLD: "寒冷",
            Climate.MILD: "温和",
            Climate.WARM: "温暖",
            Climate.HOT: "炎热",
            Climate.VERY_HOT: "酷热",
        }[climate]
        print(f"{name:<15} {weight:>4}kg {activity_name:<10} {climate_name:<8} {format_water_amount(target):>10}")


def example_daily_tracking():
    """示例 3: 每日饮水追踪"""
    print("\n" + "=" * 50)
    print("示例 3: 每日饮水追踪")
    print("=" * 50)
    
    # 创建追踪器
    calculator = WaterIntakeCalculator(
        weight_kg=70,
        activity_level=ActivityLevel.MODERATE,
        climate=Climate.MILD,
    )
    tracker = WaterTracker(calculator)
    
    # 模拟一天的饮水记录
    now = datetime.now()
    
    print(f"\n今日饮水记录:")
    print("-" * 40)
    
    # 早起
    tracker.add_drink(250, DrinkType.WATER, timestamp=now.replace(hour=7, minute=30), note="起床第一杯")
    print(f"07:30 - 🚰 纯净水 250ml - 起床第一杯")
    
    # 早餐
    tracker.add_drink(200, DrinkType.MILK, timestamp=now.replace(hour=8, minute=0), note="早餐")
    print(f"08:00 - 🥛 牛奶 200ml - 早餐")
    
    # 上午咖啡
    tracker.add_drink(200, DrinkType.COFFEE, timestamp=now.replace(hour=10, minute=30), note="上午咖啡")
    print(f"10:30 - ☕ 咖啡 200ml - 上午咖啡")
    
    # 午餐
    tracker.add_drink(300, DrinkType.SOUP, timestamp=now.replace(hour=12, minute=30), note="午餐汤")
    print(f"12:30 - 🍲 汤 300ml - 午餐汤")
    
    # 下午茶
    tracker.add_drink(250, DrinkType.TEA, timestamp=now.replace(hour=15, minute=0), note="下午茶")
    print(f"15:00 - 🍵 茶 250ml - 下午茶")
    
    # 运动后
    tracker.add_drink(400, DrinkType.SPORTS_DRINK, timestamp=now.replace(hour=18, minute=0), note="运动后补水")
    print(f"18:00 - 🧃 运动饮料 400ml - 运动后补水")
    
    # 晚餐
    tracker.add_drink(300, DrinkType.WATER, timestamp=now.replace(hour=19, minute=30), note="晚餐")
    print(f"19:30 - 🚰 纯净水 300ml - 晚餐")
    
    # 睡前
    tracker.add_drink(200, DrinkType.WATER, timestamp=now.replace(hour=21, minute=30), note="睡前")
    print(f"21:30 - 🚰 纯净水 200ml - 睡前")
    
    # 获取汇总
    print("\n" + "-" * 40)
    summary = tracker.get_daily_summary()
    print(f"\n今日汇总:")
    print(f"  总饮水量: {format_water_amount(summary.total_ml)}")
    print(f"  有效水量: {format_water_amount(summary.effective_ml)}")
    print(f"  目标水量: {format_water_amount(summary.target_ml)}")
    print(f"  完成率: {summary.completion_rate * 100:.1f}%")
    print(f"  状态: {'✅ 达标' if summary.is_goal_met else '❌ 未达标'}")
    
    # 显示进度条
    print(f"\n进度: {get_water_percentage(summary.effective_ml, summary.target_ml)}")


def example_drink_schedule():
    """示例 4: 饮水时间表"""
    print("\n" + "=" * 50)
    print("示例 4: 饮水时间表")
    print("=" * 50)
    
    calculator = WaterIntakeCalculator(
        weight_kg=70,
        activity_level=ActivityLevel.MODERATE,
        climate=Climate.MILD,
    )
    
    schedule = calculator.get_drink_schedule(
        start_time=time(7, 0),
        end_time=time(21, 0),
        interval_minutes=90,
        drink_size_ml=250,
    )
    
    print(f"\n建议饮水时间表 (每次 250ml):")
    print("-" * 30)
    for i, (drink_time, amount) in enumerate(schedule, 1):
        emoji = "🌅" if drink_time.hour < 12 else "☀️" if drink_time.hour < 18 else "🌙"
        print(f"{i:2}. {emoji} {drink_time.strftime('%H:%M')} - {int(amount)}ml")
    
    total = sum(amount for _, amount in schedule)
    print(f"\n总计划饮水量: {format_water_amount(total)}")


def example_reminder():
    """示例 5: 饮水提醒"""
    print("\n" + "=" * 50)
    print("示例 5: 饮水提醒")
    print("=" * 50)
    
    calculator = WaterIntakeCalculator(
        weight_kg=70,
        activity_level=ActivityLevel.SEDENTARY,
        climate=Climate.MILD,
    )
    tracker = WaterTracker(calculator)
    
    reminder = DrinkReminder(
        tracker=tracker,
        interval_minutes=60,
        start_time=time(7, 0),
        end_time=time(22, 0),
    )
    
    # 检查提醒
    print("\n当前状态检查:")
    message = reminder.check_reminder()
    if message:
        print(f"  💧 {message}")
    
    # 添加一些饮水记录
    tracker.add_drink(250, DrinkType.WATER)
    print(f"\n已记录: 250ml 纯净水")
    
    # 再次检查
    message = reminder.check_reminder()
    if message:
        print(f"  💧 {message}")
    else:
        print(f"  ✅ 刚喝过水，暂时不需要提醒")
    
    # 获取下次提醒时间
    next_time = reminder.get_next_reminder_time()
    if next_time:
        print(f"\n下次提醒时间: {next_time.strftime('%H:%M')}")
    
    # 获取剩余提醒次数
    remaining = reminder.get_remaining_reminders_today()
    print(f"今日预计还需提醒: {remaining} 次")


def example_weekly_statistics():
    """示例 6: 周统计"""
    print("\n" + "=" * 50)
    print("示例 6: 周统计")
    print("=" * 50)
    
    calculator = WaterIntakeCalculator(
        weight_kg=70,
        activity_level=ActivityLevel.MODERATE,
        climate=Climate.MILD,
    )
    tracker = WaterTracker(calculator)
    
    # 模拟一周的数据
    import random
    now = datetime.now()
    
    for i in range(7):
        date = now - timedelta(days=i)
        # 随机 6-10 杯水
        num_drinks = random.randint(6, 10)
        for j in range(num_drinks):
            hour = 7 + j * 2
            if hour > 22:
                hour = 22
            tracker.add_drink(
                random.choice([200, 250, 300]),
                random.choice([DrinkType.WATER, DrinkType.TEA, DrinkType.COFFEE]),
                timestamp=date.replace(hour=hour, minute=random.randint(0, 59)),
            )
    
    # 周汇总
    weekly = tracker.get_weekly_summary()
    
    print(f"\n本周饮水记录:")
    print("-" * 50)
    day_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    
    for summary in weekly:
        date = datetime.strptime(summary.date, "%Y-%m-%d")
        day_name = day_names[date.weekday()]
        status = "✅" if summary.is_goal_met else "❌"
        print(f"{summary.date} ({day_name}): {format_water_amount(summary.effective_ml):>8} {status}")
    
    # 统计数据
    stats = tracker.get_statistics(days=7)
    
    print("\n" + "-" * 50)
    print(f"\n周统计汇总:")
    print(f"  记录天数: {stats['days_tracked']} 天")
    print(f"  达标天数: {stats['days_goal_met']} 天")
    print(f"  达标率: {stats['goal_met_rate'] * 100:.1f}%")
    print(f"  平均饮水量: {format_water_amount(stats['average_ml'])}")
    print(f"  平均完成率: {stats['average_completion_rate'] * 100:.1f}%")
    print(f"  总饮水量: {format_water_amount(stats['total_ml'])}")


def example_persistence():
    """示例 7: 数据持久化"""
    print("\n" + "=" * 50)
    print("示例 7: 数据持久化")
    print("=" * 50)
    
    # 创建并记录数据
    calculator = WaterIntakeCalculator(
        weight_kg=70,
        activity_level=ActivityLevel.ACTIVE,
        climate=Climate.WARM,
        age=28,
    )
    tracker = WaterTracker(calculator)
    
    tracker.add_drink(250, DrinkType.WATER, note="早上一杯")
    tracker.add_drink(200, DrinkType.COFFEE, note="上午咖啡")
    tracker.add_drink(300, DrinkType.WATER, note="午餐")
    
    # 导出为 JSON
    json_data = tracker.to_json()
    print(f"\n导出的 JSON 数据:")
    print(json_data[:300] + "..." if len(json_data) > 300 else json_data)
    
    # 从 JSON 导入
    restored = WaterTracker.from_json(json_data)
    
    print(f"\n从 JSON 恢复:")
    print(f"  体重: {restored.calculator.weight_kg}kg")
    print(f"  活动水平: {restored.calculator.activity_level.value}")
    print(f"  气候: {restored.calculator.climate.value}")
    print(f"  年龄: {restored.calculator.age}")
    print(f"  记录数: {len(restored.records)}")


def example_convenience_functions():
    """示例 8: 便捷函数"""
    print("\n" + "=" * 50)
    print("示例 8: 便捷函数")
    print("=" * 50)
    
    # 快速计算饮水量
    target1 = calculate_water_needs(weight_kg=70)
    print(f"\n70kg 成人（默认活动水平和气候）: {format_water_amount(target1)}")
    
    target2 = calculate_water_needs(
        weight_kg=60,
        activity_level="active",
        climate="hot",
    )
    print(f"60kg 活跃人群，炎热气候: {format_water_amount(target2)}")
    
    target3 = calculate_water_needs(
        weight_kg=65,
        activity_level="light",
        climate="mild",
        is_pregnant=True,
    )
    print(f"65kg 孕妇: {format_water_amount(target3)}")
    
    # 格式化函数
    print(f"\n格式化示例:")
    print(f"  500ml -> {format_water_amount(500)}")
    print(f"  1500ml -> {format_water_amount(1500)}")
    print(f"  2000ml -> {format_water_amount(2000)}")
    
    # 进度条
    print(f"\n进度条示例:")
    print(f"  25%: {get_water_percentage(500, 2000)}")
    print(f"  50%: {get_water_percentage(1000, 2000)}")
    print(f"  75%: {get_water_percentage(1500, 2000)}")
    print(f"  100%: {get_water_percentage(2000, 2000)}")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("🚰 Water Intake Utils - 使用示例")
    print("=" * 60)
    
    example_basic_calculation()
    example_different_scenarios()
    example_daily_tracking()
    example_drink_schedule()
    example_reminder()
    example_weekly_statistics()
    example_persistence()
    example_convenience_functions()
    
    print("\n" + "=" * 60)
    print("✅ 所有示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()