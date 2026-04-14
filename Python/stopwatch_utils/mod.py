"""
StopWatch Utils - 秒表计时工具模块

提供精确计时、性能测量、多计时器管理等功能。
零外部依赖，纯 Python 标准库实现。

核心功能:
- StopWatch: 精确秒表类，支持启动/暂停/重置
- Timer: 倒计时器类，支持回调通知
- LapTimer: 圈计时器，记录多个时间点
- PerformanceTimer: 性能测量计时器，支持上下文管理
- decorators: 计时装饰器
"""

import time
import threading
from typing import Optional, Callable, List, Dict, Any
from dataclasses import dataclass, field
from contextlib import contextmanager
from functools import wraps


@dataclass
class LapRecord:
    """圈记录"""
    lap_number: int
    lap_time: float  # 该圈用时（秒）
    total_time: float  # 累计时间（秒）
    timestamp: float  # 时间戳
    label: Optional[str] = None


class StopWatch:
    """
    精确秒表类
    
    支持启动、暂停、重置、圈计时等功能。
    使用 time.perf_counter() 实现高精度计时。
    
    示例:
        >>> sw = StopWatch()
        >>> sw.start()
        >>> time.sleep(1)
        >>> elapsed = sw.elapsed()  # 获取已用时间
        >>> sw.pause()
        >>> time.sleep(0.5)  # 暂停期间不计入时间
        >>> sw.resume()
        >>> sw.reset()  # 重置秒表
    """
    
    def __init__(self, auto_start: bool = False):
        """
        初始化秒表
        
        Args:
            auto_start: 是否自动开始计时
        """
        self._start_time: Optional[float] = None
        self._pause_time: Optional[float] = None
        self._paused_elapsed: float = 0.0  # 暂停前累计的时间
        self._is_running: bool = False
        self._is_paused: bool = False
        
        if auto_start:
            self.start()
    
    def start(self) -> 'StopWatch':
        """
        启动秒表
        
        Returns:
            self，支持链式调用
        """
        if self._is_running and not self._is_paused:
            return self
        
        if self._is_paused:
            return self.resume()
        
        self._start_time = time.perf_counter()
        self._paused_elapsed = 0.0
        self._is_running = True
        self._is_paused = False
        return self
    
    def pause(self) -> 'StopWatch':
        """
        暂停秒表
        
        Returns:
            self，支持链式调用
        """
        if not self._is_running or self._is_paused:
            return self
        
        self._pause_time = time.perf_counter()
        self._paused_elapsed += self._pause_time - self._start_time
        self._is_paused = True
        return self
    
    def resume(self) -> 'StopWatch':
        """
        恢复暂停的秒表
        
        Returns:
            self，支持链式调用
        """
        if not self._is_paused:
            return self
        
        self._start_time = time.perf_counter()
        self._is_paused = False
        return self
    
    def reset(self) -> 'StopWatch':
        """
        重置秒表
        
        Returns:
            self，支持链式调用
        """
        self._start_time = None
        self._pause_time = None
        self._paused_elapsed = 0.0
        self._is_running = False
        self._is_paused = False
        return self
    
    def elapsed(self, unit: str = 'seconds') -> float:
        """
        获取已用时间
        
        Args:
            unit: 时间单位 ('seconds', 'milliseconds', 'microseconds', 'minutes', 'hours')
        
        Returns:
            已用时间（指定单位）
        """
        if not self._is_running:
            return 0.0
        
        if self._is_paused:
            total = self._paused_elapsed
        else:
            total = self._paused_elapsed + (time.perf_counter() - self._start_time)
        
        # 转换单位
        if unit == 'seconds':
            return total
        elif unit == 'milliseconds':
            return total * 1000
        elif unit == 'microseconds':
            return total * 1000000
        elif unit == 'minutes':
            return total / 60
        elif unit == 'hours':
            return total / 3600
        else:
            raise ValueError(f"未知的时间单位: {unit}")
    
    def elapsed_str(self, precision: int = 3) -> str:
        """
        获取格式化的时间字符串
        
        Args:
            precision: 小数位数
        
        Returns:
            格式化的时间字符串（自动选择合适的单位）
        """
        total = self.elapsed()
        
        if total < 0.001:
            return f"{total * 1000000:.{precision}f} μs"
        elif total < 1:
            return f"{total * 1000:.{precision}f} ms"
        elif total < 60:
            return f"{total:.{precision}f} s"
        elif total < 3600:
            minutes = int(total // 60)
            seconds = total % 60
            return f"{minutes}m {seconds:.{precision}f}s"
        else:
            hours = int(total // 3600)
            minutes = int((total % 3600) // 60)
            seconds = total % 60
            return f"{hours}h {minutes}m {seconds:.{precision}f}s"
    
    @property
    def is_running(self) -> bool:
        """是否正在计时（未暂停）"""
        return self._is_running and not self._is_paused
    
    @property
    def is_paused(self) -> bool:
        """是否已暂停"""
        return self._is_paused
    
    def __enter__(self) -> 'StopWatch':
        """上下文管理器入口"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """上下文管理器出口"""
        self.pause()
    
    def __repr__(self) -> str:
        status = "paused" if self._is_paused else ("running" if self._is_running else "stopped")
        return f"StopWatch(status={status}, elapsed={self.elapsed_str()})"


class LapTimer(StopWatch):
    """
    圈计时器
    
    继承 StopWatch，增加圈计时功能，适合体育计时、
    性能分析等需要记录多个时间点的场景。
    
    示例:
        >>> timer = LapTimer()
        >>> timer.start()
        >>> time.sleep(1)
        >>> timer.lap("第一圈")  # 记录第一圈
        >>> time.sleep(0.5)
        >>> timer.lap("第二圈")  # 记录第二圈
        >>> timer.get_laps()  # 获取所有圈记录
    """
    
    def __init__(self, auto_start: bool = False):
        super().__init__(auto_start=auto_start)
        self._laps: List[LapRecord] = []
        self._last_lap_time: float = 0.0
    
    def lap(self, label: Optional[str] = None) -> LapRecord:
        """
        记录一圈
        
        Args:
            label: 圈标签
        
        Returns:
            圈记录
        """
        if not self._is_running:
            raise RuntimeError("秒表未启动")
        
        current_time = self.elapsed()
        lap_time = current_time - self._last_lap_time
        self._last_lap_time = current_time
        
        record = LapRecord(
            lap_number=len(self._laps) + 1,
            lap_time=lap_time,
            total_time=current_time,
            timestamp=time.time(),
            label=label
        )
        self._laps.append(record)
        return record
    
    def get_laps(self) -> List[LapRecord]:
        """获取所有圈记录"""
        return self._laps.copy()
    
    def get_fastest_lap(self) -> Optional[LapRecord]:
        """获取最快的一圈"""
        if not self._laps:
            return None
        return min(self._laps, key=lambda x: x.lap_time)
    
    def get_slowest_lap(self) -> Optional[LapRecord]:
        """获取最慢的一圈"""
        if not self._laps:
            return None
        return max(self._laps, key=lambda x: x.lap_time)
    
    def get_average_lap(self) -> float:
        """获取平均圈用时"""
        if not self._laps:
            return 0.0
        return sum(lap.lap_time for lap in self._laps) / len(self._laps)
    
    def reset(self) -> 'LapTimer':
        """重置计时器和所有圈记录"""
        super().reset()
        self._laps = []
        self._last_lap_time = 0.0
        return self
    
    def summary(self) -> str:
        """生成计时摘要"""
        lines = [
            f"总计时间: {self.elapsed_str()}",
            f"圈数: {len(self._laps)}"
        ]
        
        if self._laps:
            lines.append(f"平均圈时: {self.get_average_lap():.3f} s")
            fastest = self.get_fastest_lap()
            slowest = self.get_slowest_lap()
            if fastest:
                lines.append(f"最快圈: #{fastest.lap_number} ({fastest.lap_time:.3f} s)")
            if slowest:
                lines.append(f"最慢圈: #{slowest.lap_number} ({slowest.lap_time:.3f} s)")
            
            lines.append("\n圈详情:")
            for lap in self._laps:
                label = f" ({lap.label})" if lap.label else ""
                lines.append(f"  #{lap.lap_number}: {lap.lap_time:.3f}s (累计: {lap.total_time:.3f}s){label}")
        
        return "\n".join(lines)


class Timer:
    """
    倒计时器
    
    支持倒计时和回调通知，可用于超时控制、
    定时任务提醒等场景。
    
    示例:
        >>> def on_timeout():
        ...     print("时间到！")
        >>> timer = Timer(10, callback=on_timeout)  # 10秒倒计时
        >>> timer.start()
        >>> timer.cancel()  # 取消倒计时
    """
    
    def __init__(
        self,
        duration: float,
        callback: Optional[Callable[[], Any]] = None,
        auto_start: bool = False
    ):
        """
        初始化倒计时器
        
        Args:
            duration: 倒计时时长（秒）
            callback: 时间到时的回调函数
            auto_start: 是否自动开始
        """
        self._duration = duration
        self._callback = callback
        self._timer: Optional[threading.Timer] = None
        self._start_time: Optional[float] = None
        self._is_running = False
        self._is_paused = False
        self._remaining: float = duration
        
        if auto_start:
            self.start()
    
    @property
    def duration(self) -> float:
        """总时长"""
        return self._duration
    
    @property
    def is_running(self) -> bool:
        """是否正在运行"""
        return self._is_running and not self._is_paused
    
    def start(self) -> 'Timer':
        """启动倒计时"""
        if self._is_running and not self._is_paused:
            return self
        
        if self._is_paused:
            return self.resume()
        
        self._start_time = time.perf_counter()
        self._is_running = True
        self._is_paused = False
        
        self._timer = threading.Timer(self._remaining, self._on_complete)
        self._timer.start()
        return self
    
    def pause(self) -> 'Timer':
        """暂停倒计时"""
        if not self._is_running or self._is_paused:
            return self
        
        if self._timer:
            self._timer.cancel()
            self._timer = None
        
        elapsed = time.perf_counter() - self._start_time
        self._remaining = self._duration - elapsed
        self._is_paused = True
        return self
    
    def resume(self) -> 'Timer':
        """恢复暂停的倒计时"""
        if not self._is_paused:
            return self
        
        self._start_time = time.perf_counter()
        self._is_paused = False
        
        self._timer = threading.Timer(self._remaining, self._on_complete)
        self._timer.start()
        return self
    
    def cancel(self) -> 'Timer':
        """取消倒计时"""
        if self._timer:
            self._timer.cancel()
            self._timer = None
        self._is_running = False
        self._is_paused = False
        self._remaining = self._duration
        return self
    
    def remaining(self) -> float:
        """获取剩余时间"""
        if not self._is_running:
            return self._remaining
        
        if self._is_paused:
            return self._remaining
        
        elapsed = time.perf_counter() - self._start_time
        return max(0, self._duration - elapsed)
    
    def _on_complete(self):
        """倒计时完成回调"""
        self._is_running = False
        if self._callback:
            self._callback()
    
    def __enter__(self) -> 'Timer':
        return self.start()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cancel()


class PerformanceTimer:
    """
    性能测量计时器
    
    专为性能分析设计，支持上下文管理器和装饰器用法，
    可记录多次测量并计算统计数据。
    
    示例:
        >>> # 上下文管理器用法
        >>> with PerformanceTimer("数据库查询") as timer:
        ...     # 执行操作
        ...     pass
        >>> print(timer.elapsed_str())
        
        >>> # 多次测量
        >>> perf = PerformanceTimer("API调用")
        >>> for _ in range(10):
        ...     with perf.measure():
        ...         # 执行操作
        ...         pass
        >>> print(perf.statistics())
    """
    
    def __init__(self, name: Optional[str] = None, auto_print: bool = False):
        """
        初始化性能计时器
        
        Args:
            name: 计时器名称
            auto_print: 自动打印结果
        """
        self._name = name
        self._auto_print = auto_print
        self._stopwatch = StopWatch()
        self._measurements: List[float] = []
    
    @property
    def name(self) -> Optional[str]:
        return self._name
    
    @contextmanager
    def measure(self):
        """测量代码块执行时间"""
        self._stopwatch.reset().start()
        yield self
        self._stopwatch.pause()
        self._measurements.append(self._stopwatch.elapsed())
    
    def elapsed(self, unit: str = 'seconds') -> float:
        """获取最近一次测量的时间"""
        if not self._measurements:
            return 0.0
        return self._measurements[-1]
    
    def elapsed_str(self, precision: int = 3) -> str:
        """获取最近一次测量的格式化时间"""
        total = self.elapsed()
        if total < 0.001:
            return f"{total * 1000000:.{precision}f} μs"
        elif total < 1:
            return f"{total * 1000:.{precision}f} ms"
        elif total < 60:
            return f"{total:.{precision}f} s"
        else:
            return f"{total / 60:.{precision}f} min"
    
    def get_measurements(self) -> List[float]:
        """获取所有测量记录"""
        return self._measurements.copy()
    
    def count(self) -> int:
        """获取测量次数"""
        return len(self._measurements)
    
    def total(self) -> float:
        """获取总时间"""
        return sum(self._measurements)
    
    def average(self) -> float:
        """获取平均时间"""
        if not self._measurements:
            return 0.0
        return sum(self._measurements) / len(self._measurements)
    
    def min_time(self) -> float:
        """获取最短时间"""
        if not self._measurements:
            return 0.0
        return min(self._measurements)
    
    def max_time(self) -> float:
        """获取最长时间"""
        if not self._measurements:
            return 0.0
        return max(self._measurements)
    
    def statistics(self) -> Dict[str, Any]:
        """获取统计数据"""
        return {
            'name': self._name,
            'count': self.count(),
            'total': self.total(),
            'average': self.average(),
            'min': self.min_time(),
            'max': self.max_time(),
            'measurements': self._measurements.copy()
        }
    
    def summary(self) -> str:
        """生成统计摘要"""
        stats = self.statistics()
        lines = [
            f"性能计时器: {self._name or 'unnamed'}",
            f"  测量次数: {stats['count']}",
            f"  总时间: {stats['total']:.6f}s",
            f"  平均时间: {stats['average']:.6f}s",
            f"  最短时间: {stats['min']:.6f}s",
            f"  最长时间: {stats['max']:.6f}s"
        ]
        return "\n".join(lines)
    
    def __enter__(self) -> 'PerformanceTimer':
        self._stopwatch.reset().start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stopwatch.pause()
        self._measurements.append(self._stopwatch.elapsed())
        if self._auto_print:
            print(f"[{self._name or 'Timer'}] {self.elapsed_str()}")


# ============ 装饰器 ============

def timed(
    name: Optional[str] = None,
    print_result: bool = True,
    precision: int = 3
):
    """
    函数计时装饰器
    
    Args:
        name: 计时器名称（默认使用函数名）
        print_result: 是否打印结果
        precision: 小数位数
    
    示例:
        >>> @timed("数据处理")
        ... def process_data():
        ...     time.sleep(1)
        ...     return "done"
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            timer_name = name or func.__name__
            start = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                elapsed = time.perf_counter() - start
                if elapsed < 0.001:
                    time_str = f"{elapsed * 1000000:.{precision}f} μs"
                elif elapsed < 1:
                    time_str = f"{elapsed * 1000:.{precision}f} ms"
                elif elapsed < 60:
                    time_str = f"{elapsed:.{precision}f} s"
                else:
                    time_str = f"{elapsed / 60:.{precision}f} min"
                
                if print_result:
                    print(f"[{timer_name}] 耗时: {time_str}")
        
        return wrapper
    return decorator


def timed_async(
    name: Optional[str] = None,
    print_result: bool = True,
    precision: int = 3
):
    """
    异步函数计时装饰器
    
    Args:
        name: 计时器名称
        print_result: 是否打印结果
        precision: 小数位数
    
    示例:
        >>> @timed_async("异步操作")
        ... async def async_operation():
        ...     await asyncio.sleep(1)
        ...     return "done"
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            timer_name = name or func.__name__
            start = time.perf_counter()
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                elapsed = time.perf_counter() - start
                if elapsed < 0.001:
                    time_str = f"{elapsed * 1000000:.{precision}f} μs"
                elif elapsed < 1:
                    time_str = f"{elapsed * 1000:.{precision}f} ms"
                elif elapsed < 60:
                    time_str = f"{elapsed:.{precision}f} s"
                else:
                    time_str = f"{elapsed / 60:.{precision}f} min"
                
                if print_result:
                    print(f"[{timer_name}] 耗时: {time_str}")
        
        return wrapper
    return decorator


class StopwatchContext:
    """
    简化的上下文计时器
    
    示例:
        >>> with StopwatchContext("操作名称"):
        ...     # 执行代码
        ...     pass
        # 自动打印: [操作名称] 耗时: 1.234 s
    """
    
    def __init__(self, name: str = "", precision: int = 3, print_result: bool = True):
        self._name = name
        self._precision = precision
        self._print_result = print_result
        self._start: Optional[float] = None
    
    def __enter__(self) -> 'StopwatchContext':
        self._start = time.perf_counter()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.perf_counter() - self._start
        
        if elapsed < 0.001:
            time_str = f"{elapsed * 1000000:.{self._precision}f} μs"
        elif elapsed < 1:
            time_str = f"{elapsed * 1000:.{self._precision}f} ms"
        elif elapsed < 60:
            time_str = f"{elapsed:.{self._precision}f} s"
        else:
            time_str = f"{elapsed / 60:.{self._precision}f} min"
        
        if self._print_result:
            print(f"[{self._name}] 耗时: {time_str}")


# ============ 便捷函数 ============

def measure_time(func: Callable, *args, **kwargs) -> tuple:
    """
    测量函数执行时间
    
    Args:
        func: 要测量的函数
        *args: 函数参数
        **kwargs: 函数关键字参数
    
    Returns:
        (结果, 耗时秒数) 元组
    
    示例:
        >>> result, elapsed = measure_time(time.sleep, 1)
        >>> print(f"返回值: {result}, 耗时: {elapsed:.3f}s")
    """
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start
    return result, elapsed


def measure_time_async(coro) -> tuple:
    """
    测量异步函数执行时间
    
    Args:
        coro: 协程对象
    
    Returns:
        (结果, 耗时秒数) 元组
    
    示例:
        >>> import asyncio
        >>> async def my_async_func():
        ...     await asyncio.sleep(1)
        ...     return "done"
        >>> result, elapsed = asyncio.run(measure_time_async(my_async_func()))
    """
    import asyncio
    
    async def _measure():
        start = time.perf_counter()
        result = await coro
        elapsed = time.perf_counter() - start
        return result, elapsed
    
    return asyncio.run(_measure())


def countdown(
    seconds: int,
    callback: Optional[Callable[[int], Any]] = None,
    interval: float = 1.0
) -> None:
    """
    倒计时函数（阻塞式）
    
    Args:
        seconds: 倒计时秒数
        callback: 每秒回调函数，接收剩余秒数
        interval: 回调间隔（秒）
    
    示例:
        >>> countdown(5, lambda s: print(f"剩余 {s} 秒"))
        剩余 5 秒
        剩余 4 秒
        ...
    """
    remaining = seconds
    while remaining > 0:
        if callback:
            callback(remaining)
        time.sleep(interval)
        remaining -= 1


# 模块导出
__all__ = [
    # 类
    'StopWatch',
    'LapTimer',
    'Timer',
    'PerformanceTimer',
    'StopwatchContext',
    'LapRecord',
    # 装饰器
    'timed',
    'timed_async',
    # 函数
    'measure_time',
    'measure_time_async',
    'countdown',
]