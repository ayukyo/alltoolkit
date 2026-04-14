"""
Terminal Utilities - 终端控制工具集
零外部依赖的终端控制库，提供颜色输出、光标控制、进度条、表格等功能
"""

import sys
import os
import time
import shutil
from typing import Optional, List, Any, Dict, Union, Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum


class Color(Enum):
    """ANSI 颜色枚举"""
    # 前景色
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    BRIGHT_BLACK = 90
    BRIGHT_RED = 91
    BRIGHT_GREEN = 92
    BRIGHT_YELLOW = 93
    BRIGHT_BLUE = 94
    BRIGHT_MAGENTA = 95
    BRIGHT_CYAN = 96
    BRIGHT_WHITE = 97
    # 背景色
    BG_BLACK = 40
    BG_RED = 41
    BG_GREEN = 42
    BG_YELLOW = 43
    BG_BLUE = 44
    BG_MAGENTA = 45
    BG_CYAN = 46
    BG_WHITE = 47
    BG_BRIGHT_BLACK = 100
    BG_BRIGHT_RED = 101
    BG_BRIGHT_GREEN = 102
    BG_BRIGHT_YELLOW = 103
    BG_BRIGHT_BLUE = 104
    BG_BRIGHT_MAGENTA = 105
    BG_BRIGHT_CYAN = 106
    BG_BRIGHT_WHITE = 107


class Style(Enum):
    """ANSI 样式枚举"""
    RESET = 0
    BOLD = 1
    DIM = 2
    ITALIC = 3
    UNDERLINE = 4
    BLINK = 5
    REVERSE = 7
    HIDDEN = 8
    STRIKETHROUGH = 9


@dataclass
class TerminalSize:
    """终端尺寸"""
    width: int
    height: int


def supports_color() -> bool:
    """检测终端是否支持颜色"""
    if sys.platform == 'win32':
        return os.environ.get('ANSICON') is not None or 'WT_SESSION' in os.environ
    if not hasattr(sys.stdout, 'isatty'):
        return False
    if not sys.stdout.isatty():
        return False
    return os.environ.get('TERM') is not None


def get_terminal_size() -> TerminalSize:
    """获取终端尺寸"""
    try:
        size = shutil.get_terminal_size()
        return TerminalSize(width=size.columns, height=size.lines)
    except Exception:
        return TerminalSize(width=80, height=24)


def clear_screen() -> None:
    """清屏"""
    sys.stdout.write('\033[2J\033[H')
    sys.stdout.flush()


def clear_line(mode: int = 2) -> None:
    """
    清除当前行
    
    Args:
        mode: 0=光标到行尾, 1=行首到光标, 2=整行
    """
    sys.stdout.write(f'\033[{mode}K')
    sys.stdout.flush()


class Cursor:
    """光标控制类"""
    
    @staticmethod
    def hide() -> None:
        """隐藏光标"""
        sys.stdout.write('\033[?25l')
        sys.stdout.flush()
    
    @staticmethod
    def show() -> None:
        """显示光标"""
        sys.stdout.write('\033[?25h')
        sys.stdout.flush()
    
    @staticmethod
    def move_to(row: int, col: int) -> None:
        """
        移动光标到指定位置
        
        Args:
            row: 行号 (1-indexed)
            col: 列号 (1-indexed)
        """
        sys.stdout.write(f'\033[{row};{col}H')
        sys.stdout.flush()
    
    @staticmethod
    def move_up(n: int = 1) -> None:
        """向上移动 n 行"""
        sys.stdout.write(f'\033[{n}A')
        sys.stdout.flush()
    
    @staticmethod
    def move_down(n: int = 1) -> None:
        """向下移动 n 行"""
        sys.stdout.write(f'\033[{n}B')
        sys.stdout.flush()
    
    @staticmethod
    def move_left(n: int = 1) -> None:
        """向左移动 n 列"""
        sys.stdout.write(f'\033[{n}D')
        sys.stdout.flush()
    
    @staticmethod
    def move_right(n: int = 1) -> None:
        """向右移动 n 列"""
        sys.stdout.write(f'\033[{n}C')
        sys.stdout.flush()
    
    @staticmethod
    def save_position() -> None:
        """保存光标位置"""
        sys.stdout.write('\033[s')
        sys.stdout.flush()
    
    @staticmethod
    def restore_position() -> None:
        """恢复光标位置"""
        sys.stdout.write('\033[u')
        sys.stdout.flush()
    
    @staticmethod
    def to_start_of_line() -> None:
        """移动到行首"""
        sys.stdout.write('\r')
        sys.stdout.flush()


