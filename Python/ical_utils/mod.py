"""
iCalendar (ICS) Utilities - 零外部依赖的日历格式处理工具

支持功能:
- 创建日历事件
- 解析 ICS 文件
- 生成符合 RFC 5545 标准的 ICS 文件
- 支持重复事件 (RRULE)
- 支持时区处理
- 支持 VTODO 和 VJOURNAL
"""

import re
from datetime import datetime, date, timedelta
from typing import Optional, Union, List, Dict, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum


class Frequency(Enum):
    """重复频率"""
    SECONDLY = "SECONDLY"
    MINUTELY = "MINUTELY"
    HOURLY = "HOURLY"
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"


class WeekDay(Enum):
    """星期"""
    SU = "SU"  # Sunday
    MO = "MO"  # Monday
    TU = "TU"  # Tuesday
    WE = "WE"  # Wednesday
    TH = "TH"  # Thursday
    FR = "FR"  # Friday
    SA = "SA"  # Saturday


@dataclass
class RecurrenceRule:
    """重复规则 (RRULE)"""
    frequency: Frequency
    interval: int = 1
    count: Optional[int] = None
    until: Optional[Union[datetime, date]] = None
    by_day: Optional[List[WeekDay]] = None
    by_month: Optional[List[int]] = None
    by_month_day: Optional[List[int]] = None
    by_hour: Optional[List[int]] = None
    by_minute: Optional[List[int]] = None
    by_second: Optional[List[int]] = None
    week_start: WeekDay = WeekDay.MO
    
    def to_ical(self) -> str:
        """转换为 ICS 格式的 RRULE 字符串"""
        parts = [f"FREQ={self.frequency.value}"]
        
        if self.interval != 1:
            parts.append(f"INTERVAL={self.interval}")
        
        if self.count is not None:
            parts.append(f"COUNT={self.count}")
        
        if self.until is not None:
            if isinstance(self.until, datetime):
                parts.append(f"UNTIL={_format_datetime_utc(self.until)}")
            else:
                parts.append(f"UNTIL={_format_date(self.until)}")
        
        if self.by_day:
            parts.append(f"BYDAY={','.join(d.value for d in self.by_day)}")
        
        if self.by_month:
            parts.append(f"BYMONTH={','.join(map(str, self.by_month))}")
        
        if self.by_month_day:
            parts.append(f"BYMONTHDAY={','.join(map(str, self.by_month_day))}")
        
        if self.by_hour:
            parts.append(f"BYHOUR={','.join(map(str, self.by_hour))}")
        
        if self.by_minute:
            parts.append(f"BYMINUTE={','.join(map(str, self.by_minute))}")
        
        if self.by_second:
            parts.append(f"BYSECOND={','.join(map(str, self.by_second))}")
        
        if self.week_start != WeekDay.MO:
            parts.append(f"WKST={self.week_start.value}")
        
        return ";".join(parts)


