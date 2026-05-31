#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Terminal Progress Utilities Module

Terminal progress display utilities with zero external dependencies.
Provides progress bars, spinners, tables, and status indicators for CLI applications.

Author: AllToolkit
License: MIT
"""

import sys
import time
import threading
from typing import Optional, Callable, Any, List, Tuple
from enum import Enum


# =============================================================================
# Enums
# =============================================================================

class ProgressStyle(Enum):
    """Progress bar style options"""
    BLOCK = "block"           # ████░░░░░░
    ARROW = "arrow"           #━━━━━━░░░░
    DOTS = "dots"            # ●●●●○○○○○
    BRAILLE = "braille"       # ⣀⣤⣴⣶⣷
    PERCENT = "percent"       # [50%]


class SpinnerStyle(Enum):
    """Spinner animation style options"""
    DOTS = "dots"            # ⠋⠙⠹⠸⠼
    LINE = "line"            # | / - \
    CIRCLE = "circle"        # ◐ ◓ ◑ ◒
    SQUARE = "square"        # ◰ ◳ ◲ ◱


class TableAlign(Enum):
    """Table column alignment"""
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


# =============================================================================
# Constants
# =============================================================================

# Progress bar block characters
BLOCK_CHARS = ["░", "▒", "▓", "█"]
ARROW_CHARS = ["━", "◀"]
DOT_CHARS = ["○", "●"]
BRAILLE_DOTS = ["⠁", "⠉", "⠋", "⠍", "⠎", "⠑", "⠒", "⠓", "⠔", "⠖", "⠘", "⠲", "⠴", "⠶", "⠷", "⣿"]

# Spinner characters
SPINNERS = {
    SpinnerStyle.DOTS: ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
    SpinnerStyle.LINE: ["|", "/", "─", "\\"],
    SpinnerStyle.CIRCLE: ["◐", "◓", "◑", "◒"],
    SpinnerStyle.SQUARE: ["◰", "◳", "◲", "◱"],
}

# Color escape codes (ANSI)
COLOR_RESET = "\033[0m"
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_MAGENTA = "\033[95m"
COLOR_CYAN = "\033[96m"

# Cursor control
CURSOR_UP = "\033[1A"
CURSOR_DOWN = "\033[1B"
CURSOR_CLEAR_LINE = "\033[2K"
CURSOR_HOME = "\r"


# =============================================================================
# Progress Bar
# =============================================================================

class ProgressBar:
    """Terminal progress bar display
    
    Example:
        bar = ProgressBar(total=100, width=40)
        for i in range(100):
            bar.update(i + 1)
            time.sleep(0.05)
        bar.finish()
    """
    
    def __init__(
        self,
        total: int = 100,
        width: int = 40,
        style: ProgressStyle = ProgressStyle.BLOCK,
        prefix: str = "",
        suffix: str = "",
        show_percent: bool = True,
        show_count: bool = True,
        color: Optional[str] = None
    ):
        self.total = max(1, total)
        self.width = max(5, width)
        self.style = style
        self.prefix = prefix
        self.suffix = suffix
        self.show_percent = show_percent
        self.show_count = show_count
        self.color = color or ""
        self.current = 0
        self.start_time = time.time()
        self._displayed = False
    
    def update(self, current: int) -> None:
        """Update progress bar to current value"""
        self.current = max(0, min(current, self.total))
        self._render()
    
    def increment(self, delta: int = 1) -> None:
        """Increment progress by delta"""
        self.update(self.current + delta)
    
    def _render(self) -> None:
        """Render the progress bar to terminal"""
        percent = self.current / self.total
        filled = int(self.width * percent)
        empty = self.width - filled
        
        if self.style == ProgressStyle.BLOCK:
            filled_str = BLOCK_CHARS[3] * filled
            empty_str = BLOCK_CHARS[0] * empty
        elif self.style == ProgressStyle.ARROW:
            filled_str = ARROW_CHARS[0] * (filled - 1) + ARROW_CHARS[1] if filled > 0 else ""
            empty_str = ARROW_CHARS[0] * empty
        elif self.style == ProgressStyle.DOTS:
            filled_str = DOT_CHARS[1] * filled
            empty_str = DOT_CHARS[0] * empty
        elif self.style == ProgressStyle.BRAILLE:
            filled_str = self._braille_progress(filled)
            empty_str = BRAILLE_DOTS[0] * (empty // 2 + 1)
        else:
            filled_str = "█" * filled
            empty_str = "░" * empty
        
        bar = f"[{filled_str}{empty_str}]"
        
        parts = []
        if self.prefix:
            parts.append(self.prefix)
        parts.append(bar)
        
        if self.show_count:
            parts.append(f"{self.current}/{self.total}")
        if self.show_percent:
            parts.append(f"{percent * 100:.1f}%")
        
        if self.suffix:
            parts.append(self.suffix)
        
        line = " ".join(parts)
        if self.color:
            line = f"{self.color}{line}{COLOR_RESET}"
        
        if self._displayed:
            sys.stdout.write(f"{CURSOR_UP}{CURSOR_CLEAR_LINE}")
        sys.stdout.write(line)
        sys.stdout.flush()
        self._displayed = True
    
    def _braille_progress(self, filled: int) -> str:
        """Generate braille-style progress"""
        result = []
        for i in range(0, filled, 2):
            result.append(BRAILLE_DOTS[min(15, i // 2)])
        return "".join(result)
    
    def finish(self, message: str = "Done") -> None:
        """Complete the progress bar"""
        self.current = self.total
        self._render()
        elapsed = time.time() - self.start_time
        sys.stdout.write(f" {message} ({elapsed:.1f}s)\n")
        self._displayed = False


# =============================================================================
# Spinner
# =============================================================================

class Spinner:
    """Terminal spinner animation
    
    Example:
        spinner = Spinner(message="Processing...")
        spinner.start()
        # do work
        spinner.stop()
    """
    
    def __init__(
        self,
        message: str = "Working",
        style: SpinnerStyle = SpinnerStyle.DOTS,
        color: Optional[str] = None
    ):
        self.message = message
        self.style = style
        self.color = color or ""
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._index = 0
        self._displayed = False
    
    def start(self) -> None:
        """Start the spinner animation"""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()
    
    def stop(self, message: Optional[str] = None) -> None:
        """Stop the spinner"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=0.5)
        if message:
            sys.stdout.write(f"{CURSOR_CLEAR_LINE}{message}\n")
        elif self._displayed:
            sys.stdout.write(f"{CURSOR_CLEAR_LINE}")
        self._displayed = False
    
    def _spin(self) -> None:
        """Animation loop"""
        chars = SPINNERS.get(self.style, SPINNERS[SpinnerStyle.DOTS])
        while self._running:
            char = chars[self._index % len(chars)]
            line = f"{self.color}{char} {self.message}{COLOR_RESET}"
            if self._displayed:
                sys.stdout.write(f"{CURSOR_CLEAR_LINE}")
            sys.stdout.write(line)
            sys.stdout.flush()
            self._displayed = True
            self._index += 1
            time.sleep(0.1)
        sys.stdout.write(f"{CURSOR_CLEAR_LINE}")
        sys.stdout.flush()


