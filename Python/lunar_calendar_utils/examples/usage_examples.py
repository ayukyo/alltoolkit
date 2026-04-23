"""
农历日历工具模块使用示例 (Lunar Calendar Utils Examples)
================================================

展示农历日历工具的主要功能：
- 公历农历转换
- 干支计算
- 节气查询
- 节日查询
- 完整信息展示

作者: AllToolkit 自动化开发助手
日期: 2026-04-23
"""

from datetime import date
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    LunarDate, LunarCalendar,
    solar_to_lunar, lunar_to_solar,
    get_year_ganzhi, get_day_ganzhi, get_month_ganzhi, get_hour_ganzhi,
    get_zodiac, get_constellation,
    get_solar_term_year, get_current_solar_term,
    get_lunar_festival, get_solar_festival, get_all_festivals,
    format_lunar_date, get_lunar_info,
    today_lunar, today_info, quick_convert,
    LUNAR_MONTH_NAMES, LUNAR_DAY_NAMES
)


def example_01_basic_conversion():
    """示例1：基本转换"""
    print("\n" + "=" * 50)
    print("示例1：公历农历基本转换")
    print("=" * 50)
    
    # 公历转农历
    print("\n【公历转农历】")
    solar_dates = [
        (2024, 2, 10),  # 春节
        (2024, 9, 17),  # 中秋节
        (2024, 6, 10),  # 端午节
        (2023, 3, 22),  # 闰二月
    ]
    
    for y, m, d in solar_dates:
        lunar = solar_to_lunar(y, m, d)
        if lunar:
            print(f"  公历 {y}-{m}-{d} -> {format_lunar_date(lunar)}")
    
    # 农历转公历
    print("\n【农历转公历】")
    lunar_dates = [
        (2024, 1, 1, False),   # 正月初一
        (2024, 8, 15, False),  # 八月十五
        (2024, 5, 5, False),   # 五月初五
        (2023, 2, 1, True),    # 闰二月初一
    ]
    
    for y, m, d, is_leap in lunar_dates:
        solar = lunar_to_solar(y, m, d, is_leap)
        leap_str = "闰" if is_leap else ""
        if solar:
            print(f"  农历 {y}年{leap_str}{LUNAR_MONTH_NAMES[m]}{LUNAR_DAY_NAMES[d]} -> {solar}")


def example_02_ganzhi():
    """示例2：干支计算"""
    print("\n" + "=" * 50)
    print("示例2：干支计算")
    print("=" * 50)
    
    # 年干支
    print("\n【年干支】")
    for year in [1984, 2000, 2024, 2025, 2030]:
        ganzhi = get_year_ganzhi(year)
        zodiac = get_zodiac(year)
        print(f"  {year}年: {ganzhi}年（{zodiac}年）")
    
    # 日干支
    print("\n【日干支】")
    dates = [(2024, 1, 1), (2024, 2, 10), (2024, 12, 31)]
    for y, m, d in dates:
        ganzhi = get_day_ganzhi(y, m, d)
        print(f"  {y}-{m}-{d}: {ganzhi}日")
    
    # 时辰干支
    print("\n【时辰干支】")
    hours = [0, 6, 12, 18, 23]
    day_ganzhi = "甲子"
    for hour in hours:
        hour_ganzhi = get_hour_ganzhi(day_ganzhi, hour)
        print(f"  {hour}点: {hour_ganzhi}")


def example_03_zodiac_constellation():
    """示例3：生肖与星座"""
    print("\n" + "=" * 50)
    print("示例3：生肖与星座")
    print("=" * 50)
    
    # 生肖
    print("\n【生肖】")
    for year in [2020, 2021, 2022, 2023, 2024, 2025, 2026]:
        zodiac = get_zodiac(year)
        print(f"  {year}年: {zodiac}")
    
    # 星座
    print("\n【星座】")
    dates = [(1, 1), (2, 14), (3, 21), (5, 20), (7, 23), (10, 24), (12, 25)]
    for m, d in dates:
        constellation = get_constellation(m, d)
        print(f"  {m}月{d}日: {constellation}")