class Ansi:
    """ANSI 转义序列处理类"""
    
    @staticmethod
    def color(text: str, fg: Optional[Color] = None, bg: Optional[Color] = None,
             styles: Optional[List[Style]] = None) -> str:
        """
        为文本添加颜色和样式
        
        Args:
            text: 要着色的文本
            fg: 前景色
            bg: 背景色
            styles: 样式列表
        
        Returns:
            着色后的文本
        """
        if not supports_color():
            return text
        
        codes = []
        if fg:
            codes.append(str(fg.value))
        if bg:
            codes.append(str(bg.value))
        if styles:
            codes.extend(str(s.value) for s in styles)
        
        if not codes:
            return text
        
        return f'\033[{";".join(codes)}m{text}\033[0m'
    
    @staticmethod
    def strip(text: str) -> str:
        """移除所有 ANSI 转义序列"""
        result = []
        i = 0
        while i < len(text):
            if text[i] == '\033' and i + 1 < len(text) and text[i + 1] == '[':
                j = i + 2
                while j < len(text) and text[j] not in 'mK':
                    j += 1
                i = j + 1
            else:
                result.append(text[i])
                i += 1
        return ''.join(result)
    
    @staticmethod
    def length(text: str) -> int:
        """获取文本的可见长度（排除 ANSI 序列）"""
        return len(Ansi.strip(text))


# 预定义的快捷颜色函数
def red(text: str) -> str:
    return Ansi.color(text, fg=Color.RED)

def green(text: str) -> str:
    return Ansi.color(text, fg=Color.GREEN)

def yellow(text: str) -> str:
    return Ansi.color(text, fg=Color.YELLOW)

def blue(text: str) -> str:
    return Ansi.color(text, fg=Color.BLUE)

def magenta(text: str) -> str:
    return Ansi.color(text, fg=Color.MAGENTA)

def cyan(text: str) -> str:
    return Ansi.color(text, fg=Color.CYAN)

def white(text: str) -> str:
    return Ansi.color(text, fg=Color.WHITE)

def bold(text: str) -> str:
    return Ansi.color(text, styles=[Style.BOLD])

def dim(text: str) -> str:
    return Ansi.color(text, styles=[Style.DIM])

def underline(text: str) -> str:
    return Ansi.color(text, styles=[Style.UNDERLINE])

def italic(text: str) -> str:
    return Ansi.color(text, styles=[Style.ITALIC])


class ProgressBar:
    """
    终端进度条
    
    支持多种样式、自定义填充字符、预估剩余时间等
    """
    
    def __init__(
        self,
        total: int,
        width: int = 40,
        fill: str = '█',
        empty: str = '░',
        prefix: str = '',
        suffix: str = '',
        show_percent: bool = True,
        show_eta: bool = True,
        show_counter: bool = True,
        color: Optional[Color] = None
    ):
        """
        初始化进度条
        
        Args:
            total: 总任务数
            width: 进度条宽度
            fill: 填充字符
            empty: 空白字符
            prefix: 前缀文本
            suffix: 后缀文本
            show_percent: 是否显示百分比
            show_eta: 是否显示预估剩余时间
            show_counter: 是否显示计数器
            color: 进度条颜色
        """
        self.total = total
        self.width = width
        self.fill = fill
        self.empty = empty
        self.prefix = prefix
        self.suffix = suffix
        self.show_percent = show_percent
        self.show_eta = show_eta
        self.show_counter = show_counter
        self.color = color
        
        self.current = 0
        self.start_time = 0.0
        self.last_update = 0.0
        self._finished = False
    
    def start(self) -> 'ProgressBar':
        """开始进度条"""
        self.current = 0
        self.start_time = time.time()
        self.last_update = self.start_time
        self._finished = False
        Cursor.hide()
        self._render()
        return self
    
    def update(self, n: int = 1) -> 'ProgressBar':
        """更新进度"""
        if self._finished:
            return self
        
        self.current = min(self.current + n, self.total)
        self._render()
        
        if self.current >= self.total:
            self._finished = True
            Cursor.show()
            sys.stdout.write('\n')
            sys.stdout.flush()
        
        return self
    
    def set_progress(self, value: int) -> 'ProgressBar':
        """直接设置进度值"""
        if self._finished:
            return self
        
        self.current = max(0, min(value, self.total))
        self._render()
        
        if self.current >= self.total:
            self._finished = True
            Cursor.show()
            sys.stdout.write('\n')
            sys.stdout.flush()
        
        return self
    
    def _render(self) -> None:
        """渲染进度条"""
        if self._finished:
            return
        
        now = time.time()
        if now - self.last_update < 0.02 and self.current < self.total:
            return
        self.last_update = now
        
        percent = self.current / self.total if self.total > 0 else 0
        filled = int(self.width * percent)
        empty = self.width - filled
        
        bar = self.fill * filled + self.empty * empty
        
        if self.color and supports_color():
            bar = Ansi.color(bar, fg=self.color)
        
        parts = [self.prefix, '[', bar, ']']
        
        if self.show_percent:
            parts.append(f' {percent * 100:5.1f}%')
        
        if self.show_counter:
            parts.append(f' {self.current}/{self.total}')
        
        if self.show_eta and self.current > 0 and percent < 1:
            elapsed = now - self.start_time
            eta = elapsed / percent * (1 - percent)
            parts.append(f' ETA: {self._format_time(eta)}')
        
        parts.append(self.suffix)
        
        line = ''.join(parts)
        sys.stdout.write('\r' + line)
        sys.stdout.flush()
    
    def _format_time(self, seconds: float) -> str:
        """格式化时间"""
        if seconds < 60:
            return f'{int(seconds)}s'
        elif seconds < 3600:
            minutes = int(seconds / 60)
            secs = int(seconds % 60)
            return f'{minutes}m{secs}s'
        else:
            hours = int(seconds / 3600)
            minutes = int((seconds % 3600) / 60)
            return f'{hours}h{minutes}m'
    
    def __enter__(self) -> 'ProgressBar':
        return self.start()
    
    def __exit__(self, *args) -> None:
        if not self._finished:
            self._finished = True
            Cursor.show()
            sys.stdout.write('\n')
            sys.stdout.flush()