@dataclass
class VEvent:
    """日历事件"""
    uid: str
    dtstart: Union[datetime, date]
    dtend: Optional[Union[datetime, date]] = None
    duration: Optional[timedelta] = None
    summary: str = ""
    description: str = ""
    location: str = ""
    organizer: Optional[str] = None
    organizer_name: Optional[str] = None
    attendees: List[Tuple[str, Optional[str]]] = field(default_factory=list)  # (email, name)
    categories: List[str] = field(default_factory=list)
    status: str = "CONFIRMED"  # TENTATIVE, CONFIRMED, CANCELLED
    priority: Optional[int] = None  # 1-9, 1 = highest
    rrule: Optional[RecurrenceRule] = None
    exdates: List[Union[datetime, date]] = field(default_factory=list)
    alarms: List[int] = field(default_factory=list)  # minutes before
    url: Optional[str] = None
    dtstamp: Optional[datetime] = None
    created: Optional[datetime] = None
    last_modified: Optional[datetime] = None
    is_all_day: bool = False
    timezone: str = "UTC"
    
    def __post_init__(self):
        if self.dtstamp is None:
            self.dtstamp = datetime.utcnow()
        if isinstance(self.dtstart, date) and not isinstance(self.dtstart, datetime):
            self.is_all_day = True
    
    def to_ical(self) -> str:
        """转换为 ICS 格式"""
        lines = ["BEGIN:VEVENT"]
        
        # UID
        lines.append(f"UID:{self.uid}")
        
        # DTSTAMP
        lines.append(f"DTSTAMP:{_format_datetime_utc(self.dtstamp)}")
        
        # DTSTART
        if self.is_all_day:
            lines.append(f"DTSTART;VALUE=DATE:{_format_date(self.dtstart)}")
        else:
            if self.timezone and self.timezone != "UTC":
                lines.append(f"DTSTART;TZID={self.timezone}:{_format_datetime_local(self.dtstart)}")
            else:
                lines.append(f"DTSTART:{_format_datetime_utc(self.dtstart)}")
        
        # DTEND or DURATION
        if self.dtend:
            if self.is_all_day:
                lines.append(f"DTEND;VALUE=DATE:{_format_date(self.dtend)}")
            else:
                if self.timezone and self.timezone != "UTC":
                    lines.append(f"DTEND;TZID={self.timezone}:{_format_datetime_local(self.dtend)}")
                else:
                    lines.append(f"DTEND:{_format_datetime_utc(self.dtend)}")
        elif self.duration:
            lines.append(f"DURATION:{_format_duration(self.duration)}")
        
        # SUMMARY
        if self.summary:
            lines.append(f"SUMMARY:{_escape_text(self.summary)}")
        
        # DESCRIPTION
        if self.description:
            lines.append(f"DESCRIPTION:{_escape_text(self.description)}")
        
        # LOCATION
        if self.location:
            lines.append(f"LOCATION:{_escape_text(self.location)}")
        
        # ORGANIZER
        if self.organizer:
            if self.organizer_name:
                lines.append(f"ORGANIZER;CN={_escape_text(self.organizer_name)}:mailto:{self.organizer}")
            else:
                lines.append(f"ORGANIZER:mailto:{self.organizer}")
        
        # ATTENDEES
        for email, name in self.attendees:
            if name:
                lines.append(f"ATTENDEE;CN={_escape_text(name)};RSVP=TRUE:mailto:{email}")
            else:
                lines.append(f"ATTENDEE;RSVP=TRUE:mailto:{email}")
        
        # CATEGORIES
        if self.categories:
            lines.append(f"CATEGORIES:{','.join(_escape_text(c) for c in self.categories)}")
        
        # STATUS
        lines.append(f"STATUS:{self.status}")
        
        # PRIORITY
        if self.priority is not None:
            lines.append(f"PRIORITY:{self.priority}")
        
        # RRULE
        if self.rrule:
            lines.append(f"RRULE:{self.rrule.to_ical()}")
        
        # EXDATE
        for exdate in self.exdates:
            if isinstance(exdate, datetime):
                lines.append(f"EXDATE:{_format_datetime_utc(exdate)}")
            else:
                lines.append(f"EXDATE;VALUE=DATE:{_format_date(exdate)}")
        
        # VALARM (reminders)
        for alarm_minutes in self.alarms:
            lines.extend([
                "BEGIN:VALARM",
                "ACTION:DISPLAY",
                f"DESCRIPTION:{_escape_text(self.summary)}",
                f"TRIGGER:-PT{alarm_minutes}M",
                "END:VALARM"
            ])
        
        # URL
        if self.url:
            lines.append(f"URL:{self.url}")
        
        # CREATED
        if self.created:
            lines.append(f"CREATED:{_format_datetime_utc(self.created)}")
        
        # LAST-MODIFIED
        if self.last_modified:
            lines.append(f"LAST-MODIFIED:{_format_datetime_utc(self.last_modified)}")
        
        lines.append("END:VEVENT")
        return "\n".join(lines)


