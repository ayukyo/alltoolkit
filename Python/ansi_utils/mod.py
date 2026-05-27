"""
ANSI Terminal Utilities - 零外部依赖的终端样式和光标控制工具包

功能:
- 256色和真彩色支持
- 文本样式 (粗体、斜体、下划线、闪烁等)
- 光标控制 (移动、隐藏、保存/恢复)
- 屏幕操作 (清屏、滚动)
- 进度条和表格
- 终端检测和兼容性处理
- 链式调用 API
"""

import os
import sys
from typing import Optional, Tuple, List, Union
from functools import wraps


def _supports_color() -> bool:
    """检测终端是否支持颜色"""
    # 检查是否在 TTY 环境
    if not hasattr(sys.stdout, 'isatty'):
        return False
    if not sys.stdout.isatty():
        return False
    
    # 检查环境变量
    term = os.environ.get('TERM', '').lower()
    colorterm = os.environ.get('COLORTERM', '').lower()
    
    # NO_COLOR 环境变量
    if os.environ.get('NO_COLOR'):
        return False
    
    # 常见支持颜色的终端
    color_terms = ['xterm', 'xterm-256color', 'screen', 'screen-256color',
                   'tmux', 'tmux-256color', 'vt100', 'ansi', 'linux',
                   'cygwin', 'color', 'truecolor']
    
    if any(t in term for t in color_terms):
        return True
    
    if 'truecolor' in colorterm or '24bit' in colorterm:
        return True
    
    # Windows 10+ 支持 ANSI
    if sys.platform == 'win32':
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            # 启用 ANSI 转义序列
            handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
            mode = ctypes.c_ulong()
            kernel32.GetConsoleMode(handle, ctypes.byref(mode))
            return (mode.value & 0x0004) != 0  # ENABLE_VIRTUAL_TERMINAL_PROCESSING
        except:
            return False
    
    return False


def _supports_256color() -> bool:
    """检测是否支持 256 色"""
    if not _supports_color():
        return False
    
    term = os.environ.get('TERM', '').lower()
    colorterm = os.environ.get('COLORTERM', '').lower()
    
    return '256color' in term or '256' in term or colorterm != ''


def _supports_truecolor() -> bool:
    """检测是否支持真彩色"""
    if not _supports_color():
        return False
    
    colorterm = os.environ.get('COLORTERM', '').lower()
    term = os.environ.get('TERM', '').lower()
    
    return 'truecolor' in colorterm or 'truecolor' in term or '24bit' in colorterm


# 全局状态
_COLOR_SUPPORT = _supports_color()
_256COLOR_SUPPORT = _supports_256color()
_TRUECOLOR_SUPPORT = _supports_truecolor()


