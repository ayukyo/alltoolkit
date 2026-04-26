"""
datetime_utils.py - 日期时间工具模块
功能：日期格式化、时区转换、时间计算、日期范围操作
依赖：仅使用 Python 标准库（datetime, zoneinfo, calendar）
作者：AllToolkit 自动生成
日期：2026-04-27
"""

from datetime import datetime, date, timedelta, timezone
from typing import Optional, Union, Tuple, List
import calendar
import re

# Python 3.9+ 使用 zoneinfo
try:
    from zoneinfo import ZoneInfo
    HAS_ZONEINFO = True
except ImportError:
    HAS_ZONEINFO = False


# ============== 常用日期格式 ==============
DATE_FORMATS = {
    'iso': '%Y-%m-%d',
    'iso_datetime': '%Y-%m-%d %H:%M:%S',
    'iso_datetime_t': '%Y-%m-%dT%H:%M:%S',
    'cn_date': '%Y年%m月%d日',
    'cn_datetime': '%Y年%m月%d日 %H时%M分%S秒',
    'us_date': '%m/%d/%Y',
    'us_datetime': '%m/%d/%Y %I:%M:%S %p',
    'eu_date': '%d/%m/%Y',
    'eu_datetime': '%d/%m/%Y %H:%M:%S',
    'compact': '%Y%m%d',
    'compact_datetime': '%Y%m%d%H%M%S',
    'readable': '%B %d, %Y',
    'readable_datetime': '%B %d, %Y at %I:%M %p',
    'log': '%Y-%m-%d %H:%M:%S.%f',
    'filename': '%Y-%m-%d_%H-%M-%S',
}


# ============== 日期格式化与解析 ==============

def format_datetime(
    dt: Union[datetime, date, None] = None,
    fmt: str = 'iso_datetime',
    tz: Optional[str] = None
) -> str:
    """
    格式化日期时间
    
    Args:
        dt: 日期时间对象，默认当前时间
        fmt: 格式名称或格式字符串，见 DATE_FORMATS
        tz: 目标时区名称（如 'Asia/Shanghai', 'UTC'）
    
    Returns:
        格式化后的日期时间字符串
    
    Examples:
        >>> format_datetime()  # 当前时间
        '2026-04-27 04:00:00'
        >>> format_datetime(fmt='cn_date')
        '2026年04月27日'
        >>> format_datetime(fmt='%Y/%m/%d', tz='UTC')
        '2026/04/26'
    """
    if dt is None:
        dt = datetime.now()
    elif isinstance(dt, date) and not isinstance(dt, datetime):
        dt = datetime.combine(dt, datetime.min.time())
    
    # 应用时区转换
    if tz and isinstance(dt, datetime):
        if HAS_ZONEINFO:
            try:
                target_tz = ZoneInfo(tz)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=ZoneInfo('UTC'))
                dt = dt.astimezone(target_tz)
            except Exception:
                pass
    
    # 获取格式
    format_str = DATE_FORMATS.get(fmt, fmt)
    return dt.strftime(format_str)


