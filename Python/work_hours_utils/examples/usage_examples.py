"""
工作时长计算工具使用示例

演示如何使用 work_hours_utils 模块的各种功能。
"""

from datetime import datetime, time, date, timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    WorkHoursCalculator,
    WorkShift,
    TimeSlot,
    PunchRecord,
    WorkDayType,
    OvertimeType,
    ShiftScheduler,
    TimeAttendanceAnalyzer,
    create_punch_record,
    STANDARD_DAY_SHIFT,
    STANDARD_NIGHT_SHIFT,
    THREE_SHIFT_MORNING,
    THREE_SHIFT_AFTERNOON,
    THREE_SHIFT_NIGHT,
)


def example_daily_hours_calculation():
    """示例：日工作时长计算"""
    print("=" * 60)
    print("示例 1: 日工作时长计算")
    print("=" * 60)
    
    # 创建计算器，设置午休时间
    calculator = WorkHoursCalculator(
        standard_work_hours=8.0,
        break_periods=[(time(12, 0), time(13, 0))]  # 12:00-13:00 午休
    )
    
    # 场景 1: 正常工作日
    print("\n场景 1: 正常工作日 (09:00 - 18:00)")
    result = calculator.calculate_daily_hours(
        check_in=time(9, 0),
        check_out=time(18, 0)
    )
    print(f"  总时长: {result['total_hours']} 小时")
    print(f"  休息时长: {result['break_hours']} 小时")
    print(f"  实际工作: {result['actual_work_hours']} 小时")
    print(f"  加班时长: {result['overtime_hours']} 小时")
    
    # 场景 2: 有加班
    print("\n场景 2: 加班情况 (09:00 - 21:00)")
    result = calculator.calculate_daily_hours(
        check_in=time(9, 0),
        check_out=time(21, 0)
    )
    print(f"  总时长: {result['total_hours']} 小时")
    print(f"  实际工作: {result['actual_work_hours']} 小时")
    print(f"  加班时长: {result['overtime_hours']} 小时")
    
    # 场景 3: 夜班
    print("\n场景 3: 夜班 (22:00 - 06:00)")
    result = calculator.calculate_daily_hours(
        check_in=time(22, 0),
        check_out=time(6, 0)
    )
    print(f"  总时长: {result['total_hours']} 小时")
    print(f"  夜班时长: {result['night_hours']} 小时")
    
    print("\n" + "-" * 60)


def example_weekly_hours_calculation():
    """示例：周工作时长统计"""
    print("=" * 60)
    print("示例 2: 周工作时长统计")
    print("=" * 60)
    
    calculator = WorkHoursCalculator(
        break_periods=[(time(12, 0), time(13, 0))]
    )
    
    # 创建一周的打卡记录
    records = [
        create_punch_record("2024-01-08", "09:00", "18:00"),  # 周一 正常
        create_punch_record("2024-01-09", "09:00", "19:30"),  # 周二 加班1.5h
        create_punch_record("2024-01-10", "09:00", "20:00"),  # 周三 加班2h
        create_punch_record("2024-01-11", "09:00", "18:00"),  # 周四 正常
        create_punch_record("2024-01-12", "09:00", "17:30"),  # 周五 早退0.5h
    ]
    
    result = calculator.calculate_weekly_hours(records)
    
    print(f"\n本周工作统计:")
    print(f"  总工作时长: {result['total_work_hours']} 小时")
    print(f"  加班时长: {result['total_overtime_hours']} 小时")
    print(f"  夜班时长: {result['total_night_hours']} 小时")
    print(f"  工作天数: {result['work_days']}")
    print(f"  日均时长: {result['average_daily_hours']} 小时")
    
    # 显示加班详情
    print(f"\n加班详情:")
    for ot in result['overtime_records']:
        print(f"  {ot.date}: {ot.hours}小时 ({ot.overtime_type.value}) - 倍率{ot.rate}x")
    
    # 合规检查
    compliance = result['compliance']
    print(f"\n合规检查:")
    print(f"  是否合规: {'是' if compliance['is_compliant'] else '否'}")
    if compliance['warnings']:
        print(f"  警告:")
        for w in compliance['warnings']:
            print(f"    {w}")
    
    print("\n" + "-" * 60)


