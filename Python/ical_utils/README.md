# Ical Utils


iCalendar (ICS) Utilities - 零外部依赖的日历格式处理工具

支持功能:
- 创建日历事件
- 解析 ICS 文件
- 生成符合 RFC 5545 标准的 ICS 文件
- 支持重复事件 (RRULE)
- 支持时区处理
- 支持 VTODO 和 VJOURNAL


## 功能

### 类

- **Frequency**: 重复频率
- **WeekDay**: 星期
- **RecurrenceRule**: 重复规则 (RRULE)
  方法: to_ical
- **VEvent**: 日历事件
  方法: to_ical
- **VTodo**: 待办事项
  方法: to_ical
- **VJournal**: 日记/日志条目
  方法: to_ical
- **VCalendar**: 日历对象
  方法: add_event, add_todo, add_journal, to_ical

### 函数

- **parse_ical(content**) - 解析 ICS 文件内容
- **create_event(summary, dtstart, dtend**, ...) - 快速创建事件的便捷函数
- **create_todo(summary, due, priority**, ...) - 快速创建待办的便捷函数
- **create_daily_recurring_event(summary, dtstart, interval**, ...) - 创建每日重复事件
- **create_weekly_recurring_event(summary, dtstart, by_day**, ...) - 创建每周重复事件
- **save_calendar(calendar, filepath**) - 保存日历到文件
- **load_calendar(filepath**) - 从文件加载日历
- **to_ical(self**) - 转换为 ICS 格式的 RRULE 字符串
- **to_ical(self**) - 转换为 ICS 格式
- **to_ical(self**) - 转换为 ICS 格式

... 共 18 个函数

## 使用示例

```python
from mod import parse_ical

# 使用 parse_ical
result = parse_ical()
```

## 测试

运行测试：

```bash
python *_test.py
```

## 文件结构

```
{module_name}/
├── mod.py              # 主模块
├── *_test.py           # 测试文件
├── README.md           # 本文档
└── examples/           # 示例代码
    └── usage_examples.py
```

---

**Last updated**: 2026-04-28
