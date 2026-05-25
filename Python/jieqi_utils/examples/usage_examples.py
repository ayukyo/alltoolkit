"""
节气工具模块使用示例 (Jieqi Utils Usage Examples)

演示节气计算、查询和相关功能的使用方法。
"""

from datetime import date
from mod import (
    get_jieqi_date,
    get_year_jieqi_list,
    get_current_jieqi,
    get_next_jieqi,
    get_days_to_next_jieqi,
    get_jieqi_health_advice,
    get_jieqi_traditions,
    get_jieqi_info,
    get_season_jieqi,
    is_jieqi_day,
    get_jieqi_by_month,
    format_jieqi_report,
    get_jieqi_name_list,
    get_current_season,
    get_quarter_jieqi,
    search_jieqi,
)


def example_get_jieqi_date():
    """示例：获取节气日期"""
    print("\n=== 获取节气日期 ===")
    
    # 获取立春日期
    lichun = get_jieqi_date(2024, "立春")
    print(f"2024年立春日期: {lichun}")
    
    # 获取冬至日期
    dongzhi = get_jieqi_date(2024, "冬至")
    print(f"2024年冬至日期: {dongzhi}")
    
    # 获取多个节气日期
    print("\n2024年重要节气日期:")
    for name in ["立春", "清明", "立夏", "夏至", "立秋", "中秋", "立冬", "冬至"]:
        jieqi_date = get_jieqi_date(2024, name)
        if jieqi_date:
            print(f"  {name}: {jieqi_date.strftime('%Y年%m月%d日')}")


def example_get_year_jieqi_list():
    """示例：获取一年所有节气"""
    print("\n=== 获取2024年所有节气 ===")
    
    jieqi_list = get_year_jieqi_list(2024)
    
    print("节气列表:")
    for info in jieqi_list:
        print(f"  {info.name}: {info.date.strftime('%m月%d日')} ({info.season})")


def example_current_jieqi():
    """示例：获取当前节气"""
    print("\n=== 获取当前节气 ===")
    
    # 获取今天的当前节气
    current = get_current_jieqi()
    if current:
        print(f"当前节气: {current.name}")
        print(f"节气日期: {current.date}")
        print(f"所属季节: {current.season}")
    
    # 获取指定日期的当前节气
    test_date = date(2024, 2, 10)
    current = get_current_jieqi(test_date)
    print(f"\n{test_date} 的当前节气: {current.name if current else '未知'}")


def example_next_jieqi():
    """示例：获取下一个节气"""
    print("\n=== 获取下一个节气 ===")
    
    # 获取下一个节气
    next_jieqi = get_next_jieqi()
    if next_jieqi:
        print(f"下一个节气: {next_jieqi.name}")
        print(f"日期: {next_jieqi.date}")
        days = get_days_to_next_jieqi()
        print(f"距离天数: {days}天")
    
    # 获取指定日期的下一个节气
    test_date = date(2024, 2, 1)
    next_jieqi = get_next_jieqi(test_date)
    if next_jieqi:
        print(f"\n{test_date} 的下一个节气: {next_jieqi.name}")
        print(f"日期: {next_jieqi.date}")


def example_jieqi_advice():
    """示例：节气养生建议和习俗"""
    print("\n=== 节气养生建议和传统习俗 ===")
    
    # 获取立春的养生建议
    advice = get_jieqi_health_advice("立春")
    print("立春养生建议:")
    for a in advice:
        print(f"  • {a}")
    
    # 获取清明的传统习俗
    traditions = get_jieqi_traditions("清明")
    print("\n清明传统习俗:")
    for t in traditions:
        print(f"  • {t}")
    
    # 获取冬至的养生建议和习俗
    print("\n冬至:")
    advice = get_jieqi_health_advice("冬至")
    for a in advice:
        print(f"  养生: {a}")
    
    traditions = get_jieqi_traditions("冬至")
    for t in traditions:
        print(f"  习俗: {t}")


def example_jieqi_info():
    """示例：节气详细信息"""
    print("\n=== 节气详细信息 ===")
    
    # 获取立春详细信息
    info = get_jieqi_info("立春")
    print("立春详细信息:")
    print(f"  名称: {info['name']}")
    print(f"  季节: {info['season']}")
    print(f"  月份: {info['month']}")
    print(f"  含义: {info['description']}")
    print(f"  是否节气: {info['is_jieqi']}")
    
    # 获取多个节气信息
    print("\n夏季节气信息:")
    for name in get_season_jieqi("夏"):
        info = get_jieqi_info(name)
        print(f"  {name}: {info['description']}")


def example_season_jieqi():
    """示例：季节节气查询"""
    print("\n=== 季节气查询 ===")
    
    # 春季节气
    spring = get_season_jieqi("春")
    print(f"春季节气: {spring}")
    
    # 夏季节气
    summer = get_season_jieqi("夏")
    print(f"夏季节气: {summer}")
    
    # 秋季节气
    autumn = get_season_jieqi("秋")
    print(f"秋季节气: {autumn}")
    
    # 冬季节气
    winter = get_season_jieqi("冬")
    print(f"冬季节气: {winter}")


