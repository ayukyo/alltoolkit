"""
倒计时工具模块 - Countdown Utilities

提供精确的倒计时计算功能，支持多种时间单位和格式化输出。
零外部依赖，仅使用 Python 标准库。

功能：
- 计算到目标时间/日期的精确倒计时
- 支持多种时间单位（天、时、分、秒）
- 支持自定义格式化输出
- 支持相对时间倒计时（如"3天后"）
- 支持进度条显示
"""

from datetime import datetime, timedelta
from typing import Optional, Union, Tuple, List
import re


class CountdownError(Exception):
    """倒计时相关错误"""
    pass


class Countdown:
    """
    倒计时类，表示一个倒计时实例
    
    Example:
        >>> cd = Countdown("2026-12-31 23:59:59")
        >>> print(cd.format())
        >>> print(cd.progress_bar())
    """
    
    def __init__(
        self, 
        target: Union[str, datetime],
        start: Optional[Union[str, datetime]] = None,
        name: Optional[str] = None
    ):
        """
        初始化倒计时
        
        Args:
            target: 目标时间（字符串格式或datetime对象）
            start: 开始时间（默认为当前时间）
            name: 倒计时名称
        
        Raises:
            CountdownError: 时间解析失败
        """
        self.target = self._parse_datetime(target)
        self.start = self._parse_datetime(start) if start else datetime.now()
        self.name = name
        
        if self.target <= self.start:
            raise CountdownError("目标时间必须晚于开始时间")
    
    def _parse_datetime(self, dt: Union[str, datetime]) -> datetime:
        """解析日期时间"""
        if isinstance(dt, datetime):
            return dt
        
        # 支持多种日期格式
        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y-%m-%d",
            "%Y/%m/%d %H:%M:%S",
            "%Y/%m/%d %H:%M",
            "%Y/%m/%d",
            "%d-%m-%Y %H:%M:%S",
            "%d-%m-%Y",
            "%m/%d/%Y %H:%M:%S",
            "%m/%d/%Y",
            "%Y年%m月%d日 %H:%M:%S",
            "%Y年%m月%d日 %H:%M",
            "%Y年%m月%d日",
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(dt.strip(), fmt)
            except ValueError:
                continue
        
        raise CountdownError(f"无法解析日期时间: {dt}")
    
    @property
    def remaining(self) -> timedelta:
        """获取剩余时间"""
        now = datetime.now()
        if now >= self.target:
            return timedelta(0)
        return self.target - now
    
    @property
    def total_seconds(self) -> float:
        """总剩余秒数"""
        return self.remaining.total_seconds()
    
    @property
    def is_expired(self) -> bool:
        """是否已过期"""
        return datetime.now() >= self.target
    
    @property
    def progress(self) -> float:
        """
        获取进度（0.0 - 1.0）
        从开始时间到目标时间的进度
        """
        total = (self.target - self.start).total_seconds()
        if total <= 0:
            return 1.0
        elapsed = (datetime.now() - self.start).total_seconds()
        return min(1.0, max(0.0, elapsed / total))
    
    def get_components(self) -> Tuple[int, int, int, int]:
        """
        获取时间组件
        
        Returns:
            (days, hours, minutes, seconds) 元组
        """
        seconds = int(self.total_seconds)
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return days, hours, minutes, secs
    
    def format(
        self, 
        style: str = "default",
        include_seconds: bool = True,
        include_name: bool = False
    ) -> str:
        """
        格式化倒计时输出
        
        Args:
            style: 格式风格
                - default: "XX天 XX小时 XX分钟 XX秒"
                - compact: "XXd XXh XXm XXs"
                - chinese: "XX天XX小时XX分钟XX秒"
                - digital: "DD:HH:MM:SS"
                - words: "X天X小时X分钟X秒"
            include_seconds: 是否包含秒
            include_name: 是否包含名称
        
        Returns:
            格式化后的倒计时字符串
        """
        if self.is_expired:
            result = "已结束"
            if include_name and self.name:
                result = f"{self.name} {result}"
            return result
        
        days, hours, minutes, seconds = self.get_components()
        
        if style == "default":
            parts = []
            if days > 0:
                parts.append(f"{days}天")
            if hours > 0 or days > 0:
                parts.append(f"{hours}小时")
            if minutes > 0 or hours > 0 or days > 0:
                parts.append(f"{minutes}分钟")
            if include_seconds:
                parts.append(f"{seconds}秒")
            result = " ".join(parts) if parts else "0秒"
        
        elif style == "compact":
            parts = []
            if days > 0:
                parts.append(f"{days}d")
            if hours > 0 or days > 0:
                parts.append(f"{hours}h")
            if minutes > 0 or hours > 0 or days > 0:
                parts.append(f"{minutes}m")
            if include_seconds:
                parts.append(f"{seconds}s")
            result = " ".join(parts) if parts else "0s"
        
        elif style == "chinese":
            parts = []
            if days > 0:
                parts.append(f"{days}天")
            if hours > 0 or days > 0:
                parts.append(f"{hours}小时")
            if minutes > 0 or hours > 0 or days > 0:
                parts.append(f"{minutes}分钟")
            if include_seconds:
                parts.append(f"{seconds}秒")
            result = "".join(parts) if parts else "0秒"
        
        elif style == "digital":
            if include_seconds:
                result = f"{days:02d}:{hours:02d}:{minutes:02d}:{seconds:02d}"
            else:
                result = f"{days:02d}:{hours:02d}:{minutes:02d}"
        
        elif style == "words":
            parts = []
            if days > 0:
                parts.append(f"{days}天")
            if hours > 0:
                parts.append(f"{hours}小时")
            if minutes > 0:
                parts.append(f"{minutes}分钟")
            if include_seconds and seconds > 0:
                parts.append(f"{seconds}秒")
            result = "".join(parts) if parts else "不到1秒"
        
        else:
            result = f"{days}天 {hours}小时 {minutes}分钟"
            if include_seconds:
                result += f" {seconds}秒"
        
        if include_name and self.name:
            result = f"{self.name}: {result}"
        
        return result
    
    def progress_bar(
        self, 
        width: int = 20,
        filled_char: str = "█",
        empty_char: str = "░",
        show_percent: bool = True
    ) -> str:
        """
        生成进度条
        
        Args:
            width: 进度条宽度
            filled_char: 填充字符
            empty_char: 空白字符
            show_percent: 是否显示百分比
        
        Returns:
            进度条字符串
        """
        progress = self.progress
        filled = int(progress * width)
        empty = width - filled
        bar = filled_char * filled + empty_char * empty
        
        if show_percent:
            return f"[{bar}] {progress * 100:.1f}%"
        return f"[{bar}]"
    
    def to_dict(self) -> dict:
        """
        转换为字典格式
        
        Returns:
            包含倒计时信息的字典
        """
        days, hours, minutes, seconds = self.get_components()
        return {
            "name": self.name,
            "target": self.target.isoformat(),
            "start": self.start.isoformat(),
            "remaining_seconds": self.total_seconds,
            "days": days,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds,
            "is_expired": self.is_expired,
            "progress": self.progress,
            "formatted": self.format()
        }
    
    def __str__(self) -> str:
        return self.format()
    
    def __repr__(self) -> str:
        return f"Countdown(target={self.target.isoformat()}, name={self.name!r})"


