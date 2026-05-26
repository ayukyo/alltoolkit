"""
Timeline Utils Examples - 使用示例

演示时间线工具的各种功能和使用场景。
"""

from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from timeline_utils import (
    Timeline, TimelineEvent, EventType,
    create_timeline, create_point_event,
    create_range_event, create_milestone,
    format_duration, check_overlap
)


def example_basic_timeline():
    """基础时间线示例"""
    print("\n" + "="*60)
    print("Example 1: Basic Timeline")
    print("="*60)
    
    # 创建时间线
    timeline = Timeline("Daily Schedule")
    
    # 基准时间
    base = datetime(2024, 1, 15, 8, 0)
    
    # 添加范围事件
    timeline.add_range_event(
        "morning_work", "Morning Work",
        base, base + timedelta(hours=3),
        description="Focus time for deep work",
        tags=["work", "focus"]
    )
    
    # 添加瞬时事件
    timeline.add_point_event(
        "break", "Coffee Break",
        base + timedelta(hours=3),
        tags=["break"]
    )
    
    # 添加另一个范围事件
    timeline.add_range_event(
        "meeting", "Team Meeting",
        base + timedelta(hours=3, minutes=30),
        base + timedelta(hours=4, minutes=30),
        description="Weekly sync meeting",
        tags=["meeting", "team"]
    )
    
    # 添加里程碑
    timeline.add_milestone(
        "lunch", "Lunch Time",
        base + timedelta(hours=5),
        description="Break for lunch"
    )
    
    # 渲染时间线
    print("\n--- ASCII Timeline (Vertical) ---")
    print(timeline.render_ascii(width=60))
    
    print("\n--- Horizontal Timeline (Gantt Style) ---")
    print(timeline.render_horizontal(width=50))
    
    # 统计信息
    print("\n--- Statistics ---")
    stats = timeline.statistics()
    print(f"Total events: {stats['total_events']}")
    print(f"Range events: {stats['range_events']}")
    print(f"Point events: {stats['point_events']}")
    print(f"Milestones: {stats['milestones']}")
    print(f"Total event duration: {format_duration(timedelta(seconds=stats['total_event_duration_seconds']))}")


def example_conflict_detection():
    """冲突检测示例"""
    print("\n" + "="*60)
    print("Example 2: Conflict Detection")
    print("="*60)
    
    timeline = Timeline("Meeting Schedule")
    
    base = datetime(2024, 1, 15, 9, 0)
    
    # 添加会议
    timeline.add_range_event("m1", "Planning Meeting", base, base + timedelta(hours=1))
    timeline.add_range_event("m2", "Team Sync", base + timedelta(minutes=30), base + timedelta(hours=1, minutes=30))
    timeline.add_range_event("m3", "Client Call", base + timedelta(hours=2), base + timedelta(hours=3))
    
    # 渲染
    print(timeline.render_ascii(width=60, highlight_overlaps=True))
    
    # 检测冲突
    print("\n--- Conflict Analysis ---")
    if timeline.has_conflicts():
        print("⚠️  Conflicts detected!")
        overlaps = timeline.find_overlaps()
        for e1, e2 in overlaps:
            print(f"  - '{e1.name}' overlaps with '{e2.name}'")
            print(f"    {e1.start_time.strftime('%H:%M')}-{e1.end_time.strftime('%H:%M')} vs {e2.start_time.strftime('%H:%M')}-{e2.end_time.strftime('%H:%M')}")
    else:
        print("✅ No conflicts")


def example_gap_finding():
    """查找空闲时间示例"""
    print("\n" + "="*60)
    print("Example 3: Finding Free Time (Gaps)")
    print("="*60)
    
    timeline = Timeline("Work Day")
    
    base = datetime(2024, 1, 15, 8, 0)
    
    # 添加日程
    timeline.add_range_event("e1", "Morning Routine", base, base + timedelta(hours=1))
    timeline.add_range_event("e2", "Deep Work", base + timedelta(hours=1, minutes=30), base + timedelta(hours=3))
    timeline.add_range_event("e3", "Lunch", base + timedelta(hours=4), base + timedelta(hours=5))
    timeline.add_range_event("e4", "Afternoon Work", base + timedelta(hours=6), base + timedelta(hours=8))
    
    # 渲染
    print(timeline.render_ascii(width=60, compact=True))
    
    # 查找间隙
    print("\n--- Available Free Time ---")
    gaps = timeline.find_gaps(min_gap=timedelta(minutes=10))
    
    if gaps:
        for start, end in gaps:
            gap_duration = format_duration(end - start)
            print(f"  Free: {start.strftime('%H:%M')} - {end.strftime('%H:%M')} ({gap_duration})")
    else:
        print("  No free time slots available")


