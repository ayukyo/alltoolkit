"""
周期性模式工具使用示例

展示如何使用 recurring_pattern_utils 处理各种周期性模式
"""

from datetime import datetime, date, timedelta
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from recurring_pattern_utils.mod import (
    parse_natural_language, parse_cron,
    get_next_occurrence, get_previous_occurrence,
    get_occurrences_in_range, validate_pattern,
    pattern_to_description, get_nth_weekday_of_month,
    calculate_next_n_occurrences, humanize_timedelta,
    parse, next_occurrence, is_match
)


def demo_natural_language_parsing():
    """演示自然语言解析"""
    print("=" * 60)
    print("自然语言解析示例")
    print("=" * 60)
    
    patterns = [
        "每天",
        "每天上午9点",
        "每天下午3点30分",
        "每周一",
        "每周一三五",
        "工作日",
        "周末",
        "每月1号",
        "每月15号",
        "每月第二个周二",
        "每月最后一个周五",
        "每3天",
        "every 2 weeks",
    ]
    
    for p in patterns:
        try:
            parsed = parse_natural_language(p)
            desc = pattern_to_description(parsed)
            print(f"  {p:30s} -> {desc}")
        except ValueError as e:
            print(f"  {p:30s} -> 错误: {e}")
    
    print()


def demo_cron_parsing():
    """演示 cron 表达式解析"""
    print("=" * 60)
    print("Cron 表达式解析示例")
    print("=" * 60)
    
    cron_expressions = [
        "0 9 * * *",       # 每天 9:00
        "30 14 * * 1-5",   # 工作日 14:30
        "0 0 1 * *",       # 每月 1 号 00:00
        "0 12 * * 1,3,5",  # 每周一三五 12:00
        "*/15 * * * *",    # 每 15 分钟
        "0 9 1 1 *",       # 每年 1 月 1 日 9:00
    ]
    
    for cron in cron_expressions:
        try:
            parsed = parse_cron(cron)
            desc = pattern_to_description(parsed)
            print(f"  {cron:20s} -> {desc}")
        except ValueError as e:
            print(f"  {cron:20s} -> 错误: {e}")
    
    print()


def demo_next_occurrence():
    """演示下一个触发时间计算"""
    print("=" * 60)
    print("下一个触发时间示例")
    print("=" * 60)
    
    # 当前时间
    now = datetime(2024, 1, 15, 10, 30)  # 周一 10:30
    print(f"当前时间: {now.strftime('%Y-%m-%d %H:%M')} (周一)")
    print()
    
    patterns = [
        ("每天", "每天"),
        ("每天14:00", "每天 14:00"),
        ("每周一", "每周一"),
        ("每周五", "每周五"),
        ("每月15号", "每月 15 号"),
        ("每月第二个周二", "每月第二个周二"),
    ]
    
    for pattern_str, desc in patterns:
        pattern = parse(pattern_str)
        next_time = get_next_occurrence(pattern, now)
        if next_time:
            humanized = humanize_timedelta(next_time, now)
            weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
            weekday = weekday_names[next_time.weekday()]
            print(f"  {desc:15s} -> {next_time.strftime('%Y-%m-%d %H:%M')} ({weekday}) [{humanized}]")
        else:
            print(f"  {desc:15s} -> 无下一个触发时间")
    
    print()


def demo_previous_occurrence():
    """演示上一个触发时间计算"""
    print("=" * 60)
    print("上一个触发时间示例")
    print("=" * 60)
    
    now = datetime(2024, 1, 15, 10, 30)  # 周一 10:30
    print(f"当前时间: {now.strftime('%Y-%m-%d %H:%M')} (周一)")
    print()
    
    patterns = [
        ("每天", "每天"),
        ("每天9:00", "每天 9:00"),
        ("每周一", "每周一"),
        ("每月15号", "每月 15 号"),
    ]
    
    for pattern_str, desc in patterns:
        pattern = parse(pattern_str)
        prev_time = get_previous_occurrence(pattern, now)
        if prev_time:
            weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
            weekday = weekday_names[prev_time.weekday()]
            print(f"  {desc:15s} -> {prev_time.strftime('%Y-%m-%d %H:%M')} ({weekday})")
        else:
            print(f"  {desc:15s} -> 无上一个触发时间")
    
    print()


def demo_occurrences_in_range():
    """演示时间范围内的触发时间"""
    print("=" * 60)
    print("时间范围内触发时间示例")
    print("=" * 60)
    
    start = datetime(2024, 1, 1, 0, 0)
    end = datetime(2024, 1, 31, 23, 59)
    
    print(f"时间范围: {start.strftime('%Y-%m-%d')} 到 {end.strftime('%Y-%m-%d')}")
    print()
    
    # 每周一
    pattern = parse("每周一")
    occurrences = get_occurrences_in_range(pattern, start, end)
    print(f"  每周一: 共 {len(occurrences)} 次")
    for occ in occurrences[:5]:  # 只显示前5个
        print(f"    - {occ.strftime('%Y-%m-%d')}")
    if len(occurrences) > 5:
        print(f"    ... 还有 {len(occurrences) - 5} 次")
    
    print()
    
    # 每月15号
    pattern = parse("每月15号")
    occurrences = get_occurrences_in_range(pattern, start, end)
    print(f"  每月15号: 共 {len(occurrences)} 次")
    for occ in occurrences:
        print(f"    - {occ.strftime('%Y-%m-%d %H:%M')}")
    
    print()


