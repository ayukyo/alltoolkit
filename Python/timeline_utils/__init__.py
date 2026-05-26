"""
Timeline Utils - 时间线管理工具库

快速导入常用函数和类。
"""

from .mod import (
    Timeline,
    TimelineEvent,
    EventType,
    create_timeline,
    create_event,
    create_point_event,
    create_range_event,
    create_milestone,
    check_overlap,
    check_adjacent,
    format_duration,
)

__all__ = [
    'Timeline',
    'TimelineEvent',
    'EventType',
    'create_timeline',
    'create_event',
    'create_point_event',
    'create_range_event',
    'create_milestone',
    'check_overlap',
    'check_adjacent',
    'format_duration',
]