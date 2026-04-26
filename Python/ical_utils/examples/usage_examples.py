"""
iCalendar Utils 使用示例

演示各种日历操作场景：
1. 创建简单事件
2. 创建重复事件
3. 创建待办事项
4. 创建完整日历
5. 解析 ICS 文件
6. 高级用法
"""

from datetime import datetime, date, timedelta
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    VCalendar, VEvent, VTodo, VJournal, RecurrenceRule,
    Frequency, WeekDay,
    parse_ical, create_event, create_todo,
    create_daily_recurring_event, create_weekly_recurring_event,
    save_calendar, load_calendar
)


def example_1_basic_event():
    """示例 1: 创建基本事件"""
    print("\n" + "=" * 60)
    print("示例 1: 创建基本事件")
    print("=" * 60)
    
    event = VEvent(
        uid="meeting-001",
        dtstart=datetime(2025, 4, 27, 14, 0),  # 下午2点
        dtend=datetime(2025, 4, 27, 15, 30),    # 下午3:30
        summary="项目进度会议",
        description="讨论 Q2 季度目标和里程碑",
        location="会议室 A-301",
        organizer="manager@company.com",
        organizer_name="项目经理",
        attendees=[
            ("alice@company.com", "Alice"),
            ("bob@company.com", "Bob"),
            ("charlie@company.com", "Charlie"),
        ],
        categories=["WORK", "MEETING"],
        alarms=[15]  # 提前15分钟提醒
    )
    
    print("\n事件内容 (ICS 格式):")
    print("-" * 40)
    print(event.to_ical())


def example_2_all_day_event():
    """示例 2: 创建全天事件"""
    print("\n" + "=" * 60)
    print("示例 2: 创建全天事件")
    print("=" * 60)
    
    event = VEvent(
        uid="holiday-001",
        dtstart=date(2025, 5, 1),  # 只传日期，自动识别为全天事件
        dtend=date(2025, 5, 6),   # 结束日期（不含，实际是5月1-5日）
        summary="劳动节假期",
        description="放假休息",
        categories=["HOLIDAY"]
    )
    
    print(f"是否为全天事件: {event.is_all_day}")
    print("\n事件内容:")
    print("-" * 40)
    print(event.to_ical())


def example_3_recurring_events():
    """示例 3: 创建重复事件"""
    print("\n" + "=" * 60)
    print("示例 3: 创建重复事件")
    print("=" * 60)
    
    # 每日站会
    daily_standup = create_daily_recurring_event(
        summary="每日站会",
        dtstart=datetime(2025, 4, 27, 9, 30),
        interval=1,  # 每天
        count=30     # 共30次
    )
    print("\n每日站会 (30次):")
    print(daily_standup.to_ical()[:500] + "...")
    
    # 每周一、三、五的例会
    weekly_meeting = create_weekly_recurring_event(
        summary="部门例会",
        dtstart=datetime(2025, 4, 27, 14, 0),
        by_day=[WeekDay.MO, WeekDay.WE, WeekDay.FR]
    )
    print("\n\n每周一三五例会:")
    print(weekly_meeting.to_ical()[:500] + "...")
    
    # 每月最后一天发工资
    salary_day = VEvent(
        uid="salary-001",
        dtstart=datetime(2025, 5, 1, 10, 0),
        summary="发工资日",
        rrule=RecurrenceRule(
            frequency=Frequency.MONTHLY,
            by_month_day=[1],
            count=12
        )
    )
    print("\n\n每月1号发工资:")
    print(salary_day.to_ical()[:500] + "...")


def example_4_todos():
    """示例 4: 创建待办事项"""
    print("\n" + "=" * 60)
    print("示例 4: 创建待办事项")
    print("=" * 60)
    
    # 创建待办列表
    todos = [
        VTodo(
            uid="todo-001",
            summary="完成项目报告",
            due=datetime(2025, 4, 30, 18, 0),
            priority=1,  # 最高优先级
            categories=["WORK", "URGENT"]
        ),
        VTodo(
            uid="todo-002",
            summary="购买生日礼物",
            due=date(2025, 5, 5),
            priority=3,
            categories=["PERSONAL"]
        ),
        VTodo(
            uid="todo-003",
            summary="学习 Python",
            priority=5,
            percent_complete=60,
            status="IN-PROCESS"
        ),
    ]
    
    for i, todo in enumerate(todos, 1):
        print(f"\n待办 {i}:")
        print("-" * 40)
        print(todo.to_ical())


