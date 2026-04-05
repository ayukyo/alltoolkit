"""
DateTime Utilities Example
时间日期工具模块使用示例

展示 datetime_utils 模块的各种功能用法
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'datetime_utils'))

from datetime import datetime, timedelta
from mod import DateTimeUtils, now, format_datetime, parse_datetime, days_between, is_leap_year, get_age, relative_time


def example_basic_operations():
    """示例：基本操作"""
    print("=" * 60)
    print("示例 1: 基本操作")
    print("=" * 60)

    current = DateTimeUtils.now()
    print(f"当前时间: {current}")

    utc = DateTimeUtils.now_utc()
    print(f"UTC 时间: {utc}")

    today = DateTimeUtils.today()
    print(f"今天日期: {today}")

    ts = DateTimeUtils.timestamp()
    ts_ms = DateTimeUtils.timestamp_ms()
    print(f"时间戳（秒）: {ts}")
    print(f"时间戳（毫秒）: {ts_ms}")
    print()


def example_formatting():
    """示例：格式化"""
    print("=" * 60)
    print("示例 2: 格式化")
    print("=" * 60)

    dt = DateTimeUtils.now()
    print(f"默认格式: {DateTimeUtils.format(dt)}")
    print(f"ISO 8601: {DateTimeUtils.format(dt, DateTimeUtils.FORMAT_ISO8601)}")
    print(f"日期格式: {DateTimeUtils.format(dt, DateTimeUtils.FORMAT_DATE)}")
    print(f"时间格式: {DateTimeUtils.format(dt, DateTimeUtils.FORMAT_TIME)}")
    print(f"中文格式: {DateTimeUtils.format(dt, DateTimeUtils.FORMAT_CHINESE)}")
    print(f"紧凑格式: {DateTimeUtils.format(dt, DateTimeUtils.FORMAT_COMPACT)}")
    print()


def example_parsing():
    """示例：解析"""
    print("=" * 60)
    print("示例 3: 解析")
    print("=" * 60)

    dt = DateTimeUtils.parse("2024-03-15 10:30:00")
    print(f"解析结果: {dt}")

    test_strings = [
        "2024-03-15",
        "2024/03/15 10:30:00",
        "15/03/2024",
        "2024-03-15T10:30:00",
        "10:30:00",
    ]

    for s in test_strings:
        result = DateTimeUtils.parse_auto(s)
        print(f"自动解析 '{s}': {result}")
    print()


def example_time_arithmetic():
    """示例：时间计算"""
    print("=" * 60)
    print("示例 4: 时间计算")
    print("=" * 60)

    dt = DateTimeUtils.now()
    print(f"当前时间: {DateTimeUtils.format(dt)}")
    print(f"+5 天: {DateTimeUtils.format(DateTimeUtils.add_days(dt, 5))}")
    print(f"+3 小时: {DateTimeUtils.format(DateTimeUtils.add_hours(dt, 3))}")
    print(f"+30 分钟: {DateTimeUtils.format(DateTimeUtils.add_minutes(dt, 30))}")
    print(f"+60 秒: {DateTimeUtils.format(DateTimeUtils.add_seconds(dt, 60))}")
    print(f"+2 个月: {DateTimeUtils.format(DateTimeUtils.add_months(dt, 2))}")
    print(f"+1 年: {DateTimeUtils.format(DateTimeUtils.add_years(dt, 1))}")
    print()


def example_time_difference():
    """示例：时间差计算"""
    print("=" * 60)
    print("示例 5: 时间差计算")
    print("=" * 60)

    start = DateTimeUtils.parse("2024-03-01 08:00:00")
    end = DateTimeUtils.parse("2024-03-05 18:30:00")
    print(f"开始时间: {DateTimeUtils.format(start)}")
    print(f"结束时间: {DateTimeUtils.format(end)}")
    print(f"天数差: {DateTimeUtils.days_between(start, end)} 天")
    print(f"小时差: {DateTimeUtils.hours_between(start, end):.2f} 小时")
    print(f"分钟差: {DateTimeUtils.minutes_between(start, end):.2f} 分钟")
    print(f"秒差: {DateTimeUtils.seconds_between(start, end):.0f} 秒")
    print()


def example_date_checks():
    """示例：日期判断"""
    print("=" * 60)
    print("示例 6: 日期判断")
    print("=" * 60)

    today = DateTimeUtils.today()
    yesterday = DateTimeUtils.add_days(today, -1)
    tomorrow = DateTimeUtils.add_days(today, 1)

    print(f"今天: {DateTimeUtils.format(today)}")
    print(f"  是今天? {DateTimeUtils.is_today(today)}")
    print(f"  是昨天? {DateTimeUtils.is_yesterday(today)}")
    print(f"  是明天? {DateTimeUtils.is_tomorrow(today)}")
    print(f"  是本周? {DateTimeUtils.is_this_week(today)}")
    print(f"  是本月? {DateTimeUtils.is_this_month(today)}")
    print(f"  是今年? {DateTimeUtils.is_this_year(today)}")

    print(f"\n昨天: {DateTimeUtils.format(yesterday)}")
    print(f"  是昨天? {DateTimeUtils.is_yesterday(yesterday)}")

    print(f"\n明天: {DateTimeUtils.format(tomorrow)}")
    print(f"  是明天? {DateTimeUtils.is_tomorrow(tomorrow)}")

    friday = DateTimeUtils.parse("2024-03-15", "%Y-%m-%d")
    saturday = DateTimeUtils.parse("2024-03-16", "%Y-%m-%d")
    print(f"\n{DateTimeUtils.format(friday)} 是周末? {DateTimeUtils.is_weekend(friday)}")
    print(f"{DateTimeUtils.format(saturday)} 是周末? {DateTimeUtils.is_weekend(saturday)}")
    print()


def example_leap_year():
    """示例：闰年判断"""
    print("=" * 60)
    print("示例 7: 闰年判断")
    print("=" * 60)

    years = [2020, 2024, 2023, 1900, 2000]
    for year in years:
        is_leap = DateTimeUtils.is_leap_year(year)
        days = DateTimeUtils.days_in_month(year, 2)
        print(f"{year}年: {'是' if is_leap else '不是'}闰年, 2月有{days}天")
    print()


def example_period_boundaries():
    """示例：周期边界"""
    print("=" * 60)
    print("示例 8: 周期边界")
    print("=" * 60)

    dt = DateTimeUtils.parse("2024-03-15 14:30:45")
    print(f"原始时间: {DateTimeUtils.format(dt)}")
    print(f"当天开始: {DateTimeUtils.format(DateTimeUtils.start_of_day(dt))}")
    print(f"当天结束: {DateTimeUtils.format(DateTimeUtils.end_of_day(dt))}")
    print(f"当周开始（周一）: {DateTimeUtils.format(DateTimeUtils.start_of_week(dt))}")
    print(f"当周结束（周日）: {DateTimeUtils.format(DateTimeUtils.end_of_week(dt))}")
    print(f"当月开始: {DateTimeUtils.format(DateTimeUtils.start_of_month(dt))}")
    print(f"当月结束: {DateTimeUtils.format(DateTimeUtils.end_of_month(dt))}")
    print(f"当年开始: {DateTimeUtils.format(DateTimeUtils.start_of_year(dt))}")
    print(f"当年结束: {DateTimeUtils.format(DateTimeUtils.end_of_year(dt))}")
    print()


def example_age_calculation():
    """示例：年龄计算"""
    print("=" * 60)
    print("示例 9: 年龄计算")
    print("=" * 60)

    today = DateTimeUtils.parse("2024-03-15", "%Y-%m-%d")
    birth_dates = [
        datetime(2000, 3, 14),
        datetime(2000, 3, 16),
        datetime(2000, 3, 15),
        datetime(1990, 6, 1),
    ]

    for birth in birth_dates:
        age = DateTimeUtils.get_age(birth, today)
        print(f"出生日期: {DateTimeUtils.format(birth, '%Y-%m-%d')}, 年龄: {age}岁")
    print()


def example_names():
    """示例：星期和月份名称"""
    print("=" * 60)
    print("示例 10: 星期和月份名称")
    print("=" * 60)

    dt = DateTimeUtils.parse("2024-03-15", "%Y-%m-%d")
    print(f"日期: {DateTimeUtils.format(dt, '%Y-%m-%d')}")
    print(f"星期（英文）: {DateTimeUtils.get_weekday_name(dt, 'en')}")
    print(f"星期（中文）: {DateTimeUtils.get_weekday_name(dt, 'cn')}")
    print(f"星期（缩写）: {DateTimeUtils.get_weekday_name(dt, 'short')}")
    print(f"月份（英文）: {DateTimeUtils.get_month_name(3, 'en')}")
    print(f"月份（中文）: {DateTimeUtils.get_month_name(3, 'cn')}")
    print(f"月份（缩写）: {DateTimeUtils.get_month_name(3, 'short')}")
    print()


def example_relative_time():
    """示例：相对时间"""
    print("=" * 60)
    print("示例 11: 相对时间")
    print("=" * 60)

    now = DateTimeUtils.now()
    test_times = [
        (now - timedelta(seconds=30), "30秒前"),
        (now - timedelta(minutes=5), "5分钟前"),
        (now - timedelta(hours=2), "2小时前"),
        (now - timedelta(days=1), "昨天"),
        (now - timedelta(days=3), "3天前"),
        (now - timedelta(days=10), "10天前"),
    ]

    for dt, desc in test_times:
        relative = DateTimeUtils.relative_time(dt, now)
        print(f"{desc}: {relative}")
    print()


def example_duration_formatting():
    """示例：时长格式化"""
    print("=" * 60)
    print("示例 12: 时长格式化")
    print("=" * 60)

    durations = [45, 300, 365, 7200, 7500, 172800, 176400]
    for d in durations:
        formatted = DateTimeUtils.format_duration(d)
        print(f"{d}秒 = {formatted}")
    print()


def example_countdown():
    """示例：倒计时"""
    print("=" * 60)
    print("示例 13: 倒计时")
    print("=" * 60)

    now = DateTimeUtils.now()
    target = now + timedelta(days=2, hours=5, minutes=30, seconds=15)
    print(f"当前时间: {DateTimeUtils.format(now)}")
    print(f"目标时间: {DateTimeUtils.format(target)}")

    countdown = DateTimeUtils.countdown(target, now)
    print(f"倒计时: {countdown['days']}天 {countdown['hours']}小时 {countdown['minutes']}分 {countdown['seconds']}秒")
    print(f"总秒数: {countdown['total_seconds']}")
    print()


def example_date_range():
    """示例：日期范围生成"""
    print("=" * 60)
    print("示例 14: 日期范围生成")
    print("=" * 60)

    start = DateTimeUtils.parse("2024-03-01", "%Y-%m-%d")
    end = DateTimeUtils.parse("2024-03-07", "%Y-%m-%d")
    dates = DateTimeUtils.generate_date_range(start, end)

    print(f"从 {DateTimeUtils.format(start, '%Y-%m-%d')} 到 {DateTimeUtils.format(end, '%Y-%m-%d')}:")
    for d in dates:
        print(f"  {DateTimeUtils.format(d, '%Y-%m-%d')} ({DateTimeUtils.get_weekday_name(d, 'cn')})")
    print()


def example_iso8601():
    """示例：ISO 8601 格式"""
    print("=" * 60)
    print("示例 15: ISO 8601 格式")
    print("=" * 60)

    dt = DateTimeUtils.now()
    iso = DateTimeUtils.to_iso8601(dt)
    print(f"ISO 8601 格式: {iso}")

    parsed = DateTimeUtils.from_iso8601(iso)
    print(f"解析结果: {parsed}")
    print()


def example_convenience_functions():
    """示例：便捷函数"""
    print("=" * 60)
    print("示例 16: 便捷函数")
    print("=" * 60)

    # now
    print(f"now(): {now()}")

    # format_datetime
    dt = datetime(2024, 3, 15, 10, 30, 0)
    print(f"format_datetime(): {format_datetime(dt)}")

    # parse_datetime
    parsed = parse_datetime("2024-03-15 10:30:00")
    print(f"parse_datetime(): {parsed}")

    # days_between
    start = datetime(2024, 3, 1)
    end = datetime(2024, 3, 10)
    print(f"days_between(): {days_between(start, end)} 天")

    # is_leap_year
    print(f"is_leap_year(2024): {is_leap_year(2024)}")
    print(f"is_leap_year(2023): {is_leap_year(2023)}")

    # get_age
    birth = datetime(2000, 1, 1)
    print(f"get_age(2000-01-01): {get_age(birth)} 岁")

    # relative_time
    dt = datetime.now() - timedelta(hours=3)
    print(f"relative_time(3小时前): {relative_time(dt)}")
    print()


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("DateTime Utilities 使用示例")
    print("=" * 60 + "\n")

    example_basic_operations()
    example_formatting()
    example_parsing()
    example_time_arithmetic()
    example_time_difference()
    example_date_checks()
    example_leap_year()
    example_period_boundaries()
    example_age_calculation()
    example_names()
    example_relative_time()
    example_duration_formatting()
    example_countdown()
    example_date_range()
    example_iso8601()
    example_convenience_functions()

    print("=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()
