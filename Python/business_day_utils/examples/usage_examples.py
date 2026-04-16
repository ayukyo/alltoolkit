"""
Business Day Utils 使用示例

演示工作日计算工具库的各种用法
"""

from datetime import date, timedelta
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    BusinessDayCalculator,
    BusinessDayConfig,
    Holiday,
    create_china_holiday_calculator,
    create_us_holiday_calculator,
    is_business_day,
    add_business_days,
    business_days_between,
    next_business_day,
    previous_business_day
)


def example_basic_usage():
    """基本用法示例"""
    print("=" * 60)
    print("基本用法示例")
    print("=" * 60)
    
    calc = BusinessDayCalculator()
    
    # 判断是否为工作日
    test_date = date(2024, 1, 8)  # 周一
    print(f"{test_date} 是工作日: {calc.is_business_day(test_date)}")
    
    test_date = date(2024, 1, 6)  # 周六
    print(f"{test_date} 是工作日: {calc.is_business_day(test_date)}")
    
    # 添加工作日
    start = date(2024, 1, 8)  # 周一
    result = calc.add_business_days(start, 5)
    print(f"\n{start} + 5 个工作日 = {result}")
    
    # 计算工作日数量
    start = date(2024, 1, 1)
    end = date(2024, 1, 31)
    count = calc.business_days_inclusive(start, end)
    print(f"\n{start} 到 {end} 之间有 {count} 个工作日")
    
    # 获取下一个/上一个工作日
    friday = date(2024, 1, 5)  # 周五
    print(f"\n{friday} 的下一个工作日: {calc.next_business_day(friday)}")
    
    monday = date(2024, 1, 8)  # 周一
    print(f"{monday} 的上一个工作日: {calc.previous_business_day(monday)}")


def example_with_holidays():
    """带节假日的示例"""
    print("\n" + "=" * 60)
    print("带节假日的示例")
    print("=" * 60)
    
    config = BusinessDayConfig()
    
    # 添加节假日
    config.add_holiday("元旦", date(2024, 1, 1), is_recurring=True)
    config.add_holiday("春节", date(2024, 2, 10))
    config.add_holiday("春节", date(2024, 2, 11))
    config.add_holiday("春节", date(2024, 2, 12))
    config.add_holiday("春节", date(2024, 2, 13))
    config.add_holiday("春节", date(2024, 2, 14))
    config.add_holiday("春节", date(2024, 2, 15))
    config.add_holiday("春节", date(2024, 2, 16))
    config.add_holiday("春节", date(2024, 2, 17))
    
    # 添加调休工作日
    config.add_adjusted_workday(date(2024, 2, 4))   # 春节前调休
    config.add_adjusted_workday(date(2024, 2, 18))  # 春节后调休
    
    calc = BusinessDayCalculator(config)
    
    # 测试节假日
    new_year = date(2024, 1, 1)
    print(f"{new_year} 是节假日: {not calc.is_business_day(new_year)}")
    
    # 测试调休工作日
    adjusted = date(2024, 2, 4)  # 周日调休
    print(f"{adjusted} 是调休工作日: {calc.is_business_day(adjusted)}")
    
    # 春节假期期间的工作日计算
    print(f"\n春节期间 (2024-02-10 ~ 2024-02-17) 的工作日:")
    start = date(2024, 2, 9)
    end = date(2024, 2, 18)
    business_days = calc.get_business_days_in_range(start, end)
    for d in business_days:
        print(f"  {d} ({['周一','周二','周三','周四','周五','周六','周日'][d.weekday()]})")


def example_china_holidays():
    """中国节假日示例"""
    print("\n" + "=" * 60)
    print("中国节假日示例")
    print("=" * 60)
    
    calc = create_china_holiday_calculator(2024)
    
    # 检查固定节假日
    holidays = [
        (date(2024, 1, 1), "元旦"),
        (date(2024, 5, 1), "劳动节"),
        (date(2024, 10, 1), "国庆节"),
    ]
    
    for hol_date, name in holidays:
        is_hol, hol_name = calc.is_holiday(hol_date)
        print(f"{hol_date}: {'是' if is_hol else '不是'}节假日 ({hol_name or '否'})")
    
    # 计算某月工作日数量
    print(f"\n2024年1月工作日数量: {calc.business_days_in_month(2024, 1)}")
    print(f"2024年5月工作日数量: {calc.business_days_in_month(2024, 5)}")


def example_us_holidays():
    """美国节假日示例"""
    print("\n" + "=" * 60)
    print("美国节假日示例")
    print("=" * 60)
    
    calc = create_us_holiday_calculator(2024)
    
    # 列出2024年所有节假日
    print("2024年美国节假日:")
    
    start = date(2024, 1, 1)
    end = date(2024, 12, 31)
    
    holidays = calc.list_holidays_in_range(start, end)
    for hol_date, holiday in holidays:
        print(f"  {hol_date}: {holiday.name}")


