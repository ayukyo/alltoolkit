"""
Terminal Spinner Utils - 终端加载动画工具

提供多种风格的终端加载动画，用于显示长时间操作的进度。
零外部依赖，纯 Python 标准库实现。

功能：
- 多种内置动画样式（dots, arrow, pulse, bounce, wave 等）
- 自定义动画帧
- 支持自定义消息和颜色
- 上下文管理器支持
- 装饰器支持
- 动态消息更新
- 进度百分比显示
"""

import sys
import time
import threading
import itertools
from typing import Callable, Optional, Iterator, Any, List
from contextlib import contextmanager


# 内置动画样式
SPINNER_FRAMES = {
    'dots': ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
    'dots2': ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷'],
    'dots3': ['⠋', '⠙', '⠚', '⠞', '⠖', '⠦', '⠴', '⠲', '⠳', '⠓'],
    'line': ['-', '\\', '|', '/'],
    'line2': ['=', '==', '===', '====', '===', '=='],
    'pipe': ['┤', '┘', '┴', '└', '├', '┌', '┬', '┐'],
    'arrow': ['→', '↘', '↓', '↙', '←', '↖', '↑', '↗'],
    'arrow2': ['▹▹▹▹▹', '▸▹▹▹▹', '▹▸▹▹▹', '▹▹▸▹▹', '▹▹▹▸▹', '▹▹▹▹▸'],
    'bounce': ['[    ]', '[=   ]', '[==  ]', '[=== ]', '[====]', '[ ===]', '[  ==]', '[   =]'],
    'pulse': ['█▁▁▁▁▁▁▁▁▁', '██▁▁▁▁▁▁▁▁', '███▁▁▁▁▁▁▁', '████▁▁▁▁▁▁', 
              '█████▁▁▁▁▁', '██████▁▁▁▁', '███████▁▁▁', '████████▁▁',
              '█████████▁', '██████████', '█████████▁', '████████▁▁'],
    'wave': ['▁▂▃▄▅▆▇█', '▂▃▄▅▆▇█▇', '▃▄▅▆▇█▇▆', '▄▅▆▇█▇▆▅', '▅▆▇█▇▆▅▄',
             '▆▇█▇▆▅▄▃', '▇█▇▆▅▄▃▂', '█▇▆▅▄▃▂▁', '▇▆▅▄▃▂▁▂', '▆▅▄▃▂▁▂▃'],
    'triangle': ['◢', '◣', '◤', '◥'],
    'square': ['■', '□', '■', '□'],
    'star': ['✦', '✧', '✦', '✧'],
    'moon': ['🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘'],
    'earth': ['🌍', '🌎', '🌏'],
    'clock': ['🕐', '🕑', '🕒', '🕓', '🕔', '🕕', '🕖', '🕗', '🕘', '🕙', '🕚', '🕛'],
    'hearts': ['💛', '💙', '💜', '💚', '❤️'],
    'hamburger': ['🍔', '🍟', '🌭', '🍿', '🥤'],
    'weather': ['☀️', '🌤', '⛅', '🌥', '☁️'],
    'balloon': ['🎈', '🎈', '🎈', '🎉', '🎊'],
}