def parse_datetime(
    date_str: str,
    fmt: Optional[str] = None,
    tz: Optional[str] = None
) -> datetime:
    """
    解析日期时间字符串
    
    Args:
        date_str: 日期时间字符串
        fmt: 格式名称或格式字符串，None 则自动检测
        tz: 时区名称（用于无时区信息的时间）
    
    Returns:
        datetime 对象
    
    Raises:
        ValueError: 无法解析日期字符串
    
    Examples:
        >>> parse_datetime('2026-04-27')
        datetime.datetime(2026, 4, 27, 0, 0)
        >>> parse_datetime('2026年4月27日', fmt='cn_date')
        datetime.datetime(2026, 4, 27, 0, 0)
    """
    date_str = date_str.strip()
    
    # 如果指定了格式
    if fmt:
        format_str = DATE_FORMATS.get(fmt, fmt)
        dt = datetime.strptime(date_str, format_str)
    else:
        # 自动尝试常见格式
        formats_to_try = [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%dT%H:%M:%S%z',
            '%Y-%m-%d',
            '%Y/%m/%d %H:%M:%S',
            '%Y/%m/%d',
            '%Y年%m月%d日 %H时%M分%S秒',
            '%Y年%m月%d日',
            '%d/%m/%Y %H:%M:%S',
            '%d/%m/%Y',
            '%m/%d/%Y %I:%M:%S %p',
            '%m/%d/%Y',
            '%Y%m%d%H%M%S',
            '%Y%m%d',
        ]
        
        for f in formats_to_try:
            try:
                dt = datetime.strptime(date_str, f)
                break
            except ValueError:
                continue
        else:
            raise ValueError(f"无法解析日期字符串: {date_str}")
    
    # 应用时区
    if tz and dt.tzinfo is None and HAS_ZONEINFO:
        try:
            dt = dt.replace(tzinfo=ZoneInfo(tz))
        except Exception:
            pass
    
    return dt


def parse_natural_time(text: str, base: Optional[datetime] = None) -> Optional[datetime]:
    """
    解析自然语言时间表达式
    
    Args:
        text: 自然语言时间描述
        base: 基准时间，默认当前时间
    
    Returns:
        解析后的 datetime，无法解析返回 None
    
    Examples:
        >>> parse_natural_time('明天')
        datetime.datetime(2026, 4, 28, 0, 0)
        >>> parse_natural_time('下周三')
        datetime.datetime(2026, 4, 29, 0, 0)
        >>> parse_natural_time('3天后')
        datetime.datetime(2026, 4, 30, 0, 0)
    """
    if base is None:
        base = datetime.now()
    
    text = text.strip().lower()
    
    # 简单模式匹配
    patterns = {
        # 相对日期
        r'^今天$': lambda: base.replace(hour=0, minute=0, second=0, microsecond=0),
        r'^明天$': lambda: (base + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0),
        r'^后天$': lambda: (base + timedelta(days=2)).replace(hour=0, minute=0, second=0, microsecond=0),
        r'^昨天$': lambda: (base - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0),
        r'^前天$': lambda: (base - timedelta(days=2)).replace(hour=0, minute=0, second=0, microsecond=0),
        
        # 相对时间
        r'^(\d+)秒前$': lambda m: base - timedelta(seconds=int(m.group(1))),
        r'^(\d+)分钟前$': lambda m: base - timedelta(minutes=int(m.group(1))),
        r'^(\d+)小时前$': lambda m: base - timedelta(hours=int(m.group(1))),
        r'^(\d+)天前$': lambda m: base - timedelta(days=int(m.group(1))),
        r'^(\d+)周前$': lambda m: base - timedelta(weeks=int(m.group(1))),
        r'^(\d+)个月后$': lambda m: add_months(base, int(m.group(1))),
        r'^(\d+)年后$': lambda m: base.replace(year=base.year + int(m.group(1))),
        
        r'^(\d+)秒后$': lambda m: base + timedelta(seconds=int(m.group(1))),
        r'^(\d+)分钟后$': lambda m: base + timedelta(minutes=int(m.group(1))),
        r'^(\d+)小时后$': lambda m: base + timedelta(hours=int(m.group(1))),
        r'^(\d+)天后$': lambda m: base + timedelta(days=int(m.group(1))),
        r'^(\d+)周后$': lambda m: base + timedelta(weeks=int(m.group(1))),
        
        # 周几
        r'^下周([一二三四五六日天])$': lambda m: next_weekday(base, parse_weekday_cn(m.group(1))),
        r'^本周([一二三四五六日天])$': lambda m: this_weekday(base, parse_weekday_cn(m.group(1))),
        r'^上周末$': lambda: last_weekday(base, 6),  # 周日
    }
    
    for pattern, calc in patterns.items():
        match = re.match(pattern, text)
        if match:
            try:
                if callable(calc) and not hasattr(calc, '__call__'):
                    return calc
                elif match.groups():
                    return calc(match)
                else:
                    return calc()
            except Exception:
                return None
    
    return None