def create_countdown(
    target: Union[str, datetime],
    start: Optional[Union[str, datetime]] = None,
    name: Optional[str] = None
) -> Countdown:
    """
    创建倒计时实例
    
    Args:
        target: 目标时间
        start: 开始时间
        name: 倒计时名称
    
    Returns:
        Countdown 实例
    """
    return Countdown(target, start, name)


def countdown_from_delta(
    delta: Union[timedelta, int, float],
    name: Optional[str] = None
) -> Countdown:
    """
    从时间差创建倒计时
    
    Args:
        delta: 时间差（timedelta或秒数）
        name: 倒计时名称
    
    Returns:
        Countdown 实例
    
    Example:
        >>> cd = countdown_from_delta(timedelta(days=7))
        >>> cd = countdown_from_delta(3600)  # 1小时后
    """
    if isinstance(delta, (int, float)):
        delta = timedelta(seconds=delta)
    
    target = datetime.now() + delta
    return Countdown(target, name=name)


def multi_countdown(
    targets: List[Union[str, datetime, Tuple[str, str]]]
) -> List[dict]:
    """
    批量倒计时
    
    Args:
        targets: 目标列表，可以是:
            - 字符串（目标时间）
            - datetime对象
            - (名称, 目标时间) 元组
    
    Returns:
        倒计时信息列表
    
    Example:
        >>> targets = [
        ...     "2026-12-31",
        ...     ("春节", "2027-01-29"),
        ...     ("考试", "2026-06-15 09:00:00")
        ... ]
        >>> result = multi_countdown(targets)
    """
    results = []
    
    for target in targets:
        if isinstance(target, tuple):
            name, dt = target
            cd = Countdown(dt, name=name)
        else:
            cd = Countdown(target)
        
        results.append(cd.to_dict())
    
    # 按剩余时间排序
    results.sort(key=lambda x: x["remaining_seconds"])
    return results


