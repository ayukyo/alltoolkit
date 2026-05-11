"""
自然语言日期解析工具库 - 使用示例
Examples for Natural Date Parser Utilities

展示各种自然语言日期表达式的解析方法和应用场景。
"""

from datetime import datetime
from natural_date_utils import (
    NaturalDateParser,
    parse,
    parse_with_info,
    is_valid,
    get_date_type,
    parse_range,
    parse_batch,
    extract_dates,
    DateType,
)


def example_basic_relative_dates():
    """示例1：基本相对日期解析"""
    print("=" * 60)
    print("示例1：基本相对日期解析")
    print("=" * 60)
    
    now = datetime(2024, 1, 15, 10, 30, 0)  # 周一 上午10:30
    parser = NaturalDateParser(now=now)
    
    expressions = [
        "今天",
        "明天",
        "后天",
        "昨天",
        "前天",
        "大后天",
        "大前天",
    ]
    
    for expr in expressions:
        result = parser.parse(expr)
        if result.success:
            print(f"  '{expr}' → {result.datetime_obj.strftime('%Y-%m-%d %H:%M')}")
    
    print()


def example_relative_dates_with_time():
    """示例2：带时间的相对日期"""
    print("=" * 60)
    print("示例2：带时间的相对日期")
    print("=" * 60)
    
    now = datetime(2024, 1, 15, 10, 30, 0)
    parser = NaturalDateParser(now=now)
    
    expressions = [
        "今天下午3点",
        "明天早上8点",
        "后天晚上9点",
        "昨天中午",
        "明天15点30分",
    ]
    
    for expr in expressions:
        result = parser.parse(expr)
        if result.success:
            print(f"  '{expr}' → {result.datetime_obj.strftime('%Y-%m-%d %H:%M')}")
            print(f"    类型: {result.date_type.value}, 包含时间: {result.has_time}")
    
    print()


def example_weekday_dates():
    """示例3：星期日期解析"""
    print("=" * 60)
    print("示例3：星期日期解析")
    print("=" * 60)
    
    now = datetime(2024, 1, 15, 10, 30, 0)  # 周一
    parser = NaturalDateParser(now=now)
    
    expressions = [
        "周一",
        "周三",
        "周五",
        "下周二",
        "下周日",
        "上周五",
        "这周四",
        "下周三下午3点",
    ]
    
    for expr in expressions:
        result = parser.parse(expr)
        if result.success:
            weekday_name = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][result.datetime_obj.weekday()]
            print(f"  '{expr}' → {result.datetime_obj.strftime('%Y-%m-%d')} ({weekday_name})")
    
    print()


def example_monthly_dates():
    """示例4：月度日期解析"""
    print("=" * 60)
    print("示例4：月度日期解析")
    print("=" * 60)
    
    now = datetime(2024, 1, 15, 10, 30, 0)
    parser = NaturalDateParser(now=now)
    
    expressions = [
        "下个月",
        "上个月",
        "下个月15号",
        "月底",
        "下个月月底",
    ]
    
    for expr in expressions:
        result = parser.parse(expr)
        if result.success:
            print(f"  '{expr}' → {result.datetime_obj.strftime('%Y-%m-%d')}")
    
    print()


def example_yearly_dates():
    """示例5：年度日期解析"""
    print("=" * 60)
    print("示例5：年度日期解析")
    print("=" * 60)
    
    now = datetime(2024, 1, 15, 10, 30, 0)
    parser = NaturalDateParser(now=now)
    
    expressions = [
        "明年",
        "今年",
        "去年",
        "明年5月",
        "去年国庆节",
    ]
    
    for expr in expressions:
        result = parser.parse(expr)
        if result.success:
            print(f"  '{expr}' → {result.datetime_obj.strftime('%Y-%m-%d')}")
    
    print()


def example_holiday_dates():
    """示例6：节日日期解析"""
    print("=" * 60)
    print("示例6：节日日期解析")
    print("=" * 60)
    
    now = datetime(2024, 1, 15, 10, 30, 0)
    parser = NaturalDateParser(now=now)
    
    holidays = [
        "元旦",
        "情人节",
        "劳动节",
        "儿童节",
        "国庆节",
        "圣诞节",
        "明年元旦",
    ]
    
    for holiday in holidays:
        result = parser.parse(holiday)
        if result.success:
            print(f"  '{holiday}' → {result.datetime_obj.strftime('%Y-%m-%d')}")
    
    print()


