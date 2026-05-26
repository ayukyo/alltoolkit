"""
AllToolkit - Nth Weekday Utilities 使用示例

本文件展示 nth_weekday_utils 模块的各种使用场景。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from nth_weekday_utils.mod import (
    NthWeekdayUtils, Weekday,
    nth_weekday, last_weekday, first_weekday,
    all_weekdays_in_month, count_weekdays_in_month,
    which_nth_weekday, holiday, list_holidays,
    weekdays_between, count_weekdays_between,
    next_weekday_after, previous_weekday_before,
    weekday_name, month_name
)
from datetime import date


def example_nth_weekday():
    """示例 1: 基本第 N 个星期几查找"""
    print("=" * 60)
    print("示例 1: 第 N 个星期几查找")
    print("=" * 60)
    
    # 感恩节：11 月第 4 个星期四
    thanksgiving = nth_weekday(2024, 11, 4, Weekday.THURSDAY)
    print(f"感恩节 2024: {thanksgiving} ({weekday_name(Weekday.THURSDAY, 'zh')})")
    
    # 劳动节：9 月第 1 个星期一
    labor_day = nth_weekday(2024, 9, 1, Weekday.MONDAY)
    print(f"劳动节 2024: {labor_day} ({weekday_name(Weekday.MONDAY, 'zh')})")
    
    # 阵亡将士纪念日：5 月最后一个星期一
    memorial_day = nth_weekday(2024, 5, -1, Weekday.MONDAY)
    print(f"阵亡将士纪念日 2024: {memorial_day} ({weekday_name(Weekday.MONDAY, 'zh')})")
    
    # 母亲节：5 月第 2 个星期日
    mothers_day = nth_weekday(2024, 5, 2, Weekday.SUNDAY)
    print(f"母亲节 2024: {mothers_day} ({weekday_name(Weekday.SUNDAY, 'zh')})")
    
    print()


def example_first_last():
    """示例 2: 第一个/最后一个星期几"""
    print("=" * 60)
    print("示例 2: 第一个/最后一个星期几")
    print("=" * 60)
    
    # 2024 年 11 月第一个星期四
    first_thursday = first_weekday(2024, 11, Weekday.THURSDAY)
    print(f"2024年11月第一个星期四: {first_thursday}")
    
    # 2024 年 5 月最后一个星期一
    last_monday = last_weekday(2024, 5, Weekday.MONDAY)
    print(f"2024年5月最后一个星期一: {last_monday}")
    
    # 2024 年 12 月最后一个星期日
    last_sunday = last_weekday(2024, 12, Weekday.SUNDAY)
    print(f"2024年12月最后一个星期日: {last_sunday}")
    
    print()


def example_all_weekdays():
    """示例 3: 获取月份内所有星期几"""
    print("=" * 60)
    print("示例 3: 月份内所有星期几")
    print("=" * 60)
    
    # 2024 年 11 月所有星期四
    thursdays = all_weekdays_in_month(2024, 11, Weekday.THURSDAY)
    print(f"2024年11月所有星期四 ({len(thursdays)} 个):")
    for d in thursdays:
        print(f"  - {d}")
    
    # 2024 年 1 月所有星期一
    mondays = all_weekdays_in_month(2024, 1, Weekday.MONDAY)
    print(f"\n2024年1月所有星期一 ({len(mondays)} 个):")
    for d in mondays:
        print(f"  - {d}")
    
    # 计算出现次数
    count = count_weekdays_in_month(2024, 11, Weekday.THURSDAY)
    print(f"\n2024年11月星期四出现次数: {count}")
    
    print()


def example_which_nth():
    """示例 4: 判断日期是第几个星期几"""
    print("=" * 60)
    print("示例 4: 判断日期是第几个星期几")
    print("=" * 60)
    
    # 感恩节是第几个星期四？
    year, month, nth = which_nth_weekday(date(2024, 11, 28))
    print(f"2024-11-28 是 {month_name(month, 'zh')}的第 {nth} 个星期{weekday_name(date(2024, 11, 28).weekday(), 'zh')}")
    
    # 劳动节
    year, month, nth = which_nth_weekday('2024-09-02')
    print(f"2024-09-02 是 {month_name(month, 'zh')}的第 {nth} 个星期{weekday_name(date(2024, 9, 2).weekday(), 'zh')}")
    
    print()


def example_holidays():
    """示例 5: 节假日计算"""
    print("=" * 60)
    print("示例 5: 节节假日计算")
    print("=" * 60)
    
    # 单个节假日
    holidays_to_check = ['thanksgiving', 'labor_day', 'memorial_day', 
                         'mothers_day', 'fathers_day', 'presidents_day']
    
    print("2024 年美国节假日:")
    for h in holidays_to_check:
        d = holiday(h, 2024)
        name = h.replace('_', ' ').title()
        print(f"  {name}: {d}")
    
    print("\n2024 年英国节假日:")
    uk_holidays = list_holidays(2024, 'uk')
    for name, d in uk_holidays:
        print(f"  {name}: {d}")
    
    print("\n2025 年感恩节:")
    print(f"  Thanksgiving: {holiday('thanksgiving', 2025)}")
    
    print()


def example_weekdays_between():
    """示例 6: 日期范围内的星期几"""
    print("=" * 60)
    print("示例 6: 日期范围内的星期几")
    print("=" * 60)
    
    # 2024 年 1 月所有星期五
    fridays = weekdays_between('2024-01-01', '2024-01-31', Weekday.FRIDAY)
    print(f"2024年1月所有星期五 ({len(fridays)} 个):")
    for d in fridays:
        print(f"  - {d}")
    
    # 跨月份
    mondays = weekdays_between('2024-11-25', '2024-12-15', Weekday.MONDAY)
    print(f"\n2024-11-25 到 2024-12-15 之间的星期一 ({len(mondays)} 个):")
    for d in mondays:
        print(f"  - {d}")
    
    # 计数
    count = count_weekdays_between('2024-01-01', '2024-12-31', Weekday.MONDAY)
    print(f"\n2024年全年星期一数量: {count}")
    
    print()


def example_next_previous():
    """示例 7: 前后星期几查找"""
    print("=" * 60)
    print("示例 7: 前后星期几查找")
    print("=" * 60)
    
    # 从 2024-11-27（星期三）找下一个星期一
    next_mon = next_weekday_after('2024-11-27', Weekday.MONDAY)
    print(f"2024-11-27 之后的第一个星期一: {next_mon}")
    
    # 包含当天
    next_mon_incl = next_weekday_after('2024-12-02', Weekday.MONDAY, inclusive=True)
    print(f"2024-12-02 之后的第一个星期一（含当天）: {next_mon_incl}")
    
    # 不包含当天
    next_mon_excl = next_weekday_after('2024-12-02', Weekday.MONDAY, inclusive=False)
    print(f"2024-12-02 之后的第一个星期一（不含当天）: {next_mon_excl}")
    
    # 之前的星期一
    prev_mon = previous_weekday_before('2024-11-27', Weekday.MONDAY)
    print(f"\n2024-11-27 之前的最后一个星期一: {prev_mon}")
    
    print()


def example_multilingual():
    """示例 8: 多语言支持"""
    print("=" * 60)
    print("示例 8: 多语言星期/月份名称")
    print("=" * 60)
    
    languages = ['en', 'zh', 'es', 'fr', 'de', 'ja']
    
    print("星期名称:")
    print("语言 | 星期一 | 星期四 | 星期日")
    print("-" * 40)
    for lang in languages:
        mon = weekday_name(Weekday.MONDAY, lang)
        thu = weekday_name(Weekday.THURSDAY, lang)
        sun = weekday_name(Weekday.SUNDAY, lang)
        print(f"{lang:4} | {mon:8} | {thu:10} | {sun}")
    
    print("\n月份名称:")
    print("语言 | 一月 | 六月 | 十一月")
    print("-" * 40)
    for lang in languages:
        jan = month_name(1, lang)
        jun = month_name(6, lang)
        nov = month_name(11, lang)
        print(f"{lang:4} | {jan:10} | {jun:6} | {nov}")
    
    print()


def example_scheduling():
    """示例 9: 实际调度场景"""
    print("=" * 60)
    print("示例 9: 实际调度场景")
    print("=" * 60)
    
    # 场景 1: 定期会议安排
    print("场景 1: 每月第二个星期二开会")
    for month in range(1, 13):
        meeting_date = nth_weekday(2024, month, 2, Weekday.TUESDAY)
        print(f"  {month_name(month, 'zh')}: {meeting_date}")
    
    # 场景 2: 季度报告（每季度最后星期五）
    print("\n场景 2: 季度末最后一个星期五提交报告")
    quarters = [(3, '第一季度'), (6, '第二季度'), (9, '第三季度'), (12, '第四季度')]
    for month, name in quarters:
        deadline = last_weekday(2024, month, Weekday.FRIDAY)
        print(f"  {name}: {deadline}")
    
    # 场景 3: 发薪日（每月15日，如果是周末则调整）
    print("\n场景 3: 发薪日（遇周末则延后到周一）")
    for month in range(1, 13):
        payday = date(2024, month, 15)
        if payday.weekday() == Weekday.SATURDAY:
            payday = next_weekday_after(payday, Weekday.MONDAY)
        elif payday.weekday() == Weekday.SUNDAY:
            payday = next_weekday_after(payday, Weekday.MONDAY)
        print(f"  {month_name(month, 'zh')}: {payday}")
    
    print()


def main():
    """运行所有示例"""
    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 12 + "AllToolkit Nth Weekday Utilities 示例" + " " * 10 + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    example_nth_weekday()
    example_first_last()
    example_all_weekdays()
    example_which_nth()
    example_holidays()
    example_weekdays_between()
    example_next_previous()
    example_multilingual()
    example_scheduling()
    
    print("=" * 60)
    print("所有示例完成!")
    print("=" * 60)
    print()


if __name__ == '__main__':
    main()