def example_jieqi_day():
    """示例：节气日判断"""
    print("\n=== 节气日判断 ===")
    
    # 检查今天是否是节气日
    is_today = is_jieqi_day()
    print(f"今天是否节气日: {is_today}")
    
    # 检查立春日期是否是节气日
    lichun_date = get_jieqi_date(2024, "立春")
    is_lichun = is_jieqi_day(lichun_date)
    print(f"立春日期({lichun_date})是否节气日: {is_lichun}")
    
    # 检查非节气日
    test_date = date(2024, 2, 10)
    is_test = is_jieqi_day(test_date)
    print(f"{test_date}是否节气日: {is_test}")


def example_jieqi_by_month():
    """示例：月份节气查询"""
    print("\n=== 月份节气查询 ===")
    
    for month in range(1, 13):
        jieqi = get_jieqi_by_month(month)
        print(f"{month}月节气: {jieqi[0]}、{jieqi[1]}")


def example_format_report():
    """示例：节气报告格式化"""
    print("\n=== 节气报告格式化 ===")
    
    # 获取立春信息并格式化报告
    jieqi_list = get_year_jieqi_list(2024)
    lichun = jieqi_list[2]  # 立春
    
    report = format_jieqi_report(lichun)
    print(report)
    
    print("\n" + "-" * 30 + "\n")
    
    # 冬至报告
    dongzhi = jieqi_list[23]
    report = format_jieqi_report(dongzhi)
    print(report)


def example_current_season():
    """示例：获取当前季节"""
    print("\n=== 当前季节 ===")
    
    # 获取当前季节
    season = get_current_season()
    print(f"当前季节: {season}")
    
    # 获取指定日期的季节
    dates = [
        date(2024, 3, 15),  # 春季
        date(2024, 6, 15),  # 夏季
        date(2024, 9, 15),  # 秋季
        date(2024, 12, 15),  # 冬季
    ]
    
    for d in dates:
        season = get_current_season(d)
        print(f"{d.strftime('%m月%d日')}: {season}")


def example_quarter_jieqi():
    """示例：四时八节"""
    print("\n=== 四时八节 ===")
    
    quarter = get_quarter_jieqi()
    print("四时八节:")
    for name, desc in quarter.items():
        jieqi_date = get_jieqi_date(2024, name)
        if jieqi_date:
            print(f"  {name} ({desc}): {jieqi_date.strftime('%m月%d日')}")


def example_search_jieqi():
    """示例：节气搜索"""
    print("\n=== 节气搜索 ===")
    
    # 搜索包含"春"的节气
    result = search_jieqi("春")
    print(f"包含'春'的节气: {result}")
    
    # 搜索包含"立"的节气
    result = search_jieqi("立")
    print(f"包含'立'的节气: {result}")
    
    # 搜索包含"至"的节气
    result = search_jieqi("至")
    print(f"包含'至'的节气: {result}")


def example_complete_workflow():
    """示例：完整工作流程"""
    print("\n=== 完整工作流程：今日节气状态 ===")
    
    today = date.today()
    
    # 获取当前节气
    current = get_current_jieqi(today)
    if current:
        print(f"\n当前节气: {current.name}")
        print(f"节气日期: {current.date.strftime('%Y年%m月%d日')}")
        print(f"节气含义: {current.description}")
        
        # 养生建议
        advice = get_jieqi_health_advice(current.name)
        if advice:
            print("\n养生建议:")
            for a in advice:
                print(f"  • {a}")
        
        # 传统习俗
        traditions = get_jieqi_traditions(current.name)
        if traditions:
            print("\n传统习俗:")
            for t in traditions:
                print(f"  • {t}")
    
    # 获取下一个节气
    next_j = get_next_jieqi(today)
    if next_j:
        print(f"\n下一个节气: {next_j.name}")
        print(f"日期: {next_j.date.strftime('%Y年%m月%d日')}")
        days = get_days_to_next_jieqi(today)
        print(f"距离: {days}天")
    
    # 检查是否节气日
    if is_jieqi_day(today):
        print("\n今天是节气日！")
    else:
        print(f"\n今天不是节气日，当前处于【{current.name if current else '未知'}】节气")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("节气工具模块 (jieqi_utils) 使用示例")
    print("=" * 60)
    
    example_get_jieqi_date()
    example_get_year_jieqi_list()
    example_current_jieqi()
    example_next_jieqi()
    example_jieqi_advice()
    example_jieqi_info()
    example_season_jieqi()
    example_jieqi_day()
    example_jieqi_by_month()
    example_format_report()
    example_current_season()
    example_quarter_jieqi()
    example_search_jieqi()
    example_complete_workflow()
    
    print("\n" + "=" * 60)
    print("所有示例运行完毕")
    print("=" * 60)


if __name__ == "__main__":
    main()