# Timeline Utils

时间线管理工具库，用于创建、管理和可视化事件时间线。

## 功能

- **事件管理**：添加、删除、更新、排序事件
- **事件类型**：瞬时事件、时间范围事件、里程碑
- **时间查询**：查找特定时间范围内的事件
- **冲突检测**：检测重叠事件、相邻事件
- **间隙分析**：查找时间线中的空闲间隙
- **统计信息**：持续时间、密度、事件计数等
- **可视化**：ASCII 格式渲染，甘特图风格
- **导入导出**：JSON、CSV 格式支持

## 快速开始

```python
from timeline_utils import Timeline, EventType
from datetime import datetime, timedelta

# 创建时间线
timeline = Timeline("Project Schedule")

# 添加范围事件
timeline.add_range_event(
    "e1", "Design Phase",
    datetime(2024, 1, 1, 9, 0),
    datetime(2024, 1, 1, 12, 0),
    tags=["design", "phase1"]
)

# 添加瞬时事件
timeline.add_point_event(
    "p1", "Meeting Start",
    datetime(2024, 1, 1, 14, 0)
)

# 添加里程碑
timeline.add_milestone(
    "m1", "Alpha Release",
    datetime(2024, 1, 1, 17, 0),
    description="First release"
)

# 渲染时间线
print(timeline.render_ascii())
```

## API 参考

### Timeline 类

#### 创建时间线

```python
timeline = Timeline(name="My Timeline")
```

#### 添加事件

```python
# 添加范围事件
timeline.add_range_event(
    id="e1",
    name="Event Name",
    start_time=datetime(2024, 1, 1, 10, 0),
    end_time=datetime(2024, 1, 1, 12, 0),
    description="Optional description",
    tags=["tag1", "tag2"],
    metadata={"key": "value"}
)

# 添加瞬时事件
timeline.add_point_event(
    id="p1",
    name="Point Event",
    time=datetime(2024, 1, 1, 14, 0)
)

# 添加里程碑
timeline.add_milestone(
    id="m1",
    name="Milestone",
    time=datetime(2024, 1, 1, 17, 0)
)
```

#### 删除事件

```python
timeline.remove_event("e1")  # 返回 True/False
```

#### 更新事件

```python
timeline.update_event("e1", name="New Name", description="Updated")
```

#### 查询事件

```python
# 获取单个事件
event = timeline.get_event("e1")

# 按标签查找
events = timeline.find_by_tag("work")

# 按名称模式查找（支持正则）
events = timeline.find_by_name("Meet")

# 获取指定时间的事件
events = timeline.get_events_at(datetime(2024, 1, 1, 10, 30))

# 获取时间范围内的事件
events = timeline.get_events_in_range(
    start=datetime(2024, 1, 1, 9, 0),
    end=datetime(2024, 1, 1, 12, 0),
    include_overlapping=True
)
```

#### 冲突检测

```python
# 查找所有重叠的事件对
overlaps = timeline.find_overlaps()

# 检查是否有冲突
has_conflicts = timeline.has_conflicts()
```

#### 间隙分析

```python
# 查找时间线中的间隙
gaps = timeline.find_gaps(min_gap=timedelta(minutes=5))
# 返回 [(start_time, end_time), ...]
```

#### 合合与分割

```python
# 合并相邻事件
merged = timeline.merge_adjacent(
    tolerance=timedelta(minutes=5),
    merged_name="Merged Event"
)

# 分割事件
timeline.split_event(
    "e1",
    split_time=datetime(2024, 1, 1, 11, 0)
)
```

#### 统计信息

```python
stats = timeline.statistics()
# 返回 {
#     "total_events": 10,
#     "point_events": 2,
#     "range_events": 6,
#     "milestones": 2,
#     "total_duration_seconds": 3600,
#     "total_event_duration_seconds": 1800,
#     "density": 0.5,
#     "gaps": 3,
#     "overlaps": 1,
#     "tags": ["work", "meeting"]
# }
```

#### 渲染

```python
# ASCII 渲染（垂直）
print(timeline.render_ascii(width=80, show_time=True))

# 水平渲染（甘特图风格）
print(timeline.render_horizontal(width=60))
```

#### 导入导出

