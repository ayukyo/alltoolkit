"""
Span Utils 使用示例

展示区间操作工具的各种使用场景。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from span_utils.mod import (
    Span, BoundType,
    span, closed_span, open_span, point_span,
    merge_spans, intersection_of, subtract_span, subtract_spans,
    union_spans, find_gaps, split_span_into_chunks,
    count_overlapping, max_overlap_count, cover_spans
)


def example_basic_usage():
    """基本用法示例"""
    print("=" * 50)
    print("1. 基本用法")
    print("=" * 50)
    
    # 创建区间
    s1 = closed_span(1, 10)      # [1, 10]
    s2 = open_span(1, 10)        # (1, 10)
    s3 = Span(1, 10, BoundType.CLOSED, BoundType.OPEN)  # [1, 10)
    
    print(f"闭区间: {s1}")
    print(f"开区间: {s2}")
    print(f"左闭右开: {s3}")
    
    # 检查值是否在区间内
    print(f"\n5 在 {s1} 中: {5 in s1}")
    print(f"1 在 {s2} 中: {1 in s2}")  # 开区间不包含边界
    print(f"1 在 {s1} 中: {1 in s1}")  # 闭区间包含边界
    
    # 区间属性
    print(f"\n{s1} 长度: {s1.length()}")
    print(f"{s1} 是单点: {s1.is_point()}")
    print(f"{point_span(5)} 是单点: {point_span(5).is_point()}")


def example_merge_intervals():
    """合并重叠区间示例"""
    print("\n" + "=" * 50)
    print("2. 合并重叠区间 - 日程冲突处理")
    print("=" * 50)
    
    # 模拟一个会议安排
    meetings = [
        closed_span(9, 11),    # 9:00-11:00
        closed_span(10, 12),   # 10:00-12:00 (与前一个重叠)
        closed_span(14, 16),   # 14:00-16:00
        closed_span(15, 17),   # 15:00-17:00 (与前一个重叠)
        closed_span(18, 19),   # 18:00-19:00
    ]
    
    print("原始会议安排:")
    for i, m in enumerate(meetings, 1):
        print(f"  会议{i}: {m}")
    
    # 合并重叠区间
    merged = merge_spans(meetings)
    
    print("\n合并后的忙碌时段:")
    for i, m in enumerate(merged, 1):
        print(f"  时段{i}: {m}")


def example_time_slots():
    """时间段操作示例"""
    print("\n" + "=" * 50)
    print("3. 时间段操作 - 找出空闲时间")
    print("=" * 50)
    
    # 工作时间 9:00-18:00
    work_hours = closed_span(9, 18)
    
    # 已安排的会议
    busy_times = [
        closed_span(9, 10),
        closed_span(12, 13),
        closed_span(15, 16),
        closed_span(16, 17),
    ]
    
    print(f"工作时间: {work_hours}")
    print("已安排:")
    for t in busy_times:
        print(f"  {t}")
    
    # 找出空闲时间
    free_times = find_gaps(busy_times, work_hours)
    
    print("\n空闲时间:")
    for i, t in enumerate(free_times, 1):
        print(f"  时段{i}: {t}")


def example_ip_ranges():
    """IP 地址范围示例"""
    print("\n" + "=" * 50)
    print("4. IP 地址范围操作")
    print("=" * 50)
    
    # 模拟 IP 地址范围（简化版，实际 IP 是 4 段）
    allowed_ranges = [
        closed_span(100, 200),   # 192.168.1.100-200
        closed_span(150, 250),  # 192.168.1.150-250 (部分重叠)
        closed_span(300, 400),  # 192.168.1.300-400
    ]
    
    print("允许的 IP 范围:")
    for r in allowed_ranges:
        print(f"  {r}")
    
    # 合并重叠范围
    merged = merge_spans(allowed_ranges)
    
    print("\n合并后的范围:")
    for r in merged:
        print(f"  {r}")
    
    # 检查某个 IP 是否在允许范围内
    test_ips = [120, 220, 350, 500]
    print("\nIP 检查:")
    for ip in test_ips:
        in_range = any(ip in r for r in merged)
        status = "✓ 允许" if in_range else "✗ 拒绝"
        print(f"  IP {ip}: {status}")


def example_temperature_monitoring():
    """温度监控范围示例"""
    print("\n" + "=" * 50)
    print("5. 温度监控 - 范围分割与检查")
    print("=" * 50)
    
    # 安全温度范围
    safe_range = closed_span(18, 26)
    
    print(f"安全温度范围: {safe_range}°C")
    
    # 分割为监控区间
    zones = split_span_into_chunks(safe_range, 2)
    
    print("监控区间:")
    for i, z in enumerate(zones, 1):
        print(f"  区间{i}: {z}°C")
    
    # 温度警报范围
    warning_ranges = [
        closed_span(15, 18),   # 低温预警
        closed_span(26, 30),   # 高温预警
    ]
    
    test_temps = [16, 20, 25, 27]
    
    print("\n温度检查:")
    for temp in test_temps:
        if temp in safe_range:
            status = "正常 ✓"
        elif any(temp in r for r in warning_ranges):
            status = "预警 ⚠"
        else:
            status = "危险 ✗"
        print(f"  {temp}°C: {status}")


def example_resource_allocation():
    """资源分配示例"""
    print("\n" + "=" * 50)
    print("6. 资源分配 - 区间减法")
    print("=" * 50)
    
    # 可用资源时段
    available = closed_span(0, 24)
    
    # 已分配的资源
    allocated = [
        closed_span(2, 4),
        closed_span(8, 10),
        closed_span(14, 16),
        closed_span(20, 22),
    ]
    
    print("总资源时段:", available)
    print("已分配:")
    for i, a in enumerate(allocated, 1):
        print(f"  任务{i}: {a}")
    
    # 计算剩余可用时段
    remaining = subtract_spans(available, allocated)
    
    print("\n剩余可用时段:")
    for i, r in enumerate(remaining, 1):
        print(f"  时段{i}: {r}")


def example_overlap_analysis():
    """重叠分析示例"""
    print("\n" + "=" * 50)
    print("7. 重叠分析 - 最大重叠区间")
    print("=" * 50)
    
    # 多个服务的运行时段
    service_times = [
        closed_span(0, 8),     # 服务 A: 0-8点
        closed_span(4, 12),    # 服务 B: 4-12点
        closed_span(8, 16),    # 服务 C: 8-16点
        closed_span(10, 18),   # 服务 D: 10-18点
        closed_span(12, 20),   # 服务 E: 12-20点
    ]
    
    print("服务运行时段:")
    services = ['A', 'B', 'C', 'D', 'E']
    for s, t in zip(services, service_times):
        print(f"  服务 {s}: {t}")
    
    # 找出最大重叠
    max_count, max_region = max_overlap_count(service_times)
    
    print(f"\n最大同时运行服务数: {max_count}")
    print(f"发生在: {max_region}")
    
    # 检查各时段的运行服务数
    test_hours = [2, 6, 10, 14, 18]
    print("\n各时段运行服务数:")
    for hour in test_hours:
        count = count_overlapping(service_times, hour)
        print(f"  {hour}:00 - {count} 个服务运行中")


def example_boundary_types():
    """边界类型示例"""
    print("\n" + "=" * 50)
    print("8. 不同边界类型")
    print("=" * 50)
    
    # 四种区间类型
    intervals = [
        ("闭区间 [a,b]", Span(1, 5, BoundType.CLOSED, BoundType.CLOSED)),
        ("开区间 (a,b)", Span(1, 5, BoundType.OPEN, BoundType.OPEN)),
        ("左开右闭 (a,b]", Span(1, 5, BoundType.OPEN, BoundType.CLOSED)),
        ("左闭右开 [a,b)", Span(1, 5, BoundType.CLOSED, BoundType.OPEN)),
    ]
    
    print("区间类型及边界检查:")
    for name, s in intervals:
        print(f"\n{name} {s}")
        print(f"  1 在区间内: {1 in s}")
        print(f"  3 在区间内: {3 in s}")
        print(f"  5 在区间内: {5 in s}")


def example_number_range_operations():
    """数值范围操作示例"""
    print("\n" + "=" * 50)
    print("9. 数值范围操作")
    print("=" * 50)
    
    # 多个数值范围
    ranges = [
        closed_span(1, 10),
        closed_span(5, 15),
        closed_span(20, 30),
        closed_span(25, 35),
    ]
    
    print("原始范围:")
    for r in ranges:
        print(f"  {r}")
    
    # 并集
    union = union_spans(ranges)
    print("\n并集 (合并后):")
    for r in union:
        print(f"  {r}")
    
    # 交集
    inter = intersection_of(ranges)
    print(f"\n交集: {inter if inter else '无交集'}")
    
    # 覆盖范围
    cover = cover_spans(ranges)
    print(f"\n覆盖范围: {cover}")


def example_practical_scheduling():
    """实际调度示例"""
    print("\n" + "=" * 50)
    print("10. 实际应用：会议室调度")
    print("=" * 50)
    
    # 会议室开放时间
    room_hours = closed_span(8, 18)
    
    # 已预订的时段
    bookings = [
        ("团队A", closed_span(9, 10)),
        ("团队B", closed_span(11, 12)),
        ("团队C", closed_span(11, 13)),  # 与 B 重叠
        ("团队D", closed_span(14, 16)),
    ]
    
    print("会议室开放时间:", room_hours)
    print("\n已预订:")
    for name, time in bookings:
        print(f"  {name}: {time}")
    
    # 合并预订
    merged_bookings = merge_spans([t for _, t in bookings])
    
    print("\n合并后占用时段:")
    for t in merged_bookings:
        print(f"  {t}")
    
    # 可预订时段
    available = subtract_spans(room_hours, merged_bookings)
    
    print("\n可预订时段:")
    for i, t in enumerate(available, 1):
        hours = int(t.length())
        print(f"  时段{i}: {t} ({hours}小时)")
    
    # 尝试预订新时段
    new_booking = closed_span(10, 11)
    conflicts = [b for b in bookings if b[1].overlaps(new_booking)]
    
    print(f"\n尝试预订 {new_booking}:")
    if conflicts:
        print("  冲突! 与以下预订重叠:")
        for name, time in conflicts:
            print(f"    {name}: {time}")
    else:
        print("  可以预订 ✓")


if __name__ == "__main__":
    example_basic_usage()
    example_merge_intervals()
    example_time_slots()
    example_ip_ranges()
    example_temperature_monitoring()
    example_resource_allocation()
    example_overlap_analysis()
    example_boundary_types()
    example_number_range_operations()
    example_practical_scheduling()
    
    print("\n" + "=" * 50)
    print("所有示例运行完成!")
    print("=" * 50)