def example_overtime_pay_calculation():
    """示例：加班工资计算"""
    print("=" * 60)
    print("示例 3: 加班工资计算")
    print("=" * 60)
    
    calculator = WorkHoursCalculator(
        break_periods=[(time(12, 0), time(13, 0))]
    )
    
    # 创建包含各种加班类型的记录
    records = [
        # 工作日加班
        create_punch_record("2024-01-08", "09:00", "21:00"),  # 加班3h
        create_punch_record("2024-01-09", "09:00", "20:00"),  # 加班2h
        # 周末加班
        create_punch_record("2024-01-13", "09:00", "18:00", "weekend"),  # 周末加班8h
        # 法定节假日加班
        create_punch_record("2024-01-14", "09:00", "18:00", "holiday"),  # 节假日加班8h
    ]
    
    result = calculator.calculate_weekly_hours(records)
    
    # 计算加班工资（假设小时工资率为 50 元）
    hourly_rate = 50.0
    overtime_pay = calculator.calculate_overtime_pay(
        result['overtime_records'],
        hourly_rate=hourly_rate
    )
    
    print(f"\n加班工资计算:")
    print(f"  小时工资率: ¥{hourly_rate}")
    print(f"  总加班时长: {overtime_pay['total_overtime_hours']} 小时")
    print(f"  总加班工资: ¥{overtime_pay['total_overtime_pay']}")
    
    print(f"\n加班明细:")
    print(f"  {'日期':<12} {'类型':<20} {'时长':<8} {'倍率':<6} {'工资':<8}")
    print(f"  {'-'*12} {'-'*20} {'-'*8} {'-'*6} {'-'*8}")
    for item in overtime_pay['breakdown']:
        print(f"  {item['date']:<12} {item['type']:<20} {item['hours']:<8} {item['rate']:<6} ¥{item['pay']:<8}")
    
    # 加班倍率说明
    print(f"\n加班倍率说明:")
    print(f"  工作日加班: 1.5 倍")
    print(f"  周末加班: 2.0 倍")
    print(f"  法定节假日: 3.0 倍")
    
    print("\n" + "-" * 60)


def example_flexible_work_hours():
    """示例：弹性工作制"""
    print("=" * 60)
    print("示例 4: 弹性工作制")
    print("=" * 60)
    
    # 创建弹性工作计算器
    # 核心工作时间：10:00-16:00 必须在岗
    calculator = WorkHoursCalculator(
        flexible_hours=True,
        core_hours=(time(10, 0), time(16, 0)),
        standard_work_hours=8.0,
        break_periods=[(time(12, 0), time(13, 0))]
    )
    
    # 场景 1: 早到早走
    print("\n场景 1: 早到早走 (08:00 - 17:00)")
    result = calculator.calculate_flexible_hours(
        check_in=time(8, 0),
        check_out=time(17, 0)
    )
    print(f"  实际工作: {result['actual_work_hours']} 小时")
    print(f"  与标准差异: {result['hours_difference']} 小时")
    print(f"  弹性额度: {result['flex_credit']} 小时")
    print(f"  核心时间: {result['core_hours']['start']} - {result['core_hours']['end']}")
    
    # 场景 2: 晚到晚走
    print("\n场景 2: 晚到晚走 (10:00 - 19:00)")
    result = calculator.calculate_flexible_hours(
        check_in=time(10, 0),
        check_out=time(19, 0)
    )
    print(f"  实际工作: {result['actual_work_hours']} 小时")
    print(f"  与标准差异: {result['hours_difference']} 小时")
    
    # 场景 3: 加班积累弹性额度
    print("\n场景 3: 加班积累 (09:00 - 20:00)")
    result = calculator.calculate_flexible_hours(
        check_in=time(9, 0),
        check_out=time(20, 0)
    )
    print(f"  实际工作: {result['actual_work_hours']} 小时")
    print(f"  弹性额度: {result['flex_credit']} 小时 (可用于调休)")
    
    print("\n" + "-" * 60)


