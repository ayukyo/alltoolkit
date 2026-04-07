"""
DateTime Utilities - 时间日期工具模块

提供全面的时间日期处理功能，包括格式化、解析、计算、时区转换等。
零依赖，仅使用 Python 标准库。

Author: AllToolkit
Version: 1.0.0
"""

import time
import re
from datetime import datetime, timedelta, timezone
from typing import Optional, Union, List, Tuple, Dict, Any
from calendar import monthrange, isleap


class DateTimeUtils:
    """时间日期工具类"""

    # 常用日期时间格式
    FORMAT_ISO8601 = "%Y-%m-%dT%H:%M:%S"
    FORMAT_ISO8601_FULL = "%Y-%m-%dT%H:%M:%S.%fZ"
    FORMAT_DEFAULT = "%Y-%m-%d %H:%M:%S"
    FORMAT_DATE = "%Y-%m-%d"
    FORMAT_TIME = "%H:%M:%S"
    FORMAT_CHINESE = "%Y年%m月%d日 %H时%M分%S秒"
    FORMAT_CHINESE_DATE = "%Y年%m月%d日"
    FORMAT_SLASH = "%Y/%m/%d %H:%M:%S"
    FORMAT_US = "%m/%d/%Y %I:%M:%S %p"
    FORMAT_COMPACT = "%Y%m%d%H%M%S"

    @staticmethod
    def now() -> datetime:
        """获取当前日期时间"""
        return datetime.now()

    @staticmethod
    def now_utc() -> datetime:
        """获取当前 UTC 日期时间"""
        return datetime.now(timezone.utc)

    @staticmethod
    def today() -> datetime:
        """获取今天日期（时间为 00:00:00）"""
        return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    @staticmethod
    def timestamp() -> float:
        """获取当前时间戳（秒级）"""
        return time.time()

    @staticmethod
    def timestamp_ms() -> int:
        """获取当前时间戳（毫秒级）"""
        return int(time.time() * 1000)

    @staticmethod
    def timestamp_to_datetime(timestamp: Union[int, float], unit: str = 's') -> datetime:
        """将时间戳转换为日期时间对象"""
        if unit == 's':
            return datetime.fromtimestamp(timestamp)
        elif unit == 'ms':
            return datetime.fromtimestamp(timestamp / 1000)
        elif unit == 'us':
            return datetime.fromtimestamp(timestamp / 1000000)
        else:
            raise ValueError(f"Invalid unit: {unit}. Use 's', 'ms', or 'us'")

    @staticmethod
    def datetime_to_timestamp(dt: datetime, unit: str = 's') -> Union[int, float]:
        """将日期时间对象转换为时间戳"""
        ts = dt.timestamp()
        if unit == 's':
            return ts
        elif unit == 'ms':
            return int(ts * 1000)
        elif unit == 'us':
            return int(ts * 1000000)
        else:
            raise ValueError(f"Invalid unit: {unit}. Use 's', 'ms', or 'us'")

    @staticmethod
    def format(dt: Optional[datetime] = None, fmt: str = FORMAT_DEFAULT) -> str:
        """格式化日期时间为字符串"""
        if dt is None:
            dt = datetime.now()
        return dt.strftime(fmt)

    @staticmethod
    def parse(date_string: str, fmt: str = FORMAT_DEFAULT) -> datetime:
        """解析日期时间字符串"""
        return datetime.strptime(date_string, fmt)

    # 预编译的 ISO 8601 正则表达式，避免重复编译
    _ISO8601_TZ_PATTERN = re.compile(r'(.+?)([+-]\d{2}:\d{2})$')
    _ISO8601_FORMATS = ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S")
    
    # 预定义的日期时间格式列表
    _PARSE_FORMATS = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y",
        "%m/%d/%Y %H:%M:%S",
        "%m/%d/%Y",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y%m%d%H%M%S",
        "%Y%m%d",
        "%H:%M:%S",
        "%H:%M",
    ]

    @classmethod
    def parse_auto(cls, date_string: str) -> Optional[datetime]:
        """自动解析日期时间字符串（支持多种常见格式）"""
        # 快速路径：尝试预定义格式
        for fmt in cls._PARSE_FORMATS:
            try:
                return datetime.strptime(date_string, fmt)
            except ValueError:
                continue

        # 处理 ISO 8601 带时区格式
        try:
            iso_str = date_string.replace('Z', '+00:00')
            # 检查是否有时区部分
            if '+' in iso_str or '-' in iso_str[10:]:
                match = cls._ISO8601_TZ_PATTERN.match(iso_str)
                if match:
                    dt_part = match.group(1)
                    for fmt in cls._ISO8601_FORMATS:
                        try:
                            return datetime.strptime(dt_part, fmt)
                        except ValueError:
                            continue
            # 无时区的基本 ISO 格式
            return datetime.strptime(iso_str.replace('+00:00', ''), "%Y-%m-%dT%H:%M:%S")
        except (ValueError, AttributeError):
            pass

        return None

    @staticmethod
    def add_days(dt: datetime, days: int) -> datetime:
        """添加/减少天数"""
        return dt + timedelta(days=days)

    @staticmethod
    def add_hours(dt: datetime, hours: int) -> datetime:
        """添加/减少小时"""
        return dt + timedelta(hours=hours)

    @staticmethod
    def add_minutes(dt: datetime, minutes: int) -> datetime:
        """添加/减少分钟"""
        return dt + timedelta(minutes=minutes)

    @staticmethod
    def add_seconds(dt: datetime, seconds: int) -> datetime:
        """添加/减少秒"""
        return dt + timedelta(seconds=seconds)

    @staticmethod
    def add_months(dt: datetime, months: int) -> datetime:
        """添加/减少月份"""
        month = dt.month - 1 + months
        year = dt.year + month // 12
        month = month % 12 + 1
        day = min(dt.day, monthrange(year, month)[1])
        return dt.replace(year=year, month=month, day=day)

    @staticmethod
    def add_years(dt: datetime, years: int) -> datetime:
        """添加/减少年份"""
        try:
            return dt.replace(year=dt.year + years)
        except ValueError:
            return dt.replace(year=dt.year + years, day=dt.day - 1)

    @staticmethod
    def days_between(start: datetime, end: datetime) -> int:
        """计算两个日期之间的天数差"""
        return (end.date() - start.date()).days

    @staticmethod
    def hours_between(start: datetime, end: datetime) -> float:
        """计算两个日期时间之间的小时差"""
        return (end - start).total_seconds() / 3600

    @staticmethod
    def minutes_between(start: datetime, end: datetime) -> float:
        """计算两个日期时间之间的分钟差"""
        return (end - start).total_seconds() / 60

    @staticmethod
    def seconds_between(start: datetime, end: datetime) -> float:
        """计算两个日期时间之间的秒差"""
        return (end - start).total_seconds()

    @staticmethod
    def is_today(dt: datetime) -> bool:
        """判断日期是否为今天"""
        return dt.date() == datetime.now().date()

    @staticmethod
    def is_yesterday(dt: datetime) -> bool:
        """判断日期是否为昨天"""
        return dt.date() == (datetime.now() - timedelta(days=1)).date()

    @staticmethod
    def is_tomorrow(dt: datetime) -> bool:
        """判断日期是否为明天"""
        return dt.date() == (datetime.now() + timedelta(days=1)).date()

    @staticmethod
    def is_this_week(dt: datetime) -> bool:
        """判断日期是否在本周"""
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=7)
        return start_of_week.date() <= dt.date() < end_of_week.date()

    @staticmethod
    def is_this_month(dt: datetime) -> bool:
        """判断日期是否在本月"""
        today = datetime.now()
        return dt.year == today.year and dt.month == today.month

    @staticmethod
    def is_this_year(dt: datetime) -> bool:
        """判断日期是否在今年"""
        return dt.year == datetime.now().year

    @staticmethod
    def is_weekend(dt: datetime) -> bool:
        """判断日期是否为周末"""
        return dt.weekday() >= 5

    @staticmethod
    def is_weekday(dt: datetime) -> bool:
        """判断日期是否为工作日"""
        return dt.weekday() < 5

    @staticmethod
    def is_leap_year(year: int) -> bool:
        """判断是否为闰年"""
        return isleap(year)

    @staticmethod
    def days_in_month(year: int, month: int) -> int:
        """获取某年某月的天数"""
        return monthrange(year, month)[1]

    @staticmethod
    def start_of_day(dt: datetime) -> datetime:
        """获取日期当天的开始时间"""
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)

    @staticmethod
    def end_of_day(dt: datetime) -> datetime:
        """获取日期当天的结束时间"""
        return dt.replace(hour=23, minute=59, second=59, microsecond=999999)

    @staticmethod
    def start_of_week(dt: datetime) -> datetime:
        """获取日期所在周的开始时间（周一）"""
        return (dt - timedelta(days=dt.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)

    @staticmethod
    def end_of_week(dt: datetime) -> datetime:
        """获取日期所在周的结束时间（周日）"""
        return (dt + timedelta(days=6 - dt.weekday())).replace(hour=23, minute=59, second=59, microsecond=999999)

    @staticmethod
    def start_of_month(dt: datetime) -> datetime:
        """获取日期所在月的开始时间"""
        return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    @staticmethod
    def end_of_month(dt: datetime) -> datetime:
        """获取日期所在月的结束时间"""
        last_day = monthrange(dt.year, dt.month)[1]
        return dt.replace(day=last_day, hour=23, minute=59, second=59, microsecond=999999)

    @staticmethod
    def start_of_year(dt: datetime) -> datetime:
        """获取日期所在年的开始时间"""
        return dt.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

    @staticmethod
    def end_of_year(dt: datetime) -> datetime:
        """获取日期所在年的结束时间"""
        return dt.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)

    @staticmethod
    def get_age(birth_date: datetime, today: Optional[datetime] = None) -> int:
        """计算年龄"""
        if today is None:
            today = datetime.now()
        age = today.year - birth_date.year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        return age

    @staticmethod
    def get_weekday_name(dt: datetime, locale: str = 'en') -> str:
        """获取星期几的名称"""
        weekdays_en = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekdays_cn = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
        weekdays_short = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

        if locale == 'cn':
            return weekdays_cn[dt.weekday()]
        elif locale == 'short':
            return weekdays_short[dt.weekday()]
        else:
            return weekdays_en[dt.weekday()]

    @staticmethod
    def get_month_name(month: int, locale: str = 'en') -> str:
        """获取月份名称"""
        months_en = ['January', 'February', 'March', 'April', 'May', 'June',
                     'July', 'August', 'September', 'October', 'November', 'December']
        months_cn = ['一月', '二月', '三月', '四月', '五月', '六月',
                     '七月', '八月', '九月', '十月', '十一月', '十二月']
        months_short = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        if locale == 'cn':
            return months_cn[month - 1]
        elif locale == 'short':
            return months_short[month - 1]
        else:
            return months_en[month - 1]

    # 时间阈值常量（秒）
    _THRESHOLD_MINUTE = 60
    _THRESHOLD_HOUR = 3600
    _THRESHOLD_DAY = 86400
    _THRESHOLD_YESTERDAY = 172800
    _THRESHOLD_WEEK = 604800
    _THRESHOLD_MONTH = 2592000
    _THRESHOLD_YEAR = 31536000

    @classmethod
    def relative_time(cls, dt: datetime, now: Optional[datetime] = None) -> str:
        """获取相对时间描述（如：刚刚、5分钟前、昨天等）"""
        if now is None:
            now = datetime.now()

        seconds = (now - dt).total_seconds()

        if seconds < cls._THRESHOLD_MINUTE:
            return "刚刚"
        elif seconds < cls._THRESHOLD_HOUR:
            return f"{int(seconds // 60)}分钟前"
        elif seconds < cls._THRESHOLD_DAY:
            return f"{int(seconds // 3600)}小时前"
        elif seconds < cls._THRESHOLD_YESTERDAY:
            return "昨天"
        elif seconds < cls._THRESHOLD_WEEK:
            return f"{int(seconds // 86400)}天前"
        elif seconds < cls._THRESHOLD_MONTH:
            return f"{int(seconds // 604800)}周前"
        elif seconds < cls._THRESHOLD_YEAR:
            return f"{int(seconds // 2592000)}个月前"
        else:
            return f"{int(seconds // 31536000)}年前"

    @classmethod
    def format_duration(cls, seconds: Union[int, float], level: str = 'auto') -> str:
        """格式化时长（秒数转换为可读字符串）"""
        if level == 'auto':
            if seconds < cls._THRESHOLD_MINUTE:
                return f"{int(seconds)}秒"
            elif seconds < cls._THRESHOLD_HOUR:
                minutes = int(seconds // 60)
                secs = int(seconds % 60)
                return f"{minutes}分{secs}秒" if secs > 0 else f"{minutes}分钟"
            elif seconds < cls._THRESHOLD_DAY:
                hours = int(seconds // 3600)
                minutes = int((seconds % 3600) // 60)
                return f"{hours}小时{minutes}分" if minutes > 0 else f"{hours}小时"
            else:
                days = int(seconds // 86400)
                hours = int((seconds % 86400) // 3600)
                return f"{days}天{hours}小时" if hours > 0 else f"{days}天"
        elif level == 'second':
            return f"{int(seconds)}秒"
        elif level == 'minute':
            return f"{seconds / 60:.1f}分钟"
        elif level == 'hour':
            return f"{seconds / 3600:.1f}小时"
        elif level == 'day':
            return f"{seconds / 86400:.1f}天"
        else:
            return f"{int(seconds)}秒"

    @staticmethod
    def countdown(target: datetime, now: Optional[datetime] = None) -> Dict[str, int]:
        """计算到目标时间的倒计时"""
        if now is None:
            now = datetime.now()

        diff = target - now
        total_seconds = max(0, diff.total_seconds())

        days = int(total_seconds // 86400)
        hours = int((total_seconds % 86400) // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)

        return {
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds,
            'total_seconds': int(total_seconds)
        }

    @staticmethod
    def generate_date_range(start: datetime, end: datetime, step_days: int = 1) -> List[datetime]:
        """生成日期范围列表"""
        dates = []
        current = start
        while current <= end:
            dates.append(current)
            current += timedelta(days=step_days)
        return dates

    @staticmethod
    def to_iso8601(dt: datetime) -> str:
        """转换为 ISO 8601 格式字符串"""
        return dt.isoformat()

    @classmethod
    def from_iso8601(cls, iso_string: str) -> datetime:
        """从 ISO 8601 格式字符串解析"""
        # 处理带 Z 的 UTC 格式
        iso_str = iso_string.replace('Z', '+00:00')
        # 移除时区信息，解析为本地时间
        if '+' in iso_str or '-' in iso_str[10:]:
            match = cls._ISO8601_TZ_PATTERN.match(iso_str)
            if match:
                dt_part = match.group(1)
                for fmt in cls._ISO8601_FORMATS:
                    try:
                        return datetime.strptime(dt_part, fmt)
                    except ValueError:
                        continue
        # 基本格式
        for fmt in cls._ISO8601_FORMATS:
            try:
                return datetime.strptime(iso_str, fmt)
            except ValueError:
                continue
        raise ValueError(f"Invalid ISO 8601 format: {iso_string}")

    @staticmethod
    def utc_to_local(dt: datetime) -> datetime:
        """将 UTC 时间转换为本地时间"""
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone()

    @staticmethod
    def local_to_utc(dt: datetime) -> datetime:
        """将本地时间转换为 UTC 时间"""
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.now().astimezone().tzinfo)
        return dt.astimezone(timezone.utc)


# 便捷函数（可直接导入使用）
def now() -> datetime:
    """获取当前日期时间"""
    return DateTimeUtils.now()


def format_datetime(dt: Optional[datetime] = None, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """格式化日期时间"""
    return DateTimeUtils.format(dt, fmt)


def parse_datetime(date_string: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """解析日期时间字符串"""
    return DateTimeUtils.parse(date_string, fmt)


def days_between(start: datetime, end: datetime) -> int:
    """计算两个日期之间的天数差"""
    return DateTimeUtils.days_between(start, end)


def is_leap_year(year: int) -> bool:
    """判断是否为闰年"""
    return DateTimeUtils.is_leap_year(year)


def get_age(birth_date: datetime) -> int:
    """计算年龄"""
    return DateTimeUtils.get_age(birth_date)


def relative_time(dt: datetime) -> str:
    """获取相对时间描述"""
    return DateTimeUtils.relative_time(dt)