# =============================================================================
# Status Indicator
# =============================================================================

class StatusIndicator:
    """Text-based status indicator with labels
    
    Example:
        status = StatusIndicator()
        status.show("Loading", "pending")
        time.sleep(1)
        status.show("Processing", "active")
        time.sleep(1)
        status.show("Complete", "success")
    """
    
    STATUS_SYMBOLS = {
        "pending": ("○", COLOR_YELLOW),
        "active": ("●", COLOR_CYAN),
        "success": ("✓", COLOR_GREEN),
        "error": ("✗", COLOR_RED),
        "warning": ("⚠", COLOR_YELLOW),
        "info": ("ℹ", COLOR_BLUE),
    }
    
    def __init__(self, width: int = 60):
        self.width = max(20, width)
        self.last_line = ""
    
    def show(self, label: str, status: str = "pending") -> None:
        """Display status line"""
        symbol, color = self.STATUS_SYMBOLS.get(status, ("●", COLOR_RESET))
        display_label = label[:self.width - 10]
        line = f"{color}{symbol}{COLOR_RESET} {display_label}"
        if len(line) < self.width:
            line = line + " " * (self.width - len(line))
        if self.last_line:
            sys.stdout.write(f"{CURSOR_UP}{CURSOR_CLEAR_LINE}")
        sys.stdout.write(line)
        sys.stdout.flush()
        self.last_line = line


# =============================================================================
# Table Display
# =============================================================================