def format_duration(
    seconds: Union[int, float],
    style: str = "default"
) -> str:
    """
    格式化持续时间
    
    Args:
        seconds: 秒数
        style: 格式风格
    
    Returns:
        格式化后的时间字符串
    
    Example:
        >>> format_duration(3661)
        '1小时 1分钟 1秒'
        >>> format_duration(86400)
        '1天'
    """
    if seconds < 0:
        return "已结束"
    
    seconds = int(seconds)
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if style == "compact":
        parts = []
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0 or days > 0:
            parts.append(f"{hours}h")
        if minutes > 0 or hours > 0 or days > 0:
            parts.append(f"{minutes}m")
        if secs > 0 or not parts:
            parts.append(f"{secs}s")
        return " ".join(parts)
    
    elif style == "digital":
        return f"{days:02d}:{hours:02d}:{minutes:02d}:{secs:02d}"
    
    else:  # default
        parts = []
        if days > 0:
            parts.append(f"{days}天")
        if hours > 0:
            parts.append(f"{hours}小时")
        if minutes > 0:
            parts.append(f"{minutes}分钟")
        if secs > 0 or not parts:
            parts.append(f"{secs}秒")
        return " ".join(parts)


def time_until(
    target: Union[str, datetime],
    reference: Optional[datetime] = None
) -> timedelta:
    """
    计算到目标时间的剩余时间
    
    Args:
        target: 目标时间
        reference: 参考时间（默认当前时间）
    
    Returns:
        剩余时间的timedelta对象
    """
    if isinstance(target, str):
        # 简单解析
        for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%H:%M:%S", "%H:%M"]:
            try:
                parsed = datetime.strptime(target, fmt)
                if fmt in ["%H:%M:%S", "%H:%M"]:
                    # 只有时间，使用今天的日期
                    today = datetime.now().date()
                    parsed = datetime.combine(today, parsed.time())
                target = parsed
                break
            except ValueError:
                continue
    
    if reference is None:
        reference = datetime.now()
    
    return target - reference


def next_occurrence(
    time_str: str,
    reference: Optional[datetime] = None
) -> datetime:
    """
    获取指定时间的下一次出现
    
    Args:
        time_str: 时间字符串，格式如 "09:00" 或 "17:30"
        reference: 参考时间（默认当前时间）
    
    Returns:
        下一次出现的datetime
    
    Example:
        >>> next_occurrence("09:00")  # 返回今天或明天的9点
    """
    if reference is None:
        reference = datetime.now()
    
    # 解析时间
    for fmt in ["%H:%M:%S", "%H:%M"]:
        try:
            parsed = datetime.strptime(time_str, fmt)
            break
        except ValueError:
            continue
    else:
        raise CountdownError(f"无法解析时间: {time_str}")
    
    # 构造今天的这个时间
    today_time = datetime.combine(reference.date(), parsed.time())
    
    # 如果已经过了，返回明天
    if today_time <= reference:
        return today_time + timedelta(days=1)
    return today_time


