"""
Sleep Cycle Utilities 使用示例

演示:
- 计算起床时间
- 计算入睡时间
- 睡眠债务计算
- 小睡建议
- 昼夜节律分析
- 睡眠阶段时间线
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sleep_cycle_utils.mod import (
    SleepCycleCalculator, SleepQuality, NapType,
    calculate_wake_times, calculate_bed_times,
    get_optimal_sleep_duration, format_sleep_duration,
    get_quality_description, recommend_nap
)
from datetime import datetime, time


def example_calculate_wake_times():
    """示例：计算起床时间"""
    print("\n" + "="*60)
    print("示例 1：计算起床时间")
    print("="*60)
    
    calc = SleepCycleCalculator()
    
    # 设置入睡时间（比如今晚22:00）
    bed_time = datetime.now().replace(hour=22, minute=0, second=0, microsecond=0)
    
    print(f"\n如果 {bed_time.strftime('%H:%M')} 入睡，推荐的起床时间：")
    
    wake_times = calc.calculate_wake_times(bed_time)
    
    for result in wake_times:
        print(f"\n{result.target_time.strftime('%H:%M')} 起床")
        print(f"  周期数: {result.cycle_count} 个")
        print(f"  睡眠时长: {format_sleep_duration(result.duration_minutes)}")
        print(f"  睡眠质量: {get_quality_description(result.quality)}")
        print(f"  建议: {result.recommendation}")


def example_calculate_bed_times():
    """示例：计算入睡时间"""
    print("\n" + "="*60)
    print("示例 2：计算入睡时间")
    print("="*60)
    
    calc = SleepCycleCalculator()
    
    # 设置目标起床时间（比如明天7:00）
    wake_time = datetime.now().replace(hour=7, minute=0, second=0, microsecond=0)
    # 如果当前时间超过目标时间，则假设是明天
    if datetime.now().hour >= wake_time.hour:
        wake_time += datetime.timedelta(days=1)
    
    print(f"\n如果需要在 {wake_time.strftime('%H:%M')} 起床，推荐的入睡时间：")
    
    bed_times = calc.calculate_bed_times(wake_time)
    
    for result in bed_times:
        print(f"\n{result.target_time.strftime('%H:%M')} 入睡")
        print(f"  周期数: {result.cycle_count} 个")
        print(f"  睡眠时长: {format_sleep_duration(result.duration_minutes)}")
        print(f"  睡眠质量: {get_quality_description(result.quality)}")
        print(f"  建议: {result.recommendation}")


def example_sleep_debt():
    """示例：睡眠债务计算"""
    print("\n" + "="*60)
    print("示例 3：睡眠债务计算")
    print("="*60)
    
    calc = SleepCycleCalculator()
    
    # 一周的睡眠记录（假设目标8小时）
    sleep_records = [
        {"date": "2024-01-01", "hours": 6.5},
        {"date": "2024-01-02", "hours": 5.0},   # 睡眠严重不足
        {"date": "2024-01-03", "hours": 7.0},
        {"date": "2024-01-04", "hours": 6.0},
        {"date": "2024-01-05", "hours": 7.5},
        {"date": "2024-01-06", "hours": 8.0},   # 正常
        {"date": "2024-01-07", "hours": 5.5},   # 又不足
    ]
    
    debt = calc.calculate_sleep_debt(sleep_records, target_hours=8, recovery_days=3)
    
    print(f"\n睡眠债务分析：")
    print(f"  目标睡眠时长: {debt.target_hours} 小时/天")
    print(f"  实际平均时长: {debt.actual_hours:.1f} 小时/天")
    print(f"  累计睡眠债务: {debt.debt_hours} 小时 ({debt.debt_minutes} 分钟)")
    print(f"  累计天数: {debt.accumulated_days} 天")
    
    print(f"\n恢复计划（3天）：")
    for day in debt.recovery_plan:
        print(f"  第{day['day']}天: 睡眠 {day['total_hours']} 小时（额外 {day['extra_hours']} 小时）")


def example_nap_recommendation():
    """示例：小睡建议"""
    print("\n" + "="*60)
    print("示例 4：小睡建议")
    print("="*60)
    
    calc = SleepCycleCalculator()
    
    # 不同时间的小睡建议
    times_to_check = [
        (datetime.now().replace(hour=9, minute=0), "上午"),
        (datetime.now().replace(hour=14, minute=0), "下午"),
        (datetime.now().replace(hour=17, minute=0), "傍晚"),
    ]
    
    for check_time, period_name in times_to_check:
        nap = calc.get_nap_recommendation(check_time)
        print(f"\n{period_name} ({check_time.strftime('%H:%M')}) 小睡建议：")
        print(f"  类型: {nap.nap_type.value}")
        print(f"  时长: {nap.duration_minutes} 分钟")
        print(f"  最佳时段: {nap.best_time_start.strftime('%H:%M')} - {nap.best_time_end.strftime('%H:%M')}")
        print(f"  好处: {', '.join(nap.benefits)}")
        print(f"  注意: {', '.join(nap.warnings)}")
    
    # 不同类型小睡对比
    print("\n\n不同类型小睡对比：")
    for nap_type in [NapType.POWER, NapType.SHORT, NapType.IDEAL]:
        nap = calc.get_nap_recommendation(datetime.now(), nap_type)
        print(f"\n{nap_type.value} 小睡:")
        print(f"  时长: {nap.duration_minutes} 分钟")
        print(f"  好处: {nap.benefits[0]}")


def example_circadian_rhythm():
    """示例：昼夜节律分析"""
    print("\n" + "="*60)
    print("示例 5：昼夜节律分析")
    print("="*60)
    
    calc = SleepCycleCalculator()
    
    # 分析不同的睡眠习惯
    profiles = [
        ("早起型", time(6, 0), time(22, 0), 30),
        ("晚睡型", time(9, 0), time(1, 0), 25),
        ("中间型", time(7, 30), time(23, 30), 35),
        ("极度早起", time(5, 0), time(21, 0), 40),
    ]
    
    for name, wake_time, bed_time, age in profiles:
        analysis = calc.analyze_circadian_rhythm(wake_time, bed_time, age)
        
        print(f"\n{name}（{age}岁）：")
        print(f"  起床时间: {wake_time.strftime('%H:%M')}")
        print(f"  入睡时间: {bed_time.strftime('%H:%M')}")
        print(f"  睡眠类型: {analysis['chronotype_name']}")
        print(f"  睡眠时长: {analysis['sleep_duration_hours']} 小时")
        print(f"  睡眠质量: {analysis['sleep_quality']}")
        print(f"  最佳时段: {analysis['peak_performance_hours']['start']} - {analysis['peak_performance_hours']['end']}")
        print(f"  能量低谷: {analysis['energy_low_hours']['start']} - {analysis['energy_low_hours']['end']}")
        print(f"  建议睡眠: {analysis['recommended_hours']} 小时")


def example_sleep_stages_timeline():
    """示例：睡眠阶段时间线"""
    print("\n" + "="*60)
    print("示例 6：睡眠阶段时间线")
    print("="*60)
    
    calc = SleepCycleCalculator()
    
    # 设置入睡时间
    bed_time = datetime.now().replace(hour=22, minute=0, second=0, microsecond=0)
    
    timeline = calc.get_sleep_stages_timeline(bed_time, cycle_count=5)
    
    print(f"\n从 {bed_time.strftime('%H:%M')} 开始的睡眠阶段分布：")
    
    total_deep = 0
    total_rem = 0
    
    for cycle in timeline:
        print(f"\n周期 {cycle['cycle']} ({cycle['start_time']} - {cycle['end_time']}):")
        for stage in cycle['stages']:
            stage_name = {
                'light': '浅睡',
                'deep': '深睡',
                'rem': 'REM'
            }.get(stage['stage'], stage['stage'])
            print(f"  {stage_name}: {stage['duration_minutes']}分钟 ({stage['percentage']}%)")
            
            if stage['stage'] == 'deep':
                total_deep += stage['duration_minutes']
            elif stage['stage'] == 'rem':
                total_rem += stage['duration_minutes']
        
        print(f"  最佳起床窗口: {cycle['best_wake_window']['start']} - {cycle['best_wake_window']['end']}")
    
    print(f"\n总结:")
    print(f"  总深睡时间: {total_deep} 分钟 ({total_deep/60:.1f} 小时)")
    print(f"  总REM时间: {total_rem} 分钟 ({total_rem/60:.1f} 小时)")
    print(f"  深睡集中在前半夜，REM集中在后半夜")


def example_sleep_window():
    """示例：最佳睡眠窗口"""
    print("\n" + "="*60)
    print("示例 7：最佳睡眠窗口计算")
    print("="*60)
    
    calc = SleepCycleCalculator()
    
    # 设置目标起床时间
    wake_time = datetime.now().replace(hour=7, minute=0, second=0, microsecond=0)
    
    # 计算不同睡眠时长目标的窗口
    durations = [7.5, 8, 9, 6]
    
    print(f"\n目标起床时间: {wake_time.strftime('%H:%M')}")
    
    for duration in durations:
        window = calc.calculate_optimal_sleep_window(wake_time, preferred_duration_hours=duration)
        
        print(f"\n目标睡眠 {duration} 小时：")
        print(f"  入睡时间: {window.start_time.strftime('%H:%M')}")
        print(f"  起床时间: {window.end_time.strftime('%H:%M')}")
        print(f"  实际周期: {window.cycle_count} 个")
        print(f"  睡眠评分: {window.score}/100")
        print(f"  睡眠质量: {get_quality_description(window.quality)}")


def example_convenience_functions():
    """示例：便捷函数"""
    print("\n" + "="*60)
    print("示例 8：便捷函数")
    print("="*60)
    
    # 快速计算起床时间
    bed_time = datetime.now().replace(hour=22, minute=0)
    wake_times = calculate_wake_times(bed_time)
    
    print(f"\n快速计算 - {bed_time.strftime('%H:%M')} 入睡后的起床时间：")
    for r in wake_times[:2]:
        print(f"  {r.target_time.strftime('%H:%M')} ({r.cycle_count}周期)")
    
    # 快速计算入睡时间
    wake_time = datetime.now().replace(hour=7, minute=0)
    bed_times = calculate_bed_times(wake_time)
    
    print(f"\n快速计算 - {wake_time.strftime('%H:%M')} 起床前的入睡时间：")
    for r in bed_times[:2]:
        print(f"  {r.target_time.strftime('%H:%M')} ({r.cycle_count}周期)")
    
    # 最佳睡眠时长
    for cycles in [3, 4, 5, 6]:
        duration = get_optimal_sleep_duration(cycles)
        print(f"\n{cycles}周期最佳时长: {format_sleep_duration(duration)}")
    
    # 小睡建议
    nap = recommend_nap(14, "low")
    print(f"\n下午2点低能量时的小睡建议：")
    print(f"  类型: {nap.nap_type.value}")
    print(f"  时长: {nap.duration_minutes} 分钟")


def example_real_world_scenario():
    """示例：真实场景"""
    print("\n" + "="*60)
    print("示例 9：真实场景 - 工作日睡眠规划")
    print("="*60)
    
    calc = SleepCycleCalculator()
    
    # 场景：明天需要7:30起床上班
    wake_time = datetime.now().replace(hour=7, minute=30)
    
    print(f"\n场景：明天需要 {wake_time.strftime('%H:%M')} 起床上班")
    
    # 获取推荐入睡时间
    bed_times = calc.calculate_bed_times(wake_time, min_cycles=4, max_cycles=5)
    
    # 找到5周期的推荐（最理想）
    ideal = None
    for r in bed_times:
        if r.cycle_count == 5:
            ideal = r
            break
    
    if ideal:
        print(f"\n推荐入睡时间: {ideal.target_time.strftime('%H:%M')}")
        print(f"  这样可以获得约7.5小时的理想睡眠")
        print(f"  在周期末尾醒来，感觉最清醒")
    
    # 如果现在的时间
    current_hour = datetime.now().hour
    current_minute = datetime.now().minute
    current_time_str = f"{current_hour:02d}:{current_minute:02d}"
    
    print(f"\n当前时间: {current_time_str}")
    
    # 判断是否有足够时间
    if ideal:
        ideal_hour = ideal.target_time.hour
        if current_hour < ideal_hour - 1:
            print(f"  ✓ 还有足够时间准备入睡")
        elif current_hour < ideal_hour:
            print(f"  ⚠ 入睡时间快到了，开始准备")
        else:
            print(f"  ⚠ 已过了推荐入睡时间，考虑下一个周期选项")
    
    # 计算最晚可行的入睡时间
    min_sleep = bed_times[-1]  # 4周期
    print(f"\n最晚入睡时间（4周期）: {min_sleep.target_time.strftime('%H:%M')}")
    print(f"  仍可获得约6小时睡眠")


def run_all_examples():
    """运行所有示例"""
    print("="*60)
    print("Sleep Cycle Utilities 使用示例")
    print("="*60)
    
    example_calculate_wake_times()
    example_calculate_bed_times()
    example_sleep_debt()
    example_nap_recommendation()
    example_circadian_rhythm()
    example_sleep_stages_timeline()
    example_sleep_window()
    example_convenience_functions()
    example_real_world_scenario()
    
    print("\n" + "="*60)
    print("示例运行完毕")
    print("="*60)


if __name__ == "__main__":
    # 需要在函数中添加 timedelta 的引用
    import datetime
    
    run_all_examples()