class Table:
    """Terminal table display
    
    Example:
        table = Table(headers=["Name", "Age", "City"])
        table.add_row(["Alice", "30", "NYC"])
        table.add_row(["Bob", "25", "LA"])
        print(table.render())
    """
    
    def __init__(
        self,
        headers: Optional[List[str]] = None,
        alignments: Optional[List[TableAlign]] = None,
        border: bool = True
    ):
        self.headers = headers or []
        self.rows: List[List[str]] = []
        self.alignments = alignments or []
        self.border = border
        self._col_widths: Optional[List[int]] = None
    
    def add_row(self, row: List[str]) -> None:
        """Add a row to the table"""
        self.rows.append([str(cell) for cell in row])
    
    def set_col_widths(self, widths: List[int]) -> None:
        """Manually set column widths"""
        self._col_widths = widths
    
    def render(self) -> str:
        """Render table as string"""
        if not self.headers and not self.rows:
            return ""
        
        all_rows = [self.headers] + self.rows if self.headers else self.rows
        
        # Calculate column widths
        if self._col_widths:
            col_widths = self._col_widths
        else:
            col_widths = [max(len(str(row[i])) for row in all_rows if i < len(row)) 
                         for i in range(max(len(r) for r in all_rows))]
        
        # Pad headers to center
        padded_headers = []
        for i, h in enumerate(self.headers):
            w = col_widths[i] if i < len(col_widths) else len(h)
            padded_headers.append(h.center(w))
        
        lines = []
        
        if self.border:
            sep = "┌" + "┬".join("─" * w for w in col_widths) + "┐"
            lines.append(sep)
        
        if self.headers:
            lines.append("│" + "│".join(padded_headers) + "│")
        
        if self.border and self.headers:
            mid_sep = "├" + "┼".join("─" * w for w in col_widths) + "┤"
            lines.append(mid_sep)
        
        for row in self.rows:
            cells = []
            for i, cell in enumerate(row):
                w = col_widths[i] if i < len(col_widths) else len(str(cell))
                align = self.alignments[i] if i < len(self.alignments) else TableAlign.LEFT
                if align == TableAlign.RIGHT:
                    cells.append(str(cell).rjust(w))
                elif align == TableAlign.CENTER:
                    cells.append(str(cell).center(w))
                else:
                    cells.append(str(cell).ljust(w))
            lines.append("│" + "│".join(cells) + "│")
        
        if self.border:
            lines.append("└" + "┴".join("─" * w for w in col_widths) + "┘")
        
        return "\n".join(lines)


# =============================================================================
# Multi-Step Progress
# =============================================================================

class MultiStepProgress:
    """Multi-step progress tracker with phases
    
    Example:
        steps = MultiStepProgress(["Download", "Extract", "Install", "Configure"])
        steps.start()
        for i in range(100):
            steps.update(0, i)  # update step 0 progress
            time.sleep(0.1)
        steps.next_step()
        for i in range(100):
            steps.update(1, i)  # update step 1 progress
            time.sleep(0.1)
        steps.finish("Installation complete!")
    """
    
    def __init__(self, step_names: List[str], width: int = 30):
        self.step_names = step_names
        self.width = width
        self.current_step = 0
        self.step_progress = [0] * len(step_names)
        self.start_time = time.time()
        self._displayed = False
    
    def start(self) -> None:
        """Start the multi-step progress"""
        self._render()
    
    def update(self, step: int, progress: int) -> None:
        """Update a specific step's progress"""
        if 0 <= step < len(self.step_names):
            self.step_progress[step] = max(0, min(100, progress))
            self._render()
    
    def next_step(self) -> None:
        """Move to the next step"""
        if self.current_step < len(self.step_names) - 1:
            self.step_progress[self.current_step] = 100
            self.current_step += 1
            self._render()
    
    def _render(self) -> None:
        """Render all steps"""
        lines = []
        for i, (name, prog) in enumerate(zip(self.step_names, self.step_progress)):
            filled = int(self.width * prog / 100)
            empty = self.width - filled
            prefix = "►" if i == self.current_step else " "
            bar = f"[{'█' * filled}{'░' * empty}]"
            label = f"{name} {prog:3d}%"
            lines.append(f"{prefix} {bar} {label}")
        
        lines.append(f"Step {self.current_step + 1}/{len(self.step_names)}")
        
        output = "\n".join(lines)
        if self._displayed:
            sys.stdout.write("\033[" + str(len(lines)) + "A")
        sys.stdout.write(output)
        sys.stdout.flush()
        self._displayed = True
    
    def finish(self, message: str = "Complete") -> None:
        """Finish the multi-step progress"""
        self.step_progress = [100] * len(self.step_names)
        elapsed = time.time() - self.start_time
        sys.stdout.write(f"\n{message} ({elapsed:.1f}s)\n")
        self._displayed = False


# =============================================================================
# Live Value Display
# =============================================================================

class LiveValue:
    """Live updating value display for terminal
    
    Example:
        live = LiveValue()
        for i in range(100):
            live.update(f"Processing: {i}%", i)
            time.sleep(0.1)
    """
    
    def __init__(self, prefix: str = "", suffix: str = ""):
        self.prefix = prefix
        self.suffix = suffix
        self.last_len = 0
    
    def update(self, label: str, value: Any = None) -> None:
        """Update the live display"""
        if value is not None:
            text = f"{self.prefix}{label}: {value}{self.suffix}"
        else:
            text = f"{self.prefix}{label}{self.suffix}"
        
        padding = max(0, self.last_len - len(text))
        if self.last_len:
            sys.stdout.write(f"{CURSOR_CLEAR_LINE}")
        sys.stdout.write(text + " " * padding)
        sys.stdout.flush()
        self.last_len = len(text)
    
    def clear(self) -> None:
        """Clear the live display"""
        if self.last_len:
            sys.stdout.write(f"{CURSOR_CLEAR_LINE}")
            sys.stdout.flush()
            self.last_len = 0


