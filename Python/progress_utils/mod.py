"""
进度追踪工具模块

提供进度条、进度计算、时间估算等功能，零外部依赖。
"""

import sys
import time
from typing import Any, Callable, Dict, Generator, Iterable, List, Optional, Tuple


class ProgressBar:
    """
    ASCII 进度条生成器
    
    支持多种样式、时间估算、自定义格式。
    """
    
    # 预定义样式
    STYLES = {
        'classic': {'filled': '#', 'empty': '-', 'border': '[]'},
        'modern': {'filled': '█', 'empty': '░', 'border': '||'},
        'dots': {'filled': '●', 'empty': '○', 'border': '[]'},
        'arrows': {'filled': '▶', 'empty': '▷', 'border': '[]'},
        'blocks': {'filled': '▓', 'empty': '░', 'border': '[]'},
        'minimal': {'filled': '=', 'empty': ' ', 'border': '[]'},
        'fancy': {'filled': '▉', 'empty': ' ', 'border': '❰❱'},
    }
    
    def __init__(
        self,
        total: int,
        width: int = 40,
        style: str = 'modern',
        show_percent: bool = True,
        show_eta: bool = True,
        show_count: bool = True,
        output: Any = None,
        prefix: str = '',
        suffix: str = '',
    ):
        """
        初始化进度条
        
        Args:
            total: 总任务数
            width: 进度条宽度（字符数）
            style: 样式名称（classic, modern, dots, arrows, blocks, minimal, fancy）
            show_percent: 是否显示百分比
            show_eta: 是否显示预计剩余时间
            show_count: 是否显示计数（当前/总数）
            output: 输出流（默认 stderr）
            prefix: 前缀文本
            suffix: 后缀文本
        """
        if total <= 0:
            raise ValueError("total 必须为正数")
        
        self.total = total
        self.width = width
        self.show_percent = show_percent
        self.show_eta = show_eta
        self.show_count = show_count
        self.prefix = prefix
        self.suffix = suffix
        self.output = output or sys.stderr
        
        # 获取样式
        if style not in self.STYLES:
            raise ValueError(f"未知样式: {style}，可选: {list(self.STYLES.keys())}")
        self.style = self.STYLES[style]
        
        # 状态
        self.current = 0
        self.start_time: Optional[float] = None
        self.last_update_time: Optional[float] = None
        self._completed = False
    
    def _format_time(self, seconds: float) -> str:
        """格式化时间为可读格式"""
        if seconds < 0 or seconds == float('inf'):
            return '--:--:--'
        
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours:d}:{minutes:02d}:{secs:02d}"
        elif minutes > 0:
            return f"{minutes:d}:{secs:02d}"
        else:
            return f"{secs:d}s"
    
    def _calculate_eta(self, elapsed: float, progress: float) -> float:
        """计算预计剩余时间"""
        if progress <= 0:
            return float('inf')
        if progress >= 1:
            return 0
        
        # 基于当前速度估算
        rate = progress / elapsed
        remaining_progress = 1 - progress
        return remaining_progress / rate if rate > 0 else float('inf')
    
    def render(self, current: Optional[int] = None) -> str:
        """
        渲染进度条字符串
        
        Args:
            current: 当前进度值（可选，默认使用内部状态）
            
        Returns:
            进度条字符串
        """
        if current is not None:
            self.current = max(0, min(current, self.total))
        
        progress = self.current / self.total
        
        # 计算填充长度
        filled_length = int(self.width * progress)
        empty_length = self.width - filled_length
        
        # 构建进度条
        filled = self.style['filled'] * filled_length
        empty = self.style['empty'] * empty_length
        bar = f"{self.style['border'][0]}{filled}{empty}{self.style['border'][1]}"
        
        # 构建显示信息
        parts = []
        
        if self.prefix:
            parts.append(self.prefix)
        
        parts.append(bar)
        
        if self.show_percent:
            parts.append(f"{progress * 100:5.1f}%")
        
        if self.show_count:
            parts.append(f"{self.current}/{self.total}")
        
        if self.show_eta and self.start_time:
            elapsed = time.time() - self.start_time
            eta = self._calculate_eta(elapsed, progress)
            parts.append(f"ETA: {self._format_time(eta)}")
        
        if self.suffix:
            parts.append(self.suffix)
        
        return ' '.join(parts)
    
    def update(self, n: int = 1) -> None:
        """
        更新进度
        
        Args:
            n: 增加的进度量（默认 1）
        """
        if self._completed:
            return
        
        if self.start_time is None:
            self.start_time = time.time()
        
        self.current = min(self.current + n, self.total)
        
        # 输出进度条
        output = self.render()
        self.output.write(f"\r{output}")
        self.output.flush()
        
        # 检查完成
        if self.current >= self.total:
            self._completed = True
            self.output.write('\n')
            self.output.flush()
    
    def set_progress(self, current: int) -> None:
        """
        直接设置当前进度
        
        Args:
            current: 当前进度值
        """
        self.current = max(0, min(current, self.total))
        
        if self.start_time is None:
            self.start_time = time.time()
        
        output = self.render()
        self.output.write(f"\r{output}")
        self.output.flush()
        
        if self.current >= self.total:
            self._completed = True
            self.output.write('\n')
            self.output.flush()
    
    def reset(self) -> None:
        """重置进度条状态"""
        self.current = 0
        self.start_time = None
        self._completed = False
    
    def __enter__(self) -> 'ProgressBar':
        return self
    
    def __exit__(self, *args) -> None:
        if not self._completed:
            self.output.write('\n')
            self.output.flush()