class Spinner:
    """
    终端加载动画
    
    支持多种动画样式
    """
    
    STYLES = {
        'dots': ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
        'line': ['-', '\\', '|', '/'],
        'arrow': ['←', '↖', '↑', '↗', '→', '↘', '↓', '↙'],
        'bounce': ['⠁', '⠃', '⠇', '⡇', '⣇', '⣧', '⣷', '⣿', '⣷', '⣧', '⣇', '⡇', '⠇', '⠃', '⠁'],
        'circle': ['◐', '◓', '◑', '◒'],
        'clock': ['🕛', '🕐', '🕑', '🕒', '🕓', '🕔', '🕕', '🕖', '🕗', '🕘', '🕙', '🕚'],
        'moon': ['🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘'],
        'progress': ['█', '▓', '▒', '░'],
    }
    
    def __init__(
        self,
        message: str = 'Loading...',
        style: str = 'dots',
        color: Optional[Color] = None
    ):
        """
        初始化加载动画
        
        Args:
            message: 显示的消息
            style: 动画样式
            color: 动画颜色
        """
        self.message = message
        self.frames = self.STYLES.get(style, self.STYLES['dots'])
        self.color = color
        self._running = False
        self._current_frame = 0
    
    def start(self) -> 'Spinner':
        """开始动画"""
        self._running = True
        self._render()
        return self
    
    def update(self, message: str) -> 'Spinner':
        """更新消息"""
        self.message = message
        self._render()
        return self
    
    def stop(self, final_message: Optional[str] = None) -> None:
        """停止动画"""
        self._running = False
        if final_message:
            sys.stdout.write('\r' + ' ' * (len(self.message) + 10) + '\r')
            print(final_message)
        else:
            sys.stdout.write('\r' + ' ' * (len(self.message) + 10) + '\r')
            sys.stdout.flush()
    
    def _render(self) -> None:
        """渲染当前帧"""
        if not self._running:
            return
        
        frame = self.frames[self._current_frame % len(self.frames)]
        if self.color and supports_color():
            frame = Ansi.color(frame, fg=self.color)
        
        sys.stdout.write(f'\r{frame} {self.message}')
        sys.stdout.flush()
        self._current_frame += 1
    
    def advance(self) -> None:
        """推进一帧"""
        if self._running:
            self._render()
    
    def __enter__(self) -> 'Spinner':
        return self.start()
    
    def __exit__(self, *args) -> None:
        self.stop()


