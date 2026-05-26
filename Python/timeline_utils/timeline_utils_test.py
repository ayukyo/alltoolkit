"""
Timeline Utils Test - 时间线工具测试

测试覆盖：
- 事件创建和验证
- 时间线管理（添加/删除/更新）
- 时间范围查询
- 重叠和相邻检测
- 间隙查找
- 统计信息
- ASCII 渲染
- JSON/CSV 导入导出
- 边界值测试
"""

import sys
import os

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from timeline_utils.mod import (
    Timeline, TimelineEvent, EventType,
    create_timeline, create_event, create_point_event,
    create_range_event, create_milestone,
    check_overlap, check_adjacent, format_duration
)


class TestResultCollector:
    """测试结果收集器"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def assert_true(self, condition, msg=""):
        if condition:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"Assertion failed: {msg}")
    
    def assert_equal(self, expected, actual, msg=""):
        if expected == actual:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"Expected {expected}, got {actual} - {msg}")
    
    def assert_raises(self, exception_type, func, msg=""):
        try:
            func()
            self.failed += 1
            self.errors.append(f"Expected {exception_type.__name__} - {msg}")
        except exception_type:
            self.passed += 1
        except Exception as e:
            self.failed += 1
            self.errors.append(f"Wrong exception: {e} - {msg}")
    
    def assert_not_none(self, value, msg=""):
        if value is not None:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"Expected not None - {msg}")
    
    def assert_none(self, value, msg=""):
        if value is None:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"Expected None, got {value} - {msg}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*50}")
        print(f"Tests: {total}, Passed: {self.passed}, Failed: {self.failed}")
        if self.errors:
            print("\nErrors:")
            for err in self.errors[:10]:  # 只显示前10个错误
                print(f"  - {err}")
        print(f"{'='*50}")
        return self.failed == 0


def test_event_creation():
    """测试事件创建"""
    collector = TestResultCollector()
    print("\n[Testing Event Creation]")
    
    # 测试瞬时事件
    event = create_point_event("e1", "Test", datetime(2024, 1, 1, 10, 0))
    collector.assert_equal("e1", event.id, "event id")
    collector.assert_equal("Test", event.name, "event name")
    collector.assert_equal(EventType.POINT, event.event_type, "event type")
    collector.assert_none(event.end_time, "point event should have no end_time")
    
    # 测试范围事件
    event = create_range_event(
        "e2", "Range",
        datetime(2024, 1, 1, 10, 0),
        datetime(2024, 1, 1, 12, 0)
    )
    collector.assert_equal(EventType.RANGE, event.event_type, "range event type")
    collector.assert_not_none(event.end_time, "range event should have end_time")
    collector.assert_equal(timedelta(hours=2), event.duration, "duration")
    
    # 测试里程碑
    event = create_milestone("m1", "Milestone", datetime(2024, 1, 1, 15, 0))
    collector.assert_equal(EventType.MILESTONE, event.event_type, "milestone type")
    
    # 测试无效事件（end_time < start_time）
    collector.assert_raises(
        ValueError,
        lambda: create_range_event(
            "e3", "Invalid",
            datetime(2024, 1, 1, 12, 0),
            datetime(2024, 1, 1, 10, 0)
        ),
        "invalid range event"
    )
    
    return collector.summary()


def test_event_properties():
    """测试事件属性"""
    collector = TestResultCollector()
    print("\n[Testing Event Properties]")
    
    start = datetime(2024, 1, 1, 10, 0)
    end = datetime(2024, 1, 1, 14, 30)
    
    event = create_range_event("e1", "Test Event", start, end)
    
    # 测试持续时间
    collector.assert_equal(timedelta(hours=4, minutes=30), event.duration, "duration")
    collector.assert_equal(270 * 60, event.duration_seconds, "duration seconds")
    collector.assert_equal(270, event.duration_minutes, "duration minutes")
    collector.assert_equal(4.5, event.duration_hours, "duration hours")
    
    # 测试 contains
    collector.assert_true(event.contains(datetime(2024, 1, 1, 11, 0)), "contains middle")
    collector.assert_true(event.contains(start), "contains start")
    collector.assert_true(event.contains(end), "contains end")
    collector.assert_true(not event.contains(datetime(2024, 1, 1, 9, 0)), "not contains before")
    collector.assert_true(not event.contains(datetime(2024, 1, 1, 15, 0)), "not contains after")
    
    # 测试瞬时事件 contains
    point = create_point_event("p1", "Point", datetime(2024, 1, 1, 10, 0))
    collector.assert_true(point.contains(datetime(2024, 1, 1, 10, 0)), "point contains exact")
    collector.assert_true(not point.contains(datetime(2024, 1, 1, 10, 1)), "point not contains other")
    
    return collector.summary()


def test_event_overlap():
    """测试事件重叠检测"""
    collector = TestResultCollector()
    print("\n[Testing Event Overlap]")
    
    base = datetime(2024, 1, 1, 10, 0)
    
    # 重叠情况
    e1 = create_range_event("e1", "Event 1", base, base + timedelta(hours=2))
    e2 = create_range_event("e2", "Event 2", base + timedelta(hours=1), base + timedelta(hours=3))
    collector.assert_true(e1.overlaps(e2), "overlapping events")
    collector.assert_true(e2.overlaps(e1), "overlap is symmetric")
    
    # 不重叠情况（有间隙）
    e3 = create_range_event("e3", "Event 3", base + timedelta(hours=3), base + timedelta(hours=4))
    collector.assert_true(not e1.overlaps(e3), "non-overlapping events")
    
    # 完全包含
    e4 = create_range_event("e4", "Event 4", base + timedelta(minutes=30), base + timedelta(hours=1))
    collector.assert_true(e1.overlaps(e4), "contained event overlaps")
    
    # 边界重叠（刚好相邻）
    e5 = create_range_event("e5", "Event 5", base + timedelta(hours=2), base + timedelta(hours=3))
    # 根据定义：start_time < other_end and other_start_time < end_time
    # e1: 10:00-12:00, e5: 12:00-13:00
    # 10:00 < 13:00 and 12:00 < 12:00? -> False
    collector.assert_true(not e1.overlaps(e5), "adjacent events not overlap")
    
    # 瞬时事件重叠
    p1 = create_point_event("p1", "Point 1", base + timedelta(hours=1))
    p2 = create_point_event("p2", "Point 2", base + timedelta(hours=1))
    collector.assert_true(p1.overlaps(p2), "same time point overlap")
    
    p3 = create_point_event("p3", "Point 3", base + timedelta(hours=2))
    collector.assert_true(not p1.overlaps(p3), "different time point not overlap")
    
    # 瞬时事件在范围内
    collector.assert_true(e1.overlaps(p1), "point in range overlaps")
    collector.assert_true(not e1.overlaps(p3), "point outside range not overlap")
    
    return collector.summary()


def test_event_adjacent():
    """测试事件相邻检测"""
    collector = TestResultCollector()
    print("\n[Testing Event Adjacent]")
    
    base = datetime(2024, 1, 1, 10, 0)
    
    e1 = create_range_event("e1", "Event 1", base, base + timedelta(hours=2))
    
    # 完全相邻
    e2 = create_range_event("e2", "Event 2", base + timedelta(hours=2), base + timedelta(hours=3))
    collector.assert_true(e1.adjacent(e2), "adjacent events")
    
    # 有小间隙（在容忍范围内）
    e3 = create_range_event("e3", "Event 3", base + timedelta(hours=2, minutes=1), base + timedelta(hours=3))
    collector.assert_true(e1.adjacent(e3, tolerance=timedelta(minutes=2)), "small gap within tolerance")
    collector.assert_true(not e1.adjacent(e3, tolerance=timedelta(seconds=30)), "small gap outside tolerance")
    
    # 有大间隙
    e4 = create_range_event("e4", "Event 4", base + timedelta(hours=4), base + timedelta(hours=5))
    collector.assert_true(not e1.adjacent(e4), "large gap not adjacent")
    
    return collector.summary()


def test_timeline_creation():
    """测试时间线创建"""
    collector = TestResultCollector()
    print("\n[Testing Timeline Creation]")
    
    timeline = create_timeline("Test Timeline")
    collector.assert_equal("Test Timeline", timeline.name, "timeline name")
    collector.assert_equal(0, timeline.count(), "empty timeline")
    
    return collector.summary()


def test_timeline_add_event():
    """测试添加事件"""
    collector = TestResultCollector()
    print("\n[Testing Timeline Add Event]")
    
    timeline = create_timeline()
    
    # 添加范围事件
    e1 = timeline.add_range_event(
        "e1", "Event 1",
        datetime(2024, 1, 1, 10, 0),
        datetime(2024, 1, 1, 12, 0)
    )
    collector.assert_equal(1, timeline.count(), "one event added")
    collector.assert_equal(e1, timeline.get_event("e1"), "event retrieved")
    
    # 添加瞬时事件
    e2 = timeline.add_point_event("p1", "Point", datetime(2024, 1, 1, 14, 0))
    collector.assert_equal(2, timeline.count(), "two events")
    
    # 添加里程碑
    e3 = timeline.add_milestone("m1", "Milestone", datetime(2024, 1, 1, 16, 0))
    collector.assert_equal(3, timeline.count(), "three events")
    
    # ID 重复应该报错
    collector.assert_raises(
        ValueError,
        lambda: timeline.add_point_event("e1", "Duplicate", datetime(2024, 1, 1, 18, 0)),
        "duplicate id"
    )
    
    return collector.summary()


def test_timeline_remove_event():
    """测试删除事件"""
    collector = TestResultCollector()
    print("\n[Testing Timeline Remove Event]")
    
    timeline = create_timeline()
    timeline.add_point_event("e1", "Event 1", datetime(2024, 1, 1, 10, 0))
    timeline.add_point_event("e2", "Event 2", datetime(2024, 1, 1, 11, 0))
    
    # 删除存在的
    collector.assert_true(timeline.remove_event("e1"), "remove existing event")
    collector.assert_equal(1, timeline.count(), "one event remaining")
    collector.assert_none(timeline.get_event("e1"), "removed event not found")
    
    # 删除不存在的
    collector.assert_true(not timeline.remove_event("e99"), "remove non-existing")
    
    return collector.summary()


def test_timeline_update_event():
    """测试更新事件"""
    collector = TestResultCollector()
    print("\n[Testing Timeline Update Event]")
    
    timeline = create_timeline()
    timeline.add_point_event("e1", "Old Name", datetime(2024, 1, 1, 10, 0))
    
    # 更新名称
    collector.assert_true(timeline.update_event("e1", name="New Name"), "update name")
    collector.assert_equal("New Name", timeline.get_event("e1").name, "name updated")
    
    # 更新不存在的
    collector.assert_true(not timeline.update_event("e99", name="Test"), "update non-existing")
    
    return collector.summary()


def test_timeline_time_range():
    """测试时间线时间范围"""
    collector = TestResultCollector()
    print("\n[Testing Timeline Time Range]")
    
    timeline = create_timeline()
    
    # 空时间线
    collector.assert_none(timeline.start_time, "empty start")
    collector.assert_none(timeline.end_time, "empty end")
    collector.assert_none(timeline.total_duration, "empty duration")
    
    # 添加事件
    timeline.add_range_event("e1", "Event 1", datetime(2024, 1, 1, 9, 0), datetime(2024, 1, 1, 12, 0))
    timeline.add_point_event("p1", "Point", datetime(2024, 1, 1, 15, 0))
    
    collector.assert_equal(datetime(2024, 1, 1, 9, 0), timeline.start_time, "start time")
    collector.assert_equal(datetime(2024, 1, 1, 15, 0), timeline.end_time, "end time")
    collector.assert_equal(timedelta(hours=6), timeline.total_duration, "total duration")
    
    return collector.summary()


def test_timeline_get_events_in_range():
    """测试获取时间范围内事件"""
    collector = TestResultCollector()
    print("\n[Testing Get Events In Range]")
    
    timeline = create_timeline()
    base = datetime(2024, 1, 1, 9, 0)
    
    timeline.add_range_event("e1", "Event 1", base, base + timedelta(hours=2))
    timeline.add_range_event("e2", "Event 2", base + timedelta(hours=3), base + timedelta(hours=5))
    timeline.add_point_event("p1", "Point", base + timedelta(hours=6))
    
    # 完全在范围内的
    events = timeline.get_events_in_range(base, base + timedelta(hours=2), include_overlapping=False)
    collector.assert_equal(1, len(events), "one event fully in range")
    collector.assert_equal("e1", events[0].id, "correct event")
    
    # 部分重叠的（include_overlapping=True）
    events = timeline.get_events_in_range(base + timedelta(hours=1), base + timedelta(hours=4), include_overlapping=True)
    collector.assert_equal(2, len(events), "two overlapping events")
    
    # 部分重叠的（include_overlapping=False）
    events = timeline.get_events_in_range(base + timedelta(hours=1), base + timedelta(hours=4), include_overlapping=False)
    collector.assert_equal(0, len(events), "no fully contained events")
    
    return collector.summary()


def test_timeline_find():
    """测试查找功能"""
    collector = TestResultCollector()
    print("\n[Testing Timeline Find]")
    
    timeline = create_timeline()
    base = datetime(2024, 1, 1, 9, 0)
    
    timeline.add_range_event("e1", "Meeting", base, base + timedelta(hours=1), tags=["work", "meeting"])
    timeline.add_range_event("e2", "Lunch", base + timedelta(hours=1), base + timedelta(hours=2), tags=["personal"])
    timeline.add_range_event("e3", "Workshop", base + timedelta(hours=2), base + timedelta(hours=3), tags=["work", "training"])
    
    # 按标签查找
    events = timeline.find_by_tag("work")
    collector.assert_equal(2, len(events), "two work events")
    
    # 按名称模式查找
    events = timeline.find_by_name("Meet")
    collector.assert_equal(1, len(events), "one meeting")
    
    # 按时间点查找
    events = timeline.get_events_at(base + timedelta(minutes=30))
    collector.assert_equal(1, len(events), "one event at time")
    
    return collector.summary()


def test_timeline_overlaps():
    """测试时间线重叠检测"""
    collector = TestResultCollector()
    print("\n[Testing Timeline Overlaps]")
    
    timeline = create_timeline()
    base = datetime(2024, 1, 1, 9, 0)
    
    # 无重叠
    timeline.add_range_event("e1", "Event 1", base, base + timedelta(hours=1))
    timeline.add_range_event("e2", "Event 2", base + timedelta(hours=1), base + timedelta(hours=2))
    overlaps = timeline.find_overlaps()
    collector.assert_equal(0, len(overlaps), "no overlaps")
    collector.assert_true(not timeline.has_conflicts(), "no conflicts")
    
    # 有重叠
    timeline.add_range_event("e3", "Event 3", base + timedelta(minutes=30), base + timedelta(hours=2))
    overlaps = timeline.find_overlaps()
    collector.assert_equal(2, len(overlaps), "two overlapping pairs")
    collector.assert_true(timeline.has_conflicts(), "has conflicts")
    
    return collector.summary()


def test_timeline_gaps():
    """测试间隙查找"""
    collector = TestResultCollector()
    print("\n[Testing Timeline Gaps]")
    
    timeline = create_timeline()
    base = datetime(2024, 1, 1, 9, 0)
    
    timeline.add_range_event("e1", "Event 1", base, base + timedelta(hours=1))
    timeline.add_range_event("e2", "Event 2", base + timedelta(hours=2), base + timedelta(hours=3))
    timeline.add_range_event("e3", "Event 3", base + timedelta(hours=4), base + timedelta(hours=5))
    
    # 有间隙
    gaps = timeline.find_gaps(min_gap=timedelta(minutes=1))
    collector.assert_equal(2, len(gaps), "two gaps")
    
    # 间隙时间
    collector.assert_equal(timedelta(hours=1), gaps[0][1] - gaps[0][0], "1 hour gap")
    
    # 无间隙（调整阈值）
    gaps = timeline.find_gaps(min_gap=timedelta(hours=2))
    collector.assert_equal(0, len(gaps), "no large gaps")
    
    return collector.summary()


def test_timeline_merge():
    """测试合并相邻事件"""
    collector = TestResultCollector()
    print("\n[Testing Timeline Merge]")
    
    timeline = create_timeline()
    base = datetime(2024, 1, 1, 9, 0)
    
    timeline.add_range_event("e1", "Event 1", base, base + timedelta(hours=1))
    timeline.add_range_event("e2", "Event 2", base + timedelta(hours=1), base + timedelta(hours=2))
    timeline.add_range_event("e3", "Event 3", base + timedelta(hours=4), base + timedelta(hours=5))
    
    merged = timeline.merge_adjacent(tolerance=timedelta(minutes=5))
    collector.assert_equal(2, len(merged), "two merged events")
    
    # 第一个合并事件覆盖 e1 和 e2
    collector.assert_equal(base, merged[0].start_time, "merged start")
    collector.assert_equal(base + timedelta(hours=2), merged[0].end_time, "merged end")
    
    return collector.summary()


def test_timeline_split():
    """测试分割事件"""
    collector = TestResultCollector()
    print("\n[Testing Timeline Split]")
    
    timeline = create_timeline()
    base = datetime(2024, 1, 1, 9, 0)
    
    timeline.add_range_event("e1", "Long Event", base, base + timedelta(hours=4))
    
    # 在中间分割
    result = timeline.split_event("e1", base + timedelta(hours=2))
    collector.assert_not_none(result, "split succeeded")
    collector.assert_equal(2, timeline.count(), "two events after split")
    
    # 验证分割后的事件
    first, second = result
    collector.assert_equal(base, first.start_time, "first start")
    collector.assert_equal(base + timedelta(hours=2), first.end_time, "first end")
    collector.assert_equal(base + timedelta(hours=2), second.start_time, "second start")
    collector.assert_equal(base + timedelta(hours=4), second.end_time, "second end")
    
    # 分割不存在的
    result = timeline.split_event("e99", base + timedelta(hours=1))
    collector.assert_none(result, "split non-existing")
    
    return collector.summary()


def test_timeline_statistics():
    """测试统计信息"""
    collector = TestResultCollector()
    print("\n[Testing Timeline Statistics]")
    
    timeline = create_timeline()
    base = datetime(2024, 1, 1, 9, 0)
    
    # 空时间线
    stats = timeline.statistics()
    collector.assert_equal(0, stats["total_events"], "empty stats")
    
    # 有事件
    timeline.add_range_event("e1", "Event 1", base, base + timedelta(hours=2))
    timeline.add_point_event("p1", "Point", base + timedelta(hours=3))
    timeline.add_milestone("m1", "Milestone", base + timedelta(hours=4))
    
    stats = timeline.statistics()
    collector.assert_equal(3, stats["total_events"], "three events")
    collector.assert_equal(1, stats["point_events"], "one point")
    collector.assert_equal(1, stats["range_events"], "one range")
    collector.assert_equal(1, stats["milestones"], "one milestone")
    
    # 持续时间统计
    collector.assert_equal(7200, stats["total_event_duration_seconds"], "2 hours duration")
    
    return collector.summary()


def test_timeline_render():
    """测试渲染"""
    collector = TestResultCollector()
    print("\n[Testing Timeline Render]")
    
    timeline = create_timeline()
    base = datetime(2024, 1, 1, 9, 0)
    
    timeline.add_range_event("e1", "Event 1", base, base + timedelta(hours=2))
    timeline.add_point_event("p1", "Point", base + timedelta(hours=3))
    
    # ASCII 渲染
    ascii_str = timeline.render_ascii(width=60)
    collector.assert_true(len(ascii_str) > 0, "ascii output")
    collector.assert_true("Event 1" in ascii_str, "event name in output")
    collector.assert_true("Point" in ascii_str, "point name in output")
    
    # 水平渲染
    horiz_str = timeline.render_horizontal(width=50)
    collector.assert_true(len(horiz_str) > 0, "horizontal output")
    
    return collector.summary()


def test_timeline_json_export():
    """测试 JSON 导入导出"""
    collector = TestResultCollector()
    print("\n[Testing Timeline JSON Export]")
    
    timeline = create_timeline("Test")
    base = datetime(2024, 1, 1, 9, 0)
    
    timeline.add_range_event("e1", "Event 1", base, base + timedelta(hours=1), tags=["test"])
    timeline.add_point_event("p1", "Point", base + timedelta(hours=2))
    
    # 导出
    json_str = timeline.to_json()
    collector.assert_true(len(json_str) > 0, "json output")
    collector.assert_true("Event 1" in json_str, "event in json")
    
    # 导入
    restored = Timeline.from_json(json_str)
    collector.assert_equal(2, restored.count(), "restored events")
    collector.assert_equal("Event 1", restored.get_event("e1").name, "restored name")
    
    return collector.summary()


def test_timeline_csv_export():
    """测试 CSV 导入导出"""
    collector = TestResultCollector()
    print("\n[Testing Timeline CSV Export]")
    
    timeline = create_timeline()
    base = datetime(2024, 1, 1, 9, 0)
    
    timeline.add_range_event("e1", "Event 1", base, base + timedelta(hours=1), tags=["work"])
    timeline.add_point_event("p1", "Point", base + timedelta(hours=2))
    
    # 导出
    csv_str = timeline.to_csv()
    collector.assert_true(len(csv_str) > 0, "csv output")
    collector.assert_true("Event 1" in csv_str, "event in csv")
    
    # 导入
    restored = Timeline.from_csv(csv_str)
    collector.assert_equal(2, restored.count(), "restored events")
    
    return collector.summary()


def test_event_to_dict():
    """测试事件序列化"""
    collector = TestResultCollector()
    print("\n[Testing Event To Dict]")
    
    base = datetime(2024, 1, 1, 9, 0)
    event = create_range_event(
        "e1", "Test",
        base, base + timedelta(hours=1),
        description="Test event",
        tags=["a", "b"]
    )
    
    d = event.to_dict()
    collector.assert_equal("e1", d["id"], "id in dict")
    collector.assert_equal("Test", d["name"], "name in dict")
    collector.assert_equal("range", d["event_type"], "type in dict")
    collector.assert_equal(["a", "b"], d["tags"], "tags in dict")
    
    # 反序列化
    restored = TimelineEvent.from_dict(d)
    collector.assert_equal(event.id, restored.id, "restored id")
    collector.assert_equal(event.name, restored.name, "restored name")
    
    return collector.summary()


def test_format_duration():
    """测试持续时间格式化"""
    collector = TestResultCollector()
    print("\n[Testing Format Duration]")
    
    collector.assert_equal("30s", format_duration(timedelta(seconds=30)), "seconds")
    collector.assert_equal("5min", format_duration(timedelta(minutes=5)), "minutes")
    collector.assert_equal("5min 30s", format_duration(timedelta(minutes=5, seconds=30)), "minutes+seconds")
    collector.assert_equal("2h", format_duration(timedelta(hours=2)), "hours")
    collector.assert_equal("2h 30min", format_duration(timedelta(hours=2, minutes=30)), "hours+minutes")
    collector.assert_equal("1d", format_duration(timedelta(days=1)), "days")
    collector.assert_equal("2d 5h", format_duration(timedelta(days=2, hours=5)), "days+hours")
    
    return collector.summary()


def test_convenience_functions():
    """测试便捷函数"""
    collector = TestResultCollector()
    print("\n[Testing Convenience Functions]")
    
    base = datetime(2024, 1, 1, 10, 0)
    
    # check_overlap
    e1 = create_range_event("e1", "E1", base, base + timedelta(hours=2))
    e2 = create_range_event("e2", "E2", base + timedelta(hours=1), base + timedelta(hours=3))
    collector.assert_true(check_overlap(e1, e2), "overlap check")
    
    # check_adjacent
    e3 = create_range_event("e3", "E3", base + timedelta(hours=2), base + timedelta(hours=3))
    collector.assert_true(check_adjacent(e1, e3), "adjacent check")
    
    return collector.summary()


def test_edge_cases():
    """测试边界值"""
    collector = TestResultCollector()
    print("\n[Testing Edge Cases]")
    
    # 零持续时间事件
    base = datetime(2024, 1, 1, 10, 0)
    e = create_range_event("e1", "Zero", base, base)
    collector.assert_equal(timedelta(0), e.duration, "zero duration")
    
    # 单事件时间线
    timeline = create_timeline()
    timeline.add_point_event("e1", "Solo", base)
    collector.assert_equal(base, timeline.start_time, "single event start")
    collector.assert_equal(base, timeline.end_time, "single event end")
    
    # 大时间跨度
    timeline2 = create_timeline()
    timeline2.add_range_event("e1", "Long", base, base + timedelta(days=365))
    collector.assert_equal(timedelta(days=365), timeline2.total_duration, "year duration")
    
    # 同一时间多个事件
    timeline3 = create_timeline()
    timeline3.add_point_event("e1", "P1", base)
    timeline3.add_point_event("e2", "P2", base)
    timeline3.add_point_event("e3", "P3", base)
    events = timeline3.get_events_at(base)
    collector.assert_equal(3, len(events), "three events at same time")
    
    # 空字符串名称
    e = create_point_event("e1", "", base)
    collector.assert_equal("", e.name, "empty name allowed")
    
    # 空标签列表
    e = create_point_event("e2", "Test", base, tags=[])
    collector.assert_equal([], e.tags, "empty tags")
    
    return collector.summary()


def run_all_tests():
    """运行所有测试"""
    tests = [
        test_event_creation,
        test_event_properties,
        test_event_overlap,
        test_event_adjacent,
        test_timeline_creation,
        test_timeline_add_event,
        test_timeline_remove_event,
        test_timeline_update_event,
        test_timeline_time_range,
        test_timeline_get_events_in_range,
        test_timeline_find,
        test_timeline_overlaps,
        test_timeline_gaps,
        test_timeline_merge,
        test_timeline_split,
        test_timeline_statistics,
        test_timeline_render,
        test_timeline_json_export,
        test_timeline_csv_export,
        test_event_to_dict,
        test_format_duration,
        test_convenience_functions,
        test_edge_cases,
    ]
    
    all_passed = True
    for test in tests:
        if not test():
            all_passed = False
    
    return all_passed


if __name__ == "__main__":
    print("="*60)
    print("Timeline Utils Test Suite")
    print("="*60)
    
    success = run_all_tests()
    
    if success:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")