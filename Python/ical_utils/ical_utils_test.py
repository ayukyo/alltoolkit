"""
iCalendar Utilities 测试文件

测试所有核心功能：
- 事件创建和序列化
- 待办事项
- 日志条目
- 重复规则
- ICS 解析
- 文件读写
"""

import sys
import unittest
from datetime import datetime, date, timedelta
import os
import tempfile


# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    VCalendar, VEvent, VTodo, VJournal, RecurrenceRule,
    Frequency, WeekDay,
    parse_ical, create_event, create_todo,
    create_daily_recurring_event, create_weekly_recurring_event,
    save_calendar, load_calendar
)


class TestVEvent(unittest.TestCase):
    """测试事件功能"""
    
    def test_basic_event(self):
        """测试基本事件创建"""
        event = VEvent(
            uid="test-001",
            dtstart=datetime(2025, 1, 15, 10, 0),
            dtend=datetime(2025, 1, 15, 11, 0),
            summary="Team Meeting",
            description="Weekly team sync",
            location="Conference Room A"
        )
        
        ical = event.to_ical()
        self.assertIn("BEGIN:VEVENT", ical)
        self.assertIn("UID:test-001", ical)
        self.assertIn("SUMMARY:Team Meeting", ical)
        self.assertIn("DESCRIPTION:Weekly team sync", ical)
        self.assertIn("LOCATION:Conference Room A", ical)
        self.assertIn("END:VEVENT", ical)
    
    def test_all_day_event(self):
        """测试全天事件"""
        event = VEvent(
            uid="test-002",
            dtstart=date(2025, 1, 15),
            summary="Birthday Party"
        )
        
        ical = event.to_ical()
        self.assertIn("DTSTART;VALUE=DATE:20250115", ical)
        self.assertTrue(event.is_all_day)
    
    def test_event_with_duration(self):
        """测试使用持续时间的事件"""
        event = VEvent(
            uid="test-003",
            dtstart=datetime(2025, 1, 15, 14, 0),
            duration=timedelta(hours=1, minutes=30),
            summary="Workshop"
        )
        
        ical = event.to_ical()
        self.assertIn("DURATION:PT1H30M", ical)
    
    def test_event_with_organizer(self):
        """测试包含组织者的事件"""
        event = VEvent(
            uid="test-004",
            dtstart=datetime(2025, 1, 15, 10, 0),
            summary="Project Kickoff",
            organizer="boss@company.com",
            organizer_name="The Boss"
        )
        
        ical = event.to_ical()
        self.assertIn("ORGANIZER;CN=The Boss:mailto:boss@company.com", ical)
    
    def test_event_with_attendees(self):
        """测试包含参会者的事件"""
        event = VEvent(
            uid="test-005",
            dtstart=datetime(2025, 1, 15, 10, 0),
            summary="Review Meeting",
            attendees=[
                ("alice@example.com", "Alice"),
                ("bob@example.com", None),
            ]
        )
        
        ical = event.to_ical()
        self.assertIn("ATTENDEE;CN=Alice;RSVP=TRUE:mailto:alice@example.com", ical)
        self.assertIn("ATTENDEE;RSVP=TRUE:mailto:bob@example.com", ical)
    
    def test_event_with_categories(self):
        """测试包含分类的事件"""
        event = VEvent(
            uid="test-006",
            dtstart=datetime(2025, 1, 15, 10, 0),
            summary="Important Meeting",
            categories=["WORK", "IMPORTANT", "PROJECT-X"]
        )
        
        ical = event.to_ical()
        self.assertIn("CATEGORIES:WORK,IMPORTANT,PROJECT-X", ical)
    
    def test_event_with_alarm(self):
        """测试包含提醒的事件"""
        event = VEvent(
            uid="test-007",
            dtstart=datetime(2025, 1, 15, 10, 0),
            summary="Important Event",
            alarms=[15, 60]  # 15分钟和1小时前提醒
        )
        
        ical = event.to_ical()
        self.assertIn("BEGIN:VALARM", ical)
        self.assertIn("TRIGGER:-PT15M", ical)
        self.assertIn("TRIGGER:-PT60M", ical)
        self.assertIn("END:VALARM", ical)
    
    def test_event_status(self):
        """测试事件状态"""
        event_confirmed = VEvent(
            uid="test-008",
            dtstart=datetime(2025, 1, 15, 10, 0),
            summary="Meeting",
            status="CONFIRMED"
        )
        self.assertIn("STATUS:CONFIRMED", event_confirmed.to_ical())
        
        event_cancelled = VEvent(
            uid="test-009",
            dtstart=datetime(2025, 1, 15, 10, 0),
            summary="Cancelled Meeting",
            status="CANCELLED"
        )
        self.assertIn("STATUS:CANCELLED", event_cancelled.to_ical())