def progress_bar(
    total: int,
    width: int = 40,
    style: str = 'modern',
    **kwargs
) -> ProgressBar:
    """
    创建进度条的快捷函数
    
    Args:
        total: 总任务数
        width: 进度条宽度
        style: 样式名称
        **kwargs: 其他 ProgressBar 参数
        
    Returns:
        ProgressBar 实例
    """
    return ProgressBar(total, width, style, **kwargs)


def track(
    iterable: Iterable,
    total: Optional[int] = None,
    description: str = '',
    style: str = 'modern',
    width: int = 40,
) -> Generator:
    """
    跟踪可迭代对象的进度
    
    Args:
        iterable: 可迭代对象
        total: 总数（自动检测如果可能）
        description: 描述文本
        style: 进度条样式
        width: 进度条宽度
        
    Yields:
        可迭代对象的元素
    """
    # 尝试获取总数
    if total is None:
        try:
            total = len(iterable)  # type: ignore
        except (TypeError, AttributeError):
            total = None
    
    if total is None:
        # 无法获取总数，只显示计数
        count = 0
        for item in iterable:
            count += 1
            sys.stderr.write(f"\r{description} {count} items")
            sys.stderr.flush()
            yield item
        sys.stderr.write('\n')
        sys.stderr.flush()
    else:
        # 有总数，显示进度条
        bar = ProgressBar(
            total=total,
            width=width,
            style=style,
            prefix=description,
        )
        for item in iterable:
            yield item
            bar.update()


