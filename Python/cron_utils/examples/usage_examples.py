"""
Cron Utilities 使用示例

演示 Cron 表达式解析、验证、计算和调度功能。
"""

from datetime import datetime, timedelta
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    CronExpression,
    CronValidator,
    CronCalculator,
    CronScheduler,
    parse,
    validate,
    is_valid,
    next_run,
    next_runs,
    describe,
)


def print_separator(title: str) -> None:
    """打印分隔线"""
    print(f"\n{'=' * 60}")
    print(f" {title}")
    print('=' * 60)


def example_basic_parsing():
    """基础解析示例"""
    print_separator("基础解析")
    
    expressions = [
        "* * * * *",          # 每分钟
        "0 * * * *",          # 每小时整点
        "0 0 * * *",          # 每天午夜
        "0 9 * * 1-5",        # 工作日早上9点
        "0 0 1 * *",          # 每月1号
        "*/15 * * * *",       # 每15分钟
        "0 9,12,18 * * *",    # 每天9点、12点、18点
        "0 0 0 1 1 *",        # 每年1月1日（6字段）
    ]
    
    for expr in expressions:
        try:
            cron = CronExpression(expr)
            print(f"\n表达式: {expr}")
            print(f"  描述: {cron.get_description()}")
            print(f"  字段数: {len(cron.field_values)}")
            print(f"  含秒字段: {cron.has_seconds}")
        except Exception as e:
            print(f"\n表达式: {expr}")
            print(f"  错误: {e}")


def example_special_expressions():
    """特殊表达式示例"""
    print_separator("特殊表达式")
    
    special = [
        "@yearly",
        "@annually",
        "@monthly",
        "@weekly",
        "@daily",
        "@midnight",
        "@hourly",
        "@every_minute",
    ]
    
    for expr in special:
        cron = CronExpression(expr)
        print(f"\n{expr:15} -> {cron.normalized_expression}")
        print(f"  描述: {cron.get_description()}")


def example_field_formats():
    """字段格式示例"""
    print_separator("字段格式")
    
    formats = [
        ("*", "任意值"),
        ("*/5", "每 5 个单位"),
        ("0-30", "范围 0 到 30"),
        ("0,15,30,45", "列表值"),
        ("0-30/5", "范围内每 5 个单位"),
        ("jan", "月份名称"),
        ("mon-fri", "星期范围"),
        ("jan,apr,jul,oct", "月份列表"),
    ]
    
    print("\n字段格式说明：")
    for fmt, desc in formats:
        print(f"  {fmt:20} -> {desc}")
    
    # 示例表达式
    print("\n组合示例：")
    examples = [
        ("0 */2 * * *", "每 2 小时整点"),
        ("30 9 * * mon-fri", "工作日 9:30"),
        ("0 0 1 jan-apr *", "1-4月每月1号午夜"),
    ]
    
    for expr, desc in examples:
        cron = CronExpression(expr)
        print(f"  {expr:20} -> {cron.get_description()}")


def example_validation():
    """验证示例"""
    print_separator("验证")
    
    valid_expressions = [
        "* * * * *",
        "0 9 * * 1-5",
        "*/15 * * * *",
        "0 0 0 1 1 *",
    ]
    
    invalid_expressions = [
        "* * * *",           # 字段不足
        "* * * * * * * *",   # 字段过多
        "60 * * * *",        # 分钟超出范围
        "* 24 * * *",        # 小时超出范围
        "* * 32 * *",        # 日期超出范围
    ]
    
    print("\n有效表达式：")
    for expr in valid_expressions:
        is_valid, error = validate(expr)
        status = "✓ 有效" if is_valid else "✗ 无效"
        print(f"  {expr:20} {status}")
    
    print("\n无效表达式：")
    for expr in invalid_expressions:
        is_valid, error = validate(expr)
        status = "✓ 有效" if is_valid else "✗ 无效"
        print(f"  {expr:20} {status}")
        if error:
            print(f"  {'':20} 错误: {error}")