def example_shift_scheduling():
    """示例：排班调度"""
    print("=" * 60)
    print("示例 5: 排班调度")
    print("=" * 60)
    
    # 创建三班倒调度器
    scheduler = ShiftScheduler([
        THREE_SHIFT_MORNING,    # 06:00-14:00
        THREE_SHIFT_AFTERNOON,  # 14:00-22:00
        THREE_SHIFT_NIGHT,      # 22:00-06:00
    ])
    
    print("\n班次信息:")
    for shift_name in ["早班", "中班", "晚班"]:
        shift = scheduler.shifts[shift_name]
        print(f"  {shift.name}:")
        for period in shift.work_periods:
            print(f"    {period.start.strftime('%H:%M')} - {period.end.strftime('%H:%M')}")
        print(f"    总时长: {shift.total_work_hours()} 小时")
        print(f"    夜班: {'是' if shift.is_night_shift else '否'}")
    
    # 生成本周排班表
    employee_id = "EMP001"
    start_date = date(2024, 1, 8)
    shift_pattern = ["早班", "中班", "晚班", "早班", "中班", "off", "off"]
    
    print(f"\n员工 {employee_id} 本周排班表:")
    schedule = scheduler.generate_weekly_schedule(employee_id, start_date, shift_pattern)
    
    for day in schedule:
        if day['is_rest_day']:
            print(f"  {day['date']} ({day['day_of_week'][:3]}): 休息")
        else:
            shift = day['shift']
            periods_str = ", ".join([
                f"{p['start']}-{p['end']}" for p in shift['work_periods']
            ])
            print(f"  {day['date']} ({day['day_of_week'][:3]}): {shift['name']} [{periods_str}]")
    
    # 统计
    stats = scheduler.calculate_shift_statistics(schedule)
    print(f"\n本周统计:")
    print(f"  工作天数: {stats['work_days']}")
    print(f"  休息天数: {stats['rest_days']}")
    print(f"  夜班次数: {stats['night_shifts']}")
    print(f"  总工作时长: {stats['total_work_hours']} 小时")
    
    print("\n" + "-" * 60)


def example_attendance_analysis():
    """示例：考勤分析"""
    print("=" * 60)
    print("示例 6: 考勤分析")
    print("=" * 60)
    
    # 创建考勤分析器
    analyzer = TimeAttendanceAnalyzer(
        standard_start=time(9, 0),
        standard_end=time(18, 0),
        grace_minutes=15,        # 宽限15分钟
        late_threshold_minutes=30,  # 超过30分钟为严重迟到
    )
    
    # 创建一个月的打卡记录
    records = [
        # 第1周
        create_punch_record("2024-01-08", "09:00", "18:00"),  # 正常
        create_punch_record("2024-01-09", "09:05", "18:00"),  # 宽限内
        create_punch_record("2024-01-10", "09:20", "18:00"),  # 迟到
        create_punch_record("2024-01-11", "09:00", "17:30"),  # 早退
        create_punch_record("2024-01-12", "09:00", "18:00"),  # 正常
        # 第2周
        create_punch_record("2024-01-15", "09:00", "18:00"),  # 正常
        create_punch_record("2024-01-16", "09:35", "18:00"),  # 严重迟到
        create_punch_record("2024-01-17", None, None),        # 缺勤
        create_punch_record("2024-01-18", "09:00", None),     # 缺卡
        create_punch_record("2024-01-19", "09:00", "18:00"),  # 正常
    ]
    
    # 分析
    result = analyzer.analyze_period(records)
    summary = result['summary']
    
    print(f"\n考勤统计:")
    print(f"  统计天数: {summary['total_days']}")
    print(f"  工作天数: {summary['work_days']}")
    print(f"  正常天数: {summary['normal_days']}")
    print(f"  迟到天数: {summary['late_days']}")
    print(f"  早退天数: {summary['early_leave_days']}")
    print(f"  缺勤天数: {summary['absent_days']}")
    print(f"  缺卡天数: {summary['missing_checkout_days']}")
    print(f"  累计迟到: {summary['total_late_minutes']} 分钟")
    print(f"  累计早退: {summary['total_early_leave_minutes']} 分钟")
    
    print(f"\n绩效指标:")
    print(f"  出勤率: {summary['attendance_rate']}%")
    print(f"  准时率: {summary['punctuality_rate']}%")
    
    # 显示异常记录
    print(f"\n异常记录详情:")
    anomalies = [d for d in result['details'] if d.get('status') != 'normal' and d.get('is_work_day')]
    for a in anomalies:
        print(f"  {a['date']}: {a['status_text']}")
        if a.get('late_minutes', 0) > 0:
            print(f"    迟到 {a['late_minutes']} 分钟")
        if a.get('early_leave_minutes', 0) > 0:
            print(f"    早退 {a['early_leave_minutes']} 分钟")
    
    print("\n" + "-" * 60)


