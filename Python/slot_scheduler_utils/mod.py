"""
时间槽调度工具 (Slot Scheduler Utils)

提供时间槽管理、预约调度、冲突检测等功能。
零外部依赖，仅使用 Python 标准库。

功能：
- 时间槽创建与管理
- 预约与取消
- 冲突检测
- 可用时间查询
- 批量操作
- 重复调度（每日/每周/每月）
"""

from datetime import datetime, timedelta, date, time
from typing import List, Dict, Optional, Tuple, Set, Iterator
from dataclasses import dataclass, field
from enum import Enum
import re


class RecurrenceType(Enum):
    """重复类型"""
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class BookingStatus(Enum):
    """预约状态"""
    AVAILABLE = "available"
    BOOKED = "booked"
    BLOCKED = "blocked"
    PENDING = "pending"


@dataclass
class TimeSlot:
    """时间槽"""
    start: datetime
    end: datetime
    resource_id: str
    slot_id: Optional[str] = None
    status: BookingStatus = BookingStatus.AVAILABLE
    metadata: Dict = field(default_factory=dict)
    
    def __post_init__(self):
        """验证时间槽"""
        if self.start >= self.end:
            raise ValueError(f"开始时间必须早于结束时间: {self.start} >= {self.end}")
        if self.slot_id is None:
            self.slot_id = self._generate_id()
    
    def _generate_id(self) -> str:
        """生成唯一ID"""
        return f"{self.resource_id}_{self.start.strftime('%Y%m%d%H%M')}_{self.end.strftime('%H%M')}"
    
    @property
    def duration(self) -> timedelta:
        """时长"""
        return self.end - self.start
    
    @property
    def duration_minutes(self) -> int:
        """时长（分钟）"""
        return int(self.duration.total_seconds() / 60)
    
    def overlaps(self, other: 'TimeSlot') -> bool:
        """检查是否与另一时间槽重叠"""
        if self.resource_id != other.resource_id:
            return False
        return self.start < other.end and self.end > other.start
    
    def contains(self, dt: datetime) -> bool:
        """检查指定时间是否在时间槽内"""
        return self.start <= dt < self.end
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'slot_id': self.slot_id,
            'resource_id': self.resource_id,
            'start': self.start.isoformat(),
            'end': self.end.isoformat(),
            'duration_minutes': self.duration_minutes,
            'status': self.status.value,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TimeSlot':
        """从字典创建"""
        # 使用 strptime 解析 ISO 格式时间
        start_str = data['start']
        end_str = data['end']
        
        # 尝试多种格式解析
        def parse_datetime(dt_str: str) -> datetime:
            formats = [
                '%Y-%m-%dT%H:%M:%S',
                '%Y-%m-%dT%H:%M:%S.%f',
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d %H:%M:%S.%f'
            ]
            for fmt in formats:
                try:
                    return datetime.strptime(dt_str, fmt)
                except ValueError:
                    continue
            raise ValueError(f"无法解析时间格式: {dt_str}")
        
        return cls(
            start=parse_datetime(start_str),
            end=parse_datetime(end_str),
            resource_id=data['resource_id'],
            slot_id=data.get('slot_id'),
            status=BookingStatus(data.get('status', 'available')),
            metadata=data.get('metadata', {})
        )