class ProgressTracker:
    """
    高级进度追踪器
    
    支持多阶段进度、子任务、回调等功能。
    """
    
    def __init__(
        self,
        total: int,
        description: str = '',
        on_update: Optional[Callable[[int, int, float], None]] = None,
        on_complete: Optional[Callable[[], None]] = None,
    ):
        """
        初始化进度追踪器
        
        Args:
            total: 总任务数
            description: 任务描述
            on_update: 更新回调（current, total, progress）
            on_complete: 完成回调
        """
        self.total = total
        self.description = description
        self.on_update = on_update
        self.on_complete = on_complete
        
        self.current = 0
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self._milestones: List[Tuple[int, str, float]] = []
        self._sub_trackers: List['ProgressTracker'] = []
    
    @property
    def progress(self) -> float:
        """当前进度（0-1）"""
        return self.current / self.total if self.total > 0 else 0
    
    @property
    def percent(self) -> float:
        """当前百分比（0-100）"""
        return self.progress * 100
    
    @property
    def elapsed(self) -> float:
        """已用时间（秒）"""
        if self.start_time is None:
            return 0
        end = self.end_time or time.time()
        return end - self.start_time
    
    @property
    def eta(self) -> float:
        """预计剩余时间（秒）"""
        if self.start_time is None or self.progress <= 0:
            return float('inf')
        if self.progress >= 1:
            return 0
        
        rate = self.current / self.elapsed
        remaining = self.total - self.current
        return remaining / rate if rate > 0 else float('inf')
    
    @property
    def rate(self) -> float:
        """处理速率（项/秒）"""
        if self.elapsed == 0:
            return 0
        return self.current / self.elapsed
    
    @property
    def is_complete(self) -> bool:
        """是否完成"""
        return self.current >= self.total
    
    def start(self) -> 'ProgressTracker':
        """开始追踪"""
        self.start_time = time.time()
        return self
    
    def update(self, n: int = 1) -> 'ProgressTracker':
        """
        更新进度
        
        Args:
            n: 增加的进度量
            
        Returns:
            self（支持链式调用）
        """
        self.current = min(self.current + n, self.total)
        
        if self.on_update:
            self.on_update(self.current, self.total, self.progress)
        
        if self.is_complete and self.on_complete:
            self.end_time = time.time()
            self.on_complete()
        
        return self
    
    def set_progress(self, current: int) -> 'ProgressTracker':
        """
        设置当前进度
        
        Args:
            current: 当前进度值
            
        Returns:
            self（支持链式调用）
        """
        self.current = max(0, min(current, self.total))
        
        if self.on_update:
            self.on_update(self.current, self.total, self.progress)
        
        if self.is_complete:
            self.end_time = time.time()
            if self.on_complete:
                self.on_complete()
        
        return self
    
    def milestone(self, name: str) -> 'ProgressTracker':
        """
        添加里程碑

        Args:
            name: 里程碑名称

        Returns:
            self（支持链式调用）
        """
        self._milestones.append((self.current, name, time.time()))
        return self
    
    def get_milestones(self) -> List[Dict]:
        """获取所有里程碑信息"""
        return [
            {
                'progress': m[0],
                'name': m[1],
                'time': m[2],
                'elapsed_from_start': m[2] - self.start_time if self.start_time else 0,
            }
            for m in self._milestones
        ]
    
    def add_sub_tracker(
        self,
        total: int,
        description: str = '',
        weight: float = 1.0,
    ) -> 'ProgressTracker':
        """
        添加子追踪器

        Args:
            total: 子任务总数
            description: 子任务描述
            weight: 权重（用于计算总进度）

        Returns:
            子追踪器实例
        """
        sub = ProgressTracker(total, description)
        sub._weight = weight  # type: ignore
        self._sub_trackers.append(sub)
        return sub
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        return {
            'description': self.description,
            'current': self.current,
            'total': self.total,
            'progress': self.progress,
            'percent': self.percent,
            'elapsed': self.elapsed,
            'eta': self.eta,
            'rate': self.rate,
            'is_complete': self.is_complete,
            'milestones': len(self._milestones),
        }
    
    def __enter__(self) -> 'ProgressTracker':
        return self.start()
    
    def __exit__(self, *args) -> None:
        if not self.is_complete:
            self.end_time = time.time()


class Spinner:
    """
    终端旋转动画
    
    用于不确定时间的等待过程。
    """
    
    STYLES = {
        'dots': ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
        'line': ['-', '\\', '|', '/'],
        'arrow': ['←', '↖', '↑', '↗', '→', '↘', '↓', '↙'],
        'circle': ['◐', '◓', '◑', '◒'],
        'brackets': ['[    ]', '[=   ]', '[==  ]', '[=== ]', '[====]', '[ ===]', '[  ==]', '[   =]'],
        'bounce': ['[    ]', '[=   ]', '[==  ]', '[=== ]', '[====]', '[ ===]', '[  ==]', '[   =]'],
        'ascii': ['|', '/', '-', '\\'],
    }
    
    def __init__(
        self,
        message: str = 'Loading...',
        style: str = 'dots',
        output: Any = None,
    ):
        """
        初始化旋转动画
        
        Args:
            message: 显示消息
            style: 样式名称
            output: 输出流
        """
        if style not in self.STYLES:
            raise ValueError(f"未知样式: {style}，可选: {list(self.STYLES.keys())}")
        
        self.message = message
        self.frames = self.STYLES[style]
        self.output = output or sys.stderr
        self._index = 0
        self._active = False
    
    def _render(self) -> str:
        """渲染当前帧"""
        frame = self.frames[self._index]
        self._index = (self._index + 1) % len(self.frames)
        return f"{frame} {self.message}"
    
    def update(self, message: Optional[str] = None) -> None:
        """
        更新显示
        
        Args:
            message: 新消息（可选）
        """
        if message:
            self.message = message
        
        output = self._render()
        # 清除当前行并写入新内容
        self.output.write(f"\r{output}   ")
        self.output.flush()
    
    def start(self) -> 'Spinner':
        """开始动画"""
        self._active = True
        self.update()
        return self
    
    def stop(self, final_message: Optional[str] = None) -> None:
        """
        停止动画
        
        Args:
            final_message: 最终消息（可选）
        """
        self._active = False
        if final_message:
            self.output.write(f"\r{final_message}   \n")
        else:
            # 清除动画行
            self.output.write(f"\r{' ' * (len(self.message) + 10)}\r")
        self.output.flush()
    
    def __enter__(self) -> 'Spinner':
        return self.start()
    
    def __exit__(self, *args) -> None:
        self.stop()