def example_business_day_calculations():
    """工作日计算示例"""
    print("\n" + "=" * 60)
    print("工作日计算示例")
    print("=" * 60)
    
    calc = BusinessDayCalculator()
    
    # 计算项目截止日期（假设需要10个工作日）
    start_date = date(2024, 1, 8)
    deadline = calc.add_business_days(start_date, 10)
    print(f"项目开始: {start_date}")
    print(f"项目截止: {deadline} (10个工作日后)")
    
    # 获取接下来5个工作日
    print(f"\n接下来5个工作日:")
    next_days = calc.get_next_n_business_days(start_date, 5)
    for d in next_days:
        weekday = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][d.weekday()]
        print(f"  {d} ({weekday})")
    
    # 获取某月第1个和最后一个工作日
    year, month = 2024, 1
    first_bd = calc.nth_business_day_of_month(year, month, 1)
    last_bd = calc.nth_business_day_of_month(year, month, -1)
    print(f"\n{year}年{month}月:")
    print(f"  第一个工作日: {first_bd}")
    print(f"  最后一个工作日: {last_bd}")


def example_project_planning():
    """项目规划示例"""
    print("\n" + "=" * 60)
    print("项目规划示例")
    print("=" * 60)
    
    config = BusinessDayConfig()
    # 假设公司在春节期间放假
    spring_festival_dates = [
        date(2024, 2, 10), date(2024, 2, 11), date(2024, 2, 12),
        date(2024, 2, 13), date(2024, 2, 14), date(2024, 2, 15),
        date(2024, 2, 16), date(2024, 2, 17)
    ]
    for d in spring_festival_dates:
        config.add_holiday("春节", d)
    
    calc = BusinessDayCalculator(config)
    
    # 项目计划：从2024年1月15日开始，需要30个工作日
    project_start = date(2024, 1, 15)
    required_days = 30
    project_end = calc.add_business_days(project_start, required_days)
    
    print(f"项目开始日期: {project_start}")
    print(f"所需工作日: {required_days} 天")
    print(f"预计完成日期: {project_end}")
    
    # 计算每个月的工作日分配
    print("\n各月工作日分配:")
    current = project_start
    month_days = {}
    
    while current <= project_end:
        if calc.is_business_day(current):
            month_key = f"{current.year}年{current.month}月"
            month_days[month_key] = month_days.get(month_key, 0) + 1
        current += timedelta(days=1)
    
    for month, days in sorted(month_days.items()):
        print(f"  {month}: {days} 个工作日")


def example_custom_work_week():
    """自定义工作周示例"""
    print("\n" + "=" * 60)
    print("自定义工作周示例")
    print("=" * 60)
    
    # 示例1：六天工作制（周日休息）
    config_six_days = BusinessDayConfig(
        workdays={0, 1, 2, 3, 4, 5},  # 周一到周六
        weekends={6}  # 周日
    )
    calc_six = BusinessDayCalculator(config_six_days)
    
    print("六天工作制:")
    print(f"  周六 (2024-01-06) 是工作日: {calc_six.is_business_day(date(2024, 1, 6))}")
    print(f"  周日 (2024-01-07) 是工作日: {calc_six.is_business_day(date(2024, 1, 7))}")
    
    # 示例2：中东工作周（周日到周四工作）
    config_middle_east = BusinessDayConfig(
        workdays={0, 1, 2, 3, 6},  # 周一到周四 + 周日
        weekends={4, 5}  # 周五、周六
    )
    calc_me = BusinessDayCalculator(config_middle_east)
    
    print("\n中东工作周:")
    print(f"  周五 (2024-01-05) 是工作日: {calc_me.is_business_day(date(2024, 1, 5))}")
    print(f"  周六 (2024-01-06) 是工作日: {calc_me.is_business_day(date(2024, 1, 6))}")
    print(f"  周日 (2024-01-07) 是工作日: {calc_me.is_business_day(date(2024, 1, 7))}")


def example_convenience_functions():
    """便捷函数示例"""
    print("\n" + "=" * 60)
    print("便捷函数示例")
    print("=" * 60)
    
    # 使用便捷函数（不需要创建计算器实例）
    test_date = date(2024, 1, 8)
    print(f"使用便捷函数:")
    print(f"  {test_date} 是工作日: {is_business_day(test_date)}")
    
    start = date(2024, 1, 8)
    print(f"  {start} + 5 个工作日 = {add_business_days(start, 5)}")
    
    end = date(2024, 1, 15)
    print(f"  {start} 到 {end} 之间有 {business_days_between(start, end)} 个工作日")
    
    print(f"  {test_date} 的下一个工作日: {next_business_day(test_date)}")
    print(f"  {test_date} 的上一个工作日: {previous_business_day(test_date)}")


def example_find_special_days():
    """查找特殊日期示例"""
    print("\n" + "=" * 60)
    print("查找特殊日期示例")
    print("=" * 60)
    
    calc = BusinessDayCalculator()
    
    # 找下一个发薪日（假设15号发薪）
    today = date(2024, 1, 1)
    pay_day = calc.find_next_business_day_matching(
        today,
        lambda d: d.day == 15
    )
    print(f"下一个发薪日（15号）: {pay_day}")
    
    # 找下一个周一
    next_monday = calc.find_next_business_day_matching(
        today,
        lambda d: d.weekday() == 0
    )
    print(f"下一个周一: {next_monday}")
    
    # 找下一个月末工作日
    end_of_month = calc.get_month_end_business_day(today.year, today.month)
    print(f"本月最后一个工作日: {end_of_month}")


def main():
    """运行所有示例"""
    example_basic_usage()
    example_with_holidays()
    example_china_holidays()
    example_us_holidays()
    example_business_day_calculations()
    example_project_planning()
    example_custom_work_week()
    example_convenience_functions()
    example_find_special_days()
    
    print("\n" + "=" * 60)
    print("所有示例完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()