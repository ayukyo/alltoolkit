#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Table Utilities Module
====================================
A comprehensive table formatting and rendering utility module for Python with zero external dependencies.

Features:
    - Multiple table styles (simple, grid, box, markdown, HTML)
    - Column alignment (left, center, right)
    - Custom column widths
    - ANSI color support for cells
    - Header and footer support
    - Table sorting by column
    - Export to various formats (CSV, Markdown, HTML)
    - Unicode box-drawing characters
    - Responsive width calculation
    - Cell padding and spacing control

Author: AllToolkit Contributors
License: MIT
"""

import re
from typing import Union, List, Tuple, Optional, Dict, Any, Callable, Iterator
from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# Enums
# ============================================================================

class Align(Enum):
    """Column alignment options."""
    LEFT = 'left'
    CENTER = 'center'
    RIGHT = 'right'


class Style(Enum):
    """Table style options."""
    SIMPLE = 'simple'
    GRID = 'grid'
    BOX = 'box'
    MINIMAL = 'minimal'
    COMPACT = 'compact'
    MARKDOWN = 'markdown'
    HTML = 'html'
    CSV = 'csv'


# ============================================================================
# ANSI Color Codes
# ============================================================================

ANSI_COLORS = {
    'reset': '\033[0m',
    'bold': '\033[1m',
    'dim': '\033[2m',
    'italic': '\033[3m',
    'underline': '\033[4m',
    'black': '\033[30m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    'bg_black': '\033[40m',
    'bg_red': '\033[41m',
    'bg_green': '\033[42m',
    'bg_yellow': '\033[43m',
    'bg_blue': '\033[44m',
    'bg_magenta': '\033[45m',
    'bg_cyan': '\033[46m',
    'bg_white': '\033[47m',
}


# ============================================================================
# Box Drawing Characters
# ============================================================================

BOX_CHARS = {
    'light': {
        'horizontal': '─',
        'vertical': '│',
        'top_left': '┌',
        'top_right': '┐',
        'bottom_left': '└',
        'bottom_right': '┘',
        'left_tee': '├',
        'right_tee': '┤',
        'top_tee': '┬',
        'bottom_tee': '┴',
        'cross': '┼',
    },
    'heavy': {
        'horizontal': '━',
        'vertical': '┃',
        'top_left': '┏',
        'top_right': '┓',
        'bottom_left': '┗',
        'bottom_right': '┛',
        'left_tee': '┣',
        'right_tee': '┫',
        'top_tee': '┳',
        'bottom_tee': '┻',
        'cross': '╋',
    },
    'double': {
        'horizontal': '═',
        'vertical': '║',
        'top_left': '╔',
        'top_right': '╗',
        'bottom_left': '╚',
        'bottom_right': '╝',
        'left_tee': '╠',
        'right_tee': '╣',
        'top_tee': '╦',
        'bottom_tee': '╩',
        'cross': '╬',
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
}


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class Column:
    """Table column definition."""
    name: str
    align: Align = Align.LEFT
    width: Optional[int] = None
    min_width: int = 1
    max_width: Optional[int] = None
    format: Optional[str] = None
    color: Optional[str] = None
    header_color: Optional[str] = None
    visible: bool = True
    
    def __post_init__(self):
        """Validate column settings."""
        if self.min_width < 1:
            self.min_width = 1
        if self.max_width is not None and self.max_width < self.min_width:
            self.max_width = self.min_width


@dataclass
class Cell:
    """Table cell definition."""
    value: Any
    align: Optional[Align] = None
    color: Optional[str] = None
    format: Optional[str] = None
    
    def formatted_value(self, default_format: Optional[str] = None) -> str:
        """Get formatted cell value."""
        fmt = self.format or default_format
        
        if fmt:
            try:
                return fmt.format(self.value)
            except (ValueError, TypeError):
                pass
        
        if self.value is None:
            return ''
        
        return str(self.value)


@dataclass
class TableConfig:
    """Table configuration."""
    style: Style = Style.GRID
    padding: int = 1
    border_style: str = 'light'
    show_header: bool = True
    show_footer: bool = False
    header_align: Align = Align.CENTER
    footer_align: Align = Align.RIGHT
    use_colors: bool = True
    wrap_text: bool = True
    max_table_width: Optional[int] = None
    sort_column: Optional[int] = None
    sort_reverse: bool = False
    row_separator: bool = False


# ============================================================================
# Table Class
# ============================================================================

class Table:
    """
    A table representation with formatting capabilities.
    
    Examples:
        >>> table = Table(['Name', 'Age', 'City'])
        >>> table.add_row(['Alice', 25, 'New York'])
        >>> table.add_row(['Bob', 30, 'London'])
        >>> print(table.render())
    """
    
    def __init__(
        self,
        headers: Optional[List[str]] = None,
        columns: Optional[List[Column]] = None,
        config: Optional[TableConfig] = None
    ):
        """
        Initialize a table.
        
        Args:
            headers: List of header names (simple mode)
            columns: List of Column objects (advanced mode)
            config: Table configuration
        """
        self._columns: List[Column] = []
        self._rows: List[List[Cell]] = []
        self._footer: List[Cell] = []
        
        if columns:
            self._columns = columns
        elif headers:
            self._columns = [Column(name=h) for h in headers]
        
        self.config = config or TableConfig()
    
    @property
    def columns(self) -> List[Column]:
        """Get visible columns."""
        return [c for c in self._columns if c.visible]
    
    @property
    def num_columns(self) -> int:
        """Get number of visible columns."""
        return len(self.columns)
    
    @property
    def num_rows(self) -> int:
        """Get number of rows."""
        return len(self._rows)
    
    def add_column(
        self,
        name: str,
        align: Align = Align.LEFT,
        width: Optional[int] = None,
        **kwargs
    ) -> None:
        """
        Add a column to the table.
        
        Args:
            name: Column header name
            align: Column alignment
            width: Fixed column width
            **kwargs: Additional Column arguments
        """
        self._columns.append(Column(name=name, align=align, width=width, **kwargs))
    
    def add_row(self, values: List[Any], colors: Optional[List[str]] = None) -> None:
        """
        Add a row to the table.
        
        Args:
            values: List of cell values
            colors: Optional list of cell colors
        """
        cells = []
        for i, value in enumerate(values):
            color = colors[i] if colors and i < len(colors) else None
            cells.append(Cell(value=value, color=color))
        self._rows.append(cells)
    
    def add_rows(self, rows: List[List[Any]]) -> None:
        """
        Add multiple rows to the table.
        
        Args:
            rows: List of row data lists
        """
        for row in rows:
            self.add_row(row)
    
    def set_footer(self, values: List[Any]) -> None:
        """
        Set footer row.
        
        Args:
            values: Footer cell values
        """
        self._footer = [Cell(value=v) for v in values]
    
    def clear_rows(self) -> None:
        """Clear all rows."""
        self._rows = []
    
    def get_row(self, index: int) -> List[Cell]:
        """
        Get a row by index.
        
        Args:
            index: Row index
        
        Returns:
            List of cells in the row
        """
        return self._rows[index]
    
    def get_cell(self, row_index: int, col_index: int) -> Cell:
        """
        Get a cell by position.
        
        Args:
            row_index: Row index
            col_index: Column index
        
        Returns:
            Cell object
        """
        return self._rows[row_index][col_index]
    
    def set_cell(self, row_index: int, col_index: int, value: Any) -> None:
        """
        Set a cell value.
        
        Args:
            row_index: Row index
            col_index: Column index
            value: New cell value
        """
        if row_index < len(self._rows) and col_index < len(self._rows[row_index]):
            self._rows[row_index][col_index].value = value
    
    def sort(self, column_index: int, reverse: bool = False) -> None:
        """
        Sort rows by a column.
        
        Args:
            column_index: Column index to sort by
            reverse: Sort in descending order
        """
        def sort_key(row: List[Cell]) -> Any:
            if column_index < len(row):
                return row[column_index].value
            return None
        
        self._rows.sort(key=sort_key, reverse=reverse)
    
    def filter(self, predicate: Callable[[List[Cell]], bool]) -> 'Table':
        """
        Filter rows by a predicate function.
        
        Args:
            predicate: Function that takes a row and returns True/False
        
        Returns:
            New filtered Table
        """
        filtered = Table(columns=self._columns, config=self.config)
        for row in self._rows:
            if predicate(row):
                filtered._rows.append(row)
        return filtered
    
    def map(self, func: Callable[[List[Cell]], List[Cell]]) -> 'Table':
        """
        Transform rows with a function.
        
        Args:
            func: Function that transforms a row
        
        Returns:
            New transformed Table
        """
        mapped = Table(columns=self._columns, config=self.config)
        for row in self._rows:
            mapped._rows.append(func(row))
        return mapped
    
    def __iter__(self) -> Iterator[List[Cell]]:
        """Iterate over rows."""
        return iter(self._rows)
    
    def __len__(self) -> int:
        """Get number of rows."""
        return len(self._rows)
    
    def __getitem__(self, index: int) -> List[Cell]:
        """Get row by index."""
        return self._rows[index]
    
    def _calculate_widths(self) -> List[int]:
        """Calculate column widths."""
        widths = []
        visible_cols = self.columns
        
        for i, col in enumerate(visible_cols):
            if col.width:
                widths.append(col.width)
            else:
                max_len = len(col.name)
                # Check rows
                for row in self._rows:
                    if i < len(row):
                        cell_text = row[i].formatted_value(col.format)
                        max_len = max(max_len, len(cell_text))
                # Check footer
                if self._footer and i < len(self._footer):
                    footer_text = self._footer[i].formatted_value(col.format)
                    max_len = max(max_len, len(footer_text))
                
                width = max(col.min_width, max_len + self.config.padding * 2)
                if col.max_width:
                    width = min(width, col.max_width)
                widths.append(width)
        
        return widths
    
    def _align_cell(self, text: str, width: int, align: Align, pad: int = 1) -> str:
        """Align cell content."""
        text_len = len(text)
        available = width - pad * 2
        
        if text_len > available and self.config.wrap_text:
            text = self._wrap_text(text, available)
            text_len = len(text)
        
        if align == Align.LEFT:
            return text.ljust(available)[:available]
        elif align == Align.RIGHT:
            return text.rjust(available)[:available]
        else:
            return text.center(available)[:available]
    
    def _wrap_text(self, text: str, width: int) -> str:
        """Wrap text to fit width."""
        if len(text) <= width:
            return text
        return text[:width - 1] + '…'
    
    def _apply_color(self, text: str, color: Optional[str]) -> str:
        """Apply ANSI color to text."""
        if not self.config.use_colors or not color:
            return text
        
        color_lower = color.lower()
        if color_lower in ANSI_COLORS:
            return f"{ANSI_COLORS[color_lower]}{text}{ANSI_COLORS['reset']}"
        return text
    
    def render(self, style: Optional[Style] = None) -> str:
        """
        Render the table as a string.
        
        Args:
            style: Override table style
        
        Returns:
            Formatted table string
        """
        render_style = style or self.config.style
        
        if render_style == Style.HTML:
            return self._render_html()
        elif render_style == Style.MARKDOWN:
            return self._render_markdown()
        elif render_style == Style.CSV:
            return self._render_csv()
        else:
            return self._render_text(render_style)
    
    def _render_text(self, style: Style) -> str:
        """Render table as plain text."""
        widths = self._calculate_widths()
        visible_cols = self.columns
        chars = BOX_CHARS.get(self.config.border_style, BOX_CHARS['light'])
        pad = self.config.padding
        
        lines = []
        
        # Apply sorting if configured
        if self.config.sort_column is not None:
            self.sort(self.config.sort_column, self.config.sort_reverse)
        
        # Top border
        if style in (Style.GRID, Style.BOX):
            top_line = chars['top_left'] + chars['horizontal']
            for i, w in enumerate(widths):
                top_line += chars['horizontal'] * w
                if i < len(widths) - 1:
                    top_line += chars['top_tee'] + chars['horizontal']
            top_line += chars['horizontal'] + chars['top_right']
            lines.append(top_line)
        
        # Header row
        if self.config.show_header and visible_cols:
            header_parts = []
            for i, (col, w) in enumerate(zip(visible_cols, widths)):
                aligned = self._align_cell(col.name, w, self.config.header_align, pad)
                colored = self._apply_color(' ' * pad + aligned + ' ' * pad, col.header_color)
                header_parts.append(colored)
            
            if style == Style.SIMPLE:
                lines.append(' '.join(header_parts))
                separator = '-' * (sum(widths) + len(widths) - 1)
                lines.append(separator)
            elif style == Style.MINIMAL:
                lines.append(' | '.join([p.strip() for p in header_parts]))
            elif style == Style.COMPACT:
                lines.append(' '.join([p.strip() for p in header_parts]))
            else:
                row_line = chars['vertical'] + ' ' + chars['vertical']
                row_line = chars['vertical']
                for i, part in enumerate(header_parts):
                    row_line += part
                    if i < len(header_parts) - 1:
                        row_line += chars['vertical']
                row_line += chars['vertical']
                lines.append(row_line)
        
        # Header separator
        if style in (Style.GRID, Style.BOX) and self.config.show_header:
            sep_line = chars['left_tee'] + chars['horizontal']
            for i, w in enumerate(widths):
                sep_line += chars['horizontal'] * w
                if i < len(widths) - 1:
                    sep_line += chars['cross'] + chars['horizontal']
            sep_line += chars['horizontal'] + chars['right_tee']
            lines.append(sep_line)
        elif style == Style.MARKDOWN:
            sep_parts = []
            for i, (col, w) in enumerate(zip(visible_cols, widths)):
                if col.align == Align.LEFT:
                    sep_parts.append(':' + '-' * (w - 1))
                elif col.align == Align.RIGHT:
                    sep_parts.append('-' * (w - 1) + ':')
                else:
                    sep_parts.append('-' * w)
            lines.append('|' + '|'.join(sep_parts) + '|')
        
        # Data rows
        for row_idx, row in enumerate(self._rows):
            row_parts = []
            for i, (col, w) in enumerate(zip(visible_cols, widths)):
                if i < len(row):
                    cell = row[i]
                    text = cell.formatted_value(col.format)
                    align = cell.align or col.align
                    aligned = self._align_cell(text, w, align, pad)
                    color = cell.color or col.color
                    colored = self._apply_color(' ' * pad + aligned + ' ' * pad, color)
                else:
                    colored = ' ' * w
                row_parts.append(colored)
            
            if style == Style.SIMPLE:
                lines.append(' '.join(row_parts))
            elif style == Style.MINIMAL:
                lines.append(' | '.join([p.strip() for p in row_parts]))
            elif style == Style.COMPACT:
                lines.append(' '.join([p.strip() for p in row_parts]))
            else:
                row_line = chars['vertical']
                for i, part in enumerate(row_parts):
                    row_line += part
                    if i < len(row_parts) - 1:
                        row_line += chars['vertical']
                row_line += chars['vertical']
                lines.append(row_line)
            
            # Row separator
            if self.config.row_separator and row_idx < len(self._rows) - 1:
                if style in (Style.GRID, Style.BOX):
                    sep_line = chars['left_tee'] + chars['horizontal']
                    for i, w in enumerate(widths):
                        sep_line += chars['horizontal'] * w
                        if i < len(widths) - 1:
                            sep_line += chars['cross'] + chars['horizontal']
                    sep_line += chars['horizontal'] + chars['right_tee']
                    lines.append(sep_line)
        
        # Footer row
        if self.config.show_footer and self._footer:
            footer_parts = []
            for i, (col, w) in enumerate(zip(visible_cols, widths)):
                if i < len(self._footer):
                    cell = self._footer[i]
                    text = cell.formatted_value(col.format)
                    aligned = self._align_cell(text, w, self.config.footer_align, pad)
                    colored = self._apply_color(' ' * pad + aligned + ' ' * pad, cell.color)
                else:
                    colored = ' ' * w
                footer_parts.append(colored)
            
            if style in (Style.GRID, Style.BOX):
                sep_line = chars['left_tee'] + chars['horizontal']
                for i, w in enumerate(widths):
                    sep_line += chars['horizontal'] * w
                    if i < len(widths) - 1:
                        sep_line += chars['cross'] + chars['horizontal']
                sep_line += chars['horizontal'] + chars['right_tee']
                lines.append(sep_line)
                
                row_line = chars['vertical']
                for i, part in enumerate(footer_parts):
                    row_line += part
                    if i < len(footer_parts) - 1:
                        row_line += chars['vertical']
                row_line += chars['vertical']
                lines.append(row_line)
            else:
                lines.append(' '.join(footer_parts))
        
        # Bottom border
        if style in (Style.GRID, Style.BOX):
            bottom_line = chars['bottom_left'] + chars['horizontal']
            for i, w in enumerate(widths):
                bottom_line += chars['horizontal'] * w
                if i < len(widths) - 1:
                    bottom_line += chars['bottom_tee'] + chars['horizontal']
            bottom_line += chars['horizontal'] + chars['bottom_right']
            lines.append(bottom_line)
        
        return '\n'.join(lines)
    
    def _render_markdown(self) -> str:
        """Render table as Markdown."""
        widths = self._calculate_widths()
        visible_cols = self.columns
        
        lines = []
        
        # Header
        header = '|' + '|'.join([c.name for c in visible_cols]) + '|'
        lines.append(header)
        
        # Separator
        sep_parts = []
        for col in visible_cols:
            if col.align == Align.LEFT:
                sep_parts.append(':---')
            elif col.align == Align.RIGHT:
                sep_parts.append('---:')
            else:
                sep_parts.append(':---:')
        lines.append('|' + '|'.join(sep_parts) + '|')
        
        # Rows
        for row in self._rows:
            row_parts = []
            for i, col in enumerate(visible_cols):
                if i < len(row):
                    text = row[i].formatted_value(col.format)
                else:
                    text = ''
                row_parts.append(text)
            lines.append('|' + '|'.join(row_parts) + '|')
        
        return '\n'.join(lines)
    
    def _render_html(self) -> str:
        """Render table as HTML."""
        visible_cols = self.columns
        
        lines = ['<table>']
        
        # Header
        if self.config.show_header:
            lines.append('<thead>')
            lines.append('<tr>')
            for col in visible_cols:
                align_attr = f' align="{col.align.value}"' if col.align != Align.LEFT else ''
                lines.append(f'<th{align_attr}>{col.name}</th>')
            lines.append('</tr>')
            lines.append('</thead>')
        
        # Body
        lines.append('<tbody>')
        for row in self._rows:
            lines.append('<tr>')
            for i, col in enumerate(visible_cols):
                if i < len(row):
                    text = row[i].formatted_value(col.format)
                    align_attr = f' align="{col.align.value}"' if col.align != Align.LEFT else ''
                    lines.append(f'<td{align_attr}>{text}</td>')
                else:
                    lines.append('<td></td>')
            lines.append('</tr>')
        lines.append('</tbody>')
        
        # Footer
        if self.config.show_footer and self._footer:
            lines.append('<tfoot>')
            lines.append('<tr>')
            for i, col in enumerate(visible_cols):
                if i < len(self._footer):
                    text = self._footer[i].formatted_value(col.format)
                    lines.append(f'<td>{text}</td>')
                else:
                    lines.append('<td></td>')
            lines.append('</tr>')
            lines.append('</tfoot>')
        
        lines.append('</table>')
        
        return '\n'.join(lines)
    
    def _render_csv(self) -> str:
        """Render table as CSV."""
        visible_cols = self.columns
        lines = []
        
        # Header
        if self.config.show_header:
            lines.append(','.join([self._csv_escape(c.name) for c in visible_cols]))
        
        # Rows
        for row in self._rows:
            row_parts = []
            for i, col in enumerate(visible_cols):
                if i < len(row):
                    text = row[i].formatted_value(col.format)
                    row_parts.append(self._csv_escape(text))
                else:
                    row_parts.append('')
            lines.append(','.join(row_parts))
        
        return '\n'.join(lines)
    
    def _csv_escape(self, text: str) -> str:
        """Escape text for CSV format."""
        if ',' in text or '"' in text or '\n' in text:
            return '"' + text.replace('"', '""') + '"'
        return text
    
    def __str__(self) -> str:
        """String representation."""
        return self.render()
    
    def __repr__(self) -> str:
        """Repr representation."""
        return f"Table(columns={self.num_columns}, rows={self.num_rows})"


# ============================================================================
# Convenience Functions
# ============================================================================

def create_table(
    headers: List[str],
    rows: Optional[List[List[Any]]] = None,
    style: Style = Style.GRID
) -> Table:
    """
    Create a table from headers and rows.
    
    Args:
        headers: Column headers
        rows: Optional data rows
        style: Table style
    
    Returns:
        Table object
    
    Examples:
        >>> table = create_table(['A', 'B'], [[1, 2], [3, 4]])
        >>> print(table.render())
    """
    table = Table(headers=headers, config=TableConfig(style=style))
    if rows:
        table.add_rows(rows)
    return table


def format_table(
    headers: List[str],
    rows: List[List[Any]],
    style: Style = Style.GRID,
    align: Align = Align.LEFT
) -> str:
    """
    Format data as a table string.
    
    Args:
        headers: Column headers
        rows: Data rows
        style: Table style
        align: Default alignment
    
    Returns:
        Formatted table string
    
    Examples:
        >>> print(format_table(['A', 'B'], [[1, 2], [3, 4]], Style.SIMPLE))
        A B
        -----
        1 2
        3 4
    """
    table = Table(headers=headers, config=TableConfig(style=style))
    for col in table._columns:
        col.align = align
    table.add_rows(rows)
    return table.render()


def format_simple_table(headers: List[str], rows: List[List[Any]]) -> str:
    """
    Format a simple table (no borders).
    
    Args:
        headers: Column headers
        rows: Data rows
    
    Returns:
        Simple table string
    
    Examples:
        >>> format_simple_table(['Name', 'Age'], [['Alice', 25]])
        'Name Age\\n-----\\nAlice 25'
    """
    return format_table(headers, rows, Style.SIMPLE)


def format_grid_table(headers: List[str], rows: List[List[Any]]) -> str:
    """
    Format a grid table (with borders).
    
    Args:
        headers: Column headers
        rows: Data rows
    
    Returns:
        Grid table string
    """
    return format_table(headers, rows, Style.GRID)


def format_markdown_table(headers: List[str], rows: List[List[Any]]) -> str:
    """
    Format a Markdown table.
    
    Args:
        headers: Column headers
        rows: Data rows
    
    Returns:
        Markdown table string
    
    Examples:
        >>> print(format_markdown_table(['A', 'B'], [[1, 2]]))
        |A|B|
        |---|---|
        |1|2|
    """
    return format_table(headers, rows, Style.MARKDOWN)


def format_html_table(headers: List[str], rows: List[List[Any]]) -> str:
    """
    Format an HTML table.
    
    Args:
        headers: Column headers
        rows: Data rows
    
    Returns:
        HTML table string
    """
    return format_table(headers, rows, Style.HTML)


def format_csv(headers: List[str], rows: List[List[Any]]) -> str:
    """
    Format data as CSV.
    
    Args:
        headers: Column headers
        rows: Data rows
    
    Returns:
        CSV string
    """
    return format_table(headers, rows, Style.CSV)


def format_columns(
    data: List[Dict[str, Any]],
    columns: Optional[List[str]] = None,
    style: Style = Style.GRID
) -> str:
    """
    Format dictionary data as a table.
    
    Args:
        data: List of dictionaries
        columns: Optional column names (uses dict keys if not provided)
        style: Table style
    
    Returns:
        Formatted table string
    
    Examples:
        >>> data = [{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}]
        >>> print(format_columns(data))
    """
    if not data:
        return ''
    
    headers = columns or list(data[0].keys())
    rows = [[d.get(h, '') for h in headers] for d in data]
    return format_table(headers, rows, style)


def format_list(
    items: List[Any],
    header: str = 'Value',
    style: Style = Style.SIMPLE
) -> str:
    """
    Format a list as a single-column table.
    
    Args:
        items: List of items
        header: Column header
        style: Table style
    
    Returns:
        Formatted table string
    
    Examples:
        >>> print(format_list(['a', 'b', 'c']))
    """
    return format_table([header], [[item] for item in items], style)


def format_key_value(
    data: Dict[str, Any],
    style: Style = Style.SIMPLE,
    key_header: str = 'Key',
    value_header: str = 'Value'
) -> str:
    """
    Format a dictionary as a key-value table.
    
    Args:
        data: Dictionary to format
        style: Table style
        key_header: Header for key column
        value_header: Header for value column
    
    Returns:
        Formatted table string
    
    Examples:
        >>> print(format_key_value({'a': 1, 'b': 2}))
    """
    rows = [[k, v] for k, v in data.items()]
    return format_table([key_header, value_header], rows, style)


def align_columns(
    rows: List[List[str]],
    align: Align = Align.LEFT,
    padding: int = 2
) -> str:
    """
    Align columns without table borders.
    
    Args:
        rows: Data rows (first row is header)
        align: Column alignment
        padding: Space between columns
    
    Returns:
        Aligned columns string
    """
    if not rows:
        return ''
    
    # Calculate widths
    num_cols = max(len(row) for row in rows)
    widths = [0] * num_cols
    
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    
    # Format rows
    lines = []
    for row in rows:
        parts = []
        for i in range(num_cols):
            text = str(row[i]) if i < len(row) else ''
            if align == Align.LEFT:
                parts.append(text.ljust(widths[i]))
            elif align == Align.RIGHT:
                parts.append(text.rjust(widths[i]))
            else:
                parts.append(text.center(widths[i]))
        lines.append((' ' * padding).join(parts))
    
    return '\n'.join(lines)


def column_widths(rows: List[List[str]], min_width: int = 1) -> List[int]:
    """
    Calculate column widths for data.
    
    Args:
        rows: Data rows
        min_width: Minimum width per column
    
    Returns:
        List of column widths
    """
    if not rows:
        return []
    
    num_cols = max(len(row) for row in rows)
    widths = [min_width] * num_cols
    
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    
    return widths


def pad_columns(
    rows: List[List[str]],
    widths: Optional[List[int]] = None,
    align: Align = Align.LEFT
) -> List[List[str]]:
    """
    Pad columns to specified widths.
    
    Args:
        rows: Data rows
        widths: Target widths (calculated if not provided)
        align: Alignment
    
    Returns:
        Padded rows
    """
    if not rows:
        return []
    
    if widths is None:
        widths = column_widths(rows)
    
    num_cols = len(widths)
    padded = []
    
    for row in rows:
        padded_row = []
        for i in range(num_cols):
            text = str(row[i]) if i < len(row) else ''
            if align == Align.LEFT:
                padded_row.append(text.ljust(widths[i]))
            elif align == Align.RIGHT:
                padded_row.append(text.rjust(widths[i]))
            else:
                padded_row.append(text.center(widths[i]))
        padded.append(padded_row)
    
    return padded


# ============================================================================
# ANSI Color Helpers
# ============================================================================

def colorize(text: str, color: str) -> str:
    """
    Apply ANSI color to text.
    
    Args:
        text: Text to colorize
        color: Color name (red, green, blue, etc.)
    
    Returns:
        Colorized text
    
    Examples:
        >>> colorize('Error', 'red')
        '\\033[31mError\\033[0m'
    """
    return f"{ANSI_COLORS.get(color.lower(), '')}{text}{ANSI_COLORS['reset']}"


def strip_colors(text: str) -> str:
    """
    Remove ANSI color codes from text.
    
    Args:
        text: Text with color codes
    
    Returns:
        Text without color codes
    """
    ansi_pattern = re.compile(r'\033\[[0-9;]*m')
    return ansi_pattern.sub('', text)


def colored_table(
    headers: List[str],
    rows: List[List[Any]],
    header_color: str = 'cyan',
    row_colors: Optional[List[List[str]]] = None
) -> str:
    """
    Create a table with colored headers.
    
    Args:
        headers: Column headers
        rows: Data rows
        header_color: Header color
        row_colors: Optional colors for each cell
    
    Returns:
        Colored table string
    """
    table = Table(headers=headers, config=TableConfig(use_colors=True))
    for col in table._columns:
        col.header_color = header_color
    
    for i, row in enumerate(rows):
        colors = row_colors[i] if row_colors and i < len(row_colors) else None
        table.add_row(row, colors)
    
    return table.render()


# ============================================================================
# Main Demo
# ============================================================================

if __name__ == '__main__':
    print("=== Basic Table Examples ===")
    
    # Simple table
    headers = ['Name', 'Age', 'City']
    rows = [
        ['Alice', 25, 'New York'],
        ['Bob', 30, 'London'],
        ['Charlie', 35, 'Tokyo'],
    ]
    
    print("\n--- Simple Style ---")
    print(format_simple_table(headers, rows))
    
    print("\n--- Grid Style ---")
    print(format_grid_table(headers, rows))
    
    print("\n--- Markdown Style ---")
    print(format_markdown_table(headers, rows))
    
    print("\n--- HTML Style ---")
    print(format_html_table(headers, rows)[:200] + "...")
    
    print("\n--- CSV Style ---")
    print(format_csv(headers, rows))
    
    print("\n=== Advanced Table Examples ===")
    
    # Table with alignment
    table = Table(headers=['Left', 'Center', 'Right'])
    table._columns[0].align = Align.LEFT
    table._columns[1].align = Align.CENTER
    table._columns[2].align = Align.RIGHT
    table.add_rows([
        ['A', 'B', 'C'],
        ['1', '2', '3'],
        ['abc', 'def', 'ghi'],
    ])
    print("\n--- Aligned Columns ---")
    print(table.render(Style.GRID))
    
    # Table with sorting
    table2 = Table(headers=['Name', 'Score', 'Rank'])
    table2.add_rows([
        ['Alice', 85, 2],
        ['Bob', 90, 1],
        ['Charlie', 80, 3],
    ])
    table2.sort(1, reverse=True)
    print("\n--- Sorted by Score (descending) ---")
    print(table2.render(Style.SIMPLE))
    
    # Key-value table
    print("\n--- Key-Value Table ---")
    print(format_key_value({'name': 'Alice', 'age': 25, 'city': 'New York'}))
    
    # Dictionary table
    print("\n--- Dictionary Table ---")
    data = [
        {'name': 'Alice', 'age': 25, 'city': 'New York'},
        {'name': 'Bob', 'age': 30, 'city': 'London'},
    ]
    print(format_columns(data))
    
    # Box styles
    print("\n=== Box Styles ===")
    for style_name in ['light', 'heavy', 'double', 'rounded']:
        config = TableConfig(style=Style.BOX, border_style=style_name)
        table3 = Table(headers=['A', 'B', 'C'], config=config)
        table3.add_row([1, 2, 3])
        print(f"\n--- {style_name} Style ---")
        print(table3.render())
    
    # Colored table
    print("\n=== Colored Table ===")
    print(colored_table(
        ['Status', 'Value'],
        [['OK', '100'], ['Warning', '50'], ['Error', '0']],
        header_color='cyan',
        row_colors=[['green', None], ['yellow', None], ['red', None]]
    ))
    
    print("\n=== Table Operations ===")
    table4 = Table(headers=['ID', 'Value'])
    table4.add_rows([[1, 'a'], [2, 'b'], [3, 'c'], [4, 'd']])
    
    print(f"Number of rows: {table4.num_rows}")
    print(f"Number of columns: {table4.num_columns}")
    
    filtered = table4.filter(lambda row: row[0].value > 2)
    print(f"Filtered (ID > 2): {filtered.num_rows} rows")
    print(filtered.render(Style.SIMPLE))
    
    print("\n=== Column Alignment Helper ===")
    aligned = align_columns(
        [['Name', 'Score'], ['Alice', 85], ['Bob', 90]],
        Align.RIGHT,
        padding=4
    )
    print(aligned)