class Table:
    """
    终端表格
    
    支持多种边框样式、自动列宽、对齐等
    """
    
    STYLES = {
        'simple': {
            'horizontal': '-',
            'vertical': '|',
            'corner': '+',
        },
        'double': {
            'horizontal': '═',
            'vertical': '║',
            'corner': '╬',
        },
        'rounded': {
            'horizontal': '─',
            'vertical': '│',
            'top_left': '╭',
            'top_right': '╮',
            'bottom_left': '╰',
            'bottom_right': '╯',
            'left_tee': '├',
            'right_tee': '┤',
            'top_tee': '┬',
            'bottom_tee': '┴',
            'cross': '┼',
        },
        'minimal': {
            'horizontal': '─',
            'vertical': ' ',
            'top_left': '┌',
            'top_right': '┐',
            'bottom_left': '└',
            'bottom_right': '┘',
        },
        'markdown': {
            'horizontal': '-',
            'vertical': '|',
            'corner': '|',
        },
    }
    
    def __init__(
        self,
        headers: Optional[List[str]] = None,
        style: str = 'rounded',
        padding: int = 1,
        header_color: Optional[Color] = None,
        border_color: Optional[Color] = None
    ):
        """
        初始化表格
        
        Args:
            headers: 表头
            style: 边框样式
            padding: 单元格内边距
            header_color: 表头颜色
            border_color: 边框颜色
        """
        self.headers = headers or []
        self.rows: List[List[str]] = []
        self.style_name = style
        self.style = self.STYLES.get(style, self.STYLES['rounded'])
        self.padding = padding
        self.header_color = header_color
        self.border_color = border_color
        self._col_widths: List[int] = []
    
    def add_row(self, *cells: Any) -> 'Table':
        """添加一行"""
        row = [str(cell) for cell in cells]
        self.rows.append(row)
        return self
    
    def _calculate_widths(self) -> List[int]:
        """计算各列宽度"""
        all_rows = [self.headers] + self.rows if self.headers else self.rows
        if not all_rows:
            return []
        
        col_count = max(len(row) for row in all_rows)
        widths = [0] * col_count
        
        for row in all_rows:
            for i, cell in enumerate(row):
                widths[i] = max(widths[i], len(Ansi.strip(cell)))
        
        return widths
    
    def _colorize(self, text: str, color: Optional[Color]) -> str:
        """应用颜色"""
        if color and supports_color():
            return Ansi.color(text, fg=color)
        return text
    
    def _render_horizontal_line(self, width: int, left: str, mid: str, right: str) -> str:
        """渲染水平线"""
        line = left
        for i, w in enumerate(self._col_widths):
            line += self._colorize(self.style.get('horizontal', '-') * (w + self.padding * 2), self.border_color)
            if i < len(self._col_widths) - 1:
                line += mid
        line += right
        return line
    
    def render(self) -> str:
        """渲染表格为字符串"""
        self._col_widths = self._calculate_widths()
        if not self._col_widths:
            return ''
        
        lines = []
        pad = ' ' * self.padding
        v = self._colorize(self.style.get('vertical', '|'), self.border_color)
        
        # 顶部边框
        if self.style_name == 'rounded':
            lines.append(self._render_horizontal_line(len(self._col_widths), 
                self.style['top_left'], self.style['top_tee'], self.style['top_right']))
        elif self.style_name == 'simple':
            lines.append(self._render_horizontal_line(len(self._col_widths), 
                self.style['corner'], self.style['corner'], self.style['corner']))
        elif self.style_name == 'double':
            lines.append(self._render_horizontal_line(len(self._col_widths), 
                self.style['corner'], self.style['corner'], self.style['corner']))
        
        # 表头
        if self.headers:
            cells = []
            for i, header in enumerate(self.headers):
                w = self._col_widths[i] if i < len(self._col_widths) else 0
                content = self._colorize(header, self.header_color) if self.header_color else header
                cells.append(f'{pad}{content:<{w}}{pad}')
            lines.append(f'{v}{v.join(cells)}{v}' if self.style.get('vertical', '|') != ' ' else '  '.join(cells))
            
            # 表头分隔线
            if self.style_name == 'rounded':
                lines.append(self._render_horizontal_line(len(self._col_widths), 
                    self.style['left_tee'], self.style['cross'], self.style['right_tee']))
            elif self.style_name == 'simple':
                lines.append(self._render_horizontal_line(len(self._col_widths), 
                    self.style['corner'], self.style['corner'], self.style['corner']))
            elif self.style_name == 'double':
                lines.append(self._render_horizontal_line(len(self._col_widths), 
                    self.style['corner'], self.style['corner'], self.style['corner']))
            elif self.style_name == 'markdown':
                lines.append(self._render_horizontal_line(len(self._col_widths), 
                    '|', '|', '|'))
        
        # 数据行
        for row in self.rows:
            cells = []
            for i, cell in enumerate(row):
                w = self._col_widths[i] if i < len(self._col_widths) else 0
                cells.append(f'{pad}{cell:<{w}}{pad}')
            if self.style.get('vertical', '|') != ' ':
                lines.append(f'{v}{v.join(cells)}{v}')
            else:
                lines.append('  '.join(cells))
        
        # 底部边框
        if self.style_name == 'rounded':
            lines.append(self._render_horizontal_line(len(self._col_widths), 
                self.style['bottom_left'], self.style['bottom_tee'], self.style['bottom_right']))
        elif self.style_name == 'simple':
            lines.append(self._render_horizontal_line(len(self._col_widths), 
                self.style['corner'], self.style['corner'], self.style['corner']))
        elif self.style_name == 'double':
            lines.append(self._render_horizontal_line(len(self._col_widths), 
                self.style['corner'], self.style['corner'], self.style['corner']))
        
        return '\n'.join(lines)
    
    def print(self) -> None:
        """打印表格"""
        print(self.render())
    
    def __str__(self) -> str:
        return self.render()