def parse_weekday_cn(char: str) -> int:
    """解析中文星期几为数字（周一=0, 周日=6）"""
    mapping = {'一': 0, '二': 1, '三': 2, '四': 3, '五': 4, '六': 5, '日': 6, '天': 6}
    return mapping.get(char, 0)


def next_weekday(base: datetime, weekday: int) -> datetime:
    """获取下一个指定周几的日期"""
    days_ahead = weekday - base.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return (base + timedelta(days=days_ahead)).replace(hour=0, minute=0, second=0, microsecond=0)


def this_weekday(base: datetime, weekday: int) -> datetime:
    """获取本周指定周几的日期"""
    days_diff = weekday - base.weekday()
    return (base + timedelta(days=days_diff)).replace(hour=0, minute=0, second=0, microsecond=0)


def last_weekday(base: datetime, weekday: int) -> datetime:
    """获取上一个指定周几的日期"""
    days_behind = base.weekday() - weekday
    if days_behind < 0:
        days_behind += 7
    return (base - timedelta(days=days_behind)).replace(hour=0, minute=0, second=0, microsecond=0)


# ============== 时区转换 ==============

def get_timezone(tz_name: str):
    """
    获取时区对象
    
    Args:
        tz_name: 时区名称（如 'Asia/Shanghai', 'UTC', 'America/New_York'）
    
    Returns:
        时区对象，如果 zoneinfo 不可用返回 None
    
    Examples:
        >>> tz = get_timezone('Asia/Shanghai')
        >>> tz.key
        'Asia/Shanghai'
    """
    if not HAS_ZONEINFO:
        if tz_name.upper() == 'UTC':
            return timezone.utc
        return None
    
    try:
        return ZoneInfo(tz_name)
    except Exception:
        return None


def convert_timezone(
    dt: datetime,
    target_tz: str,
    source_tz: Optional[str] = None
) -> datetime:
    """
    时区转换
    
    Args:
        dt: datetime 对象
        target_tz: 目标时区名称
        source_tz: 源时区名称（如果 dt 无时区信息）
    
    Returns:
        转换后的 datetime
    
    Examples:
        >>> dt = datetime(2026, 4, 27, 12, 0, tzinfo=ZoneInfo('UTC'))
        >>> convert_timezone(dt, 'Asia/Shanghai')
        datetime.datetime(2026, 4, 27, 20, 0, tzinfo=zoneinfo.ZoneInfo(key='Asia/Shanghai'))
    """
    if not HAS_ZONEINFO:
        return dt
    
    # 如果 dt 无时区信息，先添加源时区
    if dt.tzinfo is None:
        if source_tz:
            try:
                dt = dt.replace(tzinfo=ZoneInfo(source_tz))
            except Exception:
                dt = dt.replace(tzinfo=ZoneInfo('UTC'))
        else:
            dt = dt.replace(tzinfo=ZoneInfo('UTC'))
    
    # 转换到目标时区
    try:
        return dt.astimezone(ZoneInfo(target_tz))
    except Exception:
        return dt


def now_in_timezone(tz_name: str) -> datetime:
    """
    获取指定时区的当前时间
    
    Args:
        tz_name: 时区名称
    
    Returns:
        当前时间（带时区信息）
    
    Examples:
        >>> now_in_timezone('Asia/Shanghai')
        datetime.datetime(2026, 4, 27, 4, 0, tzinfo=zoneinfo.ZoneInfo(key='Asia/Shanghai'))
    """
    if HAS_ZONEINFO:
        try:
            return datetime.now(ZoneInfo(tz_name))
        except Exception:
            pass
    return datetime.now(timezone.utc)


# ============== 时间计算 ==============