class TestRecurrenceRule(unittest.TestCase):
    """测试重复规则"""
    
    def test_daily_recurrence(self):
        """测试每日重复"""
        rrule = RecurrenceRule(
            frequency=Frequency.DAILY,
            interval=2,
            count=10
        )
        
        ical = rrule.to_ical()
        self.assertIn("FREQ=DAILY", ical)
        self.assertIn("INTERVAL=2", ical)
        self.assertIn("COUNT=10", ical)
    
    def test_weekly_recurrence(self):
        """测试每周重复"""
        rrule = RecurrenceRule(
            frequency=Frequency.WEEKLY,
            by_day=[WeekDay.MO, WeekDay.WE, WeekDay.FR]
        )
        
        ical = rrule.to_ical()
        self.assertIn("FREQ=WEEKLY", ical)
        self.assertIn("BYDAY=MO,WE,FR", ical)
    
    def test_monthly_recurrence(self):
        """测试每月重复"""
        rrule = RecurrenceRule(
            frequency=Frequency.MONTHLY,
            by_month_day=[1, 15],
            count=12
        )
        
        ical = rrule.to_ical()
        self.assertIn("FREQ=MONTHLY", ical)
        self.assertIn("BYMONTHDAY=1,15", ical)
    
    def test_yearly_recurrence(self):
        """测试每年重复"""
        rrule = RecurrenceRule(
            frequency=Frequency.YEARLY,
            by_month=[1, 7],
            by_month_day=[1]
        )
        
        ical = rrule.to_ical()
        self.assertIn("FREQ=YEARLY", ical)
        self.assertIn("BYMONTH=1,7", ical)
    
    def test_recurrence_with_until(self):
        """测试带结束日期的重复"""
        rrule = RecurrenceRule(
            frequency=Frequency.DAILY,
            until=datetime(2025, 12, 31, 23, 59, 59)
        )
        
        ical = rrule.to_ical()
        self.assertIn("UNTIL=20251231T235959Z", ical)
    
    def test_event_with_recurrence(self):
        """测试带重复规则的事件"""
        event = VEvent(
            uid="test-recurring",
            dtstart=datetime(2025, 1, 15, 10, 0),
            summary="Weekly Standup",
            rrule=RecurrenceRule(
                frequency=Frequency.WEEKLY,
                by_day=[WeekDay.MO, WeekDay.WE, WeekDay.FR],
                count=20
            )
        )
        
        ical = event.to_ical()
        self.assertIn("RRULE:FREQ=WEEKLY", ical)
        self.assertIn("BYDAY=MO,WE,FR", ical)
        self.assertIn("COUNT=20", ical)


class TestVTodo(unittest.TestCase):
    """测试待办事项"""
    
    def test_basic_todo(self):
        """测试基本待办"""
        todo = VTodo(
            uid="todo-001",
            summary="Buy groceries",
            priority=3
        )
        
        ical = todo.to_ical()
        self.assertIn("BEGIN:VTODO", ical)
        self.assertIn("UID:todo-001", ical)
        self.assertIn("SUMMARY:Buy groceries", ical)
        self.assertIn("PRIORITY:3", ical)
        self.assertIn("STATUS:NEEDS-ACTION", ical)
        self.assertIn("END:VTODO", ical)
    
    def test_todo_with_due_date(self):
        """测试带截止日期的待办"""
        todo = VTodo(
            uid="todo-002",
            summary="Submit report",
            due=datetime(2025, 1, 20, 17, 0)
        )
        
        ical = todo.to_ical()
        self.assertIn("DUE:20250120T170000Z", ical)
    
    def test_todo_progress(self):
        """测试待办进度"""
        todo = VTodo(
            uid="todo-003",
            summary="Complete project",
            percent_complete=75,
            status="IN-PROCESS"
        )
        
        ical = todo.to_ical()
        self.assertIn("PERCENT-COMPLETE:75", ical)
        self.assertIn("STATUS:IN-PROCESS", ical)
    
    def test_completed_todo(self):
        """测试已完成的待办"""
        todo = VTodo(
            uid="todo-004",
            summary="Done task",
            status="COMPLETED",
            completed=datetime(2025, 1, 15, 16, 30)
        )
        
        ical = todo.to_ical()
        self.assertIn("STATUS:COMPLETED", ical)
        self.assertIn("COMPLETED:20250115T163000Z", ical)


class TestVJournal(unittest.TestCase):
    """测试日志条目"""
    
    def test_basic_journal(self):
        """测试基本日志"""
        journal = VJournal(
            uid="journal-001",
            dtstart=date(2025, 1, 15),
            summary="Daily Notes",
            description="Today was productive!"
        )
        
        ical = journal.to_ical()
        self.assertIn("BEGIN:VJOURNAL", ical)
        self.assertIn("UID:journal-001", ical)
        self.assertIn("SUMMARY:Daily Notes", ical)
        self.assertIn("DESCRIPTION:Today was productive!", ical)
        self.assertIn("END:VJOURNAL", ical)


