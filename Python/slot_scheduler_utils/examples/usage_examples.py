"""
时间槽调度工具使用示例

演示：
- 创建会议室预订系统
- 医生预约排班
- 多资源调度
- 重复预约处理
"""

from datetime import datetime, timedelta, date, time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    TimeSlot, RecurrenceRule, RecurrenceType, BookingStatus,
    SlotScheduler,
    create_daily_slots, find_free_time, calculate_utilization
)


def example_meeting_room():
    """示例：会议室预订系统"""
    print("\n" + "="*60)
    print("示例 1: 会议室预订系统")
    print("="*60)
    
    scheduler = SlotScheduler(default_slot_duration=30)
    
    # 创建一周的会议室时间槽
    slots = scheduler.create_slots_from_schedule(
        resource_id="meeting_room_A",
        start_date=date(2024, 1, 15),
        end_date=date(2024, 1, 19),
        daily_start_time=time(9, 0),
        daily_end_time=time(18, 0),
        slot_duration=60,
        break_between_slots=0,
        working_days=[0, 1, 2, 3, 4]  # 周一到周五
    )
    
    print(f"\n创建了 {len(slots)} 个时间槽（5个工作日，每天9小时）")
    
    # 查看周一的时间槽
    monday_slots = [s for s in slots if s.start.date() == date(2024, 1, 15)]
    print(f"\n周一 ({date(2024, 1, 15)}) 的时间槽:")
    for slot in monday_slots[:3]:
        print(f"  {slot.start.strftime('%H:%M')} - {slot.end.strftime('%H:%M')}")
    
    # 预约几个时间槽
    print("\n预约时间槽:")
    
    # 预约周一上午10点的会议
    booking1 = scheduler.book_slot(
        slot_id=monday_slots[1].slot_id,
        user_id="user_zhang",
        notes="产品评审会议"
    )
    print(f"  张三预约: {booking1.slot.start.strftime('%Y-%m-%d %H:%M')} - {booking1.slot.end.strftime('%H:%M')}")
    
    # 预约周一下午2点的会议
    booking2 = scheduler.book_slot(
        slot_id=monday_slots[5].slot_id,
        user_id="user_li",
        notes="技术讨论"
    )
    print(f"  李四预约: {booking2.slot.start.strftime('%Y-%m-%d %H:%M')} - {booking2.slot.end.strftime('%H:%M')}")
    
    # 尝试预约已被占用的时段
    failed_booking = scheduler.book_slot(
        slot_id=monday_slots[1].slot_id,
        user_id="user_wang",
        notes="紧急会议"
    )
    print(f"  王五尝试预约已被占用时段: {'成功' if failed_booking else '失败（时段已被预订）'}")
    
    # 查找下一个可用时间槽
    next_available = scheduler.find_next_available(
        resource_id="meeting_room_A",
        after=datetime(2024, 1, 15, 11, 0)
    )
    print(f"\n下一个可用时间槽: {next_available.start.strftime('%Y-%m-%d %H:%M')}")
    
    # 获取周一的调度摘要
    summary = scheduler.get_schedule_summary("meeting_room_A", date(2024, 1, 15))
    print(f"\n周一调度摘要:")
    print(f"  总时间槽: {summary['total_slots']}")
    print(f"  已预订: {summary['booked_slots']}")
    print(f"  可用: {summary['available_slots']}")
    print(f"  利用率: {summary['utilization_rate']:.1%}")