class ANSI:
    """ANSI 转义序列生成器"""
    
    # 基础转义
    ESC = '\033'
    CSI = ESC + '['
    OSC = ESC + ']'
    
    # 重置
    RESET = CSI + '0m'
    
    # 文本样式
    BOLD = CSI + '1m'
    DIM = CSI + '2m'
    ITALIC = CSI + '3m'
    UNDERLINE = CSI + '4m'
    BLINK = CSI + '5m'
    RAPID_BLINK = CSI + '6m'
    REVERSE = CSI + '7m'
    HIDDEN = CSI + '8m'
    STRIKETHROUGH = CSI + '9m'
    
    # 样式重置
    BOLD_OFF = CSI + '22m'
    ITALIC_OFF = CSI + '23m'
    UNDERLINE_OFF = CSI + '24m'
    BLINK_OFF = CSI + '25m'
    REVERSE_OFF = CSI + '27m'
    HIDDEN_OFF = CSI + '28m'
    STRIKETHROUGH_OFF = CSI + '29m'
    
    # 标准 16 色
    COLORS = {
        'black': 0, 'red': 1, 'green': 2, 'yellow': 3,
        'blue': 4, 'magenta': 5, 'cyan': 6, 'white': 7,
        'bright_black': 8, 'bright_red': 9, 'bright_green': 10,
        'bright_yellow': 11, 'bright_blue': 12, 'bright_magenta': 13,
        'bright_cyan': 14, 'bright_white': 15
    }
    
    @classmethod
    def fg(cls, color: Union[str, int, Tuple[int, int, int]]) -> str:
        """设置前景色
        
        Args:
            color: 颜色名称、8位色码或 RGB 元组
        
        Returns:
            ANSI 转义序列
        """
        if not _COLOR_SUPPORT:
            return ''
        
        if isinstance(color, str):
            # 标准颜色名称
            if color.lower() in cls.COLORS:
                idx = cls.COLORS[color.lower()]
                # 标准 0-7 用 30-37，高亮 8-15 用 90-97
                if idx < 8:
                    code = 30 + idx
                else:
                    code = 90 + (idx - 8)
                return f'{cls.CSI}{code}m'
            return ''
        
        if isinstance(color, int):
            # 256 色
            if 0 <= color <= 255:
                if _TRUECOLOR_SUPPORT or _256COLOR_SUPPORT:
                    return f'{cls.CSI}38;5;{color}m'
            return ''
        
        if isinstance(color, (tuple, list)) and len(color) == 3:
            # RGB 真彩色
            r, g, b = color
            if all(0 <= c <= 255 for c in (r, g, b)):
                if _TRUECOLOR_SUPPORT:
                    return f'{cls.CSI}38;2;{r};{g};{b}m'
                elif _256COLOR_SUPPORT:
                    # 降级到 256 色
                    code = cls._rgb_to_256(r, g, b)
                    return f'{cls.CSI}38;5;{code}m'
            return ''
        
        return ''
    
    @classmethod
    def bg(cls, color: Union[str, int, Tuple[int, int, int]]) -> str:
        """设置背景色
        
        Args:
            color: 颜色名称、8位色码或 RGB 元组
        
        Returns:
            ANSI 转义序列
        """
        if not _COLOR_SUPPORT:
            return ''
        
        if isinstance(color, str):
            if color.lower() in cls.COLORS:
                idx = cls.COLORS[color.lower()]
                # 标准 0-7 用 40-47，高亮 8-15 用 100-107
                if idx < 8:
                    code = 40 + idx
                else:
                    code = 100 + (idx - 8)
                return f'{cls.CSI}{code}m'
            return ''
        
        if isinstance(color, int):
            if 0 <= color <= 255:
                if _TRUECOLOR_SUPPORT or _256COLOR_SUPPORT:
                    return f'{cls.CSI}48;5;{color}m'
            return ''
        
        if isinstance(color, (tuple, list)) and len(color) == 3:
            r, g, b = color
            if all(0 <= c <= 255 for c in (r, g, b)):
                if _TRUECOLOR_SUPPORT:
                    return f'{cls.CSI}48;2;{r};{g};{b}m'
                elif _256COLOR_SUPPORT:
                    code = cls._rgb_to_256(r, g, b)
                    return f'{cls.CSI}48;5;{code}m'
            return ''
        
        return ''
    
    @classmethod
    def _rgb_to_256(cls, r: int, g: int, b: int) -> int:
        """将 RGB 转换为最接近的 256 色码"""
        if r == g == b:
            # 灰度
            if r < 8:
                return 16
            if r > 248:
                return 231
            return round((r - 8) / 247 * 24) + 232
        
        # 6x6x6 色立方
        return 16 + (36 * round(r / 255 * 5) +
                     6 * round(g / 255 * 5) +
                     round(b / 255 * 5))
    
    @classmethod
    def reset(cls) -> str:
        """重置所有样式"""
        return cls.RESET
    
    @classmethod
    def bold(cls, text: str = '') -> str:
        """粗体文本"""
        if not _COLOR_SUPPORT:
            return text
        return f'{cls.BOLD}{text}{cls.RESET}' if text else cls.BOLD
    
    @classmethod
    def dim(cls, text: str = '') -> str:
        """暗淡文本"""
        if not _COLOR_SUPPORT:
            return text
        return f'{cls.DIM}{text}{cls.RESET}' if text else cls.DIM
    
    @classmethod
    def italic(cls, text: str = '') -> str:
        """斜体文本"""
        if not _COLOR_SUPPORT:
            return text
        return f'{cls.ITALIC}{text}{cls.RESET}' if text else cls.ITALIC
    
    @classmethod
    def underline(cls, text: str = '') -> str:
        """下划线文本"""
        if not _COLOR_SUPPORT:
            return text
        return f'{cls.UNDERLINE}{text}{cls.RESET}' if text else cls.UNDERLINE
    
    @classmethod
    def strikethrough(cls, text: str = '') -> str:
        """删除线文本"""
        if not _COLOR_SUPPORT:
            return text
        return f'{cls.STRIKETHROUGH}{text}{cls.RESET}' if text else cls.STRIKETHROUGH
    
    @classmethod
    def blink(cls, text: str = '') -> str:
        """闪烁文本"""
        if not _COLOR_SUPPORT:
            return text
        return f'{cls.BLINK}{text}{cls.RESET}' if text else cls.BLINK
    
    @classmethod
    def reverse(cls, text: str = '') -> str:
        """反转前景/背景色"""
        if not _COLOR_SUPPORT:
            return text
        return f'{cls.REVERSE}{text}{cls.RESET}' if text else cls.REVERSE
    
    @classmethod
    def hide(cls, text: str = '') -> str:
        """隐藏文本"""
        if not _COLOR_SUPPORT:
            return text
        return f'{cls.HIDDEN}{text}{cls.RESET}' if text else cls.HIDDEN


