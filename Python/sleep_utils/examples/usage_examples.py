"""
Sleep Utils 使用示例

演示睡眠工具的各种用法：
- 睡眠周期计算
- 最佳作息时间规划
- 睡眠负债追踪
- 小睡建议
- 昼夜节律分析
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from mod import (
    calculate_wake_times, calculate_bedtimes,
    calculate_sleep_debt, suggest_nap,
    analyze_circadian_rhythm,
    get_sleep_stage_distribution,
    calculate_sleep_efficiency,
    when_to_wake, when_to_sleep,
    format_duration,
    SleepQuality
)


def example_1_calculate_wake_times():
    """示例1: 根据就寝时间计算最佳起床时间"""
    print("=" * 50)
    print("示例1: 根据就寝时间计算最佳起床时间")
    print("=" * 50)
    
    # 假设今晚23:00就寝
    bedtime = datetime.now().replace(hour=23, minute=0, second=0, microsecond=0)
    print(f"就寝时间: {bedtime.strftime('%H:%M')}")
    
    # 计算推荐的起床时间
    results = calculate_wake_times(bedtime)
    
    print("\n推荐的起床时间（按质量排序）：")
    for i, r in enumerate(results, 1):
        quality_level = SleepQuality.from_score(r.quality_score)
        print(f"{i}. {r.wake_time.strftime('%H:%M')}起床 "
              f"- {r.cycles}个睡眠周期 "
              f"- {r.total_sleep_minutes / 60:.1f}小时 "
              f"- 质量: {r.quality_score:.1f}/10 ({quality_level})")
    
    print(f"\n最佳建议: {results[0].wake_time.strftime('%H:%M')}起床，"
          f"可获得{results[0].quality_score:.1f}分的睡眠质量")


def example_2_calculate_bedtimes():
    """示例2: 根据起床时间计算最佳就寝时间"""
    print("\n" + "=" * 50)
    print("示例2: 根据起床时间计算最佳就寝时间")
    print("=" * 50)
    
    # 需要明天早上7:00起床
    wake_time = datetime.now().replace(hour=7, minute=0, second=0, microsecond=0)
    print(f"期望起床时间: {wake_time.strftime('%H:%M')}")
    
    # 计算推荐的就寝时间
    results = calculate_bedtimes(wake_time)
    
    print("\n推荐的就寝时间（按质量排序）：")
    for i, r in enumerate(results, 1):
        quality_level = SleepQuality.from_score(r.quality_score)
        print(f"{i}. {r.bedtime.strftime('%H:%M')}就寝 "
              f"- {r.cycles}个睡眠周期 "
              f"- {r.total_sleep_minutes / 60:.1f}小时 "
              f"- 质量: {r.quality_score:.1f}/10 ({quality_level})")
    
    print(f"\n最佳建议: {results[0].bedtime.strftime('%H:%M')}就寝")


def example_3_sleep_debt():
    """示例3: 计算睡眠负债"""
    print("\n" + "=" * 50)
    print("示例3: 睡眠负债追踪")
    print("=" * 50)
    
    print("目标睡眠时长: 7.5小时/天")
    
    # 过去一周的睡眠数据（小时）
    sleep_data = [6.5, 7.0, 5.5, 8.0, 6.0, 7.5, 6.0]
    days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    
    print("\n实际睡眠记录:")
    for day, hours in zip(days, sleep_data):
        diff = hours - 7.5
        if diff >= 0:
            print(f"  {day}: {hours}小时 (达标 ✓)")
        else:
            print(f"  {day}: {hours}小时 (少睡{-diff:.1f}小时)")
    
    # 计算睡眠负债
    debt = calculate_sleep_debt(target_hours=7.5, actual_hours_list=sleep_data, days=7)
    
    print(f"\n睡眠负债统计:")
    print(f"  累计负债: {debt['debt_hours']:.1f}小时 ({debt['debt_minutes']}分钟)")
    print(f"  平均睡眠: {debt['average_actual']:.1f}小时/天")
    print(f"  负债比例: {debt['debt_percentage']:.1f}%")
    print(f"  负债状态: {debt['status']}")
    
    if debt['days_to_recover'] > 0:
        print(f"  恢复建议: 每天多睡1小时，需要{debt['days_to_recover']}天补回")


def example_4_nap_suggestion():
    """示例4: 小睡建议"""
    print("\n" + "=" * 50)
    print("示例4: 小睡建议")
    print("=" * 50)
    
    # 不同时长的小睡建议
    durations = [20, 30, 45, 60, 90]
    
    print("不同时长的小睡效果分析:")
    for dur in durations:
        result = suggest_nap(duration_minutes=dur)
        suggestion = result['suggestions'][0]
        status = "✓ 推荐" if suggestion['recommended'] else "✗ 不推荐"
        print(f"\n{dur}分钟小睡: {status}")
        print(f"  类型: {suggestion['type']}")
        print(f"  描述: {suggestion['description']}")
        if not suggestion['recommended']:
            print(f"  建议: {suggestion['tip']}")
    
    # 当前时间的小睡适合度
    print("\n下午时间段的小睡建议:")
    for hour in [13, 14, 15, 17, 20]:
        result = suggest_nap(current_hour=hour)
        time_advice = None
        for s in result['suggestions']:
            if 'time_advice' in s:
                time_advice = s['time_advice'][0]
                break
        if time_advice:
            print(f"  {hour}:00 - {time_advice['suitability']} ({time_advice['period']})")


def example_5_circadian_rhythm():
    """示例5: 昼夜节律分析"""
    print("\n" + "=" * 50)
    print("示例5: 昼夜节律分析")
    print("=" * 50)
    
    # 分析不同作息习惯的昼夜节律
    schedules = [
        ("早起型", datetime(2024, 1, 1, 5, 30), datetime(2024, 1, 1, 21, 30)),
        ("标准型", datetime(2024, 1, 1, 7, 0), datetime(2024, 1, 1, 23, 0)),
        ("晚睡型", datetime(2024, 1, 1, 9, 30), datetime(2024, 1, 1, 1, 30)),
    ]
    
    for name, wake, bed in schedules:
        print(f"\n{name}作息分析:")
        print(f"  起床: {wake.strftime('%H:%M')}")
        print(f"  就寝: {bed.strftime('%H:%M')}")
        
        result = analyze_circadian_rhythm(wake, bed)
        print(f"  时型: {result['chronotype']}")
        
        if result['recommendations']:
            print("  建议:")
            for rec in result['recommendations'][:2]:
                print(f"    - {rec}")
        
        if result['alerts']:
            print("  提醒:")
            for alert in result['alerts'][:2]:
                print(f"    - {alert}")


def example_6_sleep_stages():
    """示例6: 睡眠阶段分布"""
    print("\n" + "=" * 50)
    print("示例6: 睡眠阶段分布分析")
    print("=" * 50)
    
    # 分析不同睡眠时长对应的阶段分布
    for cycles in [4, 5, 6]:
        stages = get_sleep_stage_distribution(cycles)
        
        print(f"\n{cycles}个睡眠周期 ({stages['total_hours']}小时):")
        for stage_name, info in stages['stages'].items():
            stage_display = {
                'light_sleep': '浅睡眠',
                'deep_sleep': '深度睡眠',
                'rem_sleep': 'REM睡眠'
            }
            print(f"  {stage_display[stage_name]}: "
                  f"{format_duration(info['minutes'])} "
                  f"({info['percentage']}%)")
            print(f"    作用: {info['description']}")


def example_7_sleep_efficiency():
    """示例7: 睡眠效率分析"""
    print("\n" + "=" * 50)
    print("示例7: 睡眠效率分析")
    print("=" * 50)
    
    # 分析不同睡眠效率
    cases = [
        ("高效睡眠者", 480, 450),  # 8小时在床，7.5小时睡着
        ("正常睡眠者", 480, 420),  # 8小时在床，7小时睡着
        ("入睡困难者", 480, 360),  # 8小时在床，6小时睡着
        ("失眠者", 480, 300),      # 8小时在床，5小时睡着
    ]
    
    for name, in_bed, actual in cases:
        result = calculate_sleep_efficiency(in_bed, actual)
        
        print(f"\n{name}:")
        print(f"  在床时间: {format_duration(in_bed)}")
        print(f"  实际睡眠: {format_duration(actual)}")
        print(f"  睡眠效率: {result['efficiency_percentage']}%")
        print(f"  评级: {result['rating']}")
        print(f"  说明: {result['description']}")


def example_8_quick_functions():
    """示例8: 便捷函数使用"""
    print("\n" + "=" * 50)
    print("示例8: 便捷函数快速查询")
    print("=" * 50)
    
    # 快速查询：今晚23:00睡觉，几点起床？
    print("今晚23:00就寝，推荐起床时间:")
    bedtime = datetime(2024, 1, 1, 23, 0)
    results = when_to_wake(bedtime)
    for r in results:
        print(f"  {r['wake_time']} - {r['cycles']}周期 - 质量{r['quality']:.1f}/10")
    
    # 快速查询：明天7:00起床，几点睡觉？
    print("\n明天7:00起床，推荐就寝时间:")
    wake_time = datetime(2024, 1, 1, 7, 0)
    results = when_to_sleep(wake_time)
    for r in results:
        print(f"  {r['bedtime']} - {r['cycles']}周期 - 质量{r['quality']:.1f}/10")


def example_9_custom_fall_asleep():
    """示例9: 自定义入睡时间"""
    print("\n" + "=" * 50)
    print("示例9: 自定义入睡时间")
    print("=" * 50)
    
    # 不同入睡速度的人
    bedtime = datetime(2024, 1, 1, 23, 0)
    
    print(f"就寝时间: {bedtime.strftime('%H:%M')}")
    print("\n不同入睡速度的起床时间:")
    
    for fall_asleep in [5, 15, 30, 45]:
        results = when_to_wake(bedtime, fall_asleep_minutes=fall_asleep)
        best = results[0]
        print(f"  入睡需要{fall_asleep}分钟: "
              f"{best['wake_time']}起床 ({best['cycles']}周期)")


def example_10_week_sleep_plan():
    """示例10: 一周睡眠计划"""
    print("\n" + "=" * 50)
    print("示例10: 一周睡眠计划生成")
    print("=" * 50)
    
    # 工作日早上7点起床，周末自由
    workday_wake = datetime(2024, 1, 1, 7, 0)
    
    print("工作日睡眠计划（7:00起床）:")
    workday_bed = calculate_bedtimes(workday_wake)
    print(f"  建议就寝: {workday_bed[0].bedtime.strftime('%H:%M')}")
    print(f"  睡眠时长: {workday_bed[0].total_sleep_minutes / 60:.1f}小时")
    print(f"  睡眠周期: {workday_bed[0].cycles}个")
    
    print("\n周末睡眠计划（可多睡一些）:")
    weekend_wake = datetime(2024, 1, 1, 9, 0)
    weekend_bed = calculate_bedtimes(weekend_wake)
    print(f"  建议就寝: {weekend_bed[0].bedtime.strftime('%H:%M')}")
    print(f"  睡眠时长: {weekend_bed[0].total_sleep_minutes / 60:.1f}小时")


def main():
    """运行所有示例"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "Sleep Utils 使用示例" + " " * 21 + "║")
    print("╚" + "═" * 58 + "╝")
    
    example_1_calculate_wake_times()
    example_2_calculate_bedtimes()
    example_3_sleep_debt()
    example_4_nap_suggestion()
    example_5_circadian_rhythm()
    example_6_sleep_stages()
    example_7_sleep_efficiency()
    example_8_quick_functions()
    example_9_custom_fall_asleep()
    example_10_week_sleep_plan()
    
    print("\n" + "=" * 60)
    print("更多用法请参考 README.md")
    print("=" * 60)


if __name__ == "__main__":
    main()