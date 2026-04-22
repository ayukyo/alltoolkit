"""
Progress Bar Utils - 进度条工具集

提供终端进度条显示的实现，适用于：
- 命令行任务进度展示
- 文件下载/上传进度
- 数据处理进度
- 批量任务执行状态

特点：
- 零外部依赖（纯 Python 标准库）
- 支持多种进度条样式
- 支持多任务并行进度
- 支持自定义格式
- 支持预估剩余时间
- 线程安全
"""

import sys
import time
import threading
from typing import Optional, Callable, List, Dict, Any, TextIO, Iterator
from dataclasses import dataclass, field
from contextlib import contextmanager
import math


@dataclass
class ProgressBarStyle:
    """进度条样式配置"""
    filled: str = '█'
    empty: str = '░'
    prefix: str = ''
    suffix: str = ''
    decimals: int = 1
    length: int = 30
    show_eta: bool = True
    show_rate: bool = True
    show_percent: bool = True
    
    @classmethod
    def classic(cls) -> 'ProgressBarStyle':
        """经典样式"""
        return cls(filled='#', empty='-', length=40)
    
    @classmethod
    def modern(cls) -> 'ProgressBarStyle':
        """现代样式"""
        return cls(filled='█', empty='░', length=30)
    
    @classmethod
    def minimal(cls) -> 'ProgressBarStyle':
        """简约样式"""
        return cls(filled='=', empty=' ', length=20, show_eta=False, show_rate=False)
    
    @classmethod
    def blocks(cls) -> 'ProgressBarStyle':
        """方块样式"""
        return cls(filled='▓', empty='░', length=25)
    
    @classmethod
    def arrows(cls) -> 'ProgressBarStyle':
        """箭头样式"""
        return cls(filled='▶', empty='▷', length=20)


