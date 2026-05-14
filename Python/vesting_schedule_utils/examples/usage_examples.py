"""
Vesting Schedule Utils - 使用示例

展示股权归属计划计算工具的各种使用场景
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date, timedelta
from mod import (
    VestingType,
    VestingFrequency,
    VestingSchedule,
    create_standard_schedule,
    create_backloaded_schedule,
    calculate_vesting_schedule,
    get_vesting_status,
    calculate_accelerated_vesting,
    generate_vesting_calendar,
    estimate_vesting_value,
    calculate_vesting_summary,
    days_until_next_vesting,
    get_vesting_timeline,
    format_vesting_event
)


def example_standard_vesting():
    """示例1：标准硅谷归属计划"""
    print("\n" + "=" * 60)
    print("示例1：标准硅谷归属计划")
    print("=" * 60)
    
    # 创建标准4年归属计划
    # - 10000股期权
    # - 2020年1月1日授予
    # - 1年Cliff（25%）
    # - 剩余75%按月归属36个月
    schedule = create_standard_schedule(
        total_shares=10000,
        grant_date=date(2020, 1, 1),
        vesting_years=4,
        cliff_years=1,
        cliff_percentage=25.0
    )
    
    print(f"\n授予详情：")
    print(f"  总份额: {schedule.total_shares} 股")
    print(f"  授予日期: {schedule.grant_date}")
    print(f"  归属周期: {schedule.vesting_period_months} 个月")
    print(f"  Cliff期: {schedule.cliff_months} 个月")
    print(f"  Cliff比例: {schedule.cliff_percentage}%")
    print(f"  归属频率: {schedule.frequency.value}")
    
    # 获取归属时间线
    print(f"\n归属时间线：")
    timeline = get_vesting_timeline(schedule)
    print(timeline)


def example_check_vesting_status():
    """示例2：检查归属状态"""
    print("\n" + "=" * 60)
    print("示例2：检查归属状态")
    print("=" * 60)
    
    schedule = create_standard_schedule(10000, date(2020, 1, 1))
    
    # 检查不同日期的状态
    check_dates = [
        date(2020, 6, 1),   # Cliff前
        date(2021, 1, 1),   # Cliff日
        date(2022, 1, 1),   # 2年后
        date(2023, 1, 1),   # 3年后
        date(2024, 1, 1),   # 完全归属
        date(2025, 1, 1),   # 完全归属后
    ]
    
    print(f"\n归属状态追踪：")
    for d in check_dates:
        status = get_vesting_status(schedule, d)
        print(f"\n日期: {d}")
        print(f"  已归属: {status.vested_shares} 股 ({status.vested_percentage:.2f}%)")
        print(f"  未归属: {status.unvested_shares} 股")
        print(f"  完全归属: {status.is_fully_vested}")
        if status.next_vesting_date:
            days = days_until_next_vesting(schedule, d)
            print(f"  下次归属: {status.next_vesting_date} ({days}天后)")
            print(f"  下次份额: {status.next_vesting_shares} 股")


def example_quarterly_vesting():
    """示例3：季度归属计划"""
    print("\n" + "=" * 60)
    print("示例3：季度归属计划")
    print("=" * 60)
    
    # 创建季度归属计划
    schedule = VestingSchedule(
        total_shares=10000,
        grant_date=date(2020, 1, 1),
        vesting_type=VestingType.LINEAR,
        vesting_period_months=48,
        cliff_months=12,
        cliff_percentage=25.0,
        frequency=VestingFrequency.QUARTERLY
    )
    
    events = calculate_vesting_schedule(schedule)
    
    print(f"\n季度归属事件：")
    print(f"  总事件数: {len(events)}")
    
    # 显示前几个事件
    print(f"\n归属事件列表：")
    for i, event in enumerate(events[:5]):
        print(f"  {format_vesting_event(event)}")
    
    if len(events) > 5:
        print(f"  ... 还有 {len(events) - 5} 个事件")


def example_backloaded_vesting():
    """示例4：后置归属计划"""
    print("\n" + "=" * 60)
    print("示例4：后置归属计划（逐年递增）")
    print("=" * 60)
    
    # 创建后置归属计划：10%, 20%, 30%, 40%
    schedule = create_backloaded_schedule(
        total_shares=10000,
        grant_date=date(2020, 1, 1)
    )
    
    print(f"\n后置归属详情：")
    print(f"  阶梯计划: {schedule.graded_schedule}")
    
    events = calculate_vesting_schedule(schedule)
    
    print(f"\n阶梯归属事件：")
    for event in events:
        print(f"  {format_vesting_event(event)}")
    
    # 验证总份额
    total = sum(e.shares for e in events)
    print(f"\n  总归属份额: {total} 股")


def example_immediate_vesting():
    """示例5：即时归属"""
    print("\n" + "=" * 60)
    print("示例5：即时归属（顾问/创始人）")
    print("=" * 60)
    
    # 顾问或创始人通常获得即时归属
    schedule = VestingSchedule(
        total_shares=5000,
        grant_date=date(2020, 1, 1),
        vesting_type=VestingType.IMMEDIATE,
        vesting_period_months=0
    )
    
    status = get_vesting_status(schedule)
    
    print(f"\n即时归属：")
    print(f"  授予份额: {schedule.total_shares} 股")
    print(f"  已归属: {status.vested_shares} 股 ({status.vested_percentage:.2f}%)")
    print(f"  完全归属: {status.is_fully_vested}")
    print(f"  归属事件数: {len(status.vesting_events)}")


def example_cliff_only_vesting():
    """示例6：纯Cliff归属"""
    print("\n" + "=" * 60)
    print("示例6：纯Cliff归属")
    print("=" * 60)
    
    # 4年后一次性归属全部
    schedule = VestingSchedule(
        total_shares=10000,
        grant_date=date(2020, 1, 1),
        vesting_type=VestingType.CLIFF,
        vesting_period_months=48,
        cliff_months=48
    )
    
    events = calculate_vesting_schedule(schedule)
    
    print(f"\n纯Cliff归属：")
    print(f"  Cliff期: {schedule.cliff_months} 个月")
    print(f"  归属事件数: {len(events)}")
    
    for event in events:
        print(f"  {format_vesting_event(event)}")
    
    # Cliff前的状态
    status_before = get_vesting_status(schedule, date(2022, 1, 1))
    print(f"\n2022年状态（Cliff前）：")
    print(f"  已归属: {status_before.vested_shares} 股")
    print(f"  完全归属: {status_before.is_fully_vested}")
    
    # Cliff后的状态
    status_after = get_vesting_status(schedule, date(2024, 1, 1))
    print(f"\n2024年状态（Cliff后）：")
    print(f"  已归属: {status_after.vested_shares} 股")
    print(f"  完全归属: {status_after.is_fully_vested}")


def example_vesting_value():
    """示例7：价值估算"""
    print("\n" + "=" * 60)
    print("示例7：归属价值估算")
    print("=" * 60)
    
    schedule = create_standard_schedule(10000, date(2020, 1, 1))
    
    # 假设股价 $10
    price = 10.0
    
    print(f"\n价值估算（股价 $${price}）：")
    
    check_dates = [
        date(2020, 6, 1),
        date(2021, 1, 1),
        date(2022, 1, 1),
        date(2024, 1, 1),
    ]
    
    for d in check_dates:
        value = estimate_vesting_value(schedule, price, d)
        print(f"\n  {d}:")
        print(f"    已归属价值: $${value['vested_value']:,}")
        print(f"    未归属价值: $${value['unvested_value']:,}")
        print(f"    总价值: $${value['total_value']:,}")


def example_accelerated_vesting():
    """示例8：加速归属（离职/收购场景）"""
    print("\n" + "=" * 60)
    print("示例8：加速归属")
    print("=" * 60)
    
    schedule = create_standard_schedule(10000, date(2020, 1, 1))
    
    # 假设2021年6月离职（Cliff后）
    leave_date = date(2021, 6, 1)
    
    print(f"\n离职日期: {leave_date}")
    
    # 离职时的状态
    status = get_vesting_status(schedule, leave_date)
    print(f"\n离职时归属状态：")
    print(f"  已归属: {status.vested_shares} 股 ({status.vested_percentage:.2f}%)")
    print(f"  未归属: {status.unvested_shares} 股")
    
    # 假设50%加速归属
    accel_shares, accel_events = calculate_accelerated_vesting(
        schedule, 50.0, leave_date
    )
    
    print(f"\n50%加速归属：")
    print(f"  加速归属份额: {accel_shares} 股")
    
    for event in accel_events:
        print(f"  {format_vesting_event(event)}")
    
    # 实际获得
    total_received = status.vested_shares + accel_shares
    print(f"\n实际获得总份额: {total_received} 股")
    
    # 100%加速归属（公司收购场景）
    full_accel_shares, _ = calculate_accelerated_vesting(
        schedule, 100.0, leave_date
    )
    print(f"\n如100%加速归属: {status.vested_shares + full_accel_shares} 股（全部）")


def example_vesting_calendar():
    """示例9：归属日历"""
    print("\n" + "=" * 60)
    print("示例9：归属日历")
    print("=" * 60)
    
    schedule = create_standard_schedule(10000, date(2020, 1, 1))
    
    # 生成2021年日历
    calendar_2021 = generate_vesting_calendar(schedule, 2021)
    
    print(f"\n2021年归属日历：")
    for month, events in sorted(calendar_2021.items()):
        month_names = ["一月", "二月", "三月", "四月", "五月", "六月",
                       "七月", "八月", "九月", "十月", "十一月", "十二月"]
        print(f"\n  {month_names[month-1]}:")
        for event in events:
            print(f"    {format_vesting_event(event)}")
    
    # 生成2024年日历（最后归属年）
    calendar_2024 = generate_vesting_calendar(schedule, 2024)
    
    print(f"\n2024年归属日历（最后归属）：")
    for month, events in sorted(calendar_2024.items()):
        month_names = ["一月", "二月", "三月", "四月", "五月", "六月",
                       "七月", "八月", "九月", "十月", "十一月", "十二月"]
        print(f"\n  {month_names[month-1]}:")
        for event in events:
            print(f"    {format_vesting_event(event)}")


def example_summary():
    """示例10：归属摘要"""
    print("\n" + "=" * 60)
    print("示例10：归属摘要")
    print("=" * 60)
    
    schedule = create_standard_schedule(10000, date(2020, 1, 1))
    
    summary = calculate_vesting_summary(schedule, date(2022, 1, 1))
    
    print(f"\n归属摘要（截至 2022-01-01）：")
    for key, value in summary.items():
        if value is not None:
            print(f"  {key}: {value}")


def example_custom_schedule():
    """示例11：自定义归属计划"""
    print("\n" + "=" * 60)
    print("示例11：自定义归属计划")
    print("=" * 60)
    
    # 自定义计划：
    # - 20000股
    # - 6个月Cliff（10%）
    # - 3年归属周期
    # - 按季度归属
    schedule = VestingSchedule(
        total_shares=20000,
        grant_date=date(2023, 1, 1),
        vesting_type=VestingType.LINEAR,
        vesting_period_months=36,
        cliff_months=6,
        cliff_percentage=10.0,
        frequency=VestingFrequency.QUARTERLY
    )
    
    print(f"\n自定义归属计划：")
    print(f"  总份额: {schedule.total_shares} 股")
    print(f"  授予日期: {schedule.grant_date}")
    print(f"  归属周期: {schedule.vesting_period_months} 个月")
    print(f"  Cliff期: {schedule.cliff_months} 个月 ({schedule.cliff_percentage}%)")
    print(f"  归属频率: {schedule.frequency.value}")
    
    events = calculate_vesting_schedule(schedule)
    
    print(f"\n归属事件 ({len(events)} 次)：")
    for event in events[:3]:
        print(f"  {format_vesting_event(event)}")
    print(f"  ...")
    for event in events[-2:]:
        print(f"  {format_vesting_event(event)}")
    
    # 验证总份额
    total = sum(e.shares for e in events)
    print(f"\n  总归属份额: {total} 股")


def run_all_examples():
    """运行所有示例"""
    print("=" * 60)
    print("Vesting Schedule Utils - 使用示例")
    print("=" * 60)
    
    example_standard_vesting()
    example_check_vesting_status()
    example_quarterly_vesting()
    example_backloaded_vesting()
    example_immediate_vesting()
    example_cliff_only_vesting()
    example_vesting_value()
    example_accelerated_vesting()
    example_vesting_calendar()
    example_summary()
    example_custom_schedule()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()