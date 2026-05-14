"""
Cron Utils 使用示例

演示如何使用 cron_utils 进行：
1. 解析 cron 表达式
2. 计算下次运行时间
3. 验证表达式
4. 生成人类可读描述
"""

from datetime import datetime, timedelta
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    CronExpression,
    parse,
    get_next_run,
    get_next_runs,
    validate,
    to_description,
    EVERY_MINUTE,
    EVERY_HOUR,
    EVERY_DAY,
    EVERY_WEEK,
    EVERY_MONTH,
    EVERY_YEAR,
    EVERY_5_MINUTES,
    EVERY_15_MINUTES,
    EVERY_30_MINUTES,
    WEEKDAYS_9AM,
    WEEKDAYS_6PM,
)


def print_separator(title: str):
    """打印分隔线"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def example_basic_parsing():
    """基本解析示例"""
    print_separator("1. 基本 Cron 表达式解析")
    
    expressions = [
        "* * * * *",           # 每分钟
        "0 * * * *",           # 每小时整点
        "0 0 * * *",           # 每天午夜
        "0 9 * * 1-5",         # 工作日早上9点
        "*/15 * * * *",        # 每15分钟
        "0 9,12,18 * * *",     # 每天9点、12点、18点
    ]
    
    for expr in expressions:
        cron = parse(expr)
        print(f"\n表达式: {expr}")
        print(f"  分钟: {sorted(cron.fields['minute'])}")
        print(f"  小时: {sorted(cron.fields['hour'])}")
        print(f"  日: {sorted(cron.fields['day'])}")
        print(f"  月: {sorted(cron.fields['month'])}")
        print(f"  星期: {sorted(cron.fields['weekday'])}")


def example_special_expressions():
    """特殊表达式示例"""
    print_separator("2. 特殊表达式")
    
    specials = [
        "@yearly",
        "@monthly",
        "@weekly",
        "@daily",
        "@hourly",
        "@every_minute",
    ]
    
    for expr in specials:
        cron = parse(expr)
        print(f"\n{expr:15} -> {cron.to_description()}")


def example_next_run():
    """计算下次运行时间示例"""
    print_separator("3. 计算下次运行时间")
    
    expressions = [
        ("每分钟", EVERY_MINUTE),
        ("每5分钟", EVERY_5_MINUTES),
        ("每小时", EVERY_HOUR),
        ("每天午夜", EVERY_DAY),
        ("每周日", EVERY_WEEK),
        ("工作日早上9点", WEEKDAYS_9AM),
    ]
    
    now = datetime.now()
    print(f"\n当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    
    for name, expr in expressions:
        cron = parse(expr)
        next_run = cron.get_next_run(now)
        if next_run:
            delta = next_run - now
            print(f"\n{name} ({expr}):")
            print(f"  下次运行: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  距今: {delta}")


def example_multiple_runs():
    """计算多次运行时间示例"""
    print_separator("4. 计算未来多次运行时间")
    
    # 每3小时的运行时间
    cron = parse("0 */3 * * *")
    now = datetime.now()
    
    print(f"\n表达式: 0 */3 * * * (每3小时)")
    print(f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n接下来5次运行时间:")
    
    runs = cron.get_next_runs(count=5, after=now)
    for i, run in enumerate(runs, 1):
        print(f"  {i}. {run.strftime('%Y-%m-%d %H:%M:%S')} ({run.strftime('%A')})")


def example_validation():
    """验证示例"""
    print_separator("5. 表达式验证")
    
    test_cases = [
        "* * * * *",           # 有效
        "0 9 * * 1-5",         # 有效
        "*/15 0-23 * * *",     # 有效
        "* * * *",             # 无效：字段不足
        "* * * * * * *",       # 无效：字段过多
        "60 * * * *",          # 无效：分钟超出范围
        "0 25 * * *",          # 无效：小时超出范围
        "@invalid",            # 无效：未知特殊表达式
    ]
    
    for expr in test_cases:
        valid, error = validate(expr)
        status = "✓ 有效" if valid else "✗ 无效"
        print(f"\n{expr:20} -> {status}")
        if error:
            print(f"                     错误: {error}")


def example_descriptions():
    """生成描述示例"""
    print_separator("6. 人类可读描述")
    
    expressions = [
        "* * * * *",
        "*/5 * * * *",
        "0 * * * *",
        "0 9 * * *",
        "0 9 * * 1-5",
        "0 0 1 * *",
        "0 0 1 1 *",
        "*/15 9-17 * * 1-5",
    ]
    
    print("\n中文描述:")
    for expr in expressions:
        desc = to_description(expr, lang='zh')
        print(f"  {expr:20} -> {desc}")
    
    print("\n英文描述:")
    for expr in expressions:
        desc = to_description(expr, lang='en')
        print(f"  {expr:20} -> {desc}")


def example_six_field_format():
    """6字段格式示例（带秒）"""
    print_separator("7. 6字段格式（带秒）")
    
    expressions = [
        "0 * * * * *",           # 每分钟整秒
        "*/10 * * * * *",        # 每10秒
        "0 30 * * * *",          # 每分钟的第30秒
        "0 0 0 * * *",           # 每小时整点
    ]
    
    now = datetime.now()
    print(f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    
    for expr in expressions:
        cron = parse(expr)
        print(f"\n表达式: {expr}")
        print(f"  has_seconds: {cron.has_seconds}")
        print(f"  描述: {cron.to_description()}")
        next_run = cron.get_next_run(now)
        if next_run:
            print(f"  下次运行: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")


def example_month_weekday_names():
    """月份和星期名称示例"""
    print_separator("8. 月份和星期名称")
    
    expressions = [
        "0 0 1 JAN *",           # 每年1月1日
        "0 0 1 jan,apr,jul,oct *",  # 每季度首日
        "0 9 * * MON-FRI",       # 工作日早上9点
        "0 9 * * sat,sun",       # 周末早上9点
    ]
    
    for expr in expressions:
        cron = parse(expr)
        print(f"\n表达式: {expr}")
        print(f"  描述: {cron.to_description()}")
        now = datetime.now()
        next_run = cron.get_next_run(now)
        if next_run:
            print(f"  下次运行: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")


def example_practical_scenarios():
    """实际应用场景示例"""
    print_separator("9. 实际应用场景")
    
    scenarios = [
        ("日志清理", "0 2 * * 0"),           # 每周日凌晨2点
        ("数据库备份", "0 3 * * *"),         # 每天凌晨3点
        ("邮件发送", "0 9 * * 1"),           # 每周一早上9点
        ("报告生成", "0 0 1 * *"),           # 每月1号午夜
        ("健康检查", "*/5 * * * *"),         # 每5分钟
        ("缓存刷新", "*/30 * * * *"),        # 每30分钟
        ("月度账单", "0 0 1 1-12 *"),        # 每月1号
        ("季度报告", "0 9 1 1,4,7,10 *"),    # 每季度首日9点
    ]
    
    now = datetime.now()
    print(f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    for name, expr in scenarios:
        cron = parse(expr)
        next_run = cron.get_next_run(now)
        desc = cron.to_description()
        print(f"{name:10} | {expr:20} | {desc:25} | ", end="")
        if next_run:
            print(f"下次: {next_run.strftime('%m/%d %H:%M')}")
        else:
            print("无法计算")


def example_using_constants():
    """使用预定义常量示例"""
    print_separator("10. 使用预定义常量")
    
    constants = [
        ("EVERY_MINUTE", EVERY_MINUTE),
        ("EVERY_HOUR", EVERY_HOUR),
        ("EVERY_DAY", EVERY_DAY),
        ("EVERY_WEEK", EVERY_WEEK),
        ("EVERY_MONTH", EVERY_MONTH),
        ("EVERY_YEAR", EVERY_YEAR),
        ("EVERY_5_MINUTES", EVERY_5_MINUTES),
        ("EVERY_15_MINUTES", EVERY_15_MINUTES),
        ("EVERY_30_MINUTES", EVERY_30_MINUTES),
        ("WEEKDAYS_9AM", WEEKDAYS_9AM),
        ("WEEKDAYS_6PM", WEEKDAYS_6PM),
    ]
    
    for name, value in constants:
        cron = parse(value)
        print(f"{name:20} = \"{value}\"")
        print(f"  描述: {cron.to_description()}")


def main():
    """运行所有示例"""
    print("\n" + "█" * 60)
    print("█" + " " * 58 + "█")
    print("█" + "     Cron Utils - 使用示例演示".center(50) + "█")
    print("█" + " " * 58 + "█")
    print("█" * 60)
    
    example_basic_parsing()
    example_special_expressions()
    example_next_run()
    example_multiple_runs()
    example_validation()
    example_descriptions()
    example_six_field_format()
    example_month_weekday_names()
    example_practical_scenarios()
    example_using_constants()
    
    print_separator("完成")
    print("\n所有示例运行完成！\n")


if __name__ == "__main__":
    main()