@dataclass
class VTodo:
    """待办事项"""
    uid: str
    dtstart: Optional[Union[datetime, date]] = None
    due: Optional[Union[datetime, date]] = None
    summary: str = ""
    description: str = ""
    status: str = "NEEDS-ACTION"  # NEEDS-ACTION, COMPLETED, IN-PROCESS, CANCELLED
    priority: Optional[int] = None
    percent_complete: Optional[int] = None  # 0-100
    completed: Optional[datetime] = None
    categories: List[str] = field(default_factory=list)
    dtstamp: Optional[datetime] = None
    
    def __post_init__(self):
        if self.dtstamp is None:
            self.dtstamp = datetime.utcnow()
    
    def to_ical(self) -> str:
        """转换为 ICS 格式"""
        lines = ["BEGIN:VTODO"]
        
        lines.append(f"UID:{self.uid}")
        lines.append(f"DTSTAMP:{_format_datetime_utc(self.dtstamp)}")
        
        if self.dtstart:
            if isinstance(self.dtstart, date) and not isinstance(self.dtstart, datetime):
                lines.append(f"DTSTART;VALUE=DATE:{_format_date(self.dtstart)}")
            else:
                lines.append(f"DTSTART:{_format_datetime_utc(self.dtstart)}")
        
        if self.due:
            if isinstance(self.due, date) and not isinstance(self.due, datetime):
                lines.append(f"DUE;VALUE=DATE:{_format_date(self.due)}")
            else:
                lines.append(f"DUE:{_format_datetime_utc(self.due)}")
        
        if self.summary:
            lines.append(f"SUMMARY:{_escape_text(self.summary)}")
        
        if self.description:
            lines.append(f"DESCRIPTION:{_escape_text(self.description)}")
        
        lines.append(f"STATUS:{self.status}")
        
        if self.priority is not None:
            lines.append(f"PRIORITY:{self.priority}")
        
        if self.percent_complete is not None:
            lines.append(f"PERCENT-COMPLETE:{self.percent_complete}")
        
        if self.completed:
            lines.append(f"COMPLETED:{_format_datetime_utc(self.completed)}")
        
        if self.categories:
            lines.append(f"CATEGORIES:{','.join(self.categories)}")
        
        lines.append("END:VTODO")
        return "\n".join(lines)


@dataclass
class VJournal:
    """日记/日志条目"""
    uid: str
    dtstart: Union[datetime, date]
    summary: str = ""
    description: str = ""
    categories: List[str] = field(default_factory=list)
    dtstamp: Optional[datetime] = None
    
    def __post_init__(self):
        if self.dtstamp is None:
            self.dtstamp = datetime.utcnow()
    
    def to_ical(self) -> str:
        """转换为 ICS 格式"""
        lines = ["BEGIN:VJOURNAL"]
        
        lines.append(f"UID:{self.uid}")
        lines.append(f"DTSTAMP:{_format_datetime_utc(self.dtstamp)}")
        
        if isinstance(self.dtstart, date) and not isinstance(self.dtstart, datetime):
            lines.append(f"DTSTART;VALUE=DATE:{_format_date(self.dtstart)}")
        else:
            lines.append(f"DTSTART:{_format_datetime_utc(self.dtstart)}")
        
        if self.summary:
            lines.append(f"SUMMARY:{_escape_text(self.summary)}")
        
        if self.description:
            lines.append(f"DESCRIPTION:{_escape_text(self.description)}")
        
        if self.categories:
            lines.append(f"CATEGORIES:{','.join(self.categories)}")
        
        lines.append("END:VJOURNAL")
        return "\n".join(lines)