class Cursor:
    """光标控制"""
    
    CSI = '\033['
    
    @classmethod
    def up(cls, n: int = 1) -> str:
        """向上移动光标"""
        return f'{cls.CSI}{n}A'
    
    @classmethod
    def down(cls, n: int = 1) -> str:
        """向下移动光标"""
        return f'{cls.CSI}{n}B'
    
    @classmethod
    def forward(cls, n: int = 1) -> str:
        """向前移动光标"""
        return f'{cls.CSI}{n}C'
    
    @classmethod
    def back(cls, n: int = 1) -> str:
        """向后移动光标"""
        return f'{cls.CSI}{n}D'
    
    @classmethod
    def next_line(cls, n: int = 1) -> str:
        """移动到下 n 行开头"""
        return f'{cls.CSI}{n}E'
    
    @classmethod
    def prev_line(cls, n: int = 1) -> str:
        """移动到上 n 行开头"""
        return f'{cls.CSI}{n}F'
    
    @classmethod
    def column(cls, n: int) -> str:
        """移动到当前行的第 n 列"""
        return f'{cls.CSI}{n}G'
    
    @classmethod
    def position(cls, row: int, col: int) -> str:
        """移动到指定行列位置"""
        return f'{cls.CSI}{row};{col}H'
    
    @classmethod
    def save(cls) -> str:
        """保存光标位置"""
        return f'{cls.CSI}s'
    
    @classmethod
    def restore(cls) -> str:
        """恢复光标位置"""
        return f'{cls.CSI}u'
    
    @classmethod
    def hide_cursor(cls) -> str:
        """隐藏光标"""
        return f'{cls.CSI}?25l'
    
    @classmethod
    def show_cursor(cls) -> str:
        """显示光标"""
        return f'{cls.CSI}?25h'


class Screen:
    """屏幕操作"""
    
    CSI = '\033['
    
    @classmethod
    def clear(cls) -> str:
        """清屏"""
        return f'{cls.CSI}2J'
    
    @classmethod
    def clear_from_cursor(cls) -> str:
        """从光标位置清除到屏幕末尾"""
        return f'{cls.CSI}J'
    
    @classmethod
    def clear_to_cursor(cls) -> str:
        """从屏幕开头清除到光标位置"""
        return f'{cls.CSI}1J'
    
    @classmethod
    def clear_line(cls) -> str:
        """清除当前行"""
        return f'{cls.CSI}2K'
    
    @classmethod
    def clear_line_from_cursor(cls) -> str:
        """从光标位置清除到行尾"""
        return f'{cls.CSI}K'
    
    @classmethod
    def clear_line_to_cursor(cls) -> str:
        """从行首清除到光标位置"""
        return f'{cls.CSI}1K'
    
    @classmethod
    def scroll_up(cls, n: int = 1) -> str:
        """向上滚动 n 行"""
        return f'{cls.CSI}{n}S'
    
    @classmethod
    def scroll_down(cls, n: int = 1) -> str:
        """向下滚动 n 行"""
        return f'{cls.CSI}{n}T'
    
    @classmethod
    def set_title(cls, title: str) -> str:
        """设置终端标题"""
        return f'\033]0;{title}\007'