def example_absolute_dates():
    """示例7：绝对日期解析"""
    print("=" * 60)
    print("示例7：绝对日期解析")
    print("=" * 60)
    
    now = datetime(2024, 1, 15, 10, 30, 0)
    parser = NaturalDateParser(now=now)
    
    expressions = [
        "2024年5月20日",
        "5月20日",
        "12月25日",
        "2024年6月1日下午3点",
    ]
    
    for expr in expressions:
        result = parser.parse(expr)
        if result.success:
            print(f"  '{expr}' → {result.datetime_obj.strftime('%Y-%m-%d %H:%M')}")
    
    print()


def example_number_days():
    """示例8：数字天数解析"""
    print("=" * 60)
    print("示例8：数字天数解析")
    print("=" * 60)
    
    now = datetime(2024, 1, 15, 10, 30, 0)
    parser = NaturalDateParser(now=now)
    
    expressions = [
        "3天后",
        "7天前",
        "2周后",
        "1个月后",
        "半年后",
        "1年后",
        "100天后",
    ]
    
    for expr in expressions:
        result = parser.parse(expr)
        if result.success:
            print(f"  '{expr}' → {result.datetime_obj.strftime('%Y-%m-%d')}")
    
    print()


def example_time_periods():
    """示例9：时间段解析"""
    print("=" * 60)
    print("示例9：时间段解析")
    print("=" * 60)
    
    now = datetime(2024, 1, 15, 10, 30, 0)
    parser = NaturalDateParser(now=now)
    
    periods = [
        "凌晨", "早上", "上午", "中午",
        "下午", "傍晚", "晚上", "深夜",
    ]
    
    for period in periods:
        result = parser.parse(f"明天{period}")
        if result.success:
            print(f"  '明天{period}' → {result.datetime_obj.strftime('%H:%M')} ({period}时段)")
    
    print()


def example_date_ranges():
    """示例10：日期范围解析"""
    print("=" * 60)
    print("示例10：日期范围解析")
    print("=" * 60)
    
    now = datetime(2024, 1, 15, 10, 30, 0)  # 周一
    
    ranges = [
        "这周",
        "下周",
        "这个月",
        "下个月",
    ]
    
    for range_text in ranges:
        start, end = parse_range(range_text, now=now)
        if start and end:
            print(f"  '{range_text}':")
            print(f"    开始: {start.strftime('%Y-%m-%d')}")
            print(f"    结束: {end.strftime('%Y-%m-%d')}")
    
    print()


def example_parse_with_info():
    """示例11：获取解析详细信息"""
    print("=" * 60)
    print("示例11：获取解析详细信息")
    print("=" * 60)
    
    now = datetime(2024, 1, 15, 10, 30, 0)
    
    expressions = [
        "明天下午3点",
        "下周三",
        "国庆节",
        "无效表达式",
    ]
    
    for expr in expressions:
        result = parse_with_info(expr, now=now)
        print(f"  '{expr}':")
        print(f"    成功: {result.success}")
        print(f"    类型: {result.date_type.value}")
        print(f"    置信度: {result.confidence}")
        print(f"    包含时间: {result.has_time}")
        if result.datetime_obj:
            print(f"    结果: {result.datetime_obj.strftime('%Y-%m-%d %H:%M')}")
        if result.error_message:
            print(f"    错误: {result.error_message}")
        print()
    
    print()


def example_batch_parse():
    """示例12：批量解析"""
    print("=" * 60)
    print("示例12：批量解析")
    print("=" * 60)
    
    now = datetime(2024, 1, 15, 10, 30, 0)
    
    expressions = [
        "今天", "明天", "后天",
        "下周三", "下个月",
        "国庆节", "圣诞节",
    ]
    
    results = parse_batch(expressions, now=now)
    
    for expr, result in zip(expressions, results):
        if result.success:
            print(f"  '{expr}' → {result.datetime_obj.strftime('%Y-%m-%d')}")
        else:
            print(f"  '{expr}' → 解析失败")
    
    print()


def example_extract_dates():
    """示例13：从文本中提取日期"""
    print("=" * 60)
    print("示例13：从文本中提取日期")
    print("=" * 60)
    
    now = datetime(2024, 1, 15, 10, 30, 0)
    
    text = "今天要开会，明天交报告，后天放假。下周三还有个重要会议。"
    
    dates = extract_dates(text, now=now)
    
    print(f"  文本: '{text}'")
    print("  提取的日期:")
    for expr, dt in dates:
        print(f"    '{expr}' → {dt.strftime('%Y-%m-%d')}")
    
    print()


def example_check_validity():
    """示例14：检查日期表达式有效性"""
    print("=" * 60)
    print("示例14：检查日期表达式有效性")
    print("=" * 60)
    
    now = datetime(2024, 1, 15, 10, 30, 0)
    
    expressions = [
        "明天",
        "下周三",
        "这是一个无效的日期",
        "国庆节",
        "随便说点什么",
    ]
    
    for expr in expressions:
        valid = is_valid(expr, now=now)
        status = "✓ 有效" if valid else "✗ 无效"
        print(f"  '{expr}' → {status}")
    
    print()