@dataclass
class VCalendar:
    """日历对象"""
    events: List[VEvent] = field(default_factory=list)
    todos: List[VTodo] = field(default_factory=list)
    journals: List[VJournal] = field(default_factory=list)
    prodid: str = "-//AllToolkit//iCalendar Utils//EN"
    version: str = "2.0"
    calscale: str = "GREGORIAN"
    method: Optional[str] = None  # PUBLISH, REQUEST, REPLY, CANCEL, etc.
    name: Optional[str] = None
    description: Optional[str] = None
    timezone: str = "UTC"
    
    def add_event(self, event: VEvent) -> None:
        """添加事件"""
        self.events.append(event)
    
    def add_todo(self, todo: VTodo) -> None:
        """添加待办"""
        self.todos.append(todo)
    
    def add_journal(self, journal: VJournal) -> None:
        """添加日志"""
        self.journals.append(journal)
    
    def to_ical(self) -> str:
        """生成完整的 ICS 文件内容"""
        lines = ["BEGIN:VCALENDAR"]
        lines.append(f"PRODID:{self.prodid}")
        lines.append(f"VERSION:{self.version}")
        lines.append(f"CALSCALE:{self.calscale}")
        
        if self.method:
            lines.append(f"METHOD:{self.method}")
        
        if self.name:
            lines.append(f"X-WR-CALNAME:{_escape_text(self.name)}")
        
        if self.description:
            lines.append(f"X-WR-CALDESC:{_escape_text(self.description)}")
        
        if self.timezone and self.timezone != "UTC":
            lines.append(f"X-WR-TIMEZONE:{self.timezone}")
        
        # Add timezone component if needed
        if self.timezone and self.timezone != "UTC":
            lines.extend(_generate_vtimezone(self.timezone))
        
        # Add all components
        for event in self.events:
            lines.append(event.to_ical())
        
        for todo in self.todos:
            lines.append(todo.to_ical())
        
        for journal in self.journals:
            lines.append(journal.to_ical())
        
        lines.append("END:VCALENDAR")
        
        return "\n".join(lines)


# === Helper Functions ===

def _format_datetime_utc(dt: datetime) -> str:
    """格式化为 UTC 时间 (YYYYMMDDTHHMMSSZ)"""
    return dt.strftime("%Y%m%dT%H%M%SZ")


def _format_datetime_local(dt: datetime) -> str:
    """格式化为本地时间 (YYYYMMDDTHHMMSS)"""
    return dt.strftime("%Y%m%dT%H%M%S")


def _format_date(d: Union[date, datetime]) -> str:
    """格式化为日期 (YYYYMMDD)"""
    if isinstance(d, datetime):
        return d.strftime("%Y%m%d")
    return d.strftime("%Y%m%d")


def _format_duration(td: timedelta) -> str:
    """格式化时间间隔"""
    total_seconds = int(td.total_seconds())
    days = total_seconds // 86400
    remaining = total_seconds % 86400
    hours = remaining // 3600
    remaining %= 3600
    minutes = remaining // 60
    seconds = remaining % 60
    
    parts = ["P"]
    if days > 0:
        parts.append(f"{days}D")
    
    if hours or minutes or seconds:
        parts.append("T")
        if hours:
            parts.append(f"{hours}H")
        if minutes:
            parts.append(f"{minutes}M")
        if seconds:
            parts.append(f"{seconds}S")
    
    return "".join(parts)


def _escape_text(text: str) -> str:
    """转义 ICS 文本中的特殊字符"""
    text = text.replace("\\", "\\\\")
    text = text.replace(",", "\\,")
    text = text.replace(";", "\\;")
    text = text.replace("\n", "\\n")
    # 注意: 冒号在 RFC 5545 中在属性值内不需要转义
    # 只有在属性名和参数值中才需要转义
    return text


def _unescape_text(text: str) -> str:
    """反转义 ICS 文本"""
    text = text.replace("\\n", "\n")
    text = text.replace("\\;", ";")
    text = text.replace("\\,", ",")
    text = text.replace("\\\\", "\\")
    return text