@dataclass
class RecurrenceRule:
    """重复规则"""
    recurrence_type: RecurrenceType
    interval: int = 1  # 间隔（如每2周）
    end_date: Optional[date] = None
    count: Optional[int] = None  # 重复次数
    days_of_week: Optional[List[int]] = None  # 0=周一, 6=周日
    day_of_month: Optional[int] = None  # 每月的第几天
    exceptions: Set[date] = field(default_factory=set)  # 排除的日期
    
    def get_occurrences(self, start: date, end: date) -> List[date]:
        """获取指定日期范围内的所有出现日期"""
        occurrences = []
        actual_end = end
        
        if self.end_date and self.end_date < actual_end:
            actual_end = self.end_date
        
        count = 0
        
        if self.recurrence_type == RecurrenceType.DAILY:
            # 每日重复：按间隔跳跃
            current = start
            while current <= actual_end:
                if self.count and count >= self.count:
                    break
                if current not in self.exceptions:
                    occurrences.append(current)
                    count += 1
                current = current + timedelta(days=self.interval)
        
        elif self.recurrence_type == RecurrenceType.WEEKLY:
            # 每周重复：找出范围内所有匹配星期几的日期
            current = start
            while current <= actual_end:
                if self.count and count >= self.count:
                    break
                # 检查是否是目标星期几
                if self.days_of_week:
                    if current.weekday() in self.days_of_week and current not in self.exceptions:
                        occurrences.append(current)
                        count += 1
                else:
                    # 无指定星期几，从 start 开始每周跳跃
                    if current not in self.exceptions:
                        occurrences.append(current)
                        count += 1
                    current = current + timedelta(weeks=self.interval)
                    continue
                current = current + timedelta(days=1)
        
        elif self.recurrence_type == RecurrenceType.MONTHLY:
            # 每月重复：找出范围内每月指定日
            target_day = self.day_of_month or start.day
            # 从第一个月开始
            current_year = start.year
            current_month = start.month
            
            while True:
                if self.count and count >= self.count:
                    break
                
                # 构造该月的目标日期
                try:
                    # 安全处理：如果目标日超出该月天数，使用最后一天
                    last_day_of_month = (date(current_year, current_month % 12 + 1, 1) - timedelta(days=1)).day
                    actual_day = min(target_day, last_day_of_month)
                    candidate = date(current_year, current_month, actual_day)
                    
                    if candidate > actual_end:
                        break
                    
                    if candidate >= start and candidate not in self.exceptions:
                        occurrences.append(candidate)
                        count += 1
                except ValueError:
                    pass
                
                # 下一个月
                current_month += self.interval
                if current_month > 12:
                    current_year += (current_month - 1) // 12
                    current_month = ((current_month - 1) % 12) + 1
        
        elif self.recurrence_type == RecurrenceType.YEARLY:
            # 每年重复
            current_year = start.year
            while True:
                if self.count and count >= self.count:
                    break
                
                try:
                    candidate = date(current_year, start.month, start.day)
                    if candidate > actual_end:
                        break
                    if candidate >= start and candidate not in self.exceptions:
                        occurrences.append(candidate)
                        count += 1
                except ValueError:
                    pass
                
                current_year += self.interval
        
        else:
            # NONE 或其他：只返回开始日期
            if start not in self.exceptions:
                occurrences.append(start)
        
        return occurrences
    
    def _matches_rule(self, d: date) -> bool:
        """检查日期是否匹配规则"""
        if self.recurrence_type == RecurrenceType.DAILY:
            return True
        elif self.recurrence_type == RecurrenceType.WEEKLY:
            if self.days_of_week:
                return d.weekday() in self.days_of_week
            return True
        elif self.recurrence_type == RecurrenceType.MONTHLY:
            if self.day_of_month:
                return d.day == self.day_of_month
            return True
        elif self.recurrence_type == RecurrenceType.YEARLY:
            return True
        return False
    
    def _next_date(self, current: date) -> date:
        """获取下一个日期"""
        if self.recurrence_type == RecurrenceType.DAILY:
            return current + timedelta(days=self.interval)
        elif self.recurrence_type == RecurrenceType.WEEKLY:
            return current + timedelta(weeks=self.interval)
        elif self.recurrence_type == RecurrenceType.MONTHLY:
            month = current.month + self.interval
            year = current.year + (month - 1) // 12
            month = ((month - 1) % 12) + 1
            day = min(current.day, 28)  # 安全处理
            return date(year, month, day)
        elif self.recurrence_type == RecurrenceType.YEARLY:
            return date(current.year + self.interval, current.month, current.day)
        return current + timedelta(days=1)


@dataclass
class Booking:
    """预约"""
    booking_id: str
    slot: TimeSlot
    user_id: str
    created_at: datetime = field(default_factory=datetime.now)
    notes: str = ""
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'booking_id': self.booking_id,
            'slot': self.slot.to_dict(),
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'notes': self.notes,
            'metadata': self.metadata
        }