def example_get_date_type():
    """示例15：获取日期表达式类型"""
    print("=" * 60)
    print("示例15：获取日期表达式类型")
    print("=" * 60)
    
    now = datetime(2024, 1, 15, 10, 30, 0)
    
    expressions = [
        ("明天", DateType.RELATIVE),
        ("下周三", DateType.WEEKDAY),
        ("下个月", DateType.MONTHLY),
        ("明年", DateType.YEARLY),
        ("国庆节", DateType.ABSOLUTE),
        ("这周", DateType.RANGE),
    ]
    
    for expr, expected_type in expressions:
        actual_type = get_date_type(expr, now=now)
        match = "✓" if actual_type == expected_type else "✗"
        print(f"  '{expr}' → {actual_type.value} {match}")
    
    print()


def example_cross_boundary():
    """示例16：跨边界场景（跨月、跨年）"""
    print("=" * 60)
    print("示例16：跨边界场景")
    print("=" * 60)
    
    # 月底场景
    end_of_month = datetime(2024, 1, 30, 10, 0)
    parser = NaturalDateParser(now=end_of_month)
    
    result = parser.parse("3天后")
    print(f"  1月30日 + 3天 → {result.datetime_obj.strftime('%Y-%m-%d')} (跨月)")
    
    # 年底场景
    end_of_year = datetime(2024, 12, 30, 10, 0)
    parser = NaturalDateParser(now=end_of_year)
    
    result = parser.parse("3天后")
    print(f"  12月30日 + 3天 → {result.datetime_obj.strftime('%Y-%m-%d')} (跨年)")
    
    # 中文数字
    now = datetime(2024, 1, 15, 10, 0)
    parser = NaturalDateParser(now=now)
    
    result = parser.parse("十五天后")
    print(f"  中文 '十五天后' → {result.datetime_obj.strftime('%Y-%m-%d')}")
    
    print()


def example_practical_usage():
    """示例17：实际应用场景"""
    print("=" * 60)
    print("示例17：实际应用场景")
    print("=" * 60)
    
    now = datetime(2024, 1, 15, 10, 30, 0)
    
    # 场景1：日程安排
    print("  场景：日程安排系统")
    schedule_requests = [
        "明天下午2点开会",
        "下周一上午9点汇报",
        "月底提交报告",
        "国庆节放假",
    ]
    
    for request in schedule_requests:
        dt = parse(request, now=now)
        if dt:
            print(f"    '{request}' → {dt.strftime('%Y-%m-%d %H:%M')}")
    
    print()
    
    # 场景2：提醒系统
    print("  场景：提醒系统")
    reminders = [
        "3天后提醒我",
        "一周后检查",
        "下个月第一天备份数据",
    ]
    
    for reminder in reminders:
        dt = parse(reminder, now=now)
        if dt:
            print(f"    '{reminder}' → {dt.strftime('%Y-%m-%d')}")
    
    print()
    
    # 场景3：客服对话
    print("  场景：客服对话解析")
    customer_queries = [
        "我想预约下周三的服务",
        "订单什么时候能到？后天行吗？",
        "元旦有什么活动？",
    ]
    
    for query in customer_queries:
        dates = extract_dates(query, now=now)
        print(f"    '{query}'")
        for expr, dt in dates:
            print(f"      → '{expr}' 对应 {dt.strftime('%Y-%m-%d')}")
    
    print()


def example_chinese_number_conversion():
    """示例18：中文数字转换"""
    print("=" * 60)
    print("示例18：中文数字转换")
    print("=" * 60)
    
    now = datetime(2024, 1, 15, 10, 0)
    parser = NaturalDateParser(now=now)
    
    expressions = [
        "三天后",
        "七天前",
        "两周后",
        "十天后",
        "二十天后",
        "三十天后",
    ]
    
    for expr in expressions:
        result = parser.parse(expr)
        if result.success:
            print(f"  '{expr}' → {result.datetime_obj.strftime('%Y-%m-%d')}")
    
    print()


def run_all_examples():
    """运行所有示例"""
    example_basic_relative_dates()
    example_relative_dates_with_time()
    example_weekday_dates()
    example_monthly_dates()
    example_yearly_dates()
    example_holiday_dates()
    example_absolute_dates()
    example_number_days()
    example_time_periods()
    example_date_ranges()
    example_parse_with_info()
    example_batch_parse()
    example_extract_dates()
    example_check_validity()
    example_get_date_type()
    example_cross_boundary()
    example_practical_usage()
    example_chinese_number_conversion()
    
    print("=" * 60)
    print("所有示例演示完毕！")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()