def _generate_vtimezone(tzid: str) -> List[str]:
    """生成简单的 VTIMEZONE 组件"""
    # 简化版本，只包含基本信息
    return [
        "BEGIN:VTIMEZONE",
        f"TZID:{tzid}",
        "END:VTIMEZONE"
    ]


# === Parsing Functions ===

def _parse_datetime(value: str, params: Dict[str, str] = None) -> Union[datetime, date]:
    """解析日期时间"""
    params = params or {}
    
    # 移除尾随 Z
    if value.endswith("Z"):
        value = value[:-1]
        try:
            return datetime.strptime(value, "%Y%m%dT%H%M%S")
        except ValueError:
            pass
    
    # 纯日期
    if len(value) == 8:
        return datetime.strptime(value, "%Y%m%d").date()
    
    # 日期时间
    try:
        return datetime.strptime(value, "%Y%m%dT%H%M%S")
    except ValueError:
        pass
    
    raise ValueError(f"无法解析日期时间: {value}")


def _parse_property(line: str) -> Tuple[str, Dict[str, str], str]:
    """解析属性行，返回 (名称, 参数字典, 值)"""
    # 格式: NAME;PARAM1=VALUE1;PARAM2=VALUE2:PROPERTY_VALUE
    if ":" not in line:
        return line, {}, ""
    
    colon_pos = line.index(":")
    name_params = line[:colon_pos]
    value = line[colon_pos + 1:]
    
    params = {}
    if ";" in name_params:
        parts = name_params.split(";")
        name = parts[0]
        for param in parts[1:]:
            if "=" in param:
                pk, pv = param.split("=", 1)
                params[pk] = pv
    else:
        name = name_params
    
    return name, params, value


def _fold_line(line: str, max_length: int = 75) -> str:
    """按 RFC 5545 规则折叠长行"""
    if len(line) <= max_length:
        return line
    
    result = []
    current_line = ""
    
    for char in line:
        if len(current_line.encode('utf-8')) >= max_length:
            result.append(current_line)
            current_line = " " + char
        else:
            current_line += char
    
    if current_line:
        result.append(current_line)
    
    return "\r\n".join(result)


def _unfold_lines(content: str) -> List[str]:
    """展开折叠的行"""
    lines = []
    current = ""
    
    for line in content.replace("\r\n", "\n").split("\n"):
        if line.startswith(" ") or line.startswith("\t"):
            current += line[1:]
        else:
            if current:
                lines.append(current)
            current = line
    
    if current:
        lines.append(current)
    
    return lines


def parse_ical(content: str) -> VCalendar:
    """解析 ICS 文件内容"""
    lines = _unfold_lines(content)
    calendar = VCalendar()
    
    current_component = None
    component_data = {}
    
    for line in lines:
        if not line.strip():
            continue
        
        name, params, value = _parse_property(line)
        name = name.upper()
        
        if name == "BEGIN":
            if value == "VCALENDAR":
                continue
            elif value == "VEVENT":
                current_component = "VEVENT"
                component_data = {}
            elif value == "VTODO":
                current_component = "VTODO"
                component_data = {}
            elif value == "VJOURNAL":
                current_component = "VJOURNAL"
                component_data = {}
            elif value == "VALARM":
                # 跳过 VALARM 解析
                pass
        elif name == "END":
            if value == "VCALENDAR":
                break
            elif current_component == "VEVENT" and value == "VEVENT":
                event = _build_event(component_data)
                calendar.events.append(event)
                current_component = None
            elif current_component == "VTODO" and value == "VTODO":
                todo = _build_todo(component_data)
                calendar.todos.append(todo)
                current_component = None
            elif current_component == "VJOURNAL" and value == "VJOURNAL":
                journal = _build_journal(component_data)
                calendar.journals.append(journal)
                current_component = None
        elif current_component:
            # 存储组件属性
            key = f"{name}_{params.get('TZID', '')}" if params.get('TZID') else name
            if key in component_data:
                if isinstance(component_data[key], list):
                    component_data[key].append((value, params))
                else:
                    component_data[key] = [component_data[key], (value, params)]
            else:
                component_data[key] = (value, params)
        else:
            # 日历级属性
            if name == "PRODID":
                calendar.prodid = value
            elif name == "VERSION":
                calendar.version = value
            elif name == "CALSCALE":
                calendar.calscale = value
            elif name == "METHOD":
                calendar.method = value
            elif name == "X-WR-CALNAME":
                calendar.name = _unescape_text(value)
            elif name == "X-WR-CALDESC":
                calendar.description = _unescape_text(value)
            elif name == "X-WR-TIMEZONE":
                calendar.timezone = value
    
    return calendar