class ProgressBar:
    """
    终端进度条
    
    支持多种样式、预估时间、速率显示等功能。
    
    示例:
        >>> # 基础用法
        >>> pb = ProgressBar(100, "下载文件")
        >>> for i in range(100):
        ...     pb.update(i + 1)
        ...     time.sleep(0.01)
        >>> pb.close()
        
        >>> # 使用上下文管理器
        >>> with ProgressBar(100, "处理数据") as pb:
        ...     for i in range(100):
        ...         pb.update(i + 1)
        ...         time.sleep(0.01)
    """
    
    def __init__(
        self,
        total: int,
        desc: str = "",
        style: Optional[ProgressBarStyle] = None,
        file: Optional[TextIO] = None,
        min_update_interval: float = 0.1
    ):
        """
        初始化进度条
        
        Args:
            total: 总任务数
            desc: 描述文字
            style: 进度条样式
            file: 输出文件（默认 stderr）
            min_update_interval: 最小更新间隔（秒）
        """
        if total <= 0:
            raise ValueError("Total must be positive")
        
        self._total = total
        self._desc = desc
        self._style = style or ProgressBarStyle.modern()
        self._file = file or sys.stderr
        self._min_interval = min_update_interval
        
        self._current = 0
        self._start_time: Optional[float] = None
        self._last_update_time: float = 0
        self._last_update_str: str = ""
        self._closed = False
        self._lock = threading.RLock()
        
        # 启动
        self._start_time = time.time()
        self._display()
    
    @property
    def current(self) -> int:
        """当前进度"""
        return self._current
    
    @property
    def total(self) -> int:
        """总数"""
        return self._total
    
    @property
    def progress(self) -> float:
        """进度比例 (0.0 - 1.0)"""
        return self._current / self._total if self._total > 0 else 0.0
    
    @property
    def percent(self) -> float:
        """完成百分比"""
        return self.progress * 100
    
    @property
    def elapsed(self) -> float:
        """已用时间（秒）"""
        if self._start_time is None:
            return 0.0
        return time.time() - self._start_time
    
    @property
    def eta(self) -> Optional[float]:
        """预估剩余时间（秒），如果无法预估返回 None"""
        if self._current <= 0:
            return None
        
        rate = self._current / self.elapsed
        if rate <= 0:
            return None
        
        remaining = self._total - self._current
        return remaining / rate
    
    @property
    def rate(self) -> Optional[float]:
        """处理速率（项/秒）"""
        if self.elapsed <= 0:
            return None
        return self._current / self.elapsed
    
    def update(self, n: int = 1) -> None:
        """
        更新进度
        
        Args:
            n: 增加的数量（默认 1）
        """
        with self._lock:
            if self._closed:
                return
            
            self._current = min(self._current + n, self._total)
            
            # 检查更新间隔
            now = time.time()
            if now - self._last_update_time < self._min_interval and self._current < self._total:
                return
            
            self._last_update_time = now
            self._display()
    
    def set_current(self, current: int) -> None:
        """
        直接设置当前进度
        
        Args:
            current: 当前进度值
        """
        with self._lock:
            if self._closed:
                return
            
            self._current = max(0, min(current, self._total))
            self._last_update_time = time.time()
            self._display()
    
    def _format_time(self, seconds: Optional[float]) -> str:
        """格式化时间"""
        if seconds is None:
            return "?"
        
        if seconds < 60:
            return f"{seconds:.0f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.0f}m {seconds % 60:.0f}s"
        else:
            hours = seconds / 3600
            minutes = (seconds % 3600) / 60
            return f"{hours:.0f}h {minutes:.0f}m"
    
    def _format_rate(self, rate: Optional[float]) -> str:
        """格式化速率"""
        if rate is None:
            return "?"
        
        if rate >= 1000000:
            return f"{rate / 1000000:.1f}M/s"
        elif rate >= 1000:
            return f"{rate / 1000:.1f}K/s"
        else:
            return f"{rate:.1f}/s"
    
    def _display(self) -> None:
        """显示进度条"""
        if self._closed:
            return
        
        percent = self.percent
        filled_length = int(self._style.length * self._current / self._total)
        empty_length = self._style.length - filled_length
        
        bar = self._style.filled * filled_length + self._style.empty * empty_length
        
        # 构建显示字符串
        parts = []
        
        if self._desc:
            parts.append(f"{self._desc}:")
        
        parts.append(f"|{bar}|")
        
        if self._style.show_percent:
            parts.append(f"{percent:.{self._style.decimals}f}%")
        
        parts.append(f"{self._current}/{self._total}")
        
        if self._style.show_eta and self._current > 0:
            parts.append(f"[ETA: {self._format_time(self.eta)}]")
        
        if self._style.show_rate and self._current > 0:
            parts.append(f"[{self._format_rate(self.rate)}]")
        
        elapsed_str = f"[{self._format_time(self.elapsed)}]"
        parts.append(elapsed_str)
        
        line = " ".join(parts)
        
        # 清除之前的内容并写入新行
        clear_line = "\r" + " " * (len(self._last_update_str) + 10) + "\r"
        self._file.write(clear_line + line)
        self._file.flush()
        
        self._last_update_str = line
    
    def close(self) -> None:
        """关闭进度条"""
        with self._lock:
            if self._closed:
                return
            
            self._closed = True
            self._file.write("\n")
            self._file.flush()
    
    def reset(self, total: Optional[int] = None, desc: Optional[str] = None) -> None:
        """
        重置进度条
        
        Args:
            total: 新的总数（可选）
            desc: 新的描述（可选）
        """
        with self._lock:
            self._current = 0
            if total is not None:
                self._total = total
            if desc is not None:
                self._desc = desc
            self._start_time = time.time()
            self._last_update_time = 0
            self._closed = False
            self._display()
    
    def __enter__(self) -> 'ProgressBar':
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
    
    def __repr__(self) -> str:
        return f"ProgressBar(current={self._current}, total={self._total}, desc='{self._desc}')"


