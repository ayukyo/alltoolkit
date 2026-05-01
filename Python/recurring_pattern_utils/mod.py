"""
周期性模式工具模块 (Recurring Pattern Utils)

用于解析、处理和计算周期性模式的工具集。
支持多种周期性模式：每日、每周、每月、自定义间隔、cron风格表达式等。

零外部依赖，纯 Python 标准库实现。

主要功能:
- 解析自然语言周期模式
- 解析类 cron 表达式
- 计算下一个/上一个触发时间
- 验证模式有效性
- 计算指定时间范围内的所有触发时间
- 支持复杂组合模式
"""

from datetime import datetime, timedelta, date
from typing import List, Optional, Tuple, Set, Dict, Any
import re
from enum import Enum


class PatternType(Enum):
    """周期模式类型"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    INTERVAL = "interval"
    CRON = "cron"
    CUSTOM = "custom"


class Weekday(Enum):
    """星期枚举"""
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


# 中文名称到 Weekday 的映射
WEEKDAY_CN_MAP = {
    '一': Weekday.MONDAY, '周一': Weekday.MONDAY, '星期一': Weekday.MONDAY,
    '二': Weekday.TUESDAY, '周二': Weekday.TUESDAY, '星期二': Weekday.TUESDAY,
    '三': Weekday.WEDNESDAY, '周三': Weekday.WEDNESDAY, '星期三': Weekday.WEDNESDAY,
    '四': Weekday.THURSDAY, '周四': Weekday.THURSDAY, '星期四': Weekday.THURSDAY,
    '五': Weekday.FRIDAY, '周五': Weekday.FRIDAY, '星期五': Weekday.FRIDAY,
    '六': Weekday.SATURDAY, '周六': Weekday.SATURDAY, '星期六': Weekday.SATURDAY,
    '日': Weekday.SUNDAY, '周日': Weekday.SUNDAY, '星期日': Weekday.SUNDAY,
    '天': Weekday.SUNDAY, '周天': Weekday.SUNDAY, '星期天': Weekday.SUNDAY,
}

# 英文名称到 Weekday 的映射
WEEKDAY_EN_MAP = {
    'mon': Weekday.MONDAY, 'monday': Weekday.MONDAY,
    'tue': Weekday.TUESDAY, 'tuesday': Weekday.TUESDAY,
    'wed': Weekday.WEDNESDAY, 'wednesday': Weekday.WEDNESDAY,
    'thu': Weekday.THURSDAY, 'thursday': Weekday.THURSDAY,
    'fri': Weekday.FRIDAY, 'friday': Weekday.FRIDAY,
    'sat': Weekday.SATURDAY, 'saturday': Weekday.SATURDAY,
    'sun': Weekday.SUNDAY, 'sunday': Weekday.SUNDAY,
}


class RecurringPattern:
    """周期性模式类"""
    
    def __init__(
        self,
        pattern_type: PatternType,
        interval: int = 1,
        weekdays: Optional[Set[Weekday]] = None,
        days_of_month: Optional[Set[int]] = None,
        months: Optional[Set[int]] = None,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        cron_expression: Optional[str] = None,
        nth_weekday: Optional[Tuple[int, Weekday]] = None,  # 如 "每月第二个周二"
    ):
        self.pattern_type = pattern_type
        self.interval = max(1, interval)
        self.weekdays = weekdays or set()
        self.days_of_month = days_of_month or set()
        self.months = months or set()
        self.hour = hour
        self.minute = minute
        self.second = second
        self.start_date = start_date
        self.end_date = end_date
        self.cron_expression = cron_expression
        self.nth_weekday = nth_weekday  # (n, weekday) 如 (2, Weekday.TUESDAY) 表示第二个周二
    
    def __repr__(self) -> str:
        return f"RecurringPattern(type={self.pattern_type.value}, interval={self.interval})"
    
    def matches(self, dt: datetime) -> bool:
        """检查给定时间是否匹配此模式"""
        # 检查日期范围
        if self.start_date and dt.date() < self.start_date:
            return False
        if self.end_date and dt.date() > self.end_date:
            return False
        
        # 检查时间
        if dt.hour != self.hour or dt.minute != self.minute or dt.second != self.second:
            return False
        
        # 根据模式类型检查
        if self.pattern_type == PatternType.DAILY:
            return True
        
        elif self.pattern_type == PatternType.WEEKLY:
            if not self.weekdays:
                return True
            return Weekday(dt.weekday()) in self.weekdays
        
        elif self.pattern_type == PatternType.MONTHLY:
            if self.days_of_month:
                return dt.day in self.days_of_month
            return True
        
        elif self.pattern_type == PatternType.YEARLY:
            if self.months:
                return dt.month in self.months
            return True
        
        return False


def parse_natural_language(pattern: str) -> RecurringPattern:
    """
    解析自然语言周期模式
    
    支持的格式:
    - "每天", "每日", "daily"
    - "每周一", "每周一三五", "weekly on monday"
    - "每月1号", "每月15号", "monthly on 15"
    - "每月第一个周一", "每月最后一个周五"
    - "每3天", "每2周", "every 3 days"
    - "工作日", "周末"
    - 时间: "每天上午9点", "每周一下午3点30分"
    
    Args:
        pattern: 自然语言模式字符串
        
    Returns:
        RecurringPattern 对象
        
    Raises:
        ValueError: 无法解析的模式
    """
    pattern = pattern.strip().lower()
    original = pattern
    
    # 默认时间
    hour, minute, second = 0, 0, 0
    
    # 提取时间
    time_patterns = [
        (r'上午(\d{1,2})[点时](\d{1,2})?[分]?', lambda m: (int(m.group(1)), int(m.group(2)) if m.group(2) else 0, 0)),
        (r'下午(\d{1,2})[点时](\d{1,2})?[分]?', lambda m: (int(m.group(1)) + 12, int(m.group(2)) if m.group(2) else 0, 0)),
        (r'(\d{1,2})[点时](\d{1,2})?[分]?', lambda m: (int(m.group(1)), int(m.group(2)) if m.group(2) else 0, 0)),
        (r'(\d{1,2}):(\d{2})(?::(\d{2}))?', lambda m: (int(m.group(1)), int(m.group(2)), int(m.group(3)) if m.group(3) else 0)),
        (r'at (\d{1,2}):(\d{2})', lambda m: (int(m.group(1)), int(m.group(2)), 0)),
    ]
    
    for time_regex, extractor in time_patterns:
        match = re.search(time_regex, pattern)
        if match:
            hour, minute, second = extractor(match)
            if hour >= 24:
                hour = hour % 24
            pattern = re.sub(time_regex, '', pattern).strip()
            # 清除剩余的时间相关词汇
            pattern = re.sub(r'[上午下午]', '', pattern).strip()
            break
    
    # 解析间隔
    interval = 1
    interval_match = re.search(r'每(\d+)', pattern)
    if interval_match:
        interval = int(interval_match.group(1))
        pattern = re.sub(r'每\d+', '每', pattern)
    
    # 每天模式
    if re.match(r'^每?天?$', pattern) or re.match(r'^每?日?$', pattern) or '天' in pattern or pattern == 'daily':
        return RecurringPattern(
            pattern_type=PatternType.DAILY,
            interval=interval,
            hour=hour, minute=minute, second=second
        )
    
    # 工作日模式 (周一到周五)
    if '工作日' in pattern or 'weekday' in pattern:
        return RecurringPattern(
            pattern_type=PatternType.WEEKLY,
            weekdays={Weekday.MONDAY, Weekday.TUESDAY, Weekday.WEDNESDAY, 
                     Weekday.THURSDAY, Weekday.FRIDAY},
            hour=hour, minute=minute, second=second
        )
    
    # 周末模式
    if '周末' in pattern or 'weekend' in pattern:
        return RecurringPattern(
            pattern_type=PatternType.WEEKLY,
            weekdays={Weekday.SATURDAY, Weekday.SUNDAY},
            hour=hour, minute=minute, second=second
        )
    
    # 解析每月第 n 个周几 (如 "每月第二个周二") - 需要在普通星期解析之前
    # 首先尝试 "最后一个" 格式
    last_match = re.search(r'每月最后.*周([一二三四五六日天])', original)
    if last_match:
        weekday_text = last_match.group(1)
        weekday = WEEKDAY_CN_MAP.get(weekday_text)
        
        if weekday:
            return RecurringPattern(
                pattern_type=PatternType.MONTHLY,
                nth_weekday=(-1, weekday),
                hour=hour, minute=minute, second=second
            )
    
    # 然后尝试 "第n个" 格式
    nth_match = re.search(r'每月第?(一|二|三|四).*周([一二三四五六日天])', original)
    if nth_match:
        nth_text = nth_match.group(1)
        weekday_text = nth_match.group(2)
        
        nth_map = {'一': 1, '二': 2, '三': 3, '四': 4}
        nth = nth_map.get(nth_text, 1)
        
        weekday = WEEKDAY_CN_MAP.get(weekday_text)
        
        if weekday:
            return RecurringPattern(
                pattern_type=PatternType.MONTHLY,
                nth_weekday=(nth, weekday),
                hour=hour, minute=minute, second=second
            )
    
    # 解析每月几号
    day_match = re.search(r'每月第?(\d{1,2})[号日]', original)
    if day_match:
        day = int(day_match.group(1))
        if 1 <= day <= 31:
            return RecurringPattern(
                pattern_type=PatternType.MONTHLY,
                days_of_month={day},
                hour=hour, minute=minute, second=second
            )
    
    # 解析星期
    weekdays = set()
    
    # 中文星期
    for cn, wd in WEEKDAY_CN_MAP.items():
        if cn in pattern:
            weekdays.add(wd)
    
    # 英文星期
    for en, wd in WEEKDAY_EN_MAP.items():
        if en in pattern:
            weekdays.add(wd)
    
    # 每周模式
    if weekdays and ('周' in pattern or '星期' in pattern or 'week' in pattern or 'every' in pattern):
        return RecurringPattern(
            pattern_type=PatternType.WEEKLY,
            weekdays=weekdays,
            interval=interval,
            hour=hour, minute=minute, second=second
        )
    
    # 英文格式: "monthly on 15"
    monthly_match = re.search(r'monthly on (\d{1,2})', pattern)
    if monthly_match:
        day = int(monthly_match.group(1))
        return RecurringPattern(
            pattern_type=PatternType.MONTHLY,
            days_of_month={day},
            hour=hour, minute=minute, second=second
        )
    
    # 解析每隔几天/几周
    every_match = re.search(r'every (\d+) (day|week|month|year)s?', pattern)
    if every_match:
        interval = int(every_match.group(1))
        unit = every_match.group(2)
        
        type_map = {
            'day': PatternType.DAILY,
            'week': PatternType.WEEKLY,
            'month': PatternType.MONTHLY,
            'year': PatternType.YEARLY,
        }
        
        return RecurringPattern(
            pattern_type=type_map[unit],
            interval=interval,
            hour=hour, minute=minute, second=second
        )
    
    # 每月模式
    if '每月' in pattern or 'monthly' in pattern:
        return RecurringPattern(
            pattern_type=PatternType.MONTHLY,
            interval=interval,
            hour=hour, minute=minute, second=second
        )
    
    # 每年模式
    if '每年' in pattern or 'yearly' in pattern or 'annually' in pattern:
        return RecurringPattern(
            pattern_type=PatternType.YEARLY,
            interval=interval,
            hour=hour, minute=minute, second=second
        )
    
    # 每周模式 (无具体星期)
    if '每周' in pattern or 'weekly' in pattern:
        return RecurringPattern(
            pattern_type=PatternType.WEEKLY,
            interval=interval,
            hour=hour, minute=minute, second=second
        )
    
    raise ValueError(f"无法解析的模式: {original}")


def parse_cron(expression: str) -> RecurringPattern:
    """
    解析 cron 风格的表达式
    
    格式: 分 时 日 月 周
    支持的字段:
    - * : 任意值
    - 数字 : 具体值
    - 数字-数字 : 范围
    - 数字,数字 : 列表
    - */数字 : 步进
    
    示例:
    - "0 9 * * *" : 每天 9:00
    - "30 14 * * 1-5" : 周一到周五 14:30
    - "0 0 1 * *" : 每月 1 号 00:00
    - "0 12 * * 1,3,5" : 每周一三五 12:00
    
    Args:
        expression: cron 表达式
        
    Returns:
        RecurringPattern 对象
        
    Raises:
        ValueError: 无效的 cron 表达式
    """
    parts = expression.strip().split()
    if len(parts) != 5:
        raise ValueError(f"cron 表达式必须有 5 个字段: {expression}")
    
    minute_str, hour_str, day_str, month_str, weekday_str = parts
    
    def parse_field(field: str, min_val: int, max_val: int) -> Set[int]:
        """解析单个字段"""
        result = set()
        
        if field == '*':
            return set(range(min_val, max_val + 1))
        
        # 处理多个值
        for part in field.split(','):
            # 步进
            if '/' in part:
                base, step = part.split('/')
                step = int(step)
                if base == '*':
                    result.update(range(min_val, max_val + 1, step))
                else:
                    start = int(base)
                    result.update(range(start, max_val + 1, step))
            # 范围
            elif '-' in part:
                start, end = part.split('-')
                result.update(range(int(start), int(end) + 1))
            # 单个值
            else:
                result.add(int(part))
        
        # 验证范围
        for v in result:
            if v < min_val or v > max_val:
                raise ValueError(f"值 {v} 超出范围 [{min_val}, {max_val}]")
        
        return result
    
    minutes = parse_field(minute_str, 0, 59)
    hours = parse_field(hour_str, 0, 23)
    days = parse_field(day_str, 1, 31)
    months = parse_field(month_str, 1, 12)
    
    # cron 的周几: 0-6, 0=周日, 但我们用 Python 的 0-6, 0=周一
    # 需要转换
    cron_weekdays = parse_field(weekday_str, 0, 6)
    weekdays = set()
    for wd in cron_weekdays:
        if wd == 0:  # cron 中 0 是周日
            weekdays.add(Weekday.SUNDAY)
        else:
            weekdays.add(Weekday(wd - 1))  # 1-5 变成 0-4
    
    # 确定模式类型
    if len(weekdays) < 7 and weekday_str != '*':
        pattern_type = PatternType.WEEKLY
    elif day_str != '*':
        pattern_type = PatternType.MONTHLY
    elif month_str != '*':
        pattern_type = PatternType.YEARLY
    else:
        pattern_type = PatternType.DAILY
    
    # 对于 cron，我们只取第一个时间
    hour = min(hours) if hours else 0
    minute = min(minutes) if minutes else 0
    
    return RecurringPattern(
        pattern_type=pattern_type,
        weekdays=weekdays,
        days_of_month=days,
        months=months,
        hour=hour,
        minute=minute,
        cron_expression=expression
    )


def get_next_occurrence(
    pattern: RecurringPattern,
    from_time: datetime,
    max_iterations: int = 10000
) -> Optional[datetime]:
    """
    获取下一个触发时间
    
    Args:
        pattern: 周期模式
        from_time: 起始时间
        max_iterations: 最大迭代次数
        
    Returns:
        下一个触发时间，如果超过限制则返回 None
    """
    # 首先检查今天是否还有未来的触发时间
    today_target = from_time.replace(hour=pattern.hour, minute=pattern.minute, second=0, microsecond=0)
    
    if today_target > from_time and pattern.matches(today_target):
        # 检查结束日期
        if pattern.end_date and today_target.date() > pattern.end_date:
            pass  # 继续往下找
        else:
            return today_target
    
    # 如果今天没有，开始逐日查找
    current = from_time.replace(hour=pattern.hour, minute=pattern.minute, second=0, microsecond=0)
    
    for _ in range(max_iterations):
        # 向前推进一天
        current += timedelta(days=1)
        
        # 检查是否匹配
        if pattern.matches(current) and current > from_time:
            # 检查结束日期
            if pattern.end_date and current.date() > pattern.end_date:
                return None
            return current
    
    return None


def get_previous_occurrence(
    pattern: RecurringPattern,
    from_time: datetime,
    max_iterations: int = 10000
) -> Optional[datetime]:
    """
    获取上一个触发时间
    
    Args:
        pattern: 周期模式
        from_time: 起始时间
        max_iterations: 最大迭代次数
        
    Returns:
        上一个触发时间，如果超过限制则返回 None
    """
    # 首先检查当天是否有一个已过的触发时间
    today_target = from_time.replace(hour=pattern.hour, minute=pattern.minute, second=0, microsecond=0)
    
    if today_target < from_time and pattern.matches(today_target):
        # 检查开始日期
        if pattern.start_date and today_target.date() < pattern.start_date:
            pass  # 继续往前找
        else:
            return today_target
    
    # 如果当天没有，往前找
    current = from_time.replace(second=0, microsecond=0)
    
    for _ in range(max_iterations):
        # 向后推进
        if pattern.pattern_type == PatternType.DAILY:
            current -= timedelta(days=pattern.interval)
        elif pattern.pattern_type == PatternType.WEEKLY:
            current -= timedelta(days=1)
        elif pattern.pattern_type == PatternType.MONTHLY:
            # 简单处理：回到上个月
            if current.month == 1:
                current = current.replace(year=current.year - 1, month=12)
            else:
                current = current.replace(month=current.month - 1)
        elif pattern.pattern_type == PatternType.YEARLY:
            current = current.replace(year=current.year - 1)
        else:
            current -= timedelta(days=1)
        
        current = current.replace(hour=pattern.hour, minute=pattern.minute)
        
        # 检查时间
        if pattern.matches(current) and current < from_time:
            # 检查开始日期
            if pattern.start_date and current.date() < pattern.start_date:
                return None
            return current
    
    return None


def get_occurrences_in_range(
    pattern: RecurringPattern,
    start: datetime,
    end: datetime
) -> List[datetime]:
    """
    获取时间范围内的所有触发时间
    
    Args:
        pattern: 周期模式
        start: 开始时间
        end: 结束时间
        
    Returns:
        触发时间列表
    """
    occurrences = []
    current = start
    
    while current < end:
        next_occ = get_next_occurrence(pattern, current)
        if next_occ is None or next_occ > end:
            break
        occurrences.append(next_occ)
        current = next_occ + timedelta(minutes=1)
    
    return occurrences


def validate_pattern(pattern_str: str) -> Tuple[bool, Optional[str]]:
    """
    验证模式字符串是否有效
    
    Args:
        pattern_str: 模式字符串
        
    Returns:
        (是否有效, 错误信息)
    """
    # 尝试作为自然语言解析
    try:
        parse_natural_language(pattern_str)
        return True, None
    except ValueError:
        pass
    
    # 尝试作为 cron 解析
    try:
        parse_cron(pattern_str)
        return True, None
    except ValueError as e:
        return False, str(e)


def pattern_to_description(pattern: RecurringPattern) -> str:
    """
    将模式转换为人类可读的描述
    
    Args:
        pattern: 周期模式
        
    Returns:
        描述字符串
    """
    time_str = f"{pattern.hour:02d}:{pattern.minute:02d}"
    
    if pattern.pattern_type == PatternType.DAILY:
        if pattern.interval == 1:
            return f"每天 {time_str}"
        return f"每隔 {pattern.interval} 天 {time_str}"
    
    elif pattern.pattern_type == PatternType.WEEKLY:
        if pattern.weekdays:
            wd_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
            days = ', '.join(wd_names[wd.value] for wd in sorted(pattern.weekdays, key=lambda x: x.value))
            return f"每周 {days} {time_str}"
        return f"每周 {time_str}"
    
    elif pattern.pattern_type == PatternType.MONTHLY:
        if pattern.nth_weekday:
            nth, weekday = pattern.nth_weekday
            nth_names = {1: '第一个', 2: '第二个', 3: '第三个', 4: '第四个', -1: '最后一个'}
            wd_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
            nth_text = nth_names.get(nth, f'第{nth}个')
            return f"每月{nth_text}{wd_names[weekday.value]} {time_str}"
        if pattern.days_of_month:
            days = ', '.join(str(d) for d in sorted(pattern.days_of_month))
            return f"每月 {days} 号 {time_str}"
        return f"每月 {time_str}"
    
    elif pattern.pattern_type == PatternType.YEARLY:
        if pattern.months:
            month_names = ['一月', '二月', '三月', '四月', '五月', '六月',
                          '七月', '八月', '九月', '十月', '十一月', '十二月']
            months = ', '.join(month_names[m-1] for m in sorted(pattern.months))
            return f"每年 {months} {time_str}"
        return f"每年 {time_str}"
    
    elif pattern.pattern_type == PatternType.CRON:
        return f"Cron: {pattern.cron_expression} ({time_str})"
    
    return f"自定义模式 ({time_str})"


def get_nth_weekday_of_month(year: int, month: int, n: int, weekday: Weekday) -> Optional[date]:
    """
    获取某月第 n 个指定星期几的日期
    
    Args:
        year: 年份
        month: 月份
        n: 第几个 (1-5, -1 表示最后一个)
        weekday: 星期几
        
    Returns:
        日期对象，如果不存在则返回 None
    """
    if n == -1:
        # 找最后一个
        # 从月末往前找
        if month == 12:
            next_month = date(year + 1, 1, 1)
        else:
            next_month = date(year, month + 1, 1)
        last_day = next_month - timedelta(days=1)
        
        current = last_day
        while current.weekday() != weekday.value:
            current -= timedelta(days=1)
        return current
    else:
        # 找第 n 个
        first_day = date(year, month, 1)
        
        # 找到第一个匹配的星期几
        days_until = (weekday.value - first_day.weekday()) % 7
        first_occurrence = first_day + timedelta(days=days_until)
        
        # 第 n 个 = 第一个 + (n-1) 周
        result = first_occurrence + timedelta(weeks=n - 1)
        
        # 验证仍在该月
        if result.month != month:
            return None
        
        return result


def calculate_next_n_occurrences(
    pattern: RecurringPattern,
    from_time: datetime,
    n: int
) -> List[datetime]:
    """
    计算接下来的 n 个触发时间
    
    Args:
        pattern: 周期模式
        from_time: 起始时间
        n: 数量
        
    Returns:
        触发时间列表
    """
    results = []
    current = from_time
    
    for _ in range(n):
        next_occ = get_next_occurrence(pattern, current)
        if next_occ is None:
            break
        results.append(next_occ)
        current = next_occ
    
    return results


def humanize_timedelta(dt: datetime, from_time: Optional[datetime] = None) -> str:
    """
    将时间差转换为人类可读的字符串
    
    Args:
        dt: 目标时间
        from_time: 参考时间 (默认为当前时间)
        
    Returns:
        人类可读的描述
    """
    if from_time is None:
        from_time = datetime.now()
    
    diff = dt - from_time
    total_seconds = int(diff.total_seconds())
    
    if total_seconds < 0:
        return "已经过去"
    
    if total_seconds < 60:
        return f"{total_seconds} 秒后"
    
    minutes = total_seconds // 60
    if minutes < 60:
        return f"{minutes} 分钟后"
    
    hours = minutes // 60
    remaining_minutes = minutes % 60
    if hours < 24:
        if remaining_minutes > 0:
            return f"{hours} 小时 {remaining_minutes} 分钟后"
        return f"{hours} 小时后"
    
    days = hours // 24
    remaining_hours = hours % 24
    if remaining_hours > 0:
        return f"{days} 天 {remaining_hours} 小时后"
    return f"{days} 天后"


# 便捷函数
def parse(pattern: str) -> RecurringPattern:
    """解析模式 (自动检测自然语言或 cron)"""
    # 尝试自然语言
    try:
        return parse_natural_language(pattern)
    except ValueError:
        pass
    
    # 尝试 cron
    try:
        return parse_cron(pattern)
    except ValueError:
        pass
    
    raise ValueError(f"无法解析的模式: {pattern}")


def next_occurrence(pattern_str: str, from_time: Optional[datetime] = None) -> Optional[datetime]:
    """获取下一个触发时间 (便捷函数)"""
    pattern = parse(pattern_str)
    if from_time is None:
        from_time = datetime.now()
    return get_next_occurrence(pattern, from_time)


def is_match(pattern_str: str, dt: datetime) -> bool:
    """检查时间是否匹配模式 (便捷函数)"""
    try:
        pattern = parse(pattern_str)
        # 对于匹配检查，只检查时间部分
        if dt.hour != pattern.hour or dt.minute != pattern.minute:
            return False
        return pattern.matches(dt)
    except ValueError:
        return False