def _build_event(data: Dict) -> VEvent:
    """从解析数据构建事件"""
    def get_value(key):
        if key in data:
            val = data[key]
            if isinstance(val, tuple):
                return val[0], val[1]
            return val[0] if isinstance(val, list) else val, {}
        return None, {}
    
    uid, _ = get_value("UID")
    summary, _ = get_value("SUMMARY")
    description, _ = get_value("DESCRIPTION")
    location, _ = get_value("LOCATION")
    status, _ = get_value("STATUS")
    priority, _ = get_value("PRIORITY")
    url, _ = get_value("URL")
    organizer, organizer_params = get_value("ORGANIZER")
    
    # 解析日期
    dtstart_val, dtstart_params = get_value("DTSTART")
    dtend_val, dtend_params = get_value("DTEND")
    
    dtstart = None
    dtend = None
    is_all_day = False
    
    if dtstart_val:
        is_all_day = dtstart_params.get("VALUE") == "DATE"
        dtstart = _parse_datetime(dtstart_val, dtstart_params)
    
    if dtend_val:
        dtend = _parse_datetime(dtend_val, dtend_params)
    
    return VEvent(
        uid=uid or "",
        dtstart=dtstart or datetime.utcnow(),
        dtend=dtend,
        summary=_unescape_text(summary) if summary else "",
        description=_unescape_text(description) if description else "",
        location=_unescape_text(location) if location else "",
        status=status or "CONFIRMED",
        priority=int(priority) if priority else None,
        url=url,
        is_all_day=is_all_day,
        organizer=organizer.replace("mailto:", "") if organizer else None,
        organizer_name=_unescape_text(organizer_params.get("CN", "")) if organizer_params else None
    )


def _build_todo(data: Dict) -> VTodo:
    """从解析数据构建待办"""
    def get_value(key):
        if key in data:
            val = data[key]
            if isinstance(val, tuple):
                return val[0]
            return val[0] if isinstance(val, list) else val
        return None
    
    uid = get_value("UID")
    summary = get_value("SUMMARY")
    description = get_value("DESCRIPTION")
    status = get_value("STATUS")
    priority = get_value("PRIORITY")
    percent_complete = get_value("PERCENT-COMPLETE")
    
    dtstart_val = get_value("DTSTART")
    due_val = get_value("DUE")
    completed_val = get_value("COMPLETED")
    
    dtstart = _parse_datetime(dtstart_val) if dtstart_val else None
    due = _parse_datetime(due_val) if due_val else None
    completed = _parse_datetime(completed_val) if completed_val else None
    
    return VTodo(
        uid=uid or "",
        dtstart=dtstart,
        due=due,
        summary=_unescape_text(summary) if summary else "",
        description=_unescape_text(description) if description else "",
        status=status or "NEEDS-ACTION",
        priority=int(priority) if priority else None,
        percent_complete=int(percent_complete) if percent_complete else None,
        completed=completed
    )


