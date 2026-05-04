"""
Persian Calendar Utilities - 使用示例

演示波斯历工具包的各种用法。
"""

import sys
import os
from datetime import date, datetime

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from persian_calendar_utils import (
    persian_to_gregorian,
    gregorian_to_persian,
    is_leap_year_persian,
    days_in_persian_month,
    format_persian_date,
    get_persian_month_name,
    get_persian_weekday_name,
    get_persian_weekday,
    persian_day_of_year,
    persian_days_in_year,
    now_persian,
    persian_add_days,
    persian_diff_days,
    persian_from_date,
    persian_from_datetime,
    persian_to_date,
    gregorian_year_to_persian_year,
    persian_year_to_gregorian_year,
    PERSIAN_MONTH_NAMES,
    PERSIAN_MONTH_NAMES_EN,
)


def print_section(title):
    """打印章节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def demo_conversion():
    """演示日期转换"""
    print_section("日期转换")
    
    # 波斯历 -> 公历
    print("波斯历转公历:")
    persian_dates = [
        (1403, 1, 1),
        (1402, 12, 29),
        (1403, 6, 15),
        (1403, 12, 30),
    ]
    for py, pm, pd in persian_dates:
        gy, gm, gd = persian_to_gregorian(py, pm, pd)
        print(f"  波斯历 {py}/{pm}/{pd} -> 公历 {gy}/{gm}/{gd}")
    
    # 公历 -> 波斯历
    print("\n公历转波斯历:")
    gregorian_dates = [
        (2024, 3, 20),
        (2024, 3, 19),
        (2024, 12, 31),
        (2025, 1, 1),
    ]
    for gy, gm, gd in gregorian_dates:
        py, pm, pd = gregorian_to_persian(gy, gm, gd)
        print(f"  公历 {gy}/{gm}/{gd} -> 波斯历 {py}/{pm}/{pd}")


def demo_leap_year():
    """演示闰年判断"""
    print_section("闰年判断")
    
    years = [1400, 1401, 1402, 1403, 1404, 1405]
    
    print("波斯历闰年判断:")
    for year in years:
        is_leap = is_leap_year_persian(year)
        days = persian_days_in_year(year)
        status = "闰年 ✓" if is_leap else "平年"
        print(f"  {year}: {status} ({days} 天)")
    
    # 验证 Esfand 月天数
    print("\nEsfand 月（第12月）天数验证:")
    for year in years:
        days = days_in_persian_month(year, 12)
        print(f"  {year} 年 Esfand: {days} 天")


def demo_formatting():
    """演示日期格式化"""
    print_section("日期格式化")
    
    year, month, day = 1403, 6, 15
    
    print("格式化选项:")
    print(f"  短格式: {format_persian_date(year, month, day)}")
    print(f"  长格式(波斯语): {format_persian_date(year, month, day, 'long')}")
    print(f"  长格式(英语): {format_persian_date(year, month, day, 'long', 'en')}")
    print(f"  完整格式(波斯语): {format_persian_date(year, month, day, 'full')}")
    print(f"  完整格式(英语): {format_persian_date(year, month, day, 'full', 'en')}")


def demo_month_weekday_names():
    """演示月份和星期名称"""
    print_section("月份和星期名称")
    
    print("波斯历月份名称:")
    for i in range(1, 13):
        name_fa = get_persian_month_name(i)
        name_en = get_persian_month_name(i, "en")
        print(f"  {i:2d}: {name_fa} ({name_en})")
    
    print("\n波斯历星期名称:")
    for i in range(7):
        name_fa = get_persian_weekday_name(i)
        name_en = get_persian_weekday_name(i, "en")
        gregorian_day = ["周六", "周日", "周一", "周二", "周三", "周四", "周五"][i]
        print(f"  {i}: {name_fa} ({name_en}) = {gregorian_day}")


def demo_weekday():
    """演示星期计算"""
    print_section("星期计算")
    
    print("波斯历1403年1月的星期:")
    for day in range(1, 8):
        weekday = get_persian_weekday(1403, 1, day)
        weekday_name = get_persian_weekday_name(weekday)
        weekday_name_en = get_persian_weekday_name(weekday, "en")
        gy, gm, gd = persian_to_gregorian(1403, 1, day)
        gregorian_day = date(gy, gm, gd).strftime("%A")
        print(f"  {day} 日: {weekday_name} ({weekday_name_en}) = 公历 {gregorian_day}")


def demo_day_of_year():
    """演示年日计算"""
    print_section("年日计算")
    
    print("波斯历1403年重要日期的年日:")
    important_dates = [
        (1, 1),    # 新年
        (1, 13),   # Sizdah Bedar (自然日)
        (3, 14),   # 水节开始
        (6, 31),   # 夏季最后一天
        (12, 30),  # 年末
    ]
    for month, day in important_dates:
        doy = persian_day_of_year(1403, month, day)
        print(f"  {month}/{day} -> 第 {doy} 天")


def demo_current_date():
    """演示获取当前日期"""
    print_section("当前日期")
    
    # 波斯历当前日期
    py, pm, pd = now_persian()
    print("当前波斯历日期:")
    print(f"  波斯历: {py}/{pm}/{pd}")
    print(f"  格式化: {format_persian_date(py, pm, pd, 'full')}")
    print(f"  英语格式: {format_persian_date(py, pm, pd, 'full', 'en')}")
    
    # 公历对应
    gy, gm, gd = persian_to_gregorian(py, pm, pd)
    print(f"  公历对应: {gy}/{gm}/{gd}")
    
    # Python date 对象
    py_date = persian_to_date(py, pm, pd)
    print(f"  Python date: {py_date}")


def demo_date_arithmetic():
    """演示日期计算"""
    print_section("日期计算")
    
    start_date = (1403, 1, 1)
    
    print("日期加法:")
    offsets = [30, 100, 365, -1]
    for offset in offsets:
        result = persian_add_days(*start_date, offset)
        gy, gm, gd = persian_to_gregorian(*result)
        print(f"  {start_date[0]}/{start_date[1]}/{start_date[2]} + {offset} 天 -> {result[0]}/{result[1]}/{result[2]}")
    
    print("\n日期差计算:")
    date_pairs = [
        ((1403, 1, 1), (1403, 1, 11)),
        ((1403, 1, 1), (1404, 1, 1)),
        ((1402, 12, 29), (1403, 1, 1)),
    ]
    for date1, date2 in date_pairs:
        diff = persian_diff_days(*date1, *date2)
        print(f"  {date2[0]}/{date2[1]}/{date2[2]} - {date1[0]}/{date1[1]}/{date1[2]} = {diff} 天")


def demo_python_date():
    """演示与 Python date 对象的交互"""
    print_section("与 Python date 对象交互")
    
    # 从 date 对象转换
    g_date = date(2024, 3, 20)
    p_date = persian_from_date(g_date)
    print(f"从 date 转换:")
    print(f"  date(2024, 3, 20) -> 波斯历 {p_date[0]}/{p_date[1]}/{p_date[2]}")
    
    # 转换为 date 对象
    result_date = persian_to_date(1403, 1, 1)
    print(f"\n转换为 date:")
    print(f"  波斯历 1403/1/1 -> {result_date}")
    
    # datetime 支持
    dt = datetime(2024, 3, 20, 14, 30)
    p_from_dt = persian_from_datetime(dt)
    print(f"\n从 datetime 转换:")
    print(f"  datetime(2024, 3, 20, 14, 30) -> 波斯历 {p_from_dt[0]}/{p_from_dt[1]}/{p_from_dt[2]}")


def demo_year_range():
    """演示年份范围转换"""
    print_section("年份范围转换")
    
    print("公历年份对应波斯历年份范围:")
    for g_year in [2023, 2024, 2025]:
        start, end = gregorian_year_to_persian_year(g_year)
        print(f"  {g_year} -> 波斯历 {start}-{end}")
    
    print("\n波斯历年份对应公历年份范围:")
    for p_year in [1402, 1403, 1404]:
        start, end = persian_year_to_gregorian_year(p_year)
        print(f"  {p_year} -> 公历 {start}-{end}")


def demo_special_dates():
    """演示特殊日期"""
    print_section("波斯历特殊日期")
    
    special_dates = [
        ("Nowruz (新年)", 1403, 1, 1),
        ("Sizdah Bedar", 1403, 1, 13),
        ("Tirgan (水节)", 1403, 4, 1),
        ("Mehrgan", 1403, 7, 16),
        ("Yalda (冬至)", 1403, 9, 30),
        ("年末", 1403, 12, 30),
    ]
    
    print("2024-2025 波斯历年度重要日期:")
    for name, year, month, day in special_dates:
        gy, gm, gd = persian_to_gregorian(year, month, day)
        weekday = get_persian_weekday(year, month, day)
        weekday_name = get_persian_weekday_name(weekday, "en")
        print(f"  {name}: 波斯历 {month}/{day} -> 公历 {gy}/{gm}/{gd} ({weekday_name})")


def main():
    """运行所有示例"""
    print("\n" + "="*60)
    print("  Persian Calendar Utilities - 使用示例")
    print("  波斯历( Jalali )工具包演示")
    print("="*60)
    
    demo_conversion()
    demo_leap_year()
    demo_formatting()
    demo_month_weekday_names()
    demo_weekday()
    demo_day_of_year()
    demo_current_date()
    demo_date_arithmetic()
    demo_python_date()
    demo_year_range()
    demo_special_dates()
    
    print("\n" + "="*60)
    print("  示例演示完成！")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()