class Style:
    """链式样式构建器"""
    
    def __init__(self, text: str = ''):
        self._text = text
        self._styles: List[str] = []
        self._prefix: str = ''
        self._suffix: str = ''
    
    def bold(self) -> 'Style':
        """添加粗体样式"""
        if _COLOR_SUPPORT:
            self._styles.append(ANSI.BOLD)
        return self
    
    def dim(self) -> 'Style':
        """添加暗淡样式"""
        if _COLOR_SUPPORT:
            self._styles.append(ANSI.DIM)
        return self
    
    def italic(self) -> 'Style':
        """添加斜体样式"""
        if _COLOR_SUPPORT:
            self._styles.append(ANSI.ITALIC)
        return self
    
    def underline(self) -> 'Style':
        """添加下划线样式"""
        if _COLOR_SUPPORT:
            self._styles.append(ANSI.UNDERLINE)
        return self
    
    def strikethrough(self) -> 'Style':
        """添加删除线样式"""
        if _COLOR_SUPPORT:
            self._styles.append(ANSI.STRIKETHROUGH)
        return self
    
    def blink(self) -> 'Style':
        """添加闪烁样式"""
        if _COLOR_SUPPORT:
            self._styles.append(ANSI.BLINK)
        return self
    
    def reverse(self) -> 'Style':
        """添加反转样式"""
        if _COLOR_SUPPORT:
            self._styles.append(ANSI.REVERSE)
        return self
    
    def fg(self, color: Union[str, int, Tuple[int, int, int]]) -> 'Style':
        """设置前景色"""
        if _COLOR_SUPPORT:
            self._styles.append(ANSI.fg(color))
        return self
    
    def bg(self, color: Union[str, int, Tuple[int, int, int]]) -> 'Style':
        """设置背景色"""
        if _COLOR_SUPPORT:
            self._styles.append(ANSI.bg(color))
        return self
    
    def color(self, color: Union[str, int, Tuple[int, int, int]]) -> 'Style':
        """设置前景色 (fg 的别名)"""
        return self.fg(color)
    
    def on(self, color: Union[str, int, Tuple[int, int, int]]) -> 'Style':
        """设置背景色 (bg 的别名)"""
        return self.bg(color)
    
    def text(self, content: str) -> 'Style':
        """设置文本内容"""
        self._text = content
        return self
    
    def prefix(self, s: str) -> 'Style':
        """添加前缀"""
        self._prefix = s
        return self
    
    def suffix(self, s: str) -> 'Style':
        """添加后缀"""
        self._suffix = s
        return self
    
    def render(self) -> str:
        """渲染样式文本"""
        if not self._styles:
            return f'{self._prefix}{self._text}{self._suffix}'
        styles = ''.join(self._styles)
        return f'{self._prefix}{styles}{self._text}{ANSI.RESET}{self._suffix}'
    
    def __str__(self) -> str:
        return self.render()
    
    def __repr__(self) -> str:
        return self.render()


class ProgressBar:
    """进度条"""
    
    def __init__(self, total: int, width: int = 40, 
                 filled_char: str = '█', empty_char: str = '░',
                 style: Optional[Style] = None):
        self.total = total
        self.width = width
        self.filled_char = filled_char
        self.empty_char = empty_char
        self.style = style
        self._current = 0
    
    def update(self, current: int) -> str:
        """更新进度条"""
        self._current = min(current, self.total)
        percent = self._current / self.total if self.total > 0 else 0
        filled = int(self.width * percent)
        empty = self.width - filled
        
        bar = self.filled_char * filled + self.empty_char * empty
        percent_str = f'{percent * 100:5.1f}%'
        
        result = f'[{bar}] {percent_str}'
        
        if self.style:
            return self.style.text(result).render()
        return result
    
    def __str__(self) -> str:
        return self.update(self._current)


