#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Sparkline Utilities Module

Text-based mini chart utilities for terminal visualization with zero external dependencies.
Provides sparklines, mini bar charts, trend indicators, and more for command-line applications.

Author: AllToolkit
License: MIT
"""

import math
from typing import List, Optional, Tuple, Union, Sequence
from enum import Enum


# =============================================================================
# Type Aliases
# =============================================================================

Number = Union[int, float]
DataSequence = Sequence[Number]


# =============================================================================
# Constants
# =============================================================================

# Unicode block characters for sparklines (8 levels)
SPARKLINE_CHARS = ' ▁▂▃▄▅▆▇█'

# Vertical block characters (8 levels)
VERTICAL_BLOCKS = [' ', '▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']

# Horizontal block characters
HORIZONTAL_BLOCKS = [' ', '▏', '▎', '▍', '▌', '▋', '▊', '▉', '█']

# Braille patterns for 2x4 dots (256 patterns)
# Each pattern represents a 2-wide x 4-tall grid
BRAILLE_BASE = 0x2800  # Unicode Braille block start

# Arrow characters for trend indicators
TREND_UP = '↑'
TREND_DOWN = '↓'
TREND_FLAT = '→'
TREND_UP_STRONG = '⬆'
TREND_DOWN_STRONG = '⬇'

# Box drawing characters
BOX_LIGHT = {'h': '─', 'v': '│', 'tl': '┌', 'tr': '┐', 'bl': '└', 'br': '┘'}
BOX_HEAVY = {'h': '━', 'v': '┃', 'tl': '┏', 'tr': '┓', 'bl': '┗', 'br': '┛'}
BOX_DOUBLE = {'h': '═', 'v': '║', 'tl': '╔', 'tr': '╗', 'bl': '╚', 'br': '╝'}

# ASCII fallback characters
ASCII_SPARKLINE = [' ', '.', ':', '|', '+', '*', '#', '@', '█']
ASCII_BAR = [' ', '.', ':', '=', '#', '%', '&', '@', 'W']


class SparklineStyle(Enum):
    """Sparkline rendering styles."""
    UNICODE = 'unicode'      # Unicode block characters
    BRAILLE = 'braille'      # Braille patterns (higher resolution)
    ASCII = 'ascii'           # ASCII fallback
    BAR = 'bar'               # Vertical bars
    DOT = 'dot'               # Dot matrix


# =============================================================================
# Core Sparkline Functions
# =============================================================================

def sparkline(
    data: DataSequence,
    width: Optional[int] = None,
    style: SparklineStyle = SparklineStyle.UNICODE,
    min_val: Optional[Number] = None,
    max_val: Optional[Number] = None
) -> str:
    """
    Generate a one-line sparkline from numeric data.
    
    Args:
        data: Sequence of numeric values
        width: Maximum width in characters (default: len(data))
        style: Rendering style (unicode, braille, ascii)
        min_val: Minimum value for scaling (default: min(data))
        max_val: Maximum value for scaling (default: max(data))
    
    Returns:
        Sparkline string
    
    Examples:
        >>> sparkline([1, 2, 3, 4, 5, 6, 7, 8])
        '▁▂▃▄▅▆▇█'
        >>> sparkline([1, 5, 22, 13, 53], style=SparklineStyle.ASCII)
        '.:|*@'
    """
    if not data:
        return ''
    
    data = list(data)
    
    # Handle width scaling
    if width is not None and len(data) > width:
        data = _resample(data, width)
    
    # Calculate min/max for scaling
    data_min = min_val if min_val is not None else min(data)
    data_max = max_val if max_val is not None else max(data)
    
    # Handle constant data
    if data_max == data_min:
        data_max = data_min + 1
    
    # Scale data to 0-8 range (for 8-level sparkline chars)
    scaled = [_scale_value(v, data_min, data_max, 0, 8) for v in data]
    
    if style == SparklineStyle.UNICODE:
        return ''.join(SPARKLINE_CHARS[max(0, min(8, int(round(v))))] for v in scaled)
    elif style == SparklineStyle.ASCII:
        return ''.join(ASCII_SPARKLINE[max(0, min(8, int(round(v))))] for v in scaled)
    elif style == SparklineStyle.BAR:
        return ''.join(VERTICAL_BLOCKS[max(0, min(8, int(round(v))))] for v in scaled)
    else:
        return ''.join(SPARKLINE_CHARS[max(0, min(8, int(round(v))))] for v in scaled)


def sparkline_braille(
    data: DataSequence,
    width: Optional[int] = None,
    height: int = 4,
    min_val: Optional[Number] = None,
    max_val: Optional[Number] = None
) -> str:
    """
    Generate a high-resolution sparkline using Braille patterns.
    Braille patterns provide 2x4 dot resolution per character.
    
    Args:
        data: Sequence of numeric values
        width: Maximum width in Braille cells (default: auto)
        height: Height in dot rows (1-4, default: 4)
        min_val: Minimum value for scaling
        max_val: Maximum value for scaling
    
    Returns:
        Braille sparkline string
    
    Examples:
        >>> sparkline_braille([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        '⡇⣤⣶⣾⣿'
    """
    if not data:
        return ''
    
    data = list(data)
    height = max(1, min(4, height))
    
    # Calculate scaling
    data_min = min_val if min_val is not None else min(data)
    data_max = max_val if max_val is not None else max(data)
    
    if data_max == data_min:
        data_max = data_min + 1
    
    # Resample if width specified
    if width is not None:
        # Each Braille cell is 2 dots wide
        target_dots = width * 2
        if len(data) > target_dots:
            data = _resample(data, target_dots)
    
    # Scale to height levels (4 max)
    scaled = [_scale_value(v, data_min, data_max, 0, height) for v in data]
    
    # Convert to Braille
    result = []
    for i in range(0, len(scaled), 2):
        # Each Braille cell covers 2 data points
        v1 = scaled[i] if i < len(scaled) else 0
        v2 = scaled[i + 1] if i + 1 < len(scaled) else 0
        
        # Build Braille pattern
        pattern = _braille_pattern_from_values(v1, v2, height)
        result.append(chr(BRAILLE_BASE + pattern))
    
    return ''.join(result)


def sparkline_multiline(
    data: DataSequence,
    width: int = 40,
    height: int = 4,
    style: SparklineStyle = SparklineStyle.UNICODE,
    min_val: Optional[Number] = None,
    max_val: Optional[Number] = None,
    show_axis: bool = True
) -> str:
    """
    Generate a multi-line sparkline chart with optional axis.
    
    Args:
        data: Sequence of numeric values
        width: Width in characters
        height: Height in lines
        style: Rendering style
        min_val: Minimum value for scaling
        max_val: Maximum value for scaling
        show_axis: Whether to show Y-axis labels
    
    Returns:
        Multi-line sparkline chart string
    
    Examples:
        >>> print(sparkline_multiline([1,2,3,5,8,13,21,34,55,89], width=20, height=3))
        89 ┤  ▄▆█
        45 ┤ ▃▅▇
         1 ┤█▁▂▄
    """
    if not data:
        return ''
    
    data = list(data)
    
    # Calculate min/max
    data_min = min_val if min_val is not None else min(data)
    data_max = max_val if max_val is not None else max(data)
    
    if data_max == data_min:
        data_max = data_min + 1
    
    # Resample data to fit width
    if len(data) > width:
        resampled = _resample(data, width)
    else:
        resampled = data
    
    # Create 2D grid for the chart
    grid = [[' ' for _ in range(len(resampled))] for _ in range(height)]
    
    for col, value in enumerate(resampled):
        # Scale value to height
        scaled = _scale_value(value, data_min, data_max, 0, height)
        # Fill from bottom up
        for row in range(height):
            row_from_bottom = height - 1 - row
            if row_from_bottom < scaled:
                grid[row][col] = '█'
    
    # Build output lines
    lines = []
    chars = SPARKLINE_CHARS if style == SparklineStyle.UNICODE else ASCII_SPARKLINE
    
    # Calculate axis label positions
    axis_width = max(len(_format_number(data_max)), len(_format_number(data_min))) + 2
    
    for row_idx, row in enumerate(grid):
        if show_axis:
            # Calculate Y value for this row
            y_frac = (height - 1 - row_idx) / (height - 1) if height > 1 else 0.5
            y_val = data_min + y_frac * (data_max - data_min)
            
            # Show label for top, middle, and bottom rows
            if row_idx == 0 or row_idx == height - 1 or row_idx == height // 2:
                label = _format_number(y_val).rjust(axis_width - 2)
                line = f"{label} ┤"
            else:
                line = ' ' * (axis_width - 2) + ' ┤'
            
            # Add the chart data
            line += ''.join(chars[max(0, min(8, int(round(_scale_value(v, data_min, data_max, 0, 8)))))] 
                          if v > data_min else ' ' for v in resampled)
        else:
            line = ''.join(row)
        
        lines.append(line)
    
    return '\n'.join(lines)


# =============================================================================
# Bar Chart Functions
# =============================================================================

def bar_chart(
    data: DataSequence,
    width: int = 20,
    height: int = 10,
    title: Optional[str] = None,
    labels: Optional[List[str]] = None,
    min_val: Optional[Number] = None,
    max_val: Optional[Number] = None
) -> str:
    """
    Generate a vertical bar chart.
    
    Args:
        data: Sequence of numeric values
        width: Maximum width in characters
        height: Height in lines
        title: Optional chart title
        labels: Optional labels for each bar
        min_val: Minimum value for Y-axis
        max_val: Maximum value for Y-axis
    
    Returns:
        Bar chart string
    
    Examples:
        >>> print(bar_chart([3, 7, 2, 5, 9], labels=['A','B','C','D','E']))
        9.0 ┤  █
        7.5 ┤  █ █
        6.0 ┤  █ █ █
        4.5 ┤█ █ █ █
        3.0 ┤█ █ █ █
        1.5 ┤█ █▂█ █
            └────────
              A B C D E
    """
    if not data:
        return ''
    
    data = list(data)
    
    # Calculate min/max
    data_min = min_val if min_val is not None else 0
    data_max = max_val if max_val is not None else max(data)
    
    if data_max == data_min:
        data_max = data_min + 1
    
    # Calculate bar width and spacing
    bar_width = 1
    spacing = 1
    
    # Build grid
    grid = [[' ' for _ in range(len(data) * (bar_width + spacing))] for _ in range(height)]
    
    for i, value in enumerate(data):
        # Scale to height
        scaled = _scale_value(value, data_min, data_max, 0, height)
        col = i * (bar_width + spacing)
        
        for h in range(height):
            row = height - 1 - h
            if h < scaled:
                grid[row][col] = '█'
    
    # Build output
    lines = []
    
    if title:
        lines.append(title.center(len(data) * (bar_width + spacing)))
    
    # Y-axis labels
    axis_width = len(_format_number(data_max)) + 1
    
    for row_idx, row in enumerate(grid):
        y_frac = (height - 1 - row_idx) / (height - 1) if height > 1 else 0.5
        y_val = data_min + y_frac * (data_max - data_min)
        
        # Show label for top, middle, bottom
        if row_idx == 0 or row_idx == height - 1 or row_idx == height // 2:
            label = _format_number(y_val).rjust(axis_width)
            line = f"{label} ┤"
        else:
            line = ' ' * axis_width + ' ┤'
        
        line += ''.join(row)
        lines.append(line)
    
    # X-axis
    lines.append(' ' * axis_width + ' └' + '─' * (len(data) * (bar_width + spacing) - 1))
    
    # Labels
    if labels:
        label_line = ' ' * (axis_width + 2)
        for i, label in enumerate(labels[:len(data)]):
            label_line += label[:bar_width].ljust(bar_width + spacing)
        lines.append(label_line)
    
    return '\n'.join(lines)


def horizontal_bar_chart(
    labels: List[str],
    data: DataSequence,
    width: int = 30,
    title: Optional[str] = None,
    show_values: bool = True
) -> str:
    """
    Generate a horizontal bar chart.
    
    Args:
        labels: Labels for each bar
        data: Sequence of numeric values
        width: Maximum bar width in characters
        title: Optional chart title
        show_values: Whether to show values at the end of bars
    
    Returns:
        Horizontal bar chart string
    
    Examples:
        >>> print(horizontal_bar_chart(['A', 'B', 'C'], [30, 50, 20]))
        A ██████████████ 30
        B ████████████████████████ 50
        C █████████ 20
    """
    if not data or not labels:
        return ''
    
    data = list(data)[:len(labels)]
    labels = labels[:len(data)]
    
    # Calculate scaling
    max_val = max(data) if data else 1
    if max_val == 0:
        max_val = 1
    
    # Calculate label width
    label_width = max(len(str(l)) for l in labels) + 1
    
    # Build bars
    lines = []
    
    if title:
        lines.append(title)
        lines.append('')
    
    for label, value in zip(labels, data):
        bar_length = int(_scale_value(value, 0, max_val, 0, width))
        bar = '█' * bar_length
        
        if show_values:
            line = f"{str(label).ljust(label_width)} {bar} {value}"
        else:
            line = f"{str(label).ljust(label_width)} {bar}"
        
        lines.append(line)
    
    return '\n'.join(lines)


# =============================================================================
# Trend and Indicator Functions
# =============================================================================

def trend_indicator(
    data: DataSequence,
    threshold: Number = 0.05
) -> str:
    """
    Generate a trend indicator arrow based on data trend.
    
    Args:
        data: Sequence of numeric values (at least 2 points)
        threshold: Minimum relative change to show strong trend
    
    Returns:
        Trend indicator character
    
    Examples:
        >>> trend_indicator([1, 2, 3, 4, 5])
        '↑'
        >>> trend_indicator([5, 4, 3, 2, 1])
        '↓'
    """
    if len(data) < 2:
        return TREND_FLAT
    
    first = data[0]
    last = data[-1]
    
    if first == 0:
        if last > 0:
            return TREND_UP
        elif last < 0:
            return TREND_DOWN
        return TREND_FLAT
    
    relative_change = abs(last - first) / abs(first)
    
    if last > first:
        if relative_change > threshold:
            return TREND_UP_STRONG
        return TREND_UP
    elif last < first:
        if relative_change > threshold:
            return TREND_DOWN_STRONG
        return TREND_DOWN
    
    return TREND_FLAT


def trend_sparkline(
    data: DataSequence,
    width: int = 10,
    show_value: bool = True,
    show_arrow: bool = True
) -> str:
    """
    Generate a sparkline with trend indicator.
    
    Args:
        data: Sequence of numeric values
        width: Sparkline width
        show_value: Whether to show the last value
        show_arrow: Whether to show trend arrow
    
    Returns:
        Sparkline with trend indicator
    
    Examples:
        >>> trend_sparkline([1, 2, 3, 4, 5])
        '▁▂▃▄▅ 5 ↑'
    """
    if not data:
        return ''
    
    line = sparkline(data, width=width)
    
    if show_value:
        line += f" {data[-1]}"
    
    if show_arrow:
        line += f" {trend_indicator(data)}"
    
    return line


def delta_indicator(
    old_value: Number,
    new_value: Number,
    show_percent: bool = True,
    show_value: bool = True
) -> str:
    """
    Generate a delta change indicator.
    
    Args:
        old_value: Original value
        new_value: New value
        show_percent: Whether to show percentage change
        show_value: Whether to show absolute change
    
    Returns:
        Delta indicator string
    
    Examples:
        >>> delta_indicator(100, 110)
        '+10 (+10.0%) ↑'
    """
    delta = new_value - old_value
    
    parts = []
    
    if show_value:
        sign = '+' if delta >= 0 else ''
        parts.append(f"{sign}{delta}")
    
    if show_percent and old_value != 0:
        percent = (delta / old_value) * 100
        sign = '+' if percent >= 0 else ''
        parts.append(f"({sign}{percent:.1f}%)")
    
    # Add trend arrow
    if delta > 0:
        parts.append(TREND_UP)
    elif delta < 0:
        parts.append(TREND_DOWN)
    else:
        parts.append(TREND_FLAT)
    
    return ' '.join(parts)


# =============================================================================
# Specialized Sparklines
# =============================================================================

def win_loss_sparkline(
    data: Sequence[int],
    win_char: str = '█',
    loss_char: str = '▄',
    draw_char: str = '─'
) -> str:
    """
    Generate a win/loss sparkline.
    
    Args:
        data: Sequence of 1 (win), 0 (draw), -1 (loss)
        win_char: Character for wins
        loss_char: Character for losses
        draw_char: Character for draws
    
    Returns:
        Win/loss sparkline string
    
    Examples:
        >>> win_loss_sparkline([1, 1, -1, 0, 1, -1])
        '██▄─█▄'
    """
    result = []
    for v in data:
        if v > 0:
            result.append(win_char)
        elif v < 0:
            result.append(loss_char)
        else:
            result.append(draw_char)
    return ''.join(result)


def gauge(
    value: Number,
    max_value: Number = 100,
    width: int = 10,
    filled_char: str = '█',
    empty_char: str = '░'
) -> str:
    """
    Generate a horizontal gauge/bar.
    
    Args:
        value: Current value
        max_value: Maximum value
        width: Width in characters
        filled_char: Character for filled portion
        empty_char: Character for empty portion
    
    Returns:
        Gauge string
    
    Examples:
        >>> gauge(75, 100, 10)
        '███████░░░'
    """
    if max_value == 0:
        return empty_char * width
    
    filled = int(_scale_value(value, 0, max_value, 0, width))
    filled = max(0, min(width, filled))
    
    return filled_char * filled + empty_char * (width - filled)


def gauge_with_value(
    value: Number,
    max_value: Number = 100,
    width: int = 20,
    show_percent: bool = True,
    show_value: bool = False
) -> str:
    """
    Generate a gauge with value display.
    
    Args:
        value: Current value
        max_value: Maximum value
        width: Width in characters
        show_percent: Whether to show percentage
        show_value: Whether to show actual value
    
    Returns:
        Gauge string with value
    
    Examples:
        >>> gauge_with_value(75, 100, 10)
        '[███████░░░] 75%'
    """
    bar = gauge(value, max_value, width)
    
    parts = [f'[{bar}]']
    
    if show_percent:
        percent = (value / max_value * 100) if max_value else 0
        parts.append(f'{percent:.0f}%')
    
    if show_value:
        parts.append(f'({value}/{max_value})')
    
    return ' '.join(parts)


# =============================================================================
# Histogram Functions
# =============================================================================

def histogram(
    data: DataSequence,
    bins: int = 10,
    width: int = 40,
    height: int = 10,
    show_counts: bool = True
) -> str:
    """
    Generate a histogram from numeric data.
    
    Args:
        data: Sequence of numeric values
        bins: Number of histogram bins
        width: Width in characters
        height: Height in lines
        show_counts: Whether to show count labels
    
    Returns:
        Histogram string
    
    Examples:
        >>> print(histogram([1,1,2,2,2,3,3,4,5,5,5,5], bins=5, width=20))
        4 ┤    █
        3 ┤    █ █
        2 ┤  █ █ █
        1 ┤█ █ █ █ █
          └──────────
            1 2 3 4 5
    """
    if not data:
        return ''
    
    data = list(data)
    
    # Calculate bin edges
    data_min = min(data)
    data_max = max(data)
    
    if data_max == data_min:
        data_max = data_min + bins
    
    bin_width = (data_max - data_min) / bins
    counts = [0] * bins
    
    for value in data:
        bin_idx = int((value - data_min) / bin_width)
        bin_idx = max(0, min(bins - 1, bin_idx))
        counts[bin_idx] += 1
    
    # Create bar chart for counts
    max_count = max(counts) if counts else 1
    
    # Build grid
    grid = [[' ' for _ in range(bins * 2)] for _ in range(height)]
    
    for i, count in enumerate(counts):
        scaled = _scale_value(count, 0, max_count, 0, height)
        col = i * 2
        for h in range(height):
            row = height - 1 - h
            if h < scaled:
                grid[row][col] = '█'
    
    # Build output
    lines = []
    axis_width = len(str(max_count)) + 1
    
    for row_idx, row in enumerate(grid):
        y_frac = (height - 1 - row_idx) / (height - 1) if height > 1 else 0.5
        y_val = max_count * y_frac
        
        if row_idx == 0 or row_idx == height - 1 or row_idx == height // 2:
            label = str(int(y_val)).rjust(axis_width)
            line = f"{label} ┤"
        else:
            line = ' ' * axis_width + ' ┤'
        
        line += ''.join(row)
        lines.append(line)
    
    # X-axis
    lines.append(' ' * axis_width + ' └' + '─' * (bins * 2 - 1))
    
    # X-axis labels
    x_labels = []
    for i in range(bins):
        bin_val = data_min + i * bin_width + bin_width / 2
        x_labels.append(f"{bin_val:.0f}")
    
    label_line = ' ' * (axis_width + 2)
    label_line += ' '.join(l.rjust(2)[:2] for l in x_labels)
    lines.append(label_line)
    
    return '\n'.join(lines)


# =============================================================================
# Utility Functions
# =============================================================================

def _scale_value(
    value: Number,
    from_min: Number,
    from_max: Number,
    to_min: Number,
    to_max: Number
) -> float:
    """Scale a value from one range to another."""
    if from_max == from_min:
        return to_min + (to_max - to_min) / 2
    
    ratio = (value - from_min) / (from_max - from_min)
    return to_min + ratio * (to_max - to_min)


def _resample(data: List[Number], target_length: int) -> List[Number]:
    """Resample data to target length using linear interpolation."""
    if target_length <= 0 or not data:
        return []
    
    if len(data) == target_length:
        return data
    
    result = []
    for i in range(target_length):
        # Calculate position in original data
        pos = i * (len(data) - 1) / (target_length - 1) if target_length > 1 else 0
        
        # Linear interpolation
        idx = int(pos)
        frac = pos - idx
        
        if idx >= len(data) - 1:
            result.append(data[-1])
        else:
            interpolated = data[idx] * (1 - frac) + data[idx + 1] * frac
            result.append(interpolated)
    
    return result


def _braille_pattern_from_values(v1: Number, v2: Number, height: int) -> int:
    """
    Convert two values to a Braille pattern.
    Each Braille cell has 2 columns × 4 rows of dots.
    """
    # Braille dot positions (in order of Unicode bit positions):
    # 0x01  0x08    ⠁ ⠉
    # 0x02  0x10    ⠂ ⠙
    # 0x04  0x20    ⠄ ⠑
    # 0x40  0x80    ⠤ ⠭
    
    pattern = 0
    
    # Column 1 (left dots)
    h1 = int(min(height, max(0, v1)))
    if h1 >= 1:
        pattern |= 0x01
    if h1 >= 2:
        pattern |= 0x02
    if h1 >= 3:
        pattern |= 0x04
    if h1 >= 4:
        pattern |= 0x40
    
    # Column 2 (right dots)
    h2 = int(min(height, max(0, v2)))
    if h2 >= 1:
        pattern |= 0x08
    if h2 >= 2:
        pattern |= 0x10
    if h2 >= 3:
        pattern |= 0x20
    if h2 >= 4:
        pattern |= 0x80
    
    return pattern


def _format_number(value: Number, decimals: int = 1) -> str:
    """Format a number for display, with smart decimal handling."""
    if isinstance(value, float):
        if value == int(value):
            return str(int(value))
        return f"{value:.{decimals}f}"
    return str(value)


# =============================================================================
# Convenience Functions
# =============================================================================

def sparkline_stats(data: DataSequence) -> str:
    """
    Generate a quick statistical summary with sparkline.
    
    Args:
        data: Sequence of numeric values
    
    Returns:
        Statistical summary string
    
    Examples:
        >>> sparkline_stats([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        '▁▂▃▄▅▆▇█ n=10 min=1 max=10 avg=5.5'
    """
    if not data:
        return 'no data'
    
    data = list(data)
    n = len(data)
    mn = min(data)
    mx = max(data)
    avg = sum(data) / n
    
    line = sparkline(data)
    line += f" n={n} min={mn} max={mx} avg={avg:.1f}"
    
    return line


def mini_chart(
    data: DataSequence,
    chart_type: str = 'line'
) -> str:
    """
    Generate a quick mini chart (single function for common cases).
    
    Args:
        data: Sequence of numeric values
        chart_type: Type of chart ('line', 'bar', 'gauge', 'trend')
    
    Returns:
        Mini chart string
    
    Examples:
        >>> mini_chart([1, 2, 3, 4, 5], 'line')
        '▁▂▃▄▅'
        >>> mini_chart([75, 100], 'gauge')
        '██████████░░░░░░░░░░░ 75%'
    """
    if not data:
        return ''
    
    data = list(data)
    
    if chart_type == 'line':
        return sparkline(data)
    elif chart_type == 'bar':
        return ''.join(VERTICAL_BLOCKS[min(8, int(v))] for v in data)
    elif chart_type == 'gauge':
        return gauge_with_value(data[0], data[1] if len(data) > 1 else 100)
    elif chart_type == 'trend':
        return trend_sparkline(data)
    else:
        return sparkline(data)


# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == '__main__':
    # Demo
    print("=" * 60)
    print("Sparkline Utilities Demo")
    print("=" * 60)
    
    # Basic sparkline
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"\nBasic sparkline: {sparkline(data)}")
    print(f"ASCII sparkline: {sparkline(data, style=SparklineStyle.ASCII)}")
    print(f"Braille sparkline: {sparkline_braille(data)}")
    
    # Multi-line sparkline
    print("\nMulti-line sparkline:")
    print(sparkline_multiline(data, width=20, height=4))
    
    # Bar chart
    print("\nBar chart:")
    print(bar_chart([3, 7, 2, 5, 9, 4, 6], labels=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']))
    
    # Horizontal bar chart
    print("\nHorizontal bar chart:")
    print(horizontal_bar_chart(['A', 'B', 'C', 'D', 'E'], [30, 50, 20, 80, 45]))
    
    # Trend indicators
    print(f"\nTrend indicator: {trend_indicator(data)}")
    print(f"Trend sparkline: {trend_sparkline(data)}")
    print(f"Delta indicator: {delta_indicator(100, 110)}")
    
    # Gauge
    print(f"\nGauge: {gauge(75, 100, 10)}")
    print(f"Gauge with value: {gauge_with_value(75, 100, 20)}")
    
    # Win/loss
    print(f"\nWin/loss: {win_loss_sparkline([1, 1, -1, 0, 1, -1, 1, 1])}")
    
    # Histogram
    print("\nHistogram:")
    print(histogram([1, 1, 2, 2, 2, 3, 3, 4, 5, 5, 5, 5, 6, 7, 8, 9, 10], bins=5))
    
    # Stats
    print(f"\nSparkline stats: {sparkline_stats(data)}")