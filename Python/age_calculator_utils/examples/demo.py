"""
Age Calculator Utilities 使用示例

演示各种年龄计算功能的使用方法。
"""

from datetime import date
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    AgeCalculatorUtils, Generation,
    calculate_age, calculate_exact_age, days_until_birthday,
    get_generation, format_age
)


def print_section(title):
    """打印分隔线"""
    print(f"\n{'='*50}")
    print(f"  {title}")
    print('='*50)


def main():
    print("\n🎂 年龄计算工具演示程序 🎂")
    
    # 示例出生日期
    birth_date = "1990-05-15"
    today = date.today()
    
    print_section("1. 基本年龄计算")
    age = calculate_age(birth_date)
    print(f"出生日期: {birth_date}")
    print(f"当前年龄: {age}岁")
    
    print_section("2. 精确年龄")
    years, months, days = calculate_exact_age(birth_date)
    print(f"精确年龄: {years}岁{months}个月{days}天")
    
    print_section("3. 年龄格式化")
    print(f"完整格式: {format_age(birth_date, format_type='full')}")
    print(f"简单格式: {format_age(birth_date, format_type='simple')}")
    print(f"天数格式: {format_age(birth_date, format_type='days')}")
    print(f"周数格式: {format_age(birth_date, format_type='weeks')}")
    
    print_section("4. 不同单位的年龄")
    print(f"已生活天数: {AgeCalculatorUtils.calculate_age_in_days(birth_date)}天")
    weeks, days = AgeCalculatorUtils.calculate_age_in_weeks(birth_date)
    print(f"已生活周数: {weeks}周{days}天")
    print(f"已生活月数: {AgeCalculatorUtils.calculate_age_in_months(birth_date)}个月")
    print(f"已生活小时: {AgeCalculatorUtils.calculate_age_in_hours(birth_date)}小时")
    
    print_section("5. 生日倒计时")
    days_to_birthday = days_until_birthday(birth_date)
    next_birthday = AgeCalculatorUtils.next_birthday_date(birth_date)
    print(f"距离下次生日: {days_to_birthday}天")
    print(f"下次生日日期: {next_birthday}")
    if days_to_birthday == 0:
        print("🎉 今天是生日！生日快乐！🎉")
    
    print_section("6. 完整生日信息")
    info = AgeCalculatorUtils.get_birthday_info(birth_date)
    print(f"当前年龄: {info['current_age']}岁")
    print(f"精确年龄: {info['exact_age']['years']}年 {info['exact_age']['months']}月 {info['exact_age']['days']}日")
    print(f"今天是否生日: {'是' if info['is_birthday_today'] else '否'}")
    print(f"距离下次生日: {info['days_until_birthday']}天")
    print(f"下次生日年龄: {info['next_birthday_age']}岁")
    print(f"已生活总天数: {info['total_days_lived']}天")
    print(f"已生活总周数: {info['total_weeks_lived']}周")
    
    print_section("7. 代际分类")
    generation = get_generation(birth_date)
    print(f"代际: {generation.value}")
    
    gen_info = AgeCalculatorUtils.get_generation_info(birth_date)
    print(f"英文名: {gen_info['english_name']}")
    print(f"年份范围: {gen_info['year_range'][0]}-{gen_info['year_range'][1]}")
    print(f"描述: {gen_info['description']}")
    print(f"特征: {', '.join(gen_info['characteristics'])}")
    
    print_section("8. 年龄里程碑")
    print("即将到来的里程碑:")
    milestone = AgeCalculatorUtils.get_next_milestone(birth_date)
    if milestone:
        print(f"  {milestone['description']}")
        print(f"  日期: {milestone['date']}")
        print(f"  还有: {milestone['days_until']}天")
    
    print("\n所有重要年龄生日:")
    milestones = AgeCalculatorUtils.get_age_milestones(birth_date)
    age_milestones = [m for m in milestones if m['type'] == '年龄生日'][:5]
    for m in age_milestones:
        status = f"（{m['status']}）" if m['status'] != '未到' else ""
        print(f"  {m['description']}: {m['date']} {status}")
    
    print_section("9. 年龄差计算")
    date1 = "1990-05-15"
    date2 = "1985-03-20"
    diff = AgeCalculatorUtils.calculate_age_difference(date1, date2)
    print(f"日期1: {date1}")
    print(f"日期2: {date2}")
    print(f"年龄差: {diff['difference_years']}年 {diff['difference_months']}个月")
    print(f"相差天数: {diff['difference_days']}天")
    print(f"相差周数: {diff['difference_weeks']}周")
    
    print_section("10. 中国生肖")
    zodiac = AgeCalculatorUtils.get_chinese_zodiac(birth_date)
    print(f"出生年份: {birth_date[:4]}年")
    print(f"生肖: {zodiac}")
    
    # 测试几个不同年份
    print("\n生肖对照表:")
    test_years = [2020, 2021, 2022, 2023, 2024]
    for year in test_years:
        z = AgeCalculatorUtils.get_chinese_zodiac(f"{year}-01-01")
        print(f"  {year}年: {z}")
    
    print_section("11. 闰年生日宝宝")
    leap_birth = "2000-02-29"
    is_leap = AgeCalculatorUtils.is_leap_year_baby(leap_birth)
    print(f"出生日期: {leap_birth}")
    print(f"是否闰年宝宝: {'是' if is_leap else '否'}")
    
    if is_leap:
        leap_info = AgeCalculatorUtils.get_leap_year_birthday_info(leap_birth)
        print(f"真实生日次数: {leap_info['real_birthday_count']}次")
        if leap_info['next_real_birthday']:
            print(f"下次真实生日: {leap_info['next_real_birthday']}")
    
    # 测试非闰年宝宝
    normal_birth = "2000-03-01"
    is_leap_normal = AgeCalculatorUtils.is_leap_year_baby(normal_birth)
    print(f"\n出生日期: {normal_birth}")
    print(f"是否闰年宝宝: {'是' if is_leap_normal else '否'}")
    
    print_section("12. 代际示例")
    print("不同年份出生的代际分类:")
    test_births = [
        "1920-01-01",  # 最伟大一代
        "1935-01-01",  # 沉默一代
        "1955-01-01",  # 婴儿潮
        "1975-01-01",  # X世代
        "1990-01-01",  # 千禧一代
        "2005-01-01",  # Z世代
        "2018-01-01",  # 阿尔法世代
    ]
    
    for birth in test_births:
        gen = get_generation(birth)
        print(f"  {birth[:4]}年出生: {gen.value}")
    
    print("\n" + "="*50)
    print("  演示完成！")
    print("="*50 + "\n")


if __name__ == "__main__":
    main()