def countdown_to_next(time_str: str, name: Optional[str] = None) -> Countdown:
    """
    创建到下一个指定时间的倒计时
    
    Args:
        time_str: 时间字符串，如 "09:00"
        name: 倒计时名称
    
    Returns:
        Countdown 实例
    
    Example:
        >>> cd = countdown_to_next("17:00", "下班")
        >>> print(cd.format())
    """
    target = next_occurrence(time_str)
    return Countdown(target, name=name)


class CountdownTimer:
    """
    简易计时器类（用于正向计时）
    
    Example:
        >>> timer = CountdownTimer()
        >>> # ... 做一些事情 ...
        >>> print(timer.elapsed())
        >>> print(timer.elapsed_formatted())
    """
    
    def __init__(self):
        """初始化计时器"""
        self._start = datetime.now()
        self._paused_at: Optional[datetime] = None
        self._total_paused = timedelta(0)
    
    def elapsed(self) -> timedelta:
        """获取已流逝时间"""
        if self._paused_at:
            return self._paused_at - self._start - self._total_paused
        return datetime.now() - self._start - self._total_paused
    
    def elapsed_seconds(self) -> float:
        """获取已流逝秒数"""
        return self.elapsed().total_seconds()
    
    def elapsed_formatted(self, style: str = "default") -> str:
        """格式化已流逝时间"""
        return format_duration(self.elapsed_seconds(), style)
    
    def pause(self) -> None:
        """暂停计时"""
        if not self._paused_at:
            self._paused_at = datetime.now()
    
    def resume(self) -> None:
        """恢复计时"""
        if self._paused_at:
            self._total_paused += datetime.now() - self._paused_at
            self._paused_at = None
    
    def reset(self) -> None:
        """重置计时器"""
        self._start = datetime.now()
        self._paused_at = None
        self._total_paused = timedelta(0)
    
    def lap(self) -> timedelta:
        """记录一圈时间并返回"""
        elapsed = self.elapsed()
        self.reset()
        return elapsed


# 便捷函数
def days_until(target: Union[str, datetime]) -> int:
    """计算到目标日期的天数"""
    cd = Countdown(target)
    return cd.get_components()[0]


def hours_until(target: Union[str, datetime]) -> int:
    """计算到目标时间的小时数"""
    cd = Countdown(target)
    days, hours, _, _ = cd.get_components()
    return days * 24 + hours


def minutes_until(target: Union[str, datetime]) -> int:
    """计算到目标时间的分钟数"""
    return int(Countdown(target).total_seconds / 60)


if __name__ == "__main__":
    # 演示
    from datetime import datetime, timedelta
    
    print("=" * 50)
    print("倒计时工具演示")
    print("=" * 50)
    
    # 创建一个未来7天的倒计时
    target = datetime.now() + timedelta(days=7, hours=3, minutes=30, seconds=45)
    cd = Countdown(target, name="活动开始")
    
    print(f"\n倒计时: {cd.name}")
    print(f"目标时间: {cd.target}")
    print(f"格式化输出: {cd.format()}")
    print(f"紧凑格式: {cd.format(style='compact')}")
    print(f"数字格式: {cd.format(style='digital')}")
    print(f"进度条: {cd.progress_bar()}")
    
    # 批量倒计时
    print("\n" + "=" * 50)
    print("批量倒计时")
    print("=" * 50)
    
    targets = [
        ("周末", (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")),
        ("月末", "2026-05-31 23:59:59"),
        ("新年", "2027-01-01 00:00:00"),
    ]
    
    for item in multi_countdown(targets):
        print(f"{item['name']}: {item['formatted']}")
    
    # 计时器演示
    print("\n" + "=" * 50)
    print("计时器演示")
    print("=" * 50)
    
    timer = CountdownTimer()
    import time
    time.sleep(0.1)  # 模拟一些操作
    print(f"已用时: {timer.elapsed_formatted()}")