class MultiProgressBar:
    """
    多任务并行进度条
    
    同时显示多个任务的进度，适用于并发任务监控。
    
    示例:
        >>> mpb = MultiProgressBar(3)
        >>> mpb.add_task("下载文件A", 100)
        >>> mpb.add_task("下载文件B", 200)
        >>> mpb.add_task("下载文件C", 150)
        >>> mpb.update(0, 50)
        >>> mpb.update(1, 100)
        >>> mpb.close()
    """
    
    def __init__(
        self,
        num_bars: int = 5,
        style: Optional[ProgressBarStyle] = None,
        file: Optional[TextIO] = None
    ):
        """
        初始化多进度条
        
        Args:
            num_bars: 最大任务数
            style: 进度条样式
            file: 输出文件
        """
        self._style = style or ProgressBarStyle.minimal()
        self._file = file or sys.stderr
        self._lock = threading.RLock()
        
        self._tasks: Dict[int, Dict[str, Any]] = {}
        self._task_order: List[int] = []
        self._start_time = time.time()
        self._closed = False
        self._last_display_lines = 0
    
    def add_task(self, desc: str, total: int, task_id: Optional[int] = None) -> int:
        """
        添加任务
        
        Args:
            desc: 任务描述
            total: 总数
            task_id: 任务ID（可选，自动生成）
            
        Returns:
            任务ID
        """
        with self._lock:
            if task_id is None:
                task_id = len(self._task_order)
                while task_id in self._tasks:
                    task_id += 1
            
            self._tasks[task_id] = {
                'desc': desc,
                'total': total,
                'current': 0,
                'start_time': time.time()
            }
            self._task_order.append(task_id)
            
            self._display()
            return task_id
    
    def update(self, task_id: int, n: int = 1) -> None:
        """
        更新任务进度
        
        Args:
            task_id: 任务ID
            n: 增加的数量
        """
        with self._lock:
            if task_id not in self._tasks or self._closed:
                return
            
            task = self._tasks[task_id]
            task['current'] = min(task['current'] + n, task['total'])
            self._display()
    
    def set_progress(self, task_id: int, current: int) -> None:
        """
        直接设置任务进度
        
        Args:
            task_id: 任务ID
            current: 当前进度
        """
        with self._lock:
            if task_id not in self._tasks or self._closed:
                return
            
            task = self._tasks[task_id]
            task['current'] = max(0, min(current, task['total']))
            self._display()
    
    def remove_task(self, task_id: int) -> None:
        """
        移除任务
        
        Args:
            task_id: 任务ID
        """
        with self._lock:
            if task_id in self._tasks:
                del self._tasks[task_id]
                self._task_order.remove(task_id)
                self._display()
    
    def _display(self) -> None:
        """显示所有进度条"""
        if self._closed:
            return
        
        # 清除之前的行
        for _ in range(self._last_display_lines):
            self._file.write("\033[F\033[K")  # 上移一行并清除
        
        lines = []
        for task_id in self._task_order:
            task = self._tasks[task_id]
            current = task['current']
            total = task['total']
            desc = task['desc']
            
            percent = current / total * 100 if total > 0 else 0
            filled_length = int(self._style.length * current / total) if total > 0 else 0
            empty_length = self._style.length - filled_length
            
            bar = self._style.filled * filled_length + self._style.empty * empty_length
            
            line = f"{desc}: |{bar}| {percent:.1f}% ({current}/{total})"
            lines.append(line)
        
        self._file.write("\n".join(lines) + "\n")
        self._file.flush()
        
        self._last_display_lines = len(lines)
    
    def close(self) -> None:
        """关闭多进度条"""
        with self._lock:
            if self._closed:
                return
            self._closed = True
    
    def __enter__(self) -> 'MultiProgressBar':
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()


