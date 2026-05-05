#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Table Utilities Examples
======================================
Demonstrates various table formatting capabilities.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Table, Column, Cell, TableConfig,
    Align, Style,
    create_table, format_table, format_simple_table,
    format_grid_table, format_markdown_table, format_html_table,
    format_csv, format_columns, format_list, format_key_value,
    align_columns, colored_table
)


def example_basic():
    """Basic table examples."""
    print("=" * 50)
    print("BASIC TABLE EXAMPLES")
    print("=" * 50)
    
    headers = ['Name', 'Age', 'City']
    rows = [
        ['Alice', 25, 'New York'],
        ['Bob', 30, 'London'],
        ['Charlie', 35, 'Tokyo'],
        ['Diana', 28, 'Paris'],
    ]
    
    print("\n--- Simple Style ---")
    print(format_simple_table(headers, rows))
    
    print("\n--- Grid Style ---")
    print(format_grid_table(headers, rows))
    
    print("\n--- Box Style ---")
    config = TableConfig(style=Style.BOX)
    table = Table(headers=headers, config=config)
    table.add_rows(rows)
    print(table.render())


def example_styles():
    """All style variations."""
    print("\n" + "=" * 50)
    print("ALL TABLE STYLES")
    print("=" * 50)
    
    headers = ['Product', 'Price', 'Qty']
    rows = [
        ['Apple', 1.50, 100],
        ['Banana', 0.75, 200],
        ['Orange', 2.00, 150],
    ]
    
    styles = [
        ('Simple', Style.SIMPLE),
        ('Grid', Style.GRID),
        ('Box', Style.BOX),
        ('Minimal', Style.MINIMAL),
        ('Compact', Style.COMPACT),
        ('Markdown', Style.MARKDOWN),
        ('CSV', Style.CSV),
    ]
    
    for name, style in styles:
        print(f"\n--- {name} ---")
        result = format_table(headers, rows, style)
        if style == Style.HTML:
            print(result[:200] + "...")
        else:
            print(result)


def example_alignment():
    """Column alignment examples."""
    print("\n" + "=" * 50)
    print("COLUMN ALIGNMENT")
    print("=" * 50)
    
    table = Table(columns=[
        Column('Left', align=Align.LEFT, width=12),
        Column('Center', align=Align.CENTER, width=12),
        Column('Right', align=Align.RIGHT, width=12),
    ])
    
    table.add_rows([
        ['A', 'B', 'C'],
        ['Short', 'Medium', 'LongText'],
        ['1', '2', '3'],
        ['abc', 'def', 'ghi'],
    ])
    
    print(table.render(Style.GRID))


def example_box_styles():
    """Different box drawing styles."""
    print("\n" + "=" * 50)
    print("BOX DRAWING STYLES")
    print("=" * 50)
    
    box_styles = ['light', 'heavy', 'double', 'rounded']
    
    for style_name in box_styles:
        print(f"\n--- {style_name.capitalize()} ---")
        config = TableConfig(style=Style.BOX, border_style=style_name)
        table = Table(headers=['A', 'B', 'C'], config=config)
        table.add_row([1, 2, 3])
        table.add_row([4, 5, 6])
        print(table.render())


def example_sorting():
    """Table sorting examples."""
    print("\n" + "=" * 50)
    print("TABLE SORTING")
    print("=" * 50)
    
    table = Table(['Name', 'Score', 'Rank'])
    table.add_rows([
        ['Alice', 85, 3],
        ['Bob', 95, 1],
        ['Charlie', 90, 2],
        ['Diana', 80, 4],
    ])
    
    print("\n--- Original Order ---")
    print(table.render(Style.SIMPLE))
    
    print("\n--- Sorted by Score (descending) ---")
    table.sort(1, reverse=True)
    print(table.render(Style.SIMPLE))
    
    print("\n--- Sorted by Name (ascending) ---")
    table.sort(0)
    print(table.render(Style.SIMPLE))