def example_project_schedule():
    """项目进度示例"""
    print("\n" + "="*60)
    print("Example 4: Project Schedule (Gantt Chart)")
    print("="*60)
    
    timeline = Timeline("Website Development")
    
    base = datetime(2024, 1, 1, 0, 0)
    
    # 项目阶段
    timeline.add_range_event(
        "phase1", "Requirements Gathering",
        base, base + timedelta(days=3),
        tags=["planning"]
    )
    
    timeline.add_range_event(
        "phase2", "Design",
        base + timedelta(days=3), base + timedelta(days=7),
        tags=["design"]
    )
    
    timeline.add_range_event(
        "phase3", "Development",
        base + timedelta(days=7), base + timedelta(days=14),
        tags=["dev"]
    )
    
    timeline.add_range_event(
        "phase4", "Testing",
        base + timedelta(days=14), base + timedelta(days=18),
        tags=["qa"]
    )
    
    timeline.add_milestone(
        "m1", "Alpha Release",
        base + timedelta(days=18),
        tags=["release"]
    )
    
    timeline.add_range_event(
        "phase5", "Bug Fixes",
        base + timedelta(days=18), base + timedelta(days=21),
        tags=["fix"]
    )
    
    timeline.add_milestone(
        "m2", "Production Launch",
        base + timedelta(days=21),
        tags=["release", "production"]
    )
    
    # 渲染甘特图
    print(timeline.render_horizontal(width=60))
    
    # 统计
    print("\n--- Project Statistics ---")
    stats = timeline.statistics()
    print(f"Total phases: {stats['range_events']}")
    print(f"Milestones: {stats['milestones']}")
    print(f"Project duration: {format_duration(timeline.total_duration)}")
    print(f"Work density: {stats['density']:.1%}")
    
    # 按标签查找
    print("\n--- Release Milestones ---")
    releases = timeline.find_by_tag("release")
    for event in releases:
        print(f"  {event.name}: {event.start_time.strftime('%Y-%m-%d')}")


def example_history_timeline():
    """历史事件时间线示例"""
    print("\n" + "="*60)
    print("Example 5: Historical Events Timeline")
    print("="*60)
    
    timeline = Timeline("Technology Milestones")
    
    # 科技里程碑
    timeline.add_point_event(
        "phone", "First Telephone",
        datetime(1876, 3, 10),
        description="Alexander Graham Bell",
        tags=["communication"]
    )
    
    timeline.add_point_event(
        "light", "Electric Light Bulb",
        datetime(1879, 10, 22),
        description="Thomas Edison",
        tags=["energy"]
    )
    
    timeline.add_range_event(
        "ww1", "World War I",
        datetime(1914, 7, 28),
        datetime(1918, 11, 11),
        tags=["history"]
    )
    
    timeline.add_milestone(
        "tv", "First Television",
        datetime(1927, 9, 7),
        tags=["media"]
    )
    
    timeline.add_point_event(
        "internet", "ARPANET Launch",
        datetime(1969, 10, 29),
        tags=["internet", "computing"]
    )
    
    timeline.add_milestone(
        "moon", "Moon Landing",
        datetime(1969, 7, 20),
        description="Apollo 11",
        tags=["space"]
    )
    
    timeline.add_point_event(
        "web", "World Wide Web",
        datetime(1991, 8, 6),
        description="Tim Berners-Lee",
        tags=["internet", "web"]
    )
    
    timeline.add_milestone(
        "iphone", "iPhone Launch",
        datetime(2007, 1, 9),
        tags=["mobile", "apple"]
    )
    
    # 渲染
    print(timeline.render_ascii(width=80, compact=True))
    
    # 按类别查找
    print("\n--- Internet/Computing Events ---")
    tech_events = timeline.find_by_tag("internet")
    for event in tech_events:
        print(f"  {event.name}: {event.start_time.strftime('%Y-%m-%d')}")


def example_json_export():
    """JSON 导入导出示例"""
    print("\n" + "="*60)
    print("Example 6: JSON Export/Import")
    print("="*60)
    
    # 创建时间线
    timeline = Timeline("Event Schedule")
    
    base = datetime(2024, 1, 15, 10, 0)
    
    timeline.add_range_event("e1", "Workshop", base, base + timedelta(hours=2))
    timeline.add_point_event("p1", "Break", base + timedelta(hours=2))
    
    # 导出 JSON
    json_str = timeline.to_json()
    
    print("--- JSON Export ---")
    print(json_str)
    
    # 导入 JSON
    print("\n--- Import and Verify ---")
    restored = Timeline.from_json(json_str)
    print(f"Timeline name: {restored.name}")
    print(f"Events: {restored.count()}")
    for event in restored.events:
        print(f"  - {event.name}: {event.start_time.strftime('%H:%M')}")