class TestVCalendar(unittest.TestCase):
    """测试日历对象"""
    
    def test_empty_calendar(self):
        """测试空日历"""
        calendar = VCalendar()
        ical = calendar.to_ical()
        
        self.assertIn("BEGIN:VCALENDAR", ical)
        self.assertIn("VERSION:2.0", ical)
        self.assertIn("CALSCALE:GREGORIAN", ical)
        self.assertIn("END:VCALENDAR", ical)
    
    def test_calendar_with_name(self):
        """测试带名称的日历"""
        calendar = VCalendar(
            name="My Calendar",
            description="Personal events"
        )
        ical = calendar.to_ical()
        
        self.assertIn("X-WR-CALNAME:My Calendar", ical)
        self.assertIn("X-WR-CALDESC:Personal events", ical)
    
    def test_calendar_with_multiple_events(self):
        """测试包含多个事件的日历"""
        calendar = VCalendar()
        calendar.add_event(VEvent(
            uid="event-1",
            dtstart=datetime(2025, 1, 15, 9, 0),
            summary="Morning Meeting"
        ))
        calendar.add_event(VEvent(
            uid="event-2",
            dtstart=datetime(2025, 1, 15, 14, 0),
            summary="Afternoon Review"
        ))
        calendar.add_todo(VTodo(
            uid="todo-1",
            summary="Task"
        ))
        
        ical = calendar.to_ical()
        self.assertEqual(ical.count("BEGIN:VEVENT"), 2)
        self.assertEqual(ical.count("BEGIN:VTODO"), 1)


class TestParsing(unittest.TestCase):
    """测试 ICS 解析"""
    
    def test_parse_basic_event(self):
        """测试解析基本事件"""
        ics_content = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Test//Test//EN
BEGIN:VEVENT
UID:parse-test-001
DTSTAMP:20250115T100000Z
DTSTART:20250115T140000Z
DTEND:20250115T150000Z
SUMMARY:Parsed Event
DESCRIPTION:This is a parsed event
LOCATION:Office
END:VEVENT
END:VCALENDAR"""
        
        calendar = parse_ical(ics_content)
        
        self.assertEqual(len(calendar.events), 1)
        event = calendar.events[0]
        
        self.assertEqual(event.uid, "parse-test-001")
        self.assertEqual(event.summary, "Parsed Event")
        self.assertEqual(event.description, "This is a parsed event")
        self.assertEqual(event.location, "Office")
        self.assertEqual(event.dtstart.year, 2025)
        self.assertEqual(event.dtstart.month, 1)
        self.assertEqual(event.dtstart.day, 15)
    
    def test_parse_all_day_event(self):
        """测试解析全天事件"""
        ics_content = """BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
UID:parse-test-002
DTSTAMP:20250115T100000Z
DTSTART;VALUE=DATE:20250115
SUMMARY:All Day Event
END:VEVENT
END:VCALENDAR"""
        
        calendar = parse_ical(ics_content)
        event = calendar.events[0]
        
        self.assertTrue(event.is_all_day)
        self.assertIsInstance(event.dtstart, date)
    
    def test_parse_todo(self):
        """测试解析待办"""
        ics_content = """BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VTODO
UID:parse-todo-001
DTSTAMP:20250115T100000Z
SUMMARY:Task to do
PRIORITY:3
PERCENT-COMPLETE:50
STATUS:IN-PROCESS
END:VTODO
END:VCALENDAR"""
        
        calendar = parse_ical(ics_content)
        
        self.assertEqual(len(calendar.todos), 1)
        todo = calendar.todos[0]
        
        self.assertEqual(todo.uid, "parse-todo-001")
        self.assertEqual(todo.summary, "Task to do")
        self.assertEqual(todo.priority, 3)
        self.assertEqual(todo.percent_complete, 50)
    
    def test_parse_journal(self):
        """测试解析日志"""
        ics_content = """BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VJOURNAL
