"""
Natural Time Parser Utilities - 使用示例

展示自然语言时间解析器的各种用法。

Author: AllToolkit
"""

import sys
import os
from datetime import datetime, timedelta

# Add parent directories to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from natural_time_parser_utils.mod import (
    NaturalTimeParser,
    DurationParser,
    TimeExpressionExtractor,
    RelativeTimeFormatter,
    parse_time,
    parse_duration,
    format_duration,
    extract_times,
    relative_time,
    when,
    how_long,
)


def basic_time_parsing():
    """基础时间解析"""
    print("=" * 60)
    print("基础时间解析示例")
    print("=" * 60)
    
    # 设置参考时间
    reference = datetime(2026, 4, 16, 7, 0, 0)
    parser = NaturalTimeParser(reference)
    
    # 英文相对时间
    print("\n英文相对时间:")
    expressions = [
        "in 5 minutes",
        "in 2 hours",
        "in 3 days",
        "in 1 week",
        "in 2 months",
    ]
    for expr in expressions:
        result = parser.parse(expr)
        print(f"  '{expr}' -> {result.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 中文相对时间
    print("\n中文相对时间:")
    expressions = [
        "5分钟后",
        "2小时后",
        "3天后",
        "一周后",
        "半年后",
        "半小时后",
    ]
    parser = NaturalTimeParser(reference)
    for expr in expressions:
        result = parser.parse(expr)
        print(f"  '{expr}' -> {result.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 绝对时间（英文）
    print("\n英文绝对时间:")
    expressions = [
        "today",
        "tomorrow",
        "yesterday",
        "day after tomorrow",
        "next monday",
        "next friday",
    ]
    for expr in expressions:
        result = parser.parse(expr)
        print(f"  '{expr}' -> {result.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 绝对时间（中文）
    print("\n中文绝对时间:")
    expressions = [
        "今天",
        "明天",
        "后天",
        "下周一",
        "下周三",
        "上周五",
    ]
    for expr in expressions:
        result = parser.parse(expr)
        print(f"  '{expr}' -> {result.strftime('%Y-%m-%d %H:%M:%S')}")


def time_point_parsing():
    """时间点解析"""
    print("\n" + "=" * 60)
    print("时间点解析示例")
    print("=" * 60)
    
    reference = datetime(2026, 4, 16, 7, 0, 0)
    parser = NaturalTimeParser(reference)
    
    # 英文时间点
    print("\n英文时间点:")
    expressions = [
        "at 3pm",
        "at 9am",
        "at 15:30",
        "at 8:45 am",
    ]
    for expr in expressions:
        result = parser.parse(expr)
        print(f"  '{expr}' -> {result.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 中文时间点
    print("\n中文时间点:")
    expressions = [
        "3点",
        "下午3点",
        "8点半",
        "晚上8点",
        "凌晨2点",
        "中午12点",
        "下午3点半",
        "早上8点一刻",
    ]
    for expr in expressions:
        result = parser.parse(expr)
        print(f"  '{expr}' -> {result.strftime('%Y-%m-%d %H:%M:%S')}")


def combined_expression_parsing():
    """组合表达式解析"""
    print("\n" + "=" * 60)
    print("组合表达式解析示例")
    print("=" * 60)
    
    reference = datetime(2026, 4, 16, 7, 0, 0)
    parser = NaturalTimeParser(reference)
    
    print("\n组合表达式:")
    expressions = [
        "tomorrow at 3pm",
        "next monday at 9am",
        "明天下午3点",
        "下周一早上9点",
        "后天晚上8点",
        "后天中午12点半",
    ]
    for expr in expressions:
        result = parser.parse(expr)
        print(f"  '{expr}' -> {result.strftime('%Y-%m-%d %H:%M:%S')}")


def duration_parsing():
    """时长解析"""
    print("\n" + "=" * 60)
    print("时长解析示例")
    print("=" * 60)
    
    # 英文时长
    print("\n英文时长:")
    expressions = [
        "2h 30m",
        "1 hour 30 minutes",
        "90 seconds",
        "1 day",
        "2 weeks",
    ]
    for expr in expressions:
        result = DurationParser.parse(expr)
        formatted = format_duration(result, 'en')
        print(f"  '{expr}' -> {formatted}")
    
    # 中文时长
    print("\n中文时长:")
    expressions = [
        "2小时30分钟",
        "1小时",
        "90秒",
        "1天",
        "2周",
        "半小时",
        "一刻钟",
    ]
    for expr in expressions:
        result = DurationParser.parse(expr)
        formatted = format_duration(result, 'cn')
        print(f"  '{expr}' -> {formatted}")
    
    # 冒号格式
    print("\n冒号格式时长:")
    expressions = [
        "1:30:00",
        "2:30",
        "0:45:30",
    ]
    for expr in expressions:
        result = DurationParser.parse(expr)
        formatted = format_duration(result, 'cn')
        print(f"  '{expr}' -> {formatted}")


def time_expression_extraction():
    """时间表达式提取"""
    print("\n" + "=" * 60)
    print("时间表达式提取示例")
    print("=" * 60)
    
    # 英文文本
    print("\n英文文本提取:")
    text = "Let's meet tomorrow at 3pm for about 2 hours. The deadline is next friday."
    results = extract_times(text)
    print(f"  文本: '{text}'")
    for r in results:
        parsed_str = r['parsed'].strftime('%Y-%m-%d %H:%M:%S') if r['parsed'] else '无法解析'
        print(f"  找到: '{r['match']}' -> {parsed_str}")
    
    # 中文文本
    print("\n中文文本提取:")
    text = "明天下午3点开会，预计持续2小时。下周一早上9点有另一个会议。"
    results = extract_times(text)
    print(f"  文本: '{text}'")
    for r in results:
        parsed_str = r['parsed'].strftime('%Y-%m-%d %H:%M:%S') if r['parsed'] else '无法解析'
        print(f"  找到: '{r['match']}' -> {parsed_str}")


def relative_time_formatting():
    """相对时间格式化"""
    print("\n" + "=" * 60)
    print("相对时间格式化示例")
    print("=" * 60)
    
    now = datetime(2026, 4, 16, 7, 0, 0)
    
    print("\n过去时间（中文）:")
    times = [
        now - timedelta(seconds=5),
        now - timedelta(minutes=30),
        now - timedelta(hours=3),
        now - timedelta(days=1),
        now - timedelta(days=5),
        now - timedelta(weeks=2),
        now - timedelta(days=60),
        now - timedelta(days=400),
    ]
    for t in times:
        result = relative_time(t, now, 'cn')
        print(f"  {t.strftime('%Y-%m-%d %H:%M:%S')} -> '{result}'")
    
    print("\n未来时间（中文）:")
    times = [
        now + timedelta(minutes=30),
        now + timedelta(hours=3),
        now + timedelta(days=1),
        now + timedelta(days=5),
        now + timedelta(weeks=2),
    ]
    for t in times:
        result = relative_time(t, now, 'cn')
        print(f"  {t.strftime('%Y-%m-%d %H:%M:%S')} -> '{result}'")
    
    print("\n英文格式:")
    times = [
        now - timedelta(minutes=30),
        now + timedelta(hours=3),
        now - timedelta(days=1),
        now + timedelta(days=5),
    ]
    for t in times:
        result = relative_time(t, now, 'en')
        print(f"  {t.strftime('%Y-%m-%d %H:%M:%S')} -> '{result}'")


def convenience_functions():
    """便捷函数示例"""
    print("\n" + "=" * 60)
    print("便捷函数示例")
    print("=" * 60)
    
    reference = datetime(2026, 4, 16, 7, 0, 0)
    
    # when() 函数
    print("\nwhen() 函数:")
    expressions = ["明天", "下周一", "2小时后", "明天下午3点"]
    for expr in expressions:
        result = when(expr, reference)
        print(f"  when('{expr}') -> {result.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # how_long() 函数
    print("\nhow_long() 函数:")
    expressions = ["2小时", "1小时30分钟", "半小时", "90秒"]
    for expr in expressions:
        result = how_long(expr)
        print(f"  how_long('{expr}') -> {format_duration(result, 'cn')}")


def practical_use_cases():
    """实际应用场景"""
    print("\n" + "=" * 60)
    print("实际应用场景示例")
    print("=" * 60)
    
    # 场景1: 会议安排
    print("\n场景1: 会议安排")
    now = datetime(2026, 4, 16, 7, 0, 0)
    meeting_time = parse_time("明天下午3点", now)
    duration = parse_duration("2小时")
    end_time = meeting_time + duration
    print(f"  会议开始: {meeting_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  会议时长: {format_duration(duration, 'cn')}")
    print(f"  会议结束: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 场景2: 提醒设置
    print("\n场景2: 提醒设置")
    reminder_time = parse_time("下周一早上9点", now)
    time_until = reminder_time - now
    print(f"  提醒时间: {reminder_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  距现在还有: {format_duration(time_until, 'cn')}")
    
    # 场景3: 从消息中提取时间
    print("\n场景3: 从消息中提取时间")
    message = "我们明天下午3点见面吧，大概聊2小时"
    results = extract_times(message)
    print(f"  消息: '{message}'")
    for r in results:
        if r['parsed']:
            print(f"  提取到: '{r['match']}' -> {r['parsed'].strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 场景4: 用户友好的时间显示
    print("\n场景4: 用户友好的时间显示")
    post_time = datetime(2026, 4, 15, 15, 30, 0)  # 昨天下午
    display = relative_time(post_time, now, 'cn')
    print(f"  原始时间: {post_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  显示为: '{display}'")


def main():
    """运行所有示例"""
    basic_time_parsing()
    time_point_parsing()
    combined_expression_parsing()
    duration_parsing()
    time_expression_extraction()
    relative_time_formatting()
    convenience_functions()
    practical_use_cases()
    
    print("\n" + "=" * 60)
    print("所有示例完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()