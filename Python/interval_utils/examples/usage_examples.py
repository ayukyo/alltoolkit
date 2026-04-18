"""
区间操作工具使用示例

展示 Interval、IntervalSet、RangeSet 等类的实际应用场景
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from interval_utils.mod import (
    Interval, IntervalSet, IntervalMap, RangeSet,
    merge_intervals, interval_intersection, interval_difference,
    interval_union, find_gaps, is_covered, find_containing_interval,
    get_total_coverage
)


def example_1_basic_intervals():
    """示例1：基础区间操作"""
    print("=" * 50)
    print("示例1：基础区间操作")
    print("=" * 50)
    
    # 创建区间
    i1 = Interval(1, 10)
    i2 = Interval(5, 15)
    
    print(f"区间1: {i1}")
    print(f"区间2: {i2}")
    
    # 基本属性
    print(f"\n区间1 长度: {i1.length}")
    print(f"区间1 包含 5: {5 in i1}")
    print(f"区间1 包含 15: {15 in i1}")
    
    # 区间运算
    print(f"\n重叠检测: {i1.overlaps(i2)}")
    print(f"相邻检测: {i1.adjacent(i2)}")
    print(f"交集: {i1.intersection(i2)}")
    print(f"合并: {i1.merge(i2)}")
    
    # 差集
    diff = i1.difference(i2)
    print(f"差集 (i1 - i2): {diff}")
    
    print()


def example_2_interval_set():
    """示例2：区间集合操作"""
    print("=" * 50)
    print("示例2：区间集合操作")
    print("=" * 50)
    
    # 创建区间集合
    schedule = IntervalSet()
    
    # 添加会议时间段
    schedule.add(Interval(9, 10))   # 9:00-10:00
    schedule.add(Interval(10, 11))  # 10:00-11:00 (会自动合并)
    schedule.add(Interval(14, 16))  # 14:00-16:00
    schedule.add(Interval(16, 17))  # 16:00-17:00 (会自动合并)
    
    print(f"日程安排: {schedule}")
    print(f"区间数量: {len(schedule)}")
    print(f"总时长: {schedule.total_length} 小时")
    
    # 检查时间段是否可用
    print(f"\n10:30 是否有安排: {schedule.contains(10)}")
    print(f"12:00 是否有安排: {schedule.contains(12)}")
    
    # 查找空闲时间
    gaps = schedule.gaps()
    print(f"\n空闲时间段: {gaps}")
    
    # 检查新会议是否可以安排
    new_meeting = Interval(15, 17)
    conflicts = schedule.find_overlapping(new_meeting)
    print(f"\n15:00-17:00 会议冲突: {conflicts}")
    
    print()


def example_3_time_range_management():
    """示例3：时间范围管理"""
    print("=" * 50)
    print("示例3：时间范围管理（任务调度场景）")
    print("=" * 50)
    
    # 模拟任务执行时间范围
    tasks = IntervalSet()
    
    # 添加已执行任务的时间范围
    tasks.add(Interval(0, 100))    # 任务A: 时间点 0-100
    tasks.add(Interval(150, 250))  # 任务B: 时间点 150-250
    tasks.add(Interval(300, 400))   # 任务C: 时间点 300-400
    
    print(f"已完成任务覆盖的时间范围: {tasks}")
    print(f"总执行时间: {tasks.total_length}")
    
    # 检查某时间点是否有任务执行
    print(f"\n时间点 50 是否有任务: {tasks.contains(50)}")
    print(f"时间点 200 是否有任务: {tasks.contains(200)}")
    print(f"时间点 280 是否有任务: {tasks.contains(280)}")
    
    # 找出未执行的时间段
    gaps = tasks.gaps()
    print(f"\n未执行时间段: {gaps}")
    
    # 计算某范围内的覆盖率
    range_start, range_end = 0, 500
    covered = tasks.cover_range(range_start, range_end)
    uncovered = tasks.uncovered_range(range_start, range_end)
    
    print(f"\n在 {range_start}-{range_end} 范围内:")
    print(f"  已覆盖: {covered}")
    print(f"  未覆盖: {uncovered}")
    print(f"  覆盖率: {covered.total_length / (range_end - range_start + 1) * 100:.1f}%")
    
    print()


def example_4_convenience_functions():
    """示例4：便捷函数使用"""
    print("=" * 50)
    print("示例4：便捷函数使用")
    print("=" * 50)
    
    # 场景：合并服务器维护时间窗口
    maintenance_windows = [
        (1, 5), (3, 8),   # 有重叠
        (10, 12), (13, 15), # 相邻，会合并
        (20, 25), (22, 28)  # 有重叠
    ]
    
    print(f"原始维护窗口: {maintenance_windows}")
    
    # 合并
    merged = merge_intervals(maintenance_windows)
    print(f"合并后窗口: {merged}")
    print(f"总维护时间: {get_total_coverage(maintenance_windows)}")
    
    # 场景：检查IP是否在黑名单中
    blocked_ranges = [(100, 200), (500, 600), (1000, 1100)]
    
    test_ips = [150, 300, 550, 1050]
    for ip in test_ips:
        if is_covered(blocked_ranges, ip):
            containing = find_containing_interval(blocked_ranges, ip)
            print(f"IP {ip} 被阻止 (在范围 {containing} 内)")
        else:
            print(f"IP {ip} 允许访问")
    
    print()


def example_5_interval_set_operations():
    """示例5：区间集合运算"""
    print("=" * 50)
    print("示例5：区间集合运算")
    print("=" * 50)
    
    # 两个人的可用时间
    alice = IntervalSet([
        Interval(9, 12),
        Interval(14, 18),
        Interval(20, 22)
    ])
    
    bob = IntervalSet([
        Interval(10, 11),
        Interval(15, 17),
        Interval(19, 21)
    ])
    
    print(f"Alice 可用时间: {alice}")
    print(f"Bob 可用时间: {bob}")
    
    # 共同可用时间（交集）
    common = alice.intersection(bob)
    print(f"\n共同可用时间: {common}")
    
    # Alice 独有的时间
    alice_only = alice.difference(bob)
    print(f"Alice 独有时间: {alice_only}")
    
    # 所有人可用时间（并集）
    all_available = alice.union(bob)
    print(f"至少一人可用: {all_available}")
    
    print()


def example_6_range_set():
    """示例6：RangeSet 范围集合"""
    print("=" * 50)
    print("示例6：RangeSet 范围集合（高效整数集合）")
    print("=" * 50)
    
    # 创建ID集合
    used_ids = RangeSet()
    used_ids.add_range(1, 100)    # 分配 1-100
    used_ids.add_range(200, 300)  # 分配 200-300
    used_ids.add_range(500, 600)  # 分配 500-600
    
    print(f"已分配ID区间: {used_ids.intervals}")
    print(f"已分配ID数量: {len(used_ids)}")
    
    # 检查ID是否已分配
    test_ids = [50, 150, 250, 400]
    for id in test_ids:
        status = "已分配" if id in used_ids else "可用"
        print(f"ID {id}: {status}")
    
    # 分配新ID范围
    used_ids.add_range(150, 160)
    print(f"\n分配 150-160 后: {used_ids.intervals}")
    
    # 释放ID范围
    used_ids.remove_range(50, 70)
    print(f"释放 50-70 后: {used_ids.intervals}")
    
    # ID集合运算
    another_project = RangeSet()
    another_project.add_range(80, 120)
    
    # 冲突检测
    conflicts = used_ids.intersection(another_project)
    print(f"\n与另一项目的ID冲突: {conflicts.intervals}")
    
    print()


def example_7_interval_map():
    """示例7：IntervalMap 区间映射"""
    print("=" * 50)
    print("示例7：IntervalMap 区间映射")
    print("=" * 50)
    
    # 创建时间段到优先级的映射
    priority_map = IntervalMap()
    
    priority_map.set(0, 8, "低优先级")      # 凌晨
    priority_map.set(9, 12, "高优先级")     # 上午
    priority_map.set(12, 14, "中优先级")    # 午休
    priority_map.set(14, 18, "高优先级")    # 下午
    priority_map.set(18, 24, "低优先级")    # 晚间
    
    print("时间段优先级映射:")
    for start, end, priority in priority_map.items():
        print(f"  {start:02d}:00-{end:02d}:00: {priority}")
    
    # 查询特定时间的优先级
    test_hours = [3, 10, 12, 15, 20]
    for hour in test_hours:
        priority = priority_map.get(hour)
        print(f"\n{hour}:00 的优先级: {priority}")
    
    # 查询时间范围内的映射
    print(f"\n8-12点的映射: {priority_map.get_range(8, 12)}")
    
    print()


def example_8_resource_allocation():
    """示例8：资源分配场景"""
    print("=" * 50)
    print("示例8：资源分配（磁盘空间管理）")
    print("=" * 50)
    
    # 模拟磁盘块分配
    allocated = IntervalSet()
    
    # 初始分配
    allocated.add(Interval(0, 99))     # 文件1: 块 0-99
    allocated.add(Interval(200, 299))   # 文件2: 块 200-299
    allocated.add(Interval(500, 599))   # 文件3: 块 500-599
    
    print(f"初始分配: {allocated}")
    print(f"已用空间: {allocated.total_length} 块")
    
    # 找出空闲区域
    gaps = allocated.gaps()
    print(f"\n空闲区域: {gaps}")
    
    # 找出最大连续空闲区域
    if gaps:
        max_gap = max(gaps, key=lambda x: x.length)
        print(f"最大连续空闲区域: {max_gap} ({max_gap.length} 块)")
    
    # 分配新文件（使用第一个足够大的空闲区域）
    needed_blocks = 80
    for gap in sorted(gaps, key=lambda x: x.start):
        if gap.length >= needed_blocks:
            print(f"\n新文件分配到: 块 {gap.start}-{gap.start + needed_blocks - 1}")
            allocated.add(Interval(gap.start, gap.start + needed_blocks - 1))
            break
    
    print(f"分配后: {allocated}")
    
    # 删除文件（释放空间）
    print("\n删除文件1（释放块 0-99）...")
    allocated.remove(Interval(0, 99))
    print(f"释放后: {allocated}")
    
    print()


def example_9_meeting_scheduler():
    """示例9：会议室调度"""
    print("=" * 50)
    print("示例9：会议室调度")
    print("=" * 50)
    
    # 一天的会议安排（时间用小时数表示）
    booked = IntervalSet()
    
    # 已预订的会议
    booked.add(Interval(9, 10))    # 9:00-10:00
    booked.add(Interval(11, 12))   # 11:00-12:00
    booked.add(Interval(14, 16))   # 14:00-16:00
    
    print("已预订会议:")
    for interval in booked:
        print(f"  {interval.start}:00-{interval.end}:00")
    
    # 尝试预订新会议
    new_meetings = [
        (10, 11),   # 10:00-11:00
        (11, 12),   # 11:00-12:00
        (15, 17),   # 15:00-17:00
        (16, 18),   # 16:00-18:00
    ]
    
    print("\n新会议预订请求:")
    for start, end in new_meetings:
        meeting = Interval(start, end)
        conflicts = booked.find_overlapping(meeting)
        
        if conflicts:
            print(f"  {start}:00-{end}:00 ❌ 与 {list(conflicts)} 冲突")
        else:
            print(f"  {start}:00-{end}:00 ✅ 可以预订")
            booked.add(meeting)
    
    print(f"\n更新后的预订: {booked}")
    
    # 找出可用时段
    working_hours = Interval(9, 18)
    available = IntervalSet([working_hours])
    for meeting in booked:
        available.remove(meeting)
    
    print(f"\n剩余可用时段: {available}")
    
    print()


def example_10_ip_address_management():
    """示例10：IP地址段管理"""
    print("=" * 50)
    print("示例10：IP地址段管理")
    print("=" * 50)
    
    # 公司IP地址池管理
    allocated = IntervalSet()
    
    # 已分配的IP段
    allocated.add(Interval(
        ip_to_int("192.168.1.1"),
        ip_to_int("192.168.1.50")
    ))
    allocated.add(Interval(
        ip_to_int("192.168.1.100"),
        ip_to_int("192.168.1.150")
    ))
    
    print("已分配IP段:")
    for interval in allocated:
        print(f"  {int_to_ip(interval.start)} - {int_to_ip(interval.end)}")
    
    # 检查IP是否已分配
    test_ips = ["192.168.1.25", "192.168.1.75", "192.168.1.125"]
    print("\nIP分配状态:")
    for ip in test_ips:
        ip_int = ip_to_int(ip)
        if allocated.contains(ip_int):
            containing = allocated.find_containing(ip_int)
            print(f"  {ip}: 已分配 (在 {int_to_ip(containing.start)}-{int_to_ip(containing.end)} 段)")
        else:
            print(f"  {ip}: 可用")
    
    # 找出可用IP段
    full_range = Interval(
        ip_to_int("192.168.1.1"),
        ip_to_int("192.168.1.254")
    )
    available = IntervalSet([full_range])
    for interval in allocated:
        available.remove(interval)
    
    print("\n可用IP段:")
    for interval in available:
        print(f"  {int_to_ip(interval.start)} - {int_to_ip(interval.end)} ({interval.length} 个)")
    
    print()


def ip_to_int(ip: str) -> int:
    """IP地址转整数"""
    parts = ip.split(".")
    return (int(parts[0]) << 24) + (int(parts[1]) << 16) + (int(parts[2]) << 8) + int(parts[3])


def int_to_ip(num: int) -> str:
    """整数转IP地址"""
    return f"{(num >> 24) & 255}.{(num >> 16) & 255}.{(num >> 8) & 255}.{num & 255}"


if __name__ == "__main__":
    example_1_basic_intervals()
    example_2_interval_set()
    example_3_time_range_management()
    example_4_convenience_functions()
    example_5_interval_set_operations()
    example_6_range_set()
    example_7_interval_map()
    example_8_resource_allocation()
    example_9_meeting_scheduler()
    example_10_ip_address_management()
    
    print("=" * 50)
    print("所有示例运行完成！")
    print("=" * 50)