def example_event_operations():
    """事件操作示例"""
    print("\n" + "="*60)
    print("Example 7: Event Operations")
    print("="*60)
    
    timeline = Timeline()
    
    base = datetime(2024, 1, 15, 9, 0)
    
    # 添加事件
    timeline.add_range_event("e1", "Long Event", base, base + timedelta(hours=4))
    print(f"Added event 'e1': {base.strftime('%H:%M')} - {(base + timedelta(hours=4)).strftime('%H:%M')}")
    
    # 分割事件
    print("\n--- Splitting Event ---")
    result = timeline.split_event("e1", base + timedelta(hours=2))
    if result:
        first, second = result
        print(f"Split into two events:")
        print(f"  {first.name}: {first.start_time.strftime('%H:%M')} - {first.end_time.strftime('%H:%M')}")
        print(f"  {second.name}: {second.start_time.strftime('%H:%M')} - {second.end_time.strftime('%H:%M')}")
    
    # 更新事件
    print("\n--- Updating Event ---")
    timeline.update_event("e1_1", name="First Half", description="Updated description")
    event = timeline.get_event("e1_1")
    print(f"Updated event: name='{event.name}', description='{event.description}'")
    
    # 删除事件
    print("\n--- Deleting Event ---")
    timeline.remove_event("e1_2")
    print(f"Events remaining: {timeline.count()}")


def example_time_range_query():
    """时间范围查询示例"""
    print("\n" + "="*60)
    print("Example 8: Time Range Query")
    print("="*60)
    
    timeline = Timeline("Weekly Events")
    
    base = datetime(2024, 1, 15, 9, 0)
    
    # 添加多天的事件
    timeline.add_range_event("day1", "Day 1 Work", base, base + timedelta(hours=8))
    timeline.add_range_event("day2", "Day 2 Work", base + timedelta(days=1), base + timedelta(days=1, hours=8))
    timeline.add_range_event("day3", "Day 3 Work", base + timedelta(days=2), base + timedelta(days=2, hours=8))
    timeline.add_point_event("special", "Special Event", base + timedelta(days=1, hours=12))
    
    # 查询特定天
    print("\n--- Events on Day 2 ---")
    day2_start = base + timedelta(days=1)
    day2_end = base + timedelta(days=2)
    
    events = timeline.get_events_in_range(day2_start, day2_end, include_overlapping=True)
    for event in events:
        print(f"  {event.name}: {event.start_time.strftime('%Y-%m-%d %H:%M')}")


def example_merge_events():
    """合并事件示例"""
    print("\n" + "="*60)
    print("Example 9: Merge Adjacent Events")
    print("="*60)
    
    timeline = Timeline()
    
    base = datetime(2024, 1, 15, 9, 0)
    
    # 添加相邻事件
    timeline.add_range_event("e1", "Task A", base, base + timedelta(hours=1))
    timeline.add_range_event("e2", "Task B", base + timedelta(hours=1), base + timedelta(hours=2))
    timeline.add_range_event("e3", "Task C", base + timedelta(hours=2), base + timedelta(hours=3))
    timeline.add_range_event("e4", "Break", base + timedelta(hours=4), base + timedelta(hours=5))
    
    print("--- Original Timeline ---")
    for event in timeline.events:
        print(f"  {event.name}: {event.start_time.strftime('%H:%M')}-{event.end_time.strftime('%H:%M')}")
    
    # 合合相邻事件
    print("\n--- Merged Timeline ---")
    merged = timeline.merge_adjacent(tolerance=timedelta(minutes=10))
    for event in merged:
        print(f"  {event.name}: {event.start_time.strftime('%H:%M')}-{event.end_time.strftime('%H:%M')}")


def run_all_examples():
    """运行所有示例"""
    examples = [
        example_basic_timeline,
        example_conflict_detection,
        example_gap_finding,
        example_project_schedule,
        example_history_timeline,
        example_json_export,
        example_event_operations,
        example_time_range_query,
        example_merge_events,
    ]
    
    for example in examples:
        example()
    
    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60)


if __name__ == "__main__":
    run_all_examples()