UID:parse-journal-001
DTSTAMP:20250115T100000Z
DTSTART:20250115
SUMMARY:Daily Entry
DESCRIPTION:Journal content
END:VJOURNAL
END:VCALENDAR"""
        
        calendar = parse_ical(ics_content)
        
        self.assertEqual(len(calendar.journals), 1)
        journal = calendar.journals[0]
        
        self.assertEqual(journal.summary, "Daily Entry")
        self.assertEqual(journal.description, "Journal content")


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_create_event(self):
        """测试快速创建事件"""
        event = create_event(
            summary="Quick Event",
            dtstart=datetime(2025, 1, 15, 10, 0),
            duration_hours=2,
            description="Created with helper function",
            location="Room 101"
        )
        
        self.assertIsNotNone(event.uid)
        self.assertEqual(event.summary, "Quick Event")
        self.assertEqual(event.duration, timedelta(hours=2))
        self.assertEqual(event.location, "Room 101")
    
    def test_create_todo(self):
        """测试快速创建待办"""
        todo = create_todo(
            summary="Quick Task",
            due=datetime(2025, 1, 20, 17, 0),
            priority=2
        )
        
        self.assertIsNotNone(todo.uid)
        self.assertEqual(todo.summary, "Quick Task")
        self.assertEqual(todo.priority, 2)
    
    def test_create_daily_recurring_event(self):
        """测试创建每日重复事件"""
        event = create_daily_recurring_event(
            summary="Daily Standup",
            dtstart=datetime(2025, 1, 15, 9, 0),
            interval=1,
            count=30
        )
        
        self.assertIsNotNone(event.uid)
        self.assertEqual(event.rrule.frequency, Frequency.DAILY)
        self.assertEqual(event.rrule.interval, 1)
        self.assertEqual(event.rrule.count, 30)
    
    def test_create_weekly_recurring_event(self):
        """测试创建每周重复事件"""
        event = create_weekly_recurring_event(
            summary="Weekly Meeting",
            dtstart=datetime(2025, 1, 15, 14, 0),
            by_day=[WeekDay.MO, WeekDay.FR]
        )
        
        self.assertEqual(event.rrule.frequency, Frequency.WEEKLY)
        self.assertEqual(event.rrule.by_day, [WeekDay.MO, WeekDay.FR])


class TestFileOperations(unittest.TestCase):
    """测试文件操作"""
    
    def test_save_and_load_calendar(self):
        """测试保存和加载日历"""
        calendar = VCalendar(name="Test Calendar")
        calendar.add_event(VEvent(
            uid="file-test-001",
            dtstart=datetime(2025, 1, 15, 10, 0),
            dtend=datetime(2025, 1, 15, 11, 0),
            summary="File Test Event"
        ))
        calendar.add_todo(VTodo(
            uid="file-todo-001",
            summary="File Test Todo"
        ))
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ics', delete=False) as f:
            temp_path = f.name
        
        try:
            save_calendar(calendar, temp_path)
            
            self.assertTrue(os.path.exists(temp_path))
            
            loaded = load_calendar(temp_path)
            
            self.assertEqual(len(loaded.events), 1)
            self.assertEqual(len(loaded.todos), 1)
            self.assertEqual(loaded.events[0].summary, "File Test Event")
            self.assertEqual(loaded.todos[0].summary, "File Test Todo")
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_special_characters_escaping(self):
        """测试特殊字符转义"""
        event = VEvent(
            uid="special-001",
            dtstart=datetime(2025, 1, 15, 10, 0),
            summary="Meeting: Important!",  # 冒号在属性值中不需要转义
            description="Attendees: Alice, Bob\nLocation: Room A; Building B"
        )
        
        ical = event.to_ical()
        
        # 冒号在属性值中是正常的，不需要转义
        self.assertIn("SUMMARY:Meeting: Important!", ical)
        self.assertIn("\\,", ical)  # 逗号转义
        self.assertIn("\\;", ical)  # 分号转义
        self.assertIn("\\n", ical)  # 换行转义
    
    def test_url_in_event(self):
        """测试事件中的 URL"""
        event = VEvent(
            uid="url-001",
            dtstart=datetime(2025, 1, 15, 10, 0),
            summary="Online Meeting",
            url="https://meeting.example.com/room/123"
        )
        
        ical = event.to_ical()
        self.assertIn("URL:https://meeting.example.com/room/123", ical)
    
    def test_timezone_support(self):
        """测试时区支持"""
        event = VEvent(
            uid="tz-001",
            dtstart=datetime(2025, 1, 15, 10, 0),
            summary="Beijing Meeting",
            timezone="Asia/Shanghai"
        )
        
        ical = event.to_ical()
        self.assertIn("TZID=Asia/Shanghai", ical)


class TestDurationFormatting(unittest.TestCase):
    """测试持续时间格式化"""
    
    def test_format_duration(self):
        """测试持续时间格式化"""
        from mod import _format_duration
        
        self.assertEqual(_format_duration(timedelta(hours=1)), "PT1H")
        self.assertEqual(_format_duration(timedelta(minutes=30)), "PT30M")
        self.assertEqual(_format_duration(timedelta(seconds=45)), "PT45S")
        self.assertEqual(_format_duration(timedelta(hours=2, minutes=30)), "PT2H30M")
        self.assertEqual(_format_duration(timedelta(days=1, hours=2, minutes=30)), "P1DT2H30M")


if __name__ == "__main__":
    unittest.main()