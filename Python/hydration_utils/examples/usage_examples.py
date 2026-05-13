"""
Hydration Utils - 使用示例

展示水分追踪工具的各种使用场景
"""

from datetime import datetime, date, timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mod import (
    ActivityLevel,
    ClimateType,
    BeverageType,
    HydrationStatus,
    HydrationTracker,
    calculate_daily_water_needs,
    calculate_hydration_status,
    get_drinking_schedule,
    calculate_beverage_hydration,
    estimate_water_from_foods,
    get_exercise_hydration_plan,
    calculate_caffeine_impact,
    generate_hydration_report,
    calculate_oral_rehydration_solution,
    get_weather_adjusted_target,
    FOOD_WATER_CONTENT,
)


def example_basic_calculation():
    """示例1：基础每日水需求计算"""
    print("\n" + "="*60)
    print("示例1：基础每日水需求计算")
    print("="*60)
    
    # 计算不同人群的每日水需求
    
    # 久坐办公族
    sedentary = calculate_daily_water_needs(
        weight_kg=70,
        age=30,
        gender="male",
        activity_level=ActivityLevel.SEDENTARY,
        climate=ClimateType.TEMPERATE
    )
    print(f"\n久坐办公族（70kg，30岁男性）：")
    print(f"  基础需求：{sedentary['base_need_ml']}ml")
    print(f"  总需求：{sedentary['total_need_ml']}ml")
    print(f"  约需：{sedentary['recommended_glasses']}杯（250ml/杯）")
    
    # 运动爱好者
    active = calculate_daily_water_needs(
        weight_kg=75,
        age=25,
        gender="male",
        activity_level=ActivityLevel.ACTIVE,
        climate=ClimateType.WARM,
        exercise_minutes=60
    )
    print(f"\n运动爱好者（75kg，25岁男性，每日运动60分钟）：")
    print(f"  基础需求：{active['base_need_ml']}ml")
    print(f"  活动调整：{active['activity_adjusted_ml']}ml")
    print(f"  运动额外：{active['exercise_addition_ml']}ml")
    print(f"  总需求：{active['total_need_ml']}ml")
    
    # 孕期女性
    pregnant = calculate_daily_water_needs(
        weight_kg=60,
        age=28,
        gender="female",
        activity_level=ActivityLevel.LIGHT,
        climate=ClimateType.TEMPERATE,
        is_pregnant=True
    )
    print(f"\n孕期女性（60kg，28岁）：")
    print(f"  基础需求：{pregnant['base_need_ml']}ml")
    print(f"  孕期额外：{pregnant['pregnancy_addition_ml']}ml")
    print(f"  总需求：{pregnant['total_need_ml']}ml")


def example_drinking_schedule():
    """示例2：生成饮水时间表"""
    print("\n" + "="*60)
    print("示例2：生成饮水时间表")
    print("="*60)
    
    # 生成一天8次饮水时间表
    schedule = get_drinking_schedule(
        target_ml=2400,
        wake_time="06:30",
        sleep_time="22:30",
        intervals=8
    )
    
    print(f"\n每日饮水计划（目标2400ml，8次）：")
    print("-"*40)
    for entry in schedule:
        print(f"  {entry['time']} - {entry['amount_ml']}ml "
              f"（累计：{entry['cumulative_ml']}ml，{entry['percentage']}%）")


def example_beverage_hydration():
    """示例3：不同饮料的补水效果"""
    print("\n" + "="*60)
    print("示例3：不同饮料的补水效果对比")
    print("="*60)
    
    beverages = [
        (BeverageType.WATER, 500, "纯净水"),
        (BeverageType.COFFEE, 300, "咖啡"),
        (BeverageType.TEA, 400, "茶"),
        (BeverageType.ALCOHOL_BEER, 500, "啤酒"),
        (BeverageType.JUICE, 300, "果汁"),
        (BeverageType.SPORTS_DRINK, 500, "运动饮料"),
    ]
    
    print(f"\n各饮料补水效果对比（相同容量参考）：")
    print("-"*60)
    print(f"{'饮料类型':<12} {'容量':<8} {'有效补水':<10} {'咖啡因':<10} {'效率'}")
    print("-"*60)
    
    for beverage_type, volume, name in beverages:
        result = calculate_beverage_hydration(beverage_type, volume)
        print(f"{name:<12} {result['volume_ml']}ml     "
              f"{result['effective_hydration_ml']}ml       "
              f"{result['caffeine_mg']:.0f}mg       "
              f"{result['hydration_efficiency']}%")