class ETAEstimator:
    """
    ETA 估算器
    
    基于历史数据估算剩余时间，使用指数加权移动平均。
    """
    
    def __init__(self, alpha: float = 0.3):
        """
        初始化 ETA 估算器
        
        Args:
            alpha: 平滑因子（0-1），越大越重视近期数据
        """
        self.alpha = alpha
        self._samples: List[Tuple[float, int]] = []
        self._last_time: Optional[float] = None
        self._last_progress: int = 0
        self._ewma_rate: Optional[float] = None
    
    def update(self, progress: int) -> None:
        """
        更新进度
        
        Args:
            progress: 当前进度值
        """
        now = time.time()
        
        if self._last_time is not None:
            time_delta = now - self._last_time
            progress_delta = progress - self._last_progress
            
            if time_delta > 0 and progress_delta > 0:
                instant_rate = progress_delta / time_delta
                
                if self._ewma_rate is None:
                    self._ewma_rate = instant_rate
                else:
                    self._ewma_rate = (
                        self.alpha * instant_rate + 
                        (1 - self.alpha) * self._ewma_rate
                    )
        
        self._last_time = now
        self._last_progress = progress
        self._samples.append((now, progress))
    
    def estimate(self, total: int) -> float:
        """
        估算剩余时间
        
        Args:
            total: 总进度值
            
        Returns:
            预计剩余时间（秒）
        """
        if self._ewma_rate is None or self._ewma_rate <= 0:
            return float('inf')
        
        remaining = total - self._last_progress
        return remaining / self._ewma_rate
    
    def get_rate(self) -> float:
        """获取当前处理速率"""
        return self._ewma_rate or 0
    
    def reset(self) -> None:
        """重置估算器"""
        self._samples.clear()
        self._last_time = None
        self._last_progress = 0
        self._ewma_rate = None


def format_duration(seconds: float) -> str:
    """
    格式化持续时间
    
    Args:
        seconds: 秒数
        
    Returns:
        格式化的时间字符串
    """
    if seconds < 0:
        return "未知"
    
    units = [
        ('年', 31536000),
        ('天', 86400),
        ('小时', 3600),
        ('分钟', 60),
        ('秒', 1),
    ]
    
    for name, divisor in units:
        if seconds >= divisor:
            value = seconds / divisor
            if value < 10:
                return f"{value:.1f}{name}"
            else:
                return f"{int(value)}{name}"
    
    return f"{seconds:.1f}秒"


def format_rate(rate: float, unit: str = '项') -> str:
    """
    格式化处理速率
    
    Args:
        rate: 速率（项/秒）
        unit: 单位名称
        
    Returns:
        格式化的速率字符串
    """
    if rate <= 0:
        return f"0 {unit}/秒"
    
    if rate < 1:
        return f"{rate:.2f} {unit}/秒"
    elif rate < 10:
        return f"{rate:.1f} {unit}/秒"
    elif rate < 1000:
        return f"{rate:.0f} {unit}/秒"
    elif rate < 1000000:
        return f"{rate/1000:.1f}k {unit}/秒"
    else:
        return f"{rate/1000000:.1f}M {unit}/秒"