def example_doctor_appointment():
    """示例：医生预约排班"""
    print("\n" + "="*60)
    print("示例 2: 医生预约排班")
    print("="*60)
    
    scheduler = SlotScheduler()
    
    # 创建医生的每日门诊时间槽
    today = date(2024, 1, 15)
    
    # 上午门诊: 8:00-12:00，每30分钟一个号
    morning_slots = scheduler.create_slots_from_schedule(
        resource_id="doctor_wang",
        start_date=today,
        end_date=today,
        daily_start_time=time(8, 0),
        daily_end_time=time(12, 0),
        slot_duration=30,
        break_between_slots=5  # 每个号之间休息5分钟
    )
    
    # 下午门诊: 14:00-17:00
    afternoon_slots = scheduler.create_slots_from_schedule(
        resource_id="doctor_wang",
        start_date=today,
        end_date=today,
        daily_start_time=time(14, 0),
        daily_end_time=time(17, 0),
        slot_duration=30,
        break_between_slots=5
    )
    
    print(f"\n王医生今日门诊时间槽:")
    print(f"  上午: {len(morning_slots)} 个")
    print(f"  下午: {len(afternoon_slots)} 个")
    
    # 预约挂号
    bookings = []
    patients = [
        ("patient_001", "头痛检查"),
        ("patient_002", "体检复查"),
        ("patient_003", "开药"),
        ("patient_004", "咨询"),
    ]
    
    all_slots = morning_slots + afternoon_slots
    
    print("\n挂号预约:")
    for i, (patient_id, reason) in enumerate(patients):
        slot = all_slots[i]
        booking = scheduler.book_slot(
            slot_id=slot.slot_id,
            user_id=patient_id,
            notes=reason
        )
        bookings.append(booking)
        print(f"  患者{patient_id}: {slot.start.strftime('%H:%M')} - {reason}")
    
    # 查找下午第一个可用时间槽
    next_slot = scheduler.find_next_available(
        resource_id="doctor_wang",
        after=datetime(2024, 1, 15, 14, 0)
    )
    print(f"\n下午第一个可用时间: {next_slot.start.strftime('%H:%M')}")
    
    # 封锁一个时间槽（医生临时有事）
    block_slot = all_slots[5]
    scheduler.block_slot(block_slot.slot_id, "医生外出急诊")
    print(f"\n临时封锁时间槽: {block_slot.start.strftime('%H:%M')} (医生外出急诊)")
    
    # 再次查看可用时间
    available_count = len(scheduler.get_available_slots("doctor_wang"))
    print(f"\n当前可用挂号数: {available_count}")


def example_multi_resource():
    """示例：多资源调度"""
    print("\n" + "="*60)
    print("示例 3: 多资源调度（网球场地）")
    print("="*60)
    
    scheduler = SlotScheduler()
    
    # 创建3个网球场地的时间槽
    courts = ["court_1", "court_2", "court_3"]
    
    for court in courts:
        scheduler.create_slots_from_schedule(
            resource_id=court,
            start_date=date(2024, 1, 15),
            end_date=date(2024, 1, 15),
            daily_start_time=time(8, 0),
            daily_end_time=time(20, 0),
            slot_duration=60,
            break_between_slots=15
        )
    
    print(f"\n创建了3个网球场地的时间槽")
    
    # 查看每个场地的可用情况
    for court in courts:
        available = len(scheduler.get_available_slots(court))
        print(f"  {court}: {available} 个可用时间槽")
    
    # 预约场地
    print("\n预约场地:")
    
    # 用户1预约场地1的上午时段
    court1_slots = scheduler.get_slots_by_resource("court_1")
    booking1 = scheduler.book_slot(
        slot_id=court1_slots[0].slot_id,
        user_id="player_chen",
        notes="双打练习"
    )
    print(f"  陈同学预约场地1: {booking1.slot.start.strftime('%H:%M')}")
    
    # 用户2预约场地2同一时段
    court2_slots = scheduler.get_slots_by_resource("court_2")
    booking2 = scheduler.book_slot(
        slot_id=court2_slots[0].slot_id,
        user_id="player_zhou",
        notes="教学课"
    )
    print(f"  周同学预约场地2: {booking2.slot.start.strftime('%H:%M')}")
    
    # 查找任何场地在指定时段的可用性
    print("\n查找10:00时段的可用场地:")
    for court in courts:
        available, conflicts = scheduler.check_availability(
            resource_id=court,
            start=datetime(2024, 1, 15, 10, 0),
            end=datetime(2024, 1, 15, 11, 0)
        )
        print(f"  {court}: {'可用' if available else '已预订'}")