def example_04_solar_terms():
    """示例4：节气查询"""
    print("\n" + "=" * 50)
    print("示例4：节气查询")
    print("=" * 50)
    
    # 一年节气
    print("\n【2024年节气】")
    terms = get_solar_term_year(2024)
    for i, (name, term_date) in enumerate(terms):
        print(f"  {name}: {term_date}")
        if i >= 11:  # 只显示上半年
            print("  ...")
            break
    
    # 当前节气
    print("\n【指定日期节气】")
    dates = [(2024, 1, 6), (2024, 6, 21), (2024, 12, 22)]
    for y, m, d in dates:
        term, days = get_current_solar_term(y, m, d)
        print(f"  {y}-{m}-{d}: 当前节气 {term}, 距下个节气 {days} 天")


def example_05_festivals():
    """示例5：节日查询"""
    print("\n" + "=" * 50)
    print("示例5：节日查询")
    print("=" * 50)
    
    # 农历节日
    print("\n【农历传统节日】")
    lunar_festivals = [
        (2024, 1, 1),   # 春节
        (2024, 1, 15),  # 元宵
        (2024, 5, 5),   # 端午
        (2024, 7, 7),   # 七夕
        (2024, 8, 15),  # 中秋
        (2024, 9, 9),   # 重阳
    ]
    
    for y, m, d in lunar_festivals:
        festival = get_lunar_festival(y, m, d)
        month_name = LUNAR_MONTH_NAMES[m]
        day_name = LUNAR_DAY_NAMES[d]
        print(f"  农历{month_name}{day_name}: {festival}")
    
    # 公历节日
    print("\n【公历节日】")
    solar_festivals = [
        (1, 1), (2, 14), (5, 1), (6, 1), (10, 1), (12, 25)
    ]
    
    for m, d in solar_festivals:
        festival = get_solar_festival(m, d)
        print(f"  {m}月{d}日: {festival}")
    
    # 综合节日查询
    print("\n【某日所有节日】")
    dates = [(2024, 1, 1), (2024, 2, 10), (2024, 10, 1)]
    for y, m, d in dates:
        festivals = get_all_festivals(y, m, d)
        print(f"  {y}-{m}-{d}: {', '.join(festivals) if festivals else '无'}")


def example_06_complete_info():
    """示例6：完整信息"""
    print("\n" + "=" * 50)
    print("示例6：日期完整信息")
    print("=" * 50)
    
    # 获取完整农历信息
    dates = [
        (2024, 2, 10),   # 春节
        (2024, 9, 17),   # 中秋
        (date.today().year, date.today().month, date.today().day),  # 今天
    ]
    
    for y, m, d in dates:
        info = get_lunar_info(y, m, d)
        print(f"\n【{y}-{m}-{d}】")
        print(f"  公历日期: {info['solar_date']}")
        print(f"  农历日期: {info['lunar_date']}")
        print(f"  干支纪年: {info['year_ganzhi']}年")
        print(f"  生肖: {info['zodiac']}")
        print(f"  星座: {info['constellation']}")
        print(f"  当前节气: {info['solar_term']}")
        print(f"  节日: {', '.join(info['festivals']) if info['festivals'] else '无'}")


def example_07_lunar_calendar_class():
    """示例7：LunarCalendar类"""
    print("\n" + "=" * 50)
    print("示例7：LunarCalendar类使用")
    print("=" * 50)
    
    # 创建年历
    cal = LunarCalendar(2024)
    
    print("\n【2024年信息】")
    info = cal.get_year_info()
    print(f"  干支: {info['ganzhi']}")
    print(f"  生肖: {info['zodiac']}")
    print(f"  闰月: {info['leap_month'] if info['leap_month'] else '无'}")
    
    # 带日期的日历
    cal_date = LunarCalendar(2024, 2, 10)
    lunar = cal_date.get_lunar_date()
    print(f"\n【2024年2月10日】")
    print(f"  农历: {format_lunar_date(lunar)}")
    
    # 月历
    print("\n【2024年2月月历（部分）】")
    month_cal = cal.get_month_calendar(2)
    for week_idx, week in enumerate(month_cal[:2]):  # 只显示两周
        print(f"  第{week_idx + 1}周:")
        for day_info in week:
            if day_info:
                d = day_info['solar'].day
                lunar_str = str(day_info['lunar']) if day_info['lunar'] else ""
                print(f"    {d}号: {lunar_str}")