class SlotScheduler:
    """时间槽调度器"""
    
    def __init__(self, default_slot_duration: int = 30):
        """
        初始化调度器
        
        Args:
            default_slot_duration: 默认时间槽时长（分钟）
        """
        self.default_slot_duration = default_slot_duration
        self.slots: Dict[str, TimeSlot] = {}
        self.bookings: Dict[str, Booking] = {}
        self.user_bookings: Dict[str, Set[str]] = {}  # user_id -> booking_ids
    
    def create_slot(
        self,
        start: datetime,
        end: datetime,
        resource_id: str,
        metadata: Optional[Dict] = None
    ) -> TimeSlot:
        """
        创建时间槽
        
        Args:
            start: 开始时间
            end: 结束时间
            resource_id: 资源ID
            metadata: 元数据
            
        Returns:
            创建的时间槽
        """
        slot = TimeSlot(
            start=start,
            end=end,
            resource_id=resource_id,
            metadata=metadata or {}
        )
        self.slots[slot.slot_id] = slot
        return slot
    
    def create_slots_from_schedule(
        self,
        resource_id: str,
        start_date: date,
        end_date: date,
        daily_start_time: time,
        daily_end_time: time,
        slot_duration: Optional[int] = None,
        break_between_slots: int = 0,
        working_days: Optional[List[int]] = None
    ) -> List[TimeSlot]:
        """
        根据日程创建多个时间槽
        
        Args:
            resource_id: 资源ID
            start_date: 开始日期
            end_date: 结束日期
            daily_start_time: 每日开始时间
            daily_end_time: 每日结束时间
            slot_duration: 时间槽时长（分钟）
            break_between_slots: 时间槽间隔（分钟）
            working_days: 工作日（0=周一, 6=周日），None表示每天
            
        Returns:
            创建的时间槽列表
        """
        duration = slot_duration or self.default_slot_duration
        slots = []
        current_date = start_date
        
        while current_date <= end_date:
            if working_days is None or current_date.weekday() in working_days:
                current_time = datetime.combine(current_date, daily_start_time)
                end_time = datetime.combine(current_date, daily_end_time)
                
                while current_time + timedelta(minutes=duration) <= end_time:
                    slot = self.create_slot(
                        start=current_time,
                        end=current_time + timedelta(minutes=duration),
                        resource_id=resource_id
                    )
                    slots.append(slot)
                    current_time += timedelta(minutes=duration + break_between_slots)
            
            current_date += timedelta(days=1)
        
        return slots
    
    def create_recurring_slots(
        self,
        base_start: datetime,
        base_end: datetime,
        resource_id: str,
        recurrence: RecurrenceRule,
        metadata: Optional[Dict] = None
    ) -> List[TimeSlot]:
        """
        创建重复时间槽
        
        Args:
            base_start: 基础开始时间
            base_end: 基础结束时间
            resource_id: 资源ID
            recurrence: 重复规则
            metadata: 元数据
            
        Returns:
            创建的时间槽列表
        """
        slots = []
        duration = base_end - base_start
        
        start_date = base_start.date()
        end_date = recurrence.end_date or (start_date + timedelta(days=365))
        
        occurrences = recurrence.get_occurrences(start_date, end_date)
        
        for occ_date in occurrences:
            slot_start = datetime.combine(occ_date, base_start.time())
            slot_end = slot_start + duration
            
            slot = self.create_slot(
                start=slot_start,
                end=slot_end,
                resource_id=resource_id,
                metadata=metadata
            )
            slots.append(slot)
        
        return slots
    
    def get_slot(self, slot_id: str) -> Optional[TimeSlot]:
        """获取时间槽"""
        return self.slots.get(slot_id)
    
    def get_slots_by_resource(
        self,
        resource_id: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None
    ) -> List[TimeSlot]:
        """
        获取资源的时间槽
        
        Args:
            resource_id: 资源ID
            start: 开始时间过滤
            end: 结束时间过滤
            
        Returns:
            时间槽列表
        """
        slots = [s for s in self.slots.values() if s.resource_id == resource_id]
        
        if start:
            slots = [s for s in slots if s.end > start]
        if end:
            slots = [s for s in slots if s.start < end]
        
        return sorted(slots, key=lambda s: s.start)
    
    def get_available_slots(
        self,
        resource_id: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None
    ) -> List[TimeSlot]:
        """
        获取可用时间槽
        
        Args:
            resource_id: 资源ID
            start: 开始时间过滤
            end: 结束时间过滤
            
        Returns:
            可用时间槽列表
        """
        slots = self.get_slots_by_resource(resource_id, start, end)
        return [s for s in slots if s.status == BookingStatus.AVAILABLE]
    
    def book_slot(
        self,
        slot_id: str,
        user_id: str,
        notes: str = "",
        metadata: Optional[Dict] = None
    ) -> Optional[Booking]:
        """
        预约时间槽
        
        Args:
            slot_id: 时间槽ID
            user_id: 用户ID
            notes: 备注
            metadata: 元数据
            
        Returns:
            预约对象，如果失败返回None
        """
        slot = self.slots.get(slot_id)
        if not slot:
            return None
        
        if slot.status != BookingStatus.AVAILABLE:
            return None
        
        # 检查用户是否已有冲突预约
        user_slot_ids = self.user_bookings.get(user_id, set())
        for booking_id in user_slot_ids:
            existing = self.bookings.get(booking_id)
            if existing and existing.slot.overlaps(slot):
                return None
        
        # 更新状态
        slot.status = BookingStatus.BOOKED
        
        # 创建预约
        booking = Booking(
            booking_id=f"booking_{slot_id}_{user_id}",
            slot=slot,
            user_id=user_id,
            notes=notes,
            metadata=metadata or {}
        )
        
        self.bookings[booking.booking_id] = booking
        
        if user_id not in self.user_bookings:
            self.user_bookings[user_id] = set()
        self.user_bookings[user_id].add(booking.booking_id)
        
        return booking
    
    def cancel_booking(self, booking_id: str) -> bool:
        """
        取消预约
        
        Args:
            booking_id: 预约ID
            
        Returns:
            是否成功
        """
        booking = self.bookings.get(booking_id)
        if not booking:
            return False
        
        # 更新时间槽状态
        booking.slot.status = BookingStatus.AVAILABLE
        
        # 从用户预约中移除
        if booking.user_id in self.user_bookings:
            self.user_bookings[booking.user_id].discard(booking_id)
        
        # 删除预约
        del self.bookings[booking_id]
        
        return True
    
    def block_slot(self, slot_id: str, reason: str = "") -> bool:
        """
        封锁时间槽（不可预约）
        
        Args:
            slot_id: 时间槽ID
            reason: 封锁原因
            
        Returns:
            是否成功
        """
        slot = self.slots.get(slot_id)
        if not slot:
            return False
        
        slot.status = BookingStatus.BLOCKED
        slot.metadata['blocked_reason'] = reason
        return True
    
    def unblock_slot(self, slot_id: str) -> bool:
        """
        解除封锁
        
        Args:
            slot_id: 时间槽ID
            
        Returns:
            是否成功
        """
        slot = self.slots.get(slot_id)
        if not slot or slot.status != BookingStatus.BLOCKED:
            return False
        
        slot.status = BookingStatus.AVAILABLE
        slot.metadata.pop('blocked_reason', None)
        return True
    
    def find_next_available(
        self,
        resource_id: str,
        after: datetime,
        duration_minutes: Optional[int] = None
    ) -> Optional[TimeSlot]:
        """
        查找下一个可用时间槽
        
        Args:
            resource_id: 资源ID
            after: 开始查找的时间
            duration_minutes: 要求的最小时长（分钟）
            
        Returns:
            可用时间槽，如果没有返回None
        """
        slots = self.get_slots_by_resource(resource_id, start=after)
        
        for slot in slots:
            if slot.status == BookingStatus.AVAILABLE:
                if duration_minutes is None or slot.duration_minutes >= duration_minutes:
                    return slot
        
        return None
    
    def find_available_range(
        self,
        resource_id: str,
        start: datetime,
        end: datetime,
        duration_minutes: int
    ) -> List[TimeSlot]:
        """
        查找指定时间范围内能容纳指定时长的时间槽
        
        Args:
            resource_id: 资源ID
            start: 开始时间
            end: 结束时间
            duration_minutes: 需要的时长（分钟）
            
        Returns:
            符合条件的时间槽列表
        """
        slots = self.get_available_slots(resource_id, start, end)
        return [s for s in slots if s.duration_minutes >= duration_minutes]
    
    def get_user_bookings(
        self,
        user_id: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None
    ) -> List[Booking]:
        """
        获取用户的预约
        
        Args:
            user_id: 用户ID
            start: 开始时间过滤
            end: 结束时间过滤
            
        Returns:
            预约列表
        """
        booking_ids = self.user_bookings.get(user_id, set())
        bookings = []
        
        for booking_id in booking_ids:
            booking = self.bookings.get(booking_id)
            if booking:
                if start and booking.slot.end <= start:
                    continue
                if end and booking.slot.start >= end:
                    continue
                bookings.append(booking)
        
        return sorted(bookings, key=lambda b: b.slot.start)
    
    def check_availability(
        self,
        resource_id: str,
        start: datetime,
        end: datetime
    ) -> Tuple[bool, List[TimeSlot]]:
        """
        检查资源在指定时间段是否可用
        
        Args:
            resource_id: 资源ID
            start: 开始时间
            end: 结束时间
            
        Returns:
            (是否可用, 冲突的时间槽列表)
        """
        slots = self.get_slots_by_resource(resource_id, start, end)
        conflicts = []
        
        for slot in slots:
            if slot.overlaps(TimeSlot(start=start, end=end, resource_id=resource_id)):
                if slot.status != BookingStatus.AVAILABLE:
                    conflicts.append(slot)
        
        return len(conflicts) == 0, conflicts
    
    def get_schedule_summary(
        self,
        resource_id: str,
        date: date
    ) -> Dict:
        """
        获取某日的调度摘要
        
        Args:
            resource_id: 资源ID
            date: 日期
            
        Returns:
            摘要信息
        """
        start = datetime.combine(date, time.min)
        end = datetime.combine(date, time.max)
        
        slots = self.get_slots_by_resource(resource_id, start, end)
        
        total_slots = len(slots)
        available = sum(1 for s in slots if s.status == BookingStatus.AVAILABLE)
        booked = sum(1 for s in slots if s.status == BookingStatus.BOOKED)
        blocked = sum(1 for s in slots if s.status == BookingStatus.BLOCKED)
        
        total_minutes = sum(s.duration_minutes for s in slots)
        available_minutes = sum(
            s.duration_minutes for s in slots 
            if s.status == BookingStatus.AVAILABLE
        )
        
        return {
            'resource_id': resource_id,
            'date': date.isoformat(),
            'total_slots': total_slots,
            'available_slots': available,
            'booked_slots': booked,
            'blocked_slots': blocked,
            'total_minutes': total_minutes,
            'available_minutes': available_minutes,
            'utilization_rate': (total_minutes - available_minutes) / total_minutes if total_minutes > 0 else 0
        }
    
    def delete_slot(self, slot_id: str) -> bool:
        """
        删除时间槽
        
        Args:
            slot_id: 时间槽ID
            
        Returns:
            是否成功
        """
        slot = self.slots.get(slot_id)
        if not slot:
            return False
        
        if slot.status == BookingStatus.BOOKED:
            return False  # 不能删除已预约的时间槽
        
        del self.slots[slot_id]
        return True
    
    def clear_past_slots(self, before: datetime) -> int:
        """
        清理过去的时间槽
        
        Args:
            before: 清理此时间之前的时间槽
            
        Returns:
            清理的数量
        """
        to_delete = [
            slot_id for slot_id, slot in self.slots.items()
            if slot.end < before and slot.status != BookingStatus.BOOKED
        ]
        
        for slot_id in to_delete:
            del self.slots[slot_id]
        
        return len(to_delete)
    
    def to_dict(self) -> Dict:
        """导出为字典"""
        return {
            'slots': {sid: slot.to_dict() for sid, slot in self.slots.items()},
            'bookings': {bid: booking.to_dict() for bid, booking in self.bookings.items()}
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'SlotScheduler':
        """从字典导入"""
        scheduler = cls()
        
        # 解析时间字符串的辅助函数
        def parse_datetime(dt_str: str) -> datetime:
            formats = [
                '%Y-%m-%dT%H:%M:%S',
                '%Y-%m-%dT%H:%M:%S.%f',
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d %H:%M:%S.%f'
            ]
            for fmt in formats:
                try:
                    return datetime.strptime(dt_str, fmt)
                except ValueError:
                    continue
            raise ValueError(f"无法解析时间格式: {dt_str}")
        
        for slot_data in data.get('slots', {}).values():
            slot = TimeSlot.from_dict(slot_data)
            scheduler.slots[slot.slot_id] = slot
        
        for booking_data in data.get('bookings', {}).values():
            slot = TimeSlot.from_dict(booking_data['slot'])
            booking = Booking(
                booking_id=booking_data['booking_id'],
                slot=slot,
                user_id=booking_data['user_id'],
                created_at=parse_datetime(booking_data['created_at']),
                notes=booking_data.get('notes', ''),
                metadata=booking_data.get('metadata', {})
            )
            scheduler.bookings[booking.booking_id] = booking
            
            # 更新时间槽状态
            if slot.slot_id in scheduler.slots:
                scheduler.slots[slot.slot_id].status = slot.status
            
            # 更新用户预约索引
            if booking.user_id not in scheduler.user_bookings:
                scheduler.user_bookings[booking.user_id] = set()
            scheduler.user_bookings[booking.user_id].add(booking.booking_id)
        
        return scheduler


# 便捷函数

def create_daily_slots(
    resource_id: str,
    date: date,
    start_time: time,
    end_time: time,
    slot_duration: int = 30,
    break_minutes: int = 0
) -> List[TimeSlot]:
    """
    为某日创建时间槽
    
    Args:
        resource_id: 资源ID
        date: 日期
        start_time: 开始时间
        end_time: 结束时间
        slot_duration: 时间槽时长（分钟）
        break_minutes: 间隔时间（分钟）
        
    Returns:
        时间槽列表
    """
    scheduler = SlotScheduler()
    return scheduler.create_slots_from_schedule(
        resource_id=resource_id,
        start_date=date,
        end_date=date,
        daily_start_time=start_time,
        daily_end_time=end_time,
        slot_duration=slot_duration,
        break_between_slots=break_minutes
    )


def find_free_time(
    slots: List[TimeSlot],
    min_duration_minutes: int
) -> List[Tuple[datetime, datetime]]:
    """
    查找连续空闲时间段
    
    Args:
        slots: 时间槽列表
        min_duration_minutes: 最小空闲时长（分钟）
        
    Returns:
        空闲时间段列表 [(开始, 结束), ...]
    """
    if not slots:
        return []
    
    sorted_slots = sorted(slots, key=lambda s: s.start)
    free_periods = []
    
    # 找到第一个可用时间槽之前的时间
    first_available = None
    for slot in sorted_slots:
        if slot.status == BookingStatus.AVAILABLE:
            first_available = slot
            break
    
    # 合并连续的可用时间槽
    current_start = None
    current_end = None
    
    for slot in sorted_slots:
        if slot.status == BookingStatus.AVAILABLE:
            if current_start is None:
                current_start = slot.start
                current_end = slot.end
            elif slot.start <= current_end:
                current_end = max(current_end, slot.end)
            else:
                # 有间隙，保存当前段并开始新段
                duration = (current_end - current_start).total_seconds() / 60
                if duration >= min_duration_minutes:
                    free_periods.append((current_start, current_end))
                current_start = slot.start
                current_end = slot.end
    
    # 保存最后一段
    if current_start and current_end:
        duration = (current_end - current_start).total_seconds() / 60
        if duration >= min_duration_minutes:
            free_periods.append((current_start, current_end))
    
    return free_periods


def calculate_utilization(
    slots: List[TimeSlot],
    start: Optional[datetime] = None,
    end: Optional[datetime] = None
) -> Dict:
    """
    计算利用率
    
    Args:
        slots: 时间槽列表
        start: 开始时间过滤
        end: 结束时间过滤
        
    Returns:
        利用率统计
    """
    if start or end:
        filtered = []
        for slot in slots:
            if start and slot.end <= start:
                continue
            if end and slot.start >= end:
                continue
            filtered.append(slot)
        slots = filtered
    
    if not slots:
        return {
            'total_slots': 0,
            'total_minutes': 0,
            'booked_minutes': 0,
            'utilization': 0.0
        }
    
    total_minutes = sum(s.duration_minutes for s in slots)
    booked_minutes = sum(
        s.duration_minutes for s in slots 
        if s.status == BookingStatus.BOOKED
    )
    
    return {
        'total_slots': len(slots),
        'total_minutes': total_minutes,
        'booked_minutes': booked_minutes,
        'utilization': booked_minutes / total_minutes if total_minutes > 0 else 0.0
    }