class TerminalMenu:
    """
    终端交互菜单
    
    支持键盘导航、多选等
    """
    
    def __init__(
        self,
        options: List[str],
        title: Optional[str] = None,
        cursor: str = '►',
        highlight_color: Optional[Color] = Color.CYAN
    ):
        """
        初始化菜单
        
        Args:
            options: 选项列表
            title: 标题
            cursor: 光标字符
            highlight_color: 高亮颜色
        """
        self.options = options
        self.title = title
        self.cursor = cursor
        self.highlight_color = highlight_color
        self.selected_index = 0
    
    def _render(self) -> None:
        """渲染菜单"""
        if self.title:
            print(bold(self.title))
            print()
        
        for i, option in enumerate(self.options):
            if i == self.selected_index:
                cursor = self._colorize(self.cursor + ' ', self.highlight_color)
                text = self._colorize(option, self.highlight_color)
                print(f'\r{cursor}{text}')
            else:
                print(f'\r  {option}')
    
    def _colorize(self, text: str, color: Optional[Color]) -> str:
        """应用颜色"""
        if color and supports_color():
            return Ansi.color(text, fg=color)
        return text
    
    def select(self) -> int:
        """
        显示菜单并等待用户选择
        
        Returns:
            选中项的索引（从0开始）
        """
        if not self.options:
            return -1
        
        # 简化版：逐行渲染
        self._render()
        
        try:
            # 读取用户输入
            while True:
                key = sys.stdin.read(1)
                
                if key == '\x1b':  # ESC 序列
                    next_key = sys.stdin.read(2)
                    if next_key == '[A':  # 上箭头
                        self.selected_index = (self.selected_index - 1) % len(self.options)
                    elif next_key == '[B':  # 下箭头
                        self.selected_index = (self.selected_index + 1) % len(self.options)
                    # 重新渲染
                    Cursor.move_up(len(self.options) + (2 if self.title else 0))
                    self._render()
                elif key == '\n' or key == '\r':  # Enter
                    break
                elif key == 'q' or key == '\x03':  # q 或 Ctrl+C
                    return -1
        except KeyboardInterrupt:
            return -1
        
        return self.selected_index