@contextmanager
def progress(
    total: int,
    desc: str = "",
    style: Optional[ProgressBarStyle] = None
) -> Iterator[ProgressBar]:
    """
    进度条上下文管理器
    
    Args:
        total: 总数
        desc: 描述
        style: 样式
        
    Yields:
        ProgressBar 实例
        
    示例:
        >>> with progress(100, "处理数据") as pb:
        ...     for i in range(100):
        ...         pb.update()
        ...         time.sleep(0.01)
    """
    pb = ProgressBar(total, desc, style)
    try:
        yield pb
    finally:
        pb.close()


def progress_range(
    start: int,
    stop: int,
    step: int = 1,
    desc: str = "",
    style: Optional[ProgressBarStyle] = None
) -> Iterator[int]:
    """
    带进度条的 range 迭代器
    
    Args:
        start: 起始值
        stop: 结束值
        step: 步长
        desc: 描述
        style: 样式
        
    Yields:
        当前值
        
    示例:
        >>> for i in progress_range(0, 100, desc="处理中"):
        ...     time.sleep(0.01)
    """
    total = (stop - start) // step
    pb = ProgressBar(total, desc, style)
    
    try:
        for i, value in enumerate(range(start, stop, step)):
            pb.set_current(i + 1)
            yield value
    finally:
        pb.close()


def progress_iter(
    iterable,
    desc: str = "",
    style: Optional[ProgressBarStyle] = None,
    total: Optional[int] = None
) -> Iterator:
    """
    带进度条的迭代器
    
    Args:
        iterable: 可迭代对象
        desc: 描述
        style: 样式
        total: 总数（可选，自动推断）
        
    Yields:
        迭代元素
        
    示例:
        >>> items = [1, 2, 3, 4, 5]
        >>> for item in progress_iter(items, "处理数据"):
        ...     time.sleep(0.1)
    """
    try:
        # 尝试获取长度
        if total is None:
            total = len(iterable)
    except (TypeError, AttributeError):
        total = None
    
    if total is None:
        # 无法获取长度，使用简单计数
        count = 0
        for item in iterable:
            count += 1
            yield item
        return
    
    pb = ProgressBar(total, desc, style)
    
    try:
        for item in iterable:
            pb.update()
            yield item
    finally:
        pb.close()


class SpinnerProgress:
    """
    旋转加载动画
    
    适用于无法确定进度的长时间任务。
    
    示例:
        >>> with SpinnerProgress("加载数据") as sp:
        ...     time.sleep(5)
    """
    
    SPINNER_FRAMES = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    ASCII_FRAMES = ['|', '/', '-', '\\']
    
    def __init__(
        self,
        desc: str = "",
        file: Optional[TextIO] = None,
        use_unicode: bool = True,
        interval: float = 0.1
    ):
        """
        初始化旋转动画
        
        Args:
            desc: 描述文字
            file: 输出文件
            use_unicode: 是否使用 Unicode 字符
            interval: 帧间隔（秒）
        """
        self._desc = desc
        self._file = file or sys.stderr
        self._frames = self.SPINNER_FRAMES if use_unicode else self.ASCII_FRAMES
        self._interval = interval
        
        self._current_frame = 0
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._start_time: Optional[float] = None
        self._lock = threading.RLock()
    
    @property
    def elapsed(self) -> float:
        """已用时间（秒）"""
        if self._start_time is None:
            return 0.0
        return time.time() - self._start_time
    
    def _spin(self) -> None:
        """旋转动画循环"""
        while self._running:
            with self._lock:
                frame = self._frames[self._current_frame % len(self._frames)]
                elapsed = self._format_time(self.elapsed)
                line = f"\r{frame} {self._desc} [{elapsed}]"
                self._file.write(line)
                self._file.flush()
                self._current_frame += 1
            time.sleep(self._interval)
    
    def _format_time(self, seconds: float) -> str:
        """格式化时间"""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
    
    def start(self) -> None:
        """开始动画"""
        with self._lock:
            if self._running:
                return
            self._running = True
            self._start_time = time.time()
            self._thread = threading.Thread(target=self._spin, daemon=True)
            self._thread.start()
    
    def stop(self, message: Optional[str] = None) -> None:
        """
        停止动画
        
        Args:
            message: 完成消息（可选）
        """
        with self._lock:
            if not self._running:
                return
            self._running = False
        
        if self._thread:
            self._thread.join(timeout=1)
        
        # 清除并输出最终消息
        clear = "\r" + " " * (len(self._desc) + 30) + "\r"
        self._file.write(clear)
        
        if message:
            self._file.write(f"{message}\n")
        else:
            elapsed = self._format_time(self.elapsed)
            self._file.write(f"✓ {self._desc} [{elapsed}]\n")
        self._file.flush()
    
    def __enter__(self) -> 'SpinnerProgress':
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            self.stop(f"✗ {self._desc} [失败]")
        else:
            self.stop()