def example_exercise_hydration():
    """示例4：运动补水计划"""
    print("\n" + "="*60)
    print("示例4：运动补水计划")
    print("="*60)
    
    # 中等强度跑步
    plan = get_exercise_hydration_plan(
        exercise_type="running",
        duration_minutes=45,
        intensity="moderate",
        weight_kg=70,
        temperature_celsius=25
    )
    
    print(f"\n45分钟跑步补水计划：")
    print(f"  预估出汗量：{plan['estimated_sweat_loss_ml']}ml")
    print(f"\n  运动前补水：")
    print(f"    - 2小时前：{plan['pre_exercise']['2_hours_before_ml']}ml")
    print(f"    - 30分钟前：{plan['pre_exercise']['30_min_before_ml']}ml")
    print(f"\n  运动中补水：")
    print(f"    - 每{plan['during_exercise']['interval_minutes']}分钟：{plan['during_exercise']['per_interval_ml']}ml")
    print(f"    - 总计：{plan['during_exercise']['total_ml']}ml")
    print(f"\n  运动后补水：")
    print(f"    - 建议：{plan['post_exercise']['recommended_ml']}ml")
    print(f"    - 时间：{plan['post_exercise']['timing']}")
    print(f"\n  其他建议：")
    print(f"    - 需要电解质：{'是' if plan['electrolyte_needed'] else '否'}")
    print(f"    - 推荐运动饮料：{'是' if plan['sports_drink_recommended'] else '否'}")


def example_caffeine_impact():
    """示例5：咖啡因影响分析"""
    print("\n" + "="*60)
    print("示例5：咖啡因影响分析")
    print("="*60)
    
    # 分析不同时间点喝咖啡的影响
    caffeine_amounts = [100, 200, 400]  # mg
    
    print(f"\n咖啡因代谢分析：")
    print("-"*70)
    
    for amount in caffeine_amounts:
        print(f"\n摄入 {amount}mg 咖啡因：")
        for hours in [0, 2, 5.5, 8, 12]:
            impact = calculate_caffeine_impact(amount, hours)
            print(f"  {hours}小时后：剩余{impact['remaining_caffeine_mg']:.0f}mg "
                  f"({impact['metabolized_percent']:.0f}%已代谢) "
                  f"{'⚠️影响睡眠' if impact['sleep_disruption_risk'] else '✓不影响睡眠'}")


def example_hydration_tracker():
    """示例6：使用水分追踪器"""
    print("\n" + "="*60)
    print("示例6：使用水分追踪器")
    print("="*60)
    
    # 创建追踪器
    tracker = HydrationTracker(
        weight_kg=70,
        activity_level=ActivityLevel.MODERATE,
        climate=ClimateType.TEMPERATE
    )
    
    # 模拟一天的饮水记录
    today = date.today()
    
    # 早上
    tracker.log_water(250, datetime(today.year, today.month, today.day, 7, 30), log_date=today)
    tracker.log_coffee(300, caffeine_mg=120, 
                       timestamp=datetime(today.year, today.month, today.day, 8, 0), 
                       log_date=today)
    
    # 上午
    tracker.log_water(500, datetime(today.year, today.month, today.day, 10, 0), log_date=today)
    tracker.log_tea(400, caffeine_mg=80,
                    timestamp=datetime(today.year, today.month, today.day, 11, 0),
                    log_date=today)
    
    # 中午
    tracker.log_water(300, datetime(today.year, today.month, today.day, 13, 0), log_date=today)
    
    # 下午
    tracker.log_beverage(
        BeverageType.JUICE,
        200,
        timestamp=datetime(today.year, today.month, today.day, 15, 30),
        log_date=today
    )
    tracker.log_water(400, datetime(today.year, today.month, today.day, 17, 0), log_date=today)
    
    # 获取当前状态
    status = tracker.get_current_status()
    print(f"\n当前水分状态：")
    print(f"  风险等级：{status['risk_level']}")
    print(f"  水分状态：{status['hydration_status']}")
    print(f"  完成进度：{status['completion_percentage']:.1f}%")
    print(f"  当前摄入：{status['current_intake_ml']:.0f}ml")
    print(f"  目标量：{status['target_ml']:.0f}ml")
    print(f"  还需补充：{status['deficit_ml']:.0f}ml")
    
    # 获取饮水提醒
    reminder = tracker.get_drinking_reminder()
    print(f"\n饮水提醒：")
    print(f"  需要提醒：{'是' if reminder['should_remind'] else '否'}")
    print(f"  消息：{reminder['message']}")
    
    # 获取每日报告
    report = tracker.get_daily_report()
    print(f"\n每日水分报告：")
    print(f"  总摄入量：{report['summary']['total_intake_ml']}ml")
    print(f"  有效补水：{report['summary']['effective_hydration_ml']}ml")
    print(f"  补水效率：{report['hydration_efficiency']}%")
    print(f"  纯水占比：{report['summary']['pure_water_percentage']}%")