def example_08_today():
    """示例8：今天信息"""
    print("\n" + "=" * 50)
    print("示例8：今天农历信息")
    print("=" * 50)
    
    # 快速获取今天农历
    lunar = today_lunar()
    if lunar:
        print(f"\n【今天农历】")
        print(f"  {format_lunar_date(lunar)}")
    
    # 完整信息
    info = today_info()
    print(f"\n【今天完整信息】")
    print(f"  公历: {info['solar_date']}")
    print(f"  农历: {info['lunar_date']}")
    print(f"  干支: {info['year_ganzhi']}年")
    print(f"  生肖: {info['zodiac']}年")
    print(f"  星座: {info['constellation']}")
    print(f"  节气: {info['solar_term']}")
    if info['festivals']:
        print(f"  节日: {', '.join(info['festivals'])}")
    
    # 快速转换
    print(f"\n【快速转换】")
    print(f"  {quick_convert(date.today())}")


def example_09_special_cases():
    """示例9：特殊情况"""
    print("\n" + "=" * 50)
    print("示例9：特殊情况处理")
    print("=" * 50)
    
    # 闰月
    print("\n【闰月】")
    print("  2023年有闰二月:")
    lunar = solar_to_lunar(2023, 3, 22)
    if lunar:
        print(f"    2023-03-22 -> {lunar} (is_leap={lunar.is_leap_month})")
    
    solar = lunar_to_solar(2023, 2, 1, True)
    if solar:
        print(f"    农历闰二月初一 -> {solar}")
    
    # 除夕
    print("\n【除夕】")
    lunar = solar_to_lunar(2024, 2, 9)  # 2024年除夕前一天
    if lunar:
        print(f"  2024-02-09 -> {lunar}")
    
    lunar = solar_to_lunar(2024, 2, 10)  # 春节
    if lunar:
        print(f"  2024-02-10 -> {lunar}")
    
    # 大月小月
    print("\n【农历大小月】")
    from lunar_calendar_utils.mod import get_lunar_month_days
    for month in [1, 2, 3, 4, 5, 6]:
        days = get_lunar_month_days(2024, month)
        print(f"  2024年{LUNAR_MONTH_NAMES[month]}: {days}天")


def example_10_batch_conversion():
    """示例10：批量转换"""
    print("\n" + "=" * 50)
    print("示例10：批量转换")
    print("=" * 50)
    
    # 一周转换
    print("\n【本周农历】")
    today = date.today()
    for i in range(7):
        d = today.replace(day=today.day) if today.day <= 28 else today
        from datetime import timedelta
        d = today + timedelta(days=i)
        lunar = solar_to_lunar(d.year, d.month, d.day)
        if lunar:
            print(f"  {d}: {str(lunar)}")
    
    # 一年重要日期
    print("\n【2024年重要农历日期】")
    important_dates = [
        (2024, 2, 10),   # 春节
        (2024, 2, 24),   # 元宵
        (2024, 4, 4),    # 清明
        (2024, 6, 10),   # 端午
        (2024, 9, 17),   # 中秋
        (2024, 10, 11),  # 重阳
    ]
    
    for y, m, d in important_dates:
        lunar = solar_to_lunar(y, m, d)
        festivals = get_all_festivals(y, m, d)
        if lunar:
            print(f"  {y}-{m}-{d}: {str(lunar)} ({', '.join(festivals)})")


def main():
    """运行所有示例"""
    example_01_basic_conversion()
    example_02_ganzhi()
    example_03_zodiac_constellation()
    example_04_solar_terms()
    example_05_festivals()
    example_06_complete_info()
    example_07_lunar_calendar_class()
    example_08_today()
    example_09_special_cases()
    example_10_batch_conversion()
    
    print("\n" + "=" * 50)
    print("所有示例完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()