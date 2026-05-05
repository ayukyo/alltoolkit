# Table Utilities Module

A comprehensive table formatting and rendering utility module for Python with zero external dependencies.

## Features

- **Multiple Table Styles**: Simple, Grid, Box, Minimal, Compact, Markdown, HTML, CSV
- **Column Alignment**: Left, Center, Right alignment per column
- **Custom Column Widths**: Fixed widths, min/max constraints
- **ANSI Color Support**: Colorize headers and cells
- **Unicode Box Drawing**: Light, Heavy, Double, Rounded border styles
- **Sorting**: Sort rows by any column (ascending/descending)
- **Filtering**: Filter rows by predicate function
- **Export Formats**: Markdown, HTML, CSV
- **Responsive Width Calculation**: Automatic column width detection
- **Cell Padding Control**: Customize padding and spacing

## Quick Start

```python
from table_utils import Table, Style, Align

# Simple table
table = Table(['Name', 'Age', 'City'])
table.add_rows([
    ['Alice', 25, 'New York'],
    ['Bob', 30, 'London'],
])
print(table.render())
```

## Table Styles

```python
# Simple - No borders
print(table.render(Style.SIMPLE))

# Grid - Unicode borders
print(table.render(Style.GRID))

# Box - Full box with borders
print(table.render(Style.BOX))

# Markdown - Markdown format
print(table.render(Style.MARKDOWN))

# HTML - HTML table
print(table.render(Style.HTML))

# CSV - CSV format
print(table.render(Style.CSV))
```

## Column Alignment

```python
from table_utils import Column, Align

table = Table(columns=[
    Column('Left', align=Align.LEFT),
    Column('Center', align=Align.CENTER),
    Column('Right', align=Align.RIGHT),
])
table.add_rows([
    ['A', 'B', 'C'],
    ['1', '2', '3'],
])
print(table.render())
```

## Convenience Functions

```python
from table_utils import (
    format_simple_table,
    format_markdown_table,
    format_html_table,
    format_key_value,
    format_columns,
)

# Quick formatting
print(format_simple_table(['A', 'B'], [[1, 2], [3, 4]]))
print(format_markdown_table(['Name', 'Score'], [['Alice', 85]]))
print(format_key_value({'name': 'Alice', 'age': 25}))

# Dictionary data
data = [{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}]
print(format_columns(data))
```

## Sorting

```python
table = Table(['Name', 'Score'])
table.add_rows([
    ['Alice', 85],
    ['Bob', 90],
    ['Charlie', 80],
])
table.sort(1, reverse=True)  # Sort by Score descending
print(table.render())
```

## Filtering

```python
table = Table(['ID', 'Value'])
table.add_rows([[1, 'a'], [2, 'b'], [3, 'c'], [4, 'd']])

# Filter rows where ID > 2
filtered = table.filter(lambda row: row[0].value > 2)
print(filtered.render())
```

## Colored Tables

```python
from table_utils import colored_table, colorize

# Colored header
result = colored_table(
    ['Status', 'Value'],
    [['OK', '100'], ['Error', '0']],
    header_color='cyan',
    row_colors=[['green', None], ['red', None]]
)

# Manual coloring
print(colorize('Error', 'red'))
```

## Box Styles

```python
from table_utils import Table, TableConfig, Style

# Light (default)
config = TableConfig(style=Style.BOX, border_style='light')

# Heavy
config = TableConfig(style=Style.BOX, border_style='heavy')

# Double
config = TableConfig(style=Style.BOX, border_style='double')

# Rounded
config = TableConfig(style=Style.BOX, border_style='rounded')
```

## Advanced Configuration

```python
from table_utils import Table, TableConfig, Column, Align, Style

config = TableConfig(
    style=Style.GRID,
    padding=2,
    show_header=True,
    show_footer=True,
    row_separator=True,
    use_colors=True,
)

table = Table(
    columns=[
        Column('Name', align=Align.LEFT, width=15),
        Column('Score', align=Align.RIGHT, color='green'),
    ],
    config=config
)

table.add_rows([
    ['Alice', 85],
    ['Bob', 90],
])
table.set_footer(['Average', 87.5])
print(table.render())
```

## API Reference

### Classes

- `Table(headers, columns, config)` - Main table class
- `Column(name, align, width, ...)` - Column definition
- `Cell(value, align, color, format)` - Cell definition
- `TableConfig(style, padding, ...)` - Configuration options

### Enums

- `Align.LEFT`, `Align.CENTER`, `Align.RIGHT` - Alignment options
- `Style.SIMPLE`, `Style.GRID`, `Style.BOX`, `Style.MARKDOWN`, `Style.HTML`, `Style.CSV` - Style options

### Functions

- `create_table(headers, rows, style)` - Create table
- `format_table(headers, rows, style, align)` - Format table
- `format_simple_table(headers, rows)` - Simple format
- `format_grid_table(headers, rows)` - Grid format
- `format_markdown_table(headers, rows)` - Markdown format
- `format_html_table(headers, rows)` - HTML format
- `format_csv(headers, rows)` - CSV format
- `format_columns(data, columns, style)` - Format dictionaries
- `format_list(items, header, style)` - Format list
- `format_key_value(data, style)` - Format key-value pairs
- `align_columns(rows, align, padding)` - Align columns
- `colorize(text, color)` - Apply ANSI color
- `strip_colors(text)` - Remove ANSI colors
- `colored_table(headers, rows, header_color, row_colors)` - Colored table

## License

MIT License - Part of AllToolkit