# ANSI 颜色代码
ANSI_COLORS = {
    'black': '\033[30m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    'bright_black': '\033[90m',
    'bright_red': '\033[91m',
    'bright_green': '\033[92m',
    'bright_yellow': '\033[93m',
    'bright_blue': '\033[94m',
    'bright_magenta': '\033[95m',
    'bright_cyan': '\033[96m',
    'bright_white': '\033[97m',
}
ANSI_RESET = '\033[0m'


class Spinner:
    """
    终端加载动画类
    
    示例:
        >>> spinner = Spinner("Loading...", style='dots')
        >>> spinner.start()
        >>> # 执行长时间操作
        >>> spinner.stop()
        
        # 或使用上下文管理器
        >>> with Spinner("Processing...") as s:
        ...     # 执行操作
        ...     pass
    """
    
    def __init__(
        self,
        message: str = "Loading...",
        style: str = 'dots',
        color: Optional[str] = None,
        interval: float = 0.1,
        frames: Optional[List[str]] = None,
        show_elapsed: bool = False,
        show_progress: bool = False,
        output: Any = sys.stderr
    ):
        """
        初始化 Spinner
        
        Args:
            message: 显示的消息
            style: 动画样式名称
            color: 颜色名称 (black, red, green, yellow, blue, magenta, cyan, white)
            interval: 帧间隔时间（秒）
            frames: 自定义动画帧（覆盖 style）
            show_elapsed: 是否显示已用时间
            show_progress: 是否显示进度百分比
            output: 输出流（默认 stderr）
        """
        self.message = message
        self.interval = interval
        self.show_elapsed = show_elapsed
        self.show_progress = show_progress
        self.output = output
        
        # 设置动画帧
        if frames:
            self.frames = frames
        else:
            self.frames = SPINNER_FRAMES.get(style, SPINNER_FRAMES['dots'])
        
        # 设置颜色
        self.color_code = ANSI_COLORS.get(color, '') if color else ''
        self.color_reset = ANSI_RESET if color else ''
        
        # 状态变量
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._start_time: Optional[float] = None
        self._progress: Optional[float] = None
        self._final_message: Optional[str] = None
        self._success_symbol = '✓'
        self._fail_symbol = '✗'
    
    def _animate(self) -> None:
        """动画循环（在后台线程中运行）"""
        frame_iterator = itertools.cycle(self.frames)
        
        while self._running:
            frame = next(frame_iterator)
            elapsed_str = ''
            progress_str = ''
            
            if self.show_elapsed and self._start_time:
                elapsed = time.time() - self._start_time
                elapsed_str = f' [{elapsed:.1f}s]'
            
            if self.show_progress and self._progress is not None:
                progress_str = f' [{self._progress:.0%}]'
            
            output_str = f'\r{self.color_code}{frame}{self.color_reset} {self.message}{progress_str}{elapsed_str}'
            self._write(output_str)
            time.sleep(self.interval)
    
    def _write(self, text: str) -> None:
        """写入输出流"""
        try:
            self.output.write(text)
            self.output.flush()
        except (BrokenPipeError, AttributeError):
            pass
    
    def _clear(self) -> None:
        """清除当前行"""
        self._write('\r' + ' ' * 80 + '\r')
    
    def start(self) -> 'Spinner':
        """启动动画"""
        if self._running:
            return self
        
        self._running = True
        self._start_time = time.time()
        self._thread = threading.Thread(target=self._animate, daemon=True)
        self._thread.start()
        return self
    
    def stop(
        self,
        message: Optional[str] = None,
        success: bool = True,
        symbol: Optional[str] = None
    ) -> None:
        """
        停止动画
        
        Args:
            message: 完成时显示的消息
            success: 是否成功（影响显示的符号）
            symbol: 自定义结束符号
        """
        if not self._running:
            return
        
        self._running = False
        if self._thread:
            self._thread.join()
        
        # 显示最终消息
        final_msg = message if message is not None else self.message
        if symbol is not None:
            final_symbol = symbol
        else:
            final_symbol = self._success_symbol if success else self._fail_symbol
        
        color = '\033[32m' if success else '\033[31m'
        self._clear()
        self._write(f'{color}{final_symbol}{ANSI_RESET} {final_msg}\n')
    
    def update(self, message: str) -> None:
        """
        更新消息
        
        Args:
            message: 新的消息
        """
        self.message = message
    
    def set_progress(self, progress: float) -> None:
        """
        设置进度
        
        Args:
            progress: 进度值 (0.0 - 1.0)
        """
        self._progress = max(0.0, min(1.0, progress))
    
    def __enter__(self) -> 'Spinner':
        """上下文管理器入口"""
        return self.start()
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """上下文管理器退出"""
        success = exc_type is None
        self.stop(success=success)


@contextmanager
def spinner(
    message: str = "Loading...",
    style: str = 'dots',
    color: Optional[str] = None,
    interval: float = 0.1
):
    """
    快捷上下文管理器
    
    Args:
        message: 显示的消息
        style: 动画样式
        color: 颜色名称
        interval: 帧间隔时间
    
    示例:
        >>> with spinner("Processing data..."):
        ...     time.sleep(2)
    """
    s = Spinner(message, style, color, interval)
    s.start()
    try:
        yield s
    finally:
        s.stop()


def spin(
    message: str = "Loading...",
    style: str = 'dots',
    color: Optional[str] = None
) -> Callable:
    """
    装饰器，为函数添加加载动画
    
    Args:
        message: 显示的消息
        style: 动画样式
        color: 颜色名称
    
    示例:
        >>> @spin("Downloading...", style='arrow')
        ... def download_file():
        ...     time.sleep(2)
        ...     return "done"
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            s = Spinner(message, style, color)
            s.start()
            try:
                result = func(*args, **kwargs)
                s.stop(success=True)
                return result
            except Exception as e:
                s.stop(message=f"{message} (Error: {e})", success=False)
                raise
        return wrapper
    return decorator


class SpinnerIterator:
    """
    为迭代器添加进度的包装器
    
    示例:
        >>> items = list(range(100))
        >>> for item in SpinnerIterator(items, "Processing"):
        ...     time.sleep(0.01)
    """
    
    def __init__(
        self,
        iterable: Any,
        message: str = "Processing",
        style: str = 'dots',
        color: Optional[str] = None
    ):
        """
        初始化迭代器包装器
        
        Args:
            iterable: 可迭代对象
            message: 显示的消息
            style: 动画样式
            color: 颜色名称
        """
        self.iterable = iterable
        self.message = message
        self.spinner = Spinner(message, style, color, show_progress=True)
        self._iterator = None
        self._total: Optional[int] = None
        self._count = 0
    
    def __iter__(self) -> Iterator:
        """返回迭代器"""
        try:
            self._total = len(self.iterable)
        except TypeError:
            self._total = None
        
        self._iterator = iter(self.iterable)
        self._count = 0
        self.spinner.start()
        return self
    
    def __next__(self) -> Any:
        """获取下一个元素"""
        try:
            item = next(self._iterator)
            self._count += 1
            
            if self._total:
                self.spinner.set_progress(self._count / self._total)
            
            return item
        except StopIteration:
            self.spinner.stop()
            raise


def animated_wait(
    seconds: float,
    message: str = "Waiting",
    style: str = 'dots',
    color: Optional[str] = None
) -> None:
    """
    带动画的等待
    
    Args:
        seconds: 等待秒数
        message: 显示的消息
        style: 动画样式
        color: 颜色名称
    
    示例:
        >>> animated_wait(5, "Please wait...", style='moon')
    """
    with Spinner(message, style, color, show_elapsed=True) as s:
        end_time = time.time() + seconds
        while time.time() < end_time:
            remaining = end_time - time.time()
            s.update(f"{message} ({remaining:.1f}s remaining)")
            time.sleep(0.1)


class MultiSpinner:
    """
    多任务并发动画管理器
    
    示例:
        >>> with MultiSpinner() as ms:
        ...     ms.add("Task 1", 'dots')
        ...     ms.add("Task 2", 'arrow')
        ...     time.sleep(2)
        ...     ms.complete(0, success=True)
        ...     time.sleep(1)
        ...     ms.complete(1, success=False)
    """
    
    def __init__(self, interval: float = 0.1):
        """初始化多任务管理器"""
        self.tasks: List[dict] = []
        self.interval = interval
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
    
    def add(
        self,
        message: str,
        style: str = 'dots',
        color: Optional[str] = None
    ) -> int:
        """
        添加任务
        
        Args:
            message: 任务消息
            style: 动画样式
            color: 颜色名称
        
        Returns:
            任务索引
        """
        with self._lock:
            frames = SPINNER_FRAMES.get(style, SPINNER_FRAMES['dots'])
            color_code = ANSI_COLORS.get(color, '') if color else ''
            color_reset = ANSI_RESET if color else ''
            
            task = {
                'message': message,
                'frames': frames,
                'frame_iter': itertools.cycle(frames),
                'color_code': color_code,
                'color_reset': color_reset,
                'completed': False,
                'success': True,
                'symbol': '✓'
            }
            self.tasks.append(task)
            return len(self.tasks) - 1
    
    def _animate(self) -> None:
        """动画循环"""
        while self._running:
            with self._lock:
                lines = []
                for task in self.tasks:
                    if task['completed']:
                        color = '\033[32m' if task['success'] else '\033[31m'
                        line = f"  {color}{task['symbol']}{ANSI_RESET} {task['message']}"
                    else:
                        frame = next(task['frame_iter'])
                        line = f"  {task['color_code']}{frame}{task['color_reset']} {task['message']}"
                    lines.append(line)
                
                # 移动到行首并清除
                self._write('\r\033[K')
                # 移动到第一行
                if len(self.tasks) > 1:
                    self._write(f'\033[{len(self.tasks)-1}A')
                
                # 打印所有行
                for i, line in enumerate(lines):
                    if i > 0:
                        self._write('\n')
                    self._write('\r\033[K' + line)
            
            time.sleep(self.interval)
    
    def _write(self, text: str) -> None:
        """写入输出流"""
        try:
            sys.stderr.write(text)
            sys.stderr.flush()
        except (BrokenPipeError, AttributeError):
            pass
    
    def complete(
        self,
        index: int,
        success: bool = True,
        message: Optional[str] = None,
        symbol: Optional[str] = None
    ) -> None:
        """
        标记任务完成
        
        Args:
            index: 任务索引
            success: 是否成功
            message: 更新的消息
            symbol: 自定义符号
        """
        with self._lock:
            if 0 <= index < len(self.tasks):
                self.tasks[index]['completed'] = True
                self.tasks[index]['success'] = success
                if message:
                    self.tasks[index]['message'] = message
                self.tasks[index]['symbol'] = symbol or ('✓' if success else '✗')
    
    def start(self) -> 'MultiSpinner':
        """启动动画"""
        if self._running:
            return self
        
        self._running = True
        self._thread = threading.Thread(target=self._animate, daemon=True)
        self._thread.start()
        return self
    
    def stop(self) -> None:
        """停止动画"""
        if not self._running:
            return
        
        self._running = False
        if self._thread:
            self._thread.join()
        
        # 打印最终状态
        self._write('\n')
    
    def __enter__(self) -> 'MultiSpinner':
        return self.start()
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.stop()


def list_styles() -> List[str]:
    """
    列出所有可用的动画样式
    
    Returns:
        样式名称列表
    """
    return list(SPINNER_FRAMES.keys())


def preview_styles(interval: float = 0.15, duration: float = 2.0) -> None:
    """
    预览所有动画样式
    
    Args:
        interval: 帧间隔时间
        duration: 每个样式的展示时间
    """
    for style in list_styles():
        frames = SPINNER_FRAMES[style]
        print(f"\n{style}:")
        
        start_time = time.time()
        while time.time() - start_time < duration:
            for frame in frames:
                elapsed = time.time() - start_time
                if elapsed >= duration:
                    break
                sys.stdout.write(f'\r  {frame} Loading... ({elapsed:.1f}s)')
                sys.stdout.flush()
                time.sleep(interval)
        
        sys.stdout.write('\r' + ' ' * 50 + '\r')
        sys.stdout.flush()


if __name__ == '__main__':
    # 演示所有功能
    print("=== Terminal Spinner Utils Demo ===\n")
    
    # 基本使用
    print("1. Basic Spinner:")
    with Spinner("Loading data...", style='dots') as s:
        time.sleep(2)
    
    # 不同样式
    print("\n2. Different Styles:")
    for style in ['dots', 'arrow', 'pulse', 'moon', 'hearts']:
        with Spinner(f"Using {style} style", style=style):
            time.sleep(1)
    
    # 带颜色
    print("\n3. With Colors:")
    with Spinner("Processing in cyan...", style='dots', color='cyan'):
        time.sleep(1.5)
    
    # 显示时间
    print("\n4. With Elapsed Time:")
    with Spinner("Computing...", show_elapsed=True):
        time.sleep(2)
    
    # 显示进度
    print("\n5. With Progress:")
    s = Spinner("Processing items...", show_progress=True)
    s.start()
    for i in range(10):
        time.sleep(0.2)
        s.set_progress((i + 1) / 10)
    s.stop()
    
    # 迭代器
    print("\n6. Spinner Iterator:")
    for item in SpinnerIterator(range(20), "Processing items", style='arrow'):
        time.sleep(0.05)
    
    # 装饰器
    print("\n7. Decorator:")
    @spin("Executing task...", style='earth')
    def long_task():
        time.sleep(1.5)
        return "done"
    
    result = long_task()
    print(f"Result: {result}")
    
    # 等待
    print("\n8. Animated Wait:")
    animated_wait(2, "Please wait", style='clock')
    
    # 多任务
    print("\n9. Multi-Spinner:")
    with MultiSpinner() as ms:
        task1 = ms.add("Downloading file 1", 'dots', 'blue')
        task2 = ms.add("Downloading file 2", 'arrow', 'green')
        task3 = ms.add("Processing data", 'moon', 'yellow')
        
        time.sleep(1)
        ms.complete(task1, message="File 1 downloaded")
        
        time.sleep(0.5)
        ms.complete(task2, success=False, message="File 2 failed")
        
        time.sleep(0.5)
        ms.complete(task3, message="Data processed")
    
    print("\n=== Demo Complete ===")