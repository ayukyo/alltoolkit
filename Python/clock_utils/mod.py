"""
时钟工具集 (Clock Utils)
提供世界时钟、计时器、倒计时、秒表、时区转换等功能
零外部依赖，纯 Python 标准库实现

功能列表:
1. WorldClock - 世界时钟，支持多时区显示
2. Stopwatch - 秒表，支持计次
3. Timer - 倒计时器
4. TimeFormatter - 时间格式化
5. TimeDifference - 时区差异计算
6. Countdown - 倒计时（天/时/分/秒）
7. AlarmClock - 闹钟（模拟）
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
import time
import math


class ClockFormat(Enum):
    """时钟格式枚举"""
    FORMAT_12H = "12h"  # 12小时制 (AM/PM)
    FORMAT_24H = "24h"  # 24小时制


@dataclass
class LapRecord:
    """秒表计次记录"""
    lap_number: int
    lap_time: float  # 秒
    total_time: float  # 累计时间（秒）
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class TimerEvent:
    """计时器事件"""
    name: str
    target_time: datetime
    callback: Optional[Callable] = None
    message: str = ""
    triggered: bool = False


class WorldClock:
    """
    世界时钟类
    支持多时区时间显示和转换
    使用 UTC 偏移量实现，零外部依赖，兼容所有 Python 版本
    """
    
    # 常用时区 UTC 偏移量（小时）
    TIMEZONE_OFFSETS: Dict[str, float] = {
        "Beijing": 8.0,      # UTC+8
        "Tokyo": 9.0,        # UTC+9
        "NewYork": -5.0,     # UTC-5 (EST)
        "London": 0.0,       # UTC+0 (GMT)
        "Paris": 1.0,        # UTC+1 (CET)
        "Sydney": 11.0,      # UTC+11
        "Dubai": 4.0,        # UTC+4
        "Moscow": 3.0,       # UTC+3
        "LosAngeles": -8.0,  # UTC-8 (PST)
        "Singapore": 8.0,    # UTC+8
        "Mumbai": 5.5,       # UTC+5:30
        "Berlin": 1.0,       # UTC+1 (CET)
        "UTC": 0.0,          # UTC
        "HongKong": 8.0,     # UTC+8
        "Seoul": 9.0,        # UTC+9
        "Melbourne": 11.0,   # UTC+11
        "Chicago": -6.0,     # UTC-6 (CST)
        "Denver": -7.0,      # UTC-7 (MST)
        "Phoenix": -7.0,     # UTC-7 (MST)
        "Honolulu": -10.0,   # UTC-10 (HST)
        "Toronto": -5.0,     # UTC-5 (EST)
        "Vancouver": -8.0,   # UTC-8 (PST)
        "Cairo": 2.0,        # UTC+2
        "Jakarta": 7.0,      # UTC+7
        "Bangkok": 7.0,      # UTC+7
        "Kolkata": 5.5,      # UTC+5:30
        "Lagos": 1.0,        # UTC+1
        "SaoPaulo": -3.0,    # UTC-3
        "BuenosAires": -3.0, # UTC-3
        "Lima": -5.0,        # UTC-5
        "MexicoCity": -6.0,  # UTC-6
        "Madrid": 1.0,       # UTC+1 (CET)
        "Rome": 1.0,         # UTC+1 (CET)
        "Amsterdam": 1.0,    # UTC+1 (CET)
        "Stockholm": 1.0,    # UTC+1 (CET)
        "Helsinki": 2.0,     # UTC+2
        "Warsaw": 1.0,       # UTC+1 (CET)
        "Vienna": 1.0,       # UTC+1 (CET)
        "Zurich": 1.0,       # UTC+1 (CET)
        "Athens": 2.0,       # UTC+2
        "Jerusalem": 3.0,    # UTC+3 (IST)
        "Nairobi": 3.0,      # UTC+3
        "CapeTown": 2.0,     # UTC+2
        "Johannesburg": 2.0, # UTC+2
        "Istanbul": 3.0,     # UTC+3
        "Karachi": 5.0,      # UTC+5
        "Dhaka": 6.0,        # UTC+6
        "Manila": 8.0,       # UTC+8
        "Osaka": 9.0,        # UTC+9
        "Auckland": 13.0,    # UTC+13
    }
    
    def __init__(self, city: str = "Beijing"):
        """
        初始化世界时钟
        
        Args:
            city: 城市名称，用于获取时区
        """
        self.city = city
        self._utc_offset = self._get_utc_offset(city)
    
    def _get_utc_offset(self, city: str) -> float:
        """获取城市的 UTC 偏移量"""
        return self.TIMEZONE_OFFSETS.get(city, 0.0)
    
    def get_current_time(self) -> datetime:
        """获取当前时间（基于 UTC 偏移）"""
        utc_now = datetime.utcnow()
        offset_hours = int(self._utc_offset)
        offset_minutes = int((abs(self._utc_offset) - abs(offset_hours)) * 60)
        if self._utc_offset < 0:
            offset_minutes = -offset_minutes
        return utc_now + timedelta(hours=offset_hours, minutes=offset_minutes)
    
    def get_time_str(self, fmt: ClockFormat = ClockFormat.FORMAT_24H) -> str:
        """
        获取格式化的时间字符串
        
        Args:
            fmt: 时间格式
        
        Returns:
            格式化的时间字符串
        """
        now = self.get_current_time()
        if fmt == ClockFormat.FORMAT_12H:
            return now.strftime("%I:%M:%S %p")
        else:
            return now.strftime("%H:%M:%S")
    
    def get_full_time_str(self, fmt: ClockFormat = ClockFormat.FORMAT_24H) -> str:
        """获取完整的日期时间字符串"""
        now = self.get_current_time()
        if fmt == ClockFormat.FORMAT_12H:
            return now.strftime("%Y-%m-%d %I:%M:%S %p")
        else:
            return now.strftime("%Y-%m-%d %H:%M:%S")
    
    def get_multiple_times(self, cities: List[str], 
                          fmt: ClockFormat = ClockFormat.FORMAT_24H) -> Dict[str, str]:
        """
        获取多个城市的当前时间
        
        Args:
            cities: 城市名称列表
            fmt: 时间格式
        
        Returns:
            城市 -> 时间字符串的映射
        """
        result = {}
        for city in cities:
            clock = WorldClock(city)
            result[city] = clock.get_time_str(fmt)
        return result
    
    @staticmethod
    def list_cities() -> List[str]:
        """列出所有支持的城市"""
        return list(WorldClock.TIMEZONE_OFFSETS.keys())
    
    def __str__(self) -> str:
        return f"{self.city}: {self.get_full_time_str()}"


class Stopwatch:
    """
    秒表类
    支持开始、暂停、重置、计次等功能
    """
    
    def __init__(self):
        """初始化秒表"""
        self._start_time: Optional[float] = None
        self._pause_time: Optional[float] = None
        self._paused_duration: float = 0.0
        self._laps: List[LapRecord] = []
        self._running: bool = False
        self._lap_count: int = 0
    
    def start(self) -> bool:
        """
        开始或继续秒表
        
        Returns:
            是否成功启动
        """
        if self._running:
            return False
        
        if self._start_time is None:
            # 首次启动
            self._start_time = time.time()
        elif self._pause_time is not None:
            # 从暂停中恢复
            self._paused_duration += time.time() - self._pause_time
            self._pause_time = None
        
        self._running = True
        return True
    
    def pause(self) -> bool:
        """
        暂停秒表
        
        Returns:
            是否成功暂停
        """
        if not self._running:
            return False
        
        self._pause_time = time.time()
        self._running = False
        return True
    
    def reset(self) -> None:
        """重置秒表"""
        self._start_time = None
        self._pause_time = None
        self._paused_duration = 0.0
        self._laps = []
        self._running = False
        self._lap_count = 0
    
    def lap(self) -> Optional[LapRecord]:
        """
        记录一个计次
        
        Returns:
            计次记录，如果秒表未运行则返回 None
        """
        if self._start_time is None:
            return None
        
        self._lap_count += 1
        current_time = self.elapsed
        
        # 计算本次计次时间
        if self._laps:
            prev_total = self._laps[-1].total_time
            lap_time = current_time - prev_total
        else:
            lap_time = current_time
        
        record = LapRecord(
            lap_number=self._lap_count,
            lap_time=lap_time,
            total_time=current_time
        )
        self._laps.append(record)
        return record
    
    @property
    def elapsed(self) -> float:
        """
        获取已计时时长（秒）
        
        Returns:
            已计时的秒数
        """
        if self._start_time is None:
            return 0.0
        
        if self._running:
            return time.time() - self._start_time - self._paused_duration
        elif self._pause_time is not None:
            return self._pause_time - self._start_time - self._paused_duration
        else:
            return self._paused_duration
    
    @property
    def elapsed_str(self) -> str:
        """获取格式化的已计时时长"""
        return TimeFormatter.format_duration(self.elapsed)
    
    @property
    def is_running(self) -> bool:
        """秒表是否在运行"""
        return self._running
    
    @property
    def laps(self) -> List[LapRecord]:
        """获取所有计次记录"""
        return self._laps.copy()
    
    def get_best_lap(self) -> Optional[LapRecord]:
        """获取最快计次"""
        if not self._laps:
            return None
        return min(self._laps, key=lambda x: x.lap_time)
    
    def get_worst_lap(self) -> Optional[LapRecord]:
        """获取最慢计次"""
        if not self._laps:
            return None
        return max(self._laps, key=lambda x: x.lap_time)
    
    def get_average_lap(self) -> Optional[float]:
        """获取平均计次时间"""
        if not self._laps:
            return None
        return sum(lap.lap_time for lap in self._laps) / len(self._laps)
    
    def __str__(self) -> str:
        status = "运行中" if self._running else "停止"
        return f"秒表 [{status}] - {self.elapsed_str}"


class Timer:
    """
    计时器类（倒计时）
    支持倒计时、暂停、重置、回调通知
    """
    
    def __init__(self, duration_seconds: float, 
                 name: str = "Timer",
                 callback: Optional[Callable] = None,
                 message: str = ""):
        """
        初始化计时器
        
        Args:
            duration_seconds: 倒计时秒数
            name: 计时器名称
            callback: 计时结束时的回调函数
            message: 计时结束时的消息
        """
        self.duration = duration_seconds
        self.name = name
        self.callback = callback
        self.message = message
        
        self._start_time: Optional[float] = None
        self._pause_time: Optional[float] = None
        self._paused_duration: float = 0.0
        self._running: bool = False
        self._completed: bool = False
    
    @classmethod
    def from_minutes(cls, minutes: float, **kwargs) -> "Timer":
        """从分钟创建计时器"""
        return cls(minutes * 60, **kwargs)
    
    @classmethod
    def from_hours(cls, hours: float, **kwargs) -> "Timer":
        """从小时创建计时器"""
        return cls(hours * 3600, **kwargs)
    
    @classmethod
    def from_time_parts(cls, hours: int = 0, minutes: int = 0, 
                       seconds: int = 0, **kwargs) -> "Timer":
        """从时分秒创建计时器"""
        total = hours * 3600 + minutes * 60 + seconds
        return cls(total, **kwargs)
    
    def start(self) -> bool:
        """开始倒计时"""
        if self._running or self._completed:
            return False
        
        if self._start_time is None:
            self._start_time = time.time()
        elif self._pause_time is not None:
            self._paused_duration += time.time() - self._pause_time
            self._pause_time = None
        
        self._running = True
        return True
    
    def pause(self) -> bool:
        """暂停倒计时"""
        if not self._running:
            return False
        
        self._pause_time = time.time()
        self._running = False
        return True
    
    def reset(self) -> None:
        """重置计时器"""
        self._start_time = None
        self._pause_time = None
        self._paused_duration = 0.0
        self._running = False
        self._completed = False
    
    @property
    def remaining(self) -> float:
        """获取剩余时间（秒）"""
        if self._completed:
            return 0.0
        
        elapsed = self.duration - self.elapsed
        return max(0.0, elapsed)
    
    @property
    def elapsed(self) -> float:
        """获取已过时间（秒）"""
        if self._start_time is None:
            return 0.0
        
        if self._running:
            return time.time() - self._start_time - self._paused_duration
        elif self._pause_time is not None:
            return self._pause_time - self._start_time - self._paused_duration
        else:
            return self._paused_duration
    
    @property
    def remaining_str(self) -> str:
        """获取格式化的剩余时间"""
        return TimeFormatter.format_duration(self.remaining)
    
    @property
    def progress(self) -> float:
        """获取进度百分比 (0.0 - 1.0)"""
        if self.duration == 0:
            return 1.0
        return min(1.0, self.elapsed / self.duration)
    
    @property
    def progress_percent(self) -> float:
        """获取进度百分比 (0 - 100)"""
        return self.progress * 100
    
    @property
    def is_completed(self) -> bool:
        """计时器是否已完成"""
        return self._completed or self.remaining <= 0
    
    @property
    def is_running(self) -> bool:
        """计时器是否在运行"""
        return self._running
    
    def check(self) -> bool:
        """
        检查计时器状态，如果完成则触发回调
        
        Returns:
            计时器是否已完成
        """
        if self._completed:
            return True
        
        if self.remaining <= 0:
            self._completed = True
            self._running = False
            if self.callback:
                try:
                    self.callback(self)
                except Exception:
                    pass
            return True
        
        return False
    
    def wait(self) -> None:
        """阻塞等待计时完成"""
        while not self.is_completed:
            self.check()
            time.sleep(0.01)
    
    def get_progress_bar(self, width: int = 20, 
                        filled: str = "█", 
                        empty: str = "░") -> str:
        """
        获取进度条字符串
        
        Args:
            width: 进度条宽度
            filled: 已完成字符
            empty: 未完成字符
        
        Returns:
            进度条字符串
        """
        filled_count = int(self.progress * width)
        empty_count = width - filled_count
        return filled * filled_count + empty * empty_count
    
    def __str__(self) -> str:
        if self._completed:
            return f"[{self.name}] 已完成!"
        status = "运行中" if self._running else "暂停"
        bar = self.get_progress_bar()
        return f"[{self.name}] {bar} {self.remaining_str} ({status})"


class TimeFormatter:
    """
    时间格式化工具类
    提供各种时间格式化功能
    """
    
    @staticmethod
    def format_duration(seconds: float, 
                       show_ms: bool = False,
                       show_hours: bool = True) -> str:
        """
        格式化时长
        
        Args:
            seconds: 秒数
            show_ms: 是否显示毫秒
            show_hours: 是否显示小时（如果为0）
        
        Returns:
            格式化的时长字符串
        """
        if seconds < 0:
            return "00:00:00" if show_hours else "00:00"
        
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        ms = int((seconds % 1) * 1000)
        
        if show_ms:
            if hours > 0 or show_hours:
                return f"{hours:02d}:{minutes:02d}:{secs:02d}.{ms:03d}"
            return f"{minutes:02d}:{secs:02d}.{ms:03d}"
        else:
            if hours > 0 or show_hours:
                return f"{hours:02d}:{minutes:02d}:{secs:02d}"
            return f"{minutes:02d}:{secs:02d}"
    
    @staticmethod
    def format_relative(delta: timedelta) -> str:
        """
        格式化相对时间（中文）
        
        Args:
            delta: 时间差（正数表示过去，负数表示将来）
        
        Returns:
            相对时间字符串
        """
        total_seconds = abs(delta.total_seconds())
        
        if total_seconds < 60:
            return "刚刚"
        elif total_seconds < 3600:
            minutes = int(total_seconds / 60)
            suffix = "前" if delta.total_seconds() > 0 else "后"
            return f"{minutes}分钟{suffix}"
        elif total_seconds < 86400:
            hours = int(total_seconds / 3600)
            suffix = "前" if delta.total_seconds() > 0 else "后"
            return f"{hours}小时{suffix}"
        elif total_seconds < 2592000:  # 30天
            days = int(total_seconds / 86400)
            suffix = "前" if delta.total_seconds() > 0 else "后"
            return f"{days}天{suffix}"
        elif total_seconds < 31536000:  # 365天
            months = int(total_seconds / 2592000)
            suffix = "前" if delta.total_seconds() > 0 else "后"
            return f"{months}个月{suffix}"
        else:
            years = int(total_seconds / 31536000)
            suffix = "前" if delta.total_seconds() > 0 else "后"
            return f"{years}年{suffix}"
    
    @staticmethod
    def format_countdown(target: datetime, now: Optional[datetime] = None) -> str:
        """
        格式化倒计时
        
        Args:
            target: 目标时间
            now: 当前时间（可选，默认为当前时间）
        
        Returns:
            倒计时字符串
        """
        if now is None:
            now = datetime.now()
        
        delta = target - now
        
        if delta.total_seconds() <= 0:
            return "已过期"
        
        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        parts = []
        if days > 0:
            parts.append(f"{days}天")
        if hours > 0 or days > 0:
            parts.append(f"{hours}时")
        if minutes > 0 or hours > 0 or days > 0:
            parts.append(f"{minutes}分")
        parts.append(f"{seconds}秒")
        
        return "".join(parts)
    
    @staticmethod
    def format_time_ago(dt: datetime, now: Optional[datetime] = None) -> str:
        """
        格式化"多久以前"（中文版）
        
        Args:
            dt: 过去的时间点
            now: 当前时间（可选）
        
        Returns:
            格式化的时间字符串
        """
        if now is None:
            now = datetime.now()
        
        delta = now - dt  # 正数表示过去
        return TimeFormatter.format_relative(delta)
    
    @staticmethod
    def humanize_seconds(seconds: float) -> str:
        """
        人性化秒数显示
        
        Args:
            seconds: 秒数
        
        Returns:
            人性化字符串
        """
        if seconds < 1:
            return f"{int(seconds * 1000)}毫秒"
        
        parts = []
        
        # 天
        days = int(seconds // 86400)
        if days > 0:
            parts.append(f"{days}天")
            seconds %= 86400
        
        # 小时
        hours = int(seconds // 3600)
        if hours > 0:
            parts.append(f"{hours}小时")
            seconds %= 3600
        
        # 分钟
        minutes = int(seconds // 60)
        if minutes > 0:
            parts.append(f"{minutes}分钟")
            seconds %= 60
        
        # 秒
        secs = int(seconds)
        if secs > 0:
            parts.append(f"{secs}秒")
        
        if not parts:
            return "0秒"
        
        return "".join(parts)


class TimeDifference:
    """
    时区差异计算工具
    """
    
    @staticmethod
    def get_timezone_offset(city: str) -> float:
        """
        获取城市相对于UTC的时区偏移（小时）
        
        Args:
            city: 城市名称
        
        Returns:
            UTC偏移小时数
        """
        return WorldClock.TIMEZONE_OFFSETS.get(city, 0.0)
    
    @staticmethod
    def get_time_difference(city1: str, city2: str) -> float:
        """
        获取两个城市的时差（小时）
        
        Args:
            city1: 第一个城市
            city2: 第二个城市
        
        Returns:
            时差小时数
        """
        offset1 = TimeDifference.get_timezone_offset(city1)
        offset2 = TimeDifference.get_timezone_offset(city2)
        return offset2 - offset1
    
    @staticmethod
    def convert_time(source_city: str, target_city: str, 
                    hour: int, minute: int = 0) -> Tuple[int, int]:
        """
        时间转换：将源城市的时间转换为目标城市的时间
        
        Args:
            source_city: 源城市
            target_city: 目标城市
            hour: 小时
            minute: 分钟
        
        Returns:
            (目标小时, 目标分钟)
        """
        diff = TimeDifference.get_time_difference(source_city, target_city)
        
        # 计算总分钟
        total_minutes = hour * 60 + minute + int(diff * 60)
        
        # 规范化到0-23小时范围
        total_minutes %= 24 * 60
        if total_minutes < 0:
            total_minutes += 24 * 60
        
        return total_minutes // 60, total_minutes % 60
    
    @staticmethod
    def get_working_hours_overlap(city1: str, city2: str,
                                 work_start: int = 9,
                                 work_end: int = 18) -> Optional[Tuple[int, int]]:
        """
        计算两个城市工作时间的重叠时段
        
        Args:
            city1: 第一个城市
            city2: 第二个城市
            work_start: 工作开始时间（小时）
            work_end: 工作结束时间（小时）
        
        Returns:
            重叠时段 (开始小时, 结束小时) 或 None
        """
        # 获取城市1的工作时间在城市2的对应时间
        start2, _ = TimeDifference.convert_time(city1, city2, work_start)
        end2, _ = TimeDifference.convert_time(city1, city2, work_end)
        
        # 计算重叠
        overlap_start = max(work_start, start2)
        overlap_end = min(work_end, end2)
        
        if overlap_start < overlap_end:
            return (overlap_start, overlap_end)
        return None


class Countdown:
    """
    倒计时工具类
    用于计算到特定日期/时间的倒计时
    """
    
    def __init__(self, target: datetime, name: str = ""):
        """
        初始化倒计时
        
        Args:
            target: 目标时间
            name: 倒计时名称
        """
        self.target = target
        self.name = name
    
    @classmethod
    def to_date(cls, year: int, month: int, day: int, 
               hour: int = 0, minute: int = 0, second: int = 0,
               name: str = "") -> "Countdown":
        """从日期创建倒计时"""
        target = datetime(year, month, day, hour, minute, second)
        return cls(target, name)
    
    @classmethod
    def to_new_year(cls, year: Optional[int] = None) -> "Countdown":
        """创建到新年的倒计时"""
        if year is None:
            now = datetime.now()
            year = now.year + 1
        return cls.to_date(year, 1, 1, 0, 0, 0, f"{year}年新年")
    
    @classmethod
    def to_christmas(cls, year: Optional[int] = None) -> "Countdown":
        """创建到圣诞节的倒计时"""
        if year is None:
            now = datetime.now()
            year = now.year
            if (now.month, now.day) > (12, 25):
                year += 1
        return cls.to_date(year, 12, 25, 0, 0, 0, f"{year}年圣诞节")
    
    @property
    def remaining(self) -> timedelta:
        """获取剩余时间"""
        now = datetime.now()
        delta = self.target - now
        return delta if delta.total_seconds() > 0 else timedelta(0)
    
    @property
    def is_expired(self) -> bool:
        """倒计时是否已过期"""
        return datetime.now() >= self.target
    
    @property
    def total_seconds(self) -> float:
        """总剩余秒数"""
        return self.remaining.total_seconds()
    
    @property
    def days(self) -> int:
        """剩余天数"""
        return self.remaining.days
    
    @property
    def hours(self) -> int:
        """剩余小时"""
        return self.remaining.seconds // 3600
    
    @property
    def minutes(self) -> int:
        """剩余分钟"""
        return (self.remaining.seconds % 3600) // 60
    
    @property
    def seconds(self) -> int:
        """剩余秒数"""
        return self.remaining.seconds % 60
    
    def get_formatted(self) -> str:
        """获取格式化的倒计时字符串"""
        return TimeFormatter.format_countdown(self.target)
    
    def get_detailed(self) -> Dict[str, int]:
        """获取详细的倒计时字典"""
        return {
            "days": self.days,
            "hours": self.hours,
            "minutes": self.minutes,
            "seconds": self.seconds,
            "total_seconds": int(self.total_seconds)
        }
    
    def __str__(self) -> str:
        name = f"[{self.name}] " if self.name else ""
        if self.is_expired:
            return f"{name}已过期"
        return f"{name}{self.get_formatted()}"


class AlarmClock:
    """
    闹钟类（模拟）
    支持设置多个闹钟，检查闹钟状态
    """
    
    def __init__(self):
        """初始化闹钟"""
        self._alarms: Dict[str, datetime] = {}
        self._triggered: set = set()
    
    def add_alarm(self, name: str, target: datetime) -> None:
        """
        添加一个闹钟
        
        Args:
            name: 闹钟名称
            target: 目标时间
        """
        self._alarms[name] = target
        self._triggered.discard(name)
    
    def add_alarm_from_time(self, name: str, hour: int, minute: int = 0, 
                           second: int = 0, today_only: bool = True) -> bool:
        """
        从时间添加闹钟
        
        Args:
            name: 闹钟名称
            hour: 小时
            minute: 分钟
            second: 秒
            today_only: 是否仅今天（如果时间已过则返回False）
        
        Returns:
            是否成功添加
        """
        now = datetime.now()
        target = now.replace(hour=hour, minute=minute, second=second, microsecond=0)
        
        if target <= now:
            if today_only:
                return False
            target += timedelta(days=1)
        
        self.add_alarm(name, target)
        return True
    
    def remove_alarm(self, name: str) -> bool:
        """
        移除闹钟
        
        Args:
            name: 闹钟名称
        
        Returns:
            是否成功移除
        """
        if name in self._alarms:
            del self._alarms[name]
            self._triggered.discard(name)
            return True
        return False
    
    def check(self) -> List[str]:
        """
        检查所有闹钟状态
        
        Returns:
            触发的闹钟名称列表
        """
        now = datetime.now()
        triggered = []
        
        for name, target in self._alarms.items():
            if name not in self._triggered and now >= target:
                self._triggered.add(name)
                triggered.append(name)
        
        return triggered
    
    def is_triggered(self, name: str) -> bool:
        """检查闹钟是否已触发"""
        return name in self._triggered
    
    def get_remaining(self, name: str) -> Optional[timedelta]:
        """获取闹钟剩余时间"""
        if name not in self._alarms:
            return None
        
        remaining = self._alarms[name] - datetime.now()
        return remaining if remaining.total_seconds() > 0 else timedelta(0)
    
    def list_alarms(self) -> Dict[str, datetime]:
        """列出所有闹钟"""
        return self._alarms.copy()
    
    def list_pending(self) -> Dict[str, datetime]:
        """列出未触发的闹钟"""
        return {name: target for name, target in self._alarms.items()
                if name not in self._triggered}
    
    def snooze(self, name: str, minutes: int = 5) -> bool:
        """
        贪睡功能：将闹钟延后指定分钟
        
        Args:
            name: 闹钟名称
            minutes: 延后分钟数
        
        Returns:
            是否成功
        """
        if name not in self._alarms:
            return False
        
        self._alarms[name] = datetime.now() + timedelta(minutes=minutes)
        self._triggered.discard(name)
        return True
    
    def clear_all(self) -> None:
        """清除所有闹钟"""
        self._alarms.clear()
        self._triggered.clear()


class PomodoroTimer:
    """
    番茄钟计时器
    支持工作/休息周期
    """
    
    def __init__(self, work_minutes: int = 25, 
                 short_break_minutes: int = 5,
                 long_break_minutes: int = 15,
                 long_break_after: int = 4):
        """
        初始化番茄钟
        
        Args:
            work_minutes: 工作时长（分钟）
            short_break_minutes: 短休息时长（分钟）
            long_break_minutes: 长休息时长（分钟）
            long_break_after: 长休息前的工作周期数
        """
        self.work_duration = work_minutes * 60
        self.short_break = short_break_minutes * 60
        self.long_break = long_break_minutes * 60
        self.long_break_after = long_break_after
        
        self._timer: Optional[Timer] = None
        self._session_count: int = 0
        self._is_work: bool = True
        self._running: bool = False
    
    @property
    def current_phase(self) -> str:
        """当前阶段"""
        return "工作" if self._is_work else "休息"
    
    @property
    def session_count(self) -> int:
        """已完成的工作周期数"""
        return self._session_count
    
    def start(self) -> Tuple[str, int]:
        """
        开始当前阶段
        
        Returns:
            (阶段名称, 时长秒数)
        """
        if self._running:
            return self.current_phase, 0
        
        if self._is_work:
            duration = self.work_duration
        else:
            # 判断是短休息还是长休息
            if self._session_count > 0 and self._session_count % self.long_break_after == 0:
                duration = self.long_break
            else:
                duration = self.short_break
        
        self._timer = Timer(duration, name=self.current_phase)
        self._timer.start()
        self._running = True
        
        return self.current_phase, duration
    
    def pause(self) -> bool:
        """暂停"""
        if self._timer and self._running:
            self._timer.pause()
            self._running = False
            return True
        return False
    
    def resume(self) -> bool:
        """继续"""
        if self._timer and not self._running:
            self._timer.start()
            self._running = True
            return True
        return False
    
    def check(self) -> Optional[str]:
        """
        检查状态
        
        Returns:
            如果阶段完成，返回阶段名称；否则返回None
        """
        if not self._timer:
            return None
        
        if self._timer.check():
            completed = self.current_phase
            if self._is_work:
                self._session_count += 1
            self._is_work = not self._is_work
            self._running = False
            self._timer = None
            return completed
        return None
    
    @property
    def remaining(self) -> float:
        """剩余时间（秒）"""
        return self._timer.remaining if self._timer else 0
    
    @property
    def remaining_str(self) -> str:
        """剩余时间字符串"""
        return TimeFormatter.format_duration(self.remaining)
    
    def reset(self) -> None:
        """重置番茄钟"""
        if self._timer:
            self._timer.reset()
        self._timer = None
        self._session_count = 0
        self._is_work = True
        self._running = False
    
    def __str__(self) -> str:
        phase = self.current_phase
        remaining = self.remaining_str
        sessions = self._session_count
        status = "运行中" if self._running else "暂停"
        return f"番茄钟 [{status}] 第{sessions}轮 - {phase}: {remaining}"


# 便捷函数
def get_world_time(city: str) -> str:
    """获取指定城市的当前时间"""
    clock = WorldClock(city)
    return clock.get_full_time_str()


def get_multiple_times(cities: List[str]) -> Dict[str, str]:
    """获取多个城市的当前时间"""
    return WorldClock("Beijing").get_multiple_times(cities)


def create_timer(seconds: float, name: str = "") -> Timer:
    """创建一个倒计时器"""
    return Timer(seconds, name)


def create_stopwatch() -> Stopwatch:
    """创建一个秒表"""
    return Stopwatch()


def format_duration(seconds: float) -> str:
    """格式化时长"""
    return TimeFormatter.format_duration(seconds)


def create_countdown(target: datetime, name: str = "") -> Countdown:
    """创建倒计时"""
    return Countdown(target, name)