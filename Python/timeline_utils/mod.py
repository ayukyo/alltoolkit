"""
Timeline Utils - 时间线管理工具库

功能：
- 时间线创建和管理：支持多个事件、时间范围
- 事件操作：添加、删除、更新、排序、合并
- 时间线可视化：ASCII 格式渲染，支持紧凑/详细模式
- 时间范围查询：查找特定时间范围内的事件
- 事件冲突检测：检测重叠、相邻事件
- 时间线统计：持续时间、密度、间隙分析
- 数据导入导出：JSON、CSV 格式支持
- 零外部依赖，纯 Python 标准库实现

使用场景：
- 项目进度管理
- 会议日程安排
- 历史事件时间线
- 日程冲突检测
- 任务追踪
"""

from typing import List, Dict, Any, Optional, Tuple, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import json
import re

# Python 3.6 兼容的 datetime 解析
def _parse_datetime(dt_str: str) -> datetime:
    """解析 ISO 格式的 datetime 字符串"""
    if not dt_str:
        return None
    # 尝试解析各种 ISO 格式
    # 格式: YYYY-MM-DDTHH:MM:SS 或 YYYY-MM-DD HH:MM:SS
    for fmt in [
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%dT%H:%M:%S.%f',
        '%Y-%m-%d %H:%M:%S.%f',
    ]:
        try:
            return datetime.strptime(dt_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Cannot parse datetime: {dt_str}")


class EventType(Enum):
    """事件类型枚举"""
    POINT = "point"      # 瞬时事件（无持续时间）
    RANGE = "range"      # 时间范围事件
    MILESTONE = "milestone"  # 里程碑事件


@dataclass
class TimelineEvent:
    """时间线事件"""
    id: str
    name: str
    start_time: datetime
    end_time: Optional[datetime] = None  # None 表示瞬时事件
    event_type: EventType = EventType.POINT
    description: str = ""
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """验证事件数据"""
        if self.event_type == EventType.RANGE:
            if self.end_time is None:
                raise ValueError("Range event must have end_time")
            if self.end_time < self.start_time:
                raise ValueError("end_time must be >= start_time")
    
    @property
    def duration(self) -> Optional[timedelta]:
        """获取事件持续时间"""
        if self.end_time is None:
            return None
        return self.end_time - self.start_time
    
    @property
    def duration_seconds(self) -> Optional[float]:
        """获取持续时间（秒）"""
        if self.duration is None:
            return None
        return self.duration.total_seconds()
    
    @property
    def duration_minutes(self) -> Optional[float]:
        """获取持续时间（分钟）"""
        if self.duration_seconds is None:
            return None
        return self.duration_seconds / 60
    
    @property
    def duration_hours(self) -> Optional[float]:
        """获取持续时间（小时）"""
        if self.duration_minutes is None:
            return None
        return self.duration_minutes / 60
    
    def contains(self, time: datetime) -> bool:
        """检查指定时间是否在事件范围内"""
        if self.event_type == EventType.POINT:
            return time == self.start_time
        if self.end_time is None:
            return False
        return self.start_time <= time <= self.end_time
    
    def overlaps(self, other: 'TimelineEvent') -> bool:
        """检查是否与另一事件重叠"""
        if self.event_type == EventType.POINT and other.event_type == EventType.POINT:
            return self.start_time == other.start_time
        
        # 获取各自的结束时间
        self_end = self.end_time or self.start_time
        other_end = other.end_time or other.start_time
        
        return self.start_time < other_end and other.start_time < self_end
    
    def adjacent(self, other: 'TimelineEvent', tolerance: timedelta = timedelta(minutes=1)) -> bool:
        """检查是否与另一事件相邻"""
        self_end = self.end_time or self.start_time
        other_end = other.end_time or other.start_time
        
        # self 结束后紧跟 other 开始，或 vice versa
        gap1 = abs(other.start_time - self_end)
        gap2 = abs(self.start_time - other_end)
        
        return gap1 <= tolerance or gap2 <= tolerance
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "event_type": self.event_type.value,
            "description": self.description,
            "tags": self.tags,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TimelineEvent':
        """从字典创建"""
        return cls(
            id=data["id"],
            name=data["name"],
            start_time=_parse_datetime(data["start_time"]),
            end_time=_parse_datetime(data["end_time"]) if data.get("end_time") else None,
            event_type=EventType(data.get("event_type", "point")),
            description=data.get("description", ""),
            tags=data.get("tags", []),
            metadata=data.get("metadata", {})
        )


class Timeline:
    """时间线管理器"""
    
    def __init__(self, name: str = "Timeline"):
        self.name = name
        self.events: List[TimelineEvent] = []
    
    def add_event(self, event: TimelineEvent) -> None:
        """添加事件"""
        # 检查 ID 重复
        if any(e.id == event.id for e in self.events):
            raise ValueError(f"Event ID '{event.id}' already exists")
        self.events.append(event)
        self._sort_events()
    
    def add_point_event(
        self,
        id: str,
        name: str,
        time: datetime,
        description: str = "",
        tags: List[str] = [],
        metadata: Dict[str, Any] = {}
    ) -> TimelineEvent:
        """添加瞬时事件"""
        event = TimelineEvent(
            id=id,
            name=name,
            start_time=time,
            event_type=EventType.POINT,
            description=description,
            tags=tags,
            metadata=metadata
        )
        self.add_event(event)
        return event
    
    def add_range_event(
        self,
        id: str,
        name: str,
        start_time: datetime,
        end_time: datetime,
        description: str = "",
        tags: List[str] = [],
        metadata: Dict[str, Any] = {}
    ) -> TimelineEvent:
        """添加时间范围事件"""
        event = TimelineEvent(
            id=id,
            name=name,
            start_time=start_time,
            end_time=end_time,
            event_type=EventType.RANGE,
            description=description,
            tags=tags,
            metadata=metadata
        )
        self.add_event(event)
        return event
    
    def add_milestone(
        self,
        id: str,
        name: str,
        time: datetime,
        description: str = "",
        tags: List[str] = [],
        metadata: Dict[str, Any] = {}
    ) -> TimelineEvent:
        """添加里程碑"""
        event = TimelineEvent(
            id=id,
            name=name,
            start_time=time,
            event_type=EventType.MILESTONE,
            description=description,
            tags=tags,
            metadata=metadata
        )
        self.add_event(event)
        return event
    
    def remove_event(self, event_id: str) -> bool:
        """删除事件"""
        for i, event in enumerate(self.events):
            if event.id == event_id:
                self.events.pop(i)
                return True
        return False
    
    def get_event(self, event_id: str) -> Optional[TimelineEvent]:
        """获取事件"""
        for event in self.events:
            if event.id == event_id:
                return event
        return None
    
    def update_event(self, event_id: str, **kwargs) -> bool:
        """更新事件属性"""
        event = self.get_event(event_id)
        if event is None:
            return False
        
        for key, value in kwargs.items():
            if hasattr(event, key):
                setattr(event, key, value)
        
        # 重新验证
        event.__post_init__()
        self._sort_events()
        return True
    
    def _sort_events(self) -> None:
        """按开始时间排序事件"""
        self.events.sort(key=lambda e: e.start_time)
    
    def clear(self) -> None:
        """清空所有事件"""
        self.events.clear()
    
    @property
    def start_time(self) -> Optional[datetime]:
        """获取时间线开始时间"""
        if not self.events:
            return None
        return min(e.start_time for e in self.events)
    
    @property
    def end_time(self) -> Optional[datetime]:
        """获取时间线结束时间"""
        if not self.events:
            return None
        ends = [e.end_time or e.start_time for e in self.events]
        return max(ends)
    
    @property
    def total_duration(self) -> Optional[timedelta]:
        """获取时间线总跨度"""
        if self.start_time is None or self.end_time is None:
            return None
        return self.end_time - self.start_time
    
    def count(self) -> int:
        """获取事件总数"""
        return len(self.events)
    
    def count_by_type(self, event_type: EventType) -> int:
        """按类型计数"""
        return sum(1 for e in self.events if e.event_type == event_type)
    
    def get_events_in_range(
        self,
        start: datetime,
        end: datetime,
        include_overlapping: bool = True
    ) -> List[TimelineEvent]:
        """获取指定时间范围内的事件"""
        result = []
        for event in self.events:
            event_end = event.end_time or event.start_time
            
            if include_overlapping:
                # 包含任何与范围有交集的事件
                if event.start_time <= end and event_end >= start:
                    result.append(event)
            else:
                # 只包含完全在范围内的事件
                if event.start_time >= start and event_end <= end:
                    result.append(event)
        
        return result
    
    def get_events_at(self, time: datetime) -> List[TimelineEvent]:
        """获取指定时间点的事件"""
        return [e for e in self.events if e.contains(time)]
    
    def find_by_tag(self, tag: str) -> List[TimelineEvent]:
        """按标签查找事件"""
        return [e for e in self.events if tag in e.tags]
    
    def find_by_name(self, name_pattern: str) -> List[TimelineEvent]:
        """按名称模式查找事件（支持正则）"""
        pattern = re.compile(name_pattern, re.IGNORECASE)
        return [e for e in self.events if pattern.search(e.name)]
    
    def find_overlaps(self) -> List[Tuple[TimelineEvent, TimelineEvent]]:
        """查找所有重叠的事件对"""
        overlaps = []
        for i, e1 in enumerate(self.events):
            for e2 in self.events[i+1:]:
                if e1.overlaps(e2):
                    overlaps.append((e1, e2))
        return overlaps
    
    def find_gaps(self, min_gap: timedelta = timedelta(minutes=1)) -> List[Tuple[datetime, datetime]]:
        """查找时间线中的间隙"""
        if len(self.events) < 2:
            return []
        
        gaps = []
        for i in range(len(self.events) - 1):
            e1 = self.events[i]
            e2 = self.events[i + 1]
            
            e1_end = e1.end_time or e1.start_time
            
            gap = e2.start_time - e1_end
            if gap >= min_gap:
                gaps.append((e1_end, e2.start_time))
        
        return gaps
    
    def has_conflicts(self) -> bool:
        """检查是否有冲突（重叠）"""
        return len(self.find_overlaps()) > 0
    
    def merge_adjacent(
        self,
        tolerance: timedelta = timedelta(minutes=5),
        merged_name: str = "Merged Event"
    ) -> List[TimelineEvent]:
        """合并相邻事件"""
        if not self.events:
            return []
        
        merged = []
        current_group = [self.events[0]]
        
        for i in range(1, len(self.events)):
            prev = self.events[i - 1]
            curr = self.events[i]
            
            if prev.adjacent(curr, tolerance):
                current_group.append(curr)
            else:
                # 完成当前组
                if len(current_group) > 1:
                    merged_event = TimelineEvent(
                        id=f"merged_{len(merged)}",
                        name=merged_name,
                        start_time=min(e.start_time for e in current_group),
                        end_time=max(e.end_time or e.start_time for e in current_group),
                        event_type=EventType.RANGE,
                        description=f"Merged from {len(current_group)} events",
                        tags=list(set(t for e in current_group for t in e.tags))
                    )
                    merged.append(merged_event)
                else:
                    merged.append(current_group[0])
                
                current_group = [curr]
        
        # 处理最后一组
        if len(current_group) > 1:
            merged_event = TimelineEvent(
                id=f"merged_{len(merged)}",
                name=merged_name,
                start_time=min(e.start_time for e in current_group),
                end_time=max(e.end_time or e.start_time for e in current_group),
                event_type=EventType.RANGE,
                description=f"Merged from {len(current_group)} events"
            )
            merged.append(merged_event)
        else:
            merged.append(current_group[0])
        
        return merged
    
    def split_event(
        self,
        event_id: str,
        split_time: datetime,
        first_id: str = None,
        second_id: str = None
    ) -> Optional[Tuple[TimelineEvent, TimelineEvent]]:
        """在指定时间点分割事件"""
        event = self.get_event(event_id)
        if event is None:
            return None
        
        if event.event_type != EventType.RANGE:
            return None
        
        if split_time <= event.start_time or split_time >= event.end_time:
            return None
        
        first_id = first_id or f"{event_id}_1"
        second_id = second_id or f"{event_id}_2"
        
        first = TimelineEvent(
            id=first_id,
            name=event.name,
            start_time=event.start_time,
            end_time=split_time,
            event_type=EventType.RANGE,
            description=event.description,
            tags=event.tags.copy(),
            metadata=event.metadata.copy()
        )
        
        second = TimelineEvent(
            id=second_id,
            name=event.name,
            start_time=split_time,
            end_time=event.end_time,
            event_type=EventType.RANGE,
            description=event.description,
            tags=event.tags.copy(),
            metadata=event.metadata.copy()
        )
        
        # 删除原事件，添加新事件
        self.remove_event(event_id)
        self.add_event(first)
        self.add_event(second)
        
        return (first, second)
    
    def statistics(self) -> Dict[str, Any]:
        """获取时间线统计信息"""
        if not self.events:
            return {
                "total_events": 0,
                "point_events": 0,
                "range_events": 0,
                "milestones": 0,
                "total_duration": None,
                "total_event_duration": 0,
                "density": 0,
                "gaps": 0,
                "overlaps": 0
            }
        
        point_count = self.count_by_type(EventType.POINT)
        range_count = self.count_by_type(EventType.RANGE)
        milestone_count = self.count_by_type(EventType.MILESTONE)
        
        # 计算事件总持续时间
        total_event_duration = timedelta()
        for e in self.events:
            if e.duration:
                total_event_duration += e.duration
        
        # 计算密度（事件时间占比）
        if self.total_duration and self.total_duration.total_seconds() > 0:
            density = total_event_duration.total_seconds() / self.total_duration.total_seconds()
        else:
            density = 0
        
        return {
            "total_events": len(self.events),
            "point_events": point_count,
            "range_events": range_count,
            "milestones": milestone_count,
            "total_duration_seconds": self.total_duration.total_seconds() if self.total_duration else 0,
            "total_event_duration_seconds": total_event_duration.total_seconds(),
            "density": density,
            "gaps": len(self.find_gaps()),
            "overlaps": len(self.find_overlaps()),
            "tags": list(set(t for e in self.events for t in e.tags))
        }
    
    def render_ascii(
        self,
        width: int = 80,
        show_time: bool = True,
        compact: bool = False,
        highlight_overlaps: bool = True
    ) -> str:
        """渲染 ASCII 时间线"""
        if not self.events:
            return "(empty timeline)"
        
        start = self.start_time
        end = self.end_time
        total_seconds = (end - start).total_seconds()
        
        if total_seconds <= 0:
            return "(invalid timeline)"
        
        lines = []
        lines.append(f"Timeline: {self.name}")
        lines.append("=" * width)
        
        if show_time:
            lines.append(f"Start: {start.strftime('%Y-%m-%d %H:%M')}")
            lines.append(f"End: {end.strftime('%Y-%m-%d %H:%M')}")
            lines.append("")
        
        # 检测重叠
        overlaps = self.find_overlaps() if highlight_overlaps else []
        overlapping_ids = set()
        for e1, e2 in overlaps:
            overlapping_ids.add(e1.id)
            overlapping_ids.add(e2.id)
        
        # 渲染每个事件
        for event in self.events:
            event_end = event.end_time or event.start_time
            
            # 计算位置
            start_pos = int((event.start_time - start).total_seconds() / total_seconds * (width - 10))
            end_pos = int((event_end - start).total_seconds() / total_seconds * (width - 10))
            
            start_pos = max(0, min(width - 10, start_pos))
            end_pos = max(start_pos, min(width - 10, end_pos))
            
            # 构建条形
            bar_length = max(1, end_pos - start_pos)
            
            if event.event_type == EventType.POINT:
                marker = "●"
            elif event.event_type == EventType.MILESTONE:
                marker = "◆"
            else:
                marker = "━" * bar_length
            
            # 高亮重叠
            if event.id in overlapping_ids:
                marker = f"!{marker}!"
            
            if compact:
                time_str = event.start_time.strftime('%H:%M')
                line = f"{time_str} {marker} {event.name[:20]}"
            else:
                time_str = f"{event.start_time.strftime('%H:%M')}"
                if event.end_time:
                    time_str += f" - {event.end_time.strftime('%H:%M')}"
                duration_str = ""
                if event.duration:
                    duration_str = f" ({event.duration_minutes:.0f}min)"
                line = f"{time_str} {marker} {event.name}{duration_str}"
                if event.description:
                    lines.append(f"         └─ {event.description[:40]}")
                if event.tags:
                    lines.append(f"         └─ Tags: {', '.join(event.tags)}")
            
            lines.append(line)
        
        return "\n".join(lines)
    
    def render_horizontal(
        self,
        width: int = 60,
        row_height: int = 1
    ) -> str:
        """渲染水平时间线（甘特图风格）"""
        if not self.events:
            return "(empty timeline)"
        
        start = self.start_time
        end = self.end_time
        total_seconds = (end - start).total_seconds()
        
        if total_seconds <= 0:
            return "(invalid timeline)"
        
        lines = []
        
        # 时间轴
        time_axis = "│" + "─" * width + "│"
        time_labels = f"{start.strftime('%H:%M')}" + " " * (width - 14) + f"{end.strftime('%H:%M')}"
        
        lines.append(time_labels)
        lines.append(time_axis)
        
        # 每个事件一行
        for event in self.events:
            event_end = event.end_time or event.start_time
            
            # 计算位置
            start_pos = int((event.start_time - start).total_seconds() / total_seconds * width)
            end_pos = int((event_end - start).total_seconds() / total_seconds * width)
            
            start_pos = max(0, min(width, start_pos))
            end_pos = max(start_pos + 1, min(width, end_pos))
            
            # 构建行
            prefix = "│" + " " * start_pos
            
            if event.event_type == EventType.POINT:
                bar = "●"
            elif event.event_type == EventType.MILESTONE:
                bar = "◆"
            else:
                bar = "█" * (end_pos - start_pos)
            
            suffix = " " * (width - end_pos) + "│"
            
            line = prefix + bar + suffix + f" {event.name[:15]}"
            lines.append(line)
        
        lines.append(time_axis)
        
        return "\n".join(lines)
    
    def to_json(self) -> str:
        """导出为 JSON"""
        data = {
            "name": self.name,
            "events": [e.to_dict() for e in self.events]
        }
        return json.dumps(data, indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Timeline':
        """从 JSON 导入"""
        data = json.loads(json_str)
        timeline = cls(name=data.get("name", "Timeline"))
        for event_data in data.get("events", []):
            event = TimelineEvent.from_dict(event_data)
            timeline.events.append(event)
        timeline._sort_events()
        return timeline
    
    def to_csv(self) -> str:
        """导出为 CSV"""
        lines = ["id,name,start_time,end_time,event_type,description,tags"]
        for event in self.events:
            tags_str = ";".join(event.tags)
            end_time_str = event.end_time.isoformat() if event.end_time else ""
            lines.append(f"{event.id},{event.name},{event.start_time.isoformat()},{end_time_str},{event.event_type.value},{event.description},{tags_str}")
        return "\n".join(lines)
    
    @classmethod
    def from_csv(cls, csv_str: str) -> 'Timeline':
        """从 CSV 导入"""
        lines = csv_str.strip().split("\n")
        if len(lines) < 2:
            return cls()
        
        timeline = cls()
        for line in lines[1:]:
            parts = line.split(",")
            if len(parts) >= 5:
                event = TimelineEvent(
                    id=parts[0],
                    name=parts[1],
                    start_time=_parse_datetime(parts[2]),
                    end_time=_parse_datetime(parts[3]) if parts[3] else None,
                    event_type=EventType(parts[4]),
                    description=parts[5] if len(parts) > 5 else "",
                    tags=parts[6].split(";") if len(parts) > 6 and parts[6] else []
                )
                timeline.events.append(event)
        
        timeline._sort_events()
        return timeline
    
    def __repr__(self) -> str:
        return f"Timeline(name='{self.name}', events={len(self.events)})"


# 便捷函数

def create_timeline(name: str = "Timeline") -> Timeline:
    """创建时间线"""
    return Timeline(name)


def create_event(
    id: str,
    name: str,
    start_time: datetime,
    end_time: Optional[datetime] = None,
    event_type: EventType = EventType.POINT,
    description: str = "",
    tags: List[str] = []
) -> TimelineEvent:
    """创建事件"""
    return TimelineEvent(
        id=id,
        name=name,
        start_time=start_time,
        end_time=end_time,
        event_type=event_type,
        description=description,
        tags=tags
    )


def create_point_event(
    id: str,
    name: str,
    time: datetime,
    description: str = "",
    tags: List[str] = []
) -> TimelineEvent:
    """创建瞬时事件"""
    return create_event(id, name, time, None, EventType.POINT, description, tags)


def create_range_event(
    id: str,
    name: str,
    start_time: datetime,
    end_time: datetime,
    description: str = "",
    tags: List[str] = []
) -> TimelineEvent:
    """创建范围事件"""
    return create_event(id, name, start_time, end_time, EventType.RANGE, description, tags)


def create_milestone(
    id: str,
    name: str,
    time: datetime,
    description: str = "",
    tags: List[str] = []
) -> TimelineEvent:
    """创建里程碑"""
    return create_event(id, name, time, None, EventType.MILESTONE, description, tags)


def check_overlap(event1: TimelineEvent, event2: TimelineEvent) -> bool:
    """检查两个事件是否重叠"""
    return event1.overlaps(event2)


def check_adjacent(
    event1: TimelineEvent,
    event2: TimelineEvent,
    tolerance: timedelta = timedelta(minutes=1)
) -> bool:
    """检查两个事件是否相邻"""
    return event1.adjacent(event2, tolerance)


def format_duration(duration: timedelta) -> str:
    """格式化持续时间"""
    total_seconds = int(duration.total_seconds())
    
    if total_seconds < 60:
        return f"{total_seconds}s"
    elif total_seconds < 3600:
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        if seconds == 0:
            return f"{minutes}min"
        return f"{minutes}min {seconds}s"
    elif total_seconds < 86400:
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        if minutes == 0:
            return f"{hours}h"
        return f"{hours}h {minutes}min"
    else:
        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        if hours == 0:
            return f"{days}d"
        return f"{days}d {hours}h"


if __name__ == "__main__":
    # 演示
    print("=== Timeline Utils Demo ===\n")
    
    # 创建时间线
    timeline = create_timeline("Project Schedule")
    
    # 添加事件
    base = datetime(2024, 1, 1, 9, 0)
    
    timeline.add_range_event(
        "e1", "Design Phase",
        base, base + timedelta(hours=2),
        "Initial design work", ["design", "phase1"]
    )
    
    timeline.add_range_event(
        "e2", "Development",
        base + timedelta(hours=2), base + timedelta(hours=5),
        "Main development", ["dev", "phase2"]
    )
    
    timeline.add_milestone(
        "m1", "Alpha Release",
        base + timedelta(hours=5),
        "First alpha version", ["milestone", "release"]
    )
    
    timeline.add_range_event(
        "e3", "Testing",
        base + timedelta(hours=5, minutes=30), base + timedelta(hours=7),
        "QA testing", ["test", "qa"]
    )
    
    timeline.add_point_event(
        "p1", "Bug Found",
        base + timedelta(hours=6),
        "Critical bug discovered", ["bug", "critical"]
    )
    
    # 渲染
    print(timeline.render_ascii(width=60))
    print("\n")
    print(timeline.render_horizontal(width=50))
    
    # 统计
    print("\n=== Statistics ===")
    stats = timeline.statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # 查找重叠
    print("\n=== Overlaps ===")
    overlaps = timeline.find_overlaps()
    for e1, e2 in overlaps:
        print(f"{e1.name} overlaps with {e2.name}")
    
    # 导出 JSON
    print("\n=== JSON Export ===")
    print(timeline.to_json())