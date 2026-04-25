#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Biorhythm Utilities Examples
==========================================
Practical examples demonstrating the biorhythm_utils module usage.

Examples:
    1. Basic daily biorhythm calculation
    2. Finding critical and peak days
    3. ASCII chart generation
    4. Compatibility analysis
    5. Best day planning
    6. Full profile generation
"""

from datetime import date, timedelta
import sys
import os

# Add module directory to path for imports
module_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, module_dir)

from mod import (
    CycleType,
    calculate_biorhythms,
    find_critical_days,
    find_peak_days,
    generate_ascii_chart,
    calculate_compatibility,
    get_best_days,
    get_daily_summary,
    get_full_profile,
    get_chinese_zodiac,
)


def example_1_basic_daily():
    """Example 1: Basic daily biorhythm calculation."""
    print("=" * 60)
    print("Example 1: 基础每日生物节律计算")
    print("=" * 60)
    
    birth_date = date(1990, 6, 15)
    
    # Calculate for today
    result = calculate_biorhythms(birth_date)
    
    print(f"\n生日: {birth_date}")
    print(f"今天: {result.target_date}")
    print(f"已生活: {result.days_alive} 天 ({result.days_alive / 365.25:.1f} 岁)")
    print()
    
    print("主要周期状态:")
    for cycle_type, value in result.primary_cycles.items():
        print(f"  {cycle_type.value}: {value.value:+.1f}% ({value.state})")
    
    print(f"\n综合能量: {result.overall_energy:+.1f}%")
    print()
    print(result.get_summary())


def example_2_critical_peak_days():
    """Example 2: Finding critical and peak days."""
    print("\n" + "=" * 60)
    print("Example 2: 查找临界日和高峰日")
    print("=" * 60)
    
    birth_date = date(1990, 6, 15)
    start_date = date.today()
    
    # Find critical days in next 60 days
    critical_days = find_critical_days(birth_date, start_date, days=60)
    
    print(f"\n未来60天的临界日 (节律零点):")
    if critical_days:
        for cd in critical_days[:10]:
            cycle_name = {
                CycleType.PHYSICAL: "体力",
                CycleType.EMOTIONAL: "情绪",
                CycleType.INTELLECTUAL: "智力",
            }.get(cd.cycle_type, cd.cycle_type.value)
            print(f"  {cd.date.strftime('%Y-%m-%d')} - {cycle_name} ({cd.direction}穿越)")
    else:
        print("  无临界日")
    
    # Find peak days
    peak_days = find_peak_days(birth_date, start_date, days=60)
    
    print(f"\n未来60天的高峰/低谷日:")
    if peak_days:
        for pd in peak_days[:10]:
            cycle_name = {
                CycleType.PHYSICAL: "体力",
                CycleType.EMOTIONAL: "情绪",
                CycleType.INTELLECTUAL: "智力",
            }.get(pd.cycle_type, pd.cycle_type.value)
            status = "高峰" if pd.is_peak else "低谷"
            print(f"  {pd.date.strftime('%Y-%m-%d')} - {cycle_name} {status}")


def example_3_ascii_chart():
    """Example 3: ASCII chart generation."""
    print("\n" + "=" * 60)
    print("Example 3: ASCII图表生成")
    print("=" * 60)
    
    birth_date = date(1990, 6, 15)
    start_date = date.today()
    
    chart = generate_ascii_chart(
        birth_date,
        start_date,
        days=30,
        width=50,
        height=11
    )
    
    print(chart)


def example_4_compatibility():
    """Example 4: Compatibility analysis."""
    print("\n" + "=" * 60)
    print("Example 4: 配对契合度分析")
    print("=" * 60)
    
    birth1 = date(1990, 6, 15)  # Person A
    birth2 = date(1992, 3, 20)  # Person B
    
    compat = calculate_compatibility(birth1, birth2)
    
    print(f"\nA生日: {birth1}")
    print(f"B生日: {birth2}")
    print(f"分析日期: {compat['date']}")
    print()
    
    print("契合度评分:")
    print(f"  体力契合: {compat['physical']}%")
    print(f"  情绪契合: {compat['emotional']}%")
    print(f"  智力契合: {compat['intellectual']}%")
    print(f"  综合契合: {compat['overall']}%")
    print()
    print(f"解读: {compat['interpretation']}")


def example_5_best_day_planning():
    """Example 5: Planning best days for activities."""
    print("\n" + "=" * 60)
    print("Example 5: 最佳日期规划")
    print("=" * 60)
    
    birth_date = date(1990, 6, 15)
    start_date = date.today()
    
    print("\n根据不同节律规划最佳日期:")
    print()
    
    # Best days for physical activities (sports, exercise)
    print("体力最佳 (适合运动、体力活动):")
    best_physical = get_best_days(birth_date, start_date, days=30, 
                                  cycle_type=CycleType.PHYSICAL, top_n=3)
    for d, v in best_physical:
        print(f"  {d.strftime('%Y-%m-%d (%A)')}: {v:+.1f}%")
    
    # Best days for emotional activities (creative work, social)
    print("\n情绪最佳 (适合创作、社交活动):")
    best_emotional = get_best_days(birth_date, start_date, days=30,
                                   cycle_type=CycleType.EMOTIONAL, top_n=3)
    for d, v in best_emotional:
        print(f"  {d.strftime('%Y-%m-%d (%A)')}: {v:+.1f}%")
    
    # Best days for intellectual activities (study, analysis)
    print("\n智力最佳 (适合学习、思考、分析):")
    best_intellectual = get_best_days(birth_date, start_date, days=30,
                                      cycle_type=CycleType.INTELLECTUAL, top_n=3)
    for d, v in best_intellectual:
        print(f"  {d.strftime('%Y-%m-%d (%A)')}: {v:+.1f}%")


def example_6_full_profile():
    """Example 6: Complete profile generation."""
    print("\n" + "=" * 60)
    print("Example 6: 完整个人档案")
    print("=" * 60)
    
    birth_date = date(1990, 6, 15)
    
    profile = get_full_profile(birth_date)
    
    print(f"\n基本信息:")
    print(f"  生日: {profile['birth_date']}")
    print(f"  年龄: {profile['age_years']} 岁")
    print(f"  天数: {profile['days_alive']} 天")
    
    print(f"\n生肖信息:")
    zodiac = profile['zodiac']
    print(f"  动物: {zodiac['animal_cn']} ({zodiac['animal_en']})")
    print(f"  地支: {zodiac['earthly_branch']}")
    print(f"  五行: {zodiac['element']}")
    print(f"  描述: {zodiac['description']}")
    
    print(f"\n当前节律状态:")
    for cycle, data in profile['primary_cycles'].items():
        print(f"  {cycle}: {data['value']:+.1f}% ({data['state']})")
        if data['is_critical']:
            print(f"    ⚠️ 临界日!")
    
    print(f"\n综合能量: {profile['overall_energy']:+.1f}%")
    
    print(f"\n近期临界日:")
    for cd in profile['upcoming_critical_days'][:3]:
        print(f"  {cd['date']} - {cd['cycle']} ({cd['direction']})")


def example_7_chinese_zodiac():
    """Example 7: Chinese zodiac lookup."""
    print("\n" + "=" * 60)
    print("Example 7: 中国生肖查询")
    print("=" * 60)
    
    test_years = [
        date(1980, 1, 1),
        date(1990, 1, 1),
        date(2000, 1, 1),
        date(2012, 1, 1),
        date(2020, 1, 1),
    ]
    
    print("\n各年份生肖:")
    for birth in test_years:
        zodiac = get_chinese_zodiac(birth)
        print(f"  {birth.year}: {zodiac['description']} "
              f"(地支: {zodiac['earthly_branch']})")


def example_8_daily_summary():
    """Example 8: Daily summary generation."""
    print("\n" + "=" * 60)
    print("Example 8: 每日节律摘要")
    print("=" * 60)
    
    birth_date = date(1990, 6, 15)
    
    summary = get_daily_summary(birth_date)
    
    print(summary)


def example_9_specific_date():
    """Example 9: Analyzing a specific date."""
    print("\n" + "=" * 60)
    print("Example 9: 分析特定日期")
    print("=" * 60)
    
    birth_date = date(1990, 6, 15)
    # Analyze a future date
    specific_date = date.today() + timedelta(days=15)
    
    result = calculate_biorhythms(birth_date, specific_date, include_secondary=True)
    
    print(f"\n生日: {birth_date}")
    print(f"目标日期: {specific_date}")
    print(f"距离天数: {(specific_date - birth_date).days} 天")
    print()
    
    print("主要周期:")
    for cycle_type, value in result.primary_cycles.items():
        status = "📈" if value.value > 50 else ("📉" if value.value < -50 else "➡️")
        if value.is_critical:
            status = "⚠️ "
        print(f"  {cycle_type.value}: {value.value:+.1f}% {status}")
    
    print("\n次要周期:")
    for cycle_type, value in result.secondary_cycles.items():
        status = "📈" if value.value > 50 else ("📉" if value.value < -50 else "➡️")
        print(f"  {cycle_type.value}: {value.value:+.1f}% {status}")


def example_10_multiple_people():
    """Example 10: Comparing multiple people."""
    print("\n" + "=" * 60)
    print("Example 10: 多人节律对比")
    print("=" * 60)
    
    birth_dates = [
        ("张三", date(1990, 6, 15)),
        ("李四", date(1992, 3, 20)),
        ("王五", date(1988, 12, 1)),
    ]
    
    print(f"\n{date.today()} 当日节律对比:")
    print()
    
    for name, birth in birth_dates:
        result = calculate_biorhythms(birth)
        phys = result.primary_cycles[CycleType.PHYSICAL].value
        emo = result.primary_cycles[CycleType.EMOTIONAL].value
        intel = result.primary_cycles[CycleType.INTELLECTUAL].value
        
        print(f"{name} (生日: {birth}):")
        print(f"  体力: {phys:+.1f}%, 情绪: {emo:+.1f}%, 智力: {intel:+.1f}%")
        print(f"  综合: {result.overall_energy:+.1f}%")
        print()


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("AllToolkit - 生物节律工具示例")
    print("=" * 60)
    
    example_1_basic_daily()
    example_2_critical_peak_days()
    example_3_ascii_chart()
    example_4_compatibility()
    example_5_best_day_planning()
    example_6_full_profile()
    example_7_chinese_zodiac()
    example_8_daily_summary()
    example_9_specific_date()
    example_10_multiple_people()
    
    print("\n" + "=" * 60)
    print("示例完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()