def example_custom_shift():
    """示例：自定义班次"""
    print("=" * 60)
    print("示例 7: 自定义班次")
    print("=" * 60)
    
    # 创建自定义班次
    custom_shift = WorkShift(
        name="弹性班",
        work_periods=[
            TimeSlot(time(10, 0), time(13, 0)),
            TimeSlot(time(14, 0), time(19, 0)),
        ],
        is_night_shift=False
    )
    
    print(f"\n自定义班次信息:")
    print(f"  名称: {custom_shift.name}")
    for period in custom_shift.work_periods:
        print(f"  工作时段: {period.start.strftime('%H:%M')} - {period.end.strftime('%H:%M')}")
    print(f"  总时长: {custom_shift.total_work_hours()} 小时")
    
    # 创建包含休息时段的计算器
    calculator = WorkHoursCalculator(
        standard_work_hours=8.0,
        break_periods=[
            (time(12, 0), time(13, 0)),  # 午休
            (time(15, 30), time(16, 0)), # 下午茶歇
        ]
    )
    
    # 计算该班次的工作时长
    result = calculator.calculate_daily_hours(
        check_in=time(10, 0),
        check_out=time(19, 0)
    )
    
    print(f"\n该班次工作时长计算:")
    print(f"  总时长: {result['total_hours']} 小时")
    print(f"  休息时长: {result['break_hours']} 小时")
    print(f"  实际工作: {result['actual_work_hours']} 小时")
    
    print("\n" + "-" * 60)


def example_compliance_check():
    """示例：工时合规检查"""
    print("=" * 60)
    print("示例 8: 工时合规检查")
    print("=" * 60)
    
    calculator = WorkHoursCalculator()
    
    # 测试不同周工时的合规情况
    test_cases = [
        (40.0, "标准周工时"),
        (44.0, "法定上限"),
        (48.0, "超标"),
        (55.0, "严重超标"),
    ]
    
    print(f"\n合规标准:")
    print(f"  标准周工时: {calculator.standard_weekly_hours} 小时")
    print(f"  法定上限: 44 小时")
    
    print(f"\n合规测试:")
    for hours, desc in test_cases:
        result = calculator.check_weekly_compliance(hours)
        status = "✓ 合规" if result['is_compliant'] else "✗ 超标"
        print(f"\n  {desc} ({hours}小时):")
        print(f"    状态: {status}")
        print(f"    加班时长: {result['overtime_hours']} 小时")
        print(f"    超出上限: {result['exceeded_hours']} 小时")
        if result['warnings']:
            print(f"    警告:")
            for w in result['warnings']:
                print(f"      {w}")
    
    print("\n" + "-" * 60)


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("工作时长计算工具 (work_hours_utils) 使用示例")
    print("=" * 60 + "\n")
    
    example_daily_hours_calculation()
    example_weekly_hours_calculation()
    example_overtime_pay_calculation()
    example_flexible_work_hours()
    example_shift_scheduling()
    example_attendance_analysis()
    example_custom_shift()
    example_compliance_check()
    
    print("\n所有示例运行完成！")


if __name__ == "__main__":
    main()