def add_months(dt: datetime, months: int) -> datetime:
    """
    月份加减
    
    Args:
        dt: 原始日期
        months: 增加的月数（可为负）
    
    Returns:
        计算后的日期
    
    Examples:
        >>> add_months(datetime(2026, 1, 31), 1)
        datetime.datetime(2026, 2, 28, 0, 0)
        >>> add_months(datetime(2026, 3, 15), -2)
        datetime.datetime(2026, 1, 15, 0, 0)
    """
    month = dt.month - 1 + months
    year = dt.year + month // 12
    month = month % 12 + 1
    
    # 处理日期溢出
    day = min(dt.day, calendar.monthrange(year, month)[1])
    
    return dt.replace(year=year, month=month, day=day)


def add_years(dt: datetime, years: int) -> datetime:
    """
    年份加减
    
    Args:
        dt: 原始日期
        years: 增加的年数（可为负）
    
    Returns:
        计算后的日期
    
    Examples:
        >>> add_years(datetime(2024, 2, 29), 1)  # 闰年处理
        datetime.datetime(2025, 2, 28, 0, 0)
    """
    try:
        return dt.replace(year=dt.year + years)
    except ValueError:
        # 2月29日在非闰年变为2月28日
        return dt.replace(year=dt.year + years, day=28)


def date_diff(
    start: Union[datetime, date, str],
    end: Union[datetime, date, str]
) -> dict:
    """
    计算两个日期的差值
    
    Args:
        start: 开始日期
        end: 结束日期
    
    Returns:
        包含各种时间单位差值的字典
    
    Examples:
        >>> date_diff('2026-01-01', '2026-04-27')
        {'days': 116, 'weeks': 16, 'months': 3, 'years': 0, 'total_seconds': 10022400.0}
    """
    if isinstance(start, str):
        start = parse_datetime(start)
    if isinstance(end, str):
        end = parse_datetime(end)
    
    if isinstance(start, date) and not isinstance(start, datetime):
        start = datetime.combine(start, datetime.min.time())
    if isinstance(end, date) and not isinstance(end, datetime):
        end = datetime.combine(end, datetime.min.time())
    
    delta = end - start
    
    # 计算月份差
    months = (end.year - start.year) * 12 + end.month - start.month
    if end.day < start.day:
        months -= 1
    
    return {
        'total_seconds': delta.total_seconds(),
        'days': delta.days,
        'weeks': delta.days // 7,
        'months': months,
        'years': end.year - start.year,
        'hours': delta.total_seconds() / 3600,
        'minutes': delta.total_seconds() / 60,
    }


def age(
    birth_date: Union[datetime, date, str],
    reference: Optional[Union[datetime, date]] = None
) -> dict:
    """
    计算年龄
    
    Args:
        birth_date: 出生日期
        reference: 参考日期，默认当前日期
    
    Returns:
        包含年龄信息的字典
    
    Examples:
        >>> age('1990-05-15')
        {'years': 35, 'months': 11, 'days': 12, 'total_days': 13126, 'next_birthday': '2027-05-15'}
    """
    if isinstance(birth_date, str):
        birth_date = parse_datetime(birth_date)
    
    if isinstance(birth_date, datetime):
        birth_date = birth_date.date()
    
    if reference is None:
        reference = date.today()
    elif isinstance(reference, datetime):
        reference = reference.date()
    elif isinstance(reference, str):
        reference = parse_datetime(reference).date()
    
    # 计算年龄
    years = reference.year - birth_date.year
    months = reference.month - birth_date.month
    days = reference.day - birth_date.day
    
    if days < 0:
        months -= 1
        # 获取上个月的天数
        prev_month = reference.month - 1 if reference.month > 1 else 12
        prev_year = reference.year if reference.month > 1 else reference.year - 1
        days += calendar.monthrange(prev_year, prev_month)[1]
    
    if months < 0:
        years -= 1
        months += 12
    
    # 计算下次生日
    next_birthday = date(reference.year, birth_date.month, birth_date.day)
    if next_birthday <= reference:
        next_birthday = date(reference.year + 1, birth_date.month, birth_date.day)
    
    return {
        'years': years,
        'months': months,
        'days': days,
        'total_days': (reference - birth_date).days,
        'next_birthday': next_birthday.isoformat(),
        'days_to_birthday': (next_birthday - reference).days,
    }