def example_5_journal():
    """示例 5: 创建日志/日记"""
    print("\n" + "=" * 60)
    print("示例 5: 创建日志/日记")
    print("=" * 60)
    
    journal = VJournal(
        uid="journal-001",
        dtstart=date(2025, 4, 27),
        summary="工作日志",
        description="""
今天完成了以下工作：
1. 完成了项目需求文档
2. 参加了团队会议
3. 解决了客户反馈的 bug

明天计划：
- 开始编码实现
- 编写测试用例
        """.strip(),
        categories=["WORK", "DIARY"]
    )
    
    print(journal.to_ical())


def example_6_complete_calendar():
    """示例 6: 创建完整日历"""
    print("\n" + "=" * 60)
    print("示例 6: 创建完整日历")
    print("=" * 60)
    
    # 创建日历
    calendar = VCalendar(
        name="我的工作日历",
        description="2025年工作安排",
        timezone="Asia/Shanghai"
    )
    
    # 添加事件
    calendar.add_event(VEvent(
        uid="work-001",
        dtstart=datetime(2025, 4, 28, 9, 0),
        dtend=datetime(2025, 4, 28, 10, 0),
        summary="周一例会",
        location="会议室1",
        rrule=RecurrenceRule(
            frequency=Frequency.WEEKLY,
            by_day=[WeekDay.MO]
        )
    ))
    
    calendar.add_event(VEvent(
        uid="work-002",
        dtstart=datetime(2025, 4, 28, 14, 0),
        dtend=datetime(2025, 4, 28, 17, 0),
        summary="项目评审",
        location="大会议室",
        attendees=[
            ("team@company.com", "开发团队"),
        ]
    ))
    
    # 添加待办
    calendar.add_todo(VTodo(
        uid="todo-work-001",
        summary="准备 PPT",
        due=datetime(2025, 4, 29, 12, 0),
        priority=1
    ))
    
    print("\n日历内容 (前1500字符):")
    print("-" * 40)
    ical = calendar.to_ical()
    print(ical[:1500])
    print(f"\n... (共 {len(ical)} 字符)")


def example_7_parse_ics():
    """示例 7: 解析 ICS 文件"""
    print("\n" + "=" * 60)
    print("示例 7: 解析 ICS 文件")
    print("=" * 60)
    
    # 模拟一个 ICS 文件内容
    ics_content = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example Corp.//CalDAV Client//EN