```python
# 导出 JSON
json_str = timeline.to_json()

# 导入 JSON
timeline = Timeline.from_json(json_str)

# 导出 CSV
csv_str = timeline.to_csv()

# 导入 CSV
timeline = Timeline.from_csv(csv_str)
```

### TimelineEvent 类

#### 属性

```python
event = timeline.get_event("e1")

event.id           # 事件 ID
event.name         # 事件名称
event.start_time   # 开始时间
event.end_time     # 结束时间（None 表示瞬时事件）
event.event_type   # EventType.POINT/RANGE/MILESTONE
event.description  # 描述
event.tags         # 标签列表
event.metadata     # 元数据字典

event.duration           # 持续时间（timedelta）
event.duration_seconds   # 持续时间（秒）
event.duration_minutes   # 持续时间（分钟）
event.duration_hours     # 持续时间（小时）
```

#### 方法

```python
# 检查时间是否在事件范围内
event.contains(datetime(2024, 1, 1, 10, 30))

# 检查是否与另一事件重叠
event.overlaps(other_event)

# 检查是否与另一事件相邻
event.adjacent(other_event, tolerance=timedelta(minutes=5))

# 序列化
event.to_dict()
TimelineEvent.from_dict(data)
```

### EventType 枚举

```python
EventType.POINT      # 瞬时事件（无持续时间）
EventType.RANGE      # 时间范围事件
EventType.MILESTONE  # 里程碑事件
```

### 便捷函数

```python
from timeline_utils import (
    create_timeline,
    create_point_event,
    create_range_event,
    create_milestone,
    check_overlap,
    check_adjacent,
    format_duration
)

# 创建时间线
timeline = create_timeline("My Timeline")

# 创建事件
event = create_point_event("p1", "Point", datetime.now())
event = create_range_event("e1", "Range", start, end)
event = create_milestone("m1", "Milestone", time)

# 检查重叠
is_overlap = check_overlap(event1, event2)

# 检查相邻
is_adjacent = check_adjacent(event1, event2, tolerance=timedelta(minutes=5))

# 格式化持续时间
formatted = format_duration(timedelta(hours=2, minutes=30))  # "2h 30min"
```

## 使用场景

### 项目进度管理

```python
timeline = Timeline("Project Alpha")

# 添加各阶段
timeline.add_range_event("phase1", "Planning", start, start + timedelta(days=5))
timeline.add_range_event("phase2", "Development", start + timedelta(days=5), start + timedelta(days=20))
timeline.add_milestone("m1", "Beta Release", start + timedelta(days=20))

# 检查是否有重叠阶段
if timeline.has_conflicts():
    print("Warning: overlapping phases detected!")

# 渲染甘特图
print(timeline.render_horizontal(width=80))
```

### 会议日程安排

```python
day_schedule = Timeline("Today's Schedule")

day_schedule.add_range_event("meeting1", "Team Meeting", datetime(9, 0), datetime(10, 0))
day_schedule.add_range_event("meeting2", "Client Call", datetime(10, 30), datetime(11, 30))
day_schedule.add_range_event("meeting3", "Review", datetime(11, 0), datetime(12, 0))

# 检测会议冲突
conflicts = day_schedule.find_overlaps()
for e1, e2 in conflicts:
    print(f"Conflict: {e1.name} overlaps with {e2.name}")

# 查找空闲时间
gaps = day_schedule.find_gaps()
for start, end in gaps:
    print(f"Free: {start.strftime('%H:%M')} - {end.strftime('%H:%M')}")
```

### 历史事件时间线

```python
history = Timeline("World History")

history.add_range_event("ww1", "World War I", datetime(1914, 7, 28), datetime(1918, 11, 11))
history.add_point_event("moon", "Moon Landing", datetime(1969, 7, 20))
history.add_milestone("internet", "Internet Launch", datetime(1991, 8, 6))

# 导出保存
json_str = history.to_json()
```

## 测试

```bash
python timeline_utils/timeline_utils_test.py
```

测试覆盖：
- 事件创建和验证（类型、时间、边界）
- 时间线操作（添加、删除、更新）
- 时间范围查询
- 重叠和相邻检测
- 间隙查找
- 统计计算
- ASCII 渲染
- JSON/CSV 导入导出
- 边界值（零持续时间、大跨度、多事件同时间）

## 许可证

MIT License