def example_recurring():
    """示例：重复预约"""
    print("\n" + "="*60)
    print("示例 4: 重复预约（每周例会）")
    print("="*60)
    
    scheduler = SlotScheduler()
    
    # 创建每周一上午的重复时间槽
    rule = RecurrenceRule(
        recurrence_type=RecurrenceType.WEEKLY,
        interval=1,
        days_of_week=[0],  # 周一
        count=4  # 4周
    )
    
    recurring_slots = scheduler.create_recurring_slots(
        base_start=datetime(2024, 1, 15, 10, 0),
        base_end=datetime(2024, 1, 15, 11, 30),
        resource_id="weekly_meeting",
        recurrence=rule
    )
    
    print(f"\n创建了 {len(recurring_slots)} 个每周重复的时间槽")
    
    for slot in recurring_slots:
        print(f"  {slot.start.strftime('%Y-%m-%d %H:%M')} - {slot.end.strftime('%H:%M')}")
    
    # 预约整个系列的会议
    print("\n预约每周例会:")
    for slot in recurring_slots:
        scheduler.book_slot(
            slot_id=slot.slot_id,
            user_id="team_alpha",
            notes="团队周例会"
        )
    
    print("  已预约全部4周的时间槽")
    
    # 取消其中一周的会议
    second_slot = recurring_slots[1]
    booking = scheduler.get_user_bookings("team_alpha")[1]
    scheduler.cancel_booking(booking.booking_id)
    print(f"\n取消了第二周的会议: {second_slot.start.strftime('%Y-%m-%d')}")
    
    # 查看当前预约状态
    remaining_bookings = scheduler.get_user_bookings("team_alpha")
    print(f"\n剩余预约数: {len(remaining_bookings)}")


def example_free_time_detection():
    """示例：空闲时间检测"""
    print("\n" + "="*60)
    print("示例 5: 空闲时间检测")
    print("="*60)
    
    scheduler = SlotScheduler()
    
    # 创建一天的时间槽
    scheduler.create_slots_from_schedule(
        resource_id="office",
        start_date=date(2024, 1, 15),
        end_date=date(2024, 1, 15),
        daily_start_time=time(8, 0),
        daily_end_time=time(18, 0),
        slot_duration=30
    )
    
    # 预约一些时段
    slots = scheduler.get_slots_by_resource("office")
    
    # 预约上午的几个时段
    for i in range(4):  # 8:00-10:00
        scheduler.book_slot(slots[i].slot_id, "user_meeting")
    
    # 预约下午的一些时段
    for i in range(16, 20):  # 16:00-18:00
        scheduler.book_slot(slots[i].slot_id, "user_meeting")
    
    print(f"\n已预约时段: 8:00-10:00 和 16:00-18:00")
    
    # 使用 find_free_time 查找连续空闲时间
    all_slots = scheduler.get_slots_by_resource("office")
    free_periods = find_free_time(all_slots, min_duration_minutes=60)
    
    print(f"\n查找至少60分钟的连续空闲时间:")
    for start, end in free_periods:
        duration = (end - start).total_seconds() / 60
        print(f"  {start.strftime('%H:%M')} - {end.strftime('%H:%M')} ({duration:.0f}分钟)")
    
    # 计算利用率
    stats = calculate_utilization(all_slots)
    print(f"\n利用率统计:")
    print(f"  总时长: {stats['total_minutes']} 分钟")
    print(f"  已预订: {stats['booked_minutes']} 分钟")
    print(f"  利用率: {stats['utilization']:.1%}")


def example_data_export():
    """示例：数据导出导入"""
    print("\n" + "="*60)
    print("示例 6: 数据导出导入")
    print("="*60)
    
    scheduler = SlotScheduler()
    
    # 创建一些时间槽和预约
    scheduler.create_slots_from_schedule(
        resource_id="room_export",
        start_date=date(2024, 1, 15),
        end_date=date(2024, 1, 15),
        daily_start_time=time(9, 0),
        daily_end_time=time(12, 0),
        slot_duration=60
    )
    
    slots = scheduler.get_slots_by_resource("room_export")
    scheduler.book_slot(slots[0].slot_id, "user_export", "测试导出")
    
    # 导出数据
    data = scheduler.to_dict()
    
    print("\n导出数据结构:")
    print(f"  时间槽数量: {len(data['slots'])}")
    print(f"  预约数量: {len(data['bookings'])}")
    
    # 导入数据到新调度器
    new_scheduler = SlotScheduler.from_dict(data)
    
    print("\n导入后的调度器状态:")
    print(f"  时间槽数量: {len(new_scheduler.slots)}")
    print(f"  预约数量: {len(new_scheduler.bookings)}")
    print(f"  用户预约: {len(new_scheduler.user_bookings)}")


def main():
    """运行所有示例"""
    example_meeting_room()
    example_doctor_appointment()
    example_multi_resource()
    example_recurring()
    example_free_time_detection()
    example_data_export()
    
    print("\n" + "="*60)
    print("所有示例完成！")
    print("="*60)


if __name__ == "__main__":
    main()