# ============== 工作日计算 ==============

def workdays_between(
    start: Union[datetime, date, str],
    end: Union[datetime, date, str],
    holidays: Optional[List[Union[datetime, date, str]]] = None,
    weekend: Tuple[int, int] = (5, 6)
) -> int:
    """
    计算两个日期之间的工作日数
    
    Args:
        start: 开始日期
        end: 结束日期
        holidays: 节假日列表
        weekend: 周末的星期值，默认(5, 6)即周六周日
    
    Returns:
        工作日数量
    
    Examples:
        >>> workdays_between('2026-04-20', '2026-04-27')
        5
    """
    if isinstance(start, str):
        start = parse_datetime(start).date()
    if isinstance(end, str):
        end = parse_datetime(end).date()
    
    if isinstance(start, datetime):
        start = start.date()
    if isinstance(end, datetime):
        end = end.date()
    
    if start > end:
        start, end = end, start
    
    # 处理节假日
    holiday_set = set()
    if holidays:
        for h in holidays:
            if isinstance(h, str):
                h = parse_datetime(h).date()
            elif isinstance(h, datetime):
                h = h.date()
            holiday_set.add(h)
    
    workdays = 0
    current = start
    while current <= end:
        if current.weekday() not in weekend and current not in holiday_set:
            workdays += 1
        current += timedelta(days=1)
    
    return workdays


def add_workdays(
    start: Union[datetime, date, str],
    days: int,
    holidays: Optional[List[Union[datetime, date, str]]] = None,
    weekend: Tuple[int, int] = (5, 6)
) -> date:
    """
    增加工作日
    
    Args:
        start: 开始日期
        days: 要增加的工作日数（可为负）
        holidays: 节假日列表
        weekend: 周末的星期值
    
    Returns:
        计算后的日期
    
    Examples:
        >>> add_workdays('2026-04-24', 3)  # 周五 + 3 工作日 = 下周三
        datetime.date(2026, 4, 29)
    """
    if isinstance(start, str):
        start = parse_datetime(start).date()
    if isinstance(start, datetime):
        start = start.date()
    
    # 处理节假日
    holiday_set = set()
    if holidays:
        for h in holidays:
            if isinstance(h, str):
                h = parse_datetime(h).date()
            elif isinstance(h, datetime):
                h = h.date()
            holiday_set.add(h)
    
    direction = 1 if days > 0 else -1
    days_remaining = abs(days)
    current = start
    
    while days_remaining > 0:
        current += timedelta(days=direction)
        if current.weekday() not in weekend and current not in holiday_set:
            days_remaining -= 1
    
    return current


def is_workday(
    dt: Union[datetime, date, str],
    holidays: Optional[List[Union[datetime, date, str]]] = None,
    weekend: Tuple[int, int] = (5, 6)
) -> bool:
    """
    判断是否为工作日
    
    Args:
        dt: 日期
        holidays: 节假日列表
        weekend: 周末的星期值
    
    Returns:
        是否为工作日
    
    Examples:
        >>> is_workday('2026-04-25')  # 周六
        False
        >>> is_workday('2026-04-27')  # 周日
        False
        >>> is_workday('2026-04-28')  # 周一
        True
    """
    if isinstance(dt, str):
        dt = parse_datetime(dt).date()
    if isinstance(dt, datetime):
        dt = dt.date()
    
    # 检查是否为周末
    if dt.weekday() in weekend:
        return False
    
    # 检查是否为节假日
    if holidays:
        for h in holidays:
            if isinstance(h, str):
                h = parse_datetime(h).date()
            elif isinstance(h, datetime):
                h = h.date()
            if dt == h:
                return False
    
    return True


# ============== 日期范围 ==============