# =============================================================================
# Counter
# =============================================================================

class Counter:
    """Animated counter for terminal
    
    Example:
        counter = Counter()
        for i in range(1000):
            counter.show(i)
            time.sleep(0.01)
    """
    
    def __init__(self, prefix: str = "", suffix: str = "", decimals: int = 0):
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.last_len = 0
    
    def show(self, value: float) -> None:
        """Display current count"""
        if self.decimals > 0:
            text = f"{self.prefix}{value:.{self.decimals}f}{self.suffix}"
        else:
            text = f"{self.prefix}{int(value)}{self.suffix}"
        
        padding = max(0, self.last_len - len(text))
        sys.stdout.write(f"{CURSOR_CLEAR_LINE}{text}{' ' * padding}")
        sys.stdout.flush()
        self.last_len = len(text)


# =============================================================================
# Utility Functions
# =============================================================================

def progress_bar(
    current: int,
    total: int,
    width: int = 40,
    style: ProgressStyle = ProgressStyle.BLOCK,
    prefix: str = "",
    color: Optional[str] = None
) -> str:
    """Simple progress bar string generator
    
    Args:
        current: Current progress value
        total: Total value
        width: Bar width in characters
        style: Bar style
        prefix: Text prefix
        color: ANSI color code
    
    Returns:
        Formatted progress bar string
    
    Example:
        >>> print(progress_bar(50, 100))
        [████████████░░░░░░░░░░░░░] 50.0%
    """
    percent = current / max(1, total)
    filled = int(width * percent)
    empty = width - filled
    
    if style == ProgressStyle.BLOCK:
        filled_str = "█" * filled
        empty_str = "░" * empty
    elif style == ProgressStyle.ARROW:
        filled_str = "━" * (filled - 1) + "◀" if filled > 0 else ""
        empty_str = "━" * empty
    elif style == ProgressStyle.DOTS:
        filled_str = "●" * filled
        empty_str = "○" * empty
    else:
        filled_str = "█" * filled
        empty_str = "░" * empty
    
    bar = f"[{filled_str}{empty_str}]"
    text = f"{prefix}{bar} {percent * 100:.1f}%" if prefix else f"{bar} {percent * 100:.1f}%"
    
    if color:
        return f"{color}{text}{COLOR_RESET}"
    return text


def loading_spinner(message: str = "Loading", style: SpinnerStyle = SpinnerStyle.DOTS) -> str:
    """Generate spinner character (for custom animation)
    
    Args:
        message: Message to display
        style: Spinner style
    
    Returns:
        Spinner frame string
    
    Example:
        >>> for _ in range(10):
        ...     print(loading_spinner(), end="\r")
        ...     time.sleep(0.1)
    """
    chars = SPINNERS.get(style, SPINNERS[SpinnerStyle.DOTS])
    idx = int(time.time() * 10) % len(chars)
    return f"{chars[idx]} {message}"


def status_bar(
    label: str,
    status: str = "pending",
    width: int = 60,
    icon: Optional[str] = None
) -> str:
    """Generate a status bar line
    
    Args:
        label: Status label
        status: Status type (pending/active/success/error/warning/info)
        width: Total width
        icon: Custom icon (overrides default)
    
    Returns:
        Formatted status bar string
    
    Example:
        >>> print(status_bar("Installation complete", "success"))
    """
    symbols = {
        "pending": icon or "○",
        "active": icon or "●",
        "success": icon or "✓",
        "error": icon or "✗",
        "warning": icon or "⚠",
        "info": icon or "ℹ",
    }
    
    colors = {
        "pending": COLOR_YELLOW,
        "active": COLOR_CYAN,
        "success": COLOR_GREEN,
        "error": COLOR_RED,
        "warning": COLOR_YELLOW,
        "info": COLOR_BLUE,
    }
    
    symbol = symbols.get(status, "●")
    color = colors.get(status, COLOR_RESET)
    display_label = label[:width - 5]
    
    return f"{color}{symbol}{COLOR_RESET} {display_label}"


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    # Enums
    "ProgressStyle",
    "SpinnerStyle", 
    "TableAlign",
    # Classes
    "ProgressBar",
    "Spinner",
    "StatusIndicator",
    "Table",
    "MultiStepProgress",
    "LiveValue",
    "Counter",
    # Functions
    "progress_bar",
    "loading_spinner",
    "status_bar",
    # Constants
    "BLOCK_CHARS",
    "ARROW_CHARS",
    "DOT_CHARS",
    "BRAILLE_DOTS",
    "SPINNERS",
]