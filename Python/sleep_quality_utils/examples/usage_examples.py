#!/usr/bin/env python3
"""
Sleep Quality Utils 使用示例

演示睡眠质量分析工具的各种功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from mod import (
    SleepSession, SleepStage, SleepQuality, SleepTracker,
    calculate_sleep_quality_score,
    get_quality_level,
    calculate_sleep_debt,
    calculate_sleep_efficiency,
    suggest_optimal_sleep_time,
    analyze_sleep_patterns,
    analyze_sleep_cycles,
    analyze_sleep_session,
    calculate_optimal_wake_times,
    format_sleep_duration,
    get_sleep_stage_distribution,
    estimate_sleep_stages,
    get_nap_recommendation,
    calculate_ideal_nap_time,
    OPTIMAL_SLEEP_HOURS
)


def example_basic_sleep_analysis():
    """基本睡眠分析示例"""
    print("=" * 60)
    print("示例1: 基本睡眠分析")
    print("=" * 60)
    
    # 创建一个典型的睡眠记录
    session = SleepSession(
        start_time=datetime(2026, 4, 29, 23, 30),
        end_time=datetime(2026, 4, 30, 7, 15),
        awakenings=1,
        awakening_duration_minutes=10,
        sleep_stages={
            SleepStage.DEEP: 85,
            SleepStage.LIGHT: 245,
            SleepStage.REM: 90
        },
        rating=7,
        notes="睡前喝了一杯茶"
    )
    
    print(f"\n睡眠记录:")
    print(f"  入睡时间: {session.start_time.strftime('%Y-%m-%d %H:%M')}")
    print(f"  醒来时间: {session.end_time.strftime('%Y-%m-%d %H:%M')}")
    print(f"  总在床时间: {format_sleep_duration(session.total_time_in_bed)}")
    print(f"  总睡眠时间: {format_sleep_duration(session.total_sleep_time)}")
    print(f"  夜间醒来: {session.awakenings} 次")
    print(f"  醒来时长: {session.awakening_duration_minutes} 分钟")
    
    # 计算睡眠效率
    efficiency = calculate_sleep_efficiency(session)
    print(f"\n睡眠效率: {efficiency:.1f}%")
    
    # 计算睡眠质量评分
    score = calculate_sleep_quality_score(session, "adult")
    level = get_quality_level(score)
    print(f"睡眠质量评分: {score:.1f}")
    print(f"睡眠质量等级: {level.value}")
    
    # 睡眠阶段分布
    distribution = get_sleep_stage_distribution(session)
    print(f"\n睡眠阶段分布:")
    print(f"  深睡眠: {distribution['deep']:.1f}%")
    print(f"  浅睡眠: {distribution['light']:.1f}%")
    print(f"  REM睡眠: {distribution['rem']:.1f}%")
    print(f"  清醒: {distribution['awake']:.1f}%")


def example_comprehensive_analysis():
    """综合睡眠分析示例"""
    print("\n" + "=" * 60)
    print("示例2: 综合睡眠分析")
    print("=" * 60)
    
    session = SleepSession(
        start_time=datetime(2026, 4, 29, 22, 45),
        end_time=datetime(2026, 4, 30, 6, 30),
        awakenings=2,
        awakening_duration_minutes=20,
        sleep_stages={
            SleepStage.DEEP: 70,
            SleepStage.LIGHT: 280,
            SleepStage.REM: 75
        }
    )
    
    analysis = analyze_sleep_session(session, "adult", 8.0)
    
    print(f"\n综合分析结果:")
    print(f"  质量评分: {analysis.quality_score:.1f}")
    print(f"  质量等级: {analysis.quality_level.value}")
    print(f"  睡眠效率: {analysis.efficiency:.1f}%")
    print(f"  睡眠时长: {analysis.total_sleep_hours:.2f} 小时")
    print(f"  深睡眠占比: {analysis.deep_sleep_percentage:.1f}%")
    print(f"  REM睡眠占比: {analysis.rem_sleep_percentage:.1f}%")
    print(f"  睡眠债务: {analysis.sleep_debt_hours:.2f} 小时")
    
    print(f"\n改进建议:")
    for i, rec in enumerate(analysis.recommendations, 1):
        print(f"  {i}. {rec}")


def example_optimal_sleep_time():
    """最佳睡眠时间建议示例"""
    print("\n" + "=" * 60)
    print("示例3: 最佳睡眠时间建议")
    print("=" * 60)
    
    # 需要在7点醒来，应该什么时候睡？
    wake_time = datetime(2026, 4, 30, 7, 0)
    
    print(f"\n目标醒来时间: {wake_time.strftime('%H:%M')}")
    print("\n建议入睡时间 (基于睡眠周期):")
    
    for cycles in [4, 5, 6]:
        bedtime, _ = suggest_optimal_sleep_time(wake_time, num_cycles=cycles)
        sleep_hours = cycles * 1.5  # 每周期1.5小时
        print(f"  {cycles}个周期 ({sleep_hours}小时): {bedtime.strftime('%H:%M')} 入睡")
    
    # 计划11点入睡，最佳醒来时间？
    print("\n如果23:00入睡，建议醒来时间:")
    bedtime = datetime(2026, 4, 29, 23, 0)
    wake_times = calculate_optimal_wake_times(bedtime)
    
    for wake, cycles in wake_times:
        print(f"  {wake.strftime('%H:%M')} ({cycles}个周期)")


def example_sleep_tracker():
    """睡眠追踪器示例"""
    print("\n" + "=" * 60)
    print("示例4: 睡眠追踪器（一周追踪）")
    print("=" * 60)
    
    tracker = SleepTracker(target_hours=8.0, age_group="adult")
    
    # 模拟一周的睡眠数据
    import random
    random.seed(42)
    
    base_date = datetime(2026, 4, 23, 23, 0)
    
    weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    
    print("\n睡眠记录:")
    for i, day in enumerate(weekdays):
        # 工作日睡得少一点，周末睡得多一点
        if i < 5:
            sleep_hours = 6.5 + random.random() * 1
        else:
            sleep_hours = 8 + random.random() * 1
        
        start = base_date + timedelta(days=i, hours=random.random()*2-1)
        end = start + timedelta(hours=sleep_hours)
        
        session = SleepSession(
            start_time=start,
            end_time=end,
            awakenings=random.randint(0, 2),
            awakening_duration_minutes=random.randint(0, 15),
            sleep_stages={
                SleepStage.DEEP: int(sleep_hours * 60 * 0.18),
                SleepStage.LIGHT: int(sleep_hours * 60 * 0.55),
                SleepStage.REM: int(sleep_hours * 60 * 0.22)
            }
        )
        
        tracker.add_session(session)
        
        quality = calculate_sleep_quality_score(session, "adult")
        print(f"  {day}: {format_sleep_duration(session.total_sleep_time)}, "
              f"效率 {session.sleep_efficiency:.0f}%, 质量分 {quality:.1f}")
    
    # 获取周报告
    weekly = tracker.get_weekly_report()
    
    print(f"\n周统计:")
    print(f"  平均睡眠时长: {weekly['average_sleep_hours']} 小时")
    print(f"  平均效率: {weekly['average_efficiency']}%")
    print(f"  平均质量分: {weekly['average_quality_score']}")
    print(f"  平均入睡时间: {weekly['average_bedtime']}")
    print(f"  平均醒来时间: {weekly['average_wake_time']}")
    print(f"  一致性评分: {weekly['consistency_score']}")
    
    print(f"\n最佳睡眠日: {weekly['best_day']['date']} (分数: {weekly['best_day']['score']})")
    print(f"最差睡眠日: {weekly['worst_day']['date']} (分数: {weekly['worst_day']['score']})")
    
    print(f"\n睡眠债务: {tracker.get_sleep_debt(7):.2f} 小时")
    print(f"趋势分析: {tracker.get_trend(7)}")


def example_sleep_debt():
    """睡眠债务示例"""
    print("\n" + "=" * 60)
    print("示例5: 睡眠债务计算")
    print("=" * 60)
    
    # 模拟一周睡眠不足的情况
    sessions = []
    base_date = datetime(2026, 4, 23, 23, 0)
    
    print("\n模拟一周睡眠:")
    for i in range(7):
        start = base_date + timedelta(days=i)
        # 每天睡6-7小时，目标8小时
        sleep_hours = 6 + (i % 2) * 0.5
        end = start + timedelta(hours=sleep_hours)
        sessions.append(SleepSession(start_time=start, end_time=end))
        print(f"  第{i+1}天: {sleep_hours:.1f} 小时")
    
    debt = calculate_sleep_debt(sessions, target_hours=8.0, days=7)
    print(f"\n累计睡眠债务: {debt:.2f} 小时")
    print(f"平均每天欠: {debt/7:.2f} 小时")


def example_sleep_cycles():
    """睡眠周期分析示例"""
    print("\n" + "=" * 60)
    print("示例6: 睡眠周期分析")
    print("=" * 60)
    
    sleep_hours = [5, 6, 7, 7.5, 8, 9]
    
    print("\n不同睡眠时长的周期分析:")
    for hours in sleep_hours:
        analysis = analyze_sleep_cycles(hours)
        print(f"\n{hours} 小时睡眠:")
        print(f"  完整周期: {analysis['complete_cycles']} 个")
        print(f"  剩余时间: {analysis['remaining_minutes']:.1f} 分钟")
        print(f"  估算深睡眠: {analysis['estimated_deep_minutes']:.1f} 分钟")
        print(f"  估算REM: {analysis['estimated_rem_minutes']:.1f} 分钟")
        print(f"  周期质量: {analysis['cycle_quality']}")


def example_age_specific():
    """年龄相关睡眠建议示例"""
    print("\n" + "=" * 60)
    print("示例7: 不同年龄组的睡眠建议")
    print("=" * 60)
    
    print("\n各年龄组最佳睡眠时长:")
    for group, (min_h, max_h) in OPTIMAL_SLEEP_HOURS.items():
        print(f"  {group}: {min_h}-{max_h} 小时")
    
    print("\n不同年龄睡眠阶段估算 (8小时睡眠):")
    ages = [15, 25, 40, 55, 70]
    
    for age in ages:
        stages = estimate_sleep_stages(480, age)
        print(f"\n{age}岁:")
        print(f"  深睡眠: {stages[SleepStage.DEEP]} 分钟 ({stages[SleepStage.DEEP]/480*100:.1f}%)")
        print(f"  浅睡眠: {stages[SleepStage.LIGHT]} 分钟 ({stages[SleepStage.LIGHT]/480*100:.1f}%)")
        print(f"  REM: {stages[SleepStage.REM]} 分钟 ({stages[SleepStage.REM]/480*100:.1f}%)")


def example_nap_analysis():
    """小睡分析示例"""
    print("\n" + "=" * 60)
    print("示例8: 小睡分析")
    print("=" * 60)
    
    print("\n入睡潜伏期评估:")
    latencies = [10, 20, 35, 50, 70]
    for minutes in latencies:
        result = calculate_sleep_onset_latency(minutes / 60)
        print(f"  {minutes}分钟: {result}")
    
    print("\n小睡时长建议:")
    durations = [10, 20, 30, 45, 60, 90]
    for minutes in durations:
        result = get_nap_recommendation(minutes)
        print(f"  {minutes}分钟: {result}")
    
    print("\n理想小睡时长计算:")
    scenarios = [
        (8.0, 0, "睡眠充足"),
        (7.0, 1, "轻微不足"),
        (6.0, 3, "严重不足"),
    ]
    
    for hours, debt, desc in scenarios:
        duration, reason = calculate_ideal_nap_time(hours, debt)
        print(f"  {desc}: {duration}分钟 - {reason}")


def example_quality_scenarios():
    """不同睡眠质量场景示例"""
    print("\n" + "=" * 60)
    print("示例9: 不同睡眠质量场景")
    print("=" * 60)
    
    scenarios = [
        ("优质睡眠", SleepSession(
            start_time=datetime(2026, 4, 29, 22, 30),
            end_time=datetime(2026, 4, 30, 6, 30),
            awakenings=0,
            awakening_duration_minutes=0,
            sleep_stages={
                SleepStage.DEEP: 100,
                SleepStage.LIGHT: 280,
                SleepStage.REM: 120
            }
        )),
        ("一般睡眠", SleepSession(
            start_time=datetime(2026, 4, 29, 23, 0),
            end_time=datetime(2026, 4, 30, 6, 30),
            awakenings=1,
            awakening_duration_minutes=15,
            sleep_stages={
                SleepStage.DEEP: 60,
                SleepStage.LIGHT: 250,
                SleepStage.REM: 85
            }
        )),
        ("较差睡眠", SleepSession(
            start_time=datetime(2026, 4, 30, 0, 0),
            end_time=datetime(2026, 4, 30, 5, 0),
            awakenings=3,
            awakening_duration_minutes=30,
            sleep_stages={
                SleepStage.DEEP: 30,
                SleepStage.LIGHT: 200,
                SleepStage.REM: 40
            }
        )),
    ]
    
    for name, session in scenarios:
        score = calculate_sleep_quality_score(session, "adult")
        level = get_quality_level(score)
        
        print(f"\n{name}:")
        print(f"  时长: {format_sleep_duration(session.total_sleep_time)}")
        print(f"  效率: {session.sleep_efficiency:.1f}%")
        print(f"  质量分: {score:.1f}")
        print(f"  等级: {level.value}")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("Sleep Quality Utils 使用示例")
    print("=" * 60)
    
    example_basic_sleep_analysis()
    example_comprehensive_analysis()
    example_optimal_sleep_time()
    example_sleep_tracker()
    example_sleep_debt()
    example_sleep_cycles()
    example_age_specific()
    example_nap_analysis()
    example_quality_scenarios()
    
    print("\n" + "=" * 60)
    print("示例演示完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()