def demo_nth_weekday():
    """演示每月第 n 个周几"""
    print("=" * 60)
    print("每月第 N 个周几示例")
    print("=" * 60)
    
    year, month = 2024, 1
    print(f"2024年1月:")
    print()
    
    examples = [
        (1, "第一个周一", 0),   # Monday = 0
        (2, "第二个周二", 1),   # Tuesday = 1
        (3, "第三个周三", 2),   # Wednesday = 2
        (-1, "最后一个周五", 4), # Friday = 4
        (-1, "最后一个周日", 6), # Sunday = 6
    ]
    
    weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    
    from recurring_pattern_utils.mod import Weekday
    weekday_enum = [Weekday.MONDAY, Weekday.TUESDAY, Weekday.WEDNESDAY,
                   Weekday.THURSDAY, Weekday.FRIDAY, Weekday.SATURDAY, Weekday.SUNDAY]
    
    for n, desc, wd_idx in examples:
        result = get_nth_weekday_of_month(year, month, n, weekday_enum[wd_idx])
        if result:
            print(f"  {desc}: {result.strftime('%Y-%m-%d')}")
        else:
            print(f"  {desc}: 不存在")
    
    print()


def demo_validation():
    """演示模式验证"""
    print("=" * 60)
    print("模式验证示例")
    print("=" * 60)
    
    patterns = [
        "每天",
        "每周一三五",
        "每月15号",
        "0 9 * * *",
        "无效模式",
        "xyz",
    ]
    
    for p in patterns:
        valid, error = validate_pattern(p)
        status = "✓ 有效" if valid else f"✗ 无效: {error}"
        print(f"  {p:20s} -> {status}")
    
    print()


def demo_convenience_functions():
    """演示便捷函数"""
    print("=" * 60)
    print("便捷函数示例")
    print("=" * 60)
    
    now = datetime(2024, 1, 15, 10, 30)
    print(f"当前时间: {now.strftime('%Y-%m-%d %H:%M')}")
    print()
    
    # next_occurrence
    next_time = next_occurrence("每周一", now)
    print(f"  下一个周一: {next_time.strftime('%Y-%m-%d %H:%M')}")
    
    # is_match
    check_time = datetime(2024, 1, 15, 9, 0)
    print(f"  {check_time.strftime('%Y-%m-%d %H:%M')} 匹配 '每天9:00': {is_match('每天9:00', check_time)}")
    print(f"  {check_time.strftime('%Y-%m-%d %H:%M')} 匹配 '每周一': {is_match('每周一', check_time)}")
    
    print()


def demo_real_world_scenarios():
    """演示实际应用场景"""
    print("=" * 60)
    print("实际应用场景示例")
    print("=" * 60)
    
    # 场景1: 会议提醒
    print("\n场景1: 会议提醒")
    print("-" * 40)
    meeting_pattern = parse("每周一三五 14:00" if " " in "每周一三五" else "每周一三五")
    meeting_pattern.hour = 14
    meeting_pattern.minute = 0
    
    now = datetime.now()
    next_meeting = get_next_occurrence(meeting_pattern, now)
    if next_meeting:
        humanized = humanize_timedelta(next_meeting, now)
        print(f"  下次会议: {next_meeting.strftime('%Y-%m-%d %H:%M')} ({humanized})")
    
    # 场景2: 账单提醒
    print("\n场景2: 账单提醒")
    print("-" * 40)
    bill_pattern = parse("每月1号")
    next_bill = get_next_occurrence(bill_pattern, now)
    if next_bill:
        humanized = humanize_timedelta(next_bill, now)
        print(f"  下次账单日: {next_bill.strftime('%Y-%m-%d')} ({humanized})")
    
    # 场景3: 计算接下来5次触发
    print("\n场景3: 接下来5次触发")
    print("-" * 40)
    pattern = parse("每周一")
    occurrences = calculate_next_n_occurrences(pattern, now, 5)
    weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    for occ in occurrences:
        print(f"  {occ.strftime('%Y-%m-%d')} ({weekday_names[occ.weekday()]})")
    
    # 场景4: 工作日调度
    print("\n场景4: 工作日调度")
    print("-" * 40)
    workday_pattern = parse("工作日 9:00" if " " in "工作日" else "工作日")
    workday_pattern.hour = 9
    next_workday = get_next_occurrence(workday_pattern, now)
    if next_workday:
        print(f"  下一个工作日 9:00: {next_workday.strftime('%Y-%m-%d %H:%M')}")
    
    print()


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("周期性模式工具 (Recurring Pattern Utils) 使用示例")
    print("=" * 60 + "\n")
    
    demo_natural_language_parsing()
    demo_cron_parsing()
    demo_next_occurrence()
    demo_previous_occurrence()
    demo_occurrences_in_range()
    demo_nth_weekday()
    demo_validation()
    demo_convenience_functions()
    demo_real_world_scenarios()
    
    print("\n" + "=" * 60)
    print("示例演示完成!")
    print("=" * 60 + "\n")