def example_next_run():
    """下次执行时间计算示例"""
    print_separator("下次执行时间")
    
    expressions = [
        ("* * * * *", "每分钟"),
        ("0 * * * *", "每小时整点"),
        ("0 9 * * *", "每天 9 点"),
        ("0 9 * * 1-5", "工作日 9 点"),
        ("0 0 1 * *", "每月 1 号"),
        ("*/15 * * * *", "每 15 分钟"),
    ]
    
    from_time = datetime(2024, 1, 15, 10, 30, 45)
    print(f"\n起始时间: {from_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'星期':10} {from_time.strftime('%A')}")
    
    print("\n")
    for expr, desc in expressions:
        cron = CronExpression(expr)
        next_time = cron.get_next_run(from_time)
        
        print(f"{desc:15} ({expr})")
        print(f"  下次执行: {next_time.strftime('%Y-%m-%d %H:%M:%S %A') if next_time else '无'}")
        
        # 计算时间差
        if next_time:
            delta = next_time - from_time
            print(f"  距离现在: {delta}")


def example_next_runs():
    """多次执行时间示例"""
    print_separator("多次执行时间")
    
    expressions = [
        ("0 * * * *", "每小时"),
        ("0 9 * * 1-5", "工作日 9 点"),
        ("0 0 1 * *", "每月 1 号"),
    ]
    
    from_time = datetime(2024, 1, 15, 10, 0, 0)
    print(f"\n起始时间: {from_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    for expr, desc in expressions:
        cron = CronExpression(expr)
        runs = cron.get_next_runs(5, from_time)
        
        print(f"\n{desc} ({expr}):")
        for i, run in enumerate(runs, 1):
            weekday = run.strftime('%A')
            print(f"  {i}. {run.strftime('%Y-%m-%d %H:%M:%S')} {weekday}")


def example_scheduler():
    """调度器示例"""
    print_separator("调度器")
    
    scheduler = CronScheduler()
    
    # 添加任务
    scheduler.add_job("hourly_report", "0 * * * *")
    scheduler.add_job("daily_backup", "0 2 * * *")
    scheduler.add_job("weekly_cleanup", "0 3 * * 0")
    scheduler.add_job("monthly_billing", "0 0 1 * *")
    
    print("\n已添加任务：")
    for job in scheduler.get_jobs():
        print(f"  - {job}")
    
    # 获取到期任务
    test_times = [
        datetime(2024, 1, 15, 10, 0, 0),  # 整点
        datetime(2024, 1, 15, 10, 30, 0),  # 非整点
        datetime(2024, 1, 1, 0, 0, 0),     # 月初
        datetime(2024, 1, 21, 3, 0, 0),    # 周日凌晨 3 点
    ]
    
    print("\n到期检查：")
    for test_time in test_times:
        due = scheduler.get_due_jobs(test_time)
        print(f"  {test_time.strftime('%Y-%m-%d %H:%M:%S %A')}")
        if due:
            print(f"    到期任务: {', '.join(due)}")
        else:
            print(f"    到期任务: 无")
    
    # 获取未来 24 小时调度表
    from_time = datetime(2024, 1, 15, 10, 0, 0)
    schedule = scheduler.get_schedule(hours=24, from_time=from_time)
    
    print(f"\n未来 24 小时调度表（从 {from_time.strftime('%Y-%m-%d %H:%M')}）：")
    for job, runs in schedule.items():
        print(f"\n  {job}:")
        for run in runs[:5]:  # 只显示前 5 次
            print(f"    - {run.strftime('%Y-%m-%d %H:%M:%S')}")


def example_time_until():
    """时间距离计算示例"""
    print_separator("距离下次执行时间")
    
    expressions = [
        ("0 * * * *", "每小时"),
        ("0 9 * * *", "每天 9 点"),
        ("0 9 * * 1-5", "工作日 9 点"),
    ]
    
    test_times = [
        datetime(2024, 1, 15, 8, 30, 0),
        datetime(2024, 1, 15, 10, 0, 0),
        datetime(2024, 1, 15, 23, 30, 0),
        datetime(2024, 1, 20, 8, 30, 0),  # 周六
    ]
    
    for test_time in test_times:
        weekday = test_time.strftime('%A')
        print(f"\n{test_time.strftime('%Y-%m-%d %H:%M:%S')} {weekday}")
        
        for expr, desc in expressions:
            delta = CronCalculator.time_until_next(expr, test_time)
            if delta:
                print(f"  {desc:15}: {delta}")


def example_description():
    """描述生成示例"""
    print_separator("人类可读描述")
    
    expressions = [
        "* * * * *",
        "0 * * * *",
        "0 0 * * *",
        "0 9 * * 1-5",
        "*/15 * * * *",
        "0 9,12,18 * * *",
        "0 0 1 * *",
        "0 0 1 1 *",
        "30 14 * * mon,fri",
        "0 0 29 2 *",  # 闰年相关
    ]
    
    print("\n")
    for expr in expressions:
        desc = describe(expr)
        print(f"  {expr:20} -> {desc}")


def example_real_world():
    """实际应用示例"""
    print_separator("实际应用场景")
    
    # 场景：备份调度
    print("\n【场景：系统备份】")
    
    backup_jobs = {
        "database_backup": "0 2 * * *",     # 每天凌晨 2 点
        "log_rotation": "0 0 * * 0",        # 每周日午夜
        "monthly_archive": "0 0 1 * *",     # 每月 1 号
    }
    
    print("\n备份任务：")
    for name, expr in backup_jobs.items():
        cron = CronExpression(expr)
        next_run = cron.get_next_run()
        print(f"  {name:20}: {expr} -> 下次: {next_run.strftime('%Y-%m-%d %H:%M') if next_run else 'N/A'}")
    
    # 场景：定时提醒
    print("\n【场景：工作提醒】")
    
    reminders = [
        ("晨会提醒", "0 9 * * 1-5"),
        ("午休提醒", "0 12 * * 1-5"),
        ("下班提醒", "0 18 * * 1-5"),
    ]
    
    print("\n工作提醒：")
    for name, expr in reminders:
        desc = describe(expr)
        print(f"  {name:10}: {desc}")
    
    # 场景：监控检查
    print("\n【场景：系统监控】")
    
    monitors = {
        "health_check": "*/5 * * * *",      # 每 5 分钟
        "disk_check": "0 */6 * * *",        # 每 6 小时
        "security_scan": "0 3 * * 0",       # 每周日凌晨 3 点
    }
    
    print("\n监控任务：")
    for name, expr in monitors.items():
        cron = CronExpression(expr)
        runs = cron.get_next_runs(3)
        print(f"  {name:15}: {expr}")
        for i, run in enumerate(runs, 1):
            print(f"    第{i}次: {run.strftime('%Y-%m-%d %H:%M:%S')}")


def example_quartz_format():
    """Quartz 格式示例"""
    print_separator("Quartz 格式（7 字段）")
    
    expressions = [
        "0 0 0 1 1 * 2024",      # 2024 年 1 月 1 日
        "0 0 0 1 1 * 2024-2025", # 2024-2025 年 1 月 1 日
        "0 30 10 * * * 2024",    # 2024 年每天 10:30
    ]
    
    print("\nQuartz 格式：秒 分 时 日 月 周 年")
    for expr in expressions:
        try:
            cron = CronExpression(expr)
            print(f"\n  {expr}")
            print(f"  含秒字段: {cron.has_seconds}")
            print(f"  含年字段: {cron.has_year}")
            print(f"  描述: {cron.get_description()}")
        except Exception as e:
            print(f"\n  {expr}")
            print(f"  错误: {e}")


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print(" Cron Utilities 使用示例")
    print("=" * 60)
    
    example_basic_parsing()
    example_special_expressions()
    example_field_formats()
    example_validation()
    example_next_run()
    example_next_runs()
    example_scheduler()
    example_time_until()
    example_description()
    example_real_world()
    example_quartz_format()
    
    print("\n" + "=" * 60)
    print(" 示例完成")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()