def date_range(
    start: Union[datetime, date, str],
    end: Union[datetime, date, str],
    step: timedelta = timedelta(days=1)
) -> List[date]:
    """
    生成日期范围
    
    Args:
        start: 开始日期
        end: 结束日期
        step: 步长
    
    Returns:
        日期列表
    
    Examples:
        >>> date_range('2026-04-25', '2026-04-28')
        [date(2026, 4, 25), date(2026, 4, 26), date(2026, 4, 27), date(2026, 4, 28)]
    """
    if isinstance(start, str):
        start = parse_datetime(start).date()
    if isinstance(end, str):
        end = parse_datetime(end).date()
    
    if isinstance(start, datetime):
        start = start.date()
    if isinstance(end, datetime):
        end = end.date()
    
    dates = []
    current = start
    
    if start <= end:
        while current <= end:
            dates.append(current)
            current += step
    else:
        while current >= end:
            dates.append(current)
            current -= step
    
    return dates


def get_month_range(
    year: int,
    month: int
) -> Tuple[date, date]:
    """
    获取月份的日期范围
    
    Args:
        year: 年份
        month: 月份
    
    Returns:
        (月初日期, 月末日期)
    
    Examples:
        >>> get_month_range(2026, 2)
        (date(2026, 2, 1), date(2026, 2, 28))
    """
    first_day = date(year, month, 1)
    last_day = date(year, month, calendar.monthrange(year, month)[1])
    return first_day, last_day


def get_week_range(
    dt: Union[datetime, date, str, None] = None,
    week_start: int = 0  # 0=周一, 6=周日
) -> Tuple[date, date]:
    """
    获取周的日期范围
    
    Args:
        dt: 日期，默认今天
        week_start: 周起始日（0=周一, 6=周日）
    
    Returns:
        (周初日期, 周末日期)
    
    Examples:
        >>> get_week_range('2026-04-27')  # 周日
        (date(2026, 4, 27), date(2026, 5, 3))  # 如果周一开始
    """
    if dt is None:
        dt = date.today()
    elif isinstance(dt, str):
        dt = parse_datetime(dt).date()
    elif isinstance(dt, datetime):
        dt = dt.date()
    
    # 计算周初
    days_since_week_start = (dt.weekday() - week_start) % 7
    week_start_date = dt - timedelta(days=days_since_week_start)
    week_end_date = week_start_date + timedelta(days=6)
    
    return week_start_date, week_end_date


# ============== 时间戳操作 ==============

def timestamp_to_datetime(ts: Union[int, float], ms: bool = False) -> datetime:
    """
    时间戳转 datetime
    
    Args:
        ts: 时间戳
        ms: 是否为毫秒时间戳
    
    Returns:
        datetime 对象
    
    Examples:
        >>> timestamp_to_datetime(1745678400)
        datetime.datetime(2025, 4, 26, 16, 0)
    """
    if ms:
        ts = ts / 1000
    return datetime.fromtimestamp(ts)


def datetime_to_timestamp(dt: Optional[datetime] = None, ms: bool = False) -> Union[int, float]:
    """
    datetime 转时间戳
    
    Args:
        dt: datetime 对象，默认当前时间
        ms: 是否返回毫秒时间戳
    
    Returns:
        时间戳
    
    Examples:
        >>> datetime_to_timestamp()
        1745678400
    """
    if dt is None:
        dt = datetime.now()
    
    ts = dt.timestamp()
    return int(ts * 1000) if ms else int(ts)


# ============== 其他实用功能 ==============

def is_leap_year(year: int) -> bool:
    """
    判断是否为闰年
    
    Examples:
        >>> is_leap_year(2024)
        True
        >>> is_leap_year(2025)
        False
    """
    return calendar.isleap(year)


def days_in_month(year: int, month: int) -> int:
    """
    获取月份的天数
    
    Examples:
        >>> days_in_month(2026, 2)
        28
        >>> days_in_month(2024, 2)
        29
    """
    return calendar.monthrange(year, month)[1]


