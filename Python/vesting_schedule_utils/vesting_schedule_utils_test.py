"""
Vesting Schedule Utilities Test Suite

测试股权归属计划计算工具的所有功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import date, timedelta
from mod import (
    VestingType,
    VestingFrequency,
    VestingSchedule,
    VestingEvent,
    VestingStatus,
    calculate_vesting_schedule,
    get_vesting_status,
    add_months,
    months_between,
    calculate_accelerated_vesting,
    generate_vesting_calendar,
    estimate_vesting_value,
    create_standard_schedule,
    create_backloaded_schedule,
    calculate_vesting_summary,
    days_until_next_vesting,
    format_vesting_event,
    get_vesting_timeline
)

test_results = []


def test_result(name, passed, message=""):
    """记录测试结果"""
    status = "✅ PASS" if passed else "❌ FAIL"
    test_results.append({
        "name": name,
        "passed": passed,
        "message": message
    })
    print(f"{status}: {name}")
    if message:
        print(f"   {message}")


# ============================================================
# 基础工具函数测试
# ============================================================

def test_add_months():
    """测试日期加月份"""
    # 正常月份增加
    d1 = date(2020, 1, 15)
    d2 = add_months(d1, 1)
    test_result("add_months - 正常增加", d2 == date(2020, 2, 15))
    
    # 跨年增加
    d3 = add_months(d1, 12)
    test_result("add_months - 跨年增加", d3 == date(2021, 1, 15))
    
    # 多年增加
    d4 = add_months(d1, 24)
    test_result("add_months - 两年增加", d4 == date(2022, 1, 15))
    
    # 月末处理（1月31日 -> 2月28/29日）
    d5 = date(2020, 1, 31)  # 闰年
    d6 = add_months(d5, 1)
    test_result("add_months - 闰年二月末", d6 == date(2020, 2, 29))
    
    d7 = date(2021, 1, 31)  # 非闰年
    d8 = add_months(d7, 1)
    test_result("add_months - 非闰年二月末", d8 == date(2021, 2, 28))
    
    # 零月份
    d9 = add_months(d1, 0)
    test_result("add_months - 零月份", d9 == d1)
    
    # 大月份增加
    d10 = add_months(d1, 50)
    test_result("add_months - 大月份增加", d10 == date(2024, 3, 15))


def test_months_between():
    """测试月数计算"""
    # 相同日期
    d1 = date(2020, 1, 15)
    test_result("months_between - 相同日期", months_between(d1, d1) == 0)
    
    # 一个月
    d2 = date(2020, 2, 15)
    test_result("months_between - 一个月", months_between(d1, d2) == 1)
    
    # 跨年
    d3 = date(2021, 1, 15)
    test_result("months_between - 跨年", months_between(d1, d3) == 12)
    
    # 日小于起始日
    d4 = date(2020, 2, 10)
    test_result("months_between - 日小于起始日", months_between(d1, d4) == 0)
    
    # 结束日期在开始前
    test_result("months_between - 结束在前", months_between(d2, d1) == 0)


# ============================================================
# 归属计划创建测试
# ============================================================

def test_vesting_schedule_creation():
    """测试归属计划创建"""
    # 正常创建
    schedule = VestingSchedule(
        total_shares=10000,
        grant_date=date(2020, 1, 1),
        vesting_type=VestingType.LINEAR,
        vesting_period_months=48,
        cliff_months=12,
        cliff_percentage=25.0
    )
    test_result("VestingSchedule - 正常创建", 
                schedule.total_shares == 10000 and schedule.vesting_period_months == 48)
    
    # 错误：零份额
    try:
        bad_schedule = VestingSchedule(
            total_shares=0,
            grant_date=date(2020, 1, 1),
            vesting_type=VestingType.LINEAR,
            vesting_period_months=48
        )
        test_result("VestingSchedule - 零份额验证", False, "应该抛出异常")
    except ValueError:
        test_result("VestingSchedule - 零份额验证", True)
    
    # 错误：零周期
    try:
        bad_schedule = VestingSchedule(
            total_shares=10000,
            grant_date=date(2020, 1, 1),
            vesting_type=VestingType.LINEAR,
            vesting_period_months=0
        )
        test_result("VestingSchedule - 零周期验证", False, "应该抛出异常")
    except ValueError:
        test_result("VestingSchedule - 零周期验证", True)
    
    # 错误：Cliff大于周期
    try:
        bad_schedule = VestingSchedule(
            total_shares=10000,
            grant_date=date(2020, 1, 1),
            vesting_type=VestingType.LINEAR,
            vesting_period_months=12,
            cliff_months=24
        )
        test_result("VestingSchedule - Cliff大于周期验证", False, "应该抛出异常")
    except ValueError:
        test_result("VestingSchedule - Cliff大于周期验证", True)


def test_create_standard_schedule():
    """测试标准归属计划创建"""
    schedule = create_standard_schedule(
        total_shares=10000,
        grant_date=date(2020, 1, 1),
        vesting_years=4,
        cliff_years=1,
        cliff_percentage=25.0
    )
    
    test_result("create_standard_schedule - 份额", schedule.total_shares == 10000)
    test_result("create_standard_schedule - 周期", schedule.vesting_period_months == 48)
    test_result("create_standard_schedule - Cliff月", schedule.cliff_months == 12)
    test_result("create_standard_schedule - Cliff比例", schedule.cliff_percentage == 25.0)
    test_result("create_standard_schedule - 类型", schedule.vesting_type == VestingType.LINEAR)


def test_create_backloaded_schedule():
    """测试后置归属计划创建"""
    schedule = create_backloaded_schedule(
        total_shares=10000,
        grant_date=date(2020, 1, 1)
    )
    
    test_result("create_backloaded_schedule - 份额", schedule.total_shares == 10000)
    test_result("create_backloaded_schedule - 类型", schedule.vesting_type == VestingType.GRADED)
    test_result("create_backloaded_schedule - 阶梯计划", 
                schedule.graded_schedule == [(1, 10), (2, 20), (3, 30), (4, 40)])
    
    # 自定义阶梯计划
    custom_schedule = create_backloaded_schedule(
        total_shares=10000,
        grant_date=date(2020, 1, 1),
        schedule=[(1, 15), (2, 25), (3, 35), (4, 25)]
    )
    test_result("create_backloaded_schedule - 自定义阶梯", 
                custom_schedule.graded_schedule == [(1, 15), (2, 25), (3, 35), (4, 25)])


# ============================================================
# 归属计算测试
# ============================================================

def test_immediate_vesting():
    """测试即时归属"""
    schedule = VestingSchedule(
        total_shares=10000,
        grant_date=date(2020, 1, 1),
        vesting_type=VestingType.IMMEDIATE,
        vesting_period_months=0
    )
    
    events = calculate_vesting_schedule(schedule)
    test_result("immediate_vesting - 事件数量", len(events) == 1)
    test_result("immediate_vesting - 归属份额", events[0].shares == 10000)
    test_result("immediate_vesting - 归属比例", events[0].percentage == 100.0)
    test_result("immediate_vesting - 归属日期", events[0].date == date(2020, 1, 1))


def test_cliff_vesting():
    """测试一次性Cliff归属"""
    schedule = VestingSchedule(
        total_shares=10000,
        grant_date=date(2020, 1, 1),
        vesting_type=VestingType.CLIFF,
        vesting_period_months=48,
        cliff_months=48
    )
    
    events = calculate_vesting_schedule(schedule)
    test_result("cliff_vesting - 事件数量", len(events) == 1)
    test_result("cliff_vesting - 归属日期", events[0].date == date(2024, 1, 1))
    test_result("cliff_vesting - 归属份额", events[0].shares == 10000)
    test_result("cliff_vesting - Cliff标记", events[0].is_cliff == True)


def test_linear_vesting_with_cliff():
    """测试带Cliff的线性归属"""
    schedule = VestingSchedule(
        total_shares=10000,
        grant_date=date(2020, 1, 1),
        vesting_type=VestingType.LINEAR,
        vesting_period_months=48,
        cliff_months=12,
        cliff_percentage=25.0,
        frequency=VestingFrequency.MONTHLY
    )
    
    events = calculate_vesting_schedule(schedule)
    
    # Cliff事件
    cliff_event = events[0]
    test_result("linear_vesting_cliff - Cliff日期", cliff_event.date == date(2021, 1, 1))
    test_result("linear_vesting_cliff - Cliff份额", cliff_event.shares == 2500)
    test_result("linear_vesting_cliff - Cliff比例", cliff_event.percentage == 25.0)
    test_result("linear_vesting_cliff - Cliff标记", cliff_event.is_cliff == True)
    
    # Cliff后应该有36次月归属
    test_result("linear_vesting_cliff - 总事件数", len(events) == 37)
    
    # 最后一次归属应处理余数
    last_event = events[-1]
    total_vested = sum(e.shares for e in events)
    test_result("linear_vesting_cliff - 总归属份额", total_vested == 10000)


def test_linear_vesting_quarterly():
    """测试季度归属"""
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
    
    # Cliff + 12个季度归属
    test_result("quarterly_vesting - 总事件数", len(events) == 13)
    
    # 每季度归属份额（75% / 12 = 6.25%）
    post_cliff_events = events[1:]
    expected_per_quarter = 7500 / 12
    test_result("quarterly_vesting - 每季度份额", 
                post_cliff_events[0].shares == int(expected_per_quarter))


def test_linear_vesting_annually():
    """测试年度归属"""
    schedule = VestingSchedule(
        total_shares=10000,
        grant_date=date(2020, 1, 1),
        vesting_type=VestingType.LINEAR,
        vesting_period_months=48,
        cliff_months=0,
        cliff_percentage=0,
        frequency=VestingFrequency.ANNUALLY
    )
    
    events = calculate_vesting_schedule(schedule)
    
    # 4次年度归属（从授予后12个月开始）
    test_result("annual_vesting - 总事件数", len(events) == 4)
    
    # 每年归属25%
    test_result("annual_vesting - 每年份额", events[0].shares == 2500)
    
    # 验证归属日期（第一次归属在授予后12个月）
    test_result("annual_vesting - 第1年日期", events[0].date == date(2021, 1, 1))
    test_result("annual_vesting - 第2年日期", events[1].date == date(2022, 1, 1))
    test_result("annual_vesting - 第3年日期", events[2].date == date(2023, 1, 1))
    test_result("annual_vesting - 第4年日期", events[3].date == date(2024, 1, 1))


def test_graded_vesting():
    """测试阶梯归属"""
    schedule = VestingSchedule(
        total_shares=10000,
        grant_date=date(2020, 1, 1),
        vesting_type=VestingType.GRADED,
        vesting_period_months=48,
        graded_schedule=[(1, 10), (2, 20), (3, 30), (4, 40)]
    )
    
    events = calculate_vesting_schedule(schedule)
    
    test_result("graded_vesting - 总事件数", len(events) == 4)
    
    # 验证每年份额
    test_result("graded_vesting - 第1年", events[0].shares == 1000)
    test_result("graded_vesting - 第2年", events[1].shares == 2000)
    test_result("graded_vesting - 第3年", events[2].shares == 3000)
    test_result("graded_vesting - 第4年", events[3].shares == 4000)
    
    # 验证总份额
    total = sum(e.shares for e in events)
    test_result("graded_vesting - 总份额", total == 10000)


def test_graded_vesting_default():
    """测试默认阶梯归属（25/25/25/25）"""
    schedule = VestingSchedule(
        total_shares=10000,
        grant_date=date(2020, 1, 1),
        vesting_type=VestingType.GRADED,
        vesting_period_months=48
    )
    
    events = calculate_vesting_schedule(schedule)
    
    test_result("graded_vesting_default - 总事件数", len(events) == 4)
    
    # 默认阶梯：25% / 年
    test_result("graded_vesting_default - 每年份额", events[0].shares == 2500)


# ============================================================
# 归属状态测试
# ============================================================

def test_vesting_status_before_cliff():
    """测试Cliff前的归属状态"""
    schedule = create_standard_schedule(10000, date(2020, 1, 1))
    
    status = get_vesting_status(schedule, date(2020, 6, 1))
    
    test_result("status_before_cliff - 已归属份额", status.vested_shares == 0)
    test_result("status_before_cliff - 未归属份额", status.unvested_shares == 10000)
    test_result("status_before_cliff - 已归属比例", status.vested_percentage == 0.0)
    test_result("status_before_cliff - 完全归属", status.is_fully_vested == False)
    test_result("status_before_cliff - 下次归属日期", status.next_vesting_date == date(2021, 1, 1))


def test_vesting_status_after_cliff():
    """测试Cliff后的归属状态"""
    schedule = create_standard_schedule(10000, date(2020, 1, 1))
    
    # 2021年1月1日刚好是Cliff日，也是第一个月归属日
    status = get_vesting_status(schedule, date(2021, 1, 1))
    
    test_result("status_after_cliff - 已归属份额(Clash日)", status.vested_shares == 2500)
    test_result("status_after_cliff - 未归属份额(Clash日)", status.unvested_shares == 7500)
    test_result("status_after_cliff - 已归属比例(Clash日)", status.vested_percentage == 25.0)
    test_result("status_after_cliff - 完全归属", status.is_fully_vested == False)
    
    # 2021年2月1日已经有Cliff + 1个月归属
    status_feb = get_vesting_status(schedule, date(2021, 2, 1))
    test_result("status_after_cliff - 2月已归属份额", status_feb.vested_shares == 2708)
    test_result("status_after_cliff - 2月未归属份额", status_feb.unvested_shares == 7292)
    test_result("status_after_cliff - 2月已归属比例", status_feb.vested_percentage == 27.08)


def test_vesting_status_mid_vesting():
    """测试中间归属状态"""
    schedule = create_standard_schedule(10000, date(2020, 1, 1))
    
    # 2年后（Cliff + 12个月）
    status = get_vesting_status(schedule, date(2022, 1, 15))
    
    # Cliff 25% + 12个月 6.25% * 12 = 75%
    # 总计约 2500 + 625*12 = 10000
    expected_vested = 2500 + 625 * 12  # 实际需要精确计算
    
    test_result("status_mid_vesting - 已归属份额>0", status.vested_shares > 2500)
    test_result("status_mid_vesting - 未归属份额>0", status.unvested_shares > 0)


def test_vesting_status_fully_vested():
    """测试完全归属状态"""
    schedule = create_standard_schedule(10000, date(2020, 1, 1))
    
    status = get_vesting_status(schedule, date(2025, 1, 1))
    
    test_result("status_fully_vested - 已归属份额", status.vested_shares == 10000)
    test_result("status_fully_vested - 未归属份额", status.unvested_shares == 0)
    test_result("status_fully_vested - 已归属比例", status.vested_percentage == 100.0)
    test_result("status_fully_vested - 完全归属标记", status.is_fully_vested == True)
    test_result("status_fully_vested - 下次归属", status.next_vesting_date is None)


def test_vesting_status_on_vesting_date():
    """测试在归属日期的状态"""
    schedule = create_standard_schedule(10000, date(2020, 1, 1))
    
    # Cliff日
    status = get_vesting_status(schedule, date(2021, 1, 1))
    test_result("status_on_cliff - 已归属份额", status.vested_shares == 2500)


# ============================================================
# 加速归属测试
# ============================================================

def test_accelerated_vesting():
    """测试加速归属"""
    schedule = create_standard_schedule(10000, date(2020, 1, 1))
    
    # 1年后（Cliff刚过）
    shares, events = calculate_accelerated_vesting(
        schedule, 
        acceleration_percentage=50.0,
        as_of_date=date(2021, 1, 1)
    )
    
    # 7500未归属 * 50% = 3750
    test_result("accelerated_vesting - 加速份额", shares == 3750)
    test_result("accelerated_vesting - 加速事件数", len(events) == 1)


def test_accelerated_vesting_full():
    """测试100%加速归属"""
    schedule = create_standard_schedule(10000, date(2020, 1, 1))
    
    shares, events = calculate_accelerated_vesting(
        schedule, 
        acceleration_percentage=100.0,
        as_of_date=date(2021, 1, 1)
    )
    
    test_result("accelerated_vesting_full - 加速份额", shares == 7500)
    
    # 完全归属后
    status = get_vesting_status(schedule, date(2021, 1, 1))
    # 注意：加速归属不会改变实际状态，只是返回可加速的份额


def test_accelerated_vesting_zero():
    """测试零加速"""
    schedule = create_standard_schedule(10000, date(2020, 1, 1))
    
    shares, events = calculate_accelerated_vesting(
        schedule, 
        acceleration_percentage=0.0,
        as_of_date=date(2021, 1, 1)
    )
    
    test_result("accelerated_vesting_zero - 加速份额", shares == 0)
    test_result("accelerated_vesting_zero - 加速事件数", len(events) == 0)


# ============================================================
# 归属日历测试
# ============================================================

def test_vesting_calendar():
    """测试归属日历"""
    schedule = create_standard_schedule(10000, date(2020, 1, 1))
    
    # 2021年的归属事件
    calendar_2021 = generate_vesting_calendar(schedule, 2021)
    
    # 2021年1月有Cliff
    test_result("vesting_calendar - 2021年1月有事件", 1 in calendar_2021)
    test_result("vesting_calendar - Cliff事件", 
                calendar_2021[1][0].is_cliff == True)
    
    # 2024年最后归属
    calendar_2024 = generate_vesting_calendar(schedule, 2024)
    test_result("vesting_calendar - 2024年有事件", 1 in calendar_2024)


def test_vesting_calendar_empty_year():
    """测试无归属事件的年份"""
    schedule = create_standard_schedule(10000, date(2020, 1, 1))
    
    calendar_2019 = generate_vesting_calendar(schedule, 2019)
    test_result("vesting_calendar_empty - 无事件", len(calendar_2019) == 0)


# ============================================================
# 价值估算测试
# ============================================================

def test_estimate_vesting_value():
    """测试价值估算"""
    schedule = create_standard_schedule(10000, date(2020, 1, 1))
    
    value = estimate_vesting_value(schedule, price_per_share=10.0, as_of_date=date(2020, 6, 1))
    
    test_result("estimate_value - 总价值", value["total_value"] == 100000)
    test_result("estimate_value - 已归属价值", value["vested_value"] == 0)
    test_result("estimate_value - 未归属价值", value["unvested_value"] == 100000)
    test_result("estimate_value - 每股价格", value["price_per_share"] == 10.0)


def test_estimate_vesting_value_partial():
    """测试部分归属的价值估算"""
    schedule = create_standard_schedule(10000, date(2020, 1, 1))
    
    value = estimate_vesting_value(schedule, price_per_share=10.0, as_of_date=date(2021, 1, 1))
    
    test_result("estimate_value_partial - 已归属价值", value["vested_value"] == 25000)
    test_result("estimate_value_partial - 未归属价值", value["unvested_value"] == 75000)


# ============================================================
# 汇要和工具测试
# ============================================================

def test_vesting_summary():
    """测试归属摘要"""
    schedule = create_standard_schedule(10000, date(2020, 1, 1))
    
    summary = calculate_vesting_summary(schedule, date(2021, 1, 1))
    
    test_result("vesting_summary - 总份额", summary["total_shares"] == 10000)
    test_result("vesting_summary - 已归属份额", summary["vested_shares"] == 2500)
    test_result("vesting_summary - 未归属份额", summary["unvested_shares"] == 7500)
    test_result("vesting_summary - 类型", summary["vesting_type"] == "linear")


def test_days_until_next_vesting():
    """测试距离下次归属的天数"""
    schedule = create_standard_schedule(10000, date(2020, 1, 1))
    
    # Cliff前
    days = days_until_next_vesting(schedule, date(2020, 6, 1))
    expected = (date(2021, 1, 1) - date(2020, 6, 1)).days
    test_result("days_until_next - Cliff前", days == expected)
    
    # 完全归属后
    days_fully = days_until_next_vesting(schedule, date(2025, 1, 1))
    test_result("days_until_next - 完全归属后", days_fully == -1)


def test_format_vesting_event():
    """测试归属事件格式化"""
    event = VestingEvent(
        date=date(2021, 1, 1),
        shares=2500,
        percentage=25.0,
        is_cliff=True,
        description="Cliff归属"
    )
    
    formatted = format_vesting_event(event)
    test_result("format_event - 包含日期", "2021-01-01" in formatted)
    test_result("format_event - 包含份额", "2,500" in formatted)
    test_result("format_event - 包含比例", "25.00%" in formatted)
    test_result("format_event - Cliff标记", "[CLIFF]" in formatted)


def test_vesting_timeline():
    """测试归属时间线"""
    schedule = create_standard_schedule(10000, date(2020, 1, 1))
    
    timeline = get_vesting_timeline(schedule)
    
    test_result("vesting_timeline - 包含授予日期", "授予日期" in timeline)
    test_result("vesting_timeline - 包含总份额", "10,000" in timeline)
    test_result("vesting_timeline - 包含归属类型", "linear" in timeline)
    test_result("vesting_timeline - 包含Cliff信息", "Cliff" in timeline)


# ============================================================
# 边界值测试
# ============================================================

def test_edge_cases():
    """测试边界值"""
    # 最小份额
    schedule = VestingSchedule(
        total_shares=1,
        grant_date=date(2020, 1, 1),
        vesting_type=VestingType.IMMEDIATE,
        vesting_period_months=0
    )
    events = calculate_vesting_schedule(schedule)
    test_result("edge_case - 最小份额", events[0].shares == 1)
    
    # 大份额
    schedule = VestingSchedule(
        total_shares=10000000,
        grant_date=date(2020, 1, 1),
        vesting_type=VestingType.LINEAR,
        vesting_period_months=48,
        cliff_months=12,
        cliff_percentage=25.0
    )
    events = calculate_vesting_schedule(schedule)
    total = sum(e.shares for e in events)
    test_result("edge_case - 大份额", total == 10000000)
    
    # 最短周期（无Cliff）
    schedule = VestingSchedule(
        total_shares=100,
        grant_date=date(2020, 1, 1),
        vesting_type=VestingType.LINEAR,
        vesting_period_months=12,
        cliff_months=0,
        frequency=VestingFrequency.ANNUALLY
    )
    events = calculate_vesting_schedule(schedule)
    test_result("edge_case - 最短周期", len(events) == 1)
    
    # 最大Cliff比例
    schedule = VestingSchedule(
        total_shares=10000,
        grant_date=date(2020, 1, 1),
        vesting_type=VestingType.LINEAR,
        vesting_period_months=48,
        cliff_months=12,
        cliff_percentage=100.0  # Cliff归属全部
    )
    events = calculate_vesting_schedule(schedule)
    test_result("edge_case - Cliff全部", events[0].shares == 10000)


def test_date_edge_cases():
    """测试日期边界值"""
    # 月末日期
    schedule = VestingSchedule(
        total_shares=10000,
        grant_date=date(2020, 1, 31),
        vesting_type=VestingType.LINEAR,
        vesting_period_months=12,
        frequency=VestingFrequency.MONTHLY
    )
    events = calculate_vesting_schedule(schedule)
    test_result("date_edge - 月末授予", len(events) > 0)
    
    # 验证事件日期是否合理
    first_event = events[0]
    test_result("date_edge - 月末归属日期有效", 
                first_event.date.day <= 31)


# ============================================================
# 运行所有测试
# ============================================================

def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Vesting Schedule Utilities Test Suite")
    print("=" * 60)
    print()
    
    # 基础工具
    test_add_months()
    test_months_between()
    
    # 创建
    test_vesting_schedule_creation()
    test_create_standard_schedule()
    test_create_backloaded_schedule()
    
    # 归属计算
    test_immediate_vesting()
    test_cliff_vesting()
    test_linear_vesting_with_cliff()
    test_linear_vesting_quarterly()
    test_linear_vesting_annually()
    test_graded_vesting()
    test_graded_vesting_default()
    
    # 归属状态
    test_vesting_status_before_cliff()
    test_vesting_status_after_cliff()
    test_vesting_status_mid_vesting()
    test_vesting_status_fully_vested()
    test_vesting_status_on_vesting_date()
    
    # 加速归属
    test_accelerated_vesting()
    test_accelerated_vesting_full()
    test_accelerated_vesting_zero()
    
    # 日历和日历
    test_vesting_calendar()
    test_vesting_calendar_empty_year()
    
    # 价值估算
    test_estimate_vesting_value()
    test_estimate_vesting_value_partial()
    
    # 汇要和工具
    test_vesting_summary()
    test_days_until_next_vesting()
    test_format_vesting_event()
    test_vesting_timeline()
    
    # 边界值
    test_edge_cases()
    test_date_edge_cases()
    
    print()
    print("=" * 60)
    passed = sum(1 for r in test_results if r["passed"])
    total = len(test_results)
    print(f"测试结果: {passed}/{total} 通过")
    print("=" * 60)
    
    if passed == total:
        print("✅ 所有测试通过!")
    else:
        print("❌ 存在失败的测试")
        for r in test_results:
            if not r["passed"]:
                print(f"  - {r['name']}: {r['message']}")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)