X-WR-CALNAME:我的日历
BEGIN:VEVENT
UID:19970901T130000Z-123401@example.com
DTSTAMP:19970901T130000Z
DTSTART:19970903T163000Z
DTEND:19970903T190000Z
SUMMARY:Annual Employee Review
CATEGORIES:BUSINESS,PERSONNEL
LOCATION:Conference Room - F123, Bldg. 1
BEGIN:VALARM
TRIGGER:-PT2H
ACTION:DISPLAY
DESCRIPTION:Annual Employee Review
END:VALARM
END:VEVENT
BEGIN:VTODO
UID:19970901T130000Z-123402@example.com
DTSTAMP:19970901T130000Z
SUMMARY:Submit Income Tax Form
DUE:19970415T000000
STATUS:NEEDS-ACTION
PRIORITY:2
END:VTODO
END:VCALENDAR"""
    
    # 解析
    calendar = parse_ical(ics_content)
    
    print(f"\n解析结果:")
    print(f"- 日历名称: {calendar.name}")
    print(f"- 事件数量: {len(calendar.events)}")
    print(f"- 待办数量: {len(calendar.todos)}")
    
    if calendar.events:
        event = calendar.events[0]
        print(f"\n事件详情:")
        print(f"- 主题: {event.summary}")
        print(f"- 地点: {event.location}")
        print(f"- 分类: {event.categories}")
    
    if calendar.todos:
        todo = calendar.todos[0]
        print(f"\n待办详情:")
        print(f"- 主题: {todo.summary}")
        print(f"- 优先级: {todo.priority}")


def example_8_file_operations():
    """示例 8: 文件读写操作"""
    print("\n" + "=" * 60)
    print("示例 8: 文件读写操作")
    print("=" * 60)
    
    import tempfile
    
    # 创建日历
    calendar = VCalendar(name="测试日历")
    calendar.add_event(create_event(
        summary="测试事件",
        dtstart=datetime(2025, 5, 1, 10, 0),
        duration_hours=1
    ))
    
    # 保存到临时文件
    with tempfile.NamedTemporaryFile(suffix=".ics", delete=False) as f:
        temp_path = f.name
    
    try:
        save_calendar(calendar, temp_path)
        print(f"✓ 已保存日历到: {temp_path}")
        
        # 读取文件内容
        with open(temp_path, "r") as f:
            content = f.read()
        print(f"\n文件内容 (前500字符):")
        print(content[:500])
        
        # 重新加载
        loaded = load_calendar(temp_path)
        print(f"\n✓ 成功重新加载日历")
        print(f"- 事件数量: {len(loaded.events)}")
        print(f"- 事件主题: {loaded.events[0].summary}")
    finally:
        import os
        if os.path.exists(temp_path):
            os.unlink(temp_path)
            print(f"\n✓ 已清理临时文件")


def example_9_advanced_rrule():
    """示例 9: 高级重复规则"""
    print("\n" + "=" * 60)
    print("示例 9: 高级重复规则")
    print("=" * 60)
    
    # 每月最后一个周五
    last_friday = VEvent(
        uid="last-friday",
        dtstart=datetime(2025, 5, 30, 18, 0),
        summary="月末总结会",
        rrule=RecurrenceRule(
            frequency=Frequency.MONTHLY,
            by_day=[WeekDay.FR],
            count=12
        )
    )
    print("每月最后一个周五:")
    print(last_friday.to_ical()[:400])
    
    # 工作日提醒 (周一到周五)
    workday_reminder = VEvent(
        uid="workday-reminder",
        dtstart=datetime(2025, 4, 27, 9, 0),
        summary="晨间提醒",
        rrule=RecurrenceRule(
            frequency=Frequency.WEEKLY,
            by_day=[WeekDay.MO, WeekDay.TU, WeekDay.WE, WeekDay.TH, WeekDay.FR]
        )
    )
    print("\n\n工作日提醒 (周一到周五):")
    print(workday_reminder.to_ical()[:400])
    
    # 每季度第一天
    quarterly = VEvent(
        uid="quarterly",
        dtstart=datetime(2025, 4, 1, 10, 0),
        summary="季度规划",
        rrule=RecurrenceRule(
            frequency=Frequency.YEARLY,
            by_month=[1, 4, 7, 10],
            by_month_day=[1]
        )
    )
    print("\n\n每季度第一天:")
    print(quarterly.to_ical()[:400])


def example_10_timezone_example():
    """示例 10: 时区处理"""
    print("\n" + "=" * 60)
    print("示例 10: 时区处理")
    print("=" * 60)
    
    # 北京时间会议
    beijing_meeting = VEvent(
        uid="beijing-meeting",
        dtstart=datetime(2025, 4, 27, 14, 0),  # 北京时间下午2点
        dtend=datetime(2025, 4, 27, 15, 0),
        summary="北京时间会议",
        timezone="Asia/Shanghai"
    )
    
    print("带时区的事件:")
    print(beijing_meeting.to_ical())
    
    # 带时区的日历
    calendar = VCalendar(
        name="国际会议",
        timezone="Asia/Shanghai"
    )
    calendar.add_event(beijing_meeting)
    
    print("\n带时区的日历:")
    print(calendar.to_ical()[:600])


def main():
    """运行所有示例"""
    print("=" * 60)
    print("iCalendar Utils 使用示例")
    print("=" * 60)
    
    examples = [
        example_1_basic_event,
        example_2_all_day_event,
        example_3_recurring_events,
        example_4_todos,
        example_5_journal,
        example_6_complete_calendar,
        example_7_parse_ics,
        example_8_file_operations,
        example_9_advanced_rrule,
        example_10_timezone_example,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n错误: {e}")
    
    print("\n" + "=" * 60)
    print("所有示例完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()