def example_filtering():
    """Table filtering examples."""
    print("\n" + "=" * 50)
    print("TABLE FILTERING")
    print("=" * 50)
    
    table = Table(['ID', 'Category', 'Value'])
    table.add_rows([
        [1, 'A', 100],
        [2, 'B', 200],
        [3, 'A', 150],
        [4, 'B', 250],
        [5, 'A', 50],
    ])
    
    print("\n--- Original Table ---")
    print(table.render(Style.SIMPLE))
    
    print("\n--- Filtered: Category A ---")
    filtered = table.filter(lambda row: row[1].value == 'A')
    print(filtered.render(Style.SIMPLE))
    
    print("\n--- Filtered: Value > 150 ---")
    filtered2 = table.filter(lambda row: row[2].value > 150)
    print(filtered2.render(Style.SIMPLE))


def example_formatting():
    """Convenience formatting functions."""
    print("\n" + "=" * 50)
    print("CONVENIENCE FUNCTIONS")
    print("=" * 50)
    
    print("\n--- format_list ---")
    print(format_list(['Item 1', 'Item 2', 'Item 3'], header='Items'))
    
    print("\n--- format_key_value ---")
    config = {
        'name': 'Alice',
        'age': 25,
        'city': 'New York',
        'job': 'Engineer',
    }
    print(format_key_value(config))
    
    print("\n--- format_columns ---")
    data = [
        {'name': 'Alice', 'score': 85, 'passed': True},
        {'name': 'Bob', 'score': 90, 'passed': True},
        {'name': 'Charlie', 'score': 60, 'passed': False},
    ]
    print(format_columns(data, columns=['name', 'score', 'passed']))


def example_markdown():
    """Markdown table examples."""
    print("\n" + "=" * 50)
    print("MARKDOWN OUTPUT")
    print("=" * 50)
    
    headers = ['Feature', 'Status', 'Priority']
    rows = [
        ['Login', 'Done', 'High'],
        ['Dashboard', 'In Progress', 'Medium'],
        ['Reports', 'Planned', 'Low'],
    ]
    
    print(format_markdown_table(headers, rows))


def example_html():
    """HTML table examples."""
    print("\n" + "=" * 50)
    print("HTML OUTPUT")
    print("=" * 50)
    
    headers = ['Name', 'Email', 'Role']
    rows = [
        ['Alice', 'alice@example.com', 'Admin'],
        ['Bob', 'bob@example.com', 'User'],
    ]
    
    print(format_html_table(headers, rows))


def example_csv():
    """CSV output examples."""
    print("\n" + "=" * 50)
    print("CSV OUTPUT")
    print("=" * 50)
    
    headers = ['ID', 'Name', 'Score']
    rows = [
        [1, 'Alice', 85],
        [2, 'Bob', 90],
        [3, 'Charlie', 80],
    ]
    
    print(format_csv(headers, rows))


def example_advanced():
    """Advanced table configuration."""
    print("\n" + "=" * 50)
    print("ADVANCED CONFIGURATION")
    print("=" * 50)
    
    config = TableConfig(
        style=Style.GRID,
        padding=2,
        show_header=True,
        show_footer=True,
        row_separator=True,
    )
    
    table = Table(
        columns=[
            Column('Product', align=Align.LEFT, width=15),
            Column('Price', align=Align.RIGHT, width=10),
            Column('Stock', align=Align.CENTER, width=8),
        ],
        config=config
    )
    
    table.add_rows([
        ['Laptop', '$999', '50'],
        ['Mouse', '$25', '200'],
        ['Keyboard', '$75', '100'],
    ])
    
    table.set_footer(['Total', '$1099', '350'])
    
    print(table.render())


def example_colored():
    """Colored table examples (ANSI)."""
    print("\n" + "=" * 50)
    print("COLORED TABLES (ANSI)")
    print("=" * 50)
    
    # Note: Colors only visible in terminal with ANSI support
    result = colored_table(
        ['Status', 'Value', 'Note'],
        [
            ['SUCCESS', '100', 'All good'],
            ['WARNING', '50', 'Check needed'],
            ['ERROR', '0', 'Failed'],
        ],
        header_color='cyan',
        row_colors=[
            ['green', None, None],
            ['yellow', None, None],
            ['red', None, None],
        ]
    )
    print(result)


def main():
    """Run all examples."""
    example_basic()
    example_styles()
    example_alignment()
    example_box_styles()
    example_sorting()
    example_filtering()
    example_formatting()
    example_markdown()
    example_html()
    example_csv()
    example_advanced()
    example_colored()
    
    print("\n" + "=" * 50)
    print("ALL EXAMPLES COMPLETE")
    print("=" * 50)


if __name__ == '__main__':
    main()