class Table:
    """简单的文本表格"""
    
    def __init__(self, headers: Optional[List[str]] = None,
                 border: bool = True,
                 border_style: Optional[Style] = None,
                 header_style: Optional[Style] = None):
        self.headers = headers or []
        self.rows: List[List[str]] = []
        self.border = border
        self.border_style = border_style or Style().dim()
        self.header_style = header_style or Style().bold()
        self._col_widths: List[int] = []
    
    def add_row(self, *cells: str) -> 'Table':
        """添加一行"""
        self.rows.append([str(c) for c in cells])
        return self
    
    def _calculate_widths(self) -> List[int]:
        """计算每列宽度"""
        all_rows = [self.headers] + self.rows if self.headers else self.rows
        if not all_rows:
            return []
        
        num_cols = max(len(row) for row in all_rows)
        widths = [0] * num_cols
        
        for row in all_rows:
            for i, cell in enumerate(row):
                # 去除 ANSI 转义序列计算实际宽度
                clean_cell = self._strip_ansi(cell)
                widths[i] = max(widths[i], len(clean_cell))
        
        return widths
    
    def _strip_ansi(self, text: str) -> str:
        """移除 ANSI 转义序列"""
        result = []
        i = 0
        while i < len(text):
            if text[i] == '\033':
                # 跳过转义序列
                while i < len(text) and text[i] != 'm':
                    i += 1
                i += 1  # 跳过 'm'
            else:
                result.append(text[i])
                i += 1
        return ''.join(result)
    
    def _pad_cell(self, cell: str, width: int) -> str:
        """填充单元格到指定宽度"""
        clean_len = len(self._strip_ansi(cell))
        padding = ' ' * (width - clean_len)
        return f'{cell}{padding}'
    
    def render(self) -> str:
        """渲染表格"""
        widths = self._calculate_widths()
        if not widths:
            return ''
        
        lines = []
        total_width = sum(widths) + len(widths) + 1
        
        # 顶部边框
        if self.border:
            border_line = '+' + '+'.join('-' * w for w in widths) + '+'
            if self.border_style:
                border_line = self.border_style.text(border_line).render()
            lines.append(border_line)
        
        # 表头
        if self.headers:
            cells = [self._pad_cell(h, w) for h, w in zip(self.headers, widths)]
            if self.border:
                row = '|' + '|'.join(cells) + '|'
            else:
                row = ' '.join(cells)
            
            if self.header_style:
                # 对整个行应用样式会破坏边框，只对内容应用
                content = '|' + '|'.join(cells) + '|' if self.border else ' '.join(cells)
                lines.append(content)
            else:
                lines.append(row)
            
            if self.border:
                border_line = '+' + '+'.join('-' * w for w in widths) + '+'
                if self.border_style:
                    border_line = self.border_style.text(border_line).render()
                lines.append(border_line)
        
        # 数据行
        for row in self.rows:
            cells = []
            for i, cell in enumerate(row):
                w = widths[i] if i < len(widths) else 0
                cells.append(self._pad_cell(str(cell), w))
            
            # 补齐空列
            while len(cells) < len(widths):
                cells.append(' ' * widths[len(cells)])
            
            if self.border:
                lines.append('|' + '|'.join(cells) + '|')
            else:
                lines.append(' '.join(cells))
        
        # 底部边框
        if self.border:
            border_line = '+' + '+'.join('-' * w for w in widths) + '+'
            if self.border_style:
                border_line = self.border_style.text(border_line).render()
            lines.append(border_line)
        
        return '\n'.join(lines)
    
    def __str__(self) -> str:
        return self.render()


def strip_ansi(text: str) -> str:
    """移除文本中的所有 ANSI 转义序列"""
    result = []
    i = 0
    while i < len(text):
        if text[i] == '\033':
            # CSI 序列: ESC [ ... letter
            if i + 1 < len(text) and text[i + 1] == '[':
                i += 2
                while i < len(text) and not text[i].isalpha():
                    i += 1
                i += 1
            # OSC 序列: ESC ] ... BEL/ST
            elif i + 1 < len(text) and text[i + 1] == ']':
                i += 2
                while i < len(text) and text[i] not in ('\x07', '\033'):
                    i += 1
                if i < len(text) and text[i] == '\033':
                    i += 1
                    if i < len(text) and text[i] == '\\':
                        i += 1
                else:
                    i += 1
            else:
                result.append(text[i])
                i += 1
        else:
            result.append(text[i])
            i += 1
    return ''.join(result)