def _build_journal(data: Dict) -> VJournal:
    """从解析数据构建日志"""
    def get_value(key):
        if key in data:
            val = data[key]
            if isinstance(val, tuple):
                return val[0]
            return val[0] if isinstance(val, list) else val
        return None
    
    uid = get_value("UID")
    summary = get_value("SUMMARY")
    description = get_value("DESCRIPTION")
    dtstart_val = get_value("DTSTART")
    
    dtstart = _parse_datetime(dtstart_val) if dtstart_val else date.today()
    
    return VJournal(
        uid=uid or "",
        dtstart=dtstart,
        summary=_unescape_text(summary) if summary else "",
        description=_unescape_text(description) if description else ""
    )


# === Convenience Functions ===

def create_event(
    summary: str,
    dtstart: Union[datetime, date],
    dtend: Optional[Union[datetime, date]] = None,
    duration_hours: Optional[float] = None,
    description: str = "",
    location: str = "",
    uid: Optional[str] = None,
    timezone: str = "UTC"
) -> VEvent:
    """快速创建事件的便捷函数
    
    Args:
        summary: 事件标题
        dtstart: 开始时间
        dtend: 结束时间 (可选)
        duration_hours: 持续时间 (小时) (可选，与 dtend 互斥)
        description: 描述
        location: 地点
        uid: 唯一标识符 (可选，自动生成)
        timezone: 时区
    """
    duration = None
    if dtend is None and duration_hours is not None:
        if isinstance(dtstart, datetime):
            duration = timedelta(hours=duration_hours)
            dtend = dtstart + duration
        else:
            # 对于日期类型，duration_hours 表示天数
            dtend = dtstart
    
    if uid is None:
        import uuid
        uid = str(uuid.uuid4())
    
    return VEvent(
        uid=uid,
        dtstart=dtstart,
        dtend=dtend,
        duration=duration,
        summary=summary,
        description=description,
        location=location,
        timezone=timezone
    )


def create_todo(
    summary: str,
    due: Optional[Union[datetime, date]] = None,
    priority: Optional[int] = None,
    uid: Optional[str] = None
) -> VTodo:
    """快速创建待办的便捷函数"""
    if uid is None:
        import uuid
        uid = str(uuid.uuid4())
    
    return VTodo(
        uid=uid,
        due=due,
        summary=summary,
        priority=priority
    )


def create_daily_recurring_event(
    summary: str,
    dtstart: datetime,
    interval: int = 1,
    count: Optional[int] = None,
    until: Optional[datetime] = None
) -> VEvent:
    """创建每日重复事件"""
    import uuid
    return VEvent(
        uid=str(uuid.uuid4()),
        dtstart=dtstart,
        summary=summary,
        rrule=RecurrenceRule(
            frequency=Frequency.DAILY,
            interval=interval,
            count=count,
            until=until
        )
    )


def create_weekly_recurring_event(
    summary: str,
    dtstart: datetime,
    by_day: List[WeekDay],
    interval: int = 1,
    count: Optional[int] = None
) -> VEvent:
    """创建每周重复事件"""
    import uuid
    return VEvent(
        uid=str(uuid.uuid4()),
        dtstart=dtstart,
        summary=summary,
        rrule=RecurrenceRule(
            frequency=Frequency.WEEKLY,
            interval=interval,
            by_day=by_day,
            count=count
        )
    )


def save_calendar(calendar: VCalendar, filepath: str) -> None:
    """保存日历到文件"""
    content = calendar.to_ical()
    # 应用行折叠
    lines = content.split("\n")
    folded_lines = [_fold_line(line) for line in lines]
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\r\n".join(folded_lines))


def load_calendar(filepath: str) -> VCalendar:
    """从文件加载日历"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    return parse_ical(content)


# === Module Exports ===

__all__ = [
    # Classes
    "VCalendar",
    "VEvent",
    "VTodo",
    "VJournal",
    "RecurrenceRule",
    "Frequency",
    "WeekDay",
    # Functions
    "parse_ical",
    "create_event",
    "create_todo",
    "create_daily_recurring_event",
    "create_weekly_recurring_event",
    "save_calendar",
    "load_calendar",
]