def example_food_water():
    """示例7：食物水分估算"""
    print("\n" + "="*60)
    print("示例7：从食物中获取的水分")
    print("="*60)
    
    # 一天的食物水分估算
    foods = [
        {"name": "watermelon", "weight_g": 200, "water_percent": FOOD_WATER_CONTENT["watermelon"]},
        {"name": "cucumber", "weight_g": 100, "water_percent": FOOD_WATER_CONTENT["cucumber"]},
        {"name": "orange", "weight_g": 150, "water_percent": FOOD_WATER_CONTENT["orange"]},
        {"name": "soup", "weight_g": 300, "water_percent": FOOD_WATER_CONTENT["soup"]},
        {"name": "rice", "weight_g": 200, "water_percent": FOOD_WATER_CONTENT["rice"]},
    ]
    
    total_water = estimate_water_from_foods(foods)
    
    print(f"\n食物水分估算：")
    print("-"*50)
    for food in foods:
        water = food["weight_g"] * food["water_percent"] / 100
        print(f"  {food['name']:<12} {food['weight_g']}g × {food['water_percent']}% = {water:.0f}ml")
    print("-"*50)
    print(f"  总计：{total_water:.0f}ml")


def example_weather_adjustment():
    """示例8：天气影响调整"""
    print("\n" + "="*60)
    print("示例8：天气对水分需求的影响")
    print("="*60)
    
    base_target = 2400  # 基础目标
    
    conditions = [
        (10, 50, False, "凉爽阴天"),
        (22, 50, False, "温和天气"),
        (22, 50, True, "晴天"),
        (30, 50, True, "炎热晴天"),
        (35, 80, True, "高温高湿"),
        (35, 30, True, "高温干燥"),
    ]
    
    print(f"\n不同天气条件下的水分需求调整：")
    print(f"基础目标：{base_target}ml")
    print("-"*60)
    
    for temp, humidity, sunny, desc in conditions:
        adjusted = get_weather_adjusted_target(base_target, temp, humidity, sunny)
        increase = adjusted - base_target
        pct = (increase / base_target) * 100
        print(f"  {desc:<12} ({temp}°C, {humidity}%湿度): {adjusted}ml "
              f"({'+' if increase > 0 else ''}{increase}ml, {pct:+.1f}%)")


def example_oral_rehydration():
    """示例9：口服补液盐方案"""
    print("\n" + "="*60)
    print("示例9：口服补液盐方案（轻度脱水）")
    print("="*60)
    
    # 轻度脱水
    mild = calculate_oral_rehydration_solution(weight_kg=70, dehydration_level="mild")
    print(f"\n轻度脱水补液方案（70kg成人）：")
    print(f"  建议总量：{mild['recommended_total_ml']}ml")
    print(f"\n  服用方法：")
    print(f"    第一小时：{mild['administration']['first_hour_ml']}ml")
    print(f"    后续3-4小时：{mild['administration']['next_3_4_hours_ml']}ml")
    print(f"    建议：{mild['administration']['sips']}")
    
    print(f"\n  简易家庭配方：")
    recipe = mild['simplified_home_recipe']
    print(f"    水：{recipe['water_ml']}ml")
    print(f"    盐：{recipe['salt_g']}g")
    print(f"    糖：{recipe['sugar_g']}g")
    
    # 中度脱水
    moderate = calculate_oral_rehydration_solution(weight_kg=70, dehydration_level="moderate")
    print(f"\n中度脱水补液方案：")
    print(f"  建议总量：{moderate['recommended_total_ml']}ml")
    print(f"  ⚠️ {moderate['warning']}")


def example_weekly_summary():
    """示例10：周总结报告"""
    print("\n" + "="*60)
    print("示例10：周水分摄入总结")
    print("="*60)
    
    tracker = HydrationTracker(weight_kg=70)
    
    # 模拟一周数据
    today = date.today()
    for i in range(7):
        d = today - timedelta(days=i)
        # 模拟不同的饮水量
        amounts = [1800, 2200, 2000, 2400, 1900, 2500, 2100]
        tracker.log_water(amounts[i], log_date=d)
    
    summary = tracker.get_weekly_summary()
    
    print(f"\n本周水分摄入总结：")
    print(f"  周起始日：{summary['week_start']}")
    print(f"  记录天数：{summary['days_logged']}天")
    print(f"  总摄入量：{summary['total_intake_ml']}ml")
    print(f"  有效补水：{summary['total_effective_ml']}ml")
    print(f"  平均完成率：{summary['average_completion']}%")
    print(f"\n  每日详情：")
    for day in summary['daily_summaries']:
        print(f"    {day['date']}：{day['intake_ml']}ml（完成{day['completion']}%）")


def main():
    """运行所有示例"""
    print("\n" + "="*60)
    print("       Hydration Utils - 水分追踪工具使用示例")
    print("="*60)
    
    example_basic_calculation()
    example_drinking_schedule()
    example_beverage_hydration()
    example_exercise_hydration()
    example_caffeine_impact()
    example_hydration_tracker()
    example_food_water()
    example_weather_adjustment()
    example_oral_rehydration()
    example_weekly_summary()
    
    print("\n" + "="*60)
    print("       所有示例运行完成！")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()