def colorize(text: str, fg: Union[str, int, Tuple[int, int, int]] = None,
             bg: Union[str, int, Tuple[int, int, int]] = None,
             bold: bool = False, italic: bool = False,
             underline: bool = False) -> str:
    """快速应用颜色和样式到文本
    
    Args:
        text: 要着色的文本
        fg: 前景色
        bg: 背景色
        bold: 是否粗体
        italic: 是否斜体
        underline: 是否下划线
    
    Returns:
        着色后的文本
    """
    if not _COLOR_SUPPORT:
        return text
    
    styles = []
    if bold:
        styles.append(ANSI.BOLD)
    if italic:
        styles.append(ANSI.ITALIC)
    if underline:
        styles.append(ANSI.UNDERLINE)
    if fg is not None:
        styles.append(ANSI.fg(fg))
    if bg is not None:
        styles.append(ANSI.bg(bg))
    
    if not styles:
        return text
    
    return f'{"".join(styles)}{text}{ANSI.RESET}'


def rainbow(text: str) -> str:
    """将文本转换为彩虹色"""
    if not _COLOR_SUPPORT:
        return text
    
    colors = [196, 202, 208, 214, 226, 190, 154, 118, 82, 46,
              47, 48, 49, 51, 45, 39, 33, 27, 21, 57,
              93, 129, 165, 201, 200, 199, 198, 197]
    
    result = []
    for i, char in enumerate(text):
        if char == ' ':
            result.append(char)
        else:
            color = colors[i % len(colors)]
            result.append(f'{ANSI.fg(color)}{char}{ANSI.RESET}')
    
    return ''.join(result)


def gradient(text: str, start_color: Tuple[int, int, int],
            end_color: Tuple[int, int, int]) -> str:
    """创建渐变色文本
    
    Args:
        text: 文本
        start_color: 起始 RGB 颜色
        end_color: 结束 RGB 颜色
    
    Returns:
        渐变色文本
    """
    if not _COLOR_SUPPORT or not text:
        return text
    
    # 过滤空格
    visible_chars = [c for c in text if c != ' ']
    if not visible_chars:
        return text
    
    result = []
    visible_idx = 0
    visible_count = len(visible_chars)
    
    for char in text:
        if char == ' ':
            result.append(char)
        else:
            # 计算当前位置的颜色
            t = visible_idx / (visible_count - 1) if visible_count > 1 else 0
            r = int(start_color[0] + (end_color[0] - start_color[0]) * t)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * t)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * t)
            
            result.append(f'{ANSI.fg((r, g, b))}{char}{ANSI.RESET}')
            visible_idx += 1
    
    return ''.join(result)


# 便捷函数别名
def red(text: str) -> str:
    return colorize(text, fg='red')

def green(text: str) -> str:
    return colorize(text, fg='green')

def yellow(text: str) -> str:
    return colorize(text, fg='yellow')

def blue(text: str) -> str:
    return colorize(text, fg='blue')

def magenta(text: str) -> str:
    return colorize(text, fg='magenta')

def cyan(text: str) -> str:
    return colorize(text, fg='cyan')

def white(text: str) -> str:
    return colorize(text, fg='white')

def bright_red(text: str) -> str:
    return colorize(text, fg='bright_red')

def bright_green(text: str) -> str:
    return colorize(text, fg='bright_green')

def bright_yellow(text: str) -> str:
    return colorize(text, fg='bright_yellow')

def bright_blue(text: str) -> str:
    return colorize(text, fg='bright_blue')

def bright_magenta(text: str) -> str:
    return colorize(text, fg='bright_magenta')

def bright_cyan(text: str) -> str:
    return colorize(text, fg='bright_cyan')

def bright_white(text: str) -> str:
    return colorize(text, fg='bright_white')