class ProgressBarBuilder:
    """
    进度条构建器
    
    提供链式调用创建进度条。
    
    示例:
        >>> pb = (ProgressBarBuilder()
        ...     .total(100)
        ...     .desc("下载")
        ...     .style(ProgressBarStyle.modern())
        ...     .build())
    """
    
    def __init__(self):
        self._total: int = 100
        self._desc: str = ""
        self._style: Optional[ProgressBarStyle] = None
        self._file: Optional[TextIO] = None
        self._min_interval: float = 0.1
    
    def total(self, total: int) -> 'ProgressBarBuilder':
        """设置总数"""
        self._total = total
        return self
    
    def desc(self, desc: str) -> 'ProgressBarBuilder':
        """设置描述"""
        self._desc = desc
        return self
    
    def style(self, style: ProgressBarStyle) -> 'ProgressBarBuilder':
        """设置样式"""
        self._style = style
        return self
    
    def file(self, file: TextIO) -> 'ProgressBarBuilder':
        """设置输出文件"""
        self._file = file
        return self
    
    def min_interval(self, interval: float) -> 'ProgressBarBuilder':
        """设置最小更新间隔"""
        self._min_interval = interval
        return self
    
    def build(self) -> ProgressBar:
        """构建进度条"""
        return ProgressBar(
            total=self._total,
            desc=self._desc,
            style=self._style,
            file=self._file,
            min_update_interval=self._min_interval
        )


def create_progress_bar(
    total: int,
    desc: str = "",
    style: str = "modern"
) -> ProgressBar:
    """
    创建进度条的便捷函数
    
    Args:
        total: 总数
        desc: 描述
        style: 样式名称 ("classic", "modern", "minimal", "blocks", "arrows")
        
    Returns:
        ProgressBar 实例
    """
    styles = {
        "classic": ProgressBarStyle.classic,
        "modern": ProgressBarStyle.modern,
        "minimal": ProgressBarStyle.minimal,
        "blocks": ProgressBarStyle.blocks,
        "arrows": ProgressBarStyle.arrows,
    }
    
    style_factory = styles.get(style, ProgressBarStyle.modern)
    return ProgressBar(total, desc, style_factory())


def timed_progress(duration: float, desc: str = "", steps: int = 100) -> None:
    """
    定时进度条
    
    在指定时间内完成进度条动画。
    
    Args:
        duration: 持续时间（秒）
        desc: 描述
        steps: 步数
    """
    interval = duration / steps
    with ProgressBar(steps, desc) as pb:
        for i in range(steps):
            time.sleep(interval)
            pb.update()


# 导出的公共接口
__all__ = [
    'ProgressBarStyle',
    'ProgressBar',
    'MultiProgressBar',
    'SpinnerProgress',
    'ProgressBarBuilder',
    'progress',
    'progress_range',
    'progress_iter',
    'create_progress_bar',
    'timed_progress',
]