class Box:
    """
    终端文本框
    
    支持多种边框样式
    """
    
    STYLES = {
        'single': {
            'tl': '┌', 'tr': '┐', 'bl': '└', 'br': '┘',
            'h': '─', 'v': '│'
        },
        'double': {
            'tl': '╔', 'tr': '╗', 'bl': '╚', 'br': '╝',
            'h': '═', 'v': '║'
        },
        'rounded': {
            'tl': '╭', 'tr': '╮', 'bl': '╰', 'br': '╯',
            'h': '─', 'v': '│'
        },
        'thick': {
            'tl': '┏', 'tr': '┓', 'bl': '┗', 'br': '┛',
            'h': '━', 'v': '┃'
        },
    }
    
    def __init__(
        self,
        text: str,
        title: Optional[str] = None,
        style: str = 'rounded',
        padding: int = 1,
        border_color: Optional[Color] = None,
        text_color: Optional[Color] = None,
        title_color: Optional[Color] = None,
        align: str = 'left'
    ):
        """
        初始化文本框
        
        Args:
            text: 框内文本
            title: 标题
            style: 边框样式
            padding: 内边距
            border_color: 边框颜色
            text_color: 文本颜色
            title_color: 标题颜色
            align: 对齐方式 (left/center/right)
        """
        self.text = text
        self.title = title
        self.style_name = style
        self.style = self.STYLES.get(style, self.STYLES['rounded'])
        self.padding = padding
        self.border_color = border_color
        self.text_color = text_color
        self.title_color = title_color
        self.align = align
    
    def _colorize(self, text: str, color: Optional[Color]) -> str:
        """应用颜色"""
        if color and supports_color():
            return Ansi.color(text, fg=color)
        return text
    
    def render(self) -> str:
        """渲染文本框"""
        lines = self.text.split('\n')
        max_width = max(len(Ansi.strip(line)) for line in lines) if lines else 0
        
        # 考虑标题
        if self.title:
            title_width = len(Ansi.strip(self.title)) + 4
            max_width = max(max_width, title_width)
        
        content_width = max_width + self.padding * 2
        pad = ' ' * self.padding
        
        s = self.style
        h = self._colorize(s['h'] * content_width, self.border_color)
        v = self._colorize(s['v'], self.border_color)
        
        result = []
        
        # 顶部边框
        if self.title:
            title_text = self._colorize(self.title, self.title_color)
            title_line = f" {title_text} "
            title_line_len = len(Ansi.strip(title_line))
            top = self._colorize(s['tl'], self.border_color) + \
                  self._colorize(s['h'] * ((content_width - title_line_len) // 2), self.border_color) + \
                  title_line + \
                  self._colorize(s['h'] * (content_width - title_line_len - (content_width - title_line_len) // 2), self.border_color) + \
                  self._colorize(s['tr'], self.border_color)
        else:
            top = self._colorize(s['tl'], self.border_color) + h + self._colorize(s['tr'], self.border_color)
        result.append(top)
        
        # 内容行
        for line in lines:
            content = self._colorize(line, self.text_color)
            stripped_len = len(Ansi.strip(line))
            
            if self.align == 'center':
                padding_left = (max_width - stripped_len) // 2
                padding_right = max_width - stripped_len - padding_left
            elif self.align == 'right':
                padding_left = max_width - stripped_len
                padding_right = 0
            else:
                padding_left = 0
                padding_right = max_width - stripped_len
            
            padded_content = ' ' * padding_left + content + ' ' * padding_right
            result.append(f"{v}{pad}{padded_content}{pad}{v}")
        
        # 底部边框
        bottom = self._colorize(s['bl'], self.border_color) + h + self._colorize(s['br'], self.border_color)
        result.append(bottom)
        
        return '\n'.join(result)
    
    def print(self) -> None:
        """打印文本框"""
        print(self.render())
    
    def __str__(self) -> str:
        return self.render()


@contextmanager
def hidden_cursor():
    """隐藏光标的上下文管理器"""
    Cursor.hide()
    try:
        yield
    finally:
        Cursor.show()


@contextmanager
def saved_cursor():
    """保存/恢复光标位置的上下文管理器"""
    Cursor.save_position()
    try:
        yield
    finally:
        Cursor.restore_position()


def bell() -> None:
    """发出终端铃声"""
    sys.stdout.write('\a')
    sys.stdout.flush()


def set_title(title: str) -> None:
    """设置终端窗口标题"""
    sys.stdout.write(f'\033]0;{title}\a')
    sys.stdout.flush()


def beep(count: int = 1, interval: float = 0.2) -> None:
    """
    发出蜂鸣声
    
    Args:
        count: 蜂鸣次数
        interval: 间隔秒数
    """
    for _ in range(count):
        bell()
        if count > 1:
            time.sleep(interval)


def strip_ansi(text: str) -> str:
    """移除所有 ANSI 转义序列（别名）"""
    return Ansi.strip(text)


def visible_length(text: str) -> int:
    """获取文本的可见长度（别名）"""
    return Ansi.length(text)


# 导出的公共接口
__all__ = [
    'Color',
    'Style',
    'TerminalSize',
    'Ansi',
    'Cursor',
    'ProgressBar',
    'Spinner',
    'Table',
    'TerminalMenu',
    'Box',
    'supports_color',
    'get_terminal_size',
    'clear_screen',
    'clear_line',
    'hidden_cursor',
    'saved_cursor',
    'bell',
    'set_title',
    'beep',
    'strip_ansi',
    'visible_length',
    # 颜色快捷函数
    'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white',
    'bold', 'dim', 'underline', 'italic',
]