def quarter(dt: Union[datetime, date, str, None] = None) -> int:
    """
    获取季度（1-4）
    
    Examples:
        >>> quarter('2026-04-27')
        2
    """
    if dt is None:
        dt = date.today()
    elif isinstance(dt, str):
        dt = parse_datetime(dt).date()
    elif isinstance(dt, datetime):
        dt = dt.date()
    
    return (dt.month - 1) // 3 + 1


def week_of_year(dt: Union[datetime, date, str, None] = None) -> Tuple[int, int]:
    """
    获取年份和周数
    
    Args:
        dt: 日期
    
    Returns:
        (年份, 周数)
    
    Examples:
        >>> week_of_year('2026-04-27')
        (2026, 17)
    """
    if dt is None:
        dt = date.today()
    elif isinstance(dt, str):
        dt = parse_datetime(dt).date()
    elif isinstance(dt, datetime):
        dt = dt.date()
    
    return dt.isocalendar()[:2]


def humanize_delta(
    delta: Union[timedelta, int, float],
    precision: int = 2
) -> str:
    """
    人性化时间差描述
    
    Args:
        delta: 时间差（timedelta 或秒数）
        precision: 精度（显示几个单位）
    
    Returns:
        人性化描述
    
    Examples:
        >>> humanize_delta(3661)
        '1小时1分钟'
        >>> humanize_delta(timedelta(days=2, hours=3))
        '2天3小时'
    """
    if isinstance(delta, (int, float)):
        delta = timedelta(seconds=delta)
    
    seconds = int(delta.total_seconds())
    
    if seconds < 0:
        return "刚刚"
    
    units = [
        ('年', 31536000),
        ('天', 86400),
        ('小时', 3600),
        ('分钟', 60),
        ('秒', 1),
    ]
    
    parts = []
    for unit_name, unit_seconds in units:
        if seconds >= unit_seconds:
            count = seconds // unit_seconds
            seconds -= count * unit_seconds
            parts.append(f"{count}{unit_name}")
            if len(parts) >= precision:
                break
    
    return ''.join(parts) if parts else "0秒"


def format_duration(seconds: Union[int, float]) -> str:
    """
    格式化时长
    
    Args:
        seconds: 秒数
    
    Returns:
        格式化的时长字符串
    
    Examples:
        >>> format_duration(3665)
        '1:01:05'
        >>> format_duration(65)
        '1:05'
    """
    seconds = int(seconds)
    
    if seconds < 0:
        seconds = abs(seconds)
        sign = "-"
    else:
        sign = ""
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{sign}{hours}:{minutes:02d}:{secs:02d}"
    else:
        return f"{sign}{minutes}:{secs:02d}"


# ============== 快捷函数 ==============

def now(fmt: str = 'iso_datetime', tz: Optional[str] = None) -> str:
    """获取当前时间的格式化字符串"""
    return format_datetime(datetime.now(), fmt, tz)


def today(fmt: str = 'iso') -> str:
    """获取今天的日期字符串"""
    return date.today().strftime(DATE_FORMATS.get(fmt, fmt))


def yesterday(fmt: str = 'iso') -> str:
    """获取昨天的日期字符串"""
    return (date.today() - timedelta(days=1)).strftime(DATE_FORMATS.get(fmt, fmt))


def tomorrow(fmt: str = 'iso') -> str:
    """获取明天的日期字符串"""
    return (date.today() + timedelta(days=1)).strftime(DATE_FORMATS.get(fmt, fmt))


if __name__ == '__main__':
    # 简单演示
    print("=== datetime_utils 演示 ===")
    print(f"当前时间: {now()}")
    print(f"今天: {today()}")
    print(f"明天: {tomorrow()}")
    print(f"格式化: {format_datetime(fmt='cn_datetime')}")
    print(f"解析: {parse_datetime('2026年4月27日', fmt='cn_date')}")
    print(f"年龄: {age('1990-05-15')}")
    print(f"工作日计算: {workdays_between('2026-04-20', '2026-04-27')} 个工作日")
    print(f"日期差: {date_diff('2026-01-01', '2026-04-27')}")